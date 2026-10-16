# Case study: an evidence-backed research system built by an AI model under human governance

- **Status:** accepted (decided by the human on 2026-10-16, S25 H-3; D-230). Written by the
  Portfolio Reviewer (D-229).
- **Claim discipline:** a count is **measured**, and names where it was measured: mostly the S24 portfolio audit's
  script ([`measures.json`](quality/audit-evidence/portfolio-audit/measures.json), at public commit `5fd5891`), so
  later commits are not in it. Every judgement is the Portfolio Reviewer's `INTERPRETATION`, written beside its
  evidence. A capability is credited only for something a reviewer can open and recount, never for a document's
  description of itself.

## 1. The problem

Claims about the hardware behind AI are easy to find and hard to check. A page that says who makes the memory inside
an AI accelerator rarely says on what evidence, as of when, or what is not known. The Atlas asks one question,
answers it end to end, and makes every step of the answer inspectable:

> What does an AI accelerator's memory depend on, who is reported to supply it, and which recorded export-control
> texts name those parts?

## 2. What was built

A research database of canonical JSON records, in which every relationship rests on claims and every claim quotes a
registered source at a locator. On top of it sit a SQL layer, 18 generated pages and a printable client brief, all
rebuilt byte for byte from the records and published from the release commit. The
[final architecture record](architecture/final-architecture.md) has the layers. The
[demonstration](release/demonstration.md) walks one value from a page to its source sentence.

## 3. What it shows

The verdicts are the S24 audit's ([portfolio audit](architecture/portfolio-audit.md) Part 3), unchanged except where
the release changed the evidence.

| Capability | Verdict | What a reviewer can open |
|---|---|---|
| Evidence methodology and domain research | **shown**, as depth of method on a narrow slice | 197 claims, each quoting its source at a locator, of five types kept apart; 21 candidate links refused with their reasons; S23's second retrieval found 178 of 178 readable quoted passages at their locators ([release content audit](research/release-content-audit.md)) |
| Data engineering | **shown** | 7 schemas for 13 record kinds; explicit unknown states; every schema change with a decision (19 of 19 commits); no canonical claim or source ever removed or reworded |
| SQL and Python | **shown** | four queries, each its own tutorial, results committed with input digests and recomputed independently; standard-library tools, with one pinned dependency |
| Governance of AI-assisted work | **shown**, as governance, not as autonomous agents | roles as written contracts checked in CI; every file owned; drafts held in staging; 197 of 197 canonical claims accepted by the human ([review record](quality/human-reviews.md)) |
| Reproducibility | **shown**, and since v1.0 visible at a public address | every page rebuilt byte for byte from digested inputs, locally, in CI and before publication; the published pages checked against the release commit |
| Policy analysis | **thin** | seven export-control acts with dated events, statuses derived on a date, a logged search for later rules, refusals at the term level. This is evidence-grounded policy description and change tracking, not analysis (P-6) |
| Client value | **the weakest point** | one printable brief, every sentence recomputed by a check, scope and limits on its first page; two first-time readers found it accurate but thin, dated and written in the project's codes |
| Documentation | **shown for a builder; costly for a newcomer** | decisions with their rejected alternatives; audits with measured evidence; dense with internal codes |

**Reading** (`INTERPRETATION`): the Atlas demonstrates evidence engineering and the governance of AI-drafted work
more strongly than it demonstrates domain coverage or policy judgement. That is the shape v1 chose (one path, depth
first), and the [known limitations](known-limitations.md) state it.

## 4. How it was built

Measured by S24 over the public history to `5fd5891` and, as counts only, over the private archive:

- **168 non-merge commits on 12 calendar days**, 29 September to 16 October 2026, in governed sessions, each driven
  by a written session prompt and closed by a report.
- **About 110,000 lines added by Claude**, an AI model made by Anthropic: code, documents, data and generated pages.
  **3,529 lines by the human owner**: the rule documents uploaded at the start.
- **The human decided.** The human wrote the rules, chose at every decision put as options, accepted or rejected every
  claim (197 of 197) and merged every pull request (41 of 41 at S24).
- **Checks before code.** 27 of 30 session reports record new checks shown failing before they were trusted. A
  harness of deliberate faults, 222 at S24 and 230 at the release, must each be caught for the reason it names.
- **Little rework in code and data.** Six decisions were superseded. The churn is in the state rows that every
  session rewrites.

Three limits of the process are stated, not hidden:

- **No review of the code by a person is recorded (P-2).** The 41 pull requests carry 0 reviews and 0 comments, with
  a median of 29 seconds from opening to merge. The code is checked by tests, planted faults, browser checks in CI and
  audits that Claude wrote, not by a person. Whether to add a human review sample is the human's decision
  ([final audit](architecture/final-audit.md#4-what-stays-open)).
- **The richest record of the process is private (P-13).** Session prompts, reports and their 180 numbered
  deviations are in a private archive by decision (D-152). The public record is the commits, the decision log, the
  audits and these counts.
- **How closely the human read each claim is not recorded.** The review record holds each verdict, its date and
  the anchors the human spot-checked, not the time or depth of each reading; both first-time readers of the release
  said they could not tell careful drafting from light review.
- **The owner's learning is not measured.** The repository records decisions and verdicts, not what the human learned.

## 5. What it does not show

- **Breadth.** One path of the AI compute chain, for two accelerators. Foundries, packaging, equipment, data centres
  and energy have no supply-chain records (KL-01).
- **Corroboration.** No value rests on two independent publishers (KL-02).
- **Use by an outside person.** The pages are public from v1.0, but no person who did not build the Atlas is recorded
  as having used them (KL-15).
- **Analysis or advice.** The Atlas says what texts say and when; it does not say what follows from them, and it
  never says what anyone should do (P-6, KB-01).

## 6. Lessons

From the audits, in the order they were learned:

- **A check that has never failed is not yet a check** (S22). The browser checks had passed for ten sessions without
  being able to fail.
- **Re-retrieve the evidence** (S23). A second retrieval of every source found two that had begun refusing automated
  requests, and the one opposing official text the Atlas lacked.
- **A first-time reader finds what internal audits cannot** (S24). Two readers given four artifacts found in minutes
  that the strongest evidence was hard to reach and that authorship was unstated.
- **Controls outside CI decay** (S24). The archive's report rule stopped being enforced when the reports moved out of
  the checked repository.
- **A check proves where a sentence comes from, not that it is still true** (S25). A reader of the release found a
  query tutorial, shown on a page, still saying the suppliers were not researched, nine days after they were
  recorded; every check had passed. It was corrected before the release (D-230).

## 7. The exit-condition reading

The roadmap's condition for v1.0 is that another person can understand what the system does, how its data is
structured, how claims are verified, how metrics are produced, how agents are governed, how to reproduce the build,
and why it is useful. Two fresh AI readers were given the release candidate's tree and nothing else, and answered one
form field per point before any assessment (D-228). Their answers are kept as given in
[`exit-reading/`](quality/audit-evidence/portfolio-audit/exit-reading/).

**The assessment** (`INTERPRETATION`, written after both answers were in):

| Point | Understood? | What the readers doubted or could not find |
|---|---|---|
| 1. What it does | yes, both: the question, its scope, the pages, the audience | who the "client" is; no named user |
| 2. How the data is structured | yes, both: thirteen kinds, claims citing sources, records citing claims, explicit unknown states, staging | no single overview diagram of the model |
| 3. How claims are verified | yes, both: extraction, re-read, the human's verdict, the checks | how closely the human read each claim (now stated in Part 4) |
| 4. How metrics are produced | yes, both: the warehouse, the queries as tutorials, the digests, the independent recomputation | two tutorial sentences no longer true, and stale lines in `metrics.md`: corrected before the release (D-230) |
| 5. How agents are governed | yes, both: roles as contracts that Claude works under, no runtime, the owner and data checks, the human's merges | role boundaries are checked after the fact, not when a file is written (P-11); no review of the code by a person (P-2) |
| 6. How to reproduce the build | yes, both: Python 3.11, the pins, `check_all.py`, byte comparison, the harness | the published files lack `.github/` and Git history, so they cannot be checked as served: the release notes now say to clone |
| 7. Why it is useful | yes, both, and both judged it the same way: a worked, checkable template for evidence-grade research more than a data product a practitioner can rely on today | no outside user; coverage too narrow and evidence too old for a decision |

**Result:** both readers understood all seven points, and neither misread the system. Their doubts are limits the
Atlas states or now states, and one was a real defect, which was corrected. The limit of the test: the readers are
language models, not people, and they read the pages as text without rendering them.

## 8. Check it yourself

- The pages: <https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/index.html>
- Every check, on a clone with Python 3.11: `python tools/check_all.py` ([README](../README.md#validate)).
- CI on every push: <https://github.com/andreatosti2001/AI-Infrastructure-Atlas/actions/workflows/ci.yml>
- The audits and their evidence: [audit history](quality/audit-history.md).
