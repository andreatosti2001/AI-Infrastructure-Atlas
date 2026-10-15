"""Build the S21 client brief from the Atlas's records (docs/architecture/client-brief.md; D-202 to D-206).

Writes site/briefs/accelerator-memory/index.html: one self-contained, printable page with inline CSS and SVG and no
script. It answers one question over a stated scope: "What does an AI accelerator's memory depend on, who is
reported to supply it, and which recorded export-control texts name those parts?"

The Client Output's build (contracts.md, D-205). It summarises and never alters a record (MA §11.10): every value
comes from a canonical record or a committed SQL result through the machinery of build_page.Page and
build_journeys.Journey (record values, labels, derived values, the HBM figure, panels, cards, the policy matrix,
statuses, the palette). The summary groups and tallies the dependency result's rows (D-124 rules a to d); an act's
status comes from tools/policy_status.py on the as-of date (D-156, D-191). Nothing else is computed. DuckDB is
never imported (D-118).

Usage:
    python tools/build_brief.py           write the brief
    python tools/build_brief.py --check   rebuild in memory; exit 1 if the committed brief differs

Run it last: after tools/warehouse.py, tools/build_page.py, tools/build_insight.py and tools/build_journeys.py (the
brief links the journey pages, and the build refuses a link with no target). The checks are tests/test_brief.py
(BR-1 to BR-12). Standard library only (D-003).
"""

from __future__ import annotations

import argparse
import html
import json
import re
import string
import sys
from pathlib import Path

import build_journeys
import build_page
from build_page import DATA, REPO_ROOT, BuildError, esc, input_digest

TEMPLATE = REPO_ROOT / "tools" / "brief_template.html"
PAGE = build_journeys.BRIEF  # one home for the path: the entry page links it (D-206)
DEP = build_page.SQL_QUERY  # the dependency result the brief summarises (S14)
INPUT_GLOBS = build_page.INPUT_GLOBS
INPUT_FILES = (
    "docs/architecture/company-dataset.md",
    "docs/architecture/decisions.md",
    "docs/architecture/relationship-taxonomy.md",
    "docs/research/change-detection.md",
    "docs/research/source-policy.md",
    "tools/brief_template.html",
    "tools/build_brief.py",
    "tools/build_journeys.py",
    "tools/build_page.py",
    "tools/evidence_age.py",
    "tools/facility_status.py",
    "tools/journey_template.html",
    "tools/navigate.py",
    "tools/page_template.html",
    "tools/policy_status.py",
    "tools/trace.py",
)
RULINGS = ("D-094", "D-124", "D-147", "D-148", "D-156", "D-161", "D-167", "D-172", "D-175", "D-202", "D-203", "D-204")
BOUNDARY = "This brief describes what the Atlas’s records hold. It is not legal, investment or procurement advice, and it makes no recommendation."

# Every fixed word the brief adds (BR-1): none names a record or holds a digit.
LABELS = build_journeys.LABELS | frozenset(
    {
        BOUNDARY, "Client brief", "built by", "tools/build_brief.py", "read as of",
        "Evidence, each claim once", "derived from",  # S22: the printed evidence list (D-210, D-214)
        "’s memory depend on, who is reported to supply it, and which recorded export-control texts name those parts?",
        "Question and scope", "Executive summary", "Dependency map", "Export-control texts", "Key entities",
        "Recent changes", "Evidence gaps and caveats", "What this brief does not track", "Methodology",
        "Evidence appendix", "Source appendix", "How to cite this brief",
        "The chain:", "accelerator recorded", "accelerators recorded", "rows of the dependency result shown",
        "row of the dependency result shown", "act recorded, issued in", "acts recorded, issued in",
        "class the chain reaches", "classes the chain reaches", "Out of scope", "Later texts were searched for up to", "; texts published after it were not searched.",
        "At a glance", "Accelerators", "Chain rows", "Acts", "Classes compared",
        "each", "which", "a recorded gap, not a link", "Who designs or fabricates each accelerator:",
        "Who supplies that memory, as reported:", "in", "source-policy criterion not met:",
        "named in a recorded act:", "considered for a recorded act and refused:", "no recorded relationship with a recorded act:", "status on",
        "The chain as a table", "The classes against the acts", "Statuses on the as-of date",
        "the export-control comparison", "Name", "On this chain", "Headquartered in", "Profile",
        "company page", "vendor of", "designs or fabricates", "Dated events of the acts", "The latest publication date the Atlas holds:",
        "Evidence on the chain dated from", "Classes named by a recorded act that the chain does not reach",
        "named among the items controlled by", "acts", "no recorded dependency link to this chain",
        "Caveats from the result", "Rulings this brief depends on", "Inputs", "rebuild this brief:",
        "python tools/build_brief.py --check", "the dependency result:", "the policy links of one class:",
        "Source", "Publisher", "Class", "Stated dates", "Accessed", "client brief, as of", "Policy texts and links",
        "Refused policy candidates", "Policy events", "The chain’s records", "the evidence", "act",
    }
)


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


