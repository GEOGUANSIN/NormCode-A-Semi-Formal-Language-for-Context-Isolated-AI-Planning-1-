# ICCBR 2026 Paper — Plan

**Title:** A Working Language for Human-Interpretable AI Workflow Orchestration: NormCode and the Case-Based Lifecycle

**Alternative titles (to choose from):**
- "NormCode: An Interpretable Planning Language for Enforceable, Case-Based AI Workflow Orchestration"
- "From Language to Lifecycle: Interpretable AI Workflow Planning with Case-Based Execution Management"

**Venue:** International Conference on Case-Based Reasoning (ICCBR 2026)
**Location:** University of Bremen, Germany, August 13–16, 2026
**Submission deadline:** March 20, 2026
**Submission category:** Deployed Applications
**Format:** Springer LNCS — 14 pages + 2 pages (refs/acknowledgments/AI statement)
**Review:** Double-blind (cite companion paper as [Anon. 2025])

**Companion paper:** [Anon. 2025] — the formal NormCode language specification: grammar,
symbol set, type system, scope rule, and compilation theory. Canvas App and compiler
appear there briefly (~400 words, one of six contributions). That paper answers *what
NormCode is*. This paper answers *what NormCode makes possible*: the Canvas App and
compiler together realize a full two-level CBR system, with concrete case definitions,
the four CBR operations mapped to deployed UI interactions, the compiler as a Level 2
distillation process, and C1/C2/C3 demonstrated in production. The CBR framing and
empirical evaluation are explicitly deferred to future work in the companion paper.

---

## Core Argument (updated)

### The Gap No One Names

Every AI deployment stack has three layers that practitioners understand: the
model layer (raw LLMs), the framework layer (LangChain, AutoGen), and the
interface layer (web apps, APIs). What is systematically missing is a **reasoning
medium** — a shared, interpretable language between human intent and machine
execution in which reasoning plans can be authored, verified, executed, and
accumulated as experience.

SQL filled this role for databases: not as a tool applied to data, but as the
medium in which questions about data are formulated, reviewed, and answered.
You learn it once; it expresses any query; the statement is a portable artifact
that can be read by a developer, reviewed by a manager, audited by a regulator,
and re-executed years later on a different engine. The power of SQL is not its
syntax — it is that it is a *medium*: a shared representational system that lets
humans and machines reason about data together.

AI orchestration lacks this medium. Without it, reasoning plans are either locked
inside code (opaque to non-developers), locked inside no-code platforms
(unscalable, proprietary), or left implicit in the prompt engineering conventions
of individual practitioners (unrepeatable, unverifiable). There is no shared form
in which a designer, operator, compliance officer, and orchestration engine can
all engage with the same reasoning plan at the level appropriate to their role.

### NormCode as a Reasoning Medium

NormCode is not a workflow tool. It is a **medium of reasoning** — a
representational language in which multi-step AI reasoning plans are formulated
with the same precision that mathematics formulates scientific arguments or SQL
formulates database queries.

A reasoning medium has a specific relationship to its subject: it does not
describe reasoning from the outside, it IS the structure of reasoning, made
legible. When you write a NormCode plan, you are not specifying how a system
should behave — you are articulating a reasoning episode: what is known (input
concepts), what is derived and how (inference steps), what is produced (output
concepts), and how derivations depend on each other (scope structure). The plan
is the reasoning, expressed in a form that is simultaneously human-readable and
machine-executable.

This is a substantively different claim from "NormCode is a planning DSL." A
planning DSL maps user intent to machine instructions. A reasoning medium
externalizes the structure of reasoning itself into a form that can be inspected,
verified, shared, corrected, and accumulated as experience — by humans and
machines alike.

A working reasoning medium for AI orchestration must have six properties:

1. **Interpretable** — humans at multiple roles can read, author, and verify it
   without programming expertise. The syntax reads like structured natural
   language; the compiled `.ncn` output reads like plain prose. The medium
   is legible at every level of the stack.

