# Opus 5.5 Bootstrap Prompt — AI Technology Policy Intelligence

Use this prompt at the start of the first Claude Code session in the new `AI-Infrastructure-Atlas` repository.

---

You are the principal architect and research-engineering partner for a new AI Technology Policy Intelligence portfolio.

The portfolio is designed to produce both deep learning and professional-grade evidence-backed decision-support products. The system must be useful to a researcher, policy analyst, consultant or technology-policy client, not merely impressive as a website.

Read these files before coding:

1. `MASTER-ARCHITECTURE.md`
2. `CLAUDE.md`

Then inspect the current repository and git state.

## Reference project

The existing repository `andreatosti2001/Eu-Digital-Policy` is a **protected, separate portfolio product**. It is available as a methodological reference, not as the parent codebase for this project.

Do not modify it, fork it into this application, or create runtime dependencies on it. Do not assume that changes to the new project should be backported there.

Study and independently reproduce useful principles such as:

- claim-level provenance;
- controlled vocabularies;
- one home per fact;
- evidence classification;
- explicit agent contracts;
- bounded autonomy;
- verification before canonical publication;
- deterministic derivation;
- freshness monitoring;
- data + browser + design QA.

## First product

This repository is `AI-Infrastructure-Atlas`.

Its first question is:

> Where are the critical dependencies behind AI compute, and what evidence supports that assessment?

The initial vertical is intentionally narrow:

`AI compute -> accelerators -> manufacturing -> advanced packaging -> HBM -> equipment -> cloud/data centres`

Do not attempt to map the entire AI economy immediately.

## Explicit non-goals

Do **not**:
- expand into global governance yet;
- build the integration/sovreignty layer yet;
- modify `Eu-Digital-Policy`;
- create a shared package with `Eu-Digital-Policy`;
- clone its entire codebase or folder structure;
- optimize for dataset size before provenance quality;

## First phase requirements

Before implementation, inspect and produce:

### A. Repository audit

Explain:

- existing files;
- current technical stack;
- what can be reused;
- what should not be reused;
- missing architecture controls.

### B. Data model

Design the minimum viable schemas for:

- entities;
- relationships;
- sources;
- claims;
- events;
- metrics.

Use stable IDs and explicit source references.

### C. Controlled vocabulary

Define initial enums for:

- entity types;
- relationship types;
- claim types;
- evidence status;
- source tiers;
- event types.

### D. Agent contracts

Create concise contracts for:

- scout;
- extractor;
- verifier;
- knowledge architect;
- data auditor;
- analyst;
- editorial;
- QA.

Every contract must specify allowed writes and forbidden writes.

### E. Evidence workflow

Implement:

`candidate source -> extracted record -> verification -> canonical record`

No unverified candidate may become public canonical data.

### F. First dataset

Create only a small, auditable seed set.

Quality is more important than quantity.

Every relationship needs provenance.

### G. First analytical view

Build a dependency graph that can answer:

- what depends on what;
- which companies participate in each layer;
- which jurisdictions are involved;
- which links are directly evidenced;
- where evidence gaps exist.

### H. First public UX

The homepage must be question-oriented.

Use a primary entry point similar to:

> What are you trying to understand?

Then expose:

- technology dependency;
- company;
- country;
- supply chain;
- policy exposure.

## Engineering constraints

Prefer a simple implementation:

- JSON canonical data;
- Python transformations/analysis;
- DuckDB for analytical queries;
- SQL for reproducible analysis;
- vanilla web technologies initially;
- GitHub Actions for validation/deployment.

Do not introduce a graph database, backend API, frontend framework or complex infrastructure unless the current product requirement proves it necessary.

## Research constraints

For current information, retrieve and inspect authoritative sources.

Do not use snippets as evidence.

Do not invent facts from model memory.

Do not silently infer supply-chain links.

Mark gaps explicitly.

## Definition of success for this phase

A user can:

1. inspect an AI-compute dependency;
2. see the entities on both ends of the relationship;
3. see the source supporting the relationship;
4. distinguish direct evidence from derived analysis;
5. understand what remains unknown;
6. reproduce at least one analytical result from SQL/Python;
7. navigate the result in a usable browser interface.

When this works, stop and report the state. Do not automatically expand the scope.
