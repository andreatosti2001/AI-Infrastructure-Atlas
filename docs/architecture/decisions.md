# Architecture Decision Log

Append-only. A superseded decision is marked `superseded by D-NNN`, never rewritten
(`SESSION-PROMPT-SPEC.md` §6). References to a renamed document are updated so they still resolve. Paths
under `sessions/` say where a file was when the entry was written; those files are kept in the private
development archive, not in this repository (D-151).

Status values: `proposed` (awaiting human review) · `accepted` · `superseded`.
Each entry gives its date and status; the status records the outcome and its date, never the question as
asked or the human's words (D-114). Status lines were condensed to this form once (D-151).

---

## D-001 — Constitutional documents stay at the repository root

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29)
- **Context:** The user placed `CLAUDE.md`, `MASTER-ARCHITECTURE.md`,
  `SESSION-PROMPT-SPEC.md`, `PROJECT-EVALUATION-FRAMEWORK.md`, `SESSION-ROADMAP.md`,
  the operational roadmap and the bootstrap prompt at the root. Every document refers to
  them by bare filename, and Claude Code loads `CLAUDE.md` from the root.
- **Decision:** Leave them in place, unmodified. `docs/README.md` indexes them.
- **Rejected:** moving them under `docs/` — this would break cross-references and
  `CLAUDE.md` loading, and restructure human-authored documents without need.

## D-002 — Session system layout

- **Date:** 2026-09-29 · **Status:** superseded by D-151 (2026-10-08); earlier: accepted (2026-09-29)
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

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29); amended by D-026 (pinned test-only dependencies)
- **Context:** Python is the intended language (MA §17). S00 needs only a structural
  validator and its tests.
- **Decision:** `tools/validate_repo.py` and `tests/` use the standard library (`unittest`,
  `pathlib`, `re`). No `pyproject.toml`, lockfile or third-party packages.
- **Rejected:** pytest, a linter/formatter, pre-commit hooks, a Makefile or a package
  layout. None has a current requirement; each can be added, with a recorded reason,
  when one appears (e.g. DuckDB in S14).

## D-004 — One CI job, read-only permissions

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29)
- **Decision:** `.github/workflows/ci.yml` runs the unit tests and the Gate 0 validator on
  every push and pull request, on Python 3.11 (the version the S00 checks were run on),
  with `contents: read` permission.
- **Rejected:** a Python version matrix, deployment/Pages jobs, scheduled runs. There is
  nothing to deploy and no compatibility requirement yet.

## D-005 — No placeholder directories or stub documents

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29)
- **Context:** CLAUDE.md §19 and MA §24 forbid adding infrastructure for appearance.
- **Decision:** Do not create `data/`, `schemas/`, `web/`, `analysis/` or empty stub
  documents. `docs/README.md` lists each planned artifact with its status and owning
  session; the session that first needs a directory creates and designs it.
- **Rejected:** a full scaffold of empty folders with `.gitkeep` files — it would fix a
  data layout before S03–S06 have designed one.

## D-006 — Independence from `Eu-Digital-Policy`

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review; independence confirmed)
- **Decision:** No file, code, folder structure, workflow or data was copied from
  `Eu-Digital-Policy`. That repository was not opened in S00. Methodological
  principles are taken only from this repository's own constitutional documents.
- **Consequence:** Any later reuse of a pattern from `Eu-Digital-Policy` must be
  reimplemented locally and recorded here (MA §4.2).

## D-007 — Baseline record references, not restates, the master architecture

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29)
- **Decision:** `docs/architecture/baseline.md` cites MA/CLAUDE.md sections and records
  only repository state, gaps and uncertainties.
- **Rejected:** copying MA content into the baseline — it would create a second home for
  the same architectural statements, and the two would drift.

## D-008 — First analytical question: global first, EU lens later (resolves U-1)

- **Date:** 2026-09-29 · **Status:** accepted (human decision)
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

- **Date:** 2026-09-29 · **Status:** superseded by D-151 (2026-10-08); earlier: accepted (human decision)
- **Decision:** The session system (`SESSION-ROADMAP.md` + `sessions/prompts/`) governs
  sequencing and scope. The bootstrap prompt stays at the root, unmodified, as a
  historical reference. It does not set session scope.
- **Rejected:** keeping it as an active checklist that S00–S11 must jointly satisfy.

## D-010 — Agent contracts are written in S06 under `docs/agents/`; no `AGENTS.md` (resolves U-4, U-5)

- **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Decision:** S06 (evidence/claim system) writes `docs/agents/roles.md` and
  `docs/agents/contracts.md` in the MA §12 format, because that is when the
  staging → verification → canonical workflow first exists. This repository has no root
  `AGENTS.md`; `CLAUDE.md` remains the single file of agent working rules.
- **Consequence:** The future S06 prompt must include this in its scope.
- **Rejected:** a root `AGENTS.md` (a second rules file next to `CLAUDE.md`); deferring
  the decision to S02.

## D-011 — S01 prompt drafted by Claude, pending human review

- **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Decision:** Claude drafts `sessions/prompts/S01-PROMPT.md` following
  `SESSION-PROMPT-SPEC.md` §2. The human reviews and may edit it before S01 starts. It
  becomes immutable only once S01 begins.

## D-012 — S01 prompt: human text governs, Claude's detail aligned beneath it

- **Date:** 2026-09-29 · **Status:** accepted (human instruction)
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

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review; TQ-05 answer)
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

- **Date:** 2026-09-29 · **Status:** superseded in part by D-039 (2026-09-30): the retrieval clause. Raw retrieval and no circumvention continue in D-039
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

- **Date:** 2026-09-29 · **Status:** superseded by D-036 (2026-09-30) for the tier order, and by D-048 (2026-09-30) for the meaning of `verified`, which D-048 confirms and extends
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

- **Date:** 2026-09-29 · **Status:** accepted (human decision)
- **Context:** Part A's "Human task" asked the human to challenge the domain map's
  terminology. The map listed 12 questions (TQ-01 to TQ-12).
- **Decision:** The human's answers, recorded once in `docs/research/domain-map.md`
  §7.1, are the working terminology for S02–S04. Later sessions may revise them, but
  only through a new decision record. The answers do not resolve the recorded source
  conflicts (map §5).
- **Rejected:** copying the answers into this log, which would give them a second home
  that could drift from the map.

## D-017 — Project boundaries for v1.0

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29)
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

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29); all nine items L-01 to L-09 accepted
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

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29)
- **Context:** U-2. MA §22 M0–M7 are portfolio milestones. `SESSION-ROADMAP.md` M0–M7 are
  Atlas project milestones.
- **Decision:** In documents written in this repository, a bare `M0`–`M7` means the
  `SESSION-ROADMAP.md` milestones. MA §22 milestones are always written "portfolio M4"
  or "MA §22 M4". The human-authored root documents are not edited.
- **Rejected:** renaming the milestones in MA or the roadmap (editing human documents to
  fix a label); a different letter prefix (it would diverge from both documents).

## D-020 — v1 concept classification is S03's starting input

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29)
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

- **Date:** 2026-09-29 · **Status:** accepted (2026-09-29); non-goals frozen from this date
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30); Event schema owner S09 confirmed
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30, human
  decision on the S03 plan)
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

- **Date:** 2026-09-30 · **Status:** accepted (human decision)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
- **Context:**
  - `SESSION-ROADMAP.md` S05: "Create a source hierarchy tailored to industrial technology
    research".
  - The register's 23 sources and its blocked hosts include filings (blocked), datasheets,
    press releases, product pages, newsroom explainers, government documents, national
    laboratory reports, policy briefs and an association report.
  - The human chose option (b) for machine-readability before S05 started, with (a) as the
    fallback (S05 prompt Part B §16, H-2).
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
- **Context:**
  - D-014 asked "whether manual retrieval by the human is acceptable".
  - The human answered before S05 started (Part B §16, H-1): allowed, with conditions.
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30); the 12-month horizon approved
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (human decision)
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

- **Date:** 2026-09-30 · **Status:** accepted (human decision, given before the change)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
- **Context:**
  - D-015's second part defines `verified` "until S06's claim model confirms or replaces
    it" (D-036).
  - CLAUDE.md §9 makes real claims class C: the human reviews them before they are
    canonical.
  - Before S06 started, the human chose a staging seed of 5 to 10 real claims (H-1) and one JSON array
    file per record kind (H-2).
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
- **Context:**
  - MA §15 asks for a documented `validate-data`.
  - D-026 keeps `tools/` standard library.
  - Before S06 started, the human chose tests in CI (H-4).
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
- **Context:**
  - D-010 assigns `docs/agents/roles.md` and `docs/agents/contracts.md` to S06, in the MA
    §12 format.
  - Before S06 started, the human chose full contracts for the roles active through S10
    (H-3).
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

- **Date:** 2026-09-30 · **Status:** accepted (2026-09-30)
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** the roadmap's S07 target is "A small, high-quality seed set rather than
  maximum coverage". Before S07 started, the human chose eight companies, one per chain
  layer (H-1). `entity-taxonomy.md` §3.1 makes a record
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** D-005 leaves each data layout to the session that first needs it. Before S07
  started, the human chose one JSON array file per entity type (H-2).
- **Decision:** `data/companies.json` and `data/jurisdictions.json` hold canonical records.
  `data/staging/companies.json` and `data/staging/jurisdictions.json` hold staging records.
  Each joins `validate-data` in this session (L-05), and `tools/trace.py` reads them by
  default.
- **Rejected:** one `data/entities.json` for every type (H-2); a staging flag inside one file
  (the D-048 reason: a consumer could read a staging record as canonical).

## D-056 — Company ID rule (ID-1)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** H-4 required ISO 3166-1 as ISO
  publishes it, and said to stop and ask if it could not be retrieved under RA-1/RA-2.
  `www.iso.org` refused plain requests (HTTP 403 challenge) on 2026-10-01, so S07 stopped and
  asked. The human chose manual retrieval.
- **Decision** (`company-dataset.md` §5):
  - The human captures the ISO Online Browsing Platform entries for US, NL, KR and TW. Each
    capture is a source record with `standard_specification` class and method
    `manual_by_human`, and the file stays outside the repository. The human supplied
    screenshots; each shows the `iso.org` host and the OBP
    header, and the Verifier reads its anchors off the image.
  - Each jurisdiction record's identity claim is a `FACT`, standing `originator`, whose
    anchor carries the alpha-2 code (J-1).
  - ISO 3166-2 subdivision entries on the same pages are `FACT`s used as inputs to the
    state-to-country derivations (D-057).
  - Display names are editorial, and ISO's short names are aliases, as ISO gives them.
- **Rejected:** a secondary code list (RA-5); no jurisdiction records in S07 (H-4's
  alternative, not chosen).

## D-059 — Regulator-hosted filings readable under RA-1 (SK hynix)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** D-042 takes filings from the filer's own copy, because EDGAR refused plain
  requests and its access policy could not be read. SK hynix's IR site hosts no annual
  report and points readers to the regulator's English DART for disclosures. DART answered
  plain HTTPS requests. The human chose the DART copy.
- **Decision:**
  - D-042's filer-copy rule answers EDGAR's refusal. It does not forbid a regulator's copy
    that answers an ordinary request.
  - A filing read from a regulator's own system under RA-1 is recorded with
    `filing_copy: regulator_hosted`.
  - EDGAR stays an access gap, and no identity is declared to any site (D-042, RA-7).
- **Rejected:** SK hynix's newsroom pages as identity evidence (an acceptable class, but
  weaker, and `incorporated_in` has no acceptable alternative); leaving SK hynix out.

## D-060 — TSMC's 20-F by manual retrieval (RA-4)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** every TSMC host and EDGAR answered with a challenge or refusal on 2026-10-01.
  The human chose to download the 20-F.
- **Decision:** the human downloads TSMC's 2025 Form 20-F from `investor.tsmc.com` and
  supplies it. It is a source record with method `manual_by_human` and `filing_copy:
  filer_hosted_not_checked`. The Verifier reads the file the human supplies, and records its
  hash (RA-4(5)).
- **Rejected:** leaving TSMC open with a seven-company seed.

## D-061 — Staging and canonical for entity records; the human's review in S07 (H-3)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** the accepted entity schema has no review field, and Part B §08 forbids adding
  one without approval. Before S07 started, the human chose to review inside S07 (H-3).
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** VD-11 machine-checks only anchors whose text is in the repository
  (`claim-model.md` §5, §16). Before S07 started, the human chose Verifier attestation with
  a human sample (H-6).
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** D-050 left `publisher_entity` `not_researched` for company publishers until
  S07. The S07 prompt (§06 q11) allows it only where the evidence shows the legal entity.
- **Decision** (`company-dataset.md` §10): a filing's `publisher_entity` names its filer's
  canonical company record. Web pages stay `not_researched`, because they name a channel or
  brand, not a legal entity. V-1 checks that the reference names a canonical company.
- **Rejected:** setting it from copyright lines (a rights holder is not shown to be the
  publisher); setting it for a staging company (V-1).

## D-066 — The M1 milestone audit is written first in S07 (H-5)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01)
- **Context:** PEF §4 requires a milestone audit "At every major milestone". M1 (S03–S06)
  closed with S06, and no session was assigned the audit. Before S07 started, the human
  placed it as S07's first task (H-5).
- **Decision:** `docs/architecture/milestone-audits/M1-audit.md`, a document only, with a row
  in `docs/quality/audit-history.md`. Claude writes it in the Portfolio Reviewer role, which
  `docs/agents/roles.md` marks inactive and gives no contract. This is recorded as a
  deviation from `roles.md`, not a change to it.
- **Rejected:** deferring the audit to S12 (H-5's alternative); activating the Portfolio
  Reviewer role with a contract for one document (D-052's reason: a contract for work no
  session does regularly yet).

## D-067 — Concept scope: 15 of 17 concepts recorded; HBM-03 and HBM-04 are gaps (H-1)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
- **Context:** H-1: every concept that `entity-taxonomy.md`
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
- **Context:** S07's ID rule slugs a claim-backed legal name. A concept's name is editorial
  (Part B §06 q4).
- **Decision** (`concept-dataset.md` §3): the ID is the record type plus the slug of the
  concept's name in `entity-taxonomy.md` §5, an accepted document; a split concept's terms
  use only words of that name and cite a decision. `tests/test_data_entities.py` (CI-1)
  checks the concept table against §5, the schema's `x-concepts` and the records.
- **Rejected:** the S01 concept ID (opaque); a defining standard's term (most concepts have
  none, and HIR says the "2.x" names have no technical basis); the display name (editorial).

## D-069 — Working definitions are always an INTERPRETATION (H-4; DEF-1, DEF-2)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
- **Context:** H-4: each working definition is an
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02); earlier: not approved at human review, left open at H-0
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
- **Context:** `entity-taxonomy.md` §3.3, §3.4 and §9: `broader` is taxonomy only, may have
  several parents, and must be acyclic.
- **Decision** (`concept-dataset.md` §5): data-centre GPU and AI ASIC under AI accelerator;
  assembly and packaging tools under SME; 2.5D packaging and 3D die stacking under advanced
  packaging. The multi-die package has no parent. V-1, CE-1 and B-1 check the references and
  the absence of cycles.
- **Rejected:** multi-die package under advanced packaging (not always high-density); a
  lithography parent (SME-02 has no record).

## D-072 — Products: three records, their IDs (PI-1) and the `instance_of` basis (IO-1) (H-2)

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
- **Context:** H-2: H100, Trainium2, Micron HBM, an ASML
  EUV system. `instance_of` has no claim field in the schema.
- **Decision** (`concept-dataset.md` §7): NVIDIA H100, AWS Trainium2 and Micron HBM4 36GB
  12H. No ASML product: its page names only families. A product ID is `product-`, the
  vendor's ID without `company-`, and the slug of the anchored product name (PI-1). Each
  `instance_of` value has a basis row naming its claim (IO-1).
- **Rejected:** an ASML system from the families page; a schema field for the basis (a
  schema change the human has not approved).

## D-073 — The GH100 ruling

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-01, human ruling at human review)
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
- **Context:** VD-11 (D-062) requires an attested read to be of the registered bytes.
  `src-006`, `src-010`, `src-013` and `src-015` returned changed bytes; their existing
  records are the home of S06 reads.
- **Decision** (`concept-dataset.md` §6): each changed retrieval S08 cites is a new record
  (`src-042` to `src-045`), with the same URL, a title marked with the retrieval date and the
  earlier record's ID, and its own full hash. The old record stays unchanged.
- **Rejected:** rewriting the old record's hash (it would orphan the S06 reads, VD-12); a
  schema field linking the two records (a schema change).

## D-076 — Class rulings for the new sources

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02); earlier: not approved at human review, left open at H-0
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

- **Date:** 2026-10-01 · **Status:** accepted (2026-10-02)
- **Context:** H-3 and H-6.
- **Decision** (`concept-dataset.md` §8, §9): `data/technologies.json`,
  `data/components.json` and `data/products.json`, each with a staging copy; promotion as
  D-061, on the human's verdicts. `tests/test_data_entities.py` extends V-1, CE-1, V-9, V-4
  and V-10 to the new kinds and adds CI-1, DEF-1, DEF-2, B-1, PI-1 and IO-1, with fixtures and
  planted faults. `tools/trace.py` reads the new files and prints `vendor`, `instance_of` and
  `broader`.