2. **Enforceable** — what humans review is exactly what executes. The compiler
   verifies the structure before any run; the orchestrator enforces it at runtime.
   A reasoning plan that passes review cannot behave differently than the review
   described. The medium has teeth.

3. **Composable** — a small set of primitives (three symbols, one scope rule)
   combine into arbitrarily complex reasoning workflows: nested loops,
   conditionals, parallel derivation, multi-agent coordination. The rules of
   composition never change as complexity grows. The medium does not break at scale.

4. **Locally Addressable** — any reasoning step can be isolated and worked on
   independently. Flow indices give every node a precise address; the scope rule
   makes every step epistemically self-contained. A developer can debug step
   `1.3.2`, a compliance officer can review just the output of step `1.1`, and
   the orchestrator can re-run only downstream-stale steps after a correction —
   all without touching the rest of the plan. The medium scales to human attention
   by making local reasoning work structurally safe.

5. **Generalizable** — the primitives are domain-agnostic. The same three symbols
   express a PPT generation plan, a code review pipeline, a BOM matching task, a
   scientific data analysis, or a medical treatment pathway. The medium can
   represent any multi-step reasoning task without domain-specific extensions.

6. **Portable** — the reasoning plan is a plain text artifact: version-controlled,
   shareable, executable by any compliant orchestrator, independent of any
   specific LLM or deployment platform. The medium belongs to its authors.

### NormCode Realizes CBR at Two Levels

Here is the central claim of this paper: **when a reasoning medium has these six
properties, Case-Based Reasoning is not applied to it — it is realized by it,
at two distinct levels simultaneously.**

#### Level 1 — Concrete Case Management (within a plan)

**A Level 1 case IS a NormCode runtime state** — not a data record about a past
run, but a suspended execution environment: the full Blackboard (which nodes
completed, in-progress, pending, skipped), the full Concept Repository (all
tensors for all completed nodes), and the derivable Waitlist (what remains to
execute). A checkpoint captures this entire runtime state and persists it.

This is what makes CBR in NormCode literal rather than metaphorical:

- **Retrieve** = locate a suspended runtime in the case base by (run_id,
  flow_index); inspect its Concept Repository via the Tensor Inspector to verify
  it is the right state to continue from.
- **Reuse (Fork)** = reinstantiate that suspended runtime as a new execution;
  the orchestrator loads the stored Blackboard and Concept Repository and resumes
  from there. You are not loading data into a fresh system — you are continuing
  a specific runtime that was paused.
- **Revise** = modify the runtime state before resuming: override a tensor in
  the Concept Repository, mark downstream nodes stale in the Blackboard, and
  resume. The scope rule guarantees the stale boundary is exact.
- **Retain** = the resumed runtime deposits new Blackboard/Concept Repository
  snapshots at every completed node — new suspended runtimes added to the case base.

The scope rule is what makes these operations reliable: because each step's
tensor is epistemically clean (contains exactly what that step used, nothing
more), reinstantiating from any checkpoint produces the same data-dependency
behavior as the original execution. The runtime is resumable because it was
isolated in the first place.

#### Level 2 — Abstract Case Learning (across plans)

Across many runs of similar tasks, patterns emerge. Those patterns can be
distilled into a NormCode plan — and this is where the deeper CBR insight lives.

**A Level 2 case IS a NormCode runtime definition** — the plan (Inference
Repository + Concept Repository schema) that specifies what runtimes of this type
are possible. Where a Level 1 case is a suspended runtime (a specific execution
paused at a point), a Level 2 case is a generative template: every run instantiates
a new runtime from the same definition. The plan records not what happened in one
episode, but the structure of what works across all similar episodes — the concepts
that matter, the inference steps and their dependencies, the derivation operations.

