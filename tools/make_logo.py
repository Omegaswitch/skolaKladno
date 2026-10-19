#!/usr/bin/env python3
"""Builds the school logo SVGs in static/img/logo/ (run once; the output is committed).

Pattern: the logo of the Order's school in Prague (Vyšší odborná škola zdravotnická, vos.mojezdravka.cz,
logo-vos-male2.png): the official red shield (vector unchanged from maltezskyrad.cz), "MALTÉZSKÝ ŘÁD /
ČESKÁ REPUBLIKA", a hairline rule with a short tick down at its left end, and the school's name in two
lines of the Order's red. Sizes and spacing are the shared geometry below, measured on the Prague logo and
identical in the Skutec generator. Lettering: Century Gothic Bold per the Order's guidelines, substituted
by TeX Gyre Adventor Bold (GUST font licence) with size and tracking fitted to the Prague logo; outlines.

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
VOS_GLYPHS, VOS_CMAP, VOS_UPM = GLYPHS, CMAP, UPM

# Shield: paths 0-7 of the master lockup, in its own coordinates (x 113.9-223.5, y 228.2-354.4).
SHIELD_SRC = (ROOT / "tools" / "shield.svg").read_text()
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


# ---- Shared logo geometry (identical in skolaKladno, skolaSkutec; source: the Prague school's logo) ----
# Measured on the Prague logo (vos.mojezdravka.cz, logo-vos-male2.png trimmed to 748×266 px; shield ink x 0–216, y 17–265)
# and fitted in TeX Gyre Adventor Bold, so the three school logos have the same sizes and spacing. All numbers are those
# pixels; VOS_X/VOS_Y map them onto the lockup's units (shield ink 126 units tall, as in the Order's cs.svg).
VOS_K = 126.0 / 249
VOS_X = lambda px: -0.22 + px * VOS_K
VOS_Y = lambda px: 0.19 + (px - 17) * VOS_K
VOS_ORDER = (("MALTÉZSKÝ ŘÁD", 61, 60.89, 0.0219), ("ČESKÁ REPUBLIKA", 106, 46.01, 0.0036))  # text, baseline, size, tracking (em)
VOS_TEXT_X, VOS_NAME_X = 233, 253                       # ink left edge of the Order lines and of the school name
VOS_RULE_Y, VOS_RULE_X, VOS_TICK_TO, VOS_RULE_END_PAD, VOS_STROKE = 129.5, 234.5, 172, 10, 1.2
VOS_NAME_BASE, VOS_NAME_PITCH, VOS_NAME_SIZE, VOS_NAME_TRACK = 237, 47, 54.15, 0.001  # last baseline; lines stack upwards


def vos_text(s, ink_left, base, size_px, track):
    """Outline path of s with its ink starting at ink_left (px) on baseline base (px); returns (d, ink right in units)."""
    from fontTools.pens.boundsPen import BoundsPen
    size = size_px * VOS_K
    k = size / VOS_UPM
    lsb = BoundsPen(VOS_GLYPHS)
    VOS_GLYPHS[VOS_CMAP[ord(s[0])]].draw(lsb)
    x, y = VOS_X(ink_left) - lsb.bounds[0] * k, VOS_Y(base)
    pen, box = SVGPathPen(VOS_GLYPHS), BoundsPen(VOS_GLYPHS)
    for ch in s:
        g = VOS_GLYPHS[VOS_CMAP[ord(ch)]]
        g.draw(TransformPen(pen, (k, 0, 0, -k, x, y)))
        g.draw(TransformPen(box, (k, 0, 0, -k, x, y)))
        x += g.width * k + track * size
    return pen.getCommands(), box.bounds[2]


def vos_lockup(shield_svg, name_lines, name_colour, order_colour, title):
    """Shield, MALTÉZSKÝ ŘÁD / ČESKÁ REPUBLIKA, the rule with its tick, and the school name, laid out as the Prague logo."""
    order, right = [], 0
    for s, base, size, track in VOS_ORDER:
        d, r = vos_text(s, VOS_TEXT_X, base, size, track)
        order.append(d)
        right = max(right, r)
    names, name_right = [], 0
    for i, line in enumerate(name_lines):
        base = VOS_NAME_BASE - (len(name_lines) - 1 - i) * VOS_NAME_PITCH
        d, r = vos_text(line, VOS_NAME_X, base, VOS_NAME_SIZE, VOS_NAME_TRACK)
        names.append(d)
        name_right = max(name_right, r)
    right = max(right, name_right)
    rule = (f'<path fill="none" stroke="{order_colour}" stroke-width="{VOS_STROKE * VOS_K:.2f}" '
            f'd="M{VOS_X(VOS_RULE_X):.2f} {VOS_Y(VOS_TICK_TO):.2f}V{VOS_Y(VOS_RULE_Y):.2f}H{name_right - VOS_RULE_END_PAD * VOS_K:.2f}"/>')
    top, w, h = VOS_Y(0) - 0.5, right + 1.5, 126.6 - (VOS_Y(0) - 0.5)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-0.5 {top:.2f} {w:.2f} {h:.2f}" width="{w:.2f}" height="{h:.2f}" role="img">'
            f'<title>{title}</title>{shield_svg}<path fill="{order_colour}" d="{" ".join(order)}"/>{rule}'
            f'<path fill="{name_colour}" d="{" ".join(names)}"/></svg>\n')
# ---- end of shared logo geometry ----


def lockup(name_color=RED, order_color="#000", red=RED, white="#fff"):
    return vos_lockup(shield(red, white), ["Základní škola", "Maltézských rytířů"], name_color, order_color,
                      "Maltézský řád – Základní škola Maltézských rytířů")


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
        svg = re.sub(r"(\d+\.\d{4})\d+", r"\1", svg)  # 4 decimals: fewer would distort the shield outline's 0.998785 scale
        (OUT / f).write_text(svg, encoding="utf-8")
        print(f, len(svg))


if __name__ == "__main__":
    main()
