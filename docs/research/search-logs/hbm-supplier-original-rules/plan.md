# S16.5 search plan (Part B §06 q2–q3, §07 task 5)

Written before any search, on 2026-10-07. The Source Scout follows it and logs each step in `search-log.md`.

## The question (two instances)

- **Q-H100:** which company supplies the High Bandwidth Memory incorporated in the NVIDIA H100? It is the
  `supplier` of `rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory`.
- **Q-TRN2:** which company supplies the High Bandwidth Memory incorporated in AWS Trainium2? It is the
  `supplier` of `rel-product-amazon-com-trainium2-incorporates-component-high-bandwidth-memory`.

**What counts as an answer** (`source-policy.md` matrix row `rel:incorporates.supplier`; ER-9; F-1;
taxonomy §12):

- a statement **about this product** (H100, or Trainium2; not "NVIDIA", "AWS", "AI accelerators" or
  "a customer");
- **about HBM** ("memory" is not HBM);
- made by a **party**: the accelerator's vendor (NVIDIA, Amazon/AWS) or a supplier naming itself;
- in a **preferred** class (`company_technical_documentation`, `company_filing`) or an **acceptable** one
  (`company_press_release`);
- with an **evidence date within 12 months** of verification, so on or after 2025-10-07 for a
  verification on 2026-10-07. Each date's basis is recorded: as-of, the source's own date, or the
  access date.

**What never counts:**

- news media, market research or analyst estimates, except as a pointer to a primary source;
- market share;
- a supplier's customer list without the product;
- a company-level statement.

## Parties and classes, in search order (ER-3: preferred classes first)

| # | Party | Class | What to look for |
|---|---|---|---|
| 1 | NVIDIA | `company_technical_documentation` | the H100 datasheet, the Hopper architecture whitepaper, the H100 product page: is the memory maker named? |
| 2 | Amazon/AWS | `company_technical_documentation` | the Trainium2 architecture page (Neuron docs, `src-043`'s successor), the Trn2 instance pages: is the memory maker named? |
| 3 | NVIDIA | `company_filing` | the latest annual report (FY2026 Form 10-K), company-hosted copy (RA-6, D-042): suppliers named, and at what level |
| 4 | Amazon | `company_filing` | the latest annual report (2025 Form 10-K), company-hosted copy: suppliers named for Trainium |
| 5 | SK hynix | `company_technical_documentation`, `company_filing` | product pages and the latest annual or business report (English, company-hosted): H100 or Trainium2 named as using its HBM? |
| 6 | Micron | `company_technical_documentation`, `company_filing` | product pages and the FY2025 Form 10-K (company-hosted): H100 or Trainium2 named? |
| 7 | Samsung Electronics (no company record) | `company_technical_documentation`, `company_filing` | product pages and the latest annual or business report (English, company-hosted): H100 or Trainium2 named? |
| 8 | all of the above | `company_press_release` (acceptable) | newsroom releases naming H100 or Trainium2 together with the supplier's HBM |

Then, only as pointers: news or analyst reports that name a primary source. The primary source is then
retrieved under rows 1–8. A pointer never becomes a citation.

## Retrieval (RA-1 to RA-7)

- **Discovery:** web search only discovers URLs.
- **Retrieval:** each kept candidate is retrieved with an ordinary HTTPS request. Its bytes are hashed
  (sha256) and its text is extracted locally. Full texts stay out of the repository; the repository keeps
  the record, the locators and short anchors.
- **Refusals:** a refusal (403, challenge, login wall) is an access gap, recorded, never bypassed. SEC
  EDGAR is not used (D-042); filings come from company-hosted copies.

## Stop rules for the scout

- **Every candidate is logged:** the query, the URL, the class, the party, kept or dropped, and why.
- **ER-3 is complete for a part** when rows 1–7 have each been searched for that part, or recorded as an
  access gap, and row 8 has been searched.
- Nothing is written to `data/` or `data/staging/` by the scout. The Extractor stages records after the
  log exists.
