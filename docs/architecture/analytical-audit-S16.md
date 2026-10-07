# Analytical audit (S16)

**Status:** findings written 2026-10-07; **verdicts decided by the human on 2026-10-07** (H-3, H-4):
coverage modified (D-133), source age modified (D-134), publishers retired (D-135), the supplier metrics kept
(D-136), the reference date moved with each session that rebuilds the pages (D-137), the findings split as
proposed in §8 (D-138). Every finding below is the Atlas's assessment (`INTERPRETATION`) of its own metrics,
never a fact about the world.

- **Session:** S16 · **Kind:** analytical depth audit (PEF §8), the mandatory audit "after the first
  analytical layer" (SPEC §4) · **Milestone:** M4.
- **Scope** (decided at the S16 opening, H-1 A, 2026-10-07): the five metrics and how the research view
  shows them, plus two rulings:
  - D-130, that a metric without data is shown as "cannot be computed yet";
  - D-124, that a page only copies SQL cells or counts its own rows.
- **Base:** `main` @ `1ca2e89`. At the start, in a fresh Python 3.11 virtualenv: 357 tests OK, Gate 0 OK,
  and all three `--check` commands up to date.
- **Evidence kept with the session report:**
  - `sessions/reports/SESSION-16-cold-reading/` (the form, the readers' input, both readers' answers);
  - `SESSION-16-reproduction/` (the definitions given, the script, its output);
  - `SESSION-16-probes/` (the script and its output).
- **Roles:**
  - Analyst: the per-metric answers and the probes;
  - Data Auditor: the reproduction;
  - Knowledge Architect: the findings and the split;
  - QA: the rendered text;
  - Portfolio Reviewer: inactive (H-1 A); its kind of judgement is the Knowledge Architect's.

## In short

| Metric | What the audit found, in one sentence | Recommendation |
|---|---|---|
| **Evidence coverage** | It counts how each accelerator's recorded links split between stated, inferred and gap. Both readers read the counts correctly, but neither understood the "records" line. Someone with only the plain definition got the H100 wrong (5 links, not 4) | **modify:** the records line reworded; the definition says which refused relations become gaps |
| **Source age** | It is correct as a description of dates, but it applies the 12-month horizon to every link. The source policy applies that horizon only to time-sensitive links (who fabricates a product, who supplies a part). So "older than twelve months" reads as "stale" for four links that have no age limit, and its tutorial says so in error | **modify:** the block's note and the tutorial say where the horizon applies |
| **Publishers behind a sourced link** | Its "2" comes only from the one inferred link, whose two publishers back different reasoning steps, never one statement twice. The block counts 6 rows from 5 records without saying so, and computes a per-row count the page never shows. Neither reader could act on it | **retire:** the table already flags "one publisher only" on each row |
| **Supplier count, geographic concentration, single-source relationships** | Both readers read them correctly as unknown, not zero. The three blocks repeat one line word for word, but each "needs" line is different, and no reader was misled | **keep as built** |

**Verdict on PEF §8** (`INTERPRETATION`):

- The Atlas's metrics answer real questions over stated populations. They are reproducible from the
  committed queries, and limited honestly where data is missing.
- The audit found three defects: one rule misapplied in a tutorial, one block outside D-124, and two
  definitions too thin to reproduce from.
- None changes a number. All three are wording or a block's removal.

## 1. Method

1. **Cold readings.** Two fresh agents answered the same seven-question form
   (`SESSION-16-cold-reading/form.md`). Each saw only the rendered page with every tutorial removed, and
   neither saw the other's answers. The first worked from the desktop screenshots and the visible text, the
   second from the mobile screenshots.
   - The human's reading was waived by the human on 2026-10-07 (the report, Deviations). Claude did not
     answer the form, because Claude had read the queries, so its reading would not be cold.
2. **Independent reproduction.** A third agent got only `data/` and each metric's `question`,
   `population` and `denominator` lines (`SESSION-16-reproduction/definitions.md`). It wrote a
   standard-library script and listed every choice the definition left open.
