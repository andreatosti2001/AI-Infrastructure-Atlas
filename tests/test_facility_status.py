"""ST-1: a facility's status is derived from its events, never stored (S09; facility-dataset.md §7).

Tests tools/facility_status.py on fictional events, then on the real events: every facility's
status is derivable on the dates its events bound, and plans never move it (ER-8).
Standard library only.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from facility_status import STATUSES, derive_status, period  # noqa: E402
from test_data_entities import facilities, load_entities  # noqa: E402
from test_data_events import load_events  # noqa: E402


def event(eid, kind, date, subject="facility-xa-site"):
    return {"id": eid, "event_type": kind, "subject": subject, "date": date, "claim_ids": ["claim-fixture-1"]}


class PeriodTests(unittest.TestCase):
    def test_partial_dates_are_periods(self) -> None:
        self.assertEqual(period("2021"), ("2021-01-01", "2021-12-31"))
        self.assertEqual(period("2024-02"), ("2024-02-01", "2024-02-29"))
        self.assertEqual(period("2021-02-01"), ("2021-02-01", "2021-02-01"))


class DerivationTests(unittest.TestCase):
    def test_no_occurrence_is_unknown_not_closed(self) -> None:
        self.assertEqual(derive_status("facility-xa-site", [], "2026-01-01")[0], "no_recorded_opening")

    def test_opened_then_closed(self) -> None:
        events = [event("e1", "opened", "2019-05"), event("e2", "closed", "2024")]
        self.assertEqual(derive_status("facility-xa-site", events, "2018-12-31"), ("not_yet_opened", ["e1"]))
        self.assertEqual(derive_status("facility-xa-site", events, "2019-06-01"), ("opened", ["e1"]))
        self.assertEqual(derive_status("facility-xa-site", events, "2024-06-01")[0], "indeterminate")
        self.assertEqual(derive_status("facility-xa-site", events, "2025-01-01"), ("closed", ["e2"]))

    def test_a_date_inside_an_event_period_is_indeterminate(self) -> None:
        events = [event("e1", "opened", "2021-02")]
        self.assertEqual(derive_status("facility-xa-site", events, "2021-02-10")[0], "indeterminate")
        self.assertEqual(derive_status("facility-xa-site", events, "2021-02-28")[0], "opened")

    def test_plans_and_expansions_never_move_the_status(self) -> None:
        # ER-8: an announced opening is not an opening.
        plan = [event("e1", "announced", "2022-09-06"), event("e2", "expanded", "2023")]
        self.assertEqual(derive_status("facility-xa-site", plan, "2026-01-01")[0], "no_recorded_opening")
        both = plan + [event("e3", "opened", "2020")]
        self.assertEqual(derive_status("facility-xa-site", both, "2026-01-01"), ("opened", ["e3"]))

    def test_unorderable_occurrences_are_indeterminate(self) -> None:
        events = [event("e1", "opened", "2020"), event("e2", "closed", "2020-06")]
        self.assertEqual(derive_status("facility-xa-site", events, "2021-01-01")[0], "indeterminate")

    def test_other_subjects_are_ignored(self) -> None:
        events = [event("e1", "opened", "2020", subject="facility-xa-other")]
        self.assertEqual(derive_status("facility-xa-site", events, "2021-01-01")[0], "no_recorded_opening")


class RealEventTests(unittest.TestCase):
    def test_st1_every_facility_status_is_derivable_and_plans_do_not_move_it(self) -> None:
        events = load_events()
        entities = load_entities()
        for where in ("canonical", "staging"):
            # A canonical facility's status reads canonical events only; staging reads both.
            pool = events["canonical"] + (events["staging"] if where == "staging" else [])
            occurrences = [e for e in pool if e["event_type"] in ("opened", "closed")]
            for record in entities[where]["facilities"]:
                dates = {"2000-01-01", "2100-01-01"} | {d for e in pool if e["subject"] == record["id"] for d in period(e["date"])}
                for on in sorted(dates):
                    with self.subTest(facility=record["id"], on=on):
                        status, _ = derive_status(record["id"], pool, on)
                        self.assertIn(status, STATUSES)
                        self.assertEqual(status, derive_status(record["id"], occurrences, on)[0])

    def test_no_record_stores_a_status(self) -> None:
        # MA §5.6: the schemas allow no status field; this guards the files as well.
        events = load_events()
        records = facilities(load_entities()) + events["canonical"] + events["staging"]
        self.assertEqual([r["id"] for r in records if any("status" in key for key in r)], [])


if __name__ == "__main__":
    unittest.main()
