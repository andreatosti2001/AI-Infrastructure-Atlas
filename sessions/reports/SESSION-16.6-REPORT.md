# SESSION-16.6 Report — Supplier-evidence rules and the HBM supplier research, redone

- **Session:** S16.6 · **Type:** ARCHITECTURE / RESEARCH · **Milestone:** between M4 and M5
- **Date:** 2026-10-07
- **Prompt:** [`sessions/prompts/S16.6-PROMPT.md`](../prompts/S16.6-PROMPT.md), from D-143.
- **Branch:** `claude/new-session-u2e1xq`. `main` holds S16 and S16.5 up to `eade6f5` (PR #28, merged by the
  human); this branch carries S16.5's last commit and S16.6.
- **Base** (D-018 L-03): `cdbd920`. 362 tests OK and Gate 0 OK, re-run on a clean checkout of `cdbd920`.
- **Commits:**
  - `b35d4be`: the prompt and the registry row;
  - `3c23995`: the proposed rule revision (R-1 to R-4);
  - `79174d2`: the rules as decided (D-144 to D-147), checks first;
  - `1ad67fa`: the search plan;
  - `f5f7e7e`: the records approved at H-2 and the criteria loaded into SQL;
  - `ccbbc2b`: the presentation proposal and its mock-up (H-3);
  - `a3143b0`: the supplier values set and drawn as "reported";
  - and the commit that adds D-148, D-149, the Samsung card, the break harness and its full run, the
    findings, this report and the state rows.

## Mission outcome

**Delivered.**

1. **The rules for supplier evidence** were proposed in plain language
   ([`supplier-evidence-rules-S16.6.md`](../../docs/research/supplier-evidence-rules-S16.6.md)) and decided by
   the human. Four changes, each with checks written first:
   - **historical values** (D-144): a supplier value may end at a date. It is then exempt from the 12-month
     rule, must be dated by its evidence, and is always shown with its period;
   - **teardowns** (D-145): an independent teardown of the named product may support its part's maker;
   - **sources registered when retrieved** (D-146): the Extractor's contract governs;
   - **third parties under the human's criteria** (D-147): recent where possible, internationally recognised
     as reliable, independent of the parties, and any unmet criterion stated. A value resting only on them
     is shown as **reported**.
2. **The research was redone** under those rules by Claude itself: a plan written first, 40 queries, 35
   retrieval attempts, the decisive anchors re-read in the retrieved bytes
   ([`hbm-supplier-research-S16.6.md`](../../docs/research/hbm-supplier-research-S16.6.md)).
3. **Both HBM suppliers are now named, as reported:**

| Part | Supplier now in the Atlas | Resting on | Shown as |
|---|---|---|---|
| HBM in the NVIDIA H100 | SK hynix, **historical, to 2024-03** | TrendForce, 2024-03-13: H100 HBM3 supply "primarily met by SK hynix" | reported · historical, to 2024-03 |
| HBM in AWS Trainium2 | Samsung Electronics | SemiAnalysis, 2025-12-04: Trn2's HBM speed "due to using memory supplied by Samsung" | reported · criterion not met: recognised |

4. **Their presentation** was proposed with a mock-up, chosen by the human, and built on both pages (D-148).
   The three supplier metrics stay "cannot be computed yet": neither report says its maker was the only one.

**In one sentence** (`INTERPRETATION`): the Atlas now records who third parties say made each HBM part, never
as a party's statement, with the H100's value bounded in time and Trainium2's carrying its unmet criterion;
no current H100 supplier is established.

**Decided by the human** (2026-10-07; outcomes only, D-114):

| Decision point | Outcome | Effect |
|---|---|---|
| H-1, the rules | historical values, teardowns and sources at retrieval adopted; the human set the criteria for third parties; a new label "reported" | D-144 to D-147 |
| H-2, the H100 | SK hynix, historical to 2024-03, reported by TrendForce | the H100's `supplier` field |
| H-2, Trainium2 | Samsung, reported by SemiAnalysis, recognition declared unmet; a Samsung Electronics company record | Trainium2's `supplier` field; the company record |
| H-3, the presentation | as in the preview, built now | D-148 |
| The refused memory-supplier card naming Samsung as a firm with no record | link Samsung's new record; the card stays refused | D-149 |

## Files changed

