# Appendix A — NormCode Language Reference

This appendix provides a complete quick-reference for the NormCode `.ncds`
syntax. Every code fragment in the body of this paper can be read using the
definitions below, without consulting the companion paper.

---

## A.1 The Three Primary Markers

NormCode plans are written using three structural markers. Indentation defines
scope; flow indices address every node.

| Symbol | Name | Role | Analogy |
|--------|------|------|---------|
| `<-` | **Data marker** | Declares a concept: a value, document, tensor, or result flowing through the plan | Noun / variable |
| `<=` | **Action marker** | Declares an operation that an AI agent or a tool performs to produce the concept above it | Verb / function call |
| `<*` | **State marker** | Declares mutable data carried across loop iterations (loop variable / accumulator) | Loop variable |
| `::` | **Grounding operator** | Binds an action to a specific tool or resource (file system, Python interpreter, external API) | Method binding |

Indentation defines scope: a concept declared at depth N can be passed only to
actions declared at depth N+1 within the same block. The orchestrator enforces
this at execution time — no concept is accessible outside its declared scope.

Flow indices (`1`, `1.1`, `1.1.1`, …) are assigned by the compiler during
Phase 2. Every concept and every action receives a unique hierarchical address.
These addresses are used for breakpointing, tensor inspection, selective re-run,
and cross-referencing in audit logs.

---

## A.2 The Scope Rule

The scope rule is the enforcement mechanism for data isolation. It reads:

> **An action at flow index `i.j.k` can only receive data declared within
> the same indented block, at depth `k+1` directly beneath it.**

This means:
- An action cannot read the full conversation history
- An action cannot access prior steps' outputs unless those outputs are
  explicitly re-declared as inputs
- An action cannot reach "upward" to enclosing scope
- Global inputs (provided by the caller at runtime) must be explicitly
  declared at every depth where they are needed

This is not a runtime check — it is a compile-time guarantee. Plans that
attempt to use an out-of-scope concept are rejected by the compiler before
any execution takes place.

---

## A.3 Annotated Plan: The Two-Step Summary Workflow

The canonical minimal example, fully annotated:

```
<- summary                       ← concept: "summary" (flow index 1)
                                   The top-level output of the plan.
    <= summarize the findings    ← action producing "summary" (1.1)
                                   This is a semantic (LLM) call.
    <- report                    ← input concept: "report" (1.1.1)
                                   Declared inside 1.1's block → visible to 1.1 only.
        <= :: read the file      ← action producing "report" (1.1.1.1)
                                   `::` grounds it to a tool call (file_system).
    <- style_guide               ← input concept: "style_guide" (1.1.2)
                                   A global input — provided by the caller.
```

**Reading direction:** Bottom-up. The file is read to produce `report`;
`report` and `style_guide` are used by `summarize the findings` to produce
`summary`. The action at `1.1` can only see `1.1.1` and `1.1.2` — not the
file contents directly, not the caller's context.

**What the orchestrator enforces:** When `summarize the findings` (1.1) runs,
the orchestrator constructs its prompt using only the resolved values of
`report` (1.1.1) and `style_guide` (1.1.2). No other data — no session
history, no implicit state, no prior plan outputs — is included.

---

## A.4 File Formats

The compiler transforms `.ncds` source through a pipeline of intermediate
formats. Each format serves a distinct audience.

| Format | Extension | Produced by | Primary audience | Purpose |
|--------|-----------|-------------|-----------------|---------|
| NormCode Design Spec | `.ncds` | Human author or AI generator | Designers, humans | The plan as an authorable, portable text artifact |
| NormCode Design | `.ncd` | Compiler (Phase 2) | Compiler, power users | Formal plan with assigned flow indices and sequence types |
| NormCode Natural | `.ncn` | Compiler (Phase 2) | Domain experts, compliance | Plain-English verification narrative of the same plan |
| NormCode Design Natural | `.ncdn` | Compiler (Phase 2) | Mixed audiences | Hybrid: `.ncd` structure with `.ncn` prose interleaved |
| Concept Repository | `concept_repo.json` | Compiler (Phase 4) | Orchestrator | All data concepts with tensor axes, shapes, and metadata |
| Inference Repository | `inference_repo.json` | Compiler (Phase 4) | Orchestrator | All actions with paradigm IDs, dependencies, and wiring |

