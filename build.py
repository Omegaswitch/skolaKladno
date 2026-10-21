#!/usr/bin/env python3
"""Static site generator for zsmr.eu (Základní škola Maltézských rytířů, Kladno). Python 3.10+, standard library only.
Same architecture as maltezskyrad.cz: content/ -> dist/, no CMS, no database.

    python3 build.py                 preview build into dist/ (noindex, content-status labels shown)
    python3 build.py --production    production build (indexable, no status labels)
    python3 build.py serve [port]    preview build, then serve dist/ with _headers and _redirects applied
"""
import html
import json
import os
import re
import shutil
import struct
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent
CONTENT, STATIC, DIST = ROOT / "content", ROOT / "static", ROOT / "dist"
PRODUCTION = "--production" in sys.argv
SITE = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))
SB = SITE["supabase"]  # the shared database of the school sites; the key is the public one
ASSET_VERSION = datetime.now().strftime("%Y%m%d%H%M")
MONTHS = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"]
STATUS = {"verified": "Ověřený obsah", "existing": "Převzato ze stávajícího webu – čeká na revizi",
          "new": "Nový text – čeká na schválení", "approval": "Vyžaduje schválení školou nebo zřizovatelem"}
esc = lambda s: html.escape(str(s or ""), quote=True)


# ---------------------------------------------------------------- content


def read_doc(path):
    _, meta, body = path.read_text(encoding="utf-8").split("---\n", 2)
    return json.loads(meta), body.strip()


DYNAMIC_PAGE = re.compile(r"data-events|data-gallery")  # such pages are rendered on request by api/page.py


def load_pages():
    pages = {}
    for f in sorted((CONTENT / "pages").rglob("index.html")):
        meta, body = read_doc(f)
        pages[meta["url"]] = {**meta, "body": body}
    return pages


def load_news():
    news = []
    for f in (CONTENT / "news").rglob("*.html"):
        meta, body = read_doc(f)
        news.append({**meta, "body": body, "src": f.relative_to(ROOT).as_posix()})
    return sorted(news, key=lambda n: n["date"], reverse=True)


PAGES, NEWS = load_pages(), load_news()

# ---------------------------------------------------------------- published content (shared by the Order of Malta sites)
# Staff publish through /pridat-aktualitu/ (api/news.js). A post marked draft, or dated in the future, is kept in
# the repository but not built until it is due; a post an admin pinned is shown as a notice on the home page and
# the news listing; events live in content/events.json; a post with two or more photos is also in the gallery.
ALL_NEWS = NEWS
try:
    from zoneinfo import ZoneInfo
    BUILD_TIME = datetime.now(ZoneInfo("Europe/Prague")).strftime("%Y-%m-%dT%H:%M")  # Vercel builds in UTC
except Exception:
    BUILD_TIME = datetime.now().strftime("%Y-%m-%dT%H:%M")
NEWS = [n for n in ALL_NEWS if not n.get("draft") and str(n.get("date", ""))[:10] <= BUILD_TIME[:10]]  # a scheduled post goes out on its day
PINNED = [n for n in NEWS if n.get("pinned")]
EVENTS_FILE = CONTENT / "events.json"
EVENTS = sorted(json.loads(EVENTS_FILE.read_text(encoding="utf-8")), key=lambda e: e["start"]) if EVENTS_FILE.exists() else []
if "MONTHS_SHORT" not in globals():
    MONTHS_SHORT = ["led", "úno", "bře", "dub", "kvě", "čvn", "čvc", "srp", "zář", "říj", "lis", "pro"]


def pinned_html():
    """The notices an admin pinned, for the home page and the news listing."""
    return "".join(
        f'<aside class="pinned" aria-label="Důležité oznámení"><div class="wrap"><p><b>{esc(n["title"])}</b>'
        f'{" " + esc(n["excerpt"]) if n.get("excerpt") else ""} <a href="{n["url"]}">Více</a></p></div></aside>' for n in PINNED)


def photos_of(n):
    found = ([n["image"]] if n.get("image") else []) + re.findall(r'<img[^>]+src="(/media/[^"]+)"', n.get("body", ""))
    return list(dict.fromkeys(found))


def gallery_posts():
    return [n for n in NEWS if len(photos_of(n)) >= 2]


def gallery_html(items):
    if not items:
        return '<p class="empty">Zatím tu nejsou žádné fotografie. Fotogalerii tvoří aktuality se dvěma a více fotografiemi.</p>'
    cards = "".join(
        f'<li><a href="{n["url"]}">{img(photos_of(n)[0], "")}<b>{esc(n["title"])}</b>'
        f'<span>{short_date(n["date"])} · {len(photos_of(n))} fotografií</span></a></li>' for n in items)
    return f'<ol class="photo-posts">{cards}</ol>'


def event_slug(e):
    return e["url"].strip("/").split("/")[-1] if e.get("url") else re.sub(r"[^a-z0-9]+", "-", e["title"].lower()).strip("-")


def event_when(e):
    a, b = datetime.fromisoformat(e["start"]), datetime.fromisoformat(e["end"])
    if a.date() == b.date():
        return short_date(e["start"]) + ("" if e.get("allDay") else f", {a.hour}:{a.minute:02d}")
    if a.year == b.year:
        return f"{a.day}. {a.month}. – {b.day}. {b.month}. {b.year}"
    return f"{short_date(e['start'])} – {short_date(e['end'])}"


def events_list(items, time=None, compact=False):
    rows = []
    for e in items:
        d = datetime.fromisoformat(e["start"])
        desc = "" if compact else plain(e.get("description", ""), 400)
        when = event_when(e) + (f", {time}" if time else "") + (f" · {e['place']}" if e.get("place") else "")
        rows.append(f'<li id="{event_slug(e)}"><time datetime="{e["start"][:10]}"><b>{d.day}</b>{MONTHS_SHORT[d.month - 1]} {d.year}</time>'
                    f'<div><b>{esc(e["title"])}</b><span>{esc(when)}{" · " + esc(desc) if desc else ""}</span></div></li>')
    return f'<ol class="events">{"".join(rows)}</ol>'


def upcoming(limit=4, today=None):
    today = today or datetime.now().strftime("%Y-%m-%d")
    return [e for e in EVENTS if e["end"][:10] >= today][:limit]


def home_events_band(url):
    items = upcoming(6)
    if not items:
        return ""
    return f"""<section class="band" aria-labelledby="events-title"><div class="wrap split">
 <div class="split-head"><h2 id="events-title" class="display-m">Nadcházející akce</h2><p><a class="link-strong" href="{url}">Všechny akce a termíny</a></p></div>
 {events_list(items, compact=True)}
</div></section>"""


def events_page_html():
    today = datetime.now().strftime("%Y-%m-%d")
    future = [e for e in EVENTS if e["end"][:10] >= today]
    past = [e for e in EVENTS if e["end"][:10] < today and e["start"][:4] >= str(int(today[:4]) - 1)][-24:][::-1]
    out = ""
    if future:
        out += f'<h2>Nadcházející</h2>{events_list(future)}'
    else:
        out += '<p class="empty">Na nejbližší dobu zatím nejsou v kalendáři žádné akce.</p>'
    if past:
        out += f'<h2>Proběhlo</h2>{events_list(past)}'
    return out
