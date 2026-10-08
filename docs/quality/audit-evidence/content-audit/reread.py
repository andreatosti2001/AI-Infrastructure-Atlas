"""S13 Verifier re-read: find each sampled claim's anchors in freshly retrieved bytes.

Kept with the report (S12 DT-8 pattern). Not a repository tool: PDF text extraction needs
`pypdf`, which is installed only in a scratch virtualenv (S13 Part B §09), and the retrieved
bytes stay outside the repository (RA-4 (4); copyright).

1. Retrieve each registered source cited by a sampled claim with plain `curl` over HTTPS
   (RA-1, RA-2: no changed client identity), into BYTES/<source_id>.bin:
       curl -sS -L --max-time 120 -o BYTES/src-NNN.bin <url>
2. Run this script with that folder: for every citation of every claim in sample.json it
   records the SHA-256 of the bytes, whether they equal the registered retrieval (a full hash
   or the 12-character prefix of the migrated records) and the citation's `read`, and the PDF
   page(s) or HTML document where the anchor is found. A 403 challenge page is an access gap.

Text: HTML is reduced to its text nodes (scripts and styles dropped), entities unescaped,
NFC-normalised, whitespace collapsed; a PDF page is pypdf's extract_text, likewise collapsed.
"exact" means the collapsed anchor is a substring of the collapsed text; "whitespace-insensitive"
means it is only found with all whitespace removed (none in S13).

Usage (from the repository root, in the scratch virtualenv):
    python docs/quality/audit-evidence/content-audit/reread.py BYTES > reread-result.json
"""

from __future__ import annotations

import hashlib
import html
import io
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip -= 1
        self.out.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def pages(raw: bytes) -> list[str]:
    if raw[:4] == b"%PDF":
        import pypdf  # scratch virtualenv only

        return [norm(p.extract_text() or "") for p in pypdf.PdfReader(io.BytesIO(raw)).pages]
    parser = Text()
    parser.feed(raw.decode("utf-8", "replace"))
    return [norm("".join(parser.out))]


def main() -> None:
    folder = Path(sys.argv[1])
    claims = {c["id"]: c for c in json.loads((REPO / "data/claims.json").read_text(encoding="utf-8"))}
    sources = {s["id"]: s for s in json.loads((REPO / "data/sources.json").read_text(encoding="utf-8"))}
    sample = json.loads((HERE / "sample.json").read_text(encoding="utf-8"))
    ids = [c["id"] for c in sample["weight_bearing"]] + [c["id"] for c in sample["drawn"]]
    cache: dict[str, list[str]] = {}
    rows = []
    for cid in ids:
        for n, cit in enumerate(claims[cid].get("citations", []), start=1):
            sid = cit["source_id"]
            raw = (folder / f"{sid}.bin").read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            registered = sources[sid]["retrieval"].get("sha256", "")
            row = {
                "claim": cid,
                "citation": n,
                "source_id": sid,
                "locator": cit["locator"],
                "sha256": digest,
                "equals_registered": digest.startswith(registered) if registered else None,
                "equals_read": digest == cit.get("read", {}).get("sha256"),
            }
            if raw[:4] != b"%PDF" and b"Just a moment" in raw[:4000]:
                row["anchor"] = "access_gap: HTTP 403 challenge page"
                rows.append(row)
                continue
            if sid not in cache:
                cache[sid] = pages(raw)
            anchor = norm(html.unescape(cit["anchor"]))
            hits = [i + 1 for i, t in enumerate(cache[sid]) if anchor in t]
            mode = "exact"
            if not hits:
                squash = re.sub(r"\s+", "", anchor)
                hits = [i + 1 for i, t in enumerate(cache[sid]) if squash in re.sub(r"\s+", "", t)]
                mode = "whitespace-insensitive" if hits else "not_found"
            row["anchor"] = mode
            row["found_on"] = ("pdf_pages", hits) if len(cache[sid]) > 1 else ("html", bool(hits))
            m = re.match(r"p\.(\d+)", cit["locator"])
            if m and len(cache[sid]) > 1:
                row["locator_page_matches"] = int(m.group(1)) in hits
            rows.append(row)
    print(json.dumps(rows, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
