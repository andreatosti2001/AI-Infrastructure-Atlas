"""Repository integrity validator (MASTER-ARCHITECTURE.md §14, Gate 0).

Checks the structural invariants established in S00:

- the constitutional documents and baseline architecture record exist;
- every session prompt follows the naming convention and is listed in the
  prompt registry;
- every session report follows the naming convention, has a matching prompt,
  and contains the minimum sections required by SESSION-PROMPT-SPEC.md §5.

It does not validate data: no schema or canonical data exists yet.

Usage: python tools/validate_repo.py [repo_root]
Exit status is 0 when the repository is valid, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FILES = (
    "CLAUDE.md",
    "MASTER-ARCHITECTURE.md",
    "SESSION-PROMPT-SPEC.md",
    "PROJECT-EVALUATION-FRAMEWORK.md",
    "docs/architecture/baseline.md",
    "docs/architecture/decisions.md",
    "sessions/prompts/PROMPT-REGISTRY.md",
)

PROMPTS_DIR = "sessions/prompts"
REPORTS_DIR = "sessions/reports"
REGISTRY_NAME = "PROMPT-REGISTRY.md"

PROMPT_RE = re.compile(r"^S(\d{2})-PROMPT\.md$")
REPORT_RE = re.compile(r"^SESSION-(\d{2})-REPORT\.md$")

# Minimum report fields, SESSION-PROMPT-SPEC.md §5. Each must appear as a
# level-2 heading ("## Mission outcome"); matching is case-insensitive.
REPORT_SECTIONS = (
    "Mission outcome",
    "Files changed",
    "Data changed",
    "Tests run",
    "Evidence added/retired",
    "Decisions made",
    "Deviations",
    "Debt introduced/resolved",
    "Unresolved issues",
    "Process lessons",
    "Implications for the next session",
)


def _h2_headings(text: str) -> set[str]:
    return {
        line[3:].strip().lower()
        for line in text.splitlines()
        if line.startswith("## ")
    }


def validate(root: Path) -> list[str]:
    """Return a list of human-readable errors; empty means valid."""
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    prompts_dir = root / PROMPTS_DIR
    registry = prompts_dir / REGISTRY_NAME
    registry_text = registry.read_text(encoding="utf-8") if registry.is_file() else ""

    prompt_ids: set[str] = set()
    if prompts_dir.is_dir():
        for path in sorted(p for p in prompts_dir.iterdir() if p.is_file()):
            if path.name == REGISTRY_NAME:
                continue
            match = PROMPT_RE.match(path.name)
            if not match:
                errors.append(f"{PROMPTS_DIR}/{path.name}: name must match SNN-PROMPT.md")
                continue
            prompt_ids.add(match.group(1))
            if path.name not in registry_text:
                errors.append(f"{PROMPTS_DIR}/{path.name}: not listed in {REGISTRY_NAME}")

    reports_dir = root / REPORTS_DIR
    if reports_dir.is_dir():
        for path in sorted(p for p in reports_dir.iterdir() if p.is_file()):
            rel = f"{REPORTS_DIR}/{path.name}"
            match = REPORT_RE.match(path.name)
            if not match:
                errors.append(f"{rel}: name must match SESSION-NN-REPORT.md")
                continue
            session_id = match.group(1)
            if session_id not in prompt_ids:
                errors.append(f"{rel}: no matching prompt {PROMPTS_DIR}/S{session_id}-PROMPT.md")
            headings = _h2_headings(path.read_text(encoding="utf-8"))
            for section in REPORT_SECTIONS:
                if section.lower() not in headings:
                    errors.append(f"{rel}: missing section '## {section}'")

    return errors


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