3. **Sensitivity probes.** `SESSION-16-probes/probes.py` copies the repository into a scratch directory,
   plants one change, and rebuilds the results, then the HBM page, then the research view. It records each
   indicator block, or the error that stopped a build.
   - Every planted value is hypothetical. The planted supplier is a placeholder id that names no company.
   - The repository was unchanged afterwards.
4. **The rulings.** D-130 and D-124 are read against the build's code (`tools/build_insight.py`
   `indicators()`, `scope()`, `evidence_index()`) and the rendered text.

## 2. Evidence coverage (`sql/evidence_coverage.sql`)

**Measures.** For each accelerator, the rows of the table of links split by basis:

- stated (at least one cited claim is a `FACT`);
- inferred (no cited claim is);
- gap (an unknown field, or a relation refused only because its evidence is too old).

It also counts how many distinct records those rows come from. Today: Trainium2 2 / 1 / 1 of 4, H100
1 / 1 / 2 of 4, each from 3 records with 1 shared.

**Does not measure:**

- how dependent an accelerator is, or how risky its supply;
- whether a statement is true; stated means one source says it, not that it is confirmed;
- like-for-like documentation. The four links are not the same kinds of link for both accelerators:
  - Trainium2's first link is "Amazon designs" (stated);
  - the H100's first link is "TSMC fabricates" (a gap, evidence not fresh);
  - the H100 has no designs link, because "NVIDIA designs H100" was refused for another reason (`cand-007`,
    `relation_not_stated`), and the first query draws only refusals whose one reason is stale evidence;
  - Trainium2 has no fabrication link at all.

  The nearest wrong reading is that "2 of 4 vs 1 of 4" means Trainium2's chain is better documented on
  equal terms.

**Missing data that could distort it.** If the HBM suppliers were researched, each accelerator could gain a
stated link. Links nobody looked for are in no row. A designer or fabricator link refused for a reason other
than age is invisible here, as `cand-007` and `cand-008` are.

**Selection and survivorship:**

- The two accelerators were chosen for the slice (S11).
- The links are the ones the HBM slice drew: the accelerator's own edges, plus what its incorporated part
  requires. They are not all of an accelerator's dependencies.
- A gap exists only where the Atlas looked. The H100 has one more gap than Trainium2 because research found
  TSMC evidence and refused it as stale. Looking produced a gap; not looking would have produced no row.
- The one inferred link under each accelerator is the same record ("HBM requires 3D die stacking"). S13's
  F-8 found that it restates HBM's definition and carries little independent weight.

**Misleading presentation:**

- **The records line.** "rows drawn from 3 records, of which shared with another accelerator: 1" was
  understood by neither reader (C-1 below).
- **"Gap" covers two different things.** Both readers were surprised that a gap can mean stale evidence as
  well as missing evidence (C-2). The block's split line says "2 gaps" without the two reasons.
- **Ranking.** Both readers concluded that Trainium2 is "somewhat better documented in this dataset". Both
  qualified it at once ("a one-link difference is fragile"). That is a correct reading of the records, not a
  ranking of chips.
- **The unit squares** follow chain position, so they come in a different order for the two chips
  (reader 2). Minor.

**Is the question real?** Yes. A researcher asks how much of a chain rests on a source's own statement
before relying on it, and would use the answer to decide where research is needed.

**Reproduction.** From the plain definition alone:

- Trainium2: exactly 4 / 2 / 1 / 1 / 3 records / 1 shared.
- **H100: 5 links (1 / 1 / 3), 4 records.** The extra row is `cand-007` ("NVIDIA designs H100", refused as
  not stated). Nothing in the population or denominator line says that only relations refused for stale
  evidence become gap rows. The query's header delegates this to "the first query's definitions", which the
  tutorial does not show.
- The reproducer also had to guess:
  - that "stated" means `FACT` only (it also counted `ATTRIBUTION`; no number changes today);
  - how far "around" reaches; two other readings give 3 or 6 links for Trainium2.

**Sensitivity:**

- **P1** (the shared inferred claim re-typed as a `FACT`) moves **both** accelerators at once: Trainium2 to
  3 of 4, H100 to 2 of 4, and "inferred" to 0 for both. One record decides a quarter of each chain.
