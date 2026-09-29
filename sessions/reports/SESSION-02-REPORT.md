# SESSION-02 Report — Architecture baseline + process benchmark

- **Session:** S02 · **Type:** AUDIT / SYNTHESIS · **Milestone:** M0 — Project Constitution (`SESSION-ROADMAP.md` numbering; see D-019)
- **Date:** 2026-09-29
- **Prompt:** [`sessions/prompts/S02-PROMPT.md`](../prompts/S02-PROMPT.md)
- **Branch:** `claude/atlas-architecture-baseline-jow618`, from `main` @ `e071d4b`
- **Base at start** (D-018 L-03, done by hand):
  - `git branch -a` listed `main`, `origin/main` and `origin/claude/magical-galileo-vwn13j`;
  - the last of these has no commits that are not on `main`.
  - `Eu-Digital-Policy` was read at `origin/main` @ `cc1f7d0`.

## Mission outcome

**Delivered for human decision.** M0 is **not** complete. The prompt's closing line,
"Milestone M0 complete", depends on three human decisions. This session prepared them
but cannot make them.

| Prompt item | Result |
|---|---|
| Compare the planned architecture with lessons from `EU-Digital-Policy` | done: `docs/architecture/milestone-audits/M0-audit.md` Part 1 (13 measures, 7 keep-lessons, 11 anti-patterns, transfer table) |
| Human decision: approve project boundaries | **prepared**: `baseline.md` §2 + D-017; pending |
| Human decision: freeze non-goals | **prepared**: `baseline.md` §6 (NG-01 to NG-13) + D-021; pending |
| Human decision: approve the initial architecture baseline | **prepared**: `baseline.md` (status "proposed for approval", approval record §8) + D-018 to D-020; pending |
| Milestone M0 complete | **open** until `baseline.md` §8 reads `approved` in every row |

**Restated contract** (operating contract step 6):

- **Mission:** test the Atlas architecture against EU-DP's history without copying its
  implementation. Bring the baseline, the boundaries and the non-goals to the human for
  approval.
- **Scope:** reading both repositories; a process benchmark; the PEF §4 milestone audit;
  a first maturity rating; proposed decisions; baseline revisions. The S01 handoff's
  "freeze the v1 concept set" is treated as part of "approve project boundaries".
- **Non-goals:**
  - any write to `Eu-Digital-Policy`;
  - schemas and vocabularies (S03/S04);
  - source policy (S05);
  - tooling changes;
  - data;
  - any edit to the human-authored root documents;
  - deciding D-014/D-015 (a recommendation only).
- **Acceptance:**
  - the benchmark gives evidence for every lesson;
  - every proposed decision is recorded as `proposed`;
  - the baseline carries an approval record;
  - every cross-reference resolves;
  - tests and the Gate 0 validator pass;
  - this report satisfies SPEC §5 and the prompt's report list.
- **Plan** (it held, apart from Deviation 1):
  1. inspect both repositories;
  2. measure EU-DP;
  3. write the audit;
  4. append the decisions;
  5. revise the baseline and the index;
  6. check the cross-references;
  7. run the tests;
  8. write this report;
  9. commit and push.

## Files changed

Added:

- `sessions/prompts/S02-PROMPT.md`: the human prompt (see Deviation 2).
- `docs/architecture/milestone-audits/M0-audit.md`. It has four parts:
  - Part 1: the EU-DP process benchmark;
  - Part 2: the PEF §4 eight questions;
  - Part 3: the maturity baseline;
  - Part 4: the proposed v1 concept classification.
- `docs/quality/audit-history.md`: an index of audits (PEF §11), with one row.
- `sessions/reports/SESSION-02-REPORT.md`: this report.

Modified:

- `docs/architecture/baseline.md`:
  - status set to "proposed for approval";
  - §1 state table;
  - §2 boundaries restated once, with citations;
  - §3 agent-runtime line;
  - §5 `validate-i18n` row;
  - §6 replaced by the frozen non-goal list NG-01 to NG-13;
  - §7 U-2 and D-014/D-015 notes;
  - new §8 approval record.
- `docs/architecture/decisions.md`: D-017 to D-021 appended, all `proposed`.
- `docs/README.md`: three rows (baseline, milestone audits, audit history).

Not modified:

- root constitutional documents;
- `tools/`, `tests/`, CI;
- `docs/research/`;
- `sessions/prompts/PROMPT-REGISTRY.md` (it already lists S02);
- **anything in `Eu-Digital-Policy`**.

## Data changed

None. No canonical records, schema or data files exist, and none were created.

## Tests run

