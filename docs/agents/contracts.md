# Agent contracts

**Status:** ACCEPTED (human review, 2026-09-30; D-052, D-010); the Editorial and QA contracts accepted on
2026-10-02 (D-107). Paths are kept current when a file moves (Editorial, paths only); no role or boundary
changes without a decision. S19's agent audit (`docs/architecture/agent-audit.md`): every file has an owner,
checked (D-180); the Analyst's contract (D-181); the Verifier re-scoped (D-182); drafts always in staging (D-183),
all accepted on 2026-10-14. S21: the Client Output's contract, for the client brief (D-205), accepted on 2026-10-14. S21.5: the Change Detector's
contract, for the dated search for later rules (D-207), decided by the human on 2026-10-14. S24: the Portfolio Reviewer's
contract, for the portfolio audit and v1.0's known limitations (D-223), decided by the human on 2026-10-16.

MA §12 contracts for the roles [`roles.md`](./roles.md) marks active. Each contract has
MA's nine fields, in MA's order.

- **Paths are repository paths.** A role writes only its allowed paths. A path ending in `/` covers its folder;
  `*` matches within one name. Every tracked file is in some role's allowed writes or in the list "Outside every
  contract" below; `tests/test_agent_contracts.py` fails otherwise (D-180). The session report, kept in the
  private development archive outside this repository (D-151), may record any role's findings.
- **A validation gate is a test module that CI runs on every push** (L-02).
  `tests/test_agent_contracts.py` checks that each one exists.
- **The human's review is outside every contract.** No role writes a `review` verdict or
  `data/claims.json` (CLAUDE.md §9, class C; `claim-model.md` §7). Moving an accepted claim
  there is done in a session, on the human's recorded verdict.

## Source Scout

| Field | Value |
|---|---|
| ROLE | Source Scout |
| INPUTS | the session's question; the preferred classes for the matrix row it concerns (`source-policy.md` §7); the source records in `data/sources.json`, to avoid duplicates |
| OUTPUTS | candidate URLs, each with the class it would have and the row it would serve; access gaps met (host, response, time) |
| ALLOWED_WRITES | the session report, outside this repository (the candidate list and the access gaps); `docs/research/search-logs/` for a search log that a research document cites as its method (D-151); the later-rule search tool `tools/later_rule_search.py` (S22, D-211), which writes its logs in `docs/research/search-logs/later-rules/`; the research documents `docs/research/domain-map.md`, `docs/research/source-register.md`, `docs/research/hbm-supplier-research.md` and `docs/research/hbm-supplier-research-original-rules.md` (S19, D-180) |
| FORBIDDEN_WRITES | any file in `data/`; any schema; a claim's `review`; a class assigned without reading the source |
| EVIDENCE_REQUIREMENTS | search results and snippets are discovery aids only, never cited (`source-policy.md` §2, MA §11.2); no circumvention of a refusal (RA-2); declaring an identity to a site is the human's (RA-7) |
| HANDOFF_FORMAT | a report table: URL, proposed class, row served, why it is preferred, access result |
| VALIDATION_GATE | none of its own writes reach data; the Extractor's sources are checked by `tests/test_data_schema.py` and `tests/test_data_integrity.py`; from S22, the search tool by `tests/test_later_rule_search.py`, which the Data Auditor writes and the Source Scout does not (D-211), and its logs by JR-13 in `tests/test_journeys.py` |
| FAILURE_BEHAVIOUR | a refused or unreadable source is recorded as an access gap and left unsearched (SP-7, ER-3); never replaced by a secondary summary |

## Extractor

