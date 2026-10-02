"""validate-data, part 5: relationship records (S10; edge-dataset.md §10; D-096).

Checks the edges in data/relationships.json (canonical) and data/staging/relationships.json
(staging) against the entity records, the claims, the sources and the events. Standard library
only; schema validity of the edges is part 2 (tests/test_data_schema.py). The rules are read
from their homes: kind constraints from relationship-taxonomy.md §2, the rows from
source-policy.md §7, the relation words from edge-dataset.md §7, product terms from
concept-dataset.md §7. The checks, by ID:

- V-1  endpoints, `item` and `supplier` values resolve to records of the prefixed type; every
       claim the edge or its `supplier` cites resolves;
- V-2  the kind constraints of relationship-taxonomy.md §2;
- V-3  no edge from a record to itself;
- V-4  valid_from <= valid_to, at the coarser precision;
- V-5  no two edges with the same type, endpoints and `item` over overlapping periods (an
       undated edge overlaps every period);
- V-6  a `requires` or `has_part` edge does not restate a `broader` link between its endpoints;
- V-7  warning: a `supplies` edge whose `item` is a product whose vendor is not the source;
- V-8  warning: RW-1 to RW-3 (relationship-taxonomy.md §11);
- V-9  no placeholder slug in an endpoint, `item` or `supplier` value;
- V-10 each edge rests on a citation whose class and standing its `rel:<type>` row allows;
       each `supplier` assertion on `rel:incorporates.supplier`; a not_publicly_determinable
       supplier's search covers every preferred class of that row (ER-3, claim-model.md §8);
- CE-1 a canonical edge cites canonical claims and has canonical endpoints, `item` and
       `supplier` companies; edge IDs are unique, and none is both staging and canonical;
- RI-1 an edge ID is `rel-`, the source ID, the type (`_` as `-`), the target ID and, for
       `supplies`, the item ID (edge-dataset.md §2);
- PL-1 a product edge rests on an anchor carrying the first word of the product's term (ER-9);
- EP-1 a `fabricates` edge never cites directly a claim serving a `vendor_process_name` (ER-1);
- PE-1 an edge cites a FACT or DERIVATION, and no claim of an `announced` event (ER-8);
- RV-1 an anchor the edge reaches carries a word of its type's row (RR-1).

The check functions take record lists, so the same checks run on the fictional fixtures.
"""

import copy
import json
import re
import unittest
import warnings
from pathlib import Path

from test_data_entities import (
    all_records,
    coarse,
    fixture_world,
    leaf_citations,
    load_entities,
    matrix,
    placeholder_pattern,
    product_table,
)
from test_data_events import fixture_events, load_events
from test_data_integrity import DATA, load_data, load_records
from test_entity_taxonomy import cells, section
from test_source_policy import column_classes, matrix_rows

REPO_ROOT = Path(__file__).resolve().parent.parent
REL_SCHEMA = json.loads((REPO_ROOT / "schemas/relationships.schema.json").read_text(encoding="utf-8"))
TAXONOMY = (REPO_ROOT / "docs/architecture/relationship-taxonomy.md").read_text(encoding="utf-8")
EDGES_DOC = (REPO_ROOT / "docs/architecture/edge-dataset.md").read_text(encoding="utf-8")
EDGE_FIXTURES = json.loads((REPO_ROOT / "tests/fixtures/edge_records.json").read_text(encoding="utf-8"))

VOCAB = REL_SCHEMA["$defs"]["vocab_relation_type"]["oneOf"]
TYPES = {v["const"] for v in VOCAB}
LEVEL = {v["const"]: v["x-level"] for v in VOCAB}
PREFIX_TYPE = {"company": "company", "facility": "facility", "technology": "technology", "component": "component", "product": "product"}


def edge_files() -> tuple[Path, Path]:
    """(canonical, staging) paths of the relationship files (H-2 layout, D-098)."""
    return DATA / "relationships.json", DATA / "staging" / "relationships.json"


def load_edges() -> dict:
    canonical, staging = edge_files()
    return {
        "canonical": load_records(canonical) if canonical.exists() else [],
        "staging": load_records(staging) if staging.exists() else [],
    }