- **Rejected:** one combined concepts file (H-3's alternative); a `tools/validate_data.py`
  (D-051).

## D-078 — Facility scope: filing-named sites; plans as events; ASML a gap (H-1)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-1. The registered filings were
  re-retrieved (H-4). At the start of S09 the human ruled that ASML's sites stay a gap with a
  proposal for a new facility kind, and agreed to re-supply TSMC's 20-F.
- **Decision** (`facility-dataset.md` §1): a facility record needs a sentence, from a source
  its rows accept, that names one site, places it, and gives its kind. Records: Micron's fab
  in Manassas, Virginia and SK hynix's M16. TSMC's sites are a gap: its 20-F was not
  re-supplied during S09, and the human closed it as a gap. Sites known
  only from plans (Micron Boise and Clay, SK hynix M15X, Amkor Arizona) are events (ER-8). No
  site sentence (Micron's and Amkor's country tables), no jurisdiction record (Japan), or
  no kind evidence (SK hynix Cheongju) means no record. No data centre is named.
- **Rejected:** Micron or Amkor country rows as sites; facility records for sites under
  construction; ASML sites forced into an existing kind.

## D-079 — Facility ID rule (FI-1)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
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

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02); its flagged ruling (clause-only anchors that leave out a head-office clause or phrase) approved at human review (2026-10-02)
- **Context:** R-5; `source-policy.md` §7 rows `attr:facility.located_in`, `.locality`.
- **Decision** (`facility-dataset.md` §3): `located_in` and `locality` rest on a sentence
  placing the site; a subdivision reaches the country by the D-057 `DERIVATION`; `locality`
  is in the source's script. HQ-1 fails a location that reaches a claim serving a company's
  headquarters or incorporation (ISO claims aside), or an anchor carrying an excluded word
  of §3's table.
- **Rejected:** M16's location from SK hynix's release phrase "at headquarter located in
  Icheon"; the head-office address as the bridge from 이천 to 경기도.

## D-081 — Facility kinds rest on basis rows and listed words (FK-1)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02); its flagged ruling ("fab"
  and "fabrication plant" read as `wafer_fab`) approved at the S09 review (2026-10-02)
- **Context:** `facility_kinds` has no claim field; IO-1 (`concept-dataset.md` §7) is the
  precedent for a basis table.
- **Decision** (`facility-dataset.md` §4): each kind of each record has a basis row naming an
  identity claim and a word in its anchor; the word must be one §4 lists for the kind.
- **Rejected:** a kind read from the company's role (R-3); a kind without a named word.

## D-082 — Ownership, operation and production evidence for S10 (H-3)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-3; `relationship-taxonomy.md`
  §4.3, §4.4, §5.
- **Decision** (`facility-dataset.md` §5): the candidate sentences are staging claims, each
  marked against §5. Micron's "our fab" fails both `owns` and `operates`. SK hynix's
  "생산공장을 설치ㆍ가동" partly meets `operates` (the site is named by its town), as a
  `DERIVATION` with the M16 row; it fails `owns`. No edge is created. No v1 type holds
  site-level production; nothing is proposed.
- **Rejected:** "our" read as controlling ownership; an operator inferred from the filer.

## D-083 — The event schema (H-2)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, human review; its two flagged rulings, 준공 recorded as `opened` and the company as the
  subject of a planned site's announcement, approved)
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

- **Date:** 2026-10-02 · **Status:** accepted (adding rows approved at the
  start of S09; the rows' content approved at the review on 2026-10-02)
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

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** MA §5.6; R-8; Part B §06 q5.
- **Decision** (`facility-dataset.md` §7): `tools/facility_status.py` derives `opened`,
  `closed`, `not_yet_opened`, `indeterminate` or `no_recorded_opening` on a date from the
  occurrence events, reading partial dates as periods. Plans and expansions never move it.
  Tested by `tests/test_facility_status.py` (ST-1). The tool is a Data Auditor write
  (`docs/agents/contracts.md`).
- **Rejected:** a stored status; "operating" as a state (an `opened` event says completed or
  began operating on a date, not today).

## D-086 — Capacity and data centres (CAP-1)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** TQ-10; the schema's `nameplate_it_capacity_mw`.
- **Decision** (`facility-dataset.md` §8): `not_applicable` on any site that is not a data
  centre; on a data centre, a value needs an anchor carrying a §8 marker. No data-centre
  record in S09.
- **Rejected:** a power or interconnection figure as capacity.

## D-087 — Layout, review and validate-data for facilities and events (H-5, H-6)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-5, H-6.
- **Decision** (`facility-dataset.md` §9 to §11): `data/facilities.json` and
  `data/events.json` with staging copies; promotion as D-061 on the human's verdicts.
  Checks FI-1, HQ-1, FK-1, CAP-1 in `tests/test_data_entities.py`; EV-1 to EV-4 and EI-1 in
  `tests/test_data_events.py`; VD-2 for events; ST-1. Each English DART section is its own
  source record (`src-046` to `src-048`), as `src-030` is.
- **Rejected:** one combined file; a separate validator script (D-051).

## D-088 — Proposal: a facility kind for equipment manufacturing (not applied)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02): the gap stands and the proposal goes to a later session; no schema
  is changed (the gap and the proposal chosen by the human at the start of S09)
- **Context:** ASML's manufacturing sites (`claim-asml-manufacturing-sites`) assemble and
  test lithography systems; `vocab_facility_kind` has no fitting value.
- **Proposal:** a later session adds a kind for sites that manufacture semiconductor
  manufacturing equipment (the `production_equipment` use class), with its definition and
  words for FK-1, by an approved schema change. Until then ASML's sites have no record.
- **Rejected for S09:** any schema change (Part B §08).

## D-089 — Edge scope: five edges, and the candidates that fail §5 (H-1)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-1 (agreed by the human on 2026-10-02: product and company edges first, then `operates`
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

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** Part B §06 q2: a stable, non-editorial rule from the type and endpoints, with
  `item` where the type has one, machine-checked as FI-1 and EI-1 are.
- **Decision** (`edge-dataset.md` §2): `rel-<source_entity>-<type, _ as ->-<target_entity>`, and
  `-<item>` for `supplies`. Entity IDs keep their type prefixes. A second record for the same
  relation (another period, V-5) would collide and needs a decision.
- **Rejected:** IDs without type prefixes (a technology and a component with one slug would
  collide); a counter (not recomputable); a claim or display name in the ID.

## D-091 — A class edge read out of a definition (the human's ruling)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, human review; the edge approved as a
  flagged ruling); the ruling itself was given at the start of S10 (2026-10-02, a §16 stop condition)
- **Context:** `requires` needs necessity stated for the class (§5). The ECP report defines HBM
  as vertically stacked DRAM dies directly connected by TSVs; no source states "HBM requires 3D
  die stacking" in words, and ER-1 does not cover the step.
- **Decision:** HBM `requires` 3D die stacking rests on `claim-hbm-requires-3d-die-stacking`, a
  `DERIVATION` from the ECP definition and the two working definitions. RV-1's `requires` row
  carries "stacks" for this case. It is flagged on the review sheet.
- **Rejected:** no class edge (the human's alternative); HBM `requires` TSV (TSV is a gap,
  `concept-dataset.md` §1).

## D-092 — TSMC → H100 `fabricates` is a gap until fresh evidence (the human's ruling)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02); the ruling was given at the
  start of S10 (2026-10-02)
- **Context:** the edge meets §5 only as an ER-1 `DERIVATION` from "Using the TSMC 4N fabrication
  process enables H100" (`claim-h100-process-name`), whose source was last modified 2025-07-22.
  `rel:fabricates` is `time_sensitive`, so F-1 (extended to edges, D-096) fails. NVIDIA's live
  Hopper page names TSMC 4N for the architecture, not the product.
- **Decision:** no edge. The derivation `claim-tsmc-fabricates-h100` is staged for review; the
  edge waits for product-level evidence dated within the horizon.
- **Rejected:** the Hopper page as fresh input (architecture, not product: D-073 logic); waiving
  F-1 for edges.

## D-093 — "AWS-designed" gives a `designs` edge from `company-amazon-com` (the human's ruling)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02); the ruling was given at the
  start of S10 (2026-10-02)
- **Context:** Amazon's release (`src-052`) names "Amazon Web Services, Inc. (AWS), an
  Amazon.com, Inc. company" announcing "two AWS-designed chip families—AWS Graviton4 and AWS
  Trainium2". There is no AWS company record; AWS is an accepted alias of `company-amazon-com`
  (D-074).
- **Decision:** the edge's source is `company-amazon-com`; the claim keeps the release's wording,
  including the AWS legal entity's name. The AWS legal-entity question stays open.
