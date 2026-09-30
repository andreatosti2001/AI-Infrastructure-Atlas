"""validate-data, part 1: integrity checks over data/ (S06; D-051; standard library only).

With tests/test_data_schema.py (part 2, schema validity with the pinned jsonschema), this
is the Atlas's documented equivalent of MA §15's `validate-data`. H-4 placed it in CI as
tests; tools/ stays standard library (D-026). The checks, by ID (claim-model.md §11):

- VD-1  the data files exist and are JSON arrays of objects;
- VD-3  IDs are unique: sources, and claims across staging and canonical;
- VD-4  every source ID a claim cites (citations, search records) exists;
- VD-5  every input and competing claim exists and is not the claim itself; the graph of
        input claims has no cycle;
- VD-6  a claim's status is allowed by its inputs' statuses (claim-model.md §4);
- VD-7  disputes are mutual: each competing claim is disputed and names this one;
- VD-8  canonical claims (data/claims.json) are accepted by the human, and rest only on
        canonical claims; no staging claim carries an accepted verdict;
- VD-9  the migration is exact: every register row and S05 retrieval is one source record,
        with the values the register and source-policy.md §8.1 and §8.3 give;
- VD-10 a FACT cites at least one source whose class is sufficient for some matrix row
        (source-policy.md §7);
- VD-11 every anchor is verbatim in its machine-checkable home: the domain map for
        register sources, source-policy.md §8.3 for S05 retrievals;
- VD-12 dates are in order: bytes were read after the source was registered, and the claim
        was verified on or after the day the bytes were read;
- VD-13 a search record lists each class once, and each source under its own class.

The check functions take record lists, so the same checks run on the fictional fixtures.
"""

import json
import re
import unittest
from pathlib import Path

from test_claim_model import STATUSES, backticked, flat, status_rows
from test_entity_taxonomy import cells, section
from test_source_policy import column_classes, mapping_rows, matrix_rows, register_rows

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
SOURCES_FILE = DATA / "sources.json"
STAGING_FILE = DATA / "staging" / "claims.json"
CANONICAL_FILE = DATA / "claims.json"

POLICY = (REPO_ROOT / "docs/research/source-policy.md").read_text(encoding="utf-8")
REGISTER = (REPO_ROOT / "docs/research/source-register.md").read_text(encoding="utf-8")
DOMAIN_MAP = (REPO_ROOT / "docs/research/domain-map.md").read_text(encoding="utf-8")
COMPANY_CLASSES = {"company_filing", "company_technical_documentation", "company_press_release", "company_marketing"}

# One register row whose publisher cell names two organisations. source-policy.md §2 and
# §8.1 record SIA as the publishing party, with the BCG co-authorship in the authors
# (claim-model.md §9, rule for `publisher`).
PUBLISHER_OVERRIDES = {
    "SRC-005": (
        "Semiconductor Industry Association (SIA)",
        "R. Varadarajan et al. (Semiconductor Industry Association and Boston Consulting Group)",
    ),
}


def load_records(path: Path) -> list[dict]:
    """VD-1: a data file is a JSON array of objects."""
    records = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(records, list), f"{path} is not a JSON array"
    assert all(isinstance(r, dict) for r in records), f"{path} holds a non-object"
    return records


def load_data() -> tuple[list[dict], list[dict], list[dict]]:
    canonical = load_records(CANONICAL_FILE) if CANONICAL_FILE.exists() else []
    return load_records(SOURCES_FILE), load_records(STAGING_FILE), canonical


# --- migration (VD-9) -----------------------------------------------------------------------


def stated_dates(cell: str):
    if cell == "undated (live page)":
        return {"state": "undated"}
    match = re.fullmatch(r"(\d{4}(?:-\d{2}){0,2})(?: \(modified (\d{4}-\d{2}-\d{2})\))?", cell)
    if match:
        dates = [{"kind": "published", "date": match.group(1)}]
        if match.group(2):
            dates.append({"kind": "modified", "date": match.group(2)})
        return dates
    match = re.fullmatch(r"(modified|last updated) (\d{4}-\d{2}-\d{2})", cell)
    if match:
        return [{"kind": match.group(1).replace(" ", "_"), "date": match.group(2)}]
    raise ValueError(f"unparsed publication_date: {cell!r}")


