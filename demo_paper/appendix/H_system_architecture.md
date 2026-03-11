# Appendix H — System Architecture

This appendix provides the technical architecture of the NormCode Canvas system:
the component breakdown, the runtime data flow, the WebSocket event protocol,
and the SQLite checkpoint schema. The body's §3.2 gives a one-paragraph summary;
this appendix is for readers evaluating integration, deployment, or extension.

---

## H.1 Component Overview

The Canvas system has two tiers: a React frontend (the Canvas App) and a
FastAPI backend (the Canvas Backend + Orchestrator). They communicate via
REST for control operations and WebSockets for real-time execution events.

```
┌───────────────────────────────────────────────────────────────────┐
│                       Canvas App (Frontend)                        │
│          React 18 · TypeScript · React Flow · Zustand             │
│          TailwindCSS · Vite · WebSocket client                    │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐ │
│  │   Graph View     │  │   Left Panel     │  │   Right Panel    │ │
│  │   React Flow     │  │   Agent config   │  │  Tensor inspector│ │
│  │   nodes + edges  │  │   Tool call log  │  │  Node detail     │ │
│  │   status colors  │  │   Live prompts   │  │  Value override  │ │
│  └─────────────────┘  └─────────────────┘  └──────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Execution Controls: [Run] [Pause] [Step] [Fork] [Reset]    │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────┬─────────────────────────────────┘
                     REST API      │    WebSocket (real-time events)
                   /run /pause     │    node_start, node_complete,
                   /step /fork     │    node_failed, run_complete,
                   /override       │    tool_call, breakpoint_hit
┌─────────────────────────────────▼─────────────────────────────────┐
│                     Canvas Backend                                  │
│               FastAPI · Python 3.11 · Uvicorn                     │
│                                                                   │
│  ┌─────────────────────────┐   ┌───────────────────────────────┐ │
│  │      REST Router         │   │    WebSocket Manager          │ │
│  │  POST /run               │   │  ConnectionPool               │ │
│  │  POST /pause             │   │  broadcast_event(run_id, msg) │ │
│  │  POST /step              │   │  per-run subscription         │ │
│  │  POST /fork              │   └───────────────────────────────┘ │
│  │  POST /override          │                                    │
│  │  GET  /checkpoints       │                                    │
│  │  GET  /runs              │                                    │
│  └──────────────┬───────────┘                                    │
│                 │                                                  │
│  ┌──────────────▼──────────────────────────────────────────────┐ │
│  │                     Orchestrator                              │ │
│  │                                                              │ │
│  │  concept_repo.json + inference_repo.json → execution graph  │ │
│  │  topological sort → ready queue → executor dispatch         │ │
│  │  dependency tracker → selective re-run engine               │ │
│  │  breakpoint registry → pause/resume control                 │ │
│  │  checkpoint store interface (SQLite)                        │ │
│  └──────────────────────┬──────────────────────────────────────┘ │
│                          │ paradigm executor calls                 │
│  ┌───────────────────────▼──────────────────────────────────────┐ │
│  │              Agent Paradigm Executors                         │ │
│  │                                                              │ │
│  │  ┌─────────────────┐    ┌───────────────────────────────┐  │ │
│  │  │  Semantic        │    │  Syntactic                    │  │ │
│  │  │  Imperative      │    │  Grouping (collect)           │  │ │
│  │  │  Judgement       │    │  Timing (conditional)         │  │ │
│  │  └────────┬─────────┘    │  Looping (iterate)            │  │ │
│  │           │ LLM API      └───────────────────────────────┘  │ │
│  │  ┌────────▼─────────┐    ┌───────────────────────────────┐  │ │
│  │  │  LLM Client      │    │  Tool Registry                │  │ │
│  │  │  (configurable   │    │  file_system                  │  │ │
│  │  │  per agent/step) │    │  python_interpreter           │  │ │
│  │  └──────────────────┘    │  slide_renderer               │  │ │
│  │                          │  html_exporter                │  │ │
│  │                          └───────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                  SQLite Checkpoint Store                      │ │
│  │  runs · checkpoints · events · overrides · forks             │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

> **[APP-FIGURE H-1 HERE — Clean rendered version of the architecture diagram
> above, using consistent styling with the rest of the paper's figures.
> Recommended tool: draw.io or Figma. Color the Frontend tier blue,
> Backend tier purple, SQLite tier gray.]**

---

## H.2 Runtime Data Flow: Step-by-Step

The following sequence describes a typical Canvas session from plan load
to breakpoint debugging.

**1. Plan load.**
The operator opens a compiled plan project in Canvas. The frontend sends
`GET /plans/{plan_id}` → the backend returns the graph structure (node list,
edge list, node metadata) extracted from `concept_repo.json` and
`inference_repo.json`. The React Flow graph is rendered with all nodes
in pending state (gray).

**2. Run initiation.**
The operator clicks Run → `POST /run {plan_id, inputs}` → the backend
creates a new run entry in SQLite, instantiates the Orchestrator with the
loaded repositories, and begins execution.

**3. Orchestrator execution loop.**
The Orchestrator builds the topological order from the inference graph.
It maintains a ready queue: an inference is ready when all its input
concepts have stored checkpoints. On startup, global inputs (provided
by the caller) are stored as initial checkpoints.

For each ready inference:
- The Orchestrator emits `node_start` via WebSocket → the Canvas frontend
  updates the node to running state (blue pulsing).
- The Orchestrator dispatches the inference to the appropriate paradigm executor.
- The executor calls the LLM or tool, receives the result, formats it as a tensor.
- The Orchestrator stores the tensor in SQLite (`checkpoints` table).
- The Orchestrator emits `node_complete` via WebSocket → the Canvas frontend
  updates the node to completed state (green).
- The Orchestrator checks the ready queue: any inference whose inputs are
  now all satisfied is added to the queue.

Syntactic inferences (Grouping, Timing, Looping) follow the same flow
but execute in microseconds with no external call.

**4. Breakpoint pause.**
If a breakpoint is registered at flow index `i.j.k`, the Orchestrator
checks before dispatching inference `i.j.k`. If a breakpoint is found:
- The Orchestrator emits `breakpoint_hit {flow_index}` → Canvas updates
  the node to paused state (blue solid + breakpoint indicator).
- The Orchestrator suspends the ready queue and waits for a control signal.

**5. Tensor inspection.**
While paused, the operator can request the tensor at any completed node:
`GET /checkpoints/{run_id}/{flow_index}` → the backend returns the stored
tensor JSON → the Canvas tensor inspector displays it in table/list/JSON view.

**6. Value override.**
The operator edits the tensor and submits: `POST /override {run_id, flow_index, tensor}`.
The backend:
- Replaces the checkpoint tensor in SQLite for the specified flow index.
- Marks all downstream inferences (those with a dependency path from
  the overridden node) as stale in the dependency tracker.
- Does not modify any non-downstream checkpoint.
Returns a list of stale inference flow indices to the frontend → Canvas
marks those nodes as pending (gray) again.

**7. Resume.**
The operator clicks Resume → `POST /resume {run_id}` → the Orchestrator
re-enters the ready queue, beginning with stale inferences in topological
order.

**8. Fork.**
The operator clicks Fork at a specific checkpoint: `POST /fork {run_id, flow_index}`.
The backend:
- Creates a new run entry in SQLite.
- Copies all checkpoints from the original run up to and including the
  specified flow index into the new run.
- Returns the new run ID to the frontend → Canvas opens the new run in
  parallel view.
The original run is unaffected. Both runs proceed independently from
the fork point.

---

## H.3 WebSocket Event Protocol

All real-time execution events follow a common envelope:

```json
{
  "event": "node_complete",
  "run_id": "run_20240301_001",
  "flow_index": "1.1.3",
  "timestamp": "2024-03-01T14:23:11.432Z",
  "payload": { ... }
}
```

**Event catalog:**

| Event | Trigger | Payload |
|-------|---------|---------|
| `node_start` | Inference dispatched to executor | `{ "flow_index", "paradigm", "agent_id" }` |
| `node_complete` | Tensor stored in checkpoint | `{ "flow_index", "tensor_shape", "duration_ms" }` |
| `node_failed` | Executor raised exception | `{ "flow_index", "error_type", "error_message" }` |
| `node_skipped` | Timing node condition not met | `{ "flow_index", "condition" }` |
| `breakpoint_hit` | Breakpoint pause triggered | `{ "flow_index" }` |
| `tool_call` | LLM or tool executor making external call | `{ "flow_index", "tool", "prompt_preview", "token_count" }` |
| `tool_response` | LLM or tool call returned | `{ "flow_index", "tool", "response_preview", "latency_ms" }` |
| `run_complete` | All inferences finished | `{ "run_id", "total_calls", "total_tokens", "duration_ms" }` |
| `run_failed` | Run terminated with error | `{ "run_id", "error_flow_index", "error_message" }` |

The `tool_call` and `tool_response` events populate the Canvas left-panel
tool call monitor in real time. Each event includes a `prompt_preview` (the
first 200 characters of the prompt) for immediate inspection without
opening the full detail view.

---

## H.4 SQLite Checkpoint Store Schema

The checkpoint store is a local SQLite database managed by the backend.
It persists across sessions — closing and reopening Canvas restores all
prior runs with their checkpoints.

```sql
-- One row per Canvas session / plan project
CREATE TABLE runs (
    run_id          TEXT PRIMARY KEY,
    plan_id         TEXT NOT NULL,
    parent_run_id   TEXT,           -- SET if this run is a fork
    fork_flow_index TEXT,           -- the flow index forked from
    created_at      DATETIME NOT NULL,
    status          TEXT NOT NULL,  -- running | completed | failed | paused
    input_json      TEXT NOT NULL,  -- caller-provided global inputs
    metadata_json   TEXT
);

