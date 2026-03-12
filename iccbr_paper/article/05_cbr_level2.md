# 5. CBR Level 2: Abstract Case Learning

Level 1 CBR (§4) operates *within* a plan: each execution produces concrete cases
(suspended runtimes) that accumulate in the case base. Level 2 CBR operates *across*
plans: it treats the plans themselves as cases — abstract reasoning patterns that encode
what structure of reasoning reliably solves a class of problem. This section formalizes
the Level 2 architecture, the compilation pipeline as a distillation process, and the
self-hosted compiler as recursive case-based learning.

## 5.1 What a Level 2 Case Is

A Level 2 case is not a suspended execution. It is a **NormCode runtime definition** —
the compiled plan that specifies what all executions of this type are possible.

**Definition.** A *Level 2 case* $P$ is a pair:

$$P = (\mathcal{IR},\; \mathcal{CR}_{\text{schema}})$$

where:
- $\mathcal{IR}$ is the **Inference Repository**: the complete inference graph for this
  plan — all concept-inference relationships, flow indices, sequence types (Imperative,
  Judgement, Grouping, Timing, Looping), paradigm assignments, and agent mappings.
- $\mathcal{CR}_{\text{schema}}$ is the **Concept Repository schema**: the declared
  tensor axes and shapes for every concept in the plan — the structural signature that
  every runtime of this type must satisfy.

Every Level 1 run is an *instance* of the Level 2 case that defines it: it instantiates
$\mathcal{IR}$ with specific input values and generates a Concept Repository $\mathcal{C}$
that conforms to $\mathcal{CR}_{\text{schema}}$. The Level 2 case records not what
happened in one episode, but the structure of what works across all similar episodes.

**The case library.** Four production-ready plans — PPT Generation, Code Assistant, NC
Compilations, Canvas Assistant — are Level 2 cases: an initial case library of abstract
reasoning patterns for AI orchestration tasks. Each encodes a reusable workflow
structure that has been validated in production.

## 5.2 The Level 2 CBR Cycle

The four CBR operations apply at Level 2 with distinct semantics from Level 1:

**Retrieve.** When a new task arrives, the practitioner identifies which Level 2 case
(plan) matches the task class. Retrieval at Level 2 is plan matching: does the
Inference Repository structure of an existing plan suit the new task? The `.ncn`
artifact makes this assessment tractable — a practitioner reads the plain-prose
narrative of an existing plan and determines whether it matches the new problem.

**Reuse.** The retrieved plan is instantiated with new input values and run. This is
Reuse at the abstract level: the full reasoning structure is reused without modification.
All four production-ready plans are reused in this sense on every run — a new PPT topic
instantiates the PPT Generation plan; a new codebase task instantiates the Code
Assistant plan. Reuse at Level 2 generates a fresh set of Level 1 cases.

**Revise.** When the retrieved plan does not perfectly suit the new task, the designer
modifies the `.ncds` source and recompiles: new `.ncd`, `.ncn`, and JSON repositories
are generated. The `.ncn` re-review verifies the revised abstract case before it
generates any concrete cases. This is abstract case revision: the plan's inference
structure, scope bindings, or paradigm assignments are changed to fit the new problem
class. The revised plan is retained for future similar problems.

**Retain.** The revised or newly authored plan joins the case library — a new runtime
definition retained for reuse in future tasks of this class. The case library grows
through use: each new deployment domain that warrants a NormCode plan adds a Level 2
case.

| CBR Operation | Level 2 mechanism | What changes |
|---------------|-------------------|--------------|
| **Retrieve** | Plan matching via `.ncn` review | Identify the right $\mathcal{IR}$ for the task |
| **Reuse** | Instantiate plan with new inputs; run | New Level 1 cases generated |
| **Revise** | Edit `.ncds`, recompile, re-review `.ncn` | New $(\mathcal{IR}, \mathcal{CR}_{\text{schema}})$ |
| **Retain** | Revised plan joins the case library | Case library grows |

## 5.3 The Compilation Pipeline as Distillation

The compilation pipeline (Derivation → Formalization → Post-Formalization → Activation)
is the distillation process that produces Level 2 cases from experience and intent.

**Input.** A natural language description of the task, accompanied by observed patterns
from Level 1 runs (which reasoning steps proved necessary, what intermediate results
were useful, where the original approach failed).

**Output.** A compiled, executable Level 2 case: `concept_repo.json` +
`inference_repo.json` + `.ncn` narrative.

**The distillation phases:**

- *Derivation* extracts the conceptual structure from the natural language description:
  what concepts are involved, how they depend on each other, what operations transform
  them. This is the analogue of identifying patterns in Level 1 case traces.

