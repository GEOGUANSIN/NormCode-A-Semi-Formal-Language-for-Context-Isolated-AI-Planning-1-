# 1. Introduction

Practitioners building AI agent workflows today navigate a fragmented landscape.
**Raw LLMs** (GPT, Claude, Qwen) are powerful but opaque — each model carries its
own prompt style and training assumptions; you adapt to the model rather than
defining the workflow. **Agent code frameworks** (LangChain, LlamaIndex, CrewAI)
provide orchestration but lock the workflow inside Python code: only developers can
read it, only developers can change it, and when something goes wrong, debugging
happens in the dark [CITE: patel2025]. **No-code orchestration UIs** (Dify, Coze)
lower the barrier but cannot scale to complex scenarios requiring loops,
conditionals, and dynamic data routing — and the workflow is locked inside the
platform's proprietary representation.

What all three approaches lack is a **working language** — an intermediate
representation with the property that only languages have: *learn it once and
describe any workflow*, independent of any specific model, framework, or
deployment target. Like SQL for databases, a working language for AI agent
workflows gives every stakeholder a common medium for expressing, inspecting, and
reasoning about what an agent will do. The plan is a portable text document:
version-controlled, shareable, executable by any compliant orchestrator, with no
vendor lock-in.

**NormCode** is that language. Plans are written in a minimal three-symbol syntax
(`<-` for data, `<=` for actions, `<*` for loop/condition state) that non-programmers can
read, and enforced by a compiler and orchestrator that guarantee explicit data
isolation between every step. Each step sees only what it is explicitly given —
no accumulated context, no implicit state leakage — making failures immediately
localizable and the full execution auditable by construction [CITE: full paper].

This paper presents the **NormCode Canvas** (v1.1.3), the primary visual
environment for executing and debugging NormCode plans. We demonstrate the system
through two scenarios that cover the full stakeholder journey:

- **Scenario A — PPT Agent:** An end-to-end run through the complete lifecycle
  (Describe → Compile → Review → Run → Modify → Deploy), using a production
  presentation-generation plan. We highlight the `.ncn` human-verification layer
  — a plain-English narrative a domain expert reads before any LLM call is made.

- **Scenario B — Debug and Fork:** A debugging session on the NormCode Code
  Assistant plan, showing breakpoint pausing, tensor inspection of bounded step
  inputs, value override without restart, and checkpoint forking for parallel
  experimentation.

Both scenarios run on production software. The formal language specification,
type system, and compiler theory are detailed in the companion paper
[CITE: arXiv:2512.10563]; this paper focuses on the demonstrated system.
