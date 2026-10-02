# Source policy — which sources the Atlas believes, and for what

**Status:** ACCEPTED (human review of S05, 2026-09-30): D-034 to D-041; with D-042 and D-043.
**Week-2 gate:** passed (human decision, 2026-09-30, after reading §14: "Accetto s14").
**Amended in S09:** §7 gains one row per event type (D-084; the human approved adding
them at the start of S09, 2026-10-02: "Add the rows (Recommended)"; the rows' content is
proposed with D-084).
**Session:** S05 · **Date:** 2026-09-30
**Inputs:**
- `../architecture/relationship-taxonomy.md` §5 (evidence expectations), §9 (unknown and
  non-public edges), §12 (worked examples);
- `../architecture/entity-taxonomy.md` §3.7 (publishers) and §7 (attribute contract);
- `source-register.md` (SRC-001 to SRC-023, its notes and its access-gap tables);
- `domain-map.md` "How to read this map", §5 (CON-01 to CON-05) and §8;
- MA §5.2–5.3, §5.7, §10, §16; PEF §6; decisions D-014, D-015, D-022, D-025, D-028, D-031.

**Schema:** [`schemas/sources.schema.json`](../../schemas/sources.schema.json) (the class
vocabulary only; S06 builds the source record around it).

**One home for each kind of statement:**

- **The schema** holds the class values and their one-line definitions.
- **This document** holds the reasoning:
  - the test that separates each class from its neighbours (§3);
  - what each class is primary for, and never enough for (§2);
  - the preferred classes for every material claim type (§7);
  - the class of every registered source (§8), until S06 migrates the register;
  - the conflict, retrieval and freshness rules (§10–§12).
- **Not here.** What a source must *show* for each relation type stays in
  `relationship-taxonomy.md` §5. The matrix (§7) points to those rows by type and never
  restates them. Field meanings stay in `entities.schema.json`.
- `tests/test_source_policy.py` checks the tables against the schemas, the register and
  the domain map.

**Claim labels.** The policy is the Atlas's design (`INTERPRETATION`), and its
consequences are `IMPLICATION`. Where it says what a real source contains, it gives a
register ID with a locator, or an S05 retrieval (§8.3) with URL, access time and hash.
No numeric score, rank or confidence value appears anywhere in this policy (D-028,
NG-11).

---

## 1. Principles

| ID | Principle | Why |
|---|---|---|
| SP-1 | **A class describes a document and its publisher, not whether it is true.** A datasheet can be wrong; a marketing page can be right. The class says what the document is *for* and who answers for it | MA §10: "The source hierarchy is guidance, not a substitute for checking whether the source actually supports the claim" |
| SP-2 | **Preference depends on the claim type.** There is no global ranking. A vendor's product page is the preferred evidence that the product exists, and is never enough for a technology definition | §7; D-036 |
| SP-3 | **"Primary" is a relation between a source and a claim, not a class.** A source is first-hand for a claim when its publisher is a party to it or originated it (§4) | S04 finding; D-035 |
| SP-4 | **Statements, not only pages, carry attribution.** A superlative or exclusivity claim is `ATTRIBUTION` in every class, including filings and technical documentation | D-015; ER-5 |
| SP-5 | **A preferred class is never a verification.** Nothing is supported until the Verifier finds the statement at its locator, and the wording does not exceed it | MA §10; ER-10 |
| SP-6 | **Conflicts are recorded, never settled by rank.** A conflict closes only when new evidence explains it, and a material one only with a human decision | §10; CLAUDE.md §9 C/D |
| SP-7 | **An access gap is a gap, not a search.** A source that could not be read supports nothing, including a finding that something is not public | ER-3; D-014 |

## 2. The source classes (machine-checked against the schema)

The vocabulary has 11 classes. The definitions are in the schema. Company documents get
several classes, because company sources differ most in what they are accountable for: the same
firm publishes a filing, a datasheet, a press release and a product page, and each is
evidence of something different.

| Class | Primary for (first-hand, §4) | Never enough on its own for |
|---|---|---|
| `company_filing` | The filer's own identity, legal name, incorporation and principal office; its subsidiaries; its business model; supply relations it states with named firms (S05-R1 p.1, p.8, p.88) | A product-level edge or supplier, when the filing speaks at company level (ER-9); its forward-looking statements as states of the world (ER-8); class-level technical necessity |
| `company_technical_documentation` | Its own product's specifications, contents and process name; its own service's availability; design statements about its own products (SRC-006, SRC-008) | Comparative or superlative statements (ER-5); class-level necessity, because it is one vendor's description (taxonomy §5 `requires`); a fabricator read from a process name (ER-1) |
| `company_press_release` | That the company announced something on that date (an event, S09); its own stated intentions, as `ATTRIBUTION`; transactions it is party to (SRC-014) | That a plan was carried out (ER-8); any state after the release date; class-level claims |
| `company_marketing` | That the company offers a named product; how the vendor names and describes its own products (SRC-007) | Technology or component definitions: the roadmap's S08 mission is to model them "independently of company marketing language"; class-level necessity; exclusivity or leadership (ER-5); anything about another firm |
| `standard_specification` | As originator: standardised terms, interfaces, generations and measurement methods; structures a standard mandates for every conforming instance | Which firm makes, supplies or uses anything; adoption or market state |
| `government_publication` | As originator: definitions it issues (SRC-001); official-register facts (incorporation, permits, site location); its own programme facts (SRC-004) | Company activity it only reports; data it takes from others (ER-6) |
| `research_report` | As originator: its own methods, measurements and estimates (as `DERIVATION` or `ATTRIBUTION` of the estimate); technical definitions in its own work (SRC-021) | Data it reports from others (ER-6; SRC-021 p.31, p.33); company-specific edges; anything outside its stated scope |
| `policy_research_brief` | Its own assessments and glossary definitions, as `ATTRIBUTION` (SRC-002, SRC-003) | Facts about named companies; market data, which it reports with an as-of date (SRC-002 p.5: "current as of 2019"); technical necessity |
| `industry_association` | Its own positions and definitions, as `ATTRIBUTION` (SRC-005) | Any fact about its members or the market; a definition that other sources contest (CON-03, CON-04). It states a representational role (SRC-005 p.2) |
| `market_research_consultancy` | Its own estimates, as `ATTRIBUTION` | Any record. Its data usually reaches the Atlas second-hand and cannot be retrieved: SRC-021 lists IDC data as purchased (p.33) and cites an IDC analyst's personal communication (p.31) |
| `news_media` | That the outlet reported something on its date, as `ATTRIBUTION` | Any record. It is a route to the primary source, which must then be retrieved |

**What is not a source.** Search results, snippets, aggregator copies (sites that repost a
filing or a report) and tertiary summaries are discovery aids. They get no class and are
never cited (D-014; MA §11.2). The S05 search for a filing returned the company's copy and
several aggregator copies. Only the company's copy was retrieved (§8.3).

**One class per source.** A jointly written or commissioned report takes the class of the
party that publishes it, because that party decides what is published. SRC-005 is
published on SIA's site with BCG authors, so it is `industry_association`. SRC-022 is
published by LBNL "with The Brattle Group" (register), so it is `research_report`. The
co-author is recorded in the source's author text, not as a second class.

