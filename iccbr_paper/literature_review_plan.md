# Literature Review Plan — ICCBR 2026 Paper

**Purpose:** Research brief for gathering literature, papers, and comparisons
for the ICCBR 2026 paper on NormCode as a reasoning medium that realizes
Case-Based Reasoning at two levels.

**Paper thesis:** NormCode is a reasoning medium — a representational language
with six properties (Interpretable, Enforceable, Composable, Locally Addressable,
Generalizable, Portable) — that realizes CBR natively at two levels:
- **Level 1**: Execution checkpoints as suspended NormCode runtimes = concrete cases
- **Level 2**: NormCode plans as runtime definitions = abstract cases; the
  compilation pipeline as the distillation process; self-hosting as recursive CBR

**Submission category:** Deployed Applications
**Companion paper:** arXiv:2512.10563 (NormCode language specification)

---

## New Research Questions (ICCBR framing)

1. What is the state of Process-Oriented CBR (POCBR), and what prior work
   establishes the notion of workflow traces as cases?

2. Has anyone in CBR treated runtime states (suspended execution environments)
   as cases? What is the closest prior work?

3. What is the literature on multi-level or hierarchical CBR — cases at both
   the episode level and the abstract pattern level simultaneously?

4. What work exists on CBR and Large Language Models — specifically using CBR
   to manage LLM execution (our direction) vs. using LLMs to enhance CBR
   (the common direction)?

5. What formal and semi-formal languages have been proposed as reasoning media?
   What properties do they claim, and how do they compare to NormCode's six
   properties?

6. What is the process mining literature, and how does it relate to distilling
   workflow patterns from execution traces (our Level 2 learning)?

7. What CBR work exists on case base maintenance, competence, and quality —
   relevant to the case base management limitations we discuss?

8. What is the prior work on self-hosting / reflexive systems in AI, and how
   does the self-hosted NormCode compiler relate to meta-learning in CBR?

---

## Category 1: Process-Oriented CBR Foundations (PRIORITY 1 — must cover)

**This is the primary theoretical context for the paper.**

### Core papers to find and read in full:

- **Bergmann (2002)** — "Experience Management: Foundations, Development
  Methodology, and Internet-Based Applications" — the foundational POCBR text;
  find specific chapters on workflow cases and process-oriented retrieval

- **Aamodt & Plaza (1994)** — "Case-Based Reasoning: Foundational Issues,
  Methodological Variations, and System Approaches" — the canonical CBR cycle
  paper; need the exact formulation of Retrieve/Reuse/Revise/Retain

- **Kolodner (1993)** — "Case-Based Reasoning" — foundational textbook; find
  the definition of case integrity and case representation

- **Minor et al. (2014)** — any papers by Mirjam Minor on process-oriented CBR,
  workflow retrieval, and case representation for processes; check ICCBR
  proceedings 2010–2015

- **Klusch et al.** — workflow adaptation and retrieval in POCBR; find specific
  papers on adapting retrieved workflow cases

### Questions to answer from this literature:
- What is the standard definition of a "process case" in POCBR?
- What prior work exists on intermediate state representation within a workflow case?
- How does standard POCBR handle the retrieval of partial workflow states
  (i.e., starting from step $k$ rather than from the beginning)?
- Has POCBR been applied to AI/LLM workflow management before?

---

## Category 2: Multi-Level and Hierarchical CBR (PRIORITY 1 — core theoretical claim)

**NormCode's two-level CBR architecture needs grounding in prior multi-level CBR work.**

### Papers to find:

- **Hierarchical CBR** — any papers on CBR operating at multiple levels of
  abstraction simultaneously (e.g., abstract cases and concrete cases)

- **Case abstraction in CBR** — papers on how concrete cases are generalized
  into abstract cases; Smyth & Keane; Bergmann & Wilke on abstraction hierarchies

- **Meta-CBR** — any papers on CBR systems that reason about their own
  case retrieval or case quality processes

- **Template-based CBR** — cases as parameterized templates (analogous to our
  Level 2 plans as runtime definitions)

