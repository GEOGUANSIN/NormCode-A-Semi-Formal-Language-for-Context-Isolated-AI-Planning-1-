# Illustrations Plan — NormCode Demo Paper

**Purpose:** Specifications for every figure, diagram, and chart needed in the demo paper and appendix. Each entry specifies what must be shown, what to label, suggested creation method, and the caption draft.

**Color convention (maintain across all figures):**
- Semantic / functional nodes: `#c084fc` purple stroke, `#faf5ff` fill (hexagon shape)
- Data / value nodes: `#60a5fa` blue stroke, `#eff6ff` fill (rounded rectangle)
- Syntactic / routing nodes: `#94a3b8` gray stroke, `#f8fafc` fill (rounded rectangle)
- Status — completed: `#22c55e` green indicator
- Status — running: `#3b82f6` blue pulsing indicator
- Status — pending: `#9ca3af` gray indicator
- Status — failed: `#ef4444` red indicator
- Status — skipped: striped gray
- Output node: `#ef4444` red outer ring on data node
- Background: white with subtle dot grid pattern

---

## MAIN BODY FIGURES (4 max for 6-page format)

---

### Figure 1 — Canvas App: Annotated Interface Overview

**Section:** §3 The Canvas App
**Type:** Screenshot with annotation overlays (callout boxes + arrows)
**Size:** Full column width or full page width (use `figure*` in LaTeX)

**What to capture:**
Take a screenshot of the Canvas App with a mid-execution state — some nodes completed (green), one running (blue pulsing), some pending (gray). The PPT generation plan or the summary workflow is ideal.

**Required elements visible in screenshot:**
- **Center panel:** The inference graph with ≥8 nodes visible
  - At least 2 purple hexagon nodes (semantic/imperative)
  - At least 3 blue rounded-rect nodes (data/value)
  - At least 1 gray node (syntactic routing)
  - 1 node with green completed indicator
  - 1 node with blue pulsing running indicator
  - 1 node with red output ring (the final output node)
  - Edge arrows showing data flow
- **Left panel (open):** Agent configuration showing at least one LLM model name configured + tool call log with 1–2 visible entries
- **Right panel (open):** Node detail view — show the tensor inspector for a completed data node, with axis name visible and some data preview
- **Top bar:** Execution controls (Run / Pause / Step / Fork buttons) visible
- **File tree (if visible):** Project files including one `.ncds` file

**Callout annotations to add (7 callouts):**
1. → Graph center: "Inference graph — semantic nodes (purple) vs. data nodes (blue) vs. syntactic routing (gray)"
2. → Running node (blue pulse): "Real-time execution — WebSocket event streaming"
3. → Completed node (green): "Every completed step stores its full output"
4. → Left panel: "Agent configuration — assign different LLMs to different steps"
5. → Tool call log: "Live tool call monitor — every LLM prompt and response"
6. → Right panel tensor inspector: "Tensor inspector — N-dimensional data viewer with axis names"
7. → Execution controls: "Run / Pause / Step / Fork from checkpoint"

**Caption draft:**
> Figure 1: The NormCode Canvas App (v1.1.3). The graph center visualizes the inference plan with semantic operations (purple hexagons) distinct from data nodes (blue) and syntactic routing (gray). Left panel: live agent configuration and tool call monitor. Right panel: tensor inspector showing structured intermediate data at a completed node. Execution controls (top) support run, pause, step-by-step advancement, and fork from any checkpoint.

---

### Figure 2 — PPT Agent: The Plan Lifecycle in One Scenario

**Section:** §4 Demo Scenario A
**Type:** Two-panel figure — left: code block comparison (`.ncds` snippet + `.ncn` translation), right: Canvas execution graph screenshot
**Size:** Full column width, two subfigures side by side

**Left subfigure — Format Comparison (`.ncds` → `.ncn`):**
A static diagram (can be drawn, no screenshot needed) showing the same plan fragment in two formats side by side:

Left column header: `.ncds` (authored by designer)
```
<- slide_3
    <= :: generate slide content
    <- outline_section_3
    <- style_guide
```

Right column header: `.ncn` (read by domain expert before execution)
```
(OUTPUT) slide_3
  (ACTION) is obtained by generating
           slide content
  (INPUT)  using outline_section_3
  (INPUT)  and style_guide
```

Add a bracket/arrow between them labeled: "Compiler — no information lost"

Below both columns, add a small note box:
> "The domain expert reads `.ncn` to verify logic before any LLM call is made."

