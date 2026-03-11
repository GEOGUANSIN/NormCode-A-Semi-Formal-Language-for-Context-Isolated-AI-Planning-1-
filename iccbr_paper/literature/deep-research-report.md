# NormCode Canvas 相关工作与文献深度调研报告

## 研究背景与核心定位

NormCode（及其 Canvas App）面向的是“多步 LLM 工作流/智能体（agentic）系统”在工程化落地时普遍遭遇的三个痛点：一是上下文在多步链路中不断累积导致的“上下文污染/漂移”（模型混淆中间产物、约束丢失、幻觉或错误链式放大）；二是数据流与控制流在多数框架里以“隐式上下文 + 约定俗成的状态对象”方式穿透步骤，导致难以复盘每一步到底看到了什么、做了什么；三是缺少能像传统软件一样支持断点/检查点、可复现重跑与差分调试的“可执行计划工件”。这些问题在智能体系统综述中被反复归因于长程推理、记忆管理、评测与工程可控性不足等瓶颈。citeturn7search1turn8search30

NormCode 的伴随论文明确提出：通过把工作流表达为一种“半形式（semi-formal）的计划语言”，并在语言层面强制“步骤间数据隔离（context-isolated / data isolation）”，使得每个推理步骤只接收显式传递的输入，从而在结构上消除跨步污染；同时把“语义操作（LLM 推理、非确定）”与“句法/确定性操作（数据重排、结构化转换）”分离，以便在成本、可靠性、可追溯性上做精细化记录与分析。citeturn9search10turn9search14

对比当下主流生态，一个可用于 demo paper 的稳定归纳是：  
（1）“原生 LLM/提示词”侧重快速试验但缺乏可复现与过程可视化；（2）“代码级编排框架/库”提供可组合组件与一定的状态管理，但往往仍以隐式上下文传递为主；（3）“低/无代码可视化 UI”降低门槛但易产生平台锁定与调试深度不足。相关综述与框架文档能够直接支撑“代码框架 + 低代码工具 + 可观测平台”已成为常见组合的判断。citeturn4search28turn7search1turn20search12

下文的文献与系统条目，按 demo paper 的“Related Work / Introduction framing / 技术背景”三类用途标注，并在每个条目中给出可直接写入论文的“局限点”（即 NormCode/Canvas 相比之下能主张的差异化价值）。

## 可视化与图形化 LLM 工作流工具

### entity["organization","Langflow","visual llm workflow builder"]

**引用信息**：Langflow contributors. *Langflow Documentation: Build flows*（文档，在线；访问日期 2026-03-10）。在线链接见 BibTeX。citeturn19search20turn19search0  
**两句摘要**：Langflow 提供拖拽式“组件—连线”画布来构建 LLM 应用工作流，并把工作流抽象为可复用的 flow。文档强调 flow “完全可序列化”，可在安装所在文件系统中保存与加载，从而把 UI 中的图结构固化为可再执行工件。citeturn19search20turn19search0  
**关键局限（相对 NormCode/Canvas）**：其“图”主要是应用编排表示，并不在语言层面强制每步输入/输出的隔离与类型化约束；可序列化不等价于“可审计的语义边界”，尤其当步骤仍依赖共享上下文或外部记忆组件时。citeturn19search20  
**相关性**：Related Work（直接可视化竞品）、Introduction framing（低代码图编排现状）。  
**BibTeX**：
```bibtex
@misc{langflow_docs_build_flows,
  author       = {Langflow Contributors},
  title        = {Langflow Documentation: Build flows},
  howpublished = {Online documentation},
  year         = {2026},
  note         = {Accessed: 2026-03-10},
  url          = {https://docs.langflow.org/concepts-flows}
}
```

### entity["organization","LangSmith","llm observability platform"]

**引用信息**：LangChain, Inc. *LangSmith Docs*（文档，在线；访问日期 2026-03-10）。在线链接见 BibTeX。citeturn20search2turn20search11turn4search17  
**两句摘要**：LangSmith 将“端到端 trace（调用链追踪）”作为核心工件：每次请求会生成覆盖 LLM 调用、工具调用与中间节点的执行记录，并提供 UI/SDK 支持过滤、对比、导出与监控。其 evaluation 工作流强调用数据集、评估器（含人评、规则、LLM-as-judge）与实验来系统化对比提示词/链路改动。citeturn20search11turn4search17  
**关键局限（相对 NormCode/Canvas）**：它增强的是“事后可观测性（post-hoc observability）”，但并不改变底层系统的隐式数据流范式；trace 能显示发生了什么，却未必保证“每一步只看到了被允许看到的数据”。此外，工作流本体通常仍寄存于代码/框架对象而非可移植语言工件。citeturn20search2turn20search5  
**相关性**：Related Work（调试/追踪平台对比）、Introduction framing（“可观测性是必要条件”）。  
**BibTeX**：
```bibtex
@misc{langsmith_docs_home,
  author       = {LangChain, Inc.},
  title        = {LangSmith Documentation},
  howpublished = {Online documentation},
  year         = {2026},
  note         = {Accessed: 2026-03-10},
  url          = {https://docs.langchain.com/langsmith/home}
}
```

### entity["organization","Prompt flow","microsoft prompt workflow tool"]

