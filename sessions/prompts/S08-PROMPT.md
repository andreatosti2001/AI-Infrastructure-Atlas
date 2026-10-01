# AI-Infrastructure-Atlas — S08 Session Prompt

## Operating contract

This is a governed Opus 5.5 session. Before changing anything:

1. Read `CLAUDE.md`.
2. Read the relevant sections of `MASTER-ARCHITECTURE.md`.
3. Read `SESSION-PROMPT-SPEC.md` and `PROJECT-EVALUATION-FRAMEWORK.md`.
4. Read the immediately previous session report if it exists.
5. Inspect the actual repository state; do not assume the roadmap matches reality.
6. Restate mission, scope, non-goals and acceptance criteria.
7. Propose the smallest safe execution plan before implementation.

Follow:
`inspect → reason → propose → implement → validate → report`

### Evidence rules
- Use authoritative/current sources when current information matters.
- Do not use search snippets as evidence.
- Do not invent facts or silently infer supply-chain relationships.
- Separate FACT, DERIVATION, INTERPRETATION and IMPLICATION.
- Preserve uncertainty and source conflicts explicitly.

### Engineering rules
- Prefer the simplest architecture that satisfies the requirement.
- Do not introduce infrastructure merely for appearance.
- Do not perform broad refactors outside this session's scope.
- Never overwrite canonical data from unverified text.
- Run relevant tests/validators before declaring completion.

### Autonomy boundary
If a required decision crosses an approval boundary, stop and report it rather than improvising.

## Session-specific mission

### Mission

Technology/component dataset

Model concepts independently of company language.

## Required end-of-session report

Record:
- files/components changed;
- data/evidence changes;
- commands/tests and results;
- decisions and rejected alternatives;
- deviations from this prompt;
- unresolved debt and evidence gaps;
- human approvals required;
- one concrete next-session handoff.

Commit only verified work.

---

# Part B — Session contract detail (SESSION-PROMPT-SPEC §2)

> **Provenance and precedence (D-012 pattern).**
> - Everything above this line is **Part A**. As for S07, no upload was made: the human
>   asked Claude to "write session 8's prompt as in the previous sessions".
>   - Claude assembled Part A from the fixed template: the operating contract, report list
>     and headings are byte-identical to S07's Part A, and are copied unchanged.
>   - The session-specific mission is copied verbatim from the operational roadmap's week-4
>     entry for S08 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`, "S08 —
>     Technology/component dataset"). That entry lists no human focus, and none is added.
>   - **The human confirmed Part A as assembled** before S08 started ("Confirm as assembled
>     (Recommended)", 2026-10-01).
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2. It was written after S07 (`SESSION-07-REPORT.md`,
>   `company-dataset.md`, D-054 to D-066) and before the merge that brings S07 to `main`.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The higher-level
>   documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The prompt becomes immutable once S08 begins (D-011).
> - **Answered before S08 started (2026-10-01):** the human answered H-0 to H-6 in §16,
>   choosing Claude's recommendation each time, and confirmed Part A. H-0 (the S07 review)
>   was applied before this prompt reached `main`.

## 01 — Session identity

- **Session:** S08
- **Title:** Technology + component dataset (operational roadmap: "Technology/component
  dataset")
- **Type:** IMPLEMENTATION (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`), with research: it
  retrieves the definitional sources the records need.
- **Milestone:** M2 — Canonical Dataset (`SESSION-ROADMAP.md` numbering, D-019). S08 is M2's
  second session.
- **Predecessor:** S07 — Company dataset (8 canonical companies, 4 jurisdictions; D-054 to
  D-066 accepted at the S07 review, H-0).
- **Expected successor:** S09 — Facility dataset.
- **Complexity class:** large. It creates three new record kinds at once (technology,
  component, product), the first definitional claims since S06, and the checks for them.
  The human can narrow it in §16.

## 02 — Mission

Create the canonical technology and component records of the first vertical, each with a
sourced working definition that does not collapse technically distinct concepts, and the
first product records (D-027), each pointing to a canonical company as its vendor.

