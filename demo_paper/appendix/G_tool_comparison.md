# Appendix G — Extended Tool Comparison

This appendix provides a full feature matrix comparing NormCode Canvas (v1.1.3)
against the most widely used visual and debugging tools for LLM agent workflows.
The Related Work section (§7) provides focused prose comparisons; this appendix
gives the complete feature table for practitioners evaluating tools.

**Tools compared:**
- **NormCode Canvas** (this system, v1.1.3)
- **LangSmith** (LangChain's tracing and evaluation platform)
- **LangFlow** (drag-and-drop visual builder for LangChain)
- **Microsoft PromptFlow** (DAG-based workflow tool for Azure AI)
- **AutoGen Studio** (visual interface for Microsoft AutoGen multi-agent framework)
- **Flowise** (open-source no-code LLM app builder)
- **Dify** (open-source LLM app development platform)

---

## G.1 Feature Matrix

| Feature | NormCode Canvas | LangSmith | LangFlow | PromptFlow | AutoGen Studio | Flowise | Dify |
|---------|----------------|-----------|----------|------------|----------------|---------|------|
| **Authoring & Plan Representation** | | | | | | | |
| Plan as portable text file | ✓ (`.ncds`) | ✗ (Python) | ✗ (platform JSON) | ✓ (YAML) | ✗ (Python config) | ✗ (platform JSON) | ✓ (YAML/JSON) |
| Version-controllable in Git | ✓ | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ |
| Non-programmer authoring | ✓ (`<-`, `<=`, `<*`) | ✗ | ✓ (drag-drop) | ✗ | ✗ | ✓ (drag-drop) | ✓ (UI) |
| AI-assisted plan generation | ✓ (Phase 1 derivation) | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ (limited) |
| **Pre-Execution Review** | | | | | | | |
| Human-readable plan before execution | ✓ (`.ncn` narrative) | ✗ | Partial (visual) | Partial (YAML) | ✗ | Partial (visual) | Partial (visual) |
| Non-technical review layer | ✓ (`.ncn` requires no syntax) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Review before any LLM is called | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Data Isolation & Context** | | | | | | | |
| Enforced data isolation between steps | ✓ (language-level) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Explicit input declaration per step | ✓ (required by syntax) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| No accumulated conversation history | ✓ (structural) | N/A | ✗ | ✗ | ✗ | ✗ | ✗ |
| Perceptual signs (lazy data refs) | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Execution & Monitoring** | | | | | | | |
| Real-time execution graph visualization | ✓ (WebSocket streaming) | ✗ | Partial (polling) | ✓ | ✗ | Partial | ✓ |
| Semantic vs. syntactic node distinction | ✓ (color-coded in graph) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Live tool call monitor (LLM prompts) | ✓ | ✓ (post-hoc) | ✗ | ✓ | ✗ | ✗ | ✓ |
| Per-step token cost visibility | ✓ (running counter) | ✓ (trace) | ✗ | ✓ | ✗ | ✗ | ✓ |
| **Debugging** | | | | | | | |
| Breakpoint at specific step | ✓ (flow index) | ✗ | ✗ | Partial | ✗ | ✗ | ✗ |
| Step-by-step advancement | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Inspect exact step inputs before execution | ✓ (tensor inspector) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Inspect inputs as typed N-dim tensor | ✓ (named axes, table/list/JSON) | ✗ (raw strings) | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Modification Without Restart** | | | | | | | |
| Value override at a paused step | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Selective re-run (only affected steps) | ✓ (dependency-driven) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Checkpoint-based state persistence | ✓ (SQLite, every step) | Partial (run-level) | ✗ | ✗ | ✗ | ✗ | ✗ |
| Fork from checkpoint | ✓ (parallel run branches) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Multi-Agent Support** | | | | | | | |
| Multiple LLMs in one workflow | ✓ (per flow index range) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Per-step LLM assignment | ✓ (pattern rules) | ✗ | Partial (per-node) | ✓ | ✓ | ✓ | ✓ |
| Heterogeneous tool bodies per agent | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Auditability** | | | | | | | |
| Full audit trail (every step logged) | ✓ (by construction) | ✓ (post-hoc) | ✗ | Partial | ✗ | ✗ | Partial |
| Audit trail without instrumentation | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Step addressable by stable ID | ✓ (flow index) | Partial (span ID) | ✗ | Partial | ✗ | ✗ | ✗ |
| Pre-execution audit document | ✓ (`.ncn`) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Deployment** | | | | | | | |
| Desktop app (Windows) | ✓ (Canvas App v1.1.3) | ✗ | Browser | Browser | Browser | Browser/self-hosted | Browser/self-hosted |
| Server/API deployment | ✓ (NormCode Server) | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| End-user client interface | ✓ (NormCode Clients) | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Open source | Partial (orchestrator) | ✗ (SaaS) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Platform-agnostic plan execution | ✓ (any NormCode orchestrator) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

---

## G.2 Key Distinctions Explained

**NormCode Canvas vs. LangSmith:**
Both provide full audit trails. The difference is *when* and *how*. LangSmith
captures what happened through post-hoc instrumentation — it hooks into the
LangChain execution path and records calls. NormCode's audit trail is
structural: because every concept declares its inputs and every input is stored
as a tensor, the audit is a by-product of how the plan runs, not a separate
logging layer. Removing LangSmith's instrumentation removes the audit trail;
removing NormCode's tensor store removes the system's ability to run at all.

Additionally, LangSmith shows the audit trail after a failure; NormCode's
tensor inspector shows what a step *is about to receive* before it runs —
enabling pre-failure inspection at a breakpoint. This is a qualitatively
different capability.

**NormCode Canvas vs. LangFlow / Flowise / Dify:**
All three provide non-programmer visual authoring. The critical difference is
portability. A LangFlow workflow is a platform-internal JSON graph — it cannot
be executed outside LangFlow, version-controlled as a text file, or handed to
a colleague running a different tool. A NormCode `.ncds` file is plain text:
any text editor can open it, any Git repository can store it, any NormCode
orchestrator can run it. The plan belongs to its author; the platform is
interchangeable.

Additionally, none of the visual builders produce a pre-execution
human-readable verification document. The `.ncn` format has no equivalent
in LangFlow, Flowise, or Dify — reviewers must read the visual graph (which
requires platform access and visual-graph literacy) or read Python code.

**NormCode Canvas vs. PromptFlow:**
PromptFlow is the closest architectural cousin — DAG-based, YAML-portable,
with Azure deployment support. The key gaps are: PromptFlow does not enforce
data isolation (data flows between nodes via prompt template variable binding,
which is implicit); it has no equivalent to breakpoint debugging with tensor
inspection; and it has no value override or checkpoint fork. PromptFlow's
`.jinja2` prompt templates make the data-flow contract implicit rather than
structurally enforced.

**NormCode Canvas vs. AutoGen Studio:**
AutoGen Studio focuses on multi-agent *conversation* patterns — agents exchange
messages in a conversation thread. The conversation history is the shared medium.
This is precisely the context pollution pattern NormCode eliminates: every agent
in an AutoGen conversation can see the entire prior conversation, with no
structural boundary between what each agent is supposed to know. NormCode
multi-agent configurations assign different LLMs to different step ranges while
maintaining the same isolation guarantee — each step sees only its declared
inputs regardless of which agent runs it.

---

## G.3 Feature Uniqueness Summary

Features present only in NormCode Canvas across all compared tools:

| Feature | Why it matters |
|---------|---------------|
| Enforced data isolation at language level | Debugging is a property of the language, not a feature of the tool |
| `.ncn` pre-execution human review | Non-technical stakeholders can verify logic before any cost is incurred |
| Tensor inspector (N-dimensional, named axes, before execution) | "What will this step see?" answered structurally, not reconstructed |
| Value override without restart | Fixing one step does not discard all completed upstream work |
| Checkpoint fork (parallel run branches) | Experimental branching without destroying the current run |
| Semantic/syntactic separation visible in graph | Cost and failure attribution are immediate from graph color |
| Perceptual signs / lazy data references | Large data objects pass between steps as pointers, not content |
| Platform-agnostic plan (`.ncds` text file) | The plan is an asset; the platform is infrastructure |
