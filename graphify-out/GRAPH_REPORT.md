# Graph Report - skolaKladno  (2026-10-19)

## Corpus Check
- 25 files · ~25,237,947 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 41 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 726 nodes · 2008 edges · 33 communities (27 shown, 6 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `311b96ca`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .forEach
- build.py
- news.js
- i
- .value
- import_wp.py
- length
- news-editor.js
- quill.js
- Rt
- re
- jt
- h
- .listen
- build
- c
- s
- .add
- vercel.json
- zsmr.eu
- School logo: Základní škola Maltézských rytířů
- Design system: zsmr.eu
- make_logo.py
- CLAUDE.md
- Product
- .remove
- Content inventory and migration map
- render_page
- Deployment
- do_GET
- Brand compliance report

## God Nodes (most connected - your core abstractions)
1. `i` - 63 edges
2. `m` - 51 edges
3. `length()` - 51 edges
4. `o` - 47 edges
5. `s` - 44 edges
6. `h()` - 35 edges
7. `b()` - 29 edges
8. `update()` - 28 edges
9. `jt()` - 26 edges
10. `split()` - 25 edges

## Surprising Connections (you probably didn't know these)
- `i` --indirect_call--> `e()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 3 → community 11_
- `i` --indirect_call--> `i()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 3 → community 0_
- `m` --indirect_call--> `e()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 6 → community 11_
- `b()` --indirect_call--> `e()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 11_
- `formatAt()` --indirect_call--> `i()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 6_

## Import Cycles
- None detected.

## Communities (33 total, 6 thin omitted)

### Community 0 - ".forEach"
Cohesion: 0.09
Nodes (29): A(), applyDelta(), b(), build(), clean(), create(), deleteText(), descendants() (+21 more)

### Community 1 - "build.py"
Cohesion: 0.19
Nodes (13): _descendants(), fmt_date(), _index(), load_news(), load_pages(), news_card(), news_item(), page_title() (+5 more)

### Community 2 - "news.js"
Cohesion: 0.06
Nodes (41): ALLOWED, CATEGORIES, commit(), crypto, editable(), env(), esc(), excerptOf() (+33 more)

### Community 4 - ".value"
Cohesion: 0.33
Nodes (4): attribute(), copy(), move(), values()

### Community 5 - "import_wp.py"
Cohesion: 0.09
Nodes (21): download(), get_all(), get_json(), _get_json(), _iframe_label(), lead_image(), legacy_map(), main() (+13 more)

### Community 6 - "length"
Cohesion: 0.05
Nodes (28): appendChild(), attachUI(), d(), deleteAt(), descendant(), enforceAllowedChildren(), Et(), format() (+20 more)

### Community 7 - "news-editor.js"
Cohesion: 0.16
Nodes (29): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), del(), drop(), edit() (+21 more)

### Community 8 - "quill.js"
Cohesion: 0.11
Nodes (21): attach(), constructor(), Dt(), emit(), focus(), formats(), getNativeRange(), handleComposition() (+13 more)

### Community 10 - "re"
Cohesion: 0.17
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "jt"
Cohesion: 0.19
Nodes (15): Bt(), Ct(), Ft(), Gt(), e(), jt(), kt(), Lt() (+7 more)

### Community 12 - "h"
Cohesion: 0.09
Nodes (9): E(), h(), hasNext(), N, peek(), peekLength(), peekType(), rest() (+1 more)

### Community 13 - ".listen"
Cohesion: 0.15
Nodes (8): formula(), getBounds(), hide(), link(), qt(), St(), T(), video()

### Community 14 - "build"
Cohesion: 0.19
Nodes (11): build(), layout(), logo(), nav_html(), paginate(), redirect_lines(), render_news_editor(), render_news_index() (+3 more)

### Community 15 - "c"
Cohesion: 0.08
Nodes (4): c, clone(), q(), R()

### Community 17 - "s"
Cohesion: 0.08
Nodes (8): image(), index(), k, normalizedToRange(), normalizeNative(), offset(), register(), s

### Community 18 - ".add"
Cohesion: 0.33
Nodes (7): buildItem(), buildLabel(), buildOptions(), buildPicker(), l(), position(), selectItem()

### Community 19 - "vercel.json"
Cohesion: 0.20
Nodes (9): buildCommand, cleanUrls, framework, headers, installCommand, outputDirectory, redirects, $schema (+1 more)

### Community 20 - "zsmr.eu"
Cohesion: 0.29
Nodes (6): Commands, Documentation, Editorial workflow, Settings in Vercel (Project → Settings → Environment Variables), Where things are, zsmr.eu

### Community 21 - "School logo: Základní škola Maltézských rytířů"
Cohesion: 0.33
Nodes (5): Approvals and open points, Basis, Files (`static/img/logo/`), Rules, School logo: Základní škola Maltézských rytířů

### Community 22 - "Design system: zsmr.eu"
Cohesion: 0.40
Nodes (4): Added components, Design system: zsmr.eu, Rules kept, What changes, and why

### Community 23 - "make_logo.py"
Cohesion: 0.13
Nodes (6): compact(), lockup(), main(), mark(), shield(), text_path()

### Community 27 - "Product"
Cohesion: 0.17
Nodes (11): Accessibility & Inclusion, Brand Commitments, Capabilities and Constraints, Operating Context, Platform, Positioning, Product, Product Principles (+3 more)

### Community 28 - ".remove"
Cohesion: 0.12
Nodes (8): add(), close(), escape(), handleDOM(), listenDOM(), show(), value(), z()

### Community 31 - "Content inventory and migration map"
Cohesion: 0.25
Nodes (7): Categories, Content inventory and migration map, Flagged content (needs a decision, not invented), News by year, Other content of the old site, Pages, Totals

### Community 33 - "render_page"
Cohesion: 0.19
Nodes (11): breadcrumbs(), contact_card(), crumbs_html(), enhance_body(), fix_img(), image_size(), img(), render_article() (+3 more)

### Community 34 - "Deployment"
Cohesion: 0.50
Nodes (3): Deployment, Domain, Launch checklist

### Community 37 - "do_GET"
Cohesion: 0.67
Nodes (4): serve(), do_GET(), end_headers(), guess_type()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `i` connect `i` to `.forEach`, `length`, `quill.js`, `jt`, `h`, `c`, `s`, `.add`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `.forEach` be split into smaller, more focused modules?**
  _Cohesion score 0.08893360160965795 - nodes in this community are weakly interconnected._
- **Why does `m` connect `length` to `.forEach`, `.value`, `quill.js`, `Rt`, `jt`, `.listen`, `c`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `news.js` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._
- **Why does `s` connect `s` to `.forEach`, `i`, `length`, `quill.js`, `jt`, `h`, `.add`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `i` be split into smaller, more focused modules?**
  _Cohesion score 0.07051282051282051 - nodes in this community are weakly interconnected._