| Field | Value |
|---|---|
| ROLE | Extractor |
| INPUTS | a retrieved source (bytes, access time, hash) or a manual retrieval by the human (RA-4); the claim model and the schemas |
| OUTPUTS | a source record; candidate claims with citations (locator, verbatim anchor, standing, originator for a chain) or input claims with reasoning; all with `evidence_status: unverified` and `review: not_reviewed` |
| ALLOWED_WRITES | `data/sources.json` (new records, registered when retrieved and before any review, while their claims wait in staging: S16.6, D-146; `publisher_entity` per D-065); `data/staging/claims.json` (new claims); `data/staging/companies.json`, `data/staging/jurisdictions.json` (staging entity records, S07, D-055); `data/staging/technologies.json`, `data/staging/components.json`, `data/staging/products.json` (S08, D-077); `data/staging/facilities.json`, `data/staging/events.json` (S09, D-087); `data/staging/relationships.json` (S10, D-098); `data/staging/refused_candidates.json` (S12, D-109); `data/staging/identity_basis.json` (S14, D-117); `data/staging/policies.json` (S17, D-155) |
| FORBIDDEN_WRITES | `data/claims.json`; a claim's `review`; `evidence_status` other than `unverified`; `verified_on` or a citation's `read`; migrated source values (a change needs a decision, VD-9) |
| EVIDENCE_REQUIREMENTS | every candidate keeps its provenance (MA §11.3); the anchor is copied verbatim; the type follows `claim-model.md` §2 and ER-1 to ER-10; unknowns are explicit states, never null or zero |
| HANDOFF_FORMAT | the records themselves, plus a report list of new IDs for the Verifier |
| VALIDATION_GATE | `tests/test_data_schema.py` (VD-2) and `tests/test_data_integrity.py` (VD-1, VD-3 to VD-13); for entity records, `tests/test_data_entities.py` (V-1, V-4, V-9, V-10, CE-1, ID-1, J-1, S07; CI-1, DEF-1, DEF-2, B-1, PI-1, IO-1, S08; FI-1, HQ-1, FK-1, CAP-1, S09); for events, `tests/test_data_events.py` (EV-1 to EV-4, EI-1, S09); for edges, `tests/test_data_relationships.py` (V-1 to V-10, CE-1, RI-1, PN-1, EP-1, PE-1, RV-1, S10) |
| FAILURE_BEHAVIOUR | a value the source does not give is left as an explicit state; a sentence that cannot be quoted is not cited; the problem is reported, never patched with an inference; drafts always land in `data/staging/` before the human's review, and a session prompt cannot keep them elsewhere (S19, D-183) |

## Verifier

| Field | Value |
|---|---|
| ROLE | Verifier |
| INPUTS | staged claims with `evidence_status: unverified`; the cited sources, re-retrieved or supplied by the human |
| OUTPUTS | per claim: a status (`supported`, `partial`, `context_only`, or `disputed` with the competing claims), `verified_on`, and each citation's `read`; findings for the report |
| ALLOWED_WRITES | `data/staging/claims.json`: only `evidence_status`, `verified_on`, `disputed_with` and each citation's `read`; `data/staging/refused_candidates.json`: only each considered sentence's `read` (D-109); the session report (D-151) |
| FORBIDDEN_WRITES | a claim's `statement`, `claim_type`, citations' anchors or locators (a change is a new claim from the Extractor); a claim's `review`; `data/claims.json`; source records |
| EVIDENCE_REQUIREMENTS | its authority is the re-read: each anchor found on its stated page in the bytes whose hash is the registered one, by a script whose output is kept, and a written list of every statement whose wording exceeds its anchor; read the whole sentence at each locator (`claim-model.md` §6); a class is never a verification (ER-10); record the bytes read; re-check anchors when a hash has changed (`source-policy.md` §12). When the session that drafted the claims also verifies them, the judgement of wording is not independent: the human's review of every claim is the independent check (D-182) |
| HANDOFF_FORMAT | the updated claims, plus a report table: claim, status, what was read, and any wording that exceeds its evidence |
| VALIDATION_GATE | `tests/test_data_integrity.py` (VD-6, VD-7, VD-11, VD-12) and `tests/test_data_schema.py` (VD-2) |
| FAILURE_BEHAVIOUR | a source that cannot be re-read leaves the claim `unverified` (SP-7); an anchor not found makes it `context_only`; the Verifier never invents replacement evidence (MA §11.4) |

## Change Detector

