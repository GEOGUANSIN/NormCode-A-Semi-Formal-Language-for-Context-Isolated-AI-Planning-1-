# Illustration requirements — ICCBR 2026 paper

Individual requirement specs for each figure and artifact. Use this index to see **which items need multi-model LLM** (or other) generation.

## Index: creation method and LLM use

| ID | Title | Creation method | **Needs multi-model LLM?** | LLM use case |
|----|--------|------------------|----------------------------|--------------|
| [fig1](fig1_two_level_cbr.md) | Two-Level CBR Architecture | Constructed (TikZ or Figma → PDF) | **Yes** | Diagram generation: text spec → TikZ/Figma/SVG (layout, arrows, labels) |
| [fig2](fig2_scope_rule_isolation.md) | NormCode Syntax: Scope Rule and Case Isolation | Constructed (annotated code block + diagram) | **Yes** | (1) Annotated code figure from spec; (2) Isolation-boundary diagram from spec |
| [fig3](fig3_canvas_cbr_interface.md) | Canvas App: CBR Interface | Screenshot + annotation overlays | **Partial** | Overlay design only: callout positions, arrows, labels; screenshot = human capture |
| [fig4](fig4_retrieve_revise_cycle.md) | Case Study: Retrieve–Revise Cycle | Constructed (preferred) or screenshots | **Yes** (if constructed) | Three-panel diagram from spec; if screenshots, same as fig3 (partial) |
| [suppA](suppA_six_properties.md) | Six-Property Table (visual) | Constructed (2×3 grid of cards) | **Yes** | Grid/card layout from table spec (TikZ/HTML/Figma) |
| [suppB](suppB_compilation_pipeline.md) | Compilation Pipeline as Level 2 Distillation | Constructed diagram | **Yes** | Pipeline diagram from description |
| [suppC](suppC_production_plans.md) | Six Production Plans (scale evidence) | Table or table-based visual | **Optional** | Data is manual; visual/chart version could be LLM-generated |
| [suppD](suppD_ecosystem_pipeline.md) | NormCode ecosystem / pipeline | Constructed diagram | **Yes** | Pipeline or positioning diagram from description |
| [listings](req_listings_code_artifacts.md) | NormCode listings & code artifacts | LaTeX (lstset, captioned listings) | **Yes** | Generate `lstdefinestyle` / snippet wrappers / artifact headers from requirements |

## Filtering by “multi-model LLM”

- **Use for LLM generation (diagram/code/layout):** fig1, fig2, fig4 (constructed), suppA, suppB, suppC (optional), suppD, listings.
- **Screenshot-first (LLM only for overlays):** fig3, fig4 (if screenshot option).
- **Human-only capture:** All Canvas screenshots must be from real Canvas App v1.1.3.

## Color convention (apply to all constructed figures)

- Semantic nodes: `#c084fc` stroke, `#faf5ff` fill, hexagon
- Concept nodes: `#60a5fa` stroke, `#eff6ff` fill, rounded rect
- Syntactic nodes: `#94a3b8` stroke, `#f8fafc` fill, rounded rect
- Completed: `#22c55e`; Running: `#3b82f6`; Pending: `#9ca3af`; Failed: `#ef4444`
- Output node: `#ef4444` outer ring; Case base / Level 2: `#f59e0b` amber
- Background: white, subtle dot grid

## Output paths (see main plan)

- Main: `iccbr_paper/figures/fig1_two_level_cbr.pdf`, etc.
- Supp: `figures/suppA_six_properties.pdf`, etc.