**引用信息**：Promptflow contributors. *Prompt flow documentation*（文档，在线）；以及 *Develop a dag flow*（DAG Flow 指南）。在线链接见 BibTeX。citeturn20search1turn20search0turn20search13turn20search30  
**两句摘要**：Prompt flow 将 LLM 应用表达为“函数/工具节点构成的 DAG（有向无环图）”，节点通过输入/输出依赖连接，并由执行器按拓扑顺序运行；flow 在工程上对应一组可下载/纳入版本控制的文件（核心为 YAML 定义 + Python/Jinja 工具）。其文档还提供 tracing（标注为实验性）来记录执行期事件与状态，辅助调试与理解节点 I/O。citeturn20search0turn20search16turn20search30  
**关键局限（相对 NormCode/Canvas）**：以 DAG 为主的范式更接近传统流水线/评测链路，对“循环/长程 agent loop”与复杂恢复语义通常需额外机制；更重要的是，它的“图结构”不等价于“显式隔离的语义边界”，节点仍可能通过共享上下文或外部状态间接耦合。citeturn20search0turn20search30  
**相关性**：Related Work（可视化 DAG 编排的强竞品）、技术背景（以 YAML/文件夹为工件的可移植性讨论）。  
**BibTeX**：
```bibtex
@misc{promptflow_dag_docs,
  author       = {Promptflow Contributors},
  title        = {Prompt flow: Develop a DAG flow},
  howpublished = {Online documentation},
  year         = {2026},
  note         = {Accessed: 2026-03-10},
  url          = {https://microsoft.github.io/promptflow/how-to-guides/develop-a-dag-flow/index.html}
}
```

### entity["organization","Flowise","drag and drop llm builder"]

**引用信息**：FlowiseAI. *Flowise: Build AI Agents, Visually*（开源仓库与文档入口，在线；访问日期 2026-03-10）；另：Flowise 文档的 embed/主题定制能力。citeturn21search10turn21search23  
**两句摘要**：Flowise 以“拖拽 UI + 节点连线”方式帮助用户基于 LangChainJS 组件拼装 LLM 应用/对话代理，并提供自托管与多种部署说明。其文档显示可将聊天组件嵌入到外部应用，并对外观与交互（例如按钮拖拽、主题、免责声明等）进行较细粒度定制。citeturn21search10turn21search23  
**关键局限（相对 NormCode/Canvas）**：更侧重快速搭建与交付“可用应用”，而不是把“计划/步骤语义”固化成可审计、可复盘、可约束的数据隔离语言；当链路复杂化（多分支、多轮循环、故障恢复）时，调试往往退化为查看日志或逐节点试跑，缺少语言级的断点/状态快照语义。citeturn21search10  
**相关性**：Related Work（no-code/low-code 竞品）、Introduction framing（非程序员可用性）。  
**BibTeX**：
```bibtex
@misc{flowise_github,
  author       = {FlowiseAI},
  title        = {Flowise: Build AI Agents, Visually},
  howpublished = {GitHub repository and docs},
  year         = {2026},
  note         = {Accessed: 2026-03-10},
  url          = {https://github.com/FlowiseAI/Flowise}
}
```

### entity["organization","AutoGen Studio","no-code autogen ui"]

**引用信息**：Victor Dibia 等. *AutoGen Studio: A No-Code Developer Tool for Building and Debugging Multi-Agent Systems*（arXiv, 2024；在线）。另：官方用户指南明确其定位“非生产级应用”。citeturn19search2turn19search3turn19search5  
**两句摘要**：AutoGen Studio 提供面向多智能体工作流的 no-code/low-code UI：用拖拽与声明式（JSON）规范来描述 agent team、组件、工具与终止条件，并提供交互式评测与调试界面，以及可复用组件库（gallery）。官方文档同时强调 Studio 旨在快速原型与演示，不被定位为生产就绪应用，鼓励开发者用底层 AutoGen 框架自行实现认证、安全等部署能力。citeturn19search2turn19search3  
**关键局限（相对 NormCode/Canvas）**：其核心 IR 是“对话/消息驱动的多 agent 协作规范”，而不是以“步骤级数据隔离”为第一原则的计划语言；因此更接近“把 agent 系统配置化/可视化”，但对“跨步数据最小化、显式输入集、可验证的边界”通常仍依赖约定与运行时日志。citeturn19search2turn19search3  
**相关性**：Priority 1 Related Work（最接近的“可视化 + 多 agent + 调试”系统论文）、技术背景（声明式 JSON 作为工件）。  
**BibTeX**：
```bibtex
@misc{dibia2024autogenstudio,
  title        = {AutoGen Studio: A No-Code Developer Tool for Building and Debugging Multi-Agent Systems},
  author       = {Dibia, Victor and others},
  year         = {2024},
  eprint       = {2408.15247},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2408.15247}
}
```

image_group{"layout":"carousel","aspect_ratio":"16:9","query":["Langflow UI flow builder screenshot","LangSmith tracing UI screenshot","Microsoft PromptFlow visual editor screenshot","Flowise AI drag and drop UI screenshot","AutoGen Studio Team Builder screenshot"],"num_per_query":1}

### 第二梯队：观测与评测平台为“可视化调试”提供底座

在“可视化编排”之外，近两年快速增长的是 LLM observability / tracing / evaluation 平台：它们通常不负责生成工作流本体，但负责记录每次执行的输入输出、latency、token、成本、错误，并提供数据集评测与回归检测。

**entity["company","Langfuse","open source llm observability"]**：官方文档强调其 trace 记录请求生命周期，覆盖 LLM 调用、检索、工具执行与自定义逻辑，并提供 token/cost、评测与 prompt 管理等面向 LLM 的一体化功能；同时声称 SDK 异步上报以避免增加在线延迟。citeturn21search3  
**entity["company","Helicone","llm observability gateway"]**：开源仓库将其定位为“AI Gateway & LLM Observability”，主打一行代码接入、提示词版本管理与自托管，属于“以网关切面捕获调用”的工程路线。citeturn21search2  
**entity["company","Braintrust","ai observability platform"]**：文档把 evaluation 定义为把非确定输出转为可度量反馈回路的系统化实验（数据集 + 任务函数 + 打分器），强调用于回归检测与迭代。citeturn21search9turn21search22  

这些平台与 NormCode/Canvas 的关系可以在 Related Work 中表述为：它们解决“记录与对比”的问题，但大多不解决“计划工件的可移植语义与隔离约束”问题，因此 NormCode 可以把自身定位为“可观测的对象（object of observability）本身更结构化”。citeturn20search11turn9search14

## 代理编排框架与数据流透明性

### entity["organization","ReAct","reasoning and acting prompting"]

