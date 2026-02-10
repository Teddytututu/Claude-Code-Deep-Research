# Framework Selection Knowledge Base

## Overview
从 `framework_selection.py` 提取的框架选择核心逻辑

**Purpose**: 提供 2026 年多智能体框架选择决策支持

---

## Key Classes / 类

### FrameworkCategory

**Purpose**: 框架分类枚举

**Values**:
- `LIGHTWEIGHT_ORCHESTRATION`: 轻量级编排 (Swarm, Agents SDK)
- `COMPREHENSIVE_PLATFORM`: 综合平台 (LangGraph, AutoGen)
- `ROLE_BASED_COLLABORATION`: 基于角色的协作 (CrewAI, MetaGPT)
- `OBSERVABILITY_DEVTOOLS`: 可观测性工具 (AgentOps)
- `CLI_NATIVE_CODING`: CLI 原生开发 (Claude Code)

### ProductionReadiness

**Purpose**: 生产就绪度等级

**Values**:
- `EDUCATIONAL_ONLY`: 仅教育用途 (Swarm)
- `EMERGING`: 新兴 (Agents SDK, MetaGPT)
- `PRODUCTION_READY`: 生产就绪 (CrewAI, AutoGen, AgentOps)
- `ENTERPRISE_STANDARD`: 企业标准 (LangGraph)

### FrameworkInfo

**Purpose**: 框架信息数据结构

**Key Attributes**:
- `name`: 框架名称
- `category`: FrameworkCategory 枚举值
- `production_readiness`: ProductionReadiness 枚举值
- `companies_deployed`: 部署公司数量
- `latency_overhead`: 延迟开销 (百分比)
- `time_to_production`: 上线时间
- `key_features`: 关键特性列表
- `limitations`: 局限性列表
- `recommendation`: 推荐理由

### FrameworkSelector2026

**Purpose**: 框架选择器主类

**Key Methods**:
- `recommend_framework(use_case, priority, team_size, timeline)`: 根据需求推荐框架
- `get_chinese_consensus()`: 获取中文社区共识
- `get_decision_tree()`: 获取决策树
- `get_production_metrics()`: 获取生产指标

### MCPDynamicSelector

**Purpose**: MCP 工具动态选择

**Key Methods**:
- `select_mcps(query, session_id, max_mcps, max_tools)`: 选择最优 MCP 组合
- `get_tool_count(mcp_names)`: 获取工具总数
- `estimate_token_cost(mcp_names)`: 估算 token 成本

---

## Decision Logic / 决策逻辑

### Framework Decision Tree

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

### Decision Matrix (Code Logic)

```python
def recommend_framework(use_case, priority, team_size, timeline):
    """
    框架推荐逻辑

    Args:
        use_case: 使用场景描述
        priority: 优先级 (production/speed/simplicity/learning)
        team_size: 团队规模 (small/medium/large)
        timeline: 时间线 (immediate/weeks/months/flexible)
    """

    # Priority-based routing
    if priority == "learning":
        return frameworks["swarm"]  # Educational only

    elif priority == "speed" or timeline == "immediate":
        if "role" in use_case or "team" in use_case:
            return frameworks["crewai"]  # 2 weeks to production
        else:
            return frameworks["openai_agents_sdk"]  # Emerging but fast

    elif priority == "production":
        if "complex" in use_case or "branching" in use_case:
            return frameworks["langgraph"]  # Enterprise standard
        elif "conversation" in use_case or "iterative" in use_case:
            return frameworks["autogen"]  # Microsoft ecosystem
        else:
            return frameworks["langgraph"]  # Default production

    elif priority == "simplicity":
        if "team" in use_case or "role" in use_case:
            return frameworks["crewai"]
        else:
            return frameworks["openai_agents_sdk"]

    return frameworks["langgraph"]  # Default
```

### Chinese Community Consensus

