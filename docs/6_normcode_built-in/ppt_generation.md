# PPT Generation

**A component-based presentation generator that produces HTML and PPTX output from content, style guides, and templates.**

**Location**: `direct_infra_experiment/tests/ppt生成_v2/`
**Status**: Production
**Category**: Content generation workflow

---

## Overview

The PPT Generation plan demonstrates NormCode's ability to orchestrate complex, multi-step creative workflows. Given a topic, audience, and reference materials, it generates a full presentation through analysis, outlining, per-slide content generation, template selection, and final assembly — producing both HTML (for preview) and PPTX (for delivery).

### Component System

The plan uses a component-based design rather than fixed templates:

**6 Layouts**: `full`, `left_right`, `main_sidebar`, `top_bottom`, `three_column`, `header_body`

**14 Component Types**: `text_bullets`, `text_paragraph`, `diagram_flow`, `diagram_sequence`, `diagram_mindmap`, `diagram_timeline`, `diagram_pie`, `diagram_quadrant`, `table`, `highlight_box`, `process_steps`, `icon_grid`, `stat_cards`, `quote`

---

## The Plan (`.ncds`)

```
:<:{演示文稿包}
    <= 完成演示文稿报告，总结生成的工件和输出路径
    /: HTML和PPTX都从相同的组件化内容JSON文件生成
    
    /: ═══════════════════════════════════════════════════════════════
    /: 基础输入
    /: ═══════════════════════════════════════════════════════════════
    
    <- {项目目录}
        /: 基础值：项目目录的文件路径
    
    <- {演示主题}
    <- {目标受众}
    <- {期望长度}
    
    <- [内容参考元数据]
        /: 领域/主题材料：{name, path, type}
    
    <- [模板参考元数据]
        /: HTML幻灯片模板文件：{name, path, type}
    
    <- [内容风格参考元数据]
        /: 内容写作风格、受众适应、演示技巧指南：{name, path, type}
    
    <- [模板选择参考元数据]
        /: HTML模板选择指南：{name, path, type}
    
    <- [PPTX布局参考元数据]
        /: PPTX布局选择指南：{name, path, type}
    
    /: ═══════════════════════════════════════════════════════════════
    /: 阶段0 - 从路径加载参考内容
    /: ═══════════════════════════════════════════════════════════════
    
    /: 步骤0.1：加载内容参考
    <- [内容参考]
        <= 对于内容参考元数据中的每个元数据
            <= 返回此迭代的加载内容
            <- {加载的内容}
                <= 从文件路径加载内容
                <- {当前内容元数据}
                <- {项目目录}
        <- [内容参考元数据]
        <* {当前内容元数据}
    
    /: 步骤0.2：加载模板文件
    <- [模板参考]
        <= 对于模板参考元数据中的每个元数据
            <= 返回此迭代的加载模板
            <- {加载的模板}
                <= 从文件路径加载模板
                <- {当前模板元数据}
                <- {项目目录}
        <- [模板参考元数据]
        <* {当前模板元数据}
    
    /: 步骤0.3：加载内容风格指南
    <- [内容风格参考]
        <= 对于内容风格参考元数据中的每个元数据
            <= 返回此迭代的加载指南
            <- {加载的内容风格}
                <= 从文件路径加载指南
                <- {当前内容风格元数据}
                <- {项目目录}
        <- [内容风格参考元数据]
        <* {当前内容风格元数据}
    
    /: 步骤0.4：加载模板选择指南
    <- [模板选择参考]
        <= 对于模板选择参考元数据中的每个元数据
            <= 返回此迭代的加载指南
            <- {加载的模板选择指南}
                <= 从文件路径加载指南
                <- {当前模板选择元数据}
                <- {项目目录}
        <- [模板选择参考元数据]
        <* {当前模板选择元数据}
    
    /: 步骤0.5：加载PPTX布局指南
    <- [PPTX布局参考]
        <= 对于PPTX布局参考元数据中的每个元数据
            <= 返回此迭代的加载指南
            <- {加载的PPTX布局指南}
                <= 从文件路径加载指南
                <- {当前PPTX布局元数据}
                <- {项目目录}
        <- [PPTX布局参考元数据]
        <* {当前PPTX布局元数据}
    
    /: ═══════════════════════════════════════════════════════════════
    /: 阶段1 - 内容规划
    /: ═══════════════════════════════════════════════════════════════
    
    /: 步骤1.1：收集各类参考
    <- {所有内容参考}
        <= 将所有内容参考收集到单个对象中
        <- [内容参考]
    
    <- {所有模板参考}
        <= 将所有模板参考收集到单个对象中
        <- [模板参考]
    
    <- {内容风格指南}
        <= 将内容风格指南收集到单个对象中
        <- [内容风格参考]
    
    <- {模板选择指南}
        <= 将模板选择指南收集到单个对象中
        <- [模板选择参考]
    
    <- {PPTX布局指南}
        <= 将PPTX布局指南收集到单个对象中
        <- [PPTX布局参考]
    
    /: 步骤1.2：分析需求
    <- {已保存的分析}
        <= 将分析保存到项目目录
        <- {分析}
            <= 分析演示文稿需求：主题深度、受众水平、语调、关键主题
            <- {演示主题}
            <- {目标受众}
            <- {期望长度}
            <- {所有内容参考}
            <- {内容风格指南}
        <- {项目目录}
    
    /: 步骤1.3：生成大纲
    <- {已保存的大纲}
        <= 将大纲保存到项目目录
        <- {大纲}
            <= 创建带幻灯片规格的大纲，每个都包含内容提示
            <- {分析}
            <- {所有内容参考}
            <- {内容风格指南}
        <- {项目目录}
    
    /: ═══════════════════════════════════════════════════════════════
    /: 阶段2 - 提取幻灯片规格
    /: ═══════════════════════════════════════════════════════════════
    
    <- [幻灯片规格]
        <= 运行extract_slide_specs脚本将大纲解析为幻灯片规格
        <- {大纲}
    
    /: ═══════════════════════════════════════════════════════════════
    /: 阶段3 - 组件化幻灯片生成循环
    /: ═══════════════════════════════════════════════════════════════
    
    <- [所有已渲染的幻灯片]
        <= 对于幻灯片规格中的每个幻灯片规格
            <= 返回此迭代的幻灯片渲染结果
            
            /: 步骤3.1：获取相关内容上下文
            <- {幻灯片内容上下文}
                <= 获取此特定幻灯片的相关内容
                <- {当前幻灯片规格}
                <- {所有内容参考}
            
            /: 步骤3.2：生成组件化内容
            <- {幻灯片内容}
                <= 生成组件化幻灯片内容
                <- {当前幻灯片规格}
                <- {幻灯片内容上下文}
                <- {分析}
                <- {内容风格指南}
            
            /: 步骤3.3：保存内容JSON
            <- {已保存的幻灯片内容}
                <= 将幻灯片内容保存到项目目录
                <- {幻灯片内容}
                <- {当前幻灯片规格}
                <- {项目目录}
            
            /: 步骤3.4：生成 Mermaid 图表代码
            <- {增强后的幻灯片内容}
                <= 为 diagram 组件生成 Mermaid 代码
                <- {幻灯片内容}
                <- {幻灯片内容上下文}
            
            /: 步骤3.5：选择HTML模板
            <- {选定的html模板}
                <= 为此内容选择最佳HTML模板
                <- {增强后的幻灯片内容}
                <- {当前幻灯片规格}
                <- {所有模板参考}
                <- {模板选择指南}
            
            /: 步骤3.5b：加载HTML模板内容
            <- {html模板内容}
                <= 从模板路径加载HTML模板内容
                <- {选定的html模板}
                <- {项目目录}
            
            /: 步骤3.6：渲染HTML幻灯片
            <- {已保存的html幻灯片}
                <= 将html幻灯片保存到项目目录
                <- {html幻灯片}
                    <= 通过用内容填充模板来渲染html幻灯片
                    <- {增强后的幻灯片内容}
                    <- {html模板内容}
                    <- {当前幻灯片规格}
                    <- {内容风格指南}
                <- {项目目录}
            
            /: 步骤3.7：选择PPTX布局
            <- {选定的pptx布局}
                <= 为此内容选择最佳PPTX布局
                <- {增强后的幻灯片内容}
                <- {当前幻灯片规格}
                <- {PPTX布局指南}
            
            /: 步骤3.8：保存PPTX幻灯片规格
            <- {已保存的pptx幻灯片规格}
                <= 将pptx幻灯片规格保存到项目目录
                <- {pptx幻灯片规格}
                    <= 创建pptx幻灯片规格
                    <- {增强后的幻灯片内容}
                    <- {选定的pptx布局}
                    <- {当前幻灯片规格}
                <- {项目目录}

            /: 捆绑HTML和PPTX结果
            <- {幻灯片渲染结果}
                <= 将此幻灯片的html和pptx结果捆绑在一起
                <- {已保存的html幻灯片}
                <- {已保存的pptx幻灯片规格}
            
        <- [幻灯片规格]
        <* {当前幻灯片规格}
    
    /: ═══════════════════════════════════════════════════════════════
    /: 阶段4 - 组装最终输出
    /: ═══════════════════════════════════════════════════════════════
    
    <- {所有幻灯片集合}
        <= 将所有已渲染的幻灯片收集到单个对象中
        <- [所有已渲染的幻灯片]
    
    <- {已保存的html演示文稿}
        <= 将html演示文稿保存到项目目录
        <- {html演示文稿}
            <= 组装带导航的html幻灯片
            <- {所有幻灯片集合}
            <- {大纲}
            <- {项目目录}
        <- {项目目录}
    
    <- {已保存的pptx演示文稿}
        <= 将pptx演示文稿保存到项目目录
        <- {pptx演示文稿}
            <= 从幻灯片规格组装pptx
            <- {所有幻灯片集合}
            <- {大纲}
            <- {项目目录}
        <- {项目目录}
    
    /: ═══════════════════════════════════════════════════════════════
    /: 最终分组
    /: ═══════════════════════════════════════════════════════════════
    
    <- {所有报告输出}
        <= 收集所有生成的输出以供最终报告
        <- {已保存的html演示文稿}
        <- {已保存的pptx演示文稿}
        <- {项目目录}
```