**引用信息**：*ReAct: Synergizing Reasoning and Acting in Language Models*（arXiv:2210.03629；ICLR 2023）。citeturn5search0turn5search16  
**两句摘要**：ReAct 通过“交错生成推理轨迹与行动（工具/API/环境交互）”把 reasoning 与 acting 结合起来，并在 QA、事实核验与交互式任务上展示相对基线的优势，同时强调更强的人类可解释性。论文还指出仅靠纯推理链可能出现幻觉与误差传播，而与环境交互能提供纠错信号。citeturn5search0  
**关键局限（相对 NormCode/Canvas）**：ReAct 主要是 prompting 范式与轨迹结构，而非“可执行的、带数据隔离约束的计划语言”；因此其数据流边界更多依赖提示模板与实践约定，并不从结构上禁止跨步污染或隐式共享状态。citeturn5search0  
**相关性**：Priority 1 Related Work（agent 架构原型）、Introduction framing（解释“reason+act loop”是主流心智模型）。  
**BibTeX**：
```bibtex
@misc{yao2022react,
  title        = {ReAct: Synergizing Reasoning and Acting in Language Models},
  author       = {Yao, Shunyu and others},
  year         = {2022},
  eprint       = {2210.03629},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  url          = {https://arxiv.org/abs/2210.03629}
}
```

### entity["organization","LangGraph","stateful agent orchestration"]

**引用信息**：LangChain 文档：LangGraph overview；以及 persistence/human-in-the-loop 相关说明（在线）。citeturn4search0turn4search15turn4search36  
**两句摘要**：LangGraph 将 agentic 应用建模为“带状态的图”，强调 durable execution、流式输出与 human-in-the-loop，并通过 checkpoint/persistence 支持中断、检查、修改状态与恢复执行。文档与示例仓库都把其主要用例指向长流程、多步骤与多参与者（multi-actor）应用。citeturn4search0turn4search15turn4search36  
**关键局限（相对 NormCode/Canvas）**：LangGraph 的强项在运行时编排与持久化，它对“步骤边界的数据最小输入集”并不强制——常见实现仍以共享 state 对象在节点间流转；这使得可追溯性更像“把 state 记录下来”，而不是“从语言结构推导出每步合法可见的数据域”。citeturn4search15turn4search0  
**相关性**：Priority 1 Related Work（编排框架基线）、技术背景（检查点/中断与 Canvas 调试体验对齐）。  
**BibTeX**：
```bibtex
@misc{langgraph_overview,
  author       = {LangChain},
  title        = {LangGraph Overview},
  howpublished = {Online documentation},
  year         = {2026},
  note         = {Accessed: 2026-03-10},
  url          = {https://docs.langchain.com/oss/python/langgraph/overview}
}
```

### entity["organization","AutoGen","multi-agent conversation framework"]

**引用信息**：*AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework*（arXiv:2308.08155；并在 OpenReview/Microsoft Research 有对应条目）。citeturn5search2turn5search30  
**两句摘要**：AutoGen 提供“多智能体可对话（conversable）”框架，让开发者通过自然语言与代码共同定义 agent 交互模式，并支持人类参与与工具调用，从而构建多样复杂度的应用。论文报告其在多个示例领域的有效性，并把 multi-agent conversation 视为复杂任务分解与集成的通用基础设施。citeturn5search2  
**关键局限（相对 NormCode/Canvas）**：AutoGen 的核心抽象是会话与交互协议，天然更偏“协作过程编程”；对数据流透明性通常依赖日志/trace，而不是由语言结构确保“每一步输入即权限边界”。因此其可审计性更多是“记录对话”，而非“约束对话能携带什么”。citeturn5search2  
**相关性**：Priority 1 Related Work（多 agent 框架代表）。  
**BibTeX**：
```bibtex
@misc{wu2023autogen,
  title        = {AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework},
  author       = {Wu, Qingyun and others},
  year         = {2023},
  eprint       = {2308.08155},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2308.08155}
}
```

### Reflexion 与“自反式记忆”路线

**引用信息**：*Reflexion: Language Agents with Verbal Reinforcement Learning*（arXiv:2303.11366；NeurIPS 2023）。citeturn5search1turn5search13  
**两句摘要**：Reflexion 通过“语言化反馈 + episodic memory”让 agent 不改权重而从试错中改进，把过去失败的反思写入记忆缓冲以提升后续决策。其结果显示在多类任务（含编程）上可显著超越某些基线。citeturn5search1  
**关键局限（相对 NormCode/Canvas）**：该路线强化的是“记忆驱动的自我改进”，但更强的记忆也会加剧上下文累积的管理难题；它缺少对“哪些信息可以跨步传播”的结构性限制，因此与 NormCode 的“隔离优先”策略形成对照。citeturn5search1  
**相关性**：Related Work（agent 反思/记忆机制）、技术动机（上下文累积的风险来源）。  
**BibTeX**：
```bibtex
@misc{shinn2023reflexion,
  title        = {Reflexion: Language Agents with Verbal Reinforcement Learning},
  author       = {Shinn, Noah and others},
  year         = {2023},
  eprint       = {2303.11366},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2303.11366}
}
```

### MetaGPT 与 SOP 化多角色协作

**引用信息**：*MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework*（arXiv:2308.00352；ICLR 2024 口头报告版本在 arXiv 更新）。citeturn5search3turn5search7  
**两句摘要**：MetaGPT 把人类软件工程 SOP（标准作业流程）编码为 prompt 序列，让多角色 agent 以“流水线/装配线”方式协作，并强调通过中间验证与模块化输出减少级联幻觉。论文将其定位为“把有效的人类工作流注入 LLM 多 agent 协作”的方法。citeturn5search3  
**关键局限（相对 NormCode/Canvas）**：SOP/prompt 序列依旧主要在自然语言层面约束过程，输出模块化≠输入隔离；当工作链更长、更复杂时，仍需要一个更强的“可执行中间表示/语言”来保证每步只接触显式输入，并在 IDE 中实现断点与状态检查。citeturn5search3  
**相关性**：Priority 2 Related Work（结构化多 agent 工作流对比）。  
**BibTeX**：
```bibtex
@misc{hong2023metagpt,
  title        = {MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework},
  author       = {Hong, Sirui and others},
  year         = {2023},
  eprint       = {2308.00352},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2308.00352}
}
```

