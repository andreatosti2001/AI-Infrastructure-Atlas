# Relationship taxonomy — typed edges for the first vertical

**Status:** PROPOSED (S04, 2026-09-30): D-028 to D-033, awaiting human review.
**Session:** S04 · **Date:** 2026-09-30
**Inputs:**
- `entity-taxonomy.md` (§1 rules R-1 to R-8, §3, §4.2–4.4, §7, §9);
- `../research/domain-map.md` §3 (DEP-01 to DEP-18 and the † verbs), §4 (blurs B-1 to
  B-5), §7.1 (TQ-04, TQ-06, TQ-07, TQ-11);
- MA §5.4–5.7, §6.2, §18;
- `SESSION-ROADMAP.md` S04, S06, S09, S10, S15, S17;
- decisions D-020 to D-027; `baseline.md` §2, §4, §6.

**Schema:** [`schemas/relationships.schema.json`](../../schemas/relationships.schema.json)

**One home for each kind of statement:**

- **This document** holds the reasoning:
  - why each relation type exists;
  - what a source must show before an edge may be recorded;
  - what each type must not be confused with;
  - where every candidate verb and every S01 dependency ends up.
- **The schema** holds the record shape, the relation-type vocabulary with one-line
  definitions, and the endpoint types of each relation type.
- **One checked overlap.** The §2 table repeats each type's endpoints and level so that a
  reader can see them next to the reasoning. `tests/test_relationship_taxonomy.py` fails
  if the table and the schema disagree, so the schema stays the one home.

**Claim labels.**
- The vocabulary is the Atlas's design (`INTERPRETATION`). Its consequences are
  `IMPLICATION`.
- Where a definition depends on what an industry term covers, it cites the S01 entry
  (e.g. `PKG-07`). Sources, locators and verbatim anchors stay in that domain-map entry,
  which is their one home.
- No external source was retrieved in S04.

---

## 1. Design rules

These extend the entity rules R-1 to R-8. They apply to every later change to the
vocabulary.

| ID | Rule | Why |
|---|---|---|
| RR-1 | **An edge states one activity or one structural fact.** Two names appearing in the same source is never an edge. The source must state the relation itself (§5). | `SESSION-ROADMAP.md` S04 mission: "prevent accidental inference from co-occurrence" |
| RR-2 | **One verb, one level.** A type connects either vendor-neutral classes (class level) or named things (instance level), never both. | The two levels need different evidence (domain map §3, "structural" vs "contingent"); §3 |
| RR-3 | **Every type is directed and stored in one direction.** The inverse reading ("fabricated by") is display text. There are no symmetric types in v1. | A stored inverse is a second copy of the same fact (CLAUDE.md §7) |
| RR-4 | **A fact held by an entity field is never restated as an edge.** | One home (CLAUDE.md §7; D-018 L-05; §7) |
| RR-5 | **Nothing derived is stored.** No `depends_on`, no transitive edges, no inverses, no roles inferred from edges, no edge inferred from a role. | R-8; MA §5.6; D-024 |
| RR-6 | **Every edge cites at least one claim.** Claim type and evidence status live on the claim. There is no record-level `source_ids`, no confidence score and no stored status. | D-025 precedent; L-06; S06 gate "What exactly supports this relationship?" |
| RR-7 | **A missing edge means "not recorded", never "no relationship".** No placeholder endpoint stands in for an unknown party. | MA §5.7; `SESSION-ROADMAP.md` S10 rule; §9 |
| RR-8 | **An edge holds over an interval; an event happens at a date.** Plans and announcements are events plus claims. Events are not endpoints. | `entity-taxonomy.md` §4.2, §4.4 |
| RR-9 | **Endpoints are instantiable entity types only.** Reserved types (policy, institution), record kinds (source, claim, event) and excluded domains (energy, networking) have no edges in v1. | D-022; NG-04; NG-05 |
| RR-10 | **A verb is adopted only with a definition and an evidence expectation.** A verb for which no evidence expectation can be written is rejected as vague. | `SESSION-ROADMAP.md` S04 gate |

**Direction convention** (`INTERPRETATION`). Every edge reads as an English sentence,
`<source_entity> <relation_type> <target_entity>`:

- **structural edges** (`requires`, `has_part`, `incorporates`, `houses`,
  `provides_access_to`) point from the thing that depends to the thing it depends on;
- **activity edges** (`owns`, `operates`, `designs`, `fabricates`, `packages`,
  `supplies`) point from the actor to what it acts on.

So "what depends on X?" (MA §18) is answered by the structural edges that point *into* X,
and "who does what to X?" by the activity edges that point into X.

## 2. The v1 relation types at a glance (machine-checked)

Eleven types: two at class level, nine at instance level (D-029). The "Inverse reading"
column is display text only.

| Type | Level | Source | Target | Qualifier | Inverse reading | DEPs |
|---|---|---|---|---|---|---|
| `requires` | class | technology, component | technology, component | — | required by | DEP-02, DEP-03, DEP-06, DEP-07, DEP-08, DEP-09, DEP-18 |
| `has_part` | class | component | component | — | part of | — |
| `owns` | instance | company | company, facility | — | owned by | — |
| `operates` | instance | company | facility | — | operated by | DEP-13 |
| `designs` | instance | company | product | — | designed by | DEP-05, DEP-15 |
| `fabricates` | instance | company | product | — | fabricated by | DEP-05 |
| `packages` | instance | company | product | — | packaged by | DEP-02 |
| `incorporates` | instance | product | product, component | `supplier` | incorporated in | DEP-01 |
| `supplies` | instance | company | company | `item` | supplied by | DEP-07, DEP-09 |
| `houses` | instance | facility | product | — | housed in | DEP-12 |
| `provides_access_to` | instance | product | product | — | accessible through | DEP-14 |

