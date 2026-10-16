# Known limitations of v1.0

**Status:** accepted (decided by the human on 2026-10-16, S24 H-2; D-222, D-223, D-224). Written by the Portfolio Reviewer;
checked against the built pages by `tests/test_known_limitations.py` (KL-1 to KL-8). S25 links it from the release
notes.

This page says what v1.0 of the Atlas does not do, in one place. **Gaps** are things a later session could close:
each says what is missing, why, what would close it, and which session after v1.0 owns it. **Boundaries by design**
are things the Atlas does not do on purpose; nothing in the plan closes them, and changing one needs a decision.
Each row links to the record that holds the gap (the audit finding, the decision); it restates no record's value.

The last two tables tie the document to the pages. **Where the pages state each limit** quotes, for every row, the
sentence or label a reader meets on a page, or says "none" when no page states it. **Framing sentences that explain
rather than limit** lists the remaining sentences of the pages' limits framing, so that every such sentence is
accounted for. The check compares these quotations with the built pages, sentence by sentence: a limit added to a
page and missing here, or quoted here and gone from the page, fails the suite.

## Gaps

| ID | Key | What is missing | Why | What would close it | Owner after v1.0 | Record |
|---|---|---|---|---|---|---|
| KL-01 | `coverage` | Breadth. The Atlas follows one path: two accelerators, the memory inside them and the process that memory needs. Foundries, packaging, equipment, data centres and energy have no supply-chain records, and most concepts of the Atlas's own domain map have none | v1 was scoped to one end-to-end slice before growing | research and datasets for each layer of the chain, with v1's method | v2, phase B (finish the first chain) and later phases | [release content audit C-6](research/release-content-audit.md); D-201 |
| KL-02 | `single-voice` | Corroboration. No value in the Atlas rests on two independent publishers; each is one voice, and the supplier fields rest on two market-research firms | v1 recorded the best available source per value; it did not seek a second | a second, independent source for the values a page relies on, recorded through the review path | v2 (D-201); not yet a named session | [release content audit C-5](research/release-content-audit.md); D-218 (DT-S23-3) |
| KL-03 | `h100-supplier-current` | A current memory supplier for the NVIDIA H100. The supplier field rests on one market-research report and holds only for a period that ended well before the as-of date | no newer product-level statement was found in v1's supplier research | a current, product-level statement from a recognised source, through staging and the human's review | a supplier research session after v1.0 that the roadmap does not yet name (D-218) | [release content audit C-10](research/release-content-audit.md); [supplier research](research/hbm-supplier-research.md); D-218 |
| KL-04 | `h100-fabricator` | Who fabricates the NVIDIA H100. The only product-level statement is older than the freshness rule allows, so the link is drawn as a recorded gap, not a link | the evidence was refused as not fresh (a refused candidate) | a fresh product-level statement; the build then stops by name until the HBM page's specification is updated with it | a research session after v1.0 that the roadmap does not yet name (D-218) | `cand-001`; D-092; [release content audit, Part 6 row 6](research/release-content-audit.md); D-218 |
| KL-05 | `trainium2-recognised` | A recognised source for who makes AWS Trainium2's memory. The supplier field rests on one assessment that does not meet the source policy's "recognised" criterion | no recognised source naming the maker was found | a statement from a recognised source, or from the parties | a supplier research session after v1.0 that the roadmap does not yet name (D-218) | [release content audit C-10](research/release-content-audit.md); D-147; D-218 |
| KL-06 | `aged-values` | Newer evidence for values past the freshness horizon. Company values whose newest evidence is older than the horizon allows are marked on their company page, not refreshed | refreshing them is new research, which S23 sent to a later session | the company's newer filing, read and reviewed; the mark then goes away by itself | a research session after v1.0 that the roadmap does not yet name (D-218) | D-221; [release content audit C-2](research/release-content-audit.md) |
| KL-07 | `ear-dates` | The Export Administration Regulations' own dates. The EAR is recorded, but no effective date of its own, so its status is "no recorded effect" | the dated official text of the EAR's reissue was not retrieved in v1 | the official text that dates the EAR, registered and read | the next policy research session, which the roadmap does not yet name (D-210, D-218) | D-210; [release content audit, Part 6 row 8](research/release-content-audit.md); D-218 |
| KL-08 | `bis-guidance-2026-05` | BIS's later guidance on the AI Diffusion rule. A later official text cites it by its address, which the pages quote; the Atlas has not read the guidance itself, and its printed address did not answer | the address returned an error when S23 sought it | the guidance retrieved from its current address, registered, and read against the rule | the next policy research session, which the roadmap does not yet name (D-210, D-218) | D-210; [release content audit, Part 6 row 8](research/release-content-audit.md); D-218 |
| KL-09 | `later-texts` | Rules, amendments or guidance published after the search date. The later-rule search covers each act up to the as-of date and no further | the search is dated and logged, and stops at the as-of date by rule | re-running the later-rule search to each new as-of date before the pages move to it | every session that moves the as-of date (D-208); S25 if it moves it | D-208; D-211 |
| KL-10 | `supplier-changes` | Changes of supplier, design or fabrication after the dates of the evidence. The Atlas records what its sources said when they said it, and watches nothing | v1 has a dated search for later rules, not a monitor of companies | a change detector for company and supplier evidence, with its own search log | v2 (agent activation at scale, D-201) | D-207; D-201 |
| KL-11 | `unlinked-classes` | Dependencies of the recorded classes that no link starts or ends at, and of the records drawn beside the chain without an edge. A question about what they depend on cannot be answered yet | v1 recorded the classes it needed to name, but linked only the one path | research and links for those classes | v2, phase B | [release content audit C-6](research/release-content-audit.md); D-201 |
| KL-12 | `search` | Search across the records. The entry page lists every page instead | the pages load no script and need no server (v1's design rules) | a search decided at v1.5's opening, if the human approves it | v1.5, the overview and interaction session | D-201 (v1.5's plan); D-193 |
| KL-13 | `concept-layer` | A page for the Atlas's working definitions and the conflicts between sources' definitions. That research is in the records but on no page | no v1 journey needed it | a page for the concepts and their conflicts | v1.5 | [release content audit C-7](research/release-content-audit.md); D-218 (DT-S23-4) |
| KL-14 | `access-gaps` | A second reading, without the human, of every source the Atlas cites. Some sources (standards pages, one annual report, two company pages) refuse automated retrieval, so their anchors can be re-read only from a file the human supplies | the publishers refuse automated requests, and the Atlas never circumvents a refusal | the human's file for each, when a claim citing it is next relied on | the Verifier, with the human's file, in the session that next relies on them | [release content audit C-4](research/release-content-audit.md); D-218 (DT-S23-2) |
| KL-15 | `outside-reader` | Any use by a reader outside the project, and a public address. The pages are built and checked in the repository but not published, and no one who did not build them has used them | publication is the human's decision (an external action), and v1 measured readers only by the human and by fresh AI readers | publishing the pages, and a reading by someone outside the project | S25 (the release decides publication); v1.5's design review | [portfolio audit P-3](architecture/portfolio-audit.md); D-184 |

## Boundaries by design

| ID | Key | What the Atlas does not do | Why | What would change it | Owner | Record |
|---|---|---|---|---|---|---|
| KB-01 | `legal-determination` | Decide whether any product, firm or transaction falls under a text, or apply a text's conditions (destinations, licence policy, thresholds, exemptions) | the Atlas describes texts; legal advice and compliance determinations are out of scope | nothing planned; a change of scope needs a decision | none: boundary by design | NG-12 ([baseline](architecture/baseline.md)); D-167 |
| KB-02 | `other-law` | Record the law of any jurisdiction other than the acts it lists | v1's policy layer holds United States export-control acts only | v2's global policy phase, by decision at its opening | v2, phase C | [baseline](architecture/baseline.md); D-201 |
| KB-03 | `state-control` | Say whether a state controls or influences a firm, or treat a place as more than where a record says a company is incorporated, headquartered or located | control is a legal and factual judgement the evidence model does not make | nothing planned | none: boundary by design | [policy links](architecture/policy-links.md) |
| KB-04 | `quantities` | Record market share, revenue, price, volume, capacity, customers or ownership | v1 records relations and their evidence, not quantities; ownership links were refused for lack of a statement | v1.5's measured-data slice adds sourced figures; shares and rankings stay excluded | v1.5 (figures); none for shares | NG-11 ([baseline](architecture/baseline.md)); D-201 |
| KB-05 | `no-scores` | Compute shares, rankings, scores or confidence values, or count the world | a count on a page counts the Atlas's records; a score would add a judgement no record holds | nothing planned | none: boundary by design | NG-11 ([baseline](architecture/baseline.md)); D-124 |

## Where the pages state each limit

`framing`: the quotation is found, whole, in an Atlas framing block of every page the path names. `label`: it is found
in the text of every page the path names. `none`: no page states it; the record column says where it is held.

| Row | Page | Kind | Text on the page |
|---|---|---|---|
| KL-01 | `site/briefs/accelerator-memory/index.html` | framing | "Accelerators other than those named above, and stages of the chain beyond memory: fabrication beyond the recorded gap, packaging, equipment, servers and cloud." |
| KL-01 | `site/briefs/accelerator-memory/index.html` | framing | "Accelerators, memory products and stages of the chain outside the scope." |
| KL-02 | `site/briefs/accelerator-memory/index.html` | label | "one publisher only" |
| KL-02 | `site/hbm-chain/index.html` | label | "one publisher only" |
| KL-03 | `site/briefs/accelerator-memory/index.html` | label | "historical, to" |
| KL-03 | `site/hbm-insight/index.html` | label | "historical, to" |
| KL-03 | `site/briefs/accelerator-memory/index.html` | framing | "A named or reported supplier is not the only supplier: a source that names one maker does not say that there are no others." |
| KL-04 | `site/briefs/accelerator-memory/index.html` | label | "a recorded gap, not a link" |
| KL-04 | `site/hbm-chain/index.html` | label | "evidence not fresh" |
| KL-05 | `site/briefs/accelerator-memory/index.html` | label | "criterion not met: recognised" |
| KL-05 | `site/hbm-insight/index.html` | label | "criterion not met: recognised" |
| KL-06 | `site/companies/company-micron-technology/index.html` | framing | "It does not mean the value has changed: the Atlas has not yet re-checked it against newer evidence." |
| KL-07 | `site/questions/export-control-texts/index.html` | label | "no recorded effect" |
| KL-08 | `site/questions/export-control-texts/index.html` | framing | "A text the later statement itself cites is held only as the statement quotes it: the Atlas has not read it." |
| KL-08 | `site/briefs/accelerator-memory/index.html` | framing | "A text the later statement itself cites is held only as the statement quotes it: the Atlas has not read it." |
| KL-09 | `site/briefs/accelerator-memory/index.html` | framing | "Acts, amendments or guidance published after the latest publication date shown in this brief." |
| KL-09 | `site/questions/export-control-texts/index.html` | framing | "Only the acts the Atlas holds and the later texts its search found were read; texts published after the search date below were not searched." |
| KL-10 | `site/briefs/accelerator-memory/index.html` | framing | "Changes of supplier, design or fabrication after the dates of the evidence shown." |
| KL-11 | `site/index.html` | framing | "The classes listed here are recorded, but no dependency link starts or ends at them, so a question about what they depend on cannot be answered yet." |
| KL-11 | `site/hbm-chain/index.html` | framing | "The records in the lane under the diagram sit near this chain in the Atlas, but no recorded edge links them to the accelerators on it." |
| KL-12 | `site/index.html` | framing | "Searching across the records would need a script or a server, so the Atlas lists every page instead." |
| KL-13 | — | none | No page shows the concept layer, so no page can say it is missing. Held in the release content audit (C-7) |
| KL-14 | — | none | Access gaps are a property of the Atlas's re-reading, not of a page's content. Held in the release content audit (C-4) |
| KL-15 | `site/hbm-insight/index.html` | framing | "It is not published." |
| KB-01 | `site/briefs/accelerator-memory/index.html` | framing | "Whether any product, firm or transaction falls under a text: the Atlas never makes that determination." |
| KB-01 | `site/briefs/accelerator-memory/index.html` | framing | "Whether any product, firm or transaction falls under a text, and what anyone would need to do about it." |
| KB-01 | `site/briefs/accelerator-memory/index.html` | framing | "Destinations, licence policy, thresholds and exemptions: they stay in the texts." |
| KB-01 | `site/questions/export-control-texts/index.html` | framing | "Whether any product or company is controlled, for which destinations and under which licence policy: those conditions stay in the texts, and the Atlas never applies a threshold to a product or a firm." |
| KB-02 | `site/briefs/accelerator-memory/index.html` | framing | "The law of any other jurisdiction." |
| KB-02 | `site/places/*/index.html` | framing | "Whether a state controls or influences a firm, and any law of the place other than the acts listed." |
| KB-03 | `site/places/*/index.html` | framing | "Whether a state controls or influences a firm, and any law of the place other than the acts listed." |
| KB-04 | `site/briefs/accelerator-memory/index.html` | framing | "Market share, price, volume, capacity or customers." |
| KB-04 | `site/briefs/accelerator-memory/index.html` | framing | "Quantities: market share, price, volume, capacity, customers." |
| KB-04 | `site/companies/*/index.html` | framing | "Market share, revenue, capacity, customers or ownership: the Atlas records none of them." |
| KB-05 | `site/hbm-chain/index.html` | framing | "The page shows no shares, counts, rankings or scores, and no confidence values: each claim carries its type and evidence status instead." |
| KB-05 | `site/hbm-insight/index.html` | framing | "Every number describes what the Atlas records, never the industry, and a count of rows is not a count of records." |
| KB-05 | `site/hbm-insight/index.html` | framing | "The page computes no share, ranking or score, and no confidence value." |
| KB-05 | `site/questions/export-control-texts/index.html` | framing | "Each count on this page counts the Atlas's records, never the world." |
| KB-05 | `site/companies/*/index.html` | framing | "Each count on this page counts the Atlas's records about the company, never its activity." |

## Framing sentences that explain rather than limit

Sentences of the pages' limits framing that say how to read the page or how it was made, not what it lacks.

| Page | Text |
|---|---|
| `site/*` | "Only canonical records appear: records awaiting review are left out." |
| `site/*` | "The page is generated from the Atlas's data files by a tested build step; nothing on it is typed by hand." |
| `site/*` | "The digest identifies the exact inputs; rebuilding from the same inputs gives the same page, byte for byte." |
| `site/briefs/accelerator-memory/index.html` | "The brief is generated from the Atlas's data files and its computed results by a tested build step; nothing on it is typed by hand." |
| `site/briefs/accelerator-memory/index.html` | "The summary copies values, counts the rows it shows, takes the first and last of a date column, and groups rows; it computes nothing else." |
| `site/briefs/accelerator-memory/index.html` | "A status comes from the Atlas's status rule on the as-of date." |
| `site/briefs/accelerator-memory/index.html` | "The digest identifies the exact inputs; rebuilding from the same inputs gives the same brief, byte for byte." |
| `site/briefs/accelerator-memory/index.html` | "What the records leave open, each with its reason: values the Atlas could not determine, candidate links it considered and refused, and pairs with no record either way." |
| `site/briefs/accelerator-memory/index.html` | "A gap is never a zero and never a “no”." |
| `site/briefs/accelerator-memory/index.html` | "This list describes the Atlas's coverage." |
| `site/briefs/accelerator-memory/index.html` | "It is not a list of things to watch." |
| `site/companies/*/index.html` | "An ownership link it considered is a refused candidate, shown above with its reason." |
| `site/hbm-chain/index.html` | "They are drawn apart so that their absence from the chain is visible, not to suggest a link." |
| `site/hbm-chain/index.html` | "A missing line means the Atlas has not recorded a relationship; it never means that no relationship exists." |
| `site/hbm-chain/index.html` | "The reasons above are the Atlas's own explanations, each held in the record of the candidate it refuses." |
| `site/hbm-chain/index.html` | "Their rule codes are listed with the place each is defined." |
| `site/hbm-chain/index.html` | "A section mark (§) points into one of the Atlas's design documents; the edge design record linked above the cards says which." |
| `site/hbm-chain/index.html` | "The chain is walked from the relationship records each time the page is built, and is not stored." |
| `site/hbm-chain/index.html` | "The rulings below shape what the records hold." |
| `site/hbm-insight/index.html` | "The page is generated from the committed SQL results and the Atlas's records by a tested build step; nothing on it is typed by hand." |
| `site/hbm-insight/index.html` | "Each measure is a SQL result with its own explanation below; the few counts the page makes itself are tallies of rows it draws, each shown beside the number of rows it is counted over." |
| `site/index.html` | "A missing link means the Atlas has not recorded one; it never means that none exists." |
| `site/places/*/index.html` | "Incorporation and headquarters are where a company's own filings place it; a company whose incorporation the Atlas has not researched is listed under its headquarters, with that state in words." |
| `site/places/*/index.html` | "A missing entry means the Atlas has not recorded one; it never means that none exists." |