def migrated_records() -> list[dict]:
    """The source records the register and the S05 retrievals become (claim-model.md §9).

    Deterministic: re-run it and compare with data/sources.json. publisher_entity is left
    out, because S07 fills it once the company records exist."""
    classes = {row[0]: backticked(row[1])[0] for row in mapping_rows()}
    records = []
    for row in register_rows():
        label, publisher_cell, title, url, published, _type, _tier, accessed, sha, _locators = row
        publisher, _, authors = publisher_cell.partition(" — ")
        publisher, authors = PUBLISHER_OVERRIDES.get(label, (publisher, authors))
        records.append({
            "id": label.lower(),
            "migrated_from": label,
            "source_class": classes[label],
            "title": title,
            "publisher": publisher,
            "authors": authors or {"state": "not_researched"},
            "url": url,
            "stated_dates": stated_dates(published),
            "retrieval": {"method": "automated", "accessed_at": accessed, "sha256": sha.strip("`")},
        })
    body = section(POLICY, "### 8.3 ", "**Why S05-R1")
    retrievals = [r for r in (cells(l) for l in body.splitlines()) if len(r) == 4 and re.fullmatch(r"S05-R\d+", r[0])]
    assert retrievals, "no S05 retrieval rows in source-policy.md §8.3"
    for label, what, retrieval, source_class in retrievals:
        (url,) = [b for b in backticked(what) if b.startswith("https://")]
        described = what[: what.index(", `")]
        publisher, _, title = described.partition(", ")
        copy = " (company-hosted copy)"
        record = {
            "id": f"src-{len(records) + 1:03d}",
            "migrated_from": label,
            "source_class": backticked(source_class)[0],
            "title": title.removesuffix(copy),
            "publisher": publisher,
            "authors": {"state": "not_researched"},
            "url": url,
            "stated_dates": [{"kind": "signed", "date": re.search(r"signed (\d{4}-\d{2}-\d{2})", retrieval).group(1)}],
            "retrieval": {
                "method": "automated",
                "accessed_at": re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z", retrieval).group(0),
                "sha256": re.search(r"SHA-256 prefix `([0-9a-f]+)`", retrieval).group(1),
            },
        }
        if title.endswith(copy):
            record["filing_copy"] = "filer_hosted_not_checked"
        records.append(record)
    return records


def check_migration(sources: list[dict]) -> list[str]:
    """VD-9."""
    errors = []
    by_label: dict[str, list[dict]] = {}
    for record in sources:
        if "migrated_from" in record:
            by_label.setdefault(record["migrated_from"], []).append(record)
    expected = migrated_records()
    for want in expected:
        found = by_label.get(want["migrated_from"], [])
        if len(found) != 1:
            errors.append(f"{want['migrated_from']}: {len(found)} source records, expected 1")
            continue
        for key, value in want.items():
            if found[0].get(key) != value:
                errors.append(f"{want['migrated_from']}.{key}: {found[0].get(key)!r} != {value!r}")
        if want["source_class"] in COMPANY_CLASSES:
            if found[0].get("publisher_entity") == {"state": "not_applicable"}:
                errors.append(f"{want['migrated_from']}: a company publisher is not not_applicable")
    extra = set(by_label) - {w["migrated_from"] for w in expected}
    errors += [f"{label}: migrated from a label that is not in the register or §8.3" for label in sorted(extra)]
    return errors


# --- claim checks ----------------------------------------------------------------------------


def all_claims(staging: list[dict], canonical: list[dict]) -> list[dict]:
    return staging + canonical


def check_ids(sources, staging, canonical) -> list[str]:
    """VD-3."""
    errors = []
    for kind, records in (("source", sources), ("claim", all_claims(staging, canonical))):
        seen = set()
        for record in records:
            if record["id"] in seen:
                errors.append(f"{kind} {record['id']} is defined twice")
            seen.add(record["id"])
    return errors


def check_source_references(sources, staging, canonical) -> list[str]:
    """VD-4."""
    ids = {s["id"] for s in sources}
    errors = []
    for claim in all_claims(staging, canonical):
        cited = [c["source_id"] for c in claim.get("citations", [])]
        for searched in claim.get("search", {}).get("classes", []):
            cited += searched.get("source_ids", [])
        errors += [f"{claim['id']} cites missing source {s}" for s in cited if s not in ids]
    return errors


