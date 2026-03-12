# Supp. Figure A — The Six-Property Table (visual)

**ID:** suppA  
**Output:** `figures/suppA_six_properties.pdf`  
**Section:** Optional / supplementary  
**Creation method:** Constructed — 2×3 grid of property cards  
**Needs multi-model LLM:** **Yes** — generate grid/card layout from table spec (TikZ/HTML/Figma).

---

## Purpose

Six properties of a reasoning medium as a visual (not prose): each card has property name, NormCode realization, failure mode without it.

## Layout

2×3 grid of cards. Each card contains:

- Property name (bold)
- One-line implementation in NormCode
- One-line failure mode in tools without this property

## Data (exact content)

| Card | Property | NormCode realization | Failure without it |
|------|----------|----------------------|---------------------|
| 1 | Interpretable | `.ncn` plain-prose output | Plans locked in code |
| 2 | Enforceable | Compiler verifies scope; orchestrator enforces | Review ≠ what runs |
| 3 | Composable | 3 symbols × 1 scope rule; unlimited depth | Breaks at scale |
| 4 | Locally Addressable | Flow indices + scope = per-step isolation | O(k) debugging |
| 5 | Generalizable | Same primitives: PPT, code, BOM, medical | Domain-specific DSLs |
| 6 | Portable | Plain text `.ncds`; any compliant orchestrator | Platform lock-in |

## Style

Cards: readable font; clear separation; optional amber accent for “NormCode” column. Background: white; consistent with main figures.

## LLM use

Feed this table + “2×3 card grid, publication-ready” to generate TikZ, SVG, or Figma layout.