### HuggingGPT、Voyager 与“工具/技能库”派

**引用信息**：  
HuggingGPT（arXiv:2303.17580）。citeturn6search0  
Voyager（arXiv:2305.16291）。citeturn6search1  

**两句摘要**：HuggingGPT 让 ChatGPT 充当控制器：把用户请求分解为子任务、在模型库中选择合适的专家模型执行并汇总结果，是“LLM 规划 + 工具执行”的早期系统化范式。citeturn6search0 Voyager 强调在 Minecraft 中进行开放式、终身学习：用自动 curriculum、可增长技能库与迭代式提示，将执行错误与环境反馈纳入程序改进。citeturn6search1  
**关键局限（相对 NormCode/Canvas）**：两者都展示了“长链路 + 工具/技能”的可行性，但其计划表达仍偏系统内部结构，缺少统一、可移植、可审计的计划语言工件；对上下文与中间数据的治理更多依赖工程策略而非结构性隔离。citeturn6search0turn6search1  
**相关性**：技术背景（工具调用型 agent 的谱系）、动机（长链路需要更强的调试与隔离）。  
**BibTeX**：
```bibtex
@misc{shen2023hugginggpt,
  title        = {HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face},
  author       = {Shen, Yongliang and others},
  year         = {2023},
  eprint       = {2303.17580},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  url          = {https://arxiv.org/abs/2303.17580}
}

@misc{wang2023voyager,
  title        = {Voyager: An Open-Ended Embodied Agent with Large Language Models},
  author       = {Wang, Guanzhi and others},
  year         = {2023},
  eprint       = {2305.16291},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2305.16291}
}
```

### AgentBench 与 Auto-GPT 风格系统的评测线索

**引用信息**：AgentBench（arXiv:2308.03688）。citeturn6search3  
Auto-GPT for Online Decision Making（arXiv:2306.02224）。citeturn7search0  

**两句摘要**：AgentBench 将 LLM-as-Agent 置于多环境、多维度 benchmark，报告商业与开源模型在交互式任务上的差距，并把“长期推理、决策与指令遵循失败”作为主要障碍。citeturn6search3 Auto-GPT 风格评测工作则试图把“自动规划+执行的循环系统”放到在线决策任务中做系统性对比，以弥补早期 demo 缺少基准的问题。citeturn7search0  
**关键局限（相对 NormCode/Canvas）**：评测工作能证明问题存在，但无法直接提供“可移植、可审计、可调试”的计划工件；NormCode/Canvas 可将这些 benchmark 作为“为何需要结构化隔离与调试”的动机引用。citeturn6search3turn7search0  
**相关性**：Introduction framing（痛点与现状证据）、技术背景（评测基准）。  
**BibTeX**：
```bibtex
@misc{liu2023agentbench,
  title        = {AgentBench: Evaluating LLMs as Agents},
  author       = {Liu, Xiao and others},
  year         = {2023},
  eprint       = {2308.03688},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2308.03688}
}

@misc{yang2023autogpt_odm,
  title        = {Auto-GPT for Online Decision Making},
  author       = {Yang, H. and others},
  year         = {2023},
  eprint       = {2306.02224},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2306.02224}
}
```

## 上下文污染与长上下文退化研究

### Lost in the Middle 与长上下文“位置敏感性”

**引用信息**：*Lost in the Middle: How Language Models Use Long Contexts*（arXiv:2307.03172；并在 TACL 2024 发表）。citeturn8search0turn8search4  
**两句摘要**：该工作系统分析了长上下文模型在“多文档 QA 与 key-value 检索”任务上的使用方式，发现相关信息位于上下文中间时性能显著下降，而在开头或结尾更好，呈现典型“lost in the middle”效应。它因此提供了直接支撑“长上下文并不稳定等价于更强能力”的实验依据。citeturn8search0turn8search4  
**关键局限（相对 NormCode/Canvas）**：论文解释了现象，但不提供一个通用的工程 IR 来系统性拆分与隔离上下文；NormCode/Canvas 可以把“隔离 + 显式输入”作为对这一现象的结构性缓解路径。citeturn9search14turn8search0  
**相关性**：Priority 2 Introduction framing（核心技术动机）。  
**BibTeX**：
```bibtex
@article{liu2024lost_middle,
  title   = {Lost in the Middle: How Language Models Use Long Contexts},
  author  = {Liu, Nelson F. and others},
  journal = {Transactions of the Association for Computational Linguistics},
  year    = {2024},
  url     = {https://aclanthology.org/2024.tacl-1.9/},
  note    = {Originally circulated as arXiv:2307.03172}
}
```

### NormCode 将“上下文污染”作为语言级目标

**引用信息**：*NormCode: A Semi-Formal Language for Context-Isolated AI Planning*（arXiv:2512.10563，2025）。citeturn9search10turn9search14  
**两句摘要**：该论文明确把“多步 LLM 链的上下文污染”视为系统失效来源，并提出通过“步骤级数据隔离 + 显式输入传递”在结构上避免跨步污染，同时以可执行的 orchestrator 支持依赖调度与 checkpoint。它还强调“可审计 by construction”，把中间状态检查与验证作为语言工件的一部分。citeturn9search10turn9search14  
**关键局限（相对 Canvas demo paper）**：伴随论文主要聚焦语言与编译/执行系统；Canvas demo paper 需要补齐“IDE 级可视化执行/调试体验如何把语言优势落到人机协作流程”的证据与对比（即本次调研的核心）。citeturn9search14turn4search15  
**相关性**：技术背景（自引/定位）。  
**BibTeX**：
```bibtex
@misc{guan2025normcode,
  title        = {NormCode: A Semi-Formal Language for Context-Isolated AI Planning},
  author       = {Guan, Xin},
  year         = {2025},
  eprint       = {2512.10563},
  archivePrefix= {arXiv},
  primaryClass = {cs.AI},
  url          = {https://arxiv.org/abs/2512.10563}
}
```

