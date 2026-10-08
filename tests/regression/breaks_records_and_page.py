"""Breaks for the records and the HBM page: data integrity, refused candidates, the page's checks (D-109 to D-111).

Each break copies the repository (without .git) into a scratch folder, makes one edit, optionally rebuilds the
page, runs the full unit suite, and passes only if the suite fails AND every expected fragment appears in its
output (the break fails for the reason it names). A control passes only if the suite passes.

A layer of the full harness: run it through `tests/regression/breaks.py`, which replaces the breaks whose
setup text later changes removed. Run alone, some of this layer's breaks no longer apply.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PAGE = "site/hbm-chain/index.html"


def edit(root: Path, rel: str, old: str, new: str, count: int = 1) -> None:
    p = root / rel
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"break setup: {old!r} not in {rel}")
    p.write_text(text.replace(old, new, count), encoding="utf-8")


def jedit(root: Path, rel: str, fn) -> None:
    p = root / rel
    data = json.loads(p.read_text(encoding="utf-8"))
    fn(data)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cand(data, cid):
    return next(c for c in data if c["id"] == cid)


def move_to_staging(root: Path, kind: str, rid: str) -> None:
    canon = json.loads((root / f"data/{kind}.json").read_text(encoding="utf-8"))
    rec = next(r for r in canon if r["id"] == rid)
    canon.remove(rec)
    (root / f"data/{kind}.json").write_text(json.dumps(canon, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    stag = json.loads((root / f"data/staging/{kind}.json").read_text(encoding="utf-8"))
    stag.append(rec)
    (root / f"data/staging/{kind}.json").write_text(json.dumps(stag, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def remove_last_card(root: Path, cid: str) -> None:
    p = root / PAGE
    text = p.read_text(encoding="utf-8")
    cards = list(re.finditer(rf'<li class="card" data-candidate="{cid}">.*?</li>', text, re.S))
    if len(cards) < 2:
        raise SystemExit(f"break setup: {cid} has {len(cards)} cards")
    last = cards[-1]
    p.write_text(text[: last.start()] + text[last.end():], encoding="utf-8")


def remove_rule_definition(root: Path, code: str) -> None:
    p = root / PAGE
    text = p.read_text(encoding="utf-8")
    new, n = re.subn(rf'<div><dt><strong data-ref="doc:rules#{code}".*?</dd></div>', "", text, count=1, flags=re.S)
    if not n:
        raise SystemExit(f"break setup: no definition of {code}")
    p.write_text(new, encoding="utf-8")


EDGE_DESIGNS = "rel-company-amazon-com-designs-product-amazon-com-trainium2"

# (id, what, edit, rebuild, expected fragments; [] with control=True means the suite must pass)
BREAKS = [
    ("1", "a mark with no record behind it",
     lambda r: edit(r, PAGE, 'data-ref="component-high-bandwidth-memory"', 'data-ref="company-example-nothing"'),
     False, ["test_pg3", "company-example-nothing"]),
    ("2", "a hand-edited label (NVIDIA H100 -> H200)",
     lambda r: edit(r, PAGE, ">NVIDIA H100<", ">NVIDIA H200<"),
     False, ["test_pg2", "NVIDIA H200"]),
    ("4", "a supplier gap drawn as zero",
     lambda r: edit(r, PAGE, 'data-format="state">not researched<', 'data-format="state">0<'),
     False, ["test_pg2", "'0'"]),
    ("5", "a staging edge on the page (not rebuilt)",
     lambda r: move_to_staging(r, "relationships", EDGE_DESIGNS),
     False, ["test_pg3", EDGE_DESIGNS]),
    ("7", "a changed claim statement, not rebuilt",
     lambda r: jedit(r, "data/claims.json", lambda d: next(c for c in d if c["id"] == "claim-h100-hbm-stacks").update(
         statement="NVIDIA states that the H100 supports 96 GB of HBM3 memory.")),
     False, ["test_pg2", "claim-h100-hbm-stacks"]),
    ("8", "an anchor that no longer matches (page only)",
     lambda r: edit(r, PAGE, "raises the bar", "lowers the bar"),
     False, ["test_pg2", "lowers the bar"]),
    ("10", "an evidence panel removed",
     lambda r: edit(r, PAGE, f'id="ev-{EDGE_DESIGNS}"', 'id="ev-removed"'),
     False, ["test_pg3"]),
    ("11", "a build that stamps the clock (rebuilt)",
     lambda r: edit(r, "tools/build_page.py", 'parts["palette"] =', 'parts["palette"] = f"/* {__import__(\'time\').time_ns()} */ " +'),
     True, ["test_pg7"]),
    ("12", "framing that names a record (rebuilt)",
     lambda r: edit(r, "tools/page_template.html", "it states no fact about the world.",
                    "it states no fact about the world, unlike SK hynix."),
     True, ["test_pg6", "SK hynix"]),
    ("13", "'none' for a missing relationship",
     lambda r: edit(r, PAGE, '>no recorded relationship</span>', '>none</span>'),
     False, ["none"]),
    ("15", "a script fetched from the network",
     lambda r: edit(r, PAGE, "</body>", '<script src="https://example.com/x.js"></script></body>'),
     False, ["test_pg9", "<script>"]),
    ("16", "a hover-only rule (rebuilt)",
     lambda r: edit(r, "tools/page_template.html", ".framing {", "li.card:hover { color: var(--ink-strong); }\n.framing {"),
     True, ["test_pg8", "li.card:hover"]),
    ("17", "a text colour below WCAG AA (rebuilt)",
     lambda r: edit(r, "tools/build_page.py", '"ink-muted": "#4d5865"', '"ink-muted": "#b0b6bd"'),
     True, ["test_pg8", "not greater than or equal to 4.5"]),
    ("21", "a journey candidate moved to staging (not rebuilt)",
     lambda r: move_to_staging(r, "refused_candidates", "cand-002"),
     False, ["cand-002"]),
    ("22", "a no-record name that is a record's name (ASML)",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-004")["source_entities"][0].update(name="ASML")),
     False, ["names a record (company-asml-holding)"]),
    ("23", "an item with no record, its reason dropped",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-004")["reasons"].remove("item_has_no_record")),
     False, ["item_has_no_record is not a reason"]),
    ("25", "a stored status on a candidate (RR-6)",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-001").update(status="refused")),
     False, ["'status' was unexpected"]),
    ("26", "a reasoning that quotes a rule with no home",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-005").update(
         reasoning=cand(d, "cand-005")["reasoning"] + " (ER-99)")),
     False, ["ER-99"]),
    ("6", "a DERIVATION drawn as stated",
     lambda r: edit(r, PAGE, 'data-target="claim-tsmc-fabricates-h100" data-basis="inferred"', 'data-target="claim-tsmc-fabricates-h100" data-basis="stated"'),
     False, ["test_pg4"]),
    ("9", "a mark unreachable by keyboard",
     lambda r: edit(r, PAGE, '<a class="mark edge" href=', '<a class="mark edge" tabindex="-1" href='),
     False, ["test_pg8"]),
    ("18", "a quoted rule code whose definition is removed",
     lambda r: remove_rule_definition(r, "ER-9"),
     False, ["test_pg10", "ER-9"]),
    ("19", "a refused candidate referenced in the diagram",
     lambda r: edit(r, PAGE, '<a class="mark gap inferred" href="#ev-claim-tsmc-fabricates-h100"',
                    '<a class="mark gap inferred" data-candidate="cand-002" href="#ev-claim-tsmc-fabricates-h100"'),
     False, ["test_pg5"]),
    ("20", "a card removed from one of its reason groups",
     lambda r: remove_last_card(r, "cand-002"),
     False, ["test_pg5_candidates_are_cards_never_lines"]),
    ("24", "a sentence used by an edge and refused (Amazon designs Trainium2)",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-008").update(
         considered=[{"claim_id": "claim-aws-designed-trainium2"}])),
     False, ["claim-aws-designed-trainium2 supports"]),
    ("27", "a candidate given an edge's ID",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-001").update(id="rel-company-x-supplies-company-y")),
     False, ["test_rc1"]),
    # S13, D-111
    ("S13-1", "Samsung removed from the page's card by hand (not rebuilt)",
     lambda r: edit(r, PAGE, 'data-field="/source_entities/2/name">Samsung</span>', 'data-field="/source_entities/2/name"></span>', 2),
     False, ["test_pg2", "cand-002"]),
    ("S13-2", "Samsung kept, its reason dropped",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-002")["reasons"].remove("endpoint_has_no_record")),
     False, ["cand-002: an endpoint has no record, but endpoint_has_no_record is not a reason"]),
    ("S13-3", "Samsung's no-record name replaced by a record's name (SK hynix)",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-002")["source_entities"][2].update(name="SK hynix")),
     False, ["no_record 'SK hynix' names a record"]),
    ("S13-4", "Samsung's no-record name replaced by a placeholder",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: cand(d, "cand-002")["source_entities"][2].update(name="unknown")),
     False, ["placeholder"]),
    ("S13-5", "Samsung dropped from the data, page not rebuilt",
     lambda r: jedit(r, "data/refused_candidates.json", lambda d: (cand(d, "cand-002")["source_entities"].pop(),
                                                                    cand(d, "cand-002")["reasons"].remove("endpoint_has_no_record"))),
     False, ["test_pg7"]),
    ("C", "control: README edited",
     lambda r: edit(r, "README.md", "# AI-Infrastructure-Atlas", "# AI-Infrastructure-Atlas (control)"),
     False, []),
    ("D", "control: edge-dataset.md prose edited",
     lambda r: edit(r, "docs/architecture/edge-dataset.md", "#", "# ", 1),
     False, []),
]


def run(scratch: Path, wanted: set[str]) -> int:
    py = sys.executable
    bad = 0
    for bid, what, mutate, rebuild, expected in BREAKS:
        if wanted and bid not in wanted:
            continue
        root = scratch / f"break-{bid}"
        if root.exists():
            shutil.rmtree(root)
        shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git"))
        mutate(root)
        if rebuild:
            built = subprocess.run([py, "tools/build_page.py"], cwd=root, capture_output=True, text=True)
            if built.returncode:
                print(f"{bid:6} {'BUILD FAILED':24} {what} | {built.stderr.strip().splitlines()[-1]}")
                bad += 1
                shutil.rmtree(root)
                continue
        res = subprocess.run([py, "-m", "unittest", "discover", "-s", "tests"], cwd=root, capture_output=True, text=True)
        out = res.stdout + res.stderr
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", out, re.M)))
        if not expected:
            ok = res.returncode == 0
            verdict = "passes, as it must" if ok else "CONTROL FAILED"
        else:
            missing = [f for f in expected if f not in out]
            ok = res.returncode != 0 and not missing
            verdict = "caught" if ok else f"NOT CAUGHT as named (missing {missing})"
        bad += not ok
        print(f"{bid:6} {verdict:24} {what} | failed: {', '.join(failed) or '-'}")
        shutil.rmtree(root)
    return bad


if __name__ == "__main__":
    sys.exit(1 if run(Path(sys.argv[1]), set(sys.argv[2:])) else 0)
