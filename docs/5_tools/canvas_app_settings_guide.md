# Canvas App Settings & Configuration Guide

**LLM providers, GIM settings, Python environment, deployment, and project portability.**

---

## Introduction

The Canvas App has several configuration layers:
- **`settings.yaml`** — API keys and model definitions (file-based)
- **LLM Settings Panel** — Provider management with presets (UI-based)
- **GIM Settings Panel** — Generative image model configuration
- **Python Settings Panel** — Python environment and package management
- **Settings Panel** — Per-project execution settings
- **Deployment Panel** — Remote server management
- **Export/Import** — Portable project packages

---

## LLM Configuration

### settings.yaml (Quick Setup)

The simplest way to configure LLM access. Create `settings.yaml` in the project root:

```yaml
# Model name → API key mapping
qwen-plus:
    DASHSCOPE_API_KEY: sk-your-key-here

gpt-4o:
    OPENAI_API_KEY: sk-your-key-here

claude-3-5-sonnet:
    ANTHROPIC_API_KEY: sk-your-key-here

# Custom OpenAI-compatible endpoint
my-local-model:
    OPENAI_API_KEY: sk-local-key
    BASE_URL: http://localhost:8080/v1
```

The model name becomes available in the Settings Panel dropdown. `demo` mode is always available without any API key.

A template is provided at `canvas_app/settings.yaml.example`.

### LLM Settings Panel (Advanced)

For more control, use the LLM Settings Panel (accessible from the toolbar):

#### Supported Providers

| Provider | Key | Models |
|----------|-----|--------|
| **DashScope** (Alibaba/Qwen) | `DASHSCOPE_API_KEY` | qwen-plus, qwen-turbo, qwen-max, deepseek-r1-* |
| **OpenAI** | `OPENAI_API_KEY` | gpt-4o, gpt-4o-mini, gpt-3.5-turbo |
| **Anthropic** | `ANTHROPIC_API_KEY` | claude-3-5-sonnet, claude-3-opus |
| **Azure OpenAI** | (custom) | Azure-hosted models |
| **Ollama** | (none) | Local models via Ollama |
| **Custom** | (varies) | Any OpenAI-compatible endpoint |

#### Provider Configuration

Each provider is configured with:

```typescript
interface LLMProviderConfig {
  id: string;
  name: string;                    // Display name
  provider: LLMProvider;           // openai | anthropic | azure | dashscope | ollama | custom
  api_key?: string;                // API key (masked in UI)
  base_url?: string;               // Custom endpoint URL
  model: string;                   // Default model name
  temperature: number;             // 0.0 - 2.0
  max_tokens?: number;             // Response token limit
  top_p?: number;                  // Nucleus sampling
  is_default: boolean;             // Default provider for new agents
  is_enabled: boolean;             // Active/inactive toggle
}
```

#### Provider Presets

The panel includes presets for quick setup. Select a provider, enter your API key, and the preset auto-fills base URL and available models.

#### Testing

Each provider has a **Test** button that sends a simple prompt and verifies the connection works.

### Per-Agent Model Selection

Agents can use different LLM models. In the Agent Panel:
1. Select an agent
2. Change the **LLM Model** dropdown
3. Adjust **Temperature** and **Max Tokens**

This allows multi-agent setups where different inferences use different models (e.g., a fast model for classification, a capable model for generation).

### Frontend Store: `llmStore`

```typescript
interface LLMState {
  providers: LLMProviderConfig[];
  presets: LLMProviderPreset[];
  isLoading: boolean;
  
  fetchProviders(): Promise<void>;
  createProvider(config: CreateProviderRequest): Promise<void>;
  updateProvider(id: string, updates: Partial<LLMProviderConfig>): Promise<void>;
  deleteProvider(id: string): Promise<void>;
  testProvider(id: string): Promise<TestResult>;
  setDefault(id: string): Promise<void>;
}
```

---

## GIM Configuration

The **GIM (Generative Image Model) Settings Panel** configures text-to-image capabilities:

- Provider selection and API keys
- Model selection
- Image size, quality, and style presets
- Test generation
- Gallery of generated images

### Frontend Store: `gimStore`

Manages GIM provider configs, test results, and generated image gallery.

---

## Python Environment

The **Python Settings Panel** manages the Python runtime used for script execution:

### Features

- **Virtual environment** detection and creation
- **Package management** — install, uninstall, list packages
- **Python version** display
- **Path configuration** — which Python interpreter to use

### Frontend Store: `pythonStore`

```typescript
interface PythonState {
  pythonPath: string;
  version: string;
  packages: PackageInfo[];
  venvPath?: string;
  isVenvActive: boolean;
  
  fetchInfo(): Promise<void>;
  installPackage(name: string): Promise<void>;
  createVenv(path: string): Promise<void>;
}
```

---

## Execution Settings

The **Settings Panel** (gear icon in the toolbar) configures per-project execution:

| Setting | Description | Default |
|---------|-------------|---------|
| **LLM Model** | Model for inference execution | From default provider |
| **Max Cycles** | Maximum execution cycles | 100 |
| **DB Path** | Orchestrator database file | `orchestration.db` |
| **Base Directory** | Working directory for file operations | Project root |
| **Paradigm Directory** | Custom paradigm folder | `provision/paradigm` |

### Frontend Store: `configStore`

