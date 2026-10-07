-- question: As of a fixed reference date, how old is the newest evidence behind each link around each
--   AI accelerator on this page, and which links rest only on evidence more than 12 months older than
--   that date?
-- population: The links in the table of links, one row per accelerator and link, with the evidence dates
--   that table gives them. A link with nothing to date (an unknown) is listed with no age.
-- denominator: For a share read from this table, the number of links that have a date. The links with
--   nothing to date are a separate part, never counted as old or as new.
-- assumptions: The reference date is fixed in this file and moves only by a commit: each session that
--   rebuilds the pages sets it to the day it opened, so the result does not change with the calendar. The
--   12 months is the source policy's re-check horizon, which the policy applies only to time-sensitive
--   links (who fabricates a product, who supplies a part); for every other link it is a reading aid. A link's age is the age of its newest evidence, because the freshness
--   rule asks for at least one recent citation. A partial date counts from the start of its period. A
--   web page that states no date is dated by the day it was read, and its row says so.
-- missing data: Fourteen sources state no date of their own. Where one of them is the newest evidence,
--   the age measures the reading, not the content.
-- reproduce: python tools/warehouse.py rebuilds this result; the warehouse's checks recompute every age
--   independently, in plain Python, and check that moving the reference date changes the ages and
--   nothing else.
-- sensitivity: Each age moves one day for each day the reference date moves. A link crosses the
--   horizon on a known date, which the reference date makes visible rather than hiding.
-- does not prove: An old date does not make a statement false, and a recent date does not make it true.
--   Age is not reliability. Past 12 months, the freshness rule asks for newer evidence only on a
--   time-sensitive link, and even then it does not withdraw the link; a stable link (who designs a
--   product, what it incorporates, what a part requires) has no age limit.
-- reading: One row per link. newest_evidence is the newest evidence date behind the link, and
--   newest_evidence_basis says where that date comes from: a claim's as-of date, a date the source states
--   for itself, or the day the page was read. age_days counts the days from that date to the reference
--   date. beyond_horizon is yes when the newest evidence is more than 12 months older than the reference
--   date. Rows with nothing to date say not applicable in each of these columns.

-- step: Set the reference date and the horizon
-- Ages are measured from the reference date written here, not from today, so the same files always
-- give the same result. The horizon is the freshness rule's 12 months; that rule applies it only to
-- time-sensitive links, so for the others the flag below is a reading aid, not a re-check.
WITH params AS (
    SELECT DATE '2026-10-07' AS reference_date, INTERVAL 12 MONTH AS horizon
),

-- step: Take the newest evidence date of each link
-- This query reads the result of the links query, accelerator_dependencies, as a table, so it ages
-- exactly the links the page draws. A partial date such as 2020-12 is completed to the first day of its
-- period before any arithmetic, and a row with nothing to date keeps no date at all.
dated AS (
    SELECT d.accelerator, d.accelerator_id, d.position, d.record_id, d.gap_reason, d.from_id,
           d.from_name, d.relation, d.to_name, d.basis,
           d.evidence_dated_to AS newest_evidence,
           d.evidence_dated_to_basis AS newest_evidence_basis,
           CASE WHEN d.evidence_dated_to = 'not_applicable' THEN NULL
                WHEN length(d.evidence_dated_to) = 4 THEN CAST(d.evidence_dated_to || '-01-01' AS DATE)
                WHEN length(d.evidence_dated_to) = 7 THEN CAST(d.evidence_dated_to || '-01' AS DATE)
                ELSE CAST(d.evidence_dated_to AS DATE) END AS newest_start
    FROM accelerator_dependencies AS d
)

-- step: Measure each age against the reference date
-- date_diff counts whole days from the newest evidence to the reference date. A link is beyond the
-- horizon when its newest evidence starts before the reference date minus 12 months. A row with nothing
-- to date says not_applicable in words, never a zero and never an empty cell. The final ORDER BY keeps
-- the order of the table of links.
SELECT x.accelerator,
       x.accelerator_id,
       x.position,
       x.record_id,
       x.gap_reason,
       x.from_id,
       x.from_name,
       x.relation,
       x.to_name,
       x.basis,
       CAST(p.reference_date AS VARCHAR) AS reference_date,
       x.newest_evidence,
       x.newest_evidence_basis,
       CASE WHEN x.newest_start IS NULL THEN 'not_applicable'
            ELSE CAST(date_diff('day', x.newest_start, p.reference_date) AS VARCHAR) END AS age_days,
       CASE WHEN x.newest_start IS NULL THEN 'not_applicable'
            WHEN x.newest_start < p.reference_date - p.horizon THEN 'yes'
            ELSE 'no' END AS beyond_horizon
FROM dated AS x
CROSS JOIN params AS p
ORDER BY x.accelerator, x.position, x.record_id, x.gap_reason, x.from_id
