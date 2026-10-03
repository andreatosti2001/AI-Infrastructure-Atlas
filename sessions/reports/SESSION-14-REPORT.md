# SESSION-14 Report — The SQL layer

- **Session:** S14 · **Type:** ARCHITECTURE / IMPLEMENTATION · **Milestone:** M4 — Analytical
  Intelligence (first session)
- **Date:** 2026-10-03
- **Prompt:** [`sessions/prompts/S14-PROMPT.md`](../prompts/S14-PROMPT.md), followed as written
  (Part A confirmed at the opening, unchanged).
- **Branch:** `claude/new-session-f8y32i`, created at `main` @ `cc99f57` (the PR #23 merge, which
  carries S13 and this prompt).
- **Base** (D-018 L-03), at the start: `git branch -a` showed `claude/new-session-f8y32i` and `main`,
  with their two remotes, all at `cc99f57`. `git ls-remote` showed `HEAD` and `main` at `cc99f57`,
  `claude/new-session-4kuwvw` at `2759111`, and the older `claude/*` branches as S13 listed them.
- **Commits:**
  - `bc62560` (H-0);
  - `bed8bce` (DT-1);
  - `c93ad9d` (the SQL layer, the page section);
  - `432b7b8` (documents);
  - `b8df903` (the tutorial after the human's reading);
  - and the commit that adds this report.

## Mission outcome

**Delivered: a SQL layer rebuilt from `data/` on every run, its first query answered, and the result
on the HBM page with its "How this was computed" tutorial. The human read the query before
Claude's explanation.**

- **DT-1 first (H-1).** 28 per-record values left four design-document tables for
  `data/identity_basis.json`, with a schema and checks (D-117). The SQL layer and the checks no
  longer read Markdown for them.
- **The SQL layer** (`docs/architecture/sql-layer.md`, D-118, D-119):
  - `python tools/warehouse.py` loads the canonical files into a fresh in-memory DuckDB, runs
    `sql/*.sql`, and writes `sql/results/*.json` with the digests of everything it read.
  - The database is never stored, never committed and never written back.
  - Unknowns keep their own words in SQL; NULL appears only beside a state that explains it.
- **The first result** (D-120): for each accelerator on the page, every link the Atlas records,
  with its basis (stated / inferred / gap), its evidence dates, its publishers and its caveats.
  8 rows, 4 per accelerator, matching the diagram line by line. A plain-Python recomputation of
  the same definitions gives the same rows (WH-10).
- **The page** (D-121, H-3): a new section, "The chain as a table", follows "The chain". Beside it
  is a closed "How this was computed" tutorial generated from the query file, character for
  character. The page build still uses the standard library only.

**Restated contract** (at the start):

- **Mission:** a SQL layer rebuilt from `data/` that never becomes where facts live; one first
  question answered with it; that answer on the page with a short tutorial of its query; the
  human able to read and explain the query.
- **Non-goals:** Part B §08: no metrics, counts, shares or scores; no new sources, claims, edges
  or entities; no server, ORM, notebook or framework; no committed database; no deployment.
- **Acceptance:** Part B §15.
- **Plan:**
  1. opening decisions;
  2. DT-1 (checks first, scripted migration);
  3. the design;
  4. checks first;
  5. the SQL layer;
  6. the page;
  7. the human's reading;
  8. breaks and browser QA;
  9. documents and this report.

  The plan held; the reading came after the page (Deviations, 4).

**Decided by the human** (2026-10-03; outcomes only, D-114):

| Decision point | Outcome | Effect |
|---|---|---|
| The session prompt (Part A) | followed as written | prompt unchanged |
| S13 audit's maturity ratings (H-0) | accepted, unchanged (process 3, outcome 2) | two status lines (`bc62560`) |
| When the document tables move into the data (H-1) | first, inside S14 | D-117; `bed8bce` |
| The SQL engine (H-2) | DuckDB, pinned; the page reads saved results | D-118 |
| Where the first result appears (H-3) | a section of the existing HBM page | D-121 |
| The reading form | asked as questions with candidate answers, not as a free-text form | Deviations, 4 |

## Files changed

| File | Change |
|---|---|
| `data/identity_basis.json`, `data/staging/identity_basis.json` | new: 28 rows moved from the documents; staging empty (D-117) |
| `schemas/identity_basis.schema.json` | new (proposed, D-117) |
| `docs/architecture/concept-dataset.md` §3, §5, §7; `facility-dataset.md` §2, §4; `company-dataset.md` §2 | tables of per-record values replaced by pointers to the rows; restated columns removed; rules unchanged |
| `tests/test_data_entities.py` | the CI-1, PI-1, IO-1, FI-1 and FK-1 rows read from data; check logic unchanged |
| `tests/test_data_identity_basis.py` | new: IB-1 to IB-4 and planted faults |
| `tools/warehouse.py` | new: the loader, the runner, `--check`, `--db` |
| `sql/accelerator_dependencies.sql`, `sql/results/accelerator_dependencies.json` | new: the first query (also its tutorial) and its generated result (11,000 bytes) |
| `tests/test_warehouse.py` | new: WH-1 to WH-10, one break test |
| `requirements-analysis.txt`; `.github/workflows/ci.yml` | new pin `duckdb==1.5.6`; CI installs it (Deviations, 1) |
| `tools/build_page.py`, `tools/page_template.html` | the section, its tutorial and styles; `sql/` among the inputs |
| `tests/test_page.py` | PG-11; `sql/` among the inputs; the identity-basis file is not a record home |
| `site/hbm-chain/index.html` | rebuilt (326,153 bytes) |
| `docs/architecture/sql-layer.md` | new: the design (proposed) |
| `docs/architecture/decisions.md` | D-117 to D-121 appended (proposed) |
| `docs/research/content-audit-S13.md`, `docs/quality/audit-history.md` | status lines (H-0) |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows |
| `sessions/reports/SESSION-14-migration/` | the DT-1 migration script and its fail-first output (DT-8) |
| `sessions/reports/SESSION-14-breaks/` | DT-1 and SQL break scripts; S13's breaks re-run; their outputs |
| `sessions/reports/SESSION-14-qa/` | browser QA script (S13's, plus one block), results, twelve screenshots |

## Data changed

- **New canonical file, no new fact:** `data/identity_basis.json` holds the 28 rows the four
  document tables held. Every value came from a parsed cell, by script. Before any document was
  edited, the script asserted that the JSON returns exactly the tuples the Markdown returned.
- **No source, claim, entity, event, relationship or refused-candidate record was created or
  edited.**
- **Derived, committed:** `sql/results/accelerator_dependencies.json`, generated, never edited.
- Measured at `b8df903`:

  | Record kind | Count |
  |---|---|
  | sources | 52 |
  | claims | 120 |
  | entity records | 33 |
  | events | 4 |
  | relationships | 5 |
  | refused candidates | 12 |
  | identity-basis rows | 28 |

  Staging is empty.

## Tests run

Python 3.11.15. "Fresh venv" means a virtualenv built from the pinned files in the scratchpad;
`pip freeze`, sorted, equalled the pins.

| Command / check | Result |
|---|---|
| **At start** (`cc99f57`), fresh venv | OK (301 tests); `Repository integrity: OK`; `page: up to date` |
| DT-1 **fail-first** (checks written, no data yet) | 48 failures, 12 errors, each "no … rows in data/identity_basis.json" or IB-1–IB-4 (`dt1-failfirst.txt`) |
| DT-1 after the migration | OK (313); the missing D-117 was caught first by the cited-decision check |
| SQL **fail-first** | `test_warehouse.py`: `ModuleNotFoundError: warehouse`. PG-11: "no SQL table on the page", no tutorial, inputs list without `sql/` |
| `tools/warehouse.py` run twice | byte-identical results; `--check`: up to date |
| `--db` inside the repository | refused (exit 2); outside it saves a database file holding the 120 claims |
| Page build on a Python **without DuckDB** | `page: up to date` (PG-7 needs no SQL engine) |
| **Final** (`b8df903`), fresh venv with both pin files | OK (328 tests); Gate 0 OK; page and results up to date |
| **CI** | runs 119 (`bed8bce`), 120 (`c93ad9d`): success, DuckDB installed by the new step. Run 121 (`432b7b8`) and the later commits: not observed at writing |

### Deliberate breaks

Each break edits a fresh copy, rebuilds where stated, and counts only if the suite fails with the
named fragment in its output.

- **DT-1** (`dt1-breaks-result.txt`): 8 of 8 caught, the control passes:
  - a product term changed;
  - a concept term changed;
  - a kind's basis removed;
  - a class basis pointed elsewhere;
  - a facility term not in an anchor;
  - a gap given a record;
  - a row put back in a document;
  - a legal name restated in a document.
- **SQL layer** (`sql-breaks-result.txt`): 12 of 12 caught, 2 controls pass:

  | # | Break | Caught by |
  |---|---|---|
  | Q1 | the query file changed, nothing rebuilt | WH-2 (stale result), PG-11 (other query version) |
  | Q2 | query changed, results rebuilt, page not | PG-7, PG-11 tutorial |
  | Q3 | the final `ORDER BY` removed | WH-8 |
  | Q4 | a tutorial line names a record | WH-9 |
  | Q5 | evidence dated by the oldest source date | WH-10 (independent computation) |
  | Q6 | every refused candidate admitted as a gap | WH-10 |
  | R1 | a result cell hand-edited | WH-2, PG-11 |
  | R2 | data changed, results not rebuilt | WH-2 |
  | P1 | a table cell on the page hand-edited | PG-11, PG-7 |
  | P2 | the tutorial's code hand-edited | PG-11 |
  | P3 | a caveat flag removed | PG-11 |
  | L1 | the loader turns states into `value` | WH-4 |
  | C1, C2 | controls: a tutorial sentence; a display name, rebuilt | pass |

  A first C2 was invalid data, not a control: it planted the H100 supplier as
  `not_publicly_determinable` without the search record that state requires (ER-3). The schema
  and the edge checks refused it. WH-5 plants that state below the data checks.
- **S13's breaks re-run** (`s13-breaks-rerun-result.txt`): 30 caught, 2 controls pass. Break 25 (a
  stored status on a candidate) is now also caught by the loader's key contract. S12's #3, #14 and
  control E are still not scripted.

## Browser QA (D-106)

Playwright from `/opt/node-tools` with the pre-installed Chromium: S13's script plus one block for
the new section ([`qa.js`](./SESSION-14-qa/qa.js), [`qa-result.json`](./SESSION-14-qa/qa-result.json)).

| Check | 1280 px | 375 px |
|---|---|---|
| Console messages, page errors, network | none, none, the page file only | same |
| Document overflow; wide elements | 1280 / 1280; none | 375 / 375; none |
| The section, every disclosure open: elements wider than the viewport | none | none |
| Table layout | a table | stacked cards, each cell labelled |
| Tutorial closed at load; opens by keyboard | yes; yes | yes; yes |
| Diagram marks reached by Tab; Enter lands on each panel | 17 of 17; all | same |
| Contrast: whole page; the section with disclosures open | min 6.21:1; min 6.42:1; none below 4.5 | same |

Two defects found and fixed before the final run: an empty "Caveats" heading on phone cards, and
words broken mid-word in a narrow column.
Screenshots: [`desktop-05-table.png`](./SESSION-14-qa/desktop-05-table.png),
[`mobile-05-table.png`](./SESSION-14-qa/mobile-05-table.png),
[`desktop-06-table-tutorial-open.png`](./SESSION-14-qa/desktop-06-table-tutorial-open.png).

## The first query and its result

*For each accelerator on the page, which links does the Atlas record around it, on what basis, and
how old is the evidence?*

| Accelerator | Link | Basis | Evidence dated | Caveats |
|---|---|---|---|---|
| AWS Trainium2 | Amazon designs AWS Trainium2 | stated | 2023-11-28 | one publisher; publisher not linked (`src-052`) |
| AWS Trainium2 | AWS Trainium2 incorporates HBM | stated | 2026-10-01 (access date: the page states no date) | one publisher; publisher not linked (`src-043`) |
| AWS Trainium2 | HBM · supplier | gap: not researched | not applicable | — |
| AWS Trainium2 | HBM requires 3D die stacking | inferred | 2018-06-08 to 2020-12 | rests on the Atlas's own definitions |
| NVIDIA H100 | TSMC fabricates NVIDIA H100 | gap: evidence not fresh | 2025-07-22 | one publisher; publisher not linked (`src-042`) |
| NVIDIA H100 | NVIDIA H100 incorporates HBM | stated | 2025-07-22 | one publisher; publisher not linked (`src-051`) |
| NVIDIA H100 | HBM · supplier | gap: not researched | not applicable | — |
| NVIDIA H100 | HBM requires 3D die stacking | inferred | 2018-06-08 to 2020-12 | rests on the Atlas's own definitions |

Each row also carries its edge or candidate, the edge through which it is reached, its claims, its
sources, and the claim that makes its product an accelerator.

## The human's reading (task 7; DT-11, F-11)

Asked on 2026-10-03, before Claude's explanation, with the query's explanations hidden: one
question per point, each with candidate answers (some wrong, none marked) and a free answer.
Outcomes only (D-114):

| Question | Compared with Claude's reading |
|---|---|
| What `walked_links` does | differed: read as finding suppliers. It walks what the parts need; suppliers are a separate row |
| What `gap_rows` holds | matched |
| What `reached` and `evidence` give a row | differed: read as counting agreeing sources. They list and date sources; nothing counts, and sources listed together do not confirm one another |
| What one row means (the inferred "requires" row) | matched |
| What would make a row wrong | the human named a cause Claude had not listed: the world changing after the evidence date, so a correct row read as current misleads. Claude's three causes (stale result, the query's definitions, a wrong record) were not chosen |

