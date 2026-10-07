# S16.6 search plan, under the rules as decided (D-144 to D-147)

Written before any S16.6 search, on 2026-10-07. S16.5's log
([`../SESSION-16.5-research/search-log.md`](../SESSION-16.5-research/search-log.md)) stands. Its searches are not
repeated, except where the new rules change what counts.

## The questions

The same two questions as S16.5:

- **Q-H100:** who supplies the HBM in the NVIDIA H100?
- **Q-TRN2:** who supplies the HBM in AWS Trainium2?

## What now counts

- **The parties, as before:** a product-level statement from NVIDIA, Amazon/AWS or a memory maker.
  - Evidence dated on or after 2025-10-07 supports a current value.
  - Older evidence supports a **historical** value, with `valid_to` no later than the evidence date
    (D-144), and only if it states the past, not a plan (ER-8).
- **Teardowns (D-145):** a report by a laboratory that examined the **named product** (H100 SXM5, H100 PCIe,
  H100 NVL, or Trainium2) and identified the HBM's maker from the unit (markings, die analysis). Class
  `research_report`, `originator` standing.
- **Third parties (D-147):** a report or article naming the HBM maker for the named product, by a publisher
  that is:
  - **internationally recognised as reliable:** an international news agency or newspaper of record (for
    example Reuters, Bloomberg, Financial Times, Nikkei Asia, The Wall Street Journal), or an established,
    independent analysis or teardown firm (for example TrendForce, TechInsights, Yole Group, Counterpoint,
    Omdia);
  - **independent:** not owned, commissioned or sponsored by a party for the statement.

  Recency is preferred: on or after 2025-10-07. Older reports support only historical values. An unmet
  criterion is allowed only if no better source exists, and it is recorded.
- **Still never counts:**
  - market share alone;
  - a supplier's customer list without the product;
  - a company-level statement (ER-9);
  - a search snippet;
  - a paywalled article read only through its headline or teaser. The headline may be logged as a pointer
    and an access gap.

## Search order

| # | Kind | What to look for |
|---|---|---|
| 1 | Teardowns | public teardown reports or articles of an H100 or Trainium2 unit naming the HBM maker (TechInsights, Yole Group, and others) |
| 2 | Recognised press | articles by international outlets naming the HBM maker for the H100 or Trainium2; recent first |
| 3 | Recognised analysts | public releases by TrendForce, Counterpoint, Omdia and others naming the maker for the product; recent first |
| 4 | Parties, past tense | statements by NVIDIA, AWS, SK hynix, Samsung or Micron that they **supplied** (not "will supply") HBM for the H100 or Trainium2, for R-1 |
| 5 | Pointers from S16.5 | TrendForce 2024-03-13; DIGITIMES 2023-12-07 (paywalled); KED Global 2022-06-09: retrieve the public ones and assess them under the criteria |

## Retrieval and recording

- **Retrieval:** RA-1 to RA-7, as in S16.5. Raw bytes stay outside the repository; refusals are access
  gaps.
- **For each kept source, the log records:**
  - its class, publisher and dates;
  - whether it names the specific product and HBM;
  - the anchor and locator;
  - the publisher's **recognition** and **independence**, each with the reason the scout proposes. The
    Verifier confirms.
