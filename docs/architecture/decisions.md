# Architecture Decision Log

Append-only. A superseded decision is marked `superseded by D-NNN`, never rewritten
(`SESSION-PROMPT-SPEC.md` §6).

Status values: `proposed` (awaiting human review) · `accepted` · `superseded`.

---

## D-001 — Constitutional documents stay at the repository root

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00)
- **Context:** The user placed `CLAUDE.md`, `MASTER-ARCHITECTURE.md`,
  `SESSION-PROMPT-SPEC.md`, `PROJECT-EVALUATION-FRAMEWORK.md`, `SESSION-ROADMAP.md`,
  the operational roadmap and the bootstrap prompt at the root. Every document refers to
  them by bare filename, and Claude Code loads `CLAUDE.md` from the root.
- **Decision:** Leave them in place, unmodified. `docs/README.md` indexes them.
- **Rejected:** moving them under `docs/` — this would break cross-references and
  `CLAUDE.md` loading, and restructure human-authored documents without need.

## D-002 — Session system layout

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00)
- **Context:** The operational roadmap places prompts under `sessions/prompts/`;
  `SESSION-PROMPT-SPEC.md` §5 places reports at `sessions/reports/SESSION-XX-REPORT.md`.
  `PROMPT-REGISTRY.md` links to prompts as `./SNN-PROMPT.md`, which resolves only when
  the registry sits beside them.
- **Decision:** `sessions/prompts/SNN-PROMPT.md` (verbatim, immutable once the session
  starts), `sessions/prompts/PROMPT-REGISTRY.md` (moved from the root with `git mv`,
  content unchanged) and `sessions/reports/SESSION-NN-REPORT.md`.
- **Rejected:** leaving the registry at the root (its links stay broken); rewriting its
  links (editing a human-authored document to fit a layout choice).

## D-003 — Tooling uses the Python standard library only

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00); amended by D-026 (pinned test-only dependencies)
- **Context:** Python is the intended language (MA §17). S00 needs only a structural
  validator and its tests.
- **Decision:** `tools/validate_repo.py` and `tests/` use the standard library (`unittest`,
  `pathlib`, `re`). No `pyproject.toml`, lockfile or third-party packages.
- **Rejected:** pytest, a linter/formatter, pre-commit hooks, a Makefile or a package
  layout. None has a current requirement; each can be added, with a recorded reason,
  when one appears (e.g. DuckDB in S14).

## D-004 — One CI job, read-only permissions

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00)
- **Decision:** `.github/workflows/ci.yml` runs the unit tests and the Gate 0 validator on
  every push and pull request, on Python 3.11 (the version the S00 checks were run on),
  with `contents: read` permission.
- **Rejected:** a Python version matrix, deployment/Pages jobs, scheduled runs. There is
  nothing to deploy and no compatibility requirement yet.

## D-005 — No placeholder directories or stub documents

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00)
- **Context:** CLAUDE.md §19 and MA §24 forbid adding infrastructure for appearance.
- **Decision:** Do not create `data/`, `schemas/`, `web/`, `analysis/` or empty stub
  documents. `docs/README.md` lists each planned artifact with its status and owning
  session; the session that first needs a directory creates and designs it.
- **Rejected:** a full scaffold of empty folders with `.gitkeep` files — it would fix a
  data layout before S03–S06 have designed one.

## D-006 — Independence from `Eu-Digital-Policy`

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00; independence confirmed)
- **Decision:** No file, code, folder structure, workflow or data was copied from
  `Eu-Digital-Policy`. That repository was not opened in S00. Methodological
  principles are taken only from this repository's own constitutional documents.
- **Consequence:** Any later reuse of a pattern from `Eu-Digital-Policy` must be
  reimplemented locally and recorded here (MA §4.2).

## D-007 — Baseline record references, not restates, the master architecture

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00)
- **Decision:** `docs/architecture/baseline.md` cites MA/CLAUDE.md sections and records
  only repository state, gaps and uncertainties.
- **Rejected:** copying MA content into the baseline — it would create a second home for
  the same architectural statements, and the two would drift.

## D-008 — First analytical question: global first, EU lens later (resolves U-1)

- **Session:** S00 (human review) · **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Context:** CLAUDE.md §10/§20 and MA §25 frame the first question globally; MA §6.3
  and MA §22 M2 frame it as EU dependence on non-EU capabilities.
- **Decision:** S01 onward answers *"Where are the critical dependencies behind AI
  compute, and what evidence supports that assessment?"* The EU vs non-EU question is
  a later analytical view over the same records, built from entity jurisdiction data.
  It is not a separate dataset.
- **Consequence:** Until that view is built, sessions do not classify entities as EU or
  non-EU. They must still record jurisdiction/location evidence where it is gathered, so
  the later view is possible without re-research.
- **Rejected:** framing everything as EU vs non-EU from the start; dropping the EU lens
  from the Atlas.

## D-009 — `OPUS-5.5-BOOTSTRAP-PROMPT.md` is superseded (resolves U-3)

- **Session:** S00 (human review) · **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Decision:** The session system (`SESSION-ROADMAP.md` + `sessions/prompts/`) governs
  sequencing and scope. The bootstrap prompt stays at the root, unmodified, as a
  historical reference. It does not set session scope.
- **Rejected:** keeping it as an active checklist that S00–S11 must jointly satisfy.

## D-010 — Agent contracts are written in S06 under `docs/agents/`; no `AGENTS.md` (resolves U-4, U-5)

- **Session:** S00 (human review) · **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Decision:** S06 (evidence/claim system) writes `docs/agents/roles.md` and
  `docs/agents/contracts.md` in the MA §12 format, because that is when the
  staging → verification → canonical workflow first exists. This repository has no root
  `AGENTS.md`; `CLAUDE.md` remains the single file of agent working rules.
- **Consequence:** The future S06 prompt must include this in its scope.
- **Rejected:** a root `AGENTS.md` (a second rules file next to `CLAUDE.md`); deferring
  the decision to S02.

## D-011 — S01 prompt drafted by Claude, pending human review

- **Session:** S00 (human review) · **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Decision:** Claude drafts `sessions/prompts/S01-PROMPT.md` following
  `SESSION-PROMPT-SPEC.md` §2. The human reviews and may edit it before S01 starts. It
  becomes immutable only once S01 begins.

## D-012 — S01 prompt: human text governs, Claude's detail aligned beneath it

- **Session:** S00 (human review) · **Date:** 2026-09-29 · **Status:** accepted (human instruction)
- **Context:** After D-011, the human supplied their own S01 prompt, in the S00 format, and
  asked for Claude's draft to be made compatible with it.
- **Decision:** `sessions/prompts/S01-PROMPT.md` = **Part A**, the human prompt verbatim
  (byte-identical to the upload), followed by **Part B**, Claude's 18-section
  elaboration (SESSION-PROMPT-SPEC §2). Part A governs any conflict. Alignments made in
  Part B:
  - layer names use Part A's wording (e.g. "HBM", "EDA/equipment");
  - Part A's human task and weekly gate become a plain-language chain overview and a
    terminology section. The weekly gate stays a human judgement;
  - Part A's report checklist is mapped onto the SESSION-PROMPT-SPEC §5 headings;
  - Part A's claim classes omit `ATTRIBUTION`. Part B keeps it, because CLAUDE.md §6
    takes precedence.
- **Rejected:** replacing Part A with Part B (the human's contract would be lost);
  keeping two separate S01 prompt files (two sources of truth for one session).
- **Supersedes:** the DRAFT notice in the D-011 draft. The human's instruction to merge
  this work into `main` is taken as approval of the combined prompt.

## D-013 — Map "EDA/equipment" as two sub-layers (5a EDA, 5b SME)

- **Session:** S01 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S01; TQ-05 answer)
- **Context:** Part A names "EDA/equipment" as one layer. The retrieved sources treat
  EDA (design software) and semiconductor manufacturing equipment (capital tools) as
  separate production inputs (SRC-002 p.3, p.6). EDA is also co-dependent with foundry
  process information (domain map EDA-03).
- **Decision:** In `docs/research/domain-map.md`, keep Part A's layer numbering but map
  the layer as two sub-layers, `5a EDA` and `5b SME`. S03/S04 decide whether the schema
  keeps them as one layer or two.
- **Rejected:** a single merged layer, which would hide the EDA ↔ foundry dependency;
  two fully separate top-level layers, which would renumber Part A's human-authored
  layer list without approval.

## D-014 — S01 source retrieval: raw retrieval only; blocked sites are recorded, not worked around

- **Session:** S01 · **Date:** 2026-09-29 · **Status:** superseded in part by D-039 (2026-09-30, human review of S05): the retrieval clause. Raw retrieval and no circumvention continue in D-039
- **Context:** At the start of S01 the environment blocked all primary-source hosts. The
  human widened network access mid-session. After that, several sites still refused
  plain HTTPS requests (HTTP 403 or a challenge page). A headless-browser fetch was
  attempted once and denied by the environment's permission check.
- **Decision:** Sources are retrieved with `curl` and read from locally extracted text
  (PDF via `pypdf`, installed only in the session scratch area, not the repository).
  Web search is used only to discover URLs. Sites that refuse ordinary requests are
  listed as "not retrievable" in `source-register.md` and their entries are marked
  `not_researched`. They are not replaced by snippets, and the access controls are not
  circumvented.
- **Consequence:** JEDEC, TSMC, Samsung, Intel, SEC, IEA and The Green Grid / ISO PUE
  sources are missing from S01. S05 should decide whether manual retrieval by the human
  is acceptable for such sources.
- **Rejected:** citing search snippets or secondary summaries in place of blocked primary
  sources; retrieving through a headless browser to get past bot filtering.

## D-015 — Provisional source tiers and the meaning of `verified` in research artifacts

- **Session:** S01 · **Date:** 2026-09-29 · **Status:** superseded by D-036 (2026-09-30, human review of S05) for the tier order, and by D-048 (2026-09-30, human review of S06) for the meaning of `verified`, which D-048 confirms and extends
- **Decision:** Until S05, source tiers follow the S01 prompt Part B §05 order (`T1`
  company documentation/filings … `T6` news). A `T1` company source is primary only for
  its own products and processes. Its comparative or superlative claims ("unique to",
  "world's first", "leader") are recorded as `ATTRIBUTION`. In research artifacts,
  `verified` means the Verifier role re-read the retrieved source and found the quoted
  anchor at its locator. It does **not** mean human review or canonical status
  (CLAUDE.md §9, class C).
- **Rejected:** reusing MA §10's evidence-status labels (`direct`, `partial` …) in S01;
  they belong to the S06 claim model and would create a second status vocabulary
  before that model exists.

## D-016 — S01 terminology review: working terms for S02–S04

- **Session:** S01 (human review) · **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Context:** Part A's "Human task" asked the human to challenge the domain map's
  terminology. The map listed 12 questions (TQ-01 to TQ-12).
- **Decision:** The human's answers, recorded once in `docs/research/domain-map.md`
  §7.1, are the working terminology for S02–S04. Later sessions may revise them, but
  only through a new decision record. The answers do not resolve the recorded source
  conflicts (map §5).
- **Rejected:** copying the answers into this log, which would give them a second home
  that could drift from the map.

## D-017 — Project boundaries for v1.0

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S02: "Approvo la baseline")
- **Context:** The boundaries are scattered across MA §3, §6.4 and §25, D-008, D-013 and
  D-016. Some rest on decisions and some on prose. S01 marked four energy concepts `v1`,
  while MA §6.4 adds energy "after the base graph is reliable".
- **Decision:** The boundaries are stated once, in `baseline.md` §2. Where MA and a session
  prompt differ, MA governs (SESSION-PROMPT-SPEC §1). So energy stays concept-level in v1
  (no records or edges); rated power and nameplate capacity are only attributes.
- **Rejected:** treating S01's `v1` energy calls as canonical scope (a session prompt would
  override MA); dropping energy from the domain map (the concept-level understanding is
  still needed, and S09 needs TQ-10's capacity rule).

## D-018 — Lessons from `Eu-Digital-Policy` adopted as architecture commitments

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S02: "Approvo la baseline"); all nine items L-01 to L-09 accepted
- **Context:** The S02 process benchmark (`milestone-audits/M0-audit.md` Part 1) found
  eleven anti-patterns (A-1 to A-11) in EU-DP's history. This record is the one home of
  the commitments that follow. The audit holds the evidence.
- **Decision:** the Atlas commits to:
  - **L-01 · Agent runtime comes last.** Until S19 finds a manual workflow that needs one,
    agents are role contracts (S06) plus deterministic validators. No orchestrator,
    dispatcher, autonomous write path or control plane (A-1).
  - **L-02 · A gate exists only when CI runs it.** No document may call a check a gate
    unless CI runs it on every push. An unrun check is described as "manual" (A-2).
  - **L-03 · Every session report records its base.** This means the commit it started
    from and the `git branch -a` result at start. A future Gate 0 extension checks the
    field (A-3). S02's report does this by hand.
  - **L-04 · No hand-typed derived counts.** A count in a document is either produced by a
    script or labelled "as measured at `<commit>`" (A-4).
  - **L-05 · One copy of each fact.** No inlined copies of data in pages, and no
    translations in v1.0 (NG-10). Each new data file joins the validator's scope in the
    session that creates it (A-5).
  - **L-06 · Two axes, per-record dates.** Claim type and evidence status are separate
    fields from S06's first schema. Verification dates are per record, never a batch
    stamp (K-3, A-8).
  - **L-07 · Only `main` counts, and there is no cumulative handover.** A lesson or
    decision is in force only once it is on `main`. Session state lives in the session
    report, and no single handover file accumulates sessions (A-6, A-10).
  - **L-08 · Reports keep "ran locally" and "CI result" apart,** and never report a
    placeholder as a value (A-7).
  - **L-09 · Read before you automate.** A step is performed and checked by hand on real
    sources before it is automated. Content review is budgeted before form checks (A-9).
- **Rejected:**
  - copying EU-DP's policy documents, validators or agent modules (MA §4.2, D-006);
  - adopting EU-DP's A/B/C/D autonomy detail beyond CLAUDE.md §9, which already has it;
  - a GP-06-style self-updating `CLAUDE.md` (EU-DP's own proposal records the case
    against it).

## D-019 — Milestone label convention (resolves U-2)

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S02: "Approvo la baseline")
- **Context:** U-2. MA §22 M0–M7 are portfolio milestones. `SESSION-ROADMAP.md` M0–M7 are
  Atlas project milestones.
- **Decision:** In documents written in this repository, a bare `M0`–`M7` means the
  `SESSION-ROADMAP.md` milestones. MA §22 milestones are always written "portfolio M4"
  or "MA §22 M4". The human-authored root documents are not edited.
- **Rejected:** renaming the milestones in MA or the roadmap (editing human documents to
  fix a label); a different letter prefix (it would diverge from both documents).

## D-020 — v1 concept classification is S03's starting input

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S02: "Approvo la baseline")
- **Decision:** The 40 `v1` concepts from S01 are classified as follows in
  `milestone-audits/M0-audit.md` Part 4 (the single home of the list):
  - 20 model;
  - 5 actor role;
  - 4 attribute;
  - 2 energy concept-only;
  - 9 definitional.

  S03 starts from this list. S03 may reclassify a concept only through a decision record
  that gives the reason. The "actor role" class asks S03 to test MA §6.1's role-named
  entity types (`CloudProvider`, `EquipmentSupplier`) against the S01 blurs B-2 and B-3.
- **Rejected:**
  - modelling all 40 as entity types (it would create entities for glossary terms);
  - deciding the schema here (S03 owns it).

