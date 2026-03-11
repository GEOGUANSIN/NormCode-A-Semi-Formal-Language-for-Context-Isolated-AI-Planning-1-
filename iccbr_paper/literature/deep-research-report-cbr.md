# NormCode 作为推理媒介的双层案例推理：ICCBR 2026 文献综述深度研究简报

## 研究目标与检索范围

本研究简报面向你给出的 ICCBR 2026 “Deployed Applications”论文论题：把 **NormCode**定位为一种“推理媒介（reasoning medium）”，并主张它以**两层**方式原生实现案例推理（CBR）：  
层一把“执行检查点/可恢复的运行时（suspended runtime）”当作具体案例；层二把“NormCode 计划/运行时定义（plan as runtime definition）”当作抽象案例，并以编译管线作为从执行到抽象的“蒸馏/保留（distillation/retain）过程”，以及以自托管编译器形成递归式的 CBR。该主张的语言与系统细节来自你指定的 companion paper：arXiv:2512.10563。citeturn14search0turn14search12turn14search8

为覆盖 ICCBR/CBR 社群的相关工作，我把检索重点放在你标注的 P1/P2 类别，并用可直接获取的原文 PDF、出版社目录页、作者主页/机构镜像、CEUR/AAAI 等开放论文源进行交叉核对。涉及“近期进展/会议论文（2023–2025）”的条目，优先使用 ICCBR 2023–2025 的 Springer 目录与可公开的作者自存版本。citeturn13view0turn13view2turn12search0turn24search14

---

## CBR 基础：经典 4R 循环与“案例”概念边界

### 核心文献卡片

**Aamodt & Plaza (1994)**  
1) 完整引文：entity["people","Agnar Aamodt","cbr researcher"] 与 entity["people","Enric Plaza","ai researcher"]. “Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches.” *AI Communications*, 7(1), 39–59, 1994.（常被视为标准 CBR 循环的奠基性综述之一）citeturn6view2  
2) 两句总结：论文用知识层/任务分解的方式组织 CBR 方法，系统化讨论了案例表示、检索、复用、修正与保留等核心问题，并给出可操作的任务分解视角。其“从以往经验解决新问题”的范式化表述，为后续把“流程/工作流”纳入“经验载体”提供了方法论入口。citeturn6view2  
3) 与 NormCode 论题的关系：**支持（基础语义锚点）**。NormCode 需要在 Related Work 中把“层一 checkpoint case / 层二 plan case”明确映射到 4R 的哪一步（尤其 Retrieve/Reuse/Retain）。citeturn6view2turn14search0  
4) 缺口或一致性：Aamodt & Plaza 的“case memory/representation”讨论强调“存什么、怎么组织、怎么索引”，但并未把“可恢复运行时状态”当作案例类型来专门讨论；这为你提出“runtime-state-as-case”的新颖性声明留下空间（但也意味着你要补上定义与完整性标准）。citeturn6view2  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义（该文语境）：以“经验”为核心，可被实现为问题-解或更复杂知识结构；重点在案例记忆的结构与索引。citeturn6view2  
- 多层结构：提供任务分解/方法学分层，但未提出“同时存在的双层案例库”。citeturn6view2  
- 隔离/完整性：讨论“存储内容与组织”，但没有把“执行隔离（isolation）”作为案例可靠性的系统性约束。citeturn6view2  

**Kolodner (1993)**  
1) 完整引文：entity["people","Janet Kolodner","cbr researcher"]. *Case-Based Reasoning*. Morgan Kaufmann, 1993.（开放材料：书前页/章节导读）citeturn15search0turn15search12  
2) 两句总结：该书对“什么是案例”“案例应包含哪些信息”“检索/适应/学习的工程权衡”做了系统化梳理，并以多系统案例贯穿。它把“案例可以是情境/事件/过程性经验的记录”这一更宽的案例观念，变成 CBR 教科书式共识。citeturn15search0turn15search12  
3) 与 NormCode 论题的关系：**支持（案例表示与完整性讨论的经典依托）**。NormCode 的“checkpoint=case”如果要站得住，需要对照 Kolodner 讨论的“案例内容、结构、索引、更新”给出你自己的“案例完整性/污染（contamination）”规范。citeturn15search0turn14search0  
4) 缺口或一致性：Kolodner 的案例观念足够宽以容纳“过程/轨迹”，但书的讨论主要以认知/任务层面的案例表示为主，并未触及“把可恢复执行环境（stack/heap/IO bindings 等）封装为案例对象”的工程化定义。citeturn15search0  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义：书中专设“What is a case?”，强调案例是关于具体情境的可复用记忆单元（可包含问题、情境、方案、结果、解释等）。citeturn15search12turn15search0  
- 多层结构：讨论记忆组织与抽象/概括的重要性，但不等同于你要的“两个并行案例层”。citeturn15search0  
- 隔离/完整性：强调案例内容与可复用性，但“执行隔离”不是该时代的中心议题；因此你需要把“隔离”重新解释为“案例可追溯/可审计/可复现实验条件”的现代对应物。citeturn14search0turn15search0  

**López de Mántaras et al. (2005)**  
1) 完整引文：entity["people","Ramon López de Mántaras","ai researcher"] 等. “Retrieval, reuse, revision and retention in case-based reasoning.” *The Knowledge Engineering Review*, 20(3), 215–240, 2005. DOI: 10.1017/S0269888906000646.citeturn15search9turn15search6  
2) 两句总结：该综述把 CBR 的 4R 分解与研究脉络做了广谱回顾，尤其强调“适应知识瓶颈”“相似度度量”“保留与维护”等长期主题。作为社群共识型文献，它非常适合用来给 NormCode 的两层映射提供“术语对齐”。citeturn15search6turn15search9  
3) 与 NormCode 论题的关系：**支持（术语与研究问题清单）**。你可以把“层二编译蒸馏”定位为一种特殊的 retain/maintenance 机制，把“层一检查点 fork/compare”定位为 revision 的可操作形态。citeturn15search6turn14search0turn14search12  
4) 缺口或一致性：该文覆盖大量 CBR 变体，但对“流程轨迹/运行时状态作为案例”的专门化定义较少；因此它更适合作为“综述背书”，而不是“直接先行工作”。citeturn15search6  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义：延续“经验驱动、从过去情形复用到新问题”的宽定义。citeturn15search6  
- 多层结构：提及抽象、泛化、适应等，但不提出你要的“episode + pattern”双层并行结构。citeturn15search6  
- 隔离/完整性：把“案例质量/维护”作为主题之一，但不含你所说的“跨步骤污染”这一 LLM 工作流特有问题设定。citeturn15search6turn14search0  

