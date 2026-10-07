# S16.5 search log: who supplies the HBM in the H100 and in Trainium2

Written by the **Source Scout, S16.5**, on **2026-10-07**. It follows `plan.md` (rows 1 to 8, in order).

What this log is: a record of every search query, every candidate URL, what was retrieved, and the
short verbatim anchors found in each retrieved text. What it is not: a decision. It does not say what is
canonical, what counts as an answer, or what evidence status any claim has. Those belong to the
Extractor and the Verifier. The scout wrote nothing under `data/`.

**Method.** Web search was used only to find URLs. Each kept URL was retrieved once with plain `curl`
(default client identity, no custom headers, through the session's preconfigured HTTPS proxy), and the raw
bytes were hashed with `sha256sum`. Text was extracted locally (`pdftotext -layout` for PDFs; a Python
standard-library HTML parser, run with `python3 -I`, for HTML). Refusals, challenge pages, empty
replies, paywalls and empty JavaScript shells were recorded as access gaps and not worked around. SEC EDGAR
was not used (D-042); a result on `sec.gov` was dropped. Raw files and extracted texts are in the scout's
scratchpad (`.../scratchpad/s165-sources/`, files `S-01` to `S-51`), not in the repository.

**Dates.** "Stated date" is the date the document prints for itself (or puts in its page metadata, as
labelled). "Undated" means no date for the content was found; a copyright year in a page footer is shown
but is not a publication date. Access times are UTC.

**Classes** are the scout's proposal, using the neighbour tests in `source-policy.md` §3. The Extractor and
Verifier may reclassify.

---

## 1. Search queries

All queries were run on 2026-10-07 with the WebSearch tool. "Domains" means the search was limited to the
listed domains.

| # | Query text | Domains | Plan row | Question |
|---|---|---|---|---|
| Q1 | NVIDIA H100 Tensor Core GPU datasheet PDF | none | 1 | Q-H100 |
| Q2 | NVIDIA H100 Hopper architecture whitepaper HBM3 | none | 1 | Q-H100 |
| Q3 | H100 datasheet PDF site nvidia.com | nvidia.com, resources/images/docs/developer.nvidia.com | 1 | Q-H100 |
| Q4 | Hopper architecture whitepaper gtc22 nvidia | same as Q3 | 1 | Q-H100 |
| Q5 | H100 HBM3 SK hynix Micron Samsung | nvidia.com, nvidianews, docs, developer, investor.nvidia.com | 1 (also found a row-8 candidate) | Q-H100 |
| Q6 | Trainium2 architecture Neuron documentation HBM | none | 2 | Q-TRN2 |
| Q7 | Amazon EC2 Trn2 instances Trainium2 HBM memory | aws.amazon.com, amazon.com, aboutamazon.com, docs.aws.amazon.com | 2 | Q-TRN2 |
| — | (no search: the URL of NVIDIA's FY2026 Form 10-K was taken from `source-policy.md` §8.3, S05-R1) | — | 3 | Q-H100 |
| Q8 | Amazon.com 2025 annual report Form 10-K PDF ir.aboutamazon.com | none | 4 | Q-TRN2 |
| Q9 | Amazon 10-K 2025 annual report | ir.aboutamazon.com, s2.q4cdn.com, aboutamazon.com | 4 | Q-TRN2 |
| Q10 | SK hynix HBM3 NVIDIA H100 supply | skhynix.com, news.skhynix.com, product.skhynix.com | 5 | Q-H100 |
| Q11 | SK hynix annual report 2025 English PDF | none | 5 | both |
| Q12 | SK hynix investor relations business report English 2025 audit report | skhynix.com | 5 | both |
| Q13 | SK hynix HBM product page HBM3E HBM3 | skhynix.com, product.skhynix.com | 5 | both |
| Q14 | skhynix.com ir annual report disclosure "Business Report" OR "Annual Report" SK hynix 2025 pdf download | skhynix.com | 5 | both |
| Q15 | SK hynix ADR prospectus F-1 NYSE listing 2026 HBM customers NVIDIA | none | 5 | both |
| Q16 | SK hynix prospectus American depositary shares registration statement | skhynix.com, news.skhynix.com | 5 | both |
| Q17 | SK hynix HBM AWS Trainium | skhynix.com, news.skhynix.com | 5 | Q-TRN2 |
| Q18 | Trainium2 HBM supplier SK hynix Samsung Micron | none | pointer search | Q-TRN2 |
| Q19 | Micron fiscal 2025 Form 10-K annual report PDF investors.micron.com | micron.com, investors.micron.com, q4cdn.com | 6 | both |
| Q20 | Micron HBM3E H100 OR H200 OR Trainium | micron.com, investors.micron.com | 6 | both |
| Q21 | Samsung Electronics 2025 business report English PDF investor relations | samsung.com, images.samsung.com | 7 | both |
| Q22 | Samsung HBM3 HBM3E product page Icebolt Shinebolt semiconductor.samsung.com | semiconductor.samsung.com, samsung.com, news.samsung.com | 7 | both |
| Q23 | NVIDIA newsroom SK hynix HBM supply partnership press release 2026 | nvidianews.nvidia.com, news.skhynix.com, blogs.nvidia.com | 8 | Q-H100 |
| Q24 | Samsung HBM NVIDIA H100 OR Trainium press release | news.samsung.com, semiconductor.samsung.com, nvidianews.nvidia.com | 8 | both |
| Q25 | Trainium2 HBM memory press release SK hynix OR Samsung OR Micron Amazon | press.aboutamazon.com, aboutamazon.com, aws.amazon.com, news.skhynix.com, news.samsung.com, micron.com, semiconductor.samsung.com | 8 | Q-TRN2 |
| Q26 | Micron commences volume production HBM3E NVIDIA H200 news release | micron.com | 8 | Q-H100 |
| Q27 | Micron fiscal 2026 Form 10-K annual report | micron.com, q4cdn.com | 6 | both |
| Q28 | Trainium2 Hot Chips presentation HBM3 stacks AWS | none | 2 / pointer search | Q-TRN2 |

---

## 2. Candidate URLs

"Party" means the publisher is a party to that question's supplier claim under `source-policy.md` §4:
the accelerator's vendor (NVIDIA for Q-H100; Amazon/AWS for Q-TRN2) or an HBM maker that could name
itself as the supplier (SK hynix, Micron, Samsung). Stated dates are as printed. Hashes are of the raw
bytes received, including for refusals.

### 2.1 Retrieved (an HTTP response was received)

| S-id | URL (final URL after redirects, if different) | Publisher | Proposed class | Party to | Stated dates | Access (UTC) | sha256 | HTTP | Kept / dropped, why |
|---|---|---|---|---|---|---|---|---|---|
| S-01 | https://www.nvidia.com/en-us/data-center/h100/ | NVIDIA | `company_marketing` (product page with a spec table) | Q-H100 | undated (live page); footer "Copyright © 2026" | 2026-10-07T15:21Z | `096f1d0be2cfc7c13cfbd1c610cd5ce648a1f48447cf103aa4a0e7f4cb6eaa37` | 200 | kept; HBM named, no memory maker |
| S-02 | https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf | NVIDIA | `company_technical_documentation` (H100 PCIe product brief) | Q-H100 | "PB-11133-001_v02 \| November 2022"; history: v01 "September 30, 2022", v02 "November 30, 2022" | 2026-10-07T15:21Z | `66ed708d7fb1a7dc5adb83e4852243a99c47d0c19afb3d501211f052f6d28fa7` | 200 | kept; HBM2e named, no memory maker |
| S-03 | https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/h100/PB-11773-001_v01.pdf | NVIDIA | `company_technical_documentation` (H100 NVL product brief) | Q-H100 | "PB-11773-001_v01 \| March 2024"; history: "March 14, 2024 … Initial release" | 2026-10-07T15:21Z | `08fdff16f08b72010c206dd9c1aa6291620e108d11cbfea84080ff8be728b6ef` | 200 | kept; HBM3 named, no memory maker |
| S-04 | https://resources.nvidia.com/en-us-data-center-overview/gtc22-whitepaper-hopper (→ https://resources.nvidia.com/en-us-hopper-architecture/nvidia-h100-tensor-c) | NVIDIA | none (a document-viewer page, not a source) | — | — | 2026-10-07T15:21Z | `aa9182036ccbe9b65fa0b5b9b952ce07324718747e3b899edcd588e9edbf3c4e` | 200 | dropped as a source; used only to find the PDF links it embeds (S-07, S-08, S-09) |
| S-05 | https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/ | NVIDIA (Technical Blog) | `company_technical_documentation` (architecture in depth) | Q-H100 | page metadata: datePublished "2022-03-22T18:00:00+00:00", dateModified "2025-07-22T22:49:15+00:00" | 2026-10-07T15:21Z | `f535ec409ba3c81418c05c787cd8a336da6b0e7f8965496ec8f29ed565d17ccd` | 200 | kept; HBM3/HBM2e named, no memory maker |
| S-06 | https://resources.nvidia.com/en-us-tensor-core/nvidia-tensor-core-gpu-datasheet (→ https://www.nvidia.com/en-us/) | NVIDIA | none | — | — | 2026-10-07T15:21Z | `f323271d64317f6115bde8a0fe3b0fe66467af380b1b9dc13b07fd4b1a7816df` | 200 after redirect | dropped: redirected to NVIDIA's home page; the datasheet was not served at this URL (the current datasheet was found as S-11) |
| S-07 | https://dam-cdn.nvd.orangelogic.com/AssetLink/705n6ur546g0uk43w0117r17n8042d73.pdf | NVIDIA ("NVIDIA H100 Tensor Core GPU Architecture" whitepaper) | `company_technical_documentation` | Q-H100 | "V1.04"; "Copyright © 2023 NVIDIA Corporation"; PDF metadata created 2023-05-04 | 2026-10-07T15:22Z | `3641614979809a027a8aabdc2e77639efb8fcd0f8dc7873a22ba2125489f5a27` | 200 | kept; HBM3/HBM2e named, no memory maker. Host note: the file is served from NVIDIA's digital-asset CDN domain (`dam-cdn.nvd.orangelogic.com`), as the `sourceUrl` that NVIDIA's own page S-04 embeds for "NVIDIA H100 GPU Whitepaper" |
| S-08 | https://dam-cdn.nvd.orangelogic.com/AssetLink/mfj81tsm68n0ne632upmuvirso3ta3g3.pdf | NVIDIA ("NVIDIA H100 \| Tensor Core GPU" datasheet, older edition) | `company_technical_documentation` | Q-H100 | "© 2022 NVIDIA Corporation"; PDF metadata created 2022-05-17 | 2026-10-07T15:22Z | `200a1084af6cc4a7d1195124a26f5b2915f1e2cf9fa307c02ad47079a750c785` | 200 | kept; no memory maker. Same host note as S-07 (linked from S-04) |
| S-09 | https://dam-cdn.nvd.orangelogic.com/AssetLink/44wa8u63l12ps4ie2870214xa2exoyra.pdf | NVIDIA ("NVIDIA HGX H100 \| NVIDIA HGX H200 Datasheet") | `company_technical_documentation` | Q-H100 | "© 2024 NVIDIA Corporation"; PDF metadata created 2024-07-30 | 2026-10-07T15:22Z | `e51ee5fb7d9aca6040ad03cc061264221ef5f2078e5d0080481553c4059a3e3e` | 200 | kept; no memory maker. Same host note (linked from S-04) |
| S-10 | https://resources.nvidia.com/en-us-gpu-resources/h100-datasheet-24306 | NVIDIA | none (document-viewer page) | — | — | 2026-10-07T15:22Z | `e91bd5de38596239004ee42e2db530716ff7465bfb7d944b2d8028199beb945c` | 200 | dropped as a source; used only to find the "NVIDIA H100 GPU Datasheet" PDF link (S-11) |
| S-11 | https://dam-cdn.nvd.orangelogic.com/AssetLink/u5hh6fv4r7564i4y673484y3m20083nj.pdf | NVIDIA ("NVIDIA H100 Tensor Core GPU Datasheet", current edition) | `company_technical_documentation` | Q-H100 | "© 2024 NVIDIA Corporation"; PDF metadata created 2024-09-23 | 2026-10-07T15:22Z | `17494a1792c15c55bae2453305e265ad508987b474e9235ecbc6f7c815399b98` | 200 | kept; HBM3 named, no memory maker. Same host note (linked from S-10) |
| S-12 | https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html | Amazon/AWS (AWS Neuron documentation) | `company_technical_documentation` | Q-TRN2 | undated content; site banner "Neuron 2.32.0 is released!"; footer "© Copyright 2026, Amazon.com." | 2026-10-07T15:23Z | `746c25212873fd403894481c62b4cd1535b02ebf4f7439ae98b507fe47400cbf` | 200 | kept; HBM named, no memory maker |
| S-13 | https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html | Amazon/AWS (Neuron "Trainium2 Architecture Guide for NKI") | `company_technical_documentation` | Q-TRN2 | undated content; same banner and footer as S-12 | 2026-10-07T15:23Z | `3ec620f26a54c4fd677899ecf396037d6e4e0846e6c9c84dd654eecc33f4ea25` | 200 | kept; HBM named, no memory maker |
| S-14 | https://aws.amazon.com/ec2/instance-types/trn2/ | Amazon/AWS | `company_marketing` (instance page with a spec table; could be argued `company_technical_documentation`) | Q-TRN2 | undated (live page); footer "© 2026" | 2026-10-07T15:23Z | `4ccc9a5b26daccc8fe4a979323421ef93a9d61fed1930585033c9cdaa200d776` | 200 | kept; HBM named, no memory maker |
| S-15 | https://aws.amazon.com/ai/machine-learning/trainium/ | Amazon/AWS | `company_marketing` | Q-TRN2 | undated (live page); footer "© 2026" | 2026-10-07T15:23Z | `5a539451bcff098d4f29b3b1de3e6b098039cba7b5948177f484d0fc6fd1cdfa` | 200 | kept; mentions Trainium3 HBM3e, no memory maker |
| S-16 | https://aws.amazon.com/blogs/aws/amazon-ec2-trn2-instances-and-trn2-ultraservers-for-aiml-training-and-inference-is-now-available/ | Amazon/AWS (AWS News Blog, Jeff Barr) | `company_press_release` (announces a dated launch) | Q-TRN2 | "03 DEC 2024"; update note "12/3/2024: Updated chip-to-chip communication…" | 2026-10-07T15:23Z | `d6e5a045eef1d318d8e6d16b849382984b3a1314fc8186f0cf97eae3fd27839e` | 200 | kept; HBM named, no memory maker |
| S-17 | https://aws.amazon.com/about-aws/whats-new/2024/12/amazon-ec2-trn2-instances-available/ | Amazon/AWS ("What's New") | `company_press_release` | Q-TRN2 | "Posted on: Dec 3, 2024" | 2026-10-07T15:23Z | `68acb0961a522a45fd97b7cfa07bfd190528e90e839fd7c6399d373e48fe7758` | 200 | kept; "high bandwidth memory" named, no memory maker |
| S-18 | https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf (→ https://s201.q4cdn.com/141608511/files/doc_financials/2026/q4/10K-NVDA.pdf) | NVIDIA (Form 10-K, fiscal year ended January 25, 2026; company-hosted copy) | `company_filing` | Q-H100 | fiscal year ended January 25, 2026; signed 2026-02-25 (per §8.3, not re-read here) | 2026-10-07T15:23Z | `a056b59e4170c0123217a8e861a39af4a4a48d2df0d27b641017a618a280a396` | 200 | kept; company-level "memory" suppliers. The hash prefix matches S05-R1 (`a056b59e4170`, §8.3), so the bytes are probably unchanged since 2026-09-30 (only the prefix was compared). Identity with the SEC copy: not checked (EDGAR not used) |
| S-19 | https://s2.q4cdn.com/299287126/files/doc_financials/2026/ar/Amazon-2025-Annual-Report.pdf | Amazon.com, Inc. (2025 Annual Report, which contains the Form 10-K for the fiscal year ended December 31, 2025, and a shareholder letter) | `company_filing` (for the Form 10-K pages; the shareholder letter at the front is not the filing) | Q-TRN2 | 10-K for fiscal year ended December 31, 2025; auditor's report dated "February 5, 2026" | 2026-10-07T15:24Z | `63196177ef83756ddfaff5aacda547f0eabac4669c0f6144bcee8401cd8cfbfc` | 200 | kept; company-level semiconductor-supplier and memory-chip statements, no memory maker named. Host: Amazon's investor-relations file host (s2.q4cdn.com, found via search filtered to Amazon IR domains). Identity with SEC copy: not checked |
| S-20 | https://news.skhynix.com/en/sk-hynix-to-supply-industrys-first-hbm3-dram-to-nvidia/ | SK hynix (newsroom, labelled "PRESS") | `company_press_release` | Q-H100 | "June 8, 2022" | 2026-10-07T15:24Z | `3712f70b893f491fda26a1e47826ca83a0161beeee78b33290c3b1de9593174a` | 200 | kept; product-level statement naming the H100 and HBM3 (see §3). Date is before 2025-10-07 |
| S-21 | https://product.skhynix.com/products/dram/hbm/hbm3.go | SK hynix | `company_marketing` (product page) | both | undated; footer "COPYRIGHT ©2021" | 2026-10-07T15:24Z | `7a2f63276073249441518f51a34ab29ea430986d5a7e835b4e68ea4b90ee664e` | 200 | kept; names no customer product |
| S-22 | https://product.skhynix.com/products/dram/hbm/hbm3e.go | SK hynix | `company_marketing` (product page) | both | undated | 2026-10-07T15:24Z | `efbc05090de2f9210e28fd14c0a4f3fc5bed1cd4229dc8737794871b8d174ffc` | 200 | kept; names no customer product |
| S-23 | https://news.skhynix.com/en/sk-hynix-announces-fy25-financial-results/ | SK hynix | `company_press_release` | both | "January 28, 2026" ("Seoul, January 28, 2026") | 2026-10-07T15:24Z | `581a8e28f3db3a5daaf58d71ec5a29718113bd890af8222b1f3b535a4912e864` | 200 | kept; company-level HBM statements, no customer named |
| S-24 | https://www.skhynix.com/ir/UI-FR-IR06/ | SK hynix (IR, "Earnings Release") | none | — | — | 2026-10-07T15:24Z | `2e5eda94f4b75b47997e599a5085b0aacde02b2762146d7d7945cbb2284a8133` | 200 | **access gap**: page shell; the document list is loaded by JavaScript and is not in the HTML. URL was reached by IR navigation, not search |
| S-25 | https://www.skhynix.com/ir/UI-FR-IR01/ | SK hynix (IR home) | none | — | — | 2026-10-07T15:25Z | `1c8f38a5a3be27cfc54d586b6e78bf788a6618bae62fb84944c989774f46a774` | 200 | used for navigation only. Its menu shows "Earnings Release", "Annual/Quarterly Operating Report", "Ownership Structure", "Financial Statements", "IR Events", "IR Material"; no annual report or business report item was visible |
| S-26 | https://www.skhynix.com/ir/UI-FR-IR07/ | SK hynix (IR, "Financial Statements") | none | — | — | 2026-10-07T15:25Z | `4115d05ff90d48a9fb0f8a2b0d3d1f727a5618d040add3656d2e4b1e0c8cf854` | 200 | **access gap**: empty JavaScript shell (heading only, no documents in the HTML) |
| S-27 | https://www.skhynix.com/ir/UI-FR-IR10/ | SK hynix (IR, "IR Event") | none | — | — | 2026-10-07T15:25Z | `d15eed4bc32dd29f5d5fe18603674f4aa664eb668858d27649e755756d4a95c5` | 200 | **access gap**: empty JavaScript shell |
| S-28 | https://news.skhynix.com/en/2026-market-outlook-focus-on-the-hbm-led-memory-supercycle/ | SK hynix (newsroom feature) | `company_marketing` (editorial feature that reports analysts' views; `reporter` standing for those) | Q-TRN2 (SK hynix) | "January 5, 2026" | 2026-10-07T15:26Z | `9fff80315bf4e25f31c117ba49e2b588ca66abe99b4eafd16f583ed54435202c` | 200 | kept; mentions AWS choosing HBM3E in general; names no supplier for AWS and no Trainium product |
| S-29 | https://apps.digitimes.com/news/a20231207PD211/samsung-sk-hynix-hbm3-aws.html | DIGITIMES | `news_media` (pointer only) | not a party | "Dec 7, 2023, 15:47" | 2026-10-07T15:26Z | `f66755a290a115618b895730c0d125609260ea6dd9c2d2712ac557a6f7dd7c64` | 200 | **pointer; body behind paywall** ("The article requires paid subscription."). The visible text names no primary source. Logged, not usable as a citation |
| S-30 | https://s25.q4cdn.com/621799436/files/doc_financials/2025/ar/2025-Form-10-K.pdf | Micron Technology, Inc. (Form 10-K, fiscal year ended August 28, 2025; company-hosted copy) | `company_filing` | both | fiscal year ended August 28, 2025; signed "October 3, 2025" | 2026-10-07T15:26Z | `4b50d54e91dae01c043a4be883157cd09348dd852d58a1d74384edf7ec551fe9` | 200 | kept; HBM at company level; names neither NVIDIA nor Amazon. Signature date is 4 days before 2025-10-07. Host: Micron's IR file host (s25.q4cdn.com, from search). Identity with SEC copy: not checked |
| S-31 | https://www.micron.com/products/memory/hbm/hbm3e | Micron | `company_marketing` (product page with FAQ) | both | undated; footer "©2023 Micron Technology, Inc." | 2026-10-07T15:26Z | `b96b23f4eade8e56d17ea851975bce2b63dfe54c00cf828048c2a57e348a775f` | 200 | kept; names the **H200**, not the H100 (see §3) |
| S-32 | https://investors.micron.com/news-releases/news-release-details/micron-commences-volume-production-industry-leading-hbm3e | Micron (IR newsroom) | would be `company_press_release` | Q-H100 (Micron) | not read | 2026-10-07T15:26Z | `2eee75c3221db700c152f49d9310f20bfecfe74e3f35b8bf3dbca768c37dded5` (challenge page) | 403 | **access gap**: Cloudflare challenge page ("Just a moment...") |
| S-33 | https://investors.micron.com/financials/annual-reports/default.aspx | Micron (IR) | none | — | — | 2026-10-07T15:26Z | `ed05233cd9f7d66f9247dd5b552b06c19eeff1f76cb80bc08374d6f7e61d8188` (challenge page) | 403 | **access gap**: same Cloudflare challenge |
| S-34 | https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2025_4Q_Interim_Report.pdf | Samsung Electronics Co., Ltd. ("2025 Business Report", English; 358 pp.) | `company_filing` (proposed; it is Samsung's business report for the year, which refers to DART disclosure; the statute is not stated on the cover, so §3's test is not fully met — Verifier to confirm) | both | "2025 Business Report / For the year ended December 31, 2025"; PDF metadata created 2026-04-21 | 2026-10-07T15:27Z | `626dd527bb25dc1ffd7ce72d84a0ded10f4d8f3daa0352d6c6b6be07c3eae73a` | 200 | kept; company-level HBM statements; NVIDIA and Amazon not named as customers |
| S-35 | https://semiconductor.samsung.com/dram/hbm/hbm3-icebolt/ (→ https://semiconductor.samsung.com/dram/hbm/hbm3/) | Samsung Electronics | `company_marketing` | both | undated; "Copyright© Samsung" | 2026-10-07T15:27Z | `a0afc0c91119b2cbbdf0242db37a92b54a2612a97ce43e9fd698ac218225fd91` | 200 | kept; names no customer product ("Amazon" appears only in a cookie/CDN list) |
| S-36 | https://semiconductor.samsung.com/dram/hbm/hbm3e-shinebolt/ (→ https://semiconductor.samsung.com/dram/hbm/hbm3e/) | Samsung Electronics | `company_marketing` | both | undated | 2026-10-07T15:27Z | `0ae218dd62a160f9a2f185c0a8a11bc82b0bd35fcaf623c0d1a95a3cf4cbbef2` | 200 | kept; names no customer product |
| S-37 | https://www.samsung.com/global/ir/reports-disclosures/business-report/ | Samsung Electronics (IR listing) | none | — | — | 2026-10-07T15:27Z | `7c3e9953dcf013511e756d4465715b0e720d1397699f919359ca248b2b3a37dc` | 200 | navigation page only; not read as a source |
| S-38 | https://nvidianews.nvidia.com/news/sk-hynix-ai-factory | NVIDIA (newsroom) | `company_press_release` | Q-H100 | "June 7, 2026" | 2026-10-07T15:27Z | `24dc20277c37eb669692fbec93ba9421aa7b2cd8af33f79a8390630a4b74f95f` | 200 | kept; company-level "memory" statements naming SK hynix; no H100 |
| S-39 | https://nvidianews.nvidia.com/news/sk-group-and-nvidia-expand-strategic-partnership-across-ai-factories-and-next-generation-memory | NVIDIA (newsroom; joint release with SK) | `company_press_release` | Q-H100 | "July 24, 2026" | 2026-10-07T15:27Z | `5ce077f03758f793c8a29f064a43396a4edd7dec5f16d0f93ea676d82ae2e114` | 200 | kept; HBM partnership and Vera Rubin with SK hynix HBM4 (another product); no H100 |
| S-40 | https://nvidianews.nvidia.com/news/sk-group-ai-factory | NVIDIA (newsroom) | `company_press_release` | Q-H100 | "October 30, 2025" | 2026-10-07T15:27Z | `1610048ac575c7525a1815252b1fac3b7ec292fcc5f36cdf12fdab42d7bd35b8` | 200 | kept; company-level HBM development statement; no H100 |
| S-41 | https://nvidianews.nvidia.com/news/samsung-ai-factory | NVIDIA (newsroom) | `company_press_release` | Q-H100 | "October 30, 2025" | 2026-10-07T15:27Z | `3e597a97fcf3feda05be3685f5d6f29fcf1449bd9be47036bd5c6fd827d088fc` | 200 | kept; company-level HBM3E/HBM4 supply statement naming Samsung; no H100 |
| S-42 | https://news.samsung.com/global/samsung-unveils-hbm4e-showcasing-comprehensive-ai-solutions-nvidia-partnership-and-vision-at-nvidia-gtc-2026 | Samsung Electronics (newsroom) | would be `company_press_release` | Q-H100 (Samsung) | not read | 2026-10-07T15:27Z and retry 15:28Z | none (no bytes) | no response: `curl: (52) Empty reply from server`, twice; `https://news.samsung.com/global/` also returned an empty reply | **access gap**: Samsung global newsroom. Proxy status showed no relay failures, so the cause is not known |
| S-43 | https://news.skhynix.com/en/skhynix-nvidia-partnership-2026/ | SK hynix (newsroom; same announcement as S-39) | `company_press_release` | Q-H100 | "July 25, 2026" ("Seoul, July 25, 2026") | 2026-10-07T15:28Z | `6721d73f4e8c48a340da2312518b12677e73821e0d6448c75c1ae65c2653131c` | 200 | kept; same content as S-39 from the other party; no H100 |
| S-44 | https://press.aboutamazon.com/2024/12/aws-trainium2-instances-now-generally-available | Amazon (US Press Center, Business Wire) | `company_press_release` | Q-TRN2 | "December 03, 2024" | 2026-10-07T15:28Z | `ae6b595a1be59a81283efad26f4da3eb6cfd67dde751e1c289087daa4fd05c21` | 200 | kept; Trainium2 named, no memory maker, no HBM named |
| S-45 | https://press.aboutamazon.com/2023/11/aws-unveils-next-generation-aws-designed-chips | Amazon (US Press Center, Business Wire) | `company_press_release` | Q-TRN2 | "November 28, 2023" | 2026-10-07T15:28Z | `6a6c3fe30012dc67d0a3724e70d781e7021e8d32a3f585d6d946a6aa8e533ef3` | 200 | kept; "memory capacity" only, no memory maker |
| S-46 | https://nvidianews.nvidia.com/news/nvidia-hopper-in-full-production | NVIDIA (newsroom) | `company_press_release` | Q-H100 | "September 20, 2022" | 2026-10-07T15:28Z | `ed31ac3395522e6cea2e14978a1d13cf9c50da3e3d9b5e84265af8ad73088afe` | 200 | kept; H100 named, no memory maker (names AWS only as a cloud deploying H100) |
| S-47 | https://nvidianews.nvidia.com/news/nvidia-announces-hopper-architecture-the-next-generation-of-accelerated-computing | NVIDIA (newsroom) | `company_press_release` | Q-H100 | "March 22, 2022" | 2026-10-07T15:28Z | `5d916c78e256f9d6b535b88a3c45377604dd1064dc81fa080815d77c7eed3c14` | 200 | kept; H100 named, no memory maker |
| S-48 | https://investors.micron.com/news-releases/news-release-details/micron-high-volume-production-hbm4-designed-nvidia-vera-rubin | Micron (IR newsroom) | would be `company_press_release` | Q-H100 (Micron) | not read | 2026-10-07T15:30Z | `0128235ecf120f7f5d07340998fa091b11735d92ea77bd7fd137f91ba7ddce9e` (challenge page) | 403 | **access gap**: Cloudflare challenge. The title (from search) concerns Vera Rubin, not the H100 |
| S-49 | https://s25.q4cdn.com/621799436/files/doc_financials/2026/q3/0000723125-26-000015.pdf | Micron (Form 10-Q, quarter ended May 28, 2026; company-hosted copy) | `company_filing` | both | "For the quarterly period ended May 28, 2026" | 2026-10-07T15:30Z | `79ef98b3cdc1ffc608b02635ef1fa5e9ed07298bf24f7bb717b03a06bda5e2cd` | 200 | kept; HBM at company level; names neither NVIDIA nor Amazon |
| S-50 | https://s25.q4cdn.com/621799436/files/doc_financials/2026/q4/Q4-FY26-Prepared-Remarks.pdf | Micron ("Fiscal Q4 2026 Earnings Call Prepared Remarks") | `company_press_release` (proposed: an earnings-call script; no statute stated) | both | no calendar date printed; refers to "fiscal fourth-quarter (Q4) 2026" | 2026-10-07T15:30Z | `2821d4ccaae50b40dcd28cd4e766c69c509e73d666e4109d5907c7205a03b700` | 200 | kept; names NVIDIA for a custom HBM4E on next-generation GPUs (another product); no H100, no Amazon |
| S-51 | https://newsletter.semianalysis.com/p/amazons-ai-self-sufficiency-trainium2-architecture-networking | SemiAnalysis | `market_research_consultancy` (pointer only) | not a party | "Dec 03, 2024" | 2026-10-07T15:30Z | `7c184e85df1feb2f1b4704a588309cb9209c18490bf778b60c63dc3a7f3b317e` | 200 | **pointer; partly paywalled** ("This post is for paid subscribers"). The free part names no memory maker and no primary source for one |

### 2.2 Considered but not retrieved

| URL | Publisher | Class it would have | Found by | Why not retrieved |
|---|---|---|---|---|
| https://www.sec.gov/Archives/edgar/data/0002120882/000119312526299963/d32785d424b4.htm and the related F-1, F-1/A, DRS, DRS/A, F-6 and 8-A12B filings of SK hynix Inc. (2026) | SK hynix, filed with the SEC | `company_filing` | Q10, Q15, Q16, Q23 | **dropped: SEC EDGAR is not used (D-042).** Q16 looked for a copy hosted by SK hynix and found none. This is an access gap for SK hynix's most detailed English-language filing |
| https://www.sec.gov/Archives/edgar/data/723125/000072312525000028/mu-20250828.htm (and exhibits); Micron 8-K exhibits on sec.gov | Micron, filed with the SEC | `company_filing` | Q19, Q26 | dropped: SEC EDGAR is not used; the company-hosted 10-K was retrieved instead (S-30) |
| https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/… | Amazon, filed with the SEC | `company_filing` | Q9 | dropped: SEC EDGAR; the company-hosted copy was retrieved instead (S-19) |
| pny.com, openzeka.com, cisco (bxin.cisco.com), microway.com, MEGWARE.com, gpusolutions.hrp.hu, lenovopress.lenovo.com, uvation.com copies of the H100 datasheet | resellers and system makers | none (copies of unknown provenance) | Q1 | dropped: not NVIDIA-hosted; NVIDIA's own copies were retrieved (S-08, S-11) |
| https://images.nvidia.cn/aem-dam/en-zz/Solutions/data-center/h100/nvidia-h100-datasheet-nvidia-a4-2287922-r7-zhCN.pdf | NVIDIA (China) | `company_technical_documentation` | Q1 | dropped: Chinese-language edition of the datasheet; the English current edition was retrieved (S-11) |
| Wikipedia, techpowerup, pcgameshardware, computerbase, hwcooling, club386, hpctech.co.jp, episteme.tllm.fr | encyclopedias and news | `news_media` / none | Q2 | dropped: not primary; they name no primary source for a memory supplier that was not already searched |
| https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/nvidia-dgx-h100-datasheet.pdf | NVIDIA | `company_technical_documentation` | Q3 | not retrieved: a system (DGX) datasheet, not the H100 GPU's; **not searched** for a memory maker |
| https://images.nvidia.com/aem-dam/Solutions/documents/HGX-H100-PCF-Summary.pdf | NVIDIA | `company_technical_documentation` | Q3 | not retrieved: product carbon footprint summary for HGX H100; **not searched** (it could in principle list component origins; unread) |
| https://nvidianews.nvidia.com/_gallery/download_pdf/… (PDF copies of S-47 and S-39) | NVIDIA | `company_press_release` | Q4, Q23 | not retrieved: PDF copies of releases already retrieved as HTML |
| https://developer.nvidia.com/blog/nvidia-grace-hopper-superchip-architecture-in-depth/ and Grace Hopper whitepapers | NVIDIA | `company_technical_documentation` | Q4 | not retrieved: about Grace Hopper (GH200), not the H100 |
| https://awsdocs-neuron.readthedocs-hosted.com/en/v2.xx/… (older Neuron versions and `_sources/*.rst`) | Amazon/AWS | `company_technical_documentation` | Q6 | not retrieved: older versions of S-12/S-13; the `latest` edition was retrieved |
| https://aws.amazon.com/ec2/ultraservers/, https://aws.amazon.com/ec2/instance-types/accelerated-computing/ | Amazon/AWS | `company_marketing` | Q7 | **not retrieved** (time); not searched for a memory maker |
| https://s2.q4cdn.com/299287126/files/doc_financials/2025/ar/Amazon-2024-Annual-Report.pdf; Amazon webslides Q1/Q3 2025 | Amazon | `company_filing` / none | Q9 | not retrieved: older edition superseded by S-19; slides not a filing |
| https://ir.aboutamazon.com/sec-filings/sec-filings-details/default.aspx?FilingId=18165478 | Amazon IR | — | Q9 | not retrieved: index page; S-19 already holds the 10-K |
| fxbaogao.com, seekingalpha.com, annualreports.com/.co.uk, bullfincher.io, qz.com, stockanalysis.com, financialfilings.com, technode.global, digitimes (FY25 results), taiwannews, startuprecipe, longtermwiki | aggregators and news | none / `news_media` | Q8, Q11 | dropped: aggregator copies or news; not primary |
| https://news.skhynix.com/… other hits (HBM3E development and volume production, 12-layer HBM3, HBM4, SC25, OCP 2025, CES 2026, TSMC symposium, "5 things", "HBM to eSSD", SK AI Summit, quarterly results 2024–2026, AGM) | SK hynix | `company_press_release` / `company_marketing` | Q12, Q13, Q17, Q25 | **not retrieved** (time). Their search titles do not name the H100 or Trainium2; a product-level statement inside them cannot be ruled out without reading them |
| https://news.skhynix.com/en/q2-2026-business-results/ | SK hynix | `company_press_release` | Q12 | **not retrieved** (most recent results release; not read) |
| https://www.tomshardware.com/…, https://www.trendforce.com/presscenter/…, datawrapper chart, longportapp.cn, design-reuse.com, tweaktown.com, vnreview.vn | news, market research | `news_media`, `market_research_consultancy` | Q18 | dropped: not primary; the search results did not show any of them naming a primary source for Trainium2's HBM supplier (titles only; not read) |
| benzinga.com, indmoney.com, ibtimes.co.uk, itiger.com, convergedigest.com, igorslab.de, communicationstoday.co.in | news | `news_media` | Q15 | dropped: news about SK hynix's US listing; the primary source they point to is the SEC filing, which is out of bounds (D-042) |
| https://www.micron.com/about/blog/… (HBM3E blog, GTC 2024 takeaways, MGX storage), in.micron.com / sg.micron.com / my.micron.com copies, assets.micron.com "memory-centric data center" PDF, prd.micron.com | Micron | `company_marketing` | Q20, Q26 | **not retrieved** (time); blogs and regional copies |
| https://images.samsung.com/…/2025_con_quarter04_all.pdf, earnings presentations 1Q/3Q/4Q 2025, Samsung IR financial-statement pages | Samsung | `company_filing` / none | Q21 | not retrieved: financial statements and slides; the full business report (S-34) was retrieved |
| https://semiconductor.samsung.com/dram/hbm/hbm3e-shinebolt/khbb84a03b-mc1j/, semiconductor.samsung.com tech-blog and news pages (Memory Tech Day 2023, HBM3E editorials), semiconductor.samsung.com/us/dram/hbm/ | Samsung | `company_technical_documentation` / `company_marketing` | Q22 | **not retrieved** (time). Titles do not name the H100 or Trainium2 |
| https://news.samsung.com/global/tag/nvidia; https://news.samsung.com/global/samsung-electronics-and-broadcom-expand-strategic-collaboration-… | Samsung newsroom | `company_press_release` | Q24 | not retrieved: same host as S-42, which returned empty replies |
| https://nvidianews.nvidia.com/news/nvidia-hpc-platform-hopper-quantum-2-worldwide-adoption; https://nvidianews.nvidia.com/news/nvidia-hopper-gpus-expand-reach-as-demand-for-ai-grows | NVIDIA | `company_press_release` | Q24 | **not retrieved** (time); 2022–2023 H100 releases |
| https://investors.micron.com/news-releases/news-release-details/micron-ships-hbm4-key-customers-power-next-gen-ai-platforms | Micron | `company_press_release` | Q25 | not retrieved: same host as S-32/S-33/S-48 (403 challenge) |
| https://www.sec.gov/…/a2026q3ex991-pressrelease.htm | Micron, via SEC | `company_press_release` | Q26 | dropped: SEC EDGAR |
| newsletter.semianalysis.com (Trainium specs, Trainium3 pages), introl.com, uncoveralpha.com, aws.amazon.com/pt/… | analysts, blogs, AWS (Portuguese) | `market_research_consultancy`, `news_media`, `company_marketing` | Q28 | dropped except S-51 (one pointer read to see whether it names a primary source) |

---

## 3. Anchors found in the retrieved sources

Verbatim, from the locally extracted text. Locators: PDF page numbers are the physical page in the PDF
file (counted from 1), not the printed folio, unless "printed" is said. "Product-level" means the
sentence names a specific product; "company-level" means it speaks of the company's suppliers or
partners in general. "HBM" vs "memory" is recorded as worded.

### Q-H100: statements that name a memory maker

| S-id | Locator | Anchor (verbatim) | Level | Product | Item as worded | Note |
|---|---|---|---|---|---|---|
| S-20 | "News Highlights", 2nd bullet | "HBM3 to be combined with NVIDIA H100 Tensor Core GPU for accelerated computing" | product-level | H100 | HBM3 | SK hynix speaking about its own HBM3 and NVIDIA's H100; dated June 8, 2022; worded as a future arrangement |
| S-20 | body, paragraph beginning "NVIDIA has recently completed its performance evaluation" | "SK hynix will provide HBM3 for NVIDIA systems expected to ship starting in the third quarter of this year." | company/system-level ("NVIDIA systems") | none named in this sentence | HBM3 | forward-looking as worded (2022) |
| S-20 | body, paragraph beginning "The highly anticipated NVIDIA H100" | "The highly anticipated NVIDIA H100 is the world's largest and most powerful accelerator. SK hynix's HBM3 is expected to enhance accelerated computing performance…" | product-level (H100 named in the paragraph) | H100 | HBM3 | "expected to" (forward-looking); the first sentence is SK hynix describing NVIDIA's product (superlative) |
| S-20 | page header block labelled "AI Summary" | "The chip will power NVIDIA's H100 GPUs…" | — | H100 | "chip" (HBM3) | an automatically generated page summary, not part of the release text; listed so it is not mistaken for an anchor |
| S-18 | PDF p.8, Item 1 Business, "Manufacturing" | "We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung." | company-level | none | memory | NVIDIA 10-K; the same anchor as S05-R1 p.8 |
| S-38 | body, quote of Jensen Huang (paragraph beginning "“AI factories are the engines…") | "SK hynix has been an extraordinary partner to NVIDIA, playing a central role in delivering advanced memory technologies for NVIDIA AI computing platforms." | company-level | none | "advanced memory technologies" | June 7, 2026 |
| S-38 | body, paragraph beginning "The multiyear agreement supports supply…" | "The multiyear agreement supports supply to address the extended development cycles of advanced memory." | company-level | names Vera Rubin, Vera CPUs, RTX Spark PCs, Jetson Thor later in the paragraph (other products) | "advanced memory" | forward-looking |
| S-40 | summary bullet under the headline | "SK Group and NVIDIA are deepening their partnership to advance SK hynix HBM and future memory solutions for NVIDIA GPUs, chip manufacturing and telecommunications." | company-level ("NVIDIA GPUs") | none | HBM | October 30, 2025; development collaboration, not a supply statement |
| S-40 | body, paragraph beginning "Further expanding the NVIDIA and SK Group partnership" | "…the companies are collaborating on the development of SK hynix high-bandwidth memory (HBM) and next-generation advanced memory solutions for NVIDIA GPUs…" | company-level | none | HBM | October 30, 2025 |
| S-41 | body, paragraph after Jay Y. Lee's quote, beginning "From their first collaboration on NVIDIA's first graphics card NV1…" | "…introducing the industry's first commercial HBM, and a key supply collaboration for HBM3E and HBM4 today…" | company-level | none | HBM3E and HBM4 (the H100 uses HBM3/HBM2e per S-02, S-03, S-07) | October 30, 2025; NVIDIA release about Samsung; "industry's first" is a superlative |
| S-39 / S-43 | S-39 summary bullet; S-43 "▪" bullet | S-39: "NVIDIA and SK hynix establish long-term partnership to secure and codevelop next-generation AI memory, including HBM." | company-level | none | HBM | July 24, 2026 (NVIDIA) / July 25, 2026 (SK hynix) |
| S-39 | body, paragraph on SK Telecom's AI cloud | "…deploy NVIDIA Vera Rubin accelerated computing powered by SK hynix HBM4…" | product-level, **other product** | Vera Rubin (not H100) | HBM4 | does not concern the H100 (ER-9 flag: other product) |
| S-31 | FAQ, "When will Micron's HBM3E be available?" | "Micron HBM3E 24GB 8-high will ship in NVIDIA H200 Tensor Core GPUs starting in the second calendar quarter 2024." | product-level, **other product** | H200 (not H100) | HBM3E | undated page; the same page's footnotes 4–6 cite the H100 only as a comparison platform ("as compared to the current shipping platform (H100)") |
| S-50 | PDF p.4, paragraph beginning "In HBM, our revenue in fiscal Q4 2026…" | "…proud to be working with NVIDIA on the industry's first custom-HBM4E implementation, NVHBM, to be adopted on next generation of GPUs and NVLink Fusion platforms." | product-level, **other product** | unnamed "next generation of GPUs" (not H100) | HBM4E | fiscal Q4 2026; forward-looking |

### Q-H100: NVIDIA's own H100 documents (row 1): HBM named, memory maker not named

| S-id | Locator | Anchor (verbatim) | Note |
|---|---|---|---|
| S-07 | PDF p.36, "H100 HBM3 and HBM2e DRAM Subsystems" | "The H100 SXM5 GPU raises the bar considerably by supporting 80 GB (five stacks) of fast HBM3 memory…" | whitepaper V1.04; the only manufacturer named in the spec table is "TSMC Manufacturing Process" (GPU die) |
| S-05 | section "H100 HBM3 and HBM2e DRAM subsystems" | "The H100 SXM5 GPU raises the bar considerably by supporting 80 GB (five stacks) of fast HBM3 memory…" | same text as S-07 |
| S-02 | PDF p.8, specification table | "Memory type HBM2e" | H100 PCIe |
| S-03 | PDF p.8, specification table | "Memory type HBM3" | H100 NVL |
| S-11 | PDF p.1 | "…the PCIe-based NVIDIA H100 NVL with NVLink bridge utilizes Transformer Engine, NVLink, and 188GB HBM3 memory…" | current datasheet; same sentence on S-01 |
| S-01, S-08, S-09, S-46, S-47 | whole text searched | no memory maker named (searched for "hynix", "Micron", "Samsung", "supplier") | S-02 PDF p.17 mentions "qualified suppliers of a power adapter" only |

### Q-TRN2: statements found

No retrieved source names a memory maker for Trainium2. What the AWS sources say about its memory:

| S-id | Locator | Anchor (verbatim) | Level | Item as worded |
|---|---|---|---|---|
| S-13 | "Trainium2 Architecture Guide for NKI", list after "The diagram below shows a block diagram of a Trainium2 device" | "4 HBM stacks with a total device memory capacity of 96GiB and bandwidth of 3TB/s." | product-level, no supplier | HBM |
| S-12 | "Trainium2 chip components" → "Device Memory"; table "Memory" | "96 GiB of device memory with 2.9 TB/sec of bandwidth."; table row "HBM Capacity (GiB) … 96" | product-level, no supplier | HBM |
| S-16 | AWS News Blog post body | "Each Trainium2 chip is home to eight NeuronCores and 96 GiB of High Bandwidth Memory (HBM)…" | product-level, no supplier | HBM |
| S-14 | "Features" → "Up to 6 TB HBM with 185 TBps bandwidth" | "Trn2 instances deliver 1.5 TB of accelerator memory with 46 TBps of total memory bandwidth." | instance-level, no supplier | HBM (heading), "accelerator memory" (text) |
| S-17 | body | "Trn2 instances feature 16 Trainium2 chips to deliver … 1.5 TB high bandwidth memory…" | instance-level, no supplier | high bandwidth memory |
| S-45 | body | "Trainium2 is designed to deliver up to 4x faster training performance and 3x more memory capacity compared to first generation Trainium chips…" | product-level, no supplier | memory |
| S-44 | whole text searched | no memory maker; no HBM sentence | — |
| S-15 | Trainium3 section | "144 GB HBM3e per chip, 4.9 TB/s bandwidth - 1.7x higher than Trainium2." | **other product** (Trainium3), no supplier | HBM3e |
| S-19 | PDF p.23, Item 1A Risk Factors, "Our Supplier Relationships Subject Us to a Number of Risks" | "…we rely on a limited group of suppliers for semiconductor products, including products related to artificial intelligence infrastructure such as graphics processing units." | company-level; no supplier named | "semiconductor products" (not memory, not HBM) |
| S-19 | PDF p.31 (and p.41), forward-looking statements / guidance | "…resource and supply volatility, including for memory chips…" | company-level; no supplier named | "memory chips" |
| S-19 | PDF p.5, shareholder letter (not part of the Form 10-K) | "…our custom AI silicon (Trainium2) had about 30% better price-performance than comparable GPUs, and has largely sold out." | product named; nothing on memory | — |
| S-28 | section "SK hynix's HBM3E Leadership to Extend to HBM4", 1st paragraph | "…Global Big Tech companies, including Google and AWS, are expanding their proprietary ASIC-based AI chip development and selecting HBM3E as the optimal solution." | company-level about AWS; SK hynix does not name itself as AWS's supplier here; the paragraph attributes the outlook to "experts" | HBM3E |
| S-29 | headline (visible text; body paywalled) | "Samsung and SK Hynix will both supply HBM3 for AWS Trainium 2" | `news_media`, pointer only; no primary source named in the visible text | HBM3 |
| S-51 | free section of the post | "Trn2 will use both HBM3 & HBM3e but all current SKUs have been set with to HBM3 speeds of 2.9TByte/s through firmware." | `market_research_consultancy`, pointer only; names no memory maker in the free part | HBM3 / HBM3e |

### Company-level statements by the HBM makers (both questions)

| S-id | Locator | Anchor (verbatim) | Note |
|---|---|---|---|
| S-30 | PDF p.9, Item 1 Business, "Cloud Memory Business Unit" | "CMBU is focused on memory solutions for large hyperscale cloud customers, and HBM for all data center customers." | Micron 10-K (signed October 3, 2025); no customer named |
| S-30 | PDF p.97, Note 28 "Certain Concentrations" | "Revenue from one customer was 17% (primarily included in the CMBU segment) of total revenue for 2025." | customer not named |
| S-49 | Form 10-Q, Part I | (searched) no NVIDIA, Amazon, H100 or Trainium | quarter ended May 28, 2026 |
| S-23 | body, DRAM paragraph | "In the DRAM segment, HBM revenue more than doubled year-on-year…" | SK hynix, January 28, 2026; no customer named |
| S-34 | PDF p.41, "Business condition" | "…we plan to actively address customer demand with the timely and expanded supply of competitive HBM4 targeting new GPU and ASIC markets within the AI sector." | Samsung 2025 Business Report; forward-looking; no customer named |
| S-34 | PDF p.29, "E. Major customers" | "In 2025, major customers (listed alphabetically) included Alphabet, Apple, Deutsche Telekom, Hong Kong Techtronics, and Supreme Electronics." | NVIDIA and Amazon are not in this list. (NVIDIA appears elsewhere, p.23, only as a supplier *to* Samsung's Harman unit; "AWS" appears only as "advanced wireless services" radio bands) |
| S-21, S-22, S-35, S-36 | whole text searched | no customer product named | HBM product pages of SK hynix and Samsung |

---

## 4. Summary per question (what was searched, not what it means)

### Q-H100 — who supplies the HBM in the NVIDIA H100

| Plan row | Status | Sources |
|---|---|---|
| 1 NVIDIA technical documentation | **searched**. Datasheets (two editions), two product briefs, the architecture whitepaper V1.04, the architecture blog post and the product page name HBM3/HBM2e but no memory maker | S-01, S-02, S-03, S-05, S-07, S-08, S-09, S-11 (S-04, S-10 navigation; S-06 dropped). Not read: DGX H100 datasheet, HGX H100 carbon-footprint summary |
| 2 Amazon/AWS technical documentation | not applicable: Amazon is not a party to the H100's supplier | — |
| 3 NVIDIA filing | **searched**: FY2026 Form 10-K, company-hosted. Company-level "memory" from SK Hynix, Micron and Samsung; H100 named only in export-control passages | S-18. **Not searched:** NVIDIA's 2026 Forms 10-Q (fiscal 2027 Q1 and Q2) |
| 4 Amazon filing | not applicable | — |
| 5 SK hynix | **technical/marketing pages searched** (no customer product). **Filings: access gap.** No English annual or business report was found on SK hynix's site; its IR document pages are empty JavaScript shells (S-24, S-26, S-27). SK hynix's 2026 F-1 / 424B4 prospectus appears in search results only on SEC EDGAR, which is out of bounds (D-042). Korean-language business report (DART) not searched (plan asks for English, company-hosted) | S-21, S-22, S-23; gaps S-24, S-26, S-27, SEC-only filings |
| 6 Micron | **searched**: FY2025 10-K (signed 2025-10-03), Q3 FY2026 10-Q, HBM3E product page. None names the H100; the product page names the **H200**. **Access gap:** investors.micron.com (press releases, annual-reports page) returns a 403 Cloudflare challenge. Micron's FY2026 10-K was not found on a company host | S-30, S-49, S-31, S-50; gaps S-32, S-33, S-48 |
| 7 Samsung | **searched**: 2025 Business Report (English), HBM3 and HBM3E product pages. None names the H100 or NVIDIA as a customer | S-34, S-35, S-36 |
| 8 press releases | **searched**: NVIDIA newsroom (S-38, S-39, S-40, S-41, S-46, S-47), SK hynix newsroom (S-20, S-23, S-43). **Only S-20 (SK hynix, June 8, 2022) names the H100 together with the supplier's HBM.** The 2025–2026 NVIDIA releases name SK hynix (HBM, "advanced memory") and Samsung (HBM3E, HBM4) at company level or for other products (Vera Rubin). **Access gaps:** Micron's IR newsroom (403), Samsung's global newsroom news.samsung.com (empty reply, S-42). Not retrieved: several SK hynix newsroom items and two older NVIDIA H100 releases (titles do not name an HBM maker) | see §2 |

### Q-TRN2 — who supplies the HBM in AWS Trainium2

| Plan row | Status | Sources |
|---|---|---|
| 1 NVIDIA technical documentation | not applicable: NVIDIA is not a party to Trainium2's supplier | — |
| 2 Amazon/AWS technical documentation | **searched**: both Neuron architecture pages, the Trn2 instance page, the Trainium page, the launch blog post, What's New. They name HBM (4 stacks, 96 GiB) but no memory maker | S-12, S-13, S-14, S-15, S-16, S-17. Not read: EC2 UltraServers page, accelerated-computing instance page |
| 3 NVIDIA filing | not applicable | — |
| 4 Amazon filing | **searched**: 2025 Annual Report containing the Form 10-K, company-hosted. No memory maker named; company-level "limited group of suppliers for semiconductor products" and "memory chips" supply volatility | S-19. **Not searched:** Amazon's 2026 Forms 10-Q |
| 5 SK hynix | **searched** (product pages, results release, outlook feature): Trainium not named; S-28 says AWS is selecting HBM3E in general without naming a supplier. **Filings: access gap** as for Q-H100 | S-21, S-22, S-23, S-28; gaps as above |
| 6 Micron | **searched**: 10-K, 10-Q, product page, Q4 FY2026 remarks: Amazon and Trainium not named. **Access gap:** investors.micron.com | S-30, S-31, S-49, S-50; gaps S-32, S-33, S-48 |
| 7 Samsung | **searched**: 2025 Business Report, HBM product pages: Amazon and Trainium not named | S-34, S-35, S-36 |
| 8 press releases | **searched**: Amazon press center (S-44 GA, S-45 announcement), AWS announcements (S-16, S-17), SK hynix newsroom (search Q17, Q25; no Trainium release found). **Access gaps:** Micron IR newsroom, Samsung global newsroom. No release naming Trainium2 together with a supplier's HBM was found | see §2 |
| pointers | DIGITIMES (S-29, Dec 7, 2023) headline says Samsung and SK Hynix "will both supply HBM3 for AWS Trainium 2"; body paywalled, names no primary source in the visible text. SemiAnalysis (S-51, Dec 3, 2024) free part names no supplier; rest paywalled. Neither led to a primary source that could be retrieved | S-29, S-51 |

### Rows or items not searched, stated plainly

- NVIDIA's and Amazon's 2026 quarterly reports (Forms 10-Q).
- SK hynix's Korean-language business report on DART, and any English annual report SK hynix may publish
  elsewhere than its IR pages (none found by Q11, Q12, Q14).
- Micron's FY2026 Form 10-K (not found on a company host on 2026-10-07).
- Samsung's semiconductor newsroom (`semiconductor.samsung.com/news-events/…`) was reached only through
  searches Q22 and Q24, not browsed; its pages that the searches returned were not retrieved.
- Several SK hynix newsroom items, Micron blog posts, two older NVIDIA H100 releases, the DGX H100 datasheet,
  the HGX H100 carbon-footprint summary and two AWS instance pages were found but not retrieved (§2.2).
  Their titles do not name the H100 or Trainium2 with an HBM maker, but their text was not read.
- AWS conference material (re:Invent or Hot Chips slides) about Trainium2: Q28 returned none hosted by AWS.
