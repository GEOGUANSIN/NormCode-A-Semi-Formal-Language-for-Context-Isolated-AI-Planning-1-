# Appendix E — Perceptual Signs and the Tensor System

This appendix explains two foundational concepts that appear in the body of
this paper but are not fully elaborated there: perceptual signs (the pointer
mechanism seen in the Scenario B tensor inspector) and the tensor system
(the N-dimensional data structure used to represent all data flowing through
a NormCode plan).

---

## E.1 The Context Pollution Problem

Multi-step AI agent workflows typically accumulate context. Step N's prompt
contains step N-1's prompt, which contains step N-2's prompt, and so on:

```
CONVENTIONAL MULTI-STEP PROMPT STRUCTURE:

[System prompt]
[Step 1 instruction + output]
[Step 2 instruction + output]
[Step 3 instruction + output]
...
[Step N-1 instruction + output]
[Step N instruction]
```

As the history grows, several failure modes emerge:

| Failure mode | Mechanism | Effect |
|-------------|-----------|--------|
| **Attention dilution** | LLM attention spreads across entire history | Later steps given less focus than earlier ones |
| **Context override** | Early instructions persist and conflict with step N | LLM follows the wrong instruction |
| **Hallucination amplification** | A hallucinated output in step K pollutes all subsequent steps | Error propagates and compounds |
| **Irreproducibility** | Repeating step N produces different results if history has changed | System behavior depends on prior state |
| **Audit impossibility** | "What did step N actually use?" requires reconstructing the full prompt | No clean answer without full log |
| **Token waste** | 90% of tokens in step N's prompt may be prior-step content irrelevant to step N | Unnecessary cost and context pressure |

NormCode eliminates context pollution by construction. No step receives a
prompt that contains prior steps' outputs unless that output is explicitly
declared as an input in the plan. The mechanism is the tensor system plus
perceptual signs.

---

## E.2 Perceptual Signs

### E.2.1 Definition

A perceptual sign is a lightweight pointer token that *identifies* a data
object without *containing* its content. The orchestrator passes perceptual
signs between steps; the LLM sees the sign, not the data. Content is
retrieved only when a step has a grounded tool action (`<= ::`) that
explicitly reads the referenced object.

**Format:**

```
%{norm_type}unique_id(signifier)
```

| Component | Format | Description |
|-----------|--------|-------------|
| `norm_type` | Identifier in `{}` | The type of the referenced object; determines which tool resolves it |
| `unique_id` | Alphanumeric hash | Stable session-scoped identifier; same object across steps has the same ID |
| `signifier` | Human-readable string in `()` | A label that makes the sign interpretable to humans (filename, title, etc.) |

### E.2.2 Examples by Type

| Norm type | Example sign | Signifier meaning |
|-----------|--------------|------------------|
| `file_location` | `%{file_location}a1c(src/orchestrator.py)` | A file path in the project |
| `document` | `%{document}b2d(Q3 Financial Report)` | A document by title |
| `url` | `%{url}c3e(https://...)` | A web resource |
| `model` | `%{model}d4f(assembly_v2.stl)` | A 3D model file |
| `image` | `%{image}e5g(figure_3.png)` | An image file |
| `db_record` | `%{db_record}f6h(customer:12345)` | A database record by ID |

### E.2.3 Token Cost Comparison

Consider an Explore stage that identifies 10 relevant source files averaging
500 lines each:

| Approach | Tokens passed to synthesis step | Risk |
|----------|--------------------------------|------|
| **Raw content (conventional)** | ~100,000 tokens (10 × 500 lines) | Context overflow; attention dilution across all files |
| **Perceptual signs (NormCode)** | ~100 tokens (10 signs × ~10 tokens each) | None — content retrieved on demand by specific actions |

The synthesis step receives 10 signs. If it needs the content of file 3,
it declares a `<= :: read file` action in the plan that retrieves it.
Files it does not need are never loaded into its context — by declaration,
not by runtime heuristic.

---

## E.3 The Tensor System

### E.3.1 Tensors as the Data Representation

Every concept in a NormCode plan — every `<-` declaration — is stored as
a tensor when it is resolved. A tensor is an N-dimensional array with named
axes. This is the data structure the tensor inspector displays.

