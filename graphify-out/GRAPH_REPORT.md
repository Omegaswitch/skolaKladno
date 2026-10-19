# Graph Report - skolaKladno  (2026-10-19)

## Corpus Check
- 25 files · ~25,237,859 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 41 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 725 nodes · 2006 edges · 39 communities (32 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `034a737f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- length
- build.py
- news.js
- i
- .remove
- import_wp.py
- m
- news-editor.js
- quill.js
- Rt
- re
- jt
- N
- .listen
- .slice
- c
- .attach
- .forEach
- .add
- vercel.json
- zsmr.eu
- School logo: Základní škola Maltézských rytířů
- Design system: zsmr.eu
- make_logo.py
- CLAUDE.md
- Product
- .contains
- Sanitiser
- Media
- Content inventory and migration map
- enhance_body
- Deployment
- T
- read_doc
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
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 4 → community 11_
- `update()` --indirect_call--> `e()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 11_

## Import Cycles
- None detected.

## Communities (39 total, 7 thin omitted)

### Community 0 - "length"
Cohesion: 0.06
Nodes (34): A(), applyDelta(), attribute(), create(), d(), deleteText(), descendants(), f (+26 more)

### Community 1 - "build.py"
Cohesion: 0.13
Nodes (29): breadcrumbs(), build(), contact_card(), crumbs_html(), _descendants(), fmt_date(), img(), _index() (+21 more)

### Community 2 - "news.js"
Cohesion: 0.06
Nodes (41): ALLOWED, CATEGORIES, commit(), crypto, editable(), env(), esc(), excerptOf() (+33 more)

### Community 4 - ".remove"
Cohesion: 0.07
Nodes (23): appendChild(), b(), build(), clean(), copy(), deleteAt(), descendant(), enforceAllowedChildren() (+15 more)

### Community 5 - "import_wp.py"
Cohesion: 0.20
Nodes (13): get_all(), get_json(), _get_json(), lead_image(), legacy_map(), main(), make_url_map(), post_url() (+5 more)

### Community 6 - "m"
Cohesion: 0.07
Nodes (7): attachUI(), g(), getHTML(), m, replaceWith(), X, z()

### Community 7 - "news-editor.js"
Cohesion: 0.16
Nodes (29): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), del(), drop(), edit() (+21 more)

### Community 8 - "quill.js"
Cohesion: 0.11
Nodes (23): constructor(), detach(), Dt(), emit(), focus(), format(), formats(), getNativeRange() (+15 more)

### Community 9 - "Rt"
Cohesion: 0.11
Nodes (4): j, nt(), Rt(), show()

### Community 10 - "re"
Cohesion: 0.17
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "jt"
Cohesion: 0.35
Nodes (11): Bt(), Ct(), Ft(), Gt(), e(), jt(), Pt(), Tt() (+3 more)

### Community 12 - "N"
Cohesion: 0.16
Nodes (3): E(), N, w()

### Community 13 - ".listen"
Cohesion: 0.20
Nodes (7): formula(), getBounds(), hide(), link(), qt(), St(), video()

### Community 14 - ".slice"
Cohesion: 0.27
Nodes (3): add(), u, value()

### Community 15 - "c"
Cohesion: 0.08
Nodes (4): c, clone(), q(), R()

### Community 16 - ".attach"
Cohesion: 0.48
Nodes (4): attach(), getRange(), insertBefore(), Ot()

### Community 17 - ".forEach"
Cohesion: 0.24
Nodes (5): image(), index(), k, normalizedToRange(), normalizeNative()

### Community 18 - ".add"
Cohesion: 0.22
Nodes (10): buildItem(), buildLabel(), buildOptions(), buildPicker(), close(), escape(), l(), Lt() (+2 more)

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
Cohesion: 0.23
Nodes (6): compact(), lockup(), main(), mark(), shield(), text_path()

### Community 27 - "Product"
Cohesion: 0.17
Nodes (11): Accessibility & Inclusion, Brand Commitments, Capabilities and Constraints, Operating Context, Platform, Positioning, Product, Product Principles (+3 more)

### Community 28 - ".contains"
Cohesion: 0.26
Nodes (4): handleDOM(), kt(), listenDOM(), Wt()

### Community 29 - "Sanitiser"
Cohesion: 0.20
Nodes (4): _iframe_label(), url_map(), sanitise(), Sanitiser

### Community 30 - "Media"
Cohesion: 0.31
Nodes (4): download(), Media, _norm(), retry()

### Community 31 - "Content inventory and migration map"
Cohesion: 0.25
Nodes (7): Categories, Content inventory and migration map, Flagged content (needs a decision, not invented), News by year, Other content of the old site, Pages, Totals

### Community 33 - "enhance_body"
Cohesion: 0.33
Nodes (3): enhance_body(), fix_img(), image_size()

### Community 34 - "Deployment"
Cohesion: 0.50
Nodes (3): Deployment, Domain, Launch checklist

### Community 36 - "read_doc"
Cohesion: 0.67
Nodes (3): load_news(), load_pages(), read_doc()

### Community 37 - "do_GET"
Cohesion: 1.00
Nodes (3): serve(), do_GET(), end_headers()

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `i` connect `i` to `length`, `.remove`, `m`, `quill.js`, `jt`, `N`, `c`, `.add`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `length` be split into smaller, more focused modules?**
  _Cohesion score 0.0581039755351682 - nodes in this community are weakly interconnected._
- **Why does `m` connect `m` to `length`, `T`, `.remove`, `quill.js`, `Rt`, `jt`, `c`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `build.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13015873015873017 - nodes in this community are weakly interconnected._
- **Why does `s` connect `length` to `i`, `.remove`, `quill.js`, `jt`, `.forEach`, `.add`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `news.js` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._