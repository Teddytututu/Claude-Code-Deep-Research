# Bilingual Format Guide / 双语格式指南

> **Purpose**: Bilingual output format guidelines for report writers.
> **Usage**: Reference this file via `@knowledge:bilingual_format_guide.md`

---

## Bilingual Format Levels

### Level 1: Term-Only (Recommended Default)

仅专业术语使用英文：
- 示例: "中央编排（Centralized Orchestration）模式适合简单场景"
- 适用: 大多数技术报告

### Level 2: Concept

概念术语 + 括号内英文：
- 示例: "编排（Orchestration）是指协调多个智能体的过程"
- 适用: 概念解释部分

### Level 3: Full Bilingual

完整句子可中英混合：
- 示例: "研究显示，多智能体系统（Multi-Agent Systems）可带来90.2%的性能提升"
- 适用: Executive Summary

**Default: Level 1 (Term-Only)**

---

## Language Style Specification

```
✓ CORRECT (Level 1):
中央编排（Centralized Orchestration）模式适合简单场景，
但单一节点可能成为瓶颈（Single Point of Failure）。
LangGraph 提供了 StateGraph 模式实现分层架构。

✗ INCORRECT:
Centralized Orchestration is suitable for simple scenarios,
but may have Single Point of Failure.
```

---

## Citation Format Standards

### Academic Papers / 学术论文

```markdown
中文：Liu 等人（2023）在 ACL 会议上指出...
英文链接：[arXiv:2307.03172](https://arxiv.org/abs/2307.03172) | [PDF](https://arxiv.org/pdf/2307.03172.pdf) (850+ citations)

完整格式：
Liu 等人（2023）. "Lost in the Middle." ACL.
[arXiv:2307.03172](https://arxiv.org/abs/2307.03172) | [PDF](https://arxiv.org/pdf/2307.03172.pdf) (850+ citations)
```

### GitHub Projects / GitHub 项目

```markdown
中文：LangGraph 提供了 StateGraph 模式...
英文链接：[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) ⭐ 15k+

完整格式：
**LangGraph** (langchain-ai): StateGraph orchestration framework
GitHub: [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) ⭐ 15k+
```

### Community Discussions / 社区讨论

```markdown
中文：Reddit r/LocalLLaMA 社区反映...
英文链接：[Discussion Thread](https://reddit.com/r/LocalLLaMA/comments/xyz) (200+ upvotes)

完整格式：
"Context management on long running agents is burning me out"
- Reddit [r/LLMDevs](https://reddit.com/r/LLMDevs/comments/xyz), 150+ upvotes
```

---

## Chinglish Avoidance

```
❌ AVOID:
- "Make agent coordination good"
- "The research shows important results"
- "Using multi-agent can improve performance"

✅ PREFER:
- "智能体协调显著提升性能" / "Agent coordination significantly improves performance"
- "研究表明..." / "Research indicates..."
- "采用多智能体架构可提升性能" / "Multi-agent architecture improves performance"
```

---

## Mathematical Formula Format

### Inline Formula

使用 `$...$` 作为行内公式：

```markdown
The coordination overhead scales as $O(n^2)$ where $n$ is the number of agents.
The 45% threshold rule states $P(\text{single-agent}) < 0.45$.
```

### Block Formula

使用 `$$...$$` 作为块级公式：

```markdown
The token cost multiplier is:

$$ \text{Cost}_{\text{multi-agent}} = \frac{\text{Tokens}_{\text{multi-agent}}}{\text{Tokens}_{\text{single-agent}}} \approx 15\times $$
```

---

## Quality Checklist

- [ ] 所有英文术语首次出现时标注中文
- [ ] 使用 Level 1 双语格式（term-only）
- [ ] 避免 Chinglish 表达
- [ ] 数学公式使用 LaTeX 格式
- [ ] 代码块和配置保持英文
- [ ] 报告使用中文叙述 + 英文术语
