# Canvas App Chat System

**How the chat interface works, how controllers drive conversations, and how to build chat-driven NormCode plans.**

---

## Introduction

The Canvas App includes a chat panel that is driven by NormCode plans called **controllers**. Unlike a simple chatbot, the chat system is a full NormCode execution loop — the controller is a plan that reads user messages, processes them through inferences, and responds via the chat tool.

This means every chat interaction is a visible, inspectable, debuggable NormCode execution.

---

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                        CHAT PANEL (Frontend)                   │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Controller Selector                                     │ │
│  │  [Canvas Assistant v2.0 ▼]  [▶ Start] [⏸ Pause]        │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │  Message Feed                                             │ │
│  │  ┌─────────────────────────────────────┐                  │ │
│  │  │ 🤖 Controller connected. Ready.     │                  │ │
│  │  │ 👤 Show me node 1.2.1              │                  │ │
│  │  │ 🤖 Selected node 1.2.1 for you.    │                  │ │
│  │  └─────────────────────────────────────┘                  │ │
│  │  [Notification: thinking... / command classified: ...]    │ │
│  ├──────────────────────────────────────────────────────────┤ │
│  │  Input Bar                                                │ │
│  │  [Type a message...                          ] [Send]    │ │
│  └──────────────────────────────────────────────────────────┘ │
└───────────────┬───────────────────────────────────────────────┘
                │  WebSocket Events
                ▼
