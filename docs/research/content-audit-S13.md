# S13 Content and Evidence Depth Audit

**Status:** FINDINGS RULED (S13, 2026-10-02): the human ruled on every finding at H-3 (Part 7).
The maturity ratings (Part 8) stay proposed until the human accepts them. Every finding is the
Atlas's assessment (`INTERPRETATION`), never a new fact.
**Required by:** `SESSION-ROADMAP.md` S13 ("Sample claims and relationships and test whether the
content layer is stronger than the presentation layer"; gate: "No scaling until evidence
weaknesses are corrected or explicitly documented"); `PROJECT-EVALUATION-FRAMEWORK.md` (PEF) §6
(content and review audit), §3 (maturity); S13 prompt Part B §06, §07.
**Base:** `main` @ `bb3a9a6` (S12 and the S13 prompt merged); measured on the session branch at
`ed9a8f4` (H-0's status lines and the sample; no claim, source, edge or entity changed).
**Roles:** Verifier (the re-reads), Knowledge Architect (the findings and the blocking/debt split),
Data Auditor (the measurements). No role writes a verdict.

## Contents

- Part 1 — The sample and how it was drawn
- Part 2 — The human's own reading (H-2), before Claude's
- Part 3 — The re-reads: every sampled claim
- Part 4 — The edges, the drawn gap and the page
- Part 5 — Source quality, coverage and freshness exposure
- Part 6 — Findings: blocking or debt
- Part 7 — Rulings and remediation (filled after H-3)
- Part 8 — Maturity (PEF §3, §6) and the S13 gate

---

## Part 1 — The sample and how it was drawn

**The human's rule** (H-1, verbatim): "Page's 14 key claims + 20 drawn (Recommended)".

**The script:** [`sessions/reports/SESSION-13-sample/draw_sample.py`](../../sessions/reports/SESSION-13-sample/draw_sample.py),
standard library only; its output [`sample.json`](../../sessions/reports/SESSION-13-sample/sample.json)
records the SHA-256 of `data/claims.json` and `data/relationships.json`. Run twice: identical
output; `--check` passes.

1. **The weight-bearing set (14).** The six claims S12 handed over: the five the five edges cite,
   and the drawn gap's DERIVATION. The script asserts that the edges cite exactly the five. Then
   every input claim of a DERIVATION or INTERPRETATION in the set, transitively:

   | Claim | Type | Why it is in the set |
   |---|---|---|
   | `claim-h100-hbm-stacks` | FACT | edge: H100 incorporates HBM |
   | `claim-trainium2-hbm-capacity` | FACT | edge: Trainium2 incorporates HBM |
   | `claim-hbm-requires-3d-die-stacking` | DERIVATION | edge: HBM requires 3D die stacking (D-091) |
   | `claim-tsmc-fabricates-h100` | DERIVATION | the drawn gap (D-092) |
   | `claim-aws-designed-trainium2` | FACT | edge: Amazon designs Trainium2 (D-093) |
   | `claim-sk-hynix-operates-m16` | DERIVATION | edge: SK hynix operates M16 (D-099) |
   | `claim-ecp-hbm-definition` | ATTRIBUTION | input of D-091 |
   | `claim-atlas-3d-die-stacking-working-definition` | INTERPRETATION | input of D-091 |
   | `claim-atlas-high-bandwidth-memory-working-definition` | INTERPRETATION | input of D-091 |
   | `claim-h100-process-name` | FACT | input of the TSMC derivation |
   | `claim-sk-hynix-production-plants-icheon-cheongju` | FACT | input of D-099 |
   | `claim-sk-hynix-m16-completed-icheon` | FACT | input of D-099 |
   | `claim-sk-hynix-m16-fabrication-plant` | FACT | input of D-099 |
   | `claim-hir-3d-architecture-definition` | ATTRIBUTION | input of the 3D die stacking definition |

2. **The drawn set (20)** from the other 106 canonical claims, in proportion to type by largest
   remainder, ordered within each type by SHA-256 of `S13-content-audit:<claim ID>`: 9 FACT, 5
   ATTRIBUTION, 3 DERIVATION, 3 INTERPRETATION, 0 IMPLICATION (the pool holds one IMPLICATION;
   its exact share, 0.19, rounds to none). Both of that IMPLICATION's source-citing inputs were drawn
   (`claim-aws-availability-zone-data-centers`, `claim-nist-cloud-location-independence`), and both hold. The list is in `sample.json`.
3. **The edges:** the five canonical relationships, and the drawn gap.

**Limits of the sample.** 20 of 106 claims is a probe, not a survey. Zero defects in a sample of
18 readable claims is compatible with a defect rate up to about one in six across the rest
(the "rule of three": 3/18). The one IMPLICATION claim is not sampled. 27 more claims are shown on
the page (names, locations, ISO codes); 6 of them were drawn.

## Part 2 — The human's own reading (H-2), before Claude's

Claude sent three weight-bearing claims, each with its source link, locator, quoted anchor and
four questions (does the sentence say it; does the claim or the line drawn say more; can the
sentence be found again; is it the right kind of statement), before writing any assessment of
them: `claim-h100-hbm-stacks` (solid line), `claim-aws-designed-trainium2` (solid line),
`claim-tsmc-fabricates-h100` (dashed gap).

**The human's answer, verbatim:**

> Yes
> Yes
> Yes

**What it can and cannot tell** (`INTERPRETATION`). The answer has three lines for three claims,
so it reads most naturally as one overall "yes, it holds" per claim. It does not answer the four
questions one by one, and a literal "yes" to question 2 would mean "it says more than the
source", the opposite. Read as "each claim holds":

| Claim | The human | Claude (Part 3, 4) | Agree? |
|---|---|---|---|
| H100 incorporates HBM | holds | the claim and the line hold; the source labels its H100 specifications "preliminary", which neither the claim nor the page shows (F-3) | on the line yes; Claude adds a caveat |
| Amazon designs Trainium2 | holds | the claim holds; the line's "Amazon" is the Atlas's alias step from "Amazon Web Services, Inc. … an Amazon.com, Inc. company", drawn as "stated" without that note (F-4) | on the claim yes; Claude adds a page-level caveat |
| TSMC fabricates H100 (gap) | holds | holds as a DERIVATION, drawn as an inferred gap (Part 4) | yes |

So the first independent reading found nothing Claude did not, and did not record the reasoning
that would show whether the same questions were asked. DT-11 is **partly** closed: the human did
read before Claude's view; the reading's granularity is not enough to test agreement question by
question (debt DT-S13-10, F-11).

## Part 3 — The re-reads: every sampled claim

**Method** (Verifier). The 20 registered sources the sample cites were re-retrieved on 2026-10-02 at
23:10Z with plain `curl` over HTTPS (RA-1, RA-2). Text was extracted with
[`reread.py`](../../sessions/reports/SESSION-13-sample/reread.py) (PDF pages with `pypdf` 6.19.0 in a
scratch virtualenv, not a repository dependency); every anchor was searched for in that text, and the
sentence around it read. Results per citation, with the SHA-256 of the bytes read:
[`reread-result.json`](../../sessions/reports/SESSION-13-sample/reread-result.json).

**Retrieval** (`FACT`, measured):

- 17 of the 18 automated sources returned their registered bytes.
- `src-042` and `src-051` (the same NVIDIA blog URL) returned different bytes. Two later requests
  returned a third hash. The differences are a render-timing comment and cache-busting script
  versions; the stated dates (published 2022-03-22, modified 2025-07-22) are unchanged. Every anchor
  was found again (F-6).
- `src-031` (TSMC Form 20-F) and `src-038` (ISO OBP, TW) returned HTTP 403 challenge pages ("Just a
  moment..."). Both were registered by manual retrieval (RA-4); a plain request is refused, as at
  registration. Not bypassed (RA-2). Five citations are access gaps (F-7).

**Anchors** (`FACT`, measured): of 28 citations, 23 anchors were found exactly, each PDF anchor on
the page its locator names (13 of 13); 5 are the access gaps. None was found only with whitespace
ignored, and none was missing.

**Per claim.** "Wording" asks whether the statement exceeds the sentence read at the locator;
"Type/standing" whether the claim type and each citation's standing fit the matrix row of every
record citing it; "Fresh" whether a `time_sensitive` row has accepted evidence within 12 months of
verification (F-1); "Conflict" whether another source the Atlas holds contradicts it.

| Claim | Anchor | Wording | Type / standing | Fresh | Conflict | Finding |
|---|---|---|---|---|---|---|
| `claim-h100-hbm-stacks` | found (`src-051`, changed bytes) | holds: "NVIDIA states that …" reproduces both sentences | FACT, party; `rel:incorporates` (stable) | n/a | none held | F-3: the page labels H100 specs "preliminary … subject to change in the shipping products" (Table 3 note; Figure 18: "Memory data rates not finalized") |
| `claim-trainium2-hbm-capacity` | found (`src-043`, same bytes) | holds | FACT, party; `rel:incorporates` | n/a | none | F-9: the anchor is a table row; the same page says "Each Trainium2 chip consists of … 96 GiB of device memory", which with the row supports containment |
| `claim-aws-designed-trainium2` | found ×2 (`src-052`) | holds; keeps the AWS legal entity's name | FACT, party; `rel:designs` (stable); press release is *acceptable* for the row | n/a | none | F-4 (page level) |
| `claim-hbm-requires-3d-die-stacking` | — (inputs) | step follows: ECP defines HBM as vertically stacked DRAM dies connected by TSVs; HIR's 3D architecture is stacked active devices interconnected without the package | DERIVATION; inputs research reports, originator (`rel:requires` preferred) | n/a | none | F-8: the target's v1 scope is HBM stacking only, so the edge restates HBM's definition |
| `claim-tsmc-fabricates-h100` | — (input) | step is ER-1's: TSMC appears only in process names ("Using the TSMC 4N fabrication process enables H100…"; the GH100 die "is fabricated using the TSMC 4N process"; Table 3 "TSMC Manufacturing Process … 4N customized for NVIDIA") | DERIVATION, as ER-1 requires | not an edge: F-1 fails (2025-07-22), D-092 | none | holds as ruled |
| `claim-sk-hynix-operates-m16` | — (inputs) | step follows from the three inputs below; the filing does not list the 이천 plants one by one, and M16's continuity rests on no later change being listed | DERIVATION; `rel:operates` (time_sensitive), filing 2026-03-17 | yes, until 2027-03-17 | none | F-8 |
| `claim-ecp-hbm-definition` | found p.5 | holds | ATTRIBUTION, originator | n/a | none | — |
| `claim-atlas-3d-die-stacking-working-definition` | — | the choice follows its inputs | INTERPRETATION | n/a | — | — |
| `claim-atlas-high-bandwidth-memory-working-definition` | — | the choice follows its input | INTERPRETATION | n/a | — | — |
| `claim-h100-process-name` | found (`src-042`, changed bytes) | holds | FACT, party; `attr:product.vendor_process_name` | n/a | none | — |
| `claim-sk-hynix-production-plants-icheon-cheongju` | found (`src-047`) | holds ("경기도 이천시와 충청북도 청주시에 생산공장을 설치ㆍ가동하고 있습니다") | FACT, party | input only | none | — |
| `claim-sk-hynix-m16-completed-icheon` | found (`src-046`) | holds ("2021. 02 이천 신규 공장 M16 준공") | FACT, party | stable rows | none | — |
| `claim-sk-hynix-m16-fabrication-plant` | found (`src-049`) | holds | FACT, party | stable rows | none | — |
| `claim-hir-3d-architecture-definition` | found p.4 | holds | ATTRIBUTION, originator | n/a | none | — |
| `claim-asml-holding-nv-company` | found p.76 | holds | FACT, party; `identity:company`, `attr:company.legal_name` | yes (2026-02-25) | none | — |
| `claim-aws-availability-zone-data-centers` | found (`src-020`) | holds | FACT, party; input of the one IMPLICATION (`claim-cloud-compute-facility-often-undisclosed`) | n/a | none | — |
| `claim-asml-incorporated-netherlands` | found p.309 | holds | FACT, party | yes | none | — |
| `claim-tsmc-legal-name` | **access gap** ×4 (`src-031`, 403) | not re-read | FACT, party | yes (2026-04-16) | — | F-7 |
| `claim-micron-manassas-fab` | found p.48 (also p.56) | holds: "our fab in Manassas, Virginia" | FACT, party; facility identity (stable) | n/a | none | — |
| `claim-nvidia-incorporation-history` | found p.5 | holds | FACT, party | input only | none | — |
| `claim-asml-headquarters-veldhoven` | found p.327 | holds | FACT, party | yes | none | — |
| `claim-iso-3166-1-tw` | **access gap** (`src-038`, 403) | not re-read | FACT, originator | stable | — | F-7 |
| `claim-amazon-incorporation-state` | found p.12 | holds | FACT, party | input only | none | — |
| `claim-lbnl-gpu-definition` | found p.7 | holds | ATTRIBUTION, originator | n/a | none | — |
| `claim-sia-advanced-packaging-breadth` | found p.21 | holds | ATTRIBUTION, originator | n/a | CON-04 (definitional; preserved) | — |
| `claim-cset-sme-definition` | found p.67 | holds | ATTRIBUTION, originator | n/a | none | — |
| `claim-nist-cloud-location-independence` | found p.6 | holds | ATTRIBUTION, originator | n/a | none | — |
| `claim-lbnl-asic-definition` | found p.6 | holds (omits "due to their efficiency": narrower, not more) | ATTRIBUTION, originator | n/a | none | — |
| `claim-tsmc-incorporated-in-tw` | — (inputs) | step follows; the code is an identifier, the filing's name for the jurisdiction stays in its claim | DERIVATION | yes | none | — |
| `claim-micron-headquartered-in-us` | — | step follows (ISO 3166-2 prefix) | DERIVATION | yes, until 2026-10-03 | none | F-5 |
| `claim-nvidia-headquartered-in-us` | — | step follows | DERIVATION | yes | none | — |
| `claim-atlas-advanced-packaging-working-definition` | — | a choice; both breadths kept (CON-04) | INTERPRETATION | n/a | definitional, preserved | — |
| `claim-atlas-ai-asic-working-definition` | — | a choice; narrows to the AI accelerator | INTERPRETATION | n/a | none | — |
| `claim-atlas-ai-accelerator-working-definition` | — | a choice (CON-01, preserved) | INTERPRETATION | n/a | definitional, preserved | — |

**Outcome of the re-reads** (`DERIVATION` from the table): of 34 sampled claims, 32 could be judged
(2 access gaps). In none does the statement exceed its sentence, none has the wrong claim type,
and no source the Atlas holds contradicts any of them. No claim needs `partial`, `context_only` or
`disputed`. The weaknesses found are in what the page shows (F-1, F-3, F-4), in records that are
not claims (F-1, F-2), and in the evidence system around the claims (F-5 to F-7).

## Part 4 — The edges, the drawn gap and the page

**Does the evidence state each relation as strongly as the page draws it?**

| Mark on the page | Drawn as | Evidence | Verdict |
|---|---|---|---|
| NVIDIA H100 incorporates HBM | solid, stated | NVIDIA's sentences on the H100's HBM3 and HBM2e stacks | as strong as drawn; the figures carry a "preliminary" note the page does not show (F-3) |
| AWS Trainium2 incorporates HBM | solid, stated | the HBM capacity row; "consists of … device memory" on the same page | as strong as drawn (F-9 on the anchor) |
| Amazon designs AWS Trainium2 | solid, stated | AWS, Inc. ("an Amazon.com, Inc. company") on "AWS-designed chip families" | the source states design by AWS, Inc.; drawing it from the parent's record is the Atlas's alias step (D-074, D-093), not shown on the page (F-4) |
| HBM requires 3D die stacking | inferred | D-091's DERIVATION | as drawn; it adds little beyond the definition (F-8) |
| SK hynix operates M16 | inferred, in the lane | D-099's DERIVATION | as drawn |
| TSMC → NVIDIA H100, fabricates | dashed gap, inferred | ER-1 DERIVATION; F-1 fails | as drawn; the reasons shown are the records' |

**Does any sentence, lane, legend or card remove a caveat the records carry?**

- **The short answer** ("NVIDIA H100 and AWS Trainium2 each incorporates High Bandwidth Memory
  (stated), which requires 3D die stacking (inferred). Who makes that memory: not researched in
  each.") keeps each mark's basis and the `not_researched` state, which the page defines as "Says
  nothing about whether the value is public." No caveat removed.
- **The lane framing** says "A missing line means the Atlas has not recorded a relationship; it
  never means that no relationship exists." No caveat removed.
- **The card "SK hynix, Micron Technology → NVIDIA · supplies · item: memory"** (`cand-002`)
  shows two firms. The sentence it refuses names three: "We purchase memory from SK Hynix Inc.,
  Micron Technology, Inc., and Samsung" (`src-024` p.8, re-read; its quote is in the record).
  On a page whose question is "who is known to make it", the card drops a firm the source names
  (F-1).
- **"What each maker states about the memory"** shows the H100 figures without the source's
  "preliminary" note (F-3).
- **The "Amazon designs" panel** shows the quote naming AWS, Inc., so a careful reader can see
  the legal entity; nothing on the page says that "Amazon" here is the Atlas's alias decision (F-4).

## Part 5 — Source quality, coverage and freshness exposure

Measured on `data/` at `ed9a8f4` (`FACT`); readings `INTERPRETATION`.

- **Classes of the 99 citations** on the 85 claims that cite sources: company filing 49, research
  report 10, standard specification 10, company technical documentation 8, policy research brief
  7, government publication 6, company press release 4, company marketing 3, industry association
  2. Company-published: 64 of 99. Company marketing: 3 citations, on 3 claims, each its only
  source: `claim-asml-euv-unique-to-asml` (ATTRIBUTION, ER-5), `claim-micron-hbm4-identity` (FACT;
  `identity:product` prefers marketing), `claim-sk-hynix-chiplet-description` (ATTRIBUTION).
  Marketing carries little weight.
- **Standing:** 63 party citations, 35 originator, 1 reporter.
- **Corroboration** (ER-7): no claim cites two publishers. Every claim rests on one voice. For a
  party's statement about itself this is the policy's design (the party is first-hand), but it
  means no value in the Atlas is corroborated, and S14 must not present any as such.
- **DT-10, publisher not linked** (F-2): 23 sources have `publisher_entity` `not_researched`; 10
  of them are cited, by 14 of the 63 party citations. Among them are four of the five edges'
  claims (`src-051`, `src-043`, `src-052`) and the M16 release (`src-049`). For those citations,
  "party" is asserted by hand: no check can test that the publisher is the party.
- **Bytes changed since registration** (sampled sources only): `src-042`/`src-051`, every
  request (F-6). The other 31 registered sources were not re-retrieved (no claim of theirs is
  sampled).
- **Freshness exposure** (PEF §6): 35 values on `time_sensitive` rows (34 company attributes and
  one edge). Each value's newest accepted evidence, and when it turns 12 months old:

  | Records | Evidence | 12 months on |
  |---|---|---|
  | Micron: legal name, incorporation, headquarters, roles | 10-K signed 2025-10-03 | **2026-10-03** |
  | Synopsys: the same four | 10-K, 2025-12-19 | 2026-12-19 |
  | Amazon: the same four | 10-K, 2026-02-05 | 2027-02-05 |
  | Amkor: the same four | 10-K, 2026-02-20 | 2027-02-20 |
  | NVIDIA, ASML: the same four each | 2026-02-25 | 2027-02-25 |
  | SK hynix: legal name, headquarters, roles; the M16 `operates` edge | 2026-03-17 | 2027-03-17 |
  | TSMC: legal name, incorporation, headquarters, roles | 20-F, 2026-04-16 | 2027-04-16 |

  F-1 measures age at each claim's **verification**, by design ("re-reading an old document does
  not make its content newer"), so none of these will ever fail a check unless re-verified. Nothing
  reports when a value passes the horizon in place (F-5).

## Part 6 — Findings: blocking or debt

Each finding is `INTERPRETATION`. "Blocking" means fixed before S14, with the human's ruling;
"debt" means documented with an owner. The recommendation is Claude's; the ruling is the human's
(Part 7).

| ID | Finding | Evidence | Recommended |
|---|---|---|---|
| **F-1** | **The page drops a memory supplier NVIDIA names.** `cand-002` and its card name SK hynix and Micron; NVIDIA's sentence, quoted in the record itself, names SK hynix, Micron and Samsung. The record narrows the source; nothing checks a refused candidate's parties against its own quote | `src-024` p.8, re-read (hash = registered); `data/refused_candidates.json` `cand-002`; the page's card | **blocking**: add Samsung to `cand-002` as a party with no record (as `cand-004` does for Zeiss), with the reason "a party has no record"; rebuild the page (D-111) |
| F-2 | **"Party" standing is unchecked on 14 citations** (DT-10, inherited): their sources' publisher is not linked to a company record | Part 5 | debt; DT-10 re-owned: linking a web publisher to a company needs a rule for what proves who publishes a page (a filing names its filer; a blog does not), and the AWS sources wait on DT-6 (D-113) |
| F-3 | **The H100 figures come from a launch-time blog that calls its H100 specifications preliminary**; the claim and the page show the figures without that note. The edge (the H100 contains HBM) does not rest on the figures | `src-051`: Table 3 note "Preliminary specifications for H100 based on current expectations and are subject to change in the shipping products"; Figure 18 note | debt: the claim stays (it reports what NVIDIA states, accurately); S14 must not compute over the H100 capacity figures, and a current product source replaces the blog when product attributes are next researched (D-112) |
| F-4 | **"Amazon designs Trainium2" is drawn "stated" from the parent's record, while the source names the subsidiary AWS, Inc.**; the alias step (D-074, D-093) is not shown on the page | `src-052`; D-093; DT-6 | debt, under DT-6: showing it on the page needs a place in the data for an edge's ruling (a model change, outside S13); fixed when the AWS record question is settled |
| F-5 | **Evidence ages past the horizon without any check noticing.** Micron's four values cross it on 2026-10-03 | Part 5; `tests/test_freshness.py` docstring | debt: a report (not a test, which would make CI depend on the clock) listing values past the horizon, owned by S01's weekly gate / the Change Detector; before S14's first query that presents a value as current |
| F-6 | **The NVIDIA blog's bytes change on every request** while its text does not, so "same bytes as registered" can never hold for it and a byte change is no signal there | Part 3 | debt: record a hash of the extracted text beside the byte hash for dynamic pages (Data Auditor), before the next re-read of an HTML source |
| F-7 | **Two manually supplied sources cannot be re-read automatically** (TSMC 20-F, ISO OBP TW: HTTP 403 challenge); `claim-tsmc-legal-name` and `claim-iso-3166-1-tw`, both on the page, were last re-read at their verification (2026-10-01/02) | `reread-result.json` | debt: an access gap, re-read from a file the human supplies (RA-4) when either claim is next relied on for a new record |
| F-8 | **Two inferred edges carry little independent weight:** "HBM requires 3D die stacking" restates HBM's definition (the 3D die stacking record covers HBM stacking only in v1), and "SK hynix operates M16" relies on M16's continuity from the absence of a later change | Part 3 | debt: S14 must not count D-091 as independent evidence of a dependency, and must show D-099's date of evidence |
| F-9 | **The Trainium2 edge's anchor is a table row** ("HBM Capacity (GiB) 32 96 3x"); a containment sentence on the same page ("consists of … 96 GiB of device memory") is not cited | `src-043` | debt: cite the sentence when the claim is next revised (Extractor; a new claim ID) |
| F-10 | **`cand-003` quotes NVIDIA's foundry sentence with an ellipsis that removes Samsung**, the other foundry it names ("We utilize foundries, such as … TSMC … to produce"). The refusal is about TSMC alone, and the card is not on the page | `src-024` p.8 | debt: no change; a refused candidate's quote should not drop a named party (checked by hand in S13) |
| F-11 | **The human's first independent reading was too brief to compare question by question** ("Yes / Yes / Yes") | Part 2 | debt DT-11 narrowed: future readings ask for one answer per question |

**Not findings** (checked, nothing wrong): every sampled anchor found where its locator says; no
overreach; no wrong claim type; no contradiction between two sources the Atlas holds (so no stop
condition); the short answer, the lane framing and the gap reasons keep their caveats; D-091,
D-099 and the TSMC derivation follow from their inputs as stated; marketing evidence is marginal.

## Part 7 — Rulings and remediation

**The human's rulings at H-3** (verbatim; each question as asked):

| Question | Answer | Effect |
|---|---|---|
| NVIDIA's 10-K says it buys memory from SK hynix, Micron and Samsung, but the page's card (a relation the Atlas refused to draw) lists only SK hynix and Micron. Should the card name all three firms before the SQL session? | "Card names all three firms (Recommended)" | F-1 blocking, remediated (D-111) |
| The H100 memory figures (80 GB of HBM3, five stacks) come from NVIDIA's 2022 launch blog, which labels its H100 specifications 'preliminary, subject to change'. What should happen to that claim? | "Claim stays, caveat logged (Recommended)" | F-3 debt (D-112) |
| Should the other nine weaknesses (findings 2 and 4 to 11 …) be recorded as known weaknesses, each with an owner and a deadline, with no data change now? | "Record all nine with owners (Recommended)" | F-2, F-4 to F-11 debt (D-113) |

Every ruling again followed the recommendation (P-3); the human's own reading came first (Part 2).

**Remediation of F-1** (D-111). `data/refused_candidates.json`, `cand-002` only:

- `source_entities` gains `{"state": "no_record", "name": "Samsung"}`, the word the quoted sentence
  uses;
- `reasons` gains `endpoint_has_no_record` (RC-5 requires it for a party with no record);
- `reasoning` gains "Samsung, the third firm the sentence names, has no company record (D-111)";
- the ruling stays D-089; the quote, locator and `read` are unchanged (the sentence was re-read in
  S13, in bytes equal to the registered ones).

No claim, source, edge or entity record changed; no Samsung record was created. The page was
rebuilt: the card reads "SK hynix, Micron Technology, Samsung (no record in the Atlas) → NVIDIA ·
supplies · item: memory" under both "endpoint has no record" and "item has no record", and D-111
joins the rules cited. Checks, breaks and browser QA: `SESSION-13-REPORT.md`.

**No check was added.** The missing check is "a refused candidate names every party its quote
names"; telling which words of a sentence are firms needs a reader, not a pattern. It stays a
Verifier's reading (F-10's debt covers the same gap).

**Debt register** (D-112, D-113):

| ID | From | What | Owner | Due |
|---|---|---|---|---|
| DT-S13-1 | F-2 | `party` standing unchecked on 14 citations; DT-10 re-owned | Knowledge Architect (a rule for who publishes a web page; AWS sources with DT-6) | before client output relies on standing (M6) |
| DT-S13-2 | F-3 | H100 figures from a source that calls them preliminary | S14 (no computation over them); the session that next researches product attributes (a current source) | S14 |
| DT-S13-3 | F-4 | "Amazon designs" drawn from the parent's record; alias not shown | DT-6's owner (the session that creates the AWS record) | with DT-6 |
| DT-S13-4 | F-5 | evidence ageing past the horizon is unreported (Micron: 2026-10-03) | S01's weekly gate / Change Detector: a report, not a clock-reading test | before S14 presents any value as current |
| DT-S13-5 | F-6 | dynamic HTML bytes change on every request | Data Auditor: a text hash beside the byte hash | before the next re-read of an HTML source |
| DT-S13-6 | F-7 | TSMC 20-F and ISO OBP refuse automated re-reads | Verifier, with the human's file (RA-4) | when either claim next supports a new record |
| DT-S13-7 | F-8 | D-091 restates a definition; D-099 rests on continuity | S14: not counted as independent evidence; D-099's evidence date shown | S14 |
| DT-S13-8 | F-9 | Trainium2 edge anchored on a table row | Extractor (a new claim ID citing the "consists of" sentence) | when the claim is next revised |
| DT-S13-9 | F-10 | a refused candidate's quote may elide a named party (`cand-003`) | Verifier, by reading | every candidate review |
| DT-S13-10 | F-11 | the human's reading too brief to compare | each session prompt asks one answer per question | next human reading |

## Part 8 — Maturity (PEF §3, §6) and the S13 gate

Ratings are `INTERPRETATION` on the evidence cited.

| PEF §6 | Rating | Evidence |
|---|---|---|
| Process: discovery and qualification | 3 | a matrix row for every field; class and standing per citation; access gaps recorded, never bypassed (Part 3) |
| Process: extraction and verification | 3 | every sampled anchor found at its locator; hashes per read. Held back: the checks are floors (S12 S10-1), and refused-candidate parties are not checked against their quotes (F-1) |
| Process: contradiction handling | 3 | CON-01 to CON-05 preserved; no contradiction found to handle |
| Process: stale-source replacement | 2 | F-1 is defined and tested at verification; ageing in place is unreported (F-5) |
| Process: editorial and interpretation review | 2 | the page keeps its caveats except F-1, F-3, F-4; review still follows recommendations (F-11) |
| **Process overall** | **3** (unchanged from M2) | |
| Outcome: accuracy of wording | 3 | 0 overreach in 32 judged claims |
| Outcome: locator quality | 3 | 23 of 23 readable anchors found, 13 of 13 PDF pages exact |
| Outcome: currency | 2 | all within the horizon today; Micron passes it on 2026-10-03 with no signal |
| Outcome: source quality | 2 | company-published 64 of 99; no corroborated value; publisher unlinked on 14 party citations |
| Outcome: depth | 2 | 5 edges; no supplier known for either accelerator's HBM; one first-hand voice per claim |
| **Outcome overall** | **2** (unchanged from M2) | the content is accurate where it speaks; it speaks about little, and from single voices |

**The content layer against the presentation layer** (the roadmap's question): the claims are as
strong as the page says, and the page is careful with gaps and inferences. The page is weaker than
its records in three places (F-1, F-3, F-4); the records are not weaker than the page anywhere.

**The S13 gate** ("No scaling until evidence weaknesses are corrected or explicitly documented"):
**met.** The one blocking finding (F-1) is corrected with the human's ruling; F-2 to F-11 are
documented debt with owners (Part 7). With S12's B-1 remediated, M3's blocking findings are all
remediated.