```bibtex
@article{AamodtPlaza1994,
  author  = {Aamodt, Agnar and Plaza, Enric},
  title   = {Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches},
  journal = {AI Communications},
  volume  = {7},
  number  = {1},
  pages   = {39--59},
  year    = {1994}
}

@book{Kolodner1993,
  author    = {Kolodner, Janet L.},
  title     = {Case-Based Reasoning},
  publisher = {Morgan Kaufmann},
  year      = {1993},
  isbn      = {1558602372}
}

@article{LopezDeMantaras2005RRRR,
  author  = {L{\'o}pez de M{\'a}ntaras, Ramon and McSherry, David and Bridge, Derek and Leake, David and Smyth, Barry and Craw, Susan and Faltings, Boi and Maher, Mary Lou and Cox, Michael T. and Forbus, Kenneth and Keane, Mark and Aamodt, Agnar and Watson, Ian},
  title   = {Retrieval, reuse, revision and retention in case-based reasoning},
  journal = {The Knowledge Engineering Review},
  volume  = {20},
  number  = {3},
  pages   = {215--240},
  year    = {2005},
  doi     = {10.1017/S0269888906000646}
}
```

---

## POCBR 现状：工作流/流程作为案例、部分流程检索与适应

POCBR（process-oriented CBR）最直接地回答了你研究问题 1：“工作流轨迹是否被当作案例”。从可获取的文献看，POCBR 的主流做法是把**流程模型/工作流图（workflow model as graph）**当作案例；同时也存在把**执行痕迹/事件日志（trace/event log）**当作案例来源、用于运行中检索与建议（operational support）的路线。citeturn7search8turn16view2turn22search1turn18view0

### 核心文献卡片

**Bergmann (2002)**  
1) 完整引文：entity["people","Ralph Bergmann","cbr researcher"]. *Experience Management: Foundations, Development Methodology, and Internet-Based Applications*. LNCS 2432, entity["company","Springer","academic publisher"], 2002. DOI: 10.1007/3-540-45759-3.citeturn6view0  
2) 两句总结：该书以“经验管理（experience management）”为总框架，把 CBR 与组织知识/流程经验的长期积累联系起来，并在此脉络下发展面向过程/工作流的经验复用思想。它通常被视为 POCBR 的关键理论背景之一（你计划中将其定位为“foundational POCBR text”与社群引用习惯一致）。citeturn6view0turn16view2  
3) 与 NormCode 论题的关系：**支持（POCBR 的理论母体）**。NormCode 的“工作流=案例、流程经验可复用”可以在此框架下被解释为“经验单元的可管理化”；但你需要进一步把“隔离/可审计”提升为经验管理里“经验可靠性”的新维度。citeturn6view0turn14search0  
4) 缺口或一致性：该书年代较早，主要围绕经验对象与管理流程展开；对“LLM 工作流的检查点可靠性/污染”没有直接论述，因此更适合作为“POCBR 正当性来源”，而非“runtime checkpoint case”的直接先行工作。citeturn6view0turn14search0  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义：以“经验对象/经验单元”统领，允许过程性经验成为可复用对象。citeturn6view0  
- 多层结构：经验管理框架允许抽象层（best practices）与实例层并存，但你仍需用更贴近 CBR 文献的“多层案例结构”来对齐。citeturn6view0turn16view0  
- 隔离/完整性：经验管理强调组织化与复用价值，但对你所强调的“跨步骤数据污染”缺乏现代 LLM 视角下的形式化约束。citeturn14search0  

**Minor, Montani & Recio-García (2014)**  
1) 完整引文：entity["people","Mirjam Minor","cbr researcher"] 等. “Process-oriented case-based reasoning.” *Information Systems*, 40, 103–105, 2014. DOI: 10.1016/j.is.2013.06.004.citeturn7search8  
2) 两句总结：该短文作为编者导读性质文本，明确把 POCBR 描述为将 CBR 原则应用到流程/工作流管理的方向，并强调它与工作流复用、流程建模支持等问题的关系。它适合在论文中用一句话把 POCBR 的“研究对象”定性：经验以过程模型与流程知识呈现。citeturn7search8  
3) 与 NormCode 论题的关系：**直接支持（POCBR 的社群定义锚点）**。你可以把 NormCode 的层二“计划/运行时定义”解释为一种更严格的“过程知识表示”，从而把论文放进 POCBR 的主叙事。citeturn7search8turn14search0  
4) 缺口或一致性：该文不是技术细节论文，因此对“部分状态检索（从 step k 开始）”“中间状态表示”不会给出算法答案，需要你用后续具体 POCBR 工作补齐。citeturn7search8turn16view3  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义：默认“过程/工作流”可作为案例载体。citeturn7search8  
- 多层结构：未展开。citeturn7search8  
- 隔离/完整性：未展开。citeturn7search8  

**Bergmann & Gil (2014)**  
1) 完整引文：entity["people","Yolanda Gil","ai researcher"] 与 Bergmann. “Similarity Assessment and Efficient Retrieval of Semantic Workflows.” *Information Systems*, 40, 115–127, 2014. DOI: 10.1016/j.is.2012.07.005.（可获取预印本）citeturn16view2turn7search17  
2) 两句总结：论文用“语义标注有向图（semantically labeled graphs）”统一表示工作流，并给出工作流相似度与高效检索算法（强调结构匹配与知识密集型相似度）。它把“工作流案例检索”推进到可工程化的图检索与相似度计算层面，是 POCBR 中“案例=工作流图”的代表性技术路线。citeturn16view2turn7search17  
3) 与 NormCode 论题的关系：**支持 + 可对比**。NormCode 的层二“计划定义”可以对照这里的“workflow graph”作为抽象案例；你也可以指出：Bergmann & Gil 关注工作流结构与语义相似度，但并不保证“每个中间点的输入是可审计且未被污染的”，因此无法自然推出“checkpoint 的案例可靠性”。citeturn16view2turn14search0  
4) 缺口或一致性：POCBR 在此路线下把“案例”基本等同为“过程模型”，而不是等同为“运行中状态”；这正是你论文层一主张需要明确“与主流不同”的地方。citeturn16view2turn14search0  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义：案例库是工作流（图）库，检索对象是相似工作流结构。citeturn16view2  
- 多层结构：隐含“语义抽象（ontology/taxonomy）”用于相似度，但并非并行双层案例库。citeturn16view2turn16view0  
- 隔离/完整性：工作流图路线通常默认步骤数据流存在，但不会把“隔离”作为案例正确性公理；NormCode 可在此形成差异化。citeturn16view2turn14search0  

