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

**Link Validation** (委托给 link-validator agent):
- ❌ Validate report links manually → Use `link-validator` agent

**CLAUDE.md ROLE** (编排者职责):
- ✅ Analyze user query and determine if multi-agent is needed
- ✅ Coordinate decision-support agents (performance-predictor, framework-selector, mcp-coordinator)
- ✅ Deploy research subagents in parallel with proper task specifications
- ✅ **Wait for subagents to complete and check results**
- ✅ **If subagent incomplete due to time limit: relaunch with continuation instructions**
- ✅ Coordinate logic analysis before report generation
- ✅ Deploy dual report writers in parallel
- ✅ Deploy link-validator agent automatically after reports
- ✅ Review link validation results and report broken links to user
- ✅ Deploy task_handle agent for custom output (optional)
- ✅ Verify both reports' quality and deliver results to user
- ✅ Handle error recovery and workflow coordination

**CRITICAL: CLAUDE.md 是顺序编排器，不能并行工作**
- CLAUDE.md 本身是 **sequential orchestrator**（顺序编排器）
- 它 **launches subagents in parallel**（并行启动子智能体），但本身是 **sequential execution**
- CLAUDE.md 一次只能做一件事：调用一个 agent，等待结果，然后调用下一个
- **真正的并行**发生在 subagents 层面：academic-researcher、github-watcher、community-listener 同时运行

**Key Principle**: CLAUDE.md 是编排者（Orchestrator），不是执行者（Executor）。质量胜于数量，智能委托胜于蛮力搜索。

---

## Complete Multi-Agent Workflow / 完整多智能体工作流

```
用户查询: "深度研究 [topic]"

│
┌─────────────────────────────────────────────────────────────────┐
│ ⏱️  TIME BUDGET (INFORMATION ONLY - 无需确认)                    │
│                                                                  │
│  如果用户指定时间预算:                                            │
│  ├─ Total Budget: X 小时                                        │
│  ├─ Per-Agent Timeout: X × 80% 分钟 (NOT 除以 agent 数!)         │
│  └─ 你实际等待时间: ~X 小时 (agents 并行运行)                    │
│                                                                  │
│  如果用户未指定:                                                  │
│  └─ 基于 performance-predictor 估算默认值                          │
│                                                                  │
│  ⚠️ IMPORTANT: Re-allocation 自动基于 wall-clock，无需确认       │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│ Phase -1: Performance Prediction (性能预测)                      │
│ Agent: performance-predictor                                     │
│ 决策: 是否使用 Multi-Agent？ (45% threshold rule)                │
└────────────────────────────┬────────────────────────────────────┘
                             │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                             │
                    ┌─────────┴─────────┐
                    │ YES: Continue      │ NO: Single-agent
                    ↓                   ↓
        ┌───────────────────┐      ┌──────────────┐
        │ Phase 0: Framework │      │ Direct Answer │
        │     Selection      │      └──────────────┘
        └─────────┬───────────┘
                  │
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0: Framework Selection (框架选择)                           │
│ Agent: framework-selector                                         │
│ 决策: "AutoGen快、CrewAI稳、LangGraph强"                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                             │
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0.5: MCP Coordination (MCP 协调)                          │
│ Agent: mcp-coordinator                                            │
│ 决策: 启用 5-6 MCPs, <80 tools                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                             │
┌─────────────────────────────────────────────────────────────────┐
│ Phase 0.75: Production Readiness (Optional - 生产就绪度检查)     │
│ Agent: readiness-assessor (仅当涉及生产部署时)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                             │
┌───────────────────────────────────────┐
│ Phase 1: Parallel Research Execution │
│   Deploy 3 research subagents        │
│   (带 max_turns 限制)                │
└───────────────────┬───────────────────┘
                    │ ⏱️  CHECKPOINT [显示每个 agent 的 progress]
                    │
┌───────────────────┴───────────────────┐
│ Phase 1.1: Completion Check (NEW!)    │
│   检查 subagent 是否完成最小要求        │
│   如未完成: 从 checkpoint 继续执行     │
└───────────────────┬───────────────────┘
                    │ ⏱️  CHECKPOINT [显示: 是否需要 relaunch]
                    │
┌───────────────────┴───────────────────┐
│ Phase 1.5: Cross-Domain Tracking     │
│ Agent: cross-domain-tracker           │
└───────────────────┬───────────────────┘
                    │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                    │
┌───────────────────┴───────────────────┐
│ Phase 2a: Logic Analysis              │
│ Agent: literature-analyzer            │
└───────────────────┬───────────────────┘
                    │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                    │
┌───────────────────┴───────────────────┐
│ Phase 2b: Dual Report Synthesis       │
│ ├─ deep-research-report-writer        │
│ └─ literature-review-writer           │
└───────────────────┬───────────────────┘
                    │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                    │
┌───────────────────┴───────────────────┐
│ Phase 2d: Link Validation (Automatic) │
│ Agent: link-validator                  │
└───────────────────┬───────────────────┘
                    │ ⏱️  CHECKPOINT [显示 elapsed, remaining]
                    │
┌───────────────────┴───────────────────┐
│ Phase 2e: Task Handler (Optional)     │
│ Agent: task_handle                    │
└───────────────────────────────────────┘
                    │
                    ⏱️  FINAL SUMMARY [总用时, 各 phase 用时 breakdown]
```

