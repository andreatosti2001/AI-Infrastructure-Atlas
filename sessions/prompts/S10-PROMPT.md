# AI-Infrastructure-Atlas — S10 Session Prompt

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

Supply-chain edges

Create the first auditable relationships.

### Human focus

- inspect at least 10 relationships end-to-end from source to published edge.

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
> - Everything above this line is **Part A**. As for S07 to S09, no upload was made: Claude
>   assembled Part A at the end of S09, after the human agreed to the edge ordering Claude
>   suggested ("I agree", 2026-10-02).
>   - The operating contract, report list and headings are byte-identical to S09's Part A.
>   - The session-specific mission and the human focus are copied verbatim from the
>     operational roadmap's week-4 entry for S10 (`AI-Infrastructure-Atlas-Operational-Roadmap.md`,
>     "S10 — Supply-chain edges"). That entry also marks M2 complete after S10.
>   - **The human confirmed Part A as assembled** before S10 started ("Report closes M2;
>     confirm A (Recommended)", 2026-10-02).
> - Part B is Claude's elaboration of Part A into the 18 sections of
>   `SESSION-PROMPT-SPEC.md` §2, written after S09 (`SESSION-09-REPORT.md` with its two
>   addenda, `facility-dataset.md`, D-078 to D-088).
> - Part B adds detail only. **If the two ever conflict, Part A governs.** The higher-level
>   documents (`CLAUDE.md`, `MASTER-ARCHITECTURE.md`) govern both.
> - The prompt becomes immutable once S10 begins (D-011).
> - **Answered before S10 started (2026-10-02, end of S09):** H-1 ("I agree", to Claude's edge
>   ordering) and H-2 to H-7, each with Claude's recommendation; H-0 had nothing open. Do not
>   ask them again; record them in decisions (`proposed`, citing the answer).

## 01 — Session identity

- **Session:** S10
- **Title:** First supply-chain edges (operational roadmap: "Supply-chain edges")
- **Type:** IMPLEMENTATION (`SESSION-ROADMAP.md`; `PROMPT-REGISTRY.md`), with research.
- **Milestone:** M2 — Canonical Dataset (`SESSION-ROADMAP.md` numbering, D-019). S10 is M2's
  last session; M2 is complete after it (operational roadmap).
- **Predecessor:** S09 — Facility dataset (2 facilities, 4 events; D-078 to D-088, all
  accepted; S08's D-070 and D-076 accepted at its end).
- **Expected successor:** S11 — First end-to-end vertical slice (M3).
- **Complexity class:** large: the first relationship records, the relationship checks
  that arrive with them (V-2, V-3, V-5 to V-8), and the navigation the gate asks for.

## 02 — Mission

Create a small set of canonical relationship records, each resting on claims that meet
`relationship-taxonomy.md` §5 for its type, and make them navigable from relational files,
so that the human can follow at least 10 of them from source sentence to published edge.

The result must make five things impossible:

- an edge from co-mention (RR-1), or one whose claims do not meet §5 for its type;
- a `fabricates` edge resting on a process name alone, unless it is a `DERIVATION` (ER-1);
- a product edge resting on a company-level statement (ER-9);
- an edge from a plan or announcement (ER-8; RR-8);
- a placeholder endpoint, a stored inverse, a stored `depends_on`, or a confidence score
  (RR-3, RR-5, RR-7; D-028).

## 03 — Why this session exists

**The roadmap.** `SESSION-ROADMAP.md` S10: "Connect canonical entities through a small
auditable set of supply-chain relationships." Rule: "No relationship is published without
evidence or an explicit non-published/unverified state." Gate: "Graph-like navigation is
possible using relational data without introducing a graph database." Primary gate
(`PROMPT-REGISTRY.md`): "auditable supply edges".

**The governing question needs edges.** "Where are the critical dependencies behind AI
compute, and what evidence supports that assessment?" is answered by edges, not entity
pages (MA §6.2, §18). S15's dependency metrics will be derived from them.

**Earlier decisions that land here:**

- D-028 to D-033: the relationship record, vocabulary, unknown suppliers, the D-032 limits.
- `relationship-taxonomy.md` §15: V-2, V-3 and V-5 to V-8 arrive with the first edges
  (L-05, L-09).
- S07 (`company-dataset.md` §14): `supplies` from the filings' supplier paragraphs (NVIDIA
  p.8), `owns` from subsidiary lists; the AWS legal entity.
- S08 (`concept-dataset.md` §12): product edges (`incorporates`, `fabricates`, `packages`,
  `designs`) for the 3 products; class-level `requires`/`has_part` candidates.
- S09 (`facility-dataset.md` §5, §13): `operates` SK hynix → M16 only as a `DERIVATION`;
  no `owns` candidate meets §5; TSMC's 20-F carried into S10 (RA-4).

## 04 — Current state

As of `main` after the S09 merge. Verify at start, and record the base, `git branch -a` and
`git ls-remote` in the report (D-018 L-03). **This prompt must be on `main` before S10
starts.**

**Accepted model:** entity schema (D-022 to D-027); relationship schema (D-028 to D-033);
source policy with event rows (D-034 to D-043, D-084); claim model (D-044 to D-053);
company, concept and facility datasets (D-054 to D-088, all accepted).

**Data at the start** (as measured at the S09 final commit, `b27f0a9`):

- 50 source records; 114 canonical claims; no staging claim or record;
- 8 companies, 4 jurisdictions, 7 components, 9 technologies, 3 products, 2 facilities,
  4 events; **no relationship record**.

**Checks at the start:** 221 tests; `validate-data` (VD-1 to VD-13; V-1, V-4, V-9, V-10,
CE-1, ID-1, J-1, CI-1, DEF-1, DEF-2, B-1, PI-1, IO-1, FI-1, HQ-1, FK-1, CAP-1; EV-1 to EV-4,
EI-1), ST-1 and `validate-freshness` (F-1) in CI.

**Open items S10 inherits:** TSMC's 20-F (RA-4); the AWS legal entity
(`company-dataset.md` §14); S01's weekly gate; S05 debt (the class table vs the matrix;
SRC-023 not re-read).

