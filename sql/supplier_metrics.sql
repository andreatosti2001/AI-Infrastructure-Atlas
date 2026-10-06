-- question: Can the Atlas yet count the suppliers of the parts the AI accelerators on this page
--   incorporate, say where those suppliers are concentrated, or show a part with a single source?
-- population: The parts the accelerators on this page incorporate, counted per accelerator: each
--   accelerator's incorporates link carries its own supplier field, because who makes the memory in one
--   product says nothing about who makes it in another.
-- denominator: The number of those incorporated parts. A supplier metric would need a named supplier for
--   each; this table counts how many have one and how many are unknown, and it computes no metric until
--   at least one is named.
-- assumptions: A supplier is known only when the Atlas records it by name, with the claims behind it.
--   An unknown supplier keeps its own state word. Supply links between companies are counted in a
--   separate column and are never read as the supplier of a part.
-- missing data: Who supplies each part. No source the Atlas holds states it, and the research has not
--   been done.
-- reproduce: python tools/warehouse.py rebuilds this result; the warehouse's checks recompute each count
--   independently, in plain Python, from the records.
-- sensitivity: The first named supplier changes the status of all three metrics; until then nothing a
--   reader could vary changes the answer.
-- does not prove: That a part has no supplier, one supplier or many. An unknown is not a zero, and the
--   absence of a metric says nothing about concentration in the world.
-- reading: One row per supplier metric. parts counts the incorporated parts on the page, one per
--   accelerator and part; parts_supplier_named and parts_supplier_unknown split them by what the Atlas
--   records; unknown_state gives the record's own word for the unknowns. supplies_links counts the company-to-company supply links recorded for those parts,
--   kept apart from the supplier field. status says whether the metric can be computed yet, and needs says
--   what evidence it would take.

-- step: Take the supplier of each part on the page
-- This query reads the result of the links query, accelerator_dependencies, as a table. Each part an
-- accelerator incorporates has a supplier row on its incorporates link: a name when the Atlas records
-- one, otherwise the state word of the unknown. record_id is that link, so each accelerator's part is
-- counted separately even when two accelerators incorporate the same class of part.
WITH suppliers AS (
    SELECT DISTINCT d.record_id, d.to_id AS part_id, d.basis, d.gap_reason
    FROM accelerator_dependencies AS d
    WHERE d.relation = 'supplier'
),

-- step: Count the supply links recorded for those parts
-- A supply link is a separate kind of record: one company supplies an item to another. It is counted in
-- its own column, so a supply link is never mistaken for the supplier of a part, and the other way round.
supply_links AS (
    SELECT count(*) AS n
    FROM relationships AS r
    WHERE r.relation_type = 'supplies'
      AND r.item_state = 'value'
      AND r.item_value IN (SELECT part_id FROM suppliers)
),

-- step: Name the three supplier metrics and the evidence each needs
-- VALUES writes a small table by hand: the three metrics the roadmap asks for, and in plain words what
-- the Atlas would have to record before each could be computed.
metrics AS (
    SELECT * FROM (VALUES
        (1, 'supplier count', 'who supplies each part, named in a source'),
        (2, 'geographic concentration', 'where each named supplier makes the part'),
        (3, 'single-source relationships', 'a source stating that a part has exactly one supplier')
    ) AS m(ordinal, metric, needs)
)

-- step: Decide whether each metric can be computed
-- A metric can be computed only when at least one supplier is named. Until then its status is
-- cannot_be_computed_yet, and the counts beside it show why. string_agg lists the distinct state words
-- of the unknowns in a fixed order. The final ORDER BY fixes the order of the rows.
SELECT m.metric,
       (SELECT count(DISTINCT record_id) FROM suppliers) AS parts,
       (SELECT count(DISTINCT record_id) FROM suppliers WHERE basis <> 'gap') AS parts_supplier_named,
       (SELECT count(DISTINCT record_id) FROM suppliers WHERE basis = 'gap') AS parts_supplier_unknown,
       coalesce((SELECT string_agg(DISTINCT gap_reason, ', ' ORDER BY gap_reason)
                 FROM suppliers WHERE basis = 'gap'), 'not_applicable') AS unknown_state,
       (SELECT n FROM supply_links) AS supplies_links,
       CASE WHEN NOT EXISTS (SELECT 1 FROM suppliers WHERE basis <> 'gap') THEN 'cannot_be_computed_yet'
            ELSE 'computable_not_yet_defined' END AS status,
       m.needs
FROM metrics AS m
ORDER BY m.ordinal