## D-021 — Non-goals frozen for v1.0

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S02: "Approvo la baseline"); non-goals frozen from this date
- **Decision:**
  - `baseline.md` §6 lists the non-goals NG-01 to NG-13. That list is their only home.
  - Once accepted, they are frozen until the v1.0 release (S25).
  - A non-goal changes only through a new decision record, approved by the human
    **before** the work starts.
  - A session that finds a non-goal blocking must stop and report (CLAUDE.md §18). It
    may not work around the non-goal.
- **Rejected:** freezing until the end of M1 only (too short to protect the build
  phases); an unwritten list carried in each session prompt (it would drift from one
  session to the next).

## D-022 — Entity taxonomy: six instantiable types, two reserved, four record kinds owned elsewhere

- **Session:** S03 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S03); Event schema owner S09 confirmed
- **Context:**
  - `SESSION-ROADMAP.md` S03 lists twelve candidates. The human's S03 focus names ten.
  - MA §5.1 and §6.1 list more, some of them role or facility labels.
  - M0 Part 4 (D-020) says which v1 concepts must be modelled.
- **Decision:** `docs/architecture/entity-taxonomy.md` is the one home of the type
  reasoning. `schemas/entities.schema.json` is the one home of field shapes and vocabulary
  values.
  - **Instantiable domain types:** `company`, `facility`, `technology`, `component`,
    `product`, `jurisdiction`.
    - Each has its own identity test (taxonomy R-1) and a v1 use (R-2, §5).
    - The human's "Country" is the type `jurisdiction`, with kind `country` the only one
      allowed in v1. This avoids a rename when the D-008 EU lens needs a supranational
      jurisdiction.
  - **Reserved** (defined, no schema; the schema rejects their records):
    - `institution`: S05/S06 if source publishers link to it, otherwise S17;
    - `policy`: S17.
  - **Record kinds** (boundary defined here, schema owned elsewhere):
    - `source` (S05/S06);
    - `claim` (S06);
    - `relationship` (S04);
    - `event`: S09, **proposed**, because S09's gate is the temporal facility model.
      The roadmap names no owner.
  - Design rules R-1 to R-8 (taxonomy §1) apply to every later schema change.
- **Rejected:**
  - one entity schema holding claims, sources, events and relationships as "entity types"
    (four kinds with different owners and lifecycles in one schema);
  - a type named `country` (renamed later, when the EU lens arrives);
  - instantiating `institution` now (no v1 concept needs it, R-2);
  - an Event schema in S03 (no dated record exists before S09; L-09).

## D-023 — Dispositions of the MA entity-type lists

- **Session:** S03 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S03)
- **Context:**
  - MA §6.1 lists role-named types (`CloudProvider`, `EquipmentSupplier`) and
    facility-named types (`Fab`, `PackagingFacility`, `DataCentre`).
  - D-020 asked S03 to test the role-named types against blurs B-2 and B-3.
  - MA §5 expects physical schemas to "differ" while the concepts converge. So mapping an
    MA type onto a role or a kind puts MA's concept into practice; it does not override
    MA (SESSION-PROMPT-SPEC §1: expected evolution, not a scope violation).
- **Decision:** every MA §6.1 and §5.1 entity type has exactly one disposition, in
  `entity-taxonomy.md` §6 (machine-checked). In summary:
  - role-named types become `roles` values on Company;
  - facility-named types become `facility_kinds` values;
  - `ChipDesign` is folded into Product for v1;
  - `Investment` is an event;
  - `Metric` is a derivation (NG-11);
  - a cited `standard` is a source;
  - `dependency` is a relationship or a derivation;
  - policy-named types are reserved for S17;
  - `provision` stays out of this repository;
  - energy and network assets are excluded (NG-04, NG-05).
  - MA §5.1's example-record fields `jurisdiction`, `status` and `source_ids` are not
    adopted (taxonomy §4.5).
- **Rejected:**
  - typing firms by role (one firm would need several records: blurs B-2, B-3);
  - dropping MA types without a recorded disposition;
  - a separate `ChipDesign` type (no v1 concept needs a design apart from the product,
    and it would give "which process is this chip made on" two homes).

## D-024 — Actor roles are claim-backed, time-bounded values on Company; FAB-03 reclassified

- **Session:** S03 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S03)
- **Decision:**
  - What a firm does is recorded in the company's `roles` attribute. Each value cites
    claims and may carry `valid_from`/`valid_to`. A company may hold several roles.
  - The vocabulary (defined in the schema):
    - `fabless_designer`, `idm`, `foundry_operator`, `osat`, `memory_manufacturer`,
      `cloud_provider`, `equipment_maker`, `eda_vendor`.
  - A role is **never derived** from relationships. "Fabless" asserts that a firm has *no*
    fabs, and incomplete data cannot establish an absence (unknown ≠ none). A later
    semantic check may warn when a role and the relationships disagree (taxonomy §9).
  - **FAB-03 "Foundry" is reclassified from model to actor role** (`foundry_operator`),
    as D-020 allows.
    - Reason: TQ-04 made "foundry" the business model and "foundry operator" the firm,
      and no separate foundry record is needed.
    - The fab itself is FAB-02, a facility kind.
    - M0 Part 4 is not edited. Taxonomy §5 records the move and cites this decision.
  - `equipment_maker` and `eda_vendor` are not D-020 concepts.
    - They come from the actor-type column of domain map §4, and from MA's
      `EquipmentSupplier`.
    - They are added so that layers 5a and 5b have actors (`INTERPRETATION`).
    - Each assignment still needs a claim.
- **Rejected:**
  - deriving roles from edges;
  - roles as relationships to role records (a role is not an entity);
  - a `hyperscaler` role (TQ-08);
  - an `accelerator_designer` role for B-2. The S04 `designs` relationship already says
    it, and a role would be a second home.

## D-025 — Attribute value contract for entity records

- **Session:** S03 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S03)
- **Decision** (explained in taxonomy §7; the schema is the home of the shapes):
  - **Two groups of field.** Identity fields say *what the record is*. They include
    `identity_claim_ids`, which needs at least one claim. Attributes say *what is true of
    it*.
  - **Two forms of attribute.** Every attribute holds either a non-empty list of
    assertions `{value, claim_ids, valid_from?, valid_to?}` or an explicit state:
    - `not_researched`;
    - `not_publicly_determinable`, which must cite claims;
    - `not_applicable`.
  - **Every field of a type is required.** A missing field or `null` is invalid.
  - **Unknown is never zero or false.** Power and capacity values must be greater than
    zero. A boolean is `false` only when a source says so.
  - **Evidence states stay on claims.** `verified` and `disputed` describe evidence, so
    they belong to claims (S06; K-3, L-06). Competing values are several assertions.
  - **Forbidden fields:** no free-text `notes`, `status` or `layer`.
  - **References are typed by ID prefix.** Whether a referenced record exists is checked
    by `validate-data` (S06/S07).
  - **Taxonomy is a field; composition and dependency are relationships.** Hierarchy is
    the `broader` field. "Part of" and "requires" are S04 relationships.
  - **The claim ID format is fixed** as `claim-<slug>`. S06 may change it through a
    decision.
- **Rejected:**
  - optional or nullable fields (a missing field hides "not researched", so it breaks
    unknown ≠ null);
  - record-level `source_ids` (they cannot say which source supports which value);
  - a `disputed` value state (it would duplicate the claim's evidence status: a second
    home);
  - taxonomic `is_a` relationships in S04's table (dependency queries would walk the
    classification tree).

## D-026 — Pinned test-only dependency for schema validation (amends D-003)

- **Session:** S03 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human
  decision on the S03 plan: "Schema + jsonschema tests")
- **Context:**
  - S03's registry gate is a stable entity schema.
  - A JSON Schema is only known to behave when records are validated against it.
  - D-003 allowed a dependency "with a recorded reason, when one appears".
- **Decision:**
  - `requirements-test.txt` pins `jsonschema` and its transitive dependencies to exact
    versions. CI installs it before the tests.
  - `tests/test_entity_schema.py` validates fictional fixtures. Valid records must pass,
    and each invalid case (one mutation of a valid record) must fail.
  - `tools/` stays standard-library only. Only tests may import pinned test dependencies.
- **Rejected:**
  - a hand-written validator for a subset of JSON Schema (it reimplements a standard, and
    would itself need testing);
  - leaving the schema untested until S06/S07;
  - an unpinned requirement (the result could change between runs).

## D-027 — S08 creates the first product records

- **Session:** S03 (human review) · **Date:** 2026-09-30 · **Status:** accepted (human decision)
- **Context:** Product is an instantiable type (D-022), but no roadmap session was
  assigned to create product records (`entity-taxonomy.md` §9).
- **Decision:** S08 (technology + component dataset) creates the first product records.
  S08 already creates the component and technology classes, so each product's
  `instance_of` can point to a class made in the same session. S10 then connects
  products with supply-chain edges.
- **Consequence:** the future S08 prompt must include product records in its scope.
- **Rejected:** creating products only in S10, which would build classes and their
  instances in different sessions and leave S10 to do both entity and edge work.

## D-028 — Relationship record contract

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S04: "Approve all six")
- **Context:**
  - MA §5.4 shows a relationship with `id`, `source_entity`, `relation_type`,
    `target_entity`, `valid_from`, `valid_to` and `source_ids`.
  - S03 replaced record-level `source_ids` on entities with claim-level provenance
    (D-025).
  - The S06 gate asks "What exactly supports this relationship?".
- **Decision:** `schemas/relationships.schema.json` is the one home of the record shape.
  `relationship-taxonomy.md` §1–§2 explains it.
  - **Fields:**
    - `id` (`rel-<slug>`);
    - `relation_type`;
    - `source_entity` and `target_entity`, typed by ID prefix (MA §5.4 names kept);
    - `claim_ids`, with at least one claim;
    - optional `valid_from` / `valid_to` (partial dates);
    - a per-type qualifier only where the type needs one (`item`, `supplier`).
  - **Replaced:** MA §5.4's `source_ids` is replaced by `claim_ids`, following the D-025
    precedent.
  - **Forbidden:** `source_ids`, `notes`, `status`, `confidence`, `evidence_status` and any
    inverse or symmetric field. Evidence status lives on claims (L-06).
  - **Endpoints** are instantiable entity types only (D-022). Reserved types, record kinds
    (source, claim, event) and jurisdictions are never endpoints. The schema rejects
    placeholder endpoint IDs (`…-unknown…`, `…-tbd` and similar).
  - **Every type is directed and stored once.** Inverse readings are display text. No
    inverse, transitive or derived edge is stored.
  - Shared shapes (claim IDs, partial dates, entity ID patterns, assertions, explicit
    states) are `$ref`s into `entities.schema.json`, never copies. A test proves that
    `jsonschema` resolves them.
- **Rejected:**
  - record-level `source_ids` (it cannot say which source supports the edge);
  - a confidence score (it invents precision; confidence is the claim's evidence status);
  - a free-text `notes` field (a hidden second home);
  - a stored `status` (derived, R-8);
  - copying the shared shapes into the relationship schema (two homes).

## D-029 — Relationship vocabulary v1: eleven types at two levels

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S04: "Approve all six")
- **Context:**
  - `SESSION-ROADMAP.md` S04: "prevent accidental inference from co-occurrence"; gate
    "Every relationship has a clear semantic definition and evidence expectation."
  - The domain map separates structural from contingent dependencies, which need
    different evidence.
  - S03 left ownership, operation, composition and design, fabrication and packaging to
    S04 (`entity-taxonomy.md` §9).
- **Decision:** the v1 types, each defined in the schema and explained in
  `relationship-taxonomy.md` §4, with evidence expectations in §5:
  - **class level** (technology and component endpoints, no dates): `requires`,
    `has_part`;
  - **instance level** (at least one company, facility or product endpoint): `owns`,
    `operates`, `designs`, `fabricates`, `packages`, `incorporates`, `supplies`,
    `houses`, `provides_access_to`.
  - **One verb, one level (RR-2).** A class-level statement needs a source stating
    necessity for the class. A product's use of a class is an instance edge.
  - **Direction convention:** structural edges point from the dependent to the
    dependency; activity edges point from the actor to its object.
  - **Composition** is `has_part` (whole → part), so that it follows the convention. "Part
    of" is its display reading.
  - **Ownership** is an `owns` edge with its own claims and period. It is not derived from
    acquisition events: event histories are rarely complete, and filings state the
    ownership itself. Acquisitions and investments stay events (D-023).
  - **Activity edges target named products only.** What a firm does in general is a role
    (D-024).
  - **Kind constraints** (use class, facility kind, product kind) need the endpoint
    record. They are documented in taxonomy §2 and checked by `validate-data` later.
    The schema checks types by prefix.
- **Rejected:**
  - one verb serving both levels;
  - `manufactures` or `produces` as umbrellas (TQ-06);
  - `part_of` as the stored direction;
  - company → class edges;
  - symmetric types;
  - a stored `depends_on`.

## D-030 — Reconciliation of the three verb lists; one-home rulings on S03 fields

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S04: "Approve all six")
- **Context:** MA §6.2, the `SESSION-ROADMAP.md` S04 list and domain map §3 name
  different verbs (28 distinct, as measured at `1d0522c` by the parser in
  `tests/test_relationship_taxonomy.py`). `baseline.md` §4 asks S04 to reconcile them.
- **Decision:** every verb has exactly one disposition, in `relationship-taxonomy.md` §6
  (machine-checked against the three documents):
  - **adopted:** `owns`, `operates`, `supplies`, `requires`, `designs`, `packages`,
    `fabricates`, `houses`;
  - **merged:**
    - `enables` → `requires` (its inverse);
    - `licenses` → `supplies`;
    - `offered_via` → `provides_access_to`;
    - `integrates` → `packages`;
    - `stacks_on` → `has_part`;
  - **entity field:** `located_in`;
  - **events:** `invests_in`, `acquired`;
  - **derivations:** `depends_on`, `competes_with`;
  - **reserved for S17:** `restricted_by`, `regulated_by`, `supported_by`,
    `constrained_by`;
  - **excluded:** `supplies_power_to` (NG-05);
  - **rejected as vague:** `manufactures`, `produces`, `uses`, `partners_with`,
    `affected_by`.
  - **One home:** every accepted S03 field listed in the S04 prompt stays the home of its
    fact (taxonomy §7):
    - `located_in`, `incorporated_in` and `headquartered_in`;
    - `vendor`;
    - `broader` and `instance_of`;
    - `vendor_process_name`;
    - `roles`.

    No fact moves from a field to an edge, so no accepted S03 decision changes. No v1
    type has a jurisdiction endpoint.
  - **Exclusions:** DEP-10 and DEP-11 map to no edge (taxonomy §8). The reasons are
    definitional endpoints, a two-way relation, and a market-state claim.
  - **MA text is not edited.** MA §6.2 introduces its list as "Examples". MA §5.4's
    `manufactures` is replaced by the specific activity types.
- **Rejected:**
  - adopting all 28 verbs (several have no definable evidence expectation);
  - a `located_in` edge beside the fields (a second home);
  - editing MA to match.

## D-031 — Unknown suppliers and non-public edges

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S04: "Approve all six")
- **Context:**
  - DEP-01 and HBM-06: which HBM maker supplies which accelerator is
    `not_publicly_determinable` from the product documentation retrieved.
  - `SESSION-ROADMAP.md` S10: "No relationship is published without evidence or an
    explicit non-published/unverified state." A missing edge must never read as "no
    relationship".
