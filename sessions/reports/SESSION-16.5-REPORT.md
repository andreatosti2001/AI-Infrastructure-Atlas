# SESSION-16.5 Report — Milestone audits and HBM supplier research

- **Session:** S16.5 · **Type:** RESEARCH, with an AUDIT opening · **Milestone:** M4 (closed here), before
  M5
- **Date:** 2026-10-07
- **Prompt:** [`sessions/prompts/S16.5-PROMPT.md`](../prompts/S16.5-PROMPT.md). Claude assembled it from
  D-139 and D-140 when the human asked for S16.5 to start once its prompt was generated. That instruction is
  recorded as the confirmation of Part A.
- **Branch:** `claude/new-session-u2e1xq`, continuing after S16. PR #28 (S16) was open and not merged, so
  S16.5's commits are on the same PR.
- **Base** (D-018 L-03), at the start:
  - `git branch -a`: this branch and `main`, with their remotes;
  - `git ls-remote`: `main` and `HEAD` at `1ca2e89`; this branch at `a203265`; three older `claude/*`
    branches;
  - 361 tests OK; Gate 0 OK; the three `--check` commands up to date.
- **Commits:**
  - `a203265`: the prompt and the registry row;
  - `c7574ee`: the M3 and M4 audits and the search plan;
  - `53fa6bc`: the audits accepted;
  - `ca42d07`: the search log and the research findings;
  - `eade6f5`: D-141, D-142, the data, the schema line, the rebuild and the S16.5 breaks;
  - and the commit that adds the full break run, D-143, this report and the state rows.

## Mission outcome

**Delivered.**

1. **The M3 and M4 milestone audits** (D-140) were written and accepted by the human on 2026-10-07. M4 is
   closed. Neither audit found a blocking issue.
2. **The supplier research** (D-139) was done by Claude itself: a search plan written first, 28 queries,
   51 retrieval attempts, and the decisive quotes re-read in the retrieved bytes.

| Part | What the Atlas now knows | Outcome (D-141) |
|---|---|---|
| HBM in the NVIDIA H100 | SK hynix stated on 2022-06-08 that its HBM3 was "to be combined with NVIDIA H100 Tensor Core GPU". That is more than 12 months older than its verification, so F-1 refuses it as a supplier value. NVIDIA's FY2026 10-K names SK Hynix, Micron and Samsung as memory suppliers at company level only (ER-9) | supplier stays `not_researched`. The 2022 statement is kept as canonical evidence (`src-053`, `claim-sk-hynix-hbm3-for-h100-2022`) |
| HBM in AWS Trainium2 | no party names the memory maker | supplier stays `not_researched`, with the research recorded |

**In one sentence** (`INTERPRETATION`): no evidence fresh and specific enough to name either memory supplier
was found. One stale statement is now held as evidence, and the access gaps that kept the search incomplete
are recorded.

**Decided by the human** (2026-10-07; outcomes only, D-114):

| Decision point | Outcome | Effect |
|---|---|---|
| Part A | confirmed by the instruction to start once the prompt was generated | prompt unchanged |
| The M3 and M4 audits | accepted | status lines; audit-history rows; M4 closed |
| The H100's supplier (H-1/H-2) | stays unknown; SK hynix's 2022 statement kept as evidence; the claim schema accepts sub-session reports | D-141, D-142 |
| Trainium2's supplier | no candidate to rule on; stays unknown with the research recorded | D-141 |
| The supplier metrics' presentation (H-3) | not asked: no supplier was named | the three blocks keep "cannot be computed yet" |
| Third-party sources (news, market research, teardowns) | the rules for supplier evidence are revised in their own session before S17, then the research is redone (D-143) | a session, S16.6, opens with a proposed policy decision |

## Files changed

| File | Change |
|---|---|
| `sessions/prompts/S16.5-PROMPT.md`, `PROMPT-REGISTRY.md` | new prompt; one registry row |
| `docs/architecture/milestone-audits/M3-audit.md`, `M4-audit.md` | new; accepted |
| `docs/quality/audit-history.md` | two rows |
| `docs/research/hbm-supplier-research-S16.5.md` | new: the findings |
| `sessions/reports/SESSION-16.5-research/` | the search plan and the search log |
| `data/sources.json` | `src-053` (SK hynix newsroom, 2022-06-08) |
| `data/claims.json` | `claim-sk-hynix-hbm3-for-h100-2022` (`FACT`, party, accepted) |
| `schemas/claims.schema.json` | `recorded_in` accepts D-126's one-digit suffix (D-142) |
| `tests/test_claim_schema.py` | one check, written first |
| `docs/architecture/decisions.md` | D-141, D-142 |
| `sql/results/*.json`, `site/hbm-chain/index.html`, `site/hbm-insight/index.html` | rebuilt: input digests only, since `data/claims.json` and `data/sources.json` are inputs |
| `sessions/reports/SESSION-16.5-breaks/`, `SESSION-16.5-qa/` | the harness with S16.5's breaks and its full run; the fail-first output |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md` | state rows |

