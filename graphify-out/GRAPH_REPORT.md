# Graph Report - skolaKladno  (2026-10-19)

## Corpus Check
- 19 files · ~738,086 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 39 file(s) not represented in the graph (top: .woff2 16, .odt 14, .otf 4)

## Summary
- 692 nodes · 1977 edges · 27 communities (22 shown, 5 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `83adef48`
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
- s
- jt
- N
- .listen
- .slice
- q
- .attach
- .forEach
- .add
- vercel.json
- zsmr.eu
- School logo: Základní škola Maltézských rytířů
- Design system: zsmr.eu
- .value
- CLAUDE.md

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
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 3 → community 0_
- `m` --indirect_call--> `e()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 6 → community 0_
- `formatAt()` --indirect_call--> `i()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 4_
- `jt()` --indirect_call--> `i()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 11_
- `create()` --indirect_call--> `e()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 9_

## Import Cycles
- None detected.

## Communities (27 total, 5 thin omitted)

### Community 0 - "length"
Cohesion: 0.07
Nodes (32): A(), applyDelta(), b(), build(), d(), deleteText(), descendants(), f (+24 more)

### Community 1 - "build.py"
Cohesion: 0.05
Nodes (48): breadcrumbs(), build(), contact_card(), crumbs_html(), _descendants(), enhance_body(), fix_img(), fmt_date() (+40 more)

### Community 2 - "news.js"
Cohesion: 0.06
Nodes (41): ALLOWED, CATEGORIES, commit(), crypto, editable(), env(), esc(), excerptOf() (+33 more)

### Community 3 - "i"
Cohesion: 0.05
Nodes (4): getText(), i, l(), offset()

### Community 4 - ".remove"
Cohesion: 0.09
Nodes (20): appendChild(), c, clone(), deleteAt(), descendant(), enforceAllowedChildren(), Et(), format() (+12 more)

### Community 5 - "import_wp.py"
Cohesion: 0.09
Nodes (21): download(), get_all(), get_json(), _get_json(), _iframe_label(), lead_image(), legacy_map(), main() (+13 more)

### Community 6 - "m"
Cohesion: 0.09
Nodes (7): attachUI(), clean(), formats(), g(), getHTML(), m, query()

### Community 7 - "news-editor.js"
Cohesion: 0.16
Nodes (29): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), del(), drop(), edit() (+21 more)

### Community 8 - "quill.js"
Cohesion: 0.11
Nodes (22): constructor(), detach(), Dt(), emit(), focus(), getNativeRange(), handleComposition(), handleCompositionEnd() (+14 more)

### Community 9 - "Rt"
Cohesion: 0.12
Nodes (4): create(), j, nt(), Rt()

### Community 11 - "jt"
Cohesion: 0.21
Nodes (13): Bt(), Ct(), Ft(), Gt(), jt(), kt(), Lt(), Pt() (+5 more)

### Community 12 - "N"
Cohesion: 0.16
Nodes (3): E(), N, w()

### Community 13 - ".listen"
Cohesion: 0.20
Nodes (7): formula(), getBounds(), hide(), link(), qt(), St(), video()

### Community 14 - ".slice"
Cohesion: 0.15
Nodes (5): add(), keys(), T(), u, value()

### Community 15 - "q"
Cohesion: 0.16
Nodes (3): q(), R(), X

### Community 16 - ".attach"
Cohesion: 0.17
Nodes (6): attach(), getRange(), handleDOM(), listenDOM(), Ot(), z()

### Community 17 - ".forEach"
Cohesion: 0.20
Nodes (7): copy(), image(), index(), k, move(), normalizedToRange(), normalizeNative()

### Community 18 - ".add"
Cohesion: 0.33
Nodes (8): buildItem(), buildLabel(), buildOptions(), buildPicker(), close(), escape(), position(), selectItem()

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

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `i` connect `i` to `length`, `m`, `quill.js`, `s`, `.slice`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `length` be split into smaller, more focused modules?**
  _Cohesion score 0.0741901776384535 - nodes in this community are weakly interconnected._
- **Why does `m` connect `m` to `length`, `i`, `.remove`, `quill.js`, `Rt`, `.slice`, `q`, `.value`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Should `build.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05128205128205128 - nodes in this community are weakly interconnected._
- **Why does `s` connect `s` to `length`, `i`, `.remove`, `quill.js`, `Rt`, `jt`, `.forEach`, `.add`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `news.js` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._