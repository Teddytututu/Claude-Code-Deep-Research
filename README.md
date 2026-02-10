# Deep Researcher

A multi-agent research orchestration system built on Anthropic's architecture for producing comprehensive, Gemini Deep Research-style reports.

## Features

- **Multi-Agent Orchestration**: Parallel research execution with specialized subagents
- **Performance-Aware Resource Allocation**: Intelligent decision-making based on task complexity
- **Hybrid Memory System**: Semantic, temporal, and episodic memory (MAGMA-inspired)
- **Framework Selection**: Automated framework recommendations (LangGraph, CrewAI, AutoGen)
- **Bilingual Output**: Chinese narrative with English terminology
- **Dual Report Generation**: Comprehensive reports + literature reviews

## Project Structure

```
deep-researcher/
├── .claude/                    # Agent configurations
├── research_data/              # Research data storage
├── research_output/            # Generated reports
├── CLAUDE.md                   # Project instructions
├── hierarchical_orchestrator.py
├── memory_system.py
├── memory_graph.py
├── hybrid_retriever.py
├── framework_selection.py
├── observability.py
├── resilience.py
├── quality_gate.py
├── output_formatter.py
├── research_orchestrator.py
└── research_state.py
```

## Quick Start

```python
from research_orchestrator import ResearchOrchestrator

orchestrator = ResearchOrchestrator()
result = orchestrator.research("multi-agent timeout mechanisms")
```

## Architecture

Based on Anthropic's multi-agent research system:
- **Lead Agent** (Opus 4.5): Coordinates workflow
- **Research Subagents** (Sonnet 4): Parallel academic, GitHub, and community research
- **Report Writers**: Synthesize findings into comprehensive reports

## License

MIT
