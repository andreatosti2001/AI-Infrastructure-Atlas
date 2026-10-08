# M4 Milestone Audit — Analytical Intelligence (S14 to S16)

> **Records cited.** This is a process audit (PEF §4). The session reports and prompts it cites are kept in the
> private development archive, not in this repository (D-151); the decisions, documents and files it cites are here.

**Status:** ACCEPTED by the human on 2026-10-07 (S16.5). Written in S16.5 under D-140; M4 closes with this audit
(D-140).
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4; `SESSION-ROADMAP.md` M4.
**Written by:** Claude, as the Knowledge Architect, with the Portfolio Reviewer's process judgement (S16.5
Part B §10).
**Base read:** `claude/new-session-u2e1xq` @ `a203265`. The milestone's work reached `main` in PR #24 (S14,
`2a6e91c`), #26 (S14.5, `2c14e90`) and #27 (S15, `1ca2e89`). S16 is in PR #28, open at writing.
**What this audit is:** an `INTERPRETATION` of the project's own record. Each answer cites a report, a decision
or a file. Answers that repeat a session report are summarised and linked, never copied.

## Part 1 — The eight questions (PEF §4)

### 1. What was intended

The roadmap's M4:

- **S14:** "a reproducible analytical warehouse without making the warehouse the canonical source of
  truth". Gate: "All published metrics can be regenerated from versioned inputs".
- **S15:** "transparent descriptive metrics for supplier and geographic concentration":
  - the five metrics: supplier counts, geographic concentration, single-source relationships, evidence
    coverage and source age;
  - non-goal: no "opaque composite 'dependency score'".
- **S16:** "Challenge whether the metrics answer real questions and whether their denominators,
  populations and assumptions are defensible"; the human to "approve, modify or retire each metric".

### 2. What was implemented

| Session | Delivered | Record |
|---|---|---|
| S14 | DT-1 first (28 identity-basis rows); `tools/warehouse.py` rebuilding an in-memory DuckDB from `data/` on every run; results committed with their input digests; the first query (the table of links) on the HBM page with its "How this was computed" | `sql-layer.md`; D-117 to D-121 |
| S14.5 (inserted by the human) | a visual benchmark (five organisations, 29 patterns); the seven-layer research-experience architecture; the SQL-to-visual binding rule; the research view prototype `site/hbm-insight/index.html` | `visual-architecture.md`, `visual-benchmark.md`; D-122 to D-126 |
| S15 | evidence coverage and source age, computed in SQL; the three supplier metrics shown as "cannot be computed yet"; queries built on queries; the merged break harness | `metrics.md`; D-127 to D-132 |
| S16 | the analytical audit; coverage and source age modified, the publishers tally retired, the supplier metrics kept; the reference date's owner | `analytical-audit.md`; D-133 to D-140 |

**Against the gates:**

- **S14's gate is met:** every result is regenerated from versioned inputs, `--check` runs in the suite
  (WH-2), and CI installs the pinned engine.
- **S15's mission is met in part.** Of the two concentration metrics it names, neither can be computed:
  no supplier is recorded. They are shown as gaps, not hidden (D-130).
- **S16's gate is met.** Every metric was ruled on; the cold reading was taken by two fresh agents after
  the human waived theirs (S16, Deviation 1).

### 3. What changed, and why

- **A session was inserted** (S14.5, by the human) to design the visual and research experience before the
  metrics, so the metrics would land in a designed place. Sub-session numbering entered the validator
  (D-126).
- **The page stopped being the only consumer of the records.** Results became a derived layer
  (`sql/results/`), and the research view became a second page whose input is the HBM page (D-125).
- **Queries began to build on queries** (D-131). A change to the first query now reaches every metric and
  both pages.
- **Two of the five metrics turned out uncomputable,** and the design made them visible gaps (D-130).
- **S16 retired one count and corrected two metrics' wording** after unprimed readers misread them
  (D-133 to D-135).
- **The research gap became the next session's work** (D-139), at the human's direction.

### 4. Which assumptions failed

| Assumption | What happened | Record |
|---|---|---|
| "DT-1 makes the session large" | it was 25 table rows and two column removals | S14 |
| An evidence date is a date of the evidence | for 14 undated sources, it is the day a page was read; Trainium2's "recent" link rests on one | S14, S15 (date basis), S16 (C-4, probe P3) |
| "Every row has one publisher" | the inferred rows rest on two publishers, for two steps of one reasoning | S14.5; D-127 |
| "8 links" means 8 records | 8 rows from 5 records | S14.5; D-128 |
| The supplier population is the parts on the page | it is the parts per accelerator: 2, not 1 | S15 |
| Source age's horizon is the source policy's horizon | it is, but the policy applies it only to time-sensitive links | S16, C-4; D-134 |
| A metric's plain definition reproduces it | the H100's coverage could not be reproduced from it | S16, C-3; D-133 |
| The publishers count is a tally of drawn rows | its range was a per-row count the page computed | S16, C-7; D-135 |