- *Formalization* assigns precise addresses (flow indices) and determines execution
  types — which steps invoke LLMs (semantic), which perform deterministic routing
  (syntactic). This is the analogue of abstracting a general pattern from specific
  instances.

- *Post-Formalization* assigns execution resources: which agent handles which
  inference, what tools are available, what tensor shapes are expected. This is the
  analogue of instantiation parameters in a generalized case [Müller & Bergmann 2015].

- *Activation* serializes the abstract case into orchestrator-ready JSON — the form
  in which it is stored, retrieved, and instantiated.

The compilation pipeline is related to process mining [van der Aalst 2011] in that
both extract structured process representations from experience. The key difference is
authorial: process mining performs automated discovery from event logs; NormCode
compilation is human-directed and LLM-assisted, producing interpretable artifacts
rather than mined process models.

## 5.4 Self-Hosting: Recursive Case-Based Learning

The most striking consequence of NormCode as a reasoning medium is this: **the
compilation pipeline itself is a NormCode plan.**

Going from a natural-language task description to a compiled, executable plan is a
multi-step reasoning process — identify concepts, extract dependencies, formalize
inference structure, assign execution resources, generate repositories. This process
is expressible in NormCode syntax, with four top-level inference groups corresponding
to the four compilation phases.

An initial `.ncds` sketch of the compilation plan looks like this:

```
<- compilation result
    <= report compilation status and output paths
    <- specification analysis
        <= analyze specification: identify root output, ground inputs, and transformations
        <- task specification
        <- project context
    <- ncds draft
        <= derive hierarchical concept structure from specification analysis
        <- specification analysis
    <- formal ncd
        <= formalize draft: assign flow indices, sequence types, and value bindings
        <- ncds draft
    <- post-formal ncd
        <= post-formalize: assign paradigms, reference shapes, and provision paths
        <- formal ncd
    <- repositories
        <= activate post-formal plan into executable concept and inference repositories
        <- post-formal ncd
    <- task specification
    <- project context
```

Each `<=` in this initial sketch is a high-level operation whose meaning is
unambiguous but whose execution is underspecified. The compilation process itself
decomposes these into concrete inferences — for example, "derive hierarchical concept
structure" expands into sub-steps for extracting concepts, mapping dependencies,
assigning markers, and verifying hierarchy; "formalize draft" expands into flow index
assignment, sequence type determination, and value binding resolution. This progressive
decomposition is itself a Level 2 revision cycle: the initial `.ncds` is the starting
abstract case, revised through repeated compilation iterations and retained as the
refined executable plan. Each decomposition iteration improves accuracy — finer
inferences receive more precisely scoped inputs, reducing the ambiguity that a single
coarse LLM call would face.

The self-hosted compilation case study (§8) demonstrates this concretely: the NC
Compilations plan runs the NormCode compiler pipeline within NormCode, producing
`concept_repo.json` and `inference_repo.json` for new plans. This is Level 1 CBR
instantiating a Level 2 case — the compilation plan — and generating checkpoints at
each compilation phase.

The recursive structure has three consequences:

1. **Validation.** If the compilation pipeline produces correct plans for other tasks,
   and the compilation pipeline itself is a NormCode plan, then the pipeline is
   self-consistent: it can compile itself. This is a standard self-hosting test, here
   reinterpreted as a Level 2 CBR validation.

2. **Improvement through revision.** Improving the compilation pipeline is abstract
   case revision at the meta-level: modify the `.ncds` of the compilation plan,
   recompile, and test by re-running the self-hosted compilation. A better compiler
   is a better abstract case for "how to build abstract cases."

3. **Recursive retention.** Each improvement to the compilation pipeline is retained
   as a new Level 2 case — the updated compilation plan joins the case library.
   Improvements to the meta-case refine the entire case generation process.

This self-similar structure distinguishes NormCode from a planning DSL. A DSL executes
instructions. A reasoning medium can reason about how to improve its own instructions
— and retain those improvements as experience.

## 5.5 Relation Between the Two Levels

Level 1 and Level 2 are not independent architectures — they are reciprocally
constitutive:

- Every Level 1 run is an instance of exactly one Level 2 case. The Level 2 case
  defines the structure; Level 1 runs produce the experience.
- Experience accumulated as Level 1 cases informs the revision of Level 2 cases:
  patterns of failure, useful intermediate checkpoints, and successful revision
  cycles all provide evidence for refining the plan.
- The compilation pipeline — the mechanism for producing Level 2 cases — is itself
  a Level 2 case, instantiated to produce new Level 2 cases.

The Canvas App makes both levels accessible in one environment: the Graph View and
Tensor Inspector for Level 1; the compilation workflow and `.ncn` review for Level 2.
An operator who cannot read `.ncds` syntax can fully participate in Level 1 CBR; a
designer who uses the compilation workflow participates in Level 2.
