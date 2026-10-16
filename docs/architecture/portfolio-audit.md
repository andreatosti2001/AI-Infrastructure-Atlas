# Portfolio and capability audit (S24)

- **Status:** proposed (S24, 2026-10-16). Findings, dispositions and ratings await the human's ruling, item by item.
- **Author:** the Portfolio Reviewer, in its first activation (D-223). PEF §12's eight outputs: process findings and
  outcome findings (Part 5), the evidence for each (Parts 3 to 5), maturity per dimension (Part 6), regressions
  (Part 7), high-value and rejected improvements (Part 8), new learning outcomes (Part 9).
- **Base:** public `claude/new-session-fzwktz` @ `5fd5891` (main `a4763d6`, S23's D-222 commit `bb908e6`, and S24's
  activation of this role); private archive @ `7cdf624`. The as-of date of the pages is 2026-10-15.
- **Evidence:** [`../quality/audit-evidence/portfolio-audit/`](../quality/audit-evidence/portfolio-audit/):
  `measure.py` and its output `measures.json` (run twice, identical; the commits and the SHA-256 of every file read
  are in its `base`), `pull-requests.json` (the repository's merged pull requests), and `cold-reading/` (the form,
  the readers' input and both answers as given).
- **Claim discipline:** counts are labelled **measured** and come from the scripts. Every reading of them is the
  Portfolio Reviewer's `INTERPRETATION`, written beside its evidence. A capability is credited only for what a
  reviewer can open and recount, never for a document's description of itself (PEF §10).

## Contents

1. The question, what counts as evidence, and the reading test
2. What two first-time readers took away
3. The eight capabilities
4. The development history (PEF §4 retrospective)
5. Findings
6. Maturity per dimension
7. Regressions since the previous audits
8. High-value improvements, and improvements rejected
9. New learning outcomes
10. The known-limitations document, audited
11. Rulings

## 1. The question, what counts as evidence, and the reading test

**The roadmap's question (S24):** does the project communicate professional capability through both its result and
its development history?

**What counts as evidence of a capability.** An artifact a reviewer can open and recount:

- a check shown failing on a planted fault;
- a query with its tutorial and its committed result;
- a decision with its context and rejected alternatives;
- a claim re-read against its source;
- a count produced by a script.

A document saying that the project has a capability is not evidence of it.

**Blocking, debt or limitation** (S24 prompt §06.6):

- **blocking:** a capability the documentation claims and no artifact supports. It would be an overstatement in the
  release.
- **debt:** a capability with thin or hidden evidence. It has an owner.
- **limitation:** something v1 never aimed at. It is not a finding.

**The reading test (H-0).** Two fresh AI readers answered a 13-question form (`cold-reading/form.md`) before this
audit's assessment was written. They had never seen the project. Each was given only four artifacts:

- the README;
- the client brief's visible text and its first screen at 1280 and 375 px;
- the brief's "How this was computed" tutorial;
- one decision with its rejected alternatives (D-118).

The second reader was told to read as a hiring manager for a technology-policy research and data role. Their answers
are copied as given.

**Limits of the test:**

- The readers were language models, not people.
- They saw four artifacts, not the repository, so they could not run anything. Where they wrote "claimed", the
  reason is often that the front door gives no way to check, not that no artifact exists. Part 3 separates the two.
- The test measures what a first-time reader takes away from the front door. It does not measure whether the
  Atlas's content is right; S13 and S23 audited that.

## 2. What two first-time readers took away

From `cold-reading/answers-fresh-reader-1.md` and `-2.md`, question by question; quoted words are theirs.

| Question | Both readers | Where they differ |
|---|---|---|
| What the project is (Q1) | a narrow research database on AI hardware dependencies with every link tied to a quoted source; both recovered the question and the two accelerators | reader 2: the README "turns into an internal changelog" after its opening |
| What the README claims that they would check (Q2) | none of its capability claims (tests, breaks, byte-identical rebuilds, human review) can be checked from the README; no live page, no CI badge, no sample output | — |
| The brief's answer (Q3) | correct, in two or three sentences, including the one act naming HBM; both called the answer thin and dated | reader 2: the supplier answer "amounts to two analyst reports, one of them sub-par" |
| The brief's limits (Q4) | found every scope limit; reader 2: "stated more thoroughly than in most professional briefs" | — |
| Trust for a decision (Q5) | a well-sourced fact sheet, not a basis for a decision; trust raised by quotes, locators and refusals; lowered by thin coverage, internal codes in client text ("F-1 fails", "D-092", "ER-9") and a summary of record groupings | reader 1: the matrix's "Data-centre GPU · refused: term not matched" could be misread as "not controlled"; reader 2: the first screen leads with disclaimers, not a finding |
| One statement traced (Q6) | both traced SK hynix → H100 to its quote, locator, dates and review; both noticed the source's "primarily" is dropped in the summary line | — |
| The query (Q7, Q8) | understood the recursive query; could not reproduce it without the loader, the data and the result rows, which the tutorial does not show | — |
| What the query does not prove (Q9) | the tutorial says "dates, not ages" and "one publisher is one voice"; it does not say that a missing row is not a missing dependency, or that "stated" may mean stated by the vendor itself | — |
| The decision (Q10, Q11) | understood the decision; only one rejected alternative has its reason in the record ("H-2 B", "H-2 C" point elsewhere); a heavily governed, fast process | reader 2: "which judgements were the candidate's own and which were an agent's" |
| The eight capabilities (Q12) | data engineering and SQL **shown**; Python, reproducibility, agents **claimed**; client value shown but modest; documentation shown but dense with codes | policy analysis: reader 1 "shown as policy description, not analysis"; reader 2 "not visible" |
| What would change their view (Q13) | seeing it run: a live page, a CI log, a fresh clone passing its checks | reader 2: "a one-page note separating what the candidate decided from what AI agents produced" |

**Reading** (`INTERPRETATION`): the readers found the evidence discipline at once. They could not reach the
strongest engineering evidence, which sits behind the front door. They asked two questions the repository answers
nowhere in one place: who did what, and what the analysis concludes.

## 3. The eight capabilities

For each point: what a reviewer can recount (measured, `measures.json` section in brackets); what the readers took
away; what is missing. Then the verdict.

### 3.1 Domain expertise

- **Recountable:**
  - 197 claims, each quoting its source at a locator: 105 FACT, 52 ATTRIBUTION, 22 DERIVATION, 17 INTERPRETATION,
    1 IMPLICATION [capabilities.1];
  - 65 sources in 11 classes, including 8 official legal texts and 12 company filings;
  - 21 refused candidates, each with its reason, for example HBM named only in a "red flag" rather than as a
    controlled item, or "TSMC 4N" naming a process, not a fabricator;
  - S23's re-read found 178 of 178 readable anchors at their locators ([release content audit](../research/release-content-audit.md)).
- **Readers:** "shown, narrowly". Both cited the refusals as close reading of the texts.
- **Missing:** breadth (S23: 15 of 45 domain-map concepts recorded); current-generation products; the definitional
  research, which is on no page (44 of 197 claims on no page, measured [retrospective.8]).
- **Verdict:** **shown**, as depth of method on a narrow slice.

### 3.2 Data engineering

- **Recountable** [capabilities.2]:
  - 7 schemas, 13 record kinds;
  - 489 tests in 34 modules;
  - 212 deliberate breaks (188 faults, 24 controls), of which 28 run in the suite on every commit. S23's full run caught
    188 of 188;
  - 5 builds with `--check`, every page rebuilt byte for byte;
  - explicit states for unknowns.
- **History:** every one of 19 commits that changed a schema names or appends a decision [retrospective.5]. No
  canonical claim or source was ever removed, and no statement was changed under the same ID (197 of 197 claim IDs and
  65 of 65 source IDs ever canonical are still canonical) [retrospective.6].
- **Readers:** "shown in design, claimed in operation".
- **Missing:** nothing the repository claims. The evidence is reachable only by cloning and running it (P-3).
- **Verdict:** **shown in the repository; not visible at the front door.**

### 3.3 SQL and Python

- **Recountable** [capabilities.3]:
  - 4 queries, each with a tutorial header;
  - 6 "How this was computed" tutorials on 3 pages;
  - results committed with input digests and recomputed independently (WH-10 to WH-14);
  - 13 tools in 5,577 lines, standard library except the pinned DuckDB in one.
- **Readers:** SQL **shown** (the recursive query readable); Python "claimed" (only command names in the four
  artifacts).
- **Missing:**
  - the brief's own query (`accelerator_dependencies.sql`) states its question but not its population or what it does
    not prove. 3 of 4 query headers state question, population, denominator and "does not prove" (P-7);
  - the tutorial shows no result rows (P-7).
- **Verdict:** **shown**, with one query below the Analyst's own contract.

### 3.4 AI governance and agents

- **Recountable** [capabilities.4]:
  - 12 roles, 11 active, each with a contract holding MA §12's nine fields, checked in CI;
  - every tracked file has an owner (233 files);
  - 197 of 197 canonical claims reviewed by the human, through 10 review entries;
  - 137 of 223 decisions name the human in their status;
  - an agent audit (S19) and the autonomy classes applied: drafts in staging, verdicts the human's.
- **History:** 9 of 233 files are owned by two contracts [retrospective.4]. 7 are files a contract excludes in prose
  ("except the templates…"), which the owner check cannot read. 2 are designed field-level splits (Extractor and
  Verifier on staging claims).
- **Readers:** "claimed": nothing in the four artifacts shows how the roles act. Reader 2 asked who decided what.
- **Missing:**
  - an account of the division of labour. `roles.md` says that "an agent is a role, not a program", played by Claude
    in a session or by the human;
  - the README never says that the records, code and documents were drafted by an AI model under the human's
    governance (P-1).
- **Verdict:** **shown as the governance of AI-assisted work.** It is not shown as autonomous agents, and v1 has none
  by design (NG-08). The authorship is unstated at the front door (P-1).

### 3.5 Policy analysis

- **Recountable** [capabilities.5]:
  - 7 US export-control acts with 20 dated events (4 announced, 9 effective, 1 opened, 6 published);
  - 4 `restricts` links, each quoting the act's own words;
  - status derived from events on the as-of date;
  - a dated, logged search for later rules (3 logs) and the Change Detector's comparisons;
  - 9 refused policy candidates;
  - BIS's May 2025 announcement recorded without changing the rule's status (D-220).
- **Readers:** reader 1 "shown as policy description, not analysis"; reader 2 "not visible". Both expected a "so
  what".
- **Missing:**
  - an analytical judgement: 18 of 197 claims are INTERPRETATION or IMPLICATION, and the brief replaces "monitoring
    considerations" with "What this brief does not track" by decision (D-203: monitoring would be advice by another
    name);
  - the Atlas states what texts say and when, not what follows from them (P-6).
