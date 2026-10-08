"""PL-7: a policy's status is derived from its events, never stored (S17; policy-dataset.md P-4; D-156, D-164).

Tests tools/policy_status.py on fictional events, then on the real ones: every policy's status is derivable
on the dates its events bound, an announced rescission never moves it (ER-8), and a proposal never takes
effect. Standard library only.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from policy_status import STATUSES, derive_status  # noqa: E402
from facility_status import period  # noqa: E402
from test_data_entities import load_entities, policies  # noqa: E402
from test_data_events import load_events  # noqa: E402

RULE = "policy-xa-ex-1-100"


def event(eid, kind, date, subject=RULE):
    return {"id": eid, "event_type": kind, "subject": subject, "date": date, "claim_ids": ["claim-fixture-1"]}


def status(events, on, forms=("interim_final_rule",)):
    return derive_status(RULE, events, on, set(forms))


class DerivationTests(unittest.TestCase):
    def test_no_effective_event_is_unknown_not_out_of_effect(self) -> None:
        self.assertEqual(status([], "2026-01-01")[0], "no_recorded_effect")
        self.assertEqual(status([event("p", "published", "2022-10-13")], "2026-01-01")[0], "no_recorded_effect")

    def test_staged_effect_beginning_before_publication(self) -> None:
        # The 2022 pattern: part effective six days before publication, the rest later (P-4).
        events = [event("p", "published", "2022-10-13"), event("e1", "effective", "2022-10-07"), event("e2", "effective", "2022-10-21")]
        self.assertEqual(status(events, "2022-10-06"), ("not_yet_published", []))
        self.assertEqual(status(events, "2022-10-08"), ("has_taken_effect", ["e1"]))
        self.assertEqual(status(events, "2022-10-30"), ("has_taken_effect", ["e1", "e2"]))

    def test_published_before_its_effective_date(self) -> None:
        events = [event("p", "published", "2023-10-25"), event("e", "effective", "2023-11-17")]
        self.assertEqual(status(events, "2023-11-01"), ("published_not_yet_in_effect", ["p", "e"]))
        self.assertEqual(status(events, "2023-11-17"), ("has_taken_effect", ["e"]))

    def test_repeal(self) -> None:
        events = [event("e", "effective", "2025-01-13"), event("r", "repealed", "2025-05")]
        self.assertEqual(status(events, "2025-04-30"), ("has_taken_effect", ["e"]))
        self.assertEqual(status(events, "2025-05-10")[0], "indeterminate")
        self.assertEqual(status(events, "2025-06-01"), ("repealed", ["r"]))

    def test_an_announced_rescission_changes_nothing(self) -> None:
        # ER-8: the authority saying it will rescind a rule is not a repeal.
        events = [event("e", "effective", "2025-01-13"), event("a", "announced", "2025-05-13")]
        self.assertEqual(status(events, "2026-01-01"), ("has_taken_effect", ["e"]))

    def test_a_proposal_never_takes_effect(self) -> None:
        events = [event("p", "published", "2024-01-02"), event("e", "effective", "2024-03-01")]
        self.assertEqual(status(events, "2026-01-01", forms=("proposed_rule",))[0], "proposed")

    def test_a_date_inside_an_event_period_is_indeterminate(self) -> None:
        events = [event("e", "effective", "2024")]
        self.assertEqual(status(events, "2024-06-01")[0], "indeterminate")
        self.assertEqual(status(events, "2025-01-01")[0], "has_taken_effect")

    def test_other_subjects_are_ignored(self) -> None:
        events = [event("e", "effective", "2020", subject="policy-xa-ex-2-200")]
        self.assertEqual(status(events, "2021-01-01")[0], "no_recorded_effect")


class RealEventTests(unittest.TestCase):
    def test_pl7_every_policy_status_is_derivable(self) -> None:
        events = load_events()
        entities = load_entities()
        for where in ("canonical", "staging"):
            # A canonical policy's status reads canonical events only; staging reads both.
            pool = events["canonical"] + (events["staging"] if where == "staging" else [])
            for record in entities[where]["policies"]:
                forms = {a["value"] for a in record["instrument_form"]} if isinstance(record["instrument_form"], list) else set()
                dates = {"2000-01-01", "2100-01-01"} | {d for e in pool if e["subject"] == record["id"] for d in period(e["date"])}
                for on in sorted(dates):
                    with self.subTest(policy=record["id"], on=on):
                        derived, _ = derive_status(record["id"], pool, on, forms)
                        self.assertIn(derived, STATUSES)
                        if "proposed_rule" in forms:
                            self.assertEqual(derived, "proposed")

    def test_no_policy_stores_a_status(self) -> None:
        # MA §5.6: the schema allows no status field; this guards the files as well.
        records = policies(load_entities())
        self.assertEqual([r["id"] for r in records if any("status" in key or "date" in key for key in r)], [])


if __name__ == "__main__":
    unittest.main()
