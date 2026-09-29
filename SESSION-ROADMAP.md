# AI-Infrastructure-Atlas — Session Roadmap

## Operating model

This roadmap is deliberately more structured than the historical evolution of `EU-Digital-Policy`.

The objective is not to maximize the number of sessions. It is to create a traceable sequence in which research, architecture, implementation and audit reinforce one another.

The project starts with a narrow vertical slice and expands only after the evidence model, data model and quality controls demonstrate that the system can support the additional complexity.

---

## Milestone map

```text
M0 Constitution
  S00–S02
       ↓
M1 Domain + Evidence Foundation
  S03–S06
       ↓
M2 Canonical Dataset
  S07–S10
       ↓
M3 Vertical Slice + Audit
  S11–S13
       ↓
M4 Analytical Intelligence
  S14–S16
       ↓
M5 Policy / Geopolitical Layer
  S17–S19
       ↓
M6 Client Product
  S20–S21
       ↓
M7 Final Audits + Release
  S22–S25
```

---

# M0 — Project Constitution

## S00 — Repository bootstrap
**Type:** ARCHITECTURE

### Mission
Create the independent repository and establish the project's constitutional layer without importing unnecessary implementation from `EU-Digital-Policy`.

### Focus
- repository structure;
- `CLAUDE.md`;
- `MASTER-ARCHITECTURE.md`;
- session system;
- evaluation framework linkage;
- CI skeleton;
- baseline documentation.

### Non-goals
- production data ingestion;
- frontend polish;
- graph database;
- external API dependency.

### Gate
Repository is runnable, documented and auditable before substantive data work begins.

---

## S01 — Domain map: the physical AI stack
**Type:** RESEARCH

### Mission
Build the first defensible conceptual map of the physical and industrial dependencies behind AI compute.

### Focus
- accelerator layer;
- HBM/memory;
- advanced packaging;
- foundries;
- semiconductor equipment;
- data centres/cloud;
- energy interface.

### Required output
A domain map with explicit uncertainty markers and a source register.

### Audit question
Which concepts are genuinely necessary for the initial product, and which belong to future scope?

---

## S02 — Architecture baseline + process benchmark
**Type:** AUDIT / SYNTHESIS

### Mission
Test the proposed architecture against the lessons learned from `EU-Digital-Policy` without copying its implementation.

### Focus
- identify reusable methodological lessons;
- identify anti-patterns from long iterative development;
- establish initial architecture decisions;
- freeze non-goals.

### Gate
Baseline Architecture Record approved.

---

# M1 — Domain + Evidence Foundation

## S03 — Entity taxonomy
**Type:** ARCHITECTURE

### Mission
Define the minimum canonical entity vocabulary needed to represent the initial AI compute supply chain.

### Focus
Company, Country/Jurisdiction, Facility, Technology, Component, Product, Policy, Institution, Source, Claim, Event, Relationship.

### Critical test
No entity should exist merely because it is convenient for the UI.

---

## S04 — Relationship taxonomy
**Type:** ARCHITECTURE

### Mission
Define precise semantic relationships and prevent accidental inference from co-occurrence.

### Focus
`owns`, `operates`, `manufactures`, `designs`, `supplies`, `depends_on`, `requires`, `produces`, `located_in`, `packages`, `fabricates`, `uses`, `constrained_by`, `affected_by`.

### Gate
Every relationship has a clear semantic definition and evidence expectation.

---

## S05 — Source hierarchy and evidence policy
**Type:** RESEARCH / ARCHITECTURE

### Mission
Create a source hierarchy tailored to industrial technology research.

### Focus
- government/institutional sources;
- company primary sources;
- financial/regulatory filings;
- standards bodies;
- reputable research;
- secondary media;
- source conflict handling.

### Gate
Every material claim type has a preferred source class.

---

## S06 — Evidence/claim system
**Type:** IMPLEMENTATION

### Mission
Implement claim-level provenance, verification state and temporal metadata before dataset scale-up.

### Required claim types
`FACT | ATTRIBUTION | DERIVATION | INTERPRETATION | IMPLICATION`

