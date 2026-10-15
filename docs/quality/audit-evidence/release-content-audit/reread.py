"""S23 Verifier re-read: find every canonical claim's anchors in freshly retrieved bytes (H-1, D-218).

Not a repository tool and not a check: audit evidence, run once at the audit's base (S13 pattern). The retrieved bytes
stay outside the repository (RA-4 (4); copyright).

1. Retrieve each registered source a canonical claim cites with plain curl over HTTPS (RA-1, RA-2: no changed client
   identity), into BYTES/<source_id>.bin. A refusal (an HTTP 403, a challenge page, an "Access Denied" page) is an
   access gap, recorded with host, status and time in the retrieval log; it is never bypassed.
2. Run this script on that folder. For every citation of every canonical claim it records the SHA-256 of the bytes
   read; whether they equal the source's registered retrieval hash (the full hash, or the 12-character prefix the
   migrated records keep) and the citation's own `read` hash; a SHA-256 of the extracted text (S13 F-6: a dynamic
   page's bytes change while its text may not); and whether the anchor is in that text, and where.

Text. HTML is reduced to its text nodes (scripts and styles dropped), entities unescaped. A PDF's text is poppler's
`pdftotext` (H-1: the machine's PDF tool, not a repository dependency; its version is recorded in the output), one
page per form feed. Every text is NFC-normalised, no-break spaces made spaces, whitespace collapsed. Modes, in order:
"exact" (the collapsed anchor is a substring); "whitespace-insensitive" (found only with all whitespace removed);
"typographic" (found only after folding curly quotes, dashes, ligatures and soft hyphens, and removing whitespace);
otherwise "not_found", which a person then reads at the locator. For a PDF, "pages" lists every page holding the
anchor, and "locator_page_matches" says whether a "p.N" or "page N" in the locator is among them.

Standard library and the system's pdftotext only. Usage (from the repository root):
    python docs/quality/audit-evidence/release-content-audit/reread.py BYTES > reread-result.json
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
GAP_MARKERS = (b"Just a moment", b"Access Denied")
FOLD = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-",
                      "−": "-", "­": None, "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff"})


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        self.out.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


def fold(text: str) -> str:
    return squash(text.translate(FOLD))


def pdftotext_version() -> str:
    done = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True)
    return (done.stderr or done.stdout).splitlines()[0].strip()


def pages(raw: bytes, path: Path) -> list[str]:
    if raw[:4] == b"%PDF":
        done = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"], capture_output=True)
        return [norm(p) for p in done.stdout.decode("utf-8", "replace").split("\f")]
    parser = Text()
    parser.feed(raw.decode("utf-8", "replace"))
    return [norm("".join(parser.out))]


def locator_page(locator: str) -> int | None:
    m = re.search(r"\b(?:p\.|page )\s*(\d+)", locator)
    return int(m.group(1)) if m else None


def find(anchor: str, texts: list[str]) -> tuple[str, list[int]]:
    a = norm(html.unescape(anchor))
    for mode, f in (("exact", lambda s: s), ("whitespace-insensitive", squash), ("typographic", fold)):
        hits = [i + 1 for i, t in enumerate(texts) if f(a) in f(t)]
        if hits:
            return mode, hits
    return "not_found", []


def main() -> None:
    folder = Path(sys.argv[1])
    claims = json.loads((REPO / "data/claims.json").read_text(encoding="utf-8"))
    sources = {s["id"]: s for s in json.loads((REPO / "data/sources.json").read_text(encoding="utf-8"))}
    cache: dict[str, list[str]] = {}
    rows = []
    for claim in claims:
        for n, cit in enumerate(claim.get("citations", []), start=1):
            sid = cit["source_id"]
            path = folder / f"{sid}.bin"
            raw = path.read_bytes() if path.exists() else b""
            registered = sources[sid]["retrieval"].get("sha256", "")
            row = {"claim": claim["id"], "claim_type": claim["claim_type"], "citation": n, "source_id": sid,
                   "locator": cit["locator"]}
            if not raw or (raw[:4] != b"%PDF" and any(m in raw[:4000] for m in GAP_MARKERS)):
                row["anchor"] = "access_gap"
                rows.append(row)
                continue
            digest = hashlib.sha256(raw).hexdigest()
            if sid not in cache:
                cache[sid] = pages(raw, path)
            texts = cache[sid]
            mode, hits = find(cit["anchor"], texts)
            row.update({
                "sha256": digest,
                "equals_registered": digest.startswith(registered) if registered else None,
                "equals_read": digest == cit.get("read", {}).get("sha256") if cit.get("read") else None,
                "text_sha256": hashlib.sha256("\f".join(texts).encode("utf-8")).hexdigest(),
                "anchor": mode,
            })
            if raw[:4] == b"%PDF":
                row["pages"] = hits
                want = locator_page(cit["locator"])
                if want is not None:
                    row["locator_page_matches"] = want in hits
            rows.append(row)
    print(json.dumps({"pdftotext": pdftotext_version(), "citations": rows}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
