# AI-Infrastructure-Atlas — Operational Roadmap with Claude Opus 5.5

## Operating principle

This project should be built as a governed sequence of research, architecture, implementation and audit sessions. `EU-Digital-Policy` remains protected and independent. It is a methodological benchmark only; no runtime dependency or major refactor is required.

## Calendar window

Assuming a start on **Monday 28 September 2026**, the default 12-week execution window runs through **Sunday 20 December 2026**. The weekly blocks are:

| Week | Dates | Sessions | Main outcome |
|---|---|---|---|
| 1 | 28 Sep–4 Oct | S00–S02 | Constitution + domain boundary |
| 2 | 5–11 Oct | S03–S05 | Ontology + source policy |
| 3 | 12–18 Oct | S06–S07 | Evidence system + company seed |
| 4 | 19–25 Oct | S08–S10 | Canonical dataset + supply-chain edges |
| 5 | 26 Oct–1 Nov | S11–S13 | Vertical slice + data/content audits |
| 6 | 2–8 Nov | S14–S15 | SQL/analytics foundation |
| 7 | 9–15 Nov | S16–S17 | Analytical audit + policy layer |
| 8 | 16–22 Nov | S18–S19 | Policy relationships + agent audit |
| 9 | 23–29 Nov | S20–S21 | Researcher UX + client brief |
| 10 | 30 Nov–6 Dec | S22 | Engineering audit |
| 11 | 7–13 Dec | S23–S24 | Research-depth + portfolio audit |
| 12 | 14–20 Dec | S25 | v1.0 synthesis + release |

This is a planning window, not a deadline. A blocking audit finding should move the schedule rather than be hidden to preserve the calendar.

## Recommended cadence

- 2 substantive Opus sessions per week as the default.
- A third lighter session only when the previous session produced a clean handoff and no audit debt.
- Reserve time between sessions for the human review of sources, concepts and architectural decisions.
- Do not use Opus simply to fill time: a session ends when its acceptance criteria are met or a stop condition is triggered.

A practical weekly rhythm is:

- Session A: Research / Architecture / Build
- Session B: Build / Audit / Synthesis
- Optional Session C: targeted correction, documentation or evidence review

## Before every session

1. Open the project repository.
2. Read `CLAUDE.md`.
3. Read the relevant section of `MASTER-ARCHITECTURE.md`.
4. Read the previous session report.
5. Read the exact session prompt under `sessions/prompts/`.
6. Start a fresh Opus 5.5 session rather than carrying an uncontrolled long context.
7. Paste the session prompt verbatim.
8. Tell Opus to inspect the actual repository before proposing changes.
9. Do not approve broad refactors unless the prompt explicitly authorizes them.

## During every session

Opus should follow:

`inspect → reason → propose → implement → validate → report`

The user should review:

- architectural decisions;
- newly introduced data semantics;
- evidence quality for material claims;
- changes outside the declared scope;
- audit findings that require human judgment.

## End of every session

Before closing the session, require Opus to:

1. run the defined verification suite;
2. summarize files changed;
3. summarize data/evidence changed;
4. record decisions and rejected alternatives;
5. record deviations from the prompt;
6. record new/resolved debt;
7. create `sessions/reports/SESSION-XX-REPORT.md`;
8. identify any blocking issue for the next session;
9. propose the next-session starting state without silently changing the next prompt.

Commit only after the session passes its acceptance criteria.

---

# Week-by-week plan

## Week 1 — Constitution and research boundary
### S00 — Repository bootstrap
**Type:** Architecture

User action:
- Create the new GitHub repository.
- Add the project documentation pack.
- Start Opus with `S00-PROMPT.md`.

Opus outcome:
- repository skeleton;
- CI/test skeleton;
- documentation structure;
- session system;
- baseline architecture record.

Human review:
- confirm this is genuinely independent from `EU-Digital-Policy`;
- reject unnecessary copied infrastructure.

### S01 — Domain map: physical AI stack
**Type:** Research

