# AI-Infrastructure-Atlas — S04 Session Prompt

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

Relationship taxonomy

Define semantic relationships.

Human focus:
- reject ambiguous relationships such as `associated_with` when a more precise relationship exists;
- require evidence expectations per relationship type.

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
> - Everything above this line is **Part A**, the human-authored S04 prompt, reproduced
>   verbatim (byte-identical to the upload).
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2. It was written at the end of S03, and it carries S03's
>   findings forward: `SESSION-03-REPORT.md` with its review addendum;
>   `entity-taxonomy.md` §9; D-022 to D-027.
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The
>   higher-level documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The human may edit Part B before S04 starts. It becomes immutable once S04 begins
>   (D-011).

## 01 — Session identity

- **Session:** S04
- **Title:** Relationship taxonomy
- **Type:** ARCHITECTURE
- **Milestone:** M1 — Domain + Evidence Foundation (`SESSION-ROADMAP.md` numbering, D-019)
- **Predecessor:** S03 — Entity taxonomy (merged to `main` at `1d0522c`)
- **Expected successor:** S05 — Source hierarchy and evidence policy
- **Complexity class:** medium to large (design, schema, tests; no new source retrieval
  expected)

## 02 — Mission

Define the Atlas relationship vocabulary as a relationship schema plus a reasoning
document. Each relationship type gets:

- a precise definition;
- a direction;
- typed endpoints;
- a level (between classes, or between instances);
- a way of handling time;
- an evidence expectation.

The result must make two things impossible: recording an edge because two names appear
in the same source, and recording a vague relationship such as `associated_with` where a
precise one exists.

## 03 — Why this session exists

- **The roadmap.** `SESSION-ROADMAP.md` S04 gives the mission "prevent accidental
  inference from co-occurrence". Its gate is "Every relationship has a clear semantic
  definition and evidence expectation."
- **Edges carry the intelligence.** MA §6.2: "Relationships are first-class records
  because supply-chain intelligence depends on edges".
- **Three later sessions stand on this vocabulary:**
  - S10 builds the first edges;
  - S06 must answer "What exactly supports this relationship?";
  - S14/S15 traverse edges to compute metrics.

  A vague verb damages all three.
- **S03 left facts waiting for a home.** S03 deliberately kept some facts out of entity
  records, and they have none until S04 defines them:
  - ownership and operation of facilities;
  - design, fabrication and packaging of products;
  - composition ("part of").
- **The human's learning.** Why "supplies", "fabricates" and "depends_on" are different
  claims, and why an edge needs different evidence from an entity.

## 04 — Current state

As of `main` @ `1d0522c`. Verify at start, and record the base and the `git branch -a`
result in the report (D-018 L-03).

- **Accepted entity model** (D-022 to D-025):
  - instantiable types: `company`, `facility`, `technology`, `component`, `product`,
    `jurisdiction`;
  - `institution` and `policy` are reserved (no schema);
  - `source`, `claim`, `event` and `relationship` are record kinds;
  - **S04 owns the relationship schema** (D-022);
  - S09 owns the event schema (D-022);
  - S08 creates the first product records (D-027).
- **Files:**
  - `schemas/entities.schema.json`;
  - `docs/architecture/entity-taxonomy.md`;
  - `tests/test_entity_schema.py` (uses the pinned `jsonschema`, D-026);
  - `tests/test_entity_taxonomy.py` (standard library);
  - `tests/fixtures/entities.json`.

  CI installs `requirements-test.txt`.
