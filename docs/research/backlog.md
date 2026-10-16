# Future research backlog — after v1.0

- **Status:** accepted (decided by the human on 2026-10-16, S25 H-3; D-230). Written by the
  Knowledge Architect (D-229).
- **What it is:** each research gap of v1.0's [known limitations](../known-limitations.md) that no planned session
  closes, with the kind of session that would close it and where it could fall in
  [`VERSION-ROADMAP.md`](../../VERSION-ROADMAP.md). It answers D-218's C-8: gaps owned by sessions the roadmap does
  not name.
- **What it is not:** a roadmap change. A row enters `SESSION-ROADMAP.md` only when the human opens v1.5 (S26) or v2
  (S32) and approves it there (D-201). Each row links the gap it would close and restates none of its values.
- **Claim label:** a plan (`INTERPRETATION`).

## 1. Gaps no planned session closes

| ID | Gaps | What the research is | Session kind and roles | Where it could fall | Before it can start |
|---|---|---|---|---|---|
| RB-1 | KL-03, KL-05 | a current, product-level statement of who makes each accelerator's memory, from a source the [source policy](source-policy.md) recognises, or from the parties | RESEARCH: Source Scout, Extractor, Verifier; the human's review | v1.5's measured-data session (S28 in the plan), which reads the same products' primary documents for their memory figures | nothing new: the supplier field and its evidence rules exist ([`supplier-evidence-rules.md`](supplier-evidence-rules.md)) |
| RB-2 | KL-04 | a fresh product-level statement of who fabricates the NVIDIA H100 | RESEARCH, as RB-1 | v2 phase B's foundry session, where fabrication is the subject; or with RB-1 | when the refused candidate is resolved, the HBM page's specification must be updated with it; a test stops the builds by name until then (F-3, D-216) |
| RB-3 | KL-06 | newer company filings for the values marked past the freshness horizon | RESEARCH, small: Extractor, Verifier; the human's review | the first session after v1.0 that reads company filings: S28 or v2 phase B's first session | nothing: the mark goes away by itself when newer evidence is canonical (D-221) |
| RB-4 | KL-07, KL-08 | the official text that dates the Export Administration Regulations, and the BIS guidance a later rule cites, registered and read | RESEARCH (policy): Source Scout, Extractor, Change Detector, Verifier; the human's review | v2 phase C's opening session (global policy), which starts from the policy model; or a short policy session in v1.5 if the human wants v1's export-control page complete first | the later-rule search re-run to the session's day (D-208) |
| RB-5 | KL-02 | a second, independent publisher for each value a page relies on | RESEARCH across the chain, with a review rule | v2, after its opening decides review capacity (`VERSION-ROADMAP.md` §3, item 4) | a decision: whether two independent publishers become a criterion, and what the pages show when only one exists |

## 2. Gaps a planned session or a standing rule already owns

Listed so that the backlog is complete; nothing to place.

| Gaps | Owner |
|---|---|
| KL-01, KL-11 | v2 phase B (finish the first chain) |
| KL-09 | every session that moves the as-of date (D-208) |
| KL-10 | v2's agent activation (D-201) |
| KL-12, KL-13 | v1.5 (search if its opening approves scripts; the concept page) |
| KL-14 | the Verifier, with the human's file, in the session that next relies on those sources (D-218) |
| KL-15 | v1.5's design review (a reading by a person outside the project) |

## 3. Questions for the version openings

Not research gaps, but research directions the audits named:

- **An analysis layer** (portfolio audit P-6): labelled interpretations of what the recorded texts imply, kept apart
  from the facts. This is a decision for v2's opening.
- **The EU lens** (D-008, NG-06): MA's "EU AI compute dependency map" needs a classification of entities that v1
  deliberately left out. This is a decision for v2's opening.
- **Measured values** (`VERSION-ROADMAP.md` §2, item 5): the record kind for a figure with its unit and date. This is
  a decision for v1.5's opening, and RB-1 could share its sources.
