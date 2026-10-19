# zsmr.eu

Website of **Základní škola Maltézských rytířů** (Kladno – Kročehlavy), a Christian primary school founded by the Sovereign Order of Malta – Czech Grand Priory (Suverénní řád maltézských rytířů – České velkopřevorství).

It is built exactly like [maltezskyrad.cz](https://github.com/Omegaswitch/maltezskyrad): a Python script (standard library only) turns the files in `content/` into plain HTML in `dist/`. There is no CMS, no database and nothing to install. Staff publish news in the browser at `/pridat-aktualitu/`.

## Commands

```sh
python3 build.py serve 8000      # preview build, served at http://localhost:8000 with headers and legacy redirects applied
python3 build.py                 # preview build into dist/ (noindex, content-status labels shown)
python3 build.py --production    # production build
python3 check.py                 # checks dist/: links, headings, descriptions, brand assets, acronym
node tests/news.test.js          # news editor API (GitHub stubbed)
node tests/trust.test.js         # Schránka důvěry API (e-mail stubbed)
```

## Where things are

| Path | What |
|---|---|
| `content/pages/<url>/index.html` | Pages. JSON front matter between `---` lines, then HTML. |
| `content/news/YYYY/MM/DD/slug.html` | News (436 posts imported from 2017 to today). |
| `content/site.json` | Names, contacts, menu, news categories, footer project logos. |
| `content/legacy.json` | Every old `?p=`, `?page_id=` and `?cat=` address and its new URL. |
| `vercel.json` | Hosting, security headers and the permanent redirects for all old addresses (generated from `legacy.json` by `tools/import_wp.py --redirects`). |
| `api/news.js` | News publishing (same code as maltezskyrad.cz). |
| `api/trust.js` | Schránka důvěry: sends the form to the school by e-mail. |
| `static/img/logo/` | School logo set; see `docs/logo.md`. |
| `static/media/` | Migrated photos and documents (images reduced to ≤ 1024 px). |
| `tools/import_wp.py` | Importer from the old WordPress site. Never overwrites a file marked `"imported": false`. |
| `tools/make_logo.py` | Generates the logo SVGs. |

## Editorial workflow

**News (no GitHub needed).** Go to `/pridat-aktualitu/` (not linked, not indexed), sign in, write the article, choose categories (class, družina, kroužek …), add a main photo and attachments, publish. Several photos can be inserted into the text at once; two or more in a row appear as a photo grid. PDFs over 1 MB are shrunk in the browser by Ghostscript compiled to WebAssembly (`static/js/pdf-worker.js`, `static/js/vendor/ghostscript-1.1.0/`, AGPL: licence and source links in that folder, offered on the staff page), loaded only when such a PDF is attached. The site rebuilds and the article is online in about a minute. The **Upravit nebo smazat** tab edits or deletes any article, including the imported ones. Photos are shrunk in the browser and stripped of location data.

**Pages.** Edit the file in `content/pages/`. Set `"imported": false` so a re-import never overwrites it, and remove `"status"` once the text is approved (`existing` = carried over, `new` = new text, `approval` = needs sign-off; shown only in preview builds).

**Contacts and menu.** Edit `content/site.json`.

**Documents (PDF, ODT).** Put the file in `static/media/YYYY/MM/` and link it from the page as `<p class="file"><a href="/media/…">Name</a> (PDF)</p>`.

## Settings in Vercel (Project → Settings → Environment Variables)

| Variable | Value |
|---|---|
| `NEWS_USERS` | one `Name:password` per line, one per teacher who publishes |
| `NEWS_SECRET` | long random string (`openssl rand -base64 32`) |
| `GITHUB_TOKEN` | fine-grained token for `Omegaswitch/skolaKladno` only, Contents: read and write |
| `RESEND_API_KEY` | Resend key; needed by the Schránka důvěry (and optional news notices) |
| `TRUST_TO` | who receives Schránka důvěry messages (default `skola@zsmr.cz`) |
| `MAIL_FROM` | sender on a domain verified in Resend, e.g. `Škola <web@zsmr.eu>` |
| `NEWS_NOTIFY` | optional: who is e-mailed about every new article |

## Documentation

- `DESIGN.md`: how this site varies the shared design system.
- `docs/logo.md`: school logo, files and usage rules, approvals needed.
- `docs/content-inventory.md`: the old site's pages, the migration map and the open content questions.
- `docs/brand-compliance.md`: checklist against the Order's communications policy and emblem guidelines.
- `docs/deployment.md`: build, hosting, domain, launch checklist.
- `docs/qa-report.md`: what was tested and the results.

## Shared code

`api/news.js`, `static/js/news-editor.js`, `static/js/pdf-worker.js`, `static/js/head.js`, the menu and image code in `static/js/site.js`, the frame in `static/css/site.css` and the sanitiser in `tools/import_wp.py` are shared with maltezskyrad.cz and the other Order school sites (skolaKladno, skolaPraha, skolaSkutec). Change them in one place and copy the file to the others; do not fork them.

## Security notes

- Headers (`vercel.json`): CSP with no third-party origins and no inline styles or scripts (`'wasm-unsafe-eval'` only lets WebAssembly compile, for the PDF shrinking), HSTS, `nosniff`, `frame-ancestors 'none'`, Referrer-Policy, Permissions-Policy. `check.py` fails the build on any inline `style` attribute.
- `api/news.js`: passwords compared in constant time, signed `HttpOnly; Secure; SameSite=Strict` session cookie scoped to the API path, same-origin check on every POST, sign-in throttling per function instance, uploads checked by content and renamed, text rebuilt from a tag allowlist. The GitHub token must be fine-grained to this repository only (Contents: read and write).
- Quill 2.0.3 (`static/js/vendor/`): CVE-2025-15056 (XSS through its HTML export, no patched release yet). Not exploitable here: the editor's HTML is never rendered unsanitised; the server rebuilds it from the allowlist before it reaches any page.
- Ghostscript 10.06.0 as WebAssembly (`static/js/vendor/ghostscript-1.1.0/`): runs only in the staff member's own browser, in a worker that is dropped after one file. Update by replacing the folder with a newer `@okathira/ghostpdl-wasm` build.

