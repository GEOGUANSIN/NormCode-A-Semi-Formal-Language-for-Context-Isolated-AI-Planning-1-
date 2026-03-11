# Canvas App Overview

**The NormCode Graph Canvas App is a visual, interactive environment for executing, debugging, and auditing NormCode plans.**

---

## Introduction

The Canvas App transforms NormCode from "run and hope" to "observe and control". Instead of executing plans blindly and inspecting results after the fact, users can:

1. **Visualize** the entire inference graph before execution
2. **Watch** execution progress in real-time
3. **Debug** with breakpoints and step-by-step execution
4. **Inspect** tensor data at any node
5. **Configure** multiple agents with different LLM models
6. **Edit** NormCode files directly within the app

---

## Core Concepts

### Project-Based Architecture

The Canvas App operates like an IDE (PyCharm, VS Code). Everything is organized around **projects**:

```
my_project/
├── gold-analysis.normcode-canvas.json    # Project config
├── concepts.json                         # Concept repository
├── inferences.json                       # Inference repository
├── inputs.json                           # Input data (optional)
└── provision/
    └── paradigm/                         # Custom paradigms
```

**Project Config** (`{name}.normcode-canvas.json`):
```json
{
  "id": "a1b2c3d4",
  "name": "Gold Analysis",
  "description": "Investment analysis project",
  "repositories": {
    "concepts": "concepts.json",
    "inferences": "inferences.json",
    "inputs": "inputs.json"
  },
  "execution": {
    "llm_model": "qwen-plus",
    "max_cycles": 100,
    "db_path": "orchestration.db",
    "paradigm_dir": "provision/paradigm"
  },
  "breakpoints": ["1.1", "2.3.1"]
}
```

### Multi-Project Support

A single directory can contain multiple project configurations:
- `gold-analysis.normcode-canvas.json`
- `gold-debug.normcode-canvas.json`
- `gold-chinese.normcode-canvas.json`

Each project has its own settings, breakpoints, and execution history while sharing the same repository files.

### Centralized Registry

All known projects are tracked in `~/.normcode-canvas/project-registry.json`:
```json
{
  "projects": [
    {
      "id": "a1b2c3d4",
      "name": "Gold Analysis",
      "directory": "C:/path/to/project",
      "config_file": "gold-analysis.normcode-canvas.json",
      "last_opened": "2024-12-21T15:30:00"
    }
  ]
}
```

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           BROWSER                                        │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  React App (Vite + TypeScript)                                    │  │
│  │  ├── Zustand Stores (state management)                            │  │
│  │  ├── React Flow (graph visualization)                             │  │
│  │  └── WebSocket Client (real-time events)                          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│              │ REST API              │ WebSocket                         │
└──────────────┼───────────────────────┼───────────────────────────────────┘
               ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         BACKEND (FastAPI)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  Routers                                                            ││
