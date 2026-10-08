# Who supplies the HBM in the H100 and in Trainium2? (S16.6 research findings)

**Status:** findings written 2026-10-07; the outcome for each part decided by the human on 2026-10-07 (H-2).
Every statement below says what a retrieved source states, or what the Atlas concludes from the rules
(`INTERPRETATION`). Nothing here is a new fact about the world beyond what the cited sources state.

**Read with:** S16.5's findings ([`hbm-supplier-research-original-rules.md`](hbm-supplier-research-original-rules.md)), which
stand for the parties' own statements; the rules decided at S16.6's opening (D-144 to D-147,
[`supplier-evidence-rules.md`](supplier-evidence-rules.md)).

**Method:**

- the search plan ([`plan.md`](search-logs/hbm-supplier/plan.md)) was written before any
  search, under the decided rules;
- the Source Scout ran it and logged 40 queries and 35 retrieval attempts (T-01 to T-35,
  [`search-log.md`](search-logs/hbm-supplier/search-log.md)). Search results only found
  URLs; no snippet is evidence;
- the Verifier (Claude) re-read the two decisive anchors in the retrieved bytes and recorded each third-party
  citation's §7.1 criteria (`recognised`, `independent`, each met or not, with the reason);
- retrieved bytes stay outside the repository. The source records keep each URL, hash and access time.

**What the new rules admit** (`source-policy.md` §7.1, §12):

- a third party (teardown lab, market research, news) may support a product's supplier when it is
  recognised as reliable and independent of the parties, with any unmet criterion stated (D-147);
- evidence older than 12 months supports only a **historical** value, ending at a stated date (D-144);
- a value resting only on third parties is shown as **reported**, never as stated (D-147, D-148).

## The NVIDIA H100

| What was found | Source | Criteria (§7.1) | Date | Outcome |
|---|---|---|---|---|
| "The current HBM3 supply for NVIDIA's H100 solution is primarily met by SK hynix" | TrendForce press release (T-15, `src-054`) | recognised: met; independent: met (no sponsor or tie stated; ownership not researched) | 2024-03-13 | **canonical, historical:** supplier SK hynix, reported, to 2024-03 (claim `claim-trendforce-h100-hbm3-primarily-sk-hynix-2024`) |
| the same sentence, repeated | TrendForce news (T-18) | same publisher, not a second voice (ER-7) | 2024-06-03 | not recorded |
| SK hynix "supplied" HBM3 "to NVIDIA" | SK hynix pages (T-29, T-30) | party | 2022-12-29; undated | company-level, not the H100 (ER-9) |
| HBM3 makers and H100 "SKUs" | SemiAnalysis (T-28); TrendForce (T-17) | — | 2023 | the maker-to-H100 link is not stated, or grammatically open |
| teardowns of the H100 | TechInsights (T-05 to T-07) | recognised | 2023 | **access gap:** the public pages name no memory maker |
| an SK hynix HBM3 package in a teardown | TechInsights (T-03) | recognised | undated | another product (Grace Hopper Superchip), not the H100 |

**What the rules conclude** (`INTERPRETATION`):

- TrendForce's 2024 sentence is product-level and worded as a present state in its day, not a plan (ER-8);
- it is older than 12 months, so it supports only a historical value (D-144). Its period ends at its own date,
  2024-03; nothing is said about later dates;
- "primarily" is not "only": the supplier metrics do not count it as single-sourcing (D-148);
- **no current supplier is established.** No source dated on or after 2025-10-07 names the H100's HBM maker.

## AWS Trainium2

| What was found | Source | Criteria (§7.1) | Date | Outcome |
|---|---|---|---|---|
| "the 5.7Gbps pin speed that was used in Trn2 …"; "The speed deficiency was due to using memory supplied by Samsung" | SemiAnalysis, "AWS Trainium3 Deep Dive", free part (T-19, `src-055`) | recognised: **not met** (no evidence found that parties, governments or intergovernmental bodies routinely cite it); independent: met (no sponsor or tie stated; the firm sells research and consulting to the industry) | 2025-12-04 | **canonical, current, with the unmet criterion shown:** supplier Samsung Electronics, reported (claim `claim-semianalysis-trn2-hbm-samsung-2025`) |
| "Samsung and SK Hynix will both supply HBM3 for AWS Trainium 2" | DIGITIMES headline (T-21) | — | 2023-12-07 | a plan (ER-8), body paywalled: not recorded |
| no party statement naming Trainium2's memory maker | AWS, SK hynix, Samsung, Micron (S16.5 and Q33 to Q36) | party | — | — |
| no teardown of a Trainium2 unit | any query | — | — | — |

**What the rules conclude** (`INTERPRETATION`):

- SemiAnalysis's sentence is recent and product-level by its paragraph's subject (Trn2), worded as past fact;
- it names no source and does not say Samsung was the only supplier. It contains a comparative judgement of
  Samsung's memory, which the claim does not carry (ER-5);
- the human approved it with the recognition criterion declared unmet (H-2). Every page shows "criterion not
  met: recognised" beside it;
- it disagrees in form with DIGITIMES's 2023 plan (Samsung and SK hynix "will both supply"). Neither text
  excludes the other: recorded, not resolved.

**A new company record.** Samsung Electronics had no record. It was created from its 2025 Business Report
(`src-056`, company-hosted): legal name, head office, country (derived), memory products. Its ID,
`company-samsung-electronics-co-ltd`, keeps "co-ltd" because the ID rule's list of legal forms does not hold
"Co., Ltd." (debt, below).

## Debt and next checks

| Item | Owner |
|---|---|
| The ID rule's legal-form list lacks "Co., Ltd.", so Samsung's ID keeps it | the next schema session (S22 engineering audit) |
| SemiAnalysis's recognition is unmet: a recognised source naming Trainium2's HBM maker would replace or confirm it | the next supplier research |
| TechInsights's H100 teardowns are paid: a reader with legitimate access could settle the H100 at product level (RA-4 needs the human) | the human, if access exists |
| Reuters, FT, WSJ and AP could not be searched (the search tool refused their domains) | the next supplier research, with another discovery route |
| No current H100 supplier: a fresh product-level statement would add one beside the historical value | Change Detector (inactive); the next supplier research |