Python 3.11, from the repository root.

| Command / check | Result |
|---|---|
| `python -m unittest discover -s tests` (start) | OK (10 tests) |
| `python tools/validate_repo.py` (start) | `Repository integrity: OK` |
| Scratch cross-reference check (session scratch, not repository tooling). It checked that the concept IDs in Part 4 match the domain map's `v1` scope calls, and that every `D-`, `NG-`, `L-`, `A-`/`K-`/`E-` reference and every relative link in the changed docs resolves | 40 of 40 `v1` concepts classified, 0 duplicates, 0 missing; 0 unresolved references; 0 broken links |
| `python -m unittest discover -s tests` (final) | OK (10 tests) |
| `python tools/validate_repo.py` (final, with this report present) | `Repository integrity: OK` |
| CI result | not yet observed. The session reports local results only (D-018 L-08) |

Commands run against EU-DP (read-only; `git status` in that clone was empty afterwards):

- `node tools/validate.mjs`: 0 errors, 0 warnings, 47 unverified;
- `node agent/proposals/governance/cli.mjs corpus`: approval ledger `ABSENT`;
- `node agent/production/cli.mjs readiness`: **did not finish in 120 s**, abandoned; its
  figures are cited as `ATTRIBUTION`;
- `git log` / `wc -l` measurements.

Not applicable: schema, browser, accessibility, performance.

## Evidence added/retired

- **External sources:** none added. `source-register.md` is unchanged.
- **Repository evidence:**
  - The benchmark cites EU-DP by commit hash, path and line, or by a command and its
    output (audit §1.2, E-1 to E-13).
  - Each row is labelled `FACT`, `ATTRIBUTION` or `DERIVATION`. Lessons are
    `INTERPRETATION`, and commitments are `IMPLICATION`.
  - EU-DP's self-reports that were not re-measured are `ATTRIBUTION`: E-10, and the
    "then" half of E-11.
- **Retired:** none.

## Decisions made

All are **proposed**. None is in force until the human decides.

- **D-017:** project boundaries. They are stated once, in `baseline.md` §2. Energy stays
  concept-level in v1, because MA §6.4 outranks S01's `v1` energy calls.
- **D-018:** nine commitments, L-01 to L-09, drawn from the benchmark. The human can
  accept or reject each one.
- **D-019:** U-2 label convention. A bare `M0`–`M7` means the roadmap's milestones, and
  MA §22's are written "portfolio M…".
- **D-020:** the v1 concept classification is S03's starting input. It sorts the 40
  concepts as 20 model / 5 actor role / 4 attribute / 2 energy concept-only /
  9 definitional.
- **D-021:** non-goals NG-01 to NG-13 are frozen until v1.0. A change needs a prior
  decision record.

**Recommendation on D-014 and D-015** (the S01 handoff asked S02 to decide them; this
session only recommends):

- accept both as interim rules;
- mark them "superseded by S05's source policy" once that policy exists.

Leaving them `proposed` means that every `verified` marker in the S01 map rests on a
definition nobody has accepted.

### Rejected alternatives

- **Pushing to the branch designated in `Eu-Digital-Policy`.** It would break CLAUDE.md §3
  and MA §4.1. The human chose this repository instead (Deviation 1).
- **Copying EU-DP policy documents or validators as a starting point.** MA §4.2 and D-006
  forbid it.
- **One overall maturity score.** PEF §1 forbids collapsing the axes.
- **Rating EU-DP's maturity.** The benchmark is a process study. It is not an outcome
  audit of another product, and it would add nothing the Atlas needs.
- **Implementing L-03/L-04 checks in `tools/` now.** Tooling is out of this session's scope
  and the commitments are not yet accepted.
- **A separate benchmark document next to the audit.** The benchmark is Part 1 of the M0
  audit, so the evidence and the eight questions share one home.
- **Classifying the four energy concepts as `v1` records.** See D-017.

## Deviations

1. **Repository and branch** (SPEC §1: *scope violation* avoided).
   - The session's designated push branch was in `Eu-Digital-Policy`.
   - Writing Atlas records there would break the protection rule.
   - The session stopped and asked the human, who chose this repository.
   - The branch name `claude/atlas-architecture-baseline-jow618` was reused here.
     `Eu-Digital-Policy` was only read.
   - The EU-DP clone's local refs were deepened by a `git fetch` to read the full history.
     No file there changed.
2. **Prompt encoding.**
   - The prompt arrived with its UTF-8 punctuation mis-decoded as Windows-1252: "â€”" for
     "—", "â†’" for "→".
   - `S02-PROMPT.md` records the decoded text. The wording is unchanged, but the file is
     not byte-identical to what was received.
