"""validate-freshness, first rule (S07; company-dataset.md §9; D-040). Standard library only.

F-1: a record field whose matrix row is `time_sensitive` (source-policy.md §7) must rest on
at least one citation that the row accepts (class and standing, as V-10) and whose evidence
date is no more than the horizon of source-policy.md §12 before its use.

- The evidence date is the citing claim's `as_of` when it is a date, otherwise the latest
  date the source states for itself, otherwise (an undated source) its access date
  (source-policy.md §12). A partial date counts from the start of its period.
- The use is the date the Verifier checked that citation for this record: the claim's
  `verified_on` (company-dataset.md §9). Re-checking stale evidence means citing newer
  evidence, because re-reading an old document does not make its content newer.
- `stable` rows have no age limit.

S10 (edge-dataset.md §4, D-096): F-1 extends to edges. An edge on a `time_sensitive` `rel:*` row,
and each `supplier` assertion on `rel:incorporates.supplier`, needs such a citation. An explicit
state (`not_researched`, `not_publicly_determinable`) is not a value: its search carries its own
date, so F-1 does not apply to it.

Run alone: python -m unittest discover -s tests -p "test_freshness.py" -v
"""

import calendar
import copy
import re
import unittest

from test_data_entities import fields, fixture_world, leaf_citations, load_entities, matrix
from test_data_relationships import edge_fixture_world, load_edges
from test_data_integrity import POLICY, load_data
from test_entity_taxonomy import section


def horizon_months() -> int:
    body = section(POLICY, "\n## 12. ", "\n## 13. ")
    (months,) = set(re.findall(r"more than (\d+) months before its use", body))
    return int(months)


def months_before(day: str, months: int) -> str:
    """The same day of the month `months` earlier, clamped to that month's length."""
    year, month, dom = (int(x) for x in day.split("-"))
    total = year * 12 + (month - 1) - months
    year, month = total // 12, total % 12 + 1
    return f"{year:04d}-{month:02d}-{min(dom, calendar.monthrange(year, month)[1]):02d}"


def start_of(partial: str) -> str:
    return (partial + "-01-01")[:10] if len(partial) == 4 else (partial + "-01")[:10] if len(partial) == 7 else partial


def evidence_date(claim: dict, source: dict) -> str:
    as_of = claim.get("as_of")
    if isinstance(as_of, str):
        return start_of(as_of)
    dates = source["stated_dates"]
    if isinstance(dates, list):
        return max(start_of(d["date"]) for d in dates)
    return source["retrieval"]["accessed_at"][:10]


def fresh_support(ids, row, months, by_id, claims) -> bool:
    """At least one citation the row accepts, within the horizon of its claim's verification."""
    for claim, citation in (lc for cid in ids for lc in leaf_citations(cid, claims)):
        source = by_id.get(citation["source_id"])
        if source is None or source["source_class"] not in row["sufficient"] or citation["standing"] not in row["standings"]:
            continue
        if "verified_on" in claim and evidence_date(claim, source) >= months_before(claim["verified_on"], months):
            return True
    return False


def historical_support(assertion, row, months, by_id, claims) -> bool:
    """S16.6 (R-1, D-144): at least one accepted citation dated no earlier than `valid_to` and no later than
    `valid_to` plus the horizon. A partial `valid_to` counts from the start of its period."""
    start = start_of(assertion["valid_to"])
    end = months_before(start, -months)
    for claim, citation in (lc for cid in assertion["claim_ids"] for lc in leaf_citations(cid, claims)):
        source = by_id.get(citation["source_id"])
        if source is None or source["source_class"] not in row["sufficient"] or citation["standing"] not in row["standings"]:
            continue
        if "verified_on" in claim and start <= evidence_date(claim, source) <= end:
            return True
    return False


def check_edge_freshness(edges, sources, staging_claims, canonical_claims) -> list[str]:
    """F-1, on every edge, staging and canonical (S10)."""
    rows = matrix()
    months = horizon_months()
    by_id = {s["id"]: s for s in sources}
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for where in ("canonical", "staging"):
        for edge in edges[where]:
            row_key = f"rel:{edge['relation_type']}"
            if rows[row_key]["freshness"] == "time_sensitive" and not fresh_support(edge["claim_ids"], rows[row_key], months, by_id, claims):
                errors.append(f"{edge['id']}: no accepted evidence within {months} months of its verification ({row_key} is time_sensitive)")
            qualifier = f"{row_key}.supplier"
            supplier = edge.get("supplier")
            if qualifier in rows and rows[qualifier]["freshness"] == "time_sensitive" and isinstance(supplier, list):
                for assertion in supplier:
                    if "valid_to" in assertion:
                        # a historical value (S16.6, D-144): its evidence dates its period, F-1 does not apply
                        if not historical_support(assertion, rows[qualifier], months, by_id, claims):
                            errors.append(f"{edge['id']}.supplier = {assertion['value']}: historical value whose evidence is not dated from valid_to {assertion['valid_to']} to {months} months after it")
                    elif not fresh_support(assertion["claim_ids"], rows[qualifier], months, by_id, claims):
                        errors.append(f"{edge['id']}.supplier = {assertion['value']}: no accepted evidence within {months} months of its verification ({qualifier} is time_sensitive)")
    return errors


