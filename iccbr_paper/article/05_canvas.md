# 6. The Canvas App: Interface for Both CBR Levels

NormCode Canvas (v1.1.3) is the deployed system that makes both levels of CBR
accessible in one environment. It is not a debugging tool appended to a workflow
runner — the CBR operations are its primary interaction model. This section describes
how each UI component maps to a CBR operation at Level 1 or Level 2.

> **[Fig. 3 here — Canvas App screenshot annotated with CBR operation labels]**

## 6.1 Level 1 Interface: Concrete Case Management

### Graph View — Pre-Execution Case Structure

Before execution begins, Canvas renders the complete inference graph from the compiled
`concept_repo.json` and `inference_repo.json`. The graph is the case structure made
visible: every node is a potential Level 1 case (a future checkpoint), identified by
its flow index. Semantic nodes (purple hexagons) and syntactic nodes (gray rectangles)
are visually distinct — the cost structure of the plan is readable before any LLM call.

The graph view serves CBR in two ways. First, it establishes the *case base address
space*: a practitioner who knows the graph knows where valuable checkpoints will
accumulate (typically at the output of expensive semantic nodes). Second, it visualizes
the dependency structure that the scope rule enforces — making the stale-set of any
future revision visually apparent.

### Real-Time Execution — Retain

During a run, Canvas streams execution events via WebSocket. Node status follows the
progression: pending (gray) → running (blue pulsing) → completed (green) → failed
(red) → skipped (striped). Every transition to completed writes a new Level 1 case to
SQLite: `(run_id, flow_index, Blackboard_snapshot, Concept_Repository_snapshot)`. The
Tool Call Monitor (left panel) logs every LLM prompt and response, file access, and
Python execution, indexed by flow index — an audit trail for each semantic node.

Retain is fully automatic. The case base grows with every completed node, across every
run, without operator intervention.

### Breakpoint + Tensor Inspector — Retrieve

Any node can be designated as a breakpoint by flow index. Execution pauses before
that node runs, giving the operator the opportunity to inspect the case before the next
step executes. This is the Level 1 Retrieve operation: locating the suspended runtime
by `(run_id, flow_index)` and verifying its content before reuse or revision.

The Tensor Inspector (right panel) opens the Concept Repository at any completed node.
It displays the full N-dimensional Reference: axis names (e.g., `[file]`, `[slide]`,
`[feature]`), axis shapes, and content values or perceptual signs, in table, list, or
JSON view. The inspection is O(1): the bounded inputs of any step are structurally
available — not reconstructed from logs, not inferred from conversation history. This
is C1 — exact reasoning step inspection in a constant number of operations.

Step-by-step advancement moves execution forward one node at a time, enabling
incremental case inspection through the execution sequence.

### Value Override — Revise

At a breakpoint, or from the Checkpoint Panel on any completed case, the operator
clicks **Override** to enter edit mode. The Tensor Inspector becomes editable: the
operator modifies axis entries, adds new entries, or removes incorrect ones.

On resume, the orchestrator:
1. Records the modified tensor as the new Concept Repository entry at that flow index.
2. Marks all downstream nodes as stale, computed automatically from the dependency
   graph (the scope rule guarantees the stale set is exact).
3. Re-executes only stale nodes; serves all upstream nodes from their cached tensors.

This is C3 — scope-bounded selective re-run. In a 40-inference plan with a revision
at inference 30, the 29 upstream inferences are preserved; the downstream 10
re-execute. Override entries are recorded with `is_override = true` in SQLite,
distinguishing revised cases from original execution cases.

### Fork — Reuse

The Checkpoint Panel lists all Level 1 cases in the case base, organized by run ID
and flow index. For any checkpoint, the operator clicks **Fork** to instantiate a new
execution from that case:

1. New run identifier $r'$ is created.
2. The orchestrator loads the stored $(\mathcal{B}_f, \mathcal{C}_f)$.
3. All upstream nodes are marked completed — no re-execution.
4. All downstream nodes are placed on the Waitlist and execute fresh.

The parent run is preserved unchanged in the case base. The Checkpoint Panel records
the fork relationship (`parent_run_id`, `fork_flow_index`), making case genealogy
inspectable. Fork supports: failure recovery (resume from last good checkpoint),
A/B testing (compare two continuations from the same mid-plan state), cost efficiency
(reuse expensive early-stage outputs across task variations), and iterative refinement
(try a different approach without losing prior results).

## 6.2 Level 2 Interface: Abstract Case Management

### `.ncn` Review Panel — Abstract Case Verification

The `.ncn` file generated by the compiler's Formalization phase is the Level 2
interpretability artifact. Canvas exposes it in a review panel available before the
first run — the point at which a stakeholder can verify the abstract case (the plan
structure) before it generates any concrete cases (Level 1 checkpoints).

This is C2 — zero-cost pre-execution review. The review costs no tokens, consumes no
LLM calls, and requires no NormCode syntax knowledge. A domain expert reads the
plain-prose narrative, verifies that the reasoning structure matches intent, and either
approves the plan for execution or rejects it for revision. All prior human-in-the-loop
interventions for LLM systems (RLHF, Constitutional AI, red-teaming) operate during
or after probabilistic computation. The `.ncn` review is the only intervention at the
plan structure level before any computation begins.

### Compilation Workflow Visibility

When the NC Compilations plan runs the compiler pipeline (§8), Canvas shows the
compilation as a Level 1 execution: each compilation phase is a node in the graph,
producing checkpoints at each phase's output. The Tensor Inspector exposes intermediate
compilation artifacts — the draft `.ncd`, the generated flow indices, the paradigm
assignments — at every phase checkpoint.

This visibility means the compilation pipeline is debuggable via Level 1 CBR: if
Formalization produces incorrect flow indices, the operator can retrieve the
Derivation checkpoint, inspect the draft structure, override the problematic concept,
and resume from Formalization. The Level 2 distillation process is itself managed by
the Level 1 retrieve–revise cycle.

### Plan Modification Tools

`.ncds` files are plain text, editable in any editor. A designer modifies the plan
file, re-runs the compiler (via NC Compilations or directly), and the Canvas App loads
the new `concept_repo.json` and `inference_repo.json` for the next run. The revised
`.ncn` is available for review before execution — verifying the abstract case revision
before it generates new concrete cases.

## 6.3 Architecture

**Frontend:** React 18 with TypeScript; React Flow for graph visualization; Zustand
for state management; TailwindCSS.

**Backend:** FastAPI with Python 3.11; SQLite for case base persistence; native Python
WebSockets for real-time execution events.

**Communication:** REST for control operations (load plan, configure agents, set
breakpoints, fork, override); WebSockets for real-time execution events (node status,
tool calls, checkpoint creation).

**Orchestrator:** Dependency-driven scheduling via Waitlist (priority queue by flow
index) and Blackboard (status tracker). Each cycle scans the Waitlist for nodes whose
declared input concepts are all completed in the Concept Repository, executes ready
nodes, and updates the Blackboard. The scope rule is enforced by construction: the
orchestrator passes only the declared tensor references to each inference's input —
never the full Concept Repository.

**Multi-agent support.** The left configuration panel registers multiple agents with
different LLM models (e.g., `qwen-plus`, `gpt-4o`, `claude-3-opus`), tool
configurations, and paradigm directories. Inferences are mapped to agents by pattern
rules on flow indices or by explicit assignments. Agent configuration is part of the
Level 1 case metadata: a forked run can use a different agent configuration than the
parent, enabling controlled comparison of agent capabilities on identical task inputs.
