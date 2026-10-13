# Policy dataset: the instruments that act on the chain

**Status:** ACCEPTED (the human's rulings of 2026-10-08, H-1): every item P-1 to P-11 as proposed
(D-154 to D-163), and one rule found while writing the checks, effective dates fixed in advance (D-164).
The rulings are listed at the end. The text below is the design as decided; the two implementation details
that differ from the proposal are marked "(as built)".
**Date:** 2026-10-08
**Decided before this proposal** (D-153): the first policy records are export controls on AI chips,
high-bandwidth memory, chipmaking tools and chip-design software.
**Inputs:**
- `entity-taxonomy.md` §1 (R-1 to R-8), §3.7 (the reserved types), §4.2 (policy vs event vs claim), §6
  (the MA dispositions), §7 (the attribute contract);
- `relationship-taxonomy.md` §1 (RR-1 to RR-10), §13 (the reserved verbs);
- `claim-model.md` §2 (normative text reserved for S17), §4, §7;
- `facility-dataset.md` §6 and §7 (events, and a status derived from them);
- `../research/source-policy.md` §2 to §7, §12;
- `baseline.md` §2 (the policy layer must not duplicate `Eu-Digital-Policy`) and §6 (NG-01, NG-02, NG-12);
- MA §3, §5.5 to §5.7, §6.1, §7, §10; `SESSION-ROADMAP.md` S17 and S18;
- the Federal Register's records of the BIS rules, read to see what such a text states (below, "What a
  rule's text gives").

**Claim labels.** The design is the Atlas's choice (`INTERPRETATION`); its consequences are `IMPLICATION`.
The facts about real rules quoted here were read from the Federal Register on 2026-10-08 to inform the
design. They are not records. The records, their sources and their anchors come after H-1, through the
search plan and the human's review (H-2).

**Schemas:** [`schemas/entities.schema.json`](../../schemas/entities.schema.json) (the `policy` type, its
two vocabularies) and [`schemas/events.schema.json`](../../schemas/events.schema.json) (the policy events);
the source class in [`schemas/sources.schema.json`](../../schemas/sources.schema.json).
**Status tool:** [`tools/policy_status.py`](../../tools/policy_status.py), the only home of a policy's status.
**Data:** [`data/policies.json`](../../data/policies.json) and its staging copy.
**Checks:** PL-1 to PL-9 (P-10).

---

## In one paragraph

A policy record describes **one published legal act**, such as one rule the US Bureau of Industry and
Security (BIS) published in the Federal Register. The record holds only what identifies the act: its
official title and citation, who issued it, in which country, what form it takes ("interim final rule"),
what kind of measure it is (an export control) and which act it amends. Each value rests on a claim that
quotes the act's own text. **What the act requires is never a field.** It stays in claims that attribute
the words to the authority ("BIS's rule states that…"). **Its dates are events** (published, effective,
repealed), and its status on any day is computed from those events, never stored. Linking an act to the
companies, parts and technologies it bears on is S18's work. This document only defines the links and the
evidence each needs.

## What a rule's text gives (design reading, 2026-10-08)

The Federal Register's own record of BIS rule 2022-21658 (87 FR 62186, published 13 October 2022) shows
three things the design must handle:

1. **One act, several effective dates.** Its "DATES" section says some instructions took effect on
   7 October 2022 and others on later dates. So a single "effective date" field would be wrong.
2. **Effect before publication.** Those first instructions took effect six days *before* publication.
   So no check may assume "takes effect after publication".
3. **Acts amend a standing regulation.** The rule amends the Export Administration Regulations (EAR),
   15 CFR parts 734 to 774. Later rules (October 2023, December 2024, January 2025) amend the same EAR,
   in part the same entries. So "what is in effect today" is a chain of acts, not one text.

A fourth fact shapes the status rules. The Federal Register's search for the AI Diffusion rule
(90 FR 4544, January 2025) returns no rescinding rule, although a withdrawal has been widely reported. The
Atlas must not show an act as repealed because a withdrawal was announced or reported. Only a text that
repeals it counts.

---

## P-1 Scope and boundary: which instruments the Atlas records

**Proposal.** The Atlas records a policy instrument only when both hold:

1. **It acts on the chain.** It is an industrial, trade, export-control, investment or public-support
   measure, and its text names an item, technology or company class that the Atlas's chain holds (for
   example, it controls "high-bandwidth memory" or semiconductor manufacturing equipment). Each record must
   have its S18 use (R-2): at least one link S18 could evidence.