- **Facts already held by accepted entity fields.** A verb from the roadmap or MA could
  duplicate each of these. They are the one-home conflicts S04 must settle:
  - `facility.located_in`, `company.incorporated_in` and `company.headquartered_in`
    (claim-backed jurisdiction references) vs a `located_in` relationship (roadmap S04,
    MA §6.2);
  - `product.vendor` (identity) vs any "offers" or "sells" relationship;
  - `broader` on technology and component, and `product.instance_of` (taxonomy) vs any
    `is_a`, `subclass_of` or `instance_of` relationship. `entity-taxonomy.md` §3.3
    explains why taxonomy must stay out of the edge table;
  - `product.vendor_process_name` (FAB-05, TQ-07) vs a process qualifier on a
    fabrication edge;
  - `company.roles` (claim-backed, never derived from edges, D-024) vs edges that would
    imply a role.
- **Three verb lists that differ:**
  - MA §6.2;
  - `SESSION-ROADMAP.md` S04 "Focus";
  - `docs/research/domain-map.md` §3: dependencies DEP-01 to DEP-18, and the verbs marked
    † there.

  `baseline.md` §4 requires S04 to reconcile them.
- **No relationship vocabulary, schema or records exist.** No data records of any kind
  exist.
- **Open, but not S04's:**
  - D-014 and D-015 (source retrieval and tiers; S05);
  - S01's weekly gate;
  - the week-2 gate ("ontology and evidence policy understandable"), which falls after
    S05.
- **Next decision number:** D-028.

## 05 — Inputs and evidence

Documents, in this order:

1. `sessions/reports/SESSION-03-REPORT.md`, including the review addendum.
2. `docs/architecture/entity-taxonomy.md`:
   - §1 (rules R-1 to R-8);
   - §3 (types);
   - §4.2 (confusable pairs);
   - §4.3–4.4 (worked examples);
   - §7 (attribute contract);
   - §9 (what S03 left to S04).
3. `schemas/entities.schema.json`.
4. `docs/research/domain-map.md`:
   - §3: the DEP table, the structural vs contingent distinction, the columns "Evidence
     that would establish it" and "Likely non-public", and the † verbs;
   - §4: blurs B-1 to B-5;
   - §7.1: TQ-04, TQ-06, TQ-07, TQ-11.
5. `MASTER-ARCHITECTURE.md`:
   - §5.4 (the relationship record);
   - §5.5–5.6 (events, derived status);
   - §6.2 (verbs);
   - §18 (the six graph questions the model must be able to answer).
6. `SESSION-ROADMAP.md`: S04, S06, S09, S10, S15 and S17.
7. `docs/architecture/decisions.md` (D-020 to D-027) and `baseline.md` (§2, §4, §6).

Repository paths to inspect: `schemas/`, `tests/`, `docs/architecture/`, `.github/`.

**External research.** Not expected.

- Relationship definitions are design choices (`INTERPRETATION`).
- Where a definition depends on what an industry term covers (e.g. what an OSAT's
  packaging includes), cite the existing domain-map entry.
- Retrieve a new source only if no entry supports the definition. Follow D-014:
  retrieve the source raw, and record a blocked site as a gap.

**Audit findings to carry:**

- A-5: second homes;
- A-1: machinery before a used loop;
- S03's process lessons: fail first; deliberate breakage; invalid fixtures built by
  mutating a valid record; worked examples drawn from real S01 sentences.

## 06 — Required reasoning

Answer these before writing the schema. The answers go into
`relationship-taxonomy.md` and the decision records.

1. **Reconciliation.** Take every verb in MA §6.2, the roadmap's S04 list and domain map
   §3, including the † verbs. Give each exactly one disposition, with a reason:
   - adopt;
   - merge into another verb;
   - already an entity field;
   - an event;
   - a derivation;
   - reserved for S17;
   - excluded by a non-goal;
   - rejected as vague.
2. **One home.** For each entity field listed in §04, decide whether the field or a
   relationship is the home of that fact.
   - The default is the accepted field.
   - Moving a fact from a field to a relationship changes an accepted decision. That is
     a stop condition (§16).
3. **Level.** Some relationships connect classes (technology, component). These are
   structural, concept-level statements: HBM requires TSV (DEP-03). Others connect
   instances (company, facility, product). These are contingent, entity-level
   statements: a named foundry fabricates a named product (DEP-05).
   - May one verb serve both levels?
   - The two levels need different evidence (domain map §3).
