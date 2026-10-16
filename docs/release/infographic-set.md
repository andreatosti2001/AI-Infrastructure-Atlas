# The representative infographic set — v1.0

- **Status:** accepted (decided by the human on 2026-10-16, S25 H-3; D-230). Written by the
  Editorial (D-229).
- **What it is:** four visuals chosen from the 18 pages to show the Atlas's visual language and its evidence-aware
  storytelling. No visual was made for this set. Each entry says which question the visual answers, why it has its
  form, how a reader gets from a mark to the source sentence, and which checks hold it. This is v1.5's starting point
  (`VERSION-ROADMAP.md` §1). Screenshots at 1280 and 375 px are kept in the private archive with the session's QA.
- **Read them live:** each link opens the published page at the visual.

## The visual language, in common

- **Every mark is evidence.** A mark, a cell or a dot is a link. Pressing Enter on it opens the panel with the claims
  it rests on, each shown whole, with its type, evidence status, quoted sentence, locator, source and the human's
  review. No value appears only on hover.
- **Unknowns are drawn, with words.** A gap is a dashed mark labelled as a gap, a refusal is a word with its reason,
  and nothing missing is ever drawn as a zero.
- **The page says how to read it.** An "Atlas framing" block beside each visual says what the encoding means and what
  it does not show; KL-1 to KL-8 tie those sentences to the [known limitations](../known-limitations.md).
- **One palette and system fonts.** Contrast is measured on every rendered text node, and every page is laid out for
  phones at 375 px. Nothing loads, and no script runs.

## 1. The dependency chain diagram

- **Where:** [the HBM dependency journey, "The chain"](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/hbm-chain/index.html#chain).
- **Question:** what does an AI accelerator's memory depend on, and who is known to make it?
- **Form, and why:** a node-link chain read left to right, from each accelerator to its memory, the memory's maker and
  the process it requires. A dependency is a path of typed links, so position shows the layer and the line shows how
  the link is known (stated, inferred, reported, or a recorded gap). Records near the chain but not linked to it sit in
  a lane below it, drawn apart so that their absence from the chain is visible.
- **From mark to source:** each mark opens its evidence panel on the same page, and the panel links the source and
  the review entry. The chain is walked from `data/relationships.json` at each build and not stored.
- **Held by:** PG-1 to PG-10 (`tests/test_page.py`: text provenance, marks, inference labels, gaps, framing,
  identical rebuild, contrast, links); `tests/browser/hbm-chain.qa.js` (the keyboard path to every panel).

## 2. The research view's indicators and side-by-side chains

- **Where:** [the research view, "What the records show"](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/hbm-insight/index.html#insight)
  and ["The chains, side by side"](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/hbm-insight/index.html#visual).
- **Question:** where do the two accelerators' chains agree and differ, and how is each link known?
- **Form, and why:** the answer comes first, then indicator blocks, then the two chains as parallel strips with one
  unit square per link, coloured by how the link is known, and a filter that outlines one basis at a time (CSS only).
  A comparison of two short chains needs alignment, not a chart. Each tally prints its denominator in the same block,
  and a metric that cannot be computed is shown as that state, with its reason (D-124, D-130, D-132).
- **From mark to source:** every cell is the committed SQL result, cell for cell. A unit square opens its table row,
  and the row opens the HBM page's evidence panel. Each indicator has a "How this was computed" tutorial: the query,
  what each part does, and how to read the result.
- **Held by:** IN-1 to IN-14 (`tests/test_insight.py`); `tests/browser/hbm-insight.qa.js`;
  `tests/browser/filter.qa.js` (the filter in Chromium, Firefox and WebKit).

## 3. The export-control matrix and timeline

- **Where:** [the export-control comparison, "The matrix"](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/questions/export-control-texts/index.html#matrix),
  ["The timeline"](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/questions/export-control-texts/index.html#timeline)
  and ["Statuses"](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/questions/export-control-texts/index.html#statuses).
- **Question:** which parts and technologies does each recorded export-control text name among the items it
  controls, and when did each take effect?
- **Form, and why:** a matrix of acts against the classes on the chain, with words in the cells rather than colours,
  because a refusal and its reason are the finding. A timeline puts one lane per act and every dated event on one
  scale: hollow for published, filled for effective, a dashed line for the as-of date. An act with no dated event is
  listed beside the axis, never placed at a guessed date. Each act's status is derived on the as-of date, with the line
  that the page describes the text and does not advise.
- **From mark to source:** each cell and each dot opens the act's evidence (the act's own quoted sentence and its
  official text). A later statement about an act sits in that act's panel.
- **Held by:** JR-4 (the matrix equals the records), JR-5 (every dated event at its date), JR-6, JR-7 (statuses on the
  as-of date), JR-13 to JR-15 (`tests/test_journeys.py`); `tests/browser/journeys.qa.js` (Enter on a timeline mark
  and on a matrix cell).
- **Known limit:** on a phone the timeline's text is too small; the word list under it is the phone form until v1.5
  (engineering audit F-6).

## 4. The client brief's dependency map

- **Where:** [the client brief, "Dependency map"](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/briefs/accelerator-memory/index.html#map).
- **Question:** what does an AI accelerator's memory depend on, who is reported to supply it, and which recorded
  export-control texts name those parts?
- **Form, and why:** the HBM page's accepted figure, drawn again inside a printable brief, then the chain in words and
  the full result table with its tutorial. A brief travels as paper, so the map prints, and its scope, limits, as-of
  date and input digest are on the first printed page.
- **From mark to source:** marks open the brief's own evidence panels. In print, a compact list carries every claim
  once.
- **Held by:** BR-3 (the tutorial is its query file), BR-4 (the map draws the HBM page's figure; the table shows every
  row), BR-7 and BR-13 (print) (`tests/test_brief.py`); `tests/browser/brief.qa.js` (screen at two widths, print on A4
  and Letter, Enter on a diagram mark).

## What the set does not show

The set has no quantity chart, because v1.0 records relations, not quantities (KB-04). It has no map of places and no
overview dashboard. Those, the benchmark's visual quality, hover and interaction are v1.5's subject (D-201).
