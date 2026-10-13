# Search log: the first export-control records (S17)

Follows [`plan.md`](plan.md). Source Scout, then Extractor and Verifier, on 2026-10-08. Times are UTC.

## Locating the candidates (pointers, not evidence)

| # | When | Query | Tool | Result | Kept as pointer |
|---|---|---|---|---|---|
| L-1 | 2026-10-08 | Federal Register search: agency `industry-and-security-bureau`, term "advanced computing", type rule | Federal Register API (`documents.json`) | 24 documents, 2022-10-13 to 2026-07-14 | 87 FR 62186 (2022-21658); 88 FR 73458 (2023-23055); 88 FR 73424 (2023-23049); 89 FR 96790 (2024-28270) |
| L-2 | 2026-10-08 | the same agency, term "high bandwidth memory" | Federal Register API | 7 documents | confirms 88 FR 73458 and 89 FR 96790 mention HBM (for S18; not used in S17) |
| L-3 | 2026-10-08 | the same agency, term "Artificial Intelligence Diffusion" | Federal Register API | 4 documents; no rescinding rule among them | not in S17's set (D-163); recorded because it shaped the status rules (P-4) |
| L-4 | 2026-10-08 | the record of document 2022-21658 | Federal Register API (`documents/2022-21658.json`) | one `effective_on` value (2022-10-07), while the text fixes three dates | the API's summary is not used as evidence (plan, "What never counts") |
| L-5 | 2026-10-08 | where the EAR are codified | govinfo.gov, Code of Federal Regulations, 2026 edition, Title 15 volume 2 | the volume PDF answers (HTTP 206 on a range request); the chapter-level URLs redirect | Part 730, the part that states what "the EAR" refers to |

## Retrievals (official texts)

All by an ordinary HTTPS request at 2026-10-08T19:54Z, each answering HTTP 200 with a PDF. Each was hashed in
full, and its text extracted locally (`pdftotext`, reading order and raw stream). The bytes stay outside the
repository. All five were re-hashed after a worker restart the same evening and matched.

| # | Act | URL | Bytes | Pages | sha256 | Registered as |
|---|---|---|---|---|---|---|
| T-1 | EAR, 15 CFR part 730 (1–1–26 Edition) | https://www.govinfo.gov/content/pkg/CFR-2026-title15-vol2/pdf/CFR-2026-title15-vol2-part730.pdf | 248587 | 10 | `ae2ed36c9fed7314d42ba28b25b9018d342a68e14c6b47c14e03772d4ce1abc2` | `src-057` |
| T-2 | BIS rule 2022-21658, 87 FR 62186 | https://www.govinfo.gov/content/pkg/FR-2022-10-13/pdf/2022-21658.pdf | 579311 | 30 | `a4d622d8c5578b38b8e2bedbcb9442d6f22385f91cdeeb373d46a299a8b8c52b` | `src-058` |
| T-3 | BIS rule 2023-23055, 88 FR 73458 | https://www.govinfo.gov/content/pkg/FR-2023-10-25/pdf/2023-23055.pdf | 949336 | 60 | `7ae382cb1812b0b3052ad66a4f1bacbc6c93f45e0aab72912cac9807475309a1` | `src-059` |
| T-4 | BIS rule 2023-23049, 88 FR 73424 | https://www.govinfo.gov/content/pkg/FR-2023-10-25/pdf/2023-23049.pdf | 669089 | 32 | `6706911eb862774430771d9c847c8594accb8cbb886feb8b4e7dd166c4ff83db` | `src-060` |
| T-5 | BIS rule 2024-28270, 89 FR 96790 | https://www.govinfo.gov/content/pkg/FR-2024-12-05/pdf/2024-28270.pdf | 530065 | 41 | `9c9ea7f0655e32b76647b83ca64432792a83f43e74eb917017466b806c3f4c84` | `src-061` |

No access gap: every planned text was retrieved.

## What each text states (the fields of P-3 and the dates of P-4)

Every anchor was found verbatim in the extracted text of the registered bytes, at the page given in its
claim's locator. The 2023-23055 dates sentence was matched in the raw stream only: the reading-order
extraction splices a column heading ("Background") into it.

| Act | Title, citation, form | Authority, country | Amends | Measure | Published | Effective (as the text fixes) |
|---|---|---|---|---|---|---|
| EAR | "Export Administration Regulations (EAR)" = "15 CFR chapter VII, subchapter C" (§ 730.1) | "United States Department of Commerce, Bureau of Industry and Security (BIS)" (§ 730.1) | not applicable | "under laws relating to the control of certain exports, reexports, and activities" | not researched | not researched |
| 2022-21658 | p.1 title; Vol. 87, p. 62186; "Interim final rule; request for comments." | "Bureau of Industry and Security, Department of Commerce." | EAR parts 734, 736, 740, 742, 744, 762, 772, 774 (p.10) | title: "Additional Export Controls" | 2022-10-13 | 2022-10-07 (instructions 7, 9, 11, 17, 25); 2022-10-12 (15); 2022-10-21 (2, 3, 5, 8, 12, 14, 16, 18, 19, 21, 23, 26) |
| 2023-23055 | p.1 title; Vol. 88, p. 73458; "Interim final rule; request for comments." | "Bureau of Industry and Security, Department of Commerce." | EAR, twelve parts (p.30) | title: "Additional Export Controls" | 2023-10-25 | 2023-11-17; instruction 11 "effective from November 17, 2023, to January 1, 2026" |
| 2023-23049 | p.1 title; Vol. 88, p. 73424; "Interim final rule; request for comments." | "Bureau of Industry and Security, Commerce."; "Bureau of Industry and Security, U.S. Department of Commerce" (p.1, contact) | EAR, seven parts (p.23) | title: "Export Controls on Semiconductor Manufacturing Items" | 2023-10-25 | 2023-11-17; instruction 5 on 2026-01-01 |
| 2024-28270 | p.1 title; Vol. 89, p. 96790; "Interim final rule." | "Bureau of Industry and Security, Commerce." | EAR, eleven parts (p.20) | SUMMARY: "changes to the Export Administration Regulations (EAR) controls" | 2024-12-05 | 2024-12-02 (later compliance dates for some instructions are not effective dates) |

## Findings for the record

- **The API's single effective date is wrong for 2022-21658** (L-4): the text fixes three. The design's rule
  (one event per date the text fixes) is the one the text needs.
- **Effect before publication is common:** 2022-21658 (instructions effective 2022-10-07, published
  2022-10-13) and 2024-28270 (effective 2024-12-02, published 2024-12-05).
- **An instruction with an end date:** 2023-23055 makes one instruction effective only until 2026-01-01. The
  schema has no event for the end of one instruction; it is stated in the claim and listed as a limitation.
- **2024-28270's heading and its amendatory clause list different parts** (the heading names part 746, the
  clause part 770). The record cites the clause, which is the operative text.
- **"United States" in the rules:** only 2023-23049 names the "U.S. Department of Commerce". For the other
  three, the country rests on two official texts: the rule's own AGENCY line and the EAR's statement that the
  EAR are issued by the United States Department of Commerce, BIS (`src-057`). This is put to the human at
  H-2 as the one place where two texts are joined.
- **The EAR's own dates were not researched:** part 730 notes "SOURCE: 61 FR 12734, Mar. 25, 1996, unless
  otherwise noted", which dates part 730's text, not the EAR as a whole. The EAR record therefore has no
  events, and its status reads "no effective date recorded in the Atlas".

## Drafts (staging)

5 sources registered at retrieval (D-146); 5 policy records, 37 claims and 11 events drafted in
`data/staging/`, by the private drafting script of the session.
