# Claim model — how the Atlas records what supports a statement

**Status:** ACCEPTED (human review of S06, 2026-09-30: "Approve all"): D-044 to D-053.
**Session:** S06 · **Date:** 2026-09-30
**Inputs:**
- `../research/source-policy.md` §4 (standing and chains), §5 (separate axes), §6 (ER-1 to
  ER-10), §7 (matrix), §8 (classes of the registered sources), §10 (conflicts), §12
  (dates), §16 (handoff);
- `entity-taxonomy.md` §7 (attribute contract); `relationship-taxonomy.md` §9, §12, §15;
- `../research/source-register.md`; `../research/domain-map.md` "How to read this map";
- MA §5.2–5.3, §5.6–5.7, §10–§16; PEF §6–§7; D-010, D-015, D-018, D-025, D-026, D-028,
  D-031, D-034 to D-043.

**Schemas:** [`schemas/claims.schema.json`](../../schemas/claims.schema.json) (the claim
record) and [`schemas/sources.schema.json`](../../schemas/sources.schema.json) (the source
record, around the S05 class vocabulary).
**Data:** [`data/sources.json`](../../data/sources.json) (canonical source records) and
[`data/staging/claims.json`](../../data/staging/claims.json) (claims awaiting the human's
review). `data/claims.json` is created when the first claim is accepted (H-2).

**One home for each kind of statement:**

- **The schemas** hold the record shapes and every vocabulary value, each with a one-line
  definition.
- **This document** holds the reasoning:
  - what a claim is;
  - how MA §10's lists map onto the vocabularies;
  - the rules that combine claim type and evidence status (§4, read by the tests);
  - what `verified` and canonical mean;
  - the search record;
  - the migration;
  - the checks that make up `validate-data`.
- **Not here.** What a source class is for, standing, the evidence rules, the matrix and the
  conflict kinds stay in `source-policy.md`. This document cites them by section and never
  restates them.
- `tests/test_claim_model.py`, `tests/test_claim_schema.py` and the `validate-data` tests
  check the tables against the schemas, MA and the data.

**Claim labels.** The model is the Atlas's design (`INTERPRETATION`), and its consequences
are `IMPLICATION`. What a real source says is cited through a claim record in `data/`, or
through its register ID and locator.

---

## 1. What a claim is

- **One proposition, stated once.** A claim is one statement in the Atlas's words, with
  what supports it. Several sources may support the same proposition. Each is a citation
  on the one claim, not a second claim. Corroboration still needs independent publishers
  (ER-7): two citations from one publisher are one voice.
- **The link runs from records to claims** (D-044). Entities hold `identity_claim_ids` and
  assertion `claim_ids`; relationships hold `claim_ids` (D-025, D-028). A claim never lists
  the records it supports: that would be a second home for the same link. "Which records
  cite this claim?" is computed by scanning the records (the trace does it, §12).
- **Claims point to claims in one direction too.** A `DERIVATION`, `INTERPRETATION` or
  `IMPLICATION` lists its `input_claim_ids`. An input never lists what is derived from it.
- **The matrix row is derived, not stored.** Which row of `source-policy.md` §7 a claim is
  judged against depends on the record and field that cite it. One claim can support two
  fields with different rows. So the row is read from the citing record (V-10, §11). A
  `matrix_row` field on the claim would be a second home, and the schema rejects it.
- **The claim ID format** stays `claim-<slug>` (D-025). Nothing in S06 needed a change, so
  `entities.schema.json` is untouched.

## 2. Claim types (MA §10 reconciled)

The schema has five claim types and five evidence statuses. The claim types are the
labels of CLAUDE.md §6, written as CLAUDE.md writes them: `FACT`, `ATTRIBUTION`,
`DERIVATION`, `INTERPRETATION` and `IMPLICATION`. Their definitions are in the schema.

MA §10 lists seven claim types "at minimum". Each has one disposition. MA is not edited.