2. **No other portfolio product owns it.**
   - **`Eu-Digital-Policy` owns EU digital regulation.** As read on 2026-10-08 (read-only copy, commit
     `e37f23b`), it holds 24 EU instruments, among them the EU Chips Act (Regulation (EU) 2023/1781) and
     the Cloud and AI Development Act. The Atlas never records any of them. If a later session needs one, it
     cites the instrument by its official identifier, with no copy of its content, through a new decision.
   - **`Global-AI-Governance` owns comparative governance** (NG-02): who governs AI, through which
     mechanisms, and how jurisdictions compare. The Atlas has no comparative fields, no provisions as
     records, no obligations or enforcement model and no institution profiles.

**Machine-checked for now:** a policy record's issuing jurisdiction must be a `country` record. No EU
jurisdiction exists (D-008, NG-06), so no EU instrument can be recorded until a decision creates one.

**Consequence.** The Atlas becomes the home of a narrow set of non-EU industrial and trade measures, chosen
by what the chain needs. That is far short of a catalogue of statutes.

## P-2 What one record is

**Proposal.** One record is **one act as officially published**:
- a rule in an official journal (each BIS rule in the Federal Register is one record); or
- a codified regulation as a whole (the EAR, 15 CFR parts 730 to 774), which is the standing text that
  rules amend.

**Identity test** (R-1): two records are the same instrument when they have the same official publication
identifier. That is the Federal Register document number for a rule, and the Code of Federal Regulations
parts for a codified regulation.

**ID rule:** `policy-<ISO code of the issuing jurisdiction>-<official identifier as a slug>`. Examples:
`policy-us-fr-2022-21658` and `policy-us-15-cfr-730-774`. The identifier has one home, the ID, as the ISO
code does for jurisdictions.

**Not records:**
- a **provision** (an entry such as ECCN 3A090). Provisions stay outside this repository (D-023). A claim
  cites them as a locator;
- a **press release or fact sheet** about an act. It is a source, which may support an `announced` event;
- a **licence decision or an individual designation**. Neither is needed in S17.

**Alternatives rejected:**
- *one record for "US export controls on AI chips" as a whole*: it has no single text, so no one source
  could support it, and its "status" would have to be invented;
- *one record per provision*: that is governance content (D-023), and the provisions change with every
  amending rule.

## P-3 The fields

| Field | What it holds | Shape | Rests on |
|---|---|---|---|
| `id`, `type`, `name`, `aliases`, `identity_claim_ids` | as for every entity (taxonomy §7); `name` is an editorial label | as today | the identity claims |
| `official_title` | the title as the text prints it | sourced text | the act's text |
| `official_citation` | how the official journal cites it, e.g. "87 FR 62186" | sourced text | the act's text |
| `issued_in` | the jurisdiction whose authority issued it | sourced jurisdiction | the act's text; must be a `country` (P-1) |
| `issuing_authority` | the issuing body, as the text names it (e.g. "Bureau of Industry and Security, Commerce") | sourced text (institutions stay reserved, P-7) | the act's text |
| `instrument_form` | what the act is, in the journal's own label: `codified_regulation`, `interim_final_rule`, `final_rule`, `proposed_rule` | sourced vocabulary value | the act's "ACTION" line, or the code's title |
| `measure_kinds` | what kind of measure: `export_control` only for now; `public_support` and others are added by the session that records the first one | sourced vocabulary list | the act's text stating it |
| `amends` | the act or acts this text says it amends | sourced references to policy records, or `not_applicable` | the act's text |

**Every field is required.** A value the text does not state is `not_researched` or `not_applicable`,
never left out (R-7).

