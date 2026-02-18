# Literature Review Template / 文献综述模板

> **Purpose**: Academic literature review report structure for `literature-review-writer` agent.
> **Usage**: Reference this file via `@knowledge:literature_review_template.md`

---

## OUTPUT FORMAT: Academic Literature Review

### Report Structure

```markdown
# {Topic}: A Literature Review / {Topic} 文献综述

**Abstract / 摘要**
- 研究背景（1-2 句话）
- 主要发现（3-4 句话，按演进路径组织）
- 研究空白（1-2 句话）
- 关键词（5-7 个）

---

## 1. Introduction / 引言

### 1.1 Background and Motivation / 研究背景与动机

**逻辑写法**: 从根基论文引入，说明领域起源

示例：
> 多智能体评估的研究起源于 2023 年中期，当时 LLM 展现出执行复杂任务的潜力，但缺乏系统性的评估方法。[AgentBench](https://arxiv.org/abs/2307.16789) 首次提出了多环境评估框架，为后续研究奠定了基础。

### 1.2 Scope and Organization / 文献综述范围与结构

**逻辑写法**: 明确综述范围，说明组织逻辑

示例：
> 本综述聚焦于 {n} 篇核心论文，按时间演进和主题深化两条线索组织。第 2 节回顾奠基性工作，第 3 节分析研究演进路径，第 4 节按主题深入讨论，第 5 节总结研究空白与未来方向。

---

## 2. Research Evolution / 研究演进

### 2.1 Foundation Work / 奠基性工作

**逻辑写法**: 介绍早期研究的贡献和局限

**[根基论文名称]**

**核心贡献**: [从逻辑分析中提取]

**局限与挑战**:
- 局限 1 → 引发后续研究方向
- 局限 2 → 引发后续研究方向

示例：
> [AgentBench](https://arxiv.org/abs/2307.16789) 提出了多环境评估框架，包含 6 个不同难度的环境。其核心贡献是建立了二分类成功指标，但这种方法**过于粗糙**，无法反映 agent 能力的细微差异。这一局限**直接推动了**后续细粒度评估方法的发展。

### 2.2 Methodological Evolution / 方法论演进

**[演进路径名称]**

**逻辑写法**: 使用演进连接词，体现因果关系

**从 [方法A] 到 [方法B] 的演进**:

早期研究如 [Paper A] 采用 [方法A]，其核心思想是...。**然而**，这种方法面临 [局限]。为解决这些问题，[Paper B] 提出了 [方法B]，通过 [关键技术] 实现了...

**演进驱动力**:
- 驱动因素 1 → 影响 [方面]
- 驱动因素 2 → 影响 [方面]

示例：
> **从二分类指标到细粒度追踪的演进**
>
> [AgentBench](https://arxiv.org/abs/2307.16789) 采用简单的二分类成功/失败指标。然而，这种方法无法区分"完全失败"和"接近成功"的情况。**为解决这一问题**，[AgentBoard](https://arxiv.org/abs/2404.03807) 提出了细粒度的进度追踪指标，包括 `progress_rate` 和 `step_completion`。这种演进**反映了**研究者对评估精度需求的提升。

### 2.3 Paradigm Shifts / 范式转移

**[范式名称]**

**逻辑写法**: 明确说明范式转移的触发点和原因

**从 [旧范式] 到 [新范式]**:

- **触发论文**: [Paper]
- **转移原因**: [从逻辑分析中提取]
- **影响评估**: [从逻辑分析中提取]

示例：
> **范式转移：从单一指标到多维评估**
>
> 这一范式转移由 [AgentBoard](https://arxiv.org/abs/2404.03807) 触发。研究团队发现，单一的成功指标无法全面反映 agent 能力，因此引入了包括成功率、进度率、成本效率在内的多维度评估体系。这一范式**被后续工作广泛采用**，包括 [PLANET](https://arxiv.org/abs/2504.14773)。

---

## 3. Thematic Analysis / 主题分析

### 3.1 [主题一: Evaluation Metrics]

**逻辑写法**: 共同关注点 → 不同方法 → 演进路径 → 不同观点

**共同关注点**:

[Paper A], [Paper B], 和 [Paper C] 都关注评估指标设计，但采用不同方法...

**演进路径**:

```mermaid
graph LR
    A[二分类成功] --> B[细粒度进度]
    B --> C[多维度综合]
