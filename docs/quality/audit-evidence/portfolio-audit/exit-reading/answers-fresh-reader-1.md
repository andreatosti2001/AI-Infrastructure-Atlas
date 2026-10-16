# S25 exit-condition reading: fresh reader 1's answers

**Reader:** a fresh agent (not an agent role), told to read as a technology-policy researcher who wants to understand the project well enough to explain it. It was given only the release candidate's tree (public commit `495028e`, the tracked files as the publication serves them: without `.github/` and dotfiles; see `input.md`) and the seven fields of `form.md`, in an isolated folder. It was told to open nothing else, to use no web and no Git, and to run no code. It wrote nothing to either repository. Answered on 2026-10-16, before any assessment. Copied as given, from the line "Read:" on.

Read: README.md (all); docs/README.md (all); docs/case-study.md (all); docs/release/release-notes.md (all); docs/release/demonstration.md (all); docs/architecture/final-architecture.md (all); docs/architecture/claim-model.md (all); docs/architecture/metrics.md (all); docs/known-limitations.md (all); docs/agents/roles.md (all); docs/agents/contracts.md (first ~120 lines: Source Scout to Analyst); docs/quality/human-reviews.md (first ~90 lines: index table and first three entries); sql/evidence_coverage.sql (all); sql/results/evidence_coverage.json (all); sql/source_age.sql (searched for the reference date only); sql/results/source_age.json (~60 lines of rows); data/relationships.json (first ~90 lines); data/claims.json (one claim, ~50 lines, found by search); schemas/sources.schema.json (the source-class vocabulary, ~20 lines); tools/check_all.py (all); tools/warehouse.py (docstring and first ~60 lines); tests/regression/README.md (all); tests/test_agent_contracts.py (test names and docstring lines only, by search); site/briefs/accelerator-memory/index.html (section headings by search, plus ~30 lines covering the header, scope, executive summary and the start of the dependency map; the file is about 1 MB); site/index.html (question-card headings by search). I also listed the folder's files and checked file sizes. I tried to open .github/workflows/ci.yml, but it is not in the folder.

---

## 1. What the system does

