# Documentation map

Where each governing document lives, what it holds, and its status. It also lists every audit artifact
required by `PROJECT-EVALUATION-FRAMEWORK.md` §11; planned artifacts are listed rather than created as empty
stubs (D-005). The repository holds the current system; session prompts and reports are kept in the private
development archive (D-151).

## Constitutional documents (repository root)

Precedence follows `SESSION-PROMPT-SPEC.md` §1: higher rows win.

| Document | Role |
|---|---|
| [`PROJECT-EVALUATION-FRAMEWORK.md`](../PROJECT-EVALUATION-FRAMEWORK.md) | Process and outcome audit framework (portfolio-wide) |
| [`CLAUDE.md`](../CLAUDE.md) | Project constitution and agent working rules |
| [`MASTER-ARCHITECTURE.md`](../MASTER-ARCHITECTURE.md) | Portfolio and Atlas architecture |
| [`SESSION-ROADMAP.md`](../SESSION-ROADMAP.md) | The plan: milestones M0–M7 and their sessions S00–S25 |
| [`SESSION-PROMPT-SPEC.md`](../SESSION-PROMPT-SPEC.md) | How a development session is specified, run and reported |

## Architecture and data model

| Document | What it holds | Status |
|---|---|---|
| [`architecture/baseline.md`](./architecture/baseline.md) | intended architecture, scope boundaries, current state, quality controls, frozen non-goals | approved 2026-09-29; state rows current |
| [`architecture/decisions.md`](./architecture/decisions.md) | the architecture decision log (append-only) | active |
| [`architecture/entity-taxonomy.md`](./architecture/entity-taxonomy.md) with [`../schemas/entities.schema.json`](../schemas/entities.schema.json) | why each entity type exists, its identity test; field shapes and vocabularies | accepted 2026-09-30 (D-022 to D-025) |
| [`architecture/relationship-taxonomy.md`](./architecture/relationship-taxonomy.md) with [`../schemas/relationships.schema.json`](../schemas/relationships.schema.json) | relation types, levels, evidence expectations; record shape and endpoint types | accepted 2026-09-30 (D-028 to D-033) |
| [`architecture/claim-model.md`](./architecture/claim-model.md) with [`../schemas/claims.schema.json`](../schemas/claims.schema.json) and the source record in [`../schemas/sources.schema.json`](../schemas/sources.schema.json) | claim types and evidence status; citations; staging, canonical and the human's review; the search record; `validate-data`; the trace | accepted 2026-09-30 (D-044 to D-053); review record D-151 |
| [`architecture/company-dataset.md`](./architecture/company-dataset.md) | the company records: legal-entity rulings, the ID rule, claim patterns, jurisdictions, attested anchors, record checks, freshness | accepted 2026-10-01 (D-054 to D-066) |
| [`architecture/concept-dataset.md`](./architecture/concept-dataset.md) | technologies, components and products: scope and gaps, the ID rule, working definitions, `broader`, record checks | accepted 2026-10-02 (D-067 to D-077) |
| [`architecture/facility-dataset.md`](./architecture/facility-dataset.md) with [`../schemas/events.schema.json`](../schemas/events.schema.json) and [`../tools/facility_status.py`](../tools/facility_status.py) | facility scope and ID rule, location without headquarters evidence, kind words, events, the derived status | accepted 2026-10-02 (D-078 to D-088) |
| [`architecture/edge-dataset.md`](./architecture/edge-dataset.md) with [`../tools/navigate.py`](../tools/navigate.py) and [`../schemas/refused_candidates.schema.json`](../schemas/refused_candidates.schema.json) | which candidates became edges and why the others did not; the edge ID rule; evidence guards; navigation; edge checks | accepted 2026-10-02 (D-089 to D-099); §1 amended (D-109) |
| [`../schemas/identity_basis.schema.json`](../schemas/identity_basis.schema.json) | the terms behind rule-made IDs and the claims behind identity fields | accepted 2026-10-03 (D-117) |
| [`architecture/sql-layer.md`](./architecture/sql-layer.md) with [`../tools/warehouse.py`](../tools/warehouse.py), [`../sql/`](../sql/) and [`../sql/results/`](../sql/results/) | the SQL layer: canonical vs derived, the rebuild, explicit states in SQL, lineage, the SQL tutorial, the tables loaded | accepted 2026-10-03 (D-117 to D-121) |
| [`architecture/metrics.md`](./architecture/metrics.md) | the metrics: evidence coverage, source age, the three supplier metrics shown as "cannot be computed yet"; rows vs records; placement | accepted 2026-10-06 (D-127 to D-132); revised after the analytical audit (D-133 to D-137) and for reported suppliers (D-148) |
| [`architecture/vertical-slice.md`](./architecture/vertical-slice.md) with [`../tools/build_page.py`](../tools/build_page.py), [`../tools/page_template.html`](../tools/page_template.html) and [`../site/hbm-chain/index.html`](../site/hbm-chain/index.html) | the HBM journey: question and scope, the visual specification, the text provenance rule, gaps, evidence panels, accessibility, page checks | accepted 2026-10-02 (D-100 to D-108) |
| [`architecture/visual-architecture.md`](./architecture/visual-architecture.md) with [`../tools/build_insight.py`](../tools/build_insight.py), [`../tools/insight_template.html`](../tools/insight_template.html) and [`../site/hbm-insight/index.html`](../site/hbm-insight/index.html) | the research view: seven layers from question to method, visual and UX principles, the minimal design system, the SQL-to-visual binding rule | accepted 2026-10-06 (D-123 to D-126) |
| [`agents/roles.md`](./agents/roles.md), [`agents/contracts.md`](./agents/contracts.md) | every agent role; the contracts of the active roles (inputs, outputs, allowed writes, gates) | accepted 2026-09-30 (D-052); Editorial and QA 2026-10-02 (D-107) |