**Not S10's:** metrics, concentration or `depends_on` (S14–S15); policy (S17); a UI (S11).

**Next decision number:** D-089.

## 05 — Inputs and evidence

**Documents, in this order:**

1. `sessions/reports/SESSION-09-REPORT.md`, with both addenda.
2. `docs/architecture/relationship-taxonomy.md` §1 (RR-1 to RR-10), §2, §4, §5, §9, §10,
   §11, §12, §15; `schemas/relationships.schema.json`.
3. `docs/research/source-policy.md` §4 (standing), §6 (ER-1, ER-2, ER-8, ER-9), §7 (the
   `rel:*` rows), §11, §12.
4. `docs/architecture/facility-dataset.md` §5, `concept-dataset.md` §7, §12,
   `company-dataset.md` §14 (the edge candidates each session left).
5. `docs/architecture/claim-model.md` §1, §4, §8 (the search record), §12 (the trace).
6. `docs/architecture/decisions.md`: D-028 to D-033, D-037, D-049, D-072 to D-075, D-082.

**External research: expected, narrow.** Re-retrieve each registered source before citing
it again (D-075); one RA-4 list at the start (TSMC's 20-F first). Web search only discovers
URLs. Candidate sentences (`INTERPRETATION`; the session reads each):

- NVIDIA's 10-K supplier paragraph (`src-024` p.8): `supplies` from named suppliers;
- the H100 and Trainium2 technical pages (`src-042`, `src-043`): `incorporates` HBM;
  `designs` only where a sentence states design;
- NVIDIA's "TSMC 4N" sentence (`claim-h100-process-name`): `fabricates` as a `DERIVATION`
  (ER-1, `relationship-taxonomy.md` §12 example 1);
- SK hynix's filing (`claim-sk-hynix-production-plants-icheon-cheongju`,
  `claim-sk-hynix-m16-completed-icheon`): `operates` as a `DERIVATION` (D-082);
- the ECP report (`claim-ecp-hbm-definition`): HBM `requires` 3D die stacking, if the
  sentence states necessity for the class.

**Audit findings to carry:** L-01, L-02, L-04, L-05, L-09; S07 to S09 lessons: read the
sentence; plan RA-4 at the start; re-retrieve before citing; write the checks before the
data; ask flagged rulings separately, with a rule for an unticked box; ask before editing
a file the prompt does not list; never push after a failed gate.

## 06 — Required reasoning

Answer these before writing edges, in a document (§07 task 1) and decisions.

