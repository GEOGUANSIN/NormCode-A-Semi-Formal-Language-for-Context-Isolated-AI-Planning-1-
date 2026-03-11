# 9. Discussion

## 9.1 Language as the Substrate

The central argument of this paper is not that NormCode has useful debugging features,
or that checkpoints are convenient for workflow management. It is that the six
properties of a reasoning medium — Interpretable, Enforceable, Composable, Locally
Addressable, Generalizable, Portable — are not features to be added to a workflow tool.
They are the structural preconditions for reliable CBR.

C1, C2, and C3 are not design choices about the Canvas App. They are structural
consequences of having a reasoning medium with these properties:

- **C1** (O(1) case inspection) follows from Local Addressability: every step has an
  exact flow index, its inputs are exactly its declared scope, and the Tensor Inspector
  reads the bounded inputs directly. Without Local Addressability, inspection requires
  reconstructing accumulated context — O(k) effort for step $k$.

- **C2** (pre-execution review) follows from Interpretability + Enforceability: the
  `.ncn` is a human-readable rendering of the formal plan, and what the reviewer reads
  is exactly what executes. Without both properties together, a review is either
  unreadable (too formal) or non-binding (advisory only).

- **C3** (scope-bounded re-run) follows from Local Addressability + Enforceability:
  the scope rule determines exactly which downstream nodes depend on any given step, and
  the orchestrator enforces this boundary. Without enforceability, the stale set cannot
  be computed deterministically.

Existing LLM orchestration tools can add checkpoint UI features. They cannot produce
C1–C3 structurally without first providing a reasoning medium that satisfies these six
properties.

## 9.2 Sustainable Improvement Through Two-Level CBR

A reasoning medium with two-level CBR produces a system that improves through use in
a principled way:

- **Level 1 accumulation:** Every run deposits concrete cases. The case base grows
  continuously; past checkpoints are available for retrieval, reuse, and revision
  without operator intervention.

- **Level 2 refinement:** Each domain that warrants a new plan extends the abstract
  case library. Plans are revised as task patterns evolve, and revised plans are
  retained. The case library encodes organizational experience.

- **Recursive improvement:** The compilation pipeline — itself a Level 2 case —
  improves through the same revision cycle. A better compiler produces better plans;
  better plans produce better Level 1 cases; better Level 1 cases inform better Level
  2 revisions. The recursive structure is what makes "sustainable improvement" a
  structural property of the system, not an aspiration.

This is what distinguishes NormCode from a logging or tracing tool. A logging tool
records what happened. NormCode accumulates experience in a form that can be retrieved,
reused, and improved — which is what CBR theory has always proposed and what prior
POCBR work [Bergmann 2002; Müller & Bergmann 2015] has developed for workflow domains.
NormCode instantiates this for LLM orchestration, with structural isolation as the
enabling condition.

## 9.3 What CBR Gains from a Reasoning Medium

**A language substrate that guarantees case integrity.** Prior POCBR work has largely
assumed that cases are well-formed — addressing retrieval and adaptation without
formalizing the preconditions for case reliability. NormCode contributes a structural
answer: the scope rule, enforced at compile time and runtime, guarantees that every
checkpoint is a self-contained case. Case integrity is not a property to be verified
after the fact; it is guaranteed by the language.

**A new case type: the suspended runtime.** The Level 1 case definition (Blackboard +
Concept Repository snapshot) extends POCBR's case representation beyond workflow traces
[Leake & Kendall-Morwick 2008; Bottrighi et al. 2016] to resumable execution
environments. This is not a terminological difference. A trace records what happened;
a suspended runtime is a state from which execution can be continued — with exactly the
same data-dependency behavior as the original execution. Retrieval of a suspended
runtime produces a guarantee that retrieval of a trace does not.

**A concrete instance of two-level CBR.** Müller & Bergmann [2015] introduced
generalized workflow cases as a two-level structure; this paper deploys it: a case
library of six abstract reasoning patterns (Level 2), each generating concrete cases
on every run (Level 1), with the distillation process (compilation pipeline) itself a
Level 2 case. The architecture is validated in production, not only in theory.

## 9.4 Limitations

**Manual retrieval.** The Checkpoint Panel requires operator judgment to select the
appropriate fork target and flow index. For practitioners unfamiliar with the plan
structure, identifying the right checkpoint requires plan knowledge. Learned similarity
measures — trained on past reuse outcomes (which checkpoints led to successful outputs
downstream?) — would lower this barrier substantially.

**Unbounded case base growth.** The current system retains all checkpoints
indefinitely. For long-running deployments with many runs, the Checkpoint Panel
becomes cluttered and case base search becomes slower. Competence-based pruning [Smyth
& McKenna] — removing cases that add no new retrieval coverage — and quality-based
filtering (deprioritize cases from failed runs) are well-studied approaches applicable
here.

**Semantic checkpoint reproducibility.** Syntactic checkpoints are perfectly
reproducible (deterministic). Semantic checkpoints (LLM outputs) are
bounded-stochastic: given the same input tensor and LLM configuration, the output
follows a distribution rather than a fixed value. Reuse of semantic cases is
probabilistically valid but not guaranteed to reproduce the original output — an
important caveat for high-stakes applications.

**Environmental replication for perceptual-sign cases.** A checkpoint is structurally
self-contained, but if its tensors contain perceptual signs pointing to external
resources — source files, uploaded documents, API endpoints — those resources must be
accessible and consistent for reuse to produce valid continuations. A case retrieved
from a run six months ago may reference files that have since been modified or deleted.
This is analogous to the open-world assumption problem in knowledge representation: the
case encodes *what was referenced*, not the referenced content. Operators must verify
environmental preconditions before forking from perceptual-sign checkpoints in
long-running deployments.

**LLM-assisted derivation.** The Derivation phase (Phase 1 of compilation) uses an
LLM to extract conceptual structure from natural language. This introduces
non-determinism in plan generation. The resulting plan is reviewed in the `.ncn`
format before execution, but the derivation process itself is not fully auditable in
the same way as execution. A more formal derivation procedure is a direction for future
work.

## 9.5 Generality

The two-level CBR architecture is not specific to NormCode's implementation. Any
orchestration system that satisfies: (1) structural isolation between steps, (2)
persistent addressable checkpoints, and (3) resumable execution from any checkpoint,
instantiates a Level 1 process-oriented CBR system. Any system that also supports
(4) a plan representation that is human-reviewable and compiler-verified adds Level 2.
NormCode provides all four by design. The six properties of §3 are a characterization
of what a reasoning medium must have to support both levels naturally.

The broader implication: other domains where complex multi-step reasoning is externalized
into a shared medium — scientific workflow management, legal document processing, medical
treatment planning — would benefit from the same architecture. The requirement is a
medium with the six properties, not NormCode specifically.
