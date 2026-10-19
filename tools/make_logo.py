#!/usr/bin/env python3
"""Builds the school logo SVGs in static/img/logo/ (run once; the output is committed).

Pattern: the lockup of the Order's school Vyšší odborná škola zdravotnická (vos.mojezdravka.cz,
logo-vos-male2.png), measured and rebuilt: the official Czech lockup of the Order (red shield +
"MALTÉZSKÝ ŘÁD / ČESKÁ REPUBLIKA", vector taken unchanged from maltezskyrad.cz static/img/lockup/cs.svg),
a hairline rule under it with a short tick down at its left end, and the school's name in two lines of
the Order's red below the rule. Font of the name: TeX Gyre Adventor Bold (GUST font licence), the
substitute for Century Gothic already used for the Order's lockups; all text is set as outlines.

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
# "MALTÉZSKÝ ŘÁD / ČESKÁ REPUBLIKA": path 8 of the same official lockup (cs.svg), in viewBox coordinates.
ORDER_SRC = (ROOT / "tools" / "order-lockup-cs.svg").read_text().strip()
SHIELD_H = 126.2


def text_path(s, x, y, size, tracking=-10):
    """Outline path of a string; tracking in thousandths of an em, as in the Order's lockup spec."""
    pen = SVGPathPen(GLYPHS)
    scale = size / UPM
    for ch in s:
        g = CMAP[ord(ch)]
        GLYPHS[g].draw(TransformPen(pen, (scale, 0, 0, -scale, x, y)))
        x += (GLYPHS[g].width + tracking) * scale
    return pen.getCommands(), x


def shield(fill_red=RED, white="#fff"):
    """white: the white ground under the shield outline and the cross; "none" drops the ground (negative use)."""
    paths = re.findall(r"<path[^>]*/>", SHIELD_SRC)
    base, cross = (white, "#000") if white == "none" else (white, white)
    out = [paths[0].replace("#fff", base)] + [x.replace("#e31818", fill_red) for x in paths[1:4]] + [x.replace("#fff", cross) for x in paths[4:]]
    return f'<g transform="translate(-113.9 -228.2)">{"".join(out)}</g>'


def lockup(name_color=RED, order_color="#000", red=RED, white="#fff"):
    """VOS geometry in shield units (shield 126.2 high): rule at y 57.3 from x 118.6, tick down to y 78,
    name at x 128.2, size 27.5, baselines 87.6 and 111.2 (measured on logo-vos-male2.png)."""
    names, end = [], 0
    for line, base in (("Základní škola", 87.6), ("Maltézských rytířů", 111.2)):
        d, x = text_path(line, 128.2, base, 27.5, tracking=0)
        names.append(f'<path fill="{name_color}" d="{d}"/>')
        end = max(end, x)
    rule = f'<path fill="none" stroke="{order_color}" stroke-width=".6" d="M118.6 57.3H{end - 5:.1f}M118.9 57V78"/>'
    order = ORDER_SRC.replace('fill="#fff"', f'fill="{order_color}"')
    w = round(max(end, 351.1) + 1, 1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -7.2 {w} 133.4" width="{w}" height="133.4" role="img">'
            f'<title>Maltézský řád – Základní škola Maltézských rytířů</title>{shield(red, white)}{order}{rule}{"".join(names)}</svg>\n')


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
    files = {
        "zsmr-logo.svg": lockup(),  # light grounds: Order text black (CoA guidelines: emblem text black)
        "zsmr-logo-photo.svg": lockup(order_color="#fff"),  # photographs and dark grounds, as the VOS original
        "zsmr-logo-compact.svg": compact(),
        "zsmr-mark.svg": mark(),
        "zsmr-logo-mono-black.svg": lockup("#000", "#000", "#000"),
        "zsmr-logo-mono-white.svg": lockup("#fff", "#fff", "#fff", white="none"),
    }
    for f, svg in files.items():
        svg = re.sub(r"(\d+\.\d{2})\d+", r"\1", svg)  # 2 decimals is plenty at these sizes
        (OUT / f).write_text(svg, encoding="utf-8")
        print(f, len(svg))


if __name__ == "__main__":
    main()
