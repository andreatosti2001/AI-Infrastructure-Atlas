# S25 exit-condition reading: fresh reader 2's answers

**Reader:** a fresh agent (not an agent role), told to read as a data engineer who may be asked to take over maintaining the project. It was given only the release candidate's tree (public commit `495028e`, the tracked files as the publication serves them: without `.github/` and dotfiles; see `input.md`) and the seven fields of `form.md`, in an isolated folder. It was told to open nothing else, to use no web and no Git, and to run no code. It wrote nothing to either repository. Answered on 2026-10-16, before any assessment. Copied as given, from the line "Read:" on.

Read: README.md (all); docs/README.md (all); CLAUDE.md (not opened as a file in the folder; I did not rely on it); tools/check_all.py (all); docs/architecture/claim-model.md (all); docs/architecture/metrics.md (all); docs/architecture/sql-layer.md (all); sql/evidence_coverage.sql (all); sql/source_age.sql (all); sql/results/evidence_coverage.json (all); tools/warehouse.py (function list and docstrings only, by search); data/relationships.json (all); data/products.json (all); data/refused_candidates.json (first 60 lines, 2 of 21 records); data/claims.json (one record, about 60 lines); record counts for every data/*.json file and for data/staging/ (by search, not read); docs/agents/roles.md (all); docs/agents/contracts.md (lines 1-66 and the "Outside every contract" section, plus a search over the rest); tests/test_agent_contracts.py (first 100 lines plus the test names); docs/quality/human-reviews.md (first 80 lines: the index and the first two entries); docs/known-limitations.md (all); site/briefs/accelerator-memory/index.html (about 40 lines around the scope, summary, map and table, plus a search); site/hbm-insight/index.html (one search only); docs/quality/audit-evidence/engineering-audit/reproducibility.txt (all); requirements-test.txt and requirements-analysis.txt (all); docs/release/release-notes.md (all); tools/validate_repo.py (lines 20-79 plus a search); docs/case-study.md (all); tests/regression/README.md (all); docs/architecture/decisions.md (only counted its headings: 229 decisions); docs/architecture/final-architecture.md (sections 1-6); docs/architecture/final-audit.md (section 4 only); tools/build_page.py (lines 1-60 and 222-241). I also listed the folder with Glob and once with a directory listing (`ls -la`, no project code run) to see hidden files. About 31 files opened in total, most of them in full.

---

## 1. What the system does

**(a)** It is a small, hand-curated research database about the physical supply chain behind AI hardware. The database comes with generated static web pages and a printable "client brief". It answers one narrow question end to end: *what does an AI accelerator's memory depend on, who is reported to supply it, and which recorded US export-control texts name those parts?* It covers two accelerators, the NVIDIA H100 and AWS Trainium2. For each it records the High Bandwidth Memory (HBM) inside it, the reported HBM maker (SK hynix for the H100 up to 2024-03, Samsung for Trainium2, both only "reported" by a market-research firm), and the fact that HBM requires 3D die stacking. It also holds seven US export-control acts (BIS rules) and four "restricts" links saying an act's text names a class such as HBM or semiconductor equipment. The selling point is not coverage but traceability. Every value on a page links to a quoted sentence in a registered, hashed source. Unknowns are shown as named gaps, never as zero, and every page can be rebuilt byte for byte. The intended readers are policy and technology analysts, a "client" reading the brief, and, very explicitly, portfolio reviewers judging the builder's method. The pages say on every page that they are not legal, investment or procurement advice.

**(b)** README.md; docs/release/release-notes.md; docs/case-study.md; site/briefs/accelerator-memory/index.html; data/relationships.json.

**(c)**
- I did not open the entry page (site/index.html) or the export-control page, so I am taking their content from the README.
- "Who is it for" is stated mostly as "a client" and "a reviewer". No named user type with a concrete decision to make is described. The project itself says no outside person is recorded as having used it (KL-15).

## 2. How the data is structured

**(a)** The canonical data is plain JSON arrays in `data/`, one file per record kind (13 kinds), with JSON Schemas in `schemas/` (7 schemas, which also hold the controlled vocabularies).
- **Evidence:** `sources.json` holds 65 sources, each with URL, publisher, class, access time and SHA-256 of the bytes read. `claims.json` holds 197 claims.
- **Entities:** companies (9), jurisdictions (4), technologies (9), components (7), products (3), facilities (2), and policies (7 export-control acts).
- **Other records:**
  - `events` (20): dated happenings, for example an act's effective date.
  - `relationships` (9 typed edges: incorporates, designs, requires, operates, restricts).
  - `refused_candidates` (21): links that were considered and rejected, with a reason such as `evidence_not_fresh` or `item_has_no_record`.
  - `identity_basis`: why a rule-made ID holds.

**How the pieces link.** Records point *to* claims (`claim_ids`, `identity_claim_ids`), and claims point to sources through citations. A citation holds a locator, a verbatim anchor, a standing (party, originator or reporter) and the hash of the bytes read. Claims never point back to records; that direction is computed. Derived claims point to their input claims. Attributes are either a list of `{value, claim_ids}` assertions or a state object.

**How unknowns are represented.** JSON `null` is never used. An unknown is an object such as `{"state": "not_researched"}`, `not_publicly_determinable` (which must cite a search record), `not_applicable`, `not_stated`, `undated` or `no_record`. In SQL each such field is split into a `_value` column and a `_state` column, so NULL never stands alone. Staging (`data/staging/`) mirrors the canonical files for records awaiting review. It is currently empty, by my search.

**(b)** data/relationships.json; data/products.json; data/refused_candidates.json; data/claims.json (one record); docs/architecture/claim-model.md §1, §5, §8, §9; docs/architecture/sql-layer.md §3, §8; docs/architecture/final-architecture.md §2; README.md "What it contains".

**(c)**
- I did not open the schemas or the entity and relationship taxonomies.
- The volume is very small: 9 edges in total. The "graph" is really a handful of links plus a lot of identity and policy claims.
- I could not see a single overview diagram of the data model; I pieced it together from three documents.
- Some fields hold either a list or a state object (`vendor_process_name` is a list on one product and `{"state": ...}` on another). This works, but a consumer has to handle both shapes.

## 3. How claims are verified

**(a)** The workflow is a staged pipeline:

`retrieve and register the source (with hash) -> Extractor drafts the claim into data/staging/ as unverified, not_reviewed -> Verifier re-reads the anchor in the registered bytes -> the human gives a verdict -> the claim moves unchanged to data/claims.json`

- **Claim types.** Each claim is one proposition, typed FACT, ATTRIBUTION, DERIVATION, INTERPRETATION or IMPLICATION. Strict rules apply: a FACT needs a first-hand source, a third-party report can only be an ATTRIBUTION, and the Atlas's own inferences are DERIVATIONs that cite other claims, never sources.
- **The Verifier** re-reads the anchor sentence in the registered bytes and sets the evidence status: `supported`, `partial`, `context_only` or `disputed`. It records `verified_on` and the hash it read.
- **The human decides** whether a claim becomes canonical. The verdict (accepted or rejected, the date, and a pointer to an entry in docs/quality/human-reviews.md) is written into the claim's `review` field.
- **The checks:**
  - VD-8: every canonical claim is human-accepted and `supported` or `disputed`, and rests only on canonical claims; staging holds no accepted claim.
  - test_human_reviews.py ties the counts in the review record to the data.
  - The SQL layer and the pages read only canonical files, so nothing in staging can appear.
- **How a link is shown.** Whether a link appears as "stated", "inferred" or "reported" is derived from the types of the claims it cites. A link also needs fresh enough evidence: a 12-month horizon applies to time-sensitive links, otherwise the link becomes a recorded gap, as with TSMC fabricating the H100.

**(b)** docs/architecture/claim-model.md §3-§7, §11, §14; docs/quality/human-reviews.md; README.md "How evidence works"; docs/agents/contracts.md (Extractor, Verifier); data/claims.json (one record); data/refused_candidates.json (cand-001).

**(c)**
- **How independent the human review is.** The README says the human "read and accepted or rejected every claim". The review record shows batch reviews: 62 claims in one entry, 37 in another. The first entry records a spot-check of only three anchors by the human. The project says that when Claude drafts and also verifies, the human's review is the "independent check" (D-182). For anything beyond those spot-checks, I could not tell how deeply the human checked each claim. 197 of 197 claims were accepted and none was ever rejected or narrowed. That could mean careful drafting or light review; the folder does not let me tell.
- **What a machine can check.** The `review` field is written by Claude "on the human's recorded verdict". No mechanism can show that the verdict really came from the human; the checks only show it is consistent with the review record.
- Anchors for sources that refuse automated retrieval can only be re-checked from a file the human supplies (KL-14).

## 4. How metrics are produced

**(a)**
- **How the numbers are computed.** `tools/warehouse.py` loads the canonical JSON (never staging) into a fresh in-memory DuckDB, one thread and pinned to 1.5.6. It runs the four queries in `sql/` in dependency order; a later query reads an earlier query's result as a view. Each result is written to `sql/results/<query>.json` together with the query's SHA-256, the SHA-256 of every input file and the engine version. The database is never stored.
- **The two computed metrics.**
  - Evidence coverage: per accelerator, the counts of stated, inferred, reported and gap links. Trainium2: 4 links = 2 stated + 1 inferred + 1 reported + 0 gaps. H100: 1 stated + 1 inferred + 1 reported + 1 gap.
  - Source age: the age of each link's newest evidence against a reference date fixed in the SQL file (2026-10-15), not "today", so results stay byte-stable.
- **The three supplier metrics** (count, geographic concentration, single-sourcing) are deliberately shown as "cannot be computed yet", because no source states a complete supplier set.
- **How pages use them.** Page builds copy cells from the committed results; they do not compute. Each query file opens with comment headers (question, population, denominator, assumptions, missing data, does-not-prove). Those headers are rendered as the "How this was computed" tutorial on the page.
- **How to check a number.**
  1. Run `python tools/warehouse.py --check`, which reruns and byte-compares.
  2. Read the query: the population and denominator are stated in its header.
  3. Follow the IDs that each row carries (`record_id`, `claim_ids`, `source_ids`) with `tools/trace.py`.
  4. The tests (WH-2, WH-6, WH-12, WH-13) recompute the metrics independently in plain Python, and they move the reference date to check that only the ages change.

**(b)** docs/architecture/metrics.md; docs/architecture/sql-layer.md; sql/evidence_coverage.sql; sql/source_age.sql; sql/results/evidence_coverage.json; tools/warehouse.py (function list); site/briefs/accelerator-memory/index.html (cells carry `data-query`/`data-row`/`data-column`); requirements-analysis.txt.

**(c)**
- **Stale tutorial text on a page.** The header of `sql/evidence_coverage.sql` still says under "missing data": "The suppliers of the memory are not researched". That is no longer true: both suppliers are now "reported", and the same query's result has `reported: 1` per accelerator. The sentence is rendered on the published research view (site/hbm-insight/index.html contains it). So the "every text node has a home" checks verify that text came from its home, but not that the home is still true.
- **Stale design document.** metrics.md still describes source age "as of 2026-10-07" in its summary table, while the query now uses 2026-10-15.
- **Not opened.** I did not read `accelerator_dependencies.sql` in full; it is the base query and the most important one. I also did not read the test files that do the independent recomputation.
- **What the "metrics" are.** They are counts over 4 rows per accelerator. The project is candid that they describe its own records, not the industry.

## 5. How agents are governed

**(a)** The "agents" are not programs. They are 12 named roles, 11 of them active: Source Scout, Extractor, Verifier, Change Detector, Knowledge Architect, Data Auditor, Analyst, Editorial, Client Output, QA and Portfolio Reviewer; the Orchestrator is inactive. Claude (Anthropic's model) plays all of them inside human-initiated working sessions, and the human plays the Orchestrator through session prompts.

**What a contract fixes.** Each active role has a written contract in docs/agents/contracts.md, with inputs, outputs, ALLOWED_WRITES, FORBIDDEN_WRITES, evidence requirements, validation gate and failure behaviour. For example:
- the Extractor may only write `data/sources.json` and `data/staging/*`;
- the Verifier may only change `evidence_status`, `verified_on`, `disputed_with` and the `read` field in staging;
- no role may write `data/claims.json` or a review verdict. Those, the canonical entity files, the constitutional documents and the contracts themselves are "outside every contract": changed only on the human's recorded decision.

**What stops a role in practice.**
1. **Static checks.** `tests/test_agent_contracts.py` checks that every tracked file has an owner role, that no contract grants writes to canonical claims, and that each role's validation gate is a test that CI runs.
2. **Data checks.** VD-8 and related checks mean an unreviewed claim cannot sit in the canonical files without failing CI.
3. **Process.** The human merges every pull request and decides every option.

There is no agent runtime, queue or autonomous write path, by decision (NG-08).

**(b)** docs/agents/roles.md; docs/agents/contracts.md; tests/test_agent_contracts.py; README.md "How this was built"; docs/case-study.md §4; docs/architecture/final-audit.md §4.

**(c)**
- **Write boundaries are not enforced at write time.** Since one Claude session plays every role, the per-role boundaries are discipline plus after-the-fact data checks. The project's own audit says the owner check "proves an owner exists, not that it is the only one" (P-11).
- **Weak human gate on code.** The case study reports 41 pull requests with 0 reviews and 0 comments, merged with a median of 29 seconds from opening to merge (P-2). So "the human merges every change" is a weak gate for code. Code correctness rests on tests that Claude itself wrote, although these are tested by a harness of 230 planted faults.
- **CI file missing from this folder.** The contract test reads `.github/workflows/ci.yml` to confirm CI runs the tests. That file is not present in this folder; see 6.

## 6. How to reproduce the build

**(a)** The README's recipe:
1. Create a Python 3.11 virtualenv. CI pins 3.11; check_all prints a note if you use another version.
2. Run `pip install -r requirements-test.txt -r requirements-analysis.txt`. These are exact pins: jsonschema and its dependencies, plus duckdb 1.5.6. Everything else is the standard library.
3. Run `python tools/check_all.py`.

check_all runs, in order and stopping at the first failure:
- the unit test suite (`unittest discover -s tests`), which includes 28 planted data faults;
- Gate 0 (`tools/validate_repo.py`: required documents exist, every relative Markdown link resolves, no session records are committed);
- `--check` on the warehouse, then on the HBM page, research view, 15 journey pages and client brief, in that build order.

Each `--check` rebuilds in memory and exits 1 if the committed bytes differ. You know it matched when every step prints "ok" and the script ends with "every check passed". The expected outputs are shown in docs/quality/audit-evidence/engineering-audit/reproducibility.txt ("results: up to date", "page: up to date", 466 tests OK at S22, also reproduced on Python 3.12 and 3.13 for the page builds).

You can also cross-check digests:
- each SQL result lists the SHA-256 of every input;
- each page prints an "input digest".

Further layers:
- **Browser checks:** Node 22, `npm ci`, then the scripts in tests/browser/.
- **The break harness:** `python tests/regression/breaks.py SCRATCH_DIR`; about 35 minutes on 4 cores.
- **The published-site check:** `tools/check_published.py <address>`.

**(b)** README.md "Validate" and "How quality is controlled"; tools/check_all.py; tools/validate_repo.py; requirements-test.txt; requirements-analysis.txt; docs/quality/audit-evidence/engineering-audit/reproducibility.txt; tests/regression/README.md; docs/architecture/sql-layer.md §2; tools/build_page.py (header).

**(c)**
- **This folder as given probably would not pass its own checks.** There is no `.github/` directory in it, but:
  - README, release notes and final-architecture refer to `.github/workflows/ci.yml` and `pages.yml`;
  - docs/release/release-notes.md links to `../../.github/workflows/`, which Gate 0's link check should then report as missing;
  - `tests/test_agent_contracts.py` reads `.github/workflows/ci.yml` and asserts that it contains "unittest discover -s tests". With the file absent, it reads an empty string and should fail.

  Either hidden files were dropped when this release candidate was copied, or the published tree really lacks them. I could not tell which, and I did not run anything to confirm.
- **Missing git history.** There is no `.git` folder either. Some tests use `git ls-files` (with a fallback), and the break harness's `--since main` needs git.
- **Page builds depend on documentation files.** They read docs/architecture/decisions.md and other design documents (parsing decision titles and rule tables by regular expression). An edit to a document can therefore make a page stale, and the formatting of those documents is effectively part of the build contract. check_all.py warns about exactly this.
- **Not opened.** I did not open package.json or the browser scripts, so I cannot say which browser tool they use.

## 7. Why the product is useful

**(a)** *My judgement.* As a data product, it is small: 9 relationships, 2 accelerators, 7 export-control acts. Its main answer is that HBM goes into both chips and the suppliers are known only through market-research reports. That answer would not surprise an industry analyst, and much of the evidence is old or single-source (no value has two independent publishers). Its real value is as a **worked, checkable template for evidence-grade research data**:
- claim typing that keeps "a company says", "a third party reports" and "we infer" apart;
- explicit unknown states that never collapse to zero;
- refused candidates kept as records, so you can see what was *not* asserted and why;
- deterministic SQL with input digests and self-documenting queries;
- pages whose every text node is traced to a record;
- a large, tested battery of checks, including planted faults that prove the checks can fail.

**Who could use it, and for what.**
- A policy or due-diligence analyst could use the brief as a carefully hedged starting point, with sources one click away.
- A data team building a provenance-heavy knowledge base could reuse the patterns.
- A reviewer could see what disciplined AI-assisted research looks like.

**Main limits.**
- Narrow coverage.
- Single-voice, partly stale evidence.
- No analysis or advice: it describes texts and never says what applies to whom.
- No search.
- Very heavy internal jargon. D-numbers, S-numbers and rule codes are everywhere, which makes onboarding slow (229 decisions, many audits).
- A process whose human checks on code are thin.

**Worth maintaining?** As a maintainer, I would say yes, if the goal is to grow this method into wider coverage. The tooling is standard-library Python plus one pinned dependency, and it is well guarded. The cost is high, though: the ceremony per added fact is large, the build is coupled to Markdown documentation, and the checks do not catch stale explanatory prose (point 4 above).

**(b)** docs/case-study.md; docs/known-limitations.md; docs/architecture/final-audit.md §4; README.md "Limitations"; site/briefs/accelerator-memory/index.html; data/relationships.json; tools/build_page.py.

**(c)**
- No outside user is recorded (KL-15), so usefulness to a real client is unproven.
- I did not open the export-control comparison page, which may be the most useful page to a policy reader.
- I cannot judge how accurate the domain content is without the sources; I relied on the project's own re-read audit (178 of 178 passages found, as reported in the README and case study), which I did not verify.
