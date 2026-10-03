# AI-Infrastructure-Atlas — S14 Session Prompt

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

Add the reproducible analytical warehouse.

### Human learning target

- understand canonical vs derived data;
- read and explain the key SQL queries.

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
> - Everything above this line is **Part A**. Claude assembled it at the end of S13, after the human
>   approved writing the S14 prompt (2026-10-03). The operating contract and the report list are
>   S13's Part A, word for word; the mission and the learning target are the operational roadmap's
>   week-6 entry for S14 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`, "S14 — DuckDB / SQL
>   layer"), word for word.
> - Part B is Claude's elaboration into SPEC §2's 18 sections, written after S13
>   (`SESSION-13-REPORT.md`, `docs/research/content-audit-S13.md`, D-111 to D-116).
> - Part B adds detail only. **If the two ever conflict, Part A governs.** `CLAUDE.md` and
>   `MASTER-ARCHITECTURE.md` govern both. The prompt becomes immutable once S14 begins (D-011).
> - **New since S13, binding here:** decisions are recorded as outcomes and dates, never as
>   transcripts (D-114); every result a page computes with SQL carries a "How this was computed"
>   tutorial (D-115); pages and documents put plain-language meaning first (D-116).
> - **Not yet answered:** Part A's confirmation and H-0 to H-3, asked at the start of S14.

## 01 — Session identity

- **Session:** S14 · **Title:** DuckDB / SQL analytical layer
- **Type:** ARCHITECTURE / IMPLEMENTATION (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`: "reproducible
  SQL layer")
- **Milestone:** M4 — Analytical Intelligence (first session). M3 closed in S13.
- **Predecessor:** S13 — content and evidence depth audit. **Successor:** S15 — dependency metrics.
- **Complexity:** large if DT-1 is done here (H-1 A); medium otherwise.

## 02 — Mission

Give the Atlas a SQL layer it can rebuild from its JSON records at any time, without the database
ever becoming the place where facts live. Answer one first question with it, show that answer on the
page with a short tutorial of its query, and leave the human able to read and explain that query.

## 03 — Why this session exists

- **The roadmap.** `SESSION-ROADMAP.md` S14: "Introduce a reproducible analytical warehouse without
  making the warehouse the canonical source of truth"; focus: relational views, reproducible SQL,
  source-to-metric lineage, rebuild procedure; gate: "All published metrics can be regenerated from
  versioned inputs."
- **What S13 hands over** (`SESSION-13-REPORT.md`, "Implications for the next session"):
  - safe to compute over: the 120 canonical claims and 5 edges, with each value's basis (stated,
    inferred, gap) and evidence date carried into every result;
  - weaknesses a query must show: no value is corroborated by a second publisher; the H100 capacity
    figures are not computed over (DT-S13-2); D-091 is not independent evidence and D-099 shows its
    evidence date (DT-S13-7); "party" standing is unchecked on 14 citations (DT-S13-1);
    `time_sensitive` values age in place, so "current" needs a computed age (DT-S13-4);
  - recommended first question: *for each accelerator on the page, which dependencies does the
    Atlas record, with what basis and what evidence date?*
- **Debt due now** (`M2-audit.md` Part 4): DT-1 (four document tables of per-record values move to
  `data/`, due before S14: "the SQL layer must not parse Markdown"), DT-3 (ID stability, before the
  first export), DT-4 (flattening for SQL), DT-7 (`vendor` vs `designs`, `supplier` vs `supplies`,
  when a query combines them), DT-9 (with DT-1).

## 04 — Current state

As of `main` after S13 is merged. **S13 (`claude/new-session-4kuwvw`, with this prompt) must be on
`main` before S14 starts.** Verify, and record the base, `git branch -a` and `git ls-remote`.

- **Data:** 52 sources; 120 canonical claims; 33 entity records; 4 events; 5 relationships; 12
  refused candidates; staging empty.
- **Checks:** 301 tests and Gate 0 in CI; the page is rebuilt byte-identically from its inputs.
- **Tooling:** standard library only (D-003), plus pinned test-only `jsonschema` (D-026). **No SQL
  engine is installed in the repository.** Adding DuckDB is a new dependency and needs an approved
  decision (H-2).
- **Status:** the S13 audit's maturity ratings are proposed (H-0).

**Not S14's:** metrics, shares, counts, concentration or any score (S15); a composite risk score
(never); new sources, claims or edges; public deployment (NG-13).

