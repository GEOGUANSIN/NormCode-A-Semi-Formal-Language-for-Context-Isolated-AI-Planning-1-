# 5. Demo Scenario B: Debug and Fork

This scenario uses the **NormCode Code Assistant** — a production plan that
handles software engineering tasks through a seven-stage pipeline: Receive →
Triage → Explore → Plan → Implement → Verify → Report. The plan contains
approximately 40 inferences. We demonstrate debugging at the Explore stage, where
the plan queries the codebase before generating an implementation plan.

The scenario is designed to show what happens when a step receives incomplete or
unexpected inputs — and how NormCode's structural data isolation makes the failure
immediately visible and correctable without restarting the run.

## Step 1 — Set a Breakpoint

In Canvas, the operator right-clicks the node at flow index `1.3.2` — the
**"synthesize exploration findings"** inference, which aggregates file inspection
results into a structured summary that the Plan stage will use. A breakpoint badge
appears on the node. The operator clicks Run.

Execution proceeds normally: Receive completes (green), Triage completes (green),
the parallel Explore file-reading nodes complete (green). Execution pauses at
`1.3.2`. The node turns blue and holds. **No LLM has been called yet for the Plan
stage — the pause is before this inference runs.**

## Step 2 — Inspect the Tensor

The operator clicks the completed upstream node `1.3.1` — the output of the
parallel file exploration. The Tensor Inspector opens in the right panel:

```
Axis: [file]   Shape: (7,)

  [0]  %{file_location}a1c(src/orchestrator.py)
  [1]  %{file_location}b2d(src/blackboard.py)
  [2]  %{file_location}c3e(src/agent_sequences.py)
  [3]  %{file_location}d4f(src/reference_system.py)
  [4]  %{file_location}e5g(src/paradigms.py)
  [5]  %{file_location}f6h(src/compiler/formalization.py)
  [6]  %{file_location}g7i(src/compiler/activation.py)
```

These are **perceptual signs** — lightweight pointers that identify files without
loading their full content. The Explore stage found seven relevant files. The
operator notices immediately: `src/compiler/derivation.py` is missing. The task
requires understanding the full compilation pipeline, but the Explore stage's
search pattern did not match the derivation module.

This is the value of bounded inputs. Because `1.3.2` can only see what is
explicitly in `1.3.1`, the operator knows with certainty what the synthesis step
will work from — not approximately, not inferred from logs, but exactly. There is
no accumulated context from prior tasks, no implicit state carried forward from
Triage.

> **[FIGURE 3 HERE — Breakpoint at 1.3.2 (blue, paused), Tensor Inspector open
> showing the [file] axis with 7 entries, value override input visible]**

## Step 3 — Override the Value

The operator clicks **Override** in the right panel on node `1.3.1`. An edit
field appears populated with the current tensor data. They append a new entry:

```
  [7]  %{file_location}h8j(src/compiler/derivation.py)
```

The tensor now has eight entries. The operator clicks **Resume**.

The orchestrator re-runs `1.3.2` with the updated tensor — and only `1.3.2`
and its downstream dependents. All upstream nodes (the seven completed file
reads, the Triage output, the Receive stage) remain cached. No work is repeated
unnecessarily. The Plan, Implement, Verify, and Report stages proceed with the
corrected context.

## Step 4 — Fork for Comparison

After the corrected run completes, the operator clicks **Fork** on the checkpoint
at `1.3.1` — the state just before the synthesis node ran. A new run branches
from this checkpoint, initialized with the *original* tensor (seven files, no
derivation module). Both runs are now tracked independently in the checkpoint
panel.

The operator can compare the two runs' outputs at the Report stage — seeing
concretely how the missing file affected the implementation plan quality. This is
**experimental branching without destroying the corrected run**: a git-like
workflow for agent execution, enabled directly by the SQLite-backed checkpoint
system.

## What This Scenario Demonstrates

| Claim | Evidence in this scenario |
|-------|--------------------------|
| Input auditability | Tensor Inspector shows exactly what `1.3.2` will receive — bounded, named, inspectable before the step runs |
| Failures are immediately localizable | The missing file is visible in the tensor at pause time; no log archaeology required |
| Data isolation as a debugging tool | Because `1.3.2` sees only `1.3.1`'s output, the failure boundary is structurally guaranteed |
| Modification without restart | Override + selective re-run: only downstream inferences re-execute; upstream cache is preserved |
| Fork as experimental branching | Two runs from the same checkpoint, tracked independently; compare outputs without losing work |
| Deterministic syntactic steps never fail | All gray nodes (file path grouping, timing conditions) completed instantly and correctly; the failure was in scope definition, not data routing |

## Connection to Auditability in Regulated Domains

For high-stakes applications — legal document analysis, medical reasoning,
financial compliance — the question "what did step N actually see?" is not
optional. It is the prerequisite for any meaningful audit. In this scenario, that
question is answered in two clicks: set a breakpoint, open the tensor inspector.
No log parsing, no prompt reconstruction, no reverse-engineering of hidden state.
The answer is structurally available because the language enforced it.