### 记忆机制与“上下文/记忆治理”成为独立研究主题

**引用信息**：*A Survey on the Memory Mechanism of Large Language Model-Based Agents*（ACM Computing Surveys，页面信息）。citeturn8search27  
**两句摘要**：该类 survey 通常把 agent 记忆拆为短期上下文、长期记忆、外部检索与总结压缩等组件，并讨论在不同任务下如何存取、更新与遗忘。其存在本身可作为“上下文工程/记忆管理已成为 LLM agent 的系统层议题”的旁证。citeturn8search27turn8search37  
**关键局限（相对 NormCode/Canvas）**：记忆治理常以“策略/组件”呈现，难以获得语言级的可验证边界；NormCode 的差异化主张在于把“哪些信息能跨步流动”写入计划结构而非只写入策略。citeturn9search14turn8search37  
**相关性**：技术背景（context/memory 的学术脉络）。  
**BibTeX**：
```bibtex
@article{survey_memory_llm_agents,
  title   = {A Survey on the Memory Mechanism of Large Language Model-Based Agents},
  author  = {Unknown},
  journal = {ACM Computing Surveys},
  year    = {2024},
  doi     = {10.1145/3748302},
  url     = {https://dl.acm.org/doi/10.1145/3748302}
}
```

## 可审计性、可追溯性与安全隔离

### 欧盟 AI Act 对“日志与可追溯性”的要求

**引用信息**：欧盟 AI Act 被标识为 Regulation (EU) 2024/1689；欧盟官方政策页与 EUR-Lex summary 可用于引用其监管定位。citeturn16search5turn16search10turn16search0  
**两句摘要**：AI Act 对高风险 AI 系统提出记录保存与可追溯性要求：欧委会的 AI Act Service Desk 对 Article 12（Record-keeping）解释为高风险系统需具备自动日志能力，用于识别风险、支持 post-market monitoring、追踪系统运行；并在 Article 19 强调提供方需保留自动生成日志至少 6 个月（或按适用法律）。citeturn16search1turn16search12  
**关键局限（相对 NormCode/Canvas）**：监管条款强调“要能记录”，但多数学术/工业系统采取“事后日志/trace”来满足；NormCode 的主张是把可审计性前移为“结构性产物（by construction）”，使日志不仅是附加件，而是从计划语言的显式 I/O 边界中自然导出。citeturn9search14turn16search1  
**相关性**：Priority 2 Introduction framing（合规动机）、Related Work（auditability/traceability）。  
**BibTeX**：
```bibtex
@misc{eu_ai_act_2024_1689,
  author       = {{European Union}},
  title        = {Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence (Artificial Intelligence Act)},
  year         = {2024},
  note         = {High-risk requirements include record-keeping and log retention; see Commission explanations for Articles 12 and 19. Accessed: 2026-03-10},
  url          = {https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai}
}
```

**时效性提示（可选写入 Introduction 的脚注）**：截至 2025-11-19，路透社报道欧委会在“Digital Omnibus”简化方案中提出将部分高风险规则适用期从 2026-08 延至 2027-12 的提议，仍需后续立法程序。citeturn16news41

### entity["organization","NIST","us standards institute"] 的 AI RMF 对“透明、可解释、问责”的框架化

**引用信息**：NIST AI RMF 1.0（NIST AI 100-1，2023）以及其 Generative AI Profile（NIST AI 600-1，2024）。citeturn16search2turn16search25  
**两句摘要**：NIST AI RMF 1.0 将“透明、可解释、可问责”列为可信 AI 的关键特征，并以 GOVERN/MAP/MEASURE/MANAGE 的过程框架组织风险治理。其 Generative AI Profile 作为配套资源，专门面向生成式系统的风险与评测落地，适合用来支撑“记录—评测—持续监控”在合规与工程中的正当性。citeturn16search2turn16search25  
**关键局限（相对 NormCode/Canvas）**：RMF 是治理框架而非系统 IR/语言，难以直接回答“如何在工作流层面构造可审计的执行边界”；因此 NormCode 可将自己定位为落实 RMF “透明与可追溯”目标的工程载体之一。citeturn16search2turn9search14  
**相关性**：Introduction framing（行业治理共识）、技术背景（合规语境）。  
**BibTeX**：
```bibtex
@misc{nist_ai_rmf_100_1,
  author       = {{National Institute of Standards and Technology}},
  title        = {Artificial Intelligence Risk Management Framework (AI RMF 1.0)},
  year         = {2023},
  series       = {NIST AI 100-1},
  url          = {https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf}
}

@misc{nist_genai_profile_600_1,
  author       = {{National Institute of Standards and Technology}},
  title        = {AI RMF Generative AI Profile},
  year         = {2024},
  series       = {NIST AI 600-1},
  url          = {https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf}
}
```

### entity["organization","Washington University in St. Louis","university in st louis"] 的 IsolateGPT：从安全角度提出“执行隔离”

**引用信息**：*IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems*（NDSS 2025；官网与 PDF 均可引用）。citeturn9search0turn9search11turn9search19  
**两句摘要**：IsolateGPT 从系统安全出发，讨论 LLM agent 系统在“共享环境”中处理多方资源/工具带来的风险，并提出用执行隔离（isolation）与访问控制来限制外部工具之间的数据暴露。该工作强调把安全原则引入 agentic 系统，并用实验评估隔离可行性与性能开销。citeturn9search0turn9search11  
**关键局限（相对 NormCode/Canvas）**：IsolateGPT 聚焦“工具/应用层隔离”与安全边界，而不是“推理步骤的语义输入边界”；NormCode 的区别在于把隔离内化为计划语言的结构属性，使调试与审计可以在更细粒度（step/variable scope）上进行。citeturn9search14turn9search0  
**相关性**：Related Work（隔离/审计的系统研究对照）、技术背景（安全与隔离的旁证）。  
**BibTeX**：
```bibtex
@inproceedings{wu2025isolategpt,
  title     = {IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems},
  author    = {Wu, Yuhao and others},
  booktitle = {Network and Distributed System Security Symposium (NDSS)},
  year      = {2025},
  url       = {https://www.ndss-symposium.org/ndss-paper/isolategpt-an-execution-isolation-architecture-for-llm-based-agentic-systems/}
}
```