The `.ncds` file is the primary portable artifact. `concept_repo.json` and
`inference_repo.json` are generated artifacts and can be regenerated from
`.ncds` at any time. The `.ncn` is available after Phase 2 — before any
execution resource is assigned or any LLM is called.

---

## A.5 Paradigm Types

Every action in a NormCode plan is assigned a paradigm by the compiler during
Phase 3. Paradigms determine how the orchestrator executes the action.

| Paradigm | Type | Invokes LLM | Deterministic | Description |
|----------|------|------------|---------------|-------------|
| **Imperative** | Semantic | Yes | No | LLM generates a free-form output given its inputs |
| **Judgement** | Semantic | Yes | No | LLM returns a boolean decision plus reasoning trace |
| **Grouping** | Syntactic | No | Yes | Collects multiple inputs into a single collection (array) |
| **Timing** | Syntactic | No | Yes | Conditional branch — executes downstream only if a condition holds |
| **Looping** | Syntactic | No | Yes | Iterates an inner plan over each element of a collection |

**Syntactic paradigms are free and deterministic.** They invoke no LLM, consume
no tokens, and cannot hallucinate. In a typical production plan, 60–70% of nodes
are syntactic. The Canvas graph makes this visible: syntactic nodes are gray;
semantic nodes are purple. Cost and failure attribution follow directly from
this separation.

**Judgement paradigms return a boolean.** The orchestrator uses the boolean to
select which branch of a timing node to activate, enabling conditional logic
without any implicit state accumulation.

---

## A.6 Loop State (`<*`)

The `<*` marker declares a state variable — a concept that the orchestrator
updates after each iteration of a loop. It is the only mechanism in NormCode
for carrying data across iterations, and it must be declared explicitly.

**Example: Accumulating slides across a loop:**

```
<- slides
    <* current_slide           ← state: loop variable (index or accumulator)
    <= :: generate slide       ← action producing one slide per iteration
    <- outline_section
        <= :: extract section  ← syntactic: pulls section i from outline
        <- outline
        <- current_slide
```

The `<*` marker ensures the compiler knows which data changes across iterations.
The orchestrator initializes it before the first iteration and updates it after
each pass. No other concept in the plan can accumulate state implicitly.

---

## A.7 Perceptual Sign Syntax

Perceptual signs are lightweight pointer tokens used to reference data objects
without embedding their contents. They appear in tensors inspected via the
Canvas tensor inspector and are passed between steps instead of raw content.

**Format:**

```
%{norm_type}unique_id(signifier)
```

| Component | Example | Meaning |
|-----------|---------|---------|
| `norm_type` | `file_location` | How to resolve this pointer (which tool/reader handles it) |
| `unique_id` | `a1c` | Stable session-scoped unique identifier |
| `signifier` | `src/orchestrator.py` | Human-readable label (filename, title, URL, etc.) |

**Example — a tensor on the `[file]` axis:**

```
Axis: [file]   Shape: (7,)

  [0]  %{file_location}a1c(src/orchestrator.py)
  [1]  %{file_location}b2d(src/blackboard.py)
  [2]  %{file_location}c3e(src/agent_sequences.py)
  [3]  %{file_location}d4f(src/reference_system.py)
  [4]  %{file_location}e5g(src/paradigms.py)
  [5]  %{file_location}f6h(src/compiler/formalization.py)
  [6]  %{file_location}g7i(src/compiler/activation.py)
```

The LLM receiving this tensor sees the seven signs — not the file contents.
A downstream action with a `:: read file` grounded action retrieves the
content on demand when it needs to process a specific file. This is lazy
evaluation: content is pulled only when explicitly required by an action
that declares it.