---

## Phase-by-Phase Walkthrough

### Phase 0: Load References

Five parallel loops load different types of reference material from file paths:
- Content references (domain materials)
- HTML template files
- Content style guides
- Template selection guides
- PPTX layout guides

Each loop uses the same pattern: iterate over metadata, load file content per item.

### Phase 1: Content Planning

1. **Group** all loaded references into single objects (syntactic, free)
2. **Analyze** requirements — topic depth, audience level, tone, key themes (LLM)
3. **Generate** structured outline with per-slide specifications (LLM)

### Phase 2: Slide Extraction

A Python script parses the outline JSON into a list of individual slide specifications. This is a deterministic operation — no LLM cost.

### Phase 3: Per-Slide Loop

The core of the plan — each slide is generated through 8 steps:

| Step | Operation | Type |
|------|-----------|------|
| 3.1 | Get relevant content context | LLM (filters content for this slide) |
| 3.2 | Generate component content JSON | LLM (text, bullets, diagrams) |
| 3.3 | Save content JSON | Script |
| 3.4 | Generate Mermaid diagram code | LLM (if slide has diagrams) |
| 3.5 | Select HTML template | LLM |
| 3.5b | Load HTML template file | Script |
| 3.6 | Render HTML slide | LLM (fill template with content) |
| 3.7 | Select PPTX layout | LLM |
| 3.8 | Save PPTX slide spec | Script |