| MA §10 claim type | Disposition | Why |
|---|---|---|
| law / normative text | reserved: the policy layer (S17) | No v1 record states a rule. When S17 starts, it decides whether a normative text needs its own type or is an `ATTRIBUTION` to the issuing authority |
| fact | `FACT` | The same idea. The Atlas adds the condition that the source is first-hand (§4) |
| derived | `DERIVATION` | The same idea. MA also lists "derived" as an evidence status; that one is dropped (§3) |
| attributed | `ATTRIBUTION` | The same idea |
| interpretation | `INTERPRETATION` | The same idea |
| critique | `ATTRIBUTION` for a named source's critique; `INTERPRETATION` for the Atlas's own | Whose critique it is decides the type. The Verifier's source-quality notes (e.g. domain map §5's "looks like a typographical error") are the Atlas's own |
| forecast | `ATTRIBUTION` for a third party's forecast or a company's plan (ER-8); the Atlas's own forecast is out of scope (`NG-11`) | A forecast is always someone's. The Atlas makes no forecasts before S15 defines a question and denominator |

`IMPLICATION` has no MA counterpart. It comes from CLAUDE.md §6: a consequence for the
project, such as what a data gap means for a later session. It is not a forecast about the
world.

## 3. Evidence status (MA §10 reconciled)

Evidence status says how well the evidence supports a claim, after verification. It is a
separate field from claim type (L-06; `source-policy.md` §5). It never holds a number.

MA §10 lists six evidence statuses "at minimum". Each has one disposition.

| MA §10 evidence status | Disposition | Why |
|---|---|---|
| direct | renamed `supported` | "Direct" reads like first-hand, which is standing's job (`source-policy.md` §4). It also cannot describe a derivation. `supported` means the Verifier found the anchor and the wording does not exceed it, or that every input is supported and the step follows |
| partial | `partial` | The wording exceeds the evidence. The claim must be narrowed before any record rests on it |
| derived | dropped: `DERIVATION` is a claim type | Keeping it would give "derived" two homes (L-06). A derivation's strength comes from its inputs (§4) |
| context-only | `context_only` | The cited locators do not state the proposition. It supports nothing (ER-10) |
| unverified | `unverified` | Written explicitly. A missing status is invalid, never read as `unverified` |
| disputed | `disputed` | Only for a factual contradiction (`source-policy.md` §10.1), and it names the competing claims |

**MA §5.7's `verified` and `disputed`.** `verified` is not a value. A claim is verified
when its status is anything other than `unverified`, and it then carries `verified_on`
(§6). `disputed` is the evidence status above. Neither is an attribute state: those stay
`not_researched`, `not_publicly_determinable` and `not_applicable` (D-025).

**Why `disputed` is narrow.** The conflict kinds in `source-policy.md` §10.1 are recorded
in different ways. Only a factual contradiction leaves two claims that cannot both hold:

- a definitional or wording conflict gives one `ATTRIBUTION` per source, and each is true
  as an attribution;
- a temporal conflict gives dated assertions;
- a scope conflict records each claim's scope.

So `disputed` is allowed on `FACT` and `DERIVATION` only. A disputed claim names its
competitors in `disputed_with`, and each competitor names it back (VD-7). No status ever
replaces the competing claims.

## 4. Rules by type and status (machine-checked)

The schema enforces these tables on each record. `tests/test_claim_schema.py` builds a probe
record for every type and status, and checks that the schema accepts it exactly when the
table does. The data checks read the second table.

**By claim type.**

| Type | Sources | Input claims | Standing | Reasoning | as_of | Statuses |
|---|---|---|---|---|---|---|
| `FACT` | required | forbidden | `party`, `originator` | forbidden | required | `unverified`, `supported`, `partial`, `context_only`, `disputed` |
| `ATTRIBUTION` | required | forbidden | `party`, `originator`, `reporter` | forbidden | required | `unverified`, `supported`, `partial`, `context_only` |
| `DERIVATION` | forbidden | required (or a search record, §8) | — | required | forbidden | `unverified`, `supported`, `partial`, `disputed` |
| `INTERPRETATION` | forbidden | required | — | required | forbidden | `unverified`, `supported`, `partial` |
| `IMPLICATION` | forbidden | required | — | required | forbidden | `unverified`, `supported`, `partial` |

How to read it:

