# Source register — S01 domain map

**Status:** FROZEN (S06, 2026-09-30; D-050, proposed): migrated into [`data/sources.json`](../../data/sources.json) as `src-NNN`; kept as history · **Session:** S01 · **Accessed:** 2026-09-29
**Used by:** [`domain-map.md`](./domain-map.md)

> **One home / lifecycle.** This register is a *research-staging* artifact, not canonical
> data. S06 (evidence/claim system) migrates these rows into canonical source records;
> after that migration this file is **frozen** and kept as history. Do not add
> canonical sources here after S06.

## How to read this register

- **Fields** follow MA §5.3 (`id`, `publisher`, `title`, `url`, `publication_date`,
  `source_type`, `source_tier`, `accessed_at`) plus `locators_used` (S01 prompt Part B
  §11) and `content_sha256` (first 12 hex characters of the SHA-256 of the bytes
  retrieved, so a later session can tell whether a page has changed since S01).
- **Retrieval.** Every row was retrieved in full over HTTPS with `curl` on the access
  date and read from the retrieved text (PDF text extracted locally). No row is a
  search-results page or snippet. Web search was used only to discover URLs.
- **Locators.** For PDFs, `p.N` is the **PDF page index** (the Nth page as a PDF viewer
  shows it), not the printed page number. For HTML pages, the locator is the
  section heading or the quoted sentence, because live pages have no stable page
  numbers.
- **`publication_date`.** As stated by the source. `undated (live page)` means the page
  shows no publication or revision date; for these rows, `accessed_at` is the only
  temporal anchor. `modified` dates are the page's own metadata.
- **`source_tier` (provisional).** Uses the order in the S01 prompt Part B §05, until the
  S05 source policy replaces it:
  `T1` official company documentation / filings · `T2` standards bodies and technical
  specifications · `T3` government / intergovernmental reports · `T4` peer-reviewed or
  reputable academic/technical research · `T5` high-quality secondary analysis ·
  `T6` news/media.
- **Tier caveat.** A T1 company source is primary evidence only for statements about
  that company's own products and processes. Comparative or superlative self-claims
  ("unique to", "world's first", "leader") are recorded in the map as `ATTRIBUTION`,
  never as `FACT`.

## Register

