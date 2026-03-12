# Appendix D — The `.ncn` Format: Extended Examples

The NormCode Natural (`.ncn`) format is a compiler-generated plain-English
narrative of a NormCode plan. It is produced automatically at the end of
Phase 2 of the compilation pipeline — before any execution resource is
assigned, before any LLM is called. It is not a description of what the
system does; it is a verbatim translation of the formal plan structure
into prose that any stakeholder can read.

This appendix gives three extended examples and a compliance checklist
application. The body of this paper uses the `.ncn` in §4 (the PPT Agent
review step); the detail omitted there is provided here.

---

## D.1 Format Conventions

The `.ncn` format uses five structural keywords, each corresponding to a
`.ncds` element:

| Keyword | Maps to | Meaning |
|---------|---------|---------|
| `(OUTPUT)` | `<-` concept | The concept being produced by this block |
| `(ACTION)` | `<=` action | How the concept is produced |
| `(INPUT)` | `<-` nested concept | A declared input to this action |
| `(STATE)` | `<*` state | A loop variable carried across iterations |
| `(LOOP over X)` | Looping paradigm | Iteration marker |

The indentation of the `.ncn` mirrors the indentation of the `.ncds`. Each
`(INPUT)` block is itself a nested `(OUTPUT)/(ACTION)/(INPUT)` sub-tree,
preserving the full dependency structure. No information is lost in
translation.

---

## D.2 Example 1 — Simple: Two-Step Summary

**`.ncds` source:**

```
<- summary
    <= summarize the findings
    <- report
        <= :: read the uploaded file
    <- style_guide
```

**`.ncn` output:**

```
(OUTPUT) summary
  (ACTION) is obtained by summarizing the findings
  (INPUT)  using report
             (OUTPUT) report
               (ACTION) is obtained by reading the uploaded file
               (INPUT)  [grounded to: file_system tool]
               (INPUT)  [file path provided by caller]
  (INPUT)  and style_guide
           [provided by caller as a global input]
```

**What a reader learns:**
- `summary` is produced by one LLM action that receives exactly two things:
  `report` and `style_guide`.
- `report` is produced by reading a file — not by another LLM call.
- `style_guide` is an external input (provided by the user running the plan).
- `summary` cannot access the file directly; it sees only the report.

A reader with no programming background can verify: "Does the summarizer
see the raw file? No — it only sees the report that was read from it. Is
that what we want?" If the answer is no, the designer adds `<- raw_file`
to the summarizer's scope before the plan runs.

---

## D.3 Example 2 — Nested Loop: PPT Slide Generation

**`.ncds` source (partial — the slide generation loop):**

```
<- slides
    <* current_slide
    <= :: generate slide content
    <- outline_section
        <= :: extract section for current slide
        <- outline
            <= :: generate presentation outline
            <- topic
    <- style_guide
```

**`.ncn` output:**

```
(OUTPUT) slides
  (LOOP over current_slide)
  (STATE)  current_slide tracks position across iterations
  (ACTION) is obtained by, for each current_slide,
           generating slide content
           [grounded to: slide_generator tool]
  (INPUT)  using outline_section
             (OUTPUT) outline_section
               (ACTION) is obtained by extracting the section
                        for the current slide
                        [grounded to: section_extractor tool]
               (INPUT)  using outline
                          (OUTPUT) outline
                            (ACTION) is obtained by generating
                                     a presentation outline
                            (INPUT)  using topic
                                       [provided by caller]
               (INPUT)  and current_slide
                          [loop state — current iteration index]
  (INPUT)  and style_guide
           [provided by caller as a global input]
```

**What a reader learns:**
- `slides` is produced by a loop — one slide per iteration.
- Each iteration of the loop produces one `outline_section`, then uses it
  plus the `style_guide` to produce one slide.
- The outline is generated once (not per slide) — this is visible because
  the `outline` sub-tree appears inside `outline_section`, not inside the
  per-slide block.
- `style_guide` is global — available to every slide without repetition.
- No slide content action can see another slide's output or the full outline.

A compliance officer reviewing this for a regulated document-generation
workflow could verify: "Does slide 3 see slide 2's content? No. Does it
see the full outline? No — only its own section. Is there any accumulated
state between slides other than the loop index? No."