- **A claim either cites sources or rests on claims, never both.** A derivation that cited
  a source directly would look like a sourced fact. Its sources are reached through its
  inputs.
- **`FACT` needs first-hand standing.** A `reporter` citation supports at most
  `ATTRIBUTION` (ER-4, ER-6).
- **`as_of` belongs to claims that cite sources.** A claim with inputs takes its dates
  from them, so storing one would be a second home.
- **`context_only` needs cited locators**, so only claims that cite sources can have it.
- **`disputed`** is explained in §3.
- **Which class the sources must have is judged on the record.** A `FACT` must also cite a
  preferred or acceptable class for the citing record's matrix row (`source-policy.md`
  §5). The row is known only on the record (§1), so V-10 checks it there. What can be
  checked on the claim alone is VD-10: at least one cited class is sufficient for some
  row.

**By status.** Whether a claim with this status may be canonical, and which statuses its
input claims may have. This is "no stronger than its weakest input".

| Status | Canonical | Inputs may be | Set by |
|---|---|---|---|
| `supported` | yes | `supported` | Verifier |
| `disputed` | yes | `supported`, `disputed` | Verifier, when it flags a factual contradiction; closing it is the human's (`source-policy.md` §10.1) |
| `partial` | no | `supported`, `disputed`, `partial` | Verifier |
| `context_only` | no | none: only claims that cite sources have it | Verifier |
| `unverified` | no | any | Extractor |

## 5. Citations, standing and chains

A citation records one source at one locator (schema `$defs/citation`, D-047):

- **`source_id`:** a source record in `data/sources.json`. A register label (`SRC-006`) is
  not accepted; its record is `src-006` (§9).
- **`locator`:** the PDF page index (`p.N`, as the register defines it) or, for HTML, the
  section heading and the opening words of the sentence.
- **`anchor`:** a verbatim extract of that sentence, including the source's own quotation
  marks and apostrophes. It is required for every citation. A figure or a table with no
  quotable text cannot be cited in v1. It is recorded as a gap until a decision defines
  another anchor.
- **`standing`:** `party`, `originator` or `reporter`, as `source-policy.md` §4 defines
  them. It is per citation, because one source can be party to one claim and reporter for
  the next (D-035).
- **`originator`:** required exactly when the standing is `reporter`. It is the chain of
  ER-6: who the reporter names, the class that originator's statement would have, and
  where the reporter names it. The originator was not retrieved, so it gets no source
  record and is never cited as if it had been.
- **`read`:** the access time and SHA-256 of the bytes the Verifier read (§6). Required
  exactly when the claim is verified.

**The sentence, not only the anchor, is what is judged.** The anchor pins where the
evidence is. The Verifier, and the human in the manual test (§14), read the whole sentence
at the locator and ask whether the statement says more than it. The machine checks that
the anchor text matches its home (VD-11). Only a reader can judge the wording.

**Anchors from manual retrieval** (RA-4). The full text stays outside the repository. The
source record keeps the URL, the method `manual_by_human`, the download time and the
hash. The citation keeps the locator and the anchor. The Verifier reads the file the human
supplies, and records its hash in `read`. The anchor cannot be machine-checked against a
text in the repository. VD-11 therefore reports it as having no machine-checkable home,
until a decision says how such anchors are recorded (§16).

## 6. What `verified` means

**Decision (D-048).** D-015's second part is **confirmed and extended**.

- **For a claim that cites sources**, verified means: the Verifier re-read each cited
  source at its locator, found the anchor, read the sentence around it, and judged whether
  the statement exceeds it. The outcome is the status (`supported`, `partial` or
  `context_only`). `verified_on` records the date, and each citation's `read` records the
  bytes read.
- **For a claim with inputs**, verified means: the Verifier checked that every input
  exists and has an allowed status (§4), and that the stated step (`reasoning`) follows
  from the inputs. For example, ER-1 really applies, and the working definition cites
  every side of the conflict.
- **Verified is not reviewed.** As D-015 said, it does not mean human review or canonical
  status. The Verifier may verify, downgrade or reject a claim. It may never write a
  review verdict, and never invent replacement evidence (MA §11.4).