**Müller & Bergmann (2015, POQL)**  
1) 完整引文：entity["people","Gilbert Müller","cbr researcher"] 与 Bergmann. “POQL: A New Query Language for Process-Oriented Case-Based Reasoning.” In *Proceedings of the LWA 2015 Workshops*, CEUR-WS Vol.1458, 2015, pp. 247–255.（开放 PDF）citeturn16view3turn15search29  
2) 两句总结：论文指出 POCBR 常见交互设置是：用户正在构建一个**部分工作流**作为查询，系统检索相似工作流以用于“自动补全/复用与适应”，因此需要更贴合用户表达的查询语言。它把“从中间开始（partial workflow as query）”变成显式假设，为你论文里“从 step k 开始检索”提供了最接近的 POCBR 先行语境。citeturn16view3  
3) 与 NormCode 论题的关系：**强支持（部分流程检索）**。层一“checkpoint case”可以被解释为比“partial workflow query”更强的对象：不仅有结构片段，还有可恢复的执行上下文与已绑定输入输出；你需要据此强调 NormCode 的新颖点在于“状态严密性与可恢复性”。citeturn16view3turn14search0  
4) 缺口或一致性：POQL 把“部分工作流”当作查询，但案例库仍以“工作流模型”为主；它没有把“运行时快照”作为案例一等公民。citeturn16view3  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义：案例库=语义工作流；查询=正在设计的部分工作流/需求约束。citeturn16view3  
- 多层结构：未主打“双层案例”，但对“查询作为部分结构”给出了明确建模。citeturn16view3  
- 隔离/完整性：讨论重点在表达能力与检索匹配，不涉及“中间点输入污染”。citeturn16view3turn14search0  

**Bergmann et al. (2016, Retrieval of adaptable workflow cases)**  
1) 完整引文：Bergmann, Müller, entity["people","Christian Zeyen","cbr researcher"] 等. “Retrieving Adaptable Cases in Process-Oriented Case-Based Reasoning.” In *Proceedings of FLAIRS*, 2016.（开放 PDF）citeturn2view1  
2) 两句总结：论文提出在 POCBR 检索阶段显式考虑“可适应性（adaptability）”，并通过离线分析/模拟适应执行来学习案例的可适应评级，再将其引入检索排序。其贡献在于把“检索-适应耦合”前移，强调在案例稀缺时适应能力对成功复用的重要性。citeturn2view1  
3) 与 NormCode 论题的关系：**支持（层二：抽象案例与适应驱动检索的论证素材）**。你可用它类比 NormCode 层二的“编译蒸馏”：通过管线把适应/复用的先验结构化，减少在线不确定性。citeturn2view1turn14search0  
4) 缺口或一致性：该文的“可适应性学习”仍建立在“工作流案例”的结构表示上，不触及“运行时状态案例”的隔离要求；因此它更像 NormCode 层二的相关工作，而不是层一。citeturn2view1turn14search0  
5) BibTeX：见本节末尾汇总代码块。  

### POCBR 版图表：系统 × 案例表示 × 检索 × 适应 × 领域

| POCBR/相邻系统 | 案例表示类型 | 检索方法 | 适应/复用方法 | 典型领域 |
|---|---|---|---|---|
| Phala（Leake & Kendall‑Morwick） | 从 provenance/执行痕迹挖掘的工作流片段/轨迹案例 | 从大型 trace 库中检索相关工作流/片段用于交互式构建 | 以“知识轻量”方式复用先前片段（强调用户交互与可扩展性问题） | e‑Science 科学工作流citeturn18view0 |
| 语义工作流检索（Bergmann & Gil） | 语义标注工作流图（semantic workflow graph） | 图相似度 + 高效检索（算法化相似度计算与选择交织） | 主要聚焦检索；为后续适应提供基础 | 科学工作流、业务工作流citeturn16view2 |
| POQL 查询 + POCBR（Müller & Bergmann） | 案例库=语义工作流图；查询=部分工作流/约束 | 用查询语言表达需求以驱动相似检索 | 面向“自动补全/适应支持”的查询建模 | 以烹饪工作流作例citeturn16view3 |
| 可适应性引导检索（Bergmann et al.） | 工作流图案例 + 可适应性元数据 | 相似度 + 离线学习的可适应评分融合 | 通过离线模拟适应执行估计“可适应性”，增强在线成功率 | 烹饪工作流实验citeturn2view1 |

> 解释：表中“案例表示”全部落在“过程模型/轨迹”层面；它们支持你论文的 POCBR 背景与“查询可从部分流程出发”，但并不自动推出“可恢复运行时状态=案例”的层一主张，需要你在下一节把缺口说清楚。citeturn16view3turn14search0

```bibtex
@book{Bergmann2002ExperienceManagement,
  author    = {Bergmann, Ralph},
  title     = {Experience Management: Foundations, Development Methodology, and Internet-Based Applications},
  series    = {Lecture Notes in Computer Science},
  volume    = {2432},
  publisher = {Springer},
  year      = {2002},
  doi       = {10.1007/3-540-45759-3},
  isbn      = {3-540-44191-3}
}

@article{MinorMontaniRecioGarcia2014POCBR,
  author  = {Minor, Mirjam and Montani, Stefania and Recio-Garc{\'i}a, Juan A.},
  title   = {Process-oriented case-based reasoning},
  journal = {Information Systems},
  volume  = {40},
  pages   = {103--105},
  year    = {2014},
  doi     = {10.1016/j.is.2013.06.004}
}

@article{BergmannGil2014SemanticWorkflows,
  author  = {Bergmann, Ralph and Gil, Yolanda},
  title   = {Similarity Assessment and Efficient Retrieval of Semantic Workflows},
  journal = {Information Systems},
  volume  = {40},
  pages   = {115--127},
  year    = {2014},
  doi     = {10.1016/j.is.2012.07.005}
}

@inproceedings{MuellerBergmann2015POQL,
  author    = {M{\"u}ller, Gilbert and Bergmann, Ralph},
  title     = {POQL: A New Query Language for Process-Oriented Case-Based Reasoning},
  booktitle = {Proceedings of the LWA 2015 Workshops},
  series    = {CEUR Workshop Proceedings},
  volume    = {1458},
  pages     = {247--255},
  year      = {2015},
  publisher = {CEUR-WS.org}
}

@inproceedings{BergmannEtAl2016AdaptableRetrieval,
  author    = {Bergmann, Ralph and M{\"u}ller, Gilbert and Zeyen, Christian and Manderscheid, Jens},
  title     = {Retrieving Adaptable Cases in Process-Oriented Case-Based Reasoning},
  booktitle = {Proceedings of the Florida Artificial Intelligence Research Society Conference (FLAIRS)},
  year      = {2016}
}
```

