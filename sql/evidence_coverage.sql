-- question: For each AI accelerator on this page, how do the links the Atlas records around it divide
--   between links a source states, links the Atlas infers, and gaps the Atlas has recorded?
-- population: The links around each accelerator, exactly as the table of links lists them: one row
--   per accelerator and link. Around means the edges that start or end at the accelerator, plus the
--   incorporates and requires edges reached outward from the parts it incorporates. An unknown field on
--   an edge (who supplies the part) is a row of its own. A relation the Atlas considered and refused is a
--   row, as a gap, only when its one reason is that its evidence is too old; refused for any other reason,
--   it is in no row. It is a census of what the Atlas has recorded, not of the world's supply chain. A
--   link the Atlas has not recorded is in no row and in no count.
-- denominator: The number of links the Atlas records around that accelerator. The rows are not
--   independent records: one link can appear under several accelerators, and an unknown supplier is a
--   row of its own that sits on the link it qualifies. The records column says how many distinct
--   records the rows come from.
-- assumptions: A link is stated when at least one claim it cites is a FACT, inferred when every cited
--   claim is the Atlas's reasoning, and a gap when the Atlas records that it does not know. These are the
--   first query's definitions, used unchanged. Every link weighs the same.
-- missing data: The suppliers of the memory are not researched, so each accelerator has a gap that a
--   piece of research could turn into a stated link. Links nobody has looked for are not counted at all.
-- reproduce: python tools/warehouse.py rebuilds this result from the records; the warehouse's checks
--   recompute it independently, in plain Python and without SQL.
-- sensitivity: With four links per accelerator, one new link or one gap resolved moves the split by a
--   quarter. Small counts: read the numbers, not a proportion.
-- does not prove: It does not measure how dependent an accelerator is, how risky its supply is, or how
--   reliable a source is. A stated link rests on one source's statement; stated is not confirmed.
-- reading: One row per accelerator. links is the number of rows the table of links holds for it;
--   stated, inferred and gap split that number and always add up to it. records counts the distinct
--   records behind those rows, and shared counts the records that also appear under another accelerator.

-- step: Take the table of links
-- This query reads the result of the links query, accelerator_dependencies, as if it were a table:
-- the warehouse turns each earlier query into a view before it runs this one. Building on that result,
-- instead of repeating its definitions, means the counts below describe exactly the rows the page draws.
WITH links AS (
    SELECT accelerator, accelerator_id, record_id, basis
    FROM accelerator_dependencies
),

-- step: Find the records shared between accelerators
-- A record is shared when the table lists it under more than one accelerator, as happens when two
-- accelerators incorporate the same part and that part's own needs are walked for each of them.
shared AS (
    SELECT record_id
    FROM links
    GROUP BY record_id
    HAVING count(DISTINCT accelerator_id) > 1
)

-- step: Count each accelerator's links by basis
-- count(*) counts every row, and each FILTER keeps only the rows of one basis, so stated, inferred and
-- gap add up to links. A gap is counted as a gap, in its own column: it is never left out and never
-- turned into a zero of something else. The final ORDER BY fixes the order of the rows.
SELECT l.accelerator,
       l.accelerator_id,
       count(*) AS links,
       count(*) FILTER (WHERE l.basis = 'stated') AS stated,
       count(*) FILTER (WHERE l.basis = 'inferred') AS inferred,
       count(*) FILTER (WHERE l.basis = 'gap') AS gap,
       count(DISTINCT l.record_id) AS records,
       count(DISTINCT l.record_id) FILTER (WHERE l.record_id IN (SELECT record_id FROM shared)) AS shared
FROM links AS l
GROUP BY l.accelerator, l.accelerator_id
ORDER BY l.accelerator, l.accelerator_id
