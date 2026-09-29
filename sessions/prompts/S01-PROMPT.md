# AI-Infrastructure-Atlas — S01 Session Prompt

> **DRAFT — pending human review (D-011).** Drafted by Claude at the end of S00. The human
> may edit it freely until S01 starts; from then on it is immutable
> (`SESSION-PROMPT-SPEC.md` §6). Delete this notice when approving.

## 01 — Session identity

- **Session:** S01
- **Title:** Domain map: the physical AI stack
- **Type:** RESEARCH
- **Milestone:** M0 — Project Constitution (`SESSION-ROADMAP.md` numbering)
- **Predecessor:** S00 — Repository bootstrap
- **Expected successor:** S02 — Architecture baseline + process benchmark
- **Complexity class:** large (research-heavy; no code)

## 02 — Mission

Produce a sourced, concept-level map of the physical and industrial layers that AI compute
depends on, with explicit uncertainty markers and a source register, so that S02–S04 can
decide what the data model must represent.

## 03 — Why this session exists

The schema sessions (S03 entities, S04 relationships) must model a domain the project
understands. Without a sourced domain map, the schema would encode the model's memory of
the industry instead of evidence. S01 also answers the roadmap's audit question: *which
concepts are genuinely necessary for the initial product, and which belong to future scope?*

## 04 — Current state

Inherited from S00 (read `sessions/reports/SESSION-00-REPORT.md`):

- constitutional documents at the root; session system under `sessions/`;
- `tools/validate_repo.py` (Gate 0) and 10 unit tests, both run in CI;
- `docs/architecture/baseline.md` (DRAFT) and `decisions.md` (D-001–D-011);
- **no** data, schemas, source policy, agent contracts or research artifacts;
- open: U-2 (milestone label collision) — does not block S01.

Decisions that bind S01:

- **D-008:** the governing question is *"Where are the critical dependencies behind AI
  compute, and what evidence supports that assessment?"* Do not frame the map as EU vs
  non-EU. Record location/jurisdiction evidence where you find it.
- **D-005:** create only the directories this session needs.

## 05 — Inputs and evidence

Documents to read, in order:

1. `CLAUDE.md` (all), especially §5–§6 and §16
2. `MASTER-ARCHITECTURE.md` §3.2, §5, §6, §10, §25
3. `SESSION-PROMPT-SPEC.md`, `PROJECT-EVALUATION-FRAMEWORK.md` §6
4. `SESSION-ROADMAP.md` S01–S05
5. `sessions/reports/SESSION-00-REPORT.md`
6. `docs/architecture/baseline.md`, `docs/architecture/decisions.md`

Repository paths to inspect: the whole tree. It is small; confirm it matches the S00 report.

Datasets: none exist.