- **Decision:**
  - `incorporates` carries a required `supplier` qualifier, using the D-025 attribute
    contract:
    - claim-backed company assertions, where several means multi-sourcing; or
    - `not_researched`; or
    - `not_publicly_determinable`, citing claims that show what was searched.
  - When the part is a named product, `supplier` must be `not_applicable`, because the
    part's `vendor` already says it. The schema enforces this.
  - A missing edge means "not recorded". Consumers must not render it as "none", and
    metrics must not count it as zero.
  - Placeholder companies are rejected by the schema.
  - A general "unknown endpoint" record is **not** created in v1. S01's other
    non-public findings are quantities, not parties. S10 proposes one if it meets the
    case (M0 audit A-1; L-09).
- **Rejected:**
  - a placeholder company;
  - leaving the supplier out (hides `not_researched`);
  - inferring the supplier from market share or a supplier's customer list;
  - an unknown-endpoint record type now.

## D-032 — Vendor-named packaging processes and constituent-level fabrication are not modelled in v1

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S04: "Approve all six")
- **Context:**
  - SK hynix describes CoWoS as "A TSMC proprietary packaging process" (PKG-04, SRC-014).
  - SK hynix plans to use TSMC's logic process for the HBM4 base die (DEP-04), so one
    product's dies would come from two fabricators.
  - The chip's fabrication process already lives in `product.vendor_process_name`.
- **Decision:**
  - No packaging-process qualifier on `packages`, and no `part` qualifier on
    `fabricates`, in v1.
  - CoWoS does not become a technology record (R-4). It never goes into
    `vendor_process_name`, whose definition is the fabrication process.
  - A `fabricates` edge is never recorded for a whole product when the evidence covers
    only one constituent. S10 must stop and propose a qualifier, with the first confirmed
    case as its evidence.
- **Rejected:**
  - a `packaging_process` qualifier now: no retrieved source ties a named packaging
    process to a named product;
  - a `part` qualifier now: its only case is an announced plan, an event;
  - reusing `vendor_process_name`: it would make that field mean two things.

## D-033 — Role and edge conflicts are semantic warnings; validate-data rules for edges

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S04: "Approve all six")
- **Context:**
  - D-024 makes roles claim-backed and never derived. It foresaw "a later semantic check"
    when roles and relationships disagree.
  - MA §14 Gate 3 asks for "no impossible relationships".
- **Decision:**
  - The conflicts RW-1 to RW-3 (`relationship-taxonomy.md` §11) are **warnings**. They
    are raised when a `fabless_designer` company also owns or operates a wafer fab,
    fabricates, or packages, over overlapping or undated periods.
  - No record is corrected automatically.
  - An `idm`, `foundry_operator` or `memory_manufacturer` that packages (B-3), and a
    `cloud_provider` that designs (B-2), are not conflicts.
  - Rules V-1 to V-9 in taxonomy §15 are handed to `validate-data` (S06/S07). They cover
    references resolving, kind constraints, self-loops, date order, duplicates, `broader`
    restated as an edge, the vendor of a supplied item, the role warnings, and
    placeholder entity IDs.
  - None of them is a gate until CI runs it (L-02).
- **Rejected:**
  - correcting roles or edges automatically;
  - encoding the role checks in the relationship schema: they need two records, and
    JSON Schema sees one.

## D-034 — Source classes: document kinds, one per source, in a vocabulary schema

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte")
- **Context:**
  - `SESSION-ROADMAP.md` S05: "Create a source hierarchy tailored to industrial technology
    research".
  - The register's 23 sources and its blocked hosts include filings (blocked), datasheets,
    press releases, product pages, newsroom explainers, government documents, national
    laboratory reports, policy briefs and an association report.
  - The human chose option (b) for machine-readability before S05 started, with (a) as the
    fallback (S05 prompt Part B §16, H-2: "i follow your recommendations").
- **Decision:**
  - The classes, defined once in `schemas/sources.schema.json`: `company_filing`,
    `company_technical_documentation`, `company_press_release`, `company_marketing`,
    `standard_specification`, `government_publication`, `research_report`,
    `policy_research_brief`, `industry_association`, `market_research_consultancy`,
    `news_media`.
  - `source-policy.md` §2 and §3 hold what each class is primary for, what it is never
    enough for, and a neighbour test for each easily confused pair.
  - Company sources are split by document kind, because each kind answers for different
    things.
  - One class per source. A joint or commissioned report takes its publisher's class
    (SRC-005: `industry_association`).
  - Search results, snippets, aggregator copies and tertiary summaries are not sources and
    have no class.
  - The classes settled (CSET by document purpose; SIA/BCG by publishing party), so H-2's
    option (b) applies, not the fallback.
- **Rejected:**
  - one `company` class;
  - "primary" and "secondary" as classes (D-035);
  - a two-class value for joint reports;
  - a `tertiary_summary` class;
  - the full source-record schema now (S06's, H-2).

## D-035 — Standing, attribution chains and independence

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte")
- **Context:** D-015 made a company source primary "for its own products and processes".
  S04's worked examples showed a company can be first-hand about an edge with another firm
  (NVIDIA naming TSMC's process for NVIDIA's own chip, SRC-006), and a laboratory can be
  second-hand (LBNL reporting IDC, DEP-11).
- **Decision:**
  - "Primary" is a relation between a source and one claim, called **standing**:
    `party`, `originator` or `reporter` (`source-policy.md` §4). It is a claim field for S06,
    not a class.
  - First-hand means `party` (instance-level claims) or `originator` (class-level claims and
    definitions). `reporter` supports at most `ATTRIBUTION`.
  - Second-hand claims record the chain (reporter, originator, locator). The originator is
    never cited as if retrieved.
  - Sources are independent only when their publishers differ and neither commissioned the
    other. One publisher's documents are one voice.
  - To test `party`, S06's source record must let a company publisher be a reference to a
    company record. `institution` stays reserved (D-022).
- **Consequence:** S01's corroboration of DEP-02 and DEP-03 rests on one publisher (SK
  hynix). The domain map is not edited. S08 and S10 must find an independent source before
  those class-level edges are recorded as `FACT`.
- **Rejected:**
  - standing as a source property (one source can be party to one claim and reporter for
    the next);
  - counting pages rather than publishers for corroboration.

## D-036 — Preference matrix; no global ranking; MA §10 and D-015 reconciled

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte")
- **Context:**
  - The roadmap S05 gate: "Every material claim type has a preferred source class."
  - MA §10 and D-015 give two different global orders (`source-policy.md` §9).
  - D-015: provisional tiers, "superseded by S05's source policy when written".
- **Decision:**
  - Material claim types are read from the schemas: every relation type, every edge
    qualifier with its own claims, the identity of every entity type, and every attribute
    field. Each has one row in `source-policy.md` §7, which assigns every class to
    preferred, acceptable or never sufficient alone, and states the standing and freshness
    it needs. Rows point to `relationship-taxonomy.md` §5 and the entity schema; they never
    copy them. A test fails when a schema gains a type or field without a row.
  - No global ranking survives. The matrix is the "project-specific source policy" MA §10
    asks for. MA's order stays as its general guidance, and MA is not edited.
  - D-015's tier order is superseded by this decision once accepted. D-015's meaning of
    `verified` in research artifacts stays in force until S06's claim model confirms or
    replaces it.
  - Event types get rows when S09 defines them. Until then ER-8 governs plans.
- **Rejected:**
  - keeping MA §10's or D-015's order as a tie-break;
  - a hand-written list of claim types (it would drift from the schemas);
  - numeric scores per class (D-028; NG-11).

## D-037 — Evidence rules ER-1 to ER-10, including the search rule for `not_publicly_determinable`

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte")
- **Context:** S04 left three evidence rules without a policy home
  (`relationship-taxonomy.md` §12, §9): the process name as fabricator, the vendor as
  designer, and a single page's silence.
- **Decision:** `source-policy.md` §6 is the one home of ER-1 to ER-10. In particular:
  - ER-1: a foundry named only inside a process name supports fabrication only as
    `DERIVATION`;
  - ER-2: a vendor is not a designer;
  - ER-3: `not_publicly_determinable` needs every **preferred** class of the row to have
    been searched for the specific question. The claim records the question, the classes
    and sources searched, the date and the result. An inaccessible preferred class leaves
    the value `not_researched`;
  - ER-8: plans and forward-looking statements, in any class, support an event and an
    intention, never a state;
  - ER-9: company-level statements never support product-level edges or suppliers;
  - ER-10: a preferred class is never a verification.
- **Rejected:**
  - letting a filing's supplier list stand in for a product's supplier (S05-R1 shows why);
  - allowing `not_publicly_determinable` after searching any class other than the
    preferred ones.

## D-038 — Conflict policy: kinds of conflict, never settled by rank

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte")
- **Context:** Domain map §5 preserves CON-01 to CON-05. CLAUDE.md §9 makes "publication of
  unresolved material disputes" human-only.
- **Decision:**
  - Kinds: `definitional`, `wording`, `factual_contradiction`, `temporal`, `scope`
    (`source-policy.md` §10.1). Each has a recording rule.
  - No conflict is settled by class or rank. Evidence is never deleted.
  - A factual contradiction closes only on new evidence that explains it, and a material
    one also needs the human. A working definition is a choice, not a resolution.
  - Self-interest is recorded through class and standing. It is not a kind of conflict and
    never decides one.
  - CON-01 to CON-05 are each classified in §10.2, and all stay preserved. The domain map is not edited.
- **Rejected:**
  - self-interest as a kind;
  - resolving a conflict by the higher-preferred class (CON-02 shows the rank orders would
    have favoured the less specific source).

## D-039 — Retrieval and access; manual retrieval by the human (supersedes D-014's retrieval clause)

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte")
- **Context:**
  - D-014 asked "whether manual retrieval by the human is acceptable".
  - The human answered before S05 started (Part B §16, H-1: "i follow your
    recommendations"): allowed, with conditions.
- **Decision:**
  - `source-policy.md` §11, RA-1 to RA-7. Raw retrieval and no circumvention continue from
    D-014.
  - RA-4 records H-1: legitimate access only; targeted; each download records URL, the
    method "manual, by the human", the human's download date and a content hash, and is
    marked not reproducible; full texts stay out of the repository; verification is
    unchanged.
  - Following a site's published rules for automated clients is not circumvention, but only
    after the rules have been read. For SEC EDGAR they could not be read: the refusal page
    cites a policy that is behind the same refusal (S05-A1). Nothing is assumed, and no
    client identity was sent.
  - Declaring an identity to a site is the human's decision (class D).
  - Whether "external API dependency" becomes a non-goal is recorded, not decided.
- **Consequence:** D-014's retrieval clause is superseded once this is accepted; its
  status line changes at the human's review.
- **Rejected:**
  - sending a declared client identity to EDGAR from memory of its policy;
  - treating a secondary summary of a paywalled standard as the standard.

## D-040 — Freshness: separate dates, byte changes trigger re-checks, a proposed 12-month horizon

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte"); the 12-month horizon approved ("12 mesi")
- **Context:** Undated live pages (register note 3); CSET's 2019 data; SK hynix's 2024 plan.
  S05 re-retrieved every registered source: some returned changed bytes, yet every anchor
  re-read was still at its locator (counts as measured on 2026-09-30 are in `source-policy.md` §12).
- **Decision:**
  - As-of date, publication date, access date with content hash, and verification date are
    kept apart. The as-of and verification dates belong to claims (S06).
  - A changed hash triggers an anchor re-check. Staleness is a missing anchor, a newer
    edition in the same series, or a plan whose date has passed.
  - `time_sensitive` matrix rows: evidence more than 12 months old at use must be re-checked.
    The 12 months is a proposal for the human (`INTERPRETATION`). `stable` rows have no age
    limit.
  - `validate-freshness` implements this later (S06+).
- **Rejected:**
  - treating any byte change as staleness (it would have flagged sources whose anchors had not
    moved; `source-policy.md` §12);
  - one age limit for every claim type.

## D-041 — Where each source's class lives; the CSET decision

- **Session:** S05 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S05: "Approva tutte")
- **Context:** The register holds S01's provisional `source_tier`. S06 migrates the register
  into source records and then freezes it. S05 may not edit the register without a
  human-approved decision (Part B §08).
- **Decision:**
  - `source-policy.md` §8.1 is the one home of each registered source's class until S06.
    The source record's class field then becomes the home, and §8.1 becomes history.
  - The register is not annotated. Its tier column stays S01's record.
  - Sources retrieved in S05 are listed in §8.3 (S05-R1) until S06 migrates them.
  - CSET (SRC-002, SRC-003) is `policy_research_brief`: in S01's terms, from T4 to T5
    (register note 1).
- **Rejected:** annotating the register (a second home, and outside S05's write boundary).

## D-042 — Filings are taken from the filer's own published copy; no identity is declared to EDGAR

- **Session:** S05 (human review) · **Date:** 2026-09-30 · **Status:** accepted (human decision: "Filing dai siti aziendali")
- **Context:** SEC EDGAR refused plain requests, and the access policy it cites is behind the
  same refusal (`source-policy.md` §11, S05-A1). D-039 left the path to the human.
- **Decision:**
  - Filings are retrieved from copies the filer publishes itself (as S05-R1), under RA-6.
    Each records its host, and that its identity with the regulator's copy is not verified.
  - No client identity is declared to EDGAR. Filings available only from the SEC remain an
    access gap.
- **Rejected:** the human reading EDGAR's policy now (possible later, under RA-4, through a
  new decision); leaving filings as a gap.

## D-043 — External API dependency is a v1.0 non-goal (NG-14; amends the D-021 list)

- **Session:** S05 (human review) · **Date:** 2026-09-30 · **Status:** accepted (human decision, given before the change: "Sì, non-obiettivo v1.0")
- **Context:** S00 listed "external API dependency" as a session non-goal. Baseline §6 left it
  to the human. D-039 recorded it as a question. D-021 lets the non-goal list change only
  through a decision the human approves before the work starts.
- **Decision:** NG-14 is added to `baseline.md` §6: no runtime or retrieval dependency on an
  external API in v1.0. Sources are retrieved by ordinary HTTPS requests (RA-1) or manually
  by the human (RA-4). It is frozen with the other non-goals until S25.
- **Rejected:** leaving the question open (the policy's retrieval rules already assume no API);
  allowing regulator APIs now (no session needs one, and it would add an external runtime
  dependency).

## D-044 — The claim record: one proposition, linked from records, row derived

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:**
  - Entity and relationship records already cite `claim_ids` (D-025, D-028), and the
    `claim-<slug>` format waits for the claim record (`entity-taxonomy.md` §7).
  - The S06 gate asks "What exactly supports this relationship?".
- **Decision** (`claim-model.md` §1; shapes in `schemas/claims.schema.json`):
  - A claim is one proposition, stated once. Several sources supporting it are citations on
    that one claim. Corroboration still needs independent publishers (ER-7).
  - The link runs one way: records list claims, and a derived claim lists its inputs. A
    claim never lists the records it supports. The inverse is computed (the trace).
  - The matrix row a claim is judged against is derived from the citing record and field,
    never stored on the claim.
  - The `claim-<slug>` format is kept. No accepted schema changes.
- **Rejected:** a `supports` list on the claim (a second home for the link); a `matrix_row`
  field (one claim can serve two rows); one claim per source sentence (it would split one
  proposition across records).

## D-045 — Claim types: the CLAUDE.md labels; MA §10's list reconciled

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:** CLAUDE.md §6 and the roadmap S06 require their labels. MA §10 lists its own
  types "at minimum".
- **Decision** (`claim-model.md` §2, machine-checked against MA):
  - The values are `FACT`, `ATTRIBUTION`, `DERIVATION`, `INTERPRETATION`, `IMPLICATION`,
    written as CLAUDE.md writes them.
  - MA's fact, derived, attributed and interpretation map directly.
  - A critique is an `ATTRIBUTION` when a named source makes it, and an `INTERPRETATION`
    when the Atlas does.
  - A forecast is an `ATTRIBUTION` (a third party's, or a company's plan under ER-8). The
    Atlas's own forecasts are out of scope (NG-11).
  - Law / normative text is reserved for the policy layer (S17).
  - MA is not edited.
- **Rejected:** MA's list as values (critique and forecast are the same labels with a
  speaker rule);
  lower-case values (a second spelling of labels used across the documents).

