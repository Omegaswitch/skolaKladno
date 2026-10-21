# QA report — 19 October 2026

Everything below was run against the built site (`python3 build.py serve`, Chromium via Playwright), not inferred from code.

## Results

| Area | Test | Result |
|---|---|---|
| Build | `python3 build.py` and `--production` | ✅ 21 pages, 436 articles, 515 HTML files |
| Links, headings, metadata | `python3 check.py`: every internal link and image resolves, one `<h1>` per page, a title and description on every page, only approved brand files, no forbidden acronym | ✅ 0 problems on 515 pages |
| Legacy URLs | All 473 old `?p=` / `?page_id=` / `?cat=` addresses requested: each must answer 301 to its mapped URL, and that URL must load | ✅ 473/473 |
| Other legacy forms | `/index.php?p=`, `?page_id=232/` (with slash), `?paged=`, `?author=`, `?feed=rss2`, `/wp-content/uploads/…` | ✅ all 301 to a live page or file |
| Unknown URL | `/neexistuje/` | ✅ 404 with the site's own error page |
| Accessibility | axe-core 4.10, WCAG 2.0/2.1/2.2 A + AA rules, **all 513 sitemap pages** at 390 px and 40 at 1280 px | ✅ 0 violations (after fixes below) |
| Mobile layout | horizontal overflow on all 513 pages at 360 px and 390 px | ✅ none |
| Contrast | muted text (dates, labels, footer) against white and `#f3f3f3` | ✅ 5.75–6.39 : 1 |
| Keyboard | menu, submenus, class grid, form fields, button: visible focus ring, no traps | ✅ |
| JavaScript | console errors on key pages | ✅ none (only the expected 404 of `/api/news` on the local preview, which has no serverless functions) |
| News editor API | `node tests/news.test.js` (sign-in, publish, edit, delete, file checks, cross-site rejection; GitHub stubbed) | ✅ |
| Schránka důvěry API | `node tests/trust.test.js` (validation, HTML escaping, honeypot, rate limit, cross-site rejection; e-mail stubbed) | ✅ |
| Importer | `python3 tools/import_wp.py --check`: sanitiser, URL mapping, galleries, video handling | ✅ (also run by `check.py`) |
| Production build | no status labels, indexable, editor page `noindex`, `robots.txt` with sitemap | ✅ |
| Security headers | CSP `default-src 'self'` with no third-party origins, HSTS, `nosniff`, `frame-ancestors 'none'`, Referrer-Policy, Permissions-Policy (in `vercel.json`) | ✅ configured; to verify on the live host |

## Fixed during QA

- Photos linked to their own file had no accessible link name: the redundant links are removed and other image-only links labelled.
- Imported text full of non-breaking spaces widened articles past the phone screen: grid columns now `minmax(0,1fr)`. The same latent bug exists in maltezskyrad.cz.
- A redirect target with Cyrillic characters crashed the preview server and would have been fragile on Vercel: destinations are now percent-encoded.
- Design critique (Impeccable, two independent assessments; score 24/40 before fixes): families block moved before news, phone in the top bar on phones, long photo articles turned into linked photo grids, footer consistency, tap targets in the footer, focus ring on the red button.

## Not verified here (needs the live environment)

- The news editor and the Schránka důvěry against the real GitHub and Resend services (environment variables are not set in this repository).
- Deployment on Vercel itself; headers and redirects as served by Vercel; HTTPS on the final domain.
- **Deploy size:** `static/media` is about 0.9 GB (2,422 photos after recompression, plus 19 videos). Check it against the Vercel plan's limits before launch; if needed, move the videos to YouTube or Vercel Blob.
- The enrolment booking app (`/php/zapis/register_child.php`) and two large videos stay on the old server. **Before DNS moves to Vercel, give the old server its own hostname** (e.g. `stary.zsmr.eu`) and update `ORIGIN` links, or the links in those articles will break.
- Two images were already missing (404) on the old server; the articles show their other photos.

## Pre-presentation audit — 19 October 2026 (second round)

Two independent reviews (design review compared with maltezskyrad.cz and velkoprevorskypalac.eu; detector + motion + interaction QA), fixes, then an independent re-check by the same reviewers.

| | Before | After fixes |
|---|---|---|
| Visual quality | 74/100 | **84/100** |
| Functional quality | 86/100 | **94/100** |
| Nielsen heuristics | 28/40 | — |
| axe WCAG 2.2 AA | 1 violation (split link on /rozvrh/) | 0 on all 513 pages (390 px) and a sample at 1280 px |
| CLS (home, 1280 px) | 0.0061 | 0.0033 |
| Horizontal overflow (360, 390, 768, 1024 px) | none | none |