```typescript
interface ConfigState {
  llmModel: string;
  maxCycles: number;
  dbPath: string;
  baseDir: string;
  paradigmDir: string;
  availableModels: string[];
  
  setLlmModel(model: string): void;
  setMaxCycles(cycles: number): void;
  fetchConfig(): Promise<void>;
}
```

---

## Deployment & Remote Execution

The Canvas App can deploy projects to remote NormCode servers and monitor remote execution. This corresponds to the **Deploy** stage of the [NormCode lifecycle](../1_intro/ecosystem.md#the-lifecycle).

> For full details on the NormCode Server itself (installation, REST API, authentication, directory structure), see the **[NormCode Server Guide](normcode_server_guide.md)**. This section covers the Canvas-side deployment configuration.

### Deployment Panel

Access via the toolbar's deploy icon.

#### Server Management

Register remote NormCode servers:

```typescript
interface DeploymentServer {
  id: string;
  name: string;                // Display name
  url: string;                 // Server URL (http://host:port)
  description?: string;
  is_default: boolean;
}
```

#### Health Monitoring

Each server shows:
- Connection status (healthy / unhealthy / unreachable / timeout)
- Number of deployed plans
- Active and completed runs
- Available LLM models on the server

#### Deploy Workflow

1. **Add Server** — Register a remote NormCode server URL
2. **Check Health** — Verify the server is reachable
3. **Deploy** — Upload the current project to the server
4. **Run** — Start execution on the remote server
5. **Monitor** — Watch execution progress and results

#### Remote Run Monitoring

```typescript
interface RemoteRunStatus {
  run_id: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: { completed: number; total: number; cycle: number };
  started_at?: string;
  completed_at?: string;
}

interface RemoteRunResult {
  run_id: string;
  status: string;
  outputs: Record<string, any>;
  logs: string[];
  duration_ms: number;
}
```

### Frontend Store: `deploymentStore`

Manages server list, health status, deployed plans, and remote runs.

### Backend Services

| Service | Purpose |
|---------|---------|
| `DeploymentService` | Server registration, health checks |
| `RemoteRunService` | Remote run lifecycle |
| `RemoteExecutionController` | Proxy for remote execution control |
| `RemoteProxyExecutor` | Execute inferences on remote servers |

---

## Project Export & Import

The **Portable Projects** system packages projects for sharing or backup.

### Export

Export a project as a self-contained archive:

```typescript
interface ExportOptions {
  scope?: 'full' | 'project' | 'selected';    // What to include
  selected_run_ids?: string[];                  // Specific runs to export
  include_database?: boolean;                   // Include orchestration.db
  include_logs?: boolean;                       // Include log files
  include_provisions?: boolean;                 // Include paradigms, prompts
  include_agent_config?: boolean;               // Include .agent.json
  create_zip?: boolean;                         // Create .zip archive
}
```

**Export scopes**:
| Scope | Content |
|-------|---------|
| `full` | Everything — repos, provisions, database, logs, configs |
| `project` | Project config, repos, provisions (no database/logs) |
| `selected` | Only selected runs and their checkpoints |

### Import

Import a previously exported archive:

```typescript
interface ImportOptions {
  target_directory: string;          // Where to extract
  new_project_name?: string;         // Rename on import
  overwrite_existing?: boolean;      // Overwrite if project exists
  import_database?: boolean;         // Import orchestration.db
  import_runs?: boolean;             // Import execution runs
  merge_with_existing?: boolean;     // Merge into existing project
}
```

### Quick Export/Import

Simplified one-click operations:
- **Quick Export**: Full project export with defaults
- **Quick Import**: Import an archive to a target directory

### Portable Manifest

Every export includes a manifest describing its contents:

```typescript
interface PortableManifest {
  format_version: string;
  exported_at: string;
  project_name: string;
  files: string[];
  has_database: boolean;
  runs_count: number;
  provisions_included: Record<string, string>;
}
```

### Frontend Store: `portableStore`

Manages export/import operations, archive listing, and preview.

### Access

Export/Import is available from:
1. The **Export Panel** in the Editor view
2. The Settings Panel toolbar
3. REST API endpoints at `/api/portable/*`

---

## Additional Stores

Beyond the 6 stores documented in the API Reference, the frontend includes:

| Store | Purpose |
|-------|---------|
| `canvasCommandStore` | Canvas commands received from backend WebSocket |
| `chatStore` | Chat panel state, messages, controller lifecycle |
| `deploymentStore` | Remote server management and run monitoring |
| `gimStore` | GIM provider configs and image gallery |
| `layoutStore` | Zoom level, panel sizes, layout preferences |
| `llmStore` | LLM provider management |
| `notificationStore` | Toast notification queue |
| `panelStore` | Panel open/close states |
| `portableStore` | Export/import operations |
| `pythonStore` | Python environment state |
| `workerStore` | Worker status and management |

---

## See Also

- **[NormCode Server Guide](normcode_server_guide.md)**: Full Server documentation (API, auth, installation)
- **[Ecosystem Overview](../1_intro/ecosystem.md)**: Where deployment fits in the lifecycle
- **[Canvas App User Guide](canvas_app_user_guide.md)**: General usage
- **[API Reference](canvas_app_api_reference.md)**: REST endpoints and WebSocket events
- **[Canvas App Overview](canvas_app_overview.md)**: Architecture
- **[Debugging Guide](canvas_app_debugging_guide.md)**: Inspection and debugging tools

---

**Last Updated**: March 2026
