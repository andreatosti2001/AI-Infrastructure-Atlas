# SESSION-14.5 Report — Visual intelligence and research-experience architecture

- **Session:** S14.5 · **Type:** RESEARCH / ARCHITECTURE / LIMITED IMPLEMENTATION · **Milestone:** M4 —
  Analytical Intelligence (inserted between S14 and S15)
- **Date:** 2026-10-06
- **Prompt:** [`sessions/prompts/S14.5-PROMPT.md`](../prompts/S14.5-PROMPT.md), recorded verbatim as
  the human gave it (no Part B; Deviations, 1).
- **Branch:** `claude/magical-maxwell-qar167`, at `main` @ `2a6e91c` (the PR #24 merge, which carries
  S14 and its review).
- **Base** (D-018 L-03), at the start:
  - `git branch -a`: `claude/magical-maxwell-qar167` and `main`, with their two remotes;
  - the working tree was clean;
  - in a fresh Python 3.11 virtualenv built from both pin files: 328 tests OK, `Repository
    integrity: OK`, `page: up to date`, `results: up to date`.
- **Commits:**
  - `359fe8a` (the prompt; sub-session numbering, D-126);
  - `cb0145e` (the benchmark, the architecture, the prototype, its checks; the HBM page's digest);
  - and the commit that adds this report, its QA and breaks, and the state rows.

## Mission outcome

**Delivered.** The repository now has a defensible answer to the acceptance question: what an Atlas
research experience should look and behave like, and how it stays traceable to the evidence and the
SQL layer. One generated prototype shows the answer working on the HBM slice.

- **Benchmark** ([`docs/research/visual-benchmark-S14.5.md`](../../docs/research/visual-benchmark-S14.5.md),
  D-122): Epoch AI, Our World in Data, IEA, the Stanford AI Index and Datawrapper, each across the
  fourteen dimensions. The pages were observed in a headless browser at 1440 and 390 px; IEA was
  read through its published report, because its website refuses automated access. 29 patterns are
  classified: 6 ADOPT, 15 ADAPT (4 of them deferred to S15–S21), 8 REJECT.
- **Architecture** ([`docs/architecture/visual-architecture.md`](../../docs/architecture/visual-architecture.md),
  D-123, D-124):
  - the seven-layer model `QUESTION → INSIGHT → VISUAL → EXPLORE → EVIDENCE → DATA → METHOD`, each
    layer with its source and its check;
  - 11 visual principles and 8 analytical UX principles;
  - the minimal design system (the S11 palette's tokens named by job, the line and mark vocabulary,
    type, space, numbers, words);
  - the information architecture proposed for S20;
  - the component inventory;
  - the grammar for the eight forms;
  - evidence-aware semantics;
  - the rules for visual vs table vs text;
  - the SQL-to-visual binding rule;
  - the boundary with S15–S16 and S20.
- **Prototype** ([`site/hbm-insight/index.html`](../../site/hbm-insight/index.html), D-125): generated
  by `tools/build_insight.py` from the S14 result and the records, checked by `tests/test_insight.py`
  (18 tests), browser-tested at 1280 and 375 px. The HBM page and its build are unchanged apart from
  the HBM page's input digest (Deviations, 3).

**Decided by the human** (2026-10-06; outcomes only, D-114):

| Decision point | Outcome | Effect |
|---|---|---|
| Whether the prototype's indicator blocks may show counts before S15 defines metrics | counts of the links the page draws, each with its denominator in the same block | D-124's tally rule; the four indicator blocks |

## Files changed

| File | Change |
|---|---|
| `docs/research/visual-benchmark-S14.5.md` | new: method, five benchmarks × fourteen dimensions, the pattern register P-01 to P-29 (proposed) |
| `docs/architecture/visual-architecture.md` | new: the architecture (proposed) |
| `docs/architecture/decisions.md` | D-122 to D-126 appended (proposed) |
| `tools/build_insight.py` | new: the prototype build (standard library; subclass of `build_page.Page`) |
| `tools/insight_template.html` | new: framing and the component styles; the base style is read from `tools/page_template.html` |
| `site/hbm-insight/index.html` | new, generated (92,526 bytes) |
| `site/hbm-chain/index.html` | rebuilt: its input digest only (`decisions.md` is an input) |
| `tests/test_insight.py` | new: IN-1 to IN-9 and four build refusals |
| `tools/validate_repo.py`, `tests/test_validate_repo.py` | session numbers may carry a one-digit suffix (D-126); two tests |
| `sessions/prompts/S14.5-PROMPT.md`, `sessions/prompts/PROMPT-REGISTRY.md` | the prompt, verbatim, and its registry row |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows; NG-11's proposed exception noted beside it |
| `sessions/reports/SESSION-14.5-qa/` | browser QA script, results, ten screenshots, the fail-first output |
| `sessions/reports/SESSION-14.5-breaks/` | the break script, its first run and its final run |
| `sessions/reports/SESSION-14.5-REPORT.md` | this report |

`Eu-Digital-Policy`: not touched. No dependency added.

## Data changed

**None.** No source, claim, entity, event, relationship, refused-candidate or identity-basis record
was created or edited. The SQL result was not changed (`results: up to date`). The prototype reads
the existing result and records only.

## Tests run

| Command / check | Result |
|---|---|
| **At start** (`2a6e91c`), fresh Python 3.11 venv, both pin files | OK (328 tests); Gate 0 OK; page and results up to date |
| `tests/test_insight.py` **fail-first** (page not built) | 15 of 18 fail ([`failfirst.txt`](./SESSION-14.5-qa/failfirst.txt)): 14 "the page is not built"; the slot refusal raised for another reason (below) |
| First build | **refused**: "row 4: the dependency journey page has no panel ev-claim-h100-process-name" (below) |
| `tests/test_validate_repo.py` **fail-first** | the S14.5 pairing test failed before the validator change; 12 OK after |
| **Final**, same venv | OK (348 tests); Gate 0 OK; `results: up to date`; both pages `up to date` |
| **CI** | the first two S14.5 commits were pushed before this report; their runs were not observed at writing |

**What the first build caught.** The recorded gap TSMC → H100 (`cand-001`) considered two claims:
`claim-h100-process-name` and `claim-tsmc-fabricates-h100`. The first draft linked the gap's mark to
the first listed claim. The HBM page holds a panel only for the second, the inference. Because the
build checks every evidence link against the HBM page's anchors, it refused to write the page. The
link now opens the first considered claim that has a panel, and IN-5 checks the same rule
independently. The same fault in the test's first draft made the "two rows in one slot" refusal test
fail for the wrong reason during fail-first; both were corrected together.

### Deliberate breaks

Each break copies the repository (without `.git`) into a scratch folder and makes one edit. It rebuilds
where stated, runs the full suite, and counts only if the suite fails with the named fragment in its
output. A control counts only if the suite passes. Script:
[`insight_breaks.py`](./SESSION-14.5-breaks/insight_breaks.py).

**Result on the final state** ([`insight-breaks-result.txt`](./SESSION-14.5-breaks/insight-breaks-result.txt)):
13 of 13 caught; both controls pass.

| # | Break | Caught by |
|---|---|---|
| T1 | a tally hand-edited on the page (H100: 1 of 4 stated → 2 of 4) | IN-3 (recomputed), IN-8 |
| T2 | a tally's denominator removed from its block | IN-3 "a tally whose denominator is not in the same block" |
| T3 | the build computes a share beside a tally (rebuilt) | IN-3 "a derived value the checks do not recompute" |
| V1 | a strip line drawn as stated when its row is inferred | IN-4 "the line style does not follow the basis" |
| V2 | a gap's reason dropped from the marks (rebuilt) | IN-4 "a gap without its reason in words" |
| V3 | a unit square opens the wrong row | IN-5 |
| E1 | an evidence link to a panel the HBM page does not have | IN-5 |
| F1 | framing names a record (rebuilt) | IN-6 "framing names a record (NVIDIA)" |
| S1 | a colour outside the palette (rebuilt) | IN-7 |
| S2 | the filter fades instead of outlining (rebuilt) | IN-7 "fading lowers contrast" |
| L1 | a label in the headline hand-edited ("each" → "both") | IN-1 |
| D1 | data changed (a display name), results and HBM page rebuilt, prototype not | IN-2 (16 failures), IN-8 |
| D2 | a decision appended, HBM page rebuilt, prototype not | IN-8 (the prototype's input digest) |
| C1, C2 | controls: a framing sentence reworded and rebuilt; a display name changed and everything rebuilt in order | pass |

**The first run** ([`insight-breaks-first-run.txt`](./SESSION-14.5-breaks/insight-breaks-first-run.txt)) found one
invalid break. V2 deleted a line and left an empty `if` block, so the build died of a syntax error
and the named check never ran: "NOT CAUGHT as named", correctly. V2 now replaces the reason with
nothing, and is caught for its named reason.

## Browser QA (D-106)

Playwright from `/opt/node-tools` with the pre-installed Chromium ([`qa.js`](./SESSION-14.5-qa/qa.js),
[`qa-result.json`](./SESSION-14.5-qa/qa-result.json)).

| Check | 1280 px | 375 px |
|---|---|---|
| Console messages, page errors, network | none, none, the page file only | same |
| Document overflow; wide elements (also with every disclosure open) | 1280 / 1280; none | 375 / 375; none |
| Marks reached by Tab (8 strip marks, 8 unit squares) | 16 of 16 in 22 presses | same |
| Focus ring on a strip mark | solid 3 px | same |
| Enter on each unit square lands on its table row (`:target`) | 8 of 8 | 8 of 8 |
| Basis filter from the keyboard (arrow keys): rows kept, marks outlined | stated 3 rows / 6 marks; inferred 2 / 4; gap 3 / 6, each matching its basis; back to "all links": nothing hidden | same |
| Measured contrast, every text node (tutorial open) | min 6.21:1 over 524 nodes; none below 4.5 | min 6.21:1 over 580 nodes |

Two defects were found by looking at the page and fixed before the final run:

- the reading note said "left to right", which is false on a phone, where the chains run top to
  bottom;
- the comparison repeated words: a slot title "It incorporates" was followed by the relation word,
  and the supplier's state was said twice.

Screenshots: [`desktop-02-insight.png`](./SESSION-14.5-qa/desktop-02-insight.png),
[`desktop-03-chains.png`](./SESSION-14.5-qa/desktop-03-chains.png),
[`mobile-03-chains.png`](./SESSION-14.5-qa/mobile-03-chains.png),
[`desktop-04-filter-gap.png`](./SESSION-14.5-qa/desktop-04-filter-gap.png).

## Benchmark findings, in short

- **Common to all five:**
  - the finding comes before the chart;
  - unit, period and scope sit in the subtitle;
  - a source line sits under the chart, and the method is one step away;
  - a table sits beside the chart;
  - uncertainty is said in words near the number.
- **Strongest single lessons:**
  - Our World in Data's chart, table and sources as three views of one indicator on one URL;
  - Epoch AI's "Assumptions and limitations" disclosure under every insight, and its observed /
    projected regions labelled on the chart;
  - IEA's figure that draws every competing estimate with its own highlighted;
  - Datawrapper's "title states the takeaway, description holds the precision".
- **Rejected:**
  - the pictorial supply chain (IEA Figure 1.9: arrows with no records behind them);
  - takeaway paragraphs that fuse measurements with interpretation (AI Index);
  - canvas charts (opaque to checks);
  - brand colour as emphasis;
  - decorative dataset art;
  - video;
  - fallback descriptions that only count symbols;
  - mode switches before a metric exists.
- **What none of them shows and the Atlas must:**
  - the basis of each mark (stated, inferred, gap);
  - the unknown as a mark;
  - claim-level provenance from any mark.

The register (P-01 to P-29) is in the benchmark document, Part 3.

## Visual principles, UX architecture and components (summary)

See `visual-architecture.md` for the full text. The decisions that matter most:

- **Seven layers, one result.** The headline, the comparison, the indicators, the chains and the
  table on the prototype all render the same eight rows of the S14 result. Every SQL cell carries its
  row and column, and the checks compare it with the file.
- **The build renders; it does not compute new facts** (D-124). It may copy cells, tally drawn rows
  over a printed denominator, take a first and last date, and group rows by position. A share,
  ratio or concentration is a metric, owned by S15 as a SQL column with its tutorial.
- **The amber is reserved for gaps.** "No recorded relationship" is drawn neutral: the most
  important visual distinction the system makes (an unknown the Atlas recorded vs no record at all).
- **Components:**
  - built and checked: the question and scope line, the composed headline, the derived comparison,
    the indicator block, the unit strip, the chain strip, the reading note, the basis filter, the
    evidence index, the analytical table, the SQL tutorial, the method block;
  - proposed for S15 and S20: the ranking, the timeline, the map, the comparison matrix, the
    question card.

## Prototype decisions

| Decision | Why |
|---|---|
| A second page, not a change to the HBM page | the prompt forbids replacing the product; the HBM page's rules are accepted |
| Chain strips in HTML and CSS grid, not SVG | text wraps; at phone width the same markup becomes a vertical chain; the checks read every word |
| Aligned small multiples (one strip per accelerator) | the comparison the question implies (what differs between the two chains) is read across aligned columns |
| The headline composed from cells, the question as fallback | V-2: no free-prose finding; the build switches to the question when the rows stop supporting one sentence |
| "In common" and "Where they differ" derived by position | U-2; recomputed by IN-3. Today: the part, its maker and its process are shared; what acts on each accelerator differs (Amazon `designs`, stated; TSMC `fabricates`, a gap) |
| Four indicator blocks: a state, a tally per accelerator, a date range, a publisher range | the human's decision; each block prints its denominator, and one says that 8 rows show 5 records |
| Evidence links open the HBM page's panels | one evidence home; the build refuses a link with no panel |
| A CSS `:has()` filter | no script; without `:has()` everything stays shown |
| The base stylesheet read from the S11 template | one palette and one base stylesheet |

## Prototype validation

| Criterion | Verdict | Evidence |
|---|---|---|
| **Truth** | **met, with one limit** | Every cell equals its result cell (IN-2). Every tally, range and comparison is recomputed independently (IN-3). Every mark's line style and words follow its row (IN-4). The build refused a wrong evidence link before it could be drawn. The breaks plant each kind of untruth and are caught. **Limit:** the "Evidence dated" block's latest date (2026-10-01) is an access date: Trainium2's HBM page states no date of its own. The block says in general that "an undated web page is dated by the day it was read", but the result has no column saying which row's date is an access date, so the page cannot flag that row (debt, owner S15) |
| **Clarity** | **met on the checks this session can run; the reader test is open** | The question is answered in the headline. The single difference between the chains is listed first under "Where they differ". The strips align by column on desktop. Not yet tested with a reader who did not build it: that is the human's reading at the review |
| **Context** | **met** | The scope line names the population and the evidence dates. Every count has its denominator (IN-3), every mark its basis in words, every gap its reason. The table keeps every caveat flag. "Dates, not ages" is said in the dates block and the table framing |
| **Presentation** | **met** | Browser QA above: no overflow at 375 px, keyboard path complete, filter correct, contrast at least 6.21:1, no console or network activity |
| **Architecture** | **met** | IN-8: the page is a byte-identical rebuild of its inputs. No presentation data file exists. The build refuses rows its specification does not fit (four refusal tests) |

## Evidence added/retired

None. The benchmark pages and the IEA report were read as design references. They are not Atlas
sources, are not registered in `data/sources.json`, and back no claim.

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-122 | the visual benchmark and its pattern register | proposed |
| D-123 | the research-experience model, the principles and the minimal design system | proposed |
| D-124 | the SQL-to-visual binding rule; tallies of drawn rows with their denominators | proposed (tallies decided by the human on 2026-10-06) |
| D-125 | the prototype: build, page, checks, build order | proposed |
| D-126 | sub-session numbering (S14.5) in the validator | proposed |

**Rejected alternatives** (detailed in the decisions and in `visual-architecture.md` §14):

- a charting library;
- JavaScript;
- hover tooltips;
- redesigning the HBM page;
- a component library now;
- a presentation data file;
- percentages;
- any score, traffic light or confidence bar;
- a map of two facilities;
- dark mode;
- a copied stylesheet;
- repeated evidence panels;
- renumbering later sessions.

## Deviations

1. **The prompt has no Part B.** The human gave the contract directly and inserted the session
   between S14 and S15. It is recorded verbatim, with a provenance note, and no
   `SESSION-PROMPT-SPEC.md` §2 elaboration was written.
2. **`tools/validate_repo.py` and its test changed** (D-126), so the session's prompt and report could
   be recorded under its own number. Nothing else in Gate 0 changed.
3. **The HBM page was rebuilt.** Its input digest changed because `decisions.md`, one of its
   inputs, gained D-122 to D-126. A byte diff shows the digest line is the only change.
4. **IEA's website was not observed** (403 for automated clients; the archive was unreachable through
   the proxy). IEA is assessed from its *Energy and AI* report only, and the gap is stated in the
   benchmark's method.
5. **Break V2's first form failed for the wrong reason** (a syntax error, not the named check). The
   break was corrected and re-run (Deliberate breaks).
6. **Deviations from the existing architecture:**
   - the prototype's visual is HTML, not SVG (D-103 used SVG). The grammar allows both, and chooses
     by what the form needs;
   - NG-11 gains a proposed, bounded exception: tallies of drawn rows (D-124);
   - `tools/page_template.html` becomes an input of a second page, as the stylesheet's one home;
   - the HBM page becomes an input of the prototype (its anchors), which fixes a build order.

**Invalidated assumptions:**

- "S14 found every row has one publisher" (`sql-layer.md` §7). True of the stated rows, but the two
  inferred rows rest on two publishers each (IEEE EPS and Sandia, for two steps of one reasoning).
  The prototype says "1 to 2" and "4 of 6 sourced rows rest on one publisher". The S14 table's
  caveat flag was always correct; only the summary sentence in `sql-layer.md` §7 overstates. It is
  left unedited, because that document is accepted (debt below).
- "8 links" is not "8 records": the 8 rows show 5 records, because the shared `requires` edge appears
  under both accelerators and each unknown supplier sits on its own `incorporates` edge. S15's first
  metric must choose rows or records explicitly.

## Debt introduced/resolved

**Introduced:**

| Item | Owner |
|---|---|
| The result has no column saying when an evidence date is an access date, so the prototype cannot flag that row ("2026-10-01" reads as recent evidence) | S15, as a column of its first query or a revision of D-120 |
| `sql-layer.md` §7 says every row today has one publisher; the inferred rows have two | the S15 opening, as a status-line correction proposed to the human |
| Three break harnesses (`SESSION-13-breaks`, `SESSION-14-breaks`, `SESSION-14.5-breaks`) | the next session that changes a page, to merge them |
| `build_page.sql_section` reads the result from its fixed path; the prototype checks that its own result is that file instead of passing it in | the third composition (MA §16.1), when shared rendering is extracted |
| Count words do not agree in number ("1 of 1 links" would print if an accelerator had one row) | the third composition |
| The filter needs `:has()`; without it, nothing is filtered and no message says so | S20 |
| The prototype has not been read by someone who did not build it | the S14.5 review (the human's reading) |

**Explicitly avoided:**

- no library, framework or script;
- no new data;
- no copy of the stylesheet or the evidence panels;
- no presentation data file;
- no component library;
- no change to `tools/build_page.py`.

**Resolved:** none of the inherited debt (not in scope). DT-3 (ID stability) now also blocks
publishing the question pages of §4 (noted in `visual-architecture.md` §4).

## Unresolved issues

**Human decision required: should the S14.5 architecture and prototype become binding for S15 and
later pages?**

- *What we are deciding:* whether the five S14.5 decisions, the benchmark document and the visual
  architecture document move from "proposed" to "accepted".
- *What each one fixes:*
  - **D-122 (the benchmark):** the 29 classified patterns become the Atlas's recorded reading of the
    five products. Later sessions cite it, rather than re-benchmark.
  - **D-123 (the model and the design system):**
    - every future research page follows the seven layers;
    - the amber is used for gaps only;
    - "no recorded relationship" is drawn neutral;
    - counts always print their denominator;
    - no hover-only values, no web fonts, no scripts without a question that needs them.
  - **D-124 (the binding rule):** a page may only copy result cells, tally the rows it draws, take
    first and last values, and group rows. Any other number must be a SQL query with its tutorial,
    which is S15's work. Tallies of drawn rows become a standing, bounded exception to NG-11.
  - **D-125 (the prototype):** `site/hbm-insight/index.html` stays as a generated, checked,
    unpublished page, built after the HBM page. Its 18 checks run in CI.
  - **D-126 (numbering):** session files may be numbered like `S14.5`.
- *What will concretely change:* if accepted, only status lines change in `decisions.md`,
  `visual-architecture.md` and `visual-benchmark-S14.5.md`. Both pages' digest lines follow, because
  `decisions.md` is their input. No data, result, check or page content changes.
- *Why:* S15 will present its first metric. Accepting the rules means it presents the metric through
  this grammar and binding rule, instead of re-deciding them.
- *What stays the same:* the HBM page, the SQL layer, all data.
- *Future consequences:* S15 and S20 inherit the rules; changing them later needs a superseding
  decision. Dropping D-124 would remove the tallies from the prototype and leave NG-11 as it was.
- *Options:*
  - **A, all five binding as built:** status lines only.
  - **B, named items changed first:** Claude rewrites the named items, and the page and checks they
    affect, before acceptance.
  - **C, named items dropped:** what depends on them is removed or rebuilt. For example, dropping
    D-125 deletes the prototype, its build and its checks; dropping D-124 removes the four indicator
    blocks' counts.
- *Decision requested:* "Choose A, B or C, naming items for B or C."
- *Technical reference:* D-122 to D-126; `docs/architecture/visual-architecture.md`;
  `docs/research/visual-benchmark-S14.5.md`.

**Open questions for later sessions (no decision needed now):**

- whether browser checks join CI once a second page exists (D-106's alternative); a second page now
  exists;
- whether to replace the prototype's tallies with SQL columns (S15) or keep them as presentation;
- whether the HBM page should eventually adopt the seven layers (S20).

**Inherited, unchanged:** the S14 report's list (D-092, D-094, D-093/DT-6, D-095, S01's weekly gate,
evidence ageing DT-S13-4, the S13 debt register, S12's unscripted breaks).

**Not asked now:** merging this branch to `main`; public deployment (NG-13).

## Process lessons

- **A refusal in the build is a check that runs before the page exists.** Checking every evidence link
  against the target page's anchors found a wrong link on the first build, before any test ran.
- **A break must fail for the reason it names.** V2's first form produced a syntax error. It was
  counted as not caught, because the named fragment was missing, and it was fixed. The harness rule
  inherited from S14 did its job.
- **Looking at the page finds what the checks cannot.** Both presentation defects (an
  orientation word false on phones, repeated words) passed every check.
- **A rows-vs-records count is a truth issue, not a style issue.** "8 links" would have been true of
  rows and false of records. The indicator now says both.

## Implications for the next session

**For S15 (dependency metrics):**

- a metric arrives as a query in `sql/`, with its tutorial (D-115, D-121) and its result. It is shown
  through the grammar of `visual-architecture.md` §7, with its denominator in the same block (D-124);
- the prototype's tallies (links on stated evidence per accelerator; publishers per sourced row; rows
  with nothing to date) are candidates S15 may keep, move into SQL, or retire;
- choose the population explicitly: rows (accelerator × link) or records (edges and candidates). The
  two differ today (8 vs 5);
- add the evidence-date basis (as_of / stated date / access date) as a column, so a page can flag an
  access date on its row;
- no mode switch, share or ranking before its question and denominator are defined (P-19, NG-11);
- competing values are drawn side by side, never averaged (P-08).

**For S20 (researcher UX):**

- the information architecture of `visual-architecture.md` §4 (questions, profiles, one evidence
  home, data and method pages);
- question cards (P-16);
- the component inventory of §6;
- DT-3 (ID stability) before any page is published;
- browser checks in CI;
- the `:has()` fallback.

**Files for S15 to read first:**

- this report;
- [`docs/architecture/visual-architecture.md`](../../docs/architecture/visual-architecture.md) §7, §10
  and §11;
- [`docs/architecture/sql-layer.md`](../../docs/architecture/sql-layer.md) §9.

**Next recommended milestone:** S15, the first metric on the SQL layer, with its question,
population and denominator decided before any SQL is written, and presented through D-124's binding
rule.
