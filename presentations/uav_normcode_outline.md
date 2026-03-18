# Presentation Outline
## Balancing Mature Automation and Self-Improvisation in Human-Initiated UAV Navigation via NormCode

**Audience**: UAV solution company — builds and operates AI-powered navigation + error-check systems for enterprise clients
**Tone**: Operational, concrete, business-value-first. Not academic. They know UAVs; they don't need to be sold on AI.
**Length**: ~25 minutes + discussion
**Core message**: NormCode gives your UAV system a language for its plans — so they are auditable, recoverable, reusable, and composable. You stop restarting from scratch. You start building a mission library.

---

## Core Thesis

Every UAV operation involves two kinds of intelligence:
- **Mature automation**: the proven plan that always runs the same way for the same class of mission. Repeatable. Auditable. Reviewable before takeoff.
- **Self-improvisation**: the ability to recover, adapt, and learn when something goes wrong mid-mission — without discarding everything already computed.

Current systems force you to choose. NormCode makes both possible at the same time — because structural isolation of every step means every completed step is independently recoverable, and every proven plan is independently reusable.

The new capability that unlocks the full picture: **work outsourcing** — a mission plan can call sub-plans. Navigation logic, error-check logic, and reporting logic each live in their own `.ncds` file, owned independently, upgraded independently, composed on demand.

---

## Slide Structure

---

### SLIDE 1 — Title

**Title**: Mature Automation + Self-Improvisation
A NormCode Architecture for Human-Initiated UAV Navigation

**One-line hook**:
*"Stop restarting from scratch. Start building a mission library."*

---

### SLIDE 2 — What You're Building Today (The Current Reality)

**Frame this as a picture of their actual operational world.**

Your operations look like this:

1. Operator defines mission parameters → system plans route + error-check logic
2. UAV executes: navigate → scan → detect anomalies → report
3. Something goes wrong at step 8 of 12 → **full restart**
4. Client asks "why did the UAV take that path on Tuesday?" → **reconstruct logs manually**
5. New mission arrives that's 80% identical to last week's → **rebuild from scratch**
6. You upgrade the error-check algorithm → **re-test the entire pipeline**

**These are not software bugs. They are structural problems.**
The system has no shared language for what it's doing — so every failure is total, every audit is manual, every reuse is coincidental.

---

### SLIDE 3 — The Two Properties You Need

**Mature Automation**:
> The navigation plan runs the same way every time for the same class of mission.
> Your ground operator can read it and approve it before the UAV lifts off.
> If it ran correctly last Tuesday, it runs correctly today.

**Self-Improvised**:
> When waypoint 7 has an unexpected obstacle — the system doesn't restart.
> It picks up from where it was, with only the affected steps re-executed.
> Every mission adds to a case library your next mission can draw from.

**These two properties feel like opposites. They aren't.**
The reason they appear incompatible in current systems is that current systems have no structural isolation between steps. Fix the isolation — both become possible.

---

### SLIDE 4 — NormCode: A Language for Mission Plans

**Not a framework. Not a UI. A language.**

NormCode is a semi-formal planning language: three symbols, one rule.

```
<-   what this step produces / receives as input   (data: position, sensor reading, waypoint list)
<=   what operation produces it                    (action: scan area, plan route, check anomaly)
<*   the current item in a loop                    (in-flight state: current waypoint being processed)
```

**The one rule — Scope**:
Each step only sees the data explicitly declared in its own block.
The compiler verifies this. The orchestrator enforces it at runtime.

→ No step can accidentally read a previous step's raw sensor dump.
→ No implicit context building up across steps.
→ Every completed step is structurally independent — it can be inspected, resumed from, or overridden.

**This is what makes both mature automation and self-improvisation possible simultaneously.**

---

### SLIDE 5 — Your Two Core Plans in NormCode

**Plan A: UAV Navigation** (`uav_navigation.ncds`)

A mission receives a brief, plans a route, flies it waypoint by waypoint, collecting sensor data.

```
<- navigation result
    <= compile flight summary
    <- flight log
        <= for each waypoint: navigate and collect readings
        <- waypoint data
            <= navigate to waypoint and acquire sensor reading
            <- sensor reading
                <= scan area at current position
                <- current position
            <- current waypoint
        <- waypoint list
            <= plan optimal route
            <- mission area
            <- known obstacles
        <* current waypoint
    <- mission brief
```

**Plan B: Error Check** (`uav_error_check.ncds`)

Receives collected sensor readings, analyzes each for anomalies, classifies and reports.

```
<- error report
    <= generate structured anomaly report
    <- anomaly assessments
        <= for each reading: assess and classify
        <- anomaly assessment
            <= classify this anomaly and severity
            <- anomaly type
                <= detect anomaly type in reading
                <- sensor reading
            <- current reading
        <- sensor readings
        <* current reading
    <- mission context
```

