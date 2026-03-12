# Supp. Figure D — NormCode ecosystem / pipeline (authoring → execution)

**ID:** suppD  
**Output:** `figures/suppD_ecosystem_pipeline.pdf`  
**Section:** §1 or §3 (supplementary if figure budget full)  
**Creation method:** Constructed diagram  
**Needs multi-model LLM:** **Yes** — pipeline or positioning diagram from description.

---

## Purpose

One-view clarity on where NormCode sits: full path from authoring to execution and case base (or contrast vs. typical LLM stacks).

## Content (choose one focus)

### Option A — Full pipeline (authoring → execution)

- Flow: `.ncds` authoring → **Derivation → Formalization → Post-Formalization → Activation** → Orchestrator + Canvas → SQLite (case base).
- Optional annotations: “.ncn review” after Formalization; “Level 2 case” = compiled plan; “Level 1 cases” = checkpoints.

### Option B — Ecosystem positioning

- Contrast two boxes:
  - **Typical LLM stack:** “Conversation history / shared state, implicit context”
  - **NormCode:** “Scope-verified, checkpoint = self-contained case”
- Optional: arrow or label “structural isolation” as differentiator.

## Style

Clean arrows; minimal text; project colors. Size: can be small (~1/4 page) if in main body.

## LLM use

Description above → single diagram (TikZ/Figma/SVG). Specify “pipeline” or “positioning” depending on option.
