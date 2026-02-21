# Report Generation Protocols

报告生成协议 - 双报告系统（综合报告 + 文献综述）

**Version**: v1.0 (2026-02-21)

---

## Output System

| 报告类型 | Agent | 目标读者 | 字数 | 特点 |
|---------|-------|---------|------|------|
| **综合报告** | `deep-research-report-writer` | 技术决策者 | 6,000-8,000 | 全面覆盖 |
| **文献综述** | `literature-review-writer` | 研究者 | 3,000-5,000 | 逻辑驱动 |

---

## Report Deployment

```python
# Phase 2b: Dual Report Synthesis (run in parallel)
Task(
    subagent_type="deep-research-report-writer",
    prompt=f"""Synthesize research findings into a comprehensive report.

INPUT DATA:
- Academic research: research_data/academic_researcher_output.json
- GitHub research: research_data/github_researcher_output.json
- Community research: research_data/community_researcher_output.json

TOPIC: {original_query}
OUTPUT: research_output/{sanitized_topic}_comprehensive_report.md
"""
)

Task(
    subagent_type="literature-review-writer",
    prompt=f"""Generate academic literature review based on logic analysis.

INPUT DATA:
- Research data: research_data/*.json
- Logic analysis: research_data/logic_analysis.json

OUTPUT: research_output/{sanitized_topic}_literature_review.md
"""
)
```

---

## Comprehensive Report Structure

```markdown
# {Topic} - 深度研究报告

## Executive Summary
[8-12 条核心发现，中英混合 + 可点击引用]

## 1. 理论框架
[概念定义，数学公式，根基论文]

## 2. 学术版图
[Root Papers, SOTA, Survey 分类]

## 3. 开源生态
[技术流派，架构对比，代码示例]

## 4. 社区视角
[实践反馈，共识点，痛点]

## 5. 综合分析
[跨域关系，实现差距]

## 6. 实践建议
[基于发现的可操作建议]

## 7. 参考资料
[所有引用，可点击]
```

---

## Literature Review Structure

```markdown
# {Topic} - 文献综述

## 摘要
[200-300 字总结]

## 1. 引言
[研究背景，问题定义]

## 2. 理论基础
[核心概念，关键定义]

## 3. 研究方法演进
[按时间或流派组织]

## 4. 主题聚类分析
[方法族，技术范式]

## 5. 技术演进路径
[从根基到 SOTA 的发展]

## 6. 研究空白与开放问题
[未解决的问题，未来方向]

## 参考文献
