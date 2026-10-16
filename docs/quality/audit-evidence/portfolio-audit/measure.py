"""S24 measures: the roadmap's eight capability points and PEF §4's retrospective items, counted (portfolio audit).

Every number in measures.json is counted from the repository at the audit's base: its Git history, the canonical
records, the documents, the checks and the generated pages. With --archive, it also counts the private development
archive's prompts and reports; it copies no text from them (D-152), only counts. The readings of the numbers are the
audit's (INTERPRETATION). The output records the commits it read and the SHA-256 of every file it read, so a re-run
on a later tree shows that it differs; it never reads the clock.

What each section counts, and its population and denominator, is stated beside it in the output ("population").

Standard library, plus the contract test's helpers, imported read-only. Usage (from the repository root):
    python docs/quality/audit-evidence/portfolio-audit/measure.py [--archive PATH] > .../measures.json
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import html.parser
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tests"))

import test_agent_contracts as tac  # noqa: E402

READ: dict[str, str] = {}

CONSTITUTION = ["CLAUDE.md", "MASTER-ARCHITECTURE.md", "PROJECT-EVALUATION-FRAMEWORK.md", "SESSION-PROMPT-SPEC.md",
                "SESSION-ROADMAP.md", "VERSION-ROADMAP.md"]
# Internal codes a first-time reader cannot decode without the project's records: decision, session, milestone and
# rule or finding identifiers (P-4, the cold readers' observation). Legal citations (§ 730.1), standard codes (ISO
# 3166-2 KR-41) and SHA-256 are not internal and are left out; a section sign is counted separately.
CODE = re.compile(r"(?<![\w-])(?:D-\d{3}|S\d{2}(?:\.\d)?|M\d|[A-Z]{1,4}-\d{1,3}[a-z]?)(?![\w-])")
NOT_INTERNAL = re.compile(r"^(?:SHA|KR|US|EU|CN|TW|JP|ISO|HBM|DDR|ECCN)-")
SECTION_SIGN = re.compile(r"§\s?\d")
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
SESSION = re.compile(r"^(S\d{2}(?:\.\d)?)\b")


def read(path: str) -> str:
    text = (REPO / path).read_text(encoding="utf-8")
    READ[path] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text


def git(*args: str, cwd: Path = REPO) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def items(blob):
    """A data file's records: the file is a list, or an object holding one list."""
    return blob[next(iter(blob))] if isinstance(blob, dict) else blob


def kind(path: str) -> str:
    if path.startswith(("site/", "sql/results/")):
        return "generated"
    if path.startswith("data/"):
        return "data"
    if path.endswith(".md"):
        return "docs"
    return "code"


def commits() -> list[dict]:
    """Every commit reachable from HEAD, oldest first: author, date, subject, parents, files with lines added."""
    out = git("log", "--reverse", "--format=%x1e%H%x1f%P%x1f%an%x1f%aI%x1f%s", "--numstat", "-m", "--first-parent")
    result = []
    for block in out.split("\x1e")[1:]:
        head, _, body = block.partition("\n")
        sha, parents, author, date, subject = head.split("\x1f")
        files = []
        for line in body.splitlines():
            parts = line.split("\t")
            if len(parts) == 3:
                added = int(parts[0]) if parts[0].isdigit() else 0
                files.append((parts[2], added))
        result.append({"sha": sha, "parents": parents.split(), "author": author, "date": date[:10],
                       "subject": subject, "files": files})
    return result


def no_merge_commits() -> list[dict]:
    """Non-merge commits reachable from HEAD, oldest first, with the files each changed (lines added)."""
    out = git("log", "--reverse", "--no-merges", "--format=%x1e%H%x1f%an%x1f%aI%x1f%s", "--numstat")
    result = []
    for block in out.split("\x1e")[1:]:
        head, _, body = block.partition("\n")
        sha, author, date, subject = head.split("\x1f")
        files = []
        for line in body.splitlines():
            parts = line.split("\t")
            if len(parts) == 3:
                files.append((parts[2], int(parts[0]) if parts[0].isdigit() else 0))
        result.append({"sha": sha, "author": author, "date": date[:10], "subject": subject, "files": files})
    return result


class Text(html.parser.HTMLParser):
    """The text of a page, every element included (disclosures closed or open), scripts and styles left out."""

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def page_text(path: str) -> str:
    p = Text()
    p.feed(read(path))
    return re.sub(r"\s+", " ", " ".join(p.parts))


