# Appendix B — Built-In Plans Gallery

NormCode ships with six production-quality plans. These are not toy examples
or tutorials — they are the plans the development team uses to validate the
system, and the plans available to operators immediately after installation.
Their variety demonstrates expressive completeness: NormCode can describe
workflows from document generation to meta-compilation to structured matching.

---

## B.1 Plans Overview

| Plan | `.ncds` file | Inferences (approx.) | LLM calls per run | Key techniques |
|------|-------------|---------------------|-------------------|----------------|
| **PPT Generation** | `ppt_generation.ncds` | ~30 | ~10–14 | Nested loop, 6 slide layouts, 14 component types, parallel assembly |
| **Code Assistant** | `code_assistant.ncds` | ~40 | ~8–15 | 7-stage pipeline, parallel codebase exploration, judgement branching |
| **NC Compilations** | `nc_compilations.ncds` | ~25 | ~12–20 | Meta-compilation: NormCode compiling NormCode plans via the compiler |
| **Canvas Assistant** | `canvas_assistant.ncds` | ~20 | ~4–8 | Context-aware help, plan structure introspection, scoped Q&A |
| **3D Model Report** | `model_report.ncds` | ~15 | ~6–10 | Multi-modal perceptual signs, geometry analysis pipeline, structured output |
| **BOM Matching** | `bom_matching.ncds` | ~35 | ~15–25 | Large-N parallel matching, judgement loops, confidence scoring, structured output |

