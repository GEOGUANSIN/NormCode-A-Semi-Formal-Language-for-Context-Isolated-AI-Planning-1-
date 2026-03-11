# NormCode Tools

**User-facing tools and interfaces for working with NormCode plans.**

---

## Ecosystem Context

In the [NormCode Ecosystem](../1_intro/ecosystem.md), this section covers the **Product Operator** tools — the products used to inspect, debug, deploy, and manage NormCode plans:

| Product | Role | Description |
|---------|------|-------------|
| **Canvas** | Product Operator | Visual debugging, step-by-step inspection, multi-agent config, audit trails |
| **Server** | Product Operator | Standalone deployment server for remote execution and team collaboration |
| **Clients** | End User | Purpose-built interfaces for end users of deployed plans |

These products span the **Review → Run → Modify → Deploy** stages of the [lifecycle](../1_intro/ecosystem.md#the-lifecycle).

---

## Overview

This section documents the tools that enable users to create, execute, debug, and audit NormCode plans. The primary tool is the **Graph Canvas App**—a unified visual interface that brings together all aspects of working with NormCode. The **NormCode Server** provides deployment and remote execution capabilities.

---

## The Graph Canvas App

The Graph Canvas App is a standalone React/FastAPI application designed around a core principle: **the inference graph IS the interface**.

### Current Status: ✅ Production Ready (v0.8.0)

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1**: Foundation | ✅ Complete | Graph display, node visualization |
| **Phase 2**: Execution | ✅ Complete | Real-time execution, WebSocket events |
| **Phase 3**: Debugging | ✅ Complete | Breakpoints, stepping, tensor inspection |
| **Phase 4**: Modification | ✅ Complete | Value override, function modification, selective re-run |
| **Phase 5**: Polish | 🔄 In Progress | Keyboard shortcuts, search, export |

### Key Capabilities

| Capability | Status | Description |
|------------|--------|-------------|
| **Visualize** | ✅ | See the full inference graph with function and value nodes |
| **Execute** | ✅ | Run plans with live progress on the graph |
| **Debug** | ✅ | Set breakpoints, step through, inspect state |
| **Inspect** | ✅ | View tensors, logs, and execution context at any node |
| **Project Management** | ✅ | IDE-like project system with persistence |
| **Multi-Agent** | ✅ | Configure multiple agents with different LLMs |
| **Editor** | ✅ | Integrated NormCode file editor |
| **Modify** | ✅ | Override values, change paradigms, selective re-run |
| **Checkpoint/Resume** | ✅ | Resume or fork from saved checkpoints |
| **Code Assistant Tools** | ✅ | Shell, search, git, and editor tools for software engineering plans |
| **Semantic Memory** | ✅ | Cross-session memory storage and retrieval via mem0 |

---

## Documentation

### User Documentation

| Document | Description |
|----------|-------------|
| **[Canvas App Overview](canvas_app_overview.md)** | Architecture, concepts, and system design |
| **[Canvas App User Guide](canvas_app_user_guide.md)** | Complete usage guide |
| **[Canvas App API Reference](canvas_app_api_reference.md)** | REST API, WebSocket events, and stores |

### System Guides

| Document | Description |
|----------|-------------|
| **[Canvas Integration Guide](canvas_integration_guide.md)** | Three-perspective architecture (`me`/`you`/`it`), faculties, facades |
| **[Chat System Guide](canvas_app_chat_system.md)** | Chat controllers, lifecycle, building chat-driven NormCode plans |
| **[Debugging & Auditing Guide](canvas_app_debugging_guide.md)** | DB Inspector, Execution Log Viewer, data trace, step pipeline |
| **[Settings & Configuration Guide](canvas_app_settings_guide.md)** | LLM providers, GIM, Python env, deployment, export/import |

### Deployment

| Document | Description |
|----------|-------------|
| **[NormCode Server Guide](normcode_server_guide.md)** | Standalone deployment server — REST API, plan management, remote execution, auth |

### Planning & Development

| Document | Description |
|----------|-------------|
| **[Implementation Plan](implementation_plan.md)** | Remaining work and roadmap |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm 9+

### LLM Configuration (settings.yaml)

Create `settings.yaml` in the project root to configure LLM API keys:

```yaml
qwen-plus:
    DASHSCOPE_API_KEY: sk-your-api-key-here

gpt-4o:
    OPENAI_API_KEY: sk-your-openai-key-here

claude-3-sonnet:
    ANTHROPIC_API_KEY: sk-your-anthropic-key-here
```

**Note**: The `demo` mode is always available without an API key for testing.

### Running the App

```powershell
# From project root
cd canvas_app
python launch.py
```

The launcher automatically checks and installs dependencies on first run.

**Launcher Options:**
```powershell
python launch.py              # Start in dev mode (default)
python launch.py --prod       # Production mode (no auto-reload)
python launch.py --install    # Force reinstall all dependencies
python launch.py --skip-deps  # Skip dependency checks (faster startup)
python launch.py --backend-only   # Only start backend
python launch.py --frontend-only  # Only start frontend
python launch.py --kill       # Kill existing servers before starting
```

**Access Points:**
- **App**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws/events

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CANVAS APP                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Frontend (React + TypeScript + Vite)                                    │
│  ├── Graph Canvas (React Flow)                                          │
│  ├── Control Panel (execution controls)                                 │
│  ├── Detail Panel (node inspection, tensor viewer)                      │
│  ├── Agent Panel (multi-agent configuration)                            │
│  ├── Editor Panel (NormCode file editing)                               │
│  ├── Log Panel (real-time execution logs)                               │
│  └── Project Panel (project management)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│  Backend (FastAPI + Python)                                              │
│  ├── Execution Service (Orchestrator wrapper)                           │
│  ├── Graph Service (graph building & layout)                            │
│  ├── Agent Service (multi-agent registry)                               │
│  ├── Body Faculty Manager (tool declaration & injection)                │
│  ├── Project Service (project management)                               │
│  └── WebSocket Events (real-time updates)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  NormCode Infrastructure (infra/)                                        │
│  ├── Orchestrator (execution engine)                                    │
│  ├── ConceptRepo / InferenceRepo                                        │
│  └── Agent Body & Faculties (LLM, shell, search, git, editor, etc.)    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## The Two Node Types

The graph displays two fundamentally different kinds of nodes:

### Value Nodes (Data)
- Contain **References** (multi-dimensional tensors)
- Show **axes**, **shape**, and **data preview**
- Represent the data flowing through the plan
- Expandable to show full tensor contents via TensorInspector

### Function Nodes (Operations)
- Contain **sequences** (imperative, grouping, looping, etc.)
- Show **paradigm** and **working interpretation**
- Represent the operations transforming data
- Expandable to show execution pipeline status

---

## Execution Control

### Control Actions

| Control | Description |
|---------|-------------|
| **▶ Run** | Execute all ready inferences |
| **⏸ Pause** | Stop after current inference |
| **⏭ Step** | Execute exactly one inference |
| **🎯 Run to** | Execute until selected node |
| **🔄 Reset** | Reset execution and start fresh |

### Breakpoints

| Type | Behavior |
|------|----------|
| **Unconditional** | Always pause at this node |
| **Per-node toggle** | Click BP button in detail panel |

---

## Project Management

The canvas app operates like an IDE with project-based workflow:

- **Project Config**: `{name}.normcode-canvas.json` in project directory
- **Project Registry**: `~/.normcode-canvas/project-registry.json`
- **Multiple Projects**: Same directory can have multiple project configs
- **Persistence**: Breakpoints, settings, and state saved per project

---

## Relationship to Other Sections

| Section | Ecosystem Product | Relationship |
|---------|------------------|--------------|
| **[1. Introduction](../1_intro/README.md)** | — | Ecosystem overview, philosophy, quickstart |
| **[2. Grammar](../2_grammar/README.md)** | Language | Tools work with `.ncd` format (via compilation) |
| **[3. Execution](../3_execution/README.md)** | Agent | Tools integrate with the Orchestrator |
| **[4. Compilation](../4_compilation/README.md)** | Compiler | Tools load compiled repositories |
| **[6. Built-in Plans](../6_normcode_built-in/README.md)** | All | Plans that run inside Canvas (Canvas Assistant, Code Assistant, etc.) |

---

## Body Faculty System

The NormCode runtime provides tools to plans via the **Body** object. Each tool is a "faculty" — a named capability that gets injected into the execution context and is accessible by paradigms during plan execution.

All faculties are declared in `body_faculty_manager.py` and automatically wrapped with monitoring proxies for the Agent Panel.

### Core Faculties

| Faculty | Body Attribute | Purpose |
|---------|---------------|---------|
| `llm` | `body.llm` | Language model (text generation, structured output) |
| `file_system` | `body.file_system` | File I/O (read, write, list, exists) |
| `python_interpreter` | `body.python_interpreter` | Python script execution via subprocess |
| `prompt` | `body.prompt_tool` | Prompt template loading and rendering |
| `user_input` | `body.user_input` | Human-in-the-loop blocking input |
| `gim` | `body.gim_tool` | Generative image model (text-to-image) |
| `paradigm` | `body.paradigm_tool` | Paradigm file loading |

### Canvas Faculties

| Faculty | Body Attribute | Purpose |
|---------|---------------|---------|
| `chat` | `body.chat` | Chat interface (write, confirm, notify) |
| `canvas` | `body.canvas` | Canvas display and graph manipulation |
| `parser` | `body.parser` | NormCode parsing and serialization |
| `model_runner` | `body.model_runner` | Paradigm/model execution |
| `composition` | `body.composition_tool` | Function composition for paradigms |
| `perception` | `body.perception_router` | Perceptual sign routing |
| `formatter` | `body.formatter_tool` | Data formatting and parsing |

### Code Assistant Faculties

These tools enable NormCode plans to perform software engineering tasks — searching codebases, editing files surgically, running shell commands, and managing git repositories.

| Faculty | Body Attribute | Purpose |
|---------|---------------|---------|
| `shell` | `body.shell` | Shell command execution with timeout, background process management, dangerous command blocking |
| `search` | `body.search` | Code search via ripgrep (grep, glob, find definitions, find references) |
| `git` | `body.git` | Git operations (status, diff, log, add, commit, branch, checkout, stash) |
| `editor` | `body.editor` | Surgical file editing (exact text replacement, line insertion/deletion, file creation) |
| `memory` | `body.memory` | Semantic memory (cross-session storage and retrieval via mem0) |

Code assistant faculties are injected via `inject_code_tools()` in `tool_injection.py` and are configurable per agent in the Agent Panel.

### Faculty Registration

Adding a new tool requires:
1. Create the tool class in `canvas_app/backend/tools/`
2. Add a `FacultySpec` to `FACULTY_SPECS` in `body_faculty_manager.py`
3. Add creation logic in the appropriate `create_*` method
4. The tool automatically gets monitoring (Agent Panel visibility) and WebSocket event emission

---

## Built-in Projects

The Canvas App includes built-in projects that serve as interactive assistants. These are NormCode plans that run inside the canvas and use the faculty system to interact with the user and the environment. For detailed walkthroughs of all built-in plans (including non-Canvas plans like PPT Generation, NC Compilations, and BOM Matching), see **[Section 6: Built-in Plans](../6_normcode_built-in/README.md)**.

### Canvas Assistant

**Location**: `canvas_app/built_in_projects/canvas_assistant/`

A chat-driven controller for the canvas itself. It classifies user commands (navigation, execution control, queries) and executes them via the Canvas Integration Tool. Uses `me.vision` (read UI state), `me.hands` (UI actions), and `me.mind` (execution control) perspectives.

### Code Assistant (In Development)

**Location**: `canvas_app/built_in_projects/code_assistant/`

A structured software engineering workflow expressed as a NormCode plan. Uses shell, search, git, and editor tools to perform coding tasks with full transparency:

- **Explore**: Parallel codebase discovery (grep, glob, file reads, git status)
- **Plan**: LLM generates a change plan, shown to user for approval
- **Implement**: Surgical edits with lint-fix inner loops
- **Verify**: Parallel test/build/typecheck with automatic recovery
- **Report**: Git diff summary and optional commit

Each step is a visible, inspectable, overridable node on the canvas graph. See the [Code Assistant README](../../canvas_app/built_in_projects/code_assistant/README.md) for the full design.

---

## Clients

**Clients** are purpose-built interfaces for end users of deployed NormCode plans. While the Canvas is for operators who debug and manage plans, Clients are for the people who *use* the finished product.

Examples:
- **PPT Generator** — an interactive web UI for generating presentations, deployed on the [NormCode Server](normcode_server_guide.md)
- **Workflow Runner** — a CLI client for executing plans and streaming results
- **Custom dashboards** — any frontend that calls the Server's REST API

Clients communicate with the NormCode Server via its REST API and SSE/WebSocket event streams. Each deployed plan can have multiple client interfaces tailored to different user needs.

See the [NormCode Server Guide](normcode_server_guide.md) for the API that clients connect to, and the [Ecosystem Overview](../1_intro/ecosystem.md) for how Clients fit into the 3-role model.

---

## Legacy Tools

While the Graph Canvas App is the primary tool, legacy tools include:

| Tool | Location | Description |
|------|----------|-------------|
| **CLI Orchestrator** | `cli_orchestrator.py` | Command-line execution |
| **Streamlit App** | `streamlit_app/` | Web UI for execution (legacy) |
| **Editor App** | `editor_app/` | React/FastAPI editor (legacy) |

---

## Next Steps

See the [Implementation Plan](implementation_plan.md) for remaining work and roadmap.

---

**Version**: 0.9.0  
**Last Updated**: March 2026
