# AI-Infrastructure-Atlas — S15 Session Prompt

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

Implement transparent metrics:
- supplier count;
- geographic concentration;
- demonstrable single-source relationships;
- evidence coverage;
- source age.

### Human task

- challenge the denominator and population of every metric.

**Do not allow an opaque composite risk score.**

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
> - Everything above this line is **Part A**. Claude assembled it after S14 was merged, at the
>   human's request to write the S15 prompt (2026-10-06):
>   - the operating contract and the report list are S14's Part A, word for word;
>   - the mission, the human task and the closing rule are the operational roadmap's week-6 entry
>     for S15 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`, "S15 — Dependency metrics"), word
>     for word.
> - Part B is Claude's elaboration into SPEC §2's 18 sections, written after S14
>   (`SESSION-14-REPORT.md`, `docs/architecture/sql-layer.md`, D-117 to D-121).
> - Part B adds detail only. **If the two ever conflict, Part A governs.** `CLAUDE.md` and
>   `MASTER-ARCHITECTURE.md` govern both. The prompt becomes immutable once S15 begins (D-011).
> - **Not yet answered:** Part A's confirmation and H-1 to H-4, asked at the start of S15.

## 01 — Session identity

- **Session:** S15 · **Title:** Dependency metrics
- **Type:** ANALYSIS (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`: "transparent metrics")
- **Milestone:** M4 — Analytical Intelligence (second session).
- **Predecessor:** S14, the SQL layer. **Successor:** S16, the analytical audit.
- **Complexity:** medium. It becomes large if H-1 B adds a research step.

## 02 — Mission

Give the Atlas its first metrics, each one answering a stated question over a stated population
and denominator. Compute each in SQL from the warehouse S14 built. Show each on the page with its
"How this was computed" tutorial. Where the Atlas holds no data for a metric, show that the metric
cannot be computed yet, and why, instead of a number. Then have the human challenge every
denominator before Claude explains it.

## 03 — Why this session exists

- **The roadmap.**
  - `SESSION-ROADMAP.md` S15: "Implement transparent descriptive metrics for supplier and
    geographic concentration"; explicit non-goal: "Do not create an opaque composite 'dependency
    score'".
  - The operational roadmap names the five metrics of Part A and the human's task: "challenge the
    denominator and population of every metric".
- **What S14 hands over** (`SESSION-14-REPORT.md`, "Implications for the next session"):
  - the tables a metric may use (`sql-layer.md` §8);
  - the populations it could count (the 5 edges, the 120 claims, the 99 citations on 85 cited
    claims, the 2 accelerators, the 8 links of the first result), each a census of what the Atlas
    holds, not of the world;
  - the weaknesses every metric must carry;
  - Claude's proposal for the first metric (H-2 below).
- **What the data allows today** (measured on `main` @ `2a6e91c`, before writing this prompt):

  | Metric (Part A) | Its population today | Computable? |
  |---|---|---|
  | supplier count | suppliers recorded for a part: none. 0 `supplies` edges; both HBM `supplier` fields are `not_researched` (D-094) | no: unknown, never zero |
  | geographic concentration | the jurisdictions of those suppliers: none, for the same reason | no |
  | demonstrable single-source relationships | evidence that a part has exactly one supplier: none read | no |
  | evidence coverage | the 8 links of the first result; or every edge, field and claim | yes |
  | source age | the evidence dates of the 52 sources and 99 citations (14 sources state no date of their own) | yes, once "age as of when" is decided (H-3) |

  Three of Part A's five metrics have no population. That is a finding, and H-1 asks what to do
  with it.
