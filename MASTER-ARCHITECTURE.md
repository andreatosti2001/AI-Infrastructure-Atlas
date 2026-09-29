# AI Technology Policy Intelligence — Master Architecture

**Status:** Architecture baseline v0.1
**Date:** 2026-09-28
**Primary implementation partner:** Claude Opus 5.5 via vibecoding
**Methodological reference only:** `andreatosti2001/Eu-Digital-Policy`
**Protection rule:** `Eu-Digital-Policy` is an existing portfolio product and should not be materially refactored, expanded into other domains, or made a runtime dependency of the new projects.

## 1. Purpose

This document defines the architecture for a portfolio of interoperable research and decision-support projects around AI governance, digital regulation, AI infrastructure, industrial policy and technological dependencies.

The portfolio has two explicit objectives:

1. **Learning objective:** force deep, evidence-backed study of the domains through building functioning systems rather than merely reading material.
2. **Professional objective:** produce demonstrable, client-facing systems showing research, data modelling, regulatory analysis, automation, software engineering, provenance, QA and analytical communication.

The portfolio must not become a collection of attractive AI-generated websites. The underlying asset is a reproducible **Technology Policy Intelligence System**.

---

## 2. Product thesis

The user should not enter the system merely to browse information.

The system should help the user answer questions such as:

- What rules apply to this technology, product or business model?
- What changed recently?
- Which institutions and jurisdictions matter?
- What infrastructure and supply chains does this technology depend on?
- Where are strategic dependencies concentrated?
- Which companies, technologies or facilities sit on those dependencies?
- What evidence supports each substantive finding?
- What should a researcher, analyst or client monitor next?

The core product pattern is therefore:

`Question -> Scope -> Evidence -> Structured knowledge -> Analysis -> Decision-support output`

The system must preserve the distinction between:

`Fact -> Attribution -> Derivation -> Interpretation -> Implication`

It must never collapse these into an undifferentiated AI answer.

---

## 3. Portfolio architecture

The portfolio is deliberately split into domain products rather than one giant repository.

```text
                         TECHNOLOGY POLICY INTELLIGENCE
                                      |
                +---------------------+---------------------+
                |                     |                     |
                v                     v                     v
       EU DIGITAL POLICY     AI INFRASTRUCTURE ATLAS    GLOBAL AI GOVERNANCE
       What regulates?       What enables AI?            How is AI governed?
                |                     |                     |
                +---------------------+---------------------+
                                      |
                                      v
                         AI TECHNOLOGY SOVEREIGNTY
                         How do they interact?
```

### Portfolio projects

#### 3.1 `Eu-Digital-Policy`

**Role:** EU regulatory reference layer.

**Question:** What does the EU digital regulatory framework say, when does it apply, who is responsible, how is it enforced, and how do instruments interact?

This remains a focused regulatory intelligence product. Do not turn it into the universal home for infrastructure, geopolitics or industry data.

The existing repository should remain a stable reference implementation for evidence discipline, claim provenance, regulatory data modelling, agent governance and regression QA. **Do not materially modify it for the sake of the new portfolio.** Its scope remains EU digital regulation. Any lessons learned should be reimplemented independently in the new repositories unless there is a strong reason to extract a standalone shared component later.

#### 3.2 `AI-Infrastructure-Atlas`

**Role:** AI industrial and physical layer.

**Question:** What physical, industrial and economic systems make modern AI possible, and where are the dependencies?

Core domains:

- energy
- data centres
- connectivity/networking
- semiconductor design
- EDA
- wafers
- fabs
- manufacturing equipment
- advanced packaging
- HBM/memory
- AI accelerators
- cloud
- compute capacity
- foundation/open-weight models
- application layer

#### 3.3 `Global-AI-Governance`

**Role:** comparative governance layer.

**Question:** How do different jurisdictions and international institutions govern AI, using which instruments and institutions?

Primary coverage:

- European Union
- United States
- China
- OECD
- Council of Europe
- UNESCO
- UN
- G7/G20
- ISO/IEC and other standards ecosystems

Do not reduce this project to a catalogue of statutes. Model governance mechanisms: legislation, executive action, agency action, standards, procurement, certification, export controls, licensing, competition rules, guidance, voluntary frameworks and treaties.

#### 3.4 `AI-Tech-Sovereignty`

**Role:** integration / decision-support layer.

**Question:** How do regulation, infrastructure, industrial capacity and geopolitics interact?

This is not the place to duplicate all underlying records. It should consume validated records and relationships from the domain products and generate cross-domain analysis.

---

## 4. Repository strategy

### 4.1 Protect `Eu-Digital-Policy`

Treat the existing repository as a **stable finished/continuing portfolio product**, not as the codebase from which the new projects should evolve.

The default rule is:

> **New project work must not require changes to `Eu-Digital-Policy`.**

Changes to that repository should happen only when independently justified by its own roadmap. A need arising from `AI-Infrastructure-Atlas`, `Global-AI-Governance` or `AI-Tech-Sovereignty` is not by itself a valid reason to modify it.

### 4.2 Reuse methodology, not architecture by inheritance

The new repositories may study and reproduce patterns visible in `Eu-Digital-Policy`: claim-level provenance, source hierarchy, verification, controlled vocabularies, bounded agents, freshness and regression QA.

Do not initially copy its application code, folder tree, deployment system or data files. This keeps the new projects independently understandable and avoids turning the older repository into a fragile monorepo-by-proxy.

### 4.3 Independent repository topology

```text
portfolio/
├── Eu-Digital-Policy/                 # protected existing product
├── AI-Infrastructure-Atlas/           # independent new product
├── Global-AI-Governance/               # independent new product
└── AI-Tech-Sovereignty/               # independent integration product
```

There is intentionally no shared package in v1. If genuinely identical abstractions emerge across multiple new repositories, extract them only after the repetition is demonstrated and the extraction reduces rather than increases complexity.

### 4.4 GitHub strategy

Each domain product should have:

- `main` = reviewed/deployable state
- short-lived feature branches
- architecture documents committed alongside implementation
- issues or task ledger for governed work
- release notes for meaningful data-model changes

Never ask an agent to work from an assumed repository tree. It must inspect the actual branch and current files first.

---

## 5. Shared conceptual data contract

The **new projects** should converge on these concepts, even if physical schemas differ. `Eu-Digital-Policy` remains conceptually compatible but is not required to adopt the new schema.

### 5.1 Entity

Represents a durable object.

```json
{
  "id": "company-nvidia",
  "type": "company",
  "name": "NVIDIA",
  "jurisdiction": "US",
  "status": "active",
  "source_ids": ["source-123"]
}
```

Core types:

- company
- country/jurisdiction
- institution
- regulation/instrument
- provision
- technology
- component
- facility
- product
- infrastructure asset
- policy instrument
- standard
- event
- metric
- dependency
- relationship
- claim
- source

### 5.2 Claim

A claim is a substantive proposition that must be traceable to evidence or explicitly classified as synthesis/analysis.

```json
{
  "id": "claim-001",
  "statement": "...",
  "claim_type": "fact",
  "evidence_status": "direct",
  "source_ids": ["source-001"],
  "locator": "section 4.2 / page 17",
  "verified_at": "2026-09-28",
  "notes": null
}
```

### 5.3 Source

```json
{
  "id": "source-001",
  "publisher": "...",
  "title": "...",
  "url": "...",
  "publication_date": "2026-09-01",
  "source_type": "official",
  "source_tier": 1,
  "accessed_at": "2026-09-28"
}
```

### 5.4 Relationship

```json
{
  "id": "rel-001",
  "source_entity": "company-nvidia",
  "relation_type": "manufactures",
  "target_entity": "component-gpu",
  "valid_from": null,
  "valid_to": null,
  "source_ids": ["source-002"]
}
```