┌───────────────────────────────────────────────────────────────┐
│                        BACKEND                                 │
│                                                               │
│  ChatControllerService                                        │
│  ├── Controller Registry (available controllers)              │
│  ├── Message Buffer (user → controller message queue)         │
│  └── ExecutionController (runs the NormCode plan)             │
│                                                               │
│  Chat Router (/api/chat/*)                                    │
│  ├── GET  /controllers        → list available controllers    │
│  ├── POST /select             → select & start a controller   │
│  ├── POST /message            → send user message             │
│  ├── GET  /messages           → get message history           │
│  ├── POST /input/respond      → respond to input request      │
│  ├── POST /start              → start controller execution    │
│  ├── POST /pause              → pause controller              │
│  ├── POST /resume             → resume controller             │
│  └── POST /stop               → stop controller               │
└───────────────────────────────────────────────────────────────┘
```

---

## Core Concepts

### Controllers

A **controller** is a NormCode project that drives the chat. It's a regular NormCode plan with chat-specific paradigms that:

1. Read user messages via `ChatTool.read()`
2. Process them (classify, analyze, generate responses)
3. Write responses via `ChatTool.write()`
4. Optionally execute canvas commands via the Canvas Integration Tool

Controllers are discovered automatically from `canvas_app/built_in_projects/` and from any open project that includes chat paradigms.

### Controller Lifecycle

```
disconnected → connecting → connected → running ⇄ paused → disconnected
                                          │
                                          └──→ error
```

| State | Description |
|-------|-------------|
| `disconnected` | No controller selected |
| `connecting` | Loading controller project, initializing execution |
| `connected` | Controller ready, waiting for user input |
| `running` | Controller is actively processing (executing inferences) |
| `paused` | Controller paused mid-execution |
| `error` | Controller encountered an error |

### Message Types

| Role | Source | Description |
|------|--------|-------------|
| `user` | User typing | User's message |
| `assistant` | Controller via ChatTool | Controller's response |
| `system` | System events | Connection status, errors |
| `controller` | Controller notifications | Status updates, phase indicators |
| `compiler` | Compilation events | Compilation output |

### Notifications vs Messages

**Messages** persist in the chat history. **Notifications** are ephemeral status indicators that show what the controller is doing:

| Category | Example | Purpose |
|----------|---------|---------|
| `message_received` | "Message received" | Confirms user message was buffered |
| `context_summary` | "Understanding context..." | Thinking phase indicator |
| `command_classified` | "Navigation: select_node (0.92)" | Shows classified command and confidence |
| `execution_result` | "Action succeeded" | Command execution outcome |
| `info` | "Loading project..." | General status |

---

## Frontend: Chat Store

The `chatStore` (Zustand) manages the entire chat state:

```typescript
interface ChatState {
  messages: ChatMessage[];
  
  // Controller state
  availableControllers: ControllerInfo[];
  controllerId: string | null;
  controllerName: string | null;
  controllerStatus: ControllerStatusType;
  currentFlowIndex: string | null;
  
  // Input state
  inputValue: string;
  isInputDisabled: boolean;
  isSending: boolean;
  pendingInputRequest: ChatInputRequest | null;
  
  // Notification (ephemeral)
  currentNotification: ChatNotification | null;
  
  // Controller lifecycle
  loadControllers(): Promise<void>;
  selectController(controllerId: string): Promise<void>;
  startController(): Promise<void>;
  pauseController(): Promise<void>;
  resumeController(): Promise<void>;
  stopController(): Promise<void>;
  
  // Message actions
  submitInput(value: string): Promise<void>;
  respondToInputRequest(response: string): Promise<void>;
  
  // Project integration
  openControllerProject(): Promise<void>;
}
```

### WebSocket Events

The chat system listens for these events:

| Event | Direction | Description |
|-------|-----------|-------------|
| `chat:message` | Server → Client | New message from controller |
| `chat:notification` | Server → Client | Ephemeral status notification |
| `chat:input_request` | Server → Client | Controller requesting user input |
| `chat:status` | Server → Client | Controller status change |
| `chat:controller_update` | Server → Client | Controller info update (name, status, flow_index) |
| `chat:buffer_status` | Server → Client | Message buffer state |

---

## Frontend: Chat Panel Component

The `ChatPanel.tsx` component renders:

1. **Controller Selector** — Dropdown of available controllers with start/pause/stop controls
2. **Message Feed** — Scrollable list of messages with role-based styling
3. **Code Blocks** — Syntax-highlighted code in messages (via `CodeBlockDisplay`)
4. **Notification Bar** — Current ephemeral notification with category-based styling
5. **Input Bar** — Text input with send button, disabled during controller processing
6. **Input Request Modal** — Appears when controller needs structured input (text, code, confirm, select)

---

## How Controllers Process Messages

### The Chat Loop

A typical controller follows this cycle:

```
                    ┌──────────────────────┐
                    │                      │
                    ▼                      │
        ┌───────────────────┐              │
        │  Wait for message │              │
        │  (ChatTool.read)  │              │
        └────────┬──────────┘              │
                 │                         │
                 ▼                         │
        ┌───────────────────┐              │
        │  Process message  │              │
        │  (LLM classify)   │              │
        └────────┬──────────┘              │
                 │                         │
                 ▼                         │
        ┌───────────────────┐              │
        │  Execute command  │              │
        │  (Canvas action)  │              │
        └────────┬──────────┘              │
                 │                         │
                 ▼                         │
        ┌───────────────────┐              │
        │  Generate response│              │
        │  (ChatTool.write) │              │
        └────────┬──────────┘              │
                 │                         │
                 ▼                         │
        ┌───────────────────┐              │
        │  Judge: continue? │──── yes ─────┘
        │  (terminate check)│
        └────────┬──────────┘
                 │ no
                 ▼
            [End cycle]
```

### Message Flow

```
User types "select node 1.3"
    │
    ▼
Frontend: chatStore.submitInput("select node 1.3")
    │
    ▼
Backend: POST /api/chat/message → message buffered
    │
    ▼
Controller plan: ChatTool.read() → returns "select node 1.3"
    │
    ▼
Controller plan: LLM classifies → {type: "navigation", action: "select_node", params: {node: "1.3"}}
    │
    ▼
Controller plan: me.hands.select_node("1.3") → ActionResult.ok()
    │
    ▼
Controller plan: ChatTool.write("Selected node 1.3 for you.") → appears in chat
    │
    ▼
Frontend: WebSocket event → message appears in feed
```

---

## Building a Chat Controller

### Required Paradigms

A chat controller needs paradigms for:

1. **Chat Read** — Read user input from the message buffer
2. **Chat Write** — Write response to the chat panel
3. **Processing** — LLM-based message classification and response generation

### Example Paradigm Set

```
provisions/paradigms/
├── c_ChatRead-o_Literal.json              # Read user message
├── h_Response-c_ChatWrite-o_Status.json   # Write response
├── h_UserMessage-c_Classify-o_Command.json # Classify message
└── h_Context-c_Generate-o_Response.json    # Generate response
```

### Connecting to Canvas Integration

For controllers that need to manipulate the canvas:

1. The controller project's agent config enables canvas integration
2. The Canvas Integration Tool is injected into the controller's Body
3. Paradigms access it via `me.vision`, `me.hands`, `me.mind` (first person) or `you.*` (second person facades)

### Controller Discovery

Controllers are discovered from two sources:

1. **Built-in projects** in `canvas_app/built_in_projects/` — automatically available
2. **Current project** — if it has chat paradigms, it appears as a selectable controller

---

## Built-in Controllers

### Canvas Assistant (v2.0)

The primary built-in controller. Located at `built_in_projects/canvas_assistant/`.

**Pipeline**: wait → summarize context → classify command → execute → generate response → judge terminate

**Capabilities**:
- Navigation commands (select node, zoom, fit, collapse)
- Execution control (run, pause, step)
- Canvas queries (what is selected, execution status)
- General conversation (explain concepts, help)

### Canvas Assistant v3.0 (Design)

A redesigned controller with tiered architecture. Located at `built_in_projects/canvas_assistant_v3/`.

**Tiered approach**:
- **Tier 0**: Pattern match (regex, no LLM, ~100ms)
- **Tier 1**: Quick path (1 LLM call, ~4s)
- **Tier 2**: Contextual (2 LLM calls, ~12s)
- **Tier 3**: Agentic (2+ LLM calls, act-observe loop)

---

## See Also

- **[Canvas Integration Guide](canvas_integration_guide.md)**: Perspectives, faculties, facades
- **[Canvas App User Guide](canvas_app_user_guide.md)**: Using the chat panel
- **[API Reference](canvas_app_api_reference.md)**: Chat REST endpoints and WebSocket events
- **[Canvas App Overview](canvas_app_overview.md)**: System architecture

---

**Last Updated**: March 2026
