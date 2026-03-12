# Canvas App Debugging & Auditing Guide

**Deep inspection tools for understanding, debugging, and auditing NormCode plan execution.**

---

## Introduction

NormCode's core value proposition is transparency — every inference, every tool call, every data transformation is observable. The Canvas App provides multiple layers of inspection, from real-time graph status to deep database forensics.

This guide covers:
- Graph-level debugging (breakpoints, step execution, data trace)
- Execution Log Viewer (cycle-by-cycle parsed logs)
- Orchestrator DB Inspector (database forensics)
- Tool call monitoring
- Data inspection and tensor viewing

---

## Debugging Layers

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Graph Canvas (real-time visual)                       │
│  ├── Node status colors (pending/running/completed/failed)     │
│  ├── Live execution progress                                    │
│  └── Breakpoint indicators                                      │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Control & Stepping                                    │
│  ├── Run / Pause / Step / Run To                               │
│  ├── Breakpoint Navigator                                       │
│  └── Step Pipeline (current inference progress)                │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: Data Inspection                                       │
│  ├── Detail Panel (node metadata, tensor data)                 │
│  ├── TensorInspector (N-D tensor viewing)                      │
│  ├── Data Trace Panel (data lineage)                           │
│  └── Value Override (modify and re-run)                        │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: Log Analysis                                          │
│  ├── Log Panel (real-time filtered logs)                       │
│  ├── Execution Log Viewer (structured cycle parsing)           │
│  └── Issue Navigator (warnings, errors)                        │
├─────────────────────────────────────────────────────────────────┤
│  Layer 5: Database Forensics                                    │
│  ├── Orchestrator DB Inspector                                 │
│  ├── Checkpoint viewer (blackboard, workspace)                 │
│  └── Execution record browser                                  │
├─────────────────────────────────────────────────────────────────┤
│  Layer 6: Tool Monitoring                                       │
│  ├── Agent Panel tool call feed                                │
│  └── Per-tool WebSocket events                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Layer 1: Graph Canvas Debugging

### Node Status Colors

During execution, every node on the graph reflects its real-time status:

| Color | Status | Meaning |
|-------|--------|---------|
| Gray | `pending` | Not yet executed |
| Blue (pulsing) | `running` | Currently executing |
| Green | `completed` | Successfully executed |
| Red | `failed` | Execution failed |
| Yellow | `skipped` | Skipped (dependency not met or condition false) |

### Setting Breakpoints

Breakpoints pause execution before a specific inference runs:

1. **From the graph**: Click a function node, then click the breakpoint icon in the Detail Panel
2. **From the Breakpoint Navigator**: View all breakpoints, add/remove, jump to node
3. **From code**: Pre-configure breakpoints in the project config (`breakpoints: ["1.2.1", "2.3"]`)

### Breakpoint Navigator

The `BreakpointNavigator` component provides a dedicated view:
- List all active breakpoints with flow indices and concept names
- Click to navigate to the breakpointed node on the graph
- Toggle individual breakpoints on/off
- Clear all breakpoints

---

## Layer 2: Execution Control

### Control Panel

| Button | Action | Keyboard |
|--------|--------|----------|
| **Run** | Execute all ready inferences | — |
| **Pause** | Stop after current inference completes | — |
| **Step** | Execute exactly one inference | — |
| **Run To** | Execute until selected node | — |
| **Reset** | Clear execution state, reload plan | — |

### Step Pipeline

The `StepPipeline` component shows the internal progress of the currently-executing inference:

```
┌─────────────────────────────────────────────────────────────┐
│  Inference 1.2.1: h_Analyze-c_DeepReview-o_Report           │
│                                                             │
│  [IWI] → [IR] → [MFP] → [TVA] → [OR] → [OWI]            │
│   ✓       ✓      ●                                         │
│                                                             │
│  Step: Model-Function-Perception (MFP)                      │
│  Duration: 1.2s                                             │
└─────────────────────────────────────────────────────────────┘
```

Pipeline steps:
| Step | Full Name | What It Does |
|------|-----------|-------------|
| **IWI** | Input Working Interpretation | Resolve input data |
| **IR** | Input Reference | Load input tensors |
| **MFP** | Model-Function-Perception | Set up tool affordances, compose function |
| **TVA** | Tool-Value-Actuation | Execute the composed function (LLM call, file read, etc.) |
| **OR** | Output Reference | Store output tensors |
| **OWI** | Output Working Interpretation | Update output metadata |

