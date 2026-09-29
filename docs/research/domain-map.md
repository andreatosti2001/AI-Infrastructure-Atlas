# Domain map — the physical AI compute stack

**Status:** DRAFT research artifact, awaiting human terminology review (S01 Part A "Human task").
**Session:** S01 · **Date:** 2026-09-29 · **Sources:** [`source-register.md`](./source-register.md)
**Governing question (D-008):** *Where are the critical dependencies behind AI compute, and
what evidence supports that assessment?*

This is a **concept-level** map. It names kinds of things (technologies, components,
processes, facilities, actor types) and how they depend on each other. It is not a
dataset. Named companies and products appear only as **attributed examples** that
support a concept. They are not entity records, and nothing here is an entity-to-entity
supply edge (that is S10's job). There are no market shares, rankings or metrics.

---

## How to read this map

**Entry fields.** Every concept entry has: an ID, its **kind**, a **definition** with a
**claim class**, **evidence** (source ID + locator + a short verbatim anchor), a
**status**, concept-level **upstream / downstream** links, and a **scope** call with a
one-line justification.

**Claim classes** (CLAUDE.md §6):
`FACT` directly supported by a primary/authoritative source, or corroborated by
two or more independent sources · `ATTRIBUTION` "source X says/defines …", used for
single-source definitions, company self-descriptions of comparative standing, and
secondary analysis · `DERIVATION` follows from combining cited statements ·
`INTERPRETATION` this map's own judgement (e.g. a chosen working definition) ·
`IMPLICATION` consequence for the project.

**Status markers** (MA §5.7):
`verified` means the S01 Verifier role re-read the retrieved source and the anchor
quote is present at the locator, with wording judged not to exceed the evidence. It
does **not** mean human-reviewed or canonical. ·
`disputed` means retrieved sources define or bound the concept differently (see §5) ·
`not_researched` means no retrieved source covers it yet ·
`not_publicly_determinable` means the information is, on current evidence, not
disclosed publicly · `not_applicable`.

**Locators.** `p.N` is the PDF page index (see register). HTML sources are located by
the quoted sentence.

**Scope.** `v1` means needed to answer the governing question for the first vertical
(CLAUDE.md §10, MA §25). `future` means real and relevant, but not needed for the first
answer. The v1/future calls are **proposals** for S02 to freeze.

**Layers.** Part A's seven layers, with "EDA/equipment" mapped as two sub-layers,
`5a EDA` and `5b SME` (see TQ-05 and decision D-013).

---

## 1. Plain-language overview of the chain

*Written for the Part A weekly gate. Each sentence cites the entries it relies on.*

1. **What is being made.** "AI compute" here means the large-scale computation used to
   train and run AI models. It is delivered mainly by specialised "AI chips" rather than
   general-purpose processors [X-01, ACC-01].
2. **The chip.** The workhorse is an **AI accelerator**: a data-centre GPU or an AI-specific
   ASIC such as Google's TPU or AWS's Trainium [ACC-01, ACC-02, ACC-03]. Companies
   design accelerators with **EDA** software [EDA-01]. Many designers are **fabless**:
   they do not own factories [ACC-04].
3. **Making the logic die.** A fabless designer's chip is manufactured by a **foundry**.
   A foundry runs **fabs** that build transistors and wiring on silicon wafers,
   layer by layer [FAB-01, FAB-02, FAB-03]. The most advanced layers are patterned with
   **EUV lithography** (the most intricate layers), the rest with DUV [SME-02, SME-03]. Deposition, etch and other
   tools build and shape each layer [SME-04]. Example (company-reported): NVIDIA
   states its H100 and Blackwell GPUs are made on TSMC process variants [FAB-05].
4. **The memory.** According to SK hynix, AI training needs far more memory bandwidth
   than ordinary server memory provides [DEP-01]. The current answer is **High Bandwidth Memory (HBM)**: a stack of
   DRAM dies joined vertically by **through-silicon vias (TSVs)** and sitting on a base
   die [HBM-01, HBM-02, HBM-03, HBM-04]. HBM is made by memory manufacturers, not by
   the accelerator designer [HBM-06].
5. **Putting them together.** HBM ships as a "semi-packaged" product. It is placed
   side-by-side with the accelerator's logic die on a silicon **interposer**. This is
   **2.5D packaging**, a form of **advanced packaging** [PKG-03, PKG-04, DEP-02]. Some
   accelerators also join more than one logic die in one package; NVIDIA's Blackwell
   uses two [ACC-05, PKG-06].
   Advanced packaging reuses wafer-fab processes and equipment, so it straddles "front
   end" and "back end" [DEP-06, TQ-06].
6. **Into the building.** Packaged accelerators go into **accelerated servers**,
   including rack-scale, liquid-cooled systems [DC-05, DC-06]. Those servers sit
   in **data centres**, facilities that house computing equipment [DC-01]. Many users
   reach them as a **cloud** service (for example rented compute, IaaS), not by
   owning the hardware [DC-02, DC-03, DC-04].
7. **The energy interface.** Every layer above ends up as electrical load. Chips and
   servers have rated power. The facility adds overhead, mostly cooling, measured by
   **PUE**. The site draws power through a **grid interconnection** or builds its own
   generation [EN-01 … EN-05].
8. **Where the critical dependencies are likely to sit.** On current evidence, these
   are the joints where one layer cannot proceed without another:
   - logic die ← foundry ← lithography;
   - accelerator ← HBM ← TSV stacking;
   - logic + HBM ← 2.5D packaging;
   - facility ← power connection.

   This is an `INTERPRETATION` built from the dependency table (§3). *How* critical
   each joint is (concentration, substitutability) is **not** assessed here. That needs
   the entity data and metrics planned for S07–S15.

---

## 2. Concept entries by layer

### Cross-layer anchor

#### X-01 — AI compute
- **Kind:** capability (the thing whose dependencies are mapped)
- **Definition** (`ATTRIBUTION` — CSET): computation at a scale that modern AI techniques
  rely on, "delivered by computer chips" tailored to AI calculations. **Working
  definition** (`INTERPRETATION`): the capacity to run AI training and inference
  workloads on AI accelerators installed in data centres.
- **Evidence:** SRC-003 p.3 — "This enormous computational power is delivered by computer chips"; SRC-003 p.3 — "specialized “AI chips” are essential for cost-effectively implementing AI at scale"; SRC-021 p.25 — "training workloads require the parallel processing capabilities of GPUs and ASICs"
- **Status:** verified (the working definition is a proposal; see TQ-12)
- **Upstream:** ACC-01, DC-01, EN-01 · **Downstream:** AI models and applications (out of scope)
- **Scope:** v1 — it is the object of the governing question.

### Layer 1 — AI accelerators

#### ACC-01 — AI accelerator ("AI chip")
- **Kind:** component/product class
- **Definition** (`ATTRIBUTION`, **disputed boundary**): CSET (2020) defines "AI chips"
  as GPUs, FPGAs and AI-specialised ASICs. LBNL (2026) counts "AI accelerators" as GPUs
  and ASICs; the report does not mention FPGAs. **Working definition**
  (`INTERPRETATION`): a data-centre logic chip, GPU or AI ASIC, whose primary purpose
  is AI training or inference.
- **Evidence:** SRC-003 p.4 — "Our definition of “AI chips” includes graphics processing units (GPUs), field-programmable gate arrays (FPGAs), and certain types of application-specific integrated circuits (ASICs)"; SRC-021 p.16 — "this update expands the accounting to all AI accelerators, namely ASICs"
- **Status:** disputed (boundary: FPGAs; see CON-01, TQ-01)
- **Upstream:** EDA-01, FAB-03, HBM-02, PKG-03 · **Downstream:** DC-05
- **Scope:** v1 — the central component of the question.

#### ACC-02 — Data-centre GPU
- **Kind:** component/product class
- **Definition** (`FACT`, two sources): a logic chip specialised for parallel processing,
  used for graphics and AI. Data-centre GPUs such as NVIDIA's H100 are built mainly for
  AI/HPC compute, not graphics.
- **Evidence:** SRC-002 p.66 — "Graphics processing units (GPUs) are specialized logic chips"; SRC-021 p.7 — "A type of processor particularly well-suited for parallel processing tasks"; SRC-006 — "primarily built for executing data center and edge compute workloads for AI, HPC, and data analytics, but not graphics processing"
- **Status:** verified
- **Upstream:** as ACC-01 · **Downstream:** DC-05
- **Scope:** v1 — the dominant accelerator type in the retrieved sources.

#### ACC-03 — AI ASIC (e.g. Google TPU, AWS Trainium)
- **Kind:** component/product class
- **Definition** (`FACT`): an application-specific integrated circuit (a logic chip
  specialised for one application) designed to accelerate machine-learning workloads.
  Google describes TPUs as ASICs. AWS calls Trainium2 a purpose-built machine-learning
  chip, and LBNL counts Trainium among AI ASICs.
- **Evidence:** SRC-002 p.65 — "Application-specific integrated circuits (ASICs) are logic chips with designs specialized for certain applications"; SRC-008 — "Tensor Processing Units (TPUs) are Google's custom-developed, application-specific integrated circuits (ASICs) used to accelerate machine learning workloads"; SRC-010 — "Trainium2 is the third generation, purpose-built Machine Learning chip from AWS"; SRC-021 p.17 — "with smaller numbers of Amazon Web Services (AWS) Trainium and Inferentia units"
- **Status:** verified
- **Upstream:** as ACC-01 · **Downstream:** DC-05, DC-03 (offered as cloud services)
- **Scope:** v1 — a second accelerator path whose designers are cloud providers (see §4, blur B-2).

#### ACC-04 — Fabless chip designer (actor type)
- **Kind:** actor type / business model
- **Definition** (`ATTRIBUTION` — CSET): a firm that designs and sells chips but buys
  fabrication from foundries and assembly, test and packaging (ATP) services from OSATs.
- **Evidence:** SRC-002 p.66 — "Fabless firms design and sell chips"; SRC-002 p.6 — "a fabless firm designs and sells the chip and purchases fabrication services from a foundry and ATP services from an outsourced semiconductor assembly and test (OSAT) firm"
- **Status:** verified
- **Upstream:** EDA-01 · **Downstream:** FAB-03, PKG-07
- **Scope:** v1 — the business model that creates the designer → foundry dependency.

#### ACC-05 — Multi-die accelerator
- **Kind:** technology / design approach
- **Definition** (`FACT`, company-reported example): an accelerator presented as one
  device but built from more than one logic die in one package. NVIDIA states all
  Blackwell products join two reticle-limited dies with a chip-to-chip interconnect.
- **Evidence:** SRC-007 — "two reticle-limited dies connected by a 10 terabytes per second (TB/s) chip-to-chip interconnect in a unified single GPU"
- **Status:** verified (for the example). Whether this counts as a "chiplet" design is open (TQ-09).
- **Upstream:** FAB-01, PKG-06 · **Downstream:** ACC-01
- **Scope:** v1 — makes the accelerator → advanced-packaging dependency explicit.

*Considered and excluded from Layer 1:* FPGAs (future; outside LBNL's accelerator
accounting, see CON-01), CPUs (future; host processors, not the accelerator
dependency), edge/mobile AI chips (future; the question concerns data-centre compute).

### Layer 2 — HBM (high-bandwidth memory)

#### HBM-01 — DRAM
- **Kind:** component class (memory chip)
- **Definition** (`ATTRIBUTION` — CSET): a memory chip that holds data while powered and
  loses it at power-down. HBM is built from DRAM dies (HBM-02).
- **Evidence:** SRC-002 p.66 — "Dynamic random-access memory (DRAM) is a memory chip"
- **Status:** verified
- **Upstream:** FAB-01 (memory fabrication) · **Downstream:** HBM-02
- **Scope:** v1 — HBM cannot be explained without it.

#### HBM-02 — High Bandwidth Memory (HBM)
- **Kind:** component/product class
- **Definition** (`FACT`, two independent makers): DRAM dies stacked vertically and
  connected by TSVs, giving a very wide data interface (SK hynix: 1,024 data paths) for
  AI and HPC processors.
- **Evidence:** SRC-011 — "vertically stacking multiple DRAMs using through-silicon via (TSV)"; SRC-011 — "It has a whopping 1,024 DQs"; SRC-015 — "high-performance, 3D-stacked DRAM designed to deliver massive data throughput"
- **Status:** verified. **Standards-body definition not retrieved:** the JEDEC HBM
  standards were blocked (HTTP 403), so the standardised definition is `not_researched`.
- **Upstream:** HBM-01, HBM-04, HBM-03 · **Downstream:** PKG-04, ACC-01
- **Scope:** v1 — a named Part A layer and a structural input to current accelerators (DEP-01).

#### HBM-03 — HBM base die
- **Kind:** component (logic die at the bottom of the stack)
- **Definition** (`ATTRIBUTION` — SK hynix): the die at the bottom of an HBM stack. It
  carries TSVs, the core DRAM dies sit on it, and it connects to the GPU. SK hynix says
  it made base dies with its own technology up to HBM3E, and plans to use TSMC's logic
  process for the HBM4 base die.
- **Evidence:** SRC-014 — "HBM is made by stacking a core DRAM die on top of a base die that features TSV"; SRC-014 — "plans to adopt TSMC’s advanced logic process for HBM4’s base die"
- **Status:** verified (stack structure). The HBM4 base-die sourcing is a **2024 plan**
  stated by one company (time-bound; see DEP-04).
- **Upstream:** FAB-01 (from HBM4, possibly a foundry logic process) · **Downstream:** HBM-02
- **Scope:** v1 — the point where the memory and foundry layers start to overlap.

#### HBM-04 — Through-silicon via (TSV)
- **Kind:** technology / process
- **Definition** (`FACT`, two sources): a vertical electrical connection that passes
  completely through a silicon die or wafer, enabling dies to be stacked. SK hynix
  classifies TSV as a **wafer-level package** technology.
- **Evidence:** SRC-012 — "In the earlier days, TSV was regarded merely as a packaging technology"; SRC-013 — "Therefore, TSV is classified as a wafer-level package technology"; SRC-014 — "HBM is made by stacking a core DRAM die on top of a base die that features TSV"
- **Status:** verified
- **Upstream:** SME-04 (plating, etch), SME-06 · **Downstream:** HBM-02, PKG-04, PKG-05
- **Scope:** v1 — the shared technology linking HBM, packaging and equipment.

#### HBM-05 — HBM generation
- **Kind:** attribute (product generation)
- **Definition** (`DERIVATION` from SK hynix): HBM is released in successive
  generations. SK hynix calls HBM3 the fourth generation and HBM4 the sixth, and its
  articles name HBM2E and HBM3E as intermediate generations.
- **Evidence:** SRC-011 — "As the fourth generation of HBM, HBM3"; SRC-014 — "the sixth generation of the HBM family"
- **Status:** verified (company numbering). JEDEC generation definitions are `not_researched` (403).
- **Upstream:** — · **Downstream:** HBM-02
- **Scope:** future — record as an attribute when product entities exist (S08). Not needed to identify the dependency.

#### HBM-06 — Memory manufacturer (actor type)
- **Kind:** actor type
- **Definition** (`DERIVATION`): a firm that fabricates DRAM, stacks it into HBM, and
  ships HBM to the maker of the logic package. CSET lists SK hynix and Micron among
  foundries/IDMs doing in-house ATP. SK hynix describes HBM being "sent to a system
  semiconductor manufacturer" for 2.5D packaging.
- **Evidence:** SRC-002 p.24 — "Hynix (South Korea), Micron (U.S.)"; SRC-013 — "Rather than being a fully packaged product, HBM is a semi-packaged product"
- **Status:** verified. Which HBM maker supplies which accelerator is `not_publicly_determinable` from the product documentation retrieved (SRC-006 names HBM3 but no supplier).
- **Upstream:** FAB-01, HBM-04 · **Downstream:** PKG-04
- **Scope:** v1 — the actor type behind the HBM layer.

*Considered and excluded from Layer 2:* 3D-TSV DRAM server modules / 3DS (future; not
accelerator memory, SRC-012/013), NAND/storage (future), HBM product specifications
(future, S08).

### Layer 3 — Advanced packaging

#### PKG-01 — Semiconductor packaging
- **Kind:** process / capability
- **Definition** (`FACT`, two sources): enclosing and connecting a fabricated chip. NIST
  gives two purposes: protect the chip, and provide inter-chip communication, power
  delivery and a test and system-integration platform.
- **Evidence:** SRC-002 p.67 — "Packaging bonds a fabricated chip to an encasing package"; SRC-004 p.4 — "Semiconductor packaging serves two general purposes"
- **Status:** verified
- **Upstream:** FAB-01, SME-06 · **Downstream:** ACC-01, HBM-02
- **Scope:** v1 — prerequisite for the advanced-packaging layer.

#### PKG-02 — Assembly, test and packaging (ATP) / "back-end"
- **Kind:** production segment
- **Definition** (`ATTRIBUTION` — CSET): the production step after fabrication. The
  finished wafer is cut into chips, which are mounted, enclosed and tested. It is done
  in-house by IDMs and foundries or outsourced to OSATs. SIA/BCG uses "back-end" for
  this segment.
- **Evidence:** SRC-002 p.45 — "taking a wafer with completed, unseparated chips and turning it into separate, packaged chips"; SRC-002 p.23 — "as in-house ATP services performed by integrated device manufacturers (IDMs) and foundries after fabrication"
- **Status:** verified
- **Upstream:** FAB-01 · **Downstream:** ACC-01
- **Scope:** v1 — the segment that contains advanced packaging.

#### PKG-03 — Advanced packaging
- **Kind:** technology family (umbrella term)
- **Definition** (`ATTRIBUTION`, **disputed breadth**): NIST ties it to heterogeneous
  integration of multi-component assemblies with many interconnects, to a degree that
  "blurs the line between chip and package". SIA/BCG says the term "covers a wide range
  of materials and manufacturing technologies", of which chiplet assembly is a small
  subset. **Working definition** (`INTERPRETATION`, v1): packaging that integrates
  multiple dies at high interconnect density. For v1 that means 2.5D interposer
  integration of logic and HBM (PKG-04), and vertical die stacking (PKG-05).
- **Evidence:** SRC-004 p.4 — "blurs the line between chip and package"; SRC-005 p.21 — "The term “advanced packaging” covers a wide range of materials and manufacturing technologies"
- **Status:** disputed (breadth; CON-04, TQ-03)
- **Upstream:** FAB-01, SME-06, EDA-01 (co-design, SRC-004 p.5) · **Downstream:** ACC-01
- **Scope:** v1 — a named Part A layer.

#### PKG-04 — 2.5D packaging with an interposer
- **Kind:** technology
- **Definition** (`FACT`, company sources): two or more active chips placed side by side
  on a silicon interposer, which carries the dense wiring between them. The interposer
  sits on a package substrate. SK hynix states HBM is integrated with a processor this
  way. SK hynix describes TSMC's CoWoS as one proprietary 2.5D process (`ATTRIBUTION`;
  entity-level example only).
