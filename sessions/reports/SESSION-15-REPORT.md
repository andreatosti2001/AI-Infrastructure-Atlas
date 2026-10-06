# SESSION-15 Report — The first metrics

- **Session:** S15 · **Type:** ANALYSIS · **Milestone:** M4 — Analytical Intelligence (after S14 and S14.5)
- **Date:** 2026-10-06
- **Prompt:** [`sessions/prompts/S15-PROMPT.md`](../prompts/S15-PROMPT.md): Part A as the human gave it,
  Part B integrated with S14.5. Followed as written; Part A was confirmed at the opening.
- **Branch:** `claude/magical-maxwell-qar167`, restarted at `main` @ `2c14e90` (the PR #26 merge, which
  carries S14.5 and this prompt).
- **Base** (D-018 L-03), at the start:
  - `git branch -a`: this branch and `main`, with their remotes, at `2c14e90`;
  - `git ls-remote`: `HEAD` and `main` at `2c14e90`; `claude/new-session-f8y32i` at `36c44a5`;
    `claude/new-session-4kuwvw` at `2759111`;
  - in a fresh Python 3.11 virtualenv built from both pin files: 348 tests OK, `Repository integrity:
    OK`, results and both pages up to date.
- **Before the session:**
  - PR #26 conflicted with `main`, because `main` carried the first draft of the S15 prompt. The
    conflict was resolved by keeping the integrated prompt (merge commit `201de8b`);
  - the human then directed Claude to merge #26 (merged at `2c14e90`, after CI passed on the merge
    commit).