When a new problem arrives that fits a known class, the practitioner retrieves the
matching NormCode plan (the abstract case), instantiates it with new inputs, and
runs it. This is Reuse at the plan level. When the plan needs adjustment for the
specific problem, the designer modifies the `.ncds` file and recompiles — Revise
at the plan level. The revised plan is retained for future similar problems.

The six production plans (PPT generation, Code Assistant, BOM Matching, etc.) are
not just demonstrated workflows. They are **a case library of abstract reasoning
patterns** for AI orchestration tasks — each encoding what structure of reasoning
reliably solves a class of problem.

#### The Connection: The Distillation Process is Itself a NormCode Plan

The most striking consequence of NormCode as a reasoning medium is this: **the
process of distilling experience into abstract cases (Level 2) is itself expressible
as a NormCode plan.**

Going from natural language task descriptions and observed patterns to a compiled,
executable NormCode plan is a reasoning process: identify the concepts involved,
extract their dependencies, formalize the inference structure, assign execution
types and paradigms, generate the executable repositories. This is the NormCode
compilation pipeline (Derivation → Formalization → Post-Formalization →
Activation). And the compilation pipeline is itself a NormCode plan — demonstrated
by the self-hosted compilation case study, where NormCode compiles itself.

This self-similarity means NormCode supports **general case-based learning**:
- Concrete experiences (runs) accumulate as Level 1 cases.
- Patterns across those experiences are distilled into Level 2 cases (plans) via
  the compilation pipeline.
- The compilation pipeline is itself a Level 2 case — a reusable reasoning pattern
  for the task of "turn a described workflow into an executable NormCode plan."
- Improvements to the compilation pipeline refine the abstract case for
  "how to build abstract cases" — and can be tested by re-running the self-hosted
  compilation (recursive validation).

This recursive structure — where the medium can reason about how to improve its
own case abstraction process — is what distinguishes NormCode from a planning DSL.
A DSL executes instructions. A reasoning medium can improve its own instructions.

The Canvas App makes both levels accessible: Graph View and Tensor Inspector
for Level 1 (concrete case inspection and correction); the compilation workflow
and plan modification tools for Level 2 (abstract case refinement).

### The Three Measurable Properties (C1, C2, C3)

This paper demonstrates three measurable properties that follow from having a
genuine reasoning medium — properties absent from existing LLM workflow tools:

**(C1) Exact reasoning step inspection in O(1) operations.** Because every step's
inputs are explicitly declared and stored at its flow index, "what did step $k$
reason from?" is answered by opening the Tensor Inspector — not by reconstructing
accumulated logs. The reasoning medium makes each step's epistemic state
permanently available.

**(C2) Zero-cost pre-execution review of the full reasoning plan.** The compiler's
Formalization phase produces a `.ncn` file — a plain-English narrative of the
entire reasoning plan — available before any LLM call is made. A domain expert
can read this narrative, verify that the reasoning structure matches intent, and
reject the plan before any probabilistic computation begins.

**(C3) Scope-bounded correction without re-reasoning from scratch.** When a
reasoning step is corrected (its output tensor overridden), the scope rule
determines exactly which downstream steps logically depend on it. Only those steps
re-execute. The medium's structure makes correction efficient by construction.

### Why This Is the Right Paper for ICCBR

CBR is a theory of how reasoning systems learn from experience. This paper argues
that the quality of that learning depends critically on the quality of the medium
in which reasoning is expressed. NormCode is a concrete instantiation of what a
high-quality reasoning medium looks like for AI orchestration — and the Canvas
App is the evidence that such a medium, deployed in production, realizes CBR
natively across its full lifecycle.

ICCBR topics addressed: "Case representation" (NormCode plans as reasoning medium);
"Case authoring, elicitation, and visualization" (Canvas App); "Workflow management
and process-oriented CBR" (direct); "CBR architectures and frameworks" (the
emergent CBR lifecycle); "CBR and Large Language Models" (the specific domain).

---

