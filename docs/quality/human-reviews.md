# Human review record

This file is the durable record of the human's reviews of real claims (`CLAUDE.md` §9, class C). A claim
becomes canonical only on the human's verdict (`docs/architecture/claim-model.md` §7). Each canonical claim's
`review` names its verdict, the reviewer, the date, and in `recorded_in` the entry below that holds the review:
`docs/quality/human-reviews.md#<entry>`. The entry's anchor ends with the review date, which equals the
claim's `reviewed_on`.

Each entry states what was put to the human, the question each claim was read against, the outcome, and what
the outcome changed in the data. It records outcomes in project terms; it does not quote the human or copy
the questions as asked (`SESSION-PROMPT-SPEC.md` §9). Which claims an entry covers is not listed here: it is
the set of claims in `data/claims.json` whose `recorded_in` names the entry, and
`tests/test_human_reviews.py` checks that every claim resolves to an entry, that the dates agree, and that
each entry's claim count below is the count in the data.

**The review question** (`claim-model.md` §14; the edge form in `edge-dataset.md` §9). For each claim, the
human opens the source at the locator, finds the anchor, reads the whole sentence and asks: **does it say
this, and no more?** A working definition (`INTERPRETATION`) is read against its inputs: **does it stay
within them, and keep apart the concepts it must?** A relationship is read as: **does the sentence state this
relation, about this item, and no more?** The verdict per claim is **accept**, **reject** or **wording too
strong** (the last makes the Verifier set `partial` and the Extractor propose a narrowed claim). A batch
verdict covers only the claims the human was shown.

To list an entry's claims with their sources, locators and anchors, run `python tools/trace.py <claim ID>`
on each claim whose `recorded_in` names it, or query `claims.review_recorded_in` in the SQL layer
(`docs/architecture/sql-layer.md`).