### 5. Which shortcuts were taken

- **The research view stayed a prototype:** one slice, two accelerators, not published (NG-13).
- **The human's reading of the SQL came after the page,** as questions with candidate answers, at the
  human's request (S14, Deviation 4).
- **S14.5 ran without a Part B** (S14.5, Deviation 1).
- **Breaks were re-run selectively** after wording changes, with a reasoned argument that stricter checks
  cannot uncatch a fault (S15). S16 ran the merged harness in full.
- **The human's cold reading was waived** in S16. Two agents read instead, so a person's misreading
  remains untested for the S16 wording.

### 6. What technical and research debt was created

| Debt | Owner | Record |
|---|---|---|
| A supplier metric's presentation once a supplier is named (both builds stop) | S16.5 (D-139) | D-130, D-136 |
| "Gap" mixes not researched with refused as stale (C-2); the H100's age tally includes its recorded gap (C-5) | S20 | D-138 |
| One source with two access dates (C-8); a resolved recorded gap stops both builds (E-1); an unnamed crash on an invalid value (E-2); `build_page.sql_section`'s fixed path | S22 | D-138; S15 |
| The two accelerators' links are not the same kinds (C-9) | the session that next adds accelerator links | D-138 |
| The research view's filter needs `:has()` | S20 | S14.5 |
| An Atlas-wide ageing report (DT-S13-4 beyond the page's chain) | Change Detector (inactive) | D-129 |
| ID stability (DT-3) now also blocks publishing the question pages | as before | S14.5 |

### 7. What was removed or rejected

- **Engine and storage options:**
  - a committed database file;
  - SQLite;
  - DuckDB's JSON reader;
  - CSV results;
  - DuckDB in the page build (D-118).
- **Presentation options:**
  - a charting library;
  - JavaScript;
  - hover tooltips;
  - percentages;
  - any score or traffic light;
  - dark mode (D-123).
- **Metric designs:**
  - whole-Atlas coverage;
  - today's date for ages;
  - counting part classes;
  - showing "0 named suppliers" (`metrics.md` §9).
- **Retired in S16:** the publishers tally (D-135).
- **Rejected in S16:** merging the three supplier blocks (D-136).

### 8. What should be carried into the next phase

**The metric rules** (S16 report, "Implications"):

- a question, population and denominator before any number;
- a population line a stranger can reproduce from;
- an unknown is a gap, never a zero;
- a cited rule is applied with its scope;
- a page copies cells or tallies drawn rows, saying when a record repeats;
- a reference date moved by each session that rebuilds the pages.

**The presentation risks:**

- a line naming records and rows at once;
- one word for two states;
- a threshold shown for items it does not govern;
- a range of a per-row count;
- a large tally whose meaning sits in small type.

**Into M5:**

- **The supplier research comes first** (D-139). S17's policy entities can attach to a named supplier
  only if the research names one.
- **The milestone audit should be planned:** M5's last session (S19) should carry its milestone audit in
  its prompt (M3-P1).

## Part 2 — Process findings (PEF §4, §12)

| ID | Finding | Evidence | Disposition |
|---|---|---|---|
| M4-P1 | **The decisive defects were found by readers, not checks.** S15's "2 of 2 parts" and S16's horizon question came from a person and an unprimed agent. Every check had passed | S15, the human's challenge; S16, reader 2 q2 | standing practice: a cold reading before findings, in every audit of something a reader sees |
| M4-P2 | **A rule was cited without its scope** for two sessions (the horizon, S15–S16) | D-129 vs `source-policy.md` §12 | resolved by D-134; the lesson is in S16's report |
| M4-P3 | **The milestone ended without its audit,** like M2 and M3 (M3-P1) | `audit-history.md` | resolved by D-140; carried into M5's planning |
| M4-P4 | **The merged break harness works as a regression gate:** 74 faults and 9 controls run in full on S16's tree | the full run's output (session record, D-151); the harness is `tests/regression/breaks.py` | kept; one harness, extended per session |

## Part 3 — Maturity (PEF §3), where M4 produced new evidence

| Dimension | Rating | Evidence |
|---|---|---|
| Analytical depth: process | **3, Controlled** | `analytical-audit.md` §9 |
| Analytical depth: outcome | **3, Controlled** after S16's remediation (2 at the audit) | `analytical-audit.md` §9; D-133 to D-135; WH-15, IN-12 |
| Reproducibility: outcome | **3, Controlled** | results rebuilt byte-identically from versioned inputs with their digests (WH-1, WH-2); `--check` in the suite and CI; the independent computations WH-10 to WH-14 |
| Code / engineering: outcome | **2, Defined** | tested and harnessed (361 tests; 83 breaks). But two plausible data changes stop the builds without a design (E-1), one crashes them without a named reason (E-2), and a fixed result path remains (S22 debt) |

## Part 4 — Findings and debt

This audit adds no blocking finding. M4's debt is listed in Part 1 §6 with its owners. M4-P3 is carried into
M5's planning.

**M4 is closed** with this audit (D-140).
