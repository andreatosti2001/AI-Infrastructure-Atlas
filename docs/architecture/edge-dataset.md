# Edge dataset — the first relationship records

**Status:** PROPOSED (S10): D-089 to D-099. Four rulings were taken by the human at the start of
S10 (2026-10-02, §1): the class edge from a definition (D-091), the TSMC → H100 gap (D-092), the
AWS designer endpoint (D-093) and the RA-4 request for TSMC's 20-F (§11).
**Session:** S10 · **Date:** 2026-10-02
**Inputs:**
- `relationship-taxonomy.md` §1 (RR-1 to RR-10), §2 (types, kind constraints), §4, §5
  (evidence expectations), §9 (unknowns), §10 (time), §11 (role warnings), §12 (worked
  examples), §15 (V-1 to V-9);
- `../research/source-policy.md` §4 (standing), §6 (ER-1, ER-2, ER-3, ER-8, ER-9), §7 (the
  `rel:*` rows), §11 (RA-1 to RA-7), §12 (freshness);
- `claim-model.md` §1, §4, §8 (the search record), §12 (the trace);
- `company-dataset.md` §3, §4, §9, §14; `concept-dataset.md` §7, §12; `facility-dataset.md`
  §5, §13;
- the S10 prompt, Part B, with the human's answers H-0 to H-7 and the four answers given at
  the start of S10.

**Schemas:** unchanged. Edges follow
[`schemas/relationships.schema.json`](../../schemas/relationships.schema.json) as accepted in S04.
**Data:** [`data/relationships.json`](../../data/relationships.json) (canonical) and
[`data/staging/relationships.json`](../../data/staging/relationships.json) (staging), one file
with the relation type as a field (H-2, D-098).

**One home for each kind of statement:**

- **The schema** holds the record shape, the relation-type vocabulary, each type's endpoint
  types and the inverse readings.
- **`relationship-taxonomy.md`** holds why each type exists, its level, its kind constraints
  (§2) and what a source must show (§5). This document cites them and never restates them.
- **`source-policy.md` §7** holds which classes and standing each `rel:*` row accepts, and
  whether it is `time_sensitive`.
- **This document** holds the reasoning for the first edges: which candidates became edges and
  why the others did not, the edge ID rule, the evidence guards and their word table, the
  navigation questions, and the record-level checks.
- **The records** hold the edges, and **the claims** hold the sentences and sources. Nothing in
  this document is a value of a record.
- **Checked by** `tests/test_data_relationships.py`, `tests/test_freshness.py`,
  `tests/test_data_schema.py`, `tests/test_navigate.py` and `tests/test_trace.py`.

**Claim labels.** The rules are the Atlas's design (`INTERPRETATION`), and their consequences
are `IMPLICATION`. What a source says is cited through a claim in `data/`, never stated here as
a fact.

---

## 1. Scope: which candidates became edges (H-1)

**Rule** (D-089). A candidate becomes an edge only when its claims meet
`relationship-taxonomy.md` §5 for its type, as `FACT`, or as a `DERIVATION` that ER-1 or an
approved ruling covers; when both endpoints (and the `item`) are records; and when the checks
of §10 pass. H-1's order was followed: product and company edges, then `operates` for M16,
then class edges.

**Rulings taken at the start of S10** (2026-10-02, verbatim):

| Question | Answer | Effect |
|---|---|---|
| RA-4: re-supply TSMC's 20-F? | "Re-supply it (Recommended)" | §11 |
| Stop condition: "HBM requires 3D die stacking" read out of a definition | "Allow, as DERIVATION (Recommended)" | D-091 |
| TSMC → H100 `fabricates` fails F-1 | "Gap until fresh evidence (Recommended)" | D-092 |
| Which endpoint for "AWS-designed"? | "company-amazon-com, as D-074 (Recommended)" | D-093 |

