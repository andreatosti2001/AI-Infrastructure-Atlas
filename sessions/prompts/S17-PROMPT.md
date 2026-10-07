# AI-Infrastructure-Atlas — S17 Session Prompt

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
Introduce a policy layer connecting infrastructure dependencies to public policy without duplicating
`EU-Digital-Policy`.

### Focus
- industrial policy;
- export controls;
- strategic dependencies;
- investment policy;
- technology restrictions;
- public support.

### Boundary
The project may reference EU regulatory instruments but must not become another EU digital-law database.

### Validation regime (decided by the human on 2026-10-07, D-150)
- The full merged break harness runs **only at a milestone audit**. The next one is M5's.
- Sessions in between run the breaks that touch the files they change, plus their own new breaks.
- Reminders, to be scheduled by the human at this session's opening:
  - turn the most useful breaks into permanent tests with planted data inside the suite, so they run in
    seconds on every commit and in CI;
  - select breaks by the files a session touches, instead of running all of them;
  - run breaks in parallel, each in its own copy.

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
> - Everything above this line is **Part A**. No upload was made. Claude assembled Part A on 2026-10-07:
>   - the operating contract and the report list are S16.6's Part A, word for word;
>   - the mission, focus and boundary are the S17 entry of `SESSION-ROADMAP.md`, word for word;
>   - the validation regime restates D-150, which the human decided on 2026-10-07 at the end of S16.6.
> - **Confirmation.** The human asked for this prompt on 2026-10-07. It is confirmed when the human starts
>   S17 with it, and the human may amend it before then.
> - Part B was written with the state measured at the end of S16.6, on `claude/new-session-u2e1xq`.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** `CLAUDE.md` and
>   `MASTER-ARCHITECTURE.md` govern both. The prompt becomes immutable once S17 begins (D-011).

## 01 — Session identity

- **Session:** S17 · **Title:** Policy entities
- **Type:** RESEARCH / ARCHITECTURE. Its dominant purpose is the design of the policy layer's records; the
  research supplies the first candidates.
- **Milestone:** M5, Policy / Geopolitical Layer (S17 to S19). M5's milestone audit is planned for S19
  (M4 audit, D-140).
- **Predecessor:** S16.6. **Successor:** S18, jurisdiction and policy relationships.
- **Complexity:** large. It opens a new layer: a record type, its vocabulary, its source-policy rows and its
  checks.

## 02 — Mission

Design the Atlas's first policy records, so that a small set of real policy instruments, each resting on
its own text, can be linked in S18 to the companies, parts and technologies the HBM chain already holds,
without duplicating `Eu-Digital-Policy`.

## 03 — Why this session exists

- **The roadmap:** M5 adds the policy and geopolitical layer, and S17 is its first session.
- **The data is ready to attach to:** S16.6 named both HBM suppliers (as reported) and added Samsung
  Electronics. The Atlas now holds nine companies a policy instrument could bear on: NVIDIA, Amazon, TSMC,
  SK hynix, Micron Technology, Samsung Electronics, ASML, Amkor Technology, Synopsys.
- **Reserved since S03 to S06, still undecided:**
  - the entity types `policy` and `institution` (D-022);
  - the relation types `restricted_by`, `regulated_by`, `supported_by`, `constrained_by` (D-030);
  - whether a normative text needs its own claim type or is an `ATTRIBUTION` to its issuing authority
    (`claim-model.md` §2 and its debt row).

## 04 — Current state

Measured at the end of S16.6.

- **Data:** 56 sources, 127 claims, 9 companies, 4 jurisdictions, 7 components, 9 technologies, 3 products,
  2 facilities, 4 events, 5 relationships, 12 refused candidates, 28 identity-basis rows; staging empty.
- **The two HBM suppliers** (D-148): SK hynix for the H100 (historical, to 2024-03, reported by TrendForce);
  Samsung Electronics for Trainium2 (reported by SemiAnalysis, recognition criterion unmet). The supplier
  metrics stay "cannot be computed yet".
- **Supplier-evidence rules** (D-144 to D-147): historical values; independent teardowns; sources
  registered when retrieved; third parties under the human's criteria (`source-policy.md` §7.1), shown as
  "reported".
- **No policy record exists.** The schema rejects `policy` and `institution` records.
- **Checks:** the suite, Gate 0 and the three `--check` commands pass. The merged harness has 100 breaks
  (`sessions/reports/SESSION-16.6-breaks/breaks.py`), all as named in S16.6's full run.
