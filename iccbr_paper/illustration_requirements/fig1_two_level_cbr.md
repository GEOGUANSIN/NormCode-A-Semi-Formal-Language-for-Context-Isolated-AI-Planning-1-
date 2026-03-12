# Fig 1 — Two-Level CBR Architecture

**ID:** fig1  
**Output:** `figures/fig1_two_level_cbr.pdf`  
**Section:** §4–§5  
**Creation method:** Constructed (TikZ or Figma → PDF; no screenshot)  
**Needs multi-model LLM:** **Yes** — diagram generation from this spec (text → TikZ / Figma / SVG).

---

## Purpose

Communicate in one figure: NormCode realizes CBR at two levels simultaneously, with the compilation pipeline connecting them.

## Size

Full column width; ~1/2 page. LNCS single-column.

## Layout (three horizontal bands, top to bottom)

### Top band — Level 2: Abstract Cases (Plans)

- Label: `LEVEL 2 — Abstract Case Learning (across tasks)`.
- Row of 3–4 rectangular plan cards: `[ PPT Generation Plan ]` `[ Code Assistant Plan ]` `[ BOM Matching Plan ]` `[ … ]`.
- Each card: two small icons `[IR]` (Inference Repository) + `[CR schema]` (Concept Repository schema).
- Color: amber border (abstract case objects).
- Below row: *"Level 2 case = NormCode runtime definition (plan)"*.
- Arrow down from one plan card, label: *"Instantiate (run)"*.

### Middle band — Compilation Pipeline (two routes into Level 2)

- Horizontal arrow full width; above it four phase labels:  
  `Derivation → Formalization → Post-Formalization → Activation`.
- Below arrow (smaller text): *"→ compiled, executable plan (Level 2 case)"*.
- **Two routes that produce Level 2 cases (show both):**
  - **Route A — Distillation of experience:** Experience (from Level 1 runs, debugging, failures) → **human author** (revises/designs) → pipeline → new/revised plan. (Dashed arrow from Level 1 up to pipeline; optional “human author” or “author + pipeline” label.)
  - **Route B — Direct compilation of mature rationale:** Mature rationale (e.g. clear task description, design doc) → pipeline (no prior runs required) → new plan. (Arrow or label from left into pipeline: “Natural language / rationale → pipeline”.)
- Left: curved upward arrow from pipeline back to Level 2, label: *"Retain (revised plan)"*.
- Annotation below: *"The compilation pipeline is itself a NormCode plan (self-hosted — §8)"* with small recursive arrow.

### Bottom band — Level 1: Concrete Cases (Runtime States)

- Label: `LEVEL 1 — Concrete Case Management (within a plan)`.
- Clarification: Level 1 cases are created **only by execution** (a run with a specific input and environment); they are **not** produced by the compilation/distillation pipeline (that pipeline produces Level 2 cases).
- One plan execution as horizontal sequence:  
  `[ node 1.1 ✓ ] → [ node 1.2 ✓ ] → [ node 1.3 ⏸ ] → [ node 1.4 … ] → [ node 1.5 … ]`.  
  Node 1.3 has breakpoint badge.
- Below completed nodes: small case icon (cylinder = SQLite): checkpoint, checkpoint, checkpoint.
- Bracket below: *"Level 1 case = suspended NormCode runtime (Blackboard + Concept Repository snapshot)"*.
- Right: four CBR labels with dotted arrows to nodes:
  - **Retrieve** → node 1.3: "Locate suspended runtime by (run_id, flow_index)"
  - **Reuse (Fork)** → node 1.3, branching arrow: "Reinstantiate runtime as new execution"
  - **Revise** → node 1.3, pencil: "Override tensor; mark downstream stale"
  - **Retain** → checkpoint cylinders: "Every completed node → new case in SQLite"

### Connecting arrows (causality — do not invert)

- **Down (Level 2 → Level 1):** Thick arrow from one plan card down to the execution row. Label: *"Run (with input and environment) → generates Level 1 cases"*. Level 1 cases are created **only** by execution: each run with a given input and environment produces checkpoints (suspended runtimes) at completed nodes; no Level 1 case comes from the compilation pipeline.
- **Level 2 cases = two routes (both feed the pipeline; pipeline output = Level 2 case):**
  - **Route A — Distillation of experience:** Dashed arrow from Level 1 (experience from runs) **to** the compilation pipeline. Label: *"Experience (from runs) → human author + pipeline → **new Level 2 case**"*. Experience informs the author, who revises or designs; the pipeline compiles to a revised plan.
  - **Route B — Direct compilation of mature rationale:** Arrow or label from the left into the pipeline: *"Mature rationale (task description, design) → pipeline → new Level 2 case"*. No prior runs required; direct compilation produces a new plan.
- Show pipeline output feeding back into the Level 2 row (e.g. “revised plan” card or the existing “Retain (revised plan)” curved arrow on the left), so **both routes** produce Level 2 cases.

## Caption

**Fig. 1.** NormCode realizes CBR at two levels simultaneously. *Level 2*: A compiled NormCode plan is an abstract case — a runtime definition from which all executions of this type are instantiated. The six production plans constitute a case library of abstract reasoning patterns. Level 2 cases arise from two routes: (A) distillation of experience (experience → human author + pipeline → new/revised plan) and (B) direct compilation of mature rationale (rationale → pipeline → new plan). The compilation pipeline (Derivation → Formalization → Post-Formalization → Activation) is itself a NormCode plan (self-hosted). *Level 1*: Each execution checkpoint is a concrete case — a suspended runtime state (Blackboard + Concept Repository snapshot) persisted in SQLite. The four CBR operations map directly onto Canvas operations at this level.

## Color convention

Use project color convention: amber for Level 2 / case base; green for completed nodes; blue for running; gray for pending. Background: white, subtle dot grid.
