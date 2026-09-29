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

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** accepted (2026-09-29, human review of S00)
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

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** proposed (human decision required: "approve project boundaries", S02 prompt)
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

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** proposed (human decision; each item may be accepted or rejected separately)
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

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** proposed (human decision)
- **Context:** U-2. MA §22 M0–M7 are portfolio milestones. `SESSION-ROADMAP.md` M0–M7 are
  Atlas project milestones.
- **Decision:** In documents written in this repository, a bare `M0`–`M7` means the
  `SESSION-ROADMAP.md` milestones. MA §22 milestones are always written "portfolio M4"
  or "MA §22 M4". The human-authored root documents are not edited.
- **Rejected:** renaming the milestones in MA or the roadmap (editing human documents to
  fix a label); a different letter prefix (it would diverge from both documents).

## D-020 — v1 concept classification is S03's starting input

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** proposed (human decision; the S01 handoff's "recommended next decision")
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

- **Session:** S02 · **Date:** 2026-09-29 · **Status:** proposed (human decision required: "explicitly freeze non-goals", S02 prompt)
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
