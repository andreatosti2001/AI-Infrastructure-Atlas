"""The published address serves the release commit's pages and every file they link to (S25, D-226, D-227).

`tools/check_published.py` (the Data Auditor's) compares what an address serves with the committed files, byte for
byte. These tests run it against a local server on this machine, never the network: the repository as committed,
then the same with one planted difference at a time.

- PA-1 each page under `site/` is served at its path under the address and equals the committed page;
- PA-2 each file a page links to by a relative link (inside or outside `site/`) is served and equals the committed file;
- PA-3 the check covers every page and every relative link target, counted here independently of the tool;
- PW-1 the publication workflow runs only by hand, refuses a commit without a release tag, runs `tools/check_all.py`
  before it publishes, publishes the commit's tracked files, and checks the published address afterwards with the
  tool and the five browser scripts.

Standard library only.
"""

from __future__ import annotations

import functools
import http.server
import importlib.util
import os
import re
import threading
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github/workflows/pages.yml"

spec = importlib.util.spec_from_file_location("check_published", REPO_ROOT / "tools/check_published.py")
check_published = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_published)

BRIEF = "site/briefs/accelerator-memory/index.html"
CLAIMS = "data/claims.json"


class Served:
    """A local server for the repository's files, with planted differences: {path: bytes} serves other bytes,
    {path: None} answers 404."""

    def __init__(self, planted: dict[str, bytes | None] | None = None) -> None:
        planted = planted or {}

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                rel = self.path.split("?")[0].split("#")[0].lstrip("/")
                if rel in planted:
                    body = planted[rel]
                    if body is None:
                        self.send_error(404)
                        return
                    self.send_response(200)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return
                super().do_GET()

            def log_message(self, *args):
                pass

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Handler, directory=str(REPO_ROOT)))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self) -> str:
        self.thread.start()
        return f"http://127.0.0.1:{self.server.server_address[1]}/"

    def __exit__(self, *exc) -> None:
        self.server.shutdown()
        self.server.server_close()


def failures_with(planted=None) -> list[str]:
    with Served(planted) as base:
        return check_published.check(base)["failures"]


class TestPublished(unittest.TestCase):
    # PA-1, PA-2
    def test_pa1_pa2_the_committed_tree_passes(self) -> None:
        self.assertEqual(failures_with(), [])

    # PA-1
    def test_pa1_a_page_whose_bytes_differ_fails_by_name(self) -> None:
        page = (REPO_ROOT / BRIEF).read_bytes().replace(b"</h1>", b" (draft)</h1>", 1)
        failures = failures_with({BRIEF: page})
        self.assertEqual(len(failures), 1, failures)
        self.assertIn(f"PA-1 {BRIEF}: served bytes differ from the committed page", failures[0])

    # PA-1
    def test_pa1_a_page_not_served_fails_by_name(self) -> None:
        failures = failures_with({BRIEF: None})
        self.assertEqual(len(failures), 1, failures)
        self.assertIn(f"PA-1 {BRIEF}: not served (HTTP 404)", failures[0])

    # PA-2
    def test_pa2_a_linked_file_whose_bytes_differ_fails_by_name(self) -> None:
        failures = failures_with({CLAIMS: (REPO_ROOT / CLAIMS).read_bytes() + b"\n"})
        self.assertEqual(failures, [f"PA-2 {CLAIMS}: served bytes differ from the committed file"])

    # PA-2
    def test_pa2_a_linked_file_not_served_fails_by_name(self) -> None:
        self.assertEqual(failures_with({CLAIMS: None}), [f"PA-2 {CLAIMS}: not served (HTTP 404)"])

    # PA-1: the state before any deployment exists
    def test_pa1_an_address_that_serves_nothing_fails_every_page(self) -> None:
        nothing = {rel: None for rel in check_published.pages()}
        nothing.update({rel: None for rel in check_published.targets()})
        failures = failures_with(nothing)
        self.assertEqual(len([f for f in failures if f.startswith("PA-1 ")]), len(check_published.pages()))

    # PA-3
    def test_pa3_every_page_and_every_relative_link_target_is_covered(self) -> None:
        pages = sorted(str(p.relative_to(REPO_ROOT)) for p in (REPO_ROOT / "site").rglob("*.html"))
        targets = set()
        for page in pages:
            for href in re.findall(r'(?:href|src)="([^"]*)"', (REPO_ROOT / page).read_text(encoding="utf-8")):
                if href.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I):
                    continue
                targets.add(os.path.normpath(os.path.join(os.path.dirname(page), href.split("#")[0])))
        self.assertEqual(sorted(check_published.pages()), pages)
        self.assertEqual(set(check_published.targets()), targets - set(pages))
        self.assertTrue(any(not t.startswith("site/") for t in targets), "no target outside site/: the test reads nothing")


class TestPagesWorkflow(unittest.TestCase):
    # PW-1
    def test_pw1_the_workflow_publishes_only_a_checked_tagged_commit_and_checks_the_address(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        triggers = re.search(r"^on:\n((?:  .*\n)+)", text, re.M)
        self.assertIsNotNone(triggers, "the workflow names no trigger")
        self.assertEqual(re.findall(r"^  (\w+):", triggers.group(1), re.M), ["workflow_dispatch"],
                         "the workflow must run only by hand")
        steps = [
            ("the tag guard", r"git tag --points-at HEAD --list 'v\*'"),
            ("check_all.py", r"python tools/check_all\.py"),
            ("the tracked tree", r"git archive HEAD"),
            ("the upload", r"uses: actions/upload-pages-artifact@"),
            ("the deployment", r"uses: actions/deploy-pages@"),
            ("the address check", r"python tools/check_published\.py"),
        ]
        at = [(name, re.search(pattern, text)) for name, pattern in steps]
        self.assertEqual([name for name, m in at if m is None], [], "a step of the publication is missing")
        self.assertEqual([name for name, m in sorted(at, key=lambda x: x[1].start())], [name for name, _ in steps],
                         "the steps run out of order")
        for script in ("hbm-chain", "hbm-insight", "journeys", "brief", "filter"):
            self.assertIn(f"node tests/browser/{script}.qa.js", text[at[-1][1].start():],
                          f"the published address is not checked by {script}.qa.js")
        self.assertIn("QA_BASE_URL", text)


if __name__ == "__main__":
    unittest.main()
