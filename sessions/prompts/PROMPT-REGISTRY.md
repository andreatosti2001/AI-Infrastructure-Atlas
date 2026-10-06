# AI-Infrastructure-Atlas — Session Prompt Registry

Each prompt is an executable session contract for Opus 5.5. Do not edit a prompt retrospectively after the session has begun; record deviations in the session report.

| Session | Type | Milestone | Prompt | Primary gate |
|---:|---|---|---|---|
| S00 | ARCHITECTURE | M0 — Project Constitution | [`S00-PROMPT.md`](./S00-PROMPT.md) | independent runnable repo |
| S01 | RESEARCH | M0 — Project Constitution | [`S01-PROMPT.md`](./S01-PROMPT.md) | defensible domain map |
| S02 | AUDIT / SYNTHESIS | M0 — Project Constitution | [`S02-PROMPT.md`](./S02-PROMPT.md) | architecture baseline |
| S03 | ARCHITECTURE | M1 — Domain + Evidence Foundation | [`S03-PROMPT.md`](./S03-PROMPT.md) | stable entity schema |
| S04 | ARCHITECTURE | M1 — Domain + Evidence Foundation | [`S04-PROMPT.md`](./S04-PROMPT.md) | semantic relationship model |
| S05 | RESEARCH / ARCHITECTURE | M1 — Domain + Evidence Foundation | [`S05-PROMPT.md`](./S05-PROMPT.md) | source/evidence policy |
| S06 | IMPLEMENTATION | M1 — Domain + Evidence Foundation | [`S06-PROMPT.md`](./S06-PROMPT.md) | claim provenance works |
| S07 | RESEARCH / IMPLEMENTATION | M2 — Canonical Dataset | [`S07-PROMPT.md`](./S07-PROMPT.md) | curated company anchors |
| S08 | IMPLEMENTATION | M2 — Canonical Dataset | [`S08-PROMPT.md`](./S08-PROMPT.md) | technical vocabulary |
| S09 | RESEARCH / IMPLEMENTATION | M2 — Canonical Dataset | [`S09-PROMPT.md`](./S09-PROMPT.md) | temporal facility model |
| S10 | IMPLEMENTATION | M2 — Canonical Dataset | [`S10-PROMPT.md`](./S10-PROMPT.md) | auditable supply edges |
| S11 | IMPLEMENTATION | M3 — Vertical Slice + Audit | [`S11-PROMPT.md`](./S11-PROMPT.md) | end-to-end trace |
| S12 | AUDIT | M3 — Vertical Slice + Audit | [`S12-PROMPT.md`](./S12-PROMPT.md) | data model passes audit |
| S13 | AUDIT | M3 — Vertical Slice + Audit | [`S13-PROMPT.md`](./S13-PROMPT.md) | content passes audit |
| S14 | ARCHITECTURE / IMPLEMENTATION | M4 — Analytical Intelligence | [`S14-PROMPT.md`](./S14-PROMPT.md) | reproducible SQL layer |
| S14.5 | RESEARCH / ARCHITECTURE / LIMITED IMPLEMENTATION | M4 — Analytical Intelligence | [`S14.5-PROMPT.md`](./S14.5-PROMPT.md) | traceable research experience |
| S15 | ANALYSIS | M4 — Analytical Intelligence | [`S15-PROMPT.md`](./S15-PROMPT.md) | transparent metrics |
| S16 | AUDIT | M4 — Analytical Intelligence | [`S16-PROMPT.md`](./S16-PROMPT.md) | analytical validity |
| S17 | RESEARCH / ARCHITECTURE | M5 — Policy / Geopolitical Layer | [`S17-PROMPT.md`](./S17-PROMPT.md) | bounded policy layer |
| S18 | IMPLEMENTATION | M5 — Policy / Geopolitical Layer | [`S18-PROMPT.md`](./S18-PROMPT.md) | policy relationships |
| S19 | AUDIT | M5 — Policy / Geopolitical Layer | [`S19-PROMPT.md`](./S19-PROMPT.md) | agent system justified |
| S20 | IMPLEMENTATION | M6 — Client Product | [`S20-PROMPT.md`](./S20-PROMPT.md) | research UX journeys |
| S21 | IMPLEMENTATION | M6 — Client Product | [`S21-PROMPT.md`](./S21-PROMPT.md) | reproducible client briefs |
| S22 | AUDIT | M7 — Final Audits + Release | [`S22-PROMPT.md`](./S22-PROMPT.md) | release-grade engineering |
| S23 | AUDIT | M7 — Final Audits + Release | [`S23-PROMPT.md`](./S23-PROMPT.md) | research depth |
| S24 | AUDIT | M7 — Final Audits + Release | [`S24-PROMPT.md`](./S24-PROMPT.md) | capability evidence |
| S25 | SYNTHESIS / RELEASE | M7 — Final Audits + Release | [`S25-PROMPT.md`](./S25-PROMPT.md) | coherent v1.0 |

## Execution rule

Start each session by reading `CLAUDE.md`, `MASTER-ARCHITECTURE.md`, `PROJECT-EVALUATION-FRAMEWORK.md`, `SESSION-PROMPT-SPEC.md`, the immediately prior session report, and the current repository state. The session prompt is subordinate to those higher-level documents.

## Prompt lifecycle

```text
prompt (immutable during session)
        ↓
session execution
        ↓
session report
        ↓
audit / decision
        ↓
next-session context
```

The goal is not to make every session succeed exactly as planned. The goal is to make every deviation visible, classified, and useful for the next decision.
