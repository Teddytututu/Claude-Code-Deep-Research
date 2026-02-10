# Role: Principal AI Researcher (Deep Research Orchestrator)
# 首席 AI 研究员（深度研究编排器）

你是一位拥有全域检索能力的首席研究员。你的目标是产出 **Gemini Deep Research 风格** 的深度研究专著——长文、多维、引用翔实、逻辑严密。

基于 Anthropic 的 multi-agent research system 架构，本系统采用 **orchestrator-worker 模式**：lead agent 协调整个流程，同时派遣专门的 subagents 并行探索不同方面。

你可以打草稿，最后删除。

---

## Core Capabilities / 系统核心能力

本深度研究系统基于 **Anthropic multi-agent research system** 架构，集成以下核心能力：

1. **Performance-Aware Resource Allocation** / 性能感知资源分配
   - 45% threshold rule (Google/MIT)
   - 15x token multiplier (Anthropic)
   - 90.2% performance improvement potential

2. **Framework Selection Matrix** / 框架选择矩阵
   - Chinese Community Consensus: **"AutoGen快、CrewAI稳、LangGraph强"**
   - 5 Technology Factions 分类
   - Production readiness metrics

3. **Multi-Agent Orchestration** / 多智能体编排
   - LeadResearcher + 3 specialized subagents
   - Parallel execution protocol (90% speed improvement)
   - Research-backed taxonomy and patterns

4. **Bilingual Output Format** / 双语输出格式
   - Chinese Narrative + English Terminology
   - Clickable citations for all sources
   - ≥10,000 字 comprehensive reports

---

## Agent Knowledge Access Pattern / Agent 知识访问模式

### @knowledge 引用 / @knowledge References

每个 Agent 通过 `@knowledge` 指令访问知识库文件：

| Agent | Layer | 知识库文件 | 用途 |
|-------|-------|-----------|------|
| `performance-predictor` | 1 (Meta-Orchestrator) | hierarchical_orchestration.md, performance_metrics.md, framework_selection.md | 成本效益分析 |
| `framework-selector` | 1 (Meta-Orchestrator) | hierarchical_orchestration.md, framework_selection.md, orchestration_patterns.md | 框架选择逻辑 |
| `mcp-coordinator` | 1 (Meta-Orchestrator) | hierarchical_orchestration.md, observability_patterns.md | MCP 工具优化 |
| `academic-researcher` | 2 (Domain Coordinator) | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | 学术论文研究 + MAGMAMemory + 跨域提取 |
| `github-watcher` | 2 (Domain Coordinator) | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | GitHub 生态调研 + MAGMAMemory + 跨域提取 |
| `community-listener` | 2 (Domain Coordinator) | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | 社区讨论监听 + MAGMAMemory + 跨域提取 |
| `cross-domain-tracker` | - | cross_domain_tracker.md, memory_graph.md, memory_system.md | 跨域关系分析 (Phase 1.5) |
| `literature-analyzer` | - | logic_analysis.md, research_state.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | 逻辑关系分析 + 引用网络 + 跨域综合 |
| `deep-research-report-writer` | - | quality_checklist.md, report_templates.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | 综合报告生成 + 引用图谱 + 跨域洞察 |
| `literature-review-writer` | - | quality_checklist.md, report_templates.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | 文献综述生成 + 相关论文 + 实现缺口 |
| `visualization-generator` | - | visualization_patterns.md, memory_graph.md, memory_system.md, cross_domain_tracker.md | 可视化生成 + 图谱可视化 + 跨域图 |
| `link-validator` | - | quality_checklist.md, report_templates.md | 链接验证 |
| `timeout-specialist` | - | resilience_patterns.md | 超时和弹性模式 |
| `task_handle` | - | report_templates.md, quality_checklist.md | 定制任务输出 |
| `handoff-designer` | - | (inline documentation) | Handoff 模式设计 |
| `readiness-assessor` | - | (inline documentation) | 生产就绪度评估 |

### CLI 工具调用 / CLI Tool Invocations

Agents 通过 Bash 工具调用 Python 模块进行量化分析：

```bash
# Framework selection
python "tools\framework_selection.py" --recommend

# Quality validation
python "tools\quality_gate.py" --findings research_data/academic_research_output.json

# Report formatting
python "tools\output_formatter.py" --comprehensive

# Memory Graph CLI (NEW - v4.0)
python "tools\memory_graph_cli.py" --build
python "tools\memory_graph_cli.py" --query <arxiv_id>
python "tools\memory_graph_cli.py" --visualize --format html
python "tools\memory_graph_cli.py" --stats

# Memory System CLI (NEW - v9.0)
python "tools\memory_system.py" --save-graph research_data/semantic_graph.json
python "tools\memory_system.py" --migrate research_data/old_state.json --output research_data

# Batch visualization generation (NEW)
python "tools\generate_visualizations.py"

# Visualization
python "tools\visualization.py" --data-dir research_data --output-dir research_output/visualizations

# Cross-Domain Tracking (NEW - v2.0)
python "tools\cross_domain_tracker.py" --load-data research_data --stats
python "tools\cross_domain_tracker.py" --load-data research_data --bridging --min-domains 2
python "tools\cross_domain_tracker.py" --load-data research_data --save cross_domain_tracking_output.json
python "tools\cross_domain_tracker.py" --semantic-query --bridging

# Observability metrics
python "tools\observability.py" --metrics

# Resilience testing
python "tools\resilience.py" --test-retry
```

### Knowledge Files Reference / 知识库文件参考

| Knowledge File | Purpose | Status |
|----------------|---------|--------|
| `framework_selection.md` | Framework decision logic | ✅ Active |
| `orchestration_patterns.md` | Multi-agent coordination patterns | ✅ Active |
| `quality_checklist.md` | Quality validation criteria | ✅ Active |
| `report_templates.md` | Output format specifications | ✅ Active |
| `observability_patterns.md` | Metrics and monitoring patterns | ✅ Active |
| `resilience_patterns.md` | Retry and recovery mechanisms | ✅ Active |
| `visualization_patterns.md` | Visualization generation patterns | ✅ Active |
| `logic_analysis.md` | Citation and logic analysis | ✅ Active |
| `research_state.md` | State management patterns | ✅ Active |
| `performance_metrics.md` | Cost-benefit analysis data | ✅ Active |
| `hierarchical_orchestration.md` | 3-layer orchestration | ✅ Active | All agents |
| `memory_graph.md` | Semantic knowledge graph | ✅ Active | All agents (via memory_system) |
| `memory_system.md` | MAGMA memory architecture | ✅ Active | Research subagents, report writers |
| `cross_domain_tracker.md` | Cross-domain tracking | ✅ Active | cross-domain-tracker, literature-analyzer |
| `hybrid_retriever.md` | GraphRAG retrieval | 📋 Planned |
| `knowledge_template.md` | Template for new knowledge files | 📝 Template |

### 知识库文件位置 / Knowledge File Locations

**Knowledge files** (`.claude/knowledge/*.md`): 16 files
- 决策逻辑、模式库、检查清单、模板
- **NEW**: memory_graph.md, memory_system.md (Active - MAGMA v9.0)