- **Records:** technologies and components for the v1 concepts (H-1); a few products (H-2).
- **Evidence:** definitional sources of the classes `identity:technology`,
  `identity:component` and `attr:*.definition` prefer (`source-policy.md` §7): standards,
  government publications and research reports. Product evidence from the vendors' own
  documents.
- **Checks:** the record checks of S07 extended to the new kinds, plus `broader` acyclicity
  (`entity-taxonomy.md` §9).

The result must make three things impossible:

- a technology or component record whose definition rests only on a vendor's marketing (the
  roadmap's "independently of company marketing language");
- two technically distinct concepts in one record, or one concept in two records (the gate);
- a product whose vendor is not a canonical company, or whose attributes are read off a
  class or another product.

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S08: "Model the technologies/components themselves
independently of company marketing language". Focus: "Accelerator types, HBM, packaging,
foundry processes, critical equipment categories, relevant data-centre infrastructure
layers". Gate: "Definitions are sourced and do not collapse technically distinct concepts."

**Every later edge needs these endpoints.** S10's `requires`, `has_part`, `incorporates`,
`fabricates` and `packages` edges have technology, component or product endpoints
(`relationship-taxonomy.md` §2). DEP-01 to DEP-18 cannot become edges without them.

**Earlier decisions that land here:**

- D-027: S08 creates the first product records.
- D-016 and the TQ answers: the working terms the human chose for CON-01 to CON-05 (H-4).
- `entity-taxonomy.md` §9: `broader` acyclic; the first product records.
- S07's handoff (`SESSION-07-REPORT.md`, Implications): vendors point to the S07 companies;
  plan RA-4 retrievals early; the S06 claims S08 can cite are canonical.

## 04 — Current state

As of `main` after the S07 merge. Verify at start, and record the base, `git branch -a` and
`git ls-remote` in the report (D-018 L-03). **This prompt must be on `main` before S08
starts.**

**Accepted model:**

- entity types and fields (D-022 to D-027): `schemas/entities.schema.json`: `technology`
  (`technology_kind`, `broader`, `concept_refs`, `definition`), `component` (`use_class`,
  `broader`, `concept_refs`, `definition`), `product` (`vendor`, `product_kind`,
  `instance_of`, `vendor_process_name`, `tdp_w`, `rated_power_w`, `rack_scale`,
  `cooling_method`);
- relationships (D-028 to D-033), source policy (D-034 to D-043), claim model (D-044 to
  D-053), company dataset (D-054 to D-066).

**Data at the start** (as measured at the S07 final commit, `4a5f7b3`):

- 38 source records; 62 canonical claims, among them the S06 definitional ones:
  `claim-cset-ai-chip-definition`, `claim-lbnl-ai-accelerator-accounting`,
  `claim-atlas-ai-accelerator-working-definition` (TQ-01), `claim-nist-cloud-location-independence`,
  and the GH100 process `FACT` (`claim-h100-gh100-process-name`);
- 8 canonical companies, 4 jurisdictions; staging empty.

**Checks at the start:** 181 tests; `validate-data` (VD-1 to VD-13; V-1, V-4, V-9, V-10,
CE-1, ID-1, J-1) and `validate-freshness` (F-1) in CI. The entity checks walk
`companies` and `jurisdictions` only (`ENTITY_KINDS` in `tests/test_data_entities.py`).

**Open items S08 inherits:**

- the GH100 finding: the process claim is about the GH100 die, not the H100 product;
- the AWS legal entity (`company-dataset.md` §14), relevant to Trainium2's vendor;
- S05 debt: the class table vs the matrix; SRC-023 not re-read;
- the operational roadmap's week-3 checkpoint; S01's weekly gate.

**Not S08's:** facilities (S09), relationships (S10), events (S09), metrics (S14–S15).