- **Debt carried** (S16.6 report): the ID rule's legal-form list lacks "Co., Ltd."; SemiAnalysis's
  recognition unmet; no current H100 supplier; paid H100 teardowns; Reuters, FT, WSJ and AP not
  searchable; `not_researched`'s definition against ER-3.
- **Next decision number:** D-151.

## 05 — Inputs and evidence

1. `sessions/reports/SESSION-16.6-REPORT.md`; `docs/research/hbm-supplier-research-S16.6.md`;
   `docs/research/supplier-evidence-rules-S16.6.md`.
2. `MASTER-ARCHITECTURE.md` §6.1 (the Atlas's entities, among them `PolicyInstrument`, `TradeMeasure`,
   `ExportControl`, `Investment`) and §7.1 (the governance layer's entities, for the boundary).
3. `docs/architecture/entity-taxonomy.md`, `relationship-taxonomy.md`, `claim-model.md`; the decisions that
   reserved the policy types (D-022, D-030).
4. `docs/research/source-policy.md`: the classes (`government_publication`, `policy_research_brief`), the
   standing rules, §7's matrix and how a new row is added.
5. `Eu-Digital-Policy` as a **methodological reference only**: read its patterns; never modify, copy or
   couple to it.

**External access: required** to retrieve the texts of the candidate instruments. Snippets locate
candidates only.

## 06 — Required reasoning

**Before designing:**

1. **What is a policy record?** One instrument (a law, regulation, rule, programme or measure), its issuing
   authority, its dates, its status, its scope. What is the record, and what is a claim about it?
2. **One home per fact.** Which fields are stated by the instrument's own text, and which are the Atlas's
   reading (`INTERPRETATION`)? Is status (in force, proposed, repealed) stored or derived from dated events?
3. **Normative text.** Is "the rule says X" an `ATTRIBUTION` to the authority, or a new claim type?
4. **Boundary with `Eu-Digital-Policy`.** Which EU instruments are in scope (only as they bear on the
   chain's industrial dependencies), and which belong to that product?
5. **Legal advice.** How does every record and page stay description, never advice (`CLAUDE.md` §13)?
6. **What S18 needs.** Which link types will connect a policy record to a company, part or technology, and
   what evidence each needs? S17 defines them; S18 records them.

**Before researching:** which instruments, chosen by the human (H-1), and which classes of source count for
each field.

## 07 — Tasks

**Opening**

1. Record the base, `git branch -a` and `git ls-remote`. Fresh virtualenv: the suite, Gate 0 and the three
   `--check` commands.
2. **H-0:** put to the human, in `CLAUDE.md` §9A form: which kind of instrument S17 models first, and when
   the three harness improvements in Part A are scheduled.

**Design**

3. Write the policy-layer proposal (`docs/architecture/policy-dataset.md`): the record, its fields, its
   vocabulary, its states, its source-policy rows, its checks, and the link types reserved for S18.
4. **H-1:** the proposal, item by item.
5. Implement only what is approved: schema, vocabulary, source-policy rows, validators, checks written first.

**Research**

6. Write a search plan for the chosen instruments, then search, retrieve, hash and log (Source Scout).
7. Draft the records with provenance (Extractor); re-read each anchor (Verifier). Sources are registered when
   retrieved (D-146); records wait in staging.
8. **H-2:** each record, recorded, refused or held.

**Validation and documentation**

9. The suite, Gate 0 and the `--check` commands in a fresh virtualenv. **The breaks that touch the changed
   files, plus S17's own** (D-150); not the full harness.
10. `README.md`, `docs/README.md`, baseline rows, `PROMPT-REGISTRY.md`, and
    `sessions/reports/SESSION-17-REPORT.md`.

## 08 — Explicit non-goals

- No link from a policy record to a company, part or technology: that is S18.
- No assessment of an instrument's effect, no exposure score and no forecast.
- No legal advice, and no legal or regulatory status the instrument's own text or its authority does not
  state.
- No EU digital-law coverage beyond what bears on the chain (`Eu-Digital-Policy` boundary).
- No page for the policy layer unless the human approves its design first.
- No full merged break harness (D-150): it runs at M5's audit.
- The three harness improvements, unless the human schedules them into S17 at H-0.

## 09 — Constraints

- **A new record type is a foundational schema change:** proposed with its consequences, decided by the
  human, recorded as a decision, enforced by checks written first. `SESSION-PROMPT-SPEC.md` §4 asks for an
  audit after it; M5's audit covers it.
- **Evidence-first:** every field rests on the instrument's own text or its authority's publication,
  retrieved, hashed and re-read.
- **Claim discipline:** what a text says is attributed to its authority; the Atlas's reading is an
  `INTERPRETATION`, kept apart.
- **Unknown is never zero;** a proposed instrument is never shown as in force.
- **Plain language first,** codes behind it.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Knowledge Architect | the proposal; `decisions.md` (append); schemas and vocabularies after H-1 | IDs, types, states |
| Source Scout | `sessions/reports/SESSION-17-research/` | candidates, never evidence |
| Extractor | `data/sources.json` at retrieval; drafts in `data/staging/` | provenance on every record |
| Verifier | verification of the drafts | may reject or downgrade; may not fabricate |
| Data Auditor | validators; tests; S17's breaks | fail-first |
| Editorial | the proposal's plain-language text | no fact not in a record |

## 11 — Data and evidence rules

- **Canonical entities:** the new policy records, only after H-2. Existing records unchanged.
- **Relationship types:** none recorded in S17; S18's types are only defined.
- **Required sources:** the instrument's own text, or its issuing authority's publication. Secondary sources
  locate; they never support a policy record's fields.
- **Temporal:** every date (adopted, published, in force, amended) with its basis.
- **Unknown:** status or date not stated by the text stays in its state word, never guessed.

## 12 — Implementation rules

**May create:** `docs/architecture/policy-dataset.md`; the new schema and its tests; `sessions/reports/SESSION-17-*/`;
the report.

**May modify, after H-1:** `schemas/`, the vocabularies, `docs/research/source-policy.md` (new rows),
`docs/architecture/entity-taxonomy.md`, `claim-model.md`, the validators and tests.

**May modify, after H-2:** `data/` (the new records, and sources at retrieval).

**Always:** `decisions.md` (append), docs indexes, baseline rows, `PROMPT-REGISTRY.md`.

**Prohibited:** a graph database or new dependency; any change to `Eu-Digital-Policy`; a policy record
without its text retrieved; a loosened check.

## 13 — Verification plan

- At start: fresh virtualenv, suite, Gate 0, `--check`; base recorded.
- Each approved schema or rule change: its check first, failing for its reason.
- Research: hashes recorded, anchors re-read.
- Breaks: those touching the changed files plus S17's own (D-150). Browser QA only if a page changes.
- CI is reported separately.

## 14 — Evaluation requirements

The report records the proposal and its rulings, each change with its check, the search plan and log, each
record's outcome, deviations, invalidated assumptions, rejected alternatives and debt.

## 15 — Acceptance criteria

1. The policy record was proposed in plain language and decided by the human before any schema changed.
2. Every approved change has a decision and a check written first.
3. Every canonical policy record rests on its own text, retrieved, hashed and re-read, with its dates and
   their basis.
4. No policy record links to the chain (S18), and no record or text gives legal advice.
5. Staging is empty at the end, or holds only records the human chose to hold.
6. The suite, Gate 0, `--check` and the selected breaks pass; the full harness is not run (D-150).
7. The report satisfies SPEC §5, Part A and D-114.

## 16 — Stop conditions

Stop and report when:

- an instrument's text cannot be retrieved (an access gap; RA-4 is the human's choice);
- a field could only be filled by interpretation;
- the design would duplicate `Eu-Digital-Policy` or need a change to it;
- any condition in SPEC §2.16 or `CLAUDE.md` §18 applies.

**Human decisions** (`CLAUDE.md` §9A; recorded as outcomes, D-114):

- **H-0 (opening):** which kind of instrument first; when the harness improvements are scheduled.
- **H-1 (the proposal):** each design item.
- **H-2 (the records):** each record, recorded, refused or held.

## 17 — Deliverables

- `docs/architecture/policy-dataset.md`, its rulings and the approved changes with their checks.
- The search plan, the log and the approved records.
- The documentation and `sessions/reports/SESSION-17-REPORT.md`.

## 18 — Handoff

S17 hands S18:

- **The policy record as decided,** with its vocabulary and source rules.
- **The first policy records.**
- **The link types defined for S18** and the evidence each needs.
- **Debt with owners,** including the three harness improvements if not scheduled.
- **The recommended next decision,** per `CLAUDE.md` §9A.
- **Files to read first:** the S17 report; `policy-dataset.md`; the S18 entry of `SESSION-ROADMAP.md`.