## IR 与半形式工作流语言谱系

### 以“推理中间表示”为主线：从自然语言到程序与图结构

**Chain-of-Thought**  
**引用信息**：*Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*（arXiv:2201.11903；OpenReview 2022）。citeturn10search0turn10search4  
**两句摘要**：CoT 通过在提示中示范“中间推理步骤”，显著提升模型在算术、常识与符号推理任务上的表现，奠定了“用自然语言作为 IR 诱导推理”的范式。它也间接推动了后续把“推理轨迹”当作可视化/可审计对象的工程思路。citeturn10search0  
**关键局限（相对 NormCode/Canvas）**：CoT 的中间表示是自然语言、缺少形式化 I/O 边界与可执行语义，难以稳定复现与约束数据流；NormCode 试图占据“比自然语言更结构化、比完全形式语言更易生成”的中间地带。citeturn9search14turn10search0  
**相关性**：Priority 3 技术背景（IR lineage）。  
**BibTeX**：
```bibtex
@misc{wei2022cot,
  title        = {Chain-of-Thought Prompting Elicits Reasoning in Large Language Models},
  author       = {Wei, Jason and others},
  year         = {2022},
  eprint       = {2201.11903},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  url          = {https://arxiv.org/abs/2201.11903}
}
```

**Tree of Thoughts**  
**引用信息**：*Tree of Thoughts: Deliberate Problem Solving with Large Language Models*（arXiv:2305.10601）。citeturn10search1  
**两句摘要**：ToT 把推理从单链扩展为“可探索的 thought 单元树”，通过生成多条路径、自评与回溯实现更强的搜索式规划能力。它强化了“结构化推理轨迹（tree/graph）”作为 IR 的观点。citeturn10search1  
**关键局限（相对 NormCode/Canvas）**：ToT 仍以自然语言 thought 为核心工件，缺少对步骤数据域、确定性转换与可执行调试语义的统一建模；对审计而言，树结构≠可验证的输入输出边界。citeturn10search1turn9search14  
**相关性**：技术背景（结构化推理 IR）。  
**BibTeX**：
```bibtex
@misc{yao2023tot,
  title        = {Tree of Thoughts: Deliberate Problem Solving with Large Language Models},
  author       = {Yao, Shunyu and others},
  year         = {2023},
  eprint       = {2305.10601},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  url          = {https://arxiv.org/abs/2305.10601}
}
```

**Graph of Thoughts（Besta 等的框架化版本）**  
**引用信息**：*Graph of Thoughts: Solving Elaborate Problems with Large Language Models*（arXiv:2308.09687；AAAI 2024 版本可引用）。citeturn10search2turn10search30  
**两句摘要**：该工作把“thought”建模为图节点、依赖为边，使推理可以以任意图结构组合、蒸馏与反馈回路增强，并报告在若干任务上相对 ToT 的质量与成本收益。它把 IR 进一步推向“可操作的图结构”，与可视化工作流天然贴近。citeturn10search2turn10search30  
**关键局限（相对 NormCode/Canvas）**：GoT 强调“thought 组合的搜索/变换”，但并未把“数据隔离/权限边界”作为第一性原则；而 Canvas 的切入点更接近软件工程中的“可调试执行图”，强调每步状态可检查与输入最小化。citeturn10search2turn4search15  
**相关性**：技术背景（graph-IR）。  
**BibTeX**：
```bibtex
@misc{besta2023got,
  title        = {Graph of Thoughts: Solving Elaborate Problems with Large Language Models},
  author       = {Besta, Maciej and others},
  year         = {2023},
  eprint       = {2308.09687},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  url          = {https://arxiv.org/abs/2308.09687}
}
```

**Program-of-Thoughts**  
**引用信息**：*Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks*（arXiv:2211.12588）。citeturn10search3turn10search19  
**两句摘要**：PoT 把推理过程表达为可执行程序，把计算交给外部解释器执行，从而实现“推理与计算解耦”，并在数学/金融 QA 数据集上报告提升。它代表了“用更形式化的 IR（代码）替代纯自然语言”的方向。citeturn10search3  
**关键局限（相对 NormCode/Canvas）**：PoT 的 IR 偏向数值计算与代码执行，难以直接表达复杂 agent 工作流的控制结构、数据域隔离与审计需求；NormCode 的定位是面向“计划/步骤编排”的 IR，而非单纯把推理变成代码。citeturn10search3turn9search14  
**相关性**：技术背景（IR 对比：NL vs code）。  
**BibTeX**：
```bibtex
@misc{chen2022pot,
  title        = {Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks},
  author       = {Chen, Wenhu and others},
  year         = {2022},
  eprint       = {2211.12588},
  archivePrefix= {arXiv},
  primaryClass = {cs.CL},
  url          = {https://arxiv.org/abs/2211.12588}
}
```

### IR 的工程教科书：以 entity["organization","LLVM","compiler infrastructure"] 为例

