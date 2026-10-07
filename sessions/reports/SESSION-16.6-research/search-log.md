# S16.6 search log: who supplies the HBM in the H100 and in Trainium2 (under D-144 to D-147)

Written by the **Source Scout, S16.6**, on **2026-10-07**. It follows [`plan.md`](plan.md), search order rows 1 to 5.
S16.5's log ([`../SESSION-16.5-research/search-log.md`](../SESSION-16.5-research/search-log.md)) stands; its party
searches (S-01 to S-51) were not repeated. This log adds the kinds of source that the new rules admit: teardowns
(D-145), recognised and independent third parties (D-147), and past-tense party statements (row 4).

What this log is: a record of every query, every candidate URL, what was retrieved, and short verbatim anchors.
What it is not: a decision. It does not say what is canonical or what evidence status any claim has; the
`recognised` / `independent` entries are the scout's **proposals** for the Verifier (`source-policy.md` §7.1). The
scout wrote nothing under `data/`.

**Method.** WebSearch only discovered URLs; no snippet is used as evidence or anchor. Each kept URL was retrieved
with plain `curl -sSL` (default client identity, no custom headers, through the session's preconfigured HTTPS
proxy). Raw bytes were hashed with `sha256sum` and kept outside the repository, in the scout's scratchpad
(`.../scratchpad/s166-sources/`, files `T-01` to `T-35`). Text was extracted locally with a Python
standard-library HTML parser run with `python3 -I`. No downloaded file was executed. Refusals, bot challenges,
connection resets and paywalls are recorded as access gaps and were not worked around (RA-2): no other client
identity, no headless browser, no mirror, archive or proxy. SEC EDGAR was not used (D-042); `sec.gov` results were
dropped.

**Dates.** "Stated date" is what the document prints for itself (or its page metadata, as labelled). Access times
are UTC. "Recent" means stated date on or after **2025-10-07** (§7.1 criterion 1, 12 months before today).

**Quotation marks.** Several sources use typographic apostrophes and dashes (’, —); anchors below reproduce the
words exactly but may show a straight apostrophe. "…" marks an omission by the scout.

**Locators.** For HTML pages, a locator names the heading or paragraph opening; "text line N" is the line in the
scout's extracted text file (`T-xx.txt`), given only as a convenience for re-finding the passage.

---

## 1. Search queries

All run on 2026-10-07 with WebSearch ("standard" mode unless marked "extended").

