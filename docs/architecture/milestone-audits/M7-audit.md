# M7 Milestone Audit — Final Audits and Release (S22 to S25)

> **Records cited.** This is a process audit (PEF §4). The session reports and prompts it cites are kept in the
> private development archive, not in this repository (D-151); the decisions, documents and files it cites are here.

**Status:** ACCEPTED by the human on 2026-10-16 (S25 H-3, D-230); M7 closes with this audit. Written in S25, the
milestone's last session, as M6-P5 asked: "the last session of a milestone carries its audit".
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4 (a milestone audit at every major milestone); S24's prompt
§08 ("it closes with S25").
**Written by:** Claude, as the Knowledge Architect. The same model did the work it audits; counts are recounted from
Git, the checks and the session reports.
**Base read:** `claude/new-session-4ip8g6` during S25. M7's work before S25 reached `main` in PR #39 (S22), #40 (S22.5),
#41 (S23) and #42 (S24).
**What this audit is:** an `INTERPRETATION` of the project's own record. The milestone's outcome is rated in the
[final process and outcome audit](../final-audit.md); this audit is about how M7 went.

## Part 1 — The eight questions (PEF §4)

### 1. What was intended

The roadmap's M7, "Final Audits + Release": three audits, each with its own question, then a release.

- **S22:** audit the repository as an engineered system (twelve points).
- **S23:** does the project show real domain depth rather than surface-level web research (seven points)?
- **S24:** does it communicate professional capability through its result and its development history (eight points)?
- **S25:** freeze a coherent v1.0, with nine outputs and an exit condition that another person must meet.

Added during the milestone by the human: **S22.5** (D-216), to close the engineering findings outside v1.5;
**v1.0's known limitations** written and audited in S24 rather than at the release (D-222); **publication** of the
pages at the release (D-226).

### 2. What was implemented

| Session | Delivered | Record |
|---|---|---|
| S22 | the engineering audit (14 findings, one blocking: browser checks that could not fail) and M6's audit; browser checks that fail by name, in CI on three engines; the later-rule search as a tool; `check_all.py` | [engineering audit](../engineering-audit.md); D-211 to D-214 |
| S22.5 | F-2, F-5, F-12, F-14 remediated checks first; F-1, F-4, F-7, F-11 and F-13's print half re-verified; CI's actions pinned by commit | D-216, D-217 |
| S23 | the release content audit: 59 weight-bearing and 30 drawn claims read in full, 203 quoted passages searched for again; BIS's May 2025 announcement recorded; values past the freshness horizon marked | [release content audit](../../research/release-content-audit.md); D-218 to D-221 |
| S24 | the portfolio audit, with two first-time readers; every PEF dimension rated; v1.0's known limitations, tied to the pages sentence by sentence; the Portfolio Reviewer active; the README's account of how the Atlas was built | [portfolio audit](../portfolio-audit.md); [known limitations](../../known-limitations.md); D-222 to D-226 |
| S25 | publication of the release commit, checked at its address; the nine release outputs; this audit; the exit-condition reading | D-227 to D-229; [release notes](../../release/release-notes.md) |

**Against the gates:** each audit was accepted by the human with no blocking finding left open (D-213, D-218, D-224).
S22.5's gate was met (D-216). S25's acceptance is H-3's.

**Counts** (recounted from the session reports and the checks):

- **Tests:** 466 → 483 (S22) → 487 (S22.5) → 489 (S23) → 498 (S24) → 506 (S25).
- **Breaks:** 178 → 197 → 208 → 212 → 222 → 230. Each full run was clean: 175 of 175, 185 of 185, 188 of 188 and
  197 of 197 faults caught as named; S25's run is in its report.
- **Records:** sources 64 → 65, claims 196 → 197, events 19 → 20, all in S23 on the human's verdict (D-220).
- **Decisions:** D-211 to D-229.

### 3. What changed, and why

- **S22.5 was inserted** (D-216) because the human chose to close the engineering findings before the content audit,
  rather than leave four of them to v1.5's opening as D-213 had ruled.
