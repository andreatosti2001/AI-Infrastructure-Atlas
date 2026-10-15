# S23 Release Content Audit (research depth and content, before v1.0)

**Status:** PROPOSED. Findings and dispositions await the human's ruling (S23 H-2, Part 8). Every finding and rating
is the Atlas's assessment (`INTERPRETATION`) of the evidence shown beside it; counts are measured (`FACT`, L-04) and
labelled so.
**Required by:** `SESSION-ROADMAP.md` S23 ("Assess whether the project demonstrates real domain depth rather than
surface-level web research"; seven points to examine); `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §4 (the pre-release
dual audit; S22 covered the engineering half), §6 (content and review audit), §3 (maturity); `SESSION-PROMPT-SPEC.md`
§4 (an audit before v1.0).
**Base:** public `main` @ `741d683` (S22.5 merged), re-measured at the start: 196 claims, 64 sources, 9 relationships,
18 pages, staging empty, as the S23 prompt recorded. As-of date and "Searched to": 2026-10-15, S23's opening day
(D-215's window from 2026-10-16 was empty; the search tool refuses it before any request).
**Roles:** Verifier (retrievals and re-reads), Source Scout (the opposing-evidence searches), Knowledge Architect
(this document; the Portfolio Reviewer is inactive, D-184), Data Auditor (the measures). No role writes a verdict.
**Evidence:** [`../quality/audit-evidence/release-content-audit/`](../quality/audit-evidence/release-content-audit/);
the searches: [`search-logs/release-content-audit/search-log.md`](search-logs/release-content-audit/search-log.md).

## Contents

- Part 1 — The question, the sample and how it was drawn
- Part 2 — The re-reads
- Part 3 — The roadmap's seven points, measured
- Part 4 — PEF §6: the research process
- Part 5 — Findings
- Part 6 — The debt S23 inherits: dispositions
- Part 7 — Maturity (PEF §3) and the answer to the roadmap's question
- Part 8 — Rulings (filled after H-2)

---

## Part 1 — The question, the sample and how it was drawn

**The question** (roadmap S23): does the Atlas show real domain depth, or surface-level web research? S13 audited
the HBM page only (34 of 126 claims, 2026-10-02). Since then the Atlas added supplier research (S16.5, S16.6), the
policy layer (S17, S18), the journeys (S20), the client brief (S21) and the later-rule search (S21.5, S22); none of
it had a content audit.

**The rule** (approved by the human on 2026-10-15, H-0): every weight-bearing claim plus 30 drawn by type are read in
full; in addition, the anchor of **every** citation of every canonical claim is searched for in freshly retrieved
bytes. Script: [`draw_sample.py`](../quality/audit-evidence/release-content-audit/draw_sample.py) (standard library;
its output [`sample.json`](../quality/audit-evidence/release-content-audit/sample.json) records the SHA-256 of the
five files it read; run twice, identical; `--check` passes).

1. **Weight-bearing (59 claims, measured):** every claim a page result rests on, found mechanically: every claim ID in
   `data/relationships.json` (the five chain edges, their two supplier fields, the four `restricts` links; 21), in the
   dependency table's rows (`sql/results/accelerator_dependencies.json`: the drawn gap and each accelerator's class;
   4 more), in `data/events.json` (every derived status; 18 more), in the Change Detector's "Later statements about
   acts held" (1), then every input claim, transitively (15). By type: 23 FACT, 23 ATTRIBUTION, 7 DERIVATION,
   6 INTERPRETATION.
2. **Drawn (30 of the other 137):** in proportion to type by largest remainder, ordered within each type by SHA-256 of
   `S23-release-content-audit:<claim ID>`: 18 FACT, 6 ATTRIBUTION, 3 DERIVATION, 3 INTERPRETATION, 0 IMPLICATION (the
   pool holds one IMPLICATION; its exact share, 0.22, rounds to none).
3. **Every anchor:** all 203 citations of the 156 claims that cite a source (50 sources), not only the sample's.

