# How a reported supplier is shown (S16.6, H-3): proposal

**Status:** decided by the human on 2026-10-07 (H-3: "as in the preview, built now"); built in S16.6 (D-148). One
deviation from the mock-up: the research view draws "reported" as a double line, not dash-dot (D-148).
Proposed earlier on 2026-10-07.
**Why now:** the human approved two supplier values on 2026-10-07 (H-2):

- **the H100's HBM:** SK hynix, historical (to 2024-03), reported by TrendForce;
- **Trainium2's HBM:** Samsung, reported by SemiAnalysis, recognition not shown.

Both page builds stop as soon as a supplier is named (D-130). They cannot draw an undesigned value. D-147
asks for the "reported" label.

**Preview:** [`../../sessions/reports/SESSION-16.6-qa/mockup/supplier-mockup.png`](../../sessions/reports/SESSION-16.6-qa/mockup/supplier-mockup.png),
a hand-made mock-up, not a build.

## What the reader would see

| Place | Today | Proposed |
|---|---|---|
| HBM page and research view, "the part's maker" | `supplier: gap · not researched` (amber) | **H100:** `supplier: SK hynix · reported · historical, to 2024-03` — "primarily", per TrendForce, 2024-03-13. **Trainium2:** `supplier: Samsung · reported` — per SemiAnalysis, 2025-12-04; "recognition as a reliable source not shown". A "reported" link is drawn as a dash-dot ink line, with the word "reported" (never colour alone) |
| Evidence panel of the supplier | the gap's state | the attributed claim, its anchor and the two criteria (met or not, with the reason), plus the date that makes it historical |
| Headline of the research view | "who makes it: not researched" | the question only, because the two chains no longer share one state (the existing rule, V-2) |
| Evidence coverage | 4 links: stated, inferred, gap | 4 links: stated, inferred, **reported**, gap. Trainium2: 2 stated, 1 inferred, 1 reported, 0 gaps. H100: 1 stated, 1 inferred, 1 reported, 1 gap |
| Evidence age | the supplier rows are undated | the supplier rows are dated by their reports. The H100's is marked historical (2024-03-13, older than twelve months); Trainium2's is 2025-12-04 |
| The three supplier blocks | "2 of 2 with supplier not researched" | still **cannot be computed yet**, with a new reason: "2 of 2 with a supplier reported by a third party; none with its full set of suppliers stated". Neither report says its maker was the only one ("primarily"; "does not say only"). A count of 1 would read as single-sourcing |

## What changes in the files

| File | Change | Supersedes |
|---|---|---|
| `sql/accelerator_dependencies.sql` | a supplier assertion becomes a row with its company; basis **reported** when the row's claims include an `ATTRIBUTION` and no `FACT`; new columns: the period end (`valid_to`, for "historical") and the unmet criteria | D-120's basis definitions (D-147) |
| `sql/evidence_coverage.sql` | a `reported` column: stated + inferred + reported + gap = links | D-128's split |
| `sql/supplier_metrics.sql` | a metric is computable only when its "needs" are met, not when any supplier is named. Counts of reported and party-stated suppliers are kept apart | D-130's status rule |
| `tools/build_page.py`, `tools/build_insight.py`, the templates | draw a named supplier with its basis, period and unmet criteria; the dash-dot line for "reported" | D-104 and D-130's stop rule (it stays for a supplier with no design) |
| `docs/architecture/visual-architecture.md` §9 | one row: "an edge field resting on third-party reports → reported → dash-dot line → ink" | S14.5's semantics (a superseding decision) |
| tests | PG, IN and WH checks for the label, the period, the criteria and the coverage add-up, written first | — |

Unchanged: the data approved at H-2, the other blocks, and the rule that every word comes from a record or a
marked framing.

## What it costs and limits

- It is the largest change since S15: three queries, both builds, the semantics table, about ten checks,
  the full harness and browser QA. It takes the rest of this session.
- "Reported" becomes a fourth basis, which every later metric must handle.
- The supplier metrics stay uncomputable until a source states a part's full supplier set.
