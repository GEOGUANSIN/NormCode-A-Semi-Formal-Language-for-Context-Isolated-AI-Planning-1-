# BOM Matching

**A hybrid deterministic/LLM workflow that matches bill-of-materials rows against component databases — demonstrating NormCode's semantic vs. syntactic cost optimization.**

**Location**: `direct_infra_experiment/tests/normcode_bom/`
**Status**: Production
**Category**: Data processing + LLM hybrid

---

## Overview

The BOM Matching plan (非正规BOM查找, "Non-standard BOM Lookup") accepts a user-supplied BOM spreadsheet, matches each component row against the AllChips component database, enriches rows with pricing and availability, and produces an interactive table for review and CSV export.

Its most important design property: **the plan only calls the LLM when deterministic matching fails**. Exact database matches are free syntactic operations; LLM-assisted selection only fires for ambiguous cases.

---

## The Plan (`.ncds`)

```
/: 智能BOM — Intelligent BOM Matching & Pricing Workflow
/:
/: Accepts a user-supplied BOM spreadsheet, matches each component row
/: against the AllChips component database using an exact-match shortcut
/: or LLM-assisted selection, enriches rows with pricing and availability,
/: and produces an interactive priced BOM table for review and CSV export.
/:
/: Ground inputs:
/:   {raw bom input}      — CSV / Excel / TXT file uploaded by user
/:   {component database} — AllChips SQLite database

<- {enriched bom report}
    <= export user-reviewed bom as downloadable csv file
    <- {user reviewed bom}
        <= present enriched rows in interactive table for user review
        /: User interactions:
        /:   - filter: all / matched / needs review / not found
        /:   - inline edit of row quantity
        /:   - detail drawer for component specs, pricing, datasheet
        /:   - expand row to view/select alternative candidates
        /:   - adjust board quantity multiplier
        /:   - trigger re-match or background scrape for missing components
        <- {total bom cost}
            <= sum all row price subtotals, then multiply by board quantity
            <- [enriched bom rows]
            <- {board quantity}
                <= accept number of boards from user input (default: 1)
        <- [enriched bom rows]
            <= for each parsed bom row, match against database and enrich

                <= return the enriched row for this iteration

                <- {enriched bom row}
                    <= merge selected candidate fields into row dict
                    /: Fields: 推荐型号 推荐品牌 推荐参数 库存 交期 MPQ MOQ
                    /:         售价(含税) 小计(含税) 总用量 _match_confidence
                    <- {parsed bom row}
                    <- {selected candidate}
                        <= select best matching component from candidates
                        <- <is single exact mpn match>
                            <= judge if candidates contain exactly one entry whose
                               mpn matches the row's requirement (case-insensitive)
                            <- [row candidates]
                            <- {parsed bom row}
                        <- [row candidates]
                            <= query component database by mpn, brand, and package
                            /: returns up to 5 ranked candidates
                            <- {parsed bom row}
                            <- {component database}
                        <- {llm match result}
                            <= prompt llm to select the best candidate index,
                               confidence score, match type, reasoning, and warnings
                            /: only invoked when <is single exact mpn match> is false
                            <- {formatted match prompt}
                                <= fill match prompt template with requirement
                                   and numbered candidate list
                                <- {parsed bom row}
                                <- [row candidates]

            <- [parsed bom rows]
            <* {parsed bom row} from [parsed bom rows]
            <- {component database}

        <- [parsed bom rows]
            <= parse raw bom input into normalized row dicts
            <- {file format metadata}
                <= detect encoding and infer delimiter
                <- {raw bom input}
            <- {header mapping}
                <= map detected column headers to standard names
                /: standard: 序号 位号 型号 品牌 封装 参数 数量
                <- {file format metadata}
                <- {raw bom input}
            <- {raw bom input}
                <= receive bom from user as file upload or pasted csv

        <- {component database}
            <= open allchips sqlite database


/: ─────────────────────────────────────────────────────────────────
/: OPTIONAL: Database Refresh via AllChips Scraper
/: Triggered on-demand when components are not found in database.
/: ─────────────────────────────────────────────────────────────────

<- {database refresh result}
    <= save newly scraped components into sqlite database
    <- [scraped components]
        <= for each unmatched mpn, scrape allchips for component data

            <= return scraped components for this mpn

            <- [mpn components]
                <= search allchips website using playwright browser automation
                /: extracts rows from tr[data-wareid] elements
                <- {current mpn}

        <- [unmatched mpn list]
        <* {current mpn} from [unmatched mpn list]
    <- [unmatched mpn list]
        <= accept list of mpns to scrape from user
```

