# Graph Report - skolakladno  (2026-10-21)

## Corpus Check
- 31 files · ~25,254,197 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 43 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 862 nodes · 2252 edges · 42 communities (34 shown, 8 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `58822f25`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .forEach
- c
- news.js
- i
- m
- import_wp.py
- appendChild
- news-editor.js
- quill.js
- Rt
- re
- jt
- h
- news.local.js
- build.py
- .remove
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
- insertBefore
- Publishing (news, events, notices, galleries)
- Content inventory and migration map
- Sanitiser
- Deployment
- Media
- N
- eb
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
- `va()` --indirect_call--> `E()`  [INFERRED]
  static/js/vendor/ghostscript-1.1.0/gs.js → static/js/vendor/quill-2.0.3/quill.js
- `jt()` --indirect_call--> `P()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/ghostscript-1.1.0/gs.js

## Import Cycles
- None detected.

## Communities (42 total, 8 thin omitted)

### Community 0 - ".forEach"
Cohesion: 0.05
Nodes (46): A(), applyDelta(), b(), build(), clean(), create(), d(), deleteAt() (+38 more)

### Community 1 - "c"
Cohesion: 0.13
Nodes (4): c, image(), k, normalizeNative()

### Community 2 - "news.js"
Cohesion: 0.07
Nodes (52): ALLOWED, CATEGORIES, commit(), contentsPath(), crypto, editable(), env(), esc() (+44 more)

### Community 3 - "i"
Cohesion: 0.05
Nodes (3): getText(), i, l()

### Community 4 - "m"
Cohesion: 0.06
Nodes (7): attachUI(), g(), getHTML(), m, q(), R(), X

### Community 5 - "import_wp.py"
Cohesion: 0.20
Nodes (13): get_all(), get_json(), _get_json(), lead_image(), legacy_map(), main(), make_url_map(), post_url() (+5 more)

### Community 6 - "appendChild"
Cohesion: 0.23
Nodes (6): appendChild(), kt(), listenDOM(), Lt(), Ot(), Wt()

### Community 7 - "news-editor.js"
Cohesion: 0.12
Nodes (41): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), dateHint(), del(), delEvent() (+33 more)

### Community 8 - "quill.js"
Cohesion: 0.09
Nodes (30): attach(), clone(), constructor(), detach(), emit(), find(), focus(), format() (+22 more)

### Community 10 - "re"
Cohesion: 0.18
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "jt"
Cohesion: 0.15
Nodes (8): formula(), getBounds(), hide(), link(), qt(), St(), T(), video()

### Community 12 - "h"
Cohesion: 0.08
Nodes (10): ua(), E(), h(), hasNext(), N, peek(), peekLength(), peekType() (+2 more)

### Community 13 - "news.local.js"
Cohesion: 0.14
Nodes (9): blobs, crypto, fs, handler, http, path, port, ROOT (+1 more)

### Community 14 - "build.py"
Cohesion: 0.07
Nodes (52): breadcrumbs(), build(), contact_card(), crumbs_html(), _descendants(), enhance_body(), fix_img(), event_slug() (+44 more)

### Community 15 - ".remove"
Cohesion: 0.14
Nodes (15): add(), attribute(), buildItem(), buildLabel(), buildOptions(), buildPicker(), close(), copy() (+7 more)

### Community 16 - "jt"
Cohesion: 0.27
Nodes (12): Bt(), Ct(), Dt(), Ft(), Gt(), It(), jt(), Pt() (+4 more)

### Community 17 - "trust.js"
Cohesion: 0.20
Nodes (4): recent, assert, call(), handler

### Community 18 - "Module"
Cohesion: 0.10
Nodes (11): Module(), a(), bb(), cc(), a(), O(), R(), sa() (+3 more)

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

### Community 29 - "insertBefore"
Cohesion: 0.42
Nodes (3): descendant(), Et(), insertBefore()

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
Cohesion: 0.31
Nodes (4): download(), Media, _norm(), retry()

### Community 36 - "N"
Cohesion: 0.52
Nodes (7): hb(), ib(), M(), N(), P(), Q(), rb()

### Community 37 - "eb"
Cohesion: 0.33
Nodes (6): Aa(), eb(), fb(), wa(), ya(), za()

### Community 40 - "QA report — 19 October 2026"
Cohesion: 0.29
Nodes (6): Cross-device audit and publishing workflow (21 October 2026), Fixed during QA, Not verified here (needs the live environment), Pre-presentation audit — 19 October 2026 (second round), QA report — 19 October 2026, Results

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Module()` connect `Module` to `N`, `eb`, `pdf-worker.js`, `h`, `news.local.js`, `.Cb`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `.forEach` be split into smaller, more focused modules?**
  _Cohesion score 0.05024859832857294 - nodes in this community are weakly interconnected._
- **Why does `e()` connect `.forEach` to `i`, `m`, `appendChild`, `h`, `jt`, `.Cb`, `insertBefore`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 6 inferred relationships involving `Module()` (e.g. with `ac()` and `$b()`) actually correct?**
  _`Module()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Should `c` be split into smaller, more focused modules?**
  _Cohesion score 0.13071895424836602 - nodes in this community are weakly interconnected._
- **Why does `jt()` connect `jt` to `.forEach`, `N`, `appendChild`, `quill.js`, `Rt`, `jt`, `.remove`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._