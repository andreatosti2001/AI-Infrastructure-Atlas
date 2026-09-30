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

- **Session:** S01 · **Date:** 2026-09-29 · **Status:** proposed (deferred at the S01 human review, 2026-09-29; to be decided in S02/S05)
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

- **Session:** S01 · **Date:** 2026-09-29 · **Status:** proposed (deferred at the S01 human review, 2026-09-29; to be decided in S02/S05; superseded by S05's source policy when written)
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

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** proposed
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

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** proposed
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

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** proposed
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

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** proposed
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

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** proposed
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

- **Session:** S04 · **Date:** 2026-09-30 · **Status:** proposed
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
