# Performance Metrics / 性能指标

## Overview / 概述

Performance-aware decision framework for multi-agent systems based on research from Google/MIT and Anthropic.

---

## The 45% Threshold Rule / 45% 阈值规则

**Based on Google/MIT study**:

```
IF (single_agent_success_rate < 45% AND task_value > cost):
    RETURN "Use multi-agent system"
    EXPECTED: +90.2% performance improvement, 15x token cost
ELSE:
    RETURN "Single-agent sufficient"
```

**Key insight**: Multi-agent systems are only beneficial when single-agent success rate is below 45%.

---

## Token Cost Multipliers / Token 成本倍数

**Source**: [Anthropic Engineering Research](https://www.anthropic.com/engineering/multi-agent-research-system)

| Metric | Value | Description |
|--------|-------|-------------|
| Chat → Single Agent | 4x tokens | Baseline increase |
| Chat → Multi-Agent | 15x tokens | Full orchestration |
| Single agent efficiency | 67 tasks/1K tokens | Tasks per token |
| Multi-agent efficiency | 14-21 tasks/1K tokens | Lower per-token efficiency |

**Decision formula**:
```
Expected Cost = Base Tokens × Multiplier
Single-Agent: T × 1
Multi-Agent: T × 15
```

---

## Performance vs Single-Agent / 相对单智能体性能

| Scenario | Improvement | Source |
|----------|-------------|--------|
| General complex queries | **+90.2%** | Anthropic research |
| Parallel tasks | +80.9% | Financial analysis |
| Sequential tasks | -70% | Minecraft planning |
| Hierarchical orchestration | +50-80% | Depends on structure |

**Parallel vs Sequential**:
- **Parallel tasks**: Multi-agent excels (multiple subagents work independently)
- **Sequential tasks**: Multi-agent underperforms (coordination overhead)

---

## Coordination Overhead Scaling / 协调开销扩展

**Potential interactions formula**:
```
Potential interactions = n(n-1)/2
where n = number of agents

2 agents: 1 interaction
4 agents: 6 interactions
10 agents: 45 interactions
```

**Implication**: As agent count increases, coordination overhead grows quadratically.

**Mitigation**: Hierarchical structure reduces coordination overhead:
- Flat: All agents can interact with each other
- Hierarchical: Agents only interact within their layer

---

## Decision Framework / 决策框架

### When to Use Multi-Agent / 何时使用多智能体

✅ **Use Multi-Agent When**:
- Single-agent success rate < 45% (Google/MIT threshold)
- Task has parallelizable aspects (embarrassingly parallel)
- Information exceeds single context window
- Interfacing with numerous complex tools
- Task value justifies 15x cost increase

❌ **Use Single-Agent When**:
- Sequential dependencies between steps
- Single-agent success rate > 45%
- Cost-sensitive applications
- Sub-second latency required

---

### Query Type Classification / 查询类型分类

| Query Type | Success Rate | Recommendation |
|------------|--------------|----------------|
| Simple fact-finding | >60% | Single-agent |
| Direct comparison | 50-60% | Single-agent or lightweight multi |
| Complex research | <45% | Multi-agent (hierarchical) |
| Deep synthesis | <35% | Multi-agent (full orchestration) |

---

## Performance Estimation / 性能估算

### Single-Agent Success Rate Estimation

**Complexity indicators**:
```python
complexity_keywords = [
    "comprehensive", "detailed", "in-depth", "analysis",
    "vs", "versus", "comparison", "framework", "architecture"
]

has_complexity = any(kw in query.lower() for kw in complexity_keywords)
word_count = len(query.split())

if has_complexity or word_count > 5:
    estimated_success = 0.35  # Below 45% threshold
else:
    estimated_success = 0.60  # Above threshold
```

### Parallelizability Assessment

```python
parallelizable_aspects = []

if "paper" in query.lower() or "academic" in query.lower():
    parallelizable_aspects.append("academic_research")

if "github" in query.lower() or "code" in query.lower():
    parallelizable_aspects.append("github_analysis")

if "community" in query.lower() or "discussion" in query.lower():
    parallelizable_aspects.append("community_listening")
```

---

## Cost-Benefit Analysis / 成本效益分析

### Decision Matrix

| Single-Agent Success | Parallelizable Aspects | Decision |
|---------------------|----------------------|----------|
| <45% | ≥2 | Use Multi-Agent (+90.2%, 15x cost) |
| <45% | 0-1 | Consider lightweight multi |
| ≥45% | Any | Single-Agent sufficient |

### Expected Improvement Calculation

```
if success_rate < 0.45 and parallelizable >= 2:
    expected_improvement = "+90.2%"
    expected_cost_multiplier = "15x"
    recommendation = "Use hierarchical multi-agent"
else:
    expected_improvement = "baseline"
    expected_cost_multiplier = "1x"
    recommendation = "Use single-agent"
```

---

## Time-Budgeted Execution / 基于时间的执行

### Per-Agent Time Allocation

**For parallel execution with time budget**:
```
Per-Agent Time = Total Budget × 80%
(20% coordination overhead)

Example: "给我1小时"
→ Per-agent: 48 minutes
→ 3 agents parallel: 144 total minutes of query time
→ You wait: ~60 minutes for report
```

### Industry Timeout Standards

| Platform | Default | Production Reality |
|----------|---------|-------------------|
| Palantir AIP | 5 min | 90% failure rate |
| AWS Bedrock | 15 min idle | Async with /ping |
| LangGraph | Configurable | Checkpoint resume |

---

## CLI Usage / 命令行使用

```bash
# Analyze query performance characteristics
python "tools\performance_analyzer.py" --analyze "深度研究 multi-agent frameworks"

# Compare single vs multi-agent for a query
python "tools\performance_analyzer.py" --compare --query "LangGraph vs CrewAI"

# Show performance metrics history
python "tools\performance_analyzer.py" --history
```

---

## Related Knowledge / 相关知识

- **hierarchical_orchestration.md**: Hierarchical structure to reduce overhead
- **orchestration_patterns.md**: Orchestration pattern selection
- **performance-predictor**: Agent that uses these metrics for decision-making