**Key observations**:
- Purple nodes (LLM calls): route planning, scan, anomaly detection, classification, report
- Gray nodes (deterministic, free): loop control, data collection, assembly
- 60–70% of nodes are syntactic — no LLM cost, no latency, no hallucination risk

---

### SLIDE 6 — [PLACEHOLDER] Work Outsourcing: Composing Plans

**[TO BE DEVELOPED — discuss architecture before this slide is finalized]**

**Concept**: A top-level mission plan can call sub-plans as units of work.
`uav_mission.ncds` calls `uav_navigation.ncds` and `uav_error_check.ncds`.

**What this enables**:
- Navigation logic and error-check logic are owned and upgraded independently
- The same error-check plan works across different mission types (patrol, inspection, delivery)
- A new mission type only needs a new top-level plan — sub-plans are reused
- Teams can specialize: one team owns navigation plans, another owns error-check plans

**Draft sketch** (structure TBD):

```
<- mission outcome
    <= [call uav_navigation plan] → navigation result
    <= [call uav_error_check plan with navigation result] → error report
    <- mission brief
    <- known obstacles
```

**[Architecture to be worked out — calling convention, data passing, checkpoint behavior across plan boundaries]**

---

### SLIDE 7 — Mature Automation: The Mission Plan Library

**Every compiled NormCode plan is a reusable mission template.**

Before any UAV lifts off, the system generates a `.ncn` plain-English narrative of the full plan:

```
(OUTPUT) navigation result
    (ACTION) compile flight summary from
    (VALUE) flight log
        (ACTION) for each current_waypoint, navigating and collecting:
        (VALUE) waypoint data
            (ACTION) navigate to waypoint and acquire sensor reading from
            (VALUE) sensor reading
                (ACTION) scan area at
                (VALUE) current position
        (VALUE) waypoint list
            (ACTION) plan optimal route from
            (VALUE) mission area
            (VALUE) known obstacles
    (VALUE) mission brief
```

**Your ground operator reads this. Approves it. UAV takes off.**

No code. No drag-and-drop. A structured narrative that describes exactly what will happen — generated from the same representation the system executes.

**For your plan library**:
- `area_patrol.ncds` — grid coverage with anomaly check
- `infrastructure_inspection.ncds` — linear path with structural assessment
- `delivery_confirmation.ncds` — navigate + verify destination conditions
- Each is reused across every mission of that type, with new inputs (area, obstacles, brief)

---

### SLIDE 8 — Self-Improvisation: What Happens When Something Goes Wrong

**Three capabilities that exist only when steps are structurally isolated:**

---

**(C1) Find the problem in 2 clicks**

Waypoint 7 produced a bad anomaly classification.
Operator opens the Tensor Inspector on that step's flow index.
Sees exactly what the classification step received — which sensor reading, what anomaly type was detected.
No log reconstruction. No scrolling through conversation history. The data is there because the scope rule enforced it.

---

**(C2) Catch the problem before takeoff**

The auto-generated narrative shows the route planning step receives `known_obstacles` but not `live_weather_data`.
Operator rejects the plan. Plan is revised. UAV never takes off with the wrong logic.
Zero LLM calls, zero flight time, zero wasted computation.

---

**(C3) Fix the problem without restarting**

New obstacle detected at waypoint 5. Operator overrides the route tensor.
System automatically identifies which steps depend on that route — only those re-execute.
Waypoints 1–4 are cached. The route planning LLM call is not repeated.
Mission continues from waypoint 5 with corrected route.

**In a 12-waypoint mission with correction at waypoint 5:**
- 4 waypoints preserved from cache
- 7 waypoints re-execute
- Operator interaction: under 90 seconds

---

### SLIDE 9 — Concrete Mission: Patrol + Error Check

**Full scenario walkthrough** (12 waypoints, 2 plans, 1 correction)

**Setup**:
- Mission type: area patrol with thermal anomaly detection
- `uav_navigation.ncds` + `uav_error_check.ncds`
- 12 waypoints; estimated 18 LLM calls total

**Run A (what happens without NormCode)**:
- Route planned. Waypoints 1–4 complete. At waypoint 5, obstacle detected.
- **Full restart.** Waypoints 1–4 re-fly. Route re-planned. 18 LLM calls repeated.
- Total time lost: ~40% of mission duration + operator frustration.

**Run B (with NormCode)**:
1. Route plan completes. Waypoints 1–4 complete with sensor data collected.
2. Operator detects new obstacle via live feed.
3. Tensor Inspector → route tensor → override 7 waypoints.
4. Stale boundary computed: waypoints 5–12 re-execute. Waypoints 1–4 cached.
5. Error check runs on full collected readings (mix of cached + new).
6. Report generated. Mission complete.

**After mission**: Both Run A (original route) and Run B (corrected route) exist in the case base. Next patrol in this area starts from the corrected route — no replanning needed.

---

### SLIDE 10 — The Case Library: Your Mission Grows Over Time

**Every mission adds to a flight case library. You stop starting from zero.**

