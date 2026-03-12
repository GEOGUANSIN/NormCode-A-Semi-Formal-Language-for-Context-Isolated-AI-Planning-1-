# NormCode Server Guide

**The NormCode Server is a standalone deployment server for executing NormCode plans remotely — the "Deploy" stage of the NormCode lifecycle.**

---

## Overview

The NormCode Server (`canvas_app/normal_server/`) is a self-contained FastAPI server that enables teams to deploy, manage, and execute NormCode plans in a shared environment. It provides REST APIs for plan management, run control, and real-time event streaming.

```
┌─────────────────────────────────────────────────────────────┐
│                    NormCode Server                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Plan Management ──▶ Run Execution ──▶ Result Delivery      │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│  │  Deploy   │   │  Execute │   │  Stream  │               │
│  │  plans    │   │  plans   │   │  events  │               │
│  │  (upload/ │   │  (start/ │   │  (SSE/   │               │
│  │  manage)  │   │  pause/  │   │  WebSocket│               │
│  │           │   │  resume) │   │  /REST)  │               │
│  └──────────┘   └──────────┘   └──────────┘               │
│                                                             │
│  Auth (Redis)    DB Inspector    Canvas Integration          │
└─────────────────────────────────────────────────────────────┘
```

### In the Ecosystem

| Lifecycle Stage | Product | Role |
|----------------|---------|------|
| Describe → Compile | Language + Compiler | Agent Designer |
| Review → Run → Modify | **Canvas** | Product Operator |
| **Deploy** | **Server** | Product Operator |
| Use | Clients | End User |

The Server is the bridge between the Canvas (where you debug and test) and the Clients (where end users interact with finished agents).

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend dashboard)
- Redis (for authentication)

### Installation

```powershell
cd canvas_app/normal_server

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (dashboard UI)
npm install

# Configure LLM settings
# Edit data/config/settings.yaml with your API keys
```

### Starting the Server

**Method 1: Interactive Launcher (Recommended)**

```powershell
python launch.py
```

The interactive menu provides options to start the server, configure LLM settings, check dependencies, and monitor health.

Quick start shortcuts:

```powershell
python launch.py --quick              # Start with defaults
python launch.py --quick --monitor    # Start and open dashboard
```

**Method 2: Direct Start**

```powershell
python server.py
python server.py --port 9000 --host 0.0.0.0
python server.py --reload    # Auto-reload for development
```

**Method 3: Start Script**

```powershell
python scripts/start_server.py
python scripts/start_server.py --port 9000
```

### Common Options

| Option | Default | Description |
|--------|---------|-------------|
| `--port` | `8080` | Server port |
| `--host` | `0.0.0.0` | Host to bind |
| `--plans-dir` | `data/plans/` | Plans directory |
| `--runs-dir` | `data/runs/` | Runs directory |
| `--reload` | off | Enable auto-reload for development |

### Access Points

| Endpoint | Description |
|----------|-------------|
| `http://localhost:8080/health` | Health check |
| `http://localhost:8080/docs` | Interactive API docs (Swagger) |
| `http://localhost:8080/info` | Server information |
| `http://localhost:8080/server/ui` | Server dashboard |

---

## REST API

### Plan Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/plans` | List deployed plans |
| `GET` | `/api/plans/{plan_id}` | Get plan details |
| `GET` | `/api/plans/{plan_id}/graph` | Get full graph data (concepts + inferences) |
| `GET` | `/api/plans/{plan_id}/files/{path}` | Get plan files (prompts, paradigms) |
| `POST` | `/api/plans/deploy-file` | Deploy a plan (zip upload) |
| `DELETE` | `/api/plans/{plan_id}` | Remove a plan |
| `DELETE` | `/api/plans` | Remove all plans |

### Run Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/runs` | Start a new run |
| `GET` | `/api/runs` | List all runs (active + historical) |
| `GET` | `/api/runs/{run_id}` | Get run status |
| `GET` | `/api/runs/{run_id}/result` | Get run result |
| `POST` | `/api/runs/{run_id}/resume` | Resume from checkpoint |
| `POST` | `/api/runs/{run_id}/stop` | Stop execution |
| `DELETE` | `/api/runs` | Remove all runs |

### Run Database Inspector

Remote inspection of run databases for debugging and analysis:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/runs/{run_id}/db/overview` | Database structure and statistics |
| `GET` | `/api/runs/{run_id}/db/executions` | Execution history |
| `GET` | `/api/runs/{run_id}/db/executions/{id}/logs` | Detailed logs for an execution |
| `GET` | `/api/runs/{run_id}/db/statistics` | Status counts, cycles |
| `GET` | `/api/runs/{run_id}/db/checkpoints` | List checkpoints |
| `GET` | `/api/runs/{run_id}/db/checkpoints/{cycle}` | Get checkpoint state |
| `GET` | `/api/runs/{run_id}/db/blackboard` | Blackboard summary |
| `GET` | `/api/runs/{run_id}/db/concepts` | Completed concepts with data previews |

### Server Info

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/info` | Server information |
| `GET` | `/api/models` | Available LLM models |
| `GET` | `/api/connect` | Connection info for Canvas integration |
| `POST` | `/api/server/reset` | Full server reset |

---

## Deploying Plans

### Option 1: HTTP Upload

```powershell
curl -X POST http://localhost:8080/api/plans/deploy-file -F "plan=@my-plan.zip"
```

### Option 2: Direct Copy

Copy a compiled plan folder directly into the plans directory:

```powershell
Copy-Item -Recurse .\my-plan\ .\data\plans\my-plan\
```

### Running a Plan

```powershell
curl -X POST http://localhost:8080/api/runs `
  -H "Content-Type: application/json" `
  -d '{"plan_id": "my-plan", "llm_model": "qwen-plus"}'
```