Study with Opus:
- AI accelerators;
- HBM;
- advanced packaging;
- foundries;
- EDA/equipment;
- cloud/data centres;
- energy interface.

Human task:
- read the generated domain map and challenge terminology.

**Weekly gate:** You can explain the physical AI compute stack without relying on the website.

### S02 — Architecture baseline + process benchmark
**Type:** Audit/Synthesis

Opus compares the planned architecture with lessons from `EU-Digital-Policy`.

Human decision:
- approve project boundaries;
- explicitly freeze non-goals;
- approve the initial architecture baseline.

**Milestone M0 complete.**

---

## Week 2 — Model the world before building the interface
### S03 — Entity taxonomy
Define canonical entities.

Human focus:
- understand why Company, Facility, Technology, Component, Country, Product, Policy, Source, Claim and Event are distinct.

### S04 — Relationship taxonomy
Define semantic relationships.

Human focus:
- reject ambiguous relationships such as `associated_with` when a more precise relationship exists;
- require evidence expectations per relationship type.

### S05 — Source hierarchy and evidence policy
Build the industrial-technology source hierarchy.

Human focus:
- distinguish primary sources from company marketing and secondary reporting;
- examine how conflicts between sources will be handled.

**Weekly gate:** the ontology and evidence policy are understandable before large-scale data collection begins.

---

## Week 3 — Evidence system
### S06 — Claim/evidence system
Implement claim-level provenance.

Human focus:
- understand FACT vs DERIVATION vs INTERPRETATION vs IMPLICATION;
- test a few claims manually.

### S07 — Company dataset
Start a small, curated company seed set.

Human focus:
- manually inspect a sample of canonical entities and identity evidence.

**Milestone M1 complete.**

---

## Week 4 — Canonical dataset
### S08 — Technology/component dataset
Model concepts independently of company language.

### S09 — Facility dataset
Add physical locations and distinguish ownership, operation and production.

### S10 — Supply-chain edges
Create the first auditable relationships.

Human focus:
- inspect at least 10 relationships end-to-end from source to published edge.

**Milestone M2 complete.**

---

## Week 5 — First product slice and first hard audit
### S11 — First end-to-end vertical slice
Build one complete user journey:

`source → entity → relationship → dependency path → visualization → evidence`

Human task:
- use it as if you were a new user;
- try to break the chain;
- note confusing terminology.

### S12 — Data architecture audit
Do not build new features during this session unless needed for remediation.

Audit:
- normalization;
- stable IDs;
- temporal model;
- relationships;
- provenance;
- queryability;
- migration risk.

### S13 — Content/evidence depth audit
Sample claims and relationships.

Human task:
- inspect conflicts and weak sources;
- decide which claims must be downgraded or removed.

**Milestone M3 complete only after remediation of blocking audit findings.**

---

## Week 6 — Analytical foundation
### S14 — DuckDB / SQL layer
Add the reproducible analytical warehouse.

Human learning target:
- understand canonical vs derived data;
- read and explain the key SQL queries.

### S15 — Dependency metrics
Implement transparent metrics:
- supplier count;
- geographic concentration;
- demonstrable single-source relationships;
- evidence coverage;
- source age.

Human task:
- challenge the denominator and population of every metric.

**Do not allow an opaque composite risk score.**

---

## Week 7 — Analytical audit and correction
### S16 — Analytical audit
No feature expansion.

Audit:
- what each metric measures;
- what it does not measure;
- missing data;
- survivorship/selection issues;
- misleading presentation.

Human decision:
- approve, modify or retire each metric.

### S17 — Policy entities
Only now add the policy layer.

Human focus:
- industrial policy;
- export controls;
- strategic dependencies;
- investment restrictions/support;
- infrastructure policy.

Boundary:
- do not turn the project into a second `EU-Digital-Policy`.

**Milestone M4 complete; M5 begins.**

---

## Week 8 — Policy relationships and agent architecture
### S18 — Jurisdiction/policy relationships
Connect jurisdictions, companies, technologies and policy instruments.