Each slide receives only its own specification and relevant content — it cannot see other slides' data. This is data isolation applied to creative generation.

### Phase 4: Assembly

Two parallel operations assemble the final outputs:
- **HTML assembly** — combines all rendered HTML slides with navigation
- **PPTX assembly** — builds PowerPoint from all slide specifications

---

## Client Interfaces

This plan has multiple client interfaces, demonstrating the **Clients** concept:

| Client | Type | Location |
|--------|------|----------|
| Web wizard (no template) | Browser | `new_website/demo/ppt生成/page-flows.html` |
| Web wizard (with template) | Browser | `new_website/demo/ppt上传模板/page-flows.html` |
| CLI client | Python | `mock_clients/ppt_client.py` |
| Desktop GUI | Python/HTML | `mock_clients/ppt_clients/run_ppt_gui.py` |

### Variants

| Variant | Approach | Location |
|---------|----------|----------|
| `ppt生成` | Content-first, optional user template | `tests/ppt生成/` |
| `ppt生成_v2` | Component-based, HTML + PPTX (this doc) | `tests/ppt生成_v2/` |
| `html构建ppt` | Template-driven, PPTX → analysis → rebuild | `tests/html构建ppt/` |

---

## Key Design Patterns

| Pattern | How It's Used |
|---------|--------------|
| **Per-item loop** | Each slide generated independently with scoped inputs |
| **Data isolation** | Slide 5 cannot see content of slide 3 |
| **Component abstraction** | Layout and component types are separate concerns |
| **Multi-output** | Same content JSON produces both HTML and PPTX |
| **Reference loading loops** | 5 parallel loops load different reference types identically |
| **Mermaid integration** | LLM generates diagram specs, rendered by scripts |

---

## See Also

- **[README](README.md)** — Overview of all built-in plans
- **[NormCode Server Guide](../5_tools/normcode_server_guide.md)** — Where this plan gets deployed
- **[Ecosystem Overview](../1_intro/ecosystem.md)** — PPT clients demonstrate the end-user role

---

**Last Updated**: March 2026
