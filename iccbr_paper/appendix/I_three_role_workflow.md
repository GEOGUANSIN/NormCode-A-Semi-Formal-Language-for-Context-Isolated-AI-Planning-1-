# Appendix I — The Three-Role Workflow: End-to-End Narrative

This appendix traces the lifecycle of a single plan — `ppt_generation.ncds`
— from initial authoring through to end-user interaction. It shows the
complete three-role handoff: what each role does, what tool they use, what
artifact they produce or consume, and where one role's work ends and the
next's begins.

The purpose is to answer: "Who does what with the `.ncds` file across its
lifetime?" The body of this paper describes each role in isolation; this
appendix shows the handoff seams.

---

## I.1 Role Summary

| Role | Who | Primary tools | What they own |
|------|-----|--------------|---------------|
| **Agent Designer** | Engineer, AI specialist | NormCode language + Compiler (CLI or Canvas) | The `.ncds` file — the plan itself |
| **Product Operator** | Manager, ops team, technical lead | Canvas App (v1.1.3) + NormCode Server | The deployment — where and how the plan runs |
| **End User** | Domain expert, customer, employee | NormCode Client (web form, embedded interface) | The output — the result of one plan run |

---

## I.2 Designer's Session

**Goal:** Produce a compiled, reviewed, and version-controlled PPT generation plan.

**Step 1 — Describe.**
The designer writes `ppt_generation.ncds` in a text editor or the Canvas file
editor. Alternatively, they provide a natural-language description to the
NormCode compiler's Phase 1 derivation, which generates a draft `.ncds` for
them to review and edit.

The plan takes approximately 30 minutes to author from scratch for a designer
familiar with NormCode syntax, or 5–10 minutes to review and edit from a
Phase 1 draft.

**Step 2 — Compile.**
The designer runs:

```bash
normcode compile ppt_generation.ncds
```

The compiler produces five artifacts:
- `ppt_generation.ncd` — formal plan with flow indices
- `ppt_generation.ncn` — plain-English verification narrative
- `ppt_generation.ncdn` — hybrid format
- `concept_repo.json` — data concept definitions
- `inference_repo.json` — action definitions and wiring

If the compiler finds an error (undefined concept, scope violation, missing
dependency), it reports the offending line and description. The designer
fixes the `.ncds` and recompiles.

**Step 3 — Self-review (optional but common).**
The designer reads `ppt_generation.ncn` to verify that the compiler's
interpretation of their plan matches their intent. This takes 5–10 minutes
for a 30-inference plan. If anything is wrong, they edit the `.ncds` and
recompile.

**Step 4 — Commit.**
The designer commits `ppt_generation.ncds` (and optionally the compiled
artifacts) to the team's Git repository:

```bash
git add ppt_generation.ncds ppt_generation.ncn concept_repo.json inference_repo.json
git commit -m "Add PPT generation plan v1"
git push
```

The `.ncds` file is the primary artifact. The compiled JSON files can be
regenerated from it at any time. The `.ncn` is committed alongside for
non-technical stakeholders to read in the repository browser.

**Designer's deliverables:** `.ncds` (the plan), `.ncn` (the verification
document), compiled repositories.

---

## I.3 Operator's Session

**Goal:** Verify the plan's logic, test it with a sample input, and deploy it
to the NormCode Server for end-user access.

**Step 1 — Review.**
The operator opens Canvas and loads the compiled plan project (the folder
containing `concept_repo.json` and `inference_repo.json`). Canvas renders
the inference graph immediately — all nodes visible, no execution needed.

The operator opens `ppt_generation.ncn` from the file panel and reads it.
This is the plan's logic, stated in plain English. The operator is not a
programmer; they read English. They verify:
- Does the plan generate an outline before generating slide content? Yes.
- Does each slide see only its own section, not the full outline? Yes.
- Is the style guide available to every slide? Yes (declared as global input).
- Is there any step that accesses external data the team hasn't approved? No.

If the operator disagrees with the logic — say, the outline should reference
a brand guidelines document — they send feedback to the designer. The designer
edits the `.ncds`, recompiles, and the operator reviews the new `.ncn`.
No LLM has been called.