**What the sample can and cannot show.** The 59 weight-bearing claims are a census, not a sample: what is said of them
holds for every claim a page result rests on. Of the 30 drawn, 27 could be judged (3 access gaps). Zero claims whose
wording exceeds their evidence among 27 judged is compatible with a rate up to about one in nine among the 137
unread claims (the "rule of three": 3/27). The anchor search has no sampling bound: it covers every citation, but
finding an anchor shows only that the quoted words are there, not that the claim's wording stays within them; that
judgement was made for the 89 sampled claims alone.

## Part 2 — The re-reads

**Method** (Verifier; H-1). The 50 cited sources were re-retrieved on 2026-10-15 from 20:2xZ with plain curl over
HTTPS, default client identity (RA-1, RA-2):
[`fetch.py`](../quality/audit-evidence/release-content-audit/fetch.py), log
[`retrieval-log.json`](../quality/audit-evidence/release-content-audit/retrieval-log.json) (host, time, status, size
and SHA-256 per request). Two requests failed at the TLS connection with no HTTP response (`www.asml.com`,
`englishdart.fss.or.kr`); each was repeated once, identically, and returned 200. Text was extracted by
[`reread.py`](../quality/audit-evidence/release-content-audit/reread.py): HTML with the standard library, PDF with the
machine's poppler `pdftotext` 24.02.0 (H-1: no repository dependency). Result per citation, with the hash of the bytes
and of the extracted text: [`reread-result.json`](../quality/audit-evidence/release-content-audit/reread-result.json);
verdict per sampled claim:
[`reread-outcomes.json`](../quality/audit-evidence/release-content-audit/reread-outcomes.json).

**Retrieval** (measured):

- 40 of 50 sources were read. **10 are access gaps:** the seven ISO Online Browsing Platform pages and TSMC's 20-F
  (Cloudflare challenge, HTTP 403; all eight were registered by manual retrieval, RA-4, as in S13), and **Amkor's two
  sources** (`src-026`, the 10-K; `src-050`, the Arizona release), refused by Akamai ("Access Denied", HTTP 403)
  although both were registered by automated retrieval on 2026-10-01 and 2026-10-02 (C-4). 25 of 203 citations
  (12 %) sit in these ten sources. Nothing was bypassed (RA-2).
- Of the 178 citations read, **161 are in bytes equal to the registered retrieval; 17 are not**, in 12 HTML sources
  (C-3). Every PDF returned its registered bytes.

**Anchors** (measured): of the 178 readable citations, **175 were found by the script** (all exact), **3 by hand at the
page their locator names**, each a PDF extraction artefact rather than a change in the text:
`claim-hir-2d-architecture-definition` (p.4, "side-by-side" broken at a line end and extracted as "side-byside"),
`claim-bis-rule-2023-23055-effective-2023-11-17` (p.1, DATES, interleaved with the next column),
`claim-bis-rule-2024-28270-revises-3b001-3b002` (p.15, the Federal Register page footer extracted inside the
sentence). **178 of 178 readable anchors found, every PDF anchor on the page its locator names** (152 of 152). None
is missing.

**The sampled claims** (89; the full list with notes is `reread-outcomes.json`):

| Outcome | Weight-bearing | Drawn | Meaning |
|---|---|---|---|
| holds | 45 | 21 | the anchors are found at their locators and the statement does not say more than the sentence around them |
| step follows | 13 | 6 | a DERIVATION or INTERPRETATION citing no source of its own: its reasoning follows from its inputs as stated |
| not retrievable | 1 | 3 | every citation is an access gap today: `claim-amkor-arizona-phase-2-announced` (`src-050`); `claim-iso-3166-1-us`, `claim-iso-3166-2-us-id` (ISO OBP); `claim-tsmc-incorporated-roc` (TSMC 20-F) |
| wording exceeds evidence | 0 | 0 | — |
| anchor not found | 0 | 0 | — |
| source changed so that the anchor no longer holds | 0 | 0 | — |

**Readings worth recording** (each `INTERPRETATION`):

