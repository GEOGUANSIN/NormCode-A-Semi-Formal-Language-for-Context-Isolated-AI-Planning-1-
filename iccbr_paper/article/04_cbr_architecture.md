# 4. CBR Level 1: Concrete Case Management

The scope rule of §3 is an enabling condition: once each step's inputs are structurally
isolated, every completed execution state is a self-contained case. This section
formalizes what that means — defining the case object, the case base, and each of the
four CBR operations as they are implemented in NormCode Canvas.

## 4.1 What a Level 1 Case Is

A Level 1 case is not a data record about a past run. It is a **suspended NormCode
runtime** — the full execution environment at a specific flow index, captured and
persisted.

**Definition.** A *Level 1 case* $c$ is a tuple:

$$c = (r,\; f,\; \mathcal{B}_f,\; \mathcal{C}_f,\; \mathcal{E}_f^{\,?})$$

where:
- $r$ is the run identifier,
- $f$ is the flow index of the last completed node,
- $\mathcal{B}_f$ is the **Blackboard snapshot** at $f$: the full node status map
  (completed, in-progress, pending, skipped) for all nodes in the plan at the moment
  $f$ completed,
- $\mathcal{C}_f$ is the **Concept Repository snapshot** at $f$: all tensors for all
  nodes completed up through $f$, indexed by flow index,
- $\mathcal{E}_f^{\,?}$ is an **optional environment snapshot**: present when
  $\mathcal{C}_f$ contains perceptual signs referencing external resources (files, APIs,
  databases), recording sufficient state — e.g. file hashes, endpoint versions,
  input document contents — for those references to remain valid on reuse.

The Blackboard encodes *where in the execution* this case sits — what has run and what
remains. The Concept Repository encodes *what was produced* — the tensor contents of
every completed step. Together they constitute a suspended execution: an orchestrator
that loads $\mathcal{B}_f$ and $\mathcal{C}_f$ can resume execution from exactly this
point, without re-running any upstream step.

**Case quality guarantee.** Because the scope rule prevents any node from accessing
data outside its declared block, $\mathcal{C}_f$ is epistemically clean: every tensor
it contains is exactly the data that downstream nodes will use — no hidden dependency
on accumulated context, no implicit reference to prior conversation history. Retrieving
$c$ and loading $\mathcal{C}_f$ into a new execution context will produce the same
data-dependency behavior as the original execution, *provided* the external environment
referenced by any perceptual signs in $\mathcal{C}_f$ is accessible and consistent
(see §3.5). $\mathcal{E}_f^{\,?}$ makes this precondition explicit and checkable
rather than implicit. The runtime is resumable because it was isolated in the first
place.

This guarantee does not hold for workflows without structural isolation. In a framework
where steps can access accumulated conversation history, a checkpoint at step $k$
implicitly depends on the full history of steps $1, \ldots, k-1$, which is not
captured in the checkpoint itself. Retrieval of such a checkpoint in a new context
produces incorrect behavior.

## 4.2 The Case Base

**Definition.** The *case base* $\mathcal{CB}$ is the set of all Level 1 cases across
all runs:

$$\mathcal{CB} = \{(r, f, \mathcal{B}_f, \mathcal{C}_f, \mathcal{E}_f^{\,?}) \mid r \in \text{Runs},\; f \in \text{FlowIndices}(r)\}$$

The case base is persisted in SQLite. At every completed node across every run, the
orchestrator automatically writes a new case. The Checkpoint Panel in the Canvas App
is the visual interface to $\mathcal{CB}$: it lists all runs, their completion status,
and the flow indices at which checkpoints exist. The case base grows continuously and
requires no operator action to maintain (Retain, §4.6).

## 4.3 Retrieve

Retrieval selects a past case from $\mathcal{CB}$ as the starting point for a new
execution. Two triggers initiate retrieval:

1. A run **fails** at flow index $f^*$: the operator retrieves the last good checkpoint
   at some $f < f^*$.
2. A new task is **similar** to a past execution: the operator identifies a checkpoint
   from a past run whose Concept Repository content is appropriate as a starting point.

**Case inspection.** Before committing to reuse, the operator inspects the candidate
case using the Tensor Inspector — opening $\mathcal{C}_f$ at any flow index $f' \leq f$
in table, list, or JSON view. This is the human-in-the-loop verification step that
precedes reuse or revision: "does this checkpoint contain the right data for the current
task?" For syntactic checkpoints (deterministic, perfectly reproducible), reuse is
reliable without inspection. For semantic checkpoints (LLM-generated, bounded-
stochastic), the operator verifies content appropriateness.

