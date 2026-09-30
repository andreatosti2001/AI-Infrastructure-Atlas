# Entity taxonomy — canonical entity types for the first vertical

**Status:** PROPOSED. Decisions D-022 to D-025 await human review; D-026 is accepted.
**Session:** S03 · **Date:** 2026-09-30
**Inputs:**
- `milestone-audits/M0-audit.md` Part 4 (D-020);
- MA §5–6;
- `../research/domain-map.md` §2, §4, §7.1;
- `baseline.md` §2 and §6.

**Schema:** [`schemas/entities.schema.json`](../../schemas/entities.schema.json)

**One home for each kind of statement:**

- **This document** holds the reasoning:
  - why each type exists;
  - how to tell whether two records are the same thing;
  - what each type must not be confused with;
  - where every v1 concept and every MA entity type ends up.
- **The schema** holds the field shapes and the controlled-vocabulary values, each with
  its definition. This document names vocabulary values but does not define them.

**Claim labels.**
- The type design is the Atlas's choice (`INTERPRETATION`). Its consequences are
  `IMPLICATION`.
- Where a choice rests on evidence, it cites the S01 concept ID (e.g. `FAB-05`). The
  source, locator and quoted anchor stay in that domain-map entry, which is their one home.

---

## 1. Design rules

| ID | Rule | Why |
|---|---|---|
| R-1 | **A type needs its own identity test**: a rule that says when two records describe the same thing. Two candidates that share one identity test are one type with a kind field. | Stops types multiplying for labels (e.g. Fab, DataCentre) |
| R-2 | **A type needs a v1 use.** Every instantiable type is needed by at least one v1 concept (§5). | `SESSION-ROADMAP.md` S03 critical test: "No entity should exist merely because it is convenient for the UI" |
| R-3 | **Roles are not types.** What a company does (fabless, foundry, OSAT, cloud) is a claim-backed role *on* the company. | A firm typed by role would need several records, and so several homes for its facts (M0 Part 4; blurs B-2, B-3) |
| R-4 | **A class and a named offering are different types.** A vendor-neutral class (component, technology) is not a vendor's product. | `SESSION-ROADMAP.md` S08: model concepts "independently of company marketing language" |
| R-5 | **Location, ownership and operation are different facts.** A facility's location is a field on the facility. Ownership and operation are relationships (S04). Incorporation and headquarters are two separate company fields. | `SESSION-ROADMAP.md` S09 "Critical distinction" |
| R-6 | **Evidence and change are not world entities.** Sources and claims are evidence about entities. Events record change. Relationships connect entities. | MA §5.2–5.6; S06 gate "What exactly supports this relationship?" |
| R-7 | **Every substantive value is claim-backed or explicitly unresolved.** A missing field or `null` is invalid. Unknown is never zero or false. | CLAUDE.md §7; MA §5.7; D-025 |
| R-8 | **Nothing derivable is stored.** Status is derived from events, a record's layer from its concept references, and roles are never inferred from missing edges. | CLAUDE.md §7; MA §5.6; M0 audit K-1 |

## 2. The record kinds at a glance

The human's ten are in **bold**. The roadmap adds Institution and Relationship.

| Kind | Level | Status in v1 | Schema owner | Quick test |
|---|---|---|---|---|
| **Company** | world: commercial actor | instantiable | S03 | Can it own a site, sell a product and sign a contract? |
| **Facility** | world: place | instantiable | S03 | Is it a physical site where wafers are made, dies are packaged or computers are housed? |
| **Technology** | world: know-how | instantiable | S03 | Is it a way of making, integrating, designing or delivering that more than one vendor could use? |
| **Component** | world: class of physical item | instantiable | S03 | Is it a kind of physical item, described without naming a vendor? |
| **Product** | world: named offering | instantiable | S03 | Does a company offer it under its own name? |
| **Country** → Jurisdiction | world: authority over territory | instantiable, kind `country` only | S03 | Does it have its own legal authority and an ISO 3166-1 code? |
| Institution | world: non-commercial actor | reserved (defined, no records) | S05/S06 or S17 | Is it a public, standards or research body acting as such? |
| **Policy** | world: rule | reserved (defined, no records) | S17 | Is it a legal or governmental instrument? |
| **Source** | evidence | boundary defined here | S05/S06 | Is it a document or dataset that can be retrieved? |
| **Claim** | evidence | boundary defined here | S06 | Is it one proposition, with a claim type and an evidence status, tied to a source locator? |
| **Event** | change over time | boundary defined here | S09 (proposed, D-022) | Is it a dated occurrence that changed something? |
| Relationship | connection | boundary defined here | S04 | Is it a typed, directed statement linking two entities? |

