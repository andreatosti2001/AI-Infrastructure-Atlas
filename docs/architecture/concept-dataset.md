# Concept dataset — technologies, components and the first products

**Status:** PROPOSED (S08): D-067 to D-077, for the human's review.
**Session:** S08 · **Date:** 2026-10-01
**Inputs:**
- `entity-taxonomy.md` §3.3 (technology), §3.4 (component), §3.5 (product), §4.2 (the
  pairs most easily confused), §5 (v1 concept mapping), §9 (handoffs);
- `../research/domain-map.md` §5 (the concept entries), §6 (CON-01 to CON-05), §7.1 (the
  TQ answers);
- `claim-model.md` §2 to §4 (claim types and statuses), §13;
- `../research/source-policy.md` §2 (classes), §7 (rows `identity:technology`,
  `identity:component`, `identity:product`, `attr:*.definition`, `attr:product.*`), §10
  (conflicts), §11 (RA-1 to RA-7), §12 (byte changes);
- `company-dataset.md` (the patterns reused: staging, attested anchors, record checks);
- the S08 prompt, Part B, with the human's answers H-1 to H-6.

**Schemas:** unchanged. Records follow
[`schemas/entities.schema.json`](../../schemas/entities.schema.json) as accepted in S03.
**Data:** [`data/technologies.json`](../../data/technologies.json),
[`data/components.json`](../../data/components.json) and
[`data/products.json`](../../data/products.json) (canonical), with their staging copies
under [`data/staging/`](../../data/staging/) (H-3).

**One home for each kind of statement:**

- **The schema** holds the record shapes and the kind vocabularies, including which concept
  each `technology_kind` and `use_class` value serves (`x-concepts`).
- **`entity-taxonomy.md` §5** holds which concept becomes which record type, and the
  concept's name.
- **This document** holds the reasoning for the first concept and product records: which
  concepts got records and which are gaps, the ID rules, the working-definition rule,
  `broader`, the product rulings, and the record-level checks.
- **The records** hold the values, and **the claims** hold the sentences and sources.
  Nothing in this document is a value of a record.
- **Checked by** `tests/test_data_entities.py` and `tests/test_data_integrity.py`.

**Claim labels.** The rules are the Atlas's design (`INTERPRETATION`), and their
consequences are `IMPLICATION`. What a source says is cited through a claim in `data/`,
never stated here as a fact.

---

## 1. Scope: 15 concepts recorded, 2 gaps (H-1)

**Rule** (D-067). Every v1 concept that `entity-taxonomy.md` §5 maps to `type:technology`
or `type:component` gets a record, unless no source of a class that the row
`identity:technology` or `identity:component` accepts defines it. Such a concept is a
**gap**: it gets no record and is listed in §3 with the reason. It is never defined from a
vendor's marketing (Part B §16).

**Result:** 15 of the 17 concepts have a definitional source of a sufficient class, and give
16 records (SME-03 gives two, §2). Two concepts are gaps:

- **HBM-03, HBM base die.** The only sentence retrieved is Micron's product page
  (`company_marketing`): HBM "stacks multiple DRAM dies vertically atop an optional base
  die". Marketing never defines a class.
- **HBM-04, Through-silicon via.** The ECP report (§6) names TSVs as the connection inside
  an HBM stack, but does not define them. CSET's only "vias" sentence is a footnote about
  slurry materials (src-002 p.96), not a definition of the process.

Both wait on JEDEC JESD238 (HBM3), requested from the human under RA-4 (§6). If it arrives
and defines them, the next session adds the two records by the same rules.

## 2. Keeping distinct concepts apart

The taxonomy separates five pairs (Part B §06 q2). Each record's working definition keeps
its pair apart, and two checks make a merge visible:

| Pair | What keeps them apart | Machine check |
|---|---|---|
| TSV vs HBM stack | TSV is a process (technology), HBM a constituent (component). TSV is a gap in S08, so it cannot be merged into the HBM record: the HBM definition cites the ECP sentence, which names TSVs as the connection, not as the item | DEF-2: no definition claim serves two records |
| 2.5D vs 3D | HIR's 2D-enhanced ("2DS") architecture places dies side by side on an interposer or bridge; its 3D architecture stacks dies "without the agency of the package". Two ATTRIBUTION claims, two working definitions | DEF-2; concept uniqueness |
| Data-centre GPU vs AI ASIC | CSET and LBNL define GPUs and ASICs in separate glossary entries; both records sit under AI accelerator through `broader` | DEF-2; concept uniqueness |
| EUV vs DUV | NIST gives the two wavelengths (13.5 nm and 193 nm). CSET lists EUV and DUV as separate grades of photolithography tool. One SME-03 record would hold both, so S08 splits it (D-070) | the split is listed in §3; every other concept has one record |
| Packaging process vs packaging equipment | Advanced packaging (PKG-03) is a technology; assembly and packaging tools (SME-06) are a component class with `use_class: production_equipment`, under SME (SME-01) | the record kind is read from §5; the kind value from the schema's `x-concepts` |

**What the checks cannot see.** Two definitions written in different words for one concept
pass DEF-2. The human's review (§10) is the check for that. The concept table (§3) limits
the risk, because each record is tied to one taxonomy concept.

## 3. Concept table and IDs (CI-1, machine-checked)

**Rule** (D-068). A technology or component ID is the record type, `-`, and the slug of the
row's **term**: lower-case ASCII words joined by `-`, every run of other characters becoming
one `-`.

- The term is the concept's **name in `entity-taxonomy.md` §5**, which is an accepted
  document. So an ID changes only when the taxonomy changes, by a decision.
- **Split concepts** (D-070): when one concept gives two records, each term uses only words
  of the §5 name, and the row cites the decision.
- **Why not the concept ID** (technology- plus "sme-03"): it is opaque to a reader of an edge.
  **Why not a defining standard's term**: most concepts have no standard in S08, and HIR
  says the "2.x" names "do not have any particular technical basis", so a standard's term
  can disagree with the Atlas's working term.
- **The display name** is free. A test changes one and checks that no ID error appears.

`tests/test_data_entities.py` reads this table. It checks that every §5 concept mapped to
`type:technology` or `type:component` has at least one row; that each row's record type is
the §5 target; that each record exists, with `concept_refs` naming exactly that concept,
and with the `technology_kind` or `use_class` whose `x-concepts` list the concept; and that
no record exists for a gap.

| Concept | Term | Record | Note |
|---|---|---|---|
| ACC-01 | AI accelerator | `component-ai-accelerator` | TQ-01 |
| ACC-02 | Data-centre GPU | `component-data-centre-gpu` | |
| ACC-03 | AI ASIC | `component-ai-asic` | |
| ACC-05 | Multi-die accelerator | `technology-multi-die-accelerator` | TQ-09 |
| HBM-02 | High Bandwidth Memory | `component-high-bandwidth-memory` | |
| HBM-03 | HBM base die | — | gap: no definitional source of a sufficient class (§1) |
| HBM-04 | Through-silicon via | — | gap: no definitional source of a sufficient class (§1) |
| PKG-03 | Advanced packaging | `technology-advanced-packaging` | TQ-03 |
| PKG-04 | 2.5D packaging with an interposer | `technology-2-5d-packaging-with-an-interposer` | |
| PKG-05 | 3D die stacking | `technology-3d-die-stacking` | |
| PKG-06 | Multi-die package | `technology-multi-die-package` | TQ-09 |
| SME-01 | Semiconductor manufacturing equipment | `component-semiconductor-manufacturing-equipment` | |
| SME-03 | EUV lithography | `technology-euv-lithography` | split, D-070 |
| SME-03 | DUV lithography | `technology-duv-lithography` | split, D-070 |
| SME-06 | Assembly, packaging and wafer-level packaging tools | `component-assembly-packaging-and-wafer-level-packaging-tools` | |
| EDA-01 | Electronic design automation | `technology-electronic-design-automation` | |
| DC-02 | Cloud computing | `technology-cloud-computing` | |
| DC-05 | Accelerated server | `component-accelerated-server` | TQ-11 |

## 4. Working definitions (DEF-1, DEF-2, machine-checked)

**Rule** (D-069, H-4). The `definition` of every technology and component is one assertion
citing exactly one claim: the Atlas's **working definition**, an `INTERPRETATION`.