def check_claim_references(staging, canonical) -> list[str]:
    """VD-5."""
    claims = {c["id"]: c for c in all_claims(staging, canonical)}
    errors = []
    for claim in claims.values():
        for field in ("input_claim_ids", "disputed_with"):
            for ref in claim.get(field, []):
                if ref == claim["id"]:
                    errors.append(f"{claim['id']}.{field} names itself")
                elif ref not in claims:
                    errors.append(f"{claim['id']}.{field} names missing claim {ref}")
    state: dict[str, str] = {}

    def visit(node: str, path: list[str]) -> None:
        if state.get(node) == "done" or node not in claims:
            return
        if state.get(node) == "open":
            errors.append("input cycle: " + " -> ".join(path + [node]))
            return
        state[node] = "open"
        for ref in claims[node].get("input_claim_ids", []):
            visit(ref, path + [node])
        state[node] = "done"

    for node in sorted(claims):
        visit(node, [])
    return errors


def check_status_rules(staging, canonical) -> list[str]:
    """VD-6: claim-model.md §4, status table, column "Inputs may be"."""
    rules = status_rows()
    claims = {c["id"]: c for c in all_claims(staging, canonical)}
    errors = []
    for claim in claims.values():
        allowed = rules[claim["evidence_status"]]["inputs"]
        for ref in claim.get("input_claim_ids", []):
            if ref in claims and claims[ref]["evidence_status"] not in allowed:
                errors.append(
                    f"{claim['id']} is {claim['evidence_status']} but input {ref} is {claims[ref]['evidence_status']}"
                )
    return errors


def check_disputes(staging, canonical) -> list[str]:
    """VD-7."""
    claims = {c["id"]: c for c in all_claims(staging, canonical)}
    errors = []
    for claim in claims.values():
        for ref in claim.get("disputed_with", []):
            other = claims.get(ref)
            if other and (other["evidence_status"] != "disputed" or claim["id"] not in other.get("disputed_with", [])):
                errors.append(f"{claim['id']} disputes {ref}, which does not dispute it back")
    return errors


def check_canonical(staging, canonical) -> list[str]:
    """VD-8."""
    canonical_ids = {c["id"] for c in canonical}
    canonical_statuses = {s for s, row in status_rows().items() if row["canonical"]}
    errors = []
    for claim in canonical:
        if claim["review"].get("verdict") != "accepted" or claim["review"].get("reviewer") != "human":
            errors.append(f"{claim['id']} is canonical without the human's acceptance")
        if claim["evidence_status"] not in canonical_statuses:
            errors.append(f"{claim['id']} is canonical with status {claim['evidence_status']}")
        for field in ("input_claim_ids", "disputed_with"):
            errors += [
                f"canonical {claim['id']} rests on staging claim {ref}"
                for ref in claim.get(field, [])
                if ref not in canonical_ids
            ]
    for claim in staging:
        if claim["review"].get("verdict") == "accepted":
            errors.append(f"{claim['id']} is accepted but still in staging")
    return errors


def never_sufficient_everywhere() -> set[str]:
    """Classes in the "never sufficient alone" column of every matrix row (source-policy.md §7)."""
    columns = [set(column_classes(row[3])) for row in matrix_rows()]
    return set.intersection(*columns)


def check_fact_classes(sources, staging, canonical) -> list[str]:
    """VD-10."""
    classes = {s["id"]: s["source_class"] for s in sources}
    weak = never_sufficient_everywhere()
    errors = []
    for claim in all_claims(staging, canonical):
        if claim["claim_type"] != "FACT":
            continue
        cited = {classes.get(c["source_id"]) for c in claim["citations"]}
        if cited <= weak:
            errors.append(f"FACT {claim['id']} cites only classes that are never sufficient alone: {sorted(cited)}")
    return errors