CATS = SITE["newsCategories"]


def page_title(url):
    p = PAGES.get(url)
    return p["title"] if p else url


NAV_INDEX = {}  # url -> {node, parent, top}


def _index(nodes, parent=None, top=None):
    for n in nodes:
        n.setdefault("title", page_title(n["url"]))
        NAV_INDEX[n["url"]] = {"node": n, "parent": parent, "top": top or n["url"]}
        _index(n.get("children", []), n["url"], top or n["url"])


_index(SITE["nav"])


def breadcrumbs(url):
    trail = []
    while url in NAV_INDEX:
        trail.insert(0, (NAV_INDEX[url]["node"]["title"], url))
        url = NAV_INDEX[url]["parent"]
    return trail


# ---------------------------------------------------------------- helpers


def image_size(rel_url):
    """Width/height of a local JPEG, PNG or WebP (for layout-stable <img>)."""
    try:
        b = (STATIC / unquote(rel_url.lstrip("/"))).read_bytes()[:65536]
    except OSError:
        return None
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
        c = b[12:16]
        if c == b"VP8 ":
            w, h = struct.unpack("<HH", b[26:30])
            return w & 0x3FFF, h & 0x3FFF
        if c == b"VP8L":
            v = int.from_bytes(b[21:25], "little")
            return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
        if c == b"VP8X":
            return int.from_bytes(b[24:27], "little") + 1, int.from_bytes(b[27:30], "little") + 1
    if b[:2] == b"\xff\xd8":
        i = 2
        while i < len(b) - 9:
            if b[i] != 0xFF:
                i += 1
                continue
            marker, length = b[i + 1], struct.unpack(">H", b[i + 2:i + 4])[0]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", b[i + 5:i + 9])
                return w, h
            i += 2 + length
    return None


def img(src, alt, cls="", eager=False):
    wh = image_size(src)
    dims = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="ph-img {cls}" src="{esc(src)}" alt="{esc(alt)}"{dims} {load} decoding="async">'