## Section Structure (14 pages)

| Section | Title | Angle | Pages |
|---------|-------|-------|-------|
| Abstract | — | Reasoning medium → two-level CBR → three measurable properties | 0.25 |
| 1 | Introduction | The missing reasoning medium; six properties; two-level CBR; C1/C2/C3 | 1.5 |
| 2 | Background | POCBR; two-level case structures in CBR; the case integrity requirement | 1.0 |
| 3 | NormCode as a Reasoning Medium | Six properties realized; syntax; scope rule; `.ncn`; semantic/syntactic | 1.5 |
| 4 | CBR Level 1: Concrete Case Management | Cases = checkpoints; case base = SQLite; Retrieve/Reuse/Revise/Retain in Canvas | 1.5 |
| 5 | CBR Level 2: Abstract Case Learning | Plans = abstract cases; compilation = distillation; self-hosting = general case learning | 1.5 |
| 6 | The Canvas App | The interface for both CBR levels; Graph View, Tensor Inspector, Override, Fork, compilation workflow | 1.25 |
| 7 | Case Studies | PPT Agent (Level 2 plan-as-case reuse + Level 1 checkpoint retrieval); Code Assistant (retrieve–revise cycle) | 1.75 |
| 8 | Evaluation | 100% accuracy; self-hosted compilation as Level 2 CBR validation; six production plans | 1.0 |
| 9 | Discussion | Language as the substrate; recursive self-improvement; what CBR gains; limitations | 0.75 |
| 10 | Related Work | POCBR; multi-level CBR; CBR + LLMs; LLM workflow tools; formal reasoning languages | 0.75 |
| 11 | Conclusion | Two-level CBR from a reasoning medium; the path forward | 0.25 |

---

## Section-by-Section Notes

### Abstract
- Open with the language gap, not with "LLM workflows fail"
- State the four properties of a working language in one sentence
- Name C1, C2, C3 explicitly
- CBR cycle emerges from these properties when execution state accumulates
- Deployed evidence: six plans, 100% accuracy, self-hosted compilation

### §1 Introduction
- **Hook:** LLM frameworks (LangChain, LangGraph, AutoGen, PromptFlow) made multi-step
  workflows easy to build but left a structural problem: implicit shared state makes
  checkpoints unreliable, failures unlocalizable, experience non-accumulating
- **The missing piece:** a reasoning medium — what SQL is for databases
- **NormCode:** the reasoning medium; six properties; scope rule as the mechanism
- **Two-level CBR emerges:** Level 1 (suspended runtimes as cases), Level 2 (plans as
  abstract cases, compiler as distillation, self-hosting as recursive learning)
- **C1, C2, C3:** three measurable properties that follow structurally
- **Relation to companion paper [Anon. 2025]:** companion = language spec (grammar,
  type system, scope rule); this paper = what Canvas + compiler make possible as a
  CBR system; companion explicitly defers CBR framing and empirical work here
- **Double-blind:** self-cite companion as [Anon. 2025]; do not link to arXiv in body
- **Framework citations:** Chase 2022 (LangChain), Langgraph 2024, Wu et al. 2023
  (AutoGen), Microsoft 2023 (PromptFlow)
- **C2 citations:** Ouyang et al. 2022 (RLHF/InstructGPT), Bai et al. 2022
  (Constitutional AI)

### §2 Background
- POCBR: cases as processes, the CBR cycle
- What makes a workflow case reliable (case integrity, §2.3)
- Why current tools don't produce reliable cases (no structural isolation)
- The enabling condition: isolation as a language property, not a tooling feature

### §3 NormCode as a Working Language
- **3.1 The six properties realized** — show how each property is implemented:
  - Interpretable: three symbols + `.ncn` plain-prose output
  - Enforceable: compiler verification + runtime enforcement
  - Composable: Imperative / Judgement / Grouping / Timing / Looping — same rules at any depth
  - Locally Addressable: flow indices as precise step addresses; scope rule makes each step self-contained; re-run only stale downstream steps
  - Generalizable: same primitives for PPT generation, code review, BOM matching, scientific workflows
  - Portable: `.ncds` text file, `concept_repo.json` + `inference_repo.json`
