# SESSION-08 Report — Technology, component and product dataset

- **Session:** S08 · **Type:** IMPLEMENTATION, with research · **Milestone:** M2 — Canonical Dataset (second session)
- **Date:** 2026-10-01
- **Prompt:** [`sessions/prompts/S08-PROMPT.md`](../prompts/S08-PROMPT.md) (Part A assembled by
  Claude from the template and confirmed by the human; Part B SPEC §2 detail; H-0 to H-6
  answered before the session).
- **Branch:** `claude/s08-concept-dataset`, created from `main` @ `2c059f6` (the PR #12
  merge, which carries the S07 work and the S08 prompt).
- **Base** (D-018 L-03), as listed at the end of the session:
  - `git branch -a`: `main`, `claude/s07-company-dataset` (merged), `claude/s08-concept-dataset`, and
    their remotes, plus six older `claude/*` remote branches.
  - `git ls-remote`: `main` at `2c059f6`. The six older `claude/*` branches are at
    `26acdf9`, `ace06f0`, `ce5b881`, `d9d0a83`, `11185a6` and `e23965c`, the same commits
    S07 found merged or cherry-picked. `claude/s07-company-dataset` is at `a5032ef`, which PR
    #12 merged.
  - The S08 prompt was on `main` before the session started.

## Mission outcome

**Delivered; partly canonical after the human's review.** The Atlas now models the v1
concepts separately from any company's marketing language:

- **Concepts:** 15 of the 17 concepts mapped to technology or component have a sourced
  working definition, in 16 records. 11 are canonical (7 components, 4 technologies).
  Five technology records stay in staging, because the human did not approve the two
  rulings they rest on.
- **Products:** the first three product records are canonical, each pointing to a
  canonical company as its vendor.
- **Gaps:** two concepts are recorded gaps. Their only definitions are from vendors'
  marketing pages.

| Deliverable | Where | Status |
|---|---|---|
| Concept-dataset design: scope and gaps, concept table and ID rule, working definitions, `broader`, sources and re-retrievals, products, checks | `docs/architecture/concept-dataset.md` | proposed (D-067 to D-077; D-074 accepted) |
| New sources: HIR ch.22, an ECP/Sandia report, a NIST news article, and 4 re-retrievals with changed bytes | `data/sources.json` (`src-039` to `src-045`) | source records |
| Claims: 42 new | 33 canonical (`data/claims.json`), 9 staging (`data/staging/claims.json`) | reviewed |
| Components: AI accelerator, data-centre GPU, AI ASIC, HBM, SME, assembly and packaging tools, accelerated server | `data/components.json` | canonical (7) |
| Technologies: multi-die accelerator, multi-die package, EDA, cloud computing | `data/technologies.json` | canonical (4) |
| Technologies: advanced packaging, 2.5D packaging with an interposer, 3D die stacking, EUV lithography, DUV lithography | `data/staging/technologies.json` | staging, waiting on D-070 and D-076 |
| Products: NVIDIA H100, AWS Trainium2, Micron HBM4 36GB 12H | `data/products.json` | canonical (3) |
| Checks: V-1 and CE-1 extended to `broader`, `instance_of`, `vendor`; CI-1, DEF-1, DEF-2, B-1, PI-1, IO-1 | `tests/test_data_entities.py`, `tests/fixtures/entity_records.json` | in CI |
| Trace reads the new files and prints `vendor`, `instance_of`, `broader` | `tools/trace.py` | in CI |

**Roadmap gate, "Definitions are sourced and do not collapse technically distinct
concepts": met for the canonical records, and reviewed.**

- **Sourced.** Each canonical technology and component has a working definition (an
  `INTERPRETATION`). Its inputs are `ATTRIBUTION` claims from sources whose class the
  definition and identity rows accept, with `originator` standing (V-10, DEF-1).
- **Not collapsed.** No definition claim serves two records, and no concept is in two
  records except a listed split (DEF-2, CI-1).
- **Enforced.** A deliberate break of each rule fails the tests.
- **The two staged pairs.** The EUV/DUV pair and the 2.5D/3D pair are kept apart in their
  records. They are staging only because their source-class rulings and the split are
  open.

**Restated contract:**

- **Mission:** canonical technology and component records for the v1 concepts, each with
  a sourced, non-marketing working definition; a few products with canonical vendors.
- **Non-goals:** Part B §08. No facility, relationship, event or metric record; no
  schema or vocabulary change; nothing canonical without the human's verdict.
- **Plan:** access probe and RA-4; design document; sources and staging claims with a
  Verifier pass; staging records; checks (fail first, breaks); review and promotion;
  decisions, docs, report. The plan held.

**Decisions the human took during the session** (verbatim, from the review questions):

| Question | Answer (verbatim) | Effect |
|---|---|---|
| Batch A (16 technology/component records, 38 claims) | "Accept all (Recommended)" | claims accepted, except those held by an open ruling (below) |
| Batch B (3 products) | "Accept all (Recommended)" | 3 products canonical |
| Which flagged rulings do you approve? | "Trainium2 vendor = Amazon, Trainium2 is an AI ASIC" | D-074 accepted; `claim-atlas-trainium2-ai-asic` accepted. **Not ticked:** "EUV/DUV as two records" (D-070) and "Source class rulings" (D-076). The question said unticked rulings stay open and what rests on them stays staging |
| JEDEC JESD238 has not arrived | "Close them as gaps (Recommended)" | HBM-03 and HBM-04 recorded gaps (D-067) |

**How the partial verdict was applied.**

- **Held: 9 claims.** The 4 claims citing `src-039` (HIR) or `src-041` (NIST news), and the
  5 working definitions that take them as inputs. They stay staging, `not_reviewed`. VD-8
  forbids an accepted claim in staging, so the human's "accept" on them is recorded here
  and nowhere else.
- **Held: 5 records.** The records resting on those claims: advanced packaging, 2.5D
  packaging, 3D die stacking, EUV lithography and DUV lithography.
- **Promoted:** everything else, 33 claims and 14 records.

## Files changed

| File | Change |
|---|---|
| `docs/architecture/concept-dataset.md` | new: the design, with the concept table (§3) and product table (§7) that the tests read |
| `docs/architecture/decisions.md` | D-067 to D-077 appended; D-074 accepted; review notes on D-070 and D-076 |
| `data/sources.json` | 7 new records (`src-039` to `src-045`) |
| `data/claims.json`, `data/staging/claims.json` | 33 canonical and 9 staging claims |
| `data/technologies.json`, `data/components.json`, `data/products.json` and their `data/staging/` copies | new files (H-3) |
| `tests/test_data_entities.py` | `ENTITY_KINDS` extended; V-1 and CE-1 extended; CI-1, DEF-1, DEF-2, B-1, PI-1, IO-1; 9 new tests; the document-reference test covers `concept-dataset.md` |
| `tests/fixtures/entity_records.json` | fictional technologies, components and a product; 14 new planted faults |
| `tools/trace.py` | reads the new files; prints `vendor`, `instance_of` and `broader` and flags them `MISSING` if unresolved |
| `README.md`, `docs/README.md`, `docs/architecture/baseline.md`, `docs/agents/contracts.md` | state rows and paths (Editorial) |
| `sessions/reports/SESSION-08-REPORT.md` | this report |

`tests/test_data_schema.py` and `tests/test_freshness.py` needed no edit: both read
`ENTITY_KINDS`, so VD-2 and F-1 cover the new files automatically.

## Data changed

As measured at the final commit (produced by script, L-04):

| Measure | Count |
|---|---|
| source records | 45 (7 new: `research_report` 2, `government_publication` 1, `company_technical_documentation` 2, `company_marketing` 2; all `automated`) |
| canonical claims | 95: `FACT` 47, `ATTRIBUTION` 23, `DERIVATION` 12, `INTERPRETATION` 12, `IMPLICATION` 1 |
| claims created and accepted in S08 | 33 (`ATTRIBUTION` 18, `INTERPRETATION` 11, `FACT` 4), with 22 citations |
| staging claims | 9 (`ATTRIBUTION` 4, `INTERPRETATION` 5) |
| components | 7 canonical (`constituent` 5, `production_equipment` 2), 0 staging |
| technologies | 4 canonical, 5 staging (`process` 6, `design_approach` 1, `software` 1, `service_model` 1) |
| products | 3 canonical (`hardware` 3), 0 staging |
| concepts recorded / gaps | 15 / 2 (HBM-03, HBM-04) |

**Data model:** no schema change. The entity schema accepted in S03 holds every record.

## Tests run

Python 3.11.15. "Fresh venv" means a virtualenv built from `requirements-test.txt` in the
session scratchpad.

| Command / check | Result |
|---|---|
| Full suite at start | OK (181 tests), as at the S07 final commit merged in `2c059f6`. The start run was not logged separately (Deviation 6) |
| **Fail-first:** suite with the S08 checks written, before any S08 data, decision or record | 190 tests, 50 failures (subtests): the 3 "entity file exists" tests, the S08 gate, CI-1, PI-1/IO-1, the display-name control, and the reference tests for every source, claim, record and decision the design cites. The fixture tests passed: every new planted fault was caught on the fictional world |
| Suite with the staging data written | 11 failures, all for decisions D-067 to D-077 not yet written; then OK |
| **Deliberate breaks**, staging run (15 breaks + control) | 15 caught; control 6b passes as it must |
| **Deliberate breaks**, final run on the promoted data (16 breaks + control) | 16 caught; control 6b passes. Output below |
| `python -m unittest discover -s tests`, final, system Python | OK (190 tests: 181 before, 9 new) |
| The same, final, fresh venv; `pip freeze` sorted vs the pins | installed set = pinned set; OK (190) |
| `python tools/validate_repo.py`, final | `Repository integrity: OK` |
| `python tools/trace.py` on the 14 canonical S08 records | exit 0 each; no `MISSING` |
| CI | not observed at the commit that adds this report (L-08) |

**What the checks cannot see.** Two definitions in different words for one concept pass
DEF-2. A working definition that drifts beyond its inputs passes every check. The concept
table, the Verifier and the human's review are the guard (`concept-dataset.md` §2, §10).

**Side effect in the breaks output.** `test_display_name_does_not_move_a_concept_or_product_id`
runs CI-1 and PI-1 on the real data with every display name changed. So it fails alongside
any break of the real records, as well as the test aimed at the break. This is expected.

Not applicable: browser, accessibility, performance.

## Evidence added/retired

**New sources** (all retrieved automatically on 2026-10-01; texts outside the repository):

| Source | What | Class | Cited by |
|---|---|---|---|
| `src-039` | IEEE EPS Heterogeneous Integration Roadmap 2020, ch.22 | `research_report` (ruling open, D-076) | 3 staging claims |
| `src-040` | ECP Milestone M1 Report, Sandia (SAND2018-6370R) | `research_report` (precedent) | `claim-ecp-hbm-definition` |
| `src-041` | NIST news, "UV Lithography: Taking Extreme Measures" (2011) | `government_publication` (ruling open, D-076) | 1 staging claim |
| `src-042` | NVIDIA Hopper in-depth, re-retrieval of `src-006` | `company_technical_documentation` | H100 identity and process name |
| `src-043` | AWS Trainium2 architecture, re-retrieval of `src-010` | `company_technical_documentation` | Trainium2 identity |
| `src-044` | Micron HBM page, re-retrieval of `src-015` | `company_marketing` | Micron HBM4 identity |
| `src-045` | SK hynix back-end process 4, re-retrieval of `src-013` | `company_marketing` | SK hynix's side of CON-03 |