def enhance_body(body):
    """Layout-stable lazy images and scrollable tables in imported content."""
    def fix_img(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if not src:
            return tag
        wh = image_size(html.unescape(src.group(1))) if src.group(1).startswith("/") else None
        extra = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
        if ' alt="' not in tag:
            extra += ' alt=""'
        return tag[:-1] + f'{extra} loading="lazy" decoding="async" class="ph-img">'
    # WordPress linked photos to their own file; after migration that is the same file: drop the link
    body = re.sub(r'<a href="([^"]+)">(<img src="\1"[^>]*>)</a>', r"\2", body)
    # any other link that holds only an undescribed photo still needs a name for screen readers
    body = re.sub(r'<a href="([^"]+)">(<img (?:(?! alt="[^"]+")[^>])*>)</a>', r'<a href="\1" aria-label="Zobrazit fotografii">\2</a>', body)
    body = re.sub(r"<img [^>]+>", fix_img, body)
    body = body.replace('<figure><ul class="gallery"></ul></figure>', "")
    # ".odt .pdf" download pairs stay on one line
    body = re.sub(r'(<a href="[^"]+">\.odt</a>)\s*(<a href="[^"]+">\.pdf</a>)', r'<span class="file-pair">\1 \2</span>', body)  # empty gallery blocks, empty on the old site too
    photo = r'(?:<figure><img [^>]+></figure>|<p><img [^>]+></p>|<img [^>]+>)'
    body = re.sub(rf"(?:{photo}\s*){{2,}}", lambda m: '<div class="photo-run">' + re.sub(
        r'<img src="([^"]+)"[^>]*>', lambda i: f'<a href="{i.group(1)}" aria-label="Zobrazit celou fotografii">{i.group(0)}</a>', m.group(0)) + "</div>", body)
    body = re.sub(r"<table>", '<div class="table-wrap" tabindex="0"><table>', body)
    return body.replace("</table>", "</table></div>")


def plain(html_text, n=180):
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", html_text))).strip()
    return t if len(t) <= n else t[: t.rfind(" ", 0, n)] + "…"


def fmt_date(iso):
    d = datetime.fromisoformat(iso[:10])
    return f"{d.day}. {MONTHS[d.month - 1]} {d.year}"


def short_date(iso):
    d = datetime.fromisoformat(iso[:10])
    return f"{d.day}. {d.month}. {d.year}"


# ---------------------------------------------------------------- layout

FONTS_PRELOAD = ["asap-latin-400-normal", "asap-latin-ext-400-normal", "eb-garamond-latin-500-normal"]  # Czech text needs latin-ext at once


def nav_html(current_url):
    top = NAV_INDEX.get(current_url, {}).get("top")
    if not top and (current_url.startswith("/aktuality/") or re.match(r"^/\d{4}/", current_url)):
        top = "/aktuality/"
    lis = []
    for n in SITE["nav"]:
        cur = ' aria-current="page"' if n["url"] == current_url else (' class="is-active"' if n["url"] == top else "")
        kids = n.get("children", [])
        sub = ""
        if kids:
            sub_items = "".join(f'<li><a href="{c["url"]}">{esc(c["title"])}</a></li>' for c in kids)
            sub = (f'<button class="sub-toggle" type="button" aria-expanded="false" aria-label="{esc(n["title"])}: další stránky">'
                   f'<span aria-hidden="true"></span></button><ul class="sub">{sub_items}</ul>')
        lis.append(f'<li class="{"has-sub" if kids else ""}"><a href="{n["url"]}"{cur}>{esc(n["title"])}</a>{sub}</li>')
    return f'<ul class="nav-list">{"".join(lis)}</ul>'


def logo_viewbox():
    """The school lockup's viewBox: its height and the accents above the shield top, in shield units (see .lockup in the CSS)."""
    return [float(v) for v in re.search(r'viewBox="([^"]+)"', (STATIC / "img" / "logo" / "zsmr-logo-photo.svg").read_text()).group(1).split()]


def logo():
    """The school lockup in the banner, sized and placed exactly as on the Prague and Skutec school sites (.lockup: shield at
    the Grand Magistry web size; --h and --t carry the SVG's height and its accents above the shield top, in shield units)."""
    vb = logo_viewbox()
    return (f'<img class="lockup" src="/img/logo/zsmr-logo-photo.svg" alt="Maltézský řád – Základní škola Maltézských rytířů" width="{vb[2]:.0f}" height="{vb[3]:.0f}"'
            f' fetchpriority="high">')


def layout(*, url, title, body, description="", image=None, status=None, main_class=""):
    names, c = SITE["names"], SITE["contact"]
    full_title = f"{title} | {names['site']}" if title != names["site"] else title
    canonical = SITE["baseUrl"] + url
    # one 1200×630 card for every page: the Order's flag and the school lockup (tools/make_og.py). Served from the domain Vercel
    # serves now (its .vercel.app address until the school's domain moves, then that domain), so shared links show it before launch.
    og_image = (f"https://{os.environ['VERCEL_PROJECT_PRODUCTION_URL']}" if os.environ.get("VERCEL_PROJECT_PRODUCTION_URL") else SITE["baseUrl"]) + "/img/og.jpg"
    robots = "" if PRODUCTION else '<meta name="robots" content="noindex, nofollow">'
    preload = "".join(f'<link rel="preload" href="/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>' for f in FONTS_PRELOAD) + '<link rel="preload" href="/img/header/krajina.webp" as="image" fetchpriority="high">'
    ld = ""
    if url == "/":  # who we are, for search engines (data only, not executed)
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "ElementarySchool", "name": names["school"], "url": canonical,
            "email": c["email"], "telephone": c["phones"][0][1], "logo": SITE["baseUrl"] + "/img/logo/zsmr-logo.svg",
            "identifier": {"@type": "PropertyValue", "propertyID": "IČO", "value": c["ico"]},
            "address": {"@type": "PostalAddress", "streetAddress": "Školská 349", "postalCode": "272 01", "addressLocality": "Kladno", "addressCountry": "CZ"},
            "parentOrganization": {"@type": "Organization", "name": names["founder"], "url": "https://www.maltezskyrad.cz/"},
        }, ensure_ascii=False).replace("</", "<\\/") + "</script>"
    status_bar = ""
    if status and not PRODUCTION:
        status_bar = f'<p class="content-status content-status--{esc(status)}"><span>{esc(STATUS.get(status, status))}</span></p>'
    footer_nav = "".join(
        f'<li><a href="{n["url"]}">{esc(n["title"])}</a>'
        + ("<ul>" + "".join(f'<li><a href="{k["url"]}">{esc(k["title"])}</a></li>' for k in n.get("children", []) if not k["url"].startswith("/aktuality/")) + "</ul>" if n.get("children") else "")
        + "</li>" for n in SITE["nav"])
    projects = "".join(
        (f'<a href="{esc(p["url"])}" rel="noopener">' if p.get("url") else "<span>") + img(p["img"], p["alt"], "proj-img") + ("</a>" if p.get("url") else "</span>")
        for p in SITE["projects"])
    phones = " · ".join(f'{esc(k)} <a href="tel:{v.replace(" ", "")}">{v}</a>' for k, v in c["phones"])
    return f"""<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(plain(description or body, 160))}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(names['site'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(plain(description or body, 160))}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(names['school'])}">
<meta property="og:locale" content="cs_CZ">
<meta name="twitter:card" content="summary_large_image">
{ld}
<meta name="theme-color" content="#e31a18">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/img/logo/zsmr-mark.svg">
<link rel="apple-touch-icon" href="/img/favicon/apple-touch-icon-180x180.png">
<link rel="alternate" type="application/rss+xml" title="{esc(names['site'])}" href="/feed.xml">
{preload}
<link rel="stylesheet" href="/css/site.css?v={ASSET_VERSION}">
<script src="/js/head.js?v={ASSET_VERSION}"></script>
<script src="/js/site.js?v={ASSET_VERSION}" defer></script>
</head>
<body class="school">
<a class="skip" href="#main">Přejít na obsah</a>
<header class="site-header">
 <div class="topbar"><div class="wrap">
  <a class="topbar-home" href="https://www.maltezskyrad.cz/">Maltézský řád · České velkopřevorství</a>
  <span class="topbar-social"><a href="tel:{c['phones'][0][1].replace(' ', '')}">{c['phones'][0][1]}</a><a href="mailto:{c['email']}">{c['email']}</a></span>
 </div></div>
 <div class="banner"><div class="wrap">
  <a class="banner-home" href="/">{logo()}</a>
  <p class="fullname">{esc(names['tagline'])}<span>{esc(names['founder'])} · zřizovatel školy</span></p>
 </div></div>
 <nav class="mainnav" aria-label="Hlavní menu"><div class="wrap">
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <div id="menu" class="menu">{nav_html(url)}</div>
 </div></nav>
</header>
<main id="main" class="{main_class}" tabindex="-1">
{pinned_html() if url in ("/", "/aktuality/") else ""}
{status_bar}
{body}
</main>
<footer class="site-footer">
 <div class="f-nav"><div class="wrap"><ul>{footer_nav}</ul></div></div>
 <div class="f-id"><div class="wrap f-id-grid">
  <div><p class="f-name">{esc(names['school'])}</p>
   <p>{esc(c['address'])} · IČO {c['ico']} · datová schránka {c['dataBox']}<br><a href="mailto:{c['email']}">{c['email']}</a> · {phones}</p>
   <p class="f-partner">Partner školy: <a href="{esc(SITE['partner']['url'])}" rel="noopener">{esc(SITE['partner']['alt'])}</a></p>
   <p class="f-licence">Obsah webu podléhá licenci <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.cs" rel="license">Creative Commons Uveďte původ-Zachovejte licenci 4.0</a>.</p></div>
  <div class="f-projects"><p class="f-label">Realizované projekty</p><div class="proj">{projects}</div></div>
 </div></div>
 <div class="f-red"><div class="wrap">
  <p>Zřizovatel: <a href="https://www.maltezskyrad.cz/">{esc(names['founder'])}</a></p>
  <p>Suverénní maltézský řád: <a href="https://www.orderofmalta.int/">www.orderofmalta.int</a></p>
  <p><a href="/ochrana-osobnich-udaju-gdpr/">Ochrana osobních údajů</a> · <a href="/prohlaseni-o-pristupnosti/">Prohlášení o přístupnosti</a></p>
 </div></div>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------- shared blocks


def news_item(n, compact=False):
    excerpt = "" if compact or not n.get("excerpt") else f'<p class="n-excerpt">{esc(n["excerpt"])}</p>'
    return (f'<li class="n-item"><time datetime="{n["date"][:10]}">{short_date(n["date"])}</time>'
            f'<div><a href="{n["url"]}">{esc(n["title"])}</a>{excerpt}</div></li>')


def news_card(n, lead=False):
    """A dated story with its photograph (home page)."""
    pic = f'<a class="story-img" href="{n["url"]}" tabindex="-1" aria-hidden="true">{img(n["image"], "", eager=lead)}</a>' if n.get("image") else ""
    cats = " · ".join(esc(CATS[c]) for c in n.get("categories", []) if c in CATS)
    return (f'<article class="story{" story--lead" if lead else ""}">{pic}<div class="story-text">'
            f'<p class="story-meta"><time datetime="{n["date"][:10]}">{fmt_date(n["date"])}</time>{(" · " + cats) if cats else ""}</p>'
            f'<h3 class="story-title"><a href="{n["url"]}">{esc(n["title"])}</a></h3>'
            + (f'<p>{esc(plain(n.get("excerpt", ""), 220 if lead else 130))}</p>' if n.get("excerpt") else "") + "</div></article>")


def contact_card():
    c = SITE["contact"]
    phones = "<br>".join(f'{esc(k)}: <a href="tel:{v.replace(" ", "")}">{v}</a>' for k, v in c["phones"])
    return f"""<dl class="contact-card">
 <div><dt>Adresa</dt><dd>{esc(SITE['names']['school'])}<br>{esc(c['address'])}<br><a href="{esc(c['mapUrl'])}">Zobrazit na mapě</a></dd></div>
 <div><dt>Telefon</dt><dd>{phones}</dd></div>
 <div><dt>E-mail</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd></div>
 <div><dt>IČO</dt><dd>{c['ico']}</dd></div>
 <div><dt>Datová schránka</dt><dd>{c['dataBox']}</dd></div>
 <div><dt>Číslo účtu</dt><dd>{esc(c['account'])}</dd></div>