│  │  ├── project_router.py      # Project CRUD                         ││
│  │  ├── repository_router.py   # Load repositories                    ││
│  │  ├── graph_router.py        # Graph data                           ││
│  │  ├── execution_router.py    # Run/pause/step                       ││
│  │  ├── agent_router.py        # Agent configuration                  ││
│  │  ├── editor_router.py       # File editing                         ││
│  │  ├── checkpoint_router.py   # Resume/fork                          ││
│  │  └── websocket_router.py    # Event streaming                      ││
│  ├─────────────────────────────────────────────────────────────────────┤│
│  │  Services                                                           ││
│  │  ├── ExecutionController    # Orchestrator wrapper                 ││
│  │  ├── GraphService           # Graph building                       ││
│  │  ├── AgentRegistry          # Multi-agent management               ││
│  │  ├── BodyFacultyManager     # Tool declaration & injection         ││
│  │  ├── ProjectService         # Project persistence                  ││
│  │  └── ParserService          # NormCode parsing                     ││
│  ├─────────────────────────────────────────────────────────────────────┤│
│  │  Tools (canvas_app/backend/tools/)                                  ││
│  │  ├── LLM, FileSystem, PythonInterpreter  # Core faculties          ││
│  │  ├── Chat, Canvas, Parser, Composition   # Canvas faculties        ││
│  │  └── Shell, Search, Git, Editor, Memory  # Code assistant faculties││
│  └─────────────────────────────────────────────────────────────────────┘│
│              │                                                           │
└──────────────┼───────────────────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      NORMCODE INFRASTRUCTURE                             │
│  ├── Orchestrator              # Execution engine                       │
│  ├── ConceptRepo               # Concept storage                        │
│  ├── InferenceRepo             # Inference storage                      │
│  ├── Body                      # Agent with faculties (tools)           │
│  └── OrchestratorDB            # Checkpoint storage                     │
└─────────────────────────────────────────────────────────────────────────┘
```

### Frontend Architecture

**State Management (Zustand Stores)**:

| Store | Purpose |
|-------|---------|
| `graphStore` | Graph nodes, edges, layout, collapse state |
| `executionStore` | Execution status, node statuses, breakpoints, logs |
| `selectionStore` | Selected node/edge, highlighted branches |
| `projectStore` | Current project, recent projects, registry |
| `configStore` | Execution settings (LLM, cycles, etc.) |
| `agentStore` | Agent configurations, mappings, tool calls |

**Component Hierarchy**:

```
App
├── ProjectPanel            # Welcome screen / project management
├── Header                  # Project info, view mode tabs, controls
├── SettingsPanel           # Execution configuration
├── ControlPanel            # Run/pause/step/stop buttons
├── CheckpointPanel         # Resume/fork from checkpoints
│
├── [Canvas Mode]
│   ├── AgentPanel          # Left: agent config + tool calls
│   ├── GraphCanvas         # Center: React Flow graph
│   │   ├── ValueNode       # Value concept nodes
│   │   ├── FunctionNode    # Function concept nodes
│   │   └── CustomEdge      # Styled edges by type
│   ├── DetailPanel         # Right: node details + tensor viewer
│   └── LogPanel            # Bottom: execution logs
│
├── [Editor Mode]
│   └── EditorPanel         # File browser + code editor
│
└── StatusBar               # Connection status, node count
```

### Backend Architecture

**Execution Controller**:

The `ExecutionController` class wraps the NormCode Orchestrator with debugging support:

```python
class ExecutionController:
    orchestrator: Orchestrator           # Core execution engine
    agent_registry: AgentRegistry        # Multi-agent management
    agent_mapping: AgentMappingService   # Per-inference agent assignment
    
    node_statuses: Dict[str, str]        # Flow index → status
    breakpoints: Set[str]                # Breakpoint flow indices
    logs: List[LogEntry]                 # Execution logs
    
    async def start()                    # Begin execution
    async def pause()                    # Pause after current inference
    async def step()                     # Execute one inference
    async def stop()                     # Stop execution
    async def run_to(flow_index)         # Run until specific node
    async def restart()                  # Reset and reload
```

**Agent Registry**:

The `AgentRegistry` manages multiple agent configurations:

```python
class AgentConfig:
    id: str                              # Unique identifier
    name: str                            # Display name
    llm_model: str                       # LLM model name
    tools: Dict[str, bool]               # Tool enable/disable
    paradigm_dir: Optional[str]          # Custom paradigm directory

class AgentRegistry:
    configs: Dict[str, AgentConfig]      # Registered agents
    bodies: Dict[str, Body]              # Cached Body instances
    
    def get_body(agent_id) -> Body       # Get/create Body
    def register(config)                 # Register agent config
```

**Body Faculty Manager**:

The `BodyFacultyManager` is the centralized registry for all tool capabilities available to NormCode plans. It declares `FacultySpec` entries (name, attribute, class, description) and handles instantiation and injection into the `Body` object.

```python
class FacultySpec:
    name: str              # Faculty name ("shell", "search", ...)
    body_attr: str         # Attribute on Body ("shell", "search", ...)
    tool_class: type       # CanvasShellTool, CanvasSearchTool, ...
    description: str       # Human-readable purpose