- **Rejected:** waiting for an AWS record (the human's alternative); Amazon's "our custom AI
  silicon" (not a statement of design work, ER-2).

## D-094 — Unknown HBM suppliers are `not_researched`

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** `incorporates` requires `supplier` (D-031); ER-3 and D-049 set when
  `not_publicly_determinable` may be claimed.
- **Decision** (`edge-dataset.md` §5): both `incorporates` edges carry `not_researched`; no
  preferred class was fully searched for either product. No search claim is created. V-10
  checks a `not_publicly_determinable` search against every preferred class of
  `rel:incorporates.supplier` (the S06 handoff, `claim-model.md` §8).
- **Rejected:** `not_publicly_determinable` from one page's silence; a supplier from NVIDIA's
  company-level list (ER-9).

## D-095 — No new company records in S10 (H-3)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-3.
- **Decision** (`edge-dataset.md` §6): none is created. A subsidiary named in a parent's filing
  cannot meet D-057 (the filer's own statement of its legal name), and no supplier has a
  `supplies` edge whose item is a record. `owns` edges wait.
- **Rejected:** a subsidiary record from Amkor's Exhibit 21.1; an AWS record from the release.

## D-096 — validate-data and validate-freshness for edges

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
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

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-5; the roadmap gate "Graph-like
  navigation is possible using relational data without introducing a graph database".
- **Decision** (`edge-dataset.md` §8): `tools/navigate.py`, standard library, answers
  `depends-on`, `suppliers`, `actors`, `edges` and `evidence` (through the trace), canonical by
  default, never printing "none" for a missing edge. Tested by `tests/test_navigate.py`. A Data
  Auditor write.
- **Rejected:** DuckDB now; extending `tools/trace.py` only; a stored adjacency list.

## D-098 — Layout, review and promotion for edges (H-2, H-6)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-2 and H-6.
- **Decision** (`edge-dataset.md` §9): `data/relationships.json` and
  `data/staging/relationships.json`, the relation type as a field. Promotion as D-061, on the
  human's verdicts, when every cited claim, endpoint, item and supplier company is canonical.
  The Extractor's writes extend to the staging relationship file.
- **Rejected:** one file per relation type (H-2's alternative); promotion after the session.

## D-099 — SK hynix `operates` M16 as a `DERIVATION` (flagged for the review)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, human review; the edge approved as a flagged ruling)
- **Context:** D-082 left to S10 whether SK hynix's "생산공장을 설치ㆍ가동" (it operates its
  production plants in 경기도 이천시), with M16 listed as its plant in 이천, meets `operates`.
- **Decision:** the edge rests on `claim-sk-hynix-operates-m16`, a `DERIVATION` from those
  claims and the M16 release; it has no period. It is asked as a separate question at the
  review, and an unticked box leaves it in staging.
- **Rejected:** `valid_from: 2021-02` (construction, not operation); `owns` from 설치 (D-082).

## D-100 — The first journey: the HBM dependency chain (H-1)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-1 (2026-10-02: the recommended HBM chain approved). At the start of S11 the human
  ruled on two records the chain does not link: SK hynix's M16 is drawn in a separate lane, and
  Micron's HBM4 36GB 12H in a lane marked as not connected.
- **Decision** (`vertical-slice.md` §1): the journey answers "What does an AI accelerator's memory
  depend on, and who is known to make it?" over H100 and Trainium2 → HBM → 3D die stacking, with
  Amazon's `designs` edge, both `not_researched` suppliers and the TSMC → H100 gap. M16 and
  Micron's HBM4 are shown in a separate lane, "not linked to either accelerator".
- **Rejected:** a company profile (H-1's alternative); M16 drawn beside HBM (would imply supply);
  M16 only in the limitations (the human's alternative); Micron left off.

## D-101 — Structured output for the walk and the trace (H-4)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-4 (as part of H-1); the S10 debt "the navigation tool
  prints text only".
- **Decision** (`vertical-slice.md` §2): `tools/navigate.py` computes each answer as data
  (`depends_on_tree`, `supplier_rows`, `actors_list`, `edges_at`) and renders its text from it;
  `tools/trace.py` gains `trace_data`, the trace as a normalised structure (record, claim paths,
  claims, sources, missing references). Both print JSON with `--json`. The build imports the same
  functions. Tests check that the JSON and the text name the same edges, claims and sources.
- **Rejected:** the build walking the files itself (a second walk to keep in step); re-parsing the
  text output.

## D-102 — The build step and its stamp (H-2)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-2. Part B §11 asks the page to
  state the data commit; the human ruled that the page states an input digest instead.
- **Decision:** `tools/build_page.py` (standard library) writes one self-contained file,
  `site/hbm-chain/index.html`, with inline CSS and SVG and no script, from `data/`, the schemas,
  `edge-dataset.md` §1, `decisions.md` and `tools/page_template.html`. Output is deterministic
  (sorted inputs, no clock, no environment). The page carries a SHA-256 over its input files;
  `--check` rebuilds and compares bytes. The commit is recorded in the session report.
- **Rejected:** a page reading the JSON at run time and a charting library (H-2's alternatives); a
  commit stamp (a committed page cannot carry its own commit; CI's shallow clone); a separate
  stylesheet file (one self-contained file is what H-2 named).

## D-103 — The visual form and its encoding

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** MA §16.1 (the grammar: flows and dependencies → flow diagrams); Part B §06 q3.
- **Decision** (`vertical-slice.md` §3): a fixed vertical dependency diagram in inline SVG.
  Box fill and rule encode level (instance or class); the line style encodes the basis (solid:
  a `FACT` is cited; dashed and labelled "inferred": only `DERIVATION`s); amber hatched pills
  encode gaps. No visual channel encodes a magnitude, a confidence or time.
- **Rejected:** a table as the primary visual (kept as the text equivalent); a force-directed
  network (position would carry no meaning); colour alone for "inferred".

## D-104 — Gap encoding and the lane

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, human review; the lane rule superseded in part by D-148 (2026-10-07): the lane's note names only its facility and product
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

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** Part B §02 (five things the page must make impossible), §07 task 6; MA §15
  (`validate-design`).
- **Decision** (`vertical-slice.md` §4, §8): every text node sits inside a record value
  (`data-ref`, `data-field`), an absent value, a fixed label, a derived value or a visibly marked
  framing block that names no record. `tests/test_page.py` (PG-1 to PG-10) is `validate-design`
  for this page; it runs in CI with every test module.
- **Rejected:** checking only that the page builds (would miss a hand edit); snapshot tests of
  the HTML (would freeze presentation, not provenance); hard-coded record values in tests.

## D-106 — Browser QA in a scratch environment (H-3)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02, human review; amended by D-151 (2026-10-08): the scripts are kept in `tests/browser/`
- **Context:** H-3.
- **Decision:** browser checks run with the pre-installed Chromium and Playwright outside the
  repository: desktop and 375 px screenshots, overflow, the keyboard path to every panel, console
  and network logs, measured contrast. The script and results are recorded in the report. Static
  accessibility checks run in CI (PG-8).
- **Rejected:** Playwright pinned and run in CI (H-3's alternative; a new dependency for one page).

## D-107 — Editorial and QA contracts (H-5)

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** H-5 (the contracts written in S11, as proposals); the human approved checking them in
  both `tests/test_agent_contracts.py` and `tests/test_page.py`.
- **Decision:** `docs/agents/contracts.md` gains Editorial and QA contracts with MA §12's fields;
  `roles.md` marks both active. Editorial writes the framing and style in
  `tools/page_template.html` and the state rows of `README.md`, `docs/README.md` and
  `baseline.md`; QA writes browser findings and screenshots in `sessions/reports/`. Both are
  checked by `tests/test_page.py`. `tests/test_agent_contracts.py`'s expected active set gains the
  two roles.
- **Rejected:** leaving both inactive with the work under the Data Auditor (H-5's alternative).

## D-108 — Changes from the human's new-user test

- **Date:** 2026-10-02 · **Status:** accepted (2026-10-02)
- **Context:** the human's new-user test. Asked for suggestions, Claude
  proposed seven changes; the human agreed, on the principle that the page must not overreach
  (2026-10-02).
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
- **Not done** (the same principle: no overreach): no plain-language rewrite of the design record's
  reasons (they stay quoted verbatim); no definition for a bare section mark; no further cut of the
  evidence panels (each mark still opens its full evidence in one click).
- **Rejected:** rewriting the "why not" cells in plain words (a second home for the reasons);
  collapsing claim cards (the evidence would sit two clicks from its mark).

## D-109 — The refused candidates become records (H-1, H-2)

- **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02)
- **Context:** H-1 (end of S11: records); the S12 audit's blocking finding B-1
  (`milestone-audits/M2-audit.md` Part 2 N-2, I-5; Part 3 q1). The human decided at S12 that the 12
  relationships the Atlas considered and refused are stored in their own file, separate from real links.
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

- **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02)
- **Context:** S12 Part B §06 q2; the M2 audit's N-2 and N-3. The human decided at S12 that rules stay
  in documents and that the other document tables move later, before the SQL layer (S14).
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

- **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02)
- **Context:** content audit F-1 (`docs/research/content-audit.md`). `cand-002` refuses
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

- **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02)
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

- **Date:** 2026-10-02 · **Status:** accepted (approved by the human on 2026-10-02)
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

- **Date:** 2026-10-03 · **Status:** accepted (the human's direction, 2026-10-03)
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

- **Date:** 2026-10-03 · **Status:** accepted (the human's direction, 2026-10-03)
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

- **Date:** 2026-10-03 · **Status:** accepted (the human's direction, 2026-10-03)
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

- **Date:** 2026-10-03 · **Status:** accepted (the move decided by the human on
  2026-10-03, H-1; the row shape accepted by the human on 2026-10-03, at the S14 review)
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

- **Date:** 2026-10-03 · **Status:** accepted (the engine and its place decided by
  the human on 2026-10-03, H-2; the rest accepted by the human on 2026-10-03, at the S14 review)
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

- **Date:** 2026-10-03 · **Status:** accepted by the human on 2026-10-03
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

- **Date:** 2026-10-03 · **Status:** accepted by the human on 2026-10-03; the basis definitions superseded in part by D-148 (2026-10-07): a fourth basis, "reported"
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

- **Date:** 2026-10-03 · **Status:** accepted (the placement decided by the human
  on 2026-10-03, H-3; the tutorial format accepted by the human on 2026-10-03, at the S14 review)
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

- **Date:** 2026-10-06 · **Status:** accepted by the human on 2026-10-06
- **Context:** the S14.5 prompt asks for a study of five data-intensive research products (Epoch AI, Our
  World in Data, IEA, Stanford AI Index, Datawrapper) across fourteen dimensions, each major pattern
  classified ADOPT, ADAPT or REJECT, with no branding, asset or layout copied.
- **Decision** (`docs/research/visual-benchmark.md`):
  - the pages are observed with the pre-installed headless browser at 1440 and 390 px; screenshots and
    the script stay outside the repository;
  - the IEA website refused automated access (403), so IEA is assessed through its *Energy and AI* report
    (PDF, CC BY 4.0) only, and its web navigation and responsive behaviour are recorded as not assessed;
  - 29 patterns are classified. The register is the Atlas's reading (`INTERPRETATION`), and no
    benchmark statement enters the Atlas as a fact.
- **Rejected:** screenshots committed as evidence (they would copy other organisations' visual identity
  into the repository); benchmarking from memory (`CLAUDE.md` §5).

## D-123 — The research-experience model, the visual principles and the minimal design system

- **Date:** 2026-10-06 · **Status:** accepted by the human on 2026-10-06
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

- **Date:** 2026-10-06 · **Status:** accepted (the tallies with their denominators
  decided by the human on 2026-10-06 during the session; the rule as a whole accepted by the human on
  2026-10-06, at the S14.5 review)
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

- **Date:** 2026-10-06 · **Status:** accepted by the human on 2026-10-06
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

- **Date:** 2026-10-06 · **Status:** superseded by D-151 (2026-10-08); earlier: accepted by the human on 2026-10-06
- **Context:** the human inserted a session between S14 and S15, numbered S14.5. `tools/validate_repo.py`
  accepted only two-digit session numbers (`SNN-PROMPT.md`, `SESSION-NN-REPORT.md`), so the session's
  prompt and report could not be recorded under its own number.
- **Decision:** the validator accepts an optional one-digit suffix: `S14.5-PROMPT.md` and
  `SESSION-14.5-REPORT.md`, matched to each other like any other pair. The prompt is recorded verbatim
  as the human gave it, and listed in the registry between S14 and S15. Later session numbers are
  unchanged. `tests/test_validate_repo.py` covers the new names.
- **Rejected:** renumbering S15 to S25 (every later prompt, the roadmap and the registry would shift); a
  report under S14 or S15 (the work would be filed under another session's contract).

## D-127 — `sql-layer.md` §7: the inferred rows rest on two publishers

- **Date:** 2026-10-06 · **Status:** accepted (confirmed by the human on 2026-10-06)
- **Context:** S14.5 found that `sql-layer.md` §7 said "every row today has one" publisher, while each
  inferred row rests on two (S14.5 report, invalidated assumptions). The S14 table's caveat flags were
  always correct.
- **Decision:** the sentence now says that every stated row and every recorded gap has one publisher,
  and each inferred row two, behind different steps of one reasoning, which do not confirm one another.
  Only that sentence and its status line changed.
- **Rejected:** leaving the sentence as debt.

## D-128 — Evidence coverage: per accelerator, over its links

- **Date:** 2026-10-06 · **Status:** accepted (as built by the human on 2026-10-06; the population decided by the human on 2026-10-06; the split superseded in part by D-148 (2026-10-07): a `reported` column
- **Context:** Part A's "evidence coverage"; S14's handover; S14.5's finding that 8 rows come from 5
  records.
- **Decision** (`metrics.md` §2, §3; `sql/evidence_coverage.sql`):
  - for each accelerator, the rows of the table of links split into stated, inferred and gap, over the
    number of its links;
  - the result also gives the distinct records behind the rows and how many of them are shared with
    another accelerator;
  - the query reads the first result as a view;
  - WH-12 recomputes it independently, and IN-10 checks the page against it. It replaces the prototype's
    hand count with the same numbers.
- **Rejected:** coverage over the whole Atlas (identity fields inflate the stated part); over claims
  (says nothing about the chain); a percentage (four rows).

## D-129 — Source age against a reference date, and where each evidence date comes from

- **Date:** 2026-10-06 · **Status:** accepted (as built by the human on 2026-10-06; the reference date decided by the human on 2026-10-06)
- **Context:**
  - Part A's "source age";
  - S14 refused clock ages, and S14.5's V-5 forbids ages relative to today;
  - S14's and S14.5's debt: an access date standing as an evidence date;
  - DT-S13-4.
- **Decision** (`metrics.md` §4; `sql/source_age.sql`, `sql/accelerator_dependencies.sql`):
  - **the first query** gains `evidence_dated_from_basis` and `evidence_dated_to_basis` (`as_of`,
    `stated`, `accessed`, `not_applicable`). When kinds share a date, the weakest is reported. Its rows
    are unchanged;
  - **the source-age query** ages each link's newest evidence as of the reference date written in the
    file (2026-10-06), and flags links beyond the 12-month horizon. A link with nothing to date says
    `not_applicable`;
  - **both pages flag access dates:** the HBM page's table and the research view's chain and age
    table;
  - **checks:** WH-10 computes the date basis independently; WH-13 computes the ages independently, and
    checks that moving the reference date moves the ages and nothing else;
  - **DT-S13-4** is discharged for the page's chain. The Atlas-wide ageing report stays with the Change
    Detector.
- **Rejected:** today's date (results would change daily); a script in the page (H-3 C: three rules
  broken); integer ages with a sentinel.

## D-130 — The three supplier metrics: "cannot be computed yet", with why

- **Date:** 2026-10-06 · **Status:** accepted (as built by the human on 2026-10-06; the treatment decided by the human on 2026-10-06; the status rule superseded in part by D-148 (2026-10-07): a named supplier alone does not make a metric computable
- **Context:** supplier count, geographic concentration and single-source relationships need a named
  supplier. The Atlas names none: both HBM `supplier` fields are `not_researched` (D-094), and no
  `supplies` edge exists.
- **Decision** (`metrics.md` §5; `sql/supplier_metrics.sql`):
  - **the query:** one row per metric, giving:
    - the incorporated parts, counted per accelerator;
    - those with a named supplier and those unknown;
    - the unknowns' state word;
    - the supply links, in a separate column (DT-7);
    - the status;
    - what evidence each metric needs;
  - **the page:** each metric as an amber "cannot be computed yet" block with its reason. The named
    count and the supply-link count are never shown, because a bare zero would read as "no suppliers";
  - **the stop rule:** the page build stops if a metric becomes computable, until its presentation is
    designed;
  - **checks:** WH-14 computes the query independently, and a planted `not_publicly_determinable` keeps
    its own word;
  - **DT-7** is closed for S15's metrics.
- **Rejected:** a research step first (H-1 B); leaving the three out (H-1 C); counting part classes
  (hides one unknown).

## D-131 — Queries may build on queries; a metric's tutorial answers PEF §8

- **Date:** 2026-10-06 · **Status:** accepted as built by the human on 2026-10-06
- **Context:** the metrics must count the rows the page draws, under the first query's definitions,
  without copying them. PEF §8's eight answers must sit beside each metric and in its tutorial.
- **Decision** (`metrics.md` §8; `tools/warehouse.py`):
  - the warehouse orders the queries so that a query runs after every query whose file stem its code
    names. Each query becomes a view after it runs, and a cycle stops the run;
  - a result's inputs include the query files it builds on (WH-11);
  - the tutorial header (D-121) also accepts `population`, `denominator`, `assumptions`, `missing
    data`, `reproduce`, `sensitivity` and `does not prove`. Every metric's file answers all eight (WH-9),
    and pages render them;
  - the tutorial rendering moves into `build_page.Page.sql_tutorial_block`, shared by both pages (the
    third composition of MA §16.1);
  - the HBM page's output is unchanged apart from its access-date flag, the tutorial's query attributes
    and its digest.
- **Rejected:** repeating the first query in each metric; `CREATE MACRO` or SQL includes; PEF answers
  in a separate document (a second home).

## D-132 — The metrics in the research view's indicator blocks

- **Date:** 2026-10-06 · **Status:** accepted (as built by the human on 2026-10-06; the placement decided by the human on 2026-10-06)
- **Context:** `visual-architecture.md` §7.5 (indicator blocks), §10 (D-124); the prototype's three
  hand counts (S14.5 handover).
- **Decision** (`metrics.md` §6, §7; `tools/build_insight.py`, `tools/insight_template.html`):
  - **the INSIGHT layer** shows two rows:
    - "Indicators": evidence coverage (SQL cells), evidence age (a count of the drawn age rows, with
      access dates called out) and publishers (the presentation count, kept);
    - "Cannot be computed yet": the three supplier metrics;
  - **each metric block** links to its "How this was computed" in the METHOD layer, where one tutorial
    per metric renders its query file;
  - **the DATA layer** gains "Evidence age, link by link";
  - **of the prototype's hand counts**, "links on stated evidence" and "rows with nothing to date" are
    replaced, and "publishers" is kept;
  - **checks:** IN-10 and IN-11 are added to `tests/test_insight.py`.
- **Rejected:** a section on the HBM page (H-4 A: two ways of showing counts); a new page (H-4 B).

## D-133 — Evidence coverage kept, its records line and its population reworded

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** `analytical-audit.md` §2, findings C-1 and C-3. Neither cold reader understood "rows
  drawn from 3 records, of which shared with another accelerator: 1". An independent reader given only the
  population and denominator lines counted the H100 as 5 links, not 4.
- **Decision** (`sql/evidence_coverage.sql`; `tools/build_insight.py`):
  - the metric, its query and its numbers are unchanged;
  - the block's records line reads "The 4 links come from 3 records; 1 record is also counted under another
    accelerator", every number a cell of the result;
  - the header's population line says how far "around" reaches (the accelerator's own edges plus the
    incorporates and requires edges walked from its parts), that an unknown field is a row of its own, and
    that a refused relation is a row only when its one reason is stale evidence;
  - **checks:** IN-12 (the records line, from cells) and WH-15 (the population line).
- **Supersedes:** D-128's block wording only; its population and denominator stand.
- **Rejected:** keeping the block as built; retiring it; naming each gap's reason in the split line (C-2 is
  the first query's definition, recorded as debt in D-138).

## D-134 — Source age kept; the 12-month horizon said to apply only to time-sensitive links

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** `analytical-audit.md` §3, findings C-4 and C-6. The source policy (§12; D-040) applies
  its 12-month re-check only to `time_sensitive` rows (`rel:fabricates`, `rel:incorporates.supplier`,
  `rel:supplies`). `stable` rows (`rel:designs`, `rel:incorporates`, `rel:requires`) have no age limit.
  The block and its tutorial applied the horizon to every link, and the tutorial stated the rule wrongly.
- **Decision** (`sql/source_age.sql`; `tools/build_insight.py`):
  - the metric, its columns and its counts are unchanged;
  - the question asks which links rest only on evidence more than 12 months older than the reference date;
  - the assumptions and does-not-prove lines say where the horizon applies;
  - the block's note reads "Twelve months is a reading aid: the Atlas's re-check rule applies it only to who
    fabricates a product and who supplies a part. An undated web page is dated by the day it was read."
    This replaces "Dates, not ages: …";
  - **checks:** IN-12 (the note) and WH-15 (the header).
- **Supersedes:** D-129's description of the horizon as the freshness horizon for every link. The column
  `beyond_horizon` keeps its name and its computation.
- **Rejected:** keeping the block as built; retiring it; a time-sensitivity column in the query (the
  freshness class lives in `source-policy.md`, not in `data/`; a new SQL input is beyond an audit's
  remediation).

## D-135 — The publishers tally retired

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** `analytical-audit.md` §4, §6 and finding C-7:
  - the block's "1 to 2" was the range of a per-row count the page computed and never showed;
  - its "4 of 6" counted 6 rows from 5 records without saying so (both outside D-124);
  - its only "2" was the inferred link's two reasoning steps, which do not confirm one another;
  - neither cold reader could act on it.
- **Decision** (`tools/build_insight.py`; `metrics.md` §6):
  - the block leaves the research view;
  - every table row resting on one publisher keeps its "one publisher only" flag, on both pages;
  - **checks:** IN-12 requires the block and its four tallies to stay gone, and every flag to stay. IN-3 no
    longer recomputes the retired tallies.
- **Supersedes:** D-132's "publishers (the presentation count, kept)"; `metrics.md` §6's "kept".
- **Rejected:** keeping it, reworded, with the range still computed in the page; keeping it as built.

## D-136 — The three supplier metrics kept as built

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** `analytical-audit.md` §5 and §6:
  - both cold readers read the blocks as unknown, not zero;
  - each block's "needs" names different evidence;
  - probe P7 confirms that both builds stop, with named reasons, when a supplier is named.
- **Decision:** D-130 stands as built: three amber "cannot be computed yet" blocks, and the stop rule.
- **Rejected:** one merged block (S15's open question; no reader was misled, and each metric keeps the
  place it will take once computable); retiring them (the indicators would no longer show the gap).

## D-137 — The source-age reference date moves with each session that rebuilds the pages

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:**
  - S15's debt row, "nobody is yet charged with moving it";
  - probes P5 and P6: a move changes only the ages and the "as of" date until a link crosses 12 months.
    The next crossing is 2027-10-02, Trainium2's access-dated link.
- **Decision:**
  - a session that rebuilds the pages, for any reason, sets the reference date in `sql/source_age.sql` to
    the day it opened, as part of its rebuild;
  - S16 set it to 2026-10-07;
  - each move changes the query, `sql/results/source_age.json`, the research view's "as of", ages and age
    table, and both pages' digest lines;
  - WH-13 now moves whatever date the query holds by one year, instead of a fixed date.
- **Amends:** D-129's "moves only by a commit". It still moves only by a commit, now with an owner.
- **Rejected:** moving only in audit sessions (rebuilt pages would carry an older "as of" between audits);
  moving only when the human asks.

## D-138 — The S16 findings: remediated or debt with owners

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** `analytical-audit.md` §8.
- **Decision:**
  - **remediated in S16:** C-1 and C-3 (D-133), C-4 and C-6 (D-134), C-7 (D-135);
  - **debt:**

    | Finding | Owner |
    |---|---|
    | C-2: "gap" mixes not researched with refused as stale | S20 (the researcher product), raised again in S16's handoff |
    | C-5: the H100's age tally includes its recorded gap | S20 |
    | C-8: one source carries two access dates for the same bytes | S22 |
    | C-9: the two accelerators' links are not the same kinds | the session that next adds accelerator links |
    | E-1: a resolved recorded gap stops both builds | S22 |
    | E-2: an invalid citation standing crashes the HBM page build without a named reason | S22 |

- **Rejected:** fixing C-2 or C-9 in S16. Each needs a change to the first query's definitions or new
  research (S16 non-goals).

## D-139 — A research session on the HBM suppliers (S16.5) precedes S17

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** the S16 audit:
  - three metrics show "cannot be computed yet" because no source the Atlas holds names who supplies the
    HBM in the H100 or in Trainium2 (D-130, D-136);
  - S16's prompt forbade research to fill a gap;
  - the human asked that the system find such evidence itself rather than ask for it.
- **Decision:**
  - the next session, S16.5, researches the supplier of each incorporated HBM part from primary sources,
    under `source-policy.md` (the `rel:incorporates.supplier` row: time-sensitive, party standing);
  - Claude finds, extracts and verifies the evidence itself (Source Scout, Extractor, Verifier);
  - each supplier link is staged and becomes canonical only on the human's approval (Class C);
  - S16.5 designs the supplier metrics' presentation before any page is rebuilt with a named supplier
    (D-130's stop rule);
  - S17 (the policy entities) follows S16.5.
- **Rejected:** researching inside S16 (outside its contract); keeping the planned order (the gap stays
  debt).

## D-140 — The M3 and M4 milestone audits are written at S16.5's opening

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** PEF §4 requires a milestone audit at every major milestone. M3 (S11 to S13) has none, and M4
  (S14 to S16) closes with S16 without one (S16 report, "Unresolved issues"; H-1 C was not chosen).
- **Decision:**
  - S16.5 opens by writing both audits under `docs/architecture/milestone-audits/`, each answering PEF §4's
    eight questions, with a row each in `docs/quality/audit-history.md`;
  - the HBM supplier research (D-139) starts after them;
  - M4 closes as a milestone when its audit is written.
- **Rejected:** a separate short session after S16.5; leaving the session reports as the only record.

## D-141 — The HBM supplier research: both suppliers stay unknown; SK hynix's 2022 statement kept as evidence

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** `docs/research/hbm-supplier-research-original-rules.md`; the search log (28 queries, 51 retrievals).
  - **H100:** the only product-level statement by a party is SK hynix's press release of 2022-06-08
    (`src-053`): "HBM3 to be combined with NVIDIA H100 Tensor Core GPU". It is more than 12 months older
    than its verification, so F-1 refuses it as a supplier value.
  - **NVIDIA's FY2026 10-K** names its memory suppliers at company level only (ER-9; `cand-002`).
  - **Trainium2:** no party names the memory maker.
  - **Access gaps:** SK hynix's and Micron's filings could not be read (SP-7), so ER-3's search is
    incomplete for both parts.
- **Decision:**
  - both `supplier` fields stay `not_researched`, as ER-3 prescribes after a search with access gaps; the
    research is recorded in the findings document and the log;
  - SK hynix's 2022 statement becomes canonical evidence: source `src-053` and the `FACT` claim
    `claim-sk-hynix-hbm3-for-h100-2022`, reviewed and accepted by the human. It is linked to no edge or
    field, so no page and no metric changes;
  - the three supplier metrics stay "cannot be computed yet" (D-130, D-136). The presentation design of
    S16.5's H-3 was not needed.
- **Rejected:**
  - the research recorded only in documents (verified evidence would stay outside the queryable data);
  - SK hynix → H100 drawn as a recorded "evidence not fresh" gap, like `cand-001`. It would change the
    H100's coverage counts, and the refused-candidate model was not checked for a supplier qualifier;
  - SK hynix named as the supplier on stale evidence (F-1).

## D-142 — A claim's review may be recorded in a sub-session report

- **Date:** 2026-10-07 · **Status:** superseded by D-151 (2026-10-08); earlier: accepted (decided by the human on
  2026-10-07, with D-141)
- **Context:** `schemas/claims.schema.json` accepted `recorded_in` only as `SESSION-NN-REPORT.md`. A claim
  reviewed in S16.5 could not name its own session's report. D-126 had widened the repository validator,
  not the claim schema.
- **Decision:** `recorded_in` accepts D-126's optional one-digit suffix (`SESSION-16.5-REPORT.md`). Anything
  else stays refused. Checked by `tests/test_claim_schema.py`
  (`test_review_may_be_recorded_in_a_sub_session_report`), written first.
- **Rejected:** recording S16.5's review in S16's report (it would file the decision under another
  session's contract).

## D-143 — The supplier-evidence rules are revised in their own session (S16.6) before S17

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:**
  - D-141 left both HBM suppliers unknown;
  - sources other than the companies exist (market research, news, independent teardowns), but the
    `rel:incorporates.supplier` matrix row treats every such class as "never sufficient alone";
  - F-1 makes almost all evidence about a 2022 product stale by construction.
- **Decision:**
  - a session, S16.6, opens with a proposed revision of the supplier-evidence rules, put to the human as a
    `CLAUDE.md` §9A decision before any rule changes. At least two changes are proposed:
    - historical supplier values with a date and a validity period, outside the 12-month rule when
      marked as past;
    - an independent teardown as first-hand evidence of which maker's part a product contains;
  - the HBM supplier research is then redone under the rules as decided;
  - S17 follows.
- **Rejected:**
  - recording third-party reports only as attributed claims under the current rules;
  - leaving the rules unchanged.

## D-144 — Historical supplier values (R-1)

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** `docs/research/supplier-evidence-rules.md` R-1. F-1 treats a product's supplier as
  present-tense, so a dated past supply could not be recorded (D-141).
- **Decision** (`source-policy.md` §12, "Historical values of a `time_sensitive` row"):
  - a supplier assertion with `valid_to` states what its evidence supports up to that date. F-1 does not
    apply to it;
  - its evidence must be dated no earlier than `valid_to`, and no later than `valid_to` plus 12 months;
  - it must state the past, not a plan (ER-8);
  - pages show it with its period, never as current. The current state stays a separate question;
  - checks: `tests/test_freshness.py` (`HistoricalSupplierTests`, written first); no schema change.
- **Rejected:** keeping F-1 for every value.

## D-145 — An independent teardown as evidence of a product's part maker (R-2)

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** R-2. Only the two parties could support a supplier, and both are often silent.
- **Decision** (`source-policy.md` §2 `research_report`, §7.1; the matrix row `rel:incorporates.supplier`):
  - a teardown of the named product is `research_report` with `originator` standing, and acceptable for
    the row;
  - it must name the product and variant, and identify the maker from the unit;
  - it supports "the unit examined contained the maker's part", never every unit;
  - it is subject to D-147's criteria record;
  - checks: `tests/test_source_policy.py`.
- **Rejected:** keeping teardowns as never sufficient.

## D-146 — Retrieved sources are registered when retrieved (R-4)

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:** S16.5 found the Extractor's contract (sources straight to `data/sources.json`) in conflict
  with a prompt rule forbidding any `data/` edit before approval.
- **Decision:**
  - the contract governs. A retrieved source is registered in `data/sources.json` when it is retrieved;
  - claims and supplier values wait in staging until the human's review;
  - `docs/agents/contracts.md` says so in the Extractor's writes;
  - future prompts do not forbid it.
- **Rejected:** keeping drafts outside `data/` until approval, where the checks could not see them.

## D-147 — Third-party evidence for a product's supplier, under the human's criteria (R-5)

- **Date:** 2026-10-07 · **Status:** accepted (criteria set by the human on 2026-10-07;
  the "reported" label decided by the human the same day)
- **Context:**
  - the human's question whether sources other than the companies exist (S16.5), and the human's
    criteria for using them;
  - `source-policy.md` §9 kept market research and news never sufficient alone in every row.
- **Decision** (`source-policy.md` §7.1, §9; the matrix row; `schemas/claims.schema.json`):
  - the supplier row admits third parties (`research_report`, `market_research_consultancy`, `news_media`)
    under four criteria:
    - recency: preferably no older than 12 months, otherwise only as a historical value (D-144);
    - recognition: internationally recognised as reliable;
    - independence: no conflict of interest;
    - explicitness: any unmet criterion is stated explicitly;
  - each third-party citation carries `third_party_criteria` (`recognised`, `independent`, each `met` with a
    `reason`). V-10 refuses a third-party supplier citation without it;
  - a value resting only on third-party evidence is shown as **reported** ("reported by the publisher, on
    its date"), with any unmet criterion beside it, never as stated. This supersedes D-120's
    basis definitions (stated, inferred, gap) and D-128's coverage split, **when the first reported value
    exists**: the first query and the coverage metric gain "reported", designed and approved with that
    value's presentation (H-3);
  - every other row keeps §9's rule;
  - checks, written first: `test_source_policy.py`, `test_data_relationships.py`, `test_claim_schema.py`.
- **Rejected:** keeping third-party reports as attributed claims beside an unknown supplier; labelling a
  reported value "inferred".

## D-148 — How a reported supplier is shown (H-3)

- **Date:** 2026-10-07 · **Status:** accepted (the presentation chosen by the human on
  2026-10-07, H-3)
- **Context:**
  - the human approved two supplier values on 2026-10-07 (H-2): SK hynix for the H100's HBM, historical to
    2024-03, reported by TrendForce; Samsung Electronics for Trainium2's HBM, reported by SemiAnalysis, with
    its recognition criterion not met;
  - both page builds stopped as soon as a supplier was named (D-130), and D-147 asked for the "reported"
    label with its presentation;
  - the proposal and its mock-up: `docs/research/supplier-presentation.md`.
- **Decision:**
  - **the first query** (`sql/accelerator_dependencies.sql`): a named supplier is a row with its company. Its
    basis is **reported** when its claims include an `ATTRIBUTION` and no `FACT`. Two new columns: the
    period end (`period_to`, from `valid_to`, else `not_applicable`) and the unmet §7.1 criteria
    (`criteria_unmet`, read from the new `citation_criteria` table). Supersedes D-120's basis definitions;
  - **coverage** (`sql/evidence_coverage.sql`): a `reported` column. Stated + inferred + reported + gap =
    links. Supersedes D-128's split;
  - **the supplier metrics** (`sql/supplier_metrics.sql`): the status stays `cannot_be_computed_yet` until a
    metric's needs are met (a part's full supplier set, where each supplier makes it, a source stating one
    supplier only), not as soon as a supplier is named. Party-stated and reported suppliers are counted
    apart. The page shows each non-zero kind and never a zero one. Supersedes D-130's status rule. D-130's
    build stop stays for a status with no designed presentation;
  - **both pages:** a named supplier is drawn with its name, its basis in words, its period ("historical,
    to 2024-03") and each unmet criterion ("criterion not met: recognised"). The HBM page draws it as a
    dash-dot outlined box with a key line. The research view uses a double line or double border: its
    palette check (IN-7) forbids a new line pattern, so this differs from the mock-up's dash-dot there.
    The evidence panel shows both criteria with their reasons;
  - **the lane** (supersedes D-104's lane rule in part): SK hynix is now a reported supplier on the chain,
    so the lane's "not linked" note names only the facility and the product it holds ("the facility and
    product here: not linked to this chain"); the build still refuses a link from a lane facility or
    product to either accelerator;
  - **visual semantics:** `visual-architecture.md` §9 gains the "reported" and "historical" rows;
  - **checks, written first:** WH-3 (criteria reach SQL), WH-10, WH-12, WH-14 (independent computations
    with "reported"), PG-2, PG-5 (name, basis, period, key line), IN-3, IN-10, IN-13; the S16.6 break
    harness.
- **Rejected:** a coloured fill for "reported" (colour alone, and outside the palette); counting a reported
  supplier towards a supplier count (neither report says its maker was the only one); keeping the build
  stop for any named supplier.

## D-149 — The refused NVIDIA memory-supplier card links Samsung's new record

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:**
  - the refused candidate `cand-002` (NVIDIA's 10-K: "We purchase memory from SK Hynix Inc., Micron
    Technology, Inc., and Samsung") held Samsung as a firm with no record (D-111), one of its two reasons;
  - S16.6 created `company-samsung-electronics-co-ltd` (H-2), so the card contradicted the record the same
    page draws as Trainium2's reported supplier;
  - RC-4 matched a no-record name only exactly, so "Samsung" against "Samsung Electronics" passed.
- **Decision:**
  - `cand-002` names Samsung by its record ID and drops `endpoint_has_no_record`; its reasoning says when
    and why. It stays refused: the item, "memory", has no record (ER-9);
  - RC-4 also refuses a no-record name that is the start of a record's name, written first
    (`tests/test_data_candidates.py`);
  - on the HBM page the card moves from the "endpoint has no record" group to "item has no record" only.
- **Rejected:** leaving the card as it was, true to its 2026-10-02 ruling but contradicting the new record.

## D-150 — The full break harness runs at milestone audits

- **Date:** 2026-10-07 · **Status:** accepted (decided by the human on 2026-10-07)
- **Context:**
  - the merged harness had grown to 100 breaks. A full run takes three to four hours: each break rebuilds
    the pages and runs the whole suite, one after another;
  - S16.6 replaced twelve inherited breaks whose setup text had changed, and found one weak check through a
    break;
  - the harness tests the checks, not the evidence; content audits, cold readings, browser QA and the
    human's review cover the rest.
- **Decision:**
  - from S17, the full merged harness runs **only at a milestone audit** (the next is M5's, planned for
    S19);
  - a session in between runs the breaks that touch the files it changes, plus its own new breaks;
  - three improvements are kept as reminders in S17's prompt, for the human to schedule:
    - the most useful breaks become permanent tests with planted data inside the suite, run on every commit
      and in CI;
    - breaks are selected by the files a session touches;
    - breaks run in parallel, each in its own copy.
  - S16.6's own full run was completed as its prompt asked.
- **Rejected:** a full run in every session that changes checks or pages (the rule up to S16.6).

## D-151 — The public repository holds the current system; development records are kept privately

- **Date:** 2026-10-08 · **Status:** accepted (the boundary and the migration instructed by the human on
  2026-10-08; the condensed status lines and the search-log rule decided by the human the same day)
- **Context:**
  - beside the product, the repository held the full record of how it was built: every session prompt and
    report, a prompt registry, and per-session folders of screenshots, logs, fail-first outputs, one-off
    migration scripts and research notes;
  - three working parts of the system depended on that record: each canonical claim's `review.recorded_in`
    named a session report as the record of the human's verdict; Gate 0 checked only session file names and
    report headings; the break harness (D-150) and the browser QA scripts (D-106) lived in session folders.
- **Decision:**
  - **Boundary.** The public repository holds the current system: constitutional documents, current-state
    documentation, data, schemas, SQL, tools, tests, generated pages, and the evidence that accepted audits
    rest on. Session prompts, session reports, the prompt registry and per-session working files are kept in
    the human's private development archive, outside this repository (`SESSION-PROMPT-SPEC.md` §5, §6).
  - **Review provenance.** The human's verdicts are recorded in `docs/quality/human-reviews.md`, one entry
    per review, stating its outcome in project terms. `review.recorded_in` names the entry
    (`docs/quality/human-reviews.md#<entry>`, the anchor ending with the review date). Each of the six
    reviews maps one-to-one onto the report that held it; every verdict, reviewer and date is unchanged.
    Checked by `tests/test_claim_schema.py` (the form) and `tests/test_human_reviews.py` (HR-1 to HR-3: the
    entry exists, its date is `reviewed_on`, its stated claim count is the data's), written first.
  - **Gate 0** (`tools/validate_repo.py`) checks that the constitutional and governing documents exist and
    that every relative link in the repository's Markdown resolves. It no longer checks session files.
  - **Durable checks move to stable locations:** the break harness to `tests/regression/` (D-150 unchanged:
    its full run is for milestone audits); the browser QA scripts to `tests/browser/` (D-106 unchanged: run
    outside CI with the pre-installed browser; their results are reported, not committed).
  - **Audit evidence** that accepted audits cite moves to `docs/quality/audit-evidence/`; research and audit
    documents are named for what they cover, not for the session that wrote them.
  - **Search logs:** a search log that a public research document cites as its method is kept beside it,
    in `docs/research/search-logs/` (the Source Scout's contract), so a "searched and not found" result
    keeps its public record.
  - **This log is condensed once:** every entry's status line states its outcome and date only. The
    "Session" field and the human's quoted answers are removed; where an answer carried the outcome, the
    outcome is stated instead. Headings, decisions, contexts and evidence quotes are unchanged. This is the
    one exception to "append-only, never rewritten", made so the log follows D-114 (outcomes, not
    transcripts); new entries use the same form.
  - The bootstrap prompt (D-009) and the operational roadmap are removed; `SESSION-ROADMAP.md` remains the
    plan, unchanged.
  - References to renamed documents are updated in place. Paths under `sessions/` named in earlier entries
    say where a file was when the entry was written; they are not in the public tree. Git history keeps them.
- **Supersedes:** D-002; D-009 (the bootstrap prompt is no longer kept); D-126 (the validator's session-name
  rule); D-142. **Amends:** D-106 (the scripts are kept in `tests/browser/`).
- **Rejected:** keeping the reports public as the provenance of reviews (they expose the whole working
  process to cite one verdict); dropping `recorded_in` and keeping only the verdict and date (loses where
  the review is recorded); a public archive of the same files under new names; rewriting Git history (a
  separate publication decision, not taken here).

## D-152 — Every session archives its own records in the private archive repository

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Context:** D-151 moved session prompts, reports and working files out of the public repository into a
  private development archive, but named no place and gave no session the task of filling it. The human
  created the private repository `andreatosti2001/atlas-dev-archive` and asked that every session copy there
  what belongs there.
- **Decision:**
  - every development session works with `atlas-dev-archive` attached. At its start it commits its prompt
    there verbatim and reads the previous report from there; at its end it commits its report and its
    private working files there, and its final message gives the archive commit (`CLAUDE.md` §4, §17;
    `SESSION-PROMPT-SPEC.md` §5 lists what goes where);
  - a session that cannot attach or push to the archive stops and asks the human; it never falls back to
    the public repository;
  - Gate 0 fails if a session prompt, a session report, the prompt registry or a `sessions/` folder is
    committed to the public repository (`tests/test_validate_repo.py`, written first).
- **Not changed:** what is public (D-151); the report's minimum fields; the decision log, the human review
  record and the search logs stay public.
- **Rejected:** leaving the archive to the human by hand (records get lost between sessions); an automated
  copy from CI (it would need the public repository to hold the records first, or a secret with write access
  to the private one).

## D-153 — The first policy records are export controls; the harness improvements open the M5 audit

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Context:** S17 opens the policy layer (M5). Its prompt asked which kind of instrument to model first,
  and when to schedule the three harness improvements kept as reminders by D-150.
- **Decision:**
  - the first policy records are **export controls** on advanced AI chips, high-bandwidth memory,
    chipmaking tools and chip-design software: the US Bureau of Industry and Security's rules, read from the
    Federal Register. The record design must still hold other kinds of instrument later;
  - the three harness improvements (permanent fast tests with planted data, breaks chosen by the files a
    session touches, breaks run in parallel copies) are **the first task of the M5 audit (S19)**, before
    its full harness run. S17 and S18 choose their breaks by hand (D-150).
- **Rejected:** public support for chip and memory plants first (it bears on companies and plants more
  than parts, and an EU programme would need a supranational jurisdiction); a few of each kind (thinner
  coverage and twice the research); building the harness improvements in S17 (a large engineering task
  in a session that opens a new layer); leaving them to the engineering audit S22 (the M5 audit's full run
  would take hours).

## D-154 — Which policy instruments the Atlas records (P-1)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Context:** M5 opens the policy layer. `Eu-Digital-Policy` owns EU digital regulation (it holds 24 EU
  instruments, among them the EU Chips Act and the Cloud and AI Development Act, as read on 2026-10-08), and
  `Global-AI-Governance` owns comparative governance (NG-02).
- **Decision:** the Atlas records a policy instrument only when its text names an item, technology or firm
  class of the chain and it is an industrial, trade, export-control, investment or public-support measure;
  never an instrument another portfolio product owns, and no comparative-governance content (no provisions,
  obligations, enforcement or institution profiles). A policy's issuing jurisdiction must be a `country`
  record (PL-3), so no EU instrument can be recorded until a decision creates a supranational jurisdiction.
  `docs/architecture/policy-dataset.md` P-1.
- **Rejected:** bare records of EU instruments by reference (a supranational jurisdiction now, and a second
  home beside `Eu-Digital-Policy`).

## D-155 — The policy record: one published act, seven sourced fields (P-2, P-3)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** `policy` becomes an instantiable entity type (supersedes the reservation of policy in D-022
  and D-023; `institution` stays reserved). One record is one officially published act: a rule in an official
  journal, or a codified regulation as a whole. Identity is the official publication identifier; the ID is
  `policy-<ISO code of the issuing jurisdiction>-<identifier slug>` (PL-2). Fields: `official_title`,
  `official_citation`, `issued_in`, `issuing_authority`, `instrument_form` (`codified_regulation`,
  `interim_final_rule`, `final_rule`, `proposed_rule`), `measure_kinds` (`export_control`; further kinds come
  with their first record), `amends`, each claim-backed. No status, date, summary, content, "applies to" or
  notes field. MA §6.1 `PolicyInstrument` and `TradeMeasure` are `type:policy`; `ExportControl` is the
  measure kind `export_control`. Schema: `schemas/entities.schema.json`; checks PL-1 to PL-5.
- **Rejected:** one record per policy area (no single text); one record per provision (governance content,
  D-023); records without `amends`.

## D-156 — A policy's dates are events; its status is derived (P-4)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** three event types with a policy subject: `published`, `effective` (one per date the act
  fixes; the proposal's working name was "took effect") and `repealed` (only from a repealing text or the
  authority's official notice of the repeal). `announced` may have a policy subject and never moves the status
  (ER-8). `tools/policy_status.py` derives the status on any date: `has_taken_effect`,
  `published_not_yet_in_effect`, `not_yet_published` (the act did not exist yet on that date; added when the
  tool was written), `repealed`, `proposed`, `indeterminate`, `no_recorded_effect`. A `proposed_rule` never
  has an `effective` or `repealed` event (PL-6). The order of publication and effect is not checked. The
  Atlas says "has taken effect; no repeal recorded in the Atlas", never "in force".
- **Rejected:** a stored status (a second home that goes stale); a dated search for later repeals on every
  record with a 12-month staleness rule (kept as a possible later strengthening).

## D-157 — Normative text: no new claim type (P-5)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** settles `claim-model.md` §2's reserved row. What an act's text fixes about itself (identity,
  citation, form, publication, the dates it fixes, what it amends) is `FACT`, with the issuing authority as
  `originator`; what the act provides is `ATTRIBUTION` to the issuing authority. A policy record cites only
  `FACT` and `ATTRIBUTION` claims (PL-5).
- **Rejected:** every policy claim as `ATTRIBUTION` (the occurrence rule EV-2 would have to change); a sixth
  claim type `NORMATIVE` (rules in every table for no different treatment).

## D-158 — A source class for official legal texts (P-6)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** a twelfth class, `official_legal_text`: the act itself as an official journal or code
  publishes it. It is the only preferred class of the eleven policy rows of `source-policy.md` §7
  (`identity:policy`, seven `attr:policy.*`, `event:published`, `event:effective`, `event:repealed`);
  `government_publication` is acceptable only for `issuing_authority` and `measure_kinds`, and never
  sufficient alone for the dates and the repeal. Every row that existed before places the new class under
  "never sufficient alone", so no earlier check is loosened (PL-8). The matrix has 47 rows.
- **Rejected:** keeping official texts as `government_publication` (a press release could date or repeal an
  act).

## D-159 — Institutions stay reserved; the issuing authority is text (P-7)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** `institution` stays reserved (D-022). A policy's issuing body is the sourced text field
  `issuing_authority` until a link needs an institution record.
- **Rejected:** institution records now (a second new record type with no use yet, and drift toward
  `Global-AI-Governance`'s institutions).

## D-160 — The links S18 may record (P-8)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** settles D-030's four reserved verbs. `restricts` (policy → component, technology, product or
  company) is defined: evidenced only by the act's own text naming the target, or a party stating that the
  act applies to its own product; matching a text's term to an Atlas class is a separate `DERIVATION`; never
  the Atlas applying a threshold. `supports` (policy → company or facility) is defined, instantiable only
  when a session records public-support instruments. `regulated_by` and `constrained_by` are rejected as
  vague (RR-10). Links are stored from the policy to its target; MA's `restricted_by` and `supported_by` are
  the inverse readings. S18 adds them to the schema and amends RR-2 for a policy level; until then no
  relationship has a policy endpoint (PL-9). The definitions' one home is `policy-dataset.md` P-8.
- **Rejected:** `restricts` alone with `supports` left undefined.

## D-161 — Description, never advice (P-9)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** five rules for every policy record, claim, link and page (LA-1 to LA-5 in
  `policy-dataset.md` P-9): the Atlas states only what a text says and the dates it fixes; only an S18 link
  may say an act bears on a firm or product; no threshold, definition or exemption is applied to a product;
  "in force", "legal", "compliant", "licence required" and "prohibited" never appear in the Atlas's own voice;
  every display links the official text and says it describes and does not advise. LA-1 is checked (PL-5),
  LA-2 by the schema; LA-3 to LA-5 are review rules.
- **Rejected:** a check banning the words in claim statements (false alarms on quoted text).

## D-162 — The policy layer's checks are written first, with breaks (P-10)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** PL-1 to PL-9 are written before the schema changes and shown failing for their reasons;
  each gets a planted-fault break (`S17-…`) in `tests/regression/`, run with the breaks that touch the
  changed files (D-150).
- **Rejected:** writing S17's breaks at the M5 audit.

## D-163 — The first export-control records (P-11)

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Decision:** S17 researches five acts: the Export Administration Regulations as a whole (15 CFR parts
  730-774) and the BIS rules of 13 October 2022 (87 FR 62186), 25 October 2023 (88 FR 73458 and 88 FR 73424)
  and 5 December 2024 (89 FR 96790), each from its official text, put to the human record by record.
- **Rejected for now:** the August 2022 chip-design software rule (87 FR 49979) and the January 2025 AI
  Diffusion rule (90 FR 4544).

## D-164 — An effective date the act fixes in advance comes from the act itself

- **Date:** 2026-10-08 · **Status:** accepted (decided by the human on 2026-10-08)
- **Context:** found while writing the checks. Rules usually fix their effective date in advance (published
  25 October 2023, effective 17 November 2023). EV-3 refuses an event dated after the source that states it,
  which is right for observed occurrences.
- **Decision:** an `effective` event may be dated after a citation whose source is the act's own official
  text (an `official_legal_text` source cited by the subject policy's identity claims): an act's effective
  date is fixed by its publication, not observed later. EV-3 applies unchanged to every other event and
  every other source (`tests/test_data_events.py`). The status wording stays "has taken effect on the date its
  text fixes; no later act changing it recorded in the Atlas".
- **Rejected:** counting a future effective date only once a later official text confirms it (more research
  per record; acts would stay "not yet confirmed").

## D-165 — The first policy links go to the classes the texts name

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Context:** S18 opens the links between the five export-control records and the chain (D-160). Read
  before the decision, in the five texts re-retrieved on 2026-10-13 with their registered hashes: none names
  any of the Atlas's nine companies or three products. 89 FR 96790 adds a control "on HBM stacks", and the
  equipment rules name semiconductor manufacturing equipment.
- **Decision:** the first `restricts` links go from the acts to the **classes** of parts and technologies
  their own texts name. No named product or company is linked in S18.
- **Rejected:** named products and companies first (each needs the party's own statement that a specific
  rule applies to its product; none is retrieved, and none may exist); both kinds in one session (twice the
  research and review, with the product half possibly empty).

## D-166 — A policy level for `restricts`, with class targets only (K-1)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** `restricts` is the only type of a third level, `policy`: from a named act to a class its own
  text names, evidenced by that text, with no dates on the link. RR-2 names three levels; RR-9 admits a
  policy only as the source of `restricts`. Targets admitted now: component and technology. Product and
  company targets (defined by D-160) are admitted by the session that records the first one, with their
  evidence row. Schema: `schemas/relationships.schema.json` (`rel_restricts`, `endpoint_policy`); checks PK-1,
  PK-2. `docs/architecture/policy-links.md` K-1.
- **Rejected:** all four target kinds now (an evidence row written before any party statement is read); two
  verbs (one relation split in two, although the evidence is the same text).

## D-167 — A link needs the act's own term for the record's class (K-2)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** a link is recorded only when the act's text uses the record's name or an alias and nothing
  in the text makes it a different kind of thing. Words that limit which members are controlled ("certain",
  "specified", a parameter) are scope. A `DERIVATION` with two inputs (the act's `ATTRIBUTION` and the
  record's working-definition claim) quotes both words and concludes only that they name the same kind of
  thing: never that every member, a product or a firm is controlled, for which destination, or that the
  control is in effect. A broader term ("GPUs" for data-centre GPU), a narrower one, or an item used for the
  class (EUV pellicles for EUV lithography) is refused as `term_not_matched`. Check PK-3, PK-4.
- **Rejected:** accepting a broader term that contains the record (each link would say more than the text;
  ER-9 already refuses that step for suppliers).

## D-168 — A control's scope stays in the text (K-3)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** no qualifier on `restricts`. Parameters, destinations, licence policy and exclusions stay in
  the act, quoted where a claim needs them. The link reads "the text of <act> names <class> among the items
  it controls"; the inverse reading shown is "named among the items controlled by".
- **Rejected:** structured scope fields (legal content copied into fields, stale with every amending rule,
  and an invitation to the threshold comparisons LA-3 forbids).

## D-169 — A later change to the same entry is quoted, never dated on the link (K-4)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Context:** 88 FR 73424 (2023) removes ECCN 3B090, the equipment entry 87 FR 62186 (2022) created.
- **Decision:** a link has no dates; the act's status comes from its events. A later act the Atlas holds that
  changes the same entry is one more `ATTRIBUTION` claim cited by the earlier link, quoting the later text.
  Later acts the Atlas holds are searched for the entry's identifier and the search is logged; acts it does
  not hold are not searched, which is debt for the M5 audit. An amendment of an entry is not a repeal of the
  act.
- **Rejected:** an end date on the link (the Atlas's own inference about legal effect); refusing a link whose
  entry was later removed (it would lose what the earlier text named).

## D-170 — No jurisdiction relationship (K-5)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** S18 adds no relationship to a jurisdiction. An act's issuing country is its `issued_in`
  field (RR-4); the destinations a control names are scope in the text (D-168).
- **Rejected:** none proposed.

## D-171 — The evidence row `rel:restricts` (K-6)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** a 48th row in `docs/research/source-policy.md` §7: preferred `official_legal_text`,
  acceptable none, every other class never sufficient alone; standing originator; freshness stable. The
  session that admits product or company targets revisits it. Check PK-5.
- **Rejected:** none proposed.

## D-172 — Refused policy candidates are records, with two new reasons (K-7)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** a policy-link candidate the evidence cannot support is a refused candidate (D-109). The
  schema admits `restricts` and a policy source in a candidate, and two reasons: `term_not_matched` (D-167)
  and `applies_a_threshold` (LA-3). One product candidate is recorded as refused: 89 FR 96790 states that
  all HBM stacks in production exceed its threshold, and linking Micron's HBM4 on that ground would be the
  Atlas applying the threshold. Check PK-7.
- **Rejected:** class refusals only (the threshold temptation would be documented only in prose); refusals
  only in the search log (not checkable data).

## D-173 — Pages show no policy link; navigation shows each with its act's status (K-8)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** no page shows a policy link or a policy record until a page design is approved; a check
  fails if a built page contains one. `tools/navigate.py` reads the policy records; `depends-on`,
  `suppliers` and `actors` never return `restricts`; `edges` shows each policy link with its act's status
  on a date (derived by `tools/policy_status.py`, default today, never stored), the act's official text and
  the line "describes the text; does not advise" (LA-5). Check PK-6.
- **Rejected:** navigation ignoring policy links (they would answer no question from the tools).

## D-174 — The policy link's checks are written first, with breaks (K-9)

- **Date:** 2026-10-13 · **Status:** accepted (decided by the human on 2026-10-13)
- **Decision:** PK-1 to PK-7 (`policy-links.md` K-9), shown failing for their reasons before the schema
  changed, replace S17's PL-9; RV-1 gains a `restricts` word row (`edge-dataset.md` §7). Each check gets a
  planted-fault break (`S18-…`) in `tests/regression/`, run with the breaks that touch the changed files
  (D-150).
- **Rejected:** none proposed.

## D-175 — The M5 audit records the later-rule gap; it does not search

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-13, S19 H-0)
- **Context:** each `restricts` link and each act's status say "no later change recorded in the Atlas"; the Atlas
  has not looked for BIS rules after 5 December 2024 that change entries 3A090.c, 3B001, 3B002 or 3B993 or
  repeal one of the five acts (S17 and S18 debt; D-156, D-169).
- **Decision:** the M5 audit records the unsearched period as a finding with an owner
  (`docs/architecture/milestone-audits/M5-audit.md`). No search, no new record, no data change in S19.
- **Rejected:** a dated search of the Federal Register's official texts now (a research step and a review inside
  an audit session, with likely new records).

## D-176 — Permanent planted-fault tests: 28 breaks on every commit

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-1; D-153)
- **Decision:** `tests/test_planted_faults.py` runs 28 of the harness's breaks inside the suite, so on every push
  and in CI. Each applies the break's own setup (one home: `tests/regression/breaks.py`) to a temporary copy of
  `data/`, runs the record checks in memory and passes only if every fragment the break expects is among the
  errors, and none is among the real data's errors. Criterion: the break plants a fault in the records; its setup
  edits `data/` only and its fault is named by a check's message; its setup finds the records by ID. The harness
  keeps the 28. The CI workflow is unchanged (it runs the suite). Added time: about 3 s.
- **Rejected:** only the 15 policy-layer breaks (older data checks unguarded between audits); no per-commit tests.

## D-177 — Breaks are selected by the files they measurably touch; a check change runs the full harness

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-1; amends D-150)
- **Decision:** `breaks.py --changed PATH ...` or `--since REV` selects a break when a file its setup changes
  (measured on a scratch copy, never declared) or a tool its build steps run is among the changed files. A change
  to a check module (`tests/test_*.py`), a schema, Gate 0 (`tools/validate_repo.py`) or the harness
  (`tests/regression/`) selects the full harness. D-150's milestone full run stays.
- **Rejected:** measured selection with D-150 unchanged (a loosened check outside the selected breaks would wait for
  the next milestone audit); declared file lists (they drift from what a setup edits).

## D-178 — The harness runs breaks in parallel copies, with one combined result

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-1)
- **Decision:** `tests/regression/runner.py` (standard library only, D-003) runs `--jobs N` breaks at a time (default:
  the processors), each in its own numbered copy (four S13 IDs name two breaks each), prints the lines in the
  harness's order and one summary (faults caught as named, controls passing, stale setups). The method and the
  pass rule of each break are unchanged.
- **Rejected:** one break at a time, split across processes by hand.

## D-179 — The new harness is accepted only on an identical verdict for every break

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-1)
- **Decision:** the old runner and the new one run all 130 breaks on the same tree; every break's verdict and set of
  failing tests must be identical, or the session stops. The new runner's run is M5's full run (D-150). Each
  permanent test is shown failing with the checks disconnected and against a check loosened on purpose.
- **Rejected:** a sample of about 20 breaks.

## D-180 — Every file has an owner, checked

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2; agent audit F-2)
- **Context:** 63 files changed since S06 lay in no active role's `ALLOWED_WRITES`, and nothing checked the
  sentence "a role writes only its allowed paths" (`docs/architecture/agent-audit.md` F-2).
- **Decision:** `docs/agents/contracts.md` names an owner for every path: a role's `ALLOWED_WRITES`, or the new
  list "Outside every contract" (the constitutional documents, `docs/agents/`, the canonical data files moved on the
  human's verdict, `docs/quality/human-reviews.md`). `tests/test_agent_contracts.py` fails if a tracked file has no
  owner, or if an entry of that list owns no file. A path ending in `/` covers its folder; `*` matches within one
  name.
- **Rejected:** correcting the lists once without a check (they drifted unnoticed from S12 to S18); debt for S22.

## D-181 — The Analyst is active, with a contract

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2; agent audit F-3)
- **Decision:** the Analyst writes `sql/*.sql`, `sql/results/` (only through `tools/warehouse.py`), `sql-layer.md`,
  `metrics.md` and `analytical-audit.md`; its gate is `tests/test_warehouse.py` and `tests/test_insight.py`; it never
  writes `data/`, a result by hand, the loader or the checks, or a metric without its question, population and
  denominator. The active set is eight roles.
- **Rejected:** the Data Auditor absorbing the SQL work (the role that writes the checks would also write the
  analysis they check).

## D-182 — The Verifier's authority is the re-read; the human's review is the independent check

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2; agent audit F-4)
- **Decision:** the Verifier's contract and row say that its authority is the re-read of each anchor in the bytes
  whose hash is the registered one, by a script whose output is kept, plus a written list of wording that exceeds its
  anchor; when the drafting session also verifies, the human's review of every claim is the independent check.
  Debt: a durable re-read tool in `tools/`, owned by the next session that adds claims from a new retrieval.
- **Rejected:** merging the Extractor and the Verifier (the rule that the checker may not edit a claim's wording or
  anchor would go); leaving both contracts unchanged.

## D-183 — Drafts always land in staging

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2; agent audit F-1)
- **Context:** S16.5 and S16.6 held drafts in private research folders and wrote them to `data/` after the human's
  verdict, so the record checks did not run on them before the review.
- **Decision:** the Extractor's contract states that drafts always land in `data/staging/` before the human's review,
  and that a session prompt cannot keep them elsewhere. How claims become canonical is unchanged. No check (Git
  history is not checked in CI).
- **Rejected:** recording the two sessions as exceptions only.

## D-184 — The inactive roles: no runtime; the Change Detector's first task; who writes milestone audits

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2; agent audit F-5, F-6, F-8)
- **Decision:** `docs/agents/roles.md`:
  - **Orchestrator:** no runtime, dispatcher, queue or autonomous write path is justified; NG-08 holds for v1.0. The
    session prompt and the human coordinate;
  - **Change Detector:** stays inactive; its first task is D-175's dated search for later rules changing the acts the
    Atlas holds, no earlier than S20. S07's freshness rule is a check, the Data Auditor's;
  - **Portfolio Reviewer:** stays inactive until S24; the Knowledge Architect writes milestone audits, and the human
    accepts their findings and ratings.
  The Source Scout, Extractor, Knowledge Architect, Data Auditor, Editorial and QA are kept; Client Output stays
  inactive until S21.
- **Rejected:** recording the Orchestrator's outcome only.

## D-185 — The edge check PL-1 becomes PN-1

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2; M5 audit M5-P3)
- **Decision:** the S10 edge guard "a product edge names the product" (`edge-dataset.md` §7) is PN-1; PL-1 means only
  the policy record's shape (`policy-dataset.md` P-10). Earlier decisions keep their wording.
- **Rejected:** leaving both for S22.

## D-186 — The edge fixture world's source is `src-919`

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2; M5 audit M5-P3)
- **Decision:** `tests/fixtures/edge_records.json` names its fictional source `src-919`, so no ID is defined twice
  across the fixture worlds (`src-917` stays the entity world's).
- **Rejected:** leaving it for S22.

## D-187 — M5 closes with its audit

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S19 H-2)
- **Decision:** `docs/architecture/milestone-audits/M5-audit.md` and `docs/architecture/agent-audit.md` are accepted
  as written, with the remediations D-180 to D-186 done in S19 and the debt owners of the M5 audit's Part 1 §6. M5
  closes; S20 opens M6.
- **Rejected:** keeping M5 open until the human has read both documents.

## D-188 — The harness's documentation does not select the full harness

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, after S19; amends D-177)
- **Context:** D-177 selects the full harness for any change under `tests/regression/`. S19's last commit, a
  correction to that folder's README, therefore cost a 35-minute full run, though no check reads the README.
- **Decision:** the trigger covers the harness's code only (`tests/regression/*.py`), with the check modules, the
  schemas and Gate 0 as before. A change to `tests/regression/README.md` selects the breaks whose setup touches it
  (none today); Gate 0 still checks its links on every push. `tests/test_break_selection.py` checks the trigger.
- **Rejected:** keeping D-177 as it was (a full run for every edit of the harness's documentation).

## D-189 — A first page view of the policy links in S20

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-0; amends D-173)
- **Context:** no page showed a policy link (D-173, PK-6); the M5 audit lists this as a limit a UX must show
  (`M5-audit.md` Part 1 §8).
- **Decision:** S20 builds a first page view of the policy links. The check that no page shows a policy link or
  record (PK-6) is replaced by checks for that view (D-191); the HBM page and the research view still show none.
- **Rejected:** keeping the journeys on the supply chain and the policy links tool-only.

## D-190 — The research journeys S20 builds

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1)
- **Decision** (`visual-architecture.md` §15):
  - the roadmap's six journeys are answered by: the two built pages (explore a dependency); a new export-control
    page (compare layers, and a temporal relationship in a timeline, D-191); 9 company pages and 4 place pages
    (D-192); the evidence panels on every page (inspect evidence); and an entry page (D-193);
  - pages live at `site/index.html`, `site/questions/export-control-texts/`, `site/companies/<id>/` and
    `site/places/<id>/`; the two built pages keep their paths;
  - one build `tools/build_journeys.py`, subclassing `build_page.Page`, writes the 15 new pages from canonical
    records, one committed SQL cell (the as-of date) and the template `tools/journey_template.html`; no script, no
    dependency; checks JR-1 to JR-12 (`tests/test_journeys.py`);
  - what the records cannot answer is said on each page's method layer, never filled with framing.