</dl>"""


TRUST_FORM = """<form class="trust-form" id="trust-form" method="post" action="/api/trust">
 <div class="ne-field"><label for="tf-name">Vaše jméno <small>(nepovinné)</small></label><input id="tf-name" name="name" autocomplete="name" maxlength="120"></div>
 <div class="ne-field"><label for="tf-email">E-mail pro zaslání odpovědi <i aria-hidden="true">*</i></label><input id="tf-email" name="email" type="email" autocomplete="email" required maxlength="200"></div>
 <div class="ne-field"><label for="tf-subject">Předmět</label><input id="tf-subject" name="subject" maxlength="200"></div>
 <div class="ne-field"><label for="tf-message">Vaše zpráva <i aria-hidden="true">*</i></label><textarea id="tf-message" name="message" rows="8" required maxlength="10000"></textarea></div>
 <p class="hp" aria-hidden="true"><label>Nevyplňujte <input name="website" tabindex="-1" autocomplete="off"></label></p>
 <p><button class="btn" type="submit">Odeslat</button></p>
 <p class="ne-msg" id="tf-msg" role="status" hidden></p>
 <p class="small">Zprávu přečte vedení školy. Odešle se e-mailem a na webu se neukládá; e-mail (a jméno, pokud ho uvedete) použijeme jen k odpovědi, viz <a href="/ochrana-osobnich-udaju-gdpr/#tento-web">Ochrana osobních údajů</a>. Pokud formulář nefunguje, napište na <a href="mailto:skola@zsmr.cz">skola@zsmr.cz</a>.</p>
</form>"""


# ---------------------------------------------------------------- pages


def section_children_html(url):
    kids = NAV_INDEX.get(url, {}).get("node", {}).get("children", [])
    if not kids:
        return ""
    items = []
    for k in kids:
        p = PAGES.get(k["url"], {})
        desc = k.get("desc") or p.get("description") or plain(p.get("body", ""), 150)
        if not p and k["url"].startswith("/aktuality/"):
            n = sum(1 for x in NEWS if k["url"].split("/")[2] in x.get("categories", []))
            desc = f"Zprávy a fotografie: {n} {'článek' if n == 1 else 'články' if 2 <= n <= 4 else 'článků'}"
        items.append(f'<li><a href="{k["url"]}"><b>{esc(k["title"])}</b>{f"<span>{esc(desc)}</span>" if desc else ""}</a></li>')
    return f'<ul class="index-list">{"".join(items)}</ul>'


def _descendants(node):
    out = set()
    for c in node.get("children", []):
        out.add(c["url"])
        out |= _descendants(c)
    return out


def side_nav(url):
    info = NAV_INDEX.get(url)
    if not info:
        return ""
    top = NAV_INDEX[info["top"]]["node"]
    if not top.get("children") or info["top"] == url:  # a section's own page already lists its children
        return ""
    lis = "".join(f'<li><a href="{n["url"]}"{" aria-current=" + chr(34) + "page" + chr(34) if n["url"] == url else ""}>{esc(n["title"])}</a></li>' for n in top["children"])
    return f'<nav class="side-nav" aria-label="V této části"><p class="label"><a href="{top["url"]}">{esc(top["title"])}</a></p><ul>{lis}</ul></nav>'


def crumbs_html(url, extra=None):
    trail = [("Úvod", "/")] + breadcrumbs(url) + (extra or [])
    if len(trail) < 2:
        return ""
    items = []
    for i, (t, u) in enumerate(trail):
        items.append(f'<li><span aria-current="page">{esc(t)}</span></li>' if i == len(trail) - 1 else f'<li><a href="{u}">{esc(t)}</a></li>')
    return f'<nav class="crumbs" aria-label="Drobečková navigace"><ol>{"".join(items)}</ol></nav>'


def render_home():
    names, c = SITE["names"], SITE["contact"]
    profile = PAGES["/profil-skoly/"]
    paras = re.findall(r"<p>(.*?)</p>", profile["body"], re.S)
    intro = f"<p>{paras[1]}</p>" if len(paras) > 1 else ""
    lead, rest = (NEWS[0], NEWS[1:7]) if NEWS else (None, [])
    parents = [("/dokumenty-pro-rodice/", "Přihlášky, žádosti a formuláře"), ("/skolne-a-dalsi-platby/", "Výše školného, slevy a platby"),
               ("/rozvrh/", "Rozvrhy tříd a učitelů"), ("/dokumenty-o-skole/", "ŠVP, školní řád, prázdniny"),
               ("/pedagogove/", "Učitelé a konzultační hodiny"), ("/schranka-duvery/", "Anonymní dotaz vedení školy")]
    parents_html = "".join(f'<li><a href="{u}"><b>{esc(page_title(u))}</b><span>{esc(d)}</span></a></li>' for u, d in parents)
    classes = "".join(f'<li><a href="/aktuality/{i}-trida/">{i}.<span class="visually-hidden"> třída</span></a></li>' for i in range(1, 10))
    events_band = home_events_band('/kalendar/')
    body = f"""
<section class="home-open" aria-labelledby="home-title"><div class="wrap home-intro">
 <div class="home-intro-main">
  <h1 id="home-title" class="display">{esc(names['school'])}</h1>
  <p class="lead">{paras[0] if paras else ''}</p>
  {intro}
  <p class="text-links"><a href="/profil-skoly/">Profil školy</a><a href="/kontakty/">Kontakty</a><a href="/hledame/">Hledáme učitele</a></p>
 </div>
 <div class="home-intro-facts">
  <dl class="facts">
   <div><dt>Zřizovatel</dt><dd><a href="https://www.maltezskyrad.cz/">{esc(names['founder'])}</a></dd></div>
   <div><dt>Vedení</dt><dd>{esc(c['head'])}</dd></div>
   <div><dt>Adresa</dt><dd>{esc(c['address'])}</dd></div>
   <div><dt>Ředitelna</dt><dd><a href="tel:{c['phones'][0][1].replace(' ', '')}">{c['phones'][0][1]}</a></dd></div>
   <div><dt>Družina</dt><dd><a href="tel:{c['phones'][2][1].replace(' ', '')}">{c['phones'][2][1]}</a></dd></div>
   <div><dt>E-mail</dt><dd><a href="mailto:{c['email']}">{c['email']}</a></dd></div>
  </dl>
 </div>
</div></section>

<section class="band band-grey" aria-labelledby="parents-title"><div class="wrap split">
 <div class="split-head"><h2 id="parents-title" class="display-m">Pro rodiče a žáky</h2><p>Dokumenty, platby a rozvrhy na jednom místě.</p>
  <h3 class="display-s">Třídy</h3><ul class="class-grid" aria-label="Aktuality tříd">{classes}</ul>
  <p><a class="link-strong" href="/prehled-trid/">Přehled tříd</a></p></div>
 <ul class="works">{parents_html}</ul>
</div></section>

