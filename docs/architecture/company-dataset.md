# Company dataset — the first canonical entities

**Status:** proposed (S07): D-054 to D-066.
**Session:** S07 · **Date:** 2026-10-01
**Inputs:**
- `entity-taxonomy.md` §3.1 (company identity), §3.6 (jurisdiction), §7 (attribute contract),
  §9 (handoffs);
- `claim-model.md` §1, §4, §5, §7, §11, §16;
- `../research/source-policy.md` §4 (standing), §6 (ER-1 to ER-10), §7 (rows
  `identity:company`, `identity:jurisdiction`, `attr:company.*`), §11 (RA-1 to RA-7), §12;
- `relationship-taxonomy.md` §15 (V-1 to V-9);
- the S07 prompt, Part B, with the human's answers H-1 to H-6 and the three answers given
  during S07 (D-058 to D-060).

**Schemas:** unchanged. Company and jurisdiction records follow
[`schemas/entities.schema.json`](../../schemas/entities.schema.json) as accepted in S03.
**Data:** [`data/companies.json`](../../data/companies.json) and
[`data/jurisdictions.json`](../../data/jurisdictions.json) (canonical), with their staging
copies under [`data/staging/`](../../data/staging/) (D-055).

**One home for each kind of statement:**

- **The schema** holds the record shapes and the role and state vocabularies.
- **This document** holds the reasoning for the first company records:
  - the seed;
  - which legal entity each record is;
  - the ID rule;
  - which sentence supports which field;
  - how jurisdictions are evidenced;
  - when a record is canonical;
  - how new anchors are checked;
  - the record-level checks.
- **Not here:**
  - what a source class or standing is for (`source-policy.md`);
  - what a claim, `verified` or canonical means for a claim (`claim-model.md`);
  - what each record type is (`entity-taxonomy.md`).
- **The records** hold the values, and **the claims** hold the sentences and sources.
  Nothing in this document is a value of a record.
- **Checked by** `tests/test_data_entities.py`, `tests/test_freshness.py` and
  `tests/test_data_integrity.py`.

**Claim labels.** The rules are the Atlas's design (`INTERPRETATION`), and their
consequences are `IMPLICATION`. What a company's filing says is cited through a claim in
`data/`, never stated here as a fact.

---

## 1. The seed and what is left out

**Rule** (H-1, D-054). One company for each layer of the first vertical (MA §6.4). Each must
be named in a registered source or in the domain map. A company stays out when no
first-hand identity source can be read.

| Layer | Company | Why it is in | Identity source |
|---|---|---|---|
| Accelerators | NVIDIA | ACC-04; the S06 seed claims | `src-024` (its 10-K, re-read) |
| Memory | SK hynix | HBM-06; four registered sources | `src-030` (its annual report on DART) |
| Memory | Micron | HBM-06; named in S05-R1 p.8 | `src-025` (its 10-K) |
| Packaging | Amkor | PKG-07 | `src-026` (its 10-K) |
| Foundry | TSMC | FAB-03; named in S05-R1 p.8 and FAB-05 | `src-031` (its 20-F, manual retrieval, D-060) |
| Equipment | ASML | SME-03 | `src-029` (its 20-F) |
| EDA | Synopsys | EDA-01 | `src-027` (its 10-K) |
| Cloud | Amazon | DC-04; the S06 seed claims | `src-028` (its annual report with the 10-K) |

**Why this set is "curated" and not "complete"** (NG-03):

- it is enough to give every chain layer one actor with identity evidence;
- the S08–S10 records need endpoints in every layer, and this gives them one each;
- it is not a market map. Being in the seed says nothing about importance or share.

**Left out** (each could be added by a later session with its own evidence):

- Google, Lam Research, Samsung and Intel. They are named in registered sources, but the
  human chose eight (H-1). Samsung's and Intel's hosts refused in S01.
- Every other firm named in the filings read: suppliers, customers and subsidiaries. A
  filing's supplier list is S10's `supplies` evidence, and its subsidiary list is S10's
  `owns` evidence (Part B §08).

## 2. Which legal entity each record is