| id | publisher | title | url | publication_date | source_type | source_tier | accessed_at | content_sha256 | locators_used |
|---|---|---|---|---|---|---|---|---|---|
| SRC-001 | National Institute of Standards and Technology (NIST) — P. Mell, T. Grance | The NIST Definition of Cloud Computing (Special Publication 800-145) | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf | 2011-09 | government publication (definitional) | T3 | 2026-09-29T13:25Z | `7b0c1a9fdfc6` | p.6 (§2 definition; essential characteristics; footnote 2), p.7 (IaaS; deployment models) |
| SRC-002 | Center for Security and Emerging Technology (CSET), Georgetown University — S. M. Khan, D. Peterson, A. Mann | The Semiconductor Supply Chain: Assessing National Competitiveness (Issue Brief) | https://cset.georgetown.edu/wp-content/uploads/The-Semiconductor-Supply-Chain-Issue-Brief-1.pdf | 2021-01 | research report (policy-oriented; not peer-reviewed) | T4 (provisional — see note 1) | 2026-09-29T13:25Z | `319d942ba534` | p.3, p.5, p.6, p.7, p.19, p.23, p.24 (Table 6), p.25, p.30, p.45, p.50, p.65–67 (Appendix B glossary) |
| SRC-003 | Center for Security and Emerging Technology (CSET), Georgetown University — S. M. Khan, A. Mann | AI Chips: What They Are and Why They Matter (Issue Brief) | https://cset.georgetown.edu/wp-content/uploads/AI-Chips—What-They-Are-and-Why-They-Matter-1.pdf | 2020-04 | research report (policy-oriented; not peer-reviewed) | T4 (provisional — see note 1) | 2026-09-29T13:25Z | `0f80b4fa1650` | p.4 (footnote * definition of "AI chips"), p.20 ("AI Chip Types") |
| SRC-004 | NIST — CHIPS Research and Development Office | The Vision for the National Advanced Packaging Manufacturing Program | https://www.nist.gov/system/files/documents/2023/11/19/NAPMP-Vision-Paper-20231120.pdf | 2023-11-20 | government programme document | T3 | 2026-09-29T13:26Z | `bb83ae40b640` | p.4 ("Opportunities in advanced packaging"), p.5 (U.S. strengths; design tools; equipment), p.6 (materials and substrates; power delivery and thermal), p.7 (chiplet ecosystem) |
| SRC-005 | Semiconductor Industry Association (SIA) and Boston Consulting Group (BCG) — R. Varadarajan et al. | Emerging Resilience in the Semiconductor Supply Chain | https://www.semiconductors.org/wp-content/uploads/2024/05/Report_Emerging-Resilience-in-the-Semiconductor-Supply-Chain.pdf | 2024-05 | industry association / consultancy report | T5 (see note 2) | 2026-09-29T13:29Z | `27040f69e8e0` | p.6, p.21 (sidebar "Chiplets"), p.30 |
| SRC-006 | NVIDIA (NVIDIA Technical Blog) | NVIDIA Hopper Architecture In-Depth | https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/ | 2022-03-22 (modified 2025-07-22) | company technical documentation | T1 | 2026-09-29T13:26Z | `ed8dc6f2a694` | "H100 GPU hardware architecture in-depth" (TSMC 4N sentence; SXM5 unit list); "H100 HBM3 and HBM2e DRAM subsystems"; introduction ("world's first GPU with HBM3") |
| SRC-007 | NVIDIA | NVIDIA Blackwell Architecture (product technology page) | https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/ | undated (live page) | company product documentation | T1 | 2026-09-29T13:29Z | `66b30443aaba` | "A New Class of AI Superchip" paragraph (TSMC 4NP; two reticle-limited dies); GB200 NVL72 paragraph (rack-scale, liquid-cooled) |
| SRC-008 | Google Cloud | Introduction to Cloud TPU | https://docs.cloud.google.com/tpu/docs/intro-to-tpu | last updated 2026-09-24 | company technical documentation | T1 | 2026-09-29T13:26Z | `4e8ea7a6e8fb` | opening definition paragraph; "How to use TPUs" paragraph |
| SRC-009 | Google Cloud | TPU architecture | https://docs.cloud.google.com/tpu/docs/system-architecture-tpu-vm | last updated 2026-09-24 | company technical documentation | T1 | 2026-09-29T13:26Z | `e8db2f579437` | "TPU chip" and "TPU Pod" / "Slices" definitions |
| SRC-010 | Amazon Web Services (AWS Neuron documentation) | Trainium2 Architecture | https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html | undated (live page) | company technical documentation | T1 | 2026-09-29T13:29Z | `9afd23f3a56d` | opening paragraph; "Device Memory" line |
| SRC-011 | SK hynix Newsroom | [We Do Future Technology] Become a Semiconductor Expert with SK hynix – HBM | https://news.skhynix.com/en/become-a-semiconductor-expert-with-sk-hynix-hbm/ | 2023-05-02 | company explanatory article | T1 | 2026-09-29T13:26Z | `59489adb6035` | opening paragraph and TSV footnote; "1,024 DQs" paragraph; closing paragraph (HBM3 generation) |
| SRC-012 | SK hynix Newsroom | Creating New Values in DRAM Using Through-Silicon-Via Technology for Continued Scaling in Memory System Performance and Capacity | https://news.skhynix.com/en/creating-new-values-in-dram-using-through-silicon-via-technology-for-continued-scaling-in-memory-system-performance-and-capacity/ | 2019-11-20 | company technical article | T1 | 2026-09-29T13:26Z | `2b75c7f7cdd3` | TSV paragraph; HBM "in-package memory" paragraph; bandwidth-gap paragraph |
| SRC-013 | SK hynix Newsroom | Semiconductor Back-end Process 4: Packages, Part 2 | https://news.skhynix.com/semiconductor-back-end-process-episode-4-packages-part-2/ | 2023-06-27 | company explanatory article | T1 | 2026-09-29T13:26Z | `855179c796fa` | TSV section ("classified as a wafer-level package technology"); HBM paragraph and footnotes (interposer, 2.5D package); SiP vs SoC section; chiplets paragraph |
| SRC-014 | SK hynix Newsroom | SK hynix Partners with TSMC to Strengthen HBM Technological Leadership | https://news.skhynix.com/en/sk-hynix-partners-with-tsmc-to-strengthen-hbm-technological-leadership/ | 2024-04-19 | company press release | T1 | 2026-09-29T13:30Z | `181722d106d0` | base-die paragraph and TSV footnote; HBM4 base-die paragraph; CoWoS footnote |
| SRC-015 | Micron Technology | High-bandwidth memory (HBM) (product page) | https://www.micron.com/products/memory/hbm | undated (live page) | company product documentation | T1 | 2026-09-29T13:29Z | `7846bb06c806` | introductory definition paragraph |
| SRC-016 | Amkor Technology | 2.5D/3D TSV Packaging | https://amkor.com/technology/25d-3d-tsv/ | 2017-11-21 (modified 2025-07-31) | company technology page (OSAT) | T1 | 2026-09-29T13:27Z | `4655a423e3b4` | TSV paragraph ("does NOT provide TSV formation in foundry wafers"); MEOL paragraph |
| SRC-017 | ASML | EUV lithography systems (product page) | https://www.asml.com/en/products/euv-lithography-systems | undated (live page) | company product documentation | T1 | 2026-09-29T13:27Z | `ec896b9cb6bc` | opening ("unique to ASML"; 13.5 nm); "node" paragraph; EUV/DUV layers paragraph; NXE paragraph |
| SRC-018 | Synopsys | What is Electronic Design Automation (EDA)? (glossary) | https://www.synopsys.com/glossary/what-is-electronic-design-automation.html | modified 2025-09-09 | company explanatory documentation | T1 | 2026-09-29T13:27Z | `35ef0d04a255` | definition paragraph; DFM / mask synthesis paragraph; IP paragraph |
| SRC-019 | Lam Research | Our Processes | https://www.lamresearch.com/products/our-processes/ | 2017-08-02 (modified 2022-04-11) | company product documentation | T1 | 2026-09-29T13:30Z | `025e37a7b57b` | deposition paragraph (plating for TSV and wafer-level packaging); etch paragraph |
| SRC-020 | Amazon Web Services | AWS Regions and Availability Zones (user guide) | https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions-availability-zones.html | undated (live page) | company technical documentation | T1 | 2026-09-29T13:29Z | `1f172d6e220c` | Availability Zones definition sentence |
| SRC-021 | Lawrence Berkeley National Laboratory (LBNL) — S. J. Smith, A. Hubbard, A. Newkirk, M. Ganeshalingam, B. Holecek, D. Sartor, M. Mills, A. Shehabi | United States Data Center Energy Usage Report: 2025 Update (LBNL-2001758; DOI 10.71468/P1RP4F) | https://www.osti.gov/servlets/purl/3374245 | 2026-06-18 | government (national laboratory) technical report; marked peer reviewed on its eScholarship cover page | T3 | 2026-09-29T13:28Z | `1108b5a0f829` | p.6–7 (Glossary of Terms), p.12 (power capacity and interconnection), p.16–18 (§3.1 accelerator shipments), p.25 (§3.4.3), p.27 (§3.5 facility infrastructure) |
| SRC-022 | Lawrence Berkeley National Laboratory — A. Satchwell, N. Mims Frick, P. Cappers (with The Brattle Group and U.S. DOE) | Electricity Rate Designs for Large Loads: Evolving Practices and Opportunities (Technical Brief) | https://www.osti.gov/servlets/purl/2502077 | 2025-01 | government (national laboratory) technical brief | T3 | 2026-09-29T13:27Z | `bf8d49690b8d` | p.3 (utility tariffs), p.4 (tariff design objectives) |
| SRC-023 | Electric Power Research Institute (EPRI) | Powering Intelligence: Analyzing Artificial Intelligence and Data Center Energy Consumption (2024 White Paper) | https://restservice.epri.com/publicdownload/000000003002028905/0/Product | 2024-05 | independent non-profit research institute report | T4 | 2026-09-29T13:28Z | `c3870a8229ec` | p.2 (executive summary), p.5 (siting factors), p.6 (transmission lead times) |