<section class="band" aria-labelledby="news-title"><div class="wrap">
 <div class="section-head section-head--row"><h2 id="news-title" class="display-m">Aktuality</h2><p><a class="link-strong" href="/aktuality/">Všechny aktuality</a></p></div>
 <div class="stories">{news_card(lead, True) if lead else ''}<div class="stories-list">{''.join(news_card(n) for n in rest[:4])}</div></div>
</div></section>

{events_band}

<section class="band band-grey" aria-labelledby="more-title"><div class="wrap split">
 <div class="split-head"><h2 id="more-title" class="display-m">Družina a kroužky</h2><p>{esc(plain(re.search(r'<p>(.*?)</p>', PAGES['/o-druzine/']['body'], re.S).group(1), 400))}</p></div>
 <ul class="works">
  <li><a href="/o-druzine/"><b>O družině</b><span>Provozní doba a vnitřní řád školní družiny</span></a></li>
  <li><a href="/aktuality/akce_druziny/"><b>Akce družiny</b><span>Co se v družině děje</span></a></li>
  <li><a href="/prehled-krouzku/"><b>Přehled kroužků</b><span>Nabídka, přihláška a platby</span></a></li>
  <li><a href="/aktuality/vylety-a-akce/"><b>Výlety a akce</b><span>Výpravy, exkurze a školní akce</span></a></li>
 </ul>
</div></section>
"""
    return layout(url="/", title=SITE["names"]["site"], body=body, status="new",
                  description="Základní škola Maltézských rytířů v Kladně – Kročehlavech: křesťanská základní škola se všemi devíti ročníky, zřizovaná Maltézským řádem.")


def page_body(html_text):
    """The page's text with the placeholders filled in: <div data-gallery></div>, <div data-events></div>."""
    html_text = enhance_body(html_text).replace('<div data-gallery></div>', gallery_html(gallery_posts()[:48]))
    m = re.search(r'<div data-events(?:="([^"]*)")?(?: data-time="([^"]*)")?></div>', html_text)
    if m:
        items = [e for e in EVENTS if not m.group(1) or e["title"] == m.group(1)]
        html_text = html_text.replace(m.group(0), events_list(items, time=m.group(2), compact=bool(m.group(1))))
    return html_text


def render_page(p):
    url = p["url"]
    is_section = p.get("section") or bool(NAV_INDEX.get(url, {}).get("node", {}).get("children"))
    figure = f'<figure class="page-figure">{img(p["image"], p.get("imageAlt") or p["title"], eager=True)}</figure>' if p.get("image") else ""
    special = ""
    if url == "/kontakty/":
        special = contact_card()
    if url == "/schranka-duvery/":
        special = TRUST_FORM
    side = side_nav(url)
    body = f"""
<div class="wrap">{crumbs_html(url)}</div>
<article class="wrap page{' page--with-side' if side else ''}">
 <header class="page-head"><h1 class="display">{esc(p['title'])}</h1></header>
 <div class="page-main">
  {figure}
  {'' if url == '/kontakty/' else f'<div class="prose">{page_body(p["body"])}</div>'}
  {special}
  {section_children_html(url) if is_section else ''}
 </div>
 {f'<div class="page-side">{side}</div>' if side else ''}
</article>"""
    return layout(url=url, title=p["title"], body=body, description=p.get("description", ""), image=p.get("image"), status=p.get("status"))


def render_article(n, prev_n, next_n):
    cat_links = " · ".join(f'<a href="/aktuality/{c}/">{esc(CATS[c])}</a>' for c in n.get("categories", []) if c in CATS)
    figure = f'<figure class="page-figure">{img(n["image"], n["title"], eager=True)}</figure>' if n.get("image") and n["image"] not in n["body"] else ""
    pager = ""
    if prev_n or next_n:
        pager = ('<nav class="pager" aria-label="Další články">'
                 + (f'<a class="pager-prev" href="{next_n["url"]}"><span>Novější</span>{esc(next_n["title"])}</a>' if next_n else "<span></span>")
                 + (f'<a class="pager-next" href="{prev_n["url"]}"><span>Starší</span>{esc(prev_n["title"])}</a>' if prev_n else "") + "</nav>")
    body = f"""
<div class="wrap">{crumbs_html('/aktuality/', [(n['title'], n['url'])])}</div>
<article class="wrap page page--article">
 <header class="page-head">
  <h1 class="display">{esc(n['title'])}</h1>
  <p class="byline"><time datetime="{n['date'][:10]}">{fmt_date(n['date'])}</time>{(' · ' + cat_links) if cat_links else ''}</p>
 </header>
 <div class="page-main">
  {figure}
  <div class="prose">{enhance_body(n['body'])}</div>
  <p><a class="link-strong" href="/aktuality/">Zpět na aktuality</a></p>
  {pager}
 </div>
</article>"""
    return layout(url=n["url"], title=n["title"], body=body, description=n.get("excerpt", ""), image=n.get("image"), status=n.get("status"))


PER_PAGE = 30


def render_news_index(items, active="", year=None, url="/aktuality/", page=1, pages=1):
    counts = {c: sum(1 for n in NEWS if c in n.get("categories", [])) for c in CATS}
    cur = ' aria-current="page"'
    tabs = [f'<a href="/aktuality/"{cur if not active and not year else ""}>Vše</a>']
    tabs += [f'<a href="/aktuality/{c}/"{cur if active == c else ""}>{esc(label)} <span class="count">{counts[c]}</span></a>' for c, label in CATS.items() if counts[c]]
    years = sorted({n["date"][:4] for n in NEWS}, reverse=True)
    year_links = "".join(f'<a href="/aktuality/{y}/"{cur if year == y else ""}>{y}</a>' for y in years)
    groups, cur_year = [], None
    for n in items:
        y = n["date"][:4]
        if y != cur_year:
            if cur_year:
                groups.append("</ol></section>")
            groups.append(f'<section class="year-group"><h2 class="year">{y}</h2><ol class="news-list news-list--full">')
            cur_year = y
        groups.append(news_item(n))
    if cur_year:
        groups.append("</ol></section>")
    base = url if page == 1 else url.rsplit("strana/", 1)[0]
    pager = ""
    if pages > 1:
        pager = '<nav class="pagination" aria-label="Stránky aktualit"><ol>' + "".join(
            f'<li><a href="{base if i == 1 else f"{base}strana/{i}/"}"{cur if i == page else ""}>{i}</a></li>' for i in range(1, pages + 1)) + "</ol></nav>"
    title = "Aktuality" + (f": {CATS[active]}" if active else "") + (f" {year}" if year else "") + (f" – strana {page}" if page > 1 else "")
    body = f"""
<div class="wrap">{crumbs_html(url) if url in NAV_INDEX and url != '/aktuality/' else crumbs_html('/aktuality/', [(title, url)] if url != '/aktuality/' else None)}</div>
<div class="wrap page page--news">
 <header class="page-head"><h1 class="display">{esc(title)}</h1>
  <p class="lead-s">Zprávy ze života školy, tříd, družiny a kroužků. Archiv sahá do roku {years[-1] if years else ''}.</p></header>
 <nav class="tabs" aria-label="Rubrika">{''.join(tabs)}</nav>
 <nav class="years" aria-label="Rok">{year_links}</nav>
 {''.join(groups) or '<p class="empty">V této rubrice zatím nejsou žádné zprávy.</p>'}
 {pager}
</div>"""
    return layout(url=url, title=title, body=body,
                  description=f"Aktuality Základní školy Maltézských rytířů v Kladně{(': ' + CATS[active]) if active else ''}{(' ' + year) if year else ''}.")