**Rule** (`entity-taxonomy.md` §3.1, D-054). A record is the legal entity that the
company's own filing names as the registrant or filer. A brand stays a `name` or an alias.
A parent and a subsidiary are two records only when the evidence needs both, and no S07
field does.

| Record | Legal entity (as the filing names it) | Ruling |
|---|---|---|
| `company-nvidia` | NVIDIA CORPORATION | the 10-K registrant. "NVIDIA Technical Blog" (`src-006`) is a channel, not an entity |
| `company-micron-technology` | Micron Technology, Inc. | the 10-K registrant |
| `company-amkor-technology` | Amkor Technology, Inc. | the 10-K registrant |
| `company-synopsys` | SYNOPSYS, INC. | the 10-K registrant |
| `company-amazon-com` | AMAZON.COM, INC. | the 10-K registrant. "Amazon Web Services" is one of its three segments (p.14), so it is an alias here. Whether a separate legal entity publishes the AWS documentation (`src-010`, `src-020`) is open (§14) |
| `company-asml-holding` | ASML Holding N.V. | the 20-F registrant. The filing says it "operates through its subsidiaries" (p.89). Which subsidiary operates which site is S09/S10's |
| `company-sk-hynix` | 에스케이하이닉스 주식회사, in English SK hynix Inc. | the filer of the annual report. "SK hynix Newsroom" (`src-011` to `src-014`) is a channel |
| `company-taiwan-semiconductor-manufacturing-company` | Taiwan Semiconductor Manufacturing Company Limited, if the 20-F cover confirms it (§11) | the 20-F registrant. "TSMC" is the display name and an alias |

**Display names are editorial** (`entity-taxonomy.md` §7). "Amazon", "ASML" or "TSMC" can
change without any ID or claim changing (§3).

## 3. Stable IDs (ID-1, machine-checked)

**Rule** (D-056). A company ID is `company-` plus the slug of the company's legal name in
Latin script, as first recorded:

1. take a Latin-script value of `legal_name`;
2. drop one trailing legal-form designation listed below, and the comma before it;
3. lower-case it, reduce it to ASCII, and join the remaining words with `-`. Every run of
   other characters becomes one `-`.

| Designation | Meaning | Seed record where it applies |
|---|---|---|
| `Inc.` | incorporated (US) | Micron, Amkor, Synopsys, Amazon, SK hynix |
| `Corporation` | corporation (US) | NVIDIA |
| `N.V.` | naamloze vennootschap (NL) | ASML |
| `Limited` | limited company | TSMC |

The designations match case-insensitively. A new designation is added to this table by a
decision, when a record first needs it (M0 audit A-1).

**Why the legal name, and not the display name.** The display name is an editorial choice,
so an ID built from it would change when the editor's choice changes. The legal name is
claim-backed, and it changes only by an event (a rename).

**What the rule guarantees, and how:**

- **Renames.** A renamed company keeps its ID (`entity-taxonomy.md` §3.1). The old legal
  name stays as an assertion with a `valid_to`, and the new one is added. ID-1 accepts the
  slug of *any* Latin-script legal name, so the ID still checks.
- **Collisions.** If two legal names give one slug, the second record adds `-` and its
  incorporation jurisdiction code (e.g. `-us`). If that also collides, a decision is needed.
  The seed has none.
- **Placeholders.** An ID may never match the relationship schema's `not_placeholder`
  pattern (V-9). A company nobody can identify gets no record: an unknown supplier is an
  explicit state (D-031).
- **Machine check.** `tests/test_data_entities.py` (ID-1) recomputes the slug from the
  record's legal names. A test also changes a display name and checks that no ID error
  appears.

**Consequences:**

