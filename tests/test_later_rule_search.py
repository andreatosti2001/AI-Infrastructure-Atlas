"""The later-rule search tool (S22, D-210, D-211): tools/later_rule_search.py, checked without the network.

Every response the tool reads is a constructed recorded response (the Federal Register index's JSON, an official
daily edition's XML, a PDF's bytes) served by a fake fetcher that fails on any request it was not given, so each test
also fixes the requests the tool makes. The documents are fictional (numbers 2099-NNNNN).

LS-1  a window with nothing to report: "none found in the searched window", every request logged with its time.
LS-2  a candidate (an entry named in an official text, 15 CFR part 774 in its heading): listed with its PDF's hash;
      the outcome sends it to the Change Detector and the "Searched to" date does not move.
LS-3  a refused index request is an access gap (host, status, time), the outcome is incomplete, never "none found".
LS-4  an issue the index says exists but the official edition does not serve is an access gap; a day with no
      document in the index and no issue is not.
LS-5  a registered official text whose bytes changed is reported (CD-5); the tool edits no record.
LS-6  the two registers disagree (a BIS document in the index, absent from the official edition): listed for review.
LS-7  the window: from after to, or to after today, is refused.
LS-8  the terms come from their homes: the entries from CD-3 of change-detection.md, the acts from data/policies.json.
LS-9  the command line writes only its log, never data/ or change-detection.md; a log path inside the repository
      outside docs/research/search-logs/later-rules/ is refused.
LS-10 the index's count is honoured: fewer results than the count is an access gap.
LS-11 rescind and repeal words select BIS rules, never BIS notices (orders denying export privileges).
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import later_rule_search as lrs  # noqa: E402

NOW = "2026-03-04T12:00:00Z"
WINDOW = ("2026-02-27", "2026-03-02")  # Friday to Monday; Monday is a fictional holiday with no issue
PDF_A = b"%PDF-1.7 fictional rule 2099-00001\n"
PDF_REG = b"%PDF-1.7 fictional registered act\n"
REG_URL = "https://www.govinfo.gov/content/pkg/FR-2099-01-02/pdf/2099-00100.pdf"
TERMS = lrs.make_terms(("3A090", "3B001"), (("89 FR 96790", "2024-28270"),))
REGISTERED = (("src-900", REG_URL, hashlib.sha256(PDF_REG).hexdigest()),)


def sha(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def api(results: list[dict], count: int | None = None) -> bytes:
    return json.dumps({"count": len(results) if count is None else count, "total_pages": 1, "results": results}).encode()


def doc(number: str, day: str, title: str, kind: str = "Rule", bis: bool = True) -> dict:
    slug = lrs.BIS if bis else "federal-aviation-administration"
    return {"document_number": number, "citation": f"99 FR {number[-3:]}", "publication_date": day, "title": title,
            "type": kind, "action": "Final rule.", "agencies": [{"slug": slug}],
            "pdf_url": lrs.pdf_url(day, number)}


def issue(*docs: tuple[str, str, str, str, str]) -> bytes:
    """An official daily edition: (section, agency, sub-agency, cfr heading, number + text) per document."""
    sections: dict[str, list[str]] = {}
    for kind, agency, sub, cfr, text in docs:
        number = text.split()[0]
        body = (f"<{kind}><PREAMB><AGENCY>{agency}</AGENCY><SUBAGY>{sub}</SUBAGY><CFR>{cfr}</CFR>"
                f"<SUBJECT>Fictional</SUBJECT></PREAMB><SUPLINF><P>{text}</P></SUPLINF>"
                f"<FRDOC>[FR Doc. {number} Filed 1-1-99; 8:45 am]</FRDOC></{kind}>")
        sections.setdefault({"RULE": "RULES", "PRORULE": "PRORULES", "NOTICE": "NOTICES"}[kind], []).append(body)
    inner = "".join(f"<{s}>{''.join(b)}</{s}>" for s, b in sections.items())
    return f'<?xml version="1.0"?><FEDREG><VOL>99</VOL>{inner}</FEDREG>'.encode()


class Fake:
    """A fetcher that serves only the responses it was given, each with the recorded time NOW."""

    def __init__(self, responses: dict[str, tuple[int, bytes]]) -> None:
        self.responses, self.asked = dict(responses), []

    def get(self, url: str) -> lrs.Response:
        if url not in self.responses:
            raise AssertionError(f"unexpected request: {url}")
        self.asked.append(url)
        status, body = self.responses[url]
        return lrs.Response(url, status, body if status == 200 else b"", NOW)

    def today(self) -> str:
        return NOW[:10]


def quiet_world() -> dict[str, tuple[int, bytes]]:
    """Friday has one BIS notice and one other agency's rule; the weekend and Monday have no issue."""
    a, b = WINDOW
    world = {
        lrs.index_url(a, b, page=1, bis=True): (200, api([doc("2099-00002", a, "Order Denying Export Privileges", "Notice")])),
        lrs.index_url(a, b, page=1, bis=True, term="rescission"): (200, api([])),
        lrs.index_url(a, b, page=1, bis=True, term="rescind"): (200, api([])),
        lrs.index_url(a, b, page=1, bis=True, term="repeal"): (200, api([])),
        lrs.index_url(a, b, page=1, bis=True, term="withdraw"): (200, api([])),
        lrs.index_url(a, b, page=1, bis=True, term="withdrawal"): (200, api([])),
        lrs.facets_url(a, b): (200, json.dumps({"2026-02-27": {"count": 2}, "2026-02-28": {"count": 0},
                                                "2026-03-01": {"count": 0}, "2026-03-02": {"count": 0}}).encode()),
        lrs.issue_url("2026-02-27"): (200, issue(
            ("NOTICE", "DEPARTMENT OF COMMERCE", "Bureau of Industry and Security", "",
             "2099-00002 an order; the denial is not repealed"),
            ("RULE", "DEPARTMENT OF TRANSPORTATION", "Federal Aviation Administration", "14 CFR Part 39",
             "2099-00003 airworthiness directive for a fictional engine"))),
        lrs.issue_url("2026-03-02"): (302, b""),
        REG_URL: (200, PDF_REG),
    }
    for term in TERMS:
        if term.index_query:
            world[lrs.index_url(a, b, page=1, bis=False, term=term.index_query)] = (200, api([]))
    return world


