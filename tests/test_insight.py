"""Checks for the S14.5 visual prototype: validate-design for site/hbm-insight/index.html.

S14.5 (docs/architecture/visual-architecture.md §10, §12; D-124, D-125). Standard library only. The
prototype renders the committed S14 SQL result (sql/results/accelerator_dependencies.json) in the seven
layers QUESTION → INSIGHT → VISUAL → EXPLORE → EVIDENCE → DATA → METHOD. The checks read the committed
page, the result file and the data with their own loaders (the S11 page checks' DOM and homes), never
the build's, and recompute every value the page shows:

IN-1  every text node sits inside a record value, a fixed label, a derived value or a framing block; no
      label holds a digit or names a record;
IN-2  every record value equals its home; every SQL cell equals its cell in the committed result;
IN-3  every derived value (tallies with their denominators, ranges, the headline's condition, the
      comparison, the input digest) is recomputed from the result and the files;
IN-4  the visual encodes its rows: one strip mark and one unit square per result row, each carrying the
      row's basis in its class and in words, a gap's reason in words; each strip holds exactly its
      accelerator's rows; "none" never appears;
IN-5  every evidence link opens an existing panel of the HBM page, every distinct record has an entry in
      the evidence index, and every fragment resolves;
IN-6  framing is visibly marked, holds no digit and names no record;
IN-7  accessibility basics: lang, title equal to the h1, one h1, no skipped heading level, the filter is
      a labelled radio group, the palette and its contrast, hover rules shared with focus;
IN-8  the committed page equals a rebuild, and two builds are identical;
IN-9  the page loads nothing, runs no script, is marked as a prototype, and the build refuses rows its
      visual specification does not fit.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_page as tp  # noqa: E402  (the S11 checks' DOM, homes and contrast; no test class is imported)

PAGE = REPO_ROOT / "site" / "hbm-insight" / "index.html"
CHAIN_PAGE = REPO_ROOT / "site" / "hbm-chain" / "index.html"
RESULT = REPO_ROOT / "sql" / "results" / "accelerator_dependencies.json"
SQL_QUERY = "accelerator_dependencies"
INPUT_GLOBS = ("data/*.json", "data/staging/*.json", "schemas/*.json", "sql/*.sql", "sql/results/*.json")
INPUT_FILES = (
    "docs/architecture/company-dataset.md",
    "docs/architecture/decisions.md",
    "docs/architecture/relationship-taxonomy.md",
    "docs/research/source-policy.md",
    "site/hbm-chain/index.html",
    "tools/build_insight.py",
    "tools/build_page.py",
    "tools/insight_template.html",
    "tools/navigate.py",
    "tools/page_template.html",
    "tools/trace.py",
)
# The visual specification's slots (visual-architecture.md §10, §12): position in the result → slot.
SLOTS = {1: "actor", 2: "part", 3: "supplier", 4: "process"}
DERIVED_KINDS = {
    "sql-cell", "sql-flag", "sql-question", "sql-reading", "sql-step-title", "sql-step-text", "sql-step-code", "sql-file", "sql-digest",
    "input-file", "input-digest", "acc-count", "row-count", "record-count", "supplier-gap-count", "stated-count", "acc-rows",
    "date-first", "date-last", "undated-count", "pub-min", "pub-max", "one-pub-count", "sourced-count", "shown-in",
}


def result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


def input_digest(paths: list[str]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.encode("utf-8") + b"\0" + hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest().encode("ascii") + b"\n")
    return digest.hexdigest()


def evidence_target(row: dict, panels: set[str]) -> str:
    """The HBM page's panel for a row: the edge's own panel, or for a recorded gap the first claim it
    considered that has a panel there."""
    if not row["record_id"].startswith("cand-"):
        return f"ev-{row['record_id']}"
    return next(f"ev-{c}" for c in row["claim_ids"] if f"ev-{c}" in panels)


def build_module():
    import build_insight  # noqa: PLC0415 (imported late: the checks are written before the build)

    return build_insight


class InsightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
        cls.root = tp.parse(cls.raw) if cls.raw else tp.Node("#root", {}, None)
        cls.homes = tp.Homes()
        cls.nodes = list(cls.root.walk())
        cls.by_id = {n.attrs["id"]: n for n in cls.nodes if "id" in n.attrs}
        body = [n for n in cls.nodes if n.tag == "body"]
        cls.body = body[0] if body else tp.Node("body", {}, None)
        cls.result = result()
        cls.rows = cls.result["rows"]
        chain = tp.parse(CHAIN_PAGE.read_text(encoding="utf-8"))
        cls.chain_ids = {n.attrs["id"] for n in chain.walk() if "id" in n.attrs}

    def setUp(self) -> None:
        if not self.raw:
            self.fail(f"the page is not built: {PAGE.relative_to(REPO_ROOT)} (python tools/build_insight.py)")

    def derived(self, kind: str, **attrs) -> list:
        return [n for n in self.nodes if n.attrs.get("data-derived") == kind and all(n.attrs.get(f"data-{k}") == v for k, v in attrs.items())]

    def accelerators(self) -> list[str]:
        seen: list[str] = []
        for r in self.rows:
            if r["accelerator_id"] not in seen:
                seen.append(r["accelerator_id"])
        return seen

    # IN-1
    def test_in1_every_text_node_has_a_home(self) -> None:
        labels = set(build_module().LABELS)
        for text, parent in self.body.texts():
            if parent.tag in ("style", "script") or tp.BARE.match(text):
                continue
            owner = parent.annotated()
            with self.subTest(text=tp.norm(text)[:80]):
                self.assertIsNotNone(owner, "text with no record, label, derived value or framing behind it")
                if "data-label" in owner.attrs:
                    self.assertIn(owner.text(), labels, "a label that is not one of the build's labels")
        for node in self.nodes:
            if any(a in node.attrs for a in ("data-ref", "data-label", "data-derived")):
                inner = [n for n in node.walk() if n is not node and any(a in n.attrs for a in tp.ANNOTATIONS)]
                self.assertEqual(inner, [], "an annotated value must not contain another")

    def test_in1_labels_carry_no_fact(self) -> None:
        for label in build_module().LABELS:
            with self.subTest(label=label):
                self.assertNotRegex(label, r"\d", "a label holds a digit")
                self.assertNotRegex(label.lower(), r"\bnone\b")
                for name in self.homes.names:
                    self.assertNotRegex(label, rf"(?<![\w-]){re.escape(name)}(?![\w-])", f"a label names a record ({name})")

    # IN-2
    def test_in2_record_values_equal_their_homes(self) -> None:
        values = [n for n in self.nodes if "data-ref" in n.attrs]
        self.assertTrue(values)
        for node in values:
            ref, field = node.attrs["data-ref"], node.attrs.get("data-field")
            with self.subTest(ref=ref, field=field):
                self.assertTrue(self.homes.has(ref, field), "no such home")
                expected = tp.norm(tp.FORMATS[node.attrs.get("data-format")](str(self.homes.resolve(ref, field))))
                self.assertEqual(node.text(), expected)

    def test_in2_sql_cells_equal_the_result(self) -> None:
        cells = self.derived("sql-cell")
        self.assertTrue(cells)
        for node in cells:
            index, column = int(node.attrs["data-row"]), node.attrs["data-column"]
            self.assertEqual(node.attrs.get("data-query"), SQL_QUERY)
            value = self.rows[index][column]
            if "data-item" in node.attrs:
                value = value[int(node.attrs["data-item"])]
            text = str(value).replace("_", " ") if node.attrs.get("data-format") == "state" else str(value)
            with self.subTest(row=index, column=column):
                self.assertEqual(node.text(), tp.norm(text))

    # IN-3
    def test_in3_derived_values_are_recomputed(self) -> None:
        kinds = {n.attrs["data-derived"] for n in self.nodes if "data-derived" in n.attrs}
        self.assertLessEqual(kinds, DERIVED_KINDS, "a derived value the checks do not recompute")
        rows = self.rows
        sourced = [r for r in rows if r["publishers"]]
        dates = sorted({d for r in rows for d in (r["evidence_dated_from"], r["evidence_dated_to"]) if d != "not_applicable"})
        pubs = sorted(len(r["publishers"]) for r in sourced)
        supplier = [r for r in rows if r["position"] == 3]
        expected = {
            "acc-count": str(len(self.accelerators())),
            "row-count": str(len(rows)),
            "record-count": str(len({r["record_id"] for r in rows})),
            "supplier-gap-count": str(len({r["accelerator_id"] for r in supplier if r["basis"] == "gap"})),
            "date-first": dates[0],
            "date-last": dates[-1],
            "undated-count": str(sum(r["evidence_dated_from"] == "not_applicable" for r in rows)),
            "pub-min": str(pubs[0]),
            "pub-max": str(pubs[-1]),
            "one-pub-count": str(sum(len(r["publishers"]) == 1 for r in sourced)),
            "sourced-count": str(len(sourced)),
        }
        for kind, want in expected.items():
            for node in self.derived(kind):
                with self.subTest(kind=kind):
                    self.assertEqual(node.text(), want)
        for kind in ("acc-count", "supplier-gap-count", "date-first", "date-last", "pub-min", "sourced-count"):
            self.assertTrue(self.derived(kind), f"{kind} is not shown")
        for acc in self.accelerators():
            mine = [r for r in rows if r["accelerator_id"] == acc]
            with self.subTest(accelerator=acc):
                self.assertEqual([n.text() for n in self.derived("stated-count", accelerator=acc)], [str(sum(r["basis"] == "stated" for r in mine))])
                self.assertEqual([n.text() for n in self.derived("acc-rows", accelerator=acc)], [str(len(mine))], "a tally without its denominator")
        for record in {r["record_id"] for r in rows}:
            with self.subTest(record=record):
                self.assertEqual([n.text() for n in self.derived("shown-in", record=record)], [str(sum(r["record_id"] == record for r in rows))])
        files = [n.text() for n in self.derived("input-file")]
        self.assertEqual(sorted(files), input_paths())
        self.assertEqual([n.text() for n in self.derived("input-digest")], [input_digest(input_paths())])

    def test_in3_every_tally_has_its_denominator_in_its_block(self) -> None:
        pairs = {"stated-count": "acc-rows", "supplier-gap-count": "acc-count", "one-pub-count": "sourced-count", "undated-count": "row-count"}
        for numerator, denominator in pairs.items():
            for node in self.derived(numerator):
                block = next((a for a in node.ancestors() if "indicator" in a.attrs.get("class", "").split() or a.tag == "li"), None)
                with self.subTest(tally=numerator):
                    self.assertIsNotNone(block, "a tally outside an indicator block or list item")
                    self.assertTrue(any(n.attrs.get("data-derived") == denominator for n in block.walk()), "a tally whose denominator is not in the same block")

    def test_in3_the_headline_and_the_comparison(self) -> None:
        h1 = [n for n in self.nodes if n.tag == "h1"][0]
        parts = [r for r in self.rows if r["position"] == 2]
        suppliers = [r for r in self.rows if r["position"] == 3]
        uniform = (
            len({(r["relation"], r["to_id"], r["basis"]) for r in parts}) == 1
            and len({r["gap_reason"] for r in suppliers}) == 1
            and {r["accelerator_id"] for r in parts} == {r["accelerator_id"] for r in suppliers} == set(self.accelerators())
        )
        if uniform:
            cells = [(int(n.attrs["data-row"]), n.attrs["data-column"]) for n in h1.walk() if n.attrs.get("data-derived") == "sql-cell"]
            self.assertEqual({self.rows[i]["accelerator_id"] for i, c in cells if c == "accelerator"}, set(self.accelerators()), "the headline names every accelerator")
            self.assertTrue(any(c == "gap_reason" for _, c in cells), "the headline states who makes the part")
        else:
            self.assertIn("question", h1.attrs.get("class", ""), "the rows do not support one sentence: the question is the headline")

        def key(r: dict) -> tuple:
            other = r["from_id"] if r["to_id"] == r["accelerator_id"] else r["to_id"] if r["from_id"] == r["accelerator_id"] else (r["from_id"], r["to_id"])
            return (r["relation"], r["basis"], r["gap_reason"], other)

        common, differ = set(), set()
        for position in sorted({r["position"] for r in self.rows}):
            keys = {acc: [key(r) for r in self.rows if r["accelerator_id"] == acc and r["position"] == position] for acc in self.accelerators()}
            (common if len({tuple(v) for v in keys.values()}) == 1 and all(keys.values()) else differ).add(str(position))
        shown = {name: {n.attrs["data-position"] for n in self.nodes if n.attrs.get("data-compare") == name} for name in ("common", "differ")}
        self.assertEqual(shown, {"common": common, "differ": differ})

    # IN-4
    def test_in4_the_visual_encodes_its_rows(self) -> None:
        for kind in ("strip", "unit"):
            marks = [n for n in self.nodes if n.attrs.get("data-mark") == kind]
            self.assertEqual(sorted(int(n.attrs["data-row"]) for n in marks), list(range(len(self.rows))), f"one {kind} mark per result row")
            for mark in marks:
                i = int(mark.attrs["data-row"])
                row = self.rows[i]
                with self.subTest(kind=kind, row=i):
                    self.assertEqual(mark.attrs.get("data-basis"), row["basis"])
                    self.assertIn(row["basis"], mark.attrs.get("class", "").split(), "the line style does not follow the basis")
                    columns = {(int(n.attrs["data-row"]), n.attrs["data-column"]) for n in mark.walk() if n.attrs.get("data-derived") == "sql-cell"}
                    self.assertIn((i, "basis"), columns, "the basis is not said in words on the mark")
                    if row["basis"] == "gap" and kind == "strip":
                        self.assertIn((i, "gap_reason"), columns, "a gap without its reason in words")
        strips = [n for n in self.nodes if "data-strip" in n.attrs]
        self.assertEqual([s.attrs["data-strip"] for s in strips], self.accelerators())
        for strip in strips:
            inside = {int(n.attrs["data-row"]) for n in strip.walk() if n.attrs.get("data-mark") == "strip"}
            with self.subTest(strip=strip.attrs["data-strip"]):
                self.assertEqual(inside, {i for i, r in enumerate(self.rows) if r["accelerator_id"] == strip.attrs["data-strip"]})
                for slot in SLOTS.values():
                    filled = [n for n in strip.walk() if n.attrs.get("data-slot") == slot]
                    self.assertEqual(len(filled), 1, f"slot {slot}: one mark or one 'no recorded relationship' cell")
        rows = [n for n in self.nodes if n.tag == "tr" and n.attrs.get("id", "").startswith("row-")]
        self.assertEqual([(n.attrs["id"], n.attrs.get("data-basis")) for n in rows], [(f"row-{i}", r["basis"]) for i, r in enumerate(self.rows)])
        text = self.body.text().lower()
        self.assertNotRegex(text, r"\bnone\b", "an unknown written as 'none'")

    # IN-5
    def test_in5_evidence_links_open_existing_panels(self) -> None:
        prefix = "../hbm-chain/index.html#"
        for mark in (n for n in self.nodes if n.attrs.get("data-mark") == "strip"):
            row = self.rows[int(mark.attrs["data-row"])]
            with self.subTest(row=mark.attrs["data-row"]):
                self.assertEqual(mark.tag, "a")
                self.assertEqual(mark.attrs.get("href"), prefix + evidence_target(row, self.chain_ids))
        index = [n for n in self.nodes if "data-evidence-record" in n.attrs]
        self.assertEqual(sorted(n.attrs["data-evidence-record"] for n in index), sorted({r["record_id"] for r in self.rows}), "one evidence entry per distinct record")
        for node in self.nodes:
            href = node.attrs.get("href")
            if href is None:
                continue
            with self.subTest(href=href):
                if href.startswith("#"):
                    self.assertIn(href[1:], self.by_id, "a fragment with no target")
                elif href.startswith(prefix):
                    self.assertIn(href[len(prefix) :], self.chain_ids, "an evidence link to a panel the HBM page does not have")
                elif not re.match(r"https?://", href):
                    self.assertTrue((PAGE.parent / href.split("#")[0]).resolve().exists(), "a link to a file that does not exist")
        for unit in (n for n in self.nodes if n.attrs.get("data-mark") == "unit"):
            self.assertEqual(unit.attrs.get("href"), f"#row-{unit.attrs['data-row']}", "a unit square that does not open its row")

    # IN-6
    def test_in6_framing_is_marked_and_names_no_record(self) -> None:
        framing = [n for n in self.nodes if "data-framing" in n.attrs]
        self.assertTrue(framing)
        for block in framing:
            marks = [n for n in block.walk() if "data-label" in n.attrs and n.text() == tp.FRAMING_MARK]
            with self.subTest(block=block.text()[:60]):
                self.assertEqual(len(marks), 1, "a framing block without its visible mark")
                own = " ".join(t for t, parent in block.texts() if parent.annotated() is block)
                self.assertNotRegex(own, r"\d", "framing holds a digit")
                for name in self.homes.names:
                    self.assertNotRegex(own, rf"(?<![\w-]){re.escape(name)}(?![\w-])", f"framing names a record ({name})")

    # IN-7
    def test_in7_document_structure_and_filter(self) -> None:
        html = next(n for n in self.nodes if n.tag == "html")
        self.assertEqual(html.attrs.get("lang"), "en")
        titles = [n for n in self.nodes if n.tag == "title"]
        h1 = [n for n in self.nodes if n.tag == "h1"]
        self.assertEqual(len(titles), 1)
        self.assertEqual(len(h1), 1)
        self.assertEqual(titles[0].text(), h1[0].text())
        levels = [int(n.tag[1]) for n in self.nodes if re.fullmatch(r"h[1-6]", n.tag)]
        for before, after in zip(levels, levels[1:]):
            self.assertLessEqual(after, before + 1, "a skipped heading level")
        radios = [n for n in self.nodes if n.tag == "input" and n.attrs.get("type") == "radio"]
        self.assertTrue(radios, "no exploration control")
        for radio in radios:
            with self.subTest(radio=radio.attrs.get("id")):
                self.assertTrue(any(a.tag == "fieldset" for a in radio.ancestors()), "a radio outside a fieldset")
                self.assertTrue(any(n.tag == "label" and n.attrs.get("for") == radio.attrs.get("id") for n in self.nodes), "a radio with no label")
        fieldset = next(a for a in radios[0].ancestors() if a.tag == "fieldset")
        self.assertTrue(any(n.tag == "legend" for n in fieldset.walk()))
        self.assertEqual(sum("checked" in r.attrs for r in radios), 1, "exactly one filter is on at load")
        self.assertEqual([r for r in radios if "checked" in r.attrs][0].attrs.get("value"), "all", "everything is shown at load")
        tutorials = [n for n in self.nodes if n.tag == "details" and "sql-tutorial" in n.attrs.get("class", "").split()]
        self.assertEqual(len(tutorials), 1)
        self.assertNotIn("open", tutorials[0].attrs)

    def test_in7_palette_and_contrast(self) -> None:
        css = "".join("".join(t for t, _ in n.texts()) for n in self.nodes if n.tag == "style")
        root = re.search(r":root\s*\{([^}]*)\}", css)
        self.assertIsNotNone(root)
        palette = dict(re.findall(r"--([a-z-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;", root.group(1)))
        import build_page  # noqa: PLC0415

        self.assertEqual(palette, build_page.PALETTE, "the prototype uses the Atlas palette, from its one home")
        inks = {k: v for k, v in palette.items() if k.startswith("ink")}
        surfaces = {k: v for k, v in palette.items() if k.startswith("surface")}
        lines = {k: v for k, v in palette.items() if k.startswith("line")}
        for ink, colour in inks.items():
            for surface, ground in surfaces.items():
                self.assertGreaterEqual(tp.contrast(colour, ground), 4.5, f"{ink} on {surface}")
        for line, colour in lines.items():
            for surface, ground in surfaces.items():
                self.assertGreaterEqual(tp.contrast(colour, ground), 3.0, f"{line} on {surface}")
        body = css[root.end() :]
        self.assertNotRegex(body, r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", "a colour outside the palette")
        self.assertNotRegex(body, r"opacity\s*:", "fading lowers contrast: emphasis is by outline, never by opacity")
        for prop, value in re.findall(r"(?<![-\w])(color|background|background-color|fill|stroke|border-color|outline-color|border-left-color|border-top-color)\s*:\s*([^;}]+)", body):
            with self.subTest(prop=prop, value=value):
                tokens = re.findall(r"var\(--([a-z-]+)\)", value)
                if prop == "color":
                    self.assertTrue(tokens and all(t.startswith("ink") for t in tokens))
                elif prop in ("background", "background-color"):
                    self.assertTrue(value.strip() in ("none", "transparent") or (tokens and all(t.startswith("surface") for t in tokens)))
                else:
                    self.assertTrue(value.strip() in ("none", "transparent", "currentColor") or (tokens and all(t in palette for t in tokens)))
        for rule in re.findall(r"([^{}]+)\{", body):
            if ":hover" in rule:
                self.assertIn(":focus-visible", rule, f"a hover rule without focus: {rule.strip()}")

    # IN-8
    def test_in8_rebuild_is_byte_identical(self) -> None:
        build = build_module()
        first, second = build.build(), build.build()
        self.assertEqual(first, second, "two builds differ")
        self.assertEqual(first, PAGE.read_bytes(), "the committed page is not the build of the current inputs (python tools/build_insight.py)")

    # IN-9
    def test_in9_nothing_loads_and_the_page_is_a_marked_prototype(self) -> None:
        for node in self.nodes:
            self.assertNotIn(node.tag, ("script", "iframe", "object", "embed", "img", "link", "canvas"))
            self.assertNotIn("src", node.attrs)
            self.assertFalse([a for a in node.attrs if a.startswith("on")], "an inline script handler")
        css = "".join("".join(t for t, _ in n.texts()) for n in self.nodes if n.tag == "style")
        self.assertNotRegex(css, r"@import|url\(")
        kicker = [n for n in self.nodes if "kicker" in n.attrs.get("class", "").split()]
        self.assertTrue(kicker and "Prototype" in kicker[0].text(), "the page is not marked as a prototype")


class InsightRefusalTests(unittest.TestCase):
    """The build refuses rows its visual specification does not fit (visual-architecture.md §10)."""

    def build_with(self, change_rows=None, drop_panel: str | None = None) -> None:
        build = build_module()
        with tempfile.TemporaryDirectory() as tmp:
            res = Path(tmp) / "result.json"
            data = result()
            if change_rows:
                change_rows(data["rows"])
            res.write_text(json.dumps(data), encoding="utf-8")
            chain = Path(tmp) / "chain.html"
            shutil.copy(CHAIN_PAGE, chain)
            if drop_panel:
                text = chain.read_text(encoding="utf-8")
                chain.write_text(text.replace(f'id="{drop_panel}"', 'id="gone"'), encoding="utf-8")
            build.Insight(result_path=res, chain_page=chain).render()

    def test_a_slot_with_two_rows(self) -> None:
        def twice(rows):
            rows.append(dict(rows[0]))

        with self.assertRaisesRegex(build_module().BuildError, "slot"):
            self.build_with(twice)

    def test_a_position_the_specification_does_not_know(self) -> None:
        def deeper(rows):
            rows[0]["position"] = 9

        with self.assertRaisesRegex(build_module().BuildError, "position"):
            self.build_with(deeper)

    def test_an_evidence_link_with_no_panel(self) -> None:
        row = result()["rows"][0]
        panels = {n.attrs["id"] for n in tp.parse(CHAIN_PAGE.read_text(encoding="utf-8")).walk() if "id" in n.attrs}
        with self.assertRaisesRegex(build_module().BuildError, "panel"):
            self.build_with(drop_panel=evidence_target(row, panels))

    def test_a_result_from_another_query_version(self) -> None:
        def stale(rows):
            pass

        build = build_module()
        with tempfile.TemporaryDirectory() as tmp:
            res = Path(tmp) / "result.json"
            data = result()
            data["query_sha256"] = "0" * 64
            res.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(build.BuildError, "another version"):
                build.Insight(result_path=res, chain_page=CHAIN_PAGE).render()


if __name__ == "__main__":
    unittest.main()
