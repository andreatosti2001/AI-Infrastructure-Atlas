# Visual benchmark: five data-intensive research products (S14.5)

**Status:** PROPOSED (S14.5, 2026-10-06; D-122). The human reviews it at the S14.5 review.
**Claim label:** every entry below is the Atlas's own reading (`INTERPRETATION`) of public pages
observed on 2026-10-06. Nothing here is evidence about AI infrastructure, and no statement made
*by* a benchmark is used as a fact anywhere in the Atlas. Where a benchmark page makes a claim about
the supply chain, it is quoted only to show a presentation pattern.
**Required by:** S14.5 prompt ("Required benchmark set"); `CLAUDE.md` §6A ("Benchmark hierarchy,
composition, annotation, typography, spacing and information density, but never copy another
organisation's branding or visual identity"); `MASTER-ARCHITECTURE.md` §16.1.
**Used by:** [`../architecture/visual-architecture.md`](../architecture/visual-architecture.md),
which turns the ADOPT and ADAPT rows of Part 3 into Atlas rules.

## In short

All five products put **the finding first and the data one step behind it**. The best of them also
keep **the source, the date, the unit and the uncertainty on the same screen as the chart**. Three
patterns transfer almost unchanged to the Atlas:

- the headline that states the takeaway;
- the chart, table and sources shown as views of one dataset (Our World in Data);
- the short "Assumptions and limitations" disclosure under every insight (Epoch AI).

Two patterns are rejected outright:

- **Pictorial supply-chain illustrations.** They imply links that no record supports.
- **Takeaway paragraphs that fuse a measured number with an interpretation.** A reader cannot tell
  which part is evidence.

The Atlas's own addition, which none of the five has, is a **visible difference between a stated
link, an inferred link and a gap**. Each mark carries that difference all the way to its claim.

## Method and its limits

| | |
|---|---|
| **Observed** | 2026-10-06, with the pre-installed headless Chromium (Playwright), at 1440 px and 390 px wide. For each page: screenshots, heading outline, landmarks, tabs and buttons, counts of SVG, canvas, table and `details` elements, image alt attributes, computed fonts, and a set of keywords (Source, Download, Table, Last updated…). The scratch script and the screenshots stayed outside the repository: no asset, logo or layout was copied |
| **Pages** | **Epoch AI:** `epoch.ai/data`, `/data-insights`, `/data-insights/frontier-data-center-power`, `/data/ai-chip-components`, `/data/machine-learning-hardware`. **Our World in Data (OWID):** `ourworldindata.org/artificial-intelligence`, three grapher pages (`share-electricity-renewables`, `data-centers-share-electricity-demand?tab=table`, `computation-used-to-train-notable-artificial-intelligence-systems`). **IEA:** *Energy and AI* (World Energy Outlook Special Report, April 2025, 304 pages, CC BY 4.0), read as the published PDF from `iea.blob.core.windows.net`. **Stanford AI Index:** the 2025 and 2026 report landing pages and the 2025 "Research and Development" chapter page. **Datawrapper:** `datawrapper.de/charts`, `/tables`, `/accessibility`, `/blog`, and two articles: "What to consider when using text in data visualizations" (L. C. Muth, 2022-09-28) and "We're improving the accessibility for Datawrapper charts and maps" (G. Aisch and L. C. Muth, 2021-03-31) |
| **Not observed** | **The IEA website:** `iea.org` answered 403 behind a security check for automated clients, and the web archive was unreachable through this environment's proxy. IEA's navigation, interactive charts and responsive behaviour are therefore **not assessed**. Only its report conventions are. **Interactions** were not exercised beyond the default state of each page: filters were not clicked and sliders not moved. **Contrast** was not measured on benchmark pages. Cookie banners covered part of several screenshots |
| **Bias** | Each product was seen through 1 to 5 pages chosen for their closeness to the Atlas's question (data centres, chips, components, AI). A product's other pages may differ |

## Part 1 — Each benchmark, across the fourteen dimensions

Short cells; "—" means the dimension was not observable on the pages seen.

### 1.1 Epoch AI

| Dimension | What was observed |
|---|---|
| Information architecture | Three content types: **datasets** ("Data on AI": hub cards, each with an "Updated <date>" line), **data explorers** (one per dataset) and **Data Insights** (short dated articles, each built on one chart). There is also a separate "Download our data" list (format and update date per file) |
| Navigation | Global bar: Latest, Our work, Navigate by topic, About. Insights index: topic checkboxes with counts ("Chips (21)"), search, sort (relevance, newest, oldest), result count ("94 results") |
| Content hierarchy | Insight page: type tag and date, then a **headline that states the finding** ("The record for power capacity in a single data center has doubled every 10 months"), a Cite button, the authors, a three-sentence lede with the key number, the chart, a one-line coverage caveat, two paragraphs, and then "Learn more about this graph" |
| Research cards | Insight card: tag, date, finding-as-title, one-sentence summary, authors, chart thumbnail. Dataset card: illustration, update date, name, one-sentence scope |
| Chart interaction | Explorer: tab buttons for the measure (Total cost / Logic / Packaging / Memory), a **Graph / Table toggle**, a settings panel (colour by component or designer, absolute or share of cost, quarterly or annual, show or project trend), info icons on legend items, Share, Download graph, Cite |
| Filtering and exploration | Explorer settings as above. Insight pages are static, with a link to "Explore this data" |
| Editorial composition | Insight chart: **observed and projected regions labelled on the chart**, a shaded trend band, a direct annotation ("2.3×/year"), direct series labels ("Frontier data centers", "Non-frontier") |
| Typography | One sans family throughout. Headline 46 px/600 on the data hub; body 16–20 px |
| Colour semantics | A teal brand accent marks the series of interest. Grey marks the context series; a pink/orange/blue set marks component categories in the explorer |
| Data density | Moderate: one chart per insight, with dense explorers behind them |
| Responsive behaviour | No horizontal overflow at 390 px on the five pages |
| Accessibility | Every image had an `alt` attribute. Charts are SVG on insight pages; the explorers also use a canvas. The main landmark was absent on the hub pages (`main: 0`) |
| Sources and methodology | Under every insight: collapsible **"Data", "Analysis", "Assumptions and limitations"**; code link ("Code for the analysis is available here"); CC BY line; dataset download with date. Explorer: Documentation / Downloads / Citations / FAQ side menu. The FAQ includes **"How confident are you in these estimates?"** and "How should the 'Other' row be interpreted?" |
| Insight ↔ visual ↔ data | Tight: one insight, one chart, one dataset, linked both ways (insight → "Explore this data"; dataset → related insights) |

### 1.2 Our World in Data

| Dimension | What was observed |
|---|---|
| Information architecture | Topic pages ("Artificial Intelligence": Key Charts, Featured Data Insights, research articles) and **data pages** (one indicator, "grapher"). Each grapher holds the chart, its table, its sources and its reuse terms on one URL |
| Navigation | Browse by topic, Data, Latest, Resources, About, search. On data pages, a "Configure the data" row of selects (Source, Metric, Frequency) |
| Content hierarchy | Chart title with the **time span as a suffix** ("…2020 to 2025"), then a subtitle that defines the measure and unit ("Measured as a percentage of total electricity generation"). Then the chart, a "Data source: … – Learn more about this data" line and a licence line |
| Research cards | "Featured Data Insights": a headline stating a finding ("Around 5% of electricity in the United States is used for data centers — far more than the global average") with its chart |
| Chart interaction | **Table / Map / Line (+ more) as tabs over one dataset.** Entity selector with search and sort; time slider; Download, Share, full screen |
| Filtering and exploration | Entity selection and the time range are the exploration model; the table can be sorted |
| Editorial composition | Restrained: the chart fills a framed card; the text around it is short. Axis notes such as "(plotted on a logarithmic axis)" |
| Typography | Serif display face for titles (40 px/600), humanist sans for body. Strong contrast between the title and the explanatory text |
| Colour semantics | Sequential greens on the renewables map; a single blue on the data-centre table's sparklines |
| Data density | High in the table view: per-entity start and end values, **a sparkline column, absolute change ("+0.3 pp") and relative change** |
| Responsive behaviour | At 390 px the tabs become icons, the selects stack, and **the table drops its sparkline and change columns** rather than scrolling sideways |
| Accessibility | Header, nav, main and footer landmarks present on data pages; images without `alt`: 2 on the renewables data page, 3 on the AI topic page |
| Sources and methodology | **"About this data"**: source, last updated, **next expected update**, date range, unit. **"What you should know about this indicator"**. **"Sources and processing"**: one card per source and "How we process data", plus "Notes on our processing step for this indicator". **"Reuse this work"**, ready-made citations (in-line and full), and downloads of full vs displayed data **with their row counts** ("7,615 rows" / "192 rows"); a data API with CSV and metadata URLs. **Uncertainty in the subtitle:** "Estimated from AI literature, albeit with some uncertainty. Estimates are expected to be accurate within a factor of 2, or a factor of 5 for recent undisclosed models like GPT-4" |
| Insight ↔ visual ↔ data | The strongest of the five: the visual, the table and the provenance are **three views of the same indicator**, one scroll apart |

### 1.3 International Energy Agency (report conventions only)

| Dimension | What was observed |
|---|---|
| Information architecture | Report: Executive Summary, numbered chapters and sections (2.3, 2.3.1…), **Annex A "Methodology and data tables", Annex B "Definitions"** |
| Navigation | Website not assessed (see Method). In the PDF: table of contents, running chapter footers ("Chapter 2 \| Energy for AI") |
| Content hierarchy | Prose carries the argument and **cites figures by number** ("(Figure 2.9)") |
| Research cards | — |
| Chart interaction | — (static figures) |
| Filtering and exploration | — |
| Editorial composition | Every figure: **"Figure 2.9 ⊳" plus a descriptive title with its period**; the unit on the axis (TWh); a licence line ("IEA. CC BY 4.0."); then **one italic, coloured sentence stating the figure's message** ("Different modelling approaches can lead to a wide range of estimates"); then **"Source: IEA analysis based on data from …"**, and "Note:" for abbreviations and definitions |
| Typography | Bold sans figure titles, a coloured figure number, a lighter source line |
| Colour semantics | One highlight colour for the agency's own estimate against neutral data points (Figure 2.9) |
| Data density | Medium: one message per figure |
| Responsive behaviour | — |
| Accessibility | The PDF is not tagged (`Tagged: no` in its metadata) |
| Sources and methodology | Source line under each figure; methods in an annex; **uncertainty handled by named sensitivity cases** (Base, Lift-Off, High Efficiency, Headwinds). Text states: "all historical data regarding global data centre electricity consumption are modelled estimates, not measured data, and the range of estimates is wide" |
| Insight ↔ visual ↔ data | Figure 2.9 **draws every competing estimate as a dot, with the agency's estimate as a labelled line**: disagreement is shown, not hidden. Figure 1.9 is a **pictorial supply chain** (sand → wafer → lithography → GPU → data centre → applications), captioned "AI is supported by a highly complex global supply chain"; it is an illustration with no data behind its arrows |

### 1.4 Stanford AI Index

| Dimension | What was observed |
|---|---|
| Information architecture | Annual report: landing page with Top Takeaways, a Chapter Lineup (nine chapters in 2026) and Past Reports; the full report as a PDF download; a separate "Global Vibrancy Tool" |
| Navigation | Institutional site navigation; chapter buttons ("01 Research and Development" …) |
| Content hierarchy | **Numbered takeaways whose headings are claims** ("3. The United States hosts the most AI data centers, with the majority of their chips fabricated by one Taiwanese foundry."), each followed by a paragraph of figures and a "See: Chapter N" link |
| Research cards | Takeaway blocks: claim heading, paragraph, chapter link, chart image beside it |
| Chart interaction | — (static chart images on the landing page) |
| Filtering and exploration | By chapter only, on the pages seen |
| Editorial composition | Alternating text and chart; the chart images carry their own titles and source notes in small type |
| Typography | Large display sans in the hero (84 px); body in the same family |
| Colour semantics | A blue institutional palette in the charts |
| Data density | Low on the landing page; the density is in the PDF |
| Responsive behaviour | No horizontal overflow at 390 px |
| Accessibility | All images had `alt`. The 2025 chapter page seen had **no `h1`** |
| Sources and methodology | In the report; on the web, the link from a takeaway to its chapter is the only route to a source |
| Insight ↔ visual ↔ data | Loose: a takeaway paragraph **fuses measured figures with interpretation**. Takeaway 3's text, for example, joins a count of data centres to "making the global AI hardware supply chain dependent on one foundry in Taiwan" in the same paragraph, with no marker of where the measurement ends and the reading begins |

### 1.5 Datawrapper (tool and its published guidance)

| Dimension | What was observed |
|---|---|
| Information architecture | A product site (charts, maps, tables), an Academy and a blog (including a "Fix my chart" series) |
| Navigation | Features, Learn, Pricing; chart-type tabs on product pages |
| Content hierarchy | Guidance: the **title states the takeaway** ("Be conversational first and precise later"); the description holds the precision (what, when, where); notes and source are small and grey |
| Research cards | — |
| Chart interaction | Keyboard navigation of chart, map and table elements ("Press Tab to go to the next element…") |
| Filtering and exploration | Tables: search, sorting, heatmap colouring and **mini charts inside table cells** |
| Editorial composition | **Direct labels instead of legends** ("Remove the color key and directly label your categories"); annotations "if you're creating an explanatory chart"; **units repeated in axis labels, tooltips and annotations** |
| Typography | — (tool, not a publication) |
| Colour semantics | An automatic **colour-blindness check** with a warning |
| Data density | — |
| Responsive behaviour | No horizontal overflow at 390 px on the product pages |
| Accessibility | **Author-written alternative text**, read to screen readers, with the chart body hidden from them (`aria-hidden`). A **fallback description** names the chart type and counts its lines or symbols, with a stated limit: "our fallback descriptions don't state what the chart actually tells us". A **"Get the data" link** |
| Sources and methodology | A source name and URL in every chart footer |
| Insight ↔ visual ↔ data | The chart carries its own text hierarchy (title → description → chart → notes → source), so it can travel alone |

## Part 2 — What the five have in common, and what none of them does

**Common, and right for the Atlas:**

1. The finding is a sentence a reader can repeat, and it sits above the visual.
2. The unit, the period and the scope are in the subtitle, before the chart.
3. A source line sits under every chart, and the full methodology is one step away.
4. The table is offered beside the chart as an equal view of the same data.
5. Uncertainty is said in words near the number: a factor of 2 (OWID), named cases (IEA), "estimates carry uncertainty" (Epoch).

**What none of them shows, and the Atlas must:**

- **The basis of each mark.** A benchmark chart can show an estimate band, but not whether a given
  bar or link rests on a first-hand statement, on the publisher's own inference, or on nothing yet.
  The Atlas already records this per link (stated, inferred, gap: D-103, D-120). Its visuals must
  carry it.
- **The unknown as a mark.** Benchmarks drop missing data from a chart or footnote it. In a
  dependency map, an absent supplier read as "no supplier" is exactly the error `CLAUDE.md` §7
  forbids. The Atlas draws the gap.
- **Claim-level provenance from a mark.** Benchmarks cite datasets. The Atlas can open, from any
  mark, the claim and the quoted sentence behind it.

## Part 3 — Pattern register: ADOPT, ADAPT, REJECT

**ADOPT** means used as observed. **ADAPT** means used with a change that the Atlas's evidence model
requires (the change is stated). **REJECT** means not used, with the reason. The "Atlas rule" column
points into [`visual-architecture.md`](../architecture/visual-architecture.md).

| # | Pattern (seen at) | Verdict | Why, and the Atlas form | Atlas rule |
|---|---|---|---|---|
| P-01 | Headline that states the finding (Epoch, OWID insights, Datawrapper) | **ADAPT** | Adopted as the reader's first line. Change: the headline is **composed from record values and fixed words** (the text provenance rule, D-105), never free prose. When the records do not support one sentence, the question stands as the headline instead | §1 V-2; §6 |
| P-02 | Subtitle with the measure, unit and period (OWID) | **ADOPT** | Every visual's subtitle says what is counted or drawn, over which population, as of which evidence dates | §1 V-4 |
| P-03 | Chart / Table / Map tabs over one dataset (OWID; Epoch's Graph/Table toggle) | **ADAPT** | The table is never hidden behind a tab in the Atlas: it is the visual's text equivalent and the place where the IDs live. It follows the visual on the same page, and both render the **same SQL result** | §8; §9 |
| P-04 | "Learn more" with Data / Analysis / Assumptions and limitations disclosures (Epoch) | **ADOPT** | Becomes the METHOD layer: a closed disclosure under each result, generated from the query file (D-115, D-121) plus the limits the result carries | §2 layer 7 |
| P-05 | "About this data": source, last updated, next update, range, unit (OWID) | **ADAPT** | Change: no "next expected update" (the Atlas has no update schedule), and "last updated" becomes **evidence dated from–to** plus the input digest. An age needs a clock, and committed results must not depend on one (`sql-layer.md` §7) | §1 V-5 |
| P-06 | Uncertainty sentence in the subtitle (OWID) | **ADAPT** | Change: the uncertainty is not a magnitude band (the Atlas has no numeric confidence) but a **basis word on every mark** (stated / inferred / gap) and the caveat flags of the row | §7 |
| P-07 | Observed vs projected regions labelled on the chart (Epoch) | **ADAPT** | Same idea, applied to links: what a source states, and what the Atlas infers, are drawn differently and **labelled in words on the mark**, not only in a legend | §7 |
| P-08 | Competing estimates all drawn, one highlighted (IEA Fig. 2.9) | **ADOPT** (future) | When two records disagree (`disputed`), both are drawn and neither is averaged. No disputed claim exists today, so this is a rule for S15 and S20, not part of the prototype | §6 grammar "comparison" |
| P-09 | One message sentence under each figure (IEA) | **ADAPT** | Change: the message sits **above** the visual (P-01), and the line under it is the **reading note** (how to read the encoding), so the takeaway is never separated from its visual on a phone | §1 V-2 |
| P-10 | "Source: X analysis based on data from Y" (IEA) | **ADOPT** | The Atlas states whose step each value is: "stated" (a source speaks), "inferred" (the Atlas's derivation), "rests on the Atlas's own definitions" | §7 |
| P-11 | Direct labels, no legend (Datawrapper) | **ADAPT** | Labels go on the marks ("inferred", "not researched"). A short key stays, because the line styles carry evidence meaning that a first-time reader must be told once | §3 |
| P-12 | Units repeated everywhere (Datawrapper) | **ADOPT** | Every count names its unit and its denominator in the same block ("1 of 4 links") | §1 V-4 |
| P-13 | Author-written alt text plus a data link (Datawrapper) | **ADAPT** | Change: the alternative is not a sentence but a **structured text equivalent** (an ordered list or table) generated from the same rows, so it cannot drift | §3; §8 |
| P-14 | Fallback description counting symbols (Datawrapper) | **REJECT** | A count of marks says nothing about what they mean; Datawrapper states that limit itself | — |
| P-15 | Colour-blindness check (Datawrapper) | **ADAPT** | The Atlas never uses colour as the only carrier (D-103), and checks contrast statically (PG-8) and in the browser | §3 |
| P-16 | Insight cards with finding-titles and thumbnails, topic filter with counts (Epoch, OWID) | **ADAPT, deferred to S20** | The future index of Atlas questions. A card shows the question, the composed finding, the evidence-date range and the basis mix; never a thumbnail without its words | §4 |
| P-17 | Dataset hub with per-dataset "Updated" dates and downloads (Epoch) | **ADAPT, deferred to S20/S21** | Change: the date is the evidence range and the input digest, not a publication date | §4 |
| P-18 | Ready-made citations, full vs displayed downloads with row counts (OWID) | **ADAPT, deferred to S21** | The client-output session decides formats; the "rows shown / rows in the result" idea is used now in the table's filter | §4; §10 |
| P-19 | Settings panel: absolute vs share, colour-by switch (Epoch) | **REJECT for now** | Mode switches that change a measure need a defined metric and denominator first (NG-11; S15–S16) | §10 |
| P-20 | Sparkline and change columns in a table (OWID) | **ADAPT, S15+** | Allowed once a time series exists; at phone width the extra columns drop, as OWID does, rather than scroll | §6 grammar "tables" |
| P-21 | Table that drops columns at phone width (OWID) | **ADAPT** | The Atlas's table already becomes stacked labelled cards (S14). It keeps that: no column carrying evidence status may be dropped | §5 |
| P-22 | Numbered takeaways with chapter links (AI Index) | **ADAPT** | One finding per block, each with its evidence link | §6 |
| P-23 | Takeaway paragraph mixing measured figures and interpretation (AI Index) | **REJECT** | It breaks the FACT / INTERPRETATION boundary (`CLAUDE.md` §6). In the Atlas the composed finding (record values) and the Atlas reading (labelled interpretation) are separate blocks | §1 V-3 |
| P-24 | Pictorial supply-chain illustration (IEA Fig. 1.9) | **REJECT** | Arrows between pictures imply dependencies that no record states. Every Atlas line is an edge, a recorded gap, or nothing | §7 |
| P-25 | Brand colour as the emphasis colour (Epoch, AI Index) | **REJECT** | In the Atlas, colour is reserved for evidence meaning (the gap amber) and for level (class tint). Decorative emphasis would compete with it | §3 |
| P-26 | Illustrated dataset cards (Epoch's abstract artwork) | **REJECT** | Decorative; no capability shown (`CLAUDE.md` §15) | — |
| P-27 | Serif display for titles, sans for reading (OWID) | **ADOPT** | Already the Atlas page's choice; kept as a token (system fonts only, no web-font loading: PG-9) | §3 |
| P-28 | Interactive chart on canvas (Epoch explorers) | **REJECT** | Canvas output is opaque to text checks and screen readers. The Atlas draws with HTML and SVG, so the provenance checks can read every mark | §3 |
| P-29 | Video in the landing page (AI Index) | **REJECT** | Not evidence; adds weight and a third-party request | — |

## Part 4 — What this means for the Atlas (the hand-off)

- **For the architecture** (`visual-architecture.md`): P-01, P-02, P-04, P-05, P-06, P-07, P-09,
  P-10, P-11, P-12, P-13, P-15 and P-21 become rules now; P-03 becomes the SQL-to-visual rule.
- **For the prototype**: headline (P-01), subtitle with denominator (P-02, P-12), reading note under
  the visual (P-09), basis words on marks (P-07, P-11), a method disclosure (P-04), the table as an
  equal view (P-03, P-21).
- **For S15** (metrics): P-08 (competing values), P-19 (no mode switch before a defined metric),
  P-20 (time series in tables).
- **For S20** (researcher UX): P-16, P-17 and the exploration model of OWID (entity selection and
  time range), adapted to "which accelerator, which layer of the chain, which basis".
- **For S21** (client output): P-18.
