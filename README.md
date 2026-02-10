# Deep Researcher

> A multi-agent research orchestration system for producing Gemini Deep Research-style comprehensive reports

## Overview

**Deep Researcher** is an intelligent research orchestration system built on Anthropic's multi-agent architecture. It uses the **orchestrator-worker pattern** to conduct deep research across academic papers, GitHub repositories, and community discussions—then synthesizes findings into dual comprehensive reports.

**Key Insight**: This is a **Claude Code-native system**. The orchestrator logic lives in `CLAUDE.md`, which coordinates specialized subagents via the `Task` tool. The Python modules provide reference implementations and supporting infrastructure.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query                                │
│              "深度研究 Agent 超时机制，给我1小时"             │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  Phase -1: Performance Predictor                            │
│  - Should we use multi-agent? (45% threshold rule)          │
│  - Cost-benefit analysis (15x tokens, 90.2% improvement)     │
└────────────────────────────┬────────────────────────────────┘
                             │ Use Multi-Agent?
                  ┌──────────┴──────────┐
                  │ Yes                 │ No → Direct answer
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 0: Framework Selector                                │
│  - "AutoGen快、CrewAI稳、LangGraph强"                         │
│  - Production readiness assessment                          │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  Phase 1: Parallel Research Execution                       │
│  ├─ academic-researcher   (ArXiv papers, citation networks) │
│  ├─ github-watcher        (Repo analysis, code examples)    │
│  └─ community-listener    (Community discussions, feedback) │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  Phase 2a: Logic Analysis                                   │
│  - Citation relationships, thematic clusters                │
│  - Technical evolution paths, research gaps                 │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  Phase 2b: Dual Report Synthesis                            │
│  ├─ comprehensive_report.md   (6,000-8,000 words)           │
│  └─ literature_review.md      (3,000-5,000 words)           │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### Basic Query

```
深度研究 [topic]
Research [topic]
```

### With Time Budget

**中文**:
```
深度研究 [topic]，给我1小时
研究 [topic]，30分钟
分析 [topic]，限时2小时
```

**English**:
```
Research [topic] in 1 hour
Study [topic], give me 30 minutes
Analyze [topic], 2h deadline
```

**Important**: Subagents run in **parallel**. Each agent gets the full available time (not divided!)

| Query | Time Budget | Per-Agent Time | Total Research |
|-------|-------------|----------------|---------------|
| `深度研究 Agent 超时机制，给我1小时` | 60 min | ~48 min each | 144 min of parallel research |
| `Research multi-agent frameworks in 30min` | 30 min | ~24 min each | 72 min of parallel research |

### With Framework Preference

```
深度研究 [topic]，使用 LangGraph
Research [topic], framework: AutoGen
```

## Decision Framework

### When to Use Multi-Agent

Based on Google/MIT research:

```
IF (single_agent_success_rate < 45% AND task_value > cost):
    → Use multi-agent system
    → Expected: +90.2% performance, 15x token cost
ELSE:
    → Single-agent sufficient
```

**Use Multi-Agent When**:
- Single-agent success rate < 45%
- Task has parallelizable aspects
- Information exceeds single context window
- Task value justifies 15x cost increase

### Framework Selection Matrix

| Framework | Companies | Latency | Time to Production | Best For |
|-----------|-----------|---------|-------------------|----------|
| **LangGraph** | ~400 | 8% | 2 months | State-heavy workflows, enterprise |
| **CrewAI** | 150+ (60% Fortune 500) | 24% | 2 weeks | Team workflows, quick deployment |
| **AutoGen → AG2** | Microsoft ecosystem | 15% | - | Research & academia |
| **Swarm** | 0 | 0% | N/A | ⚠️ Educational only |

**Community Consensus**: "AutoGen快、CrewAI稳、LangGraph强"

## Output Format

### Dual Report System

| Report | Target Audience | Length | Focus |
|--------|----------------|--------|-------|
| **Comprehensive Report** | Technical decision-makers, engineers | 6,000-8,000 words | Academic + Engineering + Community |
| **Literature Review** | Researchers, scholars | 3,000-5,000 words | Academic, logic-driven |

### Report Features

- **Bilingual**: Chinese narrative + English terminology
- **LaTeX formulas**: Mathematical notation support
- **Clickable citations**: All sources linked
- **Citation graphs**: Mermaid diagrams showing relationships
- **Evolution paths**: Technical change over time
- **Research gaps**: Open questions identified

## Project Structure