| Field | Value |
|---|---|
| ROLE | Change Detector |
| INPUTS | two versions of the same thing: an act the Atlas holds (its registered official text, the claims and links that cite it) and a later official text the Source Scout found and the Extractor registered; or a registered source and its re-retrieval (a changed hash); the search log in `docs/research/search-logs/` |
| OUTPUTS | candidate changes, one per comparison: the earlier text and the later text, each quoted at its locator in registered bytes, and what the later text does to the earlier entry or act in the later text's own words (adds, removes, revises, moves, repeals, or none found); for a search that finds nothing, the terms, registers and dates searched; a changed hash reported for the Verifier's re-read |
| ALLOWED_WRITES | `docs/research/change-detection.md` (the rules it keeps and the comparisons, S21.5, D-207); the session report, outside this repository (D-151) |
| FORBIDDEN_WRITES | any file in `data/` (the Extractor drafts the records a change needs, in staging); a claim's `review`; a date on a link, or an act dated, ended or repealed by anything but its own events (D-169, D-156); a source re-registered after its hash changed; a conclusion: that a change has legal effect, that an act or entry is in force, repealed or superseded in the Atlas's own voice, or that a product or firm is controlled (LA-1 to LA-5) |
| EVIDENCE_REQUIREMENTS | both sides of every comparison are quoted from official texts (`official_legal_text`, D-158) at their locators, in the bytes whose hash is registered; a secondary text (a press release, an index entry, a summary) may point to a later text, never stand for it (SP-7); a search that finds nothing records its terms, registers and dates, and says "none found in the searched window", never "none exists"; a text that cannot be retrieved is an access gap |
| HANDOFF_FORMAT | a comparison table in `docs/research/change-detection.md` §1: entry or act, earlier text and locator, later text and locator, the change in the later text's words, the candidate record the Extractor drafts, and its status (candidate until the human's verdict) |
| VALIDATION_GATE | `tests/test_agent_contracts.py` (the contract, its writes and its owner rows); the records it hands over are checked by the Extractor's gates (`tests/test_data_integrity.py`, `tests/test_data_events.py`) |
| FAILURE_BEHAVIOUR | a comparison whose later text cannot be retrieved or read stays open as an access gap; a later text whose effect on an entry is unclear is quoted and left as a question to the human, never resolved by inference; a finding that would change an accepted rule, a check or the schema stops the session (CLAUDE.md §18) |

## Knowledge Architect

| Field | Value |
|---|---|
| ROLE | Knowledge Architect |
| INPUTS | the session prompt; the schemas; the taxonomies, the source policy and the claim model; the decision log |
| OUTPUTS | schema and vocabulary changes, each with a decision; one-home rulings; ID formats |
| ALLOWED_WRITES | `schemas/`; `docs/architecture/claim-model.md`; `docs/architecture/company-dataset.md` (S07); `docs/architecture/concept-dataset.md` (S08); `docs/architecture/facility-dataset.md` (S09); `docs/architecture/edge-dataset.md` (S10); `docs/architecture/vertical-slice.md` (S11); `docs/architecture/milestone-audits/` (S12, the audit report; S19: also when the Portfolio Reviewer is inactive); `docs/architecture/decisions.md` (append only); `docs/architecture/entity-taxonomy.md`, `docs/architecture/relationship-taxonomy.md`; `docs/architecture/policy-dataset.md` (S17), `docs/architecture/policy-links.md` (S18); `docs/research/source-policy.md` (rows and rules, each with a decision); `docs/research/supplier-evidence-rules.md`, `docs/research/supplier-presentation.md` (S16.6); the audit record: `docs/architecture/agent-audit.md` (S19), `docs/architecture/engineering-audit.md` (S22), `docs/research/content-audit.md` (S13), `docs/research/release-content-audit.md` (S23), `docs/quality/audit-history.md`, `docs/quality/audit-evidence/` (D-180), except the portfolio audit's evidence folder (the Portfolio Reviewer's, S24, D-223) |
| FORBIDDEN_WRITES | any file in `data/`; a claim's `review`; an accepted vocabulary value or field without a decision the human approves first; the root constitutional documents |
| EVIDENCE_REQUIREMENTS | a vocabulary value needs a used case (M0 audit A-1, L-09); where a choice rests on the domain, it cites the concept or source that shows it |
| HANDOFF_FORMAT | a decision record (`proposed`) and the changed schema, with fixtures |
| VALIDATION_GATE | `tests/test_claim_schema.py`, `tests/test_source_record_schema.py`, `tests/test_claim_model.py` |
| FAILURE_BEHAVIOUR | a change that would alter an accepted schema, vocabulary or the claim ID format stops the session and is reported (S06 prompt §16) |

## Data Auditor