### Notes

1. **CSET (SRC-002, SRC-003).** Georgetown University research centre; policy-oriented
   issue briefs, not peer-reviewed. Classed T4 provisionally for **definitions and
   process descriptions only**. Their market data are as of 2019 (SRC-002 p.5) and are
   **not** used in the map. S05 should confirm or downgrade to T5.
2. **SIA/BCG (SRC-005).** An industry association with a stated advocacy role (its own
   "About SIA", p.2) and a consultancy. Used only for attributed definitions and
   characterisations, never for unattributed facts.
3. **Company pages without dates** (SRC-007, SRC-010, SRC-015, SRC-017, SRC-020) are live
   pages that can change without notice. The `content_sha256` records what S01 read.

## Retrieved but not cited

Retrieved and read in S01 but not cited in the map, because a cited source already
covered the point or the content was out of scope. Listed for transparency; these
are not register rows.

| url | reason not cited |
|---|---|
| https://cset.georgetown.edu/publication/the-semiconductor-supply-chain/ | landing page; the PDF (SRC-002) was used instead |
| https://cset.georgetown.edu/publication/ai-chips-what-they-are-and-why-they-matter/ | landing page; the PDF (SRC-003) was used instead |
| https://www.energy.gov/articles/doe-releases-new-report-evaluating-increase-electricity-demand-data-centers | press release about the 2024 LBNL report; SRC-021 is the newer primary report |
| https://www.osti.gov/biblio/3374245 | catalogue record for SRC-021 (used to find the full text) |
| https://newsroom.lamresearch.com/Deposition-Essentials-Semi-101?blog=true | explanatory; SRC-002 and SRC-019 already cover deposition |
| https://powering-intelligence.epri.com/executive-summary.html | returned a 51-character page (script-rendered); no readable content |
| https://www.micron.com/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf | returned an HTML stub, not the PDF |
| https://www.thegreengrid.org/en/resources/library-and-tools/20-PUE:-A-Comprehensive-Examination-of-the-Metric | landing page only; the PUE document itself is member-only / sold via ASHRAE (see gaps) |