def run(world: dict[str, tuple[int, bytes]], window: tuple[str, str] = WINDOW) -> tuple[lrs.Result, str, Fake]:
    fake = Fake(world)
    result = lrs.search(window[0], window[1], fake, TERMS, REGISTERED)
    return result, lrs.render(result), fake


class LaterRuleSearchTests(unittest.TestCase):
    # LS-1
    def test_ls1_a_quiet_window_records_itself_as_none_found(self) -> None:
        result, log, fake = run(quiet_world())
        self.assertEqual(lrs.outcome(result)[1], lrs.EXIT_NONE)
        self.assertIn("**Window searched: 2026-02-27 to 2026-03-02**", log)
        self.assertIn("**Outcome:** none found in the searched window", log)
        self.assertNotIn("access gap:", log.lower())
        for url in fake.asked:
            self.assertIn(url.split("://", 1)[1].split("/", 1)[0], log)
        self.assertEqual(log.count(NOW), len(fake.asked), "every request is logged with its time")
        self.assertEqual(sorted(set(fake.asked)), sorted(quiet_world()), "every response given was asked for")

    # LS-2
    def test_ls2_a_candidate_is_listed_with_its_hash_and_stops_the_date(self) -> None:
        world = quiet_world()
        world[lrs.issue_url("2026-02-27")] = (200, issue(
            ("RULE", "DEPARTMENT OF COMMERCE", "Bureau of Industry and Security", "15 CFR Parts 740 and 774",
             "2099-00001 revises ECCN 3A090 to read as follows")))
        world[lrs.index_url(*WINDOW, page=1, bis=True)] = (200, api([doc("2099-00001", WINDOW[0], "Fictional revisions")]))
        world[lrs.pdf_url(WINDOW[0], "2099-00001")] = (200, PDF_A)
        result, log, _ = run(world)
        self.assertEqual(lrs.outcome(result)[1], lrs.EXIT_REVIEW)
        row = next(line for line in log.splitlines() if line.startswith("| 2099-00001") and sha(PDF_A) in line)
        self.assertIn("3A090", row)
        self.assertIn("part 774", row)
        self.assertIn("Change Detector", log)
        self.assertIn("does not move", log)
        self.assertNotIn("none found in the searched window", log)

    # LS-3
    def test_ls3_a_refused_request_is_an_access_gap_never_none_found(self) -> None:
        world = quiet_world()
        world[lrs.index_url(*WINDOW, page=1, bis=True)] = (403, b"")
        result, log, _ = run(world)
        self.assertEqual(lrs.outcome(result)[1], lrs.EXIT_INCOMPLETE)
        gap = next(line for line in log.splitlines() if line.lower().startswith("- access gap:"))
        self.assertIn("www.federalregister.gov", gap)
        self.assertIn("403", gap)
        self.assertIn(NOW, gap)
        self.assertNotIn("none found", log)
        self.assertIn("must not move", log)

    # LS-4
    def test_ls4_a_missing_issue_is_a_gap_only_when_the_index_lists_documents(self) -> None:
        result, log, _ = run(quiet_world())
        self.assertIn("2026-03-02", log)
        self.assertEqual(result.gaps, [])
        world = quiet_world()
        world[lrs.issue_url("2026-02-27")] = (302, b"")
        result, log, _ = run(world)
        self.assertEqual(lrs.outcome(result)[1], lrs.EXIT_INCOMPLETE)
        self.assertTrue(any("2026-02-27" in g and "302" in g for g in result.gaps), result.gaps)

    # LS-5
    def test_ls5_a_changed_registered_text_is_reported(self) -> None:
        world = quiet_world()
        world[REG_URL] = (200, PDF_REG + b"changed")
        result, log, _ = run(world)
        self.assertEqual(lrs.outcome(result)[1], lrs.EXIT_REVIEW)
        row = next(line for line in log.splitlines() if line.startswith("| src-900"))
        self.assertIn("CHANGED", row)
        self.assertIn(sha(PDF_REG + b"changed"), row)
        self.assertIn(REGISTERED[0][2], row)

    # LS-6
    def test_ls6_registers_that_disagree_are_listed(self) -> None:
        world = quiet_world()
        world[lrs.index_url(*WINDOW, page=1, bis=True)] = (200, api([
            doc("2099-00002", WINDOW[0], "Order Denying Export Privileges", "Notice"),
            doc("2099-00009", WINDOW[0], "Fictional rule absent from the edition")]))
        result, log, _ = run(world)
        self.assertEqual(lrs.outcome(result)[1], lrs.EXIT_REVIEW)
        self.assertTrue(any("2099-00009" in d for d in result.disagreements), result.disagreements)

    # LS-7
    def test_ls7_the_window_is_checked(self) -> None:
        with self.assertRaises(ValueError):
            run(quiet_world(), ("2026-03-02", "2026-02-27"))
        with self.assertRaises(ValueError):
            run(quiet_world(), ("2026-03-02", "2026-03-05"))

    # LS-8
    def test_ls8_terms_come_from_their_homes(self) -> None:
        entries = lrs.entries_from_rules((REPO_ROOT / "docs/research/change-detection.md").read_text(encoding="utf-8"))
        self.assertEqual(set(entries), {"3A090", "3B001", "3B002", "3B993", "3B090"})
        policies = json.loads((REPO_ROOT / "data/policies.json").read_text(encoding="utf-8"))
        acts = lrs.acts_from_policies(policies)
        held = {p["id"][len("policy-us-fr-"):] for p in policies if p["id"].startswith("policy-us-fr-")}
        self.assertEqual({number for _, number in acts}, held)
        citations = {a["value"] for p in policies if p["id"].startswith("policy-us-fr-") for a in p.get("official_citation", [])}
        self.assertEqual({citation for citation, _ in acts}, citations)
        names = {t.name for t in lrs.make_terms(entries, acts)}
        self.assertTrue(set(entries) | held | citations | {"Artificial Intelligence Diffusion"} <= names)

    # LS-9
    def test_ls9_the_command_line_writes_only_its_log(self) -> None:
        guarded = [REPO_ROOT / "docs/research/change-detection.md", *sorted((REPO_ROOT / "data").rglob("*.json"))]
        before = {p: sha(p.read_bytes()) for p in guarded}
        world = quiet_world()
        tmp = Path(tempfile.mkdtemp())
        try:
            recorded = tmp / "recorded"
            lrs.write_recording(recorded, {u: lrs.Response(u, s, b, NOW) for u, (s, b) in world.items()})
            # the real terms and registered texts are read from the repository; serve what they ask as refusals
            log = tmp / "run.md"
            code = lrs.main(["--from", WINDOW[0], "--to", WINDOW[1], "--replay", str(recorded), "--log", str(log)])
            self.assertIn(code, (lrs.EXIT_NONE, lrs.EXIT_REVIEW, lrs.EXIT_INCOMPLETE))
            self.assertTrue(log.is_file())
            inside = REPO_ROOT / "docs" / "research" / "not-the-log-folder.md"
            with self.assertRaises(SystemExit):
                lrs.main(["--from", WINDOW[0], "--to", WINDOW[1], "--replay", str(recorded), "--log", str(inside)])
            self.assertFalse(inside.exists())
        finally:
            shutil.rmtree(tmp)
        self.assertEqual(before, {p: sha(p.read_bytes()) for p in guarded})

    # LS-10
    def test_ls10_fewer_results_than_the_count_is_an_access_gap(self) -> None:
        world = quiet_world()
        world[lrs.index_url(*WINDOW, page=1, bis=True)] = (200, api([doc("2099-00002", WINDOW[0], "Order", "Notice")], count=2))
        result, _, _ = run(world)
        self.assertEqual(lrs.outcome(result)[1], lrs.EXIT_INCOMPLETE)
        self.assertTrue(any("1 of 2" in g for g in result.gaps), result.gaps)

    # LS-11
    def test_ls11_repeal_words_select_bis_rules_not_notices(self) -> None:
        result, _, _ = run(quiet_world())
        self.assertNotIn("2099-00002", {c.number for c in result.candidates})
        world = quiet_world()
        world[lrs.issue_url("2026-02-27")] = (200, issue(
            ("RULE", "DEPARTMENT OF COMMERCE", "Bureau of Industry and Security", "15 CFR Part 744",
             "2099-00004 this rule rescinds a fictional provision")))
        world[lrs.index_url(*WINDOW, page=1, bis=True)] = (200, api([doc("2099-00004", WINDOW[0], "Fictional rescission")]))
        world[lrs.pdf_url(WINDOW[0], "2099-00004")] = (200, PDF_A)
        result, _, _ = run(world)
        self.assertIn("2099-00004", {c.number for c in result.candidates})


if __name__ == "__main__":
    unittest.main()
