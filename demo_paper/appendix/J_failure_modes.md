# Appendix J — Failure Mode Analysis

This appendix documents the failure taxonomy for NormCode plans running in
the Canvas orchestrator. For each failure type, it identifies where the failure
surfaces, how Canvas surfaces it, and what the recovery path is.

The organizing question behind this appendix is: "What happens when something
goes wrong?" — the implicit challenge a skeptical reviewer or practitioner
would raise. The answer for NormCode is structured: failures are categorized,
bounded, and surfaced at the most useful point (earliest possible, most specific
location).

---

## J.1 Failure Taxonomy

### J.1.1 Compile-Time Failures

These failures are caught before any execution. No LLM is called; no cost is
incurred.

| Failure | When detected | What the compiler reports | Fix |
|---------|--------------|--------------------------|-----|
| **Undefined concept reference** | Phase 2 | "Concept `X` at flow index `i.j` is not declared in scope" | Add the missing `<-` declaration in the correct scope |
| **Circular dependency** | Phase 2 | "Dependency cycle detected: `A → B → C → A`" | Restructure the plan to break the cycle |
| **Ungrounded tool reference** | Phase 3 | "Action `:: X` at `i.j` has no matching tool in the tool registry" | Register the tool in the agent configuration |
| **Missing paradigm match** | Phase 3 | "No paradigm found for action `X` at `i.j` — action description not recognized" | Rephrase the action, or add a matching paradigm to the paradigm directory |
| **Tensor axis mismatch** | Phase 3 | "Concept `X` declares axis `[file]` but its producer yields axis `[document]`" | Correct the axis declaration in the `.ncds` or the paradigm configuration |

**Key property:** Compile-time failures are precise. The compiler reports a
specific flow index or concept name. There is no ambiguity about where the
problem is — the report is a direct consequence of the scope and dependency
rules, not a heuristic diagnosis.

### J.1.2 Runtime Semantic Failures

These failures occur during execution when a semantic (LLM) node produces
an unexpected result.

| Failure | Where surfaces | Canvas behavior | Recovery |
|---------|---------------|----------------|---------|
| **Schema mismatch** | At the consumer of a semantic output | Red node at the consumer's flow index; diff of expected vs. actual tensor shape shown in right panel | Override the producer's output with correctly-shaped data; resume |
| **LLM refusal** | At the semantic node itself | Red node; refusal message shown in tool call monitor | Modify the action description in `.ncds`, recompile; or override the node's output manually |
| **Hallucinated concept reference** | At a downstream consumer | Red node; "perceptual sign `X` cannot be resolved" | Override the upstream node's output with valid signs; resume |
| **Empty output** | At the consumer | Red node; "required input `X` at `i.j` is empty or null" | Override the producer's output with a valid value; resume |
| **Quality failure (soft)** | Not automatically detected | Tensor inspector shows output; no red node | Set a breakpoint at a downstream judgement node; inspect and branch |

**Key property:** Schema mismatches and null outputs surface at the consumer
of the problematic output, not at the producer. This is by design: the producer
may have run successfully from its perspective; the failure is in the mismatch
between what was produced and what was expected. The consumer's flow index is
the precise failure address.

### J.1.3 Runtime Tool Failures

These failures occur when a grounded action (`<= ::`) invokes a tool that
fails.

| Failure | Where surfaces | Canvas behavior | Recovery |
|---------|---------------|----------------|---------|
| **Tool unavailable** | At the grounded action's node | Red node; "tool `X` not found in registry" | Check agent configuration; re-register tool; resume from cached checkpoint |
| **File not found** | At a `file_system` read node | Red node; `FileNotFoundError` shown in tool call monitor | Correct the file path (via override on the upstream sign) or provide the file; resume |
| **API timeout / rate limit** | At an LLM call node | Red node; timeout or rate limit error shown | Wait for limit to clear; resume — upstream checkpoints are preserved |
| **Python interpreter error** | At a `python_interpreter` node | Red node; traceback shown in tool call monitor | Debug the script externally; override the node's output with corrected result; resume |
| **Network error** | At any node requiring network | Red node; connection error shown | Restore network; resume from cached checkpoint |

**Key property:** All tool failures produce a red node at the exact flow index
that failed. Because all upstream nodes are cached in SQLite, resuming after
a tool failure (once the tool issue is resolved) re-runs only from the failure
point — not from the beginning. In a 40-inference plan, a failure at inference
30 wastes 0 of the first 29 inferences' results.

### J.1.4 Infrastructure Failures

These failures occur outside the plan's logic — in the orchestrator or the
platform.

