"""Page checks for the S20 research journeys: the entry page, the export-control page, the company and place profiles.

S20 (visual-architecture.md §15; D-189 to D-193, D-197). Standard library only. The pages are written by
tools/build_journeys.py; these checks read the committed pages and the data with their own loader (the DOM, homes
and contrast helpers of tests/test_page.py) and recompute every value the pages show. Two things come from tools,
each the one home of its rule: the build's fixed words (as PG-1 reads them) and the policy status rule
(tools/policy_status.py, D-156, D-191).

JR-1  every text node sits inside a record value, an absent value, a fixed label, a derived value or a framing
      block; no annotated value contains another;
JR-2  every record value equals its home; labels hold no digit and name no record; claims and sources in a panel
      are shown with their type, status, citations and dates;
JR-3  every derived value (counts, the as-of cell, the latest publication date, inputs, the panels' pointers and
      byte matches) equals an independent recomputation; every count names what it counts;
JR-4  the export-control matrix: one row per class or product a policy link or a policy refused candidate pairs
      with an act, one cell per act, each cell's state ("named", "refused" with its candidate, or none) equal to
      the records; the dependency-journey classes with their policy state;
JR-5  the timeline: one mark per dated event of every act, at its date on the declared scale; the as-of line at
      the as-of date; every act with no dated event listed beside it;
JR-6  every policy record shown sits in, or links to, a block that carries its official text link and the
      no-advice line (LA-5); no other page shows a policy ID (replaces PK-6 for these pages, D-189, D-191);
JR-7  every status equals policy_status.derive_status on the as-of date, which is the source-age reference date,
      a cell of its committed result;
JR-8  each profile shows every link, supplier naming, product, refused candidate and event that names its record
      (a company), or every company, facility and act recorded in it (a place); a refused candidate is never drawn
      as a link; the entry page links every research page and the client brief (S21, D-206) and lists every class
      with no dependency link;
JR-9  no forbidden word in the Atlas's own voice (labels, derived values, framing): "in force", "compliant",
      "licence required", "prohibited", "banned", "restricted", "critical";
JR-10 every link resolves (a fragment into another page names an element there); only record URLs and official
      texts point outside; nothing is loaded; no script;
JR-11 document structure (lang, one h1 equal to the title, landmarks, no skipped heading level, table headers
      with a scope, every SVG named), palette and contrast;
JR-12 every committed page equals a rebuild; two builds are identical; no other page sits in the journey folders.
"""

from __future__ import annotations

import datetime
import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import policy_status  # noqa: E402  (the one home of the status rule, D-156, D-191)
import test_page as tp  # noqa: E402  (the DOM, homes and contrast helpers; no test class is imported)

DATA = REPO_ROOT / "data"
SITE = REPO_ROOT / "site"
INDEX = "site/index.html"
EXPORT = "site/questions/export-control-texts/index.html"
BUILT = ("site/hbm-chain/index.html", "site/hbm-insight/index.html")
BRIEFS = ("site/briefs/accelerator-memory/index.html",)  # S21 (D-206): the entry page links the client brief too
AGE_RESULT = REPO_ROOT / "sql" / "results" / "source_age.json"
INPUT_GLOBS = ("data/*.json", "data/staging/*.json", "schemas/*.json", "sql/*.sql", "sql/results/*.json")
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
FORBIDDEN = ("in force", "compliant", "licence required", "license required", "prohibited", "banned", "restricted", "critical")
DERIVED_KINDS = {"count", "policy-status", "latest-published", "sql-cell", "input-file", "input-digest", "pointer", "bytes-match", "year"}
COUNT_UNITS = {
    # data-count -> the unit that must follow the number in its own line (V-4: a number shows its unit); the singular
    # stem, so that a count of one may read "1 link" (S20 browser QA found "1 links")
    "acts": "act", "classes": "class", "named-classes": "of", "links": "link", "link-acts": "act", "named-by": "of", "candidates": "refused candidate",
    "candidates-reason": "", "status": "of", "supplier": "", "products": "", "events": "", "incorporated": "", "headquartered": "",
    "located": "", "issued": "", "incorporation-unknown": "",
}


def load(name: str, folder: Path = DATA) -> list:
    return tp.load(folder / f"{name}.json")


def as_of() -> str:
    return json.loads(AGE_RESULT.read_text(encoding="utf-8"))["rows"][0]["reference_date"]