- **Rejected:** one build per page kind; a search box (needs a script); diagrams on profiles; a map; moving the two
  built pages.

## D-191 — The export-control page

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1; amends D-109 and
  D-124 for this page only)
- **Decision:**
  - **a matrix** of the acts (rows) by every class or product that a policy link or a policy refused candidate pairs
    with an act (columns). A cell is "named in the text" (a link), "refused" with its reason in words, no line and no
    mark (a refused candidate; **amends D-109 and `visual-architecture.md` §9 for this matrix**: a refusal may appear
    in a visual as a word in a cell, linked to its card), or "no recorded relationship";
  - **each act's status** on the as-of date is derived by `tools/policy_status.py`, the one home of the rule
    (D-156), shown with the date and the rule's name; **amends D-124 rule 3 for this page**: a status derived by
    that tool is allowed beside the copy, tally, minimum–maximum and grouping. The check recomputes it with the same
    module;
  - **the as-of date** is the source-age reference date, read as a cell of `sql/results/source_age.json` (D-137);
  - **a timeline** of the acts' `published` and `effective` events, with the as-of date marked;
  - **a cross-layer comparison:** each class of the HBM chain with its policy state;
  - **wording** (LA-1 to LA-5, K-3): every act shows its official text link and the line that the page describes
    and does not advise; status words are P-4's only; "in force", "compliant", "licence required", "prohibited",
    "banned" and "restricted" never appear in the Atlas's own voice;
  - **PK-6** becomes: the HBM page and the research view show no policy ID; the export-control page and the
    United States place page show policy records only with the official text link and the no-advice line (JR-6).