4. **Activity verbs.** TQ-06 says: "Model each process step separately and record who
   performs it."
   - Are `manufactures`, `produces`, `fabricates` and `packages` distinct?
   - Which of them is an umbrella term, and therefore vague?
   - Where do assembly, test, stacking (`stacks_on`) and integration (`integrates`)
     belong?
   - Blur B-3 applies: foundries and memory makers also package.
5. **Dependency verbs.**
   - Are `depends_on`, `requires` and `uses` distinct?
   - Is a company-to-company `depends_on` a stored fact, or a derivation from supply
     edges? Derived values are not stored (R-8; CLAUDE.md §7).
   - Criticality is S15's (NG-11).
6. **Relationship vs event.** D-023 made Investment an event. For MA's `acquired` and
   `invests_in`, is ownership a relationship with its own claims and validity period, or
   is it derived from acquisition events (MA §5.6)? A relationship holds over an
   interval; an event happens at a date (`entity-taxonomy.md` §4.2).
7. **Relationship vs role.** Which edges would contradict a role? For example, a
   `fabless_designer` that operates a `wafer_fab`. Record such cases as a future
   semantic warning (Gate 3), never as an automatic correction (D-024).
8. **Unknown edges.** Take HBM-06 and DEP-01: "which maker's HBM goes into which product"
   is `not_publicly_determinable` from the product documentation retrieved.
   - How is that recorded without inventing an edge or a placeholder company?
   - A missing edge must never read as "no relationship".
   - `SESSION-ROADMAP.md` S10 rule: "No relationship is published without evidence or an
     explicit non-published/unverified state."
9. **Vendor-named processes on edges.** The CoWoS case (`entity-taxonomy.md` §4.2, §9).
   Options: a qualifier field on the packaging edge, a product attribute, or nothing in
   v1. The chip's fabrication process already lives in `product.vendor_process_name`.
   Do not create a second home for it.
10. **Endpoint constraints.** For each type, what are the allowed source and target
    entity types, and which `use_class` or `facility_kinds` do they need? For example,
    composition only between `constituent` components; production equipment is never
    part of a product.
11. **Direction and symmetry.** Is every relationship directed? Does v1 need symmetric
    relations (`competes_with`, `partners_with`) at all? Inverse readings (e.g.
    "fabricated by") are display text. They are never stored edges.
12. **Evidence expectation.** For each type, state:
    - what a source must show for the edge to exist: both parties, the activity, the
      object, and a date or period where relevant;
    - what is typically not public (domain map "Likely non-public" column).

    Which *source class* is preferred is S05's gate. S04 states *what the evidence must
    show*, not which tier it comes from.
13. **Time.** How `valid_from` and `valid_to` apply to edges. Announced plans are events
    and claims, not edges (SRC-014, `entity-taxonomy.md` §4.4).
14. **Policy and energy verbs.**
    - `restricted_by`, `regulated_by`, `supported_by`, `constrained_by` and `affected_by`
      need Policy, which is reserved until S17.
    - `supplies_power_to` is energy (NG-05).

    Reserve or exclude them. Never define an endpoint on a type that has no schema.

## 07 — Tasks

**Design**

1. Write the reconciliation table (§06 q1): every verb, one disposition each.
2. For each adopted type, write:
   - its definition;
   - its direction and its inverse reading (display only);
   - its allowed endpoints;
   - its level;
   - its handling of time;
   - its evidence expectation;
   - the aspects that are typically non-public;
   - what it must not be confused with.
3. Map every dependency DEP-01 to DEP-18 in domain map §3 to one of: a relationship type,
   an event, a derivation, or a recorded exclusion.