## Research

| Document | What it holds | Status |
|---|---|---|
| [`research/source-policy.md`](./research/source-policy.md) | source classes, the preference matrix, evidence, conflict, retrieval and freshness rules, third-party criteria; the class of every registered source | accepted 2026-09-30 (D-034 to D-043); revised 2026-10-07 (D-144 to D-147) |
| [`research/domain-map.md`](./research/domain-map.md), [`research/source-register.md`](./research/source-register.md) | the physical AI stack as first mapped; the original source register | domain map: draft (terminology reviewed, D-016). Register: frozen (D-050) |
| [`research/visual-benchmark.md`](./research/visual-benchmark.md) | five data-intensive research products across fourteen dimensions; the adopt / adapt / reject register | accepted 2026-10-06 (D-122) |
| [`research/supplier-evidence-rules.md`](./research/supplier-evidence-rules.md) | the rules for supplier evidence: historical values, teardowns, sources registered at retrieval, third parties under the human's criteria | decided 2026-10-07 (D-144 to D-147) |
| [`research/hbm-supplier-research.md`](./research/hbm-supplier-research.md) with [`research/search-logs/hbm-supplier/`](./research/search-logs/hbm-supplier/) | who supplies the HBM in the H100 and in Trainium2, under those rules; the search plan and log | outcome decided 2026-10-07 |
| [`research/hbm-supplier-research-original-rules.md`](./research/hbm-supplier-research-original-rules.md) with [`research/search-logs/hbm-supplier-original-rules/`](./research/search-logs/hbm-supplier-original-rules/) | the same question under the earlier rules: the evidence found, why it could not name a supplier, the access gaps | outcome decided 2026-10-07 (D-141) |
| [`research/supplier-presentation.md`](./research/supplier-presentation.md) | how a reported supplier is shown on both pages | decided 2026-10-07 (D-148) |

## Quality and audits (`PROJECT-EVALUATION-FRAMEWORK.md` §11)

| Artifact | Status |
|---|---|
| [`quality/audit-history.md`](./quality/audit-history.md) | active: one row per audit |
| [`quality/human-reviews.md`](./quality/human-reviews.md) | active: the human's verdicts on claims, one entry per review (D-151) |
| [`architecture/milestone-audits/M0-audit.md`](./architecture/milestone-audits/M0-audit.md) | accepted 2026-09-29: M0 audit, process benchmark against `Eu-Digital-Policy`, maturity baseline |
| [`architecture/milestone-audits/M1-audit.md`](./architecture/milestone-audits/M1-audit.md) | accepted 2026-10-01: domain and evidence foundation |
| [`architecture/milestone-audits/M2-audit.md`](./architecture/milestone-audits/M2-audit.md) | accepted 2026-10-02 (D-109, D-110): canonical dataset and data architecture; its blocking finding remediated |
| [`architecture/milestone-audits/M3-audit.md`](./architecture/milestone-audits/M3-audit.md), [`M4-audit.md`](./architecture/milestone-audits/M4-audit.md) | accepted 2026-10-07 (D-140); M4 closed |
| [`research/content-audit.md`](./research/content-audit.md) with [`quality/audit-evidence/content-audit/`](./quality/audit-evidence/content-audit/) | content and evidence depth audit (PEF §6): findings ruled 2026-10-02 (D-111 to D-113); maturity accepted 2026-10-03 |
| [`architecture/analytical-audit.md`](./architecture/analytical-audit.md) with [`quality/audit-evidence/analytical-audit/`](./quality/audit-evidence/analytical-audit/) | analytical depth audit (PEF §8): verdicts decided 2026-10-07 (D-133 to D-138) |
| `research/content-review-log.md` | planned |
| `quality/evaluation-framework.md` | satisfied by the root `PROJECT-EVALUATION-FRAMEWORK.md` (not duplicated) |

Executable quality controls: the unit tests and Gate 0 run in CI; [`../tests/regression/`](../tests/regression/README.md)
holds the deliberate breaks and [`../tests/browser/`](../tests/browser/README.md) the browser QA scripts.
