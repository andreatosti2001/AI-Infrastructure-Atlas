# Change detection

**Status:** ACTIVE from S21.5 (D-207); rules CD-1 to CD-7 accepted on 2026-10-15 (D-209). **Owner:** the Change Detector (`docs/agents/contracts.md`).

This file holds the rules the Change Detector keeps and the comparisons it has ruled. A comparison is a
**candidate change**: what a later official text does to an entry or an act the Atlas holds, quoted from both
texts. It is never a conclusion about legal effect, and it changes no record. The records a change needs are
drafted by the Extractor in `data/staging/` and become canonical only on the human's recorded verdict
(D-183).

## Rules

| ID | Rule |
|---|---|
| CD-1 | **Both sides quoted.** Every comparison quotes the earlier text and the later text, each at its locator, from official texts (`official_legal_text`, D-158) read in the bytes whose hash is registered. |
| CD-2 | **The later text's own words.** What changed is said in the later text's words (adds, removes, revises, moves, repeals). The Atlas does not infer an effect the text does not state. |
| CD-3 | **What counts as a change to an entry the Atlas holds.** A later official text changes an entry the Atlas holds when it adds, removes or alters the wording of a control entry that a `restricts` link's evidence names (3A090.c; 3B001, 3B002 and 3B993, the successors of 3B090), or repeals an act the Atlas holds. An amendment of one entry is not a repeal of the act that created it (D-169). A later text that touches only entries the Atlas does not hold is out of scope and is logged as such, never silently ignored. |
| CD-4 | **A search that finds nothing records itself.** Its terms, registers, the window searched and the date it ran. The finding reads "none found in the searched window", never "none exists". |
| CD-5 | **A changed hash is reported, never silently re-registered.** If a registered source's bytes change, the Verifier re-reads every anchor that rests on it (`source-policy.md` §12); the source record is not edited to the new hash. |
| CD-6 | **Candidates only.** A comparison is a candidate until the human's verdict on the records it proposes. No link is dated by a later act; an act's status comes only from its own events (D-156, D-169). |
| CD-7 | **Pointers are not texts.** An index entry, a press release or a summary may point the search to a later text; it never stands for that text. A text that cannot be retrieved is an access gap (SP-7). |

## §1 — The later-rule search (D-175), first task

**Question.** Between 6 December 2024 (the day after the latest act the Atlas held was published) and the reference
date, did any official US text change the control entries the Atlas's `restricts` links rest on (3A090.c; 3B001,
3B002, 3B993) or repeal one of the five acts the Atlas held?

**Searched to:** 2026-10-15

**Window and method.** 2024-12-06 to 2026-10-15, the day the search ran and the reference date the pages carry
(D-137). Four registers: the Federal Register's index (every BIS document, 182; the entry identifiers and the acts'
citations as full-text terms), the List of CFR Sections Affected and the daily Federal Register's "CFR parts
affected" as an independent check, and the official texts on govinfo.gov as the only evidence. Plan, terms, times,
hashes and every document's disposition: [`search-logs/later-rules/`](search-logs/later-rules/). The ruling below
is the Change Detector's; each candidate record is the Extractor's draft in `data/staging/`, and nothing is
canonical before the human's verdict (CD-6).

### Findings

- **Two later acts change entries the Atlas holds**: 90 FR 5298 (2025-00711, published 16 January 2025) and
  90 FR 4544 (2025-00636, the AI Diffusion rule, published 15 January 2025).
- **No text in the window repeals any of the five acts.** The two rules cite them as history; 90 FR 5298 also extends
  the comment period of 89 FR 96790.
- **3B002 is not revised** by any text in the window.
- **The AI Diffusion rule:** no official text in the window rescinds or withdraws it. 91 FR 43034 (2026-14132,
  14 July 2026) states that the worldwide licence requirement it added is still specified in the EAR and that BIS
  enforces it only to named country groups, citing guidance of 13 May 2025 and 31 May 2026 (pointers, not read).
- **Mentions without change, and out of scope** (logged, no record): 90 FR 9604 re-issues 3A090 with 3A090.c word for
  word as in 90 FR 5298; 91 FR 17851 changes a date in note 1 to 3A090.a; 91 FR 43034 changes 3A090's licence-
  requirement country chart; 91 FR 1684 changes licence review policy in § 742.6; 90 FR 4612 and 89 FR 105448 change
  other entries that name 3A090.c or 3B001 in their own lists.
