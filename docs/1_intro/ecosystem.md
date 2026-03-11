# The NormCode Ecosystem

**NormCode is the working language for AI agents — a complete ecosystem for designing, compiling, running, debugging, deploying, and using structured AI workflows.**

---

## Where NormCode Fits

Today's approaches to AI agent workflows each leave a gap:

| Approach | Examples | Limitation |
|----------|----------|------------|
| **Raw AI Models** | Claude, GPT, Qwen | You adapt to how the model works. No structure, no auditability. |
| **Agent Code Frameworks** | LangChain, LlamaIndex, CrewAI | Python code — only the developer can read it, only the developer can change it. |
| **Workflow Orchestration UIs** | Dify, Coze | Drag-and-drop locked UIs. Not suited for complex, multi-step scenarios. |

**NormCode's answer**: Plans that combine minimal formalization with natural language. No coding required. Easily read and run. AI can generate them. Scale, combine, reuse.

---

## The Lifecycle

Every NormCode plan follows a six-stage lifecycle:

```
  1. Describe       2. Compile        3. Review
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Write the │────▶│ Compiler │────▶│ Read     │
  │ plan — or │     │ transforms│     │ every    │
  │ have AI   │     │ to exec- │     │ step     │
  │ generate  │     │ utable   │     │ before   │
  │ it        │     │ workflow │     │ it runs  │
  └──────────┘     └──────────┘     └──────┬───┘
                                           │
  6. Deploy         5. Modify         4. Run
  ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Ship it. │◀────│ Change   │◀────│ Orchest- │
  │ Git it,  │     │ one step │     │ rator    │
  │ publish, │     │ without  │     │ runs each│
  │ hand it  │     │ breaking │     │ step.    │
  │ to a     │     │ others.  │     │ I/O      │
  │ colleague│     │ Fork from│     │ recorded │
  └──────────┘     │ any point│     └──────────┘
                   └──────────┘
```

| Stage | What Happens | Documentation |
|-------|-------------|---------------|
| **Describe** | Write the plan in `.ncds` format, or have an LLM generate it from a description | [Quickstart](quickstart.md), [Grammar](../2_grammar/README.md) |
| **Compile** | The compiler transforms the plan through 4 phases into executable repositories | [Compilation](../4_compilation/README.md) |
| **Review** | Read every step before it runs. A manager can approve the plan. | [User Guide](../5_tools/canvas_app_user_guide.md) |
| **Run** | The orchestrator executes each inference. Every input and output is recorded. | [Execution](../3_execution/README.md), [Canvas](../5_tools/README.md) |
| **Modify** | Change one step without breaking others. Fork from any checkpoint. | [Debugging Guide](../5_tools/canvas_app_debugging_guide.md) |
| **Deploy** | Ship it. The file is yours — git it, publish it, hand it to a colleague. | [Server Guide](../5_tools/normcode_server_guide.md) |

---

## Three Roles, Six Products

The NormCode ecosystem serves three distinct roles, each with purpose-built products:

### Agent Designer — Build the intelligence

Engineers and developers who design agent workflows.

| Product | What It Does | Documentation |
|---------|-------------|---------------|
| **Language** | Structured, readable syntax for defining AI workflows. Two symbols (`<-` for data, `<=` for actions), semi-formal descriptions, progressive compilation. | [Grammar](../2_grammar/README.md) |
| **Compiler** | 4-phase pipeline: Derivation (natural language to `.ncds`) → Formalization (`.ncd`) → Post-Formalization (context + resources) → Activation (executable repositories). | [Compilation](../4_compilation/README.md) |
| **Agent** | The execution unit — the Orchestrator runs compiled workflows step by step, with data isolation, parallel execution, and checkpoint/resume. | [Execution](../3_execution/README.md) |

### Product Operator — Manage and maintain

Managers and ops teams who inspect, debug, and deploy.

| Product | What It Does | Documentation |
|---------|-------------|---------------|
| **Canvas** | Visual debugging, step-by-step inspection, breakpoints, value override, multi-agent configuration, and complete audit trails. The graph IS the interface. | [Canvas App](../5_tools/README.md) |
| **Server** | Standalone deployment server. Version control, shared workspace, remote execution, plan management, and team collaboration. | [Server Guide](../5_tools/normcode_server_guide.md) |

### End User — Use the result

Domain experts and consumers who interact with finished AI agents.

| Product | What It Does | Documentation |
|---------|-------------|---------------|
| **Clients** | Purpose-built interfaces for each scenario — chat, forms, dashboards, file upload workflows, whatever the agent needs. No technical knowledge required. | [Settings Guide](../5_tools/canvas_app_settings_guide.md) |

