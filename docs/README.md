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
| [`architecture/milestone-audits/M1-audit.md`](./architecture/milestone-audits/M1-audit.md) | accepted (S07 review, 2026-10-01; H-5): M1 audit over S03–S06, findings, maturity ratings | S07 (D-066) |
| [`research/source-policy.md`](./research/source-policy.md) (source classes, preference matrix, evidence, conflict, retrieval and freshness rules; class of every registered source) with [`../schemas/sources.schema.json`](../schemas/sources.schema.json) (the source-class vocabulary) | accepted (S05 review, 2026-09-30; D-034 to D-043) | S05 |
| `research/content-review-log.md` | planned | first session that records claims |
| [`agents/roles.md`](./agents/roles.md), [`agents/contracts.md`](./agents/contracts.md) (every CLAUDE.md §8 role; MA §12 contracts for the roles active through S10) | accepted (S06 review, 2026-09-30; D-052) | S06 (D-010) |
| `quality/evaluation-framework.md` | satisfied by root `PROJECT-EVALUATION-FRAMEWORK.md` (not duplicated) | — |
| [`quality/audit-history.md`](./quality/audit-history.md) | active | every audit |

## Data model

| Artifact | Status | Owner |
|---|---|---|
| [`architecture/entity-taxonomy.md`](./architecture/entity-taxonomy.md) (why each type exists; v1 concept and MA mappings) with [`../schemas/entities.schema.json`](../schemas/entities.schema.json) (field shapes and vocabulary values) | accepted (S03 review, 2026-09-30; D-022 to D-025) | S03 |
| [`architecture/relationship-taxonomy.md`](./architecture/relationship-taxonomy.md) (relation types, levels, evidence expectations, verb reconciliation, DEP mapping) with [`../schemas/relationships.schema.json`](../schemas/relationships.schema.json) (record shape, vocabulary, endpoint types) | accepted (S04 review, 2026-09-30; D-028 to D-033) | S04 |
| Source-class vocabulary | accepted (S05 review, 2026-09-30): [`../schemas/sources.schema.json`](../schemas/sources.schema.json) | S05 |
| [`architecture/claim-model.md`](./architecture/claim-model.md) (claim types and evidence status, MA §10 reconciled; citations; `verified`; staging and canonical; the search record; the migration; `validate-data`; the trace) with [`../schemas/claims.schema.json`](../schemas/claims.schema.json) and the source record in [`../schemas/sources.schema.json`](../schemas/sources.schema.json) | accepted (S06 review, 2026-09-30; D-044 to D-053) | S06 |
| [`architecture/company-dataset.md`](./architecture/company-dataset.md) (the seed, legal-entity rulings, the ID rule, claim patterns, jurisdictions, entity staging and canonical, attested anchors, record checks, freshness) | accepted (S07 review, 2026-10-01; D-054 to D-066) | S07 |
| [`architecture/concept-dataset.md`](./architecture/concept-dataset.md) (concept scope and gaps, the concept table and ID rule, working definitions, `broader`, new sources and re-retrievals, products, record checks) | accepted (S08 review, 2026-10-02) except D-070 and D-076, which stay proposed | S08 |
| [`../data/sources.json`](../data/sources.json), [`../data/claims.json`](../data/claims.json), [`../data/companies.json`](../data/companies.json), [`../data/jurisdictions.json`](../data/jurisdictions.json), [`../data/technologies.json`](../data/technologies.json), [`../data/components.json`](../data/components.json), [`../data/products.json`](../data/products.json) (canonical; the S07 and S08 records accepted by the human in the session), with staging copies under [`../data/staging/`](../data/staging/) | S06, S07, S08 | S06, S07, S08; later sessions add records |
| First product records | done: 3 canonical products (S08, D-072) | S08 (D-027) |
| Event schema | planned | S09 (D-022) |

## Research outputs

| Artifact | Status | Owner |
|---|---|---|
| [`research/domain-map.md`](./research/domain-map.md), [`research/source-register.md`](./research/source-register.md) | domain map: draft (S01; terminology reviewed 2026-09-29, D-016; weekly gate open). Register: frozen (S06 migration, D-050) | S01 |
