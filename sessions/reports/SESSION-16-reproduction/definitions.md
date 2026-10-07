# S16 independent reproduction: the plain definitions given to the reproducing agent

Part B §07 task 3: the agent receives `data/` and, per metric, only the `question`, `population` and
`denominator` lines of its query header (copied verbatim below from `1ca2e89`), never the SQL, the results,
the tests or the pages. Source age's reference date (2026-10-06) is in its own question's words ("a fixed
reference date") only; the agent is told the date, since the page prints it.

## Evidence coverage

- **question:** For each AI accelerator on this page, how do the links the Atlas records around it divide between links a source states, links the Atlas infers, and gaps the Atlas has recorded?
- **population:** The links around each accelerator, exactly as the table of links lists them: one row per accelerator and link. It is a census of what the Atlas has recorded, not of the world's supply chain. A link the Atlas has not recorded is in no row and in no count.
- **denominator:** The number of links the Atlas records around that accelerator. The rows are not independent records: one link can appear under several accelerators, and an unknown supplier is a row of its own that sits on the link it qualifies. The records column says how many distinct records the rows come from.

## Source age (reference date 2026-10-06, as printed on the page)

- **question:** As of a fixed reference date, how old is the newest evidence behind each link around each AI accelerator on this page, and which links rest only on evidence older than the Atlas's 12-month freshness horizon?
- **population:** The links in the table of links, one row per accelerator and link, with the evidence dates that table gives them. A link with nothing to date (an unknown) is listed with no age.
- **denominator:** For a share read from this table, the number of links that have a date. The links with nothing to date are a separate part, never counted as old or as new.

## Supplier metrics (supplier count, geographic concentration, single-source relationships)

- **question:** Can the Atlas yet count the suppliers of the parts the AI accelerators on this page incorporate, say where those suppliers are concentrated, or show a part with a single source?
- **population:** The parts the accelerators on this page incorporate, counted per accelerator: each accelerator's incorporates link carries its own supplier field, because who makes the memory in one product says nothing about who makes it in another.
- **denominator:** The number of those incorporated parts. A supplier metric would need a named supplier for each; this table counts how many have one and how many are unknown, and it computes no metric until at least one is named.