```
"AutoGen快、CrewAI稳、LangGraph强"

┌──────────┬──────────────┬─────────────────┬─────────────┐
│ Framework │ 中文评价     │ 特点            │ 生产就绪度  │
├──────────┼──────────────┼─────────────────┼─────────────┤
│ AutoGen  │ 快 (Fast)    │ 快速原型        │ Production  │
│ CrewAI   │ 稳 (Stable)  │ 角色协作        │ Production  │
│ LangGraph│ 强 (Powerful)│ 企业级状态管理  │ Enterprise  │
└──────────┴──────────────┴─────────────────┴─────────────┘
```

### MCP Selection Logic

```python
def select_mcps(query, max_mcps=6, max_tools=80):
    """
    MCP 选择算法

    优化目标:
    - 最大化相关性 (query vs MCP description)
    - 最小化 token 成本 (tool definitions)
    - 限制工具数量 (< 80)
    """

    # 1. 评分: 相关性 / token_cost
    for mcp in available_mcps:
        score = calculate_relevance(query, mcp) / mcp.tool_count

    # 2. 贪心选择: 取 top N
    selected = greedy_select(scores, max_mcps, max_tools)

    # 3. 确保必需 MCP
    if "web-search-prime" not in selected:
        selected.append("web-search-prime")

    return selected
```

---

## Production Metrics / 生产指标

### Framework Performance Comparison

| Framework | Companies | Latency Overhead | Time to Production | Daily Executions |
|-----------|-----------|------------------|-------------------|------------------|
| **LangGraph** | ~400 | 8% | 2 months | 100,000+ |
| **CrewAI** | 150+ | 24% | 2 weeks | 100,000+ |
| **AutoGen** | 200 | 15% | 1-2 months | - |
| **Swarm** | 0 (edu) | 0% | N/A | - |
| **Agents SDK** | ~50 | 5% | 3-4 weeks | - |

### Warning Labels

⚠️ **Swarm is EDUCATIONAL ONLY**:
- No state persistence
- No error handling
- No observability
- NOT for production

⚠️ **Agents SDK is EMERGING**:
- Released Nov 2025
- Evolving rapidly
- Breaking changes may occur

---

## Code Patterns / 代码模式

### Pattern 1: Framework Recommendation

```python
# 推荐框架给用户
selector = FrameworkSelector2026()
framework = selector.recommend_framework(
    use_case="Multi-agent research system",
    priority="production",
    team_size="medium",
    timeline="months"
)

print(f"Recommended: {framework.name}")
print(f"Reason: {framework.recommendation}")
print(f"Latency: {framework.latency_overhead}%")
```

### Pattern 2: MCP Dynamic Selection

```python
# 动态选择 MCP
mcp_selector = MCPDynamicSelector()
selected_mcps = mcp_selector.select_mcps(
    query="Research recent papers on multi-agent systems",
    max_mcps=6,
    max_tools=80
)

# 结果: ["arxiv-mcp-server", "web-search-prime", "web-reader", ...]
```

---

## CLI Usage / 命令行使用

```bash
python "tools\framework_selection.py" --recommend
python "tools\framework_selection.py" --metrics
python "tools\framework_selection.py" --tree
python "tools\framework_selection.py" --upgrade-plan
```

**Commands**:
- `--recommend`: 交互式推荐
- `--metrics`: 显示生产指标 (JSON)
- `--tree`: 显示决策树 (ASCII)
- `--upgrade-plan`: 生成 v9.0 升级计划 (JSON)

---

## Integration Points / 集成点

**Reading Agents**:
- `framework-selector`: 使用此知识库进行框架推荐决策

**CLI Invocations**:
```bash
# Agent 可调用此命令获取量化推荐
python "tools\framework_selection.py" --recommend --query "{user_query}"
```

**Knowledge Base References**:
- `.claude/knowledge/orchestration_patterns.md`: 编排模式相关

---

## Notes / 说明

- **Swarm WARNING**: 始终提醒用户 Swarm 不适合生产环境
- **Chinese Consensus**: "AutoGen快、CrewAI稳、LangGraph强" 是社区共识
- **LangGraph = Default**: 对于生产环境，LangGraph 是默认选择
- **MCP Optimization**: 总是限制活动 MCP 在 5-6 个，工具总数 < 80
