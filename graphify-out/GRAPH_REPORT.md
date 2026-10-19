# Graph Report - skolaKladno  (2026-10-19)

## Corpus Check
- 26 files · ~25,246,992 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 41 file(s) not represented in the graph (top: .woff2 16, .odt 15, .otf 4)

## Summary
- 738 nodes · 2023 edges · 32 communities (28 shown, 4 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6439f83a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- length
- q
- news.js
- i
- .forEach
- import_wp.py
- m
- news-editor.js
- quill.js
- Rt
- re
- jt
- N
- re
- build.py
- split
- render_article
- s
- vercel.json
- zsmr.eu
- School logo: Základní škola Maltézských rytířů
- Design system: zsmr.eu
- make_logo.py
- CLAUDE.md
- Product
- Content inventory and migration map
- Deployment
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
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 3 → community 4_
- `i` --indirect_call--> `i()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 3 → community 17_
- `o` --indirect_call--> `i()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 0 → community 17_
- `p()` --indirect_call--> `i()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 4 → community 17_
- `update()` --indirect_call--> `p()`  [INFERRED]
  static/js/vendor/quill-2.0.3/quill.js → static/js/vendor/quill-2.0.3/quill.js  _Bridges community 4 → community 8_

## Import Cycles
- None detected.

## Communities (32 total, 4 thin omitted)

### Community 0 - "length"
Cohesion: 0.08
Nodes (20): applyDelta(), create(), d(), deleteText(), formatLine(), formatText(), h(), handler() (+12 more)

### Community 1 - "q"
Cohesion: 0.14
Nodes (3): attachUI(), q(), R()

### Community 2 - "news.js"
Cohesion: 0.06
Nodes (41): ALLOWED, CATEGORIES, commit(), crypto, editable(), env(), esc(), excerptOf() (+33 more)

### Community 3 - "i"
Cohesion: 0.06
Nodes (4): getText(), i, l(), v()

### Community 4 - ".forEach"
Cohesion: 0.08
Nodes (28): b(), Bt(), clean(), copy(), Ct(), descendant(), descendants(), Et() (+20 more)

### Community 5 - "import_wp.py"
Cohesion: 0.09
Nodes (21): download(), get_all(), get_json(), _get_json(), _iframe_label(), lead_image(), legacy_map(), main() (+13 more)

### Community 6 - "m"
Cohesion: 0.09
Nodes (5): attribute(), g(), getHTML(), m, values()

### Community 7 - "news-editor.js"
Cohesion: 0.16
Nodes (29): addCategory(), attachmentRow(), call(), categories(), clearPhoto(), del(), drop(), edit() (+21 more)

### Community 8 - "quill.js"
Cohesion: 0.06
Nodes (53): appendChild(), attach(), build(), buildItem(), buildLabel(), buildOptions(), buildPicker(), close() (+45 more)

### Community 9 - "Rt"
Cohesion: 0.13
Nodes (3): j, Rt(), show()

### Community 10 - "re"
Cohesion: 0.11
Nodes (4): main(), Page, redirect_sources(), resolves()

### Community 11 - "jt"
Cohesion: 0.14
Nodes (9): formula(), getBounds(), hide(), link(), qt(), rangeToNative(), St(), T() (+1 more)

### Community 12 - "N"
Cohesion: 0.16
Nodes (3): E(), N, w()

### Community 13 - "re"
Cohesion: 0.31
Nodes (7): layout(), logo(), nav_html(), news_card(), plain(), render_home(), render_simple()

### Community 14 - "build.py"
Cohesion: 0.13
Nodes (22): breadcrumbs(), build(), contact_card(), crumbs_html(), _descendants(), _index(), load_news(), load_pages() (+14 more)

### Community 15 - "split"
Cohesion: 0.08
Nodes (8): add(), c, clone(), insertAt(), split(), u, value(), X

### Community 16 - "render_article"
Cohesion: 0.25
Nodes (6): enhance_body(), fix_img(), fmt_date(), image_size(), img(), render_article()

### Community 17 - "s"
Cohesion: 0.08
Nodes (9): A(), i(), image(), index(), k, normalizedToRange(), normalizeNative(), register() (+1 more)

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
Cohesion: 0.18
Nodes (8): compact(), lockup(), main(), mark(), shield(), text_path(), vos_lockup(), vos_text()

### Community 27 - "Product"
Cohesion: 0.17
Nodes (11): Accessibility & Inclusion, Brand Commitments, Capabilities and Constraints, Operating Context, Platform, Positioning, Product, Product Principles (+3 more)

### Community 31 - "Content inventory and migration map"
Cohesion: 0.25
Nodes (7): Categories, Content inventory and migration map, Flagged content (needs a decision, not invented), News by year, Other content of the old site, Pages, Totals

### Community 34 - "Deployment"
Cohesion: 0.40
Nodes (4): Deployment, Domain, Launch checklist, Size

### Community 37 - "do_GET"
Cohesion: 0.67
Nodes (4): serve(), do_GET(), end_headers(), guess_type()

### Community 40 - "QA report — 19 October 2026"
Cohesion: 0.33
Nodes (5): Fixed during QA, Not verified here (needs the live environment), Pre-presentation audit — 19 October 2026 (second round), QA report — 19 October 2026, Results

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `i` connect `i` to `length`, `q`, `.forEach`, `m`, `quill.js`, `N`, `s`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `i` (e.g. with `e()` and `i()`) actually correct?**
  _`i` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `length` be split into smaller, more focused modules?**
  _Cohesion score 0.08391608391608392 - nodes in this community are weakly interconnected._
- **Why does `m` connect `m` to `length`, `q`, `.forEach`, `quill.js`, `Rt`, `jt`, `split`, `s`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `q` be split into smaller, more focused modules?**
  _Cohesion score 0.1437908496732026 - nodes in this community are weakly interconnected._
- **Why does `s` connect `s` to `quill.js`, `length`, `i`, `.forEach`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `news.js` be split into smaller, more focused modules?**
  _Cohesion score 0.05952380952380952 - nodes in this community are weakly interconnected._