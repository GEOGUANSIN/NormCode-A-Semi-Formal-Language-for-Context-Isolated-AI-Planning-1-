# Appendix Plan — NormCode Demo Paper

**Purpose:** Detailed specification for the paper's supplementary appendix.
The six-page body is evidence-focused and space-constrained. The appendix
is where the system can breathe: full plan listings, complete traces, extended
comparisons, format specifications, and architecture detail that reviewers and
practitioners will want but the body cannot hold.

**Format note:** For ACL/EMNLP System Demonstrations, appendix pages are
unlimited and do not count toward the page limit. For arXiv, structure as
a self-contained extended version. Either way, every appendix section should
standalone — do not assume the reader has memorized the body.

---

## Appendix A — NormCode Language Reference

**Type:** Technical reference (tables + code blocks)
**Estimated length:** 1.5–2 pages
**Purpose:** A complete quick-reference for the `.ncds` syntax. Lets readers
understand every code fragment in the body without consulting the full paper.

### A.1 Symbol Table

| Symbol | Name | Role | Analogy |
|--------|------|------|---------|
| `<-` | **Data marker** | Declares a value, document, or result that flows through the plan | Noun / variable declaration |
| `<=` | **Action marker** | Declares an operation an AI agent or tool performs | Verb / function call |
| `<*` | **State marker** | Carries mutable data across loop iterations | Loop variable / accumulator |
| `::` | **Grounding operator** | Grounds an action to a specific tool or resource | Method binding |
| Indentation | **Scope delimiter** | Each marker sees only data declared within its own indented block | Block scope |
| Flow index | **Address** | Hierarchical unique identifier for every node (e.g., `1.3.2`) | Line number / UUID |

### A.2 File Format Summary

| Format | Extension | Produced by | Read by | Purpose |
|--------|-----------|-------------|---------|---------|
| NormCode Design Spec | `.ncds` | Human author / AI generator | Compiler, humans | The plan as a portable text artifact |
| NormCode Design | `.ncd` | Compiler (Phase 2) | Compiler (Phases 3-4), humans | Formal plan with flow indices |
| NormCode Natural | `.ncn` | Compiler (Phase 2) | Humans (domain experts) | Plain-English verification narrative |
| NormCode Design Natural | `.ncdn` | Compiler (Phase 2) | Humans | Hybrid: `.ncd` with `.ncn` interleaved |
| Concept Repository | `concept_repo.json` | Compiler (Phase 4) | Orchestrator | All data concepts and tensor metadata |
| Inference Repository | `inference_repo.json` | Compiler (Phase 4) | Orchestrator | All actions and their wiring |

### A.3 Canonical Example: Annotated Plan

Full annotation of the two-step summary workflow from the paper body:

```
<- summary                   ← Output concept (flow index: 1)
    <= summarize the findings ← Semantic action (1.1) — LLM call
    <- report                ← Input data (1.1.1)
        <= :: read the file  ← Grounded action (1.1.1.1) — tool call
    <- style_guide           ← Input data (1.1.2) — global input
```

Scope rule: `summarize the findings` (1.1) can only receive `report` (1.1.1)
and `style_guide` (1.1.2). It cannot read the contents of the file directly,
access prior plans' outputs, or accumulate session state. The orchestrator
enforces this at execution time.

### A.4 Paradigm Types

NormCode defines five paradigm families that determine how an action executes:

| Paradigm | Type | Description | Example use |
|----------|------|-------------|-------------|
| Imperative | Semantic | LLM generates free-form output | "Summarize the document" |
| Judgement | Semantic | LLM returns a boolean + reasoning | "Is the quality sufficient?" |
| Grouping | Syntactic | Collects inputs into a collection | "Gather all slide outputs" |
| Timing | Syntactic | Conditional branching on data state | "If report is non-empty" |
| Looping | Syntactic | Iterates over a collection | "For each section in outline" |

Syntactic paradigms invoke no LLM. They are free, deterministic, and instant.
They constitute approximately 60–70% of nodes in a typical production plan.

---

## Appendix B — Built-In Plans Gallery

