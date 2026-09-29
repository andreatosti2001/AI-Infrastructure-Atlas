# Documentation map

Where each governing document lives, and the status of every audit artifact required by
`PROJECT-EVALUATION-FRAMEWORK.md` §11. Planned artifacts are listed rather than created as
empty stubs (decision D-005).

## Constitutional documents (repository root)

Precedence follows `SESSION-PROMPT-SPEC.md` §1: higher rows win.

| Document | Role |
|---|---|
| [`PROJECT-EVALUATION-FRAMEWORK.md`](../PROJECT-EVALUATION-FRAMEWORK.md) | Process + outcome audit framework (portfolio-wide) |
| [`CLAUDE.md`](../CLAUDE.md) | Project constitution and agent working rules |
| [`MASTER-ARCHITECTURE.md`](../MASTER-ARCHITECTURE.md) | Portfolio and Atlas architecture |
| [`SESSION-ROADMAP.md`](../SESSION-ROADMAP.md) | S00–S25 session plan |
| [`sessions/prompts/`](../sessions/prompts/) | Per-session prompts (work contracts) |

Supporting: [`SESSION-PROMPT-SPEC.md`](../SESSION-PROMPT-SPEC.md) (prompt/report format),
[`AI-Infrastructure-Atlas-Operational-Roadmap.md`](../AI-Infrastructure-Atlas-Operational-Roadmap.md)
(calendar and human workflow), [`OPUS-5.5-BOOTSTRAP-PROMPT.md`](../OPUS-5.5-BOOTSTRAP-PROMPT.md)
(original bootstrap prompt; superseded by the session system and kept as history — D-009).

## Audit artifacts (`PROJECT-EVALUATION-FRAMEWORK.md` §11)

| Artifact | Status | Owner |
|---|---|---|
| [`architecture/baseline.md`](./architecture/baseline.md) | approved 2026-09-29 (S02; approval record §8) | S00; approved at S02 |
| [`architecture/decisions.md`](./architecture/decisions.md) | active | every session |
| [`architecture/milestone-audits/M0-audit.md`](./architecture/milestone-audits/M0-audit.md) | accepted (S02; M0 closed 2026-09-29): M0 audit, EU-DP process benchmark, maturity baseline, v1 concept classification | one per milestone |
| `research/source-policy.md` | planned | S05 |
| `research/content-review-log.md` | planned | first session that records claims |
| `agents/roles.md`, `agents/contracts.md` | planned | S06 (D-010) |
| `quality/evaluation-framework.md` | satisfied by root `PROJECT-EVALUATION-FRAMEWORK.md` (not duplicated) | — |
| [`quality/audit-history.md`](./quality/audit-history.md) | active | every audit |

## Research outputs

| Artifact | Status | Owner |
|---|---|---|
| [`research/domain-map.md`](./research/domain-map.md), [`research/source-register.md`](./research/source-register.md) | draft (S01; terminology reviewed 2026-09-29, D-016; weekly gate open) | S01; register frozen after S06 migration |
