# Abstract

Building AI agent workflows today forces a choice between three imperfect options:
raw LLMs that are opaque and model-specific, code frameworks that only developers
can read and maintain, and no-code platforms that cannot scale to complex scenarios.
What is missing is a *working language* — a shared, portable representation that
any stakeholder can learn once and apply to any workflow, independent of model,
framework, or platform.

We present the **NormCode Canvas** (v1.1.3), a visual execution and debugging
environment for NormCode — a semi-formal language for AI agent planning that
enforces explicit data isolation between steps, making workflows auditable by
construction. We demonstrate the system through two scenarios: (A) an end-to-end
PPT Agent run showing the full Describe → Compile → Review → Run → Modify →
Deploy lifecycle, including the `.ncn` human-verification layer before execution;
and (B) a Debug and Fork session on the NormCode Code Assistant plan, showing
breakpoint debugging, tensor inspection of bounded step inputs, value override
without restart, and checkpoint forking. Both scenarios run on production software
available for download. A live web demo is accessible at [URL].

> **Keywords:** AI agent workflows, visual debugging, data isolation, auditability,
> semi-formal language, LLM orchestration
