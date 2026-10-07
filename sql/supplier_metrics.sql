-- question: Can the Atlas yet count the suppliers of the parts the AI accelerators on this page
--   incorporate, say where those suppliers are concentrated, or show a part with a single source?
-- population: The parts the accelerators on this page incorporate, counted per accelerator: each
--   accelerator's incorporates link carries its own supplier field, because who makes the memory in one
--   product says nothing about who makes it in another.
-- denominator: The number of those incorporated parts. A supplier metric needs, for each part, what its
--   needs line says: the full set of its suppliers, where each makes the part, or a statement that it has
--   exactly one. This table counts how many parts have a supplier stated by a party, how many have one
--   reported by a third party, and how many are unknown, and it computes no metric until those needs are
--   met.
-- assumptions: A supplier is known only when the Atlas records it by name, with the claims behind it. It is
--   stated when a party's own statement names it, and reported when only a third party does (source-policy
--   §7.1). A named supplier is one supplier, not the full set: neither kind of statement says it was the
--   only one. An unknown supplier keeps its own state word. Supply links between companies are counted in
--   a separate column and are never read as the supplier of a part.
-- missing data: For each part, the full set of its suppliers, where each makes it, and whether it has
--   exactly one. No source the Atlas holds states any of them.
-- reproduce: python tools/warehouse.py rebuilds this result; the warehouse's checks recompute each count
--   independently, in plain Python, from the records.
-- sensitivity: A source stating a part's full set of suppliers, their locations, or a single supplier would
--   change a metric's status; a further named supplier changes only the counts.
-- does not prove: That a part has no supplier, one supplier or many. A named or reported supplier is not
--   the only supplier, an unknown is not a zero, and the absence of a metric says nothing about
--   concentration in the world.
-- reading: One row per supplier metric. parts counts the incorporated parts on the page, one per
--   accelerator and part; parts_supplier_stated, parts_supplier_reported and parts_supplier_unknown split
--   them by what the Atlas records; unknown_state gives the record's own word for the unknowns.
--   supplies_links counts the company-to-company supply links recorded for those parts, kept apart from
--   the supplier field. status says whether the metric can be computed yet, and needs says what evidence
--   it would take.

-- step: Take the supplier of each part on the page
-- This query reads the result of the links query, accelerator_dependencies, as a table. Each part an
-- accelerator incorporates has a supplier row on its incorporates link: a named supplier, with the basis
-- of the claims behind it, or the state word of the unknown. record_id is that link, so each accelerator's
-- part is counted separately even when two accelerators incorporate the same class of part.
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
        (1, 'supplier count', 'the full set of suppliers of each part, named in a source'),
        (2, 'geographic concentration', 'where each named supplier makes the part'),
        (3, 'single-source relationships', 'a source stating that a part has exactly one supplier')
    ) AS m(ordinal, metric, needs)
)

-- step: Count the parts by what the Atlas records, and keep every metric uncomputable
-- A part counts as stated when a party's statement names its supplier, as reported when only a third
-- party does, and as unknown when the field holds a state. No record kind yet holds a part's full set of
-- suppliers, their locations or a single-supplier statement, so no metric's needs can be met and every
-- status is cannot_be_computed_yet. string_agg lists the distinct state words of the unknowns in a fixed
-- order. The final ORDER BY fixes the order of the rows.
SELECT m.metric,
       (SELECT count(DISTINCT record_id) FROM suppliers) AS parts,
       (SELECT count(DISTINCT record_id) FROM suppliers WHERE basis = 'stated') AS parts_supplier_stated,
       (SELECT count(DISTINCT record_id) FROM suppliers WHERE basis = 'reported') AS parts_supplier_reported,
       (SELECT count(DISTINCT record_id) FROM suppliers WHERE basis = 'gap') AS parts_supplier_unknown,
       coalesce((SELECT string_agg(DISTINCT gap_reason, ', ' ORDER BY gap_reason)
                 FROM suppliers WHERE basis = 'gap'), 'not_applicable') AS unknown_state,
       (SELECT n FROM supply_links) AS supplies_links,
       'cannot_be_computed_yet' AS status,
       m.needs
FROM metrics AS m
ORDER BY m.ordinal