### Key question:
Has POCBR literature proposed a two-level structure where (1) workflow episodes
are cases and (2) workflow patterns/templates are abstract cases simultaneously?
If yes: how does NormCode's formalization relate to prior work?
If no: this is a theoretical contribution of the paper.

---

## Category 3: Cases as Runtime States (PRIORITY 1 — novel claim requiring literature support or gap)

**The claim that a Level 1 case IS a NormCode runtime state needs grounding.**

### Papers to find:

- **Checkpoint-based CBR** — any CBR papers that treat checkpoints or
  execution snapshots as cases

- **Anytime algorithms and CBR** — papers on suspending and resuming problem
  solving; is there CBR work on suspended reasoning episodes?

- **State-based case representation** — papers on representing computational
  state as a CBR case (outside of workflow context)

- **Debugging and CBR** — any papers applying CBR to debugging (retrieve a
  past bug episode, adapt the fix); this is related but at a different level

- **Process mining + CBR** — van der Aalst process mining work; any intersection
  with CBR where mined traces become cases

### Key question:
Is there prior CBR work that treats a suspended runtime state (not just
input-output data, but the full execution environment at a moment) as a case?
If not, this is a novel contribution that needs careful framing as such.

---

## Category 4: CBR and Large Language Models (PRIORITY 1 — active research area)

**Must position against the growing CBR+LLM literature — our direction is inverse.**

### Papers to find:

- **CBR for few-shot LLM prompting** — retrieving similar past examples to
  include in LLM prompts; Rubin et al. (2022); Wang et al. (2022); any 2023–2025
  follow-up work

- **CBR for LLM planning** — using retrieved past plans to bootstrap new LLM
  planning; any papers at ICCBR 2023, 2024

- **LLM-enhanced CBR retrieval** — using LLMs to improve case similarity
  measures, case adaptation, or case generation

- **CBR for LLM alignment/evaluation** — using CBR to store and retrieve
  successful vs. failed LLM outputs for alignment

- **ICCBR 2023 and 2024 proceedings** — search for all papers combining CBR
  and LLMs; map the landscape

### Our position (to argue clearly):
All prior CBR+LLM work uses CBR *to improve individual LLM calls* (better
few-shot examples, better prompts). Our contribution is the *inverse and orthogonal*
direction: using a CBR architecture to manage the *execution of multi-step LLM
workflows* — where the "case" is not an example for a single call but a suspended
runtime state of a complete reasoning process.

---

## Category 5: Formal and Semi-Formal Reasoning Languages as Media (PRIORITY 2)

**The "reasoning medium" framing needs literature on other languages that claimed this role.**

### Languages and papers to find:

- **PDDL (Planning Domain Definition Language)** — the standard AI planning
  language; papers on its expressiveness vs. human readability trade-off

- **HTN (Hierarchical Task Networks)** — Erol et al. (1994); find papers on
  HTN planning applied to LLM agents; how does expressiveness compare?

- **BDI (Belief-Desire-Intention)** — agent programming languages (Jason, AgentSpeak);
  any comparison with workflow languages

- **BPEL / BPMN** — business process execution languages; why they failed to
  become a universal reasoning medium (too domain-specific, too formal for
  non-experts)

- **CWL (Common Workflow Language)** — scientific workflow specification;
  find papers on its use and limitations

- **Dataflow programming languages** — LabVIEW, Pure Data, Max/MSP; visual
  dataflow as a reasoning medium

- **Jupyter Notebooks as a reasoning medium** — papers on notebooks as
  executable narratives; Rule et al. (2018) "Ten simple rules for writing and
  sharing computational analyses in Jupyter Notebooks"; Kluyver et al. (2016)

- **Literate programming** — Knuth (1984); the original argument for human-readable
  executable programs; how NormCode extends this to AI reasoning

### Key question:
Which prior languages claimed to be reasoning media, and which of NormCode's
six properties did they fail to satisfy? (Most fail Interpretable for non-experts
or Generalizable for arbitrary domains.)

---

## Category 6: Process Mining and Workflow Distillation (PRIORITY 2)