- **Evidence:** SRC-013 — "In the 2.5D structure, two or more active semiconductor chips are placed side-by-side on a silicon interposer"; SRC-012 — "HBM is an in-package memory where it is integrated with a SoC through a silicon interposer inside the same package"; SRC-014 — "A TSMC proprietary packaging process that connects GPU/xPU, a logic chip, and HBM, on a special substrate called an interposer"
- **Status:** verified
- **Upstream:** HBM-04, FAB-01 (interposer and TSV wafer processing), SME-06 · **Downstream:** ACC-01
- **Scope:** v1 — the joint where logic and HBM meet (DEP-02).

#### PKG-05 — 3D die stacking
- **Kind:** technology
- **Definition** (`ATTRIBUTION` — SK hynix): active chips integrated by stacking dies
  vertically. HBM is the v1 case.
- **Evidence:** SRC-013 — "In the 3D structure, active chips are integrated by die stacking vertically"
- **Status:** verified
- **Upstream:** HBM-04 · **Downstream:** HBM-02
- **Scope:** v1 for HBM stacking only. Logic-on-logic 3D stacking is future.

#### PKG-06 — Chiplets / heterogeneous integration
- **Kind:** technology / design approach
- **Definition** (`ATTRIBUTION`, **disputed wording**): NIST says chiplets are "small,
  partially functional" chips that form a highly functional subsystem when assembled at
  tight pitch. SIA/BCG says heterogeneous integration combines chips and chiplets to
  match a monolithic SoC. SK hynix describes chiplets as logic chips divided by
  function and connected "with TSV".
