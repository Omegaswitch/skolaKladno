# Content inventory and migration map

Source: the WordPress REST API of www.zsmr.eu, read on 19 October 2026 (`tools/import_wp.py`). The old site uses plain permalinks (`/?page_id=N`, `/?p=N`, `/?cat=N`), so **every old address changes**. Each one has a permanent (301) redirect in `vercel.json`, generated from `content/legacy.json`.

## Totals

| Item | Old site | New site |
|---|---|---|
| Pages | 21 | 18 imported, 3 excluded (below), 4 new section pages, 1 calendar page |
| News posts | 436 (2017–2026) | 436, all at `/YYYY/MM/DD/slug/` |
| Categories | 20 (18 with posts) | archive pages at `/aktuality/<slug>/` |
| Media library | 3124 files | only the files the content uses: images reduced to the largest WordPress size ≤ 1024 px; PDF, ODT, PPTX, XLSX, video and audio unchanged |
| Legacy addresses redirected | | 473 + `?paged`, `?author`, `?feed`, `?m`, `?s`, `/wp-content/uploads/*` |

## Pages

| Old address | Title | New address | In menu | Note |
|---|---|---|---|---|
| `/?page_id=2` | ZZ Zkušební stránka | `/` | no | WordPress sample page: **not migrated**, redirects to `/`. |
| `/?page_id=18` | ZZ The New UMoMA Opens its Doors | `/` | no | Theme demo page (English museum text): **not migrated**, redirects to `/`. |
| `/?page_id=21` | Blog | `/aktuality/` | yes | Empty WordPress blog placeholder → redirects to `/aktuality/`. |
| `/?page_id=116` | Profil školy | `/profil-skoly/` | yes | Contains the school video (`/large-files/DCS_ZS-Maltezska-Kladno.mp4`), migrated. |
| `/?page_id=118` | Školné a další platby | `/skolne-a-dalsi-platby/` | yes |  |
| `/?page_id=121` | Dokumenty o škole | `/dokumenty-o-skole/` | yes |  |
| `/?page_id=123` | Dokumenty pro rodiče | `/dokumenty-pro-rodice/` | yes |  |
| `/?page_id=125` | Pedagogové | `/pedagogove/` | yes |  |
| `/?page_id=127` | Hledáme | `/hledame/` | yes |  |
| `/?page_id=130` | Přehled tříd | `/prehled-trid/` | yes |  |
| `/?page_id=138` | O družině | `/o-druzine/` | yes |  |
| `/?page_id=141` | Přehled kroužků | `/prehled-krouzku/` | yes |  |
| `/?page_id=143` | Kontakty | `/kontakty/` | yes | Shown as a structured contact card. The page names **www.zsmr.cz** as the website while the site runs on zsmr.eu: confirm the canonical domain. |
| `/?page_id=221` | Kalendář akcí | `/kalendar/` | yes | Events-calendar plugin page; the plugin held **no events**. Replaced by `/kalendar/`, which points to the school-year dates document. |
| `/?page_id=232` | Prohlášení o přístupnosti | `/prohlaseni-o-pristupnosti/` | no | Text describes the old WordPress site; **must be rewritten** for the new site (flagged). |
| `/?page_id=237` | Ochrana osobních údajů – GDPR | `/ochrana-osobnich-udaju-gdpr/` | no | GDPR notice kept unchanged; review that it mentions no WordPress-specific processing. |
| `/?page_id=319` | Rozvrh | `/rozvrh/` | yes |  |
| `/?page_id=444` | Schránka důvěry | `/schranka-duvery/` | yes | Contact Form 7 form replaced by `api/trust.js` (same four fields). |
| `/?page_id=4944` | Výsledky voleb do školské rady | `/vysledky-voleb-do-skolske-rady/` | no | Election results (2024). Kept as a page. |
| `/?page_id=5072` | Konzultace o prospěchu 21. listopadu | `/konzultace-o-prospechu-21-listopadu/` | no | Dated notice (21 Nov 2024). Kept; consider moving to news or removing. |
| `/?page_id=5500` | Konzultace o prospěchu | `/konzultace-o-prospechu/` | no | Dated notice (10 Apr 2025). Kept; consider moving to news or removing. |

