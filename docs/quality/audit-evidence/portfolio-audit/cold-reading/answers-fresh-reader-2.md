# S24 cold reading: the second fresh reader's answers

**Reader:** a second fresh agent, told to read as a hiring manager for a technology-policy research and data role,
given only `reader-input/` and `form.md` (the same isolated folder and hashes as the first reader), told to open
nothing else, run no git and use no web. It did not see the first reader's answers. It wrote nothing to either
repository. Answered on 2026-10-16, before any S24 capability assessment was written. Copied as given.

Read: form.md. All of A1, A3 and A4. Both screenshots. Of the brief text (3,521 lines) I read lines 1–974 in full: the scope, executive summary, map, chain table, export-control matrix, entities, recent changes, gaps, methodology and the start of the evidence appendix. I also read lines ~1640–1760 (the 89 FR 96790 act record), ~2860–2940 (refused policy candidates), 3300–3521 (the source appendix and terms), and ran keyword searches for "HBM", "3A090.c" and "96790". That is roughly 40% of the brief.

1. It is a research database plus generated web pages on the physical supply chain behind AI chips. Every link is tied to a quoted sentence in a registered source. It is kept deliberately narrow: it answers "What does an AI accelerator's memory depend on, and who is known to make it?" for two chips only, the NVIDIA H100 and AWS Trainium2. It also has a policy layer that records which US export-control texts name those parts. The opening paragraph explains this well. After that the README turns into an internal changelog ("S21.5", "D-209", "NG-13", "M7"), and I had to work to separate what the product is from how it was managed.

2. The claims I would want to check:
   - "Every value on its pages can be traced to a sentence in a registered source."
   - "The human reviews every real claim."
   - Pages "rebuild byte-identical."
   - "28 planted data faults," "deliberate breaks (208)," and "178 of 178 readable passages found."
   - "CI runs the unit tests… on every push."

   I could check none of this from the README alone. It is prose and file links with no CI badge, no sample output and no live URL. It also says "The pages are not published (NG-13)", so a reviewer cannot just click through to the product. Some numbers are hard to reconcile without context: the README speaks of "five US export-control acts" and later of two more, and the brief shows "7 acts".