| Field | Value |
|---|---|
| ROLE | Data Auditor |
| INPUTS | `data/`, the schemas, the claim model's §4 tables, the source policy's matrix |
| OUTPUTS | the `validate-data` checks and their results; findings of broken references, duplicates, impossible dates and missing provenance (MA §11.7) |
| ALLOWED_WRITES | `tests/`; `tests/fixtures/`; `tools/` (standard library only, D-026), except the framing and style in `tools/page_template.html`, `tools/insight_template.html`, `tools/journey_template.html` and `tools/brief_template.html` (Editorial), the brief's build `tools/build_brief.py` (Client Output, S21, D-205), and the later-rule search tool `tools/later_rule_search.py` (Source Scout, S22, D-211); `site/hbm-chain/index.html`, written only by the build step `tools/build_page.py` (S11, D-102); `site/hbm-insight/index.html`, written only by `tools/build_insight.py` (S14.5, D-125); `site/index.html`, `site/questions/export-control-texts/index.html`, `site/companies/` and `site/places/` (one `index.html` per record), written only by `tools/build_journeys.py` (S20, D-190, D-197); the CI workflow `.github/workflows/ci.yml`, the pins `requirements-test.txt` and `requirements-analysis.txt`, and the browser checks' `package.json` and `package-lock.json` (S22, D-212) (a new dependency needs a decision), `.gitignore` (D-180) |
| FORBIDDEN_WRITES | any file in `data/`: the Auditor reports, and the Extractor or Verifier fixes; a claim's `review`; a check weakened to make data pass |
| EVIDENCE_REQUIREMENTS | each check is shown to catch a planted fault before it is trusted (deliberate breaks); prose counts are tested or labelled as measured (L-04) |
| HANDOFF_FORMAT | failing test output naming the record and the rule, in the session report |
| VALIDATION_GATE | `tests/test_data_integrity.py`, `tests/test_data_schema.py`, `tests/test_data_entities.py`, `tests/test_freshness.py`, `tests/test_trace.py`, `tests/test_agent_contracts.py`; from S09, `tests/test_data_events.py` and `tests/test_facility_status.py`; from S10, `tests/test_data_relationships.py` and `tests/test_navigate.py`; from S11, `tests/test_page.py`; from S20, `tests/test_journeys.py` (D-197); from S21, `tests/test_brief.py`, the client brief's checks, which the Data Auditor writes and the Client Output does not (D-205) |
| FAILURE_BEHAVIOUR | a failure that cannot be explained stops the session (CLAUDE.md §18); no test is skipped or loosened to get green |

## Analyst