| Entry | Date | Claims | Verdict |
|---|---|---|---|
| [Companies and jurisdictions](#companies-and-jurisdictions-2026-10-01) | 2026-10-01 | 62 | all accepted |
| [Technologies, components and products](#technologies-components-and-products-2026-10-01) | 2026-10-01 | 33 | all accepted |
| [Facilities, events and the held concept claims](#facilities-events-and-the-held-concept-claims-2026-10-02) | 2026-10-02 | 19 | all accepted |
| [First relationships](#first-relationships-2026-10-02) | 2026-10-02 | 6 | all accepted |
| [SK hynix HBM3 statement](#sk-hynix-hbm3-statement-2026-10-07) | 2026-10-07 | 1 | accepted |
| [Third-party supplier reports and Samsung Electronics](#third-party-supplier-reports-and-samsung-electronics-2026-10-07) | 2026-10-07 | 6 | all accepted |
| [Export-control records](#export-control-records-2026-10-08) | 2026-10-08 | 37 | all accepted |

No claim has been rejected or found "wording too strong" at review.

---

## Companies and jurisdictions, 2026-10-01

- **Reviewer:** the human. **Claims:** 62. **Verdict:** all accepted.
- **What was reviewed**, on two sheets and one follow-up:
  - the claims staged for seven companies (NVIDIA, Micron Technology, Amkor Technology, Synopsys, Amazon,
    ASML, SK hynix): legal names, roles and identity values, each from the company's own filing;
  - the ten seed claims of the claim model (`claim-model.md` §14), confirmed separately as covered;
  - the claims on the ISO 3166 evidence, the state-to-country steps (`DERIVATION`) and TSMC's records,
    including the step from the filing's "R.O.C." to the ISO 3166 entry TW, flagged as the sensitive one.
- **Spot-check of attested anchors** (`company-dataset.md` §7): the human opened three claims at their
  locators and found each anchor and sentence as stated: `claim-micron-registrant-name` (`src-025` p.1),
  `claim-nvidia-fabless-strategy` (`src-024` p.8) and `claim-asml-incorporated-netherlands` (`src-029`
  p.309). The ISO 3166 screenshots are the human's own captures, taken on 2026-10-01.
- **What changed:** the claims moved unchanged to `data/claims.json`; the eight company records and the
  four jurisdiction records (`jurisdiction-us`, `-nl`, `-kr`, `-tw`) became canonical, the companies with
  their `incorporated_in` and `headquartered_in` values (SK hynix: `headquartered_in` only) (D-061, D-065).
- **Decided at the same review:** D-054 to D-066 and the M1 audit, accepted.

## Technologies, components and products, 2026-10-01

- **Reviewer:** the human. **Claims:** 33. **Verdict:** all accepted.
- **What was reviewed:** the technology and component records with their claims and working definitions,
  and the three product records (NVIDIA H100, AWS Trainium2, Micron HBM4 36GB 12H), with the flagged ruling that
  Trainium2's vendor is Amazon and that Trainium2 is an AI ASIC.
- **What changed:** 33 claims and 14 records became canonical; D-074 accepted. HBM-03 and HBM-04 were
  recorded as gaps (D-067), because the standard they needed had not been received.
- **Held:** nine claims the human also accepted at this review rested on two rulings not yet approved (the
  EUV/DUV split, D-070; the classes of `src-039` and `src-041`, D-076). They stayed in staging, with the
  five technology records resting on them, until those rulings were approved; they are recorded in the
  next entry.
- **Decided afterwards** (2026-10-02): D-067 to D-069, D-071 to D-073, D-075 and D-077, accepted.

## Facilities, events and the held concept claims, 2026-10-02

- **Reviewer:** the human. **Claims:** 19. **Verdict:** all accepted.
- **What was reviewed:**
  - ten staged claims on two facilities (Micron's Manassas fab, SK hynix's M16) and four dated events,
    with the flagged rulings on what counts as a fab (D-081), how a completion is recorded and who is the
    subject of a planned site's announcement (D-083), and clause-only anchors (D-080);
  - the nine claims held at the previous review: the four citing `src-039` (HIR) or `src-041` (NIST news)
    and the five working definitions that take them as inputs. Their verdict had been given on 2026-10-01;
    they became canonical on this date, when D-070 and D-076 were approved.
- **What changed:** the 19 claims moved to `data/claims.json`; the two facilities and four events became
  canonical; the five held technology records (advanced packaging, 2.5D packaging, 3D die stacking, EUV and
  DUV lithography) moved to `data/technologies.json`. TSMC's sites were recorded as a gap. Staging was empty.
- **Decided at the same review:** D-070, D-076, D-078 to D-088, accepted.

## First relationships, 2026-10-02

- **Reviewer:** the human. **Claims:** 6. **Verdict:** all accepted.
- **What was reviewed:** five edges and the claims they cite: the H100 and Trainium2 each `incorporates`
  HBM (supplier then `not_researched`); Amazon `designs` Trainium2; and two flagged edges, SK hynix
  `operates` M16 (D-099) and HBM `requires` 3D die stacking (D-091), each resting on a `DERIVATION`. Also
  `claim-tsmc-fabricates-h100`, a `DERIVATION` kept out of the edges by the freshness rule F-1 (D-092):
  accepting it made the claim canonical, not an edge. The refused candidates were shown with their
  sentences and reasons (`edge-dataset.md` §1).
- **What changed:** the six claims moved to `data/claims.json` and the five edges to
  `data/relationships.json`; TSMC's annual filing was recorded as a gap. Staging was empty.
- **Decided at the same review:** D-089 to D-099, accepted.

## SK hynix HBM3 statement, 2026-10-07

- **Reviewer:** the human. **Claims:** 1. **Verdict:** accepted.
- **What was reviewed:** `claim-sk-hynix-hbm3-for-h100-2022` (`FACT`, party), SK hynix's statement of
  2022-06-08 that its HBM3 was to be combined with the NVIDIA H100, with its source `src-053`. It is older
  than the 12-month horizon at verification, so F-1 refuses it as the H100's supplier value; the review
  kept it as canonical evidence linked to no edge
  ([`hbm-supplier-research-original-rules.md`](../research/hbm-supplier-research-original-rules.md)).
- **What changed:** the claim and its source became canonical; both HBM suppliers stayed `not_researched`.
- **Decided at the same review:** D-141, accepted.

## Third-party supplier reports and Samsung Electronics, 2026-10-07

- **Reviewer:** the human. **Claims:** 6. **Verdict:** all accepted.
- **What was reviewed**, under the supplier-evidence rules decided the same day
  ([`supplier-evidence-rules.md`](../research/supplier-evidence-rules.md); D-144 to D-147):
  - TrendForce's statement (2024-03-13) that the H100's HBM3 supply was primarily met by SK hynix, and
    SemiAnalysis's statement (2025-12-04) that Trainium2's memory was supplied by Samsung, each an
    `ATTRIBUTION` with the third-party criteria judged per citation (`source-policy.md` §7.1); SemiAnalysis's
    recognition criterion is recorded as not met;
  - a company record for Samsung Electronics, with four claims from its 2025 Business Report: legal name,
    head office, country (`DERIVATION`) and memory products.
- **What changed:** the six claims and `company-samsung-electronics-co-ltd` became canonical; the H100's
  HBM `supplier` became SK hynix, historical to 2024-03, and Trainium2's became Samsung Electronics, both
  shown as "reported" (D-148); the refused memory-supplier card links Samsung's record (D-149)
  ([`hbm-supplier-research.md`](../research/hbm-supplier-research.md)).
- **Decided at the same review:** D-144 to D-149, accepted.

## Export-control records, 2026-10-08

- **Reviewer:** the human. **Claims:** 37. **Verdict:** all accepted, record by record.
- **What was reviewed**, under the policy-layer design decided the same day
  ([`policy-dataset.md`](../architecture/policy-dataset.md); D-154 to D-164), from a review sheet giving each
  claim's statement, page, verbatim anchor and the link to the official PDF on govinfo.gov
  ([search log](../research/search-logs/policy-instruments/search-log.md)):
  - the Export Administration Regulations as a whole, three claims from the 2026 edition of 15 CFR part 730:
    what "the EAR" refers to, their issuer, and the laws they are issued under;
  - four rules of the Bureau of Industry and Security in the Federal Register (2022-21658, 2023-23055,
    2023-23049, 2024-28270), each with its title and agency, citation, document number, form, the EAR parts it
    amends, its kind of measure, its country and its dates (publication, and every effective date its text
    fixes);
  - five points were flagged for the human first: three rules' country joins the rule's AGENCY line with the
    EAR's statement that BIS belongs to the United States Department of Commerce; the citation is written
    "87 FR 62186" from the volume and page printed; the EAR record has no dates; one 2023 instruction is
    effective only until 2026-01-01, which no event can hold; the 2024 rule's kind of measure joins its
    SUMMARY with the EAR's statement.
- **What changed:** the 37 claims and the five policy records (`policy-us-15-cfr-730-774`,
  `policy-us-fr-2022-21658`, `policy-us-fr-2023-23055`, `policy-us-fr-2023-23049`, `policy-us-fr-2024-28270`)
  became canonical, with eleven events: four publications and seven effective dates. No policy record is
  linked to a company, part or technology (S18).
- **Decided at the same review:** none; the design rulings D-153 to D-164 were taken earlier the same day.
