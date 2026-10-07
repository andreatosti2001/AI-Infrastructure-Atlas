# AI-Infrastructure-Atlas — S16 Session Prompt

## Operating contract

This is a governed Opus 5.5 session. Before changing anything:

1. Read `CLAUDE.md`.
2. Read the relevant sections of `MASTER-ARCHITECTURE.md`.
3. Read `SESSION-PROMPT-SPEC.md` and `PROJECT-EVALUATION-FRAMEWORK.md`.
4. Read the immediately previous session report if it exists.
5. Inspect the actual repository state; do not assume the roadmap matches reality.
6. Restate mission, scope, non-goals and acceptance criteria.
7. Propose the smallest safe execution plan before implementation.

Follow:
`inspect → reason → propose → implement → validate → report`

### Evidence rules
- Use authoritative/current sources when current information matters.
- Do not use search snippets as evidence.
- Do not invent facts or silently infer supply-chain relationships.
- Separate FACT, DERIVATION, INTERPRETATION and IMPLICATION.
- Preserve uncertainty and source conflicts explicitly.

### Engineering rules
- Prefer the simplest architecture that satisfies the requirement.
- Do not introduce infrastructure merely for appearance.
- Do not perform broad refactors outside this session's scope.
- Never overwrite canonical data from unverified text.
- Run relevant tests/validators before declaring completion.

### Autonomy boundary
If a required decision crosses an approval boundary, stop and report it rather than improvising.

## Session-specific mission

### Mission

No feature expansion.

Audit:
- what each metric measures;
- what it does not measure;
- missing data;
- survivorship/selection issues;
- misleading presentation.

### Human decision

- approve, modify or retire each metric.

## Required end-of-session report

Record:
- files/components changed;
- data/evidence changes;
- commands/tests and results;
- decisions and rejected alternatives;
- deviations from this prompt;
- unresolved debt and evidence gaps;
- human approvals required;
- one concrete next-session handoff.

Commit only verified work.


---

# Part B — Session contract detail (SESSION-PROMPT-SPEC §2)

> **Provenance and precedence (D-012 pattern).**
> - Everything above this line is **Part A**. No upload was made. Claude assembled Part A after S15
>   was merged, when the human asked for "session 16's prompt" (2026-10-07):
>   - the operating contract and the report list are S15's Part A, word for word;
>   - the mission and the human decision are the operational roadmap's week-7 entry for S16
>     (`AI-Infrastructure-Atlas-Operational-Roadmap.md`, "S16 — Analytical audit"), word for word.
> - Part B is Claude's elaboration of Part A into SPEC §2's 18 sections. It was written after S15
>   (`SESSION-15-REPORT.md`, `docs/architecture/metrics.md`, D-127 to D-132, accepted 2026-10-06),
>   with the state measured on `main` @ `1ca2e89`.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** `CLAUDE.md` and
>   `MASTER-ARCHITECTURE.md` govern both. The prompt becomes immutable once S16 begins (D-011).
> - **Not yet answered:**
>   - Part A's confirmation, H-1 and H-2: asked at the start of S16, before any finding is written;
>   - H-3 and H-4: asked once the findings exist.

## 01 — Session identity

