# Policy links: what an export-control text names

**Status:** PROPOSED (H-1 pending). Nothing below changes a schema, a check or a record until the human
decides it item by item.
**Date:** 2026-10-13
**Decided before this proposal** (H-0, 2026-10-13): the first links go from the five export-control records
to the **classes** of parts and technologies their texts name. No named product or company is linked in
this round.
**Inputs:**
- `policy-dataset.md` P-8 (the `restricts` link, D-160), P-9 (LA-1 to LA-5, D-161), P-4 (status, D-156);
- `relationship-taxonomy.md` §1 (RR-1 to RR-10), §2, §5, §9, §10;
- `edge-dataset.md` §1 (the refused-candidate rule), §2 (RI-1), §7 (the evidence guards), §8 (navigation);
- `claim-model.md` §4, §5; `../research/source-policy.md` §4, §6 (ER-1 to ER-10), §7;
- `tools/navigate.py`, `tools/build_page.py`, `tools/build_insight.py`, `tools/warehouse.py`: how they read
  relationships;
- the five official texts (`src-057` to `src-061`), re-retrieved on 2026-10-13. Their bytes match the
  registered SHA-256 hashes.

**Claim labels.** The design is the Atlas's choice (`INTERPRETATION`). Its consequences are `IMPLICATION`.
The passages quoted under "What the texts give" were read on 2026-10-13 to shape the design. They are not
records. Records come only through the search plan, the Verifier's re-read and the human's review (H-2).

---

## In one paragraph

A policy link says one thing: **this act's own text names this class among the items it controls.** For
example, "BIS rule 2024-28270 restricts high-bandwidth memory" means that rule's text says it adds a control
on HBM stacks. The link never says that every HBM stack is controlled, that a given product is, or for which
destinations or under which licence policy. Those limits stay in the text, quoted in the link's claims, and
the reader is sent to the text. Each link rests on two claims:
- an `ATTRIBUTION` quoting the act;
- a `DERIVATION` showing that the act's word and the Atlas record's name are the same kind of thing.

A candidate that fails either is recorded as a refused candidate with its reason. Pages do not show policy
links. The command-line navigation shows them with the act's computed status and a "describes, does not
advise" note.

## What the texts give (design reading, 2026-10-13)

The five texts were searched for the name and aliases of every component and technology record, and for the
names of the nine companies and three products.

- **No text names any of the Atlas's companies or products.** "Micron" appears only as a unit
  ("microns"). This confirms H-0's choice: product and company links would need the parties' own statements.
- **HBM.**
  - 89 FR 96790 (2024-28270), p.10: "BIS is adding a new ECCN control on HBM stacks with a specific memory
    bandwidth density to ECCN 3A090.c."
  - The next page (p.11) sets a threshold and an exclusion: co-packaged logic and HBM chips "are not
    controlled by 3A090.c". It also states that "All HBM stacks currently in production exceed this
    threshold."
  - In 88 FR 73458 (2023-23055), HBM appears only in red flag 19, as a feature of the chips that raise the
    flag. That rule names HBM, but not among the items it controls.
- **Semiconductor manufacturing equipment.**
  - 87 FR 62186 (2022-21658), p.7: "BIS adds to the CCL certain advanced semiconductor manufacturing
    equipment under a new ECCN 3B090".
  - 88 FR 73424 (2023-23049), p.1: it "controls semiconductor manufacturing equipment (SME)". On p.14 it
    "removes ECCN 3B090 and replaces and expands its provisions in ECCNs 3B001 and 3B002". **A later act
    changing the entry an earlier link rests on is therefore a real case, not a hypothesis.**
  - 89 FR 96790, p.1: it adds "new controls for certain semiconductor manufacturing equipment and related
    items".
- **GPUs, ASICs, accelerators.** The 3A090 note in three rules says the integrated circuits it specifies
  "include graphical processing units (GPUs), … co-processors/accelerators, … and application-specific
  integrated circuits (ASICs)". The Atlas's records are narrower: *data-centre* GPU, *AI* ASIC, *AI*
  accelerator.
