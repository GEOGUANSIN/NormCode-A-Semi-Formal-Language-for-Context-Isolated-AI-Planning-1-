# Code Assistant

**A NormCode plan for autonomous software engineering — reading codebases, planning changes, editing files, and verifying results.**

**Location**: `canvas_app/built_in_projects/code_assistant/`
**Status**: Design complete, implementation in progress
**Category**: Interactive software engineering agent

---

## Overview

The Code Assistant is a structured software engineering workflow expressed as a NormCode plan. Given a task like "fix the bug in the auth module" or "add pagination to the user list," it systematically explores the codebase, plans changes, implements them with surgical edits, and verifies the results — all as visible, inspectable nodes on the canvas graph.

Unlike a black-box coding assistant, every step is a NormCode inference with declared inputs and outputs. You can inspect what the Explore step found, override the Plan step's approach, or re-run just the Verify step.

---

## Pipeline

```
Receive ──▶ Triage ──▶ Explore ──▶ Plan ──▶ Approve ──▶ Implement ──▶ Verify ──▶ Report
                         │                                   │              │
                         ├── grep, glob, file reads           ├── lint fix   ├── test/build
                         └── git status, git log              │   inner loop │   recovery
                                                              └──────────────┘
```

| Stage | What Happens | Tools | LLM? |
|-------|-------------|-------|------|
| **Receive** | Accept user request via chat | `canvas_integration` | No |
| **Triage** | Classify complexity (Tier 1-3) | — | Yes |
| **Explore** | Parallel codebase discovery | `search`, `shell`, `git` | No |
| **Plan** | Generate change plan | — | Yes |
| **Approve** | Show plan to user for confirmation | `canvas_integration` | No |
| **Implement** | Surgical edits with lint-fix loops | `editor`, `shell` | Yes |
| **Verify** | Parallel test/build/typecheck | `shell` | No |
| **Report** | Git diff summary, optional commit | `git` | Yes |

### Tiered Complexity

| Tier | Complexity | Example | Exploration Depth |
|------|-----------|---------|-------------------|
| **Tier 1** | Simple edits | "Rename function X to Y" | Minimal — grep for usages |
| **Tier 2** | Standard features | "Add pagination to the user list" | Moderate — understand component structure |
| **Tier 3** | Complex debugging | "Fix the race condition in the cache layer" | Deep — trace data flow, read logs |

---

## The Plan (Design)

The Code Assistant's `.ncds` is being finalized. The plan structure follows this hierarchy:

```
:<: {task result}
    <= report completion status with git diff summary

    /: GROUND CONCEPTS
    <- {user request}
        <= receive task from user via chat
    
    <- {project context}
        <= collect initial project state
        <- {git status}
            <= run git status
        <- {file tree}
            <= list project structure
    
    /: PHASE 1: Triage
    <- {task tier}
        <= classify task complexity (tier 1/2/3)
        <- {user request}
        <- {project context}
    
    /: PHASE 2: Explore
    <- {exploration results}
        <= explore codebase based on task and tier
        <- {user request}
        <- {task tier}
        <- {search results}
            <= search for relevant code patterns
            <- {user request}
        <- {file contents}
            <= read key files identified by search
            <- {search results}
        <- {git history}
            <= get relevant git log
            <- {user request}
    
    /: PHASE 3: Plan
    <- {change plan}
        <= generate detailed change plan
        <- {user request}
        <- {exploration results}
        <- {task tier}
    
    /: PHASE 4: Approve
    <- {user approval}
        <= present plan to user for approval
        <- {change plan}
    
    /: PHASE 5: Implement
    <- [edit results]
        <= for each change in plan
            <= apply edit and run lint check
            <- {edit result}
                <= apply surgical edit
                <- {current change}
            <- {lint result}
                <= run linter on edited file
                <- {edit result}
            /: Inner loop: fix lint errors if any
        <- {change plan}
        <* {current change}
    
    /: PHASE 6: Verify
    <- {verification}
        <= run tests, build, and typecheck in parallel
        <- [edit results]
    
    /: PHASE 7: Report
    <- {report}
        <= generate git diff summary and optionally commit
        <- {verification}
        <- [edit results]
```

---

## Key Design Principles

### Scoped LLM Calls

Each step receives only the inputs it needs:
- **Explore** gets the user request and project context — not chat history
- **Plan** gets exploration results — not raw file contents the search found
- **Implement** gets the approved plan — not the raw search results
- **Report** gets verification results — not the full exploration data

This is NormCode's data isolation applied to software engineering. The LLM at each step isn't drowning in irrelevant context.

### Lint-Fix Inner Loop

The Implement phase has an inner loop: after each edit, the linter runs. If lint errors are introduced, the LLM fixes them before moving to the next edit. This prevents error accumulation.

### Parallel Verification

The Verify phase runs tests, build, and typecheck simultaneously (parallel execution). If any fail, the plan enters a recovery loop.

---

## Faculties Used

| Faculty | Purpose | Key Methods |
|---------|---------|-------------|
| `shell` | Run commands, build, test, lint | `execute(cmd)`, `execute_background(cmd)` |
| `search` | Ripgrep search, glob patterns | `grep(pattern)`, `glob(pattern)`, `find_definitions(symbol)` |
| `git` | Version control operations | `status()`, `diff()`, `log()`, `add()`, `commit()` |
| `editor` | Surgical file editing | `str_replace(old, new)`, `insert_lines()`, `create_file()` |
| `memory` | Cross-session semantic memory | `store(text)`, `search(query)` |
| `llm` | Reasoning and code generation | Triage, planning, code generation, analysis |
| `canvas_integration` | User interaction | `me.vision.get_chat()`, `me.hands.say()` |

---

## See Also

- **[README](README.md)** — Overview of all built-in plans
- **[Canvas App User Guide](../5_tools/canvas_app_user_guide.md)** — Agent configuration and tool settings
- **[Code Assistant README](../../canvas_app/built_in_projects/code_assistant/README.md)** — Full design document

---

**Last Updated**: March 2026
