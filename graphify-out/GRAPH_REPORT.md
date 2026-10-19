# Graph Report - skolaKladno  (2026-10-19)

## Corpus Check
- 26 files · ~25,245,971 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 41 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 732 nodes · 2013 edges · 41 communities (34 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a83e391e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- length
- re
- news.js
- i
- .value
- import_wp.py
- m
- news-editor.js
- quill.js
- Rt
- re
- jt
- h
- .listen
- build.py
- c
- b
- .forEach
- .add
- vercel.json
- zsmr.eu
- School logo: Základní škola Maltézských rytířů
- Design system: zsmr.eu
- make_logo.py
- CLAUDE.md
- Product
- z
- .remove
- u
- Content inventory and migration map
- Sanitiser
- enhance_body
- Deployment
- split
- Media
- do_GET
- Brand compliance report
- QA report — 19 October 2026

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
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 16 → community 11_
- `update()` --indirect_call--> `e()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 11_

## Import Cycles
- None detected.

## Communities (41 total, 7 thin omitted)

### Community 0 - "length"
Cohesion: 0.06
Nodes (38): A(), applyDelta(), create(), d(), deleteAt(), deleteText(), descendants(), enforceAllowedChildren() (+30 more)

### Community 1 - "re"
Cohesion: 0.38
Nodes (5): _index(), news_card(), page_title(), plain(), render_home()

### Community 2 - "news.js"
Cohesion: 0.06
Nodes (41): ALLOWED, CATEGORIES, commit(), crypto, editable(), env(), esc(), excerptOf() (+33 more)

### Community 5 - "import_wp.py"
Cohesion: 0.19
Nodes (14): get_all(), get_json(), _get_json(), lead_image(), legacy_map(), main(), make_url_map(), post_url() (+6 more)

### Community 6 - "m"
Cohesion: 0.08
Nodes (6): attachUI(), g(), getHTML(), m, replaceWith(), X

### Community 7 - "news-editor.js"
Cohesion: 0.16
Nodes (29): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), del(), drop(), edit() (+21 more)

### Community 8 - "quill.js"
Cohesion: 0.11
Nodes (24): attach(), constructor(), detach(), Dt(), emit(), focus(), format(), formats() (+16 more)

### Community 9 - "Rt"
Cohesion: 0.12
Nodes (4): j, nt(), Rt(), y()

### Community 10 - "re"
Cohesion: 0.18
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "jt"
Cohesion: 0.22
Nodes (14): Bt(), Ct(), Ft(), Gt(), e(), jt(), kt(), Ot() (+6 more)

### Community 12 - "h"
Cohesion: 0.09
Nodes (9): E(), h(), hasNext(), N, peek(), peekLength(), peekType(), rest() (+1 more)

### Community 13 - ".listen"
Cohesion: 0.15
Nodes (8): formula(), getBounds(), hide(), link(), qt(), St(), T(), video()

### Community 14 - "build.py"
Cohesion: 0.13
Nodes (27): breadcrumbs(), build(), contact_card(), crumbs_html(), _descendants(), fmt_date(), img(), layout() (+19 more)

### Community 15 - "c"
Cohesion: 0.08
Nodes (4): c, clone(), q(), R()

### Community 16 - "b"
Cohesion: 0.19
Nodes (7): b(), build(), find(), getFormat(), keys(), l(), position()

### Community 17 - ".forEach"
Cohesion: 0.23
Nodes (6): clean(), copy(), image(), k, move(), normalizeNative()

### Community 18 - ".add"
Cohesion: 0.29
Nodes (8): buildItem(), buildLabel(), buildOptions(), buildPicker(), close(), escape(), Lt(), selectItem()

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

### Community 28 - "z"
Cohesion: 0.22
Nodes (3): handleDOM(), listenDOM(), z()

### Community 29 - ".remove"
Cohesion: 0.33
Nodes (4): descendant(), Et(), insertBefore(), show()

### Community 30 - "u"
Cohesion: 0.27
Nodes (3): add(), u, value()

### Community 31 - "Content inventory and migration map"
Cohesion: 0.25
Nodes (7): Categories, Content inventory and migration map, Flagged content (needs a decision, not invented), News by year, Other content of the old site, Pages, Totals

### Community 32 - "Sanitiser"
Cohesion: 0.20
Nodes (3): _iframe_label(), url_map(), Sanitiser

### Community 33 - "enhance_body"
Cohesion: 0.33
Nodes (3): enhance_body(), fix_img(), image_size()

### Community 34 - "Deployment"
Cohesion: 0.40
Nodes (4): Deployment, Domain, Launch checklist, Size

### Community 35 - "split"
Cohesion: 0.31
Nodes (3): appendChild(), insertAt(), split()

### Community 36 - "Media"
Cohesion: 0.31
Nodes (4): download(), Media, _norm(), retry()

### Community 37 - "do_GET"
Cohesion: 0.67
Nodes (4): serve(), do_GET(), end_headers(), guess_type()

### Community 40 - "QA report — 19 October 2026"
Cohesion: 0.40
Nodes (4): Fixed during QA, Not verified here (needs the live environment), QA report — 19 October 2026, Results

## Knowledge Gaps
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `i` connect `i` to `length`, `m`, `quill.js`, `jt`, `h`, `c`, `b`, `.add`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `length` be split into smaller, more focused modules?**
  _Cohesion score 0.05840071877807727 - nodes in this community are weakly interconnected._
- **Why does `m` connect `m` to `length`, `split`, `.value`, `quill.js`, `Rt`, `jt`, `.listen`, `c`, `b`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `news.js` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._
- **Why does `s` connect `length` to `i`, `quill.js`, `jt`, `h`, `.add`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `i` be split into smaller, more focused modules?**
  _Cohesion score 0.06463414634146342 - nodes in this community are weakly interconnected._