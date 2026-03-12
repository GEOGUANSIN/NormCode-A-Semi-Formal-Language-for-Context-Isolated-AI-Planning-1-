# Appendix C — Complete Audit Trace: PPT Agent Run

This appendix presents a complete execution trace of one PPT Agent run on the
topic "machine learning in healthcare." Every inference node is listed in
execution order, indexed by flow index, with its paradigm type, declared inputs,
LLM call count, approximate token cost, and a one-line output summary.

This is the audit trail a compliance officer, senior engineer, or regulator
would inspect after the run. The key property: no row requires log parsing,
prompt reconstruction, or inference from implicit state. Every entry is a
direct record of what the orchestrator declared, sent, and stored.

---

## C.1 Run Metadata

| Field | Value |
|-------|-------|
| Plan | `ppt_generation.ncds` |
| Compiled version | `concept_repo.json` + `inference_repo.json` |
| Input | `topic = "machine learning in healthcare"` |
| Run ID | `run_20240301_ppt_001` (example) |
| Total wall-clock time | ~92 seconds |
| Total LLM calls | 12 |
| Total tokens (approximate) | ~8,400 |
| Total syntactic steps | 19 |
| Total semantic steps | 12 |
| Failures | 0 |
| Scope violations detected | 0 |

---

## C.2 Full Execution Trace

**Key:** Gray rows = syntactic (no LLM). Purple rows = semantic (LLM call).
Numbers in "Inputs declared" are flow indices of the input concepts.

| Flow index | Step name | Paradigm | Type | Inputs declared | LLM calls | Tokens (est.) | Output summary |
|-----------|-----------|----------|------|-----------------|-----------|--------------|----------------|
| 1 | presentation | Grouping | Syntactic | 1.1, 1.3 | — | 0 | Collection assembled from slides + topic |
| 1.1 | slides | Looping | Syntactic | 1.1.1*, 1.1.2, 1.1.3 | — | 0 | Loop initialized over 8 sections |
| 1.1.1 | current_slide | State | Syntactic | (loop variable) | — | 0 | Initialized: index 0 |
| **1.1.2** | **outline_section** | **Imperative** | **Semantic** | 1.1.2.1, 1.1.1 | **1** | **~130** | **Section 1 extracted: "Introduction to ML"** |
| 1.1.2.1 | outline | (cached after first) | Semantic | 1.1.2.1.1 | 1 (first only) | ~820 | 8-section outline generated |
| 1.1.2.1.1 | topic | Data | — | (global input) | — | 0 | "machine learning in healthcare" |
| **1.1.3** | **slide content** | **Imperative** | **Semantic** | 1.1.2, 1.1.3.1 | **1** | **~580** | **Slide 1 HTML: title + 4 bullet points** |
| 1.1.3.1 | style_guide | Data | — | (global input) | — | 0 | Style config (layout: content, font: sans-serif) |
| *(×7 more loop iterations — 1.1.2 and 1.1.3 re-execute for each section)* | | | | | | | |
| 1.1 [iter 2] | current_slide | State | Syntactic | — | — | 0 | Index advanced to 1 |
| **1.1.2 [iter 2]** | **outline_section** | **Imperative** | **Semantic** | 1.1.2.1 (cached), 1.1.1 | **1** | **~110** | **Section 2 extracted: "Clinical Data Challenges"** |
| **1.1.3 [iter 2]** | **slide content** | **Imperative** | **Semantic** | 1.1.2, 1.1.3.1 | **1** | **~620** | **Slide 2 HTML: header + table (3 rows)** |
| 1.1 [iter 3] | current_slide | State | Syntactic | — | — | 0 | Index advanced to 2 |
| **1.1.2 [iter 3]** | **outline_section** | **Imperative** | **Semantic** | 1.1.2.1 (cached), 1.1.1 | **1** | **~115** | **Section 3 extracted: "Model Interpretability"** |
| **1.1.3 [iter 3]** | **slide content** | **Imperative** | **Semantic** | 1.1.2, 1.1.3.1 | **1** | **~590** | **Slide 3 HTML: two-column layout** |
| *(iterations 4–8 follow the same pattern)* | | | | | | | |
| 1.1 [iter 8] | current_slide | State | Syntactic | — | — | 0 | Final index: 7 |
| **1.1.2 [iter 8]** | **outline_section** | **Imperative** | **Semantic** | 1.1.2.1 (cached), 1.1.1 | **1** | **~105** | **Section 8 extracted: "Conclusion"** |
| **1.1.3 [iter 8]** | **slide content** | **Imperative** | **Semantic** | 1.1.2, 1.1.3.1 | **1** | **~430** | **Slide 8 HTML: closing layout** |
| 1.2 | assemble final | Imperative | Semantic | 1.1, 1.3 | 1 | ~380 | Full `.pptx` assembled; HTML preview generated |
| 1.3 | topic | Data | — | (global input) | — | 0 | "machine learning in healthcare" |

