# Fig 2 — NormCode Syntax: Scope Rule and Case Isolation

**ID:** fig2  
**Output:** `figures/fig2_scope_rule_isolation.pdf`  
**Section:** §3  
**Creation method:** Adapted from website visual + constructed isolation diagram  
**Needs multi-model LLM:** **Yes** — adapt website layout to paper example + generate isolation diagram.

---

## Purpose

Show how the three markers plus indentation (scope rule) produce isolated tensors (enabling condition for Level 1 case integrity).

## Size

Full column width; ~1/3 page.

## Visual source: website `sections/language.html`

The website already has a production-quality annotated-code visual with the exact layout we need. Reuse its visual language:

- **Source file:** `new_website/sections/language.html`
- **CSS:** `new_website/css/components/tutorial.css` (3-column grid layout, annotation cards with connector lines/dots) + `new_website/css/components/code.css` (code editor with macOS title bar, syntax highlighting, flow-index line numbers)
- **Translations:** `new_website/lang/language-section.js` (EN + ZH text for all annotations)

### What to reuse from the website

| Element | Website | Fig 2 adaptation |
|---------|---------|-------------------|
| **Layout** | 3-column grid: left annotations / code editor / right annotations | Same layout; right column becomes isolation diagram instead of "read direction" note |
| **Code editor** | Dark background, macOS dots, `.ncds` filename, syntax-highlighted markers, flow-index line numbers | Same style; swap content to paper §3 example (summary/report/source_doc) |
| **Left annotations** | 3 cards: `<-` (data), `<=` (action), `<*` (loop) with symbol badge, label, hint text, color-coded border + connector line | Same 3 cards; use **English** text from `language-section.js`: "This is content" / "This is an action" / "Loop / timing state" |
| **Right annotations** | "Indentation = scope" card + "Inside-out, top-down" card with SVG icons | Keep "Indentation = scope" card; replace "read direction" card with isolation diagram |
| **Connector lines** | CSS `::after` pseudo-elements from note edge to code edge, colored dots by type | Same connector style (can be drawn as thin lines in the static figure) |
| **Color coding** | `--code-variable` (blue) for `<-`, `--code-function` (yellow-green) for `<=`, `--code-string` (warm) for `<*`, `--accent` for scope | Same color convention |

### What to change for fig2

1. **Code content** — replace batch-summarization example with the paper's §3 example:

```
<- summary                          1
    <= summarize the findings        1.1
    <- report                        1.2
        <= read the uploaded file    1.2.1
        <- source_doc               1.2.2
    <- style_guide                   1.3
```

2. **Right side** — replace "Inside-out, top-down" annotation with the **isolation boundary diagram** (see below).

3. **Static export** — the website version is interactive (JS hover effects); for the paper, export as a static image/PDF. Can be done by:
   - Screenshot of a standalone HTML page using the same CSS (recommended for draft)
   - Recreate in TikZ/Figma for camera-ready (using the website as pixel-reference)

## Grammar (match paper §3 and docs)

- **Three markers only:** `<-` (Value Concept — data), `<=` (Functional Concept — operation), `<*` (Context Concept — in-loop state). Use **ASCII** `<-` and `<=`.
- **Scope rule:** Indentation defines scope. The inputs available to any inference are exactly the concepts declared in its immediately enclosing indented block.
- **Flow indices (sibling pattern):** `summary` → 1, `summarize the findings` → 1.1, `report` → 1.2, `read the uploaded file` → 1.2.1, `source_doc` → 1.2.2, `style_guide` → 1.3.
- The paper's §3 example does **not** use `::` or syntactic operators in this snippet; keep it clean.

## Left annotations (from website, English)

- `<-` card: **"This is content"** — "Data, documents, results — the nouns flowing through the workflow." Color: blue (`--code-variable`).
- `<=` card: **"This is an action"** — "Operations the AI performs — extract, check, generate." Color: yellow-green (`--code-function`).
- `<*` card: **"Loop / timing state"** — "Repeat, wait, branch on conditions." Color: warm (`--code-string`). Note: `<*` is not used in this snippet but is shown as the third marker.

## Right side — "Indentation = scope" card + isolation boundary diagram

### "Indentation = scope" card (from website)

Keep the website's annotation card:
- Label: **"Indentation = scope"**
- Hint: "Each step sees only the data indented beneath it. No global context. No data leaking between steps."
- Connector line pointing to the indentation block under `<- report`.

### Isolation boundary diagram (new, below the scope card)

Show the runtime dependency implied by the scope rule:

- **Inference 1 (report):** `[source_doc ✓]` → `[report ✓]`. Tensor box: "Tensor for report contains only source_doc".
- **Inference 2 (summary):** `[report ✓]` + `[style_guide ✓]` → `[summary]`. Tensor box: "Tensor for summary contains only report + style_guide".

Text below: "Each completed node's tensor = self-contained case object".  
Highlight box (amber): "No hidden data in execution — if a step needs data not in its scope, the plan must be revised to declare it explicitly."

## Caption

**Fig. 2.** NormCode's scope rule as the enabling condition for Level 1 case integrity. Left: Three markers (`<-`, `<=`, `<*`) and indentation constitute the syntax; the scope block under each concept declaration specifies exactly which concepts that step receives. Right: The resulting runtime structure — the orchestrator constructs each step's input from only its declared references, so no hidden data enters execution. If a step needs data not in its scope, the plan must be revised to declare it explicitly. This structural isolation makes every checkpoint a self-contained, retrievable case.

## Color convention

Reuse website colors: blue for `<-` concepts, yellow-green for `<=` actions, warm for `<*` loop, accent for scope indicators. Amber for highlight box. Green checkmarks for completed nodes in the isolation diagram.

## Implementation options

1. **Draft (fast):** Create a standalone HTML page that includes the website's CSS + a modified `language.html` with the paper's example. Screenshot at high resolution. Add isolation diagram as a separate SVG overlay or second panel.
2. **Camera-ready:** Recreate in TikZ or Figma using the website screenshot as pixel reference. This gives vector output matching LNCS typography.
3. **Hybrid:** Use the website's HTML/CSS for the left+center (code + annotations), export as high-res PNG; combine with a TikZ isolation diagram on the right.