- **The EAR's dates:** not recorded. The CFR text points to the 1996 rule that reissued the EAR; what dates a codified
  regulation as a whole has is left to the next policy session (search log, step 9).

### Comparisons (CD-1, CD-2)

Earlier text: the act the Atlas holds, in its registered bytes. Later text: the later act, registered at retrieval.
Both re-read on the stated page by the Verifier (40 of 40 anchors found in the registered bytes).

| # | Entry | Earlier text (act held, locator) | Later text (locator) | What the later text says it does | Candidate records (staging) | Proposed beside the link |
|---|---|---|---|---|---|---|
| C-1 | 3A090.c | 89 FR 96790 (`src-061`) p.31: "c. High bandwidth memory (HBM) having a ‘memory bandwidth density’ greater than 2 gigabytes per second per square millimeter. Technical note to 3A090.c: …" | 90 FR 4544 (`src-062`) p.24, instruction 26: "Supplement no. 1 to part 774 is amended by: ■ a. Revising ECCNs 3A001, 3A090, …"; p.31: "c. High bandwidth memory having a ‘memory bandwidth density’ greater than 2 gigabytes per second per square millimeter." | revises ECCN 3A090; in 3A090.c the abbreviation "(HBM)" is absent, and the note says "high bandwidth memory" where the earlier note said "HBM". The controlled-item threshold is the same words | policy record `policy-us-fr-2025-00636`; its identity, form, dates and amends claims; `claim-bis-rule-2025-00636-revises-3a090` | `rel-policy-us-fr-2024-28270-restricts-component-high-bandwidth-memory` |
| C-2 | 3A090.c | as C-1 | 90 FR 5298 (`src-063`) p.17, instruction 30: "Supplement no. 1 to part 774 is amended by revising ECCN 3A090, 3B001, 3B993 and 3B994, … to read as follows:"; p.18: "c. High bandwidth memory (HBM) having a ‘memory bandwidth density’ greater than 2 gigabytes per second per square millimeter. Technical Note 1 to 3A090.c:" | revises ECCN 3A090 to read as follows; 3A090.c's sentence is the earlier one word for word; the note is renamed "Technical Note 1 to 3A090.c" and adds "(HBM)" after "JEDEC standards for high bandwidth memory" | policy record `policy-us-fr-2025-00711`; its identity, form, dates and amends claims; `claim-bis-rule-2025-00711-revises-3a090` | the HBM link, as C-1 |
| C-3 | 3B001 | 89 FR 96790 p.31 (3B001 as the act held revises it): "NS applies to 3B001.a.4, c, d, f.1, f.5, k to n, p.2, p.4, r."; paragraph f headed "Lithography equipment as follows" (p.33) | 90 FR 5298 p.9: "This rule adds new paragraphs under 3B001.f, 3B993.f, …"; p.18: "RS applies to 3B001.a.4, c, d, f.1, f.5, f.6, k to n, p.2, p.4, r."; p.20: "f. Lithography commodities as follows:"; p.21: "f.6. Commodities not specified by 3B001.f.1, designed or modified to perform all of the following in or with …" | adds paragraph 3B001.f.6 (commodities that improve deep-ultraviolet immersion lithography equipment) and names it in the NS and RS control lines; heads paragraph f "Lithography commodities" | `claim-bis-rule-2025-00711-adds-3b001-f6` | `rel-policy-us-fr-2023-23049-restricts-component-semiconductor-manufacturing-equipment` (its evidence names 3B001) |
| C-4 | 3B993 | 89 FR 96790 p.36: "3B993 Specified semiconductor manufacturing equipment as follows (see list of items controls)."; paragraph f headed "Lithography equipment as follows" (p.37) | 90 FR 5298 p.9: "This rule amends the headings for ECCNs 3B993 and 3B994 …"; p.21: "3B993 Specified semiconductor manufacturing equipment as follows (see list of items controls), and ‘‘specially designed’’ ‘‘components’’ and ‘‘accessories’’ therefor."; p.22: "f. Lithography commodities as follows:", "f.4. Commodities not specified by 3B993.f.1 …" | adds "specially designed" components and accessories to the heading; adds paragraph f.4; heads paragraph f "Lithography commodities" | `claim-bis-rule-2025-00711-revises-3b993` | the 2023 SME link, as C-3 (its evidence names 3B993, through `claim-bis-rule-2024-28270-revises-3b001-3b002`) |
| C-5 | the AI Diffusion rule (its status) | 90 FR 4544 p.18: § 742.6(a)(6)(iii)(A), "Worldwide license requirement" | 91 FR 43034 (`src-064`) p.3: "Although § 742.6(a)(6)(iii)(A) of the EAR specifies a worldwide license requirement … BIS is only enforcing this license requirement to destinations in Country Groups D:1, D:4, or D:5 …" | states the requirement is still specified in the EAR and how BIS enforces it; neither repeals nor amends the AI Diffusion rule | `claim-bis-rule-2025-00636-worldwide-requirement`, `claim-bis-rule-2026-14132-enforcement-statement`; no event (a repeal comes only from a repealing text, D-156) | none (no record field or link holds it) |