**Next decision number:** D-067.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-07-REPORT.md`, with its addenda.
2. `docs/architecture/company-dataset.md` (the patterns S08 reuses: IDs, staging, attested
   anchors, record checks, freshness).
3. `schemas/entities.schema.json` (`technology`, `component`, `product`).
4. `docs/architecture/entity-taxonomy.md` §3.3–§3.5, §4.2, §5, §9.
5. `docs/research/source-policy.md` §2, §7 (rows `identity:technology`, `identity:component`,
   `identity:product`, `attr:technology.definition`, `attr:component.definition`,
   `attr:product.*`), §10 (conflicts), §11.
6. `docs/research/domain-map.md`: the concept entries in §5's v1 list, CON-01 to CON-05, §7
   (TQ answers).
7. `docs/architecture/claim-model.md` §2–§4, §13.
8. `docs/architecture/decisions.md`: D-016, D-022 to D-027, D-032, D-036, D-037, D-054 to
   D-066.

**External research: expected.** Every retrieval follows `source-policy.md` §11 (RA-1 to
RA-7) and the S07 practice: an access probe first, then one targeted RA-4 list for the human
(H-5). Web search only discovers URLs. Candidate sources (`INTERPRETATION`; the session
checks each):

- standards: JEDEC HBM standards (refused in S01; free with registration, RA-4);
- government: NIST (SRC-001, SRC-004 reachable in S01–S06), the CHIPS R&D programme
  documents;
- research: LBNL (SRC-021, SRC-022), university or national-laboratory papers on packaging
  and HBM;
- policy research: CSET (acceptable for identity and definitions, as `ATTRIBUTION`);
- vendors' technical documentation for products (`identity:product`).

**Audit findings to carry:** L-01, L-02, L-04, L-05, L-09 as in S07; S07's lessons: read
the sentence; plan RA-4 at the start with exact instructions; review where evidence is
ready; ask the scope of an "accept all".

## 06 — Required reasoning

Answer these before writing records, in a document (§07 task 1) and decisions.

1. **The concepts** (H-1). For each of the 17 v1 concepts mapped to `type:technology` or
   `type:component` in `entity-taxonomy.md` §5: which source defines it, in which class,
   and with which standing (`originator`)? Which concept has no definitional source of a
   sufficient class, and is therefore left out and recorded?
2. **Not collapsing distinct concepts.** For each pair the taxonomy separates (TSV vs HBM
   stack; 2.5D vs 3D; data-centre GPU vs AI ASIC; EUV vs DUV; packaging process vs
   packaging equipment): which definitions keep them apart? What is the test, and can a
   test check it (e.g. no two records share a definition claim, `concept_refs` unique)?
3. **Working definitions** (H-4). Each is an `INTERPRETATION` citing every side's
   `ATTRIBUTION` (CON-01 to CON-05; `source-policy.md` §10.1). Which TQ answer applies to
   which record? Where no conflict exists, is a single source's definition an
   `ATTRIBUTION` that the record cites directly, or is the Atlas's working definition always
   an `INTERPRETATION`?
4. **IDs.** S07's ID rule slugged a claim-backed legal name. A technology's or component's
   name is editorial. What stable, non-editorial key gives its ID: the S01 concept ID, the
   defining standard's term, or another rule? A product's ID: vendor plus the vendor's
   product name (`entity-taxonomy.md` §3.5)? Each rule machine-checkable where possible.
5. **`broader`.** Which records have a broader record (ACC-02 and ACC-03 under ACC-01; TSV's
   several parents, B-1)? `broader` is taxonomy only; "requires" and "part of" are S10
   edges. Acyclicity is checked.
6. **Products** (H-2). For H100, Trainium2, Micron HBM and an ASML EUV system:
   - which vendor record (the AWS legal-entity question for Trainium2);
   - `instance_of`: which component or technology class, by the vendor's own statement;
   - each attribute: claim-backed, `not_applicable` or `not_researched`;
   - **the GH100 finding:** the canonical process claim names the GH100 die that powers the
     H100. Does it support the H100 product's `vendor_process_name`, or is the value
     `not_researched` until a sentence about the H100 itself is found?
7. **Staging and canonical** (H-6): as D-061; CE-1 extended to the new files.
8. **New anchors:** Verifier-attested as D-062; images and PDFs as in S07.
9. **Checks:** extend `ENTITY_KINDS`, V-1 (vendor, `instance_of`, `broader`), V-9, V-10 (the
   new rows), CE-1, freshness F-1 (the `time_sensitive` rows, if any), plus `broader`
   acyclicity and the ID rules of q4. Hand-apply each to real records first (L-09).
10. **The human's review:** a review sheet per batch, as in S07, with the definitional
    choices flagged.

## 07 — Tasks

**Design**

1. `docs/architecture/concept-dataset.md` (or a name the session justifies): the answers to
   §06, referencing the taxonomy, policy and claim model by section, never restating them.

**Research**

2. Access probe of the candidate hosts; then one RA-4 list for the human (H-5), with exact
   pages and reasons. Record every refusal.
3. Register new sources (`src-039` onward).

**Implementation**

4. Definitional and product claims in `data/staging/claims.json`, verified at their
   locators.
5. Technology, component and product records in the H-3 layout, first in staging.
6. Checks (§06 q9) in CI, with fixtures and planted faults.
7. Promotion on the human's verdicts (H-6).

**Validation**

8. Fail first; then at least eight deliberate breaks, each showing which tests fail.
   Include: a definition resting only on marketing; two records with one definition; a
   `broader` cycle; a product whose vendor is staging or missing; a product attribute
   without a claim; an ID that changes with a display name; a product `instance_of` pointing
   to a missing class.

**Documentation**

9. Decisions from D-067, each `proposed`; `docs/README.md`, the baseline state rows,
   `README.md`, `contracts.md` paths if they change.
10. `sessions/reports/SESSION-08-REPORT.md`, with the review sheets and the trace of each
    canonical record.

## 08 — Explicit non-goals

- Facilities, relationships, events, metrics (S09, S10, S14–S15). A "requires" or "part of"
  statement found while reading is an S10 candidate, recorded, not a record.
- Product families and generations (HBM-05; `entity-taxonomy.md` §3.5).
- Coverage beyond H-1 and H-2.
- Any change to an accepted schema, vocabulary value or decision without a decision the
  human approves first (§16 stop).
- A vendor's marketing as a definition (`source-policy.md` §7).
- An agent runtime, a database or graph server, a UI; an external API; circumvention.
- Promoting anything without the human's verdict.
- Editing the root documents, `domain-map.md`, the taxonomies, the frozen register or
  migrated values. Anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **Evidence:** Part A's rules, `source-policy.md` and `claim-model.md`. Definitions rest on
  `originator` sources of a preferred or acceptable class; a vendor's statement about its
  own product rests on `party` standing. ER-5 (superlatives), ER-8 (plans), ER-9
  (company-level is not product-level) apply.
- **One home:** a definition lives in the record's `definition` field through its claims;
  the concept's layer stays derived from `concept_refs` (R-8); the product's vendor is the
  only link from product to company in S08.
- **Unknown ≠ zero:** every field present; `not_researched` where no source was read;
  `not_applicable` only where the attribute cannot apply (e.g. `tdp_w` on a service).
- **Tooling:** `tools/` standard library (D-003, D-026); PDF extraction in a scratch
  environment; no new dependency without an approved decision.
- **Process:** L-02, L-04, L-08.

## 10 — Agent responsibilities

As `docs/agents/contracts.md` (accepted, D-052; paths updated in S07). The Extractor's
allowed writes extend to the new staging files (H-3) through the Editorial row, recorded in
the report. The Change Detector stays inactive.

| Agent | May write | Notes |
|---|---|---|
| Source Scout | the report | discovery only |
| Extractor | `data/sources.json` (new records), `data/staging/*.json` | provenance on every candidate |
| Verifier | verification fields of staging claims; the report | re-checks its own locators |
| Knowledge Architect | the design document, `decisions.md` (append) | ID rules, one-home rulings |
| Data Auditor | `tests/`, `tests/fixtures/`, `tools/` | the checks of §06 q9 |
| Editorial | `docs/README.md`, baseline rows, `README.md`, `contracts.md` (paths only) | the new state only |

## 11 — Data and evidence rules

- **Canonical entities:** technologies, components, products; canonical only on the human's
  verdict (H-6).
- **Allowed relationship types:** none instantiated.
- **Required source tier:** `source-policy.md` §7 rows `identity:technology`,
  `identity:component`, `attr:technology.definition`, `attr:component.definition`
  (standards, government, research preferred); `identity:product` and `attr:product.*`
  (the vendor's technical documentation and marketing).
- **Provenance:** every value cites claims in the S06 shape.
- **Temporal:** definitions are `stable` rows; product rows as the matrix says.
- **Confidence:** no numeric values.
- **Unknown or unverified:** `not_researched`; access gaps support nothing (SP-7).

## 12 — Implementation rules

**May create:** the design document; `data/technologies.json`, `data/components.json`,
`data/products.json` and their staging copies (H-3); tests and fixtures;
`sessions/reports/SESSION-08-REPORT.md`.

**May modify:** `data/sources.json` (new records); `data/staging/claims.json`,
`data/claims.json` (promotion on verdicts); `tests/test_data_entities.py`,
`tests/test_data_schema.py`, `tests/test_freshness.py` (scope); `tools/trace.py` (default
files only); `decisions.md` (append); `docs/README.md`, baseline rows, `README.md`,
`contracts.md` (paths).

**Approach:** mirror S07. Rules are read from their homes (the matrix from
`source-policy.md` §7, concepts from `entity-taxonomy.md` §5), never copied.

**Prohibited:** a hard-coded list of concepts, rows or classes in a test; a runtime; a
hand-written JSON Schema validator; copying policy or taxonomy text.

**Schema changes to accepted files:** none. If §06 needs one, stop (§16).

## 13 — Verification plan

- **At start:** the full suite and Gate 0; base, `git branch -a`, `git ls-remote`; this
  prompt on `main`.
- **Environment:** a fresh virtualenv from the pins, installed set compared with the pins.
- **Fail first;** then the breaks of §07 task 8, each with the tests it fails.
- **Manual evidence check:** the Verifier reads every anchor's sentence and re-checks its own
  locators; the human reviews each batch.
- **Trace:** each canonical record, pasted in the report.
- **CI:** reported separately from local results (L-08).
- **Not applicable:** browser, accessibility, performance.

## 14 — Evaluation requirements

The report records decisions and rejected alternatives (the ID rules, the
working-definition rule, the GH100 ruling); deviations; invalidated assumptions (a concept
no source defines, a definition that merges two concepts); new debt; unresolved questions;
the human's verdicts verbatim.

## 15 — Acceptance criteria

1. Every canonical technology and component validates against the unchanged schema, and its
   `identity_claim_ids` and `definition` rest on claims that V-10 accepts for its rows.
2. No definition rests only on a class the row calls "never sufficient alone"; marketing
   never defines a class.
3. No two records share a concept or a definition claim; `broader` is acyclic; tests fail
   when either breaks.
4. Every working definition that resolves a CON conflict is an `INTERPRETATION` citing every
   side.
5. Every canonical product's `vendor` is a canonical company; every attribute is
   claim-backed or an explicit state; the GH100 ruling is recorded.
6. Every ID follows a written rule, machine-checked where the rule allows.
7. Every new source has class, retrieval, hash and dates; access gaps are listed; RA-4
   files stay outside the repository.
8. The extended checks run in CI.
9. Nothing real is canonical without the human's recorded verdict.
10. No change to accepted schemas or vocabulary values; no relationship, facility or event
    record; no scores; no runtime.
11. Tests and Gate 0 pass in a fresh virtualenv; CI observed or reported as not observed.
12. The report satisfies SPEC §5 and Part A; new decisions appended as `proposed`.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- a record would need a field, vocabulary value or kind the accepted schema lacks (e.g. a
  product family, a new `technology_kind`);
- a concept has no definitional source of a sufficient class: it is left out and recorded,
  never defined from marketing;
- two sources define one term for technically different things and no TQ answer covers it;
- a product's vendor is not a canonical company, or the vendor's legal entity is unclear
  (Trainium2: the AWS question);
- a source is reachable only by circumvention, or an anchor cannot be re-read (SP-7);
- promoting anything would happen without the human's verdict;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions already taken** (2026-10-01, before S08 started; Claude's recommendation
first in each list). Do not ask them again. Record H-1 to H-6 in decisions (`proposed`,
citing the human's answer), and stop only if a condition cannot be met.

- **H-0 — the S07 review:**
  - *(recommended)* approve all: D-054 to D-066 and the M1 audit accepted;
  - approve with amendments;
  - leave them proposed.
  - *Answer:* "Approve all (Recommended)". Applied before S08: the status lines, the dataset
    document, the M1 audit and an addendum to the S07 report.
- **H-1 — scope of concepts:**
  - *(recommended)* all v1 concepts that `entity-taxonomy.md` §5 maps to technology or
    component; a concept with no sufficient definitional source stays out, recorded;
  - one per chain layer.
  - *Answer:* "All v1 concepts (Recommended)".
- **H-2 — products (D-027):**
  - *(recommended)* a few, named in registered sources, with canonical vendors: NVIDIA H100
    (`src-006`), AWS Trainium2 (`src-010`), Micron HBM (`src-015`), an ASML EUV system
    (`src-017`);
  - H100 only;
  - no products in S08 (amending D-027).
  - *Answer:* "Few, from sources (Recommended)".
- **H-3 — layout:**
  - *(recommended)* one file per type, as D-055: `data/technologies.json`,
    `data/components.json`, `data/products.json`, with staging copies;
  - one combined concepts file.
  - *Answer:* "One file per type (Recommended)".
- **H-4 — definitions and the CON conflicts:**
  - *(recommended)* reuse the TQ answers (D-016): each working definition is an
    `INTERPRETATION` citing every side; reopening one needs a new decision;
  - reopen them in S08.
  - *Answer:* "Reuse TQ answers (Recommended)".
- **H-5 — standards:**
  - *(recommended)* an access probe first, then one RA-4 list of free standards for the
    human; paywalled ones stay gaps (RA-5);
  - no standards in S08.
  - *Answer:* "RA-4 list early (Recommended)".
- **H-6 — when records become canonical:**
  - *(recommended)* review inside S08, as S07: sheets as evidence becomes ready; accepted
    records move before the final commit;
  - after the session.
  - *Answer:* "Review inside S08 (Recommended)".

## 17 — Deliverables

- the design document (§07 task 1);
- new source records; definitional and product claims; technology, component and product
  records (staging and canonical);
- the extended checks, tests and fixtures;
- `decisions.md`: D-067 onward, `proposed`;
- `docs/README.md`, baseline rows, `README.md`, `contracts.md` paths if changed;
- `sessions/reports/SESSION-08-REPORT.md`.

## 18 — Handoff

S08's report must hand S09 (Facility dataset; "Add physical locations and distinguish
ownership, operation and production"):

- **Completed work:** the canonical technologies, components and products; the new sources
  and access gaps; the extended checks.
- **For S09:**
  - facility records point to jurisdictions (S07) and are owned or operated by companies
    through S10 edges, never fields (R-5);
  - the facility candidates found in S07's filings (ASML's Veldhoven campus, TSMC's fabs,
    Micron's and SK hynix's production sites) and their sentences;
  - the `identity:facility` and `attr:facility.*` rows; ER-8 for announced sites.
- **Open issues:** the human approvals of the S08 decisions; the AWS legal entity; S01's
  weekly gate; S05 debt.
- **Recommended next decision:** the human confirms the concept and product IDs before S10,
  because edges will point to them.
- **Files for S09 to read first:** the S08 report; the S08 design document;
  `company-dataset.md`; `entity-taxonomy.md` §3.2, §4.2; `source-policy.md` §7 (facility
  rows), §12; D-022, D-031 and the S08 decisions.
