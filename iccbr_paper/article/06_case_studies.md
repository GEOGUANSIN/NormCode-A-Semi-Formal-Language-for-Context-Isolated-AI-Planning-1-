# 7. Case Studies

Two case studies illustrate how the two-level CBR architecture operates in practice.
The first traces Level 2 case reuse and Level 1 case accumulation in the PPT Agent —
one of the four production-ready workflows currently running. The second traces a Code
Assistant debugging session, showing a Level 1 retrieve–revise cycle with C1 and C3
in concrete operational terms.

## 7.1 Case Study 1: PPT Agent — Level 2 Reuse and Level 1 Accumulation

The PPT Agent takes a topic as input and produces a fully rendered presentation:
structured outline, slide-by-slide content, HTML preview, and `.pptx` export. The
plan contains approximately 30 inferences organized around a nested loop.

### 7.1.1 The Plan as a Level 2 Case

`ppt_generation.ncds` is a Level 2 case: a runtime definition that specifies the
complete reasoning structure for presentation generation. Its Inference Repository
encodes the conceptual dependencies:

```
<- presentation
    <= assemble final presentation
    <- all slides
        <= collect all rendered slides into single collection
        <- slides
            <= generate slide content
            <- outline_section
                <= extract section for current slide
                <- outline
                    <= generate presentation outline
                    <- topic
            <- style_guide
            <* current_slide
    <- topic
```

The most expensive node is `outline` (flow index `1.1.2`) — a single semantic inference
that generates the full presentation structure from the topic. All slide content
inferences (`1.1.3.X` for each slide) are independent from each other, each seeing
only its own `outline_section` via the scope rule. The plan supports six slide layouts
and fourteen component types with no domain-specific extensions.

**Level 2 Reuse.** When a new topic arrives, the practitioner retrieves the PPT
Generation plan from the case library, confirms via the `.ncn` review that the outline
→ section → slide structure suits the new topic, and runs it with the new topic as
input. The entire reasoning structure is reused without modification. This is abstract
case reuse: the Level 2 case produces a fresh set of Level 1 cases.

**Level 2 Revision.** When a task requires a structural change — say, generating a
scientific report instead of a slide deck — the designer modifies the `.ncds` to
replace slide layouts with report sections, and the output renderer from HTML/PPTX to
PDF/LaTeX. After recompilation and `.ncn` review, a revised Level 2 case (the report
plan) is retained in the case library. The BOM Matching plan was developed this way:
adapted from the parallel matching pattern that already existed in the Code Assistant
plan's Explore stage.

### 7.1.2 Level 1 Case Accumulation

On first execution (a new topic), the run creates Level 1 cases at every completed
node. After approximately 10 LLM calls and 20 syntactic operations, the case base
contains checkpoints for: the generated outline, each extracted section, each generated
slide, and the assembled presentation. Each is a suspended runtime state — the full
Blackboard and Concept Repository at that flow index.

### 7.1.3 Level 1 Retrieve–Revise Across Runs

When a second, structurally similar topic arrives, the operator can retrieve the
outline checkpoint from the first run:

1. **Retrieve.** Checkpoint Panel → select run from previous topic → flow index
   `1.1.2`. Tensor Inspector opens the outline tensor: section titles and structure
   of the previous presentation.

2. **Revise.** The previous outline's section structure suits the new topic (similar
   slide count and arrangement). The operator overrides the outline tensor with a
   revised outline for the new topic — 30 seconds of editing vs. one LLM outline
   generation call. The stale boundary is computed automatically: all slide content
   and assembly nodes downstream of `1.1.2` are marked stale.

3. **Reuse (Fork).** Fork from the revised `1.1.2` checkpoint. Downstream slide
   generation, section extraction, and assembly run fresh with the new outline.
   The upstream outline generation call is not repeated.

**Cost.** The revision saves one semantic LLM call (outline generation) and reuses
all syntactic operations upstream. For repeated use of the same topic domain, the
accumulated outline cases from prior runs become a practical retrieval resource —
a concrete case base of outline structures organized by topic type.

> **[Fig. 4 here — Retrieve–Revise cycle: Panel A shows checkpoint retrieval and
> tensor inspection; Panel B shows the revised outline and stale boundary; Panel C
> shows the forked run with upstream cached and downstream re-executed]**

