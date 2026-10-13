# Search plan: the first policy links (S18)

Written on 2026-10-13, after the human's rulings on the link design (D-165 to D-174) and before the
Verifier's retrieval below. The Source Scout, the Extractor and the Verifier follow it and log each step in
[`search-log.md`](search-log.md).

**Read before this plan, for the design only.** At the opening of S18 (2026-10-13T15:13Z) the five registered
texts were re-retrieved, their hashes compared with the registered ones (all matched), and searched for the
terms below to write [`policy-links.md`](../../../architecture/policy-links.md)'s "What the texts give". That
reading shaped the design; it is not evidence. The links rest only on the retrieval, the anchors and the
re-reads this plan sets out.

## The question

For each of the five acts the Atlas holds (`src-057` to `src-061`): **does the act's own text name a
component or technology class of the Atlas among the items it controls, in the record's name or an alias?**
(`policy-links.md` K-2.)

## How the candidates are found

1. **Every class, every text.** Each text is searched, in its extracted text, for the name and every alias of
   each of the seven component and nine technology records, matching case and hyphenation loosely
   ("high-bandwidth memory" matches "High Bandwidth Memory"). The term must be the record's own: a broader
   term ("GPUs", "ASICs", "accelerators"), a narrower one, or an item used for the class (equipment for a
   lithography technology) is a candidate only for refusal (`term_not_matched`).
2. **The words around each hit** are read in context. A hit is a link candidate only when the sentence states
   that the act itself controls, or adds or revises a control on, the class. A sentence that names the class
   without controlling it (a red flag, a description of another act's control) is a candidate only for
   refusal (`relation_not_stated`).
3. **Products and companies.** Each text is searched for the names and aliases of the nine companies and three
   products. No product or company link is made (D-165). A sentence that would let the Atlas apply a
   threshold to a named product is recorded as refused (`applies_a_threshold`, LA-3, D-172).
4. **Later changes** (K-4, D-169). For each link, the control entries its own anchors name (an ECCN such as
   "3A090.c") are searched in every later act the Atlas holds (published after it). A sentence that removes,
   replaces or revises that entry becomes an `ATTRIBUTION` claim cited by the link, quoting the later text.
   Acts the Atlas does not hold are not searched; that limit is logged and carried as debt.

## What counts (`source-policy.md` §7, `rel:restricts`, D-171)

- **Only the act's own official text** (`official_legal_text`, the registered govinfo.gov PDF), with the
  issuing authority as `originator`.
- **Claims:**
  - an `ATTRIBUTION` to BIS: "BIS's rule … states that …", quoting the sentence that adds or states the
    control, its locator naming the page and, where the sentence names one, the entry;
  - a `DERIVATION` per link, with two inputs (that `ATTRIBUTION` and the record's working-definition claim),
    quoting the act's term and the record's name, and concluding only that they name the same kind of part;
  - for a later change: an `ATTRIBUTION` to BIS quoting the later act.
- **Never in a claim's wording:** thresholds applied to anything, "in force", "licence required" or
  "prohibited" in the Atlas's own voice, or a statement that the control applies today (LA-1 to LA-4).

## What never counts

- the Federal Register's web pages and API metadata, eCFR, BIS press releases, law-firm alerts and news.
  None is planned; if one is read as a pointer, it is logged as such.

## Retrieval and re-reading (RA-1 to RA-7)

- Each of the five texts is retrieved again by an ordinary HTTPS request from its registered URL, hashed in
  full and compared with the registered hash. **A mismatch stops every link resting on that text** (S18 prompt
  §16) and is logged.
- Text is extracted locally (`pdftotext`, reading order and raw stream). Bytes and extracted text stay outside
  the repository.
- Each anchor is drafted from the extracted text, then re-read by the Verifier in the bytes whose hash is the
  registered one, on the page its locator names. Each claim's `read` records that access time and hash.
- No new source is expected: the five texts are registered (`src-057` to `src-061`).

## Stop rules

- A candidate that needs a threshold, a definition or an exemption applied to a product or firm is refused,
  never drafted as a link (LA-3).
- A term that is not the record's own is refused, never stretched (K-2).
- If a sentence is ambiguous between controlling a class and describing another act's control, the candidate
  is refused as `relation_not_stated` and the sentence is logged.