- **Per record, never a batch stamp** (L-06). Each claim has its own `verified_on`, and
  each citation its own `read`. A byte change in a source triggers a re-check of the
  anchors that rest on it (`source-policy.md` §12). It does not by itself change any
  status.

**What the human's review adds** (CLAUDE.md §9, class C): the decision that a real claim
becomes canonical. The Verifier's check is necessary for that, never sufficient.

## 7. Staging, canonical and the human's review

MA §16 runs raw evidence → staging → verification → canonical. MA §5.6 forbids an
overloaded status field. The simplest mechanism that never lets an unreviewed real claim
look canonical has two parts (D-048):

- **Where a claim is.** An unreviewed claim is in `data/staging/claims.json`. A canonical
  claim is in `data/claims.json` (H-2). A consumer that reads only `data/claims.json`
  cannot see a staging claim.
- **Why it is there.** Every claim carries `review`. It is either `not_reviewed`, or a
  verdict (`accepted` or `rejected`) with `reviewer: human`, the date, and the session
  report whose addendum holds the human's words.

The checks tie the two together (VD-8):

- every canonical claim is `accepted` by the human, and its status is `supported` or
  `disputed`;
- a canonical claim rests only on canonical claims;
- no staging claim carries an `accepted` verdict.

**What changes when the human reviews a claim:**

- **Accepted:** `review` gets the verdict, and the claim moves unchanged to
  `data/claims.json`.
- **Rejected:** the verdict is recorded and the claim stays in staging, so the evidence is
  not lost.
- **Wording too strong:** the Verifier sets `partial`, and the Extractor proposes a
  narrowed claim with a new ID.

No agent role writes a verdict (`docs/agents/contracts.md`).

## 8. `not_publicly_determinable`: the search record

**Where it lives** (D-049). It is a `search` block on a `DERIVATION` claim. The claim
concludes that a value is `not_publicly_determinable` or `not_researched`, from a recorded
search. The block records what ER-3 requires:

- the question;
- the date;
- each class searched, with the sources consulted, or the access gap that stopped it;
- the conclusion.

**Why not a claim type or a separate record.** The conclusion is an inference from a
search: "no preferred source states this" is the Atlas's reasoning, not any source's
statement. That makes it a `DERIVATION`. A separate record kind would be machinery for one
field (M0 audit A-1). The block exists now because the accepted schemas already require
`not_publicly_determinable` to cite claims (D-025, D-031). Without it, that state would
have nothing valid to cite.

**What the schema checks.** A `not_publicly_determinable` conclusion cannot list a class
that was `not_accessible` (SP-7). Whether the classes searched are every preferred class
of the citing record's row can only be checked on that record (§1). S10 switches that on
with the first `supplier` state.

**Applied by hand to HBM-06** (L-09). The question: which company supplies the HBM in
NVIDIA's H100? It is the `rel:incorporates.supplier` row of `source-policy.md` §7, whose
preferred classes are `company_technical_documentation` and `company_filing`.

| Preferred class | Searched | Result |
|---|---|---|
| `company_technical_documentation` | SRC-006, NVIDIA's own architecture page, re-read on 2026-09-30: it names HBM3 14 times (as measured) and no memory maker | no answer from NVIDIA. The memory makers are parties too (`source-policy.md` §4). None of their technical documentation was retrieved: SK hynix's registered pages are marketing and a press release, Micron's is a product page (SRC-015), and Samsung's documentation host refused access (register "Not retrievable") |
| `company_filing` | S05-R1, NVIDIA's 10-K: its memory suppliers are named at company level (p.8) | no answer for the product (ER-9). The memory makers' filings were not retrieved (D-042) |

**Result.** One preferred class was not fully searchable, and one party's documentation
was refused. Under ER-3 the value is **`not_researched`**, with the access gap recorded.
It is not `not_publicly_determinable`. S01's wording, "not publicly determinable from the
product documentation retrieved" (HBM-06), was careful. But its §8 lists the question
under `not_publicly_determinable`, and that assumption does not survive ER-3. The domain
map is not edited; S10 records the state. No search claim is created in S06, because no
record exists to cite it.

