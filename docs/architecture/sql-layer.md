# The SQL layer

**Status:** ACCEPTED by the human on 2026-10-03 at the S14 review (D-117 to D-121). §7's publisher sentence corrected on 2026-10-06, as the human confirmed at the S15 opening (D-127). The human decided on 2026-10-03 at the S14
opening: DuckDB runs the queries, and the page reads saved results (H-2); the first result appears
as a section of the HBM page (H-3); the per-record document tables moved into `data/` first (H-1,
D-117).
**Required by:** `SESSION-ROADMAP.md` S14 ("Introduce a reproducible analytical warehouse without
making the warehouse the canonical source of truth"; gate: "All published metrics can be
regenerated from versioned inputs"); `MASTER-ARCHITECTURE.md` §16, §17; `CLAUDE.md` §7, §11, §12;
D-110, D-115, D-116.
**Roles:** Knowledge Architect (the boundary between canonical and derived), Data Auditor (the
loader and its checks), Analyst (the queries and their results), Editorial (the page section and
the tutorial text).

## In short

The Atlas's facts live in the JSON files under `data/`, and only there. The SQL layer is a
calculator built on top of them. Every run loads the files into a fresh DuckDB database held in
memory, runs the queries in `sql/`, and writes each result to `sql/results/` with a fingerprint
(SHA-256 digest) of the files it read. Nothing is ever written back into `data/`, and the database
itself is thrown away when the run ends. Anyone can delete every result and get the same bytes back
with one command:

```bash
python tools/warehouse.py            # rebuild the database in memory, run every query, write the results
python tools/warehouse.py --check    # the same, in memory only; exit 1 if a committed result differs
python tools/warehouse.py --db /tmp/atlas.duckdb   # also keep a database file to explore (never inside the repository)
```

The first question it answers: **for each AI accelerator on the HBM page, which links does the
Atlas record around it, on what basis (stated, inferred, or a gap), and how old is the evidence?**
The answer is a table on the HBM page. Beside the table, a "How this was computed" control opens a
tutorial generated from the query file itself.

## 1. Canonical vs derived (Part B §06 q1)

| | What | Where | Who writes it |
|---|---|---|---|
| Canonical | source, claim, entity, event, relationship, refused-candidate and identity-basis records | `data/*.json` | the reviewed workflow (human approval) |
| Loaded, not stored | the same records as relational tables (§8) | a DuckDB database in memory | `tools/warehouse.py`, on every run |
| Derived, committed | each query's result, with its inputs' digest | `sql/results/<query>.json` | `tools/warehouse.py`, never by hand |
| Rendered | the page section and its tutorial | `site/hbm-chain/index.html` | `tools/build_page.py` |

- **Only canonical files are loaded.** `data/staging/` is never read, so an unreviewed record cannot
  reach a result.
- **The database is never committed or edited.** It is a cache of the JSON files, in a binary
  format tied to one DuckDB version, and it cannot be reviewed in a diff. The runner refuses to
  write a database file inside the repository (`--db` must point elsewhere), so no stray copy can
  be committed by accident.
- **Results are committed** because the page build reads them without running DuckDB (H-2). A
  result is a rendering of canonical data, like the page: it is never edited, and a check fails
  when it differs from a fresh run.
- **Nothing flows back.** No tool writes from SQL into `data/`. A value found by a query is a
  `DERIVATION` until a reviewed claim records it (`CLAUDE.md` §7).

## 2. Rebuild (q2)

- **One command** (`python tools/warehouse.py`) loads every canonical file and writes every
  result. There is no state between runs.
- **Same inputs, same bytes.** Every query ends in an explicit `ORDER BY` over a unique key. Every
  list built in SQL is ordered inside the aggregate (`list(x ORDER BY x)`). DuckDB runs with one
  thread, and nothing reads the clock or a random value. The writer emits JSON with a fixed key
  order, two-space indent and a final newline.
- **How it is checked.** `tests/test_warehouse.py` (WH-1) builds the database twice and requires
  byte-identical results; WH-2 requires each committed result to equal a fresh run. Both run in CI,
  which installs the pinned DuckDB (`requirements-analysis.txt`, D-118).
- **Each result records its inputs**: the path and SHA-256 of every file loaded, the loader, and
  the query file, with one digest over them all, plus the engine version. A result therefore shows
  what it was computed from, and any change to an input makes WH-2 fail until the results are
  rebuilt.

## 3. Explicit states in SQL (q3)

The records never use JSON `null`. An unknown is an object such as `{"state": "not_researched"}`,
and the state words mean different things (`MASTER-ARCHITECTURE.md` §5.7). The loader keeps them
apart (D-119):

- **A field that holds a value or a state becomes two columns**: `<field>_value` and
  `<field>_state`. The state column holds `value` when a value is present; otherwise it holds the
  record's own state word, unchanged (`not_researched`, `not_publicly_determinable`,
  `not_applicable`, `not_stated`, `undated`, `no_record`, …); otherwise `absent`, when the record
  has no such key (a `DERIVATION` claim has no `as_of`, by its schema).
