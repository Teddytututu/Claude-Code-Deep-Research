# Deep Researcher

> Multi-agent research system for producing comprehensive, citation-rich reports

## What It Does

Input a topic → Get a **Gemini Deep Research-style report** with:
- Academic papers (ArXiv)
- GitHub repositories
- Community discussions (Reddit, HN)
- Citation networks & research gaps
- Bilingual output (Chinese narrative + English terms)

## Quick Start

```
# Basic
深度研究 [topic]
Research [topic]

# With time budget
深度研究 [topic]，给我1小时
Research [topic] in 1 hour
```

## Custom Output Formats

```
# Blog post
深度研究 [topic]，写一篇3000字的博客文章
Research [topic], write a 3000-word blog post

# Slide deck
深度研究 [topic]，生成PPT大纲
Research [topic], create a slide deck outline

# Code examples
深度研究 [topic]，整理代码示例
Research [topic], collect code examples

# Comparison table
深度研究 [topic]，做一个框架对比表
Research [topic], create a framework comparison table

# Technical proposal
深度研究 [topic]，写一份技术提案
Research [topic], write a technical proposal

# JSON format
深度研究 [topic]，输出JSON格式
Research [topic], output as JSON
```

## Output

| Report | Length | Audience |
|--------|--------|----------|
| **Comprehensive Report** | 6,000-8,000 words | Engineers, decision-makers |
| **Literature Review** | 3,000-5,000 words | Researchers, scholars |

## Key Features

- **Parallel Research**: 3 agents search ArXiv, GitHub, and communities simultaneously
- **Quality Assurance**: Independent evaluation + automatic link validation
- **Custom Outputs**: Blog posts, slide decks, code examples, comparison tables, proposals, JSON
- **Citation Graphs**: Mermaid diagrams showing relationships

## Architecture

```
deep-researcher/
├── .claude/
│   ├── agents/          # 18 specialized agents
│   ├── knowledge/       # Research knowledge base
│   └── protocols/       # Execution protocols
├── tools/               # Python utilities
├── CLAUDE.md            # Main orchestrator
└── outputs/             # Generated reports
```

## Framework Support

| Framework | Best For |
|-----------|----------|
| LangGraph | Enterprise, state-heavy workflows |
| CrewAI | Quick deployment, team workflows |
| AutoGen | Research & academia |

## License

MIT

---

[中文版](README_CN.md)
