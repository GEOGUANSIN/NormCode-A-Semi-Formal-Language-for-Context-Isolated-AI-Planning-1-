# 3. The NormCode Canvas App

The Canvas App is NormCode's primary interface for Product Operators — the
environment where plans become visible, executable, inspectable, and modifiable.
Version 1.1.3 is production-ready across four capability phases.

## 3.1 Capability Phases

**Phase 1 — Graph View.** Before a single step runs, the Canvas renders the
complete inference graph. Semantic nodes (imperative and judgement operations that
invoke LLMs) appear as purple hexagons; data nodes appear as blue rounded
rectangles; syntactic routing nodes (grouping, timing, looping — which never
invoke LLMs) appear in gray. Edges show explicit data flow. The graph topology
makes the plan's logic auditable at a glance before execution.

**Phase 2 — Real-Time Execution.** During a run, node status updates stream via
WebSocket in real time. Indicators follow the progression: pending (gray) →
running (blue pulsing) → completed (green) → failed (red) → skipped (striped).
The tool call monitor in the left panel captures every LLM prompt and response,
every file system access, and every Python script execution as they occur.

**Phase 3 — Breakpoint Debugging.** Any node can be designated as a breakpoint
by its flow index (e.g., `1.3.2`). Execution pauses before that node runs. The
right panel opens the **Tensor Inspector** for any adjacent completed node,
showing its full N-dimensional reference data organized by named axis — not raw
prompt strings, but structured data with axis labels such as `[document]`,
`[slide]`, or `[feature]`. The inspector supports table, list, and JSON view
modes. Step-by-step advancement moves through one inference at a time.

**Phase 4 — Modification.** At a breakpoint, a value can be overridden: the user
edits the tensor content, then resumes. The orchestrator re-runs only the inferences
downstream of the modified node — the rest are served from cache. Additionally,
**Fork** creates a new run branching from any past checkpoint, preserving the
original execution for comparison. This enables A/B testing of plan logic without
restarting from scratch.

## 3.2 Architecture

The Canvas App is built on React 18 with TypeScript, React Flow for graph
visualization, and Zustand for state management. The backend runs FastAPI with
Python 3.11, using SQLite for checkpoint persistence and WebSockets for real-time
event streaming. Plans are loaded as `concept_repo.json` and `inference_repo.json`
— the output of the four-phase NormCode compiler — and executed by the NormCode
Orchestrator, which manages dependency-driven scheduling, the Blackboard (real-time
state tracker), and the Waitlist (prioritized inference queue).

> **[FIGURE 1 HERE — Canvas App annotated screenshot: graph center, left panel
> (agent config + tool call log), right panel (tensor inspector), execution controls]**