def check_freshness(entities, sources, staging_claims, canonical_claims) -> list[str]:
    """F-1, on every entity record, staging and canonical."""
    rows = matrix()
    months = horizon_months()
    by_id = {s["id"]: s for s in sources}
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for where in ("canonical", "staging"):
        for kind in entities[where]:
            for record in entities[where][kind]:
                for field, row_key, assertions in fields(record):
                    row = rows[row_key]
                    if row["freshness"] != "time_sensitive":
                        continue
                    for assertion, ids in assertions:
                        fresh = False
                        for claim, citation in (lc for cid in ids for lc in leaf_citations(cid, claims)):
                            source = by_id.get(citation["source_id"])
                            if source is None or source["source_class"] not in row["sufficient"] or citation["standing"] not in row["standings"]:
                                continue
                            if "verified_on" in claim and evidence_date(claim, source) >= months_before(claim["verified_on"], months):
                                fresh = True
                        if not fresh:
                            label = f" = {assertion['value']}" if assertion else ""
                            errors.append(f"{record['id']}.{field}{label}: no accepted evidence within {months} months of its verification ({row_key} is time_sensitive)")
    return errors


class HorizonTests(unittest.TestCase):
    def test_horizon_is_read_from_the_policy(self) -> None:
        self.assertEqual(horizon_months(), 12)

    def test_month_arithmetic(self) -> None:
        self.assertEqual(months_before("2026-10-01", 12), "2025-10-01")
        self.assertEqual(months_before("2026-03-31", 1), "2026-02-28")
        self.assertEqual(start_of("2025"), "2025-01-01")
        self.assertEqual(start_of("2025-07"), "2025-07-01")


class FreshnessTests(unittest.TestCase):
    def test_f1_real_records_rest_on_fresh_evidence(self) -> None:
        sources, staging, canonical = load_data()
        self.assertEqual(check_freshness(load_entities(), sources, staging, canonical), [])

    def test_f1_fixture_world_is_fresh(self) -> None:
        self.assertEqual(check_freshness(*fixture_world()), [])

    def test_f1_stale_evidence_is_caught(self) -> None:
        # A time_sensitive value whose only evidence is more than 12 months older than its
        # verification, not re-checked against newer evidence.
        entities, sources, staging, canonical = fixture_world()
        for source in sources:
            if source["id"] == "src-914":
                source["stated_dates"] = [{"kind": "signed", "date": "2025-09-29"}]
        errors = check_freshness(entities, sources, staging, canonical)
        self.assertTrue(any("company-example-foundry.legal_name" in e for e in errors), errors)
        self.assertFalse(any("identity_claim_ids" in e for e in errors), "identity:company is stable")

    def test_f1_as_of_overrides_the_source_date(self) -> None:
        entities, sources, staging, canonical = fixture_world()
        for claim in staging:
            if claim["id"] == "claim-fixture-312":
                claim["as_of"] = "2024-12"
        errors = check_freshness(entities, sources, staging, canonical)
        self.assertTrue(any("company-example-foundry.roles = foundry_operator" in e for e in errors), errors)


class EdgeFreshnessTests(unittest.TestCase):
    """F-1 on edges (S10; edge-dataset.md §4)."""

    def test_f1_real_edges_rest_on_fresh_evidence(self) -> None:
        sources, staging, canonical = load_data()
        self.assertEqual(check_edge_freshness(load_edges(), sources, staging, canonical), [])

    def test_f1_fixture_edges_are_fresh(self) -> None:
        edges, _, _, sources, staging, canonical, _ = edge_fixture_world()
        self.assertEqual(check_edge_freshness(edges, sources, staging, canonical), [])

    def test_f1_stale_edge_evidence_is_caught(self) -> None:
        # The fictional operates edge rests on a filing signed 2026-03-01 with as_of 2025-03;
        # an as_of more than 12 months before its verification makes it stale.
        edges, _, _, sources, staging, canonical, _ = edge_fixture_world()
        for claim in staging:
            if claim["id"] == "claim-fixture-405":
                claim["as_of"] = "2024-12"
        errors = check_edge_freshness(edges, sources, staging, canonical)
        self.assertTrue(any("operates-facility-xa-example-fab-1" in e for e in errors), errors)
        self.assertFalse(any("designs" in e for e in errors), "rel:designs is stable")


class HistoricalSupplierTests(unittest.TestCase):
    """S16.6 (R-1, D-144): a supplier value with `valid_to` is historical. F-1 does not apply; its evidence must
    date its period: no earlier than `valid_to`, and no later than `valid_to` plus the horizon. That it states a
    past fact, not a plan (ER-8), is the Verifier's reading, not a check."""

    H100_HBM = "rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory"
    BASE = {"value": "company-sk-hynix", "claim_ids": ["claim-sk-hynix-hbm3-for-h100-2022"]}

    def errors(self, assertion: dict) -> list[str]:
        sources, staging, canonical = load_data()
        edges = copy.deepcopy(load_edges())
        next(e for e in edges["canonical"] if e["id"] == self.H100_HBM)["supplier"] = [assertion]
        return [e for e in check_edge_freshness(edges, sources, staging, canonical) if ".supplier" in e]

    def test_r1_without_valid_to_stale_evidence_is_refused(self) -> None:
        self.assertTrue(self.errors(dict(self.BASE)), "a supplier on 2022 evidence passed F-1")

    def test_r1_a_historical_value_dated_by_its_evidence_passes(self) -> None:
        self.assertEqual(self.errors(dict(self.BASE, valid_to="2022-06")), [])

    def test_r1_a_period_its_evidence_does_not_date_is_refused(self) -> None:
        for valid_to in ("2022-07", "2021-05"):
            with self.subTest(valid_to=valid_to):
                errors = self.errors(dict(self.BASE, valid_to=valid_to))
                self.assertTrue(any("historical" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