- **Evidence:** SRC-004 p.7 — "Chiplets refer to small, partially functional, semiconductor chips"; SRC-005 p.21 — "Heterogeneous integration of chiplets is the process of combining multiple chips and chiplets to match the functionality of a single monolithic system-on-chip"; SRC-013 — "it is a technology that divides existing logic chips by function and connects them with TSV"
- **Status:** disputed (CON-03, TQ-09)
- **Upstream:** PKG-04, EDA-01 · **Downstream:** ACC-05
- **Scope:** v1 as a concept, because multi-die accelerators exist (ACC-05). The chiplet ecosystem and interconnect standards are future.

#### PKG-07 — Outsourced semiconductor assembly and test (OSAT) firm (actor type)
- **Kind:** actor type
- **Definition** (`ATTRIBUTION` — CSET): a firm that performs ATP for third parties.
  Amkor, an OSAT, states it performs TSV reveal and backside steps on wafers whose TSVs
  were already formed. It does not form TSVs in foundry wafers.
- **Evidence:** SRC-002 p.67 — "Outsourced semiconductor assembly and test (OSAT) firms perform assembly, testing, and packaging for third-party customers"; SRC-016 — "Amkor does NOT provide TSV formation in foundry wafers"
- **Status:** verified
- **Upstream:** FAB-03 (TSV formation), SME-06 · **Downstream:** ACC-01
- **Scope:** v1 — one of the two actor types that do advanced packaging (with foundries; blur B-3).