**The record** (D-028; the schema holds the exact shapes):

| Field | Meaning |
|---|---|
| `id` | `rel-<slug>`, as MA §5.4 |
| `relation_type` | one of the eleven types |
| `source_entity`, `target_entity` | entity IDs, typed by prefix (MA §5.4 names) |
| `claim_ids` | at least one claim supporting the edge |
| `valid_from`, `valid_to` | optional partial dates, instance level only (§10) |
| `item` | `supplies` only: the product or component class supplied |
| `supplier` | `incorporates` only: who supplies the part, or an explicit state (§9) |

Nothing else is allowed: no `source_ids`, `notes`, `status`, `confidence`,
`evidence_status`, process names or inverse fields.

**Enforced where.** The schema checks each endpoint's *type* from its ID prefix. The
*kind* constraints below need the endpoint record, so `validate-data` checks them when
records exist (S06/S07; §15, V-2).

| Type | Kind constraint (checked by `validate-data`) |
|---|---|
| `requires` | a `production_equipment` component is never the source (SME's own supply chain is future scope, domain map SME-01) |
| `has_part` | both components have `use_class: constituent`. Production equipment is never part of anything |
| `designs`, `fabricates`, `packages` | the product has `product_kind: hardware` |
| `incorporates` | source and a product target are `hardware`; a component target is `constituent` |
| `houses` | the facility's `facility_kinds` include `data_centre`; the product is `hardware` |
| `provides_access_to` | the source product is `service`; the target is `hardware` |

## 3. Two levels (human focus)

The domain map separates **structural** dependencies ("true of the technology itself")
from **contingent** ones ("true of a current market or organisational arrangement"), and
says the two "need different evidence" (§3 preamble). The Atlas turns that into two
levels of edge.

| | Class level | Instance level |
|---|---|---|
| Endpoints | vendor-neutral classes: technology, component | named things: company, facility, product |
| Example | HBM `requires` TSV (DEP-03) | a named foundry `fabricates` a named chip (DEP-05) |
| What it claims | true of every instance of the class, at the state of technology the source describes | true of these parties, over some period |
| Evidence | technical definitions, standards, process descriptions | the parties' own documents, filings, datasheets, catalogues |
| Time | none on the edge; the claim's date says how current it is | `valid_from` / `valid_to` when the claims give a period |
| Types | `requires`, `has_part` | the other nine |

**Why one verb may not serve both levels** (D-029). If "uses" connected both "data-centre
GPU → HBM" (a class) and "a named GPU → HBM" (a product), a query for structural
dependencies would silently pick up one vendor's design choice as if it were a law of
the technology. DEP-01 is exactly this case: the *need* for bandwidth is structural,
but HBM as the *solution* is contingent. So the class-level fact is recorded only when a
source states necessity (`requires`), and a product's use of HBM is an instance-level
`incorporates` edge. A general statement such as "current accelerators use HBM" is then
a `DERIVATION` over product edges (S15), not a stored class edge.

**Classes and instances meet only through entity fields.** `product.instance_of` links a
product to its class, and `broader` builds the class hierarchy. Neither is an edge
(§7). No v1 type connects a company to a class: what a firm does in general is a role
(D-024), and what it does to a named product is an instance edge.

## 4. The relation types

Each type below gives its definition, direction, endpoints, level, time handling and what
it must not be confused with. What a source must show, and what is typically not public,
is in the §5 table, the one home of evidence expectations.

### 4.1 `requires`

- **Definition:** making or operating any instance of the source class is not possible,
  at the state of technology the cited source describes, without the target class.
  It states necessity, not current practice.
- **Direction:** dependent class → needed class. Displayed inversely as "required by".
  MA's `enables` is this inverse reading (§6).
- **Endpoints:** technology or component → technology or component.
- **Level:** class.
- **Time:** none on the edge. A necessity that holds only for a period ("from HBM4",
  "at current nodes") is either stated as a narrower class, or recorded as claims
  without an edge.
- **Not to be confused with:**
  - `broader`: "2.5D packaging is a kind of advanced packaging" is taxonomy, a field;
  - `has_part`: TSV is a technique HBM needs, not a part of it (HBM-04 vs HBM-02);
  - `incorporates`: a product's use of a class is an instance fact;
  - "uses" in a source: current use supports at most an instance edge, never `requires`.

### 4.2 `has_part`

- **Definition:** every instance of the source component class physically contains an
  instance of the target component class, by the class's technical definition.
- **Direction:** whole → part. Displayed as "part of". The domain map's `stacks_on`
  (core DRAM dies on the base die) is recorded as composition (§6).
- **Endpoints:** component → component, both `constituent`.
- **Level:** class.
- **Time:** none on the edge.
- **Not to be confused with:**
  - `broader`: an HBM base die is *part of* an HBM stack, not a *kind of* HBM (HBM-03);
  - `incorporates`: one product's bill of materials is not the class definition;
  - `requires`: production equipment is needed to make a class, but it is never a part.

### 4.3 `owns`

- **Definition:** the source company holds controlling ownership of the target company or
  facility, as the cited source states it (for example, the target is a subsidiary).
- **Direction:** owner → owned. Displayed as "owned by".
- **Endpoints:** company → company or facility.
- **Level:** instance.
- **Time:** `valid_from` / `valid_to` where the claims give them. Ownership is a state over
  an interval, so it is an edge. Acquisitions and investments that change it are events
  (MA §5.5 `acquired`, `invested`; D-023). The edge is not derived from events, because
  an event history is rarely complete (ownership from founding has no acquisition event),
  while filings state the ownership itself (D-029).
- **Not to be confused with:**
  - `operates`: owning a site and running it are separate facts (S09);
  - a minority stake or an investment: an event, not `owns`;
  - `product.vendor`: whose name a product carries says nothing about corporate control.

### 4.4 `operates`

- **Definition:** the source company runs the day-to-day activity of the target facility:
  production at a fab or packaging site, or the running of a data centre.
- **Direction:** operator → facility. Displayed as "operated by".
- **Endpoints:** company → facility.
- **Level:** instance.
- **Time:** interval, from the claims.
- **Not to be confused with:**
  - `owns` (§4.3);
  - `facility.located_in`: where the site is, a field;
  - `houses`: what equipment is inside the site;
  - a cloud service's dependence on data centres: the service → facility link is not
    modelled in v1, because providers abstract location (DC-04; §8, DEP-13).

### 4.5 `designs`

- **Definition:** the source company performs design work on the target product, a chip
  or a system.
- **Direction:** designer → product. Displayed as "designed by".
- **Endpoints:** company → product (hardware).
- **Level:** instance.
- **Time:** interval if the claims give one; usually none.
- **Not to be confused with:**
  - `product.vendor`: the vendor is whose name the product carries (identity). A vendor is
    often the designer, but the vendor field alone does not establish a `designs` edge;
  - the `fabless_designer` role: a business model, claim-backed on the company (D-024).
    D-024 left cloud providers' design work (B-2) to this type instead of a role;
  - `requires` → EDA: the class-level fact that chip design needs EDA (DEP-09).

### 4.6 `fabricates`

- **Definition:** the source company performs wafer fabrication of the target product's
  dies. This is the front end, including TSV formation (B-1).
- **Direction:** fabricator → product. Displayed as "fabricated by".
- **Endpoints:** company → product (hardware).
- **Level:** instance.
- **Time:** interval, from the claims.
- **Not to be confused with:**
  - `packages`: post-fabrication steps, even when the same firm does both (B-3);
  - `designs` and `product.vendor` (DEP-05: the fabless model separates them);
  - the process: the process as the vendor names it is `product.vendor_process_name`
    (FAB-05, TQ-07). There is no process field on the edge (§7);
  - the fab: which facility makes the dies is not in v1 (§15). It must never be read off
    the fabricator's headquarters or its list of fabs (S09 conflation);
  - fabrication of only one constituent of a product (the HBM4 base-die case, DEP-04):
    not representable in v1 (D-032).

### 4.7 `packages`

- **Definition:** the source company performs assembly and packaging of the target product
  after wafer fabrication. This covers dicing, die stacking (HBM, PKG-05), 2.5D
  integration on an interposer (PKG-04) and wafer-level steps done after fabrication,
  such as TSV reveal (PKG-07: an OSAT that "does NOT provide TSV formation").
  Package test is not included, because test is future scope (domain map layer 3
  exclusions).
- **Direction:** packager → product. Displayed as "packaged by".
- **Endpoints:** company → product (hardware).
- **Level:** instance.
- **Time:** interval, from the claims.
- **Not to be confused with:**
  - the `osat` role: foundries and memory makers also package (B-3). The edge records who
    performs the step, whatever their role (TQ-06);
  - the domain map's `integrates` (HBM with logic in one package): that integration *is*
    the 2.5D packaging step, so it is this type (§6);
  - a vendor-named packaging process (CoWoS, PKG-04): not recorded in v1 (D-032).

### 4.8 `incorporates`

- **Definition:** the source product physically contains the target. The target is either
  a constituent component class, or a named product.
- **Direction:** product → part. Displayed as "incorporated in".
- **Endpoints:** product → product or component.
- **Level:** instance. The source is always a named product; a class target says what
  kind of part, not whose.
- **Qualifier `supplier`** (D-031):
  - **class target:** who supplies the part for this product. It is a list of claim-backed
    company assertions (several means multi-sourcing), or an explicit state:
    `not_researched`, or `not_publicly_determinable` with the claims that show it;
  - **named product target:** always `not_applicable`, because the supplier is that
    product's `vendor`. Recording it again would be a second home.
- **Time:** interval if the claims give one (e.g. a product revision).
- **Not to be confused with:**
  - `has_part`: a class definition, true of every instance;
  - `supplies`: a company-level sale, which says nothing about which product the goods
    go into;
  - `product.instance_of`: what the product *is*, not what it *contains*.

### 4.9 `supplies`

- **Definition:** the source company sells or licenses the `item` (a product, or a
  component class) to the target company, as a claim states at company level.
- **Direction:** supplier → customer. Displayed as "supplied by".
- **Endpoints:** company → company; `item` is a product or a component.
- **Level:** instance.
- **Time:** interval, from the claims.
- **Not to be confused with:**
  - `fabricates` and `packages`: manufacturing services performed on the customer's own
    product are those types, not `supplies`;
  - the `supplier` of an `incorporates` edge: that value is product-level. A company-level
    `supplies` edge is never derived from it, and never used to fill it in (RR-5);
  - `depends_on`: a customer's dependence on a supplier is a derivation (S15).

### 4.10 `houses`

- **Definition:** units of the target hardware product are installed and run at the
  source data-centre facility.
- **Direction:** facility → product. Displayed as "housed in".
- **Endpoints:** facility (data centre) → product (hardware).
- **Level:** instance.
- **Time:** interval, from the claims.
- **Not to be confused with:**
  - a count or a capacity: counts are metrics (NG-11) and usually non-public (DEP-12);
    capacity is `facility.nameplate_it_capacity_mw`;
  - `operates`: who runs the site;
  - a cloud service's hardware (`provides_access_to`).

### 4.11 `provides_access_to`

- **Definition:** the source service product lets its users run workloads on the target
  hardware product, as the provider's documentation states.
- **Direction:** service → hardware. The domain map's `offered_via` is its inverse
  reading, "accessible through" (§6).
- **Endpoints:** product (service) → product (hardware).
- **Level:** instance.
- **Time:** interval, from the claims.
- **Not to be confused with:**
  - `houses`: where hardware is installed;
  - `designs`: a cloud provider designing its own accelerator (DEP-15, B-2) is a separate
    fact from offering it as a service (DEP-14).

## 5. Evidence expectations (one home; handoff to S05)

What a source must show before an edge of each type may be recorded. **S04 states what the
evidence must show. S05 decides which source classes are preferred** (S05 gate). The
"Typically non-public" column quotes or cites domain map §3 "Likely non-public".

| Type | The source must show | Not enough on its own | Typically non-public |
|---|---|---|---|
| `requires` | the target class is necessary for making or operating the source class, stated as necessity for the class as a whole | a statement that a product or firm "uses" the target; a single vendor's process description; an announcement | the threshold of necessity (e.g. the EUV node threshold, SME-03, `not_researched`); alternatives (DEP-08) |
| `has_part` | a technical definition of the whole class in which the part is a constituent of every instance | one product's datasheet or teardown (that is `incorporates`) | — |
| `owns` | both parties named, and controlling ownership or subsidiary status stated, with the date or period the source gives | a shared brand name; group marketing text; an investment or partnership announcement (an event) | holdings in private companies; the structure of joint ventures |
| `operates` | both parties named, and the company stated as running the named site | ownership of the site; the company's list of locations; a site in the same city as the company | operating arrangements in joint ventures; the facility behind a cloud service (DC-04, SRC-001 p.6) |
| `designs` | the company named as having designed or developed the named product (e.g. "custom-developed", ACC-03) | the product's vendor name; a company's general role as a chip designer | design partners and the split of design work |
| `fabricates` | the fabricator, the named product and the fact of wafer fabrication. A process name that embeds a foundry's name supports the edge only as a `DERIVATION` (§12, example 1) | a foundry and a product named in the same article; the designer's fabless role; the foundry's customer list | which fab; wafer allocation and volumes (DEP-05, DEP-11) |
| `packages` | the packager, the named product and the packaging step | a description of a packaging process owned by a firm (e.g. CoWoS in PKG-04) without a named product; the packager's role | which packaging line or site packages which product (DEP-02) |
| `incorporates` | the named product and the part (class or named product) it contains, e.g. a datasheet naming the memory type (DEP-01). `supplier` values need their own claims naming the supplier for this product | a component maker's marketing that mentions a customer's product category; the market share of a supplier | which maker's part goes into which product (DEP-01, HBM-06) |
| `supplies` | supplier, customer and item named, and a supply or licence relation stated between them | co-mention of both companies; the supplier's role; a customer's product using the item class | volumes; contract terms; the installed tool base per fab (DEP-07); tool licences per designer (DEP-09) |
| `houses` | the named site and the named product, with installation or deployment at that site stated | the operator's use of the product somewhere; a region or availability zone (not a site, D-022) | deployment counts per site (DEP-12: LBNL, SRC-021 p.17) |
| `provides_access_to` | the provider's own service documentation naming the hardware product as available through the named service (e.g. SRC-008, DC-03) | a provider designing or buying the hardware | capacity and location behind the service |

**Entity identity evidence** (from S03, D-025; repeated here as S05's second input):
`identity_claim_ids` needs at least one claim establishing that the thing exists and is
of its type. S05 assigns a preferred source class to it as well.

## 6. Reconciliation of the three verb lists (machine-checked)

Every verb in MA §6.2, the `SESSION-ROADMAP.md` S04 "Focus" list and domain map §3 (the
Verb column and the † list) has exactly one disposition. "In" says which lists contain
it: MA, RM (roadmap) or DM (domain map). `tests/test_relationship_taxonomy.py` parses the
three lists from their documents and checks this table against them.

| Verb | In | Disposition | Target | Reason | Decision |
|---|---|---|---|---|---|
| `owns` | MA, RM | adopt | `rel:owns` | controlling ownership of a company or site; a state over an interval (§4.3) | D-029 |
| `operates` | MA, RM, DM | adopt | `rel:operates` | running a site, apart from owning it (S09; DEP-13) | D-029 |
| `manufactures` | MA, RM | rejected as vague | `none` | an umbrella over wafer fabrication and packaging, which different firms do (TQ-06: "Model each process step separately and record who performs it"). Replaced by `fabricates` and `packages` | D-030 |
| `supplies` | MA, RM | adopt | `rel:supplies` | company-level supply, with the item named (§4.9) | D-029 |
| `uses` | MA, RM, DM | rejected as vague | `none` | covers physical inclusion (DEP-01 → `incorporates`), necessity (→ `requires`) and consumption of a service (→ `provides_access_to`). Each has a precise type | D-030 |
| `depends_on` | MA, RM, DM | a derivation | `none` | computed from structural and activity edges; how critical a dependency is belongs to S15 (NG-11). A stored copy would be a second home (RR-5) | D-030 |
| `located_in` | MA, RM | already an entity field | `attribute:facility.located_in`, `attribute:company.incorporated_in`, `attribute:company.headquartered_in` | S03 split location into three claim-backed fields (§7) | D-030 |
| `produces` | MA, RM | rejected as vague | `none` | an umbrella like `manufactures`; aimed at a class, it would restate a role (D-024) | D-030 |
| `requires` | MA, RM, DM | adopt | `rel:requires` | class-level necessity (§4.1) | D-029 |
| `enables` | MA | merge into another verb | `rel:requires` | the inverse reading of `requires`; a stored inverse is forbidden (RR-3) | D-030 |
| `licenses` | MA | merge into another verb | `rel:supplies` | a software licence is supply of a software product (`item`, product kind `software`). IP licensing (EDA-02) is future scope | D-030 |
| `invests_in` | MA | an event | `kind:event` | Investment is an event (D-023, MA §5.5 `invested`). Controlling ownership that results is `owns` | D-030 |
| `acquired` | MA | an event | `kind:event` | a dated occurrence (MA §5.5 `acquired`); the ownership it creates is `owns` | D-030 |
| `restricted_by` | MA | reserved for S17 | `reserved:policy` | the target would be a policy, a reserved type (D-022) | D-030 |
| `regulated_by` | MA | reserved for S17 | `reserved:policy` | the target would be a policy; regulatory content also belongs to the governance repositories (baseline §2) | D-030 |
| `supported_by` | MA | reserved for S17 | `reserved:policy` | the target would be a policy (subsidy programme) | D-030 |
| `competes_with` | MA | a derivation | `none` | a view over vendors of products that are instances of the same class. Anything stronger is an interpretation, and it would be symmetric (RR-3) | D-030 |
| `partners_with` | MA | rejected as vague | `none` | "partner" covers supply, joint development, licensing and joint ventures. Each is a specific edge, or an announcement event | D-030 |
| `designs` | RM, DM | adopt | `rel:designs` | DEP-05, DEP-15; D-024 left design work (B-2) to this type | D-029 |
| `packages` | RM, DM | adopt | `rel:packages` | DEP-02; B-3 | D-029 |
| `fabricates` | RM, DM | adopt | `rel:fabricates` | DEP-05; TQ-06 | D-029 |
| `constrained_by` | RM | reserved for S17 | `reserved:policy` | only definable against a policy. S17 must define it precisely or reject it. Its non-policy use ("constrained by die supply", DEP-11) is a claim about a market state, not an edge | D-030 |
| `affected_by` | RM | rejected as vague | `none` | anything can "affect" anything; no evidence expectation can be written (RR-10). S17 may propose a precise verb | D-030 |
| `houses` | DM | adopt | `rel:houses` | DEP-12 at instance level | D-029 |
| `offered_via` | DM | merge into another verb | `rel:provides_access_to` | the same fact stored in the dependent → dependency direction; "offered via" is its inverse reading | D-030 |
| `integrates` | DM | merge into another verb | `rel:packages` | integrating HBM with logic in one package is the 2.5D packaging step (PKG-04) | D-030 |
| `supplies_power_to` | DM | excluded by a non-goal | `none` | energy edges are excluded in v1 | NG-05 |
| `stacks_on` | DM | merge into another verb | `rel:has_part` | core dies stacked on a base die is the stack's composition (HBM-03). Who does the stacking is `packages` | D-030 |

**Introduced by S04** (not in any list):

- `has_part`: composition, which S03 left to S04 (`entity-taxonomy.md` §9);
- `incorporates`: the precise replacement for DEP-01's `uses`;
- `provides_access_to`: `offered_via` stored in the convention's direction.

**Conflicts with MA recorded, not resolved by editing MA.**

- MA §6.2 introduces its list as "Examples", so a disposition other than "adopt" puts
  MA's concept into practice. It does not override MA (SESSION-PROMPT-SPEC §1: expected
  evolution).
- MA §5.4's example relationship uses `manufactures` and `source_ids`. Both are replaced
  (D-028, D-030), following the D-023 precedent for MA §5.1.

## 7. One-home rulings on accepted S03 fields (machine-checked)

For each fact already held by an accepted entity field (Part B §04 list), the field stays
the home. **No fact moves from a field to a relationship**, so no accepted S03 decision
changes (D-030).

| Field | Edge that would duplicate it | Home | Ruling |
|---|---|---|---|
| `attribute:facility.located_in` | `located_in` (MA §6.2, roadmap) | field | Where a site is. No edge. No v1 type has a jurisdiction endpoint |
| `attribute:company.incorporated_in` | `located_in`, `incorporated_in` | field | A company's legal seat. No edge |
| `attribute:company.headquartered_in` | `located_in`, `headquartered_in` | field | Where a company is based. It is never used to locate production (S09) |
| `attribute:product.vendor` | "offers", "sells" | field | Whose name the product carries (identity). `designs`, `fabricates`, `packages` and `supplies` are different facts, each needing its own claim |
| `attribute:technology.broader` | `is_a`, `subclass_of`, `kind_of` | field | Taxonomy. The schema has no taxonomic type, so a dependency query cannot walk the classification tree (`entity-taxonomy.md` §3.3) |
| `attribute:component.broader` | `is_a`, `subclass_of` | field | As above. Composition is `has_part`, not `broader` |
| `attribute:product.instance_of` | `instance_of`, `is_a` | field | Classification of a product. `incorporates` states what it contains, not what it is |
| `attribute:product.vendor_process_name` | a process qualifier on `fabricates` | field | The chip's process as the vendor names it (FAB-05, TQ-07). No process field on edges. Domain map FAB-05 calls it "an attribute of the accelerator → foundry link"; S03 put it on the product, and S04 keeps it there |
| `attribute:company.roles` | edges from a company to a class; roles read off edges | field | Roles are claim-backed and never derived (D-024). No type targets a class from a company. A role and an edge that disagree give a warning, never a correction (§11) |

## 8. DEP-01 to DEP-18 (machine-checked)

Each S01 dependency maps to one of: a relationship type, an event, a derivation or a
recorded exclusion. "Target" names the relation types involved; it does not create
edges. S10 creates edges.

| DEP | Dependency (domain map §3) | Maps to | Target | Note |
|---|---|---|---|---|
| DEP-01 | Current data-centre accelerators → HBM | relationship | `rel:incorporates` | Per product: product `incorporates` the HBM class, with `supplier` explicit when unknown (§12, example 2). "Current accelerators use HBM" in general is a derivation over products |
| DEP-02 | HBM → 2.5D packaging with the logic die | relationship | `rel:requires`, `rel:packages` | Class: HBM `requires` 2.5D interposer packaging, for in-package HBM. Instance: who `packages` a named product |
| DEP-03 | HBM → TSV stacking | relationship | `rel:requires` | Class: HBM `requires` TSV |
| DEP-04 | HBM base die → foundry logic process (from HBM4) | event | `kind:event` | An announced plan (2024): an event plus an `ATTRIBUTION` claim, no edge. A confirmed edge would be fabrication of one constituent, which is not representable in v1 (D-032; §12, example 3) |
| DEP-05 | Fabless accelerator designer → foundry fabrication | relationship | `rel:designs`, `rel:fabricates` | Instance edges per product. The designer's dependence on the foundry is a derivation from them (S15) |
| DEP-06 | Advanced packaging → wafer-fab processes and equipment | relationship | `rel:requires` | Class: packaging technology `requires` wafer-process technologies and equipment classes |
| DEP-07 | Wafer fabrication → SME | relationship | `rel:requires`, `rel:supplies` | Class: process technologies `require` equipment classes (wafer fabrication itself, FAB-01, is definitional and has no record). Instance: tool makers `supply` named firms |
| DEP-08 | Most intricate layers at advanced nodes → EUV lithography | relationship | `rel:requires` | Class. Exclusivity stays `ATTRIBUTION` on the claims; the node threshold is `not_researched` (SME-03) |
| DEP-09 | Chip design → EDA | relationship | `rel:requires`, `rel:supplies` | Class: the accelerator class `requires` EDA. Instance: an EDA licence is `supplies` of a software product, typically non-public |
| DEP-10 | EDA ↔ foundry process information | exclusion | `none` | D-030: two-way (no symmetric types); its endpoint "process information" is EDA-03, definitional with no record; certification announcements are events; preferential access is a dated `ATTRIBUTION` |
| DEP-11 | Accelerator supply → die supply | exclusion | `none` | D-030: a claim about a market state (second-hand `ATTRIBUTION`) with no entity endpoints; any measure of it is a metric (NG-11) |
| DEP-12 | Accelerated servers → data centre | relationship | `rel:houses` | Instance: a named site `houses` a named product. At class level, "servers are housed in data centres" is the definition of the `data_centre` facility kind, not an edge |
| DEP-13 | Cloud service → data centres | relationship | `rel:operates` | A provider `operates` data-centre facilities. Which facility serves which service is abstracted (DC-04), so no service → facility type in v1 |
| DEP-14 | Accelerator access → cloud offering (IaaS) | relationship | `rel:provides_access_to` | A service product `provides_access_to` a hardware product (SRC-008) |
| DEP-15 | Cloud provider → own accelerator design | relationship | `rel:designs` | The B-2 case; no extra role (D-024) |
| DEP-16 | Data centre → electricity supply | exclusion | `none` | NG-05: energy is concept-level in v1 |
| DEP-17 | Chip power → server → facility → interconnection | exclusion | `none` | NG-05; the conversions are model assumptions, and any computation is S15's (NG-11) |
| DEP-18 | Advanced packaging → design/simulation co-design | relationship | `rel:requires` | Class: packaging technology `requires` EDA (SRC-004 p.5) |

## 9. Unknown and non-public edges

Three different situations are kept apart (D-031):

| Situation | How it is recorded | What it must never become |
|---|---|---|
| Nobody has looked | Nothing. A missing edge means "not recorded" | "no relationship"; a zero in a count; evidence of absence |
| The edge is known, but one qualifier is not (DEP-01: the HBM in a product, whose maker is unknown) | The edge, with `supplier` set to `not_researched`, or to `not_publicly_determinable` citing the claims that show it | a placeholder company (`company-unknown-supplier`); a supplier inferred from market share or from a supplier's customer list |
| Research found that a party is not disclosed, with no known edge to hang it on (e.g. which foundry fabricates a product, when no source says) | The claims that record the search (S06). No relationship record in v1 | a relationship with a fake or empty endpoint |

**Why the general case has no record type in v1** (D-031). S01's `not_publicly_determinable`
findings are about one supplier question (DEP-01, HBM-06) and about *quantities*:
deployment counts (DEP-12), wafer and die allocation (DEP-05, DEP-11), interconnection
use (DEP-16). Quantities are not edges. Only DEP-01 is about a party, and the `supplier`
qualifier covers it. An "unknown endpoint" record type would be machinery with no used
case (M0 audit A-1; L-09). If S10 meets the third situation often, it proposes one.

**Rules that follow:**

- a `not_publicly_determinable` value must cite claims that say *what was searched*. One
  page's silence supports only `not_researched` (§12, example 2);
- consumers must say "no recorded relationship", never "none", and S15 metrics must not
  count a missing edge as zero (RR-7, CLAUDE.md §7);
- the schema rejects placeholder endpoint IDs (`…-unknown…`, `…-tbd`, `…-undisclosed…` and
  similar).

## 10. Time

- **Instance-level edges** may carry `valid_from` and `valid_to`, as partial dates, when the
  cited claims give a period. Leaving them out means "the claims give no period". It is
  not a claim that the edge always held, or that it holds today. How current an edge is
  comes from its claims' dates (S06, `validate-freshness`).
- **Class-level edges** carry no dates (the schema forbids them). A statement that holds
  only for a period is contingent, and so it belongs at instance level or in claims.
- **Plans and announcements are events**, never edges (`entity-taxonomy.md` §4.4; DEP-04).
  An edge starts to exist when a claim supports the activity or state itself.
- **Events are not endpoints.** When S09 designs the event schema, it decides whether an
  event may *cite* an edge (e.g. an acquisition that starts an `owns` edge). An edge never
  points to an event.
- **Several periods are several records.** An operator that leaves a site and comes back
  has two `operates` edges, each with its own claims.
- `valid_from ≤ valid_to` needs a date comparison, so it is a `validate-data` check (§15).

## 11. Role and edge conflicts (future semantic warnings)

A role is claim-backed on the company (D-024). An edge is claim-backed on its own. When
they disagree, one of the claims is wrong, out of date, or about a different period. The
Atlas **flags** the disagreement (MA §14 Gate 3). It **never** corrects either record
automatically (D-033).

| ID | Warning when | Why it is a conflict |
|---|---|---|
| RW-1 | a company holds `fabless_designer` and `owns` or `operates` a facility with kind `wafer_fab`, over overlapping or undated periods | "fabless" asserts no fabs (ACC-04; D-024) |
| RW-2 | a company holds `fabless_designer` and `fabricates` a product, over overlapping or undated periods | the fabless model buys fabrication (ACC-04) |
| RW-3 | a company holds `fabless_designer` and `packages` a product, over overlapping or undated periods | the fabless model buys ATP (ACC-04, SRC-002 p.6) |

Not warnings, because they are not conflicts:

- an `idm`, `foundry_operator` or `memory_manufacturer` that `packages` (B-3);
- a `cloud_provider` that `designs` (B-2);
- an edge from a company whose `roles` are `not_researched`.

A missing role is not evidence against an edge, and a missing edge is not evidence
against a role (unknown ≠ none).

## 12. Worked examples (illustrations, not records)

No records are created in S04. Each example takes a sentence already evidenced in the
domain map and shows which records it supports, and which it does not. The quoted anchors
are checked against the domain map by the tests.

### Example 1 — DEP-05: a fabless designer and its foundry (SRC-006)

FAB-05 quotes SRC-006, an NVIDIA technical page, on the H100: "fabricated using the TSMC 4N process customized for NVIDIA".

| Candidate | Supported by this sentence? | Record |
|---|---|---|
| TSMC `fabricates` H100 | Yes, but as a short inference. The sentence names a *process* that carries TSMC's name, and reads it as fabrication by TSMC. The Verifier should label the claim `DERIVATION`, unless a source names TSMC as the manufacturer directly (§5, `fabricates`) | S10 edge candidate, citing that claim |
| H100's process | Yes: "TSMC 4N process customized for NVIDIA", verbatim | `product.vendor_process_name` on the H100 record. Not on the edge (§7) |
| NVIDIA `designs` H100 | **No.** The quoted anchor names no designer. NVIDIA being the vendor does not make it the designer (§4.5) | none until a claim states the design |
| NVIDIA holds `fabless_designer` | **No.** SRC-002 p.6 defines the model ("a fabless firm designs and sells the chip and purchases fabrication services from a foundry and ATP services from an outsourced semiconductor assembly and test (OSAT) firm") but does not name NVIDIA. The role is never inferred from the `fabricates` edge (D-024) | `roles` stays `not_researched` |
| Which TSMC fab | **No.** The sentence names no site | not recorded; never read off TSMC's headquarters or fab list (S09) |
| NVIDIA `depends_on` TSMC | Derivable from the edges above | not stored (RR-5); computed by S15 |

### Example 2 — DEP-01: a product uses HBM, and the supplier is unknown

Domain map DEP-01 records, as a `FACT`, that SRC-006 states the H100 uses HBM3. The entry
quotes no verbatim anchor for it. The source register's locator points to SRC-006's section
on the H100 HBM3 and HBM2e DRAM subsystems, so S10 must quote the anchor from there. HBM-06
records the gap: which HBM maker supplies which accelerator is not publicly determinable
"from the product documentation retrieved". The DEP-01 "Likely non-public" cell reads:
"which maker's HBM goes into which product (SRC-006 names none)".

| Candidate | Supported? | Record |
|---|---|---|
| H100 `incorporates` HBM | Yes, from the product documentation | an `incorporates` edge to the HBM component class. "HBM3" is a generation (HBM-05, future), not a separate class |
| Who supplies the H100's HBM | Not from the retrieved sources | `supplier: {state: …}` on that edge. `not_publicly_determinable` needs claims showing what was searched; one product page's silence supports only `not_researched` (§9). S10 decides which state the search supports |
| A placeholder company for the unknown HBM maker | **Never** | rejected by the schema (RR-7) |
| A memory maker `supplies` NVIDIA | **No.** SK hynix's HBM pages (SRC-011 to SRC-014) name no customer in the anchors quoted | none |
| Data-centre GPU `has_part` HBM (class level) | **No.** SK hynix says bandwidth demand "cannot be satisfied with conventional main memories" (SRC-012). That is a structural *need*, but HBM as the solution is contingent (DEP-01 Type) | none. The general statement is a derivation over product edges (§3) |

### Example 3 — DEP-04: an announced plan is an event, not an edge

HBM-03 quotes SRC-014, an SK hynix release dated 2024-04-19: the company "plans to adopt TSMC’s advanced logic process for HBM4’s base die". The same release gives the stack's structure: "HBM is made by stacking a core DRAM die on top of a base die that features TSV".

| Candidate | Supported? | Record |
|---|---|---|
| An announcement | Yes | an event (MA §5.5 `announced`, S09 schema) plus an `ATTRIBUTION` claim |
| TSMC `fabricates` an HBM4 product | **No.** DEP-04 asks for "later primary confirmation of production". Even when confirmed, TSMC would fabricate only the base die of a product whose DRAM dies SK hynix makes. `fabricates` has no way to name one constituent in v1, so S10 must stop and propose it (D-032), never record the whole product | none |
| HBM `has_part` HBM base die | Yes, a class-level structural statement | a `has_part` edge (component → component, both constituent) |
| HBM `requires` TSV | Yes, and DEP-03 cites further sources | a `requires` edge (component → technology) |

The same release supports one event and two class-level edges, and no instance edge.

## 13. Human focus: why these are different claims

Take one sentence type: "Company F makes Company D's chip."

| Claim | What it says | Evidence it needs | Type |
|---|---|---|---|
| F `fabricates` P | F runs the wafer process for product P | F, P and the fabrication step named | activity edge |
| F `packages` P | F assembles P's dies into its package | F, P and the packaging step named | activity edge |
| F `supplies` D (item) | F sells goods of some kind to D | both firms, the item, and a supply relation | activity edge |
| D `depends_on` F | D cannot get P without F | the edges above, *and* an assessment of alternatives | derivation (S15) |
| "F manufactures P" | any of the first three | cannot be checked, because it does not say which step | rejected |

- **`requires` vs "uses".** "HBM requires TSV" is a claim about the technology. "This GPU
  uses HBM" is a claim about one product. Only the first survives a new product design.
- **Relationship vs event.** "F operates Fab 1 (2021–2024)" holds over an interval.
  "F announced it will build Fab 2" happened on a date, and nothing is operated yet.
- **Relationship vs role.** "D is fabless" is D's business model (a role). "F fabricates
  P" is a fact about one product. Neither is inferred from the other (§11).
- **Relationship vs field.** "Fab 1 is in country Z" is a property of the site (a field).
  "F operates Fab 1" connects two records (an edge).

## 14. Candidates considered and rejected

| Candidate | Why not |
|---|---|
| One verb at both levels (e.g. `uses` for classes and products) | Structural and contingent claims would mix in every dependency query (§3; RR-2) |
| A stored `depends_on` between companies | A derivation (R-8, RR-5); criticality is S15's (NG-11) |
| Symmetric types (`competes_with`, `partners_with`) | No v1 question needs them; each is vague or derivable (§6) |
| Stored inverse edges (`fabricated_by`, `part_of`) | A second copy of one fact (RR-3) |
| `part_of` as the composition verb | Its direction (part → whole) would break the convention that structural edges point from dependent to dependency (§1). The inverse reading "part of" is kept for display |
| A process qualifier on `fabricates` | Second home for `product.vendor_process_name` (§7) |
| A `packaging_process` qualifier (CoWoS), or CoWoS as a technology record | No retrieved source ties a vendor-named packaging process to a named product; R-4 forbids vendor names as technologies (D-032) |
| A `part` qualifier on `fabricates` (constituent-level fabrication) | Its only v1 case is an announced plan (DEP-04). Designing it now would be machinery with no used case (A-1); S10 proposes it with the first confirmed case (D-032) |
| Company → class edges (`adopts`, "uses technology", "fabricates DRAM") | They restate roles (D-024) or become vague capability claims. What a firm does to a named product is an instance edge |
| An "unknown endpoint" record type | No v1 evidence needs it beyond DEP-01, which `supplier` covers (§9; D-031) |
| A `located_in` edge | Location is three accepted fields (§7) |
| Record-level `source_ids` (MA §5.4) | Cannot say which source supports the edge (D-028, D-025 precedent) |
| A confidence score on the edge | Confidence is the claim's evidence status (S06; L-06). A number would invent precision |
| Service → facility edge ("served from") | Providers abstract location (DC-04); the evidence is usually a region, which is not a site (D-022). S09 may propose one if evidence appears |
| A test step in `packages`, or an `assembles` / `tests` type | Package test and server integration are `not_researched` or future scope (domain map layer 3 exclusions; TQ-11) |
| A graph library or database to hold edges | NG-07; MA §18: relational tables first |

## 15. What S04 leaves to other sessions

| Item | Owner | Note |
|---|---|---|
| Preferred source class per row of §5, and for entity identity evidence | S05 | S05 gate: "Every material claim type has a preferred source class" |
| Claim schema: claim type and evidence status; what a `not_publicly_determinable` claim must record about the search | S06 | L-06; §9 |
| `validate-data` rules for edges (below) | S06/S07, with the first records | L-05, L-09: checks arrive with the data they check |
| Event schema; whether events may cite edges | S09 (D-022) | §10 |
| Which facility fabricates or packages a product (site-level production) | S09 proposes, if evidence exists | Not representable in v1; never derived from company-level edges |
| Constituent-level fabrication (`part` qualifier); vendor-named packaging processes | S10, stop-and-propose (D-032) | §4.6, §4.7 |
| First edges | S10 | "No relationship is published without evidence or an explicit non-published/unverified state" |
| `depends_on`, concentration, single-sourcing | S15 | derived from edges; `supplier` lists give the multi-sourcing evidence |
| Policy verbs (`restricted_by`, `regulated_by`, `supported_by`, `constrained_by`) | S17 | reserved; S17 defines or rejects them |

**`validate-data` rules for relationships** (for S06/S07; none is a gate until CI runs it,
L-02):

- **V-1:** every endpoint, `item` and `supplier` value resolves to an existing record of
  the prefixed type;
- **V-2:** the kind constraints in §2;
- **V-3:** no edge from a record to itself;
- **V-4:** `valid_from ≤ valid_to`, compared at the coarser precision of the two;
- **V-5:** no two records with the same type, endpoints and `item`, and overlapping
  periods. Extra evidence is extra claims on one record;
- **V-6:** a `requires` or `has_part` edge must not restate a `broader` link between the
  same records;
- **V-7:** in a `supplies` edge whose `item` is a product, the product's vendor is the
  source company (warning);
- **V-8:** the role and edge warnings RW-1 to RW-3 (§11);
- **V-9:** no placeholder slugs in entity IDs (the relationship schema already rejects
  them as endpoints).