## Not retrievable in S01 (evidence gaps caused by access)

These sources would be preferred for some entries. The site refused an ordinary HTTPS
request (HTTP 403, 202 challenge or login wall). Per the S01 evidence rules, they were
**not** replaced by search snippets and access controls were not circumvented. The
affected entries in the map carry `not_researched` where no other retrieved source
covers them.

| source (host) | what it would add | outcome |
|---|---|---|
| JEDEC HBM standards, e.g. JESD238 (HBM3) and the JESD270-4 (HBM4) press release (`www.jedec.org`) | the standards-body definition of HBM and its generations | 403 |
| TSMC technology and annual-report pages (`www.tsmc.com`, `3dfabric.tsmc.com`, `investor.tsmc.com`, `pr.tsmc.com`) | primary foundry-model and CoWoS descriptions | 403 |
| Samsung Semiconductor (`semiconductor.samsung.com`) | a second HBM maker's and IDM-foundry's own descriptions | 403 |
| LBNL 2024 report hosts (`eta-publications.lbl.gov`, `eta.lbl.gov`, `escholarship.org`) | the 2024 report (superseded in part by SRC-021) | 403 / 202 challenge |
| IEA *Energy and AI* (`www.iea.org`) | an intergovernmental view of the energy interface | 403 |
| SEC EDGAR filings (`www.sec.gov`) | 10-K / 20-F business-model descriptions (e.g. NVIDIA, TSMC) | 403 |
| Intel (`www.intel.com`), Applied Materials, KLA, Cadence, SEMI, ISO (ISO/IEC 30134-2 PUE), OECD, Uptime Institute | IDM-foundry, equipment, EDA, standards and data-centre-industry views | 403 |
| AMD (`www.amd.com`) | a third accelerator vendor's documentation | connection error |
| The Green Grid PUE book | the standard PUE definition and measurement rules | member-only |