*Considered and excluded from Layer 3:* package substrates and their materials
(future — materials layer; SRC-004 p.6 notes silicon, glass or organic substrates),
flip-chip and fan-out wafer-level packaging as separate entries (future; they need
the TQ-03 breadth decision first), package test (future).

### Layer 4 — Foundries

#### FAB-01 — Wafer fabrication ("front end")
- **Kind:** process
- **Definition** (`ATTRIBUTION` — CSET): turning designs into chips on wafers. Fabs build
  transistors and then metal interconnects, layer by layer, using equipment and
  materials.
- **Evidence:** SRC-002 p.6 — "Semiconductor fabrication facilities (“fabs”) make chips"; SRC-002 p.3 — "Production relies on associated elements of the supply chain"
- **Status:** verified
- **Upstream:** SME-01, EDA-01 (via masks, EDA-03) · **Downstream:** ACC-01, HBM-01, PKG-02
- **Scope:** v1.

#### FAB-02 — Fab (fabrication facility)
- **Kind:** facility type
- **Definition** (`ATTRIBUTION` — CSET): a semiconductor fabrication facility where
  chips are made in wafers.
- **Evidence:** SRC-002 p.6 — "Semiconductor fabrication facilities (“fabs”) make chips"
- **Status:** verified
- **Upstream:** SME-01 · **Downstream:** FAB-03
- **Scope:** v1 — the facility type S09 will model temporally.

#### FAB-03 — Foundry
- **Kind:** business model, **used also** for a facility and for a firm
- **Definition** (`ATTRIBUTION`, **disputed usage**): CSET's glossary calls foundries
  *facilities* that make chips for third-party customers. The same report treats
  "foundry" as one of two *business models* for fabs (the other is the IDM). SIA/BCG
  speaks of a "pure-play foundry business". **Working definition**
  (`INTERPRETATION`): a business model in which fab capacity makes chips designed by
  other firms. The facility is a "fab" (FAB-02); the firm is a "foundry operator".
- **Evidence:** SRC-002 p.66 — "Foundries are semiconductor manufacturing facilities that manufacture chips for third-party customers"; SRC-002 p.19 — "foundries, i.e., fabs operating independently and manufacturing chips for third-party customers"; SRC-005 p.6 — "Taiwan in the pure-play foundry business"
- **Status:** disputed (usage; CON-05, TQ-04)
- **Upstream:** FAB-02, SME-01, EDA-01 · **Downstream:** ACC-04, HBM-03 (from HBM4), PKG-04
- **Scope:** v1 — a named Part A layer.

#### FAB-04 — Integrated device manufacturer (IDM) (actor type)
- **Kind:** actor type / business model
- **Definition** (`ATTRIBUTION` — CSET): a firm that does all three production steps:
  design, fabrication, and ATP.
- **Evidence:** SRC-002 p.66 — "Integrated device manufacturers (IDMs) are firms that perform all three steps of production"
- **Status:** verified
- **Upstream:** SME-01, EDA-01 · **Downstream:** HBM-06 (memory makers do in-house ATP, SRC-002 p.24)
- **Scope:** v1 — needed to separate foundry dependencies from in-house manufacturing.

#### FAB-05 — Process technology ("node")
- **Kind:** attribute of a fabrication process
- **Definition** (`ATTRIBUTION` + `DERIVATION`): ASML says each new chip generation is
  "often referred to as a ‘node’". NVIDIA names vendor-specific processes for its GPUs
  (H100: "TSMC 4N process customized for NVIDIA"; Blackwell: "custom-built TSMC 4NP").
  CSET compares one firm's "10 nm" with another's "7 nm", which shows node names are
  **not comparable** across firms (`DERIVATION`).
- **Evidence:** SRC-017 — "often referred to as a ‘node’"; SRC-006 — "fabricated using the TSMC 4N process customized for NVIDIA"; SRC-007 — "manufactured using a custom-built TSMC 4NP process"; SRC-002 p.23 — "Intel is fabricating 10 nm logic chips with specifications competitive with TSMC’s 7 nm node chips"
- **Status:** verified
- **Upstream:** SME-02, SME-03 · **Downstream:** ACC-01
- **Scope:** v1 as an attribute of the accelerator → foundry link. The NVIDIA/TSMC statements are attributed examples, not S10 edges.

#### FAB-06 — Leading-edge / advanced logic
- **Kind:** attribute (capability class)
- **Definition** (`ATTRIBUTION`, **threshold is source-specific**): SIA/BCG uses
  "advanced node (<10 nanometers)". Other retrieved sources give no common threshold.
- **Evidence:** SRC-005 p.30 — "advanced node (<10 nanometers)"
- **Status:** disputed (no agreed threshold; TQ-07)
- **Upstream:** SME-02 · **Downstream:** ACC-01
- **Scope:** v1 — "which fabs can make accelerator logic dies" depends on it. The threshold needs a human decision.

*Considered and excluded from Layer 4:* silicon wafers and fab materials (future —
materials layer; SRC-002 p.67), mature-node and analog fabrication (future), fab
capacity figures (out of scope — metrics).

### Layer 5a — EDA (design software)

#### EDA-01 — Electronic design automation (EDA)
- **Kind:** technology (software, plus some hardware per Synopsys)
- **Definition** (`FACT`, two sources): software used to design chips. Synopsys adds
  hardware tools, and a scope that runs from architecture to verification and
  "preparation for manufacturing".
- **Evidence:** SRC-002 p.6 — "EDA is software used to design chips"; SRC-018 — "Electronic design automation (EDA) is a set of software and hardware tools that help engineers design and build electronic systems"
- **Status:** verified
- **Upstream:** EDA-03 (process information from fabs) · **Downstream:** ACC-04, FAB-01, PKG-03
- **Scope:** v1 — structural input to accelerator design (DEP-09).

#### EDA-02 — Core IP (licensable design blocks)
- **Kind:** product class
- **Definition** (`FACT`, two sources): reusable, pre-designed blocks licensed for use
  in chip designs. Synopsys notes EDA vendors often supply them.
- **Evidence:** SRC-002 p.65 — "Core intellectual property (IP) consists of reusable modular portions of chip designs"; SRC-018 — "EDA vendors often provide pre-designed and pre-verified block designs (IP)"
- **Status:** verified
- **Upstream:** — · **Downstream:** ACC-04
- **Scope:** future — a real design input, but not needed to locate the physical dependencies behind AI compute in v1.

#### EDA-03 — Design-to-manufacturing handoff (masks, process information)
- **Kind:** process / interface
- **Definition** (`ATTRIBUTION`): Synopsys says its mask-synthesis tools deliver mask
  sets "to foundries". CSET says each chipmaker's process limits design options, and
  that leading chipmakers give top EDA firms preferential access to process
  information (as of its 2019 data).
- **Evidence:** SRC-018 — "Mask synthesis and mask data prep tools ensure quality mask sets are delivered to foundries"; SRC-002 p.50 — "Each chipmaker’s manufacturing process uniquely limits chip design options"; SRC-002 p.50 — "give the top U.S. EDA firms, such as Synopsys and Cadence, preferential access to process IP"
- **Status:** verified (the preferential-access arrangement is dated; see DEP-10)
- **Upstream:** FAB-03 · **Downstream:** EDA-01, FAB-01
- **Scope:** v1 — it makes EDA and foundries **co-dependent**, which matters for TQ-05.