New pages: `/skola/`, `/tridy/`, `/druzina/`, `/krouzky/` (section indexes, as the old menu's parent items had no page), `/kalendar/`, `/pridat-aktualitu/` (staff only).

## Categories

| Old address | Name | Posts | New address | Note |
|---|---|---|---|---|
| `/?cat=8` | 1. třída | 8 | `/aktuality/1-trida/` |  |
| `/?cat=9` | 2. třída | 10 | `/aktuality/2-trida/` |  |
| `/?cat=10` | 3. třída | 12 | `/aktuality/3-trida/` |  |
| `/?cat=11` | 4. třída | 8 | `/aktuality/4-trida/` |  |
| `/?cat=12` | 5. třída | 12 | `/aktuality/5-trida/` |  |
| `/?cat=13` | 6. třída | 20 | `/aktuality/6-trida/` |  |
| `/?cat=14` | 7. třída | 23 | `/aktuality/7-trida/` |  |
| `/?cat=15` | 8. třída | 15 | `/aktuality/8-trida/` |  |
| `/?cat=16` | 9. třída | 27 | `/aktuality/9-trida/` |  |
| `/?cat=17` | Akce družiny | 53 | `/aktuality/akce_druziny/` |  |
| `/?cat=19` | Keramický kroužek | 5 | `/aktuality/keramicky-krouzek/` |  |
| `/?cat=18` | Kroužek robotiky | 2 | `/aktuality/krouzek-robotiky/` |  |
| `/?cat=33` | Kroužky | 2 | `/aktuality/krouzky/` |  |
| `/?cat=1` | Nezařazené | 259 | `/aktuality/nezarazene/` | Shown as **Ze školy** (WordPress default name "Nezařazené"); confirm the label. |
| `/?cat=7` | Ost | 60 | `/aktuality/ost/` | Name on the old site is **"Ost"**; shown as "Ostatní". Confirm. |
| `/?cat=39` | Truhlářský kroužek | 1 | `/aktuality/truhlarsky-krouzek/` |  |
| `/?cat=20` | Úspěchy | 30 | `/aktuality/uspechy/` |  |
| `/?cat=75` | Vaření | 0 | `/aktuality/` | Empty; no page. |
| `/?cat=62` | Výlety a akce | 42 | `/aktuality/vylety-a-akce/` |  |
| `/?cat=50` | Výtvarný kroužek | 0 | `/aktuality/` | Empty; no page. |

## News by year

| Year | Posts |
|---|---|
| 2017 | 2 |
| 2018 | 1 |
| 2019 | 1 |
| 2020 | 24 |
| 2021 | 70 |
| 2022 | 57 |
| 2023 | 58 |
| 2024 | 86 |
| 2025 | 90 |
| 2026 | 47 |

## Other content of the old site

| Item | Where it is now |
|---|---|
| Sidebar "Zřizovatel školy" (old Order logo linking to maltezskyrad.cz) | Founder link in the top bar, identity band, footer and home facts. The old logo bitmap is **not** reused (emblem guidelines). |
| Footer "Partneři školy" (Spolek ZŠMR banner → Facebook) | Footer identity block: "Partner školy: Spolek ZŠMR". |
| Footer "Realizované projekty" (PPUč, ESIF/OP VVV, OP VK, Kladno, Šablony III and two OP JAK posters) | Footer "Realizované projekty", same images and links (publicity obligation). |
| Footer "Najdete nás" (address) | Footer identity block and contact card. |
| Mini events calendar widget (sidebar) | Dropped: the plugin held no events. See `/kalendar/`. |
| Creative Commons BY-SA 4.0 licence line | Kept in the footer. |
| RSS (`/?feed=rss2`) | `/feed.xml` (redirected). |
| Comments | None were published on the old site's posts; not carried over. |

## Flagged content (needs a decision, not invented)

1. **Calendar**: the events-calendar plugin had no events. `/kalendar/` links to the school-year dates document instead. Decide whether to keep a calendar at all.
2. **Domain**: the contact page says www.zsmr.cz; the site runs at www.zsmr.eu with a broken HTTPS certificate. Choose one canonical domain.
3. **Accessibility statement** (`/prohlaseni-o-pristupnosti/`): describes WordPress; rewrite for the new site (`docs/qa-report.md` has the test results).
4. **Dated notices** (consultations 2024 and 2025, school-council elections 2024): still published as pages; move to news or retire.
5. **Category labels** "Nezařazené" and "Ost": shown as "Ze školy" and "Ostatní".
6. **Imported texts** are unchanged and marked `existing` in preview builds; staff abbreviations (e.g. "SalA", "Abs33") in *Přehled tříd* and *Pedagogové* are kept as published.
7. **Photographs of pupils**: carried over from the current site; confirm that parental consent covers the new site.
8. **Outside WordPress:** the first-grade enrolment booking app (`/php/zapis/register_child.php`, PHP with a database of time slots) and large videos (`/large-files/DCS_ZS-Maltezska-Kladno.mp4` 561 MB, `/videa/…`, a 55 MB herbarium ODT) are linked at the old server, not copied. See `docs/deployment.md`.
9. **Missing on the old server:** `2025/04/IMG_20250402_140630_5-1-1024x512.jpg`, `2022/06/maly-1024x697.jpg` (404); dropped from their articles.
10. **Timetables (`/rozvrh/`):** on the old site the ".pdf" labels were split into fragments that pointed partly to the 2023/24 and 2025 timetables. Each row is now one link to the 2026/27 file. Typos "jednotlicých učiteů" are left as published.
11. **Dead download:** the ODT of "Převzetí odpovědnosti o polední pauze" pointed to the former domain zsmaltezskychrytiru.cz (no longer resolves; also 404 on zsmr.eu). The link is removed; the PDF stays. Ask the school for the ODT.
12. **GDPR page** names `skola@zsmaltezskychrytiru.cz` as the filing address; the rest of the site uses `skola@zsmr.cz`. Confirm which one receives mail.
13. **Empty gallery blocks** in 4 articles (2024/09/10, 2025/02/21, 2025/08/28, 2025/11/03) were empty on the old site too; they are hidden. The articles' other photos are intact.
14. **Typos in imported texts** (flagged, not edited): "psycholpga", "1.- 3.", "třídy ,", "rytířů .", "„ Kaleidoskop".