Each completed step of each flight is a checkpoint:
- `(run_id, flow_index, sensor_readings, route_decision, blackboard_status)`
- Stored automatically. No operator action.

**What the library gives you**:

| Next mission scenario | Without case library | With NormCode |
|-----------------------|---------------------|---------------|
| Same area, new brief | Re-plan route from scratch | Retrieve previous route checkpoint, fork, adapt |
| Similar area, different obstacles | Rebuild full mission | Retrieve route plan, override obstacle tensor, resume |
| Same mission type, new UAV | Full re-test | Instantiate same plan, compare runs |
| Upgrade error-check algorithm | Re-test entire pipeline | Run revised error-check plan on cached sensor readings |

**The pattern**: the more missions you fly, the less re-computation each new mission requires.

---

### SLIDE 11 — What the Ground Operator's Day Looks Like

**Before**: Operator monitors, sees failure, restarts, waits.
**With NormCode**: Operator monitors, sees failure, opens Tensor Inspector, overrides, resumes.

```
Pre-mission:
  1. Load mission plan from library
  2. Read .ncn narrative (auto-generated): does this match intent?
  3. Approve → UAV takes off

During mission:
  4. Canvas shows live graph: each node turns green as it completes
  5. Anomaly at waypoint 7: inspect that node in 2 clicks
  6. Override the affected tensor → mission continues

Post-mission:
  7. All checkpoints automatically stored in case base
  8. Review error report
  9. If plan needs revision: edit .ncds, recompile, new narrative reviewed before next flight
```

**One operator. Multiple concurrent missions. Each on its own plan graph. Each independently checkpointable.**

---

### SLIDE 12 — Comparison: What This Architecture Provides

| Capability | Current scripted systems | Drag-and-drop platforms | **NormCode** |
|-----------|------------------------|------------------------|--------------|
| Human-readable mission plan | ❌ code | ⚠️ visual only | ✅ `.ncn` narrative |
| Pre-flight plan approval | ❌ | ❌ | ✅ (C2) |
| Resume from mid-mission failure | ❌ full restart | ❌ full restart | ✅ (C3) |
| Step-level audit trail | ❌ logs only | ❌ | ✅ Tensor Inspector |
| Mission plan reuse | manual copy-paste | per-platform | ✅ plan library |
| Composable sub-plans | ❌ | ❌ | ✅ work outsourcing |
| Multi-UAV, multi-agent | complex custom | limited | ✅ built-in |
| Accumulated case library | ❌ | ❌ | ✅ automatic |

---

### SLIDE 13 — Summary: The Architecture in Three Lines

1. **Every mission runs from a reviewed, proven plan** — the plan is a reusable template, human-approved before takeoff (mature automation)

2. **Every flight adds checkpoints to a case library** — failures are localizable in 2 clicks, corrections are scope-bounded, previous work is never wasted (self-improvisation)

3. **Mission logic is composable** — navigation, error-check, and reporting each live in their own plan file, upgraded independently, combined on demand (work outsourcing)

*The UAV that completes mission 100 is operating in a system that learned from missions 1–99.*

---

## Plans to Draft (working files alongside this outline)

| File | Status | Content |
|------|--------|---------|
| `uav_navigation.ncds` | DRAFT NEEDED | Route planning → waypoint loop → sensor collection |
| `uav_error_check.ncds` | DRAFT NEEDED | Sensor readings → anomaly detection loop → classification → report |
| `uav_mission.ncds` | BLOCKED — work outsourcing design | Top-level plan calling both sub-plans |

---

## Open Design Questions

1. **Work outsourcing calling convention** — how does a parent `.ncds` pass data to and receive results from a child `.ncds`? What happens to checkpoints at the sub-plan boundary? *(discuss before Slide 6 is finalized)*

2. **Sensor data as perceptual signs** — large sensor readings (thermal images, LiDAR point clouds) should be passed as perceptual signs `%{sensor_data}ID(path)`, not loaded into the tensor. When exactly is the sign transmuted?

3. **Hard constraints in the plan** — no-fly zones, battery limits, regulatory rules: can these be expressed as NormCode Propositions (`<>`) with `@:'` timing operators, so the plan fails explicitly rather than silently?

4. **Case similarity for retrieval** — when operator opens the checkpoint panel, what makes "mission #47" the right starting point for today's mission? GPS bounding box? Mission type? Obstacle density?

5. **Multi-UAV coordination** — if two UAVs share a mission, do they share a plan graph? Or does each UAV run its own plan with a synchronization step?

---

## Presentation Notes

**Key visual — Slide 9** (run A vs run B comparison): this is the moment the audience sees the operational difference concretely
**Key concept to land first — Slide 4** (scope rule): everything else depends on the audience understanding why isolation matters
**Work outsourcing — Slide 6**: mark as "what comes next" — don't skip it, but flag that the architecture is in design; this is a forward-looking slide
**Tone throughout**: avoid "case-based reasoning", "Level 1/2 CBR", "tensor" in spoken delivery — use "flight records", "mission library", "data at that step"
