# Anti-Pattern Prevention / 反模式预防

> **Purpose**: Detection patterns and prevention strategies for common literature review mistakes.
> **Usage**: Reference this file via `@knowledge:anti_patterns.md`

---

## Eight Common Literature Review Mistakes / 八大常见错误

### 1. Mechanical Listing / 机械罗列 (最常见)

```python
# 检测模式
mechanical_listing_patterns = [
    r"Paper.*做了.*\.\s*Paper.*做了",  # 连续的"论文A做了X。论文B做了Y。"
    r"作者.*提出.*\.\s*作者.*提出",    # 连续的"作者A提出X。作者B提出Y。"
    r"[A-Z]\..*?\.\s*[A-Z]\..*?\.",    # A... B... C... 模式
]

# 预防措施
prevention_strategies = {
    "使用演进连接词": "然而、为解决这一问题、进一步地",
    "按主题组织": "而非按论文组织",
    "综合描述": "多句论文描述合并为一句"
}
```

❌ **错误示例**:
> Paper A 提出了方法 X。Paper B 提出了方法 Y。Paper C 提出了方法 Z。

✅ **正确示例**:
> Paper A 首先提出了方法 X，但其局限在于...。**为解决这一问题**，Paper B 和 Paper C 分别从不同角度进行了改进，其中 Paper B 专注于...，而 Paper C 则探索了...

---

### 2. Annotated Bibliography Style / 注释书目风格

```python
# 检测模式
annotated_bibliography_patterns = [
    r"这篇论文.+(主要|重点|关注)",  # "这篇论文主要研究了..."
    r"作者.+(提出|发现|表明)",      # "作者提出了..."
    r"研究.+(旨在|目标)",          # "本研究旨在..."
]

# 预防：主题导向而非论文导向
topic_oriented_approach = {
    "主题句": "先提出共同主题",
    "综合描述": "将多篇论文整合描述",
    "对比分析": "强调论文间的关系"
}
```

❌ **错误示例**:
> ## 2. 相关工作
> ### 2.1 Paper A
> 这篇论文主要研究了...
> ### 2.2 Paper B
> 这篇论文关注于...

✅ **正确示例**:
> ## 2. 评估指标设计的演进路径
> 现有研究在评估指标设计上呈现出清晰的演进路径。早期工作如 [Paper A] 采用了...，**然而**，这种方法面临...的挑战。**为解决这一问题**，后续研究 [Paper B] 和 [Paper C] 分别探索了...

---

### 3. Chronological Only / 纯按时间组织

```python
# 检测模式
chronological_only_patterns = [
    r"20\d{2}年.*20\d{2}年.*20\d{2}年",  # 连续列举年份
    r"首先.*其次.*最后.*",                # 机械的第一第二最后
]

# 预防：结合主题和时间
hybrid_organization = {
    "时间演进": "展示发展脉络",
    "主题深化": "深入关键问题",
    "方法论家族": "组织技术方法"
}
```

❌ **错误示例**:
> 2023年，Paper A 提出了...。2024年，Paper B 提出了...。2025年，Paper C 提出了...

✅ **正确示例**:
> 在评估方法论方面，现有研究形成了**三个主要范式**。**早期的二分类范式**（2023-2024 Q1）以 [Paper A] 为代表，其核心思想是...。**然而**，这种方法的局限性直接催生了**细粒度评估范式**（2024 Q2-Q3），[Paper B] 和 [Paper C] 分别从不同角度实现了...。**近期**，**多维度综合评估范式**正在兴起...

---

### 4. Lack of Synthesis / 缺乏综合

```python
# 检测
lack_of_synthesis_indicators = {
    "没有综合句": "段落结尾没有总结性陈述",
    "缺乏比较": "没有对比不同研究",
    "无模式提取": "没有提取共同模式"
}

# 预防：每段结尾添加综合
synthesis_templates = [
    "综上所述，现有研究在...方面形成了...共识",
    "这些工作共同揭示了...趋势",
    "从上述分析可以看出，研究者们..."
]
```

---

### 5. No Critical Analysis / 缺乏批判性分析