**(a)** The AI-Infrastructure-Atlas is a small research database about the physical hardware behind AI, built so that anyone can check it. Its pages are generated from the database. At v1.0 it answers one question end to end: *what does an AI accelerator's memory depend on, who is reported to supply it, and which recorded export-control texts name those parts?* It covers two accelerators, the NVIDIA H100 and AWS Trainium2, and the High Bandwidth Memory (HBM) inside them. It then follows the chain one step further: HBM requires 3D die stacking. It also records seven US export-control acts (the EAR and BIS rules from 2022 to January 2025) and says which of the chain's part classes their texts name. Here is what it shows in substance:
- Both accelerators incorporate HBM.
- The memory suppliers are named only as reported by third parties. SK hynix is named for the H100, and only for the period up to March 2024 (TrendForce). Samsung is named for Trainium2 (SemiAnalysis, a source that does not meet the project's "recognised" criterion).
- Who fabricates the H100 (TSMC) is shown as a gap, because the evidence is too old.
- One HBM-related BIS rule (December 2024) names HBM among the items it controls.

The output is 18 static HTML pages: an entry page with six question cards, an HBM dependency page, a "research view", an export-control comparison page, 9 company profiles, 4 place profiles and a printable "client brief". The stated audiences are researchers, analysts and a client reader. Its stronger, less stated purpose is to work as a portfolio piece: it shows evidence engineering and the governance of AI-drafted research. It was built by Claude in about 30 governed sessions between 29 September and 16 October 2026, under a human owner's rules and verdicts.

**(b)** README.md; docs/release/release-notes.md; docs/case-study.md; site/index.html; site/briefs/accelerator-memory/index.html; data/relationships.json.

**(c)** The "client" is never identified as a real person or organisation type. The case study itself rates client value as "the weakest point". I could not tell who the intended paying or using audience is beyond "a policy researcher or analyst". The README's opening question ("who is known to make it?") is worded slightly differently from the brief's question ("who is reported to supply it ... export-control texts"). The second is the fuller, current version.

## 2. How the data is structured

**(a)** The canonical data lives in `data/` as JSON files, one file per record kind and 13 kinds in all:
- sources;
- claims;
- companies, jurisdictions, technologies, components, products and facilities;
- policies (export-control acts);
- dated events;
- relationships;
- refused candidates (links that were considered and turned down);
- an "identity basis" file for IDs made by rule.

Each kind has a JSON Schema in `schemas/` (7 schema files), with controlled vocabularies.

The records link to each other in one direction only:
- A **source** is a retrieved document, recorded with its URL, publisher, class (e.g. `company_filing`, `official_legal_text`, `market_research_consultancy`), access time and a SHA-256 hash of the bytes.
- A **claim** is one proposition. It cites sources, each at a locator and with a verbatim quoted anchor. If the claim is an inference, it points instead to input claims plus written reasoning.
- **Entities and relationships** point to claims. Relationships are typed edges (`incorporates`, `designs`, `fabricates`, `requires`, `operates`, `restricts`...). A field on an edge, such as `supplier`, can carry its own claims and a validity window (`valid_to: 2024-03`).
- Claims never list the records that cite them. That reverse view is computed by `tools/trace.py`.

The project's rule is "one home per fact". Derived things such as a policy's status on a given date, a facility's status, evidence ages and paths through the chain are computed on demand and never stored.

Unknowns are explicit states, never null or zero:
- `not_researched` means not looked for, or only partly looked for;
- `not_publicly_determinable` must cite a recorded search, stored as a DERIVATION claim with a `search` block;
- `not_applicable` means the field does not apply.

A claim's `as_of` can be `{"state": "not_stated"}`. In SQL, each such field becomes two columns, `<field>_value` and `<field>_state`. Drafts that the human has not yet reviewed sit in `data/staging/`, which the SQL layer and the pages never read. A value that only a third party reports is shown as "reported", never as "stated".

**(b)** README.md ("What it contains", "How evidence works"); docs/architecture/final-architecture.md §2; docs/architecture/claim-model.md §1, §5, §8, §9; data/relationships.json; data/claims.json; schemas/sources.schema.json; tools/warehouse.py (docstring).

**(c)** I did not open the entity or relationship taxonomy documents, or the schemas other than the sources schema, so I cannot list every relation type or entity type with confidence. The vocabulary of relation types above comes from the data I read. I also did not check exactly how `facilities` and `events` combine to give a facility's status.

## 3. How claims are verified

**(a)** There are five steps:
1. **Extract.** A draft claim is created in staging with `evidence_status: unverified` and `review: not_reviewed`. It has a claim type (FACT, ATTRIBUTION, DERIVATION, INTERPRETATION or IMPLICATION), and each citation has a locator and a verbatim anchor.
2. **Verify.** The "Verifier" re-reads each cited source at its locator, in the bytes whose hash was registered. It checks that the anchor is there, reads the whole sentence and judges whether the claim says more than the sentence. It then sets the status: `supported`, `partial` (the wording goes too far, so the claim must be narrowed), `context_only` (the sentence does not state the claim) or `disputed` (a genuine factual contradiction, naming the competing claims). It also records the date and the hash of the bytes it read.
3. **Type rules.** These are machine-enforced:
   - a FACT needs first-hand standing (the party itself, or the originator);
   - a reporter's account can support at most an ATTRIBUTION;
   - an inference is never stronger than its weakest input.
4. **Human review.** A claim becomes canonical, and moves from `data/staging/claims.json` to `data/claims.json`, only on the human owner's recorded verdict. The human answers one question per claim: "does it say this, and no more?". Every canonical claim names the dated entry in `docs/quality/human-reviews.md` that holds its review.
5. **Checks.** A test (VD-8) enforces three things: every canonical claim was accepted by the human, no staging claim carries an acceptance, and canonical claims rest only on canonical claims.

So the human decides. The Verifier's check is "necessary, never sufficient". All 197 canonical claims were accepted, in 10 review batches between 1 and 15 October 2026, and none was rejected.

**(b)** docs/architecture/claim-model.md (§3, §4, §6, §7, §11, §14); docs/quality/human-reviews.md; docs/agents/contracts.md (Extractor, Verifier); README.md "How evidence works"; data/claims.json (one example).

**(c)** I have three doubts:
- **Independence.** The Verifier is Claude, often in the same session that drafted the claims. The project says so itself (D-182): the human's review is then the only independent check.
- **The review record.** It records outcomes in batches, such as "62 claims, all accepted", plus spot-checks of a few anchors. I cannot tell how closely the human read each of the 197 claims. Some batches were large, and a review that never rejects anything is either very good drafting or light review. The record does not let me tell which.
- **Manually supplied sources.** Their anchors cannot be machine-checked (claim-model §5). I did not find out how many claims depend on such sources.

One small puzzle: the TrendForce claim's statement gives a date (13 March 2024), yet its `as_of` is `not_stated`. I did not find out why.

## 4. How metrics are produced

**(a)** `tools/warehouse.py` loads the canonical JSON (never staging) into a fresh in-memory DuckDB database on every run. It then runs the four `.sql` files in `sql/` in dependency order: each query becomes a view that later queries read. It writes each result to `sql/results/<query>.json` together with:
- the SHA-256 of the query;
- the SHA-256 of every input data file and of the warehouse script itself;
- a combined input digest.

Each query file begins with a structured header that doubles as its tutorial: question, population, denominator, assumptions, missing data, how to reproduce, sensitivity, what it does not prove, and how to read it. The pages render this header in a "How this was computed" panel.

There are two live metrics:
- **Evidence coverage per accelerator.** It counts that accelerator's links that are stated, inferred, reported or a gap. Today: Trainium2 has 2 stated, 1 inferred, 1 reported and 0 gaps out of 4. The H100 has 1 stated, 1 inferred, 1 reported and 1 gap out of 4.
- **Source age.** The age of the newest evidence behind each link, against a reference date fixed in the query (2026-10-15), with a 12-month horizon flag.

The three supplier metrics (supplier count, geographic concentration, single-sourcing) are deliberately shown as "cannot be computed yet". No source states a part's full supplier set, so the project will not print a misleading 0 or 1. There are no composite scores, shares or rankings, by design.

You can check a number in three ways:
1. `python tools/warehouse.py --check` recomputes and fails if any committed result differs.
2. The test suite (WH-10 to WH-14) recomputes the metrics independently in plain Python, without SQL.
3. The page builds only copy cells from those results, and page tests check those copies.

By hand, you can open `sql/results/evidence_coverage.json` and recount from `accelerator_dependencies.json`.

**(b)** docs/architecture/metrics.md; sql/evidence_coverage.sql; sql/results/evidence_coverage.json; sql/source_age.sql; sql/results/source_age.json; tools/warehouse.py; docs/release/release-notes.md (point 4); site/briefs/accelerator-memory/index.html (the `data-derived="sql-cell"` attributes show that the page copies result cells).

**(c)** I did not read `accelerator_dependencies.sql`, which defines the basis rules that every metric inherits. I took its definitions from the coverage query's header. `metrics.md` has gone partly stale in two places:
- its history of the reference date stops at 2026-10-13, while the query now holds 2026-10-15;
- it still says that the research view "stays a prototype, not published (NG-13)", while the release notes say all pages are published.

The numbers are tiny (4 links per accelerator), so the "metrics" mainly show the method rather than tell you much. The project says this itself.

## 5. How agents are governed

**(a)** In this project, "agents" are not programs. There is no agent runtime, orchestrator, queue or autonomous write path. An agent is a **role**: a written contract that Claude (or occasionally the human) works under during a session. There are twelve roles, eleven of them active: Source Scout, Extractor, Verifier, Change Detector, Knowledge Architect, Data Auditor, Analyst, Editorial, Client Output, QA and Portfolio Reviewer. The Orchestrator is inactive, because the session prompt and the human coordinate the work.

Each contract has nine fields: inputs, outputs, allowed writes, forbidden writes, evidence requirements, handoff format, validation gate, failure behaviour. Some examples of the boundaries:
- The Extractor may write only to `data/staging/` and new source records.
- The Verifier may change only the status, date and bytes-read fields of staged claims.
- The Analyst may not hand-edit results or create composite scores.
- The Data Auditor writes the checks and may not loosen them.
- No role may write `data/claims.json` or a review verdict: that belongs to the human.

Three things enforce this:
1. `tests/test_agent_contracts.py` checks that:
   - the role list matches the project's rule document (CLAUDE.md);
   - every active role has a full contract;
   - every allowed-write path exists;
   - every tracked file is owned by some role or by the human;
   - no contract grants writes to canonical claims or verdicts.
2. The data checks (VD-8 and others) make it impossible for unreviewed claims to look canonical, whoever wrote them.
3. The human merges every pull request and takes every decision put as an option.

**(b)** docs/agents/roles.md; docs/agents/contracts.md; tests/test_agent_contracts.py (test names); README.md "How this was built"; docs/architecture/final-architecture.md; docs/case-study.md §4.

**(c)** The main doubt is that the tests check the **contracts as documents** and the **data's end state**, not what a role actually did in a given session. Nothing I read checks that, say, the Verifier did not edit a claim's statement. A post-hoc script in `docs/quality/audit-evidence/agent-audit/write_boundaries.py` seems to address this, but I did not open it. "Roles" are labels Claude assigns to its own work, so separation of duties is nominal. The project admits this:
- it records no review of the code by a person: 41 pull requests, 0 reviews, a median of 29 seconds from opening to merge;
- the checks that police Claude were written by Claude.

The session records that would show role discipline are in a private archive, not in this folder. I read only part of `contracts.md` and did not see the "Outside every contract" list.

## 6. How to reproduce the build

**(a)**
1. Set up Python 3.11 in a virtual environment.
2. Run `pip install -r requirements-test.txt -r requirements-analysis.txt`. The only runtime dependency outside the standard library is a pinned DuckDB; the test dependencies are also pinned.
3. Run `python tools/check_all.py`. In order, it runs:
   - the unit-test suite, including 28 planted data faults;
   - Gate 0 (`tools/validate_repo.py`: governing documents present, Markdown links resolve, no session records committed);
   - `--check` on the SQL warehouse and on each of the four page builds (HBM page, research view, 15 journey pages, client brief).

   Each `--check` rebuilds in memory and fails if the result differs **byte for byte** from what is committed. You know it matches when it prints "every check passed".

Two further, optional levels exist:
- **The break harness.** `python tests/regression/breaks.py SCRATCH_DIR` runs 230 deliberate faults, each of which must be caught for its named reason. It takes about 35 minutes on 4 cores.
- **Browser checks.** These need Node 22 and `npm ci`; the scripts are in `tests/browser/`.

For the published site, `tools/check_published.py <address>` compares the live pages with the commit. Every committed result and page also carries an input digest, so a stale output is detectable.

**(b)** README.md "Validate" and "How quality is controlled"; tools/check_all.py; tools/warehouse.py; tests/regression/README.md; docs/architecture/final-architecture.md §2, §5; docs/release/demonstration.md §3.

**(c)** I was not allowed to run anything, so I cannot confirm that the build actually reproduces. The `.github/` folder (`ci.yml`, `pages.yml`) is **not in this release-candidate folder**, although the README, release notes and final architecture all link to or rely on it, and `tests/test_agent_contracts.py` appears to read the CI file. Either the copy I was given omits dot-folders, or a test would fail on this tree as given. I cannot tell which. Byte-for-byte reproducibility also depends on the exact DuckDB version (results record "duckdb 1.5.6") and on Python 3.11. I did not check whether anything else, such as platform or locale, could affect the output.

## 7. Why the product is useful

**(a)** My judgement: it is useful less as a source of answers than as a **worked model of how to do traceable technology-policy research**. A policy researcher, think-tank analyst or due-diligence team could use it to:
- see exactly what is and is not publicly evidenced about HBM supply for two well-known accelerators, with every value one click from the quoted source sentence and the date of the evidence;
- see which US export-control texts name HBM or semiconductor equipment, with the acts' dated status computed rather than asserted, and a dated search for later rules;
- borrow the method: the claim types, explicit unknowns, the refusal of over-broad links (e.g. "GPU" is not matched to a rule's narrower term), "reported" versus "stated", and "a count of our records, not of the world".

Its honesty about gaps is a real strength. Most industry commentary would simply say "SK hynix supplies the H100's HBM". Here that is shown as one market-research firm's statement, valid only up to March 2024.

The limits are large, and the project states most of them:
- **Coverage is tiny.** There are two accelerators and one path. Foundries, packaging, equipment, data centres and energy have no supply-chain records.
- **Single sources.** No value rests on two independent publishers.
- **Old evidence.** Much of it is more than 12 months old, and there is no current supplier for the H100.
- **Few metrics.** The metrics are mostly "cannot be computed yet".
- **Description, not analysis.** It is US-only, and it explicitly gives no legal, compliance or exposure judgement.
- **Hard to read.** The pages and documents are dense with internal codes (D-xxx, S-numbers, KL-xx, VD-x). That makes them hard going for an outsider, and the brief's HTML alone is about 1 MB.
- **No outside users.** No person outside the project is recorded as having used it.

For a practitioner who needs an answer today, it is too narrow and too dated to rely on. For someone judging the builder's capability, or wanting a template for evidence-grade AI-supply-chain research, it is persuasive. The verification burden, however, rests on one human reviewing everything Claude drafts, and it is unclear how that scales.

**(b)** docs/case-study.md; docs/known-limitations.md; docs/release/release-notes.md; README.md "What it shows today" and "Limitations"; site/briefs/accelerator-memory/index.html; data/claims.json (the TrendForce claim).

**(c)** I could not judge how well the pages work for a reader, because I read the HTML as text and could not render it. I also could not tell whether the 1 MB brief really prints as the "one printable page" it is described as. I did not read the export-control comparison page or the policy documents in depth, so my view of the policy layer comes mainly from the README and the brief's summary.