**Effect:** two sentences were added to the tutorial where the readings differed (`b8df903`); the
rows did not change. The "counting" reading is the corroboration misreading S13 warned about
(audit Part 5). The page and the tutorial now both say it in plain words.

## Evidence added/retired

None. No source was retrieved. DuckDB's documentation was not cited as evidence.

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-117 | the document tables of per-record values become identity-basis rows (DT-1) | proposed (the move decided by the human at H-1) |
| D-118 | DuckDB rebuilt in memory from the canonical files; results committed; page build unchanged | proposed (engine and place decided at H-2) |
| D-119 | explicit states in SQL: value and state columns; NULL only beside a state | proposed |
| D-120 | the first query: definitions of accelerator, link, basis, evidence date, caveats | proposed |
| D-121 | the tutorial lives in the query file; the table is a section of the HBM page | proposed (placement decided at H-3) |

**Rejected alternatives:**

- a committed database file;
- DuckDB in the page build;
- SQLite;
- DuckDB's JSON reader (its type inference turns state objects into structs);
- loading staging;
- CSV results;
- new entity fields for DT-1 (would need `trace.py` and `navigate.py` edits);
- keeping the restating tables with checks (two more Markdown parsers);
- tutorial text in a separate file;
- an "age in days" column (needs the clock);
- every refused candidate as a gap row;
- the lane on the table;
- counting publishers (a metric).