- **SQL NULL appears only in a `_value` column, and only when its `_state` column says why.** WH-4
  checks this for every table, so NULL never stands for an unknown by itself, and no unknown is
  ever loaded as zero or as an empty string.
- **A list field becomes rows** (one per item, with its position), and an empty list gives no rows.
  An attribute held as assertions (`[{"value", "claim_ids"}]`) becomes one row per assertion in
  `field_values`, with its claims in `field_value_claims`. An attribute held as a state becomes one
  `field_values` row whose `state` is that word. This is the flattening DT-4 asked for.
- **Query results keep states as words.** A result cell is never NULL (WH-4). Where a row has no
  evidence to date, the date cells say `not_applicable`. Where a link is unknown, the `gap_reason`
  cell says why, in the record's own word. A planted `not_publicly_determinable` must reach the
  output as itself, distinct from `not_researched` (WH-5).
- **The loader drops nothing silently.** It knows every key of every record kind, and it fails on a
  key it does not know (WH-3), so a new field cannot be lost between JSON and SQL.

## 4. Lineage (q4)

Every result row carries the IDs that take a reader back to the records:

- `record_id`: the edge (`rel-…`) or refused candidate (`cand-…`) the row shows;
- `reached_through`: the edge from the accelerator through which the row is reached, or `direct`;
- `claim_ids`: the claims the row's record cites (for a refused candidate: the claims it
  considered);
- `source_ids`: every source those claims rest on, following input claims down to their
  citations;
- `accelerator_class_claim`: the claim that makes the product count as an accelerator (an
  `instance_of_basis` row, D-117).

WH-6 resolves every ID in every row to a canonical record. It also recomputes each row's sources
from the JSON with the standard library, without SQL, and requires the same list. `python
tools/trace.py <claim>` prints any row's evidence in full.

## 5. The page and the build (q5)

- **The page build stays standard library** (H-2, D-003). It reads `sql/results/*.json` and the
  query file `sql/*.sql`, both added to its inputs. It never imports DuckDB.
- **PG-7 still holds.** The page rebuilds byte-identically from its inputs on a machine without
  DuckDB. If an input of a result changes, WH-2 fails until `tools/warehouse.py` is run; PG-7
  fails until `tools/build_page.py` is run. The order is: data, then results, then the page.
- **PG-11** (new, `tests/test_page.py`): every cell of the table equals its cell in the committed
  result; every result row is shown; the tutorial matches the query file.

## 6. The SQL tutorial (q6, D-115)

- **Where its text lives:** in the query file, as SQL comments. `sql/accelerator_dependencies.sql`
  opens with `-- question:` and `-- reading:` paragraphs. Then each part of the query is preceded
  by `-- step:` (a short title) and the plain-language lines that explain it.
