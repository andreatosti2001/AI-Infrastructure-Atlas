# Agent contracts

**Status:** ACCEPTED (human review, 2026-09-30; D-052, D-010); the Editorial and QA contracts accepted on
2026-10-02 (D-107). Paths are kept current when a file moves (Editorial, paths only); no role or boundary
changes without a decision.

MA §12 contracts for the roles [`roles.md`](./roles.md) marks active. Each contract has
MA's nine fields, in MA's order.

- **Paths are repository paths.** A role writes only its allowed paths. The session report, kept in the
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
| ALLOWED_WRITES | the session report, outside this repository (the candidate list and the access gaps); `docs/research/search-logs/` for a search log that a research document cites as its method (D-151) |
| FORBIDDEN_WRITES | any file in `data/`; any schema; a claim's `review`; a class assigned without reading the source |
| EVIDENCE_REQUIREMENTS | search results and snippets are discovery aids only, never cited (`source-policy.md` §2, MA §11.2); no circumvention of a refusal (RA-2); declaring an identity to a site is the human's (RA-7) |
| HANDOFF_FORMAT | a report table: URL, proposed class, row served, why it is preferred, access result |
| VALIDATION_GATE | none of its own writes reach data; the Extractor's sources are checked by `tests/test_data_schema.py` and `tests/test_data_integrity.py` |
| FAILURE_BEHAVIOUR | a refused or unreadable source is recorded as an access gap and left unsearched (SP-7, ER-3); never replaced by a secondary summary |

## Extractor

| Field | Value |
|---|---|
| ROLE | Extractor |
| INPUTS | a retrieved source (bytes, access time, hash) or a manual retrieval by the human (RA-4); the claim model and the schemas |
| OUTPUTS | a source record; candidate claims with citations (locator, verbatim anchor, standing, originator for a chain) or input claims with reasoning; all with `evidence_status: unverified` and `review: not_reviewed` |
| ALLOWED_WRITES | `data/sources.json` (new records, registered when retrieved and before any review, while their claims wait in staging: S16.6, D-146; `publisher_entity` per D-065); `data/staging/claims.json` (new claims); `data/staging/companies.json`, `data/staging/jurisdictions.json` (staging entity records, S07, D-055); `data/staging/technologies.json`, `data/staging/components.json`, `data/staging/products.json` (S08, D-077); `data/staging/facilities.json`, `data/staging/events.json` (S09, D-087); `data/staging/relationships.json` (S10, D-098); `data/staging/refused_candidates.json` (S12, D-109) |
| FORBIDDEN_WRITES | `data/claims.json`; a claim's `review`; `evidence_status` other than `unverified`; `verified_on` or a citation's `read`; migrated source values (a change needs a decision, VD-9) |
| EVIDENCE_REQUIREMENTS | every candidate keeps its provenance (MA §11.3); the anchor is copied verbatim; the type follows `claim-model.md` §2 and ER-1 to ER-10; unknowns are explicit states, never null or zero |
| HANDOFF_FORMAT | the records themselves, plus a report list of new IDs for the Verifier |
| VALIDATION_GATE | `tests/test_data_schema.py` (VD-2) and `tests/test_data_integrity.py` (VD-1, VD-3 to VD-13); for entity records, `tests/test_data_entities.py` (V-1, V-4, V-9, V-10, CE-1, ID-1, J-1, S07; CI-1, DEF-1, DEF-2, B-1, PI-1, IO-1, S08; FI-1, HQ-1, FK-1, CAP-1, S09); for events, `tests/test_data_events.py` (EV-1 to EV-4, EI-1, S09); for edges, `tests/test_data_relationships.py` (V-1 to V-10, CE-1, RI-1, PL-1, EP-1, PE-1, RV-1, S10) |
| FAILURE_BEHAVIOUR | a value the source does not give is left as an explicit state; a sentence that cannot be quoted is not cited; the problem is reported, never patched with an inference |

## Verifier

