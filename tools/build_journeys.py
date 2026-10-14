"""Build the S20 research journeys from the Atlas's records (visual-architecture.md §15; D-189 to D-193).

Writes 15 self-contained pages, with inline CSS and SVG and no script:

    site/index.html                                  the entry page: "What are you trying to understand?"
    site/questions/export-control-texts/index.html   which classes each recorded export-control text names (D-191)
    site/companies/<company-id>/index.html           what the Atlas records about one company (D-192)
    site/places/<jurisdiction-id>/index.html         what is incorporated, headquartered, located or issued there

Every value comes from a canonical record, through `build_page.Page`'s machinery (record values, labels, derived
values, claim cards, evidence panels, the palette), or from one committed SQL cell: the as-of date, the source-age
reference date of sql/results/source_age.json (D-137, D-191). The build copies values, counts the rows it draws, and
derives an act's status on the as-of date with tools/policy_status.py, the one home of that rule (D-156; D-191
amends D-124 rule 3 for this). DuckDB is never imported (D-118).

Usage:
    python tools/build_journeys.py           write the pages
    python tools/build_journeys.py --check   rebuild in memory; exit 1 if a committed page differs

Run it after tools/warehouse.py, tools/build_page.py and tools/build_insight.py: the entry page links the two pages
they write, and the build refuses a link with no target. The checks are tests/test_journeys.py (JR-1 to JR-12).
Standard library only (D-003).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import html
import json
import os
import re
import string
import sys
from pathlib import Path

import build_page
import navigate
from build_page import DATA, PALETTE, REPO_ROOT, BuildError, esc, input_digest
from facility_status import period

TEMPLATE = REPO_ROOT / "tools" / "journey_template.html"
AGE_QUERY = "source_age"
INDEX = "site/index.html"
EXPORT = "site/questions/export-control-texts/index.html"
CHAIN_PAGE, INSIGHT_PAGE = "site/hbm-chain/index.html", "site/hbm-insight/index.html"
INPUT_GLOBS = build_page.INPUT_GLOBS
INPUT_FILES = (
    "docs/architecture/company-dataset.md",
    "docs/architecture/decisions.md",
    "docs/architecture/relationship-taxonomy.md",
    "docs/research/source-policy.md",
    "tools/build_journeys.py",
    "tools/build_page.py",
    "tools/facility_status.py",
    "tools/journey_template.html",
    "tools/navigate.py",
    "tools/page_template.html",
    "tools/policy_status.py",
    "tools/trace.py",
)
NO_ADVICE = "This page describes what the text says; it does not advise."
STATUS_WORDS = ("has taken effect", "no recorded effect", "published not yet in effect", "not yet published", "repealed", "proposed", "indeterminate")
# Rulings each page kind states as limitations (titles read from decisions.md).
RULINGS = {
    "index": ("D-123", "D-190", "D-193"),
    "export": ("D-156", "D-160", "D-161", "D-165", "D-166", "D-167", "D-169", "D-173", "D-175", "D-189", "D-191"),
    "company": ("D-109", "D-144", "D-147", "D-148", "D-190", "D-192"),
    "place": ("D-161", "D-190", "D-192"),
}

# Every fixed word the journeys add to the S11 page's labels (JR-1): none names a record or holds a digit.
LABELS = build_page.LABELS | frozenset(
    {
        "Research pages", "Compare layers", "Company profile", "Place profile", "All research pages", "The question",
        "What are you trying to understand?", "Questions", "Where the records stop", "Explore a dependency",
        "Investigate a company", "Investigate a place", "Inspect evidence", "the dependency journey", "the research view",
        "Which parts and technologies does each recorded export-control text name among the items it controls, and when did each take effect?",
        "What does the Atlas record about a company, and on what evidence?",
        "What does the Atlas record as incorporated, headquartered, located or issued in a place?",
        "How does the Atlas know a value, and how was it checked?",
        "Every value on every research page opens its evidence: the claim, the quoted source sentence, the source and its dates.",
        "Recorded classes with no dependency link", "no recorded relationship",
        # the export-control page
        "Which parts and technologies does each recorded export-control text name among the items it controls?",
        "Scope:", "acts recorded in the Atlas, issued in", "classes recorded (components and technologies), read as of",
        "What the records show", "Named in the texts", "of", "acts", "Indicators", "Links", "links from",
        "Refused candidates", "refused candidates", "candidates", "Status on", "On the dependency journey",
        "The matrix", "Act", "Class or product", "named in the text", "refused:", "The timeline", "The timeline in words",
        "no dated event recorded", "Acts with no dated event:", "published", "effective", "as of", "Statuses",
        "status on", "official citation", "form", "issued by", "issued in", "act", "class", "the official text",
        "quoted from the act’s text; matched to the record by the Atlas", "by", "see the card",
        "The pairs as a table", "State", "Reasons", "Record", "considered:", "no record in the Atlas",
        "the latest publication date of an act the Atlas holds:", "Method and limitations", "Built from", "Reproduce",
        "the policy links of one class:", "one act’s status:", "rebuild these pages:",
        "python tools/navigate.py edges", "python tools/policy_status.py", "--on", "python tools/build_journeys.py --check",
        "Rulings these pages depend on", "Evidence", "Acts", "Policy links", "Events", "Terms", "back to the top",
        "rows:", "columns:", "the text names the class among the items it controls",
        "the Atlas considered the pair and recorded why not", "no record either way",
        "dated event", "hollow: published", "filled: effective", "dashed line: the as-of date", "Timeline of the acts",
        # the company and place pages
        "What does the Atlas record about", ", and on what evidence?",
        "One company record, the links that name it, and the candidates the Atlas refused.",
        "recorded role", "legal name", "incorporated in", "headquartered in", "recorded links",
        "named as a supplier on", "vendor of", "products", "refused candidates name it", "recorded events",
        "no recorded event", "named as a supplier on no recorded link", "vendor of no recorded product",
        "no refused candidate names it", "Links and namings", "supplier (who makes this part)", "vendor",
        "historical, to", "reported", "stated", "inferred", "Kind", "What", "Basis or state", "link", "supplier naming",
        "product", "candidate", "event", "identity", "the evidence for one record:", "this record’s links:",
        "What does the Atlas record as incorporated, headquartered, located or issued in",
        "Every company, facility and act the Atlas records in one place.", "Incorporated here", "Headquartered here",
        "Located here", "Issued here", "incorporation:", "companies incorporated here", "companies headquartered here",
        "facilities located here", "acts issued here", "of them with incorporation not held by the Atlas",
        "no company recorded as incorporated here", "no company recorded as headquartered here",
        "no facility recorded as located here", "no act recorded as issued here", "operated by",
        "what each text names", "its evidence", "facility kind", "evidence", "company page",
        # the headings inside the template's framing blocks (the Editorial's)
        "How to read the matrix", "How to read the timeline", "What a status means", "What this page cannot answer",
        # the design pass (S20, D-198): cards, buttons, tiles, toggles
        "is", "Classes named", "classes recorded", "How to read the links", "the as-of date", "Open the dependency journey",
        "Open the research view", "Open the comparison", "Named as a supplier", "Products", "Events",
        "recorded link names it as supplier", "recorded links name it as supplier", "product it is the vendor of",
        "products it is the vendor of",
        "A chain diagram from the accelerator to its memory and the process that memory needs, with the evidence for every link.",
        "A matrix of the export-control texts the Atlas records against the parts and technologies they name, with a timeline of when each took effect.",
        "One page per company: its identity, its links, where a source names it as a supplier, and the candidates the Atlas refused.",
        "One page per place: the companies incorporated or headquartered there, the facilities located there and the acts issued there.",
        # singular forms: a count of one takes the singular (S20 browser QA)
        "link from", "refused candidate", "candidate", "recorded link", "product", "refused candidate names it",
        "recorded event", "company incorporated here", "company headquartered here", "facility located here",
        "act issued here", "of them with incorporation not held by the Atlas",
    }
    | set(STATUS_WORDS)
    | {NO_ADVICE}
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


def template_parts() -> tuple[str, dict[str, str]]:
    """The page skeleton, and the framing blocks after it by name (the Editorial's words, D-197)."""
    text = TEMPLATE.read_text(encoding="utf-8")
    skeleton, _, rest = text.partition("<!-- framing: ")
    blocks = {}
    for chunk in ("<!-- framing: " + rest).split("<!-- framing: ")[1:]:
        name, _, body = chunk.partition(" -->\n")
        if name.startswith("end framing"):
            continue
        blocks[name] = body.split("<!-- ")[0].strip("\n")
    return skeleton, blocks


def pages(data: Path = DATA) -> list[tuple[str, str, str | None]]:
    """(path, kind, subject) for every page the records call for."""
    out = [(INDEX, "index", None), (EXPORT, "export", None)]
    out += [(f"site/companies/{c['id']}/index.html", "company", c["id"]) for c in load_json(data / "companies.json")]
    out += [(f"site/places/{p['id']}/index.html", "place", p["id"]) for p in load_json(data / "jurisdictions.json")]
    return out


class Journey(build_page.Page):
    back = ("#top", "back to the top")

    def __init__(self, rel: str, kind: str, subject: str | None, data: Path = DATA) -> None:
        super().__init__(data)
        self.rel, self.kind, self.subject = rel, kind, subject
        self.to_root = "../" * rel.count("/")
        query = REPO_ROOT / "sql" / f"{AGE_QUERY}.sql"
        self.age = load_json(REPO_ROOT / "sql" / "results" / f"{AGE_QUERY}.json")
        if self.age["query_sha256"] != hashlib.sha256(query.read_bytes()).hexdigest():
            raise BuildError(f"sql/results/{AGE_QUERY}.json was computed from another version of its query (python tools/warehouse.py)")
        self.on = self.age["rows"][0]["reference_date"]
        self.atlas.on = self.on  # statuses are derived on the as-of date, never on the build's clock
        self.skeleton, self.framings = template_parts()
        recs = lambda kind: [r for r, where in self.atlas.records.values() if where == "canonical" and r.get("type") == kind]  # noqa: E731
        self.companies, self.places, self.policies = recs("company"), recs("jurisdiction"), recs("policy")
        self.products, self.facilities = recs("product"), recs("facility")
        self.classes = recs("component") + recs("technology")
        self.edges = [e for e, where in self.atlas.edges if where == "canonical"]
        self.events = [e for e in load_json(data / "events.json")]
        self.homes.update({e["id"]: e for e in self.events})
        self.links = [e for e in self.edges if e["relation_type"] == "restricts"]
        ids = {p["id"] for p in self.policies}
        self.policy_candidates = [c for c in self.candidates.values() if any(isinstance(s, str) and s in ids for s in c["source_entities"])]

    @staticmethod
    def label_text(text: str) -> str:
        if text not in LABELS:
            raise BuildError(f"not a label: {text!r}")
        return text

    # --- shared pieces ----------------------------------------------------------------------------

    def href(self, target: str, fragment: str | None = None) -> str:
        if not (REPO_ROOT / target).exists() and target not in {p for p, _, _ in pages()}:
            raise BuildError(f"a link to {target}, which does not exist")
        path = os.path.relpath(REPO_ROOT / target, (REPO_ROOT / self.rel).parent).replace(os.sep, "/")
        return esc(path + (f"#{fragment}" if fragment else ""))

    def framing(self, name: str) -> str:
        if name not in self.framings:
            raise BuildError(f"the template has no framing block {name!r}")
        return self.framings[name]

    def howto(self, name: str, title: str) -> str:
        """A framing block folded behind its question (S20 design pass): the explanation one click away."""
        return f'<details class="howto"><summary>{self.label(title)}</summary>{self.framing(name)}</details>'

    def tile(self, title: str, body: str) -> str:
        return f'<div class="tile">{self.label(title, tag="h3")}{body}</div>'

    def count(self, n: int, what: str, key: str | None = None, cls: str = "tally") -> str:
        extra = {"data_count": what} | ({"data_key": key} if key else {})
        return self.derived("count", str(n), cls=cls, **extra)

    def as_of(self, tag: str = "span") -> str:
        return self.sql_cell(0, "reference_date", self.on, tag=tag, query=AGE_QUERY)

    def section(self, sid: str, title: str, content: str) -> str:
        return f'<section id="{sid}" aria-labelledby="{sid}-h">{self.label(title, tag="h2", id=f"{sid}-h")}{content}</section>'

    def jump(self, items: list[tuple[str, str]]) -> str:
        links = "".join(f'<a href="#{sid}">{self.label(title)}</a>' for sid, title in items)
        return f'<nav class="jump" aria-label="Sections">{self.label("Jump to", cls="k")}{links}</nav>'

    def company_link(self, cid: str, field_ref: tuple[str, str] | None = None) -> str:
        ref, field = field_ref or (cid, "/name")
        return f'<a href="{self.href(f"site/companies/{cid}/index.html")}">{self.ref(ref, field)}</a>'

    def place_link(self, pid: str) -> str:
        return f'<a href="{self.href(f"site/places/{pid}/index.html")}">{self.name(pid)}</a>'

    def act_link(self, pid: str, field: str = "/official_citation/0/value") -> str:
        """A policy value, always linked to the act's own block on the page (JR-6)."""
        return f'<a href="#ev-{esc(pid)}">{self.ref(pid, field)}</a>'

    def ev(self, target: str, page: str | None = None) -> str:
        href = f"#ev-{esc(target)}" if page is None else self.href(page, f"ev-{target}")
        return f'<a class="ev-link" href="{href}">{self.label("evidence")}</a>'

    def official_sources(self, pid: str) -> list[str]:
        """The official texts the act's identity claims cite (LA-5), as source IDs."""
        found: list[str] = []
        for claim_id in self.homes[pid].get("identity_claim_ids", []):
            for citation in self.homes[claim_id].get("citations", []):
                source = self.store.sources[citation["source_id"]]
                if source["source_class"] == "official_legal_text" and citation["source_id"] not in found:
                    found.append(citation["source_id"])
        if not found:
            raise BuildError(f"{pid}: no official text to link (LA-5)")
        return found

    def act_block(self, pid: str) -> str:
        links = " · ".join(self.ref(s, "/url", tag="a", href=self.store.sources[s]["url"], cls="official", rel="noopener noreferrer") for s in self.official_sources(pid))
        return f'<div class="act-block"><p>{self.label("the official text", cls="k")} {links}</p>{self.label(NO_ADVICE, tag="p", cls="no-advice")}</div>'

    def status(self, pid: str) -> str:
        status, _ = self.atlas.policy_status(pid)
        return self.derived("policy-status", status.replace("_", " "), data_policy=pid, data_on=self.on)

    def endpoint(self, cand_id: str, pointer: str, value) -> str:
        if isinstance(value, str):
            if self.homes.get(value, {}).get("type") == "company":
                return self.company_link(value)
            if self.homes.get(value, {}).get("type") == "policy":
                return self.act_link(value)
            return self.name(value)
        return f'{self.ref(cand_id, f"{pointer}/name")} <span class="cite">({self.label("no record in the Atlas")})</span>'

    def reasons(self, cand: dict) -> str:
        return ", ".join(self.ref(f"schema:refused_candidates#vocab_reason/{r}", "/const", fmt="state") for r in cand["reasons"])

    def card(self, cand: dict) -> str:
        cid = cand["id"]
        sources = ", ".join(self.endpoint(cid, f"/source_entities/{i}", v) for i, v in enumerate(cand["source_entities"]))
        targets = ", ".join(self.endpoint(cid, f"/target_entities/{i}", v) for i, v in enumerate(cand["target_entities"]))
        types = ", ".join(self.ref(cid, f"/relation_types/{i}", cls="rel") for i in range(len(cand["relation_types"])))
        item = f' · {self.label("item")}: {self.endpoint(cid, "/item", cand["item"])}' if "item" in cand else ""
        considered = []
        for i, entry in enumerate(cand.get("considered", [])):
            if "claim_id" in entry:
                considered.append(f'<li>{self.label("claim", cls="k")} {self.ref(cid, f"/considered/{i}/claim_id", tag="code")}</li>')
                continue
            quote = f'<blockquote class="anchor">{self.ref(cid, f"/considered/{i}/anchor")}</blockquote>' if "anchor" in entry else ""
            locator = entry["locator"]
            where = self.ref(cid, f"/considered/{i}/locator/state", fmt="state") if isinstance(locator, dict) else self.ref(cid, f"/considered/{i}/locator")
            considered.append(f'<li>{quote}{self.label("source", cls="k")} {self.ref(entry["source_id"], "/title", tag="cite")} · {self.label("locator", cls="k")} {where}</li>')
        for relation in cand["relation_types"]:
            self.term("Relation types", f"schema:relationships#vocab_relation_type/{relation}")
        return (
            f'<li class="card" id="cand-{esc(cid)}" data-candidate="{esc(cid)}"><p class="card-head">{sources} → {targets} · {types}{item}</p>'
            f'<p>{self.label("refused:")} {self.reasons(cand)}</p><p>{self.ref(cid, "/reasoning")}</p>'
            f'<p class="cite">{self.label("ruling")}: {self.decision(cand["ruling"])}</p>'
            + (f'<div class="meta">{self.label("considered:")}<ul class="considered">{"".join(considered)}</ul></div>' if considered else "")
            + "</li>"
        )

    def method(self) -> str:
        paths = input_paths()
        files = "".join(f'<li><a href="{self.to_root}{esc(p)}">{self.derived("input-file", p, tag="code")}</a></li>' for p in paths)
        rulings = "".join(f"<li>{self.decision(key)}</li>" for key in RULINGS[self.kind])
        return (
            f'{self.framing("method")}'
            f'{self.label("Rulings these pages depend on", tag="h3")}<ul class="rulings">{rulings}</ul>'
            f'{self.label("Built from", tag="h3")}'
            f'<p>{self.label("input digest", cls="k")} {self.derived("input-digest", input_digest(paths), tag="code", cls="digest")}</p>'
            f'<details class="inputs"><summary>{self.label("input files")}</summary><ul class="files">{files}</ul></details>'
        )

    def reproduce(self, lines: list[tuple[str, str]]) -> str:
        body = "\n".join(f"{self.label(head)}\n{cmd}" for head, cmd in lines + [("rebuild these pages:", self.label("python tools/build_journeys.py --check"))])
        return f'{self.label("Reproduce", tag="h3")}<pre><code>{body}</code></pre>'

    def terms_section(self) -> str:
        terms = self.glossary()
        return self.section("terms", "Terms", terms) if terms else ""

    def table(self, heads: tuple[str, ...], rows: list[tuple[str, ...]]) -> str:
        k = {h: self.label(h, cls="cell-k") for h in heads}
        body = "".join("<tr>" + "".join(f"<td>{k[h]}{c}</td>" for h, c in zip(heads, row)) + "</tr>" for row in rows)
        head = "".join(f'<th scope="col">{self.label(h)}</th>' for h in heads)
        return f'<div class="table-wrap"><table class="sql"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

    # --- the entry page ------------------------------------------------------------------------------

    def render_index(self) -> dict:
        question = f'{self.label("What does an")} {self.name("component-ai-accelerator")}{self.label("’s memory depend on, and who is known to make it?")}'
        chips = lambda records, link: "".join(f"<li>{link(r['id'])}</li>" for r in sorted(records, key=lambda r: r["name"].lower()))  # noqa: E731
        button = lambda target, words: f'<a class="button" href="{self.href(target)}">{self.label(words)}</a>'  # noqa: E731
        cards = [
            ("Explore a dependency", question,
             "A chain diagram from the accelerator to its memory and the process that memory needs, with the evidence for every link.",
             button(CHAIN_PAGE, "Open the dependency journey") + button(INSIGHT_PAGE, "Open the research view")),
            ("Compare layers", self.label("Which parts and technologies does each recorded export-control text name among the items it controls, and when did each take effect?"),
             "A matrix of the export-control texts the Atlas records against the parts and technologies they name, with a timeline of when each took effect.",
             button(EXPORT, "Open the comparison")),
            ("Investigate a company", self.label("What does the Atlas record about a company, and on what evidence?"),
             "One page per company: its identity, its links, where a source names it as a supplier, and the candidates the Atlas refused.",
             f'<ul class="chips">{chips(self.companies, self.company_link)}</ul>'),
            ("Investigate a place", self.label("What does the Atlas record as incorporated, headquartered, located or issued in a place?"),
             "One page per place: the companies incorporated or headquartered there, the facilities located there and the acts issued there.",
             f'<ul class="chips">{chips(self.places, self.place_link)}</ul>'),
            ("Inspect evidence", self.label("How does the Atlas know a value, and how was it checked?"),
             "Every value on every research page opens its evidence: the claim, the quoted source sentence, the source and its dates.", ""),
        ]
        items = "".join(f'<li>{self.label(kick, cls="k")}<h3>{q}</h3>{self.label(what, tag="p", cls="what")}<div class="go">{go}</div></li>' for kick, q, what, go in cards)
        structural = ("requires", "has_part", "incorporates")
        touched = {x for e in self.edges if e["relation_type"] in structural for x in (e["source_entity"], e["target_entity"])}
        chainless = "".join(f'<li data-no-chain="{esc(c["id"])}"><span>{self.name(c["id"])}</span></li>' for c in self.classes if c["id"] not in touched)
        main = (
            self.section("questions", "Questions", f'<ul class="question-cards">{items}</ul>')
            + self.section("limits", "Where the records stop", f'{self.label("Recorded classes with no dependency link", tag="h3")}<ul class="chips quiet">{chainless}</ul>{self.framing("index-limits")}')
            + self.section("method", "Method and limitations", self.method() + self.reproduce([]))
        )
        return {
            "kicker": f'{self.label("AI Infrastructure Atlas")}{self.label("Research pages")}',
            "crumbs": "",
            "question_line": "",
            "h1": self.label("What are you trying to understand?"),
            "scope": "",
            "framing_top": self.framing("index-top"),
            "jump": "",
            "main": main,
        }

    # --- the export-control page (D-191) -------------------------------------------------------------

    def acts_in_order(self) -> list[dict]:
        def first(p: dict):
            dates = [period(e["date"])[0] for e in self.events if e["subject"] == p["id"]]
            return (0, min(dates)) if dates else (1, "")
        return sorted(self.policies, key=lambda p: (first(p), p["id"]))

    def targets(self) -> list[str]:
        found: list[str] = []
        for t in [e["target_entity"] for e in self.links] + [t for c in self.policy_candidates for t in c["target_entities"]]:
            if t not in found:
                found.append(t)
        return found

    def cell_state(self, act: str, target: str) -> tuple[str, dict | None]:
        link = next((e for e in self.links if e["source_entity"] == act and e["target_entity"] == target), None)
        if link:
            return "named", link
        cand = next((c for c in self.policy_candidates if act in c["source_entities"] and target in c["target_entities"]), None)
        return ("refused", cand) if cand else ("none", None)

    def matrix(self, acts: list[dict]) -> str:
        head = "".join(
            f'<th scope="col">{self.act_link(a["id"])}<span class="meta">{self.status(a["id"])}</span></th>' for a in acts
        )
        rows = []
        for target in self.targets():
            cells = []
            for a in acts:
                state, record = self.cell_state(a["id"], target)
                k = f'<span class="cell-k">{self.act_link(a["id"])}</span>'
                if state == "named":
                    body = f'<a class="cell-named" href="#ev-{esc(record["id"])}">{self.label("named in the text")}</a>'
                    attrs = f' data-link="{esc(record["id"])}"'
                elif state == "refused":
                    body = f'<a class="cell-refused" href="#cand-{esc(record["id"])}">{self.label("refused:")} {self.reasons(record)}</a>'
                    attrs = f' data-candidate="{esc(record["id"])}"'
                else:
                    body, attrs = f'<span class="cell-none">{self.label("no recorded relationship")}</span>', ""
                cells.append(f'<td data-act="{esc(a["id"])}" data-cell="{state}"{attrs}>{k}{body}</td>')
            rows.append(f'<tr data-target="{esc(target)}"><th scope="row">{self.name(target)} <span class="meta">{self.ref(target, "/type")}</span></th>{"".join(cells)}</tr>')
        corner = f'<th scope="col">{self.label("Class or product")}</th>'
        key = (
            f'<ul class="key"><li>{self.label("named in the text", cls="cell-named")}: {self.label("the text names the class among the items it controls")}</li>'
            f'<li>{self.label("refused:", cls="cell-refused")} {self.label("the Atlas considered the pair and recorded why not")}</li>'
            f'<li>{self.label("no recorded relationship", cls="cell-none")}: {self.label("no record either way")}</li></ul>'
        )
        return f'{key}<div class="table-wrap"><table class="matrix"><thead><tr>{corner}{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

    def timeline(self, acts: list[dict]) -> str:
        """One lane per act with a dated event; each event a dot at its date on one linear scale (a partial date as a bar
        over its period). Dots closer than one dot's width are stacked downwards in their lane (a beeswarm), so that no
        event hides another: x is the date, y carries nothing but the stacking."""
        dated = [a for a in acts if any(e["subject"] == a["id"] for e in self.events)]
        events = sorted((e for e in self.events if e["subject"] in {a["id"] for a in dated}), key=lambda e: (period(e["date"])[0], e["id"]))
        start = f"{min(period(e['date'])[0] for e in events)[:4]}-01-01"
        end = f"{max([period(e['date'])[1] for e in events] + [self.on])[:4]}-12-31"
        x0, x1, top, step, pad = 150.0, 985.0, 34, 18, 16
        d0, d1 = datetime.date.fromisoformat(start).toordinal(), datetime.date.fromisoformat(end).toordinal()
        x = lambda d: x0 + (datetime.date.fromisoformat(d).toordinal() - d0) * (x1 - x0) / (d1 - d0)  # noqa: E731
        lanes, y = [], top
        for a in dated:
            placed: list[tuple[float, int]] = []
            marks = []
            for e in (e for e in events if e["subject"] == a["id"]):
                cx = x(period(e["date"])[0])
                row = 0
                while any(abs(cx - px) < 15 and pr == row for px, pr in placed):
                    row += 1
                placed.append((cx, row))
                marks.append((e, row))
            rows = max(r for _, r in marks) + 1
            height = pad * 2 + (rows - 1) * step
            lanes.append((a, marks, y, height))
            y += height
        bottom = y
        out = []
        years = range(int(start[:4]), int(end[:4]) + 1)
        for year in years:
            xa, xb = x(f"{year}-01-01"), x(f"{year}-12-31")
            if year % 2:
                out.append(f'<rect class="band" x="{xa:.2f}" y="{top}" width="{xb - xa:.2f}" height="{bottom - top}"/>')
            out.append(self.derived("year", str(year), tag="text", cls="year", x=f"{xa + 6:.2f}", y=str(top - 10)))
        out.append(f'<line class="axis" x1="{x0:.2f}" y1="{top}" x2="{x1:.2f}" y2="{top}"/>')
        for a, marks, ly, height in lanes:
            out.append(f'<line class="lane" x1="{x0:.2f}" y1="{ly + height}" x2="{x1:.2f}" y2="{ly + height}"/>')
            out.append(f'<a href="#ev-{esc(a["id"])}">{self.ref(a["id"], "/official_citation/0/value", tag="text", cls="lane-name", x="4", y=str(ly + pad + 4))}</a>')
            for e, row in marks:
                first, last = period(e["date"])
                cy = ly + pad + row * step
                cls = {"published": "ev-published", "effective": "ev-effective"}.get(e["event_type"], "ev-other")
                if first == last:
                    shape = f'<circle class="{cls}" cx="{x(first):.2f}" cy="{cy}" r="6.5"/>'
                else:
                    w = x(last) - x(first) + (x1 - x0) / (d1 - d0)
                    shape = f'<rect class="{cls}" x="{x(first):.2f}" y="{cy - 6}" width="{w:.2f}" height="12" rx="3"/>'
                out.append(f'<a class="tl-mark" href="#ev-{esc(e["id"])}" data-event="{esc(e["id"])}" aria-labelledby="tw-{esc(e["id"])}">{shape}</a>')
        xa = x(self.on)
        out.append(f'<line class="asof" data-asof x1="{xa:.2f}" y1="{top - 4}" x2="{xa:.2f}" y2="{bottom + 6}"/>')
        out.append(f'<text class="asof-text" x="{xa - 6:.2f}" y="{bottom + 22}" text-anchor="end">{self.label("as of", tag="tspan")} {self.as_of(tag="tspan")}</text>')
        height = bottom + 30
        title = self.label("Timeline of the acts", tag="title", id="tl-title")
        svg = (
            f'<svg class="timeline" viewBox="0 0 1000 {height}" role="group" aria-labelledby="tl-title" aria-describedby="tl-words" '
            f'data-from="{start}" data-to="{end}" data-x0="{x0:.2f}" data-x1="{x1:.2f}">{title}{"".join(out)}</svg>'
        )
        words = "".join(
            f'<li id="tw-{esc(e["id"])}" data-event-word="{esc(e["id"])}">{self.ref(e["id"], "/date")} · {self.act_link(e["subject"])} · '
            f'{self.ref(e["id"], "/event_type", fmt="state")} {self.ev(e["id"])}</li>'
            for e in events
        )
        undated = "".join(f'<li data-undated="{esc(a["id"])}">{self.act_link(a["id"], "/name")} · {self.label("no dated event recorded", cls="none-word")}</li>' for a in acts if a not in dated)
        key = (
            f'<ul class="key"><li><span class="key-dot" aria-hidden="true"></span>{self.label("published")}</li>'
            f'<li><span class="key-dot filled" aria-hidden="true"></span>{self.label("effective")}</li>'
            f'<li><span class="key-line" aria-hidden="true"></span>{self.label("the as-of date")}</li></ul>'
        )
        return (
            f'{key}<figure class="timeline-fig">{svg}</figure>'
            + (f'<p>{self.label("Acts with no dated event:", cls="k")}</p><ul class="name-list">{undated}</ul>' if undated else "")
            + f'<details class="howto"><summary>{self.label("The timeline in words")}</summary><ol class="timeline-words" id="tl-words">{words}</ol></details>'
        )

    def chain_classes(self) -> list[str]:
        root = build_page.JOURNEY["walk_root"]
        chain = ["component-ai-accelerator"]
        for e in self.edges:
            if e["relation_type"] == "requires" and e["target_entity"] == root:
                chain += [e["source_entity"], e["target_entity"]]
        return chain

    def layers(self) -> str:
        inverse = ("schema:relationships#vocab_relation_type/restricts", "/x-inverse-reading")
        items = []
        for target in self.chain_classes():
            links = [e for e in self.links if e["target_entity"] == target]
            cands = [c for c in self.policy_candidates if target in c["target_entities"]]
            if links:
                state = "named"
                body = f'{self.ref(*inverse)} ' + ", ".join(self.act_link(e["source_entity"]) for e in links) + " " + " ".join(self.ev(e["id"]) for e in links)
            elif cands:
                state = "refused"
                body = "; ".join(
                    f'{self.label("refused:")} {self.reasons(c)} {self.label("by")} ' + ", ".join(self.act_link(s) for s in c["source_entities"] if isinstance(s, str))
                    + f' <a href="#cand-{esc(c["id"])}">{self.label("see the card")}</a>'
                    for c in cands
                )
            else:
                state, body = "none", self.label("no recorded relationship", cls="none-word")
            items.append(f'<li data-chain-class="{esc(target)}" data-state="{state}"><span>{self.name(target)}</span> · {body}</li>')
        return (
            f'{self.framing("export-layers")}<ul class="layers">{"".join(items)}</ul>'
            f'<p><a href="{self.href(CHAIN_PAGE)}">{self.label("the dependency journey")}</a></p>'
        )

    def link_panel(self, edge: dict) -> str:
        eid, act, target = edge["id"], edge["source_entity"], edge["target_entity"]
        heading = f'{self.name(target)} {self.ref("schema:relationships#vocab_relation_type/restricts", "/x-inverse-reading", cls="rel")} {self.ref(act, "/name")}'
        heading = heading.replace(self.ref(act, "/name"), f'<a href="#ev-{esc(act)}">{self.ref(act, "/name")}</a>', 1)
        details = [
            ("ID", self.ref(eid, "/id", tag="code")),
            ("level", self.ref("schema:relationships#vocab_relation_type/restricts", "/x-level")),
            ("basis", self.label("quoted from the act’s text; matched to the record by the Atlas")),
        ]
        self.term("Relation types", "schema:relationships#vocab_relation_type/restricts")
        return self.panel(eid, heading, details)

    def act_panel(self, policy: dict) -> str:
        pid = policy["id"]
        form = policy["instrument_form"]
        details = [
            ("ID", self.ref(pid, "/id", tag="code")),
            ("official citation", self.ref(pid, "/official_citation/0/value")),
            ("form", self.ref(pid, "/instrument_form/0/value", fmt="state") if isinstance(form, list) else self.ref(pid, "/instrument_form/state", fmt="state")),
            ("issued by", self.ref(pid, "/issuing_authority/0/value")),
            ("issued in", ", ".join(self.place_link(a["value"]) for a in policy["issued_in"])),
            ("status on", f"{self.as_of()}: {self.status(pid)}"),
        ]
        out = self.panel(pid, self.ref(pid, "/name"), details, intro=self.act_block(pid))
        return out.replace(f'<article class="panel" id="ev-{esc(pid)}">', f'<article class="panel" id="ev-{esc(pid)}" data-act="{esc(pid)}">', 1)

    def event_panel(self, event: dict) -> str:
        eid = event["id"]
        subject = event["subject"]
        about = self.act_link(subject, "/name") if self.homes[subject].get("type") == "policy" else self.name(subject)
        heading = f'{self.ref(eid, "/event_type", fmt="state")} · {self.ref(eid, "/date")}'
        return self.panel(eid, heading, [("ID", self.ref(eid, "/id", tag="code")), ("name", about)])

    def render_export(self) -> dict:
        acts = self.acts_in_order()
        n_acts = len(self.policies)
        issued = []
        for p in self.policies:
            for a in p["issued_in"]:
                if a["value"] not in issued:
                    issued.append(a["value"])
        scope = (
            f'<p class="scope">{self.label("Scope:", cls="k")} {self.count(n_acts, "acts", cls="")} '
            f'{self.label("acts recorded in the Atlas, issued in")} {", ".join(self.place_link(j) for j in issued)}; '
            f'{self.count(len(self.classes), "classes", cls="")} {self.label("classes recorded (components and technologies), read as of")} {self.as_of()}.</p>'
        )
        named = []
        for target in self.targets():
            links = [e for e in self.links if e["target_entity"] == target]
            if links:
                named.append(
                    f'<li>{self.name(target)} {self.label("is")} {self.ref("schema:relationships#vocab_relation_type/restricts", "/x-inverse-reading")} '
                    f'{self.count(len(links), "named-by", target)} {self.label("of")} {self.count(n_acts, "acts")} {self.label("acts")}: '
                    + ", ".join(self.act_link(e["source_entity"]) for e in links) + "</li>"
                )
        statuses: dict[str, int] = {}
        for p in self.policies:
            s, _ = self.atlas.policy_status(p["id"])
            statuses[s] = statuses.get(s, 0) + 1
        reasons: dict[str, int] = {}
        for c in self.policy_candidates:
            for r in c["reasons"]:
                reasons[r] = reasons.get(r, 0) + 1
        n_named = len({e["target_entity"] for e in self.links})
        n_acts_linking = len({e["source_entity"] for e in self.links})
        tiles = (
            '<div class="tiles">'
            + self.tile("Classes named", f'<p class="stat">{self.count(n_named, "named-classes")} {self.label("of")} {self.count(len(self.classes), "classes", cls="tally-s")} {self.label("classes recorded")}</p>')
            + self.tile("Links", f'<p class="stat">{self.count(len(self.links), "links")} {self.unit(len(self.links), "link from", "links from")} '
                        f'{self.count(n_acts_linking, "link-acts", cls="tally-s")} {self.label("of")} {self.count(n_acts, "acts", cls="tally-s")} {self.label("acts")}</p>')
            + self.tile("Refused candidates", f'<p class="stat">{self.count(len(self.policy_candidates), "candidates")} {self.unit(len(self.policy_candidates), "refused candidate", "refused candidates")}</p><ul>'
                        + "".join(f'<li>{self.ref(f"schema:refused_candidates#vocab_reason/{r}", "/const", fmt="state")}: {self.count(n, "candidates-reason", r, cls="tally-s")} {self.unit(n, "candidate", "candidates")}</li>' for r, n in sorted(reasons.items()))
                        + "</ul>")
            + self.tile("Status on", f'<p class="stat">{self.as_of()}</p><ul>'
                        + "".join(f'<li>{self.label(s.replace("_", " "))}: {self.count(n, "status", s, cls="tally-s")} {self.label("of")} {self.count(n_acts, "acts", cls="tally-s")} {self.label("acts")}</li>' for s, n in sorted(statuses.items()))
                        + "</ul>")
            + "</div>"
        )
        statuses_list = "".join(f'<li>{self.act_link(a["id"])} · {self.label("status on")} {self.as_of()}: {self.status(a["id"])}</li>' for a in acts)
        latest = max(e["date"] for e in self.events if e["event_type"] == "published" and e["subject"] in {p["id"] for p in self.policies})
        table_rows = []
        for target in self.targets():
            for a in acts:
                state, record = self.cell_state(a["id"], target)
                if state == "none":
                    continue
                table_rows.append((
                    self.act_link(a["id"]), self.name(target),
                    self.label("named in the text" if state == "named" else "refused:"),
                    self.reasons(record) if state == "refused" else "",
                    f'<code>{self.ref(record["id"], "/id")}</code>' if state == "named" else f'<a href="#cand-{esc(record["id"])}"><code>{self.ref(record["id"], "/id")}</code></a>',
                ))
        evidence = (
            self.label("Acts", tag="h3") + "".join(self.act_panel(a) for a in acts)
            + self.label("Policy links", tag="h3") + "".join(self.link_panel(e) for e in self.links)
            + self.label("Refused candidates", tag="h3") + f'<ul class="cards refusals">{"".join(self.card(c) for c in self.policy_candidates)}</ul>'
            + self.label("Events", tag="h3") + "".join(self.event_panel(e) for e in sorted(self.events, key=lambda e: (e["date"], e["id"])) if e["subject"] in {p["id"] for p in self.policies})
        )
        hbm = "component-high-bandwidth-memory"
        method = (
            self.label("What this page cannot answer", tag="h3") + self.framing("export-limits")
            + f'<p>{self.label("the latest publication date of an act the Atlas holds:")} {self.derived("latest-published", latest)}</p>'
            + self.method()
            + self.reproduce([
                ("the policy links of one class:", f'{self.label("python tools/navigate.py edges")} {self.ref(hbm, "/id")} {self.label("--on")} {self.as_of()}'),
                ("one act’s status:", f'{self.label("python tools/policy_status.py")} {self.act_link(acts[0]["id"], "/id")} {self.label("--on")} {self.as_of()}'),
            ])
        )
        main = (
            self.section("answer", "What the records show", f'{tiles}<ul class="findings">{"".join(named)}</ul>')
            + self.section("layers", "On the dependency journey", self.layers())
            + self.section("matrix", "The matrix", self.howto("export-matrix", "How to read the matrix") + self.matrix(acts))
            + self.section("timeline", "The timeline", self.howto("export-timeline", "How to read the timeline") + self.timeline(acts))
            + self.section("statuses", "Statuses", self.howto("export-status", "What a status means") + f'<ul class="items">{statuses_list}</ul>')
            + self.section("evidence", "Evidence", evidence)
            + self.section("data", "The pairs as a table", self.table(("Act", "Class or product", "State", "Reasons", "Record"), table_rows))
            + self.section("method", "Method and limitations", method)
        )
        main += self.terms_section()
        return {
            "kicker": f'{self.label("AI Infrastructure Atlas")}{self.label("Compare layers")}',
            "crumbs": f'<p class="crumbs"><a href="{self.href(INDEX)}">{self.label("All research pages")}</a></p>',
            "question_line": "",
            "h1": self.label("Which parts and technologies does each recorded export-control text name among the items it controls?"),
            "scope": scope,
            "framing_top": self.framing("export-top"),
            "jump": self.jump([("answer", "What the records show"), ("matrix", "The matrix"), ("timeline", "The timeline"), ("evidence", "Evidence"), ("data", "The pairs as a table"), ("method", "Method and limitations")]),
            "main": main,
        }

    # --- a company (D-192) -----------------------------------------------------------------------------

    def values(self, rid: str, field: str, link=None, fmt: str | None = None) -> str:
        """A record's multi-valued field in words, or its state when unknown."""
        value = self.homes[rid].get(field)
        if value is None:
            return self.absent(rid, f"/{field}", "no record in the Atlas")
        if isinstance(value, dict):
            return self.ref(rid, f"/{field}/state", fmt="state", cls="state-word")
        return ", ".join(link(a["value"]) if link else self.ref(rid, f"/{field}/{i}/value", fmt=fmt) for i, a in enumerate(value))

    def unit(self, n: int, one: str, many: str) -> str:
        return self.label(one if n == 1 else many)

    def tally(self, n: int, what: str, words: tuple[str, str], none: str, title: str) -> str:
        if n:
            return self.tile(title, f'<p class="stat">{self.count(n, what)} {self.unit(n, *words)}</p>')
        return self.tile(title, f'<p class="stat">{self.label(none, cls="none-word")}</p>')

    def render_company(self) -> dict:
        cid = self.subject
        record = self.homes[cid]
        own = [e for e in self.edges if cid in (e["source_entity"], e["target_entity"])]
        named = [e for e in self.edges if isinstance(e.get("supplier"), list) and any(a["value"] == cid for a in e["supplier"])]
        products = [p for p in self.products if p.get("vendor") == cid]
        cands = [c for c in self.candidates.values() if cid in [x for x in c["source_entities"] + c["target_entities"] if isinstance(x, str)] or c.get("item") == cid]
        events = sorted((e for e in self.events if e["subject"] == cid), key=lambda e: (e["date"], e["id"]))
        roles = record.get("roles")
        role_words = (
            ", ".join(f'{self.ref(cid, f"/roles/{i}/value", fmt="state")} <span class="cite">({self.ref("schema:entities#vocab_actor_role/" + a["value"], "/description")})</span>' for i, a in enumerate(roles))
            if isinstance(roles, list) else self.ref(cid, "/roles/state", fmt="state", cls="state-word")
        )
        facts = (
            f'<div class="summary-card"><dl><div><dt>{self.label("recorded role")}</dt><dd>{role_words}</dd></div>'
            f'<div><dt>{self.label("legal name")}</dt><dd>{self.values(cid, "legal_name")}</dd></div>'
            f'<div><dt>{self.label("incorporated in")}</dt><dd>{self.values(cid, "incorporated_in", self.place_link)}</dd></div>'
            f'<div><dt>{self.label("headquartered in")}</dt><dd>{self.values(cid, "headquartered_in", self.place_link)}</dd></div></dl></div>'
        )
        tallies = (
            '<div class="tiles">'
            + self.tally(len(own), "links", ("recorded link", "recorded links"), "no recorded relationship", "Links")
            + self.tally(len(named), "supplier", ("recorded link names it as supplier", "recorded links name it as supplier"), "named as a supplier on no recorded link", "Named as a supplier")
            + self.tally(len(products), "products", ("product it is the vendor of", "products it is the vendor of"), "vendor of no recorded product", "Products")
            + self.tally(len(cands), "candidates", ("refused candidate names it", "refused candidates name it"), "no refused candidate names it", "Refused candidates")
            + self.tally(len(events), "events", ("recorded event", "recorded events"), "no recorded event", "Events")
            + "</div>"
        )
        items = []
        for e in own:
            entry = self.atlas.entry(e, "canonical")
            basis = self.basis(entry)
            ends = [self.company_link(x) if self.homes[x].get("type") == "company" else self.name(x) for x in (e["source_entity"], e["target_entity"])]
            items.append(f'<li data-link="{esc(e["id"])}">{ends[0]} {self.ref(e["id"], "/relation_type", cls="rel")} {ends[1]} · {self.label(basis, cls="basis " + basis)} {self.ev(e["id"])}</li>')
            self.term("Relation types", f"schema:relationships#vocab_relation_type/{e['relation_type']}")
        for e in named:
            i = next(k for k, a in enumerate(e["supplier"]) if a["value"] == cid)
            basis = self.assertion_basis(e["supplier"][i])
            period_words = f' · {self.label("historical, to")} {self.ref(e["id"], f"/supplier/{i}/valid_to")}' if "valid_to" in e["supplier"][i] else ""
            items.append(
                f'<li data-supplier="{esc(e["id"])}">{self.name(e["source_entity"])} {self.ref(e["id"], "/relation_type", cls="rel")} {self.name(e["target_entity"])} · '
                f'{self.label("supplier (who makes this part)")}: {self.name(cid)} · {self.label(basis, cls="basis " + basis)}{period_words} {self.ev(e["id"])}</li>'
            )
        for p in products:
            items.append(f'<li data-product="{esc(p["id"])}">{self.name(p["id"])} · {self.label("vendor")}: {self.name(cid)} {self.ev(p["id"])}</li>')
        links = f'<ul class="items">{"".join(items)}</ul>' if items else f'<p>{self.label("no recorded relationship", cls="none-word")}</p>'
        cards = f'<ul class="cards refusals">{"".join(self.card(c) for c in cands)}</ul>' if cands else f'<p>{self.label("no refused candidate names it", cls="none-word")}</p>'
        ev_items = "".join(f'<li data-event="{esc(e["id"])}">{self.ref(e["id"], "/date")} · {self.ref(e["id"], "/event_type", fmt="state")} {self.ev(e["id"])}</li>' for e in events)
        events_html = f'<ul class="items">{ev_items}</ul>' if events else f'<p>{self.label("no recorded event", cls="none-word")}</p>'
        panels = [self.node_panel(cid)]
        for e in own + [e for e in named if e not in own]:
            panels.append(self.edge_panel(self.atlas.entry(e, "canonical")))
        panels += [self.node_panel(p["id"]) for p in products]
        panels += [self.event_panel(e) for e in events]
        rows = [(self.label("identity"), self.name(cid), "", f'<code>{self.ref(cid, "/id")}</code>')]
        rows += [(self.label("link"), f'{self.name(e["source_entity"])} {self.ref(e["id"], "/relation_type", cls="rel")} {self.name(e["target_entity"])}', self.label(self.basis(self.atlas.entry(e, "canonical"))), f'<code>{self.ref(e["id"], "/id")}</code>') for e in own]
        rows += [(self.label("supplier naming"), f'{self.name(e["source_entity"])} · {self.name(e["target_entity"])}', self.label(self.assertion_basis(next(a for a in e["supplier"] if a["value"] == cid))), f'<code>{self.ref(e["id"], "/id")}</code>') for e in named]
        rows += [(self.label("product"), self.name(p["id"]), "", f'<code>{self.ref(p["id"], "/id")}</code>') for p in products]
        rows += [(self.label("candidate"), ", ".join(self.ref(c["id"], f"/relation_types/{i}") for i in range(len(c["relation_types"]))), self.reasons(c), f'<code>{self.ref(c["id"], "/id")}</code>') for c in cands]
        rows += [(self.label("event"), self.ref(e["id"], "/event_type", fmt="state"), self.ref(e["id"], "/date"), f'<code>{self.ref(e["id"], "/id")}</code>') for e in events]
        main = (
            self.section("answer", "What the records show", facts + tallies)
            + self.section("links", "Links and namings", self.howto("company-links", "How to read the links") + links)
            + self.section("candidates", "Refused candidates", cards)
            + self.section("events", "Events", events_html)
            + self.section("evidence", "Evidence", "".join(panels))
            + self.section("data", "The pairs as a table", self.table(("Kind", "What", "Basis or state", "Record"), rows))
            + self.section("method", "Method and limitations", self.label("What this page cannot answer", tag="h3") + self.framing("company-limits") + self.method() + self.reproduce([
                ("this record’s links:", f'{self.label("python tools/navigate.py edges")} {self.ref(cid, "/id")}'),
                ("the evidence for one record:", f'{self.label("python tools/trace.py")} {self.ref(cid, "/id")}'),
            ]))
        )
        main += self.terms_section()
        return {
            "kicker": f'{self.label("AI Infrastructure Atlas")}{self.label("Company profile")}',
            "crumbs": f'<p class="crumbs"><a href="{self.href(INDEX)}">{self.label("All research pages")}</a></p>',
            "question_line": "",
            "h1": f'{self.label("What does the Atlas record about")} {self.name(cid)}{self.label(", and on what evidence?")}',
            "scope": f'<p class="scope">{self.label("One company record, the links that name it, and the candidates the Atlas refused.")}</p>',
            "framing_top": self.framing("company-top"),
            "jump": self.jump([("answer", "What the records show"), ("links", "Links and namings"), ("candidates", "Refused candidates"), ("evidence", "Evidence"), ("method", "Method and limitations")]),
            "main": main,
        }

    # --- a place (D-192) -------------------------------------------------------------------------------

    def render_place(self) -> dict:
        pid = self.subject
        held = lambda record, field: isinstance(record.get(field), list) and any(a["value"] == pid for a in record[field])  # noqa: E731
        inc = [c for c in self.companies if held(c, "incorporated_in")]
        hq = [c for c in self.companies if held(c, "headquartered_in")]
        located = [f for f in self.facilities if held(f, "located_in")]
        issued = [p for p in self.policies if held(p, "issued_in")]
        unknown = [c for c in hq if not isinstance(c["incorporated_in"], list)]
        hq_body = (
            f'<p class="stat">{self.count(len(hq), "headquartered")} {self.unit(len(hq), "company headquartered here", "companies headquartered here")}</p>'
            + (f'<p class="stat">{self.count(len(unknown), "incorporation-unknown", cls="tally-s")} {self.label("of them with incorporation not held by the Atlas")}</p>' if unknown else "")
            if hq else f'<p class="stat">{self.label("no company recorded as headquartered here", cls="none-word")}</p>'
        )
        tallies = (
            '<div class="tiles">'
            + self.tally(len(inc), "incorporated", ("company incorporated here", "companies incorporated here"), "no company recorded as incorporated here", "Incorporated here")
            + self.tile("Headquartered here", hq_body)
            + self.tally(len(located), "located", ("facility located here", "facilities located here"), "no facility recorded as located here", "Located here")
            + self.tally(len(issued), "issued", ("act issued here", "acts issued here"), "no act recorded as issued here", "Issued here")
            + "</div>"
        )

        def company_item(c: dict, attr: str) -> str:
            note = ""
            if attr == "headquartered" and not isinstance(c["incorporated_in"], list):
                note = f' · {self.label("incorporation:")} {self.ref(c["id"], "/incorporated_in/state", fmt="state", cls="state-word")}'
            page = "site/companies/" + c["id"] + "/index.html"
            return f'<li data-{attr}="{esc(c["id"])}">{self.company_link(c["id"])}{note} {self.ev(c["id"], page)}</li>'

        def facility_item(f: dict) -> str:
            ops = [e for e in self.edges if e["relation_type"] == "operates" and e["target_entity"] == f["id"]]
            by = f' · {self.label("operated by")} ' + ", ".join(self.company_link(e["source_entity"]) for e in ops) if ops else ""
            kinds = f' · {self.label("facility kind", cls="k")} ' + ", ".join(self.ref(f["id"], f"/facility_kinds/{i}", fmt="state") for i in range(len(f.get("facility_kinds", []))))
            return f'<li data-located="{esc(f["id"])}">{self.name(f["id"])}{kinds}{by} {self.ev(f["id"])}</li>'

        def act_item(p: dict) -> str:
            return (
                f'<li id="act-{esc(p["id"])}" data-issued="{esc(p["id"])}" data-act="{esc(p["id"])}">{self.ref(p["id"], "/name")} · {self.ref(p["id"], "/official_citation/0/value")} '
                f'{self.act_block(p["id"])}<a href="{self.href(EXPORT, "ev-" + p["id"])}">{self.label("what each text names")}</a></li>'
            )

        lists = (
            self.label("Incorporated here", tag="h3") + (f'<ul class="items">{"".join(company_item(c, "incorporated") for c in inc)}</ul>' if inc else f'<p>{self.label("no company recorded as incorporated here", cls="none-word")}</p>')
            + self.label("Headquartered here", tag="h3") + (f'<ul class="items">{"".join(company_item(c, "headquartered") for c in hq)}</ul>' if hq else f'<p>{self.label("no company recorded as headquartered here", cls="none-word")}</p>')
            + self.label("Located here", tag="h3") + (f'<ul class="items">{"".join(facility_item(f) for f in located)}</ul>' if located else f'<p>{self.label("no facility recorded as located here", cls="none-word")}</p>')
            + self.label("Issued here", tag="h3") + (f'<ul class="items">{"".join(act_item(p) for p in issued)}</ul>' if issued else f'<p>{self.label("no act recorded as issued here", cls="none-word")}</p>')
        )
        panels = [self.node_panel(pid)] + [self.node_panel(f["id"]) for f in located]
        rows = [(self.label("identity"), self.name(pid), "", f'<code>{self.ref(pid, "/id")}</code>')]
        rows += [(self.label("incorporated in"), self.name(c["id"]), "", f'<code>{self.ref(c["id"], "/id")}</code>') for c in inc]
        rows += [(self.label("headquartered in"), self.name(c["id"]), self.ref(c["id"], "/incorporated_in/state", fmt="state") if not isinstance(c["incorporated_in"], list) else "", f'<code>{self.ref(c["id"], "/id")}</code>') for c in hq]
        rows += [(self.label("Located here"), self.name(f["id"]), "", f'<code>{self.ref(f["id"], "/id")}</code>') for f in located]
        # a policy value in the table links back to its act's block above (JR-6)
        to_act = lambda p, field: f'<a href="#act-{esc(p["id"])}">{self.ref(p["id"], field)}</a>'  # noqa: E731
        rows += [(self.label("issued in"), to_act(p, "/official_citation/0/value"), "", f'<code>{to_act(p, "/id")}</code>') for p in issued]
        main = (
            self.section("answer", "What the records show", tallies + lists)
            + self.section("evidence", "Evidence", "".join(panels))
            + self.section("data", "The pairs as a table", self.table(("Kind", "What", "Basis or state", "Record"), rows))
            + self.section("method", "Method and limitations", self.label("What this page cannot answer", tag="h3") + self.framing("place-limits") + self.method() + self.reproduce([
                ("the evidence for one record:", f'{self.label("python tools/trace.py")} {self.ref(pid, "/id")}'),
            ]))
        )
        main += self.terms_section()
        return {
            "kicker": f'{self.label("AI Infrastructure Atlas")}{self.label("Place profile")}',
            "crumbs": f'<p class="crumbs"><a href="{self.href(INDEX)}">{self.label("All research pages")}</a></p>',
            "question_line": "",
            "h1": f'{self.label("What does the Atlas record as incorporated, headquartered, located or issued in")} {self.name(pid)}?',
            "scope": f'<p class="scope">{self.label("Every company, facility and act the Atlas records in one place.")}</p>',
            "framing_top": self.framing("place-top"),
            "jump": self.jump([("answer", "What the records show"), ("evidence", "Evidence"), ("method", "Method and limitations")]),
            "main": main,
        }

    # --- the page ------------------------------------------------------------------------------------

    def base_style(self) -> str:
        template = build_page.TEMPLATE.read_text(encoding="utf-8")
        style = re.search(r"<style>\n(.*?)</style>", template, re.S)
        if not style:
            raise BuildError("the S11 template has no style block to reuse")
        return style.group(1).replace("${palette}", " ".join(f"--{k}: {v};" for k, v in PALETTE.items()))

    def render(self) -> str:
        parts = getattr(self, f"render_{self.kind}")()
        attrs = f'data-page-kind="{self.kind}"' + (f' data-subject="{esc(self.subject)}"' if self.subject else "")
        parts |= {"base_style": self.base_style(), "body_attrs": attrs, "title": esc(html.unescape(re.sub(r"<[^>]+>", "", parts["h1"])))}
        return string.Template(self.skeleton).substitute(parts)


def build(data: Path = DATA) -> dict[str, bytes]:
    return {rel: Journey(rel, kind, subject, data).render().encode("utf-8") for rel, kind, subject in pages(data)}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the S20 research journeys from the Atlas's records.")
    parser.add_argument("--check", action="store_true", help="rebuild in memory and compare with the committed pages")
    args = parser.parse_args(argv[1:])
    try:
        built = build()
    except BuildError as error:
        print(f"build refused: {error}")
        return 1
    if args.check:
        stale = [rel for rel, content in built.items() if not (REPO_ROOT / rel).exists() or (REPO_ROOT / rel).read_bytes() != content]
        print("pages: up to date" if not stale else f"pages: differ from a rebuild ({', '.join(stale)}); run python tools/build_journeys.py")
        return 0 if not stale else 1
    for rel, content in built.items():
        (REPO_ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        (REPO_ROOT / rel).write_bytes(content)
    print(f"wrote {len(built)} pages ({sum(len(c) for c in built.values())} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