Because $\mathcal{C}_f$ contains exactly the bounded inputs of each completed step,
this inspection is O(1): the Tensor Inspector opens the named-axis tensor directly.
There is no log reconstruction, no accumulated history to parse. This is C1 — exact
reasoning step inspection in a constant number of operations.

**Retrieval interface.** The current implementation is operator-directed: the
Checkpoint Panel displays runs with their flow indices, and the operator selects the
case. Learned similarity measures — trained on past reuse outcomes — are a natural
future extension (§9).

## 4.4 Reuse

Reuse instantiates a new execution from a retrieved case without repeating upstream
computation.

**Mechanism — Fork.** The Fork operation in the Canvas App implements reuse:

1. A new run identifier $r'$ is created.
2. The orchestrator loads $(\mathcal{B}_f, \mathcal{C}_f)$ from the retrieved case
   into the new execution context.
3. The Blackboard $\mathcal{B}_f$ marks all nodes at flow indices $\leq f$ as
   completed; all nodes at flow indices $> f$ are placed on the Waitlist as pending.
4. Execution proceeds from the first pending node, using $\mathcal{C}_f$ as the
   foundation — the orchestrator constructs each inference's input from only the
   explicitly declared tensor references, as in any run.

The original run $r$ is not modified. Both runs exist independently in $\mathcal{CB}$,
sharing a common prefix (all cases up to $f$) and producing independent suffixes from
$f+1$ onward. The Canvas Checkpoint Panel records the fork relationship:
`parent_run_id` and `fork_flow_index` are stored in SQLite.

**No upstream re-execution.** All computation through $f$ is free — the orchestrator
loads stored tensors rather than re-executing upstream inferences. For plans where
early phases are expensive (many LLM calls at the outline or exploration stage), reuse
provides substantial cost reduction.

## 4.5 Revise

Revision adapts a retrieved case to fit the current task by modifying the runtime state
before resuming.

**Mechanism — Value Override + Selective Re-run:**

1. The operator retrieves a case at flow index $f$ (via breakpoint or Checkpoint Panel).
2. The operator **overrides** a tensor in $\mathcal{C}_f$: the Tensor Inspector opens
   in edit mode; the operator modifies axis entries, adds new entries, or removes
   incorrect ones.
3. The orchestrator marks all nodes downstream of $f$ as **stale** in the Blackboard.
4. On resume, only stale nodes re-execute; all upstream-of-$f$ nodes are served from
   their cached tensors in $\mathcal{C}_f$.
5. The revised run produces new cases at every completed node.

**Scope-bounded revision (C3).** Because the scope rule guarantees that only nodes
downstream of $f$ can depend on the tensor at $f$, the stale set is exactly determined
by the data dependency graph. No manual specification of which nodes to re-run is
required; the orchestrator computes this set automatically. In a 40-inference plan where
the revision is at inference 30, the 29 upstream inferences are preserved. The
downstream 10 re-execute — the minimum necessary and sufficient re-execution.

The original case is preserved in $\mathcal{CB}$. The override creates a modified
tensor for the new run; the original checkpoint is unchanged, enabling
fork-and-compare: after revision, the operator can fork from the original to run a
side-by-side comparison.

## 4.6 Retain

Retention adds the results of every execution episode to the case base.

**Automatic checkpointing.** Every node completed during a run — initial execution,
reuse run, or revision run — writes a new case to $\mathcal{CB}$. Retention is fully
automatic: the practitioner takes no additional action. The case base accumulates
all runs' Blackboard and Concept Repository snapshots continuously.

The Checkpoint Panel reflects this growth: after a revision cycle, $\mathcal{CB}$
contains the original run's cases, the revised run's cases (sharing a prefix up to $f$,
diverging afterward), and any fork-comparison runs. All are retained and addressable by
`(run_id, flow_index)`.

**Case base maintenance** — pruning low-quality or redundant cases to prevent unbounded
growth — is a current limitation and a direction for future work (§9).

## 4.7 Summary: The Level 1 CBR Cycle in Canvas

| CBR Operation | Canvas mechanism | Key property |
|---------------|-----------------|--------------|
| **Retrieve** | Checkpoint Panel → select run/flow index; Tensor Inspector | O(1) inspection (C1) |
| **Reuse** | Fork: load $(\mathcal{B}_f, \mathcal{C}_f)$ into new run; no upstream re-execution | Isolated case = safe reuse |
| **Revise** | Value Override: edit tensor; selective re-run of stale boundary | Scope-bounded (C3) |
| **Retain** | Automatic checkpoint at every completed node → SQLite | Always, no operator action |

Level 1 CBR is the native operational loop of every Canvas run. It requires no
configuration, no special mode — isolation guarantees it by construction.