## D-046 — Evidence status vocabulary and the type × status rules

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:** L-06 requires claim type and evidence status as separate fields. S05 defined
  no status (`source-policy.md` §5, §16). MA §10 lists six statuses.
- **Decision** (`claim-model.md` §3–§4):
  - The values are `unverified`, `supported`, `partial`, `context_only`, `disputed`.
    - MA's `direct` is renamed `supported`, because "direct" reads like standing.
    - MA's `derived` is dropped: it duplicates the `DERIVATION` type.
  - Only `supported` and `disputed` claims may be canonical.
  - A claim with inputs is no stronger than its inputs (the §4 status table).
  - `disputed` applies to factual contradictions only, on `FACT` and `DERIVATION`. It names
    the competing claims, mutually, and never replaces them.
  - The type table (§4) fixes, per type: sources or inputs, standing, reasoning, `as_of`,
    and the allowed statuses. The schema enforces it, and a test checks the two agree by
    probing every type and status.
- **Rejected:** a numeric strength or confidence (NG-11); `disputed` for definitional or
  wording conflicts (both attributions are true); a default status.

## D-047 — Citations: locator, verbatim anchor, standing, chain and bytes read

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:** `source-policy.md` §4 and ER-6 leave standing and the attribution chain to
  S06. MA §5.2 has one `locator` for several `source_ids`, so it cannot say which source is
  at which place.
- **Decision** (`claim-model.md` §5):
  - Each citation has one source, one locator, a verbatim anchor and a standing.
  - A `reporter` citation also names its originator: the originator's class, and where the
    reporter names it.
  - The anchor is required. A figure without quotable text cannot be cited in v1.
  - The claim is judged against the whole sentence at the locator, not only the anchor.
  - A verified citation records the time and hash of the bytes the Verifier read.
- **Rejected:** MA §5.2's `source_ids` plus one `locator`; standing on the source (D-035);
  optional anchors.

## D-048 — What `verified` means; staging, canonical and the human's review (H-1, H-2)

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:**
  - D-015's second part defines `verified` "until S06's claim model confirms or replaces
    it" (D-036).
  - CLAUDE.md §9 makes real claims class C: the human reviews them before they are
    canonical.
  - Before S06 started, the human chose a staging seed of 5 to 10 real claims (H-1:
    "Seed 5–10 in staging (Consigliato)") and one JSON array file per record kind (H-2:
    "Un file JSON per tipo (Consigliato)").
- **Decision** (`claim-model.md` §6–§7):
  - **`verified` is confirmed and extended.**
    - For a claim that cites sources: the Verifier re-read each source at its locator,
      found the anchor, and judged whether the statement exceeds the sentence.
    - For a claim with inputs: the inputs are allowed and the stated step follows.
    - It is recorded by a status other than `unverified`, a per-record `verified_on`, and
      per-citation bytes read.
    - It is not human review and not canonical status.
  - **Staging and canonical.** Unreviewed claims live in `data/staging/claims.json`.
    Canonical claims live in `data/claims.json`, created with the first accepted claim.
    Every claim carries `review`: `not_reviewed`, or the human's verdict with date and
    report. VD-8 ties the file to the verdict.
  - **Seed claims.** Ten real claims (as measured at this commit) cover all five types.
    They are verified, all `not_reviewed`, and none is canonical.
- **Consequence:** at the human's review, D-015's status line records that its second part
  is superseded by this decision.
- **Rejected:** a `verified` field (a third home beside the status and date); one claims
  file with a staging flag (a consumer could read an unreviewed claim as canonical); an
  agent-written verdict.

## D-049 — The `not_publicly_determinable` search record

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:** ER-3 requires the search to be recorded. D-031 and D-025 require a
  `not_publicly_determinable` state to cite claims.
- **Decision** (`claim-model.md` §8):
  - The search is a `search` block on a `DERIVATION` claim: question, date, each class with
    the sources consulted or the access gap, and a conclusion (`not_publicly_determinable`
    or `not_researched`).
  - A `not_publicly_determinable` conclusion cannot include an inaccessible class.
  - Whether every preferred class of the row was searched is checked on the citing record
    (S10).
  - **Applied by hand to HBM-06:**
    - Samsung's technical documentation was refused.
    - No memory maker's documentation or filing was read.
    - NVIDIA's filing speaks at company level only.
    - So the H100's HBM supplier is `not_researched`, not `not_publicly_determinable`.
    - The domain map is not edited.
- **Rejected:** a separate search-record kind or claim type (machinery for one block);
  leaving the shape to S10 (the accepted state would have nothing valid to cite).

## D-050 — The source record; the register migrated and frozen

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:**
  - `source-policy.md` §16 lists the source fields.
  - D-041 moves each source's class to the source record at migration.
  - The register says it is frozen after S06.
- **Decision** (`claim-model.md` §9; shape in `schemas/sources.schema.json`, class vocabulary
  unchanged):
  - **IDs** are `src-NNN`, keeping S01's numbers: `SRC-006` is `src-006`. S05-R1 is
    `src-024`. `migrated_from` keeps each old label resolvable.
  - **Fields:** class, publisher text, `publisher_entity`, authors, URL, stated dates by
    kind (or `undated`), retrieval (method, access time, hash), and `filing_copy` for
    filings.
  - **`publisher_entity`** is `not_researched` for company publishers until S07, and
    `not_applicable` otherwise.
  - **The migration is a deterministic function in the tests.** VD-9 re-runs it against
    the register and `source-policy.md` §8.1 and §8.3.
    - One override is applied: SRC-005's publisher, per §2 and §8.1.
    - `source_type`, `source_tier` and `locators_used` are not migrated.
  - **After the migration:**
    - the register's status line says it is frozen;
    - §8.1 is marked as history;
    - the tests read classes from `data/sources.json`.
- **Rejected:** MA's `source-001` (breaks the link to older documents); keeping `SRC-001`
  (breaks the lower-case ID convention); company IDs chosen now (S07's); migrating the
  "Retrieved but not cited" and "Not retrievable" rows (not sources).

## D-051 — validate-data as CI tests; no validate-freshness code yet (H-4)

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:**
  - MA §15 asks for a documented `validate-data`.
  - D-026 keeps `tools/` standard library.
  - Before S06 started, the human chose tests in CI (H-4: "Test in CI (Consigliato)").
- **Decision** (`claim-model.md` §10–§11):
  - `validate-data` is `tests/test_data_schema.py` (VD-2, pinned `jsonschema`) and
    `tests/test_data_integrity.py` (VD-1, VD-3 to VD-13, standard library). CI runs them
    in the existing unit-test step.
  - V-1 to V-9 wait for entity and relationship records. V-10 is defined and waits for the
    first record.
  - No `validate-freshness` code: its rules need matrix rows from records. The dates it
    needs are required fields now.
- **Rejected:** `tools/validate_data.py` importing `jsonschema` (amends D-026); a
  standard-library command without schema checks; running V-rules on fixtures only.

## D-052 — Agent roles and contracts (H-3; D-010)

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:**
  - D-010 assigns `docs/agents/roles.md` and `docs/agents/contracts.md` to S06, in the MA
    §12 format.
  - Before S06 started, the human chose full contracts for the roles active through S10
    (H-3: "Pipeline fino a S10 (Consigliato)").
- **Decision:**
  - `roles.md` lists every CLAUDE.md §8 role, and names the session that first
    activates each inactive one.
  - `contracts.md` gives MA §12 contracts to Source Scout, Extractor, Verifier, Knowledge
    Architect and Data Auditor. Each validation gate is a test CI runs (L-02).
  - No role may write `data/claims.json` or a review verdict.
  - Contracts are documents; there is no runtime (NG-08, L-01).
- **Rejected:** full contracts for every role now (the inactive ones would describe work no
  session does yet); deferring (it would amend D-010).

## D-053 — The trace command

- **Session:** S06 · **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human review of S06: "Approve all")
- **Context:** the S06 gate: "The system can answer: 'What exactly supports this
  relationship?'" No relationship record exists before S10.
- **Decision** (`claim-model.md` §12):
  - `tools/trace.py`, standard library, prints record → claims → citations → sources, and
    claim → inputs, recursively. For a source, it lists the claims that cite it.
  - It exits 1 when a reference does not resolve.
  - It is tested on the fictional relationship fixtures and on every seed claim.
  - The gate is **met for review**: the path from a relationship to its sources works on
    fixtures, and the path from claims to real sources works on the seed claims.
  - What it cannot show is listed in `claim-model.md` §12.