- **How it is generated:** the page build splits the file at its `-- step:` lines and shows, for
  each part, its explanation and then its SQL, exactly as the file has them. Because both the
  query that DuckDB runs and the tutorial come from that one file, the tutorial cannot show a
  different query. PG-11 rejoins the parts the page shows and requires them to equal the file.
  WH-2 requires the result's recorded query digest to equal the file's.
- **What a reader sees:** under the table, a closed disclosure, "How this was computed". Open, it
  shows the question in plain words, then each step's explanation followed by its SQL, then how to
  read a row. It works by keyboard (a native `<details>` element), and at phone width the code
  wraps instead of widening the page.

## 7. The first question, and the weaknesses it must show (q7)

**Question:** for each accelerator on the page, which links does the Atlas record, with what basis,
and what evidence date? (S13's recommended first question.)

**Definitions** (D-120), each written in the query's comments:

- **An accelerator** is a product recorded as an instance of the AI accelerator class, or of a
  class recorded as a kind of it (`broader`). Today: the NVIDIA H100 (a data-centre GPU) and AWS
  Trainium2 (an AI ASIC).
- **A link** is either:
  - an edge into or out of the accelerator;
  - an edge reached from what the accelerator incorporates, walking `incorporates` and `requires`
    outward;
  - an unknown on one of those edges (an assertion field held as a state, for example the HBM
    supplier: `not_researched`);
  - a recorded gap: a refused candidate about the accelerator whose only reason is
    `evidence_not_fresh`, meaning a claim the Atlas holds states the relation but is too old to
    use (F-1). Candidates refused for any other reason are not links: no evidence states them.
- **Basis:** `stated` if at least one claim the edge cites is a `FACT`, `inferred` if none is
  (D-103), and `gap` for an unknown or a recorded gap.
- **Evidence date** follows F-1 (`company-dataset.md` §9). For each citation it is the claim's
  `as_of` if that is a date; otherwise the latest date the source states for itself; otherwise
  the source's access date. A row shows the earliest and latest evidence date across the
  citations it rests on. A partial date (`2021-02`) is shown as recorded and sorts at the start
  of its period.

**The S13 weaknesses, row by row** (content-audit Part 5, DT-S13-1 to DT-S13-7):

| Weakness | How the result shows it |
|---|---|
| No value is corroborated by a second publisher | `publishers` lists the distinct publishers behind each row. Every stated row and every recorded gap today has one; each inferred row has two, behind different steps of one reasoning, which do not confirm one another. The table never says "confirmed" or "corroborated" |
| "HBM requires 3D die stacking" restates a definition (D-091, DT-S13-7) | `rests_on_atlas_interpretation` is true when any claim in the row's chain of reasoning is the Atlas's own `INTERPRETATION` (here the working definitions). The page marks it |
| "Party" standing unchecked on 14 citations (DT-S13-1) | `party_standing_unchecked` lists the sources cited with `party` standing whose publisher is not linked to a company record |
| Evidence ages in place (DT-S13-4) | each row shows its evidence dates. The result does **not** compute an age or call any value current: an age needs today's date, which would make the result change with the calendar. The page says so |
| H100 figures "preliminary" (DT-S13-2) | no query reads or computes over a capacity figure. The H100 row rests on the claim that the H100 contains HBM, not on the figures |
| SK hynix operates M16 rests on continuity (D-099) | not on the chain, so not a row. Its evidence date is shown in the page's lane, as before |

## 8. Tables loaded (reference)

All from canonical files. The loader is `tools/warehouse.py`; this list is its contract (WH-3).

| Table | One row per | From |
|---|---|---|
| `sources` | source | `sources.json` |
| `source_dates` | date a source states for itself | `sources.json` `stated_dates` |
| `claims` | claim | `claims.json` |
| `citations` | citation of a claim | `claims.json` `citations` |
| `citation_criteria` | one §7.1 criterion of a third-party citation: `recognised` or `independent`, met or not, and why (S16.6, D-147) | `claims.json` `citations` `third_party_criteria` |
| `claim_inputs` | input claim of a claim | `claims.json` `input_claim_ids` |
| `entities` | company, jurisdiction, technology, component, product or facility | the six entity files |
| `entity_lists` | item of a list field (`aliases`, `identity_claim_ids`, `concept_refs`, `broader`, `instance_of`, `facility_kinds`) | the six entity files |
| `entity_scalars` | single-word field (`vendor`, `product_kind`, `use_class`, `technology_kind`, `jurisdiction_kind`) | the six entity files |
| `field_values` | assertion or state of an attribute (entities) or of an edge's `supplier` | entity files, `relationships.json` |
| `field_value_claims` | claim of an assertion | the same |
| `relationships` | edge | `relationships.json` |
| `relationship_claims` | claim of an edge | `relationships.json` |
| `events`, `event_claims` | event; claim of an event | `events.json` |
| `refused_candidates` | refused candidate | `refused_candidates.json` |
| `candidate_endpoints` | endpoint of a candidate (an ID, or a name with no record) | `refused_candidates.json` |
| `candidate_relation_types`, `candidate_reasons` | type; reason | `refused_candidates.json` |
| `candidate_considered` | claim or sentence a candidate considered | `refused_candidates.json` |
| `identity_basis` | identity-basis row (D-117) | `identity_basis.json` |
| `load_manifest` | file loaded, with its SHA-256 | the run itself |

A few nested values are kept whole as JSON text, because no query needs their parts yet: a
citation's `originator` (one citation), a source's `filing_copy`, and a source's `authors` when
they are a list. Each is listed in the loader, so none is dropped silently.

## 9. What S15 receives

- **Tables a metric may use:** all of §8, through views that S15 defines in `sql/`, never by
  editing `data/`.
- **Populations it could count, and their honest denominators:** the 5 edges; the 120 canonical
  claims; the 99 citations on 85 cited claims; the 2 accelerators. Each is a census of what the
  Atlas holds, not of the world. A share over them describes the Atlas's coverage, never the
  industry.
- **Weaknesses every metric must carry:** the five rows of §7, plus `not_researched` as its own
  category (never zero, never "no").

## 10. Rejected alternatives

- **A committed database file**, or DuckDB as the store: a second home for every fact, binary,
  and unreviewable in a diff.
- **DuckDB reading the JSON itself (`read_json`)**: shorter, but it infers column types from the
  data and turns state objects into structs. The state columns would depend on DuckDB's inference,
  not on a rule this repository states.
- **Loading staging records** with a layer column: a query could then show an unreviewed record.
  S15 can add staging views if it ever needs them.
- **Tutorial text in a separate file** (Markdown or JSON beside the query): it could drift from the
  query it explains. Comments in the query file cannot.
- **An "age in days" column**: it needs today's date, so the result would change on every run.
- **CSV results**: they lose lists and types. JSON keeps each row's ID lists as lists.

## 11. Debt this design closes or moves

| ID | Disposition |
|---|---|
| DT-1 | done first in S14 (D-117) |
| DT-4 | done: flattening rules in §3 and the tables in §8; "the actors on the chain" is now a query |
| DT-7 | not triggered: the first query uses the `designs` edge and never a product's `vendor`, and never a `supplier` beside a `supplies` edge. Owner: the first S15 metric that combines them, which must keep them as separate columns |
| DT-3 | re-owned: results are derived and rebuilt from current IDs, so a renamed ID leaves no stale copy inside the repository. The cross-commit ID check is due before the first export that leaves the repository (client output, M6). Owner: Data Auditor |
| DT-9 | partly closed: the four per-record tables no longer exist, so the checks that parsed them read data (D-117). The rule-table readers remain by design (D-110) |