- **Session:** S16 · **Title:** Analytical audit
- **Type:** AUDIT (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`: "analytical validity").
- **Milestone:** M4 — Analytical Intelligence (S14–S16). S16 is its last session. It is also the
  audit SPEC §4 makes mandatory "after the first analytical layer".
- **Predecessor:** S15, the first metrics. **Successor:** S17, the policy entities (M5).
- **Complexity:** small to medium. It grows only with the remediation the human approves at H-3.

## 02 — Mission

Test whether each of the Atlas's five metrics answers a real question with a defensible population
and denominator, and whether a reader could misread it. Have readers who have not seen the
explanation read the metric blocks first. Write findings that separate what the metric measures
from what it does not, and name the missing data, the selection effects and the presentation risks.
Then put each metric to the human (approve, modify or retire) and carry out only what the human
approves.

## 03 — Why this session exists

- **The roadmap.**
  - `SESSION-ROADMAP.md` S16: "Challenge whether the metrics answer real questions and whether their
    denominators, populations and assumptions are defensible". Its required questions are: what is
    being measured, what is not, which missing data could distort the result, and could a user
    misread the metric.
  - The operational roadmap adds survivorship and selection issues and "no feature expansion". It
    also names the human's decision: "approve, modify or retire each metric".
- **The evaluation framework.**
  - PEF §8 (the analytical depth audit) exists "to prevent dashboard theatre": "A complex
    visualization without a defensible analytical question is not considered analytical depth."
  - PEF §2 ("Analytical depth"): "Are metrics reproducible, meaningful, transparent and appropriately
    limited?"
  - PEF §3: a maturity rating from 0 to 4 per dimension, each rating citing evidence.
- **What S15 hands over** (`SESSION-15-REPORT.md`, "Implications for the next session").
  - **Five metrics.** Two are computed:
    - evidence coverage, per accelerator over its links;
    - source age, as of 2026-10-06.
  - The three supplier metrics are shown as "cannot be computed yet". Each answers PEF §8 in its
    query file's header.
  - **S15's own answers to S16's questions, to check, not to adopt:**
    - **coverage** measures recorded links by basis, not dependence. Missing suppliers could distort
      it, and it could be misread as a share of truth;
    - **age** measures the newest evidence date against a reference date. It could be misread as
      reliability, or as current when the date is only an access date;
    - **the supplier metrics** measure nothing yet. The "2 of 2" could be misread as a supplier count.
  - **The presentation questions:** whether a block can be misread through the amber, the large
    count, or the order of the blocks.
  - **One reading already differed.** In the human's challenge (S15), "2 of 2 parts" was read as two
    supplier aspects being checked, not as the memory in each accelerator. The label was rewritten.
    S15 recommends starting from it.
  - **Two questions S15 left to S16:**
    - whether the three supplier blocks should be merged into one (considered at the S15 review, not
      taken; "S16 may raise it");
    - the publishers count, kept as a presentation tally ("S16 may audit it").
  - **One question S15 left open:** who moves the reference date, and when (debt row "the S15
    review: decide whether each session opening moves it"; the review did not decide it). This is
    H-4 below.
- **What the page shows today** (the research view, `site/hbm-insight/index.html`, "Indicators" and
  "Cannot be computed yet"; text as rendered on `1ca2e89`):

  | Block | What it says |
  |---|---|
  | Evidence coverage | Trainium2: "2 of 4 links stated", 1 inferred, 1 gap. H100: "1 of 4 links stated", 1 inferred, 2 gaps. Each: "rows drawn from 3 records, of which shared with another accelerator: 1" |
  | Evidence age as of 2026-10-06 | Trainium2: "2 of 3 dated links: newest evidence older than twelve months", "1 of 3 … dated only by the day a page was read". H100: 3 of 3 older, 0 of 3 access-dated |
  | Publishers behind a sourced link | "1 to 2"; "4 of 6 sourced rows rest on one publisher"; "Listed, never counted as confirmation." |
  | Supplier count, geographic concentration, single-source relationships | each "cannot be computed yet", "incorporated parts, one per accelerator: 2 of 2 with supplier not researched", and what each needs |

## 04 — Current state

As of `main` @ `1ca2e89` (S15 merged, PR #27). Verify it, and record the base, `git branch -a` and
`git ls-remote`.

- **Data** (unchanged since S13's remediation):

  | Record kind | Count |
  |---|---|
  | sources | 52 |
  | canonical claims | 120 |
  | events | 4 |
  | relationships | 5 |

  Staging is empty. The entity, identity-basis and refused-candidate files are as S15 left them.
- **SQL layer:**
  - four queries (`accelerator_dependencies`, `evidence_coverage`, `source_age`,
    `supplier_metrics`), run in dependency order by `tools/warehouse.py`. The three metrics read the
    first result as a view (D-131);
  - four results in `sql/results/`, each recording the digest of its inputs.
- **Pages** (both generated, neither published, NG-13):
  - `site/hbm-chain/index.html`, the journey page;
  - `site/hbm-insight/index.html`, the research view with the metric blocks and one "How this was
    computed" per metric (D-132).
- **Checks:**
  - 357 tests and Gate 0 pass. The three `--check` commands report up to date (measured on
    `1ca2e89`, Python 3.11);
  - the merged break harness: 74 breaks (`sessions/reports/SESSION-15-breaks/breaks.py`). On S15's
    final tree, 67 of 67 faults were caught as named and 7 of 7 controls passed.
- **Binding:**
  - D-124 (the SQL-to-visual rule): a page copies cells, tallies drawn rows with their denominator
    printed, takes first and last values, groups rows, and nothing else;
  - D-127 to D-132 and `metrics.md`, accepted as built on 2026-10-06;
  - `visual-architecture.md` (the grammar §7, the semantics §9, the rule §10).
- **Debt S16 inherits** (`SESSION-15-REPORT.md`, "Debt introduced/resolved"):
  - the reference date's owner (H-4);
  - a supplier metric's presentation once a supplier is named: owned by the session that adds the
    first supplier evidence (the build stops until then);
  - DT-S13-4 beyond the page's chain: Change Detector, inactive;
  - `build_page.sql_section`'s fixed result path: S22;
  - the research view's filter needs `:has()`: S20.
- **A gap found while writing this prompt** (`FACT`, measured on `1ca2e89`): PEF §4 requires a
  milestone audit "At every major milestone".
  - M1 and M2 have one (`docs/architecture/milestone-audits/`, `docs/quality/audit-history.md`).
  - M3 (S11–S13) has none: no file, and no row in the audit history.
  - M4 (S14–S16) closes with this session.
  - H-1 asks whether S16 takes them on.

**Next decision number:** D-133.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-15-REPORT.md` (in full, including "PEF §8, metric by metric" and the
   human's challenge); `docs/architecture/metrics.md`.
2. `PROJECT-EVALUATION-FRAMEWORK.md` §2, §3, §8; `SESSION-ROADMAP.md` S16; the operational roadmap's
   S16 entry.
3. `docs/architecture/visual-architecture.md` §7 (the grammar), §9 (the semantics), §10 (D-124);
   `docs/architecture/sql-layer.md`.
4. The four query files in `sql/` (their headers are the metrics' own PEF §8 answers) and their
   results.
5. `site/hbm-insight/index.html` as rendered, at 1280 and 375 px.
6. `docs/research/content-audit-S13.md` Part 5 (source quality, freshness exposure);
   `docs/research/source-policy.md` §12 (the 12-month horizon).
7. `docs/architecture/decisions.md` D-094, D-116, D-124, D-127 to D-132;
   `docs/quality/audit-history.md`; the M2 audit, as the model for an audit's form.
8. `tools/warehouse.py`, `tools/build_insight.py`; `tests/test_warehouse.py`, `tests/test_insight.py`.

**External access:** none. An audit finding is the Atlas's assessment (`INTERPRETATION`), never a
new fact about the world. A finding that would need a fact the Atlas does not hold, such as who
really supplies the HBM, is recorded as a gap. It is not filled by research in this session.

**Lessons to carry:**

- the human's own reading comes before Claude's (S13 H-2, S15's challenge). S15's one differing
  reading found a defect that every check had passed;
- write the checks before the code; a break must fail for the reason it names;
- an independent computation is the cheapest proof that a metric is right (S15: it caught the
  supplier population before any result was committed);
- a break that changes nothing is a finding (S15-M12): plant the case the data lacks;
- rows are not records; a zero is a presentation decision (S15);
- the human has twice declined a pop-up for a multi-part question and answered in writing. For
  questions with several parts, offer a short written form first;
- measure before estimating; ask before editing a file this prompt does not list.

## 06 — Required reasoning

Answer these in the audit before any remediation is proposed.

1. **For each of the five metrics, the roadmap's questions:**
   - What does it measure, in one plain sentence a reader could check against the page?
   - What does it not measure? Name the nearest wrong reading (for example, "evidence coverage" read
     as "how dependent").
   - Which missing data could distort it, and in which direction?
   - **Selection and survivorship:** which records exist because someone chose or found them, and
     how does that shape the number? At least:
     - the two accelerators were chosen for the slice;
     - the links "around an accelerator" are those the HBM slice drew, not all the accelerator's
       dependencies;
     - a gap exists only where the Atlas looked, so an unexamined link is neither in the
       denominator nor a gap;
     - every source was retrieved between 2026-09-29 and 2026-10-02;
     - 14 sources state no date and are dated by the day they were read;
     - only sourced rows have publishers.
   - **Misleading presentation:** could the block be misread through its encoding, its colour (the
     amber), its order on the page, a large count read without its denominator, a comparison
     between the two accelerators read as a ranking, or an "as of" date read later as current?
2. **PEF §8, rechecked.** S15 wrote eight answers per metric in each query header. For each answer,
   is it true of the query as written, complete, and in words a reader understands? A wrong or vague
   answer is a finding against the tutorial, not only against the metric.
3. **Is the question real?** For each metric, who would ask it, and what would they do with the
   answer? A metric with no real question is a candidate for retirement, whatever its correctness
   (PEF §8: "dashboard theatre").
4. **Reproducibility, independently.** Can a reader who has only `data/` and the metric's plain
   definition (not its SQL) reproduce the number? WH-12 to WH-14 are Claude's own independent
   computations. S16 tests whether the plain definition alone is enough.
5. **Sensitivity.** How much does each block move under a plausible change? For example:
   - one more link stated;
   - one undated source given a publication date;
   - the reference date moved to the day S16 starts;
   - one supplier named.

   Does the conclusion a reader draws change?
6. **The rulings under the metrics** (if H-1 A or C):
   - **S15's "cannot be computed yet" ruling (D-130):** is three blocks of a gap more informative
     than one, or louder than the evidence? Is it right that the build stops when a supplier is
     named?
   - **D-124 as applied:** is every number on the page a SQL cell or a permitted tally? Do the
     age-block tallies and the publishers count stay within "tally drawn rows with the denominator
     printed", or is a metric computed in the page?
7. **Blocking or debt.** For each finding:
   - **blocking:** fixed in S16, with the human's ruling, before M4 closes; or
   - **debt:** a named owner and a reason.

   Nothing undocumented.

## 07 — Tasks

**Opening**

1. Confirm Part A; ask H-1 and H-2 (§16). Record the base.

**Audit**

2. **Cold reading** (H-2), before any finding is written and before Claude explains a block:
   - the same short written form, one question per block: "what does this block tell you, and what
     would you conclude from it?";
   - answered by the readers H-2 names, each without seeing the others' answers or the tutorials;
   - each answer compared with what the block intends; outcomes only (D-114).
3. **Independent reproduction:**
   - an agent given only `data/` and each metric's plain-language definition (the question,
     population and denominator lines of its header, not its SQL) computes the metric;
   - a difference is a finding against the definition or the query.
4. **Sensitivity probes:**
   - each plausible change of §06 q5, applied in a scratch copy of the repository and rebuilt;
   - what each block then shows, recorded;
   - nothing committed except the probe script and its output.
5. **The audit report:** `docs/architecture/analytical-audit-S16.md`, unless the human names another
   path. It holds:
   - per metric, the §06 answers;
   - the cold readings and their comparison;
   - the reproduction and sensitivity results;
   - findings, each with its evidence (file, line, rendered text or probe output) and its
     blocking/debt split;
   - PEF §3 maturity ratings for "Analytical depth" (process and outcome), each citing evidence;
   - under H-1 C, the milestone parts.

   Add a row to `docs/quality/audit-history.md`.
6. **The human's decision** (Part A, H-3) once the findings exist:
   - approve, modify or retire each metric;
   - rule each finding blocking or debt;
   - H-4.

   Each ruling is recorded as an outcome and a date, from D-133 on.

**Remediation (only what the human approves)**

7. **For each metric modified:**
   - the change to its query, header, block or wording, with a decision that supersedes the part of
     D-128 to D-132 it changes;
   - the checks changed first (fail-first);
   - results and both pages rebuilt.
8. **For each metric retired:**
   - its block and tutorial leave the page, and its query and result leave `sql/`;
   - its checks are removed or inverted (a check that the block is gone);
   - the retirement is recorded with its reason. `metrics.md` keeps the metric's history, marked
     retired, never deleted without trace.

**Validation**

9. If a page or a result changes:
   - the full suite, Gate 0 and the three `--check` commands, in a fresh virtualenv;
   - the merged break harness, re-run in full, with S16's breaks added (one per remediation, each
     failing for its named reason);
   - browser QA at 1280 and 375 px on every page that changes.

   If nothing changes: the suite and Gate 0 only, and the report says the harness was not re-run
   and why.

**Documentation**

10. `README.md`, `docs/README.md`, the baseline rows; `metrics.md` and `sql-layer.md` where a ruling
    changes them; `sessions/reports/SESSION-16-REPORT.md`, with the handoff to S17.

## 08 — Explicit non-goals

- **No feature expansion** (Part A):
  - no new metric, query, page, chart type or interaction;
  - no new data, source, claim, edge or entity;
  - no research to fill a gap the audit finds.
- **No composite score**, and no ranking of accelerators.
- **No change to the first query's definitions** (`accelerator_dependencies.sql`: stated, inferred,
  gap, the evidence dates and their basis). A finding against them is recorded for the human. A
  change would reach every metric and both pages, which is beyond an audit's remediation without a
  superseding decision the human approves first (§16).
- **No change to S14.5's grammar, semantics or binding rule** without a superseding decision. A
  finding against them is a stop condition, not a quiet edit.
- **The researcher product** (S20); the policy layer (S17); public deployment (NG-13); anything in
  `Eu-Digital-Policy`.

## 09 — Constraints

- **An audit finding is an `INTERPRETATION`.** It cites the evidence it rests on: a file and line,
  the rendered text, a probe's output, or a reader's answer. It never states a fact about the world
  the Atlas does not hold.
- **The audit judges; it does not decide.** Approve, modify and retire are the human's (Part A).
  Claude recommends, with reasons, after the human's own reading.
- **Readers first.** No reader sees Claude's assessment of a block, or its tutorial, before answering
  the cold-reading form.
- **Unknown is never zero; a derivation lives in `sql/results/`**, never in `data/`; the build
  renders, it does not compute (D-124). These hold for every remediation.
- **Determinism.** Rebuilt results and pages are byte-identical across runs. A probe that changes the
  reference date does so in a scratch copy only. Moving the committed date is H-4's ruling.
- **Plain language first** (D-116). Each finding opens with what a reader would get wrong, or what
  is missing, in ordinary words. IDs follow.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Analyst | the audit's per-metric answers; the sensitivity probes | rechecks S15's own answers; does not defend them |
| Data Auditor | the reproduction probe and its output; tests; the break harness additions | an independent computation from the plain definition only |
| Knowledge Architect | the findings and the blocking/debt split; `decisions.md` (append); `metrics.md` status lines | populations, denominators, rows vs records |
| Editorial | the wording of any approved block or tutorial change | no fact not in a record; no "risk" or "dependency" wording |
| QA | the report's browser findings | every page that changes |
| Portfolio Reviewer | the maturity ratings' process side (if H-1 C, the milestone parts) | inactive unless H-1 C; otherwise its kind of judgement is the Knowledge Architect's, as in the M2 audit |

The fresh reader of H-2 A or C is not an agent role. It is a subagent given only the rendered page
and the form. It writes nothing to the repository; its answers are copied into the audit as
answers.

## 11 — Data and evidence rules

- **Canonical records:** read only. No record changes in S16.
- **Derived output:** generated, never edited. A remediation changes a query or a build, then
  regenerates.
- **Provenance of findings:** every finding cites where it was seen. A reader's answer is quoted as
  given, with the reader named by kind (the human, the fresh reader), not as an evaluation of the
  reader.
- **Human decisions:** recorded as outcomes and dates (D-114). The audit does not report how the
  human answered, only what was decided.
- **Confidence:** no numeric confidence values; a finding is blocking or debt.

## 12 — Implementation rules

**May create:**

- `docs/architecture/analytical-audit-S16.md` (or the path the human names);
- under H-1 C, `docs/architecture/milestone-audits/M3-audit.md` and `M4-audit.md`, or one combined
  file, as the human chooses;
- `sessions/reports/SESSION-16-*/` for the cold-reading forms, the probes and the break harness
  additions;
- `sessions/reports/SESSION-16-REPORT.md`.

**May modify, only for a remediation the human approves at H-3 or H-4:**

- `sql/evidence_coverage.sql`, `sql/source_age.sql`, `sql/supplier_metrics.sql`, and their results;
- `tools/build_insight.py`, `tools/insight_template.html`, `tests/test_insight.py`,
  `tests/test_warehouse.py`;
- `tools/build_page.py`, `tests/test_page.py`, only if a ruling changes the HBM page's access-date
  flag or the shared tutorial rendering;
- the regenerated pages.

**May always modify:** `decisions.md` (append), `metrics.md` status and history lines,
`docs/quality/audit-history.md`, `README.md`, `docs/README.md`, the baseline rows.

**Prohibited:**

- an edit to `data/`;
- an edit to `sql/accelerator_dependencies.sql`;
- a check loosened to pass;
- a metric value typed by hand;
- a new dependency;
- a remediation the human did not approve.

## 13 — Verification plan

- **At start:** in a fresh virtualenv from `requirements-test.txt` and `requirements-analysis.txt`:
  - the full suite and Gate 0;
  - `tools/warehouse.py --check`, `tools/build_page.py --check` and `tools/build_insight.py --check`.

  Record the base, `git branch -a` and `git ls-remote`.
- **Reproduction:** the fresh agent's numbers equal the committed results, or the difference is a
  finding.
- **Sensitivity:** every probe of §06 q5 is run in a scratch copy, rebuilt, and its effect on each
  block recorded. The repository is unchanged afterwards (`git status` clean apart from the probe
  files).
- **Remediation, if any:**
  - fail-first for each changed check;
  - the full merged harness plus S16's breaks, each failing for its named reason, and the controls
    passing;
  - browser QA at 1280 and 375 px on every changed page, including the tutorials open.
- **CI** is reported separately from local results.

## 14 — Evaluation requirements

The report records:

- per metric: what it measures and does not, its missing data, its selection effects, and its
  presentation risks;
- the cold readings and how each compared with the block's intent;
- the reproduction and sensitivity results;
- every finding, its blocking/debt split and the human's ruling;
- each metric's outcome: approved, modified (and how) or retired (and why);
- the maturity ratings and their evidence;
- deviations, invalidated assumptions, rejected alternatives and debt;
- whether the S16 gate ("analytical validity") is met, and whether M4 can close.

## 15 — Acceptance criteria

1. Each of the five metrics has written answers to the roadmap's five audit questions (measures, does
   not measure, missing data, selection and survivorship, misleading presentation), each citing
   evidence.