- **Rejected:** a graph or database layer (NG-07); declaring the gate met without a real
  relationship (it is the human's call, with S10).

## D-054 — The company seed and the legal-entity rulings (H-1)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** the roadmap's S07 target is "A small, high-quality seed set rather than
  maximum coverage". Before S07 started, the human chose eight companies, one per chain
  layer (H-1: "8, one per layer (Recommended)"). `entity-taxonomy.md` §3.1 makes a record
  "one record per legal entity as sources name it".
- **Decision** (`company-dataset.md` §1–§2):
  - The seed is NVIDIA, SK hynix, Micron, Amkor, TSMC, ASML, Synopsys and Amazon.
  - Each record is the legal entity that the company's own filing names as registrant or
    filer: e.g. AMAZON.COM, INC., not Amazon Web Services; ASML Holding N.V., not an
    operating subsidiary.
  - Brands and channels ("AWS", "SK hynix Newsroom", "NVIDIA Technical Blog") are names or
    aliases, never records.
  - Parent and subsidiary questions stay open for S10's `owns`.
- **Rejected:** the minimal five and the broader twelve (H-1); a record per brand or segment
  (R-3, `entity-taxonomy.md` §3.1).

## D-055 — Entity data layout: one file per entity type (H-2)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** D-005 leaves each data layout to the session that first needs it. Before S07
  started, the human chose one JSON array file per entity type (H-2: "One file per entity
  type (Recommended)").
- **Decision:** `data/companies.json` and `data/jurisdictions.json` hold canonical records.
  `data/staging/companies.json` and `data/staging/jurisdictions.json` hold staging records.
  Each joins `validate-data` in this session (L-05), and `tools/trace.py` reads them by
  default.
- **Rejected:** one `data/entities.json` for every type (H-2); a staging flag inside one file
  (the D-048 reason: a consumer could read a staging record as canonical).

## D-056 — Company ID rule (ID-1)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** the S07 gate requires "stable IDs". A renamed company keeps its ID
  (`entity-taxonomy.md` §3.1). The display name is editorial (§7).
- **Decision** (`company-dataset.md` §3):
  - A company ID is `company-` plus the slug of a Latin-script legal name, as first
    recorded: drop one trailing legal-form designation from the §3 table, lower-case,
    reduce to ASCII, and join words with `-`.
  - A rename keeps the old legal name as an assertion with `valid_to`, so the ID still
    checks.
  - Collisions add the incorporation code. A further collision needs a decision.
  - `tests/test_data_entities.py` (ID-1) checks it on every record.
- **Rejected:** IDs from the display name or a ticker (they change for reasons other than
  identity); hand-chosen short IDs (no check possible).

## D-057 — Claim patterns for company identity and attributes

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** `claim-model.md` §16 and the S06 report hand S07 the claim shape. The rows are
  `identity:company` and `attr:company.*` (`source-policy.md` §7). R-5 forbids reading a
  headquarters off a facility or a listing, and D-024 forbids deriving roles from edges.
- **Decision** (`company-dataset.md` §4):
  - One `FACT` with `party` standing, quoting the filer's own name statement, serves
    `identity_claim_ids` and `legal_name` (D-044). The legal name is recorded verbatim,
    capitals included.
  - Cover-page anchors are the value followed by its printed label, in text order. The
    locator says which value is which.
  - `incorporated_in` and `headquartered_in` are `FACT` when the sentence names the country,
    and a `DERIVATION` when it names a subdivision. The derivation's second input is the ISO
    3166-2 claim (D-058).
  - `headquartered_in` needs a sentence with "headquarters" or "head office". A cover address
    alone is not used.
  - A role needs a sentence that states the business model of the role's schema definition.
    Superlatives (ER-5) and plans (ER-8) are not adopted.
  - Korean anchors are verbatim. The statement is the Atlas's translation and says so.
  - A field with no such sentence in the sections read is `not_researched`.
- **Rejected:** a `FACT` that a Delaware company is incorporated in the United States (the
  filing does not say it); the cover address as the headquarters; inferring incorporation
  from a legal form.

## D-058 — Jurisdiction records from ISO pages retrieved by the human (H-4, RA-4)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** H-4 ("Create the needed ones (Recommended)") required ISO 3166-1 as ISO
  publishes it, and said to stop and ask if it could not be retrieved under RA-1/RA-2.
  `www.iso.org` refused plain requests (HTTP 403 challenge) on 2026-10-01, so S07 stopped and
  asked. The human chose manual retrieval ("RA-4: you save ISO pages (Recommended)").
- **Decision** (`company-dataset.md` §5):
  - The human captures the ISO Online Browsing Platform entries for US, NL, KR and TW. Each
    capture is a source record with `standard_specification` class and method
    `manual_by_human`, and the file stays outside the repository. The human supplied
    screenshots ("Can i send you the screens?"); each shows the `iso.org` host and the OBP
    header, and the Verifier reads its anchors off the image.
  - Each jurisdiction record's identity claim is a `FACT`, standing `originator`, whose
    anchor carries the alpha-2 code (J-1).
  - ISO 3166-2 subdivision entries on the same pages are `FACT`s used as inputs to the
    state-to-country derivations (D-057).
  - Display names are editorial, and ISO's short names are aliases, as ISO gives them.
- **Rejected:** a secondary code list (RA-5); no jurisdiction records in S07 (H-4's
  alternative, not chosen).

## D-059 — Regulator-hosted filings readable under RA-1 (SK hynix)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** D-042 takes filings from the filer's own copy, because EDGAR refused plain
  requests and its access policy could not be read. SK hynix's IR site hosts no annual
  report and points readers to the regulator's English DART for disclosures. DART answered
  plain HTTPS requests. The human chose the DART copy ("DART regulator copy (Recommended)").
- **Decision:**
  - D-042's filer-copy rule answers EDGAR's refusal. It does not forbid a regulator's copy
    that answers an ordinary request.
  - A filing read from a regulator's own system under RA-1 is recorded with
    `filing_copy: regulator_hosted`.
  - EDGAR stays an access gap, and no identity is declared to any site (D-042, RA-7).
- **Rejected:** SK hynix's newsroom pages as identity evidence (an acceptable class, but
  weaker, and `incorporated_in` has no acceptable alternative); leaving SK hynix out.

## D-060 — TSMC's 20-F by manual retrieval (RA-4)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** every TSMC host and EDGAR answered with a challenge or refusal on 2026-10-01.
  The human chose to download the 20-F ("RA-4: you download its 20-F (Recommended)").
- **Decision:** the human downloads TSMC's 2025 Form 20-F from `investor.tsmc.com` and
  supplies it. It is a source record with method `manual_by_human` and `filing_copy:
  filer_hosted_not_checked`. The Verifier reads the file the human supplies, and records its
  hash (RA-4(5)).
- **Rejected:** leaving TSMC open with a seven-company seed.

## D-061 — Staging and canonical for entity records; the human's review in S07 (H-3)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** the accepted entity schema has no review field, and Part B §08 forbids adding
  one without approval. Before S07 started, the human chose to review inside S07 (H-3: "Your
  review inside S07 (Recommended)").
- **Decision** (`company-dataset.md` §6):
  - A record's file says whether it is staging or canonical (D-055).
  - CE-1: a canonical record cites only canonical claims and canonical jurisdictions, and no
    ID is in both files.
  - Accepted claims move to `data/claims.json` with the human's verdict. A record moves only
    when every claim it cites is accepted.
  - The S06 seed claims move only on their own verdicts.
- **Rejected:** a review field on entity records (a schema change); promotion after the
  session (H-3's alternative).

## D-062 — Anchors from new retrievals are Verifier-attested (H-6)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** VD-11 machine-checks only anchors whose text is in the repository
  (`claim-model.md` §5, §16). Before S07 started, the human chose Verifier attestation with
  a human sample (H-6: "Verifier + your sample (Recommended)").
- **Decision** (`company-dataset.md` §7):
  - A citation read on or after the date in `company-dataset.md` §7 is attested. The
    Verifier found the anchor verbatim in text extracted from those bytes and read the
    sentence. VD-11 requires the bytes read to be the registered bytes, hashed in full.
  - Reads before that date stay machine-checked against their home.
  - The human spot-checks a sample, recorded in the report.
- **Rejected:** committing full texts so that anchors can be machine-checked (RA-4(4));
  a list of attested claim IDs (a second home for the read time); the human checking every
  anchor (H-6's alternative).

## D-063 — validate-data for entity records

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** `relationship-taxonomy.md` §15 and `claim-model.md` §11 hand V-1, V-9 and
  V-10 to S07. `entity-taxonomy.md` §9 asks for jurisdiction IDs on the ISO list.
- **Decision** (`company-dataset.md` §8): `tests/test_data_entities.py` adds V-1, V-4, V-9,
  V-10, CE-1, ID-1 and J-1. VD-2 and VD-11 are extended. Each check runs on the real files
  and on a fictional fixture world, where one planted fault per check must be caught. V-10
  reads the matrix from `source-policy.md` §7 on every run. V-2, V-3 and V-5 to V-8 wait
  for relationships (S10).
- **Rejected:** a `tools/validate_data.py` (D-051); running V-rules on fixtures only
  (D-051).

## D-064 — validate-freshness: the first rule (F-1)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** D-040 sets a 12-month horizon for `time_sensitive` rows, "before its use in a
  canonical record". D-051 left the code to the first session with such records.
- **Decision** (`company-dataset.md` §9): `tests/test_freshness.py` checks that every
  `time_sensitive` field rests on at least one accepted citation whose evidence date is
  within the horizon of the claim's `verified_on`. The horizon is read from
  `source-policy.md` §12. Re-checking means newer evidence. Scheduled re-checks as filings
  age stay with the Change Detector, which is inactive.
- **Rejected:** comparing with the date the test runs (a commit's result would change with
  the calendar); counting a re-read of an old filing as fresh.

## D-065 — `publisher_entity` is set for filings only

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** D-050 left `publisher_entity` `not_researched` for company publishers until
  S07. The S07 prompt (§06 q11) allows it only where the evidence shows the legal entity.
- **Decision** (`company-dataset.md` §10): a filing's `publisher_entity` names its filer's
  canonical company record. Web pages stay `not_researched`, because they name a channel or
  brand, not a legal entity. V-1 checks that the reference names a canonical company.
- **Rejected:** setting it from copyright lines (a rights holder is not shown to be the
  publisher); setting it for a staging company (V-1).

## D-066 — The M1 milestone audit is written first in S07 (H-5)

- **Session:** S07 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human review of S07: "Approve all (Recommended)")
- **Context:** PEF §4 requires a milestone audit "At every major milestone". M1 (S03–S06)
  closed with S06, and no session was assigned the audit. Before S07 started, the human
  placed it as S07's first task (H-5: "First task of S07 (Recommended)").
- **Decision:** `docs/architecture/milestone-audits/M1-audit.md`, a document only, with a row
  in `docs/quality/audit-history.md`. Claude writes it in the Portfolio Reviewer role, which
  `docs/agents/roles.md` marks inactive and gives no contract. This is recorded as a
  deviation from `roles.md`, not a change to it.
- **Rejected:** deferring the audit to S12 (H-5's alternative); activating the Portfolio
  Reviewer role with a contract for one document (D-052's reason: a contract for work no
  session does regularly yet).

## D-067 — Concept scope: 15 of 17 concepts recorded; HBM-03 and HBM-04 are gaps (H-1)

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** H-1 ("All v1 concepts (Recommended)"): every concept that `entity-taxonomy.md`
  §5 maps to a technology or component, unless no definitional source of a sufficient class
  exists. The only sentences on the HBM base die and on TSVs as such come from vendors'
  marketing pages. JEDEC JESD238 was requested under RA-4 and had not arrived.
- **Decision** (`concept-dataset.md` §1, §3): 16 records for 15 concepts. HBM-03 and HBM-04
  are gaps, listed in the concept table with no record; CI-1 fails if a record appears for a
  gap without the table changing.
- **Rejected:** defining the base die or TSV from Micron's or SK hynix's pages (marketing
  never defines a class); a stub record with a `not_researched` definition (a record with no
  definitional evidence would still be an endpoint S10 could use).

## D-068 — Technology and component IDs (CI-1)

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** S07's ID rule slugs a claim-backed legal name. A concept's name is editorial
  (Part B §06 q4).
- **Decision** (`concept-dataset.md` §3): the ID is the record type plus the slug of the
  concept's name in `entity-taxonomy.md` §5, an accepted document; a split concept's terms
  use only words of that name and cite a decision. `tests/test_data_entities.py` (CI-1)
  checks the concept table against §5, the schema's `x-concepts` and the records.
- **Rejected:** the S01 concept ID (opaque); a defining standard's term (most concepts have
  none, and HIR says the "2.x" names have no technical basis); the display name (editorial).

## D-069 — Working definitions are always an INTERPRETATION (H-4; DEF-1, DEF-2)

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** H-4 ("Reuse TQ answers (Recommended)"): each working definition is an
  `INTERPRETATION` citing every side of its CON conflict. Part B §06 q3 asks what applies
  where no conflict exists.
- **Decision** (`concept-dataset.md` §4): every technology and component definition cites
  exactly one `INTERPRETATION`, whose inputs are the source positions (`ATTRIBUTION`) and,
  where the record narrows a broader one, that record's working definition. The identity
  claims are `ATTRIBUTION` claims among those inputs (DEF-1). No definition claim serves two
  records, and no concept is in two records unless the concept table lists it twice (DEF-2).
- **Rejected:** citing a single source's `ATTRIBUTION` directly where no conflict exists
  (two kinds of definition in one field).

## D-070 — SME-03 becomes two records: EUV lithography and DUV lithography

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, S09 final review of the open S08 rulings: "Approve both (Recommended)"); earlier: not approved at the S08 review, left open at H-0
- **Context:** §5 maps SME-03 "EUV and DUV lithography" to one technology record and leaves
  scanner equipment classes to S08. Part B §06 q2 names EUV vs DUV as a pair to keep apart.
- **Decision** (`concept-dataset.md` §2, §3): two technology records, both with
  `concept_refs` SME-03, each with its own working definition from NIST (wavelengths) and
  CSET (separate grades). No equipment class for scanners in v1.
- **Rejected:** one record (it would hold two distinct processes); scanner classes (no v1
  concept asks for them).
- **Review (2026-10-01):** not approved at the S08 review. The two records stay staging
  (they also rest on `src-041`, D-076).

## D-071 — `broader` assignments and acyclicity (B-1)

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** `entity-taxonomy.md` §3.3, §3.4 and §9: `broader` is taxonomy only, may have
  several parents, and must be acyclic.
- **Decision** (`concept-dataset.md` §5): data-centre GPU and AI ASIC under AI accelerator;
  assembly and packaging tools under SME; 2.5D packaging and 3D die stacking under advanced
  packaging. The multi-die package has no parent. V-1, CE-1 and B-1 check the references and
  the absence of cycles.
- **Rejected:** multi-die package under advanced packaging (not always high-density); a
  lithography parent (SME-02 has no record).

## D-072 — Products: three records, their IDs (PI-1) and the `instance_of` basis (IO-1) (H-2)

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** H-2 ("Few, from sources (Recommended)"): H100, Trainium2, Micron HBM, an ASML
  EUV system. `instance_of` has no claim field in the schema.
- **Decision** (`concept-dataset.md` §7): NVIDIA H100, AWS Trainium2 and Micron HBM4 36GB
  12H. No ASML product: its page names only families. A product ID is `product-`, the
  vendor's ID without `company-`, and the slug of the anchored product name (PI-1). Each
  `instance_of` value has a basis row naming its claim (IO-1).
- **Rejected:** an ASML system from the families page; a schema field for the basis (a
  schema change the human has not approved).

## D-073 — The GH100 ruling

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** the canonical claim `claim-h100-gh100-process-name` is about the GH100 die
  that powers the H100 (S06 finding). Part B §06 q6 asks whether it supports the H100's
  `vendor_process_name`.
- **Decision** (`concept-dataset.md` §7): it does not. The re-retrieved page has a sentence
  about the H100 itself ("Using the TSMC 4N fabrication process enables H100…"), and the
  value "TSMC 4N" rests on that new claim. The GH100 claim stays about the die; its anchor
  was re-checked in the new bytes and is still at its locator.
- **Rejected:** reusing the GH100 claim (ER-9's logic: a statement about one thing does not
  support another); `not_researched` (a sentence about the H100 was found).

## D-074 — Trainium2's vendor is `company-amazon-com`

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human ruling at the S08 review: "Trainium2 vendor = Amazon")
- **Context:** Part B §16 makes an unclear vendor legal entity a stop condition. AWS's page
  says Trainium2 is "from AWS". The canonical record `company-amazon-com` carries "AWS" and
  "Amazon Web Services" as aliases, accepted at the S07 review (the 10-K names AWS as a
  segment).
- **Decision** (`concept-dataset.md` §7): the vendor is `company-amazon-com`; the record
  stays staging until the human rules on this question. Which legal entity publishes the
  page stays open for S10. The human approved the ruling at the S08 review, together with
  reading Trainium2 as an AI ASIC (`claim-atlas-trainium2-ai-asic`).
- **Rejected:** a new AWS company record (no filing of a separate AWS legal entity has been
  read); leaving Trainium2 out (H-2 names it).

## D-075 — A re-retrieval with changed bytes is a new source record

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** VD-11 (D-062) requires an attested read to be of the registered bytes.
  `src-006`, `src-010`, `src-013` and `src-015` returned changed bytes; their existing
  records are the home of S06 reads.
- **Decision** (`concept-dataset.md` §6): each changed retrieval S08 cites is a new record
  (`src-042` to `src-045`), with the same URL, a title marked with the retrieval date and the
  earlier record's ID, and its own full hash. The old record stays unchanged.
- **Rejected:** rewriting the old record's hash (it would orphan the S06 reads, VD-12); a
  schema field linking the two records (a schema change).

## D-076 — Class rulings for the new sources

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, S09 final review of the open S08 rulings: "Approve both (Recommended)"); earlier: not approved at the S08 review, left open at H-0
- **Context:** `source-policy.md` §2 assigns each source one class.
- **Decision** (`concept-dataset.md` §6): the IEEE EPS Heterogeneous Integration Roadmap
  chapter (`src-039`) is a `research_report`, and the NIST news article (`src-041`) is a
  `government_publication`. The ECP milestone report (`src-040`), a national-laboratory
  report, is a `research_report` as the LBNL reports `src-021` and `src-022` already are;
  that follows precedent and is not a ruling.
- **Review (2026-10-01):** the human did not approve the two rulings at the S08 review.
  They stay proposed, and the claims citing `src-039` and `src-041`, with the working
  definitions and records resting on them, stay staging.
- **Rejected:** `standard_specification` for the roadmap (no standards body adopted it);
  `news_media` for the NIST article (the agency is its originator, writing about its own
  work).

## D-077 — Layout, review and validate-data for concept and product records (H-3, H-6)