**Right subfigure — Execution graph screenshot:**
Canvas App showing the PPT generation plan mid-execution:
- Outer loop unfolding (slide 1, slide 2 completed green; slide 3 running blue)
- Show at least the loop structure is visible (several similar nodes in sequence/parallel)
- Output node visible with red ring

**Caption draft:**
> Figure 2: Demo Scenario A — PPT Agent lifecycle. Left: The same plan fragment in `.ncds` (authored format) and `.ncn` (human-readable verification format). A domain expert reads the `.ncn` narrative to approve logic before execution; no syntax knowledge required. Right: The PPT generation plan executing in Canvas — completed slides (green), active slide (blue pulsing), output node (red ring).

---

### Figure 3 — Debug and Fork: Breakpoint + Tensor Inspector

**Section:** §5 Demo Scenario B
**Type:** Screenshot with annotation overlays
**Size:** Full column width

**What to capture:**
Canvas App in breakpoint-paused state. The Code Assistant plan (or PPT Agent) paused at a specific flow index. The right panel tensor inspector must be open and showing real data.

**Required elements visible in screenshot:**
- **The paused node:** Blue node with a breakpoint indicator (dot/badge), labeled with flow index (e.g., `1.3.1`)
- **Tensor inspector (right panel):** Open and showing:
  - Axis name visible (e.g., `[file]` or `[document]`)
  - At least 3 rows of data visible (file paths, or text snippets)
  - The "table / list / JSON" view toggle visible
- **Value override input:** A text field or edit area visible near the paused node or in the right panel, showing the ability to modify data before resuming
- **Fork button:** Highlighted or visible in the control area
- **Upstream nodes:** 2–3 completed (green) nodes feeding into the paused node, showing the bounded inputs

**Callout annotations (5 callouts):**
1. → Paused node: "Breakpoint at flow index 1.3.1 — execution paused before this step runs"
2. → Tensor inspector data: "Exact inputs declared — nothing hidden, nothing implicit"
3. → Axis label: "Named tensor axes — data organized by semantic dimension, not position"
4. → Value override area: "Override value and resume — no full restart required"
5. → Fork button: "Fork from this checkpoint — explore alternative without losing current run"

**Caption draft:**
> Figure 3: Demo Scenario B — Debug and Fork. Execution is paused at flow index 1.3.1 via breakpoint. The tensor inspector (right) shows the exact, bounded inputs this step will receive — every input explicitly declared, nothing accumulated from prior context. A value override modifies the input without restarting; Fork creates a parallel run from this checkpoint. This is data isolation as a debugging tool, not a convention.

---

### Figure 4 — The NormCode Ecosystem (Roles × Products × Lifecycle)

**Section:** §2 The NormCode Ecosystem
**Type:** Constructed diagram (draw.io, TikZ, or Figma — not a screenshot)
**Size:** Full column or half page; can be landscape orientation

**Design: Two-part diagram**

**Part A — Roles and Products (top half):**
Three columns, one per role, with product cards:

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  AGENT DESIGNER │  │ PRODUCT OPERATOR│  │    END USER     │
│Engineers & Devs │  │  Managers & Ops │  │ Domain Experts  │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│  📄 Language    │  │  🖥  Canvas App  │  │  📱 Clients     │
│  ⚙  Compiler   │  │  🗄  Server      │  │                 │
│  🤖 Agent       │  │                 │  │                 │
│  (Orchestrator) │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

