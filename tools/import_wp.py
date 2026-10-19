#!/usr/bin/env python3
"""One-off migration of zsmr.eu (WordPress) into content/ files. Adapted from maltezskyrad.cz.

Standard library only. Reads the public WordPress REST API, sanitises every
page and post through an allowlist HTML parser, mirrors only the media the
content references, and writes front-matter HTML files that build.py renders.

    python3 tools/import_wp.py            # fetch + write content/pages, content/news, static/media
    python3 tools/import_wp.py --check    # run the sanitiser self-test only

Re-running overwrites imported files; hand-edited files are protected by
"imported": false in their front matter.
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "http://www.zsmr.eu/index.php?rest_route=/wp/v2"  # the old site's HTTPS certificate chain is broken; plain-permalink install
OLD_HOSTS = ("www.zsmr.eu", "zsmr.eu", "www.zsmr.cz", "zsmr.cz")
ORIGIN = "http://www.zsmr.eu"
SKIP_PAGES = {2, 18, 21}  # WordPress sample page, theme demo page, empty "Blog" placeholder
UPLOADS = "/wp-content/uploads/"
MAX_IMG_W = 1024

# ---------------------------------------------------------------- sanitiser

ALLOWED = {"p", "h2", "h3", "h4", "ul", "ol", "li", "a", "strong", "em", "br", "blockquote",
           "figure", "figcaption", "img", "table", "thead", "tbody", "tr", "th", "td", "hr", "video", "audio"}
RENAME = {"b": "strong", "i": "em", "h1": "h2", "h5": "h4", "h6": "h4"}
VOID = {"br", "img", "hr"}
# legacy emblem renditions on the old site; replaced by official originals (see docs/asset-manifest.md)
LEGACY_EMBLEMS = re.compile(r"/(znak(-\d+)?|logo[^/]*)\.(png|jpe?g|gif|svg)$", re.I)
DROP_WITH_CONTENT = {"script", "style", "noscript", "object", "svg", "form", "button", "select", "textarea"}
ATTRS = {"a": {"href"}, "img": {"src", "alt", "srcset"}, "video": {"src"}, "audio": {"src"}, "td": {"colspan", "rowspan"}, "th": {"colspan", "rowspan"}}


class Sanitiser(HTMLParser):
    """Rebuilds HTML from an allowlist. Unknown tags are unwrapped, never passed through."""

    def __init__(self, url_map):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.skip, self.url_map = [], [], 0, url_map

    def handle_starttag(self, tag, attrs):
        if tag in DROP_WITH_CONTENT:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "iframe":
            src = dict(attrs).get("src") or ""
            href = self.url_map(src)
            if href:
                self.out.append(f'<p><a href="{html.escape(href)}">{html.escape(_iframe_label(href))}</a></p>')
            return
        tag = RENAME.get(tag, tag)
        if tag not in ALLOWED:
            return
        if tag == "ul" and "blocks-gallery-grid" in (dict(attrs).get("class") or ""):
            self.out.append('<ul class="gallery">')
            self.stack.append(tag)
            return
        keep = []
        for k, v in attrs:
            if k in ATTRS.get(tag, ()) and v is not None:
                if k == "src" and LEGACY_EMBLEMS.search(v or ""):
                    return
                if k in ("href", "src"):
                    v = self.url_map(v)
                    if not v:
                        continue
                if k == "srcset":
                    continue  # resolved to a single local file via src
                keep.append(f' {k}="{html.escape(v, quote=True)}"')
        if tag == "img" and not any(a.startswith(" src=") for a in keep):
            return
        if tag == "a" and not any(a.startswith(" href=") for a in keep):
            return  # anchor without a target: unwrap (its closing tag is ignored, not in stack)
        if tag in ("video", "audio"):
            keep.append(' controls preload="none"')
        self.out.append(f"<{tag}{''.join(keep)}>")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        tag = RENAME.get(tag, tag)
        if tag in ALLOWED and tag not in VOID and tag in self.stack:
            while self.stack:
                t = self.stack.pop()
                self.out.append(f"</{t}>")
                if t == tag:
                    break

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))

    def result(self):
        while self.stack:
            self.out.append(f"</{self.stack.pop()}>")
        s = "".join(self.out)
        s = re.sub(r"[ \t\r\f\v]+", " ", s)
        s = re.sub(r"\s*\n\s*", "\n", s)
        for _ in range(3):  # empty blocks left behind by unwrapped layout markup
            s = re.sub(r"<(p|li|h2|h3|h4|strong|em|figure|figcaption|blockquote)>\s*(<br>\s*)*</\1>", "", s)
        s = re.sub(r"(<br>\s*){2,}", "<br>", s)
        s = re.sub(r">\s+<", ">\n<", s)
        return s.strip()


def _iframe_label(href):
    return "Přehrát záznam (YouTube)" if "youtu" in href else "Otevřít vložený obsah"


def sanitise(fragment, url_map):
    p = Sanitiser(url_map)
    p.feed(fragment)
    p.close()
    return p.result()


def _self_test():
    m = lambda u: None if u.startswith("javascript:") else u
    out = sanitise('<div style="x"><p onclick="a()">A<script>evil()</script><b>B</b></p>'
                   '<a href="javascript:alert(1)">x</a><img src="/a.jpg" onerror="z"><iframe src="https://youtu.be/q"></iframe></div>', m)
    assert "script" not in out and "onclick" not in out and "onerror" not in out and "style" not in out, out
    assert "<strong>B</strong>" in out and 'href="javascript' not in out and '<img src="/a.jpg">' in out, out
    assert 'href="https://youtu.be/q"' in out, out
    assert sanitise("<p>&lt;script&gt;</p>", m) == "<p>&lt;script&gt;</p>"
    assert sanitise('<a><img src="/b.jpg"></a><p><a href="/x/">y</a></p>', m) == '<img src="/b.jpg"><p><a href="/x/">y</a></p>'
    assert tidy_files('<a href="/m/a_b.pdf">a_b</a><a href="/m/a_b.pdf">Stáhnout</a>') == '<p class="file"><a href="/m/a_b.pdf">Stáhnout</a> (PDF)</p>'
    assert tidy_files('<a href="/m/x.pdf">Program koncertu</a><a href="/m/x.pdf">Stáhnout</a>') == '<p class="file"><a href="/m/x.pdf">Program koncertu</a> (PDF)</p>'
    assert text_excerpt('<p class="file"><a href="/m/x.pdf">Stáhnout</a> (PDF)</p>') == ""
    class _M:
        local = staticmethod(lambda u: "/media/" + u.split(UPLOADS)[1])
    um = make_url_map(_M(), {"p=5": "/2020/01/02/a/", "page_id=7": "/b/", "cat=9": "/aktuality/c/"})
    assert um("http://www.zsmr.eu/?p=5") == "/2020/01/02/a/" and um("http://zsmr.eu/?page_id=7/") == "/b/"
    assert um("/?cat=9") == "/aktuality/c/" and um("http://www.zsmr.eu/?p=404") == "/aktuality/"
    assert um("http://www.zsmr.eu/wp-content/uploads/2020/06/x.pdf") == "/media/2020/06/x.pdf"
    assert um("https://www.zsmr.cz/") == "https://www.zsmr.cz/" and um("javascript:alert(1)") is None
    assert '<ul class="gallery">' in sanitise('<ul class="blocks-gallery-grid"><li>x</li></ul>', m)
    assert sanitise('<video src="/v.mp4" autoplay></video>', m) == '<video src="/v.mp4" controls preload="none"></video>'
    print("sanitiser self-test ok")


# ---------------------------------------------------------------- fetching


def retry(fn, tries=5):
    """The old server answers 503 under load; back off and try again."""
    import time
    for i in range(tries):
        try:
            return fn()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(3 * (i + 1))


def get_json(path):
    return retry(lambda: _get_json(path))


def _get_json(path):
    with urllib.request.urlopen(f"{API}/{path}".replace("?", "&").replace("&rest_route", "?rest_route", 1), timeout=120) as r:
        return json.load(r), r.headers


def get_all(kind):
    items, page = [], 1
    while True:
        data, headers = get_json(f"{kind}?per_page=100&page={page}")
        items += data
        if page >= int(headers.get("X-WP-TotalPages", 1)):
            return items
        page += 1


def download(url, dest):
    if dest.exists():
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    fetch = _norm(url)
    try:
        dest.write_bytes(retry(lambda: urllib.request.urlopen(urllib.parse.quote(fetch, safe=":/%?=&"), timeout=120).read()))
        return True
    except Exception as e:  # keep migrating; report missing files at the end
        print(f"  ! could not download {url}: {e}", file=sys.stderr)
        return False


# ---------------------------------------------------------------- mapping


class Media:
    """Maps WordPress upload URLs to local /media/ paths, downloading only what content uses."""

    def __init__(self, media_items):
        self.by_id = {m["id"]: m for m in media_items}
        self.variants = {}  # any size URL -> (best URL <= MAX_IMG_W)
        for m in media_items:
            d = m.get("media_details") or {}
            sizes = [(s.get("width", 0), s["source_url"]) for s in (d.get("sizes") or {}).values() if s.get("source_url")]
            sizes.append((d.get("width", 0) or 0, m["source_url"]))
            fitting = [s for s in sizes if 0 < s[0] <= MAX_IMG_W] or sizes
            # documents keep their own file; their "sizes" are only JPEG previews of page one
            best = max(fitting)[1] if m.get("mime_type", "").startswith("image/") else m["source_url"]
            for _, u in sizes:
                self.variants[_norm(u)] = best
        self.missing = []

    def local(self, url):
        url = self.variants.get(_norm(url), url)
        rel = urllib.parse.unquote(urllib.parse.urlparse(url).path.split(UPLOADS, 1)[1])
        dest = ROOT / "static" / "media" / rel
        if not download(url, dest):
            self.missing.append(url)
        return "/media/" + urllib.parse.quote(rel)

    def featured(self, media_id):
        m = self.by_id.get(media_id)
        return self.local(m["source_url"]) if m else None


def _norm(u):
    u = re.sub(r"^(https?:)?//", "http://", u)
    for h in OLD_HOSTS:
        u = u.replace(f"http://{h}/", ORIGIN + "/")
    return u


def post_url(p):
    return f"/{p['date'][:4]}/{p['date'][5:7]}/{p['date'][8:10]}/{urllib.parse.unquote(p['slug'])}/"


def legacy_map(pages, posts, cats):
    """Old query-string addresses (?p=, ?page_id=, ?cat=) -> new paths; the same table feeds vercel.json."""
    m = {f"p={p['id']}": post_url(p) for p in posts}
    m |= {f"page_id={p['id']}": f"/{urllib.parse.unquote(p['slug'])}/" for p in pages if p["id"] not in SKIP_PAGES}
    m |= {f"cat={c['id']}": f"/aktuality/{c['slug']}/" for c in cats if c["count"]}
    m["page_id=21"] = "/aktuality/"
    return m


def make_url_map(media, legacy):
    def url_map(u):
        u = html.unescape((u or "").strip())
        if not u or u.startswith(("javascript:", "data:", "vbscript:")):
            return None
        if u.startswith(("#", "mailto:", "tel:")):
            return u
        if u.startswith("//"):
            u = "http:" + u
        parsed = urllib.parse.urlparse(u)
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            return None
        host = parsed.netloc.lower()
        if host in OLD_HOSTS or not host:
            if UPLOADS in parsed.path:
                return media.local(ORIGIN + parsed.path)
            if parsed.path.startswith("/large-files/"):  # files uploaded outside WordPress (the school video)
                rel = urllib.parse.unquote(parsed.path)
                if not download(ORIGIN + parsed.path, ROOT / "static" / rel.lstrip("/")):
                    media.missing.append(u)
                return parsed.path
            q = urllib.parse.parse_qs(parsed.query)
            for k in ("p", "page_id", "cat"):
                if k in q:
                    return legacy.get(f"{k}={q[k][0].strip('/')}", "/aktuality/" if k != "page_id" else "/")
            if "zsmr.cz" in host:
                return u  # the school's other domain; kept as an external link
            path = parsed.path or "/"
            return "/" if path in ("/", "/index.php") else path
        yt = re.match(r"https?://www\.youtube(?:-nocookie)?\.com/embed/([\w-]{6,})", u)
        if yt:
            return f"https://www.youtube.com/watch?v={yt.group(1)}"
        return u
    return url_map


def lead_image(clean):
    m = re.match(r'\s*(?:<p>)?\s*<img src="([^"]+)"[^>]*>\s*(?:</p>)?', clean)
    if not m:
        return None, clean
    return m.group(1), clean[m.end():].lstrip()


# WordPress file block: optional title link + a second "Stáhnout" link to the same file
FILE_BLOCK = re.compile(r'(?:<a href="([^"]+)">([^<]*)</a>\s*)?<a href="([^"]+)">Stáhnout</a>')


def tidy_files(clean):
    def one(m):
        href, name = m.group(3), (m.group(2) or "").strip()
        ext = href.rsplit(".", 1)[-1].upper() if "." in href.rsplit("/", 1)[-1] else ""
        if m.group(1) != href or not name or re.fullmatch(r"[\w.-]+", name):  # raw filename is no title
            name = "Stáhnout"
        return f'<p class="file"><a href="{href}">{name}</a>{f" ({ext})" if ext else ""}</p>'
    return FILE_BLOCK.sub(one, clean)


def text_excerpt(clean, n=200):
    clean = re.sub(r'<p class="file">.*?</p>', " ", clean)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", clean))).strip()
    return t if len(t) <= n else t[: t.rfind(" ", 0, n)] + "…"


def write(path, meta, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_text(encoding="utf-8")
        if '"imported": false' in old.split("\n---\n", 1)[0]:
            return  # hand-edited; never overwrite
    meta = {**meta, "imported": True}
    path.write_text("---\n" + json.dumps(meta, ensure_ascii=False, indent=1) + "\n---\n" + body + "\n", encoding="utf-8")


def write_redirects(legacy):
    """Old ?p= / ?page_id= / ?cat= addresses and a few WordPress leftovers -> permanent redirects in vercel.json."""
    rules = []
    for key, dest in legacy.items():
        k, v = key.split("=")
        rules.append({"source": "/:file(index\\.php)?", "has": [{"type": "query", "key": k, "value": f"^{v}/?$"}], "destination": dest, "permanent": True})
    for k, dest in (("paged", "/aktuality/"), ("author", "/aktuality/"), ("feed", "/feed.xml"), ("m", "/aktuality/"), ("s", "/aktuality/")):
        rules.append({"source": "/:file(index\\.php)?", "has": [{"type": "query", "key": k}], "destination": dest, "permanent": True})
    rules.append({"source": "/wp-content/uploads/:path*", "destination": "/media/:path*", "permanent": True})
    f = ROOT / "vercel.json"
    v = json.loads(f.read_text(encoding="utf-8"))
    v["redirects"] = rules
    f.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    if "--redirects" in sys.argv:
        write_redirects(json.loads((ROOT / "content" / "legacy.json").read_text(encoding="utf-8")))
        return
    if "--check" in sys.argv:
        _self_test()
        return
    _self_test()
    print("fetching…")
    pages, posts, media_items, cats = get_all("pages"), get_all("posts"), get_all("media"), get_all("categories")
    media = Media(media_items)
    legacy = legacy_map(pages, posts, cats)
    url_map = make_url_map(media, legacy)
    cat_slug = {c["id"]: c["slug"] for c in cats}

    for p in pages:
        if p["id"] in SKIP_PAGES or p["id"] == 221:  # 221: the events-calendar plugin page, rendered by build.py
            continue
        clean = tidy_files(sanitise(p["content"]["rendered"], url_map))
        image, clean = lead_image(clean)
        url = legacy[f"page_id={p['id']}"]
        write(ROOT / "content" / "pages" / url.strip("/") / "index.html", {
            "title": html.unescape(p["title"]["rendered"]), "url": url, "wp_id": p["id"],
            "modified": p["modified"][:10], "image": image, "status": "existing",
        }, clean)

    for p in posts:
        path = post_url(p)
        clean = tidy_files(sanitise(p["content"]["rendered"], url_map))
        write(ROOT / "content" / "news" / (path.strip("/") + ".html"), {
            "title": html.unescape(p["title"]["rendered"]), "url": path, "wp_id": p["id"],
            "date": p["date"][:16], "categories": [cat_slug[c] for c in p["categories"] if c in cat_slug],
            "image": media.featured(p["featured_media"]), "excerpt": text_excerpt(clean), "status": "existing",
        }, clean)

    write_redirects(legacy)
    (ROOT / "content" / "legacy.json").write_text(json.dumps(legacy, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"pages {len(pages)}, posts {len(posts)}, legacy URLs {len(legacy)}, missing media {len(media.missing)}")
    for u in media.missing:
        print("  missing:", u)


if __name__ == "__main__":
    main()
