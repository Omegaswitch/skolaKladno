# Brand compliance report

Checked against the same sources as maltezskyrad.cz (`maltezskyrad/docs/brand-compliance.md`): the *Sovereign Order of Malta Worldwide Communications Policy and Guide* (CP, Feb 2025), the *Guidelines for correct use of the two emblems and of the flags of the Order of Malta* (CoA, v3.3) and the Grand Magistry *Entities Theme* (Theme).

✅ complies · ⚠️ caveat or decision needed

| # | Requirement | Source | Status | How the site meets it |
|---|---|---|---|---|
| 1 | Layout and colours recognisably from the Order's web family | CP, Theme | ✅ | Red top bar, graphite menu, grey / white / red footer, `#e31a18` / `#f3f3f3` / `#c7c7c7` / `#454545`, Asap, as on maltezskyrad.cz and velkoprevorskypalac.eu. |
| 2 | Banner of an Order entity | Theme | ⚠️ | Replaced by a white identity band with the school lockup: a school is a work, not an entity. Confirm with the Grand Priory. |
| 3 | Only official emblems; none created or redrawn | CoA | ✅ | Only the red shield of works, copied as vector from the master lockup. The old site's `logo-maltezsky-rad_150x150.png` is not used. `check.py` rejects any other file under `/img/`. |
| 4 | School logo | CoA | ⚠️ | New lockup modelled on the VOS school's logo (`docs/logo.md`). Needs approval by the school, the founder and the Grand Magistry (font substitute, negative version). |
| 5 | Full name of the Order; never the acronym; never "Malta" alone | CP | ✅ | The footer and structured data name the founder in full; `check.py` fails on the acronym. Imported news texts are not rewritten. |
| 6 | Footer link to www.orderofmalta.int | CP | ✅ | Red footer band on every page. |
| 7 | Display serif EB Garamond | — | ⚠️ | Same open question as maltezskyrad.cz (one token, `--display`). |
| 8 | Apolitical, no invented facts | CP | ✅ | Every fact on the new home page and section pages is quoted from the old site's own pages. New wording is limited to headings and short labels, marked `new` in preview builds. |
| 9 | Photographs of children | CP | ⚠️ | All photographs come from the school's current site, where parents consented (the "Souhlas s pořizováním fotografií" form in *Dokumenty pro rodiče*). The school should confirm that consent covers the new site. |

## Open approvals

1. The school lockup (`docs/logo.md`, approvals 1–3).
2. The identity band in place of the Grand Magistry banner (row 2).
3. EB Garamond (row 7), shared with the other Order sites.
4. Every page marked `new` or `existing` in preview builds.