| # | Query text | Domain filter | Plan row | Question | Result in brief |
|---|---|---|---|---|---|
| Q1 | TechInsights H100 teardown HBM3 SK hynix | none | 1 | Q-H100 | TechInsights B200 blog; Yole SK hynix HBM3 report page |
| Q2 | Trainium2 teardown HBM die analysis | none | 1 | Q-TRN2 | no Trainium2 teardown found; HBM teardowns of other products |
| Q3 | Yole Group NVIDIA H100 teardown reverse costing HBM | none | 1 | Q-H100 | Yole "NVIDIA H100" report page |
| Q4 | TechInsights NVIDIA H100 GPU analysis HBM supplier | none | 1 | Q-H100 | TechInsights SK hynix HBM3 floorplan page |
| Q5 | H100 teardown HBM3 package marking SK hynix die | none | 1 | Q-H100 | same TechInsights / Yole pages; KED Global |
| Q6 | techinsights GH100 H100 SXM5 package analysis HBM3 | techinsights.com | 1 | Q-H100 | TechInsights H100 report product pages (APE, APQ, DFR), "Hopper Leaps Ahead" |
| Q7 | techinsights Trainium2 AWS | techinsights.com | 1 | Q-TRN2 | Microprocessor Report Feb 2025 review only |
| Q8 | Trainium2 chip package HBM3 stacks SK hynix Samsung photo re:Invent | none | 1 | Q-TRN2 | DIGITIMES 2023-12-07 again; no teardown |
| Q9 | H100 PCIe HBM2e Samsung OR "SK hynix" teardown | none | 1 | Q-H100 | no H100 PCIe teardown found |
| Q10 | Reuters SK Hynix HBM3 Nvidia H100 supplier | reuters.com | 2 | Q-H100 | **search tool refused the filter**: "domains are not accessible to our user agent: ['reuters.com']" |
| Q11 | Reuters Trainium2 high bandwidth memory supplier Samsung SK Hynix Amazon | reuters.com | 2 | Q-TRN2 | same refusal |
| Q12 | Reuters SK Hynix sole supplier HBM3 Nvidia H100 | none | 2 | Q-H100 | no reuters.com URL returned; TrendForce release copies |
| Q13 | Bloomberg Nvidia H100 HBM SK Hynix Samsung memory supplier | none | 2 | Q-H100 | Bloomberg 2023-09-01, 2024-03-22 |
| Q14 | TrendForce HBM3 initially exclusively supplied by SK hynix Samsung rallies AMD validation H100 | trendforce.com | 3, 5 | Q-H100 | TrendForce press release 2024-03-13 (correct URL), TrendForce news items |
| Q15 | TrendForce Trainium2 HBM3E supplier SK hynix Samsung AWS | trendforce.com | 3 | Q-TRN2 | TrendForce news items; none titled with Trainium2 |
| Q16 | Trainium2 HBM supplier SK hynix Samsung Micron 2025 (extended) | none | 2, 3 | Q-TRN2 | market-share pages and blogs; nothing product-level |
| Q17 | Trainium 2 HBM3 Samsung SK hynix supply report Korea | none | 2 | Q-TRN2 | TrendForce `?p=29218`; Korea Times (H20, not Trainium) |
| Q18 | "Trainium2" "SK hynix" HBM (extended) | none | 2, 3 | Q-TRN2 | SemiAnalysis "AWS Trainium3 Deep Dive"; DIGITIMES |
| Q19 | "Trainium2" Samsung HBM3 supply Amazon | none | 2 | Q-TRN2 | same as Q18 |
| Q20 | Financial Times SK Hynix HBM Nvidia H100 memory chips supplier | none | 2 | Q-H100 | no ft.com URL returned; Korea JoongAng Daily 2022 |
| Q21 | Nikkei Asia SK Hynix high-bandwidth memory Nvidia H100 | none | 2 | Q-H100 | no Nikkei URL; KED Global, Tom's Hardware-type pages |
| Q22 | Wall Street Journal SK Hynix memory Nvidia H100 chips supplier | none | 2 | Q-H100 | no wsj.com URL returned |
| Q23 | SK Hynix HBM3 Nvidia H100 | ft.com, asia.nikkei.com, wsj.com, bloomberg.com, apnews.com, nytimes.com, economist.com | 2 | Q-H100 | **search tool refused** apnews.com, economist.com, ft.com, nytimes.com, wsj.com |
| Q24 | Amazon Trainium high-bandwidth memory Samsung SK Hynix | same as Q23 | 2 | Q-TRN2 | same refusal |
| Q25 | SK Hynix HBM3 Nvidia H100 | asia.nikkei.com, bloomberg.com | 2 | Q-H100 | Nikkei 2024-03-20, 2026-06-02; Bloomberg 2024-07-30 and others |
| Q26 | Amazon Trainium memory chips Samsung SK Hynix | asia.nikkei.com, bloomberg.com | 2 | Q-TRN2 | Bloomberg 2025-12-02 (Trainium3); none naming Trainium2 with a maker in the title |
| Q27 | Yonhap SK hynix HBM3 Nvidia H100 supply | en.yna.co.kr | 2 | Q-H100 | no results |
| Q28 | Yonhap Amazon Trainium HBM Samsung SK hynix | en.yna.co.kr | 2 | Q-TRN2 | no results |
| Q29 | Counterpoint Research HBM H100 SK hynix supplier Nvidia | none | 3 | Q-H100 | Counterpoint "in the press" page (company-level); market shares only |
| Q30 | Omdia HBM supplier Nvidia H100 Trainium | none | 3 | both | no Omdia page; SemiAnalysis 2023-07-05 |
| Q31 | SK hynix newsroom HBM3 supplied NVIDIA H100 history | news.skhynix.com | 4 | Q-H100 | sec.gov results (dropped); S-20 again |
| Q32 | Samsung HBM3 supplied Trainium OR "H100" newsroom | semiconductor.samsung.com, news.samsung.com | 4 | both | one unrelated SSD white paper |
| Q33 | Micron HBM Trainium AWS supply | micron.com, investors.micron.com | 4 | Q-TRN2 | sec.gov results only (dropped) |
| Q34 | SK hynix AWS Trainium HBM3E supply newsroom 2025 2026 | news.skhynix.com, aboutamazon.com, aws.amazon.com, press.aboutamazon.com | 4 | Q-TRN2 | sec.gov results (dropped); S-28 again |
| Q35 | NVIDIA H100 HBM3 "SK hynix" supplied 2022 2023 past shipments | nvidianews.nvidia.com, blogs.nvidia.com, news.skhynix.com | 4 | Q-H100 | SK hynix "A Year to Remember", "Heritage", DTW 2023 pages; sec.gov results (dropped) |
| Q36 | Samsung HBM3E AWS Amazon Trainium supply | semiconductor.samsung.com, news.samsung.com, samsung.com | 4 | Q-TRN2 | sec.gov results only (dropped) |
| Q37 | Samsung HBM3E 8-high Amazon Trainium2 supply news (extended) | none | 2 | Q-TRN2 | TrendForce 2025-03-21, 2025-04-09; SemiAnalysis T-19 again |
| Q38 | Amazon Trainium2 HBM Samsung main supplier Trainium3 SK hynix Micron switch report (extended) | none | 2, 3 | Q-TRN2 | blogs and aggregators; SemiAnalysis T-19 again |
| Q39 | "H100" "SK Hynix" HBM3 2026 article sole supplier Nvidia H100 memory (extended) | none | 2 | Q-H100 | Tom's Hardware 2022; tweaktown; DIGITIMES 2025-08-20 |
| Q40 | techinsights SK hynix HBM3 die NVIDIA H100 extracted memory analysis | techinsights.com, library.techinsights.com | 1 | Q-H100 | TechInsights AME-2403-802 product page |
| — | (no search) a TrendForce press-release URL was **guessed** from the release date before Q14 | — | 5 | Q-H100 | 404 (T-14); recorded so the guess is visible, then replaced by the URL from Q14 |

**Discovery limitation.** The WebSearch tool refused domain filters for reuters.com, ft.com, wsj.com, apnews.com,
nytimes.com and economist.com (Q10, Q11, Q23, Q24), and unfiltered queries naming those outlets (Q12, Q20, Q22)
returned no URL on them. So Reuters, FT, WSJ and AP were **not searched** in any meaningful way; this is a tool
limitation, not a finding that they hold nothing.

---

## 2. Candidates

Standing (§4) is for the supplier claim of the question shown. "Party" = NVIDIA (Q-H100), Amazon/AWS (Q-TRN2), or
an HBM maker (SK hynix, Samsung, Micron). Hashes are of the raw bytes received, including refusal pages.

### 2.1 Requested (an HTTP response or a connection attempt)