- **The known limitations moved from S25 to S24** (D-222), so that an independent look (S24's audit) would check them
  before the release rather than S25 writing them once.
- **S24 remediated its own findings** on the human's ruling (D-224): the README says who drafted and who decided, the
  brief warns that a reported supplier is not the only one, and the pages say that a text a later rule cites is unread.
- **The release gained a public address** (D-226, D-227): both first-time readers in S24 named a live page as what
  would most change their view.

### 4. Which assumptions failed

- "Each session opens on a later day than its predecessor": S22, S22.5 and S23 all ran on 2026-10-15, so two search
  windows were empty (D-211; S23's Deviation 1).
- "The prompt's base is `main`": S24 found S23's last commit missing from `main`. S25's base moved during its opening,
  when PR #42 was merged (P-9).
- "Green browser runs mean the pages pass": the scripts could not fail (S22, F-1).
- "The filter is at risk in other engines": all three engines support `:has()` (S22).
- "BIS's May 2025 guidance can only be a pointer": the page was retrievable and was recorded (S23, D-220).
- "The pages state the gaps D-218 lists": most appeared only as labels, and one on no page (S24, P-14).
- "The archive's report rule is enforced": nothing checks it since the reports left the public repository (S24, P-8).

### 5. Which shortcuts were taken

- Firefox and WebKit ran only in CI; the session container has Chromium alone (S22 to S25).
- The full harness ran once per session, after every check change, rather than after each change (S22, S23).
- The exit condition was tested by two fresh AI readers, not by people (D-228).
- The CI actions that target Node.js 20 were pinned, not upgraded (S22.5; D-217's upgrade rule).

### 6. What technical and research debt was created

Listed with owners in the [final process and outcome audit, Part 4](../final-audit.md#4-what-stays-open) (P-2, P-5b,
P-6, P-11, the v1.5 visual items, F-3, Node.js 20) and in the [research backlog](../../research/backlog.md) (the
research gaps no planned session closes).

### 7. What was removed or rejected

The CFR finding-aid PDFs as the search tool's second register (D-211); manual browser checks (D-212); pip hashes
(D-217); registering the `media.bis.gov` copy of BIS's announcement (D-220); refreshing Micron's values before v1.0
(D-221); a capability score, an agent runtime, and publishing the session reports (S24, D-224); publishing `site/`
alone, publishing every merge to `main`, and a redirect page at the address's root (D-227).

### 8. What should be carried into the next phase

- **To v1.5's opening (S26):** the five rule decisions of `VERSION-ROADMAP.md` §2; the visual debt (F-6, F-8, F-9,
  F-10, A-4, dark mode, P-5b); the Node.js 20 actions; whether a person reviews a sample of the code (P-2); the
  backlog's RB-1 beside the measured-data session.
- **To v2's opening (S32):** coverage, review capacity and agent activation (`VERSION-ROADMAP.md` §3); P-6 (an
  analysis layer); P-11; the backlog's RB-2, RB-4 and RB-5.
- **Standing practice:** re-measure the base at every opening, including during it; show every new check failing
  first; ask a first-time reader before a release.

## Part 2 — Process findings (PEF §4, §12)

| ID | Finding | Evidence | Disposition |
|---|---|---|---|
| M7-P1 | **Audits of different kinds found different things.** The engineering audit found checks that could not fail; the content audit found sources that had begun refusing automated requests and an opposing official text the Atlas lacked; the portfolio audit found the front door hiding the evidence and the authorship | F-1; S23 C-1, DT-S23-2; S24 P-1, P-3 | standing practice: audit by kind before a release |
| M7-P2 | **Handoffs still race the merge.** PR #42 was merged during S25's opening, after S24 had found the same race | S24 P-9; S25's opening record | standing practice: re-measure the base at the opening and again before the first commit |
| M7-P3 | **The milestone closed with its audit**, as M6-P5 asked; M3, M4 and M6 had not | this audit; `audit-history.md` | resolved |
| M7-P4 | **Five sessions in two days, with no review of the code by a person.** The checks carried the review | S24 Part 4 (P-2) | the human's: a review rule at v1.5's opening or later |
| M7-P5 | **The checks prove provenance, not truth.** Two query-tutorial sentences shown on the research view had stopped being true (the suppliers "not researched"; "fourteen" undated sources) without any check failing; a first-time reader of the release found the first | S25's exit reading (fresh reader 2, field 4); D-230 | remediated in S25: both reworded so that they state no value that can drift; v1.5's design review should read the tutorials as text |

## Part 3 — Maturity

M7 produced no new rating beyond S24's, which covers every dimension. The ratings at the release, and what changed
after S24, are in the [final process and outcome audit](../final-audit.md).

## Part 4 — Findings and debt

No blocking finding is open. **M7 is closed** with this audit (D-230).
