# SESSION-PROMPT-SPEC — Governed Opus 5.5 Development Sessions

## Purpose

Every substantive development session in the Technology Policy portfolio must be driven by a session-specific prompt derived from the project's `CLAUDE.md`, `MASTER-ARCHITECTURE.md`, the shared `PROJECT-EVALUATION-FRAMEWORK.md`, and the actual repository state.

The session prompt is a **work contract**, not a generic instruction to "continue development".

Its job is to constrain Opus 5.5 enough to prevent uncontrolled scope expansion while leaving room for expert reasoning, discovery, and justified architectural change.

---

## 1. Prompt hierarchy

```text
Portfolio evaluation framework
        ↓
Project constitution / CLAUDE.md
        ↓
Master architecture
        ↓
Session roadmap
        ↓
Session prompt
        ↓
Task-level execution
```

Lower layers cannot silently override higher layers.

If the current repository state contradicts the planned session, Opus must first diagnose the contradiction and classify it as:

- expected evolution;
- harmless drift;
- blocking architecture issue;
- evidence/research issue;
- regression;
- scope violation.

---

## 2. Required session prompt anatomy

Every session prompt must contain the following sections in this order.

### 01 — Session identity

- session number;
- session title;
- session type;
- milestone;
- predecessor session;
- expected successor;
- expected duration/complexity class.

### 02 — Mission

One precise sentence describing what the session must accomplish.

### 03 — Why this session exists

Explain the research, architectural, product, or process reason for the session.

### 04 — Current state

Summarize the repository state that the session inherits. The prompt should identify relevant files, datasets, tests, decisions, and unresolved issues.

### 05 — Inputs and evidence

Specify:

- documents to read;
- repository paths to inspect;
- datasets to use;
- external research required;
- previous session report(s);
- relevant audit findings.

### 06 — Required reasoning

State the questions Opus must answer before modifying code or data.

The model should not jump directly from the mission to implementation.

### 07 — Tasks

Tasks should be ordered and testable. Separate:

- research;
- design;
- implementation;
- validation;
- documentation.

### 08 — Explicit non-goals

List work that is explicitly out of scope, even if Opus identifies opportunities to perform it.

This is mandatory.

### 09 — Constraints

Include technical, evidence, architectural, stylistic, performance, security, and portfolio constraints that matter to the session.

### 10 — Agent responsibilities

Identify which agents may act and what each may write. Agents not named in the session are inactive unless escalation is required.

### 11 — Data and evidence rules

Specify:

- canonical entities;
- allowed relationship types;
- required source tier;
- provenance requirements;
- temporal requirements;
- confidence rules;
- treatment of unknown/unverified data.

### 12 — Implementation rules

Specify:

- allowed files/directories to modify;
- preferred implementation approach;
- prohibited architectural shortcuts;
- dependency policy;
- migration/rebuild expectations.

### 13 — Verification plan

Every implementation must have an explicit verification plan covering relevant combinations of:

- unit tests;
- schema validation;
- data integrity checks;
- evidence checks;
- browser QA;
- accessibility checks;
- performance checks;
- regression tests.

### 14 — Evaluation requirements

Each session must leave evidence that can later be used for the process + outcome audit.

At minimum capture:

- decisions made;
- deviations from plan;
- assumptions invalidated;
- new debt;
- rejected alternatives;
- unresolved questions.

### 15 — Acceptance criteria

Criteria must be observable and binary where practical.

Bad: "make the model robust."

Good: "every published `depends_on` relationship has a source ID, source locator, verification state and target/source entity IDs."

### 16 — Stop conditions

Opus must stop implementation and report instead of improvising when:

- evidence is insufficient for a material claim;
- the proposed change requires a schema break not covered by the session;
- the task would expand scope materially;
- a security/integrity concern is discovered;
- the architecture would need a different foundational decision;
- the expected user value is no longer clear.

When a stop needs a human decision, the question is written as a `CLAUDE.md` §9A human decision request (see §9 below).

### 17 — Deliverables

List exact artifacts expected at session end.

### 18 — Handoff

State exactly what the next session should receive:

- completed work;
- open issues;
- audit findings;
- recommended next decision, explained per `CLAUDE.md` §9A if it needs the human;
- files to read first.

---

## 3. Session types

Use one primary type per session.

### RESEARCH
Domain understanding, source mapping, taxonomy, evidence baseline.