def all_edges(edges) -> list[tuple[str, dict]]:
    return [(where, e) for where in ("canonical", "staging") for e in edges[where]]


# --- the rules, read from their homes ---------------------------------------------------------


def relation_words() -> dict[str, list[str]]:
    """edge-dataset.md §7: relation type -> the words of RV-1."""
    body = section(EDGES_DOC, "\n## 7. ", "\n## 8. ")
    result = {}
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 2 and re.fullmatch(r"`[a-z_]+`", row[0]) and row[0].strip("`") in TYPES:
            result[row[0].strip("`")] = [w.strip() for w in row[1].split(";")]
    assert result, "no relation-word table in edge-dataset.md §7"
    return result


def kind_table_types() -> set[str]:
    """relationship-taxonomy.md §2: the types of the 'Kind constraint' table."""
    body = section(TAXONOMY, "**Enforced where.**", "\n## 3. ")
    types = set()
    for line in body.splitlines():
        row = cells(line)
        if len(row) == 2 and row[0].startswith("`"):
            types |= set(re.findall(r"`([a-z_]+)`", row[0]))
    assert types, "no kind-constraint table in relationship-taxonomy.md §2"
    return types


def preferred_classes(row_key: str) -> set[str]:
    """source-policy.md §7: the Preferred column of one row (ER-3's search rule)."""
    for row in matrix_rows():
        if row[0].strip("`") == row_key:
            return set(column_classes(row[1]))
    raise AssertionError(f"no matrix row {row_key}")


def product_terms(rows=None) -> dict[str, str]:
    """concept-dataset.md §7 (or a fixture world's table): product ID -> term."""
    rows = product_table() if rows is None else rows
    return {row[0]: row[1] for row in rows}


def expected_id(edge: dict) -> str:
    """RI-1 (edge-dataset.md §2)."""
    parts = [edge["source_entity"], edge["relation_type"].replace("_", "-"), edge["target_entity"]]
    if "item" in edge:
        parts.append(edge["item"])
    return "rel-" + "-".join(parts)


# --- walking edges ----------------------------------------------------------------------------


def supplier_assertions(edge: dict) -> list[dict]:
    value = edge.get("supplier")
    return value if isinstance(value, list) else []


def supplier_state(edge: dict) -> dict | None:
    value = edge.get("supplier")
    return value if isinstance(value, dict) else None


def cited_claims(edge: dict) -> list[str]:
    """Every claim the edge cites: its own, its supplier assertions' and its supplier state's."""
    ids = list(edge["claim_ids"])
    for assertion in supplier_assertions(edge):
        ids += assertion["claim_ids"]
    state = supplier_state(edge)
    if state:
        ids += state.get("claim_ids", [])
    return ids


def references(edge: dict) -> list[tuple[str, str]]:
    """(field, entity ID) for every entity the edge points to."""
    refs = [("source_entity", edge["source_entity"]), ("target_entity", edge["target_entity"])]
    if "item" in edge:
        refs.append(("item", edge["item"]))
    refs += [("supplier", a["value"]) for a in supplier_assertions(edge)]
    return refs


def overlap(a: dict, b: dict) -> bool:
    """Do two periods overlap? A missing bound is open (an undated edge overlaps every period)."""
    a_from, a_to, b_from, b_to = a.get("valid_from"), a.get("valid_to"), b.get("valid_from"), b.get("valid_to")
    if a_to and b_from and coarse(a_to, b_from) < coarse(b_from, a_to):
        return False
    if b_to and a_from and coarse(b_to, a_from) < coarse(a_from, b_to):
        return False
    return True


def records_by_id(entities) -> dict[str, tuple[str, dict]]:
    return {r["id"]: (where, r) for where, r in all_records(entities)}


# --- checks -----------------------------------------------------------------------------------