- **3.2 Syntax and scope** — annotated example, flow indices
- **3.3 Semantic vs. syntactic** — the cost visibility this enables
- **3.4 The `.ncn` as interpretability artifact** — what it enables (C2 foundation)

### §4 CBR Level 1: Concrete Case Management
- **The operational CBR contribution** — what the system does on every run
- **4.1 A case is a NormCode runtime state** — define precisely: (Blackboard snapshot, Concept Repository snapshot, run_id, flow_index); persisted in SQLite; the full suspended execution, not just one tensor
- **4.2 The case base** — collection of suspended runtimes; grows automatically on every completed node
- **4.3 Retrieve** — locate a suspended runtime by (run_id, flow_index); inspect Concept Repository tensors via Tensor Inspector; verify before reinstantiation
- **4.4 Reuse (Fork)** — reinstantiate the suspended runtime as a new execution (new run_id); orchestrator loads stored Blackboard + Concept Repository; no upstream re-execution
- **4.5 Revise** — override a tensor in the Concept Repository; Blackboard marks downstream nodes stale; resume propagates only through stale boundary (C3); scope rule guarantees boundary is exact
- **4.6 Retain** — every completed node in resumed/revised execution deposits a new suspended runtime into the case base

### §5 CBR Level 2: Abstract Case Learning
- **The theoretical CBR contribution** — what NormCode adds to CBR methodology
- **5.1 A plan is a NormCode runtime definition** — define precisely: the Inference Repository (inference graph, sequence types, paradigm assignments) + Concept Repository schema; specifies what runtimes of this type are possible; every run is an instance
- **5.2 The six-plan case library** — six runtime definitions (PPT generation, Code Assistant, BOM Matching, etc.); retrieve the matching definition for a new problem class, instantiate (run), get concrete cases
- **5.3 Plan modification as abstract case revision** — `.ncds` edits + recompilation = new runtime definition; `.ncn` re-review = verifying the abstract case before it generates concrete cases; retain = the revised plan replaces or extends the library
- **5.4 Compilation as distillation** — Derivation → Formalization → Post-Formalization → Activation = the process of turning natural language descriptions into runtime definitions (abstract cases); each phase extracts and formalizes structure
- **5.5 Self-hosting = recursive case-based learning** — the compilation pipeline is itself a runtime definition (a NormCode plan); running it = Level 1 CBR instantiating a Level 2 abstraction process; improving the compiler = revising the abstract case for "how to build abstract cases"

### §6 The Canvas App: Interface for Both Levels
- One environment; both CBR levels accessible
- **Level 1 interface**: Graph View (case structure visible before execution); Tensor Inspector (case content inspection); Override + Fork (revision and reuse)
- **Level 2 interface**: `.ncn` review panel (abstract case verification before it generates concrete cases); compilation workflow visibility; plan modification tools
- **6.1 Architecture** — React 18 + FastAPI + SQLite + WebSockets
- **Key claim**: an operator who cannot read `.ncds` syntax can fully participate in Level 1 CBR; a designer who uses the compilation workflow participates in Level 2

### §6 Case Studies
- **6.1 PPT Agent** — case library growth; plan-as-meta-case reuse across topics
- **6.2 Code Assistant** — full retrieve–revise cycle: breakpoint, inspect, override, fork-compare

### §7 Evaluation
- Correctness (base-X addition 100%, self-hosted compilation)
- Scale (six production plans, 15–40 inferences each, 60–70% syntactic)
- C1 evidence: failure localization time in practice
- C2 evidence: `.ncn` review step in the production workflow
- C3 evidence: override-and-resume re-execution count in Code Assistant debugging

