# Literature Review Plan — NormCode Demo Paper

**Purpose:** This document is a research brief for a deep-research AI to gather relevant literature, papers, and technology comparisons as background for a six-page system demonstration paper on **NormCode Canvas** — a visual execution and debugging environment for AI agent workflows.

**Paper summary:** NormCode is a semi-formal language for AI agent planning that enforces explicit data isolation between steps. The Canvas App (v1.1.3) is a visual IDE for authoring, executing, debugging, and modifying NormCode plans. The demo paper argues NormCode fills a gap in the three-tool landscape (raw LLMs / code frameworks / no-code UIs) by providing a working language that is portable, debuggable, and auditable by construction.

**Companion paper already published:** arXiv:2512.10563 — "NormCode: A Semi-Formal Language for Context-Isolated AI Planning"

---

## Research Questions to Answer

The literature review should help answer these questions for the paper's related work and framing:

1. What visual/graphical tools exist for building, monitoring, and debugging LLM agent workflows, and what are their key limitations?
2. What agent orchestration frameworks are dominant, and how do they approach data flow transparency?
3. What research exists on the problem of context pollution / context accumulation in multi-step LLM workflows?
4. What work exists on auditability, traceability, and explainability specifically for LLM-based systems?
5. What intermediate representation (IR) approaches have been applied to LLM planning or code generation?
6. What semi-formal and workflow languages are relevant comparisons?
7. What human-in-the-loop or human-AI collaboration systems are most comparable?

---

## Category 1: Visual and Graphical Tools for LLM Workflows

**These are the primary competitors for the related work section.**

### Tools to research:
- **LangFlow** — visual drag-and-drop builder for LangChain; find any papers or technical reports
- **LangSmith** — tracing, evaluation, and debugging for LangChain/LangGraph; find papers or system descriptions
- **PromptFlow (Microsoft Azure)** — DAG-based LLM workflow tool; any associated papers (look for Microsoft Research publications)
- **Flowise** — open-source no-code LLM app builder; find any technical writeups
- **Haystack Visual Pipeline** — Deepset's pipeline visualization
- **Vertex AI Pipelines / Google Cloud AI** — enterprise ML pipeline visualization
- **Weights & Biases (W&B)** — experiment tracking with some LLM workflow support
- **MLflow** — experiment tracking and model registry; LLM tracing features added 2023-2024
- **Helicone, Langfuse, Braintrust** — LLM observability tools (newer generation)
- **Dify, Coze** — no-code agent builders with visual workflow; any papers or technical reports
- **AutoGen Studio** — Microsoft's visual multi-agent framework; find associated papers

### Key comparison dimensions to find literature on:
- Data flow transparency (explicit vs. implicit)
- Debugging capabilities (breakpoints, state inspection)
- Portability of workflow artifacts (vendor lock-in)
- Support for non-programmer stakeholders

---

## Category 2: Agent Frameworks and Orchestration

**Background on the agent framework landscape — what NormCode positions against.**

### Frameworks to research (find original papers):
- **ReAct** (Yao et al., 2022) — "ReAct: Synergizing Reasoning and Acting in Language Models" — *already known, find citation*
- **Reflexion** (Shinn et al., 2023) — self-evaluating agents with linguistic feedback memory
- **LangChain** — find any associated technical papers or system descriptions (Harrison Chase et al.)
- **LangGraph** — graph-based extension of LangChain; IBM blog or Microsoft papers on it
- **AutoGPT** — find technical reports and evaluation papers
- **AutoGen** (Wu et al., 2023 — Microsoft Research) — "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
- **CrewAI** — role-based multi-agent framework; find any papers
- **MetaGPT** (Hong et al., 2023) — "MetaGPT: Meta Programming for Multi-Agent Collaborative Framework"
- **HuggingGPT / Jarvis** (Shen et al., 2023) — using ChatGPT to plan and call Hugging Face models
- **Voyager** (Wang et al., 2023) — lifelong learning agent in Minecraft with skill library
- **CAMEL** (Li et al., 2023) — communicative agents for role-playing
- **AgentBench** (Liu et al., 2023) — benchmarking LLM agents across environments