### ARCHITECTURE
Data model, agent model, interfaces, system boundaries, schema evolution.

### IMPLEMENTATION
Code, data ingestion, frontend, analytics, exports.

### AUDIT
Independent examination of process, result, evidence, code, data, agents, or UX.

### SYNTHESIS
Integrate prior work, resolve competing approaches, prepare the next milestone.

A session may contain secondary activities, but it must have one dominant purpose.

---

## 4. Build/Audit cadence

Do not stack long build sequences without independent review.

Recommended cadence:

```text
1–3 build/research sessions
        ↓
1 audit or synthesis session
        ↓
1–3 build sessions
        ↓
1 audit
```

Mandatory audits:

- after the first vertical slice;
- after the first analytical layer;
- after the first policy layer;
- before client mode is considered stable;
- before v1.0;
- after any foundational schema change.

---

## 5. Session reports

Each session must create a report at:

`sessions/reports/SESSION-XX-REPORT.md`

Minimum fields:

- mission outcome;
- files changed;
- data changed;
- tests run;
- evidence added/retired;
- decisions made;
- deviations;
- debt introduced/resolved;
- unresolved issues;
- process lessons;
- implications for the next session.

A session is incomplete without a report, even if the implementation itself works.

Any human approval or choice the report asks for (typically under unresolved issues) is written as a `CLAUDE.md` §9A human decision request. A list of decision IDs with short titles is not sufficient (§9).

---

## 6. Prompt revision policy

A later session may reveal that an earlier prompt was based on a flawed assumption.

Do not silently rewrite history.

Instead:

1. preserve the original session prompt;
2. record the invalidated assumption in the report;
3. create an explicit decision record;
4. revise only future prompts;
5. if necessary, add a retrospective note explaining the divergence.

This makes the development history itself auditable.

---

## 7. Anti-vibecoding protections

Opus must not:

- expand scope because an adjacent feature is easy to add;
- introduce dependencies without documenting why they are necessary;
- change canonical semantics without a migration decision;
- fabricate facts to complete a dataset;
- convert search snippets or secondary reporting into primary evidence without qualification;
- create metrics before defining the question and denominator;
- optimize UI before validating the underlying data and user journey;
- claim that a session is complete because tests pass if the research/content requirements are incomplete.

The objective is **controlled AI-assisted engineering**, not maximum code output per session.

---

## 8. Portfolio signal requirement

Every substantial session should contribute to at least one demonstrable capability:

- domain research;
- evidence methodology;
- data modelling;
- quantitative analysis;
- Python/SQL;
- AI agent orchestration;
- software engineering;
- product design;
- reproducibility;
- professional communication.

If a sequence of sessions produces implementation but no new capability signal, the roadmap must be revisited.

---

## 9. Human decision requests

The rule lives in `CLAUDE.md` §9A; this section only says where it applies in the session system.

Every request for a human decision made during or about a session must follow `CLAUDE.md` §9A. This covers:

- questions asked during the session, in conversation or through an interactive question tool;
- the human-approvals part of a session report (§5);
- open questions written into a session prompt for the human to answer before or during the session;
- decision records in `docs/architecture/decisions.md` that are `proposed` and await the human's review: the review request lists, for each record, what changes in plain language, not only its ID and title.

In practice:

- lead with what will be different in the project, then give `D-xxx`, `Sxx`, `H-x`, schema or file names as the technical reference;
- give every option a descriptive title and a concrete consequence;
- group several small, consequence-free confirmations into one short line rather than inflating each into a full request;
- if the session cannot say what A changes compared with B, it is not ready to ask; it reports the gap instead;
- in a session prompt, an open question's options carry outcome titles (what the project will be afterwards), never "Accept all", "Accept with changes" or "Reject", because the session will reuse them as the labels of an interactive question (`CLAUDE.md` §9A, interactive questions);
- a bundled approval lists each item with one plain sentence of what it changes, in the question itself.

A session loads `CLAUDE.md` when it starts and does not see later changes on its own. When a session merges the base branch, or otherwise pulls in new commits, it checks whether `CLAUDE.md`, `MASTER-ARCHITECTURE.md` or this file changed (`git diff --stat` over the merge) and, if so, re-reads them before asking the human anything further.

When a decision has already been taken, the record of the answer (for example a session prompt's "human decisions taken" list) keeps the human's words verbatim; the §9A format applies to the question, not to rewriting the answer.
