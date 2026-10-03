# Facility dataset — sites, their location, and the events that date them

**Status:** ACCEPTED (S09 reviews, 2026-10-02): D-083 and D-084 ("Approve both
(Recommended)"), the flagged rulings of D-080, D-081 and D-083 ("pick your
recommendations"), and D-078 to D-082 and D-085 to D-088 ("Approve all (Recommended)"). D-088
accepts the gap and the proposal; no schema is changed. The records are canonical (§10).
**Session:** S09 · **Date:** 2026-10-02
**Inputs:**
- `entity-taxonomy.md` §3.2 (facility), §4.2 (company vs facility), §4.4 (a plan is not an
  edge), §7 (attribute contract), §9 (event schema owner);
- `relationship-taxonomy.md` §4.3 (`owns`), §4.4 (`operates`), §5 (evidence expectations),
  §10 (time);
- `../research/source-policy.md` §4 (standing), §6 (ER-8, ER-9), §7 (rows
  `identity:facility`, `attr:facility.*` and, from S09, `event:*`), §11 (RA-1 to RA-7), §12;
- `claim-model.md` §2 to §4, §7; `company-dataset.md` (the patterns reused: staging,
  attested anchors, the ISO 3166-2 derivation, record checks); `concept-dataset.md`
  (re-retrievals, D-075; basis tables, IO-1);
- MA §5.5 (event), §5.6 (status semantics), §5.7;
- the S09 prompt, Part B, with the human's answers H-1 to H-6 and the three answers given at
  the start of S09 (D-078, D-084).

**Schemas:** the entity schema is unchanged; facility records follow
[`schemas/entities.schema.json`](../../schemas/entities.schema.json) as accepted in S03.
Events follow the new [`schemas/events.schema.json`](../../schemas/events.schema.json)
(proposed, D-083).
**Data:** [`data/facilities.json`](../../data/facilities.json) and
[`data/events.json`](../../data/events.json) (canonical), with their staging copies under
[`data/staging/`](../../data/staging/) (H-5).

**One home for each kind of statement:**

- **The schemas** hold the record shapes, the facility-kind and event-type vocabularies
  and their one-line definitions.
- **This document** holds the reasoning: which candidate sites became records and why the
  others did not; the facility and event ID rules; how a location is evidenced and what may
  never evidence it; which words establish a facility kind; the ownership and operation
  evidence handed to S10; how status is derived; the record checks.
- **`tools/facility_status.py`** holds the status derivation, the only home of a facility's
  status (§7).
- **The records** hold the values, and **the claims** hold the sentences and sources.
  Nothing in this document is a value of a record.
- **Checked by** `tests/test_data_entities.py`, `tests/test_data_events.py`,
  `tests/test_facility_status.py` and `tests/test_data_integrity.py`.

**Claim labels.** The rules are the Atlas's design (`INTERPRETATION`), and their
consequences are `IMPLICATION`. What a filing or a release says is cited through a claim in
`data/`, never stated here as a fact.

---

## 1. Scope: which sites became records (H-1)

**Rule** (D-078). A facility record needs, from a source its rows accept, a sentence that
names **one site**, places it, and says what it does in words that fit one of the schema's
facility kinds. A site known only from a plan is an event, not a facility (ER-8; Part B
§16). The search started from the registered filings (H-1: "Filings' fabs + packaging
(Recommended)"), re-retrieved first (H-4, D-075).

| Candidate | What the sentences give | Outcome |
|---|---|---|
| Micron, Manassas | the 10-K names "our fab in Manassas, Virginia" (`src-025` p.48) | record `facility-us-manassas-virginia` |
| Micron, Boise and Clay | fabs under construction or planned; the 10-K dates one announcement (June 2025) | event `event-micron-technology-announced-2025-06`; no facility record (ER-8) |
| Micron, Taiwan, Singapore, Japan, Malaysia, China, India | the properties table names countries, not sites; the Hiroshima facility is in Japan, which has no jurisdiction record | no record: no site sentence, or no jurisdiction record |
| SK hynix, M16 (이천) | the filing dates M16's completion in 이천 (`src-046`) and places the company's production plants in 경기도 이천시 (`src-047`); SK hynix's release calls M16 a "new fabrication plant" (`src-049`) | record `facility-kr-m16`; event `event-kr-m16-opened-2021-02` |
| SK hynix, M15X (청주) | a fair-disclosure plan of 2022-09-06 to build M15X (`src-048`) | event `event-sk-hynix-announced-2022-09-06`; no facility record (ER-8) |
| SK hynix, Cheongju plants and M15 | the filing names production plants in 충청북도 청주시, but no sentence read gives a site's kind, and no ISO 3166-2 claim covers 충청북도 | no record |
| Amkor, Arizona | under construction (10-K); the IR release of 2026-09-08 announces phase 2 (`src-050`) | event `event-amkor-technology-announced-2026-09-08`; no facility record (ER-8) |
| Amkor, other factories | the 10-K's properties table gives country totals, not sites | no record |
| ASML, Veldhoven and other sites | the 20-F names its manufacturing sites (`src-029`), but they make lithography systems, and no facility kind fits | **stop condition; gap** (D-088) |
| TSMC | the 20-F lists fabs; its host refuses automated requests, and the file was not re-supplied during S09 | **gap**: the human chose "Close as a gap (Recommended)"; the RA-4 request stays open |
| Data centres | the Amazon and NVIDIA filings name no data-centre site | no record (§8) |

**ASML** (D-088, the human's answer "Gap + proposal (Recommended)"). The schema's facility
kinds are `wafer_fab`, `packaging_facility` and `data_centre`. ASML's sites assemble and test
lithography systems, so a record would need a value the accepted schema lacks (Part B §16).
The sentence is kept as a staging claim (`claim-asml-manufacturing-sites`), and D-088
proposes a kind for a later session. No schema is changed.

## 2. Facility identity and IDs (FI-1, machine-checked)

**What one record is** (`entity-taxonomy.md` §3.2). One site at one location, at the
finest unit the first-hand source names as a site: a named plant ("M16") or, where the
source gives no name, the site it places ("our fab in Manassas, Virginia"). Production lines,
clean rooms and construction phases are sub-site detail and get no record. A site the
source names only as part of a group ("production plants in 경기도 이천시") is not one
record, because it may be several sites.

**ID rule** (D-079). `facility-`, the ISO 3166-1 alpha-2 code of `located_in` in lower case,
`-`, and the slug of the site's **term**:

- the **term** is the site's own name as an identity anchor gives it, verbatim; where the
  source gives the site no name, the term is the locality as the identity anchor gives it;
- the slug is lower-case ASCII words joined by `-`, as `concept-dataset.md` §3;
- the ID never contains an owner or operator, so it survives a change of either
  (`entity-taxonomy.md` §3.2). A renamed site keeps its ID: the term is the one first
  recorded;
- a site with no `located_in` value gets no record: a site no source places is not yet a
  record, and the code is part of its ID;
- a collision (two sites with one ID) needs a decision. None exists.

**Why the code and the term, and not an owner.** An owner prefix would make an ID wrong after
a sale. The code and the term are claim-backed and do not change while the site exists.
**The display name** is free and editorial. A test changes it and checks that no ID error
appears.

The rows (facility, term, what the term is) are data: `data/identity_basis.json`, kind
`facility_term` (S14, DT-1, D-117). `tests/test_data_entities.py` reads them. It recomputes each ID from the record's
`located_in` and the term, checks that the term is verbatim in an identity anchor, and that
every facility record has a row.

To list them: `python -m json.tool data/identity_basis.json`.

## 3. Location (HQ-1, machine-checked)

**Rule** (D-080). `located_in` and `locality` rest only on a sentence that places **the
site** (R-5; `source-policy.md` §7 rows `attr:facility.located_in`, `attr:facility.locality`):

- **Never** a headquarters, head office, principal office, incorporation, registered office
  or listing sentence, even when the site and the head office share a town. SK hynix's
  release places M16 "at headquarter located in Icheon, Gyeonggi-do, South Korea"; that
  phrase is not used.
- **From a city or province to the country:** as D-057. When the site sentence names a
  subdivision, `located_in` is a `DERIVATION` whose inputs are the site claim, the ISO
  3166-2 claim for that subdivision and the ISO 3166-1 claim for the country. The ISO
  claims are canonical since S07.
- **`locality`** is the place exactly as the site sentence gives it, in the source's script
  ("이천", not a romanisation).

**HQ-1 checks two things** for every facility's `located_in` and `locality`:

1. no anchor reached from their claims (through inputs) contains a word in the table below,
   matched without regard to case;
2. no claim reached from them is also reached from a company's `headquartered_in` or
   `incorporated_in`, except claims whose every citation is a `standard_specification` (the
   ISO claims, which serve both).

| Excluded word | Why |
|---|---|
| headquarter | a headquarters sentence (R-5) |
| head office | SK hynix's and TSMC's term for the headquarters |
| 본사 | the Korean term for the head office |
| principal executive office | the 10-K cover's address field (`company-dataset.md` §13) |
| principal office | the same, in other filings |
| incorporat | an incorporation sentence |
| registered office | a statutory seat |
| listed on | a listing sentence |

**What HQ-1 cannot see.** A site sentence that silently copies the head-office town passes.
The Verifier reads each sentence, and the human's review is the check (§10).

## 4. Facility kinds (FK-1, machine-checked)

`facility_kinds` is an identity field: it has no claim field of its own (`entity-taxonomy.md`
§7). So, as IO-1 does for `instance_of` (`concept-dataset.md` §7), each kind of each record
has a basis row naming an identity claim and the word in its anchor that gives the kind
(D-081).

**The words** that establish each kind. A kind whose word is not in this table needs a new
row, by decision:

| Kind | Words |
|---|---|
| `wafer_fab` | fab; fabrication plant; fabrication facility; wafer fab |
| `packaging_facility` | packaging facility; assembly and test facility; backend fab |
| `data_centre` | data center; data centre |

"Fab" is the industry's short form of "fabrication facility", and "fabrication plant" is
SK hynix's English wording. Reading either as `wafer_fab` is the Atlas's ruling, flagged for
the human (D-081).

Each record's basis rows are data: `data/identity_basis.json`, kind `facility_kind_basis`
(S14, DT-1, D-117).

The check requires a row for every kind on every record and a kind for every row; the
basis claim among the record's identity claims; the word in one of its anchors; and the word
in the kind's row above.

## 5. Ownership, operation and production (H-3)

**Rule** (D-082). S09 records the sentences as claims and creates no edge (H-3: "Claims now,
edges in S10 (Recommended)"). Owner and operator are never facility fields: the schema has
none, and VD-2 rejects one. Each candidate sentence is marked against
`relationship-taxonomy.md` §5:

| Facility | Claim | `owns` (§5) | `operates` (§5) | For S10 |
|---|---|---|---|---|
| `facility-us-manassas-virginia` | `claim-micron-manassas-fab` | **fails**: "our fab" is possession, not stated controlling ownership; in a consolidated 10-K "our" spans subsidiaries, so the legal owner is not named | **fails**: the company is not stated as running the site | no edge from this source; an ownership or operation statement (a property note, a register, a permit) is needed |
| `facility-kr-m16` | `claim-sk-hynix-production-plants-icheon-cheongju` | **fails**: 설치 ("installed") is not ownership | **partly meets**: SK hynix Inc., the entity of the separate statements, is stated as operating (가동) production plants in 경기도 이천시; the site is named by its town, not as M16 | an `operates` edge only as a `DERIVATION` with `claim-sk-hynix-m16-completed-icheon` (M16 is a plant in 이천). S10 decides whether that meets §5 |
| `facility-kr-m16` | `claim-sk-hynix-m16-fabrication-plant` | **fails**: "its new fabrication plant" is possession | **fails**: no running is stated | — |

**Production.** What a site does is its `facility_kinds` (§4). Which product a site makes
has no v1 relation type (`relationship-taxonomy.md` §15). SK hynix's release says M16 "will
be a manufacturing site mainly for DRAM products": a 2021 intention (ER-8), and DRAM is no
v1 component, so nothing is proposed.

**Finding** (`IMPLICATION`). The filings place and date sites, but none read states who owns
a named site. S10's `owns` edges will need other evidence than the properties sections.

## 6. Events (H-2, machine-checked)

**Schema** (D-083, proposed). `schemas/events.schema.json`: `id`, `event_type`, `subject`,
`date` (a partial date at the source's precision) and `claim_ids`. Four types, from MA §5.5:
`announced`, `opened`, `expanded`, `closed` (H-2). There is no status field, no planned
date and no owner field.

**A plan is never an occurrence** (ER-8):

- `opened`, `expanded` and `closed` are **occurrences**. Their subject is a facility, and
  they rest on at least one `FACT` or `DERIVATION`.
- `announced` is a **plan**. It rests on `ATTRIBUTION` claims only, and its date is the date
  of the announcement, never the date the plan names. Its subject is the facility when the
  plan concerns an existing record, and otherwise the announcing company, because a planned
  site gets no facility record (§1).
- An event never points to an edge, and nothing points to an event except the status
  derivation (`relationship-taxonomy.md` §10).

**Dates (EV-3).** An event is never dated after a source that states it: its date is no
later than the latest date each cited source states for itself (or, for an undated source,
its access date), compared at the coarser precision.

**ID rule (EI-1, D-083).** `event-`, the subject's ID without its type prefix, `-`, the event
type, `-`, and the date as recorded (e.g. `event-kr-m16-opened-2021-02`). A collision needs a
decision.

**`opened` and 준공.** SK hynix's filing lists M16's 준공 (completion of construction). The
`opened` type covers "completed or began operating", so the claim says which: completion.

**Evidence rows** (D-084, the human's answer "Add the rows (Recommended)"). Each event type has
a row in `source-policy.md` §7, and V-10 checks event claims against it (EV-4).

## 7. Status is derived, never stored (machine-checked)

**Rule** (D-085). `tools/facility_status.py` derives a facility's status on a date from the
occurrence events whose subject it is. `announced` and `expanded` never change it.

| Derived status | When |
|---|---|
| `opened` | the latest occurrence wholly before the date is `opened` |
| `closed` | the latest occurrence wholly before the date is `closed` |
| `not_yet_opened` | no occurrence before the date, and an `opened` event after it |
| `indeterminate` | an occurrence's period contains the date (e.g. "2021-02" asked about 2021-02-10), or two occurrences of different types cannot be ordered |
| `no_recorded_opening` | no occurrence at all. Unknown: never read as "not operating" |

"Wholly before" means the last day of the event's period is on or before the date. The
status is computed when asked, so nothing can contradict it. `opened` means completed or
began operating on that date, as the claim says; it never means "operating today".

```bash
python tools/facility_status.py facility-kr-m16 --on 2026-10-02
```

## 8. Capacity and data centres (CAP-1, machine-checked)

**Rule** (D-086). `nameplate_it_capacity_mw` is `not_applicable` on a facility without the
kind `data_centre`. On a data centre, a value needs an anchor that says the figure is IT
capacity (TQ-10), matched by one of: `nameplate`; `IT load`; `IT capacity`;
`critical IT`. A power, grid or interconnection figure is a different quantity (EN-02).

**No data centre in S09.** The registered Amazon and NVIDIA filings name no data-centre site,
and a region or availability zone is never a facility (D-022). The canonical finding
`claim-cloud-compute-facility-often-undisclosed` stands.

## 9. Sources and access

**Re-retrievals** (D-075, H-4). On 2026-10-02, `src-024` to `src-030` returned their
registered bytes. `src-031` (TSMC's 20-F) is behind a challenge page (HTTP 403), as in S07.
The human agreed to re-supply it (RA-4), but it did not arrive during S09, so the human closed
TSMC's sites as a gap; `src-031` was not cited again (D-075).

**New sources** (`src-046` onward), retrieved automatically on 2026-10-02 with full hashes;
texts stay outside the repository (RA-4(4)):

| Source | What | Class |
|---|---|---|
| `src-046` | SK hynix annual report for 2025, section I.2 "Company history" (English DART) | `company_filing`, `regulator_hosted` (D-059) |
| `src-047` | the same report, notes to the separate financial statements, note 1 "Company overview" | `company_filing`, `regulator_hosted` |
| `src-048` | the same report, section XI.1 "Progress and changes of disclosure information" | `company_filing`, `regulator_hosted` |
| `src-049` | SK hynix Newsroom, "SK hynix Announces the Completion of M16 Plant Construction" (2021-02-01) | `company_press_release` |
| `src-050` | Amkor IR, "Amkor Technology Announces Phase 2 of Arizona Advanced Packaging and Test Campus" (2026-09-08) | `company_press_release` |

Each DART section is served at its own URL with its own bytes, so each is its own record, as
`src-030` is for section I.1.

**Access gaps** (SP-7; nothing bypassed, RA-2): `investor.tsmc.com` and `www.tsmc.com`
(HTTP 403 challenge, 2026-10-02). English DART dropped many connections during a scan of the
report's sections; every section was read after slower retries.

## 10. Staging, canonical and the human's review (H-5, H-6)

As D-061 and D-077 (D-087): `data/facilities.json` and `data/events.json`, each with a
staging copy. A record becomes canonical only on the human's verdict, and only if every
claim it cites is canonical. CE-1 extends to facilities, and EV-1 to events: a canonical
event cites canonical claims and has a canonical subject.

**What the S09 review promoted** (2026-10-02, "Accept all (Recommended)"): all 10 claims, both
facilities and all four events. Nothing S09 created stays in staging.

**Review.** For each claim on the sheet in the S09 report:

1. Run `python tools/trace.py <record ID>`.
2. Open the source at the locator and read the whole sentence.
3. Answer:
   - **Each site claim:** does the sentence name this one site, and place it?
   - **Each location:** does it rest on the site sentence, never on a head-office one?
   - **Each kind:** does the word give the kind (§4)?
   - **Each event:** is an occurrence stated as having happened, and a plan only as a plan?
   - **Korean text:** is the translation faithful?
4. Give a verdict per claim: accept, reject, or "wording too strong".

The flagged rulings are asked as separate questions, with what an unticked box means.

## 11. validate-data for facilities and events

| Check | What it checks | Where |
|---|---|---|
| VD-2 (extended) | facility records against the entity schema; events against the event schema | `tests/test_data_schema.py` |
| V-1, V-4, V-9, V-10, CE-1 | as for the other kinds; `located_in` resolves to a jurisdiction | `tests/test_data_entities.py` |
| FI-1 | §2 | `tests/test_data_entities.py` |
| HQ-1 | §3 | `tests/test_data_entities.py` |
| FK-1 | §4 | `tests/test_data_entities.py` |
| CAP-1 | §8 | `tests/test_data_entities.py` |
| EV-1 | the subject and claims resolve; a canonical event cites canonical claims and has a canonical subject; no ID is both staging and canonical | `tests/test_data_events.py` |
| EV-2 | §6: occurrences rest on a `FACT` or `DERIVATION` and have a facility subject; plans rest on `ATTRIBUTION` only | `tests/test_data_events.py` |
| EV-3 | §6: no event dated after a source that states it | `tests/test_data_events.py` |
| EV-4 | V-10 for events, against the `event:*` rows | `tests/test_data_events.py` |
| EI-1 | §6 | `tests/test_data_events.py` |
| ST-1 | §7: the derivation, on fictional events and on the real ones | `tests/test_facility_status.py` |
| F-1 | unchanged: only `attr:facility.nameplate_it_capacity_mw` is `time_sensitive`, and no S09 record has a value | `tests/test_freshness.py` |

```bash
python -m unittest discover -s tests -p "test_data*.py" -v   # validate-data
python -m unittest discover -s tests -p "test_freshness.py" -v   # validate-freshness
```

## 12. Candidates considered and rejected

| Candidate | Why not |
|---|---|
| IDs with the owner's or operator's slug | wrong after a sale (§2) |
| IDs from the display name | editorial (§2) |
| A record for "SK hynix production plants in 이천" | a group, possibly several sites (§2) |
| A facility record for a site under construction (Micron Boise, Amkor Arizona) | a plan is an event (ER-8; Part B §16) |
| M16 located from the release's "at headquarter located in Icheon" | a head-office phrase (R-5, §3) |
| A stored status, or a status read from the last event in the file | a second home; status is derived (§7) |
| An `announces` field naming the kind of change a plan describes | no check or status needs it; the plan's content is in its `ATTRIBUTION` claim |
| A planned-date field on events | it would let a plan look like a state (ER-8) |
| A `construction_started` event type | not in H-2's four types; Micron's and Amkor's construction starts are left unrecorded |
| `wafer_fab` for ASML's sites, or a schema change now | the kind does not fit; the human chose gap and proposal (D-088) |
| A facility kind read from the company's role (a memory maker's plants are fabs) | R-3: roles are not facts about a site |

## 13. What S09 leaves to other sessions

| Item | Owner | Note |
|---|---|---|
| `owns` and `operates` edges from the §5 claims | S10 | most candidates fail §5 |
| A facility kind for equipment manufacturing (ASML) | a later session, by decision | D-088 |
| Micron's Japan and Taiwan sites; SK hynix's Cheongju plants and M15; Amkor's factories | the session that registers JP and the needed subdivisions, or reads site-level sources | §1 |
| TSMC's fabs and advanced-backend sites | S10: the human asked to carry the RA-4 request into S10 ("Carry into S10 (Recommended)") | §1, §9 |
| A `construction_started` type, and MA §5.5's other types | the session that needs them | §12 |
| Data-centre sites | the session that finds a first-hand site sentence | §8 |
