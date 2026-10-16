# Final architecture record — v1.0

- **Status:** proposed (S25, 2026-10-16), for the human's acceptance with the release (S25 H-3). Written by the
  Knowledge Architect (D-229).
- **What it is:** the architecture of the Atlas as released, set beside what the [baseline](baseline.md) intended on
  2026-09-29 (PEF §4). It points to each part's home and restates none of them; the baseline keeps the current-state
  rows and the frozen non-goals, and the [decision log](decisions.md) keeps every rule's reason.
- **Base:** the release commit (the tag `v1.0`).

## 1. The system in one paragraph

Sources are retrieved and registered with the hash of their bytes. Claims quote them at a locator. Records of
companies, products, parts, places, facilities, export-control acts and events cite those claims, and typed
relationships link the records. Each claim is verified by a re-read and accepted by the human before it becomes
canonical. Python builds, using the standard library, derive statuses and paths. SQL queries over an in-memory DuckDB
compute the metrics. Generated, script-free HTML pages show answers with every value's evidence one step away. Tests,
deliberate faults and browser checks guard every layer, in CI on each push and again before publication.

```text
retrieve → register (sources.json, hash) → extract (staging) → verify (re-read) → human review → canonical (data/)
        → derive (tools/, sql/) → build pages (site/) → check (tests/, breaks, browser) → publish (tagged commit)
```

## 2. The layers, each with its home

| Layer | What it holds or does | Home | Rules | Checked by |
|---|---|---|---|---|
| Records | 13 kinds of record, one file each, staging beside canonical | `data/`, `data/staging/` | D-044, one home per fact | `tests/test_data_*.py` |
| Schemas and vocabularies | 7 JSON Schemas with every controlled value | `schemas/` | [entity](entity-taxonomy.md) and [relationship](relationship-taxonomy.md) taxonomies | `tests/test_*_schema.py` |
| Evidence model | claim types, evidence status, standing, citations with anchors, explicit unknowns | [`claim-model.md`](claim-model.md); [`source-policy.md`](../research/source-policy.md) | D-044 to D-053 | VD-1 to VD-13, F-1 (freshness) |
| Review | the human's verdict on every claim | [`human-reviews.md`](../quality/human-reviews.md) | D-151, D-182, D-183 | `tests/test_human_reviews.py` |
| Derivations | statuses, paths and ages computed when asked, never stored | `tools/policy_status.py`, `facility_status.py`, `navigate.py`, `evidence_age.py`, `trace.py` | D-156; MA §7 | `tests/test_policy_status.py`, `test_facility_status.py`, `test_navigate.py`, `test_freshness.py`, `test_trace.py` |
| SQL layer | DuckDB rebuilt in memory from `data/`; queries that are also tutorials; results with input digests | `sql/`, `tools/warehouse.py` | D-118, D-121, D-124 | WH checks (`tests/test_warehouse.py`); `warehouse.py --check` |
| Pages | 18 generated pages, no script, nothing loaded | `site/`; builds and templates in `tools/` | D-100 to D-107, D-190, D-200, D-203 | PG, IN, JR, BR checks; four `--check` builds; KL-1 to KL-8 |
| Later-rule search | a dated, logged search of the official record for texts that change the acts held | `tools/later_rule_search.py`; [`change-detection.md`](../research/change-detection.md) | D-208, D-211 | LS-1 to LS-11; JR-13 |
| Regression | deliberate faults that the suite must catch for their named reason; 28 run on every commit | [`tests/regression/`](../../tests/regression/README.md) | D-150, D-176 to D-178 | the harness itself |
| Browser checks | errors, overflow, keyboard path, contrast and print, locally, in CI and at the published address | [`tests/browser/`](../../tests/browser/README.md) | D-212, D-227 | the scripts' named failures |
| CI and publication | `validate` and `browser` on every push; publication of a tagged commit after every check | `.github/workflows/ci.yml`, `pages.yml`; `tools/check_all.py`, `check_published.py` | D-004, D-213, D-217, D-227 | EN-1 to EN-3; PA-1 to PA-3; PW-1 |
| Roles | twelve roles, eleven active, each a contract of reads and writes; every file owned | [`roles.md`](../agents/roles.md), [`contracts.md`](../agents/contracts.md) | D-010, D-052, D-180, D-184 | `tests/test_agent_contracts.py` |
| Development records | session prompts and reports, kept privately | the archive repository | D-151, D-152 | Gate 0 refuses them here |