- **Verdict:** **thin.** Shown as evidence-grounded policy description and change tracking, not as policy analysis.

### 3.6 Reproducibility

- **Recountable** [capabilities.6]:
  - 18 of 18 pages carry their input digest;
  - 5 `--check` builds;
  - 7 of 7 requirements pinned exactly;
  - 5 of 5 CI actions pinned by commit;
  - `tools/check_all.py`;
  - CI rebuilding every page on another machine on every push.
- **History:** 31 prompts and 30 reports in the archive (every session but the one in progress); 223 decisions, 221 with
  rejected alternatives.
- **Readers:** "claimed": nothing they were given could be run.
- **Missing:**
  - a reproduction by someone outside the project;
  - a way from the README to a CI run;
  - public access to the session records (P-13).
- **Verdict:** **shown in the repository and in CI; not visible at the front door.**

### 3.7 Client value

- **Recountable** [capabilities.7]:
  - one client brief, with 13 sections covering 8 of `CLAUDE.md` §13's 9 parts (monitoring renamed, D-203);
  - every sentence recomputed by BR checks;
  - prints 32 A4 pages;
  - 18 of 18 pages are headed by a question.
- **Readers:**
  - "a well-sourced fact sheet", not a basis for a decision;
  - the first screen shows title, boundary and framing, with no finding;
  - the executive summary groups records ("8 of 8 rows of the dependency result shown");
  - internal codes appear in client text (the brief carries 116 internal codes, 3.1 per 1,000 words; ER-9 ×10,
    D-092 ×6, F-1 ×4) [capabilities.8];
  - the summary drops the source's "primarily".
