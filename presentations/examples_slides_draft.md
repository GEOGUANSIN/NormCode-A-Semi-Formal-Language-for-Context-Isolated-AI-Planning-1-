# Examples Slides Draft — The UAV System in NormCode

> **Context:** These slides follow the solution mechanics section (P5–P8).
> They ground the abstract concepts in a real UAV system drafted as NormCode plans.
> Audience: UAV solution company. Tone: collaborative ("we/our").
> Source plans: presentations/ncds/

---

## E1 — The Plan Hierarchy

**Headline:** Five Plans. One Coherent System.

**Tag:** Our UAV System

**Core idea:**
The full UAV system is expressed as five `.ncds` plans connected by Distribute.
Each plan is a scope-isolated contract. Each knows only what was explicitly
passed to it. Together they cover the full operator-to-drone loop.

**Diagram (tree with Distribute arrows):**

```
uav_user_assistant.ncds          operator session — ReAct loop
  |
  | Distribute
  v
uav_mission.ncds                 triage — assess + dispatch
  |                   |
  | Distribute        | Distribute
  v                   v
uav_navigation.ncds  uav_error_check.ncds
                        |
                        | Distribute (conditional)
                        v
                      uav_analysis_criteria.ncds
```

**Agent labels on each plan:**
- uav_user_assistant     → user_agent
- uav_mission            → planning_agent
- uav_navigation         → drone_agent (flight) + planning_agent (log)
- uav_error_check        → drone_agent (capture) + analysis_agent (analyse)
- uav_analysis_criteria  → user_agent + analysis_agent

**Key point:**
No plan reaches outside its scope. The Distribute arrows are the only
connection between plans — and each connection passes only what the
receiving plan declares as its inputs.

**Bottom line:**
> The system is not a monolith. It is a set of contracts, each delegating
> to the next with explicit scope.

---

## E2 — The Outer Loop

**Headline:** The Operator Always Has a Worker Listening.

**Tag:** uav_user_assistant.ncds

**Core idea:**
`uav_user_assistant.ncds` is the outermost plan. It runs a self-seeding
ReAct loop — starts with an empty conversation and iterates until the
operator ends the session.

**Diagram (the loop structure, simplified):**

```
on-going messages  ←————————————————————————+
    (starts empty)                           |
         |                                   |
         v                                   |
  [each iteration]                           |
         |                                   |
    operator message   ← read input          |
    fleet status       ← retrieve UAV state  |
    operator intent    ← interpret in context|   user_agent
         |                                   |
    classify intent                          |
    ┌──────────────────────────────────┐     |
    | mission request  → Distribute   |     |
    |                  uav_mission    |     |
    | direct question  → answer       |     |
    | ambiguous        → clarify      |     |
    └──────────────────────────────────┘     |
         |                                   |
    <is session end>?                        |
         |                                   |
    NOT end → append message ————————————————+
    end     → stop
```

**Key points:**
- `user_agent` handles all operator-facing steps — it has no access to
  drone state or flight data
- `fleet status` is fetched fresh each turn — UAV availability can change
  between messages
- The mission branch distributes to `uav_mission.ncds` — the operator
  never directly triggers a flight

**Bottom line:**
> One loop. One agent. The operator talks; the system listens, classifies,
> and routes — every turn, without exception.

---

## E3 — Triage and Dispatch

**Headline:** The Plan Decides What Work Is Needed.

**Tag:** uav_mission.ncds

**Core idea:**
`uav_mission.ncds` receives a validated intent from the user assistant.
It loads context, builds and approves a mission plan, then uses conditional
flags to dispatch only the sub-missions that are actually required.

**Diagram (conditional dispatch):**

```
validated intent  ←  from uav_user_assistant
fleet status      ←  retrieved fresh
mission history   ←  past missions loaded for context
         |
         v
    approved plan     ← planning_agent triages + operator approves
         |
    ┌────┴────┐
    |         |
<nav req>  <error check req>      ← assessed from approved plan
    |         |
  @:'         @:'                 ← conditional: only fires if true
    |         |
  Distribute  Distribute
    |         |
uav_navigation  uav_error_check
    |         |
    └────┬────┘
         v
   compiled results  ← planning_agent collects
         v
   mission complete  → returned to uav_user_assistant
```

**Key points:**
- A navigation-only mission skips error check entirely — no unnecessary work
- An error-check-only mission skips navigation
- Both can run from the same approved plan
- `planning_agent` owns triage and compilation — no operator interaction here

**Bottom line:**
> The contract decides what runs. Conditions are declared, not discovered
> at runtime.

---

## E4 — Navigation: Where Mature Automation Meets Intelligence

**Headline:** The Syntactic Backbone Carries the Deterministic Work.

**Tag:** uav_navigation.ncds