---

## Layer 3: Data Inspection

### Detail Panel

Click any node to open the Detail Panel showing:
- **Value nodes**: Concept name, axes, shape, tensor data (expandable)
- **Function nodes**: Sequence type, paradigm, working interpretation, execution status
- **Metadata**: Flow index, natural name, ground/final status

### TensorInspector

For complex multi-dimensional data, the TensorInspector provides:

| Dimension | View |
|-----------|------|
| 0D (scalar) | Single value display |
| 1D | Horizontal cards or vertical list |
| 2D | Spreadsheet-like table |
| N-D | Axis selection + slice sliders + view mode toggle |

**View modes**: Table, List, JSON raw

**Perceptual sign parsing**: Values in `%xxx({...})` format are automatically parsed and displayed as structured objects.

### Data Trace Panel

The `DataTracePanel` shows data lineage — how a value was produced:

- Which inference produced it
- What inputs were consumed
- The paradigm and sequence used
- Upstream and downstream data dependencies

### Value Override

For debugging, you can override a node's value and re-run downstream inferences:

1. Select a value node
2. Click "Override Value" in the Detail Panel
3. Enter new JSON data
4. The system identifies affected downstream nodes
5. Re-runs only the impacted subgraph

---

## Layer 4: Execution Log Viewer

The `ExecutionLogViewer` is a structured log analysis tool accessed from the Editor panel. It parses raw orchestrator logs into a navigable, cycle-by-cycle view.

### Opening

Open any `.log` file from the Editor panel's file browser. Files are found in the project's `logs/` directory with names like `run_<id>_<timestamp>.log`.

### Cycle View

Logs are parsed into execution cycles. Each cycle represents one inference:

```
┌─────────────────────────────────────────────────────────────────┐
│  Cycle 3: 1.2.1 — h_Analyze-c_DeepReview-o_Report              │
│  Status: completed | Duration: 2.4s                             │
│                                                                 │
│  ┌─ Readiness Checks ──────────────────────────────────────────┐│
│  │  ✓ 1.1.1 ready (exec_count=1)                              ││
│  │  ✓ 1.1.2 ready (exec_count=1)                              ││
│  │  ✗ 1.3.1 not ready (exec_count=0)                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─ Sequence Execution ───────────────────────────────────────┐ │
│  │  Step: IWI (12ms)                                          │ │
│  │  Step: IR  (5ms)                                           │ │
│  │  Step: MFP (234ms) ← expand for affordances, composition  │ │
│  │  Step: TVA (2.1s)  ← expand for HTTP requests, results    │ │
│  │  Step: OR  (3ms)                                           │ │
│  │  Step: OWI (8ms)                                           │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### MFP Step Block

When you expand an MFP step, you see:
- **Environment spec** used (ModelEnvSpecLite, etc.)
- **Tool specs** loaded
- **Registered affordances** (tool.method pairs)
- **Model steps** (each affordance resolution with duration)
- **Composition plan** (how affordances are composed into a function)
- **State dump** (Function, Values, Context, Inference sections after MFP)

### TVA Step Block

When you expand a TVA step, you see:
- **Tool kind** (file_read, llm_call, http_request, canvas_action)
- **HTTP requests** (method, URL, status code, duration)
- **File operations** (read/write paths)
- **Vision waits** (blocking user interaction duration)
- **Result value** (reference ID, type tag, preview)
- **State dump** after TVA
- **Warning/error counts**

### Issue Navigator

The `IssueNavigator` component filters and highlights problems:
- Warnings across all cycles
- Errors with stack traces
- Click to jump to the relevant cycle and step

### Stats Bar

Summary statistics for the entire log:
- Total lines, entries, cycles
- Level breakdown (DEBUG, INFO, WARNING, ERROR)
- Time span
- Unique flow indices and sources

---

## Layer 5: Orchestrator DB Inspector

The `OrchestratorDBInspector` provides direct access to the SQLite database used by the orchestrator for state persistence.

### Opening

Open any `.db` file from the Editor panel's file browser. The inspector renders automatically for orchestration database files.

### Views

| View | What It Shows |
|------|--------------|
| **Overview** | Database tables, row counts, file size |
| **Runs** | All execution runs with start/end times, status |
| **Executions** | Individual inference executions within a run (flow index, status, duration) |
| **Checkpoints** | Saved execution state at each cycle |
| **Blackboard** | Concept values at a checkpoint (the "blackboard" state) |
| **Concepts** | Concept definitions and their current values |

### Checkpoint Inspection

Select a run, then a checkpoint cycle to see:
- **Blackboard**: All concept values at that point in time
- **Workspace**: Working interpretation state
- **Execution status**: Which inferences were completed/pending

This is invaluable for understanding what data was available when a specific inference ran.

### Trace Export

The `TraceExportCard` component allows exporting execution traces as JSON for external analysis.

---

## Layer 6: Tool Call Monitoring

### Agent Panel Feed

The Agent Panel's tool call feed shows every tool invocation in real time:

| Column | Content |
|--------|---------|
| Timestamp | When the call started |
| Flow Index | Which inference triggered it |
| Tool.Method | e.g., `llm.generate`, `shell.run`, `editor.edit` |
| Status | ⏳ running, ✓ completed, ✗ failed |
| Duration | Time taken |

Each tool type has a distinct color chip (blue=LLM, teal=shell, sky=search, orange=git, emerald=editor).

Click any entry to expand and see full inputs and outputs.

### Per-Tool Events

Code assistant tools emit domain-specific events beyond the generic `tool:call_*`:

| Tool | Events |
|------|--------|
| Shell | `shell:started`, `shell:completed`, `shell:failed`, `shell:background_started` |
| Search | `search:grep_started`, `search:grep_completed`, `search:glob_completed` |
| Git | `git:status`, `git:diff`, `git:committed`, `git:branch_changed` |
| Editor | `editor:edit_started`, `editor:edit_completed`, `editor:file_created`, `editor:edit_failed` |

---

## Debugging Workflows

### "Why did this inference fail?"

1. Find the failed (red) node on the graph
2. Click it to open the Detail Panel — check the error message
3. Open the Log Panel, filter by flow index — see raw log context
4. Open the `.log` file in Execution Log Viewer — find the cycle, expand TVA step for HTTP errors or tool failures
5. Check the DB Inspector checkpoint before the failure — verify input data was correct

### "Why is the output wrong?"

1. Select the value node with wrong data
2. Open TensorInspector — examine the actual value
3. Open Data Trace Panel — trace which inference produced it
4. Set a breakpoint on the producing function node
5. Re-run, then step through and inspect each pipeline stage (IWI → IR → MFP → TVA → OR → OWI)
6. Use Value Override to inject correct upstream values and verify the function works

### "Why is execution slow?"

1. Check the Execution Log Viewer Stats Bar for total duration
2. Look at per-cycle durations — find the slowest cycles
3. Expand TVA steps — check HTTP request durations (LLM calls are usually the bottleneck)
4. Check the Agent Panel feed — find the longest tool calls
5. Check for unnecessary readiness check re-evaluations in the cycle view

---

## Related Components

| Component | File | Purpose |
|-----------|------|---------|
| `BreakpointNavigator` | `panels/BreakpointNavigator.tsx` | Breakpoint management |
| `DataTracePanel` | `panels/DataTracePanel.tsx` | Data lineage |
| `StepPipeline` | `panels/StepPipeline.tsx` | Inference step progress |
| `TensorInspector` | `panels/TensorInspector.tsx` | N-D tensor viewer |
| `ValueOverrideModal` | `panels/ValueOverrideModal.tsx` | Value override dialog |
| `FunctionModifyModal` | `panels/FunctionModifyModal.tsx` | Function paradigm modification |
| `RerunConfirmModal` | `panels/RerunConfirmModal.tsx` | Selective re-run confirmation |
| `ExecutionLogViewer` | `editor/execution-log/ExecutionLogViewer.tsx` | Structured log viewer |
| `OrchestratorDBInspector` | `editor/db-inspector/OrchestratorDBInspector.tsx` | Database inspector |

---

## See Also

- **[Canvas App User Guide](canvas_app_user_guide.md)**: General usage instructions
- **[Canvas App Overview](canvas_app_overview.md)**: Architecture and concepts
- **[API Reference](canvas_app_api_reference.md)**: Execution endpoints and WebSocket events
- **[Implementation Plan](implementation_plan.md)**: Remaining debugging features

---

**Last Updated**: March 2026