| Failure | Where surfaces | Canvas behavior | Recovery |
|---------|---------------|----------------|---------|
| **Orchestrator crash** | Canvas disconnects (WebSocket closed) | "Connection lost" banner; run status shows `interrupted` | Restart Canvas; the SQLite checkpoint store is intact; resume the run from the last completed checkpoint |
| **SQLite corruption** | On checkpoint read | Error shown; affected run marked `corrupted` | Restore from backup; or restart from the last valid checkpoint |
| **Out of memory** | Orchestrator process | Canvas shows `run_failed` with OS-level error | Reduce plan concurrency (fewer parallel inferences); increase system memory; retry |
| **Model endpoint changed** | At first LLM call | Red node; connection refused or 404 error | Update agent configuration with new endpoint; redeploy; resume |

**Key property:** The SQLite checkpoint store is persistent and local. An
orchestrator crash does not lose completed work. The run can be resumed from
the last stored checkpoint — even across a system restart.

### J.1.5 The Failure That Cannot Happen: Scope Contamination

Context pollution — the root failure mode described in §1 of the body — is
structurally impossible in a correctly compiled and running NormCode plan.

**Why it cannot happen:**
1. The compiler enforces scope at Phase 2. Any plan that compiles has all
   concept references within scope.
2. The orchestrator constructs each inference's input from stored tensor
   checkpoints for the declared input flow indices only. It does not access
   any other checkpoint.
3. There is no "conversation history" object in the NormCode runtime. Each
   inference call is constructed fresh from declared inputs.

This is not a claim that NormCode plans are always correct — they may produce
wrong outputs for semantic reasons. It is a claim that one specific class of
failures (context pollution, cross-step state leakage, accumulated history
confusion) is structurally eliminated by the language and enforced by the
orchestrator. A plan that compiles cannot contaminate its steps' contexts.

---

## J.2 Failure Localization: A Comparison

The table below compares how the same failure type surfaces in NormCode vs.
a conventional multi-step agent framework.

**Failure scenario:** Step 5 of a 10-step workflow produces an output that
step 7 cannot parse (schema mismatch).

| System | How failure surfaces | Time to localize | Information available |
|--------|---------------------|-----------------|----------------------|
| **NormCode** | Red node at step 7; schema diff shown; step 7's input tensor inspectable at a breakpoint before retry | ~30 seconds | Exact tensor shape mismatch; step 7's declared inputs; step 5's stored output |
| **LangChain/LangGraph** | Exception in step 7's node function; stack trace in logs | ~5–30 minutes | Stack trace; full prompt string for step 7 (mixed with all prior history); no structured view of step 5's output as typed data |
| **AutoGen** | Agent 7 sends an error message; conversation continues (hallucination risk) | Variable; may not be detected | Full conversation history; no step boundary; no clean failure address |
| **No-code builder (LangFlow)** | Run status shows failed; error in the run log | ~10–60 minutes | Raw log entry; visual node highlighted; no structured input inspection |

The key column is "Time to localize." In NormCode, the red node is the failure
address. The tensor inspector at the paused consumer shows exactly what it
received. The schema diff shows exactly what it expected. There is no "log
archaeology."

---

## J.3 Recovery Patterns

**Override and resume (most common):**
Used for schema mismatches, empty outputs, and soft quality failures where
the operator can supply or correct the problematic value. The override replaces
the stored tensor; the selective re-run propagates the correction forward.
Upstream work is preserved.

**Recompile and restart (for structural errors):**
Used when the failure reveals a plan design issue — a missing input, an
incorrect action description, or a wrong paradigm assignment. The designer
edits the `.ncds`, recompiles, and the operator starts a new run. Note that
in this case, checkpoints from the previous run cannot be reused (the new
plan has different flow indices). This is the most expensive recovery path.

**Agent reconfiguration and resume:**
Used for tool failures and model endpoint changes. The operator updates the
agent configuration in Canvas (no plan edit needed), then resumes the run.
The orchestrator picks up the updated configuration for the remaining
inferences.

**Fork and compare:**
Used for quality failures where the operator wants to test a corrected input
against the original. The operator forks at the failure-adjacent checkpoint,
runs the corrected version, and compares the two runs' outputs at the report
node. The original run is preserved as a baseline.

---

## J.4 What This Means for Production Deployment

For a plan running as an end-user service (via NormCode Server + Client),
the operator's concern shifts from interactive debugging to automated recovery.
Production deployment implications:

| Concern | NormCode approach |
|---------|-----------------|
| Transient failures (rate limits, network) | Orchestrator retries with configurable backoff; checkpoints preserved |
| Systematic failures (bad model output) | Server can be configured to emit `run_failed` to a monitoring endpoint; operator inspects via Canvas on the stored run |
| Audit on demand | Any completed or failed run's checkpoints are queryable from Canvas at any time — post-hoc inspection without re-running |
| SLA tracking | `events` table records per-inference latency; total run duration tracked in `runs` table; both queryable |
| Version rollback | Deploying a previous `.ncds` version (from Git) and recompiling restores the previous plan's behavior; no other configuration change needed |