- **Commits:**
  - `b927178` (the metrics, queries, warehouse, pages and checks);
  - `6028409` (tutorial and framing wording);
  - `bcb6f3c` (the state rows and browser QA);
  - `43db042` (the supplier blocks name their population, after the human's reading);
  - `2b9819f` (the research view's QA re-run);
  - `4c09772` (three checks strengthened after the merged break run);
  - and the commit that adds this report, its QA and breaks, and the state rows.

## Mission outcome

**Delivered.** The human challenged each denominator before Claude explained it. Three of four
readings matched; the fourth differed and changed the page's wording (below).

The Atlas has its first metrics. Each answers a stated question over a stated population, is computed
in SQL on the table of links, and is shown in the research view with its denominator in the same
block and its own "How this was computed".

| Metric | Result (as recorded, not of the world) |
|---|---|
| **Evidence coverage** | **AWS Trainium2:** 2 of 4 links stated, 1 inferred, 1 gap. **NVIDIA H100:** 1 of 4 stated, 1 inferred, 2 gaps. Each accelerator's 4 rows come from 3 records, 1 shared between them |
| **Source age**, as of 2026-10-06 | **Trainium2:** 2 of 3 dated links have newest evidence older than 12 months, and 1 of 3 is dated only by the day a page was read. **H100:** 3 of 3 older than 12 months |
| **Supplier count** | **cannot be computed yet:** 2 of 2 incorporated parts have their supplier `not researched` |
| **Geographic concentration** | **cannot be computed yet:** needs where each named supplier makes the part |
| **Single-source relationships** | **cannot be computed yet:** needs a source stating that a part has exactly one supplier |

**The finding in one sentence** (`INTERPRETATION`): of the six dated links around the two
accelerators, five rest on evidence more than a year old as of 2026-10-06. The only recent date is the
day an undated page was read, not a date its content carries. Nothing the Atlas holds names who makes
either accelerator's memory.

**Decided by the human** (2026-10-06, at the S15 opening; outcomes only, D-114):

| Decision point | Outcome | Effect |
|---|---|---|
| Part A | confirmed as written | prompt unchanged |
| `sql-layer.md` §7's publisher sentence | corrected | D-127; one sentence and a status line |
| H-1, the three metrics with no data | shown as "cannot be computed yet", with why | D-130 |
| H-2, the population of evidence coverage | per accelerator, over its links | D-128 |
| H-3, source age without the clock | against a reference date kept in the query file | D-129 |
| H-4, where the metrics appear | in the research view's indicator blocks | D-132 |
| Merging PR #26 before starting | merged by Claude at the human's direction, after CI passed | S15 starts from `main` |

## Files changed

| File | Change |
|---|---|
| `sql/evidence_coverage.sql`, `sql/source_age.sql`, `sql/supplier_metrics.sql` | new: the three metric queries, each answering PEF §8 in its header; results in `sql/results/` |
| `sql/accelerator_dependencies.sql`, its result | two columns: where the oldest and newest evidence dates come from (`as_of`, `stated`, `accessed`); rows unchanged |
| `tools/warehouse.py` | queries run in dependency order and each becomes a view; a result records the query files it builds on; a cycle stops the run (D-131) |
| `tools/build_page.py` | the tutorial header accepts the PEF fields; `sql_tutorial_block` shared by both pages; the S14 table flags access dates |
| `tools/build_insight.py`, `tools/insight_template.html` | the metric blocks, the "cannot be computed yet" blocks, the age table, one tutorial per metric, access dates flagged on the chain |
| `site/hbm-chain/index.html`, `site/hbm-insight/index.html` | rebuilt |
| `tests/test_warehouse.py` | WH-9 extended; WH-10 with the date basis, and a planted tie of date kinds; WH-11 to WH-14 with independent computations |
| `tests/test_page.py` | PG-11 expects the access-date flag where the result has it |
| `tests/test_insight.py` | IN-2 and IN-3 for the new results (a count's denominator must sit beside it); IN-7 for four tutorials; IN-10, IN-11 |
| `docs/architecture/metrics.md` | new: the design (proposed) |
| `docs/architecture/decisions.md` | D-127 to D-132 appended |
| `docs/architecture/sql-layer.md` | §7's publisher sentence and status line (D-127) |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows |
| `sessions/reports/SESSION-15-breaks/` | the merged break harness, its first full run and the final re-run |
| `sessions/reports/SESSION-15-qa/` | QA script, results and screenshots for both pages; the warehouse fail-first output |

`Eu-Digital-Policy`: not touched. No dependency added.

## Data changed

**None.** No source, claim, entity, event, relationship, refused-candidate or identity-basis record was
created or edited. Every metric is a derivation in `sql/results/`.

## Tests run

| Command / check | Result |
|---|---|
| **At start** (`2c14e90`), fresh Python 3.11 venv | OK (348 tests); Gate 0 OK; results and both pages up to date |
| Warehouse checks **fail-first** (queries written, no view support) | `Catalog Error: Table with name accelerator_dependencies does not exist`: every metric query ([`failfirst-warehouse.txt`](./SESSION-15-qa/failfirst-warehouse.txt)) |
| After the view support | 19 warehouse tests OK, after one fix to a check (below) |
| **Final**, same venv | OK (357 tests); Gate 0 OK; `results: up to date`; both pages `up to date` |
| **CI** | every commit pushed; the runs were not observed at writing |

**What writing the checks caught:**

1. **The supplier query's first draft counted part classes**, giving 1 part, not incorporated parts
   per accelerator (2). It would have hidden one of the two unknown suppliers. The independent
   computation was written against the right population, and the query was corrected before any
   result was committed.
2. **WH-13's first form required the horizon flag to change** when the reference date moves six
   months. No link crosses the horizon in that window, so the expectation was wrong, not the query.
   The check now moves the date a year, which does make a link cross, and requires the reference
   date, the ages and the flags to move, and nothing else.

### Deliberate breaks (the merged harness)

[`breaks.py`](./SESSION-15-breaks/breaks.py) merges S13's, S14's and S14.5's harnesses into one shape,
and adds 13 S15 breaks. That makes 74 in total: 67 faults and 7 controls. Each break copies the
repository, makes one edit, rebuilds where stated (always in the order results → HBM page → research
view), runs the full suite, and counts only if the suite fails with the named fragment in its output.
A control counts only if the suite passes.

**The first full run** ([`merged-breaks-first-full-run.txt`](./SESSION-15-breaks/merged-breaks-first-full-run.txt)):
64 of 67 caught for their named reasons, and 7 of 7 controls passing. Three were not caught as named,
and each found something:

| Break | What happened | What it found | Fix |
|---|---|---|---|
| S14.5-T2: a count's denominator removed from the age block | only the stale-rebuild check failed | **a weak check**: two counts in one list item shared one "same block" test, so one could lose its denominator unseen | IN-3 now requires each count's denominator in its own line (`4c09772`) |
| S15-M5: coverage counts gaps as stated | caught by WH-12 and IN-10, not by its named message | **a test-ordering defect**: the add-up message sat after an assertion that failed first | the add-up check runs first |
| S15-M12: the date basis reports the strongest kind | **nothing failed** | **an unexercised rule**: no row of today's data has two kinds of date tied on one day, so the weakest-kind rule was never tested | a new check plants a tie and compares with the independent computation |

**The final re-run** ([`merged-breaks-rerun.txt`](./SESSION-15-breaks/merged-breaks-rerun.txt)), on
`4c09772`: the 25 S14.5 and S15 fault breaks and all 7 controls were re-run. 24 of 25 were caught as named,
and 7 of 7 controls passed. S15-M12 was caught by the new tied-date check, but its expected fragment
still named WH-10's comparison, which cannot see a tie the data does not hold. The fragment now names
the planted-tie check, which also puts its specific reason first. Re-run, S15-M12 is caught as named,
and the controls still pass.

**On the final tree, all 67 fault breaks are caught for their named reasons, and all 7 controls pass.**
The 42 S13 and S14 fault breaks were caught in the first full run. Since then only checks were made
stricter, and a stricter check can only add failures, so each stays caught; their controls were re-run
and pass. The S15 changes after the
first run were all to checks and their expected fragments; no break's edit was weakened.

## Browser QA (D-106)

Playwright from `/opt/node-tools` with the pre-installed Chromium, on the final pages:

- the research view: [`qa.js`](./SESSION-15-qa/qa.js) is S14.5's script plus a tutorials block;
- the HBM page: S14's script, unchanged.

| Check | Research view, 1280 / 375 px | HBM page, 1280 / 375 px |
|---|---|---|
| Console, page errors, network | none, none, the page file only | none, none, the page file only |
| Document overflow; wide elements, also with every disclosure open | none / none | none / none |
| Marks reached by Tab | 16 of 16 | 17 of 17; Enter lands on every panel |
| Tutorials open by keyboard; each metric block's link resolves | 4 of 4; 5 of 5 links | 1 of 1 |
| Basis filter from the keyboard | correct for each basis | — |
| Measured contrast, every text node | min 6.21:1 over 795 / 899 nodes; none below 4.5 | min 6.21:1; none below 4.5 |

Two presentation defects were found by looking at the page and fixed before the final run:

- "1 gaps" (number agreement);
- the age tally's sentence was set at headline size; the count stays large, and the explanation moved
  to the smaller line.

Two wording inaccuracies were also found and fixed:

- the "reproduce" answers said "the page's checks" recompute the metrics, but the warehouse's checks
  do;
- the method framing still called every number a tally.

Screenshots: [`hbm-insight/desktop-02-insight.png`](./SESSION-15-qa/hbm-insight/desktop-02-insight.png),
[`hbm-insight/mobile-02-insight.png`](./SESSION-15-qa/hbm-insight/mobile-02-insight.png),
[`hbm-insight/desktop-06-method-tutorials-open.png`](./SESSION-15-qa/hbm-insight/desktop-06-method-tutorials-open.png),
[`hbm-chain/desktop-05-table.png`](./SESSION-15-qa/hbm-chain/desktop-05-table.png).

## PEF §8, metric by metric

Each metric answers all eight questions in its query file's header. The page renders them, and WH-9 and
IN-11 check them. In short:

| | Evidence coverage | Source age | Supplier metrics |
|---|---|---|---|
| Question | how each accelerator's recorded links divide into stated, inferred and gap | how old the newest evidence behind each link is, as of 2026-10-06, and which links are past 12 months | whether a supplier can be counted, located or shown as single |
| Population | the rows of the table of links (accelerator × link) | the same rows, with their newest evidence date | the incorporated parts, one per accelerator and part |
| Denominator | the links recorded around that accelerator (4 each) | the dated links (3 each); the undated ones are their own part | the incorporated parts (2) |
| Assumptions | the first query's definitions of stated, inferred and gap; every link weighs the same | newest evidence; a partial date counts from its start; the reference date moves only by commit | a supplier is known only when named with its claims |
| Missing data | the suppliers; links nobody has looked for | 14 sources state no date; their age measures the reading | who supplies each part |
| Reproduce | `python tools/warehouse.py`; WH-12 recomputes it independently | WH-13, including the reference-date move | WH-14 |
| Sensitivity | one link changes the split by a quarter | one day per day the reference moves; a link crosses on a known date | the first named supplier changes all three |
| Does not prove | dependence, risk, or source reliability; stated is not confirmed | that an old statement is false, or a recent one true | that a part has no supplier, one or many |

## The human's challenge of the denominators (Part A)

Answered on 2026-10-06, before Claude's explanation. The interactive form was declined, so the questions
were asked as a short written form, one per metric plus one on what the metrics support (outcomes only,
D-114):

| Question | Compared with Claude's reading |
|---|---|
| What the 4 in "2 of 4 links stated" counts | **matched:** the links the Atlas records around the accelerator, not the world's. The refinement that the 4 are rows drawn from 3 records was already in the block |
| Why the H100's age denominator is 3, and older than what | **matched:** only the dated links count, and "older than twelve months" means before 2025-10-06 (the reference date minus 12 months) |
| What the 2 in "2 of 2 parts" counts | **differed:** read as two supplier-related aspects being checked. It counts the memory incorporated in each accelerator, one unknown supplier per accelerator |
| Which conclusions the page supports | **matched:** fewer of the H100's recorded links are stated, and most dated evidence is over a year old. Not that one supply is riskier, and not that no company supplies the memory |

**Effect:** the supplier blocks now name their population: "incorporated parts, one per accelerator: 2 of
2 with supplier not researched" (`43db042`). The numbers did not change. After the comparison, the human
accepted Claude's reading of the supplier blocks' population (2026-10-06). As in S14, a differing reading
marked a place where the page's words were ambiguous.

## Evidence added/retired

None. No source was retrieved.

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-127 | `sql-layer.md` §7: the inferred rows rest on two publishers | accepted (confirmed at the opening) |
| D-128 | evidence coverage per accelerator, over its links | proposed (population decided at H-2) |
| D-129 | source age against a reference date; where each evidence date comes from | proposed (decided at H-3) |
| D-130 | the three supplier metrics: "cannot be computed yet", with why | proposed (decided at H-1) |
| D-131 | queries build on queries; a metric's tutorial answers PEF §8 | proposed |
| D-132 | the metrics in the research view's indicator blocks | proposed (placement decided at H-4) |

**Rejected alternatives** (in the decisions and `metrics.md` §9):

- repeating the first query inside each metric;
- macros or SQL includes;
- integer ages with a sentinel;
- today's date;
- counting part classes;
- showing "0 named suppliers";
- percentages;
- a summary row for source age.

## Deviations

1. **`tools/build_page.py` and `tests/test_page.py` changed under H-4 C.** Part B §12 lists them under
   H-4 A. The access-date flag had to reach the HBM page's table to meet acceptance criterion 7
   ("every evidence date says whether it is an access date"), and the shared tutorial rendering lives
   there. The HBM page changed only by the flag, the tutorial's query attributes and its digest.
2. **The merged harness replaces three S14.5 breaks** (T1 to T3), whose setup text S15 removed with
   the hand counts they edited. Each is replaced by the same fault on the S15 page, named in the
   harness.
3. **The break run was restarted twice** after wording fixes changed inputs (the first attempt had run 4
   breaks, the second 18, all caught). The full run then found three breaks not caught as named. Their
   checks were strengthened, and the 32 breaks and controls those changes could affect were re-run on the
   final tree.
4. **The challenge was asked as a written form** after the interactive form was declined. Its one differing
   reading changed a label after the browser QA, which was then re-run, and stopped the second break run,
   which was restarted on the final tree.

**Invalidated assumptions:**

- "Coverage is a count of rows only" (Part B H-2 A). It counts rows, but the records behind them had
  to be shown in the same block, or "4 links" would overstate what the Atlas holds.
- "The supplier metrics' population is the parts on the page." It is the parts per accelerator; by
  class it would hide an unknown.

## Debt introduced/resolved

**Resolved:**

- the access date standing as an evidence date (S14, S14.5): now a column, flagged on both pages;
- the three break harnesses: merged;
- DT-7, for S15's metrics: no metric combines `vendor` with `designs`, and the supplier field and
  supply links sit in separate columns;
- DT-S13-4 for the page's chain: the source-age metric is its ageing report;
- the publisher sentence (D-127);
- the prototype's hand counts: two replaced by metrics, one kept as presentation.

**Re-owned or introduced:**

| Item | Owner |
|---|---|
| DT-S13-4 beyond the page's chain: an Atlas-wide ageing report | Change Detector (inactive), as before |
| A supplier metric's presentation once a supplier is named (the build stops until then) | the session that adds the first supplier evidence |
| The reference date moves only by commit; nobody is yet charged with moving it | the S15 review: decide whether each session opening moves it |
| `build_page.sql_section` still reads its result from the fixed path | S22 (engineering audit) |
| The research view's filter needs `:has()` | S20 |

## Unresolved issues

**Human decision required: should the S15 metrics and their rules become binding?**

- *What we are deciding:* whether D-128 to D-132 and `docs/architecture/metrics.md` move from "proposed"
  to "accepted".
- *What each one fixes:*
  - **D-128:** evidence coverage is counted per accelerator over its rows, with the records behind them
    in the same block.
  - **D-129:** ages are measured from a reference date written in the query file, and every evidence date
    says whether it is an access date.
  - **D-130:** a supplier metric shows "cannot be computed yet" until a supplier is named, and the page
    build stops rather than draw one that is undesigned.
  - **D-131:** a query may read an earlier query's result, and every metric's file answers PEF §8.
  - **D-132:** metrics live in the research view's indicator blocks.
- *What will concretely change:* if accepted, status lines only. The pages' digest lines follow, because
  `decisions.md` is an input. No data, result, check or page content changes.
- *Why:* S16 audits these metrics. Accepting them fixes what it audits.
- *What stays the same:* the data; the HBM page apart from its access-date flag.
- *Options:*
  - **A, all binding as built:** status lines only.
  - **B, named items changed first:** Claude rewrites them, and the queries, pages and checks they affect,
    before acceptance.
  - **C, named items dropped:** what depends on them is removed. For example, dropping D-132 moves the
    metrics out of the research view.
- *Decision requested:* "Choose A, B or C, naming items for B or C."

**Not asked now:** merging this branch; public deployment (NG-13).

## Process lessons

- **An independent check finds a population error before the query does.** The supplier query's first
  draft counted classes; writing the check against the records showed the population was per
  accelerator.
- **A check can be wrong in its expectation.** WH-13 first required a flag to change that had no reason
  to change. The fix was to the check, with the reason stated, not to the query.
- **Building on the page's own rows keeps metric and visual in step.** Every metric reads the table of
  links as a view, so a change to the first query reaches every metric and both pages, and WH-11 makes
  that visible.
- **A reader's differing answer is a wording defect until shown otherwise.** "2 of 2 parts" passed every
  check and read as something else.
- **A break that changes nothing is a finding.** S15-M12 left every check green, because the data never
  exercises the rule it broke. The answer was a planted case, not a weaker break.
- **A zero is a presentation decision.** "0 named suppliers" is true and misleading, so the page never
  draws it.

## Implications for the next session

**For S16 (the analytical audit):**

- **Completed work:** the metrics above, with their PEF §8 answers in their query files and the table
  above; the gate "transparent metrics" is **met**: every acceptance criterion of Part B §15 holds (the
  human's challenge included).
- **For S16, per metric** (its own required questions, with S15's answers to check):
  - **coverage** measures recorded links by basis; it does not measure dependence. Missing suppliers
    could distort it. It could be misread as a share of truth;
  - **age** measures the newest evidence date against a reference date. It could be misread as
    reliability, or as current when the date is only an access date;
  - **the supplier metrics** measure nothing yet; the "2 of 2" could be misread as a supplier count.
- **Also for S16:** whether a block can be misread through its presentation: the amber, the large
  count, the order of the blocks.
- **Recommended next decision:** whether S16 audits the metrics only, or also H-1's ruling and S14.5's
  binding rule as applied.
- **Files for S16 to read first:**
  - this report;
  - [`docs/architecture/metrics.md`](../../docs/architecture/metrics.md);
  - [`docs/architecture/sql-layer.md`](../../docs/architecture/sql-layer.md);
  - [`docs/architecture/visual-architecture.md`](../../docs/architecture/visual-architecture.md) §7, §10.

**Next recommended milestone:** S16, the analytical audit of these metrics, starting from the one
reading that differed (the supplier blocks' population).
