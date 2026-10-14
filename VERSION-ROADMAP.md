# AI-Infrastructure-Atlas — Version Roadmap: v1.0, v1.5, v2

- **Status:** the three-version direction was decided by the human on 2026-10-14 (D-201). The session lists below
  are a **plan**, not a contract: each version's opening session re-plans from the repository as it then is, and
  its sessions enter `SESSION-ROADMAP.md` only on the human's approval at that point.
- **Scope of this document:** what each version is for, what it keeps from v1, what it must decide before work
  starts, and a provisional sequence of sessions. `SESSION-ROADMAP.md` stays the plan for v1.0 (S21 to S25) and is
  not changed by this document.
- **Claim label:** a plan (`INTERPRETATION`). Session counts are estimates [H], extrapolated from v1's observed pace
  (about eight data sessions produced 9 relationships, 174 claims and 61 sources) and the build/audit cadence of
  `SESSION-PROMPT-SPEC.md` §4.

## In short

| Version | Focus | Sessions (estimate) | Changes the rules? |
|---|---|---|---|
| **v1.0** | finish the planned path: client briefs, audits, release | S21 to S25 (5) | no |
| **v1.5** | **visual intelligence**: the S14.5 ambition built out — infographic layouts, an overview dashboard, reusable visual components, interaction, benchmark-quality design | S26 to S31 (about 6) | yes, decided at its opening: the no-script rule, hover, a chart layer or framework, browser checks in CI, one measured-data slice |
| **v2** | **coverage of the global AI infrastructure chain**, built with v1's method | S32 onward (about 30 to 35) | yes, decided at its opening: the frozen non-goals on coverage, energy, networking and EU classification; new record types; review capacity |

The method does not change between versions: canonical JSON records, claim-level provenance, the claim types,
explicit unknowns, one home per fact, reproducible derivations, generated pages, checks before changes, and the
human's review of evidence.

---

## 1. v1.0 — complete the path as planned (S21 to S25)

Unchanged from `SESSION-ROADMAP.md`:

| Session | Type | Mission |
|---|---|---|
| S21 | IMPLEMENTATION | client brief generator, on the stack decided by D-200 |
| S22 | AUDIT | code and engineering audit |
| S23 | AUDIT | research depth and content audit |
| S24 | AUDIT | portfolio and capability audit |
| S25 | SYNTHESIS / RELEASE | v1.0 synthesis and release |

**What v1 sessions carry forward for later versions** (no new scope):
- S21 builds briefs inside the current rules; it does not start v1.5's visual work.
- S22 already examines visual regression, responsive behaviour and chart binding. Its findings on browser checks
  outside CI and visual quality checked only by eye (S20's A-6 and A-7) become v1.5's first inputs.
- S25's "future research backlog" and "representative infographic set" are written with this document in view:
  the backlog feeds v2, and the infographic set is v1.5's baseline.

The v1.0 non-goals stay frozen until S25 (D-021). Nothing in v1.5 or v2 starts before v1.0 is released.

---

## 2. v1.5 — Visual intelligence

**Goal.** Realise what S14.5 set out (`docs/architecture/visual-architecture.md`): pages that read like
professional institutional and data-journalism products, measured against the benchmark it studied (Epoch AI,
Our World in Data, the IEA, the Stanford AI Index, Datawrapper; `docs/research/visual-benchmark.md`, D-122). Design
and visual communication are the focus. Coverage stays v1's.

**What stays fixed.** Every mark, number and word still traces to a record or a committed result. The S14.5
binding rule still applies (a page copies, tallies, takes a minimum and maximum or groups, and anything more is a
metric defined in SQL). Unknowns stay visible marks with words. The evidence and method layers stay reachable from
every visual.

**What v1.5 must decide at its opening (S26), each as a full decision request:**
1. **Whether pages may run a script**, and for what. Today U-8 allows none unless a question needs it. Hover
   tooltips, zoom, live filters and search all need one.
2. **Whether a value may appear on hover.** Today V-10 says nothing appears only on hover. Benchmark charts rely on
   it.
3. **Whether to add a chart library or a framework**, against D-200's conditions (a recorded reader question that
   needs the browser to hold state, and browser checks running in CI).
4. **How text drawn in the browser stays checkable.** Today the checks read the committed HTML. Interactive
   visuals need the same checks run on the rendered page, in CI.