- Some IDs are long (TSMC's). Length is the price of a rule with no judgement in it.
- `company-asml-holding` keeps "Holding", because "Holding" is part of the name, not a
  legal form.
- `company-amazon-com` keeps ".com" as `-com`.

## 4. Which sentence supports which field

**Rule** (D-057). Every field is either claim-backed or an explicit state (R-7). The rows
are `source-policy.md` §7's.

| Field | Row | The sentence it needs | Claim type | `as_of` |
|---|---|---|---|---|
| `identity_claim_ids` and `legal_name` | `identity:company`; `attr:company.legal_name` | the filer's own statement of its exact legal name: a 10-K or 20-F cover's "(Exact name of registrant as specified in its charter)", a filing's statement of the company's name, or ASML's sentence naming itself as a company | `FACT`, standing `party`. One claim serves both fields (D-044) | `not_stated`: the cover gives no date for the name, so the filing's own date applies (`source-policy.md` §12) |
| `incorporated_in` | `attr:company.incorporated_in` | the filer's statement of where it is incorporated | `FACT` when the sentence names the country. `DERIVATION` when it names a subdivision (a US state), with the ISO 3166-2 claim as a second input (§5) | as stated |
| `headquartered_in` | `attr:company.headquartered_in` | a sentence with the word "headquarters" or "head office" (본사). Never a facility, a listing or a cover address alone (R-5) | as `incorporated_in` | as stated |
| `roles` | `attr:company.roles` | a sentence that states the business model the role's schema definition names: fabless manufacturing, foundry, OSAT, memory manufacture, equipment, EDA, cloud services | `FACT`, standing `party`. Never derived from edges (D-024) | as stated |

**How each rule is applied:**

- **Cover-page anchors.** A cover page is a form, not prose. Its anchor is the value
  followed by its printed label, in the order the text runs, e.g. "Micron Technology, Inc.
  (Exact name of registrant as specified in its charter)". Where the extracted text puts a
  neighbouring field's value between them (an IRS number), the anchor keeps it, and the
  locator says which value is which.
- **The legal name is verbatim, capitals included.** "NVIDIA CORPORATION" and "SYNOPSYS,
  INC." are recorded as the cover prints them. The slug ignores case (§3).
- **A role needs its business model, not a product.** For `memory_manufacturer`, the
  sentence must say that the company manufactures DRAM or memory products. Which HBM product
  goes into which accelerator is product-level, and never read off a company role (ER-9;
  HBM-06 stays `not_researched`, D-049).
- **Superlatives are not adopted** (ER-5). Amkor's "world's largest" and Synopsys's "global
  leader" are left out. The role rests on a non-superlative sentence, or on the defining
  phrase only, and the locator says so.
- **Forward-looking statements support nothing here** (ER-8). Amkor's planned Arizona
  facility is not a headquarters or a facility record.
- **Korean text.** SK hynix's annual report is in Korean, with English table headings. The
  anchor is the Korean sentence, verbatim. The statement is the Atlas's translation, and
  says so. The translation is a step the human checks (§12).
- **What stays `not_researched`:** a field with no such sentence in the sections read.
  SK hynix's `incorporated_in` is one: the sections read give its founding date, its legal
  form and its head office, but no sentence names where it is incorporated. Inferring Korea
  from the legal form would be the Atlas's guess.

## 5. Jurisdictions

**Rule** (H-4, D-058). S07 creates only the jurisdiction records that the seed's
attributes point to. Each cites ISO 3166-1 as published by ISO, the preferred class for
`identity:jurisdiction` (`standard_specification`, standing `originator`).

**Access.** ISO's own pages refused plain requests: `www.iso.org` (the country-codes page and
the Online Browsing Platform, OBP) returned an HTTP 403 challenge on 2026-10-01, and ISO's
open maintenance portal has no ISO 3166 entry. That is H-4's stop condition. The human chose
manual retrieval (RA-4): the human took screenshots of the OBP entries in their own browser,
and the session registers each image as a source (`src-032` to `src-037`, §11). No secondary
list stands in for the standard (RA-5).

**Screenshots as evidence.** Each image shows the `iso.org` host, the "Online Browsing Platform
(OBP)" header and "Standard: ISO 3166", so its origin is visible. An image has no text layer,
so the Verifier reads each anchor off the image and copies it verbatim, in reading order (row
label, then value). The hash is of the image file. The human confirms these anchors on the
review sheet. The images stay outside the repository (RA-4(4)), and they show the human's ISO
account, which is a second reason.

