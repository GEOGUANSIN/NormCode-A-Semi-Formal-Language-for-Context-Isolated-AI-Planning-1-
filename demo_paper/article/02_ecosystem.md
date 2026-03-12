# 2. The NormCode Ecosystem

## 2.1 Three Roles, Six Products

NormCode is designed for three distinct roles, each with purpose-built tools:

| Role | Products | Primary activity |
|------|----------|-----------------|
| **Agent Designer** (engineers, developers) | Language · Compiler · Agent (Orchestrator) | Write plans in `.ncds`, compile to executable, run |
| **Product Operator** (managers, ops teams) | Canvas App · Server | Inspect execution, debug, manage versions, collaborate |
| **End User** (domain experts, consumers) | Clients | Interact with deployed agents via purpose-built interfaces |

The plan — a `.ncds` text file — is the artifact that flows through all three
roles. The designer authors it, the operator reviews and debugs it, the end user
receives its output. No role requires the others' tools; each engages with the
same underlying logic through a view suited to their expertise.

## 2.2 The Plan Lifecycle

Every NormCode workflow follows a six-step lifecycle:

```
Describe → Compile → Review → Run → Modify → Deploy
```

| Step | What happens | Who |
|------|-------------|-----|
| **Describe** | Write the plan in `.ncds`, or generate it from a natural-language instruction | Designer |
| **Compile** | Four-phase pipeline transforms `.ncds` into executable JSON repositories | Designer / Compiler |
| **Review** | Domain expert reads the `.ncn` plain-English narrative to approve logic before any LLM call is made | Operator / Domain expert |
| **Run** | Orchestrator executes each step; every input and output is logged with full tensor structure | Operator |
| **Modify** | Override a value mid-run, re-run only affected steps, or fork from a checkpoint | Operator |
| **Deploy** | The `.ncds` file is the asset — commit it to Git, share it, hand it to a colleague or a different orchestrator | Designer |

The Review step is the most frequently overlooked differentiator. Before a single
LLM call is made, a stakeholder who has never seen formal syntax can read:

> *(OUTPUT)* slide\_3 *(ACTION)* is obtained by generating slide content
> *(INPUT)* using outline\_section\_3 *(INPUT)* and style\_guide.

This is the `.ncn` format — a compiler-generated natural-language translation of
the formal plan, identical in information content, readable by a manager or
compliance officer.

## 2.3 The Language in Brief

NormCode uses three primary markers:

| Marker | Meaning | Analogy |
|--------|---------|---------|
| `<-` | **Data** — a value, document, or result flowing through the plan | Noun |
| `<=` | **Action** — an operation an AI agent performs | Verb |
| `<*` | **State** — carried data across loop iterations | Loop variable |

**Indentation defines scope.** Each step can only see data declared within its
own indented block — not the full plan, not prior steps' outputs, not accumulated
context. This is the enforcement mechanism for data isolation.

A complete two-step plan reads as:

```
<- summary
    <= summarize the findings
    <- report
        <= :: read the uploaded file
    <- style_guide
```

Read bottom-up: *the uploaded file is read to produce a report; the report and
the style guide are used to summarize the findings; the result is the summary.*
Flow indices (`1`, `1.1`, `1.1.1`, …) give every node a unique address for
debugging, breakpointing, and cross-referencing. The full type system, syntactic
operator algebra, and reference system are detailed in [CITE: full paper].

> **[FIGURE 4 HERE — Ecosystem roles × products table + lifecycle diagram]**