| Field | Value |
|---|---|
| ROLE | Verifier |
| INPUTS | staged claims with `evidence_status: unverified`; the cited sources, re-retrieved or supplied by the human |
| OUTPUTS | per claim: a status (`supported`, `partial`, `context_only`, or `disputed` with the competing claims), `verified_on`, and each citation's `read`; findings for the report |
| ALLOWED_WRITES | `data/staging/claims.json`: only `evidence_status`, `verified_on`, `disputed_with` and each citation's `read`; `data/staging/refused_candidates.json`: only each considered sentence's `read` (D-109); the session report (D-151) |
| FORBIDDEN_WRITES | a claim's `statement`, `claim_type`, citations' anchors or locators (a change is a new claim from the Extractor); a claim's `review`; `data/claims.json`; source records |
| EVIDENCE_REQUIREMENTS | read the whole sentence at each locator and judge whether the statement exceeds it (`claim-model.md` §6); a class is never a verification (ER-10); record the bytes read; re-check anchors when a hash has changed (`source-policy.md` §12) |
| HANDOFF_FORMAT | the updated claims, plus a report table: claim, status, what was read, and any wording that exceeds its evidence |
| VALIDATION_GATE | `tests/test_data_integrity.py` (VD-6, VD-7, VD-11, VD-12) and `tests/test_data_schema.py` (VD-2) |
| FAILURE_BEHAVIOUR | a source that cannot be re-read leaves the claim `unverified` (SP-7); an anchor not found makes it `context_only`; the Verifier never invents replacement evidence (MA §11.4) |

## Knowledge Architect

| Field | Value |
|---|---|
| ROLE | Knowledge Architect |
| INPUTS | the session prompt; the schemas; the taxonomies, the source policy and the claim model; the decision log |
| OUTPUTS | schema and vocabulary changes, each with a decision; one-home rulings; ID formats |
| ALLOWED_WRITES | `schemas/`; `docs/architecture/claim-model.md`; `docs/architecture/company-dataset.md` (S07); `docs/architecture/concept-dataset.md` (S08); `docs/architecture/facility-dataset.md` (S09); `docs/architecture/edge-dataset.md` (S10); `docs/architecture/vertical-slice.md` (S11); `docs/architecture/milestone-audits/` (S12, the audit report); `docs/architecture/decisions.md` (append only) |
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
| ALLOWED_WRITES | `tests/`; `tests/fixtures/`; `tools/` (standard library only, D-026), except the framing and style in `tools/page_template.html` (Editorial); `site/hbm-chain/index.html`, written only by the build step `tools/build_page.py` (S11, D-102) |
| FORBIDDEN_WRITES | any file in `data/`: the Auditor reports, and the Extractor or Verifier fixes; a claim's `review`; a check weakened to make data pass |
| EVIDENCE_REQUIREMENTS | each check is shown to catch a planted fault before it is trusted (deliberate breaks); prose counts are tested or labelled as measured (L-04) |
| HANDOFF_FORMAT | failing test output naming the record and the rule, in the session report |
| VALIDATION_GATE | `tests/test_data_integrity.py`, `tests/test_data_schema.py`, `tests/test_data_entities.py`, `tests/test_freshness.py`, `tests/test_trace.py`, `tests/test_agent_contracts.py`; from S09, `tests/test_data_events.py` and `tests/test_facility_status.py`; from S10, `tests/test_data_relationships.py` and `tests/test_navigate.py`; from S11, `tests/test_page.py` |
| FAILURE_BEHAVIOUR | a failure that cannot be explained stops the session (CLAUDE.md §18); no test is skipped or loosened to get green |

## Editorial

| Field | Value |
|---|---|
| ROLE | Editorial |
| INPUTS | the page as built from canonical records; `docs/architecture/vertical-slice.md` (the composition, the text provenance rule); `claim-model.md` §13 (how claims are displayed); the schema definitions the page's terms render |
| OUTPUTS | the page's framing (prose that states no fact and names no record) and its style; the state rows of the documentation, as each session prompt lists them |
| ALLOWED_WRITES | `tools/page_template.html` (framing and style only); `README.md`, `docs/README.md` and `docs/architecture/baseline.md` (state rows); the session report (D-151) |
| FORBIDDEN_WRITES | any file in `data/`; a claim's `review`; `site/hbm-chain/index.html` (generated, never edited by hand); a name, value, date, count or relation typed into the template; framing that names a record, holds a digit, or says "none" for a missing relationship; the labels and journey specification in `tools/build_page.py` (the Data Auditor's) |
| EVIDENCE_REQUIREMENTS | framing adds no fact (NG-09, `claim-model.md` §13); every value reaches the page through the build from its home (D-105); a missing edge is "no recorded relationship" (RR-7); no "critical", "concentrated", share, rank or score (NG-11) |
| HANDOFF_FORMAT | the template change and the rebuilt page in one commit, with the framing changes listed in the session report |
| VALIDATION_GATE | `tests/test_page.py` (PG-1 every text node has a home, PG-6 framing marked and naming no record, PG-7 rebuild, PG-8 style and contrast) |
| FAILURE_BEHAVIOUR | a sentence that needs a fact becomes a gap on the page or a question to the human, never framing; a failing check is reported, never loosened |

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
