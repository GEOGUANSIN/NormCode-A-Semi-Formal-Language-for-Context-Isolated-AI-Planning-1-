# Problem Slides — Draft
## For Discussion

This file covers the opening problem section of the presentation.
The goal: take the audience from "here is our current world" to "here is the gap" to "here is what NormCode is" — in a way that makes each step feel inevitable.

---

## The Argument in One Paragraph

The company already has mature, proven automation for UAV navigation. Rule-based systems that work. The question is: how do you add intelligent, adaptive behavior on top of that — without losing the reliability you already have? LLM agentic frameworks give you adaptation but no structure. Workflow platforms give you structure but no adaptation. NormCode is a contract language: you write the contract (what work gets done, in what order, with what inputs), and you provision a worker (the agent with its capabilities) to execute it. The contract enforces the mature automation. The worker brings the self-improvisation. The boundary between the two is explicit, readable, and enforceable.

---

## Slide P1 — What You Already Have (The Baseline)

**Headline**: Your existing UAV system is mature. That's the starting point.

**Content**:

The company already operates a rule-based UAV automation stack:

```
RULE-BASED AUTOMATION (what you have today)
─────────────────────────────────────────────

  Mission input (area, obstacles, objective)
          ↓
  Route planning algorithm  ←── deterministic, proven
          ↓
  Waypoint execution loop   ←── reliable, auditable
          ↓
  Sensor data collection    ←── structured, consistent
          ↓
  Anomaly detection rules   ←── known failure modes covered
          ↓
  Report generation         ←── templated, repeatable
```

**What this does well**:
- Repeatable: same input → same output, every time
- Auditable: every decision traceable to a rule
- Fast: no LLM latency on deterministic steps
- Safe: behavior is bounded by the rule set

**What it cannot do**:
- Handle terrain or obstacle types outside the rule set
- Adapt when the mission brief is ambiguous or novel
- Learn from past missions to improve future ones
- Reason about tradeoffs ("this route is 20% longer but avoids the high-risk zone")
- Scale to new mission types without engineering new rules

**The honest summary**: Rule-based automation is your foundation. It is not going away. The question is what you build on top of it.

---

## Slide P2 — What the LLM Revolution Offered (And What Each Approach Gets Wrong)

**Headline**: Two paths. Both incomplete.

**Layout**: Two columns, each with a visual + honest assessment.

---

### Left column: Agentic Frameworks
*(Claude / OpenClaw, Cursor, Copilot-style, AutoGen)*

**The promise**: Give the agent a goal and a set of tools. Let it figure out the steps.

```
  "Survey the area and report anomalies"
                  ↓
         [LLM Agent]
        /     |      \
   tools   tools   tools
  (fly)  (scan)  (analyze)
        \     |      /
         [result?]
```

**What it gives you**:
- ✅ Self-improvisation: the agent adapts, retries, changes approach
- ✅ Handles novel cases your rule set never anticipated
- ✅ Reads ambiguous instructions and makes reasonable decisions

**What it takes away**:
- ❌ Unclear execution boundary: the agent can invoke tools in any order, for any reason
- ❌ Hard to inject your existing mature automation: where does the rule-based route planner fit?
- ❌ Non-reproducible: run the same mission twice, get different behavior
- ❌ Not auditable: what did the agent actually decide at step 7?
- ❌ Failure recovery is ad-hoc: the agent retries blindly, or spirals, or halts
- ❌ No operator review point: the agent acts before you can check its plan

**The core problem**: self-improvisation with no contract.
The agent is a capable worker who shows up and does whatever it thinks is right. You have no visibility into the plan before execution, no checkpoint during execution, no structured record after.

---

### Right column: Workflow Platforms
*(Dify, LlamaIndex, n8n, Coze)*

**The promise**: Design a workflow visually. Each node is a step. Connect them.

```
  [Input]──▶[Route Plan]──▶[Loop: Waypoints]──▶[Scan]──▶[Detect]──▶[Report]
```

**What it gives you**:
- ✅ Structure: explicit steps, explicit connections
- ✅ Readable: non-developers can follow the graph
- ✅ Predictable: the workflow runs what you designed

**What it takes away**:
- ❌ Limited self-improvisation: when the workflow hits an unexpected case, it fails or falls to a generic "error" branch
- ❌ No structural isolation between nodes: each node can implicitly see the full context of the conversation so far
- ❌ Not truly composable: complex missions require very complex visual graphs; there is no "call sub-workflow" that is clean
- ❌ Locked to the platform: your plans are not portable; they live in Dify or they live in LlamaIndex — not both
- ❌ Hard to express iteration with carried state: the looping mechanisms are limited and brittle

**The core problem**: mature structure with no real adaptability.
The workflow is rigid. When the world doesn't match the workflow, the workflow fails. There is no mechanism to adapt mid-execution without redesigning the graph.

---

## Slide P3 — The Gap: What You Actually Need

**Headline**: Neither approach gives you what the mission requires.

**The fundamental tension**:

```
                        WHAT YOU NEED
                        ─────────────

  Mature automation ────────────────────────── Self-improvisation
  (your rule-based foundation)                 (LLM agent adaptability)

  ✅ Repeatable                                ✅ Handles novel cases
  ✅ Auditable                                 ✅ Learns from experience
  ✅ Bounded behavior                          ✅ Adapts mid-mission
  ✅ Human-reviewable                          ✅ Recovers from failure


  Agentic frameworks:   ──────────────────────────────────────── ●
                        (all self-improvisation, no structure)

  Workflow platforms:   ● ────────────────────────────────────────
                        (all structure, minimal adaptation)

  What you need:                    ●
                        (both — at the same time)
```

**The reason neither works**:
The two approaches fail at the same point — the boundary between what is fixed and what is adaptive is not explicit. In agents, there is no boundary. In workflow platforms, the boundary is the whole graph. You need a system where the boundary is a language-level concept — something you can write, verify, and enforce.

**The "AI worker" concept**:
What you are really looking for is an AI worker with two properties:
1. **A contract**: specifying what work will be done, in what order, with what inputs — your mature automation expressed in structured form
2. **Agentic capability**: a worker who can execute each contracted step intelligently, improvise within the scope of that step, and learn from past runs

The contract is not code. The contract is not a drag-and-drop graph. The contract is a language.

---

## Slide P4 — NormCode: A Contract Language for AI Workers

**Headline**: The plan is the contract. The agent is the worker. The scope rule is the provision.

**The contract analogy**:

A contract in the legal sense does three things:
1. **Specifies** what work will be done, by whom, producing what — readable by all parties
2. **Provisions** the worker's scope of action — what they can access, what they can decide
3. **Enforces** the terms — the contract has teeth; deviation is not possible within the system

NormCode is a contract language for AI agents:

```
THE CONTRACT (.ncds plan)
──────────────────────────

<- mission report                          ← what the contract delivers
    <= compile findings and assessment     ← how it is produced
    <- flight log                          ← worker A's deliverable
        <= navigate and collect data       ← worker A's contracted task
        <- sensor reading                  ← what worker A receives
            <= scan current position       ← sub-task
            <- current position            ← only this — nothing else
        <- current waypoint                ← only this — nothing else
    <- mission brief                       ← external input

                                           The scope rule:
                                           each worker only sees
                                           what the contract gave them
```

**The three roles the contract plays**:

| Role | What it means in NormCode |
|------|--------------------------|
| **Readable** | `.ncn` plain-English narrative — operator reads and approves before UAV lifts off |
| **Enforceable** | Compiler verifies scope; orchestrator executes exactly what was reviewed |
| **Composable** | Sub-plans are sub-contracts; call `uav_navigation.ncds` from `uav_mission.ncds` |

**Where your mature automation goes**:
Deterministic steps in the plan — route planning algorithms, rule-based anomaly filters, data formatting — are expressed as **syntactic nodes** (gray rectangles): free, instant, no LLM. Your existing logic does not disappear. It becomes contract provisions.

**Where the self-improvisation goes**:
LLM-powered steps — assess novel anomaly type, adapt to terrain, reason about tradeoffs — are expressed as **semantic nodes** (purple hexagons): the worker's agentic capability exercised within the contract's scope.

**The result**:
- Your mature automation is the structure of the contract
- The agent's capabilities are provisioned within each step's scope
- The operator reads and approves the contract before execution
- Every completed step is a self-contained checkpoint — recoverable, inspectable, reusable

---

## Discussion Notes

### Things to sharpen:

**On Slide P1** — we need to decide: do we open by affirming their existing system ("your current automation is good — this builds on it") or by identifying its limits ("your current automation can't handle X")? The former is less threatening to people who built the existing system. Recommend: lead with affirmation.

**On Slide P2** — the framing "what the LLM revolution offered" assumes they've already looked at / tried agentic frameworks. If they haven't, we need to adjust. Do they have a specific framework they evaluated? That changes which tool we put in the left column.

**On Slide P3** — the spectrum diagram (mature ← → improvised) is the central visual of this section. It needs to be clean and immediate. The key message: neither pole works, and the reason is not about features — it's about the absence of an explicit boundary language.

**On Slide P4** — the contract analogy is the conceptual pivot. Everything before this slide sets up the problem. This slide names the solution. The risk: contract sounds legal/rigid, which conflicts with "self-improvisation". Reframe if needed: "a contract that provisions the worker's intelligence, not just their behavior."

### Questions to resolve before finalizing:

1. Has this company evaluated specific LLM tools already? (Affects Slide P2 — do we name what they tried?)
2. How much of their current rule-based automation do they want to preserve vs. replace?
3. Is the audience technical (developers/engineers) or operational (product managers, executives)?
   - Technical: can go deeper on scope rule mechanics
   - Operational: keep the contract analogy front-and-center, skip mechanics until later slides
4. What is the single worst pain point they experience today?
   - "Full restart when something fails at step 8" → emphasize C3
   - "Can't explain to the client why the UAV took that route" → emphasize C1 + audit trail
   - "Every new mission type requires 2 weeks of engineering" → emphasize plan library + work outsourcing