### Gate
The system can answer: "What exactly supports this relationship?"

---

# M2 — Canonical Dataset

## S07 — Company dataset
**Type:** RESEARCH / IMPLEMENTATION

### Mission
Build the first curated company dataset across the initial stack.

### Target
A small, high-quality seed set rather than maximum coverage.

### Coverage
Accelerators, memory, packaging, foundries, equipment, selected cloud/data-centre actors.

### Gate
Every canonical company record has identity evidence and stable IDs.

---

## S08 — Technology + component dataset
**Type:** IMPLEMENTATION

### Mission
Model the technologies/components themselves independently of company marketing language.

### Focus
Accelerator types, HBM, packaging, foundry processes, critical equipment categories, relevant data-centre infrastructure layers.

### Gate
Definitions are sourced and do not collapse technically distinct concepts.

---

## S09 — Facility dataset
**Type:** RESEARCH / IMPLEMENTATION

### Mission
Represent strategically relevant production/data-centre facilities with location, operator/owner distinctions and evidence.

### Critical distinction
Do not conflate headquarters, company ownership, operating control and physical manufacturing location.

---

## S10 — First supply-chain edges
**Type:** IMPLEMENTATION

### Mission
Connect canonical entities through a small auditable set of supply-chain relationships.

### Rule
No relationship is published without evidence or an explicit non-published/unverified state.

### Gate
Graph-like navigation is possible using relational data without introducing a graph database.

---

# M3 — Vertical Slice + Audit

## S11 — First end-to-end vertical slice
**Type:** IMPLEMENTATION

### Mission
Build one complete user journey from source → entity → relationship → visualization → evidence.

### Target journey
Trace one AI compute dependency chain upstream.

### Gate
The journey is usable by a person who did not build the dataset.

---

## S12 — Data architecture audit
**Type:** AUDIT

### Mission
Independently challenge the canonical data model and the first vertical slice.

### Examine
- normalization/denormalization choices;
- duplicate concepts;
- stable IDs;
- relationship semantics;
- temporal correctness;
- provenance completeness;
- queryability;
- migration risk.

### Required output
Architecture Audit Report + remediation decisions.

---

## S13 — Content/evidence depth audit
**Type:** AUDIT

### Mission
Sample claims and relationships and test whether the content layer is stronger than the presentation layer.

### Examine
- source quality;
- locator precision;
- evidence overreach;
- stale claims;
- conflicting sources;
- interpretation/fact boundary.

### Gate
No scaling until evidence weaknesses are corrected or explicitly documented.

---

# M4 — Analytical Intelligence

## S14 — DuckDB / SQL analytical layer
**Type:** ARCHITECTURE / IMPLEMENTATION

### Mission
Introduce a reproducible analytical warehouse without making the warehouse the canonical source of truth.

### Focus
- relational views;
- reproducible SQL;
- source-to-metric lineage;
- rebuild procedure.

### Gate
All published metrics can be regenerated from versioned inputs.

---

## S15 — Dependency metrics
**Type:** ANALYSIS

### Mission
Implement transparent descriptive metrics for supplier and geographic concentration.

### Initial metrics
- supplier counts;
- geographic concentration;
- single-source relationships where demonstrable;
- evidence coverage;
- source age.

### Explicit non-goal
Do not create an opaque composite "dependency score".

---

## S16 — Analytical audit
**Type:** AUDIT

### Mission
Challenge whether the metrics answer real questions and whether their denominators, populations and assumptions are defensible.

### Required questions
- What is being measured?
- What is not being measured?
- Which missing data could distort the result?
- Could a user misread the metric?

---

# M5 — Policy / Geopolitical Layer

## S17 — Policy entities
**Type:** RESEARCH / ARCHITECTURE

### Mission
Introduce a policy layer connecting infrastructure dependencies to public policy without duplicating `EU-Digital-Policy`.

### Focus
- industrial policy;
- export controls;
- strategic dependencies;
- investment policy;
- technology restrictions;
- public support.

### Boundary
The project may reference EU regulatory instruments but must not become another EU digital-law database.

---