**引用信息**：Chris Lattner 与 Vikram Adve. *LLVM: A Compilation Framework for Lifelong Program Analysis & Transformation*（CGO 2004）。citeturn11search0turn11search15  
**两句摘要**：LLVM 论文把 IR 视为跨编译期、链接期、运行期与离线优化的持续分析基础，强调 IR 作为统一载体可以承载多阶段转换与分析。对 NormCode 类系统而言，LLVM 提供了“好 IR 应具备：可移植、可分析、可插桩、可演进”的经典参照系。citeturn11search0  
**关键局限（相对 NormCode/Canvas）**：LLVM IR 面向确定性程序与编译优化，不直接处理 LLM 的非确定推理；NormCode 需要在“可分析/可审计”与“允许 LLM 生成/修改计划”的柔性之间做权衡。citeturn11search0turn9search14  
**相关性**：技术背景（IR 设计类比）。  
**BibTeX**：
```bibtex
@inproceedings{lattner2004llvm,
  title     = {LLVM: A Compilation Framework for Lifelong Program Analysis \& Transformation},
  author    = {Lattner, Chris and Adve, Vikram},
  booktitle = {CGO},
  year      = {2004},
  url       = {https://llvm.org/pubs/2004-01-30-CGO-LLVM.pdf}
}
```

### 形式规划语言与半形式工作流语言：对“可执行计划”的两端参照

**PDDL（形式规划输入语言）**  
**引用信息**：PDDL 1.2 手册（AIPS-98 Planning Competition 语言说明）；EUR-Lex/ISI 页可用于引用概述。citeturn11search1turn11search10  
**两句摘要**：PDDL 通过形式化谓词、动作、前置条件与效果来表达规划问题，目标是可比性与可复用性，成为经典规划竞赛的通用输入语言。它代表“完全形式化 IR”的一端，具备明确语义与可验证性。citeturn11search1turn11search10  
**关键局限（相对 NormCode/Canvas）**：PDDL 表达精确但对 LLM 生成不友好（易出现语法/语义错误），且对现实工作流中的非确定推理与数据重排不够贴合；NormCode 的“半形式”主张可被表述为“在可生成性与可验证性之间取中间点”。citeturn11search1turn9search14  
**相关性**：技术背景（规划 lineage）。  
**BibTeX**：
```bibtex
@misc{mcdermott1998pddl,
  title        = {PDDL--The Planning Domain Definition Language},
  author       = {McDermott, Drew and others},
  year         = {1998},
  note         = {AIPS-98 Planning Competition language manual},
  url          = {https://www.cs.cmu.edu/~mmv/planning/readings/98aips-PDDL.pdf}
}
```

**HTN 规划（经典分解式计划）**  
**引用信息**：Erol 等. *Semantics for Hierarchical Task-Network Planning*（1994）。citeturn11search2  
**两句摘要**：HTN 通过把高层任务递归分解为子任务网络来生成计划，并在该论文中给出了形式语义与算法性质讨论。它为“先分解、后执行”的 agent 规划范式提供了经典理论背景。citeturn11search2  
**关键局限（相对 NormCode/Canvas）**：HTN 的理论语义并不直接解决 LLM 推理的上下文污染与审计问题；NormCode 可把“任务分解”与“步骤数据域隔离”结合，作为现代 LLM 工作流的 HTN 化变体。citeturn11search2turn9search14  
**相关性**：技术背景（规划 lineage）。  
**BibTeX**：
```bibtex
@misc{erol1994htn_semantics,
  title  = {Semantics for Hierarchical Task-Network Planning},
  author = {Erol, Kutluhan and others},
  year   = {1994},
  url    = {https://www.cs.umd.edu/~nau/papers/erol1994semantics.pdf}
}
```

**半形式工作流/建模语言：BPMN 与 BPEL**  
**引用信息**：OMG. *Business Process Model and Notation (BPMN) Version 2.0*（规范 PDF）。citeturn12search0turn12search20  
OASIS. *WS-BPEL 2.0*（标准/规范页）。citeturn12search13turn12search1  
**两句摘要**：BPMN 旨在提供跨业务分析师与开发者都“可读”的流程图记法，同时又足够精确以映射到可执行组件；BPEL 则更偏面向 Web Service 编排的可执行流程语言。它们共同构成“组织级流程可视化 + 可执行编排”的成熟传统，可作为 NormCode Canvas 的类比参照。citeturn12search20turn12search13  
**关键局限（相对 NormCode/Canvas）**：这些语言主要为确定性业务流程与服务编排设计，不包含 LLM 推理的非确定语义与上下文治理；NormCode 的贡献可被表述为“把 LLM 推理纳入可执行工作流语言，并把 data isolation 做成语义基元”。citeturn9search14turn12search20  
**相关性**：Priority 3 技术背景（半形式语言谱系）。  
**BibTeX**：
```bibtex
@misc{omg_bpmn_2_0,
  author       = {{Object Management Group}},
  title        = {Business Process Model and Notation (BPMN), Version 2.0},
  year         = {2011},
  howpublished = {Specification},
  url          = {https://www.omg.org/spec/BPMN/2.0/PDF/}
}

@misc{oasis_wsbpel_2_0,
  author       = {{OASIS}},
  title        = {Web Services Business Process Execution Language (WS-BPEL) Version 2.0},
  year         = {2007},
  howpublished = {Standard},
  url          = {https://www.oasis-open.org/standard/wsbpel/}
}
```

### 科学工作流语言：把“可移植工件”作为第一原则的类比

**CWL（Common Workflow Language）**  
**引用信息**：CWL v1.2 标准页；以及 CACM 论文 *Methods Included*（doi:10.1145/3486897）。citeturn13search0turn14search2turn14search29  
**两句摘要**：CWL 明确以“跨执行引擎的可移植与可复用”为目标，提供对命令行工具与工作流组合的标准化 schema 与执行语义；CACM 文章强调其 separation of concerns、provenance、portability 与社区标准化路线。它为 NormCode 论证“计划语言作为可移植工件”提供了强参照：即便执行环境多样，语言工件仍能跨平台迁移。citeturn13search0turn14search12  
**关键局限（相对 NormCode/Canvas）**：CWL 面向确定性工具链与文件流转，不解决 LLM 推理的上下文污染与语义非确定；NormCode 可被表述为把 CWL 式的可移植/可追溯理念扩展到“LLM 推理步骤”。citeturn14search12turn9search14  
**相关性**：技术背景（工作流语言对比）。  
**BibTeX**：
```bibtex
@article{crusoe2022methods_included,
  title   = {Methods Included: Standardizing Computational Reuse and Portability with the Common Workflow Language},
  author  = {Crusoe, Michael R. and others},
  journal = {Communications of the ACM},
  year    = {2022},
  doi     = {10.1145/3486897},
  url     = {https://dl.acm.org/doi/10.1145/3486897}
}
```