-- One row per completed inference node per run
CREATE TABLE checkpoints (
    checkpoint_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT NOT NULL REFERENCES runs(run_id),
    flow_index      TEXT NOT NULL,
    tensor_json     TEXT NOT NULL,  -- full tensor: axes, shape, data
    is_override     BOOLEAN DEFAULT FALSE,
    created_at      DATETIME NOT NULL,
    UNIQUE(run_id, flow_index)
);

-- One row per WebSocket event emitted during a run
CREATE TABLE events (
    event_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT NOT NULL REFERENCES runs(run_id),
    flow_index      TEXT,
    event_type      TEXT NOT NULL,
    payload_json    TEXT NOT NULL,
    created_at      DATETIME NOT NULL
);

-- One row per registered breakpoint
CREATE TABLE breakpoints (
    breakpoint_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT NOT NULL REFERENCES runs(run_id),
    flow_index      TEXT NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      DATETIME NOT NULL
);
```

**Fork implementation:** When `POST /fork` is called with `{run_id, flow_index}`,
the backend executes:

```sql
INSERT INTO runs (run_id, plan_id, parent_run_id, fork_flow_index, ...)
VALUES (new_run_id, plan_id, original_run_id, fork_flow_index, ...);

INSERT INTO checkpoints (run_id, flow_index, tensor_json, created_at)
SELECT new_run_id, flow_index, tensor_json, CURRENT_TIMESTAMP
FROM checkpoints
WHERE run_id = original_run_id
  AND flow_index <= fork_flow_index  -- topological order comparison
  AND is_within_dependency_path = TRUE;  -- only ancestors of fork point