4. Work through at least three S01 dependencies as examples. Each is an illustration, not
   a record:
   - DEP-05: a fabless designer and its foundry (SRC-006, the NVIDIA/TSMC sentence);
   - DEP-01: a product uses HBM, and the supplier is `not_publicly_determinable`;
   - DEP-04: an announced plan is an event, not an edge.

**Implementation**

5. `docs/architecture/relationship-taxonomy.md`: the one home of the reasoning, the
   reconciliation and the DEP mapping.
6. `schemas/relationships.schema.json`: the one home of shapes and vocabulary values.
   Follow the S03 pattern: each vocabulary value is a `const` with its own `description`,
   plus an annotation listing the DEP IDs it covers.
7. `tests/fixtures/relationships.json`: fictional records only. Invalid cases are single
   JSON Pointer mutations of a valid base. At minimum, the schema must reject:
   - `associated_with`;
   - a wrong endpoint type;
   - an endpoint on a reserved type;
   - a relationship with no claims;
   - record-level `source_ids`;
   - an `is_a`-style edge;
   - a stored inverse edge;
   - a placeholder "unknown supplier" endpoint.
8. Tests:
   - `tests/test_relationship_schema.py` (behaviour, uses `jsonschema`);
   - `tests/test_relationship_taxonomy.py` (consistency, standard library). It checks
     that:
     - every verb in the three lists has exactly one disposition;
     - every DEP ID is mapped;
     - every endpoint type exists in `entities.schema.json`;
     - every decision cited exists.

     Parse Markdown tables by splitting cells, not with a regex (S03 lesson).

**Validation**

9. Run the new tests before the decisions exist, and confirm they fail. Then break the
   schema and the taxonomy deliberately in a scratch copy, in at least five different
   ways, and confirm each break is caught.

**Documentation**

10. Append decisions from D-028, each `proposed`.
11. Add rows to `docs/README.md`.
12. Update the baseline's state rows (§1 table, §4, §5), but only those that have become
    false. This is the practice the human confirmed at the S03 review.
13. Write `sessions/reports/SESSION-04-REPORT.md`.

## 08 — Explicit non-goals

- Relationship records or any other data: edges are S10's, entity records S07–S09's.
- Source hierarchy and preferred source classes (S05).
- The claim schema (S06).
- The event schema (S09, D-022).
- Policy-layer relationships (S17; Policy is reserved).
- Energy and networking edges (NG-04, NG-05).
- Metrics, criticality or concentration scores, and code that derives `depends_on`
  (S15; NG-11).
- A graph database or graph library (NG-07; MA §18).
- A record validator (`validate-data`, S06/S07). S04 tests its schema with fixtures only.
- Changing an accepted S03 decision, field or vocabulary without a decision record the
  human approved **first**.
- Editing the root documents, `M0-audit.md` or `domain-map.md`.
- Anything in `Eu-Digital-Policy` (NG-01).

## 09 — Constraints

- **Evidence:**
  - Part A's evidence rules apply. Model memory is not evidence.
  - Worked examples use only sentences already evidenced in domain-map entries.
  - Check each quoted anchor against the entry.
- **Claim labels:** `FACT | ATTRIBUTION | DERIVATION | INTERPRETATION | IMPLICATION`. Part
  A lists four; CLAUDE.md §6 adds `ATTRIBUTION` and takes precedence.
- **One home:**
  - No relationship may restate a fact held by an accepted entity field (§06 q2; L-05;
    R-8).
  - MA §5.4's example keeps `source_ids` on the relationship. This is replaced by
    claim-level provenance, following the D-025 precedent. Record the choice in a
    decision.
- **Tooling:**
  - `tools/` stays standard-library only.
  - Tests may use the pinned `requirements-test.txt` (D-026).
  - Adding any dependency needs a decision and the human's approval first.
- **Process:**
  - D-018 L-02: nothing is called a gate unless CI runs it.
  - L-04: no hand-typed counts.
  - L-08: keep "ran locally" apart from "CI result".
- **Portfolio:** the session should demonstrate semantic data modelling and inference
  control, not verb-list length.

