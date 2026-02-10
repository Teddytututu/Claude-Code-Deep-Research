# Hierarchical Orchestration / 分层编排

## Overview / 概述

Three-layer hierarchical multi-agent orchestration pattern based on AgentOrchestra framework.

Based on:
- [AgentOrchestra: A Hierarchical Multi-Agent Framework](https://arxiv.org/abs/2506.12508) [arXiv:2506.12508](https://arxiv.org/abs/2506.12508)
- [A Taxonomy of Hierarchical Multi-Agent Systems](https://arxiv.org/abs/2508.12683) [arXiv:2508.12683](https://arxiv.org/abs/2508.12683)

---

## Three-Layer Hierarchy / 三层架构

### Layer 1: Meta-Orchestrator (Strategic) / 元编排器（战略层）

**Responsibilities**:
- Query analysis and complexity assessment
- Resource allocation (performance-aware)
- Framework selection
- Domain coordinator assignment
- Result synthesis

**Decision Criteria**:
```python
# 45% Threshold Rule (Google/MIT)
IF single_agent_success_rate < 45% AND parallelizable_aspects >= 2:
    RETURN "hierarchical_multi_agent"  # +90.2% improvement, 15x tokens
```

**Query Analysis**:
```python
@dataclass
class QueryAnalysis:
    complexity_level: str  # "high" or "low"
    estimated_single_agent_success: float  # 0.0 to 1.0
    parallelizable_aspects: List[str]  # ["academic_research", "github_analysis", ...]
    word_count: int
```

---

### Layer 2: Domain Coordinators (Coordination) / 域协调器（协调层）

**Domain-Specific Coordination**:

| Coordinator | Domain | Workers |
|-------------|--------|---------|
| **AcademicLead** | Academic Research | PaperSearcher |
| **GitHubLead** | GitHub Analysis | CodeExplorer |
| **CommunityLead** | Community Listening | DiscussionMonitor |

**TEA Protocol** (Tool-Environment-Agent):
1. **Task Decomposition**: Break domain task into worker tasks
2. **Worker Assignment**: Assign tasks to available workers
3. **Result Aggregation**: Combine worker results

---

### Layer 3: Worker Agents (Execution) / 工作代理（执行层）

**Specialized Executors**:

| Worker | Capability | Tools |
|--------|-----------|-------|
| **PaperSearcher** | PAPER_SEARCH | mcp__arxiv-mcp-server__search_papers |
| **CodeExplorer** | CODE_EXPLORATION | mcp__zread__get_repo_structure, mcp__zread__read_file |
| **DiscussionMonitor** | DISCUSSION_MONITORING | mcp__web-reader__webReader, mcp__web-search-prime__webSearchPrime |

---

## Agent Capabilities / 代理能力

```python
class AgentCapability(Enum):
    ACADEMIC_RESEARCH = "academic_research"
    GITHUB_ANALYSIS = "github_analysis"
    COMMUNITY_LISTENING = "community_listening"
    PAPER_SEARCH = "paper_search"
    CODE_EXPLORATION = "code_exploration"
    DISCUSSION_MONITORING = "discussion_monitoring"
    SYNTHESIS = "synthesis"
    QUALITY_ASSESSMENT = "quality_assessment"
```

---

## Task Flow / 任务流

```
User Query
    ↓
Meta-Orchestrator
    ├─ Analyze Query (complexity, parallelizability)
    ├─ Determine Strategy (single vs multi-agent)
    ├─ Create Domain Tasks
    └─ Assign to Coordinators
        ↓
Domain Coordinators (Parallel)
    ├─ AcademicLead ──→ PaperSearcher
    ├─ GitHubLead ────→ CodeExplorer
    └─ CommunityLead ─→ DiscussionMonitor
        ↓
Result Aggregation & Synthesis
```

---

## Performance-Aware Decision Framework / 性能感知决策框架

**Multi-Agent Benefits**:
- **Performance**: +90.2% improvement on complex queries
- **Cost**: 15x token multiplier
- **Speed**: +80.9% for parallel tasks

**When to Use Hierarchical**:
- Single-agent success rate < 45%
- 2+ parallelizable aspects
- Information exceeds single context window
- Task value justifies cost increase

**When NOT to Use**:
- Sequential dependencies
- Single-agent success > 45%
- Cost-sensitive applications
- Sub-second latency required

---

## CLI Usage / 命令行使用

```bash
# Execute research query
python "tools\hierarchical_orchestrator.py" --query "深度研究 multi-agent frameworks"

# Show hierarchy status
python "tools\hierarchical_orchestrator.py" --status
```

---

## Orchestration Patterns / 编排模式

### Centralized / 中央编排
- Single orchestrator coordinates all workers
- Examples: Anthropic LeadResearcher, MetaGPT
- Pros: Clear control flow
- Cons: Single point of failure

### Hierarchical / 分层架构
- Multi-level organization with team-level abstraction
- Examples: AutoGen hierarchical, Cross-Team Orchestration
- Pros: Scalable to large numbers
- Cons: More complex design

---

## Coordination Overhead / 协调开销

**Scaling Formula**:
```
Potential interactions = n(n-1)/2 where n = number of agents

2 agents: 1 interaction
4 agents: 6 interactions
10 agents: 45 interactions
```

**Solution**: Hierarchical structure reduces coordination overhead from flat structure.

---

## Related Modules / 相关模块

- **memory_system.py**: MAGMAMemory for shared state
- **research_orchestrator.py**: Main research orchestrator
- **orchestration_patterns.md**: General orchestration patterns

---

## Research Integration / 研究集成

**Academic Research**:
1. PaperSearcher finds root papers
2. PaperSearcher finds survey papers
3. AcademicLead aggregates results

**GitHub Analysis**:
1. CodeExplorer explores repository structure
2. CodeExplorer analyzes implementation
3. GitHubLead synthesizes architecture

**Community Listening**:
1. DiscussionMonitor monitors Reddit/HN
2. DiscussionMonitor extracts consensus
3. CommunityLead aggregates discussions