**Step 2 — Test run.**
The operator clicks Run in Canvas with a test topic ("quantum computing for
beginners"). They watch the inference graph execute:
- The outline generation node fires (purple, pulsing) → completes (green)
- The slide loop unfolds: 8 iterations, each producing a slide
- Syntactic routing nodes flash gray and complete instantly
- The assembly node fires → the final presentation is produced

The operator opens the tensor inspector at the assembly node's output — a
`[file]` axis with two entries: the `.pptx` path and the HTML preview path.
They click the HTML preview perceptual sign — the presentation opens in a
browser tab. They review the output and find it satisfactory.

Total test run time: approximately 90 seconds.

**Step 3 — Configure agents.**
The operator opens the agent configuration panel and confirms the LLM
assignments. For this deployment, they use a single agent (`qwen-plus`)
for all semantic steps — a cost-effective choice for routine presentation
generation.

**Step 4 — Deploy.**
The operator deploys the plan to the NormCode Server:

```bash
normcode-server deploy ppt_generation --project-dir ./ppt_project/
```

Or via the Canvas Server panel: click "Deploy" → the server registers the
plan at endpoint `/run/ppt-generation`. The deployment includes the
compiled repositories and the agent configuration.

The operator confirms the endpoint URL and sends it to the team that will
build the client interface.

**Operator's deliverables:** A running, verified, deployed plan endpoint.

---

## I.4 End User's Session

**Goal:** Get a presentation on a topic of their choice, without knowing
anything about NormCode.

**Step 1 — Access.**
The end user visits the NormCode Client interface — a web form with a single
input field and a Submit button. The interface was built by the client team
using the NormCode Client SDK; it connects to the Server's `/run/ppt-generation`
endpoint.

The end user sees:

```
┌───────────────────────────────────────────────────────┐
│  PPT Generator                                        │
│                                                       │
│  Topic: [                                           ] │
│                                                       │
│  [ Generate Presentation ]                            │
└───────────────────────────────────────────────────────┘
```

**Step 2 — Submit.**
The end user types "renewable energy in urban planning" and clicks Generate.

Behind the interface: the Client sends `POST /run/ppt-generation {topic: "..."}` →
the Server starts a NormCode Orchestrator run with the compiled plan and the
provided topic. A progress indicator appears.

**Step 3 — Output.**
After approximately 90 seconds, the interface updates:

```
┌───────────────────────────────────────────────────────┐
│  Your presentation is ready.                          │
│                                                       │
│  [▶ Preview in browser]  [⬇ Download .pptx]          │
└───────────────────────────────────────────────────────┘
```

The end user clicks Preview — an HTML presentation opens. They click Download
— the `.pptx` file is downloaded. They open it in PowerPoint.

The end user never sees a `.ncds` file, a flow index, an inference graph,
a tensor, or a perceptual sign. They see a topic input and a presentation output.

**End user's deliverable:** A `.pptx` file and HTML preview — the plan's output.

---

## I.5 What the Handoff Seams Show

**Between Designer and Operator:**
The handoff artifact is the `.ncds` file + compiled repositories. The operator
receives a plan they can inspect (`.ncn`), test (Canvas run), and deploy (Server)
without modifying it. If the operator finds a problem, they send feedback to the
designer — they do not modify the plan themselves. The `.ncds` is the designer's
artifact; the deployment is the operator's domain.

**Between Operator and End User:**
The handoff is a deployed endpoint. The end user interacts with an interface
that the client team built — not with Canvas, not with the Server API directly.
The plan's logic is completely invisible to the end user. They cannot inspect
it, modify it, or even know it exists. This is the correct information boundary:
the plan is infrastructure, not user interface.

**What this means for the organization:**
A single `.ncds` file in a Git repository is the source of truth for an
organizational capability. The designer who wrote it may have left the team;
a new designer can read the `.ncn` and understand what it does. The operator
can run it, test it, and deploy it without programming expertise. The end user
receives a clean interface that hides all complexity. The plan is a durable,
readable, executable artifact — not a platform configuration or a conversation
thread that exists only in a service's memory.

---

## I.6 Modification Cycle

When the end user or operator requests a change — "add a speaker notes section
to each slide" — the cycle is:

1. **Designer** edits `ppt_generation.ncds` (add `<- speaker_notes` and
   `<= :: generate speaker notes` within the slide loop).
2. **Designer** recompiles → new `.ncn` produced.
3. **Operator** reads the new `.ncn` — confirms speaker notes are generated
   using `outline_section` and `style_guide` (not the full outline).
4. **Operator** runs a test → verifies speaker notes appear in the output.
5. **Operator** redeploys → end users immediately receive presentations with
   speaker notes.

**Total cycle time for a simple addition:** 15–30 minutes (edit + compile +
review + test + deploy). The plan file is the only thing that changed; the
compiler, orchestrator, server, and client interface are unmodified.

This is the portability property in practice: the plan is the asset. The
infrastructure is interchangeable.