| T-id | URL (final URL if different) | Publisher | Proposed class | Standing | Stated dates | Access (UTC) | sha256 | HTTP outcome | Kept / dropped, why |
|---|---|---|---|---|---|---|---|---|---|
| T-01 | https://www.yolegroup.com/product/report/nvidia-gpu-for-artificial-intelligence---nvidia-h100/ | Yole Group | would be `research_report` (teardown report page) | would be originator | not read | 2026-10-07T16:42Z | `d9e2f6fed107746602ba3545b2eebe6029f664e42af9a8b9132a3379f5a2af20` (refusal page) | 403, CloudFront "Request blocked." | **access gap** (Yole's H100 teardown report page; its full report is a paid product in any case) |
| T-02 | https://www.yolegroup.com/product/report/sk-hynix-hbm3/ | Yole Group | would be `research_report` | would be originator | not read | 2026-10-07T16:42Z | `857a65434d0124348c2dcf072f117d1cd6766a86c04fe0e037f79ab2a1c846fb` (refusal page) | 403, CloudFront | **access gap**. Search titles suggest it concerns the GH200, not the H100; unread, so not relied on |
| T-03 | https://www.techinsights.com/node/58287 (→ https://www.techinsights.com/blog/sk-hynix-h5vg7hmd83x020r-d1z-16-gb-hbm3-dram-memory-floorplan-analysis) | TechInsights | `research_report` (public summary of a teardown analysis) | originator | **undated** (no date for this item found in the page; the dates on the page belong to sidebar items) | 2026-10-07T16:42Z | `1d30dd4472e3045b0a2f75b600f404e2a3f35cdeae30e9990fbb61b7ea5e4586` | 200 | **kept, flagged: other product.** Teardown of a **Grace Hopper Superchip** (GH200) unit, not an H100 SXM5 / PCIe / NVL. Full report behind TechInsights platform registration/subscription |
| T-04 | https://www.techinsights.com/blog/techinsights-nvidia-hgx-b200-analysis-reveals-hbm3e-supplier-and-advanced-packaging-innovation | TechInsights | `research_report` (teardown news item) | originator | "April 14, 2025" | 2026-10-07T16:42Z | `f5c6e8db97407876e58622bbec3dfad8d231f5261cd5ad364e35de032354ffa0` | 200 | dropped: other product (B200 / GB100); mentions Hopper only as a size comparison |
| T-05 | https://www.techinsights.com/products/ape-2303-801 | TechInsights | `research_report` (catalogue page of "NVIDIA Hopper H100 GPU Advanced Packaging Analysis") | would be originator | "Release Date 28/07/2023" | 2026-10-07T16:43Z | `e158d72262b33e24d69c227a1b7dc9ca2c5acebb10f875415caca9f7e190da28` | 200 | **kept as evidence that an H100 teardown exists; access gap for its content.** The public page names no memory maker; the report is a paid product |
| T-06 | https://www.techinsights.com/products/apq-2303-801 | TechInsights | as T-05 ("…Quick Look Analysis") | would be originator | "Release Date 30/06/2023" | 2026-10-07T16:43Z | `c56245f12ce49a48e9066614b9aacd9de9a46b0b6dea180af3e793929bba55db` | 200 | same as T-05 |
| T-07 | https://www.techinsights.com/products/dfr-2303-801 | TechInsights | as T-05 ("…TSMC Custom NVIDIA 4N FinFET Process Digital Floorplan Analysis") | would be originator | "Release Date 10/07/2023" | 2026-10-07T16:43Z | `1fe5e9116c87b9a6e199e7bfb2e98ac96f860001fc041ec258028769492ade0e` | 200 | same as T-05; contents list "package photographs, package X-rays, die markings" but the page names no memory maker |
| T-08 | https://www.techinsights.com/blog/nvidia-hopper-leaps-ahead | TechInsights (Microprocessor Report) | `research_report` | — | undated in page | 2026-10-07T16:43Z | `edffdba646a2428cdc99d2bae4ab1f90854b7eb85209074db3bbd9e1d5f11319` | 200 | dropped: no memory maker named |
| T-09 | https://www.techinsights.com/blog/microprocessor-report-february-2025-review | TechInsights | `research_report` | — | February 2025 (title) | 2026-10-07T16:43Z | `207c1f2fa4f6871bddd440d841297b3939434740cb9fc31c8b32f52b7b77189f` | 200 | dropped: mentions Trainium2 GA, no memory maker |
| T-10 | https://www.bloomberg.com/news/articles/2023-09-01/samsung-surges-6-on-talk-it-s-joining-nvidia-s-ai-suppliers | Bloomberg | would be `news_media` | would be reporter | not read | 2026-10-07T16:44Z | `b164e39bf4523728f3b50c396dc3c0bb9a3389c87af6d90ed18240136a6fb921` (challenge page) | 403, title "Bloomberg - Are you a robot?" | **access gap** (bot challenge) |
| T-11 | https://www.businesswire.com/news/home/20240313864555/en/HBM3-Initially-Exclusively-Supplied-by-SK-Hynix-Samsung-Rallies-Fast-After-AMD-Validation-Says-TrendForce | Business Wire (distribution of TrendForce's release) | — | — | not read | 2026-10-07T16:44Z | `f1dfc7b1ea148aa11459391aca993536b34478c4d513d88efe04b8e77fc178d8` (refusal page) | 403 "Access Denied" | dropped: a distributor's copy; the publisher's own copy was retrieved (T-15) |
| T-12 | https://www.kedglobal.com/korean-chipmakers/newsView/ked202206090017 | The Korea Economic Daily (KED Global) | would be `news_media` | would be reporter | not read | 2026-10-07T16:44Z (two attempts) | none (no bytes) | `curl: (35) Recv failure: Connection reset by peer`; second attempt: no bytes. Proxy status `recentRelayFailures`: "ws_closed_mid_exchange … host www.kedglobal.com:443" | **access gap** (plan row 5 pointer). A header-only probe at 16:47Z gave the same reset |
| T-13 | https://www.bloomberg.com/news/articles/2024-03-22/samsung-still-lacking-in-ai-investors-eyes-after-nvidia-boost | Bloomberg | would be `news_media` | would be reporter | not read | 2026-10-07T16:44Z | `7a8979c3f65a428c04ec4a153676ff62b3636794f3217b15530bf74dc9a37a41` (challenge page) | 403, bot challenge | **access gap** |
| T-14 | https://www.trendforce.com/presscenter/news/20240313-12069.html | TrendForce | — | — | — | 2026-10-07T16:44Z | `9c5d8b20f8d9940093e69baf4307eb503237a75f0e9fb25e189df6c2617918ae` | 404 | dropped: **a URL the scout guessed**; wrong. Replaced by T-15, found by Q14 |
| T-15 | https://www.trendforce.com/presscenter/news/20240313-12075.html | TrendForce (press release; byline "Avril Wu") | `market_research_consultancy` | originator of its own assessment (it names no source for the H100 sentence) | "13 March 2024" | 2026-10-07T16:44Z | `bc09c9b87630057287f07954a07427f1888518dbd64f5fda30ca9af72b97abd7` | 200 | **kept** (plan row 5 pointer, now retrieved). Product-level sentence for the H100 |
| T-16 | https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/ | TrendForce ("[News]") | `market_research_consultancy` (news digest) | reporter (originator: Chosun Biz) | "2025/12/24" (URL path) | 2026-10-07T16:44Z | `c521ff7a45d67c3ec53e220f0a1bddeeb5983cd082cd437eefb54d8491f7abdc` | 200 | dropped: names Trainium (unspecified) and **Trainium3** as using HBM3E; no maker for Trainium2 |
| T-17 | https://www.trendforce.com/news/2023/11/14/news-h200-unveiled-nvidia-integrates-hbm3e-for-enhanced-ai-performance/ | TrendForce ("[News]", byline "editor") | `market_research_consultancy` (news digest) | reporter of its own earlier release | "2023-11-14" | 2026-10-07T16:45Z | `08f97f9003a56649b575c4552599241fe4b83746d88d8bd73db0fe09a2d1326d` | 200 | **kept, weak**: says SK hynix and Samsung "began their efforts with HBM3, which is used in NVIDIA's H100/H800"; it does not say whose HBM3 is in the H100 |
| T-18 | https://www.trendforce.com/news/2024/06/03/news-heated-competition-driven-by-the-booming-ai-market-a-quick-glance-at-hbm-giants-latest-moves-and-whats-next/ | TrendForce ("[News]", byline "editor") | `market_research_consultancy` (news digest) | originator/reporter: repeats T-15's sentence without citing it | "2024-06-03" | 2026-10-07T16:45Z | `fde98b14bb2c6343dd7df469e9e81a642c60a225c0be70b4df9b0fa69a9c1ccd` | 200 | **kept** (same publisher as T-15: one voice, ER-7) |
| T-19 | https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential | SemiAnalysis (byline "Dylan Patel, Daniel Nishball, Wega Chu, and 7 others") | `market_research_consultancy` (proposed; Verifier may prefer `research_report`) | originator of its own assessment (no source named for the Samsung sentence) | "Dec 04, 2025"; metadata datePublished "2025-12-04T19:06:20+00:00" | 2026-10-07T16:45Z | `f5516abea183865b8a650bbb62040ea7fed56dec5263272a2e2b6d1c04bacf79` | 200; post marked "Paid", the free part is readable up to "This post is for paid subscribers" (text line 397) | **kept**. Product-level sentence for Trainium2 ("Trn2"), in the free part. **Recent** |
| T-20 | https://trendforce.com/news/?p=29218 (→ https://www.trendforce.com/news/2024/12/13/news-samsung-reportedly-unable-to-supply-hbm3e-to-nvidia-in-2024-as-gap-with-sk-hynix-widens/) | TrendForce ("[News]") | news digest | reporter (Wccftech) | "2024/12/13" (URL) | 2026-10-07T16:45Z | `875194b8999c0cdc9c770447cd6c8570836941cfb2ca70be0e4c472e3495649d` | 200 | dropped: no H100, no Trainium |
| T-21 | https://www.digitimes.com/news/a20231207PD211/samsung-sk-hynix-hbm3-aws.html | DIGITIMES (byline "Daniel Chiang") | `news_media` | would be reporter | "Dec 7, 2023, 15:47" | 2026-10-07T16:45Z | `8971ee1b9a8dd797bf6d23c418c322bf4ae46b4327014f4f84536ffae758be69` | 200, body **paywalled** ("The article requires paid subscription.") | **pointer and access gap** (plan row 5; same article as S16.5's S-29 on `apps.digitimes.com`). Headline usable only as a pointer |
| T-22 | https://asia.nikkei.com/business/tech/semiconductors/nvidia-looks-to-procure-high-bandwidth-memory-chips-from-samsung | Nikkei Asia (byline "YIFAN YU") | `news_media` | reporter | "March 20, 2024 10:14 JST" | 2026-10-07T16:46Z | `188b3fe2131b0d14293bba2a23eb5016ba0190bddfcb147c551bf7e9cc4737ff` | 200; metadata `"isAccessibleForFree":false`; only the lead paragraph is in the HTML | **pointer and access gap** (paywall). Visible lead names no product |
| T-23 | https://asia.nikkei.com/business/tech/semiconductors/sk-hynix-ascends-as-new-memory-king-with-high-bandwidth-ai-chips | Nikkei Asia | `news_media` | reporter | metadata datePublished "2026-06-02T22:20:24.000Z" | 2026-10-07T16:46Z | `cd29d052b509747e282952889d02b36b0cf23a7a555f8d529582b0b5b4e6c065` | 200; `"isAccessibleForFree":false`; lead paragraph only | **pointer and access gap** (paywall). Visible text names no product |
| T-24 | https://www.bloomberg.com/news/articles/2024-07-30/samsung-begins-closing-gap-in-making-ai-memory-chips-for-nvidia | Bloomberg | would be `news_media` | would be reporter | not read | 2026-10-07T16:46Z | `88c3c5cb9a6355d56b2116cae89756dc423689846216c240aa75acbd1efb86c4` (challenge page) | 403, bot challenge | **access gap** |
| T-25 | https://www.bloomberg.com/news/articles/2025-12-02/amazon-rushes-latest-ai-chip-to-market-to-take-on-nvidia-google | Bloomberg | would be `news_media` | would be reporter | not read | 2026-10-07T16:46Z | `f3c91cd902c9cde1392ff1c5c8a452b6c0d5f5c3e757241a27b7818d9e467362` (challenge page) | 403, bot challenge | **access gap** (title concerns Trainium3) |
| T-26 | https://www.kedglobal.com/newsView/ked202206090017 | KED Global (same article as T-12, the publisher's other path for it) | would be `news_media` | would be reporter | not read | 2026-10-07T16:47Z | none (no bytes) | connection reset, as T-12 | **access gap** |
| T-27 | https://www.koreajoongangdaily.com/business/nvidia-will-buy-hmb3-memory-chips-sk-hynix-says/10824589 | Korea JoongAng Daily (article credited "Yonhap" at its foot) | `news_media` | reporter (originator: SK hynix) | "Published June 9, 2022 - 3:05 p.m."; "Modified June 9, 2022 - 7:59 p.m." | 2026-10-07T16:47Z | `c2bae05c63ea46930aa13ef44b2ebe1e27a5ef5ef80fd281965972cf99160b27` | 200 | **kept** (reports SK hynix's 2022 plan; see §3) |
| T-28 | https://semianalysis.substack.com/p/ai-capacity-constraints-cowos-and (→ https://newsletter.semianalysis.com/p/ai-capacity-constraints-cowos-and) | SemiAnalysis (byline "Dylan Patel, Myron Xie, and Gerald Wong") | `market_research_consultancy` (proposed) | originator of its own estimate | "Jul 05, 2023"; metadata "2023-07-05T20:29:23+00:00" | 2026-10-07T16:47Z | `d1b690074835b12a616d4ab5a33a082e56899f651d0bdb3eddce3ae4aea965ab` | 200; "Paid", free part readable to text line 76 | **kept, weak**: a market-share statement with an H100 clause (see §3) |
| T-29 | https://news.skhynix.com/en/sk-hynix-moves-further-into-the-global-spotlight/ | SK hynix (newsroom feature) | `company_marketing` (year-in-review feature) | party | "December 29, 2022" | 2026-10-07T16:48Z | `5bb5d1bdedb3923d69efbbe02513b05f09c70ec38a6c52b0a1567cb194c18113` | 200 | **kept**: past tense, but names NVIDIA, not the H100 (ER-9) |
| T-30 | https://news.skhynix.com/heritage/ (→ https://news.skhynix.com/en/heritage/) | SK hynix (newsroom "Heritage" timeline) | `company_marketing` | party | undated live page; entry "2022. 06" | 2026-10-07T16:48Z | `49170accd2490b9ca996cbc9e39f8d3a3e377882fdcd53abde8d8c2e3c6b49c2` | 200 | **kept**: company-level ("to NVIDIA"), no product (ER-9) |
| T-31 | https://news.skhynix.com/en/sk-hynix-showcases-its-next-generation-technologies-at-dell-technologies-world-2023/ | SK hynix (newsroom, "TECH&AI") | `company_marketing` (event report) | party | "May 25, 2023" | 2026-10-07T16:48Z | `fc644e00f314cdce2cf92d1c477244cfadad574163e93fb673f7cb992b11a3ac` | 200 | **kept**: H100 and SK hynix HBM3 in one paragraph, but no explicit supply statement (see §3) |
| T-32 | https://www.trendforce.com/news/2025/03/21/news-samsung-reportedly-gears-up-for-hbm3e-8h-supply-to-broadcom/ | TrendForce ("[News]") | news digest | reporter (Sedaily) | "2025/03/21" (URL) | 2026-10-07T16:48Z | `2469648d4b6f7016a6857e7298fe96bed171a313b89873264a815eca2e03eeff` | 200 | dropped: "Amazon is also showing strong interest"; no Trainium2, no supply |
| T-33 | https://www.trendforce.com/news/2025/04/09/news-hbm3e-showdown-samsung-reportedly-aims-8h-mass-supply-in-april-micron-12h-wins-on-heat-management/ | TrendForce ("[News]") | news digest | reporter | "2025/04/09" (URL) | 2026-10-07T16:48Z | `40771fb2f440cc2cfcfc786b243acb3ebeffd2c9496a5b46b60f8d70f3fc250d` | 200 | dropped: no Trainium2, no H100 |
| T-34 | https://www.tomshardware.com/news/sk-hynix-kicks-off-hbm-3-mass-production-ships-to-nvidia | Tom's Hardware (Future plc) | `news_media` | reporter (originator: SK hynix) | metadata datePublished "2022-06-09T18:18:26+00:00" | 2026-10-07T16:49Z | `277f4f9957c18534a6f0ef38b013a83a64d517b48a778b3ea1471a9920a837dd` | 200 | **kept, weak**: reports SK hynix's 2022 plan for the H100 |
| T-35 | https://www.techinsights.com/products/ame-2403-802 | TechInsights | `research_report` (catalogue page) | — | "Availability In Creation"; "Release Date 20/03/2029" (as printed) | 2026-10-07T16:49Z | `af4a0f0988531eb7dd4fe5999c8f43bfd8f1139aab7cabb820facbec9616aab2` | 200 | dropped: names the SK hynix HBM3 die, not the product it came from |