### 5.5 Event

Use dated events instead of embedding time facts everywhere.

Examples:

- adopted
- published
- entered_into_force
- applied
- amended
- acquired
- opened
- closed
- announced
- invested
- restricted
- sanctioned
- updated

### 5.6 Status semantics

Never use one overloaded status field when a state is derived from events.

Prefer:

`event records -> deterministic derivation -> rendered status`

### 5.7 Null semantics

`null` is not the same as `unknown`.

Use explicit states where necessary:

- `not_researched`
- `not_publicly_determinable`
- `not_applicable`
- `verified`
- `disputed`

Unknown is never zero.

---

## 6. AI-Infrastructure-Atlas domain model

### 6.1 Core entities

```text
Company
Country
Facility
Technology
Component
Product
CloudProvider
DataCentre
ChipDesign
Fab
PackagingFacility
EquipmentSupplier
EnergyAsset
NetworkAsset
PolicyInstrument
TradeMeasure
ExportControl
Investment
Metric
Source
Claim
Event
Relationship
```

### 6.2 Relationship vocabulary

Examples:

```text
owns
operates
manufactures
supplies
uses
depends_on
located_in
produces
requires
enables
licenses
invests_in
acquired
restricted_by
regulated_by
supported_by
competes_with
partners_with
```

Relationships are first-class records because supply-chain intelligence depends on edges, not just entity pages.

### 6.3 First analytical question

The first meaningful analytical product should be:

**Where and how is European AI compute dependent on non-EU capabilities?**

Do not attempt a universal global supply chain on v1.

### 6.4 Minimum viable atlas

Start with a bounded vertical chain:

```text
AI compute
-> accelerators
-> GPU/AI chip architecture
-> manufacturing
-> advanced packaging
-> HBM
-> manufacturing equipment
-> cloud/data-centre layer
```

Then add energy and networking after the base graph is reliable.

---

## 7. Global-AI-Governance domain model

### 7.1 Core entities

```text
Jurisdiction
Institution
GovernanceInstrument
PolicyObjective
RegulatoryMechanism
TechnologyScope
RiskConcept
Right
Standard
Guideline
Treaty
EnforcementMechanism
Source
Claim
Event
Relationship
```

### 7.2 Governance mechanisms

Controlled vocabulary should include, where applicable:

- legislation
- regulation/rule
- executive action
- agency guidance
- technical standard
- certification
- procurement
- export control
- licensing
- competition law
- privacy/data protection
- cybersecurity requirement
- voluntary framework
- international treaty
- administrative guidance

### 7.3 Comparative model

Comparisons must explain differences without producing rankings.

For each jurisdiction, answer:

1. Who acts?
2. Through which legal/institutional mechanism?
3. What is covered?
4. What obligations or incentives result?
5. What enforcement mechanism exists?
6. What role do standards play?
7. How does national security or industrial policy interact with AI governance?
8. Which parts are federal/national versus subnational?
9. What is the evidence date?

---

## 8. AI-Tech-Sovereignty integration model

The integration layer must join domain records through explicit identifiers and validated relationships.

```text
Regulation
   |
   +--> Technology
   |
   +--> Company
   |
   +--> Infrastructure
   |
   +--> Jurisdiction

Technology
   |
   +--> Component
   +--> Compute
   +--> Supply Chain

Company
   |
   +--> Facility
   +--> Product
   +--> Country

Dependency
   |
   +--> company
   +--> technology
   +--> country
   +--> policy exposure
```

Primary output types:

- dependency maps
- regulatory exposure maps
- change alerts
- technology/country profiles
- client briefs
- evidence-backed research briefs
- cross-domain timelines

---

## 9. User journeys

### 9.1 Researcher

`Question -> search -> evidence -> compare -> trace -> export`

### 9.2 Regulatory analyst

