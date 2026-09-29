# M0 Milestone Audit — Project Constitution (S00–S02)

**Status:** DRAFT. Written in S02. The human's approval of the baseline closes M0.
**Date:** 2026-09-29
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4 ("At every major milestone") and
`SESSION-ROADMAP.md` S02 ("process benchmark").
**Milestone label:** M0 in `SESSION-ROADMAP.md` numbering. See D-019 for U-2.

**Bases read.**

- This repository: `main` @ `e071d4b`, which includes S00, S01 and the S01 review.
- `Eu-Digital-Policy` (EU-DP): `origin/main` @ `cc1f7d0` (2026-09-28). It was read only.
  Nothing was written to it and nothing was copied from it (D-006, MA §4.2). `git status`
  in that clone was empty after every command.

**Claim labels** (CLAUDE.md §6). Every row below is labelled with one of these:

- `FACT`: a file, line, commit or command output in one of the two repositories.
- `ATTRIBUTION`: what an EU-DP document says about itself, not re-measured here.
- `DERIVATION`: a count or comparison computed here from `FACT`s.
- `INTERPRETATION`: this audit's own reading.
- `IMPLICATION`: what follows for the Atlas.

A lesson is `INTERPRETATION` even when every piece of its evidence is `FACT`.

---

## Part 1 — Process benchmark: lessons from `Eu-Digital-Policy`

### 1.1 Method and limits

- **Read:** `AGENTS.md`; `docs/PROJECT-CONTEXT.md`; `docs/AUDIT-2026-09-01.md`;
  `docs/GOVERNANCE-PROPOSALS.md` §0–§4; `docs/EVIDENCE-MODEL.md` §1; the heading
  structures of `docs/HANDOVER.md` and `docs/CURRENT-ARCHITECTURE.md`; and the `git log`
  of `origin/main`.
- **Run:**
  - `node tools/validate.mjs`;
  - `node agent/proposals/governance/cli.mjs corpus`;
  - `git log` / `wc -l` measurements.
- **Not run to completion:** `node agent/production/cli.mjs readiness` did not finish
  within 120 s and was abandoned. EU-DP's production-readiness figures below are
  therefore `ATTRIBUTION`, not re-measured.
- **Not audited:** EU-DP's legal content, UI, or the correctness of its agents. This is a
  process benchmark. It is not an outcome audit of EU-DP, and it rates nothing in EU-DP.
- **Two known biases:**
  - Much of the evidence comes from EU-DP's own self-audits. They are unusually candid,
    but a project's self-audit is still an interested source.
  - `main` excludes work on unmerged branches.

### 1.2 Measured profile of EU-DP

| # | Measure | Value | Label · evidence |
|---|---|---|---|
| E-1 | Commits on `main` | 238, from 2026-08-26 to 2026-09-28 | `FACT` · `git rev-list --count origin/main` |
| E-2 | Session labels in commit subjects | 25 distinct labels between SESSION 00 and SESSION 30. No SESSION 01 or 14–19 appears in a `main` subject | `DERIVATION` · `git log` subject grep |
| E-3 | Agent layer (`agent/`) | 257 files · 78,590 lines | `FACT` · `git ls-files agent \| xargs cat \| wc -l` |
| E-4 | Reader-facing code (`js/*.js` + `app.js`) | 8,704 lines | `FACT` · `wc -l` |
| E-5 | Validators (`tools/*.mjs`) | 5,478 lines | `FACT` · `wc -l` |
| E-6 | Governance / handover prose (`docs/*.md` + `AGENTS.md`) | 17,411 lines. `AGENTS.md` alone is 727 lines and `docs/HANDOVER.md` 3,035 | `FACT` · `wc -l` |
| E-7 | Ratio of agent-layer lines to reader-facing code lines | ≈ 9 : 1 | `DERIVATION` · E-3 / E-4 |
| E-8 | Order of construction | First agent code: SESSION 02, `63a22ac`, 2026-09-01. First CI workflow: `b742b00`, 2026-09-02 | `FACT` · `git log --reverse -- agent`, `-- .github/workflows` |
| E-9 | Human decisions recorded on agent proposals | Approval ledger `agent/implement/decisions/decisions.jsonl` **absent** (tracked path, never written). One governance grant | `FACT` · `cli.mjs corpus`, run 2026-09-29 |
| E-10 | Agent runtime in production | "No production dispatcher is wired" (`AGENTS.md:79–80`). Readiness "refuses", "seventeen and three" on 27 Sep (`AGENTS.md:119–136`) | `ATTRIBUTION` |
| E-11 | Evidence base, then and now | At `7248290`: claims 91, sources 77, unverified 106 (`docs/PROJECT-CONTEXT.md` §5). At `cc1f7d0`: claims 167, sources 189, unverified or requires-verification 47 | `ATTRIBUTION` (then) · `FACT` (now, `node tools/validate.mjs`) |
| E-12 | Factual corrections forced by reading primary texts | Concentrated on 26–27 Sep, e.g. `b4b6d76` ("nine months" → "some twenty months"), `ea6deba` (three, not four, categories), `591a6ee`, `705a689` | `FACT` · commit subjects |
| E-13 | Correction commits by session label | e.g. `4fe1952`, `d10b413`, `81a30eb`, `a25f0ed`. Each corrects a session report that stated more than was measured, or a placeholder that shipped | `FACT` · commit subjects |