def check_edge_references(edges, entities, staging_claims, canonical_claims) -> list[str]:
    """V-1."""
    records = records_by_id(entities)
    claims = {c["id"] for c in staging_claims + canonical_claims}
    errors = []
    for _, edge in all_edges(edges):
        for field, ref in references(edge):
            prefix = ref.split("-", 1)[0]
            found = records.get(ref)
            if found is None:
                errors.append(f"{edge['id']}.{field}: {ref} does not exist")
            elif found[1]["type"] != PREFIX_TYPE.get(prefix):
                errors.append(f"{edge['id']}.{field}: {ref} is a {found[1]['type']} record, not a {prefix}")
        errors += [f"{edge['id']} cites missing claim {c}" for c in cited_claims(edge) if c not in claims]
    return errors


def _hardware(record) -> bool:
    return record.get("product_kind") == "hardware"


# One rule per row of relationship-taxonomy.md §2's kind-constraint table (V-2). A test checks
# that the table's types and these keys are the same set.
KIND_RULES = {
    "requires": lambda s, t: [] if not (s["type"] == "component" and s.get("use_class") == "production_equipment") else ["a production_equipment component is never the source of requires"],
    "has_part": lambda s, t: [f"{r['id']} is not a constituent component" for r in (s, t) if r.get("use_class") != "constituent"],
    "designs": lambda s, t: [] if _hardware(t) else [f"{t['id']} is not a hardware product"],
    "fabricates": lambda s, t: [] if _hardware(t) else [f"{t['id']} is not a hardware product"],
    "packages": lambda s, t: [] if _hardware(t) else [f"{t['id']} is not a hardware product"],
    "incorporates": lambda s, t: ([] if _hardware(s) else [f"{s['id']} is not a hardware product"])
    + ([] if (_hardware(t) if t["type"] == "product" else t.get("use_class") == "constituent") else [f"{t['id']} is not a hardware product or a constituent component"]),
    "houses": lambda s, t: ([] if "data_centre" in s.get("facility_kinds", []) else [f"{s['id']} is not a data_centre"]) + ([] if _hardware(t) else [f"{t['id']} is not a hardware product"]),
    "provides_access_to": lambda s, t: ([] if s.get("product_kind") == "service" else [f"{s['id']} is not a service product"]) + ([] if _hardware(t) else [f"{t['id']} is not a hardware product"]),
}


def check_edge_kinds(edges, entities) -> list[str]:
    """V-2."""
    records = records_by_id(entities)
    errors = []
    for _, edge in all_edges(edges):
        rule = KIND_RULES.get(edge["relation_type"])
        source, target = records.get(edge["source_entity"]), records.get(edge["target_entity"])
        if rule and source and target:
            errors += [f"{edge['id']} ({edge['relation_type']}): {message}" for message in rule(source[1], target[1])]
    return errors


def check_self_edges(edges) -> list[str]:
    """V-3."""
    return [f"{e['id']}: an edge from a record to itself" for _, e in all_edges(edges) if e["source_entity"] == e["target_entity"]]


def check_edge_periods(edges) -> list[str]:
    """V-4."""
    errors = []
    for _, edge in all_edges(edges):
        start, end = edge.get("valid_from"), edge.get("valid_to")
        if start and end and coarse(start, end) > coarse(end, start):
            errors.append(f"{edge['id']}: valid_from {start} is after valid_to {end}")
    return errors


def check_duplicates(edges) -> list[str]:
    """V-5."""
    listed = [e for _, e in all_edges(edges)]
    errors = []
    for i, a in enumerate(listed):
        for b in listed[i + 1 :]:
            same = all(a.get(k) == b.get(k) for k in ("relation_type", "source_entity", "target_entity", "item"))
            if same and overlap(a, b):
                errors.append(f"{a['id']} and {b['id']}: same type, endpoints and item over overlapping periods")
    return errors


def check_broader_restated(edges, entities) -> list[str]:
    """V-6."""
    records = records_by_id(entities)
    errors = []
    for _, edge in all_edges(edges):
        if LEVEL[edge["relation_type"]] != "class":
            continue
        source, target = records.get(edge["source_entity"]), records.get(edge["target_entity"])
        if source and target and (target[1]["id"] in source[1].get("broader", []) or source[1]["id"] in target[1].get("broader", [])):
            errors.append(f"{edge['id']}: restates broader between {edge['source_entity']} and {edge['target_entity']}")
    return errors