### Key questions:
- How do these frameworks handle data flow between steps? (implicit context vs. explicit passing)
- What debugging/inspection capabilities do they provide?
- Do any of them enforce data isolation by construction?

---

## Category 3: Context Pollution and Long-Context LLM Degradation

**The core technical problem NormCode solves.**

### Search terms:
- "lost in the middle" LLM long context (Liu et al., 2023 — known paper, find citation)
- "context length" LLM performance degradation
- "hallucination multi-step reasoning" LLMs
- "compounding errors" LLM chains
- "context accumulation" LLM agents
- "memory management" LLM agents
- "forgetting" LLMs long conversations

### Papers to find:
- Liu et al. (2023) — "Lost in the Middle: How Language Models Use Long Contexts"
- Any papers on error propagation in multi-step LLM chains
- Papers on LLM performance vs. context length (Anthropic, OpenAI, Google research)
- **IsolateGPT** or similar work on sandboxing LLM applications (cited in companion paper as wu2025)

---

## Category 4: Auditability, Explainability, and Transparency for AI

**The regulatory and compliance framing.**

### Topics and papers to find:
- **EU AI Act** — official text or summary papers; provisions on traceability/auditability for high-risk AI systems
- **XAI (Explainable AI)** — general survey papers, especially for sequential/agentic systems
- LIME (Ribeiro et al., 2016) and SHAP (Lundberg & Lee, 2017) — classic XAI; not directly comparable but establish the field
- Papers on **audit trails for algorithmic decision-making** — especially in legal, medical, financial domains
- **Algorithmic accountability** — research on making ML systems auditable
- Papers on **traceability in AI pipelines** — MLOps perspective
- Any papers specifically on auditability of LLM-based reasoning chains
- "Decision traceability" in regulated domains

### Key question:
- What is the state of the art for making multi-step LLM reasoning auditable, and how does NormCode's approach (structural isolation) compare to post-hoc logging approaches?

---

## Category 5: Intermediate Representations for LLM Planning

**The IR heritage — NormCode as an IR for AI planning.**

### Papers and concepts to find:
- **LLVM IR** — original paper or key descriptions (for context on what a good IR does)
- **Chain-of-Thought** (Wei et al., 2022) — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- **Tree-of-Thought** (Yao et al., 2023) — "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
- **Graph-of-Thought** (Han et al., 2023 or Besta et al., 2023) — graph-structured reasoning
- **Skeleton-of-Thought** — parallel generation technique
- **Program-of-Thought** (Chen et al., 2022) — generating code as intermediate reasoning steps
- **Blueprint First** approaches — structured decomposition before generation
- **Abstractions-of-Thought** — any papers on abstract intermediate representations for LLM reasoning
- Papers on **structured output for LLMs** (JSON mode, function calling as IR)
- **PDDL and HTN planning** applied to LLM agents — any recent papers combining classical planning with LLMs
- Papers on **program synthesis** as IR for reasoning

### Key question:
- How does NormCode's IR (explicit data flow + semi-formal syntax) compare to purely natural language IRs (CoT, ToT) and fully formal IRs (PDDL, code)?

---

## Category 6: Semi-Formal Languages and Workflow Specifications

**The language design heritage.**

### Languages and papers to find:
- **BPMN** (Business Process Model and Notation) — used for workflow specification; ISO standard
- **BPEL** (Business Process Execution Language) — executable workflow language
- **UML Activity Diagrams** — semi-formal modeling
- **CPN** (Colored Petri Nets) — formal workflow modeling
- Papers on **semi-formal specification languages** in requirements engineering
- **Deontic logic** papers — the normative reasoning tradition NormCode's name references
- Papers on **workflow languages for scientific computing** (CWL, Nextflow, Snakemake) — different domain but relevant comparison

### Key question:
- What properties distinguish semi-formal languages from fully formal ones, and why does the semi-formal approach work better for LLM-generated plans?

---

## Category 7: Human-in-the-Loop and Human-AI Collaboration