3. The question: what does the memory in an AI accelerator depend on, who supplies it, and which recorded US export-control texts name those parts. A client could repeat the answer like this:
   - Both the H100 and Trainium2 use High Bandwidth Memory (HBM), according to the vendors' own documents. HBM needs 3D die stacking, but that step is the project's own inference.
   - The supplier is known only from third-party reports: SK hynix for the H100 (TrendForce, valid only up to March 2024) and Samsung for Trainium2 (SemiAnalysis, a source that does not meet the project's own "recognised" test).
   - Of the seven US texts recorded, only BIS's December 2024 rule (89 FR 96790) names HBM among the items it controls. GPUs, ASICs and accelerators were "refused: term not matched".

   Honestly, the answer is thin. For the supplier part, it amounts to "two analyst reports, one of them sub-par".

4. The limits I noticed:
   - The "Out of scope" box: other accelerators, packaging, equipment, servers, cloud, destinations, licence policy, thresholds, exemptions, other jurisdictions, and market share, price or volume.
   - "Whether any product, firm or transaction falls under a text: the Atlas never makes that determination."
   - The search for later texts stops at 2026-10-15.
   - "TSMC fabricates H100" is a recorded gap, not a link, because the evidence is "not fresh".
   - Every chain row carries "one publisher only".
   - The Trainium2 HBM row is "dated by the day the page was read".
   - "HBM requires 3D die stacking" rests on the Atlas's own definitions.
   - "A count counts the Atlas's records, never the world."
   - "A class with no recorded relationship to a text is unknown to the Atlas, not outside the text."
   - "What this brief does not track" adds supplier changes after the evidence dates.

   The limits are stated more thoroughly than in most professional briefs I have seen.

5. I would rely on it as a well-sourced fact sheet. I would not rely on it to prepare a decision.

   What raises trust: verbatim quotes, page-level locators, access timestamps, primary govinfo.gov texts for the rules, and explicit refusals. For example, it declines to say an October 2023 rule controls HBM because the rule mentions HBM only in "red flag 19".

   What lowers trust:
   - **Coverage.** It covers two chip generations that are not current in late 2026, and every row has a single source.
   - **No decision content.** The "Executive summary" is a list of record groupings, not findings ("8 of 8 rows of the dependency result shown" means nothing to a client).
   - **Jargon in client text.** Phrases such as "F-1 fails", "§12 horizon", "D-073 logic" and "ER-9" appear in client-facing text.
   - **First screen.** On both desktop and mobile it shows only the title, a disclaimer, framing boxes and navigation, with no finding.
   - **AI Diffusion rule status.** The matrix shows 90 FR 4544 (the AI Diffusion rule) as "has taken effect" with no flag in the matrix itself. BIS announced its rescission and non-enforcement in May 2025. The brief records that further down, but a policy reader scanning the matrix could be misled.
   - **Literal term matching.** Refusing to link "AI accelerator" to rules that control "co-processors/accelerators" (because that term is broader) is defensible but counter-intuitive for a client. It needs a plain-language explanation next to the matrix.

6. I traced "SK hynix in NVIDIA H100 (reported; historical, to 2024-03)". The evidence appendix gives:
   - an ATTRIBUTION claim with the verbatim quote "The current HBM3 supply for NVIDIA's H100 solution is primarily met by SK hynix";
   - the source (TrendForce Press Center), its URL, the locator "the paragraph beginning 'The current HBM3 supply', its first sentence", publication date 2024-03-13 and access date 2026-10-07;
   - the source-policy criteria it does and does not meet, and a human-review date.

   So the trace is complete within the brief, though I could not open the URL to confirm the quote. One small point: the source says "primarily", and the summary line drops that word. The claim text keeps it, but the headline compresses it. I also traced the HBM / 89 FR 96790 link to a quoted sentence ("BIS is adding a new ECCN control on HBM stacks… to ECCN 3A090.c", p.10).

7. For every product recorded as an instance of the "AI accelerator" class (or one of its subclasses), the query lists every recorded link around it:
   - direct edges (designs, fabricates, incorporates);
   - incorporates/requires edges walked outward from its parts;
   - supplier fields as rows of their own;
   - unknown values as "gap" rows;
   - candidate links that were refused only because the evidence was too old, as "recorded gap" rows.

   For each row it assigns a basis (stated, reported, inferred or gap), the oldest and newest evidence dates and what each date is based on, publishers, unmet source criteria, and whether the row rests on the Atlas's own interpretation. The population is the Atlas's canonical records only, which in practice is the two accelerators and 8 rows.

8. No, I could not reproduce or check the result. I could follow the logic, and the step-by-step explanations are clear, but:
   - The tables it queries (entities, entity_lists, identity_basis, field_values, candidate_endpoints and so on) are built from the JSON files by a loader that is not shown. I cannot tell how the JSON maps to these tables.
   - The data itself is not given; there is only an input digest I cannot check against anything.
   - It needs a DuckDB environment and the repository.
   - It does not show the output it produced; I had to assume the brief's chain table is that output.
   - The only check offered is a command (`python tools/warehouse.py --check`), which confirms the committed result equals a fresh run, not that it is correct.

   I could still desk-check some logic. The rule "stated if any cited claim is a FACT" means a row labelled "stated" can include weaker claims. That is defined, but a client could easily miss it.

9. It says explicitly:
   - "They are dates, not ages: the table never says whether a value is still current."
   - On an inferred row, two publishers "do not confirm one another, and one publisher is one voice."
   - The evidence step "lists sources; nothing here counts them."
   - Refused candidates for reasons other than old evidence are left out.

   It does not say, in the tutorial itself:
   - that the result covers only what the Atlas has recorded, not the real supply chain;
   - that "stated" usually means stated by an interested party (the vendor itself), not independently confirmed;
   - that two accelerators is far too small a population for any comparative conclusion.

10. The decision (D-118, accepted by the human on 2026-10-03):
    - The canonical JSON files (never the staging area) are loaded into a fresh in-memory DuckDB on every run.
    - Every SQL query runs, and each result is committed as JSON with the digests of its inputs, the query and the engine version.
    - The database file is never committed, and the loader refuses to save one inside the repository.
    - DuckDB 1.5.6 is pinned.
    - The page build reads the result files and never imports DuckDB, so pages rebuild byte-identically without it.

    Rejected: a committed database file, DuckDB inside the page build, SQLite, DuckDB's own JSON reader, loading staging records, and CSV results.

    The context gives the reason: all metrics must be regenerable from versioned inputs, and new dependencies need a recorded justification. But only one rejection has a stated reason: the JSON reader "infers types and turns state objects into structs". SQLite and the page-build option are dismissed by reference only ("H-2 B", "H-2 C"), so a reader cannot evaluate those choices.

11. It shows a disciplined, governance-heavy process:
    - numbered decisions that amend earlier ones (D-003, D-026);
    - named checks (WH-1 to WH-10, PG-7, PG-11);
    - a minimal-dependency policy;
    - a clear separation between canonical data, derived results and rendered pages.

    It also suggests the work was done in fast "sessions" (S14 here; the README reaches S24 and D-221 within about two weeks), mostly by AI agent roles ("Verifier", "Change Detector", "Client Output role") under human approval gates. As a hiring manager, I would immediately want to know which judgements were the candidate's own and which were an agent's. The record style also trades readability for traceability: it is precise but opaque without the rest of the log.

12. Capabilities:
    - **Domain expertise: shown, narrowly.** A2's refused-candidate notes show close reading of BIS texts and semiconductor sources (HBM as a "red flag" feature vs. a controlled 3A090.c item, "TSMC 4N" naming the process rather than the manufacturer). Breadth and market judgement are not visible.
    - **Data engineering: shown in design, claimed in operation.** A3's schema and query and A4's pipeline decision show the design; that the pipeline runs and rebuilds byte-identically is only claimed in A1.
    - **SQL/Python: SQL shown, Python claimed.** A3 is a non-trivial recursive-CTE query I could read; the Python tools are only listed in A1.
    - **AI governance and agents: claimed.** A1 and A2 mention Verifier, Change Detector and Client Output roles, but nothing shows how the agents work or are constrained. The governance subject matter (US AI-chip export controls) is shown as description in A2.
    - **Policy analysis: not visible.** A2 deliberately "describes, never advises" and offers no analysis of consequences, exposure or trends; what is shown is careful policy description.
    - **Reproducibility: claimed.** A1, A2 and A3 give digests and `--check` commands, and A4 describes the mechanism, but nothing I was given let me run or verify it.
    - **Client value: shown, weakly.** A2 is a real, printable client brief with exemplary sourcing. Its findings are thin and its first screen and summary do not tell a client what matters.
    - **Documentation quality: shown.** A1, A3 and A4 are thorough and precise. The A3 tutorial is genuinely good, but A1 and the brief are dense with internal codes that a newcomer cannot decode.

13. What would most change my view: seeing the system run, through a published brief or a CI run log, plus a one-page note separating what the candidate decided from what AI agents produced. Today the strongest capability claims (tests, deliberate breaks, byte-identical rebuilds, human review) are all claimed and not shown.

    What I expected and did not find:
    - an actual "so what" analysis, for example concentration of HBM supply in Korea and what the December 2024 HBM control implies;
    - current-generation products;
    - a plain-language README summary free of session and decision codes;
    - a first screen that leads with the finding instead of disclaimers;
    - the two SQL metrics the README mentions (evidence coverage and source age), which do not appear in what I was given.