2. Each of S15's PEF §8 header answers is marked correct, corrected (by an approved remediation) or
   recorded as a finding.
3. Every block was read cold by the readers H-2 names, before Claude's assessment, and each reading
   was compared with the block's intent.
4. Each computed metric was reproduced from `data/` and its plain definition, or the difference is a
   finding.
5. Every finding is blocking or debt. Every blocking finding is remediated, or ruled by the human as
   accepted with its reason. Every debt has an owner.
6. The human approved, modified or retired each of the five metrics. Each outcome is recorded as a
   decision with its date (D-133 on), and each modification or retirement is reflected in the
   queries, the page, the checks and `metrics.md`.
7. No data changed. No new metric, page or source exists.
8. If anything was rebuilt:
   - the tests, Gate 0 and the three `--check` commands pass in a fresh virtualenv;
   - the merged harness catches every fault as named and every control passes;
   - browser QA is clean at 1280 and 375 px.

   CI is observed or reported as not observed.
9. The audit has a row in `docs/quality/audit-history.md`. The report satisfies SPEC §5, Part A and
   D-114.

## 16 — Stop conditions

Stop and report when:

- a finding would need a fact the Atlas does not hold (record it as a gap; do not research it);
- a remediation would change `data/` or the first query's definitions;
- a remediation would add a metric, a page or a chart type ("no feature expansion");
- a remediation would change S14.5's grammar, semantics or binding rule;
- a check would have to be loosened to pass;
- any condition in SPEC §2.16 or `CLAUDE.md` §18 applies.