**The human oversight angle — operators reviewing and modifying plans.**

### Papers to find:
- **Mixed-initiative systems** — early work on human-AI collaboration in planning
- Papers on **human-in-the-loop ML** — general survey
- Papers on **interactive machine learning** where humans can inspect and correct
- **Wizard of Oz** studies for AI workflow design
- Papers on **non-programmer interaction with AI systems** — lowering barriers for domain experts
- Any work on **plan verification** — domain experts approving AI plans before execution
- Papers on **breakpoint debugging** paradigms — from software engineering applied to AI

---

## Category 8: Debugging Tools in Software Engineering (for analogy)

**The software engineering debugging tradition that Canvas App extends to AI.**

### Concepts to find papers on:
- History of **interactive debuggers** — GDB, pdb, visual debuggers
- **Program slicing** — only re-running affected parts after a change (analogous to selective re-run)
- **Omniscient debugging** / **time-travel debugging** — inspect any past state (analogous to checkpoint/fork)
- **Dataflow debugging** — inspecting data at each program point
- Visual debuggers for **dataflow programming** (LabVIEW, Node-RED, Pure Data) — visual precedents

---

## Already-Known Citations (from companion paper arXiv:2512.10563)

These are already in the main paper's bibliography — verify the full citations and add any newer follow-up work:

| Short key | Description |
|-----------|-------------|
| yao2022 | ReAct paper |
| shinn2023 | Reflexion paper |
| wei2022 | Chain-of-Thought paper |
| yao2023 | Tree-of-Thought paper |
| han2023 | Graph-of-Thought paper |
| erol1994 | HTN planning |
| ibm2025 | LangChain/agent framework overview |
| ibm_langgraph | LangGraph description |
| wang2024 | Agent framework paper |
| patel2025 | "Debugging in the dark" practitioners note |
| ruan2024 | Context isolation / sub-agent isolation |
| wu2025 | IsolateGPT / execution isolation |
| sai2025 | Financial explainability regulations |
| chang2025 | LLM forgetting in long conversations |
| saga2025 | LLM contradictions on lengthy tasks |
| wand2025 | Compounding errors in multi-step reasoning |
| breunig2025 | Long context window degradation |
| silva_dl | Semi-formal languages in requirements engineering |
| stanford_deontic | Deontic logic (Stanford Encyclopedia) |
| sordoni2025 | LLM normative constraint consistency |
| delorenzo2025 | Abstractions-of-Thought paper |
| qiu2025 | Blueprint First approach |
| wiki_ir | Intermediate representation (Wikipedia or seminal reference) |

---

## Priority Ranking for the Demo Paper's Related Work

The related work section is ~0.5 pages. Prioritize finding detailed information on:

**Priority 1 (must cover):**
- LangFlow, LangSmith, PromptFlow — direct visual tool competitors
- AutoGen (Microsoft) — most prominent multi-agent framework with some visual support
- ReAct, LangGraph — standard agent architecture references

**Priority 2 (should cover):**
- MetaGPT, CrewAI — multi-agent frameworks
- "Lost in the Middle" (long context degradation) — technical motivation for data isolation
- EU AI Act — regulatory motivation

**Priority 3 (background context):**
- Chain-of-Thought, Tree-of-Thought — IR lineage
- HTN planning — classical planning lineage
- Semi-formal languages / BPMN — language design lineage

---

## Output Format Requested from Deep Research AI

For each relevant paper or technology found, please provide:

1. **Full citation** (authors, title, venue, year, DOI/URL)
2. **2-sentence summary** of what it does
3. **Key limitation** — what does NormCode/Canvas do that this doesn't?
4. **Relevance** — which section of the demo paper it belongs in (Related Work, Introduction framing, or technical background)
5. **BibTeX entry** if available

Additionally, please provide:
- A **comparison table** of visual LLM workflow tools (LangFlow, LangSmith, PromptFlow, Flowise, AutoGen Studio) across: data flow transparency / debugging depth / artifact portability / non-programmer access
- A **timeline** of key agent framework papers (2022–2025) showing the progression toward more structured/visual approaches
