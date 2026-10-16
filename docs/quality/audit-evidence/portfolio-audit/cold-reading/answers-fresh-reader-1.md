# S24 cold reading: the first fresh reader's answers

**Reader:** a fresh agent (not an agent role), given only `reader-input/` and `form.md` (copied to an isolated folder;
hashes in `input-hashes.txt`), told to open nothing else, run no git and use no web. It wrote nothing to either
repository. Answered on 2026-10-16, before any S24 capability assessment was written. Copied as given.

Read: all of form.md; all of A1 (README), A3 (SQL tutorial) and A4 (D-118); both PNG screenshots; of A2's text, lines 1–974 (scope, executive summary, dependency map, chain table, export-control matrix, key entities, recent changes, gaps, methodology, and the start of the evidence appendix) and lines 3300–3521 (end of the event appendix, the source appendix, the terms). That is about a third of the brief's 3,521 lines. I skimmed none of the middle.

1. It is a small research database about the hardware that AI compute depends on, built so that every link can be traced to a quoted sentence in a registered source. It answers one narrow question: what the memory (HBM) in two accelerators, the NVIDIA H100 and AWS Trainium2, depends on, and who is known to make it. It also covers which recorded US export-control texts name those parts. The README says plainly that it is "deliberately narrow and deep", and it is: two products and one chain.

2. Claims I would want to check: "Every value on its pages can be traced to a sentence in a registered source", "178 of 178 readable passages found", "deliberate breaks (208)", "rebuild byte-identical", CI running browser checks, and "The human reviews every real claim". None of these can be checked from the README alone. It points to files and commands I was not given, and there is no published page (NG-13: "The pages are not published"). The only thing I could check was internal consistency: it first says "five US export-control acts", then adds the two January 2025 rules, which matches the brief's "7 acts recorded". The README also reads more like a changelog (S20.5, D-216, S22.5…) than a front page, which makes these claims harder to weigh.

