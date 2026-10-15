# Search plan: later rules changing the entries and acts the Atlas holds (S21.5)

Written on 2026-10-15, after the Change Detector's activation (D-207) and before any official text was retrieved
for this search. The Source Scout, the Extractor, the Change Detector and the Verifier follow it and log each step
in [`search-log.md`](search-log.md). The comparisons are ruled in
[`change-detection.md`](../../change-detection.md) §1.

**Read before this plan, as pointers only.** On 2026-10-15 between 07:07Z and 07:11Z the Federal Register's
document index (`federalregister.gov/api/v1`) was queried for BIS rules in the window and for the entry identifiers,
to know the size of the task and which registers exist. That index is a finding aid, not the official edition: it
shaped this plan and is re-run as step 1, but nothing is concluded from it.

## The question

Between **6 December 2024** (the day after the latest act the Atlas holds was published) and the **reference
date**, did any official US text:

1. add, remove or alter the wording of a control entry that a `restricts` link's evidence names — **3A090.c**
   (High Bandwidth Memory), **3B001**, **3B002** and **3B993** (semiconductor manufacturing equipment; 3B090 was
   removed in 2023 and is searched as a control); or
2. repeal one of the five acts the Atlas holds — the EAR (15 CFR parts 730-774), 87 FR 62186 (2022-21658),
   88 FR 73458 (2023-23055), 88 FR 73424 (2023-23049), 89 FR 96790 (2024-28270)?

And, for the named debts: what the official texts say of the **AI Diffusion rule** (90 FR 4544, 2025-00636) and
its reported withdrawal, and which **dates** an official text gives for the EAR as a codified regulation.

**The window's end.** The reference date is 2026-10-14 (D-137). Every register is searched to the day the search
runs (2026-10-15), so either reading of H-1 (a fixed reference date, or the day each search ran) is served; the
log records both.

## Registers

| # | Register | What it is | Used as |
|---|---|---|---|
| R1 | Federal Register document index (`federalregister.gov/api/v1/documents`) | the Office of the Federal Register's search index of published documents | finding aid: the list of BIS documents, and full-text hits for each term |
| R2 | List of CFR Sections Affected (LSA), govinfo.gov, issues December 2024, December 2025 and the latest 2026 issue | the Office of the Federal Register's official finding aid: every Federal Register page that amends each CFR part | finding aid, independent of R1: every document amending 15 CFR parts 730 to 774 |
| R3 | Federal Register daily issues' "CFR Parts Affected" reader aids, govinfo.gov, for the months after the latest LSA | the same finding aid inside the official daily edition | finding aid for the months R2 does not yet cover |
| R4 | the Federal Register's official edition (govinfo.gov PDF of each document) | the act itself (`official_legal_text`) | **the only evidence**: every anchor, every comparison |

## Steps

1. **Every BIS document in the window (R1).** All documents of the Bureau of Industry and Security, every type,
   published 2024-12-06 to 2026-10-15, listed with number, citation, action and title.
2. **Full-text terms (R1).** Each term searched in every agency's documents in the window: `3A090`, `3B001`,
   `3B002`, `3B993`, `3B090`; the five acts' citations (`87 FR 62186`, `88 FR 73458`, `88 FR 73424`,
   `89 FR 96790`) and document numbers; `Artificial Intelligence Diffusion`, `90 FR 4544`; in BIS documents:
   `rescission`, `rescind`, `repeal`, `withdraw`.
3. **Independent check (R2, R3).** Every Federal Register page the LSA and the reader aids list against 15 CFR
   part 774 (the Commerce Control List, where the four entries live) in the window, and every BIS document they list
   against parts 730 to 774 that step 1 did not find.
4. **Screening.** A document becomes a candidate when step 2 or 3 ties it to an entry or an act, or when its title
   names advanced computing, semiconductors, integrated circuits or the Commerce Control List. Every other BIS
   document is logged with the reason it was not retrieved (out of scope: Entity List, firearms, tariffs, drones,
   other items), never silently dropped (CD-3).