- **Rejected:** refusals only as cards (a cell would read "no recorded relationship" where the Atlas holds a
  refusal); dates without a status; a SQL re-implementation of the status rule (a second home).

## D-192 — Company and place profiles

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1)
- **Decision:** one page per company record (9) and per jurisdiction record (4), in the seven layers
  (`visual-architecture.md` §15.4): record values with their state words; links, supplier namings, products,
  refused candidates (as cards, never links) and events; tallies of the rows drawn, never a bare zero; evidence
  panels; a table with every ID; what the page cannot answer. "Gap" is never counted on these pages.
- **Rejected:** no profiles in S20.

## D-193 — An entry page, linked from the built pages

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1)
- **Decision:** `site/index.html` asks "What are you trying to understand?" and links every research page; the HBM
  page and the research view each gain one link to it (a fixed label).
- **Rejected:** no entry page.

## D-194 — C-2: the coverage block names each gap's reason

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1; settles C-2, D-138;
  supersedes the rejection of this wording in D-133)
- **Decision:** on the research view, the coverage block's gap count is followed by each gap's reason in words,
  grouped from the first result's `gap_reason` column (D-124 rule d). The first query's definition of the basis
  `gap` is unchanged.
- **Rejected:** splitting `gap` into two bases in the first query; leaving it as debt.

