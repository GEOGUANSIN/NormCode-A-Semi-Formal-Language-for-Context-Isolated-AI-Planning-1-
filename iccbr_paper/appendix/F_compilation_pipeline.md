# Appendix F — Compilation Pipeline: Full Detail

The NormCode compiler transforms a `.ncds` source file into the two JSON
repositories (`concept_repo.json`, `inference_repo.json`) that the orchestrator
loads at runtime. The transformation happens in four phases, each with a
distinct concern and a distinct intermediate artifact. This appendix describes
each phase in detail and identifies the human review opportunities between them.

> **[APP-FIGURE F-1 HERE — Four-phase pipeline flow diagram: vertical boxes
> connected by arrows, each labeled with phase name, concern, input, output,
> and human review opportunity. See `illustrations_plan.md` App Figure A
> for full specification.]**

---

## F.1 Phase Overview

| Phase | Name | Core question | LLM-assisted? | Output |
|-------|------|---------------|--------------|--------|
| 1 | Derivation | What are we doing? | Yes | Draft `.ncds` structure |
| 2 | Formalization | In what order, which sequence types? | No (rule-based) | `.ncd` + `.ncn` + `.ncdn` |
| 3 | Post-Formalization | How, and with what resources? | Yes (partially) | Enriched `.ncd` |
| 4 | Activation | What does the orchestrator need? | No (rule-based) | `concept_repo.json` + `inference_repo.json` |

---

## F.2 Phase 1 — Derivation

**Core question:** What concepts and operations does this workflow involve,
and how do they depend on each other?

**Input:** A natural-language workflow description, or a hand-authored draft
`.ncds` file.

