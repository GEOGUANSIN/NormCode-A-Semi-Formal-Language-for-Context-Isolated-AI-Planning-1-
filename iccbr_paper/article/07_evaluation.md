# 8. Evaluation

We evaluate the deployed NormCode Canvas system across three dimensions: correctness
on a controlled benchmark, Level 2 CBR validation through self-hosted compilation,
and production scale across six deployed plans. The evaluation reflects deployed
production use rather than a controlled experimental design; formal statistical
comparison against baseline frameworks is future work (§9).

## 8.1 Correctness: Base-X Addition Benchmark

To validate correctness of NormCode-orchestrated execution, we implemented a base-X
addition algorithm as a NormCode plan — a controlled benchmark where correctness is
unambiguously verifiable against known mathematical results.

The task adds two arbitrary-base numbers digit-by-digit with carry-over, across
arbitrary digit lengths. The NormCode plan decomposes into approximately 25 inferences
across three nested loops: an outer loop over number pairs, an inner loop extracting
unit-place digits, and a parallel loop generating shifted number pairs.

**Result: 100% accuracy across test suites validated up to 150-digit numbers.** Because
NormCode ultimately invokes Python execution for the arithmetic steps, the final result
is deterministic. NormCode's role is to structure the derivation of the computation —
ensuring each step receives exactly the correct context and the overall logic is
auditable at every node.

The base-X benchmark also validates the Level 1 case system: mid-computation
checkpoints can be inspected (C1), revised (override a digit carry value, C3), and
forked — and resumption produces correct continuations. The isolation guarantee holds
throughout.

## 8.2 Level 2 CBR Validation: Self-Hosted Compilation

The most significant validation is that NormCode's own compilation pipeline is
expressible and executable as a NormCode plan — the NC Compilations plan.

**What the plan does.** The NC Compilations plan takes a natural-language task
description as input and produces, through four inference groups corresponding to the
four compilation phases (Derivation → Formalization → Post-Formalization → Activation),
a fully executable plan: `concept_repo.json` + `inference_repo.json` + `.ncn`
narrative. The plan contains approximately 25 inferences.

**What this validates at Level 2.** The self-hosted compilation is a Level 2 CBR
validation in three senses:

1. *Self-consistency.* The compilation pipeline, as a Level 2 case, can generate other
   Level 2 cases — and can generate itself. A reasoning medium that cannot compile
   itself under its own execution model is not self-consistent.

2. *Distillation validated.* Each run of NC Compilations produces Level 1 cases at
   each compilation phase checkpoint (Derivation output, Formalization output,
   Post-Formalization output, Activation output). If Formalization produces incorrect
   flow indices, the operator retrieves the Derivation checkpoint, revises the draft
   structure, and resumes — demonstrating that the Level 1 retrieve–revise cycle
   applies to the distillation process itself.

3. *Recursive improvement.* Improvements to the compilation pipeline are abstract case
   revisions: modify the NC Compilations `.ncds`, recompile, test by re-running the
   self-hosted compilation. A better compiler is a better Level 2 case for abstract
   case generation.

**Result.** The orchestrator successfully executed the NC Compilations plan end-to-end,
producing correct `concept_repo.json` and `inference_repo.json` for new plans.
Checkpointing allowed compilation to be paused and resumed across sessions — a natural
consequence of the Level 1 case system.

## 8.3 Current Deployment: Four Production-Ready Plans

Among the plans authored to date, four have reached production-ready status showing the generalizability of normcode:

| Plan | Inferences | Semantic | Syntactic | Notes |
|------|-----------|----------|-----------|-------|
| PPT Generation | ~30 | ~10 | ~20 | Nested loop; 6 layouts; 14 component types |
| Code Assistant | ~40 | ~15 | ~25 | 7-stage pipeline; parallel Explore |
| NC Compilations | ~25 | ~10 | ~15 | Self-hosting; Level 2 validation |
| Canvas Assistant | ~20 | ~8 | ~12 | Scoped Q&A over plan structure |


Across these plans, syntactic nodes constitute 60–70% of total inferences — instant,
zero-cost, and deterministic. Semantic nodes (30–40%) are the primary cost center;
their checkpoints offer the most Level 1 reuse value because they represent expensive
LLM computation that can be avoided on fork.

**These plans as an initial Level 2 case library.** Each encodes a reasoning pattern
for a distinct class of AI orchestration task — content generation, software engineering,
meta-compilation, and interactive Q&A — illustrating that the architecture is not
domain-specific. Whether this generalisability extends further is an open question for
future deployment.

## 8.4 Qualitative Observations on the CBR Properties

**C1 — Failure localization.** In all production runs, when a semantic inference
failed, the Tensor Inspector identified the exact inputs at the failing flow index
within two operations. No log reconstruction was required. Diagnosis time was seconds,
not minutes.

**C2 — Pre-execution review.** In the production workflow for deploying new plans,
the `.ncn` review is a standard step: the plan designer generates the `.ncn` and
shares it with a domain expert or project manager who verifies the reasoning structure
before the first run. This review catches logical errors in the plan (wrong data
dependencies, missing inputs) that would not surface until a specific LLM call failed.

**C3 — Scope-bounded re-run.** In Code Assistant runs, override-and-resume re-executed
an average of 60–70% of inferences downstream of the corrected node (Plan + Implement
+ Verify + Report). The upstream Receive, Triage, and Explore stages (8–10 LLM calls
and tool operations) were not repeated in any revision cycle.

**Level 1 fork reuse rate.** In iterative compilation sessions with the NC Compilations
plan, operators consistently forked from the Derivation output checkpoint rather than
re-running the full pipeline. This saved 4–6 LLM calls per iteration cycle —
approximately 40% of the plan's total LLM call budget.

**Case base growth.** Across development sessions over a week of regular use, the case
base accumulated hundreds of checkpoints across the PPT Agent, Canvas Assistant, and
Code Assistant plans. Manual navigation of the Checkpoint Panel remained practical,
supporting the current operator-directed retrieval approach. Automated similarity-based
retrieval would become necessary at larger scale (§9).