def render_calendar():
    docs = PAGES.get("/dokumenty-o-skole/", {}).get("body", "")
    holidays = re.search(r"<p>[^<]*Prázdniny.*?</p>", docs, re.S)
    body = f"""
<div class="wrap">{crumbs_html('/kalendar/')}</div>
<div class="wrap page page--with-side">
 <header class="page-head"><h1 class="display">Kalendář akcí</h1></header>
 <div class="page-main"><div class="prose">
  {events_page_html()}
  <h2>Školní rok</h2>
  <p class="lead-s">Termíny prázdnin a dalších akcí školního roku jsou v dokumentu, který škola vydává na každý rok:</p>
  {holidays.group(0) if holidays else '<p><a href="/dokumenty-o-skole/">Dokumenty o škole</a></p>'}
  <p>O konkrétních akcích, výletech a konzultacích informujeme v <a href="/aktuality/">aktualitách</a>.</p>
 </div></div>
 <div class="page-side">{side_nav('/kalendar/')}</div>
</div>"""
    return layout(url="/kalendar/", title="Kalendář akcí", body=body, status="new",
                  description="Kalendář akcí Základní školy Maltézských rytířů: prázdniny a akce školního roku.")


def render_gallery():
    body = f"""
<div class="wrap">{crumbs_html('/fotogalerie/')}</div>
<div class="wrap page page--simple"><header class="page-head"><h1 class="display">Fotogalerie</h1>
 <p class="lead-s">Fotografie ze života školy. Každá aktualita se dvěma a více fotografiemi je tu; klepnutím otevřete celou aktualitu.</p></header>
 {gallery_html(gallery_posts()[:48])}
 {'<p class="small">Starší fotografie najdete v aktualitách podle roku: ' + ' · '.join(f'<a href="/aktuality/{y}/">{y}</a>' for y in sorted({n["date"][:4] for n in gallery_posts()[48:]}, reverse=True)) + '.</p>' if len(gallery_posts()) > 48 else ''}
</div>"""
    return layout(url="/fotogalerie/", title="Fotogalerie", body=body, status="new", description="Fotogalerie školy: fotografie ze školních akcí a aktualit.")


def render_simple(url, title, inner, status=None):
    body = f'<div class="wrap page page--simple"><header class="page-head"><h1 class="display">{esc(title)}</h1></header><div class="prose">{inner}</div></div>'
    return layout(url=url, title=title, body=body, status=status)


NEWS_EDITOR_URL = "/pridat-aktualitu/"