## 3. Instantiable types

Each type below gives:
- its definition;
- its **identity test**;
- what it is **not**;
- the v1 concepts that need it;
- its fields, as a pointer to the schema;
- how time is handled.

### 3.1 Company

- **Definition:** a legal person that carries on commercial activity. It can own and
  operate facilities, offer products and enter contracts.
- **Identity:** one record per legal entity as sources name it. A renamed company keeps
  its ID.
  - A parent and a subsidiary are two records only when the evidence needs both, e.g.
    a facility operated by the subsidiary.
  - An `owns` relationship (S04) links them.
- **Not:**
  - a **role**: fabless designer, IDM, foundry operator, OSAT, memory manufacturer, cloud
    provider, equipment maker and EDA vendor are values of `roles` (D-024);
  - a brand: a brand is a `name` or an alias;
  - a **facility** (§4.2);
  - an institution;
  - a **jurisdiction**: a company's incorporation and headquarters are fields that
    point to jurisdiction records.
- **v1 need:** the actors behind every layer. The role concepts ACC-04, HBM-06, PKG-07,
  FAB-04, DC-04 and FAB-03 are roles on companies. Companies are also the endpoints of the
  S10 edges.
- **Fields:** `legal_name`, `incorporated_in`, `headquartered_in`, `roles`.
  - MA §5.1's example keeps a single `jurisdiction` field. It could mean where the
    company is incorporated, where it is headquartered, or where it produces.
  - These are three different facts. S09 keeps them apart, and the D-008 EU lens will
    need each one on its own. So there are two company fields, and production location
    sits on facilities.
- **Time:** roles and headquarters can carry `valid_from`/`valid_to`. Founding,
  dissolution and acquisitions are events.

### 3.2 Facility

- **Definition:** a physical site where wafers are fabricated, dies are assembled and
  packaged, or computing equipment is housed.
- **Identity:** one site at one location. The site keeps its ID when its owner or
  operator changes.
- **Not:**
  - a **company**: a company owns or operates a facility, and both links are S04
    relationships, never facility fields;
  - a **cloud region or availability zone**: AWS defines an availability zone as "one or
    more discrete data centers" (DC-04). It is a provider's grouping, not a site (§8);
  - a jurisdiction: `located_in` points to one;
  - a production line or clean room (sub-site detail, future).
- **v1 need:**
  - FAB-02 (kind `wafer_fab`);
  - DC-01 (kind `data_centre`);
  - the packaging facility in domain map §4, layer 3 (kind `packaging_facility`);
  - the S09 temporal facility model;
  - D-008 location evidence.
- **Fields:** `facility_kinds`, `located_in`, `locality`, `nameplate_it_capacity_mw`.
  - `facility_kinds` takes several values, because one site can fabricate wafers and
    also package dies (B-3).
  - Capacity is recorded only as nameplate IT capacity (EN-04, TQ-10).
  - Interconnection capacity (EN-02) stays concept-only (NG-05).
- **Time:** opening, closure and expansion are events. A facility's operating status is
  derived from them (MA §5.6), never stored.

### 3.3 Technology

- **Definition:** a vendor-neutral way of making, integrating, designing or delivering
  something.
- **Identity:** one technical definition. Two names for one technique are aliases of one
  record. A vendor's own named implementation is not a separate technology (§4.2,
  Technology vs Product).
- **Not:**
  - a **component**: a technology is applied, while a component is shipped or installed.
    TSV (HBM-04) is a technique, and an HBM stack (HBM-02) is an item made with it;
  - a product;
  - a claim about the technology.
- **v1 need:** HBM-04, PKG-03, PKG-04, PKG-05, PKG-06, SME-03, ACC-05, EDA-01, DC-02.
- **Fields:** `technology_kind`, `broader`, `concept_refs`, `definition`.
  - `broader` allows several parents, because TSV spans packaging and wafer processing
    (B-1).
  - `broader` is taxonomy only ("is a kind of"). "Requires" and "is part of" are S04
    relationships. Keeping them apart stops a dependency query from walking up a
    classification tree by mistake.
