# SESSION-07 Report — Company dataset

- **Session:** S07 · **Type:** RESEARCH / IMPLEMENTATION · **Milestone:** M2 — Canonical Dataset (first session)
- **Date:** 2026-10-01
- **Prompt:** [`sessions/prompts/S07-PROMPT.md`](../prompts/S07-PROMPT.md) (Part A assembled by
  Claude from the template and confirmed by the human; Part B SPEC §2 detail; H-0 to H-6
  answered before the session).
- **Branch:** `claude/s07-company-dataset`, created from `main` @ `14890d2` (the PR #11
  merge, which carries the S07 prompt).
- **Base at start** (D-018 L-03):
  - `git branch -a`: HEAD detached at `14890d2`; `main`; `remotes/origin/main`.
  - `git ls-remote`: `main` at `14890d2`; six `claude/*` branches, each at a commit already
    merged or cherry-picked (`26acdf9`, `ace06f0`, `ce5b881`, `d9d0a83`, `11185a6`,
    `e23965c`). None carried work missing from `main`.
  - The S07 prompt was on `main` before the session started.

## Mission outcome

**Delivered and reviewed in the session.** The first canonical entities of the Atlas exist:
8 companies, one or more per chain layer, and the 4 jurisdictions they point to. Every
value traces to the company's own filing or to ISO 3166, and the human accepted every claim
they rest on (H-3).

| Deliverable | Where | Status |
|---|---|---|
| M1 milestone audit (H-5) | `docs/architecture/milestone-audits/M1-audit.md`; `docs/quality/audit-history.md` | proposed (D-066) |
| Company-dataset design: seed, legal entities, ID rule, claim patterns, jurisdictions, staging and canonical, attested anchors, record checks, freshness, `publisher_entity` | `docs/architecture/company-dataset.md` | proposed (D-054 to D-066) |
| New sources: 7 filings, 7 ISO screenshots | `data/sources.json` (`src-025` to `src-038`) | canonical source records |
| Claims: 52 new, all accepted by the human; the 10 S06 seed claims accepted too | `data/claims.json` | canonical |
| 8 companies, 4 jurisdictions | `data/companies.json`, `data/jurisdictions.json` | canonical |
| Record checks V-1, V-4, V-9, V-10, CE-1, ID-1, J-1; VD-2 and VD-11 extended; freshness F-1 | `tests/test_data_entities.py`, `tests/test_freshness.py`, `tests/test_data_schema.py`, `tests/test_data_integrity.py` | in CI |
| Trace reads entity files by default and prints values | `tools/trace.py` | in CI |

**Roadmap gate, "Every canonical company record has identity evidence and stable IDs": met,
and reviewed.** Each of the 8 canonical companies has an `identity_claim_ids` claim that is a
canonical `FACT` from the company's own filing with `party` standing (V-10, CE-1), and an ID
that follows ID-1. Tests enforce both, and a deliberate break of each fails.

**Restated contract** (operating-contract step 6, given before any file was written):