def render_news_editor():
    """Staff page for publishing news and events (api/news.js); not linked, not indexed, behind a password."""
    body = f"""
<div class="wrap page page--simple ne" id="news-app" data-site="{SB["site"]}" data-supabase-url="{SB["url"]}" data-supabase-key="{SB["key"]}" data-categories="{esc(json.dumps(SITE["newsCategories"], ensure_ascii=False))}">
 <header class="page-head"><h1 class="display">Přidat aktualitu</h1>
  <p class="lead-s">Aktualita se po zveřejnění objeví na webu v sekci <a href="/aktuality/">Aktuality</a> asi za minutu.</p></header>
 <noscript><p class="ne-msg ne-msg--error">Formulář potřebuje zapnutý JavaScript.</p></noscript>
 <form id="ne-login" class="ne-card" hidden>
  <h2 class="display-s">Přihlášení</h2>
  <label class="ne-field"><span>E-mail</span><input name="email" type="email" autocomplete="username" required></label>
  <label class="ne-field"><span>Heslo</span><input name="password" type="password" autocomplete="current-password" required></label>
  <p class="ne-msg" id="ne-login-msg" role="alert" hidden></p>
  <p><button class="btn" type="submit">Přihlásit se</button> <button class="link-btn" type="button" id="ne-forgot">Zapomenuté heslo</button></p>
 </form>
 <form id="ne-mfa" class="ne-card" hidden>
  <h2 class="display-s">Ověření jednorázovým kódem</h2>
  <div id="ne-mfa-enrol" hidden>
   <p>Přihlášení má dva kroky: heslo a kód z aplikace v telefonu (například Google Authenticator, Microsoft Authenticator nebo Authy). Nastavíte to jednou: v aplikaci načtěte tento kód a opište šestimístné číslo, které aplikace ukáže.</p>
   <p class="ne-qr"><img id="ne-mfa-qr" alt="QR kód pro aplikaci" width="180" height="180"></p>
   <p class="small">Nejde načíst? Zadejte do aplikace ručně tento klíč: <code id="ne-mfa-secret"></code></p>
  </div>
  <label class="ne-field"><span>Kód z aplikace</span><input id="ne-mfa-code" inputmode="numeric" autocomplete="one-time-code" required></label>
  <p class="ne-msg" id="ne-mfa-msg" role="alert" hidden></p>
  <p><button class="btn" type="submit">Ověřit</button> <button class="link-btn" type="button" id="ne-mfa-cancel">Zrušit a odhlásit</button></p>
 </form>
 <form id="ne-recover" class="ne-card" hidden>
  <h2 class="display-s">Nové heslo</h2>
  <label class="ne-field"><span>Nové heslo <small>(alespoň 10 znaků)</small></span><input id="ne-new-password" type="password" autocomplete="new-password" minlength="10" required></label>
  <p class="ne-msg" id="ne-recover-msg" role="alert" hidden></p>
  <p><button class="btn" type="submit">Uložit heslo</button></p>
 </form>
 <div id="ne-app" hidden>
 <p class="ne-who">Přihlášen(a): <b id="ne-user"></b> · <button type="button" class="link-btn" id="ne-logout">Odhlásit</button></p>
 <div class="ne-tabs" role="tablist" aria-label="Co chcete udělat">
  <button type="button" role="tab" id="ne-tab-new" aria-selected="true" aria-controls="ne-editor">Nová aktualita</button>
  <button type="button" role="tab" id="ne-tab-list" aria-selected="false" aria-controls="ne-manage">Upravit nebo smazat</button>
  <button type="button" role="tab" id="ne-tab-events" aria-selected="false" aria-controls="ne-events">Události</button>
  <button type="button" role="tab" id="ne-tab-members" aria-selected="false" aria-controls="ne-members" hidden>Uživatelé</button>
 </div>
 <section id="ne-manage" role="tabpanel" aria-labelledby="ne-tab-list" hidden>
  <label class="ne-field"><span>Hledat aktualitu</span><input id="ne-search" type="search" placeholder="Část titulku nebo rok…"></label>
  <ul id="ne-list" class="ne-list"></ul>
  <p class="ne-hint">Koncepty a naplánované aktuality jsou označené; smazat lze jen vlastní aktuality (správce všechny).</p>
  <p class="ne-msg" id="ne-list-msg" role="alert" hidden></p>
 </section>
 <section id="ne-members" role="tabpanel" aria-labelledby="ne-tab-members" hidden>
  <form id="ne-member-form" class="ne-card">
   <h2 class="display-s">Kdo může publikovat</h2>
   <p>Účet vzniká pozvánkou v administraci Supabase (Authentication → Users → Invite user). Pozvaná osoba si nastaví heslo a aplikaci s kódy; tady jí pak dáte přístup k tomuto webu. Redaktor upravuje a maže jen své aktuality a události, správce všechny a může připnout oznámení a spravovat uživatele.</p>
   <div class="ne-row">
    <label class="ne-field"><span>E-mail účtu</span><input id="ne-member-email" type="email" required></label>
    <label class="ne-field"><span>Role</span><select id="ne-member-role"><option value="editor">redaktor</option><option value="admin">správce</option></select></label>
   </div>
   <div class="ne-submit"><button class="btn" type="submit">Přidat nebo změnit roli</button></div>
  </form>
  <h2 class="display-s">Uživatelé tohoto webu</h2>
  <ul id="ne-member-list" class="ne-list"></ul>
  <p class="ne-msg" id="ne-member-msg" role="alert" hidden></p>
 </section>
 <section id="ne-events" role="tabpanel" aria-labelledby="ne-tab-events" hidden>
  <form id="ne-event-form" class="ne-card">
   <h2 class="display-s">Událost v kalendáři</h2>
   <div class="ne-editing" id="ne-ev-editing" hidden><p>Upravujete: <b id="ne-ev-editing-title"></b></p><button type="button" class="link-btn" id="ne-ev-cancel">Zrušit úpravy</button></div>
   <label class="ne-field"><span>Název <i aria-hidden="true">*</i></span><input id="ne-ev-title" maxlength="200" required></label>
   <div class="ne-row">
    <label class="ne-field"><span>Začátek <i aria-hidden="true">*</i></span><input id="ne-ev-start" type="datetime-local" required></label>
    <label class="ne-field"><span>Konec <small>(nepovinné)</small></span><input id="ne-ev-end" type="datetime-local"></label>
    <label class="ne-check"><input id="ne-ev-allday" type="checkbox"> Celý den</label>
   </div>
   <label class="ne-field"><span>Místo <small>(nepovinné)</small></span><input id="ne-ev-place" maxlength="120"></label>
   <label class="ne-field"><span>Popis <small>(nepovinné; prázdný řádek odděluje odstavce)</small></span><textarea id="ne-ev-desc" rows="4"></textarea></label>
   <div class="ne-submit"><button class="btn" type="submit" id="ne-ev-save">Přidat událost</button></div>
  </form>
  <h2 class="display-s">Události</h2>
  <ul id="ne-event-list" class="ne-list"></ul>
  <p class="ne-msg" id="ne-event-msg" role="alert" hidden></p>
 </section>
 <form id="ne-editor" role="tabpanel" aria-labelledby="ne-tab-new">
  <div class="ne-editing" id="ne-editing" hidden><p>Upravujete: <a id="ne-editing-link"></a></p><button type="button" class="link-btn" id="ne-cancel">Zrušit úpravy</button></div>
  <p class="ne-msg ne-msg--error" id="ne-readonly" hidden>Tuto aktualitu napsal někdo jiný; upravit nebo smazat ji může jen autor nebo správce webu.</p>
  <p class="ne-msg" id="ne-draft" hidden></p>
  <label class="ne-field"><span>Titulek <i aria-hidden="true">*</i></span><input id="ne-title" maxlength="200" required></label>
  <div class="ne-row">
   <label class="ne-field"><span>Datum a čas zveřejnění</span><input id="ne-date" type="datetime-local" required><small id="ne-date-hint"></small></label>
   <fieldset class="ne-field"><legend>Kategorie</legend><div id="ne-cats" class="ne-cats"></div></fieldset>
  </div>
  <div class="ne-row ne-flags">
   <label class="ne-check"><input id="ne-draft-flag" type="checkbox"> Koncept <small>(uložit, ale zatím nezveřejnit)</small></label>
   <label class="ne-check" id="ne-pin-field" hidden><input id="ne-pin" type="checkbox"> Připnout na úvodní stránku <small>(důležité oznámení)</small></label>
  </div>
  <div class="ne-field"><span id="ne-text-label">Text <i aria-hidden="true">*</i></span>
   <div class="ne-text-wrap"><div id="ne-text" class="prose" aria-labelledby="ne-text-label"></div></div>
   <div id="ne-locked" class="ne-locked" hidden><p class="ne-msg ne-msg--error">Text této starší aktuality obsahuje prvky, které editor neumí (například fotografie s popiskem nebo tabulku). Text proto zůstane beze změny; upravit můžete titulek, datum, kategorie, perex, fotografii a přílohy.</p><div class="prose" id="ne-locked-text"></div></div>
   <p class="ne-hint" id="ne-text-hint">Nadpis a podnadpis, tučné písmo, kurzíva, seznamy, citace, odkazy a fotografie v textu. Dvě a více fotografií za sebou tvoří mřížku a aktualita se objeví i ve fotogalerii. Písmo a barvy jsou dané vzhledem webu.</p>
   <p class="ne-msg" id="ne-inline-msg" hidden></p></div>
  <label class="ne-field"><span>Perex <small>(nepovinné – krátké shrnutí v přehledu aktualit; jinak se vezme začátek textu)</small></span><textarea id="ne-excerpt" rows="2" maxlength="300"></textarea></label>
  <div class="ne-field"><span>Hlavní fotografie <small>(nepovinné – zobrazí se nad textem; zmenší se před odesláním)</small></span>
   <label class="btn btn--ghost ne-pick">Vybrat fotografii<input id="ne-photo" type="file" accept="image/jpeg,image/png,image/webp" class="visually-hidden"></label>
   <ul id="ne-photo-box" class="ne-files ne-photo"></ul></div>
  <div class="ne-field"><span>Přílohy ke stažení <small>(PDF nebo fotografie, nejvýše 3 MB na soubor; fotografie i větší PDF se před odesláním zmenší přímo v prohlížeči)</small></span>
   <div class="ne-drop" id="ne-drop"><p>Přetáhněte soubory sem, nebo</p>
    <label class="btn btn--ghost ne-pick">vyberte soubory<input id="ne-files" type="file" multiple accept="application/pdf,image/jpeg,image/png,image/webp" class="visually-hidden"></label></div>
   <ul id="ne-file-list" class="ne-files"></ul>
   <p class="ne-hint">PDF zmenšuje Ghostscript (licence AGPL) spuštěný v tomto prohlížeči; soubor nikam jinam neodchází. <a href="/js/vendor/ghostscript-1.1.0/SOURCE.txt">Zdroj a licence</a>.</p></div>
  <div class="ne-submit"><button class="btn" type="submit" id="ne-publish">Zveřejnit</button>
   <p class="ne-msg" id="ne-msg" role="alert" hidden></p></div>
 </form>
 </div>
 <div id="ne-done" class="ne-card" hidden role="status">
  <h2 class="display-s" id="ne-done-title">Zveřejněno</h2>
  <p id="ne-done-text">Změna bude na webu asi za minutu: <a id="ne-done-link"></a></p>
  <p><button class="btn" type="button" id="ne-again">Zpět na aktuality</button></p>
 </div>
</div>
<link rel="stylesheet" href="/js/vendor/quill-2.0.3/quill.snow.css">
<script src="/js/vendor/quill-2.0.3/quill.js"></script>
<script src="/js/vendor/supabase-2.49.4/supabase.js"></script>
<script src="/js/news-editor.js?v={ASSET_VERSION}"></script>"""
    h = layout(url=NEWS_EDITOR_URL, title="Přidat aktualitu", body=body, description="Přidání aktuality na web školy.")
    return h.replace("<head>\n", '<head>\n<meta name="robots" content="noindex, nofollow">\n', 1) if PRODUCTION else h