## 9. The source record and the migration

**The record** (D-050; field shapes in the schema). Every source has:

- `id`, `source_class`, `title`, `publisher`;
- `publisher_entity`, `authors`, `url`, `stated_dates`, `retrieval` (method, access time
  and hash);
- `filing_copy`, for filings only;
- `migrated_from`, on migrated records only.

**Decisions inside the record:**

- **IDs are `src-NNN`, keeping S01's numbers.** Register row `SRC-006` is `src-006`, so
  every `SRC-NNN` in older documents resolves by one rule: lower-case it.
  - The prefix is lower case, like every other Atlas ID.
  - MA §5.3's `source-001` was rejected: it would break the visual link to the IDs cited
    across the S01–S05 documents.
  - S05-R1 is numbered after the register, as `src-024`. `migrated_from` keeps every old
    label resolvable.
- **`publisher_entity` is `not_researched` for every company publisher.** Which legal
  entity publishes "Google Cloud" or "SK hynix Newsroom" is a company-identity question
  (`entity-taxonomy.md` §3.1). S07 owns it, and choosing slugs now would fix S07's IDs in
  advance. Non-company publishers are `not_applicable`, because institution stays
  reserved (D-022).
- **Dates as stated, never guessed.** `stated_dates` keeps each date the source gives with
  its kind (`published`, `modified`, `last_updated`, `signed`). A source that states none
  is `undated`, as the register's "undated (live page)".
- **The host of a copy is in the URL.** For a filing, `filing_copy` records whose copy it
  is, and whether its identity with the regulator's copy was checked (RA-6).