- **Time:** a technology is a durable concept. Its adoption by a company is a
  relationship or an event.

### 3.4 Component

- **Definition:** a vendor-neutral class of physical item. Either it is built into AI
  compute hardware (`use_class: constituent`) or it is used to make that hardware
  (`use_class: production_equipment`).
- **Identity:** one class, defined technically, without naming a vendor.
- **Not:**
  - a **product**: "data-centre GPU" (ACC-02) is a class, and a named GPU is a product;
  - a technology (see §3.3);
  - a facility.
- **Why equipment is a Component, not its own type:**
  - Under R-1, an equipment class and a chip class share one identity test: a
    vendor-neutral class of physical item.
  - They differ in how they enter the chain: built in, or used to make. `use_class`
    records that difference, and S04's endpoint rules can use it.
  - A separate Equipment type was considered and rejected (§8).
- **v1 need:**
  - constituents: ACC-01, ACC-02, ACC-03, HBM-02, HBM-03, DC-05;
  - production equipment: SME-01, SME-06.
- **Fields:** `use_class`, `broader`, `concept_refs`, `definition`.
  - Composition ("an HBM base die is part of an HBM stack", HBM-03) is an S04
    relationship, not `broader`.

### 3.5 Product

- **Definition:** a specific commercial offering, named by the company that offers it.
  It can be a chip, a memory product, a system, a software product or a service.
- **Identity:** the vendor plus the product name the vendor uses.
  - A separately named model is a separate record.
  - Product families and generations (e.g. HBM generations, HBM-05) are future scope
    (S08).
- **Not:**
  - a component class;
  - a technology;
  - a company;
  - a "chip design". MA §6.1's `ChipDesign` is folded into Product for v1 (D-023).
- **The vendor is not the maker.**
  - `vendor` is part of identity: whose name the offering carries.
  - Who designs, fabricates or packages the product are S04 relationships. For a
    fabless vendor they are different companies.
- **v1 need:**
  - FAB-05: TQ-07 says to record "each chip's process as the vendor names it", so the
    process name belongs to the chip product;
  - EN-03 and DC-06, whose attributes belong to chips and systems;
  - the named endpoints that the S10 edges and dependencies DEP-01 and DEP-14 need.
- **Fields:** `vendor`, `product_kind`, `instance_of`, `vendor_process_name`, `tdp_w`,
  `rated_power_w`, `rack_scale`, `cooling_method`. An attribute that does not apply to
  the product (e.g. `tdp_w` on a cloud service) is `not_applicable`.
- **Open:** no roadmap session is assigned to create product records (§9).

### 3.6 Jurisdiction ("Country")

- **Definition:** a territory with its own legal authority. The only kind allowed in v1
  is `country`.
- **Identity:** the ISO 3166-1 alpha-2 code. The record ID is `jurisdiction-` plus the
  code in lower case, so the code has one home.
  - The code is used as an identifier. It states no position on sovereignty.
  - The ISO standard itself is not yet in the source register (§9).
- **Why "jurisdiction" and not "country":**
  - `SESSION-ROADMAP.md` S03 says "Country/Jurisdiction", and MA §5.1 says
    "country/jurisdiction".
  - The D-008 EU lens and the S17 policy layer will need a supranational jurisdiction:
    the EU. Naming the type now avoids a rename later.
  - Until then, only `country` is allowed.
  - EU membership changes over time, so it will be a relationship, not a field.
- **Not:**
  - a facility's locality;
  - a government body: that is an institution, reserved;
  - a policy.
- **v1 need:** D-008 asks every session to record location and jurisdiction evidence. The
  fields that point to jurisdictions are `incorporated_in`, `headquartered_in` and
  `located_in`.

### 3.7 Reserved types: Institution and Policy

Both are defined here so that their boundaries are clear. Neither has a schema, so the
schema rejects any record of either type.