```

早期研究采用二分类成功指标，**中期演进**为细粒度进度追踪，**近期发展**出多维度综合评估。

**不同观点**:

- [Paper A] 强调...
- [Paper B] 则认为...
- 这种分歧反映了...

**方法论家族**:

| 方法论 | 代表论文 | 核心方法 | 优势 | 局限 |
|--------|---------|---------|------|------|
| [Family A] | [Paper] | ... | ... | ... |

### 3.2 [主题二: Benchmark Construction]

**逻辑写法**: 方法论对比 → 权衡分析 → 趋势判断

**方法论对比**:

[Paper A] 采用 [方法A]，而 [Paper B] 选择 [方法B]。这两种方法体现了 [权衡点] 的不同选择...

**权衡分析**:

**规模 vs 质量**: [Paper A] 选择小规模高质量数据，而 [Paper B] 追求大规模覆盖。**近期趋势显示**，[Paper C] 尝试通过 [方法] 平衡这一矛盾...

---

## 4. Comparative Analysis / 比较分析

### 4.1 Methodological Trade-offs / 方法论权衡

**[权衡名称]**

**权衡维度**: [从逻辑分析中提取]

**不同选择**:

- **方案 A**: [Paper] 采用 [方法]
  - 优势: ...
  - 劣势: ...

- **方案 B**: [Paper] 采用 [方法]
  - 优势: ...
  - 劣势: ...

**混合方案**: [Paper] 提出了 [混合方法]，试图平衡...

### 4.2 Technical Approaches Comparison / 技术方法对比

**[技术领域]**

**方法 1: [名称]**
- 提出者: [Paper]
- 核心思想: ...
- 验证结果: ...

**方法 2: [名称]**
- 提出者: [Paper]
- 核心思想: ...
- 验证结果: ...

**对比总结**: 方法 1 在 [方面] 优于方法 2，但方法 2 在 [方面] 更有优势...

---

## 5. Research Gaps and Future Directions / 研究空白与未来方向

### 5.1 Identified Gaps / 已识别空白

**逻辑写法**: 空白描述 → 证据支撑 → 可能原因 → 填补方向

**空白 1: [空白名称]**

**描述**: [从逻辑分析中提取]

**证据**:
- [Paper] 指出...
- 现有工作 [方面] 缺失...

**可能原因**:
- 原因 1...
- 原因 2...

**填补方向**:
- 方向 1...
- 方向 2...

示例：
> **空白 1: 缺少安全性评估维度**
>
> 现有 benchmark 主要关注功能完成度，**系统性地忽视**了安全风险。例如，[AgentBench](https://arxiv.org/abs/2307.16789) 和 [ToolBench](https://arxiv.org/abs/2307.13854) 的评估指标中均未包含安全约束。这一空白**可能源于**早期研究侧重于能力证明而非风险控制。**未来工作**可以设计多维度安全框架，包括 adversarial testing 和 safety constraints。

### 5.2 Open Questions / 开放问题

**[问题名称]**

**问题描述**: [从逻辑分析中提取]

**相关研究**:
- [Paper] 探讨了 [方面]
- [Paper] 提出了 [方法]

**可能方向**:
- 方向 1...
- 方向 2...

示例：
> **开放问题 1: 如何平衡评估成本与结果可靠性？**
>
> 这一问题在多篇论文中被提及。 [AgentBench](https://arxiv.org/abs/2307.16789) 选择人工标注确保质量，但成本高昂；[ToolBench](https://arxiv.org/abs/2307.13854) 采用自动生成扩大规模，但质量参差。**近期工作**如 [AgentBoard](https://arxiv.org/abs/2404.03807) 尝试分层采样策略，但成本-效益平衡仍未解决。**可能的方向**包括自适应采样、主动学习质量预测模型。

### 5.3 Future Directions / 未来方向

**逻辑写法**: 基于演进趋势预测未来方向

**方向 1: [方向名称]**

**趋势基础**: 基于现有研究的演进趋势...

**预期发展**: ...

**挑战**: ...

示例：
> **方向 1: 多 agent 协作评估**
>
> **趋势基础**: 现有研究从单 agent 评估逐步扩展到多 agent 场景。 [PLANET](https://arxiv.org/abs/2504.14773) 明确指出了这一空白。
>
> **预期发展**: 未来可能出现专门针对多 agent coordination 的评估指标，包括通信效率、协作质量、角色分工合理性等维度。
>
> **挑战**: 多 agent 场景的复杂性使得评估设计更加困难，需要考虑环境异构性、agent 能力差异等因素。

---

## 6. Conclusion / 结论

### 6.1 Summary of Findings / 主要发现总结

**逻辑写法**: 按演进路径总结

本综述回顾了 {n} 篇核心论文，追踪了 {topic} 领域的演进路径：

1. **奠基阶段** (2023 Q3): [Paper A] 和 [Paper B] 建立了基础框架...
2. **演进阶段** (2024): [Paper C] 提出了... **实现了从 [旧] 到 [新] 的演进**
3. **前沿阶段** (2025): [Paper D] 探索了...

**主要贡献**:
- 贡献 1...
- 贡献 2...

### 6.2 Current State Assessment / 研究现状评估

**逻辑写法**: 评估当前成熟度，指出未解决的问题

当前研究在 [方面] 已较为成熟，体现在... **然而**，[方面] 仍存在显著空白：

1. [空白 1]...
2. [空白 2]...

### 6.3 Recommendations for Future Research / 未来研究建议

**逻辑写法**: 基于空白和问题提出具体建议

**短期方向** (1-2 年):
- 方向 1: 基于 [空白]...
- 方向 2: 基于 [问题]...

**长期方向** (3-5 年):
- 方向 3: 基于 [趋势]...
- 方向 4: 基于 [演进]...

---

## References / 参考文献

[按引用顺序排列，包含所有引用的论文]

1. Author, A., et al. (Year). "Paper Title." *Venue*.
   [arXiv:ID](https://arxiv.org/abs/ID) | [PDF](https://arxiv.org/pdf/ID.pdf)

2. ...
```

---

## Section Word Count Guidelines / 字数分配指南

| 部分 | 占比 | 字数 (3K-5K) | 说明 |
|------|------|-------------|------|
| Abstract | 5% | 150-250 | 简洁摘要 |
| 1. Introduction | 10% | 300-500 | 引入背景，建立读者认知 |
| 2. Research Evolution | 20% | 600-1000 | 演进路径，范式转移 |
| 3. Thematic Analysis | 30% | 900-1500 | 核心分析，深入细节 |
| 4. Comparative Analysis | 15% | 450-750 | 方法对比，权衡分析 |
| 5. Gaps & Future | 15% | 450-750 | 提升视角，综合总结 |
| 6. Conclusion | 5% | 150-250 | 总结发现，建议 |

---

## Related Knowledge Files / 相关知识文件

- `@knowledge:writing_principles.md` - 逻辑连接词、叙事弧模式
- `@knowledge:anti_patterns.md` - 反模式检测与预防
- `@knowledge:quality_validation.md` - 质量验证代码
