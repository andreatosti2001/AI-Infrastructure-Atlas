# Final process and outcome audit — v1.0

- **Status:** proposed (S25, 2026-10-16), for the human's acceptance with the release (S25 H-3). Written by the
  Knowledge Architect (D-229).
- **What it is:** the pre-release dual audit of PEF §4, as a synthesis. M7 audited the release three times, each audit
  accepted by the human: S22 the code and engineering ([engineering audit](engineering-audit.md), D-213), S23 the
  content ([release content audit](../research/release-content-audit.md), D-218), and S24 the capability shown and
  every PEF dimension ([portfolio audit](portfolio-audit.md), D-224). This document states their conclusions side by
  side, the process axis apart from the outcome axis (PEF §1). It re-measures only what changed after them, and
  rates nothing anew.
- **Claim discipline:** ratings and readings are the audits' `INTERPRETATION`. Counts are measured, each naming its
  source.

## 1. Process: how v1.0 was built

| Dimension (PEF §2) | Rating | Rated in | The evidence, in one line |
|---|---|---|---|
| Data architecture | 3, Controlled | S24 Part 6 (3 since M2) | 19 of 19 schema commits name a decision; no canonical claim or source ever removed or reworded |
| Content and review | 3, Controlled | S24 (3 since S13) | sources registered with hashes; every claim verified by re-read and reviewed by the human; opposing evidence sought (S23 C-1) |
| Agent architecture | 3, Controlled | S24 | roles as contracts, checked in CI; drafts always in staging; the Portfolio Reviewer active from S24 |
| Analytical depth | 3, Controlled | S24 (3 since M4) | metrics defined by question, population and denominator before they were built (S15, S16) |
| Code and engineering | 3, Controlled | S22, S24 | checks shown failing first in 27 of 30 reports; a full break run for every check change; but no person reviews the code (P-2) |
| Product and user value | 3, Controlled | S24 (3 since M6) | each page built from a recorded question; the framework decision taken on evidence (D-200) |
| Reproducibility | 3, Controlled | S24 (3 since M2) | every decision with its context; nearly all with rejected alternatives; prompts and reports archived (privately, P-13) |
| Learning progression of the owner | not rated | S24 | the repository records the human's decisions and verdicts, not what the human learned: unknown, not inferred |

**Process in one sentence** (`INTERPRETATION`, S24 Part 4): a disciplined, very fast build, drafted by an AI model
under the human's governance. Decisions, schema changes and claims were controlled and recorded, rework was rare and
checks came before code. Its weaknesses: no person reviewed the code, and two controls lived outside CI and decayed
(the archive's report fields, P-8; merges racing session handoffs, P-9).

## 2. Outcome: what v1.0 is

| Dimension (PEF §2) | Rating | Rated in | The evidence, in one line |
|---|---|---|---|
| Data architecture | 3, Controlled | S24 (3 since M5) | one home per fact; explicit unknowns; derived statuses; all checked. Not 4: untested at v2's scale |
| Content and review | 2, Defined | S23, unchanged in S24 | 178 of 178 readable anchors found at their locators; 0 of 85 judged claims exceed their evidence; but coverage is narrow and every value is single-voiced |
| Agent architecture | 3, Controlled | S24 (up from 2) | eleven contracts with MA's fields; every file owned; no silent promotion. Not 4: every role is one model in one session, and exclusivity is unchecked (P-11) |
| Analytical depth | 3, Controlled | S24 | metrics reproducible and recomputed independently; every query states what it does not prove (WH-16) |
| Code and engineering | 3, Controlled | S24 (left open by D-216) | the S22 findings outside v1.5 remediated, checks first; builds byte-identical across interpreters; checks that fail, in CI on three engines |
| Product and user value | 2, Defined | S24 (2 since M6) | 18 pages, each answering a recorded question; but no outside person has used them, and two first-time readers found the brief thin, dated and coded |
| Reproducibility | 3, Controlled | S24 (3 since M2) | every page rebuilt byte for byte from digested inputs, locally and in CI; exact pins. Not 4: no reproduction by another person |

**Outcome in one sentence** (`INTERPRETATION`): v1.0 is accurate, checkable and honest about its limits, and narrow.
Its depth is of method, not of coverage. It is a well-sourced fact base and an engineering demonstration, not yet a
product that outside readers use.

## 3. What changed after the audits (measured in S25)

| What | Before | At the release | Source |
|---|---|---|---|
| Test methods (unit suite) | 498 (S24's end) | 506: PA-1 to PA-3 and PW-1 (8 methods) | `python -m unittest discover -s tests` |
| Breaks in the harness | 222 | 230: S25-1 to S25-7, the control S25-C1; S14.5-F1 replaced | `tests/regression/breaks.py --setup-only` |
| Public address | none (P-3) | the release commit's pages and the files they link to, checked byte for byte (D-227) | `tools/check_published.py` |
| Known limitations | 15 gaps, 5 boundaries | the same rows; KL-15 keeps its outside-reader half | [`known-limitations.md`](../known-limitations.md) |
| Records, claims, sources, statuses | — | unchanged | `git diff` of `data/` over S25: empty |

The publication removes one of the two reasons S24 gave for the product outcome rating of 2 (no public address). The
other reason stands: no person outside the project is recorded as having used the Atlas. S25 does not re-rate. The
exit-condition reading of two fresh AI readers is reported in the [case study](../case-study.md); it tests whether
the release can be understood, not whether it is used.

## 4. What stays open

Each item is owned. Nothing here blocks v1.0: S22, S23 and S24 each found no blocking finding open at their
acceptance.

| Item | What it is | Owner | Record |
|---|---|---|---|
| P-2 | no review of the code by a person is recorded | the human: a review rule, at v1.5's opening or later | portfolio audit; D-224 |
| P-6 | policy shown as description and change tracking, not analysis | v2's opening: an analysis layer of labelled interpretations | portfolio audit; D-224 |
| P-11 | the owner check proves an owner exists, not that it is the only one | v2's agent activation | portfolio audit; D-201 |
| P-5b | the brief's first screen and summary composition | v1.5 | portfolio audit |
| F-6, F-8, F-9, F-10, F-13 screen (A-4), dark mode | the timeline on a phone, one large base class, two composition styles, no pixel comparison, evidence repeated on screen | v1.5 | engineering audit; D-213 |
| F-3 (E-1) | the HBM page's specification names `cand-001`; a test stops the builds by name when it is resolved | the session that resolves it | D-216 |
| Node 20 in CI | CI warns that the pinned checkout and setup-python target Node.js 20; the runner forces Node.js 24, and every run passes | the Data Auditor, at v1.5's opening (an upgrade changes the actions' behaviour, D-217) | S22.5's debt; this audit |
| Research gaps | KL-01 to KL-15 | as each row names; the unplanned ones placed in the [research backlog](../research/backlog.md) | [`known-limitations.md`](../known-limitations.md) |
