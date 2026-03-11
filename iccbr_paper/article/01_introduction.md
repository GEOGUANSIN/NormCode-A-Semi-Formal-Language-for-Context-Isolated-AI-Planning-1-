# 1. Introduction

Multi-step LLM workflows — chains of inference steps where each step's output feeds
the next — have become the dominant architecture for AI deployment. Frameworks such as
LangChain [Chase 2022], LangGraph [Langgraph 2024], AutoGen [Wu et al. 2023], and
PromptFlow [Microsoft 2023] have made it straightforward to compose LLM calls into
pipelines: a code assistant runs 40 inferences across seven stages, a document analysis
pipeline runs 30, a product matching system coordinates parallel LLM calls over a large
catalogue. These are the operational reality of production AI systems in 2025.

When a workflow fails at step 30, standard practice is to restart from step 1. There
is no principled way to identify what went wrong at step 30, no way to correct only
that step, and no way to resume from step 29's output. The entire computation is
discarded. When a similar task arrives the next day, the computation runs again from
scratch. The experience accumulated across hundreds of workflow runs — which
intermediate states worked, which failed, where the reasoning diverged — is invisible
to the next run.

This is not a missing feature in these tools. It is a structural consequence of
how they are designed. LangChain, AutoGen, LangGraph, and PromptFlow pass information
between steps through accumulated conversation histories, shared Python state, or prompt
templates that silently reference prior outputs. A checkpoint captured
at step $k$ under these conditions is not self-contained: it embeds an implicit
dependency on the entire accumulated context of steps $1, \ldots, k-1$. Retrieving
such a checkpoint and continuing from it in a new execution context produces incorrect
behavior — the implicit context is gone, but the checkpoint does not encode it.
Diagnosing a failure at step $k$ requires reconstructing this accumulated context —
O(k) effort regardless of tooling sophistication.

**The missing piece is a reasoning medium.** What is absent from the AI orchestration
stack is a shared, interpretable language in which multi-step reasoning plans are
formulated, verified, executed, and accumulated as experience — the role that SQL fills
for databases and that formal notation fills for mathematics. Without such a medium,
reasoning plans are locked inside code (opaque to non-developers), locked inside
no-code platforms (unscalable, proprietary), or left implicit in prompt engineering
conventions (unrepeatable, unverifiable). A reasoning medium must be simultaneously
human-readable and machine-executable — and it must enforce the structure it describes.

**NormCode is that medium.** NormCode [Anon. 2025] is a semi-formal planning
language for LLM workflows with six properties that together constitute a working
reasoning medium: *Interpretable* (readable by multiple roles without programming
expertise), *Enforceable* (compiler-verified structure that the orchestrator executes
exactly as reviewed), *Composable* (three symbols and one scope rule, unlimited
depth), *Locally Addressable* (every step has a precise flow index; every step is
epistemically self-contained by the scope rule), *Generalizable* (domain-agnostic
primitives for any workflow), and *Portable* (plain text, any compliant orchestrator).

The scope rule is the structural mechanism: each step's inputs are declared explicitly
in an indented block, and the compiler verifies that no step accesses data outside its
block. The orchestrator enforces this at runtime. A checkpoint captured under this
guarantee is a **self-contained case**: its tensor contains exactly the data downstream
steps will use, with no implicit context dependency.

**When a reasoning medium has these six properties, Case-Based Reasoning is what you
get — at two levels simultaneously.** This is the central claim of this paper. The two
levels emerge from the medium's structure, not from additional engineering:

- **Level 1 (Concrete Case Management):** Every completed execution checkpoint is a
  *suspended NormCode runtime* — the full Blackboard (node status map) and Concept
  Repository (all tensors for all completed nodes) at a specific flow index. The four
  CBR operations map directly onto Canvas interactions: Retrieve (Tensor Inspector),
  Reuse (Fork), Revise (Value Override with automatic stale-boundary computation),
  Retain (automatic checkpointing at every completed node).

- **Level 2 (Abstract Case Learning):** Every compiled NormCode plan is a *runtime
  definition* — an abstract case specifying what all executions of that task type are
  possible. Four production-ready plans serve as an initial case library of abstract reasoning patterns.
  The compilation pipeline (Derivation → Formalization → Post-Formalization →
  Activation) is the distillation process; it is itself a NormCode plan — enabling
  recursive case-based learning.

**NormCode Canvas (v1.1.3)** is the deployed system that makes both levels accessible.
Three measurable properties absent from existing LLM workflow tools follow structurally
from the reasoning medium:

**(C1) Failure localization in O(1) operations.** Breakpoint inspection of the Tensor
Inspector answers "what did step $k$ receive?" in two clicks. The bounded inputs are
structurally available — not reconstructed from logs — because the scope rule enforced
it.

**(C2) Zero-cost pre-execution review.** The compiler's Formalization phase produces
a `.ncn` file — a plain-English narrative of the full plan — available before any LLM
call is made. A domain expert reads this narrative and rejects the plan if the reasoning
structure does not match intent. All prior human-in-the-loop interventions for LLM systems — RLHF [Ouyang et al. 2022],
Constitutional AI [Bai et al. 2022], red-teaming — operate during or after
probabilistic computation; the `.ncn` review is the only intervention at the plan
structure level before any computation begins.

**(C3) Scope-bounded selective re-run.** When a case is revised at flow index $f$, the
orchestrator re-executes only the transitively downstream nodes. In a 40-inference plan
with a revision at inference 30, 29 upstream inferences are preserved from cache.

**Relation to the companion language paper [Anon. 2025].** The companion paper is a
language specification: it defines NormCode's grammar, symbol set, type system, and
scope rule, and gives a formal account of the compilation theory. The Canvas App and
the compiler appear there briefly as one of six contributions (~400 words combined).
That paper answers *what NormCode is*. This paper answers *what NormCode makes
possible*: it takes the language as a given and demonstrates that the Canvas App and
compiler together realize a full two-level Case-Based Reasoning system — with concrete
case definitions, the four CBR operations mapped to deployed UI interactions, the
compiler as a Level 2 distillation process, and three measurable properties (C1, C2,
C3) demonstrated in production. None of these claims appear in the companion paper;
it explicitly defers the CBR framing and empirical evaluation to future work.

**System scope.** Four production-ready workflows, ranging from 20 to 40 inferences per plan.
60–70% of nodes across all plans are syntactic (deterministic, zero LLM cost).

**Contributions:**

1. **Two-level CBR realized by a reasoning medium** (§4–§5): Level 1 cases as
   suspended runtimes; Level 2 cases as runtime definitions; the compilation pipeline
   as distillation; self-hosting as recursive case-based learning.

2. **The six properties of a reasoning medium** (§3): Interpretable, Enforceable,
   Composable, Locally Addressable, Generalizable, Portable — with NormCode as a
   concrete realization of each.

3. **Three measurable properties of the deployed system** (§6–§7): C1, C2, C3
   demonstrated through the Canvas App and two production case studies.

4. **Evaluation of a deployed production system** (§8): four production-ready workflows,
   100% accuracy on a controlled benchmark, self-hosted compilation as Level 2 CBR
   validation.

This paper is submitted under the **Deployed Applications** category. The NormCode
language specification is in [Anon. 2025]. Background on POCBR and the case
integrity requirement is in §2.