## 10 — Agent responsibilities

| Agent | May write | Notes |
|---|---|---|
| Knowledge Architect | `docs/architecture/relationship-taxonomy.md`, `schemas/relationships.schema.json`, `docs/architecture/decisions.md` (append) | vocabulary, endpoints, IDs, one-home rulings |
| Data Auditor | `tests/`, `tests/fixtures/` | schema behaviour and consistency tests |
| Verifier | S04 report | checks every quoted anchor in the worked examples against the domain map; may downgrade, may not invent evidence |
| Editorial | `docs/README.md`, `baseline.md` state rows, `README.md` | only to correct statements that have become false |

All other agents are inactive. No agent writes outside `schemas/`, `tests/`,
`docs/architecture/`, `docs/README.md`, `README.md` and `sessions/reports/`.
`.github/` and `requirements-test.txt` change only if a decision requires it.

## 11 — Data and evidence rules

- **Endpoints:** only the instantiable entity types of D-022, as listed in
  `entities.schema.json` `vocab_entity_type`.
  - Reserved types and the record kinds source and claim are never endpoints.
  - Whether an edge may point to an event is a §06 decision.
- **Allowed relationship types:** only those S04 adopts through a decision record.
  - Reject `associated_with`, `related_to`, `linked_to`, and any verb that lacks a
    definition and an evidence expectation.
- **Record fields** (to decide and record):
  - an ID, with a prefix (MA §5.4 uses `rel-`);
  - `relation_type`;
  - source and target IDs, typed by prefix;
  - `claim_ids` (at least one, D-025 pattern);
  - `valid_from` and `valid_to` (partial dates);
  - any per-type qualifier the reasoning justifies.
  - Forbidden: record-level `source_ids`, free-text notes, a stored status, and a
    confidence score.
- **Provenance:** every relationship cites at least one claim. Claim type and evidence
  status live on the claim (L-06).
- **Unknown:** a missing edge means "not recorded", never "no relationship". Explicit
  states follow MA §5.7.
- **Time:** plans and announcements are events.
- **Nothing derived is stored:** no transitive edges, no inverse edges, no computed
  `depends_on`.

## 12 — Implementation rules

- **Files S04 may create:**
  - `docs/architecture/relationship-taxonomy.md`;
  - `schemas/relationships.schema.json`;
  - `tests/test_relationship_schema.py`;
  - `tests/test_relationship_taxonomy.py`;
  - `tests/fixtures/relationships.json`;
  - `sessions/reports/SESSION-04-REPORT.md`.
- **Files S04 may modify:**
  - `docs/architecture/decisions.md` (append only);
  - `docs/README.md`;
  - the `baseline.md` state rows;
  - `README.md`.
- **Approach:** mirror S03.
  - The document holds the reasoning, and the schema holds shapes and vocabulary.
  - Each vocabulary value is a `const` with a `description`.
  - Invalid fixtures are mutations of a valid base.
  - Consistency tests parse tables by splitting cells.
- **Shared definitions:** reuse `claim_ids`, `partial_date` and the entity reference
  patterns from `entities.schema.json` through `$ref`, instead of copying them (one
  home). Prove in a test that `jsonschema` resolves the cross-file reference.
- **Prohibited:**
  - graph databases or libraries;
  - stored inverse or transitive edges;
  - a stored `depends_on` between companies;
  - generic verbs.
- **Entity-schema changes:** only if a §06 answer requires one. It needs a decision
  record, and the human's approval **before** the edit (§16).

## 13 — Verification plan

- **At start:**
  - `python -m unittest discover -s tests` and `python tools/validate_repo.py`;
  - record the base commit and the `git branch -a` result.
- **Fail first:** the consistency tests fail until the decisions and the mapping exist.
- **Behaviour:**
  - the valid fixtures pass;
  - each invalid mutation fails at the path it targets. Read each error message.
