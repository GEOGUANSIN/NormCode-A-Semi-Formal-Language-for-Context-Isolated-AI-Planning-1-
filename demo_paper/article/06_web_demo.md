# 6. Live Web Demo

A live instance of the PPT Agent is accessible at:

> **[DEMO URL — to be confirmed before submission]**

Users enter a topic, click submit, and the NormCode Orchestrator runs the PPT
Agent plan server-side — the same plan and the same orchestrator described in
Scenario A, not a simplified mock. The output is a rendered HTML presentation
preview and a downloadable `.pptx` file, typically completing in under two
minutes depending on model latency.

The web demo is built on the NormCode **Server** component, which exposes the
orchestrator via a REST API, and the NormCode **Client** interface — a
purpose-built form-to-output UI that requires no NormCode knowledge to use. The
plan running behind the interface is `ppt_generation.ncds`; the client only sees
inputs and outputs. This is the three-role split in practice: the Designer
authored the plan, the Operator deployed it, the End User uses it through a
clean interface with no exposure to plan internals.

**Also available for local use:**

- **Canvas App for Windows** (alpha, v1.1.3): downloadable at [DOWNLOAD URL]
- **Portable example project** (`.normcode-portable.zip`): a pre-configured
  project containing the PPT Agent plan, compiled repositories, and a demo
  Canvas project, loadable immediately without any build steps

> **[QR CODE — link to live demo]**
>
> *A video walkthrough of both demo scenarios is available at [VIDEO URL].*
