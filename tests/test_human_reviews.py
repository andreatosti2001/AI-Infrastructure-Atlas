"""validate-data: every reviewed claim resolves to its entry in the human review record (D-151).

A claim's `review.recorded_in` names the durable public record of the human's verdict:
`docs/quality/human-reviews.md#<entry>`, where <entry> is the anchor of one level-2 heading of that file.
The checks:

- HR-1 every `recorded_in` (canonical and staging claims) names a heading that exists in the record;
- HR-2 the date that ends the entry's anchor is the claim's `reviewed_on`;
- HR-3 every entry is named by at least one claim, and the claim count it states ("**Claims:** N", and
  its row in the summary table) is the number of claims that name it.

The check functions take record lists and the record's text, so the same checks run on planted faults.
"""

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate_repo import heading_anchor  # noqa: E402

RECORD = "docs/quality/human-reviews.md"
DATE_SUFFIX = re.compile(r"-(\d{4}-\d{2}-\d{2})$")


def entries(text: str) -> dict[str, str]:
    """Each level-2 heading's anchor, mapped to the text of its section."""
    out: dict[str, str] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = heading_anchor(line[3:])
            out[current] = ""
        elif current is not None:
            out[current] += line + "\n"
    return out


def reviewed(claims: list[dict]) -> list[dict]:
    return [c for c in claims if "verdict" in c.get("review", {})]


def resolution_errors(claims: list[dict], text: str) -> list[str]:
    """HR-1 and HR-2."""
    known = entries(text)
    errors = []
    for claim in reviewed(claims):
        review = claim["review"]
        path, _, entry = review["recorded_in"].partition("#")
        if path != RECORD or entry not in known:
            errors.append(f"{claim['id']}: recorded_in {review['recorded_in']!r} names no entry of {RECORD}")
            continue
        date = DATE_SUFFIX.search(entry)
        if not date or date.group(1) != review["reviewed_on"]:
            errors.append(f"{claim['id']}: reviewed_on {review['reviewed_on']} is not the date of entry {entry!r}")
    return errors


def count_errors(claims: list[dict], text: str) -> list[str]:
    """HR-3."""
    counts: dict[str, int] = {}
    for claim in reviewed(claims):
        entry = claim["review"]["recorded_in"].partition("#")[2]
        counts[entry] = counts.get(entry, 0) + 1
    errors = []
    for entry, body in entries(text).items():
        stated = re.search(r"\*\*Claims:\*\* (\d+)\.", body)
        if not stated:
            errors.append(f"entry {entry!r} does not state its claim count")
            continue
        if entry not in counts:
            errors.append(f"entry {entry!r} is named by no claim")
        if int(stated.group(1)) != counts.get(entry, 0):
            errors.append(f"entry {entry!r} states {stated.group(1)} claims; {counts.get(entry, 0)} name it")
        row = re.search(rf"\]\(#{re.escape(entry)}\) \| [0-9-]+ \| (\d+) \|", text)
        if not row or int(row.group(1)) != counts.get(entry, 0):
            errors.append(f"entry {entry!r}: the summary table's claim count is not {counts.get(entry, 0)}")
    return errors


def load(rel: str) -> list[dict]:
    return json.loads((REPO_ROOT / rel).read_text(encoding="utf-8"))


class HumanReviewRecordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.claims = load("data/claims.json") + load("data/staging/claims.json")
        self.text = (REPO_ROOT / RECORD).read_text(encoding="utf-8")

    def test_hr1_hr2_every_review_resolves_to_its_dated_entry(self) -> None:
        self.assertEqual(resolution_errors(self.claims, self.text), [])

    def test_hr3_every_entry_is_used_and_counts_its_claims(self) -> None:
        self.assertEqual(count_errors(self.claims, self.text), [])

    def test_planted_faults_are_caught(self) -> None:
        claim = {"id": "claim-x", "review": {"verdict": "accepted", "reviewer": "human", "reviewed_on": "2026-10-01",
                                             "recorded_in": f"{RECORD}#companies-and-jurisdictions-2026-10-01"}}
        text = "## Companies and jurisdictions, 2026-10-01\n\n- **Claims:** 1.\n\n" \
               "| [x](#companies-and-jurisdictions-2026-10-01) | 2026-10-01 | 1 | all accepted |\n"
        self.assertEqual(resolution_errors([claim], text) + count_errors([claim], text), [])
        for field, value, fragment in (
            ("recorded_in", f"{RECORD}#no-such-entry-2026-10-01", "names no entry"),
            ("recorded_in", "sessions/reports/SESSION-07-REPORT.md", "names no entry"),
            ("reviewed_on", "2026-10-02", "is not the date of entry"),
        ):
            planted = json.loads(json.dumps(claim))
            planted["review"][field] = value
            with self.subTest(field=field, value=value):
                self.assertIn(fragment, " ".join(resolution_errors([planted], text)))
        self.assertIn("states 2 claims", " ".join(count_errors([claim], text.replace("**Claims:** 1.", "**Claims:** 2."))))
        self.assertIn("named by no claim", " ".join(count_errors([], text)))


if __name__ == "__main__":
    unittest.main()