- **Institution:**
  - **Definition:** a non-commercial organisation acting as a public authority,
    standards body or research organisation.
  - **Examples:** the S01 publishers NIST, LBNL and CSET, and the JEDEC standards body
    (the JEDEC source was blocked).
  - **Not a company**, because it holds no supply-chain role in v1.
  - **Open:** S05/S06 decide whether a source's publisher becomes a reference to a
    company or institution record. Today the publisher is text. Where the publisher is
    also a company (SK hynix, NVIDIA), that text is a weak second home.
- **Policy:**
  - **Definition:** a legal or governmental instrument that constrains or supports an
    activity, such as a law, regulation, export-control rule or subsidy programme.
  - **Not an event.** A policy's adoption is an event. A statement about a policy is a
    claim.
  - **Start:** S17. The policy layer must not duplicate `Eu-Digital-Policy` (baseline §2).
  - **Open:** S17 decides whether MA §6.1's `PolicyInstrument`, `TradeMeasure` and
    `ExportControl` are kinds of Policy.

## 4. Why the ten are distinct (human focus)

### 4.1 Four questions sort every candidate

```text
1. Is it evidence ABOUT the world?
     a document or dataset .............................. Source
     one proposition, typed and located ................. Claim
2. Is it a dated CHANGE? .................................. Event
3. Is it a LINK between two records? ...................... Relationship
4. Otherwise it is IN the world. What is it?
     can own, sell and contract (commercial) ............ Company
     public, standards or research body ................. Institution (reserved)
     territory with its own legal authority ............. Jurisdiction ("Country")
     a legal or governmental instrument ................. Policy (reserved)
     a physical site .................................... Facility
     a way of making, designing or delivering ........... Technology
     a kind of physical item, no vendor named ........... Component
     a named offering of a named company ................ Product
```

### 4.2 The pairs most easily confused

| Pair | The difference | Why it matters for the governing question |
|---|---|---|
| Company vs Facility | A company contracts. A facility has a location. Ownership and operation link them as relationships. | A dependency sits where production happens. That can differ from where the firm is based (S09). |
| Company vs Jurisdiction | Incorporation, headquarters and each facility's location are three separate facts, each pointing to a jurisdiction. | The later EU lens (D-008) needs each one separately. Folding them into one field would make the lens unanswerable. |
| Company vs role | "Foundry" names what a company does, not what it is. Cloud providers also design accelerators (B-2). Foundries and memory makers also package (B-3). | One firm keeps one record, whatever roles it holds. |
| Technology vs Component | TSV is a technique (HBM-04). An HBM stack is an item made with it (HBM-02). | "Which items depend on TSV?" and "which technologies does HBM require?" are different queries. |
| Component vs Product | "Data-centre GPU" is a class (ACC-02). A named GPU is a vendor's product. | Some dependencies hold for a whole class: current accelerators use HBM (DEP-01). Others are product-specific. Which HBM maker supplies which product is `not_publicly_determinable` from the product documentation retrieved so far (HBM-06). |
| Technology vs Product | 2.5D interposer packaging is vendor-neutral (PKG-04). SK hynix describes CoWoS as "A TSMC proprietary packaging process" (PKG-04, SRC-014), which is one vendor's implementation of it. | Vendor names never become technology records (R-4). How to hold a vendor-named process on a packaging edge is S04/S10's call (§9). |
| Policy vs Event vs Claim | The rule; the dated act of adopting or changing it; a statement about either. | Status is derived from events (MA §5.6), and each statement stays traceable. |
| Source vs Claim | One page (SRC-006) supports several claims. One claim can cite several sources: S01 `FACT`s often rest on two. | Provenance attaches to each proposition, not to a whole document. |
| Claim vs Relationship | A relationship is the structured statement "A fabricates B". Claims are what support it. | The S06 gate, "What exactly supports this relationship?", is answered by the claims. |
| Event vs Relationship | A relationship holds over an interval. An event happens at a date. | An announced plan is an event plus a claim. It is not yet a relationship (§4.4). |

### 4.3 Worked example 1: one sentence, six kinds of record

SRC-006 (NVIDIA technical blog, via FAB-05) says the H100 GPU is "fabricated using the TSMC
4N process customized for NVIDIA". This is an illustration, not a record. No records are
created in S03.

