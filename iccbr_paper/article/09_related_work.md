# 10. Related Work

## 10.1 Process-Oriented CBR Foundations

Bergmann [2002] established process-oriented CBR (POCBR) as the application of CBR
principles to workflow management, defining process cases as structured sequences of
operations with associated data, and developing the experience management framework
under which workflow traces become reusable experience objects. Minor, Montani &
Recio-García [2014] characterize POCBR as the field where cases capture workflow
knowledge — the path to a solution, not only its endpoint — enabling retrieval and
adaptation of past executions for new tasks. The foundational CBR cycle — Retrieve,
Reuse, Revise, Retain — was given its canonical formulation by Aamodt & Plaza [1994],
who organized the framework through a knowledge-level task decomposition; Kolodner [1993]
provides the foundational treatment of case content, structure, and indexing.

Within POCBR, Bergmann & Gil [2014] represent workflows as semantically labeled graphs
and address efficient retrieval through structural similarity; Müller & Bergmann [2015a]
introduce a query language (POQL) where the query itself is a partial workflow, enabling
retrieval from an intermediate step. Both lines confirm that POCBR supports what NormCode's
§4 operationalizes: retrieval can begin from a partial execution state, not only from a
fresh start. The key gap these works leave open is formalized in §2: their case objects are
workflow models or event-log traces, not resumable runtime environments with guaranteed
input isolation. Bottrighi et al. [2016] extend this to business process operational
support, treating trace prefixes as queries against a log of completed executions — a
close relative to NormCode's Level 1 checkpoint retrieval. Leake & Kendall-Morwick [2008]
explicitly propose mining workflow provenance traces as CBR cases, demonstrating that
the trace-as-case framing is established in the community. NormCode's contribution is to
strengthen it: by enforcing structural isolation at the language level, every captured
checkpoint is a reliable, self-contained case rather than a provenance observation whose
implicit dependencies must be reconstructed.

## 10.2 Multi-Level and Hierarchical CBR

The two-level architecture of §4–§5 — concrete runtime cases at Level 1, abstract
runtime definitions as cases at Level 2 — has a direct ancestor in POCBR. Müller &
Bergmann [2015b] introduce *generalized workflow cases* that cover a subspace of the
case representation space, with retrieval followed by specialization to match a concrete
query. This is the closest prior work to NormCode's Level 2: both treat the abstract
pattern as a case object from which concrete instances are derived. The difference is
generative: NormCode's Level 2 cases (plans) are executable compiled artifacts, and the
distillation process (compilation pipeline) is itself expressible as a NormCode plan.
Veloso [1997] and Ihrig & Kambhampati [1997] establish that *plan derivations* — the
reasoning processes that produce solutions — can themselves be stored and retrieved as
cases, supporting plan-level CBR reuse. These works provide the prior-art lineage for
treating "how reasoning was conducted" as a case object. NormCode makes this concrete
and deployable: its four production-ready plans constitute an initial case library of abstract reasoning
patterns; self-hosted compilation demonstrates Level 2 CBR applied to the compilation
process itself. López de Mántaras et al. [2005] survey the full 4R lifecycle, including
case retention and maintenance, confirming that case base management (§9 limitations)
is an active research concern.

## 10.3 CBR and Large Language Models

Recent work combining CBR and LLMs falls into two broad directions. The dominant direction
uses CBR to improve individual LLM calls: Rubin, Herzig & Berant [2022] learn to retrieve
few-shot prompts for in-context learning; Zhang, Feng & Tan [2022] frame example selection
as an active learning problem; Xu et al. [2023] apply kNN-style inference for zero-shot
generalization. Wilkerson & Leake [2024] implement CBR components using LLMs, enabling
similarity assessment and adaptation without hand-engineered knowledge; Lenz, Hoffmann &
Bergmann [2025] evaluate LLMs directly as similarity assessors in CBR pipelines
(LLsiM). These works use CBR *to improve LLM calls*, or LLMs *to implement CBR functions*.

NormCode's direction is orthogonal. Rather than improving individual calls, it applies a
CBR architecture to manage the *execution of multi-step LLM workflows* — where the case
is not an in-context example but a suspended runtime state of a complete reasoning
process. Guo et al. [2024] (DS-Agent) is the closest prior work in this direction:
CBR is used to iteratively revise multi-step data-science plans across attempts. The
difference from NormCode is structural: DS-Agent's case objects are narrative plans
without enforcement guarantees, whereas NormCode's checkpoints are structurally isolated
by compiler and runtime, guaranteeing case integrity.

## 10.4 LLM Workflow Tools

LangGraph [IBM 2024] provides a graph-topology workflow engine with checkpoint support
and explicit time-travel replay, making it the closest tool to NormCode's Canvas App in
surface behavior. PromptFlow (Microsoft Azure) and LangFlow provide DAG-based visual
workflow authoring. AutoGen [Wu et al. 2023] enables multi-agent conversations with
role specialization. None of these enforce structural isolation between steps: data
flows through accumulated conversation histories, shared Python state, or implicit prompt
templates. As established in §2, checkpoints captured without isolation guarantees are
not clean CBR cases — reusing them in a new context produces incorrect behavior because
the implicit dependencies that were present during original execution are no longer
available. The Canvas App is differentiated not by the presence of checkpoints but by
the structural guarantee that makes those checkpoints reliable case objects.

## 10.5 Process Mining

Process mining [van der Aalst 2011; van der Aalst, Weijters & Maruster 2004] discovers
process models from event logs, checks conformance between observed and normative behavior,
and enhances process models through execution evidence. NormCode's Level 2 distillation —
the compilation pipeline that transforms natural-language task descriptions into executable
plans — is related to guided process model discovery: both extract structured process
representations from experience. The key difference is authorial: process mining performs
automated discovery from logs, while NormCode's compilation is human-directed and
LLM-assisted, producing interpretable, portable artifacts rather than mined Petri nets.
The analogy strengthens the claim that NormCode's case library grows through a principled
experience-to-model distillation process rather than ad-hoc workflow accumulation.

---

**References** *(for paper compilation — BibTeX entries in `references.bib`)*

- Aamodt & Plaza (1994) AI Communications 7(1):39–59
- Bergmann (2002) LNCS 2432, Springer
- Bergmann & Gil (2014) Information Systems 40:115–127
- Bergmann, Müller et al. (2016) FLAIRS 2016
- Bottrighi et al. (2016) Expert Systems with Applications 55:212–221
- Guo et al. (2024) DS-Agent (arXiv)
- Ihrig & Kambhampati (1997) JAIR
- Kolodner (1993) Morgan Kaufmann
- Leake & Kendall-Morwick (2008) ECCBR, LNAI 5239
- Lenz, Hoffmann & Bergmann (2025) ICCBR 2025, LNCS 15662:126–141
- López de Mántaras et al. (2005) Knowledge Engineering Review 20(3):215–240
- Minor, Montani & Recio-García (2014) Information Systems 40:103–105
- Müller & Bergmann (2015a) POQL — LWA 2015, CEUR Vol.1458:247–255
- Müller & Bergmann (2015b) Generalized Cases — FLAIRS 2015
- Rubin, Herzig & Berant (2022) NAACL 2022
- van der Aalst (2011) Springer
- van der Aalst, Weijters & Maruster (2004) Workflow Mining
- Veloso (1997) ICCBR 1997
- Wilkerson & Leake (2024) ICCBR 2024, LNCS
- Wu et al. (2023) AutoGen (arXiv:2308.08155)
- Xu et al. (2023) kNN Prompting, ICLR 2023
- Zhang, Feng & Tan (2022) EMNLP 2022