## D-195 — C-5: the age tally leaves out recorded gaps, and says so

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1; settles C-5, D-138)
- **Decision:** on the research view, the age block tallies the dated links whose basis is not `gap`, and states
  beside the tally how many recorded gaps it leaves out. `sql/source_age.sql`, its result and the age table are
  unchanged.
- **Rejected:** giving a refused link no age in the query (a change to the metric's definition); leaving it as
  debt.

## D-196 — The research view's CSS filter is kept

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1)
- **Context:** S20's probe: in Chromium the filter works from the keyboard; without `:has()` it shows every row,
  but the control still changes; no keyboard or screen-reader failure was demonstrated; Firefox and Safari were
  not run.
- **Decision:** no change. The probe goes to S20.5 as baseline evidence; cross-browser runs go to S22.
- **Rejected:** a framing sentence about older browsers; a script.

## D-197 — Owners of the journey files

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20 H-1; D-180)
- **Decision:** the Data Auditor owns `tools/build_journeys.py`, its checks and the 15 pages, each written only by
  that build; the Editorial owns the framing and style of `tools/journey_template.html`, as for the two existing
  templates.
- **Rejected:** the Editorial owning the build and pages.

## D-198 — A design pass on the research journeys, within the accepted rules

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20, after reviewing the pages)
- **Context:** the pages built under D-190 to D-193 passed every check, but read as technical documents: the
  answer below the fold, a matrix of small words with no visible pattern, an entry page of link lists, a sparse
  timeline with overlapping dots, and repeated framing boxes.
- **Decision** (`tools/journey_template.html`, `tools/build_journeys.py`), within V-1 to V-11, the palette and
  system fonts, with no script and no new dependency:
  - each page leads with the answer: a row of stat tiles (each number with its unit and denominator in the same
    line) and the findings as sentences;
  - the matrix shows its pattern at a glance: a "named" cell is tinted with a filled mark, a "refused" cell
    hatched with an outlined mark, an empty cell plain; every cell keeps its words;
  - the timeline is larger, with year bands, and stacks events closer than one dot's width downwards in their
    lane (a beeswarm: x is the date, y only the stacking);
  - the entry page's cards are equal, each with what its page shows and a button; companies and places as chips;
  - profiles open with a summary card and stat tiles; refused candidates are neutral cards (amber stays for gaps);
  - explanations of how to read a visual are folded into "How to read …" toggles; limits stay visible;
  - JR-3 also recomputes the number of classes named (`named-classes`).
- **Rejected:** hiding evidence panels behind a toggle and adding a web font or colour accent (each would change
  an accepted rule; the human chose a pass within the rules); leaving the design to S20.5.

## D-199 — S20.5 runs between S20 and S21

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, at the close of S20)
- **Context:** the human's addendum to S20 announced S20.5, a frontend architecture assessment and framework
  decision; S20 left its baseline and handoff, and recommended deciding its place before S21 adds client briefs.
- **Decision:** `SESSION-ROADMAP.md` gains S20.5 (ARCHITECTURE) between S20 and S21 in M6, with its mission, inputs
  and gate. S21 starts after S20.5. Its prompt is in the private archive (D-152).
- **Rejected:** folding the assessment into S22 and starting S21 on the current stack (a later change of stack
  would then also touch the briefs).

## D-200 — The Atlas keeps its script-free generated pages; the research view's filter is hidden where it cannot work

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S20.5 H-1; amends D-196)
- **Context:** S20.5 assessed whether the Atlas should keep its pages, adopt Vue.js in one bounded place, or defer.
  The 17 pages hold no script and load nothing; their only interactions are links, disclosures and one CSS radio
  filter; no recorded user question needs state in the browser. The page checks prove each text node's provenance
  by reading the committed HTML, which text drawn by a script in the browser never reaches; Vue keeps that only by
  drawing nothing or by rendering on a Node.js build in place of the Python builds. One defect was shown: where a
  browser does not support `:has()`, the filter's radio still changes and silently does nothing.
- **Decision:**
  - the pages stay static, script-free and generated by the Python standard-library builds; U-8, V-10, NG-07 and
    D-003 are unchanged;
  - the research view's stylesheet hides the filter where `:has()` is unsupported
    (`@supports not selector(:has(*))`), so every row stays shown and no control misleads; checked by IN-14;
  - the debt observed in S20 goes to the sessions that own it: Python-version and build-code hygiene, browser
    checks in CI and visual regression to S22; one composition mechanism for templates to S21, when it adds one;
    a single home for each claim's evidence (`evidence/<claim>/`) to a later UX session;
  - a framework is reconsidered only when a recorded user question needs state in the browser that CSS and native
    elements cannot hold (search across records, a filter driving several views), and browser checks run in CI so
    that text drawn in the browser can be checked.
- **Rejected:** Vue.js on the research view's filter (a script and a dependency on a page that needs neither, and
  text the CI checks could not see); no change (the filter would keep failing silently).

## D-201 — After v1.0: a v1.5 for visual intelligence, then a v2 for the global chain

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, after S20.5)
- **Context:** S20.5 found that the Atlas's pages are far from the benchmark products' look (D-122), chiefly
  because the Atlas holds almost no quantitative data and covers one path of the chain (15 of the 40 first-version
  concepts of its domain map recorded, 5 with a supply-chain link), and partly because of design and the no-script
  rule. Widening coverage was estimated at about 30 to 35 sessions.
- **Decision:**
  - v1.0 completes as planned (S21 to S25), with its non-goals frozen until S25 (D-021);
  - **v1.5** follows, focused on visual intelligence: infographic layouts, an overview dashboard, reusable visual
    components and interaction, at the benchmark's quality, within v1's coverage plus one measured-data slice inside
    the current scope; its opening session decides the rule changes it needs (scripts, hover, a chart layer or
    framework, browser checks in CI, a record kind for measured values);
  - **v2** follows, covering the global AI infrastructure chain with v1's method; its opening session decides the
    coverage non-goals, the v2 domain map, new record types, review capacity and agent workflows;
  - the plan is kept in `VERSION-ROADMAP.md` (a constitutional document, beside `SESSION-ROADMAP.md`); its session
    lists are provisional and enter `SESSION-ROADMAP.md` when each version opens.
- **Rejected:** widening coverage before v1.0 (it would reopen frozen non-goals and delay the release); folding the
  visual work into v2 (the visual gap is visible now, and v2's presentation at scale needs v1.5's components).

## D-202 — The first client brief: its question, scope and form

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S21 H-0)
- **Context:** the S21 roadmap entry ("a reproducible, evidence-backed technology dependency brief from a defined
  question and scope"); MA §20; `CLAUDE.md` §13; U-5; D-200 (the stack).
- **Decision** (`docs/architecture/client-brief.md` §1):
  - the brief answers "What does an AI accelerator's memory depend on, who is reported to supply it, and which
    recorded export-control texts name those parts?" ("reported", not "known": both supplier namings rest on
    third-party reports, D-148);
  - its scope is the dependency result (`sql/results/accelerator_dependencies.json`: the two accelerators recorded,
    their memory, its reported suppliers, the recorded fabrication gap, the process the memory requires) and the five
    recorded US acts, read on the as-of date; what is out of scope is stated in the brief;
  - it is one printable, script-free page in the current stack, `site/briefs/accelerator-memory/index.html`; printing
    to PDF is the reader's browser's.
- **Rejected:** the memory chain alone and the export-control texts alone (each repeats an existing page); a
  Markdown export (a second output and check for no new capability); a PDF (a new dependency against D-003 and
  D-026, and timestamped bytes against the identical-rebuild check).

## D-203 — The brief's design: twelve sections, a summary composed from groups and tallies, five classes compared

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S21 H-1)
- **Context:** D-202; `CLAUDE.md` §13's nine sections and the roadmap's six outputs; V-2 (a summary sentence no
  check can recompute is not allowed); D-124; D-175; NG-12; the Boundary of the S21 roadmap entry.
- **Decision** (`docs/architecture/client-brief.md` §2 to §5):
  - twelve sections: question and scope, executive summary, dependency map, export-control texts, key entities,
    recent changes, evidence gaps and caveats, what this brief does not track, methodology, evidence appendix, source
    appendix with a ready-made citation, terms;
  - the executive summary is composed by the build from groups of the dependency result's rows and tallies of drawn
    rows (D-124 rules a to d), one sentence per group, each marked so that `tests/test_brief.py` recomputes it; a
    recorded gap is phrased as a gap, never as a link;
  - the policy section compares the **five** classes the chain reaches (each accelerator's class, the class it is
    narrower than, and every class at an end of a row), not the three of the journey page (D-191): the accelerators'
    own classes carry two refusals that concern this chain; products are never compared with a text (LA-3);
  - "recent changes" lists the recorded dated events of the acts shown, the latest publication date held and the
    chain's evidence date range, and says that a later change is unknown to the Atlas, not absent;
  - "monitoring considerations" becomes "What this brief does not track", one framing block naming no record that
    describes the Atlas's coverage, never what a reader should watch;
  - scope, the out-of-scope list, the boundary line, the as-of date and the input digest are in the first section,
    outside any disclosure, and print (U-5); "rows shown of rows in the result" and the citation carry P-18;
  - checks BR-1 to BR-12; the forbidden words of JR-9 plus "should", "must", "recommend", "is controlled", "are
    controlled" and "subject to the" in the Atlas's voice.
- **Rejected:** a free-text summary; a SQL query for the summary (nothing is computed beyond grouping and tallying);
  a new diagram (the HBM figure is accepted and checked); evidence only linked to other pages (a printed brief would
  lose it); three classes; one gap line each for "recent changes" and monitoring; leaving the monitoring section out.