### Checkpoint Resume

Resume a run from its latest checkpoint, or fork from a specific cycle:

```powershell
# Resume from latest
curl -X POST http://localhost:8080/api/runs/{run_id}/resume

# Fork from cycle 5
curl -X POST "http://localhost:8080/api/runs/{run_id}/resume?cycle=5&fork=true"
```

---

## Authentication

The server uses Redis-backed authentication with admin accounts managed via a CLI tool.

### Setting Up Redis

```powershell
# Via Docker (recommended on Windows)
docker run -d -p 6379:6379 redis
```

### Creating Admin Accounts

```powershell
python -m scripts.admin_manager
```

The interactive tool allows creating, listing, and deleting admin accounts.

**Account requirements:**
- Username: 5+ characters, letters/numbers/underscores
- Password: 8+ characters with uppercase, lowercase, numbers, and symbols

### Configuration

Default Redis connection: `localhost:6379`, database `0`. Modify via constants in `scripts/admin_manager.py`.

---

## Canvas App Integration

The NormCode Canvas App connects to the Server for remote project loading, execution, and debugging.

### How It Works

```
┌─────────────────┐       HTTP/SSE        ┌──────────────────┐
│   Canvas App    │◄─────────────────────►│  NormCode Server │
│                 │                        │                  │
│ RemoteProxy     │  POST /api/runs       │  Plan Manager    │
│ Executor        │──────────────────────►│                  │
│                 │                        │  Run Engine      │
│ Deployment      │  GET /api/runs/X/     │                  │
│ Panel           │  stream               │  (SSE events)    │
│                 │◄──────────────────────│                  │
└─────────────────┘                        └──────────────────┘
```

### Connection Flow

1. **Add server** in Canvas Deployment Panel
2. **Check health** — verify connectivity
3. **Deploy** — upload project to server
4. **Run** — execute remotely with live SSE event stream
5. **Inspect** — use DB Inspector endpoints for remote debugging

### Key Integration Endpoints

| Endpoint | Used For |
|----------|----------|
| `GET /api/connect` | Verify connectivity, get server capabilities |
| `GET /api/plans/{plan_id}/manifest` | Load plan into Canvas tab |
| `GET /api/runs/{run_id}/stream` | Real-time SSE event stream |
| `POST /api/runs/{run_id}/pause` | Remote execution control |
| `POST /api/runs/{run_id}/continue` | Resume paused execution |
| `POST /api/runs/{run_id}/step` | Step-by-step remote execution |

### SSE Event Types

Events streamed via `/api/runs/{run_id}/stream`:

| Event | Description |
|-------|-------------|
| `connected` | Initial connection with full state |
| `node:statuses` | Batch node status update |
| `inference:started` | Inference execution began |
| `inference:completed` | Inference finished successfully |
| `inference:failed` | Inference failed |
| `execution:progress` | Progress update |
| `execution:paused` | Execution paused |
| `execution:resumed` | Execution resumed |
| `execution:stopped` | Execution stopped |
| `breakpoint:hit` | Breakpoint reached |
| `run:completed` | Run finished |
| `run:failed` | Run failed |

---

## Web UI Clients

The server bundles several web UI clients for interacting with deployed plans:

| Client | URL | Description |
|--------|-----|-------------|
| **Server Dashboard** | `/server/ui` | Plan management, run monitoring |
| **PPT Generator** | `/ppt/ui` | Interactive presentation generation |
| **Legacy Monitor** | `/monitor/ui` | Run monitoring |
| **Legacy Client** | `/client/ui` | Basic plan execution |

These are examples of **Clients** — the end-user-facing product in the NormCode ecosystem. Each deployed plan can have purpose-built UI clients tailored to its specific use case.

---

## LLM Configuration

Edit `data/config/settings.yaml`:

```yaml
BASE_URL: https://dashscope.aliyuncs.com/compatible-mode/v1

qwen-plus:
  model: qwen-plus
  api_key: your-api-key-here

gpt-4o:
  model: gpt-4o
  api_key: your-openai-key
  base_url: https://api.openai.com/v1
```

---

## Directory Structure

```
normal_server/
├── server.py              # Main server code
├── launch.py              # Interactive launcher
├── runner.py              # Plan execution (shared module)
├── routes/                # API route modules
├── tools/                 # Deployment tools
├── infra/                 # Core NormCode library
├── scripts/
│   ├── pack.py            # Plan packager
│   ├── admin_manager.py   # Super admin CLI
│   └── start_server.py    # Server start script
├── mock_users/
│   ├── client.py          # CLI test client
│   └── client_gui.py      # GUI test client
├── data/
│   ├── plans/             # Deploy plans here
│   ├── runs/              # Run data (auto-created)
│   └── config/
│       └── settings.yaml  # LLM configuration
└── requirements.txt
```

---

## Additional Launcher Commands

```powershell
python launch.py --check       # Check dependencies only
python launch.py --setup       # Configure LLM settings
python launch.py --status      # Show server status
python launch.py --watchdog    # Start with auto-restart watchdog
python launch.py --health      # Health check on running server
python launch.py --crashes     # Analyze crash reports
```

---

## See Also

- **[Ecosystem Overview](../1_intro/ecosystem.md)** — Where the Server fits in the lifecycle
- **[Canvas App Overview](canvas_app_overview.md)** — The visual debugging tool that connects to the Server
- **[Settings & Configuration Guide](canvas_app_settings_guide.md)** — Deployment Panel configuration in Canvas
- **[Debugging & Auditing Guide](canvas_app_debugging_guide.md)** — Remote DB inspection via Server endpoints
- **[Implementation Plan](implementation_plan.md)** — Development roadmap

---

**Version**: 0.9.0
**Last Updated**: March 2026
