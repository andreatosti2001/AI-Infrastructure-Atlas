"""Derive a facility's status on a date from its events (S09; facility-dataset.md §7; D-085).

A facility's status is never stored (MA §5.6, R-8). It is computed here, when asked, from
the occurrence events (opened, closed) whose subject is the facility. `announced` is a plan
and `expanded` changes no state, so neither moves the status (ER-8).

Each event has a partial date (YYYY, YYYY-MM or YYYY-MM-DD), read as the period it names.
An event is "wholly before" a date when the last day of its period is on or before it.

Statuses:
    opened               the latest occurrence wholly before the date is `opened`
    closed               the latest occurrence wholly before the date is `closed`
    not_yet_opened       no occurrence before the date, and an `opened` event after it
    indeterminate        an occurrence's period contains the date, or two occurrences of
                         different types cannot be ordered
    no_recorded_opening  no occurrence at all: unknown, never "not operating"

Usage:
    python tools/facility_status.py FACILITY_ID --on YYYY-MM-DD [--data DIR] [--include-staging]

By default only canonical events (data/events.json) are read. Standard library only (D-003).
"""

from __future__ import annotations

import argparse
import calendar
import json
import sys
from pathlib import Path

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data"
OCCURRENCES = ("opened", "closed")
STATUSES = ("opened", "closed", "not_yet_opened", "indeterminate", "no_recorded_opening")


def period(partial: str) -> tuple[str, str]:
    """(first day, last day) of a partial date."""
    if len(partial) == 4:
        return f"{partial}-01-01", f"{partial}-12-31"
    if len(partial) == 7:
        year, month = (int(x) for x in partial.split("-"))
        return f"{partial}-01", f"{partial}-{calendar.monthrange(year, month)[1]:02d}"
    return partial, partial


def derive_status(facility_id: str, events: list[dict], on: str) -> tuple[str, list[str]]:
    """(status, IDs of the events it rests on) of one facility on one full date."""
    occurrences = sorted(
        (period(e["date"]) + (e["event_type"], e["id"]) for e in events if e["subject"] == facility_id and e["event_type"] in OCCURRENCES),
        key=lambda item: (item[1], item[0]),
    )
    if not occurrences:
        return "no_recorded_opening", []
    containing = [o for o in occurrences if o[0] <= on < o[1]]
    if containing:
        return "indeterminate", [o[3] for o in containing]
    before = [o for o in occurrences if o[1] <= on]
    if not before:
        opened_after = [o[3] for o in occurrences if o[2] == "opened"]
        return ("not_yet_opened", opened_after) if opened_after else ("no_recorded_opening", [])
    last = before[-1]
    rivals = [o for o in before[:-1] if o[2] != last[2] and o[1] >= last[0]]
    if rivals:
        return "indeterminate", [o[3] for o in rivals] + [last[3]]
    return last[2], [last[3]]


def load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("facility_id")
    parser.add_argument("--on", required=True, help="a full date, YYYY-MM-DD")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--include-staging", action="store_true", help="also read data/staging/events.json")
    args = parser.parse_args(argv)
    events = load(args.data / "events.json")
    if args.include_staging:
        events += load(args.data / "staging" / "events.json")
    status, basis = derive_status(args.facility_id, events, args.on)
    print(f"{args.facility_id} on {args.on}: {status}" + (f" (events: {', '.join(basis)})" if basis else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
