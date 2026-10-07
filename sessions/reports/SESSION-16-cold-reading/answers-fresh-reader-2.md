# S16 cold reading: the second fresh reader's answers

**Reader:** a second fresh agent, launched after the human waived their own reading on 2026-10-07 (the
report's Deviations). Given only the mobile screenshots (`mobile-01-top.png`, `mobile-02-indicators.png`,
`mobile-00-full-page.png`) and `desktop-02-indicators.png` of `reader-input/`, and the form. It did not see the
first reader's answers. It wrote nothing to the repository. Answered on 2026-10-07, before any S16 finding was
written. Copied as given.

1. **Evidence coverage.** Each accelerator has four recorded links. For AWS Trainium2, two of them are directly "stated" by a source, one is "inferred" and one is a "gap". For NVIDIA H100, one is stated, one inferred and two are gaps. Comparing with the "What the records show" section, I take the four links to be: incorporates HBM, HBM supplier, HBM requires 3D die stacking, and who acts on the chip (Amazon designs it, TSMC fabricates it). I would conclude that Trainium2 is somewhat better documented in this dataset, but four links each is very little. Three things were unclear to me:
   - the square icons seem to come in a different order for the two chips;
   - I don't know how "3 records, of which shared with another accelerator: 1" relates to the 4 links;
   - the TSMC link is labelled "gap" with "evidence not fresh". That suggests "gap" can mean stale evidence as well as missing evidence, which I would not have assumed.

2. **Evidence age as of 2026-10-06.** I read it as: of each accelerator's three dated links (I assume the unresearched supplier link has no date), the newest evidence is more than a year old for 2 of 3 on Trainium2 and 3 of 3 on H100. One Trainium2 date is only the day someone read an undated web page, so the real date of that evidence is unknown and could be older. I would conclude that most of this evidence is over a year old and H100's is entirely so. The big headline numbers ("2 of 3", "3 of 3") mean nothing until you read the small text under them. It is also unclear why only the TSMC link is flagged "not fresh" when all three H100 links are said to be older than twelve months.

3. **Publishers behind a sourced link.** I take "1 to 2" to mean each sourced link has between one and two publishers behind it. "4 of 6 sourced rows rest on one publisher" seems to mean 4 of the 6 rows (probably 3 per accelerator) have only a single publisher. I can't tell whether that is the same publisher every time, or just one publisher each. "Listed, never counted as confirmation" seems to say a second publisher doesn't count as corroboration, but I'm not sure what that implies here. I would conclude that independent sourcing is thin. The block doesn't split this by accelerator, so I can't compare the two chips.

4. **Supplier count (cannot be computed yet).** Nobody has yet researched who supplies the High Bandwidth Memory for either accelerator (2 of 2 not researched), so the number of suppliers cannot be stated. I would read this as "unknown", not "zero suppliers". It is the central gap on the page, matching the "who makes it: not researched" in the headline.

5. **Geographic concentration (cannot be computed yet).** This needs to know where each named supplier makes the memory. Since no supplier is named yet, nothing can be said about where the memory is made. Its main line is word-for-word the same as the supplier-count block, which tells me it is blocked by the same gap, plus a further missing piece of information (manufacturing locations).

6. **Single-source relationships (cannot be computed yet).** This would need a source saying a part has exactly one supplier. Since suppliers aren't researched, nothing can be said about single-sourcing either way. I would not conclude that there is single-sourcing, or that there isn't.

7. **The indicators together.** The only comparison possible is about the state of the evidence, not the chips themselves. Trainium2's records are slightly more complete and slightly less old than H100's. Neither tells us who makes the memory, where, or how concentrated supply is. With four links per chip, a one-link difference is fragile, and I would not draw any supply-chain or risk conclusion about either accelerator from this page.