---

## 多层与层次化 CBR：从具体流程到模式模板的“双层”先行工作

你研究问题 3（多层/层次化 CBR）与问题 2（层二抽象案例）在可检索文献中，有一条非常关键且“命中你论文主张”的线索：**POCBR 里已经有人明确引入“广义/泛化案例（generalized case）”来覆盖子空间，并通过“专化（specialization）”回到具体情境**。这与 NormCode 层二“计划/运行时定义作为抽象案例、由编译蒸馏而来”的论证可以形成强对齐。citeturn16view0turn14search0

### 核心文献卡片

**Müller & Bergmann (2015, Generalized Cases in POCBR)**  
1) 完整引文：Müller & Bergmann. “Generalization of Workflows in Process-Oriented Case-Based Reasoning.” In *Proceedings of FLAIRS*, 2015.（开放 PDF）citeturn16view0  
2) 两句总结：论文把“泛化案例”引入 POCBR：传统案例覆盖单点，而泛化案例覆盖表示空间的一个子空间，从而提升覆盖度并可能减少案例库规模；之后再针对查询进行“专化”以得到可执行/可用的具体工作流。它同时把“泛化/专化”解释为一种适应变换，并强调借助轻量本体/分类体系来指导泛化。citeturn16view0  
3) 与 NormCode 论题的关系：**强先行工作（层二）**。你可以把 NormCode 层二“计划作为抽象案例”直接类比为“generalized case”，把编译管线的 distillation 定位为一种“从实例到泛化案例的学习/构造过程”；同时指出 NormCode 的差异：你的“抽象案例”是可移植的运行时定义，并且来自“带隔离约束的可审计执行”。citeturn16view0turn14search0  
4) 缺口或一致性：该文的泛化目标是“工作流结构与语义项”的抽象，而不是“从执行检查点沉淀出可复用的计划定义”；此外它不讨论 LLM 工作流的随机性与隔离，因此你需要把“隔离”作为 NormCode 对多层 CBR 的关键增量。citeturn16view0turn14search0  
5) BibTeX：见本节末尾汇总代码块。  
CBR 附加项：  
- 案例定义：同时承认“具体工作流案例”与“泛化案例”，并给出泛化案例覆盖子空间的直观定义。citeturn16view0  
- 多层结构：**明确存在**（具体案例 ↔ 泛化案例），非常适合作为你“双层架构”的最强对照文献之一。citeturn16view0  
- 隔离/完整性：不把隔离当作案例公理；主要关注结构泛化与检索/适应效率。citeturn16view0turn14search0  

**Veloso (1997, Case-based Planning / Replay)**  
1) 完整引文：entity["people","Manuela Veloso","ai researcher"]. “Merge Strategies for Multiple Case Plan Replay.” In *ICCBR 1997* (paper PDF).citeturn23search8  
2) 两句总结：论文把“计划生成的经验”表示为可检索、可回放（replay）的“规划案例”，并研究多案例回放时的合并策略，体现了“把求解过程当经验对象”的思想。它对你“层二：自托管/递归式 CBR（系统用自己的推理过程改进未来推理）”提供了历史上的近亲：case-based planning 通过存储与回放规划经历来提速与增强。citeturn23search8  
3) 与 NormCode 论题的关系：**支持（递归 CBR 的谱系证据）**。你可以用它说明：在 CBR 的更广义实践里，“case”并不必然是静态问题-解对，也可以是“过程/派生/回放脚本”；NormCode 层二把这种思路推向“可审计、可移植的运行时定义”。citeturn23search8turn14search0  
4) 缺口或一致性：该路线的案例通常是“计划/派生轨迹”，而不是“可恢复运行时环境”；因此它更像你层二“plans as abstract cases”的先行谱系，而非层一“runtime checkpoint”。citeturn23search8turn14search0  
5) BibTeX：见本节末尾汇总代码块。  

**Ihrig & Kambhampati (1997, Plan Derivations as Cases)**  
1) 完整引文：entity["people","Lauryn Ihrig","ai researcher"] 与 entity["people","Subbarao Kambhampati","ai researcher"]. “Storing and Indexing Plan Derivations through Explanation-Based Learning.” *Journal of Artificial Intelligence Research (JAIR)*, 1997.（开放 PDF）citeturn23search0  
2) 两句总结：论文围绕“派生类比（derivational analogy）”把规划器的求解派生过程存储为可索引案例，并通过解释型学习增强索引/回放框架，以便在新问题上复用过去的规划推导。它再次证明“过程轨迹/推理派生本身可以被 CBR 化”，为你提出“编译管线=蒸馏过程、self-hosting=递归式 CBR”提供学术语境。citeturn23search0turn23search12  
3) 与 NormCode 论题的关系：**支持（层二的“过程作为案例”的传统）**。NormCode 的关键差异在于：它把“过程”进一步落到“可执行、可审计、可隔离的数据流与检查点对象”。citeturn23search0turn14search0  
4) 缺口或一致性：该工作强调规划推导的存储/索引，但不是面向 LLM 工作流的执行隔离；因此你仍需把隔离作为现代系统约束补进来。citeturn23search0turn14search0  
5) BibTeX：见本节末尾汇总代码块。  

```bibtex
@inproceedings{MuellerBergmann2015Generalization,
  author    = {M{\"u}ller, Gilbert and Bergmann, Ralph},
  title     = {Generalization of Workflows in Process-Oriented Case-Based Reasoning},
  booktitle = {Proceedings of the Florida Artificial Intelligence Research Society Conference (FLAIRS)},
  year      = {2015}
}

@inproceedings{Veloso1997PlanReplay,
  author    = {Veloso, Manuela M.},
  title     = {Merge Strategies for Multiple Case Plan Replay},
  booktitle = {Case-Based Reasoning Research and Development (ICCBR)},
  year      = {1997}
}

@article{IhrigKambhampati1997Derivations,
  author  = {Ihrig, Lauryn H. and Kambhampati, Subbarao},
  title   = {Storing and Indexing Plan Derivations through Explanation-Based Learning},
  journal = {Journal of Artificial Intelligence Research},
  year    = {1997}
}
```