class BodyFacultyManager:
    FACULTY_SPECS: List[FacultySpec]     # All registered faculties
    
    def create_core_tools(body, ...)     # LLM, file_system, python_interpreter
    def create_canvas_tools(body, ...)   # chat, canvas, parser, etc.
    def create_code_tools(body, ...)     # shell, search, git, editor
```

Every tool instantiated by the manager is automatically wrapped in a `MonitoredToolProxy` that emits `tool:call_started` / `tool:call_completed` / `tool:call_failed` WebSocket events, making all tool activity visible in the Agent Panel.

---

## Body Faculties (Tool Architecture)

The Body is the NormCode agent's interface to the outside world. Plans access capabilities through `me.body.<faculty>.<method>()`. Faculties are grouped into three tiers:

### Core Faculties

Available in all NormCode plans:

| Faculty | Methods | Description |
|---------|---------|-------------|
| `llm` | `.ask()`, `.complete()` | Language model generation |
| `file_system` | `.read()`, `.write()`, `.list()`, `.exists()` | File I/O |
| `python_interpreter` | `.run()` | Python script execution |
| `prompt` | `.load()`, `.render()` | Prompt template management |
| `user_input` | `.ask()` | Blocking user input |

### Canvas Faculties

Used by Canvas-aware plans (e.g., the Canvas Assistant):

| Faculty | Methods | Description |
|---------|---------|-------------|
| `chat` | `.write()`, `.confirm()`, `.notify()` | Chat UI interaction |
| `canvas` | `.display()`, `.add_node()` | Canvas graph manipulation |
| `parser` | `.parse()`, `.serialize()` | NormCode parsing at runtime |
| `model_runner` | `.run()` | Paradigm/model execution |
| `composition` | `.compose()` | Function composition |
| `perception` | `.route()` | Perceptual sign routing |
| `formatter` | `.format()`, `.parse()` | Data formatting |

### Code Assistant Faculties

Used by software engineering plans. Each emits WebSocket events for real-time monitoring:

| Faculty | Key Methods | WebSocket Events | Description |
|---------|-------------|-------------------|-------------|
| `shell` | `.run()`, `.run_background()`, `.check_process()`, `.kill_process()` | `shell:started`, `shell:completed`, `shell:failed` | Command execution with timeout and dangerous-command blocking |
| `search` | `.grep()`, `.glob()`, `.find_definition()`, `.find_references()` | `search:grep_started`, `search:grep_completed`, `search:glob_completed` | Ripgrep-powered code search with symbol lookup |
| `git` | `.status()`, `.diff()`, `.log()`, `.add()`, `.commit()`, `.branch()`, `.checkout()`, `.stash()` | `git:status`, `git:diff`, `git:committed`, `git:branch_changed` | Git operations with safety (no force push or hard reset) |
| `editor` | `.edit()`, `.insert_at()`, `.delete_lines()`, `.create()`, `.read_range()` | `editor:edit_started`, `editor:edit_completed`, `editor:file_created` | Surgical file editing with exact text matching |
| `memory` | `.search()`, `.add()`, `.update()`, `.delete()`, `.list_all()` | `memory:search:start`, `memory:add:start` | Cross-session semantic memory via mem0 |

### Tool Injection Pipeline

```
FacultySpec (declaration)
    │
    ▼
BodyFacultyManager.create_*_tools()    →   Tool instance created
    │
    ▼
MonitoredToolProxy(tool)               →   WebSocket event emission
    │
    ▼
body.<attr> = proxy                    →   Injected into Body
    │
    ▼
