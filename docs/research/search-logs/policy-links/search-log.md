# Search log: the first policy links (S18)

Follows [`plan.md`](plan.md). Source Scout, then Extractor and Verifier, on 2026-10-13. Times are UTC.

## Retrievals

The five registered texts, each retrieved again by an ordinary HTTPS request from its registered URL at
2026-10-13T18:45Z. Each answered HTTP 200 with a PDF, was hashed in full and compared with the registered
hash. **All five match**, so no link is stopped (S18 prompt §16). The same texts had already matched at the
opening, 2026-10-13T15:13Z, when they were read for the design only (plan, "Read before this plan").

| Source | Act | Bytes | sha256 | Registered hash |
|---|---|---|---|---|
| `src-057` | EAR, 15 CFR part 730 | 248587 | `ae2ed36c9fed7314d42ba28b25b9018d342a68e14c6b47c14e03772d4ce1abc2` | matches |
| `src-058` | 87 FR 62186 (2022-21658) | 579311 | `a4d622d8c5578b38b8e2bedbcb9442d6f22385f91cdeeb373d46a299a8b8c52b` | matches |
| `src-059` | 88 FR 73458 (2023-23055) | 949336 | `7ae382cb1812b0b3052ad66a4f1bacbc6c93f45e0aab72912cac9807475309a1` | matches |
| `src-060` | 88 FR 73424 (2023-23049) | 669089 | `6706911eb862774430771d9c847c8594accb8cbb886feb8b4e7dd166c4ff83db` | matches |
| `src-061` | 89 FR 96790 (2024-28270) | 530065 | `9c9ea7f0655e32b76647b83ca64432792a83f43e74eb917017466b806c3f4c84` | matches |

No new source was retrieved or registered. Nothing else was read: no Federal Register web page, no API
record, no press release, no secondary summary.

## Step 1 and 3: every record's name and aliases, in every text

The name and every alias of the 7 component, 9 technology, 9 company and 3 product records, searched in each
text's extracted pages (case and hyphenation loose). PDF page indices.

| Text | Record (term) | Pages |
|---|---|---|
| `src-057` | none | — |
| `src-058` | semiconductor manufacturing equipment | 1, 2, 3, 7, 23 |
| `src-058` | cloud computing | 20 |
| `src-059` | High Bandwidth Memory, HBM | 27, 31 |
| `src-059` | semiconductor manufacturing equipment; SME | 1; 1 to 28 (fifteen pages) |
| `src-059` | cloud computing | 10 |
| `src-060` | semiconductor manufacturing equipment; SME | fifteen pages; twenty-three pages |
| `src-060` | EUV lithography | 17 |
| `src-061` | High Bandwidth Memory; HBM | 1, 9 to 12, 25, 27, 31; seventeen pages |
| `src-061` | semiconductor manufacturing equipment; SME | twelve pages; seventeen pages |
| `src-061` | advanced packaging | 15 |
| `src-061` | EUV lithography | 16, 34 |
| `src-061` | DUV lithography | 39 |

**No text names any of the nine companies or three products.** "Micron" appears only in "microns", a unit. The
records data-centre GPU, AI ASIC, AI accelerator, electronic design automation, accelerated server and the
remaining technologies are not named in their own words. The rules name broader terms instead (step 2).

## Step 2: the hits read in context