### 2.2 Considered but not retrieved

| URL / source | Publisher | Found by | Why not retrieved |
|---|---|---|---|
| sec.gov copies of SK hynix's 2026 DRS, F-1, F-1/A, 424B4; NVIDIA 8-Ks; Micron 10-K/10-Q/8-K/ARS; Amazon 8-Ks | parties, via SEC | Q31, Q33, Q34, Q35, Q36 | dropped: SEC EDGAR is not used (D-042). SK hynix's prospectus remains the largest unread party document (S16.5 gap, unchanged) |
| https://www.counterpointresearch.com/insight/post-insight-in-the-press-nvidia-supplier-sk-hynix-warns-of-demand-volatility-after-quarterly-profit-soars-158-on-ai-boom | Counterpoint (press-mention page) | Q29 | not retrieved: title is company-level and a "Counterpoint in the press" page (a reprint of a news article); no H100 or Trainium2 in title |
| https://www.koreajoongangdaily.com/business/sk-hynix-has-won-two-thirds-of-nvidias-next-gen-high-bandwidth-memory-orders-industry-sources/12030483 | Korea JoongAng Daily | Q29 | not retrieved: HBM4 / next-generation products, not H100 or Trainium2 |
| https://www.digitimes.com/news/a20250820PD240/hbm-nvidia-2026-samsung-sk-hynix.html | DIGITIMES | Q39 | not retrieved: about 2026 supply (later products); DIGITIMES bodies are paywalled (T-21) |
| https://www.tweaktown.com/news/96850/… ; design-reuse, iconnect007, milaero copies of the TrendForce release | trade sites | Q12, Q39 | dropped: copies of T-15 |
| https://newsletter.semianalysis.com/p/amazons-ai-self-sufficiency-trainium2-architecture-networking | SemiAnalysis | Q18 | not re-retrieved: S16.5's S-51 read its free part (no maker named); rest paywalled |
| https://newsletter.semianalysis.com/i/174558474/… (section anchors) | SemiAnalysis | Q2, Q19 | not retrieved: anchors inside a post; the post they belong to was not identified with certainty, and its section titles are spec overviews |
| Notebookcheck, gadgetreview, 247wallst, io-fund, leverageshares, siliconanalysts, longyield, wing.vc, plutux.ai, semiconductorx, introl, clarigital, drops.mts.now, astutegroup, mirrorfrog, itechguides, biggo, guru3d, techpowerup forum, hothardware, canaltech, next.ink, profesionalreview, geeknetic, vnreview, reportify.cn, technews.tw, intuitionlabs, 3dincites, semiconductor-digest, electronicspecifier | blogs, aggregators, consumer tech press | various | dropped without retrieval: not internationally recognised publishers in the §7.1 sense, or copies; none appeared to name a primary source not already sought |
| Korea Times 2024-07-24 (Samsung HBM3 for H20) | Korea Times | Q17 | not retrieved: H20, not H100 |
| Bloomberg 2024-03-07, 2024-05-02, 2025-09-12, 2026-01-13, 2026-01-23, 2026-01-27, 2026-01-28, 2026-05-27, 2026-06-07, 2026-07-09, 2026-07-10; Bloomberg Intelligence press page; Bloomberg graphics 2026 | Bloomberg | Q25, Q26 | not retrieved: four Bloomberg requests (T-10, T-13, T-24, T-25) all returned the bot challenge, so further requests to the host were judged futile; titles are company-level or about other products |

