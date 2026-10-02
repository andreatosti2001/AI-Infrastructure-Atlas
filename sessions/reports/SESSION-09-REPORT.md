# SESSION-09 Report — Facility dataset

> **Checkpoint (work in progress, 2026-10-02).** The design, the proposed event schema, the
> checks, the sources and the staging records are in place; nothing S09 created is
> canonical yet. Waiting on: (1) the human's re-supply of TSMC's 20-F (RA-4), and (2) the
> human's review of batch A below. The full report replaces this checkpoint at the end of
> the session.

- **Session:** S09 · **Type:** RESEARCH / IMPLEMENTATION · **Milestone:** M2 — Canonical Dataset (third session)
- **Prompt:** [`sessions/prompts/S09-PROMPT.md`](../prompts/S09-PROMPT.md)
- **Branch:** `claude/new-session-mdyi2x`, created from `main` @ `c20faf4`

## Mission outcome

Pending: written at the end of S09.

## Files changed

Pending: written at the end of S09.

## Data changed

Pending: written at the end of S09.

## Tests run

At start (fresh venv from the pins, installed set = pins): 190 tests OK; Gate 0 OK. At this checkpoint: 221 tests OK; Gate 0 OK. The rest is written at the end of S09.

## Evidence added/retired

Pending: written at the end of S09.

## Decisions made

Pending: written at the end of S09.

## Deviations

Pending: written at the end of S09.

## Debt introduced/resolved

Pending: written at the end of S09.

## Unresolved issues

Pending: written at the end of S09.

## Process lessons

Pending: written at the end of S09.

## Implications for the next session

Pending: written at the end of S09.

## Review sheet — batch A (Micron, SK hynix, Amkor events, ASML)

For each claim: open the source at the locator, read the whole sentence, and answer **does it
say this, and no more?** Verdict per claim: **accept**, **reject**, or **wording too
strong**. `python tools/trace.py <record or claim ID>` prints any record with its claims,
sources, locators and anchors; `python tools/trace.py src-046` prints a source.

#### Batch A

##### `facility-us-manassas-virginia` — Micron Manassas fab · wafer_fab · located_in `jurisdiction-us` · locality “Manassas, Virginia”

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-micron-manassas-fab` | FACT | Micron has a fab in Manassas, Virginia: its 10-K calls it “our fab in Manassas, Virginia”. | src-025 (company_filing) · p.48, Item 2 'Properties', the sentence beginning 'On June 11, 2025, we also entered into a direct funding agreement' | “to expand and modernize our fab in Manassas, Virginia” | The sentence is about a CHIPS funding agreement; only 'our fab in Manassas, Virginia' is used (identity, locality, kind word 'fab'). Ruling: 'fab' gives wafer_fab (asked separately). |
| `claim-micron-manassas-fab-in-us` | DERIVATION | Micron's fab in Manassas, Virginia is in the country with ISO 3166 code US (Virginia, which ISO 3166-2 lists as US-VA). | — | inputs: `claim-micron-manassas-fab`, `claim-iso-3166-2-us-va` (canonical), `claim-iso-3166-1-us` (canonical)<br>reasoning: The site sentence names a US state, not the country (claim-micron-manassas-fab). ISO 3166-2 lists Virginia as US-VA (claim-iso-3166-2-us-va), and an ISO 3166-2 code begins with the alpha-2 code of the country it subdivides (claim-iso-3166-1-us). So the site is in the country coded US. The step is the Atlas's (D-057, D-080); no headquarters or incorporation sentence is an input. | Does the US-VA step hold? No headquarters claim is an input. |

##### `facility-kr-m16` — SK hynix M16 · wafer_fab · located_in `jurisdiction-kr` · locality “이천”

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-sk-hynix-m16-completed-icheon` | FACT | SK hynix's annual report lists, among the changes in its production facilities, the completion (준공) of its new plant M16 in 이천 (Icheon) in February 2021 (the Atlas's translation). | src-046 (company_filing) · I.2 'Company history', item (3) 생산설비의 변동 (changes in production facilities), the row dated 2021. 02 | “(3) 생산설비의 변동 2021. 02 이천 신규 공장 M16 준공” | Korean, a table row under '(3) changes in production facilities'. Is the translation faithful? 준공 = completion of construction; recorded as an opened event (asked separately). |
| `claim-sk-hynix-m16-fabrication-plant` | FACT | SK hynix describes M16 as its new fabrication plant, for which it held a completion ceremony. | src-049 (company_press_release) · body, first paragraph, the sentence beginning 'SK hynix Inc. (or ‘the Company’' (its last words, a head-office phrase, are not used) | “held a completion ceremony for its new fabrication plant M16” | The sentence ends 'at headquarter located in Icheon, Gyeonggi-do, South Korea'; that phrase is not used (R-5). Used for the kind word 'fabrication plant' only. |
| `claim-sk-hynix-m16-in-kr` | DERIVATION | SK hynix's M16 plant is in the country with ISO 3166 code KR (in 이천, which SK hynix places in 경기도, which ISO 3166-2 lists as Gyeonggi-do, KR-41). | — | inputs: `claim-sk-hynix-m16-completed-icheon`, `claim-sk-hynix-production-plants-icheon-cheongju`, `claim-iso-3166-2-kr-41` (canonical), `claim-iso-3166-1-kr` (canonical)<br>reasoning: The filing places M16 in 이천 (claim-sk-hynix-m16-completed-icheon) and the company's production plants in 경기도 이천시 (claim-sk-hynix-production-plants-icheon-cheongju), so the 이천 of the M16 row is 경기도 이천시. ISO 3166-2 lists 경기도 as Gyeonggi-do, KR-41 (claim-iso-3166-2-kr-41); the romanisation is part of this step, as in D-057. An ISO 3166-2 code begins with the alpha-2 code of its country (claim-iso-3166-1-kr). No head-office sentence is an input (D-080). | Does the 이천 → 경기도 이천시 → KR-41 → KR step hold? No head-office claim is an input. |