> **[APP-FIGURE B-1 HERE — 2×3 thumbnail grid: each plan's inference graph loaded in Canvas graph-view, labeled with plan name and inference count. No execution state needed — all nodes pending gray is fine. Zoom level should show full graph topology.]**

---

## B.2 Plan Profiles

### PPT Generation (`ppt_generation.ncds`)

**Use case:** Takes a topic string as input; produces a `.pptx` file and HTML
slide preview.

**Structure:** A nested loop over outline sections. The outer plan generates a
presentation outline; the inner loop iterates over sections, extracting each
section and generating slide content for it; a final assembly action combines
all slides into the output presentation.

**Key techniques demonstrated:**
- **Nested loop with `<*` state:** The loop variable tracks the current slide index
  across iterations so each pass knows which section it is processing.
- **Syntactic routing separating layout from content:** Six slide layout types
  (title, content, two-column, image, table, closing) are selected by timing
  nodes (syntactic, no LLM cost) before the content generation inference fires.
- **Fourteen component types:** Bullet lists, headers, callouts, code blocks,
  image placeholders, and others are structured in the output tensor — not
  free-form strings — ensuring the final renderer receives typed data.
- **Global input reuse:** The `style_guide` input is declared at the outer plan
  level and re-declared within the inner loop's scope, making it available to
  every slide generation action without being re-fetched.

**Inferences:** ~30 total. ~10–14 are semantic (LLM calls); the remainder are
syntactic routing nodes (layout selection, section extraction, collection
grouping) that execute at zero token cost.

---

### Code Assistant (`code_assistant.ncds`)

**Use case:** Takes a software engineering task description; produces an
implementation diff, test results, and a written report.

**Structure:** Seven sequential stages with internal parallelism in the Explore
stage.

```
Receive → Triage → Explore → Plan → Implement → Verify → Report
```

- **Receive:** Parses the task description into structured fields (objective,
  constraints, affected files — if known).
- **Triage:** Classifies the task (bug fix / feature / refactor / documentation)
  and sets routing flags for downstream stages.
- **Explore:** Runs parallel file-reading inferences across multiple candidate
  files; synthesizes findings into a structured exploration summary.
- **Plan:** Generates a step-by-step implementation plan using the exploration
  summary and triage output.
- **Implement:** Executes the plan, producing code changes as a structured diff.
- **Verify:** A judgement inference evaluates the diff against the task
  constraints; if it fails, a timing node routes back to Plan for revision.
- **Report:** Assembles the final output — diff, verification result, and a
  prose explanation.

**Key techniques demonstrated:**
- **Parallel inferences:** The Explore stage runs multiple file-read inferences
  concurrently; the orchestrator resolves their shared dependency on the file
  collection tensor.
- **Judgement with loop-back:** The Verify stage's boolean output controls a
  timing node that can re-enter the Plan–Implement cycle.
- **Context isolation across stages:** The Implement stage receives only the
  Plan output, the Triage flags, and the Explore summary. It cannot see the
  raw Receive text or the full file contents from Explore — only the
  structured summary that the synthesize action explicitly declared.

---

### NC Compilations (`nc_compilations.ncds`)

**Use case:** Compiles a new NormCode plan from a natural-language workflow
description, producing `.ncds`, `.ncd`, `.ncn`, and compiled repositories.

**Structure:** A meta-plan — NormCode compiling NormCode. The plan runs the
NormCode compiler's four phases as orchestrated inference steps, with LLM calls
handling the language-level reasoning (Derivation, Formalization) and rule-based
tool calls handling the formal transformations (Post-Formalization, Activation).

**Key techniques demonstrated:**
- **Grounded actions calling the compiler tools:** Each phase is a `:: compiler`
  grounded action — the LLM provides semantic reasoning; the compiler tool
  applies formal rules.
- **Multi-format output:** The plan produces all four output formats
  (`.ncds`, `.ncd`, `.ncn`, repositories) as separate output concepts with
  distinct tensor types.
- **Self-referential validation:** An optional verification stage re-reads
  the generated `.ncn` and asks a judgement inference whether the compiled
  plan matches the original intent.

---

### Canvas Assistant (`canvas_assistant.ncds`)

**Use case:** Answers questions about a loaded NormCode plan — "What does step
1.3.2 do?", "Why is node X purple?", "What would happen if I override this value?"

**Structure:** A scoped Q&A pipeline. The user's question is classified; the
relevant plan sections are extracted (not the full plan); a focused LLM call
answers using only the extracted scope.

**Key techniques demonstrated:**
- **Plan introspection via perceptual signs:** The assistant references nodes
  by flow index as perceptual signs, not by embedding the full plan text into
  every query.
- **Question-type routing:** Timing nodes classify the question as structural,
  execution-related, or debugging-related and route to specialized answering
  inferences accordingly.
- **Scoped context:** Each answering inference receives only the relevant plan
  excerpt — not the full 30–40 node plan — preventing the assistant itself from
  suffering context pollution.

---

### 3D Model Report (`model_report.ncds`)

**Use case:** Takes a 3D model file (e.g., `.obj`, `.stl`); produces a
structured analysis report covering geometry, topology, potential manufacturing
issues, and recommendations.

**Structure:** A sequential analysis pipeline with multi-modal inputs.

**Key techniques demonstrated:**
- **Multi-modal perceptual signs:** The 3D model is referenced as a
  `%{model_location}` perceptual sign throughout the pipeline; the actual
  geometry data is loaded only by the specific inferences that require it.
- **Structured output with named axes:** Analysis results are stored as
  tensors with named axes (e.g., `[issue_type]`, `[severity]`) rather than
  free-form text, enabling downstream formatting inferences to lay out the
  report with typed data.
- **Heterogeneous paradigm mix:** Some analysis steps use an imperative LLM
  call (describe the geometry); others use a judgement call (does this mesh
  have manifold errors?); structural extraction is handled by tool calls.

---

### BOM Matching (`bom_matching.ncds`)

**Use case:** Takes a Bill of Materials (list of required components) and a
parts catalog; produces a match report with confidence scores and unmatched
items flagged.

**Structure:** A large-N parallel matching pipeline with judgement-based
confidence evaluation.

**Key techniques demonstrated:**
- **Large-N parallel inferences:** Each BOM item is matched against the catalog
  in a parallel loop; the orchestrator runs these independently, with results
  collected into a results collection.
- **Judgement loops with confidence thresholds:** Each match is evaluated by a
  judgement inference (Is this match above threshold?); low-confidence matches
  are routed to a secondary disambiguation stage.
- **Structured output:** The final report is a tensor with named axes
  (`[bom_item]`, `[matched_part]`, `[confidence]`, `[status]`) — suitable
  for downstream processing by a spreadsheet export or database write action.
- **High inference count:** At ~35 inferences per standard BOM, this is the
  most computationally intensive built-in plan. The parallel architecture keeps
  wall-clock time proportional to the longest match, not the total count.

---

## B.3 What the Gallery Demonstrates

These six plans collectively establish three properties:

**1. Expressive completeness across domains.**
Document generation (PPT), software engineering (Code Assistant),
meta-tooling (NC Compilations), user assistance (Canvas Assistant),
multi-modal analysis (3D Model Report), and structured matching (BOM).
A single language with three markers handles all of these.

**2. Complexity scaling.**
Plans range from ~15 to ~40 inferences. The language does not become
unwieldy at the higher end — the nesting and flow index system keeps
large plans navigable. The Canvas graph view handles all six without
special configuration.

**3. The syntactic/semantic split holds at scale.**
Even in the 40-inference Code Assistant plan, the majority of nodes
are syntactic (routing, grouping, timing, parallel dispatch). LLM calls
are reserved for genuine reasoning tasks. The cost structure is always
visible, never hidden in framework boilerplate.