**Copies.** A copy of a filing hosted by the filer is classed as the filing. The host is
recorded, and the copy's identity with the regulator's copy is a separate check (§8.3).

**Not yet classed.** A standards body's or association's *announcement* is not a standard.
It is evidence only that the body announced something (an event). No registered source
is one, so no class is created for it (A-1). S06 decides when the first one is retrieved.

## 3. Neighbour tests

Each pair is easily confused. The test is a question, and the registered cases show the
answer.

| Pair | Test | Registered cases |
|---|---|---|
| `company_filing` vs `company_press_release` | Is the document made under a named legal reporting obligation, with the form and statute stated on it? | S05-R1 names the statute on its cover (p.1); SRC-014 names none |
| `company_technical_documentation` vs `company_marketing` | Does the document *specify* the company's own product or service for people who build on, integrate or operate it (structures, quantities, interfaces, steps)? | Channel names are only a hint. SRC-006 (architecture in depth), SRC-008 to SRC-010, SRC-020 specify; SRC-007, SRC-015, SRC-017 present products; SRC-018 explains a field |
| `company_press_release` vs `company_marketing` | Does it announce a dated event, decision or plan of the company? | SRC-014 announces a partnership and a plan; SRC-011 to SRC-013 are explainers in the same newsroom. The channel is the same, so the channel is not the test |
| `research_report` vs `policy_research_brief` | Is it framed as research reporting methods and results, or as analysis to inform policy decisions? | SRC-021 has methods, a data-source appendix (p.33) and a peer-review mark (register); SRC-002 states its aim "To help policymakers understand global semiconductor supply chains" (p.3). Both sit in or near universities, so the host institution is not the test |
| `industry_association` vs `market_research_consultancy` | Is the publisher a membership body that represents an industry, or a firm that sells analysis or advice? | SRC-005 p.2: SIA calls itself "the voice of the semiconductor industry in the US"; BCG calls itself "a leading global management consulting firm". SIA publishes the report (§2, one class per source) |
| `government_publication` vs `research_report` | Does the publisher act as a government authority or programme, or as a research organisation reporting research, even if a government funds it? | SRC-004 is a NIST programme office document; SRC-021 p.2 was "prepared as an account of work sponsored by the United States Government" |
| `standard_specification` vs `government_publication` | Is it issued by a standards body under a standard designation? | SRC-001 is a NIST Special Publication with a definition, not a designated standard (register: "government publication (definitional)"); JEDEC JESD238 would be a standard (blocked, §8.2) |
| `news_media` vs `market_research_consultancy` | Is it journalism published for readers, or analysis sold to clients? | No registered source is either. SRC-021 cites both kinds: news articles (p.31) and market-research datasets it lists as purchased (p.33) |

## 4. Standing: who is speaking about what

The class says what a document is. **Standing** says how its publisher relates to one
claim. It is recorded on the claim (S06), because one source can be first-hand for one
claim and second-hand for the next.

| Standing | Meaning | Example |
|---|---|---|
| `party` | The publisher is a party to the claim: an endpoint company of the edge, the vendor of a product endpoint, the owner or operator of a facility endpoint, or the entity whose attribute it is | NVIDIA on the H100's process (SRC-006): NVIDIA is the product's vendor, so it is a party to "TSMC fabricates H100" |
| `originator` | The publisher created the definition, standard, measurement or estimate | NIST defining cloud computing (SRC-001); LBNL's own energy estimates (SRC-021) |
| `reporter` | The publisher reports what another party said, did or measured | LBNL reporting IDC analysts on die supply (DEP-11); SK hynix describing CoWoS as TSMC's process (SRC-014) |

**Rules:**

- **First-hand means `party` or `originator`.** Each matrix row (§7) says which standing
  first-hand support needs. A `reporter` source supports at most an `ATTRIBUTION` claim.
- **A company speaking about another firm** is first-hand only when it is itself a party
  to the claim. NVIDIA naming TSMC's process for NVIDIA's own product is first-hand
  (though the fabricator is still a `DERIVATION`, ER-1). SK hynix calling CoWoS "A TSMC
  proprietary packaging process" is `reporter` standing: SK hynix is not a party to
  TSMC's ownership of a process.
- **Class-level claims have no party.** Only an originator (a standards body, a research
  organisation, a government definition) is first-hand for "HBM requires TSV" as a
  statement about every HBM stack.
- **Standing needs the publisher as an entity.** To test "party", S06's source record must
  let the publisher be a reference to a company record, where the publisher is a company.
  Non-company publishers stay text: `institution` stays reserved (D-022; entity taxonomy
  §3.7).

**Attribution chains.** When a source reports another's statement, the claim records the
chain: the retrieved source (the reporter), the originator it names, and the locator where
the reporter names it. The claim is an `ATTRIBUTION` to the originator *as reported by* the
retrieved source. The originator is never cited as if it had been retrieved. The chain is
only as strong as its first link: reading a market-research estimate through a national
laboratory does not make it a laboratory finding (ER-6).

**Independence.** Sources count as independent only when their publishers differ and
neither commissioned the other. Several documents from one company are one voice, whatever
their classes. This matters for S01's corroboration rule ("corroborated by two or more
independent sources", domain map "How to read this map"): DEP-02 cites SRC-012 and SRC-013,
and DEP-03 cites SRC-011, SRC-013 and SRC-014: all SK hynix, so each rests on one
publisher (§13, example 3).

## 5. Separate axes

| Axis | What it describes | Where it lives | Owner |
|---|---|---|---|
| Source class | the kind of document and publisher | the source (vocabulary in `sources.schema.json`) | S05 |
| Standing | how the publisher relates to one claim | the claim | S05 rule; S06 field |
| Claim type (`FACT` … `IMPLICATION`) | what kind of proposition the claim makes | the claim | CLAUDE.md §6; S06 |
| Evidence status | how well the evidence supports the claim, after verification | the claim | S06 (MA §10; L-06) |

A preferred class never sets an evidence status, and S05 defines no evidence-status
value. A claim may be recorded as `FACT` only when it cites at least one source of a
preferred or acceptable class for its row, with the standing that row requires, and the
Verifier has found the statement at its locator. Otherwise it is `ATTRIBUTION` or
`DERIVATION` (ER-1 to ER-10).

## 6. Evidence rules

These rules are D-037. Each applies to every source class.