`Organisation profile -> applicable instruments -> obligations -> dates -> authorities -> changes -> evidence`

### 9.3 Corporate/client user

`Business profile -> technology profile -> regulatory exposure -> infrastructure dependency -> monitoring list -> briefing`

### 9.4 Consultant

`Client question -> scope -> reusable evidence -> analysis -> executive brief -> appendix`

### 9.5 Public learner

`Concept -> map -> explanation -> evidence -> related policy -> deeper reading`

---

## 10. Evidence model

The existing EU-Digital-Policy evidence discipline should be treated as a portfolio-wide design principle:

### Claim types

At minimum:

- law / normative text
- fact
- derived
- attributed
- interpretation
- critique
- forecast

### Evidence status

At minimum:

- direct
- partial
- derived
- context-only
- unverified
- disputed

The system must make these distinctions visible.

### Evidence hierarchy

Use a project-specific source policy, but generally prefer:

1. primary legal/institutional sources
2. official government/company filings and documentation
3. recognised intergovernmental/standards bodies
4. peer-reviewed or academically reputable research
5. high-quality secondary analysis
6. news/media
7. tertiary summaries

The source hierarchy is guidance, not a substitute for checking whether the source actually supports the claim.

---

## 11. Agent architecture

Agents must be specialised and contract-bound.

```text
                ORCHESTRATOR
                     |
      +--------------+--------------+
      |              |              |
    SCOUT         VERIFIER       CHANGE-DETECTOR
      |              |              |
      +--------------+--------------+
                     |
               KNOWLEDGE ARCHITECT
                     |
              DATA / GRAPH AUDITOR
                     |
                ANALYST
                     |
        +------------+------------+
        |                         |
    EDITORIAL                  CLIENT-OUTPUT
        |                         |
        +------------+------------+
                     |
                    QA
```

### 11.1 Orchestrator

May:

- decompose tasks
- assign tasks
- track states
- request human approval
- merge validated outputs

May not silently alter source records or facts.

### 11.2 Source Scout

May discover candidate sources.

May not:

- assert a fact from a search snippet alone
- upgrade source quality by assumption
- mark a claim verified

### 11.3 Extractor

May transform retrieved material into structured candidate records.

Every candidate must retain source provenance.

### 11.4 Verifier

Determines whether evidence supports a claim.

May downgrade/remove a claim.

May not invent replacement evidence.

### 11.5 Change Detector

Compares versions/events and emits candidate changes.

A detected change is not automatically a substantive policy conclusion.

### 11.6 Knowledge Architect

Maintains entity IDs, relationship vocabulary, canonical ownership and one-home-per-fact constraints.

### 11.7 Data Auditor

Checks:

- schema validity
- broken references
- duplicates
- impossible relationships
- missing provenance
- orphan entities
- inconsistent dates
- null/unknown misuse

### 11.8 Analyst

Produces derived metrics or analytical narratives from validated data.

Every non-trivial calculation must be reproducible.

### 11.9 Editorial

Turns validated material into readable pages.

Editorial prose must preserve claim/evidence boundaries.

### 11.10 Client Output

Produces briefs, exports and dashboards.

It may summarise.
It must not silently alter factual records.

### 11.11 QA

Must test data, rendering, links, accessibility, browser behaviour and regression conditions.

### 11.12 Portfolio Reviewer

Evaluates whether a feature demonstrates a professional capability rather than merely adding visual polish.

Dimensions:

- domain knowledge
- research method
- evidence handling
- data modelling
- Python/SQL use
- software engineering
- automation
- analytical reasoning
- communication
- reproducibility
- client usability

---

## 12. Agent contract format

Every agent must have a contract containing:

```text
ROLE
INPUTS
OUTPUTS
ALLOWED_WRITES
FORBIDDEN_WRITES
EVIDENCE_REQUIREMENTS
HANDOFF_FORMAT
VALIDATION_GATE
FAILURE_BEHAVIOUR
```