Each rejection is detailed in its decision and in `sql-layer.md` §10.

## Deviations

1. **`.github/workflows/ci.yml` is not in Part B §12's list.** It gained one install step. The
   human's H-2 option stated that CI installs the pinned engine, so the change was made on that
   decision.
2. **`tests/test_data_entities.py` was edited and `tests/test_data_identity_basis.py` created**
   under DT-1's "checks"; `tests/test_page.py`'s record loader skips the identity-basis file (its
   rows have no ID).
3. **The two restating tables lost a column** rather than gaining a check (D-117). One "why"
   sentence was reworded so it still reads without the removed column.
4. **The reading came after the page, as questions with candidate answers**, which the human asked
   for in place of a free-text form. It covered 3 of the query's 10 named parts in question 1
   (the walk, the gaps, the evidence), plus the meaning of a row and what makes a row wrong.
5. **The tutorial changed after the reading** (two sentences); the result rows did not.
6. **The first control C2 was invalid data**, replaced (Deliberate breaks).

**Invalidated assumptions:**

- "DT-1 makes the session large": it was 25 table rows (28 data rows) and two column removals.
- "D-099 shows its evidence date" in the first result: M16 is not on an accelerator's chain, so
  it is not a row; the page's lane still shows it.
- F-1's evidence date is the access date for a source that states no date. For Trainium2's HBM
  edge, the row shows 2026-10-01, which looks recent but only dates the reading of a live page.
  The page framing says so; it is a limit for S15 to carry (below).