- **Deliberate breakage:** at least five distinct breaks in a scratch copy, each caught.
- **Environment:** a fresh virtualenv from `requirements-test.txt`, with the installed
  set compared to the pins.
- **CI:** report its result separately from local results, or say it was not observed
  (L-08).
- **Not applicable:** data validation (no records), browser, accessibility,
  performance.

## 14 — Evaluation requirements

The report records:

- decisions and rejected verbs, with reasons;
- deviations from Part A or Part B;
- assumptions invalidated, especially any S03 field the reasoning wanted to move;
- new debt;
- unresolved questions.

It also notes whether having a Part B made a difference. S04 is the first session since
S01 with a prompt in SPEC §2 form, which S02 and S03 both recorded as a gap.

## 15 — Acceptance criteria

1. Every verb in MA §6.2, the roadmap's S04 list and domain map §3 (including the †
   verbs) has exactly one disposition with a reason. Machine-checked.
2. Every adopted type states all of the following:
   - definition;
   - direction;
   - typed endpoints;
   - level;
   - handling of time;
   - evidence expectation;
   - typically non-public aspects;
   - what it must not be confused with.
3. Every DEP-01 to DEP-18 maps to a relationship type, an event, a derivation or a
   recorded exclusion. Machine-checked.
4. The schema rejects `associated_with` and its generic synonyms. There is a fixture for
   each.
5. No adopted relationship duplicates an accepted S03 entity field.
   - Each field listed in §04 appears in the reconciliation with its ruling.
   - Any move from a field to a relationship has a decision the human approved.
6. Every endpoint type is an instantiable type in `entities.schema.json`. None is
   `policy`, `institution`, `source` or `claim`. Machine-checked.
7. No energy or networking verb is adopted.
8. The relationship schema requires at least one claim ID per record, and allows no
   record-level `source_ids`.
9. The tests and the Gate 0 validator pass in a fresh virtualenv. The CI result is
   observed, or reported as not observed.
10. The report satisfies SPEC §5 and Part A's list. New decisions are appended as
    `proposed`.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- a §06 answer requires changing an accepted S03 decision, field or vocabulary. Put the
  proposal to the human first;
- a v1 relationship could never be evidenced publicly. Record the pattern with
  `not_publicly_determinable`; do not invent a proxy edge;
- v1 seems to need a policy, energy or networking endpoint (a non-goal);
- a new dependency seems necessary;
- the verb lists cannot be reconciled without editing MA text. Record the conflict; do
  not edit MA;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

## 17 — Deliverables

- `docs/architecture/relationship-taxonomy.md`
- `schemas/relationships.schema.json`
- `tests/fixtures/relationships.json`, `tests/test_relationship_schema.py`,
  `tests/test_relationship_taxonomy.py`
- `docs/architecture/decisions.md`: D-028 onward, `proposed`
- `docs/README.md` rows; `baseline.md` state rows only where they have become false
- `sessions/reports/SESSION-04-REPORT.md`

## 18 — Handoff

S04's report must hand S05 the following:

- **Completed work:** the relationship vocabulary, its schema and its tests.
- **For S05:** a table of evidence expectations, one row per relationship type, plus the
  entity identity-evidence expectation from S03 (`identity_claim_ids`). S05's gate,
  "Every material claim type has a preferred source class", assigns a preferred source
  class to each row.
- **Open issues:**
  - human approvals;
  - D-014/D-015, which fall to S05;
  - the rules left for `validate-data` (S06/S07): references resolve, endpoint records
    exist, role and edge conflicts are flagged.
- **Recommended next decision:** the human reviews the S04 decisions before S05, because
  S05's source classes attach to S04's relationship types.
- **Files for S05 to read first:**
  1. the S04 report;
  2. `relationship-taxonomy.md` (evidence expectations);
  3. `entity-taxonomy.md` §7;
  4. `docs/research/source-register.md`;
  5. D-014, D-015.
