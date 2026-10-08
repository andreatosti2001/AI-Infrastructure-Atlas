"""Derive a policy's status on a date from its events (S17; policy-dataset.md P-4; D-156, D-164).

A policy's status is never stored (MA §5.6, R-8). It is computed here, when asked, from the events whose
subject is the policy: `published`, `effective` (one per date the act's text fixes) and `repealed`.
`announced` is a plan and never moves the status (ER-8): an authority saying it will rescind a rule is not
a repeal. A `proposed_rule` never takes effect, whatever its events say.

Each event has a partial date (YYYY, YYYY-MM or YYYY-MM-DD), read as the period it names. An event is "wholly
before" a date when the last day of its period is on or before it.

Statuses:
    proposed                     the act's form is proposed_rule: a proposal never takes effect
    repealed                     a repealed event lies wholly before the date
    has_taken_effect             an effective event lies wholly before the date, and no repeal does:
                                 "has taken effect; no repeal recorded in the Atlas", never "in force"
    published_not_yet_in_effect  published before the date; every effective event is after it
    not_yet_published            the date is before the act's publication and before any effective date
    indeterminate                an event's period contains the date
    no_recorded_effect           no effective event is recorded: unknown, never "not in effect"

Usage:
    python tools/policy_status.py POLICY_ID --on YYYY-MM-DD [--data DIR] [--include-staging]

By default only canonical records (data/policies.json, data/events.json) are read. Standard library only (D-003).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from facility_status import period

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data"
STATUSES = (
    "proposed",
    "repealed",
    "has_taken_effect",
    "published_not_yet_in_effect",
    "not_yet_published",
    "indeterminate",
    "no_recorded_effect",
)


def derive_status(policy_id: str, events: list[dict], on: str, forms: set[str]) -> tuple[str, list[str]]:
    """(status, IDs of the events it rests on) of one policy on one full date, given its instrument forms."""
    if "proposed_rule" in forms:
        return "proposed", []
    mine = sorted(
        (period(e["date"]) + (e["event_type"], e["id"]) for e in events if e["subject"] == policy_id),
        key=lambda item: (item[1], item[0], item[3]),
    )
    of = lambda kind: [o for o in mine if o[2] == kind]  # noqa: E731
    containing = [o[3] for o in of("repealed") + of("effective") if o[0] <= on < o[1]]
    repealed = [o[3] for o in of("repealed") if o[1] <= on]
    if repealed:
        return ("indeterminate", containing) if containing else ("repealed", repealed)
    repeal_pending = [o[3] for o in of("repealed") if o[0] <= on < o[1]]
    if repeal_pending:
        return "indeterminate", repeal_pending
    effective_before = [o[3] for o in of("effective") if o[1] <= on]
    if effective_before:
        return "has_taken_effect", effective_before
    if containing:
        return "indeterminate", containing
    if not of("effective"):
        return "no_recorded_effect", []
    published = of("published")
    if any(o[1] <= on for o in published):
        return "published_not_yet_in_effect", [o[3] for o in published if o[1] <= on] + [o[3] for o in of("effective")]
    if any(o[0] <= on < o[1] for o in published):
        return "indeterminate", [o[3] for o in published if o[0] <= on < o[1]]
    return "not_yet_published", []


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("policy_id")
    parser.add_argument("--on", required=True, help="a full date, YYYY-MM-DD")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--include-staging", action="store_true", help="also read the staging policies and events")
    args = parser.parse_args(argv)
    policies = load(args.data / "policies.json")
    events = load(args.data / "events.json")
    if args.include_staging:
        policies += load(args.data / "staging" / "policies.json")
        events += load(args.data / "staging" / "events.json")
    record = next((p for p in policies if p["id"] == args.policy_id), None)
    if record is None:
        print(f"{args.policy_id}: no such policy record", file=sys.stderr)
        return 1
    forms = {a["value"] for a in record["instrument_form"]} if isinstance(record["instrument_form"], list) else set()
    status, basis = derive_status(args.policy_id, events, args.on, forms)
    print(f"{args.policy_id} on {args.on}: {status}" + (f" (events: {', '.join(basis)})" if basis else ""))
    if status == "has_taken_effect":
        print("  has taken effect on the date its text fixes; no repeal recorded in the Atlas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