**Core idea:**
`uav_navigation.ncds` is the clearest illustration of the syntactic/semantic
split. Route planning and waypoint filtering are deterministic — no LLM, no
cost, identical every run. The drone_agent takes over inside the waypoint loop
where real-world conditions require intelligence.

**Two-column layout:**

Left — Syntactic nodes (deterministic, our existing automation):
```
<= extract waypoints from approved navigation plan
<= filter waypoints below minimum safe altitude
<= plan optimal route from approved waypoints
<= for every waypoint in the route      ← loop structure
```

Right — Semantic nodes (drone_agent, adaptive):
```
<= fly to current waypoint
      drone_agent sees: current waypoint, route
      drone_agent does NOT see: mission brief, operator intent

<= scan area and collect sensor data at waypoint
      drone_agent sees: current position
      drone_agent does NOT see: anything from previous waypoints

<= navigate and handle in-flight conditions at waypoint
      drone_agent sees: sensor reading, current waypoint, route
      drone_agent does NOT see: full flight history
```

**Key point:**
The `drone_agent` is invoked three times per waypoint — each time with a
fresh, minimal scope. It cannot accumulate context across waypoints unless
that context is explicitly threaded through the plan.

**Bottom line:**
> Our route planning runs free. Our drone agent runs smart — but only
> within the boundary the contract drew.

---

## E5 — Error Check: Conditional Engagement

**Headline:** The Worker Decides Whether to Engage. The Contract Bounds How.

**Tag:** uav_error_check.ncds + uav_analysis_criteria.ncds

**Core idea:**
`uav_error_check.ncds` introduces two new patterns: a conditional Distribute
(the criteria discussion may or may not happen) and a split between the
drone_agent that captures images and the analysis_agent that interprets them.

**Three-part layout:**

Part 1 — The criteria decision:
```
<criteria discussion required>     ← planning_agent assesses

    @:'  → Distribute              @:!  → load defaults
         uav_analysis_criteria           (no discussion needed)
              |
         user_agent + analysis_agent
         discuss and refine criteria
              |
    analysis criteria  ← selected from whichever ran
```

Part 2 — Image capture loop (drone_agent):
```
inspection points  ← extracted from approved plan
captured images    ← drone_agent flies + shoots at each point
```

Part 3 — Analysis loop (analysis_agent):
```
for every captured image:
    image analysis  ← analysis_agent inspects against criteria
                       sees: one image + criteria
                       does NOT see: other images, flight data
```

**Key point:**
Two different agents handle the same mission step — `drone_agent` captures,
`analysis_agent` interprets. Their contexts are completely separate. The
analysis_agent never knows how the image was taken or what flight path
produced it.

**Bottom line:**
> The criteria discussion only happens when the worker judges it necessary.
> When it does, it runs as its own scoped plan — not an open conversation.

---

## E6 — The Agent Layer

**Headline:** Four Agents. Independent Contexts. Shared Across Plans.

**Tag:** Agentic Design

**Core idea:**
The four agents are configured once and shared across the workflow. Each
appears in multiple plans, but each invocation is scope-isolated — the agent
only sees what the contract gave it for that step.

**Four agent cards:**

user_agent
  Abilities:  human-in-the-loop, conversation, intent resolution
  Appears in: uav_user_assistant, uav_analysis_criteria
  Isolated from: drone telemetry, flight state, image data

drone_agent
  Abilities:  drone interface, sensor interface, camera interface
  Appears in: uav_navigation, uav_error_check
  Isolated from: operator conversation, intent, mission history

analysis_agent
  Abilities:  image analysis, criteria reasoning, file I/O
  Appears in: uav_error_check, uav_analysis_criteria
  Isolated from: flight commands, operator conversation, telemetry

planning_agent
  Abilities:  mission reasoning, file I/O, code execution
  Appears in: uav_mission, uav_navigation, uav_error_check
  Isolated from: operator conversation, drone hardware

**Key point:**
An agent being "shared" does not mean it carries state between plans.
Each step is a fresh invocation with a fresh scope. The agent brings
capability — the contract brings isolation.

**Bottom line:**
> Configure the agents once. The contract decides what each one sees.
> Safety is structural, not instructional.

---

## Notes for Slide Design

- E1: visual = tree diagram with labelled Distribute arrows and agent tags
- E2: visual = loop flow diagram (cyclic) with the three response branches
  shown as a fork. Highlight user_agent scope boundary.
- E3: visual = flow diagram with two @:' branches and Distribute arrows.
  Show the conditional clearly — one or both sub-missions.
- E4: visual = two-column annotated .ncds snippet (blue syntactic / purple
  semantic badges, same style as P6)
- E5: visual = three-panel layout (criteria decision / capture loop /
  analysis loop). Show the @:' / @:! split clearly.
- E6: visual = four agent cards in a 2x2 grid. Each card shows abilities,
  plans, and isolation boundary.

---

*Next: work outsourcing formal syntax — how Distribute is expressed in
compiled .ncd and how input/output binding works across plans.*
