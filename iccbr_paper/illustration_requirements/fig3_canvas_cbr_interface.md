# Fig 3 — Canvas App: The CBR Interface

**ID:** fig3  
**Output:** `figures/fig3_canvas_cbr_interface.png` (optionally fig3a + fig3b for two-panel)  
**Section:** §6  
**Creation method:** Screenshot from real Canvas App v1.1.3 + annotation overlays (callout boxes + arrows)  
**Needs multi-model LLM:** **Partial** — overlay design only (callout positions, arrows, label text). Screenshot = human capture.

---

## Purpose

Show the deployed system and map every visible UI element to a CBR operation. Evidence that the CBR cycle is operational.

## Screenshot requirements (human capture)

- **Source:** Actual NormCode Canvas App v1.1.3 (not mockups).
- **State:** Breakpoint-paused during a **Code Assistant** run.
- **Resolution:** 1920×1080 minimum.
- **Sanitization:** No API keys, personal file paths, or sensitive output visible. Consistent model name (e.g. `qwen-plus`).

### Required elements visible in frame

- **Graph center:** ≥8 nodes; mix of purple/blue/gray; completed nodes green; one paused node with breakpoint badge and flow index (e.g. `1.3.2`).
- **Right panel:** Tensor Inspector open; ≥3 rows of data visible; axis label visible.
- **Top controls:** Fork button and Value Override option visible.
- **Sidebar or panel:** Previous run history / checkpoint list visible (even as dropdown).

## Callout annotations (6) — for overlay layer (LLM can generate overlay layout/text)

1. → SQLite icon or checkpoint panel: **"Case Base — SQLite store of all completed node tensors across all runs"**
2. → Paused node + Tensor Inspector: **"Retrieve — locate suspended runtime by (run_id, flow_index); inspect bounded inputs"** *(C1: O(1) operations)*
3. → Value override or pencil near paused node: **"Revise — override tensor; scope rule determines exact stale boundary"** *(C3: scope-bounded re-run)*
4. → Fork button: **"Reuse — reinstantiate suspended runtime as new execution; no upstream re-run"**
5. → Green completed nodes + checkpoint icons: **"Retain — every completed node writes a case automatically"**
6. → `.ncn` review badge or file tab (if visible): **"C2 — plain-English plan narrative available before any LLM call"**

## Optional: two-panel figure

- Panel A: above (breakpoint + Tensor Inspector).
- Panel B: second screenshot — Run History / checkpoint list **or** .ncn Review Panel (C2).

## Caption

**Fig. 3.** NormCode Canvas (v1.1.3) as a CBR interface. Every UI element maps to a CBR operation: the checkpoint store (SQLite) is the case base; the Tensor Inspector realizes Retrieve by exposing the exact bounded inputs of any node in O(1) operations (C1); Value Override realizes Revise with automatic stale-boundary computation (C3); Fork realizes Reuse by reinstantiating a suspended runtime without upstream re-execution; automatic checkpointing realizes Retain. The `.ncn` pre-execution narrative (not shown) provides zero-cost human review before any LLM call (C2).

## LNCS

Full column width; total figure + caption target ≤ 6 cm height; min font 8pt in overlays.