- `claim-h100-hbm-stacks` holds; the source still says "Memory data rates not finalized and subject to change in the
  final product" (Figure 18 note), as S13 F-3 recorded. The page shows no figure computed from it (DT-S13-2).
- `claim-trendforce-h100-hbm3-primarily-sk-hynix-2024` holds; the same paragraph reports Samsung's entry "into
  NVIDIA's supply chain with its 1Znm HBM3 products in late 2023, though initially minor", not for the H100 by name.
  The claim's "primarily" keeps room for it, and the supplier field is historical (to 2024-03).
- `claim-semianalysis-trn2-hbm-samsung-2025` holds ("The speed deficiency was due to using memory supplied by
  Samsung"); the claim adds, correctly, that the source does not say Samsung was the only supplier.
- `claim-bis-rule-2024-28270-hbm-term-match` follows, and states on the page that the rule's HBM ("regardless of
  whether they conform to the JEDEC standards", p.11) and the Atlas's may differ at their edges (Part 6, row 6).
- The three ISO-based derivations drawn (`claim-amkor-incorporated-in-us`, `claim-micron-incorporated-in-us`,
  `claim-micron-manassas-fab-in-us`) follow from their inputs, two of which are ISO OBP access gaps today.

## Part 3 — The roadmap's seven points, measured

Measures: [`measure.py`](../quality/audit-evidence/release-content-audit/measure.py) →
[`measures.json`](../quality/audit-evidence/release-content-audit/measures.json) (standard library; it records the
SHA-256 of every file read; run twice, identical). Layers: a claim belongs to every layer whose records reach it,
directly or as an input.

| Layer | Claims | Citations | First-hand (party or originator) | Main classes (citations) |
|---|---|---|---|---|
| chain (products, components, technologies, identity bases, refused candidates, chain edges) | 55 | 37 | 37 of 37 | research report 9, policy research brief 7, company technical documentation 6, government publication 5 |
| suppliers (the two supplier fields) | 2 | 3 | 3 of 3 (originator) | market research consultancy 3 |
| companies and places | 65 | 63 | 63 of 63 | company filing 51, standard specification 10 |
| policy | 72 | 96 | 96 of 96 (originator) | official legal text 94 |
| reached by no record | 10 | 10 | 9 of 10 | company documents 6 |
| **all** | **196** | **203** | **202 of 203** | official legal text 96, company filing 52, research report 10, standard specification 10 |

### 1. Conceptual coverage

- **Measured:** of the domain map's 45 concepts (§2), **15 have a record**, 2 are recorded as gaps with a reason
  (HBM-03 base die, HBM-04 TSV: no definitional source of a sufficient class). By layer: accelerators 4 of 5,
  packaging 4 of 7, SME 3 of 6, data centres 2 of 6, EDA 1 of 3, HBM 1 of 6, **foundries 0 of 6, energy 0 of 6**. Of
  the map's 18 concept-level dependencies, **3 are realised by an edge** (DEP-01 accelerators use HBM, DEP-03 HBM
  needs stacking, DEP-15 a cloud provider designs its accelerator) and 1 is drawn as a gap (DEP-05, fabrication); the
  mapping is a reading by hand, listed in `measure.py`. Two accelerators, three products, two facilities, nine
  companies, seven policy instruments.
- **Reading:** the Atlas covers the slice it set out to cover (accelerator → HBM → stacking, and the export controls
  naming HBM and SME), and records the rest of the domain map as concepts without records. It is a vertical slice,
  as `CLAUDE.md` §10 asked; breadth is v2's (D-201).

### 2. Primary-source ratio

- **Measured:** 202 of 203 citations are first-hand by the source policy's definition (SP-3: the publisher is a party
  or the originator); one is `reporter` (LBNL reporting IDC analysts, recorded as a chain). The policy layer rests
  on 94 citations of the official Federal Register and CFR texts; the companies layer on 51 citations of the
  companies' own filings. **No claim rests on two independent publishers** (C-5): the eight claims citing two
  publishers combine the Federal Register and the CFR, two official publications of one government, for two halves
  of one statement. The supplier layer rests entirely on two market-research firms, one voice each, one of them
  with the recognition criterion declared unmet.