## D-204 — One composition mechanism for new templates

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S21 H-1, with the brief's design)
- **Context:** A-3 (three templates, each composed differently; S20.5, D-200: "one composition mechanism for
  templates to S21, when it adds one").
- **Decision:** a template is one skeleton with named slots (`${name}`), plus named framing blocks after `</html>`
  (`<!-- framing: name -->`) that the build picks by name; a style shared with another template is filled into a named
  style slot from its one home. The journey template already works this way; `tools/brief_template.html` follows it;
  any new template uses it. The S11 and S14.5 templates are not migrated now (their pages would change for no reader's
  benefit); A-3 stays open for them, with S22.
- **Rejected:** migrating all templates in S21 (outside the brief's scope).

## D-205 — The Client Output becomes active, with a contract; owners of the brief's files

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S21 H-1; D-180)
- **Context:** `docs/agents/roles.md` (Client Output inactive until S21); MA §11.10 ("It may summarise. It must not
  silently alter factual records."); D-180 (every file has an owner; a role writes only under a contract).
- **Decision:**
  - the Client Output is active with an MA §12 contract (`docs/agents/contracts.md`): it owns `tools/build_brief.py`
    and `site/briefs/` (written only by that build); it summarises by copying, tallying, taking first and last, and
    grouping; it never writes `data/`, `sql/`, a check or another build; its gate is `tests/test_brief.py`;
  - the Editorial owns `tools/brief_template.html` (framing and style) and `docs/architecture/client-brief.md`; the
    Data Auditor owns `tests/test_brief.py` and the brief's breaks: the role that writes the brief does not write its
    checks;
  - `tests/test_agent_contracts.py` lists the Client Output among the active roles.
- **Rejected:** the Data Auditor owning the build and the page, as for the journeys (D-197), with the Client Output
  left inactive.

## D-206 — The entry page links the client brief

- **Date:** 2026-10-14 · **Status:** accepted (decided by the human on 2026-10-14, S21 H-1; extends D-193)
- **Decision:** `site/index.html` gains one card with the brief's question and a button to it (`tools/build_journeys.py`
  and its labels); JR-8 also requires the link. The brief links back to the entry page.
- **Rejected:** leaving the entry page unchanged (the brief would be reachable only by its path).

## D-207 — S21.5 runs between S21 and S22; the Change Detector becomes active, with a contract

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-14, after the external audit of
  2026-10-14; supersedes D-184's ruling that the Change Detector stays inactive)
- **Context:** every act's status and every `restricts` link say "no later change recorded in the Atlas", but no dated
  search for later rules after 5 December 2024 has been run (D-175). The agent audit kept the Change Detector
  inactive until that search had a session (F-6, D-184). The human scheduled it as a dedicated session. The session
  prompt named this decision D-202; S21 had already used D-202 to D-206, so it is recorded under the next free number.
- **Decision:**
  - `SESSION-ROADMAP.md` gains S21.5 (RESEARCH) between S21 and S22 in M6, with its mission, inputs and gate. Its
    prompt is in the private archive (D-152);
  - the Change Detector is active with an MA §12 contract (`docs/agents/contracts.md`): it compares an act the Atlas
    holds with a later official text and writes each comparison, both sides quoted, as a candidate change in its one
    home, `docs/research/change-detection.md`; it writes nothing in `data/`, no `review`, no date on a link and no
    conclusion; the Source Scout searches and the Extractor drafts the records in staging;
  - `tests/test_agent_contracts.py` lists the Change Detector among the active roles.
- **Rejected:** folding the search into S22 (an engineering audit would carry a research step and a review);
  merging the role into the Source Scout (F-6: the Scout asserts nothing, and ruling that a later text changes an
  entry is a comparison); leaving the activation to the next policy research session (the freshness gap would stay
  open through the release audits).

## D-208 — The pages say up to when later texts were searched; a check keeps that date at or after the as-of date

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S21.5 H-1 and H-4)
- **Context:** the export-control page and the client brief said that acts published after the latest publication
  date the Atlas holds "were not searched", and the brief's framing said "The Atlas runs no change detection". After
  S21.5's dated search (`docs/research/change-detection.md` §1) both were untrue.
- **Decision:**
  - the date up to which later texts were searched has one home, the "Searched to" line of
    `docs/research/change-detection.md` §1; S21.5 set it to 2026-10-15, the day the search ran, which is also the
    reference date the pages carry (D-137 moves it to the day a rebuilding session opens);
  - the export-control page shows it as "later texts searched for up to:", and the client brief's scope and summary
    say "Later texts were searched for up to <date>; texts published after it were not searched." The framing of both
    pages is reworded to match; `change-detection.md` is an input of both builds;
  - checks: JR-3 and BR-3 recompute the date; BR-5 and BR-7 require it in the summary's limits and the first section;
    **JR-13** requires the export-control page to show it, the search log's window to end on it, and the date to be
    no earlier than the as-of date. A later session that moves the as-of date (D-137) therefore runs the later-rule
    search again, or the check fails.
- **Rejected:** keeping the old sentence until S22 (untrue in the meantime); leaving the pages to S22 (newly accepted
  acts would not appear).

## D-209 — The later-rule search's outcome: two later acts recorded, their changes quoted beside the links; the change-detection rules bind

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S21.5 review; closes D-175)
- **Context:** S21.5's dated search (2024-12-06 to 2026-10-15; `docs/research/change-detection.md` §1) found two
  later BIS rules that change the wording of entries the `restricts` links rest on, no repeal of the five acts, and
  no official text rescinding the AI Diffusion rule.
- **Decision:**
  - BIS rules 2025-00636 (90 FR 4544) and 2025-00711 (90 FR 5298) are policy records from their official texts, with
    their published and effective dates as events and their status derived (D-156); the AI Diffusion debt of D-163
    and the M5 audit is closed by recording the rule;
  - each change is an `ATTRIBUTION` quoting the later text, cited by the link whose evidence names the entry
    (D-169): the 2024 HBM link cites the two 3A090.c claims; the 2023 equipment link cites the 3B001 and 3B993 claims.
    No link is dated; no term match is re-ruled, because no later text changes the sentences the matches rest on;
  - the July 2026 rule's (2026-14132) enforcement statement is a canonical `ATTRIBUTION` with no record field; no
    `repealed` event is recorded, since no repealing text exists in the window;
  - the Change Detector's rules CD-1 to CD-7 (`change-detection.md`) bind every later comparison;
  - the EAR's dates stay unrecorded, a named gap for the next policy session (search log, step 9).
- **Rejected:** recording only 2025-00711 (the AI Diffusion rule would stay unrecorded debt); keeping the comparisons
  without records; recording the acts with the links unchanged (a reader of a link would not see the later
  amendment); a repeal or end date from the July 2026 statement (it repeals nothing).

## D-210 — S21.5's open debt: a search tool, the EAR's dates, the July 2026 statement on the pages, a compact printed appendix

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, after S21.5's report); each item is
  work for the session named, which brings its design to the human before building
- **Context:** S21.5's report left four open items: the later-rule search must be re-run whenever the as-of date moves
  (D-208), but exists only as archived session scripts; the EAR record has no dates; the July 2026 enforcement
  statement (`claim-bis-rule-2026-14132-enforcement-statement`) is canonical but on no page; the printed brief grew to
  79 A4 pages, 66 of them evidence appendices (A-4).
- **Decision:**
  - **a repository tool re-runs the later-rule search** (S22): standard library; it queries the Federal Register index
    and the CFR finding aids, writes a dated log and lists candidate texts; recording any act still goes through
    staging and the human's verdict (D-183). The Verifier's anchor re-read (agent audit F-4) is considered for the same
    tool;
  - **the EAR's dates come from the 1996 reissue** (the next policy research session): the Federal Register rule the
    CFR names as the EAR's source (61 FR 12714, 25 March 1996) is retrieved, and its publication and effective dates
    become events under the existing model; no schema change;
  - **the pages show the July 2026 statement under the AI Diffusion rule** (S22, with the page builds): a "later
    statements about this act" line quoting BIS in that act's evidence on the export-control page and the client brief;
    the act's status stays derived from its own events (D-156);
  - **the printed brief lists each claim once** (S22, with the page builds): in print only, a compact evidence list
    (statement, source, page) replaces the repeated panels; the screen version is unchanged; print checks follow.
- **Rejected:** re-running the search by hand each session; freezing the pages' as-of date until a search runs; dating
  the EAR by the CFR edition read (a new event kind); leaving the EAR undated by rule; keeping the July 2026 statement
  off the pages; keeping the full printed appendix; deferring the print length to v1.5.

## D-211 — The later-rule search tool: the index and the official daily edition, owned by the Source Scout

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S22, on the tool's design; D-210)
- **Context:** D-208 makes every page rebuild that moves the as-of date re-run the later-rule search; S21.5 ran it with
  archived session scripts. D-210 asked for a standard-library repository tool. S21.5's independent register, the List
  of CFR Sections Affected and the daily reader aids, exists only as PDF, which the standard library cannot read.
- **Decision:**
  - `tools/later_rule_search.py` runs `plan.md` steps 1 to 5 for a window: the Federal Register index (every BIS
    document; each term in every agency's documents; the rescind and repeal words in BIS documents); the **official
    daily edition's XML** on govinfo.gov, read in full text for the same terms and for CFR headings naming 15 CFR
    part 774, as the independent register; candidates selected mechanically, each official PDF hashed; the registered
    official texts re-hashed (CD-5). The entries come from CD-3 of `change-detection.md` and the acts from
    `data/policies.json` (one home each); the EAR's own citation is not a term (nearly every BIS rule names it);
  - it writes one log per run, `docs/research/search-logs/later-rules/run-<from>-to-<to>.md`, with every request's
    host, time, status and hash and one outcome: none found in the searched window (exit 0), to review (3) or
    incomplete (4); a refusal is an access gap, never retried under another identity. It never writes `data/` or
    `change-detection.md`, reads no PDF's text and rules nothing (the Change Detector does, CD-1 to CD-7);
  - the Source Scout owns the tool; the Data Auditor writes its checks, `tests/test_later_rule_search.py` (LS-1 to
    LS-11, on constructed recorded responses, without the network), and the breaks S22-3 to S22-10;
  - **JR-13** reads every log in that folder: a log whose outcome is incomplete covers nothing; the others' windows
    must join without a gap up to the "Searched to" date, which a complete log must end on (breaks S22-1, S22-2);
  - the first run covers 2026-10-15 (S22 opened on the day S21.5 searched, so the window from 2026-10-16 was empty):
    none found; "Searched to" stays 2026-10-15 (`change-detection.md` §2). A test run on 13 to 17 January 2025, kept in
    the archive, found 2025-00636 and 2025-00711 with the hashes S21.5 registered.
- **Rejected:** the LSA and reader-aid PDFs as the second register (a PDF reader, poppler's `pdftotext`, outside the
  standard library and without a decision); the Data Auditor owning both the tool and its checks; no live run in S22.

## D-212 — The browser checks can fail, and run in CI with a pinned Playwright (amends D-106 and D-026)

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S22 H-0, "Browser checks run in CI
  on every push"; H-2, the Firefox and WebKit filter check; engineering audit F-1, F-11)
- **Context:** S21's report asked whether the four browser scripts should run in CI (A-6). The engineering audit found
  that none of them could fail: all exited 0 whatever they measured, two computed no verdict, and the brief's print
  verdict ignored its own first-page measures (F-1, blocking). The research view's filter had never run outside
  Chromium (D-196, D-200; F-11).
- **Decision:**
  - every script lists each failed condition by name in `qa-result.json` and exits non-zero (`tests/browser/qa-lib.js`);
    the brief's print verdict includes the first printed page (question, boundary line, as-of date, digest);
  - `tests/browser/filter.qa.js` checks the filter per engine: where `:has()` works, each basis shows exactly its rows
    and marks; where it does not, the filter is hidden and every row shown; an engine that cannot start fails;
  - `package.json` and `package-lock.json` pin Playwright 1.56.1 (test-only, like `requirements-test.txt`; no page loads
    a script); the Data Auditor owns them. Scripts take Playwright from that package when installed, else from the
    session environment (D-106 kept for sessions);
  - CI gains a `browser` job (Node 22, `npm ci`, Playwright's Chromium, Firefox and WebKit): the four page scripts in
    Chromium and the filter in all three engines, every step run even after a failure, the results kept as an artifact
    when one fails. It adds a few minutes per push.
- **Amends:** D-106 (browser QA no longer only in a scratch environment) and D-026 (a pinned Node test-only package
  beside the Python pins). D-200's condition for reconsidering a framework ("browser checks run in CI") is now met in
  part; its other condition, a recorded user question needing state in the browser, is unchanged.
- **Rejected:** keeping the checks manual (H-0's alternative); the four page scripts in Firefox and WebKit too (their
  keyboard measures depend on each engine's Tab behaviour; only the filter's engine risk was recorded).

## D-213 — The engineering audit and the M6 audit accepted; S22's remediations and the debt's owners; M6 closes

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S22 H-1 and H-2)
- **Context:** `docs/architecture/engineering-audit.md` (findings F-1 to F-14, S22's debt rows) and
  `docs/architecture/milestone-audits/M6-audit.md` (PEF §4 over S20 to S21.5), both proposed in S22.
- **Decision:**
  - both audits are accepted with these rulings; **M6 closes** with its audit;
  - **remediated in S22:** F-1 (the browser checks can fail; with H-0's CI job, D-212); F-11 (the filter in Firefox
    and WebKit, in CI, D-212); F-4 (EN-1: every tracked Python file compiles in CI on 3.11); F-7
    (`tools/check_all.py` runs the suite, Gate 0 and every `--check` in order, checked by EN-2; `README.md` names it as
    the command run immediately before each commit); F-13's print half (D-210's compact printed evidence list);
  - **debt for v1.5's opening session:** F-2 (a named build error for an out-of-vocabulary value, E-2), F-5 (breaks for
    the five check modules never shown failing, and the untested status branch), F-12 (CI actions pinned to commit
    hashes), F-14 (the search tool's main function split by step); and, as v1.5's subject, F-6 (the timeline on a
    phone; the word list is the phone form until then), F-8 (A-2), F-9 (A-3), F-10 (A-7), F-13's screen half (A-4),
    dark mode;
  - **kept:** F-3 (E-1), owned by the session that resolves `cand-001`; the Verifier's re-read tool (agent audit F-4),
    owned by the next session that adds claims from a retrieval, which decides how PDF text is read;
  - **S23:** C-8, the M5 data rows, `not_researched`'s wording against ER-3, the ID rule's legal-form list;
  - code and engineering maturity: process 3, outcome 2 at the audit and 3 with F-1 remediated (F-2 stays debt).
- **Rejected:** the named build error, the five breaks, the split search function and hash-pinned actions in S22 (each
  moved to v1.5's opening); a scrollable timeline now; keeping seven separate commands.

## D-214 — The July 2026 statement under its act; the printed brief lists each claim once

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S22, on the two designs D-210 asked for)
- **Context:** D-210 put two page items in S22: show the July 2026 enforcement statement
  (`claim-bis-rule-2026-14132-enforcement-statement`) under the AI Diffusion rule on the export-control page and the
  client brief, and print the brief's evidence as a compact list (79 A4 pages). No record held the link between that
  statement and the act; the only accepted home of it was the Change Detector's comparison C-5.
- **Decision:**
  - the link lives in the Change Detector's ruling: `change-detection.md` §1 gains a table "Later statements about acts
    held" (act ID, claim, comparison); the journeys build reads it, refuses an act the Atlas does not hold, a claim that
    is not a canonical `ATTRIBUTION`, and a claim citing the act's own text; each act panel (export-control page and
    brief) shows its later statements under "Later statements about this act" with a framing block; the act's status
    stays derived from its own events (D-156). Checks JR-14 and BR-14;
  - in print only, the brief's evidence appendix gives way to `#evidence-print`: every claim the appendix shows, once
    each, in order of first appearance, with its statement, each citation's source title and ID and its locator; the
    screen keeps the panels. BR-7's rule that print hides no evidence is narrowed to this exchange (it still fails on
    any other hidden scope, summary, evidence or source); BR-13 checks the list and the stylesheet; the browser script
    checks print and screen. Measured: 32 A4 pages (33 Letter), from 79 (83); the HTML grows from 884 to 1,006 KB,
    because the list is in the page and hidden on screen;
  - breaks S22-13 to S22-17 and the control S22-C2.
- **Rejected:** a "later statements" field on the policy record (a schema change and a canonical data edit in an audit
  session); keeping the panels in print with repeats replaced by references (24 repeats; far fewer pages saved).

## D-215 — S23 dates its pages to its opening day and re-runs the later-rule search

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, after S22's report; the recommended
  next decision, option A)
- **Context:** S23, the research depth and content audit, reads the pages as a reader would; their as-of date
  (2026-10-15) ages with every day the audit opens later. Moving it requires the later-rule search to reach the new date
  (D-137, D-208), which is now a tool (D-211).
- **Decision:** S23 sets the reference date in `sql/source_age.sql` to its opening day, runs `tools/later_rule_search.py`
  from 2026-10-16 to that day, and, if the run is complete and finds no candidate, moves "Searched to" in
  `change-detection.md` and rebuilds the 18 pages. A candidate text stops S23 for a policy-research verdict (D-183,
  CD-6); an incomplete run moves no date.
- **Rejected:** keeping the pages as of 2026-10-15 through S23 (the audit would read stale pages; S25 would still move
  the date).

## D-216 — S22.5 closes the engineering audit's findings outside v1.5 (amends D-213's owners)

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, the S22.5 session prompt: the
  findings not assigned to v1.5 closed with checks first; F-6, F-8, F-9, F-10 and the screen half of F-13 untouched)
- **Context:** D-213 ruled F-1, F-4, F-7, F-11 and the print half of F-13 remediated in S22, F-3 kept, and F-2, F-5,
  F-12, F-14 debt for v1.5's opening session. The human opened a dedicated session, S22.5, after S22, for every finding
  not assigned to v1.5 itself.
