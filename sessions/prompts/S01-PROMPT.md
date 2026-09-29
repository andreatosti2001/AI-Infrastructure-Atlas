# AI-Infrastructure-Atlas — S01 Session Prompt

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

Domain map: physical AI stack

**Type:** Research

Study with Opus:
- AI accelerators;
- HBM;
- advanced packaging;
- foundries;
- EDA/equipment;
- cloud/data centres;
- energy interface.

Human task:
- read the generated domain map and challenge terminology.

**Weekly gate:** You can explain the physical AI compute stack without relying on the website.

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

> **Provenance and precedence (D-012).** Everything above this line is **Part A**, the
> human-authored S01 prompt, reproduced verbatim. Part B is Claude's elaboration of Part A
> into the 18 sections of `SESSION-PROMPT-SPEC.md` §2. It was drafted at the end of S00
> and aligned to Part A. Part B adds detail only. **If the two ever conflict, Part A
> governs**, and higher-level documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern
> both.

## 01 — Session identity

- **Session:** S01
- **Title:** Domain map: physical AI stack
- **Type:** RESEARCH
- **Milestone:** M0 — Project Constitution (`SESSION-ROADMAP.md` numbering)
- **Predecessor:** S00 — Repository bootstrap
- **Expected successor:** S02 — Architecture baseline + process benchmark
- **Complexity class:** large (research-heavy; no code)

## 02 — Mission

Produce a sourced, concept-level map of the seven Part A layers that AI compute depends
on, with explicit uncertainty markers and a source register. It should be clear enough
for the human to challenge its terminology and to explain the stack without the website
(Part A weekly gate), and precise enough for S02–S04 to decide what the data model must
represent.

## 03 — Why this session exists

The schema sessions (S03 entities, S04 relationships) must model a domain the project
understands. Without a sourced domain map, the schema would encode the model's memory of
the industry instead of evidence. S01 also answers the roadmap's audit question: *which
concepts are genuinely necessary for the initial product, and which belong to future
scope?* It is also a learning session for the human (Part A "Human task").

## 04 — Current state

Inherited from S00 (read `sessions/reports/SESSION-00-REPORT.md`, including its addendum):

- constitutional documents at the root; session system under `sessions/`;
- `tools/validate_repo.py` (Gate 0) and 10 unit tests, both run in CI;
- `docs/architecture/baseline.md` (DRAFT) and `decisions.md` (D-001–D-012);
- **no** data, schemas, source policy, agent contracts or research artifacts;
- open: U-2 (milestone label collision) — does not block S01.

Decisions that bind S01:

- **D-008:** the governing question is *"Where are the critical dependencies behind AI
  compute, and what evidence supports that assessment?"* Do not frame the map as EU vs
  non-EU. Record location/jurisdiction evidence where you find it.
- **D-005:** create only the directories this session needs.

## 05 — Inputs and evidence

Documents to read, in Part A's order of steps 1–4:

1. `CLAUDE.md` (all), especially §5–§6 and §16
2. `MASTER-ARCHITECTURE.md` §3.2, §5, §6, §10, §25
3. `SESSION-PROMPT-SPEC.md`; `PROJECT-EVALUATION-FRAMEWORK.md` §6
4. `sessions/reports/SESSION-00-REPORT.md`
5. also: `SESSION-ROADMAP.md` S01–S05; `docs/architecture/baseline.md`; `docs/architecture/decisions.md`

Repository paths to inspect (Part A step 5): the whole tree. It is small; confirm it
matches the S00 report.

Datasets: none exist.