---

## 运行时状态或执行痕迹作为案例：最接近先行工作与可陈述的缺口

你研究问题 2（“runtime states/suspended execution environments 是否被当作案例？”）在现有可获取 CBR 文献中，最接近的并不是“把整个执行环境快照当案例”，而是两类近邻：

第一类是 **workflow execution traces / event logs 被当作案例来源**，支持“运行中 operational support”：当一个流程实例执行到某一步时，用其已发生的前缀/模式去检索历史轨迹案例，从而推荐下一步或预测结局。citeturn18view0turn22search1turn22search27  

第二类是 **case-based planning 的 derivational trace / replay**：把求解过程（推导轨迹）当作“可回放经验对象”，服务于下一次搜索。citeturn23search0turn23search8turn23search12  

这两类都能帮助你“把层一/层二说得像 CBR”，但它们仍不足以构成你层一主张的直接先行艺术语——因为你要的层一案例是“可恢复执行环境（suspended NormCode runtime）”，强调 **检查点可恢复、输入输出显式、且具有隔离保证**。NormCode paper 对“每步强制数据隔离、消除跨步污染、使中间状态可检查”的表述，正是你把“checkpoint → 可靠案例”的关键前提。citeturn14search0turn14search8

### 核心文献卡片

**Leake & Kendall‑Morwick (2008)**  
1) 完整引文：entity["people","David Leake","cbr researcher"] 与 entity["people","Joseph Kendall-Morwick","ai researcher"]. “Towards Case-Based Support for e-Science Workflow Generation by Mining Provenance.” In *ECCBR 2008 / LNAI 5239*, 2008.（Springer 预览 PDF 可得）citeturn18view0turn2view3  
2) 两句总结：论文明确提出：如果系统能够捕获工作流执行的 provenance/轨迹，那么这些轨迹可以被“挖掘为案例”，用于交互式帮助用户构建新工作流，并指出“case mining、可扩展性、交互性”等问题。它是你“workflow traces as cases”的高质量、可引用先行工作，尤其适合回答研究问题 1 与 6 的交叉点。citeturn18view0  
3) 与 NormCode 论题的关系：**强支持（trace→case 的明确宣称）**。你可以把 NormCode 层一“checkpoint case”表述为对该路线的强化：你不仅基于轨迹文本/低层日志，而是基于具有隔离与显式数据流的运行时快照，从而让“从轨迹到案例”的映射更可靠、更可审计。citeturn18view0turn14search0  
4) 缺口或一致性：该文把“执行轨迹可挖掘为案例”讲清楚，但并不等同于“完整 suspended runtime = 案例”；它强调 provenance 是低层视角，且需要把低层执行视图映射到用户的抽象表示，这与你层二“编译蒸馏”的叙事可形成对应。citeturn18view0turn14search0  
5) BibTeX：见本节末尾汇总代码块。  

**Bottrighi et al. (2016)**  
1) 完整引文：entity["people","Alessio Bottrighi","ai researcher"] 等. “Trace retrieval for business process operational support.” *Expert Systems with Applications*, 55, 212–221, 2016. DOI: 10.1016/j.eswa.2015.12.002.citeturn22search1turn22search7  
2) 两句总结：论文把“事件日志中的历史执行轨迹（traces）”视为案例，并在流程运行中用当前实例的已发生行为作为查询，检索相似历史轨迹以支持预测/推荐等 operational support（论文摘要与目录页明确如此表述）。它为“运行中部分状态检索”提供了非常贴近你叙事的 business-process 版本：从“已经发生的部分”去找“接下来可能怎么走”的经验。citeturn22search1turn22search7  
3) 与 NormCode 论题的关系：**强支持（但仍非同一对象）**。它支持你论证“在流程/工作流领域，把运行时进行到某一步的状态（以 trace 前缀形式）用于案例检索是合理的”；而 NormCode 的增量是：把“部分 trace”提升为“可恢复且隔离的执行检查点”，使其成为更强、更可靠的案例对象。citeturn22search1turn14search0  
4) 缺口或一致性：Bottrighi 路线的“状态”更多是“执行历史的观测序列”，并不包含“完整执行环境”；因此它是你阐释“从 prefix 到 checkpoint”的关键桥梁文献，但仍允许你提出“suspended runtime as case”的明确缺口。citeturn22search1turn14search0  
5) BibTeX：见本节末尾汇总代码块。  

**Bottrighi et al. (2015, 医疗流程检索工作坊论文，开放 PDF)**  
1) 完整引文：Bottrighi 等. “Trace Retrieval as a Tool for Operational Support in Medical Process Management.”（开放 PDF，2015，ICCBR‑HS/相关工作坊语境）citeturn22search27turn22search13  
2) 两句总结：论文把医疗流程运行中的“当前实例行为模式”作为查询，在事件日志中检索历史 traces，以便实时指导专家决策，并强调用树结构/索引实现高效检索。它提供了比期刊摘要更具体的“查询=当前过程实例片段、案例=历史 trace”的操作化描述。citeturn22search27  
3) 与 NormCode 论题的关系：**支持（层一叙事可借鉴）**。你可以把 NormCode checkpoint case 解释为对这种“运行中检索”的强化：你不仅检索“相似 trace”，还可以 fork/replay 一个隔离的 checkpoint 来做对比实验与纠错。citeturn22search27turn14search0turn14search1  
4) 缺口或一致性：同样没有“执行环境快照”定义；案例仍主要是日志轨迹。citeturn22search27  
5) BibTeX：见本节末尾汇总代码块。  

> 关键缺口（可在论文中明确声明）：在主流 POCBR/trace-retrieval 文献里，“case”通常是**过程模型**或**执行轨迹**；它们支持“从中间开始检索/对运行中实例提供建议”，但很少把“包含所有可恢复绑定（变量、输入输出绑定、工具调用结果、受控数据流）的 suspended execution environment”定义为案例本体。NormCode 的贡献可以被表述为：首次将“隔离保证下的可恢复运行时”提升为案例，并以此让 checkpoint 具备案例完整性。citeturn14search0turn16view3turn22search1turn18view0  

