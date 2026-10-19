#!/usr/bin/env python3
"""Builds the school logo SVGs in static/img/logo/ (run once; the output is committed).

Pattern: the Maltese schools' lockup as used by Vyšší odborná škola zdravotnická (vos.mojezdravka.cz):
the official red shield of the Order's works (vector taken unchanged from the Grand Magistry master
lockup, see maltezskyrad.cz static/img/lockup/) and the school's name in two lines of a geometric sans,
in the Order's red. Font: TeX Gyre Adventor Bold (GUST font licence), the substitute for Century Gothic
already used for the Order's lockups; text is set as outlines.

    pip install fonttools && python3 tools/make_logo.py
"""
import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "static" / "img" / "logo"
FONT = TTFont(ROOT / "tools" / "fonts" / "texgyreadventor-bold.otf")
RED = "#e31818"
GLYPHS, CMAP, UPM = FONT.getGlyphSet(), FONT.getBestCmap(), FONT["head"].unitsPerEm

# Shield: paths 0-7 of the master lockup, in its own coordinates (x 113.9-223.5, y 228.2-354.4).
SHIELD_SRC = (ROOT / "tools" / "shield.svg").read_text()
SHIELD_H = 126.2


def text_path(s, x, y, size, tracking=-10):
    """Outline path of a string; tracking in thousandths of an em, as in the Order's lockup spec."""
    pen = SVGPathPen(GLYPHS)
    scale = size / UPM
    kern = {}
    for ch in s:
        g = CMAP[ord(ch)]
        TransformPenWrap = TransformPen(pen, (scale, 0, 0, -scale, x, y))
        GLYPHS[g].draw(TransformPenWrap)
        x += (GLYPHS[g].width + tracking) * scale
    return pen.getCommands(), x


def shield(fill_red=RED, white="#fff"):
    """white: the white ground under the shield outline and the cross; "none" drops the ground (negative use)."""
    paths = re.findall(r"<path[^>]*/>", SHIELD_SRC)
    base, cross = (white, "#000") if white == "none" else (white, white)
    out = [paths[0].replace("#fff", base)] + [x.replace("#e31818", fill_red) for x in paths[1:4]] + [x.replace("#fff", cross) for x in paths[4:]]
    return f'<g transform="translate(-113.9 -228.2)">{"".join(out)}</g>'


def lockup(lines, color=RED, white="#fff", sub=None, text=None):
    """Shield 126 high; name in two lines, cap height ~0.19 of the shield, bottom-aligned like the VOS logo.
    text: name colour when it differs from the shield (white on a photograph)."""
    text = text or color
    size, lead = 33, 37
    x0 = 126
    y_last = SHIELD_H - 18
    paths, width = [], 0
    for i, line in enumerate(lines):
        y = y_last - (len(lines) - 1 - i) * lead
        d, w = text_path(line, x0, y, size)
        paths.append(d)
        width = max(width, w)
    extra = ""
    if sub:
        d, w = text_path(sub, x0, y_last - len(lines) * lead + 2, 17, tracking=40)
        extra = f'<path fill="{text}" d="{d}"/>'
        width = max(width, w)
    body = shield(color, white) + "".join(f'<path fill="{text}" d="{d}"/>' for d in paths) + extra
    w = round(width + 2, 1)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {SHIELD_H}" width="{w}" height="{SHIELD_H}" role="img"><title>Základní škola Maltézských rytířů</title>{body}</svg>\n'


def compact(color=RED, white="#fff"):
    d, w = text_path("ZŠMR", 126, 82, 46, tracking=0)
    width = round(w + 2, 1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {SHIELD_H}" width="{width}" height="{SHIELD_H}" role="img">'
            f'<title>ZŠMR – Základní škola Maltézských rytířů</title>{shield(color, white)}<path fill="{color}" d="{d}"/></svg>\n')


def mark(color=RED, white="#fff"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 110 {SHIELD_H}" width="110" height="{SHIELD_H}" role="img">'
            f'<title>Základní škola Maltézských rytířů</title>{shield(color, white)}</svg>\n')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    name = ["Základní škola", "Maltézských rytířů"]
    files = {
        "zsmr-logo.svg": lockup(name),
        "zsmr-logo-kladno.svg": lockup(name, sub="KLADNO"),
        "zsmr-logo-compact.svg": compact(),
        "zsmr-mark.svg": mark(),
        "zsmr-logo-mono-black.svg": lockup(name, "#000"),
        "zsmr-logo-mono-white.svg": lockup(name, "#fff", white="none"),
        "zsmr-logo-photo.svg": lockup(name, text="#fff"),  # colour shield, white name: on the header photograph
    }
    for f, svg in files.items():
        svg = re.sub(r"(\d+\.\d{2})\d+", r"\1", svg)  # 2 decimals is plenty at these sizes
        (OUT / f).write_text(svg, encoding="utf-8")
        print(f, len(svg))


if __name__ == "__main__":
    main()
