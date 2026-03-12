# Introduction to NormCode

Welcome to NormCode — the working language for AI agents. A complete ecosystem for designing, compiling, running, debugging, deploying, and using structured AI workflows.

---

## Start Here

If you're new to NormCode, read these in order:

### 0. [Ecosystem](ecosystem.md)
**The big picture: 6 products, 3 roles, one lifecycle**

- Where NormCode fits (vs raw models, code frameworks, workflow UIs)
- The Describe → Compile → Review → Run → Modify → Deploy lifecycle
- Three roles: Agent Designer, Product Operator, End User
- Six products: Language, Compiler, Agent, Canvas, Server, Clients
- Six technical properties

**Read this if**: You want to understand the full NormCode ecosystem before diving into details.

**Time**: 5 minutes

---

### 1. [Overview](overview.md)
**What is NormCode and why does it exist?**

- The context pollution problem
- How data isolation solves it
- Core concepts
- When to use (and not use) NormCode
- Three formats, one system

**Read this if**: You're evaluating NormCode or want to understand the big picture.

**Time**: 10 minutes

---

### 2. [Quickstart](quickstart.md)
**Write your first plan in 5 minutes**

- Basic syntax (`<-` and `<=`)
- Execution flow (child-to-parent / inside-out)
- Multi-input operations
- Loops and conditions
- Complete working examples

**Read this if**: You want to start writing plans immediately.

**Time**: 5-10 minutes

---

### 3. [Examples](examples.md)
**Gallery of common patterns**

- Document processing
- Conditional workflows
- Iteration patterns
- Data collection
- Nested workflows
- Real-world use cases

**Read this if**: You learn best by seeing examples.

**Time**: Browse as needed

---

## Quick Navigation

### Want the Big Picture
→ [Ecosystem](ecosystem.md) — the full product landscape, roles, and lifecycle

### Just Starting
→ [Overview](overview.md) → [Quickstart](quickstart.md) → [Examples](examples.md)

### Ready to Write Plans
→ [Quickstart](quickstart.md) → [Grammar Section](../2_grammar/README.md)

### Want to Execute Plans
→ [Tools Section](../5_tools/README.md)

### Want to Deploy Plans
→ [NormCode Server Guide](../5_tools/normcode_server_guide.md)

### Need Deep Understanding
→ [Execution Section](../3_execution/README.md) → [Compilation Section](../4_compilation/README.md)

---

## Key Concepts (Quick Reference)

### Positioning

NormCode is not a raw model, not a code framework, not a drag-and-drop UI. It is a **semi-formal language** that combines structure with natural language — plans that anyone can read, AI can generate, and the orchestrator can execute with full auditability. See [Ecosystem](ecosystem.md) for the full comparison.

### The Two Symbols

| Symbol | Name | Meaning |
|--------|------|---------|
| `<-` | Value Concept | Data (nouns) |
| `<=` | Functional Concept | Actions (verbs) |

### Data Isolation

Each step only sees explicitly passed inputs. No accidental context leakage.

### Semi-Formal Language

NormCode balances structure with readability:
- **Not pure natural language** (which is ambiguous)
- **Not fully formal code** (which is rigid)  
- **Structured but accessible** (clear rules, readable content)

### Syntactic vs. Semantic

| Type | LLM Call? | Cost | Examples |
|------|-----------|------|----------|
| **Semantic** | ✅ Yes | Tokens | Analyze, generate, reason |
| **Syntactic** | ❌ No | Free | Collect, select, loop |

### Core Formats

| Format | Purpose | You Interact With |
|--------|---------|-------------------|
| `.ncds` | Draft/authoring | ✅ Start here |
| `.ncd` | Formal syntax | After formalization |
| `.nci.json` | Inference structure | Intermediate format |
| `.concept.json` + `.inference.json` | Executable repositories | Orchestrator loads these |

**Companion formats**: `.ncn` (natural language view of `.ncd`), `.ncdn` (hybrid editor format)  
**Auxiliary formats**: `.nc.json` (JSON structure for tooling)

---

## Common Questions

**Q: Do I need to learn formal syntax?**  
A: No. Start writing in `.ncds` (draft format). The compiler handles formalization to `.ncd` + `.ncn`, then structuring to `.nci.json`, and finally activation to `.concept.json` + `.inference.json`.

**Q: How is this different from LangChain?**  
A: NormCode enforces explicit data isolation. Each step's inputs are declared, not implicit.

**Q: Is this overkill for simple tasks?**  
A: Yes. Use NormCode when you have 5+ steps and need isolation/debuggability.

**Q: Can I use my own LLM?**  
A: Yes. Agent body (repositories of tools) and paradigms (execution strategies) are configurable.

**Q: What if a step fails?**  
A: Inspect its inputs in the orchestrator. Everything is explicit and traceable.

---

## What's Next?

After reading the intro section, continue to:

- **[Grammar](../2_grammar/README.md)** - The Language: complete `.ncd` syntax specification
- **[Execution](../3_execution/README.md)** - The Agent: how plans run at runtime
- **[Compilation](../4_compilation/README.md)** - The Compiler: 4-phase compilation pipeline
- **[Tools](../5_tools/README.md)** - Canvas + Server: visualization, execution, debugging, deployment
- **[Built-in Plans](../6_normcode_built-in/README.md)** - Real-world plans: assistants, meta-compiler, PPT generation, BOM matching

---

**Ready to start?** → [Ecosystem](ecosystem.md) for the big picture, or [Overview](overview.md) to dive in