| Hit | Reading | Outcome |
|---|---|---|
| 2024-28270, p.10: "BIS is adding a new ECCN control on HBM stacks …" | the act adds a control on the class, in the record's alias | link (HBM) |
| 2024-28270, p.11: "All HBM stacks currently in production exceed this threshold." | a threshold statement; linking a named HBM product on it would apply the threshold | refused, `applies_a_threshold` (Micron HBM4 36GB 12H), `cand-021` |
| 2023-23055, pp.27, 31: red flag 19, chips that "will incorporate … high-bandwidth memory (HBM)" | HBM names a feature of the chips that raise a red flag, not an item the rule controls | refused, `relation_not_stated`, `cand-013` |
| 2022-21658, p.7: "BIS adds to the CCL certain advanced semiconductor manufacturing equipment under a new ECCN 3B090"; p.23, the 3B090 heading | the act adds a control on the class, in the record's name | link (SME) |
| 2023-23049, p.1: "amends the EAR to implement SME controls more effectively"; p.14: "removes ECCN 3B090 and replaces and expands its provisions in ECCNs 3B001 and 3B002" | the act states the SME controls it implements and the entries that carry them | link (SME) |
| 2024-28270, p.1: "adding new controls for certain semiconductor manufacturing equipment and related items" | the act adds controls on the class, in the record's name | link (SME) |
| 2023-23055, p.1 and later: "SME" | describes the October 7 IFR's control and the companion "SME IFR" (2023-23049); the rule adds no SME control of its own | refused, `relation_not_stated`, `cand-014` |
| 2022-21658 p.26, 2023-23055 p.46, 2024-28270 p.31: the 3A090 note, "graphical processing units (GPUs), … co-processors/accelerators, … application-specific integrated circuits (ASICs)" | broader terms than data-centre GPU, AI accelerator and AI ASIC | refused, `term_not_matched`, `cand-015` to `cand-017` |
| 2023-23049 p.17, 2024-28270 p.16: EUV pellicles, equipment for EUV pellicles, equipment improving patterning achieved by EUV lithography | items used for the technology, not the technology | refused, `term_not_matched`, `cand-018` |
| 2024-28270 p.17: "less-advanced DUV photolithography equipment"; p.39: software for DUV lithography masks | equipment and software for the technology | refused, `term_not_matched`, `cand-019` |
| 2024-28270 p.19: ECAD software for multi-chip packaging; p.15: TSV etch equipment "used in advanced packaging applications" | a narrow kind of design software, and equipment used for the packaging technology | refused, `term_not_matched`, `cand-020` (EDA, advanced packaging) |
| 2022-21658 p.20: "Shenzhen Cloud Computing Center"; 2023-23055 p.10: "Application of EAR to Grid and Cloud Computing Services" | part of an entity's alias, and the title of an advisory opinion; neither is about the class | not a candidate (logged only) |

## Step 4: later changes to the entries the links name (K-4, D-169)

Each link's own anchors were read for the control entries they name, and every later act the Atlas holds was
searched for that identifier.

| Link | Entries in its anchors | Later acts held | Found | Recorded |
|---|---|---|---|---|
| 2022-21658 → SME | 3B090 | 2023-23055, 2023-23049, 2024-28270 | 2023-23049 removes 3B090 and replaces and expands its provisions in 3B001 and 3B002 (pp.14, 17). 2023-23055 mentions 3B090 once, in a commenter's request (p.8). 2024-28270 mentions it as history (p.2) | `claim-bis-rule-2023-23049-removes-3b090`, cited by the link |
| 2023-23049 → SME | 3B001, 3B002 (3B090 removed) | 2024-28270 | 2024-28270 amends 3B001, moves seven commodities from 3B001 into the new 3B993 (pp.15, 17), and amends 3B002 (p.16) | `claim-bis-rule-2024-28270-revises-3b001-3b002`, cited by the link |
| 2024-28270 → SME | none named in the anchor | none (the latest act held) | — | — |
| 2024-28270 → HBM | 3A090.c | none (the latest act held) | — | — |

**Not searched:** acts the Atlas does not hold, among them any rule after 5 December 2024 that may change
3A090.c, 3B001, 3B002 or 3B993. Debt for the M5 audit, with S17's repeal-search debt (D-169).

## Drafts (staging) and the Verifier's re-read

- **4 links:** `restricts` from 2024-28270 to HBM, and from 2022-21658, 2023-23049 and 2024-28270 to semiconductor
  manufacturing equipment.
- **10 claims:** 6 `ATTRIBUTION` (4 the acts' own, 2 later changes) and 4 `DERIVATION` (the term matches).
- **9 refused candidates:** `cand-013` to `cand-021`.

**Verifier:** 28 anchors (the claims' 13 citations and the refused candidates' 15 considered sentences) re-read.
Each is verbatim on the page its locator names, in the extracted text of bytes whose hash is the registered
one, and each `read` records the 18:45Z retrieval. Problems: none.

One wording note for the human: the 2024 rule defines its HBM more widely at one edge than the Atlas's working
definition: DRAM ICs count "regardless of whether they conform to the JEDEC standards". The term-match claim
states this, and the link carries neither edge.