**Why tensors?**
- Named axes make data self-describing: `Axis: [file], Shape: (7,)` is
  immediately interpretable without a schema lookup.
- N-dimensional structure supports nested data naturally: a collection of
  documents with multiple attributes per document is a 2D tensor with axes
  `[document]` and `[attribute]`.
- Axis names are declared in the plan (assigned by the compiler during
  Post-Formalization) — they are part of the formal specification,
  not inferred at runtime.

### E.3.2 Tensor Shapes by Use Case

| Use case | Axes | Shape example | Contents |
|----------|------|---------------|----------|
| Single string value | (scalar) | `()` | A topic string |
| File collection | `[file]` | `(7,)` | Seven file perceptual signs |
| Slide collection | `[slide]` | `(8,)` | Eight slide HTML strings |
| BOM match results | `[item]`, `[attribute]` | `(25, 4)` | 25 items × 4 attributes (part_id, match, confidence, status) |
| 3D analysis results | `[issue_type]`, `[severity]` | `(6, 3)` | 6 issue types × 3 severity levels |

### E.3.3 Tensor Inspector: Three View Modes

The Canvas tensor inspector provides three display modes for any stored tensor:

**Table view (default for 2D tensors):**
```
Axis: [item] × [attribute]   Shape: (3, 4)

         part_id    match              confidence  status
  [0]    BOM-001    CAT-3829-A         0.94        matched
  [1]    BOM-002    CAT-1104-C         0.72        low-confidence
  [2]    BOM-003    (none)             0.0         unmatched
```

**List view (for 1D tensors):**
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

**JSON view (for arbitrary depth):**
```json
{
  "axis": ["file"],
  "shape": [7],
  "data": [
    { "id": "a1c", "norm": "file_location", "signifier": "src/orchestrator.py" },
    { "id": "b2d", "norm": "file_location", "signifier": "src/blackboard.py" },
    ...
  ]
}
```

The JSON view is used when a tensor contains nested structures or when
an operator wants to copy the data for external processing.

---

## E.4 Perceptual Signs as a Debugging Tool

The interaction between perceptual signs and the tensor inspector creates
the debugging property described in Scenario B (§5). Because:

1. Every step's input is a tensor (not a raw prompt string)
2. Every tensor is stored in the SQLite checkpoint at step completion
3. The tensor inspector displays any stored tensor in three human-readable modes
4. Perceptual signs in the tensor are labeled with their signifiers

...an operator at a breakpoint can answer "what will the next step see?" in
two clicks: open the tensor inspector on the upstream node, read the list.

In Scenario B, the operator saw:
- A `[file]` axis with 7 entries — identified by their signifiers
- Missing: `src/compiler/derivation.py`
- Cause: the Explore stage's search pattern did not match the derivation module

The diagnosis took under 30 seconds. In a conventional multi-step system,
the same diagnosis requires:
1. Locating the relevant prompt in the tool call log
2. Parsing the full prompt string to identify which files were mentioned
3. Comparing that against the full file tree
4. Determining which file is missing
5. Verifying that the missing file is actually relevant

None of those steps are necessary when the input is a typed, labeled tensor
stored structurally at every step completion.

---

## E.5 Value Override and Selective Re-Run

When an operator overrides a tensor value at a breakpoint (as shown in
Scenario B, Step 3), the orchestrator:

1. Replaces the stored tensor in SQLite for the overridden node.
2. Marks all downstream nodes (nodes that have this node as an input dependency)
   as stale.
3. Re-runs stale nodes in topological order.
4. Leaves all non-downstream nodes (upstream and parallel branches) in their
   completed state.

The result: the override propagates exactly as far as it needs to, and no
further. In the Scenario B case:
- The `synthesize exploration findings` node (1.3.2) and all stages downstream
  of it (Plan, Implement, Verify, Report) re-ran.
- The seven completed file-read nodes in the Explore stage did not re-run.
- The Triage and Receive stages did not re-run.
- Total LLM calls for the corrected partial run: ~6 (vs. ~12 for a full restart).

This is a deterministic property of the dependency graph, not a heuristic.
The orchestrator knows exactly which nodes depend on the overridden value
because the plan declares all dependencies explicitly.