- **Decision:**
  - **F-2, F-5, F-12, F-14 move from v1.5's opening session to S22.5** and are remediated there; F-6, F-8, F-9, F-10,
    the screen half of F-13 and dark mode stay v1.5 (D-213 unchanged for them);
  - **F-2:** `Page.value` (`tools/build_page.py`) stops on a value outside its vocabulary with a `BuildError` naming the
    value, the vocabulary and every record field holding it (found from the schemas: the property names whose `$ref`
    chain reaches that vocabulary), so the three builds that read it (HBM page, journeys, brief) give the same named
    reason instead of a bare `StopIteration`. The record checks still refuse the value first (the claim schema; the
    test asserts both). Test `test_an_out_of_vocabulary_value_is_named` (`tests/test_page.py`), written first and shown
    failing with the `StopIteration`;
  - **F-3 stays kept** as D-213 ruled, since `cand-001` is unresolved (refused, `evidence_not_fresh`, D-092); no data
    change. A regression test (`test_a_resolved_drawn_gap_stops_the_builds_by_name`) confirms that the specification
    draws `cand-001` as the page's gap while the records refuse it, and that resolving it stops the HBM page and the
    brief with "refused candidate cand-001 is not canonical". It fails first when `cand-001` is resolved, telling that
    session to update `JOURNEY` with the record;
  - **F-5:** one break per module never shown failing, each failing that module alone for its named reason
    (S22.5-4 to S22.5-8: `test_claim_model.py`, `test_relationship_taxonomy.py`, `test_entity_taxonomy.py`,
    `test_facility_status.py`, `test_break_selection.py`); a fictional test runs `policy_status.derive_status`'s
    untested branch (a publication dated to the month that contains the as-of date: indeterminate), with break S22.5-9.
    No check changes;
  - **F-12:** CI's actions are pinned to commit hashes (D-217), checked by EN-3 (`tests/test_engineering.py`);
    the pip pins stay exact versions without hashes;
  - **F-14:** `later_rule_search.search` is split into one function per step (window check; BIS documents; index
    terms; the daily edition and its day counts; candidate reasons; candidates; disagreements; registered texts),
    with no change of behaviour: LS-1 to LS-11 pass, every setup of S22-3 to S22-10 still applies and each still
    fails as named, and the old and new functions give identical logs, outcomes and requests on all 13 searches the
    LS tests run. `search` goes from 104 lines and complexity 56 to 11 lines and complexity 1; no step function is longer
    than 27 lines or above complexity 12 (the audit's measure);
  - F-1, F-4, F-7, F-11 and F-13's print half are re-verified, not rebuilt: each browser script exits non-zero on a
    planted page defect; EN-1 and EN-2 keep their breaks (S22-11, S22-12); the brief prints 31 A4 pages;
  - breaks S22.5-1 to S22.5-10 and the control S22.5-C1 (`tests/regression/breaks.py`).
- **Amends:** D-213 (the owner of F-2, F-5, F-12, F-14). With F-2 remediated, D-213's "F-2 stays debt" in the code
  and engineering outcome rating no longer holds; the rating itself is left to the next audit (S24).
- **Rejected:** passing the record and field into `Page.value` from each of its callers (about 25 call sites
  changed for a message); a hand list of which field carries which vocabulary (it would drift from the schemas); a
  break that edits `data/` to make F-3's test fail as a permanent break (its fault is named by a build, not by a
  record check, so it does not meet D-176's criterion).

## D-217 — CI's actions are pinned to the commit of the release they run (F-12)

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, the S22.5 session prompt: the
  actions pinned to commit hashes, the pip pins kept exact without hashes)
- **Context:** `.github/workflows/ci.yml` named its four actions by moving tags (`actions/checkout@v4`,
  `actions/setup-python@v5`, `actions/setup-node@v4`, `actions/upload-artifact@v4`); a tag can be moved to other code.
- **Decision:** every `uses:` names a full 40-character commit hash, with the exact release beside it as a comment.
  The hashes are the commits each major tag CI already ran pointed to on 2026-10-15, read from the action's own
  repository (`git ls-remote --tags`): checkout `11d5960…` (v4.4.0), setup-python `a26af69…` (v5.6.0), setup-node
  `49933ea…` (v4.4.0), upload-artifact `ea165f8…` (v4.6.2); no action is upgraded. A later upgrade changes the hash and
  the comment together, both read from the action's repository. EN-3 fails on any `uses:` without a hash and its
  release; break S22.5-10. The Data Auditor owns the workflow, as before.
- **Rejected:** upgrading the actions while pinning them (a change of behaviour outside F-12); pip hashes (exact pins
  and a clean `pip check` suffice at this scale, the audit's own disposition).

## D-218 — The release content audit: its method, its acceptance and the dispositions of its findings

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15: S23 H-0 the sample, H-1 the PDF
  reading, H-2 the findings and dispositions)
- **Context:** S23, the research depth and content audit before v1.0 (roadmap S23; PEF §4, §6), audited the content
  as a system for the first time since S13, which read the HBM page alone. Its debt rows came from D-213 and the M6
  audit.
- **Decision:**
  - **the method:** every claim a page result rests on (59, traced mechanically) plus 30 drawn by type are read in
    full, and the anchor of every citation (203) is searched for in bytes retrieved on the audit's day; PDF text comes
    from the machine's poppler `pdftotext`, called by a standard-library script in the audit's evidence folder, its
    version recorded with every result. No repository dependency is added and D-026 is unchanged; the Verifier's
    re-read tool (agent audit F-4) still decides its own PDF reading;
  - **the audit** (`docs/research/release-content-audit.md`) **is accepted** with its ratings: research and content,
    process 3, outcome 2 (unchanged since S13). No blocking finding: 178 of 178 readable anchors found at their
    locators, 0 of 85 judged claims exceeding their evidence; ten sources are access gaps;
  - **C-1** is remediated in S23 (D-220); **C-2** in S23 (D-221); the inherited `not_researched` wording in S23
    (D-219);
  - **wording only, no data change:** `claim-model.md` §10 says that a source's retrieval date dates an undated
    source and a citation's read date records a re-read (closes the analytical audit's C-8); `policy-dataset.md` says
    that `issued_in` may rest on two official texts joined by the bureau both name, and that an official text's
    `publisher` names its edition (closes the M5 audit's two data rows); `company-dataset.md` §3 says why
    `company-samsung-electronics-co-ltd` keeps "co-ltd" and that "Co., Ltd." joins the legal-form list only by a
    decision that keeps existing IDs valid;
  - **debt with owners, nothing built:** C-3 (this audit's text hashes are the baseline for the next re-read of an
    HTML source; the Verifier's re-read tool records a text hash), C-4 (Amkor's two sources re-read from a file the
    human supplies, RA-4, when next relied on), C-5 (single-voice values: a stated limitation), C-6 (narrow coverage:
    the release's coverage statement; v2, D-201), C-7 (the concept layer on no page: v1.5), C-9 (the Verifier's tool
    tolerates PDF extraction artefacts), C-10 and E-1 (kept); "the working definition of HBM" is closed with no change
    (the difference with the 2024 rule's HBM is stated in the term-match claim on the pages);
  - **C-8, debt owned by sessions that do not exist before v1.0** (the EAR's dates, the May 2026 BIS guidance, a
    current H100 supplier and fabricator, a recognised source for Trainium2's memory maker, newer evidence for values
    past the horizon, `cand-001`): S25 lists each as a v1.0 known limitation with what is missing, and each moves to a
    named research session after the release. The roadmap is unchanged.
- **Rejected:** every claim read in full (twice the reading for a bound the anchor search already narrows); only the
  weight-bearing claims (nothing could be said of the rest); a pinned PDF reader in the test requirements; PDF anchors
  by hand; reclassifying the five `issued_in` claims as `DERIVATION` and renaming eight official sources' publishers
  (data changes for a wording question); adding a research session before S25.

## D-219 — `not_researched` covers a partial search (vocabulary wording)

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S23 H-2; release content audit,
  Part 6 row 4)
- **Context:** The vocabulary defined `not_researched` as "No source has been checked for this value yet", while
  ER-3 keeps the state after a search that did not cover every preferred class (`hbm-supplier-research-original-rules.md`;
  D-213 sent the wording to S23). SK hynix's `incorporated_in` is such a case: its annual report was read and names
  no country.
- **Decision:** the description of `not_researched` in `schemas/entities.schema.json` reads "No research has
  established this value: no source has been checked yet, or a search did not cover every preferred class
  (source-policy.md ER-3). Says nothing about whether the value is public." Only the description changes: the value,
  the validation and every record stay as they were; the pages that print the description (the HBM page, for a
  supplier left unknown) print the new text when such a value appears. A schema file changed, so the full break
  harness runs (D-177).
- **Rejected:** a second state for a partial search (a schema and data change); explaining the use in ER-3 only,
  leaving the vocabulary contradicting it.

## D-220 — BIS's announcement about the AI Diffusion rule is recorded as an `announced` event; the timeline names every kind of event it draws

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S23 H-2 "record it now", and the
  verdict on the three records, `docs/quality/human-reviews.md`)
- **Context:** The release content audit's C-1: the export-control page and the client brief show the AI Diffusion
  rule (`policy-us-fr-2025-00636`) as "has taken effect" without BIS's own announcement of 13 May 2025, held only as a
  pointer (CD-7) inside 2026-14132's sentence. The model already had its place: an `announced` event on a policy
  (`events.schema.json`), supported by a `government_publication` (`event:announced`), which never moves a status
  (ER-8; PL-7).
- **Decision:**
  - three records, accepted by the human: the source `src-065` (the bis.gov press release of 13 May 2025, the page
    91 FR 43034 cites; retrieved 2026-10-15, four anchors found); the claim
    `claim-bis-ai-diffusion-rescission-announced-2025-05-13` (`ATTRIBUTION`, party standing: what the release states,
    and that it does not itself rescind the rule); the event `event-us-fr-2025-00636-announced-2025-05-13`;
  - the Change Detector rules which act the announcement concerns, in a new table of `change-detection.md` §1,
    "Announcements about acts held": the release's name and issue date for the rule, and 91 FR 43034's citation of
    the same address. A PDF copy on `media.bis.gov` that differs from the page (12 May, "initiated", "a Federal
    Register notice") is not registered;
  - the rule's status stays "has taken effect": no text in the searched window repeals it (D-209), and an
    announcement never moves a status (D-156);
  - the export-control timeline's key names exactly the kinds of event the timeline draws, the unusual ones by their
    vocabulary value (`events.schema.json`), so the new `announced` mark is explained; JR-15, written first and shown
    failing on the rebuilt page; break S23-1.
- **Rejected:** leaving the announcement out of v1.0 (H-2's alternative); registering the `media.bis.gov` PDF (it is
  not the page the official text cites, and it differs from it); a repeal or end date from the announcement (ER-8,
  D-209); a "later statements" row for it (that table holds official texts' statements, D-214).

## D-221 — Company pages mark values whose newest evidence is past the freshness horizon on the as-of date

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, S23 H-2 "mark any value past 12
  months"; release content audit C-2)
- **Context:** Micron's legal name, incorporation, headquarters and role rest on its 10-K signed 2025-10-03, which
  passed the 12-month horizon (`source-policy.md` §12) on 2026-10-03 with no signal: F-1 measures age at verification
  by design, the source-age query (D-129) ages only the chain's links, and the Atlas-wide ageing report (DT-S13-4)
  had no owner able to build it. V-5 forbids ages from a clock.
- **Decision:**
  - `tools/evidence_age.py` (Data Auditor; standard library) says, for one value of a `time_sensitive` matrix row,
    whether the newest evidence the row accepts is dated more than the horizon before the reference date. It reads
    each input from its one home: the reference date from `sql/source_age.sql`, the horizon and the matrix from
    `source-policy.md`, evidence dates by §12's rule; a historical value (`valid_to`, D-144) is never marked. The
    journeys build stops if the reference date differs from the source-age result's;
  - each company page marks such a value beside it: "(newest evidence <date>, more than <12> months before the as-of
    date)", the date and the horizon as derived values, with a framing block saying what the mark does and does not
    mean; no age is computed and no value is called current or stale (V-5). Today it marks Micron's four values;
  - JR-16 recomputes the marks with the freshness check's own helpers (`tests/test_freshness.py`), with the as-of date
    in place of the verification date; written first and shown failing on Micron's page; JR-3 knows the two new
    derived values; break S23-2. The build's and the tests' input lists gain the module;
  - the Atlas-wide ageing report of DT-S13-4 is discharged for company values; the other `time_sensitive` rows
    (edges, facilities) are aged by the source-age query (chain links) or carry no current value outside it.
- **Rejected:** refreshing Micron from its FY2026 10-K (fixes one company once; new research for a named session after
  v1.0, D-218); listing the four values as a limitation only; a mark computed from today's date (V-5); an SQL query and
  its tutorial for a comparison of two dates.

## D-222 — S24 writes v1.0's known limitations as a document and audits it

- **Date:** 2026-10-15 · **Status:** accepted (decided by the human on 2026-10-15, after S23's report; the recommended
  next decision, option A)
- **Context:** D-218 sends the gaps no v1 session owns (C-8: the EAR's dates, the May 2026 BIS guidance, a current
  H100 supplier and fabricator, a recognised source for Trainium2's memory maker, newer evidence for values past the
  horizon, `cand-001`) to S25 as v1.0 known limitations, beside single-voice values and narrow coverage (C-5, C-6).
  S24, the portfolio and capability audit, asks whether the project communicates its capability honestly; the
  limitations are half of that answer.
- **Decision:** S24 creates `docs/known-limitations.md`, one row per gap: what is missing, why, what would close it,
  and which session after v1.0 owns it. S24 checks that the pages' limits (their "does not track" and method framing,
  the brief's scope and limits) agree with it, and audits it as part of the portfolio audit. S25 links it from the
  release notes. No record, page or check changes beyond the new document and its check; the roadmap's sessions are
  unchanged.
- **Rejected:** leaving the list to S25's release notes, written once at the release without an independent look.

## D-223 — The Portfolio Reviewer is active, for the portfolio audit and v1.0's known limitations

- **Date:** 2026-10-16 · **Status:** accepted (decided by the human on 2026-10-16, S24 H-1: "Audit plus limitations
  list (Recommended)")
- **Context:** D-184 kept the Portfolio Reviewer inactive "until S24"; every audit since S12 was written by the
  Knowledge Architect. S24 is the portfolio and capability audit (PEF §10, §12), and D-222 gives it v1.0's known
  limitations to write and audit. MA §12 requires a contract before a role acts.
- **Decision:** the Portfolio Reviewer is active with a contract (`docs/agents/contracts.md`). It writes the portfolio
  audit `docs/architecture/portfolio-audit.md`, its evidence in `docs/quality/audit-evidence/portfolio-audit/`, and
  `docs/known-limitations.md`. The Knowledge Architect keeps `decisions.md` and `audit-history.md` and no longer owns
  the portfolio audit's evidence folder; the Data Auditor writes the check that the pages' limits agree with the known
  limitations. The role credits a capability only for evidence a reviewer can recount, never for a document's
  description of itself. `tests/test_agent_contracts.py` expects the role active.
- **Rejected:** the Portfolio Reviewer writing the audit only, with the known limitations left to the Knowledge
  Architect (the capability judgement and the disclosed limits with two roles); keeping the role inactive and amending
  D-184 (the roadmap's reviewer unused before v1.0).

## D-224 — The portfolio audit is accepted with its rulings; v1.0's known limitations are accepted

- **Date:** 2026-10-16 · **Status:** accepted (decided by the human on 2026-10-16, S24 H-2: the audit and the
  known-limitations document "as written"; each remediation as recommended)
- **Context:** S24's portfolio and capability audit (`docs/architecture/portfolio-audit.md`) measured the roadmap's
  eight capability points and PEF §4's retrospective, with two fresh readers before its assessment (H-0), and found no
  blocking finding and fourteen findings, P-1 to P-14. D-222 asked S24 to write v1.0's known limitations and check
  them against the pages.
- **Decision:**
  - the audit, its ratings (Part 6; the code and engineering outcome, left open by D-216, is 3) and
    `docs/known-limitations.md` (15 gaps, 5 boundaries) are accepted; S25 links the document from the release notes;
  - **remediated in S24:** P-1, a "How this was built" section in `README.md`; P-4 and P-12, a plain-language opening
    and the break count corrected; P-5, the brief's summary framing says that a named or reported supplier is not the
    only supplier; P-7, the brief's query states its population, its denominator and what it does not prove, checked
    for every query by WH-16 (written first), results and pages rebuilt with the query's logic unchanged; P-8, the
    archive's `sessions/README.md` says that sessions, not a tool, now check a report's fields; P-10, D-225; P-14, the
    "later statements" framing says that a text a later statement cites is held only as it is quoted and is unread;
  - **owned after S24:** P-2 (no recorded code review) and P-6 (policy description, not analysis) are stated in S25's
    case study, and a code-review rule or an analysis layer is the human's decision at S25, v1.5 or v2; P-3
    (publication) is S25's decision; P-9 is a process lesson in S24's report; P-11 goes to v2's agent activation; P-13
    stays as D-152 rules, with this audit's counts as the public summary;
  - breaks S24-1 to S24-9 and the control S24-C1 test the new checks.
- **Rejected:** leaving the authorship account, the README's wording, the unread guidance, the supplier warning and
  the query header to S25 or v1.5; a checker script in the archive (the archive has no CI); leaving the three rule
  changes unrecorded; changing findings or ratings before acceptance.

## D-225 — Three changes to the rule documents of 2 October 2026 are recorded

- **Date:** 2026-10-16 · **Status:** accepted (decided by the human on 2026-10-16, S24 H-2, portfolio audit P-10)
- **Context:** three changes to the constitutional documents were made on 2 October 2026 on the human's instruction,
  each in its own pull request merged by the human, with no decision record (portfolio audit, Part 4).
- **Decision:** the record holds them, with their commits and pull requests, as taken by the human on that day:
  - `269a1fa` (pull request #16): visual intelligence and data storytelling become a cross-cutting capability
    (`CLAUDE.md` §6A, `MASTER-ARCHITECTURE.md` §16.1, `SESSION-ROADMAP.md`'s cross-cutting section);
  - `d8a5be5` (pull request #19): a request for a human decision explains its concrete consequences (`CLAUDE.md` §9A,
    `SESSION-PROMPT-SPEC.md` §9);
  - `aeec137` (pull request #21): an interactive question must be understandable on its own (`CLAUDE.md` §9A,
    `SESSION-PROMPT-SPEC.md` §9), with the S12 prompt's questions rewritten to that rule.
  No document changes; the rules stand as merged.
- **Rejected:** leaving the audit's finding as the only trace of the three changes.
