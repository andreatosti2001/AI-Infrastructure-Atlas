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