```bibtex
@inproceedings{LeakeKendallMorwick2008ProvenanceCBR,
  author    = {Leake, David and Kendall-Morwick, Joseph},
  title     = {Towards Case-Based Support for e-Science Workflow Generation by Mining Provenance},
  booktitle = {Advances in Case-Based Reasoning (ECCBR)},
  series    = {Lecture Notes in Artificial Intelligence},
  year      = {2008}
}

@article{BottrighiEtAl2016TraceRetrievalESWA,
  author  = {Bottrighi, Alessio and Canensi, Luca and Leonardi, Giorgio and Montani, Stefania and Terenziani, Paolo},
  title   = {Trace retrieval for business process operational support},
  journal = {Expert Systems with Applications},
  volume  = {55},
  pages   = {212--221},
  year    = {2016},
  doi     = {10.1016/j.eswa.2015.12.002}
}

@inproceedings{BottrighiEtAl2015MedicalTraceRetrieval,
  author    = {Bottrighi, Alessio and Canensi, Luca and Leonardi, Giorgio and Montani, Stefania and Terenziani, Paolo},
  title     = {Trace Retrieval as a Tool for Operational Support in Medical Process Management},
  booktitle = {Workshop on Case-Based Reasoning in the Health Sciences (ICCBR-HS)},
  year      = {2015}
}
```

---

## CBR 与 LLM：研究版图、方向区分与 NormCode 的“反向/正交”定位

你研究问题 4 要求的“方向区分”在近三年的文献里非常清晰：  
大量工作是 **CBR→LLM**（用检索到的例子/案例改善单次或短上下文的 LLM 输出）；另一大类是 **LLM→CBR**（用 LLM 做相似度、索引、适应、知识工程，从而降低 CBR 的知识工程成本）。citeturn8search13turn10search1turn24search18turn9search9turn9search15  

而你为 NormCode 设定的贡献主张是第三种：**用 CBR 架构去管理多步 LLM 工作流的执行**，并把“可恢复运行时”作为案例对象。这更接近“workflow operational support + 强隔离检查点 + 双层案例化”的组合，而不是“给一次调用找 few-shot examples”。NormCode companion paper 对“每步隔离、消除隐式数据流、使中间状态可检查”的论证，正是你将该方向与主流区分开的核心依据。citeturn14search0turn16view3turn22search1  

### CBR+LLM 版图表：论文 × 方向 × “case”含义 × 与 NormCode 关系

| 代表论文 | 方向（CBR→LLM / LLM→CBR） | “case”在文中主要指什么 | 与 NormCode 的关系 |
|---|---|---|---|
| Rubin et al. 2022（EPR，检索 prompts） | CBR→LLM | 用作 in-context learning 的训练示例/提示样例 | 同样是“相似例子检索”，但目标是改善单次 ICL；与“执行管理/检查点案例”不同citeturn8search13turn8search4 |
| Zhang et al. 2022（Active Example Selection） | CBR→LLM | 被选择进入上下文的示例集合（策略学习选择） | 强化“示例选择的重要性”，但仍停留在上下文示例层，不触及工作流 checkpointciteturn10search1 |
| Xu et al. 2023（kNN Prompting） | CBR→LLM（近邻推断式） | 训练数据的近邻作为推断依据（近邻检索+聚合） | 与“近邻/案例”哲学相通，但对象不是运行时状态；可用于 Related Work 的“邻近方法”对照citeturn9search12turn9search1 |
| Wilkerson & Leake 2024（用 LLM 实现 CBR 部件） | LLM→CBR | 结构化病例/案例（以 LLM 评估相似、适应等） | 强相关：证明“LLM 可用来做 CBR 的相似与适应”；你的方向则是用 CBR 管工作流执行（相对正交）citeturn9search15turn10search9 |
| Lenz & Bergmann 2023（论证图+WordNet+LLM） | LLM→CBR（用于适应/改写） | 论证图案例 | 说明 LLM 可作为适应算子/知识源；与 NormCode 的“计划作为可验证媒介”形成对照citeturn12search1turn12search9 |
| Lenz et al. 2025（LLsiM） | LLM→CBR（相似度评估/配置） | 相似度比较对象（案例对） | 直接相关：用 LLM 降低相似度知识工程负担；你可以用它来定位“LLM 帮助 CBR”是主流，而你强调“CBR 管 LLM 工作流执行”citeturn24search18turn24search8 |
| Guo et al. 2024（DS-Agent） | CBR→LLM（用 CBR 框架迭代修订计划） | 数据科学实验/计划的经验片段（用于 revise） | 与你的“多步工作流管理”更近：用 CBR 迭代修订多步方案；但其“案例”不是隔离可复现的执行检查点citeturn8search15 |
| Sourati et al. 2023（LM-driven CBR 分类） | LLM→CBR（LM 驱动检索/适应） | 论证/文本案例 | 侧重“用 LM 提升 CBR 分类鲁棒性”，可作为“主流方向对照”citeturn8search33 |
| Watson 2023/2024（Case-based persistent memory） | CBR→LLM（记忆增强） | 持久记忆中的案例/经验单元 | 与 NormCode 的“case base 管理/增长”讨论相关，但仍不等于“隔离检查点=案例”citeturn9search9turn12search10 |
| Hatalis et al. 2025（CBR for LLM agents 综述） | 混合（多种整合框架） | 案例库作为 agent 记忆/检索对象 | 可用于概括性对照，但需要在论文中明确你是“workflow execution management”的特定子方向citeturn10search12turn10search28 |

### 核心文献卡片

**Rubin, Herzig & Berant (2022)**  
1) 完整引文：entity["people","Ohad Rubin","nlp researcher"] 等. “Learning To Retrieve Prompts for In-Context Learning.” *NAACL 2022*.（ACL Anthology PDF）citeturn8search13turn8search4  
2) 两句总结：论文把“选择哪些 few-shot 示例”视为可学习的检索问题，用 LM 信号标注正负样例并训练稠密检索器，从而在测试时为输入检索更合适的 prompts。它是“检索示例提升单次 LLM ICL”的代表文献，也最符合你计划里对 Rubin et al. 的指向。citeturn8search13  
3) 与 NormCode 论题的关系：**对照（非同向）**。它支持你论证“示例检索很重要”，但你的贡献不是“为一次调用找示例”，而是“用 CBR 管理多步执行，并把运行时检查点当案例”。citeturn8search13turn14search0  
4) 缺口或一致性：该线索缺少“工作流级执行状态”概念，无法解释“checkpoint 完整性/隔离”。citeturn14search0  
5) BibTeX：见本节末尾汇总代码块。  