### Product Flow

```
Agent Designer                  Product Operator              End User
┌──────────────────────┐       ┌────────────────────┐       ┌──────────────┐
│                      │       │                    │       │              │
│  Language ──▶ Compiler ──▶ Agent ──▶ Canvas ◀──▶ Server ──▶ Clients    │
│                      │       │                    │       │              │
│  Design the plan     │       │  Debug, inspect,   │       │  Use the     │
│  Compile to workflow │       │  deploy, monitor   │       │  finished    │
│  Configure the agent │       │  version control   │       │  product     │
└──────────────────────┘       └────────────────────┘       └──────────────┘
```

---

## Six Technical Properties

These properties are built into NormCode's architecture, not bolted on:

| Property | What It Means |
|----------|--------------|
| **Semantic vs. Syntactic** | Only reasoning costs tokens. Data routing, filtering, and looping are always free. Syntactic operations (assigning, grouping, looping) never call the LLM. |
| **Parallel Execution** | Independent steps run simultaneously. The orchestrator automatically detects which inferences can execute in parallel based on data dependencies. |
| **Checkpoint & Resume** | SQLite state at every step. Pause execution, resume later, fork from any checkpoint. No work is lost. |
| **Smart Patching** | Change one step, re-run only what's affected. Previously computed results are cached. No need to re-execute the entire plan. |
| **Flow Index System** | Every node has a unique hierarchical address (e.g., `1.2.3`). Set breakpoints, trace logs, debug precisely — each step is individually addressable. |
| **Progressive Compilation** | 4 phases from natural language description to executable workflow. Inspect and validate at every stage. Start rough, refine incrementally. |

---

## Documentation Map

Each documentation section corresponds to an ecosystem product:

| Section | Ecosystem Product | Content |
|---------|------------------|---------|
| **[1. Introduction](README.md)** | — | Philosophy, quickstart, examples, ecosystem overview |
| **[2. Grammar](../2_grammar/README.md)** | Language | `.ncd` syntax, semantic concepts, references, NCN translation |
| **[3. Execution](../3_execution/README.md)** | Agent | Runtime model, reference system, agent sequences, orchestrator |
| **[4. Compilation](../4_compilation/README.md)** | Compiler | Derivation, formalization, activation, post-formalization |
| **[5. Tools](../5_tools/README.md)** | Canvas + Server | Canvas App, NormCode Server, debugging, deployment |
| **[6. Built-in Plans](../6_normcode_built-in/README.md)** | All | Real-world plans: assistants, meta-compiler, PPT, reports, BOM |

---

## Getting Started

Depending on your role:

### Agent Designer
1. Read the [Overview](overview.md) to understand the philosophy
2. Follow the [Quickstart](quickstart.md) to write your first plan
3. Study the [Grammar](../2_grammar/README.md) for full syntax
4. Learn [Compilation](../4_compilation/README.md) to understand the pipeline

### Product Operator
1. Read the [Canvas App User Guide](../5_tools/canvas_app_user_guide.md)
2. Explore [Debugging & Auditing](../5_tools/canvas_app_debugging_guide.md)
3. Set up a [NormCode Server](../5_tools/normcode_server_guide.md) for deployment

### End User
1. Access the client interface provided for your specific use case
2. The agent runs transparently — every step is auditable if you need to inspect it

---

## About PsylensAI

NormCode is developed by **Guangzhou Psylens Technology Studio** (PsylensAI).

**Mission**: Transform AI reasoning from black-box dialogue into structured, auditable execution chains. We solve the controllability, explainability, and reproducibility challenges in complex AI applications — targeting high-compliance domains like financial risk, legal review, and enterprise decision systems.

**Vision**: Auditable AI for transparent, controllable development. Human values should be clearly expressed, recorded, and executed — then transformed into sustainable technical assets that can be owned, verified, and inherited.

**Research**: [NormCode: A Normative Language for AI Agent Plans](https://arxiv.org/abs/2512.10563)

**Contact**: xin.guan@psylensai.com

---

## See Also

- **[Overview](overview.md)**: What NormCode is and why it exists
- **[Quickstart](quickstart.md)**: Write your first plan
- **[Examples](examples.md)**: Pattern gallery
- **[Tools](../5_tools/README.md)**: Canvas App and NormCode Server
- **[Built-in Plans](../6_normcode_built-in/README.md)**: Real plans that ship with NormCode

---

**Last Updated**: March 2026
