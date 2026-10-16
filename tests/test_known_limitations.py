"""v1.0's known limitations agree with the pages (S24, D-222, D-223).

`docs/known-limitations.md` (the Portfolio Reviewer's) states each gap and each boundary of v1.0 once, and says where
the pages state it. These checks (the Data Auditor's) compare the document with the built pages without reading prose
for meaning: they compare exact sentences.

- KL-1 the document has its four tables, every row has an ID of its section's form, IDs are unique and no cell is empty;
- KL-2 every gap and boundary names at least one place where the pages state it, or says "none" and why; every
  statement names an existing row;
- KL-3 a `framing` statement is found, whole, in an Atlas framing block of every page its path names; a `label`
  statement is found in the text of every page its path names; a path names at least one page;
- KL-4 every sentence of the pages' limits framing (the framing blocks in the method, limits, gaps and not-tracked
  sections, and the brief's out-of-scope box) is held by a `framing` statement or an explanation entry for that page:
  a limit added to a page and missing from the document fails here;
- KL-5 every explanation entry is found on a page it names, so the list cannot go stale;
- KL-6 every gap D-218 sends to S25 as a known limitation has a row (its key);
- KL-7 every link in the record column resolves to a file, and every decision it cites exists;
- KL-8 the descriptive columns restate no canonical value: no ISO date and no record ID (one home per fact).

Standard library only.
"""

from __future__ import annotations

import fnmatch
import html
import html.parser
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC = REPO_ROOT / "docs/known-limitations.md"
DECISIONS = REPO_ROOT / "docs/architecture/decisions.md"

# The gaps D-218 sends to S25 as v1.0 known limitations (C-8, DT-S23-5), with DT-S23-3's coverage statement: each
# must be the key of a row in "Gaps".
D218_KEYS = {
    "ear-dates",               # the EAR's own dates
    "bis-guidance-2026-05",    # the May 2026 BIS guidance, held only as an address
    "h100-supplier-current",   # a current H100 memory supplier
    "h100-fabricator",         # the H100's fabricator (cand-001, refused as not fresh)
    "trainium2-recognised",    # a recognised source for Trainium2's memory maker
    "aged-values",             # newer evidence for values past the freshness horizon
    "single-voice",            # DT-S23-3: no value rests on two independent publishers
    "coverage",                # DT-S23-3: narrow coverage
}
GAP_ID = re.compile(r"KL-\d{2}")
BOUNDARY_ID = re.compile(r"KB-\d{2}")
KINDS = {"framing", "label", "none"}
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z“\"])")
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
# A record ID: a numbered source or candidate, or a typed slug of two or more parts ("product-nvidia-h100"), never a
# hyphenated word such as "product-level".
RECORD_ID = re.compile(r"\b(?:(?:src|cand)-\d{3}|(?:claim|company|product|component|technology|policy|event|rel|"
                       r"jurisdiction|facility)-[a-z0-9]+(?:-[a-z0-9]+)+)\b")
LIMIT_REGIONS = {("section", "limits"), ("section", "method"), ("section", "gaps"), ("section", "not-tracked")}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def norm(text: str) -> str:
    text = html.unescape(text).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip()


class Framing(html.parser.HTMLParser):
    """The text of every Atlas framing block on a page, and which of them lie in a limits region. The framing tag
    ("Atlas framing") and headings inside a block are left out."""

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[bool] = []          # per open element: is it a limits region
        self.block: list[str] | None = None
        self.depth = 0
        self.skip_depth = 0
        self.blocks: list[tuple[str, bool]] = []
        self.text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        region = (tag, a.get("id")) in LIMIT_REGIONS or (tag == "div" and "data-limits" in a)
        self.stack.append(region)
        if self.block is None and tag == "div" and "data-framing" in a:
            self.block, self.depth, self.in_region = [], len(self.stack), any(self.stack[:-1])
        elif self.block is not None and not self.skip_depth and (
                tag in {"h2", "h3", "h4"} or "framing-tag" in (a.get("class") or "").split()):
            self.skip_depth = len(self.stack)

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        if self.skip_depth == len(self.stack):
            self.skip_depth = 0
        if self.block is not None and self.depth == len(self.stack):
            self.blocks.append((norm(" ".join(self.block)), self.in_region))
            self.block = None
        self.stack.pop()

    def handle_data(self, data):
        self.text.append(data)
        if self.block is not None and not self.skip_depth:
            self.block.append(data)


