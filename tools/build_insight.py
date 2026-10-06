"""Build the S14.5 visual prototype from the committed SQL result and the Atlas's records.

Writes site/hbm-insight/index.html (docs/architecture/visual-architecture.md §12; D-125): one
self-contained file with inline CSS, no script and no SVG, that answers the HBM page's question in the
seven layers of the Atlas research view:

    QUESTION → INSIGHT → VISUAL → EXPLORE → EVIDENCE → DATA → METHOD

Every value comes from sql/results/accelerator_dependencies.json (the S14 result, read as a file; DuckDB is
never imported, D-118) or from the canonical records. The build renders, it does not compute new facts
(visual-architecture.md §10, D-124): it copies cells, tallies the rows it draws over a denominator it
prints, takes the first and last of a column it shows, and groups rows by position to say what the
accelerators have in common and where they differ. Evidence links open the panels of the HBM page
(site/hbm-chain/index.html), which is therefore an input: build it first.

Usage:
    python tools/build_insight.py           write the page
    python tools/build_insight.py --check   rebuild in memory; exit 1 if the committed page differs

It reuses tools/build_page.py's machinery (record values, labels, derived values, the SQL table and its
tutorial) by subclassing it, and imports the Atlas palette from there (one home). The checks are
tests/test_insight.py (IN-1 to IN-9). Standard library only (D-003).
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import string
import sys
from pathlib import Path

import build_page
from build_page import DATA, PALETTE, REPO_ROOT, BuildError, esc, input_digest

TEMPLATE = REPO_ROOT / "tools" / "insight_template.html"
PAGE = REPO_ROOT / "site" / "hbm-insight" / "index.html"
RESULT = REPO_ROOT / "sql" / "results" / f"{build_page.SQL_QUERY}.json"
QUERY = REPO_ROOT / "sql" / f"{build_page.SQL_QUERY}.sql"
CHAIN_PAGE = REPO_ROOT / "site" / "hbm-chain" / "index.html"
CHAIN_HREF = "../hbm-chain/index.html"
TO_ROOT = "../../"
INPUT_GLOBS = build_page.INPUT_GLOBS
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

# The visual specification (visual-architecture.md §10): the result's positions and the slot each fills.
# Position is defined in the query file: links into the accelerator (1), the parts it incorporates (2),
# unknowns on those links (3), what those parts require (4). Any other position is refused.
SLOTS = {1: "actor", 2: "part", 3: "supplier", 4: "process"}
SLOT_TITLES = {"actor": "Acts on it", "part": "The part", "supplier": "The part’s maker", "process": "The part’s process"}
SLOT_KICKERS = {"actor": "acts on it", "part": "it incorporates", "process": "that part requires"}
# Rulings the page states as limitations (their titles are read from decisions.md).
DECISIONS = ("D-091", "D-092", "D-094", "D-120", "D-124")
BASES = ("stated", "inferred", "gap")

# Every fixed word this page adds to the S11 page's labels (PG-1, IN-1): none names a record or holds a digit.
LABELS = build_page.LABELS | frozenset(
    {
        "Research view", "Prototype", "The question", "Scope:", "accelerators recorded in the Atlas, and every link it records around each, with evidence dated",
        "each", "who makes it:", "What the records show", "In common", "Where they differ",
        "Acts on it", "The part", "The part’s maker", "The part’s process",
        "acts on it", "it incorporates", "that part requires", "accelerator", "who makes that part",
        "Indicators", "Who makes the memory", "of", "accelerators",
        "Counted from the table’s rows at the step “who makes that part”.",
        "Links on stated evidence", "links", "rows in the table show", "records: one record can appear under more than one accelerator, and an unknown supplier sits on the link it qualifies.",
        "rows have nothing to date", "Dates, not ages: an undated web page is dated by the day it was read.",
        "Publishers behind a sourced link", "sourced rows rest on one publisher", "Listed, never counted as confirmation.",
        "The chains, side by side", "Reading the chains", "Explore", "Show links whose basis is", "all links",
        "Highlights the matching links in the chains and keeps only the matching rows in the table.",
        "no recorded relationship", "table rows:", "open the evidence",
        "Each line opens its evidence on the dependency journey page, which holds every panel.",
        "the full dependency journey", "The links as a table", "Method and limitations", "What the counts count",
        "Built from", "Rulings this page depends on", "Reproduce", "rebuild the result:", "rebuild this page:",
        "python tools/build_insight.py --check",
    }
)


def load_result(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


class Insight(build_page.Page):
    def __init__(self, data: Path = DATA, result_path: Path = RESULT, chain_page: Path = CHAIN_PAGE) -> None:
        super().__init__(data)
        self.result = load_result(result_path)
        if self.result["query_sha256"] != hashlib.sha256(QUERY.read_bytes()).hexdigest():
            raise BuildError(f"{result_path.name} was computed from another version of its query (python tools/warehouse.py)")
        self.rows = self.result["rows"]
        self.panels = set(re.findall(r'\bid="([^"]+)"', chain_page.read_text(encoding="utf-8")))

    @staticmethod
    def label_text(text: str) -> str:
        if text not in LABELS:
            raise BuildError(f"not a label: {text!r}")
        return text

    # --- the result, read through the visual specification ----------------------------------------

    def cell(self, i: int, column: str, fmt: str | None = None, cls: str | None = None, tag: str = "span") -> str:
        value = self.rows[i][column]
        return self.sql_cell(i, column, value, fmt=fmt, tag=tag, cls=cls)

    def accelerators(self) -> list[str]:
        seen: list[str] = []
        for r in self.rows:
            if r["accelerator_id"] not in seen:
                seen.append(r["accelerator_id"])
        return seen

    def chains(self) -> dict[str, dict[str, int]]:
        """Each accelerator's rows by slot. Refuses rows the strip cannot draw honestly."""
        chains: dict[str, dict[str, int]] = {acc: {} for acc in self.accelerators()}
        for i, r in enumerate(self.rows):
            if r["position"] not in SLOTS:
                raise BuildError(f"row {i}: position {r['position']} is not in the visual specification")
            slot = SLOTS[r["position"]]
            if slot in chains[r["accelerator_id"]]:
                raise BuildError(f"{r['accelerator_id']}: slot {slot} holds two rows; the strip draws one")
            chains[r["accelerator_id"]][slot] = i
            if self.target(i) not in self.panels:
                raise BuildError(f"row {i}: the dependency journey page has no panel {self.target(i)}")
        for acc, slots in chains.items():
            if "part" not in slots:
                raise BuildError(f"{acc}: no part; the strip is drawn around what the accelerator incorporates")
            part = self.rows[slots["part"]]
            ok = part["from_id"] == acc
            if "actor" in slots:
                ok &= self.rows[slots["actor"]]["to_id"] == acc
            if "supplier" in slots:
                ok &= self.rows[slots["supplier"]]["to_id"] == part["to_id"]
            if "process" in slots:
                ok &= self.rows[slots["process"]]["from_id"] == part["to_id"]
            if not ok:
                raise BuildError(f"{acc}: the rows do not form the chain the strip draws")
        return chains

    def target(self, i: int) -> str:
        """The HBM page's panel for a row: the edge's own, or for a recorded gap the first claim it considered
        that has a panel there (the drawn gap's claim). Missing panels are refused in chains()."""
        r = self.rows[i]
        if not r["record_id"].startswith("cand-"):
            return f"ev-{r['record_id']}"
        return next((f"ev-{c}" for c in r["claim_ids"] if f"ev-{c}" in self.panels), f"ev-{r['claim_ids'][0]}")

    def basis_words(self, i: int) -> str:
        b = self.rows[i]["basis"]
        if b not in BASES:
            raise BuildError(f"row {i}: basis {b!r} has no encoding")
        words = self.cell(i, "basis", cls=f"basis {b}")
        if b == "gap":
            words += f" · {self.cell(i, 'gap_reason', fmt='state')}"
        return words

    def dated(self, i: int) -> str:
        r = self.rows[i]
        text = self.cell(i, "evidence_dated_from", fmt="state" if r["evidence_dated_from"] == "not_applicable" else None)
        if r["evidence_dated_to"] != r["evidence_dated_from"]:
            text += f" {self.label('to')} {self.cell(i, 'evidence_dated_to')}"
        return text

    def phrase(self, i: int) -> str:
        """A row in words, by its slot: the counterpart, the relation, the basis."""
        slot = SLOTS[self.rows[i]["position"]]
        if slot == "actor":
            return f"{self.cell(i, 'from_name')} {self.cell(i, 'relation', cls='rel')} · {self.basis_words(i)}"
        if slot == "part":
            return f"{self.cell(i, 'relation', cls='rel')} {self.cell(i, 'to_name')} · {self.basis_words(i)}"
        if slot == "supplier":
            return f"{self.cell(i, 'relation', cls='rel')}: {self.basis_words(i)}"  # the state is the gap's reason
        return f"{self.cell(i, 'from_name')} {self.cell(i, 'relation', cls='rel')} {self.cell(i, 'to_name')} · {self.basis_words(i)}"

    def kind(self, record_id: str) -> str:
        record = self.homes.get(record_id, {})
        return "class-level" if record.get("type") in ("component", "technology") else "instance-level"

    # --- layer 1 and 2: question and insight -------------------------------------------------------

    def question(self) -> str:
        return f'{self.label("What does an")} {self.name("component-ai-accelerator")}{self.label("’s memory depend on, and who is known to make it?")}'

    def headline(self, chains: dict) -> tuple[str, str]:
        """The finding, composed from cells; the question when the rows do not support one sentence (V-2)."""
        parts = [chains[a]["part"] for a in chains]
        suppliers = [chains[a].get("supplier") for a in chains]
        uniform = (
            len({(self.rows[i]["relation"], self.rows[i]["to_id"], self.rows[i]["basis"]) for i in parts}) == 1
            and None not in suppliers
            and len({self.rows[i]["gap_reason"] for i in suppliers}) == 1
        )
        if not uniform:
            return "question", self.question()
        names = [self.cell(i, "accelerator") for i in parts]
        joined = names[0] if len(names) == 1 else ", ".join(names[:-1]) + f" {self.label('and')} {names[-1]}"
        each = f" {self.label('each')}" if len(names) > 1 else ""
        first = parts[0]
        return "finding", (
            f"{joined}{each} {self.cell(first, 'relation', cls='rel')} {self.cell(first, 'to_name')} "
            f"({self.cell(first, 'basis', cls='basis ' + self.rows[first]['basis'])}); "
            f"{self.label('who makes it:')} {self.cell(suppliers[0], 'gap_reason', fmt='state', cls='basis gap')}"
        )

    def dates(self) -> tuple[str, str]:
        found = sorted({d for r in self.rows for d in (r["evidence_dated_from"], r["evidence_dated_to"]) if d != "not_applicable"})
        if not found:
            raise BuildError("no row has evidence to date")
        return found[0], found[-1]

    def scope(self) -> str:
        first, last = self.dates()
        return (
            f'<p class="scope">{self.label("Scope:", cls="k")} {self.derived("acc-count", str(len(self.accelerators())))} '
            f'{self.label("accelerators recorded in the Atlas, and every link it records around each, with evidence dated")} '
            f'{self.derived("date-first", first)} {self.label("to")} {self.derived("date-last", last)}.</p>'
        )

    def comparison(self, chains: dict) -> str:
        def key(i: int) -> tuple:
            r = self.rows[i]
            other = r["from_id"] if r["to_id"] == r["accelerator_id"] else r["to_id"] if r["from_id"] == r["accelerator_id"] else (r["from_id"], r["to_id"])
            return (r["relation"], r["basis"], r["gap_reason"], other)

        common, differ = [], []
        for position, slot in SLOTS.items():
            held = {a: chains[a].get(slot) for a in chains}
            if all(v is None for v in held.values()):
                continue
            title = self.label(SLOT_TITLES[slot], cls="k")
            if None not in held.values() and len({key(i) for i in held.values()}) == 1:
                common.append(f'<li data-compare="common" data-position="{position}">{title} {self.phrase(next(iter(held.values())))}</li>')
            else:
                items = "".join(
                    f"<li>{self.cell(chains[a]['part'], 'accelerator', cls='who')}: "
                    + (self.phrase(i) if i is not None else self.label("no recorded relationship", cls="basis norecord"))
                    + "</li>"
                    for a, i in held.items()
                )
                differ.append(f'<li data-compare="differ" data-position="{position}">{title}<ul>{items}</ul></li>')
        out = ""
        if common:
            out += f'<div>{self.label("In common", tag="h3")}<ul class="compare">{"".join(common)}</ul></div>'
        if differ:
            out += f'<div>{self.label("Where they differ", tag="h3")}<ul class="compare">{"".join(differ)}</ul></div>'
        return f'<div class="comparison">{out}</div>'

    def indicators(self, chains: dict) -> str:
        n_acc = str(len(chains))
        rows = self.rows
        # who makes the memory: one state, n of n accelerators
        suppliers = [chains[a]["supplier"] for a in chains if "supplier" in chains[a]]
        states = {rows[i]["gap_reason"] for i in suppliers}
        if len(states) == 1:
            value = self.cell(suppliers[0], "gap_reason", fmt="state", cls="basis gap")
        else:
            value = "<br>".join(f"{self.cell(i, 'accelerator')}: {self.cell(i, 'gap_reason', fmt='state', cls='basis gap')}" for i in suppliers)
        gaps = str(len({rows[i]["accelerator_id"] for i in suppliers if rows[i]["basis"] == "gap"}))
        k1 = (
            f'<div class="indicator state">{self.label("Who makes the memory", tag="h4")}<p class="value">{value}</p>'
            f'<p class="den">{self.derived("supplier-gap-count", gaps)} {self.label("of")} {self.derived("acc-count", n_acc)} {self.label("accelerators")}</p>'
            f'<p class="how">{self.label("Counted from the table’s rows at the step “who makes that part”.")}</p></div>'
        )
        # links on stated evidence: a tally per accelerator over its rows, with one unit square per row
        lines = []
        for acc, slots in chains.items():
            mine = sorted(i for i, r in enumerate(rows) if r["accelerator_id"] == acc)
            stated = str(sum(rows[i]["basis"] == "stated" for i in mine))
            units = "".join(
                f'<a class="unit {rows[i]["basis"]}" data-mark="unit" data-row="{i}" data-basis="{rows[i]["basis"]}" href="#row-{i}">'
                f'{self.cell(i, "basis", cls="vh")}</a>'
                for i in mine
            )
            lines.append(
                f'<li>{self.cell(slots["part"], "accelerator", cls="who")} '
                f'<span class="tally">{self.derived("stated-count", stated, data_accelerator=acc)} {self.label("of")} '
                f'{self.derived("acc-rows", str(len(mine)), data_accelerator=acc)} {self.label("links")}</span>'
                f'<span class="units">{units}</span></li>'
            )
        k2 = (
            f'<div class="indicator">{self.label("Links on stated evidence", tag="h4")}<ul class="tallies">{"".join(lines)}</ul>'
            f'<p class="how">{self.derived("row-count", str(len(rows)))} {self.label("rows in the table show")} '
            f'{self.derived("record-count", str(len({r["record_id"] for r in rows})))} '
            f'{self.label("records: one record can appear under more than one accelerator, and an unknown supplier sits on the link it qualifies.")}</p></div>'
        )
        # evidence dated: first and last date of the columns the table shows
        first, last = self.dates()
        undated = str(sum(r["evidence_dated_from"] == "not_applicable" for r in rows))
        k3 = (
            f'<div class="indicator">{self.label("Evidence dated", tag="h4")}'
            f'<p class="value range">{self.derived("date-first", first)} {self.label("to")} {self.derived("date-last", last)}</p>'
            f'<p class="den">{self.derived("undated-count", undated)} {self.label("of")} {self.derived("row-count", str(len(rows)))} {self.label("rows have nothing to date")}</p>'
            f'<p class="how">{self.label("Dates, not ages: an undated web page is dated by the day it was read.")}</p></div>'
        )
        # publishers behind a sourced link: a range, and how many rest on one
        sourced = [r for r in rows if r["publishers"]]
        counts = sorted(len(r["publishers"]) for r in sourced)
        rng = self.derived("pub-min", str(counts[0]))
        if counts[-1] != counts[0]:
            rng += f" {self.label('to')} {self.derived('pub-max', str(counts[-1]))}"
        k4 = (
            f'<div class="indicator">{self.label("Publishers behind a sourced link", tag="h4")}<p class="value range">{rng}</p>'
            f'<p class="den">{self.derived("one-pub-count", str(sum(len(r["publishers"]) == 1 for r in sourced)))} {self.label("of")} '
            f'{self.derived("sourced-count", str(len(sourced)))} {self.label("sourced rows rest on one publisher")}</p>'
            f'<p class="how">{self.label("Listed, never counted as confirmation.")}</p></div>'
        )
        return f'{self.label("Indicators", tag="h3", cls="indicators-h")}<div class="indicators">{k1}{k2}{k3}{k4}</div>'

    # --- layer 3 and 4: the visual and its filter ----------------------------------------------------

    def link(self, i: int, slot: str) -> str:
        r = self.rows[i]
        return (
            f'<a class="link {r["basis"]} s-{slot}" data-mark="strip" data-slot="{slot}" data-row="{i}" data-basis="{r["basis"]}" href="{CHAIN_HREF}#{self.target(i)}">'
            f'{self.cell(i, "relation", cls="rel")}<span class="wire" aria-hidden="true"></span>'
            f'<span class="b">{self.basis_words(i)}</span><span class="dates">{self.dated(i)}</span></a>'
        )

    def node(self, i: int, end: str, kicker: str, area: str) -> str:
        record = self.rows[i][f"{end}_id"]
        return f'<div class="node {self.kind(record)} a-{area}">{self.label(kicker, cls="nk")}{self.cell(i, f"{end}_name", cls="nn")}</div>'

    def strip(self, acc: str, slots: dict[str, int]) -> str:
        part = slots["part"]
        cells = []
        if "actor" in slots:
            cells.append(self.node(slots["actor"], "from", "acts on it", "actor"))
            cells.append(self.link(slots["actor"], "actor"))
        else:
            cells.append(f'<div class="node norecord a-actor">{self.label("no recorded relationship")}</div>')
            cells.append(f'<span class="link norecord s-actor" data-slot="actor">{self.label("no recorded relationship")}</span>')
        cells.append(f'<div class="node instance-level a-acc">{self.label("accelerator", cls="nk")}{self.cell(part, "accelerator", cls="nn")}</div>')
        cells.append(self.link(part, "part"))
        cells.append(self.node(part, "to", "it incorporates", "part"))
        if "supplier" in slots:
            i = slots["supplier"]
            r = self.rows[i]
            cells.append(
                f'<a class="slot {r["basis"]} s-supplier" data-mark="strip" data-slot="supplier" data-row="{i}" data-basis="{r["basis"]}" href="{CHAIN_HREF}#{self.target(i)}">'
                f'{self.label("who makes that part", cls="nk")}<span class="b">{self.basis_words(i)}</span></a>'
            )
        else:
            cells.append(f'<span class="slot norecord s-supplier" data-slot="supplier">{self.label("no recorded relationship")}</span>')
        if "process" in slots:
            cells.append(self.link(slots["process"], "process"))
            cells.append(self.node(slots["process"], "to", "that part requires", "process"))
        else:
            cells.append(f'<span class="link norecord s-process" data-slot="process">{self.label("no recorded relationship")}</span>')
        head = self.new_id("strip")
        return (
            f'<section class="strip" data-strip="{esc(acc)}" aria-labelledby="{head}">'
            f'<h3 id="{head}">{self.cell(part, "accelerator")}</h3><div class="chain">{"".join(cells)}</div></section>'
        )

    def key(self) -> str:
        items = [
            ("k-stated", "stated: at least one cited claim is a FACT"),
            ("k-inferred", "inferred: every cited claim is a DERIVATION"),
            ("k-gap", "gap: an unknown value or a recorded gap, never a zero"),
            ("k-norecord", "no recorded relationship"),
            ("k-instance", "named thing (instance level)"),
            ("k-class", "vendor-neutral class (class level)"),
        ]
        return '<ul class="key">' + "".join(f'<li><span class="swatch {c}" aria-hidden="true"></span>{self.label(t)}</li>' for c, t in items) + "</ul>"

    def explore(self) -> str:
        options = [("all", "all links")] + [(b, b) for b in BASES]
        radios = "".join(
            f'<span class="opt"><input type="radio" name="basis" id="f-{v}" value="{v}"{" checked" if v == "all" else ""}>'
            f'<label for="f-{v}">{self.label(t)}</label></span>'
            for v, t in options
        )
        return (
            f'<fieldset class="filter"><legend>{self.label("Show links whose basis is")}</legend>{radios}'
            f'<p class="how">{self.label("Highlights the matching links in the chains and keeps only the matching rows in the table.")}</p></fieldset>'
        )

    # --- layer 5 to 7: evidence, data, method --------------------------------------------------------

    def evidence_index(self) -> str:
        items, seen = [], []
        for i, r in enumerate(self.rows):
            if r["record_id"] in seen:  # a supplier row follows the link it qualifies, so the link is listed
                continue
            seen.append(r["record_id"])
            shown = str(sum(x["record_id"] == r["record_id"] for x in self.rows))
            items.append(
                f'<li data-evidence-record="{esc(r["record_id"])}">{self.cell(i, "from_name", fmt="state" if r["from_id"] not in self.homes else None)} '
                f'{self.cell(i, "relation", cls="rel")} {self.cell(i, "to_name")} · {self.basis_words(i)} · '
                f'{self.label("table rows:", cls="k")} {self.derived("shown-in", shown, data_record=r["record_id"])} '
                f'<a class="ev-link" href="{CHAIN_HREF}#{self.target(i)}">{self.label("open the evidence")}</a></li>'
            )
        return (
            f'<ul class="evidence-index">{"".join(items)}</ul>'
            f'<p class="how">{self.label("Each line opens its evidence on the dependency journey page, which holds every panel.")} '
            f'<a href="{CHAIN_HREF}">{self.label("the full dependency journey")}</a></p>'
        )

    def table(self) -> str:
        if self.result != load_result(RESULT):
            raise BuildError("the table and the visual must render the same result")
        body = self.sql_section()
        rows = iter(range(len(self.rows)))

        def tag(_: re.Match) -> str:
            i = next(rows)
            return f'<tr id="row-{i}" data-basis="{esc(self.rows[i]["basis"])}">'

        head, sep, rest = body.partition("<tbody>")
        tbody, sep2, tail = rest.partition("</tbody>")
        tbody = re.sub(r"<tr>", tag, tbody)
        if next(rows, None) is not None:
            raise BuildError("the table does not show every row of the result")
        return head + sep + tbody + sep2 + tail

    def method(self) -> str:
        paths = input_paths()
        files = "".join(f'<li><a href="{TO_ROOT}{esc(p)}">{self.derived("input-file", p, tag="code")}</a></li>' for p in paths)
        rulings = "".join(f"<li>{self.decision(key)}</li>" for key in DECISIONS)
        return (
            f'{self.label("Rulings this page depends on", tag="h3")}<ul class="rulings">{rulings}</ul>'
            f'{self.label("Built from", tag="h3")}'
            f'<p>{self.label("input digest", cls="k")} {self.derived("input-digest", input_digest(paths), tag="code", cls="digest")}</p>'
            f'<details class="inputs"><summary>{self.label("input files")}</summary><ul class="files">{files}</ul></details>'
            f'{self.label("Reproduce", tag="h3")}'
            f'<pre><code>{self.label("rebuild the result:")}\n{self.label("python tools/warehouse.py --check")}\n'
            f'{self.label("rebuild this page:")}\n{self.label("python tools/build_insight.py --check")}</code></pre>'
        )

    # --- the page ------------------------------------------------------------------------------------

    def base_style(self) -> str:
        template = build_page.TEMPLATE.read_text(encoding="utf-8")
        style = re.search(r"<style>\n(.*?)</style>", template, re.S)
        if not style:
            raise BuildError("the S11 template has no style block to reuse")
        return style.group(1).replace("${palette}", " ".join(f"--{k}: {v};" for k, v in PALETTE.items()))

    def render(self) -> str:
        chains = self.chains()
        kind, headline = self.headline(chains)
        parts = {
            "base_style": self.base_style(),
            "question": self.question(),
            "headline_class": "finding" if kind == "finding" else "question",
            "headline": headline,
            "scope": self.scope(),
            "comparison": self.comparison(chains),
            "indicators": self.indicators(chains),
            "key": self.key(),
            "explore": self.explore(),
            "strips": "".join(self.strip(acc, slots) for acc, slots in chains.items()),
            "evidence": self.evidence_index(),
            "table": self.table(),
            "method": self.method(),
        }
        parts["title"] = esc(html.unescape(re.sub(r"<[^>]+>", "", headline)))
        return string.Template(TEMPLATE.read_text(encoding="utf-8")).substitute(parts)


def build(data: Path = DATA) -> bytes:
    return Insight(data).render().encode("utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the S14.5 visual prototype from the S14 SQL result and the Atlas's records.")
    parser.add_argument("--check", action="store_true", help="rebuild in memory and compare with the committed page")
    args = parser.parse_args(argv[1:])
    try:
        page = build()
    except BuildError as error:
        print(f"build refused: {error}")
        return 1
    if args.check:
        same = PAGE.exists() and PAGE.read_bytes() == page
        print("page: up to date" if same else f"page: differs from a rebuild ({PAGE.relative_to(REPO_ROOT)}); run python tools/build_insight.py")
        return 0 if same else 1
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_bytes(page)
    print(f"wrote {PAGE.relative_to(REPO_ROOT)} ({len(page)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