### 1.3 What worked, and should be kept

Each lesson is `INTERPRETATION`. The Atlas status column says whether the Atlas already
has the lesson, and where.

| ID | Lesson | EU-DP evidence | Atlas status |
|---|---|---|---|
| K-1 | **Derive, never store,** anything computable from records (grades, status, counts) | `docs/AUDIT-2026-09-01.md` "What is genuinely sound": an independent re-implementation reproduced the grades byte-for-byte | Principle held: CLAUDE.md §7, MA §5.6. Not yet enforced; S06 onward |
| K-2 | **`null` ≠ `unknown` ≠ zero,** enforced in the derivation itself, not only in prose | same section: `pipeline.aggregate` returns an unaccounted-for count by construction | Principle held: MA §5.7. S01 map already uses the markers |
| K-3 | **Claim type and evidence status are two separate axes** | `docs/EVIDENCE-MODEL.md` §1, written 27 Sep 2026, a month into the project | MA §10 already separates them. Adopt from S06's first schema, not by retrofit (L-06) |
| K-4 | **An admitted gap beats a plausible substitute** | `docs/PROJECT-CONTEXT.md` §3.5 | Held: CLAUDE.md §5. S01 applied it (D-014, blocked sources left as gaps) |
| K-5 | **Controlled vocabulary checked by a validator** | `docs/PROJECT-CONTEXT.md` §3.4: all enum values resolve to `data/taxonomy.json` | Planned: S03/S04 vocabularies, S06 checks |
| K-6 | **Audits correct themselves in place and keep the error visible** | `docs/AUDIT-2026-09-01.md` F-01 is retracted but not deleted | Held: decisions log is append-only (D-001 to D-016) |
| K-7 | **A design rule that exists because of a shipped bug is written down with that bug** | `README.md:174` ("both have already shipped as bugs") | Keep as a convention in decision records |

### 1.4 What went wrong, and must not be repeated

| ID | Anti-pattern (`INTERPRETATION`) | Evidence | Mechanism |
|---|---|---|---|
| A-1 | **Control machinery outgrew the product and was never exercised.** An orchestrator, eleven agents, a control room and a production-readiness checklist were built. Not one human decision has been recorded on anything they proposed | E-3, E-7, E-9, E-10; `docs/GOVERNANCE-PROPOSALS.md` §0 | Machinery was built before one manual cycle of the workflow it automates had run end to end |
| A-2 | **Gates documented before they were enforced.** The README said a validator "can gate a commit". Nothing ran it | `docs/AUDIT-2026-09-01.md` F-02; E-8 (CI came after the first agent code) | Prose that describes a check is read as the check |
| A-3 | **A stale or parallel base read as a fact about the repository** | F-01, F-17; `docs/GOVERNANCE-PROPOSALS.md` P-01 (5 instances), P-05 (parallel branches built the same thing twice) | Nothing measured the base at session start. Nothing failed when it was stale |
| A-4 | **Counts typed into prose drift from the data they count** | F-08; P-04 (6 instances) | A derived value stored in Markdown: a second home |
| A-5 | **Second homes for facts,** including translations | F-04 (`window.__CONTENT__`); F-14 (three "as of" dates); `fd4aeb2` (three translations withdrawn because they still asserted facts the source language had corrected) | Each copy or locale is another place that has to be corrected when a fact changes |
| A-6 | **Lessons stranded on unmerged branches** | P-06: a rule took 23 days to reach `main`, recovered by a branch audit | The handover lived on the branch that was never merged |
| A-7 | **Reports claim more than was measured** | P-02 (4 instances); E-13 | Local exit codes reported as the CI result; placeholders shipped |
| A-8 | **Batch stamps disguised as per-record verification dates** | F-13: every `last_verified` is one of two sweep dates | The schema offered a per-record field that the process never filled per record |
| A-9 | **Factual errors surfaced only when primary texts were read, late** | E-11, E-12. Corrections cluster on 26–27 Sep, after the agent layer (E-8) | Effort went to machinery that checks the *form* of evidence. Reading sources checks its *content* |
| A-10 | **Orientation cost grows every session** | E-6: a 3,035-line single handover with sessions appended; a 727-line entry point | Per-session state accumulated in one file instead of in per-session records |
| A-11 | **No commit provenance at the start** | F-06: the first 47 commits were web-UI bulk uploads and deletions | No rollback unit smaller than the whole tree |