| Kind | What the sentence gives | What it does not give |
|---|---|---|
| Source | SRC-006, an NVIDIA web page, as registered in S01 | — |
| Claim | One proposition, reported by the company about its own product. A company source is primary for its own products (D-015 tier caveat). | Its claim type and evidence status are set by the S06 claim model, not here |
| Company | NVIDIA (the vendor); TSMC (named inside the process name) | Either company's incorporation or headquarters |
| Product | H100: vendor NVIDIA, an instance of the data-centre GPU class. `vendor_process_name` is the vendor's words, verbatim, not converted to a node number (TQ-07). | Any leading-edge label (TQ-07) |
| Component | The class "data-centre GPU" (ACC-02) | — |
| Relationship | A candidate S10 edge: TSMC fabricates the H100 | S03 creates no edges. S04 defines the verb |
| Facility, Jurisdiction | Nothing. The sentence names no fab and no place. | The fabrication location stays `not_researched`. Reading it off the foundry's headquarters would be the S09 conflation. |
| Event | Nothing. The sentence carries no date. | The page's publication date is metadata on the source, not the date of an event |

### 4.4 Worked example 2: a plan is not an edge

SRC-014 is an SK hynix press release dated 2024-04-19 (via HBM-03 and DEP-04). It says
the company "plans to adopt TSMC’s advanced logic process for HBM4’s base die".

- **Event:** an announcement (MA §5.5 `announced`). The date that is evidenced is the
  date of the release.
- **Claim:** `ATTRIBUTION`, a plan stated by one company.
- **Relationship: none yet.** A TSMC → HBM4 base-die manufacturing edge needs "later
  primary confirmation of production" (DEP-04, "Evidence that would establish it").
- **Component:** the class is the HBM base die (HBM-03). "HBM4" is a generation (HBM-05,
  future scope).

### 4.5 What changes from MA §5.1's example record

MA §5.1 shows a record with the fields `id`, `type`, `name`, `jurisdiction`, `status`
and `source_ids`. The Atlas makes three changes:

