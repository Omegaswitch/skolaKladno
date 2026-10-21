# Graph Report - skolakladno  (2026-10-21)

## Corpus Check
- 33 files · ~25,193,759 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 43 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 1169 nodes · 3081 edges · 50 communities (38 shown, 12 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 89 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `49b303d5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- b
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
- length
- .push
- w
- build.py
- z
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
- N
- QA report — 19 October 2026
- r
- c
- p
- .slice
- o
- .mcp.json
- img
- logo
- serve

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
- `listing()` --indirect_call--> `build()`  [INFERRED]
  api/page.py → build.py

## Import Cycles
- None detected.

## Communities (50 total, 12 thin omitted)

### Community 0 - "b"
Cohesion: 0.17
Nodes (11): attribute(), b(), build(), getDelta(), e(), insertContents(), p(), update() (+3 more)

### Community 1 - "a"
Cohesion: 0.05
Nodes (9): a, b, delete(), insert(), k, R(), update(), upsert() (+1 more)

### Community 4 - "m"
Cohesion: 0.05
Nodes (6): attachUI(), g(), m, q(), R(), X

### Community 5 - "import_wp.py"
Cohesion: 0.09
Nodes (21): download(), get_all(), get_json(), _get_json(), _iframe_label(), lead_image(), legacy_map(), main() (+13 more)

### Community 6 - ".remove"
Cohesion: 0.19
Nodes (12): deleteAt(), enforceAllowedChildren(), format(), formatAt(), formatLine(), formatText(), isolate(), moveChildren() (+4 more)

### Community 7 - "news-editor.js"
Cohesion: 0.08
Nodes (54): Accounts, sign-in, roles, Publishing (news, events, notices, galleries), Running it locally, Schema (for reference), Security, What can be published, addCategory(), afterSignIn() (+46 more)

### Community 8 - "quill.js"
Cohesion: 0.08
Nodes (36): A(), attach(), buildItem(), buildLabel(), buildOptions(), buildPicker(), close(), constructor() (+28 more)

### Community 10 - "re"
Cohesion: 0.11
Nodes (5): main(), Page, redirect_sources(), resolves(), Handler

### Community 11 - "length"
Cohesion: 0.19
Nodes (14): appendChild(), clone(), d(), formats(), getBounds(), getHTML(), handler(), insertAt() (+6 more)

### Community 12 - ".push"
Cohesion: 0.15
Nodes (8): getFormat(), h(), hasNext(), path(), peek(), peekLength(), peekType(), rest()

### Community 13 - "w"
Cohesion: 0.20
Nodes (4): i(), g, w(), y

### Community 14 - "build.py"
Cohesion: 0.10
Nodes (32): breadcrumbs(), contact_card(), crumbs_html(), _descendants(), event_slug(), events_list(), events_page_html(), gallery_html() (+24 more)

### Community 15 - "z"
Cohesion: 0.20
Nodes (3): create(), nt(), z()

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
Cohesion: 0.14
Nodes (13): includeFiles, buildCommand, cleanUrls, framework, functions, api/page.py, headers, installCommand (+5 more)

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
Cohesion: 0.18
Nodes (8): compact(), lockup(), main(), mark(), shield(), text_path(), vos_lockup(), vos_text()

### Community 27 - "Product"
Cohesion: 0.17
Nodes (11): Accessibility & Inclusion, Brand Commitments, Capabilities and Constraints, Operating Context, Platform, Positioning, Product, Product Principles (+3 more)

### Community 28 - "_"
Cohesion: 0.09
Nodes (9): _, E(), ee(), _handleTokenChanged(), _initRealtimeClient(), _initSupabaseAuthClient(), _listenForAuthEvents(), ne() (+1 more)

### Community 29 - "s"
Cohesion: 0.10
Nodes (4): k, normalizeNative(), register(), s

### Community 30 - "page.py"
Cohesion: 0.15
Nodes (16): as_event(), as_news(), cached(), events(), file_info(), full_posts(), human_size(), listing() (+8 more)

### Community 31 - "Content inventory and migration map"
Cohesion: 0.25
Nodes (7): Categories, Content inventory and migration map, Flagged content (needs a decision, not invented), News by year, Other content of the old site, Pages, Totals

### Community 32 - "o"
Cohesion: 0.19
Nodes (7): applyDelta(), deleteText(), insertEmbed(), insertText(), o, removeFormat(), wrap()

### Community 34 - "Deployment"
Cohesion: 0.40
Nodes (4): Deployment, Domain, Launch checklist, Size

### Community 35 - ".forEach"
Cohesion: 0.17
Nodes (7): clean(), copy(), descendant(), descendants(), Et(), f, move()

### Community 36 - "de"
Cohesion: 0.06
Nodes (10): Q(), d(), de, h(), j, m, re(), se (+2 more)

### Community 37 - "render"
Cohesion: 0.13
Nodes (13): dynamic_pages(), handler, is_dynamic(), not_found(), render(), render_event(), build(), event_when() (+5 more)

### Community 39 - "N"
Cohesion: 0.15
Nodes (3): E(), N, w()

### Community 40 - "QA report — 19 October 2026"
Cohesion: 0.25
Nodes (7): Cross-device audit and publishing workflow (21 October 2026), Fixed during QA, Not verified here (needs the live environment), Pre-presentation audit — 19 October 2026 (second round), QA report — 19 October 2026, Results, Shared Supabase database (21 October 2026)

### Community 41 - "r"
Cohesion: 0.18
Nodes (9): ae, C(), n(), r(), ce, i, le(), then() (+1 more)

### Community 43 - "p"
Cohesion: 0.21
Nodes (7): f, l, p, S, T(), u, v()

### Community 44 - ".slice"
Cohesion: 0.18
Nodes (7): add(), detach(), keys(), remove(), removeChild(), u, value()

### Community 47 - "img"
Cohesion: 0.24
Nodes (7): enhance_body(), fix_img(), fmt_date(), image_size(), img(), news_card(), render_article()

### Community 49 - "serve"
Cohesion: 0.67
Nodes (4): serve(), do_GET(), end_headers(), guess_type()

## Knowledge Gaps
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Schema (for reference)` connect `news-editor.js` to `page.py`?**
  _High betweenness centrality (0.336) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `a` be split into smaller, more focused modules?**
  _Cohesion score 0.05417236662106703 - nodes in this community are weakly interconnected._
- **Why does `image()` connect `news-editor.js` to `quill.js`, `s`?**
  _High betweenness centrality (0.316) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Module()` (e.g. with `ac()` and `$b()`) actually correct?**
  _`Module()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `n` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._
- **Why does `_` connect `_` to `b`, `a`, `n`, `de`, `r`, `p`, `w`, `o`?**
  _High betweenness centrality (0.261) - this node is a cross-community bridge._