- **Missing:**
  - any reader outside the project: none is recorded (M3-P3, M6);
  - publication.
- **Verdict:** **the weakest point.** Shown, honest and traceable, but thin, dated and written for the project's own
  vocabulary (P-3, P-4, P-5).

### 3.8 Documentation quality

- **Recountable** [capabilities.8]:
  - 68 Markdown files;
  - 223 decisions, 221 with rejected alternatives and 177 with an explicit context;
  - 10 audit rows in `audit-history.md`;
  - every relative link in the documentation resolves (Gate 0).
- **Readers:** precise and cross-referenced; dense with codes; the README "reads more like a changelog".
- **Measured** [capabilities.8]:
  - the README carries 65 internal codes in 2,522 words, 25.8 per 1,000; the most frequent are session numbers;
  - its "deliberate breaks (208)" is stale: 212 since S23 (P-12).
- **Verdict:** **shown for a builder; costly for a newcomer.**

### Overstatement check (blocking)

Every capability the README and `docs/README.md` claim was matched to an artifact:

| Claim | Artifact |
|---|---|
| "Every value on its pages can be traced to a sentence in a registered source" | PG-1, JR-1, BR-1 (every text node has a home); `tools/trace.py` |
| "The human reviews every real claim" | 197 of 197; `tests/test_human_reviews.py` |
| byte-identical rebuilds | PG-7 and the five `--check` |
| "each query is also its own tutorial" | 4 headers, 6 tutorials (one header incomplete, P-7) |
| CI runs the browser checks | `.github/workflows/ci.yml`; green on S23's commits (runs 253, 254, 257) |
| "178 of 178 readable passages found" | S23's re-read evidence |
| "28 planted data faults" | `tests/test_planted_faults.py` |

