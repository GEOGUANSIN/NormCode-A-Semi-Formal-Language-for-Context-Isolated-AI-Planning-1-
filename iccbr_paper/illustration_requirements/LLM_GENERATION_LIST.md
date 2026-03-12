# Requirements that need multi-model LLM generation

Use this list to feed specs into your LLM pipeline. Each file is self-contained.

---

## Full LLM generation (diagram / layout / code from spec)

| Requirement | File | LLM task |
|-------------|------|----------|
| **Fig 1** — Two-Level CBR Architecture | [fig1_two_level_cbr.md](fig1_two_level_cbr.md) | Text spec → TikZ / Figma / SVG diagram (three bands, arrows, labels) |
| **Fig 2** — Scope Rule and Case Isolation | [fig2_scope_rule_isolation.md](fig2_scope_rule_isolation.md) | (1) Annotated code block figure; (2) Isolation-boundary diagram |
| **Fig 4** — Retrieve–Revise Cycle (constructed) | [fig4_retrieve_revise_cycle.md](fig4_retrieve_revise_cycle.md) | Three-panel diagram from spec | (!!!Fig 4 is not needed)
| **Supp A** — Six-Property Table | [suppA_six_properties.md](suppA_six_properties.md) | Table spec → 2×3 card grid (TikZ/HTML/Figma) |
| **Supp B** — Compilation Pipeline | [suppB_compilation_pipeline.md](suppB_compilation_pipeline.md) | Pipeline description → diagram | (!!!Supp B  is not needed)
| **Supp D** — Ecosystem / pipeline | [suppD_ecosystem_pipeline.md](suppD_ecosystem_pipeline.md) | Pipeline or positioning description → diagram | (!!!Supp D  is not needed)
| **Listings** — Code artifacts | [req_listings_code_artifacts.md](req_listings_code_artifacts.md) | Requirements → `lstdefinestyle` + captioned listing example (LaTeX) |

---

## Partial LLM (overlay design only; capture is human)

| Requirement | File | LLM task | Human task |
|-------------|------|----------|------------|
| **Fig 3** — Canvas CBR Interface | [fig3_canvas_cbr_interface.md](fig3_canvas_cbr_interface.md) | Generate overlay layer: callout positions, arrows, 6 labels | Capture screenshot from Canvas App v1.1.3 |
| **Fig 4** — (if screenshot option) | [fig4_retrieve_revise_cycle.md](fig4_retrieve_revise_cycle.md) | Overlay design for two screenshots | Capture two Canvas states |

---

## Optional LLM (data is manual; visual is optional)

| Requirement | File | LLM task |
|-------------|------|----------|
| **Supp C** — Production plans | [suppC_production_plans.md](suppC_production_plans.md) | Table data → chart/graphic (optional); otherwise use as LaTeX table only |

---

## No LLM (human / tool only)

- **Screenshots:** All Canvas captures must be from real app; no synthetic screenshots.
- **Final TikZ/PDF:** You can use LLM output as draft, then hand-edit for camera-ready.
