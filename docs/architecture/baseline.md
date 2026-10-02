# Baseline Architecture Record

**Status:** APPROVED by the human on 2026-09-29 (S02 gate, `SESSION-ROADMAP.md` S02; see §8).
Created in S00, revised and approved in S02. S03 to S10 updated only the dated state rows (§1 table, §3, §4, §5). The S05 review added NG-14 to §6 through D-043, as D-021 requires, and updated the open items in §7 and §8.
**Date:** 2026-09-29 (S00); revised 2026-09-29 (S02)
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` §4 ("At project start").

This record states what this repository intends to be at the start of the project. It
deliberately **references** `MASTER-ARCHITECTURE.md` (MA) and `CLAUDE.md` instead of
restating them, so each architectural statement keeps one home. Decisions taken in this
repository are logged in [`decisions.md`](./decisions.md).

---

## 1. Intended architecture

- **Product role:** the AI industrial/physical layer of the portfolio — MA §3.2.
- **Independence:** a standalone repository with no runtime, code, data or packaging
  dependency on `Eu-Digital-Policy` — MA §4.1–4.3, CLAUDE.md §3. See decision D-006.
- **Pipeline:** source discovery → raw evidence → staging → verification → canonical →
  derivations → index/graph → presentation → QA → publish — MA §16.
- **Stack (intended, not yet installed):** JSON canonical records, Python transformations,
  DuckDB + SQL for analysis, vanilla HTML/CSS/JS, GitHub Actions — MA §17, CLAUDE.md §11.
  No database server, graph database or frontend framework — MA §18.

### State at end of S00, updated at S02, S03, S04, S05, S06, S07, S08, S09 and S10

| Layer | Exists? | Introduced by (per `SESSION-ROADMAP.md`) |
|---|---|---|
| Constitutional documents | yes (repo root) | user, before S00 |
| Session system (`sessions/`) | yes | S00 |
| Repository integrity validator + CI | yes | S00 |
| Domain map / source register | yes, draft (S01) | S01 |
| M0 milestone audit + EU-DP process benchmark | yes, draft (S02) | S02 |
| Entity schema | yes, accepted (S03): `schemas/entities.schema.json`, `entity-taxonomy.md` | S03 |
| Relationship schema | yes, accepted (S04): `schemas/relationships.schema.json`, `relationship-taxonomy.md` | S04 |
| Source/evidence policy | yes, accepted (S05 review): `docs/research/source-policy.md`, and the class vocabulary in `schemas/sources.schema.json` | S05 |
| Claim/provenance implementation | yes, accepted (S06 review): `docs/architecture/claim-model.md`, `schemas/claims.schema.json`, the source record in `schemas/sources.schema.json`, `tools/trace.py` | S06 |
| Canonical data | yes (S07 to S10, accepted by the human in the session): 52 source records (`data/sources.json`), 120 claims (`data/claims.json`), 8 companies, 4 jurisdictions, 7 components, 9 technologies, 3 products, 2 facilities, 4 events (`data/events.json`, schema `schemas/events.schema.json`) and 5 relationships (`data/relationships.json`), as measured at the S10 final commit. Staging is empty | S06 to S10 |
| Presentation / UI | no | S11 |
| DuckDB / SQL layer | no | S14 |

Directories for data, schemas, analysis and UI are **not** created until the session that
needs them (decision D-005). Their layout is that session's design decision.

## 2. Initial scope boundaries

Approved 2026-09-29 (D-017). This section is the single statement of
the boundaries; the sources it cites keep their own wording.

- **Repository boundary.** The Atlas holds the industrial and physical records only
  (MA §3.2). Governance and integration records belong to the other portfolio repositories
  (MA §3.3–3.4). `Eu-Digital-Policy` is a read-only methodological reference (MA §4.1–4.2,
  D-006).
- **Governing question.** The global wording (CLAUDE.md §10, MA §25). The EU vs non-EU view
  comes later, built over the same records (D-008).
- **First vertical.** Deliberately narrow: `AI compute → accelerators → manufacturing →
  advanced packaging → HBM → equipment → cloud/data centres` (MA §6.4, §25). Its layers are
  S01's seven, with EDA and SME as sub-layers 5a/5b (D-013). The working terms are
  `domain-map.md` §7.1 (D-016). Server integration stays inside layer 6 (TQ-11).
- **Which concepts become records.** The v1 classification in
  `milestone-audits/M0-audit.md` Part 4 (D-020) is S03's starting input.
- **Energy and networking.** Energy stays concept-level in v1: no records or edges, and
  only rated power and nameplate capacity as attributes. Networking is excluded (MA §6.4;
  D-017; NG-04, NG-05).
- **Policy layer.** Starts at S17 and must not duplicate `Eu-Digital-Policy`
  (`SESSION-ROADMAP.md` S17).

## 3. Intended agent roles

Roles and the contract format are defined in CLAUDE.md §8 and MA §11–12. S06 wrote
`docs/agents/roles.md` and `docs/agents/contracts.md` (accepted at the S06 review, D-052): the roles active
through S10 have contracts, and the others name the session that first activates them. There is no root `AGENTS.md`
(decision D-010). Until S19 finds a manual workflow that needs one, agents are contracts
plus deterministic validators, with no agent runtime (D-018 L-01; NG-08).

## 4. Initial data model

The conceptual contract (Entity, Claim, Source, Relationship, Event; status and null
semantics) is MA §5; the Atlas-specific entity and relationship lists are MA §6.1–6.2;
claim types and evidence status are MA §10. The entity schema was accepted in S03
(`entity-taxonomy.md`, D-022 to D-025). The relationship schema was accepted in S04
(`relationship-taxonomy.md`, D-028 to D-033); its §6 reconciles MA §6.2, the relationship
list in `SESSION-ROADMAP.md` S04 and the verbs in `domain-map.md` §3. The source policy was accepted at the S05 review (`source-policy.md`, D-034 to
D-043): source classes, a preference matrix read from both schemas, and evidence, conflict,
retrieval and freshness rules. The claim and source records were accepted at the S06 review (`claim-model.md`, D-044 to D-053). The first company and jurisdiction records follow `company-dataset.md` (S07, D-054 to D-066, accepted at the S07 review); technology, component and product records follow `concept-dataset.md` (S08, D-067 to D-077, accepted at the S08 review; D-070 and D-076 at the end of S09); facility and event records follow `facility-dataset.md` (S09, D-078 to D-088, accepted at the S09 reviews).

## 5. Quality gates

Gate definitions: MA §14. Validation-command philosophy: MA §15.

| Gate (MA §14) | Status in this repository |
|---|---|
| 0 — Repository integrity | **Partial, automated.** `tools/validate_repo.py` checks required docs and session prompt/report conventions; runs in CI. It does not check branch or unexpected generated changes. |
| 1 — Schema | **Partial, automated.** CI tests every schema's behaviour against fictional fixtures (S03 to S06; D-026), and validates every source, claim and entity record in `data/` (VD-2, S06 to S08), from S09 every event, and from S10 every relationship. |
| 2 — Provenance | **Partial, automated** (S06). Every claim's sources, inputs, anchors, statuses and review state are checked in CI (VD-3 to VD-13, `claim-model.md` §11). From S07, entity records are checked too: references, placeholder IDs, the matrix row of every field (V-10), canonical-only support (CE-1), the ID rule and ISO codes (`company-dataset.md` §8); from S08, working definitions, concept uniqueness, `broader` acyclicity and the concept and product tables (`concept-dataset.md` §9); from S09, the facility ID rule, location without headquarters evidence, kind words, capacity, and the event rules (`facility-dataset.md` §11); from S10, the edge rules V-1 to V-10, CE-1, the edge ID rule and four evidence guards (`edge-dataset.md` §10) |
| 3 — Semantic integrity | **Partial, automated** (S10): impossible edges fail in CI (V-2 kind constraints, V-3 self-edges, V-5 duplicates, V-6 `broader` restated as an edge); role and edge conflicts (RW-1 to RW-3) are reported as warnings, never corrected (D-033; `edge-dataset.md` §10) |
| 4 — Derivation | not applicable yet |
| 5 — Content | not applicable yet |
| 6 — UI | not applicable yet (no UI) |
| 7 — Browser regression | not applicable yet |
| 8 — Portfolio quality | human review at each session |

| Command (MA §15) | Status |
|---|---|
| `validate-data` | **built for sources, claims, entity, event and relationship records** (S06 to S10; D-051, D-063, D-077, D-087, D-096): `python -m unittest discover -s tests -p "test_data*.py"`, run in CI; V-7 and V-8 report warnings |
| `validate-i18n` | not applicable in v1.0 (NG-10: English only) |
| `validate-design` | not built — needs UI (S11+) |
| `validate-freshness` | **first rule built** (S07, D-064): F-1, the 12-month horizon for `time_sensitive` fields, `python -m unittest discover -s tests -p "test_freshness.py"`, run in CI. Scheduled re-checks wait for the Change Detector |
| `qa-browser` | not built — needs UI (S11+) |

## 6. Explicit non-goals — frozen for v1.0 (D-021)

This list is the one home of the Atlas non-goals. It was approved on 2026-09-29 and is
frozen until the v1.0 release (S25). A non-goal changes only through a new decision record, approved by the
human **before** the work starts. Each row cites where the rule comes from.

| ID | Not in v1.0 | Source |
|---|---|---|
| NG-01 | Modifying, forking, copying from, sharing a package with, or taking a runtime dependency on `Eu-Digital-Policy` | MA §4.1–4.3; D-006 |
| NG-02 | Global-governance or sovereignty/integration layers in this repository | MA §3 |
| NG-03 | Coverage beyond the first vertical, including the concepts marked `future` in `domain-map.md` §2 | MA §6.4, §25 |
| NG-04 | Networking and interconnect as records | MA §6.4; S01 exclusions |
| NG-05 | Energy records or edges (energy stays concept-level; D-020 attributes only) | MA §6.4; D-017 |
| NG-06 | Classifying entities as EU or non-EU before that view is built | D-008 |
| NG-07 | A database server, graph database or frontend framework without a recorded requirement | MA §17–18; CLAUDE.md §11 |
| NG-08 | An agent runtime (orchestrator, dispatcher, autonomous write path, control plane) before S19 | D-018 L-01 |
| NG-09 | A chatbot or any interface that answers from model memory | MA §24; CLAUDE.md §19 |
| NG-10 | Translations: the Atlas is English-only in v1.0 | D-018 L-05 |
| NG-11 | Metrics, scores or rankings before their question and denominator are defined (S14–S15) | SESSION-PROMPT-SPEC §7; PEF §8 |
| NG-12 | Legal advice or compliance determinations | CLAUDE.md §13; MA §20 |
| NG-13 | Public deployment before the S11 vertical slice exists and passes its gates | D-004; MA §14 |
| NG-14 | A runtime or retrieval dependency on an external API (added 2026-09-30, human decision) | S00 prompt; D-043 |

The list this section replaced was S00's, taken from `SESSION-ROADMAP.md` S00:
production data ingestion; canonical data; frontend work; graph database; external API
dependency. Those were session-scoped and stay in the S00 prompt. Graph databases are
covered by NG-07. "External API dependency" was left to the human at approval, and became NG-14 at
the S05 review (D-043). Later session-level non-goals are
listed in each session's prompt.

## 7. Known uncertainties

U-1, U-3, U-4 and U-5 were resolved by human decision after S00 (D-008–D-010). The
original wording is kept below for traceability. U-2 was resolved by D-019 at the S02
review. D-014 and D-015 (S01) were superseded in part at the S05 review (D-039, D-036).

- **U-1 — RESOLVED by D-008. First analytical question has two wordings.** CLAUDE.md §10/§20 and MA §25:
  *"Where are the critical dependencies behind AI compute, and what evidence supports that
  assessment?"* MA §6.3 and MA §22 M2: *"Where and how is European AI compute dependent
  on non-EU capabilities?"* / "EU AI compute dependency map". The second adds a
  jurisdictional frame (EU vs non-EU) that changes scope and data requirements.
- **U-2 — RESOLVED by D-019. Milestone labels collide.** MA §22 M0–M7 are portfolio milestones (e.g. M4 =
  global governance); `SESSION-ROADMAP.md` M0–M7 are project milestones (e.g. M4 =
  analytical intelligence). A bare "M4" is ambiguous.
- **U-3 — RESOLVED by D-009. First-session scope is stated three ways.** CLAUDE.md §20 and
  `OPUS-5.5-BOOTSTRAP-PROMPT.md` ask the first session for schema, vocabulary, source
  policy, agent contracts, seed data and a UI slice; `SESSION-ROADMAP.md` and
  `S00-PROMPT.md` split that across S00–S11. S00 followed the session prompt. Whether
  the bootstrap prompt is superseded is undecided.
- **U-4 — RESOLVED by D-010. No owner for agent contracts.** CLAUDE.md §20 lists "an agent contract set" as a
  first-phase output and PROJECT-EVALUATION-FRAMEWORK §11 expects `docs/agents/`, but no
  session before S19 is assigned to produce it.
- **U-5 — RESOLVED by D-010. `AGENTS.md`.** CLAUDE.md §3–§4 refers to `AGENTS.md` as canonical; the text
  appears to describe `Eu-Digital-Policy`. This repository has none. Whether the Atlas
  should have one is undecided.

## 8. Approval record (S02 gate)

Filled in from the human's decision ("Approvo la baseline", 2026-09-29). Every row reads
`approved`, so the S02 gate is passed and M0 is complete.

| Item | Where | Human decision | Date |
|---|---|---|---|
| Project boundaries | §2, D-017 | approved | 2026-09-29 |
| Non-goals frozen | §6, D-021 | approved | 2026-09-29 |
| Architecture baseline as a whole | this file, with D-018 to D-020 | approved | 2026-09-29 |

Not covered by this approval: D-014 and D-015, superseded in part at the S05 review (D-039,
D-036); "external API dependency", which became NG-14 (D-043). Still open: S01's weekly gate.
