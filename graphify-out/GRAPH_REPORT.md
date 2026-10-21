# Graph Report - skolakladno  (2026-10-21)

## Corpus Check
- 33 files · ~25,193,831 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 43 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 1170 nodes · 3084 edges · 53 communities (41 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 89 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e506fe53`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Publishing (news, events, notices, galleries)
- a
- n
- i
- m
- import_wp.py
- .remove
- news-editor.js
- quill.js
- Rt
- re
- Sanitiser
- .push
- w
- build.py
- .add
- jt
- trust.js
- Module
- vercel.json
- zsmr.eu
- School logo: Základní škola Maltézských rytířů
- Design system: zsmr.eu
- make_logo.py
- CLAUDE.md
- Product
- _
- s
- page.py
- Content inventory and migration map
- o
- optimize_media.py
- Deployment
- .forEach
- de
- render
- Brand compliance report
- site.local.py
- QA report — 19 October 2026
- r
- c
- p
- .slice
- o
- .mcp.json
- img
- layout
- serve
- Media
- page_body
- R

## God Nodes (most connected - your core abstractions)
1. `de` - 67 edges
2. `_` - 66 edges
3. `i` - 64 edges
4. `Module()` - 51 edges
5. `m` - 51 edges
6. `length()` - 51 edges
7. `h()` - 48 edges
8. `o` - 47 edges
9. `s` - 45 edges
10. `n` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Schema (for reference)` --references--> `events()`  [INFERRED]
  docs/publishing.md → api/page.py
- `Schema (for reference)` --references--> `categories()`  [INFERRED]
  docs/publishing.md → static/js/news-editor.js
- `Schema (for reference)` --references--> `image()`  [INFERRED]
  docs/publishing.md → static/js/vendor/quill-2.0.3/quill.js
- `resolves()` --calls--> `is_dynamic()`  [INFERRED]
  check.py → api/page.py
- `render_event()` --indirect_call--> `build()`  [INFERRED]
  api/page.py → build.py

## Import Cycles
- None detected.

## Communities (53 total, 12 thin omitted)

### Community 0 - "Publishing (news, events, notices, galleries)"
Cohesion: 0.17
Nodes (8): Accounts, sign-in, roles, Publishing (news, events, notices, galleries), Running it locally, Schema (for reference), Security, What can be published, image(), k

### Community 1 - "a"
Cohesion: 0.06
Nodes (7): a, delete(), insert(), k, update(), upsert(), x()

### Community 3 - "i"
Cohesion: 0.05
Nodes (3): getText(), i, l()

### Community 4 - "m"
Cohesion: 0.11
Nodes (5): d(), g(), getHTML(), length(), m

### Community 5 - "import_wp.py"
Cohesion: 0.20
Nodes (13): get_all(), get_json(), _get_json(), lead_image(), legacy_map(), main(), make_url_map(), post_url() (+5 more)

### Community 6 - ".remove"
Cohesion: 0.17
Nodes (17): appendChild(), clone(), deleteAt(), enforceAllowedChildren(), format(), formatAt(), insertAt(), insertBefore() (+9 more)

### Community 7 - "news-editor.js"
Cohesion: 0.10
Nodes (47): addCategory(), afterSignIn(), askCode(), attachmentRow(), categories(), clearPhoto(), dateHint(), del() (+39 more)

### Community 8 - "quill.js"
Cohesion: 0.08
Nodes (32): attach(), build(), clean(), close(), constructor(), create(), detach(), emit() (+24 more)

### Community 10 - "re"
Cohesion: 0.20
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "Sanitiser"
Cohesion: 0.20
Nodes (4): _iframe_label(), url_map(), sanitise(), Sanitiser

### Community 12 - ".push"
Cohesion: 0.09
Nodes (9): E(), h(), hasNext(), N, peek(), peekLength(), peekType(), rest() (+1 more)

### Community 13 - "w"
Cohesion: 0.20
Nodes (4): i(), g, w(), y

### Community 14 - "build.py"
Cohesion: 0.15
Nodes (20): breadcrumbs(), contact_card(), crumbs_html(), _descendants(), event_slug(), events_list(), events_page_html(), home_events_band() (+12 more)

### Community 15 - ".add"
Cohesion: 0.15
Nodes (11): attachUI(), buildItem(), buildLabel(), buildOptions(), buildPicker(), link(), Lt(), position() (+3 more)

### Community 16 - "jt"
Cohesion: 0.10
Nodes (21): Bt(), Ct(), Dt(), formula(), Ft(), Gt(), hide(), It() (+13 more)

### Community 17 - "trust.js"
Cohesion: 0.20
Nodes (4): recent, assert, call(), handler

### Community 18 - "Module"
Cohesion: 0.06
Nodes (31): Module(), a(), Aa(), bb(), c(), cc(), a(), d() (+23 more)

### Community 19 - "vercel.json"
Cohesion: 0.13
Nodes (14): excludeFiles, includeFiles, buildCommand, cleanUrls, framework, functions, api/page.py, headers (+6 more)

### Community 20 - "zsmr.eu"
Cohesion: 0.22
Nodes (8): Commands, Documentation, Editorial workflow, Security notes, Settings in Vercel (Project → Settings → Environment Variables), Shared code, Where things are, zsmr.eu

### Community 21 - "School logo: Základní škola Maltézských rytířů"
Cohesion: 0.33
Nodes (5): Approvals and open points, Basis, Files (`static/img/logo/`), Rules, School logo: Základní škola Maltézských rytířů

### Community 22 - "Design system: zsmr.eu"
Cohesion: 0.40
Nodes (4): Added components, Design system: zsmr.eu, Rules kept, What changes, and why

### Community 23 - "make_logo.py"
Cohesion: 0.16
Nodes (9): photos_of(), compact(), lockup(), main(), mark(), shield(), text_path(), vos_lockup() (+1 more)

### Community 27 - "Product"
Cohesion: 0.17
Nodes (11): Accessibility & Inclusion, Brand Commitments, Capabilities and Constraints, Operating Context, Platform, Positioning, Product, Product Principles (+3 more)

### Community 28 - "_"
Cohesion: 0.08
Nodes (10): _, E(), ee(), _handleTokenChanged(), _initRealtimeClient(), _initSupabaseAuthClient(), _listenForAuthEvents(), ne() (+2 more)

### Community 29 - "s"
Cohesion: 0.09
Nodes (7): getRange(), index(), normalizedToRange(), normalizeNative(), offset(), register(), s

### Community 30 - "page.py"
Cohesion: 0.17
Nodes (14): as_event(), as_news(), cached(), events(), file_info(), full_posts(), human_size(), media_src() (+6 more)

### Community 31 - "Content inventory and migration map"
Cohesion: 0.25
Nodes (7): Categories, Content inventory and migration map, Flagged content (needs a decision, not invented), News by year, Other content of the old site, Pages, Totals

### Community 32 - "o"
Cohesion: 0.17
Nodes (16): A(), applyDelta(), deleteText(), formatText(), getDelta(), handler(), i(), insertContents() (+8 more)

### Community 34 - "Deployment"
Cohesion: 0.40
Nodes (4): Deployment, Domain, Launch checklist, Size

### Community 35 - ".forEach"
Cohesion: 0.10
Nodes (13): attribute(), b(), copy(), descendant(), descendants(), Et(), f, find() (+5 more)

### Community 36 - "de"
Cohesion: 0.06
Nodes (10): Q(), d(), de, h(), j, m, re(), se (+2 more)

### Community 37 - "render"
Cohesion: 0.11
Nodes (17): dynamic_pages(), handler, is_dynamic(), listing(), not_found(), render(), render_event(), build() (+9 more)

### Community 40 - "QA report — 19 October 2026"
Cohesion: 0.25
Nodes (7): Cross-device audit and publishing workflow (21 October 2026), Fixed during QA, Not verified here (needs the live environment), Pre-presentation audit — 19 October 2026 (second round), QA report — 19 October 2026, Results, Shared Supabase database (21 October 2026)

### Community 41 - "r"
Cohesion: 0.18
Nodes (9): ae, C(), n(), r(), ce, i, le(), then() (+1 more)

### Community 43 - "p"
Cohesion: 0.16
Nodes (8): b, f, l, p, S, T(), u, v()

### Community 44 - ".slice"
Cohesion: 0.13
Nodes (5): add(), formatLine(), u, value(), X

### Community 47 - "img"
Cohesion: 0.24
Nodes (7): enhance_body(), fix_img(), fmt_date(), image_size(), img(), news_card(), render_article()

### Community 48 - "layout"
Cohesion: 0.20
Nodes (6): layout(), logo(), logo_viewbox(), nav_html(), pinned_html(), render_news_editor()

### Community 49 - "serve"
Cohesion: 0.67
Nodes (4): serve(), do_GET(), end_headers(), guess_type()

### Community 50 - "Media"
Cohesion: 0.31
Nodes (4): download(), Media, _norm(), retry()

### Community 51 - "page_body"
Cohesion: 0.47
Nodes (5): gallery_html(), gallery_posts(), page_body(), photos_of(), render_gallery()

## Knowledge Gaps
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Schema (for reference)` connect `Publishing (news, events, notices, galleries)` to `page.py`, `news-editor.js`?**
  _High betweenness centrality (0.336) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `a` be split into smaller, more focused modules?**
  _Cohesion score 0.05895061728395062 - nodes in this community are weakly interconnected._
- **Why does `image()` connect `Publishing (news, events, notices, galleries)` to `quill.js`, `.add`?**
  _High betweenness centrality (0.316) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Module()` (e.g. with `ac()` and `$b()`) actually correct?**
  _`Module()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `n` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._
- **Why does `_` connect `_` to `a`, `n`, `.forEach`, `de`, `r`, `p`, `w`, `o`?**
  _High betweenness centrality (0.261) - this node is a cross-community bridge._