### Layer 5b — Semiconductor manufacturing equipment (SME)

#### SME-01 — Semiconductor manufacturing equipment (SME)
- **Kind:** product class (capital equipment)
- **Definition** (`ATTRIBUTION` — CSET): tools used to fabricate, assemble, test and
  package chips.
- **Evidence:** SRC-002 p.67 — "Semiconductor manufacturing equipment includes tools used to fabricate, assemble, test, and package chips"
- **Status:** verified
- **Upstream:** — (SME's own supply chain is future scope) · **Downstream:** FAB-01, PKG-02
- **Scope:** v1 — a named Part A layer.

#### SME-02 — Lithography
- **Kind:** process + equipment class
- **Definition** (`ATTRIBUTION` — CSET): drawing circuit patterns into light-sensitive
  chemicals on a wafer. Photolithography is the main technique.
- **Evidence:** SRC-002 p.66 — "Lithography draws patterns in chemicals"
- **Status:** verified
- **Upstream:** SME-01 · **Downstream:** FAB-01
- **Scope:** v1.

#### SME-03 — EUV and DUV lithography
- **Kind:** technology
- **Definition** (`FACT` for the technical role; `ATTRIBUTION` for exclusivity): ASML
  states EUV uses 13.5 nm light and prints "the most intricate layers" of a chip, with
  DUV systems printing the rest. It describes EUV as "unique to ASML". CSET (2019 data)
  calls advanced photolithography equipment — "especially" EUV scanners and,
  secondarily, ArF immersion scanners — necessary for mass-producing advanced chips. It
  does not say this of EUV alone.
- **Evidence:** SRC-017 — "EUV systems are used to print the most intricate layers on a chip, with the rest of the layers printed using various DUV systems"; SRC-017 — "The technology, which is unique to ASML, prints microchips using light with a wavelength of just 13.5 nm"; SRC-002 p.30 — "necessary for mass-production of advanced chips"
- **Status:** verified. The node threshold below which EUV is necessary is `not_researched`: the retrieved sources assert necessity but do not set a threshold.
- **Upstream:** SME-01 · **Downstream:** FAB-05, FAB-06
- **Scope:** v1 — a candidate single-technology joint in the chain.

#### SME-04 — Core wafer-processing tools (deposition, etch and clean, CMP, ion implantation)
- **Kind:** equipment classes / processes
- **Definition** (`FACT`, two sources): deposition adds thin films. Etch removes
  material selectively to form features. CMP flattens the wafer. Ion implantation adds
  dopants. Lam states copper plating (a deposition method) is also used for TSVs and
  wafer-level packaging.
- **Evidence:** SRC-002 p.65 — "Deposition adds thin films of materials on a wafer"; SRC-019 — "Etch processes help create chip features by selectively removing films and materials that have been deposited on the wafer"; SRC-019 — "Metal plating of copper and other metals is also used for through-silicon vias and wafer-level packaging applications"
- **Status:** verified
- **Upstream:** SME-01 · **Downstream:** FAB-01, HBM-04, PKG-04
- **Scope:** v1 at class level. Individual tool types are future.

#### SME-05 — Process control (metrology and inspection)
- **Kind:** equipment class
- **Definition** (`ATTRIBUTION` — CSET): tools that monitor wafers, photomasks and the
  process to keep error rates low, including wafer-level packaging inspection.
- **Evidence:** SRC-002 p.67 — "Process control tools monitor wafers, photomasks, and the overall chip manufacturing process"
- **Status:** verified
- **Upstream:** SME-01 · **Downstream:** FAB-01, PKG-02
- **Scope:** future — needed in a fuller equipment map. Not a distinct joint for the first answer.

#### SME-06 — Assembly, packaging and wafer-level packaging tools
- **Kind:** equipment class
- **Definition** (`DERIVATION`): CSET lists assembly and packaging tools (dicing,
  bonding, packaging). NIST states advanced packaging needs "wafer-based fab
  processes". Amkor describes TSV reveal and backside processing (middle-end-of-line).
  Together: advanced packaging draws on both packaging tools and fab-type wafer tools.
- **Evidence:** SRC-002 p.45 — "taking a wafer with completed, unseparated chips and turning it into separate, packaged chips"; SRC-004 p.5 — "wafer-based fab processes necessary for advanced packaging"; SRC-016 — "Amkor does NOT provide TSV formation in foundry wafers"
- **Status:** verified
- **Upstream:** SME-01 · **Downstream:** PKG-03, PKG-04, HBM-04
- **Scope:** v1 — the equipment side of the packaging joint.

*Considered and excluded from Layer 5b:* test equipment (future), photomasks and mask
making (future; bridges EDA-03 and SME-02), fab materials (photoresists, gases, wet
chemicals; future), the SME industry's own suppliers (future).

### Layer 6 — Cloud / data centres

#### DC-01 — Data centre
- **Kind:** facility type
- **Definition** (`ATTRIBUTION` — LBNL): "A facility used to house computer systems and
  associated components", mainly for data storage and processing.
- **Evidence:** SRC-021 p.6 — "Data Center – A facility used to house computer systems and associated components"
- **Status:** verified. SRC-021 p.24 mentions colocation and enterprise data centres but the pages read do not define them, and "hyperscale" does not appear, so sub-types are `not_researched`.
- **Upstream:** DC-05, DC-06, EN-04 · **Downstream:** DC-02, X-01
- **Scope:** v1 — a named Part A layer.

#### DC-02 — Cloud computing
- **Kind:** service/delivery model
- **Definition** (`FACT` — NIST, authoritative definition): "a model for enabling
  ubiquitous, convenient, on-demand network access to a shared pool of configurable
  computing resources". Its infrastructure has a physical layer of hardware (server,
  storage, network components).
- **Evidence:** SRC-001 p.6 — "Cloud computing is a model for enabling ubiquitous, convenient, on- demand network access"; SRC-001 p.6 — "The physical layer consists of the hardware resources that are necessary to support the cloud services being provided"
- **Status:** verified
- **Upstream:** DC-01, DC-05 · **Downstream:** X-01 (users)
- **Scope:** v1 — a named Part A layer. Most users reach AI compute through it.

#### DC-03 — Infrastructure as a Service (IaaS)
- **Kind:** service model
- **Definition** (`FACT` — NIST): the consumer provisions processing, storage, networks
  and other computing resources, without managing the underlying infrastructure.
  Example (`FACT`, company-reported): Google offers TPUs through Compute Engine and
  other services.
- **Evidence:** SRC-001 p.7 — "The capability provided to the consumer is to provision processing, storage, networks, and other fundamental computing resources"; SRC-008 — "You can use TPUs through Compute Engine, Google Kubernetes Engine"
- **Status:** verified
- **Upstream:** DC-02 · **Downstream:** X-01
- **Scope:** v1 — the usual way accelerator capacity is consumed.

#### DC-04 — Cloud provider (actor type) and cloud location abstraction
- **Kind:** actor type + location concept
- **Definition** (`FACT` — NIST, AWS): a public cloud exists on the provider's
  premises. Resource pooling gives "a sense of location independence": customers may
  specify location only at a higher level (country, state, data centre). AWS defines
  an Availability Zone as one or more discrete data centres with redundant power,
  networking and connectivity.