def write(url, html_text):
    path = DIST / url.lstrip("/") / "index.html" if url.endswith("/") else DIST / url.lstrip("/")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_text, encoding="utf-8")


def rss():
    items = "".join(
        f"<item><title>{esc(n['title'])}</title><link>{SITE['baseUrl']}{n['url']}</link><guid>{SITE['baseUrl']}{n['url']}</guid>"
        f"<pubDate>{datetime.fromisoformat(n['date']).strftime('%a, %d %b %Y %H:%M:00 +0100')}</pubDate><description>{esc(n.get('excerpt', ''))}</description></item>"
        for n in NEWS[:30])
    return (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(SITE["names"]["site"])}</title>'
            f'<link>{SITE["baseUrl"]}/</link><description>Aktuality ZŠ Maltézských rytířů</description><language>cs</language>{items}</channel></rss>')


VERCEL = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))  # headers and redirects live here; other hosts get _headers and _redirects
HEADERS = "".join(h["source"].replace("(.*)", "*") + "\n" + "".join(f"  {x['key']}: {x['value']}\n" for x in h["headers"]) for h in VERCEL["headers"])


def redirect_lines():
    """vercel.json redirects as _redirects lines; query-matched rules become "path?key=value" sources."""
    out = []
    for r in VERCEL["redirects"]:
        q = "".join(f"?{h['key']}={h.get('value', '*').strip('^$').replace('/?', '')}" for h in r.get("has", []) if h["type"] == "query")
        src = r["source"].replace(":path*", "*").replace("/:file(index\\.php)?", "/")
        out.append(f"{src}{q} {r['destination'].replace(':path*', ':splat')} 301\n")
    return "".join(dict.fromkeys(out))


def paginate(items, url, **kw):
    pages = max(1, -(-len(items) // PER_PAGE))
    for i in range(pages):
        u = url if i == 0 else f"{url}strana/{i + 1}/"
        write(u, render_news_index(items[i * PER_PAGE:(i + 1) * PER_PAGE], url=u, page=i + 1, pages=pages, **kw))
    return [url] + [f"{url}strana/{i + 1}/" for i in range(1, pages)]


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)
    vb = logo_viewbox()  # the lockup's size variables live in the stylesheet, so pages carry no inline style (CSP style-src 'self')
    with (DIST / "css" / "site.css").open("a", encoding="utf-8") as f:
        f.write(f"\n.lockup{{--h:{vb[3] / 126:.4f};--t:{vb[1] / 126:.4f}}}\n")
    for url, p in PAGES.items():
        if not DYNAMIC_PAGE.search(p["body"]):
            write(url, render_page(p))
    write(NEWS_EDITOR_URL, render_news_editor())
    write("/404.html", render_simple("/404.html", "Stránka nenalezena",
                                     '<p>Stránka na této adrese neexistuje. Mohla být přesunuta při obnově webu.</p>'
                                     '<p><a class="link-strong" href="/">Úvodní stránka</a> · <a class="link-strong" href="/aktuality/">Aktuality</a> · <a class="link-strong" href="/kontakty/">Kontakty</a></p>'))
    (DIST / "robots.txt").write_text(("User-agent: *\nAllow: /\nDisallow: /pridat-aktualitu/\nDisallow: /api/\n\nSitemap: " + SITE["baseUrl"] + "/sitemap.xml\n") if PRODUCTION
                                     else "User-agent: *\nDisallow: /\n", encoding="utf-8")
    sizes = {}
    for f in sorted(list((STATIC / "media").rglob("*")) + list((STATIC / "img").rglob("*"))):
        if f.is_file():
            u = "/" + f.relative_to(STATIC).as_posix()
            wh = image_size(u)
            sizes[u] = list(wh) if wh else {"ext": f.suffix.lstrip(".").upper(), "size": f.stat().st_size}
    (CONTENT / "image-sizes.json").write_text(json.dumps(sizes, separators=(",", ":")), encoding="utf-8")
    (DIST / "_headers").write_text(HEADERS + ("" if PRODUCTION else "/*\n  X-Robots-Tag: noindex, nofollow\n"), encoding="utf-8")
    (DIST / "_redirects").write_text(redirect_lines(), encoding="utf-8")
    print(f"built {len(PAGES)} pages (news, events and galleries come from the database), {'production' if PRODUCTION else 'preview'} → {DIST}")


# ---------------------------------------------------------------- local preview server


def serve(port=8000):
    import functools
    import http.server
    rules = [l.split() for l in (DIST / "_redirects").read_text().splitlines() if l.strip()]
    headers, types, block = {}, {}, None
    for line in (DIST / "_headers").read_text().splitlines():
        if line and not line.startswith(" "):
            block = line.strip()
        elif line.strip():
            k, v = line.strip().split(":", 1)
            if block == "/*":
                headers[k] = v.strip()
            elif k == "Content-Type":
                types[block] = v.strip()

    class H(http.server.SimpleHTTPRequestHandler):
        def guess_type(self, path):
            return types.get(self.path.split("?")[0]) or super().guess_type(path)

        def end_headers(self):
            for k, v in headers.items():
                if k == "Strict-Transport-Security":
                    continue  # local server is plain HTTP
                self.send_header(k, v.replace("; upgrade-insecure-requests", "") if k == "Content-Security-Policy" else v)
            super().end_headers()

        def do_GET(self):
            path, _, query = self.path.partition("?")
            params = dict(p.partition("=")[::2] for p in query.split("&") if p)
            for src, dst, _ in rules:
                spath, _, sq = src.partition("?")
                if sq:
                    k, _, v = sq.partition("=")
                    if path not in ("/", "/index.php") or k not in params or v not in ("*", params[k].strip("/")):
                        continue
                elif spath.endswith("*") and path.startswith(spath[:-1]):
                    dst = dst.replace(":splat", path[len(spath) - 1:])
                elif spath != path:
                    continue
                self.send_response(301)
                self.send_header("Location", quote(unquote(dst), safe="/:?=&*"))
                self.end_headers()
                return
            fs_path = unquote(path).lstrip("/")  # media file names carry diacritics; the URL is percent-encoded
            if not (DIST / fs_path).exists() and not (DIST / fs_path / "index.html").exists():
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write((DIST / "404.html").read_bytes())
                return
            super().do_GET()

        do_HEAD = do_GET

    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), functools.partial(H, directory=str(DIST)))
    print(f"serving http://127.0.0.1:{port}/")
    httpd.serve_forever()


if __name__ == "__main__":
    build()
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve(int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 8000)