**No blocking finding:** no capability is claimed without an artifact. One count is stale (P-12).

## 4. The development history (PEF §4 retrospective)

Counted over the public history to `5fd5891` and the archive at `7cdf624` [retrospective; archive].

**The pace** (measured):

- 168 non-merge commits on 12 calendar days, 2026-09-29 to 2026-10-16;
- 30 session reports;
- 41 pull requests merged by the human.

**Lines added:**

| Author | Code | Documents | Data | Generated pages and results |
|---|---|---|---|---|
| Claude | 44,176 | 40,312 | 16,949 | 8,949 |
| The human | — | 3,529 (the constitutional documents, uploaded at the start) | — | — |

| PEF §4 item | Measured | Reading |
|---|---|---|
| Repeated rework | 6 decisions superseded; 24 of 223 amend or supersede another; the most-changed authored files are state documents (`decisions.md` 75 commits, `docs/README.md` 50, `baseline.md` 47, `README.md` 40), not code (`tools/build_page.py` 8); 3 commits only rebuild pages for their input digest | little rework in code or data; the churn is in state rows that every session rewrites, which is how the README became a changelog (P-4) |
| Duplicated abstractions | 4 page builds and 4 templates; 8 function names defined in two or more tools (`build`, `input_paths`, `load`, `main`, …) | the known F-8 and F-9 (one large base class, two composition styles), owned by v1.5 (D-213); not new |
| Architecture drift | 11 commits changed a constitutional document: the human's upload, 7 by Claude naming or appending a decision, **3 by Claude with none** (`269a1fa` visual intelligence; `d8a5be5`, `aeec137` the §9A rules), each merged by the human from its own pull request | the rules changed on the human's instruction, but three such changes have no decision record (P-10) |
| Agent overlap | 9 of 233 tracked files owned by two contracts: 7 prose carve-outs the owner check cannot read, 2 designed field splits | no real overlap found; the check proves an owner exists, not that it is the only one (P-11) |
| Undocumented schema changes | 19 commits changed `schemas/`; 0 without a decision named or appended | none |
| Content churn from weak sources | 0 of 197 claim IDs and 0 of 65 source IDs ever canonical were removed; 0 statements changed under an ID | none in the canonical records; drafts that the human rejected or narrowed stay in staging history and the review record, not measured here |
| Tests added only after regressions | 1 commit names a fix and changes tests (`e491166`); 1 of 30 reports records a red CI (S20); 27 of 30 reports record checks shown failing first (S00 to S02 had no checks to write) | checks first is the norm, recorded session by session |
| Features without a user journey | 4 of 4 queries shown on a page; 0 tools that no check, build or CI runs; 18 of 18 pages headed by a question; 44 of 197 claims on no page | the concept layer is the one body of work without a journey (S23 C-7, v1.5) |
| Code generated faster than reviewed | 41 merged pull requests with **0 reviews and 0 comments**; median 29 seconds from opening to merge (25 under a minute, 4 over 30 minutes) (`pull-requests.json`); about 110,000 lines added by Claude on 12 days; the human's review is recorded for claims (197 of 197) and decisions (137 of 223 name the human), not for code | the code is reviewed by its checks (fail-first, 212 breaks) and by Claude-written audits, not by a person (P-2) |

