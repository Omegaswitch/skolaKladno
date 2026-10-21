# Graph Report - skolaKladno  (2026-10-21)

## Corpus Check
- 29 files · ~25,250,302 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 43 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 802 nodes · 2136 edges · 39 communities (28 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 42 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5b688329`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- length
- c
- news.js
- i
- .forEach
- import_wp.py
- build
- news-editor.js
- quill.js
- Rt
- re
- jt
- N
- .Cb
- build.py
- N
- E
- s
- Module
- vercel.json
- zsmr.eu
- School logo: Základní škola Maltézských rytířů
- Design system: zsmr.eu
- make_logo.py
- CLAUDE.md
- Product
- R
- w
- Content inventory and migration map
- Sanitiser
- logo_viewbox
- Deployment
- Media
- do_GET
- Brand compliance report
- QA report — 19 October 2026

## God Nodes (most connected - your core abstractions)
1. `i` - 63 edges
2. `Module()` - 51 edges
3. `m` - 51 edges
4. `length()` - 51 edges
5. `o` - 47 edges
6. `s` - 44 edges
7. `h()` - 35 edges
8. `b()` - 29 edges
9. `update()` - 28 edges
10. `jt()` - 27 edges

## Surprising Connections (you probably didn't know these)
- `ua()` --indirect_call--> `E()`  [INFERRED]
  static/js/vendor/ghostscript-1.1.0/gs.js → static/js/vendor/quill-2.0.3/quill.js
- `jt()` --indirect_call--> `P()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/ghostscript-1.1.0/gs.js
- `va()` --indirect_call--> `E()`  [INFERRED]
  static/js/vendor/ghostscript-1.1.0/gs.js → static/js/vendor/quill-2.0.3/quill.js

## Import Cycles
- None detected.

## Communities (39 total, 11 thin omitted)

### Community 0 - "length"
Cohesion: 0.05
Nodes (23): applyDelta(), d(), f, find(), g(), getHTML(), h(), handler() (+15 more)

### Community 2 - "news.js"
Cohesion: 0.06
Nodes (41): ALLOWED, CATEGORIES, commit(), crypto, editable(), env(), esc(), excerptOf() (+33 more)

### Community 3 - "i"
Cohesion: 0.06
Nodes (3): getText(), i, v()

### Community 4 - ".forEach"
Cohesion: 0.08
Nodes (11): b(), descendant(), descendants(), Et(), getFormat(), handleDOM(), e(), nt() (+3 more)

### Community 5 - "import_wp.py"
Cohesion: 0.20
Nodes (13): get_all(), get_json(), _get_json(), lead_image(), legacy_map(), main(), make_url_map(), post_url() (+5 more)

### Community 6 - "build"
Cohesion: 0.20
Nodes (9): build(), news_item(), paginate(), redirect_lines(), render_news_editor(), render_news_index(), rss(), short_date() (+1 more)

### Community 7 - "news-editor.js"
Cohesion: 0.15
Nodes (30): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), del(), drop(), edit() (+22 more)

### Community 8 - "quill.js"
Cohesion: 0.05
Nodes (74): A(), add(), appendChild(), attach(), attachUI(), attribute(), build(), buildItem() (+66 more)

### Community 10 - "re"
Cohesion: 0.18
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "jt"
Cohesion: 0.09
Nodes (20): Bt(), Ct(), formula(), Ft(), getBounds(), Gt(), hide(), jt() (+12 more)

### Community 13 - ".Cb"
Cohesion: 0.28
Nodes (8): c(), d(), I, jb(), kb(), lb(), mb(), qb()

### Community 14 - "build.py"
Cohesion: 0.13
Nodes (25): breadcrumbs(), contact_card(), crumbs_html(), _descendants(), enhance_body(), fix_img(), fmt_date(), image_size() (+17 more)

### Community 15 - "N"
Cohesion: 0.36
Nodes (9): hb(), ib(), M(), N(), O(), P(), Q(), rb() (+1 more)

### Community 16 - "E"
Cohesion: 0.33
Nodes (6): bb(), cc(), a(), ua(), va(), E()

### Community 17 - "s"
Cohesion: 0.08
Nodes (7): index(), k, normalizedToRange(), normalizeNative(), offset(), register(), s

### Community 18 - "Module"
Cohesion: 0.10
Nodes (11): Module(), a(), Aa(), eb(), fb(), R(), sa(), ub() (+3 more)

### Community 19 - "vercel.json"
Cohesion: 0.20
Nodes (9): buildCommand, cleanUrls, framework, headers, installCommand, outputDirectory, redirects, $schema (+1 more)

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
Cohesion: 0.10
Nodes (9): compact(), lockup(), main(), mark(), shield(), text_path(), vos_lockup(), vos_text() (+1 more)

### Community 27 - "Product"
Cohesion: 0.17
Nodes (11): Accessibility & Inclusion, Brand Commitments, Capabilities and Constraints, Operating Context, Platform, Positioning, Product, Product Principles (+3 more)

### Community 31 - "Content inventory and migration map"
Cohesion: 0.25
Nodes (7): Categories, Content inventory and migration map, Flagged content (needs a decision, not invented), News by year, Other content of the old site, Pages, Totals

### Community 32 - "Sanitiser"
Cohesion: 0.20
Nodes (4): _iframe_label(), url_map(), sanitise(), Sanitiser

### Community 34 - "Deployment"
Cohesion: 0.40
Nodes (4): Deployment, Domain, Launch checklist, Size

### Community 35 - "Media"
Cohesion: 0.31
Nodes (4): download(), Media, _norm(), retry()

### Community 37 - "do_GET"
Cohesion: 0.67
Nodes (4): serve(), do_GET(), end_headers(), guess_type()

### Community 40 - "QA report — 19 October 2026"
Cohesion: 0.33
Nodes (5): Fixed during QA, Not verified here (needs the live environment), Pre-presentation audit — 19 October 2026 (second round), QA report — 19 October 2026, Results

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Module()` connect `Module` to `news.js`, `.Cb`, `N`, `E`, `pdf-worker.js`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `length` be split into smaller, more focused modules?**
  _Cohesion score 0.05311355311355311 - nodes in this community are weakly interconnected._
- **Why does `i` connect `i` to `length`, `.forEach`, `quill.js`, `Rt`, `N`, `s`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Module()` (e.g. with `ac()` and `$b()`) actually correct?**
  _`Module()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `news.js` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._
- **Why does `e()` connect `.forEach` to `length`, `i`, `quill.js`, `jt`, `N`, `.Cb`, `s`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._