```python
# 检测
no_critical_analysis_indicators = {
    "只有优点": "只描述贡献，不提局限",
    "无比较评估": "不比较不同方法"
}

# 预防：平衡描述
critical_analysis_framework = {
    "贡献": "研究的主要贡献",
    "局限": "方法的局限性",
    "适用场景": "方法的适用范围",
    "权衡": "不同选择的权衡"
}
```

---

### 6. Missing Evolution Narrative / 缺失演进叙事

```python
# 检测
missing_evolution_indicators = {
    "无演进词": "没有使用演进、发展、从...到...等词汇",
    "无因果链": "没有说明A如何导致B"
}

# 预防：明确演进路径
evolution_narrative_template = """
早期研究 [Paper A] 提出了 [方法A]，但面临 [局限]。
这一局限直接推动了 [Paper B] 的研究，其核心创新在于...
进一步地，[Paper C] 扩展了这一方向，引入了...
这种演进反映了 [趋势/需求变化]。
"""
```

---

### 7. Weak Introduction/Conclusion / 引言/结论薄弱

```python
# 检测
weak_introduction_conclusion = {
    "无引言": "直接进入第一篇论文描述",
    "无总结": "最后一篇论文结束后突然结束",
    "无连贯性": "引言和结论无呼应"
}

# 预防：使用漏斗结构
strong_introduction_template = """
[广泛背景] 领域整体情况
↓
[具体聚焦] 本综述范围和关注点
↓
[结构预告] 各章节内容预告
"""

strong_conclusion_template = """
[总结发现] 主要发现回顾
↓
[评估现状] 当前研究成熟度
↓
[未来方向] 基于空白的建议
"""
```

---

### 8. Inadequate Citation Integration / 引用整合不当

```python
# 检测
inadequate_citation_patterns = [
    r"\[Paper A\].*\[Paper B\].*\[Paper C\]",  # 引用堆砌
    r"\[.*\](?:, \[.*\]){2,}",                 # 多个引用无整合
]

# 预防：引用整合策略
citation_integration_strategies = {
    "代表性引用": "选择最具代表性的论文详细描述",
    "合并引用": "同类研究合并引用",
    "关系明确": "明确引用间的关系"
}
```

---

## Anti-Pattern Detection Checklist / 反模式检测清单

```python
def validate_anti_patterns(review_content):
    """检测反模式"""

    checks = {
        "机械罗列": detect_mechanical_listing(review_content),
        "注释书目风格": detect_annotated_bibliography_style(review_content),
        "纯时间组织": detect_chronological_only(review_content),
        "缺乏综合": detect_lack_of_synthesis(review_content),
        "无批判分析": detect_no_critical_analysis(review_content),
        "缺失演进叙事": detect_missing_evolution(review_content),
        "引言结论薄弱": detect_weak_introduction_conclusion(review_content),
        "引用整合不当": detect_inadequate_citation_integration(review_content)
    }

    return all(not v for v in checks.values()), checks
```

---

## Quick Reference / 快速参考

| 反模式 | 检测信号 | 预防策略 |
|--------|---------|---------|
| 机械罗列 | Paper A... Paper B... Paper C... | 使用演进连接词，按主题组织 |
| 注释书目 | "这篇论文主要研究了..." | 主题导向，综合描述 |
| 纯时间组织 | 2023年... 2024年... 2025年... | 结合主题和时间，方法论家族 |
| 缺乏综合 | 段落结尾无总结句 | 每段添加综合总结 |
| 无批判 | 只描述优点不提局限 | 平衡贡献与局限 |
| 缺失演进 | 无"演进"、"发展"等词汇 | 明确演进路径和因果链 |
| 引言薄弱 | 直接进入论文描述 | 漏斗结构引入 |
| 引用堆砌 | [A], [B], [C] 无整合 | 合并同类引用 |

---

## Related Knowledge Files / 相关知识文件

- `@knowledge:literature_review_template.md` - 报告结构模板
- `@knowledge:writing_principles.md` - 写作原则和叙事弧
- `@knowledge:quality_validation.md` - 质量验证代码