**Type:** Description table + plan graph thumbnails (screenshots)
**Estimated length:** 1–1.5 pages
**Purpose:** Demonstrate expressive completeness. Six production plans cover
document generation, software engineering, meta-compilation, assistance,
analysis, and matching — establishing that NormCode is not a toy language.

| Plan | Inferences (approx.) | Key techniques | Output |
|------|----------------------|----------------|--------|
| **PPT Generation** | ~30 | Nested loop, parallel slide assembly, 6 layouts, 14 component types | `.pptx` + HTML preview |
| **Code Assistant** | ~40 | 7-stage pipeline, parallel codebase exploration, judgement with branching | Implementation + diff + report |
| **NC Compilations** | ~25 | Meta-compilation: NormCode compiling NormCode plans | Compiled `.ncd` + `.ncn` |
| **Canvas Assistant** | ~20 | Context-aware help, plan structure introspection | Natural language answer |
| **3D Model Report** | ~15 | Multi-modal perceptual signs, geometry analysis pipeline | Structured analysis report |
| **BOM Matching** | ~35 | Large-N parallel matching, judgement loops, structured output | Match results + confidence scores |

**Figure App-B:** A 2×3 thumbnail grid of each plan's graph loaded in Canvas
(graph-view, no execution state). Caption: "Six production plans shipped with
NormCode v1.1.3. Each is a single `.ncds` file; complexity ranges from 15 to
40 inferences."

---

## Appendix C — Complete Audit Trace: PPT Agent Run

**Type:** Table (structured audit log)
**Estimated length:** 1–2 pages
**Purpose:** The body claims "every step is auditable." This appendix
substantiates it by showing the complete execution trace of one PPT Agent run,
indexed by flow index. This is what an auditor, regulator, or senior engineer
would actually inspect.

**Format:** One row per inference node, sorted by flow index.

| Flow index | Step name | Paradigm type | Inputs declared | LLM calls | Token count | Output summary |
|-----------|-----------|---------------|-----------------|-----------|-------------|----------------|
| 1 | presentation | Grouping | slides, topic | — | 0 | Collection assembled |
| 1.1 | slides | Looping | current_slide, outline_section, style_guide | — | 0 | Loop over 8 sections |
| 1.1.1 | current_slide | State | (loop variable) | — | 0 | Slide index 1–8 |
| 1.1.2 | outline_section | Imperative | outline, current_slide | 1 | ~120 | Section 1 extracted |
| 1.1.2.1 | outline | Imperative | topic | 1 | ~800 | 8-section outline |
| 1.1.2.1.1 | topic | Data | (input) | — | 0 | "Machine learning in healthcare" |
| 1.1.3 | slide content | Imperative | outline_section, style_guide | 1 | ~600 | Slide 1 HTML content |
| ... | *(×8 loop iterations)* | ... | ... | ... | ... | ... |
| 1.2 | assemble final | Imperative | slides, topic | 1 | ~400 | Full presentation HTML |
| 1.3 | topic | Data | (input) | — | 0 | "Machine learning in healthcare" |

**Totals row:** ~12 LLM calls, ~7,200 tokens, 0 implicit context leaks detected.

**Note:** Gray rows (syntactic) have 0 token cost and are not shown in the
Canvas tool call monitor. Purple rows are shown with full prompt + response inline.
Every row is addressable by flow index; a failed row identifies exactly which
step and which inputs to inspect.

---

## Appendix D — The `.ncn` Format: Extended Examples

**Type:** Text + code blocks
**Estimated length:** 1 page
**Purpose:** The `.ncn` human-verification format is the body's most
underexplained differentiator. This appendix gives three extended examples
spanning simple, nested, and loop-containing plans — showing what a
non-technical reviewer actually reads.

### D.1 Simple: Two-Step Summary

`.ncds` input:
```
<- summary
    <= summarize the findings
    <- report
        <= :: read the uploaded file
    <- style_guide
```

`.ncn` output (compiler-generated):
```
(OUTPUT) summary
  (ACTION) is obtained by summarizing the findings
  (INPUT)  using report
             (OUTPUT) report
               (ACTION) is obtained by reading
                        the uploaded file
               (INPUT)  [grounded to: file_system tool]
  (INPUT)  and style_guide
           [provided by caller as input]
```

### D.2 Nested Loop: PPT Slide Generation

