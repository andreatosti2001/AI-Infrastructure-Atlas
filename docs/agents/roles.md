# Agent roles

**Status:** ACCEPTED (human review of S06, 2026-09-30; D-052, D-010). **Session:** S06.

The roles are CLAUDE.md §8's; their duties are MA §11's. This file says which roles are
active and where each active role's contract is. It does not restate the duties.

**An agent is a role, not a program.** In v1 a role is played by Claude in a session or by
the human, under a written contract, checked by deterministic tests that CI runs. There is
no orchestrator, dispatcher, queue or autonomous write path (NG-08, D-018 L-01). S19 decides
whether any of that is ever justified.

**Active** means a contract exists in [`contracts.md`](./contracts.md) and the role's work is
checked in CI. The active set is the pipeline S06 to S10 needs:

source → staged claim → verified claim → reviewed claim → record.

This was the human's choice before S06 (H-3).

S11 adds the page: record → walk and trace → generated page → browser QA. Editorial and QA became active
with it (H-5, "Contracts in S11, proposed (Recommended)"; D-107).

| Role | Status | Mission (MA §11) | Contract | First active |
|---|---|---|---|---|
| Orchestrator | inactive | Decompose and assign tasks, and request human approval; never alter sources or facts | none | S19 decides whether a runtime is justified (NG-08). Until then the session prompt and the human coordinate |
| Source Scout | active | Discover candidate sources; never assert a fact from a snippet | [contracts.md](./contracts.md#source-scout) | S06 (used since S01 without a contract) |
| Extractor | active | Turn retrieved material into candidate records with provenance | [contracts.md](./contracts.md#extractor) | S06 |
| Verifier | active | Decide whether the evidence supports a claim; downgrade or reject, never invent | [contracts.md](./contracts.md#verifier) | S06 (the S01 and S05 Verifier passes followed D-015) |
| Change Detector | inactive | Compare versions and emit candidate changes, never conclusions | none | S07, with `validate-freshness` and the first `time_sensitive` records (claim-model §16) |
| Knowledge Architect | active | Keep IDs, vocabularies, ownership and one home per fact | [contracts.md](./contracts.md#knowledge-architect) | S06 (the S03 to S05 designs) |
| Data Auditor | active | Check schemas, references, duplicates, dates and missing provenance | [contracts.md](./contracts.md#data-auditor) | S06 |
| Analyst | inactive | Produce reproducible derived analysis | none | S14 (SQL layer); S15 (metrics, NG-11) |
| Editorial | active | Turn validated material into readable pages, keeping claim boundaries | [contracts.md](./contracts.md#editorial) | S11 (the first page; contract accepted at the S12 opening review, D-107). Before S11 its session work was limited to recording state rows |
| Client Output | inactive | Produce briefs and exports from validated data | none | S21 (client briefs) |
| QA | active | Test rendering, links, accessibility and browser behaviour | [contracts.md](./contracts.md#qa) | S11 (the first UI; contract accepted at the S12 opening review, D-107). Data and code checks stay the Data Auditor's |
| Portfolio Reviewer | inactive | Judge whether a feature shows a real capability | none | S24 (capability audit). Until then, the human's review at each session (baseline §5, Gate 8) |