3. **No SPEC §2 Part B.**
   - S01's prompt had an 18-section Part B, drafted in S00. S02's prompt has only the
     human text.
   - The restated contract above stands in for it.
   - This makes S02's acceptance criteria weaker than SPEC §2 requires.
4. **Plan proposed but not held for approval.**
   - Operating-contract step 7 asks for a plan "before implementation". The only question
     put to the human was the destination (Deviation 1).
   - The rest of the plan was not presented for approval before writing.
   - Every output is a `proposed` document, so no approval boundary was crossed. It is
     still a deviation.
5. **"Milestone M0 complete" is not claimed.** It is a human gate. See Mission outcome.

## Debt introduced/resolved

**Introduced:**

- **The scratch cross-reference check.** It exists only in the session scratch area. A
  Gate 0 extension that checks decision and ID references would make it reproducible. It
  belongs with D-018 L-03 when accepted.
- **Stale scope calls in the domain map.** `domain-map.md` still shows `v1` on the four
  energy entries. D-020, once accepted, supersedes those scope calls without editing the
  S01 artifact. A reader of the map alone would not see this. S03 should add a pointer
  when it next revises the map.

**Resolved:**

- U-2 has a proposed resolution (D-019).
- The M0 audit artifacts that `docs/README.md` listed as planned now exist.

## Unresolved issues

### Evidence gaps

- **EU-DP production readiness** was not re-measured (the CLI timed out).
- **Branch-only work is outside the benchmark.** It covers `main` only. Of EU-DP's four
  remote branches besides `main`, one holds work that `main` lacks:
  `scout/digest-digest-2026-09-28T06-39-53Z`, 1 commit. That work is not included.
- **Open from S01, not touched by S02:**
  - blocked primary sources;
  - CON-01 to CON-05;
  - `not_researched` items.

### Human approvals required

1. **Project boundaries**: `baseline.md` §2 / D-017.
2. **Non-goals freeze**: `baseline.md` §6 / D-021. NG-08 (no agent runtime before S19)
   and NG-10 (English only) are new restrictions drawn from the benchmark. The rest
   restate MA, CLAUDE.md or accepted decisions.
   Also decide whether S00's "external API dependency" should become a v1.0 non-goal.
   It is deliberately not frozen (baseline §6, closing note).
3. **Baseline as a whole**: `baseline.md`, with:
   - D-018 (L-01 to L-09, item by item);
   - D-019;
   - D-020.
4. **D-014 and D-015**: accept as interim, or leave for S05 (recommendation above).
5. **S01 weekly gate**: still open.
6. **Merging this branch**: no pull request has been opened.

## Process lessons

- **The first stop condition fired before any file was written.** The designated branch
  was in the protected repository. Asking cost one question. Guessing would have put
  Atlas records into EU-DP, which is exactly A-5 and the repository-boundary failure the
  benchmark warns about.
- **Re-measure what you cite.** A benchmark of another project's self-audits is only as
  good as that re-measuring. Each figure was re-measured where the tree allowed it (E-9
  today, not the September claim). Where it did not (E-10), the figure is labelled
  `ATTRIBUTION`.
- **Check cross-references by script.** Mechanically checking identifiers across the
  documents took one script and found one false alarm: `TQ-07` matched as a concept ID.
  It is a cheap guard worth promoting.

## Implications for the next session

**Handoff: S03 — Entity taxonomy (ARCHITECTURE).** S03 starts only after `baseline.md` §8
is approved.

- **Completed work:**
  - the M0 audit and benchmark;
  - the baseline proposed for approval;
  - D-017 to D-021 (proposed).
- **Open issues:**
  - the §8 approvals;
  - D-014/D-015;
  - S01's weekly gate;
  - no Part B for S03's prompt yet.
- **Audit findings to carry:**
  - A-1 (sequence: machinery after a used loop);
  - A-5 (second homes);
  - the actor-role question in audit Part 4.
- **Recommended next decision:** the human approves or amends `baseline.md` §8. Then S03's
  prompt is written in SESSION-PROMPT-SPEC §2 form *before* S03 starts, with audit Part 4
  as its required input.
- **Files to read first:**
  1. this report;
  2. `docs/architecture/baseline.md` (§2, §6, §8);
  3. `docs/architecture/milestone-audits/M0-audit.md` (Part 4, then Part 1 §1.5);
  4. `docs/architecture/decisions.md` (D-017 to D-021);
  5. `docs/research/domain-map.md` (§2, §4, §7.1).
