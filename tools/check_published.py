"""The published address serves the release commit's pages and the files they link to (S25, D-226, D-227).

v1.0's pages are published with the repository's tracked files at one address, so that each relative link a page
makes (to a record, a review entry, a query, a schema) opens the file it names. This check reads the address and
compares what it serves with the files of the commit it runs on, byte for byte:

- PA-1 each page under `site/` is served at its path under the address and equals the committed page;
- PA-2 each file a page links to by a relative link is served and equals the committed file.

Run it from a checkout of the release commit: when it passes, the published pages are that commit's build, and
`tools/check_all.py` on the same commit shows the build equals a fresh rebuild. Each failure is listed by name; the
media type each kind of file is served with is printed too, for the record (a browser shows some kinds as text and
offers others as downloads).

Usage: python tools/check_published.py BASE_URL      (the address the repository's root is served at)
Exit status 0 when every page and every linked file matches, 1 otherwise, 2 on a usage error. Standard library only.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HREF = re.compile(r'(?:href|src)="([^"]*)"')
EXTERNAL = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
TIMEOUT = 30


def pages() -> list[str]:
    """Every page under site/, as a repository path."""
    return sorted(str(p.relative_to(REPO_ROOT)) for p in (REPO_ROOT / "site").rglob("*.html"))


def targets() -> list[str]:
    """Every file a page links to by a relative link, other than the pages themselves, as a repository path."""
    found = set()
    for page in pages():
        for href in HREF.findall((REPO_ROOT / page).read_text(encoding="utf-8")):
            if href.startswith("#") or EXTERNAL.match(href):
                continue
            found.add(os.path.normpath(os.path.join(os.path.dirname(page), href.split("#")[0])))
    return sorted(found - set(pages()))


def fetch(base: str, rel: str) -> tuple[bytes | None, str]:
    """The bytes served for a repository path and their media type, or None and the reason nothing was served."""
    url = urllib.parse.urljoin(base, urllib.parse.quote(rel))
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            return response.read(), response.headers.get_content_type()
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except (urllib.error.URLError, OSError) as e:
        return None, f"no answer: {getattr(e, 'reason', e)}"


def check(base: str) -> dict:
    """Compare what `base` serves with the committed files; the failures by name and the media types seen."""
    base = base if base.endswith("/") else base + "/"
    failures: list[str] = []
    media: dict[str, set[str]] = {}
    for rule, paths, what in (("PA-1", pages(), "page"), ("PA-2", targets(), "file")):
        for rel in paths:
            body, kind = fetch(base, rel)
            if body is None:
                failures.append(f"{rule} {rel}: not served ({kind})")
                continue
            media.setdefault(Path(rel).suffix, set()).add(kind)
            if body != (REPO_ROOT / rel).read_bytes():
                failures.append(f"{rule} {rel}: served bytes differ from the committed {what}")
    return {"base": base, "pages": len(pages()), "files": len(targets()), "failures": failures,
            "media_types": {k: sorted(v) for k, v in sorted(media.items())}}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: python tools/check_published.py BASE_URL", file=sys.stderr)
        return 2
    result = check(argv[0])
    print(f"{result['base']}: {result['pages']} pages and {result['files']} linked files compared with the commit")
    for suffix, kinds in result["media_types"].items():
        print(f"  served {suffix} as {', '.join(kinds)}")
    if result["failures"]:
        print(f"FAIL: {len(result['failures'])} difference(s):\n- " + "\n- ".join(result["failures"]))
        return 1
    print("every page and every linked file equals the commit")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