## Debt introduced/resolved

**Resolved:**

- DT-1 (D-117);
- DT-4: flattening rules and tables (`sql-layer.md` §3, §8); "the actors on the chain" is now a
  query;
- DT-9 in part: the four tables' parsers are gone; the rule-table readers stay by design.

**Re-owned:**

| ID | Disposition |
|---|---|
| DT-3 | before the first export that leaves the repository (client output, M6), Data Auditor; results inside the repository are rebuilt from current IDs |
| DT-7 | not triggered (the query uses the `designs` edge, never `vendor`); due at the first S15 metric that combines them |
| DT-S13-2 | honoured: no capacity figure read |
| DT-S13-4 | honoured: no age, no "current"; the ageing report itself stays with S01's gate / Change Detector |
| DT-S13-7 | honoured: shown as "rests on the Atlas's own definitions" |
| DT-S13-1 | shown per row (`party_standing_unchecked`); the rule for web publishers stays with the Knowledge Architect |

**Introduced:**

- an access date standing as the evidence date of an undated page (owner: S15, as a flag on any
  metric using evidence dates);
- `sql_breaks.py` and `breaks.py` are two harnesses (owner: the next session that changes the page,
  to merge them);
- the reading covered 3 of 10 parts (owner: the next reading, one field per part).