##### Events

| Event | Type | Subject | Date | Claim |
|---|---|---|---|---|
| `event-kr-m16-opened-2021-02` | opened | `facility-kr-m16` | 2021-02 | `claim-sk-hynix-m16-completed-icheon` |
| `event-sk-hynix-announced-2022-09-06` | announced | `company-sk-hynix` | 2022-09-06 | `claim-sk-hynix-m15x-plan-disclosed` |
| `event-micron-technology-announced-2025-06` | announced | `company-micron-technology` | 2025-06 | `claim-micron-second-idaho-fab-announced` |
| `event-amkor-technology-announced-2026-09-08` | announced | `company-amkor-technology` | 2026-09-08 | `claim-amkor-arizona-phase-2-announced` |

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-sk-hynix-m15x-plan-disclosed` | ATTRIBUTION | SK hynix disclosed on 2022-09-06 its plan to build M15X, an extension fab of M15, from October 2022 on land it had already secured in the Cheongju Technopolis industrial complex (the Atlas's translation). | src-048 (company_filing) · XI.1 'Progress and changes of disclosure information', table 가, the row whose 신고일자 (filing date) is 2022.09.06; cells read in order, table-cell boundaries as whitespace | “2022.09.06 장래사업ㆍ경영 계획 (공정공시) 1. 제목: 생산기반 확충을 위한 투자계획 2. 내용: 2022년 10월부터 청주 테크노폴리스 산업단지 내 기존 확보된 부지에 M15의 확장 팹인 M15X(eXtension)를 건설할 계획입니다” | Korean, a table row (cells read in order). A plan (ER-8): an announced event dated by the disclosure, 2022-09-06. |
| `claim-micron-second-idaho-fab-announced` | ATTRIBUTION | Micron states that in June 2025 it announced plans for a second leading-edge memory manufacturing fab in Idaho. | src-025 (company_filing) · p.47, Item 2 'Properties', the sentence beginning 'In June 2025, in connection with certain amendments' | “In June 2025, in connection with certain amendments to our CHIPS Act agreements, we announced plans for a second leading-edge memory manufacturing fab in Idaho” | A plan (ER-8): an announced event only, never a facility or a state. |
| `claim-amkor-arizona-phase-2-announced` | ATTRIBUTION | Amkor announced on 2026-09-08 phase 2 of its Arizona advanced packaging and test campus. | src-050 (company_press_release) · first paragraph after the dateline 'TEMPE, Ariz.--(BUSINESS WIRE)--Sep. 8, 2026--' | “today announced phase 2 of its Arizona Advanced packaging and test campus” | A plan (ER-8). The release's 'leading provider' and 'first OSAT production site' (ER-5) are not used. |

##### Other staging claims

| Claim | Type | Statement | Source · locator | Anchor (verbatim) or inputs | What to look for |
|---|---|---|---|---|---|
| `claim-sk-hynix-production-plants-icheon-cheongju` | FACT | SK hynix Inc. states that it has installed and operates production plants in 경기도 이천시 (Icheon-si, Gyeonggi-do) and 충청북도 청주시 (Cheongju-si, Chungcheongbuk-do) (the Atlas's translation). | src-047 (company_filing) · notes to the separate financial statements, note 1 'Company overview', the first sentence, its last clause (the clause before it names the head office, and is not used) | “경기도 이천시와 충청북도 청주시에 생산공장을 설치ㆍ가동하고 있습니다” | Korean. The same sentence names the head office in its first clause; the anchor is only the production-plant clause. Is that a fair extract? Also the S10 operates candidate (partly meets §5). |
| `claim-asml-manufacturing-sites` | FACT | ASML states that all of its manufacturing activities, including subassembly, final assembly and system testing, take place in cleanroom facilities in Veldhoven, Eindhoven, Oirschot (the Netherlands), Berlin (Germany), Wilton, San Diego (US), Pyeongtaek (South Korea), and Linkou and Tainan (Taiwan). | src-029 (company_filing) · p.69, the paragraph on manufacturing, the sentence beginning 'All of our manufacturing activities' | “All of our manufacturing activities, including subassembly, final assembly and system testing, take place in (cleanroom) facilities in Veldhoven, Eindhoven, Oirschot (the Netherlands), Berlin (Germany), Wilton, San Diego (US), Pyeongtaek (South Korea) and Linkou and Tainan (Taiwan)” | Supports no record: ASML's sites have no facility kind (D-088, your 'Gap + proposal'). Kept as evidence for the later session. |
