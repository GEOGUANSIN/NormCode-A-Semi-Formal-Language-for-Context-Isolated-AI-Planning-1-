# Canvas App User Guide

**A complete guide to using the NormCode Graph Canvas App for executing, debugging, and auditing NormCode plans.**

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm 9 or higher

### Installation & Running

The launcher automatically checks and installs dependencies on first run:

```powershell
cd canvas_app
python launch.py
```

The launcher will:
1. Check for Python dependencies (FastAPI, uvicorn, etc.)
2. Check for Node.js dependencies (React, Vite, etc.)
3. Install any missing dependencies automatically
4. Start both backend (port 8000) and frontend (port 5173) servers

### Launcher Options

```powershell
python launch.py              # Start in dev mode (default)
python launch.py --prod       # Production mode (no auto-reload)
python launch.py --install    # Force reinstall all dependencies
python launch.py --skip-deps  # Skip dependency checks (faster startup)
python launch.py --backend-only   # Only start backend server
python launch.py --frontend-only  # Only start frontend server
python launch.py --kill       # Kill existing servers before starting (Windows)
```

### LLM Configuration

Create `settings.yaml` in the project root to configure LLM API keys:

```yaml
# settings.yaml - LLM Model Configuration
qwen-plus:
    DASHSCOPE_API_KEY: sk-your-api-key-here

qwen-turbo-latest:
    DASHSCOPE_API_KEY: sk-your-api-key-here

gpt-4o:
    OPENAI_API_KEY: sk-your-openai-key-here

claude-3-sonnet:
    ANTHROPIC_API_KEY: sk-your-anthropic-key-here
```

**Note**: The `demo` mode is always available without an API key for testing.

### Manual Setup (Optional)

If you prefer to install dependencies manually:

1. **Install Backend Dependencies**
```powershell
cd canvas_app/backend
pip install -r requirements.txt
```

2. **Install Frontend Dependencies**
```powershell
cd canvas_app/frontend
npm install
```

3. **Run Separately**

Terminal 1 (Backend):
```powershell
cd canvas_app/backend
uvicorn main:app --reload --port 8000
```

Terminal 2 (Frontend):
```powershell
cd canvas_app/frontend
npm run dev
```

### Access Points

| URL | Purpose |
|-----|---------|
| http://localhost:5173 | Main application |
| http://localhost:8000/docs | API documentation (Swagger) |
| ws://localhost:8000/ws/events | WebSocket connection |

---

## Project Management

### Welcome Screen

When you first open the app (or have no project open), you'll see the **Welcome Screen**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Welcome to NormCode Canvas                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Recent Projects:                                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 📁 Gold Analysis          C:/projects/gold  Today 15:30  │  │
│  │ 📁 Contract Parser        C:/projects/legal Yesterday    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│            [Open Project]     [New Project]                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Creating a New Project

1. Click **"New Project"**
2. Enter project details:
   - **Name**: Display name for the project
   - **Directory**: Path to the project folder
   - **Description**: Optional description
3. Configure repository paths:
   - **Concepts**: Path to `.concept.json` file
   - **Inferences**: Path to `.inference.json` file
   - **Inputs**: Path to `.inputs.json` file (optional)
4. Click **"Create"**

The app creates a `{name}.normcode-canvas.json` config file in the project directory.

### Opening an Existing Project

**Option 1: Recent Projects**
- Click any project in the Recent Projects list

**Option 2: Open by Path**
1. Click **"Open Project"**
2. Enter the project directory path
3. If multiple project configs exist, choose which to open
4. Click **"Open"**

**Option 3: Scan Directory**
1. Click **"Open Project"**
2. Enter a directory path
3. Click **"Scan"** to discover all project configs
4. Select the desired project

### Project Settings

Access project settings via the **folder icon** in the header or press `Ctrl+,`:

- View/edit project name and description
- Configure repository paths
- View project directory and config file location

---

## Main Interface