**What the benchmark does not show** (`INTERPRETATION`): that EU-DP's agent layer has no
value, or that its content is weak. E-11 shows real evidence gains. The finding is about
**sequence and proportion**: control machinery before a used decision loop, and form
checks before content checks.

### 1.5 Transfer to the Atlas

Each proposed commitment (`IMPLICATION`) is listed in decision **D-018**. That record is
its one home; the table only maps lesson to commitment and shows what the Atlas already has.

| Lesson | Already covered in the Atlas | Gap → proposed commitment (D-018) |
|---|---|---|
| A-1 | MA §11 roles; D-010 puts contracts in S06; S19 audits the agent system | No agent runtime before S19 has evidence of a manual workflow that needs one → **L-01** |
| A-2 | D-004: CI runs the validator on every push | A check exists only once CI runs it, and docs may not describe an unrun check as a gate → **L-02** |
| A-3 | CLAUDE.md §4 says inspect the branch | Each report records the base commit and the `git branch -a` result; the validator checks the field → **L-03** |
| A-4 | CLAUDE.md §7 | Counts in prose are either produced by a script or dated "as measured at `<commit>`" → **L-04** |
| A-5 | D-007 (baseline references MA); CLAUDE.md §7 | English only in v1 (NG-10); the validator's scope grows with each data file → **L-05** |
| K-3, A-8 | MA §10 | Claim type ≠ evidence status from the first schema; verification dates per record, never per batch → **L-06** |
| A-6, A-10 | Per-session reports (D-002); decisions log | Decisions and lessons only count once on `main`; no cumulative handover file → **L-07** |
| A-7 | Report template, SPEC §5 | Reports separate "run locally" from "CI result" → **L-08** |
| A-9 | S01 read full sources; D-014 | Content checks are budgeted before automation of the same step → **L-09** |
| A-11 | Git from S00 with described commits | none; already met |

---

## Part 2 — M0 milestone audit (PEF §4, eight questions)

1. **What was intended** (`SESSION-ROADMAP.md` M0):
   - S00: a runnable, documented, auditable repository;
   - S01: a defensible domain map with a source register;
   - S02: the architecture baseline tested against EU-DP, with non-goals frozen.
2. **What was implemented** (`FACT`):
   - Gate 0 validator + 10 unit tests + CI (S00);
   - domain map (46 concepts, 18 dependencies, 5 conflicts) and a source register (23
     sources) (S01);
   - decisions D-001 to D-016;
   - this audit and the proposals D-017 to D-021 (S02).
3. **What changed, and why:**
   - The first analytical question was fixed as global, with the EU lens later (D-008).
   - The bootstrap prompt was superseded by the session system (D-009).
   - Agent contracts were moved to S06 (D-010).
   - EDA/SME were split into sub-layers (D-013).
   - Terminology was fixed (D-016).
4. **Assumptions that failed** (from the S01 report):
   - primary sources are retrievable from this environment;
   - HBM is a memory-only layer;
   - advanced packaging is a back-end-only activity;
   - Part A's seven layers are exhaustive.