**Edges** (staging until the human's review, §9):

| Edge | Type | Claim | §5 met as | Note |
|---|---|---|---|---|
| `rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory` | `incorporates` | `claim-h100-hbm-stacks` | `FACT` (party, technical documentation) | both H100 models the page describes carry HBM (SXM5: HBM3; PCIe: HBM2e). HBM3 and HBM2e are generations of the HBM class, not classes (`relationship-taxonomy.md` §12, example 2). `supplier`: `not_researched` (§5) |
| `rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory` | `incorporates` | `claim-trainium2-hbm-capacity` | `FACT` (party, technical documentation) | a table row, cells read in order. `supplier`: `not_researched` |
| `rel-company-amazon-com-designs-product-amazon-com-trainium2` | `designs` | `claim-aws-designed-trainium2` | `FACT` (party, press release, an acceptable class) | "AWS-designed" states design by a named firm (ER-2). The endpoint is the AWS alias of `company-amazon-com` (D-093) |
| `rel-company-sk-hynix-operates-facility-kr-m16` | `operates` | `claim-sk-hynix-operates-m16` | `DERIVATION` (D-082, D-099) | **flagged ruling**: SK hynix states it operates its production plants in 이천; M16 is its plant in 이천. The plants are not listed one by one |
| `rel-component-high-bandwidth-memory-requires-technology-3d-die-stacking` | `requires` | `claim-hbm-requires-3d-die-stacking` | `DERIVATION` (D-091) | **flagged ruling**: necessity read out of the ECP definition of HBM, approved for S10 by the human at the start |

**Candidates that are not edges** (the sentences were read; IDs are the claims or sources):

| Candidate | Type | Sentence | Why not |
|---|---|---|---|
| TSMC → H100 | `fabricates` | `claim-h100-process-name`, via the staged `claim-tsmc-fabricates-h100` (ER-1) | meets §5 only as a `DERIVATION`, but `rel:fabricates` is `time_sensitive` and the product-level evidence is dated 2025-07-22 (`src-042`, `src-051`), more than the §12 horizon before its use. F-1 fails. The human chose a gap (D-092). NVIDIA's live Hopper page names TSMC 4N for the architecture, not the product (D-073 logic) |
| SK hynix, Micron → NVIDIA | `supplies` | `src-024` p.8: "We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung" | the `item` is "memory" (ER-9: exactly as broad as the source), and no memory component record exists. HBM would be narrower than the sentence |
| TSMC → NVIDIA | `supplies` | `src-024` p.8: "We utilize foundries, such as … TSMC … to produce our semiconductor wafers" | a manufacturing service on the customer's own product is `fabricates`, not `supplies` (`relationship-taxonomy.md` §4.9), and the sentence is company-level (ER-9) |
| Carl Zeiss SMT GmbH → ASML | `supplies` | `src-029` p.322: "Carl Zeiss SMT GmbH is our single supplier, and we are their single customer, of optical columns for lithography systems" | no "optical column" component record, and no Zeiss company record (§6) |
| ASML → TSMC | `supplies` | `src-029` p.173: "we were honored to receive the TSMC Supplier ‘Excellence in Green Manufacturing’ Award" | no item is named; an award is not a stated supply relation (RR-1) |
| ASML → Micron | `supplies` | `src-029` p.118: Micron Technology in ASML's remuneration reference group | co-mention (RR-1) |
| NVIDIA → H100 | `designs` | `claim-h100-identity`: "our ninth-generation data center GPU designed to deliver …" | states what the GPU is designed for, not who designed it (ER-2). NVIDIA's H100 product page and the 2022 H100 PCIe product brief name no designer either |
| Amazon → Trainium2 | `designs` (second sentence) | `src-028` p.5: "Our second version of our custom AI silicon (Trainium2)" | "custom" is not a statement of design work (ER-2); not used. The release sentence suffices |
| Amkor → its subsidiaries | `owns` | `src-026` p.117, Exhibit 21.1 "List of subsidiaries" | `owns` meets §5, but each subsidiary needs a company record, and D-057 requires the filer's own statement of its legal name. A parent's exhibit is not that. H-3: the edge waits (§6) |
| Amazon → Amazon Web Services, Inc. | `owns` | `src-052`: "Amazon Web Services, Inc. (AWS), an Amazon.com, Inc. company" | "an … company" is group text (§5 `owns`: not enough on its own); `rel:owns` is `time_sensitive` and the release is dated 2023-11-28; no AWS record (§6) |
| Micron → HBM4 36GB 12H | `fabricates` | `claim-micron-hbm4-identity` ("in high-volume production"); `src-025` p.7 "We manufacture our products at wholly-owned facilities" | production is not stated as wafer fabrication by Micron for this product; the 10-K sentence is company-level (ER-9) |
| Micron → Manassas | `owns`, `operates` | `claim-micron-manassas-fab` | fails both (`facility-dataset.md` §5) |

**Count.** 5 edges. The human's 10-edge review therefore covers the 5 edges, the staged
TSMC → H100 derivation, and the refused candidates above, each traced from its sentence
(`SESSION-10-REPORT.md`). Fewer than 10 edges exist because the evidence supports fewer: see
the report's deviations.

## 2. Edge IDs (RI-1, machine-checked)

**Rule** (D-090). An edge ID is `rel-`, the source entity's ID, `-`, the relation type with
`_` written as `-`, `-`, the target entity's ID, and, for `supplies`, `-` and the `item`'s ID:

```
rel-<source_entity>-<relation type>-<target_entity>[-<item>]
```

- **Stable and non-editorial.** Every part is an ID, and entity IDs are themselves rule-made
  (ID-1, CI-1, PI-1, FI-1). A display name or a claim never moves an edge ID.
- **The type prefixes are kept** (`company-`, `product-` …). Without them, a technology and a
  component with one slug would give one edge ID.
- **Collisions.** Two records with the same type, endpoints and item are allowed only for
  non-overlapping periods (V-5). The second record's ID would collide, so it needs a decision,
  as FI-1 and EI-1 do.
- **Machine check.** `tests/test_data_relationships.py` recomputes every ID.

The IDs are long. Length is the price of a rule with no judgement in it.

## 3. Level, endpoints and kinds (V-2)

- **Endpoint types** are the schema's (`relationships.schema.json` `rel_<type>`), checked by
  VD-2.
- **Endpoint kinds** are `relationship-taxonomy.md` §2's "Kind constraint" table. The check
  implements one rule per row of that table, and a test fails if the table's types and the
  check's types differ.
- **Class edges carry no dates** (the schema forbids them, §10 of the taxonomy).
- **No jurisdiction, event, source or claim is an endpoint** (RR-9; the schema).

## 4. Time

- **Periods only from claims** (taxonomy §10). None of the five edges' claims gives a period
  for the relation itself, so no edge has `valid_from` or `valid_to`. M16's completion in
  2021-02 dates a construction, not the start of operation, and is not used as `valid_from`.
  A missing period is not "always" and not "today".
- **`time_sensitive` rows** (`source-policy.md` §7): `rel:owns`, `rel:operates`,
  `rel:fabricates`, `rel:packages`, `rel:incorporates.supplier`, `rel:supplies`, `rel:houses`,
  `rel:provides_access_to`. F-1 extends to them (D-096): an edge on such a row needs at least
  one citation the row accepts whose evidence date is within the §12 horizon of its
  verification. Of the five edges, only `operates` is on such a row. Its filing is dated
  2026-03-17.

## 5. Unknown suppliers (D-094)

Both `incorporates` edges carry `supplier: {"state": "not_researched"}`.

- **Why not `not_publicly_determinable`.** ER-3 needs every preferred class of
  `rel:incorporates.supplier` searched for the specific product: `company_technical_documentation`
  and `company_filing`. For the H100, NVIDIA's page names no memory maker and its 10-K speaks
  at company level (ER-9), but the memory makers' documentation was not searched and Samsung's
  host refused access (`claim-model.md` §8). For Trainium2, AWS's page names no maker and no
  memory maker's filing was searched for it. A preferred class was not fully searched, so the
  value stays `not_researched` (ER-3, SP-7).
- **No search claim is created.** A `not_researched` state needs no claim, and a search record
  with a missing class would conclude `not_researched` anyway.
- **Never a placeholder** (RR-7) and never filled from NVIDIA's company-level memory suppliers
  (ER-9; taxonomy §4.9).
- **The check exists.** When a `not_publicly_determinable` supplier appears, V-10 requires its
  search record to cover every preferred class of the row (`claim-model.md` §8). It runs on the
  fixtures.

## 6. Company records (H-3)

H-3 allowed a new company record only for a supplier or subsidiary that an edge needs, by
the D-054 to D-057 rules. **None was created** (D-095):

- **Subsidiaries** (Amkor's Exhibit 21.1, Amazon Web Services, Inc.): D-057 needs the filer's
  own statement of its exact legal name. A parent's list is not that statement, and no
  subsidiary's own filing was read.
- **Suppliers** (Samsung, Carl Zeiss SMT GmbH, Hon Hai, Wistron, Fabrinet): none has a
  `supplies` edge whose item is a record, so none is needed.
- **The AWS legal entity** stays open. `src-052` names "Amazon Web Services, Inc." as the
  announcing company, "an Amazon.com, Inc. company". That names the entity, but does not give
  its identity evidence under D-057.

## 7. Evidence guards (machine-checked)

The taxonomy's rules RR-1, ER-1, ER-8 and ER-9 need a reader. Four guards make the plainest
violations fail in CI. They are guards, not proof: the Verifier's reading and the human's
review stay the check (§9).

| Guard | What it checks | Rule it guards |
|---|---|---|
| PL-1 | an edge with a product endpoint rests on at least one anchor that carries the first word of that product's term (`concept-dataset.md` §7) | ER-9: a company-level sentence that never names the product cannot support a product edge |
| EP-1 | a `fabricates` edge never cites directly a claim that serves a product's `vendor_process_name` | ER-1: a process name supports fabrication only through a `DERIVATION` |
| PE-1 | an edge cites at least one `FACT` or `DERIVATION`, and no claim of an `announced` event | ER-8: a plan or an announcement is never a state |
| RV-1 | at least one anchor the edge reaches carries a word of its type's row below | RR-1: two names in one sentence are not a relation |

**Relation words (RV-1).** A word matches case-insensitively, anywhere in the anchor.

| Type | Words |
|---|---|
| `requires` | requires; necessary; needs; stacks |
| `has_part` | consists of; contains; composed of; part of |
| `owns` | subsidiary; subsidiaries; wholly-owned; owns |
| `operates` | operates; operated; 가동 |
| `designs` | designed; design; developed |
| `fabricates` | fabricated; fabrication; wafer |
| `packages` | packaging; packaged; assembly |
| `incorporates` | HBM; memory; contains; incorporates |
| `supplies` | supply; supplier; purchase; sells; licenses |
| `houses` | installed; deployed; houses |
| `provides_access_to` | instances; available; access |

`stacks` is in the `requires` row because a definition that says every instance stacks dies
is the one class case S10 records (D-091). A future session that adds a class edge adds its
word by decision.

## 8. Navigation (H-5, the gate)

**Rule** (D-097). `tools/navigate.py` (standard library) reads the entity, relationship and
claim files and answers MA §18's questions without a graph database. Nothing it computes is
stored (RR-5).

| Command | Question (MA §18) | Answer |
|---|---|---|
| `depends-on ID` | What depends on this component? | the structural edges (`requires`, `has_part`, `incorporates`) that point into ID, then into each dependent, with the path; a walk computed when asked |
| `suppliers ID` | Who supplies this component? | `supplies` edges whose `item` is ID; for each `incorporates` edge into ID, its `supplier` values or state; for a product, its `vendor` field |
| `actors ID` | Who does what to this record? | the activity edges (`owns`, `operates`, `designs`, `fabricates`, `packages`, `supplies`) that point into ID |
| `evidence REL-ID` | What evidence supports the edge? | the trace (`tools/trace.py`, `claim-model.md` §12) |
| `edges ID` | Every recorded edge at ID | both directions, with the inverse reading as display text (RR-3) |

- **Canonical by default.** `--include-staging` adds staging edges, each marked `staging`.
- **"No recorded relationship", never "none"** (RR-7). A `not_researched` supplier is printed as
  that state.
- **Each line shows** the edge ID, the sentence `<source> <type> <target>`, its level, and each
  claim's type and status.

```bash
python tools/navigate.py depends-on technology-3d-die-stacking
python tools/navigate.py suppliers component-high-bandwidth-memory
python tools/navigate.py actors product-amazon-com-trainium2
python tools/navigate.py evidence rel-company-sk-hynix-operates-facility-kr-m16
```

**Rejected:** DuckDB now (S14's, and a new dependency); extending `tools/trace.py` only (it
answers one of the questions); a stored adjacency list (a second home).

## 9. Staging, canonical and the human's review (H-6)

As D-061, D-077 and D-087 (D-098): an edge becomes canonical only on the human's verdict, and
only when every claim it cites, its endpoints and its `item` or `supplier` companies are
canonical. CE-1 extends to edges. The human's verdicts go verbatim into
`SESSION-10-REPORT.md`.

**Review.** For each edge on the sheet in the S10 report:

1. Run `python tools/trace.py <edge ID>` (or `python tools/navigate.py evidence <edge ID>`).
2. Open the source at the locator, and read the whole sentence.
3. Answer:
   - **Does the sentence state the relation itself**, and not only name both parties (RR-1)?
   - **Is it about this product**, not a company in general (ER-9) or a die (D-073)?
   - **Is a plan kept out** (ER-8)?
   - **For a `DERIVATION`:** does the step hold, and is it the one the ruling allows?
4. Give a verdict per edge: accept, reject, or "wording too strong".

The flagged rulings (`operates` for M16; the class edge) are asked as separate questions. An
unticked box leaves that edge in staging.

## 10. validate-data for edges

| Check | What it checks | Where |
|---|---|---|
| VD-2 (extended) | every edge, staging and canonical, is valid against the unchanged relationship schema | `tests/test_data_schema.py` |
| V-1 | endpoints, `item` and `supplier` values resolve to records of the prefixed type; every claim resolves | `tests/test_data_relationships.py` |
| V-2 | the kind constraints of `relationship-taxonomy.md` §2 (§3) | same |
| V-3 | no edge from a record to itself | same |
| V-4 | `valid_from` ≤ `valid_to`, at the coarser precision | same |
| V-5 | no two edges with the same type, endpoints and `item` over overlapping periods (an undated edge overlaps every period) | same |
| V-6 | a `requires` or `has_part` edge does not restate a `broader` link between the same records | same |
| V-7 | **warning**: a `supplies` edge whose `item` is a product whose vendor is not the source | same |
| V-8 | **warning**: RW-1 to RW-3 (`relationship-taxonomy.md` §11) | same |
| V-9 | no placeholder slug in an endpoint, `item` or `supplier` value | same |
| V-10 | each edge rests on a citation whose class and standing its `rel:<type>` row allows; each `supplier` assertion on `rel:incorporates.supplier`; a `not_publicly_determinable` supplier's search covers every preferred class of that row | same |
| CE-1 | a canonical edge cites canonical claims, and its endpoints, `item` and `supplier` companies are canonical; no edge ID is both staging and canonical; IDs are unique | same |
| RI-1 | §2 | same |
| PL-1, EP-1, PE-1, RV-1 | §7 | same |
| F-1 | §4 | `tests/test_freshness.py` |

V-7 and V-8 are warnings (D-033): they are reported, never failures, and nothing is corrected
automatically.

```bash
python -m unittest discover -s tests -p "test_data*.py" -v   # validate-data
python -m unittest discover -s tests -p "test_freshness.py" -v   # validate-freshness
```

**What the checks cannot see.** A sentence that names the product and carries a relation word
can still state something else. A `DERIVATION` whose step does not hold passes every check.
The Verifier's reading and the human's review are the guard.

## 11. Sources and access

**Re-retrievals** (D-075, H-4), 2026-10-02: `src-024` to `src-030`, `src-040`, `src-043` and
`src-046` to `src-049` returned their registered bytes. `src-006`/`src-042` (NVIDIA's Hopper
architecture page) and `src-044` (Micron's HBM page) returned changed bytes. The H100 page's
new bytes are stable across requests and are cited, so they are a new record, `src-051`.
`src-044` is not cited in S10.

**New sources** (`src-051` onward), retrieved automatically on 2026-10-02 with full hashes; texts
stay outside the repository (RA-4(4)):

| Source | What | Class |
|---|---|---|
| `src-051` | NVIDIA Hopper Architecture In-Depth, retrieval of 2026-10-02 (earlier bytes: `src-006`, `src-042`) | `company_technical_documentation` |
| `src-052` | Amazon press release, "AWS Unveils Next Generation AWS-Designed Chips" (2023-11-28), on Amazon's own press centre | `company_press_release` |

**Read, not registered** (discovery or not cited): NVIDIA's H100 product page and Hopper
architecture page; the H100 PCIe product brief (2022); AWS's Trainium page.

**Access gaps** (SP-7; nothing bypassed, RA-2): `investor.tsmc.com` (HTTP 403 challenge,
2026-10-02). English DART's report index page did not return its section list on 2026-10-02,
so SK hynix's report was not searched for named customers in S10.

**RA-4.** The human agreed to re-supply TSMC's 20-F ("Re-supply it (Recommended)"). Until it
arrives `src-031` is not cited again (D-075).

## 12. Candidates considered and rejected

| Candidate | Why not |
|---|---|
| Edge IDs without type prefixes | a technology and a component with one slug would collide (§2) |
| Edge IDs from a counter (`rel-` and a number) | not recomputable; a check could not tell a wrong ID from a right one |
| `item` broadened or narrowed to a record that exists (HBM for "memory") | ER-9: the item is exactly as broad as the source |
| New component records (memory, optical column) for the `supplies` items | H-3 allows company records only; components are the concept dataset's, by decision |
| `valid_from: 2021-02` on the M16 edge | completion of construction is not the start of operation (§4) |
| `not_publicly_determinable` for the HBM suppliers | ER-3: a preferred class was not fully searched (§5) |
| The Hopper architecture page as fresh evidence for TSMC → H100 | architecture, not product; the human chose a gap (D-092) |
| A subsidiary record from a parent's exhibit | D-057 (§6) |
| A graph library or database | NG-07; MA §18: relational files first |

## 13. What S10 leaves to other sessions

| Item | Owner | Note |
|---|---|---|
| TSMC → H100 `fabricates` | the session with product-level evidence dated within the horizon | D-092 |
| `supplies` items broader or narrower than the records (memory, wafers, optical columns) | a concept session, by decision | §1 |
| Subsidiary and AWS company records; `owns` edges | a session that reads the subsidiaries' own filings or registers | §6 |
| HBM suppliers per product | a session that searches every preferred class (ER-3) | §5 |
| TSMC's 20-F supplier sentences | the session that receives it (RA-4) | §11 |
| `depends_on`, concentration, single-sourcing | S14–S15 | derived from these edges |