def template_parts(path: Path = TEMPLATE) -> tuple[str, dict[str, str]]:
    """The documented composition mechanism (client-brief.md §6, A-3): one skeleton with named slots, and named
    framing blocks after it, each opened by "<!-- framing: name -->"."""
    text = path.read_text(encoding="utf-8")
    skeleton, _, rest = text.partition("<!-- framing: ")
    blocks = {}
    for chunk in ("<!-- framing: " + rest).split("<!-- framing: ")[1:]:
        name, _, body = chunk.partition(" -->\n")
        if name.startswith("end framing"):
            continue
        blocks[name] = body.split("<!-- ")[0].strip("\n")
    return skeleton, blocks


def pages() -> list[str]:
    return [PAGE]


class Brief(build_journeys.Journey):
    def __init__(self, data: Path = DATA) -> None:
        super().__init__(PAGE, "brief", None, data)
        self.skeleton, self.framings = template_parts()
        self.result = json.loads((REPO_ROOT / "sql" / "results" / f"{DEP}.json").read_text(encoding="utf-8"))
        self.rows = self.result["rows"]
        known = {"designs", "fabricates", "incorporates", "supplier", "requires"}
        if not self.rows or {r["relation"] for r in self.rows} - known:
            raise BuildError("the dependency result has a relation the brief's summary does not know")

    @staticmethod
    def label_text(text: str) -> str:
        if text not in LABELS:
            raise BuildError(f"not a label: {text!r}")
        return text

    def endpoint(self, cand_id: str, pointer: str, value, panels: set[str] | None = None) -> str:
        """A candidate's party or item: the HBM page's form inside its gap blocks (with the panels it links), the
        journeys' form (company and act links) on the policy cards."""
        if panels is not None:
            return build_page.Page.endpoint(self, cand_id, pointer, value, panels)
        return super().endpoint(cand_id, pointer, value)

    # --- what the brief reads ----------------------------------------------------------------------------

    def cell(self, i: int, column: str, item: int | None = None, cls: str | None = None) -> str:
        value = self.rows[i][column] if item is None else self.rows[i][column][item]
        state = column in ("gap_reason",) or (column == "from_name" and self.rows[i]["from_id"] not in self.homes)
        return self.sql_cell(i, column, value, item=item, fmt="state" if state else None, cls=cls)

    def chain_classes(self) -> list[str]:
        """The classes the chain reaches (client-brief.md §3.4): each accelerator's class with the classes it is
        narrower than, then every class at an end of a row; a grouping of record IDs, not a metric."""
        found: list[str] = []
        for row in self.rows:
            cls = row["accelerator_class"]
            for c in self.homes[cls].get("broader", []) + [cls]:
                if c not in found:
                    found.append(c)
        for row in self.rows:
            for end in (row["from_id"], row["to_id"]):
                if self.homes.get(end, {}).get("type") in ("component", "technology") and end not in found:
                    found.append(end)
        return found

    def targets(self) -> list[str]:
        """The policy matrix's rows on the brief: the classes the chain reaches (the export page shows every pair)."""
        return self.chain_classes()

    def class_state(self, cid: str) -> str:
        if any(e["target_entity"] == cid for e in self.links):
            return "named"
        return "refused" if any(cid in c["target_entities"] for c in self.policy_candidates) else "none"

    def accelerators(self) -> list[str]:
        return list(dict.fromkeys(r["accelerator_id"] for r in self.rows))

    def latest(self) -> str:
        return self.derived("latest-published", max(e["date"] for e in self.events if e["event_type"] == "published" and e["subject"] in {p["id"] for p in self.policies}))

    def searched_to(self) -> str:
        return self.derived("searched-to", build_journeys.searched_to())

    def question(self) -> str:
        return f'{self.label("What does an")} {self.name("component-ai-accelerator")}{self.label("’s memory depend on, who is reported to supply it, and which recorded export-control texts name those parts?")}'

    def digest(self) -> str:
        return self.derived("input-digest", input_digest(input_paths()), tag="code", cls="digest")

    # --- 1 question and scope ----------------------------------------------------------------------------

    def scope(self) -> str:
        accs, classes = self.accelerators(), self.chain_classes()
        issued = list(dict.fromkeys(a["value"] for p in self.policies for a in p["issued_in"]))
        n_rows = len(self.rows)
        line = (
            f'<ul class="scope-list"><li>{self.label("The chain:", cls="k")} {self.count(len(accs), "accelerators", cls="")} '
            f'{self.unit(len(accs), "accelerator recorded", "accelerators recorded")} ('
            + ", ".join(self.name(a) for a in accs)
            + f'); {self.count(n_rows, "rows-shown", cls="")} {self.label("of")} {self.count(n_rows, "rows-in-result", cls="")} '
            f'{self.unit(n_rows, "row of the dependency result shown", "rows of the dependency result shown")}</li>'
            f'<li>{self.count(len(self.policies), "acts", cls="")} {self.unit(len(self.policies), "act recorded, issued in", "acts recorded, issued in")} '
            + ", ".join(self.place_link(j) for j in issued)
            + f'; {self.count(len(classes), "chain-classes", cls="")} {self.unit(len(classes), "class the chain reaches", "classes the chain reaches")}</li></ul>'
        )
        limits = (
            f'<div class="limits" data-limits>{self.label("Out of scope", tag="h3")}{self.framing("brief-out-of-scope")}'
            f'<p>{self.label("Later texts were searched for up to")} {self.searched_to()}{self.label("; texts published after it were not searched.")}</p></div>'
        )
        identity = (
            f'<p class="identity" data-identity>{self.label("read as of", cls="k")} {self.as_of()} · {self.label("input digest", cls="k")} {self.digest()} · '
            f'{self.label("built by", cls="k")} {self.label("tools/build_brief.py", tag="code")}</p>'
        )
        return f'{identity}{self.framing("brief-scope")}{line}{limits}'

    # --- 2 the executive summary (client-brief.md §3) ---------------------------------------------------

    def tiles(self) -> str:
        accs, classes, n = self.accelerators(), self.chain_classes(), len(self.rows)
        return (
            f'{self.label("At a glance", tag="h3", cls="visually-quiet")}<div class="tiles">'
            + self.tile("Accelerators", f'<p class="stat">{self.count(len(accs), "accelerators")} {self.unit(len(accs), "accelerator recorded", "accelerators recorded")}</p>')
            + self.tile("Chain rows", f'<p class="stat">{self.count(n, "rows-shown")} {self.label("of")} {self.count(n, "rows-in-result", cls="tally-s")} {self.unit(n, "row of the dependency result shown", "rows of the dependency result shown")}</p>')
            + self.tile("Acts", f'<p class="stat">{self.count(len(self.policies), "acts")} {self.unit(len(self.policies), "act recorded, issued in", "acts recorded, issued in")} '
                        + ", ".join(self.name(j) for j in dict.fromkeys(a["value"] for p in self.policies for a in p["issued_in"])) + "</p>")
            + self.tile("Classes compared", f'<p class="stat">{self.count(len(classes), "chain-classes")} {self.unit(len(classes), "class the chain reaches", "classes the chain reaches")}</p>')
            + "</div>"
        )

    def flags(self, i: int) -> str:
        return f' · {self.derived("sql-flag", build_page.SQL_FLAGS["rests_on_atlas_interpretation"], data_row=str(i), data_column="rests_on_atlas_interpretation")}' if self.rows[i]["rests_on_atlas_interpretation"] else ""

    def depends(self) -> list[str]:
        """One sentence per part the accelerators incorporate: who incorporates it (each row with its basis) and what
        it requires (one row: the same record under each accelerator, D-124 rule 4)."""
        out = []
        inc = [i for i, r in enumerate(self.rows) if r["relation"] == "incorporates"]
        for part in dict.fromkeys(self.rows[i]["to_id"] for i in inc):
            group = [i for i in inc if self.rows[i]["to_id"] == part]
            who = f" {self.label('and')} ".join(f'{self.cell(i, "accelerator")} ({self.cell(i, "basis", cls="basis " + self.rows[i]["basis"])})' for i in group)
            each = f" {self.label('each')}" if len(group) > 1 else ""
            first = group[0]
            text = f'{who}{each} {self.cell(first, "relation", cls="rel")} {self.cell(first, "to_name")}'
            req = [i for i, r in enumerate(self.rows) if r["relation"] == "requires" and r["from_id"] == part]
            if len({self.rows[i]["record_id"] for i in req}) > 1:
                raise BuildError(f"{part}: its requires rows are several records; the sentence is written for one")
            if req:
                k = req[0]
                text += f', {self.label("which")} {self.cell(k, "relation", cls="rel")} {self.cell(k, "to_name")} ({self.cell(k, "basis", cls="basis " + self.rows[k]["basis"])}{self.flags(k)})'
            out.append(f'<li data-summary="depends">{text}.</li>')
        return out

    def made(self) -> str:
        parts = []
        for i, r in enumerate(self.rows):
            if r["position"] != 1:
                continue
            if r["basis"] == "gap":
                parts.append(
                    f'<span data-gap-row="{i}">{self.cell(i, "from_name")} → {self.cell(i, "to_name")}, {self.cell(i, "relation", cls="rel")}: '
                    f'{self.label("a recorded gap, not a link", cls="basis gap")} ({self.cell(i, "gap_reason")})</span>'
                )
            else:
                parts.append(f'{self.cell(i, "from_name")} {self.cell(i, "relation", cls="rel")} {self.cell(i, "to_name")} ({self.cell(i, "basis", cls="basis " + r["basis"])})')
        return f'<li data-summary="made">{self.label("Who designs or fabricates each accelerator:")} ' + "; ".join(parts) + ".</li>"

    def supplied(self) -> str:
        parts = []
        for i, r in enumerate(self.rows):
            if r["relation"] != "supplier":
                continue
            words = f'{self.cell(i, "from_name")} {self.label("in")} {self.cell(i, "accelerator")} ({self.cell(i, "basis", cls="basis " + r["basis"])}'
            if r["period_to"] != "not_applicable":
                words += f'; {self.label("historical, to")} {self.cell(i, "period_to")}'
            for k in range(len(r["criteria_unmet"])):
                words += f'; {self.label("source-policy criterion not met:")} {self.cell(i, "criteria_unmet", item=k)}'
            parts.append(words + ")")
        return f'<li data-summary="supplied">{self.label("Who supplies that memory, as reported:")} ' + "; ".join(parts) + ".</li>"

    def class_words(self, cid: str, state: str) -> str:
        if state == "named":
            links = [e for e in self.links if e["target_entity"] == cid]
            acts = ", ".join(f'{self.act_link(e["source_entity"])} ({self.label("status on")} {self.as_of()}: {self.status(e["source_entity"])})' for e in links)
            return f'<span data-class="{esc(cid)}">{self.name(cid)}, {self.label("by")} {acts}</span>'
        if state == "refused":
            cands = [c for c in self.policy_candidates if cid in c["target_entities"]]
            body = "; ".join(f'{self.reasons(c)}, {self.label("by")} ' + ", ".join(self.act_link(s) for s in c["source_entities"] if isinstance(s, str)) for c in cands)
            return f'<span data-class="{esc(cid)}">{self.name(cid)} ({body})</span>'
        return f'<span data-class="{esc(cid)}">{self.name(cid)}</span>'

    def texts(self) -> list[str]:
        classes = self.chain_classes()
        heads = {"named": "named in a recorded act:", "refused": "considered for a recorded act and refused:", "none": "no recorded relationship with a recorded act:"}
        out = []
        for state in ("named", "refused", "none"):
            group = [c for c in classes if self.class_state(c) == state]
            if not group:
                continue
            out.append(
                f'<li data-summary="texts-{state}">{self.count(len(group), f"classes-{state}")} {self.label("of")} {self.count(len(classes), "chain-classes")} '
                f'{self.unit(len(classes), "class the chain reaches", "classes the chain reaches")} · {self.label(heads[state])} ' + "; ".join(self.class_words(c, state) for c in group) + ".</li>"
            )
        return out

    def summary(self) -> str:
        items = self.depends() + [self.made(), self.supplied()] + self.texts()
        items.append(f'<li data-summary="limits">{self.label("Later texts were searched for up to")} {self.searched_to()}{self.label("; texts published after it were not searched.")}</li>')
        return f'{self.tiles()}<ul class="findings summary">{"".join(items)}</ul>{self.framing("brief-summary")}'

    # --- 3 to 8 ------------------------------------------------------------------------------------------

    def texts_section(self, acts: list[dict]) -> str:
        statuses = "".join(f'<li>{self.act_link(a["id"])} · {self.label("status on")} {self.as_of()}: {self.status(a["id"])}</li>' for a in acts)
        return (
            f'{self.framing("brief-texts")}{self.label("The classes against the acts", tag="h3")}{self.matrix(acts)}'
            f'{self.label("Statuses on the as-of date", tag="h3")}{self.howto("brief-status", "What a status means")}<ul class="items">{statuses}</ul>'
            f'<p><a href="{self.href(build_journeys.EXPORT)}">{self.label("the export-control comparison")}</a></p>'
        )

    def entities(self) -> str:
        rows = []
        companies = list(dict.fromkeys([r["from_id"] for r in self.rows if self.homes.get(r["from_id"], {}).get("type") == "company"]
                                       + [self.homes[a]["vendor"] for a in self.accelerators() if "vendor" in self.homes[a]]))
        for cid in companies:
            what = [f'{self.cell(i, "relation", cls="rel")} {self.cell(i, "to_name")} ({self.cell(i, "basis", cls="basis " + r["basis"])})'
                    for i, r in enumerate(self.rows) if r["from_id"] == cid]
            what += [f'{self.label("vendor of")} {self.name(a)}' for a in self.accelerators() if self.homes[a].get("vendor") == cid]
            page = f"site/companies/{cid}/index.html"
            rows.append((cid, self.company_link(cid), self.ref(cid, "/type"), "; ".join(what), self.values(cid, "headquartered_in", self.place_link), f'<a href="{self.href(page)}">{self.label("company page")}</a>'))
        for a in self.accelerators():
            what = [f'{self.cell(i, "relation", cls="rel")} {self.cell(i, "to_name")} ({self.cell(i, "basis", cls="basis " + r["basis"])})'
                    for i, r in enumerate(self.rows) if r["from_id"] == a]
            rows.append((a, self.name(a), self.ref(a, "/type"), "; ".join(what), "", self.ev(a)))
        heads = ("Name", "type", "On this chain", "Headquartered in", "Profile")
        k = {h: self.label(h, cls="cell-k") for h in heads}
        body = "".join(f'<tr data-entity="{esc(rid)}">' + "".join(f"<td>{k[h]}{c}</td>" for h, c in zip(heads, cells)) + "</tr>" for rid, *cells in rows)
        head = "".join(f'<th scope="col">{self.label(h)}</th>' for h in heads)
        return f'{self.framing("brief-entities")}<div class="table-wrap"><table class="sql entities"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

    def changes(self, acts: list[dict]) -> str:
        ids = {a["id"] for a in acts}
        events = sorted((e for e in self.events if e["subject"] in ids), key=lambda e: (e["date"], e["id"]))
        items = "".join(
            f'<li data-event-word="{esc(e["id"])}">{self.ref(e["id"], "/date")} · {self.act_link(e["subject"])} · {self.ref(e["id"], "/event_type", fmt="state")} {self.ev(e["id"])}</li>'
            for e in events
        )
        dated_from = [r["evidence_dated_from"] for r in self.rows if r["evidence_dated_from"] != "not_applicable"]
        dated_to = [r["evidence_dated_to"] for r in self.rows if r["evidence_dated_to"] != "not_applicable"]
        return (
            f'{self.framing("brief-changes")}'
            f'<p>{self.label("The latest publication date the Atlas holds:", cls="k")} {self.latest()}</p>'
            f'<p>{self.label("Evidence on the chain dated from", cls="k")} {self.derived("evidence-first", min(dated_from))} {self.label("to")} {self.derived("evidence-last", max(dated_to))}</p>'
            f'{self.label("Dated events of the acts", tag="h3")}<ul class="items">{items}</ul>'
        )

    def gaps_section(self, j: dict) -> str:
        chain = set(self.chain_classes())
        unreached = list(dict.fromkeys(e["target_entity"] for e in self.links if e["target_entity"] not in chain))
        lines = "".join(
            f'<li data-unreached="{esc(t)}">{self.name(t)} · {self.label("named among the items controlled by")} '
            f'{self.count(sum(e["target_entity"] == t for e in self.links), "unreached-named-by", t, cls="")} {self.label("of")} {self.count(len(self.policies), "acts", cls="")} {self.label("acts")}: '
            + ", ".join(self.act_link(e["source_entity"]) for e in self.links if e["target_entity"] == t)
            + f' · {self.label("no recorded dependency link to this chain", cls="none-word")}</li>'
            for t in unreached
        )
        caveats = []
        for i, r in enumerate(self.rows):
            flags = []
            if r["rests_on_atlas_interpretation"]:
                flags.append(self.derived("sql-flag", build_page.SQL_FLAGS["rests_on_atlas_interpretation"], data_row=str(i), data_column="rests_on_atlas_interpretation"))
            if len(r["publishers"]) == 1:
                flags.append(self.derived("sql-flag", build_page.SQL_FLAGS["publishers"], data_row=str(i), data_column="publishers"))
            for column in ("evidence_dated_to_basis", "evidence_dated_from_basis"):
                if r[column] == "accessed":
                    flags.append(self.derived("sql-flag", build_page.SQL_FLAGS[column], data_row=str(i), data_column=column))
                    break
            if flags:
                caveats.append(f'<li>{self.cell(i, "accelerator")} · {self.cell(i, "from_name")} {self.cell(i, "relation", cls="rel")} {self.cell(i, "to_name")}: ' + "; ".join(flags) + "</li>")
        return (
            f'{self.framing("brief-gaps")}{self.gaps(j)}{self.rules_cited()}'
            + (f'{self.label("Classes named by a recorded act that the chain does not reach", tag="h3")}<ul class="items">{lines}</ul>' if lines else "")
            + f'{self.label("Caveats from the result", tag="h3")}<ul class="items">{"".join(caveats)}</ul>'
        )

    # --- 9 to 11 -----------------------------------------------------------------------------------------

    def method_section(self, acts: list[dict]) -> str:
        paths = input_paths()
        files = "".join(f'<li><a href="{self.to_root}{esc(p)}">{self.derived("input-file", p, tag="code")}</a></li>' for p in paths)
        rulings = "".join(f"<li>{self.decision(key)}</li>" for key in RULINGS)
        hbm = "component-high-bandwidth-memory"
        reproduce = (
            f'{self.label("the dependency result:")}\n{self.label("python tools/warehouse.py --check")}\n'
            f'{self.label("the policy links of one class:")}\n{self.label("python tools/navigate.py edges")} {self.ref(hbm, "/id")} {self.label("--on")} {self.as_of()}\n'
            f'{self.label("one act’s status:")}\n{self.label("python tools/policy_status.py")} {self.act_link(acts[0]["id"], "/id")} {self.label("--on")} {self.as_of()}\n'
            f'{self.label("rebuild this brief:")}\n{self.label("python tools/build_brief.py --check")}'
        )
        return (
            f'{self.framing("brief-method")}'
            f'{self.label("Rulings this brief depends on", tag="h3")}<ul class="rulings">{rulings}</ul>'
            f'{self.label("Inputs", tag="h3")}<p>{self.label("input digest", cls="k")} {self.digest()}</p>'
            f'<details class="inputs"><summary>{self.label("input files")}</summary><ul class="files">{files}</ul></details>'
            f'{self.label("Reproduce", tag="h3")}<pre><code>{reproduce}</code></pre>'
        )

    def evidence_section(self, j: dict, acts: list[dict]) -> str:
        cands = [c for c in self.policy_candidates if set(c["target_entities"]) & set(self.chain_classes())]
        ids = {a["id"] for a in acts}
        events = sorted((e for e in self.events if e["subject"] in ids), key=lambda e: (e["date"], e["id"]))
        return (
            self.label("The chain’s records", tag="h3") + self.evidence(j)
            + self.label("Policy texts and links", tag="h3") + "".join(self.act_panel(a) for a in acts) + "".join(self.link_panel(e) for e in self.links)
            + self.label("Refused policy candidates", tag="h3") + f'<ul class="cards refusals">{"".join(self.card(c) for c in cands)}</ul>'
            + self.label("Policy events", tag="h3") + "".join(self.event_panel(e) for e in events)
        )

    def claim_card(self, claim_id: str, panel: str, shown: set[str]) -> str:
        if getattr(self, "appendix_claims", None) is not None and claim_id not in self.appendix_claims:
            self.appendix_claims.append(claim_id)
        return super().claim_card(claim_id, panel, shown)

    def print_list(self, claims: list[str]) -> str:
        """In print only, the evidence appendix as one list: each claim once, with its statement and, per citation, the
        source and the locator (D-210, D-214; BR-13). The screen keeps the panels; print hides them."""
        items = []
        for cid in claims:
            claim = self.store.claims[cid]
            if claim.get("citations"):
                where = "; ".join(
                    f'{self.ref(c["source_id"], "/title", tag="cite")} ({self.ref(c["source_id"], "/id", tag="code")}), {self.ref(cid, f"/citations/{k}/locator")}'
                    for k, c in enumerate(claim["citations"]))
                meta = f'{self.label("source", cls="k")} {where}'
            else:
                meta = f'{self.label("derived from", cls="k")} ' + ", ".join(self.ref(cid, f"/input_claim_ids/{k}", tag="code") for k in range(len(claim.get("input_claim_ids", []))))
            items.append(f'<li data-claim="{esc(cid)}"><p>{self.ref(cid, "/statement")}</p><p class="meta">{self.ref(cid, "/id", tag="code")} · {meta}</p></li>')
        body = self.framing("brief-evidence-print") + f'<ol class="print-list">{"".join(items)}</ol>'
        return self.section("evidence-print", "Evidence, each claim once", body).replace('<section id="evidence-print"', '<section id="evidence-print" class="print-only"', 1)

    def sources_section(self) -> str:
        heads = ("Source", "Publisher", "Class", "Stated dates", "Accessed", "URL")
        k = {h: self.label(h, cls="cell-k") for h in heads}
        body = []
        for sid in sorted(self.sources_shown):
            source = self.store.sources[sid]
            s = lambda field, **kw: self.ref(sid, field, **kw)  # noqa: E731
            if isinstance(source["stated_dates"], dict):
                dates = s("/stated_dates/state", fmt="state")
            else:
                dates = "; ".join(f'{s(f"/stated_dates/{i}/kind")} {s(f"/stated_dates/{i}/date")}' for i in range(len(source["stated_dates"])))
            cells = (
                f'{s("/id", tag="code")} {s("/title", tag="cite")}', s("/publisher"), s("/source_class", cls="tag"), dates,
                s("/retrieval/accessed_at"), s("/url", tag="a", href=source["url"], rel="noopener noreferrer", cls="url"),
            )
            body.append(f'<tr data-source="{esc(sid)}">' + "".join(f"<td>{k[h]}{c}</td>" for h, c in zip(heads, cells)) + "</tr>")
        head = "".join(f'<th scope="col">{self.label(h)}</th>' for h in heads)
        citation = (
            f'<div class="cite-this" data-citation>{self.label("How to cite this brief", tag="h3")}<p>{self.label("AI Infrastructure Atlas")}, “{self.question()}”, '
            f'{self.label("client brief, as of")} {self.as_of()}, {self.label("input digest")} {self.digest()}.</p></div>'
        )
        return f'{self.framing("brief-sources")}<div class="table-wrap"><table class="sql sources"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>{citation}'

    # --- the page ----------------------------------------------------------------------------------------

    def render_brief(self) -> dict:
        j = self.journey()
        acts = self.acts_in_order()
        figure = self.figure(j)
        # the evidence is rendered before the method and sources: they list what the panels show
        self.appendix_claims: list[str] | None = []  # the claims the appendix shows, in order of first appearance
        evidence = self.evidence_section(j, acts)
        printed = self.print_list(self.appendix_claims)
        self.appendix_claims = None
        main = (
            self.section("scope", "Question and scope", self.scope())
            + self.section("summary", "Executive summary", self.summary())
            + self.section("map", "Dependency map", f'<div class="chain-grid"><figure>{figure}</figure><div>{self.howto("brief-map", "How to read the diagram")}{self.legend()}'
                           f'{self.label("The chain in words", tag="h3")}{self.words(j)}</div></div>' + self.label("The chain as a table", tag="h3") + self.sql_section())
            + self.section("texts", "Export-control texts", self.texts_section(acts))
            + self.section("entities", "Key entities", self.entities())
            + self.section("changes", "Recent changes", self.changes(acts))
            + self.section("gaps", "Evidence gaps and caveats", self.gaps_section(j))
            + self.section("not-tracked", "What this brief does not track", self.framing("brief-not-tracked"))
            + self.section("method", "Methodology", self.method_section(acts))
            + self.section("evidence", "Evidence appendix", evidence)
            + printed
            + self.section("sources", "Source appendix", self.sources_section())
        )
        main += self.terms_section()
        return {
            "kicker": f'{self.label("AI Infrastructure Atlas")}{self.label("Client brief")}',
            "crumbs": f'<p class="crumbs"><a href="{self.href(build_journeys.INDEX)}">{self.label("All research pages")}</a></p>',
            "h1": self.question(),
            "boundary": f'<p class="boundary" data-boundary data-label>{esc(self.label_text(BOUNDARY))}</p>',
            "framing_top": self.framing("brief-top"),
            "jump": self.jump([("summary", "Executive summary"), ("map", "Dependency map"), ("texts", "Export-control texts"), ("gaps", "Evidence gaps and caveats"),
                               ("method", "Methodology"), ("evidence", "Evidence appendix"), ("sources", "Source appendix")]),
            "main": main,
        }

    def journey_style(self) -> str:
        """The journey template's components, read from their one home (the documented style slot, A-3)."""
        text = build_journeys.TEMPLATE.read_text(encoding="utf-8")
        style = re.search(r"<style>\n\$\{base_style\}\n(.*?)</style>", text, re.S)
        if not style:
            raise BuildError("the journey template has no component style to reuse")
        return style.group(1)

    def render(self) -> str:
        parts = self.render_brief()
        parts |= {"base_style": self.base_style(), "journey_style": self.journey_style(), "body_attrs": 'data-page-kind="brief"',
                  "title": esc(html.unescape(re.sub(r"<[^>]+>", "", parts["h1"])))}
        return string.Template(self.skeleton).substitute(parts)


def build(data: Path = DATA) -> dict[str, bytes]:
    return {PAGE: Brief(data).render().encode("utf-8")}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the S21 client brief from the Atlas's records.")
    parser.add_argument("--check", action="store_true", help="rebuild in memory and compare with the committed brief")
    args = parser.parse_args(argv[1:])
    try:
        built = build()
    except BuildError as error:
        print(f"build refused: {error}")
        return 1
    if args.check:
        stale = [rel for rel, content in built.items() if not (REPO_ROOT / rel).exists() or (REPO_ROOT / rel).read_bytes() != content]
        print("brief: up to date" if not stale else f"brief: differs from a rebuild ({', '.join(stale)}); run python tools/build_brief.py")
        return 0 if not stale else 1
    for rel, content in built.items():
        (REPO_ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        (REPO_ROOT / rel).write_bytes(content)
    print(f"wrote {PAGE} ({sum(len(c) for c in built.values())} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
