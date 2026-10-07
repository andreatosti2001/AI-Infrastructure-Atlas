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
| [`architecture/milestone-audits/M2-audit.md`](./architecture/milestone-audits/M2-audit.md) (the M2 audit over S07–S10 and the S12 data-architecture audit: findings, maturity ratings, the blocking finding and its remediation, debt with owners, the refused-candidate design) | accepted (S13 opening review, 2026-10-02; D-109, D-110) | S12 |
| [`architecture/milestone-audits/M3-audit.md`](./architecture/milestone-audits/M3-audit.md) and [`architecture/milestone-audits/M4-audit.md`](./architecture/milestone-audits/M4-audit.md) (the M3 and M4 milestone audits, written after the fact: PEF §4's eight questions, process findings, maturity where newly evidenced) | accepted by the human (2026-10-07; D-140); M4 closed | S16.5 |
| [`research/source-policy.md`](./research/source-policy.md) (source classes, preference matrix, evidence, conflict, retrieval and freshness rules; class of every registered source) with [`../schemas/sources.schema.json`](../schemas/sources.schema.json) (the source-class vocabulary) | accepted (S05 review, 2026-09-30; D-034 to D-043) | S05 |
| `research/content-review-log.md` | planned | first session that records claims |
| [`research/content-audit-S13.md`](./research/content-audit-S13.md) (the S13 content and evidence depth audit: the sample, the re-reads, the page against its evidence, source quality and freshness exposure, findings F-1 to F-11, maturity) with [`../sessions/reports/SESSION-13-sample/`](../sessions/reports/SESSION-13-sample/) (the sampling and re-read scripts and their outputs) | findings ruled by the human (S13 review, 2026-10-02; D-111 to D-113 accepted); maturity ratings accepted by the human on 2026-10-03 (S14 opening) | S13 |
| [`agents/roles.md`](./agents/roles.md), [`agents/contracts.md`](./agents/contracts.md) (every CLAUDE.md §8 role; MA §12 contracts for the roles active through S11) | accepted (S06 review, 2026-09-30; D-052); Editorial and QA contracts accepted (S12 opening review, 2026-10-02; D-107) | S06 (D-010); S11 |
| `quality/evaluation-framework.md` | satisfied by root `PROJECT-EVALUATION-FRAMEWORK.md` (not duplicated) | — |
| [`architecture/analytical-audit-S16.md`](./architecture/analytical-audit-S16.md) (the S16 analytical depth audit: each metric's measures, non-measures, missing data, selection, presentation; cold readings, reproduction, sensitivity probes; D-130 and D-124 as applied; findings C-1 to C-9, E-1, E-2; maturity) with [`../sessions/reports/SESSION-16-cold-reading/`](../sessions/reports/SESSION-16-cold-reading/), [`../sessions/reports/SESSION-16-reproduction/`](../sessions/reports/SESSION-16-reproduction/) and [`../sessions/reports/SESSION-16-probes/`](../sessions/reports/SESSION-16-probes/) | verdicts decided by the human (2026-10-07; D-133 to D-138) | S16 |
| [`research/hbm-supplier-research-S16.5.md`](./research/hbm-supplier-research-S16.5.md) (who supplies the HBM in the H100 and in Trainium2: the evidence found, the rules applied, the access gaps) with [`../sessions/reports/SESSION-16.5-research/`](../sessions/reports/SESSION-16.5-research/) (the search plan and log) | outcome decided by the human (2026-10-07; D-141) | S16.5 |
| [`quality/audit-history.md`](./quality/audit-history.md) | active | every audit |

## Data model

| Artifact | Status | Owner |
|---|---|---|
| [`architecture/entity-taxonomy.md`](./architecture/entity-taxonomy.md) (why each type exists; v1 concept and MA mappings) with [`../schemas/entities.schema.json`](../schemas/entities.schema.json) (field shapes and vocabulary values) | accepted (S03 review, 2026-09-30; D-022 to D-025) | S03 |
| [`architecture/relationship-taxonomy.md`](./architecture/relationship-taxonomy.md) (relation types, levels, evidence expectations, verb reconciliation, DEP mapping) with [`../schemas/relationships.schema.json`](../schemas/relationships.schema.json) (record shape, vocabulary, endpoint types) | accepted (S04 review, 2026-09-30; D-028 to D-033) | S04 |
| Source-class vocabulary | accepted (S05 review, 2026-09-30): [`../schemas/sources.schema.json`](../schemas/sources.schema.json) | S05 |
| [`architecture/claim-model.md`](./architecture/claim-model.md) (claim types and evidence status, MA §10 reconciled; citations; `verified`; staging and canonical; the search record; the migration; `validate-data`; the trace) with [`../schemas/claims.schema.json`](../schemas/claims.schema.json) and the source record in [`../schemas/sources.schema.json`](../schemas/sources.schema.json) | accepted (S06 review, 2026-09-30; D-044 to D-053) | S06 |
| [`architecture/company-dataset.md`](./architecture/company-dataset.md) (the seed, legal-entity rulings, the ID rule, claim patterns, jurisdictions, entity staging and canonical, attested anchors, record checks, freshness) | accepted (S07 review, 2026-10-01; D-054 to D-066) | S07 |
| [`architecture/concept-dataset.md`](./architecture/concept-dataset.md) (concept scope and gaps, the concept table and ID rule, working definitions, `broader`, new sources and re-retrievals, products, record checks) | accepted (S08 review, 2026-10-02; D-070 and D-076 at the end of S09) | S08 |
| [`../data/sources.json`](../data/sources.json), [`../data/claims.json`](../data/claims.json), [`../data/companies.json`](../data/companies.json), [`../data/jurisdictions.json`](../data/jurisdictions.json), [`../data/technologies.json`](../data/technologies.json), [`../data/components.json`](../data/components.json), [`../data/products.json`](../data/products.json), [`../data/facilities.json`](../data/facilities.json), [`../data/events.json`](../data/events.json), [`../data/relationships.json`](../data/relationships.json), [`../data/refused_candidates.json`](../data/refused_candidates.json), [`../data/identity_basis.json`](../data/identity_basis.json) (canonical; the S07 to S10 records, the S12 refused candidates, accepted by the human in the session, and the S14 identity-basis rows moved from four document tables, D-117, schema [`../schemas/identity_basis.schema.json`](../schemas/identity_basis.schema.json)), with staging copies under [`../data/staging/`](../data/staging/) | S06 to S14 | S06 to S10, S12, S14; later sessions add records |
| First product records | done: 3 canonical products (S08, D-072) | S08 (D-027) |
| [`architecture/facility-dataset.md`](./architecture/facility-dataset.md) (facility scope, the facility ID rule, location without headquarters evidence, kind words, ownership and operation evidence for S10, events, the status derivation, capacity, record checks) with [`../schemas/events.schema.json`](../schemas/events.schema.json) (event shape and types) and [`../tools/facility_status.py`](../tools/facility_status.py) | accepted (S09 reviews, 2026-10-02; D-078 to D-088) | S09 |
| Event schema | done: `schemas/events.schema.json`, accepted at the S09 review (D-083) | S09 (D-022) |
| [`architecture/edge-dataset.md`](./architecture/edge-dataset.md) (which candidates became edges and why the others did not, the edge ID rule, evidence guards and relation words, navigation, edge checks) with [`../tools/navigate.py`](../tools/navigate.py); the refused candidates became records in S12 ([`../schemas/refused_candidates.schema.json`](../schemas/refused_candidates.schema.json), D-109), and §1 keeps the rule | accepted (S10 review, 2026-10-02; D-089 to D-099); §1 amended in S12 (D-109, accepted at the S13 opening) | S10, S12 |
| [`architecture/vertical-slice.md`](./architecture/vertical-slice.md) (the HBM journey: question and scope, the walk, the visual specification, the text provenance rule, gaps, evidence panels, accessibility, the page checks, the new-user test) with [`../tools/build_page.py`](../tools/build_page.py), [`../tools/page_template.html`](../tools/page_template.html) and the generated [`../site/hbm-chain/index.html`](../site/hbm-chain/index.html) | accepted (S12 opening review, 2026-10-02; D-100 to D-108) | S11 |
| [`architecture/visual-architecture.md`](./architecture/visual-architecture.md) (the research-experience model QUESTION → INSIGHT → VISUAL → EXPLORE → EVIDENCE → DATA → METHOD, visual and UX principles, the minimal design system, the information architecture proposed for S20, the component inventory, the visual grammar, evidence-aware semantics, when a visual and when a table, the SQL-to-visual binding rule, the S14.5 / S15–S16 / S20 boundary) with [`../tools/build_insight.py`](../tools/build_insight.py), [`../tools/insight_template.html`](../tools/insight_template.html) and the generated prototype [`../site/hbm-insight/index.html`](../site/hbm-insight/index.html) | accepted (S14.5 review, 2026-10-06; D-123 to D-126) | S14.5 |
| [`architecture/metrics.md`](./architecture/metrics.md) (the first metrics: evidence coverage, source age, and the three supplier metrics shown as "cannot be computed yet"; rows vs records; the evidence-date basis; queries built on queries; placement; rejected alternatives) with the queries [`../sql/evidence_coverage.sql`](../sql/evidence_coverage.sql), [`../sql/source_age.sql`](../sql/source_age.sql), [`../sql/supplier_metrics.sql`](../sql/supplier_metrics.sql), each answering PEF §8 in its header | accepted (S15 review, 2026-10-06; D-127 to D-132); audited in S16: coverage and source age modified, the publishers tally retired, the supplier metrics kept (2026-10-07; D-133 to D-137) | S15, S16 |
| [`architecture/sql-layer.md`](./architecture/sql-layer.md) (the SQL layer: canonical vs derived, the rebuild, explicit states in SQL, lineage, the page and the build, the SQL tutorial, the first question and the weaknesses it shows, the tables loaded, what S15 receives) with [`../tools/warehouse.py`](../tools/warehouse.py), the queries in [`../sql/`](../sql/) and their results in [`../sql/results/`](../sql/results/) | accepted (S14 review, 2026-10-03; D-117 to D-121) | S14 |

## Research outputs

| Artifact | Status | Owner |
|---|---|---|
| [`research/visual-benchmark-S14.5.md`](./research/visual-benchmark-S14.5.md) (Epoch AI, Our World in Data, IEA, Stanford AI Index and Datawrapper across fourteen dimensions; the ADOPT / ADAPT / REJECT register P-01 to P-29) | accepted (S14.5 review, 2026-10-06; D-122) | S14.5 |
| [`research/domain-map.md`](./research/domain-map.md), [`research/source-register.md`](./research/source-register.md) | domain map: draft (S01; terminology reviewed 2026-09-29, D-016; weekly gate open). Register: frozen (S06 migration, D-050) | S01 |
