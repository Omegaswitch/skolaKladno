# Design system: zsmr.eu

zsmr.eu uses the **maltezskyrad.cz design system unchanged**: same tokens (`--red #e31a18`, `--red-text #c80e00`, `--ink #454545`, `--grey #f3f3f3`, `--rule #c7c7c7`), the same type pairing (EB Garamond 500 for headings and row titles, Asap for everything a visitor reads or operates), the same 4px spacing scale, square 2px controls, hairline-ruled record rows, and the same motion and reduced-motion rules. `static/css/site.css` is the maltezskyrad stylesheet with the calendar widget and banner photograph removed and a short school section appended. Read `maltezskyrad/DESIGN.md` for the full system. This file records only what differs.

**Character: "The School Register."** The Priory site is a quiet register. The school is the same register, made a little more structured: firmer information sections, a visible editorial hierarchy for news, and more photographs, because a school's life is shown in pictures.

## What changes, and why

| Element | maltezskyrad.cz | zsmr.eu | Why |
|---|---|---|---|
| Identity band | Grand Magistry banner photograph with the "ORDER OF MALTA" lockup | **School photograph** (Krkonoše landscape from a school trip, no people) under a dark veil, with the school lockup in its photo version (colour shield, white name) on the left and, on the right, a ruled note: tagline in Garamond, founder in Asap, both white | Same idea as the Priory banner (a photograph with white lettering), but the school's own picture and lockup: a school is a work of the Order, identified by the shield of works (as on vos.mojezdravka.cz). On white, the shield's white edge disappears. |
| Top bar | Social links, language switch | Link to the founder (maltezskyrad.cz), the office phone and e-mail | Parents look for the phone first. One language only. |
| Home | Intro + facts, calendar, works, news | Short intro + facts (phones on the first screen), **"Pro rodiče a žáky" record rows with the nine-class grid**, **news as a lead story with photograph and a ruled list of four**, Družina and kroužky | Families first (critique 2026-10-19): documents and phones before news, on phones too. |
| News archive | Category tabs, years | Same, plus **pagination** (30 per page; 436 articles) and photo galleries | Size of the archive. |
| Footer | Grey nav, white identity, red legal band | Same three bands; the grey band lists each section's pages; the white band adds the **funded-project publicity logos** (OP VVV, OP JAK, PPUč, Kladno), and a licence line | EU-funded projects require visible publicity; the old site showed them in the footer. |

## Added components

- **Story** (`.story`, `.story--lead`): photograph at the Order's 800×470 basic image ratio (4:3 thumbnail in the list), muted date and category line, Garamond title; the whole story is one tap target. The photograph zooms by 2% on hover (pointer devices only, reduced-motion safe).
- **Class grid** (`.class-grid`): nine outlined 44px squares with Garamond numerals; hover fills Menu Graphite. Each links to that class's news.
- **Gallery** (`.prose .gallery`) and **photo run** (`.photo-run`): imported galleries, and any two or more consecutive photos in an article, become a 4:3 crop grid with 6px gutters; each photo links to its full file. Single photos are capped at 80vh. Long imported photo stories stay readable without editing their text.
- **Pagination**: outlined 44px squares, current page filled graphite, like the archive tabs.
- **Form** (Schránka důvěry): labelled fields with 44px targets and a red focus ring, a hidden honeypot, the result announced in a live region.

## Rules kept

- Red is signal only: links, the one filled button (Odeslat), focus and the active menu underline. Never a band or a heading colour inside the frame.
- Rows, not cards. The only "card-like" shapes are photographs, which are unframed.
- No icons, illustrations or emblems beyond the logo set listed in `docs/logo.md`; `check.py` fails the build for any other file under `/img/`.
