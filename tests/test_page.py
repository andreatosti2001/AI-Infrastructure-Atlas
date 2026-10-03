"""Page checks for the S11 vertical slice: validate-design for site/hbm-chain/index.html.

S11 (vertical-slice.md §4, §8; D-105). Standard library only. The page must make five things
impossible (S11 prompt, Part B §02): a mark, label or sentence with no record behind it; a value
typed by hand; a gap drawn as absence or zero; a staging record shown as canonical; an inference
shown without its label. The checks read the committed page and the data with their own loader,
never the build's, and recompute every value the page shows:

PG-1  every text node sits inside a record value, an absent value, a fixed label, a derived value
      or a framing block;
PG-2  every record value equals its home in data/ (the refused candidates included, S12), the
      schemas, the rule documents or decisions.md; every claim card and source shows its type, status, dates and citations;
PG-3  every mark targets a canonical record, edge or claim and links to its evidence panel; no
      staging ID appears;
PG-4  an edge is drawn as inferred exactly when no cited claim is a FACT, says so, and its panel
      shows the reasoning;
PG-5  every chain edge is drawn; every unknown supplier and recorded gap is drawn with its state;
      "none" never appears; no refused candidate is drawn in the diagram, and each candidate the
      journey names is a card under each of its reasons (S12, D-109);
PG-6  framing is visibly marked and names no record;
PG-7  the committed page equals a rebuild, and two builds are identical;
PG-8  accessibility basics, the palette and its contrast;
PG-9  links resolve and the page loads nothing from the network;
PG-10 the journey specification matches its homes;
PG-11 (S14, D-115, D-121) the SQL table equals its committed result cell by cell, every result row is
      shown, its caveats appear exactly where the result has them, and its "How this was computed"
      tutorial, beside it and closed by default, is the query file the result records.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGE = REPO_ROOT / "site" / "hbm-chain" / "index.html"
DATA = REPO_ROOT / "data"
sys.path.insert(0, str(REPO_ROOT / "tools"))

import navigate  # noqa: E402

# The build's inputs, as vertical-slice.md §6 defines them: every data file (the refused candidates
# included), every schema, the documents the page quotes rules and rulings from, the template and the
# three tools that compute it. edge-dataset.md left the list in S12 (D-109).
INPUT_GLOBS = ("data/*.json", "data/staging/*.json", "schemas/*.json", "sql/*.sql", "sql/results/*.json")
INPUT_FILES = (
    "docs/architecture/company-dataset.md",
    "docs/architecture/decisions.md",
    "docs/architecture/relationship-taxonomy.md",
    "docs/research/source-policy.md",
    "tools/build_page.py",
    "tools/navigate.py",
    "tools/page_template.html",
    "tools/trace.py",
)
ANNOTATIONS = ("data-ref", "data-label", "data-derived", "data-framing")
# The first SQL result on the page (S14, H-3) and the fixed words of its caveat flags (PG-11).
SQL_QUERY = "accelerator_dependencies"
SQL_FLAGS = {"rests_on_atlas_interpretation": "rests on the Atlas’s own definitions", "publishers": "one publisher only"}
SQL_SHOWN = ("accelerator", "from_name", "relation", "to_name", "basis", "evidence_dated_from", "record_id", "reached_through", "accelerator_class_claim")
SQL_LISTS = ("claim_ids", "source_ids", "publishers", "party_standing_unchecked")
BARE = re.compile(r"^[\s·→←↓,.;:()\[\]/—–\-\"“”'‘’…+#?!]*$")
FORMATS = {None: lambda value: value, "state": lambda value: value.replace("_", " ")}
FRAMING_MARK = "Atlas framing"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def norm(text: str) -> str:
    return " ".join(text.split())


# --- a minimal DOM ---------------------------------------------------------------------------


class Node:
    def __init__(self, tag: str, attrs: dict, parent: "Node | None") -> None:
        self.tag, self.attrs, self.parent = tag, attrs, parent
        self.children: list = []

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def texts(self):
        """(text, parent) for every text node below this node."""
        for child in self.children:
            if isinstance(child, Node):
                yield from child.texts()
            else:
                yield child, self

    def text(self) -> str:
        return norm("".join(t for t, _ in self.texts()))

    def ancestors(self):
        node = self
        while node is not None:
            yield node
            node = node.parent

    def annotated(self) -> "Node | None":
        return next((n for n in self.ancestors() if any(a in n.attrs for a in ANNOTATIONS)), None)


class Tree(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Node(tag, dict(attrs), self.current))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is self.root:
            raise AssertionError(f"unmatched </{tag}>")
        self.current = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def parse(text: str) -> Node:
    tree = Tree()
    tree.feed(text)
    tree.close()
    assert tree.current is tree.root, f"unclosed <{tree.current.tag}>"
    return tree.root


# --- the homes, read independently of the build ----------------------------------------------


def load(path: Path) -> list:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


# Data files whose rows are about records and have no ID of their own (S14, DT-1, D-117): never a home.
NOT_HOMES = frozenset({"identity_basis.json"})


class Homes:
    def __init__(self, data: Path = DATA, root: Path = REPO_ROOT) -> None:
        self.canonical: dict[str, dict] = {}
        self.staging: dict[str, dict] = {}
        for path in sorted(p for p in data.glob("*.json") if p.name not in NOT_HOMES):
            for record in load(path):
                self.canonical[record["id"]] = record
        for path in sorted(p for p in (data / "staging").glob("*.json") if p.name not in NOT_HOMES):
            for record in load(path):
                self.staging[record["id"]] = record
        self.schemas = {p.name.split(".")[0]: json.loads(p.read_text(encoding="utf-8")) for p in (root / "schemas").glob("*.json")}
        decisions = (root / "docs/architecture/decisions.md").read_text(encoding="utf-8")
        self.decisions = {m.group(1): m.group(2).strip() for m in re.finditer(r"^## (D-\d{3}) — (.+)$", decisions, re.M)}
        # a rule code's one-line home: the bold rule of its table row, or the **Rule** paragraph of the
        # section titled with it (vertical-slice.md §5; D-108)
        self.rules: dict[str, str] = {}
        for path in ("docs/research/source-policy.md", "docs/architecture/relationship-taxonomy.md", "docs/architecture/company-dataset.md"):
            text = (root / path).read_text(encoding="utf-8")
            for m in re.finditer(r"^\| ((?:ER|RR|F)-\d+) \| \*\*(.+?)\*\*", text, re.M):
                self.rules[m.group(1)] = m.group(2).replace("`", "")
            for m in re.finditer(r"^## [^\n]*\(((?:ER|RR|F)-\d+)\)\n\n\*\*Rule\*\* \([^)]*\)\. (.+?)\n\n", text, re.M | re.S):
                self.rules[m.group(1)] = " ".join(m.group(2).split()).replace("`", "")
        self.names: set[str] = set()
        for record in self.canonical.values():
            if "type" in record and "name" in record:
                self.names.add(record["name"])
                self.names.update(record.get("aliases", []))

    @staticmethod
    def pointer(value, path: str):
        for part in [p for p in path.split("/") if p]:
            value = value[int(part)] if isinstance(value, list) else value[part]
        return value

    def resolve(self, ref: str, field: str):
        if ref.startswith("schema:"):
            stem, _, rest = ref[len("schema:") :].partition("#")
            name, _, const = rest.partition("/")
            node = self.schemas[stem]["$defs"][name]
            if const:
                node = next(item for item in node["oneOf"] if item.get("const") == const)
            return self.pointer(node, field)
        if ref.startswith("doc:rules#"):
            code = ref[len("doc:rules#") :]
            if field == "code":
                return code if code in self.rules else self.rules[code]
            assert field == "rule", field
            return self.rules[code]
        if ref.startswith("doc:decisions#"):
            key = ref[len("doc:decisions#") :]
            if field == "id":
                return key if key in self.decisions else self.decisions[key]
            assert field == "title", field
            return self.decisions[key].replace("`", "")
        return self.pointer(self.canonical[ref], field)

    def has(self, ref: str, field: str) -> bool:
        try:
            self.resolve(ref, field)
            return True
        except (KeyError, IndexError, StopIteration, ValueError):
            return False


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


def input_digest(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.encode("utf-8") + b"\0" + hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest().encode("ascii") + b"\n")
    return digest.hexdigest()


def luminance(hex_colour: str) -> float:
    rgb = [int(hex_colour[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def build_module():
    import build_page  # noqa: PLC0415 (imported late: the checks are written before the build)

    return build_page


# --- the checks ------------------------------------------------------------------------------


class PageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
        cls.root = parse(cls.raw) if cls.raw else Node("#root", {}, None)
        cls.homes = Homes()
        cls.nodes = list(cls.root.walk())
        cls.by_id = {n.attrs["id"]: n for n in cls.nodes if "id" in n.attrs}
        body = [n for n in cls.nodes if n.tag == "body"]
        cls.body = body[0] if body else Node("body", {}, None)
        cls.marks = [n for n in cls.nodes if n.tag == "a" and "data-mark" in n.attrs]
        cls.atlas = navigate.Atlas(DATA, False)

    def setUp(self) -> None:
        if not self.raw:
            self.fail(f"the page is not built: {PAGE.relative_to(REPO_ROOT)} (python tools/build_page.py)")

    def visible_texts(self):
        for text, parent in self.body.texts():
            if parent.tag in ("style", "script"):
                continue
            yield text, parent

    def refs(self, field: str | None = None):
        return [n for n in self.nodes if "data-ref" in n.attrs and (field is None or n.attrs.get("data-field") == field)]

    # PG-1
    def test_pg1_every_text_node_has_a_home(self) -> None:
        labels = set(build_module().LABELS)
        for text, parent in self.visible_texts():
            if BARE.match(text):
                continue
            owner = parent.annotated()
            with self.subTest(text=norm(text)[:80]):
                self.assertIsNotNone(owner, "text with no record, label, derived value or framing behind it")
                if "data-label" in owner.attrs:
                    self.assertIn(owner.text(), labels, "a label that is not one of the build's labels")
        for node in self.nodes:
            if "data-ref" in node.attrs or "data-label" in node.attrs or "data-derived" in node.attrs:
                inner = [n for n in node.walk() if n is not node and any(a in n.attrs for a in ANNOTATIONS)]
                with self.subTest(leaf=node.attrs.get("data-ref") or node.text()[:40]):
                    self.assertEqual(inner, [], "an annotated value must not contain another")

    def test_pg1_labels_carry_no_fact(self) -> None:
        for label in build_module().LABELS:
            with self.subTest(label=label):
                self.assertNotRegex(label, r"\d", "a label holds a digit")
                self.assertNotRegex(label.lower(), r"\bnone\b")
                for name in self.homes.names:
                    self.assertNotRegex(label, rf"(?<![\w-]){re.escape(name)}(?![\w-])", f"a label names a record ({name})")

    # PG-2
    def test_pg2_every_record_value_equals_its_home(self) -> None:
        values = self.refs()
        self.assertTrue(values)
        labels = set(build_module().LABELS)
        for node in values:
            ref, field = node.attrs["data-ref"], node.attrs.get("data-field")
            with self.subTest(ref=ref, field=field):
                self.assertIsNotNone(field, "data-ref without data-field")
                if "data-absent" in node.attrs:
                    self.assertFalse(self.homes.has(ref, field), "drawn as absent, but the field exists")
                    self.assertIn(node.text(), labels)
                    continue
                self.assertTrue(self.homes.has(ref, field), "no such home")
                value = self.homes.resolve(ref, field)
                self.assertIsInstance(value, (str, int, float), "a value must be a scalar")
                expected = norm(FORMATS[node.attrs.get("data-format")](str(value)))
                self.assertEqual(node.text(), expected)
                if node.tag == "a" and field == "/url":
                    self.assertEqual(node.attrs.get("href"), value)

    def test_pg2_claims_and_sources_are_shown_whole(self) -> None:
        shown = {(n.attrs["data-ref"], n.attrs["data-field"]) for n in self.refs()}
        claims = {ref for ref, field in shown if field == "/statement"}
        self.assertTrue(claims)
        for claim_id in sorted(claims):
            claim = self.homes.canonical[claim_id]
            with self.subTest(claim=claim_id):
                for field in ("/claim_type", "/evidence_status", "/verified_on", "/review/verdict", "/review/reviewed_on"):
                    self.assertIn((claim_id, field), shown)
                for index, citation in enumerate(claim.get("citations", [])):
                    for field in ("anchor", "locator", "standing", "read/accessed_at"):
                        self.assertIn((claim_id, f"/citations/{index}/{field}"), shown)
                    source_id = citation["source_id"]
                    for field in ("/title", "/publisher", "/source_class", "/url", "/retrieval/accessed_at"):
                        self.assertIn((source_id, field), shown)
                    dates = self.homes.canonical[source_id]["stated_dates"]
                    fields = ["/stated_dates/state"] if isinstance(dates, dict) else [f"/stated_dates/{i}/date" for i in range(len(dates))]
                    for field in fields:
                        self.assertIn((source_id, field), shown)
                if claim["claim_type"] in ("DERIVATION", "INTERPRETATION", "IMPLICATION"):
                    self.assertIn((claim_id, "/reasoning"), shown)
                for input_id in claim.get("input_claim_ids", []):
                    self.assertIn((input_id, "/statement"), shown)

    def test_pg2_every_instance_edge_shows_its_period(self) -> None:
        shown = {(n.attrs["data-ref"], n.attrs["data-field"], "data-absent" in n.attrs) for n in self.refs()}
        for mark in self.marks:
            if mark.attrs["data-mark"] != "edge":
                continue
            edge = self.homes.canonical[mark.attrs["data-target"]]
            if navigate.VOCAB[edge["relation_type"]]["x-level"] != "instance":
                continue
            with self.subTest(edge=edge["id"]):
                if "valid_from" in edge:
                    self.assertIn((edge["id"], "/valid_from", False), shown)
                else:
                    self.assertIn((edge["id"], "/valid_from", True), shown)

    def test_pg2_derived_values(self) -> None:
        derived = [n for n in self.nodes if "data-derived" in n.attrs]
        kinds = {n.attrs["data-derived"] for n in derived}
        self.assertLessEqual(kinds, {"input-file", "input-digest", "verified-first", "verified-last", "accessed-first", "accessed-last", "pointer", "bytes-match", "no-activity-edge", "lane-unlinked", "rule-home", "sql-cell", "sql-flag", "sql-question", "sql-reading", "sql-step-title", "sql-step-text", "sql-step-code", "sql-file", "sql-digest"})
        files = [n.text() for n in derived if n.attrs["data-derived"] == "input-file"]
        self.assertEqual(sorted(files), input_paths())
        digests = [n.text() for n in derived if n.attrs["data-derived"] == "input-digest"]
        self.assertEqual(digests, [input_digest(input_paths())])
        claims = {n.attrs["data-ref"] for n in self.refs("/statement")}
        sources = {n.attrs["data-ref"] for n in self.refs("/title")}
        verified = sorted(self.homes.canonical[c]["verified_on"] for c in claims)
        accessed = sorted(self.homes.canonical[s]["retrieval"]["accessed_at"] for s in sources)
        expected = {"verified-first": verified[0], "verified-last": verified[-1], "accessed-first": accessed[0], "accessed-last": accessed[-1]}
        labels = build_module().LABELS
        for word in ("same bytes as registered", "bytes changed since registration", "no recorded relationship", "not linked to any accelerator on this chain"):
            self.assertIn(word, labels)
        for node in derived:
            kind = node.attrs["data-derived"]
            with self.subTest(kind=kind, target=node.attrs.get("data-target")):
                if kind in expected:
                    self.assertEqual(node.text(), expected[kind])
                elif kind == "pointer":
                    record = self.homes.canonical[node.attrs["data-target"]]
                    self.assertIn(node.attrs["data-claim"], Homes.pointer(record, node.text()))
                elif kind == "bytes-match":
                    claim = self.homes.canonical[node.attrs["data-target"]]
                    citation = claim["citations"][int(node.attrs["data-index"])]
                    registered = self.homes.canonical[citation["source_id"]]["retrieval"]["sha256"]
                    same = citation["read"]["sha256"].startswith(registered) or registered.startswith(citation["read"]["sha256"])
                    self.assertEqual(node.text(), ("same bytes as registered" if same else "bytes changed since registration"))
                elif kind == "no-activity-edge":
                    self.assertEqual(self.atlas.actors_list(node.attrs["data-target"]), [])
                    self.assertEqual(node.text(), "no recorded relationship")
                elif kind == "rule-home":
                    home = (REPO_ROOT / node.text()).read_text(encoding="utf-8")
                    self.assertRegex(home, rf"(\| {re.escape(node.attrs['data-target'])} \||\({re.escape(node.attrs['data-target'])}\)\n)", "the rule is not defined where the page says")
                elif kind == "lane-unlinked":
                    self.assertEqual(node.text(), "not linked to any accelerator on this chain")

    # PG-11
    def sql_result(self) -> dict:
        return json.loads((REPO_ROOT / "sql" / "results" / f"{SQL_QUERY}.json").read_text(encoding="utf-8"))

    def test_pg11_the_sql_table_equals_its_result(self) -> None:
        rows = self.sql_result()["rows"]
        cells = [n for n in self.nodes if n.attrs.get("data-derived") == "sql-cell"]
        self.assertTrue(cells, "no SQL table on the page")
        shown: dict[int, dict[str, set]] = {}
        for node in cells:
            self.assertEqual(node.attrs.get("data-query"), SQL_QUERY)
            index, column = int(node.attrs["data-row"]), node.attrs["data-column"]
            value = rows[index][column]
            if "data-item" in node.attrs:
                value = value[int(node.attrs["data-item"])]
            text = str(value).replace("_", " ") if node.attrs.get("data-format") == "state" else str(value)
            with self.subTest(row=index, column=column):
                self.assertEqual(node.text(), norm(text))
            shown.setdefault(index, {}).setdefault(column, set()).add(node.attrs.get("data-item"))
        self.assertEqual(set(shown), set(range(len(rows))), "a result row is missing from the table, or the table has a row the result lacks")
        for index, row in enumerate(rows):
            with self.subTest(row=index):
                for column in SQL_SHOWN:
                    self.assertIn(column, shown[index], f"{column} is not shown")
                self.assertEqual("gap_reason" in shown[index], row["basis"] == "gap", "a gap's reason is shown exactly on a gap")
                self.assertEqual("evidence_dated_to" in shown[index], row["evidence_dated_to"] != row["evidence_dated_from"], "the second date is shown exactly when it differs")
                for column in SQL_LISTS:
                    self.assertEqual(shown[index].get(column, set()), {str(i) for i in range(len(row[column]))}, f"{column}: every item is shown once")
        flags = [n for n in self.nodes if n.attrs.get("data-derived") == "sql-flag"]
        got = sorted((int(n.attrs["data-row"]), n.attrs["data-column"], n.text()) for n in flags)
        want = sorted(
            [(i, "rests_on_atlas_interpretation", SQL_FLAGS["rests_on_atlas_interpretation"]) for i, r in enumerate(rows) if r["rests_on_atlas_interpretation"]]
            + [(i, "publishers", SQL_FLAGS["publishers"]) for i, r in enumerate(rows) if len(r["publishers"]) == 1]
        )
        self.assertEqual(got, want, "a caveat flag missing, or shown where the result does not have it")

    def test_pg11_the_tutorial_is_its_query_file(self) -> None:
        from test_warehouse import tutorial  # noqa: PLC0415 (the format's reader; standard library only)

        query = REPO_ROOT / "sql" / f"{SQL_QUERY}.sql"
        result = self.sql_result()
        self.assertEqual(result["query_sha256"], hashlib.sha256(query.read_bytes()).hexdigest(), "the result was computed from another version of the query file")
        t = tutorial(query.read_text(encoding="utf-8"))
        tutorials = [n for n in self.nodes if n.tag == "details" and "sql-tutorial" in n.attrs.get("class", "").split()]
        self.assertEqual(len(tutorials), 1)
        box = tutorials[0]
        self.assertNotIn("open", box.attrs, "the tutorial is closed by default")
        summary = [n for n in box.walk() if n.tag == "summary"]
        self.assertTrue(summary and summary[0].text() == "How this was computed")
        section = next(a for a in box.ancestors() if a.tag == "section")
        self.assertTrue(any(n.attrs.get("data-derived") == "sql-cell" for n in section.walk()), "the tutorial is not beside its table")

        def of(kind: str, raw: bool = False) -> list[str]:
            nodes = [n for n in box.walk() if n.attrs.get("data-derived") == kind]
            return ["".join(text for text, _ in n.texts()) if raw else n.text() for n in nodes]

        self.assertEqual(of("sql-question"), [norm(t["header"]["question"])])
        self.assertEqual(of("sql-reading"), [norm(t["header"]["reading"])])
        self.assertEqual(of("sql-step-title"), [norm(s["title"]) for s in t["steps"]])
        self.assertEqual(of("sql-step-text"), [norm(s["explanation"]) for s in t["steps"]])
        self.assertEqual(of("sql-step-code", raw=True), [s["code"] for s in t["steps"]], "the code shown is not the query file's, character for character")
        self.assertEqual(of("sql-file"), [f"sql/{SQL_QUERY}.sql", f"sql/results/{SQL_QUERY}.json"])
        self.assertEqual(of("sql-digest"), [result["input_digest"]])

    # PG-3
    def test_pg3_marks_target_canonical_records_and_open_their_panel(self) -> None:
        self.assertTrue(self.marks)
        for mark in self.marks:
            target = mark.attrs.get("data-target", "")
            with self.subTest(mark=target):
                self.assertIn(target, self.homes.canonical, "a mark with no canonical record behind it")
                self.assertNotIn(target, self.homes.staging)
                kind = mark.attrs["data-mark"]
                record = self.homes.canonical[target]
                if kind == "node":
                    self.assertIn("type", record)
                elif kind in ("edge", "supplier-gap"):
                    self.assertIn("relation_type", record)
                elif kind == "gap":
                    self.assertIn("claim_type", record)
                else:
                    self.fail(f"unknown mark kind {kind}")
                self.assertEqual(mark.attrs.get("href"), f"#ev-{target}")
                self.assertIn(f"ev-{target}", self.by_id, "the mark's panel does not exist")
                self.assertTrue(mark.text(), "a mark with no visible label")

    def test_pg3_no_staging_record_and_every_id_canonical(self) -> None:
        for node in self.refs():
            ref = node.attrs["data-ref"]
            if ref.startswith(("schema:", "doc:")):
                continue
            with self.subTest(ref=ref):
                self.assertIn(ref, self.homes.canonical)
                self.assertNotIn(ref, self.homes.staging)
        for staged in self.homes.staging:
            self.assertNotIn(staged, self.raw, f"a staging ID on the page: {staged}")

    # PG-4
    def test_pg4_inference_is_labelled_and_reasoned(self) -> None:
        labels = build_module().LABELS
        self.assertTrue({"inferred", "stated"} <= set(labels))
        edge_marks = [m for m in self.marks if m.attrs["data-mark"] in ("edge", "gap")]
        self.assertTrue(edge_marks)
        for mark in edge_marks:
            target = mark.attrs["data-target"]
            record = self.homes.canonical[target]
            claims = [self.homes.canonical[c] for c in record.get("claim_ids", [target])]
            inferred = not any(c["claim_type"] == "FACT" for c in claims)
            words = {n.text() for n in mark.walk() if "data-label" in n.attrs}
            with self.subTest(mark=target):
                self.assertEqual(mark.attrs.get("data-basis"), "inferred" if inferred else "stated")
                self.assertEqual("inferred" in mark.attrs.get("class", "").split(), inferred)
                self.assertIn("inferred" if inferred else "stated", words)
                self.assertNotIn("stated" if inferred else "inferred", words)
                panel = self.by_id[f"ev-{target}"]
                reasons = {n.attrs["data-ref"] for n in panel.walk() if n.attrs.get("data-field") == "/reasoning"}
                for claim in claims:
                    if claim["claim_type"] == "DERIVATION":
                        self.assertIn(claim["id"], reasons, "an inference without its reasoning in the panel")

    # PG-5
    def test_pg5_the_chain_and_its_gaps_are_drawn(self) -> None:
        journey = build_module().JOURNEY
        drawn = {(m.attrs["data-mark"], m.attrs["data-target"]) for m in self.marks}

        def chain(items):
            for item in items:
                yield item
                yield from chain(item["dependents"])

        edges = list(chain(self.atlas.depends_on_tree(journey["walk_root"])))
        self.assertTrue(edges, "the walk is empty")
        for item in edges:
            edge = item["edge"]
            with self.subTest(edge=edge["id"]):
                self.assertIn(("edge", edge["id"]), drawn)
                for node in (edge["source_entity"], edge["target_entity"]):
                    self.assertIn(("node", node), drawn)
                    for actor in self.atlas.actors_list(node):
                        self.assertIn(("edge", actor["edge"]["id"]), drawn)
                supplier = edge.get("supplier")
                if supplier is not None:
                    self.assertIsInstance(supplier, dict, "named suppliers need a design before they are drawn")
                    self.assertIn(("supplier-gap", edge["id"]), drawn)
                    gap = next(m for m in self.marks if m.attrs["data-mark"] == "supplier-gap" and m.attrs["data-target"] == edge["id"])
                    states = [n for n in gap.walk() if n.attrs.get("data-field") == "/supplier/state"]
                    self.assertEqual(len(states), 1, "an unknown supplier drawn without its state")
        for gap in journey["drawn_gaps"]:
            with self.subTest(gap=gap["candidate"]):
                marks = [m for m in self.marks if m.attrs["data-mark"] == "gap" and m.attrs["data-target"] == gap["claim"]]
                self.assertEqual(len(marks), 1, "a recorded gap is not drawn")
                lines = [n for n in marks[0].walk() if "line" in n.attrs.get("class", "").split()]
                self.assertTrue(lines)
                self.assertTrue(all("marker-end" not in n.attrs for n in lines), "a gap drawn as an edge")
                words = {n.text() for n in marks[0].walk() if "data-label" in n.attrs}
                self.assertIn("gap: no edge", words)
        for text, _ in self.visible_texts():
            self.assertNotRegex(text.lower(), r"\bnone\b", "RR-7: never 'none'")
        for mark in self.marks:
            if mark.attrs["data-mark"] in ("gap", "supplier-gap"):
                self.assertNotRegex(mark.text(), r"(?<![\w.])0(?![\w.])", "a gap drawn as zero")

    def test_pg5_candidates_are_cards_never_lines(self) -> None:
        # D-109: a refused candidate is never drawn in the diagram; each one the journey names is a
        # card in the gaps section, under a heading for each of its reasons.
        figures = [n for n in self.nodes if "data-figure" in n.attrs]
        self.assertEqual(len(figures), 1)
        for node in figures[0].walk():
            self.assertFalse(node.attrs.get("data-ref", "").startswith("cand-"), "a refused candidate drawn in the diagram")
        journey = build_module().JOURNEY
        cards = [n for n in self.nodes if "data-candidate" in n.attrs]
        for cand_id in journey["candidates"]:
            with self.subTest(candidate=cand_id):
                record = self.homes.canonical[cand_id]
                mine = [c for c in cards if c.attrs["data-candidate"] == cand_id]
                groups = sorted(next(a for a in c.ancestors() if "data-reason" in a.attrs).attrs["data-reason"] for c in mine)
                self.assertEqual(groups, sorted(record["reasons"]), "a card missing from a reason group, or in a wrong one")
                for card in mine:
                    fields = {n.attrs.get("data-field") for n in card.walk() if n.attrs.get("data-ref") == cand_id}
                    self.assertIn("/reasoning", fields)
                    self.assertTrue(any(f.startswith("/relation_types/") for f in fields if f))
        for group in (n for n in self.nodes if "data-reason" in n.attrs):
            heads = [n for n in group.walk() if n.attrs.get("data-ref") == f"schema:refused_candidates#vocab_reason/{group.attrs['data-reason']}" and n.attrs.get("data-field") == "/description"]
            self.assertEqual(len(heads), 1, "a reason group without its definition")
        self.assertEqual({c.attrs["data-candidate"] for c in cards}, set(journey["candidates"]))

    def test_pg5_the_lane_is_not_linked(self) -> None:
        journey = build_module().JOURNEY
        lanes = [n for n in self.nodes if "data-lane" in n.attrs]
        self.assertEqual(len(lanes), 1)
        lane = {m.attrs["data-target"] for m in lanes[0].walk() if m.tag == "a" and "data-mark" in m.attrs}
        for edge_id in journey["lane_edges"]:
            self.assertIn(edge_id, lane)
        products = {e["edge"]["source_entity"] for e in self.atlas.depends_on_tree(journey["walk_root"])[0]["dependents"]}
        lane_records = {t for t in lane if t in self.homes.canonical and "type" in self.homes.canonical[t]}
        for edge, _ in self.atlas.edges:
            ends = {edge["source_entity"], edge["target_entity"]}
            with self.subTest(edge=edge["id"]):
                self.assertFalse(ends & lane_records and ends & products, "a lane record is linked to an accelerator")
                supplier = edge.get("supplier")
                if isinstance(supplier, list):
                    self.assertFalse({a["value"] for a in supplier} & lane_records)
        self.assertTrue(any(n.attrs.get("data-derived") == "lane-unlinked" for n in lanes[0].walk()))
        for node in self.nodes:
            if "data-mark" in node.attrs and node.attrs["data-target"] in lane:
                self.assertTrue(any("data-lane" in a.attrs for a in node.ancestors()), "a lane mark outside the lane")

    # PG-6
    def test_pg6_framing_is_marked_and_names_no_record(self) -> None:
        framing = [n for n in self.nodes if "data-framing" in n.attrs]
        self.assertTrue(framing)
        for block in framing:
            marks = [n for n in block.walk() if "data-label" in n.attrs and n.text() == FRAMING_MARK]
            with self.subTest(block=block.text()[:60]):
                self.assertEqual(len(marks), 1, "a framing block without its visible mark")
                self.assertFalse(any("data-ref" in a.attrs for a in block.ancestors() if a is not block))
                own = " ".join(t for t, parent in block.texts() if parent.annotated() is block)
                self.assertNotRegex(own, r"\d", "framing holds a digit")
                for name in self.homes.names:
                    self.assertNotRegex(own, rf"(?<![\w-]){re.escape(name)}(?![\w-])", f"framing names a record ({name})")

    # PG-7
    def test_pg7_rebuild_is_byte_identical(self) -> None:
        build = build_module()
        first, second = build.build(), build.build()
        self.assertEqual(first, second, "two builds differ")
        self.assertEqual(first, PAGE.read_bytes(), "the committed page is not the build of the current inputs (python tools/build_page.py)")

    # PG-8
    def test_pg8_document_structure(self) -> None:
        html = next(n for n in self.nodes if n.tag == "html")
        self.assertEqual(html.attrs.get("lang"), "en")
        titles = [n for n in self.nodes if n.tag == "title" and n.parent.tag == "head"]
        h1 = [n for n in self.nodes if n.tag == "h1"]
        self.assertEqual(len(titles), 1)
        self.assertEqual(len(h1), 1)
        self.assertEqual(titles[0].text(), h1[0].text())
        self.assertTrue(any(n.tag == "meta" and n.attrs.get("name") == "viewport" for n in self.nodes))
        levels = [int(n.tag[1]) for n in self.nodes if re.fullmatch(r"h[1-6]", n.tag)]
        for before, after in zip(levels, levels[1:]):
            self.assertLessEqual(after, before + 1, "a skipped heading level")
        skip = [n for n in self.nodes if n.tag == "a" and n.attrs.get("href") == "#evidence"]
        self.assertTrue(skip, "no skip link to the evidence")

    def test_pg8_the_diagram_has_a_text_equivalent_and_keyboard_marks(self) -> None:
        svgs = [n for n in self.nodes if n.tag == "svg" and "data-figure" in n.attrs]
        self.assertEqual(len(svgs), 1)
        svg = svgs[0]
        children = [c.tag for c in svg.children if isinstance(c, Node)]
        self.assertIn("title", children)
        self.assertIn("desc", children)
        described = svg.attrs.get("aria-describedby", "")
        self.assertIn(described, self.by_id, "the diagram's text equivalent is missing")
        words = self.by_id[described]
        for mark in self.marks:
            target = mark.attrs["data-target"]
            with self.subTest(mark=target):
                self.assertNotEqual(mark.attrs.get("tabindex"), "-1", "a mark unreachable by keyboard")
                self.assertTrue(mark.attrs.get("href"))
                for label_id in mark.attrs.get("aria-labelledby", "").split():
                    self.assertIn(label_id, self.by_id)
                self.assertTrue(mark.attrs.get("aria-labelledby"), "a mark with no accessible name")
                if mark.attrs["data-mark"] in ("edge", "gap", "supplier-gap"):
                    self.assertTrue(any(n.tag == "a" and n.attrs.get("href") == f"#ev-{target}" for n in words.walk()), "a line with no item in the text equivalent")
        for panel in (n for n in self.nodes if n.attrs.get("id", "").startswith("ev-")):
            self.assertFalse(any(a.tag == "details" for a in panel.ancestors() if a is not panel), "a panel hidden in a closed disclosure")

    def test_pg8_style_palette_and_contrast(self) -> None:
        css = "".join("".join(t for t, _ in n.texts()) for n in self.nodes if n.tag == "style")
        root = re.search(r":root\s*\{([^}]*)\}", css)
        self.assertIsNotNone(root, "no palette")
        palette = dict(re.findall(r"--([a-z-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;", root.group(1)))
        inks = {k: v for k, v in palette.items() if k.startswith("ink")}
        surfaces = {k: v for k, v in palette.items() if k.startswith("surface")}
        lines = {k: v for k, v in palette.items() if k.startswith("line")}
        self.assertTrue(inks and surfaces and lines)
        self.assertEqual(set(palette), set(inks) | set(surfaces) | set(lines), "a palette token outside ink, surface, line")
        for ink, colour in inks.items():
            for surface, ground in surfaces.items():
                with self.subTest(text=ink, surface=surface):
                    self.assertGreaterEqual(contrast(colour, ground), 4.5)
        for line, colour in lines.items():
            for surface, ground in surfaces.items():
                with self.subTest(mark=line, surface=surface):
                    self.assertGreaterEqual(contrast(colour, ground), 3.0)
        body = css[root.end() :]
        self.assertNotRegex(body, r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", "a colour outside the palette")
        for prop, value in re.findall(r"(?<![-\w])(color|background|background-color|fill|stroke|border-color|outline-color)\s*:\s*([^;}]+)", body):
            with self.subTest(prop=prop, value=value):
                tokens = re.findall(r"var\(--([a-z-]+)\)", value)
                if prop == "color":
                    self.assertTrue(tokens and all(t.startswith("ink") for t in tokens))
                elif prop in ("background", "background-color"):
                    self.assertTrue(tokens and all(t.startswith("surface") for t in tokens))
                else:
                    self.assertTrue(value.strip() in ("none", "transparent", "currentColor") or (tokens and all(t in palette for t in tokens)))
        for rule in re.findall(r"([^{}]+)\{", body):
            if ":hover" in rule:
                self.assertIn(":focus-visible", rule, f"a hover rule without focus: {rule.strip()}")

    # PG-9
    def test_pg9_links_resolve_and_nothing_loads(self) -> None:
        for node in self.nodes:
            self.assertNotIn(node.tag, ("script", "iframe", "object", "embed", "img", "link"), f"<{node.tag}> on a self-contained page")
            self.assertNotIn("src", node.attrs)
            for attr in ("onclick", "onmouseover", "onload", "onfocus"):
                self.assertNotIn(attr, node.attrs)
            href = node.attrs.get("href")
            if href is None:
                continue
            with self.subTest(href=href):
                if href.startswith("#"):
                    self.assertIn(href[1:], self.by_id, "a fragment with no target")
                elif re.match(r"https?://", href):
                    self.assertEqual(node.tag, "a", "a remote resource")
                else:
                    self.assertTrue((PAGE.parent / href).resolve().exists(), "a link to a file that does not exist")
        css = "".join("".join(t for t, _ in n.texts()) for n in self.nodes if n.tag == "style")
        self.assertNotRegex(css, r"@import|url\(", "the style loads a resource")
        for node in self.nodes:
            for attr in ("marker-end", "marker-start", "fill", "filter"):
                value = node.attrs.get(attr, "")
                for target in re.findall(r"url\(#([^)]+)\)", value):
                    self.assertIn(target, self.by_id)

    # PG-10
    def test_pg10_the_journey_specification_has_homes(self) -> None:
        journey = build_module().JOURNEY
        self.assertIn(journey["walk_root"], self.homes.canonical)
        for edge_id in journey["lane_edges"]:
            self.assertIn(edge_id, self.homes.canonical)
        for cand_id in journey["candidates"]:
            self.assertIn(cand_id, self.homes.canonical, "a journey candidate is not canonical")
            self.assertNotIn(cand_id, self.homes.staging)
        for gap in journey["drawn_gaps"]:
            with self.subTest(gap=gap["candidate"]):
                cand = self.homes.canonical[gap["candidate"]]
                self.assertIn(gap["claim"], [c.get("claim_id") for c in cand["considered"]], "the drawn gap's claim is not the candidate's")
                self.assertIn(gap["claim"], self.homes.canonical)
                self.assertIn(cand["ruling"], self.homes.decisions)
                mark = next(m for m in self.marks if m.attrs["data-mark"] == "gap" and m.attrs["data-target"] == gap["claim"])
                self.assertEqual([cand["source_entities"][0], cand["target_entities"][0]], [mark.attrs.get("data-from"), mark.attrs.get("data-to")])
        # every rule code quoted in a candidate's reasoning is listed with its home (D-108)
        quoted = " ".join(n.text() for n in self.refs() if n.attrs["data-ref"].startswith("cand-") and n.attrs.get("data-field") == "/reasoning")
        listed = {n.attrs["data-ref"].split("#")[1] for n in self.refs() if n.attrs["data-ref"].startswith(("doc:rules#", "doc:decisions#"))}
        for code in set(re.findall(r"\b(?:ER|RR|F)-\d+\b|\bD-\d{3}\b", quoted)):
            self.assertIn(code, listed, f"rule {code} is quoted with no definition on the page")
        for decision in journey["decisions"]:
            self.assertIn(decision, self.homes.decisions)
            self.assertTrue(any(n.attrs.get("data-ref") == f"doc:decisions#{decision}" for n in self.nodes), f"{decision} not shown")


class BuildRefusalTests(unittest.TestCase):
    """The build refuses to draw what the records do not support (vertical-slice.md §2)."""

    def build_with(self, change) -> None:
        import shutil
        import tempfile

        build = build_module()
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            shutil.copytree(DATA, data)
            change(data)
            with self.assertRaises(build.BuildError) as raised:
                build.build(data)
        return str(raised.exception)

    @staticmethod
    def rewrite(path: Path, change) -> None:
        records = load(path)
        change(records)
        path.write_text(json.dumps(records), encoding="utf-8")

    def test_a_lane_record_linked_to_an_accelerator(self) -> None:
        edge = {
            "id": "rel-product-nvidia-h100-tensor-core-gpu-incorporates-product-micron-technology-hbm4-36gb-12h",
            "relation_type": "incorporates",
            "source_entity": "product-nvidia-h100-tensor-core-gpu",
            "target_entity": "product-micron-technology-hbm4-36gb-12h",
            "claim_ids": ["claim-h100-hbm-stacks"],
            "supplier": {"state": "not_applicable"},
        }
        message = self.build_with(lambda data: self.rewrite(data / "relationships.json", lambda r: r.append(edge)))
        self.assertIn("links the lane to the chain", message)

    def test_a_chain_claim_in_staging(self) -> None:
        def stage(data: Path) -> None:
            claims = load(data / "claims.json")
            moved = [c for c in claims if c["id"] == "claim-hbm-requires-3d-die-stacking"]
            self.rewrite(data / "claims.json", lambda r: r.remove(moved[0]))
            self.rewrite(data / "staging" / "claims.json", lambda r: r.extend(moved))

        message = self.build_with(stage)
        self.assertIn("not canonical", message)

    def test_a_journey_candidate_in_staging(self) -> None:
        # D-109: the page shows canonical candidates only.
        def stage(data: Path) -> None:
            cands = load(data / "refused_candidates.json")
            moved = [c for c in cands if c["id"] == build_module().JOURNEY["candidates"][0]]
            self.rewrite(data / "refused_candidates.json", lambda r: r.remove(moved[0]))
            self.rewrite(data / "staging" / "refused_candidates.json", lambda r: r.extend(moved))

        message = self.build_with(stage)
        self.assertIn("not canonical", message)


if __name__ == "__main__":
    unittest.main()