- **Evidence:** SRC-001 p.7 — "It exists on the premises of the cloud provider"; SRC-020 — "AWS operates state-of-the-art, highly available data centers"; SRC-001 p.6 — "There is a sense of location independence"; SRC-020 — "Each Availability Zone consists of one or more discrete data centers, each with redundant power, networking, and connectivity, and housed in separate facilities"
- **Status:** verified. "Hyperscaler" has no definition in the retrieved sources (`not_researched`).
- **Upstream:** DC-01 · **Downstream:** DC-03
- **Scope:** v1 — needed for D-008. Location evidence for cloud capacity is structurally abstracted (see §6).

#### DC-05 — Accelerated server
- **Kind:** component/product class (system)
- **Definition** (`ATTRIBUTION` — LBNL): a server (a computer providing services to
  others over a network) configured with GPUs or ASICs. LBNL models configurations of
  2, 4 or 8 GPUs, and ASIC-accelerated servers.
- **Evidence:** SRC-021 p.7 — "Server – A computer or system providing data, resources, or services to other computers"; SRC-021 p.25 — "training workloads require the parallel processing capabilities of GPUs and ASICs"
- **Status:** verified
- **Upstream:** ACC-01 · **Downstream:** DC-01, EN-03
- **Scope:** v1 — the unit that carries an accelerator into a facility. The actors who build servers are `not_researched` (TQ-11).

#### DC-06 — Rack-scale architecture and liquid cooling
- **Kind:** technology (system design)
- **Definition** (`ATTRIBUTION` — LBNL; example `FACT`, company-reported): a
  high-density AI server design that shares power supplies and cooling across the
  nodes in a rack. NVIDIA describes its GB200 NVL72 as rack-scale and liquid-cooled.
  LBNL says cooling dominates facility infrastructure energy.
- **Evidence:** SRC-021 p.7 — "Rack-Scale Architecture – A server architecture designed for high-density AI installations"; SRC-007 — "in a rack-scale, liquid-cooled design"; SRC-021 p.27 — "Cooling systems, which dominate facility infrastructure energy use"
- **Status:** verified
- **Upstream:** DC-05 · **Downstream:** DC-01, EN-01
- **Scope:** v1 at concept level: it is where chip density becomes facility cooling and power demand. Cooling technology detail is future.

*Considered and excluded from Layer 6:* networking and interconnect such as NVLink,
InfiniBand or TPU ICI (future, per the S01 non-goals and MA §6.4). Accelerators are
grouped over dedicated networks: SRC-009 — "A TPU Pod is a contiguous set of TPUs
grouped together over a specialized network". This is a real dependency, deferred on
purpose. storage (future),
data-centre sub-types (future, `not_researched`), PaaS/SaaS (future), and data-centre
construction supply chains (future).

### Layer 7 — Energy interface

**Boundary** (`INTERPRETATION`, proposed; TQ-10). The energy interface **begins** at the
electrical rating of chips and servers (EN-03). It **includes** facility overhead
(EN-01), facility power capacity (EN-04) and the site's connection to supply: grid
interconnection or on-site generation (EN-02, EN-05). It **ends** at the utility's
point of connection and the service terms that govern it (EN-06). Out of scope:
generation mix, transmission planning, fuels, emissions and water. LBNL's
interconnection definition marks the edge with "at its point of connection to the
grid".

#### EN-01 — Power usage effectiveness (PUE) and facility overhead
- **Kind:** metric definition (the definition only; no values)
- **Definition** (`ATTRIBUTION` — LBNL): the ratio of total facility energy use (including
  cooling and power distribution) to IT equipment energy use.
- **Evidence:** SRC-021 p.7 — "PUE (Power Usage Effectiveness) – A measure of how efficiently a data center uses energy"
- **Status:** verified. The standard definitions (The Green Grid; ISO/IEC 30134-2) were not retrievable (member-only / 403), so they are `not_researched`.
- **Upstream:** DC-06 · **Downstream:** EN-04
- **Scope:** v1 — the concept linking IT load to facility load.

#### EN-02 — Grid interconnection capacity
- **Kind:** attribute of the facility–grid interface
- **Definition** (`ATTRIBUTION` — LBNL): the maximum power a data centre requests from the
  utility or grid operator at its point of connection, reflecting total facility needs
  plus design margins. LBNL notes its utilisation "is not well documented".
- **Evidence:** SRC-021 p.6 — "Grid Interconnection Capacity – The maximum amount of electrical power a data center requests from the utility or grid operator"; SRC-021 p.12 — "Current utilization of interconnection capacity is not well documented"
- **Status:** verified
- **Upstream:** EN-04 · **Downstream:** utility grid (out of scope)
- **Scope:** v1 — the outer edge of the interface.

#### EN-03 — Chip and server power ratings (TDP, rated power)
- **Kind:** attributes
- **Definition** (`ATTRIBUTION` — LBNL): TDP is the maximum heat a chip or component
  produces that the cooling system is designed to remove. Rated power is a server's
  maximum power draw as specified by its manufacturer.
- **Evidence:** SRC-021 p.7 — "TDP (Thermal Design Power) – The maximum amount of heat generated by a computer chip or component"; SRC-021 p.7 — "Rated Power – The maximum power consumption of a server as specified by the manufacturer"
- **Status:** verified
- **Upstream:** ACC-01, DC-05 · **Downstream:** EN-01, EN-04
- **Scope:** v1 — where the chip layers meet the energy interface.

#### EN-04 — Facility power capacity (nameplate IT capacity)
- **Kind:** attribute
- **Definition** (`ATTRIBUTION` — LBNL): data-centre "capacity" can mean the facility's
  nameplate capacity (the IT load it is designed to serve) or the interconnection
  capacity it requested. The two are different quantities.
- **Evidence:** SRC-021 p.12 — "the facility's nameplate capacity—the IT hardware load it is designed to serve"
- **Status:** verified
- **Upstream:** EN-03, EN-01 · **Downstream:** EN-02
- **Scope:** v1 — prevents a known ambiguity in facility records (TQ-10).

#### EN-05 — On-site and backup generation
- **Kind:** infrastructure option
- **Definition** (`ATTRIBUTION`): EPRI says sites favour places where they can build
  backup power, usually natural-gas or diesel generators. LBNL says some data centres may
  skip grid interconnection and build their own generation.
- **Evidence:** SRC-023 p.5 — "where the centers can develop backup power to ensure power supply (usually natural gas or diesel generators)"; SRC-021 p.12 — "some data centers may forgo grid interconnection altogether and build their own generation capacity"
- **Status:** verified
- **Upstream:** — · **Downstream:** DC-01
- **Scope:** future — record the option now; model it after the base graph is reliable (MA §6.4).

#### EN-06 — Utility service terms for large loads
- **Kind:** institutional arrangement
- **Definition** (`ATTRIBUTION` — LBNL): tariffs set the price, terms and conditions of
  electricity service and need regulatory approval. LBNL reports "no industry-standard
  tariff design" for large loads. EPRI reports connection lead times of one to two
  years (2024).
- **Evidence:** SRC-022 p.3 — "Utility tariffs define the price, terms, and conditions of electricity service"; SRC-022 p.4 — "To date, there is no industry-standard tariff design"; SRC-023 p.2 — "Connection lead times of one to two years"
- **Status:** verified
- **Upstream:** — · **Downstream:** EN-02
- **Scope:** future — sits at the energy–policy boundary (S17+).

---

## 3. Concept-level dependencies