**Related to Level 2 CBR — distilling abstract cases from execution traces.**

### Papers to find:

- **van der Aalst** — foundational process mining papers; "Process Mining:
  Discovery, Conformance and Enhancement of Business Processes" (2011);
  how do mined process models relate to NormCode plans as abstract cases?

- **Workflow mining from logs** — any papers on extracting workflow templates
  from execution traces; this is the automated version of NormCode's Level 2
  distillation

- **Conformance checking** — verifying that an execution trace conforms to
  a process model; analogous to NormCode's `.ncn` review and compiler verification

- **Process variant analysis** — comparing multiple execution traces of the
  same process; analogous to fork-and-compare in NormCode

### Key question:
Is NormCode's compilation pipeline (Derivation → Formalization → Post-Formalization
→ Activation) doing something analogous to process mining? If yes, how does the
human-authoring + LLM-assisted approach compare to automated trace mining?

---

## Category 7: Case Base Maintenance and Quality (PRIORITY 2)

**For the Discussion section — limitations and future work on case base management.**

### Papers to find:

- **Competence-based case base maintenance** — Smyth & McKenna; papers on
  which cases to keep, which to prune, to maintain retrieval quality

- **Case base quality** — papers on measuring the quality of a case base;
  coverage, correctness, consistency

- **Forgetting in CBR** — papers on intentional case removal vs. retention;
  analogous to our unbounded case base growth limitation

- **Case authoring** — papers on deliberate case creation (vs. accumulation);
  any ICCBR papers on "case authoring" as a skill

---

## Category 8: LLM Workflow Tools (PRIORITY 2 — for Related Work §10)

**Needed to position against the tool landscape — same as before but framed differently.**

The key framing shift: prior tools are not missing CBR as a feature — they are
missing the structural isolation property that would make their checkpoints
reliable cases. Without isolation, no amount of CBR tooling produces reliable
case-based reasoning.

### Tools to cover:

- **LangSmith** — post-hoc tracing (not pre-run verification); checkpoints are
  contaminated (no isolation) → not reliable cases
- **LangFlow / Flowise** — visual authoring but no case management; workflows
  locked in platform; not portable runtime definitions
- **PromptFlow** — DAG-based; implicit data flow → contaminated checkpoints
- **AutoGen / AutoGen Studio** — conversation history as implicit state → worst
  case for checkpoint integrity
- **LangGraph** — graph topology explicit but data flow implicit → partial progress
  toward isolation but not enforced

### New angle needed:
Frame these not as "lacking debugging features" but as "lacking the isolation
property that would make their execution states usable as CBR cases."

---

## Category 9: Self-Hosting, Meta-Learning, and Reflexive Systems (PRIORITY 3)

**For the self-hosting = recursive CBR claim.**

### Papers to find:

- **Self-hosting compilers** — any papers on the significance of self-hosting
  as a validation criterion; the concept in programming language theory

- **Meta-learning in AI** — MAML (Finn et al., 2017); learning to learn;
  how does NormCode's self-hosted compilation relate to meta-learning?

- **Reflexive CBR** — any CBR papers on systems that reason about their own
  case retrieval process or improve their own case base management

- **Self-improving AI systems** — papers on systems that can improve their own
  reasoning capabilities; how does NormCode's recursive structure relate?

---

## Category 10: Human Oversight and Pre-Execution Verification (PRIORITY 2)

**For C2 — the `.ncn` review as a novel human-in-the-loop intervention point.**

### Papers to find:

- **RLHF (Reinforcement Learning from Human Feedback)** — Ouyang et al. (2022)
  "InstructGPT"; operates during training — not pre-execution

- **Constitutional AI** — Bai et al. (2022, Anthropic); operates during
  generation — not pre-execution

- **Red-teaming for LLMs** — any structured pre-deployment evaluation; closest
  to pre-execution review but at the model level, not the plan level

- **Plan verification by humans** — any papers on humans reviewing AI plans
  before execution in high-stakes domains (medical, legal, financial)

- **EU AI Act** — provisions on human oversight, transparency, traceability
  for high-risk AI systems; Articles on technical documentation requirements