**Process:** The compiler makes a series of structured LLM calls to identify:
- The top-level output concept (the plan's final product)
- All intermediate concepts needed to produce it
- The operations that produce each concept
- The dependency relationships (which concepts are inputs to which operations)
- The hierarchy implied by the dependency structure

The derivation process is iterative. The compiler begins with the top-level
output and works downward, asking at each level: "What does this operation
need, and how is each of those things produced?" Cycles are detected and
flagged as errors.

**Output:** A draft `.ncds` file representing the inferred structure. If the
input was already a `.ncds` file, Phase 1 validates and possibly refines it.

**Human review opportunity:** The draft `.ncds` can be reviewed for structural
correctness — are the right concepts present? Are the dependencies correct?
Is anything missing? A designer can edit the `.ncds` before proceeding to
Phase 2.

---

## F.3 Phase 2 — Formalization

**Core question:** In what execution order should these operations run,
and what is the sequence type of each?

**Input:** The draft `.ncds` from Phase 1.

**Process:** Formalization is fully rule-based — no LLM is invoked. The
compiler applies the NormCode type system to:

1. **Assign flow indices:** Every concept and action receives a unique
   hierarchical address (1, 1.1, 1.1.1, …) based on its position in the
   dependency tree.

2. **Determine sequence types:** Each action's context determines its
   paradigm family:
   - If the action produces a boolean decision → Judgement
   - If the action iterates over a collection → Looping (with inner sub-plan)
   - If the action conditionally fires → Timing
   - If the action collects multiple inputs → Grouping
   - Otherwise → Imperative

3. **Generate the `.ncn` companion:** The formalized plan is translated into
   plain-English prose using the `(OUTPUT)/(ACTION)/(INPUT)/(STATE)` vocabulary.
   This translation is exact — no information is added or removed.

4. **Generate the `.ncdn` hybrid:** The formal `.ncd` with `.ncn` prose
   interleaved at each node — useful for human-machine pair review.

**Output:** `.ncd` (formal, indexed), `.ncn` (plain-English narrative),
`.ncdn` (hybrid).

**Human review opportunity:** This is the most important review point.
The `.ncn` is now available. A domain expert, compliance officer, or
product manager reads it to verify that the plan's logic matches the
intended workflow. No LLM has run at this point. If the expert rejects
the plan, the designer modifies the `.ncds` and restarts from Phase 1 or
Phase 2 — with zero execution cost incurred.

---

## F.4 Phase 3 — Post-Formalization

**Core question:** How will each operation execute, and with what resources?

**Input:** The formalized `.ncd` + agent configuration (tool registry, LLM
assignments, paradigm directory).

**Process:** Post-formalization enriches the formal plan with execution
metadata:

1. **Paradigm ID assignment:** Each action node is matched to a specific
   paradigm implementation in the paradigm directory (e.g., `imperative_v2`,
   `judgement_with_trace`, `grouping_collect`).

2. **Tool faculty assignment:** Actions grounded with `::` are matched to
   specific tool implementations in the agent's tool registry
   (e.g., `file_system`, `python_interpreter`, `slide_renderer`).

3. **Tensor axis declaration:** For each concept node, the compiler infers
   or assigns tensor axes and shape constraints based on the operation that
   produces it and the paradigms of actions that consume it.

4. **Agent assignment:** If multiple agents are configured (multi-agent mode),
   flow index ranges are matched to agent configurations using the pattern rules
   specified in the Canvas agent configuration panel.

**LLM involvement:** Phase 3 is largely rule-based, but may invoke a small
LLM call to resolve ambiguous paradigm matches or infer tensor axes for
novel operation descriptions.

**Output:** Enriched `.ncd` with paradigm IDs, tool faculties, tensor
metadata, and agent assignments embedded.

**Human review opportunity:** A technical reviewer can confirm the paradigm
assignments — are the right LLM models assigned to the right steps? Are the
tool bindings correct? This review is optional for straightforward plans but
valuable for complex multi-agent configurations.

---

## F.5 Phase 4 — Activation

**Core question:** What exactly does the orchestrator need at runtime?

**Input:** The enriched `.ncd` from Phase 3.

**Process:** Activation extracts the runtime representation:

1. **Concept extraction → `concept_repo.json`:** Every `<-` node becomes a
   concept entry with its flow index, tensor axes and shapes, norm types for
   any perceptual sign columns, and resolved dependencies.

2. **Inference extraction → `inference_repo.json`:** Every `<=` node becomes
   an inference entry with its flow index, paradigm ID, input concept flow
   indices, output concept flow index, agent assignment, and tool bindings.

3. **Working interpretation generation:** A summary document describing the
   overall plan structure — used by the Canvas graph renderer to display node
   labels and by the Canvas Assistant to answer questions about the plan.

**Output:** `concept_repo.json`, `inference_repo.json`, `working_interpretation`.

**No human review needed at this stage.** Phase 4 is a mechanical
transformation with no semantic decisions. The orchestrator loads the two
JSON files at startup and begins execution when the operator clicks Run.

---

## F.6 What the Compilation Guarantees

The four-phase pipeline provides three structural guarantees that hold for
any compiled plan:

**1. Scope correctness:** Every action can only receive inputs that are
declared in its scope. The compiler rejects plans where an action references
a concept outside its indented block. This guarantee is checked at Phase 2
and cannot be violated by the orchestrator at runtime.

**2. Dependency completeness:** Every concept that an action declares as an
input has a defined producer. There are no undefined references — the compiler
rejects incomplete plans. A plan that compiles is a plan that can execute.

**3. Paradigm coverage:** Every action node has a paradigm ID and, if
grounded, a tool binding. The orchestrator never encounters an action it
doesn't know how to execute. Paradigm assignment failures surface at Phase 3,
before any execution occurs.

---

## F.7 Compilation from Natural Language

When Phase 1 is driven by a natural-language instruction (rather than a
hand-authored `.ncds`), the compiler acts as a plan generator. The user
writes:

> "Read a set of uploaded documents, summarize each one individually,
> then synthesize a final report comparing the key findings."

The Phase 1 derivation produces:

```
<- final_report
    <= synthesize comparative report
    <- summaries
        <* current_doc
        <= summarize document
        <- document_content
            <= :: read uploaded document
            <- current_doc
```

This draft is presented to the designer for review and editing before Phase 2.
The designer can add, remove, or restructure concepts. The compiler is not
the author of the plan — it is a drafting assistant. The designer retains
ownership of the final `.ncds` file.

This is the "Describe" step in the six-step lifecycle, and it can be done
entirely through the Canvas interface or via the NormCode CLI.
