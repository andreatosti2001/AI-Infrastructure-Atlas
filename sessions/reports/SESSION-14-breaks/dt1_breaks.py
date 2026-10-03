"""S14 DT-1 deliberate breaks: each edits a fresh copy of the repository and runs the full suite; a break
counts only if the suite fails and the named fragment is in the output. Run from anywhere with the
pinned test environment: python sessions/reports/SESSION-14-breaks/dt1_breaks.py"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]; PY = sys.executable
def rows_edit(fn):
    def apply(root):
        p = root / "data/identity_basis.json"; rows = json.loads(p.read_text()); fn(rows); p.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
    return apply
def doc_edit(path, old, new):
    def apply(root):
        p = root / path; t = p.read_text(); assert old in t; p.write_text(t.replace(old, new, 1))
    return apply
def set_field(kind, record, field, value):
    def fn(rows):
        r = next(r for r in rows if r["kind"] == kind and r.get("record") == record); r[field] = value
    return fn
BREAKS = [
    ("product term changed (H100)", rows_edit(set_field("product_term", "product-nvidia-h100-tensor-core-gpu", "term", "H100 GPU")), "not the vendor's ID plus the slug of its term"),
    ("concept term changed (HBM-02)", rows_edit(lambda rows: next(r for r in rows if r.get("concept") == "HBM-02").update(term="HBM")), "is not the §5 name"),
    ("facility kind basis removed (M16)", rows_edit(lambda rows: rows.remove(next(r for r in rows if r["kind"] == "facility_kind_basis" and r["record"] == "facility-kr-m16"))), "kind wafer_fab has no basis row"),
    ("instance_of basis points elsewhere (Trainium2)", rows_edit(set_field("instance_of_basis", "product-amazon-com-trainium2", "class", "component-data-centre-gpu")), "has basis rows for"),
    ("facility term not in any anchor", rows_edit(set_field("facility_term", "facility-kr-m16", "term", "M 16")), "not facility- plus"),
    ("a gap given a record", rows_edit(lambda rows: next(r for r in rows if r.get("concept") == "HBM-03").update(record="component-hbm-base-die")), "in the concept table but no such record"),
    ("a concept row back in concept-dataset §3", doc_edit("docs/architecture/concept-dataset.md", "To list them: `python -m json.tool data/identity_basis.json`.", "| ACC-02 | Data-centre GPU | `component-data-centre-gpu` | |"), "holds a per-record row again (ACC-02)"),
    ("a legal name restated in company-dataset §2", doc_edit("docs/architecture/company-dataset.md", "| `company-nvidia` | the 10-K registrant.", "| `company-nvidia` | NVIDIA CORPORATION | the 10-K registrant."), "restates the legal name 'NVIDIA CORPORATION'"),
    ("control: a rule sentence in concept-dataset §3 reworded", doc_edit("docs/architecture/concept-dataset.md", "The display name** is free.", "The display name** is free and editorial."), None),
]
for name, apply, want in BREAKS:
    tmp = Path(tempfile.mkdtemp()); root = tmp / "repo"
    shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    apply(root)
    out = subprocess.run([PY, "-m", "unittest", "discover", "-s", "tests"], cwd=root, capture_output=True, text=True)
    text = out.stdout + out.stderr; failed = out.returncode != 0
    if want is None:
        ok = not failed or ("PG-7" in text and text.count("FAIL:") <= 2)
        # a doc that is not a page input changes nothing for the page
        print(f"{'PASS' if not failed else 'FAIL'}  control  {name}  (suite {'passes' if not failed else 'fails'})")
    else:
        print(f"{'CAUGHT' if failed and want in text else 'MISSED'}  {name}  [{want}]  ({text.splitlines()[-1]})")
    shutil.rmtree(tmp)
