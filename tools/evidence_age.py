"""Which values rest on evidence older than the freshness horizon, as of the pages' reference date (S23, D-221).

The release content audit (C-2) found Micron's four company values past the 12-month horizon with no signal: the
freshness check (F-1, tests/test_freshness.py) measures age at verification by design, and the source-age query
(sql/source_age.sql, D-129) ages only the chain's links. This module answers, for one record's field, whether the
newest evidence the source policy accepts for that field is dated more than the horizon before the reference date.
The company pages mark such a value beside it (tools/build_journeys.py; JR-16 recomputes it independently).

Every input has one home, read here and never restated:
  - the reference date: sql/source_age.sql (D-137; the as-of date every page carries);
  - the horizon and the matrix rows (time_sensitive or stable; the classes and standings a row accepts):
    docs/research/source-policy.md §12 and §7;
  - a claim's evidence date: its as_of when it is a date, otherwise the latest date its source states, otherwise
    (an undated source) the source's retrieval date (source-policy.md §12; claim-model.md §10). A partial date counts
    from the start of its period. Inputs of a DERIVATION are followed to their citations.

It never says a value is current or stale, and computes no age from today's date (V-5): it compares two dates the
records and the reference date fix. A historical value (valid_to, D-144) is never marked. Standard library only (D-003).

Usage:
    python tools/evidence_age.py RECORD_ID     print each time_sensitive value of a record and its newest evidence
"""

from __future__ import annotations

import calendar
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
POLICY = REPO_ROOT / "docs" / "research" / "source-policy.md"
SOURCE_AGE = REPO_ROOT / "sql" / "source_age.sql"
DATA = REPO_ROOT / "data"
STANDINGS = {"party or originator": {"party", "originator"}, "party": {"party"}, "originator": {"originator"},
             "party, or a third party under §7.1": {"party", "originator", "reporter"}}


def reference_date(text: str | None = None) -> str:
    text = SOURCE_AGE.read_text(encoding="utf-8") if text is None else text
    (day,) = re.findall(r"DATE '(\d{4}-\d{2}-\d{2})' AS reference_date", text)
    return day


def _policy_section(text: str, number: str, following: str) -> str:
    start = text.index(f"\n## {number}. ")
    return text[start : text.index(f"\n## {following}. ", start)]


def horizon_months(text: str | None = None) -> int:
    text = POLICY.read_text(encoding="utf-8") if text is None else text
    (months,) = set(re.findall(r"more than (\d+) months before its use", _policy_section(text, "12", "13")))
    return int(months)


def matrix(text: str | None = None) -> dict[str, dict]:
    """source-policy.md §7: row key -> {accepted classes (preferred and acceptable), standings, freshness}."""
    text = POLICY.read_text(encoding="utf-8") if text is None else text
    rows = {}
    for line in _policy_section(text, "7", "8").splitlines():
        cells = [c.strip() for c in line.strip()[1:-1].split("|")] if line.startswith("|") else []
        if len(cells) != 7 or not re.fullmatch(r"`(?:rel|identity|attr|event):[a-z_.]+`", cells[0]):
            continue
        classes = lambda cell: set() if cell == "none" else set(re.findall(r"`([a-z_]+)`", cell))  # noqa: E731
        rows[cells[0].strip("`")] = {"accepted": classes(cells[1]) | classes(cells[2]),
                                     "standings": STANDINGS[cells[4]], "freshness": cells[5]}
    return rows


def months_before(day: str, months: int) -> str:
    year, month, dom = (int(x) for x in day.split("-"))
    total = year * 12 + month - 1 - months
    year, month = divmod(total, 12)
    return f"{year:04d}-{month + 1:02d}-{min(dom, calendar.monthrange(year, month + 1)[1]):02d}"


def start_of(partial: str) -> str:
    return {4: partial + "-01-01", 7: partial + "-01"}.get(len(partial), partial)


def evidence_date(claim: dict, source: dict) -> str:
    if isinstance(claim.get("as_of"), str):
        return start_of(claim["as_of"])
    if isinstance(source["stated_dates"], list):
        return max(start_of(d["date"]) for d in source["stated_dates"])
    return source["retrieval"]["accessed_at"][:10]


class Ages:
    """The records, the matrix and the reference date, read once."""

    def __init__(self, data: Path = DATA) -> None:
        self.claims = {c["id"]: c for c in json.loads((data / "claims.json").read_text(encoding="utf-8"))}
        self.sources = {s["id"]: s for s in json.loads((data / "sources.json").read_text(encoding="utf-8"))}
        self.rows = matrix()
        self.on = reference_date()
        self.limit = months_before(self.on, horizon_months())

    def citations(self, claim_id: str, seen: set | None = None) -> list[tuple[dict, dict]]:
        seen = set() if seen is None else seen
        if claim_id in seen or claim_id not in self.claims:
            return []
        seen.add(claim_id)
        claim = self.claims[claim_id]
        found = [(claim, c) for c in claim.get("citations", [])]
        for ref in claim.get("input_claim_ids", []):
            found += self.citations(ref, seen)
        return found

    def newest(self, row_key: str, claim_ids: list[str]) -> str | None:
        """The newest evidence date among the citations the row accepts, or None if there is none."""
        row = self.rows[row_key]
        dates = [evidence_date(claim, self.sources[c["source_id"]]) for cid in claim_ids for claim, c in self.citations(cid)
                 if self.sources[c["source_id"]]["source_class"] in row["accepted"] and c["standing"] in row["standings"]]
        return max(dates) if dates else None

    def past_horizon(self, record: dict, field: str, index: int) -> str | None:
        """The newest evidence date of one value of a time_sensitive company attribute, when it is older than the
        horizon before the reference date; otherwise None (a stable row, a historical value, or recent evidence)."""
        row_key = f"attr:{record['type']}.{field}"
        if row_key not in self.rows or self.rows[row_key]["freshness"] != "time_sensitive":
            return None
        assertion = record[field][index]
        if "valid_to" in assertion:
            return None
        newest = self.newest(row_key, assertion["claim_ids"])
        return newest if newest is not None and newest < self.limit else None


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[-1].strip(), file=sys.stderr)
        return 2
    ages = Ages()
    records = {r["id"]: r for f in DATA.glob("*.json") if f.name != "claims.json"
               for r in json.loads(f.read_text(encoding="utf-8")) if isinstance(r, dict) and "id" in r and "type" in r}
    record = records.get(argv[0])
    if record is None:
        print(f"no record {argv[0]}", file=sys.stderr)
        return 2
    print(f"reference date {ages.on}; horizon from {ages.limit}")
    for field, value in record.items():
        if isinstance(value, list) and value and isinstance(value[0], dict) and "claim_ids" in value[0]:
            for i, assertion in enumerate(value):
                key = f"attr:{record['type']}.{field}"
                if key in ages.rows and ages.rows[key]["freshness"] == "time_sensitive":
                    newest = ages.newest(key, assertion["claim_ids"])
                    mark = "past the horizon" if ages.past_horizon(record, field, i) else "within the horizon"
                    print(f"{field}/{i} = {assertion['value']}: newest evidence {newest} ({mark})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