- **Session:** S08 · **Date:** 2026-10-01 · **Status:** accepted (2026-10-02, human review of S08: "All except D-070, D-076 (Recommended)")
- **Context:** H-3 ("One file per type (Recommended)") and H-6 ("Review inside S08
  (Recommended)").
- **Decision** (`concept-dataset.md` §8, §9): `data/technologies.json`,
  `data/components.json` and `data/products.json`, each with a staging copy; promotion as
  D-061, on the human's verdicts. `tests/test_data_entities.py` extends V-1, CE-1, V-9, V-4
  and V-10 to the new kinds and adds CI-1, DEF-1, DEF-2, B-1, PI-1 and IO-1, with fixtures and
  planted faults. `tools/trace.py` reads the new files and prints `vendor`, `instance_of` and
  `broader`.
- **Rejected:** one combined concepts file (H-3's alternative); a `tools/validate_data.py`
  (D-051).

## D-078 — Facility scope: filing-named sites; plans as events; ASML a gap (H-1)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)")
- **Context:** H-1 ("Filings' fabs + packaging (Recommended)"). The registered filings were
  re-retrieved (H-4). At the start of S09 the human answered the ASML stop condition with
  "Gap + proposal (Recommended)" and agreed to re-supply TSMC's 20-F ("I'll re-supply it
  (Recommended)").
- **Decision** (`facility-dataset.md` §1): a facility record needs a sentence, from a source
  its rows accept, that names one site, places it, and gives its kind. Records: Micron's fab
  in Manassas, Virginia and SK hynix's M16. TSMC's sites are a gap: its 20-F was not
  re-supplied during S09, and the human chose "Close as a gap (Recommended)". Sites known
  only from plans (Micron Boise and Clay, SK hynix M15X, Amkor Arizona) are events (ER-8). No
  site sentence (Micron's and Amkor's country tables), no jurisdiction record (Japan), or
  no kind evidence (SK hynix Cheongju) means no record. No data centre is named.
- **Rejected:** Micron or Amkor country rows as sites; facility records for sites under
  construction; ASML sites forced into an existing kind.

## D-079 — Facility ID rule (FI-1)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)")
- **Context:** `entity-taxonomy.md` §3.2: one site at one location; the ID survives a change
  of owner or operator.
- **Decision** (`facility-dataset.md` §2): `facility-`, the alpha-2 code of the one
  `located_in` value, and the slug of the term: the site's own name in an identity anchor,
  or, for an unnamed site, its locality as the anchor gives it. The facility table holds
  the terms; FI-1 recomputes each ID and finds the term in an identity anchor. A collision
  needs a decision.
- **Rejected:** an owner prefix (wrong after a sale); the display name (editorial); a
  record for a group of plants named only by town.

## D-080 — Facility location rests on site sentences only (HQ-1)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)"); its flagged ruling (clause-only anchors that leave out a head-office clause or phrase) approved at the S09 review (2026-10-02: "pick your recommendations"; Claude's recommendation was to approve)
- **Context:** R-5; `source-policy.md` §7 rows `attr:facility.located_in`, `.locality`.
- **Decision** (`facility-dataset.md` §3): `located_in` and `locality` rest on a sentence
  placing the site; a subdivision reaches the country by the D-057 `DERIVATION`; `locality`
  is in the source's script. HQ-1 fails a location that reaches a claim serving a company's
  headquarters or incorporation (ISO claims aside), or an anchor carrying an excluded word
  of §3's table.
- **Rejected:** M16's location from SK hynix's release phrase "at headquarter located in
  Icheon"; the head-office address as the bridge from 이천 to 경기도.

## D-081 — Facility kinds rest on basis rows and listed words (FK-1)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)"); its flagged ruling ("fab"
  and "fabrication plant" read as `wafer_fab`) approved at the S09 review (2026-10-02: "pick
  your recommendations"; Claude's recommendation was to approve)
- **Context:** `facility_kinds` has no claim field; IO-1 (`concept-dataset.md` §7) is the
  precedent for a basis table.
- **Decision** (`facility-dataset.md` §4): each kind of each record has a basis row naming an
  identity claim and a word in its anchor; the word must be one §4 lists for the kind.
- **Rejected:** a kind read from the company's role (R-3); a kind without a named word.

## D-082 — Ownership, operation and production evidence for S10 (H-3)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)")
- **Context:** H-3 ("Claims now, edges in S10 (Recommended)"); `relationship-taxonomy.md`
  §4.3, §4.4, §5.
- **Decision** (`facility-dataset.md` §5): the candidate sentences are staging claims, each
  marked against §5. Micron's "our fab" fails both `owns` and `operates`. SK hynix's
  "생산공장을 설치ㆍ가동" partly meets `operates` (the site is named by its town), as a
  `DERIVATION` with the M16 row; it fails `owns`. No edge is created. No v1 type holds
  site-level production; nothing is proposed.
- **Rejected:** "our" read as controlling ownership; an operator inferred from the filer.

## D-083 — The event schema (H-2)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 review: "Approve
  both (Recommended)"; its two flagged rulings, 준공 recorded as `opened` and the company as the
  subject of a planned site's announcement, approved: "pick your recommendations")
- **Context:** D-022 assigns the event schema to S09; MA §5.5, §5.6; ER-8.
- **Decision** (`schemas/events.schema.json`; `facility-dataset.md` §6): fields `id`,
  `event_type`, `subject`, `date`, `claim_ids`. Types `announced`, `opened`, `expanded`,
  `closed`. Occurrences have a facility subject and rest on a `FACT` or `DERIVATION`; an
  announcement rests on `ATTRIBUTION` claims and its subject is the facility, or, for a
  planned site, the announcing company. No event is dated after a source stating it (EV-3).
  ID rule EI-1. Files `data/events.json` and `data/staging/events.json` (H-5).
- **Rejected:** a status or planned-date field; an `announces` field; a facility record for
  a plan; events as edge endpoints; a `construction_started` type.

## D-084 — Event rows in the preference matrix

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (adding rows approved at the
  start of S09: "Add the rows (Recommended)"; the rows' content at the S09 review, 2026-10-02:
  "Approve both (Recommended)")
- **Context:** `source-policy.md` §7 and §16 left event rows to S09; the S09 prompt did not
  list the policy as modifiable, so the human was asked first.
- **Decision:** one row per event type (`event:announced`, `event:opened`,
  `event:expanded`, `event:closed`). Announcements: press releases and filings preferred,
  government publications acceptable, standing `party`. Occurrences: filings and government
  publications preferred, press releases acceptable, standing `party or originator`. All
  `stable`. `tests/test_source_policy.py` reads the rows from the event schema; EV-4 applies
  them.
- **Rejected:** marketing pages as evidence of an event (undated); waiting for a later session.

## D-085 — Facility status is derived by a tested function

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)")
- **Context:** MA §5.6; R-8; Part B §06 q5.
- **Decision** (`facility-dataset.md` §7): `tools/facility_status.py` derives `opened`,
  `closed`, `not_yet_opened`, `indeterminate` or `no_recorded_opening` on a date from the
  occurrence events, reading partial dates as periods. Plans and expansions never move it.
  Tested by `tests/test_facility_status.py` (ST-1). The tool is a Data Auditor write
  (`docs/agents/contracts.md`).
- **Rejected:** a stored status; "operating" as a state (an `opened` event says completed or
  began operating on a date, not today).

## D-086 — Capacity and data centres (CAP-1)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)")
- **Context:** TQ-10; the schema's `nameplate_it_capacity_mw`.
- **Decision** (`facility-dataset.md` §8): `not_applicable` on any site that is not a data
  centre; on a data centre, a value needs an anchor carrying a §8 marker. No data-centre
  record in S09.
- **Rejected:** a power or interconnection figure as capacity.

## D-087 — Layout, review and validate-data for facilities and events (H-5, H-6)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)")
- **Context:** H-5 ("One file per kind (Recommended)"), H-6 ("Review inside S09
  (Recommended)").
- **Decision** (`facility-dataset.md` §9 to §11): `data/facilities.json` and
  `data/events.json` with staging copies; promotion as D-061 on the human's verdicts.
  Checks FI-1, HQ-1, FK-1, CAP-1 in `tests/test_data_entities.py`; EV-1 to EV-4 and EI-1 in
  `tests/test_data_events.py`; VD-2 for events; ST-1. Each English DART section is its own
  source record (`src-046` to `src-048`), as `src-030` is.
- **Rejected:** one combined file; a separate validator script (D-051).

## D-088 — Proposal: a facility kind for equipment manufacturing (not applied)

- **Session:** S09 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S09 final review: "Approve all (Recommended)"): the gap stands and the proposal goes to a later session; no schema
  is changed (at the start of S09 the human chose "Gap + proposal (Recommended)")
- **Context:** ASML's manufacturing sites (`claim-asml-manufacturing-sites`) assemble and
  test lithography systems; `vocab_facility_kind` has no fitting value.
- **Proposal:** a later session adds a kind for sites that manufacture semiconductor
  manufacturing equipment (the `production_equipment` use class), with its definition and
  words for FK-1, by an approved schema change. Until then ASML's sites have no record.
- **Rejected for S09:** any schema change (Part B §08).

## D-089 — Edge scope: five edges, and the candidates that fail §5 (H-1)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)")
- **Context:** H-1 ("I agree", 2026-10-02, to product and company edges first, then `operates`
  for M16, then class edges; about 10–12 edges). The registered filings and product pages were
  re-read (H-4, D-075).
- **Decision** (`edge-dataset.md` §1): an edge needs claims meeting `relationship-taxonomy.md` §5
  for its type, as `FACT` or as a `DERIVATION` covered by ER-1 or an approved ruling, endpoints
  that are records, and the §10 checks. Five edges: H100 and Trainium2 `incorporates` HBM; Amazon
  `designs` Trainium2; SK hynix `operates` M16 (D-099); HBM `requires` 3D die stacking (D-091).
  Every `supplies` candidate from the filings fails (an item with no record, ER-9; a
  manufacturing service; co-mention), NVIDIA `designs` H100 fails ER-2, and `owns` waits on
  company records (D-095).
- **Rejected:** widening an `item` to a record that exists ("memory" as HBM); creating component
  records for items; recording a candidate that fails §5 to reach the expected count.

## D-090 — Edge ID rule (RI-1)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)")
- **Context:** Part B §06 q2: a stable, non-editorial rule from the type and endpoints, with
  `item` where the type has one, machine-checked as FI-1 and EI-1 are.
- **Decision** (`edge-dataset.md` §2): `rel-<source_entity>-<type, _ as ->-<target_entity>`, and
  `-<item>` for `supplies`. Entity IDs keep their type prefixes. A second record for the same
  relation (another period, V-5) would collide and needs a decision.
- **Rejected:** IDs without type prefixes (a technology and a component with one slug would
  collide); a counter (not recomputable); a claim or display name in the ID.

## D-091 — A class edge read out of a definition (the human's ruling)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)"; the edge approved as a
  flagged ruling: "E5: HBM requires 3D die stacking (D-091)"); the ruling itself was given at the start of S10 (2026-10-02, a §16 stop condition: "Allow, as DERIVATION (Recommended)")
- **Context:** `requires` needs necessity stated for the class (§5). The ECP report defines HBM
  as vertically stacked DRAM dies directly connected by TSVs; no source states "HBM requires 3D
  die stacking" in words, and ER-1 does not cover the step.
- **Decision:** HBM `requires` 3D die stacking rests on `claim-hbm-requires-3d-die-stacking`, a
  `DERIVATION` from the ECP definition and the two working definitions. RV-1's `requires` row
  carries "stacks" for this case. It is flagged on the review sheet.
- **Rejected:** no class edge (the human's alternative); HBM `requires` TSV (TSV is a gap,
  `concept-dataset.md` §1).

## D-092 — TSMC → H100 `fabricates` is a gap until fresh evidence (the human's ruling)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)"); the ruling was given at the
  start of S10 (2026-10-02: "Gap until fresh evidence (Recommended)")
- **Context:** the edge meets §5 only as an ER-1 `DERIVATION` from "Using the TSMC 4N fabrication
  process enables H100" (`claim-h100-process-name`), whose source was last modified 2025-07-22.
  `rel:fabricates` is `time_sensitive`, so F-1 (extended to edges, D-096) fails. NVIDIA's live
  Hopper page names TSMC 4N for the architecture, not the product.
- **Decision:** no edge. The derivation `claim-tsmc-fabricates-h100` is staged for review; the
  edge waits for product-level evidence dated within the horizon.
- **Rejected:** the Hopper page as fresh input (architecture, not product: D-073 logic); waiving
  F-1 for edges.

## D-093 — "AWS-designed" gives a `designs` edge from `company-amazon-com` (the human's ruling)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)"); the ruling was given at the
  start of S10 (2026-10-02: "company-amazon-com, as D-074 (Recommended)")
- **Context:** Amazon's release (`src-052`) names "Amazon Web Services, Inc. (AWS), an
  Amazon.com, Inc. company" announcing "two AWS-designed chip families—AWS Graviton4 and AWS
  Trainium2". There is no AWS company record; AWS is an accepted alias of `company-amazon-com`
  (D-074).
- **Decision:** the edge's source is `company-amazon-com`; the claim keeps the release's wording,
  including the AWS legal entity's name. The AWS legal-entity question stays open.
- **Rejected:** waiting for an AWS record (the human's alternative); Amazon's "our custom AI
  silicon" (not a statement of design work, ER-2).

## D-094 — Unknown HBM suppliers are `not_researched`

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)")
- **Context:** `incorporates` requires `supplier` (D-031); ER-3 and D-049 set when
  `not_publicly_determinable` may be claimed.
- **Decision** (`edge-dataset.md` §5): both `incorporates` edges carry `not_researched`; no
  preferred class was fully searched for either product. No search claim is created. V-10
  checks a `not_publicly_determinable` search against every preferred class of
  `rel:incorporates.supplier` (the S06 handoff, `claim-model.md` §8).
- **Rejected:** `not_publicly_determinable` from one page's silence; a supplier from NVIDIA's
  company-level list (ER-9).

## D-095 — No new company records in S10 (H-3)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)")
- **Context:** H-3 ("Only when an edge needs it (Recommended)").
- **Decision** (`edge-dataset.md` §6): none is created. A subsidiary named in a parent's filing
  cannot meet D-057 (the filer's own statement of its legal name), and no supplier has a
  `supplies` edge whose item is a record. `owns` edges wait.
- **Rejected:** a subsidiary record from Amkor's Exhibit 21.1; an AWS record from the release.

## D-096 — validate-data and validate-freshness for edges

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)")
- **Context:** `relationship-taxonomy.md` §15 (V-1 to V-9), D-033, L-05, L-09; Part B §06 q8.
- **Decision** (`edge-dataset.md` §7, §10): `tests/test_data_relationships.py` runs V-1 to V-6,
  V-9, V-10 (with the ER-3 search coverage), CE-1, RI-1 and four evidence guards (PL-1, EP-1,
  PE-1, RV-1, with RV-1's words in a table of the design document); V-7 and V-8 are warnings.
  VD-2 covers the relationship files; F-1 extends to edges on `time_sensitive` rows and to
  `supplier` assertions, not to explicit states. Each check is shown on fictional fixtures with
  a planted fault (`tests/fixtures/edge_records.json`).
- **Rejected:** a hand-written JSON Schema validator; V-7 and V-8 as failures (D-033); checks
  hard-coding the real edges.

## D-097 — Navigation from the JSON files (H-5)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)")
- **Context:** H-5 ("Re-retrieve + RA-4; nav tool (Recommended)"); the roadmap gate "Graph-like
  navigation is possible using relational data without introducing a graph database".
- **Decision** (`edge-dataset.md` §8): `tools/navigate.py`, standard library, answers
  `depends-on`, `suppliers`, `actors`, `edges` and `evidence` (through the trace), canonical by
  default, never printing "none" for a missing edge. Tested by `tests/test_navigate.py`. A Data
  Auditor write.
- **Rejected:** DuckDB now; extending `tools/trace.py` only; a stored adjacency list.

## D-098 — Layout, review and promotion for edges (H-2, H-6)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)")
- **Context:** H-2 and H-6 ("One file, review in S10 (Recommended)").
- **Decision** (`edge-dataset.md` §9): `data/relationships.json` and
  `data/staging/relationships.json`, the relation type as a field. Promotion as D-061, on the
  human's verdicts, when every cited claim, endpoint, item and supplier company is canonical.
  The Extractor's writes extend to the staging relationship file.
- **Rejected:** one file per relation type (H-2's alternative); promotion after the session.

## D-099 — SK hynix `operates` M16 as a `DERIVATION` (flagged for the review)

- **Session:** S10 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S10 review: "Approve all (Recommended)"; the edge approved as a flagged ruling: "E4: SK hynix operates M16 (D-099)")
- **Context:** D-082 left to S10 whether SK hynix's "생산공장을 설치ㆍ가동" (it operates its
  production plants in 경기도 이천시), with M16 listed as its plant in 이천, meets `operates`.
- **Decision:** the edge rests on `claim-sk-hynix-operates-m16`, a `DERIVATION` from those
  claims and the M16 release; it has no period. It is asked as a separate question at the
  review, and an unticked box leaves it in staging.
- **Rejected:** `valid_from: 2021-02` (construction, not operation); `owns` from 설치 (D-082).

## D-100 — The first journey: the HBM dependency chain (H-1)

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** H-1 ("yes and merge into main", 2026-10-02, to the recommended HBM chain). At the
  start of S11 the human ruled on two records the chain does not link: "Separate lane
  (Recommended)" for SK hynix's M16, and "Yes, not-connected lane (Recommended)" for Micron's
  HBM4 36GB 12H.
- **Decision** (`vertical-slice.md` §1): the journey answers "What does an AI accelerator's memory
  depend on, and who is known to make it?" over H100 and Trainium2 → HBM → 3D die stacking, with
  Amazon's `designs` edge, both `not_researched` suppliers and the TSMC → H100 gap. M16 and
  Micron's HBM4 are shown in a separate lane, "not linked to either accelerator".