**What each jurisdiction record holds:**

- **ID:** `jurisdiction-` plus the alpha-2 code in lower case (the schema). The code has one
  home, the ID.
- **Display name:** editorial. ISO's short name is kept as an alias, exactly as ISO gives it.
- **Identity claim:** a `FACT` citing the OBP page, with an anchor that carries the
  alpha-2 code. J-1 checks the code against that anchor.
- **No position on sovereignty.** The code is an identifier (`entity-taxonomy.md` §3.6).
  ISO's short name for TW is recorded as ISO gives it, and the Atlas's display name is
  "Taiwan". Neither is a statement by the Atlas.

**From a US state to a country.** US filers name a state ("Delaware"), not the country. The
schema's jurisdictions are countries. The step from the state to the country is recorded as
a `DERIVATION`. Its inputs are the company's `FACT` naming the state, and the `FACT` that ISO
3166-2 lists that state as a subdivision of the country (from the same OBP page). The same
pattern applies to SK hynix's 경기도 (Gyeonggi-do). There, the romanisation of the Korean
name is part of the reasoning the human checks.

## 6. Staging, canonical and the human's review

**Rule** (H-3, D-061). The claim-model mechanism (`claim-model.md` §7) is extended to
entities, without a review field (Part B §08):

- **Where a record is says what it is.** Staging records are in `data/staging/`, and
  canonical records in `data/companies.json` and `data/jurisdictions.json`.
- **CE-1:** a canonical record cites only canonical claims, and points only to canonical
  jurisdictions. No ID is both staging and canonical. With VD-8, a canonical record
  therefore rests only on claims the human accepted.
- **Promotion.** At the end of S07, the human reviews the identity and attribute claims on
  the review sheet (§12). Accepted claims move to `data/claims.json` with their verdicts.
  A record moves to the canonical file only when every claim it cites is accepted. A
  record with a rejected claim stays in staging, with that field left for the next
  session.
- **The S06 seed claims** move only on their own verdicts.

## 7. Anchors from new retrievals (machine-checked)

**Rule** (H-6, D-062). VD-11 machine-checks anchors only where their text is in the
repository (the domain map and `source-policy.md` §8.3). From S07, the full texts of new
sources stay outside the repository (RA-4(4)), so their anchors are Verifier-attested:

**Verifier-attested from:** `2026-10-01T00:00Z`

- A citation whose `read` is from this time on is attested. The Verifier found the anchor
  verbatim (whitespace normalised) in text extracted from those bytes, and read the sentence
  around it. VD-11 then requires the bytes read to be the registered bytes, hashed in full.
- A citation read before this time is still machine-checked against its home, exactly as
  in S06.
- **The human spot-checks a sample** of attested anchors (§12). The sample and the human's
  findings are recorded in the session report.

**Why a date and not a list.** A list of attested claims would be a second home for what
the `read` time already says. A seed anchor edited without a new read keeps its old read
time, so it is still machine-checked: S06's break 6 is still caught.

## 8. validate-data for records

**Rule** (D-063). These checks run in CI with the S06 checks (H-4 of S06, L-02):

| Check | What it checks | Where |
|---|---|---|
| VD-2 (extended) | every company and jurisdiction record, staging and canonical, is valid against the accepted entity schema | `tests/test_data_schema.py` |
| VD-11 (extended) | attested anchors were read from the registered bytes (§7) | `tests/test_data_integrity.py` |
| V-1 | every claim and jurisdiction reference resolves, and `publisher_entity` names a canonical company | `tests/test_data_entities.py` |
| V-4 | `valid_from` ≤ `valid_to` on every assertion | `tests/test_data_entities.py` |
| V-9 | no entity ID matches the `not_placeholder` pattern | `tests/test_data_entities.py` |
| V-10 | each field rests on at least one citation whose class is preferred or acceptable, and whose standing is allowed, for its row. A derivation is followed to its inputs' citations | `tests/test_data_entities.py` |
| CE-1 | §6 | `tests/test_data_entities.py` |
| ID-1 | §3 | `tests/test_data_entities.py` |
| J-1 | a jurisdiction's code is carried by an ISO 3166-1 identity anchor | `tests/test_data_entities.py` |
| F-1 | §9 | `tests/test_freshness.py` |