**Deliberately absent:**
- no status;
- no dates (they are events, P-4);
- no summary, content or obligations field (content stays in claims, P-5);
- no "applies to" field (S18's links, P-8);
- no notes field;
- no score.

## P-4 Dates are events; status is derived

**Proposal.** Three new event types, each with a policy as its subject. (As built: the second is named
`effective`, because D-164 makes it the date the act fixes rather than an observation.)

| Event | Meaning | Rests on |
|---|---|---|
| `published` | the act appeared in the official journal on this date | a `FACT` from the journal's own record of it |
| `effective` | all or part of the act has effect from this date, as its text fixes it. An act taking effect in stages has one event per stated date. The date may follow publication: the act's own text fixes it (D-164) | a `FACT` from the act's "DATES" section |
| `repealed` | the act was repealed, rescinded or removed, as a later official text or the authority's official notice of the repeal states | a `FACT` from that text |

The existing `announced` event may also have a policy as its subject: "the authority announced it will
rescind the rule". As for facilities (ER-8), an announcement changes nothing.

**Status is computed** by a new `tools/policy_status.py`, which mirrors `tools/facility_status.py`, for any
date:

| Derived status | When | Shown as |
|---|---|---|
| `has_taken_effect` | an `effective` event lies wholly before the date, and no `repealed` event does | "has taken effect (from <first date>; in stages to <last date> if several); no repeal recorded in the Atlas" |
| `published_not_yet_in_effect` | it was published before the date, and its only `effective` events are after it | "published; takes effect on <date>, as its text states" |
| `not_yet_published` (as built) | the date is before both the act's publication and its first effective date | "not yet published on this date" |
| `repealed` | a `repealed` event lies wholly before the date | "repealed on <date>" |
| `proposed` | the form is `proposed_rule` | "proposed; a proposal never takes effect" |
| `indeterminate` | an event's period contains the date, or events cannot be ordered | "indeterminate on this date" |
| `no_recorded_effect` | no `effective` event is recorded | "no effective date recorded in the Atlas": unknown, never "not in effect" |

**Two rules the checks enforce:**
- a `proposed_rule` never has an `effective` or `repealed` event, so a proposal can never be shown as in
  effect;
- the order of `published` and `effective` is not checked (the 2022 rule took effect before publication);
- an `effective` event may be dated after its source only when that source is the act's own official text
  (EV-3's one exception, D-164).

**Wording.** The Atlas never writes "in force", "legal" or "applies to". It says "has taken effect" and "no
repeal recorded in the Atlas". The second phrase is honest about what the Atlas has not checked: a later
repeal it has not recorded.

**Alternative rejected:** a stored `status` field updated by hand. It would be a second home for what the
events already say (MA §5.6, R-8), and it would go stale silently.

## P-5 Normative text: no new claim type

`claim-model.md` §2 left this open for S17. **Proposal: no new claim type.** A claim's type follows what the
claim asserts:

| What the claim says | Type | Standing | Example (illustration) |
|---|---|---|---|
| a fact about the act as a document: its title, citation, form, publication, the dates its text fixes, what it says it amends | `FACT` | `originator`: the authority made the act, so its text is first-hand for these | "Rule 2022-21658 was published in the Federal Register on 13 October 2022" |
| what the act provides: what it controls, requires or allows | `ATTRIBUTION` to the issuing authority | `originator` | "BIS's rule 2022-21658 states that it adds controls on certain advanced computing items" |
| how the act bears on a company, product or technology | never on a policy record. In S18 it is an `ATTRIBUTION` (the text names it, or a party says so), never an Atlas `FACT` (P-8, P-9) | — | — |

**Checked:** a policy record may cite only `FACT` and `ATTRIBUTION` claims. An `INTERPRETATION`,
`DERIVATION` or `IMPLICATION` on a policy field fails.

**Why not a new type.** A type is justified when the checks would treat it differently (A-1). Here the
existing two already draw the line that matters:
- a dated fact about a published document is checkable like any other `FACT`;
- what a rule requires is the authority's statement, true *as an attribution* whatever its later legal
  fate.

Treating "the rule says X" as `ATTRIBUTION` also keeps the Atlas from writing a rule's content in its own
voice, which is the first step toward advice.

**Alternative:** a `NORMATIVE` claim type. It would need its own rules in every check and table, for no
different treatment.

## P-6 A source class for official legal texts

**Proposal.** A twelfth source class, `official_legal_text`: *the text of a law, regulation or rule as
published in an official journal or official code by, or for, the body that issues it* (e.g. the Federal
Register and Code of Federal Regulations editions on govinfo.gov, or the Official Journal of the EU).

**Why a new class, not `government_publication`.** The same agency publishes the rule and a press release
about it. Both would be `government_publication`. But only the rule is the act; a press release saying "BIS
rescinds" is an announcement (ER-8). A separate class lets the matrix demand the official text for the
dates and the repeal. It also stops a press release from making an act look repealed or in effect.

**Neighbour test** (§3): *Is the document the act itself, as the official journal or code publishes it?*

**What changes in `source-policy.md`:**
- §2 gains the class and its "primary for" line;
- §3 gains the neighbour test;
- every existing matrix row places `official_legal_text` under "never sufficient alone". No current record
  rests on one, so no check is loosened;
- §7 gains **eleven rows**: `identity:policy`, the seven `attr:policy.*` fields and `event:published`,
  `event:effective`, `event:repealed`. Each row's preferred class is `official_legal_text`. For
  `issuing_authority` and `measure_kinds`, `government_publication` (the agency's own pages) is
  acceptable. Standing is "party or originator", and freshness is `stable`, because a published text never
  changes;
- the `event:announced` row already allows `government_publication`, which covers an agency announcing a
  rescission.

**Matrix after the change:** 47 rows, 12 classes.

## P-7 Institutions stay reserved

**Proposal.** Keep `institution` reserved (D-022). The issuing authority is a sourced text field
(`issuing_authority`).

**Why.** No check or link needs BIS as a record yet. Making it one would open questions S17 does not need to
answer: what an agency is, how agencies nest, and how an agency differs from a government. It would also
drift toward `Global-AI-Governance`'s institutions.

**Cost.** Two acts by the same authority repeat its name as text, a weak second home. A later session can
replace the text with a reference when a link to an institution has a use.

## P-8 The links S18 will record (defined here, none recorded)

The four verbs reserved since S04 (D-030) are ruled on as follows. Every link is stored **from the policy to
what it acts on**, the activity direction (RR-1, RR-3). MA's `restricted_by` and `supported_by` become the
inverse readings shown to readers.

| Verb | Proposal | From → to | What the evidence must show |
|---|---|---|---|
| `restricts` | **define** | policy → component, technology, product or company | **The act's own text names the target**: an item class in its own words (e.g. "high-bandwidth memory"), a named product, or a named company (e.g. an Entity List entry), or **a party states that the act applies to its own product** (e.g. a vendor's filing). Matching a text's term to an Atlas class is a separate `DERIVATION` comparing the text's words with the record's definition. **Never** the Atlas applying a technical threshold to a product (P-9) |
| `supports` | **define, not instantiable yet** | policy → company or facility | the act, or the authority's official award notice, names the recipient. Instantiable only when a session records public-support instruments, with their own matrix rows |
| `regulated_by` | **reject** | — | too broad to evidence (RR-10); regulatory content belongs to `Eu-Digital-Policy` and `Global-AI-Governance` |
| `constrained_by` | **reject** | — | as S04 warned, it has no precise meaning beyond `restricts`; a market constraint is a claim, not an edge |

**Level.** A policy link goes from a named act to either a class (HBM) or a named thing (a product).
RR-2 ("one verb, one level") would forbid that. S18 amends RR-2 for policy links: the evidence is the same
either way (the text naming the target), so a third "policy" level is proposed.

**Time.** A link carries no dates of its own. While the act has effect is derived from its events (P-4).
Whether a later rule narrowed the target is S18's to model.

## P-9 Description, never advice

Rules for every record, claim, link and page of the policy layer (CLAUDE.md §13, NG-12):

| ID | Rule |
|---|---|
| LA-1 | The Atlas states what a text says (`ATTRIBUTION`) and the dates its text fixes (`FACT`). It never states what anyone must or may do |
| LA-2 | No field says that an act applies to a firm or product. Only an S18 link can, and only on the evidence in P-8 |
| LA-3 | The Atlas never applies a threshold, definition or exemption to a product or firm. A product "meeting" an export-control threshold is a legal determination, and it is refused as a link candidate |
| LA-4 | The only status words are those of P-4. "In force", "legal", "compliant", "licence required" and "prohibited" never appear in the Atlas's own voice |
| LA-5 | Wherever a policy record is shown, its official text is linked, and the page says it describes and does not advise. That note never stands in for LA-1 to LA-4 |

LA-1 is enforced through P-5's check (only `FACT` and `ATTRIBUTION` claims), and LA-2 through the
schema (no such field). LA-3 and LA-4 are review rules for the human's H-2 review, the Verifier and the
pages (no page is built in S17).

## P-10 Checks, written first

| Check | What fails | Test |
|---|---|---|
| PL-1 | a policy record whose shape breaks P-3, including a `status`, a date, a summary or any other unlisted field | `tests/test_entity_schema.py` |
| PL-2 | an ID not of the form `policy-<code>-<slug>`, or whose code is not that of its `issued_in` value | `tests/test_data_entities.py` |
| PL-3 | `issued_in` that is not an existing `country` record (P-1) | `tests/test_data_entities.py` |
| PL-4 | `amends` naming a missing record, a non-policy, itself, or forming a cycle | `tests/test_data_entities.py` |
| PL-5 | a policy record citing a claim that is not `FACT` or `ATTRIBUTION` (P-5, LA-1) | `tests/test_data_entities.py` |
| PL-6 | a `published`, `effective` or `repealed` event whose subject is not a policy; an `effective` or `repealed` event for a `proposed_rule`; an event dated after its source, unless it is an `effective` date cited from the act's own text (D-164) | `tests/test_data_events.py` |
| PL-7 | the status derivation, on fictional events: staged effect, effect before publication, repeal, proposal, an unknown, an announced rescission that changes nothing | `tests/test_policy_status.py` |
| PL-8 | the new class missing from any matrix row, or a policy field or event type without its row; a policy row that does not prefer the official text; a policy date or repeal that a government publication could support; an earlier row that lets the new class support a record alone | `tests/test_source_policy.py` (reads the schemas) and `tests/test_policy_layer.py` |
| PL-9 | a relationship with a policy endpoint (nothing until S18) | the relationship schema (prefixes), tested in `tests/test_policy_layer.py` |

The existing checks that read every entity kind apply to policies unchanged:
- references resolve;
- placeholder slugs are refused;
- V-10 matrix support;
- canonical records rest on canonical claims;
- the taxonomy's MA disposition table (updated so that `PolicyInstrument` is `type:policy`, and
  `TradeMeasure` and `ExportControl` are `measure_kinds` values or future values).

**Breaks for S17** (`S17-…`): one planted fault per check above, plus a control.

**Files:** `data/policies.json` (canonical) and `data/staging/policies.json`. Policy events join
`data/events.json`. `tools/trace.py` reads the new file. No page, no SQL query and no new dependency.

## P-11 The first instruments

**Proposal: five records**, chosen because their texts name what the chain holds:

| Record | Official citation (to verify at retrieval) | Bears on, for S18 |
|---|---|---|
| The Export Administration Regulations, 15 CFR parts 730 to 774 | Code of Federal Regulations, govinfo edition | the standing text the four rules amend |
| BIS rule of 13 October 2022, advanced computing and semiconductor manufacturing items | 87 FR 62186 (2022-21658) | data-centre GPUs and AI accelerators (H100); manufacturing equipment |
| BIS rule of 25 October 2023, advanced computing items: updates and corrections | 88 FR 73458 (2023-23055) | accelerators; its text mentions high-bandwidth memory |
| BIS rule of 25 October 2023, semiconductor manufacturing items | 88 FR 73424 (2023-23049) | lithography and other equipment (ASML) |
| BIS rule of 5 December 2024, foreign-produced direct product rule additions and refinements | 89 FR 96790 (2024-28270) | high-bandwidth memory (SK hynix, Samsung, Micron); equipment |

**Optional additions**, each about one more record and its claims:
- **the August 2022 rule on chip-design (ECAD) software** (87 FR 49979), which bears on Synopsys and EDA;
- **the January 2025 AI Diffusion rule** (90 FR 4544). It tests the status rules on a reported withdrawal.
  It needs a search for any rescinding text, and if none is found it stays "has taken effect; no repeal
  recorded", beside an `announced` event if BIS's own announcement is retrieved.

**Per record:** about six to eight claims: title, citation, authority, form, measure kind, what it amends,
and its dates. All of them are put to the human at H-2.

---

## Rulings (H-1, 2026-10-08)

Decided by the human on 2026-10-08, item by item; outcomes only (D-114).

| Item | Outcome | Decision |
|---|---|---|
| P-1 Scope | chain-bound, non-EU instruments only; a country issuer is checked | D-154 |
| P-2, P-3 Record | one published act per record, the seven fields | D-155 |
| P-4 Status | derived from dated events, never stored | D-156 |
| P-4 Effective dates | a date the act fixes in advance comes from the act's own text (asked after the three rounds, before any check was written) | D-164 |
| P-5 Claim types | `FACT` for what the act fixes about itself, `ATTRIBUTION` for what it provides | D-157 |
| P-6 Source class | a new class, `official_legal_text` | D-158 |
| P-7 Institutions | stay reserved; the authority is text | D-159 |
| P-8 S18 links | `restricts` and `supports` defined; `regulated_by` and `constrained_by` rejected | D-160 |
| P-9 No advice | the five rules LA-1 to LA-5 | D-161 |
| P-10 Checks | written first, with breaks | D-162 |
| P-11 First records | the core five | D-163 |