| MA field | Atlas | Reason |
|---|---|---|
| `jurisdiction` | Split into `incorporated_in` and `headquartered_in`, plus `located_in` on facilities | Three facts (§4.2) |
| `status: "active"` | Removed | A derived status is not stored (MA §5.6, MA's own rule; R-8) |
| `source_ids` on the record | Replaced by `claim_ids` on each value, plus `identity_claim_ids` | A list of sources for the whole record cannot say which source supports which value |

MA §5 expects physical schemas to differ while the concepts converge ("even if physical
schemas differ"). These changes put MA's concepts into practice; they do not override
them (D-023).

## 5. v1 concept mapping (machine-checked)

Every v1 concept in M0 Part 4 appears here exactly once.

- **D-020 class** copies Part 4.
- **S03 class** differs from it only where the note cites the decision that changes it.
- **Target** shows where the concept lives:
  - `type:<entity type>`: records of that type;
  - `role:<value>` and `facility_kind:<value>`: vocabulary values in the schema;
  - `attribute:<type>.<field>`: a field;
  - `none`: no record or field.

`tests/test_entity_taxonomy.py` checks this table against Part 4, and every target
against the schema.

| Concept | Name | D-020 class | S03 class | Target | Note |
|---|---|---|---|---|---|
| ACC-01 | AI accelerator | model | model | `type:component` | constituent; the top class of accelerators (TQ-01: GPUs and AI ASICs) |
| ACC-02 | Data-centre GPU | model | model | `type:component` | constituent; `broader` = the ACC-01 record |
| ACC-03 | AI ASIC | model | model | `type:component` | constituent; `broader` = the ACC-01 record |
| ACC-05 | Multi-die accelerator | model | model | `type:technology` | kind `design_approach`; "multi-die", not "chiplet" (TQ-09) |
| HBM-02 | High Bandwidth Memory | model | model | `type:component` | constituent |
| HBM-03 | HBM base die | model | model | `type:component` | constituent; "part of an HBM stack" is an S04 relationship |
| HBM-04 | Through-silicon via | model | model | `type:technology` | kind `process`; may have several `broader` parents (B-1) |
| PKG-03 | Advanced packaging | model | model | `type:technology` | kind `process`; narrow working definition (TQ-03) |
| PKG-04 | 2.5D packaging with an interposer | model | model | `type:technology` | kind `process` |
| PKG-05 | 3D die stacking | model | model | `type:technology` | kind `process`; HBM stacking only in v1 |
| PKG-06 | Multi-die package | model | model | `type:technology` | kind `process`; "chiplet" only where a source uses it (TQ-09) |
| FAB-02 | Fab | model | model | `facility_kind:wafer_fab` | the concept is a kind; each fab is a facility record |
| FAB-03 | Foundry | model | actor role | `role:foundry_operator` | reclassified by D-024: TQ-04 made "foundry" a business model and "foundry operator" the firm |
| SME-01 | Semiconductor manufacturing equipment | model | model | `type:component` | production equipment; the top equipment class |
| SME-03 | EUV and DUV lithography | model | model | `type:technology` | kind `process`; whether scanners also get equipment classes is S08's call |
| SME-06 | Assembly, packaging and wafer-level packaging tools | model | model | `type:component` | production equipment |
| EDA-01 | Electronic design automation | model | model | `type:technology` | kind `software`; vendors' EDA tools are products |
| DC-01 | Data centre | model | model | `facility_kind:data_centre` | the concept is a kind; each data centre is a facility record |
| DC-02 | Cloud computing | model | model | `type:technology` | kind `service_model`; a provider's cloud service is a product (kind `service`) |
| DC-05 | Accelerated server | model | model | `type:component` | constituent; server-integration actors `not_researched` (TQ-11) |
| ACC-04 | Fabless chip designer | actor role | actor role | `role:fabless_designer` | |
| HBM-06 | Memory manufacturer | actor role | actor role | `role:memory_manufacturer` | |
| PKG-07 | OSAT firm | actor role | actor role | `role:osat` | |
| FAB-04 | Integrated device manufacturer | actor role | actor role | `role:idm` | |
| DC-04 | Cloud provider | actor role | actor role | `role:cloud_provider` | the entry's "cloud location abstraction" part is not modelled in v1 (§8) |
| FAB-05 | Process technology (vendor-named) | attribute | attribute | `attribute:product.vendor_process_name` | verbatim vendor wording (TQ-07) |
| DC-06 | Rack-scale architecture and liquid cooling | attribute | attribute | `attribute:product.rack_scale`, `attribute:product.cooling_method` | on system products |
| EN-03 | Chip and server power ratings | attribute | attribute | `attribute:product.tdp_w`, `attribute:product.rated_power_w` | TDP for chips, rated power for servers |
| EN-04 | Facility power capacity (nameplate IT) | attribute | attribute | `attribute:facility.nameplate_it_capacity_mw` | never interconnection capacity (TQ-10) |
| EN-01 | PUE and facility overhead | energy, concept only | energy, concept only | `none` | NG-05 |
| EN-02 | Grid interconnection capacity | energy, concept only | energy, concept only | `none` | NG-05; no interconnection field |
| X-01 | AI compute | definitional | definitional | `none` | the object of the question, not a record |
| HBM-01 | DRAM | definitional | definitional | `none` | |
| PKG-01 | Semiconductor packaging | definitional | definitional | `none` | |
| PKG-02 | Assembly, test and packaging | definitional | definitional | `none` | |
| FAB-01 | Wafer fabrication | definitional | definitional | `none` | |
| SME-02 | Lithography | definitional | definitional | `none` | |
| SME-04 | Core wafer-processing tools | definitional | definitional | `none` | |
| EDA-03 | Design-to-manufacturing handoff | definitional | definitional | `none` | kept as dependency DEP-10 for S04 |
| DC-03 | Infrastructure as a Service | definitional | definitional | `none` | |

## 6. MA entity-type dispositions (machine-checked)

Every entity type listed in MA §6.1 ("Core entities") and MA §5.1 ("Core types") gets a
disposition. The Target column uses the §5 syntax plus:
- `kind:<source|claim|event|relationship>`: a record kind owned by another session;
- `reserved:<institution|policy>`: a type that is defined but has no schema yet.

| MA item | MA § | Disposition | Target | Decision |
|---|---|---|---|---|
| Company | 6.1 | adopted | `type:company` | D-022 |
| Country | 6.1 | adopted as jurisdiction, kind `country` | `type:jurisdiction` | D-022 |
| Facility | 6.1 | adopted | `type:facility` | D-022 |
| Technology | 6.1 | adopted | `type:technology` | D-022 |
| Component | 6.1 | adopted | `type:component` | D-022 |
| Product | 6.1 | adopted | `type:product` | D-022 |
| CloudProvider | 6.1 | a role, not a type (R-3) | `role:cloud_provider` | D-023 |
| DataCentre | 6.1 | a facility kind (R-1) | `facility_kind:data_centre` | D-023 |
| ChipDesign | 6.1 | folded into product for v1 | `type:product` | D-023 |
| Fab | 6.1 | a facility kind (R-1) | `facility_kind:wafer_fab` | D-023 |
| PackagingFacility | 6.1 | a facility kind (R-1) | `facility_kind:packaging_facility` | D-023 |
| EquipmentSupplier | 6.1 | a role, not a type (R-3) | `role:equipment_maker` | D-023 |
| EnergyAsset | 6.1 | excluded from v1 | `none` | NG-05 |
| NetworkAsset | 6.1 | excluded from v1 | `none` | NG-04 |
| PolicyInstrument | 6.1 | reserved for S17 | `reserved:policy` | D-023 |
| TradeMeasure | 6.1 | reserved for S17, which decides whether it is a kind of Policy | `reserved:policy` | D-023 |
| ExportControl | 6.1 | reserved for S17, which decides whether it is a kind of Policy | `reserved:policy` | D-023 |
| Investment | 6.1 | an event (MA §5.5 `invested`), not an entity | `kind:event` | D-023 |
| Metric | 6.1 | a derivation, not a canonical entity (S14–S15) | `none` | NG-11 |
| Source | 6.1 | record kind owned by S05/S06 | `kind:source` | D-022 |
| Claim | 6.1 | record kind owned by S06 | `kind:claim` | D-022 |
| Event | 6.1 | record kind, schema proposed for S09 | `kind:event` | D-022 |
| Relationship | 6.1 | record kind owned by S04 | `kind:relationship` | D-022 |
| company | 5.1 | adopted | `type:company` | D-022 |
| country/jurisdiction | 5.1 | adopted, kind `country` only in v1 | `type:jurisdiction` | D-022 |
| institution | 5.1 | reserved (§3.7) | `reserved:institution` | D-022 |
| regulation/instrument | 5.1 | reserved for S17; regulatory content belongs to the governance repositories (baseline §2) | `reserved:policy` | D-023 |
| provision | 5.1 | outside this repository (MA §3.3; baseline §2) | `none` | D-023 |
| technology | 5.1 | adopted | `type:technology` | D-022 |
| component | 5.1 | adopted | `type:component` | D-022 |
| facility | 5.1 | adopted | `type:facility` | D-022 |
| product | 5.1 | adopted | `type:product` | D-022 |
| infrastructure asset | 5.1 | v1 kinds covered by facility; energy and network assets excluded | `type:facility` | D-023 |
| policy instrument | 5.1 | reserved for S17 | `reserved:policy` | D-023 |
| standard | 5.1 | not an entity in v1: a cited standard is a source; a standard as an instrument is S17's | `kind:source` | D-023 |
| event | 5.1 | record kind, schema proposed for S09 | `kind:event` | D-022 |
| metric | 5.1 | a derivation, not a canonical entity (S14–S15) | `none` | NG-11 |
| dependency | 5.1 | not an entity: a structural dependency is a relationship (S04); a criticality assessment is a derivation (S15) | `kind:relationship` | D-023 |
| relationship | 5.1 | record kind owned by S04 | `kind:relationship` | D-022 |
| claim | 5.1 | record kind owned by S06 | `kind:claim` | D-022 |
| source | 5.1 | record kind owned by S05/S06 | `kind:source` | D-022 |

## 7. The attribute contract (D-025)

The schema is the home of the exact shapes. This section says what they mean.

- **Identity fields:** `id`, `type`, `name`, `aliases`, `identity_claim_ids`, and each
  type's kind and class fields (`vendor` and `instance_of` on products, for example).
  They say *what the record is*.
  - `identity_claim_ids` must list at least one claim establishing that the thing exists
    and is of this type. This is the S07 gate: "identity evidence".
  - `name` is an editorial label. Where the sourced name matters, it goes in a separate
    field (`legal_name`).
- **Attributes:** every other field, such as `headquartered_in` or `tdp_w`. They say
  *what is true of it*. Each attribute holds one of two things:
  - **a list of assertions**, each with `value`, `claim_ids` (at least one) and, where
    the source gives a period, `valid_from`/`valid_to`. Several assertions can record
    history (a headquarters move) or several parallel values (roles); or
  - **an explicit state:** `not_researched`, `not_publicly_determinable` (which must cite
    the claims that show it) or `not_applicable`.
- **Every field of a type is required.** Leaving a field out, or setting it to `null`, is
  invalid. So "we did not look" can never pass for "there is nothing".
- **Unknown is never zero or false.**
  - Power and capacity values must be greater than zero.
  - A boolean is `false` only when a source states the negative.
- **Evidence states live on claims.** `verified` and `disputed` describe evidence (MA
  §5.7, MA §10), so they are properties of claims (S06). Competing values of an
  attribute are several assertions, each citing its own claims.
- **No free-text `notes`, no `status`, no `layer`.**
  - A notes field would become a hidden second home for facts. Commentary belongs on
    claims.
  - Status is derived from events.
  - The layer comes from the prefix of `concept_refs` (R-8).
- **References are typed by ID prefix.** For example, `vendor` must be a `company-…` ID.
  The schema checks the prefix. Whether the referenced record exists is checked later by
  `validate-data` (§9).
- **The claim ID format** (`claim-<slug>`) is fixed here so that references have a
  checkable shape. The claim record itself is S06's; S06 may change the format through a
  decision record.

## 8. Candidates considered and rejected

These candidates are not in MA's lists. They were considered because the S01 sources or
the chain suggested them.

| Candidate | Why not |
|---|---|
| A **layer** field or entity (layers 1–7) | Derivable from the prefix of `concept_refs` (R-8). A stored layer would be a second home |
| **Hyperscaler** as a role or type | No retrieved source defines it; TQ-08 excludes it until an authoritative definition is sourced |
| **Cloud region / availability zone** as a facility kind | A provider's grouping of one or more data centres (DC-04), not a site. v1 records cloud capacity at the data centres a source names; otherwise the location is `not_publicly_determinable` (domain map §6). A separate type can be proposed if S09 needs one |
| A separate **Equipment** type | Same identity test as Component (R-1). The difference is carried by `use_class` |
| An **Organisation** supertype over Company and Institution | It would mix supply-chain actors with evidence and policy actors. A state-owned firm that sells goods is a company. State ownership would be an `owns` relationship (S04/S17) |
| **Product family / generation** records | Future (HBM-05, S08) |
| A **brand** type | A brand is a `name` or an alias |
| A **leading-edge** flag | No threshold in v1 (TQ-07) |
| An **interconnection capacity** field | EN-02 is concept-only (NG-05) |
| Deriving roles from relationships | "Fabless" means *no* fabs, and incomplete data cannot establish an absence (unknown ≠ none). Roles are claim-backed (D-024) |

## 9. What S03 leaves to other sessions

| Item | Owner | Note |
|---|---|---|
| Relationship vocabulary, including ownership, operation, composition (`part_of`) and design/fabrication/packaging | S04 | Constraints to respect: endpoints typed by entity type and `use_class`; no taxonomic `is_a` relationship, because taxonomy is `broader`; how to hold vendor-named processes on edges (e.g. CoWoS) |
| Source schema; linking a publisher to a company or institution record | S05/S06 | §3.7 |
| Claim schema, including claim type and evidence status as two fields (L-06) | S06 | The ID format is fixed here (§7) |
| Event schema and event-type vocabulary | S09 (proposed, D-022) | S09's gate is the temporal facility model |
| `validate-data`: IDs unique; references resolve; `broader` acyclic; `valid_from` ≤ `valid_to`; jurisdiction IDs on the ISO list; warnings when roles and relationships conflict | S06/S07, with the first records | L-05, L-09: the checks arrive with the data they check |
| Which session creates product records | **unassigned** (S08 or S10) | Needs a human decision before S08 |
| Institution and Policy schemas | S05/S06 (institution, if publishers link to it); S17 (policy) | §3.7 |
| Registering the ISO 3166-1 standard as a source | S07, with the first jurisdiction records | §3.6 |