**Total: 12 LLM calls, ~8,400 tokens, 0 context leaks, 0 failures.**

---

## C.3 What This Trace Demonstrates

**Every row is complete.** There is no "see logs" or "reconstructed from prompt."
The orchestrator stores each row's full tensor in SQLite at completion time.
This is not post-hoc instrumentation — it is structural.

**Outline caching is explicit.** The `outline` node (1.1.2.1) fires once, on
the first iteration, and is then marked completed in the checkpoint store.
All subsequent iterations read from cache. This is visible in the trace:
only iteration 1 shows 1 LLM call for `outline`; all others show "(cached)."
The caching decision is a property of the dependency graph — not a runtime
optimization that may or may not fire.

**Syntactic nodes are abundant and free.** Of 31 rows in this trace (counting
loop iterations), 19 are syntactic. These 19 nodes executed in under 100ms
total, consumed zero tokens, and are invisible in the Canvas tool call monitor.
They are visible in the graph view as gray nodes — confirming that routing,
looping, and collection assembly are structurally separate from LLM reasoning.

**Scope isolation holds throughout.** No slide content action (1.1.3) receives
the full outline — it receives only the single extracted section (1.1.2). No
assembly action (1.2) receives slide-generation prompts or intermediate reasoning
— it receives only the completed slide collection (1.1). This is not enforced
by prompt engineering; it is enforced by the scope rule at the language level.

---

## C.4 Token Cost Breakdown

| Category | LLM calls | Tokens | % of total |
|----------|-----------|--------|------------|
| Outline generation (1×) | 1 | ~820 | ~10% |
| Section extraction (8×) | 8 | ~900 | ~11% |
| Slide content generation (8×) | 8 | ~4,600 | ~55% |
| Final assembly (1×) | 1 | ~380 | ~5% |
| Syntactic nodes | 0 | 0 | 0% |
| **Total** | **18** | **~6,700** | **100%** |

Note: section extraction (1.1.2) and slide content (1.1.3) each fire 8 times
(once per loop iteration). The outline (1.1.2.1) fires once and is cached.
The total semantic call count is 10 unique actions × loop count = 18 calls.

This cost structure is knowable before the run begins — the plan's topology
determines the call pattern, and the compiler can estimate token ranges from
the declared input shapes. In the Canvas execution view, the running cost
counter reflects exactly this structure.

---

## C.5 Audit Query Examples

The following queries can be answered from this trace without accessing logs,
re-running the plan, or consulting the system prompt:

| Query | Answer | Source |
|-------|--------|--------|
| What did slide 3 receive as input? | `outline_section` for "Model Interpretability" + `style_guide` (layout: two-column) | Flow index 1.1.3 [iter 3] inputs |
| Did any step access the full outline? | No — each step received only its own `outline_section` | Scope rule; 1.1.2 declared, not 1.1.2.1 |
| How many LLM calls did the outline generation make? | 1 (on first iteration; cached thereafter) | Flow index 1.1.2.1, iteration 1 |
| What was the input to the final assembly step? | The completed `slides` collection (8 items) + `topic` | Flow index 1.2, inputs 1.1 and 1.3 |
| Were there any failures? | No | Run metadata |
| What was the total cost? | ~8,400 tokens, ~12 calls | Run metadata + trace totals |