Paradigm calls me.body.<attr>.<method>()   →   Monitored execution
```

---

## Graph Visualization

### Node Types and Categories

| Category | Examples | Color | Description |
|----------|----------|-------|-------------|
| **semantic-function** | `::(analyze)`, `:<filter>` | Purple | LLM-based operations |
| **semantic-value** | `{result}`, `<item>`, `[list]` | Blue | Data containers |
| **syntactic-function** | `$collect`, `&assign` | Gray | Deterministic operations |

### Node Status Indicators

| Status | Indicator | Description |
|--------|-----------|-------------|
| `pending` | Gray dot | Not yet executed |
| `running` | Blue pulsing dot | Currently executing |
| `completed` | Green dot | Successfully completed |
| `failed` | Red dot | Execution failed |
| `skipped` | Striped dot | Skipped (SKIP value) |

### Special Node Markers

| Marker | Visual | Meaning |
|--------|--------|---------|
| **Ground** | Double border | Input data (ground concept) |
| **Output** | Red ring | Final result (output concept) |
| **Breakpoint** | Red badge | Breakpoint set on this node |

### Edge Types

| Type | Color | Style | Description |
|------|-------|-------|-------------|
| `function` | Blue | Solid | Function → Target connection |
| `value` | Purple | Solid | Value input → Target connection |
| `context` | Green | Dashed | Context input connection |
| `alias` | Gray | Dashed | Same concept at different positions |

---

## Execution Model

### Flow Index System

Every node has a **flow index** that identifies its position in the execution DAG:

```
1           # Root concept (output)
├── 1.1     # Function concept
├── 1.2     # First value input
├── 1.3     # Second value input
│   ├── 1.3.1   # Sub-inference function
│   ├── 1.3.2   # Sub-inference value
```

Flow indices are used for:
- Node identification in the graph
- Breakpoint targeting
- Log filtering
- Execution ordering

### Execution Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│  ExecutionController._run_loop()                                 │
├─────────────────────────────────────────────────────────────────┤
│  while (state == RUNNING or STEPPING):                          │
│      1. Check pause event                                        │
│      2. Get next ready inference from waitlist                  │
│      3. Check breakpoints → pause if hit                        │
│      4. Emit "inference:started" event                          │
│      5. Resolve agent for this inference                        │
│      6. Execute inference with assigned Body                    │
│      7. Emit "inference:completed" or "inference:failed"        │
│      8. Emit "execution:progress"                               │
│      9. If stepping mode → pause                                │
└─────────────────────────────────────────────────────────────────┘
```

### WebSocket Events

Real-time events streamed to the frontend:

| Event | Payload | Description |
|-------|---------|-------------|
| `execution:loaded` | `{run_id, total_inferences}` | Repositories loaded |
| `execution:started` | `{}` | Execution began |
| `execution:paused` | `{reason}` | Execution paused |
| `execution:progress` | `{completed, total}` | Progress update |
| `execution:completed` | `{}` | All inferences done |
| `inference:started` | `{flow_index}` | Inference began |
| `inference:completed` | `{flow_index}` | Inference succeeded |
| `inference:failed` | `{flow_index, error}` | Inference failed |
| `breakpoint:hit` | `{flow_index}` | Breakpoint triggered |
| `log:entry` | `{flow_index, level, message}` | Log message |
| `tool:call_started` | `{tool, method, inputs}` | Tool call began |
| `tool:call_completed` | `{tool, method, outputs}` | Tool call succeeded |

---

## Multi-Agent System

### Agent Configuration

The Agent Panel allows configuring multiple agents with different:
- LLM models (qwen-plus, gpt-4o, claude-3, etc.)
- Core tool settings (file system, Python interpreter)
- Code assistant tool settings (shell, search, git, editor — each independently enabled per agent)
- Memory tool settings (semantic memory provider and category defaults)
- Paradigm directories

### Agent Mapping

Inferences can be assigned to specific agents via:

1. **Pattern Rules**: Match by flow_index, concept_name, or sequence_type
2. **Explicit Assignment**: Direct flow_index → agent_id mapping
3. **Default Agent**: Fallback for unmatched inferences

### Tool Call Monitoring