def check_vendor_warnings(edges, entities) -> list[str]:
    """V-7 (warnings)."""
    records = records_by_id(entities)
    found = []
    for _, edge in all_edges(edges):
        item = records.get(edge.get("item", ""))
        if edge["relation_type"] == "supplies" and item and item[1]["type"] == "product" and item[1]["vendor"] != edge["source_entity"]:
            found.append(f"{edge['id']}: the supplied product's vendor is {item[1]['vendor']}, not the source (V-7)")
    return found


def check_role_warnings(edges, entities) -> list[str]:
    """V-8 (warnings): RW-1 to RW-3, over overlapping or undated periods."""
    records = records_by_id(entities)
    found = []
    for _, edge in all_edges(edges):
        company = records.get(edge["source_entity"])
        if company is None or company[1]["type"] != "company" or not isinstance(company[1].get("roles"), list):
            continue
        for role in company[1]["roles"]:
            if role["value"] != "fabless_designer" or not overlap(role, edge):
                continue
            kind, target = edge["relation_type"], records.get(edge["target_entity"])
            if kind in ("owns", "operates") and target and "wafer_fab" in target[1].get("facility_kinds", []):
                found.append(f"{edge['id']}: a fabless_designer {kind} a wafer_fab (RW-1)")
            elif kind == "fabricates":
                found.append(f"{edge['id']}: a fabless_designer fabricates a product (RW-2)")
            elif kind == "packages":
                found.append(f"{edge['id']}: a fabless_designer packages a product (RW-3)")
    return found


def check_edge_placeholders(edges) -> list[str]:
    """V-9."""
    pattern = placeholder_pattern()
    return [f"{e['id']}.{field}: {ref} is a placeholder slug" for _, e in all_edges(edges) for field, ref in references(e) if pattern.search(ref)]


def check_edge_matrix(edges, sources, staging_claims, canonical_claims) -> list[str]:
    """V-10."""
    rows = matrix()
    classes = {s["id"]: s["source_class"] for s in sources}
    claims = {c["id"]: c for c in staging_claims + canonical_claims}

    def supported(ids, row_key) -> bool:
        row = rows[row_key]
        leaves = [c for cid in ids for _, c in leaf_citations(cid, claims)]
        return any(classes.get(c["source_id"]) in row["sufficient"] and c["standing"] in row["standings"] for c in leaves)

    errors = []
    for _, edge in all_edges(edges):
        row_key = f"rel:{edge['relation_type']}"
        if not supported(edge["claim_ids"], row_key):
            errors.append(f"{edge['id']}: no citation with a class and standing that {row_key} allows")
        qualifier = f"rel:{edge['relation_type']}.supplier"
        for assertion in supplier_assertions(edge):
            if not supported(assertion["claim_ids"], qualifier):
                errors.append(f"{edge['id']}.supplier = {assertion['value']}: no citation with a class and standing that {qualifier} allows")
        state = supplier_state(edge)
        if state and state["state"] == "not_publicly_determinable":
            searched = {
                entry["source_class"]
                for cid in state.get("claim_ids", [])
                for entry in claims.get(cid, {}).get("search", {}).get("classes", [])
                if entry["outcome"] == "no_answer"
            }
            for missing in sorted(preferred_classes(qualifier) - searched):
                errors.append(f"{edge['id']}.supplier: not_publicly_determinable, but the search did not search the preferred class {missing} (ER-3)")
    return errors


def check_canonical_edges(edges, entities, canonical_claims) -> list[str]:
    """CE-1."""
    claim_ids = {c["id"] for c in canonical_claims}
    records = records_by_id(entities)
    errors = []
    seen = {}
    for where, edge in all_edges(edges):
        if edge["id"] in seen:
            errors.append(f"{edge['id']} is defined twice ({seen[edge['id']]} and {where})")
        seen[edge["id"]] = where
        if where != "canonical":
            continue
        errors += [f"canonical {edge['id']} cites staging claim {c}" for c in cited_claims(edge) if c not in claim_ids]
        for field, ref in references(edge):
            if ref in records and records[ref][0] != "canonical":
                errors.append(f"canonical {edge['id']}.{field} points to non-canonical {ref}")
    return errors


