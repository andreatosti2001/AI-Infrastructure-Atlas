# M5 Milestone Audit — Policy / Geopolitical Layer (S17 to S19)

> **Records cited.** This is a process audit (PEF §4). The session reports and prompts it cites are kept in the
> private development archive, not in this repository (D-151); the decisions, documents and files it cites are here.

**Status:** ACCEPTED by the human on 2026-10-14 (S19 H-2); M5 closes with this audit (D-187).
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4; `SESSION-PROMPT-SPEC.md` §4 (mandatory "after the first
policy layer" and "after any foundational schema change": the policy entity in S17, the policy level in S18).
**Written by:** Claude, as the Knowledge Architect; the human's review stands in for the Portfolio Reviewer
(baseline §5). The same model did the work it audits; counts below are recounted from Git and the checks.
**Base read:** `claude/new-session-vv78en` @ `cc4f44e`. M5's work reached `main` in PR #32 (S17, `5409747`) and
PR #33 (S18, `f6e6357`). S19's harness work and this audit are on the S19 branch.
**What this audit is:** an `INTERPRETATION` of the project's own record. The agent system is audited separately
in [`../agent-audit.md`](../agent-audit.md).

## Part 1 — The eight questions (PEF §4)

### 1. What was intended

The roadmap's M5:

- **S17:** "Introduce a policy layer connecting infrastructure dependencies to public policy without duplicating
  `EU-Digital-Policy`"; focus on industrial policy, export controls, strategic dependencies, investment,
  technology restrictions, public support.
- **S18:** "Model evidence-backed relationships between jurisdictions, companies, technologies and policy
  instruments". Gate: "Attribution and legal/policy status are explicit; analysis does not silently become legal
  advice".
- **S19:** the agent architecture audit (gate: "Any unnecessary agent or duplicate responsibility must be removed
  or justified"), opened by the three harness improvements (D-153) and closed by this audit.

### 2. What was implemented

| Session | Delivered | Record |
|---|---|---|
| S17 | the policy record (one published act, seven sourced fields, no stored status); legal dates as events; status derived by `tools/policy_status.py`; the class `official_legal_text`; eleven policy evidence rows; five no-advice rules; checks PL-1 to PL-9 written first; five US export-control acts canonical (5 sources, 37 claims, 11 events) | `policy-dataset.md`; D-153 to D-164; review entry of 2026-10-08 |
| S18 | `restricts` at a policy level, to the component and technology classes an act's own text names; the row `rel:restricts` (official text only); a later change to the same entry quoted, never dated on the link; refusals as records with two new reasons; navigation shows each link with its act's status and a no-advice line; no page shows a policy link; checks PK-1 to PK-7 written first; four links, 10 claims, 9 refusals canonical | `policy-links.md`; D-165 to D-174; review entry of 2026-10-13 |
| S19 | 28 breaks checked on every commit; break selection by measured files; a parallel runner; the full harness run; the agent audit; this audit | D-175 to D-179; `tests/regression/README.md`; `agent-audit.md` |

**Against the gates:**

- **S17's mission is met for export controls only.** Industrial policy, investment and public support have no
  record yet; the record design holds them (P-2), and `supports` is defined but unused (D-160).
- **S18's gate is met.** Each link rests on its act's own words as an `ATTRIBUTION` and on a separate
  `DERIVATION` matching the act's word to the record's name (PK-3, PK-4); the act's status is derived on a date,
  never stored (PL-1, D-156); navigation prints "describes the text; does not advise" (PK-6, LA-5). Jurisdictions
  are linked as issuers (PL-3), not by relationships (D-170), and companies are not linked (D-166).
- **S19's gate is met:** every role has a ruling, the Analyst is activated, every file has an owner, checked
  (`agent-audit.md` §4; D-180 to D-184).

**M5's full harness run** (D-150, D-179), on `04166fc`, the tree after S19's remediations: **116 of 116 faults
caught as named, 14 of 14 controls passing**, with the new runner (`--jobs 4`, 34.5 minutes). The old runner, run on
the same tree as four processes split by hand (36 minutes), gave the same verdict and the same failing tests for all
130 breaks. The 28 permanent breaks are among the caught.

**Counts** (recounted from `data/` at each merge): canonical records, sources included, 238 → 296 (S17) → 319
(S18). Tests 374 → 396 → 411 → 413 (S19). Breaks 107 → 119 → 130.

### 3. What changed, and why

- **The first instruments were chosen by the evidence available** (D-153): export controls, because their
  official texts name parts of the chain. EU instruments are excluded until a supranational jurisdiction exists
  (D-154), which keeps the boundary with `Eu-Digital-Policy` mechanical (PL-3).
- **Status became a derivation, not a field** (D-156): an act's status on any day is computed from dated events.
  This is the Atlas's first rule-based derivation over legal time.
- **A design question appeared while writing the checks** (D-164): EV-3 would have refused every effective date
  fixed in advance. It went to the human before any check was written.
- **S18 linked classes, not products** (D-165): none of the five texts names an Atlas product or company. The
  roadmap's example ("restricts / supports → technology or supply-chain layer") was met at the class level only.
- **A later act's change became a quoted claim, not a date on the link** (D-169), after the 2023 rule's removal of
  the 2022 entry 3B090 made the time question concrete.
- **The harness changed shape in S19** (D-176 to D-179): per-commit tests for data faults, measured selection,
  parallel copies.

### 4. Which assumptions failed

| Assumption | What happened | Record |
|---|---|---|
| The Federal Register API's summary gives an act's dates | its single `effective_on` contradicts the text, which fixes three dates | S17, search log L-1 to L-5 |
| The existing event checks would accept policy dates | EV-3 refused effective dates fixed in advance | S17; D-164 |
| An anchor found verbatim means the statement is supported | three statements said more than their verbatim anchors | S17, Verifier |
| S18 would link rules to named products | no text names an Atlas product or company | S18 H-0; D-165 |
| A control entry is stable between acts | the 2023 rule removed 3B090; the 2024 rule changed 3B001 and 3B002 | S18; D-169 |
| The rule's HBM is the Atlas's HBM | the 2024 rule's is wider at one edge (DRAM ICs regardless of JEDEC conformance) | S18, the term-match claim |
| A script can read every break's setup | five setups were unreadable; S17 and S18 added them by hand | S17, S18; D-177 |
| One check ID names one check | PL-1 names the edge guard (`edge-dataset.md` §7) and the policy shape (`policy-dataset.md` P-10) | S18 |
| A fixture source ID is unique across fixture worlds | `src-917` is defined twice with different classes | S18 |
| An expected fragment matches the suite's output line | unittest wrapped S17-7's fragment | S17 (`217758b`) |

### 5. Which shortcuts were taken

- **No search for later acts or repeals.** "No later change recorded in the Atlas" rests on no dated search after
  5 December 2024 (rejected at S17, D-156; recorded at S19, D-175).
- **The texts were read before the plans** in S17 and S18, to make the human's opening choice concrete; the
  records rest only on the planned retrieval and re-read.
- **Selected breaks, not the full harness,** in S17 and S18 (D-150), chosen by a private script with hand
  additions. S19 runs the full harness.
- **The term guard is a word match** (PK-4): it cannot tell a scope word from a different class; the Verifier and
  the human remain the check.
- **Two S18 design questions with no real alternative were grouped** in one interactive question, each listed
  with its consequence.
- **Archive commits stayed on session branches,** not on the archive's `main` (S17, S18): the session's git
  instructions limit pushes; merging is the human's.

### 6. What technical and research debt was created

| Debt | Owner (proposed where S19 is the owner) | Record |
|---|---|---|
| No dated search for later BIS rules changing 3A090.c, 3B001, 3B002, 3B993 or repealing the five acts | the next policy research session, as the Change Detector's first task | D-175; `agent-audit.md` F-6 |
| Product and company targets, and their party-statement evidence row | the session that records the first one | D-166 |
| No page design for policy links | S20 or the human | D-173 |
| The term guard is a word match | the session that adds the next policy link; the Verifier and the human stay the check | S18; PK-4 |
| The EAR record has no dates | the next policy research | S17 |
| 2023-23055's instruction-level end date lives only in a claim | the session that links that instruction | S17 |
| Three rules' country joins two texts; an official text's publisher is an edition's name | S22 | S17 |
| The AI Diffusion rule (90 FR 4544) and its reported withdrawal not researched | the next policy research | S17 |
| The 2024 rule's HBM wider than the working definition (stated in the claim) | S22 may revisit the working definition | S18 |
| The Verifier's re-read is a private, rewritten script | the next session that adds claims from a new retrieval | `agent-audit.md` F-4 |

**Resolved in M5:** D-022, D-023 and D-030's policy reservations (S17); the normative-text question (S17); S17-11's
navigation interaction (S18); computed break selection's blind spots (D-177); the three harness improvements
(D-176 to D-179); PL-1's double use (renamed PN-1, D-185); `src-917` defined twice (the edge fixture's is
`src-919`, D-186); the unowned files and the Analyst without a contract (D-180, D-181).

### 7. What was removed or rejected

- **Record designs:** one record per policy area or per provision; a stored status; a `NORMATIVE` claim type;
  official texts kept as `government_publication`; institution records; bare EU records by reference (D-154 to
  D-159).
- **Link designs:** `regulated_by` and `constrained_by` (D-160); two verbs instead of a level; a broader term that
  contains the record; structured scope fields; an end date from a later act; refusing a link whose entry was
  later removed; refusals only in the log; navigation ignoring policy links (D-166 to D-173).
- **Research scope:** public support first; a dated repeal search on every record (S17); the later-rule search in
  S19 (D-175).
- **Harness:** declared file lists; a sample equivalence check; leaving D-150 unchanged (D-176 to D-179).

### 8. What should be carried into the next phase

**The policy rules:**

- an act is recorded from its official text only; any other class may point to it, never date or repeal it;
- status is derived on a date from events, never stored, never advice;
- a link quotes the act's own word, and a separate `DERIVATION` matches it to the record's name or an alias;
- a later change to an entry is quoted, never inferred into a date;
- a refused candidate is a record, with its reason.

**Into M6 (S20, S21):**

- **A UX must show the policy layer's limits:** no page design for policy links yet (D-173), class-level links
  only, and "no later change recorded" for an unsearched period.
- **The harness as ruled:** run the breaks a change selects (`--since`), the full harness when a check changes;
  28 data faults are in CI.

## Part 2 — Process findings (PEF §4, §12)

| ID | Finding | Evidence | Disposition |
|---|---|---|---|
| M5-P1 | **Reading the source before asking made decisions concrete.** S17's EV-3 gap and S18's "no text names a product" were found by reading, and settled faster than abstract options | S17 D-164; S18 H-0 | standing practice |
| M5-P2 | **Checks written first found a real bug**: the status tool ignored a repeal whose month contains the date | S17 report, "After the schema" | standing practice (D-162, D-174) |
| M5-P3 | **Duplicate identifiers survived review**: the check ID PL-1 twice, the fixture `src-917` twice. No check reads either | `edge-dataset.md` §7, `policy-dataset.md` P-10; `tests/fixtures/` | remediated in S19 (D-185, D-186) |
| M5-P4 | **The milestone audit was planned this time** (M4-P3): S19 carried it in its prompt | S19 prompt; this file | resolved |
| M5-P5 | **Session tooling was private and rewritten each time**: break selection (resolved, D-177) and the Verifier's re-read (`agent-audit.md` F-4) | S17, S18 research and break folders | see F-4 |

## Part 3 — Maturity (PEF §3), where M5 produced new evidence

| Dimension | Rating | Evidence |
|---|---|---|
| Data architecture: outcome | **3, Controlled** | status derived from events (`policy_status.py`, PL-7); no stored status (PL-1 schema); temporal change handled as quoted claims (D-169); refusals as records (PK-7); every rule checked in CI |
| Content & review: outcome (policy layer) | **3, Controlled**, with a stated limit | every policy claim from an official text, re-read in registered bytes, reviewed by the human; limit: no search after 5 December 2024 (D-175) |
| Agent architecture: process | **3, Controlled** (2 at the audit) | contracts exist and are checked; the write boundaries drifted unchecked from S12 to S18 (`agent-audit.md` F-2) and are now checked: every tracked file has an owner (D-180) |
| Code / engineering: process | **3, Controlled** | checks written first in S17 and S18; 28 data faults in CI; selection without blind spots; equivalence shown break by break (D-179) |

## Part 4 — Findings and debt

The agent audit's F-2 and F-3 were **blocking** and are remediated (D-180, D-181); M5-P3 is remediated (D-185,
D-186); the rest is **debt** with the owners in Part 1 §6. **M5 is closed** with this audit (D-187).
