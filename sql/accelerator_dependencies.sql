-- question: For each AI accelerator on this page, which links does the Atlas record around it, on what
--   basis (stated by a source, inferred by the Atlas, or a known gap), and how old is the evidence
--   behind each link?
-- reading: Each row is one link around one accelerator. The basis says how the Atlas knows it:
--   stated (a cited claim is a FACT), inferred (every cited claim is the Atlas's reasoning), or gap
--   (the Atlas records that it does not know, and the gap reason says why, in the record's own words).
--   The two evidence dates are the oldest and newest dates of the evidence the row rests on, dated as
--   the freshness rule dates them; not applicable means there is nothing to date. They are dates, not
--   ages: the table never says whether a value is still current. Publishers lists every publisher
--   behind the row's evidence. On an inferred row, two publishers back different steps of the
--   reasoning; they do not confirm one another, and one publisher is one voice. A row that rests on the Atlas's own
--   interpretation includes the Atlas's working definitions in its reasoning. Party standing
--   unchecked lists sources whose publisher is not linked to a company record. The IDs lead back to
--   the edge or candidate, its claims and its sources.

-- step: Find the accelerators
-- A product counts as an AI accelerator when it is recorded as an instance of the AI accelerator
-- class, or of a class recorded as a kind of it. The join to identity_basis keeps the claim that
-- supports that membership, so every row can show why its product is on the list. The word
-- RECURSIVE at the top allows a later part of the query to refer to itself.
WITH RECURSIVE accelerators AS (
    SELECT p.id AS accelerator_id,
           p.name AS accelerator,
           io.value AS accelerator_class,
           b.claim_id_value AS accelerator_class_claim
    FROM entities AS p
    JOIN entity_lists AS io
      ON io.entity_id = p.id AND io.field = 'instance_of'
    JOIN identity_basis AS b
      ON b.kind = 'instance_of_basis' AND b.record_value = p.id AND b.class_value = io.value
    WHERE p.type = 'product'
      AND (io.value = 'component-ai-accelerator'
           OR EXISTS (SELECT 1 FROM entity_lists AS k
                      WHERE k.entity_id = io.value AND k.field = 'broader'
                        AND k.value = 'component-ai-accelerator'))
),

-- step: Take the edges that touch each accelerator
-- An edge whose source or target is the accelerator is a direct link: who designs or makes it, and
-- what it incorporates. Such a row is reached directly, and its depth is one.
direct_links AS (
    SELECT a.accelerator_id, r.id AS record_id, 'direct' AS reached_through, 1 AS depth
    FROM accelerators AS a
    JOIN relationships AS r
      ON a.accelerator_id IN (r.source_entity, r.target_entity)
),

-- step: Walk outward from what each accelerator contains
-- Starting from each part an accelerator incorporates, this part follows incorporates and requires
-- edges outward, one step per round, and repeats until a round finds no new edge. The first half
-- (above UNION ALL) takes the first step; the second half takes each next step from the last one.
-- reached_through keeps the accelerator's own edge, so every row says how it was reached. The depth
-- limit stops the walk even if the data ever held a loop.
walked_links AS (
    SELECT d.accelerator_id, r.id AS record_id, d.record_id AS reached_through, 2 AS depth,
           r.target_entity AS frontier
    FROM direct_links AS d
    JOIN relationships AS start
      ON start.id = d.record_id AND start.relation_type = 'incorporates'
     AND start.source_entity = d.accelerator_id
    JOIN relationships AS r
      ON r.source_entity = start.target_entity AND r.relation_type IN ('incorporates', 'requires')
    UNION ALL
    SELECT w.accelerator_id, r.id, w.reached_through, w.depth + 1, r.target_entity
    FROM walked_links AS w
    JOIN relationships AS r
      ON r.source_entity = w.frontier AND r.relation_type IN ('incorporates', 'requires')
    WHERE w.depth < 10
),

-- step: Turn each edge into a row
-- Every link found so far becomes a row with its two ends, its relation and the claims it cites.
-- position orders the rows the way the page's chain reads: links into the accelerator first (1),
-- then what it incorporates (2), then what those parts require (4 and beyond).
edge_rows AS (
    SELECT l.accelerator_id, l.record_id, l.reached_through,
           CASE WHEN r.target_entity = l.accelerator_id THEN 1
                WHEN r.source_entity = l.accelerator_id THEN 2
                ELSE 2 + l.depth END AS position,
           r.source_entity AS from_id, r.relation_type AS relation, r.target_entity AS to_id,
           'edge' AS row_kind, 'not_applicable' AS gap_reason,
           (SELECT list(rc.claim_id ORDER BY rc.claim_id)
            FROM relationship_claims AS rc WHERE rc.relationship_id = r.id) AS claim_ids
    FROM (SELECT accelerator_id, record_id, reached_through, depth FROM direct_links
          UNION ALL
          SELECT accelerator_id, record_id, reached_through, depth FROM walked_links) AS l
    JOIN relationships AS r ON r.id = l.record_id
),

-- step: Give each unknown on an edge a row of its own
-- An edge can hold a field (who supplies the part) as an explicit state instead of a value, for
-- example not_researched when no source has been checked. That unknown becomes its own row, with
-- basis gap and the state word as its gap reason: never a blank and never a zero. A supplier the
-- Atlas does record would become a row too, with the claims of that assertion. coalesce turns "no
-- claims" into an empty list rather than NULL.
field_rows AS (
    SELECT e.accelerator_id, e.record_id, e.reached_through, e.position + 1 AS position,
           CASE WHEN f.assertion_state = 'value' THEN f.assertion_value ELSE f.assertion_state END AS from_id,
           f.field AS relation, e.to_id,
           CASE WHEN f.assertion_state = 'value' THEN 'assertion' ELSE 'unknown' END AS row_kind,
           CASE WHEN f.assertion_state = 'value' THEN 'not_applicable' ELSE f.assertion_state END AS gap_reason,
           coalesce((SELECT list(fc.claim_id ORDER BY fc.claim_id)
                     FROM field_value_claims AS fc
                     WHERE fc.record_id = f.record_id AND fc.field = f.field AND fc.ordinal = f.ordinal),
                    []::VARCHAR[]) AS claim_ids
    FROM edge_rows AS e
    JOIN field_values AS f ON f.record_id = e.record_id
),

-- step: Add the recorded gaps
-- A refused candidate is a relation the Atlas considered and chose not to record. One kind belongs
-- in this table: a candidate about the accelerator whose only reason is that its evidence is too old
-- to use. A claim the Atlas holds does state that relation, so the gap is known and dated.
-- Candidates refused for any other reason are left out, because no evidence states them.
gap_rows AS (
    SELECT a.accelerator_id, c.id AS record_id, 'direct' AS reached_through, 1 AS position,
           CASE WHEN s.entity_state = 'value' THEN s.entity_value ELSE s.entity_state END AS from_id,
           t.relation_type AS relation, a.accelerator_id AS to_id,
           'recorded_gap' AS row_kind, 'evidence_not_fresh' AS gap_reason,
           coalesce((SELECT list(k.claim_id_value ORDER BY k.claim_id_value)
                     FROM candidate_considered AS k
                     WHERE k.candidate_id = c.id AND k.claim_id_state = 'value'),
                    []::VARCHAR[]) AS claim_ids
    FROM accelerators AS a
    JOIN candidate_endpoints AS target
      ON target.side = 'target' AND target.entity_value = a.accelerator_id
    JOIN refused_candidates AS c ON c.id = target.candidate_id
    JOIN candidate_endpoints AS s ON s.candidate_id = c.id AND s.side = 'source'
    JOIN candidate_relation_types AS t ON t.candidate_id = c.id
    WHERE (SELECT list(cr.reason ORDER BY cr.reason)
           FROM candidate_reasons AS cr WHERE cr.candidate_id = c.id) = ['evidence_not_fresh']
),

-- step: Put the three kinds of row together
-- UNION ALL stacks the edge rows, the unknowns and the recorded gaps into one list. row_key joins the
-- columns that identify a row into one text value, so the next steps can attach evidence to it.
all_rows AS (
    SELECT *, concat_ws('|', accelerator_id, record_id, gap_reason, from_id) AS row_key
    FROM (SELECT * FROM edge_rows
          UNION ALL SELECT * FROM field_rows
          UNION ALL SELECT * FROM gap_rows)
),

-- step: Follow each row's claims down to their sources
-- A claim either cites sources itself or is reasoned from other claims, its inputs. Starting from the
-- claims a row cites, this part keeps adding input claims until no claim has an input left to add. UNION (without ALL)
-- drops repeats, which also ends the walk. Every claim on the way is kept, so the final step can see
-- whether any of them is the Atlas's own interpretation.
reached AS (
    SELECT r.row_key, unnest(r.claim_ids) AS claim_id
    FROM all_rows AS r
    UNION
    SELECT x.row_key, i.input_claim_id
    FROM reached AS x
    JOIN claim_inputs AS i ON i.claim_id = x.claim_id
),

-- step: Date each piece of evidence
-- The freshness rule defines a citation's evidence date: the claim's as-of date if it has one;
-- otherwise the latest date the source states for itself; otherwise the day the source was accessed.
-- A partial date such as 2021-02 is kept as written and sorts at the start of its period.
evidence AS (
    SELECT x.row_key, ct.source_id, ct.standing, s.publisher, s.publisher_entity_state,
           CASE WHEN cl.as_of_state = 'value' THEN cl.as_of_value
                WHEN s.stated_dates_state = 'value'
                     THEN (SELECT max(d.date) FROM source_dates AS d WHERE d.source_id = s.id)
                ELSE substr(s.accessed_at, 1, 10) END AS evidence_date
    FROM reached AS x
    JOIN claims AS cl ON cl.id = x.claim_id
    JOIN citations AS ct ON ct.claim_id = x.claim_id
    JOIN sources AS s ON s.id = ct.source_id
)

-- step: One line per link, with its evidence summarised
-- For each row: its basis, the names of both ends, the oldest and newest evidence date, its sources
-- and publishers, and its caveats. The basis is stated when at least one claim the row cites is a
-- FACT, inferred when no cited claim is, and gap for an unknown or a recorded gap. Each list is sorted inside
-- its aggregate, and the final ORDER BY fixes the order of the rows, so every run gives the same
-- bytes.
SELECT a.accelerator,
       a.accelerator_id,
       a.accelerator_class,
       a.accelerator_class_claim,
       r.position,
       r.from_id,
       coalesce(ef.name, r.from_id) AS from_name,
       r.relation,
       r.to_id,
       coalesce(et.name, r.to_id) AS to_name,
       CASE WHEN r.row_kind IN ('unknown', 'recorded_gap') THEN 'gap'
            WHEN EXISTS (SELECT 1 FROM claims AS cl
                         WHERE list_contains(r.claim_ids, cl.id) AND cl.claim_type = 'FACT') THEN 'stated'
            ELSE 'inferred' END AS basis,
       r.gap_reason,
       r.record_id,
       r.reached_through,
       r.claim_ids,
       coalesce((SELECT list(DISTINCT e.source_id ORDER BY e.source_id)
                 FROM evidence AS e WHERE e.row_key = r.row_key), []::VARCHAR[]) AS source_ids,
       coalesce((SELECT list(DISTINCT e.publisher ORDER BY e.publisher)
                 FROM evidence AS e WHERE e.row_key = r.row_key), []::VARCHAR[]) AS publishers,
       coalesce((SELECT min(e.evidence_date) FROM evidence AS e WHERE e.row_key = r.row_key),
                'not_applicable') AS evidence_dated_from,
       coalesce((SELECT max(e.evidence_date) FROM evidence AS e WHERE e.row_key = r.row_key),
                'not_applicable') AS evidence_dated_to,
       coalesce((SELECT list(DISTINCT e.source_id ORDER BY e.source_id)
                 FROM evidence AS e
                 WHERE e.row_key = r.row_key AND e.standing = 'party'
                   AND e.publisher_entity_state <> 'value'), []::VARCHAR[]) AS party_standing_unchecked,
       EXISTS (SELECT 1 FROM reached AS x JOIN claims AS cl ON cl.id = x.claim_id
               WHERE x.row_key = r.row_key AND cl.claim_type = 'INTERPRETATION') AS rests_on_atlas_interpretation
FROM all_rows AS r
JOIN accelerators AS a ON a.accelerator_id = r.accelerator_id
LEFT JOIN entities AS ef ON ef.id = r.from_id
LEFT JOIN entities AS et ON et.id = r.to_id
ORDER BY a.accelerator, r.position, r.record_id, r.gap_reason, r.from_id
