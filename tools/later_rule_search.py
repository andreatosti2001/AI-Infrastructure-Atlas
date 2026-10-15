"""The later-rule search (S22, D-210, D-211): did any official US text in a window change an entry or an act the Atlas holds?

    python tools/later_rule_search.py --from YYYY-MM-DD --to YYYY-MM-DD [--record DIR]
        query the registers for the window and write the log
        docs/research/search-logs/later-rules/run-<from>-to-<to>.md; --record keeps every response's bytes in DIR,
        which must be outside the repository (the session's private working files)
    python tools/later_rule_search.py --from ... --to ... --replay DIR --log PATH
        the same from responses recorded with --record, without the network

Owner: the Source Scout (docs/agents/contracts.md). It runs the method of docs/research/search-logs/later-rules/plan.md,
steps 1 to 5, with the official daily edition as the independent register (D-211):

  1. the Federal Register index (federalregister.gov/api/v1, a finding aid): every Bureau of Industry and Security
     document published in the window, every type;
  2. the same index's full text: each term below in every agency's documents; the rescind and repeal words in BIS
     documents;
  3. the official daily edition (govinfo.gov, the XML of each issue in the window): every document's agency, CFR
     heading and text, read for the same terms, independently of the index;
  4. candidates: a document whose official text names a held entry, a held act's citation or number, or the AI
     Diffusion rule's name; whose heading names 15 CFR part 774 (the Commerce Control List); a BIS rule whose text
     uses a rescind or repeal word; or a document the index matched on a term. Each candidate's official PDF is
     retrieved and hashed in full. Every BIS document of step 1 gets a disposition; nothing is dropped silently (CD-3);
  5. each registered official text (data/sources.json, official_legal_text) is retrieved again and its hash compared
     with the registered one (CD-5).

The terms have one home each: the entries are the identifiers in CD-3's row of docs/research/change-detection.md;
the acts are the official citations of data/policies.json and the document numbers in its record IDs.

What it never does: write data/ or docs/research/change-detection.md; read a PDF's text (the Change Detector reads the
candidates and rules each one, CD-1 to CD-3); conclude that a text changes anything (CD-6, CD-7); retry a refused
request under another identity. A refused or unreadable response is an access gap: the outcome is then
"incomplete", and the "Searched to" date must not move (CD-4, D-208).

Exit status: 0 none found in the searched window; 3 something to review (a candidate, a changed hash, registers that
disagree); 4 incomplete (an access gap). Standard library only (D-003).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = REPO_ROOT / "docs" / "research" / "search-logs" / "later-rules"
RULES = REPO_ROOT / "docs" / "research" / "change-detection.md"
POLICIES = REPO_ROOT / "data" / "policies.json"
SOURCES = REPO_ROOT / "data" / "sources.json"

API = "https://www.federalregister.gov/api/v1"
GOVINFO = "https://www.govinfo.gov/content/pkg"
BIS = "industry-and-security-bureau"
FIELDS = ("document_number", "citation", "publication_date", "title", "type", "action", "agencies", "pdf_url")
PER_PAGE = 1000
AI_DIFFUSION = "Artificial Intelligence Diffusion"  # the held rule's name: a text rescinding it may not cite it
BIS_WORDS = ("rescission", "rescind", "repeal", "withdraw", "withdrawal")
BIS_WORD_PATTERN = re.compile(r"\b(rescind|rescission|repeal|withdraw)", re.I)
DOC_TAGS = ("RULE", "PRORULE", "NOTICE", "PRESDOCU")
USER_AGENT = f"Python-urllib/{sys.version_info[0]}.{sys.version_info[1]} (AI-Infrastructure-Atlas later-rule search)"
TIMEOUT = 120

EXIT_NONE, EXIT_REVIEW, EXIT_INCOMPLETE = 0, 3, 4


# ---- the requests ----------------------------------------------------------------------------------------------

def _window(a: str, b: str) -> list[tuple[str, str]]:
    return [("conditions[publication_date][gte]", a), ("conditions[publication_date][lte]", b)]


def index_url(a: str, b: str, page: int, bis: bool, term: str | None = None) -> str:
    params = _window(a, b)
    if bis:
        params.append(("conditions[agencies][]", BIS))
    if term is not None:
        params.append(("conditions[term]", term))
    params += [("order", "oldest"), ("per_page", str(PER_PAGE)), ("page", str(page))]
    params += [("fields[]", f) for f in FIELDS]
    return f"{API}/documents.json?{urllib.parse.urlencode(params)}"


def facets_url(a: str, b: str) -> str:
    return f"{API}/documents/facets/daily?{urllib.parse.urlencode(_window(a, b))}"


def issue_url(day: str) -> str:
    return f"{GOVINFO}/FR-{day}/xml/FR-{day}.xml"


def pdf_url(day: str, number: str) -> str:
    return f"{GOVINFO}/FR-{day}/pdf/{number}.pdf"


@dataclass
class Response:
    url: str
    status: int  # 0: no response (a network error, or a request absent from a recording)
    body: bytes
    at: str
    note: str = ""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # a redirect is recorded as its status, never followed
        return None


class LiveFetcher:
    def __init__(self, record: Path | None = None) -> None:
        self.opener = urllib.request.build_opener(_NoRedirect)
        self.record, self.seen = record, {}

    def today(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    def get(self, url: str) -> Response:
        at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with self.opener.open(request, timeout=TIMEOUT) as reply:
                response = Response(url, reply.status, reply.read(), at)
        except urllib.error.HTTPError as error:
            response = Response(url, error.code, b"", at, error.headers.get("Location", "") or "")
        except (urllib.error.URLError, OSError) as error:
            response = Response(url, 0, b"", at, f"{type(error).__name__}: {error}")
        if self.record is not None:
            self.seen[url] = response
            write_recording(self.record, self.seen)
        return response


def write_recording(folder: Path, responses: dict[str, Response]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    index = {}
    for url, r in responses.items():
        name = hashlib.sha256(url.encode()).hexdigest()[:24]
        (folder / name).write_bytes(r.body)
        index[url] = {"status": r.status, "at": r.at, "note": r.note, "file": name}
    (folder / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True) + "\n", encoding="utf-8")


class ReplayFetcher:
    """Responses recorded with --record; a request absent from the recording is answered as no response."""

    def __init__(self, folder: Path) -> None:
        self.folder = folder
        self.index = json.loads((folder / "index.json").read_text(encoding="utf-8"))

    def today(self) -> str:
        return max((r["at"] for r in self.index.values()), default="0000-00-00")[:10]

    def get(self, url: str) -> Response:
        r = self.index.get(url)
        if r is None:
            return Response(url, 0, b"", self.today() + "T00:00:00Z", "not in the recording")
        return Response(url, r["status"], (self.folder / r["file"]).read_bytes(), r["at"], r.get("note", ""))


# ---- the terms -------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Term:
    name: str
    pattern: re.Pattern
    index_query: str | None  # the index's full-text query; None for words searched only in BIS documents


def entries_from_rules(text: str) -> tuple[str, ...]:
    """The entry identifiers CD-3 names (with 3B090, searched as a control: it was removed in 2023)."""
    row = next((line for line in text.splitlines() if line.startswith("| CD-3 |")), None)
    if row is None:
        raise ValueError("change-detection.md has no CD-3 row")
    return tuple(dict.fromkeys(re.findall(r"\b3[AB]\d{3}\b", row)))


def acts_from_policies(policies: list[dict]) -> tuple[tuple[str, str], ...]:
    """(official citation, document number) of each Federal Register act the Atlas holds.

    The EAR itself (a codified regulation, cited "15 CFR chapter VII, subchapter C") is not a term: nearly every BIS
    rule names it. A text repealing it would amend 15 CFR part 774 and use a repeal word, which steps 3 and 4 select.
    """
    acts = []
    for p in policies:
        if p["id"].startswith("policy-us-fr-"):
            acts += [(citation["value"], p["id"][len("policy-us-fr-"):]) for citation in p.get("official_citation", [])]
    return tuple(acts)


def make_terms(entries: tuple[str, ...], acts: tuple[tuple[str, str], ...]) -> tuple[Term, ...]:
    terms = [Term(e, re.compile(rf"\b{re.escape(e)}\b"), f'"{e}"') for e in entries]
    for citation, number in acts:
        terms.append(Term(citation, re.compile(r"\s+".join(map(re.escape, citation.split())) + r"\b"), f'"{citation}"'))
        if number:
            terms.append(Term(number, re.compile(rf"(?<![\w-]){re.escape(number)}(?![\w-])"), f'"{number}"'))
    terms.append(Term(AI_DIFFUSION, re.compile(re.escape(AI_DIFFUSION), re.I), f'"{AI_DIFFUSION}"'))
    return tuple(dict.fromkeys(terms))


def registered_texts(sources: list[dict]) -> tuple[tuple[str, str, str], ...]:
    return tuple((s["id"], s["url"], s["retrieval"]["sha256"]) for s in sources
                 if s.get("source_class") == "official_legal_text" and s.get("retrieval", {}).get("sha256"))


# ---- the search ------------------------------------------------------------------------------------------------

@dataclass
class OfficialDoc:
    number: str
    day: str
    tag: str
    agency: str
    cfr: str
    hits: list[str]
    part_774: bool
    bis_words: list[str]

    @property
    def is_bis(self) -> bool:
        return "industry and security" in self.agency.lower()


@dataclass
class Candidate:
    number: str
    day: str
    agency: str
    reasons: list[str]
    url: str = ""
    status: int = 0
    size: int = 0
    sha256: str = ""


@dataclass
class Result:
    window: tuple[str, str]
    terms: tuple[Term, ...]
    requests: list[Response] = field(default_factory=list)
    bis_docs: list[dict] = field(default_factory=list)
    term_hits: dict[str, list[dict]] = field(default_factory=dict)
    days: list[tuple[str, str]] = field(default_factory=list)  # (day, what was read)
    official: dict[str, OfficialDoc] = field(default_factory=dict)
    candidates: list[Candidate] = field(default_factory=list)
    registered: list[tuple[str, str, str, str]] = field(default_factory=list)  # id, registered, now, verdict
    disagreements: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


def _host(url: str) -> str:
    return urllib.parse.urlsplit(url).netloc


def _gap(result: Result, r: Response, what: str) -> None:
    status = f"HTTP {r.status}" if r.status else "no response"
    note = f" ({r.note})" if r.note else ""
    result.gaps.append(f"{what}: {_host(r.url)} answered {status}{note} at {r.at} — {r.url}")


def _get(fetcher, result: Result, url: str) -> Response:
    r = fetcher.get(url)
    result.requests.append(r)
    return r


def _index(fetcher, result: Result, a: str, b: str, bis: bool, term: str | None, what: str) -> list[dict] | None:
    found, page = [], 1
    while True:
        r = _get(fetcher, result, index_url(a, b, page=page, bis=bis, term=term))
        try:
            reply = json.loads(r.body) if r.status == 200 else None
        except ValueError:
            reply = None
        if reply is None:
            _gap(result, r, f"the index did not answer {what}")
            return None
        found += reply.get("results", [])
        if len(found) >= reply["count"] or not reply.get("results") or page >= reply.get("total_pages", 1):
            if len(found) != reply["count"]:
                _gap(result, r, f"the index returned {len(found)} of {reply['count']} documents for {what}")
            return found
        page += 1


def _days(a: str, b: str) -> list[str]:
    first, last = datetime.date.fromisoformat(a), datetime.date.fromisoformat(b)
    return [(first + datetime.timedelta(n)).isoformat() for n in range((last - first).days + 1)]


def _read_issue(day: str, body: bytes, terms: tuple[Term, ...]) -> list[OfficialDoc]:
    root = ET.fromstring(body)
    docs = []
    for tag in DOC_TAGS:
        for element in root.iter(tag):
            frdoc = " ".join(" ".join(e.itertext()) for e in element.iter("FRDOC"))
            number = re.search(r"FR Doc\.\s*([A-Z0-9][\w-]*)", frdoc)
            if not number:
                continue
            preamble = element.find("PREAMB")
            heads = preamble if preamble is not None else element
            agency = " / ".join(" ".join(e.itertext()).strip() for e in heads.iter() if e.tag in ("AGENCY", "SUBAGY"))
            cfr = " ".join(" ".join(e.itertext()).strip() for e in heads.iter("CFR"))
            text = re.sub(r"\s+", " ", " ".join(element.itertext()))
            words = sorted({m.group(1).lower() for m in BIS_WORD_PATTERN.finditer(text)})
            docs.append(OfficialDoc(number.group(1), day, tag, agency, cfr, [t.name for t in terms if t.pattern.search(text)],
                                    _names_part_774(cfr), words))
    return docs


def _names_part_774(cfr: str) -> bool:
    """A CFR heading such as "15 CFR Parts 734, 740, and 774" or "15 CFR Parts 730 through 774"."""
    for title, parts in re.findall(r"(\d+)\s+CFR\b(.*?)(?=\d+\s+CFR\b|$)", cfr):
        if title != "15":
            continue
        for lo, hi in re.findall(r"(\d+)(?:\s*(?:-|–|through)\s*(\d+))?", parts):
            if int(lo) <= 774 <= int(hi or lo):
                return True
    return False


def search(a: str, b: str, fetcher, terms: tuple[Term, ...], registered: tuple[tuple[str, str, str], ...]) -> Result:
    if not (re.fullmatch(r"\d{4}-\d{2}-\d{2}", a) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", b)) or a > b:
        raise ValueError(f"the window must be two dates, the first no later than the second: {a} to {b}")
    if b > fetcher.today():
        raise ValueError(f"the window ends after today ({fetcher.today()}): a later day's texts cannot be searched yet")
    result = Result((a, b), terms)

    # step 1: every BIS document in the window (finding aid)
    bis_docs = _index(fetcher, result, a, b, bis=True, term=None, what="every BIS document")
    result.bis_docs = bis_docs or []

    # step 2: the terms in every agency's documents; the rescind and repeal words in BIS documents
    for t in terms:
        hits = _index(fetcher, result, a, b, bis=False, term=t.index_query, what=f"the term {t.name}")
        result.term_hits[t.name] = hits or []
    for word in BIS_WORDS:
        hits = _index(fetcher, result, a, b, bis=True, term=word, what=f"the word {word} in BIS documents")
        result.term_hits[f"{word} (BIS)"] = hits or []

    # step 3: the official daily edition, independently of the index
    r = _get(fetcher, result, facets_url(a, b))
    try:
        counts = {d: v["count"] for d, v in json.loads(r.body).items()} if r.status == 200 else None
    except (ValueError, KeyError, TypeError, AttributeError):
        counts = None
    if counts is None:
        _gap(result, r, "the index did not say on which days documents were published")
    for day in _days(a, b):
        listed = None if counts is None else counts.get(day, 0)
        weekday = datetime.date.fromisoformat(day).weekday() < 5
        if listed == 0 and not weekday:
            result.days.append((day, "no issue: a weekend day with no document in the index (not requested)"))
            continue
        r = _get(fetcher, result, issue_url(day))
        if r.status == 200:
            try:
                docs = _read_issue(day, r.body, terms)
            except ET.ParseError as error:
                _gap(result, r, f"the official edition of {day} could not be read ({error})")
                continue
            for d in docs:
                result.official.setdefault(d.number, d)
            bis = sum(d.is_bis for d in docs)
            result.days.append((day, f"read: {len(docs)} documents, {bis} BIS; {len(r.body)} bytes, sha256 {hashlib.sha256(r.body).hexdigest()}"))
        elif listed == 0:
            result.days.append((day, f"no issue: no document in the index that day; the edition answered HTTP {r.status}"))
        else:
            _gap(result, r, f"the official edition of {day} was not served"
                 + ("" if listed is None else f" (the index lists {listed} documents that day)"))
            result.days.append((day, "not read: access gap"))

    # step 4: candidates
    reasons: dict[str, list[str]] = {}
    for d in result.official.values():
        why = [f"names {h}" for h in d.hits]
        if d.part_774:
            why.append(f"heading names 15 CFR part 774 ({d.cfr})")
        if d.is_bis and d.tag in ("RULE", "PRORULE") and d.bis_words:
            why.append("a BIS rule using " + ", ".join(d.bis_words))
        if why:
            reasons[d.number] = why
    index_docs = {doc["document_number"]: doc for hits in result.term_hits.values() for doc in hits}
    index_docs.update({doc["document_number"]: doc for doc in result.bis_docs})
    for name, hits in result.term_hits.items():
        for doc in hits:
            why = reasons.setdefault(doc["document_number"], [])
            if not any(name.split(" (")[0] in w for w in why):
                why.append(f"the index matched {name}")
    for number in sorted(reasons, key=lambda n: (_day_of(n, result, index_docs), n)):
        official = result.official.get(number)
        indexed = index_docs.get(number, {})
        day = _day_of(number, result, index_docs)
        agency = official.agency if official else ", ".join(x.get("slug", "") for x in indexed.get("agencies", []))
        c = Candidate(number, day, agency, reasons[number])
        c.url = indexed.get("pdf_url") or pdf_url(day, number)
        r = _get(fetcher, result, c.url)
        c.status, c.size = r.status, len(r.body)
        if r.status == 200:
            c.sha256 = hashlib.sha256(r.body).hexdigest()
        else:
            _gap(result, r, f"the official text of candidate {number} was not served")
        result.candidates.append(c)
    official_bis = {n for n, d in result.official.items() if d.is_bis}
    read_days = {day for day, what in result.days if what.startswith("read")}
    for doc in result.bis_docs:
        if doc["document_number"] not in result.official and doc["publication_date"] in read_days:
            result.disagreements.append(f"{doc['document_number']} ({doc['publication_date']}, {doc['title'][:80]}): "
                                        "in the index, not in the official edition of that day")
    for number in sorted(official_bis - {doc["document_number"] for doc in result.bis_docs}):
        if bis_docs is not None:
            result.disagreements.append(f"{number} ({result.official[number].day}): a BIS document in the official "
                                        "edition, not in the index's list of BIS documents")

    # step 5: the registered official texts (CD-5)
    for source, url, registered_sha in registered:
        r = _get(fetcher, result, url)
        if r.status != 200:
            _gap(result, r, f"the registered text {source} was not served")
            result.registered.append((source, registered_sha, "", "not read: access gap"))
            continue
        now = hashlib.sha256(r.body).hexdigest()
        verdict = "unchanged" if now == registered_sha else "CHANGED: the Verifier re-reads its anchors; the record is not edited (CD-5)"
        result.registered.append((source, registered_sha, now, verdict))
    return result


def _day_of(number: str, result: Result, index_docs: dict[str, dict]) -> str:
    if number in result.official:
        return result.official[number].day
    return index_docs.get(number, {}).get("publication_date", "")


def outcome(result: Result) -> tuple[str, int]:
    if result.gaps:
        return ("incomplete: the access gaps below leave part of the window unsearched; the \"Searched to\" date "
                "must not move until a run covers it (CD-4, D-208)", EXIT_INCOMPLETE)
    changed = [r for r in result.registered if r[3].startswith("CHANGED")]
    if result.candidates or result.disagreements or changed:
        return (f"to review: {len(result.candidates)} candidate texts, {len(result.disagreements)} register "
                f"disagreements, {len(changed)} changed registered texts. The Change Detector reads and rules each "
                "candidate (CD-1 to CD-3); a text that changes a held entry or act stops the session for the human's "
                "verdict, and the \"Searched to\" date does not move before it (CD-6, D-208)", EXIT_REVIEW)
    return ("none found in the searched window (CD-4): no candidate text, the registers agree, every registered text "
            "is unchanged", EXIT_NONE)


# ---- the log ---------------------------------------------------------------------------------------------------

def _cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def render(result: Result) -> str:
    a, b = result.window
    said, _ = outcome(result)
    ran_on = max((r.at for r in result.requests), default="")[:10]
    lines = [
        f"# Later-rule search run: {a} to {b}",
        "",
        "Written by `tools/later_rule_search.py` for the Source Scout (D-210, D-211), following "
        "[`plan.md`](plan.md) steps 1 to 5 with the official daily edition as the independent register. Times are UTC. "
        "Nothing in this log is evidence: the index is a finding aid, and a candidate is a pointer until the Change "
        "Detector reads its official text and rules it in [`change-detection.md`](../../change-detection.md).",
        "",
        f"**Window searched: {a} to {b}**",
        "",
        f"**Run on:** {ran_on}, {len(result.requests)} requests (listed at the end).",
        "",
        f"**Outcome:** {said}.",
    ]
    candidates = {c.number for c in result.candidates}
    lines += ["", f"## Step 1 — every BIS document in the index ({len(result.bis_docs)})", ""]
    if result.bis_docs:
        lines += ["| Published | Document | Citation | Type | Title (shortened) | Disposition |", "|---|---|---|---|---|---|"]
        for d in result.bis_docs:
            n = d["document_number"]
            if n in candidates:
                why = "candidate (step 4)"
            elif n in result.official:
                why = "not a candidate: its official text names no term and its heading no part 774"
            else:
                why = "not read in the official edition (see disagreements or access gaps)"
            lines.append(f"| {d['publication_date']} | {n} | {_cell(d.get('citation') or '')} | {_cell(d.get('type') or '')} | "
                         f"{_cell((d.get('title') or '')[:100])} | {why} |")
    else:
        lines.append("None.")
    lines += [
        "",
        "## Step 2 — the terms in the index",
        "",
        "Entries: the identifiers in CD-3 of `change-detection.md`. Acts: the official citations of `data/policies.json` "
        "and the document numbers in its record IDs. The AI Diffusion rule's name, since a text rescinding it might "
        "not cite it. In BIS rules only: " + ", ".join(BIS_WORDS) + ".",
        "",
        "| Term | Index query | Documents the index matched (all agencies) |",
        "|---|---|---|",
    ]
    for t in result.terms:
        hits = result.term_hits.get(t.name, [])
        lines.append(f"| {_cell(t.name)} | `{_cell(t.index_query)}` | {len(hits)}"
                     + (": " + ", ".join(h["document_number"] for h in hits) if hits else "") + " |")
    for word in BIS_WORDS:
        hits = result.term_hits.get(f"{word} (BIS)", [])
        lines.append(f"| {word} (BIS documents) | `{word}` | {len(hits)}"
                     + (": " + ", ".join(h["document_number"] for h in hits) if hits else "") + " |")
    lines += ["", "## Step 3 — the official daily edition", "", "| Day | What was read |", "|---|---|"]
    lines += [f"| {day} | {_cell(what)} |" for day, what in result.days]
    lines += ["", f"## Step 4 — candidates ({len(result.candidates)})", ""]
    if result.candidates:
        lines += ["| Document | Published | Agency | Why | Official PDF | HTTP | Bytes | sha256 |", "|---|---|---|---|---|---|---|---|"]
        for c in result.candidates:
            lines.append(f"| {c.number} | {c.day} | {_cell(c.agency)} | {_cell('; '.join(c.reasons))} | {c.url} | "
                         f"{c.status or 'none'} | {c.size} | `{c.sha256}` |")
    else:
        lines.append("None.")
    lines += ["", "## Step 5 — the registered official texts (CD-5)", ""]
    if result.registered:
        lines += ["| Source | Registered sha256 | sha256 now | Verdict |", "|---|---|---|---|"]
        lines += [f"| {s} | `{reg}` | `{now}` | {v} |" for s, reg, now, v in result.registered]
    lines += ["", "## Register disagreements", ""]
    lines += [f"- {d}" for d in result.disagreements] or ["None."]
    lines += ["", "## Access gaps", ""]
    lines += [f"- Access gap: {g}" for g in result.gaps] or ["None."]
    lines += ["", "## Requests", "", "| Time | Host | Request | HTTP | Bytes | sha256 |", "|---|---|---|---|---|---|"]
    for r in result.requests:
        split = urllib.parse.urlsplit(r.url)
        path = split.path + (f"?{urllib.parse.unquote(split.query)}" if split.query else "")
        digest = f"`{hashlib.sha256(r.body).hexdigest()}`" if r.status == 200 else _cell(r.note)
        lines.append(f"| {r.at} | {split.netloc} | `{_cell(path)}` | {r.status or 'none'} | {len(r.body)} | {digest} |")
    return "\n".join(lines) + "\n"


# ---- the command line ------------------------------------------------------------------------------------------

def _inside(path: Path, folder: Path) -> bool:
    try:
        path.resolve().relative_to(folder.resolve())
        return True
    except ValueError:
        return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Search a window for later official texts changing what the Atlas holds.")
    parser.add_argument("--from", dest="start", required=True, help="first publication day searched (YYYY-MM-DD)")
    parser.add_argument("--to", dest="end", required=True, help="last publication day searched, no later than today")
    parser.add_argument("--log", type=Path, help="where to write the log (default: run-<from>-to-<to>.md in the log folder)")
    parser.add_argument("--record", type=Path, help="keep every response's bytes here (outside the repository)")
    parser.add_argument("--replay", type=Path, help="read responses recorded with --record instead of the network")
    args = parser.parse_args(argv)
    log = args.log or LOG_DIR / f"run-{args.start}-to-{args.end}.md"
    if _inside(log, REPO_ROOT) and not _inside(log, LOG_DIR):
        parser.error(f"a log inside the repository goes in {LOG_DIR.relative_to(REPO_ROOT)}/")
    if args.record and _inside(args.record, REPO_ROOT):
        parser.error("--record must be outside the repository")
    fetcher = ReplayFetcher(args.replay) if args.replay else LiveFetcher(args.record)
    terms = make_terms(entries_from_rules(RULES.read_text(encoding="utf-8")),
                       acts_from_policies(json.loads(POLICIES.read_text(encoding="utf-8"))))
    registered = registered_texts(json.loads(SOURCES.read_text(encoding="utf-8")))
    try:
        result = search(args.start, args.end, fetcher, terms, registered)
    except ValueError as error:
        parser.error(str(error))
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(render(result), encoding="utf-8")
    said, code = outcome(result)
    print(f"{log}: {said}")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
