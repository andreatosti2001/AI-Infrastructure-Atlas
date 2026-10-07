# Who supplies the HBM in the H100 and in Trainium2? (S16.5 research findings)

**Status:** findings written 2026-10-07. Nothing is canonical yet; the outcome for each part awaits the
human's ruling (S16.5 Part B §16, H-1/H-2). Every statement below says what a retrieved source states, or
what the Atlas concludes from the rules (`INTERPRETATION`). Nothing here is a new fact about the world beyond
what the cited sources state.

**Method:**

- the search plan ([`plan.md`](../../sessions/reports/SESSION-16.5-research/plan.md)) was written before any
  search;
- the Source Scout ran it and logged 28 queries and 51 retrieval attempts
  ([`search-log.md`](../../sessions/reports/SESSION-16.5-research/search-log.md));
- the Verifier (Claude) re-read the decisive anchors in the retrieved bytes, with hashes as logged:
  - S-20 (SK hynix, `3712f70b…`): "HBM3 to be combined with NVIDIA H100 Tensor Core GPU for accelerated
    computing" and "SK hynix will provide HBM3 for NVIDIA systems expected to ship starting in the third
    quarter of this year", both found;
  - S-18 (NVIDIA FY2026 10-K, `a056b59e…`): "We purchase memory from SK Hynix Inc., Micron Technology, Inc.,
    and Samsung", found;
- retrieved bytes stay outside the repository (RA-4's principle). The log keeps each URL, hash, access time
  and anchor.

**The rule set applied** (`source-policy.md`):

- the matrix row `rel:incorporates.supplier`:
  - preferred classes: technical documentation, filings;
  - acceptable: press releases;
  - standing: `party`;
  - freshness: `time_sensitive`;
- ER-9: the statement must be product-level;
- F-1: evidence dated on or after 2025-10-07 for verification on 2026-10-07;
- ER-3 and SP-7: an access gap is not a search.

## The NVIDIA H100

| What was found | Source | Class, standing | Date (basis) | Meets |
|---|---|---|---|---|
| SK hynix: "HBM3 to be combined with NVIDIA H100 Tensor Core GPU for accelerated computing"; "SK hynix will provide HBM3 for NVIDIA systems expected to ship starting in the third quarter of this year" | S-20, SK hynix newsroom, `news.skhynix.com/en/sk-hynix-to-supply-industrys-first-hbm3-dram-to-nvidia/` | `company_press_release` (acceptable), party (the supplier naming itself) | 2022-06-08 (the source's own date) | product-level (ER-9): **yes** for the first sentence. Fresh (F-1): **no**, more than three years before the horizon. Worded as a plan in 2022 |
| NVIDIA: "We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung" | S-18, NVIDIA FY2026 Form 10-K, company-hosted | `company_filing` (preferred), party | FY2026 filing (the source's own date) | fresh: yes. Product-level: **no**, company-level and "memory", not HBM (ER-9). Already in the Atlas as refused candidate `cand-002` |
| NVIDIA's H100 documents (datasheets, product briefs, the architecture whitepaper, the architecture blog) | S-01 to S-11 | technical documentation (preferred), party | various | name HBM3 or HBM2e; **no memory maker named** |
| Later NVIDIA and SK hynix releases on HBM collaboration (Oct 2025 to Jul 2026) | S-38 to S-41, S-43 | press releases, party | 2025–2026 (the sources' own dates) | fresh: yes. Product-level for the H100: **no**; they name "NVIDIA GPUs", "AI computing platforms", or other products (HBM3E, HBM4, Vera Rubin) |
| Micron: HBM3E "will ship in NVIDIA H200" | S-31 | product page (marketing), party | undated | about the H200, not the H100 |

**Searched and silent on the H100:** Micron FY2025 10-K and Q3 FY2026 10-Q; Samsung 2025 Business Report; the
SK hynix and Samsung HBM product pages.

**Access gaps** (SP-7, not searched):

- SK hynix's filings: its investor pages are empty JavaScript shells, and the 2026 prospectus is only on
  SEC EDGAR (excluded, D-042);
- Micron's investor site (HTTP 403, challenge page);
- Samsung's global newsroom (empty reply).

**Not searched:** NVIDIA's 2026 Forms 10-Q; SK hynix's Korean-language reports; Micron's FY2026 10-K (not found
on a company host); the candidate pages found but not read (log §2.2, 28 rows).

**What the rules conclude** (`INTERPRETATION`):

- **No supplier value can be canonical.** The only product-level party statement is stale (F-1).
- **`not_publicly_determinable` cannot be claimed.** Preferred classes were not all searched: there are
  access gaps, and NVIDIA's 10-Qs were not searched (ER-3).
- **So the field stays `not_researched`, with the research recorded** (ER-3: "the value stays
  `not_researched`, with the access gap recorded").
- **Which stale evidence to keep, and where, is the human's decision** (H-2).
- **A wording conflict to note:** the vocabulary defines `not_researched` as "No source has been checked
  for this value yet". ER-3 keeps that state after a partial search. The definition and the rule disagree
  (debt, below).

## AWS Trainium2

| What was found | Source | Class, standing | Date (basis) | Meets |
|---|---|---|---|---|
| AWS: "4 HBM stacks with a total device memory capacity of 96GiB and bandwidth of 3TB/s"; no maker named | S-13, Neuron architecture guide; also S-12, S-14, S-16, S-17, S-44, S-45 | technical documentation and press releases, party | undated pages (access date) or 2023–2024 | **no memory maker named** in any AWS source |
| Amazon: "we rely on a limited group of suppliers for semiconductor products, including … graphics processing units"; "supply volatility, including for memory chips" | S-19, Amazon 2025 Annual Report (Form 10-K) | `company_filing`, party | 2025 annual report | no supplier named |
| SK hynix: AWS among companies "selecting HBM3E", attributed to "experts" | S-28, SK hynix newsroom feature, 2026-01-05 | press feature, reporter standing for AWS's choice | 2026-01-05 | not a supply statement for Trainium2 |
| DIGITIMES headline: "Samsung and SK Hynix will both supply HBM3 for AWS Trainium 2" | S-29 | news media (never sufficient alone), reporter; body paywalled | 2023-12-07 | a pointer only; no primary source found behind it |

**What the rules conclude** (`INTERPRETATION`):

- **No party statement names Trainium2's memory maker.**
- **Two preferred-class searches are access gaps:** SK hynix's and Micron's filings.
- **The field stays `not_researched`, with the research recorded** (ER-3, SP-7). No candidate exists to
  keep or refuse.

## Debt and next checks

| Item | Owner |
|---|---|
| `not_researched`'s definition ("No source has been checked") disagrees with ER-3's use after a partial search | the next schema session (S22 engineering audit, or the Knowledge Architect when the vocabulary next changes) |
| SK hynix's and Micron's filings are access gaps: a company-hosted English filing, or a manual retrieval by the human (RA-4), would complete ER-3's search | the next supplier research; RA-4 needs the human |
| NVIDIA's 2026 Forms 10-Q, Micron's FY2026 10-K and the candidates found but not read (log §2.2) | the next supplier research |
| A fresh product-level statement would make the H100's supplier canonical. The candidates to watch: SK hynix, Micron and Samsung releases naming the H100 | Change Detector (inactive); the next supplier research |