External research required — retrieve and read each source; do not cite what you have not
opened. Prefer, in order (MA §10; provisional until S05's source policy):

1. official company documentation and regulatory/financial filings;
2. standards bodies and technical specifications;
3. government and intergovernmental reports;
4. peer-reviewed or reputable academic/technical research;
5. high-quality secondary analysis (attributed, never treated as primary);
6. news/media — only for recent events, always attributed.

Previous report: S00. Audit findings: none yet.

## 06 — Required reasoning

Answer these in the session before writing the map:

1. What is the minimum set of layers between "AI compute" and its physical inputs that the
   first question needs? Justify each inclusion and exclusion.
2. For each layer, what is a *technology*, what is a *component/product*, what is a
   *process/capability*, and what is an *actor type*? Where do these blur?
3. Which dependencies between layers are **structural** (true of the technology itself)
   and which are **contingent** (true of a current market arrangement)? The two need
   different evidence.
4. What kind of evidence could establish each dependency, and where is it likely to be
   non-public (`not_publicly_determinable`)?
5. Which terms are used inconsistently across sources (e.g. "advanced packaging",
   "foundry", "AI accelerator")? Choose a working definition and record the alternatives.
6. Where does the energy interface begin and end for this project's scope?

## 07 — Tasks

**Research**

1. For each layer below, identify core concepts, their definitions and their upstream and
   downstream dependencies **at the concept level**: accelerators; HBM/memory; advanced
   packaging; foundries/wafer fabrication; semiconductor equipment and EDA; cloud/data
   centres; energy interface.
2. Retrieve primary or authoritative sources for each definition and dependency.
   Register every source.

**Design**

3. Classify each concept as `v1-scope` or `future-scope`, with a one-line justification.
4. List terminology questions that need human judgement.

**Implementation** — none (no code, no data files).

**Validation**

5. Self-audit: sample at least 10 map entries. Re-open each cited source and check that
   the wording does not exceed the evidence. Record the results in the report.
6. Run `python -m unittest discover -s tests -v` and `python tools/validate_repo.py`.

**Documentation**

7. Write `docs/research/domain-map.md` and `docs/research/source-register.md`.
8. Update the `docs/README.md` research-outputs row to `draft`.
9. Append any decisions to `docs/architecture/decisions.md`.
10. Write `sessions/reports/SESSION-01-REPORT.md`.

## 08 — Explicit non-goals

Out of scope even if easy:

- canonical JSON records, schemas or controlled vocabularies (S03–S05);
- a company, product or facility dataset (S07–S09) — named companies may appear only as
  *attributed examples* supporting a concept, not as dataset entries;
- supply-chain edges between specific entities (S10);
- EU vs non-EU classification or any sovereignty assessment (D-008);
- metrics, concentration figures, market shares or rankings;
- policy/export-control analysis (S17+);
- networking, and energy beyond its interface with data centres;
- UI, validators for research files, new dependencies.

## 09 — Constraints

- **Evidence:** CLAUDE.md §5–§6, §16. Search snippets are not evidence. Model memory is
  not evidence. A plausible statement without a source is a gap, not a fact.
- **Claims:** tag every substantive statement as
  `FACT | ATTRIBUTION | DERIVATION | INTERPRETATION | IMPLICATION`.
- **Temporal:** figures and market arrangements go stale. Record the source's
  publication date, and describe current arrangements as time-bound ("as of …").
- **Architecture:** Markdown only. No change to `tools/`, `tests/`, CI or the root
  constitutional documents.
- **Portfolio:** capability signal = domain research + evidence methodology.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Source Scout | `docs/research/source-register.md` | candidate sources; may not mark claims verified |
| Extractor | `docs/research/domain-map.md` | concept entries with source IDs |
| Verifier | `docs/research/domain-map.md` (status fields only), S01 report | may downgrade or remove; may not invent evidence |
| Knowledge Architect | `docs/research/domain-map.md` (terminology section), `docs/architecture/decisions.md` (append) | concept boundaries and definitions |

All other agents are inactive. No agent may write outside `docs/research/`,
`docs/README.md`, `docs/architecture/decisions.md` or `sessions/reports/`.

## 11 — Data and evidence rules

- **Canonical entities:** none. S01 produces research artifacts, not canonical data.
- **Allowed relationship types:** concept-level only, in prose or tables, using MA §6.2
  verbs where they fit. Name any verb not in MA §6.2 and list it as input for S04.
- **Source tier:** provisional, using the §05 order. Record it per source.
- **Provenance:** every map entry cites ≥1 source ID with a usable locator (section, page,
  table), or carries `not_researched` or `not_publicly_determinable`.
- **Source register fields** (MA §5.3): `id`, `publisher`, `title`, `url`,
  `publication_date`, `source_type`, `source_tier` (provisional), `accessed_at`, plus
  `locators_used`.
- **Status markers** (MA §5.7): `verified`, `disputed`, `not_researched`,
  `not_publicly_determinable`, `not_applicable`. Unknown is never zero.
- **Conflicts:** when sources disagree, record both, attributed. Do not pick silently.
- **One home:** the source register is a research-staging artifact. S06 migrates it into
  canonical source records and then freezes it. Record that in the register header.

## 12 — Implementation rules

- **Allowed files:** `docs/research/domain-map.md`, `docs/research/source-register.md`,
  `docs/README.md`, `docs/architecture/decisions.md` (append only),
  `sessions/reports/SESSION-01-REPORT.md`.
- **Prohibited:** any other file, new directories other than `docs/research/`, any
  dependency or tooling change.
- **Migration/rebuild:** none.

## 13 — Verification plan

- `python -m unittest discover -s tests -v` → all pass.
- `python tools/validate_repo.py` → `Repository integrity: OK`.
- Manual evidence check (recorded in the report):
  - every map entry has a claim class and a source ID or explicit status marker;
  - every cited source ID exists in the register, and every register row has `url` and
    `accessed_at`;
  - self-audit of ≥10 sampled entries (see §07 task 5), with results.
- Not applicable: schema, browser, accessibility, performance.

## 14 — Evaluation requirements

The report must record: decisions made; deviations from this prompt; assumptions
invalidated; new debt; rejected alternatives (e.g. layers considered and excluded);
unresolved questions, especially terminology.

## 15 — Acceptance criteria

1. `docs/research/domain-map.md` covers all seven layers in §07 task 1.
2. Every concept entry has: definition, layer, claim class, ≥1 source ID with locator
   **or** an explicit status marker, and `v1-scope`/`future-scope` with justification.
3. Every source ID cited in the map resolves to a row in `docs/research/source-register.md`.
4. Every register row has `publisher`, `title`, `url`, `accessed_at` and a provisional tier.
5. No register row is a search-results page or snippet.
6. The map contains a terminology section listing the open questions for human review.
7. No specific entity-to-entity supply relationship is stated as `FACT` without a
   primary/authoritative source.
8. Unit tests and `tools/validate_repo.py` pass.
9. `sessions/reports/SESSION-01-REPORT.md` exists with all SESSION-PROMPT-SPEC §5 sections.

## 16 — Stop conditions

Stop and report instead of improvising when:

- a layer cannot be defined from retrievable authoritative sources;
- sources materially conflict on a definition that affects the v1 scope;
- the map would need to include entity-level data to be meaningful (this signals a scope
  problem for S03/S07);
- network restrictions prevent retrieving the sources needed (report which ones);
- any stop condition in `SESSION-PROMPT-SPEC.md` §2.16 or CLAUDE.md §18 applies.

## 17 — Deliverables

- `docs/research/domain-map.md`
- `docs/research/source-register.md`
- updated `docs/README.md` (research-outputs row)
- appended decisions (if any) in `docs/architecture/decisions.md`
- `sessions/reports/SESSION-01-REPORT.md`

## 18 — Handoff

S02 should receive:

- **completed work:** the domain map and source register;
- **open issues:** terminology questions; `not_researched` gaps; source conflicts; U-2;
- **audit findings:** the self-audit results;
- **recommended next decision:** which concepts are frozen as v1 scope for S03/S04;
- **files to read first:** `sessions/reports/SESSION-01-REPORT.md`,
  `docs/research/domain-map.md`, `docs/architecture/baseline.md`.