- **P2** (the H100's recorded gap resolved by a recorded fabrication edge) cannot be shown. Both page builds
  stop:
  - the HBM page is configured with `cand-001` by id (`build_page.py`, `drawn_gaps`);
  - the research view needs an HBM-page panel for every row (E-1).
- Conclusion: the split moves a quarter per link, as the header says. Whether a reader's comparison of the
  two accelerators holds depends on single records.

**PEF §8 header, rechecked:**

| Answer | Verdict |
|---|---|
| question, denominator, assumptions, reproduce, sensitivity, does not prove, reading | correct |
| population | **incomplete** (C-3): does not say which refused relations are rows, or how far "around" reaches |
| missing data | correct, but incomplete in the same way: relations refused for reasons other than age are also not counted |

## 3. Source age (`sql/source_age.sql`)

**Measures.** For each link, the newest evidence date behind it, its age in days at 2026-10-06, and whether
that date is more than 12 months before. Each date is labelled with where it comes from: a claim's as-of
date, a date the source states, or the day a page was read. The block tallies the dated links per
accelerator: Trainium2 2 of 3 older, 1 of 3 only access-dated; H100 3 of 3 older, 0 of 3.

**Does not measure:**

- **Whether a link needs re-checking.** The source policy's 12-month horizon (§12; D-040) applies only to
  `time_sensitive` matrix rows:
  - time-sensitive: `rel:fabricates`, `rel:incorporates.supplier` and `rel:supplies`;
  - `stable`, with "no age limit": `rel:designs`, `rel:incorporates` and `rel:requires`
    (`source-policy.md` lines 219–228).

  Of the five links shown as "older than twelve months", four are stable. The fifth, TSMC fabricates H100,
  is the only time-sensitive one, and it is already a gap *because* it is past the horizon. So the block
  flags, as old, four links the rule does not ask to re-check, plus one the Atlas has already refused.
- Reliability or truth, as the header says.

**Missing data:**

- 14 of 52 sources state no date. Where one is the newest evidence, the age measures the reading.
- The planted publication date (P3) shows how much this matters.

**Selection and survivorship:**

- **Retrieval window.** Every source was retrieved between 2026-09-29 and 2026-10-02. So an access-dated
  link is always 4 to 7 days old at the reference date. Its "recency" is a property of when this research
  was done, not of the evidence.
- **The recorded gap counts as old by construction.** The H100's "3 of 3" includes the recorded gap,
  which was refused precisely for being older than the horizon. Coverage counts it as a gap, and age counts
  it as a dated link (C-5).
- **Unknown rows have no date** and sit outside the denominator, as intended.

**Misleading presentation:**

- **Where the horizon applies.** "Newest evidence older than twelve months" under the heading "Evidence
  age" reads as a staleness finding. Reader 2 asked exactly the audit's question: "why [is] only the TSMC
  link … flagged 'not fresh' when all three H100 links are said to be older than twelve months" (C-4).
- **The heading and the note.** "Evidence age" sits above a note that opens "Dates, not ages" (reader 1),
  and the large tally "means nothing until you read the small text under them" (reader 2) (C-6).
- **The access date.** Both readers caught that Trainium2's one recent date is only an access date. The
  flag works.
- **"As of".** A page rebuilt later, still saying "as of 2026-10-06", would read as stale or as current
  depending on the reader's day (H-4).

**Is the question real?** Partly:

- "How old is the evidence behind each link" is a real descriptive question for anyone deciding what to
  re-check.
- "Which links are past the horizon" is real only for time-sensitive links. Today that means one link,
  already a gap.
- As built, the block answers the second question for every link, which the policy does not ask.

**Reproduction.** From the plain definition:

- Trainium2: 3 dated, 2 beyond, 1 access-dated, 1 undated (equal).
- H100: 4 dated, 4 beyond (the extra row is `cand-007`, as in §2).
- The reproducer had to choose:
  - which of a source's dates is "the" evidence date. It took the newest of any kind, falling back to the
    access date; the query prefers as-of, then stated, then accessed, per citation;
  - whether a month-only date counts from its start or its end. The header's assumptions line says the
    start, but that line was not in the definition given;
  - **which access date for `src-043`.** The source's retrieval says 2026-10-01T20:44Z. The citation's read
    says 2026-10-02T16:00Z, with the same hash. The query uses the source's (C-8).

  No count changes under these choices.

**Sensitivity:**

| Probe | Effect on the block |
|---|---|
| P3: `src-043` given a planted publication date older than the horizon | Trainium2 becomes **3 of 3** older, 0 access-dated, the same as the H100. The only visible difference between the accelerators' age tallies rests on one access date |
| P4: a planted recent date | 2 of 3, 0 access-dated |
| P5: the reference date moved to 2026-10-07 | only "as of" and the ages change |
| P6: one year (2027-10-06) | Trainium2 3 of 3: its access-dated link crosses on 2027-10-02 |

Conclusion: the descriptive reading ("most evidence is over a year old") is robust. The comparison between
the accelerators is not.

**PEF §8 header, rechecked:**

| Answer | Verdict |
|---|---|
| question | **misleading** (C-4): "the Atlas's 12-month freshness horizon" is applied to links the horizon does not govern |
| does not prove | **wrong for stable links** (C-4): "Past the horizon, the freshness rule asks for newer evidence before the value is used again" holds only for time-sensitive links |
| population, denominator, missing data, reproduce, sensitivity, reading | correct |
| assumptions | correct; it omits where the horizon applies |

## 4. Publishers behind a sourced link (presentation tally, `build_insight.py` lines 337–348)

**Measures:**

- "1 to 2" is the smallest and largest number of distinct publishers on a sourced row.
- "4 of 6" is the sourced rows with exactly one publisher.

**Does not measure:**

- **Corroboration.** The block says so ("Listed, never counted as confirmation").
- **More than one source for one statement.** The only rows with 2 publishers are the two copies of the
  inferred link "HBM requires 3D die stacking". Their sources back *different steps* of the reasoning, which
  the first query's own comment says "do not confirm one another".
- **P1 shows the "2" is an artefact of inference.** Re-type that claim as a stated `FACT` citing one
  source, and the block becomes "1" and "6 of 6".

**Missing data and selection:**

- Only sourced rows have publishers. The unknown-supplier rows are outside the denominator.
- The 6 rows include the recorded gap (`cand-001`).
- The 6 rows come from 5 records, and the block does not say so.

**Misleading presentation:**

- Reader 1 worked out the duplication; reader 2 could not. Reader 2 could not tell "the same publisher
  every time" from "one publisher each", or compare the chips.
- Both concluded "independent sourcing is thin". That is right, but the block does not support it: the
  table's per-row flags do.

**Is the question real?** Not as posed:

- Who asks for the range of publisher counts per row, when the block itself disclaims confirmation? The
  real question (which values rest on one publisher only?) is answered row by row.
- The research view and the HBM page each flag "one publisher only" on the four rows concerned
  (`visual-architecture.md` §9). S13's Part 5 already established that no value in the Atlas is
  corroborated.

**D-124:** two departures (C-7, below).

## 5. The three supplier metrics (`sql/supplier_metrics.sql`)

**Measures.** Whether a supplier metric can be computed: the incorporated parts, one per accelerator (2),
how many have a named supplier (0) and how many are unknown (2, `not_researched`), the supply links (0),
and what evidence each metric needs.

**Does not measure:** the number of suppliers, their location or single-sourcing. Both readers said
explicitly "unknown, not zero suppliers" and "no evidence either way".

**Missing data:** who supplies each part. Nothing the Atlas holds states it (a gap, not researched here).

**Selection:** the parts are the ones the slice drew (HBM only).

**Misleading presentation:**

- The three blocks repeat one line word for word. Both readers noticed, and each used the differing
  "needs" line to tell them apart.
- No reader misread the population. S15's "2 of 2" defect stays fixed.
- The amber follows the semantics: gap colour for an unknown (`visual-architecture.md` §3.1, §9).

**Is the question real?** Yes, it is the slice's own question (MASTER §6.3): "who makes it, how
concentrated?". The blocks show the gap where a reader would look for the answer.

**Reproduction:** equal (2 parts, 0 named, 2 `not_researched`, 0 supply links).

**Sensitivity:** P7, one placeholder supplier named. Both builds stop by design:

- the HBM page: "named suppliers need a design before they are drawn";
- the research view: the S15 stop condition.

**PEF §8 header, rechecked:** all eight answers correct.

## 6. The rulings under the metrics (H-1 A)

### D-130: "cannot be computed yet"

**Three blocks or one?** Three blocks are as informative as one: each "needs" line names different
evidence. They are not louder than the evidence, because no reader read a supplier count, a location or a
single source into them. Merging would save space and lose the place where each metric will appear once
computable. **Recommendation: keep.**

**Is it right that the build stops when a supplier is named?** Yes, and P7 confirms both stops fire with
named reasons. Its cost: the session that adds the first supplier evidence must design three metric
presentations, and the HBM page's supplier drawing, before any page builds. That debt is already owned by
that session.

### D-124 as applied

| Number on the page | Kind | Within D-124? |
|---|---|---|
| Coverage counts | cells of `evidence_coverage.json` | yes |
| Coverage unit squares | one mark per drawn row | yes |
| Age tallies ("2 of 3", "1 of 3") | tallies of the age table's drawn rows, denominator printed; no record repeats within one accelerator | yes |
| "as of 2026-10-06" | a cell | yes |
| Supplier blocks | cells; the zeros are never drawn | yes |
| Scope line: accelerators, first and last evidence date | a tally of drawn accelerators; first and last of a shown column | yes |
| Evidence index: "table rows: n" | a tally of drawn rows per record | yes |
| **Publishers "1 to 2"** | first and last of a **per-row count the page computes and never shows** (the table shows the publisher names) | **no** (C-7) |
| **Publishers "4 of 6"** | a tally of drawn rows, but 6 rows from 5 records, and the block does not say so; D-124 requires that "every tally … says when one record appears in several rows" | **no** (C-7) |

## 7. Cold readings compared with each block's intent

Two readers, both fresh agents. Outcomes only.

| Block | Intent | Reader 1 | Reader 2 | Finding |
|---|---|---|---|---|
| Evidence coverage | split of recorded links by basis; records behind rows | **matched** the split; did not follow the records line; puzzled that a link is "gap" for stale evidence | **matched** the split; did not follow the records line; surprised that a gap can mean stale | C-1, C-2 |
| Evidence age | newest evidence date per dated link; the access date flagged | **matched**; read the access date correctly; confused by "Evidence age" vs "Dates, not ages" | **matched**; asked why only TSMC is "not fresh" when all three are older than twelve months; the large tally unreadable alone | C-4, C-6 |
| Publishers | the range of publishers per sourced row; not confirmation | partly: worked out that the 2s are one link twice; concluded vendors describe their own products | **differed:** could not tell same-publisher from one-each; could not compare the chips | C-7 |
| Supplier count | cannot be counted: 2 of 2 parts unknown | **matched**: unknown, not zero | **matched** | — |
| Geographic concentration | cannot be computed; needs locations | **matched** | **matched**; noted the repeated line | — |
| Single-source | cannot be computed; needs a single-source statement | **matched**; noted the repeated line | **matched** | — |
| Together | no ranking of chips; the state of the records | **matched**: "differences reflect how far the Atlas's research has got" | **matched**: "only … the state of the evidence, not the chips" | — |

## 8. Findings

Each finding opens with what a reader would get wrong, or what is missing. The split was proposed by Claude
and ruled by the human as proposed on 2026-10-07 (D-138).

| ID | Finding | Evidence | Split (ruled 2026-10-07, D-138) |
|---|---|---|---|
| C-1 | **A reader cannot tell what "rows drawn from 3 records, of which shared with another accelerator: 1" means.** | both readers, q1; rendered text | blocking: reword the line (coverage, modify) |
| C-2 | **"Gap" means two different things in one count**: nobody has looked (the supplier), and the Atlas looked and refused the evidence as stale (TSMC). The H100 has more gaps partly because more was found. | both readers, q1; `accelerator_dependencies.json` rows 3, 5, 7 | debt: the definition is the first query's (non-goal §08); owner: the human's ruling on a superseding decision, raised again in S16's handoff for S20 (the researcher product) |
| C-3 | **The coverage definition cannot be reproduced on its own**: it does not say that only relations refused for stale evidence become gap rows, nor how far "around" reaches. An independent reader got the H100 as 5 links. | reproduction output; `sql/evidence_coverage.sql` population line | blocking: the header's population line says both (coverage, modify) |
| C-4 | **"Older than twelve months" reads as "needs re-checking" for links the rule exempts.** The 12-month horizon governs only who-fabricates and who-supplies links. Four of the five "older" links are stable, and the fifth is already a gap for that reason. The tutorial states the rule wrongly. | reader 2, q2; `source-policy.md` §12 and lines 219–228; `sql/source_age.sql` question and does-not-prove lines | **blocking:** the block's note and the header say where the horizon applies (source age, modify) |
| C-5 | **The H100's "3 of 3" includes the recorded gap,** which is old by construction. | `source_age.json` row 5 | debt: owner S20 (whether a gap belongs in an age tally is a presentation question for the researcher product); the block's wording is unchanged |
| C-6 | **"Evidence age" over "Dates, not ages", and a large tally unreadable without its small line.** | reader 1 q2, reader 2 q2 | blocking, cheap: rewritten with C-4's note |
| C-7 | **The publishers block computes a per-row count the page never shows, counts 6 rows from 5 records without saying so, and its only "2" is one inferred link's reasoning steps.** | D-124; `build_insight.py` 337–348; probe P1; reader 2 q3 | blocking: retire the block (the table keeps its per-row flags) |
| C-8 | **One source carries two access dates for the same bytes** (`src-043`: retrieval 2026-10-01, citation read 2026-10-02). | `data/sources.json`, `data/claims.json` (`claim-trainium2-hbm-capacity`) | debt: no count changes; owner S22 (engineering audit: which access date is canonical) |
| C-9 | **The coverage comparison is not like for like**: Trainium2's first link is a stated designer, the H100's a stale fabricator; neither chip has both. | `accelerator_dependencies.json` rows 1, 5; `refused_candidates.json` `cand-007`, `cand-008` | debt: needs research (non-goal §08); owner: the session that next adds accelerator links. The "Where they differ" section already shows the difference |
| E-1 | **The H100's most plausible evidence change cannot reach either page without code edits**: both builds stop when `cand-001` is resolved. | probe P2 | debt: owner S22 (alongside `build_page.sql_section`'s fixed path) |
| E-2 | **The probes' own first run crashed the HBM page** on an invalid citation standing, with an unnamed `StopIteration`. The data validators would have refused the value first, but the build gives no named reason. | first probe run (the report) | debt: owner S22 |