def check_edge_ids(edges) -> list[str]:
    """RI-1."""
    return [f"{e['id']}: not rel- plus the source, type, target and item (expected {expected_id(e)})" for _, e in all_edges(edges) if e["id"] != expected_id(e)]


def check_product_named(edges, staging_claims, canonical_claims, terms) -> list[str]:
    """PL-1."""
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for _, edge in all_edges(edges):
        anchors = [c["anchor"].lower() for cid in edge["claim_ids"] for _, c in leaf_citations(cid, claims)]
        for ref in (edge["source_entity"], edge["target_entity"]):
            if not ref.startswith("product-"):
                continue
            term = terms.get(ref)
            if term is None:
                errors.append(f"{edge['id']}: {ref} has no term in the product table")
            elif not any(term.split()[0].lower() in a for a in anchors):
                errors.append(f"{edge['id']}: its evidence never names the product {ref} ({term.split()[0]!r}; ER-9)")
    return errors


def check_process_names(edges, entities) -> list[str]:
    """EP-1."""
    process_claims = {
        cid
        for _, r in all_records(entities)
        if r["type"] == "product" and isinstance(r.get("vendor_process_name"), list)
        for a in r["vendor_process_name"]
        for cid in a["claim_ids"]
    }
    return [
        f"{e['id']}: cites {cid} directly, a process name; fabrication from a process name is a DERIVATION (ER-1)"
        for _, e in all_edges(edges)
        if e["relation_type"] == "fabricates"
        for cid in e["claim_ids"]
        if cid in process_claims
    ]


def check_edge_plans(edges, events, staging_claims, canonical_claims) -> list[str]:
    """PE-1."""
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    planned = {cid for where in ("canonical", "staging") for e in events[where] if e["event_type"] == "announced" for cid in e["claim_ids"]}
    errors = []
    for _, edge in all_edges(edges):
        types = [claims.get(cid, {}).get("claim_type") for cid in edge["claim_ids"]]
        if not any(t in ("FACT", "DERIVATION") for t in types):
            errors.append(f"{edge['id']}: rests on no FACT or DERIVATION")
        errors += [f"{edge['id']}: cites {cid}, the claim of an announced event (ER-8)" for cid in edge["claim_ids"] if cid in planned]
    return errors


def check_relation_words(edges, staging_claims, canonical_claims, words) -> list[str]:
    """RV-1."""
    claims = {c["id"]: c for c in staging_claims + canonical_claims}
    errors = []
    for _, edge in all_edges(edges):
        anchors = [c["anchor"].lower() for cid in edge["claim_ids"] for _, c in leaf_citations(cid, claims)]
        row = words.get(edge["relation_type"], [])
        if not any(w.lower() in a for w in row for a in anchors):
            errors.append(f"{edge['id']}: no relation word of {edge['relation_type']} in its anchors (edge-dataset.md §7; RR-1)")
    return errors


def edge_errors(edges, entities, events, sources, staging_claims, canonical_claims, terms) -> list[str]:
    errors = check_edge_references(edges, entities, staging_claims, canonical_claims)
    errors += check_edge_kinds(edges, entities)
    errors += check_self_edges(edges)
    errors += check_edge_periods(edges)
    errors += check_duplicates(edges)
    errors += check_broader_restated(edges, entities)
    errors += check_edge_placeholders(edges)
    errors += check_edge_matrix(edges, sources, staging_claims, canonical_claims)
    errors += check_canonical_edges(edges, entities, canonical_claims)
    errors += check_edge_ids(edges)
    errors += check_product_named(edges, staging_claims, canonical_claims, terms)
    errors += check_process_names(edges, entities)
    errors += check_edge_plans(edges, events, staging_claims, canonical_claims)
    errors += check_relation_words(edges, staging_claims, canonical_claims, relation_words())
    return errors


def edge_warnings(edges, entities) -> list[str]:
    return check_vendor_warnings(edges, entities) + check_role_warnings(edges, entities)


# --- the fictional world ----------------------------------------------------------------------