| Field | Value |
|---|---|
| ROLE | Analyst |
| INPUTS | the canonical records, read by `tools/warehouse.py`; the analytical question, its population and denominator (`metrics.md`); PEF §8 |
| OUTPUTS | SQL queries with their tutorial headers; their results, computed by `tools/warehouse.py`; the metric and SQL-layer documents; analytical audits |
| ALLOWED_WRITES | `sql/*.sql`; `sql/results/`, written only by `tools/warehouse.py`; `docs/architecture/sql-layer.md`, `docs/architecture/metrics.md`, `docs/architecture/analytical-audit.md` (S14 to S16; D-181) |
| FORBIDDEN_WRITES | any file in `data/`; a claim's `review`; a result typed or edited by hand; the warehouse loader and the checks (the Data Auditor's); a metric without its question, population and denominator; a composite score, rank or share (NG-11) |
| EVIDENCE_REQUIREMENTS | every number is recomputed from versioned inputs (WH-2) and by an independent computation in the checks (WH-10 to WH-14); an unknown is a gap, never a zero; each query states what it does not prove (PEF §8) |
| HANDOFF_FORMAT | the query, its result and the page rebuilt in one commit, with the question and denominator stated in the query's header |
| VALIDATION_GATE | `tests/test_warehouse.py` (WH-1 to WH-15) and `tests/test_insight.py` (the research view's cells equal their results) |
| FAILURE_BEHAVIOUR | a metric that cannot be computed is shown as "cannot be computed yet", never estimated (D-130); a result that differs from a fresh run stops the build |

## Editorial

| Field | Value |
|---|---|
| ROLE | Editorial |
| INPUTS | the page as built from canonical records; `docs/architecture/vertical-slice.md` (the composition, the text provenance rule); `claim-model.md` §13 (how claims are displayed); the schema definitions the page's terms render |
| OUTPUTS | the page's framing (prose that states no fact and names no record) and its style; the state rows of the documentation, as each session prompt lists them |
| ALLOWED_WRITES | `tools/page_template.html`, `tools/insight_template.html`, `tools/journey_template.html` and `tools/brief_template.html` (framing and style only; S20, D-197; S21, D-205); the visual design documents `docs/architecture/visual-architecture.md` and `docs/research/visual-benchmark.md` (S14.5, D-122 to D-126; D-180) and the brief's design `docs/architecture/client-brief.md` (S21, D-205); `README.md`, `docs/README.md` and `docs/architecture/baseline.md` (state rows); the session report (D-151) |
| FORBIDDEN_WRITES | any file in `data/`; a claim's `review`; `site/hbm-chain/index.html` and every other page under `site/` (generated, never edited by hand); a name, value, date, count or relation typed into the template; framing that names a record, holds a digit, or says "none" for a missing relationship; the labels and journey specification in `tools/build_page.py` (the Data Auditor's) |
| EVIDENCE_REQUIREMENTS | framing adds no fact (NG-09, `claim-model.md` §13); every value reaches the page through the build from its home (D-105); a missing edge is "no recorded relationship" (RR-7); no "critical", "concentrated", share, rank or score (NG-11) |
| HANDOFF_FORMAT | the template change and the rebuilt page in one commit, with the framing changes listed in the session report |
| VALIDATION_GATE | `tests/test_page.py` (PG-1 every text node has a home, PG-6 framing marked and naming no record, PG-7 rebuild, PG-8 style and contrast); `tests/test_journeys.py` (JR-1, JR-9 the Atlas's own voice, JR-11) for `tools/journey_template.html` (S20, D-197); `tests/test_brief.py` (BR-1, BR-9, BR-11) for `tools/brief_template.html` (S21, D-205) |
| FAILURE_BEHAVIOUR | a sentence that needs a fact becomes a gap on the page or a question to the human, never framing; a failing check is reported, never loosened |

## Client Output

| Field | Value |
|---|---|
| ROLE | Client Output |
| INPUTS | the canonical records, through `tools/build_page.py`'s and `tools/build_journeys.py`'s machinery; the committed SQL results `sql/results/accelerator_dependencies.json` and `sql/results/source_age.json`; the status rule `tools/policy_status.py`; accepted decisions; the brief's design `docs/architecture/client-brief.md` (D-202, D-203) |
| OUTPUTS | the client brief: its specification, labels and composition, and the page they produce; a summary composed only by copying values, tallying the rows it shows, taking the first and last of a column, and grouping rows (D-124 rules a to d), with statuses from the status rule on the as-of date |
| ALLOWED_WRITES | `tools/build_brief.py` (S21, D-205); `site/briefs/`, written only by `tools/build_brief.py` |
| FORBIDDEN_WRITES | any file in `data/`; `sql/` and `sql/results/`; a claim's `review`; the checks (`tests/`, the Data Auditor's) and the other builds; the template's framing (the Editorial's); a value, count or date typed into the build or the template; a sentence that no check can recompute (V-2); a recommendation, a compliance determination, or a statement that a product or firm is controlled (LA-1 to LA-5, NG-12) |
| EVIDENCE_REQUIREMENTS | it may summarise and never alters a record (MA §11.10); every value reaches the brief from its home (D-105); scope, limits, the as-of date and the input digest travel with the brief (U-5); every citation resolves to a source record; a recorded gap is phrased as a gap, never as a link; unknown is never zero |
| HANDOFF_FORMAT | the build change and the rebuilt brief in one commit, with any new label or summary sentence listed in the session report |
| VALIDATION_GATE | `tests/test_brief.py` (BR-1 to BR-12), run in CI; `python tools/build_brief.py --check` |
| FAILURE_BEHAVIOUR | a section the records cannot fill states its gap, never framing that fills it; rows that do not fit the brief's compositions make the build refuse, never draw; a failing check is reported, never loosened |

## QA

| Field | Value |
|---|---|
| ROLE | QA |
| INPUTS | the generated page `site/hbm-chain/index.html`; `docs/architecture/vertical-slice.md` §7, §8; MA §14 (Gate 6, Gate 7) and the roadmap's four visual QA questions |
| OUTPUTS | browser findings: screenshots at desktop and 375 px, the keyboard path to every panel, console and network logs, contrast measured on rendered text; the answers to the visual QA questions (truth, clarity, context, presentation) |
| ALLOWED_WRITES | the session report, outside this repository (findings and screenshots; D-151) |
| FORBIDDEN_WRITES | any file in `data/`; a claim's `review`; the page, the template or the build (a finding goes to the Editorial or the Data Auditor); a repository dependency for the browser run (D-106) |
| EVIDENCE_REQUIREMENTS | every finding cites a screenshot, a log line or a measured value; no session is declared complete from visual inspection alone (MA §15); a browser run states the browser, the widths and the page's input digest |
| HANDOFF_FORMAT | a report table: check, width, result, evidence |
| VALIDATION_GATE | `tests/test_page.py` (PG-8 accessibility basics, PG-9 links and no network resource), run in CI; the browser run (`tests/browser/`) is recorded in the session report, outside CI (D-106) |
| FAILURE_BEHAVIOUR | a failure is reported with its log and screenshot; a page that fails a check is not shown to the human as done, and never published (NG-13) |