All tool calls are captured and displayed in real-time via the Agent Panel's tool call feed. Each tool type has a distinct color chip:

| Tool | Color | Event Types |
|------|-------|-------------|
| `llm` | blue | LLM generation calls |
| `file_system` | green | File read/write/list |
| `python` | yellow | Script executions |
| `shell` | teal | Command execution |
| `search` | sky | Grep/glob/symbol lookup |
| `git` | orange | Git operations |
| `editor` | emerald | File editing |
| `canvas` | purple | Canvas manipulation |

The feed shows method name, inputs, outputs (collapsible), duration, and status for every call across all faculties.

---

## Data Inspection

### TensorInspector

The TensorInspector component provides N-dimensional tensor viewing:

| Dimension | View |
|-----------|------|
| 0D (scalar) | Single value display |
| 1D | Horizontal cards or vertical list |
| 2D | Table with row/column headers |
| N-D | Axis selection + slice sliders + view mode |

**View Modes**:
- **Table**: Spreadsheet-like 2D slice view
- **List**: Expandable nested list view
- **JSON**: Raw JSON representation

### Perceptual Sign Parsing

Values in `%xxx({...})` format are automatically parsed and displayed as structured objects:

```
Input:  %c2a({'action': 'BUY', 'confidence': 0.82})
Display:
  ├── action: BUY
  └── confidence: 0.82
```

---

## File Organization