- **Rejected:** a company profile (H-1's alternative); M16 drawn beside HBM (would imply supply);
  M16 only in the limitations (the human's alternative); Micron left off.

## D-101 — Structured output for the walk and the trace (H-4)

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** H-4 (Claude's recommendation, as part of H-1); the S10 debt "the navigation tool
  prints text only".
- **Decision** (`vertical-slice.md` §2): `tools/navigate.py` computes each answer as data
  (`depends_on_tree`, `supplier_rows`, `actors_list`, `edges_at`) and renders its text from it;
  `tools/trace.py` gains `trace_data`, the trace as a normalised structure (record, claim paths,
  claims, sources, missing references). Both print JSON with `--json`. The build imports the same
  functions. Tests check that the JSON and the text name the same edges, claims and sources.
- **Rejected:** the build walking the files itself (a second walk to keep in step); re-parsing the
  text output.

## D-102 — The build step and its stamp (H-2)

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** H-2 ("Static, stdlib build, inline SVG (Recommended)"). Part B §11 asks the page to
  state the data commit; the human ruled "Input digest (Recommended)".
- **Decision:** `tools/build_page.py` (standard library) writes one self-contained file,
  `site/hbm-chain/index.html`, with inline CSS and SVG and no script, from `data/`, the schemas,
  `edge-dataset.md` §1, `decisions.md` and `tools/page_template.html`. Output is deterministic
  (sorted inputs, no clock, no environment). The page carries a SHA-256 over its input files;
  `--check` rebuilds and compares bytes. The commit is recorded in the session report.
- **Rejected:** a page reading the JSON at run time and a charting library (H-2's alternatives); a
  commit stamp (a committed page cannot carry its own commit; CI's shallow clone); a separate
  stylesheet file (one self-contained file is what H-2 named).

## D-103 — The visual form and its encoding

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** MA §16.1 (the grammar: flows and dependencies → flow diagrams); Part B §06 q3.
- **Decision** (`vertical-slice.md` §3): a fixed vertical dependency diagram in inline SVG.
  Box fill and rule encode level (instance or class); the line style encodes the basis (solid:
  a `FACT` is cited; dashed and labelled "inferred": only `DERIVATION`s); amber hatched pills
  encode gaps. No visual channel encodes a magnitude, a confidence or time.
- **Rejected:** a table as the primary visual (kept as the text equivalent); a force-directed
  network (position would carry no meaning); colour alone for "inferred".

## D-104 — Gap encoding and the lane

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** RR-7; D-092, D-094; the human's lane rulings (D-100).
- **Decision** (`vertical-slice.md` §5): each `not_researched` supplier is a pill on its
  `incorporates` arrow; TSMC → H100 is a dotted line with no arrowhead and the pill "gap: no
  edge", opening the canonical `claim-tsmc-fabricates-h100`; "no recorded relationship" is
  written wherever a walk finds nothing. Four `edge-dataset.md` §1 rows are shown as text. The
  build refuses to render the lane if any edge or `supplier` assertion links a lane record to
  either accelerator.
- **Rejected:** omitting unknowns from the visual; a placeholder "unknown supplier" node (RR-7);
  the §1 "sentence" cells (not all are canonical claims).

## D-105 — The text provenance rule and validate-design for the page

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** Part B §02 (five things the page must make impossible), §07 task 6; MA §15
  (`validate-design`).
- **Decision** (`vertical-slice.md` §4, §8): every text node sits inside a record value
  (`data-ref`, `data-field`), an absent value, a fixed label, a derived value or a visibly marked
  framing block that names no record. `tests/test_page.py` (PG-1 to PG-10) is `validate-design`
  for this page; it runs in CI with every test module.
- **Rejected:** checking only that the page builds (would miss a hand edit); snapshot tests of
  the HTML (would freeze presentation, not provenance); hard-coded record values in tests.

## D-106 — Browser QA in a scratch environment (H-3)

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** H-3 ("Scratch Playwright, no repo dep (Recommended)").
- **Decision:** browser checks run with the pre-installed Chromium and Playwright outside the
  repository: desktop and 375 px screenshots, overflow, the keyboard path to every panel, console
  and network logs, measured contrast. The script and results are recorded in the report. Static
  accessibility checks run in CI (PG-8).
- **Rejected:** Playwright pinned and run in CI (H-3's alternative; a new dependency for one page).

## D-107 — Editorial and QA contracts (H-5)

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** H-5 ("Contracts in S11, proposed (Recommended)"); the human's ruling "Yes, both
  (Recommended)" on `tests/test_agent_contracts.py` and `tests/test_page.py`.
- **Decision:** `docs/agents/contracts.md` gains Editorial and QA contracts with MA §12's fields;
  `roles.md` marks both active. Editorial writes the framing and style in
  `tools/page_template.html` and the state rows of `README.md`, `docs/README.md` and
  `baseline.md`; QA writes browser findings and screenshots in `sessions/reports/`. Both are
  checked by `tests/test_page.py`. `tests/test_agent_contracts.py`'s expected active set gains the
  two roles.
- **Rejected:** leaving both inactive with the work under the Data Auditor (H-5's alternative).

## D-108 — Changes from the human's new-user test

- **Session:** S11 · **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, S12 opening review, H-0: "Rules binding, page unchanged (Recommended)")
- **Context:** the human's new-user test. Asked for suggestions ("Gimme suggestions"), Claude
  proposed seven changes; the human answered "I agree, follow the principle of “not
  overreachment”" (2026-10-02).
- **Decision** (`vertical-slice.md` §4 to §6): (1) the rule codes quoted from `edge-dataset.md` §1
  (ER-, RR-, F-, D-) are listed under "Rules cited above", each with its one-line home (the bold
  rule of its table row, the **Rule** paragraph of the section titled with it, or the decision
  title); section marks get one framing sentence, not a guessed definition; (2) a drawn gap says
  "a claim the Atlas holds, not an edge", in the legend, the words and the gaps list; (3) the short
  answer opens with one sentence composed from the records, omitted when the products do not share
  one relation type and one supplier state; (4) a record panel puts the claims of
  `legal_name`, `incorporated_in`, `headquartered_in`, `located_in` and `locality` in a closed
  disclosure; (5) a claim card leads with its type, status and statement, and a citation with its
  anchor; the claim ID, verification and review follow; (6) "supplier (who makes this part)"
  replaces "maker of this part", and "recorded as a kind of … a property of its record, not a
  supply link" replaces "instance of … an entity field, not an edge" in the lane; (7) a "Jump to"
  bar under the title. The build reads three more documents (the rule homes), so they join its
  inputs. PG-10 checks that every quoted rule code is listed.
- **Not done** (the human's "not overreachment"): no plain-language rewrite of the design record's
  reasons (they stay quoted verbatim); no definition for a bare section mark; no further cut of the
  evidence panels (each mark still opens its full evidence in one click).
- **Rejected:** rewriting the "why not" cells in plain words (a second home for the reasons);
  collapsing claim cards (the evidence would sit two clicks from its mark).

## D-109 — The refused candidates become records (H-1, H-2)

- **Session:** S12 · **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02, at the S13 opening)
- **Context:** H-1 ("Pick the recommended", end of S11: records); the S12 audit's blocking finding
  B-1 (`milestone-audits/M2-audit.md` Part 2 N-2, I-5; Part 3 q1). The human's answer at S12, to
  "Where should the 12 relationships the Atlas considered and refused … be stored": "Own file,
  separate from real links (Recommended)".
- **Decision** (M2 audit, Part 3 q1 and q6): one record per `edge-dataset.md` §1 candidate row, in
  `data/refused_candidates.json` and `data/staging/refused_candidates.json`, against
  `schemas/refused_candidates.schema.json`. A record holds `id` (`cand-NNN` in row order, never
  reused), `relation_types`, `source_entities` and `target_entities` (entity IDs, or
  `{"state": "no_record", "name"}`), an optional `item`, `considered` (claim IDs, or a source,
  locator, quoted anchor and a `read` state), `reasons` (codes from the schema's list),
  `reasoning` (the row's "why not", verbatim) and `ruling` (a decision ID). No status field
  (RR-6), no edge fields. Values are copied by a script that asserts each equals its §1 cell; the
  Verifier re-reads quoted sentences where the registered bytes can be retrieved; the human
  reviews the reason codes; accepted records are promoted (D-061 pattern) and the rows leave §1,
  which keeps the rule. Checks RC-1 to RC-7 in `tests/test_data_candidates.py`. The page reads the
  records, shows the same four candidates as cards grouped by reason, never in the diagram, and
  `edge-dataset.md` leaves the page's inputs.
- **Rejected:** extra fields in `data/relationships.json` (H-2's alternative: every edge reader
  would have to filter refusals, and a stored "refused" status breaks RR-6); rule-made IDs like
  RI-1 (impossible with unrecorded or plural endpoints); keeping the "why not" text in §1 (the page
  would still parse the table); splitting two-source rows into two records (an improvement on the
  row, not a copy).

## D-110 — Values about named records live in data; rules live in their documents

- **Session:** S12 · **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02, at the S13 opening)
- **Context:** S12 Part B §06 q2; the M2 audit's N-2 and N-3. The human's answers at S12: "Rules
  stay in documents (Recommended)" and, for the other document tables, "Later, before the SQL
  layer (S14) (Recommended)".
- **Decision:** a value or evidence pointer about a named record is data and lives in `data/`; a
  rule that governs records (a vocabulary's word table, a matrix, a horizon, a rule line) lives in
  its design document, and code may read it. The rule lines and decision titles the page quotes
  stay where they are. The four other tables that hold per-record values (the CI-1, PI-1 and FI-1
  terms; the IO-1 and FK-1 basis rows) and the two unchecked restatements (legal entities,
  `broader`) are debt DT-1, owned by the Knowledge Architect and the Data Auditor, due before S14.
- **Rejected:** a rules data file (the human's alternative: a second set of files for ~25 rule
  lines, with every defining document pointing at it); migrating the four tables in S12 (a schema
  change to entities; the human chose later).

## D-111 — A refused candidate names every party its quoted sentence names (`cand-002` and Samsung)

- **Session:** S13 · **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02, S13 review)
- **Context:** content audit F-1 (`docs/research/content-audit-S13.md`). `cand-002` refuses
  "SK hynix and Micron supply memory to NVIDIA" from NVIDIA's 10-K (`src-024` p.8), whose quoted
  sentence is "We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung". The
  record and the page's card name two of the three firms. Samsung has no company record. S12 kept
  the §1 row's two parties because the copy rule forbade improving the row (S12 Deviation 4).
- **Decision:** `cand-002` lists Samsung as a third party with no record
  (`{"state": "no_record", "name": "Samsung"}`, the sentence's own word, as `cand-004` records
  Zeiss), adds the reason `endpoint_has_no_record` (RC-5 requires it), and appends one sentence to
  its reasoning; the ruling stays D-089. The page is rebuilt: the card names three firms and also
  appears under "a party has no record". No claim, source, edge or entity changes; no Samsung
  record is created (D-095).
- **Rejected:** a Samsung company record (no filing of Samsung's has been read; D-057); removing
  the card (the refusal is right, only its parties are short); leaving it as debt (the page's
  question is "who is known to make it", and the card answers it short of the source).

## D-112 — The H100 memory figures keep their claim; the source's "preliminary" note is debt

- **Session:** S13 · **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02, S13 review)
- **Context:** content audit F-3. `claim-h100-hbm-stacks` reproduces NVIDIA's sentences on the
  H100's 80 GB of HBM3 (five stacks) and 80 GB of HBM2e. The source, NVIDIA's 2022 Hopper
  architecture blog (`src-051`), notes under its H100 specification table "Preliminary
  specifications for H100 based on current expectations and are subject to change in the shipping
  products". The `incorporates` edge rests on the H100 containing HBM, not on the figures.
- **Decision:** the claim and the edge stay; the note is recorded as debt. S14 does not
  compute over the H100's capacity figures; when product attributes are next researched, a current
  product source is sought for them.
- **Rejected:** narrowing the claim to drop the figures (a new claim ID and a rebuilt page for a
  figure no record uses as a value); adding the note to the page (it would need a place in the data
  for a citation's caveat, a model change).

## D-113 — The S13 audit's debt and owners (DT-10 re-owned)

- **Session:** S13 · **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02, S13 review)
- **Context:** content audit Part 6, findings F-2 and F-4 to F-11. DT-10 (`publisher_entity`
  `not_researched` on 23 sources) was owned by S13.
- **Decision:** each finding is documented debt with the owner Part 6 names. DT-10 is
  re-owned by the Knowledge Architect: linking a web page's publisher to a company record first
  needs a rule for what shows who publishes a page (a filing names its filer; a blog or newsroom
  does not), and the three AWS sources wait on DT-6. Due before any client output relies on
  `party` standing (M6).
- **Rejected:** linking the ten cited sources' publishers in S13 (a value about the world the
  sources do not state as a claim, without a rule; the S13 prompt admits no new fact); a freshness
  test that reads the clock (CI would turn red on a date, not a change).

## D-114 — The repository records the outcome of a human decision, never the conversation

- **Session:** S13 · **Date:** 2026-10-03 · **Status:** accepted (the human's direction, 2026-10-03)
- **Context:** reports, audits, decision statuses and session prompts have copied each question as
  asked and the human's answer word for word (`SESSION-PROMPT-SPEC.md` §9, last paragraph). The
  human does not want conversation content in the repository.
- **Decision:** a record of a human decision states the outcome in project terms and the date, for
  example "approved by the human on 2026-10-02: the card names all three firms". It does not copy
  the question's wording, quote the human's messages, or comment on how the human answered. The
  record still names the decision it settles, so who decided what stays traceable. S13's files were
  cleaned on 2026-10-03; earlier sessions' files and pushed commit messages stay as they are. Commit
  messages follow the same rule from now on.
- **Root documents** (wording approved by the human and applied on 2026-10-03):
  `SESSION-PROMPT-SPEC.md` §9, last paragraph, becomes: "When a decision has already been taken,
  the record states its outcome in project terms and its date, and names the decision it settles.
  It does not copy the question as asked, quote the human's messages, or comment on how the human
  answered." `CLAUDE.md` §17, "Unresolved", gains: "Decisions already taken are recorded as
  outcomes and dates, never as transcripts."
- **Rejected:** cleaning S00 to S12 as well, and rewriting this branch's commit messages (the
  human chose S13's files only).

## D-115 — Every result a page computes with SQL carries a short SQL tutorial

- **Session:** S13 · **Date:** 2026-10-03 · **Status:** accepted (the human's direction, 2026-10-03)
- **Context:** S14 introduces SQL (DuckDB). The project is also a learning instrument for its owner
  (`CLAUDE.md` §1).
- **Decision:** wherever a page shows a result computed with SQL, a small control next to it ("How
  this was computed") opens a short tutorial for that specific task: the question in plain words,
  the query, what each part of the query does, and how to read the result. It is closed by default,
  reachable by keyboard, works at phone width, and is generated from the same query file the
  result is computed from, so the tutorial can never show a different query. S14 builds the first
  one. Nothing appears where no SQL is used.
- **Root documents** (wording approved by the human and applied on 2026-10-03): `CLAUDE.md` §12 gains: "Where a page shows a result
  computed with SQL, a 'How this was computed' control opens a short tutorial of that query: the
  question, the query, what each part does, how to read the result."
- **Rejected:** explanations in the working sessions only, or in both places (the human chose the
  pages).

## D-116 — Reader experience first: meaning before mechanism

- **Session:** S13 · **Date:** 2026-10-03 · **Status:** accepted (the human's direction, 2026-10-03)
- **Context:** the page and the session documents have grown dense with rule codes and internal
  terms. The human prioritises a reader's experience over complexity.
- **Decision:** every page and every document a person reads makes sense in the order it is read:
  it opens with what the reader needs to know in plain language, and keeps codes, IDs, rule
  references and technical detail behind it (a link, a disclosure, a later section), present but
  never in the way. Where a choice is between more machinery and a clearer reading, the clearer
  reading wins unless evidence or traceability would be lost.
- **Root documents** (wording approved by the human and applied on 2026-10-03): `CLAUDE.md` §12 gains: "Pages and documents make sense
  in the order they are read: plain-language meaning first, codes and technical detail behind it.
  The reader's experience takes priority over additional complexity, provided no evidence or
  traceability is lost."
- **Rejected:** writing the three rules into `CLAUDE.md` directly (the human chose to review the
  wording first).

## D-117 — The document tables of per-record values become identity-basis rows in data (DT-1)

- **Session:** S14 · **Date:** 2026-10-03 · **Status:** accepted (the move decided by the human on
  2026-10-03 at the S14 opening, H-1; the row shape accepted by the human on 2026-10-03, at the S14 review)
- **Context:** D-110 puts values about named records in `data/` and rules in documents. Four
  document tables still held such values, read by checks that parsed Markdown (DT-1, DT-9;
  `M2-audit.md` N-2, M-2, M-4): the terms that CI-1, PI-1 and FI-1 build IDs from, and the claim
  (and word) behind each `instance_of` value (IO-1) and each facility kind (FK-1). Two more
  tables restated record values with no check: each company's legal name, each `broader` value.
  The SQL layer must not read Markdown.
- **Decision:**
  - The rows move to `data/identity_basis.json` (staging: `data/staging/identity_basis.json`),
    shape `schemas/identity_basis.schema.json`. One flat row per table row, with a `kind`:
    `concept_term`, `product_term`, `instance_of_basis`, `facility_term`, `facility_kind_basis`.
    A gap concept's record is the state `no_record`. 28 rows; staging empty.
  - Moved by a script, kept with the session report
    (`sessions/reports/SESSION-14-migration/migrate_tables.py`). Before editing any document, it
    asserts that the new loaders return exactly the tuples the Markdown parsers returned.
  - The checks keep their logic. CI-1, PI-1, IO-1, FI-1 and FK-1 now read the rows from data.
    New checks IB-1 to IB-4 (`tests/test_data_identity_basis.py`): each row is valid; there is one
    row per key; a row sits in its record's layer; and the documents never hold the rows again.
  - The documents keep their rules and point to the rows. The legal-entity and `broader` tables
    lose the column that restated the record's value and keep their rulings and reasons.
  - The rule tables stay in their documents (D-110): the words that establish each facility
    kind, the excluded location words, and the capacity markers.
- **Rejected:**
  - New fields on the entity records: reshaping `instance_of` into `{value, claim_ids}` would
    change `tools/trace.py` and `tools/navigate.py`, which S14 may not edit, and add a second
    shape for one field.
  - Keeping the two restating tables and checking them: that adds two Markdown parsers, against
    DT-9.
  - One data file per table: four file pairs for 28 rows.

## D-118 — The SQL layer: DuckDB rebuilt in memory from the canonical files, results committed, page build unchanged

- **Session:** S14 · **Date:** 2026-10-03 · **Status:** accepted (the engine and its place decided by
  the human on 2026-10-03 at the S14 opening, H-2; the rest accepted by the human on 2026-10-03, at the S14 review)
- **Context:** the roadmap's S14 gate: "All published metrics can be regenerated from versioned
  inputs"; `MASTER-ARCHITECTURE.md` §17 names DuckDB. D-003 allows a new dependency only with a
  recorded reason.
- **Decision** (`docs/architecture/sql-layer.md` §1, §2, §5):
  - `tools/warehouse.py` loads the canonical files of `data/` (never `data/staging/`) into a fresh
    in-memory DuckDB on every run. It runs every query in `sql/` and writes each result to
    `sql/results/<query>.json`, recording the digests of its inputs, its query and the engine
    version.
  - The database is never committed and never written back. The runner refuses to save a database
    file inside the repository.
  - `requirements-analysis.txt` pins `duckdb==1.5.6`, which has no transitive dependencies. CI
    installs it. This amends D-003 and D-026: `tools/warehouse.py` and `tests/test_warehouse.py`
    may import DuckDB; every other tool stays standard library.
  - `tools/build_page.py` reads the result and the query file as files and never imports DuckDB, so
    the page still rebuilds byte-identically without it (PG-7). The order is: data, then results
    (`tools/warehouse.py`), then the page.
  - Checks WH-1 to WH-10 (`tests/test_warehouse.py`) and the page's PG-11.
- **Rejected:** a committed database file; DuckDB inside the page build (H-2 B); SQLite (H-2 C);
  DuckDB's own JSON reader (it infers types and turns state objects into structs); loading staging;
  CSV results.

## D-119 — Explicit states in SQL: value and state columns; NULL only beside a state

- **Session:** S14 · **Date:** 2026-10-03 · **Status:** accepted by the human on 2026-10-03, at the S14 review
- **Context:** `MASTER-ARCHITECTURE.md` §5.7; `CLAUDE.md` §7 ("Unknown is never zero"); DT-4
  (`data/` needs flattening for SQL). The records never use JSON `null`.
- **Decision** (`sql-layer.md` §3, §8):
  - A field that holds a value or a state becomes `<field>_value` and `<field>_state`. The state is
    `value`, the record's own state word unchanged, or `absent` when the record has no such key.
  - NULL appears only in a `_value` column whose `_state` is not `value` (WH-4). No result cell is
    NULL. A row with nothing to date says `not_applicable`; an unknown link names its state in
    `gap_reason`.
  - Lists become rows with their position. Assertions become `field_values` rows with their claims
    in `field_value_claims`; an attribute held as a state becomes one `field_values` row carrying
    that state.
  - The loader lists every key of every record kind and refuses an unknown one (WH-3), so nothing
    is dropped silently.
- **Rejected:** NULL for unknowns, with the state in a comment; one generic table of JSON
  documents (every query would have to unpack the states itself).

## D-120 — The first query: each accelerator's links, their basis and their evidence dates

- **Session:** S14 · **Date:** 2026-10-03 · **Status:** accepted by the human on 2026-10-03, at the S14 review
- **Context:** S13's recommended first question; its weaknesses that a query must show (content
  audit Part 5; DT-S13-1, -2, -4, -7).
- **Decision** (`sql/accelerator_dependencies.sql`; `sql-layer.md` §7):
  - **An accelerator** is a product that is an instance of the AI accelerator class, or of a class
    recorded as a kind of it. The claim behind that membership comes from its `instance_of_basis`
    row (D-117).
  - **A link** is one of:
    - an edge into or out of the accelerator;
    - an edge reached by walking `incorporates` and `requires` outward from what the accelerator
      incorporates;
    - an unknown on such an edge (its state becomes the row's gap reason);
    - a recorded gap: a refused candidate about the accelerator whose only reason is
      `evidence_not_fresh`.
  - **The basis** is `stated` if a cited claim is a FACT, `inferred` if none is (D-103), and `gap`
    otherwise.
  - **The evidence dates** are the earliest and latest F-1 evidence dates over the citations the row
    rests on, following input claims.
  - **Caveats** (the S13 weaknesses):
    - `publishers`, so a single voice shows and nothing reads as corroborated;
    - `rests_on_atlas_interpretation` (D-091's definition step);
    - `party_standing_unchecked` (DT-S13-1).
  - No age is computed, because an age needs today's date (DT-S13-4). No capacity figure is read
    (DT-S13-2). No count, share or score is computed (S15).
  - Result: 8 rows, 4 per accelerator, matching the diagram's chain. `tests/test_warehouse.py`
    WH-10 recomputes the result in plain Python and requires the same rows.
- **Rejected:**
  - Every refused candidate about an accelerator as a gap row: those refused as "relation not
    stated" have no evidence stating them.
  - Including the lane (SK hynix's M16): it is not linked to an accelerator.
  - Counting publishers (a metric, S15).

## D-121 — The SQL tutorial lives in the query file; the table is a section of the HBM page

- **Session:** S14 · **Date:** 2026-10-03 · **Status:** accepted (the placement decided by the human
  on 2026-10-03 at the S14 opening, H-3; the tutorial format accepted by the human on 2026-10-03, at the S14 review)
- **Context:** D-115 (a "How this was computed" tutorial beside every SQL result, generated from the
  same query file); D-116 (meaning before mechanism).
- **Decision** (`sql-layer.md` §6):
  - The query file opens with `-- question:` and `-- reading:` paragraphs. Each part of the query
    follows a `-- step:` title and its plain-language lines.
  - The page build splits the file at `-- step:` and shows each part's explanation and its SQL,
    character for character.
  - The section "The chain as a table" follows "The chain". It opens with a framing box in plain
    words, then the table: one line per link, with the IDs behind an "IDs" disclosure, stacked into
    cards at phone width. Then a closed "How this was computed" disclosure.
  - PG-11 checks every cell against the result and the tutorial against the file. WH-9 checks that
    the file's parts rebuild it exactly and that no explanation names a record.
- **Rejected:** tutorial text in a separate file (it could drift from the query); a new page (H-3 B);
  showing the whole query once without steps (harder to follow, D-116).

## D-122 — The visual benchmark and its pattern register

- **Session:** S14.5 · **Date:** 2026-10-06 · **Status:** proposed
- **Context:** the S14.5 prompt asks for a study of five data-intensive research products (Epoch AI, Our
  World in Data, IEA, Stanford AI Index, Datawrapper) across fourteen dimensions, each major pattern
  classified ADOPT, ADAPT or REJECT, with no branding, asset or layout copied.
- **Decision** (`docs/research/visual-benchmark-S14.5.md`):
  - the pages are observed with the pre-installed headless browser at 1440 and 390 px; screenshots and
    the script stay outside the repository;
  - the IEA website refused automated access (403), so IEA is assessed through its *Energy and AI* report
    (PDF, CC BY 4.0) only, and its web navigation and responsive behaviour are recorded as not assessed;
  - 29 patterns are classified. The register is the Atlas's reading (`INTERPRETATION`), and no
    benchmark statement enters the Atlas as a fact.
- **Rejected:** screenshots committed as evidence (they would copy other organisations' visual identity
  into the repository); benchmarking from memory (`CLAUDE.md` §5).

## D-123 — The research-experience model, the visual principles and the minimal design system

- **Session:** S14.5 · **Date:** 2026-10-06 · **Status:** proposed
- **Context:** the S14.5 prompt's required outputs 1 to 9; `CLAUDE.md` §6A, §12; MA §16.1, §19.
- **Decision** (`docs/architecture/visual-architecture.md` §1 to §9):
  - a research page reads `QUESTION → INSIGHT → VISUAL → EXPLORE → EVIDENCE → DATA → METHOD`. Each layer
    is rendered from a committed SQL result or from canonical records, and a lower layer adds detail
    without weakening a higher one;
  - eleven visual principles (V-1 to V-11) and eight analytical UX principles (U-1 to U-8);
  - the design system names the S11 palette's tokens by job. The gap amber is reserved for gaps.
    "No recorded relationship" is drawn neutral, distinct from a gap. Indicator values are set in the
    sans face; system fonts only; no dark mode yet;
  - a grammar for rankings, timelines, maps, dependency diagrams, indicator blocks, comparisons,
    evidence indicators and analytical tables, each with its rule for unknowns and its "not when";
  - the rules for choosing a visual, a table or text, and the evidence-aware semantics table;
  - an information architecture organised by questions, proposed for S20 to build.
- **Rejected:** a charting library; hover tooltips by default; a component library now (two compositions
  exist, MA §16.1 asks for two or three first); a categorical palette before any visual encodes
  identity by hue; dark mode before S22.

## D-124 — From SQL results to visuals: the binding rule, and tallies of drawn rows

- **Session:** S14.5 · **Date:** 2026-10-06 · **Status:** proposed (the tallies with their denominators
  decided by the human on 2026-10-06: the prototype's indicator blocks may show counts of the links the
  page draws, each with its denominator)
- **Context:** the S14.5 prompt (required output 9; "Do not create an opaque dependency score"); NG-11
  (no metrics before their question and denominator are defined); D-115 (a tutorial beside every SQL
  result); D-118 (the page build reads committed results).
- **Decision** (`visual-architecture.md` §10):
  - a visual reads only committed SQL results and canonical records, one mark per result row, each mark
    carrying its row number;
  - the build may copy a cell, tally the rows it draws over a denominator it prints, take the first and
    last of a column it shows, and group rows to say what they share and where they differ;
  - anything else (a share, a ratio, a concentration, a count of things not drawn) is a metric. A metric
    is a SQL column defined in S15, with its tutorial;
  - every tally names its unit and its denominator in the same block, and says when one record appears in
    several rows;
  - the checks recompute every derived value from the result file without the build's code;
  - a limited, stated exception to NG-11: tallies of the rows a page draws are presentation, not metrics.
    S15 may keep them, move them into SQL, or retire them.
- **Rejected:** percentages (a share is a metric); the build computing new quantities; a presentation
  data file holding headline text or indicator values.

## D-125 — The S14.5 prototype: a generated research view of the HBM chain

- **Session:** S14.5 · **Date:** 2026-10-06 · **Status:** proposed
- **Context:** the S14.5 prompt's "Limited implementation": one controlled prototype from existing data,
  preferring the HBM slice, without replacing the current product, without a framework, without a
  general-purpose dashboard system, without new data.
- **Decision** (`visual-architecture.md` §12):
  - `tools/build_insight.py` (standard library; a subclass of `build_page.Page`) and
    `tools/insight_template.html` write `site/hbm-insight/index.html` from:
    - the S14 result `sql/results/accelerator_dependencies.json`;
    - the canonical records;
    - the query file;
    - the HBM page, whose panels its evidence links open;
  - the page shows:
    - a composed headline;
    - a derived comparison;
    - four indicator blocks;
    - one chain strip per accelerator in aligned columns;
    - a CSS-only basis filter;
    - an evidence index;
    - the S14 table with its tutorial;
    - a method block;
  - the stylesheet extends the S11 template's style block, read by the build, so the Atlas keeps one
    palette and one base stylesheet;
  - checks IN-1 to IN-9 (`tests/test_insight.py`), run in CI with every test module. The build refuses
    rows its specification does not fit: an unknown position, two rows in one slot, rows that do not
    form the chain, an evidence link with no panel, or a result from another version of the query;
  - order of builds: data, then `tools/warehouse.py`, then `tools/build_page.py`, then
    `tools/build_insight.py`;
  - the page is marked "Prototype", is not linked from the HBM page, and is not published (NG-13).
    `tools/build_page.py` and the HBM page are unchanged.
- **Rejected:**
  - redesigning the HBM page (forbidden by the prompt; its rules are accepted);
  - a copy of the S11 stylesheet (two homes for the palette);
  - SVG for the strips (HTML text wraps and reflows to a vertical chain at phone width with no second
    drawing);
  - JavaScript for the filter;
  - repeating the evidence panels on the new page (a second home for the trace).

## D-126 — Sub-session numbering: S14.5

- **Session:** S14.5 · **Date:** 2026-10-06 · **Status:** proposed
- **Context:** the human inserted a session between S14 and S15, numbered S14.5. `tools/validate_repo.py`
  accepted only two-digit session numbers (`SNN-PROMPT.md`, `SESSION-NN-REPORT.md`), so the session's
  prompt and report could not be recorded under its own number.
- **Decision:** the validator accepts an optional one-digit suffix: `S14.5-PROMPT.md` and
  `SESSION-14.5-REPORT.md`, matched to each other like any other pair. The prompt is recorded verbatim
  as the human gave it, and listed in the registry between S14 and S15. Later session numbers are
  unchanged. `tests/test_validate_repo.py` covers the new names.
- **Rejected:** renumbering S15 to S25 (every later prompt, the roadmap and the registry would shift); a
  report under S14 or S15 (the work would be filed under another session's contract).