| ID | Rule | Origin |
|---|---|---|
| ER-1 | **A process name is not a fabricator statement.** When a foundry appears only inside the vendor's name for a process, the claim that it fabricates the product is labelled `DERIVATION`, unless another statement names the manufacturer | taxonomy §5 `fabricates`, §12 example 1 |
| ER-2 | **A vendor is not a designer.** The product's `vendor` field and a firm's general designer role establish no `designs` edge. Only a statement of design or development by the named firm does | taxonomy §4.5, §12 example 1 |
| ER-3 | **Silence is `not_researched`.** `not_publicly_determinable` may be claimed for a row only when every **preferred** class for that row (§7) has been searched for that specific question, and none states the answer. The claim records: the question; each class searched and the sources consulted (IDs); the search date; and the result. A preferred class that could not be accessed (§11) was not searched, so the value stays `not_researched`, with the access gap recorded. One page's silence never suffices | taxonomy §9; D-031; HBM-06 |
| ER-4 | **Standing decides first-hand support.** Instance-level rows need a `party`; class-level and definition rows need an `originator` (§4, §7) | §4 |
| ER-5 | **Superlatives, comparisons and exclusivity are `ATTRIBUTION`** in every class: "unique to", "first", "leading", "only". The surrounding factual statements on the same page are judged on their own | D-015; SRC-017 (§13 example 2) |
| ER-6 | **Second-hand is recorded as a chain** and supports at most `ATTRIBUTION`. A reporter never upgrades the originator's class | §4; DEP-11 |
| ER-7 | **One publisher is one voice.** Corroboration needs independent publishers (§4). Several pages of one company are not two sources | §4 |
| ER-8 | **A plan is an event and an intention.** An announced plan, or a forward-looking statement in any class (a filing included: S05-R1 p.3 carries a forward-looking-statements notice), supports an event and an `ATTRIBUTION` of intent. It never supports the state it describes | taxonomy §10; DEP-04 |
| ER-9 | **Company-level is not product-level.** A statement about a firm's suppliers, foundries or technologies in general supports company-level records only (`supplies`, a role). It never supports a product edge or a product's `supplier`, and an `item` is recorded exactly as broad as the source says ("memory" is not "HBM") | S05-R1 (§8.3); taxonomy §5 `incorporates` |
| ER-10 | **Class is not verification.** A preferred-class source that does not state the claim supports nothing. The Verifier reads the statement at its locator and checks the wording does not exceed it, whatever the class | MA §10; D-015 |

## 7. Preference matrix (machine-checked)

**Material claim types are defined by the schemas**, so that a new field or relation type
fails the tests until it has a row:

- every relation type in `relationships.schema.json` (`rel:<type>`);
- every edge qualifier that carries its own claims, i.e. whose shape is an `attr_…`
  definition (`rel:<type>.<qualifier>`);
- the identity of every entity type (`identity:<type>`, the `identity_claim_ids` field);
- every attribute field in `entities.schema.json`, i.e. every field whose shape is an
  `attr_…` definition (`attr:<type>.<field>`). This includes the `definition` field of
  technology and component.
- every event type in `events.schema.json` (`event:<type>`), added in S09 (D-084).

The matrix has 36 rows: 11 relation types, 1 edge qualifier, 6 identity rows, 14
attribute rows and 4 event rows.

**How to read a row.**

- **Preferred:** the classes to search first. A record resting on them, with the standing
  required, can be `FACT` after verification. ER-3's search rule uses this column.
- **Acceptable:** may support the record when no preferred-class source states the claim.
  The claim shows its class, so a reader can see the record rests on an alternative.
- **Never sufficient alone:** a record must not rest *only* on these. Such a source may be
  kept as an `ATTRIBUTION` claim beside stronger support.
- **Every row assigns all 11 classes** to exactly one of the three columns. A class is
  never left to a default.
- **Standing** is what first-hand support needs (§4). **Freshness** is `stable` or
  `time_sensitive` (§12).
- **Expectation** points to the row that says what the evidence must show. It is never
  copied here.