```
deep-researcher/
├── .claude/                        # Claude Code configuration
│   ├── agents/                     # Subagent specifications (12 agents)
│   │   ├── academic-researcher.md
│   │   ├── github-watcher.md
│   │   ├── community-listener.md
│   │   ├── performance-predictor.md
│   │   ├── framework-selector.md
│   │   ├── mcp-coordinator.md
│   │   ├── timeout-specialist.md
│   │   ├── handoff-designer.md
│   │   ├── readiness-assessor.md
│   │   ├── literature-analyzer.md
│   │   ├── deep-research-report-writer.md
│   │   └── literature-review-writer.md
│   ├── hooks/                      # Workflow automation
│   │   ├── detect_research_intent.py
│   │   ├── token_budget_check.py
│   │   └── research_hooks.json
│   ├── utils/                      # Utilities
│   │   └── checkpoint_manager.py
│   └── mcp-servers.json            # MCP server configuration
│
├── research_data/                  # Runtime research data
│   ├── academic_research_output.json
│   ├── github_research_output.json
│   ├── community_research_output.json
│   └── logic_analysis.json
│
├── research_output/                # Generated reports
│   ├── {topic}_comprehensive_report.md
│   └── {topic}_literature_review.md
│
├── Core Python Modules             # Reference implementations
│   ├── research_orchestrator.py    # Main orchestrator (534 lines)
│   ├── hierarchical_orchestrator.py # 3-layer orchestration
│   ├── memory_system.py            # MAGMA memory architecture
│   ├── memory_graph.py             # Semantic knowledge graph
│   ├── hybrid_retriever.py         # GraphRAG hybrid retrieval
│   ├── framework_selection.py      # Framework selection engine
│   ├── observability.py            # Metrics & tracing
│   ├── resilience.py               # Error recovery & circuit breaker
│   ├── quality_gate.py             # LLM-as-judge validation
│   └── output_formatter.py         # Bilingual report formatting
│
├── CLAUDE.md                       # ⭐ Primary orchestrator logic
├── README.md                       # This file
└── README_CN.md                    # Chinese version
```

## Agent Inventory

### Decision-Support Agents (6)

| Agent | Purpose |
|-------|---------|
| **performance-predictor** | Cost-benefit analysis (45% threshold rule) |
| **framework-selector** | Framework recommendation |
| **mcp-coordinator** | MCP tool optimization |
| **handoff-designer** | Agent coordination patterns |
| **readiness-assessor** | Production readiness evaluation |
| **timeout-specialist** | Timeout budget allocation |

### Research Subagents (3)

| Agent | Tools | Output |
|-------|-------|--------|
| **academic-researcher** | ArXiv search, paper download/read | Papers, citations, full-text analysis |
| **github-watcher** | Repo structure, file reading, search | Projects, architecture, code examples |
| **community-listener** | Web reader, web search | Discussions, consensus, community feedback |

### Report Synthesis Agents (3)

| Agent | Output |
|-------|--------|
| **literature-analyzer** | logic_analysis.json |
| **deep-research-report-writer** | comprehensive_report.md |
| **literature-review-writer** | literature_review.md |

## Academic Foundation

This system is grounded in the following research:

| Paper | Topic | arXiv ID |
|------|-------|----------|
| **MAGMA** | Multi-Graph Agentic Memory Architecture | [2601.03236](https://arxiv.org/abs/2601.03236) |
| **AgentOrchestra** | Hierarchical Multi-Agent Framework | [2506.12508](https://arxiv.org/abs/2506.12508) |
| **GraphRAG** | Hybrid Retrieval System | [2507.03608](https://arxiv.org/abs/2507.03608) |
| **BudgetThinker** | Budget-Aware Execution | [2508.17196](https://arxiv.org/abs/2508.17196) |
| **ALAS** | Timeout Policies, 60% token reduction | [2511.03094](https://arxiv.org/abs/2511.03094) |
| **B2MAPO** | Batch optimization, 78.7% time reduction | [2407.15077](https://arxiv.org/abs/2407.15077) |

## Performance Metrics

Based on Anthropic official research:

| Metric | Value | Source |
|--------|-------|--------|
| Single-agent efficiency | 67 tasks/1K tokens | Anthropic Engineering |
| Multi-agent efficiency | 14-21 tasks/1K tokens | Anthropic Engineering |
| Token cost multiplier | 15x | Anthropic Engineering |
| Performance improvement | +90.2% | Anthropic Research |
| Parallel task improvement | +80.9% | Anthropic Research |

## MCP Integration

The system uses MCP (Model Context Protocol) for external data access:

**Optimization Rules**:
- Total MCPs configured: 20-30
- Active per session: 5-6
- Total active tools: < 80

**Key MCP Servers**:
- **ArXiv**: Academic paper search and retrieval
- **GitHub (zread)**: Repository analysis
- **Web Search Prime**: General web search
- **Web Reader**: Content parsing from blogs/discussions

## Production Features

### Observability Stack
- Token usage, latency, and cost tracking
- Distributed agent execution traces
- Real-time event logging

### Resilience System
- Retry policies with exponential backoff
- Circuit breaker for cascading failure prevention
- Checkpoint-based recovery
- Graceful degradation

### Quality Gate System
- LLM-as-judge pattern (88% vs 61% human consistency)
- Citation accuracy validation
- Source quality assessment
- Completeness checks

## Configuration

### MCP Servers (Optional)

Configure in `.claude/mcp-servers.json`:

```json
{
  "mcp_servers": {
    "arxiv": {
      "command": "npx",
      "args": ["-y", "@arxiv/mcp-server"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@github/mcp-server"]
    }
  }
}
```

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
DEFAULT_TIME_BUDGET_MINUTES=60
DEFAULT_FRAMEWORK=LangGraph
```

## License

MIT License

---

**Architecture**: Claude Code-native orchestrator with specialized subagents
**Updated**: 2026-02-10

[中文版 README](README_CN.md)
