# Agent architecture audit (S19)

> **Records cited.** The session reports and prompts this audit cites are kept in the private development archive,
> not in this repository (D-151); the decisions, documents, commits and files it cites are here. Audit evidence that
> can be re-run is in [`../quality/audit-evidence/agent-audit/`](../quality/audit-evidence/agent-audit/).

**Status:** PROPOSED (S19, 2026-10-14); the human rules each finding and each role at S19's H-2.
**Required by:** `SESSION-ROADMAP.md` S19 ("Any unnecessary agent or duplicate responsibility must be removed or
justified"); `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §7.
**Base read:** `claude/new-session-vv78en` @ `cc4f44e` (public `main` = `f6e6357` plus S19's harness work).
**Who audits:** Claude, the same model that played every role being audited. Where judgement is involved, this
audit prefers what a script can recount (Git history, checks, counts) to self-assessment, and shows the evidence
beside each conclusion. Each finding is an `INTERPRETATION` of that evidence.

## 1. What the agent system is, in practice

An agent here is **a role, not a program** (`roles.md`): Claude in a session, or the human, works under a written
contract, and deterministic tests in CI check the result. There is no runtime, queue or autonomous write path
(NG-08). Twelve roles are named by `CLAUDE.md` §8; seven are active with contracts (`contracts.md`); five are
inactive.

The question the roadmap asks is whether this still improves reliability rather than adding complexity. The
short answer, from the evidence below: **the contracts and checks do real work where a check enforces them, and
are paper where nothing does.** The staging and human-review path held for every canonical claim, but twice
outside staging; the write boundaries no longer describe who writes what; and the Verifier's independent
authority comes from deterministic re-reading and the human's review, not from being a separate role.

## 2. The evidence, recounted

| What was counted | Result | How |
|---|---|---|
| Commits that wrote canonical data since S06 | 21 (`git log --full-history -- data/<canonical files>`) | each listed in §3 F-1 |
| Of those, a promotion on a recorded human verdict, or an explained change of form | all 21 (F-1); each canonical claim's `review.recorded_in` resolves to its dated entry (HR-1 to HR-3 in CI) | `docs/quality/human-reviews.md`, 8 entries |
| Files changed since S06 that lie in no active role's `ALLOWED_WRITES` | 63 | [`write_boundaries.py`](../quality/audit-evidence/agent-audit/write_boundaries.py), [output](../quality/audit-evidence/agent-audit/write-boundaries-output.txt) |
| Session prompt length (words), S05 to S19 | 2,724 to 6,243; no trend after S07 (S17 3,203; S18 3,098; S19 3,715) | the archived prompts |
| Session report length (words) | peak 19,282 (S07); 2,029 to 4,368 since S12 | the archived reports |
| Human decision points named in each prompt | 3 to 8 since S06; 3 in S16.5 to S19 | the archived prompts (`H-n`) |
| Decisions in the log | 179 (D-001 to D-179), about 28,700 words: the largest governing document | `decisions.md` |
| Canonical records (sources included) at each merge | 0 (S05) → 226 (S12) → 238 (S16.6) → 296 (S17) → 319 (S18) | `git show <merge>:data/*.json` |
| Checks | 411 tests at S18; 413 with S19's permanent tests; 130 breaks | the suite; `tests/regression/` |

## 3. Findings

Each finding is marked **blocking** (the roadmap's gate is not met until it is ruled and acted on) or **debt**
(recorded with an owner). The proposed ruling is the auditor's; the human decides at H-2.

### F-1 — Two sessions wrote canonical records without staging (debt; the review path held)

- **Evidence.** From S07 to S18, every canonical write but three followed the committed path
  staging → human review → promotion: S07 (`95bb326` → `59e966b`, `4a5f7b3`), S08 (`f9cdf66` → `1922da0`), S09
  (`21c2ed4` → `f400376`), S10 (`5b42d20` → `0b2bb0e`), S12 (`1f600de` → `9ce0929`), S17 (`d4aa215` → `af2c9ca`),
  S18 (`c527b8f` → `bd6b409`). The exceptions are S16.5 (`eade6f5`: one source and one claim) and S16.6
  (`f5f7e7e`: two claims and Samsung Electronics's record; `a3143b0`: the two supplier values). Their drafts were
  held in private research folders and written to `data/` only after the human's verdict. S16.5's report gives
  the reason: its prompt forbade any edit to `data/` before approval, and there was no staging file for sources.
- **What it means.** The human reviewed every record (entries of 2026-10-07 in `human-reviews.md`), so no
  unreviewed fact became canonical. But the staged-record checks did not run on those drafts before the human saw
  them: the human reviewed records no check had passed.
- **Other writes outside a contract, each explained:** creating empty files (`f9cdf66`, `21c2ed4`, `5b42d20`,
  `f6d7dd0`); a refused card changed on the human's ruling (`cc0f665`, D-111); the review-path rewrite
  of 114 claims ordered by the human (`e9e036d`, D-151); the identity-basis migration (`bed8bce`, D-117, a
  deterministic migration); the card change approved by the human (`f24cc7b`, D-149).
- **Proposed ruling:** debt. `contracts.md` states that drafts always land in `data/staging/` and that a session
  prompt cannot forbid it; no check is added (history is not checkable in CI). This does not change how claims
  become canonical: it restores the path the contracts already describe.

### F-2 — The write boundaries no longer describe who writes what (blocking)

- **Evidence.** 63 files changed since S06 lie in no active role's `ALLOWED_WRITES`
  ([output](../quality/audit-evidence/agent-audit/write-boundaries-output.txt)). Most are expected outside every
  contract (the constitutional documents, `docs/agents/`, the canonical data files promoted on the human's
  verdict, `human-reviews.md`), but nothing says so except, for `data/claims.json` alone, `contracts.md`'s
  preamble. The rest is work done by a role whose list was never extended:
  - the SQL layer and the metrics: `sql/*.sql`, `sql/results/`, `sql-layer.md`, `metrics.md`,
    `analytical-audit.md` (S14 to S16);
  - the research view `site/hbm-insight/index.html` (S14.5 on; the Data Auditor's list names only the HBM page);
  - the policy design: `policy-dataset.md`, `policy-links.md`, `entity-taxonomy.md`, `relationship-taxonomy.md`
    (S17, S18), and `visual-architecture.md`;
  - `docs/research/source-policy.md` (7 commits, every new evidence row), the research documents and
    `source-register.md`;
  - the audit record: `audit-history.md`, `audit-evidence/`;
  - CI and the pinned engine: `.github/workflows/ci.yml`, `requirements-analysis.txt`.
- **What it means.** `contracts.md` says "a role writes only its allowed paths", but no check reads that
  sentence, and it has been false since S12. A permission boundary that is not checked cannot be audited.
- **Proposed ruling:** blocking, remediated in S19. Each path gets an owner in `contracts.md` (or in a new list of
  files written only on the human's decision), and a check written first fails if any tracked file has no owner.

### F-3 — The Analyst's work was done without an active Analyst (blocking, with F-2)

- **Evidence.** `roles.md` lists the Analyst as inactive, "first active S14 (SQL layer); S15 (metrics)". S14 built
  the warehouse and its queries (D-117 to D-121), S15 the metrics (D-127 to D-132), S16 the analytical audit
  (D-133 to D-138): derived, reproducible analysis, which is MA §11.8's mission. No contract bounded it; the Data
  Auditor's `tools/` covered `tools/warehouse.py` only.
- **Proposed ruling:** activate the Analyst with a contract: writes `sql/*.sql`, `sql/results/` (by
  `tools/warehouse.py` only), `metrics.md`, `sql-layer.md`, `analytical-audit.md`; validation gate
  `tests/test_warehouse.py` and `tests/test_insight.py`; forbidden: `data/`, a result typed by hand, a metric
  without its question and denominator (NG-11).

### F-4 — The Verifier's authority rests on re-reading and on the human, not on being a separate role (debt)

- **Evidence.** In S17 and S18 one session drafted the claims (Extractor) and re-read them (Verifier). What the
  Verifier did that the Extractor did not, and that can be recounted:
  - re-retrieved the five official texts and compared their hashes with the registered ones (S18 twice: every
    hash matched);
  - re-read every anchor on its stated page in those bytes (S17: 45 citations; S18: 28 anchors) with a script;
  - narrowed three statements that said more than their anchors (S17's report, "Narrowed before H-2").
  The script was private and rewritten each time (`SESSION-17-research/verify.py`, `SESSION-18-research/verify.py`,
  25 and 36 lines, the same logic). In CI, VD-11 checks only that a read records the registered hash; it cannot
  check that an anchor is in bytes the repository does not hold.
- **What it means.** The Verifier's mechanical half is real and deterministic, but lives in a private, rewritten
  script. Its judgement half (does the wording exceed the evidence?) is the same model checking its own draft; the
  independent check of that judgement is the human's review of every claim at H-2.
- **Proposed ruling:** keep the Verifier, re-scoped in `roles.md`: its authority is the re-read (bytes, hash,
  anchor at locator) and a written list of wording that exceeds evidence; independence comes from the human's
  review, which stays outside every contract. Debt: a durable re-read tool in `tools/`, taking the extracted text
  pages as input (standard library; PDF extraction stays a retrieval step). Owner: the next session that adds
  claims from a new retrieval.

### F-5 — No runtime orchestrator is justified (debt-free; NG-08 confirmed)

- **Evidence.** Coordination is the session prompt and the human's decisions. Since S07 the prompt has not
  grown (§2), reports have shrunk, and human decision points per session are flat (3 to 8). No session needed
  a dispatcher, queue or autonomous write: every canonical write was a human-reviewed promotion (F-1). Worker
  restarts in S17, S18 and S19 were recovered from pushed commits and archived answers, not from a control
  plane (F-7). A runtime would add a write path that itself needs a contract, a check and an audit.
- **Proposed ruling:** the Orchestrator stays inactive; its duties are the session prompt's and the human's.
  NG-08 holds for v1.0. `roles.md` replaces "S19 decides" with that outcome.

### F-6 — The Change Detector has never been needed yet; its first task now exists (debt)

- **Evidence.** S07 built the 12-month freshness rule F-1 (`test_freshness.py`): a check, the Data Auditor's. No
  session compared two versions of a source or of the data to emit candidate changes. S18's re-retrievals compared
  hashes as part of verification. The first true change-detection task is D-175's gap: later BIS rules that would
  change the entries the Atlas holds.
- **Proposed ruling:** stays inactive; its first session becomes the one that takes D-175's later-rule search. A
  merge into the Source Scout was considered: the search is the Scout's, but deciding that a later text changes an
  entry is a comparison the Scout's contract does not allow (it asserts nothing).

### F-7 — Failure recovery: nothing lost, because of commit discipline (debt-free)

- **Evidence.** S17 (several restarts over five days), S18 (two) and S19 (two before this audit) restarted their
  workers. Each lost nothing: prompts are archived before any change, the human's answers are archived as given
  as soon as they are received (`SESSION-1x-decisions/`), and commits are pushed as they are made. Near misses
  were caught by process, not by a role: a commit made while four tests failed, its exit code hidden by a pipe
  (S17, amended before push); a pop-up that carried unverified context (S17, corrected in the archived answers).
  Background runs do not survive a restart; the long break runs are re-runnable by ID.
- **Proposed ruling:** keep the practice; no role or runtime change.

### F-8 — Milestone audits: the Knowledge Architect writes what PEF §12 gives the Portfolio Reviewer (justified)

- **Evidence.** PEF §12 gives milestone findings to the Portfolio Reviewer, inactive until S24; the Knowledge
  Architect's list holds `milestone-audits/` (S12), and M4's audit says "as the Knowledge Architect, with the
  Portfolio Reviewer's process judgement".
- **Proposed ruling:** justified, stated in `roles.md`: the Knowledge Architect writes the audit document, the
  ratings are the human's to accept, and the human's review stands in for the Portfolio Reviewer until S24
  (baseline §5, Gate 8).

### F-9 — Overlaps that are boundaries, not duplicates (justified)

- **Data Auditor and QA** both name `tests/test_page.py`: the Auditor writes the checks, QA writes only reports of
  the browser run, which CI does not run (D-106).
- **Editorial and Data Auditor** share the page: the framing and style are Editorial's, the labels and journey in
  `tools/build_page.py` are the Auditor's; PG-6 checks the line.
- **Extractor and Verifier** write disjoint fields of the same staged claim (`contracts.md`); F-4 covers what is
  independent.

### F-10 — Private, per-session scripts did the harness's selection (resolved in S19)

- **Evidence.** S17 and S18 each selected breaks with a private script that could not read five setups.
- **Ruling already taken:** D-177 (measured selection, public, no blind spot on S18's files).

## 4. Proposed role rulings

| Role | Status now | Proposed | What changes in `roles.md` / `contracts.md` / the test |
|---|---|---|---|
| Orchestrator | inactive | kept inactive (F-5) | row: "no runtime (NG-08 holds for v1.0); the session prompt and the human coordinate" |
| Source Scout | active | kept | allowed writes add `docs/research/` research documents and `source-register.md` (F-2) |
| Extractor | active | kept | failure behaviour: drafts always land in `data/staging/` (F-1) |
| Verifier | active | kept, re-scoped (F-4) | mission and evidence: the re-read is its authority; independence is the human's review |
| Change Detector | inactive | kept inactive (F-6) | first session: the one that takes D-175's later-rule search |
| Knowledge Architect | active | kept | allowed writes add the design documents of S14.5 to S18, `source-policy.md`, `audit-history.md`, `audit-evidence/`, `agent-audit.md` (F-2, F-8) |
| Data Auditor | active | kept | allowed writes add `site/hbm-insight/index.html` (by its build), CI and requirements (F-2) |
| Analyst | inactive | **activated**, new contract (F-3) | a contract; the test's active set gains the Analyst |
| Editorial | active | kept | none |
| Client Output | inactive | kept inactive (S21) | none |
| QA | active | kept | none |
| Portfolio Reviewer | inactive | kept inactive (S24) (F-8) | row: the Knowledge Architect writes the milestone audit; the human's review stands in |

With these rulings, no role is unnecessary and no responsibility is duplicated without a stated justification.
