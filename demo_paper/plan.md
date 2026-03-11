# NormCode Demo Paper — Plan

**Type:** System Demonstration Paper
**Target length:** 6 pages (ACL/EMNLP System Demonstrations format, or equivalent)
**Companion paper:** "NormCode: A Semi-Formal Language for Context-Isolated AI Planning" (full paper, arXiv:2512.10563)

---

## Core Argument

Existing tools for building AI agent workflows force a choice between three imperfect options — raw LLMs (opaque, model-specific), code frameworks (developers only), and no-code platforms (doesn't scale). A **working language** fills the gap: learn it once, describe any workflow, own the plan as a portable artifact.

This paper demonstrates that NormCode is that language — not as a proposal, but as a working system. The Canvas App (v1.1.3) provides a full visual environment for authoring, executing, debugging, and modifying NormCode plans. Six production-quality built-in plans (PPT generator, Code Assistant, meta-compiler, and others) demonstrate real-world complexity.

The contribution of this paper over the full paper is **evidence**: screenshots, scenarios, and a live URL, not arguments.

---

## Section Structure

### Abstract (~150 words)
- The three-tool gap in one sentence
- NormCode as the working language filling it
- What the demo shows: Canvas App v1.1.3, two scenarios (PPT Agent end-to-end; Debug and Fork)
- Live URL

---

### 1. Introduction (~0.5 pages)

**Story:** A practitioner wants to build a multi-step AI agent workflow. They face the three-tool landscape. None of the options gives them a plan they can inspect, share, run again, or hand to a colleague. NormCode does.

**Contents:**
- Three-tool gap (3 sentences: Raw AI / Code Frameworks / No-Code UIs)
- "Only a language can be learned" — the SQL analogy
- What this paper covers: the Canvas App as the primary interface, two demo scenarios, live web demo
- Pointer to full paper for formal language specification

---

### 2. The NormCode Ecosystem (~1.0 pages)

**Story:** Before showing the demo, orient the reader on what NormCode is as a system — not just the language, but the full stack of products and the roles they serve.

**Contents:**

**2.1 Three Roles, Six Products**
Table or visual showing:

| Role | Products | What they do |
|------|----------|-------------|
| Agent Designer | Language + Compiler + Agent (Orchestrator) | Write plans, compile to executable, run |
| Product Operator | Canvas App + Server | Debug, inspect, manage, collaborate |
| End User | Clients | Interact via purpose-built interfaces |

**2.2 The Plan Lifecycle**
The 6-step lifecycle as a horizontal diagram:
`Describe → Compile → Review → Run → Modify → Deploy`
Each step annotated with what happens and who does it.

**2.3 The Language in Brief**
Three symbols + one code example (the summary workflow from the full paper):
```
<- summary
    <= summarize the findings
    <- report
        <= :: read the uploaded file
    <- style guide
```
- `<-` is data, `<=` is action, `<*` is loop/state
- Indentation = scope (each step sees only what's inside its indent)
- One inline note about flow indices (1.1, 1.1.2, etc.) enabling precise addressability
- *"Full grammar and type system in [FULL PAPER]"*

---

### 3. The Canvas App (~0.75 pages)

**Story:** The Canvas App is the primary interface for Product Operators — the environment where NormCode plans become visible, executable, and debuggable.

**Contents:**

**3.1 Overview**
Four capability phases (all production-ready at v1.1.3):
1. **Graph View** — Inference graph rendered before execution; semantic nodes (purple hexagons) vs. syntactic nodes (gray); data nodes (blue rectangles)
2. **Real-Time Execution** — WebSocket-streamed status updates; node indicators: pending (gray) → running (blue pulsing) → completed (green) → failed (red) → skipped (striped)
3. **Breakpoint Debugging** — Pause at any flow index; step-by-step advancement; tensor inspector for N-dimensional data (table / list / JSON view)
4. **Modification** — Override a value at a breakpoint; selective re-run of only affected steps; fork from any checkpoint

**3.2 Architecture (one paragraph)**
- Frontend: React 18 + TypeScript + React Flow + Zustand + TailwindCSS
- Backend: FastAPI + Python 3.11 + SQLite + WebSockets
- Communication: REST for control, WebSockets for real-time event streaming
- Plans loaded as `concept_repo.json` + `inference_repo.json` (output of the 4-phase compiler)

**Figure 1:** Annotated Canvas App screenshot
Label: graph center (semantic vs. syntactic coloring, node status), left panel (agent config + live tool call log), right panel (tensor inspector with data visible), execution controls (Run / Pause / Step / Fork)

---

### 4. Demo Scenario A: PPT Agent — Full Lifecycle (~1.25 pages)

**Story:** A user asks NormCode to build a presentation on a given topic. We follow the plan from natural language instruction all the way to rendered output, using every lifecycle stage.

**The plan:** `ppt_generation.ncds` — takes a topic, runs outline generation + slide writing loops + HTML rendering. ~30 inferences, 6 slide layouts, 14 component types.

**Walkthrough:**

**Step 1 — Describe (write the plan)**
Show a fragment of the `.ncds` file: the outer loop structure, one slide-generation inference. Emphasize: written in near-natural language, no programming expertise required.

**Step 2 — Compile + Review**
Show the corresponding `.ncn` (natural language) output for the same fragment:
> "(OUTPUT) Slide 3 — Introduction
> (ACTION) is obtained by generating slide content
> (INPUT) using the outline and style guide."

This is what a domain expert reads to verify the plan before it runs. No syntax knowledge needed.

**Step 3 — Run (Canvas execution)**
Figure 2: The running graph — outer loop unfolding, completed slides turning green, current slide blue-pulsing, semantic nodes visually distinct from syntactic routing.

**Step 4 — Output**
The rendered HTML preview of the presentation, plus the `.pptx` file path returned by the final output node.

**What this demonstrates:**
- The full Describe → Compile → Review → Run → Deploy lifecycle in one scenario
- `.ncn` as the human verification layer before execution
- Data isolation: each slide inference sees only its own outline section, not the full document
- Semantic/syntactic separation visible in the graph coloring

---

### 5. Demo Scenario B: Debug and Fork (~1.25 pages)

**Story:** Something goes wrong mid-execution. We show how NormCode's enforced data isolation makes the failure immediately localizable, how the tensor inspector shows exactly what a step saw, how a value can be overridden without restarting, and how a fork lets you explore an alternative path.

**The scenario:** Using the Code Assistant plan. A step that generates code receives an ambiguous context. We set a breakpoint, inspect, override, and fork.

**Walkthrough:**

**Step 1 — Set a breakpoint**
In Canvas, right-click on node `1.3.2` (the "Plan implementation" step). Execution pauses before the step runs. The node turns blue with a breakpoint indicator.

**Step 2 — Inspect the tensor**
Open the tensor inspector on node `1.3.1` (the "Explore codebase" output). Show the N-dimensional view: axis `[file]` with 12 entries, each a perceptual sign pointing to a file. The exact inputs for the next step are visible and bounded — nothing more, nothing less.

**Step 3 — Override a value**
The user determines that the explore output missed a key file. They override the reference at `1.3.1` to add the missing file path. No restart required.

**Step 4 — Resume and fork**
Resume execution from the breakpoint with the modified value. After the run completes, use "Fork from checkpoint" at `1.3.1` to create a parallel run with the original (unmodified) value for comparison.

**Figure 3:** Breakpoint state — paused node, tensor inspector open with data visible, value override input active

**What this demonstrates:**
- Input auditability: "what exactly did step 1.3.2 see?" — answered instantly
- Bounded debuggability: the failure is localized because context is isolated by design
- Modification without restart: selective re-run from the override point only
- Fork as experimental branching (git-like workflow for agent runs)

---

### 6. Live Web Demo (~0.25 pages)

**Contents:**
- Live URL and QR code
- What users can do: enter a topic → PPT Agent runs → download slides
- The web demo uses the same NormCode plan and orchestrator as the Canvas App — not a simplified mock
- Also available: Canvas App (Windows alpha download) + portable example project

---

### 7. Related Work (~0.5 pages)

Focus: visual and debugging tools for LLM workflows. Keep citations tight.

| Tool | What it does | What NormCode adds |
|------|-------------|-------------------|
| **LangFlow** | Visual drag-and-drop builder for LangChain flows | NormCode plans are text files (portable, git-able); LangFlow flows are platform-locked UI graphs |
| **LangSmith** | Tracing and debugging for LangChain runs | NormCode isolates data *by construction*, not by post-hoc logging; tensor inspector shows structured data, not raw prompt strings |
| **PromptFlow (Azure)** | DAG-based workflow tool with UI | NormCode separates semantic from syntactic operations (cost visibility); supports value override and forking, not just replay |
| **Flowise** | No-code LLM app builder | Same portability limitation as LangFlow; NormCode's `.ncn` format enables non-technical review before execution |

Key differentiator sentence: NormCode is the only tool where the plan itself — not the tooling around it — enforces data isolation, making debugging a property of the language rather than a feature of the debugger.

---

### 8. Conclusion (~0.1 pages)

- NormCode Canvas v1.1.3 demonstrates a working language for AI agent workflows: learn once, write any workflow, own the artifact
- The two demo scenarios show the full lifecycle (Scenario A) and the core debuggability claim (Scenario B)
- Live demo: [URL]
- Full language specification: arXiv:2512.10563

---

## Figures Summary

| # | Content | Section |
|---|---------|---------|
| Fig 1 | Canvas App annotated screenshot (graph + panels) | §3 |
| Fig 2 | PPT Agent execution graph mid-run | §4 |
| Fig 3 | Breakpoint + tensor inspector + value override | §5 |
| Fig 4 (if space) | Ecosystem table or lifecycle diagram | §2 |

---

## Writing Notes

- **Tone:** Practitioner-facing, concrete, present-tense ("the user sets a breakpoint", not "one could set")
- **No equations** — save those for the full paper
- **Every claim has a figure** — if you can't show it, cut it
- **Code blocks** only for the `.ncds` example in §2.3 and the `.ncn` review in §4 — keep them short (≤8 lines each)
- **Pointer discipline:** "see [FULL PAPER] for formal details" appears in §2.3 and §3.1 only — not repeatedly
- **The `.ncn` format is the secret weapon** — it's the most underappreciated feature and the clearest differentiator from every visual tool competitor. Make §4 Step 2 hit hard.

---

## Files to Create

```
demo_paper/
├── plan.md              ← this file
├── main.tex             ← root LaTeX document
├── sections/
│   ├── abstract.tex
│   ├── 01_introduction.tex
│   ├── 02_ecosystem.tex
│   ├── 03_canvas.tex
│   ├── 04_scenario_ppt.tex
│   ├── 05_scenario_debug.tex
│   ├── 06_web_demo.tex
│   ├── 07_related_work.tex
│   └── 08_conclusion.tex
└── figures/
    ├── fig1_canvas_annotated.png    ← to be added
    ├── fig2_ppt_execution.png       ← to be added
    └── fig3_breakpoint_inspect.png  ← to be added
```

---

## Open Questions (to resolve before writing)

1. **Target venue** — ACL System Demonstrations? EMNLP? AAAI? arXiv preprint only? This determines the LaTeX template and page format.
2. **Primary demo scenario** — PPT Agent is confirmed for Scenario A. For Scenario B (Debug), should it use the Code Assistant plan or stay with the PPT Agent to keep a single narrative thread?
3. **Live URL** — Is the web demo at a stable public URL? Needs to be confirmed before submission.
4. **Figures** — Screenshots need to be taken from the actual Canvas App. Which run/plan should be captured?
