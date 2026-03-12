# Canvas Integration Tool Guide

**How NormCode plans interact with the Canvas App through the three-perspective architecture.**

---

## Introduction

The Canvas Integration Tool is the unified interface that allows NormCode plans (like the Canvas Assistant and Code Assistant) to interact with the Canvas App. Instead of giving plans direct access to raw APIs, it provides a structured, perspective-based interface that mirrors how a person would interact with a UI.

This guide covers:
- The three-perspective architecture (`me`, `you`, `it`)
- How faculties (vision, hands, mind) work
- How facades provide private tool access
- How to build NormCode plans that use the Canvas Integration Tool

---

## The Three Perspectives

The Canvas Integration Tool organizes all interactions into three perspectives:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CanvasIntegrationTool                           │
│                                                                     │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────┐      │
│   │  me (1st)      │  │  you (2nd)     │  │  it (3rd)      │      │
│   │  Shared Stage  │  │  Private Work  │  │  Observation   │      │
│   │  User sees     │  │  User doesn't  │  │  System events │      │
│   │                │  │  see           │  │                │      │
│   │  .vision       │  │  .files        │  │  .events       │      │
│   │  .hands        │  │  .code         │  │  .activity     │      │
│   │  .mind         │  │  .blackboard   │  │                │      │
│   │  .say()        │  │  .llm          │  │                │      │
│   │  .look()       │  │  .parser       │  │                │      │
│   └────────────────┘  │  .prompt       │  └────────────────┘      │
│                       │  .graph        │                           │
│                       │  .database     │                           │
│                       │  .paradigm     │                           │
│                       │  .model        │                           │
│                       │  .compose      │                           │
│                       │  .perceive     │                           │
│                       │  .format       │                           │
│                       │  .input        │                           │
│                       │  .system       │                           │
│                       │  .history      │                           │
│                       └────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘
```

| Perspective | Pronoun | Visibility | Purpose | Analogy |
|-------------|---------|------------|---------|---------|
| **First Person** | `me` | User sees effects | Act on the shared stage (canvas, chat) | On stage |
| **Second Person** | `you` | User sees nothing | Direct backend/tool access | Backstage |
| **Third Person** | `it` | Observation only | Watch system events and activity | Audience |

---

## First Person: `me` — The Shared Stage

When a plan uses `me`, it acts as the user. Effects are visible in the UI.

### Direct Actions

```python
me.say("Hello! I found the issue.")      # Shows in chat panel
me.look()                                  # Get full UI snapshot
```

### The Three Faculties

The first person perspective is divided into three faculties — modeled after a person's capabilities:

#### Vision — What I Can See

```python
snapshot = me.vision.get_canvas()           # Full canvas state
node = me.vision.get_node("1.2.1")          # Specific node details
status = me.vision.get_execution_status()   # Execution state
selected = me.vision.get_selected()         # Currently selected node
panels = me.vision.get_panels()             # Open panels
```

Vision is read-only. It returns structured data about what's currently visible on the canvas.

#### Hands — What I Can Do

```python
me.hands.select_node("1.3")                # Select a node
me.hands.zoom_to_fit()                      # Fit graph to viewport
me.hands.open_panel("detail")              # Open a panel
me.hands.collapse_node("2.0")             # Collapse a subtree
me.hands.execute_command(cmd)              # Execute a classified command
```

Hands perform actions that change the UI state. Every action emits WebSocket events that update the frontend.

#### Mind — What I Can Control

```python
me.mind.run()                               # Start execution
me.mind.pause()                             # Pause execution
me.mind.step()                              # Execute one inference
me.mind.set_breakpoint("1.4.2")            # Set a breakpoint
me.mind.get_execution_state()              # Query execution engine
```

Mind controls the NormCode execution engine. It's the interface between the plan and the orchestrator.

---

## Second Person: `you` — The Private Workspace

When a plan uses `you`, it accesses tools directly without affecting the UI. The user sees nothing.

### Facades

Each facade wraps an existing Canvas tool, providing shortcut access:

| Facade | Tool Wrapped | Key Methods |
|--------|-------------|-------------|
| `you.files` | CanvasFileSystemTool | `.read()`, `.write()`, `.list()`, `.exists()` |
| `you.code` | CanvasPythonInterpreterTool | `.run()` |
| `you.llm` | CanvasLLMTool | `.call()`, `.complete()` |
| `you.parser` | CanvasParserTool | `.parse()`, `.serialize()` |
| `you.prompt` | CanvasPromptTool | `.load()`, `.render()` |
| `you.blackboard` | Direct state access | `.get()`, `.set()` — read/write concept values |
| `you.graph` | GraphService | `.get_node()`, `.get_edges()`, `.get_subgraph()` |
| `you.database` | OrchestratorDB | `.query()`, `.get_runs()` |
| `you.paradigm` | CanvasParadigmTool | `.load()`, `.list()` |
| `you.model` | CanvasModelRunnerTool | `.run()` |
| `you.compose` | CanvasCompositionTool | `.compose()` |
| `you.perceive` | CanvasPerceptionRouter | `.route()` |
| `you.format` | CanvasFormatterTool | `.format()`, `.parse()` |
| `you.input` | CanvasUserInputTool | `.request()` |
| `you.system` | System utilities | `.get_config()`, `.get_time()` |
| `you.history` | Execution history | `.get_runs()`, `.get_trace()` |

### When to Use `you` vs `me`

```python
# Bad: tedious through UI
me.hands.open_panel("editor")
me.hands.navigate_to("config.json")
# ... many more steps to read a file

