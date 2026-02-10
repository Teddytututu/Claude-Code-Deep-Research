# Deep Researcher

A multi-agent research orchestration system built on Anthropic's architecture for producing comprehensive, Gemini Deep Research-style reports.

## Overview

This system employs the **Orchestrator-Worker pattern**, leveraging parallel multi-agent collaboration to conduct deep research across multiple dimensions: academic papers, GitHub repositories, and community discussions.

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Agent Orchestration** | Parallel specialized subagents with 90% speed improvement |
| **Performance-Aware Resource Allocation** | Intelligent decisions based on 45% threshold rule and cost-benefit analysis |
| **MAGMA Hybrid Memory** | Three-layer architecture: Semantic + Temporal + Episodic memory |
| **Framework Selection** | Auto-recommend LangGraph, CrewAI, AutoGen, and more |
| **Dual Report Generation** | Comprehensive report (decision-maker oriented) + Literature review (scholar oriented) |
| **Bilingual Output** | Chinese narrative + English terminology with LaTeX formula support |
| **Observability** | Token usage, latency, and cost tracking with visualization |

## Quick Start

### Basic Usage

```python
from research_orchestrator import ResearchOrchestrator

# Initialize research orchestrator
orchestrator = ResearchOrchestrator()

# Execute deep research
result = orchestrator.research(
    topic="multi-agent timeout mechanisms",
    time_budget_minutes=60  # Optional: time budget
)

# Get dual reports
print(result.comprehensive_report)   # Comprehensive report
print(result.literature_review)      # Literature review
```

### Specifying Time Budget

```python
# Each subagent gets full available time (parallel execution)
# Example: 60min budget → ~48min per agent
result = orchestrator.research(
    topic="Agent timeout mechanisms",
    time_budget_minutes=60
)
```

### Framework Preference

```python
result = orchestrator.research(
    topic="multi-agent framework comparison",
    framework_preference="LangGraph"  # Or "CrewAI", "AutoGen"
)
```

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query                                │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  Phase -1: Performance Predictor                            │
│  - Single-agent success rate assessment                     │
│  - Parallelizability analysis                               │
│  - Cost-benefit decision                                    │
└────────────────────────────┬────────────────────────────────┘
                             │ Use Multi-Agent?
                  ┌──────────┴──────────┐
                  │ Yes                 │ No → Single-agent direct answer
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 0: Framework Selector                                │
│  - "AutoGen: Fast, CrewAI: Stable, LangGraph: Powerful"     │
│  - Production readiness assessment                          │
└────────────────────────────┬────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Parallel Research Execution (Research Subagents)  │
│  ├─ academic-researcher   (ArXiv papers, citation networks) │
│  ├─ github-watcher        (Repo analysis, code examples)    │
│  └─ community-listener    (Community discussions, feedback) │
└────────────────────────────┬────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2a: Logic Analysis (Literature Analyzer)            │
│  - Citation relationships & inheritance chains              │
│  - Thematic clusters & methodological families              │
│  - Technical evolution paths                                │
└────────────────────────────┬────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2b: Dual Report Synthesis (Dual Report Writers)     │
│  ├─ deep-research-report-writer → comprehensive_report.md  │
│  └─ literature-review-writer    → literature_review.md     │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
deep-researcher/
├── .claude/                        # Agent configurations
│   ├── agents/                     # Subagent specifications
│   │   ├── academic-researcher.md
│   │   ├── github-watcher.md
│   │   ├── community-listener.md
│   │   ├── performance-predictor.md
│   │   ├── framework-selector.md
│   │   └── ...
│   ├── hooks/                      # Research hook scripts
│   └── mcp-servers.json            # MCP server configuration
│
├── research_data/                  # Research data storage
│   ├── academic_research_output.json
│   ├── github_research_output.json
│   ├── community_research_output.json
│   └── logic_analysis.json
│
├── research_output/                # Generated reports
│   ├── {topic}_comprehensive_report.md
│   └── {topic}_literature_review.md
│
├── CLAUDE.md                       # Project instructions
│
├── Core Modules                    # Core modules
│   ├── research_orchestrator.py    # Main orchestrator
│   ├── hierarchical_orchestrator.py # Hierarchical orchestration
│   ├── research_state.py           # Research state management
│   │
│   ├── memory_system.py            # MAGMA memory system
│   ├── memory_graph.py             # Semantic memory graph
│   ├── hybrid_retriever.py         # Hybrid retrieval
│   │
│   ├── framework_selection.py      # Framework selection
│   ├── observability.py            # Observability
│   ├── resilience.py              # Resilience system
│   ├── quality_gate.py            # Quality gate
│   └── output_formatter.py        # Output formatting
│
└── README.md
```

## Framework Selection Matrix

| Framework | Companies Deployed | Latency Overhead | Time to Production | Use Case |
|-----------|-------------------|------------------|-------------------|----------|
| **LangGraph** | ~400 | 8% (lowest) | 2 months | State-heavy workflows, enterprise |
| **CrewAI** | 150+ (60% Fortune 500) | 24% | 2 weeks | Team workflows, quick deployment |
| **AutoGen** | Microsoft ecosystem | 15% | - | Research & academia |
| **Swarm** | 0 | 0% | N/A | ⚠️ Educational only |

## Performance Metrics

Based on Anthropic official research:

| Metric | Value | Source |
|--------|-------|--------|
| Single-agent efficiency | 67 tasks/1K tokens | Anthropic Engineering |
| Multi-agent efficiency | 14-21 tasks/1K tokens | Anthropic Engineering |
| Token cost multiplier | 15x | Anthropic Engineering |
| Performance improvement | +90.2% | Anthropic Research |
| Parallel task improvement | +80.9% | Anthropic Research |

## Decision Criteria

**When to use multi-agent systems:**

- Single-agent success rate < 45% (Google/MIT threshold)
- Task has parallelizable aspects
- Information exceeds single context window
- Task value justifies 15x cost increase

**When to use single-agent:**

- Sequential dependencies between steps
- Single-agent success rate > 45%
- Cost-sensitive applications
- Sub-second latency required

## Requirements

### Python Dependencies

```bash
pip install anthropic
pip install networkx  # For graph operations
pip install matplotlib  # Visualization
```

### MCP Servers (Optional)

The system supports 20-30 MCP server configurations, with 5-6 recommended per session:

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

## Output Format

### Comprehensive Report

- **Target Audience**: Technical decision-makers, engineers
- **Word Count**: 6,000-8,000 words
- **Content**: Comprehensive coverage of academic research + engineering practice + community feedback
- **Features**: Citation relationship graph (Mermaid), clickable citations, bilingual terminology

### Literature Review

- **Target Audience**: Researchers, scholars
- **Word Count**: 3,000-5,000 words
- **Content**: Academic-focused, logic-driven
- **Features**: Evolution path analysis, research gap identification

## Academic Foundation

This system is based on the following research:

| Paper | Topic |
|------|-------|
| MAGMA (arXiv:2601.03236) | Multi-Graph Agentic Memory Architecture |
| AgentOrchestra (arXiv:2506.12508) | Hierarchical Multi-Agent Framework |
| GraphRAG (arXiv:2507.03608) | Hybrid Retrieval System |
| BudgetThinker (arXiv:2508.17196) | Budget-Aware Execution |

## License

MIT License

---

**Author**: Deep Research System
**Updated**: 2026-02-10

[中文版 README](README_CN.md)