| Row | Preferred | Acceptable | Never sufficient alone | Standing | Freshness | Expectation |
|---|---|---|---|---|---|---|
| `rel:requires` | `standard_specification`, `research_report` | `government_publication` | `company_filing`, `company_technical_documentation`, `company_press_release`, `company_marketing`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | originator | stable | taxonomy §5 `requires`; ER-4, ER-7. A maker's description of its own process is one vendor's view; CSET's statements are reported and dated (§8.1) |
| `rel:has_part` | `standard_specification` | `research_report`, `government_publication` | `company_filing`, `company_technical_documentation`, `company_press_release`, `company_marketing`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | originator | stable | taxonomy §5 `has_part`; ER-4 |
| `rel:owns` | `company_filing`, `government_publication` | `company_press_release` | `company_technical_documentation`, `company_marketing`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | time_sensitive | taxonomy §5 `owns`; ER-8 (an acquisition announcement is an event) |
| `rel:operates` | `company_filing`, `government_publication` | `company_press_release`, `company_marketing`, `company_technical_documentation` | `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | time_sensitive | taxonomy §5 `operates` |
| `rel:designs` | `company_technical_documentation`, `company_filing` | `company_press_release`, `company_marketing` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | taxonomy §5 `designs`; ER-2 |
| `rel:fabricates` | `company_filing`, `company_technical_documentation` | `company_press_release`, `company_marketing` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | time_sensitive | taxonomy §5 `fabricates`; ER-1, ER-9 |
| `rel:packages` | `company_filing`, `company_technical_documentation` | `company_press_release`, `company_marketing` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | time_sensitive | taxonomy §5 `packages`; ER-9; D-032 |
| `rel:incorporates` | `company_technical_documentation` | `company_filing`, `company_marketing`, `company_press_release` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | taxonomy §5 `incorporates` |
| `rel:incorporates.supplier` | `company_technical_documentation`, `company_filing` | `company_press_release` | `company_marketing`, `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | time_sensitive | taxonomy §5 `incorporates` and §9; ER-3, ER-9; D-031 |
| `rel:supplies` | `company_filing` | `company_press_release`, `company_technical_documentation` | `company_marketing`, `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | time_sensitive | taxonomy §5 `supplies`; ER-9 |
| `rel:houses` | `company_press_release`, `company_technical_documentation` | `company_filing`, `government_publication` | `company_marketing`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | time_sensitive | taxonomy §5 `houses`; ER-3 (deployment is usually non-public) |
| `rel:provides_access_to` | `company_technical_documentation` | `company_marketing`, `company_press_release` | `company_filing`, `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | time_sensitive | taxonomy §5 `provides_access_to` |
| `identity:company` | `company_filing`, `government_publication` | `company_technical_documentation`, `company_press_release`, `company_marketing` | `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | stable | taxonomy §5 entity identity; entity taxonomy §7 |
| `identity:facility` | `company_filing`, `government_publication` | `company_press_release`, `company_marketing`, `company_technical_documentation` | `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | stable | entity taxonomy §7; a region or zone is not a facility (D-022) |
| `identity:technology` | `standard_specification`, `government_publication`, `research_report` | `company_technical_documentation`, `policy_research_brief` | `company_filing`, `company_press_release`, `company_marketing`, `industry_association`, `market_research_consultancy`, `news_media` | originator | stable | entity taxonomy §7; a vendor's named offering is not a technology (R-4) |
| `identity:component` | `standard_specification`, `government_publication`, `research_report` | `company_technical_documentation`, `policy_research_brief` | `company_filing`, `company_press_release`, `company_marketing`, `industry_association`, `market_research_consultancy`, `news_media` | originator | stable | entity taxonomy §7 |
| `identity:product` | `company_technical_documentation`, `company_marketing` | `company_filing`, `company_press_release` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | entity taxonomy §7. The one row where marketing is preferred: a product page is how a vendor offers a product |
| `identity:jurisdiction` | `standard_specification` | `government_publication` | `company_filing`, `company_technical_documentation`, `company_press_release`, `company_marketing`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | originator | stable | the ISO 3166-1 code is the identifier (schema); ISO 3166-1 is not yet in the register (gap) |
| `attr:company.legal_name` | `company_filing`, `government_publication` | `company_technical_documentation`, `company_press_release`, `company_marketing` | `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | time_sensitive | `entities.schema.json` `legal_name` |
| `attr:company.incorporated_in` | `company_filing`, `government_publication` | none | `company_technical_documentation`, `company_press_release`, `company_marketing`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | time_sensitive | `entities.schema.json` `incorporated_in` |
| `attr:company.headquartered_in` | `company_filing`, `government_publication` | `company_press_release`, `company_marketing` | `company_technical_documentation`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | time_sensitive | `entities.schema.json` `headquartered_in` |
| `attr:company.roles` | `company_filing` | `company_technical_documentation`, `company_press_release`, `company_marketing` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | time_sensitive | `entities.schema.json` `roles`; D-024 (never derived from edges). A third party's list of firms by business model (SRC-002 p.24) is kept as `ATTRIBUTION` beside the company's own statement |
| `attr:facility.located_in` | `company_filing`, `government_publication` | `company_press_release`, `company_marketing`, `company_technical_documentation` | `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | stable | `entities.schema.json` `located_in`; never the headquarters (S09) |
| `attr:facility.locality` | `company_filing`, `government_publication` | `company_press_release`, `company_marketing`, `company_technical_documentation` | `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | stable | `entities.schema.json` `locality` |
| `attr:facility.nameplate_it_capacity_mw` | `government_publication`, `company_filing` | `company_press_release`, `company_technical_documentation` | `company_marketing`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | time_sensitive | `entities.schema.json` `nameplate_it_capacity_mw`; the source must say the figure is nameplate IT capacity (TQ-10) |
| `attr:technology.definition` | `standard_specification`, `government_publication`, `research_report` | `company_technical_documentation`, `policy_research_brief`, `industry_association` | `company_filing`, `company_press_release`, `company_marketing`, `market_research_consultancy`, `news_media` | originator | stable | `entities.schema.json` `definition`. The working definition is `INTERPRETATION`; its claims preserve each source's own definition (§10) |
| `attr:component.definition` | `standard_specification`, `government_publication`, `research_report` | `company_technical_documentation`, `policy_research_brief`, `industry_association` | `company_filing`, `company_press_release`, `company_marketing`, `market_research_consultancy`, `news_media` | originator | stable | `entities.schema.json` `definition`, as for technology |
| `attr:product.vendor_process_name` | `company_technical_documentation`, `company_marketing` | `company_filing`, `company_press_release` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | `entities.schema.json` `vendor_process_name` ("as the vendor names it"); ER-1 |
| `attr:product.tdp_w` | `company_technical_documentation` | `company_marketing`, `company_filing`, `company_press_release` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | `entities.schema.json` `tdp_w`. A third party's measurement is a different quantity |
| `attr:product.rated_power_w` | `company_technical_documentation` | `company_marketing`, `company_filing`, `company_press_release` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | `entities.schema.json` `rated_power_w` |
| `attr:product.rack_scale` | `company_technical_documentation`, `company_marketing` | `company_press_release`, `company_filing` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | `entities.schema.json` `rack_scale` ("whether the vendor describes") |
| `attr:product.cooling_method` | `company_technical_documentation`, `company_marketing` | `company_press_release`, `company_filing` | `standard_specification`, `government_publication`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | `entities.schema.json` `cooling_method` |
| `event:announced` | `company_press_release`, `company_filing` | `government_publication` | `company_marketing`, `company_technical_documentation`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party | stable | `events.schema.json` `announced`; ER-8: supports only the announcement and an `ATTRIBUTION` of intent, never the state planned |
| `event:opened` | `company_filing`, `government_publication` | `company_press_release` | `company_marketing`, `company_technical_documentation`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | stable | `events.schema.json` `opened`; ER-8: a statement that a site will open is `announced` |
| `event:expanded` | `company_filing`, `government_publication` | `company_press_release` | `company_marketing`, `company_technical_documentation`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | stable | `events.schema.json` `expanded`; a planned expansion is `announced` |
| `event:closed` | `company_filing`, `government_publication` | `company_press_release` | `company_marketing`, `company_technical_documentation`, `standard_specification`, `research_report`, `policy_research_brief`, `industry_association`, `market_research_consultancy`, `news_media` | party or originator | stable | `events.schema.json` `closed` |

**What the matrix does not cover.**

- **Events** had no rows until S09, which added one per event type (D-084, approved by
  the human at the start of S09: "Add the rows (Recommended)"). An event's claims are
  judged against its type's row. ER-8 still governs every plan.
- **Quantities outside the schema** (volumes, market shares, deployment counts) have no
  rows, because no field holds them (NG-11). They are mostly `not_publicly_determinable`
  (domain map §8).

## 8. The registered sources and their classes (machine-checked)

### 8.1 SRC-001 to SRC-023

> **Status note (S06, 2026-09-30; D-050, accepted).** Migrated. Each source's class now
> lives in its record in `data/sources.json` (`src-NNN`, with the old label in
> `migrated_from`; S05-R1 in §8.3 is `src-024`). This table and §8.3 are history. VD-9
> (`claim-model.md` §11) checks that the migration matches them.

This table is the one home of each registered source's class until S06 migrates the
register into source records. After that, the source record's class field is the home,
and this table is history. `source-register.md` is not edited: its `source_tier` column
stays as S01's provisional record (D-041). All 23 registered sources have one class each.

| Source | Class | S01 tier | Change | Basis |
|---|---|---|---|---|
| SRC-001 | `government_publication` | T3 | none | NIST Special Publication; a definition, not a designated standard (§3) |
| SRC-002 | `policy_research_brief` | T4 | from research (T4) to policy analysis: in S01 terms, T5 (register note 1) | "To help policymakers" (p.3); not peer-reviewed (register); data "current as of 2019" (p.5) |
| SRC-003 | `policy_research_brief` | T4 | as SRC-002 | CSET issue brief, same series (register) |
| SRC-004 | `government_publication` | T3 | none | NIST CHIPS R&D Office programme document |
| SRC-005 | `industry_association` | T5 | named as an association report; BCG co-authorship recorded as authors | SIA's self-description (p.2); published on SIA's site |
| SRC-006 | `company_technical_documentation` | T1 | T1 split by document kind | architecture specified in depth, developer channel |
| SRC-007 | `company_marketing` | T1 | T1 split: product technology page | a product-technology page on the vendor's main site, not its developer documentation |
| SRC-008 | `company_technical_documentation` | T1 | T1 split | service documentation |
| SRC-009 | `company_technical_documentation` | T1 | T1 split | service documentation |
| SRC-010 | `company_technical_documentation` | T1 | T1 split | developer documentation |
| SRC-011 | `company_marketing` | T1 | T1 split: newsroom explainer | explains HBM to a general reader; branded series |
| SRC-012 | `company_marketing` | T1 | T1 split: newsroom explainer | explains TSV; announces nothing, specifies no product |
| SRC-013 | `company_marketing` | T1 | T1 split: newsroom explainer | explainer series on back-end processes |
| SRC-014 | `company_press_release` | T1 | T1 split | announces a partnership and a plan, dated 2024-04-19 |
| SRC-015 | `company_marketing` | T1 | T1 split: product page | presents the product line |
| SRC-016 | `company_marketing` | T1 | T1 split: capability page | presents an OSAT's services |
| SRC-017 | `company_marketing` | T1 | T1 split: product page | presents the product; contains an exclusivity claim (§13) |
| SRC-018 | `company_marketing` | T1 | T1 split: glossary | a glossary entry (register: explanatory documentation) |
| SRC-019 | `company_marketing` | T1 | T1 split: process overview page | an overview of process areas (register: product documentation) |
| SRC-020 | `company_technical_documentation` | T1 | T1 split | user guide |
| SRC-021 | `research_report` | T3 | from government (T3) to research | national-laboratory report "sponsored by" a government (p.2); methods and data-source appendix (p.33) |
| SRC-022 | `research_report` | T3 | from government (T3) to research | national-laboratory technical brief (register) |
| SRC-023 | `research_report` | T4 | none | register: "independent non-profit research institute report". Not re-read in S05 (§12), so this rests on the S01 description (`INTERPRETATION`) |

**The CSET decision** (register note 1). CSET's briefs are `policy_research_brief`, which
in S01's terms is a move from T4 to T5. They remain an acceptable alternative for
technology and component identity and definitions, as `ATTRIBUTION`. They are never enough
alone for a company fact, market data or a `requires` edge (§7).

### 8.2 Hosts that were not retrievable in S01

Each row of the register's "Not retrievable" table, by its leading name. The classes are
what the host would provide. They are `INTERPRETATION`, because the hosts were not read.

| Host row | Classes |
|---|---|
| JEDEC | `standard_specification`. Its press release is an announcement, not a standard (§2, "Not yet classed") |
| TSMC | `company_filing` (investor pages), `company_marketing` (technology pages), `company_press_release` (press pages) |
| Samsung | `company_technical_documentation`, `company_marketing` |
| LBNL 2024 | `research_report` |
| IEA | `government_publication` (intergovernmental) |
| SEC EDGAR | `company_filing` (the regulator hosts the companies' filings) |
| Intel | `company_technical_documentation`, `company_marketing` (Intel, Applied Materials, KLA, Cadence), `industry_association` (SEMI), `standard_specification` (ISO), `government_publication` (OECD), `market_research_consultancy` (Uptime Institute) |
| AMD | `company_technical_documentation` |
| The Green Grid | `standard_specification` (member-only; §11) |

### 8.3 Sources retrieved in S05

These live here until S06 migrates them with the register. They are not register rows,
because the register is an S01 artifact that S05 does not edit (§06 q11; D-041).

| ID | What | Retrieval | Class |
|---|---|---|---|
| S05-R1 | NVIDIA Corporation, Annual Report on Form 10-K for the fiscal year ended January 25, 2026 (company-hosted copy), `https://investor.nvidia.com/files/doc_financials/2026/q4/10K-NVDA.pdf` | `curl` over HTTPS, 2026-09-30T16:57Z; SHA-256 prefix `a056b59e4170`; 93 pages; text extracted locally; signed 2026-02-25 (p.84) | `company_filing` |
| S05-A1 | Access record, not a source: the response of `www.sec.gov` to plain requests for its EDGAR access page, `/developer` and `/privacy` | `curl`, 2026-09-30T16:56Z; HTTP 403 for all three; SHA-256 prefix `14f247606881` (first response) | none |