5. **Shortcuts taken:**
   - S01's evidence audit ran as a scratch script, not repository tooling;
   - `pypdf` was installed in the scratch area only;
   - the S01 and S02 prompts had no Claude-drafted 18-section Part B before the session
     started (S01's was drafted in S00; S02 has none — see the S02 report).
6. **Debt created:**
   - the scratch-only evidence checker (→ S06);
   - 5 undated live company pages (→ freshness check);
   - CSET 2019 data used for definitions;
   - D-014 and D-015 still `proposed`;
   - U-2 open until D-019 is decided.
7. **Removed or rejected:**
   - a root `AGENTS.md` (D-010);
   - placeholder directories (D-005);
   - a Python matrix and deploy jobs (D-004);
   - headless-browser retrieval (D-014);
   - WebFetch summaries as evidence (S01 report).
8. **Carry into M1:**
   - the frozen non-goals and boundaries (baseline §2, §6);
   - D-018 commitments L-01 to L-09;
   - the v1 concept classification (Part 4) as S03's starting input;
   - blocked sources and conflicts CON-01 to CON-05 for S05.

---

## Part 3 — Maturity baseline (PEF §3; 0 Absent · 1 Ad hoc · 2 Defined · 3 Controlled · 4 Exemplary)

This is the first rating. Later audits measure regressions against it. Where a
dimension is 0 **by design** (the session that builds it has not happened yet), it is
marked "not started". That is not a defect.

| Dimension | Process | Outcome | Evidence |
|---|---|---|---|
| Data architecture | 2 | 0 — not started | Conceptual contract in MA §5; D-005, D-007; no schema (S03/S04) |
| Content & review | 2 | 2 | S01: every source retrieved in full; 99 anchors machine-checked; 14 entries re-read, 3 fixed. The checker is scratch-only, so not 3 |
| Agent architecture | 1 | 0 — not started | Roles in CLAUDE.md §8 and MA §11; contracts deferred to S06 (D-010) |
| Analytical depth | 0 — not started | 0 — not started | S14–S16 |
| Code / engineering | 2 | 2 | `tools/validate_repo.py`, 10 tests, CI (D-003, D-004). Gate 0 is partial (baseline §5) |
| Product / user value | 2 | 0 — not started | The question is fixed (D-008); no user-facing output yet (S11) |
| Reproducibility | 2 | 1 | Immutable prompts, append-only decisions, reports enforced by CI. The S01 evidence audit is not reproducible from the repository |

---

## Part 4 — Proposed v1 concept classification (input to S03/S04; `INTERPRETATION`)

S01 proposed 40 concepts as v1 (after the TQ-07 move) and handed S02 the job of freezing
which ones S03/S04 must model. This is a proposal. **S03 owns the entity schema** and may
reclassify any row through a new decision record (D-020).

| Class | Meaning for S03/S04 | Concepts | n |
|---|---|---|---|
| **Model** | Must be representable as an entity or a relationship endpoint | ACC-01, ACC-02, ACC-03, ACC-05, HBM-02, HBM-03, HBM-04, PKG-03, PKG-04, PKG-05 (HBM stacking only), PKG-06 (multi-die package), FAB-02, FAB-03, SME-01, SME-03, SME-06, EDA-01, DC-01, DC-02, DC-05 | 20 |
| **Actor role** | A role a company holds, not a separate entity type. One firm can hold several roles (map §4, blurs B-2 and B-3) | ACC-04 fabless designer, HBM-06 memory manufacturer, PKG-07 OSAT, FAB-04 IDM, DC-04 cloud provider | 5 |
| **Attribute** | A field on another record, filled only where a source states it | FAB-05 vendor-named process (TQ-07), DC-06 rack-scale / liquid cooling, EN-03 rated power, EN-04 nameplate IT capacity (TQ-10) | 4 |
| **Energy, concept only** | Stays in the domain map. No records or edges in v1 (MA §6.4; NG-05) | EN-01 PUE, EN-02 grid interconnection | 2 |
| **Definitional** | A glossary / explanatory term with no record type of its own | X-01, HBM-01, PKG-01, PKG-02, FAB-01, SME-02, SME-04, EDA-03 (kept as dependency DEP-10), DC-03 | 9 |

**Why "actor role" matters** (`IMPLICATION`): MA §6.1 lists `CloudProvider` and
`EquipmentSupplier` as entity types. S01 found firms that span layers: cloud providers
design accelerators (B-2), and foundries and memory makers package (B-3). Typing a firm by
role would give one firm several records, and so several homes for its facts.
S03 should test MA §6.1 against this.
