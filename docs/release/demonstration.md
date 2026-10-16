# Demonstration: the dataset and one journey through it — v1.0

- **Status:** proposed (S25, 2026-10-16), for the human's acceptance with the release (S25 H-3). Written by the
  Editorial (D-229).
- **What it is:** the dataset v1.0 ships, and one journey through the published pages that a reader can repeat:
  question, answer, evidence, source. The same journey follows from a clone of the repository. No step needs an
  account, a script or a server of your own.

## 1. The demonstration dataset

The dataset is the canonical records of the release commit, exactly as the pages use them. Nothing was sampled or
prepared for the demonstration.

| What | Where | Read it as |
|---|---|---|
| The records, 13 kinds, one file each | [`data/`](../../data/) | JSON; each kind's schema in [`schemas/`](../../schemas/) |
| The counts | [baseline §1](../architecture/baseline.md), measured in [`measures.json`](../quality/audit-evidence/portfolio-audit/measures.json) | — |
| The human's verdict on every claim | [human review record](../quality/human-reviews.md) | each claim's `review` names its entry |
| The computed results | [`sql/results/`](../../sql/results/) | JSON with the SHA-256 of every input |
| What the records leave open | [known limitations](../known-limitations.md); `data/refused_candidates.json` | — |

Load it into SQL from a clone: `python tools/warehouse.py` builds an in-memory DuckDB from `data/` and runs the four
queries ([`sql-layer.md`](../architecture/sql-layer.md)).

## 2. The journey: from a question to the sentence a value rests on

Start at <https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/index.html>.

1. **Pick a question.** The entry page, "What are you trying to understand?", lists six questions. Choose "What does
   an AI accelerator's memory depend on, and who is known to make it?" and open the dependency journey.
2. **Read the short answer.** The page leads with its answer, then says why it matters. Under "How to read this
   page", the Atlas framing says what the page covers and what it does not.
3. **Find the link in the diagram.** In "The chain", the line from the NVIDIA H100 to High Bandwidth Memory carries
   the memory's reported supplier. "How to read the diagram" says what each line style means: stated, inferred,
   reported, or a gap.
4. **Open its evidence.** Select the mark, or Tab to it and press Enter. The panel "NVIDIA H100 incorporates High
   Bandwidth Memory" lists every claim the link rests on. The claim cited for the supplier is an `ATTRIBUTION`: a
   third party's statement, shown as that party's, with its evidence status.
5. **Read the evidence itself.** The panel quotes the source's own sentence and gives its locator (where in the
   source the sentence is), the source's title, publisher and class, its dates, and whether the source meets the
   source policy's criteria. The link to the source opens the page the sentence was read from.
6. **See who accepted it.** "Recorded in" opens the human's verdict on that claim, with its date, in the
   [human review record](../quality/human-reviews.md).
7. **See how it was computed.** "The chain as a table" restates the chain as one row per link, computed in SQL. Its
   "How this was computed" tutorial gives the question, the query, what each part does and how to read the result.
8. **See what is not known.** "What the Atlas does not know" lists the recorded gaps, the candidates the Atlas refused
   with their reasons, and the pairs with no record either way.
9. **Take the answer away.** The [client brief](https://andreatosti2001.github.io/AI-Infrastructure-Atlas/site/briefs/accelerator-memory/index.html)
   answers the wider question, including the export-control texts, on one printable page with its scope and limits
   first.

## 3. The same journey from a clone

```bash
python tools/trace.py rel-product-nvidia-h100-tensor-core-gpu-incorporates-component-high-bandwidth-memory
python tools/navigate.py depends-on technology-3d-die-stacking
python tools/check_all.py    # every check, and every page rebuilt and compared byte for byte
```

`trace.py` prints, for the link in step 4, every claim, its type and status, each citation's source, locator, quoted
anchor and the hash of the bytes the Verifier read, and the human's verdict. `navigate.py` walks the chain the other
way: what depends on 3D die stacking.

## 4. What the journey shows, and what it does not

It shows that a value on a page can be followed to the source sentence it rests on, to who said it, to how it was
checked and to who accepted it, and that what is not known is shown as such. It does not show that the supplier
named is the only one (the page says so), or anything after the as-of date (D-228). The Atlas's limits are listed in
the [known limitations](../known-limitations.md).