`.ncn` output for the slide generation loop (excerpt):
```
(OUTPUT) slides
  (ACTION) is obtained by, for each current_slide
           in the slide collection,
           generating slide content
  (INPUT)  using outline_section
             (OUTPUT) outline_section
               (ACTION) is obtained by extracting
                        the section for the
                        current slide
               (INPUT)  using outline
                          (OUTPUT) outline
                            (ACTION) is obtained by
                                     generating a
                                     presentation outline
                            (INPUT)  using topic
  (INPUT)  and style_guide
  (STATE)  current_slide tracks position in loop
```

### D.3 Compliance Checklist Format

For regulated domains, the `.ncn` format can be mapped directly to an
audit checklist. A compliance officer reviewing the PPT Agent might ask:

| Question | Answer from `.ncn` |
|----------|-------------------|
| What does "generate slide content" receive as input? | `outline_section` and `style_guide` |
| Can it access prior slides' content? | No — not declared in its input scope |
| Can it access the original topic directly? | No — only via `outline_section` (indirect) |
| What produces `outline_section`? | The "extract section" action, given `outline` and `current_slide` |
| What external resource does "read file" use? | `file_system` tool (declared in agent configuration) |

This structural answer is available before execution — not reconstructed from
logs after the fact.

---

## Appendix E — Perceptual Signs and the Tensor System

**Type:** Technical explanation + annotated example
**Estimated length:** 0.75–1 page
**Purpose:** Perceptual signs appear in the Scenario B tensor inspector but
are not explained in the body. This appendix gives the full picture: format,
purpose, and how they prevent context pollution.

### E.1 The Context Pollution Problem

In a conventional multi-step agent, step N's prompt typically includes:
```
[System prompt]
[Full conversation history from steps 1 to N-1]
[Task instruction for step N]
```

The LLM at step N can "see" everything. In long workflows, this creates:
- **Confusion:** Old context overrides current task intent
- **Hallucination:** The model references data that is no longer valid
- **Irreproducibility:** Repeating step N produces different results if history changed
- **Audit impossibility:** "What did step N actually use?" requires full prompt reconstruction

### E.2 Perceptual Signs as Lightweight Pointers

A perceptual sign is a token that *identifies* a data object without *containing* its content:

```
%{file_location}a1c(src/orchestrator.py)
```

| Component | Meaning |
|-----------|---------|
| `%{file_location}` | Norm type — how to resolve this pointer |
| `a1c` | Unique ID — stable reference within the session |
| `src/orchestrator.py` | Signifier — human-readable label for the pointer |

The orchestrator passes perceptual signs between steps instead of raw content.
The LLM at step N sees only the sign, not the file contents — unless step N
has a `file_system` read action that explicitly retrieves it.

This means: passing 100 file pointers to a summarizer costs ~100 tokens (the
signs), not ~500,000 tokens (the file contents). The LLM at the summary step
receives exactly the files it needs to work with — declared explicitly, not
accumulated.

### E.3 The Tensor Inspector Display

When the operator opens the tensor inspector at a completed data node, they see:

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

This is exactly what the next step will receive. Not approximately, not inferred
from configuration — exactly. The axis name (`[file]`), shape (`(7,)`), and each
sign's ID and signifier are the complete declared input boundary.

---

## Appendix F — Compilation Pipeline: Full Detail

*(This appendix expands the illustration already specified in `illustrations_plan.md`
App Figure A. The figure goes here as App-F-1; this text provides the prose.)*

**Type:** Prose + figure
**Estimated length:** 1 page

### F.1 The Four Phases

**Phase 1 — Derivation.** The compiler takes a natural-language instruction
(or a hand-authored `.ncds` draft) and identifies the concepts, operations,
dependencies, and hierarchy implied by the text. This phase is LLM-assisted:
the compiler asks "what are we doing, and what does it depend on?" Output: a
draft `.ncds` structure.

**Phase 2 — Formalization.** The draft structure is assigned flow indices
(1, 1.1, 1.1.1, …), sequence types are determined (imperative, judgement,
grouping, timing, looping), and the `.ncn` companion document is generated.
This phase is rule-based and deterministic. The `.ncn` is available for
human review at this point — before any execution resource is assigned.

