# Project Evaluation Framework — Process + Outcome Audit

## Purpose

Every new project in the Technology Policy portfolio must be evaluated on **both the process that produced it and the resulting system**.

`EU-Digital-Policy` is the reference case: its long, heterogeneous history is valuable evidence of what iterative AI-assisted development can produce, but its evolution must not be copied mechanically.

The goal is to make subsequent projects more deliberate, auditable and reproducible while preserving room for experimentation.

---

## 1. Two-axis evaluation model

### Axis A — Process quality

Evaluate **how the project was built**:

1. architecture discipline;
2. research and content workflow;
3. agent orchestration and governance;
4. decision traceability;
5. testing and regression control;
6. management of rework, drift and technical debt;
7. learning progression of the owner.

### Axis B — Outcome quality

Evaluate **what the project currently is**:

1. data architecture;
2. content quality and evidence depth;
3. agent architecture;
4. analytical depth;
5. code and engineering quality;
6. user value and product coherence;
7. reproducibility and maintainability.

Do not collapse these into one overall score. A project can have excellent outcomes despite a messy process, or a disciplined process that has not yet produced sufficient depth. Both facts should remain visible.

---

## 2. Evaluation dimensions

| Dimension | Process questions | Outcome questions |
|---|---|---|
| Data architecture | Were schema decisions explicit? Were migrations controlled? | Is the model coherent, normalized where appropriate, temporal, provenance-aware and queryable? |
| Content & review | How were claims researched, challenged and revised? | Are claims accurate, current, well sourced, deep and clearly separated from interpretation? |
| Agent architecture | Were agent roles, permissions and handoffs explicit? | Are agents modular, bounded, auditable and resistant to silent fact/inference upgrades? |
| Analytical depth | Did analysis evolve from questions rather than decoration? | Are metrics reproducible, meaningful, transparent and appropriately limited? |
| Code / engineering | Was implementation incremental, tested and reviewed? | Is the code maintainable, modular, tested, accessible, performant and secure enough for scope? |
| Product / user value | Were features driven by user questions? | Does the system materially reduce research effort or improve understanding/decision preparation? |
| Reproducibility | Could another person reconstruct the state and rationale? | Can data, analysis, builds and outputs be reproduced from documented inputs? |

---

## 3. Maturity scale

Use a 0–4 maturity level **per dimension**, not a single portfolio score.

- **0 — Absent:** no explicit method or unreliable implementation.
- **1 — Ad hoc:** working pieces exist but depend on manual memory or implicit conventions.
- **2 — Defined:** documented process/model with partial enforcement.
- **3 — Controlled:** automated or repeatable controls, explicit evidence and regression handling.
- **4 — Exemplary:** mature, reproducible, measurable, well documented and demonstrably resilient to change.

Every rating must cite evidence from the repository, commit history, tests, datasets, documentation or product behavior.

---

## 4. Process audit protocol

### At project start

Create a **Baseline Architecture Record** containing:

- intended architecture;
- known uncertainties;
- initial scope boundaries;
- intended agent roles;
- initial data model;
- quality gates;
- explicit non-goals.

### At every major milestone

Perform a **Milestone Audit**:

1. what was intended;
2. what was implemented;
3. what changed and why;
4. which assumptions failed;
5. which shortcuts were taken;
6. what technical/research debt was created;
7. what was removed or rejected;
8. what should be carried into the next phase.

### Every 8–12 substantive sessions or equivalent

Perform a **Process Retrospective** using Git history, decision logs and current architecture.

Look for:

- repeated rework;
- duplicated abstractions;
- architecture drift;
- agent overlap;
- undocumented schema changes;
- content churn caused by weak source selection;
- tests added only after regressions;
- features that never acquired a real user journey;
- code generated faster than it was understood or reviewed.

### Before v1.0

Perform a **Pre-release Dual Audit** covering both process and outcome.

---

## 5. Data architecture audit

Check both design and evolution.

### Process

- Was the canonical data model defined before uncontrolled scale?
- Are schema changes documented?
- Are breaking changes intentional?
- Are IDs stable?
- Are migrations/rebuilds reproducible?
- Are derived fields separated from source facts?

### Outcome

- One canonical home per fact.
- Explicit entity types and relationships.
- Temporal validity where necessary.
- Provenance at claim/relationship level.
- Clear distinction between unknown, unavailable and zero.
- Derived metrics reproducible from source records.
- No silent duplication or conflicting canonical records.