Verbs use MA §6.2 where one fits. Verbs marked † are **not** in MA §6.2 and are listed
as input for S04. **Structural** means true of the technology itself; **contingent**
means true of a current market or organisational arrangement. The two need different
evidence (see "Evidence that would establish it").

| ID | Dependency (concept level) | Verb | Type | Claim class · evidence | Evidence that would establish it (entity level) | Likely non-public |
|---|---|---|---|---|---|---|
| DEP-01 | Current data-centre accelerators → HBM | `uses` | **structural need** (bandwidth), **contingent solution** (HBM specifically) | `ATTRIBUTION`: SK hynix says training bandwidth demand "cannot be satisfied with conventional main memories" (SRC-012). `FACT` examples: H100 uses HBM3 (SRC-006); TPUs have HBM (SRC-008). | product datasheets naming memory type | which maker's HBM goes into which product (SRC-006 names none) → `not_publicly_determinable` from product docs |
| DEP-02 | HBM → 2.5D packaging with the logic die | `requires` | structural (for in-package HBM) | `FACT` (two SK hynix sources): HBM is "semi-packaged" and joined to logic on an interposer (SRC-013, SRC-012) | package-level technical disclosures | which packaging line or site packages which product |
| DEP-03 | HBM → TSV stacking | `requires` | structural | `FACT`: SRC-011, SRC-013, SRC-014 | memory-maker process disclosures | process yields and capacity |
| DEP-04 | HBM base die → foundry logic process (from HBM4) | `depends_on` | **contingent** (announced plan, 2024) | `ATTRIBUTION`: SRC-014 (SK hynix plan; before HBM4 its base dies used its own technology) | later primary confirmation of production | contract terms |
| DEP-05 | Fabless accelerator designer → foundry fabrication | `depends_on` (†`fabricates` from the foundry side) | structural *for the fabless model*; which foundry is contingent | `FACT` for the model (SRC-002 p.6). `FACT` company-reported examples: NVIDIA on TSMC 4N/4NP (SRC-006, SRC-007) | designer's own documentation or filings naming the process | wafer allocation and volumes |
| DEP-06 | Advanced packaging → wafer-fab processes and equipment | `requires` | structural | `DERIVATION`: SRC-004 p.5, SRC-016, SRC-019 | tool and process disclosures | tool-level supplier relationships |
| DEP-07 | Wafer fabrication → SME (lithography, deposition, etch …) | `requires` | structural | `FACT`: SRC-002 p.6–7, SRC-019 | equipment-maker disclosures; fab announcements | installed tool base per fab |
| DEP-08 | Most intricate layers at advanced nodes → EUV lithography | `requires` | structural at current technology; **exclusivity is attributed** | `ATTRIBUTION`: SRC-017 (ASML), SRC-002 p.30 (CSET, 2019 data) | technical literature on patterning alternatives (`not_researched`) | tool shipments per customer |
| DEP-09 | Chip design → EDA | `requires` | structural (at modern complexity) | `FACT`: SRC-002 p.6, SRC-018 | — | tool licences per designer |
| DEP-10 | EDA ↔ foundry process information | `depends_on` (two-way) | structural (designs must fit a process); **preferential access is contingent** (2019) | `ATTRIBUTION`: SRC-002 p.50; SRC-018 | EDA/foundry certification announcements | terms of early access |
| DEP-11 | Accelerator supply → die supply | `depends_on` | **contingent** (market state) | `ATTRIBUTION` (second-hand: LBNL reporting IDC analysts): "the market is currently constrained by die supply" (SRC-021 p.18). The source does not say which stage (wafer fabrication, HBM or packaging) limits die supply | shipment and capacity data | die allocation (`not_publicly_determinable`) |
| DEP-12 | Accelerated servers → data centre (housing, power, cooling) | †`houses` | structural | `FACT`: SRC-021 p.6, p.27 | facility disclosures | installed accelerator counts per site: LBNL says ASIC deployers "rarely disclose detailed shipment or deployment figures" (SRC-021 p.17) → `not_publicly_determinable` |
| DEP-13 | Cloud service → data centres | `operates` / `depends_on` | structural | `FACT`: SRC-001 p.6 (physical layer), SRC-020 | provider infrastructure pages | exact facility behind a service (location abstraction, SRC-001 p.6) |
| DEP-14 | Accelerator access → cloud offering (IaaS) | †`offered_via` | contingent (many users rent rather than own) | `FACT` example: SRC-008 | provider service catalogues | — |
| DEP-15 | Cloud provider → own accelerator design (vertical integration) | †`designs` | contingent (a business choice) | `FACT` examples: SRC-008 (Google TPU), SRC-010 (AWS Trainium2) | company docs | internal volumes (SRC-021 p.17) |
| DEP-16 | Data centre → electricity supply (grid or on-site) | `requires` | structural (electricity); **contingent** (grid vs own generation) | `ATTRIBUTION`: SRC-021 p.6, p.12; SRC-023 p.5 | utility filings, interconnection queues | interconnection agreements; LBNL: utilisation "not well documented" (SRC-021 p.12) |
| DEP-17 | Chip power → server power → facility power (PUE) → interconnection capacity | chain of `requires` | structural (physics); the conversions are model assumptions | `DERIVATION`: SRC-021 p.6–7, p.12 | measured facility data | per-site measured data |
| DEP-18 | Advanced packaging → design/simulation co-design | `requires` | structural | `ATTRIBUTION`: SRC-004 p.5 — "strong interdependency between chip design and packaging" | EDA product disclosures | — |

**Verbs for S04** (not in MA §6.2; some appear in `SESSION-ROADMAP.md` S04):
`designs`, `fabricates`, `packages`, `houses`, `offered_via`, `integrates` (HBM with
logic in one package), `supplies_power_to`, `stacks_on` (HBM dies on base die). The
roadmap's S04 list already has `designs`, `packages` and `fabricates`.

---

## 4. Kinds of concept, and where they blur

Required reasoning, S01 Part B §06, question 2 (`INTERPRETATION` unless cited).

| Layer | Technology | Component / product | Process / capability | Actor type | Facility |
|---|---|---|---|---|---|
| 1 Accelerators | multi-die design (ACC-05) | AI accelerator, GPU, AI ASIC | design | fabless designer; cloud provider as designer | — |
| 2 HBM | TSV, 3D stacking | DRAM die, HBM stack, base die | memory fabrication, stacking | memory manufacturer (IDM) | memory fab |
| 3 Adv. packaging | 2.5D interposer, chiplets | interposer, substrate | packaging, ATP | OSAT; foundry (in-house); memory maker | packaging facility |
| 4 Foundries | process technology / node | wafer | wafer fabrication | foundry operator; IDM | fab |
| 5a EDA | EDA software | core IP, mask data | design flow, DFM | EDA vendor | — |
| 5b SME | EUV/DUV, deposition, etch | tools | tool manufacturing | equipment maker | — |
| 6 Cloud / DC | rack-scale, liquid cooling | accelerated server | IaaS | cloud provider | data centre, availability zone |
| 7 Energy | — | — | interconnection, on-site generation | utility (future) | substation / plant (future) |

**Where the categories blur:**

- **B-1 TSV is several kinds of thing at once.** SK hynix calls it a wafer-level package
  technology (SRC-013). It is formed in wafer processing (Amkor does not form TSVs in
  foundry wafers, SRC-016). It relies on deposition and plating tools (SRC-019). One
  technology spans layers 2, 3, 4 and 5b.
