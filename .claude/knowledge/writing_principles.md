# Writing Principles / 写作原则

> **Purpose**: Logical connectors, narrative arc patterns, and synthesis techniques for literature review writing.
> **Usage**: Reference this file via `@knowledge:writing_principles.md`

---

## 1. Logical Connectors / 逻辑连接词

### 演进关系 (Evolutionary Relationships)
- 然而、但是、尽管如此
- 为解决这一问题
- 这一局限推动了后续研究
- 反映了研究者对...需求的提升
- 沿着这一方向、进一步发展
- 随之出现、接续而来
- 在此基础上、承袭这一思路

### 继承关系 (Inheritance Relationships)
- 基于...的工作
- 扩展了...的方法
- 改进了...的指标
- 沿用了...的框架
- 继承自、源于、发展自
- 在...基础上进一步
- 延续了...的思路

### 对比关系 (Comparative Relationships)
- 相比之下、与...不同
- 另一方面、反之
- ...则认为、...采取了不同路径
- 与之形成对照的是
- 不同的是、区别在于
- 值得注意的是

### 因果关联 (Causal Relationships)
- 由于...、因此...
- 导致...、促使...
- 引发了、触发了
- 产生于、源于
- 带来了、造成

### 综合关系 (Synthetic Relationships)
- 综合来看、总体而言
- 多篇研究表明、现有文献显示
- 研究者们共同关注
- 一致认为、普遍观点
- 形成了...共识

### 转折递进 (Transitional Relationships)
- 诚然...但...
- 虽然...但是...
- 不仅...而且...
- 一方面...另一方面...
- 更为重要的是
- 尤其值得注意的是

---

## 2. Narrative Arc Patterns / 叙事弧模式

### 问题-解决方案弧 (Problem-Solution Arc)

```python
NarrativeArc = {
    "Problem": "早期研究面临的共同挑战",
    "Initial_Attempts": "初步解决方案及其局限",
    "Breakthrough": "关键突破论文",
    "Refinement": "后续改进工作",
    "Current_State": "当前最优方案",
    "Remaining_Challenges": "尚未解决的问题"
}
```

**示例**:
> 早期研究者面临着如何有效评估多智能体的共同挑战。[Paper A] 首先尝试了二分类指标，但过于粗糙。**为解决这一问题**，[Paper B] 引入了细粒度追踪。**进一步地**，[Paper C] 提出了多维度评估体系。**当前**，这一范式已被广泛采用，**但**在评估效率方面仍存在挑战。

### 概念演化弧 (Concept Evolution Arc)

```python
ConceptEvolutionArc = {
    "Primitive_Form": "概念的原始形态",
    "Elaboration": "概念的细化与扩展",
    "Transformation": "概念的根本转变",
    "Integration": "概念与其他概念的融合",
    "Standardization": "概念的标准确立"
}
```

### 方法论家族弧 (Methodological Family Arc)

```python
MethodologicalFamilyArc = {
    "Common_Ancestry": "共同的理论基础",
    "Branch_Divergence": "不同分支的形成",
    "Convergence": "分支间的融合",
    "Hybrid_Forms": "混合方法的出现"
}
```

---

## 3. Metacomment Guidelines / 元评论指导原则

**元评论的作用**: 帮助读者理解文献间的关系，而非仅描述单个研究

### 有效的元评论模式

```python
# 解释选择逻辑
"本文选择从...角度切入分析，因为..."

# 预告后续内容
"接下来的分析将展示..."

# 总结已述内容
"综上所述，现有研究..."

# 指出争议
"关于...，研究者们存在分歧..."

# 强调重要性
"这一工作的重要性在于..."

# 提示读者注意
"值得注意的是..."

# 说明组织逻辑
"本节按照...顺序组织..."
```

**示例**:
> **值得注意的是**，虽然上述研究都关注评估指标设计，但它们在方法论选择上呈现出明显的分歧。接下来的分析将展示这种分歧如何导致了评估范式的根本转变。

---

## 4. Synthesis Techniques / 综合技术

### 跨论文综合 (Cross-Paper Synthesis)

```python
def synthesize_across_papers(papers, dimension):
    """综合多篇论文在特定维度的发现"""

    # 1. 识别共同点
    common_findings = extract_commonalities(papers, dimension)

    # 2. 识别差异点
    differences = extract_differences(papers, dimension)

    # 3. 解释差异原因
    explanations = explain_differences(differences)

    # 4. 提取演进模式
    patterns = extract_evolutionary_patterns(papers, dimension)

    return {
        "consensus": common_findings,
        "divergence": differences,
        "explanations": explanations,
        "patterns": patterns
    }
```

**主题综合示例**:
> 在评估指标设计方面，现有研究形成了**明显的方法论家族**。[Paper A], [Paper B], 和 [Paper C] 共同关注细粒度评估，但采用了不同的技术路径。其中，[Paper A] 和 [Paper B] 都采用基于规则的方法，而 [Paper C] 创新性地引入了学习型指标。**这种分歧反映了**研究者对评估自动化程度的不同期待。

### 空白综合 (Gap Synthesis)

```python
def synthesize_research_gaps(papers):
    """综合研究空白，避免逐个列举"""

    # 1. 按维度归类空白
    gaps_by_dimension = group_by_dimension(papers.gaps)

    # 2. 识别空白间的关系
    gap_relationships = identify_relationships(gaps_by_dimension)

    # 3. 提取系统性空白
    systematic_gaps = extract_systematic_gaps(gap_relationships)

    return {
        "surface_gaps": gaps_by_dimension,
        "structural_gaps": gap_relationships,
        "systematic_gaps": systematic_gaps
    }
```

---

## 5. Hourglass Structure / 漏斗结构

文献综述应遵循"漏斗结构"（从广泛到具体再到广泛）：

```python
HourglassStructure = {
    "Broad_Introduction": {
        "领域整体背景",
        "广泛的研究问题",
        "核心概念定义"
    },

    "Narrow_Focus": {
        "特定研究问题",
        "关键论文深入分析",
        "方法细节讨论",
        "实证结果对比"
    },

    "Broad_Synthesis": {
        "跨主题综合",
        "研究趋势总结",
        "广泛未来方向",
        "对领域的影响评估"
    }
}
```

### 各部分的字数分配建议

| 部分 | 占比 | 说明 |
|------|------|------|
| Broad Introduction | 15% | 引入背景，建立读者认知 |
| Narrow Focus | 55% | 核心分析，深入细节 |
| Broad Synthesis | 30% | 提升视角，综合总结 |

---

## Related Knowledge Files / 相关知识文件

- `@knowledge:literature_review_template.md` - 报告结构模板
- `@knowledge:anti_patterns.md` - 反模式检测与预防
- `@knowledge:quality_validation.md` - 质量验证代码
