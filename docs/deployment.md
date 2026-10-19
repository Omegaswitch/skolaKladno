# Deployment

Same hosting as maltezskyrad.cz: **Vercel**, project root = this repository, branch `main`.

- Build command `python3 build.py --production`, output `dist/` (both set in `vercel.json`). Python 3 is available in Vercel's build image; nothing is installed.
- `api/news.js` and `api/trust.js` run as Vercel Node functions. Set the environment variables listed in `README.md`, then redeploy.
- Security headers (CSP without third-party origins, HSTS, `nosniff`, `frame-ancestors 'none'`), cache headers and **all legacy redirects** are in `vercel.json`. The build also writes `dist/_headers` and `dist/_redirects` for Netlify-style hosts; `python3 build.py serve` applies both locally.

## Domain

The site answers today on **www.zsmr.eu** (HTTP; its HTTPS certificate chain is broken) and the contact page also gives **www.zsmr.cz**. Point both domains at Vercel. Vercel issues the certificates, which fixes HTTPS. Make `www.zsmr.eu` canonical (`baseUrl` in `content/site.json`) and redirect the others to it in the Vercel domain settings.

## Launch checklist

1. Approvals in `docs/brand-compliance.md` and `docs/logo.md`.
2. Environment variables set; publish a test article at `/pridat-aktualitu/` and delete it again.
3. Send a test message through the Schránka důvěry and confirm it arrives at `skola@zsmr.cz`.
4. **Before switching DNS:** the enrolment booking app (`/php/zapis/`, PHP + database) and the large videos (`/large-files/`, `/videa/`) are not part of this site and stay on the old server. Give that server its own hostname (e.g. `stary.zsmr.eu`) and replace `http://www.zsmr.eu/php/`, `/large-files/` and `/videa/` links (`grep -rl "www.zsmr.eu/" content`), or rebuild the booking app.
5. Switch DNS. Then open a few old addresses (`/?p=7347`, `/?page_id=143`, `/?cat=17`, `/wp-content/uploads/2024/09/RadSD_20240501.pdf`) and check that each lands on its new page.
6. Submit `https://www.zsmr.eu/sitemap.xml` in Google Search Console.
7. Keep the old WordPress installation offline but archived for a year.

## Size

`static/media` is about 0.9 GB, so the repository history is about 2 GB. Check the Vercel plan's deployment limits before launch. If needed, move the 19 videos to YouTube (school channel) or Vercel Blob first.
