# Architecture Decision Log

Append-only. A superseded decision is marked `superseded by D-NNN`, never rewritten
(`SESSION-PROMPT-SPEC.md` §6).

Status values: `proposed` (awaiting human review) · `accepted` · `superseded`.

---

## D-001 — Constitutional documents stay at the repository root

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** proposed
- **Context:** The user placed `CLAUDE.md`, `MASTER-ARCHITECTURE.md`,
  `SESSION-PROMPT-SPEC.md`, `PROJECT-EVALUATION-FRAMEWORK.md`, `SESSION-ROADMAP.md`,
  the operational roadmap and the bootstrap prompt at the root. Every document refers to
  them by bare filename, and Claude Code loads `CLAUDE.md` from the root.
- **Decision:** Leave them in place, unmodified. `docs/README.md` indexes them.
- **Rejected:** moving them under `docs/` — this would break cross-references and
  `CLAUDE.md` loading, and restructure human-authored documents without need.

## D-002 — Session system layout

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** proposed
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

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** proposed
- **Context:** Python is the intended language (MA §17). S00 needs only a structural
  validator and its tests.
- **Decision:** `tools/validate_repo.py` and `tests/` use the standard library (`unittest`,
  `pathlib`, `re`). No `pyproject.toml`, lockfile or third-party packages.
- **Rejected:** pytest, a linter/formatter, pre-commit hooks, a Makefile or a package
  layout. None has a current requirement; each can be added, with a recorded reason,
  when one appears (e.g. DuckDB in S14).

## D-004 — One CI job, read-only permissions

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** proposed
- **Decision:** `.github/workflows/ci.yml` runs the unit tests and the Gate 0 validator on
  every push and pull request, on Python 3.11 (the version the S00 checks were run on),
  with `contents: read` permission.
- **Rejected:** a Python version matrix, deployment/Pages jobs, scheduled runs. There is
  nothing to deploy and no compatibility requirement yet.

## D-005 — No placeholder directories or stub documents

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** proposed
- **Context:** CLAUDE.md §19 and MA §24 forbid adding infrastructure for appearance.
- **Decision:** Do not create `data/`, `schemas/`, `web/`, `analysis/` or empty stub
  documents. `docs/README.md` lists each planned artifact with its status and owning
  session; the session that first needs a directory creates and designs it.
- **Rejected:** a full scaffold of empty folders with `.gitkeep` files — it would fix a
  data layout before S03–S06 have designed one.

## D-006 — Independence from `Eu-Digital-Policy`

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** proposed (human confirmation required by S00 prompt)
- **Decision:** No file, code, folder structure, workflow or data was copied from
  `Eu-Digital-Policy`. That repository was not opened in S00. Methodological
  principles are taken only from this repository's own constitutional documents.
- **Consequence:** Any later reuse of a pattern from `Eu-Digital-Policy` must be
  reimplemented locally and recorded here (MA §4.2).

## D-007 — Baseline record references, not restates, the master architecture

- **Session:** S00 · **Date:** 2026-09-29 · **Status:** proposed
- **Decision:** `docs/architecture/baseline.md` cites MA/CLAUDE.md sections and records
  only repository state, gaps and uncertainties.
- **Rejected:** copying MA content into the baseline — it would create a second home for
  the same architectural statements, and the two would drift.
