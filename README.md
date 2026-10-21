# zsmr.eu

Website of **Základní škola Maltézských rytířů** (Kladno – Kročehlavy), a Christian primary school founded by the Sovereign Order of Malta – Czech Grand Priory (Suverénní řád maltézských rytířů – České velkopřevorství).

It is built exactly like [maltezskyrad.cz](https://github.com/Omegaswitch/maltezskyrad): a Python script (standard library only) turns the files in `content/` into plain HTML in `dist/`. There is no CMS, no database and nothing to install. Staff publish news in the browser at `/pridat-aktualitu/`.

## Commands

```sh
python3 build.py serve 8000      # preview build, served at http://localhost:8000 with headers and legacy redirects applied
python3 build.py                 # preview build into dist/ (noindex, content-status labels shown)
python3 build.py --production    # production build
python3 check.py                 # checks dist/: links, headings, descriptions, brand assets, acronym
python3 tests/site.local.py       # dist/ plus the pages rendered from the shared database
node tests/trust.test.js         # Schránka důvěry API (e-mail stubbed)
```

## Where things are

| Path | What |
|---|---|
| `content/pages/<url>/index.html` | Pages. JSON front matter between `---` lines, then HTML. |
| `content/site.json` | Names, contacts, menu, news categories, footer project logos.; `supabase` (project address, publishable key, this site's id) |
| `content/legacy.json` | Every old `?p=`, `?page_id=` and `?cat=` address and its new URL. |
| `vercel.json` | Hosting, security headers and the permanent redirects for all old addresses (generated from `legacy.json` by `tools/import_wp.py --redirects`). |
| `api/page.py` | Renders news, events, galleries, feeds and the home page on request from the shared Supabase database, with the functions of `build.py`. |
| `api/trust.js` | Schránka důvěry: sends the form to the school by e-mail. |
| `static/img/logo/` | School logo set; see `docs/logo.md`. |
| `static/media/` | Migrated photos and documents (images reduced to ≤ 1024 px). |
| `tools/import_wp.py` | Importer from the old WordPress site. Never overwrites a file marked `"imported": false`. |
| `tools/make_logo.py` | Generates the logo SVGs. |
| `tools/make_og.py` | Builds `static/img/og.jpg`, the 1200×630 link-preview card (Discord, iMessage, Facebook): the Order's flag under a dark veil, the school lockup in white, a red strip. Same layout on all three school sites. |

## Editorial workflow

**News, events, notices and galleries (no GitHub needed).** Staff publish at `/pridat-aktualitu/` (not linked, not indexed): e-mail, password and a one-time code from an authenticator app. Posts, events and photos go to the shared Supabase database of the three school sites and are on the web within a minute; `api/page.py` renders those pages on request with this site's own functions. Drafts, scheduled posts, pinned notices, roles and user management are described in `docs/publishing.md`.

**Pages.** Edit the file in `content/pages/`. Set `"imported": false` so a re-import never overwrites it, and remove `"status"` once the text is approved (`existing` = carried over, `new` = new text, `approval` = needs sign-off; shown only in preview builds).

**Contacts and menu.** Edit `content/site.json`.

**Documents (PDF, ODT).** Put the file in `static/media/YYYY/MM/` and link it from the page as `<p class="file"><a href="/media/…">Name</a> (PDF)</p>`.

## Settings in Vercel (Project → Settings → Environment Variables)

| Variable | Value |
|---|---|
| `RESEND_API_KEY` | Resend key; needed by the Schránka důvěry |
| `TRUST_TO` | who receives Schránka důvěry messages (default `skola@zsmr.cz`) |
| `MAIL_FROM` | sender on a domain verified in Resend, e.g. `Škola <web@zsmr.eu>` |

## Documentation

- `DESIGN.md`: how this site varies the shared design system.
- `docs/logo.md`: school logo, files and usage rules, approvals needed.
- `docs/content-inventory.md`: the old site's pages, the migration map and the open content questions.
- `docs/brand-compliance.md`: checklist against the Order's communications policy and emblem guidelines.
- `docs/deployment.md`: build, hosting, domain, launch checklist.
- `docs/qa-report.md`: what was tested and the results.

## Shared code

`api/page.py`, `static/js/news-editor.js`, `static/js/pdf-worker.js`, `static/js/head.js`, the menu and image code in `static/js/site.js`, the frame in `static/css/site.css` and the sanitiser in `tools/import_wp.py` are shared with maltezskyrad.cz and the other Order school sites (skolaKladno, skolaPraha, skolaSkutec). Change them in one place and copy the file to the others; do not fork them.

## Security notes

- Headers (`vercel.json`): CSP with no third-party origins and no inline styles or scripts (`'wasm-unsafe-eval'` only lets WebAssembly compile, for the PDF shrinking), HSTS, `nosniff`, `frame-ancestors 'none'`, Referrer-Policy, Permissions-Policy. `check.py` fails the build on any inline `style` attribute.
- Publishing: Supabase Auth with a mandatory second factor; row level security decides who may read or change what (see `docs/publishing.md`); the pages hold only the publishable key; `api/page.py` rebuilds every post text from a tag allowlist before it is shown.
- Quill 2.0.3 (`static/js/vendor/`): CVE-2025-15056 (XSS through its HTML export, no patched release yet). Not exploitable here: the editor's HTML is never rendered unsanitised; `api/page.py` rebuilds it from the allowlist before it reaches any page.
- Ghostscript 10.06.0 as WebAssembly (`static/js/vendor/ghostscript-1.1.0/`): runs only in the staff member's own browser, in a worker that is dropped after one file. Update by replacing the folder with a newer `@okathira/ghostpdl-wasm` build.

