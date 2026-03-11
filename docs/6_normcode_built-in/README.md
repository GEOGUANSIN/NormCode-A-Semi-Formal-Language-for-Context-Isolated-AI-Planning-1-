# NormCode Built-in Plans & Examples

**Real NormCode plans that ship with the ecosystem — from interactive assistants to meta-compilers to full production workflows.**

---

## Overview

NormCode includes several built-in plans that serve as both working tools and reference implementations. These plans demonstrate the full range of NormCode capabilities: chat loops, multi-phase pipelines, conditional branching, parallel execution, tool integration, and meta-compilation.

Each plan page includes the **full `.ncds` source** (or `.ncd` where applicable), a phase-by-phase walkthrough, paradigm mappings, and key design pattern explanations.

---

## Plans

| Plan | Category | Purpose | Location |
|------|----------|---------|----------|
| **[Canvas Assistant](canvas_assistant.md)** | Interactive | Chat controller for the Canvas UI | `canvas_app/built_in_projects/canvas_assistant/` |
| **[Code Assistant](code_assistant.md)** | Interactive | Software engineering agent | `canvas_app/built_in_projects/code_assistant/` |
| **[NC Compilations](nc_compilations.md)** | Meta | Compile natural language into NormCode plans | `direct_infra_experiment/nc_compilations/` |
| **[PPT Generation](ppt_generation.md)** | Production | Generate presentations from content | `direct_infra_experiment/tests/ppt生成_v2/` |
| **[3D Model Report](report_generation.md)** | Production | Generate academic-style research reports | `direct_infra_experiment/3D_model_report_generation/` |
| **[BOM Matching](bom_matching.md)** | Production | Match component BOMs against databases | `direct_infra_experiment/tests/normcode_bom/` |

---

## Canvas Assistant

**[Full documentation →](canvas_assistant.md)**

A NormCode plan that runs inside the Canvas App and controls it via natural language chat. Uses a self-seeding loop with context summarization, command classification, and execution via the Canvas Integration Tool (`me.hands`, `me.vision`, `me.mind`).

**Key patterns**: Self-seeding loop, context summarization, status notifications, termination judge

---

## Code Assistant

**[Full documentation →](code_assistant.md)**

A structured software engineering workflow: Receive → Triage → Explore → Plan → Approve → Implement → Verify → Report. Uses shell, search, git, editor, and memory faculties to perform coding tasks with full transparency on the canvas graph.

**Key patterns**: Tiered complexity, scoped LLM calls, lint-fix inner loops, parallel verification

---

## NC Compilations

**[Full documentation →](nc_compilations.md)**

The meta-compiler: a NormCode plan that compiles natural language task descriptions into new executable NormCode plans. Automates the full compilation pipeline through 7 phases — analysis, derivation (`.ncds`), formalization (`.ncd`), post-formalization (`.pf.ncd`), provision generation, activation (repositories), and ground initialization.

**Key patterns**: Meta-compilation, conditional branching, provision loop, LLM + script hybrid, assigning sequences

---

## PPT Generation

**[Full documentation →](ppt_generation.md)**

A component-based presentation generator with 6 layouts and 14 component types. Produces both HTML (for preview) and PPTX (for delivery). Multiple client interfaces (web wizard, CLI, desktop GUI) demonstrate the Clients concept from the ecosystem.

**Key patterns**: Per-slide loop with data isolation, component abstraction, multi-output, Mermaid diagram integration

---

## 3D Model Report Generation

**[Full documentation →](report_generation.md)**

An academic report generator that demonstrates the canonical **loop → group → integrate** pattern. Brainstorms topics, creates an outline, writes each section in a loop, groups the drafts, and integrates into a final report.

**Key patterns**: Loop → group → integrate, progressive refinement, data isolation per section

---

## BOM Matching

**[Full documentation →](bom_matching.md)**

A hybrid deterministic/LLM workflow for matching BOM rows against component databases. Exact database matches are free (syntactic); LLM selection only fires for ambiguous cases — demonstrating NormCode's semantic vs. syntactic cost optimization.

**Key patterns**: Deterministic + LLM hybrid, conditional branching, per-row loop, interactive review, on-demand scraper sub-workflow

---

## Patterns Across Plans

These plans collectively demonstrate NormCode's core capabilities:

| Capability | Canvas Asst. | Code Asst. | NC Compilations | PPT Gen | 3D Report | BOM |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| **Chat loop** | ✅ | ✅ | | | | |
| **Multi-phase pipeline** | | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Per-item loop** | | | ✅ | ✅ | ✅ | ✅ |
| **Conditional branching** | ✅ | ✅ | ✅ | | | ✅ |
| **LLM + script hybrid** | | ✅ | ✅ | ✅ | | ✅ |
| **Data isolation** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Canvas Integration** | ✅ | ✅ | | | | ✅ |
| **Code tools** | | ✅ | | | | |
| **Meta-compilation** | | | ✅ | | | |
| **Multiple clients** | | | | ✅ | | |
| **Semantic vs. syntactic optimization** | | | | | | ✅ |

---

## Relationship to Other Sections

| Section | Relationship |
|---------|--------------|
| **[1. Introduction](../1_intro/README.md)** | Built-in plans are practical examples of concepts introduced there |
| **[2. Grammar](../2_grammar/README.md)** | Each plan's `.ncds` and `.ncd` files demonstrate the syntax |
| **[3. Execution](../3_execution/README.md)** | Plans run on the Orchestrator documented there |
| **[4. Compilation](../4_compilation/README.md)** | NC Compilations automates the compilation pipeline |
| **[5. Tools](../5_tools/README.md)** | Canvas Assistant and Code Assistant use the faculties documented there |

---

## See Also

- **[Ecosystem Overview](../1_intro/ecosystem.md)** — The 6-product lifecycle these plans operate within
- **[Canvas App User Guide](../5_tools/canvas_app_user_guide.md)** — How to run these plans
- **[Canvas Integration Guide](../5_tools/canvas_integration_guide.md)** — The `me`/`you`/`it` system used by assistants

---

**Last Updated**: March 2026