Human focus:
- distinguish documented policy effect from analytical interpretation;
- avoid legal advice language.

### S19 — Agent architecture audit
Audit the agents as an engineered system.

Ask:
- does each agent have a unique responsibility?
- can agents write to canonical data safely?
- is the verifier actually independent enough?
- is orchestration worth its complexity?
- where are failure-recovery paths?

Human decision:
- delete redundant agents rather than preserving them for appearance.

**Milestone M5 complete.**

---

## Week 9 — Productization
### S20 — Researcher/analyst UX
Build question-oriented navigation:
- dependency investigation;
- company investigation;
- country investigation;
- evidence inspection;
- comparisons.

Human task:
- perform each journey without reading the code;
- record friction.

### S21 — Client brief generator
Generate an evidence-backed technology dependency brief.

Human task:
- review it as if it were being delivered to an external client;
- flag unsupported conclusions and confusing caveats.

**Milestone M6 complete.**

---

## Week 10 — Engineering audit
### S22 — Code/engineering audit
No normal feature development.

Opus audits:
- modularity;
- tests;
- regression risk;
- dependencies;
- build reproducibility;
- accessibility;
- performance;
- security basics;
- complexity.

Human task:
- prioritize remediation instead of accepting every suggestion.

---

## Week 11 — Research depth audit
### S23 — Research/content audit
Challenge whether the project demonstrates real domain competence.

Review:
- primary-source ratio;
- conceptual gaps;
- source conflicts;
- temporal coverage;
- methodological depth;
- limitations.

Human task:
- identify 3–5 areas where your own domain knowledge is still shallow.

### S24 — Portfolio/capability audit
Ask whether a recruiter/client can infer:
- domain knowledge;
- research quality;
- data engineering;
- SQL/Python;
- AI-agent governance;
- policy analysis;
- client value.

No beauty score. Only evidence of capability and gaps.

**Milestone M7 begins.**

---

## Week 12 — Release
### S25 — v1.0 synthesis and release
Opus produces:
- release notes;
- final architecture record;
- final process audit;
- final outcome audit;
- known limitations;
- research backlog;
- portfolio case study;
- reproducible demonstration journey.

Human final review:
- run the system from a clean checkout;
- follow the primary user journey;
- verify a sample of evidence;
- read the final case study as a stranger.

**Project status: v1.0.**

---

# How to work with Opus in practice

## First session of each week
Use the exact prepared session prompt. Do not summarize it from memory.

Start with:

> Read `CLAUDE.md`, `MASTER-ARCHITECTURE.md`, the previous session report, and the exact session prompt. Inspect the repository before changing anything. Restate the mission, constraints, non-goals and acceptance criteria. Then propose the smallest safe execution plan. Do not implement until the plan is consistent with the repository state.

## During a build session
Let Opus inspect and implement in small controlled phases. After each phase ask for verification results rather than accepting a large unverified batch.

## During an audit session
Tell Opus explicitly that the purpose is to challenge the existing work, not defend it. Do not let it repair everything it discovers before documenting the findings.

## After each session
Require:

- test results;
- changed files;
- evidence/data changes;
- decisions;
- deviations;
- debt;
- report;
- proposed handoff.

Then commit only the verified work.

---

# Human learning loop

For each session maintain a personal note outside the repository or in a private study log:

1. What did I learn?
2. What did I not understand?
3. What decision could I now make without Opus?
4. Which source or concept should I read independently?
5. Which part of the implementation could I explain in an interview?

At the end of each milestone, spend one session-equivalent block reviewing your own notes without Opus.

---

# Definition of success

The project is not successful merely because the site works.

Success means that by v1.0 you can independently explain:

- the AI compute supply chain represented by the system;
- why the data model is structured as it is;
- how claims and relationships are verified;
- how metrics are computed and what they cannot prove;
- why each agent exists and what it is allowed to do;
- where the code is modular and where technical debt remains;
- which policy conclusions are documented facts versus analysis;
- how the product helps a researcher or client answer a concrete question.
