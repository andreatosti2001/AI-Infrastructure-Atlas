# SESSION-16 Report — Analytical audit

- **Session:** S16 · **Type:** AUDIT · **Milestone:** M4 — Analytical Intelligence (its last session)
- **Date:** 2026-10-07
- **Prompt:** [`sessions/prompts/S16-PROMPT.md`](../prompts/S16-PROMPT.md), saved unchanged at the opening.
  - Part A was assembled by Claude from S15's Part A and the operational roadmap's S16 entry.
  - The human confirmed it as written on 2026-10-07.
- **Branch:** `claude/new-session-u2e1xq`, at `main` @ `1ca2e89` (the PR #27 merge, which carries S15).
- **Base** (D-018 L-03), at the start:
  - `git branch -a`: this branch and `main`, with their remotes, at `1ca2e89`;
  - `git ls-remote`: `HEAD` and `main` at `1ca2e89`; `claude/magical-maxwell-qar167` at `521a188`;
    `claude/new-session-4kuwvw` at `2759111`; `claude/new-session-f8y32i` at `36c44a5`;
  - in a fresh Python 3.11 virtualenv built from both pin files: 357 tests OK, `Repository integrity: OK`,
    results and both pages up to date. Data: 52 sources, 120 claims, 4 events, 5 relationships; staging
    empty.
- **Commits:**
  - `a42bf24`: the prompt, the cold-reading form and the reader's input;
  - `ad8159e`: the sensitivity probes;
  - `4d341ad`: the reproduction;
  - `9882971`: the audit and its audit-history row;
  - `dc210b2`: the remediation;
  - and the commit that adds the break harness, the QA, this report and the state rows.

## Mission outcome

**Delivered.** Each of the five metrics was audited:

- read cold by two unprimed readers;
- reproduced from `data/` and its plain definition;
- moved by seven planted changes.

The audit then put each metric to the human, who approved, modified or retired each one on 2026-10-07.

| Metric | What the audit found | Outcome (D-133 to D-136) |
|---|---|---|
| Evidence coverage | Correct counts. Neither reader understood the records line. Someone with only the plain definition got the H100 wrong (5 links, not 4) | **modified:** the records line and the population line reworded; numbers unchanged |
| Source age | Correct dates, but the 12-month horizon was applied to every link, and the tutorial stated the source policy's re-check rule wrongly: the policy applies it only to time-sensitive links. 4 of the 5 "older" links are stable | **modified:** the block's note and the tutorial say where the horizon applies; the reference date moved to 2026-10-07 (D-137) |
| Publishers behind a sourced link | Its only "2" was one inferred link's two reasoning steps. It counted 6 rows from 5 records unsaid, and computed a per-row count the page never shows (outside D-124) | **retired**; the table's per-row "one publisher only" flags stay |
| Supplier count, geographic concentration, single-source | Read correctly by both readers as unknown, not zero | **kept as built** |

**The audit in one sentence** (`INTERPRETATION`): the Atlas's metrics answer real questions over stated
populations and are reproducible from their queries. Three defects were found: a rule misapplied, a block
outside the page rule, and two definitions too thin to reproduce from. All three were wording or removal,
and none changed a number.

**Decided by the human** (2026-10-07; outcomes only, D-114):

| Decision point | Outcome | Effect |
|---|---|---|
| Part A | confirmed as written | prompt saved unchanged |
| H-1, the audit's reach | the metrics, their presentation, D-130 and D-124 as applied | one audit file; no milestone audits (put again below) |
| H-2, the cold readers | the human and a fresh agent | the human then waived their own reading; a second fresh agent read instead (Deviations) |
| H-3, each metric | coverage modified (D-133), source age modified (D-134), publishers retired (D-135), supplier metrics kept (D-136) | below |
| H-3, the findings | five remediated, six debt with owners (D-138) | below |
| H-4, the reference date | moves with each session that rebuilds the pages, to its opening day (D-137) | set to 2026-10-07 |
| The HBM supplier gap | researched by Claude in its own session, S16.5, before S17 (D-139) | the policy layer moves back one slot; the human approves each new supplier link before it is canonical |

## Files changed

| File | Change |
|---|---|
| `sessions/prompts/S16-PROMPT.md` | new: the prompt as confirmed |
| `docs/architecture/analytical-audit-S16.md` | new: the audit |
| `docs/quality/audit-history.md` | one row |
| `sql/evidence_coverage.sql` | the population line (D-133) |
| `sql/source_age.sql` | the question, assumptions, does-not-prove and one step's text (D-134); the reference date 2026-10-07 (D-137) |
| `sql/results/evidence_coverage.json`, `sql/results/source_age.json` | rebuilt (query digests; ages and reference date) |
| `tools/build_insight.py` | the records line; the age note; the publishers block removed; labels |
| `site/hbm-insight/index.html`, `site/hbm-chain/index.html` | rebuilt. The HBM page changed only in its digest lines, since `decisions.md` and the queries are inputs |
| `tests/test_insight.py` | IN-12 (three checks); IN-3 no longer recomputes the retired tallies |
| `tests/test_warehouse.py` | WH-15; WH-13 moves whatever reference date the query holds |
| `docs/architecture/decisions.md` | D-133 to D-138 appended |
| `docs/architecture/metrics.md` | the S16 status lines; §4's reference date and horizon; §6 publishers marked retired; §7 placement |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows |
| `sessions/reports/SESSION-16-cold-reading/` | the form, the reader's input (page with tutorials removed, screenshots, text), both readers' answers |
| `sessions/reports/SESSION-16-reproduction/` | the definitions given, the reproducer's script and output |
| `sessions/reports/SESSION-16-probes/` | the probe script and output |
| `sessions/reports/SESSION-16-breaks/` | the merged harness with S16's breaks, and its full run |
| `sessions/reports/SESSION-16-qa/` | fail-first output, final checks, browser QA for both pages |

`Eu-Digital-Policy`: not touched. No dependency added. `sql/accelerator_dependencies.sql`: not touched.

## Data changed

**None.** No record in `data/` was created or edited. The probes planted hypothetical values in scratch
copies only, among them a placeholder supplier id that names no company. They were never committed as data.

## Tests run

| Command / check | Result |
|---|---|
| **At start** (`1ca2e89`), fresh Python 3.11 venv | OK (357 tests); Gate 0 OK; results and both pages up to date |
| **Fail-first** (checks written, nothing else changed) | 6 failures, each with its named reason ([`failfirst.txt`](./SESSION-16-qa/failfirst.txt)): the three IN-12 checks, IN-3 (the retired kinds), WH-15 |
| **Final**, a second fresh venv | OK (361 tests); Gate 0 OK; `results: up to date`; both pages `up to date` ([`final-checks.txt`](./SESSION-16-qa/final-checks.txt)) |
| **Merged break harness**, run in full on `dc210b2` (the remediated tree) | **74 of 74 faults caught as named; 9 of 9 controls pass** ([`merged-breaks-full-run.txt`](./SESSION-16-breaks/merged-breaks-full-run.txt)) |
| **CI** | <CI> |

### Deliberate breaks

[`breaks.py`](./SESSION-16-breaks/breaks.py) loads S15's merged harness (74 breaks), replaces S15-M3, and
adds 9 S16 breaks, for 83 in total:

- **S15-M3 replaced:** its setup moved the literal 2026-10-06, which D-137 moved. It is the same fault
  on 2026-10-07.
- **The 9 S16 breaks:**
  - one per remediation and per new check (A1 to A7);
  - two controls: the reference date moved one day and rebuilt (D-137's move must need only a rebuild),
    and coverage's population reworded with what WH-15 requires kept.

| Break | Fault | Caught by |
|---|---|---|
| S16-A1 | the retired publishers block put back by the build | IN-12: "a retired publishers tally is back" |
| S16-A2 | a row's "one publisher only" flag removed by hand | IN-12: "a row on one publisher lost its flag" |
| S16-A3 | the old records line put back | IN-12: "the records line readers did not understand is back" |
| S16-A4 | the records count typed instead of copied from its cell | IN-12: "a records count typed, not copied from its cell" |
| S16-A5 | the age note back to "Dates, not ages" | IN-12: the horizon note missing |
| S16-A6 | the tutorial states the old, wrong rule | WH-15: "the old, wrong statement of the rule is back" |
| S16-A7 | coverage's population loses the refused-relations sentence | WH-15: "coverage's population does not say which refused relations are rows" |
| S16-C1 | control: the reference date moved one day, everything rebuilt | passes |
| S16-C2 | control: coverage's population reworded, keeping what WH-15 requires | passes |

All 83 setups applied on the remediated tree, and none was stale apart from S15-M3, which was replaced.
After the run, only `decisions.md` (D-139), documentation and the pages' digest lines changed. The suite
and Gate 0 were re-run on that final tree (below).

## Browser QA (D-106)

Playwright from `/opt/node-tools`, with the pre-installed Chromium, on the final pages:

- the research view: S15's [`qa.js`](./SESSION-16-qa/qa.js), unchanged;
- the HBM page: S14's script, unchanged.

| Check | Research view, 1280 / 375 px | HBM page, 1280 / 375 px |
|---|---|---|
| Console, page errors, network | none, none, the page file only | none, none, the page file only |
| Document overflow; wide elements, also with every disclosure open | none / none | none / none |
| Marks reached by Tab | 16 of 16 | 17 of 17; Enter lands on every panel |
| Tutorials open by keyboard; each metric block's link resolves | 4 of 4; 5 of 5 links | 1 of 1 |
| Basis filter from the keyboard | correct for each basis | — |
| Measured contrast, every text node | min 6.21:1 over 793 / 897 nodes; none below 4.5 | min 6.21:1; none below 4.5 |

Screenshots: [`hbm-insight/desktop-02-insight.png`](./SESSION-16-qa/hbm-insight/desktop-02-insight.png),
[`hbm-insight/mobile-02-insight.png`](./SESSION-16-qa/hbm-insight/mobile-02-insight.png),
[`hbm-insight/desktop-06-method-tutorials-open.png`](./SESSION-16-qa/hbm-insight/desktop-06-method-tutorials-open.png).
With the publishers block gone, the indicator row holds two blocks, and the layout reflows without overflow
at both widths.

## The audit's evidence, in short

The full answers per metric, the PEF §8 rechecks and the maturity ratings are in
[`analytical-audit-S16.md`](../../docs/architecture/analytical-audit-S16.md).

**Cold readings** (two fresh agents, each given only the page without its tutorials):

- every supplier block, and the overall comparison, **matched** its intent for both readers. Both said
  the differences between the chips "reflect how far the Atlas's research has got";
- **differed or unclear:**
  - coverage's records line (both);
  - "gap" covering stale evidence (both);
  - the horizon applied to every link (reader 2's question was the audit's finding);
  - the publishers block (reader 2 could not act on it).

**Reproduction** (from `data/` and the question, population and denominator lines only):

- Trainium2 equal, for coverage and age; the supplier metrics equal;
- the H100 differed: 5 links and 4 dated links, because "NVIDIA designs H100" (refused for another
  reason) was counted. The definition did not say only stale-evidence refusals are rows. It now does
  (D-133).

**Sensitivity** (seven planted changes in scratch copies):

- one shared record re-typed moves both accelerators at once (P1);
- one publication date makes Trainium2's age tally equal the H100's (P3);
- a one-day move of the reference date changes only the date (P5);
- resolving the H100's recorded gap stops both builds (P2, debt E-1);
- naming a supplier stops both builds with named reasons, as designed (P7).

## Evidence added/retired

None. No source was retrieved. The audit's findings are `INTERPRETATION`s about the Atlas's own metrics.

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-133 | evidence coverage kept; records line and population reworded | accepted (H-3, 2026-10-07) |
| D-134 | source age kept; the horizon applies only to time-sensitive links | accepted (H-3, 2026-10-07) |
| D-135 | the publishers tally retired | accepted (H-3, 2026-10-07) |
| D-136 | the three supplier metrics kept as built | accepted (H-3, 2026-10-07) |
| D-137 | the reference date moves with each session that rebuilds the pages | accepted (H-4, 2026-10-07) |
| D-138 | the findings: five remediated, six debt with owners | accepted (H-3, 2026-10-07) |
| D-139 | a research session on the HBM suppliers (S16.5) precedes S17 | accepted (decided by the human, 2026-10-07) |

**Rejected alternatives:**

- Claude answering the cold-reading form, after the human waived theirs: Claude had read the queries, so
  its reading would not be cold;
- giving the reproducer more than the three definition lines;
- fixing C-2 (what "gap" means) or C-9 (unlike links) in S16, since both need the first query or new
  research;
- a time-sensitivity column in the age query;
- merging the three supplier blocks;
- keeping the publishers block, reworded;
- moving the reference date only in audits, or only when asked.

## Deviations

1. **The human's cold reading was waived** (2026-10-07: "Answer yourself"). Part B §07 task 2 under H-2 A
   asks for the human's and a fresh agent's readings.
   - A second fresh agent read instead, from the mobile screenshots, without the first reader's answers.
     Two independent unprimed readings were kept.
   - Acceptance criterion 3 ("the readers H-2 names") is therefore met by two agents, not by the human.
     S15's lesson that a person's reading can differ from a model's is not tested here.
2. **The first reader's answers were held outside the repository** until the human's reading was settled,
   so the human could not meet them in the repository first. They were committed with the audit.
3. **The probe script's first run crashed the HBM page build.** The cause was the probe's own planted
   citation standing (`independent`, not a schema value). The probe was corrected and re-run. The crash
   is recorded as E-2: the build gives no named reason for an invalid value.
4. **WH-13 changed.** It moved the literal 2026-10-06, which D-137 makes a moving date. It now moves
   whatever date the query holds by one year. That is equally strict, and its expectations are unchanged.

**Invalidated assumptions:**

- "Source age's horizon is the source policy's horizon" (S15's `metrics.md` §4): it is, but the policy
  applies it only to time-sensitive links.
- "The publishers count is a tally of drawn rows within D-124" (S15): its range was a per-row count the
  page computed.
- "The plain definition is enough to reproduce coverage" (Part B §06 q4): it was not, for the H100.

## Debt introduced/resolved

**Resolved:**

- the reference date's owner (S15's debt row, H-4): D-137;
- S15's two questions left to S16: the publishers count (audited, retired) and merging the supplier
  blocks (considered, not taken).

**Introduced or re-owned** (D-138):

| Item | Owner |
|---|---|
| C-2: "gap" mixes not researched with refused as stale | S20 (the researcher product); a change needs a superseding decision on the first query |
| C-5: the H100's age tally includes its recorded gap | S20 |
| C-8: `src-043` carries two access dates for the same bytes | S22 |
| C-9: the two accelerators' links are not the same kinds | the session that next adds accelerator links |
| E-1: resolving a recorded gap stops both builds (`cand-001` configured by id) | S22 |
| E-2: an invalid citation standing crashes the HBM page build with no named reason | S22 |

**Carried, unchanged:**

| Item | Owner |
|---|---|
| A supplier metric's presentation once a supplier is named | S16.5, which adds the first supplier evidence (D-139) |
| DT-S13-4 beyond the page's chain | Change Detector (inactive) |
| `build_page.sql_section`'s fixed result path | S22 |
| The research view's filter needs `:has()` | S20 |

## Unresolved issues

**Human decision required: should the missing milestone reviews for milestones 3 and 4 be written, and
when?**

- **What we are deciding:** whether the two milestone reviews that the evaluation framework requires, and
  the repository lacks, are written, and in which session.
  - The framework requires a review at every major milestone.
  - Milestone 3 (sessions 11 to 13: the first end-to-end page and its two audits) has none.
  - Milestone 4 (sessions 14 to 16: the SQL layer, the research view, the metrics and this audit) closes
    with this session and has none either.
- **What will concretely change:**
  - **If written,** one or two new files under `docs/architecture/milestone-audits/`, plus a row each in
    `docs/quality/audit-history.md`. Each answers the framework's eight questions: what was intended, what
    was built, what changed, which assumptions failed, which shortcuts were taken, what debt was created,
    what was rejected, what carries forward.
  - No data, query, page or check changes.
- **Why:** without them, the two milestones' shortcuts and failed assumptions are recorded only scattered
  across session reports. For example:
  - M3's late discovery that the page counted rows, not records;
  - M4's freshness horizon misapplied until this audit.
- **What stays the same:** S16's metric verdicts, the pages and the data.
- **Options:**
  - **A, both written in S16.5's opening, before its research starts (recommended).** M4 closes with a
    full record before more evidence and M5 build on it. The research starts somewhat later.
  - **B, both written as a short separate session after S16.5.** Keeps S16.5 a pure research session,
    at the cost of one more session before S17.
  - **C, not written; the session reports stand as the record.** No extra work. The framework's
    milestone requirement stays unmet for M3 and M4, and S22 or S24 would have to reconstruct them.
- **Decision requested:** "Choose A, B or C."

**Not asked now:** merging this branch; public deployment (NG-13).

## Process lessons

- **A rule cited is not a rule applied.** S15's age metric named the source policy's horizon. Nobody
  checked the policy's own scope (time-sensitive rows only) until a cold reader asked why only one old
  link was "not fresh".
- **An unprimed reader is the cheapest audit of wording.** Two readers converged on the same three
  confusions, and on correct readings everywhere else. Agreement between two independent readers
  separates a block's defect from one reader's slip.
- **A definition-only reproduction tests the tutorial, not the query.** The query was right. Its
  population line could not carry a stranger to the same rows.
- **A probe can be wrong.** The first probe crash was the probe's planted value. It was found by reading
  the trace before recording it as a finding, and the build's unnamed crash became a smaller, true
  finding.
- **Retiring a block is a result.** The publishers count passed every check, and its information already
  lived row by row in the table.

## Implications for the next session

**For S16.5 (the HBM supplier research, D-139), and S17 after it (the policy entities, M5):**

- **Completed work:**
  - the metrics as they stand: coverage and source age, modified; the supplier metrics, kept; publishers,
    retired;
  - the audit's maturity ratings for analytical depth: process 3, outcome 2 at the audit, 3 once its
    blocking findings were remediated (now done);
  - **whether M4 can close:** the S16 gate, "analytical validity", is **met**: every acceptance criterion of Part B §15 holds, with criterion 3 met by two fresh readers rather than the human (Deviations 1). M4's closure as a
    milestone waits on the decision above about its milestone review.
- **Rules a policy-layer derivation must follow** (from S15 and S16):
  - a question, population and denominator before any number;
  - a population line a stranger can reproduce from, naming which refused or unknown records are rows;
  - an unknown is a gap, never a zero, and a metric without data is "cannot be computed yet";
  - a rule the metric cites is applied with its scope, read from the rule's own text;
  - a page copies cells or tallies drawn rows, saying when a record repeats;
  - a reference date in the query, moved by each session that rebuilds the pages.
- **Presentation risks the audit found,** for a policy block not to repeat:
  - a line that names records and rows in one breath;
  - a word ("gap") that covers two states;
  - a threshold shown for items it does not govern;
  - a range of a per-row count;
  - a large tally whose meaning sits in small type.
- **Open issues:**
  - the debt above, with owners;
  - **S16.5's research target:** the supplier metrics become computable when a source the Atlas holds
    names the supplier of each incorporated HBM part. Geographic concentration also needs where that
    supplier makes it; single-source needs a source stating that a part has exactly one supplier. Claude
    finds and verifies the sources itself (Source Scout, Extractor, Verifier; `source-policy.md`: the
    `rel:incorporates.supplier` row is time-sensitive, party standing, filings or technical documentation
    first). The links are staged, and each becomes canonical only on the human's approval (Class C). Both
    page builds stop when the first supplier is named (D-130, D-136), so S16.5 designs the supplier
    metrics' presentation before rebuilding;
  - the missing milestone reviews (the decision above).
- **Recommended next decision:** the milestone reviews, above, at S16.5's opening.
- **Files for S17 to read first:**
  - this report and [`analytical-audit-S16.md`](../../docs/architecture/analytical-audit-S16.md);
  - [`docs/architecture/metrics.md`](../../docs/architecture/metrics.md);
  - `MASTER-ARCHITECTURE.md` §7 and §8 (the governance and integration models the policy layer must not
    duplicate) and §6.2 (the relationship vocabulary);
  - the S17 entry of `SESSION-ROADMAP.md`.

**Next recommended milestone:** S16.5, the HBM supplier research (D-139): the supplier of the HBM in the
H100 and in Trainium2, found and verified from primary sources, staged for the human's approval, opening with
the decision on the M3 and M4 milestone reviews.