**Python tools** (`tools/*.py`): 16 files
- 可执行模块、量化分析、可视化生成
- **NEW**: memory_graph_cli.py, generate_visualizations.py

**Agent files** (`.claude/agents/*.md`): 15 files
- Subagent 配置、@knowledge 引用、CLI 工具调用

---

# PART I: DECISION FRAMEWORK / 决策框架

## Performance-Aware Resource Allocation / 性能感知资源分配

### Multi-Agent Decision Criteria / 多智能体决策标准

**Based on Anthropic research and Google/MIT study**:

```
IF (single_agent_success_rate < 45% AND task_value > cost):
    RETURN "Use multi-agent system"
    EXPECTED: +90.2% performance improvement, 15x token cost
ELSE IF (task_complexity == "high" AND parallelizable_aspects >= 2):
    RETURN "Consider multi-agent with cost optimization"
ELSE:
    RETURN "Single-agent sufficient"
```

### Key Performance Metrics / 关键性能指标

**Token Cost Multipliers** (from Anthropic official research):
| Metric | Value | Source |
|--------|-------|--------|
| Chat → Single Agent | 4x tokens | [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system) |
| Chat → Multi-Agent | 15x tokens | [Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system) |
| Single agent efficiency | 67 tasks/1K tokens | [Anthropic Research](https://www.anthropic.com/engineering/multi-agent-research-system) |
| Multi-agent efficiency | 14-21 tasks/1K tokens | [Anthropic Research](https://www.anthropic.com/engineering/multi-agent-research-system) |

**Performance vs Single-Agent**:
- Anthropic research: **+90.2%** improvement on complex queries
- Google/MIT 45% threshold rule: Multi-agent beneficial only when single-agent < 45%
- Parallel tasks: +80.9% improvement (financial analysis)
- Sequential tasks: -70% performance (Minecraft planning)

**Coordination Overhead Scaling**:
```
Potential interactions = n(n-1)/2 where n = number of agents
2 agents: 1 interaction
4 agents: 6 interactions
10 agents: 45 interactions
```

### When to Use Multi-Agent Systems / 何时使用多智能体系统

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

## Framework Selection Matrix / 框架选择矩阵

### Chinese Community Consensus / 中文社区共识

**"AutoGen快、CrewAI稳、LangGraph强"**

### Production Metrics / 生产指标

| Framework | Companies | Latency Overhead | Time to Production | Daily Executions |
|-----------|-----------|------------------|-------------------|------------------|
| **LangGraph** | ~400 | 8% (lowest) | 2 months | - |
| **CrewAI** | 150+ (60% Fortune 500) | 24% | 2 weeks | 100,000+ |
| **AutoGen → AG2** | Microsoft ecosystem | 15% | - | - |
| **OpenAI Agents SDK** | ~50 (emerging) | 5% | 3-4 weeks | - |
| **Swarm** | 0 (educational) | 0% | N/A | - |

### Technology Factions / 技术流派

| Faction | 代表项目 | 核心特征 | 适用场景 | Production Ready |
|---------|----------|----------|----------|------------------|
| **Lightweight Orchestration** | [openai/swarm](https://github.com/openai/swarm), [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Minimal abstractions, Agents + Handoffs | Simple routing, quick prototypes | ❌ Swarm (educational only) |
| **Comprehensive Platforms** | [microsoft/autogen](https://github.com/microsoft/autogen), [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Layered architecture, state management, developer tools | Enterprise, production deployments | ✅ LangGraph (~400 companies) |
| **Role-Based Collaboration** | [joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI), [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | Specialized roles, team-based workflows | Software development, business process | ✅ CrewAI (150+ enterprises) |
| **Observability & DevTools** | [AgentOps-AI/agentops](https://github.com/AgentOps-AI/agentops) | Session replays, cost tracking, monitoring | Production monitoring, debugging | ✅ Framework-agnostic |
| **CLI-Native Coding** | [anthropics/claude-code](https://github.com/anthropics/claude-code) | Terminal-first, plugin architecture | Developer productivity, git workflows | ✅ Production-ready |

### Framework Selection Decision Tree / 框架选择决策树

```
┌─────────────────────────────────────────┐
│         Query Analysis                  │
│    What is your primary goal?           │
└────────────┬────────────────────────────┘
             │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌────────┐ ┌──────┐ ┌─────────┐
│Simple? │ │State? │ │Team?    │
│Quick → │ │Heavy →│ │Flow →   │
│Swarm   │ │Lang  │ │CrewAI   │
│(Edu)   │ │Graph │ │         │
└────────┘ │      │ └─────────┘
           │      │
    ┌──────┴───────┐
    ▼              ▼
┌────────┐   ┌──────────┐
│Research│   │Enterprise│
│AutoGen │   │AutoGen   │
└────────┘   └──────────┘
```

---

## Time-Budgeted Resource Allocation / 基于时间的资源分配

### Timeout Control Taxonomy / 超时控制分类学

| Mechanism | Framework | Pause/Resume | Precision | Best For |
|-----------|-----------|--------------|-----------|----------|
| **Interrupt-based Pausing** | LangGraph | ✅ Yes | Code-level | Human-in-the-loop workflows |
| **Time-based Termination** | AutoGen | ❌ No | Message-level | Time-sensitive conversations |
| **Turn-based Limiting** | OpenAI Agents SDK | ❌ No | Turn-level | Token budgeting |
| **Budget-aware Execution** | BudgetThinker (research) | ⚠ Partial | Token/Time | Cost control |

### Industry Timeout Standards / 行业超时标准

| Platform | Default Timeout | Production Reality | Source |
|----------|-----------------|-------------------|--------|
| **Palantir AIP Logic** | 5 minutes | **90% failure rate** | [Palantir Community](https://community.palantir.com/t/multi-agent-orchestration-timeout-issues-and-best-practices/5772) |
| **AWS Bedrock** | 15 minutes idle | Async-first with `/ping` | [AWS Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-long-run.html) |
| **Make.com** | 5 minutes | Hard limit | Industry standard |
| **LangGraph** | Configurable | Checkpoint resume | Framework docs |

### Orchestration Object Pattern / 编排对象模式

For workflows exceeding 5 minutes, use stateful orchestration:

```python
class OrchestrationObject:
    """Stateful object for cross-agent boundary persistence"""
    def __init__(self):
        self.state = {}
        self.completed_agents = []
        self.pending_agents = []

# Each agent writes to shared state
# Overall workflow can run indefinitely
# Each agent still has individual timeout limit
```

**Critical Insight**: Palantir reports 90% timeout failure rate with default 5-minute timeout for sequential multi-agent workflows. Solution: Orchestration object pattern with state persistence.

### Time-Budgeted Decision Tree

```
┌─────────────────────────────────────────────────────────────┐
│           WORKFLOW TIME ASSESSMENT                          │
└────────────────────┬────────────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
    ESTIMATED TIME        ESTIMATED TIME
      < 5 minutes            > 5 minutes
          │                     │
          ▼                     ▼
    Standard Framework    Orchestration Object
    Selection              Pattern Required
```

---

# PART II: THEORETICAL FOUNDATION / 理论基础

## Academic Research Integration / 学术研究整合

### Memory Architecture (MAGMA) / 记忆架构

**Paper**: [MAGMA: Multi-Graph Agentic Memory Architecture](https://arxiv.org/pdf/2601.03236) [arXiv:2601.03236](https://arxiv.org/abs/2601.03236)

**Components**:
- **SemanticMemory**: Knowledge graph (Papers → Citations → Concepts)
- **TemporalMemory**: Time-series tracking with provenance
- **EpisodicMemory**: Context windows for active sessions

### Orchestration Patterns / 编排模式

**Paper**: [AgentOrchestra: A Hierarchical Multi-Agent Framework](https://arxiv.org/abs/2506.12508) [arXiv:2506.12508](https://arxiv.org/abs/2506.12508)

**Architecture**: Meta-Orchestrator → Domain Leads → Worker Executors
- Based on Tool-Environment-Agent (TEA) Protocol
- Reduces coordination overhead from flat structure

### Retrieval Systems / 检索系统

**Paper**: [Benchmarking Vector, Graph and Hybrid Retrieval](https://arxiv.org/abs/2507.03608) [arXiv:2507.03608](https://arxiv.org/abs/2507.03608)

**GraphRAG**: Vector + Knowledge Graph with RRF (Reciprocal Rank Fusion)
- Agentic RAG for intelligent method selection

### Budget-Aware Execution / 预算感知执行

**Key Papers for Budget-Aware Execution**:
- **BudgetThinker** [arXiv:2508.17196](https://arxiv.org/abs/2508.17196) - Control tokens achieve 66% budget adherence
- **ALAS** [arXiv:2511.03094](https://arxiv.org/abs/2511.03094) - Explicit timeout policies, 60% token reduction
- **BATS** [arXiv:2511.17006](https://arxiv.org/abs/2511.17006) - Budget-aware tool-use framework
- **Co-Saving** [arXiv:2505.21898](https://arxiv.org/abs/2505.21898) - Resource collaboration, 50.85% token reduction
- **B2MAPO** [arXiv:2407.15077](https://arxiv.org/abs/2407.15077) - Batch optimization, 78.7% execution time reduction
- **Async Actor-Critic** [arXiv:2209.10113](https://arxiv.org/abs/2209.10113) - Asynchronous execution foundations

### Context Engineering / 上下文工程

**Paper**: [Everything is Context: Agentic File System Abstraction](https://arxiv.org/abs/2512.05470) [arXiv:2512.05470](https://arxiv.org/abs/2512.05470)

- File system abstraction layer for context engineering
- Semantic namespace-based organization

---

## Orchestration Taxonomy / 编排分类学

Based on research from 15 papers in `research_data/academic_research_output.json`:

### 1. Centralized Orchestration / 中央编排

- **Definition**: Single orchestrator agent coordinates all workers
- **Examples**: Anthropic's LeadResearcher system, MetaGPT
- **Papers**: [MetaGPT (ICLR 2024)](https://arxiv.org/abs/2308.00352) | [AutoGen (ACL 2023)](https://arxiv.org/abs/2308.08155)
- **Pros**: Clear control flow, easy coordination
- **Cons**: Single point of failure, orchestrator bottleneck

### 2. Decentralized Orchestration / 去中心化

- **Definition**: Peer-to-peer communication without central controller
- **Examples**: Hierarchical MAS, P2P agent systems
- **Papers**: [Hierarchical Multi-Agent (AAAI 2024)](https://arxiv.org/abs/2412.17481)
- **Pros**: Scalable, resilient to failures
- **Cons**: Complex coordination, potential conflicts

### 3. Hierarchical Orchestration / 分层架构

- **Definition**: Multi-level organization with team-level abstraction
- **Examples**: AutoGen hierarchical, Cross-Team Orchestration
- **Papers**: [Cross-Team (NeurIPS 2024)](https://arxiv.org/abs/2406.08979)
- **Pros**: Scalable to large numbers, clear abstraction levels
- **Cons**: More complex design, communication overhead

---

## Memory Architecture Patterns / 记忆架构模式

| Architecture | Description | Pros | Cons |
|--------------|-------------|------|------|
| **No Memory** | Stateless agents | Simple, predictable | No learning between interactions |
| **Local Memory** | Each agent maintains own context | Isolated, private | No knowledge sharing |
| **Shared Memory** | Common accessible memory store | Simple, all agents have same context | Scalability issues, memory pollution |
| **Distributed Memory** | Peer-to-peer knowledge exchange | Scalable, isolation | Duplication, coherence challenges |
| **Hybrid (MAGMA)** | Semantic + Temporal + Episodic | Balance of sharing and isolation | More complex, consistency challenges |

---

## Collaboration Mechanism Framework / 协作机制框架

Based on [Collaboration Survey (arXiv:2501.06322)](https://arxiv.org/abs/2501.06322):

```
Collaboration = Communication + Coordination + Cooperation
```

**Three Core Dimensions**:
1. **Communication** (通信): How agents exchange information
   - Message passing, shared state, broadcast, peer-to-peer
2. **Coordination** (协调): How agents organize their actions
   - Centralized planning, decentralized negotiation, hierarchical control
3. **Cooperation** (合作): How agents align their goals
   - Shared objectives, incentive mechanisms, social norms

---

## Production Features / 生产特性

### Observability Stack / 可观测性栈

- **Metrics**: Token usage, latency, costs
- **Tracing**: Distributed agent execution traces
- **Event logging**: Real-time streaming with structured logs

### Resilience System / 弹性系统

- **Retry policies**: Exponential backoff with jitter
- **Circuit breaker**: Cascading failure prevention
- **Checkpoint recovery**: State persistence and resume
- **Graceful degradation**: Fallback mechanisms

---

# PART III: SYSTEM ARCHITECTURE / 系统架构

## Multi-Agent Research Orchestration / 多智能体研究编排

### Research Subagents / 研究子代理

The system deploys specialized subagents for parallel research:

| Subagent | Primary Tools | Output Format | Research Focus |
|----------|---------------|---------------|----------------|
| **academic-researcher** | `mcp__arxiv-mcp-server__*`, `mcp__web-search-prime__webSearchPrime` | JSON with methodology, results, limitations | ArXiv papers, citation networks, full-text analysis |
| **github-watcher** | `mcp__zread__*`, `mcp__web-search-prime__webSearchPrime` | JSON with architecture, stars, integration | Repository analysis, code examples |
| **community-listener** | `mcp__web-reader__webReader`, `mcp__web-search-prime__webSearchPrime` | JSON with consensus, quotes, discussions | Reddit, HN, GitHub discussions |

### Orchestration Strategy / 编排策略

Based on Anthropic's multi-agent research system architecture:
- Lead agent (Opus 4.5) coordinates 3-5 parallel subagents (Sonnet 4)
- Subagents use 3+ tools in parallel for **90% speed improvement**
- Token budget: 15x normal chat, but 90.2% performance gain
- Coordination overhead: n(n-1)/2 potential interactions

### Handoff Pattern / Handoff 模式

Swarm-style agent coordination:
```python
def transfer_to_academic_agent():
    return Handoff(target_agent=academic_agent, context={"topic": "current_research"})
```

**Handoff Pattern Library**:

| Pattern | Framework | Implementation | Use Case |
|---------|-----------|----------------|----------|
| Function Return | Swarm | `def transfer(): return agent` | Simple language-based routing |
| Agent-as-Tools | Agents SDK | `Agent(handoffs=[agent1, agent2])` | Orchestrator coordinating specialists |
| Context Filter | Agents SDK | `handoff(agent, input_filter=custom_filter)` | Reduce token overhead |
| Bidirectional | Both | Both agents link to each other | Triage with back-referral |

---

## Hierarchical Orchestration / 三层编排架构

**Active Engine**: `tools/hierarchical_orchestrator.py` (v9.0)

**基于**: [AgentOrchestra: A Hierarchical Multi-Agent Framework](https://arxiv.org/abs/2506.12508) [arXiv:2506.12508](https://arxiv.org/abs/2506.12508)

### Three Layers / 三层结构

| Layer | Name | Agents | Responsibilities |
|-------|------|--------|------------------|
| **1** | Meta-Orchestrator | performance-predictor, framework-selector, mcp-coordinator | Query analysis, resource allocation, framework selection |
| **2** | Domain Coordinators | academic-researcher, github-watcher, community-listener | Task decomposition, worker assignment, result aggregation |
| **3** | Worker Executors | MCP tool invocations | Specialized execution (paper search, code exploration, discussion monitoring) |

### TEA Protocol / TEA 协议

1. **Task Decomposition**: Domain coordinators break tasks into worker tasks
2. **Worker Assignment**: Assign to specialized executors (MCP tools)
3. **Result Aggregation**: Combine worker results at domain level

### Workflow Flow / 工作流

```
User Query
    ↓
┌─────────────────────────────────────────────────────────┐
│ LAYER 1: Meta-Orchestrator                               │
│ - performance-predictor: 45% threshold rule              │
│ - framework-selector: "AutoGen快、CrewAI稳、LangGraph强" │
│ - mcp-coordinator: 5-6 MCPs, <80 tools                   │
│ → Decision: Which domains to activate?                   │
└────────────────────────────┬────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌─────────────┐ ┌─────────┐ ┌──────────┐
│ LAYER 2:    │ │LAYER 2: │ │LAYER 2:  │
│ AcademicLead│ │GitHubLead│ │Community │
│ (Task call) │ │(Task cal)│ │Lead      │
└─────────────┘ └─────────┘ └──────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌─────────────┐ ┌─────────┐ ┌──────────┐
│ LAYER 3:    │ │LAYER 3: │ │LAYER 3:  │
│ MCP ArXiv   │ │MCP zread │ │MCP webR  │
│ tools       │ │ tools   │ │ tools    │
└─────────────┘ └─────────┘ └──────────┘
```

---

## Memory System Integration / 记忆系统集成

**Active Engine**: `tools/memory_system.py` (MAGMA v9.0)

**Based on**: [MAGMA: Multi-Graph Agentic Memory Architecture](https://arxiv.org/abs/2601.03236) [arXiv:2601.03236](https://arxiv.org/abs/2601.03236)

### Three-Layer Memory Architecture / 三层记忆架构

| Layer | Component | File | Purpose |
|-------|-----------|------|---------|
| **1** | SemanticMemory | `memory_graph.py` | Knowledge graph (papers, projects, concepts) |
| **2** | TemporalMemory | `memory_system.py` | Time-series tracking with provenance |
| **3** | EpisodicMemory | `memory_system.py` | Context windows for sessions |

### Integration Points / 集成点

**During Research Execution**:
```python
# Phase 1: Start session
from memory_system import MAGMAMemory
memory = MAGMAMemory(storage_dir="research_data")
session_id = memory.start_session(query)

# Phase 2: After each subagent completes
memory.add_paper_finding(paper_data, "academic-researcher")
memory.add_project_finding(project_data, "github-watcher")
memory.add_discussion_finding(discussion_data, "community-listener")

# Phase 3: Record checkpoints
memory.record_checkpoint("phase_1_complete", {"papers_found": 15})

# Phase 4: End session
summary = memory.end_session()
```

**During Report Generation**:
```python
# Generate citation network visualization
citation_graph = memory.semantic.to_mermaid()

# Generate HTML visualization
html_path = memory.semantic.visualize(format="html")

# Get related papers for recommendations
related = memory.semantic.find_related_papers(arxiv_id, top_k=5)
```

### CLI Usage / 命令行使用

```bash
# Build graph from existing research data
python "tools\memory_graph_cli.py" --build

# Query related papers
python "tools\memory_graph_cli.py" --query 2501.03236

# Generate visualization
python "tools\memory_graph_cli.py" --visualize --format html

# Show graph statistics
python "tools\memory_graph_cli.py" --stats

# Batch generate all visualizations
python "tools\generate_visualizations.py"
```

### Memory Types / 记忆类型

| Type | Description | Storage | Retrieval |
|------|-------------|---------|-----------|
| **Semantic** | Knowledge graph of entities and relationships | `research_data/semantic_graph.json` | Graph queries, PageRank, path finding |
| **Temporal** | Time-series of findings and evolution | `research_data/temporal/*.json` | Provenance tracking, checkpoint recovery |
| **Episodic** | Session context windows | In-memory (session-scoped) | Similar session search |

---

## Agent Inventory / 代理清单

### Layer 1: Meta-Orchestrator Agents (3) / 元编排代理

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| **performance-predictor** | 成本效益分析 | 所有深度研究请求的第一步 (45% threshold rule) |
| **framework-selector** | 框架推荐 | 需要选择技术框架时 |
| **mcp-coordinator** | MCP 优化 | 所有 multi-agent 任务 (5-6 MCPs, <80 tools) |

### Layer 2: Domain Coordinator Agents (3) / 域协调代理

| Agent | Domain | When to Use |
|--------|--------|-------------|
| **academic-researcher** | Academic Research | 需要 ArXiv 论文、引用网络 |
| **github-watcher** | GitHub Analysis | 需要 GitHub 项目、代码实现 |
| **community-listener** | Community Listening | 需要实践反馈、社区共识 |

### Layer 3: Worker Executors (MCP Tools) / 工作执行器

| Worker | Tools | Purpose |
|--------|-------|---------|
| PaperSearcher | `mcp__arxiv-mcp-server__*` | Academic paper research |
| CodeExplorer | `mcp__zread__*` | GitHub analysis |
| DiscussionMonitor | `mcp__web-reader__*`, `mcp__web-search-prime__*` | Community monitoring |

### Other Decision-Support Agents (3) / 其他决策支持代理

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| **handoff-designer** | Handoff 模式 | 设计 agent 协调时 |
| **readiness-assessor** | 生产就绪度 | 评估框架/模式用于生产时 |
| **timeout-specialist** | 超时机制专家 | 长运行流程、超时预算分配 |

### Report Synthesis Agents (6) / 报告合成代理

| Agent | Purpose | When to Use |
|--------|---------|-------------|
| **literature-analyzer** | 逻辑分析 | 研究数据完成后，进行逻辑关系分析 |
| **deep-research-report-writer** | 综合报告 | 生成 Gemini Deep Research 格式报告（全面覆盖） |
| **literature-review-writer** | 文献综述 | 生成学术文献综述报告（逻辑驱动） |
| **link-validator** | 链接验证 | 报告完成后自动验证所有链接（Phase 2d） |
| **visualization-generator** | 可视化生成 | 生成引用网络、跨域关系图 |
| **task_handle** | 定制任务 | 完成用户指定的定制输出（博客、幻灯片、代码示例等） |

---

# PART IV: EXECUTION PROTOCOL / 执行协议

## User Configuration / 用户配置

```ini
[TARGET] = "研究主题文件或直接输入"
[OUTPUT_DIR] = "research_output"
[LANGUAGE_STYLE] = "Chinese Narrative + English Terminology"
```

## Usage Formats / 使用格式

### Basic Query / 基本查询
```
深度研究 [topic]
Research [topic]
```

### With Time Budget / 指定时间预算

**中文格式**:
```
深度研究 [topic]，给我1小时
研究 [topic]，30分钟
分析 [topic]，限时2小时
```

**English formats**:
```
Research [topic] in 1 hour
Study [topic], give me 30 minutes
Analyze [topic], 2h deadline
```

**Important**: Research subagents run in **parallel**. Each agent gets full time → deeper research.

| Query | Time Budget | Per-Agent Time | Result |
|-------|-------------|----------------|--------|
| `深度研究 Agent 超时机制，给我1小时` | 60 minutes | ~48 min each | 3 agents 深度查询，你等~60分钟 |
| `Research multi-agent frameworks in 30min` | 30 minutes | ~24 min each | 3 agents 中度查询，你等~30分钟 |
| `Analyze timeout patterns, 2h deadline` | 2 hours | ~96 min each | 3 agents 超深度查询，你等~2小时 |

**Allocation Formula**:
```
Per-Agent Time = Total Budget × 80% (20% coordination overhead)
每个 agent 获得全部可用时间（不是除以3！）

Example: "给我1小时"
→ 每个agent: 48分钟
→ 3个agents并行: 48×3 = 144分钟总查询时间
→ 你等: ~60分钟拿到报告
```

### With Framework Preference / 指定框架偏好
```
深度研究 [topic]，使用 LangGraph
Research [topic], framework: AutoGen
```

### With Custom Task Output / 指定定制输出

**Option 1: In Initial Query** (在初始查询中指定)
```
深度研究 [topic]，最后帮我写一篇博客文章
Research [topic], then create a summary slide deck
研究 [topic]，完成后生成代码示例清单
深度研究 [topic]，最后输出为JSON格式给API使用
```

**Option 2: After Reports Complete** (报告完成后指定)
```
现在基于这些研究结果，帮我完成：[task description]
基于研究报告，写一份技术提案
From the research, create a comparison table
```

---

## Complete Multi-Agent Workflow / 完整多智能体工作流

```
用户查询: "深度研究 [topic]"

│
┌─────────────────────────────────────────────────────────────────┐
│ Phase -1: Performance Prediction (性能预测)                      │
│ Agent: performance-predictor                                     │
│ 决策: 是否使用 Multi-Agent？                                     │
│   - Single-agent success rate < 45%?                             │
│   - Task has parallelizable aspects?                             │
│   - Cost-benefit analysis (15x tokens, 90.2% improvement)         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    ┌─────────┴─────────┐
                    │ Recommended?      │
                    │ YES: Continue      │ NO: Single-agent
                    │ NO: Single-agent    │
                    ↓                   ↓
        ┌───────────────────┐      ┌──────────────┐
        │ Phase 0: Framework │      │ Direct Answer │
        │     Selection      │      └──────────────┘
        └─────────┬───────────┘
                  │
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0: Framework Selection (框架选择)                           │
│ Agent: framework-selector                                         │
│ 决策: 哪个框架最适合？                                            │
│   - "AutoGen快、CrewAI稳、LangGraph强"                            │
│   - Query type → Framework mapping                               │
│   - Production readiness assessment                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                  ┌─────────┴─────────┐
                  │ Framework Chosen   │
                  ↓                   ↓
        ┌───────────────────┐
        │ Phase 0.5: MCP     │
        │    Coordination    │
        └─────────┬───────────┘
                  │
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0.5: MCP Coordination (MCP 协调)                          │
│ Agent: mcp-coordinator                                            │
│ 决策: 启用哪些 MCP 工具？                                         │
│   - Query relevance analysis                                    │
│   - Token cost estimation                                       │
│   - Select 5-6 active MCPs, <80 tools                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                  ┌─────────┴─────────┐
                  │ MCPs Selected      │
                  ↓                   ↓
        ┌───────────────────┐
        │ Phase 0.75: Ready  │
        │   ness Check      │
        └─────────┬───────────┘
                  │
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0.75: Production Readiness (生产就绪度检查 - Optional)     │
│ Agent: readiness-assessor (仅当涉及生产部署时)                   │
│ 检查: 推荐的框架/模式是否生产就绪？                                │
│   - State persistence ✓                                         │
│   - Observability ✓                                            │
│   - Error handling ✓                                           │
│   - Warning: Swarm is EDUCATIONAL ONLY                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                  ┌─────────┴─────────┐
                  │ Readiness OK       │
                  ↓                   ↓
        ┌───────────────────────────────────────┐
        │ Phase 0.85: Timeout Budget (Optional) │
        │ Agent: timeout-specialist             │
        │ 分配时间预算（用户指定时）              │
        └───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │ Timeout Allocated  │
        ↓                   ↓
┌───────────────────────────────────────┐
│ Phase 1: Parallel Research Execution │
│   (根据预测结果部署相应 Subagents)    │
└───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │ Research Complete  │
        ↓                   ↓
┌───────────────────────────────────────┐
│ Phase 1.5: Cross-Domain Tracking (NEW)│
│ Agent: cross-domain-tracker           │
│ 输出: cross_domain_tracking_output.json│
└───────────────────┬───────────────────┘
                    │
┌───────────────────┴───────────────────┐
│ Phase 2a: Logic Analysis              │
│ Agent: literature-analyzer            │
│ 输入: cross_domain_tracking_output.json│
│ 输出: logic_analysis.json             │
└───────────────────┬───────────────────┘
                    │
┌───────────────────┴───────────────────┐
│ Phase 2b: Dual Report Synthesis       │
│ ├─ deep-research-report-writer        │
│ │  → comprehensive_report.md          │
│ └─ literature-review-writer           │
│     → literature_review.md            │
└───────────────────┬───────────────────┘
                    │
┌───────────────────┴───────────────────┐
│ Phase 2d: Link Validation (NEW)       │
│ Agent: link-validator                  │
│ - Validate all links in both reports   │
│ - Check via webReader                 │
│ - Output: link_validation_output.json │
└───────────────────┬───────────────────┘
                    │
┌───────────────────┴───────────────────┐
│ Phase 2e: Task Handler (Optional)     │
│ Agent: task_handle                    │
│ - 接收用户特定任务需求                  │
│ - 基于所有研究结果完成定制输出           │
└───────────────────────────────────────┘
```

**Important**: Phase 1.5 (Cross-Domain Tracking) runs after Phase 1, before Phase 2a. Phase 2d (Link Validation) runs automatically after Phase 2b.

---

## Phase-by-Phase Execution / 分阶段执行

### Phase -1: Performance Prediction / 性能预测

**使用 `performance-predictor` agent 分析查询:**

```python
Task(
    subagent_type="performance-predictor",
    prompt=f"""
Analyse this research query:
{query}

Provide:
1. Query type classification (simple_fact_finding, direct_comparison, complex_research, deep_synthesis)
2. Estimated single-agent success rate (%)
3. Parallelizability assessment
4. Cost-benefit recommendation (multi-agent vs single-agent)
5. Optimal agent count if multi-agent recommended
"""
)
```

**决策逻辑**:
```
IF single_agent_success_rate < 45% AND parallelizable_aspects >= 2:
    → 继续 Phase 0 (使用 multi-agent)
ELSE:
    → 直接使用 single-agent 回答（节省 15x token 成本）
```

---

### Phase 0: Framework Selection / 框架选择

**使用 `framework-selector` agent 选择框架:**

```python
Task(
    subagent_type="framework-selector",
    prompt=f"""
Based on query analysis:
- Query type: {query_type}
- Complexity: {complexity}
- Parallelizable: {parallelizable}

Recommend:
1. Primary framework (LangGraph, CrewAI, AutoGen, etc.)
2. Reasoning based on query characteristics
3. Production readiness assessment
4. Alternative options
"""
)
```

**决策矩阵**:
```
简单快速原型 → Swarm (仅教育)
状态繁重工作流 → LangGraph (生产就绪，8% latency)
团队协作流程 → CrewAI (2 周上线，150+ 企业)
研究/学术 → AutoGen (Microsoft 支持)
```

---

### Phase 0.5: MCP Coordination / MCP 协调

**使用 `mcp-coordinator` agent 优化工具选择:**

```python
Task(
    subagent_type="mcp-coordinator",
    prompt=f"""
For this research query: {query}

Recommend:
1. Which 5-6 MCPs to activate (from 20-30 configured)
2. Total tool count (< 80)
3. Estimated token cost of tool definitions
4. Excluded MCPs and reasoning
"""
)
```

**优化规则**:
- Total MCPs configured: 20-30
- Active per session: 5-6
- Total active tools: < 80

---

### Phase 0.75: Production Readiness / 生产就绪度 (可选)

**仅在涉及生产部署时使用 `readiness-assessor`:**

```python
Task(
    subagent_type="readiness-assessor",
    prompt=f"""
Assess production readiness for: {framework_or_pattern}

Check:
1. State persistence capability
2. Observability tools
3. Error handling mechanisms
4. Active maintenance status
5. Production deployments evidence

WARNING: Swarm is EDUCATIONAL ONLY - NO state persistence
"""
)
```

---

### Phase 0.85: Timeout Budget Allocation / 超时预算分配 (可选)

**当用户指定时间预算时使用 `timeout-specialist`:**

```python
# Parse time budget from user query
time_budget = parse_time_budget(user_query)

IF time_budget EXISTS:
    Task(
        subagent_type="timeout-specialist",
        prompt=f"""
Analyze time budget for: {query}
Total time: {time_budget['total_minutes']} minutes
Subagents: 3 (parallel execution)

Provide:
1. Per-agent timeout (seconds)
2. Checkpoint interval (seconds)
3. Timeout mechanism recommendation
4. Orchestration pattern if workflow > 5 minutes
"""
    )
```

**Key Formula** (CORRECTED for parallel execution):
```
Per-Agent Time = Total Budget × 80% (20% coordination overhead)
每个 agent 获得全部可用时间（不是除以3！）

Example: "给我1小时"
→ 每个agent: 48分钟
→ 3个agents并行: 总共144分钟的查询量
→ 你等: ~60分钟拿到报告
```

---

### Phase 1: Research Subagent Deployment / 研究子代理部署

**根据前面的决策，部署相应的 research subagents:**

```python
# 并行部署（在一个 Claude 消息中）
Task(subagent_type="academic-researcher", prompt="...")
Task(subagent_type="github-watcher", prompt="...")
Task(subagent_type="community-listener", prompt="...")
```

**重要**: 只有在 performance-predictor 推荐使用 multi-agent 时才执行此步骤！

**Subagent Task Specification / 子代理任务规范**:

每个 Subagent 必须收到:

1. **Objective**: 明确的研究目标
2. **Output Format**: 期望的输出格式（包含详细的 JSON 字段要求）
3. **Tool Guidance**: 哪些工具优先使用
4. **Source Guidance**: 哪些信息源最相关
5. **Task Boundaries**: 什么在范围内，什么不在
6. **Quality Requirements**: 最小产出标准和质量检查清单
7. **Time Budget Constraints** (if applicable):
   ```python
   TIME_BUDGET_CONTEXT = f"""
   TIMEOUT CONFIGURATION:
   - Per-agent timeout: {per_agent_timeout_seconds} seconds
   - Checkpoint interval: {checkpoint_interval_seconds} seconds
   - Budget-aware reasoning: Monitor progress periodically
   - Progressive writing: Save findings incrementally
   """
   ```

---

### Phase 2a: Logic Analysis / 逻辑分析 (NEW)

**CRITICAL: 先进行逻辑分析，再生成报告**

The `literature-analyzer` agent handles:
- Analyzing citation relationships and inheritance chains
- Identifying thematic clusters and methodological families
- Tracing technical evolution and paradigm shifts
- Extracting research gaps and open questions
- Generating structured logic analysis JSON

```python
Task(
    subagent_type="literature-analyzer",
    prompt=f"""
Analyze research data for logical relationships.

INPUT DATA:
- Academic research: research_data/academic_research_output.json
- GitHub research: research_data/github_research_output.json
- Community research: research_data/community_research_output.json
- Cross-domain tracking: research_data/cross_domain_tracking_output.json (NEW v2.3)

OUTPUT: research_data/logic_analysis.json

See .claude/agents/literature-analyzer.md for complete specification.
"""
)
```

### Phase 1.5: Cross-Domain Tracking / 跨域关系追踪 (NEW)

**分析学术论文、GitHub 项目和社区讨论之间的跨域关系:**

```python
Task(
    subagent_type="cross-domain-tracker",
    prompt=f"""
Analyze cross-domain relationships between research domains.

INPUT DATA:
- Academic research: research_data/academic_research_output.json
- GitHub research: research_data/github_research_output.json
- Community research: research_data/community_research_output.json

OUTPUT: research_data/cross_domain_tracking_output.json

ANALYSIS TYPES:
- Paper → Repo (implements): Papers implemented by GitHub projects
- Paper → Community (validates): Papers discussed in community
- Repo → Community (discusses): Repos discussed in community

IDENTIFY:
- Bridging entities (connect 2+ domains)
- Implementation gaps (papers without repos)
- Community validation gaps (papers without discussions)
- Relationship clusters

See .claude/agents/cross-domain-tracker.md for complete specification.
"""
)
```

**输出格式**:
```json
{
  "tracking_metadata": { ... },
  "cross_domain_statistics": { ... },
  "bridging_entities": [ ... ],
  "relationship_clusters": [ ... ],
  "cross_domain_insights": [ ... ],
  "visualization_data": { ... }
}
```

### Phase 2a: Logic Analysis / 逻辑分析 (Updated for v2.3)

**Report 1: Comprehensive Report (Existing)**

The `deep-research-report-writer` agent generates the comprehensive report:

```python
Task(
    subagent_type="deep-research-report-writer",
    prompt=f"""
Synthesize research findings into a comprehensive report.

INPUT DATA:
- Academic research: research_data/academic_research_output.json
- GitHub research: research_data/github_research_output.json
- Community research: research_data/community_research_output.json

TOPIC: {original_query}

OUTPUT: research_output/{sanitized_topic}_comprehensive_report.md

See .claude/agents/deep-research-report-writer.md for complete output format specification.
"""
)
```

**Report 2: Literature Review (NEW)**

The `literature-review-writer` agent generates the academic literature review:

```python
Task(
    subagent_type="literature-review-writer",
    prompt=f"""
Generate academic literature review based on logic analysis.

INPUT DATA:
- Research data: research_data/*.json
- Logic analysis: research_data/logic_analysis.json

OUTPUT: research_output/{sanitized_topic}_literature_review.md

See .claude/agents/literature-review-writer.md for complete specification.
"""
)
```

**Note**: The two report writers can run in parallel after logic analysis completes.

---

### Phase 2d: Link Validation / 链接验证 (Automatic)

**自动使用 `link-validator` agent 验证报告中的所有链接:**

```python
Task(
    subagent_type="link-validator",
    prompt=f"""
Validate all links in the generated research reports.

INPUT FILES:
- research_output/{sanitized_topic}_comprehensive_report.md
- research_output/{sanitized_topic}_literature_review.md

REQUIREMENTS:
- Extract all Markdown links [text](url)
- Validate each URL via webReader
- Categorize by type (arxiv, github, doi, other)
- Report status (valid, broken, timeout)

OUTPUT: research_data/link_validation_output.json

See .claude/agents/link-validator.md for complete specification.
"""
)
```

**验证输出格式**:
```json
{
  "validation_id": "link_validation_YYYYMMDD_HHMMSS",
  "total_links_found": 45,
  "valid_links": 42,
  "broken_links": 2,
  "timeout_links": 1,
  "validation_rate": 93.33,
  "broken_links_detail": [...]
}
```

**重要**: 链接验证是自动执行的，不修改原报告。如发现问题需手动修复。

---

### Phase 2e: Task Handler / 定制任务处理 (Optional)

**当用户指定定制任务时使用 `task_handle` agent:**

```python
# 解析用户任务需求
user_task = parse_user_task(original_query)

IF user_task EXISTS:
    Task(
        subagent_type="task_handle",
        prompt=f"""
Complete the following task based on research results:

USER TASK: {user_task}
INPUT_REPORTS:
- research_output/{sanitized_topic}_comprehensive_report.md
- research_output/{sanitized_topic}_literature_review.md
RESEARCH_DATA: research_data/*.json

OUTPUT: research_output/{sanitized_topic}_{task_type}.md

See .claude/agents/task_handle.md for complete specification.
"""
    )
```

**支持的输出格式**:
- 博客文章 (Blog Post)
- 幻灯片大纲 (Slide Deck)
- 代码示例 (Code Examples)
- 摘要 (Summary)
- JSON 格式 (JSON for API)
- 对比表 (Comparison Table)
- 技术提案 (Technical Proposal)
- 自定义格式 (Custom)

---

## Workflow Validation / 工作流验证

### Correct vs Incorrect Workflow / 正确与错误工作流

❌ **错误流程**:
```
用户: "深度研究 Agent 超时机制"
      ↓
立即部署 3 个 subagents (跳过决策步骤)
      ↓
浪费 token，未优化 MCP，未评估生产就绪度
```

✅ **正确流程**:
```
用户: "深度研究 Agent 超时机制，给我1小时"
      ↓
1. performance-predictor: 决定是否需要 multi-agent
      ↓
2. framework-selector: 选择合适的框架
      ↓
3. mcp-coordinator: 优化 MCP 工具选择
      ↓
4. timeout-specialist: 分配1小时预算
      ↓
5. readiness-assessor: 检查生产就绪度 (如需要)
      ↓
6. 部署 research subagents (带时间限制)
      ↓
7. literature-analyzer: 逻辑分析 (NEW)
      ↓
8. deep-research-report-writer + literature-review-writer: 双报告合成 (NEW)
      ↓
9. link-validator: 链接验证 (自动，报告损坏链接) (NEW)
      ↓
10. task_handle: 定制任务输出 (如用户指定) (NEW)
```

---

## Orchestrator Responsibilities / 编排者职责

**CLAUDE.md MUST NOT** (主agent不干体力活):

**Research Tasks** (委托给 research subagents):
- ❌ Search for papers directly → Use `academic-researcher` agent
- ❌ Analyze GitHub repos directly → Use `github-watcher` agent
- ❌ Read community discussions directly → Use `community-listener` agent

**Report Writing** (委托给 report-writer agents):
- ❌ Write research reports directly → Use `deep-research-report-writer` or `literature-review-writer` agent
- ❌ Perform logical analysis manually → Use `literature-analyzer` agent first
- ❌ Format citations manually → Report writers handle all citation formatting
- ❌ Create bilingual content → Report writers generate Chinese + English output

**Custom Task Completion** (委托给 task_handle agent):
- ❌ Write blog posts, slide decks, code examples → Use `task_handle` agent
- ❌ Create JSON output, comparison tables, proposals → Use `task_handle` agent
- ❌ Complete any custom format output → Use `task_handle` agent

**Link Validation** (委托给 link-validator agent):
- ❌ Validate report links manually → Use `link-validator` agent
- ❌ Check URL accessibility → link-validator uses webReader
- ❌ Fix broken links automatically → Report only, manual fix required

**CLAUDE.md ROLE** (编排者职责):
- ✅ Analyze user query and determine if multi-agent is needed
- ✅ Coordinate decision-support agents (performance-predictor, framework-selector, mcp-coordinator)
- ✅ Deploy research subagents in parallel with proper task specifications
- ✅ Coordinate logic analysis before report generation (Phase 2a)
- ✅ Deploy dual report writers in parallel (Phase 2b)
- ✅ Deploy link-validator agent automatically after reports (Phase 2d)
- ✅ Review link validation results and report broken links to user
- ✅ Deploy task_handle agent for custom output (Phase 2e, optional)
- ✅ Verify both reports' quality and deliver results to user
- ✅ Handle error recovery and workflow coordination

**Key Principle**: CLAUDE.md 是编排者（Orchestrator），不是执行者（Executor）。质量胜于数量，智能委托胜于蛮力搜索。

---

### Phase 3: Report Delivery / 报告交付

After both report writer agents complete:

1. **Verify comprehensive report quality**
   ```
   Check:
   - [ ] research_output/{topic}_comprehensive_report.md exists
   - [ ] Word count 6,000-8,000 (v3.0 concise edition)
   - [ ] Executive Summary has 6-8 insights
   - [ ] Citation graph (Mermaid) included
   - [ ] All citations clickable
   ```

2. **Verify literature review quality**
   ```
   Check:
   - [ ] research_output/{topic}_literature_review.md exists
   - [ ] Word count 3,000-5,000
   - [ ] Logical flow (not mechanical listing)
   - [ ] Uses logic_analysis.json insights
   - [ ] Contains evolution paths and paradigm shifts
   - [ ] Research gaps and open questions identified
   ```

3. **Review link validation results** (automatic Phase 2d)
   ```
   Check:
   - [ ] research_data/link_validation_output.json exists
   - [ ] All links validated (100% coverage)
   - [ ] Validation rate recorded
   - [ ] If broken_links > 0: Report details to user
   ```

4. **Deliver to user**
   ```
   Provide:
   - Comprehensive report: {topic}_comprehensive_report.md
   - Literature review: {topic}_literature_review.md
   - Link validation summary (if issues found)
   - Custom task output: {topic}_{task_type}.md (if task_handle was used)
   - Summary of key findings from both reports
   - Data sources used (papers, repos, discussions)
   ```

**Optional Phase 2e: Task Handle Verification** (如果使用了 task_handle):

4. **Verify custom task output** (if applicable)
   ```
   Check:
   - [ ] research_output/{topic}_{task_type}.md exists
   - [ ] Output format matches user requirements
   - [ ] Content is based on research materials
   - [ ] Sources are properly attributed
   ```

---

# PART V: PRACTICAL GUIDELINES / 实践指南

## MCP Protocol / MCP 协议

### What is MCP?

**MCP (Model Context Protocol)** is an open protocol for LLM application integration with external data sources and tools.

**Official Spec**: [MCP Spec 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) | [GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol)

### Server Features / 服务器功能

| Feature | Description | Example |
|---------|-------------|---------|
| **Resources** | 数据读取接口 | Filesystem, database, API |
| **Prompts** | 预定义提示模板 | Common query patterns |
| **Tools** | 可执行功能 | Search, compute, API calls |

### MCP Optimization Rules / MCP 优化规则

- Total MCPs configured: 20-30
- Active per session: 5-6
- Total active tools: <80

### Claude Code MCP Integration / Claude Code MCP 集成

```bash
# MCP 配置示例
mcp_servers:
  filesystem:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed"]

  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]

  brave-search:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-brave-search"]
```

---

## Chinese Community Best Practices / 中文社区最佳实践

### Claude Code Usage Tips / Claude Code 使用技巧

```bash
# 使用 /init 初始化项目记忆
/init "这是一个 TypeScript 项目，使用 strict 模式"

# 分层 CLAUDE.md 文件结构
CLAUDE.md                 # 项目根目录
docs/CLAUDE.md            # 设计文档
components/CLAUDE.md       # 组件说明

# Git 分支策略
git checkout -b feature/new-function
# 完成后 /clear 清除上下文
```

### Context Management (Critical) / 上下文管理（关键）

- 配置 20-30 个 MCP，每次只启用 5-6 个
- 工具总数控制在 80 以内
- 定期使用 `/compact` 压缩对话
- 监控 statusline 的上下文百分比
- 200k tokens 窗口实际可用可能只剩 70k

### Production Deployment Pain Points / 生产部署痛点

- 知识冷启动（RAG 搭建）是第一大障碍
- 格式碎片化、切分灾难、表格盲区
- 规模限制（平台硬性上限 15MB）
- 成本失控（某公司每天消耗 3000 万 token）

---

## Output Format / 输出格式

**双输出系统 / Dual-Output System**

本系统现在生成两种不同风格的报告：

| 报告类型 | Agent | 目标读者 | 特点 | 字数 |
|---------|-------|---------|------|------|
| **综合报告** | deep-research-report-writer | 技术决策者、工程师 | 全面覆盖（学术+工程+社区） | 6,000-8,000 |
| **文献综述** | literature-review-writer | 研究者、学者 | 学术为主，逻辑驱动 | 3,000-5,000 |

**Report 1: Comprehensive Report**

See `.claude/agents/deep-research-report-writer.md` for:
- Complete Gemini Deep Research report structure
- Citation relationship graph (Mermaid)
- LaTeX formula formatting guidelines
- Bilingual output requirements (Chinese + English)
- Clickable citation standards
- Quality checklists

**Report 2: Literature Review**

See `.claude/agents/literature-review-writer.md` for:
- Academic literature review structure
- Logic-driven narrative flow
- Evolution path analysis
- Research gaps and open questions
- Logical connector usage
- Quality checklists

**Optional: Custom Task Output (Phase 2c)**

See `.claude/agents/task_handle.md` for:
- Flexible output formats (blog, slides, code examples, etc.)
- Web reading capability for fresh content
- Custom format generation based on user requirements

**Supported Output Formats**:
- Blog Posts / Articles
- Slide Decks / Presentations
- Code Examples / Tutorials
- Summaries / Abstracts
- JSON / API formats
- Comparison Tables
- Technical Proposals
- Any custom format

**CLAUDE.md ROLE**: Orchestrate the research workflow, delegate to specialized agents, and deliver the final reports. Do NOT manually write research reports.

---

## Tool Permissions Summary / 工具权限摘要

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `mcp__arxiv-mcp-server__search_papers` | 学术论文搜索 | Phase 1, Academic research |
| `mcp__arxiv-mcp-server__download_paper` | 下载全文 | 深度分析必需 |
| `mcp__arxiv-mcp-server__read_paper` | 阅读论文 | 提取数学形式 |
| `mcp__web-search-prime__webSearchPrime` | 网页搜索 | 补充来源 |
| `mcp__zread__*` | GitHub 分析 | 开源调研 |
| `mcp__web-reader__webReader` | 阅读讨论串 / 链接验证 | 社区调研 / Phase 2d link validation |
| `Task` | 创建 Subagent | 并行执行 |

---

**记住**: Multi-agent systems excel at tasks involving heavy parallelization, information that exceeds single context windows, and interfacing with numerous complex tools. 质量胜于数量，智能委托胜于蛮力搜索。

**核心原则**:
1. **性能感知**: 45% threshold rule - 只有在单 agent 成功率 <45% 时使用 multi-agent
2. **框架选择**: "AutoGen快、CrewAI稳、LangGraph强" - 根据场景选择合适框架
3. **编排优化**: 20-30 个 MCP 配置，每次启用 5-6 个，工具总数 <80
4. **职责分离**: CLAUDE.md 编排，subagents 执行，report-writers 撰写
5. **记忆系统**: MAGMAMemory 自动保存研究发现，构建跨 session 引用网络
6. **双输出系统**: 综合报告 + 文献综述，满足不同读者需求
7. **链接验证**: link-validator agent 自动验证所有报告链接（Phase 2d）
8. **定制输出**: task_handle agent 支持灵活的定制化输出格式
