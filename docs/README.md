# Documentation map

Where each governing document lives, what it holds, and its status. It also lists every audit artifact
required by `PROJECT-EVALUATION-FRAMEWORK.md` §11; planned artifacts are listed rather than created as empty
stubs (D-005). The repository holds the current system; session prompts and reports are kept in the private
development archive, the private repository `atlas-dev-archive` (D-151, D-152).

## Constitutional documents (repository root)

Precedence follows `SESSION-PROMPT-SPEC.md` §1: higher rows win.

| Document | Role |
|---|---|
| [`PROJECT-EVALUATION-FRAMEWORK.md`](../PROJECT-EVALUATION-FRAMEWORK.md) | Process and outcome audit framework (portfolio-wide) |
| [`CLAUDE.md`](../CLAUDE.md) | Project constitution and agent working rules |
| [`MASTER-ARCHITECTURE.md`](../MASTER-ARCHITECTURE.md) | Portfolio and Atlas architecture |
| [`SESSION-ROADMAP.md`](../SESSION-ROADMAP.md) | The plan: milestones M0–M7 and their sessions S00–S25 |
| [`VERSION-ROADMAP.md`](../VERSION-ROADMAP.md) | After v1.0: v1.5 (visual intelligence) and v2 (coverage of the global chain), planned (D-201) |
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
| [`architecture/policy-dataset.md`](./architecture/policy-dataset.md) with [`../tools/policy_status.py`](../tools/policy_status.py) | the policy layer: which instruments the Atlas records, one record per published act, its fields, dates as events and the derived status, normative text as claims, the official-legal-text class, the links defined for S18, description never advice, the checks PL-1 to PL-9 | accepted 2026-10-08 (D-154 to D-164) |
| [`architecture/edge-dataset.md`](./architecture/edge-dataset.md) with [`../tools/navigate.py`](../tools/navigate.py) and [`../schemas/refused_candidates.schema.json`](../schemas/refused_candidates.schema.json) | which candidates became edges and why the others did not; the edge ID rule; evidence guards; navigation; edge checks | accepted 2026-10-02 (D-089 to D-099); §1 amended (D-109) |
| [`../schemas/identity_basis.schema.json`](../schemas/identity_basis.schema.json) | the terms behind rule-made IDs and the claims behind identity fields | accepted 2026-10-03 (D-117) |
| [`architecture/sql-layer.md`](./architecture/sql-layer.md) with [`../tools/warehouse.py`](../tools/warehouse.py), [`../sql/`](../sql/) and [`../sql/results/`](../sql/results/) | the SQL layer: canonical vs derived, the rebuild, explicit states in SQL, lineage, the SQL tutorial, the tables loaded | accepted 2026-10-03 (D-117 to D-121) |
| [`architecture/metrics.md`](./architecture/metrics.md) | the metrics: evidence coverage, source age, the three supplier metrics shown as "cannot be computed yet"; rows vs records; placement | accepted 2026-10-06 (D-127 to D-132); revised after the analytical audit (D-133 to D-137) and for reported suppliers (D-148) |
| [`architecture/vertical-slice.md`](./architecture/vertical-slice.md) with [`../tools/build_page.py`](../tools/build_page.py), [`../tools/page_template.html`](../tools/page_template.html) and [`../site/hbm-chain/index.html`](../site/hbm-chain/index.html) | the HBM journey: question and scope, the visual specification, the text provenance rule, gaps, evidence panels, accessibility, page checks | accepted 2026-10-02 (D-100 to D-108) |
| [`architecture/visual-architecture.md`](./architecture/visual-architecture.md) with [`../tools/build_insight.py`](../tools/build_insight.py), [`../tools/insight_template.html`](../tools/insight_template.html) and [`../site/hbm-insight/index.html`](../site/hbm-insight/index.html) | the research view: seven layers from question to method, visual and UX principles, the minimal design system, the SQL-to-visual binding rule | accepted 2026-10-06 (D-123 to D-126); §15, the research journeys, accepted 2026-10-14 (D-189 to D-197), with [`../tools/build_journeys.py`](../tools/build_journeys.py), [`../tools/journey_template.html`](../tools/journey_template.html) and the entry page [`../site/index.html`](../site/index.html) |
| [`architecture/client-brief.md`](./architecture/client-brief.md) with [`../tools/build_brief.py`](../tools/build_brief.py), [`../tools/brief_template.html`](../tools/brief_template.html) and [`../site/briefs/accelerator-memory/index.html`](../site/briefs/accelerator-memory/index.html) | the client brief: question and scope, twelve sections, a summary composed from groups and tallies, what travels with the brief (U-5, P-18), owners, the one composition mechanism for templates, checks BR-1 to BR-12 | accepted 2026-10-14 (D-202 to D-206) |
| [`agents/roles.md`](./agents/roles.md), [`agents/contracts.md`](./agents/contracts.md) | every agent role; the contracts of the active roles (inputs, outputs, allowed writes, gates) | accepted 2026-09-30 (D-052); Editorial and QA 2026-10-02 (D-107); S19's rulings 2026-10-14: the Analyst active, every file has an owner (checked), the Verifier re-scoped, drafts always in staging, no runtime (D-180 to D-184); the Client Output active from S21 (D-205) |

## Research

