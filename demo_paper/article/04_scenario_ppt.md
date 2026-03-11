# 4. Demo Scenario A: PPT Agent — The Full Lifecycle

The PPT Agent is a production NormCode plan that takes a topic as input and
produces a fully rendered presentation — structured outline, slide-by-slide
content, HTML preview, and `.pptx` export. The plan contains approximately 30
inferences organized around a nested loop: for each section in the outline,
generate slide content using the section text and a shared style guide. It
supports six slide layouts and fourteen component types. This scenario walks
every step of the lifecycle.

## Step 1 — Describe: Write the Plan

The plan is authored in `.ncds` — natural language with minimal structural
markers. A fragment of the slide generation loop reads:

```
<- presentation
    <= :: assemble final presentation
    <- slides
        <* current_slide
        <= :: generate slide content
        <- outline_section
            <= :: extract section for current slide
            <- outline
                <= :: generate presentation outline
                <- topic
        <- style_guide
    <- topic
```

The three symbols, indentation, and natural-language action descriptions are the
complete authoring interface. No type annotations, no paradigm IDs, no resource
paths — those are added by the compiler. A domain expert with no programming
background can read this and understand what the agent will do.

## Step 2 — Compile and Review: The `.ncn` Verification Layer

After compilation, the orchestrator has `concept_repo.json` and
`inference_repo.json`. Alongside these, the compiler produces a `.ncn`
(NormCode Natural) file — a plain-English narrative of the same plan. The `.ncn`
translation of the slide generation fragment reads:

```
(OUTPUT) slides
  (ACTION) is obtained by, for each current_slide in the collection,
           generating slide content
  (INPUT)  using outline_section
             (OUTPUT) outline_section
               (ACTION) is obtained by extracting the section
                        for the current slide
               (INPUT)  using outline
                          (OUTPUT) outline
                            (ACTION) is obtained by generating
                                     a presentation outline
                            (INPUT)  using topic
  (INPUT)  and style_guide
```

A manager, compliance officer, or domain expert reads this before execution.
No LLM has run yet. No output has been produced. This is the plan's logic, stated
plainly, awaiting approval. If the expert disagrees with a step — say, the outline
should also use a reference document — they can ask the designer to add it before
the run begins. This is the **Review** stage: human-in-the-loop before any
probabilistic operation is triggered.

> **[FIGURE 2 LEFT HERE — `.ncds` fragment and `.ncn` translation side by side,
> with "Compiler — no information lost" bridging arrow]**

## Step 3 — Run: Canvas Execution

The operator opens the plan in Canvas and clicks Run. The inference graph unfolds:

- The **outline generation** node (purple hexagon) completes first — green
  indicator, output stored.
- The **loop** begins: `current_slide` iterates through outline sections. Each
  iteration launches the `outline_section` extraction (syntactic, gray — instant,
  free) followed by `generate slide content` (semantic, purple — LLM call).
- Completed slides accumulate green; the active slide pulses blue. Syntactic
  routing nodes (the collection grouping, the loop state management) flicker gray
  and complete instantly, never visible in the tool call log because they invoke
  no LLM.
- The `assemble final presentation` node (semantic) fires once all slides are
  ready, combining them using a paradigm that calls a Python renderer.

The tool call monitor in the left panel shows every LLM prompt as it fires — the
outline generation prompt, each slide content prompt — with the full response
inline. Every call is associated with a flow index, so a failed call maps
immediately to a specific node in the graph.

> **[FIGURE 2 RIGHT HERE — Canvas execution graph mid-run: completed slides
> green, current slide blue pulsing, output node visible with red ring]**

## Step 4 — Output and Deploy

The final `presentation` node completes (green, red output ring). The Canvas
right panel shows the tensor at this node: a single value on a `[file]` axis —
a perceptual sign pointing to the rendered `.pptx` path. The HTML preview opens
in a browser tab alongside it.

The plan file — `ppt_generation.ncds` — is unchanged from Step 1. It can be
committed to Git, shared with a colleague, modified to add a new slide type, or
handed to a different orchestrator. **The workflow belongs to its author.**

## What This Scenario Demonstrates

| Claim | Evidence in this scenario |
|-------|--------------------------|
| Non-programmers can author plans | `.ncds` uses three symbols and natural-language descriptions |
| Human review before execution | `.ncn` plaintext narrative read and approved before Run |
| Data isolation by construction | Each slide generation sees only its `outline_section` — not the full outline, not prior slides' content |
| Semantic/syntactic separation visible | Syntactic routing nodes (gray, instant) vs. LLM calls (purple, logged) |
| Full audit trail | Every input/output stored; every LLM call in the tool monitor with flow index |
| Portable artifact | The `.ncds` file is the deliverable — not a platform state |
