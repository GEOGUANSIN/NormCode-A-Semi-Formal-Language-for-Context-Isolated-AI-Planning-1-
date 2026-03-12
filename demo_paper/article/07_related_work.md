# 7. Related Work

## Visual and Debugging Tools for LLM Workflows

The closest tools to the NormCode Canvas are visual builders and observability
platforms for LLM workflows.

**LangFlow** [CITE: langflow] provides a drag-and-drop visual builder for
LangChain pipelines. Workflows are constructed in a browser UI and stored as
platform-internal JSON graphs. LangFlow lowers the authoring barrier but does not
produce a portable artifact: the graph is tied to the LangFlow platform and cannot
be version-controlled as a text file or executed by an independent runtime.
NormCode's `.ncds` plans are plain text, ownable, and runtime-agnostic.

**LangSmith** [CITE: langsmith] provides tracing, evaluation, and debugging for
LangChain and LangGraph runs. It captures LLM call logs and presents them as
traces. The key distinction is that LangSmith captures what happened
*post-hoc* through instrumentation; NormCode's Canvas shows what *will happen*
before a step runs (via the `.ncn` review) and what a step *is about to receive*
at a breakpoint (via the tensor inspector). Debugging in LangSmith starts after
failure; in Canvas it starts before.

**Microsoft PromptFlow** [CITE: promptflow] is a DAG-based workflow tool for
Azure AI that supports visual authoring, testing, and evaluation of LLM flows.
It introduces a concept of connections and tools similar to NormCode's body
faculties. However, data flow between steps remains implicit in the prompt
templates, and there is no equivalent to NormCode's semantic/syntactic separation,
perceptual signs, or checkpoint-based forking.

**AutoGen Studio** [CITE: autogen_studio] (Microsoft Research) provides a visual
interface for configuring and running AutoGen multi-agent conversations. It focuses
on agent-to-agent communication patterns rather than explicit data flow; the
conversation history serves as implicit shared context, which is precisely the
context pollution pattern NormCode eliminates.

**Flowise** [CITE: flowise] and similar open-source no-code builders (Dify, Coze)
follow the same visual drag-and-drop model as LangFlow. They are effective for
simple scenarios but share the same portability and scaling limitations.

## Agent Frameworks

NormCode's position differs from agent frameworks rather than competing with them.
ReAct [CITE: yao2022] interleaves reasoning and action traces but does not isolate
context between steps. LangGraph [CITE: ibm_langgraph] makes the workflow graph
topology explicit and inspectable — a structural transparency NormCode shares —
but leaves data flow between nodes implicit in the node functions. AutoGen
[CITE: autogen] enables multi-agent conversations with role specialization but
uses accumulated conversation history as the shared medium. NormCode enforces
isolation at the language level: each node in the graph declares its inputs
explicitly, and the orchestrator enforces that no other data is accessible.

## The Auditability Gap

The need for auditable AI systems is increasingly codified. The EU AI Act
[CITE: eu_ai_act] requires that high-risk AI systems maintain logs sufficient to
enable post-hoc reconstruction of system behaviour. NormCode's audit trail —
every step's explicit inputs and outputs, every LLM call indexed by flow index —
satisfies this requirement structurally, not through post-hoc instrumentation.
Work on explainability for sequential AI [CITE: TBD from literature review] has
largely focused on explanation generation rather than structural prevention of
information leakage; NormCode's approach is complementary, providing the audit
substrate on which explanation methods can operate.

---

> **NOTE FOR FINAL VERSION:** Citations marked [CITE: TBD] and tool comparisons
> should be updated with full references from the literature review (see
> `literature_review_plan.md`). In particular, confirm: LangFlow publication or
> system description, PromptFlow EMNLP/ACL paper if any, AutoGen paper (Wu et al.
> 2023), and EU AI Act article references.