---

## 3. Anchors in the kept sources

Verbatim from the locally extracted text, each at most two lines. Columns follow the brief's step 5:
**Product** (names H100 / a variant / Trainium2?), **HBM** (says HBM, not just memory?), **Fact/plan**, **Scope**
(one examined unit = teardown, or supply in general), **Date** (the source's).

### Q-H100

| T-id | Locator | Anchor | Product | HBM | Fact / plan | Scope | Date |
|---|---|---|---|---|---|---|---|
| T-15 | 2nd paragraph of the release body (text line 123 and again below the headline) | "The current HBM3 supply for NVIDIA's H100 solution is primarily met by SK hynix, leading to a supply shortfall…" | "H100 solution"; no variant | yes, HBM3 | present tense as of the release date (fact as worded, not a plan) | supply in general; "primarily" (not sole) | 2024-03-13 |
| T-15 | same paragraph, next sentence | "Samsung's entry into NVIDIA's supply chain with its 1Znm HBM3 products in late 2023, though initially minor, signifies its breakthrough…" | **no**: "NVIDIA's supply chain", H100 not named in this sentence | yes, HBM3 | past (late 2023) | company-level (ER-9 flag) | 2024-03-13 |
| T-18 | paragraph beginning "Years after the first AI server GPU with HBM" (text line 153) | "The current HBM3 supply for NVIDIA's H100 is primarily met by SK hynix." | H100; no variant | yes | present tense | general | 2024-06-03 |
| T-18 | closing paragraph (text line 165) | "In the era of HBM3, the supply for NVIDIA's H100 solution is primarily met by SK hynix at first." | H100 | yes | past framing ("at first") | general | 2024-06-03 |
| T-17 | paragraph beginning "SK hynix and Samsung began their efforts with HBM3" (text line 162) | "SK hynix and Samsung began their efforts with HBM3, which is used in NVIDIA's H100/H800 and AMD's MI300 series products." | H100/H800 | yes | fact as worded, but says only that HBM3 (the type) is used in the H100, not whose | general; maker-to-product link **not stated** | 2023-11-14 |
| T-28 | section "The HBM Market: SK Hynix Dominance…", 1st paragraph (text line 40) | "…currently the only supplier shipping HBM3 in volume, with over 95% market share, which is what most H100 SKUs are using." | "most H100 SKUs" | yes, HBM3 | present tense (2023) | market share plus a clause on H100 SKUs; whether "which" refers to HBM3 or to SK hynix's HBM3 is grammatically open | 2023-07-05 |
| T-28 | same section, Samsung paragraph (text line 42) | "Samsung is next behind Hynix and expects to ship HBM3 in the second half of 2023. We believe they are designed for both Nvidia and AMD GPUs." | no product | yes | plan / belief | company-level | 2023-07-05 |
| T-03 | body paragraph beginning "The SK hynix H5VG7HMD83X020R was found inside" (text line 218) | "The SK hynix H5VG7HMD83X020R was found inside NVIDIA's Grace Hopper Superchip used in the use in Quanta Computer Inc's S74G-2U QuantaGrid server…" | **other product**: Grace Hopper Superchip (GH200), not an H100 variant | yes, HBM3 | fact (observation) | **one examined unit** (teardown) | undated |
| T-03 | same paragraph, 2nd sentence | "The NVIDIA GH100-888K-A1 Hopper GPU is a 2.5D/3D multi-die system in package (SiP)…containing six SK hynix 16 GB 4th generation HBM3 DRAM sub-packages…" | GH100 GPU package inside the GH200 unit; no H100 variant named | yes | fact (observation) | one unit | undated |
| T-05/06/07 | catalogue headers | "NVIDIA Hopper H100 GPU Advanced Packaging Analysis" (T-05); T-07 lists "package photographs, package X-rays, die markings, and die photographs" | H100; variant not named (T-05/T-06 item code "NVI-PCB_699-21010-0200-600") | — | — | a teardown exists; **no memory maker on the public page** | 2023-06-30 / 07-10 / 07-28 |
| T-27 | body, 6th paragraph | "Nvidia recently finished its performance review of HMB3 and will use it in its latest graphic processor unit, the H100, …according to SK hynix." | H100 | yes ("HMB3" [sic]) | **plan** ("will use") | general | 2022-06-09 |
| T-27 | body, 1st paragraph | "SK hynix said Thursday it has started mass production of a high-end product…and will supply it to American graphics-chip maker Nvidia." | no product in this sentence | "high-end product" | plan ("will supply") | company-level | 2022-06-09 |
| T-34 | article body, 1st paragraph (text line 534; the page uses non-breaking spaces between some words) | "…it had begun to mass produce HBM3 memory and these DRAMs will be used by Nvidia for its H100 compute GPUs and DGX H100 systems…" | H100 | yes | **plan** ("will be used") | general | 2022-06-09 |
| T-29 | paragraph beginning "The innovations continued into the summer" (text line 54) | "…SK hynix became the first company to mass produce HBM3…in June—which it supplied to NVIDIA." | **no**: NVIDIA, not the H100 | yes | **past tense** | company-level (ER-9) | 2022-12-29 |
| T-30 | timeline entry "2022. 06" | "SK hynix Supplies the Industry's First HBM3 DRAM to NVIDIA" | no | yes | headline of the 2022 release (S16.5's S-20, which is worded as a plan) | company-level | undated page |
| T-31 | paragraph beginning "In addition, SK hynix displayed its CXL" (text line 59) | "…held a joint exhibition of its HBM3* and NVIDIA's H100 GPU. Used for AI chatbots, NVIDIA's H100 GPU has adopted HBM3…" | H100 | yes | fact as worded, but says the H100 "has adopted HBM3" (the type), not SK hynix's HBM3; the link is by juxtaposition at a booth | general | 2023-05-25 |

### Q-TRN2

| T-id | Locator | Anchor | Product | HBM | Fact / plan | Scope | Date |
|---|---|---|---|---|---|---|---|
| T-19 | free part, paragraph beginning "The HBM3E is upgraded to 12-high for Trainium3" (text line 52) | "In fact, the 5.7Gbps pin speed that was used in Trn2 is more in line with HBM3 speeds, but it is still classified as HBM3E…" | Trn2 = Trainium2 (the same paragraph contrasts Trn2 with Trn3) | yes, HBM3E | past tense ("was used") | general | 2025-12-04 |
| T-19 | same paragraph, next sentences | "The speed deficiency was due to using memory supplied by Samsung, whose HBM3E is notably sub-par compared to that of Hynix or Micron." | Trn2 (by the paragraph's subject; the sentence itself does not repeat "Trn2") | "memory" in the clause, "HBM3E" in the same sentence | past / present, stated as fact; no source named; contains a comparative judgement (ER-5) | general; does not say Samsung was the **only** supplier | 2025-12-04 |
| T-19 | same paragraph | "For the HBM used in Trainium3, AWS is switching to Hynix and Micron to achieve much faster speeds." | **other product** (Trainium3) | yes | present progressive / plan | general | 2025-12-04 |
| T-21 | headline (body paywalled) | "Samsung and SK Hynix will both supply HBM3 for AWS Trainium 2" | Trainium 2 | yes, HBM3 | **plan** ("will") | general | 2023-12-07 |
| T-16 | paragraph "Google and Amazon Drive Additional HBM3E Demand" (text line 150) | "…Amazon's Trainium—both equipped with HBM3E—are scheduled to begin shipments in 2026… Amazon's Trainium3 reportedly uses four stacks." | Trainium (unspecified) / Trainium3; **not Trainium2** | yes | plan | general, no maker | 2025-12-24 |

**Note on T-19 vs T-21.** The two disagree in form: DIGITIMES (2023, a plan, paywalled) says Samsung and SK hynix
"will both supply HBM3"; SemiAnalysis (2025, past tense) attributes Trn2's HBM3E speed to "memory supplied by
Samsung" and names no second supplier. Neither text excludes the other. Recorded, not resolved.

---

## 4. Proposed §7.1 criteria for the kept third-party sources (for the Verifier)

"Recent" = stated date on or after 2025-10-07. Party sources (T-29, T-30, T-31) are not third parties; the
criteria do not apply to them.

| T-id | Publisher | Recognised? (proposed, with reason) | Independent? (proposed, with what was checked) | Recent? |
|---|---|---|---|---|
| T-15 | TrendForce | **yes**: an established Taiwan-based market-intelligence firm, named by the human as an example in `plan.md` | **yes, as far as seen**: the release names no sponsor or client for this statement and is a general market release; ownership was not researched | **no** (2024-03-13): historical only |
| T-18 | TrendForce | **yes** (same publisher as T-15) | **yes, as far as seen**; same publisher as T-15, so not an independent second voice (ER-7) | **no** (2024-06-03) |
| T-17 | TrendForce | **yes** | **yes, as far as seen** | **no** (2023-11-14) |
| T-19 | SemiAnalysis | **uncertain, proposed yes with low confidence**: an independent semiconductor research and consulting firm whose analysis is widely quoted in the trade and financial press; it is **not** on the human's example list, and the scout retrieved no evidence that parties, governments or intergovernmental bodies routinely cite it | **uncertain, proposed yes**: no sponsor, commission or disclosure in the retrieved text (searched for "sponsor", "disclos", "commission", "client", "conflict"); SemiAnalysis sells models and consulting to industry clients, which may include parties or their competitors; not researched further. The sentence disparages one party (Samsung) relative to its competitors, which the Verifier may weigh | **yes** (2025-12-04) |
| T-28 | SemiAnalysis | as T-19 | as T-19 | **no** (2023-07-05) |
| T-27 | Korea JoongAng Daily (story credited to Yonhap) | **partly**: Yonhap is South Korea's national news agency and JoongAng Ilbo a major Korean daily; whether either counts as "internationally recognised" in §7.1's sense is for the Verifier | **yes as publisher**, but the statement is SK hynix's own (reporter standing; the originator is a party) | **no** (2022-06-09); also a plan (ER-8) |
| T-34 | Tom's Hardware | **no** (proposed): a consumer and trade technology site, not a news agency, newspaper of record or analysis firm | **yes as publisher**, ad-funded; the statement is SK hynix's (reporter) | **no** (2022-06-09); a plan |
| T-03 | TechInsights | **yes**: an established reverse-engineering and teardown firm, named in `plan.md` | **yes, as far as seen**: no sponsor named on the page | undated; and **other product** (GH200), so outside Q-H100 as worded |
| T-05/06/07 | TechInsights | **yes** | **yes, as far as seen** | no (2023); content not accessible |

---

## 5. Per question: found, access gaps, not searched

### Q-H100 — who supplies the HBM in the NVIDIA H100

**Found (retrieved and readable):**

- **Third-party, product-level, present tense in its day:** TrendForce's press release (T-15, 2024-03-13): H100
  HBM3 supply "primarily met by SK hynix"; repeated in TrendForce news items (T-18, 2024-06-03). One voice. Not
  recent; names no H100 variant; says "primarily", not "only".
- **Weaker third-party statements:** T-17 (HBM3 type used in the H100; makers not linked to it), T-28 (SemiAnalysis
  2023: market share, with an ambiguous clause on "most H100 SKUs").
- **Party, past tense, but company-level:** SK hynix T-29 (2022-12-29, "which it supplied to NVIDIA") and T-30
  (heritage timeline). Neither names the H100 (ER-9).
- **Party, product-adjacent:** SK hynix T-31 (2023-05-25) exhibits its HBM3 with the H100 and says the H100 "has
  adopted HBM3"; it does not say the H100's HBM3 is SK hynix's.
- **Plans only (2022):** T-27 (Korea JoongAng Daily / Yonhap) and T-34 (Tom's Hardware), both reporting SK hynix's
  2022 plan; S16.5's S-20 is the original.
- **Teardowns:** TechInsights has published H100 teardown reports (T-05, T-06, T-07, 2023), but the public pages do
  not name the HBM maker. The only readable TechInsights statement naming an HBM maker from a unit (T-03) concerns
  a **Grace Hopper Superchip** (GH200) unit, not an H100 SXM5 / PCIe / NVL.
- **Nothing recent** (on or after 2025-10-07) naming the H100's HBM maker was found.

**Access gaps:**

- TechInsights H100 reports (T-05, T-06, T-07): paid content; the public pages name no maker. Candidate for RA-4
  only if the human already has legitimate access.
- Yole Group H100 report page and SK hynix HBM3 report page (T-01, T-02): 403 CloudFront.
- Bloomberg (T-10, T-13, T-24): bot challenge.
- KED Global 2022-06-09 (T-12, T-26): connection reset at the relay.
- Nikkei Asia (T-22): paywalled (visible lead names no product).
- Business Wire copy of T-15 (T-11): 403, not needed.
- SK hynix 2026 US prospectus: SEC only (D-042), unchanged from S16.5.

**Not searched:** Reuters, FT, WSJ and AP (the search tool refused those domains and returned none of their URLs:
see §1); Omdia (no page found); Counterpoint beyond one press-mention title; NVIDIA past-tense statements beyond
Q35 (none found); Samsung's newsroom (still unreachable per S16.5, and Q32 found nothing); Korean-language press;
TechInsights library items behind login.

### Q-TRN2 — who supplies the HBM in AWS Trainium2

**Found (retrieved and readable):**

- **Third-party, product-level, past tense, recent:** SemiAnalysis "AWS Trainium3 Deep Dive" (T-19, 2025-12-04),
  free part: Trn2's HBM3E speed deficiency "was due to using memory supplied by Samsung". No source named; does not
  say Samsung was the only supplier; contains a comparative judgement. Recognition and independence are uncertain
  (§4).
- **Pointer only:** DIGITIMES 2023-12-07 (T-21) headline "Samsung and SK Hynix will both supply HBM3 for AWS
  Trainium 2" (a plan; body paywalled).
- No teardown of a Trainium2 unit was found by any query (Q2, Q7, Q8).
- No party statement (AWS, SK hynix, Samsung, Micron) naming Trainium2 with an HBM maker, past or future, was found
  (Q33, Q34, Q36, plus S16.5's searches).

**Access gaps:** DIGITIMES body (T-21, paywall); SemiAnalysis paid sections of T-19 and of the 2024-12-03 Trainium2
post (S16.5 S-51); Bloomberg (T-25, bot challenge, and its title concerns Trainium3); Micron IR newsroom and
Samsung newsroom (S16.5 gaps, not retried).

**Not searched:** Reuters, FT, WSJ, AP (tool refusal, as above); Omdia and Counterpoint for Trainium2 specifically
(Q16 and Q38 surfaced neither); Yole Group for Trainium2 (no candidate surfaced; Yole's host refused requests in
any case); Korean-language press; AWS re:Invent 2024 and 2025 session material and Hot Chips slides (S16.5 Q28 found
none hosted by AWS; not re-searched).