- **Reading:** "primary" here is a relation, not a class (SP-3), so the ratio is near-total by design: companies
  speak about themselves and official texts about their own content. That is the right kind of primary evidence for
  what the Atlas records. What it cannot give is independence: every value is one voice.

### 3. Claim verification

- **Measured:** Part 2. 178 of 178 readable anchors found at their locators; 0 of 85 judged sampled claims exceed
  their evidence; 0 wrong claim types; 25 citations (12 %) not re-readable by automated retrieval today. Every
  canonical claim carries the human's verdict (`human-reviews.md`, nine review sessions from 2026-10-01 to
  2026-10-15).
- **Reading:** the content is accurate where it speaks, and checkably so: a second reader with the same tools finds
  every quoted sentence where the record says it is.

### 4. Counterevidence

- **Measured:** five conflicts recorded and preserved (CON-01 to CON-05, all definitional, each with both sides kept
  as `ATTRIBUTION`); no `factual_contradiction`; 0 claims `disputed` or `partial`. S16.6's supplier search logged 40
  queries and recorded the one disagreement it met (DIGITIMES's 2023 plan, Samsung and SK hynix, against SemiAnalysis's
  2025 statement, Samsung) as "recorded, not resolved". S23's own searches for opposing evidence on the contestable
  weight-bearing claims (the two supplier fields and the AI Diffusion rule's status; search log) found **no
  contradiction**, re-found the DIGITIMES headline already recorded, and found **one opposing text bearing on a
  page's framing**: BIS's release of 12 May 2025 on the AI Diffusion rule (C-1).
- **Reading:** contradictions are looked for and kept, not silently settled. The one material opposing text the
  Atlas does not hold was known (a pointer, CD-7) and is now retrievable.

### 5. Temporal coverage

- **Measured:** sources by newest stated date: 2011 to 2022 9, 2023 7, 2024 5, 2025 12, 2026 14, undated 16 (the
  undated are web pages dated by their access, and the ISO pages). Every access date falls between 2026-09-29 and
  2026-10-15. Of the 38 current values on `time_sensitive` matrix rows, **34 rest on evidence within 12 months of the
  reference date (2026-10-15); 4 do not: Micron's legal name, incorporation, headquarters and role**, whose newest
  evidence is the 10-K signed 2025-10-03, 12 days past the horizon (C-2). The freshness check (F-1) passes, because
  it measures age at verification by design. The H100's product-level evidence is 450 days old (a gap, `cand-001`,
  E-1, and a stable `incorporates` row, which has no age limit). The policy layer's dates are the texts' own; texts
  after 2026-10-15 are unknown to the Atlas, and every page says so.
- **Reading:** the Atlas dates everything and never calls a value current (V-5). What it lacks is a report that
  tells a reader, or a session, when a value passes the horizon in place; S13 predicted Micron's date (DT-S13-4), and
  nothing noticed it.

### 6. Analytical sophistication

- **Measured:** 40 claims reason from others (22 DERIVATION, 17 INTERPRETATION, 1 IMPLICATION), each with written
  reasoning and no citation of its own; 34 of them use 2 to 4 inputs; the deepest chain is 3 steps. The derivations
  are of five kinds: a country read from an ISO code (14), a policy term matched to a record (4), a fabricator read
  from a process name (2, ER-1), facility operation from a filing's plant list (1, D-099), a necessity read out of a
  definition (1, D-091). The interpretations are the 16 working definitions and 1 classification (Trainium2 as an AI
  ASIC). Four SQL queries compute the dependency
  table, coverage, source ages and supplier metrics, each with question, population, denominator and "does not
  prove" (S16's analytical audit); the supplier metrics say "cannot be computed yet".
