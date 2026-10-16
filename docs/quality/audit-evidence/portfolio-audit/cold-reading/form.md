# S24 cold-reading form

Answered before any S24 capability assessment is written (Part B §07 task 5; H-0: "Two fresh AI readers, no time
from you"). The same form goes to each reader; each answers without seeing the other's answers, Claude's view, or
anything outside `reader-input/`. One field per question; two to five sentences each. Say "cannot tell from what I
was given" where that is the honest answer.

**The four artifacts** (`reader-input/`, rendered by `render-reader-input.js` from the public repository at the S24
branch head):

- **A1** `1-README.md`: the repository's front page.
- **A2** `2-brief-visible-text.txt` and the two first-screen screenshots: the client brief "accelerator memory", as a
  reader sees it with every disclosure closed.
- **A3** `3-sql-tutorial-text.txt`: the brief's "How this was computed" disclosure, opened.
- **A4** `4-decision-D-118.md`: one entry of the project's decision log.

## A1 — the README

1. In your own words, what is this project, and what question does it answer?
2. What does the README claim the project can do that you would want to check, and could you check any of it from
   the README alone?

## A2 — the client brief

3. What question does the brief answer, and what is its answer, in two or three sentences a client could repeat?
4. What does the brief say it does **not** know or does not cover? Name the limits you noticed.
5. Would you rely on this brief to prepare a decision? What raises or lowers your trust, and why?
6. Pick one statement in the brief. Can you trace it to its evidence (a source, a quote, a date) from the brief
   itself? Say which statement and what you found.

## A3 — the SQL tutorial

7. What does the query compute, and for what population?
8. Could you reproduce or check its result from what the tutorial gives you? What would you need that it does not
   give?
9. What does the tutorial say (or fail to say) about what the result does **not** prove?

## A4 — the decision record

10. What was decided, what alternatives were rejected, and why?
11. What does this record tell you about how the project was built?

## Overall

12. For each capability below, say **shown** (an artifact lets you see or check it), **claimed** (an artifact says
    it, but nothing you were given lets you check it) or **not visible** (nothing in the four artifacts touches it),
    with one sentence naming the artifact:
    domain expertise · data engineering · SQL/Python · AI governance and agents · policy analysis · reproducibility ·
    client value · documentation quality.
13. What one thing would most change your view of this project's professional quality, and what is missing that you
    expected to find?