- Its inputs are `ATTRIBUTION` claims, one for each source position (originator
  standing). Where a CON conflict applies, every side's position is an input
  (`source-policy.md` §10.1), and the reasoning names the TQ answer it applies.
- An input may also be another working definition, when the record narrows a broader one
  (the data-centre GPU uses the AI-accelerator working definition).
- `identity_claim_ids` are `ATTRIBUTION` claims among the working definition's inputs:
  the sources that define the concept. So identity and definition cannot drift apart.

**Why always an `INTERPRETATION`, even with one source.** A source's sentence is the
source's position, and the record's text is the Atlas's choice of wording and scope (for
example, "in v1, HBM stacking only"). One rule for all records means the reader never has
to ask which kind of definition a record holds. The cost is one more claim per record.

**Machine checks** (`tests/test_data_entities.py`):

- **DEF-1:** the definition cites one `INTERPRETATION`, and every identity claim is one of
  its inputs.
- **DEF-2:** no claim is the definition of two records, and no concept is in the
  `concept_refs` of two records unless §3 lists the concept twice.
- **V-10** already follows the inputs down to their citations, so a definition resting only
  on marketing fails: `company_marketing` is not a class the definition rows accept.

**The TQ answers applied:**

| Record | TQ | How |
|---|---|---|
| `component-ai-accelerator` | TQ-01 | the S06 working definition, already canonical (`claim-atlas-ai-accelerator-working-definition`) |
| `technology-advanced-packaging` | TQ-03 | narrow: 2.5D interposer integration and HBM die stacking. NIST's and SIA's breadths (CON-04) are both inputs |
| `technology-multi-die-accelerator`, `technology-multi-die-package` | TQ-09 | "multi-die", with "chiplet" only as the sources' word. NIST, SIA and SK hynix (CON-03) are all inputs |
| `component-accelerated-server` | TQ-11 | a server stays a layer-6 component; who integrates servers stays `not_researched` |

TQ-02 ("in-package" HBM) is not used: the HBM working definition states what an HBM stack
is, not where it sits. Placement is an S10 `incorporates` edge.

## 5. `broader` (B-1, machine-checked)

**Rule** (D-071). `broader` records "is a kind of" only where a working definition makes it
so:

| Record | `broader` | Why |
|---|---|---|
| `component-data-centre-gpu`, `component-ai-asic` | `component-ai-accelerator` | TQ-01: an AI accelerator is a GPU or an AI ASIC |
| `component-assembly-packaging-and-wafer-level-packaging-tools` | `component-semiconductor-manufacturing-equipment` | CSET's SME definition includes tools to "assemble, test, and package" |
| `technology-2-5d-packaging-with-an-interposer`, `technology-3d-die-stacking` | `technology-advanced-packaging` | TQ-03's narrow definition names both |

**Not `broader`:**

- **Multi-die package under advanced packaging.** A multi-die package on a mainstream
  organic substrate is not "high interconnect density", so it is not always advanced
  packaging in TQ-03's sense.
- **EUV and DUV under a lithography record.** Lithography (SME-02) is definitional only
  (§5 target `none`), so it has no record.
- **Anything for "requires" or "part of".** Those are S10 edges.

**Machine check (B-1):** every `broader` reference resolves to a record of the same type
(V-1), a canonical record's `broader` is canonical (CE-1), and the graph has no cycle.

## 6. Sources

**New sources** (`src-039` onward). Each was retrieved automatically on 2026-10-01, with
its full hash registered; their texts stay outside the repository (RA-4(4)):

| Source | What | Class | Why this class |
|---|---|---|---|
| `src-039` | IEEE EPS, Heterogeneous Integration Roadmap 2020, Chapter 22 | `research_report` | a technical roadmap by a professional society's committee; not a standard (no standards body adopted it) and not policy research. **Ruling for the human** (D-076) |
| `src-040` | ECP Milestone M1 Report: HBM2/3 Evaluation on Many-core CPU (Sandia, SAND2018-6370R) | `research_report` | a national-laboratory report for the DOE Exascale Computing Project |
| `src-041` | NIST news, "UV Lithography: Taking Extreme Measures" (2011) | `government_publication` | published by NIST on nist.gov about its own work. **Ruling for the human** (D-076): it is a news article, but the agency is its originator |
| `src-042` to `src-045` | re-retrievals of `src-006`, `src-010`, `src-015` and `src-013` | as the originals | their bytes changed (below) |

