# Knowledge Base Usage Guide / 知识库使用指南

## Overview / 概述

本知识库 (`.claude/knowledge/`) 包含从 Python 模块提取的核心逻辑，供 Agent 通过 `@knowledge` 引用读取。

**Current Stats / 当前统计**:
- **Knowledge Files**: 16 files
- **Python Tools**: 14 modules
- **Agent Configs**: 15 agents

---

## Knowledge Base Files / 知识库文件

| File | Description | Status | Reading Agents |
|------|-------------|--------|----------------|
| `framework_selection.md` | Framework decision logic | ✅ Active | framework-selector, performance-predictor |
| `orchestration_patterns.md` | Multi-agent coordination patterns | ✅ Active | All orchestration-related |
| `quality_checklist.md` | Quality validation criteria | ✅ Active | deep-research-report-writer, literature-review-writer, link-validator |
| `report_templates.md` | Output format specifications | ✅ Active | deep-research-report-writer, literature-review-writer, task_handle |
| `resilience_patterns.md` | Retry and recovery mechanisms | ✅ Active | timeout-specialist |
| `observability_patterns.md` | Metrics and monitoring patterns | ✅ Active | mcp-coordinator |
| `logic_analysis.md` | Citation and logic analysis | ✅ Active | literature-analyzer |
| `research_state.md` | State management patterns | ✅ Active | All research agents |
| `performance_metrics.md` | Cost-benefit analysis data | ✅ Active | performance-predictor |
| `visualization_patterns.md` | Visualization generation patterns | ✅ Active | visualization-generator |
| `hierarchical_orchestration.md` | 3-layer orchestration | ✅ Active | All agents |
| `cross_domain_tracker.md` | Cross-domain tracking + bridging entities | ✅ Active | cross-domain-tracker, literature-analyzer, deep-research-report-writer, literature-review-writer, visualization-generator, github-watcher, community-listener |
| `memory_graph.md` | Semantic knowledge graph + PageRank | ✅ Active | All agents (via memory_system) |
| `memory_system.md` | MAGMA 3-layer memory + sessions | ✅ Active | All research + analysis agents |
| `hybrid_retriever.md` | GraphRAG retrieval | 📋 Planned | hybrid_retriever |
| `knowledge_template.md` | Template for new knowledge files | 📝 Template | - |

---

## Python Tools / Python 工具

| Tool | Description | CLI Command | Category |
|------|-------------|-------------|----------|
| `framework_selection.py` | Framework recommendation logic | `--recommend --metrics --tree` | A (Core) |
| `research_orchestrator.py` | Main research workflow | `--query --dry-run --parallel` | A (Core) |
| `quality_gate.py` | Quality validation | `--findings --report --check` | A (Core) |
| `output_formatter.py` | Report formatting | `--comprehensive --literature-review` | A (Core) |
| `observability.py` | Metrics and monitoring | `--metrics --cost-report` | B (Operations) |
| `resilience.py` | Retry and circuit breaker | `--test-retry --test-circuit-breaker` | B (Operations) |
| `checkpoint_manager.py` | State persistence | `--save --load --list` | B (Operations) |
| `research_state.py` | Research state management | `--init --update --status` | B (Operations) |
| `visualization.py` | Chart and graph generation | `--data-dir --output-dir --type` | B (Operations) |
| `memory_system.py` | MAGMA memory implementation | ✅ Active | B (Operations) |
| `hierarchical_orchestrator.py` | 3-layer orchestration | `--layers --agents --execute` | C (Future) |
| `hybrid_retriever.py` | GraphRAG retrieval | `--vector --graph --hybrid` | C (Future) |
| `memory_graph.py` | Knowledge graph operations | ✅ Active | B (Operations) |
| `memory_graph_cli.py` | Memory graph CLI | `--build --query --visualize --stats` | B (Operations) |
| `generate_visualizations.py` | Batch visualization generator | `--data-dir --output-dir` | B (Operations) |
| `cross_domain_tracker.py` | Cross-domain relationship tracking | `--bridging --stats --graph --semantic-query` | B (Operations) |