## Portfolio Reviewer

| Field | Value |
|---|---|
| ROLE | Portfolio Reviewer |
| INPUTS | the repository, its Git history and the product (the generated pages, the SQL layer and its tutorials, the tools and checks); the decision log and every accepted audit; the archive's prompts and reports, read in a session (D-152); `PROJECT-EVALUATION-FRAMEWORK.md` §3, §4, §10, §12; MA §11.12; the roadmap's capability points; the answers of cold readers given only named artifacts |
| OUTPUTS | at a major milestone, PEF §12's eight outputs: process findings, outcome findings, the evidence for each, maturity per dimension for process and outcome, regressions since the previous audit, high-value improvements, explicitly rejected improvements, new learning outcomes; v1.0's known limitations, one row per gap, each linked to its record (the finding, the decision, the page framing that states it) |
| ALLOWED_WRITES | the portfolio audit `docs/architecture/portfolio-audit.md` and its evidence `docs/quality/audit-evidence/portfolio-audit/` (measurement scripts, standard library, and their outputs); `docs/known-limitations.md` (S24, D-222, D-223); the session report, outside this repository (D-151) |
| FORBIDDEN_WRITES | any file in `data/`; a claim's `review`; a page, a template or a build (a limit the pages should state goes to the Editorial as a proposal, through the human); the checks (the Data Auditor's), including the known-limitations check; `docs/architecture/decisions.md` and `docs/quality/audit-history.md` (the Knowledge Architect's); a rating or finding marked accepted before the human rules |
| EVIDENCE_REQUIREMENTS | a capability is credited only for evidence a reviewer can open and recount (a check that fails on a planted fault, a query with its tutorial, a decision with its rejected alternatives, a claim re-read against its source), never for a document's description of itself (PEF §10); every finding is an `INTERPRETATION` shown beside its evidence; every count names its population and denominator and is produced by a script whose output records the commits or hashes it read, run twice with identical output (L-04); it never rewards feature count, code volume or appearance (PEF §12); a known limitation restates no canonical value |
| HANDOFF_FORMAT | the audit marked proposed, with findings P-1 onward (evidence, rating, proposed disposition), put to the human item by item (CLAUDE.md §9A); the known-limitations document with, per row, the gap, why, what would close it, the owner after v1.0, and the record it links to |
| VALIDATION_GATE | `tests/test_agent_contracts.py` (this contract, its writes and its owner rows) |
| FAILURE_BEHAVIOUR | a capability the documentation claims with no artifact behind it is a blocking finding and stops the session for the human's ruling before any document changes (S24 prompt §16); a limit the pages and the document disagree on is reported, never resolved by editing one side alone; a measure that cannot be recounted is left out, never estimated |

## Outside every contract

Files written only on the human's decision, in a session, never by a role on its own (CLAUDE.md §9, class C and
D; D-180). A path here is changed only to apply a recorded decision or verdict.

- `CLAUDE.md`, `MASTER-ARCHITECTURE.md`, `PROJECT-EVALUATION-FRAMEWORK.md`, `SESSION-PROMPT-SPEC.md`,
  `SESSION-ROADMAP.md`, `VERSION-ROADMAP.md`: the constitutional documents;
- `docs/agents/`: the roles and these contracts;
- `data/claims.json`, `data/companies.json`, `data/jurisdictions.json`, `data/technologies.json`,
  `data/components.json`, `data/products.json`, `data/facilities.json`, `data/events.json`, `data/policies.json`,
  `data/relationships.json`, `data/refused_candidates.json`, `data/identity_basis.json`: canonical records, moved
  from staging on the human's recorded verdict (a deterministic migration needs a decision);
- `docs/quality/human-reviews.md`: the human's verdicts, recorded as given.