**Re-retrievals.** On 2026-10-01 these sources returned their registered bytes:
`src-001` to `src-005`, `src-021` and `src-022`. These returned changed bytes: `src-006`,
`src-007`, `src-010`, `src-013`, `src-015` and `src-017`.

- **New records (D-075).** Each changed source that S08 cites got a new record.
- **GH100 anchor.** It was re-checked in `src-042` and is still there.

**Verifier pass.** Every new anchor (42 claims; 22 citations in the canonical ones) was found
verbatim in text extracted from the registered bytes. Whitespace was normalised, and so
was line-break hyphenation in PDFs ("on- demand").

**Access and RA-4:**

- **JEDEC JESD238** (free with registration): requested from the human at the start (RA-4,
  RA-7), not received; closed as a gap by the human.
- **`srcmapt.org`**: an automated challenge page; not circumvented (RA-2).
- **Considered, not registered:** a NIST paper on EUV metrology and a NIST abstract on EUV
  optics.

**Retired:** nothing. The S06 claims citing `src-006`, `src-010`, `src-013` and `src-015`
keep their old records.

**Candidate S10 statements read** (not records): HBM stacks DRAM dies connected by TSVs
(ECP); 2.5D packaging places dies on an interposer (HIR); SME includes tools to assemble
and package chips (CSET).

## Decisions made

All appended to `decisions.md` as `proposed`, except D-074, which the human approved at
the review.

| Decision | Subject | Status |
|---|---|---|
| D-067 | concept scope: 15 of 17 recorded; HBM-03, HBM-04 gaps (H-1) | proposed |
| D-068 | technology and component IDs from the §5 name (CI-1) | proposed |
| D-069 | working definitions are always an `INTERPRETATION` (H-4; DEF-1, DEF-2) | proposed |
| D-070 | SME-03 split into EUV and DUV records | proposed; **not approved at review** |
| D-071 | `broader` assignments, acyclic (B-1) | proposed |
| D-072 | three products, product IDs (PI-1), `instance_of` basis (IO-1) (H-2) | proposed |
| D-073 | GH100 ruling: the H100's process name rests on an H100 sentence | proposed |
| D-074 | Trainium2's vendor is `company-amazon-com` | **accepted** at review |
| D-075 | a re-retrieval with changed bytes is a new source record | proposed |
| D-076 | class rulings: HIR `research_report`, NIST news `government_publication` | proposed; **not approved at review** |
| D-077 | layout, review and `validate-data` for the new kinds (H-3, H-6) | proposed |

**Rejected alternatives** are listed in each decision and in `concept-dataset.md` §11.
The main ones:

- IDs from S01 concept IDs, or from a standard's term;
- one SME-03 record;
- citing a single `ATTRIBUTION` directly as the definition;
- reusing the GH100 claim for the H100;
- rewriting a changed source's hash;
- an ASML product taken from a families page.

## Deviations

1. **SME-03 gives two records** where `entity-taxonomy.md` §5 says one technology record
   (D-070). The taxonomy itself left "whether scanners also get equipment classes" to S08,
   and Part B §06 q2 names EUV vs DUV as a pair to keep apart. The taxonomy was not edited.
   The split is not yet approved, so both records are staging.
2. **Changed bytes became new source records** (D-075). The prompt did not foresee that
   four registered pages would change before S08 cited them again.
3. **The `instance_of` basis lives in a document table** (IO-1), because the schema gives
   `instance_of` no claim field and a schema change was out of scope.
4. **No ASML product**, although H-2 named "an ASML EUV system". The registered page names
   only families.
5. **D-076 narrowed after the review.** The review question named only HIR and the NIST
   news article, so the ECP report's class is recorded as precedent (national-laboratory
   reports, as LBNL's), not as part of the open ruling.
6. **The start-of-session test run was not logged** in this report. The 181-test baseline
   is the S07 final result at the merged base.
7. **Partial promotion.** Both batches were accepted, but two rulings were not, so 9
   accepted claims stay staging as `not_reviewed` (VD-8). The human's acceptance of them
   is recorded only in this report.

## Debt introduced/resolved

**Introduced:**

- 5 technology records and 9 claims in staging, waiting on D-070 and D-076.
- 2 concept gaps (HBM-03, HBM-04) waiting on JEDEC JESD238 or another sufficient source.
- Two source records per changed URL, with the link between them only in the new
  record's title (no schema field).
- The concept and product tables are parsed from a design document: a document is the
  home of the concept-to-record mapping and of the `instance_of` basis.
- Product attributes `not_researched`: H100 `tdp_w` (per-form-factor values, §7);
  Trainium2 and Micron `vendor_process_name` and `tdp_w`.

**Resolved:**

- The GH100 finding inherited from S06 (D-073).
- D-027 (first product records).
- `broader` acyclicity, an `entity-taxonomy.md` §9 handoff (B-1).

## Unresolved issues

- **The human's approval of D-067 to D-077** (D-074 approved). D-070 and D-076 were
  explicitly not approved; how to proceed is the human's call (approve, amend, or find
  other sources for the packaging and lithography definitions).
- **The AWS legal entity** behind `src-010`/`src-043` (`company-dataset.md` §14), for S10.
- **Inherited:** S01's weekly gate; S05 debt (the class table vs the matrix; SRC-023 not
  re-read); the operational roadmap's week-3 checkpoint.

## Process lessons

- **Ask flagged rulings separately, with a stated rule for what an unticked box means.**
  The multi-select made the partial outcome unambiguous. That fulfils S07's lesson "ask
  the scope of an accept all".
- **Write the checks before the data.** With the checks written first, the fail-first run
  showed the new tests failing for the right reason. In S07 the record checks passed
  vacuously on empty files.
- **Re-retrieve before citing, and decide the byte-change rule in the design.** The
  changed hashes would otherwise have surfaced as VD-11 failures after the claims were
  written.
- **Read the sentence.** The H100 process value moved from a die sentence to a product
  sentence only because the whole page was re-read.

## Implications for the next session