**A re-retrieval with changed bytes is a new source record** (D-075). A citation's `read`
must be of the bytes its source registers (VD-11, D-062). On 2026-10-01, seven
re-retrieved sources returned their registered bytes (`src-001` to `src-005`, `src-021`,
`src-022`). Six returned changed bytes: `src-006`, `src-010`, `src-013` and `src-015`,
which S08 cites, and `src-007` and `src-017`, which it does not. Rewriting the old
record would orphan its S06 reads (VD-12), so each changed retrieval that S08 cites is a
new record with the same URL, the title marked with the retrieval date, and its own hash.
The old record stays as the home of the old reads.

**The anchor re-check** (`source-policy.md` §12): the S06 claim
`claim-h100-gh100-process-name` was re-read in the new bytes of `src-006` (`src-042`), and
its anchor is still at its locator.

**Access and RA-4** (H-5):

- **JEDEC JESD238 (HBM3)** — free with registration. Registering declares an identity to a
  site, which is the human's decision (RA-7), so the human was asked to download it
  (RA-4) at the start of S08. Not received by the end of S08: HBM-03 and HBM-04 stay gaps.
- **`srcmapt.org`** (the MAPT roadmap) answered with an automated challenge page. Not
  circumvented (RA-2): an access gap.
- **Considered, not registered:** two other NIST pages on EUV (a conference paper on EUV
  metrology and a publication abstract on EUV optics). They describe EUV measurement, not EUV against DUV.

## 7. Products (PI-1, IO-1, machine-checked)

**Scope** (D-072, H-2). Three products, each named in a registered vendor document:

- **NVIDIA H100**, **AWS Trainium2** and **Micron HBM4 36GB 12H**.
- **No ASML product.** ASML's page names product families ("NXE and EXE systems"), and
  families are future scope (`entity-taxonomy.md` §3.5). No single system is named in a
  sentence the Atlas has read.

**ID rule (PI-1).** `product-`, the vendor's company ID without `company-`, `-`, then the
slug of the product's **term**: the product name as the vendor writes it in an identity
anchor, without the vendor's own name. The check recomputes the ID from the record's
`vendor` and this table, and finds the term verbatim in an identity claim's anchor.

**`instance_of` basis (IO-1).** `instance_of` has no claim field in the schema. So each
class a product is an instance of has one row here, naming the claim that supports it. The
check requires a row for every `instance_of` value and a record value for every row. The
record stays the home of the value; the row is its evidence.

| Record | Term | Class | Basis claim |
|---|---|---|---|
| `product-nvidia-h100-tensor-core-gpu` | H100 Tensor Core GPU | `component-data-centre-gpu` | `claim-h100-identity` |
| `product-amazon-com-trainium2` | Trainium2 | `component-ai-asic` | `claim-atlas-trainium2-ai-asic` |
| `product-micron-technology-hbm4-36gb-12h` | HBM4 36GB 12H | `component-high-bandwidth-memory` | `claim-micron-hbm4-identity` |

**Rulings for the human:**

- **The GH100 finding** (D-073). The canonical S06 claim names the **GH100 die** that
  powers the H100, not the H100. The changed page has a sentence about the H100 itself:
  "Using the TSMC 4N fabrication process enables H100…". So the product's
  `vendor_process_name` rests on that new claim (`claim-h100-process-name`), and the GH100
  claim stays about the die. The value is "TSMC 4N", as the H100 sentence names it; the
  GH100 sentence's longer wording ("TSMC 4N process customized for NVIDIA") stays in its
  own claim.
- **Trainium2's vendor** (D-074). AWS's page says Trainium2 is a chip "from AWS". The
  canonical company record `company-amazon-com` carries "Amazon Web Services" and "AWS" as
  aliases, accepted by the human at the S07 review, because the 10-K names AWS as one of
  Amazon's segments. So the vendor is `company-amazon-com`. Which legal entity publishes
  the page is still open (`company-dataset.md` §14), but the vendor field names whose name
  the offering carries, not the publisher. **Flagged for the human:** this is a Part B §16
  stop condition, so the record stays staging until the human rules.
