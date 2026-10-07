# Rules for supplier evidence: proposed revision (S16.6)

**Status:** PROPOSED on 2026-10-07 (S16.6, D-143). No rule changes until the human decides each item (H-1).
**Scope:** the `supplier` of a product's `incorporates` edge, the matrix row `rel:incorporates.supplier`
(`source-policy.md` §7). No other row changes.
**Why** (D-141, D-143):

- both HBM suppliers stayed unknown in S16.5;
- the only product-level party statement is from 2022;
- the sources that do name a supplier are market research, news and teardown labs, which the current row
  never accepts.

**Read with:** `source-policy.md` §2, §4, §7, §9, §12; ER-8 (plans are never states); F-1 (D-064, D-096).

## In short

| Item | What it would do | Changes rules? | Expected effect on the two HBM parts |
|---|---|---|---|
| **R-1 Historical supplier values** | a supplier value may carry an end date (`valid_to`) meaning "supported up to here"; such a value is exempt from the 12-month rule and always shown with its date, never as current | yes: §12 and F-1 | **small on its own.** SK hynix's 2022 release states a plan ("will provide"), and ER-8 never turns a plan into a state. R-1 helps only if a dated statement of actual supply is found |
| **R-2 Independent teardowns** | a teardown report that examined the named product and identified the part's maker becomes acceptable evidence (`research_report`, `originator` standing) | yes: §2's `research_report` row and the matrix row | **potentially decisive**, if a teardown of the H100 or Trainium2 can be retrieved. Most are paywalled, which would make them access gaps (RA-4 needs the human) |
| **R-3 Third-party reports recorded as reported** | "TrendForce reported on 2024-03-13 that …" kept as an `ATTRIBUTION` claim, never as the supplier | **no**: §2 already allows it ("Its own estimates, as `ATTRIBUTION`"; "That the outlet reported something on its date") | the reports become queryable evidence; the supplier field is unchanged |
| **R-4 Where retrieved sources are registered** | the Extractor registers a retrieved source in `data/sources.json` as its contract says, before approval; claims still wait in staging | clarifies a conflict S16.5 found | a source record states only what was retrieved, when, and with what hash. Claims and supplier values still wait for approval |

## R-1 — Historical supplier values

**Problem:**

- F-1 asks every `time_sensitive` value to rest on evidence dated within 12 months of its verification.
  For a product launched in 2022, almost every statement about its supplier is older than that.
- The rule treats "who supplies the part" as a present-tense fact. A dated past fact ("SK hynix supplied
  it in 2023") cannot be recorded at all, even when well sourced.

**Proposed rule** (text for `source-policy.md` §12, under "When evidence is stale"):

> **Historical values of a `time_sensitive` row.** An assertion that carries `valid_to` states what its
> evidence supports up to that date, and nothing about later dates. F-1 does not apply to it. Instead:
>
> - its evidence must be dated no later than `valid_to` plus 12 months;
> - `valid_to` is never later than the evidence date;
> - it must state the past, not a plan (ER-8);
> - every page shows it with its period, in words that cannot read as current (for example "SK hynix,
>   2023 (historical)").
>
> The current state stays a separate question. A field may hold historical values only. A page then says
> "current supplier: not researched" beside them.

**What changes:**

- `source-policy.md` §12 gains the paragraph;
- `tests/test_freshness.py`:
  - exempts assertions with `valid_to` from F-1;
  - adds a check that such an assertion's evidence is dated no later than `valid_to` plus 12 months;
  - adds a check that `valid_to` is not later than the newest evidence date;
- decision D-144.

No schema change: assertions already allow `valid_from` and `valid_to`.

**What it enables:** past supply can be recorded and dated, once a source states it as fact.

**What it limits:** a historical value never answers "who supplies it now". The page must show the period
(H-3 if a value is named).

**Hard to undo?** No: removing the paragraph and its checks restores F-1 everywhere.

**Today's evidence under R-1:** SK hynix's 2022 release (`src-053`) says HBM3 is "to be combined with" the
H100 and that SK hynix "will provide HBM3 for NVIDIA systems expected to ship". Both are plans (ER-8), so
R-1 alone does not name SK hynix.

## R-2 — Independent teardowns as evidence of a product's part maker

**Problem:**

- Only the two parties (the product's vendor and its supplier) can support a supplier today.
- Both often stay silent.
- A teardown lab that opens the product and reads the part's markings or analyses its die observes the
  answer directly. Today, `research_report` is "never sufficient" for "company-specific edges" (§2), and
  the row requires `party` standing.

**Proposed rule:**

> **A teardown of the named product** is `research_report` with `originator` standing. It is
> **acceptable**, not preferred, for `rel:incorporates.supplier` when all of these hold:
>
> - the report names the specific product (model and variant) it examined;
> - it identifies the part's maker from the examined unit (markings, die analysis), not from market
>   reports;
> - it is retrieved and read (RA-1). A paywalled report is an access gap unless the human retrieves it
>   (RA-4);
> - its date is the evidence date.
>
> **What a teardown supports:** the unit examined contained that maker's part, as of the report. It does
> not show that every unit did (multi-sourcing), so the claim says "a unit examined by …". Under R-1 it can
> be a historical value.

**What changes:**

- `source-policy.md`:
  - §2's `research_report` row gains the teardown exception;
  - the matrix row `rel:incorporates.supplier` moves `research_report` from "never sufficient alone" to
    "acceptable";
  - its standing becomes "`party`; `originator` for a teardown";
- `tests/test_source_policy.py`: the standing column accepts the two-value form. §9's test for market
  research and news is **unchanged**: they stay never sufficient alone;
- `tests/test_freshness.py`: reads the row's standings as a set (it already does);
- decision D-145.

**What it enables:** the supplier of a product can be established from direct observation, without the
parties' cooperation.

**What it limits:**

- **One unit, one date.** The claim must not generalise to all units.
- **Access.** Teardowns of current products are mostly commercial and paywalled.

**Hard to undo?** No, but values recorded under it would need re-review if it were withdrawn.

## R-3 — Third-party reports recorded as reported (no rule change)

`source-policy.md` §2 already lets market research support "Its own estimates, as `ATTRIBUTION`", and news
support "That the outlet reported something on its date, as `ATTRIBUTION`". So "TrendForce reported on
2024-03-13 that the H100's HBM3 supply is primarily met by SK hynix" can be a canonical `ATTRIBUTION` claim
once retrieved and verified. It never supports the supplier field (§9, unchanged).

It is listed for information. Each such claim is still approved with the research outcome (H-2).

## R-4 — Where retrieved sources are registered (clarification)

**The conflict:**

- `docs/agents/contracts.md` lets the Extractor write new records to `data/sources.json`. A source record
  states only what was retrieved, when, and with what hash.
- S16.5's prompt forbade any `data/` edit before approval. `data/staging/` has no sources file, so drafts
  lived outside `data/`, and the checks could not see them until promotion.

**Proposed:** the contract governs. A retrieved source is registered in `data/sources.json` when it is
retrieved. Claims and supplier values stay in `data/staging/` until the human's review. Future prompts
must not forbid it.

**What changes:**

- one sentence in `docs/agents/contracts.md` (Extractor) confirming the order;
- decision D-146.

**What it enables:** staged claims cite real source records, so `validate-data` checks them before review.

**What it limits:** sources that end up unused stay registered. That is already the case for retrieval
records.