---

## Agent Configs / 代理配置

### Decision-Support Agents (6) / 决策支持代理

| Agent | Knowledge Files | CLI Tools | Purpose |
|-------|----------------|-----------|---------|
| `performance-predictor.md` | performance_metrics.md, framework_selection.md | framework_selection.py | Cost-benefit analysis |
| `framework-selector.md` | framework_selection.md, orchestration_patterns.md | framework_selection.py | Framework recommendation |
| `mcp-coordinator.md` | observability_patterns.md | observability.py | MCP optimization |
| `handoff-designer.md` | (inline documentation) | - | Handoff pattern design |
| `readiness-assessor.md` | (inline documentation) | - | Production readiness |
| `timeout-specialist.md` | resilience_patterns.md | resilience.py | Timeout budget allocation |

### Research Subagents (3) / 研究子代理

| Agent | Knowledge Files | CLI Tools | Purpose |
|-------|----------------|-----------|---------|
| `academic-researcher.md` | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | memory_graph_cli.py | Academic paper research + MAGMAMemory |
| `github-watcher.md` | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | memory_graph_cli.py, cross_domain_tracker.py | GitHub ecosystem research + cross-domain extraction |
| `community-listener.md` | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | memory_graph_cli.py, cross_domain_tracker.py | Community discussion listening + cross-domain extraction |

### Analysis Agents (2) / 分析代理

| Agent | Knowledge Files | CLI Tools | Purpose |
|-------|----------------|-----------|---------|
| `cross-domain-tracker.md` | cross_domain_tracker.md, memory_graph.md, memory_system.md | cross_domain_tracker.py | Cross-domain relationship analysis (Phase 1.5) |
| `literature-analyzer.md` | logic_analysis.md, research_state.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | research_state.py, memory_graph_cli.py, cross_domain_tracker.py | Logic relationship analysis + cross-domain synthesis |

### Report Synthesis Agents (6) / 报告合成代理

| Agent | Knowledge Files | CLI Tools | Purpose |
|-------|----------------|-----------|---------|
| `deep-research-report-writer.md` | quality_checklist.md, report_templates.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | output_formatter.py, quality_gate.py, memory_graph_cli.py, cross_domain_tracker.py | Comprehensive report generation + cross-domain insights |
| `literature-review-writer.md` | quality_checklist.md, report_templates.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | output_formatter.py, quality_gate.py, memory_graph_cli.py | Literature review generation + implementation gaps |
| `link-validator.md` | quality_checklist.md, report_templates.md | - | Link validation |
| `visualization-generator.md` | visualization_patterns.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | visualization.py, memory_graph_cli.py, cross_domain_tracker.py | Visualization generation + cross-domain graphs |
| `task_handle.md` | report_templates.md, quality_checklist.md | output_formatter.py | Custom task output |

---

## Agent Integration / Agent 集成

### Adding Knowledge to Agent Config

在 `.claude/agents/{agent}.md` 中添加:

```markdown
## KNOWLEDGE BASE

@knowledge: .claude/knowledge/{relevant_file}.md
@knowledge: .claude/knowledge/{another_file}.md

## EXECUTABLE UTILITIES

当需要量化分析时，可调用：
```bash
python "tools\{module}.py" --{command} {args}
```
```

### Example: framework-selector.md

```markdown
## KNOWLEDGE BASE

@knowledge: .claude/knowledge/framework_selection.md
@knowledge: .claude/knowledge/orchestration_patterns.md

## EXECUTABLE UTILITIES

当需要量化分析时，可调用：
```bash
python "tools\framework_selection.py" --recommend --query "{query}"
python "tools\framework_selection.py" --metrics
```
```

### Example: literature-analyzer.md

```markdown
## KNOWLEDGE BASE

@knowledge: .claude/knowledge/logic_analysis.md
@knowledge: .claude/knowledge/research_state.md

## EXECUTABLE UTILITIES

当需要状态管理时，可调用：
```bash
python "tools\research_state.py" --load-data research_data --status
python "tools\research_state.py" --update --logic-analysis
```
```