- **Mission:** a small, curated, evidence-backed seed of company records (H-1's eight), with
  rule-based IDs, identity claims from first-hand documents, every attribute claim-backed or
  an explicit state, and V-1/V-9/V-10/freshness/canonical-entity checks in CI.
- **Non-goals:** Part B §08. No product, facility, relationship or event record; no schema,
  vocabulary or field change; nothing canonical without the human's verdict.
- **Plan:** M1 audit; `company-dataset.md`; retrieval; staging claims with a Verifier pass;
  staging records; checks (fail first, breaks); review sheet and promotion; decisions, docs,
  report. The plan held. The review ran as two sheets, because the RA-4 files arrived later
  than the filings (Deviation 7).

**Decisions the human took during the session** (each recorded in a decision):

| Question | Answer (verbatim) | Decision |
|---|---|---|
| ISO 3166-1 cannot be retrieved under RA-1/RA-2 (H-4's stop). How should S07 handle jurisdictions? | "RA-4: you save ISO pages (Recommended)" | D-058 |
| Which copy of SK hynix's filing? | "DART regulator copy (Recommended)" | D-059 |
| TSMC: every host refuses | "RA-4: you download its 20-F (Recommended)" | D-060 |
| Upload the files, or fall back? | "I'll upload them now (Recommended)" (ISO and TSMC) | — |
| Review the seven companies while files are pending? | "Yes, review the 7 now (Recommended)" | D-061 |
| May the ISO pages be screenshots? | "Can i send you the screens?" (Claude: yes, with conditions) | D-058 |

**Acceptance criteria** (Part B §15):

| # | Criterion | Result |
|---|---|---|
| 1 | Every canonical company validates against the unchanged entity schema, with a canonical identity claim V-10 accepts | met: VD-2; V-10; CE-1; `entities.schema.json` untouched |
| 2 | Every company ID follows the rule; a test fails when one breaks it | met: ID-1; breaks 6 and 9; display-name control 9b passes |
| 3 | Every field claim-backed or an explicit state; no inferred role; no headquarters from a facility or listing | met: every role cites a business-model sentence; headquarters cite sentences with "headquarters" or "head office"; SK hynix's `incorporated_in` is `not_researched` |
| 4 | Every jurisdiction pointed to exists with its own identity evidence | met: 4 records, each with an ISO identity claim (J-1) |
| 5 | Every new source has class, retrieval, hash and dates; filings record `filing_copy`; access gaps listed | met: 14 records; gaps in `company-dataset.md` §11 |
| 6 | V-1, V-9, V-10, freshness and the canonical-entity rule run in CI | met: in the unit-test step CI runs |
| 7 | Nothing real is canonical without the human's verdict; S06 seeds only on theirs | met: three verdicts in the addenda |
| 8 | The trace prints each company's evidence down to source, class, locator, anchor, standing and dates | met: below |
| 9 | The M1 audit exists | met: `M1-audit.md` |
| 10 | No change to accepted schemas or vocabulary values; no scores; no runtime; no relationship, product, facility or event record | met |
| 11 | Tests and Gate 0 pass in a fresh virtualenv; CI observed or reported | met locally; CI: not observed at this commit (L-08) |
| 12 | Report satisfies SPEC §5 and Part A; decisions appended as `proposed` | this report; D-054 to D-066 |

**Stop conditions that fired:** one. H-4's ISO stop fired on the first retrieval attempt
(`www.iso.org` refused), and the session asked before writing data. TSMC's and SK hynix's
access problems were put to the human in the same question.

## Files changed

Added:

- `docs/architecture/company-dataset.md`
- `docs/architecture/milestone-audits/M1-audit.md`
- `data/claims.json`, `data/companies.json`, `data/jurisdictions.json`
- `data/staging/companies.json`, `data/staging/jurisdictions.json` (empty at the end: every
  record was accepted)
- `tests/test_data_entities.py`, `tests/test_freshness.py`, `tests/fixtures/entity_records.json`
- `sessions/reports/SESSION-07-REPORT.md`

Modified:

- `data/sources.json`: `src-025` to `src-038` added; `publisher_entity` set on the 8 filings
  (`src-024` to `src-031`, D-065). Migrated values unchanged (VD-9 passes).
- `data/staging/claims.json`: emptied by promotion.
- `tests/test_data_integrity.py` (VD-11 extended), `tests/test_data_schema.py` (entity files
  and the fixture world in VD-2).
- `tools/trace.py`: reads the entity files by default; prints assertion values and states.
- `docs/architecture/decisions.md` (D-054 to D-066 appended), `docs/architecture/claim-model.md`
  (a status note on §16 only), `docs/agents/contracts.md` (paths only), `docs/README.md`,
  `docs/architecture/baseline.md` (dated state rows only), `docs/quality/audit-history.md`,
  `README.md`.

Not modified: the root documents; `domain-map.md`; `M0-audit.md`; both taxonomies; the
schemas; the frozen register; `.github/`; `requirements-test.txt`; `tools/validate_repo.py`;
`PROMPT-REGISTRY.md`; anything in `Eu-Digital-Policy`, which was not opened.

## Data changed

As measured at the final commit (produced by script, L-04):

| Measure | Count |
|---|---|
| source records | 38 (24 migrated; 14 new: 7 `company_filing`, 7 `standard_specification`) |
| new sources by method | `automated` 6, `manual_by_human` 8 (TSMC's 20-F and 7 ISO screenshots) |
| `publisher_entity` | set 8 (the filings), `not_researched` 15 (company web pages), `not_applicable` 15 |
| canonical claims | 62: `FACT` 43, `DERIVATION` 12, `ATTRIBUTION` 5, `INTERPRETATION` 1, `IMPLICATION` 1 |
| claims created in S07 | 52 (`FACT` 41, `DERIVATION` 11), with 53 citations |
| staging claims | 0 |
| companies | 8 canonical, 0 staging |
| jurisdictions | 4 canonical (US, NL, KR, TW), 0 staging |
| `incorporated_in` | `jurisdiction-us` 5, `-nl` 1, `-tw` 1; `not_researched` 1 (SK hynix) |
| `headquartered_in` | `jurisdiction-us` 5, `-nl` 1, `-kr` 1, `-tw` 1 |

**Data model:** no schema change. The entity schema accepted in S03 holds every record.

## Tests run

Python 3.11.15. "Fresh venv" means a virtualenv built from `requirements-test.txt` in the
session scratchpad.

| Command / check | Result |
|---|---|
| `python -m unittest discover -s tests` at start | OK (157 tests) |
| `python tools/validate_repo.py` at start | `Repository integrity: OK` |
| **Fail-first:** full suite with the checks written and no entity file | 178 tests, 2 failures: the two "entity file exists" tests. The record checks passed vacuously on empty sets; their power was shown on the fixture world, where every planted fault was caught |
| Reference test while the RA-4 files were pending | failed for each cited source and record that did not exist yet (12, then 2), and for a hypothetical ID written in backticks in the design document (fixed) |
| **Deliberate breaks**, first run (15 breaks, 7 companies in staging) | 14 caught; the display-name control passed; break 7b not caught (below) |
| **Deliberate breaks**, final run on the promoted data (18 breaks) | 16 caught, control 9b passes as it must, 7b not caught. Output below |
| `python -m unittest discover -s tests -v`, final, system Python | OK (181 tests: 157 before, 24 new) |
| The same, final, fresh venv; `pip freeze` sorted vs the pins | installed set = pinned set; OK (181) |
| `validate-data` (`-p "test_data*.py"`), final | OK (37 tests) |
| `validate-freshness` (`-p "test_freshness.py"`), final | OK (6 tests) |
| `python tools/validate_repo.py`, final | `Repository integrity: OK` |
| `python tools/trace.py` on 8 companies and 4 jurisdictions | exit 0 each; no `MISSING` |
| CI | not observed at the commit that adds this report (L-08) |

**Break 7b, not caught by design.** A role cited to a claim that does not state it (an
`idm` role resting on Amkor's name claim) passes every machine check: the claim has the right
class and standing. Whether a sentence states a business model is a reading judgement. The
Verifier and the human's review are the guard, as `company-dataset.md` §4 and §12 say.

Not applicable: browser, accessibility, performance.

## Evidence added/retired

**Retrieved by the session** (RA-1, plain HTTPS, 2026-10-01T05:33Z to 05:37Z):

- Micron, Amkor and Synopsys 10-Ks, Amazon's annual report (containing its 10-K) and ASML's
  20-F, each from the filer's own domain (`/files/` paths redirect to the filer's IR file
  host, as NVIDIA's did in S05).
- SK hynix's annual report, section I.1, from English DART (`regulator_hosted`, D-059).
- NVIDIA's 10-K (`src-024`) re-read: bytes unchanged since S05 (`a056b59e4170`).

**Supplied by the human** (RA-4):

- TSMC's 20-F, downloaded by the human from `investor.tsmc.com` and supplied through a share
  link (the chat's page limit refused it); read in full (244 pages); signature date
  2026-04-16; its internal modification date matches.
- Nine ISO OBP screenshots, seven registered (the NL and TW subdivision tables were not
  needed). The first five lacked the identity block and the address bar; the human sent four
  more on request.

**Verifier pass:**

- PDF and DART text: every anchor was searched in text extracted from the bytes read, found
  exactly once at its locator, and its sentence read in context. Two normalisations: runs of
  whitespace (as VD-11); and the space that PDF extraction puts between Chinese characters in
  TSMC's filing (the anchor keeps the true, unspaced text).
- Screenshots: no text layer. Each anchor was read off the image and copied verbatim, in
  reading order (row label, then value). The human, who took the images, accepted them.
- **The Verifier corrected itself once.** It first wrote TSMC's Articles page as "Exhibit
  1.1" before checking. The page before (p.178) was then read and does say "Exhibit 1.1".
  The S06 lesson holds: a locator is a claim too.

**Findings from reading** (recorded, not patched):

- **US filers name a state, not the country.** All five say Delaware. The country is therefore
  a `DERIVATION` through ISO 3166-2, shown as inferred (D-057).
- **TSMC's charter names the company in Chinese and English** (Article 1, p.179). The 20-F
  cover calls the English a translation. Both are recorded as legal names, as for SK hynix.
- **TSMC's filing says "R.O.C."** for its jurisdiction of incorporation and writes its head
  office as "Taiwan, Republic of China". The record points to ISO 3166's TW entry, whose short
  name is "TAIWAN, PROVINCE OF CHINA". The step is a `DERIVATION`, flagged to the human, and
  accepted. The code states no position on sovereignty (§3.6).
- **SK hynix's report section read states no jurisdiction of incorporation.** The field stays
  `not_researched`, rather than being inferred from the legal form.
- **ASML's 20-F has no cover page in the PDF read.** Identity rests on its governance sentence
  (p.76) and the 20-F signature page (p.349) identifies the document.

**Access gaps** (SP-7; nothing bypassed): `www.iso.org`, `investor.tsmc.com`, `pr.tsmc.com`,
the HTML pages of `investors.micron.com`, `investor.synopsys.com` and `ir.aboutamazon.com`,
`www.skhynix.com/ir/`, `findbiz.nat.gov.tw` (`company-dataset.md` §11). A Drive link first
returned a sign-in page; the session did not sign in (RA-7), and the human changed the
sharing setting.

**Retired:** none.

## Decisions made

| ID | Subject | Status |
|---|---|---|
| D-054 | The company seed and the legal-entity rulings (H-1) | proposed |
| D-055 | Entity data layout: one file per entity type (H-2) | proposed |
| D-056 | Company ID rule (ID-1) | proposed |
| D-057 | Claim patterns for company identity and attributes | proposed |
| D-058 | Jurisdiction records from ISO captures retrieved by the human (H-4, RA-4) | proposed |
| D-059 | Regulator-hosted filings readable under RA-1 (SK hynix) | proposed |
| D-060 | TSMC's 20-F by manual retrieval (RA-4) | proposed |
| D-061 | Staging and canonical for entity records; the human's review in S07 (H-3) | proposed |
| D-062 | Anchors from new retrievals are Verifier-attested (H-6) | proposed |
| D-063 | validate-data for entity records | proposed |
| D-064 | validate-freshness: the first rule (F-1) | proposed |
| D-065 | `publisher_entity` is set for filings only | proposed |
| D-066 | The M1 milestone audit is written first in S07 (H-5) | proposed |

**Main rejected alternatives** (each decision lists its own): IDs from display names or
tickers; a review field on entities; one entity file; a `FACT` that a Delaware company is
incorporated in the United States; cover addresses as headquarters; a secondary country-code
list; `publisher_entity` from copyright lines; a calendar-based freshness check; inferring
incorporation from a legal form.

## Deviations

1. **H-4's stop fired** on the first ISO request and was answered by the human before any data
   was written. The ISO evidence then came as **screenshots**, not saved pages. D-058 records
   it, and the dataset document says how image anchors are read.
2. **TSMC's 20-F arrived through a share link**, because the chat refused a 244-page PDF. The
   bytes are the file as downloaded; the record keeps TSMC's URL, where the human downloaded it.
3. **The milestone label.** Part A's "Milestone M1 complete." is read as the operational
   roadmap's week-3 checkpoint, as Part B §01 sets out. The human did not read it otherwise.
4. **The M1 audit was written in the Portfolio Reviewer role**, which `roles.md` marks inactive
   and gives no contract (D-066).
5. **The Change Detector stays inactive.** `roles.md` names S07 as its first active session,
   "with `validate-freshness`". The freshness check was built by the Data Auditor as a test;
   scheduled re-checks, the Change Detector's work, were not built (D-064).
6. **The S06 seed verdicts are recorded in this report**, where the human gave them, not in an
   addendum to the S06 report as `claim-model.md` §14 foresaw.
7. **Two review sheets.** Sheet 1 covered the seven companies whose evidence was in; sheet 2
   followed the RA-4 files. The human chose this ("Yes, review the 7 now").
8. **Checkpoint commits with known failures.** The environment's stop hook required each turn's
   work to be pushed. Five checkpoint commits went to the feature branch while the reference
   test failed for the pending RA-4 items, each saying so in its message. Nothing went to
   `main`.
9. **Amazon's source is its Annual Report**, which contains the full 10-K from p.12 after the
   shareholder letter, not a standalone 10-K file. Only 10-K pages are cited.
10. **Extractor and Verifier were one agent** (Claude), as in S06. The human's sample (3 claims
    on sheet 1) and the review of every claim are the independent check.

No part of Part A or Part B was skipped.

## Debt introduced/resolved

**Introduced:**

- **Role fit is not machine-checkable** (break 7b). It rests on reading and review.
- **Image anchors are attested only.** No text exists to check them against; they rest on the
  Verifier's reading and the human's acceptance.
- **Freshness does not age.** F-1 compares evidence with its verification date, so a canonical
  record does not go stale in CI as time passes (D-064). Micron's filing (signed 2025-10-03)
  is the first that a re-verification after 2026-10-03 would fail.
- **The extraction and promotion scripts lived in the session scratchpad**, not in the
  repository. Their effects are checked in CI, and each step is described here, but the
  scripts themselves are not reproducible from the repository.
- **Screenshot times are arrival times**, matched to the phone clock in two images, not a time
  the human recorded.
- **More Markdown parsing:** the legal-form table (§3) and the attestation date (§7) of
  `company-dataset.md`, each with a width or uniqueness assertion.

**Resolved:**

- V-1, V-9 and V-10, handed on by S04 and S06; the first `validate-freshness` rule (D-051's
  handoff); VD-11's scope for new anchors (H-6).
- ISO 3166 registered (`entity-taxonomy.md` §9; `source-policy.md` §7 row `identity:jurisdiction`).
- `publisher_entity` for filings (the S06 handoff, in part).
- The ten S06 seed claims' verdicts.
- PEF §4's missing M1 audit.

## Unresolved issues

### Evidence gaps

- SK hynix's jurisdiction of incorporation (`not_researched`).
- The AWS legal entity: whether a subsidiary publishes `src-010` and `src-020`; parent and
  subsidiary questions for every company (S10's `owns`).
- `publisher_entity` for the 15 company web pages.
- **Carried:** S05-R1's anchors hand-verified only; SRC-023 not re-read; the `source-policy.md`
  §2 class table vs the §7 matrix; the blocked primary sources (JEDEC, Samsung, EDGAR);
  CON-01 to CON-05, preserved.

### Human approvals required

1. **D-054 to D-066**, all `proposed`. The consequential ones: the ID rule (D-056); the
   state-to-country derivations (D-057); screenshots as ISO evidence (D-058); regulator copies
   (D-059); "use" as the verification date in F-1 (D-064).
2. **The M1 audit** (`M1-audit.md`), proposed.
3. **The operational roadmap's week-3 checkpoint** ("Milestone M1 complete"): a human
   judgement after S07.
4. **Still open from earlier sessions:** S01's weekly gate.
5. **Merging this branch:** no pull request has been opened.

## Process lessons

- **Reading the filings changed the model, again.** The state-not-country finding, TSMC's
  charter names and SK hynix's silence on incorporation were all found by reading sentences,
  not by tests. Each became a rule (D-057) before any record rested on it.
- **Plan the human's retrievals at the start.** The access probe in the first minutes found
  every refusal, so all three stop questions went to the human at once. The RA-4 files still
  took several rounds: the first screenshots missed the identity block, and the first link
  was private. *Ask for the exact rows and settings needed, with the reason.*
- **Review where the evidence is ready.** Splitting the review let the human accept seven
  companies while the files were pending, and kept each sheet small enough to read.
- **"Accept all" needs a scope.** The first one did not say whether the S06 seeds were
  included. The session asked rather than assumed, and recorded the interpretation next to
  the words.
- **A reference test catches prose, too.** It caught a hypothetical ID in backticks in a
  rejected-alternatives table, which would otherwise read as a real record.
- **A break is only as good as its target.** After promotion, the first-run breaks edited the
  emptied staging file; they were retargeted to the canonical files before the final run.

## Implications for the next session

**Handoff: S08, Technology + component dataset** (gate: "Definitions are sourced and do not
collapse technically distinct concepts").

- **Completed work:**
  - 8 canonical companies and 4 jurisdictions, all with reviewed evidence;
  - 14 new sources and their access gaps (`company-dataset.md` §11);
  - the record checks V-1, V-4, V-9, V-10, CE-1, ID-1, J-1 and F-1;
  - the M1 audit.
- **For S08:**
  - product `vendor` values point to these companies (V-1 checks it): `company-nvidia`,
    `company-sk-hynix`, `company-micron-technology`, `company-amazon-com` and the others;
  - the rows `identity:technology`, `identity:component` and `attr:*.definition` prefer
    standards, government and research sources. Expect the same access pattern as ISO: plan
    RA-4 requests early;
  - the S06 claims S08 can cite are now canonical: the working definition
    (`claim-atlas-ai-accelerator-working-definition`), CSET's and LBNL's definitions, NIST's
    cloud definition, and the GH100 process `FACT`;
  - V-10, CE-1 and F-1 already walk any entity type; S08 extends J-1-style checks only if its
    types need them, and adds `broader` acyclicity (`entity-taxonomy.md` §9).
- **Open issues:** the approvals above; parent and subsidiary questions for S10; S01's weekly
  gate; the S05 debt still open.
- **Recommended next decision:** the human confirms the ID rule (D-056) and the canonical
  companies before S08, because product `vendor` references depend on them.
- **Files for S08 to read first:**
  1. this report;
  2. `docs/architecture/company-dataset.md`;
  3. `docs/architecture/claim-model.md`;
  4. `schemas/entities.schema.json` (`technology`, `component`, `product`);
  5. `docs/architecture/entity-taxonomy.md` §3.3–§3.5, §5;
  6. `docs/research/source-policy.md` §7, §10;
  7. D-022, D-027 and D-054 to D-066.

**One next milestone:** S08 creates the first technology, component and product records, with
product vendors pointing to the S07 companies.

## Addendum — human review outcome, review sheet 1 (2026-10-01)

- **Sheet:** the 27 claims staged for the seven companies (reproduced below).
- **The human's words, verbatim:** "accept all"
- **Applied to:** the 27 claims on sheet 1. Each claim's `review` records `accepted`,
  `reviewer: human`, 2026-10-01 and this report, and the claims moved unchanged to
  `data/claims.json`. All seven company records rest only on these claims, so they moved to
  `data/companies.json` (D-061).
- **Not applied to:** the ten S06 seed claims. They were optional on the sheet and are not
  named in the verdict, so they stay `not_reviewed` in staging until the human says
  otherwise.
- **H-6 sample:** the human did not name which claims they opened. *Open:* asked again with
  sheet 2.

## Addendum — the human's spot-check of attested anchors (H-6, 2026-10-01)

- **Asked:** whether the human opened three claims at their locators: `claim-micron-registrant-name`
  (src-025 p.1), `claim-nvidia-fabless-strategy` (src-024 p.8) and
  `claim-asml-incorporated-netherlands` (src-029 p.309).
- **The human's words, verbatim:** "check all the three fines"
- **Recorded as:** the human opened all three at their locators, and found each anchor and
  sentence as the claim states. This is the H-6 sample for review sheet 1: 3 of 27 claims,
  one each of a cover-page identity, a role and an incorporation sentence.

## Addendum — the S06 seed claims and the screenshot date (2026-10-01)

- **Question put to the human:** "Did your 'accept all' also cover the ten S06 seed claims?
  Yes or no."
- **The human's words, verbatim:** "i accept all"
- **Recorded as:** yes. The ten S06 seed claims (their sheet: `SESSION-06-REPORT.md`, Review
  sheet) are accepted. Each claim's `review` records `accepted`, 2026-10-01 and this report,
  and the ten moved unchanged to `data/claims.json`. The verdict is recorded here, where the
  human gave it, and not in an addendum to the S06 report as `claim-model.md` §14 foresaw
  (deviation).
- **Not covered:** review sheet 2, which had not been sent. "Accept all" is not read as a
  verdict on claims the human has not seen.
- **Screenshot date, the human's words:** "i took them today" (2026-10-01). Each ISO source
  records the time the image reached the session, which matches the phone clock shown in two
  of the images (16:29 local, 14:29 UTC).

## Addendum — human review outcome, review sheet 2 (2026-10-01)

- **Sheet:** the 25 claims on the ISO evidence, the state-to-country steps and TSMC (reproduced
  below).
- **The human's words, verbatim:** "Accept all"
- **Applied to:** all 25 claims. Each claim's `review` records `accepted`, `reviewer: human`,
  2026-10-01 and this report, and the claims moved unchanged to `data/claims.json`.
- **Records moved or changed** (D-061): `jurisdiction-us`, `-nl`, `-kr` and `-tw` and
  `company-taiwan-semiconductor-manufacturing-company` moved to the canonical files; the seven
  canonical companies gained the `incorporated_in` and `headquartered_in` values the sheet
  listed (SK hynix: `headquartered_in` only). `src-031`'s `publisher_entity` names TSMC's
  record (D-065).
- **Included in that acceptance:** `claim-tsmc-incorporated-in-tw`, the step from the filing's
  "R.O.C." to the ISO 3166 entry TW, which the sheet flagged as the sensitive one.
- **H-6 sample for sheet 2:** the screenshots are the human's own captures. No TSMC claim was
  named as opened.

## Review sheets

### Review sheet 1 (as given to the human)

For each claim: open the URL, go to the locator, find the anchor, read the **whole sentence**, and answer: **does it say this, and no more?** Then give a verdict: **accept**, **reject**, or **wording too strong**.

`python tools/trace.py <record or claim ID>` prints the same chain. All 27 are `FACT`, standing `party`, status `supported`, verified 2026-10-01, `not_reviewed`.

#### NVIDIA — `company-nvidia`

Fields now: legal_name ['NVIDIA CORPORATION']; roles ['fabless_designer']; incorporated_in and headquartered_in wait for the ISO pages.

| Claim | Statement | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|
| `claim-nvidia-registrant-name` | The registrant of NVIDIA's Annual Report on Form 10-K for the fiscal year ended January 25, 2026 has the exact name “NVIDIA CORPORATION”, as specified in its charter. | src-024 · <https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf> · p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)' | “NVIDIA CORPORATION (Exact name of registrant as specified in its charter)” | Identity and legal name. Cover page: is the name above the label exactly this, capitals included? |
| `claim-nvidia-incorporation-history` | NVIDIA was incorporated in California in April 1993 and reincorporated in Delaware in April 1998. | src-024 · <https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf> · p.5, Item 1 'Business', the sentence beginning 'Headquartered in Santa Clara, California' | “NVIDIA was incorporated in California in April 1993 and reincorporated in Delaware in April 1998” | Kept for the incorporated_in derivation (California → Delaware, both US states). Does p.5 say exactly this? |
| `claim-nvidia-headquarters-santa-clara` | NVIDIA is headquartered in Santa Clara, California. | src-024 · <https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf> · p.5, Item 1 'Business', the sentence beginning 'Headquartered in Santa Clara, California' | “Headquartered in Santa Clara, California, NVIDIA was incorporated in California in April 1993” | Same sentence as above. Does it state the headquarters, and only the city and state? |
| `claim-nvidia-fabless-strategy` | NVIDIA utilizes a fabless and contracting manufacturing strategy: it partners with suppliers for all phases of manufacturing, including wafer fabrication, assembly, testing and packaging, and focuses its own resources on product design, quality assurance, marketing and customer support. | src-024 · <https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf> · p.8, 'Manufacturing', the sentence beginning 'We utilize a fabless and contracting manufacturing strategy'<br>src-024 · <https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf> · p.8, 'Manufacturing', the sentence beginning 'As a result, we can focus our resources' | “We utilize a fabless and contracting manufacturing strategy, whereby we employ and partner with key suppliers for all phases of the manufacturing process, including wafer fabrication, assembly, testing, and packaging”<br>“As a result, we can focus our resources on product design, quality assurance, marketing, and customer support” | Role fabless_designer. Do the two p.8 sentences state the business model the role's definition names (designs; buys fabrication, assembly, test and packaging from others)? |

#### Micron Technology — `company-micron-technology`

Fields now: legal_name ['Micron Technology, Inc.']; roles ['memory_manufacturer']; incorporated_in and headquartered_in wait for the ISO pages.

| Claim | Statement | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|
| `claim-micron-registrant-name` | The registrant of Micron's Annual Report on Form 10-K for the fiscal year ended August 28, 2025 has the exact name “Micron Technology, Inc.”, as specified in its charter. | src-025 · <https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf> · p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)' | “Micron Technology, Inc. (Exact name of registrant as specified in its charter)” | Identity and legal name (cover page). |
| `claim-micron-incorporation-state` | Micron Technology, Inc. states Delaware as its state or other jurisdiction of incorporation or organization. | src-025 · <https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf> · p.1, cover page, the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the IRS Employer Identification No. | “Delaware 75-1618004 (State or other jurisdiction of incorporation or organization)” | Cover-page form: the value 'Delaware' sits beside an IRS number. Is the locator clear about which value is which? |
| `claim-micron-headquarters-boise` | Micron's corporate headquarters are located in Boise, Idaho. | src-025 · <https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf> · p.47, Item 2 'Properties', the first sentence | “Our corporate headquarters are located in Boise, Idaho” | Item 2 'Properties'. Headquarters, not a fab: correct? |
| `claim-micron-manufactures-memory` | Micron manufactures its products, which include DRAM, NAND and NOR products, within its own facilities, and also uses subcontractors for certain manufacturing processes. | src-025 · <https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf> · p.13, 'Manufacturing', the first sentence<br>src-025 · <https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf> · p.13, 'Manufacturing', the sentence beginning 'Our DRAM, NAND, and NOR products' | “We manufacture our products within our own facilities located in Taiwan, Singapore, Japan, the United States, Malaysia, China, and India and also utilize subcontractors to perform certain manufacturing processes”<br>“Our DRAM, NAND, and NOR products share a number of common manufacturing processes” | Role memory_manufacturer. Two sentences: own facilities, and DRAM among the products. Together, enough? The HBM part of the role's definition is product-level and not claimed (ER-9). |

#### Amkor Technology — `company-amkor-technology`

Fields now: legal_name ['Amkor Technology, Inc.']; roles ['osat']; incorporated_in and headquartered_in wait for the ISO pages.

| Claim | Statement | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|
| `claim-amkor-registrant-name` | The registrant of Amkor's Annual Report on Form 10-K for the fiscal year ended December 31, 2025 has the exact name “Amkor Technology, Inc.”, as specified in its charter. | src-026 · <https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b> · p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)' | “Amkor Technology, Inc. (Exact name of registrant as specified in its charter)” | Identity and legal name (cover page). |
| `claim-amkor-incorporation-state` | Amkor Technology, Inc. states Delaware as its state or other jurisdiction of incorporation or organization. | src-026 · <https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b> · p.1, cover page, the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the I.R.S. Employer Identification Number | “Delaware 23-1722724 (State or other jurisdiction of incorporation or organization)” | Cover-page form, as Micron's. |
| `claim-amkor-us-headquartered-osat` | Amkor is a U.S. headquartered outsourced semiconductor assembly and test service provider (OSAT). | src-026 · <https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b> · p.7, Item 1 'Business', the sentence beginning 'As a U.S. headquartered OSAT'<br>src-026 · <https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b> · p.4, Item 1 'Business', 'Overview', the first sentence, where the abbreviation is defined (the sentence's superlative is not adopted, ER-5) | “As a U.S. headquartered OSAT”<br>“outsourced semiconductor assembly and test service provider (“OSAT”)” | Role osat, and later headquartered_in (it names 'U.S.' directly, so a FACT). p.4 is cited only for the acronym; its 'world's largest' is not adopted (ER-5). Agree? |

#### Synopsys — `company-synopsys`

Fields now: legal_name ['SYNOPSYS, INC.']; roles ['eda_vendor']; incorporated_in and headquartered_in wait for the ISO pages.

| Claim | Statement | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|
| `claim-synopsys-registrant-name` | The registrant of Synopsys's Annual Report on Form 10-K for the fiscal year ended October 31, 2025 has the exact name “SYNOPSYS, INC.”, as specified in its charter. | src-027 · <https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf> · p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)' | “SYNOPSYS, INC. (Exact name of registrant as specified in its charter)” | Identity and legal name (cover page, 'SYNOPSYS, INC.' in capitals). |
| `claim-synopsys-incorporation-state` | Synopsys, Inc. states Delaware as its state or other jurisdiction of incorporation or organization. | src-027 · <https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf> · p.1, cover page, the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the I.R.S. Employer Identification No. | “Delaware 56-1546236 (State or other jurisdiction of incorporation or organization)” | Cover-page form, as Micron's. |
| `claim-synopsys-headquarters-sunnyvale` | Synopsys's headquarters are located at 675 Almanor Avenue, Sunnyvale, California. | src-027 · <https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf> · p.6, Item 1 'Business', 'Corporate Information', the first sentence | “Our headquarters are located at 675 Almanor Avenue, Sunnyvale, California 94085” | 'Corporate Information', p.6. Headquarters address in California. |
| `claim-synopsys-sells-eda` | Synopsys's Design Automation segment includes an EDA revenue group, and Synopsys's EDA products automate tasks in chip design. | src-027 · <https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf> · p.7, 'Products and Services', 'Design Automation Segment', the first sentence<br>src-027 · <https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf> · p.7, the sentence beginning 'Our EDA products increase designer productivity' | “Our Design Automation segment includes the EDA, Ansys and Other revenue groups”<br>“Our EDA products increase designer productivity and efficiency by automating tasks” | Role eda_vendor. The superlative p.6 sentence ('global leader') was avoided; the p.7 segment sentence is used instead. Enough for 'makes and sells EDA tools'? |

#### Amazon — `company-amazon-com`

Fields now: legal_name ['AMAZON.COM, INC.']; roles ['cloud_provider']; incorporated_in and headquartered_in wait for the ISO pages.

| Claim | Statement | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|
| `claim-amazon-registrant-name` | The registrant of Amazon's Annual Report on Form 10-K for the fiscal year ended December 31, 2025 has the exact name “AMAZON.COM, INC.”, as specified in its charter. | src-028 · <https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf> · p.12 (the Form 10-K's cover page, which follows the shareholder letter), the name printed above the label '(Exact name of registrant as specified in its charter)' | “AMAZON.COM, INC. (Exact name of registrant as specified in its charter)” | Identity and legal name. The source is Amazon's Annual Report; the 10-K starts at p.12, after the shareholder letter. The record is AMAZON.COM, INC., not AWS. Agree? |
| `claim-amazon-incorporation-state` | Amazon.com, Inc. states Delaware as its state or other jurisdiction of incorporation or organization. | src-028 · <https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf> · p.12 (the Form 10-K's cover page), the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the I.R.S. Employer Identification No. | “Delaware 91-1646860 (State or other jurisdiction of incorporation or organization)” | Cover-page form, p.12. |
| `claim-amazon-headquarters-washington-virginia` | Amazon owns and leases its corporate headquarters in Washington's Puget Sound region and in Arlington, Virginia. | src-028 · <https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf> · p.29, Form 10-K Item 2 'Properties', the sentence after the facilities tables | “We own and lease our corporate headquarters in Washington’s Puget Sound region and Arlington, Virginia” | Two headquarters locations, both later derived to the US (Washington state, Virginia). Is 'Washington's Puget Sound region' the state? |
| `claim-amazon-provides-cloud-services` | Amazon provides cloud services to businesses, and through AWS offers on-demand technology services, including compute, storage and database services. | src-028 · <https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf> · p.23, Form 10-K Item 1A, under 'Our Commercial Agreements, Strategic Alliances, and Other Business Relationships Expose Us to Risks', the first sentence<br>src-028 · <https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf> · p.14, Form 10-K Item 1 'Business', 'Developers and Enterprises' | “We provide physical, e-commerce, and omnichannel retail, cloud services, and other services to businesses”<br>“through AWS, which offers a broad set of on-demand technology services, including compute, storage, database” | Role cloud_provider, with the next claim. p.23 is a risk-factor sentence; p.14 the business description. Enough? |
| `claim-amazon-operates-data-centers` | As of December 31, 2025, Amazon operated leased and owned facilities in the category 'Fulfillment, data centers, and other', in North America and internationally. | src-028 · <https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf> · p.29, Form 10-K Item 2 'Properties', the first sentence<br>src-028 · <https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf> · p.29, Form 10-K Item 2 'Properties', first table, column 'Description of Use', the rows for North America and International | “As of December 31, 2025, we operated the following facilities”<br>“Fulfillment, data centers, and other” | Supports the role definition's 'from facilities on its own premises': a table row 'Fulfillment, data centers, and other', owned and leased. Is a table row acceptable here? |

#### ASML — `company-asml-holding`

Fields now: legal_name ['ASML Holding N.V.']; roles ['equipment_maker']; incorporated_in and headquartered_in wait for the ISO pages.

| Claim | Statement | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|
| `claim-asml-holding-nv-company` | ASML Holding N.V. is a public limited liability company organized under Dutch law. | src-029 · <https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf> · p.76, 'Corporate governance', the sentence beginning 'ASML Holding N.V. is a public limited liability company' | “ASML Holding N.V. is a public limited liability company organized under Dutch law” | Identity and legal name. A governance sentence, not a 20-F cover (the PDF has no cover page; p.349 is the 20-F signature page). Acceptable? |
| `claim-asml-incorporated-netherlands` | ASML is incorporated in the Netherlands. | src-029 · <https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf> · p.309, Note on income taxes, 'Global Minimum Tax', the first sentence | “Global minimum tax legislation was enacted in the Netherlands, the jurisdiction in which ASML is incorporated” | incorporated_in, a FACT: the sentence names the Netherlands. Does 'ASML' mean the registrant here? |
| `claim-asml-headquarters-veldhoven` | ASML's headquarters are located in Veldhoven, the Netherlands. | src-029 · <https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf> · p.327, 'Facilities in EMEA', the first sentence | “Our headquarters, mainly manufacturing and R&D facilities, are located in Veldhoven, the Netherlands” | headquartered_in, a FACT naming the Netherlands. Headquarters, not a facility record (the campus is S09's). |
| `claim-asml-semiconductor-equipment` | ASML develops, produces, markets, sells, upgrades and services advanced semiconductor equipment systems, consisting of lithography, metrology and inspection systems. | src-029 · <https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf> · p.287, Note 3 'Segment disclosure', the first sentence | “for the development, production, marketing, sales, upgrading and servicing of advanced semiconductor equipment systems, consisting of lithography, metrology and inspection systems” | Role equipment_maker. 'holistic lithography solution provider' is not adopted; the anchor is the development/production part. |

#### SK hynix — `company-sk-hynix`

Fields now: legal_name ['에스케이하이닉스 주식회사', 'SK hynix Inc.']; roles ['memory_manufacturer']; incorporated_in and headquartered_in wait for the ISO pages.

| Claim | Statement | Source · locator | Anchor (verbatim) | What to look for |
|---|---|---|---|---|
| `claim-sk-hynix-legal-name` | The company's name is 에스케이하이닉스 주식회사, written in English as SK hynix Inc. (the Atlas's translation of the Korean sentence). | src-030 · <https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=4&offset=20380&length=52430&dtd=dart4.xsd> · I.1 'Company overview', item 나 (the company's legal and commercial names), the first sentence | “당사의 명칭은 에스케이하이닉스 주식회사이며, 영문으로는 SK hynix Inc.라고 표기합니다” | Korean anchor. My translation: 'The company's name is 에스케이하이닉스 주식회사, and in English it is written SK hynix Inc.' Faithful? Both names become legal_name values. |
| `claim-sk-hynix-head-office-gyeonggi` | SK hynix's head office address is 2091 Gyeongchung-daero, Icheon-si, Gyeonggi-do (the Atlas's translation of the Korean address). | src-030 · <https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=4&offset=20380&length=52430&dtd=dart4.xsd> · I.1 'Company overview', item 라 (head office address, telephone number and website), its heading and the address line | “본사의 주소, 전화번호, 홈페이지 주소 주소: 경기도 이천시 경충대로 2091” | Korean anchor: item 라's heading ('head office address, telephone number, website') and the address. Translation faithful? Later derived to KR via ISO 3166-2 (Gyeonggi-do). |
| `claim-sk-hynix-memory-products` | SK hynix's main manufactured products are memory semiconductor products such as DRAM, NAND Flash and MCP (Multi-chip Package) (the Atlas's translation of the Korean sentence). | src-030 · <https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=4&offset=20380&length=52430&dtd=dart4.xsd> · I.1 'Company overview', item 바 (main business), the first sentence | “현재 당사의 주력 생산제품은 DRAM, NAND Flash 및 MCP(Multi-chip Package)와 같은 메모리 반도체 제품입니다” | Korean anchor: 'Our main produced products are memory semiconductor products such as DRAM, NAND Flash and MCP.' Enough for memory_manufacturer? |

#### Your sample of attested anchors (H-6)

Please name the claims you opened yourself, so the report records your sample.

#### The S06 seed claims (optional)

The ten S06 seed claims still have no verdict. You may give them here too; their sheet is in `sessions/reports/SESSION-06-REPORT.md`.

### Review sheet 2 (as given to the human)

Same procedure as sheet 1: open the source at the locator, read the whole sentence (or the screenshot row), and answer **does it say this, and no more?** Verdict per claim: **accept**, **reject**, or **wording too strong**. You may answer "accept all" or "accept all except …".

The screenshots are yours, so for them you are checking that I copied the row correctly. TSMC's 20-F is at the `investor.tsmc.com` link (or your Drive copy).

#### Claims

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-iso-3166-1-us` | FACT | ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'. | src-032 · screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name' | “Alpha-2 code US Short name UNITED STATES OF AMERICA” | Screenshot src-032: rows 'Alpha-2 code' and 'Short name'. Read off the image. |
| `claim-iso-3166-1-nl` | FACT | ISO 3166 assigns the alpha-2 code NL to the entry with the short name “NETHERLANDS, KINGDOM OF THE” (full name “the Kingdom of the Netherlands”), with status 'Officially assigned'. | src-035 · screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name' | “Alpha-2 code NL Short name NETHERLANDS, KINGDOM OF THE” | Screenshot src-035, as above. |
| `claim-iso-3166-1-kr` | FACT | ISO 3166 assigns the alpha-2 code KR to the entry with the short name “KOREA, REPUBLIC OF” (full name “the Republic of Korea”), with status 'Officially assigned'. | src-036 · screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name' | “Alpha-2 code KR Short name KOREA, REPUBLIC OF” | Screenshot src-036, as above. |
| `claim-iso-3166-2-us-ca` | FACT | ISO 3166-2 lists California, of subdivision category 'state', with the code US-CA. | src-033 · screenshot of the subdivision table, the row for US-CA | “state US-CA California” | Screenshot src-033, the US-CA row. |
| `claim-iso-3166-2-us-de` | FACT | ISO 3166-2 lists Delaware, of subdivision category 'state', with the code US-DE. | src-033 · screenshot of the subdivision table, the row for US-DE | “state US-DE Delaware” | Screenshot src-033, the US-DE row. |
| `claim-iso-3166-2-us-id` | FACT | ISO 3166-2 lists Idaho, of subdivision category 'state', with the code US-ID. | src-033 · screenshot of the subdivision table, the row for US-ID | “state US-ID Idaho” | Screenshot src-033, the US-ID row. |
| `claim-iso-3166-2-us-va` | FACT | ISO 3166-2 lists Virginia, of subdivision category 'state', with the code US-VA. | src-034 · screenshot of the subdivision table, the row for US-VA | “state US-VA Virginia” | Screenshot src-034, the US-VA row. |
| `claim-iso-3166-2-us-wa` | FACT | ISO 3166-2 lists Washington, of subdivision category 'state', with the code US-WA. | src-034 · screenshot of the subdivision table, the row for US-WA | “state US-WA Washington” | Screenshot src-034, the US-WA row. |
| `claim-iso-3166-2-kr-41` | FACT | ISO 3166-2 lists Gyeonggi-do, of subdivision category 'province', with the code KR-41. | src-037 · screenshot of the subdivision table, the row for KR-41 | “province KR-41 Gyeonggi-do Gyeonggi” | Screenshot src-037, the KR-41 row (local variant 'Gyeonggi'). |
| `claim-iso-3166-1-tw` | FACT | ISO 3166 assigns the alpha-2 code TW to the entry with the short name “TAIWAN, PROVINCE OF CHINA” (its Full name row is empty), with status 'Officially assigned'. | src-038 · screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name' | “Alpha-2 code TW Short name TAIWAN, PROVINCE OF CHINA” | Screenshot src-038. ISO's short name is recorded exactly as ISO gives it; the code is an identifier and states no position on sovereignty (entity-taxonomy §3.6). Agree? |
| `claim-tsmc-legal-name` | FACT | TSMC's Articles of Incorporation give its name as 台灣積體電路製造股份有限公司 in the Chinese language and Taiwan Semiconductor Manufacturing Company Limited in the English language. The 20-F cover gives the Chinese name as the exact name in its charter, and the English name as its translation. | src-031 · p.179, Exhibit 1.1, Articles of Incorporation, Article 1<br>src-031 · p.20, Item 4, 'Our History and Structure', the first sentence<br>src-031 · p.1, cover page, the name printed above the label '(Exact Name of Registrant as Specified in Its Charter)'<br>src-031 · p.1, cover page, the English name and its label; the text runs on into the jurisdiction field beside it | “its name shall be 台灣積體電路製造股份有限公司 in the Chinese language, and Taiwan Semiconductor Manufacturing Company Limited in the English language”<br>“Our legal and commercial name is 台灣積體電路製造股份有限公司 (Taiwan Semiconductor Manufacturing Company Limited)”<br>“台灣積體電路製造股份有限公司 (Exact Name of Registrant as Specified in Its Charter)”<br>“Taiwan Semiconductor Manufacturing Company Limited Republic of China (Translation of Registrant’s Name Into English)” | Identity and legal name. The charter (Article 1, p.179) names the company in Chinese and in English; the cover calls the English a translation. Both names become legal_name values, as for SK hynix. Agree? |
| `claim-tsmc-incorporated-roc` | FACT | TSMC was incorporated in the R.O.C. (Republic of China) as a company limited by shares on February 21, 1987, under the Company Law of the Republic of China. | src-031 · p.179, Exhibit 1.1, Articles of Incorporation, Article 1<br>src-031 · p.20, Item 4, 'Our History and Structure', the second sentence<br>src-031 · p.108, Note 1 'General', the first sentence | “The Corporation shall be incorporated, as a company limited by shares, under the Company Law of the Republic of China”<br>“were incorporated in the R.O.C. as a company limited by shares on February 21, 1987”<br>“Taiwan Semiconductor Manufacturing Company Limited (TSMC), a Republic of China (R.O.C.) corporation, was incorporated on February 21, 1987” | The filing names the R.O.C. Does p.20 and p.108 say exactly this? |
| `claim-tsmc-head-office-taiwan` | FACT | TSMC's Articles of Incorporation place its head office in Hsinchu Science Park, Taiwan, Republic of China, and its corporate headquarters are located in the Hsinchu Science Park. | src-031 · p.180, Exhibit 1.1, Articles of Incorporation, Article 3<br>src-031 · p.21, Item 4, 'Our Semiconductor Facilities', the second sentence | “The Corporation shall have its head office in Hsinchu Science Park, Taiwan, Republic of China”<br>“Our corporate headquarters and nine of our fabs are located in the Hsinchu Science Park” | headquartered_in, a FACT: the Articles name 'Taiwan, Republic of China'. 'shall have its head office' is a charter rule, read with p.21's present-tense headquarters sentence. Enough? |
| `claim-tsmc-foundry` | FACT | As a foundry, TSMC manufactures semiconductors with its own manufacturing processes for its customers, based on proprietary integrated circuit designs that the customers provide. | src-031 · p.21, Item 4, 'Business Overview of the Company', the first sentence | “As a foundry, we manufacture semiconductors using our manufacturing processes for our customers based on proprietary integrated circuit designs provided by them” | Role foundry_operator. The 'technology leader' sentences were avoided (ER-5). |
| `claim-tsmc-incorporated-in-tw` | DERIVATION | TSMC's jurisdiction of incorporation is recorded as the ISO 3166 entry with code TW. | — | inputs: `claim-tsmc-incorporated-roc`, `claim-tsmc-head-office-taiwan`, `claim-iso-3166-1-tw`<br>reasoning: The filing names the jurisdiction of incorporation as the R.O.C. (claim-tsmc-incorporated-roc). The same filing writes the head office's place as 'Taiwan, Republic of China', using both names for one place (claim-tsmc-head-office-taiwan). ISO 3166 assigns the code TW to the entry whose short name is 'TAIWAN, PROVINCE OF CHINA' (claim-iso-3166-1-tw). So the Atlas records the entry TW. The code is an identifier and states no position on sovereignty (entity-taxonomy.md §3.6); the filing's own name for the jurisdiction stays in its claim. The step is the Atlas's (D-057). | The sensitive step: the filing says 'R.O.C.'; the Atlas records ISO entry TW, because the filing itself writes 'Taiwan, Republic of China' for the head office's place. Accept this step, or keep TSMC's incorporated_in not_researched? |
| `claim-nvidia-incorporated-in-us` | DERIVATION | NVIDIA's jurisdiction of incorporation, since April 1993, is in the country with ISO 3166 code US (California, then Delaware). | — | inputs: `claim-nvidia-incorporation-history`, `claim-iso-3166-2-us-ca`, `claim-iso-3166-2-us-de`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-nvidia-incorporation-history). ISO 3166-2 lists it as US-CA and US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-nvidia-headquartered-in-us` | DERIVATION | NVIDIA's headquarters is in the country with ISO 3166 code US (Santa Clara, California). | — | inputs: `claim-nvidia-headquarters-santa-clara`, `claim-iso-3166-2-us-ca`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-nvidia-headquarters-santa-clara). ISO 3166-2 lists it as US-CA. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-micron-incorporated-in-us` | DERIVATION | Micron Technology, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware). | — | inputs: `claim-micron-incorporation-state`, `claim-iso-3166-2-us-de`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-micron-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-micron-headquartered-in-us` | DERIVATION | Micron's headquarters is in the country with ISO 3166 code US (Boise, Idaho). | — | inputs: `claim-micron-headquarters-boise`, `claim-iso-3166-2-us-id`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-micron-headquarters-boise). ISO 3166-2 lists it as US-ID. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-amkor-incorporated-in-us` | DERIVATION | Amkor Technology, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware). | — | inputs: `claim-amkor-incorporation-state`, `claim-iso-3166-2-us-de`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-amkor-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-synopsys-incorporated-in-us` | DERIVATION | Synopsys, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware). | — | inputs: `claim-synopsys-incorporation-state`, `claim-iso-3166-2-us-de`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-synopsys-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-synopsys-headquartered-in-us` | DERIVATION | Synopsys's headquarters is in the country with ISO 3166 code US (Sunnyvale, California). | — | inputs: `claim-synopsys-headquarters-sunnyvale`, `claim-iso-3166-2-us-ca`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-synopsys-headquarters-sunnyvale). ISO 3166-2 lists it as US-CA. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-amazon-incorporated-in-us` | DERIVATION | Amazon.com, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware). | — | inputs: `claim-amazon-incorporation-state`, `claim-iso-3166-2-us-de`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-amazon-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-amazon-headquartered-in-us` | DERIVATION | Amazon's corporate headquarters is in the country with ISO 3166 code US (Washington's Puget Sound region and Arlington, Virginia). | — | inputs: `claim-amazon-headquarters-washington-virginia`, `claim-iso-3166-2-us-wa`, `claim-iso-3166-2-us-va`, `claim-iso-3166-1-us`<br>reasoning: The filing names a subdivision, not the country (claim-amazon-headquarters-washington-virginia). ISO 3166-2 lists it as US-WA and US-VA. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057). | Does each input say what the reasoning says, and does the step hold? It is shown as inferred, never as the filing's statement. |
| `claim-sk-hynix-headquartered-in-kr` | DERIVATION | SK hynix's head office is in the country with ISO 3166 code KR (경기도, which ISO lists as Gyeonggi-do; the romanisation is part of this step). | — | inputs: `claim-sk-hynix-head-office-gyeonggi`, `claim-iso-3166-2-kr-41`, `claim-iso-3166-1-kr`<br>reasoning: The filing names a subdivision, not the country (claim-sk-hynix-head-office-gyeonggi). ISO 3166-2 lists it as KR-41. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is KR (claim-iso-3166-1-kr). So the country is the one coded KR. The step is the Atlas's, not the filing's (D-057). | 경기도 → ISO 'Gyeonggi-do' (KR-41) is a romanisation step. Faithful? |

#### What your verdicts change

If you accept the claims they rest on, these records become canonical or change:

- **New canonical jurisdictions:** `jurisdiction-us` (United States), `jurisdiction-nl` (Netherlands), `jurisdiction-kr` (Republic of Korea), `jurisdiction-tw` (Taiwan). Display names are editorial; ISO's names are kept as aliases.
- **TSMC** (`company-taiwan-semiconductor-manufacturing-company`): legal names in Chinese and English; incorporated_in TW from 1987-02-21; headquartered_in TW; role foundry_operator.
- **The seven canonical companies gain these fields** (all other fields unchanged):

  - `company-nvidia`: incorporated_in = jurisdiction-us (from 1993-04) via `claim-nvidia-incorporated-in-us`; headquartered_in = jurisdiction-us via `claim-nvidia-headquartered-in-us`
  - `company-micron-technology`: incorporated_in = jurisdiction-us via `claim-micron-incorporated-in-us`; headquartered_in = jurisdiction-us via `claim-micron-headquartered-in-us`
  - `company-amkor-technology`: incorporated_in = jurisdiction-us via `claim-amkor-incorporated-in-us`; headquartered_in = jurisdiction-us via `claim-amkor-us-headquartered-osat`
  - `company-synopsys`: incorporated_in = jurisdiction-us via `claim-synopsys-incorporated-in-us`; headquartered_in = jurisdiction-us via `claim-synopsys-headquartered-in-us`
  - `company-amazon-com`: incorporated_in = jurisdiction-us via `claim-amazon-incorporated-in-us`; headquartered_in = jurisdiction-us via `claim-amazon-headquartered-in-us`
  - `company-asml-holding`: incorporated_in = jurisdiction-nl via `claim-asml-incorporated-netherlands`; headquartered_in = jurisdiction-nl via `claim-asml-headquarters-veldhoven`
  - `company-sk-hynix`: headquartered_in = jurisdiction-kr via `claim-sk-hynix-headquartered-in-kr`

SK hynix's incorporated_in stays not_researched: no sentence read states it.
A rejected claim leaves its field as it is now (not_researched), and nothing else changes.

## Deliberate breaks, final run

Each break ran in a fresh scratch copy of the working tree, with the promoted data. The list
shows which tests failed.

```text
## 1 company cites a claim that does not exist: caught
   - test_data_entities.EntityDataTests.test_ce1_canonical_records_rest_on_canonical_claims
   - test_data_entities.EntityDataTests.test_v10_fields_rest_on_allowed_classes_and_standing
   - test_data_entities.EntityDataTests.test_v1_references_resolve

## 2 incorporated_in points to a missing jurisdiction: caught
   - test_data_entities.EntityDataTests.test_v1_references_resolve

## 3 identity claim from a class identity:company never allows alone: caught
   - test_freshness.FreshnessTests.test_f1_real_records_rest_on_fresh_evidence
   - test_data_entities.EntityDataTests.test_v10_fields_rest_on_allowed_classes_and_standing
   - test_data_integrity.IntegrityTests.test_vd10_facts_rest_on_a_sufficient_class

## 4 identity claim with reporter standing: caught
   - test_freshness.FreshnessTests.test_f1_real_records_rest_on_fresh_evidence
   - test_data_entities.EntityDataTests.test_v10_fields_rest_on_allowed_classes_and_standing
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid

## 5 canonical company cites a staging claim: caught
   - test_data_entities.EntityDataTests.test_ce1_canonical_records_rest_on_canonical_claims

## 6 placeholder slug company-unknown: caught
   - test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist
   - test_data_entities.EntityDataTests.test_id1_company_ids_follow_the_rule
   - test_data_entities.EntityDataTests.test_v1_references_resolve
   - test_data_entities.EntityDataTests.test_v9_no_placeholder_ids

## 7 role asserted with no claim: caught
   - test_freshness.FreshnessTests.test_f1_real_records_rest_on_fresh_evidence
   - test_data_entities.EntityDataTests.test_v10_fields_rest_on_allowed_classes_and_standing
   - test_data_schema.DataSchemaTests.test_vd2_every_record_is_valid

## 7b role asserted with a claim that does not state it (an identity claim): NOT CAUGHT

## 8 time_sensitive value older than 12 months, not re-checked: caught
   - test_freshness.FreshnessTests.test_f1_real_records_rest_on_fresh_evidence

## 9 ID built from the display name (a bad rule): caught
   - test_data_entities.DocumentReferenceTests.test_cited_sources_claims_and_records_exist
   - test_data_entities.EntityDataTests.test_id1_company_ids_follow_the_rule
   - test_data_entities.EntityDataTests.test_v1_references_resolve

## 9b display name changed under the real rule (must NOT fail): passes, as it must

## 10 attested anchor read from other bytes: caught
   - test_data_integrity.IntegrityTests.test_vd11_anchors_are_verbatim_in_their_home

## 11 S06 seed anchor changed by one word (regression of the H-6 change): caught
   - test_data_integrity.IntegrityTests.test_vd11_anchors_are_verbatim_in_their_home

## 12 publisher_entity points to a staging company: caught
   - test_data_entities.EntityDataTests.test_v1_references_resolve

## 13 valid_from after valid_to: caught
   - test_data_entities.EntityDataTests.test_v4_periods_are_ordered

## 14 duplicate company ID in canonical: caught
   - test_data_entities.EntityDataTests.test_ce1_canonical_records_rest_on_canonical_claims

## 15 jurisdiction code not carried by its ISO anchor: caught
   - test_data_entities.EntityDataTests.test_j1_jurisdiction_codes_are_on_the_iso_list

## 16 TSMC rests on an over-old filing (freshness): caught
   - test_freshness.FreshnessTests.test_f1_real_records_rest_on_fresh_evidence
```

## Trace of every canonical record (Part B §13)

<details>
<summary>python tools/trace.py on the 8 companies and 4 jurisdictions</summary>

```text
$ python tools/trace.py company-nvidia
company-nvidia · company record · canonical companies.json
  NVIDIA
  /identity_claim_ids:
    claim-nvidia-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: The registrant of NVIDIA's Annual Report on Form 10-K for the fiscal year ended January 25, 2026 has the exact name “NVIDIA CORPORATION”, as specified in its charter.
      as of: not_stated
      citation 1 · src-024 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended January 25, 2026" · NVIDIA Corporation · https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf
        class: company_filing · publisher record: company-nvidia
        stated dates: signed 2026-02-25
        registered: automated 2026-09-30T16:57Z sha256 a056b59e4170 · migrated from S05-R1
        filing copy: filer_hosted_not_checked
        locator: p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)'
        anchor: "NVIDIA CORPORATION (Exact name of registrant as specified in its charter)"
        read by the Verifier: 2026-10-01T05:33Z sha256 a056b59e4170 (same bytes as registered)
  /legal_name/0/claim_ids: NVIDIA CORPORATION
    claim-nvidia-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /incorporated_in/0/claim_ids: jurisdiction-us
    claim-nvidia-incorporated-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: NVIDIA's jurisdiction of incorporation, since April 1993, is in the country with ISO 3166 code US (California, then Delaware).
      reasoning: The filing names a subdivision, not the country (claim-nvidia-incorporation-history). ISO 3166-2 lists it as US-CA and US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-nvidia-incorporation-history · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: NVIDIA was incorporated in California in April 1993 and reincorporated in Delaware in April 1998.
          as of: not_stated
          citation 1 · src-024 · standing party
            source: "Annual Report on Form 10-K for the fiscal year ended January 25, 2026" · NVIDIA Corporation · https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf
            class: company_filing · publisher record: company-nvidia
            stated dates: signed 2026-02-25
            registered: automated 2026-09-30T16:57Z sha256 a056b59e4170 · migrated from S05-R1
            filing copy: filer_hosted_not_checked
            locator: p.5, Item 1 'Business', the sentence beginning 'Headquartered in Santa Clara, California'
            anchor: "NVIDIA was incorporated in California in April 1993 and reincorporated in Delaware in April 1998"
            read by the Verifier: 2026-10-01T05:33Z sha256 a056b59e4170 (same bytes as registered)
      input:
        claim-iso-3166-2-us-ca · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists California, of subdivision category 'state', with the code US-CA.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-CA
            anchor: "state US-CA California"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-2-us-de · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Delaware, of subdivision category 'state', with the code US-DE.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-DE
            anchor: "state US-DE Delaware"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-032 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 d02a4287f81268386a9f61a3b8d64b96460ca1cdb4b8f4d5e0a61ac4362ecda0
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code US Short name UNITED STATES OF AMERICA"
            read by the Verifier: 2026-10-01T14:30Z sha256 d02a4287f812 (same bytes as registered)
  /headquartered_in/0/claim_ids: jurisdiction-us
    claim-nvidia-headquartered-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: NVIDIA's headquarters is in the country with ISO 3166 code US (Santa Clara, California).
      reasoning: The filing names a subdivision, not the country (claim-nvidia-headquarters-santa-clara). ISO 3166-2 lists it as US-CA. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-nvidia-headquarters-santa-clara · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: NVIDIA is headquartered in Santa Clara, California.
          as of: not_stated
          citation 1 · src-024 · standing party
            source: "Annual Report on Form 10-K for the fiscal year ended January 25, 2026" · NVIDIA Corporation · https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf
            class: company_filing · publisher record: company-nvidia
            stated dates: signed 2026-02-25
            registered: automated 2026-09-30T16:57Z sha256 a056b59e4170 · migrated from S05-R1
            filing copy: filer_hosted_not_checked
            locator: p.5, Item 1 'Business', the sentence beginning 'Headquartered in Santa Clara, California'
            anchor: "Headquartered in Santa Clara, California, NVIDIA was incorporated in California in April 1993"
            read by the Verifier: 2026-10-01T05:33Z sha256 a056b59e4170 (same bytes as registered)
      input:
        claim-iso-3166-2-us-ca · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          (shown above)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          (shown above)
  /roles/0/claim_ids: fabless_designer
    claim-nvidia-fabless-strategy · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: NVIDIA utilizes a fabless and contracting manufacturing strategy: it partners with suppliers for all phases of manufacturing, including wafer fabrication, assembly, testing and packaging, and focuses its own resources on product design, quality assurance, marketing and customer support.
      as of: not_stated
      citation 1 · src-024 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended January 25, 2026" · NVIDIA Corporation · https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf
        class: company_filing · publisher record: company-nvidia
        stated dates: signed 2026-02-25
        registered: automated 2026-09-30T16:57Z sha256 a056b59e4170 · migrated from S05-R1
        filing copy: filer_hosted_not_checked
        locator: p.8, 'Manufacturing', the sentence beginning 'We utilize a fabless and contracting manufacturing strategy'
        anchor: "We utilize a fabless and contracting manufacturing strategy, whereby we employ and partner with key suppliers for all phases of the manufacturing process, including wafer fabrication, assembly, testing, and packaging"
        read by the Verifier: 2026-10-01T05:33Z sha256 a056b59e4170 (same bytes as registered)
      citation 2 · src-024 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended January 25, 2026" · NVIDIA Corporation · https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf
        class: company_filing · publisher record: company-nvidia
        stated dates: signed 2026-02-25
        registered: automated 2026-09-30T16:57Z sha256 a056b59e4170 · migrated from S05-R1
        filing copy: filer_hosted_not_checked
        locator: p.8, 'Manufacturing', the sentence beginning 'As a result, we can focus our resources'
        anchor: "As a result, we can focus our resources on product design, quality assurance, marketing, and customer support"
        read by the Verifier: 2026-10-01T05:33Z sha256 a056b59e4170 (same bytes as registered)