## S18 — Jurisdiction and policy relationships
**Type:** IMPLEMENTATION

### Mission
Model evidence-backed relationships between jurisdictions, companies, technologies and policy instruments.

### Example
Policy instrument → restricts / supports → technology or supply-chain layer.

### Gate
Attribution and legal/policy status are explicit; analysis does not silently become legal advice.

---

## S19 — Agent architecture audit
**Type:** AUDIT

### Mission
Evaluate whether the multi-agent system still improves reliability rather than simply increasing complexity.

### Examine
- role overlap;
- permission boundaries;
- staging vs canonical writes;
- verifier authority;
- auditability;
- failure recovery;
- orchestration overhead.

### Gate
Any unnecessary agent or duplicate responsibility must be removed or justified.

---

# M6 — Client Product

## S20 — Researcher / analyst UX
**Type:** IMPLEMENTATION

### Mission
Turn the knowledge system into a product that answers concrete investigation questions efficiently.

### Core journeys
- explore a dependency;
- investigate a company;
- investigate a country;
- inspect evidence;
- compare layers.

### Gate
Each major UI feature maps to a documented user question.

---

## S21 — Client brief generator
**Type:** IMPLEMENTATION

### Mission
Generate a reproducible, evidence-backed technology dependency brief from a defined question and scope.

### Output
- executive summary;
- dependency map;
- evidence;
- methodology;
- caveats;
- source appendix.

### Boundary
No autonomous legal, investment or procurement recommendation.

---

# M7 — Final Audits + Release

## S22 — Code / engineering audit
**Type:** AUDIT

### Mission
Audit the complete repository as an engineered software system.

### Examine
- modularity;
- test coverage;
- regression resistance;
- build reproducibility;
- dependency hygiene;
- accessibility;
- performance;
- security basics;
- complexity.

---

## S23 — Research depth + content audit
**Type:** AUDIT

### Mission
Assess whether the project demonstrates real domain depth rather than surface-level web research.

### Examine
- conceptual coverage;
- primary-source ratio;
- claim verification;
- counterevidence;
- temporal coverage;
- analytical sophistication;
- limitations.

---

## S24 — Portfolio / capability audit
**Type:** AUDIT

### Mission
Determine whether the project communicates professional capability through both its result and its development history.

### Examine
- domain expertise signal;
- data engineering signal;
- SQL/Python signal;
- AI governance/agent signal;
- policy analysis signal;
- reproducibility;
- client value;
- documentation quality.

### Important
Do not optimize for a superficial aesthetic score. Identify missing evidence of capability.

---

## S25 — v1.0 synthesis and release
**Type:** SYNTHESIS / RELEASE

### Mission
Freeze a coherent v1.0, document what was learned, and establish the evidence base for the next project or major version.

### Required output
- release notes;
- final architecture record;
- final process audit;
- final outcome audit;
- known limitations;
- future research backlog;
- portfolio case study;
- demonstration dataset and user journey.

### Exit condition
The project is considered complete only when another person can understand:

1. what the system does;
2. how the data is structured;
3. how claims are verified;
4. how metrics are produced;
5. how agents are governed;
6. how to reproduce the build;
7. why the product is useful.

---

# Session dependency rules

A session may begin only when its predecessor's acceptance criteria are met, unless the session itself is an audit explicitly designed to investigate a failed predecessor.

Foundational decisions must never be silently changed by downstream implementation sessions.

If S12, S13, S16, S19, S22 or S23 reveals a structural defect, S25 cannot simply proceed. The roadmap must branch into a remediation session or an explicit documented decision to accept the limitation.

---

# Recommended Opus 5.5 working pattern

For each session:

```text
Read constitution + prior report
        ↓
Inspect actual repository state
        ↓
Identify mismatch between plan and reality
        ↓
Research / reason
        ↓
Propose implementation
        ↓
Obtain governed approval where required
        ↓
Implement
        ↓
Run verification
        ↓
Run self-audit
        ↓
Write session report
        ↓
Prepare next-session handoff
```

The model is expected to spend meaningful effort on **understanding and validation**, not simply code generation.