**The migration** (CLAUDE.md §9, class B). `tests/test_data_integrity.py`
`migrated_records()` reads the register table, `source-policy.md` §8.1 (each row's class)
and §8.3 (S05-R1). It derives the source records. `data/sources.json` was written by that
function, and VD-9 re-runs it on every test run and compares the result field by field.
The mapping:

| Register column | Source record field | Rule |
|---|---|---|
| `id` | `id`, `migrated_from` | lower-cased for `id`; kept verbatim in `migrated_from` |
| `publisher` | `publisher`, `authors`, `publisher_entity` | text before " — " is the publisher, the rest the authors (otherwise `not_researched`). One override: SRC-005's cell names two organisations, and `source-policy.md` §2 and §8.1 make SIA the publisher, with the BCG co-authorship in the authors. `publisher_entity` as above |
| `title` | `title` | verbatim |
| `url` | `url` | verbatim |
| `publication_date` | `stated_dates` | "YYYY[-MM[-DD]]" is `published`; "(modified …)" adds `modified`; "modified …" and "last updated …" alone give that kind only; "undated (live page)" is `undated`. Any other text fails the migration |
| `source_type` | not migrated: superseded by `source_class` | S01's free text; the class comes from `source-policy.md` §8.1 (D-041) |
| `source_tier` | not migrated: superseded by `source_class` and the matrix (D-036) | the register keeps it as S01's provisional record |
| `accessed_at` | `retrieval` | `accessed_at` verbatim; `method` is `automated`, because every row was retrieved with `curl` over HTTPS (register "How to read") |
| `content_sha256` | `retrieval` | the 12-character prefix, without backticks |
| `locators_used` | not migrated: locators belong to each citation's `locator` | a second home otherwise (§5) |

**S05-R1** comes from its §8.3 row: publisher and title from the "What" cell, the URL,
`accessed_at` and hash from the "Retrieval" cell, `signed` from the signature date,
`filing_copy: filer_hosted_not_checked` because it is the company-hosted copy (D-042).

**What is not migrated, and why:**

- the register's **"Retrieved but not cited"** rows: they support nothing;
- its **"Not retrievable"** rows: access gaps are not sources (SP-7);
- **S05-A1**: an access record, not a source.

All three stay in the frozen register and in `source-policy.md` §8.2–§8.3 as history.

**After the migration:**

- **The class has one live home**, the source record (D-041). `source-policy.md` §8.1 is
  marked as history.
- **The tests move with it.** `tests/test_source_policy.py` now reads each source's class
  for the conflict table (§10.2) from `data/sources.json`. The link between §8.1 and the
  data is checked once, by VD-9, as the migration's proof.
- **The register is frozen.** Its status line says so, and VD-9 fails if a migrated value
  changes on either side. A later change to a migrated value needs a decision, and the
  change is visible in the test.

## 10. Freshness

**Decision (D-051).** S06 writes **no `validate-freshness` code**. Its rules
(`source-policy.md` §12) need what S06 does not yet have:

- the 12-month horizon applies per matrix row, and a row is known only on a record (§1);
- supersession needs a newer edition to be registered;
- anchor drift needs a scheduled re-read.

Building it on the staging seed claims would be machinery before a used loop (L-01, L-09).

**What S06 does provide, so that the check can be written:**

- every source has an access time and a hash;
- every claim that cites sources has an `as_of`, or the explicit `not_stated`;
- every verified citation records the bytes it read.

The S06 Verifier pass used them by hand. SRC-006's hash had changed since S01, so its
anchor was re-checked, as `source-policy.md` §12 requires. The anchor was still there, but
the section heading had changed (§14). The first session with `time_sensitive` canonical
records (S07) builds the check.

## 11. validate-data

MA §15 asks for a documented equivalent of `validate-data`. Here it is two test modules
that CI runs on every push (H-4, D-051). The schema checks use the pinned `jsonschema`;
the rest is standard library, so `tools/` stays standard library (D-026).

```bash
python -m unittest discover -s tests -p "test_data*.py" -v   # validate-data
```

| Check | What it checks | Test | Runs on |
|---|---|---|---|
| VD-1 | each data file is a JSON array of objects | `tests/test_data_integrity.py` | `data/` |
| VD-2 | every source and claim record is valid against its schema | `tests/test_data_schema.py` | `data/` |
| VD-3 | IDs are unique: sources; claims across staging and canonical | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-4 | every source a claim cites, in citations and search records, exists | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-5 | every input and competing claim exists and is not the claim itself; inputs have no cycle | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-6 | a claim's status is allowed by its inputs' statuses (§4) | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-7 | disputes are mutual | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-8 | canonical claims are accepted by the human and rest only on canonical claims; staging holds no accepted claim | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-9 | the migration is exact (§9) | `tests/test_data_integrity.py` | `data/` |
| VD-10 | a `FACT` cites at least one class that is sufficient alone for some matrix row | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-11 | every anchor is verbatim in its machine-checkable home: the domain map for register sources, `source-policy.md` §8.3 for S05 retrievals | `tests/test_data_integrity.py` | `data/` |
| VD-12 | bytes were read after the source was registered; claims were verified on or after the day of the read | `tests/test_data_integrity.py` | `data/`, fixtures |
| VD-13 | a search record lists each class once, and each source under its own class | `tests/test_data_integrity.py` | `data/`, fixtures |
| V-1 to V-9 | the relationship rules of `relationship-taxonomy.md` §15 | not built: they check entity and relationship records, and none exist (S07, S10) | — |
| V-10 | a record does not rest only on claims whose sources are "never sufficient alone" for its matrix row, or whose standing the row does not allow | defined, not built: the row is known only on a record (S07 switches it on) | — |

"Fixtures" means the fictional sources and claims in `tests/fixtures/`. A test also plants
one fault of each kind in them and expects it to be caught.

**None of V-1 to V-9 runs yet.** V-3, V-4 and V-9 could run on the fictional relationship
fixtures, but they would check fixtures, not data. They arrive with the first records they
check (L-05, L-09).

## 12. The trace

The roadmap gate: "What exactly supports this relationship?" `tools/trace.py` (standard
library, D-053) takes any record, claim or source ID and prints the chain:

- record → claims, with the JSON path that cites each claim;
- claim → type, status, verification date and review state;
- claim → citations, each with source, class, publisher, URL, stated dates, retrieval,
  locator, anchor, standing, originator and bytes read;
- claim → input claims, recursively, with the reasoning;
- source → the claims that cite it.

It exits 1 when a reference does not resolve.

```bash
python tools/trace.py claim-tsmc-fabricates-h100-gh100
python tools/trace.py src-021
python tools/trace.py rel-example-foundry-fabricates-accelerator --data DIR --records FILE
```

**What it cannot yet show:**

- a real relationship or entity: none exists before S07–S10, so the record path is shown
  on fictional fixtures only;
- whether a claim's class and standing suit the citing record's matrix row (V-10);
- freshness;
- the source text itself, which stays outside the repository;
- a publisher as a company record (S07).

## 13. Five kinds of claim (for the human)

The five labels answer one question: **who is speaking, and how far does the statement go
beyond what was said?** Each example below is a seed claim in
`data/staging/claims.json`. Run `python tools/trace.py <claim ID>` to see everything behind
it.

- **`FACT` — a first-hand source says it about itself or its own product.** NVIDIA's
  architecture page (SRC-006) says its GH100 GPU, which powers the H100, is "fabricated
  using the TSMC 4N process customized for NVIDIA" (`claim-h100-gh100-process-name`).
  NVIDIA is the vendor, so it is a `party` (`source-policy.md` §4), and the claim is only
  about what NVIDIA calls its process. A second example: AWS on its own Availability Zones
  (`claim-aws-availability-zone-data-centers`).
- **`DERIVATION` — the Atlas reads something out of other claims.** *TSMC fabricates the GH100* is not written anywhere. It is read out of the process name (ER-1)
  (`claim-tsmc-fabricates-h100-gh100`). It cites the `FACT` above, not the page, and a
  reader sees it as inferred.
- **`ATTRIBUTION` — the Atlas records what someone says, without adopting it:**
  - ASML says EUV is "unique to ASML" (`claim-asml-euv-unique-to-asml`; ER-5). It is true
    that ASML says so. Whether it is true of the world is another claim.
  - LBNL reports that IDC analysts said "the market is currently constrained by die supply"
    (`claim-lbnl-reports-idc-gpu-die-supply`). This is a chain: LBNL is the `reporter`,
    IDC the originator, and the claim can never be more than an attribution to IDC as
    reported (ER-6).
  - CSET's and LBNL's definitions of AI chips and accelerators
    (`claim-cset-ai-chip-definition`, `claim-lbnl-ai-accelerator-accounting`), and NIST's
    cloud definition (`claim-nist-cloud-location-independence`). A source's definition is
    that source's.
- **`INTERPRETATION` — the Atlas decides.** The working definition of AI accelerator,
  GPUs and AI ASICs only (`claim-atlas-ai-accelerator-working-definition`), cites both
  source definitions it chooses between (CON-01). It is the Atlas's choice, approved by the
  human at TQ-01, not a fact.
- **`IMPLICATION` — what this means for the Atlas's work.** Because NIST says customers
  may specify location only at a level above the site, and an Availability Zone
  groups data centres, the Atlas should expect cloud facilities to be undisclosed
  (`claim-cloud-compute-facility-often-undisclosed`). It shapes S09's research. It says
  nothing new about the world.

**How it is displayed** (for S11). A reader sees the label, the status, and the sentence
behind every claim. A reader never sees a bare *TSMC makes the H100*: they see NVIDIA's
statement, the inference, and the rule that made it an inference.

## 14. Review sheet (the human's manual test)

Part A asks the human to test a few claims by hand. For each claim:

1. Run `python tools/trace.py <claim ID>`. It prints the source URL, locator, anchor,
   standing and the proposed type and status.
2. Open the URL, and find the locator and the anchor.
3. Read the whole sentence. Answer: **does it say this, and no more?** And: is the type
   right (who is speaking)?
4. Give a verdict: accept, reject, or "wording too strong".

| Claim | What to look for |
|---|---|
| `claim-h100-gh100-process-name` | The sentence names the **GH100** die that powers the H100, not the H100. The domain map, S04 and S05 wrote "the H100 is fabricated…": slightly more than the source says. The page's bytes changed since S01, and its heading now reads "NVIDIA H100 GPU architecture in-depth" |
| `claim-tsmc-fabricates-h100-gh100` | Is ER-1 applied as written? Should it stay a `DERIVATION`? |
| `claim-asml-euv-unique-to-asml` | Is "unique to ASML" kept as ASML's claim, and not adopted? |
| `claim-lbnl-reports-idc-gpu-die-supply` | The sentence reads in LBNL's voice. Its paragraph reports what "IDC analysts advised us" and closes with "(IDC, 2026)", which p.31 identifies as a personal communication. Is `reporter` right? And is "the market" the high-end GPU market of that paragraph? |
| `claim-cset-ai-chip-definition` | Footnote * on p.4: does it say "includes", and is "certain types of ASICs" kept? |
| `claim-lbnl-ai-accelerator-accounting` | Does p.16 support "the 2024 report covered GPU accelerators only"? |
| `claim-atlas-ai-accelerator-working-definition` | Is it a choice, citing both sides of CON-01? |
| `claim-nist-cloud-location-independence` | The domain map labels DC-04 `FACT`; this claim treats NIST's definition as `ATTRIBUTION` (a source's definition, `source-policy.md` §10.1). Agree? |
| `claim-aws-availability-zone-data-centers` | AWS on its own infrastructure: is `FACT` (party) right? |
| `claim-cloud-compute-facility-often-undisclosed` | Does it stay a planning consequence, without claiming any site is `not_publicly_determinable`? |