Fixed:
- **Logo:** rebuilt on the VOS pattern (official "MALTÉZSKÝ ŘÁD / ČESKÁ REPUBLIKA" lockup, rule and tick); header size raised to meet the logo's minimum width; deeper veil behind the red name.
- **Home:** thumbnails without grey bars; facts aligned; class numerals graphite.
- **Inner pages:** /pedagogove/ table readable; /skola/ one-line descriptions; clear download links that keep ".odt .pdf" pairs on one line.
- **Articles:** unified photo grids; empty gallery blocks hidden.
- **Footer:** six columns; ends on the red band; phone numbers never broken.
- **Archive:** tabs scroll on phones; pagination aligned; category breadcrumbs follow the menu.
- **Keyboard and motion:** closed mobile menu out of the tab order; Escape closes hover dropdowns and the mobile menu; cached images no longer re-fade; story images fade; consistent hover transitions.
- **Fonts:** Czech font subset preloaded.
- **Content:** /rozvrh/ links point to the 2026/27 timetables; a dead ODT link removed.

Detector: 56 "cramped-padding" / "flat-type-hierarchy" findings, all false positives (full-bleed bands padded by their inner `.wrap`; the detector does not apply CSS).

Remaining (minor or content):
- Project posters as small thumbnails.
- Identity-band text style differs slightly from the sister sites.
- Long desktop tab path through the open-on-focus menu (skip link provided).
- Typos in imported texts.
- The GDPR page's old e-mail domain.
- See `docs/content-inventory.md`.

## Cross-device audit and publishing workflow (21 October 2026)

Run with Playwright (Chromium) and axe-core 4.10 on the built site of all three school sites at six viewports
(phone 360 and 390 px, phone landscape 844 px, tablet 768 and 1024 px, desktop 1920 px): home, news listing, a post,
the main information page, contacts, the Grand Priory page, the editor.

| Check | Result |
|---|---|
| Horizontal overflow, layout | one bug across the sites: at 1024 px the hidden drop-down menus of the last items widened the page; fixed by right-aligning those menus (`.nav-list>li:nth-last-child(-n+3)>.sub`) |
| axe (WCAG 2 A/AA, 2.1, 2.2) | 0 violations at every viewport |
| Console errors, missing alt texts, one h1 | 0 |
| Sticky menu bar (added 20 Oct) | opens and scrolls correctly at every width; mobile menu limited to the viewport height |
| Small type and tap targets in the Grand Magistry frame (top bar, footer) | informational: the frame is the Order's prescribed template and was left as designed |

Publishing (see `docs/publishing.md`): roles (editor/admin), drafts, scheduled posts with a daily rebuild, pinned
notices, events and photo galleries were added to the shared editor and tested end to end in Chromium against the
local stand-in (`tests/news.local.js`): create with photo → draft → edit into a scheduled post → not built → admin pins a
notice → shown on the home page → event added, edited, deleted → post deleted → path traversal refused; 0 page errors.
`node tests/news.test.js`, `python3 build.py --production --offline` and `python3 check.py` pass.

Still needing authorisation: the Vercel environment variables (`NEWS_USERS`, `NEWS_SECRET`, `GITHUB_TOKEN`,
`DEPLOY_HOOK_URL`, `CRON_SECRET`) are not set on this project, so publishing is not live yet.

## Shared Supabase database (21 October 2026)

News, events, notices and galleries moved from files in the repository to the schools' shared Supabase project.
Verified:

| Check | Result |
|---|---|
| Row level security, run in SQL as anonymous, editor without second factor, editor with it (member of two sites), administrator | anonymous sees published posts only; no writes without the second factor; an editor writes only to their sites, edits only their own rows, cannot pin, cannot move a row to another site, cannot manage members; an administrator edits any row of their site, pins, lists and manages members, cannot touch another site or remove themselves |
| Auth REST: password sign-in, TOTP enrolment and verification, `aal2` claim, re-sign-in back to `aal1` | as designed |
| Storage: upload to own site folder, to another site's folder, without second factor, of an HTML file | 200 / refused / refused / refused (mime type) |
| Staff page in Chromium: administrator enrols the authenticator, publishes a pinned post with a photo, lists users; editor signs in with the code, sees no pin field or users tab, cannot delete or edit the administrator's post, saves a draft, adds, edits and deletes an event, deletes their own draft | all as designed, 0 page errors |
| Rendered pages from the database on the local stand-in: home (news band, pinned notice, events), listings, categories, years, pagination, posts (legacy and new, photo sizes), gallery, events page, event page, RSS, sitemap, search index, 404 | all rendered; axe 0 violations, no overflow, one h1, alt texts at 390/1024/1366 px |
| Output sanitiser on hostile text (script, event handlers, foreign image, javascript: link, iframe) | removed; legacy tables kept for imported (server-marked) posts |
| Supabase security advisors | one open item for the project owner: enable leaked-password protection (Authentication → Settings) |
| `python3 build.py --production --offline`, `python3 check.py` | pass |

Needs the project owner (Supabase dashboard): sign-ups off, Redirect URLs for the three domains, SMTP sender for
invitation and recovery mail (the built-in sender is limited to a few mails per hour), Czech e-mail templates,
leaked-password protection; then invite the real editors and remove the two test accounts.