**Why S05-R1 was retrieved.** No registered source is a filing, and the policy prefers
filings for many rows. So Part B §05 allowed one retrieval to settle what the class
contains. SEC EDGAR refused (§11), so the filer's own copy was used. Its identity with the
copy filed at the SEC is **not verified**, because EDGAR could not be read.

**What S05-R1 shows** (read by the S05 Verifier at the locators given; verbatim anchors
from the locally extracted text; the full text is not in the repository):

| Locator | Anchor | What it supports | What it does not |
|---|---|---|---|
| p.1 | "(Exact name of registrant as specified in its charter)"; "(State or other jurisdiction of incorporation or organization)" | the filing class carries the legal name and incorporation, first-hand (`identity:company`, `attr:company.legal_name`, `attr:company.incorporated_in`) | — |
| p.3 | "This Annual Report on Form 10-K contains forward-looking statements" | ER-8 applies inside filings too | — |
| p.8 | "We utilize a fabless and contracting manufacturing strategy" | `attr:company.roles` (`fabless_designer`), `party` standing | — |
| p.8 | "We purchase memory from SK Hynix Inc., Micron Technology, Inc., and Samsung." | company-level `supplies` candidates, one per named firm, with item "memory" | any product's `supplier`; an item narrower than "memory", such as HBM (ER-9) |
| p.8 | the same paragraph names TSMC and Samsung as foundries that "produce our semiconductor wafers", and says NVIDIA uses "CoWoS technology" for packaging | company-level `supplies` candidates | `fabricates` or `packages` for any named product; CoWoS as a technology record (D-032, R-4) |
| p.17 | "We do not assemble, test, or package our products" | the fabless role; no NVIDIA `packages` edge is expected | — |
| p.88 | "SUBSIDIARIES OF REGISTRANT" (Exhibit 21.1), with each subsidiary's jurisdiction | `owns` candidates, first-hand | — |

This is the lesson the filing adds: it is the strongest source for who NVIDIA is and whom it
buys from, and it cannot say which memory maker supplies the H100. HBM-06's gap is not
closed by the filing. Under ER-3, it is now one preferred class searched for that
question, not the whole search.

## 9. Reconciling MA §10 and D-015's provisional tiers

Two orders existed:

| Source | Order |
|---|---|
| MA §10 | 1 primary legal and institutional · 2 official government and company filings and documentation · 3 intergovernmental and standards bodies · 4 peer-reviewed research · 5 secondary analysis · 6 news and media · 7 tertiary summaries |
| D-015 (S01) | T1 company documentation and filings · T2 standards bodies · T3 government and intergovernmental · T4 academic and technical research · T5 secondary analysis · T6 news |

