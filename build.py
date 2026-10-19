#!/usr/bin/env python3
"""Static site generator for zsmr.eu (Základní škola Maltézských rytířů, Kladno). Python 3.10+, standard library only.
Same architecture as maltezskyrad.cz: content/ -> dist/, no CMS, no database.

    python3 build.py                 preview build into dist/ (noindex, content-status labels shown)
    python3 build.py --production    production build (indexable, no status labels)
    python3 build.py serve [port]    preview build, then serve dist/ with _headers and _redirects applied
"""
import html
import json
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
ASSET_VERSION = datetime.now().strftime("%Y%m%d%H%M")
MONTHS = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna", "září", "října", "listopadu", "prosince"]
STATUS = {"verified": "Ověřený obsah", "existing": "Převzato ze stávajícího webu – čeká na revizi",
          "new": "Nový text – čeká na schválení", "approval": "Vyžaduje schválení školou nebo zřizovatelem"}
esc = lambda s: html.escape(str(s or ""), quote=True)


# ---------------------------------------------------------------- content


def read_doc(path):
    _, meta, body = path.read_text(encoding="utf-8").split("---\n", 2)
    return json.loads(meta), body.strip()


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
    body = body.replace('<figure><ul class="gallery"></ul></figure>', "")  # empty gallery blocks, empty on the old site too
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


def logo(eager=True):
    return ('<img class="school-logo" src="/img/logo/zsmr-logo-photo.svg" alt="Maltézský řád – Základní škola Maltézských rytířů" width="368" height="133"'
            + (' fetchpriority="high"' if eager else ' loading="lazy"') + ">")


def layout(*, url, title, body, description="", image=None, status=None, main_class=""):
    names, c = SITE["names"], SITE["contact"]
    full_title = f"{title} | {names['site']}" if title != names["site"] else title
    canonical = SITE["baseUrl"] + url
    og_image = SITE["baseUrl"] + (image or "/img/logo/zsmr-og.png")
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
 <div class="idband"><div class="wrap">
  <a class="idband-home" href="/">{logo()}</a>
  <p class="idband-meta"><span>{esc(names['tagline'])}</span><span>Zřizovatel: {esc(names['founder'])}</span></p>
 </div></div>
 <nav class="mainnav" aria-label="Hlavní menu"><div class="wrap">
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <div id="menu" class="menu">{nav_html(url)}</div>
 </div></nav>
</header>
<main id="main" class="{main_class}" tabindex="-1">
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
 <p class="small">Zprávu přečte vedení školy. Pokud formulář nefunguje, napište na <a href="mailto:skola@zsmr.cz">skola@zsmr.cz</a>.</p>
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
  {'' if url == '/kontakty/' else f'<div class="prose">{enhance_body(p["body"])}</div>'}
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
  <p class="lead-s">Termíny prázdnin a dalších akcí školního roku jsou v dokumentu, který škola vydává na každý rok:</p>
  {holidays.group(0) if holidays else '<p><a href="/dokumenty-o-skole/">Dokumenty o škole</a></p>'}
  <p>O konkrétních akcích, výletech a konzultacích informujeme v <a href="/aktuality/">aktualitách</a>.</p>
 </div></div>
 <div class="page-side">{side_nav('/kalendar/')}</div>
</div>"""
    return layout(url="/kalendar/", title="Kalendář akcí", body=body, status="new",
                  description="Kalendář akcí Základní školy Maltézských rytířů: prázdniny a akce školního roku.")


def render_simple(url, title, inner, status=None):
    body = f'<div class="wrap page page--simple"><header class="page-head"><h1 class="display">{esc(title)}</h1></header><div class="prose">{inner}</div></div>'
    return layout(url=url, title=title, body=body, status=status)


NEWS_EDITOR_URL = "/pridat-aktualitu/"


def render_news_editor():
    """Staff page for publishing news (api/news.js); not linked, not indexed, behind a password. Markup as on maltezskyrad.cz."""
    tpl = (ROOT / "tools" / "news-editor.html").read_text(encoding="utf-8").replace("{ASSET_VERSION}", ASSET_VERSION)
    h = layout(url=NEWS_EDITOR_URL, title="Přidat aktualitu", body=tpl, description="Přidání aktuality na web školy.")
    return h.replace("<head>\n", '<head>\n<meta name="robots" content="noindex, nofollow">\n', 1) if PRODUCTION else h


# ---------------------------------------------------------------- output


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
    write("/", render_home())
    write("/kalendar/", render_calendar())
    for url, p in PAGES.items():
        write(url, render_page(p))
    for i, n in enumerate(NEWS):
        write(n["url"], render_article(n, NEWS[i + 1] if i + 1 < len(NEWS) else None, NEWS[i - 1] if i else None))
    listing = paginate(NEWS, "/aktuality/")
    for c in CATS:
        items = [n for n in NEWS if c in n.get("categories", [])]
        listing += paginate(items, f"/aktuality/{c}/", active=c) if items else []
    for y in sorted({n["date"][:4] for n in NEWS}):
        write(f"/aktuality/{y}/", render_news_index([n for n in NEWS if n["date"].startswith(y)], year=y, url=f"/aktuality/{y}/"))
        listing.append(f"/aktuality/{y}/")
    write(NEWS_EDITOR_URL, render_news_editor())
    (DIST / NEWS_EDITOR_URL.strip("/") / "news.json").write_text(json.dumps(  # the editor's list of posts to edit or delete
        [{"path": n["src"], "url": n["url"], "title": n["title"], "date": n["date"][:16], "author": n.get("author")} for n in NEWS],
        ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    write("/404.html", render_simple("/404.html", "Stránka nenalezena",
                                     '<p>Stránka na této adrese neexistuje. Mohla být přesunuta při obnově webu.</p>'
                                     '<p><a class="link-strong" href="/">Úvodní stránka</a> · <a class="link-strong" href="/aktuality/">Aktuality</a> · <a class="link-strong" href="/kontakty/">Kontakty</a></p>'))
    urls = ["/", "/kalendar/"] + list(PAGES) + [n["url"] for n in NEWS] + listing
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
                                      "".join(f"<url><loc>{SITE['baseUrl']}{u}</loc></url>" for u in urls) + "</urlset>", encoding="utf-8")
    (DIST / "robots.txt").write_text(("User-agent: *\nAllow: /\nDisallow: /pridat-aktualitu/\nDisallow: /api/\n\nSitemap: " + SITE["baseUrl"] + "/sitemap.xml\n") if PRODUCTION
                                     else "User-agent: *\nDisallow: /\n", encoding="utf-8")
    (DIST / "feed.xml").write_text(rss(), encoding="utf-8")
    (DIST / "_headers").write_text(HEADERS + ("" if PRODUCTION else "/*\n  X-Robots-Tag: noindex, nofollow\n"), encoding="utf-8")
    (DIST / "_redirects").write_text(redirect_lines(), encoding="utf-8")
    print(f"built {len(PAGES)} pages, {len(NEWS)} news, {'production' if PRODUCTION else 'preview'} → {DIST}")


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