Example:

```yaml
agent: verifier
inputs:
  - candidate_claims
  - retrieved_sources
outputs:
  - verified_claims
  - rejected_claims
  - evidence_gaps
allowed_writes:
  - staging/verification/
forbidden_writes:
  - canonical data without passing gate
validation_gate: verification-schema
failure_behaviour: preserve-gap-and-report
```

---

## 13. Autonomy model

Use four levels.

### A — Mechanical

Safe automatic actions:

- formatting
- deterministic validation
- tests
- duplicate detection
- index regeneration

### B — Constrained transformation

Allowed with automated checks:

- schema migrations
- deterministic derivations
- page generation
- source metadata normalization

### C — Evidence-sensitive

Human approval required before canonicalisation:

- legal claim changes
- substantive relationship additions
- new regulatory status
- source-tier decisions affecting published analysis
- interpretation that may materially alter client-facing meaning

### D — Human-only

No autonomous execution:

- legal advice
- external commitments
- publication of unresolved factual disputes
- irreversible deletion of canonical evidence
- actions with material external side effects

When in doubt, use the stricter class.

---

## 14. Quality gates

No domain product may publish canonical output unless all applicable gates pass.

### Gate 0 — Repository integrity

- clean/understood git state
- correct branch
- no unexpected generated changes

### Gate 1 — Schema

- all records valid
- controlled vocabularies pass
- IDs unique
- foreign keys resolvable

### Gate 2 — Provenance

- substantive claims have evidence
- locators are usable
- source metadata complete

### Gate 3 — Semantic integrity

- no impossible relationships
- no contradictory states left unexplained
- no accidental duplicate home for a fact

### Gate 4 — Derivation

- calculations reproducible
- formulas/versioned logic inspectable
- unknown values not treated as zero

### Gate 5 — Content

- fact/interpretation boundaries preserved
- date sensitivity checked
- outdated claims surfaced

### Gate 6 — UI

- navigation works
- no broken routes
- responsive behaviour checked
- accessibility basics pass

### Gate 7 — Browser regression

- critical paths tested
- search/filter/deep links tested
- console/network errors investigated

### Gate 8 — Portfolio quality

The change must produce identifiable evidence of a capability. Avoid feature inflation.

---

## 15. Validation command philosophy

Every repository must have a clearly documented equivalent of:

```bash
validate-data
validate-i18n
validate-design
validate-freshness
qa-browser
```

The exact implementation may differ. The principle must not.

No agent may declare a session complete using only visual inspection.

---

## 16. Data pipeline

The canonical pipeline is:

```text
SOURCE DISCOVERY
      |
      v
RETRIEVAL
      |
      v
RAW EVIDENCE
      |
      v
EXTRACTION
      |
      v
STAGING RECORDS
      |
      v
VERIFICATION
      |
      v
CANONICAL DATA
      |
      v
DERIVATIONS
      |
      v
INDEX / GRAPH
      |
      v
PRESENTATION
      |
      v
QA
      |
      v
PUBLISH
```

Never allow a language model to directly rewrite a canonical published dataset from unreviewed web text.

---

## 17. AI-Infrastructure-Atlas data stack

Recommended initial stack:

```text
Raw sources              Markdown / JSON / archived metadata
Canonical records        JSON
Analytical warehouse     DuckDB
Analysis                 Python
Transformations          Python scripts
Public API/export        JSON / CSV
Visualisation            HTML/CSS/JS initially
BI                        Power BI as an analytical consumer
```

Do not add a database server merely to look professional.

DuckDB is sufficient for a portfolio-scale analytical warehouse until scale actually requires something else.

---

## 18. Graph strategy

Use explicit relationship tables before introducing a graph database.

Minimum viable model:

```text
entities
relationships
claims
sources
events
metrics
```

A graph database may be introduced later only when graph queries become a genuine product requirement.

The system should be able to answer:

- What depends on this component?
- Who supplies this component?
- Which jurisdictions control relevant suppliers?
- Which regulations affect these firms?
- Which policies target this dependency?
- What evidence supports the edge?

---

## 19. Public UX architecture

The public site should be question-oriented rather than taxonomy-oriented.

Primary entry points:

```text
What are you trying to understand?

[Regulatory exposure]
[Technology dependency]
[Supply chain]
[Policy change]
[Country / jurisdiction]
[Company]
[Research question]
```

Every insight page should provide:

1. short answer
2. why it matters
3. evidence
4. underlying entities/relationships
5. methodology/limitations
6. date last verified
7. deeper links

---

## 20. Client mode

Every project should eventually support a client-facing output mode.

Example output:

```text
CLIENT TECHNOLOGY POLICY BRIEF

Question
Scope
Executive summary
Relevant regulation
Infrastructure dependencies
Key entities
Recent changes
Evidence gaps
Monitoring recommendations
Methodology
Evidence appendix
```

The system is not a legal-advice engine. It is a research and decision-support product.

---

## 21. Portfolio storytelling

The projects should collectively demonstrate this progression:

```text
EU legal research
      ->
Evidence engineering
      ->
Regulatory intelligence
      ->
Industrial/technology intelligence
      ->
Comparative governance
      ->
Quantitative analysis
      ->
Cross-domain decision support
```

The portfolio should make it obvious that the developer understands both the subject matter and the mechanics of building trustworthy analytical systems.

---

## 22. Milestones

### M0 — Architecture baseline

Deliver:

- this document
- agent contracts
- shared taxonomy principles
- data contract
- quality gates
- repository conventions

### M1 — AI Infrastructure Atlas skeleton

Deliver:

- entity schema
- relationship schema
- source/claim schema
- 10–20 entities across the initial vertical chain
- working provenance UI
- first dependency graph

### M2 — First analytical product

Deliver:

**EU AI compute dependency map**

with reproducible Python/SQL calculations.

### M3 — Industrial depth

Add:

- semiconductors
- HBM
- advanced packaging
- manufacturing equipment
- data centres/cloud

### M4 — Global governance

Build the comparative governance model and initial EU/US/China/international coverage.

### M5 — Integration

Build cross-domain links:

`policy <-> company <-> technology <-> infrastructure <-> jurisdiction`

### M6 — Client mode

Add:

- profile intake
- exposure map
- monitoring dashboard
- briefing export

### M7 — Portfolio hardening

Run full audit:

- technical
- data
- evidence
- UX
- accessibility
- reproducibility
- documentation
- CV/portfolio narrative

---

## 23. Definition of done

A feature is done only when:

- the domain question it solves is explicit;
- the data model is documented;
- sources and provenance are retained;
- unknowns are explicit;
- derived analysis is reproducible;
- tests pass;
- browser QA passes for affected flows;
- limitations are documented;
- the feature demonstrates a real research/client capability;
- no duplicated source of truth was introduced.

"The page looks good" is never sufficient.

---

## 24. What must not happen

Never:

- turn the project into an AI chatbot that answers from model memory;
- fabricate sources or citations;
- use search-result snippets as final evidence;
- convert uncertainty into confident prose;
- store derived values as if they were primary facts;
- create a giant universal taxonomy before validating the initial use case;
- add infrastructure solely for CV theatre;
- overbuild a framework before the data model is working;
- optimise for visual novelty at the expense of evidence quality;
- let autonomous agents directly publish sensitive canonical facts.

---

## 25. Current first implementation target

The first new repository should be `AI-Infrastructure-Atlas`.

Its first vertical should be deliberately narrow:

`AI compute -> accelerators -> manufacturing -> packaging -> HBM -> equipment -> cloud/data centres`

Its first user-facing question should be:

> **Where are the critical dependencies behind AI compute, and what evidence supports that assessment?**

Do not build the whole atlas before this workflow works end-to-end.