def check_anchors(sources, staging, canonical) -> list[str]:
    """VD-11."""
    labels = {s["id"]: s.get("migrated_from", "") for s in sources}
    homes = {"SRC": flat(DOMAIN_MAP), "S05": flat(section(POLICY, "### 8.3 ", "\n## 9. "))}
    errors = []
    for claim in all_claims(staging, canonical):
        for citation in claim.get("citations", []):
            home = homes.get(labels.get(citation["source_id"], "")[:3])
            if home is None:
                errors.append(f"{claim['id']}: no machine-checkable home for anchors of {citation['source_id']}")
            elif flat(citation["anchor"]) not in home:
                errors.append(f"{claim['id']}: anchor not verbatim in its home: {citation['anchor']!r}")
    return errors


def check_dates(sources, staging, canonical) -> list[str]:
    """VD-12."""
    registered = {s["id"]: s["retrieval"]["accessed_at"] for s in sources}
    errors = []
    for claim in all_claims(staging, canonical):
        for citation in claim.get("citations", []):
            read = citation.get("read")
            if not read:
                continue
            if citation["source_id"] in registered and read["accessed_at"] < registered[citation["source_id"]]:
                errors.append(f"{claim['id']}: {citation['source_id']} read before it was registered")
            if claim["verified_on"] < read["accessed_at"][:10]:
                errors.append(f"{claim['id']}: verified before the bytes were read")
    return errors


def check_searches(sources, staging, canonical) -> list[str]:
    """VD-13."""
    classes = {s["id"]: s["source_class"] for s in sources}
    errors = []
    for claim in all_claims(staging, canonical):
        searched = claim.get("search", {}).get("classes", [])
        names = [c["source_class"] for c in searched]
        if len(names) != len(set(names)):
            errors.append(f"{claim['id']}: a class is listed twice in the search")
        for entry in searched:
            for source_id in entry.get("source_ids", []):
                if source_id in classes and classes[source_id] != entry["source_class"]:
                    errors.append(f"{claim['id']}: {source_id} is listed under {entry['source_class']}, its class is {classes[source_id]}")
    return errors


def integrity_errors(sources, staging, canonical, anchors: bool = True) -> list[str]:
    """Every record-set check except VD-9 (migration) and, optionally, VD-11 (anchors)."""
    errors = check_ids(sources, staging, canonical)
    errors += check_source_references(sources, staging, canonical)
    errors += check_claim_references(staging, canonical)
    errors += check_status_rules(staging, canonical)
    errors += check_disputes(staging, canonical)
    errors += check_canonical(staging, canonical)
    errors += check_fact_classes(sources, staging, canonical)
    errors += check_dates(sources, staging, canonical)
    errors += check_searches(sources, staging, canonical)
    if anchors:
        errors += check_anchors(sources, staging, canonical)
    return errors


def fixture_set() -> tuple[list[dict], list[dict], list[dict]]:
    """The fictional sources and claims as one data set: accepted claims are canonical."""
    fixtures = REPO_ROOT / "tests" / "fixtures"
    sources = list(json.loads((fixtures / "source_records.json").read_text(encoding="utf-8"))["valid"].values())
    claims = list(json.loads((fixtures / "claims.json").read_text(encoding="utf-8"))["valid"].values())
    canonical = [c for c in claims if c["review"].get("verdict") == "accepted"]
    staging = [c for c in claims if c not in canonical]
    return sources, staging, canonical


class DataFileTests(unittest.TestCase):
    def test_vd1_data_files_are_arrays_of_objects(self) -> None:
        sources, staging, _ = load_data()
        self.assertTrue(sources, "data/sources.json is empty")
        self.assertTrue(staging or CANONICAL_FILE.exists(), "no claims")

    def test_claims_cover_every_claim_type(self) -> None:
        # S06 acceptance criterion 11: the seed covers all five types (H-1).
        from test_claim_model import TYPES

        _, staging, canonical = load_data()
        self.assertEqual({c["claim_type"] for c in staging + canonical}, TYPES)


class MigrationTests(unittest.TestCase):
    def test_vd9_every_register_row_is_one_exact_source_record(self) -> None:
        sources, _, _ = load_data()
        self.assertEqual(check_migration(sources), [])

    def test_migration_covers_the_register_and_s05(self) -> None:
        labels = [r["migrated_from"] for r in migrated_records()]
        self.assertEqual(labels[: len(register_rows())], [row[0] for row in register_rows()])
        self.assertTrue(any(label.startswith("S05-R") for label in labels))

    def test_register_is_marked_frozen(self) -> None:
        self.assertRegex(REGISTER.splitlines()[2], r"^\*\*Status:\*\* FROZEN")

    def test_policy_8_1_is_marked_history(self) -> None:
        body = section(POLICY, "### 8.1 ", "### 8.2 ")
        self.assertIn("data/sources.json", body)
        self.assertRegex(body, r"\bhistory\b")


class IntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sources, self.staging, self.canonical = load_data()

    def test_vd3_ids_are_unique(self) -> None:
        self.assertEqual(check_ids(self.sources, self.staging, self.canonical), [])

    def test_vd4_cited_sources_exist(self) -> None:
        self.assertEqual(check_source_references(self.sources, self.staging, self.canonical), [])

    def test_vd5_claim_references_resolve_without_cycles(self) -> None:
        self.assertEqual(check_claim_references(self.staging, self.canonical), [])

    def test_vd6_status_is_allowed_by_inputs(self) -> None:
        self.assertEqual(check_status_rules(self.staging, self.canonical), [])

    def test_vd7_disputes_are_mutual(self) -> None:
        self.assertEqual(check_disputes(self.staging, self.canonical), [])

    def test_vd8_only_accepted_claims_are_canonical(self) -> None:
        self.assertEqual(check_canonical(self.staging, self.canonical), [])

    def test_vd10_facts_rest_on_a_sufficient_class(self) -> None:
        self.assertEqual(check_fact_classes(self.sources, self.staging, self.canonical), [])

    def test_vd11_anchors_are_verbatim_in_their_home(self) -> None:
        self.assertEqual(check_anchors(self.sources, self.staging, self.canonical), [])

    def test_vd12_dates_are_in_order(self) -> None:
        self.assertEqual(check_dates(self.sources, self.staging, self.canonical), [])

    def test_vd13_searches_list_each_class_once(self) -> None:
        self.assertEqual(check_searches(self.sources, self.staging, self.canonical), [])


class FixtureSetTests(unittest.TestCase):
    """The checks accept the fictional set and catch a planted fault of each kind."""

    def test_fixture_set_is_clean(self) -> None:
        # Fixture anchors are fictional, so VD-11 does not apply to them.
        self.assertEqual(integrity_errors(*fixture_set(), anchors=False), [])

    def test_planted_faults_are_caught(self) -> None:
        import copy

        def planted(change) -> list[str]:
            sources, staging, canonical = copy.deepcopy(fixture_set())
            change(sources, staging, canonical)
            return integrity_errors(sources, staging, canonical, anchors=False)

        def claim(records, claim_id):
            return next(c for c in records if c["id"] == claim_id)

        faults = {
            "missing source": lambda s, st, c: claim(st, "claim-fixture-201")["citations"][0].update(source_id="src-999"),
            "missing input": lambda s, st, c: claim(st, "claim-fixture-109").update(input_claim_ids=["claim-fixture-998"]),
            "self input": lambda s, st, c: claim(st, "claim-fixture-204").update(input_claim_ids=["claim-fixture-204"]),
            "cycle": lambda s, st, c: claim(st, "claim-fixture-204").update(input_claim_ids=["claim-fixture-206"]),
            "input weaker than claim": lambda s, st, c: claim(st, "claim-fixture-206").update(input_claim_ids=["claim-fixture-203"]),
            "one-sided dispute": lambda s, st, c: claim(st, "claim-fixture-208").update(disputed_with=["claim-fixture-201"]),
            "staging claim in canonical": lambda s, st, c: c.append(claim(st, "claim-fixture-201")),
            "accepted claim in staging": lambda s, st, c: st.append(c.pop()),
            "duplicate claim ID": lambda s, st, c: st.append(dict(claim(st, "claim-fixture-201"))),
            "FACT from news only": lambda s, st, c: s[0].update(source_class="news_media"),
            "verified before read": lambda s, st, c: claim(st, "claim-fixture-201").update(verified_on="2026-09-01"),
            "search source under wrong class": lambda s, st, c: claim(st, "claim-fixture-112")["search"]["classes"][0].update(source_ids=["src-904"]),
        }
        for name, change in faults.items():
            with self.subTest(fault=name):
                self.assertNotEqual(planted(change), [], f"{name} was not caught")


if __name__ == "__main__":
    unittest.main()
