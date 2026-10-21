# Graph Report - skolaKladno  (2026-10-21)

## Corpus Check
- 33 files · ~25,255,630 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 43 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 869 nodes · 2262 edges · 47 communities (36 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9ce06c73`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .forEach
- c
- news.js
- i
- m
- import_wp.py
- .remove
- news-editor.js
- quill.js
- Rt
- re
- jt
- h
- news.local.js
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
- .Cb
- normalizedToRange
- Publishing (news, events, notices, galleries)
- Content inventory and migration map
- Sanitiser
- optimize_media.py
- Deployment
- Media
- N
- eb
- Brand compliance report
- QA report — 19 October 2026
- u
- a
- .value
- T
- .mcp.json

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
- `va()` --indirect_call--> `E()`  [INFERRED]
  static/js/vendor/ghostscript-1.1.0/gs.js → static/js/vendor/quill-2.0.3/quill.js
- `jt()` --indirect_call--> `P()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/ghostscript-1.1.0/gs.js

## Import Cycles
- None detected.

## Communities (47 total, 11 thin omitted)

### Community 0 - ".forEach"
Cohesion: 0.05
Nodes (45): A(), appendChild(), applyDelta(), b(), build(), clean(), create(), d() (+37 more)

### Community 1 - "c"
Cohesion: 0.08
Nodes (4): c, clone(), q(), R()

### Community 2 - "news.js"
Cohesion: 0.07
Nodes (52): ALLOWED, CATEGORIES, commit(), contentsPath(), crypto, editable(), env(), esc() (+44 more)

### Community 4 - "m"
Cohesion: 0.07
Nodes (7): attachUI(), descendant(), Et(), g(), getHTML(), m, X

### Community 5 - "import_wp.py"
Cohesion: 0.18
Nodes (14): get_all(), get_json(), _get_json(), lead_image(), legacy_map(), main(), make_url_map(), post_url() (+6 more)

### Community 6 - ".remove"
Cohesion: 0.15
Nodes (12): attach(), format(), getRange(), handleDOM(), insertBefore(), moveChildren(), Ot(), position() (+4 more)

### Community 7 - "news-editor.js"
Cohesion: 0.12
Nodes (41): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), dateHint(), del(), delEvent() (+33 more)

### Community 8 - "quill.js"
Cohesion: 0.12
Nodes (19): constructor(), detach(), emit(), focus(), formats(), handleComposition(), handleCompositionEnd(), handleCompositionStart() (+11 more)

### Community 10 - "re"
Cohesion: 0.18
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "jt"
Cohesion: 0.20
Nodes (7): formula(), getBounds(), hide(), link(), qt(), St(), video()

### Community 12 - "h"
Cohesion: 0.09
Nodes (9): E(), h(), hasNext(), N, peek(), peekLength(), peekType(), rest() (+1 more)

### Community 13 - "news.local.js"
Cohesion: 0.14
Nodes (9): blobs, crypto, fs, handler, http, path, port, ROOT (+1 more)

### Community 14 - "build.py"
Cohesion: 0.07
Nodes (52): breadcrumbs(), build(), contact_card(), crumbs_html(), _descendants(), enhance_body(), fix_img(), event_slug() (+44 more)

### Community 15 - ".add"
Cohesion: 0.29
Nodes (8): buildItem(), buildLabel(), buildOptions(), buildPicker(), close(), escape(), listenDOM(), selectItem()

### Community 16 - "jt"
Cohesion: 0.17
Nodes (16): Bt(), Ct(), Dt(), Ft(), Gt(), It(), jt(), kt() (+8 more)

### Community 17 - "trust.js"
Cohesion: 0.20
Nodes (4): recent, assert, call(), handler

### Community 18 - "Module"
Cohesion: 0.11
Nodes (6): Module(), O(), R(), sb(), ua(), ub()

### Community 19 - "vercel.json"
Cohesion: 0.18
Nodes (10): buildCommand, cleanUrls, crons, framework, headers, installCommand, outputDirectory, redirects (+2 more)

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

### Community 28 - ".Cb"
Cohesion: 0.28
Nodes (8): c(), d(), I, jb(), kb(), lb(), mb(), qb()

### Community 29 - "normalizedToRange"
Cohesion: 0.22
Nodes (6): getNativeRange(), image(), index(), k, normalizedToRange(), normalizeNative()

### Community 30 - "Publishing (news, events, notices, galleries)"
Cohesion: 0.29
Nodes (6): Daily rebuild (scheduled posts, events), Publishing (news, events, notices, galleries), Security, Testing, What can be published, Who can do what

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
Cohesion: 0.43
Nodes (3): download(), Media, _norm()

### Community 36 - "N"
Cohesion: 0.52
Nodes (7): hb(), ib(), M(), N(), P(), Q(), rb()

### Community 37 - "eb"
Cohesion: 0.33
Nodes (6): Aa(), eb(), fb(), wa(), ya(), za()

### Community 40 - "QA report — 19 October 2026"
Cohesion: 0.29
Nodes (6): Cross-device audit and publishing workflow (21 October 2026), Fixed during QA, Not verified here (needs the live environment), Pre-presentation audit — 19 October 2026 (second round), QA report — 19 October 2026, Results

### Community 42 - "u"
Cohesion: 0.27
Nodes (3): add(), u, value()

### Community 43 - "a"
Cohesion: 0.33
Nodes (6): a(), bb(), cc(), a(), sa(), va()

### Community 44 - ".value"
Cohesion: 0.33
Nodes (4): attribute(), copy(), move(), values()

## Knowledge Gaps
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Module()` connect `Module` to `N`, `eb`, `pdf-worker.js`, `a`, `news.local.js`, `.Cb`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `.forEach` be split into smaller, more focused modules?**
  _Cohesion score 0.054603174603174605 - nodes in this community are weakly interconnected._
- **Why does `e()` connect `.forEach` to `i`, `m`, `.remove`, `h`, `jt`, `.Cb`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Module()` (e.g. with `ac()` and `$b()`) actually correct?**
  _`Module()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `c` be split into smaller, more focused modules?**
  _Cohesion score 0.08275862068965517 - nodes in this community are weakly interconnected._
- **Why does `jt()` connect `jt` to `.forEach`, `N`, `.remove`, `quill.js`, `Rt`, `jt`, `.value`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._