- **Reading:** the analysis is careful and inspectable, and deliberately modest: it adds definitions, joins and
  explicit gaps, rarely a conclusion. The single IMPLICATION (`claim-cloud-compute-facility-often-undisclosed`) is on
  no page. The Atlas's strongest analytical work is in what it refuses (21 refused candidates, each with a reason)
  and in how it bounds what its links mean (the term-match claims' "does not conclude" sentences).

### 7. Limitations

- **Measured:** 19 explicit states on records (7 `not_researched`, 12 `not_applicable`); 21 refused candidates (9
  "relation not stated", 6 "term not matched", 3 "endpoint has no record", 2 "evidence not fresh", 2 "company level
  only", 2 "item has no record", 1 "wrong relation type", 1 "applies a threshold"); every page carries framing blocks
  saying what a missing line, a status, a date and a supplier do not mean. **44 of 196 claims (22 %) are on no page**
  (C-7): 36 are the concept layer (13 of the 16 working definitions and 23 source definitions and descriptions
  behind them, including both sides of the CON conflicts); the other 8 include the IMPLICATION and claims no record
  reaches.
- **Reading:** the pages state their limits precisely. What a reader cannot see is the definitional research that
  bounds the Atlas's terms, outside HBM's.

## Part 4 — PEF §6: the research process

| Item | What the records show | Rating (Part 7) |
|---|---|---|
| Source discovery | five search logs with plans (`docs/research/search-logs/`); queries, results read and dispositions recorded; refused domains named (S16.6 Q-rows); the later-rule search is a tool with a log per run (D-211) | 3 |
| Source qualification | 12 classes, standing per citation, a 48-row preference matrix and ER-1 to ER-10, all machine-checked; third-party supplier criteria declared met or unmet (D-147) | 3 |
| Claim extraction | staging and candidates; 21 refusals with reasons; quotes verbatim with locators; no claim added without the human's verdict | 3 |
| Verification | hashes per read; this audit found 178 of 178 readable anchors; but the Verifier's re-read is still a per-session script (agent audit F-4) and access gaps grew by two sources since registration (C-4) | 3 |
| Contradiction handling | CON-01 to CON-05 preserved; DIGITIMES recorded as "recorded, not resolved"; no conflict settled by rank | 3 |
| Stale-source replacement | F-1 tested at verification; the chain's source ages flagged (D-129); no Atlas-wide report, so Micron's four values aged past the horizon unseen (C-2); the H100's stale evidence has stayed unreplaced since S10 (E-1); DT-S13-5's text hash never built (C-3) | 2 |
| Editorial revision | S13's page findings fixed (F-1) or framed; the supplier caveats ("one publisher only", "criterion not met") on every page; pages never say "current" | 3 |
| Interpretation review | every INTERPRETATION approved by the human with its reasoning (TQ answers, D-091, D-099); "does not conclude" sentences on every term match | 3 |

## Part 5 — Findings

**Blocking, for this audit** (the S23 prompt §06.4): a claim whose wording exceeds its evidence on a page; a stale value
presented as current; an anchor not found in its source. **None was found.** Every finding below is debt; the
proposed disposition is Claude's, the ruling is the human's (Part 8). "New research" means a new source or claim,
which the S23 prompt (§08) sends to a named later session unless H-2 brings it into S23.

| ID | Finding | Evidence | Rating | Proposed disposition |
|---|---|---|---|---|
| **C-1** | **The export-control page and the brief show the AI Diffusion rule as "has taken effect" without the issuing agency's own announcement that it initiated a rescission and does not enforce the rule.** The status is correct by its definition (an effective date recorded, no repeal recorded; framed on the page), and the July 2026 statement under the act cites the May 2025 guidance by its address. But BIS's own release is held only as an unread pointer, and the Atlas's model already has the place for it: an `announced` event, which `government_publication` may support, and which changes no status (`policy-dataset.md`; PL-7, "an announced rescission that changes nothing") | BIS release, 12 May 2025, retrieved 2026-10-15 (HTTP 200, hash in the search log): "initiated a rescission", "not to enforce", "plans to publish a Federal Register notice formalizing the rescission"; the page's act panel | debt, the most material content gap on a page | **record it before v1.0:** one source (`government_publication`), one `ATTRIBUTION` claim quoting the release, one `announced` event on `policy-us-fr-2025-00636`, through staging and the human's verdict; pages rebuilt. New research: the human decides whether S23 does it (H-2) |
| **C-2** | **Four of Micron's time-sensitive values passed the 12-month horizon on 2026-10-03 with no signal** (legal name, incorporation, headquarters, role; 10-K signed 2025-10-03). S13 named the date (F-5, DT-S13-4); the chain's source ages (D-129) do not cover company fields; the Atlas-wide report stayed with the Change Detector, whose contract covers only the later-rule search. The pages show the evidence's date and never say "current" (V-5), so no value is presented as current | `measures.json` 5; Micron's company page (evidence panel: "signed 2025-10-03"); D-129 | debt | **a measured report, no clock:** the source-age query (or a sibling) lists every `time_sensitive` value past the horizon at the reference date, and the company page states it beside the value (Analyst, Data Auditor; checks first). Refreshing Micron from its FY2026 10-K (filed on SEC EDGAR; a company-hosted copy not yet sought) is new research for a named session |
| **C-3** | **12 HTML sources return bytes different from their registration** (17 citations), while every anchor and every stated date is unchanged. DT-S13-5 asked for a hash of the extracted text beside the byte hash "before the next re-read of an HTML source"; it was never built, so the records cannot tell a changed text from a changed page template | `reread-result.json` (`equals_registered`: 17 false); stated dates read from the pages' metadata (S23 working files) | debt | **no schema change now:** this audit's text hashes (`text_sha256` per citation) are the baseline for the next re-read; the Verifier's re-read tool (agent audit F-4) records a text hash when it is built |
| **C-4** | **Access gaps grew: Amkor's 10-K and Arizona release now refuse automated retrieval** (Akamai 403), as the TSMC 20-F and ISO pages always did. 25 of 203 citations (12 %) can no longer be re-read without the human (RA-4) | `retrieval-log.json` | debt | recorded; re-read from a file the human supplies (RA-4) when a claim citing them is next relied on for a new record (S13 DT-S13-6 extended to `src-026`, `src-050`) |
| **C-5** | **No value in the Atlas rests on two independent publishers.** Every value is one voice; the supplier layer rests on two market-research firms (one with recognition unmet) | `measures.json` 2 | debt (structural; unchanged since S13) | kept as a stated limitation; the pages already say "one publisher only" per supplier row; corroboration is v2's research (D-201) |
| **C-6** | **The Atlas is deep in method and narrow in coverage:** 15 of 45 domain-map concepts recorded, 0 for foundries and energy; 3 of 18 concept-level dependencies realised by an edge; two accelerators | `measures.json` 1 | not a defect: the v1 scope (`CLAUDE.md` §10) | carried to S24 and S25 as the release's coverage statement; v2 (D-201) |
| **C-7** | **The concept layer is invisible to readers:** 44 claims (22 %) are on no page, among them 13 of the 16 working definitions and the CON-01 to CON-05 conflicts, the Atlas's most careful definitional research | `measures.json` 7 | debt | v1.5 (a page for the concepts and their conflicts); no page change in S23 |
| **C-8** | **Several content debts are owned by sessions that do not exist before v1.0:** "the next policy research session" (the EAR's dates, the May 2025 and May 2026 guidance, D-210), "the next supplier research" (a current H100 supplier, Trainium2's recognised source), the Change Detector's Atlas-wide ageing report, "the session that resolves `cand-001`" (E-1). The v1 roadmap holds only S24 (portfolio audit) and S25 (release) | D-210, D-213, `hbm-supplier-research.md` debt tables, `SESSION-ROADMAP.md` | debt (process) | the human decides: each listed in S25's known limitations with its gap, or a research session added before S25 |
| **C-9** | **PDF text extraction breaks three anchors** (a line-break hyphen, interleaved columns, a page footer) that a person finds at once | Part 2 | debt (method) | the Verifier's re-read tool (agent audit F-4) matches across these three artefacts before it reports "not found" |
| **C-10** | **The supplier fields' basis is thin and dated:** the H100's is historical (to 2024-03, 946 days old, one market-research voice); Trainium2's rests on one assessment whose recognition criterion is unmet; DIGITIMES's 2023 plan names a second maker | `source_age.json`; `hbm-supplier-research.md` | debt (unchanged since S16.6; shown on every page) | kept; owner per C-8 |

**Not findings** (checked, nothing wrong): no anchor missing; no overreach in 85 judged claims; no wrong claim type;
no contradiction between sources the Atlas holds; every PDF in its registered bytes; every PDF anchor on its locator's
page; the term-match claims state what they do not conclude; the pages keep each supplier's caveats and never claim
exclusivity ("A named or reported supplier is not the only supplier", research view); no access gap was bypassed.

## Part 6 — The debt S23 inherits: dispositions

| Row | Item | What the records show | Proposed disposition |
|---|---|---|---|
| 1 | **C-8 (S16): `src-043` carries two access dates for the same bytes** (retrieval 2026-10-01T20:44Z; `claim-trainium2-hbm-capacity`'s read 2026-10-02T16:00Z, same hash) | The schema defines two different events: `retrieval.accessed_at`, when the Atlas obtained the bytes the source record describes; `read.accessed_at`, when the Verifier read bytes for one citation ("When the hash differs from the source record's retrieval, the source changed"). Equal hashes mean the second read found the same bytes. The source-age query already dates an undated source by its retrieval | **no data change; wording only:** `claim-model.md` says which date is canonical for what (the source's retrieval dates an undated source; a citation's read records a re-read). Closes C-8 |
| 2 | **M5 §6: three rules' country joins two texts** | Five `*-issued-in-us` claims (FACT) quote the rule's AGENCY line ("Bureau of Industry and Security, Commerce") and the CFR's § 730.1 ("issued by the United States Department of Commerce, Bureau of Industry and Security"); `issued_in` reads the country from the second. Each half is a verbatim anchor (re-read: both found); the join is the identity of the bureau named in both. 2023-23049's claim names the U.S. Department of Commerce in one text | **no data change; wording only:** `policy-dataset.md` records that `issued_in` may rest on two official texts when the rule's own text names the bureau without its country, and that the join is the bureau's identity, read from the texts, not inferred. Reclassifying the five claims as DERIVATION (a data change) is the alternative |
| 3 | **M5 §6: an official text's publisher is an edition's name** | The eight `official_legal_text` sources give `publisher` as "Federal Register (official edition, govinfo.gov)" or "Code of Federal Regulations, annual edition (govinfo.gov)": the edition and its host, not the body that publishes it (the Office of the Federal Register with the Government Publishing Office). The issuing authority is a separate, sourced field (`issuing_authority`) | **no data change; wording only:** `policy-dataset.md` states the convention (for an official legal text, `publisher` names the official edition and its host; the authority is `issuing_authority`). Renaming the publisher of eight sources (a data change, pages rebuilt) is the alternative |
| 4 | **`not_researched`'s definition ("No source has been checked for this value yet") disagrees with ER-3's use after a partial search** | A live case: SK hynix's `incorporated_in` is `not_researched` although its annual report was read (`company-dataset.md` §4: no sentence names the country). No page prints the definition | **a wording change in the vocabulary's description** (`schemas/entities.schema.json`, no validation change): "No research has established this value: no source has been checked, or a search did not cover every preferred class (source-policy.md ER-3). Says nothing about whether the value is public." Needs its own decision; a schema file changes, so the full break harness runs |
| 5 | **The ID rule's legal-form list lacks "Co., Ltd.", so Samsung's ID keeps it** | ID-1 recomputes each company ID from its legal name and the list; adding "Co., Ltd." now would make ID-1 require `company-samsung-electronics`, an ID migration across records and pages, against the rule that IDs are stable | **no list change; wording only:** `company-dataset.md` §3 records why `company-samsung-electronics-co-ltd` keeps "co-ltd" (the designation was not listed when the record was first made, and IDs never change), and that the designation is added, with an ID-1 exception for existing records, only by a decision when the next record needs it |
| 6 | **E-1: the H100's fabrication evidence** (`cand-001`, refused as `evidence_not_fresh`, D-092) | Re-read: NVIDIA's blog still names "TSMC 4N" (modified 2025-07-22, 450 days before the reference date); no fresh product-level statement is held; S22.5's regression test stops the builds by name if `cand-001` is resolved | **kept**, owner per C-8 (a session that retrieves a fresh product-level statement); no new research in S23 |
| 7 | **"The working definition of HBM"** (M6 §8) | Traced to M5-audit §6: "The 2024 rule's HBM wider than the working definition (stated in the claim) — S22 may revisit the working definition". The term-match claim states the difference on the export-control page and the brief (p.11, JEDEC; co-packaged logic), and its link "does not carry either edge" | **closed, no change:** the working definition is the human's choice (TQ, class C) and the difference is stated where a reader meets it; revisiting the definition is not needed for any page or link |
| 8 | **The EAR's dates; texts after the as-of date; the May 2025 and May 2026 BIS guidance as pointers** | The search to 2026-10-15 is complete (JR-13); the May 2025 release is retrievable today (C-1); the May 2026 guidance's printed address returns 404; the EAR's 1996 reissue is still unretrieved | the May 2025 release per C-1; the rest kept, owner per C-8 |

## Part 7 — Maturity (PEF §3) and the answer to the roadmap's question

Ratings are `INTERPRETATION` on the evidence cited. S13 rated the content dimension 3 for process and 2 for outcome.

| PEF §6 | Rating | Evidence |
|---|---|---|
| Process: discovery and qualification | 3 | Part 4; five logged searches; every refused domain and access gap named |
| Process: extraction and verification | 3 | 178 of 178 anchors; hashes per read; held back by the per-session re-read script (F-4) and C-9 |
| Process: contradiction handling | 3 | CON-01 to CON-05; DIGITIMES recorded, not resolved |
| Process: stale-source replacement | 2 | C-2, C-3, E-1: ageing in place still unreported; the H100's only product-level evidence (2025-07-22) not replaced |
| Process: editorial and interpretation review | 3 | every interpretation human-approved; page caveats kept |
| **Process overall** | **3** (unchanged since S13) | controlled and repeatable, except for evidence ageing |
| Outcome: accuracy of wording | 3 | 0 overreach in 85 judged claims (59 of 59 weight-bearing judged or step-checked, one access gap) |
| Outcome: locator quality | 3 | 178 of 178 readable anchors at their locators; 12 % of citations not re-readable without the human |
| Outcome: currency | 2 | 4 of 38 time-sensitive values past the horizon unflagged; C-1's announcement missing from the page |
| Outcome: source quality | 2 | first-hand nearly everywhere and official texts for the policy layer, but no corroborated value and the supplier layer on single market-research voices |
| Outcome: depth | 2 | 15 of 45 concepts, 3 of 18 dependencies, two accelerators |
| **Outcome overall** | **2** (unchanged since S13) | accurate, checkable and honest about its gaps; narrow and single-voiced |

**The roadmap's question** (`INTERPRETATION`): **the Atlas does not read as surface-level web research.** Its claims
quote official texts and the companies' own filings at exact locators that a second reader finds again (178 of 178);
it keeps conflicts instead of settling them, refuses what its evidence does not state (21 refusals) and says what each
link does not mean. Its depth is of **method**, not of **coverage**: one slice of the chain, two accelerators, and
values that rest on one voice each. The release can claim evidence discipline and reproducibility; it cannot claim
breadth, corroboration or currency beyond the dates it shows.

## Part 8 — Rulings (filled after H-2)

Pending.