def page_parts(path: Path) -> tuple[list[str], list[str], str]:
    """(every framing block, the limits framing blocks, the page's whole text), normalised."""
    p = Framing()
    p.feed(path.read_text(encoding="utf-8"))
    return [b for b, _ in p.blocks], [b for b, r in p.blocks if r], norm(" ".join(p.text))


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(text: str, heading: str) -> list[list[str]]:
    """The rows of the first table under a level-2 heading, header and rule left out."""
    body = text.partition(f"\n## {heading}\n")[2].split("\n## ")[0]
    lines = [ln for ln in body.splitlines() if ln.startswith("|")]
    return [cells(ln) for ln in lines[2:]]


def unquote(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] in "\"“" and text[-1] in "\"”":
        text = text[1:-1]
    return norm(text)


def pages_matching(pattern: str) -> list[Path]:
    site = sorted(p.relative_to(REPO_ROOT).as_posix() for p in (REPO_ROOT / "site").rglob("index.html"))
    return [REPO_ROOT / p for p in site if fnmatch.fnmatchcase(p, pattern)]


def load() -> dict:
    text = DOC.read_text(encoding="utf-8") if DOC.is_file() else ""
    return {
        "text": text,
        "gaps": table(text, "Gaps"),
        "boundaries": table(text, "Boundaries by design"),
        "stated": table(text, "Where the pages state each limit"),
        "explained": table(text, "Framing sentences that explain rather than limit"),
    }


def path_of(cell: str) -> str:
    return cell.strip().strip("`")


class KnownLimitationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.doc = load()
        cls.pages = {p.relative_to(REPO_ROOT).as_posix(): page_parts(p) for p in (REPO_ROOT / "site").rglob("index.html")}

    def test_kl1_the_document_has_its_tables_and_well_formed_rows(self) -> None:
        self.assertTrue(DOC.is_file(), "docs/known-limitations.md is missing (D-222)")
        d = self.doc
        for name, rows, width in (("Gaps", d["gaps"], 7), ("Boundaries by design", d["boundaries"], 7),
                                  ("Where the pages state each limit", d["stated"], 4),
                                  ("Framing sentences that explain rather than limit", d["explained"], 2)):
            with self.subTest(table=name):
                self.assertTrue(rows, f"the table under '## {name}' is missing or empty")
                for row in rows:
                    self.assertEqual(len(row), width, f"{name}: a row has {len(row)} cells, not {width}: {row[:2]}")
                    self.assertTrue(all(c for c in row), f"{name}: an empty cell in {row[:2]}")
        ids = [r[0] for r in d["gaps"]] + [r[0] for r in d["boundaries"]]
        self.assertEqual(len(ids), len(set(ids)), "a row ID is used twice")
        for r in d["gaps"]:
            self.assertRegex(r[0], GAP_ID.pattern + "$")
        for r in d["boundaries"]:
            self.assertRegex(r[0], BOUNDARY_ID.pattern + "$")
        for r in d["stated"]:
            self.assertIn(r[2], KINDS, f"statement for {r[0]}: kind {r[2]!r} is not one of {sorted(KINDS)}")

    def test_kl2_every_row_says_where_the_pages_state_it(self) -> None:
        ids = {r[0] for r in self.doc["gaps"] + self.doc["boundaries"]}
        stated = {r[0] for r in self.doc["stated"]}
        self.assertEqual(sorted(ids - stated), [], "rows with no statement (name a page, or 'none' and why)")
        self.assertEqual(sorted(stated - ids), [], "statements naming no row")
        for r in self.doc["stated"]:
            if r[2] == "none":
                self.assertEqual(r[1], "—", f"{r[0]}: a 'none' statement names no page")
            else:
                self.assertNotEqual(r[1], "—", f"{r[0]}: a {r[2]} statement must name a page")

    def test_kl3_each_statement_is_on_the_pages_it_names(self) -> None:
        for row, page, kind, quoted in self.doc["stated"]:
            if kind == "none":
                continue
            text = unquote(quoted)
            matched = pages_matching(path_of(page))
            with self.subTest(row=row, page=page):
                self.assertTrue(matched, f"{row}: {page} names no built page")
                for p in matched:
                    rel = p.relative_to(REPO_ROOT).as_posix()
                    blocks, _, whole = self.pages[rel]
                    if kind == "framing":
                        self.assertTrue(any(text in b for b in blocks),
                                        f"{row}: the framing {text!r} is not on {rel} (known-limitations.md and the page disagree)")
                    else:
                        self.assertIn(text, whole, f"{row}: the label {text!r} is not on {rel}")

    def test_kl4_every_limit_the_pages_state_is_in_the_document(self) -> None:
        held = [(path_of(r[1]), unquote(r[3])) for r in self.doc["stated"] if r[2] == "framing"]
        held += [(path_of(r[0]), unquote(r[1])) for r in self.doc["explained"]]
        missing = []
        for rel, (_, limits, _) in sorted(self.pages.items()):
            for block in limits:
                for sentence in SENTENCE.split(block):
                    if not any(fnmatch.fnmatchcase(rel, pat) and sentence in text for pat, text in held):
                        missing.append(f"{rel}: {sentence!r}")
        self.assertEqual(missing, [], "limits the pages state that docs/known-limitations.md does not hold (D-222)")

    def test_kl5_every_explanation_entry_is_on_a_page_it_names(self) -> None:
        for page, quoted in self.doc["explained"]:
            text = unquote(quoted)
            with self.subTest(text=text[:60]):
                matched = [p.relative_to(REPO_ROOT).as_posix() for p in pages_matching(path_of(page))]
                self.assertTrue(matched, f"{page} names no built page")
                self.assertTrue(any(text in b for rel in matched for b in self.pages[rel][1]),
                                f"the explanation {text!r} is in no limits framing on {page}: remove it or correct it")

    def test_kl6_every_gap_d218_sends_to_s25_has_a_row(self) -> None:
        keys = {r[1].strip("`") for r in self.doc["gaps"]}
        self.assertEqual(sorted(D218_KEYS - keys), [], "gaps D-218 sends to S25 with no row in known-limitations.md")

    def test_kl7_the_records_resolve(self) -> None:
        decisions = set(re.findall(r"^## (D-\d{3}) ", DECISIONS.read_text(encoding="utf-8"), flags=re.M))
        for r in self.doc["gaps"] + self.doc["boundaries"]:
            with self.subTest(row=r[0]):
                for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", r[6]):
                    self.assertTrue((DOC.parent / target).resolve().is_file(), f"{r[0]}: link {target} does not resolve")
                for did in re.findall(r"D-\d{3}", r[6]):
                    self.assertIn(did, decisions, f"{r[0]}: {did} is not in decisions.md")

    def test_kl8_no_canonical_value_is_restated(self) -> None:
        for r in self.doc["gaps"] + self.doc["boundaries"]:
            for cell in r[2:6]:
                with self.subTest(row=r[0]):
                    self.assertIsNone(ISO_DATE.search(cell), f"{r[0]} restates a date: {cell!r} (link the record instead)")
                    self.assertIsNone(RECORD_ID.search(cell), f"{r[0]} names a record ID in prose: {cell!r} (use the record column)")


if __name__ == "__main__":
    unittest.main()