**Human decisions** (`CLAUDE.md` §9A; recorded as outcomes, D-114).

**Asked at the start:**

- **Part A:** confirm as assembled, or amend.
- **H-1 — Human decision required: how far the audit reaches.**
  - *What we are deciding:* whether S16 audits only the five metrics as shown, or also the rules
    they were built under, or also the milestone audits the repository lacks.
  - *What will concretely change:*
    - Under A, the audit covers:
      - the five metrics and how the research view presents them;
      - S15's ruling that a metric without data is shown as "cannot be computed yet" (D-130);
      - whether every number on the page obeys the rule that a page only copies SQL cells or tallies
        drawn rows (D-124).

      One audit file results.
    - Under B, the audit covers the five metrics and their presentation only. The two rulings stand
      unexamined.
    - Under C, the audit is A plus the two milestone audits PEF §4 requires and the repository does
      not have:
      - M3 (S11 to S13, never written);
      - M4 (S14 to S16, which S16 closes).

      Each answers PEF §4's eight questions: what was intended, what was built, what changed,
      which assumptions failed, and so on. They are one or two more files and a larger session.
  - *Why:* S15's report recommends deciding this first. The ruling and the rule shape what the page
    shows as much as the queries do. A milestone without its audit leaves its shortcuts and failed
    assumptions unrecorded.
  - *What stays the same:* the cold reading, the reproduction and the human's verdict on each metric
    happen under every option.
  - *Future consequences:*
    - A lets the human revisit D-130 or D-124 with evidence.
    - B is smallest, but leaves both rules unaudited until S22.
    - C closes M4 with a full record, but makes S16 large and mixes a process audit into an
      analytical one.

      If C is not chosen, the missing milestone audits are put to the human again in S16's handoff,
      not dropped.
  - *Options:*
    - **A — The metrics, their presentation and the two rulings under them (recommended):** the
      roadmap's questions plus the two rules that most shape the page.
    - **B — The metrics and their presentation only.**
    - **C — A, plus the missing M3 and M4 milestone audits.**
  - *Decision requested:* "Choose A, B or C."