**Wilkerson & Leake (2024)**  
1) 完整引文：entity["people","Kaitlynne Wilkerson","ai researcher"] 与 Leake. “On Implementing Case-Based Reasoning with Large Language Models.” *ICCBR 2024 (LNCS)*, 2024.（作者公开 PDF；出版社 DOI 页可见）citeturn9search15turn10search9  
2) 两句总结：论文探索把 LLM 用作 CBR 管线中的能力部件，尤其用于相似度评估与推动“更像 CBR 的推理流程”，以缓解手工相似度/知识工程瓶颈。它是 ICCBR 近年里“LLM→CBR”方向最适合引用的论证型论文之一。citeturn9search15  
3) 与 NormCode 论题的关系：**相关但正交**。它塑造了“LLM 用来做 CBR”这一主流方向背景；你需要将 NormCode 定位为“用 CBR 结构来管理 LLM 工作流执行、并用强隔离使 checkpoint 成为可靠案例”。citeturn9search15turn14search0  
4) 缺口或一致性：该文的“case”通常仍是传统结构化记录，而非“可恢复运行时”；因此它不能替代你层一的先行工作，但能帮助你界定“领域主流讨论的案例含义”。citeturn9search15turn14search0  
5) BibTeX：见本节末尾汇总代码块。  

**Lenz, Hoffmann & Bergmann (2025, LLsiM)**  
1) 完整引文：entity["people","Mirko Lenz","cbr researcher"] 等. “LLsiM: Large Language Models for Similarity Assessment in Case-Based Reasoning.” *ICCBR 2025 (LNCS 15662)*, 2025, pp.126–141. DOI: 10.1007/978-3-031-96559-3_9.（公开版本）citeturn24search18turn24search8turn24search3  
2) 两句总结：论文系统比较用 LLM 直接打相似度分、做成对比较、或让 LLM 自动配置相似度模型等策略，目标是降低 CBR 相似度知识工程成本。它证明“LLM 可以进入 CBR 的 similarity 子系统”，并且把“相似度配置”本身当作可优化对象。citeturn24search18turn24search3  
3) 与 NormCode 论题的关系：**强相关（但方向不同）**。你可以引用它说明 ICCBR 近年的热点之一是“LLM→CBR”；然后强调 NormCode 的方向是“CBR→workflow execution management”，其关键在于隔离与可恢复 checkpoint。citeturn24search18turn14search0  
4) 缺口或一致性：LLsiM 处理的是“案例相似度评估”，并不处理“案例对象是否可靠（checkpoint 污染/隔离）”；这恰好让你把“隔离”突出为更底层的新问题。citeturn24search18turn14search0  
5) BibTeX：见本节末尾汇总代码块。  

```bibtex
@inproceedings{RubinHerzigBerant2022EPR,
  author    = {Rubin, Ohad and Herzig, Jonathan and Berant, Jonathan},
  title     = {Learning To Retrieve Prompts for In-Context Learning},
  booktitle = {Proceedings of NAACL-HLT},
  year      = {2022}
}

@inproceedings{ZhangFengTan2022ActiveExampleSelection,
  author    = {Zhang, Yiming and Feng, Shi and Tan, Chenhao},
  title     = {Active Example Selection for In-Context Learning},
  booktitle = {Proceedings of EMNLP},
  year      = {2022},
  doi       = {10.18653/v1/2022.emnlp-main.622}
}

@inproceedings{XuEtAl2023KNNPrompting,
  author    = {Xu, Benfeng and Wang, Quan and Mao, Zhendong and Lyu, Yajuan and She, Qiaoqiao and Zhang, Yongdong},
  title     = {$k$NN Prompting: Beyond-Context Learning with Calibration-Free Nearest Neighbor Inference},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2023}
}

@inproceedings{WilkersonLeake2024ImplementingCBRwithLLMs,
  author    = {Wilkerson, Kaitlynne and Leake, David},
  title     = {On Implementing Case-Based Reasoning with Large Language Models},
  booktitle = {Case-Based Reasoning Research and Development (ICCBR 2024), Lecture Notes in Computer Science},
  year      = {2024}
}

@inproceedings{LenzBergmann2023ArgumentGraphsLLM,
  author    = {Lenz, Mirko and Bergmann, Ralph},
  title     = {Case-Based Adaptation of Argument Graphs with WordNet and Large Language Models},
  booktitle = {Case-Based Reasoning Research and Development (ICCBR 2023), Lecture Notes in Computer Science},
  year      = {2023},
  doi       = {10.1007/978-3-031-40177-0_17}
}

@inproceedings{LenzHoffmannBergmann2025LLsiM,
  author    = {Lenz, Mirko and Hoffmann, Maximilian and Bergmann, Ralph},
  title     = {LLsiM: Large Language Models for Similarity Assessment in Case-Based Reasoning},
  booktitle = {Case-Based Reasoning Research and Development (ICCBR 2025), Lecture Notes in Computer Science},
  year      = {2025},
  doi       = {10.1007/978-3-031-96559-3_9}
}

@article{GuoEtAl2024DSAgent,
  author  = {Guo, Shiguang and others},
  title   = {DS-Agent: Automated Data Science by Empowering Large Language Models with Case-Based Reasoning},
  year    = {2024}
}

@inproceedings{SouratiEtAl2023FallacyCBRLM,
  author    = {Sourati, Zhivar and Ilievski, Filip and Sandlin, H{\^o}ng-{\^A}n and Mermoud, Alain},
  title     = {Case-Based Reasoning with Language Models for Classification of Logical Fallacies},
  booktitle = {Proceedings of IJCAI},
  year      = {2023}
}

@article{Watson2023CaseBasedPersistentMemory,
  author = {Watson, Ian},
  title  = {A Case-Based Persistent Memory for a Large Language Model},
  year   = {2023},
  eprint = {2310.08842},
  archivePrefix = {arXiv}
}

@article{Hatalis2025CBRforLLMAgents,
  author = {Hatalis, Konstantinos and others},
  title  = {Review of Case-Based Reasoning for LLM Agents},
  year   = {2025},
  eprint = {2504.06943},
  archivePrefix = {arXiv}
}
```

---

## 关联邻域：过程挖掘与推理媒介语言、工具检查点与自托管

### 过程挖掘与“从执行到模型”的对应关系