def edge_fixture_world():
    """The entity fixture world with the edge fixtures added:
    (edges, entities, events, sources, staging claims, canonical claims, product terms)."""
    entities, sources, staging, canonical = fixture_world()
    valid = copy.deepcopy(EDGE_FIXTURES["valid"])
    sources += valid["sources"]
    staging += valid["staging_claims"]
    canonical += valid["canonical_claims"]
    for _, record in all_records(entities):
        record.update(valid["product_overrides"].get(record["id"], {}))
    terms = product_terms([tuple(row) for row in valid["product_terms"]])
    return valid["relationships"], entities, fixture_events(), sources, staging, canonical, terms


def apply_fault(world, fault) -> None:
    edges, _, _, _, staging, canonical, _ = world
    claims = {c["id"]: c for c in staging + canonical}
    action = fault["action"]
    if action == "set_edge_field":
        edge = edges[fault["where"]][fault["index"]]
        if fault.get("remove"):
            edge.pop(fault["field"])
        else:
            edge[fault["field"]] = fault["value"]
    elif action == "add_edge":
        edges[fault["where"]].append(copy.deepcopy(fault["record"]))
    elif action == "move_edge":
        edges["canonical"].append(edges[fault["from"]].pop(fault["index"]))
    elif action == "set_citation_field":
        claims[fault["claim"]]["citations"][0][fault["field"]] = fault["value"]
    elif action == "drop_search_class":
        search = claims[fault["claim"]]["search"]
        search["classes"] = [c for c in search["classes"] if c["source_class"] != fault["source_class"]]
    else:
        raise AssertionError(f"unknown fault action {action}")


# --- tests ------------------------------------------------------------------------------------


class RuleSourceTests(unittest.TestCase):
    def test_relation_words_cover_the_vocabulary(self) -> None:
        # edge-dataset.md §7: every relation type has words, and no other.
        self.assertEqual(set(relation_words()), TYPES)

    def test_kind_rules_follow_the_taxonomy_table(self) -> None:
        # V-2 implements one rule per row of relationship-taxonomy.md §2.
        self.assertEqual(set(KIND_RULES), kind_table_types())

    def test_every_relation_type_and_qualifier_has_a_matrix_row(self) -> None:
        rows = matrix()
        for kind in TYPES:
            with self.subTest(row=kind):
                self.assertIn(f"rel:{kind}", rows)
        self.assertIn("rel:incorporates.supplier", rows)

    def test_edge_id_rule_examples(self) -> None:
        self.assertEqual(
            expected_id({"source_entity": "company-a", "relation_type": "provides_access_to", "target_entity": "product-b"}),
            "rel-company-a-provides-access-to-product-b",
        )
        self.assertEqual(
            expected_id({"source_entity": "company-a", "relation_type": "supplies", "target_entity": "company-b", "item": "component-c"}),
            "rel-company-a-supplies-company-b-component-c",
        )

    def test_display_name_does_not_move_an_edge_id(self) -> None:
        # RI-1 reads only IDs, never a display name.
        edges, entities, *_ = edge_fixture_world()
        for _, record in all_records(entities):
            record["name"] = "A Completely Different Display Name"
        self.assertEqual(check_edge_ids(edges), [])