S09 — Facility dataset ("Add physical locations and distinguish ownership, operation and
production"):

- **Completed work S09 can build on:**
  - canonical companies, jurisdictions, components, 4 technologies and 3 products;
  - the record checks, which now cover five record kinds;
  - the re-retrieval rule (D-075).
- **For S09:**
  - **Locations.** Facility records point to jurisdictions (S07). Owners and operators
    are linked through S10 edges, never fields (R-5).
  - **Candidates.** Facility sentences found in S07's filings: ASML's Veldhoven campus,
    TSMC's fabs, Micron's and SK hynix's production sites.
  - **Rows.** The `identity:facility` and `attr:facility.*` rows apply, and ER-8 applies
    to announced sites.
  - **New kind.** Extend `ENTITY_KINDS` and the trace when facilities arrive.
- **Open issues:** the human's approvals of the S08 decisions, especially D-070 and
  D-076; the AWS legal entity; S01's weekly gate; S05 debt.
- **Recommended next decision:** the human confirms the concept and product IDs (D-068,
  D-072) before S10, because edges will point to them.
- **Files for S09 to read first:** this report; `concept-dataset.md`; `company-dataset.md`;
  `entity-taxonomy.md` §3.2, §4.2; `source-policy.md` §7 (facility rows), §12; D-022,
  D-031 and D-067 to D-077.

**Next recommended milestone:** S09 — the facility dataset, after the human rules on
D-070 and D-076.

## Addendum — human review outcome (2026-10-01)

The review sheet below was sent before the questions. The human's answers, verbatim:

- Batch A: "Accept all (Recommended)"
- Batch B: "Accept all (Recommended)"
- Rulings approved: "Trainium2 vendor = Amazon, Trainium2 is an AI ASIC"
- JEDEC: "Close them as gaps (Recommended)"

**Applied:**

- 33 claims accepted and promoted, recorded in this report.
- D-074 accepted.
- 9 claims and 5 records held in staging, as the question stated for unticked rulings.
- HBM-03 and HBM-04 recorded as gaps.

## Review sheets

The sheet as sent to the human (headings demoted one level).

### S08 review sheet — concepts and products (42 staging claims, 19 staging records)

For each claim: open the source at the locator, read the whole sentence, and answer **does it say this, and no more?** For each working definition (INTERPRETATION): **does it stay within its inputs, and keep apart the concepts it must?** Verdict per claim: **accept**, **reject**, or **wording too strong**. "Accept all" or "accept all except …" is fine; say which batch it covers.

`python tools/trace.py <record ID>` prints any record with its claims, sources, locators and anchors.

#### Batch A — technologies and components

##### `component-ai-accelerator` — AI accelerator · constituent · concept ACC-01

(its claims are all canonical: S06 claims you accepted at the S07 review; only the record is new)

##### `component-data-centre-gpu` — Data-centre GPU · constituent · concept ACC-02 · broader `component-ai-accelerator`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-cset-gpu-definition` | ATTRIBUTION | CSET's glossary defines graphics processing units (GPUs) as specialized logic chips used most commonly for graphics processing and developing artificial intelligence algorithms. | src-002 (policy_research_brief) · p.66, Appendix B: Glossary, entry 'Graphics processing units (GPUs)' | “Graphics processing units (GPUs) are specialized logic chips used most commonly for graphics processing and developing artificial intelligence algorithms” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-lbnl-gpu-definition` | ATTRIBUTION | LBNL's 2025 update defines a GPU as a type of processor particularly well-suited for parallel processing tasks, often used in AI applications and graphics rendering. | src-021 (research_report) · p.7, glossary, entry 'GPU (Graphics Processing Unit)' | “GPU (Graphics Processing Unit) – A type of processor particularly well-suited for parallel processing tasks, often used in AI applications and graphics rendering” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-data-centre-gpu-working-definition` | INTERPRETATION | For the Atlas, a data-centre GPU is a GPU, a logic chip specialised for parallel processing, that is an AI accelerator: used in data centres primarily for AI training or inference. | — | inputs: `claim-cset-gpu-definition`, `claim-lbnl-gpu-definition`, `claim-atlas-ai-accelerator-working-definition` (canonical)<br>reasoning: CSET and LBNL define the GPU; neither defines a 'data-centre GPU'. The record narrows the GPU to the Atlas's AI accelerator (TQ-01), so the AI-accelerator working definition is an input. No CON conflict applies. | Does the working definition stay within its inputs? |

##### `component-ai-asic` — AI ASIC · constituent · concept ACC-03 · broader `component-ai-accelerator`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-cset-asic-definition` | ATTRIBUTION | CSET's glossary defines application-specific integrated circuits (ASICs) as logic chips with designs specialized for certain applications. | src-002 (policy_research_brief) · p.65, Appendix B: Glossary, entry 'Application-specific integrated circuits (ASICs)' | “Application-specific integrated circuits (ASICs) are logic chips with designs specialized for certain applications” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-lbnl-asic-definition` | ATTRIBUTION | LBNL's 2025 update defines an ASIC as a type of semiconductor designed for a specific application rather than general-purpose use, and says that in data centers ASICs are often used for AI tasks. | src-021 (research_report) · p.6, glossary, entry 'ASIC (Application-Specific Integrated Circuit)' | “ASIC (Application-Specific Integrated Circuit) – A type of semiconductor designed for a specific application rather than general-purpose use. In data centers, ASICs are often used for AI tasks due to their efficiency” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-ai-asic-working-definition` | INTERPRETATION | For the Atlas, an AI ASIC is an application-specific integrated circuit, a logic chip designed for a specific application rather than general-purpose use, whose application is AI training or inference in data centres. | — | inputs: `claim-cset-asic-definition`, `claim-lbnl-asic-definition`, `claim-atlas-ai-accelerator-working-definition` (canonical)<br>reasoning: CSET and LBNL define the ASIC in compatible terms; LBNL adds that ASICs in data centers are often used for AI tasks. The record narrows the ASIC to the Atlas's AI accelerator (TQ-01). No CON conflict applies. | Does the working definition stay within its inputs? |

##### `component-high-bandwidth-memory` — High Bandwidth Memory · constituent · concept HBM-02

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-ecp-hbm-definition` | ATTRIBUTION | An ECP milestone report by Sandia describes HBM as a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with through-silicon vias (TSVs). | src-040 (research_report) · p.5 (printed p.1), §1 'Introduction', second sentence | “HBM is a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with through-silicon vias (TSVs)” | The only non-marketing HBM definition found (a 2018 Sandia report for DOE). It calls HBM a 'stacking technology'; the Atlas records HBM as a component (the stack). |
| `claim-atlas-high-bandwidth-memory-working-definition` | INTERPRETATION | For the Atlas, high Bandwidth Memory (HBM) is a memory component: a stack of DRAM dies, placed vertically and connected directly by through-silicon vias. | — | inputs: `claim-ecp-hbm-definition`<br>reasoning: The ECP report describes HBM as a DRAM stacking technology. The Atlas records HBM as a component (entity-taxonomy §5, HBM-02), so the working definition names the stack the technology produces; the stacking process itself is the 3D die stacking record. Where the stack sits (TQ-02, in-package) is an S10 edge, not part of the definition. | Does the working definition stay within its inputs? |

##### `component-semiconductor-manufacturing-equipment` — Semiconductor manufacturing equipment · production_equipment · concept SME-01

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-cset-sme-definition` | ATTRIBUTION | CSET's glossary says semiconductor manufacturing equipment includes tools used to fabricate, assemble, test, and package chips. | src-002 (policy_research_brief) · p.67, Appendix B: Glossary, entry 'Semiconductor manufacturing equipment' | “Semiconductor manufacturing equipment includes tools used to fabricate, assemble, test, and package chips” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-semiconductor-manufacturing-equipment-working-definition` | INTERPRETATION | For the Atlas, semiconductor manufacturing equipment is the class of tools used to fabricate, assemble, test and package chips. The tools are not built into the chips they make. | — | inputs: `claim-cset-sme-definition`<br>reasoning: CSET's glossary definition, with the use class (production equipment) the taxonomy assigns. No CON conflict applies. | Does the working definition stay within its inputs? |

##### `component-assembly-packaging-and-wafer-level-packaging-tools` — Assembly, packaging and wafer-level packaging tools · production_equipment · concept SME-06 · broader `component-semiconductor-manufacturing-equipment`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-cset-assembly-packaging-tools` | ATTRIBUTION | CSET describes assembly and packaging tools as taking a wafer with completed, unseparated chips and turning it into separate, packaged chips. | src-002 (policy_research_brief) · p.45, section 'Assembly and Packaging', first sentence | “Japan, China, Singapore, the United States, and a number of other countries produce assembly and packaging tools (Figure 22 and Table 15), taking a wafer with completed, unseparated chips and turning it into separate, packaged chips” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-nist-wafer-fab-processes-for-packaging` | ATTRIBUTION | NIST's NAPMP vision paper says many wafer-based fab processes are necessary for advanced packaging. | src-004 (government_publication) · p.5, bullet 'Manufacturing equipment' | “U.S. leadership in microelectronics equipment will be leveraged to implement many wafer-based fab processes necessary for advanced packaging” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-assembly-packaging-and-wafer-level-packaging-tools-working-definition` | INTERPRETATION | For the Atlas, assembly, packaging and wafer-level packaging tools are semiconductor manufacturing equipment that turns a wafer of completed, unseparated chips into separate packaged chips, together with the wafer-based fab tools that advanced packaging needs. | — | inputs: `claim-cset-assembly-packaging-tools`, `claim-nist-wafer-fab-processes-for-packaging`, `claim-cset-sme-definition`<br>reasoning: CSET describes assembly and packaging tools; NIST says advanced packaging needs wafer-based fab processes. Combining the two is the Atlas's step, which the S01 domain map recorded as a derivation (SME-06). This record is equipment; the processes are the packaging technology records. | Combines CSET's tool description with NIST's 'wafer-based fab processes'. Is the combination fair? |

##### `component-accelerated-server` — Accelerated server · constituent · concept DC-05

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-lbnl-server-definition` | ATTRIBUTION | LBNL's 2025 update defines a server as a computer or system providing data, resources, or services to other computers (clients) over a network. | src-021 (research_report) · p.7, glossary, entry 'Server' | “Server – A computer or system providing data, resources, or services to other computers (clients) over a network” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-lbnl-accelerated-servers-category` | ATTRIBUTION | LBNL's 2025 update distinguishes accelerated servers from CPU-driven servers, and describes a shift to accelerated servers for advanced workloads. | src-021 (research_report) · p.16, §3.1.1, the sentence beginning 'This reflects the shift' | “This reflects the shift to accelerated servers for advanced workloads, moving away from CPU-driven compute” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-accelerated-server-working-definition` | INTERPRETATION | For the Atlas, an accelerated server is a server, a computer providing data, resources or services to other computers over a network, that is configured with one or more AI accelerators. | — | inputs: `claim-lbnl-server-definition`, `claim-lbnl-accelerated-servers-category`, `claim-atlas-ai-accelerator-working-definition` (canonical)<br>reasoning: LBNL defines the server and counts accelerated servers apart from CPU-driven ones; it gives no one-sentence definition of 'accelerated server'. The record composes the two with the AI-accelerator working definition. TQ-11: servers stay inside layer 6. | LBNL has no one-sentence definition of 'accelerated server'; composed from its server definition and its category. |

##### `technology-multi-die-accelerator` — Multi-die accelerator · design_approach · concept ACC-05

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-nist-chiplet-definition` | ATTRIBUTION | NIST's NAPMP vision paper says chiplets are small, partially functional semiconductor chips that, when assembled at tight pitch and close to one another, result in a highly functional subsystem. | src-004 (government_publication) · p.7, bullet 'Developing a chiplet ecosystem', the sentence beginning 'Chiplets refer to' | “Chiplets refer to small, partially functional, semiconductor chips that, when assembled at tight pitch and close to one another, result in a highly functional subsystem” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-multi-die-accelerator-working-definition` | INTERPRETATION | For the Atlas, a multi-die accelerator is a design approach in which an AI accelerator, presented as one device, is built from more than one die assembled in one package. The Atlas calls it multi-die; 'chiplet' is used only where a source uses it. | — | inputs: `claim-atlas-ai-accelerator-working-definition` (canonical), `claim-nist-chiplet-definition`, `claim-sia-heterogeneous-integration-definition`, `claim-sk-hynix-chiplet-description`<br>reasoning: CON-03: NIST, SIA/BCG and SK hynix describe chiplets differently. TQ-09 chose the neutral term 'multi-die'. The working definition keeps only what the three share (more than one die forming one functional unit) and applies it to the AI accelerator. Every side is an input; SK hynix's side is company marketing and is preserved as a position, not as a definitional source. | Composed from the AI-accelerator working definition and the three chiplet positions (TQ-09). Does it keep only what the sides share? |
| `claim-sia-heterogeneous-integration-definition` | ATTRIBUTION | SIA/BCG describe heterogeneous integration of chiplets as the process of combining multiple chips and chiplets to match the functionality of a single monolithic system-on-chip. | src-005 (industry_association) · p.21, 'SIDEBAR: Chiplets', the sentence beginning 'Heterogeneous integration of chiplets is' | “Heterogeneous integration of chiplets is the process of combining multiple chips and chiplets to match the functionality of a single monolithic system-on-chip (SoC)” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-sk-hynix-chiplet-description` | ATTRIBUTION | SK hynix describes chiplets as a technology that divides existing logic chips by function and connects them with TSV. | src-045 (company_marketing) · the paragraph after 'Figure 5. Conceptual diagram of a chiplet', the sentence beginning 'As shown in Figure 5' | “As shown in Figure 5, it is a technology that divides existing logic chips by function and connects them with TSV” | Company marketing, kept only as one side of CON-03. It defines nothing on its own (V-10 would reject it alone). |

##### `technology-advanced-packaging` — Advanced packaging · process · concept PKG-03

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-nist-advanced-packaging-scope` | ATTRIBUTION | NIST's NAPMP vision paper ties advanced packaging to integrating multi-component assemblies with large numbers of interconnects, to a degree of integration that blurs the line between chip and package. | src-004 (government_publication) · p.4, 'Opportunities in Advanced Packaging', the sentence beginning 'Advanced packaging and capabilities' | “Advanced packaging and capabilities, such as heterogeneous integration, encompass the need to integrate multi-component-assemblies with large numbers of interconnects to achieve a degree of integration that blurs the line between chip and package” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-hir-2d-architecture-definition` | ATTRIBUTION | The IEEE EPS Heterogeneous Integration Roadmap defines a 2D architecture as two or more active silicon devices placed side by side on a package and interconnected on it, and calls it 2DS when its enhanced interconnect uses an inorganic medium such as a silicon, glass or ceramic interposer or bridge. | src-039 (research_report) · p.4 (chapter page 2), §3 'Converged Nomenclature Framework for 2D & 3D Architectures', item a | “A 2D architecture is defined as an architecture where two or more active silicon devices are placed side-by-side on a package and are interconnected on the package. If the interconnect is “enhanced”, i.e., has higher interconnect density than mainstream organic packages, and is accomplished using an organic medium, the architecture is further sub-categorized as a 2DO (2D Organic) architecture and similarly, if the enhanced architecture uses an inorganic medium (e.g. a silicon/glass/ceramic interposer or bridge) the architecture is further sub-categorized as a 2DS architecture” | Class ruling: IEEE EPS roadmap as research_report (D-076). The definition covers interposers AND bridges; the Atlas's 2.5D record keeps only the interposer case. |
| `claim-hir-3d-architecture-definition` | ATTRIBUTION | The IEEE EPS Heterogeneous Integration Roadmap defines a 3D architecture as two or more active silicon devices stacked and interconnected without the agency of the package. | src-039 (research_report) · p.4 (chapter page 2), §3, item b | “A 3D architecture is defined as an architecture where two or more active silicon devices are stacked and interconnected without the agency of the package” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-advanced-packaging-working-definition` | INTERPRETATION | For the Atlas, advanced packaging is packaging that integrates multiple dies at high interconnect density. In v1 it means two things: 2.5D interposer integration of logic and HBM, and HBM die stacking. | — | inputs: `claim-nist-advanced-packaging-scope`, `claim-sia-advanced-packaging-breadth`, `claim-hir-2d-architecture-definition`, `claim-hir-3d-architecture-definition`<br>reasoning: CON-04: NIST ties the term to high-density integration that blurs chip and package; SIA/BCG say it covers a wide range of technologies. TQ-03 chose the narrow working definition for v1. HIR's 2DS and 3D definitions are the technical anchors of the two v1 cases. The choice is the human's, not a resolution of the dispute; both breadths stay as ATTRIBUTION claims. | TQ-03 as you answered it in S01: narrow. Both breadths stay as ATTRIBUTION claims. |
| `claim-sia-advanced-packaging-breadth` | ATTRIBUTION | SIA/BCG say the term “advanced packaging” covers a wide range of materials and manufacturing technologies. | src-005 (industry_association) · p.21, 'SIDEBAR: Chiplets', first sentence | “The term “advanced packaging” covers a wide range of materials and manufacturing technologies” | Does the sentence say this, and no more? Is the source its originator? |

##### `technology-2-5d-packaging-with-an-interposer` — 2.5D packaging with an interposer · process · concept PKG-04 · broader `technology-advanced-packaging`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-atlas-2-5d-packaging-with-an-interposer-working-definition` | INTERPRETATION | For the Atlas, 2.5D packaging with an interposer is the process of placing two or more active dies side by side on an interposer (silicon, glass or ceramic) that carries the dense interconnect between them, inside one package. | — | inputs: `claim-hir-2d-architecture-definition`, `claim-hir-2x-names-no-technical-basis`<br>reasoning: HIR calls this architecture 2DS and says the '2.x' names have no technical basis. The Atlas keeps the taxonomy's term '2.5D' as its working label (TQ-03), and narrows HIR's 2DS to the interposer case: HIR's 2DS also covers bridges. The naming dispute is recorded; the technical content is HIR's. | Does the working definition stay within its inputs? |
| `claim-hir-2x-names-no-technical-basis` | ATTRIBUTION | The IEEE EPS Heterogeneous Integration Roadmap says the “2.x” names for enhanced 2D architectures do not have any particular technical basis. | src-039 (research_report) · p.4 (chapter page 2), §3, item a, the sentences after the 2DS definition | “Architectures that include enhancements over and above traditional 2D architectures (typically 2 or more die flip-chip attached on a traditional organic package) are variously referred to as 2.x architectures to emphasize their specialness. These nomenclatures do not have any particular technical basis” | HIR says the '2.x' names have no technical basis. The Atlas still uses the taxonomy's '2.5D' as its label. Acceptable? |

##### `technology-3d-die-stacking` — 3D die stacking · process · concept PKG-05 · broader `technology-advanced-packaging`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-atlas-3d-die-stacking-working-definition` | INTERPRETATION | For the Atlas, 3D die stacking is the process of stacking two or more active dies and interconnecting them directly, not through the package. In v1 it covers HBM stacking only. | — | inputs: `claim-hir-3d-architecture-definition`, `claim-ecp-hbm-definition`<br>reasoning: HIR's 3D architecture gives the definition; the ECP report gives HBM as a case (DRAM dies stacked and connected by TSVs). The v1 scope (HBM only) is the taxonomy's (entity-taxonomy §5, PKG-05). | Does the working definition stay within its inputs? |

##### `technology-multi-die-package` — Multi-die package · process · concept PKG-06

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-atlas-multi-die-package-working-definition` | INTERPRETATION | For the Atlas, a multi-die package is the packaging of two or more dies in one package so that they work as one functional subsystem. The Atlas calls it multi-die; 'chiplet' is used only where a source uses it. | — | inputs: `claim-nist-chiplet-definition`, `claim-sia-heterogeneous-integration-definition`, `claim-sk-hynix-chiplet-description`<br>reasoning: CON-03 and TQ-09, as for the multi-die accelerator. This record is the packaging process; the multi-die accelerator is the design approach. Every side is an input. | Does the working definition stay within its inputs? |

##### `technology-euv-lithography` — EUV lithography · process · concept SME-03

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-nist-euv-duv-wavelengths` | ATTRIBUTION | NIST wrote in 2011 that the smallest features were typically made with deep ultraviolet light at 193 nm, and that lithography was shifting to extreme ultraviolet (EUV) at 13.5 nm. | src-041 (government_publication) · article body, the paragraph beginning 'In general, feature size is proportional to the wavelength' | “Today's super-small features are typically made with "deep" ultraviolet light at 193 nm. "But now we're trying to make a dramatic shift by dropping more than an order of magnitude, down to extreme ultraviolet (EUV) at 13.5 nm,"” | Class ruling: a NIST news article as government_publication (D-076). Written in 2011 ('Today's…'); only the wavelengths are used. |
| `claim-cset-photolithography-grades` | ATTRIBUTION | CSET lists EUV and deep ultraviolet (DUV) as separate grades of photolithography tool, DUV including ArF immersion, ArF and KrF. | src-002 (policy_research_brief) · p.32, section on lithography tools, the sentence beginning 'Photolithography tools are used in high-volume chip production' | “Photolithography tools are used in high-volume chip production, and currently include six grades from most to least advanced by supported nodes: EUV, deep ultraviolet (DUV)—which includes ArF immersion (also called wet ArF or ArFi), ArF (also called dry ArF), and krypton fluoride (KrF)—i-line, and mask aligners” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-euv-lithography-working-definition` | INTERPRETATION | For the Atlas, eUV lithography is photolithography that patterns chips with extreme ultraviolet light at a wavelength of 13.5 nm. It is a different grade of lithography from DUV. | — | inputs: `claim-nist-euv-duv-wavelengths`, `claim-cset-photolithography-grades`<br>reasoning: NIST gives the wavelength; CSET lists EUV and DUV as separate grades. SME-03 is split into two records (D-070) so that the two processes are not merged. No vendor source is used. | SME-03 split into two records (D-070). Agree that EUV and DUV are two records? |

##### `technology-duv-lithography` — DUV lithography · process · concept SME-03

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-atlas-duv-lithography-working-definition` | INTERPRETATION | For the Atlas, dUV lithography is photolithography that patterns chips with deep ultraviolet light, typically at 193 nm. CSET's DUV grade includes ArF immersion, ArF and KrF tools. | — | inputs: `claim-nist-euv-duv-wavelengths`, `claim-cset-photolithography-grades`<br>reasoning: As for EUV lithography. 'Typically at 193 nm' is NIST's wording; KrF tools use another wavelength, which no retrieved source states, so the definition does not give one. | Does the working definition stay within its inputs? |

##### `technology-electronic-design-automation` — Electronic design automation · software · concept EDA-01

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-cset-eda-definition` | ATTRIBUTION | CSET's glossary says electronic design automation (EDA) software is used to design chips. | src-002 (policy_research_brief) · p.66, Appendix B: Glossary, entry 'Electronic design automation (EDA)' | “Electronic design automation (EDA) software is used to design chips” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-electronic-design-automation-working-definition` | INTERPRETATION | For the Atlas, electronic design automation (EDA) is the class of software used to design chips. A vendor's EDA tool is a product, not this record. | — | inputs: `claim-cset-eda-definition`<br>reasoning: CSET's glossary definition. Synopsys's broader description (software and hardware tools, SRC-018) is company marketing and is not used to define the class. | Does the working definition stay within its inputs? |

##### `technology-cloud-computing` — Cloud computing · service_model · concept DC-02

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-nist-cloud-computing-definition` | ATTRIBUTION | NIST SP 800-145 defines cloud computing as a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort or service provider interaction. | src-001 (government_publication) · p.6, §2 'The NIST Definition of Cloud Computing', first sentence | “Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction” | Does the sentence say this, and no more? Is the source its originator? |
| `claim-atlas-cloud-computing-working-definition` | INTERPRETATION | For the Atlas, cloud computing is a service model: on-demand network access to a shared pool of configurable computing resources, rapidly provisioned and released with minimal management effort, as NIST defines it. A provider's cloud service is a product, not this record. | — | inputs: `claim-nist-cloud-computing-definition`<br>reasoning: NIST SP 800-145's definition, unchanged in substance. No CON conflict applies. | Does the working definition stay within its inputs? |

#### Batch B — products

##### `product-nvidia-h100-tensor-core-gpu` — NVIDIA H100 · vendor `company-nvidia` · instance_of `component-data-centre-gpu`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-h100-identity` | FACT | The NVIDIA H100 Tensor Core GPU is a data center GPU that NVIDIA offers for large-scale AI and HPC. | src-042 (company_technical_documentation) · section 'Introducing the NVIDIA H100 Tensor Core GPU', first sentence | “The NVIDIA H100 Tensor Core GPU is our ninth-generation data center GPU designed to deliver an order-of-magnitude performance leap for large-scale AI and HPC” | Does the vendor's sentence say this about this product? |
| `claim-h100-process-name` | FACT | NVIDIA names the fabrication process of the H100 “TSMC 4N”. | src-042 (company_technical_documentation) · after the GH100 specification list, the sentence beginning 'Using the TSMC 4N fabrication process' | “Using the TSMC 4N fabrication process enables H100 to increase GPU core frequency” | The GH100 ruling (D-073): this sentence is about the H100 itself, so the H100 value 'TSMC 4N' rests on it, not on the GH100 die claim. |

##### `product-amazon-com-trainium2` — AWS Trainium2 · vendor `company-amazon-com` · instance_of `component-ai-asic`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-trainium2-identity` | FACT | Trainium2 is a machine learning chip that AWS offers, its third generation of purpose-built machine learning chip. | src-043 (company_technical_documentation) · heading 'Trainium2 Architecture', first sentence | “Trainium2 is the third generation, purpose-built Machine Learning chip from AWS” | Vendor ruling (D-074): 'from AWS' -> company-amazon-com, whose accepted aliases include AWS. Asked separately. |

##### `product-micron-technology-hbm4-36gb-12h` — Micron HBM4 36GB 12H · vendor `company-micron-technology` · instance_of `component-high-bandwidth-memory`

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-micron-hbm4-identity` | FACT | Micron names an HBM4 product “HBM4 36GB 12H” and states that it is in high-volume production. | src-044 (company_marketing) · section 'Micron HBM4 in high-volume production', first sentence | “Micron is in high-volume production of HBM4 36GB 12H” | Identity only; 'in high-volume production' is not used for any field. |

#### Other staging claims

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-atlas-trainium2-ai-asic` | INTERPRETATION | For the Atlas, AWS Trainium2 is an AI ASIC: AWS describes it as a purpose-built machine learning chip, which is a chip designed for a specific application. | — | inputs: `claim-trainium2-identity`, `claim-cset-asic-definition`, `claim-lbnl-asic-definition`, `claim-atlas-ai-asic-working-definition`<br>reasoning: AWS's sentence does not use the word ASIC. 'Purpose-built' for machine learning matches CSET's and LBNL's ASIC definitions (a design specialised for an application rather than general-purpose use). The step from the vendor's words to the class is the Atlas's, so it is an INTERPRETATION, flagged for the human. | AWS never says 'ASIC'. Is 'purpose-built Machine Learning chip' enough to file Trainium2 under AI ASIC? Asked separately. |

#### Not on this sheet

- `component-ai-accelerator` rests on S06 claims you accepted at the S07 review; only its record is new.
- Gaps: HBM base die (HBM-03) and through-silicon via (HBM-04) have no record (no non-marketing definition; JEDEC JESD238 not received).
- No ASML product: its page names only product families.

## Fail-first output

Sorted counts of the failing tests, before any S08 data, decision or record existed:

```
      1 FAIL: test_ci1_concept_table_matches_taxonomy_schema_and_records (test_data_entities)
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-067')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-068')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-069')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-070')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-071')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-072')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-073')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-074')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-075')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-076')
      1 FAIL: test_cited_decisions_exist (test_data_entities) (decision='D-077')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='claim-atlas-trainium2-ai-asic')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='claim-h100-identity')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='claim-h100-process-name')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='claim-micron-hbm4-identity')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='component-accelerated-server')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='component-ai-accelerator')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='component-ai-asic')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='component-assembly-packaging-and-wafer-level-packaging-tools')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='component-data-centre-gpu')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='component-high-bandwidth-memory')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='component-semiconductor-manufacturing-equipment')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='product-amazon-com-trainium2')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='product-micron-technology-hbm4-36gb-12h')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='product-nvidia-h100-tensor-core-gpu')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='src-039')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='src-040')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='src-041')
      2 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='src-042')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='src-043')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='src-044')
      2 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='src-045')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-2-5d-packaging-with-an-interposer')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-3d-die-stacking')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-advanced-packaging')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-cloud-computing')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-duv-lithography')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-electronic-design-automation')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-euv-lithography')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-multi-die-accelerator')
      1 FAIL: test_cited_sources_claims_and_records_exist (test_data_entities) (ref='technology-multi-die-package')
      1 FAIL: test_display_name_does_not_move_a_concept_or_product_id (test_data_entities)
      1 FAIL: test_entity_files_exist (test_data_entities) (kind='components')
      1 FAIL: test_entity_files_exist (test_data_entities) (kind='products')
      1 FAIL: test_entity_files_exist (test_data_entities) (kind='technologies')
      1 FAIL: test_pi1_io1_product_ids_and_instance_of_basis (test_data_entities)
      1 FAIL: test_s08_gate_concept_records_exist (test_data_entities)
      1 FAILED (failures=50)
      1 Ran 190 tests in 1.701s
```

## Deliberate breaks, final run

Run on the promoted data; each break edits a scratch copy and lists the tests that fail.

### 1 a definition resting only on marketing (the HBM source reclassed as company_marketing): caught
   - test_data_entities.EntityDataTests.test_v10_fields_rest_on_allowed_classes_and_standing

### 2 two records with one definition (DUV cites the EUV working definition): caught
   - test_data_entities.EntityDataTests.test_def2_no_concept_or_definition_in_two_records

### 3 a broader cycle (AI accelerator under data-centre GPU): caught
   - test_data_entities.EntityDataTests.test_b1_broader_is_acyclic

### 4 a product whose vendor is missing: caught
   - test_data_entities.EntityDataTests.test_ce1_canonical_records_rest_on_canonical_claims
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_concept_or_product_id
   - test_data_entities.EntityDataTests.test_pi1_io1_product_ids_and_instance_of_basis
   - test_data_entities.EntityDataTests.test_v1_references_resolve

### 5 a product attribute without a claim (tdp_w = 700, no claim): caught
   - test_data_entities.EntityDataTests.test_v10_fields_rest_on_allowed_classes_and_standing
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid

### 6 an ID that changes with a display name (H100 ID rebuilt from its display name): caught
   - test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_concept_or_product_id
   - test_data_entities.EntityDataTests.test_pi1_io1_product_ids_and_instance_of_basis

### 6b the display name changed under the real rule (must NOT fail): passes, as it must

### 7 a product instance_of pointing to a missing class (the HBM base die gap): caught
   - test_data_entities.EntityDataTests.test_ce1_canonical_records_rest_on_canonical_claims
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_concept_or_product_id
   - test_data_entities.EntityDataTests.test_pi1_io1_product_ids_and_instance_of_basis
   - test_data_entities.EntityDataTests.test_v1_references_resolve

### 8 one concept in two records (multi-die package claims ACC-05): caught
   - test_data_entities.EntityDataTests.test_ci1_concept_table_matches_taxonomy_schema_and_records
   - test_data_entities.EntityDataTests.test_def2_no_concept_or_definition_in_two_records
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_concept_or_product_id

### 9 a source's ATTRIBUTION used directly as the definition: caught
   - test_data_entities.EntityDataTests.test_def1_definitions_are_working_definitions

### 10 a record for a gap concept (HBM base die defined from Micron's page): caught
   - test_data_entities.EntityDataTests.test_ci1_concept_table_matches_taxonomy_schema_and_records
   - test_data_entities.EntityDataTests.test_def1_definitions_are_working_definitions
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_concept_or_product_id
   - test_data_entities.EntityDataTests.test_v10_fields_rest_on_allowed_classes_and_standing

### 11 a new claim read from changed bytes but citing the old source record: caught
   - test_data_integrity.IntegrityTests.test_vd11_anchors_are_verbatim_in_their_home

### 12 a technology kind that does not serve its concept (EUV as software): caught
   - test_data_entities.EntityDataTests.test_ci1_concept_table_matches_taxonomy_schema_and_records
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_concept_or_product_id

### 13 an instance_of value with no basis row (Micron HBM4 also an AI accelerator): caught
   - test_data_entities.RuleSourceTests.test_display_name_does_not_move_a_concept_or_product_id
   - test_data_entities.EntityDataTests.test_pi1_io1_product_ids_and_instance_of_basis

### 14 a broader parent of the wrong type (2.5D packaging under a component): caught
   - test_data_entities.EntityDataTests.test_v1_references_resolve
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid

### 15 an identity claim that is not an input of the working definition (NIST cloud identity on EDA): caught
   - test_data_entities.EntityDataTests.test_def1_definitions_are_working_definitions

### 16 a held record promoted without the human's verdict (3D die stacking moved to canonical): caught
   - test_data_entities.EntityDataTests.test_ce1_canonical_records_rest_on_canonical_claims

## Traces of the canonical S08 records

`python tools/trace.py <ID>` for each of the 14 canonical records, at the final commit.

```
component-ai-accelerator · component record · canonical components.json
  AI accelerator
  /identity_claim_ids:
    claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: CSET's definition of “AI chips” includes GPUs, FPGAs and certain types of ASICs.
      as of: not_stated
      citation 1 · src-003 · standing originator
        source: "AI Chips: What They Are and Why They Matter (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf
        class: policy_research_brief · publisher record: not_applicable
        stated dates: published 2020-04
        registered: automated 2026-09-29T13:25Z sha256 0f80b4fa1650 · migrated from SRC-003
        locator: p.4, footnote *
        anchor: "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"
        read by the Verifier: 2026-09-30T21:29Z sha256 0f80b4fa1650 (same bytes as registered)
  /identity_claim_ids:
    claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: LBNL's 2025 update says that the dataset of its 2024 report covered GPU accelerators only, and that the update “expands the accounting to all AI accelerators, namely ASICs”.
      as of: not_stated
      citation 1 · src-021 · standing originator
        source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
        class: research_report · publisher record: not_applicable
        stated dates: published 2026-06-18
        registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
        locator: p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report'
        anchor: "this update expands the accounting to all AI accelerators, namely ASICs"
        read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
  /definition/0/claim_ids: An AI accelerator is a data-centre logic chip, a GPU or an AI ASIC, whose primary purpose is AI training or inference. FPGAs and CPUs are outside v1 scope.
    claim-atlas-ai-accelerator-working-definition · INTERPRETATION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: For the Atlas, an AI accelerator is a data-centre logic chip, a GPU or an AI ASIC, whose primary purpose is AI training or inference. FPGAs and CPUs are outside v1 scope.
      reasoning: CON-01 is a definitional conflict (source-policy.md §10.2): CSET's definition includes FPGAs; LBNL's accounting covers GPUs and ASICs. The working definition is a choice, not a resolution. The human chose it at TQ-01 (domain-map.md §7.1, D-016). Both source positions stay as ATTRIBUTION claims.
      input:
        claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          (shown above)
      input:
        claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          (shown above)
exit 0

component-data-centre-gpu · component record · canonical components.json
  Data-centre GPU
  /broader: component-ai-accelerator · AI accelerator · canonical components.json
  /identity_claim_ids:
    claim-cset-gpu-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: CSET's glossary defines graphics processing units (GPUs) as specialized logic chips used most commonly for graphics processing and developing artificial intelligence algorithms.
      as of: not_stated
      citation 1 · src-002 · standing originator
        source: "The Semiconductor Supply Chain: Assessing National Competitiveness (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief-1.pdf
        class: policy_research_brief · publisher record: not_applicable
        stated dates: published 2021-01
        registered: automated 2026-09-29T13:25Z sha256 319d942ba534 · migrated from SRC-002
        locator: p.66, Appendix B: Glossary, entry 'Graphics processing units (GPUs)'
        anchor: "Graphics processing units (GPUs) are specialized logic chips used most commonly for graphics processing and developing artificial intelligence algorithms"
        read by the Verifier: 2026-10-01T20:44Z sha256 319d942ba534 (same bytes as registered)
  /identity_claim_ids:
    claim-lbnl-gpu-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: LBNL's 2025 update defines a GPU as a type of processor particularly well-suited for parallel processing tasks, often used in AI applications and graphics rendering.
      as of: not_stated
      citation 1 · src-021 · standing originator
        source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
        class: research_report · publisher record: not_applicable
        stated dates: published 2026-06-18
        registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
        locator: p.7, glossary, entry 'GPU (Graphics Processing Unit)'
        anchor: "GPU (Graphics Processing Unit) – A type of processor particularly well-suited for parallel processing tasks, often used in AI applications and graphics rendering"
        read by the Verifier: 2026-10-01T20:44Z sha256 1108b5a0f829 (same bytes as registered)
  /definition/0/claim_ids: A data-centre GPU is a GPU, a logic chip specialised for parallel processing, that is an AI accelerator: used in data centres primarily for AI training or inference.
    claim-atlas-data-centre-gpu-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, a data-centre GPU is a GPU, a logic chip specialised for parallel processing, that is an AI accelerator: used in data centres primarily for AI training or inference.
      reasoning: CSET and LBNL define the GPU; neither defines a 'data-centre GPU'. The record narrows the GPU to the Atlas's AI accelerator (TQ-01), so the AI-accelerator working definition is an input. No CON conflict applies.
      input:
        claim-cset-gpu-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-lbnl-gpu-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-atlas-ai-accelerator-working-definition · INTERPRETATION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: For the Atlas, an AI accelerator is a data-centre logic chip, a GPU or an AI ASIC, whose primary purpose is AI training or inference. FPGAs and CPUs are outside v1 scope.
          reasoning: CON-01 is a definitional conflict (source-policy.md §10.2): CSET's definition includes FPGAs; LBNL's accounting covers GPUs and ASICs. The working definition is a choice, not a resolution. The human chose it at TQ-01 (domain-map.md §7.1, D-016). Both source positions stay as ATTRIBUTION claims.
          input:
            claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: CSET's definition of “AI chips” includes GPUs, FPGAs and certain types of ASICs.
              as of: not_stated
              citation 1 · src-003 · standing originator
                source: "AI Chips: What They Are and Why They Matter (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf
                class: policy_research_brief · publisher record: not_applicable
                stated dates: published 2020-04
                registered: automated 2026-09-29T13:25Z sha256 0f80b4fa1650 · migrated from SRC-003
                locator: p.4, footnote *
                anchor: "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"
                read by the Verifier: 2026-09-30T21:29Z sha256 0f80b4fa1650 (same bytes as registered)
          input:
            claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: LBNL's 2025 update says that the dataset of its 2024 report covered GPU accelerators only, and that the update “expands the accounting to all AI accelerators, namely ASICs”.
              as of: not_stated
              citation 1 · src-021 · standing originator
                source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
                class: research_report · publisher record: not_applicable
                stated dates: published 2026-06-18
                registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
                locator: p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report'
                anchor: "this update expands the accounting to all AI accelerators, namely ASICs"
                read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
exit 0

component-ai-asic · component record · canonical components.json
  AI ASIC
  /broader: component-ai-accelerator · AI accelerator · canonical components.json
  /identity_claim_ids:
    claim-cset-asic-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: CSET's glossary defines application-specific integrated circuits (ASICs) as logic chips with designs specialized for certain applications.
      as of: not_stated
      citation 1 · src-002 · standing originator
        source: "The Semiconductor Supply Chain: Assessing National Competitiveness (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief-1.pdf
        class: policy_research_brief · publisher record: not_applicable
        stated dates: published 2021-01
        registered: automated 2026-09-29T13:25Z sha256 319d942ba534 · migrated from SRC-002
        locator: p.65, Appendix B: Glossary, entry 'Application-specific integrated circuits (ASICs)'
        anchor: "Application-specific integrated circuits (ASICs) are logic chips with designs specialized for certain applications"
        read by the Verifier: 2026-10-01T20:44Z sha256 319d942ba534 (same bytes as registered)
  /identity_claim_ids:
    claim-lbnl-asic-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: LBNL's 2025 update defines an ASIC as a type of semiconductor designed for a specific application rather than general-purpose use, and says that in data centers ASICs are often used for AI tasks.
      as of: not_stated
      citation 1 · src-021 · standing originator
        source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
        class: research_report · publisher record: not_applicable
        stated dates: published 2026-06-18
        registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
        locator: p.6, glossary, entry 'ASIC (Application-Specific Integrated Circuit)'
        anchor: "ASIC (Application-Specific Integrated Circuit) – A type of semiconductor designed for a specific application rather than general-purpose use. In data centers, ASICs are often used for AI tasks due to their efficiency"
        read by the Verifier: 2026-10-01T20:44Z sha256 1108b5a0f829 (same bytes as registered)
  /definition/0/claim_ids: An AI ASIC is an application-specific integrated circuit, a logic chip designed for a specific application rather than general-purpose use, whose application is AI training or inference in data centres.
    claim-atlas-ai-asic-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, an AI ASIC is an application-specific integrated circuit, a logic chip designed for a specific application rather than general-purpose use, whose application is AI training or inference in data centres.
      reasoning: CSET and LBNL define the ASIC in compatible terms; LBNL adds that ASICs in data centers are often used for AI tasks. The record narrows the ASIC to the Atlas's AI accelerator (TQ-01). No CON conflict applies.
      input:
        claim-cset-asic-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-lbnl-asic-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-atlas-ai-accelerator-working-definition · INTERPRETATION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: For the Atlas, an AI accelerator is a data-centre logic chip, a GPU or an AI ASIC, whose primary purpose is AI training or inference. FPGAs and CPUs are outside v1 scope.
          reasoning: CON-01 is a definitional conflict (source-policy.md §10.2): CSET's definition includes FPGAs; LBNL's accounting covers GPUs and ASICs. The working definition is a choice, not a resolution. The human chose it at TQ-01 (domain-map.md §7.1, D-016). Both source positions stay as ATTRIBUTION claims.
          input:
            claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: CSET's definition of “AI chips” includes GPUs, FPGAs and certain types of ASICs.
              as of: not_stated
              citation 1 · src-003 · standing originator
                source: "AI Chips: What They Are and Why They Matter (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf
                class: policy_research_brief · publisher record: not_applicable
                stated dates: published 2020-04
                registered: automated 2026-09-29T13:25Z sha256 0f80b4fa1650 · migrated from SRC-003
                locator: p.4, footnote *
                anchor: "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"
                read by the Verifier: 2026-09-30T21:29Z sha256 0f80b4fa1650 (same bytes as registered)
          input:
            claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: LBNL's 2025 update says that the dataset of its 2024 report covered GPU accelerators only, and that the update “expands the accounting to all AI accelerators, namely ASICs”.
              as of: not_stated
              citation 1 · src-021 · standing originator
                source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
                class: research_report · publisher record: not_applicable
                stated dates: published 2026-06-18
                registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
                locator: p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report'
                anchor: "this update expands the accounting to all AI accelerators, namely ASICs"
                read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
exit 0

component-high-bandwidth-memory · component record · canonical components.json
  High Bandwidth Memory
  /identity_claim_ids:
    claim-ecp-hbm-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: An ECP milestone report by Sandia describes HBM as a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with through-silicon vias (TSVs).
      as of: not_stated
      citation 1 · src-040 · standing originator
        source: "Milestone M1 Report: HBM2/3 Evaluation on Many-core CPU (ECP Milestone ECP-MT-1000; SAND2018-6370R)" · Sandia National Laboratories, for the DOE Exascale Computing Project (ECP), via OSTI · https://www.osti.gov/servlets/purl/1455354/
        class: research_report · publisher record: not_applicable
        stated dates: published 2018-06-08
        registered: automated 2026-10-01T20:51Z sha256 8a9e0dd19680df611754313dade196f95ca80c945fa3e0dc011c1c63801e8be8
        locator: p.5 (printed p.1), §1 'Introduction', second sentence
        anchor: "HBM is a DRAM stacking technology that vertically stacks multiple DRAM dies and directly connects them with through-silicon vias (TSVs)"
        read by the Verifier: 2026-10-01T20:51Z sha256 8a9e0dd19680 (same bytes as registered)
  /definition/0/claim_ids: High Bandwidth Memory (HBM) is a memory component: a stack of DRAM dies, placed vertically and connected directly by through-silicon vias.
    claim-atlas-high-bandwidth-memory-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, high Bandwidth Memory (HBM) is a memory component: a stack of DRAM dies, placed vertically and connected directly by through-silicon vias.
      reasoning: The ECP report describes HBM as a DRAM stacking technology. The Atlas records HBM as a component (entity-taxonomy §5, HBM-02), so the working definition names the stack the technology produces; the stacking process itself is the 3D die stacking record. Where the stack sits (TQ-02, in-package) is an S10 edge, not part of the definition.
      input:
        claim-ecp-hbm-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
exit 0

component-semiconductor-manufacturing-equipment · component record · canonical components.json
  Semiconductor manufacturing equipment
  /identity_claim_ids:
    claim-cset-sme-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: CSET's glossary says semiconductor manufacturing equipment includes tools used to fabricate, assemble, test, and package chips.
      as of: not_stated
      citation 1 · src-002 · standing originator
        source: "The Semiconductor Supply Chain: Assessing National Competitiveness (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief-1.pdf
        class: policy_research_brief · publisher record: not_applicable
        stated dates: published 2021-01
        registered: automated 2026-09-29T13:25Z sha256 319d942ba534 · migrated from SRC-002
        locator: p.67, Appendix B: Glossary, entry 'Semiconductor manufacturing equipment'
        anchor: "Semiconductor manufacturing equipment includes tools used to fabricate, assemble, test, and package chips"
        read by the Verifier: 2026-10-01T20:44Z sha256 319d942ba534 (same bytes as registered)
  /definition/0/claim_ids: Semiconductor manufacturing equipment is the class of tools used to fabricate, assemble, test and package chips. The tools are not built into the chips they make.
    claim-atlas-semiconductor-manufacturing-equipment-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, semiconductor manufacturing equipment is the class of tools used to fabricate, assemble, test and package chips. The tools are not built into the chips they make.
      reasoning: CSET's glossary definition, with the use class (production equipment) the taxonomy assigns. No CON conflict applies.
      input:
        claim-cset-sme-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
exit 0

component-assembly-packaging-and-wafer-level-packaging-tools · component record · canonical components.json
  Assembly, packaging and wafer-level packaging tools
  /broader: component-semiconductor-manufacturing-equipment · Semiconductor manufacturing equipment · canonical components.json
  /identity_claim_ids:
    claim-cset-assembly-packaging-tools · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: CSET describes assembly and packaging tools as taking a wafer with completed, unseparated chips and turning it into separate, packaged chips.
      as of: not_stated
      citation 1 · src-002 · standing originator
        source: "The Semiconductor Supply Chain: Assessing National Competitiveness (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief-1.pdf
        class: policy_research_brief · publisher record: not_applicable
        stated dates: published 2021-01
        registered: automated 2026-09-29T13:25Z sha256 319d942ba534 · migrated from SRC-002
        locator: p.45, section 'Assembly and Packaging', first sentence
        anchor: "Japan, China, Singapore, the United States, and a number of other countries produce assembly and packaging tools (Figure 22 and Table 15), taking a wafer with completed, unseparated chips and turning it into separate, packaged chips"
        read by the Verifier: 2026-10-01T20:44Z sha256 319d942ba534 (same bytes as registered)
  /identity_claim_ids:
    claim-nist-wafer-fab-processes-for-packaging · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: NIST's NAPMP vision paper says many wafer-based fab processes are necessary for advanced packaging.
      as of: not_stated
      citation 1 · src-004 · standing originator
        source: "The Vision for the National Advanced Packaging Manufacturing Program" · NIST · https://www.nist.gov/system/files/documents/2023/11/19/NAPMP-Vision-Paper-20231120.pdf
        class: government_publication · publisher record: not_applicable
        stated dates: published 2023-11-20
        registered: automated 2026-09-29T13:26Z sha256 bb83ae40b640 · migrated from SRC-004
        locator: p.5, bullet 'Manufacturing equipment'
        anchor: "U.S. leadership in microelectronics equipment will be leveraged to implement many wafer-based fab processes necessary for advanced packaging"
        read by the Verifier: 2026-10-01T20:44Z sha256 bb83ae40b640 (same bytes as registered)
  /definition/0/claim_ids: Assembly, packaging and wafer-level packaging tools are semiconductor manufacturing equipment that turns a wafer of completed, unseparated chips into separate packaged chips, together with the wafer-based fab tools that advanced packaging needs.
    claim-atlas-assembly-packaging-and-wafer-level-packaging-tools-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, assembly, packaging and wafer-level packaging tools are semiconductor manufacturing equipment that turns a wafer of completed, unseparated chips into separate packaged chips, together with the wafer-based fab tools that advanced packaging needs.
      reasoning: CSET describes assembly and packaging tools; NIST says advanced packaging needs wafer-based fab processes. Combining the two is the Atlas's step, which the S01 domain map recorded as a derivation (SME-06). This record is equipment; the processes are the packaging technology records.
      input:
        claim-cset-assembly-packaging-tools · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-nist-wafer-fab-processes-for-packaging · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-cset-sme-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          statement: CSET's glossary says semiconductor manufacturing equipment includes tools used to fabricate, assemble, test, and package chips.
          as of: not_stated
          citation 1 · src-002 · standing originator
            source: "The Semiconductor Supply Chain: Assessing National Competitiveness (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief-1.pdf
            class: policy_research_brief · publisher record: not_applicable
            stated dates: published 2021-01
            registered: automated 2026-09-29T13:25Z sha256 319d942ba534 · migrated from SRC-002
            locator: p.67, Appendix B: Glossary, entry 'Semiconductor manufacturing equipment'
            anchor: "Semiconductor manufacturing equipment includes tools used to fabricate, assemble, test, and package chips"
            read by the Verifier: 2026-10-01T20:44Z sha256 319d942ba534 (same bytes as registered)
exit 0

component-accelerated-server · component record · canonical components.json
  Accelerated server
  /identity_claim_ids:
    claim-lbnl-server-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: LBNL's 2025 update defines a server as a computer or system providing data, resources, or services to other computers (clients) over a network.
      as of: not_stated
      citation 1 · src-021 · standing originator
        source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
        class: research_report · publisher record: not_applicable
        stated dates: published 2026-06-18
        registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
        locator: p.7, glossary, entry 'Server'
        anchor: "Server – A computer or system providing data, resources, or services to other computers (clients) over a network"
        read by the Verifier: 2026-10-01T20:44Z sha256 1108b5a0f829 (same bytes as registered)
  /identity_claim_ids:
    claim-lbnl-accelerated-servers-category · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: LBNL's 2025 update distinguishes accelerated servers from CPU-driven servers, and describes a shift to accelerated servers for advanced workloads.
      as of: not_stated
      citation 1 · src-021 · standing originator
        source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
        class: research_report · publisher record: not_applicable
        stated dates: published 2026-06-18
        registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
        locator: p.16, §3.1.1, the sentence beginning 'This reflects the shift'
        anchor: "This reflects the shift to accelerated servers for advanced workloads, moving away from CPU-driven compute"
        read by the Verifier: 2026-10-01T20:44Z sha256 1108b5a0f829 (same bytes as registered)
  /definition/0/claim_ids: An accelerated server is a server, a computer providing data, resources or services to other computers over a network, that is configured with one or more AI accelerators.
    claim-atlas-accelerated-server-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, an accelerated server is a server, a computer providing data, resources or services to other computers over a network, that is configured with one or more AI accelerators.
      reasoning: LBNL defines the server and counts accelerated servers apart from CPU-driven ones; it gives no one-sentence definition of 'accelerated server'. The record composes the two with the AI-accelerator working definition. TQ-11: servers stay inside layer 6.
      input:
        claim-lbnl-server-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-lbnl-accelerated-servers-category · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-atlas-ai-accelerator-working-definition · INTERPRETATION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: For the Atlas, an AI accelerator is a data-centre logic chip, a GPU or an AI ASIC, whose primary purpose is AI training or inference. FPGAs and CPUs are outside v1 scope.
          reasoning: CON-01 is a definitional conflict (source-policy.md §10.2): CSET's definition includes FPGAs; LBNL's accounting covers GPUs and ASICs. The working definition is a choice, not a resolution. The human chose it at TQ-01 (domain-map.md §7.1, D-016). Both source positions stay as ATTRIBUTION claims.
          input:
            claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: CSET's definition of “AI chips” includes GPUs, FPGAs and certain types of ASICs.
              as of: not_stated
              citation 1 · src-003 · standing originator
                source: "AI Chips: What They Are and Why They Matter (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf
                class: policy_research_brief · publisher record: not_applicable
                stated dates: published 2020-04
                registered: automated 2026-09-29T13:25Z sha256 0f80b4fa1650 · migrated from SRC-003
                locator: p.4, footnote *
                anchor: "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"
                read by the Verifier: 2026-09-30T21:29Z sha256 0f80b4fa1650 (same bytes as registered)
          input:
            claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: LBNL's 2025 update says that the dataset of its 2024 report covered GPU accelerators only, and that the update “expands the accounting to all AI accelerators, namely ASICs”.
              as of: not_stated
              citation 1 · src-021 · standing originator
                source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
                class: research_report · publisher record: not_applicable
                stated dates: published 2026-06-18
                registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
                locator: p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report'
                anchor: "this update expands the accounting to all AI accelerators, namely ASICs"
                read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
exit 0

technology-multi-die-accelerator · technology record · canonical technologies.json
  Multi-die accelerator
  /identity_claim_ids:
    claim-nist-chiplet-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: NIST's NAPMP vision paper says chiplets are small, partially functional semiconductor chips that, when assembled at tight pitch and close to one another, result in a highly functional subsystem.
      as of: not_stated
      citation 1 · src-004 · standing originator
        source: "The Vision for the National Advanced Packaging Manufacturing Program" · NIST · https://www.nist.gov/system/files/documents/2023/11/19/NAPMP-Vision-Paper-20231120.pdf
        class: government_publication · publisher record: not_applicable
        stated dates: published 2023-11-20
        registered: automated 2026-09-29T13:26Z sha256 bb83ae40b640 · migrated from SRC-004
        locator: p.7, bullet 'Developing a chiplet ecosystem', the sentence beginning 'Chiplets refer to'
        anchor: "Chiplets refer to small, partially functional, semiconductor chips that, when assembled at tight pitch and close to one another, result in a highly functional subsystem"
        read by the Verifier: 2026-10-01T20:44Z sha256 bb83ae40b640 (same bytes as registered)
  /definition/0/claim_ids: A multi-die accelerator is a design approach in which an AI accelerator, presented as one device, is built from more than one die assembled in one package. The Atlas calls it multi-die; 'chiplet' is used only where a source uses it.
    claim-atlas-multi-die-accelerator-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, a multi-die accelerator is a design approach in which an AI accelerator, presented as one device, is built from more than one die assembled in one package. The Atlas calls it multi-die; 'chiplet' is used only where a source uses it.
      reasoning: CON-03: NIST, SIA/BCG and SK hynix describe chiplets differently. TQ-09 chose the neutral term 'multi-die'. The working definition keeps only what the three share (more than one die forming one functional unit) and applies it to the AI accelerator. Every side is an input; SK hynix's side is company marketing and is preserved as a position, not as a definitional source.
      input:
        claim-atlas-ai-accelerator-working-definition · INTERPRETATION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: For the Atlas, an AI accelerator is a data-centre logic chip, a GPU or an AI ASIC, whose primary purpose is AI training or inference. FPGAs and CPUs are outside v1 scope.
          reasoning: CON-01 is a definitional conflict (source-policy.md §10.2): CSET's definition includes FPGAs; LBNL's accounting covers GPUs and ASICs. The working definition is a choice, not a resolution. The human chose it at TQ-01 (domain-map.md §7.1, D-016). Both source positions stay as ATTRIBUTION claims.
          input:
            claim-cset-ai-chip-definition · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: CSET's definition of “AI chips” includes GPUs, FPGAs and certain types of ASICs.
              as of: not_stated
              citation 1 · src-003 · standing originator
                source: "AI Chips: What They Are and Why They Matter (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf
                class: policy_research_brief · publisher record: not_applicable
                stated dates: published 2020-04
                registered: automated 2026-09-29T13:25Z sha256 0f80b4fa1650 · migrated from SRC-003
                locator: p.4, footnote *
                anchor: "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"
                read by the Verifier: 2026-09-30T21:29Z sha256 0f80b4fa1650 (same bytes as registered)
          input:
            claim-lbnl-ai-accelerator-accounting · ATTRIBUTION · supported · verified 2026-09-30 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
              statement: LBNL's 2025 update says that the dataset of its 2024 report covered GPU accelerators only, and that the update “expands the accounting to all AI accelerators, namely ASICs”.
              as of: not_stated
              citation 1 · src-021 · standing originator
                source: "United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F)" · Lawrence Berkeley National Laboratory (LBNL) · https://www.osti.gov/servlets/purl/3374245
                class: research_report · publisher record: not_applicable
                stated dates: published 2026-06-18
                registered: automated 2026-09-29T13:28Z sha256 1108b5a0f829 · migrated from SRC-021
                locator: p.16, §3.1.2 'AI Accelerator Shipments', the sentence beginning 'The analogous dataset used in the 2024 Report'
                anchor: "this update expands the accounting to all AI accelerators, namely ASICs"
                read by the Verifier: 2026-09-30T21:29Z sha256 1108b5a0f829 (same bytes as registered)
      input:
        claim-nist-chiplet-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-sia-heterogeneous-integration-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          statement: SIA/BCG describe heterogeneous integration of chiplets as the process of combining multiple chips and chiplets to match the functionality of a single monolithic system-on-chip.
          as of: not_stated
          citation 1 · src-005 · standing originator
            source: "Emerging Resilience in the Semiconductor Supply Chain" · Semiconductor Industry Association (SIA) · https://www.semiconductors.org/wp-content/uploads/2024/05/Report_Emerging-Resilience-in-the-Semiconductor-Supply-Chain.pdf
            class: industry_association · publisher record: not_applicable
            stated dates: published 2024-05
            registered: automated 2026-09-29T13:29Z sha256 27040f69e8e0 · migrated from SRC-005
            locator: p.21, 'SIDEBAR: Chiplets', the sentence beginning 'Heterogeneous integration of chiplets is'
            anchor: "Heterogeneous integration of chiplets is the process of combining multiple chips and chiplets to match the functionality of a single monolithic system-on-chip (SoC)"
            read by the Verifier: 2026-10-01T20:44Z sha256 27040f69e8e0 (same bytes as registered)
      input:
        claim-sk-hynix-chiplet-description · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          statement: SK hynix describes chiplets as a technology that divides existing logic chips by function and connects them with TSV.
          as of: not_stated
          citation 1 · src-045 · standing originator
            source: "Semiconductor Back-end Process 4: Packages, Part 2 (retrieval of 2026-10-01; earlier bytes: src-013)" · SK hynix Newsroom · https://news.skhynix.com/semiconductor-back-end-process-episode-4-packages-part-2/
            class: company_marketing · publisher record: not_researched
            stated dates: published 2023-06-27
            registered: automated 2026-10-01T20:54Z sha256 660a781f4882d74424ad4fdd7f28dfba9ff11ed1a3b23264be683e6b809235c9
            locator: the paragraph after 'Figure 5. Conceptual diagram of a chiplet', the sentence beginning 'As shown in Figure 5'
            anchor: "As shown in Figure 5, it is a technology that divides existing logic chips by function and connects them with TSV"
            read by the Verifier: 2026-10-01T20:54Z sha256 660a781f4882 (same bytes as registered)
exit 0

technology-multi-die-package · technology record · canonical technologies.json
  Multi-die package
  /identity_claim_ids:
    claim-nist-chiplet-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: NIST's NAPMP vision paper says chiplets are small, partially functional semiconductor chips that, when assembled at tight pitch and close to one another, result in a highly functional subsystem.
      as of: not_stated
      citation 1 · src-004 · standing originator
        source: "The Vision for the National Advanced Packaging Manufacturing Program" · NIST · https://www.nist.gov/system/files/documents/2023/11/19/NAPMP-Vision-Paper-20231120.pdf
        class: government_publication · publisher record: not_applicable
        stated dates: published 2023-11-20
        registered: automated 2026-09-29T13:26Z sha256 bb83ae40b640 · migrated from SRC-004
        locator: p.7, bullet 'Developing a chiplet ecosystem', the sentence beginning 'Chiplets refer to'
        anchor: "Chiplets refer to small, partially functional, semiconductor chips that, when assembled at tight pitch and close to one another, result in a highly functional subsystem"
        read by the Verifier: 2026-10-01T20:44Z sha256 bb83ae40b640 (same bytes as registered)
  /definition/0/claim_ids: A multi-die package is the packaging of two or more dies in one package so that they work as one functional subsystem. The Atlas calls it multi-die; 'chiplet' is used only where a source uses it.
    claim-atlas-multi-die-package-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, a multi-die package is the packaging of two or more dies in one package so that they work as one functional subsystem. The Atlas calls it multi-die; 'chiplet' is used only where a source uses it.
      reasoning: CON-03 and TQ-09, as for the multi-die accelerator. This record is the packaging process; the multi-die accelerator is the design approach. Every side is an input.
      input:
        claim-nist-chiplet-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
      input:
        claim-sia-heterogeneous-integration-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          statement: SIA/BCG describe heterogeneous integration of chiplets as the process of combining multiple chips and chiplets to match the functionality of a single monolithic system-on-chip.
          as of: not_stated
          citation 1 · src-005 · standing originator
            source: "Emerging Resilience in the Semiconductor Supply Chain" · Semiconductor Industry Association (SIA) · https://www.semiconductors.org/wp-content/uploads/2024/05/Report_Emerging-Resilience-in-the-Semiconductor-Supply-Chain.pdf
            class: industry_association · publisher record: not_applicable
            stated dates: published 2024-05
            registered: automated 2026-09-29T13:29Z sha256 27040f69e8e0 · migrated from SRC-005
            locator: p.21, 'SIDEBAR: Chiplets', the sentence beginning 'Heterogeneous integration of chiplets is'
            anchor: "Heterogeneous integration of chiplets is the process of combining multiple chips and chiplets to match the functionality of a single monolithic system-on-chip (SoC)"
            read by the Verifier: 2026-10-01T20:44Z sha256 27040f69e8e0 (same bytes as registered)
      input:
        claim-sk-hynix-chiplet-description · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          statement: SK hynix describes chiplets as a technology that divides existing logic chips by function and connects them with TSV.
          as of: not_stated
          citation 1 · src-045 · standing originator
            source: "Semiconductor Back-end Process 4: Packages, Part 2 (retrieval of 2026-10-01; earlier bytes: src-013)" · SK hynix Newsroom · https://news.skhynix.com/semiconductor-back-end-process-episode-4-packages-part-2/
            class: company_marketing · publisher record: not_researched
            stated dates: published 2023-06-27
            registered: automated 2026-10-01T20:54Z sha256 660a781f4882d74424ad4fdd7f28dfba9ff11ed1a3b23264be683e6b809235c9
            locator: the paragraph after 'Figure 5. Conceptual diagram of a chiplet', the sentence beginning 'As shown in Figure 5'
            anchor: "As shown in Figure 5, it is a technology that divides existing logic chips by function and connects them with TSV"
            read by the Verifier: 2026-10-01T20:54Z sha256 660a781f4882 (same bytes as registered)
exit 0

technology-electronic-design-automation · technology record · canonical technologies.json
  Electronic design automation
  /identity_claim_ids:
    claim-cset-eda-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: CSET's glossary says electronic design automation (EDA) software is used to design chips.
      as of: not_stated
      citation 1 · src-002 · standing originator
        source: "The Semiconductor Supply Chain: Assessing National Competitiveness (Issue Brief)" · Center for Security and Emerging Technology (CSET), Georgetown University · https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief-1.pdf
        class: policy_research_brief · publisher record: not_applicable
        stated dates: published 2021-01
        registered: automated 2026-09-29T13:25Z sha256 319d942ba534 · migrated from SRC-002
        locator: p.66, Appendix B: Glossary, entry 'Electronic design automation (EDA)'
        anchor: "Electronic design automation (EDA) software is used to design chips"
        read by the Verifier: 2026-10-01T20:44Z sha256 319d942ba534 (same bytes as registered)
  /definition/0/claim_ids: Electronic design automation (EDA) is the class of software used to design chips. A vendor's EDA tool is a product, not this record.
    claim-atlas-electronic-design-automation-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, electronic design automation (EDA) is the class of software used to design chips. A vendor's EDA tool is a product, not this record.
      reasoning: CSET's glossary definition. Synopsys's broader description (software and hardware tools, SRC-018) is company marketing and is not used to define the class.
      input:
        claim-cset-eda-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
exit 0

technology-cloud-computing · technology record · canonical technologies.json
  Cloud computing
  /identity_claim_ids:
    claim-nist-cloud-computing-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: NIST SP 800-145 defines cloud computing as a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort or service provider interaction.
      as of: not_stated
      citation 1 · src-001 · standing originator
        source: "The NIST Definition of Cloud Computing (Special Publication 800-145)" · National Institute of Standards and Technology (NIST) · https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf
        class: government_publication · publisher record: not_applicable
        stated dates: published 2011-09
        registered: automated 2026-09-29T13:25Z sha256 7b0c1a9fdfc6 · migrated from SRC-001
        locator: p.6, §2 'The NIST Definition of Cloud Computing', first sentence
        anchor: "Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction"
        read by the Verifier: 2026-10-01T20:54Z sha256 7b0c1a9fdfc6 (same bytes as registered)
  /definition/0/claim_ids: Cloud computing is a service model: on-demand network access to a shared pool of configurable computing resources, rapidly provisioned and released with minimal management effort, as NIST defines it. A provider's cloud service is a product, not this record.
    claim-atlas-cloud-computing-working-definition · INTERPRETATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: For the Atlas, cloud computing is a service model: on-demand network access to a shared pool of configurable computing resources, rapidly provisioned and released with minimal management effort, as NIST defines it. A provider's cloud service is a product, not this record.
      reasoning: NIST SP 800-145's definition, unchanged in substance. No CON conflict applies.
      input:
        claim-nist-cloud-computing-definition · ATTRIBUTION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
          (shown above)
exit 0

product-nvidia-h100-tensor-core-gpu · product record · canonical products.json
  NVIDIA H100
  /vendor: company-nvidia · NVIDIA · canonical companies.json
  /instance_of: component-data-centre-gpu · Data-centre GPU · canonical components.json
  /identity_claim_ids:
    claim-h100-identity · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: The NVIDIA H100 Tensor Core GPU is a data center GPU that NVIDIA offers for large-scale AI and HPC.
      as of: not_stated
      citation 1 · src-042 · standing party
        source: "NVIDIA Hopper Architecture In-Depth (retrieval of 2026-10-01; earlier bytes: src-006)" · NVIDIA (NVIDIA Technical Blog) · https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
        class: company_technical_documentation · publisher record: not_researched
        stated dates: published 2022-03-22, modified 2025-07-22
        registered: automated 2026-10-01T20:44Z sha256 c509a2dc0ff25905818e630dfea548d1fc3a7df4d2d697706129cbfaf868244c
        locator: section 'Introducing the NVIDIA H100 Tensor Core GPU', first sentence
        anchor: "The NVIDIA H100 Tensor Core GPU is our ninth-generation data center GPU designed to deliver an order-of-magnitude performance leap for large-scale AI and HPC"
        read by the Verifier: 2026-10-01T20:44Z sha256 c509a2dc0ff2 (same bytes as registered)
  /vendor_process_name/0/claim_ids: TSMC 4N
    claim-h100-process-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: NVIDIA names the fabrication process of the H100 “TSMC 4N”.
      as of: not_stated
      citation 1 · src-042 · standing party
        source: "NVIDIA Hopper Architecture In-Depth (retrieval of 2026-10-01; earlier bytes: src-006)" · NVIDIA (NVIDIA Technical Blog) · https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/
        class: company_technical_documentation · publisher record: not_researched
        stated dates: published 2022-03-22, modified 2025-07-22
        registered: automated 2026-10-01T20:44Z sha256 c509a2dc0ff25905818e630dfea548d1fc3a7df4d2d697706129cbfaf868244c
        locator: after the GH100 specification list, the sentence beginning 'Using the TSMC 4N fabrication process'
        anchor: "Using the TSMC 4N fabrication process enables H100 to increase GPU core frequency"
        read by the Verifier: 2026-10-01T20:44Z sha256 c509a2dc0ff2 (same bytes as registered)
  /tdp_w: not_researched
  /rated_power_w: not_applicable
  /rack_scale: not_applicable
  /cooling_method: not_applicable
exit 0

product-amazon-com-trainium2 · product record · canonical products.json
  AWS Trainium2
  /vendor: company-amazon-com · Amazon · canonical companies.json
  /instance_of: component-ai-asic · AI ASIC · canonical components.json
  /identity_claim_ids:
    claim-trainium2-identity · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: Trainium2 is a machine learning chip that AWS offers, its third generation of purpose-built machine learning chip.
      as of: not_stated
      citation 1 · src-043 · standing party
        source: "Trainium2 Architecture (retrieval of 2026-10-01; earlier bytes: src-010)" · Amazon Web Services (AWS Neuron documentation) · https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html
        class: company_technical_documentation · publisher record: not_researched
        stated dates: undated
        registered: automated 2026-10-01T20:44Z sha256 746c25212873fd403894481c62b4cd1535b02ebf4f7439ae98b507fe47400cbf
        locator: heading 'Trainium2 Architecture', first sentence
        anchor: "Trainium2 is the third generation, purpose-built Machine Learning chip from AWS"
        read by the Verifier: 2026-10-01T20:44Z sha256 746c25212873 (same bytes as registered)
  /vendor_process_name: not_researched
  /tdp_w: not_researched
  /rated_power_w: not_applicable
  /rack_scale: not_applicable
  /cooling_method: not_applicable
exit 0

product-micron-technology-hbm4-36gb-12h · product record · canonical products.json
  Micron HBM4 36GB 12H
  /vendor: company-micron-technology · Micron Technology · canonical companies.json
  /instance_of: component-high-bandwidth-memory · High Bandwidth Memory · canonical components.json
  /identity_claim_ids:
    claim-micron-hbm4-identity · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-08-REPORT.md)
      statement: Micron names an HBM4 product “HBM4 36GB 12H” and states that it is in high-volume production.
      as of: not_stated
      citation 1 · src-044 · standing party
        source: "High-bandwidth memory (HBM) (product page; retrieval of 2026-10-01; earlier bytes: src-015)" · Micron Technology · https://www.micron.com/products/memory/hbm
        class: company_marketing · publisher record: not_researched
        stated dates: undated
        registered: automated 2026-10-01T20:44Z sha256 bb6d6d8f798080ec8c5faee25233cc4d51b126f82cae78d9dc673d8201aba50c
        locator: section 'Micron HBM4 in high-volume production', first sentence
        anchor: "Micron is in high-volume production of HBM4 36GB 12H"
        read by the Verifier: 2026-10-01T20:44Z sha256 bb6d6d8f7980 (same bytes as registered)
  /vendor_process_name: not_researched
  /tdp_w: not_researched
  /rated_power_w: not_applicable
  /rack_scale: not_applicable
  /cooling_method: not_applicable
exit 0

```