def period(date: str) -> tuple[str, str]:
    """A partial date as the first and last day of the period it names (independent of facility_status.period)."""
    parts = [int(p) for p in date.split("-")]
    if len(parts) == 3:
        return date, date
    year = parts[0]
    if len(parts) == 2:
        month = parts[1]
        last = (datetime.date(year + (month == 12), month % 12 + 1, 1) - datetime.timedelta(days=1)).isoformat()
        return f"{year:04d}-{month:02d}-01", last
    return f"{year:04d}-01-01", f"{year:04d}-12-31"


def day(date: str) -> int:
    return datetime.date.fromisoformat(date).toordinal()


class Records:
    """What the pages must show, read from data/ independently of the build."""

    def __init__(self) -> None:
        self.companies = load("companies")
        self.places = load("jurisdictions")
        self.policies = load("policies")
        self.events = load("events")
        self.edges = load("relationships")
        self.candidates = load("refused_candidates")
        self.products = load("products")
        self.facilities = load("facilities")
        self.claims = {c["id"]: c for c in load("claims")}
        self.sources = {s["id"]: s for s in load("sources")}
        self.classes = load("components") + load("technologies")
        self.policy_ids = [p["id"] for p in self.policies]
        self.links = [e for e in self.edges if e["relation_type"] == "restricts"]
        self.policy_candidates = [c for c in self.candidates if any(isinstance(s, str) and s in self.policy_ids for s in c["source_entities"])]

    def pages(self) -> list[str]:
        return [INDEX, EXPORT] + [f"site/companies/{c['id']}/index.html" for c in self.companies] + [f"site/places/{p['id']}/index.html" for p in self.places]

    def official_texts(self, policy_id: str) -> set[str]:
        policy = next(p for p in self.policies if p["id"] == policy_id)
        urls = set()
        for claim_id in policy.get("identity_claim_ids", []):
            for citation in self.claims[claim_id].get("citations", []):
                source = self.sources[citation["source_id"]]
                if source["source_class"] == "official_legal_text":
                    urls.add(source["url"])
        return urls

    def status(self, policy_id: str, on: str) -> str:
        policy = next(p for p in self.policies if p["id"] == policy_id)
        forms = {a["value"] for a in policy["instrument_form"]} if isinstance(policy["instrument_form"], list) else set()
        return policy_status.derive_status(policy_id, self.events, on, forms)[0]

    def targets(self) -> list[str]:
        """Every class or product a policy link or a policy refused candidate pairs with an act."""
        found: list[str] = []
        for t in [e["target_entity"] for e in self.links] + [t for c in self.policy_candidates for t in c["target_entities"]]:
            if t not in found:
                found.append(t)
        return found

    def cell(self, act: str, target: str) -> tuple[str, str | None]:
        link = next((e for e in self.links if e["source_entity"] == act and e["target_entity"] == target), None)
        if link:
            return "named", link["id"]
        cand = next((c for c in self.policy_candidates if act in c["source_entities"] and target in c["target_entities"]), None)
        if cand:
            return "refused", cand["id"]
        return "none", None

    def names(self, record_id: str, candidate: dict) -> bool:
        return record_id in [e for e in candidate["source_entities"] + candidate["target_entities"] if isinstance(e, str)] or candidate.get("item") == record_id

    def company_items(self, cid: str) -> dict[str, set[str]]:
        return {
            "link": {e["id"] for e in self.edges if cid in (e["source_entity"], e["target_entity"])},
            "supplier": {e["id"] for e in self.edges if isinstance(e.get("supplier"), list) and any(a["value"] == cid for a in e["supplier"])},
            "product": {p["id"] for p in self.products if p.get("vendor") == cid},
            "candidate": {c["id"] for c in self.candidates if self.names(cid, c)},
            "event": {e["id"] for e in self.events if e["subject"] == cid},
        }

    def place_items(self, pid: str) -> dict[str, set[str]]:
        held = lambda record, field: isinstance(record.get(field), list) and any(a["value"] == pid for a in record[field])  # noqa: E731
        return {
            "incorporated": {c["id"] for c in self.companies if held(c, "incorporated_in")},
            "headquartered": {c["id"] for c in self.companies if held(c, "headquartered_in")},
            "located": {f["id"] for f in self.facilities if held(f, "located_in")},
            "issued": {p["id"] for p in self.policies if held(p, "issued_in")},
        }

    def chainless(self) -> list[str]:
        """Classes neither end of any structural link (requires, has_part, incorporates) touches."""
        touched = {x for e in self.edges if e["relation_type"] in ("requires", "has_part", "incorporates") for x in (e["source_entity"], e["target_entity"])}
        return [c["id"] for c in self.classes if c["id"] not in touched]


def input_paths() -> list[str]:
    paths = {p.relative_to(REPO_ROOT).as_posix() for pattern in INPUT_GLOBS for p in REPO_ROOT.glob(pattern)}
    return sorted(paths | set(INPUT_FILES))