## 7.2 Case Study 2: Code Assistant — The Full Level 1 Retrieve–Revise Cycle

The Code Assistant handles software engineering tasks through a seven-stage pipeline:
Receive → Triage → Explore → Plan → Implement → Verify → Report. The plan contains
approximately 40 inferences. This case study demonstrates C1 (failure localization)
and C3 (scope-bounded re-run) with exact numbers.

### 7.2.1 The Task and Breakpoint

The task: understand and document NormCode's compilation pipeline. The operator sets
a breakpoint at flow index `1.3.2` — the synthesis inference that consolidates the
parallel file exploration results from the Explore stage — before execution begins.

Execution proceeds: Receive completes (1 LLM call), Triage completes (1 LLM call),
7 parallel file-reading nodes in Explore complete (7 syntactic tool calls). Execution
pauses at `1.3.2`.

### 7.2.2 Case Inspection — C1 Demonstrated

The operator opens the Tensor Inspector on the completed upstream node `1.3.1` — the
file exploration output:

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

The operator identifies the cause immediately: `src/compiler/derivation.py` is absent.
The synthesis inference at `1.3.2` can only reason from what is in `1.3.1` — and the
missing file means the plan description will be incomplete.

**C1 demonstrated.** Total inspection time: 2 clicks (breakpoint + Tensor Inspector).
No log reconstruction. No accumulated conversation history to parse. No implicit state
to search. The scope rule guarantees that `1.3.2` depends only on `1.3.1` — the
tensor is exactly the information the step will receive. The cause is precisely located.

### 7.2.3 Case Revision — C3 Demonstrated

The operator clicks **Override** on node `1.3.1`. The tensor becomes editable:

```
  [7]  %{file_location}h8j(src/compiler/derivation.py)
```

The operator clicks **Resume**. The orchestrator computes the stale set automatically
from the data dependency graph: nodes `1.3.2`, `1.4.*` (Plan), `1.5.*` (Implement),
`1.6.*` (Verify), `1.7.*` (Report) — all downstream of `1.3.1`. Nodes `1.1.*`
(Receive), `1.2.*` (Triage), and the 7 Explore file-reading nodes (`1.3.1.X`) are
upstream and preserved.

**C3 demonstrated.** Re-execution count: approximately 30 nodes (Plan + Implement +
Verify + Report stages). Preserved from cache: approximately 10 nodes (Receive, Triage,
Explore). Upstream LLM calls not repeated: 2 (Receive and Triage). The stale boundary
is exact by the scope rule — no manual specification required.

### 7.2.4 Fork for Comparison

After the corrected run completes, the operator forks from the *original* checkpoint
at `1.3.1` — the 7-file tensor without the derivation module. Two runs now exist in
the case base:

| Run | Files in Explore | Synthesis coverage | Implementation completeness |
|-----|------------------|--------------------|------------------------------|
| Run A (corrected) | 8 files | Full pipeline including Derivation | Complete |
| Run B (original) | 7 files | Pipeline missing Derivation | Incomplete |

The Report outputs of the two runs are compared directly from the Checkpoint Panel.
The fork-and-compare operation took under 30 seconds of operator interaction. The
comparison run cost approximately 30 additional LLM calls (the same downstream stages);
the 2 upstream LLM calls (Receive, Triage) were not repeated.

### 7.2.5 CBR Cycle Mapping

| CBR Operation | Canvas mechanism | What happened |
|---------------|-----------------|---------------|
| **Retrieve** | Breakpoint at `1.3.2`; Tensor Inspector on `1.3.1` | Cause identified in 2 clicks (C1) |
| **Reuse** | Resume from breakpoint (original tensor, Run B) | Run B continues from cached upstream state |
| **Revise** | Override `1.3.1` + selective re-run | Run A (corrected): ~30 nodes re-execute, ~10 preserved (C3) |
| **Retain** | Automatic checkpointing of Run A + Run B | Both corrected and original cases in case base |

The full cycle — breakpoint to corrected output to fork-comparison — took under two
minutes of operator interaction. No upstream LLM calls were repeated. Both runs are
retained in the case base for future retrieval.
