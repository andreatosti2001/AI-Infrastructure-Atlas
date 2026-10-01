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

Run alone: python -m unittest discover -s tests -p "test_freshness.py" -v
"""

import calendar
import re
import unittest

from test_data_entities import fields, fixture_world, leaf_citations, load_entities, matrix
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


if __name__ == "__main__":
    unittest.main()
