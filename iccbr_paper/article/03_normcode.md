# 3. NormCode as a Reasoning Medium

A reasoning medium is a representational language in which reasoning plans are
formulated, not merely described. It externalizes the structure of reasoning itself —
what is known, what is derived, how derivations depend on each other — into a form
simultaneously human-readable and machine-executable. This section demonstrates that
NormCode satisfies six properties that together constitute a working reasoning medium
for AI orchestration, and shows how these properties produce the enabling condition for
two-level CBR. The formal language specification is in [Anon. 2025].

## 3.1 Six Properties of a Working Reasoning Medium

**P1 — Interpretable.** A reasoning medium must be legible to humans at multiple roles
without programming expertise. NormCode achieves this at two levels. The `.ncds`
authoring format uses three markers and indentation — syntax that reads like structured
natural language, authorable by a domain expert without developer involvement. The
compiler's Formalization phase produces `.ncn` (NormCode Natural): a plain-prose
narrative of the entire plan, generated before any LLM call. A manager, compliance
officer, or domain expert reads the `.ncn`, verifies the reasoning structure matches
intent, and may reject the plan before any computation begins (C2, §1). The medium is
legible at every level of the stack.

**P2 — Enforceable.** What is reviewed must be exactly what executes. The compiler
verifies plan structure before the first run; the orchestrator enforces the scope rule
at runtime. The `.ncn` is a deterministic rendering of the actual formal plan — not a
paraphrase of intent. A plan that passes `.ncn` review cannot behave differently than
the review described, because the review is generated from the same formal
representation the orchestrator executes. The medium has structural teeth.

**P3 — Composable.** Three symbols and one scope rule combine into arbitrarily complex
workflows: nested loops, conditionals, parallel derivation, multi-agent coordination.
The composition rules do not change as complexity grows; a 5-node plan and a 40-node
plan are governed by the same grammar. The medium does not break at scale.

**P4 — Locally Addressable.** Every reasoning step has a dot-separated flow index
(`1.1`, `1.3.2`, etc.). The scope rule makes every step epistemically self-contained:
a developer can examine step `1.3.2` without understanding steps `1.1`–`1.3.1`,
because the scope rule guarantees `1.3.2` depends only on what is declared in its own
block. A compliance officer can review the output of `1.1` in isolation. The
orchestrator can re-run only downstream-stale steps after a correction (C3, §1). Local
addressability is what makes the CBR operations in §4 structurally safe.

**P5 — Generalizable.** The three primitives are domain-agnostic. The same syntax
expresses a PPT generation plan, a code review pipeline, a BOM matching task, a
scientific data analysis, or a medical treatment pathway — without domain-specific
extensions or modifications to the language.

**P6 — Portable.** A NormCode plan is a plain text `.ncds` file accompanied by
`concept_repo.json` and `inference_repo.json`. These artifacts are version-controlled,
shareable, and executable by any compliant orchestrator, independent of any specific
LLM or deployment platform. The plan belongs to its authors, not to any platform.

## 3.2 Syntax and the Scope Rule

Three markers constitute the full syntax:

| Marker | Role | Meaning in a plan |
|--------|------|--------------------|
| `<-` | Value Concept | A named value, document, or intermediate result — data flowing between steps |
| `<=` | Functional Concept | An operation that derives its parent concept from declared inputs |
| `<*` | Context Concept | In-loop state: marks the current element during iteration |

**Indentation defines scope.** The inputs available to any inference are exactly the
concepts declared in its immediately enclosing indented block. A concept at a higher
scope is not accessible to a nested step unless explicitly declared as input in that
step's block. There is no implicit sharing. This is the scope rule: structurally
enforced, compiler-verified, runtime-enforced.

A two-concept example (`.ncds` authoring format):

```
<- summary
    <= summarize the findings
    <- report
        <= read the uploaded file
        <- source_doc
    <- style_guide
```

Read bottom-up: `source_doc` is read to produce `report`; `report` and `style_guide`
are the declared inputs to the summarization inference that produces `summary`. Whether
each `≤=` invokes an LLM (semantic) or performs deterministic data manipulation
(syntactic) is determined by the functional concept type — covered in §3.3.
`style_guide` at the `summary` scope is explicit — not inherited.

