# 2. Background: Process-Oriented CBR and LLM Workflows

## 2.1 The CBR Cycle

Case-Based Reasoning [Aamodt & Plaza 1994; Kolodner 1993] solves new problems by
retrieving and adapting solutions from a case base of past experiences. The
standard four-stage cycle — **Retrieve** a similar past case, **Reuse** its
solution as a starting point, **Revise** it to fit the new problem, **Retain**
the result as a new case — provides a principled framework for experience-based
problem solving without starting from scratch.

The quality of the CBR cycle depends critically on the integrity of cases in the
case base: a case must be a self-contained, reliable record of a past solution
state. Cases contaminated with irrelevant or implicit context produce unreliable
retrieval and incorrect reuse.

## 2.2 Process-Oriented CBR

Traditional CBR treats cases as problem–solution pairs [Kolodner 1993].
Process-Oriented CBR (POCBR) extends this to **processes as cases** — the case
captures a workflow trace: the sequence of operations, their intermediate states,
and the data that flowed between steps [Bergmann 2002; Minor et al. 2014].

POCBR is valuable for complex multi-step tasks where the path to a solution
matters as much as the solution itself. Workflow retrieval identifies similar past
executions; workflow adaptation modifies a retrieved trace to fit a new task
context; workflow retention stores the adapted trace for future reuse. Applications
include business process management [CITE: bpm], scientific workflow reuse [Gil et
al.], and clinical pathway adaptation [Peleg et al.].

Multi-step LLM workflows are a natural POCBR domain: they are complex processes
whose intermediate states contain valuable information about what worked, what
failed, and where intervention was needed. The challenge — described in §2.3 — is
ensuring that intermediate states are suitable CBR cases.

## 2.3 The Case Integrity Problem in LLM Workflows

The fundamental requirement for POCBR is **case integrity**: each intermediate
state in a workflow trace must be self-contained — its stored data must be exactly
what the next step needs, with no implicit dependency on information that is not
stored in the case itself.

Most LLM orchestration frameworks do not satisfy this requirement. LangChain,
LangGraph, and AutoGen execute steps by passing information through accumulated
conversation histories or prompt templates that silently reference prior outputs.
A checkpoint captured at step $k$ under these conditions is not a clean case: it
is a snapshot of the shared state at that moment — which includes everything from
steps $1, \ldots, k-1$ that happened to be in scope. Three consequences follow:

**Unreliable retrieval.** Retrieving such a checkpoint and continuing from it in
a new execution context produces incorrect behavior: the implicit context the
checkpoint depended on is no longer present, but the checkpoint's stored data
does not encode it.

**Non-localizable failures.** When step $k$ fails, the cause may be anywhere in
the accumulated implicit state, not in the declared inputs of step $k$ itself.
Revision requires locating this cause — which is not possible when the context
boundary is implicit.

**Irreproducible cases.** Two executions that load the same checkpoint may
produce different outputs because the implicit context that was present during
the original execution is not present during reuse.

These three failures are not engineering deficiencies that can be patched through
better tooling — they are structural consequences of the absence of an isolation
guarantee.

## 2.4 Structural Isolation as the Enabling Condition

POCBR in LLM workflows requires that intermediate execution states are case-
integrity-preserving — a property that must be guaranteed at the level of the
workflow language, not inferred post-hoc from logs.

**Definition.** A workflow language provides *structural isolation* if:
1. Each step can access only data explicitly declared in its own scope block.
2. This constraint is verified by the compiler before execution.
3. The orchestrator constructs each step's input from only its declared
   references, enforcing the constraint at runtime.

If a language provides structural isolation, then for every completed step $k$:
- The stored output tensor contains exactly the data downstream steps will need.
- Any failure at step $k+1$ has a cause in the declared inputs of $k+1$ — which
  are exactly the outputs of the steps explicitly declared as its inputs.
- Retrieving the checkpoint at step $k$ and continuing from it in a new context
  will produce the same data-dependency behavior as the original execution.

NormCode [Anon. 2025] is designed around this enabling condition. §3
describes how its scope rule, verified by the compiler and enforced by the
orchestrator, provides structural isolation. §4 formalizes the POCBR architecture
this enables.