1. **Which edges** (H-1)? For each candidate: the type, the endpoints (canonical records),
   the sentence, and whether it meets §5 as `FACT`, only as `DERIVATION`, or not at all.
   Count the edges for the human's 10-edge review, including the two borderline cases
   (TSMC → H100, SK hynix → M16).
2. **Edge IDs.** A stable, non-editorial rule (type and endpoints; `item` where the type has
   one), machine-checked, as FI-1 and EI-1 are.
3. **Level and endpoints.** V-2 from the schema's endpoint kinds and `use_class`; class
   edges carry no dates (`relationship-taxonomy.md` §10).
4. **Time.** `valid_from`/`valid_to` only where the claims give a period; a missing period
   is not "always" (§10). Which `rel:*` rows are `time_sensitive` (F-1 extends).
5. **Unknowns.** `incorporates.supplier`: `not_researched` vs `not_publicly_determinable`
   with a search record (ER-3, D-049). No placeholder (RR-7).
6. **Company records.** A `supplies` or `owns` edge may need a company the seed lacks
   (a supplier, a subsidiary). New company records follow D-054 to D-057 or the edge
   waits (H-3).
7. **Navigation (the gate, H-5).** Which questions (MA §18: "What depends on this
   component?", "Who supplies this component?", "What evidence supports the edge?") are
   answered, from the JSON files, by what standard-library code.
8. **Checks:** V-1 to V-9 for edges (with V-7, V-8 as warnings, D-033), V-10 for the `rel:*`
   rows, CE-1 for edges, the edge ID rule, F-1, the trace. Hand-apply each to real edges
   first (L-09).
9. **The human's review:** at least 10 edges, each from source sentence to published edge,
   with the flagged rulings asked separately.

## 07 — Tasks

**Design**

1. `docs/architecture/edge-dataset.md` (or a name the session justifies): the answers to
   §06, referencing the taxonomy, policy and claim model by section, never restating them.

**Research**

2. Access probe; one RA-4 list (TSMC's 20-F, and anything else refused).
3. Re-retrieve registered sources before citing them (D-075); new sources from `src-051`.

**Implementation**

4. Edge claims in `data/staging/claims.json`, verified at their locators; new company
   records only under H-3.
5. Relationship records in staging (`data/staging/relationships.json`, H-2).
6. Checks (§06 q8) in CI, with fixtures and planted faults, written before the data.
7. Navigation (H-5) with tests.
8. Promotion on the human's verdicts.

**Validation**

9. Fail first; then at least eight deliberate breaks, each showing which tests fail.
   Include: an edge from co-mention; `fabricates` from a process name as a `FACT`; a
   product edge from a company-level sentence; an edge from an announcement; a placeholder
   endpoint; a stored inverse or `depends_on`; a class edge with a date; a canonical edge
   citing a staging claim; an edge with an endpoint of the wrong kind.

**Documentation**

10. Decisions from D-089, each `proposed`; `docs/README.md`, the baseline state rows,
    `README.md`, `contracts.md` paths.
11. `sessions/reports/SESSION-10-REPORT.md`, with the review sheet, the trace of each
    canonical edge, and the M2 completion statement.

## 08 — Explicit non-goals

- Metrics, shares, concentration, `depends_on` or any score (S14–S15).
- Edge types outside the accepted vocabulary, or a change to it, without a decision the
  human approves first (§16).
- Vendor-named packaging processes (CoWoS) and constituent-level fabrication (D-032).
- Policy verbs (S17). Facility kinds beyond the schema (D-088 stays a proposal).
- A graph database, a database server, a UI, an agent runtime, an external API.
- Coverage beyond H-1; companies beyond H-3.
- Promoting anything without the human's verdict.
- Editing the root documents, the taxonomies, `domain-map.md`, the frozen register or
  migrated values. Anything in `Eu-Digital-Policy`.

## 09 — Constraints

- **Evidence:** Part A's rules, `source-policy.md` and `claim-model.md`; §5 of the taxonomy
  for each type; ER-1, ER-2, ER-8, ER-9 apply.
- **One home:** an edge never restates an entity field (RR-4); no inverse (RR-3); no derived
  edge (RR-5).
- **Unknown ≠ zero:** a missing edge means "not recorded" (RR-7).
- **Tooling:** `tools/` standard library (D-003, D-026); PDF extraction in a scratch
  environment; no new dependency without an approved decision.
- **Process:** L-02, L-04, L-08; gates run before any push.

## 10 — Agent responsibilities

As `docs/agents/contracts.md` (accepted, D-052; paths updated in S07 to S09). The
Extractor's writes extend to `data/staging/relationships.json`, recorded in the report. The
Change Detector stays inactive.

| Agent | May write | Notes |
|---|---|---|
| Source Scout | the report | discovery only |
| Extractor | `data/sources.json` (new records), `data/staging/*.json` | provenance on every candidate |
| Verifier | verification fields of staging claims; the report | re-checks its own locators |
| Knowledge Architect | the design document, `decisions.md` (append) | edge ID rule, one-home rulings |
| Data Auditor | `tests/`, `tests/fixtures/`, `tools/` | the checks of §06 q8; navigation code |
| Editorial | `docs/README.md`, baseline rows, `README.md`, `contracts.md` (paths only) | the new state only |

## 11 — Data and evidence rules

- **Canonical records:** relationships; new companies only under H-3.
- **Allowed relationship types:** the accepted vocabulary, within H-1.
- **Required source tier:** the `rel:*` rows of `source-policy.md` §7, with the standing
  each requires.
- **Provenance:** every edge cites claims in the S06 shape (RR-6).
- **Temporal:** periods only from claims; `time_sensitive` rows checked by F-1.
- **Confidence:** no numeric values.
- **Unknown or unverified:** `not_researched`; `not_publicly_determinable` only with a search
  record (ER-3); access gaps support nothing (SP-7).

## 12 — Implementation rules

**May create:** the design document; `data/relationships.json` and its staging copy;
tests and fixtures; a standard-library navigation tool (H-5); `SESSION-10-REPORT.md`.

**May modify:** `data/sources.json` (new records); `data/staging/claims.json`,
`data/claims.json` (promotion); the company files (only under H-3);
`tests/test_data_*.py`, `tests/test_freshness.py`, `tests/test_trace.py`;
`tools/trace.py`; `decisions.md` (append); `docs/README.md`, baseline rows, `README.md`,
`contracts.md` (paths).

**Approach:** mirror S07 to S09. Rules are read from their homes (endpoint kinds from the
schema, rows from `source-policy.md` §7, evidence expectations from the taxonomy §5),
never copied.

**Prohibited:** a hard-coded list of edges or rows in a test; a stored inverse, a stored
`depends_on`, a stored status or score; a graph library or database; a hand-written JSON
Schema validator.

**Schema changes to accepted files:** none. If §06 needs one, stop (§16).

## 13 — Verification plan

- **At start:** the full suite and Gate 0, logged; base, `git branch -a`, `git ls-remote`;
  this prompt on `main`.
- **Environment:** a fresh virtualenv from the pins, installed set compared with the pins.
- **Fail first;** then the breaks of §07 task 9.
- **Manual evidence check:** the Verifier reads every anchor's sentence; the human reviews
  at least 10 edges end-to-end.
- **Trace:** each canonical edge, pasted in the report.
- **Navigation:** each H-5 question answered on the real edges, output in the report.
- **CI:** reported separately from local results (L-08).
- **Not applicable:** browser, accessibility, performance.

## 14 — Evaluation requirements

The report records decisions and rejected alternatives (the edge ID rule, each borderline
ruling, the navigation design); deviations; invalidated assumptions (a candidate that fails
§5); new debt; unresolved questions; the human's verdicts verbatim; and whether M2's
deliverables are met.

## 15 — Acceptance criteria

1. Every canonical edge validates against the unchanged relationship schema and cites only
   canonical claims.
2. Every canonical edge's claims meet `relationship-taxonomy.md` §5 for its type, or the
   edge is a `DERIVATION` the human approved; none rests on co-mention, a plan or a
   company-level sentence for a product edge.
3. V-1 to V-10 and CE-1 run on edges in CI; V-7 and V-8 report warnings.
4. Every edge ID follows a written rule, machine-checked.
5. No placeholder endpoint, inverse, `depends_on`, score or graph database exists.
6. The H-5 questions are answered from the JSON files by tested standard-library code.
7. The human reviewed at least 10 edges end-to-end; their verdicts are verbatim in the report.
8. Every new source has class, retrieval, hash and dates; access gaps are listed; RA-4
   files stay outside the repository.
9. Tests and Gate 0 pass in a fresh virtualenv; CI observed or reported as not observed.
10. The report satisfies SPEC §5 and Part A; new decisions appended as `proposed`; the M2
    completion is stated against MA §22 and the roadmap.

## 16 — Stop conditions

Stop and report, rather than improvise, when:

- an edge would need a relation type, qualifier or endpoint kind the accepted schema lacks;
- a candidate meets §5 only by an inference not covered by ER-1 or an approved ruling;
- an endpoint has no canonical record and H-3 does not allow one;
- a source is reachable only by circumvention, or an anchor cannot be re-read (SP-7);
- promoting anything would happen without the human's verdict;
- any condition in SESSION-PROMPT-SPEC §2.16 or CLAUDE.md §18 applies.

**Human decisions already taken** (2026-10-02, at the end of S09; Claude's recommendation
first in each list). Do not ask them again; stop only if a condition cannot be met.

- **H-0 — the S09 review:** nothing open. D-078 to D-088 were accepted in S09, and S08's
  D-070 and D-076 at its end.
- **H-1 — edge scope and order:**
  - *(recommended)* product and company edges first (`supplies` from filings,
    `incorporates`, `designs` where stated, `fabricates` TSMC → H100 as a `DERIVATION`);
    then `operates` SK hynix → M16 as a flagged ruling; class-level `requires`/`has_part`
    last, only where an originator states necessity; about 10–12 edges;
  - class-level edges first;
  - facility edges only.
  - *Answer:* "I agree" (2026-10-02, end of S09, to Claude's suggestion of the first option).
- **H-2 — layout:**
  - *(recommended)* one file, `data/relationships.json`, with a staging copy (D-055,
    D-087 pattern; the relation type is a field);
  - one file per relation type.
  - *Answer* (asked with H-6): "One file, review in S10 (Recommended)".
- **H-3 — new company records for edge endpoints:**
  - *(recommended)* allowed only for a supplier or subsidiary an edge needs, by the D-054
    to D-057 rules, reviewed with the edges;
  - none: an edge whose endpoint is missing waits.
  - *Answer:* "Only when an edge needs it (Recommended)".
- **H-4 — sources and RA-4:**
  - *(recommended)* re-retrieve the registered sources first; one RA-4 list (TSMC's 20-F
    first); paywalled sources stay gaps;
  - registered sources only, no new retrievals.
  - *Answer* (asked with H-5): "Re-retrieve + RA-4; nav tool (Recommended)".
- **H-5 — navigation (the gate):**
  - *(recommended)* a standard-library tool reading the JSON files that answers "what
    depends on X", "who supplies X", "who does what to X" and "what supports this edge"
    (through the trace), with tests;
  - extend `tools/trace.py` only;
  - DuckDB now (S14's, and a new dependency).
  - *Answer* (asked with H-4): "Re-retrieve + RA-4; nav tool (Recommended)".
- **H-6 — when records become canonical:**
  - *(recommended)* review inside S10, as S07 to S09;
  - after the session.
  - *Answer* (asked with H-2): "One file, review in S10 (Recommended)".
- **H-7 — M2 close:**
  - *(recommended)* the S10 report states M2's completion against the roadmap and MA §22,
    and lists what M3's audits (S12, S13) should examine first;
  - a separate M2 audit document in S10.
  - *Answer* (asked with Part A): "Report closes M2; confirm A (Recommended)".
- **Part A:** confirm as assembled, or amend.
  - *Answer:* "Report closes M2; confirm A (Recommended)".

## 17 — Deliverables

- the design document;
- new source records; edge claims; relationship records (staging and canonical); new
  company records only under H-3;
- the edge checks, navigation, tests and fixtures;
- `decisions.md`: D-089 onward, `proposed`;
- `docs/README.md`, baseline rows, `README.md`, `contracts.md` paths;
- `sessions/reports/SESSION-10-REPORT.md`.

## 18 — Handoff

S10's report must hand S11 (First end-to-end vertical slice; "Build one complete user
journey from source → entity → relationship → visualization → evidence"):

- **Completed work:** the canonical edges, the edge checks, the navigation.
- **For S11:** the journey's first question and the edges it walks; which trace and
  navigation outputs a page would render.
- **Open issues:** anything H-1 to H-7 left open; TSMC if still missing; the AWS legal
  entity; S01's weekly gate; S05 debt.
- **Recommended next decision:** the user journey S11 builds first.
- **Files for S11 to read first:** the S10 report; the S10 design document;
  `relationship-taxonomy.md` §2, §4; MA §19; `claim-model.md` §12.