`Eu-Digital-Policy`: not touched. No dependency added. `sql/accelerator_dependencies.sql`: not touched.

## Data changed

- **Added:** one source (`src-053`) and one claim (`claim-sk-hynix-hbm3-for-h100-2022`), both canonical
  and approved by the human. Counts: 53 sources, 121 claims.
- **Unchanged:** relationships, refused candidates, entities and identity-basis rows. Both `supplier` fields
  stay `not_researched`.
- **Staging:** empty at the start and at the end.

## Tests run

| Command / check | Result |
|---|---|
| **At start** (`a203265`) | 361 tests OK; Gate 0 OK; three `--check` commands up to date |
| **Fail-first:** the sub-session review check, before the schema change | failed for its named reason ([`failfirst.txt`](./SESSION-16.5-qa/failfirst.txt)) |
| **After the change and the rebuild** | 362 tests OK; Gate 0 OK; the three `--check` commands up to date |
| **S16.5's four breaks** | caught as named, 3 of 3; control passes, 1 of 1 |
| **Merged break harness in full**, on `eade6f5` | **77 of 77 faults caught as named; 10 of 10 controls pass** ([`merged-breaks-full-run.txt`](./SESSION-16.5-breaks/merged-breaks-full-run.txt)) |
| **Browser QA** | not run: both pages are byte-identical to the committed ones apart from their sha256 digests (checked by comparing them with the hashes masked), so nothing a reader sees changed |
| **CI** | green on S16.5's commits pushed before this report (observed through `ca42d07`); later runs not observed at writing |

**The S16.5 breaks** ([`breaks.py`](./SESSION-16.5-breaks/breaks.py)):

| Break | Fault | Caught by |
|---|---|---|
| S16.5-A1 | SK hynix named as the H100's supplier on the stale 2022 claim | F-1 on edges: "supplier = company-sk-hynix: no accepted evidence within 12 months". Stale evidence cannot become a supplier value |
| S16.5-A2 | the claim's review recorded in a malformed report name | VD-2 (the schema) |
| S16.5-A3 | the schema's sub-session suffix removed | the new schema check and VD-2 |
| S16.5-C1 | control: the claim's statement reworded, everything rebuilt | passes |

## Evidence added/retired

- **Added:** `src-053` and its claim.
- **Retrieved and logged, not registered:** the other 50 retrieval attempts (S-01 to S-51, refusals included),
  with hashes and outcomes in the search log; their bytes are outside the repository.
- **Retired:** none.

## Decisions made

| Decision | Subject | Status |
|---|---|---|
| D-141 | both HBM suppliers stay unknown; SK hynix's 2022 statement kept as evidence | accepted (2026-10-07) |
| D-142 | a claim's review may be recorded in a sub-session report | accepted (2026-10-07) |
| D-143 | the supplier-evidence rules are revised in a session (S16.6) before S17, then the research is redone | accepted (2026-10-07) |

**Rejected alternatives:**

- the research recorded only in documents;
- SK hynix drawn as a recorded "evidence not fresh" gap, which would change the H100's coverage counts;
- SK hynix named on stale evidence;
- recording S16.5's review in S16's report.

## Deviations

1. **Part A was confirmed by an instruction, not a reply.** The human asked for S16.5 to start once the
   prompt was generated, and the prompt records that instruction as the confirmation.
2. **Sources were not registered in `data/` before approval.** The Extractor's contract allows registering
   new sources directly in `data/sources.json` (`contracts.md`), but this prompt forbids any edit to
   `data/` before approval, and `data/staging/` has no sources file. The stricter rule was followed: the
   drafts stayed in the research folder until the human ruled.
3. **The schema changed** (`claims.schema.json`, one pattern). It is not in Part B §12's "May modify" list.
   It was needed for the approved claim and was approved with it (D-142).