你研究问题 6 可以用过程挖掘（process mining）来建立强类比：过程挖掘的核心任务之一就是从事件日志（event log）中发现过程模型，并通过一致性检查（conformance checking）比较“应然模型”与“实然执行”。citeturn19search4turn20view1turn19search17turn19search13  

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["process mining event log alpha algorithm Petri net workflow mining diagram","conformance checking process mining alignment illustration","semantic workflow graph case-based reasoning process-oriented CBR diagram"],"num_per_query":1}

一个对 NormCode 很有用的写法是：  
- 把“层一：执行检查点/轨迹库”类比为过程挖掘中的“event log / traces”；  
- 把“层二：计划/运行时定义库”类比为过程挖掘中的“process model”（但 NormCode 的计划是可执行的、并可被编译为严格的运行时定义）；  
- 把“Derivation→Formalization→Post‑Formalization→Activation（你的编译蒸馏管线）”表述为一种“人类/LLM 协作的、目标导向的模型发现与规整（guided discovery and normalization）”，不同于传统过程挖掘常见的纯自动发现。NormCode paper 对“渐进式形式化（progressive formalization）”与“位于自然语言与完全形式化之间”的定位，可作为你的“半形式推理媒介”主张核心引文。citeturn14search2turn14search8turn14search12  

对应的过程挖掘基础文献可用两篇支柱来拿下“定义与权威性”：

**van der Aalst (2011, Process Mining book)**  
- 完整引文：entity["people","Wil van der Aalst","process mining researcher"]. *Process Mining: Discovery, Conformance and Enhancement of Business Processes*. Springer, 2011. DOI: 10.1007/978-3-642-19345-3.citeturn19search4turn19search0  
- 价值：为“过程挖掘=从事件数据抽取过程信息（发现/一致性/增强）”提供权威定义，支持你把“编译蒸馏”放入更宽的“从执行到模型”的谱系。citeturn19search4turn14search0  

**van der Aalst, Weijters & Maruster (2004, α-algorithm workflow mining)**  
- 完整引文：van der Aalst 等. “Workflow Mining: Discovering Process Models from Event Logs.” 2004.（开放 PDF）citeturn20view1  
- 价值：非常明确地把“日志（workflow log）→模型（WF-net/Petri net）”表述为 workflow rediscovery 问题，能用来对照你层二的“trace→plan distillation”叙事。citeturn20view1  

```bibtex
@book{vanDerAalst2011ProcessMining,
  author    = {van der Aalst, Wil M. P.},
  title     = {Process Mining: Discovery, Conformance and Enhancement of Business Processes},
  publisher = {Springer},
  year      = {2011},
  doi       = {10.1007/978-3-642-19345-3}
}

@article{vanDerAalst2004AlphaAlgorithm,
  author  = {van der Aalst, Wil M. P. and Weijters, Ton and Maruster, Laura},
  title   = {Workflow Mining: Discovering Process Models from Event Logs},
  year    = {2004}
}
```

### 工具生态中的“检查点/时间旅行”与 NormCode 的隔离主张

你计划中列举的 LLM 工作流工具，与“层一检查点作为案例”的话题确实存在表面交集：例如 LangGraph 明确支持通过 checkpoints 实现 time travel（replay/fork），并把 checkpoint 描述为每步执行的状态快照。citeturn14search7turn14search1turn14search23turn14search4  

但从你当前论题的角度，更有价值的写法是：把这些工具作为“**具备 checkpoint 但缺乏可证明的结构隔离**”的对照物——因为在没有强制显式数据流与隔离规则的情况下，checkpoint 的输入可能隐含在共享上下文/对话历史/全局变量里，从而导致你所说的“案例污染、案例不可解释”。NormCode companion paper 把“每步强制隔离、消除隐式数据流、保证中间状态可检查”作为核心主张，正好能形成对比论证。citeturn14search0turn14search8turn14search7  

### 自托管与递归式 CBR 的表述抓手

NormCode companion paper 明确把“编译器以 NormCode 计划形式自运行（self-hosted execution）”作为验证点之一，这为你研究问题 8（自托管/反身系统与 meta‑CBR）提供了直接引用点。citeturn14search12turn14search0  
自托管本身在编译器/语言传统里常被解释为“编译器能编译自身源代码”，也常被当作语言成熟度/自洽性的标志（尽管你的论文会把它重新解释为“递归式经验蒸馏”）。citeturn14search28turn14search24turn14search20  

```bibtex
@article{GuanEtAl2025NormCode,
  author = {Guan, Xin and others},
  title  = {NormCode: A Semi-Formal Language for Auditable AI Planning},
  year   = {2025},
  eprint = {2512.10563},
  archivePrefix = {arXiv},
  doi    = {10.48550/arXiv.2512.10563}
}
```

---

## 结论性对齐：对 ICCBR 论述最有用的“已知支撑”与“可写成贡献的缺口”

从上述可获取文献出发，你的 ICCBR 2026 论文在 Related Work 与 Contribution 叙事上，最稳的落点是：

POCBR 文献已经充分确立“工作流/流程经验可作为案例”“查询可以是部分流程/从中间开始”“执行轨迹可被挖掘为案例并用于运行中支持”。citeturn7search8turn16view3turn18view0turn22search1  

多层/层次化 CBR 在 POCBR 内部已有非常贴近的形式：Müller & Bergmann 把“泛化案例”显式引入工作流案例库，并以专化回落到具体情境——这可以作为你“层二抽象案例”的最强先行工作与对齐点。citeturn16view0  

“运行时状态=案例”的直接先行工作并不明显：最接近的是“trace/prefix as case”与“derivational trace/replay as case”。因此你完全可以在论文中把层一贡献精确写成：**在强制隔离前提下，将可恢复的运行时检查点提升为一等案例对象，并以此保证案例完整性与可审计性**；其中“强制隔离/显式数据流/中间状态可检查”作为前提条件，应由 NormCode 语言规范（arXiv:2512.10563）承担主要证据。citeturn14search0turn14search8turn22search1turn18view0  

> 受限说明（需要你后续补齐的最小缺口清单）：本简报未能直接获取并精读“WETICE 2007 的 suspension mechanism 工作流适应”原文（多镜像访问失败），因此尚未确认其是否真正把“正在运行的工作流实例状态”提升为案例本体；同时你计划中的 EU AI Act 条款级别引用、以及 PDDL/HTN/BDI 等“推理媒介语言”原典对照材料，在本轮可访问源中未做系统抽取，建议在正式论文写作前补齐以增强法规模块与语言对比模块的可证据性。citeturn1search28turn14search0turn14search2