**Nextflow 与 Snakemake（工程化可复现执行）**  
**引用信息**：Di Tommaso 等. *Nextflow enables reproducible computational workflows*（Nat Biotechnol 2017；doi:10.1038/nbt.3820）。citeturn14search1turn14search0  
Köster & Rahmann. *Snakemake—a scalable bioinformatics workflow engine*（Bioinformatics 2012）。citeturn13search2  
**两句摘要**：Nextflow 强调在多平台/容器化环境中实现可复现的流水线执行，属于“执行引擎 + DSL”的工程路线；Snakemake 则以可读的 Python 风格工作流定义与可扩展执行环境著称。它们说明：当工作流足够复杂时，业界会自然演化出“可执行 DSL + 可重跑/可扩展执行器”的结构，这与 NormCode “语言 + orchestrator + IDE”路线存在可比性。citeturn14search1turn13search2  
**关键局限（相对 NormCode/Canvas）**：这些系统处理的是确定性计算任务，不直接面对 LLM 推理的上下文治理；NormCode 的差异点是把“输入域隔离”作为语言语义的一部分，而不是仅依赖容器/执行器。citeturn9search14turn14search20  
**相关性**：技术背景（DSL + 执行器的类比）。  
**BibTeX**：
```bibtex
@article{ditommaso2017nextflow,
  title   = {Nextflow enables reproducible computational workflows},
  author  = {Di Tommaso, Paolo and others},
  journal = {Nature Biotechnology},
  year    = {2017},
  doi     = {10.1038/nbt.3820},
  url     = {https://pubmed.ncbi.nlm.nih.gov/28398311/}
}

@article{koster2012snakemake,
  title   = {Snakemake---a scalable bioinformatics workflow engine},
  author  = {K{\"o}ster, Johannes and Rahmann, Sven},
  journal = {Bioinformatics},
  year    = {2012},
  url     = {https://academic.oup.com/bioinformatics/article/28/19/2520/290322}
}
```

## 关键对照表与时间线

### 可视化 LLM 工作流工具对照

下表的维度定义来自各工具官方文档/论文对其能力边界的描述：Langflow 强调 flow 可序列化工件；LangSmith 强调 trace/eval；Prompt flow 强调 DAG/YAML 文件夹与（实验性）tracing；Flowise 强调拖拽搭建与自托管；AutoGen Studio 强调 no-code 多 agent 原型、调试与 JSON 规范（且明确非生产定位）。citeturn19search20turn20search11turn20search0turn21search10turn19search3turn19search2

| 工具 | 数据流透明性（显式 I/O） | 调试深度（断点/状态检查/回放） | 工件可移植性（离开平台可执行） | 非程序员可用性 | 论文可写的“关键短板”指向 |
|---|---|---|---|---|---|
| LangFlow | 中：图结构显式，但语义边界多由组件约定 | 中：可视化试跑/看中间输出，但少有语言级断点语义 | 中：flow 可序列化；依赖其生态/组件集 | 高：拖拽式低代码 | “图编排”≠“隔离 by construction” |
| LangSmith | 中：trace 显示链路，但本体仍在代码/框架 | 中-高：trace、对比、评测、人评队列 | 中：trace/数据集可导出，但计划工件非语言化 | 中：评审 UI 友好，但配置偏工程化 | 强在“事后观测”，弱在“结构约束” |
| PromptFlow | 中-高：DAG 节点 I/O 与 YAML 工件更显式 | 中：节点级运行/trace（实验性） | 高：flow 文件夹可下载入库、CI/CD | 中：有 UI，但自定义工具需编程 | DAG 偏流水线；对循环/隔离约束有限 |
| Flowise | 中：节点连线直观，但复杂控制流表达受限 | 低-中：多为日志/逐节点试跑 | 中：开源自托管；工件常与平台/节点库绑定 | 高：主打 no-code | 调试与审计深度不足、难复盘边界 |
| AutoGen Studio | 中：JSON 规范化团队/组件，但数据域仍会话化 | 中：交互式评测与调试；但官方不主张生产 | 中：JSON/框架兼容；生产需自建 | 高：no-code/low-code | 对话式多 agent ≠ 步骤级隔离语言 |

### 代理框架与“更结构化/更可视化”演化时间线

该时间线选取 2022–2025 年在论文与系统层面最能支持 demo paper 叙事的里程碑：从“提示诱导推理”到“agent loop”，再到“图编排/可视化开发工具”，最后到“语言级隔离与系统级隔离”。citeturn10search0turn5search0turn5search1turn5search2turn8search0turn4search0turn19search2turn9search10turn9search0  

- 2022：CoT 把“中间推理步骤”推向主流 IR 思路；ReAct 把推理与行动交错，形成 agent loop 的经典模板。citeturn10search0turn5search0  
- 2023：Reflexion（反思记忆）、AutoGen（多 agent 会话编排）、HuggingGPT（LLM 规划并调用模型/工具）、Voyager（长程技能库）、AgentBench（系统评测）共同扩大了“多步/多 agent”系统的范围；Lost in the Middle 为“长上下文不可靠”提供实验动机。citeturn5search1turn5search2turn6search0turn6search1turn6search3turn8search0  
- 2024：LangGraph 把 agentic 系统更明确地建模为 stateful graph，并强调持久化/中断/HITL；AutoGen Studio 作为 no-code 多 agent 开发工具进入论文与开源生态。citeturn4search0turn4search15turn19search2  
- 2025：NormCode 把“步骤数据隔离”上升为计划语言语义并主张“审计 by construction”；IsolateGPT 从安全角度提出执行隔离架构，说明“隔离”正成为 agentic 系统的跨领域共识主题。citeturn9search10turn9search0