- **EUV, DUV, EDA.**
  - 88 FR 73424 controls "‘EUV’ pellicles", equipment for EUV masks and for EUV photoresist.
  - 89 FR 96790 controls "less-advanced DUV photolithography equipment" and two kinds of "‘ECAD’
    ‘‘software’’".
  - The Atlas's EUV and DUV records are lithography *technologies* (processes), and its EDA record is the
    class of all chip-design software. The texts control equipment and parts used for the processes, and two
    narrow kinds of design software.

---

## K-1 The level, and which targets are admitted now

**Question.** RR-2 says one verb, one level. The existing levels are:
- **class level:** vendor-neutral classes, evidenced by definitions, no dates;
- **instance level:** named things, evidenced by the parties' documents, with dates.

A policy link starts from a named act, rests on that act's text, and takes its time from the act's events. It
fits neither level.

**Proposal.**
- A third level, **`policy`**, used only by `restricts`:
  - **source:** a policy record;
  - **evidence:** the act's own text (K-6);
  - **time:** none on the link; it comes from the act's events (K-4);
  - **dates on the link:** forbidden.
- RR-2 is amended to name three levels, and RR-9 to admit the policy endpoint of this one type.
- **Targets admitted now:** component and technology, the classes H-0 chose. Product and company targets,
  which D-160 also defines, are admitted by the session that records the first one. That session adds their
  evidence row (a party's own statement) with the data it checks. Until then, the schema refuses them.

**Alternatives.**
- *Two verbs* (`restricts` for classes, another for named things). This keeps RR-2 unamended, but it
  splits one relation in two, although the evidence is the same text.
- *Admit all four targets now.* This is machinery with no used case (A-1, L-09): the matrix row for a
  party's statement would be written before any such statement has been read.

**Consequence.** `schemas/relationships.schema.json` gains `restricts` with `x-level: policy`. The §2 table
in `relationship-taxonomy.md` gains a row.

## K-2 Term matching: when a text's word names an Atlas class

**Proposal.** A link is recorded only when the text's term names **the same class** as the Atlas record:
- the text uses the record's name or one of its aliases ("high-bandwidth memory", "HBM"; "semiconductor
  manufacturing equipment", "SME");
- and nothing in the text makes it a different kind of thing.

Words such as "certain", "specified", "advanced" or a parameter limit *which members* are controlled. They do
not change the class. Those limits are scope (K-3).

**The `DERIVATION`** has two inputs: the `ATTRIBUTION` quoting the act, and the record's working-definition
claim. Its reasoning quotes both words.
- **It may conclude:** "the text's term and the Atlas record name the same kind of part or technology".
- **It must never conclude** that:
  - every member of the class is controlled;
  - a product or firm meets the text's parameters (LA-3);
  - the control applies to any destination, party or transaction;
  - the control is in effect today.

**Refused** (K-7), with the code `term_not_matched`:
- **a broader term:** "GPUs" for *data-centre GPU*; "ASICs" for *AI ASIC*; "co-processors/accelerators" for
  *AI accelerator*. This is ER-9's rule applied to terms: an item is recorded exactly as broad as the source
  says, and "memory" is not "HBM";
- **a narrower term or a related item:** "‘EUV’ pellicles" or EUV mask equipment for the *EUV lithography*
  technology; "DUV photolithography equipment" for the *DUV lithography* technology; two named kinds of
  ECAD software for *electronic design automation*.

**Alternative.** Accept a broader term when the record's definition places the record inside it ("a
data-centre GPU is a GPU"). That would give links from the advanced-computing rules to three accelerator
classes. But each link would then say more than the text: the text names GPUs, and the reader would see
data-centre GPUs. ER-9 already refuses that step for suppliers.

## K-3 Scope stays in the text, not on the link

**Proposal.** **No qualifier.** The parameters, destinations, licence policy and exclusions stay in the act,
quoted where a claim needs them. They never become fields.
- **Forward reading:** "the text of <act> names <class> among the items it controls".
- **Inverse reading,** shown to readers (RR-3): "named among the items controlled by". It replaces MA's
  "restricted by", which reads as a ban.
- **The `ATTRIBUTION`** quotes the sentence that adds or states the control, and names the entry ("ECCN
  3A090.c") as its locator. It does not paraphrase the threshold.

**Alternative.** A `scope` qualifier (parameters, destinations, licence policy). It would copy legal content
into fields (D-023; governance belongs to the other repositories), go stale with every amending rule, and
invite the threshold comparisons LA-3 forbids.

## K-4 Time: a link has no dates; later changes are attributed, never guessed

**Proposal.**
- **No dates on the link.** It states what the act's text says, which never changes. When the act took
  effect, and whether a repeal is recorded, come from `tools/policy_status.py`. Navigation prints that status
  beside the link.
- **A later act that the Atlas holds and that changes the same entry** is recorded as one more `ATTRIBUTION`
  claim cited by the earlier link, quoting the later text. Example: the 2022 → SME link cites 2023-23049's
  "removes ECCN 3B090 and replaces and expands its provisions in ECCNs 3B001 and 3B002". The reader then
  sees both texts. Neither is rewritten as "no longer controlled".
- **How later changes are found:** each later act the Atlas holds is searched for the entry's identifier
  (for example "3B090"), and the search is logged. Acts the Atlas does not hold are not searched. That
  limitation is recorded as debt (for the M5 audit, with S17's repeal-search debt).
- **Unchanged:** an amendment of one entry is not a repeal of the act. The act's status does not move
  (P-4).

**Alternatives.**
- *A `valid_to` on the link*, set from the later act: an end date the Atlas infers.
- *Refusing the earlier link*: it would lose the fact that the 2022 text named the equipment.
- *An event per entry change*: P-4 rejected events per provision (D-023).

## K-5 Jurisdictions: no relationship needed

**Proposal.** None in S18.
- A policy's issuing country is its `issued_in` field. A link would restate it (RR-4).
- The destinations a control names (the PRC, Macau, country groups) are scope (K-3). "Restricts exports to a
  country" would be a different relation, with its own evidence rule. It is not defined, and not needed for
  any question S18 answers.

## K-6 The source-policy row `rel:restricts`

**Proposal.** A 48th row:

| Row | Preferred | Acceptable | Never sufficient alone | Standing | Freshness |
|---|---|---|---|---|---|
| `rel:restricts` | `official_legal_text` | none | the other eleven classes | originator | stable |

- **Stable:** a published text never changes. Whether the act still has effect is computed (K-4).
- **Never sufficient alone:** a press release, a law firm's summary or a news article never supports a
  link. They may point to a passage.
- **When product or company targets come** (K-1), the session that admits them revisits this row for a
  party's statement.
- **Unchanged:** `PL-8`'s rule that rows existing before S17 never rest on legal text alone. The new row is
  added to the policy rows that prefer it.

## K-7 Refused candidates

**Proposal.** Recorded as S10 did (D-109), in `data/refused_candidates.json`. The schema changes so that:
- `restricts` is an allowed relation type of a candidate;
- a policy may be a candidate's source;
- two reason codes are added:
  - **`term_not_matched`**: the text's term does not name the same class as the record. It is broader,
    narrower, or names an item used for it (K-2);
  - **`applies_a_threshold`**: the candidate would need the Atlas to apply a threshold, definition or
    exemption to a product or firm (LA-3).

The existing **`relation_not_stated`** covers a text that names a class without controlling it (the HBM red
flag in 2023-23055), and a text describing another act's control.

**One product candidate is recorded as refused** although H-0 chose classes. 89 FR 96790 states that "All HBM
stacks currently in production exceed this threshold", and the Atlas holds Micron's HBM4 36GB 12H. Linking
them would be the Atlas applying the threshold. The refusal records the rule at the exact place a reader would
be tempted.

## K-8 Pages and navigation

**Proposal.**
- **Pages show no policy link,** since no page design is approved.
  - The research page's walk follows `incorporates` and `requires`, and its actors are activity edges, so
    `restricts` is never read.
  - The SQL queries filter by relation type, so their results are unchanged.
  - The pages are still rebuilt, because their input digests change. The source-age reference date moves to
    2026-10-13 at that rebuild (D-137).
  - A check fails if a built page contains a policy link's ID or a policy record's ID.
- **Navigation** (`tools/navigate.py`):
  - reads `policies.json`, so `edges` and `evidence` resolve both ends of a link;
  - `depends-on`, `suppliers` and `actors` never include `restricts`. It is neither a dependency nor an
    activity;
  - `edges` prints each policy link with its inverse reading, the act's status today
    (`tools/policy_status.py`), the official text's URL, and the line "describes the text; does not advise"
    (LA-5).
- This repairs the known interaction (S17-11): `test_every_edge_is_navigable` failed because navigation did
  not read policy records.

## K-9 Checks, written first

| Check | What fails | Test |
|---|---|---|
| PK-1 | a `restricts` record whose source is not a policy, or whose target is not a component or technology; dates, `item` or `supplier` on it; a level other than `policy` | `tests/test_policy_layer.py` (schema) |
| PK-2 | any relationship with a policy endpoint other than `restricts` from its source; a `restricts` from a `proposed_rule` (a proposal never takes effect) | `tests/test_policy_layer.py` (replaces PL-9) |
| PK-3 | a link that does not cite at least one `ATTRIBUTION` resting only on its own act's official text (the source its identity claims cite), with originator standing, and one `DERIVATION` whose inputs are such an `ATTRIBUTION` and the target's working-definition claim; a link citing a `FACT`; an `ATTRIBUTION` on a link that rests on anything but the official text of an act the Atlas holds | `tests/test_data_relationships.py` |
| PK-4 | a link whose own-act anchors never carry the target's name or an alias, or whose `DERIVATION` reasoning does not quote it (the term guard; guards, not proof, as `edge-dataset.md` §7) | `tests/test_data_relationships.py` |
| PK-5 | the `rel:restricts` row missing, or preferring anything but `official_legal_text`, or not `originator` | `tests/test_policy_layer.py`, `tests/test_source_policy.py` |
| PK-6 | a built page containing a policy link's or a policy's ID; `depends-on` or `actors` returning a `restricts` link; `edges` on a policy link without the status line and the LA-5 note | `tests/test_page.py`, `tests/test_insight.py`, `tests/test_navigate.py` |
| PK-7 | a refused `restricts` candidate whose source is not a policy; the two new reason codes undefined | `tests/test_data_candidates.py` (with RC-1 to RC-8) |

**Existing checks that apply unchanged:**
- V-1 (references resolve), V-3 (no self edges), V-5 (no duplicates), V-9 (no placeholders);
- V-10 (the citation's class and standing against `rel:restricts`);
- RI-1 (the ID rule: `rel-policy-us-fr-2024-28270-restricts-component-high-bandwidth-memory`);
- PE-1 (a `DERIVATION` satisfies it);
- RV-1, with a new word row for `restricts`: "control", "controls", "controlled", "restrict";
- CE-1 (canonical links rest on canonical claims).

**Breaks** (`S18-…`): one planted fault per check above, plus a control.

---

## What S18 would then record (expected from the reading above; decided at H-2)

| Candidate | Expected outcome | Why |
|---|---|---|
| 2024-28270 → high-bandwidth memory | link | "a new ECCN control on HBM stacks" |
| 2022-21658 → semiconductor manufacturing equipment | link, citing the later removal of 3B090 (K-4) | "certain advanced semiconductor manufacturing equipment under a new ECCN 3B090" |
| 2023-23049 → semiconductor manufacturing equipment | link | "controls semiconductor manufacturing equipment (SME)" |
| 2024-28270 → semiconductor manufacturing equipment | link | "new controls for certain semiconductor manufacturing equipment" |
| 2023-23055 → high-bandwidth memory | refused, `relation_not_stated` | HBM only as a red-flag feature |
| 2023-23055 → semiconductor manufacturing equipment | refused, `relation_not_stated` | the sentence describes the 2022 rule's control |
| 2022, 2023-23055, 2024 → data-centre GPU, AI ASIC, AI accelerator | refused, `term_not_matched` | broader terms |
| 2023-23049, 2024 → EUV lithography; 2024 → DUV lithography | refused, `term_not_matched` | equipment and parts for the process |
| 2024 → electronic design automation | refused, `term_not_matched` | two narrow kinds of ECAD software |
| 2024 → Micron HBM4 36GB 12H | refused, `applies_a_threshold` | LA-3 |
| the EAR (part 730) → anything | no candidate | part 730 names no item |

Each one is researched, anchored in re-hashed bytes and put to the human at H-2. The table is a forecast,
not a record.

## Rulings (H-1)

Pending.