- **A trap to avoid, named in advance.** The 8 company records have headquarters in 4
  jurisdictions (5 of 8 in the US). A "geographic concentration" computed over them would measure
  which companies the Atlas chose to record (S07's seed), not where supply is concentrated. The
  same holds for counting companies by role (2 memory manufacturers recorded). Neither may be
  presented as a concentration or supplier metric.

## 04 — Current state

As of `main` @ `2a6e91c` (PR #24, S14 merged). Verify it, and record the base, `git branch -a` and
`git ls-remote`.

- **Data:**

  | Record kind | Count |
  |---|---|
  | sources | 52 |
  | canonical claims | 120 |
  | entity records | 33 |
  | events | 4 |
  | relationships | 5 |
  | refused candidates | 12 |
  | identity-basis rows | 28 |

  Staging is empty.
- **SQL layer:**
  - `tools/warehouse.py` builds an in-memory DuckDB 1.5.6 from the canonical files on every run.
  - It runs `sql/accelerator_dependencies.sql` (8 rows) and writes `sql/results/`.
  - The page reads the saved results and never runs DuckDB (D-118 to D-121, accepted).
- **Checks:** 328 tests and Gate 0 in CI (WH-1 to WH-10, PG-1 to PG-11). The page and the results
  rebuild byte-identically.
- **Debt due in S15** (`SESSION-14-REPORT.md`):
  - DT-7: a product's `vendor` against the `designs` edge, and an edge's `supplier` against a
    `supplies` edge, the moment a metric combines them;
  - the access date that dates an undated source must be flagged in any metric over evidence
    dates;
  - the two break harnesses (`SESSION-13-breaks/breaks.py`, `SESSION-14-breaks/sql_breaks.py`) are
    merged when the page next changes;
  - the human's reading has one field per question and per part;
  - DT-S13-4 (evidence ageing past the 12-month horizon is unreported): decide whether the
    source-age metric discharges it (§06 q6).

**Next decision number:** D-122.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-14-REPORT.md`; `docs/architecture/sql-layer.md`.
2. `PROJECT-EVALUATION-FRAMEWORK.md` §8 (the eight questions for every metric).
3. `docs/research/content-audit-S13.md` Part 5 (source quality, freshness exposure).
4. `MASTER-ARCHITECTURE.md` §5.7, §16.1; `CLAUDE.md` §6A, §7, §12; D-094, D-103, D-115, D-116,
   D-118 to D-121.
5. `docs/research/source-policy.md` §12 (the freshness horizon); `company-dataset.md` §9 (F-1).
6. `sql/accelerator_dependencies.sql`; `tools/warehouse.py`; `tools/build_page.py`;
   `tests/test_warehouse.py`; `tests/test_page.py`.

**External access:** none, unless H-1 B is chosen. In that case the source policy governs every
retrieval, and every new source, claim and edge goes to staging for the human's review.

**Lessons to carry:**

- write the checks before the code;
- a second, independent computation is the cheapest proof that SQL is right (S14 WH-10);
- check that a control is valid data before trusting it;
- ask before editing a file this prompt does not list;
- plain-language meaning first (D-116);
- a reader confuses listing with counting, so say which one a number is.

## 06 — Required reasoning

Answer these in the design before building:

1. **PEF §8, for every metric:**
   - What question does it answer?
   - What population does it cover?
   - What is the denominator?
   - What assumptions are made?
   - What data is missing?
   - Can another person reproduce it?
   - How sensitive is the conclusion to plausible changes?
   - What does it **not** prove?

   The answers are written beside the metric, in the design and in its tutorial.
2. **Unknowns inside a metric.** How `not_researched`, `not_publicly_determinable` and
   `not_applicable` enter a count or a share. They are never zero, never dropped silently, and never
   folded into the denominator without saying so. A metric with unknowns in its population shows
   them as their own part (for example, "2 links stated, 1 inferred, 2 unknown").
3. **A metric that cannot be computed.** What the page and the result show for each of the three
   metrics without a population, and what evidence would make each computable.
4. **Source age without the clock** (H-3). How an age stays reproducible byte for byte, and how a
   reader learns which date it is measured from.
5. **Undated sources.** How a source dated by its access date is kept apart, so its "age" is never
   read as the age of its content.
6. **DT-S13-4.** Does the source-age metric, measured against a stated date, serve as the
   ageing report S13 asked for? If it does not, what is still missing?
7. **No composite.** How the page keeps the metrics apart, so that no one number reads as a
   "dependency" or "risk" score.
8. **DT-7.** Whether any metric combines `vendor` with `designs`, or `supplier` with `supplies`.
   If one does, how they stay in separate columns.

## 07 — Tasks

1. Opening: confirm Part A; ask H-1 to H-4.
2. **The design**, proposed with D-122 onward: `docs/architecture/metrics.md` (or a new part of
   `sql-layer.md`, as the design argues). It covers §06 for every metric.
3. **Checks first** (fail before the code exists):
   - an independent plain-Python computation of each metric;
   - a planted `not_researched` counted as unknown, never as zero;
   - a change to the reference date that changes the ages and nothing else (if H-3 A);
   - each metric's tutorial matching its query file;
   - no number shown for a metric with no population.
4. **The queries**: one file per metric in `sql/`, each its own tutorial (D-121), with results in
   `sql/results/`.
5. **The page**: the metrics where H-4 places them. Each opens with its question in plain words,
   shows its population and denominator beside the number, and has its own "How this was
   computed".
6. **The human's task** (Part A), before Claude's explanation:
   - for each metric, the population, the denominator and what it does not measure, one question
     at a time;
   - asked as a form, or as interactive questions with candidate answers if the human prefers
     (S14);
   - the outcome is recorded per question (D-114).
7. **Validation:**
   - fail-first;
   - the merged break harness: all S13 and S14 breaks plus new metric breaks;
   - browser QA at 1280 and 375 px.
8. **Documentation:** `README.md`, `docs/README.md`, baseline rows; `SESSION-15-REPORT.md`.

## 08 — Explicit non-goals

- **Any composite score**: "dependency", "risk", "exposure" or similar (Part A: never).
- **Rankings**, and any metric presented as a statement about the world when its population is
  what the Atlas recorded.
- **A concentration metric over company headquarters or roles** (§03, the trap).
- **New sources, claims, edges or entities**, unless H-1 B is chosen; then only through staging and
  the human's review.
- **An age computed from the clock**, at build time or in a committed result.
- **A database server, an ORM, a notebook or a frontend framework.** No script in the page unless
  H-3 C is chosen.
- **Public deployment** (NG-13); anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **A metric is a derivation** (`DERIVATION`). It lives in `sql/results/`, never in `data/`, and is
  rebuilt by `tools/warehouse.py`.
- **Unknown is never zero.** Every count and share shows its unknown part next to its known part.
- **Denominators are visible.** No percentage appears without the number it is a share of, and the
  name of that population.
- **Determinism.** No clock and no random order; every query ends in `ORDER BY`. Results are byte
  identical across runs.
- **Reader first (D-116).** Each metric opens with its question and what it does not prove, in plain
  words; codes and IDs come after.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Analyst | `sql/` queries and their generated results; the metrics design | every metric answers PEF §8 |
| Data Auditor | `tests/`, `tools/warehouse.py` (only if a metric needs a loader change), the merged break harness | checks first; an independent computation per metric |
| Knowledge Architect | the metrics design's definitions; `decisions.md` (append) | populations, denominators, unknowns |
| Editorial | the page section's framing and the tutorial text | plain language, no fact not in a record, no "risk" wording |
| QA | the report (browser findings) | the page changes |
| Source Scout, Extractor, Verifier | staging only, under H-1 B | the source policy; the human's review |

## 11 — Data and evidence rules

- **Canonical records:** read only. Under H-1 B, new records go to staging only.
- **Derived output:** generated, never edited; it records the digest of its inputs.
- **Provenance:** every metric value can be traced to the rows it counts, and each row to its
  records.
- **Human decisions:** recorded as outcomes and dates (D-114).
- **Confidence:** no numeric confidence values.

## 12 — Implementation rules

**May create:**

- `docs/architecture/metrics.md` (or a part of `sql-layer.md`);
- new `sql/*.sql` files and their results;
- tests and fixtures;
- the merged break harness and the session's QA under `sessions/reports/`;
- `SESSION-15-REPORT.md`.

**May modify:**

- `tools/build_page.py`, `tools/page_template.html`, `tests/test_page.py` (H-4);
- `tests/test_warehouse.py`;
- `tools/warehouse.py`, only if a metric needs a table the loader lacks;
- `docs/architecture/sql-layer.md`; `decisions.md` (append);
- `docs/README.md`, baseline rows, `README.md`;
- under H-1 B only: `data/staging/*.json`.

**Prohibited:**

- a metric typed or edited by hand;
- a check loosened to pass;
- a new fact entering canonical data;
- an unpinned dependency;
- a composite score.

## 13 — Verification plan

- **At start:** the full suite, Gate 0, `tools/warehouse.py --check` and `tools/build_page.py
  --check`, in a fresh virtualenv built from `requirements-test.txt` and
  `requirements-analysis.txt`. Record the base, `git branch -a` and `git ls-remote`.
- **Each metric:** its SQL result equals an independent plain-Python computation.
- **Unknowns:** a planted unknown reaches the metric as unknown; a planted `not_publicly_determinable`
  stays distinct from `not_researched`. Plant it below the data checks (S14 lesson: that state
  needs a search record to be valid data).
- **Reference date** (H-3 A): changing it changes the ages, and only the ages.
- **Uncomputable metrics:** the page never shows a number for them; a planted number fails.
- **Tutorials:** a planted change to a query file fails until it is rebuilt (S14 Q1 pattern).
- **Page:** fail-first; the merged break harness; browser QA at 1280 and 375 px. CI is reported
  separately from local results.

## 14 — Evaluation requirements

The report records:

- each metric's PEF §8 answers;
- the result of each metric;
- the human's challenge of each denominator and how it compared with Claude's;
- the treatment of the three metrics that have no population;
- deviations and invalidated assumptions;
- debt;
- whether the S15 gate ("transparent metrics") is met.

## 15 — Acceptance criteria

1. Every metric S15 computes states its question, population, denominator and what it does not
   prove, on the page and in its tutorial.
2. No metric shows a number over a population the Atlas holds as unknown. The three
   supplier-dependent metrics follow H-1's ruling.
3. Every metric's result equals an independent computation, and regenerates byte for byte from
   versioned inputs.
4. No composite score exists anywhere in the repository or on the page.
5. The human challenged every denominator before Claude's explanation (Part A's human task).
6. Tests and Gate 0 pass in a fresh virtualenv; the page and the results rebuild byte-identically;
   CI is observed or reported as not observed.
7. DT-7 and DT-S13-4 are each resolved or given a new owner. The two break harnesses are merged.
8. The report satisfies SPEC §5, Part A and D-114.

## 16 — Stop conditions

Stop and report when:

- a metric would need a value only a document holds;
- a metric would have to be written into `data/`;
- a metric's denominator cannot be stated in plain words;
- a number would have to stand in for an unknown;
- any condition in SPEC §2.16 or `CLAUDE.md` §18 applies.

**Human decisions** (asked at the start, `CLAUDE.md` §9A; recorded as outcomes, D-114):

- **Part A:** confirm as assembled, or amend.
- **H-1 — Human decision required: what S15 does with the three metrics that have no data.**
  - *What we are deciding:* supplier count, geographic concentration and single-source
    relationships all need to know who supplies a part. The Atlas records no supplier: both HBM
    supplier fields are "not researched", and no `supplies` edge exists. What should S15 do with
    these three?
  - *What will concretely change:*
    - Under A, the page shows each of the three by name with "cannot be computed yet", the reason
      ("no supplier recorded; 2 of 2 not researched"), and what evidence would make it computable.
      There is no number, and the results file records the same state.
    - Under B, S15 first searches first-hand sources for who supplies the HBM in the H100 and in
      Trainium2. Anything found goes to staging for your review, and only then are the three
      computed.
    - Under C, the three are left out of S15 entirely and recorded as debt for a research session.
  - *Why:* Part A asks for these metrics; the data cannot support them. A number would turn an
    unknown into a zero.
  - *What stays the same:* evidence coverage and source age are built under every option.
  - *Future consequences:* A makes the gap visible to every reader and to S16's audit. B may add
    the first supplier evidence, but S10 searched and found none, and it makes S15 a research
    session. C keeps S15 small but hides the gap from the page.
  - *Options:*
    - **A — Shown as "cannot be computed yet", with why (recommended).**
    - **B — A bounded research step first.**
    - **C — Left out until a research session.**
  - *Decision requested:* "Choose A, B or C."
- **H-2 — Human decision required: what evidence coverage is measured over.**
  - *What we are deciding:* the population and denominator of the first computable metric.
  - *What will concretely change:*
    - Under A, for each accelerator, its recorded links are split into stated, inferred and
      unknown, over the links the Atlas records around it. For example, the H100 has 4 links:
      1 stated, 1 inferred, 2 gaps. The result is two small breakdowns on the page.
    - Under B, the same split is taken over every edge and field in the Atlas: one breakdown for
      the whole dataset.
    - Under C, the share of claims that cite a source directly rather than reasoning from other
      claims.
  - *Why:* each population answers a different question. A: "how much of this accelerator's
    chain rests on direct evidence?" B: "how well evidenced is the Atlas as a whole?" C: "how much
    of the Atlas is the Atlas's own reasoning?"
  - *Future consequences:* A stays on the page's question and is easy to check against the table
    above it. B mixes identity fields, which are stated by design, and inflates the stated part.
    C says nothing about the chain.
  - *Options:*
    - **A — Per accelerator, over its recorded links (recommended).**
    - **B — Over the whole Atlas.**
    - **C — Over the claims.**
  - *Decision requested:* "Choose A, B or C."
- **H-3 — Human decision required: how "source age" is measured without the clock.**
  - *What we are deciding:* an age is a difference between two dates. S14 refused to read today's
    date, because a committed result would then change every day.
  - *What will concretely change:*
    - Under A, the query file holds a reference date, changed only by a commit. Ages are measured
      from it, and the page says "age as of <that date>". The results stay byte-identical until
      someone moves the date.
    - Under B, no age is computed. The page keeps showing dates only, as S14 does, and the reader
      does the arithmetic.
    - Under C, a small script in the page computes ages on the day it is opened. The page then
      runs code and differs from day to day, and two of its checks would change.
  - *Why:* Part A asks for source age; S13 asked for a way to see evidence passing the 12-month
    horizon (DT-S13-4).
  - *Future consequences:* A gives a reproducible "as of" age and a natural place for the ageing
    report. B is simplest but leaves DT-S13-4 open. C is always current but gives up the page's
    reproducibility.
  - *Options:*
    - **A — Against a reference date kept in the query file (recommended).**
    - **B — Dates only, no age.**
    - **C — Computed in the page when it is opened.**
  - *Decision requested:* "Choose A, B or C."
- **H-4 — Human decision required: where the metrics appear.**
  - *What will concretely change:* under A, the HBM page gains a section, "What the Atlas can and
    cannot measure", after "The chain as a table". Each metric has its own "How this was
    computed" tutorial. Under B, a new page shows the metrics, linked from the HBM page.
  - *Options:*
    - **A — A section on the HBM page (recommended):** the metrics sit next to the chain they
      describe.
    - **B — A new page:** keeps the HBM page shorter; a second page to maintain.
  - *Decision requested:* "Choose A or B."

## 17 — Deliverables

- The metrics design and D-122 onward.
- One query per metric, with its results and its tutorial.
- The checks, including an independent computation per metric.
- The page section, rebuilt, with browser QA.
- The merged break harness and its results.
- `README.md`, `docs/README.md` and baseline rows; `sessions/reports/SESSION-15-REPORT.md`.

## 18 — Handoff

S15's report must hand S16 (the analytical audit):

- **Completed work:** each metric, with its PEF §8 answers; whether the gate is met.
- **For S16:** for every metric, what it measures, what it does not, which missing data could
  distort it, and how a user could misread it. These are S16's own required questions, with
  S15's answers to check.
- **Open issues:** debt with owners, including what evidence would make the supplier metrics
  computable.
- **Recommended next decision:** whether S16 audits the metrics only, or also the decision taken
  at H-1.
- **Files for S16 to read first:** the S15 report; the metrics design; `sql-layer.md`.