**Where the verdicts go.** The human's words go verbatim into an addendum of
`sessions/reports/SESSION-06-REPORT.md`. Each claim's `review` then records the verdict,
the date and that report (§7). An accepted claim moves to `data/claims.json`.

## 15. Candidates considered and rejected

| Candidate | Why not |
|---|---|
| A claim that lists the records it supports | A second home for the record → claim link (§1) |
| A `matrix_row` on the claim | Derived from the citing record; one claim can serve two rows (§1) |
| MA §10's seven types as values | Three of them are covered by the five labels with a rule for whose statement it is (§2) |
| MA's `derived` as a status | Duplicates `DERIVATION` (§3) |
| `direct` kept as named | Reads like standing, and cannot describe a derivation (§3) |
| `disputed` for every conflict kind | A definitional conflict leaves two true attributions (§3) |
| A numeric confidence or "strength" | NG-11, D-028. The type, status and citations carry it |
| A `verified` boolean or status value | The status and `verified_on` already say it; a third field would be a second home (§6) |
| A staging flag on one claims file | Consumers could read an unreviewed claim as canonical. Two files, checked by VD-8 (§7) |
| A separate search-record kind, or an `UNKNOWN` claim type | Machinery for one block; the conclusion is an inference (§8) |
| Source IDs kept as `SRC-001`, or MA's `source-001` | The first breaks the lower-case ID convention; the second breaks the visual link to older documents (§9) |
| Company IDs in `publisher_entity` now | They are S07's to establish (§9) |
| The register's free-text date, or its `locators_used`, in the record | Unparseable dates; locators belong to citations (§9) |
| A `tools/validate_data.py` importing `jsonschema` | H-4: tests in CI; `tools/` stays standard library (D-026) |
| `validate-freshness` code now | Needs matrix rows from records (§10) |
| Migrating the domain map's statements | S06 is limited to 5 to 10 seed claims (H-1); the map stays S01's artifact |

## 16. What S06 leaves to other sessions

| Item | Owner | Note |
|---|---|---|
| The human's verdicts on the seed claims; moving accepted claims to `data/claims.json` | the human, then the next session | §7, §14 |
| `publisher_entity` for company publishers | S07 | the company records and their IDs |
| V-10, and `validate-freshness` (the 12-month horizon per row) | S07 | the first `time_sensitive` canonical records |
| V-1 to V-9 | S07 (entities), S10 (relationships) | `relationship-taxonomy.md` §15 |
| How anchors from new retrievals are machine-checked (VD-11 covers only S01 and S05 readings) | S07, by decision, with its first new source | §5 |
| Whether the search block covers every preferred class of the row | S10, with the first `supplier` state | §8 |
| A class for announcements by standards bodies or associations | the session that retrieves one | `source-policy.md` §2 |
| Normative text as a claim type | S17 | §2 |