**V-2, V-3 and V-5 to V-8** check relationships, and none exist. They arrive with S10's
first edges (L-05).

**How V-10 reads the matrix.** It reads `source-policy.md` §7 on every run, never a copy:
the preferred and acceptable columns are the sufficient classes, and the standing column is
read as "party", "originator" or both. A field whose only evidence is "never sufficient
alone" fails. So does one whose only first-hand evidence has `reporter` standing.

```bash
python -m unittest discover -s tests -p "test_data*.py" -v   # validate-data
python -m unittest discover -s tests -p "test_freshness.py" -v   # validate-freshness
```

## 9. Freshness (F-1)

**Rule** (D-064, applying D-040). For every field whose row is `time_sensitive`, at least one
citation the row accepts must have an evidence date no more than the `source-policy.md` §12
horizon before its use.

- **Evidence date:** the claim's `as_of` if it is a date. Otherwise, the latest date the
  source states for itself. Otherwise (an undated source), its access date. A partial date
  counts from the start of its period.
- **Use:** the date the Verifier checked that citation, the claim's `verified_on`. A record
  committed today uses its claims as verified, so "use" is that check.
- **Re-checked** means newer evidence. Re-reading an old filing confirms the anchor, but the
  content is no newer. A stale field therefore needs a newer source, cited by a newly
  verified claim.
- **Where it runs:** a test that CI runs (L-02), on staging and canonical records.

**What it does not do.** The result does not change as the calendar moves: a commit that
passes today still passes next year. Ageing after verification is a scheduled re-check, the
Change Detector's job, which stays inactive (`docs/agents/roles.md`). The trace prints each
source's dates, so the age is always visible.

**Consequence now** (`IMPLICATION`). Micron's 10-K was signed on 2025-10-03. It is within
12 months of its verification on 2026-10-01, but its next annual report is due soon, and a
claim verified after 2026-10-03 on this filing would fail F-1.

## 10. `publisher_entity`

**Rule** (D-065, closing the S06 handoff in part). A source's `publisher_entity` is set to a
company record only when the evidence shows that the publisher is that legal entity, and
only to a canonical company (V-1).

- **Filings:** set. A filing is made by its registrant or filer under a legal obligation,
  and the claim on its own name shows which entity that is (§4).
- **Web pages** (`src-006` to `src-020`): left `not_researched`. A page names a channel or a
  brand ("NVIDIA Technical Blog", "SK hynix Newsroom", "Amazon Web Services"), not a legal
  entity. A copyright line names a rights holder, which is a different fact. The party test
  (`source-policy.md` §4) for these pages still rests on the brand, as in S06.

## 11. Sources and access

**New source records** (`data/sources.json`). Each records class, retrieval method, time and
full hash, stated dates, and `filing_copy`:

| Source | What | Copy |
|---|---|---|
| `src-025` | Micron, 10-K, fiscal 2025 | `filer_hosted_not_checked`: `investors.micron.com/files/…`, served from the filer's IR file host |
| `src-026` | Amkor, 10-K, 2025 | `filer_hosted_not_checked`: `ir.amkor.com` |
| `src-027` | Synopsys, 10-K, fiscal 2025 | `filer_hosted_not_checked`: `investor.synopsys.com/files/…` |
| `src-028` | Amazon, 2025 Annual Report, which contains the 10-K from p.12 | `filer_hosted_not_checked`: `ir.aboutamazon.com/files/…` |
| `src-029` | ASML, 2025 Annual Report based on US GAAP: the Form 20-F (signature page p.349) | `filer_hosted_not_checked`: `ourbrand.asml.com`, linked from `investor.asml.com` |
| `src-030` | SK hynix, Annual Report for fiscal 2025, section I.1 | `regulator_hosted`: English DART (D-059) |
| `src-031` | TSMC, 20-F for 2025 | manual retrieval by the human (D-060) |
| `src-032` to `src-037` | ISO 3166 OBP screenshots: US identity block and two subdivision tables; NL identity block; KR identity block and subdivision table | manual retrieval by the human (D-058) |