**Next decision number:** D-117.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-13-REPORT.md`; `docs/research/content-audit-S13.md` Parts 5 to 7.
2. `docs/architecture/milestone-audits/M2-audit.md` Part 2 (Q, T, I), Part 4 (DT-1 to DT-9).
3. `MASTER-ARCHITECTURE.md` §16, §17; `CLAUDE.md` §7, §11, §12; D-003, D-026, D-110, D-115, D-116.
4. The data files and schemas the queries read; `tools/navigate.py`, `tools/build_page.py`.

**External access:** none needed. DuckDB's own documentation may be read to choose versions and
settings; it is not evidence about the world and is never cited as a source.

**Lessons to carry:** write the checks before the data; ask before editing a file the prompt does not
list; a probe beats an argument; measure before estimating; a break must fail for the reason it
names; plain-language meaning first (D-116).

## 06 — Required reasoning

Answer these in the design before building:

1. **Canonical vs derived.** What exactly is loaded from `data/`, what is derived, where derived
   output lives (if anywhere in the repository), and why the database file itself is never
   committed or edited by hand.
2. **Rebuild.** One command rebuilds the database from the JSON files; the same inputs give the same
   query results, byte for byte where they are written out. How is that checked?
3. **Explicit states in SQL.** How `not_researched`, `not_publicly_determinable`, `not_applicable`
   and `null` stay distinct in tables (never collapsed to NULL or zero).
4. **Lineage.** How every row of a query result points back to its records, claims and sources.
5. **The page and the build.** Does the page build stay standard library (reading committed query
   outputs) or run DuckDB itself? What does PG-7 (byte-identical rebuild) need?
6. **The SQL tutorial (D-115).** Where its text lives, how it is generated from the same query file
   the result comes from, and what a reader sees on desktop and phone.
7. **Which S13 weaknesses the first result must show**, and how.

## 07 — Tasks

1. Opening: confirm Part A; H-0 to H-3.
2. DT-1 if H-1 says so: the four document tables become data, with checks and a scripted migration.
3. The design (§06) in `docs/architecture/sql-layer.md`, proposed, with D-117 onward.
4. Checks first: tests for the rebuild, explicit states, lineage, and the tutorial's match with its
   query, failing before the code exists.
5. The SQL layer: load, views, the first query (the lineage table), its written output.
6. The page: the lineage table and its "How this was computed" tutorial (H-3).
7. The human's reading: the query sent with a short form, one field per question (what does each
   part do; what does a row mean; what would make a row wrong), answered before Claude's
   explanation (DT-11, F-11).
8. Validation: fail-first; deliberate breaks, including `SESSION-13-breaks/breaks.py` re-run if the
   page changes; browser QA.
9. Documentation: `README.md`, `docs/README.md`, baseline rows; `SESSION-14-REPORT.md`.

## 08 — Explicit non-goals

- Metrics, counts, shares, concentration, rankings or scores (S15); any composite score (never).
- New sources, claims, edges or entities.
- A database server, an ORM, a notebook environment or a frontend framework.
- Committing the database file; editing derived output by hand.
- Public deployment (NG-13); anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **One home per fact:** JSON records stay canonical; SQL tables are rebuilt from them and never
  written back.
- **Unknown is never zero:** explicit states survive every view and every output.
- **Dependencies:** DuckDB only under an accepted decision, pinned exactly (D-026 pattern).
- **Determinism:** no clock, no random order; every query has an explicit `ORDER BY`.
- **Reader first (D-116):** the page section opens with what the table answers, in plain words.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Knowledge Architect | `sql-layer.md`, `decisions.md` (append), DT-1 schema changes if H-1 A | the canonical/derived boundary |
| Data Auditor | `tests/`, `tools/` (the loader and query runner), the DT-1 migration | checks first |
| Analyst | `sql/` queries and their written outputs | every query reproducible and explained |
| Editorial | the page section's framing and the tutorial text | plain language, no fact not in a record |
| QA | the report (browser findings) | if the page changes |

## 11 — Data and evidence rules

- **Canonical records:** read only, except DT-1's approved migration.
- **Derived output:** generated, never edited; it records the digest of its inputs.
- **Provenance:** every result row carries the IDs that let a reader trace it.
- **Human decisions:** recorded as outcomes and dates (D-114).
- **Confidence:** no numeric values.

## 12 — Implementation rules

**May create:** `docs/architecture/sql-layer.md`; `sql/` (queries); a loader and runner in `tools/`;
derived outputs where the design puts them; tests and fixtures; the DT-1 records, schema and
migration if approved; `SESSION-14-REPORT.md`.

**May modify:** `requirements-test.txt` or a new pinned requirements file (after H-2); `tools/build_page.py`,
`tools/page_template.html`, `tests/test_page.py` (H-3); `decisions.md` (append); the DT-1 source
documents (their tables replaced by pointers); `audit-history.md`; `docs/README.md`, baseline rows,
`README.md`; and, if H-0 is answered A, the status lines of `content-audit-S13.md` and its
audit-history row.

**Prohibited:** an unpinned dependency; a query result typed or edited by hand; a check loosened to
pass; a new fact entering the data.

## 13 — Verification plan

- **At start:** full suite and Gate 0 in a fresh virtualenv; base, `git branch -a`, `git ls-remote`.
- **Rebuild:** the database built twice from the same inputs gives identical query outputs.
- **States:** a planted `not_researched` value survives to the output as itself.
- **Lineage:** every output row resolves to canonical records.
- **Tutorial:** a planted change to the query file fails the tutorial check until rebuilt.
- **Page:** fail-first, breaks, browser QA at 1280 and 375 px; CI reported separately from local
  results.

## 14 — Evaluation requirements

The report records: the design and its rejected alternatives; the first query and its result; the
human's reading of the query and how it compared with Claude's; deviations; invalidated assumptions;
debt; and whether the S14 gate ("All published metrics can be regenerated from versioned inputs")
is met.

## 15 — Acceptance criteria

1. One command rebuilds the SQL layer from `data/`; nothing in it is canonical.
2. The first query answers the lineage question with basis, evidence date and explicit states.
3. The page shows its result with a working "How this was computed" tutorial generated from the same
   query file.
4. The human has read the query in the form of task 7 before Claude's explanation.
5. Tests and Gate 0 pass in a fresh virtualenv; the page rebuilds byte-identically; CI observed or
   reported as not observed.
6. DT-1 is done or re-scheduled by the human's ruling (H-1); DT-3, DT-4, DT-7, DT-9 each resolved or
   given a new owner.
7. The report satisfies SPEC §5, Part A and D-114.

## 16 — Stop conditions

Stop and report when: a query would need a value only a Markdown table holds (and H-1 kept DT-1
out); a derived value would have to be written back into `data/`; DuckDB cannot be pinned or gives
non-deterministic output; any condition in SPEC §2.16 or `CLAUDE.md` §18 applies.

**Human decisions** (asked at the start, `CLAUDE.md` §9A; recorded as outcomes, D-114):

- **Part A:** confirm as assembled, or amend.
- **H-0 — the S13 audit's maturity ratings.** Accepting them changes only the audit's status line
  and its audit-history row; the ratings are unchanged from M2 (process 3, outcome 2).
- **H-1 — Human decision required: when the four document tables move into the data files (DT-1).**
  - *What we are deciding:* whether the per-record values still kept in four design-document tables
    move into `data/` at the start of S14, or later.
  - *What will concretely change:* under A, S14 first moves the four tables (the CI-1, PI-1 and FI-1
    terms; the IO-1 and FK-1 basis rows) into data files with a schema, checks and a scripted
    migration, and the documents keep the rules only; then the SQL layer is built on `data/` alone.
    Under B, a short separate session does that move and S14 waits for it. Under C, S14 builds the
    SQL layer without those values, and any query needing them stops.
  - *Why:* the SQL layer must not read Markdown (D-110), and these values are about named records.
  - *What stays the same:* the records' meaning, the page, the evidence.
  - *Options:* **A — Move the tables first, inside S14 (recommended):** one longer session, and the
    SQL layer is complete from the start. **B — A separate short session first:** smaller steps,
    one more session. **C — SQL without those values for now:** fastest, and the first queries
    cannot use them.
  - *Decision requested:* "Choose A, B or C."
- **H-2 — Human decision required: how the Atlas runs SQL.**
  - *What we are deciding:* which SQL engine the project depends on, and where it runs.
  - *What will concretely change:* under A, DuckDB is added as an exactly pinned dependency used by
    a loader, the queries and the tests; the page build stays standard library and reads the
    committed query outputs. Under B, the same, but the page build also runs DuckDB. Under C, the
    standard library's SQLite is used, with no new dependency.
  - *Why:* D-003 allows a new dependency only with a recorded reason; `MASTER-ARCHITECTURE.md` §17
    names DuckDB.
  - *Future consequences:* A keeps the page build simple and reproducible; B makes the page depend
    on DuckDB's exact output; C avoids a dependency but departs from the architecture and DuckDB's
    analytical features.
  - *Options:* **A — DuckDB for analysis, page reads saved results (recommended)**; **B — DuckDB in
    the page build too**; **C — SQLite from the standard library.**
  - *Decision requested:* "Choose A, B or C."
- **H-3 — Human decision required: where the first SQL result and its tutorial appear.**
  - *What will concretely change:* under A, the existing HBM page gains a section, "The chain as a
    table", with the lineage table and its "How this was computed" tutorial. Under B, a small new
    page shows them, linked from the HBM page.
  - *Options:* **A — A section on the existing page (recommended):** one place to read the chain and
    its table. **B — A new page:** keeps the HBM page unchanged; a second page to maintain.
  - *Decision requested:* "Choose A or B."

## 17 — Deliverables

- `docs/architecture/sql-layer.md` and D-117 onward;
- the loader, the queries, their outputs and tests;
- the page section with its SQL tutorial, rebuilt, with browser QA;
- the DT-1 migration if approved;
- `README.md`, `docs/README.md`, baseline rows; `sessions/reports/SESSION-14-REPORT.md`.

## 18 — Handoff

S14's report must hand S15 (dependency metrics):

- **Completed work:** the SQL layer, its rebuild and its first query; whether the S14 gate is met.
- **For S15:** which tables and views a metric may use; the population and denominator each could
  have; which S13 weaknesses every metric must carry.
- **Open issues:** debt with owners.
- **Recommended next decision:** the first metric and its denominator.
- **Files for S15 to read first:** the S14 report; `sql-layer.md`; `content-audit-S13.md` Part 5.
