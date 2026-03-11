# Abstract

Case-Based Reasoning provides a proven framework for managing complex multi-step
problem-solving: capture execution states as cases, retrieve the closest match for
a new problem, adapt it, and retain the result. Applied to multi-step LLM
workflows — an increasingly prevalent architecture for AI deployment — CBR
suggests a natural operational model in which execution checkpoints are cases, fork
is retrieve-and-reuse, and value override is revision. This model depends on a
precondition: checkpoints must be genuinely self-contained. When reasoning steps
share implicit accumulated state, a checkpoint at step $k$ embeds not just that
step's output but all the prior state that leaked into it, making retrieval
unreliable and revision non-localizable.

We present **NormCode Canvas** (v1.1.3), a deployed system that realizes CBR at
two levels. Building on NormCode [Anon. 2025] — a semi-formal planning language
whose scope rule is verified by the compiler and enforced by the orchestrator —
the system delivers: **(Level 1) Concrete case CBR within each run**: every
execution checkpoint is a self-contained suspended runtime (Blackboard + Concept
Repository snapshot); the four CBR operations map onto Canvas interactions
(Retrieve via Tensor Inspector, Reuse via Fork, Revise via Value Override with
automatic stale-boundary computation, Retain via continuous checkpointing).
**(Level 2) Abstract case CBR across plans**: each compiled NormCode plan is an
abstract case — a runtime definition from which all executions of that task type
are instantiated. Four production-ready plans serve as an example of this
case library in practice; the compiler itself is a NormCode plan, enabling
recursive case-based learning. Three measurable properties follow structurally: **(C1)
Failure localization in O(1) operations**; **(C2) Zero-cost pre-execution
verification** via compiler-generated plan narrative; **(C3) Scope-bounded
selective re-run** preserving all upstream-cached nodes.

Two case studies illustrate the architecture in use: PPT Agent executions
accumulating a concrete case library under Level 2 plan reuse, and a Code
Assistant session localizing a failure via breakpoint inspection and
fork-and-compare (C1 and C3 with exact counts). Correctness is validated
through 100% accuracy on base-X addition (up to 150 digits) and self-hosted
execution of NormCode's own four-phase compiler pipeline.

> **Keywords:** case-based reasoning, process-oriented CBR, LLM workflows,
> workflow management, visual debugging, structural isolation, deployed systems