---

## D.4 Example 3 — Judgement with Branching: Code Verification

**`.ncds` source (the Verify stage of the Code Assistant):**

```
<- verification_result
    <= :: is the implementation correct?
    <- diff
    <- task_constraints
        <= :: extract constraints
        <- task_description
```

**`.ncn` output:**

```
(OUTPUT) verification_result
  (ACTION) is obtained by determining whether
           the implementation is correct
           [returns: boolean + reasoning trace]
  (INPUT)  using diff
           [provided by Implement stage output]
  (INPUT)  and task_constraints
             (OUTPUT) task_constraints
               (ACTION) is obtained by extracting
                        the task constraints
               (INPUT)  using task_description
                          [provided by caller / Receive stage]
```

**What a reader learns:**
- The verification step makes a yes/no decision.
- It sees the implementation diff and the extracted constraints — not the
  full task description, not the exploration results, not the plan.
- The constraints are extracted from the task description by a separate
  action — the verifier does not parse the task itself.
- The reasoning trace is part of the output tensor (alongside the boolean),
  making the verification decision auditable.

After this step, a timing node (syntactic, not shown) reads the boolean
and routes either to the Report stage (pass) or back to the Plan stage
(fail). The routing logic is structurally guaranteed — not a prompt instruction.

---

## D.5 Compliance Checklist Application

For regulated domains (financial analysis, legal review, medical reasoning),
the `.ncn` format maps directly to a pre-execution compliance checklist.
The following checklist is derived mechanically from the PPT Agent's `.ncn` —
every row is answerable by reading the document, before any LLM runs.

**Plan:** `ppt_generation.ncds`
**Review date:** [to be completed]
**Reviewed by:** [to be completed]

| # | Question | Answer (from `.ncn`) | Status |
|---|----------|---------------------|--------|
| 1 | What external inputs does this plan require? | `topic` (string), `style_guide` (config) | ☐ Confirm |
| 2 | What does the slide content generator receive? | `outline_section` (single section) and `style_guide` | ☐ Confirm |
| 3 | Can the slide generator access the full outline? | No — `outline` is not in its declared scope | ☐ Confirm |
| 4 | Can one slide's content affect another slide? | No — each iteration is scoped to its own inputs | ☐ Confirm |
| 5 | What grounded tools does this plan call? | `slide_generator`, `section_extractor`, `html_renderer` | ☐ Confirm |
| 6 | Is there any accumulated state between slides? | Only `current_slide` (loop index) — declared as `<*` | ☐ Confirm |
| 7 | What does the final assembly step receive? | The `slides` collection and `topic` | ☐ Confirm |
| 8 | Can the assembly step access individual slide prompts? | No — only the completed slide outputs | ☐ Confirm |
| 9 | Are there any LLM calls before the Review step? | No — the `.ncn` is produced at compile time | ☐ Confirm |
| 10 | Is the plan structure consistent with the intended workflow? | [Reviewer judgment] | ☐ Approve / ☐ Reject |

This checklist is generated before execution. A rejection at row 10 means
the designer modifies the `.ncds` and recompiles — producing a new `.ncn`
for re-review. No LLM has been called; no agent has run; no cost has been
incurred for an incorrect plan.

---

## D.6 Comparison: `.ncn` vs. Other Verification Approaches

| Approach | When available | Who can read it | Requires syntax knowledge | Information complete? |
|----------|---------------|-----------------|--------------------------|----------------------|
| NormCode `.ncn` | Before execution (Phase 2) | Anyone | No | Yes (no information lost) |
| LangSmith trace | After execution | Developers | Yes (prompt strings) | Yes (post-hoc) |
| LangGraph graph visualization | At design time | Developers | Yes (Python) | Partial (data flow implicit) |
| PromptFlow YAML | At design time | Developers | Yes (YAML) | Partial (prompt templates implicit) |
| System prompt review | At design time | Developers | No (English) | No (execution logic implicit) |
| LLM explanation of workflow | Any time | Anyone | No | No (generated, may hallucinate) |

The `.ncn` is the only approach that is simultaneously:
- Available before any execution
- Readable by non-programmers
- Complete (identical in information content to the formal plan)
- Compiler-verified (not generated by a second LLM, not hand-written)