```

The dependency path filtering ensures that only checkpoints that are
ancestors of the fork point are copied — parallel branches that have
no dependency relationship to the fork point are not copied.

---

## H.5 Multi-Agent Configuration

When multiple agents are configured in Canvas, the orchestrator uses a
pattern-matching system to assign each inference to the correct agent.

**Configuration format (Canvas left panel / `agent_config.json`):**

```json
{
  "agents": [
    {
      "agent_id": "outline_agent",
      "model": "claude-3-5-sonnet",
      "flow_index_patterns": ["1.1.2.1"],
      "tools": ["file_system"],
      "paradigm_dir": "./paradigms/outline/"
    },
    {
      "agent_id": "slide_agent",
      "model": "qwen-plus",
      "flow_index_patterns": ["1.1.3.*"],
      "tools": ["slide_renderer"],
      "paradigm_dir": "./paradigms/slide/"
    },
    {
      "agent_id": "assembly_agent",
      "model": "gpt-4o",
      "flow_index_patterns": ["1.2"],
      "tools": ["html_exporter", "pptx_builder"],
      "paradigm_dir": "./paradigms/assembly/"
    }
  ],
  "default_agent": "slide_agent"
}
```

Pattern matching supports exact flow indices (`1.1.2.1`), prefix wildcards
(`1.1.3.*` matches all children of 1.1.3), and range notation. The first
matching pattern wins. Unmatched inferences fall to the default agent.

This enables heterogeneous model configurations within a single plan —
a cheaper fast model for routine steps, a more capable model for critical
reasoning steps — while the isolation guarantee holds for all agents equally.