---

## 6. Content and review audit

The project must audit **content as a system**, not merely run spelling checks.

### Process

Track:

- source discovery;
- source qualification;
- claim extraction;
- verification;
- contradiction handling;
- stale-source replacement;
- editorial revision;
- interpretation review.

### Outcome

Sample claims across the project and classify them as:

`FACT | ATTRIBUTION | DERIVATION | INTERPRETATION | IMPLICATION`

For sampled claims inspect:

- primary/authoritative support;
- locator quality;
- publication date;
- verification date;
- whether the wording exceeds the evidence;
- whether material opposing evidence exists;
- whether confidence is justified.

Track **evidence coverage** and **freshness exposure** for important content.

---

## 7. Agent architecture audit

Evaluate agents as a socio-technical system.

### Process

Review:

- role creation;
- changes to permissions;
- handoff contracts;
- approval rules;
- escalation paths;
- failure recovery;
- repeated agent proposals that did not result in approved changes.

### Outcome

Each agent should have:

- a narrow mission;
- explicit inputs/outputs;
- canonical write boundaries;
- observable decisions;
- deterministic checks where practical;
- no authority to silently promote inference to fact.

Audit for duplicated responsibilities, circular dependencies and orchestration logic that has become harder to understand than the work itself.

---

## 8. Analytical depth audit

The purpose is to prevent "dashboard theatre".

For every material metric or model ask:

1. What question does it answer?
2. What population does it cover?
3. What is the denominator?
4. What assumptions are made?
5. What data is missing?
6. Can another person reproduce it?
7. How sensitive is the conclusion to plausible changes in assumptions?
8. What does the metric **not** prove?

A complex visualization without a defensible analytical question is not considered analytical depth.

---

## 9. Code / engineering audit

### Process indicators

- commit coherence;
- meaningful change boundaries;
- regression testing before/after risky changes;
- documented refactors;
- dependency hygiene;
- rollback/recovery discipline;
- architecture decisions recorded when they materially affect the system.

### Outcome indicators

- modularity;
- low accidental duplication;
- clear separation of data/logic/presentation;
- appropriate typing and validation;
- automated tests for critical paths;
- accessible UI;
- acceptable performance;
- basic security hygiene;
- reproducible build/deploy.

Do not reward code volume. Reward **appropriate complexity**.

---

## 10. Portfolio / learning audit

Every milestone should answer:

> **What capability did this project make demonstrably stronger?**

Examples:

- regulatory research;
- industrial research;
- data modelling;
- SQL;
- Python;
- evidence verification;
- policy analysis;
- comparative governance;
- supply-chain analysis;
- AI-assisted engineering.

The audit must link the claimed capability to visible evidence in the repository or product.

---

## 11. Required audit artifacts

Every new project should maintain:

```text
/docs/
  architecture/
    baseline.md
    decisions.md
    milestone-audits/
  research/
    source-policy.md
    content-review-log.md
  agents/
    roles.md
    contracts.md
  quality/
    evaluation-framework.md
    audit-history.md
```

The exact folder structure may vary, but the information must remain recoverable.

---

## 12. Portfolio Reviewer responsibilities

The `Portfolio Reviewer` is not a visual critic. It is responsible for asking whether the project demonstrates professional capability.

At each major milestone it produces:

- Process findings;
- Outcome findings;
- Evidence for each finding;
- Maturity level per dimension;
- Regressions since the previous audit;
- High-value improvements;
- Explicitly rejected improvements;
- New learning outcomes.

It must not optimize for superficial complexity or feature count.

---

## 13. Learning loop

Use the following loop:

```text
Build
  ↓
Observe
  ↓
Audit process
  ↓
Audit outcome
  ↓
Identify failure / learning
  ↓
Revise architecture or method
  ↓
Build again
```

The audit is part of the product development cycle, not a final retrospective exercise.

---

## 14. Relationship to EU-Digital-Policy

`EU-Digital-Policy` should be treated as a **historical reference dataset for process learning**.

Its ~200-commit evolution can be studied retrospectively for:

- successful patterns;
- avoidable rework;
- architectural drift;
- effective QA;
- agent governance lessons;
- evidence/content lessons;
- useful implementation patterns.

However, the subsequent projects should not reproduce every historical pattern. The purpose is to extract reusable principles while deliberately correcting weaknesses revealed by the history.
