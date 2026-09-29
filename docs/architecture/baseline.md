# Baseline Architecture Record

**Status:** DRAFT — created in S00; approval is the S02 gate (`SESSION-ROADMAP.md`, S02).
**Date:** 2026-09-29
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

### State at end of S00

| Layer | Exists? | Introduced by (per `SESSION-ROADMAP.md`) |
|---|---|---|
| Constitutional documents | yes (repo root) | user, before S00 |
| Session system (`sessions/`) | yes | S00 |
| Repository integrity validator + CI | yes | S00 |
| Domain map / source register | no | S01 |
| Entity / relationship schemas | no | S03, S04 |
| Source/evidence policy | no | S05 |
| Claim/provenance implementation | no | S06 |
| Canonical data | no | S07–S10 |
| Presentation / UI | no | S11 |
| DuckDB / SQL layer | no | S14 |

Directories for data, schemas, analysis and UI are **not** created until the session that
needs them (decision D-005). Their layout is that session's design decision.

## 2. Initial scope boundaries

- First analytical question: the global wording (CLAUDE.md §10, MA §25). The EU vs
  non-EU view comes later, built over the same records — decision D-008.
- First vertical, deliberately narrow: `AI compute → accelerators → manufacturing →
  advanced packaging → HBM → equipment → cloud/data centres` — MA §6.4, §25.
- Energy and networking are added only after the base graph is reliable — MA §6.4.
- The policy layer starts at S17 and must not duplicate `Eu-Digital-Policy` —
  `SESSION-ROADMAP.md` S17.

## 3. Intended agent roles

Roles and the contract format are defined in CLAUDE.md §8 and MA §11–12. **No agent
contracts exist yet.** S06 writes them in `docs/agents/`. There is no root `AGENTS.md`
(decision D-010).

## 4. Initial data model

The conceptual contract (Entity, Claim, Source, Relationship, Event; status and null
semantics) is MA §5; the Atlas-specific entity and relationship lists are MA §6.1–6.2;
claim types and evidence status are MA §10. **No physical schema exists yet**; S03/S04
own it. Those sessions must reconcile MA §6.2 with the relationship list in
`SESSION-ROADMAP.md` S04, which differs (e.g. `designs`, `packages`, `fabricates`,
`constrained_by`, `affected_by` appear only in the roadmap).

## 5. Quality gates

Gate definitions: MA §14. Validation-command philosophy: MA §15.

| Gate (MA §14) | Status in this repository |
|---|---|
| 0 — Repository integrity | **Partial, automated.** `tools/validate_repo.py` checks required docs and session prompt/report conventions; runs in CI. It does not check branch or unexpected generated changes. |
| 1 — Schema | not applicable yet (no schema) |
| 2 — Provenance | not applicable yet (no claims) |
| 3 — Semantic integrity | not applicable yet |
| 4 — Derivation | not applicable yet |
| 5 — Content | not applicable yet |
| 6 — UI | not applicable yet (no UI) |
| 7 — Browser regression | not applicable yet |
| 8 — Portfolio quality | human review at each session |

| Command (MA §15) | Status |
|---|---|
| `validate-data` | not built — needs schemas (S03+) |
| `validate-i18n` | not built — no i18n requirement is stated for the Atlas; needs a human decision on whether it applies |
| `validate-design` | not built — needs UI (S11+) |
| `validate-freshness` | not built — needs sources with access dates (S06+) |
| `qa-browser` | not built — needs UI (S11+) |

## 6. Explicit non-goals (S00 and current phase)

From `SESSION-ROADMAP.md` S00 and `OPUS-5.5-BOOTSTRAP-PROMPT.md`:

- production data ingestion; any canonical data;
- frontend work; graph database; external API dependency;
- global governance or sovereignty/integration layers;
- modifying, forking, copying or sharing a package with `Eu-Digital-Policy`.

## 7. Known uncertainties

U-1, U-3, U-4 and U-5 were resolved by human decision after S00 (D-008–D-010). The
original wording is kept below for traceability. U-2 remains open.

- **U-1 — RESOLVED by D-008. First analytical question has two wordings.** CLAUDE.md §10/§20 and MA §25:
  *"Where are the critical dependencies behind AI compute, and what evidence supports that
  assessment?"* MA §6.3 and MA §22 M2: *"Where and how is European AI compute dependent
  on non-EU capabilities?"* / "EU AI compute dependency map". The second adds a
  jurisdictional frame (EU vs non-EU) that changes scope and data requirements.
- **U-2 — OPEN. Milestone labels collide.** MA §22 M0–M7 are portfolio milestones (e.g. M4 =
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