5. **Retrieval (R4).** Each candidate's official PDF is retrieved from govinfo.gov by an ordinary HTTPS request,
   hashed in full (SHA-256) at retrieval, and its text extracted locally (`pdftotext`). Bytes and text stay outside
   the repository. The five registered texts are re-retrieved and their hashes compared (CD-5).
6. **Reading (R4).** In each candidate's text: every occurrence of the entry identifiers, of the five acts'
   citations, and of `rescind|repeal|withdraw|revoke|remove`; each amendatory instruction that names
   supplement no. 1 to part 774 is read for the ECCNs it revises.
7. **Ruling (Change Detector).** For each hit, the comparison (CD-1 to CD-3): the earlier wording at its locator in
   the act the Atlas holds, the later wording at its locator, and what the later text says it does. Outcomes:
   - **changes a held entry** → the later act is drafted as a policy record from its official text (identity,
     citation, form, issuing authority, measure kind, `amends`), its dates as events, and the change as an
     `ATTRIBUTION` quoting the later text, proposed to be cited beside the link (D-169); if the wording of the
     matched term changed, the link's term-match `DERIVATION` is re-ruled (PK-3, PK-4);
   - **mentions a held entry without changing it** (history, a cross-reference, a licence-policy statement outside
     the entry) → logged with the sentence, no record;
   - **repeals a held act** → the repeal is an event only from the repealing text (D-156);
   - **touches only entries the Atlas does not hold** → logged as out of scope.
8. **The AI Diffusion rule.** Its official text (90 FR 4544) is retrieved for the entries (step 6) like any
   candidate. Its withdrawal counts only from an official text that rescinds or withdraws it; an index entry, a
   press release or a news report is a pointer (CD-7). If no official withdrawal text is found in the window, that
   is recorded as found, not as a conclusion that the rule applies.
9. **The EAR's dates.** The registered CFR text (`src-057`) is read for what it states about its own source and
   dates; any text it points to is a further candidate only if the human widens the scope.

## What counts

- Only official texts (`official_legal_text`, D-158) as evidence; standing originator (BIS). R1 to R3 are finding
  aids: what they list is retrieved and read, never cited.
- Claims drafted in `data/staging/claims.json`: `FACT` for what an act fixes about itself (identity, citation,
  form, dates, what it amends, D-157), `ATTRIBUTION` for what it provides, `DERIVATION` only for a term match.
- Never in a claim's wording: "in force", "rescinded" or "withdrawn" in the Atlas's own voice, a threshold applied
  to anything, a statement that a control applies to a product or firm (LA-1 to LA-5).

## Stop rules

- A later text whose effect on an entry cannot be read from its own words → quoted and put to the human.
- A finding that would need a new event kind, a new refusal reason, a schema change or a change to an accepted rule
  → stop and ask (CLAUDE.md §9A); checks first if the human approves.
- A text that cannot be retrieved → access gap, logged with host, response and time.
- A registered source whose hash changed → its anchors re-read before anything rests on it.

## From S22: the search tool (D-210, D-211)

Steps 1 to 5 are run by `tools/later_rule_search.py` for a window: step 1 and step 2 as above (the index, every BIS
document and every term; the act citations and document numbers are read from `data/policies.json`, the entries from
CD-3 of `change-detection.md`); for step 3 the independent register is the **official daily edition** itself, the XML
of each issue on govinfo.gov, read in full text for the same terms and for headings naming 15 CFR part 774, in place
of the LSA and reader-aid PDFs (which the standard library cannot read); step 4 selects candidates mechanically and
hashes their official PDFs; step 5 re-hashes the registered official texts (CD-5). Each run writes its log here as
`run-<from>-to-<to>.md`, every request with its host, time, status and hash. Steps 6 to 9 stay with the Change Detector
and the Extractor: the tool reads no PDF's text and rules nothing. A run whose outcome is "incomplete" moves no date
(JR-13).