`src-024` (NVIDIA's 10-K) was re-read. Its bytes are unchanged since S05 (`a056b59e4170`).

**Access gaps** (SP-7; nothing was bypassed, RA-2):

| Host | Response, 2026-10-01 | Consequence |
|---|---|---|
| `www.iso.org` (country codes, OBP) | HTTP 403, challenge page | RA-4 (D-058) |
| `investor.tsmc.com`, `pr.tsmc.com` | HTTP 403, challenge page | RA-4 (D-060) |
| `investors.micron.com` (pages), `investor.synopsys.com` (pages), `ir.aboutamazon.com` (pages) | HTTP 403, challenge page | none: each host's `/files/` path served the filing |
| `www.skhynix.com/ir/` | HTTP 403; its IR pages point to DART for disclosures | DART (D-059) |
| `findbiz.nat.gov.tw` (Taiwan company register) | HTTP 403, challenge page | not needed once the 20-F is read |

## 12. Review sheet (the human's manual inspection)

Part A asks the human to inspect a sample of canonical companies by hand. For each claim on
the sheet in the S07 report:

1. Run `python tools/trace.py <record ID>`. It prints every field, its value, its claims
   and their sources, locators and anchors.
2. Open the source at the locator. Read the whole sentence.
3. Answer:
   - **Identity:** does the filing name this legal entity, exactly?
   - **Each value:** does the sentence say this, and no more?
   - **Derivations:** does the ISO subdivision step hold? Is it shown as inferred?
   - **Korean text:** is the translation faithful?
   - **Roles:** does the sentence state the business model that the role's definition
     names?
4. Give a verdict per claim: accept, reject, or "wording too strong".

**Where the verdicts go:** verbatim into an addendum of `sessions/reports/SESSION-07-REPORT.md`.
Each claim's `review` then records the verdict and that report (`claim-model.md` §7). §6 then
decides which records move.

## 13. Candidates considered and rejected

| Candidate | Why not |
|---|---|
| IDs from the display name, or from the stock ticker | The display name is editorial; a ticker is a listing, which can change or be shared (§3) |
| Hand-chosen short IDs ("tsmc" as TSMC's slug) | A judgement per record, with no check that it is stable |
| A review field on entity records | It needs a schema change the human has not approved (Part B §08). Two files and CE-1 do the same job |
| One `data/entities.json` | H-2 chose one file per entity type |
| `incorporated_in: jurisdiction-us` as a `FACT` from "Delaware" | The filing does not name the country. The step is the Atlas's, so it is a `DERIVATION` |
| The cover-page address as the headquarters | A cover gives "principal executive offices". The schema field is the headquarters, so a sentence that says "headquarters" is used (R-5) |
| A secondary country-code list (a registry mirror, an encyclopaedia) | RA-5: a summary of a standard is not the standard |
| `publisher_entity` from copyright lines | A rights holder is not shown to be the publisher (§10) |
| A calendar-based freshness check | A commit's result would change with the date the test runs (§9) |
| Inferring SK hynix's incorporation from its legal form | The Atlas's guess, not the filing's statement (§4) |

## 14. What S07 leaves to other sessions

| Item | Owner | Note |
|---|---|---|
| `owns` edges from the subsidiary lists (NVIDIA p.88 and the others); the AWS legal entity | S10 | §2. Whether `src-010` and `src-020` are published by a subsidiary is open |
| `supplies` edges from the supplier paragraphs (NVIDIA p.8) | S10 | ER-9 |
| Product `vendor` values pointing to these companies | S08 | D-027 |
| Facilities (ASML's Veldhoven campus, Micron's and SK hynix's fabs, Amkor's Arizona plan as an event) | S09 | R-5 |
| SK hynix's `incorporated_in` | the next session that reads its articles or a register | §4 |
| Scheduled re-checks as filings age | the Change Detector, when activated | §9 |
| `publisher_entity` for web pages | a session that needs the party test automated for them | §10 |