Color: Designer column = blue tones, Operator column = purple tones, End User column = green tones (matching the website's role tab colors)

**Part B — Lifecycle (bottom half):**
Horizontal arrow flow, 6 steps:

```
[Describe] → [Compile] → [Review] → [Run] → [Modify] → [Deploy]
```

Under each step, one line of annotation:
- Describe: "Write `.ncds` plan or generate with AI"
- Compile: "4-phase pipeline → executable repositories"
- Review: "Domain expert reads `.ncn` — approves before run"
- Run: "Orchestrator executes; every step logged"
- Modify: "Override values; re-run only affected steps"
- Deploy: "`.ncds` file — Git, share, reuse, hand to any orchestrator"

Connect the lifecycle to roles with small vertical dotted lines:
- Designer owns Describe + Compile
- Operator owns Review + Run + Modify
- End User interacts during Run + receives Deploy output

**Caption draft:**
> Figure 4: The NormCode ecosystem. Three roles (Agent Designer, Product Operator, End User) map to six products across a six-step plan lifecycle. The `.ncds` file is the portable artifact connecting all roles — authored by the designer, reviewed and executed by the operator, and consumed as output by the end user.

---

## APPENDIX FIGURES (for extended version / supplementary material)

---

### Appendix Figure A — The Four-Phase Compilation Pipeline

**Type:** Flow diagram (constructed)
**Purpose:** Show how `.ncds` → `.ncd` → enriched `.ncd` → executable JSON transforms through 4 phases

**Design:**
Vertical pipeline with 4 boxes connected by arrows, each with an input/output label:

```
Natural Language Instruction
         ↓
┌──────────────────────────────────────┐
│  Phase 1: DERIVATION                 │
│  "What are we doing?"                │
│  → Identify concepts, operations,    │
│    dependencies, hierarchy           │
└──────────────────────────────────────┘
         ↓  .ncds (draft)
┌──────────────────────────────────────┐
│  Phase 2: FORMALIZATION              │
│  "In what order, which sequence?"    │
│  → Assign flow indices (1.2.3)       │
│  → Determine sequence types          │
│  → Generate .ncn companion           │
└──────────────────────────────────────┘
         ↓  .ncd + .ncn
┌──────────────────────────────────────┐
│  Phase 3: POST-FORMALIZATION         │
│  "How and with what resources?"      │
│  → Add paradigm IDs                  │
│  → Specify tool faculties            │
│  → Declare tensor axes and shapes    │
└──────────────────────────────────────┘
         ↓  enriched .ncd
┌──────────────────────────────────────┐
│  Phase 4: ACTIVATION                 │
│  "What does the orchestrator need?"  │
│  → Extract concept_repo.json         │
│  → Extract inference_repo.json       │
│  → Generate working_interpretation   │
└──────────────────────────────────────┘
         ↓
concept_repo.json + inference_repo.json
(loaded by Orchestrator)
```

On the right side of the diagram, add human review opportunities:
- After Phase 1: "✎ Review structure"
- After Phase 2: "✎ Read .ncn to verify logic"
- After Phase 3: "✎ Confirm resource assignments"

**Caption draft:**
> Appendix A: The four-phase compilation pipeline. Natural language intent is progressively formalized into executable JSON repositories. Human review is possible after each phase. The `.ncn` output from Phase 2 provides a plain-English narrative for domain expert verification.

---

### Appendix Figure B — Semantic vs. Syntactic Separation in a Plan Graph

**Type:** Constructed diagram (annotated plan graph)
**Purpose:** Visually demonstrate the cost and determinism separation — which nodes call LLMs and which don't

**Design:**
Show a small plan graph (6–8 nodes) with clear visual separation:

**Left side annotation:** "Syntactic operations — FREE, deterministic, never hallucinate"
- Grouping node (gray): "Collect inputs"
- Timing node (gray): "If condition met"
- Loop node (gray): "Iterate over documents"

**Center:**
Arrow connecting syntactic → semantic with label "Exactly the right data, nothing more"

**Right side annotation:** "Semantic operations — token cost, non-deterministic"
- Imperative node (purple): "Summarize document"
- Judgement node (purple, with truth badge): "Is quality sufficient?"

Add a cost bar at the bottom:
```
[=====SYNTACTIC: 0 tokens=====] [==SEMANTIC: ~800 tokens==]
```

With note: "In a typical plan, 60–70% of nodes are syntactic. Only 'thinking' steps invoke LLMs."

**Caption draft:**
> Appendix B: Semantic/syntactic separation in a NormCode plan. Syntactic operations (gray) handle all data routing, filtering, looping, and branching — deterministically, at zero token cost. Semantic operations (purple) invoke LLMs only for genuine reasoning tasks. This separation makes cost and failure attribution precise by construction.

---

### Appendix Figure C — The Code Assistant Plan Graph

**Type:** Screenshot (Canvas App)
**Purpose:** Show a more complex real-world plan to demonstrate expressive completeness

**What to capture:**
The Code Assistant plan's full inference graph loaded in Canvas (not executing — just the graph view before run). This plan has the Receive → Triage → Explore → Plan → Implement → Verify → Report structure.

**Required elements:**
- Full graph visible (zoom out enough to see all major stages)
- Stage labels readable (Receive, Triage, Explore, Plan, Implement, Verify, Report)
- Node color differentiation visible (semantic purple vs. data blue vs. syntactic gray)
- No execution state needed — pending gray is fine

**Callout annotations (3 callouts):**
1. → Top of graph: "7-stage software engineering workflow — ~40 inferences"
2. → Explore stage cluster: "Parallel file exploration — independent steps run simultaneously"
3. → Verify stage: "Judgement sequence — returns boolean; plan branches on result"

**Caption draft:**
> Appendix C: The NormCode Code Assistant plan — a production software engineering workflow with 7 stages and ~40 inferences. The plan receives a task, triages it, explores the codebase (parallel), generates an implementation plan, implements, verifies, and reports. Each stage is a sub-graph of inferences; the full plan is a single `.ncds` file.

---

### Appendix Figure D — Multi-Agent Configuration Panel

**Type:** Screenshot (Canvas App left panel, close-up)
**Purpose:** Show that different LLMs can be assigned to different steps

**What to capture:**
The Canvas App's agent configuration panel open, showing:
- 2–3 agent entries with different model names (e.g., `qwen-plus`, `gpt-4o`, `claude-3`)
- Pattern rules assigning specific flow index ranges to specific agents
- At least one "tool" listed per agent (e.g., `file_system`, `python_interpreter`)

**Caption draft:**
> Appendix D: Multi-agent configuration in Canvas. Different LLM models (e.g., qwen-plus for outline generation, gpt-4o for code generation) can be assigned to specific steps via pattern rules on flow indices. Each agent has its own tool body and paradigm directory, enabling heterogeneous agent plans within a single execution.

---

## HERO DIAGRAM (for paper title page / arXiv thumbnail / website)

**Not for the paper body — for promotional use**

**Type:** Constructed diagram (Figma or code-rendered SVG)
**Inspired by:** The website's `hero.html` visual

**Design:**
Three-panel flow:

```
[Natural Language Instruction]  →  [NormCode Plan (.ncds)]  →  [Execution Graph]
"Read file and create a report.      <- summary                  [graph visualization
 Summarize using report and           <= summarize findings        with nodes and
 a style guide."                      <- report                    edges running]
                                          <= :: read file
                                      <- style guide
```

Panel 1: A chat-bubble style box with the instruction in plain text
Panel 2: A code editor frame (dark bar with three dots) showing the `.ncds` syntax with syntax highlighting (`<-` in blue, `<=` in purple)
Panel 3: A mini inference graph showing the 4 nodes (read file → report → summarize → summary) with color coding

Label below the full diagram:
> "Write once. Compile. Inspect. Run. Own the plan."

---

## PRODUCTION NOTES

**Screenshot requirements:**
- Minimum resolution: 1920×1080 for Canvas App screenshots
- Must be captured from actual running Canvas App v1.1.3, not mockups
- Use a plan with meaningful node labels (not test data)
- Ensure no personal API keys, file paths, or sensitive data are visible
- Use a consistent LLM model name across all screenshots (suggest: `qwen-plus` or `claude-3-sonnet`)

**Diagram tool options:**
- Constructed diagrams (Fig 4, App A, App B, Hero): Figma, draw.io, or TikZ in LaTeX
- TikZ is preferred for camera-ready LaTeX submissions (no external file dependencies)
- draw.io/Figma exports as high-res PNG for initial drafts

**LaTeX figure sizing:**
- Main figures: `\begin{figure*}[t]` for full-width, `\begin{figure}[t]` for column-width
- Subfigures: `\begin{subfigure}[t]{0.48\textwidth}` for two-panel layouts
- Target font size in figures: ≥8pt when printed at full size (check at 100% zoom in PDF)

**Figure file naming convention:**
```
figures/
├── fig1_canvas_overview.png
├── fig2_ppt_lifecycle.png        (or split: fig2a_format.png + fig2b_graph.png)
├── fig3_breakpoint_debug.png
├── fig4_ecosystem_lifecycle.pdf  (vector for constructed diagram)
├── appA_compilation_pipeline.pdf
├── appB_semantic_syntactic.pdf
├── appC_code_assistant_graph.png
├── appD_multiagent_config.png
└── hero_three_panel.pdf
```

---

## PRIORITY ORDER FOR CREATION

| Priority | Figure | Blocker? |
|----------|--------|---------|
| 1 | Fig 1 — Canvas overview screenshot | Yes — needed for §3, most important figure |
| 2 | Fig 4 — Ecosystem + lifecycle diagram | Yes — needed for §2, sets up everything |
| 3 | Fig 3 — Breakpoint + tensor inspector | Yes — needed for §5 |
| 4 | Fig 2 — Format comparison + execution | Yes — needed for §4 |
| 5 | App A — Compilation pipeline | No — appendix |
| 6 | App C — Code assistant graph | No — appendix |
| 7 | App B — Semantic/syntactic separation | No — appendix |
| 8 | App D — Multi-agent config | No — appendix |
| 9 | Hero diagram | No — promotional |