4. **ER-3's search was not completed**, because of access gaps:
   - SK hynix's and Micron's filings;
   - Samsung's global newsroom;
   - NVIDIA's 2026 Forms 10-Q and some found candidates were not read.

   Recorded, not bypassed (RA-2).
5. **The milestone audits rate only what each milestone newly evidenced**, citing accepted ratings for
   the rest (Part B §07, task 2).

**Invalidated assumptions:**

- "A named supplier is likely, so S16.5 will need H-3": nothing fresh and product-level was found.
- "Source records land in `data/staging/`" (Part B §07, task 7): no staging file exists for sources.

## Debt introduced/resolved

**Resolved:**

- the missing M3 and M4 audits (D-140);
- the supplier research, owned by S16.5 under D-139, is done for this pass;
- S16's debt row, a supplier metric's presentation once a supplier is named: not triggered, and returns to
  "the session that adds the first supplier evidence".

**Introduced:**

| Item | Owner |
|---|---|
| `not_researched`'s definition ("No source has been checked") disagrees with ER-3's use after a partial search | S22, or the Knowledge Architect when the vocabulary next changes |
| ER-3's search incomplete: SK hynix's and Micron's filings (access gaps), NVIDIA's 2026 Forms 10-Q, and the candidates not read (log §2.2) | the next supplier research. A manual retrieval by the human (RA-4) could close the filing gaps |
| A fresh product-level statement would make the H100's supplier canonical | Change Detector (inactive); the next supplier research |
| The Extractor's contract (sources straight to `data/sources.json`) and a "no `data/` edit before approval" prompt rule conflict | the next prompt that stages research: say which governs |

## Unresolved issues

**The human's question after the findings:** do sources other than the companies themselves exist? They do.
A quick search, used only to locate candidates, found three kinds:

- **market research:** TrendForce's 2024-03-13 release says the H100's HBM3 supply is "primarily met by SK
  hynix";
- **news:** DIGITIMES, 2023-12-07, headlined that Samsung and SK hynix both supply HBM3 for Trainium2;
- **teardown labs:** TechInsights and Yole name the HBM maker found inside GH200 and B200 boards; no H100 or
  Trainium2 teardown was found in that search.

None of these was retrieved or verified. Under the current rules, all are "never sufficient alone" for a
supplier, and all are older than 12 months.

**Decided by the human (2026-10-07, D-143):** the rules for supplier evidence are revised in their own session
(S16.6) before S17, and the research is then redone under them. The proposal S16.6 opens with:

- historical supplier values with a date and a validity period, outside the 12-month rule when marked as
  past;
- an independent teardown as first-hand evidence of which maker's part a product contains.

It is a policy decision, put to the human in the `CLAUDE.md` §9A format.

Merging PR #28 (S16 and S16.5) into `main` is not asked here.

## Process lessons

- **Write the rule's outcome before searching.** The plan stated what counts and what never counts. Every
  candidate in the log was then sorted by rule, not by plausibility.
- **A stale party statement is still evidence.** It cannot be a supplier value, but kept as a claim it
  records what was said and when.
- **Access gaps decide the state word.** ER-3 and SP-7, not the absence of an answer, keep the field
  `not_researched`.

## Implications for the next session

**For S16.6 (D-143), then S17 (the policy entities, M5):**

- **Completed work:**
  - M4 closed, with its audit;
  - both HBM suppliers unknown, with the research recorded, and SK hynix's 2022 statement held as
    evidence.
- **For S17:**
  - no supplier of either accelerator's memory is named, so a policy record cannot attach to "the H100's
    memory supplier";
  - company-level supply relations exist only as refused candidates (`cand-002`: NVIDIA buys memory from
    SK hynix, Micron and Samsung). A policy layer that needs company-level supply links would need them
    recorded under the `supplies` row of the matrix first;
  - the M4 audit's metric rules and presentation risks apply to any policy-layer derivation.
- **Open issues:** the debt above; S16's debt rows.
- **Recommended next decision:** at S17's opening, whether its policy entities attach to companies (the
  records that exist) or wait for product-level supply links. Asked per `CLAUDE.md` §9A.
- **Files for S17 to read first:**
  - this report;
  - `docs/research/hbm-supplier-research-S16.5.md`;
  - `docs/architecture/milestone-audits/M4-audit.md`;
  - `MASTER-ARCHITECTURE.md` §7 and §8;
  - the S17 entry of `SESSION-ROADMAP.md`.

**Next recommended milestone:** S16.6, the revision of the supplier-evidence rules and the research redone
under them (D-143), then S17.
