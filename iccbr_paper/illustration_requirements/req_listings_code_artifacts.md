# Listings & code artifacts (LaTeX)

**ID:** listings  
**Output:** Changes in `main.tex` and section files (no separate figure file)  
**Section:** §3, §5, §7, appendix  
**Creation method:** LaTeX — `lstset` / `lstdefinestyle`, captioned listings, optional artifact headers  
**Needs multi-model LLM:** **Yes** — generate `lstdefinestyle` / snippet wrappers / artifact headers from requirements.

---

## Purpose

Unified, citable NormCode snippet style across the paper; 1–2 key snippets as formal Listings; optional “artifact” look (filename bar).

## Requirements

1. **Unified listing style**
   - One style for all NormCode (`.ncds` and `.ncn`): same `basicstyle`, `backgroundcolor`, `frame`, `breaklines`, etc.
   - Apply to every `lstlisting` that contains NormCode in §3, §5, §7, appendix.
   - Option: thin “artifact bar” or title showing filename (e.g. `plan.ncds`, `output.ncn`).

2. **Captioned listings**
   - At least the **minimal scope-rule example** in §3: use `\begin{lstlisting}[caption={...}, label=lst:scope-rule}]` so it appears as “Listing 1” and can be cited.
   - Optionally one **.ncn excerpt**: same treatment as “Listing 2”.
   - Do not duplicate Fig. 2 content; keep wording/symbols consistent so Fig. 2 and Listing 1 reinforce each other.

3. **Optional artifact strip**
   - For the main .ncds example, add a one-line header inside or above the block, e.g. `┌─ plan.ncds ─────────────────────┐` or a listings “title”/comment so it reads as a real artifact.

## Existing usage (for consistency)

- `main.tex`: `\lstset{ basicstyle=\ttfamily\small, breaklines=true, frame=single, backgroundcolor=\color{gray!8}, rulecolor=\color{gray!40}, ... }`
- §3: two-concept example; iteration example; .ncn snippet.
- §5: compilation plan .ncds sketch.
- §7: plan fragments.
- Appendix: Base-X addition plan with caption.

## LLM use

- Input: this requirement + “generate LaTeX lstdefinestyle and example of captioned listing for NormCode.”
- Output: drop-in `\lstdefinestyle{normcode}{...}`, and example `\begin{lstlisting}[style=normcode, caption=..., label=lst:...]` for §3 minimal example.

## File naming

No new figure files; output is edits to `latex_template/main.tex` and relevant `sections/*.tex`.