- **Trainium2 as an AI ASIC.** AWS calls Trainium2 a "purpose-built Machine Learning chip",
  not an ASIC. That it is one is the Atlas's reading (`INTERPRETATION`), with CSET's and
  LBNL's ASIC definitions as inputs. **Flagged for the human.**
- **H100 thermal design power.** The page states 700 W for the SXM5 form factor and 350 W
  for PCIe. Those are two separately named models (`entity-taxonomy.md` §3.5). One value for
  "the H100" would merge them, so `tdp_w` is `not_researched` on this record.

**Attribute states:** a chip or a memory product is not a system, so `rated_power_w`,
`rack_scale` and `cooling_method` are `not_applicable` on all three. Every other attribute
without a sentence read is `not_researched`.

## 8. Staging, canonical and the human's review (H-3, H-6)

As D-061, with the layout of H-3 (D-077): one canonical and one staging file per record
type. A record becomes canonical only on the human's verdict, and only if every claim it
cites is canonical. CE-1 extends to the new files: a canonical record cites canonical
claims, and its `broader`, `instance_of` and `vendor` point to canonical records.

## 9. validate-data for concept and product records

`tests/test_data_entities.py` extends the S07 checks (D-077):

| Check | What it adds in S08 |
|---|---|
| V-1 | `broader` resolves to a record of the same type; `instance_of` to a technology or component; `vendor` to a **canonical** company |
| V-9, V-4, V-10 | unchanged, now over the new record kinds and rows |
| CE-1 | `broader`, `instance_of` and `vendor` of a canonical record are canonical; no ID is both staging and canonical in the new files |
| CI-1 | §3's concept table, against §5 and the schema |
| DEF-1, DEF-2 | §4 |
| B-1 | `broader` has no cycle |
| PI-1, IO-1 | §7 |

Freshness (F-1) needs nothing new: every row the new records use is `stable`.

## 10. Review sheet (the human's manual inspection)

For each claim on the sheet in the S08 report:

1. Run `python tools/trace.py <record ID>`.
2. Open the source at the locator and read the whole sentence.
3. Answer:
   - **Each `ATTRIBUTION`:** does the sentence say this, and is the source its
     originator?
   - **Each working definition:** does it stay within its inputs? Does it keep apart the
     concepts of §2? Is the TQ answer applied as you gave it?
   - **Each product value:** does the vendor's sentence say this about this product, and
     not about a die, a family or another model?
4. Give a verdict per claim: accept, reject, or "wording too strong".

The flagged rulings (§6, §7) are asked as separate questions.

## 11. Candidates considered and rejected

| Candidate | Why not |
|---|---|
| IDs from the S01 concept ID (technology- plus "sme-03") | opaque to a reader of an edge (§3) |
| IDs from a standard's term (HIR's "2DS") | no standard for most concepts; it can disagree with the Atlas's working term (§3) |
| One SME-03 record "EUV and DUV lithography" | it would hold two technically distinct processes (§2) |
| Equipment classes for EUV and DUV scanners | no v1 concept asks for them; SME-01 is the top equipment class |
| Defining HBM-03 or HBM-04 from Micron's or SK hynix's pages | marketing never defines a class (Part B §16) |
| A single source's `ATTRIBUTION` as the definition where no conflict exists | two kinds of definition in one field (§4) |
| Rewriting a changed source's hash in its existing record | it would orphan the S06 reads (§6) |
| H100 `tdp_w` = 700 | it is the SXM5 model's value (§7) |
| An ASML EUV system from the families page | a family is not a product (§7) |

## 12. What S08 leaves to other sessions

| Item | Owner | Note |
|---|---|---|
| HBM-03 and HBM-04 records | the session that receives JEDEC JESD238 | §1 |
| H100 SXM5 and PCIe as separate models; product families | a later product session, by decision | §7 |
| `requires`, `has_part`, `incorporates`, `fabricates`, `packages` edges between these records | S10 | the "requires"/"part of" statements read in S08 are candidates: HBM uses TSVs (ECP); 2.5D packaging uses an interposer (HIR) |
| The AWS legal entity behind `src-010` and its re-retrieval | S10 | §7 |
| Who integrates accelerated servers | future (TQ-11) | §4 |
