# The first metrics

**Status:** ACCEPTED as built by the human on 2026-10-06 at the S15 review (D-127 to D-132).
**Audited in S16 (2026-10-07,** [`analytical-audit-S16.md`](./analytical-audit-S16.md)**), decided by the human
(H-3, H-4):**
- evidence coverage: kept, with its records line and population reworded (D-133);
- source age: kept, saying that the 12-month horizon applies only to time-sensitive links (D-134);
- the publishers count: **retired** (D-135); its history stays in §6;
- the three supplier metrics: kept as built (D-136);
- the reference date moves with each session that rebuilds the pages; S16 set it to 2026-10-07 (D-137).
**Decided by the human at the S15 opening (2026-10-06):**
- the contract runs as written, with `sql-layer.md` §7's publisher sentence corrected (D-127);
- the three supplier metrics are shown as "cannot be computed yet", with why (H-1, D-130);
- evidence coverage is measured per accelerator, over its links (H-2, D-128);
- source age is measured against a reference date kept in the query file (H-3, D-129);
- the metrics appear in the research view's indicator blocks (H-4, D-132).

**Required by:**
- `SESSION-ROADMAP.md` S15 ("Implement transparent descriptive metrics for supplier and geographic
  concentration"; non-goal: "Do not create an opaque composite 'dependency score'");
- `PROJECT-EVALUATION-FRAMEWORK.md` §8;
- `visual-architecture.md` §7.5, §10 (D-124, accepted);
- `sql-layer.md` (D-117 to D-121).

**Roles:** Analyst (the queries), Knowledge Architect (populations, denominators, unknowns, rows vs
records), Data Auditor (the independent computations), Editorial (the page blocks and tutorials).
**Claim label:** every metric is a `DERIVATION` over what the Atlas records. Its value lives in
`sql/results/`, never in `data/`.

## In short

S15 asked for five metrics. The records support two of them today, so two are computed, and three
are shown as "cannot be computed yet", with the reason:

| Metric | Query | Status | What it says today |
|---|---|---|---|
| Evidence coverage | `sql/evidence_coverage.sql` | computed | Trainium2: 2 of 4 links stated, 1 inferred, 1 gap. H100: 1 of 4 stated, 1 inferred, 2 gaps. Each accelerator's 4 rows come from 3 records, 1 of them shared |
| Source age | `sql/source_age.sql` | computed, as of 2026-10-07 (D-137) | 5 of the 6 dated links rest on evidence older than 12 months; the source policy's re-check applies to only one of them, already a gap (D-134). The one recent date (6 days) is only the day an undated page was read |
| Supplier count | `sql/supplier_metrics.sql` | cannot be computed yet | 0 of 2 incorporated parts have a named supplier; both are `not_researched` |
| Geographic concentration | `sql/supplier_metrics.sql` | cannot be computed yet | needs where each named supplier makes the part |
| Single-source relationships | `sql/supplier_metrics.sql` | cannot be computed yet | needs a source stating that a part has exactly one supplier |

**One home for each metric's answers.** The eight questions of PEF §8 are answered in each query
file's header (`-- population:`, `-- denominator:`, …). The page's tutorial renders that header, and
the checks require it (WH-9). This document gives the reasoning behind the answers and does not
restate them.

## 1. What a metric is here

- **Built on the rows the page draws.** Each metric query reads the result of
  `accelerator_dependencies.sql` as a view (D-131). It therefore counts and ages exactly the links
  the page shows, under the first query's definitions, and never a second copy of them.
- **A column of a SQL result.** Every metric value on a page is a cell of a committed result (D-124,
  rule 3). The page build only copies cells.
  - The one exception is the per-accelerator count of aged rows in the "Evidence age" block. It is a
    count of rows the page draws in its age table, with the denominator printed (D-124, rule b).
  - The publishers count, the S14.5 presentation count kept in S15, was retired in S16 (§6, D-135).
- **Never a composite.** Each metric has its own block, question, denominator and tutorial. No block
  and no query combines two of them, and no word on the page reads "dependency", "risk" or "score".

## 2. Rows or records (S14.5's finding)

The first result has 8 rows: one per accelerator and link. They come from 5 records:

- the `requires` edge is listed under both accelerators;
- each unknown supplier is a row of its own on its accelerator's `incorporates` edge.

**Evidence coverage counts rows**, because the question is about each accelerator's chain (H-2). The
`records` and `shared` columns say how many records stand behind the rows, so the repetition is
visible in the same block.

**The supplier metrics count incorporated parts per accelerator, not part classes.** Both
accelerators incorporate the same class, High Bandwidth Memory, but who makes the H100's memory and
who makes Trainium2's are two separate unknowns, held on two edges. Counted by class, the population
would be 1 and would hide one of the two unknowns. The first draft of the query made exactly that
mistake. Writing the independent check caught it before any result was committed (report,
Deviations).

## 3. Evidence coverage (D-128)

- **Why per accelerator** (H-2): the page asks what each accelerator's memory depends on, so coverage
  answers how much of each chain rests on a source's own statement.
- **Whole-Atlas coverage was rejected.** It would mix identity fields, which are stated by design,
  and inflate the stated part.
- **Unknowns:** a gap is counted in its own column, `gap`, never dropped. `stated + inferred + gap =
  links` is checked (WH-12).
- **It replaces the prototype's hand count.** The prototype's "links on stated evidence" count gave
  2 of 4 and 1 of 4. The SQL metric gives the same numbers. WH-12 checks the SQL against an
  independent computation, and IN-10 checks the page against both.

## 4. Source age (D-129)

- **The reference date** is written in the query and moves only by a commit (H-3). Each session that
  rebuilds the pages sets it to the day it opened (D-137, S16): 2026-10-06 in S15, 2026-10-07 in S16. An age is "as of" that date. It is never relative to today, so S14.5's rule against clock
  ages (V-5) holds and the result is byte-identical across runs. WH-13 moves the date and checks that
  only the reference date, the ages and the horizon flags change. Since S16 it moves whatever date the query
  holds.
- **Newest evidence.** F-1 asks for at least one citation within the horizon, so a link's age is the
  age of its newest evidence.
- **The evidence-date basis** (S14's and S14.5's debt):
  - the first query now says where each oldest and newest date comes from: a claim's `as_of`, a
    date the source states, or the day it was `accessed`;
  - when kinds share a date, the weakest is reported, so an access date is never hidden;
  - both pages flag a date that is only an access date: the HBM page in the table's caveats, the
    research view on the chain's links and in the age table.
- **The horizon** is source-policy §12's 12 months. A link is beyond it when its newest evidence
  starts more than 12 months before the reference date. A partial date counts from the start of its
  period (F-1). **The policy applies the horizon only to `time_sensitive` links** (who fabricates a
  product, who supplies a part). For `stable` links it is a reading aid, and the block and the tutorial
  say so (S16 finding C-4, D-134).
- **DT-S13-4.** This is the ageing report for the page's chain: as of its reference date, it shows which
  links have passed the horizon. It is not an Atlas-wide report. The other claims' evidence ages
  unreported, as before, and the Atlas-wide report stays with the Change Detector (re-owned, D-129).

## 5. The supplier metrics (D-130)

- **What the query does** (H-1): one row per metric, with:
  - the incorporated parts;
  - how many have a named supplier and how many are unknown;
  - the unknowns' own state word;
  - the company-to-company supply links recorded for those parts;
  - the status (`cannot_be_computed_yet` while no supplier is named);
  - in plain words, what evidence each metric needs.
- **What the page shows:** each as an amber "cannot be computed yet" block, with the reason
  ("2 of 2 parts: supplier not researched") and what it needs.
- **What the page never shows** (V-4, `CLAUDE.md` §7): the named-supplier count (0) or the
  supply-link count (0). A bare zero beside "supplier count" would read as "no suppliers".
- **When the first supplier is named:** the status becomes `computable_not_yet_defined` and the page
  build stops. The metric's presentation has not been designed, and drawing it unreviewed would
  break the stop rule (Part B §16).
- **DT-7:** the `supplier` field and `supplies` edges are kept in separate columns (`parts_supplier_*`
  vs `supplies_links`). No metric combines a product's `vendor` with a `designs` edge. DT-7 is
  closed for S15's metrics.

## 6. The prototype's three hand counts (Part B §06 q10)

| Count | Outcome |
|---|---|
| Links on stated evidence | **replaced** by evidence coverage (same numbers, now SQL) |
| Rows with nothing to date | **replaced** by the evidence-age block: its denominator is the dated links, and the undated ones are a part of their own |
| Publishers behind a sourced row | **kept** in S15 as a presentation count (D-124, rule b). **Retired in S16** (D-135, 2026-10-07): its range was a per-row count the page computed and never showed, its "4 of 6" counted 6 rows from 5 records without saying so, and its only "2" was the inferred link's two reasoning steps. Each table row resting on one publisher keeps its own flag |

## 7. Placement (D-132)

The metrics sit in the research view's INSIGHT layer (H-4 C):

- an "Indicators" row with evidence coverage and evidence age (publishers until S16, D-135);
- a "Cannot be computed yet" row with the three supplier metrics.

Each metric block links to its "How this was computed" in the METHOD layer, which renders the query
file: its question, its eight PEF §8 answers, its steps and its reading guide. The DATA layer gains
"Evidence age, link by link", every row of the source-age result. The HBM journey page is unchanged
except its table's new access-date flag. The research view stays a prototype, not published (NG-13).

## 8. Queries that build on queries (D-131)

- **The view mechanism.** `tools/warehouse.py` runs the queries in dependency order. A query depends
  on another when its code (not its comments) names that query's file stem as a table. After each
  query runs, it becomes a view of the same name, so a later query reads the result instead of
  repeating its definitions.
- **What each result records.** Its inputs include every query file it builds on. A change to the
  first query therefore makes every metric's result stale (WH-11).
- **A cycle stops the run.**
- **The tutorial header** also accepts the eight PEF §8 fields. The page renders them under "The
  question", and WH-9 requires them in every metric's file. This extends D-121's format; it does not
  replace it.

## 9. Rejected alternatives

| Alternative | Why not |
|---|---|
| Repeating the first query's definitions inside each metric | two homes for one definition; a metric could count links the page does not draw |
| DuckDB's `CREATE MACRO` or a shared SQL include | a second mechanism to read; views do the job and appear in the tutorial as plain tables |
| Ages as integers with a sentinel for "nothing to date" | a sentinel is a number standing for an unknown; the column is text holding digits or `not_applicable` |
| Today's date for ages | changes the committed result daily (S14, V-5) |
| Counting part classes for the supplier metrics | hides one of the two unknowns (§2) |
| Showing "0 named suppliers" | reads as "no suppliers" (§5) |
| A share (percent) of stated links | a share over 4 rows overstates precision; the counts say the same without implying a population |
| A summary row of source age in SQL | the per-link rows are the evidence a reader needs; the block counts them with its denominator printed |
