# Illustrations Plan — ICCBR 2026 Paper

**Paper:** "NormCode Canvas as a Case-Based Reasoning Development Platform for Large Language Model Agentic Workflows"
**Format:** LNCS, 14 pages, single-column, Deployed Applications track
**Figure budget:** 4 main-body figures (LNCS single-column; each figure ~half a page)

**Color convention (maintain across all figures — matches Canvas App):**
- Semantic nodes (Imperative / Judgement): `#c084fc` purple stroke, `#faf5ff` fill, hexagon shape
- Concept / data nodes: `#60a5fa` blue stroke, `#eff6ff` fill, rounded rectangle
- Syntactic nodes (Grouping / Timing / Looping): `#94a3b8` gray stroke, `#f8fafc` fill, rounded rectangle
- Status — completed: `#22c55e` green dot indicator
- Status — running: `#3b82f6` blue pulsing indicator
- Status — pending: `#9ca3af` gray indicator
- Status — failed: `#ef4444` red indicator
- Output node: `#ef4444` red outer ring on concept node
- Case base / abstract level: `#f59e0b` amber accent
- Background: white with subtle dot grid

---

## FIGURE 1 — The Two-Level CBR Architecture

**Section:** §4–§5 (the central theoretical contribution of the paper)
**Type:** Constructed diagram (TikZ or Figma → PDF; no screenshot)
**Size:** Full column width; ~1/2 page
**Purpose:** Communicate the paper's central claim in one figure — NormCode realizes
CBR at two levels simultaneously, with the compilation pipeline connecting them.

### Layout

Vertical split into three horizontal bands:

---

**Top band — Level 2: Abstract Cases (Plans)**

Labeled: `LEVEL 2 — Abstract Case Learning (across tasks)`

A row of 3–4 rectangular "plan" cards, each labeled with a production plan name:
```
[ PPT Generation Plan ]  [ Code Assistant Plan ]  [ BOM Matching Plan ]  [ … ]
```

Each card contains two small icons: `[IR]` (Inference Repository) + `[CR schema]` (Concept Repository schema).
Color accent: amber border to distinguish abstract case objects.

Below the row, label:
> "Level 2 case = NormCode runtime definition (plan)"

Arrow pointing down from one plan card, labeled:
> "Instantiate (run)"

---

**Middle band — Compilation Pipeline (two routes into Level 2)**

A horizontal arrow spanning the full width, with 4 phase labels above it:
```
Derivation → Formalization → Post-Formalization → Activation
```

Below the arrow, in smaller text:
> "→ compiled, executable plan (Level 2 case)"

**Two routes that produce Level 2 cases (show both):**
- **Route A — Distillation of experience:** Experience (from Level 1 runs, debugging, failures) → human author (revises/designs) → pipeline → new/revised plan. Dashed arrow from Level 1 up to pipeline; optional "human author" or "author + pipeline" label.
- **Route B — Direct compilation of mature rationale:** Mature rationale (e.g. clear task description, design doc) → pipeline (no prior runs required) → new plan. Arrow or label from left into pipeline: "Natural language / rationale → pipeline".

On the left side of the arrow, a curved upward arrow pointing back to Level 2, labeled:
> "Retain (revised plan)"

Annotation box below the pipeline:
> "The compilation pipeline is itself a NormCode plan (self-hosted — §8)"
The annotation box has a small "recursive" arrow indicating self-reference.

---

**Bottom band — Level 1: Concrete Cases (Runtime States)**

Labeled: `LEVEL 1 — Concrete Case Management (within a plan)`

Show a single plan execution as a horizontal sequence of checkpoint nodes:

```
[ node 1.1 ✓ ] →[ node 1.2 ✓ ] →[ node 1.3 ⏸ ] →[ node 1.4 … ] →[ node 1.5 … ]
```

Node `1.3` has a breakpoint badge. Below each completed node, a small "case" icon (cylinder = SQLite):
```
     ▣               ▣               ▣
[checkpoint]    [checkpoint]    [checkpoint]
```

Bracket below the row:
> "Level 1 case = suspended NormCode runtime (Blackboard + Concept Repository snapshot)"

