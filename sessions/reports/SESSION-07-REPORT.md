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

> **Status of this report: in progress.** It is written while the session runs, so that the
> human's verdicts have a home (`claim-model.md` §7). Sections marked *open* are completed
> before the final commit.

## Mission outcome

*Open.* Seven of the eight seed companies are canonical: NVIDIA, Micron, Amkor, Synopsys,
Amazon, ASML and SK hynix. Their identity, legal name and role claims were accepted by the
human on review sheet 1. TSMC and the jurisdiction records wait for the human's RA-4 files
(D-058, D-060).

## Files changed

*Open.* See the final commit.

## Data changed

*Open.* As measured at this commit: 6 new source records (`src-025` to `src-030`); 27
claims accepted and moved to `data/claims.json`; 7 companies in `data/companies.json`;
`publisher_entity` set for `src-024` to `src-030` (D-065).

## Tests run

*Open.*

## Evidence added/retired

*Open.*

## Decisions made

*Open.* D-054 to D-066, all `proposed`.

## Deviations

*Open.*

## Debt introduced/resolved

*Open.*

## Unresolved issues

*Open.*

## Process lessons

*Open.*

## Implications for the next session

*Open.*

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