## 3. What the baseline intended, and what v1.0 is

| Baseline (2026-09-29) | v1.0 |
|---|---|
| Pipeline: discovery → evidence → staging → verification → canonical → derivations → index/graph → presentation → QA → publish (MA §16) | built as intended. The "index/graph" step is derivation on demand (`navigate.py`, the recursive SQL), with no graph store (MA §18, NG-07). Publish runs from v1.0 (D-227) |
| Stack: JSON, Python, DuckDB with SQL, vanilla HTML/CSS/JS, GitHub Actions | as intended, without JavaScript: the pages hold no script (D-200). DuckDB is the only runtime dependency outside the standard library, and it is pinned (D-118) |
| Agents as contracts plus validators, no runtime (D-018, NG-08) | as intended. Eleven roles active by S24; no agent runtime (D-184) |
| Quality gates 0 to 8 (MA §14) | each automated or audited ([baseline §5](baseline.md#5-quality-gates)); Gate 8 by the Portfolio Reviewer's audit (D-224) |
| The first question, global wording first, EU lens later (D-008) | the global question is answered for one path. The EU lens is not built (NG-06) |
| The first vertical, accelerators to data centres (D-017) | one path of it: accelerators, their memory, its suppliers and the process it requires, plus the export-control acts that name those parts. The other layers have no supply-chain records (KL-01) |

**Not built, by decision:** a graph database, a server or a frontend framework (NG-07, D-200); an agent runtime
(NG-08, D-184); search across records (it needs a script, KL-12); measured quantities, shares and scores (NG-11,
KB-04, KB-05); legal determinations (NG-12, KB-01).

## 4. The decisions that most shaped v1.0

- **Evidence before structure.** One proposition per claim, quoted at a locator; records cite claims (D-044). Refused
  candidates are records, never edges (D-109).
- **One home per fact, derive the rest.** A policy's status comes from its dated events (D-156), and the source-age
  reference date moves with each rebuild (D-137).
- **Generated pages that prove their text.** Every text node on a page has a home in the records or is marked framing
  (D-105). The pages stay script-free so that the checks can read what a reader sees (D-200).
- **SQL as a tutorial.** Each query explains itself, and its result carries its inputs' digests (D-118, D-121, D-124).
- **Checks that can fail.** Breaks are planted faults the suite must catch for their named reason, selected by the
  files a change touches (D-150, D-176, D-177). The browser checks fail by name, in CI (D-212).
- **The human decides.** The human gives the verdict on every claim (D-182, D-183), takes every decision put as an
  option, merges every change and does every external action. The development records stay private (D-152).
- **Narrow first, then wider.** v1.0 finishes one path. v1.5 (visual intelligence) and v2 (coverage) follow, each
  opened by the human (D-201).

## 5. What any later change must keep

- A value is shown only if a canonical record holds it, and a gap is shown as a gap, never a zero.
- A claim becomes canonical only by the human's recorded verdict. A draft waits in `data/staging/`.
- A page is generated, never edited, and rebuilding it from the same inputs gives the same bytes.
- A new check is shown failing first and has a break. A check is never loosened.
- `python tools/check_all.py` passes on Python 3.11 before each commit. Publication happens from a tagged commit only.
- Every file has an owner role.

## 6. Architectural debt carried past v1.0

Each item has an owner in its audit. The debt open at the release is listed with its owner in the
[final process and outcome audit](final-audit.md#4-what-stays-open).
