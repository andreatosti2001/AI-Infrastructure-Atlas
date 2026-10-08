"""Repository integrity validator (MASTER-ARCHITECTURE.md §14, Gate 0).

Checks the repository's structural invariants (D-151):

- the constitutional documents, the documentation map, the baseline, the decision log and the human
  review record exist;
- every relative link in the repository's Markdown resolves: the file or folder exists, and a fragment
  (`file.md#heading`, `#heading`) names a heading of the target document;
- no session record is in the public tree (D-152): no `sessions/` folder, no session prompt
  (`SNN-PROMPT.md`), session report (`SESSION-NN-REPORT.md`) or prompt registry. They belong in the private
  archive repository (`SESSION-PROMPT-SPEC.md` §5).

Data, schemas, SQL results and pages are validated by the test suite (`tests/`) and the `--check`
commands of `tools/warehouse.py`, `tools/build_page.py` and `tools/build_insight.py`.

Usage: python tools/validate_repo.py [repo_root]
Exit status is 0 when the repository is valid, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FILES = (
    "README.md",
    "CLAUDE.md",
    "MASTER-ARCHITECTURE.md",
    "SESSION-PROMPT-SPEC.md",
    "SESSION-ROADMAP.md",
    "PROJECT-EVALUATION-FRAMEWORK.md",
    "docs/README.md",
    "docs/architecture/baseline.md",
    "docs/architecture/decisions.md",
    "docs/quality/human-reviews.md",
)

# Folders that are not part of the repository's documentation.
SKIPPED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
EXTERNAL_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
SESSION_RECORD_RE = re.compile(r"^(S\d{2}(\.\d+)?-PROMPT|SESSION-\d{2}(\.\d+)?-REPORT|PROMPT-REGISTRY)\.md$")


def heading_anchor(heading: str) -> str:
    """The anchor GitHub gives a heading: lower case, punctuation dropped, spaces as hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def markdown_anchors(text: str) -> set[str]:
    """Every heading anchor of a Markdown document; a repeated heading gets -1, -2, ... as on GitHub."""
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    fenced = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        match = re.match(r"#{1,6} (.+)", line)
        if fenced or not match:
            continue
        base = heading_anchor(match.group(1).replace("`", ""))
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def _markdown_files(root: Path) -> list[Path]:
    out = []
    for path in sorted(root.rglob("*.md")):
        if not SKIPPED_DIRS.intersection(path.relative_to(root).parts):
            out.append(path)
    return out


def _links(text: str):
    """(line number, target) for every Markdown link outside code."""
    fenced = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        for match in LINK_RE.finditer(INLINE_CODE_RE.sub("", line)):
            yield number, match.group(1)


def link_errors(root: Path) -> list[str]:
    errors: list[str] = []
    anchors: dict[Path, set[str]] = {}
    for path in _markdown_files(root):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(root).as_posix()
        for number, target in _links(text):
            if EXTERNAL_RE.match(target):
                continue
            file_part, _, fragment = target.partition("#")
            resolved = (path.parent / file_part).resolve() if file_part else path
            if not resolved.exists():
                errors.append(f"{rel}:{number}: link to a missing file: {target}")
                continue
            if fragment and resolved.suffix == ".md":
                if resolved not in anchors:
                    anchors[resolved] = markdown_anchors(resolved.read_text(encoding="utf-8"))
                if fragment not in anchors[resolved]:
                    errors.append(f"{rel}:{number}: link to a missing heading: {target}")
    return errors


def session_record_errors(root: Path) -> list[str]:
    errors = [f"session record in the public repository (D-152): sessions/"] if (root / "sessions").is_dir() else []
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if SKIPPED_DIRS.intersection(rel.parts) or rel.parts[0] == "sessions":
            continue
        if SESSION_RECORD_RE.match(path.name):
            errors.append(f"session record in the public repository (D-152): {rel.as_posix()}")
    return errors


def validate(root: Path) -> list[str]:
    """Return a list of human-readable errors; empty means valid."""
    errors = [f"missing required file: {rel}" for rel in REQUIRED_FILES if not (root / rel).is_file()]
    return errors + session_record_errors(root) + link_errors(root)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent
    errors = validate(root)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"Repository integrity: FAILED ({len(errors)} error(s))")
        return 1
    print("Repository integrity: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