---

## CLI Commands / 命令行命令

### Category A: Core Tools / 核心工具

```bash
# Framework Selection
python "tools\framework_selection.py" --recommend
python "tools\framework_selection.py" --metrics
python "tools\framework_selection.py" --tree

# Research Orchestrator
python "tools\research_orchestrator.py" --query "Multi-agent frameworks"
python "tools\research_orchestrator.py" --dry-run

# Quality Gate
python "tools\quality_gate.py" --findings research_data/academic_research_output.json
python "tools\quality_gate.py" --report research_output/topic_report.md

# Output Formatter
python "tools\output_formatter.py" --comprehensive
python "tools\output_formatter.py" --literature-review
```

### Category B: Operations Tools / 运维工具

```bash
# Observability
python "tools\observability.py" --metrics
python "tools\observability.py" --cost-report

# Resilience
python "tools\resilience.py" --test-retry
python "tools\resilience.py" --test-circuit-breaker

# Checkpoint Management
python "tools\checkpoint_manager.py" --save research_data
python "tools\checkpoint_manager.py" --load latest
python "tools\checkpoint_manager.py" --list

# Research State
python "tools\research_state.py" --init
python "tools\research_state.py" --update --logic-analysis
python "tools\research_state.py" --status

# Visualization
python "tools\visualization.py" --data-dir research_data --output-dir research_output/visualizations
python "tools\visualization.py" --type citation-network
```

### Category C: Future Tools / 未来工具

```bash
# Memory Graph CLI (NEW - Active)
python "tools\memory_graph_cli.py" --build
python "tools\memory_graph_cli.py" --query 2501.03236
python "tools\memory_graph_cli.py" --visualize --format html
python "tools\memory_graph_cli.py" --stats

# Generate Visualizations
python "tools\generate_visualizations.py"

# Hierarchical Orchestrator
python "tools\hierarchical_orchestrator.py" --layers 3
python "tools\hierarchical_orchestrator.py" --execute --query "complex topic"

# Hybrid Retriever (GraphRAG)
python "tools\hybrid_retriever.py" --vector --graph
python "tools\hybrid_retriever.py" --hybrid --rrf

# Cross-Domain Tracker
python "tools\cross_domain_tracker.py" --track --domains academic,github,community
python "tools\cross_domain_tracker.py" --analyze --relationships
```

---

## Verification / 验证

### Test Python CLI Availability

```bash
# Category A: Core Tools
python "tools\framework_selection.py" --help
python "tools\research_orchestrator.py" --help
python "tools\quality_gate.py" --help
python "tools\output_formatter.py" --help

# Category B: Operations Tools
python "tools\observability.py" --help
python "tools\resilience.py" --help
python "tools\checkpoint_manager.py" --help
python "tools\research_state.py" --help
python "tools\visualization.py" --help
```

### Verify Knowledge Base Files

```bash
# Check all knowledge files exist
ls ".claude\knowledge\"

# Expected output (16 files):
# framework_selection.md
# orchestration_patterns.md
# quality_checklist.md
# report_templates.md
# resilience_patterns.md
# observability_patterns.md
# logic_analysis.md
# research_state.md
# performance_metrics.md
# visualization_patterns.md
# hierarchical_orchestration.md
# cross_domain_tracker.md
# memory_graph.md
# memory_system.md
# hybrid_retriever.md
# knowledge_template.md
```

### Verify Agent Configs

```bash
# Check all agent configs exist
ls ".claude\agents\"

# Expected output (15 files):
# performance-predictor.md
# framework-selector.md
# mcp-coordinator.md
# readiness-assessor.md
# timeout-specialist.md
# handoff-designer.md
# academic-researcher.md
# github-watcher.md
# community-listener.md
# literature-analyzer.md
# deep-research-report-writer.md
# literature-review-writer.md
# link-validator.md
# visualization-generator.md
# task_handle.md
```

---

## Notes / 说明