| Document | What it holds | Status |
|---|---|---|
| [`architecture/policy-links.md`](./architecture/policy-links.md) | the policy links: `restricts` at a policy level from an act to a class its own text names, the term rule, scope kept in the text, later changes quoted, the `rel:restricts` row, refused candidates, pages and navigation, the checks PK-1 to PK-7 | accepted 2026-10-13 (D-165 to D-174) |
| [`research/source-policy.md`](./research/source-policy.md) | source classes, the preference matrix, evidence, conflict, retrieval and freshness rules, third-party criteria; the class of every registered source | accepted 2026-09-30 (D-034 to D-043); revised 2026-10-07 (D-144 to D-147) and 2026-10-08 (the official-legal-text class and the policy rows, D-158); 2026-10-13 (`rel:restricts`, D-171) |
| [`research/domain-map.md`](./research/domain-map.md), [`research/source-register.md`](./research/source-register.md) | the physical AI stack as first mapped; the original source register | domain map: draft (terminology reviewed, D-016). Register: frozen (D-050) |
| [`research/visual-benchmark.md`](./research/visual-benchmark.md) | five data-intensive research products across fourteen dimensions; the adopt / adapt / reject register | accepted 2026-10-06 (D-122) |
| [`research/supplier-evidence-rules.md`](./research/supplier-evidence-rules.md) | the rules for supplier evidence: historical values, teardowns, sources registered at retrieval, third parties under the human's criteria | decided 2026-10-07 (D-144 to D-147) |
| [`research/hbm-supplier-research.md`](./research/hbm-supplier-research.md) with [`research/search-logs/hbm-supplier/`](./research/search-logs/hbm-supplier/) | who supplies the HBM in the H100 and in Trainium2, under those rules; the search plan and log | outcome decided 2026-10-07 |
| [`research/hbm-supplier-research-original-rules.md`](./research/hbm-supplier-research-original-rules.md) with [`research/search-logs/hbm-supplier-original-rules/`](./research/search-logs/hbm-supplier-original-rules/) | the same question under the earlier rules: the evidence found, why it could not name a supplier, the access gaps | outcome decided 2026-10-07 (D-141) |
| [`research/supplier-presentation.md`](./research/supplier-presentation.md) | how a reported supplier is shown on both pages | decided 2026-10-07 (D-148) |
| [`research/search-logs/policy-instruments/`](./research/search-logs/policy-instruments/) | the search plan and log for the first export-control records: the official texts retrieved, their hashes, what each states | records accepted 2026-10-08 |
| [`research/search-logs/policy-links/`](./research/search-logs/policy-links/) | the search plan and log for the first policy links: the texts re-retrieved and re-hashed, every record's name searched, each hit's reading, the later changes to each entry | links accepted 2026-10-13 |

## Quality and audits (`PROJECT-EVALUATION-FRAMEWORK.md` §11)

| Artifact | Status |
|---|---|
| [`quality/audit-history.md`](./quality/audit-history.md) | active: one row per audit |
| [`quality/human-reviews.md`](./quality/human-reviews.md) | active: the human's verdicts on claims, one entry per review (D-151) |
| [`architecture/milestone-audits/M0-audit.md`](./architecture/milestone-audits/M0-audit.md) | accepted 2026-09-29: M0 audit, process benchmark against `Eu-Digital-Policy`, maturity baseline |
| [`architecture/milestone-audits/M1-audit.md`](./architecture/milestone-audits/M1-audit.md) | accepted 2026-10-01: domain and evidence foundation |
| [`architecture/milestone-audits/M2-audit.md`](./architecture/milestone-audits/M2-audit.md) | accepted 2026-10-02 (D-109, D-110): canonical dataset and data architecture; its blocking finding remediated |
| [`architecture/milestone-audits/M3-audit.md`](./architecture/milestone-audits/M3-audit.md), [`M4-audit.md`](./architecture/milestone-audits/M4-audit.md) | accepted 2026-10-07 (D-140); M4 closed |
| [`architecture/milestone-audits/M5-audit.md`](./architecture/milestone-audits/M5-audit.md) | accepted 2026-10-14 (D-187): the policy layer (S17, S18) and S19; M5 closed |
| [`architecture/agent-audit.md`](./architecture/agent-audit.md) with [`quality/audit-evidence/agent-audit/`](./quality/audit-evidence/agent-audit/) | agent architecture audit (PEF §7): rulings accepted 2026-10-14 (D-180 to D-184) |
| [`research/content-audit.md`](./research/content-audit.md) with [`quality/audit-evidence/content-audit/`](./quality/audit-evidence/content-audit/) | content and evidence depth audit (PEF §6): findings ruled 2026-10-02 (D-111 to D-113); maturity accepted 2026-10-03 |
| [`architecture/analytical-audit.md`](./architecture/analytical-audit.md) with [`quality/audit-evidence/analytical-audit/`](./quality/audit-evidence/analytical-audit/) | analytical depth audit (PEF §8): verdicts decided 2026-10-07 (D-133 to D-138) |
| `research/content-review-log.md` | planned |
| `quality/evaluation-framework.md` | satisfied by the root `PROJECT-EVALUATION-FRAMEWORK.md` (not duplicated) |

Executable quality controls: the unit tests and Gate 0 run in CI, among them 28 planted data faults
(`tests/test_planted_faults.py`, D-176); [`../tests/regression/`](../tests/regression/README.md) holds the deliberate
breaks, run in parallel and selected by the files a change touches (D-177, D-178), and [`../tests/browser/`](../tests/browser/README.md) the browser QA scripts.