## S14 gate

"All published metrics can be regenerated from versioned inputs": **met for what exists.** No metric
is published yet. The one SQL result is regenerated byte for byte from versioned inputs, checked in
CI (WH-1, WH-2), and records the digests of its inputs.

## Unresolved issues

**Human decision required: should the five S14 design decisions become the project's rules as
built?**

- *What we are deciding:* whether D-117 to D-121, and the design document
  `docs/architecture/sql-layer.md`, move from "proposed" to "accepted".
- *What each one fixes:*
  - **D-117:** the words record IDs are built from, and which claim proves a product's class or a
    facility's kind, live in `data/identity_basis.json`, never again in document tables.
  - **D-118:** the Atlas depends on DuckDB 1.5.6. The database is rebuilt in memory on every run
    and never stored. Results are committed files that the page reads without DuckDB.
  - **D-119:** in SQL, every unknown keeps its own word (not researched, not applicable…). An empty
    SQL value is allowed only next to the word that explains it.
  - **D-120:** the first table's definitions:
    - what counts as an accelerator;
    - which links are listed;
    - when a link is stated, inferred or a gap;
    - how evidence is dated;
    - which caveats each row shows.
  - **D-121:** every SQL tutorial is written as comments inside its query file, and the HBM page
    keeps "The chain as a table" with its tutorial.