### Layout Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Header: [Logo] [Project Name] [Loaded] | [Canvas] [Editor] | [Panels] │
├─────────────────────────────────────────────────────────────────────────┤
│  Settings Panel (collapsible)                                           │
├─────────────────────────────────────────────────────────────────────────┤
│  Control Panel: [▶ Run] [⏸ Pause] [⏭ Step] [⏹ Stop] [🔄 Reset]         │
├──────────┬─────────────────────────────────────────────┬────────────────┤
│  Agent   │              Graph Canvas                   │   Detail       │
│  Panel   │                                             │   Panel        │
│          │   ┌───────┐     ┌───────┐     ┌───────┐    │                │
│          │   │ Node  │────▶│ Node  │────▶│ Node  │    │   [Node Info]  │
│          │   └───────┘     └───────┘     └───────┘    │   [Tensor]     │
│          │                                             │   [Connections]│
├──────────┴─────────────────────────────────────────────┴────────────────┤
│  Log Panel: [Filter▼] [Clear]                                           │
│  10:32:15 | 1.2.1 | INFO | Starting inference...                        │
├─────────────────────────────────────────────────────────────────────────┤
│  Status Bar: Ready • 75 nodes • 77 edges           path/to/project  🟢  │
└─────────────────────────────────────────────────────────────────────────┘
```

### View Modes

Toggle between two view modes using the tabs in the header:

| Mode | Purpose |
|------|---------|
| **Canvas** | Graph visualization and execution |
| **Editor** | NormCode file editing |

---

## Canvas View

### Graph Navigation

| Action | Gesture | Keyboard |
|--------|---------|----------|
| Pan | Drag canvas | — |
| Zoom | Scroll wheel | — |
| Select node | Click | — |
| Center on node | Double-click | — |
| Fit view | — | Click "Fit" button |

### Node Appearance

**Node Colors by Category**:

| Color | Category | Examples |
|-------|----------|----------|
| Purple | Semantic function | `::(analyze)`, `:<extract>` |
| Blue | Semantic value | `{result}`, `<item>`, `[list]` |
| Gray | Syntactic function | `$collect`, `&assign` |

**Node Markers**:

| Marker | Meaning |
|--------|---------|
| Double border | Ground concept (input data) |
| Red ring | Output concept (final result) |
| Red badge | Breakpoint set |

**Status Indicators** (dot in top-right corner):

| Color | Status |
|-------|--------|
| Gray | Pending |
| Blue (pulsing) | Running |
| Green | Completed |
| Red | Failed |
| Striped | Skipped |

### Layout Options

Click the layout button in the canvas toolbar:

| Layout | Description |
|--------|-------------|
| **Tree** | Hierarchical tree layout (default) |
| **Compact** | Tighter spacing for large graphs |

---

## Execution Control

### Control Panel Buttons

| Button | Action | Shortcut |
|--------|--------|----------|
| **▶ Run** | Start/continue execution | — |
| **⏸ Pause** | Pause after current inference | — |
| **⏭ Step** | Execute one inference | — |
| **⏹ Stop** | Stop execution | — |
| **🔄 Reset** | Reset to beginning | — |

### Breakpoints

**Setting a Breakpoint**:
1. Select a node in the graph
2. In the Detail Panel, click the **"+ BP"** button
3. A red badge appears on the node

**Breakpoint Behavior**:
- Execution pauses **before** executing the breakpoint node
- Click **Run** to continue past the breakpoint
- Click **Step** to execute just that node

**Clearing a Breakpoint**:
1. Select the node
2. Click the breakpoint button again

### "Run To" Feature

Execute until a specific node, then pause:

1. Select a **pending** node
2. In the Detail Panel, click **"Run To"**
3. Execution runs until that node completes, then pauses

### Progress Tracking

The Control Panel shows:
- **Progress bar**: Completed / Total inferences
- **Current inference**: Flow index being executed
- **Cycle count**: Number of execution cycles

---

## Detail Panel

### Panel Sections

When you select a node, the Detail Panel shows:

**1. Identity & Status**
- Node name (natural name if available)
- Concept ID
- Status badge
- Node type (value/function)
- Flow index

**2. Debugging Actions**
- **+ BP** / **- BP**: Toggle breakpoint
- **Run To**: Run until this node

**3. Pipeline** (function nodes only)
- Current step in execution pipeline
- Paradigm information

**4. Axes** (value nodes only)
- Axis names for the tensor
- Dimension information

**5. Function Details** (function nodes only)
- Sequence type
- Paradigm name
- Value order
- Prompt location
- Output type

**6. Connections**
- Incoming connections (sources)
- Outgoing connections (targets)
- Click any connection to navigate to that node

**7. Reference Data** (value nodes only)
- TensorInspector for viewing tensor data
- Refresh button to reload

### Fullscreen Mode

Click the **expand icon** in the panel header to view in fullscreen:
- Two-column layout
- Larger tensor viewer
- Click backdrop to close

---

## Tensor Inspection

### TensorInspector Views

| Dimensions | View |
|------------|------|
| 0D (scalar) | Single value display |
| 1D | Horizontal cards or vertical list |
| 2D | Table with row/column headers |
| 3D+ | Axis selector + slice sliders |

### N-Dimensional Navigation

For tensors with 3+ dimensions:

1. **Select display axes**: Choose which 2 axes to show as rows/columns
2. **Adjust sliders**: Set the index for other axes
3. **View mode**: Switch between Table, List, and JSON views

### Perceptual Signs

Values like `%c2a({'action': 'BUY', 'confidence': 0.82})` are automatically parsed:

```
┌─────────────────────────────────┐
│ %c2a{2 keys}                    │
├─────────────────────────────────┤
│   action: BUY                   │
│   confidence: 0.82              │
└─────────────────────────────────┘
```

---

## Log Panel

### Log Display

The Log Panel shows real-time execution logs:

```
10:32:15 | 1.2.1 | INFO  | Starting inference for {analysis_result}
10:32:16 | 1.2.1 | INFO  | Executing paradigm h_PromptTemplate-c_GenerateJson
10:32:18 | 1.2.1 | INFO  | LLM response received (1247 tokens)
10:32:18 | 1.2.1 | INFO  | Inference completed
```

### Log Filtering

| Filter | Description |
|--------|-------------|
| **Level filter** | Show only errors, warnings, or all |
| **Node filter** | Show only logs for selected node |
| **Search** | Filter by text content |

### Node-Specific Logs

1. Select a node in the graph
2. Click the **filter icon** in the Log Panel
3. Only logs for that node (and global logs) are shown
4. Matching logs are highlighted in purple

---

## Agent Panel

### Agent Configuration

The Agent Panel (left sidebar) allows configuring multiple agents:

**Agent List**:
- View all registered agents
- Click to select/edit
- **+ New** to create a new agent

**Agent Settings**:
- **LLM Model**: qwen-plus, gpt-4o, claude-3, etc.
- **Temperature**: 0.0 - 2.0
- **Max Tokens**: Response limit
- **Core Tools**: Enable/disable file system, Python interpreter, user input
- **Code Assistant Tools**: Enable/disable shell, search, git, editor (collapsible section)

### Code Assistant Tool Configuration

The Agent Editor modal includes a "Code Assistant Tools" section with individually configurable tools:

| Tool | Settings | Description |
|------|----------|-------------|
| **Shell** | `enabled`, `timeout` (seconds) | Run terminal commands with timeout |
| **Search** | `enabled` | Code search via ripgrep (grep, glob, symbols) |
| **Git** | `enabled`, `allow_commits` | Git operations with commit control |
| **Editor** | `enabled`, `base_dir` | Surgical file editing with working directory |

Each tool card is expandable to reveal its settings. Tools disabled here will not be injected into the agent's Body during execution.

### Capabilities Display

For the selected agent, view:

**Tools**:
- LLM (`.ask()`, `.complete()`)
- File System (`.read()`, `.write()`)
- Python Interpreter (`.execute()`)
- User Input (`.prompt()`)
- Shell (`.run()`, `.run_background()`) — if enabled
- Search (`.grep()`, `.glob()`, `.find_definition()`) — if enabled
- Git (`.status()`, `.diff()`, `.commit()`) — if enabled
- Editor (`.edit()`, `.insert_at()`, `.create()`) — if enabled
- Memory (`.search()`, `.add()`) — if enabled

Quick capability icons appear in the Agent Panel header showing which tools are active at a glance.

**Paradigms**:
- Project paradigms (custom)
- Default paradigms (from infra)

**Sequences**:
- Available inference sequences
- Grouped by category

### Tool Call Monitoring

The Tool Calls section shows real-time tool usage. Each tool type is color-coded:

```
10:32:15 | 1.2.1 | llm.generate         | ⏳         (blue)
10:32:14 | 1.2.1 | prompt.load          | ✓ 12ms    (blue)
10:32:13 | 1.1.1 | shell.run            | ✓ 340ms   (teal)
10:32:12 | 1.1.1 | search.grep          | ✓ 85ms    (sky)
10:32:11 | 1.1.1 | git.status           | ✓ 15ms    (orange)
10:32:10 | 1.1.1 | editor.edit          | ✓ 8ms     (emerald)
```

Click any entry to view full details:
- Complete inputs
- Complete outputs (collapsible for large payloads)
- Duration
- Status

---

## Modification Features (Phase 4)

### Value Override

Override tensor values at any node during debugging:

1. Select a node in the graph
2. In the Detail Panel, click **"Override Value"**
3. Edit the tensor data in the dialog
4. Click **"Apply"** to set the new value

**Use Cases**:
- Test with different inputs without re-running entire plan
- Debug by injecting known values
- Experiment with edge cases

### Function Modification

Change how a function node executes:

1. Select a function node
2. In the Detail Panel, click **"Modify Function"**
3. Edit:
   - **Paradigm**: Change execution strategy
   - **Prompt**: Edit the prompt template
   - **Output Type**: Change expected output format
4. Click **"Apply"**

### Selective Re-run

Re-run execution from any node:

1. Select a node in the graph
2. Right-click or use the Detail Panel menu
3. Choose **"Re-run from here"**
4. The node and all its dependents will re-execute

**Note**: This uses the current values of upstream nodes.

### Checkpoint Resume & Fork

Resume or branch from saved execution states:

**Resume**:
1. Open Project Settings
2. Select a checkpoint from the dropdown
3. Click **"Resume"** to continue from that point

**Fork**:
1. Select a checkpoint
2. Click **"Fork"** to create a new branch
3. The forked execution starts from the checkpoint state
4. Original execution history is preserved

**Checkpoint Management**:
- Checkpoints are saved automatically at breakpoints
- Manual checkpoint: Click **"Save Checkpoint"** in Control Panel
- View checkpoint history in Project Settings

---

## Editor View

### File Browser

The left sidebar shows project files:

```
📁 repos
  📄 concept_repo.json
  📄 inference_repo.json
