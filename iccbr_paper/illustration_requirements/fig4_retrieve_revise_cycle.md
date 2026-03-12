# Fig 4 — Case Study: The Retrieve–Revise Cycle

**ID:** fig4  
**Output:** `figures/fig4_retrieve_revise_cycle.pdf` (preferred) or `.png` if screenshots  
**Section:** §7 (Code Assistant case study)  
**Creation method:** Constructed three-panel (preferred) **or** two screenshots with overlays  
**Needs multi-model LLM:** **Yes** if constructed (three-panel diagram from spec). **Partial** if screenshots (overlays only).

---

## Purpose

Show the complete CBR retrieve–revise cycle in the Code Assistant debugging scenario. Empirical evidence for C1 and C3.

## Size

Full column width; ~1/3–1/2 page.

---

## Option A: Three-panel constructed diagram (preferred — use for LLM diagram generation)

### Panel 1 — Retrieve

- Run history line: `run_042  [node 1.1 ✓][node 1.2 ✓][node 1.3 ✗]  ← FAILED`
- Breakpoint at 1.3; Tensor Inspector box with: `input: file_list`, `[a.py, b.py, c.py`, `wrong_dir/]`, label "↑ cause identified".
- Label above panel: **"Retrieve — locate run_042 checkpoint at node 1.3; inspect bounded inputs in 2 clicks (C1)"**

### Panel 2 — Revise

- Override line: `file_list ← [a.py, b.py, c.py]  (removed wrong_dir/)`
- Stale boundary: `[node 1.3] [node 1.4] [node 1.5]  ← re-execute`; `[node 1.1] [node 1.2]  ← preserved from cache (C3)`.
- Label above: **"Revise — override file_list; only 3 of 40 nodes re-run (C3)"**

### Panel 3 — Reuse + Retain

- Fork → run_043: `[node 1.1 ✓ cached][node 1.2 ✓ cached][node 1.3 ✓ new]` … `[node 1.4 ✓ new][node 1.5 ✓ new]`.
- New cases: `run_043 / node 1.3  ← revised file_list`; same for 1.4, 1.5.
- Label above: **"Reuse (Fork) + Retain — corrected run produces new cases; upstream cached"**

Below all three: horizontal arrow label — *"Total: 1 breakpoint + 2 clicks to identify cause (C1); 3 of 40 inferences re-executed (C3)"*.

## Option B: Screenshots (if using real captures)

- Left: Breakpoint inspection — Tensor Inspector showing wrong file path.
- Right: Post-fork — upstream nodes green-cached, downstream green-new.
- Overlays: same CBR labels as needed. **LLM:** overlay design only.

## Caption

**Fig. 4.** The retrieve–revise cycle in the Code Assistant case study (§7.2). *Retrieve*: a failed run (run_042) is located at the node where file discovery failed; the Tensor Inspector shows the exact bounded inputs in two clicks — no log reconstruction (C1). *Revise*: the incorrect file path is overridden; the scope rule computes the exact stale boundary (3 nodes downstream). *Reuse (Fork) + Retain*: a new run (run_043) preserves the 37 upstream nodes from cache, re-executes only the 3 stale nodes, and deposits new cases in the case base. Total re-execution: 7.5% of the plan.

## Color convention

Green = completed/cached; blue = running; red = failed. Use project palette.
