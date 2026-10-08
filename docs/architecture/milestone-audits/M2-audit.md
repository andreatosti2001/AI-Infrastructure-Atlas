# M2 Milestone Audit and S12 Data Architecture Audit

> **Records cited.** This is a process audit (PEF §4). The session reports and prompts it cites are kept in the
> private development archive, not in this repository (D-151); the decisions, documents and files it cites are here.

**Status:** ACCEPTED (approved by the human on 2026-10-02, at the S13 opening). Proposed in S12; the remediation of Part 4's blocking finding was ruled in S12.
**Date:** 2026-10-02
**Required by:** `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4 ("At every major milestone"), §5 (data
architecture audit), §3 (maturity per dimension); `SESSION-ROADMAP.md` S12 ("Architecture Audit
Report + remediation decisions").
**Scope** (the human's answer at the start of S12):

- **Part 1:** the M2 milestone audit, S07 to S10 (`SESSION-ROADMAP.md` numbering, D-019), which
  ended without one;
- **Parts 2 to 4:** S12's data-architecture audit of the canonical data model and the S11 page,
  against the roadmap's S12 list, S10's five items and S11's handoff.

**Rulings the audit is measured against.** D-100 to D-108 (the S11 page rules) were accepted by
the human at the start of S12, before any finding
was written.

**Written by:** Claude, as the Knowledge Architect (`docs/agents/contracts.md`: the audit report is
in its S12 write list). The process ratings of Part 1 are the Portfolio Reviewer's kind
of judgement; that role stays inactive (`roles.md`), as in the M1 audit (D-066).

**Bases read.**

- `main` @ `3f17270` (S11 and the S12 prompt merged, PRs #20 and #21); the measures below were
  taken on the session branch at `91f8342`, which changes only status lines (H-0) and the page's
  input digest. Data files are byte-identical to `3f17270`.
- The S07 to S11 prompts and reports, including every addendum; `decisions.md` D-054 to D-108;
  the M1 audit; `baseline.md`; `git log`.
- `data/`, `schemas/`, `tools/`, `tests/`, `site/hbm-chain/index.html`.

**Claim labels** (CLAUDE.md §6), as in the M0 and M1 audits:

- `FACT`: a file, line, commit or command output in this repository;
- `ATTRIBUTION`: what a session report says about itself, not re-measured here;
- `DERIVATION`: a count, comparison or probe result computed here from `FACT`s;
- `INTERPRETATION`: this audit's own reading;
- `IMPLICATION`: what follows for S13 and later.

No external source was read. A finding that would need a fact about the world is
recorded as a gap, not answered.

---

## Part 1 — M2 audit (PEF §4, eight questions)

### 1. What was intended

`SESSION-ROADMAP.md` M2, each session's gate (`FACT`, the roadmap text):

| Session | Mission | Gate |
|---|---|---|
| S07 | the first canonical companies and jurisdictions | "Every canonical company record has identity evidence and stable IDs." |
| S08 | technologies, components and products | "Definitions are sourced and do not collapse technically distinct concepts." |
| S09 | facilities and events | "Do not conflate headquarters, company ownership, operating control and physical manufacturing location." |
| S10 | the first relationships | "Graph-like navigation is possible using relational data without introducing a graph database." |

The M1 audit (Part 1, question 8) carried into M2: the pipeline source → staged claim → verified
claim → human review → canonical record; the record-level checks V-1 to V-10 and freshness, each
arriving with its records; reading as the guard machine checks cannot replace; the open debt; and
RA-4 manual retrievals planned per session.

### 2. What was implemented

All `FACT` as measured at `91f8342` (data unchanged since S10) unless a report is cited:

| Session | Records made canonical | Decisions | Tests after the session (`ATTRIBUTION`, each report's final run) |
|---|---|---|---|
| S07 | 8 companies, 4 jurisdictions; `validate-freshness` (F-1); the M1 audit | D-054 to D-066 | 181 |
| S08 | 7 components, 9 technologies, 3 products (5 technologies promoted at the end of S09) | D-067 to D-077 | 190 |
| S09 | 2 facilities, 4 events; the event schema; `tools/facility_status.py` | D-078 to D-088 | 221 |
| S10 | 5 relationships; `tools/navigate.py` | D-089 to D-099 | 264 |

- **Data at the end of M2:** 52 source records; 120 canonical claims; 33 entity records; 4
  events; 5 relationships; staging empty.
- **Decisions:** 46 (D-054 to D-099), all accepted at the human's reviews (`FACT`, status lines).
- **Gates:** each met as the S10 report's "M2 completion" table records (`ATTRIBUTION`). S10 met
  its gate with 5 edges, not the 10 to 12 its prompt expected.

### 3. What changed, and why

| Change | From → to | Why | Record |
|---|---|---|---|
| Changed source bytes | re-cited under the old record → a new source record | a record's hash must match what was read | D-075 |
| SME-03 | one technology record → EUV and DUV lithography | the taxonomy left scanners open; Part B named the pair | D-070 |
| Events | none → an event schema; facility status derived from events | MA §5.6 | D-083, D-085 |
| F-1 | company fields → also edges on `time_sensitive` rows | S10 Part B §06 q4 | D-096 |
| Relationships layout | (open) → one file with the type as a field | H-2 of S10 | D-098 |
| `instance_of` and facility-kind evidence | (no claim field in the schema) → basis rows in design documents | schema change out of scope | S08 Deviation 3; D-081 |
| AWS | (no record) → an alias of `company-amazon-com`, the `designs` endpoint | the 10-K names AWS as a segment | D-074, D-093 |
| TSMC → H100 | expected S10 edge → a recorded gap | F-1 on a 2025 page | D-092 |

### 4. Which assumptions failed

Each is `ATTRIBUTION` (the report that found it); none was hidden by rewriting an accepted
artifact.

- **That filings' properties sections name sites.** Micron's and Amkor's give country totals;
  several "sites" were plans (S09, Invalidated assumptions).
- **That NVIDIA's supplier paragraph yields `supplies` edges.** ER-9 and the absence of a memory
  component record give none (S10).
- **That subsidiary lists yield `owns` edges.** D-057 rules out a subsidiary record from a
  parent's exhibit (S10).
- **That TSMC → H100 would be an S10 edge.** F-1 makes its product-level evidence stale (S10).
- **That 10 to 12 edges would exist.** The evidence supports 5.
- **That registered pages keep their bytes.** Four changed before S08 cited them again (S08
  Deviation 2).

### 5. Which shortcuts were taken

- **Extraction and promotion scripts lived in the session scratchpad** (S07 debt). Their effects
  are checked in CI; the scripts are not in the repository.
- **Per-record evidence in document tables** where the schema had no claim field: `instance_of`
  (IO-1), facility kinds (FK-1). See Part 2, finding N-2.
- **ISO 3166 evidence as screenshots,** attested by reading.
- **Extractor and Verifier were one agent**. S08 to S10 record no separate
  Verifier either; each session was run by one Claude session. The human's review is the
  independent check.
- **Approval by delegation** once.
- **Checkpoint commits with known failures** on the feature branch, never on `main` (S07
  Deviation 8).

### 6. What technical and research debt was created

Open at the end of M2 (`FACT`, each report's debt section, checked against `main`). The owners in
the last column are those recorded at the time; Part 4 re-assigns them where S12 finds a reason.

| Debt | Created | Owner recorded |
|---|---|---|
| Role fit not machine-checkable (break 7b "NOT CAUGHT") | S07 | reading and review |
| Freshness does not age in CI; the Change Detector stays inactive | S07 | the Change Detector's first session |
| Extraction and promotion scripts outside the repository | S07 | none |
| Markdown parsing: legal-form table, attestation date, concept and product tables, IO-1, FK-1, RV-1 words, §1 candidates | S07 to S10 | none |
| Two source records per changed URL, linked only through the title | S08 | none |
| HBM-03, HBM-04 concept gaps | S08 | JEDEC JESD238 or another sufficient source |
| TSMC's and ASML's sites; SK hynix's Cheongju plants; Micron Japan | S09 | RA-4; D-088; a JP record |
| TSMC → H100 `fabricates`; `supplies` items with no record; subsidiary records; HBM suppliers `not_researched` | S10 | D-092; a concept decision; D-095; ER-3 |
| RV-1 and PL-1 are word guards | S10 | M3's audits (this one, Part 3) |

### 7. What was removed or rejected

The main rejections, each with its decision (every decision lists its own):

- **IDs:** edge IDs from a counter or without type prefixes (D-090); IDs from display names (ID-1,
  PI-1, FI-1, each with a break that shows a rename does not move an ID).
- **Stored derivations:** a stored facility status (D-085); a stored adjacency list (D-097); a
  stored inverse or `depends_on` (S10 breaks 6, 7).
- **Evidence shortcuts:** `item` broadened or narrowed to an existing record (ER-9); a subsidiary
  record from a parent's exhibit (D-057); `not_publicly_determinable` without the full search
  (ER-3, D-094); `valid_from` from a construction date (S10 §4).
- **Infrastructure:** DuckDB and a graph database in M2 (D-097, NG-07).

### 8. What should be carried into M3

M3 began with S11 before this audit was written. What M3 inherits, besides Parts 2 to 4:

- **The pipeline works for five record kinds** (sources, claims, entities, events, edges), each
  with staging, a human verdict and promotion, and record-level checks in CI.
- **The edge evidence is thin by evidence, not by model:** no `supplies`, `fabricates` or `owns`
  edge exists. A dependency map built now will show gaps first (S10 "M2 completion").
- **Reading remains the guard** for what word checks cannot see (Part 3, S10-1).
- **The human's review is the only independent check** (Part 1 process finding P-3).

---

## Part 1b — M2 process findings (PEF §4, §12)

| ID | Finding (`INTERPRETATION`) | Evidence |
|---|---|---|
| P-1 | **The D-018 commitments held through M2.** Every new check runs in CI (L-02); each report records its base (L-03); counts in prose are measured or labelled (L-04); prompts were on `main` before each session | `FACT`: `.github/workflows/ci.yml`; each report header; the merge commits before each session (`git log`) |
| P-2 | **Fail-first runs and deliberate breaks were done every session, and reported a miss honestly.** S07 break 7b ("role asserted with a claim that does not state it") was NOT CAUGHT and recorded as debt; S10 break 9 first passed for the wrong reason and was corrected | `ATTRIBUTION`: S07 and S10 "Deliberate breaks" |
| P-3 | **The human's rulings followed Claude's recommendation in every recorded answer.** Every answer quoted in the S07 to S11 ruling tables is the option marked as recommended, a selection among items Claude flagged, or a delegation. The human's independent interventions were the S07 spot-check of three anchors (H-6) and the S08 hold on D-070 and D-076, released in S09. The S11 new-user test recorded Claude's proposals, agreed, not the human's own findings | `DERIVATION`: a search of the quoted answers in the S07 to S11 report tables (`grep` for `| "…" |` not containing "Recommended" returns only gate texts, a quoted table row, the S08 vendor/ASIC answer to Claude's two flagged rulings, the S09 delegation and the S10 ticked edges); S07 and S08 addenda; S11 report |
| P-4 | **In-session review cleared M1's backlog** (M1 P-5). At the end of M2 no record waited for a verdict; staging was empty. The pace was high: S07 to S11 ran on 2026-10-01 and 2026-10-02 | `FACT`: `data/staging/*.json` (each `[]`); `git log` dates |
| P-5 | **Markdown-as-data grew in every M2 session, and no session consolidated it.** Each session recorded its own tables as debt (P-6 below lists them); the M1 audit had already named the pattern (O-5) and rejected a shared helper "for now" | `ATTRIBUTION`: S07 to S10 debt sections; M1 audit §2.4 |
| P-6 | **Data migrations are not reproducible from the repository.** The scripts that wrote and promoted records lived in the scratchpad (S07 debt); only their effects are checked | `ATTRIBUTION`: S07 debt; no promotion script in `tools/` (`FACT`) |
| P-7 | **Scope and gate outcomes were reported as met in part when they were** (S10's 5 edges; S11's criterion 8) | `ATTRIBUTION`: S10 Deviation 1; S11 "Acceptance criterion 8 is met in part" |

---

## Part 2 — The data model: the roadmap's S12 list

Each item has a finding, its evidence, and a maturity rating (PEF §3: 0 Absent · 1 Ad hoc ·
2 Defined · 3 Controlled · 4 Exemplary). Ratings are `INTERPRETATION` on the evidence given.

### N — Normalization and denormalization (rating 3)

- **N-1 (`FACT`).** One home per kind of statement holds for the records: a field's value sits
  with the claims that support it (`{"value", "claim_ids"}`); a claim holds its statement and
  citations; a source its bytes' hash; an edge its claims, with no record-level `source_ids`
  (RR-6). Facility status is computed, never stored (D-085). Unknowns are explicit states; no
  `null` appears in `data/` (`grep -c null data/*.json`: 0 in every file).
- **N-2 (`FACT`, `INTERPRETATION`). Five design-document tables hold values or evidence about
  named records, and code reads them; two more restate record values with no check:**

  | Table | Holds | Read by |
  |---|---|---|
  | `edge-dataset.md` §1 "Candidates that are not edges" | 12 refused candidates: endpoints by display name, type, sentence, why not | `tools/build_page.py`, `tests/test_page.py` |
  | `concept-dataset.md` §3 | each concept's record and **term**, the input of its ID (CI-1) | `tests/test_data_entities.py` |
  | `concept-dataset.md` §7 | each product's term (PI-1) and the claim behind each `instance_of` value (IO-1) | `tests/test_data_entities.py` |
  | `facility-dataset.md` §2 | each facility's term, the input of its ID (FI-1) | `tests/test_data_entities.py` |
  | `facility-dataset.md` §4 | the claim and word behind each facility kind (FK-1) | `tests/test_data_entities.py` |
  | `company-dataset.md` §2; `concept-dataset.md` §5 | each company's legal entity; each `broader` value, restated beside its reason | no check (an unchecked restatement) |

  The records stay the home of the values, and the checks keep the first five in step. But the
  terms that IDs are built from, and the evidence for `instance_of` and facility kinds, live
  only in documents, and the candidates live only there. A query over `data/` cannot see them.
- **N-3 (`INTERPRETATION`).** The rule tables the code reads (the §2 kind constraints, the §7
  source-policy matrix, the RV-1 words, the freshness horizon, the rule lines the page quotes)
  are rules, not values about records. They belong in their documents (Part 3, q2).

### D — Duplicate concepts (rating 3)

- **D-1 (`FACT`).** Checks reject the plain duplicates: two records with one definition (DEF-2,
  S08 break 2), one concept in two records (S08 break 8), a `requires` restating `broader`
  (V-6), the same edge twice (V-5, S10 break 14).
- **D-2 (`INTERPRETATION`). Two pairs of near-duplicate concepts are kept apart by definition
  only:**
  - a product's `vendor` ("whose name the offering carries", D-074) and the `designs` edge (who
    designs it). Trainium2 has both, from Amazon; the H100 has a vendor and no `designs` edge;
  - an `incorporates` edge's `supplier` (product-level) and a `supplies` edge (company-level;
    `relationship-taxonomy.md` §4.9 "Not to be confused with").

  Both distinctions are sound and documented; no check stops a query from conflating them.
- **D-3 (`FACT`).** `company-amazon-com` carries "Amazon Web Services" and "AWS" as aliases (a
  segment, D-074), and S10 records "Amazon Web Services, Inc." as a legal entity with no record
  (§6). One string family names a segment of one record and an unrecorded company.

### I — Stable IDs (rating 3)

- **I-1 (`FACT`).** Entity, product, facility, event and edge IDs are rule-made and recomputed by
  checks (ID-1, CI-1, PI-1, FI-1, EI-1, RI-1). Controls that rename every display name pass (S07
  9b, S08 6b, S09 control, S10 control). The terms that CI-1, PI-1 and FI-1 build IDs from are
  held in document tables (N-2).
- **I-2 (`FACT`).** Claim IDs are `claim-<slug>` (D-025), chosen by hand; no rule recomputes
  them. Source IDs are a counter (`src-NNN`, D-050).
- **I-3 (`FACT`).** No check compares IDs across commits: renaming a claim ID and every reference
  to it passes the suite. Stability rests on convention.
- **I-4 (`DERIVATION`).** Edge IDs embed their endpoint IDs, so correcting an endpoint gives a
  new ID (S10-5 below). The longest edge ID is 84 characters; the longest claim ID 81.
- **I-5 (`FACT`).** The page resolves the §1 candidates to records by display name or alias
  (`tools/build_page.py`, `gap_ends`: `r.get("name") == end or end in r.get("aliases", [])`). It
  is the one place in the code where a record is found from a name. Blocking with N-2 (B-1).

### R — Relationship semantics (rating 3)

- **R-1 (`FACT`).** Eleven types, each with a definition, a level, endpoint types in the schema,
  kind constraints (V-2), an evidence expectation (`relationship-taxonomy.md` §5) and a
  direction convention. Nothing derived is stored (RR-5; S10 breaks 6, 7).
- **R-2 (`FACT`).** "Who makes HBM?" has no edge path. Micron's HBM4 reaches HBM through
  `instance_of` and its maker through `vendor`, both entity fields (RR-4); both `incorporates`
  suppliers are `not_researched` (D-094). The model can hold the answer (a `supplier` assertion,
  a `supplies` edge); the evidence for it was not found (S10).
- **R-3.** The evidence guards are weak (S10-1 below).

### T — Temporal correctness (rating 2)

- **T-1 (`FACT`).** The model is defined: edges and field assertions carry `valid_from` and
  `valid_to`; claims carry `as_of`; events carry dates; facility status is derived from events;
  class edges carry no dates (schema); V-4, V-5 and F-1 run in CI.
- **T-2 (`DERIVATION`). It is almost unpopulated:** 0 of 5 edges has a period; 6 of the 85
  claims with citations have a dated `as_of` (79 are `not_stated`); one field assertion has a
  `valid_from` (NVIDIA's incorporation). The page says "no period in the claims" on every edge,
  so it cannot say when any relation held.
- **T-3 (`INTERPRETATION`). F-1 cannot record a past relation** (S10-3 below).

### P — Provenance completeness (rating 3)

- **P-1 (`FACT`).** Every value on the page traces to sources with no missing reference (PG-2,
  PG-3; `tools/trace.py`). Every citation carries a locator, an anchor, a standing and the
  bytes' hash; anchors are machine-checked where text exists (VD-11).
- **P-2 (`FACT`).** Identity fields (`name`, `aliases`, `vendor`, `instance_of`, `broader`,
  `product_kind`, `technology_kind`, `use_class`, `facility_kinds`, `jurisdiction_kind`) have no
  claim field; they rest on the record's `identity_claim_ids`, with per-value basis rows for
  `instance_of` and facility kinds in documents (N-2).
- **P-3 (`DERIVATION`).** `publisher_entity` is `not_researched` on 23 of 52 sources and
  `not_applicable` on 18 (S13: source quality).

### Q — Queryability (rating 2)

- **Q-1 (`FACT`).** `tools/navigate.py` answers `depends-on`, `suppliers`, `actors`, `edges` and
  `evidence`, as text or JSON (D-097, D-101). Of MA §18's six questions, it answers two in full
  (what depends on it; what evidence supports the edge), one as a state (who supplies it:
  `not_researched`), and none of the three that need suppliers' jurisdictions, regulations or
  policies (no supplier data; regulation and policy belong to other layers, NG-02).
- **Q-2 (`FACT`).** The page needed two walks no command answers: the actors on the chain and
  "the instances of a class and their vendors". The build reads the fields directly (S11,
  Invalidated assumptions).
- **Q-3 (`INTERPRETATION`).** Loading `data/` into SQL (S14) needs the `{"value","claim_ids"}`
  arrays flattened into rows, and cannot see the values held in documents (N-2).

### M — Migration risk (rating 2)

- **M-1 (`FACT`).** Schema changes are decisions (D-083 for events); staging and canonical files
  exist per record kind; fixtures test each check.
- **M-2 (`FACT`).** The tests parse Markdown by section markers and table shapes (`section(…,
  "\n## 7. ", "\n## 8. ")`; the build's `"**Candidates that are not edges**"` to `"**Count.**"`).
  A prose edit that moves a marker breaks a check or the build, for a reason unrelated to data.
- **M-3 (`FACT`).** The page is stale whenever one of its 33 inputs changes, including five
  design documents (S11 debt). Appending a decision makes PG-7 fail until a rebuild (it did at
  the start of S12: the H-0 status change).
- **M-4 (`FACT`).** Three parsers of Markdown tables exist (`cells` in `tools/build_page.py`,
  `tests/test_page.py`, `tests/test_entity_taxonomy.py`), plus section readers in other test
  modules.
- **M-5.** Migrations are not reproducible from the repository (P-6); edge IDs change with an
  endpoint correction (I-4); schemas carry no version field (their history is `git` and the
  decision log).

### V — Is the visual derived from canonical data? (rating 3)

- **V-1 (`FACT`).** Every value on the page equals its home (PG-1, PG-2); a rebuild is
  byte-identical (PG-7, confirmed at the start of S12); staging records cannot appear (PG-3, a
  build refusal).
- **V-2 (`FACT`).** Four inputs are not records: the §1 rows (Markdown, two parsers, names
  matched to records; N-2, I-5); the rule lines and decision titles (documents, by design); the
  journey specification (IDs chosen by hand, checked by PG-10); the fixed labels (`LABELS`, which
  name no record and hold no digit).

### S — Does the visual preserve scope, units and time? (rating 3)

- **S-1 (`FACT`).** Scope: the question names one class of accelerator and its memory; the lane
  says "not linked to any accelerator on this chain" (recomputed by PG-5). Units: the capacities
  are quoted inside their claims and never compared (they use different units and models,
  `vertical-slice.md` §4). Time: no visual channel encodes time; each edge shows its period or
  "no period in the claims"; the method section derives the ranges of verification and access.
- **S-2 (`INTERPRETATION`).** The visual preserves what the data holds. What it cannot show,
  when relations held, is a data limitation (T-2).

---

## Part 3 — S10's five items, S11's handoff, and the questions of Part B §06

### S10's items

- **S10-1. RV-1 and PL-1: keep them, as floors.** `DERIVATION` (a scratch script applying RV-1's
  word table to the anchors each §1 row names): **RV-1 alone would pass 6 of the 12 refused
  candidates** (TSMC → H100, SK hynix and Micron → NVIDIA, Carl Zeiss SMT GmbH → ASML,
  ASML → TSMC, NVIDIA → H100, Amkor → its subsidiaries). Other checks catch most of the six (F-1;
  V-1 for a missing record). One passes every machine check: **a probe adding
  `company-nvidia designs product-nvidia-h100-tensor-core-gpu`, citing `claim-h100-identity`
  ("… designed to deliver …"), failed no `validate-data` or `validate-freshness` test**; only the
  page tests failed, because the layout has no slot for it. Only reading (ER-2) refused it.
  `INTERPRETATION`: the guards cost little and caught real breaks (S10 breaks 1, 3); they are
  floors, as `edge-dataset.md` §7 already says. With the candidates as records, a later check can
  show which refusals the machine catches and which only a reader catches (Part 4, debt DT-5).
- **S10-2. Edge ID length and the period-collision rule: keep.** Length is a display cost (the
  page wraps IDs). The collision rule (a second period of the same relation needs a decision)
  has never fired: no edge has a period (T-2). Debt DT-3 records it for the first dated edge.
- **S10-3. F-1 and a 2022 product.** `INTERPRETATION`: F-1 measures the evidence date against
  the date of verification, for every `time_sensitive` row, whether or not the claim describes a
  closed past period. So "TSMC fabricated the H100 in 2022", if a source said so, would fail F-1
  as soon as the source is a year older than its check. The model cannot hold a past relation on
  a `time_sensitive` row. Not blocking (no such claim exists); debt DT-2.
- **S10-4. D-091 (necessity read out of a definition).** The data model holds it inspectably: a
  `DERIVATION` with its reasoning and inputs, shown one click from its mark. Whether it should
  become an evidence rule is a content question: S13.
- **S10-5. The AWS alias endpoint (D-074, D-093).** `INTERPRETATION`: activity by a subsidiary
  recorded on its parent is a recorded ruling, visible in the claim ("AWS-designed"). The data
  risk is migration: if an AWS company record is created, the `designs` edge moves to it and its
  ID changes (I-4). Debt DT-6, for the session that creates the record.

### S11's handoff

- **Entity-field paths for "who makes it"** (R-2): by design (RR-4); the gap is evidence, plus a
  navigation question (Q-2, debt DT-4).
- **No periods** (T-2): debt DT-2.
- **The hand-chosen journey specification** (V-2): IDs only, checked by PG-10. Acceptable for one
  page; a second composition decides a reusable pattern (MA §16.1, `vertical-slice.md` §11).

### q1 — The refused candidates become records: the design (H-1)

The human chose records ("Pick the recommended", end of S11). The design below is the Knowledge
Architect's proposal (D-109); nothing is built before the human approves it (H-2).

**What one record holds.** One record per §1 row: 12 records. Every value is copied from its row,
never improved.

| Field | Holds | From the §1 row |
|---|---|---|
| `id` | `cand-NNN`, three digits, in §1 row order, never reused | (new) |
| `relation_types` | one or more relation types from the relationship schema's vocabulary (one row names two: Micron → Manassas, `owns`, `operates`) | Type |
| `source_entities`, `target_entities` | one or more endpoints each (one row names two sources: SK hynix, Micron → NVIDIA). An endpoint is an entity ID where a record exists, or `{"state": "no_record", "name": "…"}` | Candidate |
| `item` | the item named, for `supplies`: an entity ID or `{"state": "no_record", "name": "…"}`. Left out when the row names none | Why not |
| `considered` | what was read: `{"claim_id": "…"}` for a claim, or `{"source_id", "locator", "anchor", "read"}` for a sentence that is not a claim. `anchor` is the quoted text, verbatim from the row, and left out when the row quotes none. `read` is the Verifier's re-read (`accessed_at`, `sha256`, as on a claim's citation) or `{"state": "not_re_read"}` | Sentence |
| `reasons` | one or more codes from a controlled list in the schema (below) | Why not (the Extractor's coding; the human reviews it) |
| `reasoning` | the row's "why not" text, verbatim | Why not |
| `ruling` | the decision that refused it: `D-089` (edge scope), or `D-092` for TSMC → H100 | Why not, and the §1 rule |

**What it must not hold.**

- **No status** (RR-6). Being in the file is the ruling; there is no `refused` field. Whether a
  cited claim is staging or canonical is read from where it is, never copied (the row's word
  "staged" for `claim-tsmc-fabricates-h100` is stale: that claim is canonical since the S10
  review).
- **No edge fields** (`claim_ids`, `valid_from`, `supplier`), so neither schema accepts the
  other's records.
- **No inferred edge** (RR-5). A candidate is never read by `navigate.py` or the trace as an edge.

**The reasons** (controlled list; each code's definition lives in the schema, its one home):

| Code | Means | Rows |
|---|---|---|
| `relation_not_stated` | the sentence does not state this relation itself: it names the parties together, says what a thing is for, or states possession, production or group membership, which the type's evidence expectation does not accept (RR-1, ER-2, taxonomy §5) | ASML → TSMC; ASML → Micron; NVIDIA → H100; Amazon → Trainium2 (second sentence); Amazon → Amazon Web Services, Inc.; Micron → HBM4 36GB 12H; Micron → Manassas |
| `wrong_relation_type` | the sentence states a relation of another type (taxonomy §4) | TSMC → NVIDIA |
| `company_level_only` | the sentence is about a company in general, not the product or item the edge would name (ER-9) | TSMC → NVIDIA; Micron → HBM4 36GB 12H |
| `endpoint_has_no_record` | a party has no record, and this evidence cannot create one (D-057, D-095) | Carl Zeiss SMT GmbH → ASML; Amkor → its subsidiaries; Amazon → Amazon Web Services, Inc. |
| `item_has_no_record` | the item has no record, and the Atlas does not stretch it to one that exists (ER-9) | SK hynix, Micron → NVIDIA; Carl Zeiss SMT GmbH → ASML |
| `evidence_not_fresh` | the type's row is `time_sensitive` and the evidence is older than the freshness horizon (F-1) | TSMC → H100; Amazon → Amazon Web Services, Inc. |

**An endpoint with no record** (Carl Zeiss SMT GmbH, "its subsidiaries", Amazon Web Services,
Inc.; the items "memory" and "optical column") is an explicit state with the name the row
writes. It is not a placeholder (RR-7, V-9): it has no ID, no record pretends to exist, and a
check fails if the name is the name or an alias of an existing record (then the ID must be
used) or a placeholder word. Samsung, named in NVIDIA's sentence, is not added: the row names
SK hynix and Micron only, and the copy is not improved (recorded for S13).

**A sentence that is not a claim** (`src-024` p.8 and the others) is held with its source,
locator and quoted anchor, and a `read` state. It is never evidence for anything: no tool reads
`considered` as support, the page does not show it (as D-104 already rules for the "sentence"
cells), and a check fails if a candidate's considered claim is also cited by an edge of the same
type between the same endpoints (a sentence is never both used and refused for one relation).
Amazon → Trainium2 (second sentence) is the case this permits: the relation is an edge from
another sentence, and the refused sentence is not among the edge's claims.

**ID rule, file and layout.** `cand-NNN` by row order, as `src-NNN` (D-050); a rule-made ID like
RI-1 is impossible when an endpoint has no record or a row has two sources. Files under H-2
(recommended: `data/refused_candidates.json`, `data/staging/refused_candidates.json`,
`schemas/refused_candidates.schema.json`).

**Staging and review** (D-061 pattern). The Extractor writes the 12 records to staging by a
script; the script asserts every value equals its §1 cell (endpoint names to the records' names
or aliases, types, claim and source IDs, quotes, the "why not" text). The Verifier re-reads each
quoted sentence where the registered bytes can be retrieved, and records `read`, or leaves
`not_re_read`. The human reviews each record's reason codes. Accepted records move to the
canonical file; then the table's rows leave `edge-dataset.md` §1.

**Checks** (written before the data, each shown failing on a planted fault):

| Check | Fails when |
|---|---|
| RC-1 | a record is invalid against the schema (VD-2 extended to both files) |
| RC-2 | an entity ID, claim ID, source ID or ruling does not resolve (entity of the prefixed type; claim; source; a decision in `decisions.md`) |
| RC-3 | a canonical candidate cites a staging claim or record; an ID is in both files; IDs repeat; an ID breaks `cand-NNN` |
| RC-4 | a `no_record` name is the name or an alias of a record, or a placeholder word (RR-7, V-9) |
| RC-5 | the reasons disagree with the structure: `endpoint_has_no_record` without a `no_record` endpoint, or the reverse; the same for `item_has_no_record`; `evidence_not_fresh` on a type whose source-policy row is not `time_sensitive` |
| RC-6 | a considered claim is cited by an edge of the same type between the same endpoints |
| RC-7 | a rule code (ER-, RR-, F-, D-) quoted in a `reasoning` has no home (as PG-10 does now) |

**One home after the move.** `edge-dataset.md` §1 keeps the rule (D-089), the edges table, the
rulings table and a pointer to the file; the twelve rows leave it. The values (endpoints, types,
sentences, reasons, the "why not" text, the ruling) live in the records. The reason codes'
definitions live in the schema.

**What this enables** (`IMPLICATION`): the page reads one parser (JSON), not two; endpoints are IDs,
so a rename cannot break or mis-resolve them; the refusals become a labelled set a later check can
run the evidence guards against (S10-1).

### q2 — The rule tables the page reads (D-108): keep them in their documents

`INTERPRETATION`. The page quotes one-line rules (ER-, RR-, F- codes) from `source-policy.md`,
`relationship-taxonomy.md` and `company-dataset.md`, and decision titles from `decisions.md`.
These are rules and rulings, whose home is their document. Quoting them is quotation, not
duplication, and PG-10 checks every quoted code has its line.

The principle that separates q1 from q2 (proposed as D-110): **a value about a named record is
data and lives in `data/`; a rule that governs records lives in its design document, and code may
read it.** Under it, the §1 candidates move (q1), the rule tables stay, and the other tables of N-2
are debt (DT-1).

### q6 — The page after remediation

- **"What the Atlas does not know" keeps its order:** unknown values; recorded gaps (TSMC → H100,
  drawn, with its candidate's reasoning); candidates that are not edges; no recorded relationship.
- **Candidates become cards, grouped by reason.** Each group's heading is the reason code's schema
  definition; each card shows the endpoints (a record's name, linked to its evidence panel where
  the page has one; a `no_record` name marked "no record in the Atlas"), the relation type, the
  item, the reasoning and the ruling's title. A candidate with two reasons appears under each.
- **The same four candidates as now** (the journey specification names them by ID: TSMC → H100,
  SK hynix and Micron → NVIDIA, NVIDIA → H100, Micron → HBM4 36GB 12H). Showing all twelve would
  widen the page beyond its question (D-104's reason for four).
- **Never as lines.** No candidate is drawn in the diagram. TSMC → H100 stays the one drawn gap,
  opened from its canonical claim, as D-104 rules.
- **Checks that change:** PG-2 resolves `cand-` references against the records, and no longer
  reads `edge-dataset.md`; PG-10 requires each journey candidate to exist and be canonical; PG-5
  fails if a candidate reference appears inside the diagram; a build refusal for a staging
  candidate; `edge-dataset.md` leaves the build's inputs (a prose edit to it no longer makes the
  page stale); the new data file joins them through `data/*.json`.

---

## Part 4 — Blocking findings and debt

**Blocking** (fix before S13; remediated in S12 only with the human's ruling):

| ID | Finding | Remediation | Decision |
|---|---|---|---|
| B-1 | The refused candidates are values about named records held in a Markdown table, read by two parsers and resolved to records by display name; one cell is stale (N-2, I-5, V-2) | records, checks, page (q1, q6) | D-109, with H-2 |

**Remediation outcome** (S12, 2026-10-02). The human approved the design and the layout (an own file, separate from real links) and the twelve migrated records.
B-1 is remediated: `data/refused_candidates.json` holds the twelve candidates; RC-1 to RC-8 run in
CI (`tests/test_data_candidates.py`); the page reads the records and no longer reads
`edge-dataset.md` (which left its inputs); the build and `tests/test_page.py` no longer parse a
Markdown table, so two of M-4's three table parsers are gone; endpoints are IDs, so renaming every
company's display name no longer stops the build (before S12 it refused: "'TSMC' does not name one
record"). The checks are in `tests/test_data_candidates.py` and `tests/test_page.py`.

**Debt** (each with an owner; not remediated in S12):

| ID | Finding | Owner | By |
|---|---|---|---|
| DT-1 | Four other document tables hold values or evidence about named records, read by checks (N-2): the CI-1, PI-1 and FI-1 terms, the IO-1 and FK-1 basis rows; two more restate values unchecked (legal entities, `broader`) | Knowledge Architect (schema), Data Auditor (migration) | before S14: the SQL layer must not parse Markdown |
| DT-2 | No edge has a period; F-1 cannot hold a past relation on a `time_sensitive` row (T-2, S10-3) | Knowledge Architect, by decision | before the first edge with a period or a past `as_of` |
| DT-3 | ID stability rests on convention: claim IDs hand-chosen; no cross-commit check; edge IDs change with an endpoint; the period-collision rule untried (I-2 to I-4, S10-2) | Data Auditor | before the first export (S14) |
| DT-4 | Navigation has no command for "instances of a class and their vendors" or the actors on a chain; `data/` needs flattening for SQL (Q-2, Q-3) | Analyst and Data Auditor | S14 |
| DT-5 | RV-1 and PL-1 pass 6 of 12 refusals; NVIDIA → H100 passes every machine check (S10-1) | Data Auditor (a guard-calibration check over the candidate records); S13 (sampling) | after B-1; S13 |
| DT-6 | AWS as an alias of its parent; the edge moves and its ID changes when an AWS record exists (D-3, S10-5) | the session that creates the AWS record (D-093, D-095) | — |
| DT-7 | `vendor` vs `designs`, `supplier` vs `supplies`: kept apart by definition only (D-2) | Knowledge Architect | when a query combines them (S14) |
| DT-8 | Migration and promotion scripts outside the repository (P-6) | Data Auditor | from S12: a migration script is kept with its session report |
| DT-9 | Three table parsers and section readers keyed on prose markers (M-2, M-4) | Data Auditor | with DT-1, or when a second page is built |
| DT-10 | `publisher_entity` `not_researched` on 23 sources (P-3) | S13 (source quality) | S13 |
| DT-11 | The human's rulings followed every recommendation (P-3) | the human; each session prompt asks for the human's own reading before Claude's suggestions (S11's lesson) | S13's sampling |

---

## Part 5 — Maturity per dimension (PEF §3)

Compared with the M1 audit (§2.3). Each rating is `INTERPRETATION` on the evidence given.

| Dimension | M1 process / outcome | M2 process | M2 outcome | Evidence |
|---|---|---|---|---|
| Data architecture | 3 / 2 | 3 | 3 | Part 2: rule-made IDs, field-level claims, explicit unknowns, record checks in CI. Held back by temporal (2), queryability (2) and migration (2) |
| Content & review | 3 / 2 | 3 | 2 | 120 canonical claims, each accepted by the human, anchors checked, F-1. Depth thin (5 edges, no `supplies`, `fabricates`, `owns`); review follows recommendations (P-3). S13 re-rates |
| Agent architecture | 2 / 2 | 2 | 2 | Contracts for every active role (seven, with Editorial and QA from S11); Extractor and Verifier one agent; no runtime (NG-08) |
| Analytical depth | 0 / 0 | 0 — not started | 0 — not started | S14 to S16 |
| Code / engineering | 3 / 2 | 3 | 2 | 291 tests (5,950 lines), fail-first and breaks every session, a deterministic build. Maintainability cost grew: more document parsing (M-2, M-4), test cross-imports |
| Product / user value | 2 / 1 | 2 | 2 | One page answers one question with its evidence (S11); unpublished; usability shown by review, not observation |
| Reproducibility | 3 / 2 | 3 | 3 | Byte-identical page with an input digest; records with hashes and anchors. Migrations not in the repository (P-6) |

**Regressions since M1:** none in the ratings. Process concern: P-3.

---

## Part 6 — Learning outcomes (PEF §10)

**What capability did M2 make demonstrably stronger?** (`INTERPRETATION`)

- **Data modelling with evidence:** five record kinds on one pipeline, each value tied to the
  claims that support it, unknowns as states, status derived from events.
- **Evidence discipline under pressure:** S10 recorded 5 edges rather than stretch evidence to
  12, and kept refusals with their reasons.
- **Check design:** rule-made IDs with rename controls; deliberate breaks that report a miss.

M2 did not yet show temporal or analytical depth: no relation is dated, and nothing is computed
over the edges (S14 to S15).

---

## Part 7 — Handoff to S13

S13 (content and evidence depth audit; "No scaling until evidence weaknesses are corrected or
explicitly documented"):

- **Claims and edges that carry the most weight on the page:** `claim-h100-hbm-stacks` and
  `claim-trainium2-hbm-capacity` (the two `incorporates` edges, the page's short answer);
  `claim-hbm-requires-3d-die-stacking` (D-091); `claim-tsmc-fabricates-h100` (D-092, the drawn
  gap); `claim-aws-designed-trainium2` (D-093); `claim-sk-hynix-operates-m16` (D-099).
- **Derivations whose steps S13 should challenge:** D-091, D-099, the TSMC claim.
- **Whether the page's annotations remove a caveat:** the short-answer sentence and the lane.
- **First sampling question** (recommended): *for each of the five edges and the drawn gap, does
  the quoted anchor, read in its source, state the relation as strongly as the page draws it?*
- **Also for S13:** Samsung, named in the memory-supplier sentence but not in the §1 row (q1);
  DT-5, DT-10, DT-11.