📁 provision
  📁 paradigm
    📄 h_Data-c_Pass.json
  📁 prompts
    📄 analyze.md
📄 example.ncd
```

**Supported Formats**:
| Extension | Icon | Color |
|-----------|------|-------|
| `.ncd` | Code | Blue |
| `.ncn` | Document | Gray |
| `.ncdn` | Hybrid | Cyan |
| `.concept.json` | Database | Cyan |
| `.inference.json` | Hash | Pink |
| `.py` | Python | Blue |
| `.md` | Markdown | Gray |
| `.yaml` | Config | Amber |

### File Editing

1. Click a file in the browser
2. Edit in the code editor
3. **Ctrl+S** to save

**Editor Features**:
- Syntax highlighting
- Line numbers
- Character/line count
- Unsaved indicator

### View Toggle

Switch between tree and flat views:
- **Tree**: Hierarchical folder structure
- **Flat**: All files in a list

---

## Settings Panel

### Execution Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **LLM Model** | Model for LLM operations | qwen-plus |
| **Max Cycles** | Maximum execution cycles | 100 |
| **DB Path** | Checkpoint database path | orchestration.db |
| **Base Directory** | Working directory | Project path |
| **Paradigm Directory** | Custom paradigm path | provision/paradigm |

### Changing Settings

1. Click **Settings** icon in header
2. Modify values
3. Changes apply on next repository load

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save file (Editor) |
| `Escape` | Close modal/fullscreen |

---

## Troubleshooting

### "WebSocket Disconnected"

The status bar shows a red dot:

1. Check if the backend is running
2. Refresh the page
3. Restart the backend server

### "Missing Files"

Project shows "Missing files" badge:

1. Verify concept.json and inference.json exist
2. Check paths in project config
3. Update paths in Project Settings

### "No Reference Data"

TensorInspector shows empty:

1. Node may not have been executed yet
2. Click **Refresh** button
3. Run execution first

### Graph Not Loading

After loading repositories, graph is empty:

1. Check browser console for errors
2. Verify JSON files are valid
3. Check backend logs

---

## Built-in Projects

The Canvas App includes pre-built NormCode projects that run inside the canvas.

### Canvas Assistant

The Canvas Assistant is a chat-driven controller for the canvas UI. It connects automatically when opened and accepts natural language commands in the Chat Panel:

- **Navigation**: "select node 1.2.1", "zoom in", "fit to view"
- **Execution**: "run the plan", "step once", "pause"
- **Queries**: "what is selected?", "show me the execution status"

The assistant uses the Canvas Integration Tool which provides three perspectives — Vision (read state), Hands (perform actions), and Mind (control execution).

### Code Assistant (In Development)

A structured coding workflow that uses code assistant tools (shell, search, git, editor) to perform software engineering tasks as visible NormCode plan steps. Each step is a graph node that can be inspected, breakpointed, and value-overridden.

### Agent Config Preview

When viewing `.agent.json` files in the Editor, the `AgentConfigPreview` component renders a formatted view showing:
- Agent name, model, temperature
- Enabled capability icons (quick visual indicator for shell, search, git, editor, etc.)
- Expandable tool configuration details
- Raw JSON toggle for manual editing

---

## Tips and Best Practices

### Efficient Debugging

1. **Set breakpoints early**: Place breakpoints before problem areas
2. **Use "Run To"**: Jump directly to nodes of interest
3. **Filter logs**: Focus on specific nodes to reduce noise
4. **Fullscreen tensor view**: Use for complex data inspection

### Performance

1. **Collapse panels**: Hide unused panels for larger graph view
2. **Minimize agent panel**: Only open when configuring agents
3. **Use compact layout**: For graphs with 100+ nodes

### Project Organization

1. **Descriptive names**: Use meaningful project names
2. **Multiple configs**: Create separate configs for different scenarios
3. **Clean breakpoints**: Clear breakpoints when no longer needed

---

## See Also

- **[Canvas App Overview](canvas_app_overview.md)**: Architecture and concepts
- **[API Reference](canvas_app_api_reference.md)**: REST and WebSocket API
- **[Canvas Integration Guide](canvas_integration_guide.md)**: Three-perspective architecture
- **[Chat System Guide](canvas_app_chat_system.md)**: Chat controllers and lifecycle
- **[Debugging Guide](canvas_app_debugging_guide.md)**: DB Inspector and log analysis
- **[Settings Guide](canvas_app_settings_guide.md)**: LLM, deployment, export/import
- **[Implementation Plan](implementation_plan.md)**: Remaining work
