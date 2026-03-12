# 11. Conclusion

We have argued that Case-Based Reasoning in LLM workflow execution requires a reasoning
medium — a representational language with six properties (Interpretable, Enforceable,
Composable, Locally Addressable, Generalizable, Portable) — and demonstrated that when
such a medium exists, CBR is realized natively at two levels without requiring
additional machinery.

**Level 1** is immediate: every execution checkpoint is a suspended NormCode runtime
(Blackboard + Concept Repository snapshot) — a self-contained, resumable case whose
integrity is guaranteed by the scope rule. The four CBR operations map directly onto
Canvas interactions: Retrieve via Tensor Inspector inspection, Reuse via Fork, Revise
via Value Override with automatic stale-boundary computation, Retain via continuous
automatic checkpointing. The case base is the SQLite checkpoint store; it grows with
every run.

**Level 2** is the deeper contribution: each compiled NormCode plan is an abstract
case — a runtime definition from which all executions of that task type are
instantiated. Four production-ready plans serve as an initial case library of abstract
reasoning patterns. The compilation pipeline is the distillation process; it is itself a NormCode
plan, demonstrating recursive case-based learning: the medium can reason about and
improve its own case abstraction process, with self-hosted compilation as the validation.

**Three measurable properties** follow structurally from this architecture: C1
(failure localization in O(1) operations — exact bounded inputs via Tensor Inspector),
C2 (zero-cost pre-execution review — `.ncn` narrative before any LLM call), and C3
(scope-bounded selective re-run — only downstream-stale nodes re-execute on revision).
These properties are absent from existing LLM workflow tools — not because those tools
lack features, but because they lack the reasoning medium that would make these
properties structural rather than optional.

**For CBR.** NormCode contributes a new case type (the suspended runtime, stronger than
a workflow trace or a process model), a new case quality guarantee (structural isolation
as a formal precondition, not a convention), and a concrete deployed instance of
two-level POCBR in a production LLM workflow system. The four production-ready plans
and two case studies provide initial evidence that the architecture operates as claimed.

**For LLM workflows.** The CBR framing clarifies what the checkpoint system is: a case
base from which past experience can be retrieved, reused, and improved. This reframing
suggests research investments — learned similarity for automated fork selection,
competence-based case base maintenance, cross-plan reuse — that are well-studied in
CBR and unexplored in LLM workflow tooling.

**Availability.** NormCode Canvas (v1.1.3) is available for download. The language,
compiler, and orchestrator are open. A live web demo of the PPT Agent is available.
The formal language specification is documented in [Anon. 2025].

**Future work.** Immediate priorities: (1) learned similarity measures for automated
fork target selection — training on past reuse outcomes to recommend checkpoints; (2)
case base maintenance policies — competence-based pruning and quality-based filtering;
(3) formal evaluation against baseline frameworks on established multi-step reasoning
benchmarks; (4) cross-plan Level 2 retrieval — adapting abstract cases across workflow
domains (e.g., using the Code Assistant plan as a starting point for a new research
pipeline plan).

---

## Acknowledgements

*[To be completed by authors.]*

## Generative AI Statement

*[To be completed per ICCBR 2026 submission requirements.]*

## References

*[Full BibTeX entries in `references.bib`. Key entries:]*
*Aamodt & Plaza (1994); Bergmann (2002); Bergmann & Gil (2014);*
*Bottrighi et al. (2016); Guo et al. (2024); Ihrig & Kambhampati (1997);*
*Kolodner (1993); Leake & Kendall-Morwick (2008); Lenz et al. (2025);*
*López de Mántaras et al. (2005); Minor et al. (2014);*
*Müller & Bergmann (2015a, 2015b); Rubin et al. (2022); van der Aalst (2011);*
*Veloso (1997); Wilkerson & Leake (2024); Wu et al. (2023);*
*[Anon. 2025] (NormCode companion paper).*