# Good: direct access
content = you.files.read("config.json")

# Then display via me if needed
me.say(f"Config loaded: {content[:100]}...")
```

**Rule of thumb**: Use `you` for data retrieval and computation. Use `me` for user-visible communication and actions.

---

## Third Person: `it` — System Observation

The third person perspective observes what's happening in the system without interfering.

```python
events = it.events.recent(limit=50)        # Recent system events
stream = it.events.stream(filter={...})    # Live event stream
it.activity.get_current()                  # What's happening now
```

| Second Person (`you`) | Third Person (`it`) |
|----------------------|---------------------|
| Query **data/state** (what IS) | Observe **activity/behavior** (what's HAPPENING) |
| Static queries | Dynamic observation |
| Logs, workers, traces | Events, timelines, activity |

---

## Architecture: How It Works

### Injection Pipeline

```
canvas_integration/injection.py
    │
    ├── create_canvas_integration(controller, emit_callback)
    │       │
    │       ├── FirstPersonPerspective(controller, emit)
    │       │     ├── Vision(controller)
    │       │     ├── Hands(controller, emit)
    │       │     └── Mind(controller)
    │       │
    │       ├── SecondPersonPerspective(body, controller)
    │       │     ├── FilesFacade(body.file_system)
    │       │     ├── CodeFacade(body.python_interpreter)
    │       │     ├── LLMFacade(body.llm)
    │       │     ├── ... (16 facades total)
    │       │     └── HistoryFacade(controller)
    │       │
    │       └── ThirdPersonPerspective(controller)
    │             ├── EventStore
    │             └── ActivityMonitor
    │
    └── inject_canvas_integration(body, controller, emit)
            │
            └── body.canvas_integration = tool
```

### File Organization

```
canvas_app/backend/canvas_integration/
├── __init__.py              # Re-exports
├── tool.py                  # CanvasIntegrationTool (unified entry point)
├── types.py                 # ActionResult, UserViewSnapshot, etc.
├── event_store.py           # Event storage for Third Person
├── injection.py             # Creation and injection helpers
├── perspectives/
│   ├── first_person.py      # FirstPersonPerspective
│   ├── second_person.py     # SecondPersonPerspective
│   └── third_person.py      # ThirdPersonPerspective
├── faculties/
│   ├── vision.py            # Vision faculty (read canvas state)
│   ├── hands.py             # Hands faculty (perform UI actions)
│   └── mind.py              # Mind faculty (execution control)
└── facades/
    ├── files.py             # FilesFacade
    ├── code.py              # CodeFacade
    ├── parser.py            # ParserFacade
    ├── blackboard.py        # BlackboardFacade
    ├── graph.py             # GraphFacade
    ├── database.py          # DatabaseFacade
    ├── llm.py               # LLMFacade
    ├── prompt.py            # PromptFacade
    ├── paradigm.py          # ParadigmFacade
    ├── model.py             # ModelFacade
    ├── compose.py           # ComposeFacade
    ├── perceive.py          # PerceiveFacade
    ├── format.py            # FormatFacade
    ├── input.py             # InputFacade
    ├── system.py            # SystemFacade
    └── history.py           # HistoryFacade
```

---

## ActionResult: Structured Responses

All faculty actions return an `ActionResult`:

```python
@dataclass
class ActionResult:
    success: bool
    data: Any = None
    message: str = ""
    error: str = ""

    @classmethod
    def ok(cls, data=None, message="") -> 'ActionResult': ...

    @classmethod
    def fail(cls, error="", data=None) -> 'ActionResult': ...
```

Plans can check `result.success` to handle errors gracefully:

```python
result = me.hands.select_node("1.5")
if not result.success:
    me.say(f"Couldn't select node: {result.error}")
```

---

## Building a Canvas-Driven Assistant

To create a new NormCode plan that uses the Canvas Integration Tool:

### 1. Project Setup

```
my_assistant/
├── my_assistant.normcode-canvas.json    # Project config
├── repos/
│   ├── concept_repo.json                # Compiled concepts
│   └── inference_repo.json              # Compiled inferences
├── provisions/
│   ├── paradigms/                       # Custom paradigms
│   ├── prompts/                         # LLM prompt templates
│   └── schemas/                         # Command schemas
└── my_assistant.agent.json              # Agent config
```

### 2. Paradigm Design

Create paradigms that access the integration tool:

```python
# In a paradigm's working interpretation:
snapshot = me.vision.get_canvas()
user_msg = me.hands.get_last_message()

# Process with LLM
response = you.llm.call(prompt)

# Respond
me.say(response)
```

### 3. Command Dispatch Pattern

The Canvas Assistant uses a classify-then-dispatch pattern:

```
User message → Classify (LLM) → Command type → Dispatch to faculty
                                    │
                                    ├── navigation  → me.hands.*
                                    ├── query       → me.vision.*
                                    ├── execution   → me.mind.*
                                    ├── canvas_mod  → me.hands.*
                                    └── general     → you.llm.* → me.say()
```

### 4. Registration

Place the project in `canvas_app/built_in_projects/` for automatic discovery, or open it as a regular project from any directory.

---

## See Also

- **[Canvas App Overview](canvas_app_overview.md)**: System architecture
- **[Chat System Guide](canvas_app_chat_system.md)**: Chat controller lifecycle
- **[API Reference](canvas_app_api_reference.md)**: WebSocket events and stores
- **Internal Design Docs**: `canvas_app/backend/canvas_integration/docs/`

---

**Last Updated**: March 2026