**Important**:
- Phase 1.5 runs after Phase 1, before Phase 2a
- Phase 1.1 runs immediately after Phase 1 subagents complete (sequential check)
- Phase 2d runs automatically after Phase 2b
- **CLAUDE.md 是顺序编排器**：它依次等待每个 phase 完成，然后进入下一个

**⏱️ Time Re-allocation Rules (NO user confirmation - automatic)**:
- 基于实际 wall-clock 时间，不请求用户确认
- 如果 phases 完成 early → 自动将剩余时间 re-allocate 到 final phases
- 如果 wall-clock 达到 deadline → 立即停止，即使"还有预算"
- **Decision**: `reallocate_if = wall_clock_elapsed < total_budget AND phase_complete_early`

**⏱️  Time Checkpoint Format / 时间检查点格式**:

每个 phase 完成后，显示:
```
┌─────────────────────────────────────────┐
│  ⏱️  PHASE CHECKPOINT: [Phase Name]      │
├─────────────────────────────────────────┤
│  Elapsed:   5m 23s                      │
│  Remaining: 2h 54m 37s                  │
│  Progress:  [████░░░░░░░░] 15%           │
│  Next:      [Next Phase Name]           │
└─────────────────────────────────────────┘
```

对于 Phase 1 (Parallel Research), 显示每个 agent 的进度:
```
┌─────────────────────────────────────────┐
│  ⏱️  PHASE 1 PROGRESS                    │
├─────────────────────────────────────────┤
│  academic-researcher:   [████████░░] 80% │
│  github-watcher:       [██████░░░░] 60% │
│  community-listener:   [█████████░] 85% │
│                                          │
│  Overall: [███████░░░░] 75%             │
│  Elapsed: 45m 12s | Remaining: 1h 14m 48s│
└─────────────────────────────────────────┘
```

---

## Usage Formats / 使用格式

### Basic Query / 基本查询
```
深度研究 [topic]
Research [topic]
```

### With Time Budget / 指定时间预算
```
深度研究 [topic]，给我1小时
Research [topic] in 30min
```

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
```
深度研究 [topic]，最后帮我写一篇博客文章
Research [topic], then create a summary slide deck
```

---