---

## How It Works

### The Deterministic + LLM Hybrid

The core innovation of this plan is its cost-optimized matching strategy:

```
For each BOM row:
  query_database(row) ──▶ [row candidates]
                              │
  judge: exactly one exact MPN match?
                              │
              ┌───────────────┴───────────────┐
              │ yes (syntactic, free)          │ no (semantic, costs tokens)
              │                               │
         use the match directly          LLM selects best candidate
              │                               │
              └───────────────┬───────────────┘
                              │
                    {selected candidate}
                              │
                    enrich row with pricing
```

In a typical 100-row BOM:
- ~60-70% match exactly → **free** (syntactic)
- ~30-40% need LLM selection → costs tokens
- Total token cost is 30-40% of what a naive "LLM for every row" approach would cost

This is the **semantic vs. syntactic distinction** applied to real production data processing.

### Parsing Pipeline

Before matching begins, the plan parses the raw input through three deterministic steps:

1. **Detect format** — encoding (chardet) + delimiter (tab/semicolon/comma/pipe)
2. **Map headers** — map varied column names to standard Chinese names (型号, 品牌, 封装, etc.)
3. **Parse rows** — normalize into standardized row dicts

All three are syntactic operations — no LLM cost.

### Interactive Review

After matching and enrichment, the plan presents results in an interactive table via Canvas Integration:
- Filter by match status (all / matched / needs review / not found)
- Inline edit quantities
- Detail drawer for specifications and pricing
- Select alternative candidates
- Adjust board quantity multiplier

---

## Inference Breakdown

| Step | Type | LLM? | Cost |
|------|------|------|------|
| Receive BOM | User input | No | Free |
| Detect encoding/delimiter | Script (judgement) | No | Free |
| Map headers | Script | No | Free |
| Parse rows | Script | No | Free |
| Open database | Script | No | Free |
| Query candidates | Script (per row) | No | Free |
| Judge exact match | Script (per row) | No | Free |
| LLM select candidate | LLM (per ambiguous row) | **Yes** | Tokens |
| Enrich row | Script (per row) | No | Free |
| Calculate total cost | Script | No | Free |
| Interactive review | Canvas Integration | No | Free |
| Export CSV | Script | No | Free |

### Optional: Database Refresh

A separate sub-workflow scrapes AllChips via Playwright for components not found in the database. This runs on-demand — a background job triggered from the UI.

---

## Key Design Patterns

| Pattern | How It's Used |
|---------|--------------|
| **Semantic vs. syntactic** | Exact matches are free; LLM only fires for ambiguous cases |
| **Per-row loop** | Each BOM row matched independently with scoped inputs |
| **Conditional branching** | `<is single exact mpn match>` controls LLM invocation |
| **Interactive review** | Canvas Integration for user adjustment before export |
| **Progressive enrichment** | Parse → match → enrich → review → export |
| **On-demand sub-workflow** | Scraper runs separately when needed |

---

## Files

| File | Purpose |
|------|---------|
| `_.ncds` | Draft plan (shown above) |
| `_.pf.ncd` | Formal compiled plan |
| `_.pf.nci.json` | Inference index |
| `repos/concept_repo.json` | Executable concept repository |
| `provisions/prompts/match_component.md` | LLM match selection prompt |
| `provisions/scripts/parse_bom.py` | BOM parsing and normalization |
| `provisions/scripts/search_candidates.py` | Database candidate search |
| `provisions/scripts/check_exact_match.py` | Exact match judge |
| `provisions/scripts/enrich_bom_row.py` | Row enrichment |
| `provisions/scripts/calculate_total.py` | Cost calculation |
| `provisions/scripts/export_csv.py` | CSV export |
| `clients/frontend/` | Vue.js interactive review UI |
| `clients/backend/` | FastAPI backend for review |

---

## See Also

- **[README](README.md)** — Overview of all built-in plans
- **[Ecosystem Overview](../1_intro/ecosystem.md)** — Semantic vs. syntactic technical property
- **[Execution Section](../3_execution/README.md)** — How the orchestrator handles conditional execution

---

**Last Updated**: March 2026
