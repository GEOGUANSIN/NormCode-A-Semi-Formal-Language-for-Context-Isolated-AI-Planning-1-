# Canvas Assistant

**A NormCode plan that runs inside the Canvas App and controls it via natural language chat.**

**Location**: `canvas_app/built_in_projects/canvas_assistant/`
**Status**: Production (v2.0)
**Category**: Interactive chat controller

---

## Overview

The Canvas Assistant is a chat-driven controller for the NormCode Canvas. Users type commands in natural language; the plan classifies them, executes canvas operations, and responds — all as a visible, inspectable NormCode plan running on the graph.

### Example Commands

| Command | Classification | Execution |
|---------|---------------|-----------|
| "Navigate to node 1.2.3" | Navigation | `me.hands.navigate(flow_index="1.2.3")` |
| "Run the plan" | Execution control | `me.mind.run()` |
| "What is the status of step 2?" | Query | `me.vision.get_node_status()` |
| "Set a breakpoint on 1.5" | Execution control | `me.mind.set_breakpoint()` |
| "bye" | Session end | Loop terminates |

---

## The Plan (`.ncds`)

This is the full draft plan that defines the Canvas Assistant's behavior:

```
/: Canvas Assistant - Chat-Driven Command Loop
/: Derived from _.instruction.md (v2.0 with Canvas Integration)

:<: {session result}
    <= return session completion status
    /: Final output when session ends
    
    /: ══════════════════════════════════════════════════════════════════
    /: GROUND CONCEPTS (exist before loop starts)
    /: ══════════════════════════════════════════════════════════════════
    
    <- {canvas command schema}
        <= load the command schema from file
        <- {command schema file path}
            /: Ground:provisions/schemas/canvas_commands.json
    
    <- [on-going messages]
        /: Invariant: accumulates across iterations
        /: start_without_value: true (first iteration has no base)
        <= initiate an empty list.


    /: ══════════════════════════════════════════════════════════════════
    /: MAIN LOOP - Iterate over messages (self-seeding)
    /: ══════════════════════════════════════════════════════════════════
    
    <- [all canvas statuses]
        <= for each message in conversation
            <= return canvas status for this iteration
            
            /: STEP 1: Wait for user input (BLOCKING)
            <- {current message}
                <= read user message from chat
                /: Uses me.vision.get_chat() - blocks until message arrives
            
            /: STEP 2: Emit "thinking" status
            <- {thinking status emitted}
                <= emit status: thinking
                <- {current message}
            
            /: STEP 3: Summarize conversation context
            <- {messages snapshot}
                <= collect all on-going messages
                <- [on-going messages]
            
            <- {context summary}
                <= summarize on-going messages for context
                <- {messages snapshot}
            
            <- {context notified}
                <= notify chat with context summary
                <- {context summary}
            
            /: STEP 4: Classify message as canvas command
            <- {parsed command}
                <= classify user message as canvas command with context
                <- {current message}
                <- {canvas command schema}
                <- {context summary}
                
            /: STEP 5: Emit "executing" status
            <- {executing status emitted}
                <= emit status: executing
                <- {parsed command}
            
            /: STEP 6: Execute the parsed command on canvas
            <- {command status}
                <= execute parsed command on canvas
                <- {parsed command}
            
            /: STEP 7: Emit "generating" status
            <- {generating status emitted}
                <= emit status: generating
                <- {command status}
            
            /: STEP 8: Generate helpful response
            <- {response}
                <= generate response based on command result with context
                <- {current message}
                <- {command status}
                <- {context summary}
            
            /: STEP 9: Send response to user
            <- {response sent}
                <= send response to chat
                <- {response}
            
            /: STEP 10: Bundle iteration results
            <- {canvas status}
                <= bundle message, context, command status, and response
                <- {current message}
                <- {context summary}
                <- {command status}
                <- {response sent}
        
            /: LOOP CONTROL: Judge termination and conditional append
            <- <session should end>
                <= judge if user wants to end the session
                <- {current message}
                <- {messages snapshot}
            
            <- [on-going messages]
                <= append current message if session should NOT end
                    <= if session should NOT end
                    /: Timing gate: @:! (<session should end>)
                    <* <session should end>
                <- {current message}
                <- [on-going messages]

        /: LOOP BASE: Message history (self-seeding, starts empty)
        <- [on-going messages] 

        <* {message}
            /: Loop context: current message from [on-going messages]
```