### Later statements about acts held

A later official text's statement about an act the Atlas holds, as ruled in a comparison above. The export-control
page and the client brief show each claim in its act's evidence, under "Later statements about this act" (D-210,
D-214); the act's status stays derived from its own events (D-156, CD-6). A row is added only with the comparison that
rules it and the human's verdict on its claim.

| Act | Later statement | Comparison |
|---|---|---|
| `policy-us-fr-2025-00636` | `claim-bis-rule-2026-14132-enforcement-statement` | C-5 |

**Term matches (PK-3, PK-4) are not re-ruled.** Each link's `DERIVATION` matches the word of its own act's sentence
("HBM stacks" in 89 FR 96790 p.10; "semiconductor manufacturing equipment" in the SME acts); no later text changes
those sentences, and the later texts still name "High bandwidth memory" and semiconductor manufacturing equipment.

**What this does not say.** That any change has legal effect for a product, firm or destination; that any entry or
act is "in force"; that the AI Diffusion rule is or is not rescinded. The Atlas records what the texts say and the
dates they fix.

**Status:** all candidates accepted by the human on 2026-10-15 and made canonical (D-209;
`docs/quality/human-reviews.md`). The rules CD-1 to CD-7 bind every later comparison.

### Announcements about acts held (S23, D-220)

An authority's announcement about an act the Atlas holds is not a later text (CD-7): it is recorded as an
`announced` event on the act, which never moves the act's status (ER-8, D-156), and its claim is an `ATTRIBUTION` of
intent. The Change Detector rules which act it concerns.

| Act | Announcement | Why it is this act |
|---|---|---|
| `policy-us-fr-2025-00636` | `event-us-fr-2025-00636-announced-2025-05-13` (`claim-bis-ai-diffusion-rescission-announced-2025-05-13`, `src-065`, BIS press release of 13 May 2025) | the release names "the Biden Administration's AI Diffusion Rule" and says it "was issued on January 15, 2025"; the Atlas holds one act of that name published that day (90 FR 4544, "Framework for Artificial Intelligence Diffusion"); and 91 FR 43034 (p.3) cites this release's address as the guidance of 13 May 2025 about § 742.6(a)(6)(iii)(A), which 90 FR 4544 added |

The pointer of C-5 to the guidance of 13 May 2025 is now read; the one to the guidance of 31 May 2026 is not (its
printed address returned 404 on 2026-10-15; release content audit, search log). A PDF on `media.bis.gov` titled as
the same release differs from the page in its date (12 May), its verb ("initiated") and what BIS plans ("a Federal
Register notice"); it is not registered, and the page the official text cites is the source.

## §2 — Later runs of the search (S22 onward, D-211)

Each run of `tools/later_rule_search.py` writes its log in [`search-logs/later-rules/`](search-logs/later-rules/).
The "Searched to" date of §1 moves to a run's last day only when the run is complete and every candidate it lists is
ruled here (CD-4, CD-6); JR-13 checks that the complete windows join without a gap up to that date.

| Window | Log | Outcome | Ruling |
|---|---|---|---|
| 2026-10-15 to 2026-10-15 | [`run-2026-10-15-to-2026-10-15.md`](search-logs/later-rules/run-2026-10-15-to-2026-10-15.md) | none found in the searched window; the eight registered official texts unchanged | none needed; "Searched to" stays 2026-10-15 (the run re-checks S21.5's last day: S22 opened on the day S21.5's search ran) |