| File | Change |
|---|---|
| `sessions/prompts/S16.6-PROMPT.md`, `PROMPT-REGISTRY.md` | new prompt; one registry row |
| `docs/research/supplier-evidence-rules-S16.6.md` | new: the proposal, then the rulings |
| `docs/research/source-policy.md` | §2 teardown exception; the supplier matrix row; §7.1 (third-party criteria); §9 exception; §12 historical values |
| `docs/agents/contracts.md` | the Extractor registers sources when retrieved (D-146) |
| `schemas/claims.schema.json` | a citation's `third_party_criteria` (`recognised`, `independent`, each met with a reason) |
| `sessions/reports/SESSION-16.6-research/` | the search plan, the log, and `records.py` (the approved records, written once) |
| `data/sources.json`, `data/claims.json`, `data/companies.json` | 3 sources, 6 claims, 1 company (below) |
| `data/relationships.json` | the two HBM `supplier` fields |
| `data/refused_candidates.json` | `cand-002` links Samsung's record (D-149) |
| `tools/warehouse.py`, `docs/architecture/sql-layer.md` | the `citation_criteria` table |
| `sql/accelerator_dependencies.sql`, `sql/evidence_coverage.sql`, `sql/supplier_metrics.sql`, `sql/results/*.json` | the "reported" basis, the period and unmet criteria; a `reported` column; the status rule (D-148) |
| `tools/build_page.py`, `tools/page_template.html`, `site/hbm-chain/index.html` | a named supplier with its basis, period and criteria; the key line; the lane note; the criteria in the evidence panel |
| `tools/build_insight.py`, `tools/insight_template.html`, `site/hbm-insight/index.html` | the same in the research view; the double-line encoding; the supplier blocks |
| `docs/architecture/visual-architecture.md` §9 | rows for "reported" and "historical" |
| `docs/architecture/metrics.md` | coverage's `reported` column; the supplier metrics' status rule |
| `docs/architecture/decisions.md` | D-144 to D-149; D-104, D-120, D-128 and D-130 marked superseded in part |
| `docs/research/supplier-presentation-S16.6.md` and `sessions/reports/SESSION-16.6-qa/mockup/` | the H-3 proposal and its mock-up |
| `docs/research/hbm-supplier-research-S16.6.md` | new: the findings |
| tests | `test_source_policy.py`, `test_freshness.py`, `test_data_relationships.py`, `test_data_entities.py`, `test_data_candidates.py`, `test_claim_schema.py`, `test_warehouse.py`, `test_page.py`, `test_insight.py` |
| `sessions/reports/SESSION-16.6-breaks/`, `SESSION-16.6-qa/` | the harness with S16.6's breaks and its full run; the fail-first outputs; browser QA |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows |

`Eu-Digital-Policy`: not touched. No dependency added.

## Data changed

- **Sources** (registered at retrieval, D-146): `src-054` (TrendForce press release, 2024-03-13), `src-055`
  (SemiAnalysis, "AWS Trainium3 Deep Dive", 2025-12-04), `src-056` (Samsung Electronics 2025 Business Report,
  company-hosted).
- **Claims**, accepted by the human: TrendForce's and SemiAnalysis's statements (`ATTRIBUTION`, each with
  its criteria); Samsung Electronics's legal name, head office, country (`DERIVATION`) and memory products.
- **Company:** `company-samsung-electronics-co-ltd`.
- **Relationships:** the two HBM `supplier` fields, from `not_researched` to the values above.
- **Refused candidates:** `cand-002` names Samsung by its record; its reason "a firm has no record" is gone,
  and it stays refused because "memory" has no record.
- **Counts:** 56 sources, 127 claims, 9 companies, 5 relationships, 12 refused candidates.
- **Staging:** empty at the start and at the end.

## Tests run

| Command / check | Result |
|---|---|
| **At start** (`cdbd920`) | 362 tests OK; Gate 0 OK |
| **Fail-first**, each before its change | the rules ([`failfirst.txt`](./SESSION-16.6-qa/failfirst.txt)); the supplier values and their presentation ([`failfirst-supplier-values.txt`](./SESSION-16.6-qa/failfirst-supplier-values.txt)); the key line ([`failfirst-legend.txt`](./SESSION-16.6-qa/failfirst-legend.txt)); the Samsung card ([`failfirst-samsung-card.txt`](./SESSION-16.6-qa/failfirst-samsung-card.txt)). Each failed for its named reason |
| **At the end** | FINAL_SUITE |
| **S16.6's breaks** | NEW_BREAKS |
| **Merged break harness in full** | FULL_RUN |
| **Browser QA** at 1280 and 375 px, both pages | clean (below) |