- *What will concretely change:* if accepted, the status lines of the five decisions, of
  `sql-layer.md` and of the identity-basis schema change; the page's digest line follows. No data,
  query result or check changes.
- *Why:* S15's metrics build on these tables and definitions; accepting them makes them binding
  rather than provisional.
- *What stays the same:* the data, the result, the page's content.
- *Options:*
  - **A, all five binding as built:** status lines only.
  - **B, named items changed first:** Claude rewrites the named items, and the code, data and
    checks they affect, before acceptance.
  - **C, named items dropped:** what depends on them is removed or rebuilt. For example, dropping
    D-120 removes the table from the page.
- *Decision requested:* "Choose A, B or C, naming items for B or C."

**Inherited, unchanged:**

- TSMC → H100 `fabricates` (D-092);
- the HBM supplier of each product (D-094);
- the AWS legal entity (D-093, DT-6);
- subsidiary records (D-095);
- S01's weekly gate;
- evidence ageing past the horizon (Micron's 10-K turns 12 months old today, 2026-10-03, DT-S13-4);
- the S13 debt register;
- S12's breaks #3, #14 and control E not scripted.

**Not asked now:** merging this branch to `main`; public deployment (NG-13).

## Addendum: the S14 review (2026-10-03)

Accepted by the human on 2026-10-03: D-117 to D-121 bind as built, with `sql-layer.md` and
`schemas/identity_basis.schema.json`. Only status lines changed, and the page's digest line
followed. No data, result or check changed.

## Process lessons

- **A second implementation is a cheap oracle.** The plain-Python recomputation (WH-10) caught both
  semantic breaks (Q5, Q6) that every structural check let through.
- **Check that a control is valid data before trusting it.** The first C2 tested the schema, not the
  SQL layer.
- **A reading shows where an explanation is weak.** Two of the human's answers differed from
  Claude's, both where the tutorial was silent (what the walk does not do; that listing is not
  counting).
- **A ban on a word reaches the tutorial too.** "none" in two explanations failed RR-7 on the page,
  correctly.

## Implications for the next session

S15 — dependency metrics:

- **Completed work:** the SQL layer, its rebuild (`python tools/warehouse.py`, `--check`), its
  first query and result on the page. The S14 gate is met for what exists.
- **Tables a metric may use:** every table in `sql-layer.md` §8, through views in `sql/`, never by
  editing `data/`.
- **Populations and honest denominators:**
  - the 5 edges;
  - the 120 claims;
  - the 99 citations on 85 cited claims;
  - the 2 accelerators;
  - the 8 links of the first result.

  Each is a census of what the Atlas holds, not of the world. A share over them describes the
  Atlas's coverage, never the industry.
- **Weaknesses every metric must carry:**
  - a single publisher per value (no corroboration);
  - inferences that rest on the Atlas's own definitions;
  - party standing unchecked;
  - evidence dates that are access dates for undated pages;
  - no "current" without an age, and no age without a clock (a report, not a committed result);
  - `not_researched` as its own category, never zero.
- **Open issues:** the debt above, with owners.
- **Recommended next decision** (for S15's opening, to be asked in §9A form): the first metric and
  its denominator. Claude's proposal: for each accelerator, how its recorded links divide into
  stated, inferred and gap, over the links the Atlas records for it. It measures how much of the
  chain rests on direct evidence, not how dependent the world is.
- **Files for S15 to read first:**
  - this report;
  - [`docs/architecture/sql-layer.md`](../../docs/architecture/sql-layer.md);
  - [`docs/research/content-audit-S13.md`](../../docs/research/content-audit-S13.md) Part 5.

**Next recommended milestone:** S15, the first metric on the SQL layer, with its question,
population and denominator decided before any SQL is written.