## Correct vs Incorrect Workflow / 正确与错误工作流

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
1. performance-predictor: 决定是否需要 multi-agent (45% threshold)
2. framework-selector: 选择合适的框架
3. mcp-coordinator: 优化 MCP 工具选择 (5-6 MCPs, <80 tools)
4. timeout-specialist: 分配1小时预算
5. readiness-assessor: 检查生产就绪度 (如需要)
6. 部署 research subagents (带时间限制)
7. literature-analyzer: 逻辑分析
8. deep-research-report-writer + literature-review-writer: 双报告合成
9. link-validator: 链接验证 (自动)
10. task_handle: 定制任务输出 (如用户指定)
```

---

## Agent Knowledge Access Pattern / Agent 知识访问模式

### @knowledge 引用 / @knowledge References

每个 Agent 通过 `@knowledge` 指令访问知识库文件 (`.claude/knowledge/*.md`):

| Agent | Layer | 知识库文件 | 用途 |
|-------|-------|-----------|------|
| `performance-predictor` | 1 | hierarchical_orchestration.md, performance_metrics.md, framework_selection.md | 成本效益分析 |
| `framework-selector` | 1 | hierarchical_orchestration.md, framework_selection.md, orchestration_patterns.md | 框架选择逻辑 |
| `mcp-coordinator` | 1 | hierarchical_orchestration.md, observability_patterns.md | MCP 工具优化 |
| `academic-researcher` | 2 | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | 学术论文研究 + MAGMAMemory |
| `github-watcher` | 2 | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | GitHub 生态调研 + MAGMAMemory |
| `community-listener` | 2 | hierarchical_orchestration.md, memory_system.md, memory_graph.md, cross_domain_tracker.md | 社区讨论监听 + MAGMAMemory |
| `cross-domain-tracker` | - | cross_domain_tracker.md, memory_graph.md, memory_system.md | 跨域关系分析 |
| `literature-analyzer` | - | logic_analysis.md, research_state.md, memory_graph.md, memory_system.md | 逻辑关系分析 + 引用网络 |
| `deep-research-report-writer` | - | quality_checklist.md, report_templates.md, memory_graph.md, memory_system.md | 综合报告生成 |
| `literature-review-writer` | - | quality_checklist.md, report_templates.md, memory_graph.md, memory_system.md | 文献综述生成 |
| `visualization-generator` | - | visualization_patterns.md, memory_graph.md, memory_system.md | 可视化生成 |
| `link-validator` | - | quality_checklist.md, report_templates.md | 链接验证 |
| `timeout-specialist` | - | resilience_patterns.md | 超时和弹性模式 |
| `task_handle` | - | report_templates.md, quality_checklist.md | 定制任务输出 |

### CLI 工具调用 / CLI Tool Invocations

```bash
# Memory Graph CLI (v4.0)
python "tools\memory_graph_cli.py" --build
python "tools\memory_graph_cli.py" --query <arxiv_id>
python "tools\memory_graph_cli.py" --visualize --format html
python "tools\memory_graph_cli.py" --stats

# Memory System CLI (v9.0)
python "tools\memory_system.py" --save-graph research_data/semantic_graph.json
python "tools\memory_system.py" --migrate research_data/old_state.json --output research_data

# Cross-Domain Tracking (v2.0)
python "tools\cross_domain_tracker.py" --load-data research_data --stats
python "tools\cross_domain_tracker.py" --load-data research_data --bridging --min-domains 2
python "tools\cross_domain_tracker.py" --load-data research_data --save cross_domain_tracking_output.json

# Batch visualization generation
python "tools\generate_visualizations.py"
```

### Knowledge Files Reference / 知识库文件参考

**Knowledge files** (`.claude/knowledge/*.md`): 16 files
- `framework_selection.md` - Framework decision logic
- `orchestration_patterns.md` - Multi-agent coordination patterns
- `quality_checklist.md` - Quality validation criteria
- `report_templates.md` - Output format specifications
- `observability_patterns.md` - Metrics and monitoring patterns
- `resilience_patterns.md` - Retry and recovery mechanisms
- `visualization_patterns.md` - Visualization generation patterns
- `logic_analysis.md` - Citation and logic analysis
- `research_state.md` - State management patterns
- `performance_metrics.md` - Cost-benefit analysis data
- `hierarchical_orchestration.md` - 3-layer orchestration
- `memory_graph.md` - Semantic knowledge graph
- `memory_system.md` - MAGMA memory architecture
- `cross_domain_tracker.md` - Cross-domain tracking

**Python tools** (`tools/*.py`): 16 files
- `memory_graph_cli.py`, `memory_system.py`, `cross_domain_tracker.py`, `generate_visualizations.py`, etc.

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

**Coordination Overhead**: `Potential interactions = n(n-1)/2`

### When to Use Multi-Agent Systems / 何时使用多智能体系统

✅ **Use Multi-Agent When**:
- Single-agent success rate < 45% (Google/MIT threshold)
- Task has parallelizable aspects (embarrassingly parallel)
- Information exceeds single context window
- Interfacing with numerous complex tools

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
| **Comprehensive Platforms** | [microsoft/autogen](https://github.com/microsoft/autogen), [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) | Layered architecture, state management | Enterprise, production deployments | ✅ LangGraph (~400 companies) |
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
```

**Critical Insight**: Palantir reports 90% timeout failure rate with default 5-minute timeout. Solution: Orchestration object pattern with state persistence.

---

# PART II: THEORETICAL FOUNDATION / 理论基础

## Key Research Papers / 核心研究论文

| Area | Paper | arXiv ID | Key Contribution |
|------|-------|----------|-----------------|
| **Memory** | MAGMA: Multi-Graph Agentic Memory | [2601.03236](https://arxiv.org/abs/2601.03236) | Semantic + Temporal + Episodic |
| **Orchestration** | AgentOrchestra Framework | [2506.12508](https://arxiv.org/abs/2506.12508) | Meta-Orchestrator → Domain Leads |
| **Retrieval** | GraphRAG Benchmark | [2507.03608](https://arxiv.org/abs/2507.03608) | Vector + Graph RRF fusion |
| **Budget** | BudgetThinker | [2508.17196](https://arxiv.org/abs/2508.17196) | 66% budget adherence |
| **Timeout** | ALAS | [2511.03094](https://arxiv.org/abs/2511.03094) | 60% token reduction |
| **Collaboration** | Collaboration Survey | [2501.06322](https://arxiv.org/abs/2501.06322) | Comm + Coord + Coop |

## Orchestration Taxonomy / 编排分类

```
Centralized (本系统) → Single orchestrator, clear control flow
Decentralized → Peer-to-peer, scalable but complex
Hierarchical → Multi-level, team abstraction (AgentOrchestra)
```

## Memory Architecture / 记忆架构

| Type | Description | Use Case |
|------|-------------|----------|
| No Memory | Stateless | Simple tasks |
| Local Memory | Agent-private | Isolated work |
| Shared Memory | Global store | Small teams |
| **Hybrid (MAGMA)** | Semantic + Temporal + Episodic | **Production systems** |

## Production Features / 生产特性

- **Observability**: Token usage, latency, distributed tracing
- **Resilience**: Retry with backoff, circuit breaker, checkpoint recovery

---

# PART III: SYSTEM ARCHITECTURE / 系统架构

## Multi-Agent Research Orchestration / 多智能体研究编排

### Research Subagents / 研究子代理

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

```python
def transfer_to_academic_agent():
    return Handoff(target_agent=academic_agent, context={"topic": "current_research"})
```

| Pattern | Framework | Implementation | Use Case |
|---------|-----------|----------------|----------|
| Function Return | Swarm | `def transfer(): return agent` | Simple language-based routing |
| Agent-as-Tools | Agents SDK | `Agent(handoffs=[agent1, agent2])` | Orchestrator coordinating specialists |
| Context Filter | Agents SDK | `handoff(agent, input_filter=custom_filter)` | Reduce token overhead |
| Bidirectional | Both | Both agents link to each other | Triage with back-referral |

---

## Hierarchical Orchestration / 三层编排架构

**Active Engine**: `tools/hierarchical_orchestrator.py` (v9.0)
**基于**: [AgentOrchestra: A Hierarchical Multi-Agent Framework](https://arxiv.org/abs/2506.12508)

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

---

## Memory System Integration / 记忆系统集成

**Active Engine**: `tools/memory_system.py` (MAGMA v9.0)
**Based on**: [MAGMA: Multi-Graph Agentic Memory Architecture](https://arxiv.org/abs/2601.03236)

### Three-Layer Memory Architecture / 三层记忆架构

| Layer | Component | File | Purpose |
|-------|-----------|------|---------|
| **1** | SemanticMemory | `memory_graph.py` | Knowledge graph (papers, projects, concepts) |
| **2** | TemporalMemory | `memory_system.py` | Time-series tracking with provenance |
| **3** | EpisodicMemory | `memory_system.py` | Context windows for sessions |

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
[TARGET]          = "研究主题文件或直接输入"
[OUTPUT_DIR]      = "research_output"
[LANGUAGE_STYLE]  = "Chinese Narrative + English Terminology"

# Optional / 可选
[TIME_BUDGET]     = "1h" / "30min" / None
[FRAMEWORK]       = "LangGraph" / "CrewAI" / "AutoGen" / None
[CUSTOM_TASK]     = "blog" / "slides" / "code" / None
```

---

## Phase-by-Phase Execution / 分阶段执行

### Phase -1: Performance Prediction / 性能预测

```python
Task(
    subagent_type="performance-predictor",
    prompt=f"""Analyse this research query: {query}

Provide:
1. Query type classification (simple_fact_finding, direct_comparison, complex_research, deep_synthesis)
2. Estimated single-agent success rate (%)
3. Parallelizability assessment
4. Cost-benefit recommendation (multi-agent vs single-agent)
5. Optimal agent count if multi-agent recommended
6. **Estimated time budget (seconds)** based on complexity:
   - simple: 600s (10 minutes)
   - medium: 1800s (30 minutes)
   - complex: 3600s (60 minutes)
   - deep: 7200s (120 minutes)

Output format: JSON with keys: query_type, success_rate, parallelizable, recommendation, estimated_time_seconds"""
)
```

**决策逻辑**: IF `single_agent_success_rate < 45% AND parallelizable_aspects >= 2` → Continue Phase 0

**Time Budget Storage**: Store performance-predictor's time estimation for use if user doesn't specify time budget.

---

### Phase 0: Framework Selection / 框架选择

```python
Task(
    subagent_type="framework-selector",
    prompt=f"""Based on query analysis:
- Query type: {query_type}
- Complexity: {complexity}
- Parallelizable: {parallelizable}

Recommend:
1. Primary framework (LangGraph, CrewAI, AutoGen, etc.)
2. Reasoning based on query characteristics
3. Production readiness assessment
4. Alternative options"""
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

```python
Task(
    subagent_type="mcp-coordinator",
    prompt=f"""For this research query: {query}

Recommend:
1. Which 5-6 MCPs to activate (from 20-30 configured)
2. Total tool count (< 80)
3. Estimated token cost of tool definitions
4. Excluded MCPs and reasoning"""
)
```

**优化规则**: Total MCPs configured: 20-30, Active per session: 5-6, Total active tools: < 80

---

### Phase 0.75: Production Readiness / 生产就绪度 (可选)

```python
Task(
    subagent_type="readiness-assessor",
    prompt=f"""Assess production readiness for: {framework_or_pattern}

Check:
1. State persistence capability
2. Observability tools
3. Error handling mechanisms
4. Active maintenance status
5. Production deployments evidence

WARNING: Swarm is EDUCATIONAL ONLY - NO state persistence"""
)
```

---

### ⏱️ TIME CONFIRM - 显示给用户 (CRITICAL - 在 Phase 1 之前!)

**重要**: 必须在启动 research subagents 之前，向用户显示时间预算确认!

```python
### TIME CONFIRM - 显示给用户确认
print(f"""
┌─────────────────────────────────────────────────────────────┐
│  ⏱️  TIME BUDGET CONFIRMATION                               │
├─────────────────────────────────────────────────────────────┤
│  总预算:           {time_allocation['total_budget_minutes']} 分钟               │
│  单个 Agent 时间:  {time_allocation['per_agent_timeout_minutes']} 分钟 (并行运行)        │
│  检查点间隔:       {time_allocation['checkpoint_interval_minutes']} 分钟                 │
│  你实际等待时间:    ~{time_allocation['total_budget_minutes']} 分钟 (agents 并行)       │
│                                                              │
│  说明: 每个 agent 获得 {time_allocation['per_agent_timeout_minutes']} 分钟全部时间         │
│        (不是除以 3! agents 同时运行)                         │
│                                                              │
│  开始研究? (开始后 agents 将并行运行)                         │
└─────────────────────────────────────────────────────────────┘
""")
```

**用户确认后再启动 Phase 1**

---

### Phase 0.85: Timeout Budget Allocation / 超时预算分配 (内部计算)

```python
### Time Budget Calculation / 时间预算计算 (内部使用)

# Import utility functions from checkpoint_manager
from tools.checkpoint_manager import (
    parse_time_budget,
    calculate_time_allocation,
    calculate_max_turns,
    generate_time_budget_string,
    format_time_confirmation,
    should_continue_agent,
    generate_continuation_prompt,
    TimeBudgetTracker,           # v9.4: Track time saved across phases
    format_phase_checkpoint,       # v9.4: Format phase checkpoints
    get_time_assessment_from_allocation  # v9.4: Get time assessment
)

# Initialize time allocation (will be populated from user spec or performance-predictor)
time_allocation = None

# 来源1: 用户明确指定 (优先级最高)
user_time_budget = parse_time_budget(user_query)
if user_time_budget:
    # Calculate time allocation using utility function
    time_allocation = calculate_time_allocation(
        total_budget_seconds=user_time_budget['total_seconds'],
        subagent_count=3,
        coordination_overhead=0.20
    )
    time_allocation['time_source'] = 'user_specified'

# 来源2: performance-predictor估算 (如果没有用户指定)
if not time_allocation:
    # This runs after Phase -1, so we have performance_result
    # performance_result should include estimated_time_seconds
    performance_time_estimate = performance_result.get("estimated_time_seconds", 1800)  # default 30min

    time_allocation = calculate_time_allocation(
        total_budget_seconds=performance_time_estimate,
        subagent_count=3
    )
    time_allocation['time_source'] = 'performance_predictor'

# TIME CONFIRM: Display time allocation (information only, no confirmation needed)
print(f"""
[TIME BUDGET CONFIRM - Automatic Re-allocation Enabled]
├─ Total Budget: {time_allocation['total_budget_minutes']} minutes
├─ Per-Agent Timeout: {time_allocation['per_agent_timeout_minutes']} minutes (NOT divided by 3!)
├─ Wall-clock you wait: ~{time_allocation['total_budget_minutes']} minutes (agents run in parallel)
├─ Checkpoint Interval: {time_allocation['checkpoint_interval_minutes']} minutes
├─ Time Source: {time_allocation['time_source']}
└─ Start Time: {time_allocation['start_time_iso']}
""")

# Initialize TimeBudgetTracker for automatic re-allocation (NO user confirmation)
time_tracker = TimeBudgetTracker(
    total_budget_seconds=time_allocation['total_budget_seconds'],
    start_time_iso=time_allocation['start_time_iso']
)
```

**Key Formula**: `Per-Agent Time = Total Budget × 80%` (每个 agent 获得全部可用时间，不是除以3！)

**Time Budget Example**:
```python
# 用户: "深度研究 LangGraph，给我1小时"
# time_allocation = {
#     "per_agent_timeout_seconds": 2880,  # 48 minutes = 3600 × 80%
#     "checkpoint_interval_seconds": 288,  # ~5 minutes
#     "start_time_iso": "2026-02-11T10:30:00Z",
#     "time_source": "user_specified",
#     "total_budget_seconds": 3600
# }
```

---

### Phase 1: Research Subagent Deployment / 研究子代理部署

```python
### Calculate max_turns based on time allocation
# Use utility function to calculate max_turns
max_turns_per_agent = None
time_budget_str = ""

if time_allocation:
    # Calculate max_turns: assuming 2 minutes (120 seconds) per turn on average
    max_turns_per_agent = calculate_max_turns(
        per_agent_timeout_seconds=time_allocation.get("per_agent_timeout_seconds", 0),
        seconds_per_turn=120
    )

    # Generate TIME_BUDGET string for subagent prompts
    time_budget_str = generate_time_budget_string(time_allocation)

# TIME CONFIRM: Display deployment parameters before launching subagents
print(f"""
[TIME CONFIRM - Phase 1: Subagent Deployment]
├─ Max Turns per Agent: {max_turns_per_agent}
├─ Per-Agent Timeout: {time_allocation.get('per_agent_timeout_minutes', 'N/A')} minutes
├─ Subagents to Deploy: 3 (academic-researcher, github-watcher, community-listener)
└─ Time Budget String Generated: {len(time_budget_str)} characters
""")

# 并行部署（在一个 Claude 消息中）
# IMPORTANT: Pass max_turns parameter to enforce time limits
Task(
    subagent_type="academic-researcher",
    prompt=f"""...原有prompt...
{time_budget_str}
""",
    max_turns=max_turns_per_agent  # 关键：传递max_turns参数
)

Task(
    subagent_type="github-watcher",
    prompt=f"""...原有prompt...
{time_budget_str}
""",
    max_turns=max_turns_per_agent
)

Task(
    subagent_type="community-listener",
    prompt=f"""...原有prompt...
{time_budget_str}
""",
    max_turns=max_turns_per_agent
)
```

**Subagent Task Specification**: 每个 Subagent 必须收到:
1. **Objective**: 明确的研究目标
2. **Output Format**: 期望的输出格式（包含详细的 JSON 字段要求）
3. **Tool Guidance**: 哪些工具优先使用
4. **Source Guidance**: 哪些信息源最相关
5. **Task Boundaries**: 什么在范围内，什么不在
6. **Quality Requirements**: 最小产出标准和质量检查清单
7. **Time Budget Constraints** (当 time_allocation 存在时):
   - `per_agent_timeout_seconds`: 每个agent的时间限制
   - `start_time_iso`: 开始时间（ISO格式）
   - `checkpoint_interval_seconds`: 检查点间隔
   - `time_source`: 时间来源（user_specified 或 performance_predictor）

**Critical**: `max_turns` 参数直接传递给 Task 工具，强制限制子智能体的执行轮次。当达到限制时，子智能体会优雅终止，已保存的checkpoint不会丢失。

---

### Phase 1.1: Subagent Completion Check & Continuation (子智能体完成检查与续传)

**Purpose**: 检查子智能体是否因时间限制提前终止，如果是则从 checkpoint 继续执行。

**Trigger**: 当任何 research subagent 完成后（无论成功还是因 max_turns 限制终止）

**Continuation Protocol**:

```python
### Phase 1.1: Check and Continue Incomplete Subagents

# 定义最小完成要求
MINIMUM_REQUIREMENTS = {
    "academic-researcher": {"papers_analyzed": 5, "key_papers": 3},
    "github-watcher": {"projects_analyzed": 8, "key_projects": 4},
    "community-listener": {"threads_analyzed": 15, "consensus_points": 3}
}

def check_minimum_requirements(output_file: str, agent_type: str) -> tuple[bool, dict]:
    """
    检查 subagent 输出是否满足最小要求

    Returns:
        (is_complete, remaining_requirements)
    """
    from pathlib import Path
    import json

    output_path = Path(output_file)
    if not output_path.exists():
        return False, {"error": "Output file not found"}

    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    findings = data.get("research_findings", {})
    requirements = MINIMUM_REQUIREMENTS.get(agent_type, {})
    remaining = {}

    for key, min_value in requirements.items():
        current_value = findings.get(key, 0)
        if current_value < min_value:
            remaining[key] = {
                "current": current_value,
                "required": min_value,
                "remaining": min_value - current_value
            }

    return len(remaining) == 0, remaining

# 等待所有 subagents 完成
# 注意：CLAUDE.md 是顺序执行，必须等待每个 Task 完成
academic_result = wait_for_task(academic_task)
github_result = wait_for_task(github_task)
community_result = wait_for_task(community_task)

# TIME CONFIRM: Check elapsed time after subagent completion
if time_allocation:
    from tools.checkpoint_manager import get_time_assessment_from_allocation
    time_assessment = get_time_assessment_from_allocation(time_allocation)
    print(f"""
[TIME CONFIRM - Phase 1.0: Subagent Completion]
├─ Elapsed Time: {time_assessment.get('elapsed_formatted', 'N/A')}
├─ Remaining Time: {time_assessment.get('remaining_formatted', 'N/A')}
├─ Time Status: {time_assessment.get('time_status', 'unknown')}
└─ Should Accelerate: {time_assessment.get('should_accelerate', False)}
""")

# 检查每个 subagent 的完成状态
subagents = [
    ("academic-researcher", academic_result, "research_data/academic_researcher_output.json"),
    ("github-watcher", github_result, "research_data/github_researcher_output.json"),
    ("community-listener", community_result, "research_data/community_researcher_output.json")
]

for agent_type, result, output_file in subagents:
    is_complete, remaining = check_minimum_requirements(output_file, agent_type)

    if not is_complete:
        # 检查是否有 checkpoint 可以继续
        from pathlib import Path
        checkpoint_dir = Path("research_data/checkpoints")
        checkpoints = sorted(checkpoint_dir.glob(f"{agent_type.replace('-', '_')}_*.json"))

        if checkpoints:
            latest_checkpoint = checkpoints[-1]

            # 使用 utility 函数判断是否继续
            if time_allocation:
                should_continue, remaining_seconds, status = should_continue_agent(time_allocation)

                if status == "continue":
                    new_max_turns = calculate_max_turns(remaining_seconds, seconds_per_turn=120)

                    # 使用 utility 函数生成 continuation prompt
                    continuation_prompt = generate_continuation_prompt(
                        agent_type=agent_type,
                        output_file=output_file,
                        remaining_requirements=remaining,
                        remaining_seconds=remaining_seconds
                    )

                    # 添加 checkpoint 信息到 prompt
                    continuation_prompt += f"\n\nLATEST CHECKPOINT: {latest_checkpoint}"

                    print(format_time_confirmation(
                        f"Phase 1.1: Relaunch {agent_type}",
                        time_allocation,
                        {
                            "New Max Turns": new_max_turns,
                            "Checkpoint": latest_checkpoint.name,
                            "Mode": "ACCELERATE" if remaining_seconds < 1200 else "CONTINUATION"
                        }
                    ))

                    # 重新启动 agent
                    Task(
                        subagent_type=agent_type,
                        prompt=continuation_prompt,
                        max_turns=new_max_turns
                    )

                    # 等待 relaunch 完成并再次检查
                    relaunch_complete, relaunch_remaining = check_minimum_requirements(output_file, agent_type)

                    print(format_time_confirmation(
                        f"Phase 1.1: Relaunch Complete ({agent_type})",
                        time_allocation,
                        {
                            "Now Complete": relaunch_complete,
                            "Still Missing": str(relaunch_remaining) if not relaunch_complete else "None"
                        }
                    ))

                    # 如果仍未完成且还有时间，可以再尝试一次（最多2次续传）
                    if not relaunch_complete and remaining_seconds >= 600:
                        final_max_turns = calculate_max_turns(remaining_seconds // 2, seconds_per_turn=120)
                        final_prompt = generate_continuation_prompt(
                            agent_type=agent_type,
                            output_file=output_file,
                            remaining_requirements=relaunch_remaining,
                            remaining_seconds=remaining_seconds // 2
                        )
                        final_prompt += "\n\nThis is your SECOND and FINAL continuation. Complete rapidly."

                        print(f"[TIME CONFIRM - Phase 1.1: Final Relaunch {agent_type}]")
                        print(f"├─ Last attempt with {final_max_turns} turns")

                        Task(
                            subagent_type=agent_type,
                            prompt=final_prompt,
                            max_turns=final_max_turns
                        )

                elif status == "insufficient_time":
                    print(format_time_confirmation(
                        f"Phase 1.1: Skip {agent_type}",
                        time_allocation,
                        {
                            "Required": "5 minutes minimum",
                            "Status": "INSUFFICIENT TIME - accepting incomplete"
                        }
                    ))
        else:
            print(f"[CLAUDE.md] No checkpoint found for {agent_type}, cannot continue")
```

**Minimum Requirements by Agent Type**:

| Agent Type | Minimum Papers/Projects | Minimum Key Items | Rationale |
|------------|------------------------|-------------------|-----------|
| `academic-researcher` | 5 papers analyzed | 3 key papers | Basic coverage of research topic |
| `github-watcher` | 8 projects analyzed | 4 key projects | Representation across tech factions |
| `community-listener` | 15 threads analyzed | 3 consensus points | Minimum community validation |

**Acceleration Mode Protocol**:

当 subagent 进入续传模式时：
1. **Skip full-text downloads** — 使用 abstract 和 summary
2. **Limit citation chains** — 只追踪直接引用，不递归
3. **Reduce tool calls** — 批量处理而非逐个查询
4. **Simplify output** — 跳过详细分析，保留核心发现

**Checkpoint Resume Format**:

```json
{
  "checkpoint_number": 2,
  "phase": "phase2_deep_exploration",
  "timestamp": "2026-02-11T12:00:00Z",
  "items_processed": 3,
  "time_assessment": {
    "elapsed_seconds": 1800,
    "remaining_seconds": 300,
    "time_status": "time_critical"
  },
  "content": {
    "work_summary": "Analyzed 3 papers: 2501.03236, 2506.12508, 2507.03608",
    "next_steps": [
      "Download remaining 2 papers",
      "Build citation network",
      "Identify research gaps"
    ]
  }
}
```

---

### Phase 1.5: Cross-Domain Tracking / 跨域关系追踪

```python
# Mark Phase 1 as complete for time tracking
time_tracker.end_phase("Phase 1")

# TIME CHECKPOINT: Display current progress
print(format_phase_checkpoint(
    "Phase 1.5: Cross-Domain Tracking",
    time_allocation,
    progress_percent=60,
    next_phase="Logic Analysis"
))

if time_allocation:
    print(format_time_confirmation("Phase 1.5: Cross-Domain Tracking", time_allocation))
Task(
    subagent_type="cross-domain-tracker",
    prompt=f"""Analyze cross-domain relationships between research domains.

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

See .claude/agents/cross-domain-tracker.md for complete specification."""
)
```

---

### Phase 2a: Logic Analysis / 逻辑分析

```python
# Mark Phase 1.5 as complete for time tracking
time_tracker.end_phase("Phase 1.5")

# TIME CHECKPOINT: Before logic analysis
print(format_phase_checkpoint(
    "Phase 2a: Logic Analysis",
    time_allocation,
    progress_percent=75,
    next_phase="Report Synthesis"
))

if time_allocation:
    print(format_time_confirmation("Phase 2a: Logic Analysis", time_allocation))

Task(
    subagent_type="literature-analyzer",
    prompt=f"""Analyze research data for logical relationships.

INPUT DATA:
- Academic research: research_data/academic_research_output.json
- GitHub research: research_data/github_research_output.json
- Community research: research_data/community_research_output.json
- Cross-domain tracking: research_data/cross_domain_tracking_output.json

OUTPUT: research_data/logic_analysis.json

See .claude/agents/literature-analyzer.md for complete specification."""
)
```

The `literature-analyzer` agent handles:
- Analyzing citation relationships and inheritance chains
- Identifying thematic clusters and methodological families
- Tracing technical evolution and paradigm shifts
- Extracting research gaps and open questions

---

### Phase 2b: Dual Report Synthesis / 双报告合成

```python
# ⏱️ AUTOMATIC TIME RE-ALLOCATION - No user confirmation, based on wall-clock
from tools.checkpoint_manager import TimeBudgetTracker, format_phase_checkpoint

# Initialize tracker at session start (before Phase -1)
time_tracker = TimeBudgetTracker(
    total_budget_seconds=time_allocation['total_budget_seconds'],
    start_time_iso=time_allocation['start_time_iso']
)

# Mark completed phases (done after each phase finishes)
for phase in ["Phase -1", "Phase 0", "Phase 0.5", "Phase 0.75", "Phase 1", "Phase 1.1", "Phase 1.5", "Phase 2a"]:
    time_tracker.end_phase(phase)

# Before report synthesis, check wall-clock time saved
saved_info = time_tracker.get_saved_time()
wall_clock_elapsed = (datetime.now() - datetime.fromisoformat(time_allocation['start_time_iso'])).total_seconds()
wall_clock_remaining = time_allocation['total_budget_seconds'] - wall_clock_elapsed

# Re-allocation decision: ONLY if wall-clock says we have time
if wall_clock_remaining > 600:  # At least 10 minutes wall-clock remaining
    reallocated_seconds = int(saved_info['total_saved_seconds'] + wall_clock_remaining)
    reallocated_minutes = reallocated_seconds // 60

    print(f"""
┌─────────────────────────────────────────────────────────────┐
│  ⏱️  TIME SAVED - Auto re-allocating {reallocated_minutes}min to Reports   │
├─────────────────────────────────────────────────────────────┤
│  Wall-clock elapsed: {int(wall_clock_elapsed // 60)}min                         │
│  Wall-clock remaining: {int(wall_clock_remaining // 60)}min                       │
│  Phases under budget: {len(saved_info['phases_under_budget'])}                     │
│                                                                      │
│  ACTION: Report writers get +{reallocated_minutes}min for quality           │
│  • Deeper analysis and synthesis                                  │
│  • Comprehensive citation verification                            │
│  • Enhanced quality validation                                    │
└─────────────────────────────────────────────────────────────┘
""")

    # Extend time allocation for report writers
    extended_time_allocation = time_allocation.copy()
    extended_time_allocation['per_agent_timeout_seconds'] = wall_clock_remaining
    extended_time_allocation['per_agent_timeout_minutes'] = int(wall_clock_remaining / 60)
    extended_time_allocation['mode'] = 'extended_quality'

else:
    # Wall-clock says stop - use original allocation
    print(f"[TIME CONFIRM] Wall-clock at deadline - using standard allocation")
    extended_time_allocation = time_allocation
    extended_time_allocation['mode'] = 'standard'
```

**Comprehensive Report** (with extended time if wall-clock allows):
```python
# Pass extended_time_allocation to report writers
Task(
    subagent_type="deep-research-report-writer",
    prompt=f"""Synthesize research findings into a comprehensive report.

TIME ALLOCATION: You have {extended_time_allocation['per_agent_timeout_minutes']} minutes total.
If the research phases completed early, use the extra time for:
- Deeper analysis of findings
- More comprehensive citation verification
- Enhanced quality validation
- Additional synthesis insights

**Comprehensive Report**:
```python
Task(
    subagent_type="deep-research-report-writer",
    prompt=f"""Synthesize research findings into a comprehensive report.

INPUT DATA:
- Academic research: research_data/academic_research_output.json
- GitHub research: research_data/github_research_output.json
- Community research: research_data/community_research_output.json

TOPIC: {original_query}

OUTPUT: research_output/{sanitized_topic}_comprehensive_report.md

See .claude/agents/deep-research-report-writer.md for complete specification."""
)
```

**Literature Review**:
```python
Task(
    subagent_type="literature-review-writer",
    prompt=f"""Generate academic literature review based on logic analysis.

INPUT DATA:
- Research data: research_data/*.json
- Logic analysis: research_data/logic_analysis.json

OUTPUT: research_output/{sanitized_topic}_literature_review.md

See .claude/agents/literature-review-writer.md for complete specification."""
)
```

**Note**: The two report writers can run in parallel after logic analysis completes.

---

### Phase 2d: Link Validation / 链接验证 (Automatic)

```python
Task(
    subagent_type="link-validator",
    prompt=f"""Validate all links in the generated research reports.

INPUT FILES:
- research_output/{sanitized_topic}_comprehensive_report.md
- research_output/{sanitized_topic}_literature_review.md

REQUIREMENTS:
- Extract all Markdown links [text](url)
- Validate each URL via webReader
- Categorize by type (arxiv, github, doi, other)
- Report status (valid, broken, timeout)

OUTPUT: research_data/link_validation_output.json"""
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

```python
user_task = parse_user_task(original_query)
IF user_task EXISTS:
    Task(
        subagent_type="task_handle",
        prompt=f"""Complete the following task based on research results:

USER TASK: {user_task}
INPUT_REPORTS:
- research_output/{sanitized_topic}_comprehensive_report.md
- research_output/{sanitized_topic}_literature_review.md

OUTPUT: research_output/{sanitized_topic}_{task_type}.md"""
    )
```

**支持的输出格式**: Blog Post, Slide Deck, Code Examples, Summary, JSON for API, Comparison Table, Technical Proposal, Custom

---

### Phase 3: Report Delivery / 报告交付

```python
# TIME CONFIRM: Final time assessment at completion
if time_allocation:
    time_assessment = get_time_assessment_from_allocation(time_allocation)
    efficiency = int((time_assessment.get('elapsed_seconds', 0) / time_allocation.get('total_budget_seconds', 1)) * 100)

    print(format_time_confirmation(
        "Phase 3: Report Delivery - FINAL",
        time_allocation,
        {
            "Total Budget": f"{time_allocation.get('total_budget_minutes', 'N/A')} minutes",
            "Time Efficiency": f"{efficiency}% used"
        }
    ))
```

After both report writer agents complete:

**Verify comprehensive report quality**:
- [ ] research_output/{topic}_comprehensive_report.md exists
- [ ] Word count 6,000-8,000
- [ ] Executive Summary has 6-8 insights
- [ ] Citation graph (Mermaid) included
- [ ] All citations clickable

**Verify literature review quality**:
- [ ] research_output/{topic}_literature_review.md exists
- [ ] Word count 3,000-5,000
- [ ] Logical flow (not mechanical listing)
- [ ] Uses logic_analysis.json insights
- [ ] Contains evolution paths and paradigm shifts

**Review link validation results**:
- [ ] research_data/link_validation_output.json exists
- [ ] All links validated (100% coverage)
- [ ] If broken_links > 0: Report details to user

**Deliver to user**:
- Comprehensive report: {topic}_comprehensive_report.md
- Literature review: {topic}_literature_review.md
- Link validation summary (if issues found)
- Custom task output (if task_handle was used)
- Summary of key findings from both reports

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

**Comprehensive Report**: See `.claude/agents/deep-research-report-writer.md` for complete Gemini Deep Research report structure, citation relationship graph (Mermaid), LaTeX formula formatting, bilingual output requirements, clickable citation standards, quality checklists.

**Literature Review**: See `.claude/agents/literature-review-writer.md` for academic literature review structure, logic-driven narrative flow, evolution path analysis, research gaps and open questions.

**Custom Task Output**: See `.claude/agents/task_handle.md` for flexible output formats (blog, slides, code examples, etc.), web reading capability, custom format generation.

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
1. **性能感知**: 45% threshold rule
2. **框架选择**: "AutoGen快、CrewAI稳、LangGraph强"
3. **编排优化**: 20-30 个 MCP 配置，每次启用 5-6 个，工具总数 <80
4. **职责分离**: CLAUDE.md 编排，subagents 执行，report-writers 撰写
5. **记忆系统**: MAGMAMemory 自动保存研究发现，构建跨 session 引用网络
6. **双输出系统**: 综合报告 + 文献综述
7. **链接验证**: link-validator agent 自动验证所有报告链接
8. **定制输出**: task_handle agent 支持灵活的定制化输出格式
