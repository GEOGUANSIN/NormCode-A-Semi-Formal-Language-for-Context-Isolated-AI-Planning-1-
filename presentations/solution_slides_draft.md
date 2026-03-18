# Solution Slides Draft — NormCode's Three Mechanisms

> **Context:** These slides follow the problem section (P1–P4).
> They answer: "How does NormCode actually close the gap?"
> Audience: UAV solution company. Tone: collaborative ("we/our").

---

## S1 — Agentic Design: Configure the Abilities

**Headline:** Before the Worker Starts, We Configure What It Can Do.

**Core idea:**
NormCode does not assume what a worker knows how to do. Before a plan
runs, we configure a set of **abilities** — the interfaces any worker in
the workflow is allowed to draw from.

A worker is not necessarily a single agent. A worker can be a group of
agents. What we configure is the **ability pool** they share.

**Abilities (examples):**
- Code execution
- Human-in-the-loop approval
- File read / write
- External API call
- Sensor data interface

**Key point:**
The ability pool is explicit and bounded. A worker in a given step can
only use abilities that have been configured. Nothing outside the pool
is reachable.

**Bottom line:**
> Agentic Design answers: *what can our workers do?*

---

## S2 — Workflow Design: Define the Work

**Headline:** Each Step Is a Declared Work, Not an Open Instruction.

**Core idea:**
The `.ncds` contract is composed of individual **works** — each one
declares:
- What it must deliver (`<-` deliverable)
- What task produces that deliverable (`<=` task)
- What it is allowed to receive as input (its indented scope)

Resources are **not global**. They are scoped to the step. The worker
at each step only sees what the contract gave it — nothing from steps
above or below that was not explicitly passed.

This is where our mature automation lives. Deterministic steps — route
planning, waypoint logic, sensor collection — are syntactic nodes. They
run without an LLM. Zero latency. Zero deviation.

Steps that require judgment are semantic nodes. The worker receives its
scoped inputs, applies its configured abilities, and produces the
declared deliverable.

**Key point:**
The boundary between fixed and adaptive is explicit in the contract.
Not implicit. Not runtime-determined.

**Bottom line:**
> Workflow Design answers: *what does each step do, and with what?*

---

## S3 — Continual Engagement: Bounded Improvisation

**Headline:** Adaptation Happens. Inside the Contract.

**Core idea:**
A worker is not just an executor. Within the scope it was given, a
worker can improvise. NormCode provides two mechanisms for this:

### Mechanism 1 — ReAct Loop
The worker observes the result of its action and decides whether to act
again. This is the observe → act → observe cycle running inside a
single step.

- The worker is not re-invoking new steps in the contract.
- It is iterating within the boundary of the current deliverable.
- The scope does not change. Only the worker's internal reasoning does.

**Use case:** The scan step receives a sensor reading that is ambiguous.
The worker retries with a different approach, then produces the
deliverable once confident.

### Mechanism 2 — Distribute Tool *(coming soon)*
The worker delegates part of its work to a **sub-worker**.

- The sub-worker is given a scoped subset of the current step's inputs.
- The sub-worker produces a partial result and returns it.
- The original worker integrates the result and completes the
  deliverable.

This is not free-form delegation. The contract still governs what is
passed and what is expected back.

**Use case:** The navigate step delegates obstacle assessment to a
specialist sub-worker without exposing the full mission context to it.

**Key point:**
Both mechanisms are **limited improvisation**. The worker adapts. But
adaptation is bounded by the declared scope — the contract is not
rewritten at runtime.

**Bottom line:**
> Continual Engagement answers: *how does the worker handle what the
> contract could not fully anticipate?*

---

## S4 — How the Three Mechanisms Combine

**Headline:** One Contract. Configured Abilities. Bounded Intelligence.

**Core idea:**
The three mechanisms are not separate products. They are layers of the
same system.

| Layer | Mechanism | What it provides |
|---|---|---|
| Capability | Agentic Design | Abilities workers can draw from |
| Structure | Workflow Design | Declared works with scoped resources |
| Adaptation | Continual Engagement | ReAct loop + sub-worker delegation |

Together they produce the balance we are looking for:

- **Mature automation** lives in syntactic nodes — deterministic, fast,
  auditable, directly carrying over our existing rule logic.
- **Self-improvisation** lives in semantic nodes + continual engagement
  — adaptive, bounded, inspectable at every checkpoint.

The contract makes the boundary between the two explicit. That
explicitness is the thing neither pure agents nor pure workflows give us.

**Bottom line:**
> NormCode does not replace our automation. It gives it a contract —
> and introduces a worker who can operate under it.

---

## Notes for Slide Design

- S1: visual = ability pool diagram (icons for each interface type,
  labeled as abilities, not tools)
- S2: visual = annotated `.ncds` block showing syntactic vs. semantic
  nodes side by side (blue vs. purple)
- S3: visual = two-panel: ReAct loop (cyclic arrow within a step box)
  | Distribute Tool (step box spawning a sub-worker box)
- S4: visual = layered architecture diagram or the three-row table
  above, with the mature/improvised split called out

---

*Next: work outsourcing — calling one `.ncds` from another (blocked
pending architecture discussion)*