On the right side, 4 CBR operation labels connected to relevant nodes with dotted arrows:
- **Retrieve** → points to node `1.3` (breakpoint): "Locate suspended runtime by (run_id, flow_index)"
- **Reuse (Fork)** → points to node `1.3` with a branching arrow: "Reinstantiate runtime as new execution"
- **Revise** → points to node `1.3` with a pencil icon: "Override tensor; mark downstream stale"
- **Retain** → points to the checkpoint cylinders: "Every completed node → new case in SQLite"

---

**Connecting arrows (causality):**
- **Down:** Thick arrow from Level 2 (a plan card) to Level 1 (the execution row): "Run (with input and environment) → generates Level 1 cases". Level 1 cases are created **only by execution**; they are not produced by the compilation pipeline.
- **Level 2 cases = two routes (both feed the pipeline; pipeline output = Level 2 case):**
  - **Route A — Distillation of experience:** Dashed arrow from Level 1 (experience from runs) to the pipeline. Label: "Experience → human author + pipeline → new/revised Level 2 case". Experience informs the author, who revises or designs; the pipeline compiles to a revised plan.
  - **Route B — Direct compilation of mature rationale:** Arrow or label from the left into the pipeline: "Mature rationale (task description, design) → pipeline → new Level 2 case". No prior runs required; direct compilation produces a new plan.
- Show pipeline output feeding back into the Level 2 row so **both routes** produce Level 2 cases.

**Caption:**
> **Fig. 1.** NormCode realizes CBR at two levels simultaneously. *Level 2*: A compiled NormCode plan is an abstract case — a runtime definition from which all executions of this type are instantiated. Level 2 cases arise from two routes: (A) distillation of experience (experience → human author + pipeline → new/revised plan) and (B) direct compilation of mature rationale (rationale → pipeline → new plan). The compilation pipeline (Derivation → Formalization → Post-Formalization → Activation) is itself a NormCode plan (self-hosted). *Level 1*: Each execution checkpoint is a concrete case — a suspended runtime state (Blackboard + Concept Repository snapshot) persisted in SQLite. The four CBR operations map directly onto Canvas operations at this level.

---

## FIGURE 2 — NormCode Syntax: Scope Rule and Case Isolation

**Section:** §3 (NormCode as a Reasoning Medium)
**Type:** Constructed diagram — annotated code block + isolation boundary illustration
**Size:** Full column width; ~1/3 page
**Purpose:** Show how the three markers plus indentation (scope rule) produce isolated
tensors, which is the enabling condition for reliable Level 1 cases.

**Grammar (match paper §3 and docs):** Three markers are `<-` (Value Concept), `<=` (Functional Concept), `<*` (Context Concept). Use ASCII `<-` and `<=` in the figure. The paper's example does not use `::`; keep the code block identical to §3.

### Layout

**Left half — Annotated `.ncds` example:**

A code block (light gray background, monospace font) showing the same fragment as in §3:

```
<- summary
    <= summarize the findings
    <- report
        <= read the uploaded file
        <- source_doc
    <- style_guide
```

Callout annotations connected with thin arrows:
- `<-` symbol: "Value Concept — data (inputs/outputs) flowing between steps"
- `<=` symbol: "Functional Concept — operation that derives its parent from declared inputs"
- Indentation block under `<- report`: "Scope block — inference for `report` can access only `source_doc`"
- `<- summary` at top level: "Flow index 1 — `summary` can access only `report` (1.2) and `style_guide` (1.3)"
- Do not add a `::` callout; syntactic operators ($, &, @, *) are described elsewhere in §3.

**Right half — Isolation boundary / data-flow diagram:**

Runtime dependency implied by the scope rule (multiple concepts, not literally two nodes):
```
[source_doc ✓] ──→ [ report ✓ ]
                         │
                   ┌─────┴──────┐
                   │  Tensor:   │
                   │  {report}  │
                   │  ← only    │
                   │  source_doc│
                   └────────────┘
                         │
[style_guide ✓] ─────→ [ summary ]
                         │
                   ┌─────┴──────────────┐
                   │  Tensor:           │
                   │  {summary}         │
                   │  ← only report     │
                   │    + style_guide   │
                   └────────────────────┘
```

Above the diagram: "Compiler verifies: no step can reference data outside its scope block"
Below: "Each completed node's tensor = self-contained case object"

Highlight box (amber): "No hidden data in execution — if a step needs data not in its scope, the plan must be revised to declare it explicitly"