External research required. Part A's evidence rules apply: retrieve and read each source,
and do not cite what you have not opened. Prefer, in order (MA §10; provisional until
S05's source policy):

1. official company documentation and regulatory/financial filings;
2. standards bodies and technical specifications;
3. government and intergovernmental reports;
4. peer-reviewed or reputable academic/technical research;
5. high-quality secondary analysis (attributed, never treated as primary);
6. news/media — only for recent events, always attributed.

Previous report: S00. Audit findings: none yet.

## 06 — Required reasoning

Before writing the map, do Part A steps 6–7: restate the mission, scope, non-goals and
acceptance criteria, and propose the smallest safe plan. Then answer:

1. What is the minimum set of concepts in each Part A layer that the first question needs?
   Justify each inclusion and exclusion.
2. For each layer, what is a *technology*, what is a *component/product*, what is a
   *process/capability*, and what is an *actor type*? Where do these blur?
3. Which dependencies between layers are **structural** (true of the technology itself)
   and which are **contingent** (true of a current market arrangement)? The two need
   different evidence.
4. What kind of evidence could establish each dependency, and where is it likely to be
   non-public (`not_publicly_determinable`)?
5. Which terms are used inconsistently across sources (e.g. "advanced packaging",
   "foundry", "AI accelerator", and Part A's combined "EDA/equipment")? Choose a working
   definition and record the alternatives.
6. Where does the energy interface begin and end for this project's scope?

## 07 — Tasks

**Research**

1. For each Part A layer — **AI accelerators; HBM; advanced packaging; foundries;
   EDA/equipment; cloud/data centres; energy interface** — identify core concepts, their
   definitions and their upstream and downstream dependencies **at the concept level**.
   "EDA/equipment" is one Part A layer covering two distinct inputs (design software and
   manufacturing tools). Map both, and record in the terminology section whether they
   should stay one layer.
2. Retrieve primary or authoritative sources for each definition and dependency.
   Register every source.

**Design**

3. Classify each concept as `v1-scope` or `future-scope`, with a one-line justification.
4. Write a short plain-language overview of the whole chain, citing the entries it relies
   on. This supports the human's weekly gate.
5. List terminology questions that need human judgement (Part A "Human task").

**Implementation** — none (no code, no data files).

**Validation**

6. Self-audit: sample at least 10 map entries. Re-open each cited source and check that
   the wording does not exceed the evidence. Record the results in the report.
7. Run `python -m unittest discover -s tests -v` and `python tools/validate_repo.py`.

**Documentation**

8. Write `docs/research/domain-map.md` and `docs/research/source-register.md`.
9. Update the `docs/README.md` research-outputs row to `draft`.
10. Append any decisions to `docs/architecture/decisions.md`.
11. Write `sessions/reports/SESSION-01-REPORT.md` (see §14).

## 08 — Explicit non-goals

Out of scope even if easy:

- canonical JSON records, schemas or controlled vocabularies (S03–S05);
- a company, product or facility dataset (S07–S09) — named companies may appear only as
  *attributed examples* supporting a concept, not as dataset entries;
- supply-chain edges between specific entities (S10). Part A: do not silently infer
  supply-chain relationships;
- EU vs non-EU classification or any sovereignty assessment (D-008);
- metrics, concentration figures, market shares or rankings;
- policy/export-control analysis (S17+);
- networking, and energy beyond its interface with data centres;
- UI, validators for research files, new dependencies (Part A engineering rules).

## 09 — Constraints

- **Evidence:** Part A evidence rules; CLAUDE.md §5–§6, §16. Model memory is not evidence.
  A plausible statement without a source is a gap, not a fact.
- **Claims:** tag every substantive statement as
  `FACT | ATTRIBUTION | DERIVATION | INTERPRETATION | IMPLICATION`. Part A lists four of
  these classes. `ATTRIBUTION` comes from CLAUDE.md §6, which takes precedence. It is
  needed for attributed examples and secondary analysis.
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
- **Conflicts:** when sources disagree, record both, attributed. Do not pick silently
  (Part A: preserve source conflicts explicitly).
- **One home:** the source register is a research-staging artifact. S06 migrates it into
  canonical source records and then freezes it. Record that in the register header.

## 12 — Implementation rules

- **Allowed files:** `docs/research/domain-map.md`, `docs/research/source-register.md`,
  `docs/README.md`, `docs/architecture/decisions.md` (append only),
  `sessions/reports/SESSION-01-REPORT.md`.
- **Prohibited:** any other file, new directories other than `docs/research/`, any
  dependency or tooling change.
- **Migration/rebuild:** none.
- **Commit:** only verified work (Part A), after §13 passes.

## 13 — Verification plan

- `python -m unittest discover -s tests -v` → all pass.
- `python tools/validate_repo.py` → `Repository integrity: OK`.
- Manual evidence check (recorded in the report):
  - every map entry has a claim class and a source ID or explicit status marker;
  - every cited source ID exists in the register, and every register row has `url` and
    `accessed_at`;
  - self-audit of ≥10 sampled entries (§07 task 6), with results.
- Not applicable: schema, browser, accessibility, performance.

## 14 — Evaluation requirements

The report must carry the `SESSION-PROMPT-SPEC.md` §5 headings (enforced by
`tools/validate_repo.py`) and must also cover every item in Part A's "Required
end-of-session report":

| Part A item | Report location |
|---|---|
| files/components changed | `## Files changed` |
| data/evidence changes | `## Data changed`, `## Evidence added/retired` |
| commands/tests and results | `## Tests run` |
| decisions and rejected alternatives | `## Decisions made` (with a rejected-alternatives subsection) |
| deviations from this prompt | `## Deviations` |
| unresolved debt and evidence gaps | `## Debt introduced/resolved`, `## Unresolved issues` |
| human approvals required | `## Unresolved issues` → human approvals subsection |
| one concrete next-session handoff | `## Implications for the next session` |

The report must also record: assumptions invalidated; layers or concepts considered and
excluded; open terminology questions.

## 15 — Acceptance criteria

1. `docs/research/domain-map.md` covers all seven Part A layers.
2. Every concept entry has: definition, layer, claim class, ≥1 source ID with locator
   **or** an explicit status marker, and `v1-scope`/`future-scope` with justification.
3. Every source ID cited in the map resolves to a row in `docs/research/source-register.md`.
4. Every register row has `publisher`, `title`, `url`, `accessed_at` and a provisional tier.
5. No register row is a search-results page or snippet.
6. The map contains a plain-language chain overview and a terminology section listing
   the open questions for the human (Part A "Human task").
7. No specific entity-to-entity supply relationship is stated as `FACT` without a
   primary/authoritative source.
8. Unit tests and `tools/validate_repo.py` pass.
9. `sessions/reports/SESSION-01-REPORT.md` exists and satisfies §14.

The Part A **weekly gate** is a human judgement made after the session. Opus supports it
through criterion 6 but cannot declare it passed.

## 16 — Stop conditions

Stop and report instead of improvising (Part A autonomy boundary) when:

- a layer cannot be defined from retrievable authoritative sources;
- sources materially conflict on a definition that affects the v1 scope;
- the map would need to include entity-level data to be meaningful (this signals a scope
  problem for S03/S07);
- network restrictions prevent retrieving the sources needed (report which ones);
- any stop condition in `SESSION-PROMPT-SPEC.md` §2.16 or CLAUDE.md §18 applies.

## 17 — Deliverables

- `docs/research/domain-map.md` (including the chain overview and terminology section)
- `docs/research/source-register.md`
- updated `docs/README.md` (research-outputs row)
- appended decisions (if any) in `docs/architecture/decisions.md`
- `sessions/reports/SESSION-01-REPORT.md`

## 18 — Handoff

S02 should receive:

- **completed work:** the domain map and source register;
- **open issues:** terminology questions (and the human's challenges to them);
  `not_researched` gaps; source conflicts; U-2;
- **audit findings:** the self-audit results;
- **recommended next decision:** which concepts are frozen as v1 scope for S03/S04;
- **files to read first:** `sessions/reports/SESSION-01-REPORT.md`,
  `docs/research/domain-map.md`, `docs/architecture/baseline.md`.