class EdgeDataTests(unittest.TestCase):
    """The checks on the real files."""

    def setUp(self) -> None:
        self.edges = load_edges()
        self.entities = load_entities()
        self.events = load_events()
        self.sources, self.staging, self.canonical = load_data()

    def test_edge_files_exist(self) -> None:
        # L-05: each data file this session creates is in the validator's scope.
        for path in edge_files():
            with self.subTest(path=path.name):
                self.assertTrue(path.exists())

    def test_s10_gate_edges_exist(self) -> None:
        # Roadmap S10 gate: "auditable supply edges"; the checks below check them.
        self.assertTrue(self.edges["canonical"] + self.edges["staging"], "no relationship record")

    def test_v1_references_resolve(self) -> None:
        self.assertEqual(check_edge_references(self.edges, self.entities, self.staging, self.canonical), [])

    def test_v2_kind_constraints(self) -> None:
        self.assertEqual(check_edge_kinds(self.edges, self.entities), [])

    def test_v3_no_self_edges(self) -> None:
        self.assertEqual(check_self_edges(self.edges), [])

    def test_v4_periods_are_ordered(self) -> None:
        self.assertEqual(check_edge_periods(self.edges), [])

    def test_v5_no_duplicate_edges(self) -> None:
        self.assertEqual(check_duplicates(self.edges), [])

    def test_v6_no_broader_restated(self) -> None:
        self.assertEqual(check_broader_restated(self.edges, self.entities), [])

    def test_v7_v8_warnings_are_reported(self) -> None:
        # D-033: warnings, never failures; nothing is corrected.
        for message in edge_warnings(self.edges, self.entities):
            warnings.warn(message)

    def test_v9_no_placeholder_endpoints(self) -> None:
        self.assertEqual(check_edge_placeholders(self.edges), [])

    def test_v10_edges_rest_on_allowed_classes_and_standing(self) -> None:
        self.assertEqual(check_edge_matrix(self.edges, self.sources, self.staging, self.canonical), [])

    def test_ce1_canonical_edges_rest_on_canonical_records(self) -> None:
        self.assertEqual(check_canonical_edges(self.edges, self.entities, self.canonical), [])

    def test_ri1_edge_ids_follow_the_rule(self) -> None:
        self.assertEqual(check_edge_ids(self.edges), [])

    def test_pl1_product_edges_name_the_product(self) -> None:
        self.assertEqual(check_product_named(self.edges, self.staging, self.canonical, product_terms()), [])

    def test_ep1_no_fabricates_from_a_process_name(self) -> None:
        self.assertEqual(check_process_names(self.edges, self.entities), [])

    def test_pe1_no_edge_from_a_plan(self) -> None:
        self.assertEqual(check_edge_plans(self.edges, self.events, self.staging, self.canonical), [])

    def test_rv1_relation_words(self) -> None:
        self.assertEqual(check_relation_words(self.edges, self.staging, self.canonical, relation_words()), [])


class EdgeFixtureTests(unittest.TestCase):
    """The checks accept the fictional edges and catch a planted fault of each kind."""

    def test_fixture_edges_are_clean(self) -> None:
        self.assertEqual(edge_errors(*edge_fixture_world()), [])
        edges, entities, *_ = edge_fixture_world()
        self.assertEqual(edge_warnings(edges, entities), [])

    def test_planted_faults_are_caught(self) -> None:
        faults = EDGE_FIXTURES["faults"]
        self.assertTrue(faults)
        for fault in faults:
            with self.subTest(fault=fault["name"]):
                world = edge_fixture_world()
                apply_fault(world, fault)
                errors = edge_errors(*world)
                self.assertTrue(any(fault["expect"] in e for e in errors), f"{fault['name']}: {errors}")

    def test_planted_warnings_are_warnings(self) -> None:
        for case in EDGE_FIXTURES["warnings"]:
            with self.subTest(case=case["name"]):
                world = edge_fixture_world()
                world[0]["staging"].append(copy.deepcopy(case["record"]))
                self.assertTrue(any(case["expect"] in w for w in edge_warnings(world[0], world[1])))


class EdgeDocumentReferenceTests(unittest.TestCase):
    """Every decision, source, claim, record and edge cited in edge-dataset.md exists."""

    def test_cited_ids_exist(self) -> None:
        sources, staging, canonical = load_data()
        known = {s["id"] for s in sources} | {c["id"] for c in staging + canonical}
        known |= {r["id"] for _, r in all_records(load_entities())}
        known |= {e["id"] for _, e in all_edges(load_edges())}
        for ref in sorted(set(re.findall(r"`((?:src|claim|company|technology|component|product|facility|rel)-[a-z0-9-]+)`", EDGES_DOC))):
            with self.subTest(ref=ref):
                self.assertTrue(ref in known, f"{ref} is cited but does not exist")

    def test_cited_decisions_exist(self) -> None:
        from test_entity_taxonomy import decision_exists

        for ref in sorted(set(re.findall(r"\bD-\d{3}\b", EDGES_DOC))):
            with self.subTest(decision=ref):
                self.assertTrue(decision_exists(ref))


if __name__ == "__main__":
    unittest.main()