---

## How It Works

### Self-Seeding Loop

The plan uses a **self-seeding loop** — the loop base (`[on-going messages]`) grows each iteration because the plan appends new messages back into it:

1. Loop starts with an empty `[on-going messages]`
2. Each iteration waits for a user message, processes it, and appends it back
3. The termination judge (`<session should end>`) controls whether the append happens
4. When the user says "bye" or "quit", the append is skipped → list is complete → plan finishes

### Per-Iteration Pipeline

Each chat cycle executes 10 steps:

```
Wait ──▶ Think ──▶ Summarize ──▶ Classify ──▶ Execute ──▶ Generate ──▶ Send ──▶ Judge
  │                                                                               │
  │                                                                               │
  └── blocks until ◀──────────────── loop back if NOT should end ◀────────────────┘
      message arrives
```

### Context Summarization

Rather than passing the entire message history to each LLM call (which would grow unboundedly), the plan summarizes the conversation each cycle. This keeps downstream LLM calls focused and prevents context pollution — NormCode's core design principle in action.

---

## Inference-Level Breakdown

### Ground Concepts

| Concept | Type | Source |
|---------|------|--------|
| `{canvas command schema}` | Value | Loaded from `provisions/schemas/canvas_commands.json` |
| `[on-going messages]` | Value (list) | Initialized empty, accumulates across iterations |

### Paradigm Mapping

| Inference | Paradigm | Faculty |
|-----------|----------|---------|
| Read file | `h_LiteralPath-c_ReadFile-o_Literal` | `file_system` |
| Wait for input | `c_CanvasIntegrationGetChat-o_Literal` | `canvas_integration` |
| Emit status | `h_Literal-c_CanvasIntegrationNotify-o_LiteralStatus` | `canvas_integration` |
| Summarize / Classify / Generate | `v_PromptLocation-h_Literal-c_GenerateThinkJson-o_Literal` | `llm` |
| Judge termination | `v_PromptLocation-h_Literal-c_GenerateThinkJson-o_Boolean` | `llm` |
| Execute command | `h_Literal-c_CanvasIntegrationExecute-o_LiteralStatus` | `canvas_integration` |
| Send response | `h_Literal-c_CanvasIntegrationSay-o_LiteralStatus` | `canvas_integration` |

---

## Key Design Patterns

| Pattern | How It's Used |
|---------|--------------|
| **Self-seeding loop** | `[on-going messages]` grows via conditional append; drives loop continuation |
| **Context summarization** | LLM compresses history each cycle to prevent unbounded context growth |
| **Status notifications** | "thinking", "executing", "generating" emitted via `me.hands.notify` |
| **Termination judge** | LLM decides if user wants to end session; controls loop via timing gate |
| **Command schema** | JSON schema passed to classifier so LLM knows all valid canvas commands |

---

## Files

| File | Purpose |
|------|---------|
| `_.ncds` | Draft plan (shown above) |
| `_.pf.ncd` | Formal compiled plan with flow indices and paradigms |
| `_.pf.nci.json` | Inference index |
| `repos/concept_repo.json` | Executable concept repository |
| `repos/inference_repo.json` | Executable inference repository |
| `provisions/schemas/canvas_commands.json` | Command classification schema |
| `provisions/prompts/classify_command.md` | Classifier prompt |
| `provisions/prompts/generate_response.md` | Response generation prompt |
| `provisions/prompts/summarize_context.md` | Context summarization prompt |
| `provisions/prompts/judge_terminate.md` | Termination judge prompt |

---

## See Also

- **[README](README.md)** — Overview of all built-in plans
- **[Canvas Integration Guide](../5_tools/canvas_integration_guide.md)** — The `me`/`you`/`it` faculty system
- **[Chat System Guide](../5_tools/canvas_app_chat_system.md)** — How chat controllers work

---

**Last Updated**: March 2026