**Phase 3 — Post-Formalization.** Each action receives a paradigm ID, tool
faculties are assigned from the agent configuration, and tensor axes and shapes
are declared for every data concept. Resource paths are resolved. This phase
enriches the `.ncd` with execution metadata.

**Phase 4 — Activation.** The enriched `.ncd` is split into two JSON
repositories: `concept_repo.json` (all data concepts with tensor metadata)
and `inference_repo.json` (all actions with wiring, paradigm IDs, and
dependencies). A `working_interpretation` document is generated summarizing
the plan. The orchestrator loads these two files at runtime.

### F.2 Human Review Points

The pipeline exposes three natural review opportunities:
- **After Phase 1:** The draft `.ncds` can be inspected for structural correctness
- **After Phase 2:** The `.ncn` plain-English narrative can be read by domain experts
- **After Phase 3:** The enriched `.ncd` with paradigm assignments can be confirmed

No LLM has been called at any of these review points. The plan is fully
understood — and potentially rejected or modified — before any probabilistic
operation begins.

---

## Appendix G — Extended Tool Comparison

**Type:** Table + brief annotations
**Estimated length:** 1 page
**Purpose:** The Related Work (§7) provides a focused comparison. This appendix
gives a full feature matrix for practitioners evaluating tools.

| Feature | NormCode Canvas | LangSmith | LangFlow | PromptFlow | AutoGen Studio | Flowise |
|---------|----------------|-----------|----------|------------|----------------|---------|
| **Plan format** | `.ncds` plain text | Python/LCEL code | Internal JSON graph | YAML/Python | Python config | Internal JSON |
| **Portable artifact** | ✓ (text file, Git-able) | ✗ | ✗ (platform graph) | Partial (YAML) | ✗ | ✗ |
| **Non-programmer authoring** | ✓ (`.ncds` + `.ncn`) | ✗ | ✓ (drag-drop) | Partial | ✗ | ✓ (drag-drop) |
| **Human review before execution** | ✓ (`.ncn` narrative) | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Enforced data isolation** | ✓ (language-level) | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Breakpoint debugging** | ✓ | ✗ | ✗ | Partial | ✗ | ✗ |
| **Tensor inspector** | ✓ (N-dimensional, named axes) | ✗ (raw strings) | ✗ | ✗ | ✗ | ✗ |
| **Value override without restart** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Checkpoint fork** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Multi-agent (heterogeneous LLMs)** | ✓ (per-step) | Partial | Partial | ✓ | ✓ | Partial |
| **Perceptual signs / lazy refs** | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Semantic/syntactic separation** | ✓ (explicit in graph) | ✗ | ✗ | Partial | ✗ | ✗ |
| **Full token-level audit trail** | ✓ (by construction) | ✓ (post-hoc) | ✗ | Partial | ✗ | ✗ |
| **Open-source / self-hosted** | Partial (orchestrator open) | ✗ (SaaS) | ✓ | ✓ | ✓ | ✓ |
| **Windows desktop app** | ✓ (Canvas App v1.1.3) | ✗ | Browser | Browser | Browser | Browser |

**Key distinctions:**
- LangSmith and NormCode Canvas both provide full audit trails — but LangSmith's
  is post-hoc (instrumentation); NormCode's is structural (the language enforces it).
- LangFlow and Flowise both provide non-programmer authoring — but their plans are
  platform-locked UI graphs, not portable text files.
- Only NormCode Canvas exposes a pre-execution human review layer (`.ncn`), value
  override, checkpoint forking, and structural data isolation.

---

## Appendix H — System Architecture

**Type:** Prose + architecture diagram (App-H-1)
**Estimated length:** 0.75 page
**Purpose:** Provides the technical architecture detail missing from the body's
one-paragraph §3.2. Useful for readers evaluating integration or deployment.

### H.1 Component Overview