3. Both the NVIDIA H100 and AWS Trainium2 contain High Bandwidth Memory, which by definition requires 3D die stacking. Who makes that memory is only reported by third parties: SK hynix "primarily" for the H100 as of March 2024 (TrendForce), and Samsung for Trainium2 (SemiAnalysis, December 2025, a source that fails the project's "recognised" criterion). Of the seven US export-control texts recorded, only the December 2024 BIS rule (89 FR 96790) names HBM among the items it controls. Terms like "AI accelerator", "GPU" and "ASIC" were "not matched", and nothing is recorded for 3D die stacking.

4. The "Out of scope" box excludes other accelerators, chain stages beyond memory (packaging, equipment, cloud), destinations, licence policy, thresholds, other jurisdictions, and market share, price or volume. It also says the brief never determines whether any product or firm falls under a text. "Later texts were searched for up to 2026-10-15" and "a change published after that date is unknown". "TSMC fabricates NVIDIA H100" is a recorded gap because the evidence is stale. Nearly every chain row is flagged "one publisher only", and the Trainium2 HBM row is "dated by the day the page was read". It also says "A count counts the Atlas's records, never the world" and "A class with no recorded relationship to a text is unknown to the Atlas, not outside the text."

5. Not as the basis of a decision, only as a well-sourced footnote. Trust goes up because of the verbatim anchors, locators, access timestamps and the careful "stated / reported / inferred / gap" labelling. Gaps are shown rather than hidden. Trust goes down for three reasons:
   - The substantive answer is thin and dated: a 2022 product, a supplier report from 2024, and one weak source.
   - Internal jargon leaks into client text, e.g. "meets §5 only as a DERIVATION, but rel:fabricates is time_sensitive … F-1 fails. The human chose a gap (D-092)". A client cannot evaluate that, and "the human's ruling" is not evidence I can weigh.
   - The export-control matrix shows "Data-centre GPU · refused: term not matched" against the October 2022 rule. A non-expert could read that as "GPUs aren't controlled", even though that rule is widely understood to target advanced chips. The framing note explains what "refused" means, but the grid misleads at a glance.

6. I traced "SK hynix in NVIDIA H100 (reported; historical, to 2024-03)". The evidence appendix gives the TrendForce press release of 2024-03-13 with its URL and a locator ("the paragraph beginning 'The current HBM3 supply', its first sentence"). It also gives the verbatim quote "The current HBM3 supply for NVIDIA's H100 solution is primarily met by SK hynix", the access time, and how the source does against the criteria. So the trace is complete and good. But the quote says "primarily", and the at-a-glance summary and the dependency map drop that qualifier and show SK hynix simply as "supplier". That loses meaning in the place a client is most likely to read.

7. For each product recorded as an instance of the "AI accelerator" class (or of a class directly recorded as a kind of it), the query lists every link around it. That means direct edges, incorporates/requires edges walked outward, the supplier field as its own row, and recorded gaps refused only for stale evidence. Each row gets a basis label, its sources and publishers, its oldest and newest evidence dates, and its caveats. Here the population is two products (H100 via Data-centre GPU, Trainium2 via AI ASIC), giving the 8 rows the brief shows. The subclass test only goes one level ("broader" = AI accelerator). The RECURSIVE part is the dependency walk, not the class hierarchy, which the prose blurs slightly.

8. No. I could follow the logic and check that 8 rows (4 per accelerator) fits the brief's table, but I could not run it. I would need the data/ files, `tools/warehouse.py` to see how JSON becomes tables like `entity_lists`, `identity_basis` and `field_values`, DuckDB 1.5.6, and the result file itself. The tutorial names `sql/results/accelerator_dependencies.json` but shows none of its rows. The input digest is useless to me without the inputs.

9. It does say some limits:
   - "They are dates, not ages: the table never says whether a value is still current."
   - Several publishers on an inferred row "do not confirm one another"; "one publisher is one voice".
   - "This part lists sources; nothing here counts them."

   It fails to say:
   - That a missing row does not mean a missing dependency. The brief says this elsewhere; the tutorial does not.
   - That "reported" does not mean sole or current supplier.
   - That "stated" needs only one FACT among the cited claims, so a row's label can overstate a mixed evidence base.

   The question line promises "how old is the evidence", but the query outputs dates rather than ages, which it admits only at the end.

10. The decision was to load the canonical JSON files into a fresh in-memory DuckDB on every run. Results are committed as JSON with input, query and engine digests. The database file is never committed, DuckDB is pinned at 1.5.6, and the page build reads the result files without importing DuckDB, so pages rebuild without it. Rejected: a committed database file, DuckDB inside the page build, SQLite, DuckDB's own JSON reader, loading staging data, and CSV results. Only one rejection is explained in the record: the JSON reader "infers types and turns state objects into structs". The reasons for rejecting SQLite and the others are not stated here and are presumably in `sql-layer.md`, which I could not see.

11. It suggests a heavily governed build: a human approves named options (H-2) with dates, every new dependency needs a recorded reason (D-003), and checks are numbered (WH-1 to WH-10, PG-7). It also shows strict separation of stages (data, then results, then page) built for reproducibility. The decision, its human approval and the review all fall on the same day, 2026-10-03, and the session codes (S14) hint at fast, AI-agent-driven development with one human approver. That raises my confidence in the process discipline, but it also says the process is heavy relative to a dataset this small.

12.
   - **Domain expertise: shown (narrowly).** A2 makes informed distinctions, e.g. "TSMC 4N" as a process name versus a named fabricator, and company-level 10-K statements versus product-level evidence, but it covers only a few facts.
   - **Data engineering: shown.** A3 exposes a real relational model (entities, claims, citations, candidates, explicit states); the pipeline itself (hashes, rebuild) is only claimed in A1 and A4.
   - **SQL/Python: SQL shown, Python claimed.** A3's recursive CTE query is non-trivial and readable; the Python tools appear only as command names in A1, A2 and A4.
   - **AI governance and agents: claimed.** A1 and A2 mention a "Verifier" and a "Change Detector" and "READ BY THE VERIFIER" stamps, but nothing lets me see or check how the agents behave.
   - **Policy analysis: shown as policy description, not analysis.** A2's export-control matrix and dated events are careful, but the brief refuses by design to interpret or draw implications.
   - **Reproducibility: claimed.** A1, A2 and A3 give digests and `--check` commands and A4 explains the design, but I could run or verify none of it.
   - **Client value: shown.** A2 is the client product itself, so I can judge it, and my judgement is that it is modest: honest but thin, dated and jargon-heavy.
   - **Documentation quality: shown.** A1, A3 and A4 are precise and well cross-referenced, but very dense with internal codes, and A1 reads as a changelog.

13. What would most change my view is evidence that someone outside the project can reproduce a result and finds it correct: a live page, a fresh clone running `check_all.py`, or an independent check of the quoted passages. Right now the strongest claims are self-attested. What I expected and did not find:
   - a plain-language "so what" for a client (implications, what to watch, why these two accelerators);
   - coverage of current-generation accelerators;
   - the actual result rows in the SQL tutorial;
   - a glossary that turns codes like ER-9, F-1 and D-092 into words before they appear in client text.