**Browser QA** (Playwright from `/opt/node-tools`, the pre-installed Chromium; S14's script for the HBM page,
S15's for the research view with the filter extended to "reported"):

| Check | Research view, 1280 / 375 px | HBM page, 1280 / 375 px |
|---|---|---|
| Console, page errors | none | none |
| Document overflow; wide elements, also with every disclosure open | none | none |
| Marks reached by Tab | 16 of 16 | 17 of 17 |
| Enter on each mark lands on its evidence | all | all |
| Basis filter from the keyboard: stated, inferred, **reported**, gap | each shows only its rows and outlines only its marks | — |
| Lowest measured contrast | 6.21 | 6.21 |

Two rendering faults were found by looking at the screenshots and fixed before the end: the H100's supplier
box overflowed with its period on one line (the period now has its own line), and the research view split
"2024-03" across two lines (dates no longer wrap).

**The S16.6 breaks** ([`breaks.py`](./SESSION-16.6-breaks/breaks.py)):

BREAK_TABLE

## Evidence added/retired

- **Added:** `src-054`, `src-055`, `src-056` and their six claims.
- **Retrieved and logged, not registered:** the other retrieval attempts (T-01 to T-35), with hashes in the
  search log; their bytes are outside the repository.
- **Retired:** none. `claim-sk-hynix-hbm3-for-h100-2022` (S16.5) stays evidence linked to no edge: it states
  a plan (ER-8).

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-144 | historical supplier values | accepted (2026-10-07) |
| D-145 | independent teardowns as evidence of a part's maker | accepted (2026-10-07) |
| D-146 | sources registered when retrieved | accepted (2026-10-07) |
| D-147 | third parties under the human's criteria; the "reported" label | accepted (2026-10-07) |
| D-148 | how a reported supplier is shown; supersedes parts of D-104, D-120, D-128, D-130 | accepted (2026-10-07) |
| D-149 | the refused memory-supplier card links Samsung's record | accepted (2026-10-07) |

**Rejected alternatives:** third-party reports kept beside an unknown supplier; "inferred" for a reported
value; a coloured fill for "reported"; a reported supplier counted as a supplier count; the build stopping
for any named supplier; the Samsung card left contradicting the new record.

## Deviations

1. **The research view draws "reported" as a double line,** not the mock-up's dash-dot: its palette check
   (IN-7) forbids a new line pattern. The HBM page keeps the dash-dot box. Recorded in D-148.
2. **The lane's note changed.** SK hynix sits in the lane (with its M16 plant) and is now a reported supplier
   on the chain, so the note no longer says the lane's records are unlinked; it names the facility and the
   product. The rule that the lane's facility and product never link to the chain stands (D-148).
3. **A seventh decision point arose after H-3:** the Samsung card (D-149), found while checking the page.
   It was put to the human before any change.
4. **Twelve inherited breaks were replaced,** because S16.6 changed their setup text or meaning (named in
   `breaks.py`). The merged harness had silently given two S13 breaks the same ID each time; the
   replacements are keyed by description.

## Debt introduced/resolved

**Resolved:**

- S16.5's question whether third-party evidence can name a supplier (D-143), by D-144 to D-147;
- S16's debt row, a supplier metric's presentation once a supplier is named: designed (D-148);
- the Extractor's contract against "no `data/` edit before approval" (D-146);
- the page check "a gap drawn as zero" read a mark's text joined without spaces, so a 0 beside a word
  passed; it now reads each text node (found by the harness; caught on a broken copy, passes on the page).

**Introduced:**

| Item | Owner |
|---|---|
| The ID rule's legal-form list lacks "Co., Ltd.", so Samsung's ID keeps `co-ltd` | S22 engineering audit |
| SemiAnalysis's recognition is unmet; a recognised source naming Trainium2's HBM maker would confirm or replace it | the next supplier research |
| No current H100 supplier: only a historical value | the next supplier research; Change Detector (inactive) |
| TechInsights's H100 teardowns are paid; a reader with legitimate access could settle the H100 at product level | the human (RA-4), if access exists |
| Reuters, FT, WSJ and AP could not be searched: the search tool refused their domains | the next supplier research |
| `not_researched`'s definition against ER-3 (S16.5) | unchanged, S22 |

## Unresolved issues

- **No human decision is pending.**
- **Disagreement recorded, not resolved:** DIGITIMES (2023, a plan) says Samsung and SK hynix "will both
  supply" Trainium2's HBM3; SemiAnalysis (2025, past) names Samsung only. Neither excludes the other.
- Merging this branch into `main` is not asked here.

## Process lessons

- **Look at the screenshot, not only the numbers.** Both rendering faults passed every automated check.
- **A break that is not caught as named is a finding.** S13-4's replacement exposed the joined-text weakness
  in the zero check.
- **A new record can falsify an old card.** Creating Samsung's record made a refused candidate's reason
  untrue; RC-4 now catches a short form of a record's name.

## Implications for the next session

**For S17 (the policy entities, M5):**

- **The rules for supplier evidence as decided:** party statements as before; third parties under §7.1 with
  their criteria recorded; historical values with an end date.
- **Each HBM part's supplier outcome:** H100, SK hynix, historical to 2024-03, reported; Trainium2, Samsung
  Electronics, reported, recognition unmet.
- **What the policy layer can attach to:** company records (now including Samsung Electronics); product-level
  supply only as reported, and for the H100 only historically; company-level supply relations remain refused
  candidates (`cand-002` to `cand-006`).
- **Debt with owners:** above.
- **Files to read first:** this report; the rules proposal; the findings; the S17 entry of
  `SESSION-ROADMAP.md`.

**Recommended next decision** (asked at S17's opening, in the `CLAUDE.md` §9A format): which kind of policy
instrument S17 models first (for example export controls on advanced memory and accelerators, or public
support for memory manufacturing), so that its first records attach to the companies and parts this chain
already holds.