**Flow indices** assigned during Formalization give each concept a stable address.
Following the sibling pattern — the functional concept is always `.1` under its parent,
value inputs are siblings at `.2`, `.3`, etc.:
`summary` → `1`, `report` → `1.2`, `source_doc` → `1.2.2`, `style_guide` → `1.3`.
Every checkpoint is stored and retrieved by `(run_id, flow_index)`.

**Iteration.** The context concept (`<*`) marks the current element during a loop.
It carries in-loop state without making it available to outer scopes:

```
<- all summaries
    <= for each document in the collection
    <- summary
        <= summarize this document
        <- document
    <- documents
    <* document
```

Each iteration of `summary` receives only its own `document` instance; sibling
iterations are invisible to each other. This is the structural guarantee that makes
per-slide isolation in the PPT Agent (§7.1) and per-file exploration in the Code
Assistant (§7.2) reliable CBR cases rather than entangled computations.

For full grammar, type system, and formal scope semantics, see [Anon. 2025].

## 3.3 Semantic vs. Syntactic Separation

**Semantic inferences** invoke LLMs to create new information. *Imperative* inferences
produce a concept (a named-axis tensor); *Judgement* inferences evaluate a truth
condition and return a boolean. Both are probabilistic, consume tokens, and are the
primary cost center.

**Syntactic inferences** perform deterministic data manipulation without LLM
involvement using four operator families: *Assigning* (`$`) routes data between
concepts; *Grouping* (`&`) collects or concatenates concepts; *Timing* (`@`) gates
execution on conditions or sequencing dependencies; *Looping* (`*`) manages
iteration with carried state. These are instant, zero-cost, and fully deterministic.

In production plans, 60–70% of nodes are syntactic. The Canvas App renders semantic
nodes as purple hexagons and syntactic nodes as gray rectangles — making the cost
structure of a plan immediately visible. This separation matters for CBR: syntactic
checkpoints are perfectly reproducible cases (same input → same output, always);
semantic checkpoints are bounded-stochastic (same input → same output distribution).

## 3.4 The Compilation Pipeline

A NormCode plan is compiled through four phases:

1. **Derivation** (LLM-assisted): extracts concepts, inference operations, dependencies,
   and hierarchical structure from the `.ncds` draft.

2. **Formalization** (rule-based): assigns flow indices; determines sequence types;
   generates the `.ncn` plain-prose narrative.

3. **Post-Formalization**: assigns paradigm IDs (execution configurations), tool
   faculties, tensor axis declarations, and agent assignments.

4. **Activation**: extracts `concept_repo.json` and `inference_repo.json` for the
   orchestrator.

The `.ncn` output of Phase 2 is the pre-execution interpretability artifact (C2). For
the slide generation plan:

```
(OUTPUT) collection of written slides
    (ACTION) is obtained by iterating over slide-outlines, where each iteration:
        (ACTION) is returning the following as individual output:
        (VALUE) slide-page-written
            (ACTION) is to write the following:
            (VALUE) slide-page
                (ACTION) is obtained by generating page from
                (VALUE) topic
                (VALUE) style_guide
                (VALUE) current_slide_outline
    (VALUE) slide-outlines
    (CONTEXT) for each current_slide_outline in the iteration
```

Little NormCode training is required to read this. §5 formalizes the compilation pipeline
itself as a Level 2 case — showing that the distillation process is itself expressible
and executable as a NormCode plan (self-hosting).

## 3.5 The Reference System and Perceptual Signs

Concepts' data are stored as **References** — N-dimensional named-axis tensors whose entries
can be values, file pointers, or *perceptual signs*: compact symbolic pointers of the
form `%{norm_type}unique_id(signifier)` that identify data without loading content into
the prompt. Large inputs (a 200-page document, a directory of source files) pass
between steps as tokens, preventing token-level context accumulation alongside the
structural isolation enforced by the scope rule.

When a step requires actual content, the orchestrator *transmutes* the perceptual sign
at the moment of the LLM call — never earlier. Checkpoints store compact pointers, not
content dumps, keeping the case base efficient at scale. The Tensor Inspector visualizes
References in table, list, or JSON view — making every completed step's exact bounded
inputs inspectable in O(1) operations (C1).

**Environmental replication.** A checkpoint whose tensors contain perceptual signs is
structurally self-contained — the scope rule eliminates hidden context dependencies —
but resuming from it requires the referenced external resources (files, APIs, databases)
to be accessible and consistent. This is a precondition for case reuse, distinct from
the structural isolation guarantee: the plan encodes *what* was used; whether that
environment is still available is outside the language's control. See §9.4.
