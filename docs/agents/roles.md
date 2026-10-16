# Agent roles

**Status:** ACCEPTED (human review of S06, 2026-09-30; D-052, D-010); S19's rulings accepted on 2026-10-14 (D-180 to D-184); the Client Output active from S21 (D-205); the Change Detector active from S21.5 (D-207); the Portfolio Reviewer active from S24 (D-223). **Session:** S06.

The roles are CLAUDE.md §8's; their duties are MA §11's. This file says which roles are
active and where each active role's contract is. It does not restate the duties.

**An agent is a role, not a program.** In v1 a role is played by Claude in a session or by
the human, under a written contract, checked by deterministic tests that CI runs. There is
no orchestrator, dispatcher, queue or autonomous write path (NG-08, D-018 L-01). S19's agent audit found none of
that justified: NG-08 holds for v1.0 (`docs/architecture/agent-audit.md`, D-184).

**Active** means a contract exists in [`contracts.md`](./contracts.md) and the role's work is
checked in CI. The active set is the pipeline S06 to S10 needs:

source → staged claim → verified claim → reviewed claim → record.

This was the human's choice before S06 (H-3).

S11 adds the page: record → walk and trace → generated page → browser QA. Editorial and QA became active
with it (H-5, "Contracts in S11, proposed (Recommended)"; D-107).

S19 audited the roles (`docs/architecture/agent-audit.md`) and the human ruled on 2026-10-14: the Analyst became
active with a contract, for the SQL layer and the metrics S14 to S16 built (D-181); every tracked file has an
owner, checked (D-180); the Verifier was re-scoped (D-182); the other roles were kept, the inactive ones with the
rows below (D-184).

S21 activates the Client Output for the client brief (D-205): it writes the brief's build and page; the Data Auditor
writes the brief's checks.

S21.5 activates the Change Detector for its first task, the dated search for later rules (D-207, superseding D-184's
inactive ruling for this role): it compares an act the Atlas holds with a later text and writes each comparison as a
candidate change in `docs/research/change-detection.md`; the Source Scout searches, the Extractor drafts the records.

S24 activates the Portfolio Reviewer for the portfolio and capability audit (D-223, as D-184 planned): it writes the
audit, its evidence and v1.0's known limitations; the Knowledge Architect keeps the decision log and the audit index,
and the Data Auditor writes the check that the pages' limits agree with the known limitations.

| Role | Status | Mission (MA §11) | Contract | First active |
|---|---|---|---|---|
| Orchestrator | inactive | Decompose and assign tasks, and request human approval; never alter sources or facts | none | none in v1.0: S19 found no runtime justified (NG-08, D-184). The session prompt and the human coordinate |
| Source Scout | active | Discover candidate sources; never assert a fact from a snippet | [contracts.md](./contracts.md#source-scout) | S06 (used since S01 without a contract) |
| Extractor | active | Turn retrieved material into candidate records with provenance | [contracts.md](./contracts.md#extractor) | S06 |
| Verifier | active | Decide whether the evidence supports a claim; downgrade or reject, never invent. Its authority is the re-read of each anchor in the registered bytes and its list of wording that exceeds evidence; when the drafting session verifies, the human's review is the independent check (D-182) | [contracts.md](./contracts.md#verifier) | S06 (the S01 and S05 Verifier passes followed D-015) |
| Change Detector | active | Compare versions and emit candidate changes, never conclusions | [contracts.md](./contracts.md#change-detector) | S21.5 (D-175's dated search for later rules changing the entries and acts the Atlas holds; contract from S21.5, D-207). S07's freshness rule stays a check, the Data Auditor's |
| Knowledge Architect | active | Keep IDs, vocabularies, ownership and one home per fact | [contracts.md](./contracts.md#knowledge-architect) | S06 (the S03 to S05 designs) |
| Data Auditor | active | Check schemas, references, duplicates, dates and missing provenance | [contracts.md](./contracts.md#data-auditor) | S06 |
| Analyst | active | Produce reproducible derived analysis | [contracts.md](./contracts.md#analyst) | S14 (SQL layer), S15 (metrics), S16 (analytical audit); contract from S19 (D-181) |
| Editorial | active | Turn validated material into readable pages, keeping claim boundaries | [contracts.md](./contracts.md#editorial) | S11 (the first page; contract accepted at the S12 opening review, D-107). Before S11 its session work was limited to recording state rows |
| Client Output | active | Produce briefs and exports from validated data; summarise, never alter a record | [contracts.md](./contracts.md#client-output) | S21 (the client brief; contract accepted at S21 H-1, D-205) |
| QA | active | Test rendering, links, accessibility and browser behaviour | [contracts.md](./contracts.md#qa) | S11 (the first UI; contract accepted at the S12 opening review, D-107). Data and code checks stay the Data Auditor's |
| Portfolio Reviewer | active | Judge whether a feature shows a real capability | [contracts.md](./contracts.md#portfolio-reviewer) | S24 (the portfolio and capability audit and v1.0's known limitations; contract accepted at S24 H-1, D-223). Before S24, the human's review at each session (baseline §5, Gate 8), with the milestone audits written by the Knowledge Architect (D-184) |