5. **One measured-data slice inside the current scope.** Benchmark-style charts need numbers. The Atlas holds
   almost none about the world. Candidates within scope: HBM generations and products (bandwidth and capacity per
   stack, stack height, market dates) and the in-scope accelerators' memory figures, each from primary sources. This
   needs a record kind for a measured value with its unit and date (a schema decision). It adds measurements to
   records already in scope; it does not widen coverage.

**Provisional sessions:**

| Session | Type | Mission | Gate |
|---|---|---|---|
| S26 | ARCHITECTURE | v1.5 opening: refresh the visual benchmark against the current sites; record the reader questions that need interaction; decide items 1 to 5 above | every rule change decided and recorded before any code |
| S27 | IMPLEMENTATION | visual foundations: design system 2.0 (type scale, grid, colour roles for categories and sequences), reusable chart components generated from records (dot plot, bar, timeline, matrix, small multiples, indicator tiles), browser and visual-regression checks in CI | each component checked for provenance, accessibility and responsiveness; screenshots compared in CI |
| S28 | RESEARCH | the measured-data slice: HBM and accelerator figures from primary sources, with claims, verification and the human's review | every figure has a source, a locator, a unit and a date |
| S29 | IMPLEMENTATION | flagship infographics: an HBM figures chart, a redesigned dependency view, export-control matrix and timeline; one evidence page per claim (S20's A-4) | each passes the visual quality gate (MA §16.1) and the human's design review |
| S30 | IMPLEMENTATION | overview and interaction: an entry dashboard of the Atlas's questions, and the interactions S26 approved (filters with live counts, search if approved) | every interaction maps to a recorded reader question |
| S31 | AUDIT / RELEASE | v1.5 visual audit against the benchmark, then release | the human judges the result against the benchmark; every existing check still passes |

**Exit criterion.** A reader can compare an Atlas page side by side with a benchmark page and find it of comparable
clarity and polish, while every visual still opens its evidence.

---

## 3. v2 — Coverage of the global AI infrastructure chain

**Goal.** Extend the Atlas from one deep path (the HBM chain) to the global AI infrastructure chain, with v1's
method unchanged. Today the Atlas records 15 of the 40 first-version concepts of its own domain map
(`docs/research/domain-map.md`), and 5 of them carry a supply-chain link.

**What v2 must decide at its opening (S32), each as a full decision request:**
1. **The coverage non-goals:** NG-03 (no coverage beyond the first vertical), NG-04 (no networking records), NG-05
   (no energy records or links) and NG-06 (no EU/non-EU classification) (`docs/architecture/baseline.md` §6).
2. **The v2 domain map:** which layers, countries and actors are in scope, and in what order.
3. **New record types:** energy and network assets, materials, other chips; the schema changes and migrations they
   need.
4. **Review capacity.** Every canonical claim is reviewed by the human (D-182). At ten times today's volume this is
   the binding constraint; a sampling or tiered review policy needs a decision.
5. **Agent activation.** The Source Scout, Extractor and Change Detector work today as manual roles. At scale they
   need defined, governed workflows.
6. **Presentation at scale:** graph navigation and search across hundreds of records, built on v1.5's components.

**Provisional phases:**

| Phase | Content | Sessions (estimate) |
|---|---|---|
| A — open v2 | S32: the decisions above | 1 |
| B — finish the first chain | foundry, advanced packaging, equipment, cloud and data centres: research and dataset per layer, then an audit (no rule change needed: the current record and link types cover these layers) | about 10 |
| C — global policy | export controls and industrial policy of further jurisdictions (EU, China, Japan, South Korea, Taiwan, the Netherlands), on the policy model built in S17 to S19 | about 5 to 8 |
| D — new layers | energy, networking, materials, other chips (CPUs, FPGAs): schema, research, dataset, audit | about 8 to 12 |
| E — presentation at scale | graph navigation, search, per-layer and per-country views | about 3 to 4 |
| F — final audits and v2 release | engineering, research, portfolio audits; release | about 3 |

**Exit criterion.** Every layer of the v2 domain map has records and evidence-backed links, every gap is recorded
as a gap, and a reader can follow any dependency from AI compute to its suppliers, places and policies, with each
step traced to its sources.

---

## 4. How sessions use this document

- **v1 sessions (S21 to S25)** read it for direction only: they do not build v1.5 or v2 work and do not change the
  frozen non-goals.
- **S25** writes its backlog and infographic set with it in view.
- **Each version's opening session** (S26, S32) re-plans from the repository, asks the human for its opening
  decisions, and, on approval, adds its sessions to `SESSION-ROADMAP.md`.
- A change to the direction itself (the three versions, their focus, their order) is the human's, recorded as a
  decision.
