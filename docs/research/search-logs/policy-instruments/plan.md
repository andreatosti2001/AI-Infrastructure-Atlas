# Search plan: the first export-control records (S17)

Written before any retrieval, on 2026-10-08, after the design rulings (D-154 to D-164) and the choice of the
five acts (D-163). The Source Scout follows it and logs each step in [`search-log.md`](search-log.md).

## The questions

For each act, what its own official text states about:

1. **identity**: its official title, its official citation, its issuing authority, the jurisdiction that
   issued it, and its form as the official journal labels it (`attr:policy.*`, `identity:policy`);
2. **what kind of measure it is**, in its own words (`attr:policy.measure_kinds`);
3. **what it amends**, in its own words (`attr:policy.amends`);
4. **its dates**: the date of publication, and every effective date its "DATES" section fixes
   (`event:published`, `event:effective`). A compliance date, a comment deadline or a delayed
   applicability is not an effective date and is not recorded as one.

Nothing else is extracted in S17. What the act controls, and whom it names, is S18's question (D-160).

| # | Act | Official text to retrieve |
|---|---|---|
| A-1 | The Export Administration Regulations (EAR), 15 CFR parts 730 to 774 | the Code of Federal Regulations, annual edition on govinfo.gov, the part that states what "the EAR" refers to (part 730) |
| A-2 | BIS rule 2022-21658, 87 FR 62186, 13 October 2022 | the Federal Register, official PDF edition on govinfo.gov |
| A-3 | BIS rule 2023-23055, 88 FR 73458, 25 October 2023 | the same |
| A-4 | BIS rule 2023-23049, 88 FR 73424, 25 October 2023 | the same |
| A-5 | BIS rule 2024-28270, 89 FR 96790, 5 December 2024 | the same |

The citations above come from the Federal Register's search service, which located the candidates on
2026-10-08. They are pointers. Each is confirmed or corrected from the retrieved text.

## What counts (source-policy.md §7, the policy rows; D-157, D-158)

- **Only `official_legal_text`** supports these fields and dates: the act as the official journal or the
  official code publishes it. govinfo.gov is the U.S. Government Publishing Office's official publication
  site for the Federal Register and the annual Code of Federal Regulations.
- **Standing:** the issuing authority is the `originator` of its own act.
- **Claim types:** `FACT` for what the text fixes about the act itself (identity, citation, form,
  publication, effective dates, what it amends); `ATTRIBUTION` to the authority for what the act provides
  (here, only that it is an export-control measure). Nothing else (PL-5).

## What never counts

- the Federal Register's web pages and its API metadata, including its single `effective_on` value. They
  locate the document; the PDF edition is the text. (The API gives one effective date for rule
  2022-21658, while its text fixes several.)
- eCFR, which presents itself as an editorial compilation, not the official edition;
- BIS press releases, fact sheets and FAQs (`government_publication`): never sufficient for a policy's dates
  (D-158). Not needed in S17;
- news, law-firm alerts and secondary summaries. Pointers at most, and none is planned.

## Retrieval (RA-1 to RA-7)

- Each text is retrieved by an ordinary HTTPS request, hashed (sha256) in full, and its text extracted
  locally with `pdftotext -layout`. The bytes and the extracted text stay outside the repository; the log
  keeps the URL, the time, the size and the hash.
- A source is registered in `data/sources.json` when retrieved (D-146), as `official_legal_text`.
- Anchors are read in the extracted text of the registered bytes and recorded verbatim (Verifier-attested,
  VD-11). Each anchor is then re-read once more, in the bytes, before H-2.
- A refusal (403, challenge, timeout) is an access gap, logged, never worked around. If an act's text cannot
  be retrieved, its record is not drafted (S17 prompt §16).

## Stop rules for the scout

- Every retrieval attempt is logged, kept or not, with the reason.
- A field the text does not state stays `not_researched` or `not_applicable`, never inferred.
- If a text contradicts the pointer (another citation, title or date), the text wins and the difference is
  logged.