- **Scalable oversight** (Bowman et al., 2022; Leike et al.) — oversight
  mechanisms for AI systems; how does `.ncn` review compare?

### Key argument (C2):
The `.ncn` pre-execution review is the only intervention at the *plan structure*
level before any probabilistic computation. All prior human-in-the-loop approaches
operate during or after computation. This is a novel intervention point.

---

## Priority Summary for the ICCBR Paper

| Priority | Category | Why it matters |
|----------|----------|----------------|
| **P1** | POCBR Foundations | Primary theoretical context; all CBR claims rest here |
| **P1** | Multi-level CBR | Novel two-level architecture needs prior art or gap |
| **P1** | Cases as Runtime States | Novel claim; needs prior art or explicit gap statement |
| **P1** | CBR + LLMs | Must position clearly against active research area |
| **P2** | Formal reasoning languages | "Reasoning medium" framing needs language comparison |
| **P2** | Process mining | Level 2 distillation has process mining analogy |
| **P2** | Case base maintenance | Needed for Discussion limitations |
| **P2** | LLM workflow tools | Related Work positioning |
| **P2** | Human oversight | C2 novelty argument |
| **P3** | Self-hosting / meta-learning | Self-hosting = recursive CBR argument |

---

## Citations Already Known (from arXiv:2512.10563 companion paper)

These cover the LLM/agent landscape and some IR work — still useful but now
secondary to the CBR literature above:

| Key | Description | New role in ICCBR paper |
|-----|-------------|------------------------|
| yao2022 | ReAct | Agent framework background |
| shinn2023 | Reflexion | Agent framework background |
| wei2022 | Chain-of-Thought | IR comparison |
| ibm_langgraph | LangGraph | LLM tool landscape |
| wu2023_autogen | AutoGen | LLM tool landscape |
| eu_ai_act | EU AI Act | C2 regulatory motivation |
| ruan2024 | Context isolation | Isolation problem background |
| wu2025 | IsolateGPT | Isolation problem background |
| chang2025 | LLM forgetting | Case integrity motivation |
| bergmann2002 | POCBR (if already cited) | **Primary** — confirm full details |
| aamodt1994 | CBR cycle | **Primary** — confirm exact formulation |

---

## New Citations Needed (not in companion paper)

These are gaps the literature review must fill:

| Gap | What to find | Urgency |
|-----|-------------|---------|
| POCBR workflow case definition | Bergmann 2002; Minor et al. | Critical |
| CBR cycle canonical source | Aamodt & Plaza 1994; Kolodner 1993 | Critical |
| Multi-level CBR | Search ICCBR proceedings | Critical |
| Runtime state as case | Search — may be a gap | Critical |
| CBR + LLM (our inverse direction) | ICCBR 2023, 2024; recent arXiv | High |
| Process mining analogy | van der Aalst | Medium |
| Case base maintenance | Smyth & McKenna | Medium |
| PDDL vs. NormCode | Classical planning papers | Medium |
| Literate programming | Knuth 1984 | Low |
| Self-hosting significance | PL theory papers | Low |

---

## Output Format Requested

For each paper found, provide:

1. **Full citation** (authors, title, venue, year, DOI/arXiv)
2. **2-sentence summary** of what it claims
3. **Relation to NormCode thesis**: Does it support, challenge, or provide
   prior art for the two-level CBR / reasoning medium argument?
4. **Gap or agreement**: Does NormCode extend, contradict, or fill a gap left
   by this paper?
5. **BibTeX entry**

For the CBR literature specifically, also provide:
- The paper's definition of "case" — is it data, a process, a state, a template?
- Whether the paper addresses multi-level case structures
- Whether the paper addresses the isolation/integrity of cases

Additionally provide:
- A **POCBR landscape table**: Prior POCBR systems × case representation type ×
  retrieval method × adaptation method × domain
- A **CBR+LLM landscape table**: Prior CBR+LLM papers × direction (CBR→LLM or
  LLM→CBR) × what "case" means × relation to NormCode's approach