Not findings: the readers' cautious comparison of the two chips (both qualified it as a statement about
the records); the access-date flag (both read it right); the supplier blocks (§5).

## 9. Maturity: Analytical depth (PEF §3)

| Side | Rating | Evidence |
|---|---|---|
| **Process:** did analysis evolve from questions rather than decoration? | **3, Controlled** | every metric was defined by question, population and denominator before its query (D-128 to D-131); the human challenged each denominator before explanation (S15); independent computations WH-12 to WH-14 caught a population error before any result was committed; this audit adds unprimed readers, a definition-only reproduction and probes |
| **Outcome:** are metrics reproducible, meaningful, transparent and appropriately limited? | **2, Defined** (3 once C-1, C-3, C-4, C-6 and C-7 are remediated) | reproducible from the queries (WH-12 to WH-14, byte-identical results); limited honestly where data is missing (§5). But one tutorial misstates the rule it invokes (C-4), one definition cannot be reproduced alone (C-3), and one block sits outside D-124 (C-7) |

## 10. Rejected alternatives

| Alternative | Why not |
|---|---|
| Claude answering the cold-reading form | Claude had read the queries; its reading would not be cold |
| Giving the reproducer the assumptions lines as well | Part B §07 task 3 names question, population and denominator; the gap it found is the finding |
| Fixing C-2 or C-9 in the page | both are the first query's definitions or need new data (non-goals §08) |
| Adding a time-sensitivity column to `source_age.sql` | the freshness class lives in `source-policy.md`, not in `data/`; a new SQL input is beyond an audit's remediation. The wording fix is enough for today's links |
| Merging the three supplier blocks | no reader was misled; each block's "needs" differs (§6) |