**Caption:**
> **Fig. 2.** NormCode's scope rule as the enabling condition for Level 1 case integrity. Left: Three markers (`<-`, `<=`, `<*`) and indentation constitute the syntax; the scope block under each concept declaration specifies exactly which concepts that step receives. Right: The resulting runtime structure — the orchestrator constructs each step's input from only its declared references, so no hidden data enters execution. If a step needs data not in its scope, the plan must be revised to declare it explicitly. This structural isolation makes every checkpoint a self-contained, retrievable case.

---

## FIGURE 3 — Canvas App: The CBR Interface

**Section:** §6 (The Canvas App)
**Type:** Screenshot with annotation overlays (callout boxes + arrows)
**Size:** Full column width; ~1/2 page
**Purpose:** Show the deployed system and map every visible UI element to a CBR operation.
The figure must make the CBR mapping visceral — this is not a UI tour, it is evidence
that the CBR cycle is operational.

### What to capture

Canvas App in **breakpoint-paused state** during a Code Assistant run.
- Several nodes completed (green), one paused at a breakpoint (blue with badge)
- Tensor Inspector open in right panel showing real data (bounded inputs to the paused node)
- Checkpoint Panel / run history visible (even as a small sidebar or dropdown)
- Fork button visible in top controls

**Required elements visible:**
- Graph center: ≥8 nodes, mix of purple/blue/gray, completed green nodes, one paused node with breakpoint badge and flow index label (e.g., `1.3.2`)
- Right panel: Tensor Inspector open with at least 3 rows of data visible, axis label visible
- Top controls: Fork button and Value Override option visible
- Either sidebar or panel showing previous run history / checkpoint list

**Callout annotations (6, mapped to CBR operations):**

1. → SQLite icon or checkpoint panel: **"Case Base — SQLite store of all completed node tensors across all runs"**
2. → Paused node + Tensor Inspector: **"Retrieve — locate suspended runtime by (run_id, flow_index); inspect bounded inputs"** *(C1: O(1) operations)*
3. → Value override field or pencil icon near paused node: **"Revise — override tensor; scope rule determines exact stale boundary"** *(C3: scope-bounded re-run)*
4. → Fork button: **"Reuse — reinstantiate suspended runtime as new execution; no upstream re-run"**
5. → Green completed nodes + checkpoint icons: **"Retain — every completed node writes a case automatically"**
6. → `.ncn` review badge or file tab (if visible): **"C2 — plain-English plan narrative available before any LLM call"**

**Caption:**
> **Fig. 3.** NormCode Canvas (v1.1.3) as a CBR interface. Every UI element maps to a CBR operation: the checkpoint store (SQLite) is the case base; the Tensor Inspector realizes Retrieve by exposing the exact bounded inputs of any node in O(1) operations (C1); Value Override realizes Revise with automatic stale-boundary computation (C3); Fork realizes Reuse by reinstantiating a suspended runtime without upstream re-execution; automatic checkpointing realizes Retain. The `.ncn` pre-execution narrative (not shown) provides zero-cost human review before any LLM call (C2).

---

## FIGURE 4 — Case Study: The Retrieve–Revise Cycle

**Section:** §7 (Case Studies — Code Assistant)
**Type:** Multi-panel constructed diagram OR annotated screenshot sequence
**Size:** Full column width; ~1/3–1/2 page
**Purpose:** Show the complete CBR retrieve–revise cycle in a concrete production
scenario — the Code Assistant debugging session. This is the empirical evidence for C1 and C3.

### Layout Option A: Three-panel sequence (preferred — no screenshot dependency)

**Panel 1 — Retrieve:**
```
Run history:
  run_042  [node 1.1 ✓][node 1.2 ✓][node 1.3 ✗]  ← FAILED
                                          │
                              Breakpoint at 1.3
                              Tensor Inspector:
                              ┌──────────────────┐
                              │ input: file_list │
                              │ [a.py, b.py, c.py│
                              │  wrong_dir/]     │
                              └──────────────────┘
                              ↑ cause identified
```
Label above: **"Retrieve — locate run_042 checkpoint at node 1.3; inspect bounded inputs in 2 clicks (C1)"**

**Panel 2 — Revise:**
```
Override tensor at 1.3:
  file_list ← [a.py, b.py, c.py]  (removed wrong_dir/)

  Stale boundary (computed by scope rule):
  [node 1.3] [node 1.4] [node 1.5]  ← re-execute
  [node 1.1] [node 1.2]             ← preserved from cache (C3)
```
Label above: **"Revise — override file_list; only 3 of 40 nodes re-run (C3)"**