(exit 0)

$ python tools/trace.py company-micron-technology
company-micron-technology · company record · canonical companies.json
  Micron Technology
  /identity_claim_ids:
    claim-micron-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: The registrant of Micron's Annual Report on Form 10-K for the fiscal year ended August 28, 2025 has the exact name “Micron Technology, Inc.”, as specified in its charter.
      as of: not_stated
      citation 1 · src-025 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended August 28, 2025" · Micron Technology, Inc. · https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf
        class: company_filing · publisher record: company-micron-technology
        stated dates: signed 2025-10-03
        registered: automated 2026-10-01T05:33Z sha256 4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9
        filing copy: filer_hosted_not_checked
        locator: p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)'
        anchor: "Micron Technology, Inc. (Exact name of registrant as specified in its charter)"
        read by the Verifier: 2026-10-01T05:33Z sha256 4b50d54e91da (same bytes as registered)
  /legal_name/0/claim_ids: Micron Technology, Inc.
    claim-micron-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /incorporated_in/0/claim_ids: jurisdiction-us
    claim-micron-incorporated-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Micron Technology, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware).
      reasoning: The filing names a subdivision, not the country (claim-micron-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-micron-incorporation-state · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: Micron Technology, Inc. states Delaware as its state or other jurisdiction of incorporation or organization.
          as of: not_stated
          citation 1 · src-025 · standing party
            source: "Annual Report on Form 10-K for the fiscal year ended August 28, 2025" · Micron Technology, Inc. · https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf
            class: company_filing · publisher record: company-micron-technology
            stated dates: signed 2025-10-03
            registered: automated 2026-10-01T05:33Z sha256 4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9
            filing copy: filer_hosted_not_checked
            locator: p.1, cover page, the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the IRS Employer Identification No.
            anchor: "Delaware 75-1618004 (State or other jurisdiction of incorporation or organization)"
            read by the Verifier: 2026-10-01T05:33Z sha256 4b50d54e91da (same bytes as registered)
      input:
        claim-iso-3166-2-us-de · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Delaware, of subdivision category 'state', with the code US-DE.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-DE
            anchor: "state US-DE Delaware"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-032 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 d02a4287f81268386a9f61a3b8d64b96460ca1cdb4b8f4d5e0a61ac4362ecda0
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code US Short name UNITED STATES OF AMERICA"
            read by the Verifier: 2026-10-01T14:30Z sha256 d02a4287f812 (same bytes as registered)
  /headquartered_in/0/claim_ids: jurisdiction-us
    claim-micron-headquartered-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Micron's headquarters is in the country with ISO 3166 code US (Boise, Idaho).
      reasoning: The filing names a subdivision, not the country (claim-micron-headquarters-boise). ISO 3166-2 lists it as US-ID. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-micron-headquarters-boise · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: Micron's corporate headquarters are located in Boise, Idaho.
          as of: not_stated
          citation 1 · src-025 · standing party
            source: "Annual Report on Form 10-K for the fiscal year ended August 28, 2025" · Micron Technology, Inc. · https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf
            class: company_filing · publisher record: company-micron-technology
            stated dates: signed 2025-10-03
            registered: automated 2026-10-01T05:33Z sha256 4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9
            filing copy: filer_hosted_not_checked
            locator: p.47, Item 2 'Properties', the first sentence
            anchor: "Our corporate headquarters are located in Boise, Idaho"
            read by the Verifier: 2026-10-01T05:33Z sha256 4b50d54e91da (same bytes as registered)
      input:
        claim-iso-3166-2-us-id · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Idaho, of subdivision category 'state', with the code US-ID.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-ID
            anchor: "state US-ID Idaho"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          (shown above)
  /roles/0/claim_ids: memory_manufacturer
    claim-micron-manufactures-memory · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Micron manufactures its products, which include DRAM, NAND and NOR products, within its own facilities, and also uses subcontractors for certain manufacturing processes.
      as of: not_stated
      citation 1 · src-025 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended August 28, 2025" · Micron Technology, Inc. · https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf
        class: company_filing · publisher record: company-micron-technology
        stated dates: signed 2025-10-03
        registered: automated 2026-10-01T05:33Z sha256 4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9
        filing copy: filer_hosted_not_checked
        locator: p.13, 'Manufacturing', the first sentence
        anchor: "We manufacture our products within our own facilities located in Taiwan, Singapore, Japan, the United States, Malaysia, China, and India and also utilize subcontractors to perform certain manufacturing processes"
        read by the Verifier: 2026-10-01T05:33Z sha256 4b50d54e91da (same bytes as registered)
      citation 2 · src-025 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended August 28, 2025" · Micron Technology, Inc. · https://investors.micron.com/files/doc_financials/2025/ar/2025-Form-10-K.pdf
        class: company_filing · publisher record: company-micron-technology
        stated dates: signed 2025-10-03
        registered: automated 2026-10-01T05:33Z sha256 4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9
        filing copy: filer_hosted_not_checked
        locator: p.13, 'Manufacturing', the sentence beginning 'Our DRAM, NAND, and NOR products'
        anchor: "Our DRAM, NAND, and NOR products share a number of common manufacturing processes"
        read by the Verifier: 2026-10-01T05:33Z sha256 4b50d54e91da (same bytes as registered)
(exit 0)

$ python tools/trace.py company-amkor-technology
company-amkor-technology · company record · canonical companies.json
  Amkor Technology
  /identity_claim_ids:
    claim-amkor-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: The registrant of Amkor's Annual Report on Form 10-K for the fiscal year ended December 31, 2025 has the exact name “Amkor Technology, Inc.”, as specified in its charter.
      as of: not_stated
      citation 1 · src-026 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended December 31, 2025" · Amkor Technology, Inc. · https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b
        class: company_filing · publisher record: company-amkor-technology
        stated dates: signed 2026-02-20
        registered: automated 2026-10-01T05:33Z sha256 e73f374e6925226c9f632287899f6ee9ecd71ec94c5c1022966887b85b94dc0d
        filing copy: filer_hosted_not_checked
        locator: p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)'
        anchor: "Amkor Technology, Inc. (Exact name of registrant as specified in its charter)"
        read by the Verifier: 2026-10-01T05:33Z sha256 e73f374e6925 (same bytes as registered)
  /legal_name/0/claim_ids: Amkor Technology, Inc.
    claim-amkor-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /incorporated_in/0/claim_ids: jurisdiction-us
    claim-amkor-incorporated-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Amkor Technology, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware).
      reasoning: The filing names a subdivision, not the country (claim-amkor-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-amkor-incorporation-state · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: Amkor Technology, Inc. states Delaware as its state or other jurisdiction of incorporation or organization.
          as of: not_stated
          citation 1 · src-026 · standing party
            source: "Annual Report on Form 10-K for the fiscal year ended December 31, 2025" · Amkor Technology, Inc. · https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b
            class: company_filing · publisher record: company-amkor-technology
            stated dates: signed 2026-02-20
            registered: automated 2026-10-01T05:33Z sha256 e73f374e6925226c9f632287899f6ee9ecd71ec94c5c1022966887b85b94dc0d
            filing copy: filer_hosted_not_checked
            locator: p.1, cover page, the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the I.R.S. Employer Identification Number
            anchor: "Delaware 23-1722724 (State or other jurisdiction of incorporation or organization)"
            read by the Verifier: 2026-10-01T05:33Z sha256 e73f374e6925 (same bytes as registered)
      input:
        claim-iso-3166-2-us-de · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Delaware, of subdivision category 'state', with the code US-DE.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-DE
            anchor: "state US-DE Delaware"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-032 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 d02a4287f81268386a9f61a3b8d64b96460ca1cdb4b8f4d5e0a61ac4362ecda0
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code US Short name UNITED STATES OF AMERICA"
            read by the Verifier: 2026-10-01T14:30Z sha256 d02a4287f812 (same bytes as registered)
  /headquartered_in/0/claim_ids: jurisdiction-us
    claim-amkor-us-headquartered-osat · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Amkor is a U.S. headquartered outsourced semiconductor assembly and test service provider (OSAT).
      as of: not_stated
      citation 1 · src-026 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended December 31, 2025" · Amkor Technology, Inc. · https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b
        class: company_filing · publisher record: company-amkor-technology
        stated dates: signed 2026-02-20
        registered: automated 2026-10-01T05:33Z sha256 e73f374e6925226c9f632287899f6ee9ecd71ec94c5c1022966887b85b94dc0d
        filing copy: filer_hosted_not_checked
        locator: p.7, Item 1 'Business', the sentence beginning 'As a U.S. headquartered OSAT'
        anchor: "As a U.S. headquartered OSAT"
        read by the Verifier: 2026-10-01T05:33Z sha256 e73f374e6925 (same bytes as registered)
      citation 2 · src-026 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended December 31, 2025" · Amkor Technology, Inc. · https://ir.amkor.com/static-files/ab60f0aa-e0e8-433f-9a27-191c6ff48b5b
        class: company_filing · publisher record: company-amkor-technology
        stated dates: signed 2026-02-20
        registered: automated 2026-10-01T05:33Z sha256 e73f374e6925226c9f632287899f6ee9ecd71ec94c5c1022966887b85b94dc0d
        filing copy: filer_hosted_not_checked
        locator: p.4, Item 1 'Business', 'Overview', the first sentence, where the abbreviation is defined (the sentence's superlative is not adopted, ER-5)
        anchor: "outsourced semiconductor assembly and test service provider (“OSAT”)"
        read by the Verifier: 2026-10-01T05:33Z sha256 e73f374e6925 (same bytes as registered)
  /roles/0/claim_ids: osat
    claim-amkor-us-headquartered-osat · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
(exit 0)

$ python tools/trace.py company-synopsys
company-synopsys · company record · canonical companies.json
  Synopsys
  /identity_claim_ids:
    claim-synopsys-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: The registrant of Synopsys's Annual Report on Form 10-K for the fiscal year ended October 31, 2025 has the exact name “SYNOPSYS, INC.”, as specified in its charter.
      as of: not_stated
      citation 1 · src-027 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended October 31, 2025" · Synopsys, Inc. · https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf
        class: company_filing · publisher record: company-synopsys
        stated dates: signed 2025-12-19
        registered: automated 2026-10-01T05:33Z sha256 f9ee4e270742e7d364fc911adff20682eda7f8c2a43ee6fee90ff16d8718a905
        filing copy: filer_hosted_not_checked
        locator: p.1, cover page, the name printed above the label '(Exact name of registrant as specified in its charter)'
        anchor: "SYNOPSYS, INC. (Exact name of registrant as specified in its charter)"
        read by the Verifier: 2026-10-01T05:33Z sha256 f9ee4e270742 (same bytes as registered)
  /legal_name/0/claim_ids: SYNOPSYS, INC.
    claim-synopsys-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /incorporated_in/0/claim_ids: jurisdiction-us
    claim-synopsys-incorporated-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Synopsys, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware).
      reasoning: The filing names a subdivision, not the country (claim-synopsys-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-synopsys-incorporation-state · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: Synopsys, Inc. states Delaware as its state or other jurisdiction of incorporation or organization.
          as of: not_stated
          citation 1 · src-027 · standing party
            source: "Annual Report on Form 10-K for the fiscal year ended October 31, 2025" · Synopsys, Inc. · https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf
            class: company_filing · publisher record: company-synopsys
            stated dates: signed 2025-12-19
            registered: automated 2026-10-01T05:33Z sha256 f9ee4e270742e7d364fc911adff20682eda7f8c2a43ee6fee90ff16d8718a905
            filing copy: filer_hosted_not_checked
            locator: p.1, cover page, the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the I.R.S. Employer Identification No.
            anchor: "Delaware 56-1546236 (State or other jurisdiction of incorporation or organization)"
            read by the Verifier: 2026-10-01T05:33Z sha256 f9ee4e270742 (same bytes as registered)
      input:
        claim-iso-3166-2-us-de · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Delaware, of subdivision category 'state', with the code US-DE.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-DE
            anchor: "state US-DE Delaware"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-032 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 d02a4287f81268386a9f61a3b8d64b96460ca1cdb4b8f4d5e0a61ac4362ecda0
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code US Short name UNITED STATES OF AMERICA"
            read by the Verifier: 2026-10-01T14:30Z sha256 d02a4287f812 (same bytes as registered)
  /headquartered_in/0/claim_ids: jurisdiction-us
    claim-synopsys-headquartered-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Synopsys's headquarters is in the country with ISO 3166 code US (Sunnyvale, California).
      reasoning: The filing names a subdivision, not the country (claim-synopsys-headquarters-sunnyvale). ISO 3166-2 lists it as US-CA. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-synopsys-headquarters-sunnyvale · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: Synopsys's headquarters are located at 675 Almanor Avenue, Sunnyvale, California.
          as of: not_stated
          citation 1 · src-027 · standing party
            source: "Annual Report on Form 10-K for the fiscal year ended October 31, 2025" · Synopsys, Inc. · https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf
            class: company_filing · publisher record: company-synopsys
            stated dates: signed 2025-12-19
            registered: automated 2026-10-01T05:33Z sha256 f9ee4e270742e7d364fc911adff20682eda7f8c2a43ee6fee90ff16d8718a905
            filing copy: filer_hosted_not_checked
            locator: p.6, Item 1 'Business', 'Corporate Information', the first sentence
            anchor: "Our headquarters are located at 675 Almanor Avenue, Sunnyvale, California 94085"
            read by the Verifier: 2026-10-01T05:33Z sha256 f9ee4e270742 (same bytes as registered)
      input:
        claim-iso-3166-2-us-ca · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists California, of subdivision category 'state', with the code US-CA.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-CA
            anchor: "state US-CA California"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          (shown above)
  /roles/0/claim_ids: eda_vendor
    claim-synopsys-sells-eda · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Synopsys's Design Automation segment includes an EDA revenue group, and Synopsys's EDA products automate tasks in chip design.
      as of: not_stated
      citation 1 · src-027 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended October 31, 2025" · Synopsys, Inc. · https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf
        class: company_filing · publisher record: company-synopsys
        stated dates: signed 2025-12-19
        registered: automated 2026-10-01T05:33Z sha256 f9ee4e270742e7d364fc911adff20682eda7f8c2a43ee6fee90ff16d8718a905
        filing copy: filer_hosted_not_checked
        locator: p.7, 'Products and Services', 'Design Automation Segment', the first sentence
        anchor: "Our Design Automation segment includes the EDA, Ansys and Other revenue groups"
        read by the Verifier: 2026-10-01T05:33Z sha256 f9ee4e270742 (same bytes as registered)
      citation 2 · src-027 · standing party
        source: "Annual Report on Form 10-K for the fiscal year ended October 31, 2025" · Synopsys, Inc. · https://investor.synopsys.com/files/doc_financials/2025/q4/cb4c09c0-5b5a-4b6f-870f-0e69ec26a5ae.pdf
        class: company_filing · publisher record: company-synopsys
        stated dates: signed 2025-12-19
        registered: automated 2026-10-01T05:33Z sha256 f9ee4e270742e7d364fc911adff20682eda7f8c2a43ee6fee90ff16d8718a905
        filing copy: filer_hosted_not_checked
        locator: p.7, the sentence beginning 'Our EDA products increase designer productivity'
        anchor: "Our EDA products increase designer productivity and efficiency by automating tasks"
        read by the Verifier: 2026-10-01T05:33Z sha256 f9ee4e270742 (same bytes as registered)
(exit 0)

$ python tools/trace.py company-amazon-com
company-amazon-com · company record · canonical companies.json
  Amazon
  /identity_claim_ids:
    claim-amazon-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: The registrant of Amazon's Annual Report on Form 10-K for the fiscal year ended December 31, 2025 has the exact name “AMAZON.COM, INC.”, as specified in its charter.
      as of: not_stated
      citation 1 · src-028 · standing party
        source: "2025 Annual Report (including the Annual Report on Form 10-K for the fiscal year ended December 31, 2025)" · Amazon.com, Inc. · https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf
        class: company_filing · publisher record: company-amazon-com
        stated dates: signed 2026-02-05
        registered: automated 2026-10-01T05:33Z sha256 63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc
        filing copy: filer_hosted_not_checked
        locator: p.12 (the Form 10-K's cover page, which follows the shareholder letter), the name printed above the label '(Exact name of registrant as specified in its charter)'
        anchor: "AMAZON.COM, INC. (Exact name of registrant as specified in its charter)"
        read by the Verifier: 2026-10-01T05:33Z sha256 63196177ef83 (same bytes as registered)
  /legal_name/0/claim_ids: AMAZON.COM, INC.
    claim-amazon-registrant-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /incorporated_in/0/claim_ids: jurisdiction-us
    claim-amazon-incorporated-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Amazon.com, Inc.'s jurisdiction of incorporation is in the country with ISO 3166 code US (Delaware).
      reasoning: The filing names a subdivision, not the country (claim-amazon-incorporation-state). ISO 3166-2 lists it as US-DE. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-amazon-incorporation-state · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: Amazon.com, Inc. states Delaware as its state or other jurisdiction of incorporation or organization.
          as of: not_stated
          citation 1 · src-028 · standing party
            source: "2025 Annual Report (including the Annual Report on Form 10-K for the fiscal year ended December 31, 2025)" · Amazon.com, Inc. · https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf
            class: company_filing · publisher record: company-amazon-com
            stated dates: signed 2026-02-05
            registered: automated 2026-10-01T05:33Z sha256 63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc
            filing copy: filer_hosted_not_checked
            locator: p.12 (the Form 10-K's cover page), the field labelled '(State or other jurisdiction of incorporation or organization)', whose value is 'Delaware'; the number printed beside it is the I.R.S. Employer Identification No.
            anchor: "Delaware 91-1646860 (State or other jurisdiction of incorporation or organization)"
            read by the Verifier: 2026-10-01T05:33Z sha256 63196177ef83 (same bytes as registered)
      input:
        claim-iso-3166-2-us-de · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Delaware, of subdivision category 'state', with the code US-DE.
          as of: not_stated
          citation 1 · src-033 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, Alabama to New York (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 d247a0bf3d4e92ee22b5b16366f2da11526190619595d104461333652c045a9d
            locator: screenshot of the subdivision table, the row for US-DE
            anchor: "state US-DE Delaware"
            read by the Verifier: 2026-10-01T14:26Z sha256 d247a0bf3d4e (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-032 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 d02a4287f81268386a9f61a3b8d64b96460ca1cdb4b8f4d5e0a61ac4362ecda0
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code US Short name UNITED STATES OF AMERICA"
            read by the Verifier: 2026-10-01T14:30Z sha256 d02a4287f812 (same bytes as registered)
  /headquartered_in/0/claim_ids: jurisdiction-us
    claim-amazon-headquartered-in-us · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Amazon's corporate headquarters is in the country with ISO 3166 code US (Washington's Puget Sound region and Arlington, Virginia).
      reasoning: The filing names a subdivision, not the country (claim-amazon-headquarters-washington-virginia). ISO 3166-2 lists it as US-WA and US-VA. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is US (claim-iso-3166-1-us). So the country is the one coded US. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-amazon-headquarters-washington-virginia · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: Amazon owns and leases its corporate headquarters in Washington's Puget Sound region and in Arlington, Virginia.
          as of: not_stated
          citation 1 · src-028 · standing party
            source: "2025 Annual Report (including the Annual Report on Form 10-K for the fiscal year ended December 31, 2025)" · Amazon.com, Inc. · https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf
            class: company_filing · publisher record: company-amazon-com
            stated dates: signed 2026-02-05
            registered: automated 2026-10-01T05:33Z sha256 63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc
            filing copy: filer_hosted_not_checked
            locator: p.29, Form 10-K Item 2 'Properties', the sentence after the facilities tables
            anchor: "We own and lease our corporate headquarters in Washington’s Puget Sound region and Arlington, Virginia"
            read by the Verifier: 2026-10-01T05:33Z sha256 63196177ef83 (same bytes as registered)
      input:
        claim-iso-3166-2-us-wa · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Washington, of subdivision category 'state', with the code US-WA.
          as of: not_stated
          citation 1 · src-034 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, North Carolina to Wyoming (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 6825089a17a0758f864082577ffe219557c0991199c759f3b02bb1e96731f5b7
            locator: screenshot of the subdivision table, the row for US-WA
            anchor: "state US-WA Washington"
            read by the Verifier: 2026-10-01T14:26Z sha256 6825089a17a0 (same bytes as registered)
      input:
        claim-iso-3166-2-us-va · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Virginia, of subdivision category 'state', with the code US-VA.
          as of: not_stated
          citation 1 · src-034 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, subdivision table, North Carolina to Wyoming (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 6825089a17a0758f864082577ffe219557c0991199c759f3b02bb1e96731f5b7
            locator: screenshot of the subdivision table, the row for US-VA
            anchor: "state US-VA Virginia"
            read by the Verifier: 2026-10-01T14:26Z sha256 6825089a17a0 (same bytes as registered)
      input:
        claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          (shown above)
  /roles/0/claim_ids: cloud_provider
    claim-amazon-provides-cloud-services · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: Amazon provides cloud services to businesses, and through AWS offers on-demand technology services, including compute, storage and database services.
      as of: not_stated
      citation 1 · src-028 · standing party
        source: "2025 Annual Report (including the Annual Report on Form 10-K for the fiscal year ended December 31, 2025)" · Amazon.com, Inc. · https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf
        class: company_filing · publisher record: company-amazon-com
        stated dates: signed 2026-02-05
        registered: automated 2026-10-01T05:33Z sha256 63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc
        filing copy: filer_hosted_not_checked
        locator: p.23, Form 10-K Item 1A, under 'Our Commercial Agreements, Strategic Alliances, and Other Business Relationships Expose Us to Risks', the first sentence
        anchor: "We provide physical, e-commerce, and omnichannel retail, cloud services, and other services to businesses"
        read by the Verifier: 2026-10-01T05:33Z sha256 63196177ef83 (same bytes as registered)
      citation 2 · src-028 · standing party
        source: "2025 Annual Report (including the Annual Report on Form 10-K for the fiscal year ended December 31, 2025)" · Amazon.com, Inc. · https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf
        class: company_filing · publisher record: company-amazon-com
        stated dates: signed 2026-02-05
        registered: automated 2026-10-01T05:33Z sha256 63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc
        filing copy: filer_hosted_not_checked
        locator: p.14, Form 10-K Item 1 'Business', 'Developers and Enterprises'
        anchor: "through AWS, which offers a broad set of on-demand technology services, including compute, storage, database"
        read by the Verifier: 2026-10-01T05:33Z sha256 63196177ef83 (same bytes as registered)
  /roles/0/claim_ids: cloud_provider
    claim-amazon-operates-data-centers · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: As of December 31, 2025, Amazon operated leased and owned facilities in the category 'Fulfillment, data centers, and other', in North America and internationally.
      as of: 2025-12-31
      citation 1 · src-028 · standing party
        source: "2025 Annual Report (including the Annual Report on Form 10-K for the fiscal year ended December 31, 2025)" · Amazon.com, Inc. · https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf
        class: company_filing · publisher record: company-amazon-com
        stated dates: signed 2026-02-05
        registered: automated 2026-10-01T05:33Z sha256 63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc
        filing copy: filer_hosted_not_checked
        locator: p.29, Form 10-K Item 2 'Properties', the first sentence
        anchor: "As of December 31, 2025, we operated the following facilities"
        read by the Verifier: 2026-10-01T05:33Z sha256 63196177ef83 (same bytes as registered)
      citation 2 · src-028 · standing party
        source: "2025 Annual Report (including the Annual Report on Form 10-K for the fiscal year ended December 31, 2025)" · Amazon.com, Inc. · https://ir.aboutamazon.com/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf
        class: company_filing · publisher record: company-amazon-com
        stated dates: signed 2026-02-05
        registered: automated 2026-10-01T05:33Z sha256 63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc
        filing copy: filer_hosted_not_checked
        locator: p.29, Form 10-K Item 2 'Properties', first table, column 'Description of Use', the rows for North America and International
        anchor: "Fulfillment, data centers, and other"
        read by the Verifier: 2026-10-01T05:33Z sha256 63196177ef83 (same bytes as registered)
(exit 0)

$ python tools/trace.py company-asml-holding
company-asml-holding · company record · canonical companies.json
  ASML
  /identity_claim_ids:
    claim-asml-holding-nv-company · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ASML Holding N.V. is a public limited liability company organized under Dutch law.
      as of: not_stated
      citation 1 · src-029 · standing party
        source: "2025 Annual Report based on US GAAP (Annual Report on Form 20-F for the year ended December 31, 2025)" · ASML Holding N.V. · https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf
        class: company_filing · publisher record: company-asml-holding
        stated dates: signed 2026-02-25
        registered: automated 2026-10-01T05:33Z sha256 add58be9d9822ca12584b63c55c089b36e1ae5bf7a1825ebf1d1572628f2c52c
        filing copy: filer_hosted_not_checked
        locator: p.76, 'Corporate governance', the sentence beginning 'ASML Holding N.V. is a public limited liability company'
        anchor: "ASML Holding N.V. is a public limited liability company organized under Dutch law"
        read by the Verifier: 2026-10-01T05:33Z sha256 add58be9d982 (same bytes as registered)
  /legal_name/0/claim_ids: ASML Holding N.V.
    claim-asml-holding-nv-company · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /incorporated_in/0/claim_ids: jurisdiction-nl
    claim-asml-incorporated-netherlands · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ASML is incorporated in the Netherlands.
      as of: not_stated
      citation 1 · src-029 · standing party
        source: "2025 Annual Report based on US GAAP (Annual Report on Form 20-F for the year ended December 31, 2025)" · ASML Holding N.V. · https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf
        class: company_filing · publisher record: company-asml-holding
        stated dates: signed 2026-02-25
        registered: automated 2026-10-01T05:33Z sha256 add58be9d9822ca12584b63c55c089b36e1ae5bf7a1825ebf1d1572628f2c52c
        filing copy: filer_hosted_not_checked
        locator: p.309, Note on income taxes, 'Global Minimum Tax', the first sentence
        anchor: "Global minimum tax legislation was enacted in the Netherlands, the jurisdiction in which ASML is incorporated"
        read by the Verifier: 2026-10-01T05:33Z sha256 add58be9d982 (same bytes as registered)
  /headquartered_in/0/claim_ids: jurisdiction-nl
    claim-asml-headquarters-veldhoven · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ASML's headquarters are located in Veldhoven, the Netherlands.
      as of: not_stated
      citation 1 · src-029 · standing party
        source: "2025 Annual Report based on US GAAP (Annual Report on Form 20-F for the year ended December 31, 2025)" · ASML Holding N.V. · https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf
        class: company_filing · publisher record: company-asml-holding
        stated dates: signed 2026-02-25
        registered: automated 2026-10-01T05:33Z sha256 add58be9d9822ca12584b63c55c089b36e1ae5bf7a1825ebf1d1572628f2c52c
        filing copy: filer_hosted_not_checked
        locator: p.327, 'Facilities in EMEA', the first sentence
        anchor: "Our headquarters, mainly manufacturing and R&D facilities, are located in Veldhoven, the Netherlands"
        read by the Verifier: 2026-10-01T05:33Z sha256 add58be9d982 (same bytes as registered)
  /roles/0/claim_ids: equipment_maker
    claim-asml-semiconductor-equipment · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ASML develops, produces, markets, sells, upgrades and services advanced semiconductor equipment systems, consisting of lithography, metrology and inspection systems.
      as of: not_stated
      citation 1 · src-029 · standing party
        source: "2025 Annual Report based on US GAAP (Annual Report on Form 20-F for the year ended December 31, 2025)" · ASML Holding N.V. · https://ourbrand.asml.com/m/71076aaad607de4d/original/asml-2025-annual-report-based-on-us-gaap.pdf
        class: company_filing · publisher record: company-asml-holding
        stated dates: signed 2026-02-25
        registered: automated 2026-10-01T05:33Z sha256 add58be9d9822ca12584b63c55c089b36e1ae5bf7a1825ebf1d1572628f2c52c
        filing copy: filer_hosted_not_checked
        locator: p.287, Note 3 'Segment disclosure', the first sentence
        anchor: "for the development, production, marketing, sales, upgrading and servicing of advanced semiconductor equipment systems, consisting of lithography, metrology and inspection systems"
        read by the Verifier: 2026-10-01T05:33Z sha256 add58be9d982 (same bytes as registered)
(exit 0)

$ python tools/trace.py company-sk-hynix
company-sk-hynix · company record · canonical companies.json
  SK hynix
  /identity_claim_ids:
    claim-sk-hynix-legal-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: The company's name is 에스케이하이닉스 주식회사, written in English as SK hynix Inc. (the Atlas's translation of the Korean sentence).
      as of: not_stated
      citation 1 · src-030 · standing party
        source: "Annual Report for fiscal year 2025 (제78기), section I.1 'Company overview' (English DART)" · SK hynix Inc. · https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=4&offset=20380&length=52430&dtd=dart4.xsd
        class: company_filing · publisher record: company-sk-hynix
        stated dates: published 2026-03-17
        registered: automated 2026-10-01T05:37Z sha256 b067389a5f3c7d88fb7c3d91b7fef948e924a2d49791736ce8a92327fd4b6f2c
        filing copy: regulator_hosted
        locator: I.1 'Company overview', item 나 (the company's legal and commercial names), the first sentence
        anchor: "당사의 명칭은 에스케이하이닉스 주식회사이며, 영문으로는 SK hynix Inc.라고 표기합니다"
        read by the Verifier: 2026-10-01T05:37Z sha256 b067389a5f3c (same bytes as registered)
  /legal_name/0/claim_ids: 에스케이하이닉스 주식회사
    claim-sk-hynix-legal-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /legal_name/1/claim_ids: SK hynix Inc.
    claim-sk-hynix-legal-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /headquartered_in/0/claim_ids: jurisdiction-kr
    claim-sk-hynix-headquartered-in-kr · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: SK hynix's head office is in the country with ISO 3166 code KR (경기도, which ISO lists as Gyeonggi-do; the romanisation is part of this step).
      reasoning: The filing names a subdivision, not the country (claim-sk-hynix-head-office-gyeonggi). ISO 3166-2 lists it as KR-41. An ISO 3166-2 code begins with the alpha-2 code of the country it subdivides, and the table is the subdivision table of the ISO 3166 entry whose alpha-2 code is KR (claim-iso-3166-1-kr). So the country is the one coded KR. The step is the Atlas's, not the filing's (D-057).
      input:
        claim-sk-hynix-head-office-gyeonggi · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: SK hynix's head office address is 2091 Gyeongchung-daero, Icheon-si, Gyeonggi-do (the Atlas's translation of the Korean address).
          as of: not_stated
          citation 1 · src-030 · standing party
            source: "Annual Report for fiscal year 2025 (제78기), section I.1 'Company overview' (English DART)" · SK hynix Inc. · https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=4&offset=20380&length=52430&dtd=dart4.xsd
            class: company_filing · publisher record: company-sk-hynix
            stated dates: published 2026-03-17
            registered: automated 2026-10-01T05:37Z sha256 b067389a5f3c7d88fb7c3d91b7fef948e924a2d49791736ce8a92327fd4b6f2c
            filing copy: regulator_hosted
            locator: I.1 'Company overview', item 라 (head office address, telephone number and website), its heading and the address line
            anchor: "본사의 주소, 전화번호, 홈페이지 주소 주소: 경기도 이천시 경충대로 2091"
            read by the Verifier: 2026-10-01T05:37Z sha256 b067389a5f3c (same bytes as registered)
      input:
        claim-iso-3166-2-kr-41 · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166-2 lists Gyeonggi-do, of subdivision category 'province', with the code KR-41.
          as of: not_stated
          citation 1 · src-037 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for KR, subdivision table (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:KR
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:26Z sha256 e81ab0ff68a4abb36414a2be4381d9e23836651e58a893abe37afd2aeca97fa8
            locator: screenshot of the subdivision table, the row for KR-41
            anchor: "province KR-41 Gyeonggi-do Gyeonggi"
            read by the Verifier: 2026-10-01T14:26Z sha256 e81ab0ff68a4 (same bytes as registered)
      input:
        claim-iso-3166-1-kr · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code KR to the entry with the short name “KOREA, REPUBLIC OF” (full name “the Republic of Korea”), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-036 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for KR, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:KR
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 639a2393887f70a7b4f73aa146d0fd909420441eccf87933ad8433cc7567cb21
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code KR Short name KOREA, REPUBLIC OF"
            read by the Verifier: 2026-10-01T14:30Z sha256 639a2393887f (same bytes as registered)
  /roles/0/claim_ids: memory_manufacturer
    claim-sk-hynix-memory-products · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: SK hynix's main manufactured products are memory semiconductor products such as DRAM, NAND Flash and MCP (Multi-chip Package) (the Atlas's translation of the Korean sentence).
      as of: not_stated
      citation 1 · src-030 · standing party
        source: "Annual Report for fiscal year 2025 (제78기), section I.1 'Company overview' (English DART)" · SK hynix Inc. · https://englishdart.fss.or.kr/report/eng/viewer.do?rcpNo=20260317000635&dcmNo=11132576&eleId=4&offset=20380&length=52430&dtd=dart4.xsd
        class: company_filing · publisher record: company-sk-hynix
        stated dates: published 2026-03-17
        registered: automated 2026-10-01T05:37Z sha256 b067389a5f3c7d88fb7c3d91b7fef948e924a2d49791736ce8a92327fd4b6f2c
        filing copy: regulator_hosted
        locator: I.1 'Company overview', item 바 (main business), the first sentence
        anchor: "현재 당사의 주력 생산제품은 DRAM, NAND Flash 및 MCP(Multi-chip Package)와 같은 메모리 반도체 제품입니다"
        read by the Verifier: 2026-10-01T05:37Z sha256 b067389a5f3c (same bytes as registered)
  /incorporated_in: not_researched
(exit 0)

$ python tools/trace.py company-taiwan-semiconductor-manufacturing-company
company-taiwan-semiconductor-manufacturing-company · company record · canonical companies.json
  TSMC
  /identity_claim_ids:
    claim-tsmc-legal-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: TSMC's Articles of Incorporation give its name as 台灣積體電路製造股份有限公司 in the Chinese language and Taiwan Semiconductor Manufacturing Company Limited in the English language. The 20-F cover gives the Chinese name as the exact name in its charter, and the English name as its translation.
      as of: not_stated
      citation 1 · src-031 · standing party
        source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
        class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
        stated dates: signed 2026-04-16
        registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
        filing copy: filer_hosted_not_checked
        locator: p.179, Exhibit 1.1, Articles of Incorporation, Article 1
        anchor: "its name shall be 台灣積體電路製造股份有限公司 in the Chinese language, and Taiwan Semiconductor Manufacturing Company Limited in the English language"
        read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
      citation 2 · src-031 · standing party
        source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
        class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
        stated dates: signed 2026-04-16
        registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
        filing copy: filer_hosted_not_checked
        locator: p.20, Item 4, 'Our History and Structure', the first sentence
        anchor: "Our legal and commercial name is 台灣積體電路製造股份有限公司 (Taiwan Semiconductor Manufacturing Company Limited)"
        read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
      citation 3 · src-031 · standing party
        source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
        class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
        stated dates: signed 2026-04-16
        registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
        filing copy: filer_hosted_not_checked
        locator: p.1, cover page, the name printed above the label '(Exact Name of Registrant as Specified in Its Charter)'
        anchor: "台灣積體電路製造股份有限公司 (Exact Name of Registrant as Specified in Its Charter)"
        read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
      citation 4 · src-031 · standing party
        source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
        class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
        stated dates: signed 2026-04-16
        registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
        filing copy: filer_hosted_not_checked
        locator: p.1, cover page, the English name and its label; the text runs on into the jurisdiction field beside it
        anchor: "Taiwan Semiconductor Manufacturing Company Limited Republic of China (Translation of Registrant’s Name Into English)"
        read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
  /legal_name/0/claim_ids: 台灣積體電路製造股份有限公司
    claim-tsmc-legal-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /legal_name/1/claim_ids: Taiwan Semiconductor Manufacturing Company Limited
    claim-tsmc-legal-name · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /incorporated_in/0/claim_ids: jurisdiction-tw
    claim-tsmc-incorporated-in-tw · DERIVATION · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: TSMC's jurisdiction of incorporation is recorded as the ISO 3166 entry with code TW.
      reasoning: The filing names the jurisdiction of incorporation as the R.O.C. (claim-tsmc-incorporated-roc). The same filing writes the head office's place as 'Taiwan, Republic of China', using both names for one place (claim-tsmc-head-office-taiwan). ISO 3166 assigns the code TW to the entry whose short name is 'TAIWAN, PROVINCE OF CHINA' (claim-iso-3166-1-tw). So the Atlas records the entry TW. The code is an identifier and states no position on sovereignty (entity-taxonomy.md §3.6); the filing's own name for the jurisdiction stays in its claim. The step is the Atlas's (D-057).
      input:
        claim-tsmc-incorporated-roc · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: TSMC was incorporated in the R.O.C. (Republic of China) as a company limited by shares on February 21, 1987, under the Company Law of the Republic of China.
          as of: not_stated
          citation 1 · src-031 · standing party
            source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
            class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
            stated dates: signed 2026-04-16
            registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
            filing copy: filer_hosted_not_checked
            locator: p.179, Exhibit 1.1, Articles of Incorporation, Article 1
            anchor: "The Corporation shall be incorporated, as a company limited by shares, under the Company Law of the Republic of China"
            read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
          citation 2 · src-031 · standing party
            source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
            class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
            stated dates: signed 2026-04-16
            registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
            filing copy: filer_hosted_not_checked
            locator: p.20, Item 4, 'Our History and Structure', the second sentence
            anchor: "were incorporated in the R.O.C. as a company limited by shares on February 21, 1987"
            read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
          citation 3 · src-031 · standing party
            source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
            class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
            stated dates: signed 2026-04-16
            registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
            filing copy: filer_hosted_not_checked
            locator: p.108, Note 1 'General', the first sentence
            anchor: "Taiwan Semiconductor Manufacturing Company Limited (TSMC), a Republic of China (R.O.C.) corporation, was incorporated on February 21, 1987"
            read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
      input:
        claim-tsmc-head-office-taiwan · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: TSMC's Articles of Incorporation place its head office in Hsinchu Science Park, Taiwan, Republic of China, and its corporate headquarters are located in the Hsinchu Science Park.
          as of: not_stated
          citation 1 · src-031 · standing party
            source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
            class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
            stated dates: signed 2026-04-16
            registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
            filing copy: filer_hosted_not_checked
            locator: p.180, Exhibit 1.1, Articles of Incorporation, Article 3
            anchor: "The Corporation shall have its head office in Hsinchu Science Park, Taiwan, Republic of China"
            read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
          citation 2 · src-031 · standing party
            source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
            class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
            stated dates: signed 2026-04-16
            registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
            filing copy: filer_hosted_not_checked
            locator: p.21, Item 4, 'Our Semiconductor Facilities', the second sentence
            anchor: "Our corporate headquarters and nine of our fabs are located in the Hsinchu Science Park"
            read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
      input:
        claim-iso-3166-1-tw · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
          statement: ISO 3166 assigns the alpha-2 code TW to the entry with the short name “TAIWAN, PROVINCE OF CHINA” (its Full name row is empty), with status 'Officially assigned'.
          as of: not_stated
          citation 1 · src-038 · standing originator
            source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for TW, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:TW
            class: standard_specification · publisher record: not_applicable
            stated dates: undated
            registered: manual_by_human 2026-10-01T14:30Z sha256 506e72caa98ef136479a2530204364f63a761b9ac1ff658c2ec47b9b0f7291b8
            locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
            anchor: "Alpha-2 code TW Short name TAIWAN, PROVINCE OF CHINA"
            read by the Verifier: 2026-10-01T14:30Z sha256 506e72caa98e (same bytes as registered)
  /headquartered_in/0/claim_ids: jurisdiction-tw
    claim-tsmc-head-office-taiwan · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      (shown above)
  /roles/0/claim_ids: foundry_operator
    claim-tsmc-foundry · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: As a foundry, TSMC manufactures semiconductors with its own manufacturing processes for its customers, based on proprietary integrated circuit designs that the customers provide.
      as of: not_stated
      citation 1 · src-031 · standing party
        source: "Annual Report on Form 20-F for the fiscal year ended December 31, 2025" · Taiwan Semiconductor Manufacturing Company Limited · https://investor.tsmc.com/sites/ir/sec-filings/2025_20F%20Report.pdf
        class: company_filing · publisher record: company-taiwan-semiconductor-manufacturing-company
        stated dates: signed 2026-04-16
        registered: manual_by_human 2026-10-01T14:44Z sha256 923117acae9536fa30629f87573e6f976fb6e678ad46070c1e68520eb375de29
        filing copy: filer_hosted_not_checked
        locator: p.21, Item 4, 'Business Overview of the Company', the first sentence
        anchor: "As a foundry, we manufacture semiconductors using our manufacturing processes for our customers based on proprietary integrated circuit designs provided by them"
        read by the Verifier: 2026-10-01T14:44Z sha256 923117acae95 (same bytes as registered)
(exit 0)

$ python tools/trace.py jurisdiction-us
jurisdiction-us · jurisdiction record · canonical jurisdictions.json
  United States
  /identity_claim_ids:
    claim-iso-3166-1-us · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ISO 3166 assigns the alpha-2 code US to the entry with the short name “UNITED STATES OF AMERICA” (full name “the United States of America”), with status 'Officially assigned'.
      as of: not_stated
      citation 1 · src-032 · standing originator
        source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for US, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:US
        class: standard_specification · publisher record: not_applicable
        stated dates: undated
        registered: manual_by_human 2026-10-01T14:30Z sha256 d02a4287f81268386a9f61a3b8d64b96460ca1cdb4b8f4d5e0a61ac4362ecda0
        locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
        anchor: "Alpha-2 code US Short name UNITED STATES OF AMERICA"
        read by the Verifier: 2026-10-01T14:30Z sha256 d02a4287f812 (same bytes as registered)
(exit 0)

$ python tools/trace.py jurisdiction-nl
jurisdiction-nl · jurisdiction record · canonical jurisdictions.json
  Netherlands
  /identity_claim_ids:
    claim-iso-3166-1-nl · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ISO 3166 assigns the alpha-2 code NL to the entry with the short name “NETHERLANDS, KINGDOM OF THE” (full name “the Kingdom of the Netherlands”), with status 'Officially assigned'.
      as of: not_stated
      citation 1 · src-035 · standing originator
        source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for NL, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:NL
        class: standard_specification · publisher record: not_applicable
        stated dates: undated
        registered: manual_by_human 2026-10-01T14:30Z sha256 354e5466a3de5c738b2b7b1e4ff37543e12c828cfaa044770e6d2525f2870292
        locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
        anchor: "Alpha-2 code NL Short name NETHERLANDS, KINGDOM OF THE"
        read by the Verifier: 2026-10-01T14:30Z sha256 354e5466a3de (same bytes as registered)
(exit 0)

$ python tools/trace.py jurisdiction-kr
jurisdiction-kr · jurisdiction record · canonical jurisdictions.json
  Republic of Korea
  /identity_claim_ids:
    claim-iso-3166-1-kr · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ISO 3166 assigns the alpha-2 code KR to the entry with the short name “KOREA, REPUBLIC OF” (full name “the Republic of Korea”), with status 'Officially assigned'.
      as of: not_stated
      citation 1 · src-036 · standing originator
        source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for KR, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:KR
        class: standard_specification · publisher record: not_applicable
        stated dates: undated
        registered: manual_by_human 2026-10-01T14:30Z sha256 639a2393887f70a7b4f73aa146d0fd909420441eccf87933ad8433cc7567cb21
        locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
        anchor: "Alpha-2 code KR Short name KOREA, REPUBLIC OF"
        read by the Verifier: 2026-10-01T14:30Z sha256 639a2393887f (same bytes as registered)
(exit 0)

$ python tools/trace.py jurisdiction-tw
jurisdiction-tw · jurisdiction record · canonical jurisdictions.json
  Taiwan
  /identity_claim_ids:
    claim-iso-3166-1-tw · FACT · supported · verified 2026-10-01 · canonical, accepted by the human on 2026-10-01 (sessions/reports/SESSION-07-REPORT.md)
      statement: ISO 3166 assigns the alpha-2 code TW to the entry with the short name “TAIWAN, PROVINCE OF CHINA” (its Full name row is empty), with status 'Officially assigned'.
      as of: not_stated
      citation 1 · src-038 · standing originator
        source: "ISO 3166 — Codes for the representation of names of countries and their subdivisions: Online Browsing Platform entry for TW, identity block (screenshot)" · International Organization for Standardization (ISO) · https://www.iso.org/obp/ui/#iso:code:3166:TW
        class: standard_specification · publisher record: not_applicable
        stated dates: undated
        registered: manual_by_human 2026-10-01T14:30Z sha256 506e72caa98ef136479a2530204364f63a761b9ac1ff658c2ec47b9b0f7291b8
        locator: screenshot of the OBP entry, below 'Standard: ISO 3166', rows 'Alpha-2 code' and 'Short name'
        anchor: "Alpha-2 code TW Short name TAIWAN, PROVINCE OF CHINA"
        read by the Verifier: 2026-10-01T14:30Z sha256 506e72caa98e (same bytes as registered)
(exit 0)
```

</details>
