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