```
┌────────────────────────────────────────────────────┐
│                   Canvas App (Frontend)             │
│  React 18 · TypeScript · React Flow · Zustand      │
│  TailwindCSS · Vite                                │
│                                                    │
│  ┌──────────┐  ┌─────────────┐  ┌───────────────┐ │
│  │Graph View│  │Left Panel   │  │Right Panel    │ │
│  │React Flow│  │Agent Config │  │Tensor Inspector│ │
│  │nodes+edges│  │Tool log     │  │Node detail    │ │
│  └──────────┘  └─────────────┘  └───────────────┘ │
└────────────────────────┬───────────────────────────┘
          REST API        │      WebSocket (real-time events)
┌────────────────────────▼───────────────────────────┐
│                   Canvas Backend                    │
│  FastAPI · Python 3.11 · Uvicorn                  │
│                                                    │
│  ┌──────────────┐  ┌──────────────┐               │
│  │  REST router  │  │ WS manager   │               │
│  │  /run /pause  │  │ event stream │               │
│  │  /fork /step  │  │ node updates │               │
│  └──────┬───────┘  └──────────────┘               │
│         │                                          │
│  ┌──────▼──────────────────────┐                  │
│  │      Orchestrator           │                  │
│  │  concept_repo + inference   │                  │
│  │  Checkpoint store (SQLite)  │                  │
│  │  Selective re-run engine    │                  │
│  └──────┬──────────────────────┘                  │
│         │ tool calls                               │
│  ┌──────▼──────────────────────┐                  │
│  │  Agent Paradigm Executors   │                  │
│  │  ┌────────┐  ┌──────────┐  │                  │
│  │  │ LLM    │  │ Tool     │  │                  │
│  │  │imperative│ │file_sys  │  │                  │
│  │  │judgement│  │py_interp │  │                  │
│  │  └────────┘  └──────────┘  │                  │
│  └─────────────────────────────┘                  │
└────────────────────────────────────────────────────┘
          ↑
  concept_repo.json + inference_repo.json
  (output of Compiler, loaded at startup)
```

### H.2 Data Flow at Runtime

1. Operator loads a compiled plan (JSON repositories) into Canvas via the file tree.
2. Operator clicks Run → REST `POST /run` → Orchestrator begins execution.
3. Orchestrator resolves the inference graph's topological order.
4. For each ready inference: calls the assigned Agent's paradigm executor.
5. Executor calls the LLM or tool; on completion, stores the output tensor in SQLite.
6. Orchestrator emits a WebSocket `node_complete` event → Canvas updates the node to green.
7. At a breakpoint: Orchestrator emits `node_paused`; waits for `POST /resume` or `POST /override`.
8. On override: Orchestrator updates the stored tensor in SQLite; marks only downstream
   inferences as stale; re-runs stale inferences in topological order.
9. On fork: Orchestrator creates a new run entry in SQLite, copies checkpoint state
   up to the fork point, and executes the new run independently.

### H.3 Checkpoint Store Schema (simplified)

```sql
runs (run_id, plan_id, created_at, status)
checkpoints (checkpoint_id, run_id, flow_index, tensor_json, created_at)
events (event_id, run_id, flow_index, event_type, payload, created_at)
```

Every row in `checkpoints` is the full tensor at a completed node. Forking
copies all checkpoint rows up to the fork point into a new run. The original
run is unaffected.

---

## Appendix I — The Three-Role Workflow: End-to-End Narrative

**Type:** Scenario walkthrough (prose)
**Estimated length:** 0.75 page
**Purpose:** Shows the full three-role handoff for a single plan — from
designer authoring through operator deployment through end-user interaction.
Answers "who does what with the `.ncds` file across its lifetime?"

**Scenario:** The `ppt_generation.ncds` plan, from creation to end-user use.

**Designer's session:**
The designer writes `ppt_generation.ncds` in a text editor. The NormCode
compiler is run (`normcode compile ppt_generation.ncds`), producing
`concept_repo.json`, `inference_repo.json`, and `ppt_generation.ncn`.
The designer sends all four files to the operator. They commit the `.ncds`
to the team's Git repository — `concept_repo.json` and `inference_repo.json`
are generated artifacts and may be committed alongside or regenerated on demand.

**Operator's session:**
The operator opens Canvas, loads the project, and reads `ppt_generation.ncn` —
a plain-English narrative of the entire plan — to verify that the logic matches
the intended behavior. They run the plan with a test topic ("quantum computing"),
watch the execution graph unfold step by step, and inspect a mid-run tensor
to confirm slide content quality. Satisfied, they deploy the plan to the
NormCode Server with `POST /plans/upload`.

