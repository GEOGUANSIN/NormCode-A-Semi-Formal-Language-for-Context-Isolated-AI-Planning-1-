# 3D Model Report Generation

**An academic report generator that demonstrates NormCode's canonical loop → group → integrate pattern.**

**Location**: `direct_infra_experiment/3D_model_report_generation/`
**Status**: Production
**Category**: Research document generation

---

## Overview

This plan generates a structured academic-style report on "3D Urban Scene Generation." It is the clearest demonstration of NormCode's aggregation pattern: extract a list, loop to produce content for each item, group the results, and integrate into a final output.

---

## The Plan (`.ncds`)

```
:<:{final report}
    <= integrate all sections into cohesive report with abstract, conclusion, and references
    /: Combine all sections, review for consistency, flow, and completeness
    /: only use {report topic}, {outline}, and {all section drafts collection}
    
    /: ============================================================
    /: GROUND CONCEPT - The main report topic
    /: ============================================================
    <- {report topic}
        /: Ground value: "3D Urban Scene Generation"
    
    /: ============================================================
    /: PHASE 1 - Outline & Topic Identification
    /: ============================================================
    <- {outline}
        <= create structured outline with main sections and subsections
        /: Define scope and depth for each section
        <- {topic areas}
            <= brainstorm and identify key areas to cover
            /: Areas to explore:
            /: 1. Introduction & Background
            /: 2. Problem Definition & Challenges
            /: 3. Data Sources & Representations (point clouds, meshes, voxels, implicit)
            /: 4. Traditional Methods (procedural generation, rule-based systems)
            /: 5. Deep Learning Approaches (GANs, VAEs, diffusion models, transformers)
            /: 6. Neural Radiance Fields (NeRF) and Gaussian Splatting
            /: 7. Text-to-3D and Image-to-3D urban generation
            /: 8. Datasets & Benchmarks
            /: 9. Evaluation Metrics
            /: 10. Applications (autonomous driving, urban planning, gaming, AR/VR)
            /: 11. Current Limitations & Open Challenges
            /: 12. Future Directions
            <- {report topic}
    
    /: ============================================================
    /: PHASE 2 - Section Writing (iteration over sections)
    /: ============================================================

    <- [sections]
        <= extract sections list from outline
        <- {outline}

    <- [all section drafts]
        <= for each section in outline
            <= return section draft for this iteration
            <- {section draft}
                <= research and write this section with citations, figures, and technical details
                /: Maintain consistent academic tone and formatting
                /: Focus on recent advances (2020-2026)
                /: Balance between breadth (survey-style) and depth (technical details)
                <- {current section}
        <- [sections]
        <* {current section}

    <- {all section drafts collection}
        <= collect all section drafts
        <- [all section drafts]
```

---

## How It Works

### The Loop → Group → Integrate Pattern

This plan is the textbook example of NormCode's aggregation pattern:

```
{report topic}
      │
      ▼
[brainstorm] ──▶ {topic areas}
      │
      ▼
[create outline] ──▶ {outline}
      │
      ▼
[extract sections] ──▶ [sections]          ← List extraction
      │
      ▼
[loop: write section] ──▶ [all section drafts]   ← Per-item generation
      │
      ▼
[collect] ──▶ {all section drafts collection}     ← Grouping (syntactic, free)
      │
      ▼
[integrate report] ──▶ {final report}             ← Final synthesis (LLM)
```

Each step receives only what it needs:
- **Brainstorm** gets only `{report topic}`
- **Create outline** gets `{report topic}` + `{topic areas}`
- **Write section** gets only `{current section}` — not other sections' drafts
- **Integrate** gets `{report topic}` + `{outline}` + `{all section drafts collection}`

### Data Isolation in Practice

The section-writing loop is where data isolation matters most. Each section draft is generated with only:
- The current section specification from the outline
- No other section's draft text
- No raw brainstorming data

This prevents cross-contamination — section 5 won't accidentally reference content meant for section 3, and the model isn't overwhelmed by the full context of all previous sections.

---

## Inference Breakdown

| Step | Type | Input | Output |
|------|------|-------|--------|
| Brainstorm | LLM (imperative) | `{report topic}` | `{topic areas}` |
| Create outline | LLM (imperative) | `{report topic}`, `{topic areas}` | `{outline}` |
| Extract sections | LLM (imperative) | `{outline}` | `[sections]` |
| Write section | LLM (imperative, looped) | `{current section}` | `{section draft}` → `[all section drafts]` |
| Collect drafts | Syntactic (grouping) | `[all section drafts]` | `{all section drafts collection}` |
| Integrate report | LLM (imperative) | `{report topic}`, `{outline}`, `{all section drafts collection}` | `{final report}` |

### Cost Analysis

- **LLM calls**: 3 fixed + N per section (where N = number of sections, ~12) + 1 integration = ~16 total
- **Syntactic operations**: 1 grouping (free)
- **Parallel potential**: Section drafts could theoretically run in parallel (independent inputs)

---

## Key Design Patterns

| Pattern | How It's Used |
|---------|--------------|
| **Loop → Group → Integrate** | Extract list, generate per item, combine into one |
| **Data isolation** | Each section only sees its own specification |
| **Progressive refinement** | Topic → areas → outline → sections → drafts → report |
| **Grouping** | `{all section drafts collection}` packs the loop output into a single object |

---

## See Also

- **[README](README.md)** — Overview of all built-in plans
- **[Execution Section](../3_execution/README.md)** — How the orchestrator runs loops
- **[Grammar Section](../2_grammar/README.md)** — Loop and grouping syntax

---

**Last Updated**: March 2026
