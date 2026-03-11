# NC Compilations

**A NormCode plan that compiles natural language task descriptions into new executable NormCode plans — the meta-compiler.**

**Location**: `direct_infra_experiment/nc_compilations/`
**Status**: Production
**Category**: Meta-compiler

---

## Overview

NC Compilations is the most distinctive plan in the NormCode ecosystem: **a NormCode workflow that produces other NormCode workflows**. Given a natural language task specification (e.g., "Build a workflow that analyzes customer feedback, categorizes it, and generates a summary report"), it generates a complete, executable NormCode project — draft, formal plan, provisions, and repositories.

This automates the "Describe" stage of the [NormCode lifecycle](../1_intro/ecosystem.md#the-lifecycle).

### Pipeline

```
Task Spec ──▶ Analyze ──▶ Derive (.ncds) ──▶ Formalize (.ncd) ──▶ Post-formalize (.pf.ncd)
                                                                           │
    ◀── Activate (repos) ◀── Parse (.nci.json) ◀── Generate Provisions ◀───┘
```

---

## The Plan (`.ncd`)

The `.ncds` for this project is a stub (`:<:{empty result} <= produce empty result`) because the compilation pipeline itself was authored directly in `.ncd` format. Here is the full formal plan:

```
:<:{compilation result} | ?{flow_index}: 1
    <= ::(report compilation status and output paths) | ?{sequence}: imperative
    
    /: ============================================================
    /: GROUND CONCEPTS - User-provided inputs
    /: ============================================================
    <- {project dir} | ?{flow_index}: 1.2
        <= :>: (input project dir) | ?{sequence}: imperative
        /: User-provided via folder picker
        <- {project dir user explanation}<:{1}>
    
    <- {task specification input} | ?{flow_index}: 1.3
        <= :>: (input task specification) | ?{sequence}: imperative
        /: User-provided via text entry or file path
        <- {task specification input user explanation}<:{1}>
    
    <- [context source paths] | ?{flow_index}: 1.4
        <= :>: (input context source paths) | ?{sequence}: imperative
        /: User-provided via multi-file picker
        <- [context source paths user explanation]<:{1}>
    
    /: ============================================================
    /: PHASE 0 - Setup Project Inputs
    /: ============================================================
    
    /: Determine if input is a file path or inline text
    <- <input is file path> | ?{flow_index}: 1.5
        <= ::(judge if task specification input is a valid file path) | ?{sequence}: judgement
        <- {task specification input}
    
    /: Copy from file (if is file path)
    <- {spec from file} | ?{flow_index}: 1.6
        <= ::(copy specification file to project) | ?{sequence}: imperative
            <= @:'(<input is file path>)           /: Timing gate: only if IS file path
            <* <input is file path>
        <- {task specification input}<:{1}>
        <- {project dir}<:{2}>
    
    /: Write text directly (if NOT file path)
    <- {spec from text} | ?{flow_index}: 1.7
        <= ::(write specification text to project) | ?{sequence}: imperative
            <= @:!(<input is file path>)           /: Timing gate: only if NOT file path
            <* <input is file path>
        <- {task specification input}<:{1}>
        <- {project dir}<:{2}>
    
    /: Load the specification (whichever was created)
    <- {task specification} | ?{flow_index}: 1.8
        <= ::(load task specification from project) | ?{sequence}: imperative
        <- {spec we have}<:{1}>
            <= $. %>({spec we have}) %<[{spec from file}, {spec from text}] | ?{sequence}: assigning
            /: Selects the first available from the list
            <- {spec from file}
            <- {spec from text}
        <- {project dir}<:{2}>
    
    <- {project context} | ?{flow_index}: 1.9
        <= ::(copy context sources into project and load) | ?{sequence}: imperative
        <- [context source paths]<:{1}>
        <- {project dir}<:{2}>
    
    /: ============================================================
    /: PHASE 1 - Specification Analysis
    /: ============================================================
    <- {specification analysis} | ?{flow_index}: 1.10
        <= ::(analyze specification to identify root output, ground inputs,
              and intermediate transformations) | ?{sequence}: imperative
        <- {task specification}
    
    /: ============================================================
    /: PHASE 2 - Draft Derivation (.ncds)
    /: ============================================================
    <- {ncds draft} | ?{flow_index}: 1.11
        <= ::(derive hierarchical draft structure with root at top
              and dependencies nested below) | ?{sequence}: imperative
        <- {specification analysis}
    
    <- {ncds file written} | ?{flow_index}: 1.12
        <= ::(write ncds draft to project directory) | ?{sequence}: imperative
        <- {ncds draft}<:{1}>
        <- {project dir}<:{2}>
    
    /: ============================================================
    /: PHASE 3 - Formalization (.ncd)
    /: ============================================================
    <- {formal ncd} | ?{flow_index}: 1.13
        <= ::(formalize draft by adding flow indices, sequence types,
              and value bindings) | ?{sequence}: imperative
        <- {ncds draft}
    
    <- {ncd file written} | ?{flow_index}: 1.14
        <= ::(write formal ncd to project directory) | ?{sequence}: imperative
        <- {formal ncd}<:{1}>
        <- {project dir}<:{2}>
    
    /: ============================================================
    /: PHASE 4 - Post-Formalization (.pf.ncd)
    /: ============================================================
    <- {post-formal ncd} | ?{flow_index}: 1.15
        <= ::(post-formalize by annotating paradigms, reference shapes,
              and provision paths) | ?{sequence}: imperative
        <- {formal ncd}
    
    <- {pf ncd file written} | ?{flow_index}: 1.16
        <= ::(write post-formal ncd to project directory) | ?{sequence}: imperative
        <- {post-formal ncd}<:{1}>
        <- {project dir}<:{2}>
    
    /: ============================================================
    /: PHASE 5 - Provision Generation
    /: ============================================================
    
    /: Extract provision demand from pf.ncd
    <- [required provisions] | ?{flow_index}: 1.17
        <= ::(extract all unique provision references from post-formal ncd)
        <- {post-formal ncd}
    
    /: Match context to demand and save mapping
    <- {context mapping saved} | ?{flow_index}: 1.18
        <= ::(save context mapping to project directory) | ?{sequence}: imperative
        <- {context mapping}<:{1}>
            <= ::(analyze project context and match to required provisions)
            <- {list of all required provisions}<:{1}>
                <= ::(collect all required provisions) | ?{sequence}: grouping
                <- [required provisions]
            <- {list of all project context}<:{2}>
                <= ::(collect all project context) | ?{sequence}: grouping
                <- {project context}
        <- {project dir}<:{2}>
    
    /: Generate and save each provision (loop)
    <- [provisions saved] | ?{flow_index}: 1.19
        <= *. loop over [required provisions]
            <= return saved provision status
            <- {provision content saved}
                <= ::(save provision content to project directory)
                <- {provision content}<:{1}>
                    <= ::(generate provision content using matched context)
                    <- {current provision}<:{1}>
                    <- {current provision context}<:{2}>
                        <= ::(get matched context content for current provision)
                        <- {current provision}<:{1}>
                        <- {context mapping}<:{2}>
                        <- {list of all project context}<:{3}>
                    <- {post-formal ncd}<:{3}>
                <- {project dir}<:{2}>
        <- [required provisions]
        <* {current provision}
    
    /: ============================================================
    /: PHASE 6 - Activation (Repository Generation)
    /: ============================================================
    
    /: Parse pf.ncd to nci.json (deterministic script)
    <- {nci json} | ?{flow_index}: 1.20
        <= ::(run parse_to_nci.py script) | ?{sequence}: imperative
        <- {pf ncd file written}<:{1}>
        <- {project dir}<:{2}>
    
    /: Activate nci.json to generate repositories (deterministic script)
    <- {repos written} | ?{flow_index}: 1.21
        <= ::(run activate_nci.py script) | ?{sequence}: imperative
        <- {nci json}<:{1}>
        <- {all provisions saved}<:{2}>
            <= ::(collect all saved provisions) | ?{sequence}: grouping
            <- [provisions saved]
        <- {project dir}<:{3}>
    
    /: ============================================================
    /: PHASE 7 - Ground Concept Initialization
    /: ============================================================
    
    <- [ground concepts needing input] | ?{flow_index}: 1.22
        <= ::(run extract_ground_concepts.py script) | ?{sequence}: imperative
            <= @.({repos written})    /: Timing: wait for repos to be written
            <* {repos written}
        <- {project dir}
    
    <- {inputs json written} | ?{flow_index}: 1.23
        <= ::(write inputs.json to project directory)
        <- {inputs json content}<:{1}>
            <= ::(generate inputs.json with ground concept placeholders)
            <- {list of ground concepts needing input}<:{1}>
                <= ::(collect all ground concepts) | ?{sequence}: grouping
                <- [ground concepts needing input]
            <- {task specification}<:{2}>
            <- {ncds draft}<:{3}>
            <- {list of all project context}<:{4}>
        <- {project dir}<:{2}>
    
    <- {placeholder files created} | ?{flow_index}: 1.24
        <= ::(write placeholder files to project directory)
        <- {placeholder content}<:{1}>
            <= ::(create simulated context files for file-based ground concepts)
            <- {list of ground concepts needing input}<:{1}>
            <- {task specification}<:{2}>
            <- {list of all project context}<:{3}>
        <- {project dir}<:{2}>
    
    /: ============================================================
    /: FINAL - Collect all info for report
    /: ============================================================
    <- {all infos to report} | ?{flow_index}: 1.25
        <= ::(collect all infos to report) | ?{sequence}: grouping
        <- {repos written}<:{1}>
        <- {inputs json written}<:{2}>
        <- {placeholder files created}<:{3}>
        <- {project dir}<:{4}>
```

---

## Phase-by-Phase Walkthrough

### Phase 0: Setup

Accepts three user inputs and resolves the specification:
- **`{project dir}`** — folder picker for the output project
- **`{task specification input}`** — text or file path; conditional branching determines how to load it
- **`[context source paths]`** — optional reference files copied into the project

The conditional branching pattern (`@:'(<input is file path>)` vs `@:!(<input is file path>)`) routes to either file copy or text write. An `assigning` sequence then selects whichever was produced.

### Phase 1: Specification Analysis

A single LLM call analyzes the task specification to identify:
- **Root output**: What the workflow ultimately produces
- **Ground inputs**: What external data is required
- **Transformations**: What operations connect grounds to root

### Phase 2-4: Progressive Compilation

Three LLM-driven phases progressively compile the plan:

| Phase | Input | Output | What's Added |
|-------|-------|--------|-------------|
| **Derive** | `{specification analysis}` | `.ncds` draft | Hierarchical concept structure, `<-` and `<=` markers |
| **Formalize** | `.ncds` draft | `.ncd` formal | Flow indices, sequence types, value bindings |
| **Post-formalize** | `.ncd` formal | `.pf.ncd` | Paradigm assignments, reference shapes, provision paths |

Each phase writes its output to disk before the next phase begins.

### Phase 5: Provision Generation

A loop iterates over all provisions referenced in the `.pf.ncd`:
1. **Extract** all unique provision references (prompt paths, paradigm names)
2. **Match** each provision to relevant context files (LLM)
3. **Generate** content for each provision using matched context (LLM per provision)
4. **Save** each provision to the project directory

### Phase 6: Activation

Two deterministic Python scripts transform the plan into executable repositories:
- **`parse_to_nci.py`** — parses `.pf.ncd` into `.pf.nci.json` (inference index)
- **`activate_nci.py`** — activates `.pf.nci.json` into `concept_repo.json` + `inference_repo.json`

These are syntactic operations — no LLM calls, no token cost.

### Phase 7: Ground Initialization

Prepares the generated project for first run:
- Extracts ground concepts that need user input
- Generates `inputs.json` with placeholder values
- Creates simulated context files for testing

---

## Key Design Patterns

| Pattern | How It's Used |
|---------|--------------|
| **Meta-compilation** | A NormCode plan that produces NormCode plans — the compiler uses its own output format |
| **Conditional branching** | `@:'` / `@:!` timing gates route file vs text input handling |
| **Assigning sequence** | `$. %>` selects the first available value from alternatives |
| **Provision loop** | `*. %>` iterates over provisions with per-item context matching |
| **LLM + script hybrid** | Creative decisions (analysis, derivation) use LLM; deterministic transforms (parsing, activation) use Python scripts |
| **Grouping** | `$#` packs lists into single objects before passing to LLM (avoiding axis conflicts) |

---

## Paradigm Distribution

| Type | Count | Purpose |
|------|-------|---------|
| LLM (imperative) | 8 | Analyze, derive, formalize, post-formalize, extract provisions, match context, generate provision, generate inputs |
| Python script (imperative) | 10 | parse_to_nci, activate_nci, file operations, extract_ground_concepts |
| User input | 3 | Folder picker, text input, multi-file picker |
| Conditional (judgement) | 1 | File path check |
| Assigning | 1 | Select spec from file or text |
| Grouping | 4 | Pack lists into objects for LLM consumption |
| Looping | 1 | Provision generation loop |

---

## Files

| File | Purpose |
|------|---------|
| `_.ncd` | Full formal plan (shown above, simplified) |
| `_.pf.ncd` | Post-formalized plan with paradigm annotations |
| `_.pf.nci.json` | Inference index |
| `repos/concept_repo.json` | Executable concept repository |
| `repos/inference_repo.json` | Executable inference repository |
| `provisions/prompts/analyze_specification.md` | Specification analysis prompt |
| `provisions/prompts/derive_ncds.md` | Draft derivation prompt |
| `provisions/prompts/formalize_ncd.md` | Formalization prompt |
| `provisions/prompts/post_formalize_ncd.md` | Post-formalization prompt |
| `provisions/prompts/extract_provisions.md` | Provision extraction prompt |
| `provisions/prompts/generate_provision.md` | Provision content generation prompt |
| `provisions/scripts/nc_compiler/` | Parser, concept builder, inference builder |
| `provisions/scripts/parse_to_nci.py` | `.pf.ncd` → `.pf.nci.json` |
| `provisions/scripts/activate_nci.py` | `.pf.nci.json` → repositories |
| `context/` | NormCode documentation used as reference for compilation |

---

## See Also

- **[README](README.md)** — Overview of all built-in plans
- **[Compilation Section](../4_compilation/README.md)** — The compilation pipeline this plan automates
- **[Grammar Section](../2_grammar/README.md)** — The `.ncd` syntax the plan generates

---

**Last Updated**: March 2026