**Ruling (D-036).** The Atlas keeps no global ranking. The matrix (§7) is the
"project-specific source policy" that MA §10 asks for ("Use a project-specific source
policy, but generally prefer: …"). MA's order is its general guidance, and MA is not
edited.

- **Why no global ranking survives.** No single order fits the rows. Company marketing is
  preferred for product identity and never enough for a technology definition. Standards
  are preferred for definitions and never enough for who supplies whom.
- **Where the orders differ, and what the matrix does:**
  - both orders put company documents in one level. The matrix splits them by document
    kind, because a filing, a datasheet, a press release and a product page answer for
    different things (§2);
  - MA ranks government above standards, and D-015 ranks standards above government. The
    matrix prefers standards for class definitions and jurisdiction codes, and government
    for official-register facts. Neither is above the other in general;
  - D-015 put company documentation first because every S01 use was a company describing
    its own products. That is the `party` standing rule (§4), not a rank;
  - MA's level 1 (primary legal sources) has no v1 row: the policy layer starts at S17;
  - MA's level 7 (tertiary summaries) is not a class. It is not a source (§2).
- **Where they agree.** Secondary analysis and news are never enough alone for any record
  in the matrix. Their rows all place `market_research_consultancy` and `news_media` in
  "never sufficient alone".

**D-015's parts.** Its tier order is superseded by D-036 when accepted. Its meaning of
`verified` in research artifacts is kept until S06's claim model confirms or replaces it
(D-036).

## 10. Conflicts

This policy is D-038. A conflict is two or more claims that cannot all be read as one value.

### 10.1 Kinds of conflict

| Kind | Recognised by | Recorded as | Closed when |
|---|---|---|---|
| `definitional` | sources define or bound a term differently | one `ATTRIBUTION` claim per source definition. The Atlas working definition is an `INTERPRETATION` assertion that cites them all | never: the working definition is a choice, not a resolution. The human approves it (class C) |
| `wording` | one source uses a term loosely against more specific sources | the loose statement is kept as an `ATTRIBUTION` claim; the Atlas's reading of it is an `INTERPRETATION` claim | never: the source still says what it says |
| `factual_contradiction` | incompatible values for the same thing, scope and time | several assertions, each citing its own claims (D-025), and the evidence status for disputed claims that S06 defines | only by new evidence that explains it (a correction by the publisher, a demonstrated error), recorded as a claim; a material one also needs the human (class C) |
| `temporal` | different values for different dates | several assertions with `valid_from`/`valid_to`; a newer edition of the same publisher's series marks the older as superseded for what it covers (§12) | it is history, not a dispute. Nothing is deleted |
| `scope` | the sources measure or define different populations | each claim records its scope; the claims are not compared as if they were about one thing | when the scopes are recorded, it is not a conflict |

**Rules for every kind:**

- **No conflict is settled by class or rank.** A preferred class is not a tie-break.
  CON-02 shows why: the rank orders would have favoured Google's technical documentation,
  but the Atlas reading follows SK hynix's more specific description.
- **Evidence is never deleted.** Both sides' claims stay in the record. Removing canonical
  evidence is human-only (CLAUDE.md §9, class D).
- **Self-interest is recorded, not a kind.** An advocacy association (SRC-005 p.2) or a
  vendor claiming exclusivity (SRC-017) has an interest. The class and standing record it.
  It never decides a conflict, because an interested source can be right.
- **Publishing an unresolved material dispute is human-only** (CLAUDE.md §9, class D). A
  consumer shows both positions, and any client output that presents one needs the human's
  sign-off.
- **Who may flag.** The Verifier and Data Auditor may flag a conflict and propose its kind.
  Only the human closes a material one.

**Cases seen outside §10.2** (illustrations from registered sources):

- **`temporal`:** SK hynix's base dies use its own technology up to HBM3E, and it plans
  TSMC's logic process for HBM4 (HBM-03, SRC-014). Two periods, and the second is a plan
  (ER-8). LBNL's 2024 report is partly superseded by its 2025 update (SRC-021; register
  "Not retrievable").
- **`scope`:** CSET's market shares are by firm headquarters, "rather than locations of
  operations" (SRC-002 p.5; domain map §6). SRC-021 reports that IDC uses its global ASIC totals as its
  U.S. forecast, and that its own Reference Case keeps that assumption (p.17–18).
- **`factual_contradiction`:** none among the 23 registered sources, as S01 recorded them.
  The kind is defined so that S07–S10 do not improvise when the first one appears.

### 10.2 CON-01 to CON-05 (machine-checked)

Illustrations only. `domain-map.md` is not edited, and its "Handling" column stays S01's.

| Conflict | Kind | Sides (source · class) | Recorded as | Status | Who may change it |
|---|---|---|---|---|---|
| CON-01 | `definitional` | SRC-003 p.4 · `policy_research_brief`; SRC-021 p.16 · `research_report` | two `ATTRIBUTION` claims; the working definition (TQ-01) in `component.definition`. LBNL's side is also an accounting scope (`scope`), recorded on its claim | preserved | the human (TQ-01, D-016) |
| CON-02 | `wording` | SRC-008 · `company_technical_documentation`; SRC-012 · `company_marketing` | Google's "on-chip" kept as an `ATTRIBUTION` claim; "loose wording" is an `INTERPRETATION` claim (TQ-02) | preserved | the human (TQ-02) |
| CON-03 | `definitional` | SRC-004 p.7 · `government_publication`; SRC-013 · `company_marketing`; SRC-005 p.21 · `industry_association` | three `ATTRIBUTION` claims; the neutral term "multi-die" (TQ-09) | preserved | the human (TQ-09) |
| CON-04 | `definitional` | SRC-004 p.4 · `government_publication`; SRC-005 p.21 · `industry_association` | two `ATTRIBUTION` claims; the narrow working definition (TQ-03) | preserved | the human (TQ-03) |
| CON-05 | `definitional` | SRC-002 p.66, p.19 · `policy_research_brief`; SRC-005 p.6 · `industry_association` | `ATTRIBUTION` claims, including CSET's inconsistency with itself; the term is split (TQ-04, D-024) | preserved | the human (TQ-04, D-024) |

In every case, the human's terminology answers (D-016) chose the Atlas's working terms.
None of them removed a source's position, and none used a rank.

## 11. Retrieval and access

| ID | Rule |
|---|---|
| RA-1 | **Raw retrieval.** Sources are retrieved with an ordinary HTTPS request and read from locally extracted text. Web search only discovers URLs. |
| RA-2 | **No circumvention.** A refusal (403, a challenge page, a login wall) is recorded as an access gap. It is never replaced by a snippet or a secondary summary, and never bypassed with a headless browser, a changed client identity, a mirror of unknown provenance or a proxy. |
| RA-3 | **A published access policy may be followed, once it has been read.** Following a site's written rules for automated clients is not circumvention. But the rules must be read first, and model memory of them is not evidence. |
| RA-4 | **Manual retrieval by the human** (H-1, D-039), with all of these conditions: (1) only sources the human can access legitimately: public pages, filings, and standards free with registration; nothing paywalled or members-only unless the human already has legitimate access; (2) targeted: only sources this policy prefers for a claim that matters, listed by the session that needs them; (3) each download records the URL, the method "manual, by the human", the human's download date and the file's content hash, and is marked as not reproducible by automated retrieval; (4) full texts stay out of the repository: the repository keeps the record, the locators and short quoted anchors, and the file lives in a local folder that is not committed; (5) verification is unchanged: Claude reads the text the human supplies and checks each anchor at its locator. |
| RA-5 | **Paywalled and member-only standards** (ISO/IEC 30134-2, The Green Grid PUE) are gaps unless the human already has legitimate access (RA-4). A secondary summary of a standard is an `ATTRIBUTION` by its own publisher, never the standard. |
| RA-6 | **Company-hosted copies of filings** may be used, classed as the filing (§2). Whether the copy is the one filed with the regulator is recorded as checked or not checked. |
| RA-7 | **Declaring an identity to a site is a human decision.** A declared client identity names a contact. Choosing one is an external commitment, so Claude does not choose it (CLAUDE.md §9, class D). |

**SEC EDGAR, checked rather than assumed.** On 2026-09-30, plain requests for EDGAR's
access page, `www.sec.gov/developer` and `www.sec.gov/privacy` all returned HTTP 403
(S05-A1). The refusal page is titled "Request Rate Threshold Exceeded", although these were
S05's first requests to the host. Its text says "Automated access to our sites must comply
with SEC.gov's Privacy and Security Policy" and points to `www.sec.gov/developer` for
"Fair Access guidelines". Those guidelines are behind the same refusal. So:

- **What is established:** EDGAR's refusal cites a published policy for automated access.
- **What is not established:** what the policy requires, or whether a declared client
  identity would satisfy it. S05 sent no custom client identity (RA-3, RA-7).
- **The path chosen** (D-042): filings are taken from copies the filer publishes itself
  (RA-6), and no identity is declared to EDGAR. Filings available only from the SEC stay an
  access gap.

**External API dependency is a non-goal** (NG-14, D-043). Retrieving filings through a
regulator's programmatic interface would make the Atlas depend on an external API, so v1.0
does not.

## 12. Freshness and dated evidence

**The dates, kept apart:**

| Date | What it is | Where it lives |
|---|---|---|
| as-of date | the date the content describes, when the source says it (CSET: "current as of 2019", SRC-002 p.5) | the claim (S06), because one source can hold data of several dates |
| publication date | the date the source states for itself; "undated (live page)" is recorded as such, never guessed | the source |
| access date and content hash | when the Atlas retrieved it, and a hash of the bytes retrieved | the source (manual retrievals: RA-4) |
| verification date | when the Verifier found the anchor at its locator | the claim (L-06: per record, never a batch stamp) |

**A byte change is a signal, not staleness.** S05 re-retrieved all 23 registered sources on
2026-09-30 (as measured at base `092c607`, not a tested count). 14 returned the same bytes
as in S01, and 9 returned different bytes. Every domain-map anchor was found again in the
22 sources whose text was re-read, including all 8 changed web pages. (SRC-017 needed a
second request after a connection error; its bytes were unchanged.) SRC-023's PDF changed
and could not be re-read (it is encrypted, and the extraction library would have needed an
extra package). So:

- a changed hash triggers an anchor re-check at each locator the Atlas relies on;
- a claim becomes stale when its anchor is no longer at its locator, not when the bytes
  change;
- an undated live page is dated only by its access date. A claim resting on one says
  "as retrieved on" that date.

**When evidence is stale:**

- **Supersession.** A newer edition in the same publisher's series supersedes the older
  one for what it covers: LBNL's 2025 update and its 2024 report. SRC-021 cites a 2026 EPRI
  update of the SRC-023 series (p.31), so SRC-023 is a supersession candidate. It must be
  checked before any record relies on it.
- **Plans** are stale once the date they refer to has passed, or a later statement
  confirms or contradicts them. They never become states (ER-8). SK hynix's 2024 HBM4
  base-die plan (SRC-014) needs re-checking before any record relies on it (domain map §8).
- **`time_sensitive` rows** (§7): evidence whose as-of date (or publication date, when no
  as-of date is given) is more than 12 months before its use in a canonical record must be
  re-checked first. The 12 months is a design choice (`INTERPRETATION`), approved by the
  human at the S05 review (D-040). CSET's 2019 market data are stale by this rule, and the
  domain map already does not use them.
- **`stable` rows** have no age limit. Only supersession and anchor drift make them stale.

The rule is written here. `validate-freshness` implements it later (S06+), and S05 writes
no freshness code (L-01, L-09).

## 13. Worked examples (illustrations, not records)

Each example takes registered sources the domain map already quotes. The quoted anchors are
checked against the domain map by the tests.

### Example 1 — SRC-006: NVIDIA on its own chip, and what that says about TSMC

FAB-05 quotes SRC-006 (`company_technical_documentation`): the H100 is "fabricated using
the TSMC 4N process customized for NVIDIA".

| Candidate claim | Standing | Supported? | Label |
|---|---|---|---|
| H100's process, as the vendor names it | `party` (vendor) | yes: a preferred class for `attr:product.vendor_process_name` | `FACT` after verification |
| TSMC `fabricates` H100 | `party` (NVIDIA is the vendor of the product endpoint) | only by reading a fabricator out of a process name | `DERIVATION` (ER-1) |
| NVIDIA `designs` H100 | — | no: the anchor names no designer (ER-2) | none |
| NVIDIA's introduction calling the H100 the world's first GPU with HBM3 (register locator for SRC-006) | `party` | only as what NVIDIA claims | `ATTRIBUTION` (ER-5) |

The class is preferred for this edge. The wording still limits the claim to a
`DERIVATION`: class does not replace reading (ER-10).

### Example 2 — SRC-017: an exclusivity claim on a product page

SME-03 quotes ASML's product page (`company_marketing`): "The technology, which is unique to
ASML, prints microchips using light with a wavelength of just 13.5 nm". The same page says
"EUV systems are used to print the most intricate layers on a chip, with the rest of the
layers printed using various DUV systems".

| Candidate claim | Supported? | Label |
|---|---|---|
| EUV is unique to ASML | as ASML's claim only | `ATTRIBUTION` (ER-5). An interested source (§10.1), and not refuted by that |
| EUV uses 13.5 nm light | a technical statement on a marketing page | kept as ASML's description (`ATTRIBUTION`). Marketing is never sufficient alone for `identity:technology` or `attr:technology.definition`, which prefer standards, government or research |
| advanced-node fabrication `requires` EUV (DEP-08) | no: marketing is never enough alone for `rel:requires` | CSET says advanced lithography is "necessary for mass-production of advanced chips" (SRC-002 p.30), a `policy_research_brief` with 2019 data. That class is also never sufficient alone for `rel:requires`, so the statement is kept as `ATTRIBUTION`. DEP-08 needs research or a standard, and its alternatives are `not_researched` (domain map §8) |

### Example 3 — SRC-014: a press release with a plan, and a statement about another firm

HBM-03 quotes SK hynix's press release (`company_press_release`, 2024-04-19): SK hynix
"plans to adopt TSMC’s advanced logic process for HBM4’s base die". It also says "HBM is
made by stacking a core DRAM die on top of a base die that features TSV", and describes
CoWoS as "A TSMC proprietary packaging process that connects GPU/xPU, a logic chip, and
HBM, on a special substrate called an interposer".

| Candidate claim | Standing | Supported? | Label |
|---|---|---|---|
| SK hynix announced the plan on 2024-04-19 | `party` | yes | an event (S09) |
| SK hynix intends to use TSMC's process for HBM4 base dies | `party` | as SK hynix's intention only | `ATTRIBUTION` (ER-8) |
| TSMC fabricates an HBM4 base die | — | no: a plan is not a state; and D-032 applies | none |
| CoWoS is TSMC's proprietary process | `reporter` | as SK hynix's description of another firm | `ATTRIBUTION` (§4) |
| HBM `has_part` base die; HBM `requires` TSV | none (class level) | a press release is never enough alone for either row | acceptable only with a standard or research source. DEP-03's three sources are all SK hynix, so they are one voice (ER-7) |

### Example 4 — SRC-021: a second-hand chain (DEP-11)

DEP-11 quotes SRC-021 (`research_report`): "the market is currently constrained by die
supply". The domain map records it as second-hand: LBNL reporting IDC analysts. SRC-021
cites that sentence to an IDC analyst's personal communication (p.31) and lists IDC as
purchased market research (p.33).