**Panel 3 — Reuse + Retain:**
```
Fork → run_043:
  [node 1.1 ✓ cached][node 1.2 ✓ cached][node 1.3 ✓ new]
                                          [node 1.4 ✓ new]
                                          [node 1.5 ✓ new]

New cases added to case base:
  run_043 / node 1.3  ←  revised file_list
  run_043 / node 1.4  ←  downstream result
  run_043 / node 1.5  ←  final output
```
Label above: **"Reuse (Fork) + Retain — corrected run produces new cases; upstream cached"**

Below all three panels, a horizontal arrow labeled:
> "Total: 1 breakpoint + 2 clicks to identify cause (C1); 3 of 40 inferences re-executed (C3)"

### Layout Option B: Screenshots (if Canvas App can be captured in these states)

Two screenshots side by side:
- Left: Breakpoint inspection — Tensor Inspector showing the wrong file path
- Right: Post-fork execution — upstream nodes green-cached, downstream nodes green-new

**Caption:**
> **Fig. 4.** The retrieve–revise cycle in the Code Assistant case study (§7.2). *Retrieve*: a failed run (run\_042) is located at the node where file discovery failed; the Tensor Inspector shows the exact bounded inputs in two clicks — no log reconstruction (C1). *Revise*: the incorrect file path is overridden; the scope rule computes the exact stale boundary (3 nodes downstream of the correction). *Reuse (Fork) + Retain*: a new run (run\_043) preserves the 37 upstream nodes from cache, re-executes only the 3 stale nodes, and deposits new cases in the case base. Total re-execution: 7.5\% of the plan.

---

## GAPS AND ATTRACTIVITY IMPROVEMENTS

**Assessment:** The current plan covers the two-level CBR story, scope rule, one Canvas screenshot, and the retrieve–revise case study. To improve clarity and attractivity, three additions are recommended:

### 1. Overall ecosystem / pipeline diagram (currently lacking)

**Gap:** Fig. 1 explains *what* NormCode does (two-level CBR) but not *where* it sits: author → compiler → runtime → case base, or how it differs from LangChain/LangGraph (structural isolation as differentiator).

**Recommendation:** Add one of the following (within or beyond the 4-figure budget):
- **Option A — Full pipeline (authoring → execution):** One diagram showing: `.ncds` authoring → Compilation (4 phases) → Orchestrator + Canvas → SQLite case base. Positions NormCode as a full stack, not just “CBR layer.” Place in §1 or §3; can be small (e.g. ~1/4 page) or supplementary.
- **Option B — Ecosystem positioning:** NormCode vs. typical LLM stacks: “Conversation history / shared state” vs. “Scope-verified, checkpoint = case.” Helps readers from the LLM-tooling community see the value proposition in one glance.
- **Priority:** High for attractivity; Option A is more informative for a Deployed Applications paper. If figure budget is tight, make this **Supp. Figure D — NormCode pipeline (authoring to execution)** and reference it in the introduction.

### 2. Additional Canvas app snapshots

**Current:** Fig. 3 is one annotated screenshot (breakpoint + Tensor Inspector + controls). Sufficient for “CBR interface exists,” but the paper would feel more concrete with more evidence of the *deployed* system.

**Recommendation:**
- **Fig. 3 as two-panel:** Panel A = current plan (breakpoint + Tensor Inspector); Panel B = second state: e.g. Run History / checkpoint list, or the **.ncn Review Panel** (C2). Same figure, two snapshots → stronger “this is a real tool” impression.
- **Optional second figure or in-text thumbnail:** One small screenshot in §6 or §7 showing a different plan (e.g. PPT Generation) or the plan selector, to show generality without a full extra figure.
- **Checklist for any Canvas screenshot:** Graph with ≥8 nodes, Tensor Inspector with real data, one of [Fork | Value Override | Run History | .ncn panel] visible; no API keys or sensitive paths.

### 3. NormCode code-block artifacts (elevate and unify)

**Current:** Snippets appear as inline `lstlisting` in §3, §5, §7, and appendix; only the appendix uses a caption. Fig. 2 includes an annotated code block as part of a constructed diagram. There is no unified “artifact” look or citable listings.