- **H-2 — Human decision required: who reads the metric blocks cold, before the audit's findings.**
  - *What we are deciding:* who answers "what does this block tell you?" for each block, before
    Claude explains anything.
  - *What will concretely change:*
    - Under A, two sets of readings:
      - you answer a short written form, one question per block (about seven questions);
      - a fresh agent, given only the rendered page and the same form, answers separately.

      Both sets are compared with each block's intent, and every difference becomes a finding.
    - Under B, only your readings are taken.
    - Under C, only the fresh agent reads. You rule on the findings afterwards, without having read
      the blocks cold.
  - *Why:* in S15 your one differing reading found a defect every check had passed. A second,
    unprimed reader tests whether a misreading is one person's or the block's.
  - *What stays the same:* the audit's other work, and your verdict on each metric at the end.
  - *Future consequences:*
    - A gives the strongest evidence of misreading. It costs you about ten minutes.
    - B keeps the human reading but gives no second reader.
    - C saves your time, but a model's reading may differ from a person's, and you lose the first
      look.
  - *Options:*
    - **A — You and a fresh agent, separately (recommended).**
    - **B — You only.**
    - **C — A fresh agent only.**
  - *Decision requested:* "Choose A, B or C." The form is written by default, since the last two
    multi-part questions were declined as pop-ups.