- **B-2 Cloud providers are also accelerator designers** (SRC-008, SRC-010), so a single
  actor spans layers 1 and 6.
- **B-3 "Packaging" is not only done by packagers.** Foundries and IDMs do in-house ATP
  (SRC-002 p.23). SK hynix describes CoWoS as a TSMC (foundry) process (SRC-014). The
  foundry and packaging layers overlap for AI accelerators.
- **B-4 HBM is both a product and an input to packaging.** It ships "semi-packaged"
  (SRC-013). From HBM4 its base die may be a foundry logic die (SRC-014).
- **B-5 EDA reaches into manufacturing** (mask synthesis, DFM, SRC-018) and into
  packaging (co-design, SRC-004 p.5).

---

## 5. Source conflicts (preserved, not resolved)

| ID | Topic | Position A | Position B | Handling |
|---|---|---|---|---|
| CON-01 | Scope of "AI accelerator" | CSET (2020): GPUs, FPGAs, AI ASICs (SRC-003 p.4) | LBNL (2026): GPUs and ASICs (SRC-021 p.16) | working definition excludes FPGAs from v1; TQ-01 |
| CON-02 | Where HBM sits | Google: "on-chip high-bandwidth memory (HBM)" (SRC-008) | SK hynix: "in-package memory" on an interposer (SRC-012) | treated as loose wording by Google (`INTERPRETATION`); TQ-02 |
| CON-03 | What a chiplet is | NIST: small, partially functional chips assembled at tight pitch (SRC-004 p.7) | SK hynix: logic divided by function and "connects them with TSV" (SRC-013); SIA: integration to match a monolithic SoC (SRC-005 p.21) | kept as three attributed definitions; TQ-09 |
| CON-04 | Breadth of "advanced packaging" | NIST: heterogeneous integration that "blurs the line between chip and package" (SRC-004 p.4) | SIA/BCG: covers "a wide range of materials and manufacturing technologies" (SRC-005 p.21) | narrow v1 working definition; TQ-03 |
| CON-05 | What "foundry" names | CSET glossary: a facility (SRC-002 p.66) | CSET body text / SIA: a business model (SRC-002 p.19; SRC-005 p.6) | term split into fab / foundry model / foundry operator; TQ-04 |

**Source-quality observation** (Verifier, `INTERPRETATION`): SRC-002 Table 6 (p.24)
lists "Samsung (U.S.)" among in-house ATP firms. This looks like a typographical
error. S01 does not rely on that table's country labels, and no country attribution
in this map comes from it.

---

## 6. Location and jurisdiction evidence found (pointers only, D-008)

D-008 asks sessions to record location/jurisdiction evidence where they find it,
without classifying anything as EU or non-EU. These are **pointers** for later
sessions. No figures are restated or analysed (metrics are out of scope for S01).

- SRC-004 p.4: NIST states "the vast majority of advanced packaging manufacturing
  capacity currently resides in Asia" (`ATTRIBUTION`, 2023).
- SRC-005 p.20–21: SIA/BCG ATP-capacity distribution by region (figures not restated).
- SRC-002 p.8 (Table 1): value-add and market shares by **firm headquarters**, 2019 data.
  CSET notes headquarters "may not fully capture national competitiveness" (p.5).
- SRC-001 p.6 and SRC-020: cloud location is **abstracted**. Customers may know only
  a country or region, not the facility. `IMPLICATION`: location evidence for cloud AI
  compute will often be `not_publicly_determinable` at facility level.

---

## 7. Terminology questions for the human (Part A "Human task")

Each question gives the options found in sources and the working choice used in this
draft. Please challenge any of them. Answers go to S02.

- **TQ-01 "AI accelerator" vs "AI chip".** Include FPGAs (CSET), or only GPUs and ASICs
  (LBNL)? *Working choice:* GPUs + AI ASICs; FPGAs as future scope. Should CPUs used for
  inference (SRC-021 p.25) ever count?
- **TQ-02 "On-chip" vs "in-package" HBM.** *Working choice:* in-package (HBM is a
  separate stack beside the logic die). Is "on-package memory" a better neutral term?
- **TQ-03 "Advanced packaging" breadth.** Narrow (2.5D/3D integration of logic and HBM)
  or broad (everything SIA/BCG counts, including flip-chip and fan-out)? *Working
  choice:* narrow for v1.
- **TQ-04 "Foundry".** Facility, business model or firm? *Working choice:* "fab" is the
  facility, "foundry" the business model, "foundry operator" the firm. Do IDMs that sell
  foundry services count as foundries for v1?
- **TQ-05 Should "EDA/equipment" stay one layer?** EDA is design-stage software. SME is
  manufacturing capital equipment. They share only being "production inputs"
  (SRC-002 p.3), and EDA is co-dependent with foundries (EDA-03). *Working choice:*
  two sub-layers, 5a and 5b (proposed D-013). Keep one layer, or split into two?
- **TQ-06 "Front end" / "back end" / "middle end".** Amkor uses "middle-end-of-line" for
  TSV reveal (SRC-016). Should the Atlas model a middle stage, or tag processes by the
  actor that performs them?
- **TQ-07 "Leading edge" / "advanced node" threshold.** SIA/BCG uses <10 nm (SRC-005 p.30).
  Node names are vendor labels that are not comparable across firms (FAB-05). Should
  v1 use a numeric threshold, vendor-declared process generations, or "requires EUV"
  (SME-03)?
- **TQ-08 "Data centre" vs "cloud".** *Working choice:* data centre is a facility,
  cloud is a service model delivered from facilities. Is "hyperscaler" needed as a
  term? No retrieved source defines it.
- **TQ-09 "Chiplet".** Three competing definitions (CON-03). Is NVIDIA's two-die GPU
  (ACC-05) a chiplet design? The retrieved NVIDIA page does not use the word.
- **TQ-10 Energy-interface boundary.** Is "ends at the utility point of connection" the
  right edge? Should "capacity" always be qualified as nameplate IT capacity or
  interconnection capacity (EN-04)?
- **TQ-11 A missing layer?** Server/system integration (accelerated servers, rack-scale
  systems) sits between Part A's "accelerators" and "data centres" but is not a Part A
  layer. Add it, or keep it inside "cloud/data centres"?
- **TQ-12 "AI compute".** Is the working definition in X-01 (the capacity to run AI
  workloads on accelerators in data centres) the right top node?

---

## 8. Gaps and open evidence work

- **Blocked primary sources** (see the register): JEDEC (HBM standards), TSMC
  (foundry/CoWoS), Samsung, Intel, SEC filings, IEA, Green Grid / ISO (PUE). Each is a
  better source for some entries than the one used.
- **`not_researched`:** the EUV necessity threshold (SME-03); data-centre sub-types
  (DC-01); "hyperscaler" (DC-04); server-integration actors (DC-05); HBM
  standards-body definitions (HBM-02, HBM-05); PUE standard definitions (EN-01);
  alternatives to EUV patterning (DEP-08).
- **`not_publicly_determinable` (on current evidence):** HBM supplier per accelerator
  (HBM-06, DEP-01); accelerator deployment counts per site (DEP-12); die/wafer
  allocation (DEP-05, DEP-11); interconnection-capacity utilisation (DEP-16).
- **Dated evidence:** CSET's market-structure statements are 2019 data (SRC-002 p.5);
  SK hynix's HBM4 base-die plan is a 2024 statement (SRC-014). Both need re-checking
  before any canonical record relies on them.