def code_density(text: str) -> dict:
    words = len(WORD.findall(text))
    codes = [c for c in CODE.findall(text) if not NOT_INTERNAL.match(c)]
    return {"words": words, "internal_codes": len(codes), "per_1000_words": round(1000 * len(codes) / words, 1),
            "section_signs": len(SECTION_SIGN.findall(text)),
            "most_frequent": collections.Counter(codes).most_common(12)}


def decisions() -> list[dict]:
    text = read("docs/architecture/decisions.md")
    result = []
    for part in re.split(r"^## (?=D-\d{3} )", text, flags=re.M)[1:]:
        did = part[:5]
        status = re.search(r"\*\*Status:\*\*(.*?)(?:\n- \*\*|\Z)", part, flags=re.S)
        status = re.sub(r"\s+", " ", status.group(1)) if status else ""
        date = re.search(r"\*\*Date:\*\* (\d{4}-\d{2}-\d{2})", part)
        result.append({"id": did, "date": date.group(1) if date else None, "status": status,
                       "rejected": "**Rejected" in part, "context": "**Context" in part,
                       "amends": sorted(set(re.findall(r"(?:amends|supersed\w*|replaces|reverses)(?: in part)?(?: by)? (D-\d{3})", part)))})
    return result


def harness() -> dict:
    """The break harness's entries, by the harness's own list (tests/regression/breaks.py): faults expect fragments in
    the suite's failure; controls expect none (the suite must pass)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("breaks", REPO / "tests/regression/breaks.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    entries = mod.breaks()
    controls = [b[0] for b in entries if not b[4]]
    prefix = collections.Counter(re.match(r"(S\d{2}(?:\.\d)?|D\d{3}|[A-Z]+)", b[0]).group(1) for b in entries)
    return {"entries": len(entries), "faults": len(entries) - len(controls), "controls": len(controls),
            "by_id_prefix": dict(sorted(prefix.items()))}


def capabilities(data: dict, decs: list[dict], tracked: list[str]) -> dict:
    claims, sources = data["claims"], data["sources"]
    tests = {p: read(p) for p in tracked if re.fullmatch(r"tests/test_[a-z_]+\.py", p)}
    test_count = sum(len(re.findall(r"^\s+def test_\w+", t, flags=re.M)) for t in tests.values())
    sql = sorted(p for p in tracked if re.fullmatch(r"sql/[a-z_]+\.sql", p))
    sql_head = {p: read(p).split("\n\n", 1)[0] for p in sql}
    tools = sorted(p for p in tracked if re.fullmatch(r"tools/[a-z_]+\.py", p))
    tool_text = {p: read(p) for p in tools}
    third_party = {p: sorted(set(re.findall(r"^\s*(?:import|from) (duckdb|jsonschema|requests|numpy|pandas)\b", t, flags=re.M)))
                   for p, t in tool_text.items()}
    pages = sorted(p for p in tracked if p.startswith("site/") and p.endswith("index.html"))
    page_html = {p: read(p) for p in pages}
    tutorials = {p: len(re.findall(r'class="sql-tutorial"', h)) for p, h in page_html.items()}
    digests = sum(1 for h in page_html.values() if 'data-derived="input-digest"' in h)
    questions = {p: bool(re.search(r"<h1[^>]*>[^<]*\?\s*</h1>", re.sub(r"<(?!/?h1)[^>]+>", "", h))) for p, h in page_html.items()}
    roles = tac.role_rows()
    contracts = tac.contracts()
    reviews = read("docs/quality/human-reviews.md")
    review_rows = re.findall(r"^\| \[[^\]]+\]\(#[^)]+\) \| (\d{4}-\d{2}-\d{2}) \| (\d+) \|", reviews, flags=re.M)
    human_status = [d for d in decs if re.search(r"\bhuman\b", d["status"])]
    for p in tracked:
        if p.startswith("tests/regression/") and p.endswith(".py"):
            read(p)
    permanent = re.search(r"PERMANENT\s*=\s*\(?\[?([^\]\)]*)", read("tests/test_planted_faults.py"))
    ci = read(".github/workflows/ci.yml")
    reqs = read("requirements-test.txt") + read("requirements-analysis.txt")
    brief = page_text("site/briefs/accelerator-memory/index.html")
    readme = read("README.md")
    brief_html = page_html["site/briefs/accelerator-memory/index.html"]
    h2 = [re.sub(r"<[^>]+>", "", m) for m in re.findall(r"<h2[^>]*>(.*?)</h2>", brief_html)]
    first_h2 = brief.find("Question and scope")
    summary_at = brief.find("Executive summary")
    doc_files = sorted(p for p in tracked if p.endswith(".md"))
    return {
        "1_domain_expertise": {
            "population": "canonical records at the base",
            "claims_by_type": dict(sorted(collections.Counter(c["claim_type"] for c in claims).items())),
            "sources_by_class": dict(sorted(collections.Counter(s["source_class"] for s in sources).items())),
            "refused_candidates": len(data["refused_candidates"]),
            "records_by_kind": {k: len(v) for k, v in sorted(data.items())},
        },
        "2_data_engineering": {
            "population": "tracked files at the base",
            "schemas": len([p for p in tracked if p.startswith("schemas/") and p.endswith(".json")]),
            "test_modules": len(tests), "test_methods_declared": test_count,
            "builds_with_check": len(re.findall(r'"--check"', read("tools/check_all.py"))),
            "break_harness": harness(),
            "permanent_breaks_listed": len(re.findall(r'"[A-Z0-9.]+-[A-Z0-9]+"', permanent.group(1))) if permanent else None,
        },
        "3_sql_python": {
            "population": "sql/*.sql and tools/*.py at the base; the 18 generated pages",
            "queries": len(sql),
            "queries_whose_header_states_question_population_denominator": sum(
                1 for h in sql_head.values() if all(w in h.lower() for w in ("question", "population", "denominator"))),
            "query_header_words": {p: [w for w in ("question", "population", "denominator", "does not prove") if w in h.lower()] for p, h in sql_head.items()},
            "tools": len(tools), "tool_lines": sum(t.count("\n") for t in tool_text.values()),
            "tools_importing_a_third_party_package": {p: v for p, v in third_party.items() if v},
            "pages_with_a_sql_tutorial": {p: n for p, n in tutorials.items() if n},
        },
        "4_ai_governance_agents": {
            "population": "docs/agents/roles.md rows; contracts.md; decisions.md D-001 to the last; human-reviews.md index",
            "roles": len(roles), "roles_active": sum(1 for r in roles if r[1] == "active"),
            "contracts": len(contracts),
            "contracts_with_all_nine_ma_fields": sum(1 for c in contracts.values() if list(c) == tac.ma_fields()),
            "decisions": len(decs), "decisions_whose_status_names_the_human": len(human_status),
            "human_review_entries": len(review_rows), "claims_in_review_entries": sum(int(n) for _, n in review_rows),
            "canonical_claims": len(claims),
            "canonical_claims_reviewed_by_the_human": sum(1 for c in claims if c.get("review", {}).get("reviewer") == "human"),
        },
        "5_policy_analysis": {
            "population": "canonical records; docs/research/change-detection.md; docs/research/search-logs/later-rules/",
            "policies": len(data["policies"]),
            "events_by_kind": dict(sorted(collections.Counter(e.get("event_type") for e in data["events"]).items())),
            "relationships_by_type": dict(sorted(collections.Counter(r["relation_type"] for r in data["relationships"]).items())),
            "claims_interpretation_or_implication": sum(1 for c in claims if c["claim_type"] in {"INTERPRETATION", "IMPLICATION"}),
            "later_rule_search_logs": len([p for p in tracked if p.startswith("docs/research/search-logs/later-rules/")]),
        },
        "6_reproducibility": {
            "population": "the 18 generated pages; CI; the pins",
            "pages": len(pages), "pages_with_input_digest": digests,
            "requirements_pinned_exactly": len(re.findall(r"^[A-Za-z0-9_.-]+==", reqs, flags=re.M)),
            "requirements_unpinned": len(re.findall(r"^[A-Za-z0-9_.-]+(?:>=|~=|<|>)?\s*$", reqs, flags=re.M)),
            "ci_actions_pinned_by_commit": len(re.findall(r"uses: [\w./-]+@[0-9a-f]{40}", ci)),
            "ci_actions_pinned_by_tag": len(re.findall(r"uses: [\w./-]+@v\d", ci)),
            "readme_mentions_ci_status_badge": "badge" in readme.lower() or "shields.io" in readme,
            "pages_published": "not published" not in readme,
        },
        "7_client_value": {
            "population": "the client brief, site/briefs/accelerator-memory/index.html, and the 18 pages",
            "briefs": len([p for p in pages if p.startswith("site/briefs/")]),
            "brief_sections": h2,
            "brief_words": len(WORD.findall(brief)),
            "words_before_question_and_scope": len(WORD.findall(brief[:first_h2])),
            "words_before_executive_summary": len(WORD.findall(brief[:summary_at])),
            "pages_whose_h1_is_a_question": sum(questions.values()),
            "records_of_a_reader_outside_the_project": "none found in the repository (searched: README, docs, decisions)",
        },
        "8_documentation_quality": {
            "population": "tracked .md files; decisions.md; the README and the brief's text",
            "markdown_files": len(doc_files),
            "decisions_with_context": sum(1 for d in decs if d["context"]),
            "decisions_with_rejected_alternatives": sum(1 for d in decs if d["rejected"]),
            "readme_internal_code_density": code_density(readme),
            "brief_internal_code_density": code_density(brief),
        },
    }


def retrospective(log: list[dict], first_parent: list[dict], decs: list[dict], tracked: list[str]) -> dict:
    by_session: dict[str, dict] = collections.defaultdict(lambda: collections.Counter())
    session_dates: dict[str, set] = collections.defaultdict(set)
    for c in log:
        m = SESSION.match(c["subject"])
        s = m.group(1) if m else ("human upload or edit" if c["author"] != "Claude" else "unlabelled (decision or governance commit)")
        by_session[s]["commits"] += 1
        session_dates[s].add(c["date"])
        for path, added in c["files"]:
            by_session[s][f"lines_added_{kind(path)}"] += added
    days = sorted({c["date"] for c in log})
    merges = [c for c in first_parent if len(c["parents"]) > 1]
    human_merges = [c for c in merges if c["author"] != "Claude" and c["subject"].startswith("Merge pull request")]
    authored = collections.Counter(kind(p) for c in log if c["author"] == "Claude" for p, _ in c["files"])
    added = collections.Counter()
    for c in log:
        for path, n in c["files"]:
            added[(c["author"] == "Claude", kind(path))] += n

    # 1. repeated rework: decisions that amend or supersede earlier ones; the most-changed authored files;
    #    commits that only rebuild pages for their input digest.
    churn = collections.Counter(p for c in log for p, _ in c["files"] if kind(p) in {"code", "docs"})
    digest_only = [c for c in log if re.search(r"rebuilt for (?:their|the) input digest", c["subject"])]
    # 2. duplicated abstractions: top-level functions defined with the same name in two or more tools.
    defs = collections.defaultdict(list)
    for p in tracked:
        if re.fullmatch(r"tools/[a-z_]+\.py", p):
            for name in re.findall(r"^def (\w+)\(", read(p), flags=re.M):
                defs[name].append(p)
    dup = {n: ps for n, ps in sorted(defs.items()) if len(ps) > 1}
    # 3. drift: commits that change a constitutional document, and whether they name a decision (subject) or append
    #    one (decisions.md in the same commit), or were the human's own edit.
    const = []
    for c in log:
        touched = sorted(p for p, _ in c["files"] if p in CONSTITUTION)
        if touched:
            const.append({"sha": c["sha"][:7], "date": c["date"], "author": "human" if c["author"] != "Claude" else "Claude",
                          "files": touched, "decision_named_or_appended": bool(re.search(r"D-\d{3}", c["subject"])) or any(p == "docs/architecture/decisions.md" for p, _ in c["files"])})
    # 4. agent overlap: tracked files that two or more contracts' allowed writes name.
    contracts = tac.contracts()
    owners = collections.defaultdict(list)
    for role, c in contracts.items():
        pats = re.findall(r"`([^`]+)`", c["ALLOWED_WRITES"])
        for f in tracked:
            if tac.owned(f, pats):
                owners[f].append(role)
    overlap = {f: sorted(r) for f, r in sorted(owners.items()) if len(r) > 1}
    # 5. schema changes: commits that change schemas/, and whether each names or appends a decision.
    schema = [{"sha": c["sha"][:7], "date": c["date"],
               "decision_named_or_appended": bool(re.search(r"D-\d{3}", c["subject"])) or any(p == "docs/architecture/decisions.md" for p, _ in c["files"])}
              for c in log if any(p.startswith("schemas/") for p, _ in c["files"])]
    # 6. content churn: every ID ever present in the canonical claims and sources files, against the IDs present now.
    ever = {"data/claims.json": set(), "data/sources.json": set()}
    statement = collections.defaultdict(set)
    for c in log:
        for path in ever:
            if any(p == path for p, _ in c["files"]):
                try:
                    blob = json.loads(git("show", f"{c['sha']}:{path}"))
                except (subprocess.CalledProcessError, json.JSONDecodeError):
                    continue
                for it in items(blob):
                    ever[path].add(it["id"])
                    if path == "data/claims.json":
                        statement[it["id"]].add(it.get("statement"))
    now = {path: {it["id"] for it in items(json.loads(read(path)))} for path in ever}
    # 7. tests after regressions: test changes in commits whose subject names a fix, a red CI or a regression;
    #    decisions that mention a red CI.
    fix_tests = [c["sha"][:7] for c in log if re.search(r"\bfix|red CI|regression|repair", c["subject"], flags=re.I)
                 and any(p.startswith("tests/") for p, _ in c["files"])]
    red_ci_decisions = [d["id"] for d in decs if re.search(r"red CI|CI (?:was|went|turned) red|CI red", read_decision(d["id"]))]
    # 8. features without a journey: queries whose result no page shows; tools that no check, build or CI runs.
    site = "".join(read(p) for p in tracked if p.startswith("site/") and p.endswith(".html"))
    queries = sorted(Path(p).stem for p in tracked if re.fullmatch(r"sql/[a-z_]+\.sql", p))
    shown = {q: (f'data-query="{q}"' in site) for q in queries}
    runners = "".join(read(p) for p in tracked if p.startswith(("tests/", "tools/", ".github/")) and p.endswith((".py", ".yml", ".js")))
    tools = sorted(p for p in tracked if re.fullmatch(r"tools/[a-z_]+\.py", p))
    unused = [p for p in tools if Path(p).stem not in runners.replace(p, "")]
    claim_ids = now["data/claims.json"]
    on_page = {c for c in claim_ids if c in site}
    return {
        "population": "commits reachable from HEAD (non-merge unless stated); decisions.md; tracked files at the base",
        "calendar_days_with_commits": len(days), "first_commit_date": days[0], "last_commit_date": days[-1],
        "non_merge_commits": len(log), "first_parent_merges": len(merges), "pull_requests_merged_by_the_human": len(human_merges),
        "lines_added_by_kind": {("Claude" if k[0] else "human") + "_" + k[1]: v for k, v in sorted(added.items())},
        "files_touched_by_kind_in_claude_commits": dict(sorted(authored.items())),
        "sessions": {s: dict(sorted(v.items())) | {"days": sorted(session_dates[s])} for s, v in sorted(by_session.items())},
        "decisions_by_date": dict(sorted(collections.Counter(d["date"] for d in decs).items())),
        "1_repeated_rework": {
            "decisions_superseded": [d["id"] for d in decs if d["status"].startswith(" superseded")],
            "decisions_that_amend_or_supersede_another": sum(1 for d in decs if d["amends"]),
            "most_changed_authored_files": churn.most_common(12),
            "commits_that_rebuild_pages_for_their_input_digest_only": len(digest_only),
        },
        "2_duplicated_abstractions": {"functions_defined_in_two_or_more_tools": dup,
                                       "templates": len([p for p in tracked if re.fullmatch(r"tools/[a-z_]+_template\.html", p)]),
                                       "page_builds": len([p for p in tracked if re.fullmatch(r"tools/build_[a-z_]+\.py", p)])},
        "3_architecture_drift": {"commits_changing_a_constitutional_document": const,
                                 "of_which_by_claude_without_a_decision": sum(1 for c in const if c["author"] == "Claude" and not c["decision_named_or_appended"])},
        "4_agent_overlap": {"tracked_files_owned_by_two_or_more_roles": overlap, "tracked_files": len(tracked)},
        "5_schema_changes": {"commits_changing_schemas": len(schema),
                             "without_a_decision_named_or_appended": [c for c in schema if not c["decision_named_or_appended"]]},
        "6_content_churn": {
            "claim_ids_ever_canonical": len(ever["data/claims.json"]), "claim_ids_now": len(now["data/claims.json"]),
            "claim_ids_removed": sorted(ever["data/claims.json"] - now["data/claims.json"]),
            "claims_whose_statement_changed_under_the_same_id": sorted(i for i, s in statement.items() if len(s) > 1),
            "source_ids_ever_canonical": len(ever["data/sources.json"]), "source_ids_now": len(now["data/sources.json"]),
            "source_ids_removed": sorted(ever["data/sources.json"] - now["data/sources.json"]),
        },
        "7_tests_after_regressions": {"commits_naming_a_fix_or_regression_that_change_tests": fix_tests,
                                      "decisions_mentioning_a_red_ci": red_ci_decisions},
        "8_features_without_a_journey": {"queries_shown_on_a_page": shown,
                                         "tools_no_check_build_or_ci_names": unused,
                                         "canonical_claims_named_on_no_page": len(claim_ids - on_page),
                                         "canonical_claims": len(claim_ids)},
    }


_DECISION_TEXT: dict[str, str] = {}


def read_decision(did: str) -> str:
    if not _DECISION_TEXT:
        text = read("docs/architecture/decisions.md")
        for part in re.split(r"^## (?=D-\d{3} )", text, flags=re.M)[1:]:
            _DECISION_TEXT[part[:5]] = part
    return _DECISION_TEXT[did]


def archive(path: Path) -> dict:
    """Counts only, from the private archive (D-152): prompts, reports, and per report the numbered deviations and
    whether it records invalidated assumptions, fail-first output and a red CI."""
    head = git("rev-parse", "HEAD", cwd=path).strip()
    prompts = sorted(p.name for p in (path / "sessions/prompts").glob("S*-PROMPT.md"))
    reports = sorted((path / "sessions/reports").glob("SESSION-*-REPORT.md"))
    per = {}
    for r in reports:
        text = r.read_text(encoding="utf-8")
        dev = re.search(r"^## Deviations\s*\n(.*?)(?=^## )", text, flags=re.S | re.M)
        body = dev.group(1) if dev else ""
        per[r.name[8:-10]] = {
            "deviations_numbered": len(re.findall(r"^\d+\. ", body, flags=re.M)),
            "invalidated_assumptions_recorded": bool(re.search(r"invalidated assumption", text, flags=re.I)),
            "fail_first_recorded": bool(re.search(r"fail-first|failfirst|failing first|shown failing", text, flags=re.I)),
            "red_ci_recorded": bool(re.search(r"red CI|CI (?:was|went|turned) red|CI red", text)),
            "minimum_fields_present": all(f"## {f}" in text for f in (
                "Mission outcome", "Files changed", "Data changed", "Tests run", "Evidence added/retired",
                "Decisions made", "Deviations", "Debt introduced/resolved", "Unresolved issues", "Process lessons",
                "Implications for the next session")),
        }
    sessions_with_prompt = {p[1:-len("-PROMPT.md")] for p in prompts}
    return {"archive_head": head, "prompts": len(prompts), "reports": len(reports),
            "prompts_without_report": sorted(sessions_with_prompt - set(per)),
            "per_report": per,
            "reports_with_red_ci": sorted(k for k, v in per.items() if v["red_ci_recorded"]),
            "reports_with_fail_first": sum(1 for v in per.values() if v["fail_first_recorded"]),
            "deviations_total": sum(v["deviations_numbered"] for v in per.values())}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", type=Path, help="a checkout of the private development archive (counts only)")
    a = ap.parse_args()
    tracked = sorted(git("ls-files").split())
    data = {}
    for p in tracked:
        if re.fullmatch(r"data/[a-z_]+\.json", p):
            blob = json.loads(read(p))
            data[Path(p).stem] = items(blob)
    decs = decisions()
    log = no_merge_commits()
    out = {
        "base": {"public_head": git("rev-parse", "HEAD").strip()},
        "capabilities": capabilities(data, decs, tracked),
        "retrospective": retrospective(log, commits(), decs, tracked),
    }
    if a.archive:
        out["archive"] = archive(a.archive)
    out["base"]["files_read_sha256"] = dict(sorted(READ.items()))
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False, sort_keys=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