**Asked once the findings exist:**

- **H-3 — Human decision required: approve, modify or retire each metric** (Part A).
  - It is asked as one request listing the five metrics. For each, it gives:
    - one plain sentence of what the audit found;
    - Claude's recommendation;
    - three outcomes:
      - **kept as built:** the block, query and checks stay;
      - **kept with the named change:** what the block or query will say afterwards, and which
        checks change;
      - **retired:** the block and its tutorial leave the page, and the query leaves `sql/`.
  - Retiring a supplier block removes a visible gap from the page, and the request says so.
  - The same request asks the blocking/debt split of each finding. It also asks, if raised, whether
    the three supplier blocks become one.
  - If the list is too long to read in one sitting, it is split as `CLAUDE.md` §9A requires.
- **H-4 — Human decision required: when the source-age reference date moves.**
  - *What we are deciding:* who moves the date that every age is measured from (now 2026-10-06), and
    when. S15 left this to its review, which did not decide it.
  - The options are written once the sensitivity probes show how much a move changes the page.
    Candidates are:
    - each session that rebuilds the pages moves it to its opening date;
    - each audit session moves it;
    - it moves only when the human asks.
  - Each option says which files change at each move: the query, the result, the research view, and
    the digest lines of both pages.

## 17 — Deliverables

