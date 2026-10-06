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
> - Part B is Claude's elaboration into SPEC §2's 18 sections. It was first written after S14
>   (`SESSION-14-REPORT.md`, `docs/architecture/sql-layer.md`, D-117 to D-121), then revised at the
>   human's request on 2026-10-06 to integrate S14.5 (`SESSION-14.5-REPORT.md`,
>   `docs/architecture/visual-architecture.md`, D-122 to D-126, accepted 2026-10-06). The revision
>   changed only Part B: the predecessor, the base, the next decision number, the rules S14.5 made
>   binding, the debt it handed over, and an H-4 option for the research view.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** `CLAUDE.md` and
>   `MASTER-ARCHITECTURE.md` govern both. The prompt becomes immutable once S15 begins (D-011).
> - **Not yet answered:** Part A's confirmation and H-1 to H-4, asked at the start of S15.

## 01 — Session identity

- **Session:** S15 · **Title:** Dependency metrics
- **Type:** ANALYSIS (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`: "transparent metrics")
- **Milestone:** M4 — Analytical Intelligence (third session, after S14 and S14.5).
- **Predecessor:** S14.5, the visual and research-experience architecture (S14, the SQL layer, before
  it). **Successor:** S16, the analytical audit.
- **Complexity:** medium. It becomes large if H-1 B adds a research step.

## 02 — Mission

Give the Atlas its first metrics, each one answering a stated question over a stated population
and denominator. Compute each in SQL from the warehouse S14 built. Show each through the visual
grammar S14.5 made binding, with its denominator in the same block and its "How this was computed"
tutorial. Where the Atlas holds no data for a metric, show that the metric cannot be computed yet,
and why, instead of a number. Then have the human challenge every denominator before Claude
explains it.

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
- **What S14.5 hands over** (`SESSION-14.5-REPORT.md`, "Implications for the next session";
  `visual-architecture.md`, accepted 2026-10-06):
  - **The binding rule** (D-124, §10). A page may copy result cells, tally the rows it draws over a
    denominator it prints, take first and last values, and group rows. **Anything else is a metric,
    and a metric is a column of a SQL result with its tutorial.** S15's metrics are the first to
    pass through that rule.
  - **The grammar** (§7). Indicator blocks (§7.5) hold a state, a tally or a range, each with its
    unit and denominator. Rankings (§7.1) list unknowns apart, never at zero. Comparisons (§7.6)
    draw competing values side by side, never averaged (P-08). No mode switch (absolute ↔ share)
    before a metric exists (P-19).
  - **The semantics** (§9). The amber is reserved for gaps. "No recorded relationship" is neutral,
    distinct from a gap the Atlas recorded. Every mark says its basis in words.
  - **A working example.** The research-view prototype (`site/hbm-insight/index.html`) already shows
    per-accelerator tallies of the S14 result: links on stated evidence, rows with nothing to date,
    and publishers per sourced row. S14.5 handed them to S15 to keep as presentation, to move into
    SQL as metrics, or to retire.
  - **Two findings that shape H-2 and H-3:**
    - **Rows are not records.** The S14 result has 8 rows (accelerator × link) drawn from 5 records:
      the `requires` edge appears under both accelerators, and each unknown supplier sits on its own
      `incorporates` edge. A count over rows and a count over records give different answers.
    - **Some evidence dates are access dates.** The latest evidence date in the S14 result,
      2026-10-01, is the day an undated web page was read, not a publication date. The result has
      no column that says which dates are access dates.
- **What the data allows today** (measured on `main` @ `2a6e91c`, before writing this prompt; S14.5
  added no data):

  | Metric (Part A) | Its population today | Computable? |
  |---|---|---|
  | supplier count | suppliers recorded for a part: none. 0 `supplies` edges; both HBM `supplier` fields are `not_researched` (D-094) | no: unknown, never zero |
  | geographic concentration | the jurisdictions of those suppliers: none, for the same reason | no |
  | demonstrable single-source relationships | evidence that a part has exactly one supplier: none read | no |
  | evidence coverage | the 8 links (rows) of the first result, drawn from 5 records; or every edge, field and claim | yes |
  | source age | the evidence dates of the 52 sources and 99 citations (14 sources state no date of their own) | yes, once "age as of when" is decided (H-3) |

  Three of Part A's five metrics have no population. That is a finding, and H-1 asks what to do
  with it.
- **A trap to avoid, named in advance.** The 8 company records have headquarters in 4
  jurisdictions (5 of 8 in the US). A "geographic concentration" computed over them would measure
  which companies the Atlas chose to record (S07's seed), not where supply is concentrated. The
  same holds for counting companies by role (2 memory manufacturers recorded). Neither may be
  presented as a concentration or supplier metric (`visual-architecture.md` V-4: every number says
  what population it counts, the Atlas's records, never the world).

## 04 — Current state

As of `main` after S14.5 is merged. **S14.5 (`claude/magical-maxwell-qar167` @ `69642b0`, with
its review) must be on `main` before S15 starts.** Verify it, and record the base, `git branch -a`
and `git ls-remote`.

- **Data** (unchanged by S14.5):

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
  - The pages read the saved results and never run DuckDB (D-118 to D-121, accepted).
- **Pages** (both generated, neither published):
  - `site/hbm-chain/index.html`, the dependency journey (S11, S14): it holds every evidence panel;
  - `site/hbm-insight/index.html`, the research-view prototype (S14.5, D-125). It renders the S14
    result in the seven layers and links each mark to an evidence panel of the journey page.
  - **Build order:** data, `tools/warehouse.py`, `tools/build_page.py`, `tools/build_insight.py`.
    `decisions.md` is an input of both pages, so every decision appended means rebuilding both
    (their digest lines change).
- **Checks:** 348 tests and Gate 0 in CI: WH-1 to WH-10, PG-1 to PG-11, IN-1 to IN-9 and the build
  refusals. Both pages and the results rebuild byte-identically. Gate 0 accepts sub-session numbers
  (D-126).
- **Binding since S14.5** (accepted 2026-10-06): `visual-architecture.md` V-1 to V-11, U-1 to U-8,
  the design tokens (§3), the grammar (§7), the semantics (§9) and the binding rule (§10, D-124).
- **Debt due in S15:**
  - from S14 (`SESSION-14-REPORT.md`):
    - DT-7: a product's `vendor` against the `designs` edge, and an edge's `supplier` against a
      `supplies` edge, the moment a metric combines them;
    - the access date that dates an undated source must be flagged in any metric over evidence
      dates;
    - the human's reading has one field per question and per part;
    - DT-S13-4 (evidence ageing past the 12-month horizon is unreported): decide whether the
      source-age metric discharges it (§06 q6);
  - from S14.5 (`SESSION-14.5-REPORT.md`):
    - **the evidence-date basis.** Add a column saying whether each evidence date is a claim's
      `as_of`, a date the source states, or an access date. A page can then flag the access date on
      its row. This is the S14 debt above, made concrete;
    - **the break harnesses are now three** (`SESSION-13-breaks/breaks.py`,
      `SESSION-14-breaks/sql_breaks.py`, `SESSION-14.5-breaks/insight_breaks.py`). They are merged
      when a page next changes;
    - **`sql-layer.md` §7 overstates** "every row today has one publisher". The two inferred rows
      rest on two publishers each (the S14 table's caveat flags were always correct). A status-line
      correction is proposed at the opening, as a one-line confirmation;
    - **the prototype's tallies:** keep, move into SQL, or retire (H-4).

**Next decision number:** D-127.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-14.5-REPORT.md`; `docs/architecture/visual-architecture.md` §7, §9,
   §10, §11.
2. `sessions/reports/SESSION-14-REPORT.md`; `docs/architecture/sql-layer.md`.
3. `PROJECT-EVALUATION-FRAMEWORK.md` §8 (the eight questions for every metric).
4. `docs/research/content-audit-S13.md` Part 5 (source quality, freshness exposure).
5. `MASTER-ARCHITECTURE.md` §5.7, §16.1; `CLAUDE.md` §6A, §7, §12; D-094, D-103, D-115, D-116,
   D-118 to D-121, D-124.
6. `docs/research/source-policy.md` §12 (the freshness horizon); `company-dataset.md` §9 (F-1).
7. `docs/research/visual-benchmark-S14.5.md` Part 3, rows P-05, P-06, P-08, P-12, P-19, P-20.
8. `sql/accelerator_dependencies.sql`; `tools/warehouse.py`; `tools/build_page.py`;
   `tools/build_insight.py`; `tests/test_warehouse.py`; `tests/test_page.py`; `tests/test_insight.py`.

**External access:** none, unless H-1 B is chosen. In that case the source policy governs every
retrieval, and every new source, claim and edge goes to staging for the human's review.

**Lessons to carry:**

- write the checks before the code;
- a second, independent computation is the cheapest proof that SQL is right (S14 WH-10);
- check that a control is valid data before trusting it;
- ask before editing a file this prompt does not list;
- plain-language meaning first (D-116);
- a reader confuses listing with counting, so say which one a number is;
- **a break must fail for the reason it names** (S14.5 V2): a syntax error is not a caught break;
- **a build refusal is a check that runs before the page exists** (S14.5's first build refused a
  wrong evidence link);
- **rows are not records**: say which one a count counts;
- **looking at the rendered page finds what the checks cannot**: an orientation word false on
  phones, repeated words.

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

   The answers are written beside the metric, in the design and in its tutorial. On the page they
   sit in the METHOD layer (`visual-architecture.md` §2), and the question and the denominator also
   sit in the INSIGHT layer, in the metric's own block (V-4).
2. **Unknowns inside a metric.** How `not_researched`, `not_publicly_determinable` and
   `not_applicable` enter a count or a share. They are never zero, never dropped silently, and never
   folded into the denominator without saying so. A metric with unknowns in its population shows
   them as their own part (for example, "2 links stated, 1 inferred, 2 unknown"), drawn in the gap
   style (§9).
3. **A metric that cannot be computed.** What the page and the result show for each of the three
   metrics without a population, and what evidence would make each computable. In the grammar this
   is a state block (§7.5) in the gap style, not an empty chart and not a zero.
4. **Source age without the clock** (H-3). How an age stays reproducible byte for byte, and how a
   reader learns which date it is measured from. V-5 forbids ages relative to today. An age "as of"
   a stated reference date is not relative to today, but the design must say so explicitly.
5. **Undated sources.** How a source dated by its access date is kept apart, so its "age" is never
   read as the age of its content. This needs the evidence-date basis column (§04 debt).
6. **DT-S13-4.** Does the source-age metric, measured against a stated date, serve as the
   ageing report S13 asked for? If it does not, what is still missing?
7. **No composite.** How the page keeps the metrics apart, so that no one number reads as a
   "dependency" or "risk" score. One block per metric, each with its own question, denominator and
   tutorial; no block combines two metrics.
8. **DT-7.** Whether any metric combines `vendor` with `designs`, or `supplier` with `supplies`.
   If one does, how they stay in separate columns.
9. **Rows or records** (new from S14.5). For every count: does it count rows of a result (for
   example, accelerator × link) or records (edges, candidates, claims)? Where one record appears in
   several rows, the block says so (D-124, rule 4).
10. **The prototype's tallies** (new from S14.5). For each of the three, does S15 keep it as a
    presentation tally, replace it with a SQL metric (with its tutorial), or retire it? A metric that
    replaces a tally must give the same number, or explain the difference.

## 07 — Tasks

1. **Opening:**
   - confirm Part A;
   - ask H-1 to H-4;
   - confirm in one line the correction of `sql-layer.md` §7's publisher sentence (status line only).
2. **The design**, proposed with D-127 onward: `docs/architecture/metrics.md` (or a new part of
   `sql-layer.md`, as the design argues). It covers §06 for every metric, and the evidence-date
   basis column.
3. **Checks first** (fail before the code exists):
   - an independent plain-Python computation of each metric;
   - a planted `not_researched` counted as unknown, never as zero;
   - a change to the reference date that changes the ages and nothing else (if H-3 A);
   - an access date flagged as one on its row;
   - each metric's tutorial matching its query file;
   - no number shown for a metric with no population;
   - each metric's denominator in the same block as its number (the IN-3 pattern).
4. **The queries:** one file per metric in `sql/`, each its own tutorial (D-121), with results in
   `sql/results/`.
5. **The page:** the metrics where H-4 places them, through the grammar of `visual-architecture.md`
   §7. Each metric:
   - opens with its question in plain words;
   - shows its population and denominator beside the number;
   - shows its unknown part in the gap style;
   - has its own "How this was computed".
6. **The human's task** (Part A), before Claude's explanation:
   - for each metric, the population, the denominator and what it does not measure, one question
     at a time;
   - asked as a form, or as interactive questions with candidate answers if the human prefers
     (S14);
   - the outcome is recorded per question (D-114).
7. **Validation:**
   - fail-first;
   - the merged break harness: all S13, S14 and S14.5 breaks plus new metric breaks, each failing
     for its named reason;
   - browser QA at 1280 and 375 px on every page that changes.
8. **Documentation:** `README.md`, `docs/README.md`, baseline rows; `SESSION-15-REPORT.md`.

## 08 — Explicit non-goals

- **Any composite score**: "dependency", "risk", "exposure" or similar (Part A: never).
- **Rankings**, and any metric presented as a statement about the world when its population is
  what the Atlas recorded.
- **A concentration metric over company headquarters or roles** (§03, the trap).
- **New sources, claims, edges or entities**, unless H-1 B is chosen; then only through staging and
  the human's review.
- **An age computed from the clock**, at build time or in a committed result.
- **A database server, an ORM, a notebook or a frontend framework.** No script in a page unless H-3
  C is chosen; the research view's filter stays CSS only.
- **Changing S14.5's rules** (the grammar, the semantics, the binding rule) without a superseding
  decision. A metric that does not fit them is a stop condition (§16), not a quiet exception.
- **The researcher product** (S20): navigation, question cards, profiles.
- **Public deployment** (NG-13); anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **A metric is a derivation** (`DERIVATION`). It lives in `sql/results/`, never in `data/`, and is
  rebuilt by `tools/warehouse.py`.
- **The build renders, it does not compute** (D-124). Every metric value is a cell of a SQL result,
  never a number computed in `build_page.py` or `build_insight.py`.
- **Unknown is never zero.** Every count and share shows its unknown part next to its known part.
- **Denominators are visible.** No percentage appears without the number it is a share of, and the
  name of that population, in the same block.
- **Determinism.** No clock and no random order; every query ends in `ORDER BY`. Results are byte
  identical across runs.
- **Reader first (D-116).** Each metric opens with its question and what it does not prove, in plain
  words; codes and IDs come after.
- **Colour.** The amber is used for gaps only; no metric gets a status colour (good, warning, bad).
  No new hue enters the palette without a decision.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Analyst | `sql/` queries and their generated results; the metrics design | every metric answers PEF §8 |
| Data Auditor | `tests/`, `tools/warehouse.py` (only if a metric needs a loader change), the merged break harness | checks first; an independent computation per metric |
| Knowledge Architect | the metrics design's definitions; `decisions.md` (append) | populations, denominators, unknowns, rows vs records |
| Editorial | the page sections' framing and the tutorial text | plain language, no fact not in a record, no "risk" wording |
| QA | the report (browser findings) | every page that changes |
| Source Scout, Extractor, Verifier | staging only, under H-1 B | the source policy; the human's review |

## 11 — Data and evidence rules

- **Canonical records:** read only. Under H-1 B, new records go to staging only.
- **Derived output:** generated, never edited; it records the digest of its inputs.
- **Provenance:** every metric value can be traced to the rows it counts, and each row to its
  records. A metric block opens its rows (as the prototype's unit squares open table rows).
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

- `tools/build_page.py`, `tools/page_template.html`, `tests/test_page.py` (H-4 A);
- `tools/build_insight.py`, `tools/insight_template.html`, `tests/test_insight.py` (H-4 C, or if
  `accelerator_dependencies.sql` gains a column the prototype must show);
- `sql/accelerator_dependencies.sql`, only to add the evidence-date basis column; the rows must not
  change;
- `tests/test_warehouse.py`;
- `tools/warehouse.py`, only if a metric needs a table the loader lacks;
- `docs/architecture/sql-layer.md`: the design part and the §7 correction confirmed at the opening;
- `decisions.md` (append);
- `docs/README.md`, baseline rows, `README.md`;
- under H-1 B only: `data/staging/*.json`.

If a shared rendering function is extracted from the two builds (this is the "third composition"
of MA §16.1, and `visual-architecture.md` §6), it goes in `tools/`, with its decision.

**Prohibited:**

- a metric typed or edited by hand;
- a metric computed in a page build;
- a check loosened to pass;
- a new fact entering canonical data;
- an unpinned dependency;
- a composite score.

## 13 — Verification plan

- **At start:** in a fresh virtualenv built from `requirements-test.txt` and
  `requirements-analysis.txt`:
  - the full suite and Gate 0;
  - `tools/warehouse.py --check`, `tools/build_page.py --check` and `tools/build_insight.py --check`.

  Record the base, `git branch -a` and `git ls-remote`.
- **Each metric:** its SQL result equals an independent plain-Python computation.
- **Unknowns:** a planted unknown reaches the metric as unknown; a planted `not_publicly_determinable`
  stays distinct from `not_researched`. Plant it below the data checks (S14 lesson: that state
  needs a search record to be valid data).
- **Reference date** (H-3 A): changing it changes the ages, and only the ages.
- **Access dates:** a source with no date of its own is flagged as access-dated in every row and
  every age that uses it.
- **Uncomputable metrics:** no page shows a number for them; a planted number fails.
- **Tutorials:** a planted change to a query file fails until it is rebuilt (S14 Q1 pattern).
- **Binding rule:** a metric value computed in a page build, instead of read from a result, fails
  (the S14.5 T3 pattern).
- **Pages:**
  - fail-first;
  - the merged break harness;
  - browser QA at 1280 and 375 px for every page that changes.

  CI is reported separately from local results.

## 14 — Evaluation requirements

The report records:

- each metric's PEF §8 answers;
- the result of each metric, and whether it counts rows or records;
- the human's challenge of each denominator and how it compared with Claude's;
- the treatment of the three metrics that have no population;
- what happened to each of the prototype's three tallies;
- deviations and invalidated assumptions;
- debt;
- whether the S15 gate ("transparent metrics") is met.

## 15 — Acceptance criteria

1. Every metric S15 computes states its question, population, denominator and what it does not
   prove, on the page and in its tutorial. The denominator sits in the same block as the number.
2. No metric shows a number over a population the Atlas holds as unknown. The three
   supplier-dependent metrics follow H-1's ruling.
3. Every metric's result equals an independent computation, and regenerates byte for byte from
   versioned inputs.
4. No composite score exists anywhere in the repository or on any page.
5. The human challenged every denominator before Claude's explanation (Part A's human task).
6. Tests and Gate 0 pass in a fresh virtualenv; every page and the results rebuild
   byte-identically; CI is observed or reported as not observed.
7. DT-7 and DT-S13-4 are each resolved or given a new owner. The three break harnesses are merged.
   Every evidence date says whether it is an access date.
8. Every metric value on a page is a cell of a SQL result (D-124). The prototype's three tallies are
   each kept, replaced or retired, as decided.
9. The report satisfies SPEC §5, Part A and D-114.

## 16 — Stop conditions

Stop and report when:

- a metric would need a value only a document holds;
- a metric would have to be written into `data/`;
- a metric's denominator cannot be stated in plain words;
- a number would have to stand in for an unknown;
- a metric cannot be shown within the grammar and semantics of `visual-architecture.md` without
  changing them;
- any condition in SPEC §2.16 or `CLAUDE.md` §18 applies.

**Human decisions** (asked at the start, `CLAUDE.md` §9A; recorded as outcomes, D-114):

- **Part A:** confirm as assembled, or amend.
- **One-line confirmation:** `sql-layer.md` §7's sentence "every row today has one publisher" is
  corrected to say that the inferred rows rest on two publishers each. Only that sentence and its
  status line change; no result, check or page changes.
- **H-1 — Human decision required: what S15 does with the three metrics that have no data.**
  - *What we are deciding:* supplier count, geographic concentration and single-source
    relationships all need to know who supplies a part. The Atlas records no supplier: both HBM
    supplier fields are "not researched", and no `supplies` edge exists. What should S15 do with
    these three?
  - *What will concretely change:*
    - Under A, the page shows each of the three by name, in a gap-style state block, with "cannot be
      computed yet", the reason ("no supplier recorded; 2 of 2 not researched") and what evidence
      would make it computable. There is no number, and the results file records the same state.
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
      unknown, over the links the Atlas records around it. The count is over **rows** (accelerator
      × link). For example, the H100 has 4 links: 1 stated, 1 inferred, 2 gaps. Each block says that
      the 8 rows come from 5 records, because one link is shared and an unknown supplier sits on the
      link it qualifies. The result is two small breakdowns. They replace the prototype's "links on
      stated evidence" tally, with the same numbers now computed in SQL.
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
    date, because a committed result would then change every day, and S14.5's rule V-5 forbids
    ages relative to today.
  - *What will concretely change:*
    - Under A, the query file holds a reference date, changed only by a commit. Ages are measured
      from it, and the page says "age as of <that date>". Every age that rests on an access date is
      flagged as such. The results stay byte-identical until someone moves the date.
    - Under B, no age is computed. The pages keep showing dates only, as they do now, and the reader
      does the arithmetic.
    - Under C, a small script in the page computes ages on the day it is opened. The page then
      runs code and differs from day to day. Three rules would have to change: the byte-identical
      rebuild, the research view's "no script" check (IN-9) and S14.5's V-5.
  - *Why:* Part A asks for source age; S13 asked for a way to see evidence passing the 12-month
    horizon (DT-S13-4).
  - *Future consequences:* A gives a reproducible "as of" age and a natural place for the ageing
    report. B is simplest but leaves DT-S13-4 open. C is always current but gives up the pages'
    reproducibility.
  - *Options:*
    - **A — Against a reference date kept in the query file (recommended).**
    - **B — Dates only, no age.**
    - **C — Computed in the page when it is opened.**
  - *Decision requested:* "Choose A, B or C."
- **H-4 — Human decision required: where the metrics appear.**
  - *What we are deciding:* which page shows the metrics.
  - *What will concretely change:*
    - Under A, the HBM journey page gains a section, "What the Atlas can and cannot measure", after
      "The chain as a table". Each metric has its own "How this was computed" tutorial. The
      research view keeps its tallies unchanged.
    - Under B, a new page shows the metrics, linked from the HBM page.
    - Under C, the metrics replace the indicator blocks of the research view
      (`site/hbm-insight/index.html`). Its presentation tallies become SQL metrics, each with its
      tutorial in the method layer. The three metrics without data appear there as "cannot be
      computed yet" blocks. The journey page stays as it is.
  - *Why:* S14.5 designed the indicator block (`visual-architecture.md` §7.5) as the place a metric
    is shown, and built one page that uses it.
  - *What stays the same:* the metrics, their queries and their checks are the same under every
    option; only where they are shown changes.
  - *Future consequences:*
    - A puts the metrics next to the full evidence, but makes a long page longer, and leaves two
      ways of showing counts (the tallies on one page, the metrics on the other).
    - B adds a third page to maintain.
    - C uses the layout built for metrics and retires the tallies, so every number on that page
      comes from SQL. The research view stays a prototype, not published.
  - *Options:*
    - **A — A section on the HBM journey page.**
    - **B — A new metrics page.**
    - **C — In the research view's indicator blocks (recommended):** one layout for metrics, every
      number from SQL.
  - *Decision requested:* "Choose A, B or C."

## 17 — Deliverables

- The metrics design and D-127 onward.
- One query per metric, with its results and its tutorial.
- The evidence-date basis column, with its check.
- The checks, including an independent computation per metric.
- The page section or blocks (H-4), rebuilt, with browser QA.
- The merged break harness and its results.
- `README.md`, `docs/README.md` and baseline rows; `sessions/reports/SESSION-15-REPORT.md`.

## 18 — Handoff

S15's report must hand S16 (the analytical audit):

- **Completed work:** each metric, with its PEF §8 answers; whether the gate is met.
- **For S16:** for every metric, what it measures, what it does not, which missing data could
  distort it, and how a user could misread it. These are S16's own required questions, with
  S15's answers to check. They include whether a block could be misread through its presentation:
  its encoding, its colour, its order, or a number read without its denominator.
- **Open issues:** debt with owners, including what evidence would make the supplier metrics
  computable.
- **Recommended next decision:** whether S16 audits the metrics only, or also the decision taken
  at H-1 and S14.5's binding rule as applied.
- **Files for S16 to read first:**
  - the S15 report;
  - the metrics design;
  - `sql-layer.md`;
  - `visual-architecture.md` §7 and §10.