### §8 Discussion
- **Language as the enabler** — the six properties are not features; they are what makes C1–C3 structurally possible
- **Sustainable improvement** — how the system gets better over time: plans are refined, case base grows, operators learn from fork-compare cycles
- **What CBR gains** — a language substrate that guarantees case integrity; learned similarity as future work; case base maintenance policies
- **Limitations** — derivation is LLM-assisted; semantic cases are bounded-stochastic; case base grows without maintenance
- **The broader thesis** — other domains where an interpretable, enforceable language would unlock CBR: scientific workflow management, legal document processing, medical treatment planning

### §9 Related Work
- POCBR foundations [Bergmann, Minor, Aamodt & Plaza]
- CBR and LLMs [few-shot retrieval; our contribution is the inverse direction]
- Formal workflow languages [BPEL, YAML-based orchestration — none have the interpretability + enforceability combination]
- LLM workflow tools [LangSmith, LangFlow, PromptFlow, AutoGen — post-hoc tracing vs. structural guarantees]
- Explainable AI and auditability [EU AI Act; XAI approaches — NormCode provides the substrate]

### §10 Conclusion
- A working language is the missing layer in the AI orchestration stack
- NormCode provides that language; the Canvas App makes it accessible; the CBR lifecycle emerges
- C1, C2, C3 are evidence that the working language thesis holds
- Future: learned similarity for fork selection; case base maintenance; cross-domain applications

---

## What Makes This Paper Different from arXiv:2512.10563

| Dimension | arXiv (language paper) | This paper (ICCBR) |
|-----------|------------------------|---------------------|
| Central subject | The NormCode language (grammar, type system, compiler theory) | The working language thesis and its CBR consequences |
| Canvas coverage | ~400 words, one subsection | Central artifact of the paper |
| CBR | Not mentioned | Core framing — CBR emerges from the language |
| Evaluation | Base-X addition, self-hosted compilation (language correctness) | C1, C2, C3 demonstrations (lifecycle properties) |
| Interpretability | Language property | Key claim with evidence |
| Sustainable improvement | Not addressed | Core consequence of the working language |
| Audience | Language researchers, formal methods | CBR community, workflow management, AI practitioners |

---

## Files

```
iccbr_paper/
├── plan.md                    ← this file (updated)
├── cbr.md                     ← ICCBR 2026 CFP (reference)
├── article/
│   ├── abstract.md            ← to rewrite with language-first framing
│   ├── 01_introduction.md     ← to rewrite with SQL analogy + four properties
│   ├── 02_background.md       ← POCBR + case integrity (mostly done)
│   ├── 03_normcode.md         ← rewrite as "four properties realized"
│   ├── 04_cbr_architecture.md ← rewrite as "emergent CBR lifecycle"
│   ├── 05_canvas.md           ← add .ncn review panel as C2 interface
│   ├── 06_case_studies.md     ← done (mostly)
│   ├── 07_evaluation.md       ← add C1/C2/C3 evidence columns
│   ├── 08_discussion.md       ← add sustainable improvement + broader thesis
│   ├── 09_related_work.md     ← add formal workflow languages subsection
│   └── 10_conclusion.md       ← rewrite with working language thesis
├── appendix/
└── figures/
    ├── fig1_canvas_cbr.png     ← Canvas with CBR cycle labels
    ├── fig2_language_stack.png ← the missing language layer diagram
    └── fig3_retrieve_revise.png← fork + override workflow
```

---

## Submission Notes

- Category: **Deployed Applications**
- Submit via EasyChair: https://easychair.org/conferences/?conf=iccbr26
- If simultaneously under review elsewhere: add footnote on p.1 and email chairs@iccbr.org
- LNCS template: https://overleaf.com/read/kxtrhfvdzjdr#c03410
- At least one author must register by May 20, 2026 and present in person
- Deadline: **March 20, 2026** — 9 days from today