**End User's session:**
The end user visits the NormCode Client interface — a simple web form with a
single input field ("Enter your topic") and a download button. They type
"renewable energy in urban planning" and click Submit. The Server calls the
Orchestrator with the plan and input; after approximately 90 seconds (8 LLM
calls), the output appears: an HTML preview of the presentation and a
`.pptx` download link. The end user never sees a `.ncds` file, a flow index,
or a tensor — only a clean interface and a presentation.

**What this shows:** The same `.ncds` file serves three roles with no
duplication, no interface leakage, and no platform lock-in. The designer owns
the plan; the operator owns the execution; the end user owns the output.

---

## Appendix J — Failure Mode Analysis

**Type:** Table + brief explanations
**Estimated length:** 0.5 page
**Purpose:** Addresses the implicit reviewer question: "What happens when
something goes wrong?" NormCode's structural properties make failures
predictable and localizable — this appendix documents the taxonomy.

| Failure type | Where it surfaces | How NormCode surfaces it | Recovery |
|-------------|------------------|--------------------------|---------|
| **LLM output schema mismatch** | At the node that expected a structured output | The orchestrator fails the node immediately; red indicator with schema diff | Override the upstream node with corrected output; resume |
| **Missing input (scope violation)** | At compile time | Compiler rejects the plan — undefined concept referenced outside scope | Fix the `.ncds` and recompile |
| **Tool unavailable** | At the node that calls the tool | Node fails with tool error; upstream nodes remain completed | Fix tool configuration; resume from cached checkpoint |
| **LLM hallucination (soft failure)** | At any semantic node's output | Visible in the tensor inspector at the output node; not automatically detected | Set a breakpoint at the next consumer; inspect and override |
| **Timeout / rate limit** | At any semantic node | Node fails; cached checkpoints preserved | Resume from cached state after limit clears |
| **Scope contamination** | Never — prevented structurally | Not applicable | Not applicable |

The final row is the important one: scope contamination — the root cause of
the "context pollution" failure mode described in §1 — cannot occur at runtime
because the orchestrator enforces scope at the language level. It is not a
runtime check; it is a structural property.

---

## Summary Table

| Appendix | Content | Type | Est. pages |
|----------|---------|------|------------|
| A | Language Reference (symbol table, file formats, paradigm types) | Tables + code | 1.5 |
| B | Built-In Plans Gallery (6 plans, thumbnails) | Table + figures | 1.0 |
| C | Complete Audit Trace: PPT Agent run | Table | 1.5 |
| D | The `.ncn` Format: Extended Examples | Code + tables | 1.0 |
| E | Perceptual Signs and the Tensor System | Prose + code | 0.75 |
| F | Compilation Pipeline: Full Detail | Prose + figure | 1.0 |
| G | Extended Tool Comparison (feature matrix) | Table | 1.0 |
| H | System Architecture (diagram + data flow) | Prose + diagram | 0.75 |
| I | Three-Role Workflow: End-to-End Narrative | Prose | 0.75 |
| J | Failure Mode Analysis | Table | 0.5 |
| **Total** | | | **~10 pages** |

---

## Figures Needed for Appendix

| ID | Caption | Section |
|----|---------|---------|
| App-A-1 | Four-phase compilation pipeline (flow diagram) | Appendix F (formerly App Fig A) |
| App-B-1 | Semantic/syntactic separation annotated graph | Appendix A §A.4 (formerly App Fig B) |
| App-B-2 | 2×3 thumbnail gallery of all six built-in plans | Appendix B |
| App-C-1 | Code Assistant plan graph — full 7-stage view | Appendix B (formerly App Fig C) |
| App-D-1 | Multi-agent configuration panel close-up | Appendix H §H.2 (formerly App Fig D) |
| App-H-1 | Full system architecture diagram | Appendix H §H.1 |

---

> **NOTE ON ORDERING:** The appendix sections above are ordered from
> language-level → system-level → operational → failure taxonomy.
> For the submission, reorder based on reviewer expectations:
> put the Language Reference (A) and Tool Comparison (G) early
> if the venue emphasizes novelty claims; put Audit Trace (C) and
> Failure Analysis (J) early if the venue emphasizes evaluation rigor.