**Recommendation:**
- **Unified listing style:** In `main.tex` (or a shared snippet style), define a consistent look for all NormCode: same font, background, border; optional thin “artifact bar” with filename (e.g. `plan.ncds`, `output.ncn`) so it reads as real artifacts, not ad-hoc examples.
- **1–2 key snippets as captioned listings:** Promote the minimal scope-rule example (§3) and optionally one .ncn excerpt to `\begin{lstlisting}[caption={...}, label=lst:...]` so they are “Listing 1”, “Listing 2” and can be cited. Improves traceability and looks intentional.
- **Optional “artifact strip”:** For the main .ncds example, add a one-line header inside or above the block, e.g. `┌─ plan.ncds ─────────────────────┐`, so the paper clearly presents *artifacts* of the system.
- **Do not duplicate Fig. 2:** The annotated code in Fig. 2 stays as the main *explained* example; the in-text listings are the *reference* versions. Keep wording and symbols consistent between Fig. 2 and Listing 1 so they reinforce each other.

**Summary:** Adding (1) one ecosystem/pipeline diagram, (2) a second Canvas snapshot (e.g. as second panel in Fig. 3), and (3) a unified, captioned treatment of NormCode snippets will improve both understanding and the perceived quality of the paper without overloading the figure budget.

---

## FIGURE PRIORITY AND SECTION DEPENDENCIES

| Priority | Figure | Paper section | Blocker? | Creation method |
|----------|--------|---------------|----------|-----------------|
| **1** | Fig. 1 — Two-Level CBR Architecture | §4–§5 (theoretical core) | Yes — the paper's central claim | Constructed: TikZ or Figma |
| **2** | Fig. 3 — Canvas App CBR Interface | §6 (deployed system) | Yes — deployed applications evidence | Screenshot + callout overlays |
| **3** | Fig. 4 — Retrieve–Revise Cycle | §7 (case studies) | Yes — C1 and C3 evidence | Constructed (preferred) or screenshots |
| **4** | Fig. 2 — Syntax + Scope Rule | §3 (NormCode background) | Yes — isolation enabling condition | Constructed: annotated code block |

---

## OPTIONAL / SUPPLEMENTARY FIGURES

These are not required for the 14-page submission but strengthen specific claims:

### Supp. Figure A — The Six-Property Table (as a visual, not prose)

A 2×3 grid of property cards, each with:
- Property name (bold)
- One-line implementation in NormCode
- One-line failure mode in tools without this property

| Card | Property | NormCode realization | Failure without it |
|------|----------|---------------------|--------------------|
| 1 | Interpretable | `.ncn` plain-prose output | Plans locked in code |
| 2 | Enforceable | Compiler verifies scope; orchestrator enforces | Review ≠ what runs |
| 3 | Composable | 3 symbols × 1 scope rule; unlimited depth | Breaks at scale |
| 4 | Locally Addressable | Flow indices + scope = per-step isolation | O(k) debugging |
| 5 | Generalizable | Same primitives: PPT, code, BOM, medical | Domain-specific DSLs |
| 6 | Portable | Plain text `.ncds`; any compliant orchestrator | Platform lock-in |

### Supp. Figure B — Compilation Pipeline as Level 2 Distillation

The four-phase pipeline (Derivation → Formalization → Post-Formalization → Activation)
annotated to show:
- Input: natural language task description
- Output: compiled runtime definition (Level 2 case)
- Each phase: what structure is extracted
- Review points: where human verification occurs (`.ncn` after Phase 2)
- Self-hosting annotation: "This pipeline is itself a NormCode plan"

### Supp. Figure C — The Six Production Plans (Scale Evidence)

A table/visual showing the six production plans:

| Plan | Inferences | Syntactic % | LLM cost (tokens/run) | Domain |
|------|-----------|-------------|----------------------|--------|
| PPT Generation | ~25 | 65% | ~3,200 | Presentation |
| Code Assistant | ~40 | 70% | ~8,500 | Software dev |
| BOM Matching | ~20 | 60% | ~2,100 | Manufacturing |
| Model Report | ~18 | 65% | ~1,800 | Analytics |
| [Plan 5] | … | … | … | … |
| [Plan 6] | … | … | … | … |

*(Fill actual numbers from production data before camera-ready)*

### Supp. Figure D — NormCode ecosystem / pipeline (authoring → execution)