**The archive's own record** (counts only, D-152):

- 180 numbered deviations across 30 reports;
- invalidated assumptions recorded in 18 of 30 reports;
- **29 of 30 reports have SPEC §5's eleven minimum fields; S20.5's has none**, and nothing has checked the archive
  since reports moved there (P-8);
- every prompt has its report except S24's, which is in progress. S22.5's report, which S23 recorded as missing,
  reached the archive minutes after S23 opened (P-9).

**Reading** (`INTERPRETATION`): the history is that of a disciplined, very fast, AI-drafted build under human
governance:

- decisions, schema changes and claims are controlled and recorded;
- rework is rare;
- checks precede code.

Its two weaknesses are human review of code, which is absent, and controls that live outside CI and have decayed
(the archive's minimum fields, merges that race session handoffs).

## 5. Findings

The ratings are `INTERPRETATION`. The proposed dispositions are the Portfolio Reviewer's; the rulings are the
human's (Part 11). "Remediable in S24" means wording, documentation or framing that S24's prompt allows once
approved (§12).

| ID | Axis | Finding | Evidence | Rating | Proposed disposition |
|---|---|---|---|---|---|
| **P-1** | outcome | **The front door does not say how the Atlas was built or who decided what.** The README presents roles (Verifier, Change Detector) and "the human" but never says that an AI model drafted the records, code and documents under the human's governance | 169 of 212 commits by Claude; 3,529 of about 114,000 added lines by the human; the human's 197 claim verdicts, 41 merges, decisions; reader 2's Q11 and Q13 | debt, the most important for the portfolio's honesty | remediable in S24: a short "How this was built" section in `README.md` (documentation only): who drafted, who decided, what the checks do, where the human's verdicts are recorded (`human-reviews.md`, decisions) |
| **P-2** | process | **No person reviews the code.** Code is controlled by checks first, planted faults and audits that Claude writes | 0 reviews and 0 comments on 41 pull requests; median 29 s open to merge; 44,176 code lines by Claude | debt (process) | recorded as a stated limitation of the process in S25's case study; a human code-review sample (for example one tool and its tests per session) is a rule change for the human to decide at S25 or v1.5's opening; nothing in S24 |
| **P-3** | outcome | **No one outside the project has used the Atlas, and it has no public address.** The strongest evidence (CI, checks, rebuilds) is reachable only by cloning | NG-13's condition (the S11 slice passing its gates) has held since S12; M3-P3, M6; both readers' Q13 | debt | S25 decides publication (an external action, the human's); KL-15 |
| **P-4** | outcome | **The front-door documents speak the project's internal code and read as a changelog** | README: 25.8 internal codes per 1,000 words (65); the brief: 3.1 (116); readers 1 and 2 (Q1, Q2, Q5) | debt | remediable in S24 for the README: a plain-language opening paragraph before the session history (documentation only); the brief's codes come from record text and template labels, v1.5's design session |
| **P-5** | outcome | **The brief's summary can be read as naming the only memory supplier**, and it leads with disclaimers, not a finding | the summary drops the source's "primarily"; "not the only supplier" is framing on the research view only; reader 1 and reader 2 (Q6), reader 2 (Q5, first screen) | debt | remediable in S24, (a) only: add to the brief's summary framing the research view's limit, that a reported supplier is not the only supplier (an approved limitation statement; template framing; brief rebuilt); (b) the first screen and the summary's composition, v1.5 (non-goal §08) |
| **P-6** | outcome | **Policy analysis is shown as description and tracking, not analysis** | 18 of 197 claims INTERPRETATION or IMPLICATION; D-203 (monitoring renamed); both readers (Q12) | debt (thin evidence for a roadmap capability) | S25's case study names the capability as "evidence-grounded policy description and change tracking"; an analysis layer of labelled interpretations is a decision for v2; nothing in S24 |
| **P-7** | outcome | **The brief's own query states neither its population nor what it does not prove**, below the Analyst's contract ("each query states what it does not prove"); its tutorial shows no result rows | `sql/accelerator_dependencies.sql` header: "question", "reading" only; 3 of 4 queries complete; readers (Q8, Q9) | debt | remediable in S24 if approved: the Analyst adds "population" and "does not prove" lines to the header (the tutorial is generated from it), checks first (a WH check that every header carries the four), results and pages rebuilt; the result rows in the tutorial, v1.5 |
| **P-8** | process | **The archive's report rule is no longer enforced.** Since D-152 moved reports out of the public repository, nothing checks SPEC §5's minimum fields; the archive's `sessions/README.md` still says Gate 0 does | S20.5's report has none of the eleven fields (1 of 30) | debt (a control that decayed) | remediable in S24 in the archive: correct its README; whether to add a checker to the archive (it has no CI) is the human's |
| **P-9** | process | **Session handoffs race the human's merge** | S22.5's report reached the archive after S23 opened; S23's D-222 commit was pushed 56 minutes after PR #41 merged and was missing from `main` at S24's opening (S24 merged it) | debt (process, low) | a process lesson recorded in S24's report; a one-line rule (the final message names the commit the merge must contain) is a SPEC change for the human; nothing in S24 |
| **P-10** | process | **Three constitutional changes have no decision record** | `269a1fa`, `d8a5be5`, `aeec137` (Part 4) | debt (low) | remediable in S24: one decision appended that records the three changes, their dates and their pull requests (documentation only) |
| **P-11** | outcome | **The owner check proves that each file has an owner, not one owner** | 9 of 233 files owned twice; 7 prose carve-outs | debt (low) | v2's agent activation (D-201, item 5); nothing in S24 |
| **P-12** | outcome | **The README's break count is stale** | "deliberate breaks (208)"; 212 since S23 | debt (low) | remediable in S24: correct the count (wording) |
| **P-13** | outcome | **The richest evidence of the development history is private.** Prompts and reports are in the private archive (D-152); a public reader can recount the history from commits, decisions and audits only | 31 prompts, 30 reports, 180 deviations in the archive; this audit's counts are the first public summary of them | debt (by decision) | S25's case study describes the process with these counts; publishing any report is the human's (D-152); nothing in S24 beyond this audit |
| **P-14** | outcome | **One known limitation a reader meets is stated on no page:** the pages quote a later rule that cites BIS's May 2026 guidance, and never say that the Atlas has not read that guidance | `known-limitations.md` KL-08 (Part 10) | debt | remediable in S24: one framing sentence in the "later statements" framing (journey and brief templates), naming no record: the Atlas holds texts a later statement cites only as the statement quotes them, without reading them (an approved limitation statement; pages rebuilt) |

## 6. Maturity per dimension

PEF §3's 0 to 4 scale, process and outcome kept apart (PEF §1). The previous rating and its source are beside each.

| Dimension | Process (previous) | Outcome (previous) | Evidence |
|---|---|---|---|
| Data architecture | **3** (3, M2) | **3** (3, M5) | 19 of 19 schema commits with a decision; 0 canonical records removed or reworded; one home per fact, explicit states and derived statuses all checked. Not 4: untested at the scale v2 plans |
| Content and review | **3** (3, S23) | **2** (2, S23) | unchanged since S23 (accurate, checkable, narrow, single-voiced); this audit read no claim afresh |
| Agent architecture | **3** (3, M5) | **3** (2, M2; S19 gave none) | 11 contracts with MA's fields checked in CI; every file owned (D-180); no silent promotion (197 of 197 human verdicts); the reviewer role now active. Not 4: every role is one model in one session, with independence from the human's review (D-182), and exclusivity is unchecked (P-11) |
| Analytical depth | **3** (3, M4) | **3** (3, M4) | metrics defined by question, population and denominator, recomputed independently; one query below its contract (P-7). The policy layer's lack of judgement is P-6, a product question, not a metric's |
| Code and engineering | **3** (3, S22) | **3** (2 at S22, 3 with F-1 remediated, D-213; **left open by D-216**) | F-1, F-2, F-4, F-5, F-7, F-11, F-12, F-14 remediated with checks first; 489 tests; 212 breaks, 188 of 188 caught; checks that can fail, in CI on three engines. Open: F-6, F-8, F-9, F-10, A-4 (v1.5, maintainability and visual). Process held at 3, not lowered, because the controls are automated and proven; but no person reviews the code (P-2) |
| Product and user value | **3** (3, M6) | **2** (2, M6) | 18 pages each from a recorded question; but no outside reader, no public address, and two first-time readers found the brief thin, dated and coded (P-3 to P-5) |
| Reproducibility | **3** (3, M2) | **3** (3, M6) | every page rebuilt byte for byte from digested inputs, here and in CI; exact pins; 221 of 223 decisions with rejected alternatives. Not 4: no reproduction by another person; the session records are private (P-13) |

**The code and engineering outcome rating D-216 left open: 3, Controlled.**

**Learning progression of the owner** (PEF Axis A, item 7): the repository records the human's decisions and verdicts,
not what the human learned. It is **not rated**: unknown, not inferred.

## 7. Regressions since the previous audits

Measured against S22 and S23:

- **No check was loosened.** The tests went from 487 at S23's start to 489 at its end, and S24 adds its own; the
  breaks went from 208 to 212.
- **A control decayed:** the archive's minimum fields (P-8), unchecked since D-152. S20.5's report, written on
  2026-10-14, is the one that lacks them.
- **A count went stale:** the README's 208 breaks (P-12).
- **A decision was missing from `main`:** D-222 (P-9). S24 merged it at its opening.

## 8. High-value improvements, and improvements rejected

**High value**, in order of what they would change for a reader of the portfolio:

1. **P-1:** say how the Atlas was built and who decided what.
2. **P-3:** decide publication at S25, with a link from the README to the CI runs.
3. **P-14:** say on the pages that the guidance a later rule cites is unread.
4. **P-5a:** the brief says that a reported supplier is not the only supplier.
5. **P-7:** the brief's query states its population and what it does not prove.
6. **P-4:** a plain-language opening for the README.
7. **P-13 and P-6:** S25's case study states the process with its counts, and names the policy capability for what
   it is.

**Rejected:**

| Improvement | Why not |
|---|---|
| a capability score or a single portfolio grade | PEF §1 keeps dimensions apart; a score would be the dashboard theatre PEF §8 forbids |
| an agent runtime, to make "agents" visible | NG-08 holds for v1.0 (D-184); it would be infrastructure for appearance (MA §24) |
| redesigning the brief's first screen and summary now | v1.5's work (non-goal §08); the evidence is weighed, not fixed |
| removing the internal codes from refusal reasons | they are record text, canonical; a change is a data change for the human, and the codes link to their rules |
| new research to widen coverage or refresh the H100's supplier before v1.0 | non-goal §08; D-218 sends it after v1.0 |
| publishing the session reports wholesale | D-152; the counts here carry the evidence without the private text |
| adding pages to show more capability | feature count is not capability (PEF §12) |

## 9. New learning outcomes

- **A first-time reading finds what the project's own audits cannot.** Ten audits checked the evidence. Two readers
  with four artifacts found in minutes that the evidence is hard to reach and that authorship is unstated.
- **Evidence that exists is not evidence that is communicated.** The data engineering and reproducibility are strong
  and recountable. At the front door they read as "claimed".
- **The pages state boundaries; the research gaps live in labels and audits.** The known-limitations check made this
  measurable: 3 of 15 gaps are stated on no page (Part 10).
- **Controls outside CI decay.** The archive's report fields were enforced while reports lived in the public
  repository, and stopped being enforced when they moved.

## 10. The known-limitations document, audited

[`../known-limitations.md`](../known-limitations.md) (D-222, written by the Portfolio Reviewer) has two kinds of row:

- **15 gaps:** what is missing, why, what would close it, and the owner after v1.0;
- **5 boundaries by design.**

It ties both to the pages in two tables: where each limit is stated, and the remaining framing sentences that explain
rather than limit. `tests/test_known_limitations.py` (KL-1 to KL-8, the Data Auditor's) compares them with the built
pages sentence by sentence. Every one of the 46 distinct sentences in the pages' limits framing is accounted for
(measured: the check passes on the pages as built). It fails on a planted disagreement in either direction; the
breaks are in the harness.

**What it shows** (measured from the document):

- **Every gap D-218 sends to S25 has a row (KL-6).** These are: the EAR's dates, the May 2026 guidance, a current
  H100 supplier, the H100's fabricator, Trainium2's recognised source, aged values, single voice, and coverage.
- **12 of 15 gaps are stated on at least one page.** 7 are stated as framing, 5 as labels drawn from the records.
- **3 gaps are stated on no page:**
  - KL-08, the unread May 2026 guidance: material, because readers meet its citation (P-14);
  - KL-13, the concept layer, which is invisible by definition;
  - KL-14, access gaps, which belong to the Atlas's re-reading, not to a page.
- **Owners:** 7 gaps are owned by "a research session after v1.0 that the roadmap does not yet name" or by v2
  without a named session. D-218's C-8 holds after S24: the roadmap names no session for them, and S25's backlog
  should.

## 11. Rulings

Pending: the human's ruling on each finding P-1 to P-14, the ratings in Part 6, and the known-limitations document
(S24 H-2).