```
canvas_app/
├── backend/
│   ├── main.py                     # FastAPI entry point
│   ├── requirements.txt            # Python dependencies
│   ├── core/
│   │   ├── config.py              # App settings
│   │   └── events.py              # Event emitter
│   ├── routers/
│   │   ├── project_router.py      # Project CRUD
│   │   ├── repository_router.py   # Load repos
│   │   ├── graph_router.py        # Graph data
│   │   ├── execution_router.py    # Execution control
│   │   ├── agent_router.py        # Agent config
│   │   ├── editor_router.py       # File editing
│   │   ├── checkpoint_router.py   # Resume/fork
│   │   └── websocket_router.py    # Events
│   ├── services/
│   │   ├── execution_service.py   # ExecutionController
│   │   ├── graph_service.py       # Graph building
│   │   ├── agent_service.py       # Agent registry
│   │   ├── body_faculty_manager.py # Tool declaration & injection
│   │   ├── project_service.py     # Project management
│   │   ├── parser_service.py      # NormCode parsing
│   │   └── execution/
│   │       └── tool_injection.py  # Faculty injection pipeline
│   ├── tools/
│   │   ├── llm_tool.py            # LLM faculty
│   │   ├── file_system_tool.py    # File system faculty
│   │   ├── python_interpreter_tool.py  # Python interpreter
│   │   ├── chat_tool.py           # Chat interface
│   │   ├── canvas_tool.py         # Canvas display
│   │   ├── parser_tool.py         # NormCode parser
│   │   ├── shell_tool.py          # Shell execution (code assistant)
│   │   ├── search_tool.py         # Code search (code assistant)
│   │   ├── git_tool.py            # Git operations (code assistant)
│   │   ├── editor_tool.py         # File editing (code assistant)
│   │   └── memory_tool.py         # Semantic memory (code assistant)
│   └── schemas/
│       ├── execution_schemas.py   # Execution models
│       ├── graph_schemas.py       # Graph models
│       └── project_schemas.py     # Project models
│
├── frontend/
│   ├── package.json               # Node dependencies
│   ├── vite.config.ts             # Vite configuration
│   ├── tailwind.config.js         # Tailwind CSS config
│   └── src/
│       ├── App.tsx                # Main component
│       ├── main.tsx               # Entry point
│       ├── components/
│       │   ├── graph/
│       │   │   ├── GraphCanvas.tsx
│       │   │   ├── ValueNode.tsx
│       │   │   ├── FunctionNode.tsx
│       │   │   └── CustomEdge.tsx
│       │   └── panels/
│       │       ├── ControlPanel.tsx
│       │       ├── DetailPanel.tsx
│       │       ├── LogPanel.tsx
│       │       ├── AgentPanel.tsx
│       │       ├── ToolConfigCards.tsx
│       │       ├── EditorPanel.tsx
│       │       ├── ProjectPanel.tsx
│       │       ├── SettingsPanel.tsx
│       │       ├── CheckpointPanel.tsx
│       │       └── TensorInspector.tsx
│       ├── stores/
│       │   ├── graphStore.ts
│       │   ├── executionStore.ts
│       │   ├── selectionStore.ts
│       │   ├── projectStore.ts
│       │   ├── configStore.ts
│       │   └── agentStore.ts
│       ├── services/
│       │   ├── api.ts             # REST client
│       │   └── websocket.ts       # WebSocket client
│       ├── hooks/
│       │   └── useWebSocket.ts    # WebSocket hook
│       ├── types/
│       │   ├── graph.ts
│       │   ├── execution.ts
│       │   └── project.ts
│       └── utils/
│           └── tensorUtils.ts     # Tensor utilities
│
├── launch.py                      # Combined launcher
├── launch.ps1                     # PowerShell launcher
├── README.md                      # Quick start guide
├── IMPLEMENTATION_JOURNAL.md      # Development history
├── AGENT_PANEL_PLAN.md           # Agent feature plan
└── CHECKPOINT_FEATURE_PLAN.md    # Checkpoint feature plan
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React 18 | UI framework |
| | TypeScript | Type safety |
| | Vite | Build tool & dev server |
| | React Flow | Graph visualization |
| | Zustand | State management |
| | TailwindCSS | Styling |
| | Lucide React | Icons |
| **Backend** | FastAPI | REST API framework |
| | Python 3.11+ | Runtime |
| | WebSockets | Real-time events |
| | Pydantic | Data validation |
| **Infrastructure** | NormCode Orchestrator | Execution engine |
| | SQLite | Checkpoint storage |

---

## Built-in Projects

The Canvas App ships with built-in NormCode projects that demonstrate the faculty system and serve as interactive assistants.

### Canvas Assistant (`built_in_projects/canvas_assistant/`)

A chat-driven controller for the canvas UI. Runs as a NormCode plan that classifies user messages into commands (navigation, execution control, queries) and dispatches them via the Canvas Integration Tool's three perspectives:

- **Vision** (`me.vision`): Read canvas state (selected node, graph layout, execution status)
- **Hands** (`me.hands`): Execute UI actions (select node, zoom, fit view)
- **Mind** (`me.mind`): Control execution (run, pause, step)

### Code Assistant (`built_in_projects/code_assistant/`)

A structured software engineering workflow plan. Uses code assistant faculties (shell, search, git, editor) to perform coding tasks as transparent, inspectable NormCode inferences:

1. **Receive**: Accept task description
2. **Explore**: Parallel codebase discovery (grep, glob, git status)
3. **Plan**: LLM generates change plan, shown for approval
4. **Implement**: Surgical edits with lint-fix inner loops
5. **Verify**: Parallel test/build/typecheck with recovery
6. **Report**: Git diff summary and optional commit

Each step is a visible node on the canvas graph that can be breakpointed, inspected, value-overridden, or re-run selectively.

---

## See Also

- **[User Guide](canvas_app_user_guide.md)**: Detailed usage instructions
- **[API Reference](canvas_app_api_reference.md)**: REST and WebSocket API
- **[Canvas Integration Guide](canvas_integration_guide.md)**: Three-perspective architecture
- **[Chat System Guide](canvas_app_chat_system.md)**: Chat controllers and lifecycle
- **[Debugging Guide](canvas_app_debugging_guide.md)**: DB Inspector and log analysis
- **[Settings Guide](canvas_app_settings_guide.md)**: LLM, deployment, export/import
- **[Implementation Plan](implementation_plan.md)**: Remaining work