### Design Principles / 设计原则

- **知识库优先**: Agent 应优先读取知识库，而非直接解析 Python 代码
- **CLI 可选**: CLI 工具用于量化分析，知识库用于定性决策
- **一致性**: Python 代码和知识库保持逻辑一致
- **版本控制**: 知识库文件应与 Python 代码同步更新

### Category Definitions / 类别定义

| Category | Name | Description | Usage |
|----------|------|-------------|--------|
| **A** | Core Tools | Production-ready, actively used | Every research session |
| **B** | Operations | Monitoring and state management | As needed for ops/debug |
| **C** | Future | Advanced features, research-stage | For complex queries only |

### Adding New Knowledge / 添加新知识

1. Create new knowledge file from template:
   ```bash
   cp .claude/knowledge/knowledge_template.md .claude/knowledge/new_feature.md
   ```

2. Add to relevant agent config:
   ```markdown
   @knowledge: .claude/knowledge/new_feature.md
   ```

3. Update this README with new entry

4. If executable, create corresponding Python tool in `tools/`

---

## Workflow Integration / 工作流集成

### Phase-based Knowledge Access

```
Phase -1: Performance Prediction
├── Agent: performance-predictor
├── Knowledge: performance_metrics.md, framework_selection.md
└── CLI: framework_selection.py --recommend

Phase 0: Framework Selection
├── Agent: framework-selector
├── Knowledge: framework_selection.md, orchestration_patterns.md
└── CLI: framework_selection.py --tree

Phase 0.5: MCP Coordination
├── Agent: mcp-coordinator
├── Knowledge: observability_patterns.md
└── CLI: observability.py --metrics

Phase 1: Research Execution
├── Agents: academic-researcher, github-watcher, community-listener
├── Knowledge: None (MCP direct)
└── CLI: research_orchestrator.py --parallel

Phase 2a: Logic Analysis
├── Agent: literature-analyzer
├── Knowledge: logic_analysis.md, research_state.md
└── CLI: research_state.py --update --logic-analysis

Phase 2b: Report Synthesis
├── Agents: deep-research-report-writer, literature-review-writer
├── Knowledge: quality_checklist.md, report_templates.md
└── CLI: output_formatter.py --comprehensive, quality_gate.py --check

Phase 2d: Link Validation
├── Agent: link-validator
├── Knowledge: quality_checklist.md, report_templates.md
└── CLI: None (uses webReader directly)

Phase 2e: Task Handler (Optional)
├── Agent: task_handle
├── Knowledge: report_templates.md, quality_checklist.md
└── CLI: output_formatter.py --custom
```

---

## Quick Reference / 快速参考

### Agent → Knowledge Mapping

```
performance-predictor     → performance_metrics.md, framework_selection.md
framework-selector        → framework_selection.md, orchestration_patterns.md
mcp-coordinator           → observability_patterns.md
timeout-specialist        → resilience_patterns.md
readiness-assessor        → (inline)
handoff-designer          → (inline)
literature-analyzer       → logic_analysis.md, research_state.md
deep-research-report-writer → quality_checklist.md, report_templates.md
literature-review-writer  → quality_checklist.md, report_templates.md
link-validator            → quality_checklist.md, report_templates.md
visualization-generator   → visualization_patterns.md
task_handle               → report_templates.md, quality_checklist.md
academic-researcher       → (MCP direct, no knowledge file)
github-watcher            → (MCP direct, no knowledge file)
community-listener        → (MCP direct, no knowledge file)
```

### Knowledge → CLI Mapping

```
framework_selection.md     → framework_selection.py
orchestration_patterns.md  → research_orchestrator.py
quality_checklist.md       → quality_gate.py
report_templates.md        → output_formatter.py
resilience_patterns.md     → resilience.py
observability_patterns.md  → observability.py
logic_analysis.md          → research_state.py
research_state.md          → research_state.py, checkpoint_manager.py
visualization_patterns.md  → visualization.py
performance_metrics.md     → framework_selection.py, observability.py
```