def build_module():
    import build_journeys  # noqa: PLC0415 (imported late: the checks are written before the build)

    return build_journeys


class Page:
    def __init__(self, rel: str) -> None:
        self.rel = rel
        self.path = REPO_ROOT / rel
        self.raw = self.path.read_text(encoding="utf-8") if self.path.exists() else ""
        self.root = tp.parse(self.raw) if self.raw else tp.Node("#root", {}, None)
        self.nodes = list(self.root.walk())
        self.by_id = {n.attrs["id"]: n for n in self.nodes if "id" in n.attrs}
        body = [n for n in self.nodes if n.tag == "body"]
        self.body = body[0] if body else tp.Node("body", {}, None)

    def find(self, **attrs) -> list:
        return [n for n in self.nodes if all(n.attrs.get(k.replace("_", "-")) == v for k, v in attrs.items())]

    def has(self, attr: str) -> list:
        return [n for n in self.nodes if attr in n.attrs]

    def visible(self):
        for text, parent in self.body.texts():
            if parent.tag not in ("style", "script"):
                yield text, parent


class JourneyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = Records()
        cls.homes = tp.Homes()
        cls.pages = {rel: Page(rel) for rel in cls.records.pages()}
        cls.on = as_of()

    def setUp(self) -> None:
        missing = [rel for rel, page in self.pages.items() if not page.raw]
        if missing:
            self.fail(f"pages not built: {', '.join(missing)} (python tools/build_journeys.py)")

    # JR-1
    def test_jr1_every_text_node_has_a_home(self) -> None:
        labels = set(build_module().LABELS)
        for rel, page in self.pages.items():
            for text, parent in page.visible():
                if tp.BARE.match(text):
                    continue
                owner = parent.annotated()
                with self.subTest(page=rel, text=tp.norm(text)[:80]):
                    self.assertIsNotNone(owner, "text with no record, label, derived value or framing behind it")
                    if "data-label" in owner.attrs:
                        self.assertIn(owner.text(), labels, "a label that is not one of the build's labels")
            for node in page.nodes:
                if any(a in node.attrs for a in ("data-ref", "data-label", "data-derived")):
                    inner = [n for n in node.walk() if n is not node and any(a in n.attrs for a in tp.ANNOTATIONS)]
                    with self.subTest(page=rel, leaf=node.attrs.get("data-ref") or node.text()[:40]):
                        self.assertEqual(inner, [], "an annotated value must not contain another")

    # JR-2
    def test_jr2_labels_carry_no_fact(self) -> None:
        for label in build_module().LABELS:
            with self.subTest(label=label):
                self.assertNotRegex(label, r"\d", "a label holds a digit")
                self.assertNotRegex(label.lower(), r"\bnone\b")
                for name in self.homes.names:
                    self.assertNotRegex(label, rf"(?<![\w-]){re.escape(name)}(?![\w-])", f"a label names a record ({name})")

    def test_jr2_every_record_value_equals_its_home(self) -> None:
        labels = set(build_module().LABELS)
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                values = page.has("data-ref")
                self.assertTrue(values, "no record value on the page")
                for node in values:
                    ref, field = node.attrs["data-ref"], node.attrs.get("data-field")
                    with self.subTest(page=rel, ref=ref, field=field):
                        self.assertIsNotNone(field, "data-ref without data-field")
                        self.assertNotIn(ref, self.homes.staging, "a staging record shown")
                        if "data-absent" in node.attrs:
                            self.assertFalse(self.homes.has(ref, field), "drawn as absent, but the field exists")
                            self.assertIn(node.text(), labels)
                            continue
                        self.assertTrue(self.homes.has(ref, field), "no such home")
                        value = self.homes.resolve(ref, field)
                        self.assertIsInstance(value, (str, int, float), "a value must be a scalar")
                        self.assertEqual(node.text(), tp.norm(tp.FORMATS[node.attrs.get("data-format")](str(value))))
                        if node.tag == "a" and field == "/url":
                            self.assertEqual(node.attrs.get("href"), value)

    def test_jr2_claims_in_panels_are_shown_whole(self) -> None:
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                shown = {(n.attrs["data-ref"], n.attrs["data-field"]) for n in page.has("data-ref")}
                for claim_id in sorted({ref for ref, field in shown if field == "/statement" and ref.startswith("claim-")}):
                    claim = self.homes.canonical[claim_id]
                    with self.subTest(page=rel, claim=claim_id):
                        for field in ("/claim_type", "/evidence_status", "/verified_on"):
                            self.assertIn((claim_id, field), shown)
                        for index, citation in enumerate(claim.get("citations", [])):
                            self.assertIn((claim_id, f"/citations/{index}/anchor"), shown)
                            self.assertIn((citation["source_id"], "/url"), shown)
                        if claim["claim_type"] in ("DERIVATION", "INTERPRETATION", "IMPLICATION"):
                            self.assertIn((claim_id, "/reasoning"), shown)

    # JR-3
    def expected_counts(self, page: Page) -> dict:
        r = self.records
        kind = page.body.attrs.get("data-page-kind")
        subject = page.body.attrs.get("data-subject")
        out: dict = {}
        if kind == "export":
            out[("acts", None)] = len(r.policies)
            out[("classes", None)] = len(r.classes)
            out[("links", None)] = len(r.links)
            out[("named-classes", None)] = len({e["target_entity"] for e in r.links})  # S20 design pass (D-198)
            out[("link-acts", None)] = len({e["source_entity"] for e in r.links})
            out[("candidates", None)] = len(r.policy_candidates)
            for target in {e["target_entity"] for e in r.links}:
                out[("named-by", target)] = sum(e["target_entity"] == target for e in r.links)
            for reason in {x for c in r.policy_candidates for x in c["reasons"]}:
                out[("candidates-reason", reason)] = sum(reason in c["reasons"] for c in r.policy_candidates)
            for status in {r.status(p, self.on) for p in r.policy_ids}:
                out[("status", status)] = sum(r.status(p, self.on) == status for p in r.policy_ids)
        elif kind == "company":
            for what, ids in r.company_items(subject).items():
                key = {"link": "links", "supplier": "supplier", "product": "products", "candidate": "candidates", "event": "events"}[what]
                if ids:
                    out[(key, None)] = len(ids)
        elif kind == "place":
            items = r.place_items(subject)
            for what, ids in items.items():
                if ids:
                    out[(what, None)] = len(ids)
            unknown = [c for c in items["headquartered"] if not isinstance(next(x for x in r.companies if x["id"] == c)["incorporated_in"], list)]
            if unknown:
                out[("incorporation-unknown", None)] = len(unknown)
        return out

    def test_jr3_derived_values_are_recomputed(self) -> None:
        age = json.loads(AGE_RESULT.read_text(encoding="utf-8"))
        latest = max(e["date"] for e in self.records.events if e["event_type"] == "published" and e["subject"] in self.records.policy_ids)
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                derived = page.has("data-derived")
                self.assertLessEqual({n.attrs["data-derived"] for n in derived}, DERIVED_KINDS, "a derived value the checks do not recompute")
                counts = {}
                for node in derived:
                    kind = node.attrs["data-derived"]
                    with self.subTest(page=rel, kind=kind, at=node.attrs.get("data-count") or node.attrs.get("data-target")):
                        if kind == "count":
                            key = (node.attrs["data-count"], node.attrs.get("data-key"))
                            counts.setdefault(key, set()).add(node.text())
                        elif kind == "sql-cell":
                            self.assertEqual(node.attrs.get("data-query"), "source_age")
                            value = age["rows"][int(node.attrs["data-row"])][node.attrs["data-column"]]
                            self.assertEqual(node.text(), str(value))
                        elif kind == "latest-published":
                            self.assertEqual(node.text(), latest)
                        elif kind == "pointer":
                            record = self.homes.canonical[node.attrs["data-target"]]
                            self.assertIn(node.attrs["data-claim"], tp.Homes.pointer(record, node.text()))
                        elif kind == "bytes-match":
                            claim = self.homes.canonical[node.attrs["data-target"]]
                            citation = claim["citations"][int(node.attrs["data-index"])]
                            registered = self.homes.canonical[citation["source_id"]]["retrieval"]["sha256"]
                            same = citation["read"]["sha256"].startswith(registered) or registered.startswith(citation["read"]["sha256"])
                            self.assertEqual(node.text(), "same bytes as registered" if same else "bytes changed since registration")
                        elif kind == "year":
                            svg = next(a for a in node.ancestors() if a.tag == "svg")
                            years = range(int(svg.attrs["data-from"][:4]), int(svg.attrs["data-to"][:4]) + 1)
                            self.assertIn(int(node.text()), years)
                with self.subTest(page=rel, what="counts"):
                    want = {k: {str(v)} for k, v in self.expected_counts(page).items()}
                    self.assertEqual(counts, want, "a count that differs from the records, or a count shown where nothing is counted")
                files = [n.text() for n in page.find(data_derived="input-file")]
                with self.subTest(page=rel, what="inputs"):
                    self.assertEqual(sorted(files), input_paths())
                    self.assertEqual([n.text() for n in page.find(data_derived="input-digest")], [tp.input_digest(input_paths())])

    def test_jr3_every_count_names_its_unit(self) -> None:
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                for node in page.find(data_derived="count"):
                    line = node.parent
                    text = tp.norm(line.text())
                    unit = COUNT_UNITS[node.attrs["data-count"]]
                    with self.subTest(page=rel, count=node.attrs["data-count"]):
                        self.assertTrue(any(n is not node and "data-label" in n.attrs for n in line.walk()), "a bare number with no words beside it")
                        if unit:
                            self.assertIn(unit, text)
                        self.assertNotEqual(node.text(), "0", "a zero shown as a count: the page says 'no recorded …' instead")

    # JR-4
    def test_jr4_the_matrix_equals_the_records(self) -> None:
        page = self.pages[EXPORT]
        r = self.records
        rows = [n for n in page.nodes if n.tag == "tr" and "data-target" in n.attrs]
        self.assertEqual([n.attrs["data-target"] for n in rows], r.targets(), "a target missing, added or out of order")
        for row in rows:
            target = row.attrs["data-target"]
            cells = [n for n in row.walk() if "data-cell" in n.attrs]
            self.assertEqual(sorted(c.attrs["data-act"] for c in cells), sorted(r.policy_ids), f"{target}: not one cell per act")
            for cell in cells:
                act = cell.attrs["data-act"]
                state, record = r.cell(act, target)
                with self.subTest(target=target, act=act):
                    self.assertEqual(cell.attrs["data-cell"], state)
                    if state == "named":
                        self.assertEqual(cell.attrs.get("data-link"), record)
                        self.assertTrue(any(n.tag == "a" and n.attrs.get("href") == f"#ev-{record}" for n in cell.walk()), "a named cell that does not open its link's evidence")
                    elif state == "refused":
                        self.assertEqual(cell.attrs.get("data-candidate"), record)
                        reasons = {n.attrs["data-ref"].rsplit("/", 1)[1] for n in cell.walk() if n.attrs.get("data-ref", "").startswith("schema:refused_candidates#vocab_reason/")}
                        self.assertEqual(reasons, set(next(c for c in r.candidates if c["id"] == record)["reasons"]), "a refusal without its reasons")
                        self.assertFalse([n for n in cell.walk() if n.tag in ("svg", "line")], "a refusal drawn as a line")
                    else:
                        self.assertIn("no recorded relationship", cell.text())

    def test_jr4_the_journey_classes_carry_their_policy_state(self) -> None:
        page = self.pages[EXPORT]
        r = self.records
        import build_page  # noqa: PLC0415 (the HBM page's own specification: which classes its chain reaches)

        chain = ["component-ai-accelerator"]
        for e in r.edges:
            if e["relation_type"] == "requires" and e["target_entity"] == build_page.JOURNEY["walk_root"]:
                chain += [e["source_entity"], e["target_entity"]]
        items = [n for n in page.nodes if "data-chain-class" in n.attrs]
        self.assertEqual([n.attrs["data-chain-class"] for n in items], chain)
        for item in items:
            target = item.attrs["data-chain-class"]
            links = [e for e in r.links if e["target_entity"] == target]
            cands = [c for c in r.policy_candidates if target in c["target_entities"]]
            with self.subTest(target=target):
                self.assertEqual(item.attrs["data-state"], "named" if links else "refused" if cands else "none")
                if not links and not cands:
                    self.assertIn("no recorded relationship", item.text())

    # JR-5
    def test_jr5_the_timeline_draws_every_dated_event_at_its_date(self) -> None:
        page = self.pages[EXPORT]
        r = self.records
        svgs = [n for n in page.nodes if n.tag == "svg" and "timeline" in n.attrs.get("class", "").split()]
        self.assertEqual(len(svgs), 1)
        svg = svgs[0]
        start, end, x0, x1 = svg.attrs["data-from"], svg.attrs["data-to"], float(svg.attrs["data-x0"]), float(svg.attrs["data-x1"])
        x = lambda d: x0 + (day(d) - day(start)) * (x1 - x0) / (day(end) - day(start))  # noqa: E731
        events = [e for e in r.events if e["subject"] in r.policy_ids]
        self.assertLessEqual(start, min(period(e["date"])[0] for e in events))
        self.assertGreaterEqual(end, max([period(e["date"])[1] for e in events] + [self.on]))
        marks = {n.attrs["data-event"]: n for n in svg.walk() if "data-event" in n.attrs}
        self.assertEqual(set(marks), {e["id"] for e in events}, "an event without a mark, or a mark without an event")
        for e in events:
            first, last = period(e["date"])
            shape = next(n for n in marks[e["id"]].walk() if n.tag in ("circle", "rect"))
            with self.subTest(event=e["id"]):
                if shape.tag == "circle":
                    self.assertEqual(first, last, "a period drawn as a day")
                    self.assertAlmostEqual(float(shape.attrs["cx"]), x(first), places=1)
                else:
                    self.assertAlmostEqual(float(shape.attrs["x"]), x(first), places=1)
                    self.assertAlmostEqual(float(shape.attrs["x"]) + float(shape.attrs["width"]), x(last) + (x1 - x0) / (day(end) - day(start)), places=1)
                self.assertTrue(marks[e["id"]].attrs.get("aria-labelledby") or marks[e["id"]].tag == "a", "a mark with no accessible name")
        asof = [n for n in svg.walk() if "data-asof" in n.attrs]
        self.assertEqual(len(asof), 1)
        self.assertAlmostEqual(float(asof[0].attrs["x1"]), x(self.on), places=1)
        undated = {p for p in r.policy_ids if not any(e["subject"] == p for e in events)}
        listed = {n.attrs["data-undated"] for n in page.nodes if "data-undated" in n.attrs}
        self.assertEqual(listed, undated, "an act with no dated event not listed beside the axis")
        words = {n.attrs["data-event-word"] for n in page.nodes if "data-event-word" in n.attrs}
        self.assertEqual(words, {e["id"] for e in events}, "the timeline's text equivalent misses an event")

    # JR-6
    def test_jr6_every_policy_shown_has_its_official_text_and_the_no_advice_line(self) -> None:
        r = self.records
        policy_like = set(r.policy_ids) | {e["id"] for e in r.links}
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                shown = {n.attrs["data-ref"] for n in page.has("data-ref") if n.attrs["data-ref"] in r.policy_ids}
                ids_in_text = {i for i in policy_like if i in page.raw}
                allowed = rel == EXPORT or (page.body.attrs.get("data-page-kind") == "place" and r.place_items(page.body.attrs["data-subject"])["issued"])
                if not allowed:
                    self.assertEqual(ids_in_text, set(), "a policy ID on a page with no policy view (PK-6)")
                    continue
                blocks = {n.attrs["data-act"]: n for n in page.nodes if "data-act" in n.attrs and n.tag in ("article", "li", "div")}
                for policy in shown:
                    block = blocks.get(policy)
                    with self.subTest(policy=policy):
                        self.assertIsNotNone(block, "a policy shown with no block for its text and the no-advice line")
                        hrefs = {n.attrs.get("href") for n in block.walk() if n.tag == "a" and "official" in n.attrs.get("class", "").split()}
                        self.assertTrue(hrefs and hrefs <= r.official_texts(policy), "no official text link, or a link that is not the act's official text")
                        self.assertIn(NO_ADVICE, [n.text() for n in block.walk() if "data-label" in n.attrs], "no no-advice line (LA-5)")
                for node in page.has("data-ref"):
                    ref = node.attrs["data-ref"]
                    if ref not in r.policy_ids:
                        continue
                    inside = any(a.attrs.get("data-act") == ref for a in node.ancestors())
                    linked = any(a.tag == "a" and a.attrs.get("href", "").startswith("#") and page.by_id.get(a.attrs["href"][1:]) is not None and page.by_id[a.attrs["href"][1:]].attrs.get("data-act") == ref for a in node.ancestors())
                    with self.subTest(policy=ref, field=node.attrs["data-field"]):
                        self.assertTrue(inside or linked, "a policy value outside its block and not linked to it")

    def test_jr6_the_built_pages_still_show_no_policy(self) -> None:
        r = self.records
        for rel in BUILT:
            raw = (REPO_ROOT / rel).read_text(encoding="utf-8")
            for ref in r.policy_ids + [e["id"] for e in r.links]:
                with self.subTest(page=rel, ref=ref):
                    self.assertNotIn(ref, raw)

    # JR-7
    def test_jr7_statuses_are_derived_on_the_as_of_date(self) -> None:
        page = self.pages[EXPORT]
        r = self.records
        statuses = page.find(data_derived="policy-status")
        self.assertEqual(sorted({n.attrs["data-policy"] for n in statuses}), sorted(r.policy_ids), "an act without its status")
        for node in statuses:
            with self.subTest(policy=node.attrs["data-policy"]):
                self.assertEqual(node.attrs["data-on"], self.on, "a status on another date than the as-of date")
                self.assertEqual(node.text(), r.status(node.attrs["data-policy"], self.on).replace("_", " "))
                self.assertTrue(any(n.attrs.get("data-column") == "reference_date" for n in node.parent.walk()) or any(n.attrs.get("data-column") == "reference_date" for n in page.nodes), "a status shown without its date")
        self.assertTrue(page.find(data_derived="sql-cell", data_query="source_age", data_column="reference_date"), "the as-of date is not the source-age cell")

    # JR-8
    def test_jr8_profiles_show_every_item_that_names_their_record(self) -> None:
        r = self.records
        for c in r.companies:
            page = self.pages[f"site/companies/{c['id']}/index.html"]
            with self.subTest(company=c["id"]):
                self.assertEqual(page.body.attrs.get("data-subject"), c["id"])
                for what, ids in r.company_items(c["id"]).items():
                    shown = {n.attrs[f"data-{what}"] for n in page.nodes if f"data-{what}" in n.attrs and n.tag == "li"}
                    self.assertEqual(shown, ids, f"{what}: the page and the records differ")
                cands = {n.attrs["data-candidate"] for n in page.nodes if "data-candidate" in n.attrs}
                links = {n.attrs.get("data-link") for n in page.nodes}
                self.assertFalse(cands & links, "a refused candidate drawn as a link")
                for n in page.nodes:
                    if n.tag == "li" and "data-candidate" in n.attrs:
                        self.assertIn("card", n.attrs.get("class", "").split(), "a refused candidate not shown as a card")
        for p in r.places:
            page = self.pages[f"site/places/{p['id']}/index.html"]
            with self.subTest(place=p["id"]):
                self.assertEqual(page.body.attrs.get("data-subject"), p["id"])
                for what, ids in r.place_items(p["id"]).items():
                    shown = {n.attrs[f"data-{what}"] for n in page.nodes if f"data-{what}" in n.attrs and n.tag == "li"}
                    self.assertEqual(shown, ids, f"{what}: the page and the records differ")
                for n in page.nodes:
                    if n.tag == "li" and "data-headquartered" in n.attrs:
                        company = next(x for x in r.companies if x["id"] == n.attrs["data-headquartered"])
                        if not isinstance(company["incorporated_in"], list):
                            state = company["incorporated_in"]["state"]
                            self.assertTrue(any(x.attrs.get("data-ref") == company["id"] and x.attrs.get("data-field") == "/incorporated_in/state" for x in n.walk()), f"{company['id']}: incorporation {state} not said")

    def test_jr8_the_entry_page_links_every_page_and_names_the_chainless_classes(self) -> None:
        page = self.pages[INDEX]
        hrefs = {(page.path.parent / n.attrs["href"]).resolve() for n in page.nodes if n.tag == "a" and "href" in n.attrs and not n.attrs["href"].startswith(("#", "http"))}
        for rel in [p for p in self.records.pages() if p != INDEX] + list(BUILT) + list(BRIEFS):
            with self.subTest(target=rel):
                self.assertIn((REPO_ROOT / rel).resolve(), hrefs, "a research page the entry page does not link")
        listed = [n.attrs["data-no-chain"] for n in page.nodes if "data-no-chain" in n.attrs]
        self.assertEqual(listed, self.records.chainless())
        for rel in BUILT:
            raw = (REPO_ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(built=rel):
                self.assertIn('href="../index.html"', raw, "a built page with no link to the entry page (D-193)")

    # JR-9
    def test_jr9_no_forbidden_word_in_the_atlas_voice(self) -> None:
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                for text, parent in page.visible():
                    owner = parent.annotated()
                    if owner is None or "data-ref" in owner.attrs:
                        continue  # a record value: quoted, the record's own words
                    for word in FORBIDDEN:
                        with self.subTest(page=rel, word=word):
                            self.assertNotRegex(text.lower(), rf"\b{word}\b", f"'{word}' in the Atlas's own voice: {tp.norm(text)[:80]}")

    # JR-10
    def test_jr10_links_resolve_and_nothing_loads(self) -> None:
        urls = {s["url"] for s in self.records.sources.values()}
        other = {}
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                for node in page.nodes:
                    self.assertNotIn(node.tag, ("script", "iframe", "object", "embed", "img", "link"), f"<{node.tag}> on a self-contained page")
                    self.assertNotIn("src", node.attrs)
                    for attr in ("onclick", "onmouseover", "onload", "onfocus"):
                        self.assertNotIn(attr, node.attrs)
                    href = node.attrs.get("href")
                    if href is None:
                        continue
                    with self.subTest(page=rel, href=href):
                        if href.startswith("#"):
                            self.assertIn(href[1:], page.by_id, "a fragment with no target")
                        elif re.match(r"https?://", href):
                            self.assertEqual(node.tag, "a")
                            self.assertIn(href, urls, "an outside link that is not a source's URL")
                        else:
                            path, _, fragment = href.partition("#")
                            target = (page.path.parent / path).resolve()
                            self.assertTrue(target.exists(), "a link to a file that does not exist")
                            if fragment and target.suffix == ".html":
                                if target not in other:
                                    other[target] = {n.attrs["id"] for n in tp.parse(target.read_text(encoding="utf-8")).walk() if "id" in n.attrs}
                                self.assertIn(fragment, other[target], "a fragment with no element in its page")
                            elif fragment:
                                self.assertTrue(path.endswith(".md"))
                                self.assertIn(fragment, tp.markdown_anchors(target.read_text(encoding="utf-8")))
                css = "".join("".join(t for t, _ in n.texts()) for n in page.nodes if n.tag == "style")
                self.assertNotRegex(css, r"@import|url\(", "the style loads a resource")

    # JR-11
    def test_jr11_document_structure(self) -> None:
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                html = next(n for n in page.nodes if n.tag == "html")
                self.assertEqual(html.attrs.get("lang"), "en")
                titles = [n for n in page.nodes if n.tag == "title" and n.parent.tag == "head"]
                h1 = [n for n in page.nodes if n.tag == "h1"]
                self.assertEqual(len(titles), 1)
                self.assertEqual(len(h1), 1)
                self.assertEqual(titles[0].text(), h1[0].text())
                self.assertTrue(any(n.tag == "meta" and n.attrs.get("name") == "viewport" for n in page.nodes))
                self.assertEqual(len([n for n in page.nodes if n.tag == "main"]), 1)
                levels = [int(n.tag[1]) for n in page.nodes if re.fullmatch(r"h[1-6]", n.tag)]
                for before, after in zip(levels, levels[1:]):
                    self.assertLessEqual(after, before + 1, "a skipped heading level")
                for th in (n for n in page.nodes if n.tag == "th"):
                    self.assertIn(th.attrs.get("scope"), ("col", "row"), "a table header with no scope")
                for svg in (n for n in page.nodes if n.tag == "svg" and n.attrs.get("aria-hidden") != "true"):
                    self.assertTrue(svg.attrs.get("aria-labelledby") and all(i in page.by_id for i in svg.attrs["aria-labelledby"].split()), "an unnamed figure")
                for panel in (n for n in page.nodes if n.attrs.get("id", "").startswith("ev-")):
                    self.assertFalse(any(a.tag == "details" for a in panel.ancestors() if a is not panel), "a panel hidden in a closed disclosure")

    def test_jr11_palette_and_contrast(self) -> None:
        for rel, page in self.pages.items():
            with self.subTest(page=rel):
                css = "".join("".join(t for t, _ in n.texts()) for n in page.nodes if n.tag == "style")
                root = re.search(r":root\s*\{([^}]*)\}", css)
                self.assertIsNotNone(root, "no palette")
                palette = dict(re.findall(r"--([a-z-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;", root.group(1)))
                for ink in (k for k in palette if k.startswith("ink")):
                    for surface in (k for k in palette if k.startswith("surface")):
                        self.assertGreaterEqual(tp.contrast(palette[ink], palette[surface]), 4.5, f"{ink} on {surface}")
                body = css[root.end():]
                self.assertNotRegex(body, r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", "a colour outside the palette")
                for rule in re.findall(r"([^{}]+)\{", body):
                    if ":hover" in rule:
                        self.assertIn(":focus-visible", rule, f"a hover rule without focus: {rule.strip()}")

    # JR-12
    def test_jr12_rebuild_is_byte_identical(self) -> None:
        build = build_module()
        first, second = build.build(), build.build()
        self.assertEqual(first, second, "two builds differ")
        self.assertEqual(sorted(first), sorted(self.records.pages()), "the build writes other pages than the records call for")
        for rel, content in first.items():
            with self.subTest(page=rel):
                self.assertEqual(self.pages[rel].raw.encode("utf-8"), content, "the committed page differs from a rebuild (python tools/build_journeys.py)")
        found = {p.relative_to(REPO_ROOT).as_posix() for folder in ("questions", "companies", "places") for p in (SITE / folder).rglob("*") if p.is_file()} if SITE.exists() else set()
        found |= {INDEX} if (SITE / "index.html").exists() else set()
        self.assertEqual(found, set(self.records.pages()), "a stray file in the journey folders")


if __name__ == "__main__":
    unittest.main()