| Link | Class | Standing | What it supports |
|---|---|---|---|
| LBNL (retrieved) | `research_report` | `reporter` for this sentence | that LBNL reports IDC's view |
| IDC analyst (named, not retrievable) | `market_research_consultancy` | `originator` | nothing directly: the Atlas cannot read it |

The claim is an `ATTRIBUTION` to IDC as reported by LBNL (ER-6). No die-supply record can
rest on it. The same report says ASIC deployers "rarely disclose detailed shipment or
deployment figures" (p.17). That is LBNL's own statement (`originator`), and it is
evidence toward, not proof of, `not_publicly_determinable` for a named site (ER-3).

### Example 5 — SRC-005: an association report written by a consultancy

SRC-005 (`industry_association`, §2) says "The term “advanced packaging” covers a wide range
of materials and manufacturing technologies" (CON-04), and refers to "Taiwan in the
pure-play foundry business" (FAB-03).

| Candidate claim | Supported? | Label |
|---|---|---|
| SIA/BCG's definition of advanced packaging | as their definition | `ATTRIBUTION`; one side of CON-04 |
| a working definition of advanced packaging | no: an association is acceptable for definitions only beside a standard, government or research source | the Atlas's narrow definition is `INTERPRETATION` (TQ-03) |
| any company's role or location | no: never enough alone for company facts | none |

## 14. How the Atlas decides what to believe

*Written for the week-2 gate (operational roadmap, week 2): the ontology and evidence policy
are understandable before large-scale data collection begins. It walks one S01 sentence through all three models.
The human judged the gate on this section and declared it passed (2026-09-30).*

**The sentence.** NVIDIA's technical page says the H100 is "fabricated using the TSMC 4N
process customized for NVIDIA" (SRC-006, quoted in FAB-05).

1. **The source (S05).** Who published it, and what kind of document is it? NVIDIA
   published it, and it specifies NVIDIA's own chip in depth, so it is
   `company_technical_documentation` (§3). It is not a filing (no legal obligation), not a
   press release (no dated announcement) and not a product page (it specifies).
2. **Standing (S05).** How does NVIDIA relate to what the sentence says? It sells the H100,
   so it is a `party` to anything about the H100 (§4).
3. **The statements (S05 rules).** The sentence says two things. The process name is
   NVIDIA's own wording, so it is first-hand. That TSMC does the fabrication is read out of
   the process name, so it is a `DERIVATION` (ER-1).
4. **The entities (S03).** The H100 is a product record. Its `vendor` is NVIDIA, which does
   not make NVIDIA its designer (ER-2). The process name goes in the product's
   `vendor_process_name` field, which is the one home for it.
5. **The relationship (S04).** *TSMC `fabricates` H100* is a candidate edge. It needs a
   claim. The claim here is a `DERIVATION`, so the edge would show as inferred.
6. **The preference (S05).** For `fabricates`, the matrix prefers a filing or technical
   documentation from a party (§7). This source is one, so the search can stop only if a
   direct statement is wanted. NVIDIA's 10-K (S05-R1) names TSMC among its foundries, but
   not for the H100 (ER-9), so it does not turn the derivation into a fact.
7. **Checking (S05, then S06).** The Verifier must find the words at the locator. The class
   never does this for it (ER-10). S06 then gives the claim an evidence status.
8. **Display.** A reader should see that NVIDIA states the H100 is made on a TSMC process,
   and that TSMC fabricating it is inferred, with the source, its class, the date retrieved
   and the reason it is an inference. A reader should never see a bare *TSMC makes the
   H100*.

**Three things the policy makes impossible:**

- **Marketing as fact about the world.** A product page is never enough alone for a
  definition or a `requires` edge (§7), and its superlatives are `ATTRIBUTION` (ER-5).
- **A report standing in for its source.** A report of someone else's statement is a chain,
  and supports only an `ATTRIBUTION` to the originator (ER-6).
- **A conflict settled by rank.** No class breaks a tie; both sides stay, and a material
  dispute needs the human (§10).

## 15. Candidates considered and rejected

| Candidate | Why not |
|---|---|
| A global ranking (MA §10's order, or D-015's T1–T6) | It cannot express that one class is preferred for one claim type and insufficient for another (§9; D-036) |
| Numeric credibility, reliability or confidence scores per source | Invented precision; D-028 rejects confidence scores; NG-11. Class, standing, claim type and evidence status carry it |
| "Primary" and "secondary" as classes | One source is first-hand for one claim and second-hand for the next (§4). Standing is per claim |
| One `company` class (D-015's T1) | A filing, a datasheet, a press release and a product page answer for different things (§2) |
| Marketing as a statement label only, with no page class | The page's purpose matters for what it is never enough for (definitions, necessity). Statement-level attribution (ER-5) is kept as well |
| A two-class value for joint reports (SIA/BCG) | Breaks one class per source; the publishing party decides what is published (§2) |
| A `tertiary_summary` class | Tertiary summaries, snippets and aggregators are not sources at all (§2) |
| A class for standards bodies' or associations' announcements | No registered source is one (A-1). S06 decides with the first case (§2) |
| Self-interest as a kind of conflict | Interest is a property of a source, recorded by class and standing. As a kind it would invite deciding against the interested side (§10.1) |
| Standing values in the source schema | Standing is a relation between a source and a claim, so it is a claim field (S06) |
| Event rows now | Event types are S09's; ER-8 covers plans until then (§7) |
| Annotating `source-register.md` with the new classes | The register is S01's record, frozen after S06; editing it would need a human-approved decision (Part B §08). §8 is the home instead |
| The full source-record schema now (H-2 option (c)) | S06's, with the claim model and the migration (H-2) |
| Retrieving EDGAR with a declared client identity | The access policy could not be read, and choosing an identity is the human's (RA-3, RA-7) |

## 16. What S05 leaves to other sessions

> **Status note (S06, 2026-09-30; D-044 to D-051, accepted).** S06 took the source record,
> the claim fields, the meaning of `verified` and the migration (`claim-model.md`).
> `validate-freshness` is left to S07 (D-051). The announcement class is still open.

| Item | Owner | Note |
|---|---|---|
| Source record: class (this vocabulary); publisher as text, and as a company reference where the publisher is a company (§4); authors; retrieval method (automated or "manual, by the human"); access date; content hash; publication date as stated; host of a copy (RA-6) | S06 | extends `sources.schema.json` (H-2) |
| Claim fields: standing (§4); the attribution chain (reporter, originator, locator); the as-of date (§12); the search scope of a `not_publicly_determinable` claim (ER-3); the evidence status for disputed claims (§10) | S06 | S05 defines the rules, not the fields |
| The meaning of `verified` (D-015's second part) | S06 | confirm or supersede in the claim model |
| Migrating the register: each row's class from §8.1; S05-R1 from §8.3 | S06 | the register is then frozen |
| A class for announcements by standards bodies or associations, if one is retrieved | S06 | §2 |
| `validate-freshness`: hash-change re-checks, supersession, the 12-month horizon | S06+ | §12; L-01 |
| Event rows in the matrix | S09 | §7. Done in S09 (D-084) |
| Filings only available from the SEC | the session that needs them; a new decision if EDGAR's policy is to be read (D-042) | §11 |
| ISO 3166-1 as a registered source for jurisdiction identity | S07 or the first session that creates a jurisdiction record | §7 |