- The audit (`analytical-audit-S16.md`, or the path named), with a row in `audit-history.md`.
- Under H-1 C, the M3 and M4 milestone audits.
- The cold-reading forms and answers, the reproduction probe and the sensitivity probes, with
  their outputs.
- The human's rulings, recorded from D-133 on.
- The approved remediation, with its checks, rebuilt results and pages, the harness run and browser
  QA. If no remediation is approved, a statement that nothing was rebuilt.
- `README.md`, `docs/README.md` and baseline rows; `sessions/reports/SESSION-16-REPORT.md`.

## 18 — Handoff

S16's report must hand S17 (the policy entities, M5):

- **Completed work:**
  - the metrics as they stand after the human's verdict;
  - the audit's maturity ratings;
  - whether M4 can close.
- **For S17:**
  - which metric rules a policy-layer derivation must follow (population, denominator, unknowns,
    "cannot be computed yet");
  - which presentation risks the audit found, so a policy block does not repeat them.
- **Open issues:** debt with owners, including what evidence would make the supplier metrics
  computable, and, if H-1 C was not chosen, the missing milestone audits, put again to the human
  per `CLAUDE.md` §9A.
- **Recommended next decision**, per `CLAUDE.md` §9A.
- **Files for S17 to read first:**
  - the S16 report and audit;
  - `metrics.md`;
  - `MASTER-ARCHITECTURE.md`'s policy-layer sections;
  - the S17 entry of `SESSION-ROADMAP.md`.
