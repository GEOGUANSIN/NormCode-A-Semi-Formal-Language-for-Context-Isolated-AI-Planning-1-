# Supp. Figure B — Compilation Pipeline as Level 2 Distillation

**ID:** suppB  
**Output:** `figures/suppB_compilation_pipeline.pdf`  
**Section:** Optional / supplementary  
**Creation method:** Constructed diagram  
**Needs multi-model LLM:** **Yes** — pipeline diagram from description.

---

## Purpose

Show the four-phase compilation pipeline as the Level 2 distillation process, with inputs, outputs, and review points.

## Content to show

- **Pipeline:** Derivation → Formalization → Post-Formalization → Activation (horizontal, left to right).
- **Input:** Natural language task description (at start).
- **Output:** Compiled runtime definition (Level 2 case) (at end).
- **Per phase:** What structure is extracted (short label per phase).
- **Review point:** Where human verification occurs — `.ncn` after Phase 2 (Formalization).
- **Annotation:** "This pipeline is itself a NormCode plan" (self-hosting).

## Style

Arrows between phases; optional boxes for input/output; highlight or callout for “.ncn review”. Use project color convention; amber for Level 2 / abstract case if needed.

## LLM use

Text description → pipeline diagram (TikZ/Figma/SVG) with phases, labels, and annotation.