**Purpose:** One-page clarity on where NormCode sits: full path from authoring to execution and case base.

**Content (choose one focus):**
- **Pipeline:** `.ncds` → Derivation → Formalization → Post-Formalization → Activation → Orchestrator + Canvas → SQLite. Optional: annotate “.ncn review” after Formalization, “Level 2 case” = compiled plan, “Level 1 cases” = checkpoints.
- **Positioning:** Contrast box “Typical LLM stack (shared state, implicit context)” vs. “NormCode (scope-verified, checkpoint = self-contained case).”

Reference in §1 or §3; use as supplementary if main figure budget is full.

---

## PRODUCTION NOTES

**Screenshot requirements (for Fig. 3 and optional Fig. 4B):**
- Resolution: 1920×1080 minimum
- Must be captured from actual Canvas App v1.1.3, not mockups
- Use Code Assistant plan for Fig. 3 (most nodes, clearest CBR cycle demonstration)
- Ensure no API keys, personal file paths, or sensitive output data visible
- Consistent model name across all screenshots (e.g., `qwen-plus`)

**Constructed diagram tools:**
- **TikZ (preferred for camera-ready):** No external file dependencies; fonts match paper
- **Figma/draw.io:** Acceptable for drafts; export as high-res PDF for LNCS submission
- Fig. 1 (Two-Level Architecture): Most complex — start early; allow revision time
- Fig. 4 (Retrieve–Revise): Option A (constructed) is preferred because it is cleaner and does not depend on capturing the exact Canvas state

**LNCS single-column sizing:**
- Full column width: `\begin{figure}[t]` with `\includegraphics[width=\linewidth]{...}`
- Two-panel (Fig. 4): `\begin{subfigure}[t]{0.48\linewidth}` × 2
- Target: figures readable at 100% zoom in single-column PDF; minimum font size 8pt
- LNCS page width ≈ 12.2 cm; plan figure heights so total figure + caption ≤ 6 cm

**Listings / code artifacts:**
- Define a custom `lstdefinestyle` or use consistent `lstset` for all NormCode (e.g. `language=`, `basicstyle=`, `backgroundcolor=`, `frame=`) so every `.ncds` / `.ncn` block matches.
- Add `caption=` and `label=lst:...` to at least the minimal scope-rule example in §3 and, if space, one `.ncn` block; cite as “Listing 1” in text.
- Optional: use a listings “title” or a one-line comment inside the block to show filename (e.g. `% plan.ncds`) for an artifact feel.

**File naming convention:**
```
iccbr_paper/figures/
├── fig1_two_level_cbr.pdf        (constructed — vector)
├── fig2_scope_rule_isolation.pdf (constructed — vector)
├── fig3_canvas_cbr_interface.png (screenshot + overlays; consider fig3a_*.png, fig3b_*.png if two-panel)
├── fig4_retrieve_revise_cycle.pdf (constructed — vector, preferred)
│   fig4_retrieve_revise_cycle.png (screenshot alternative, if used)
├── suppA_six_properties.pdf
├── suppB_compilation_pipeline.pdf
├── suppC_production_plans.pdf
└── suppD_ecosystem_pipeline.pdf  (optional — authoring → execution or positioning)
```

---

## CBR LABEL GLOSSARY (for consistency across all figures)

Use these exact labels whenever a CBR operation is named in a figure:

| Operation | Canvas UI element | Figure label text |
|-----------|-------------------|-------------------|
| Case | Checkpoint at any completed node | "Case = suspended runtime (run_id, flow_index)" |
| Case Base | SQLite checkpoint store | "Case Base — SQLite; grows on every completed node" |
| Retrieve | Breakpoint → Tensor Inspector | "Retrieve — locate by (run_id, flow_index); inspect bounded inputs" |
| Reuse | Fork button | "Reuse (Fork) — reinstantiate suspended runtime" |
| Revise | Value Override | "Revise — override tensor; stale boundary by scope rule" |
| Retain | Automatic checkpointing | "Retain — every completed node writes a case" |
| Level 1 case | Node checkpoint | "Concrete case = suspended NormCode runtime" |
| Level 2 case | Compiled plan (.ncds) | "Abstract case = NormCode runtime definition" |
| Distillation | Compilation pipeline | "Distillation = Derivation → Formalization → Post-Formalization → Activation" |
