# Orchestration Patterns Knowledge Base

## Overview
从 `research_orchestrator.py` 提取的多智能体编排模式核心逻辑

**Purpose**: 提供基于 Anthropic multi-agent research system 的编排模式

---

## Key Classes / 类

### AgentRole

**Purpose**: 研究代理角色枚举

**Values**:
- `LEAD`: 首席研究员 (Opus 4.5)
- `ACADEMIC`: 学术研究子代理 (Sonnet 4)
- `GITHUB`: GitHub 观察子代理 (Sonnet 4)
- `COMMUNITY`: 社区监听子代理 (Sonnet 4)
- `CITATION`: 引用处理代理 (Sonnet 4)

### Agent

**Purpose**: 代理配置数据结构

**Key Attributes**:
- `name`: 代理名称
- `role`: AgentRole 枚举值
- `instructions`: 任务指令文本
- `tools`: 工具列表
- `model`: 使用的模型 (默认 claude-sonnet-4-20250514)
- `max_turns`: 最大轮次 (默认 20)

### Handoff

**Purpose**: Swarm 风格的代理切换模式

**Code Pattern**:
```python
@dataclass
class Handoff:
    target_agent: Agent
    context: Dict[str, Any] = field(default_factory=dict)

# Usage:
def transfer_to_github_agent():
    return Handoff(target_agent=github_agent, context={"repo": "langgraph"})
```

### ResearchState

**Purpose**: LangGraph 风格的状态管理

**Key Attributes**:
- `query`: 研究查询
- `phase`: 当前阶段 (planning/research/synthesis/complete)
- `findings`: 研究发现字典
- `citations`: 引用列表
- `token_budget`: Token 预算 (默认 200000)
- `session_id`: 会话 ID (UUID)
- `start_time`: 开始时间 (ISO 格式)

**Methods**:
- `to_json()`: 序列化为 JSON
- `from_json(json_str)`: 从 JSON 反序列化

### ResearchOrchestrator

**Purpose**: 多智能体研究编排器主类

**Key Methods**:
- `analyze_query_complexity(query)`: 分析查询复杂度
- `run_research(query, max_subagents, parallel, output_dir)`: 执行研究
- `_parallel_execute()`: 并行执行子代理
- `_sequential_execute()`: 顺序执行子代理

### ResearchStateManager

**Purpose**: 状态持久化管理

**Key Methods**:
- `save_state(session_id, state)`: 保存状态
- `load_state(session_id)`: 加载状态
- `list_sessions()`: 列出所有会话

---

## Decision Logic / 决策逻辑

### Query Complexity Analysis

```python
def analyze_query_complexity(query):
    """
    分析查询复杂度，决定是否使用 multi-agent

    Decision Criteria:
    - Single-agent success rate < 45% → Use multi-agent
    - Parallelizable aspects → Use multi-agent
    - Token cost: 15x for multi-agent

    Returns:
        Dict with: complexity_level, recommend_multi_agent, subagent_count
    """

    # Keywords indicating complexity
    complexity_keywords = [
        "comprehensive", "detailed", "in-depth", "analysis", "comparison",
        "vs", "versus", "framework", "architecture", "best practices"
    ]

    # Decision logic
    if has_comparison or (has_complexity_keywords and word_count > 5):
        return {
            "complexity_level": "high",
            "recommend_multi_agent": True,
            "subagent_count": 5,
            "reason": "Comparison or complex analysis detected"
        }
    elif word_count > 3:
        return {
            "complexity_level": "medium",
            "recommend_multi_agent": True,
            "subagent_count": 3,
            "reason": "Multi-faceted query detected"
        }
    else:
        return {
            "complexity_level": "low",
            "recommend_multi_agent": False,
            "subagent_count": 1,
            "reason": "Simple fact-finding query"
        }
```

### Orchestrator-Worker Pattern

```python
"""
Lead Agent (Opus 4.5) 职责:
1. 分析查询复杂度
2. 决定是否使用 multi-agent
3. 部署并行 subagents
4. 综合研究发现
5. 生成最终报告

Subagents (Sonnet 4) 职责:
- academic-researcher: ArXiv 论文搜索
- github-watcher: GitHub 项目分析
- community-listener: 社区讨论监听
- citation-agent: 引用处理
"""
```

---

## Handoff Pattern / Handoff 模式

### Function Return Handoff

```python
# Swarm-style handoff for agent switching

def transfer_to_github_agent():
    return Handoff(target_agent=github_agent, context={"repo": "langgraph"})

# Add to agent's function list
agent.functions.append(transfer_to_github_agent)
```

### Agent-as-Tools Handoff

```python
# OpenAI Agents SDK style

agent = Agent(
    name="triage",
    instructions="You are a triage agent",
    handoffs=[academic_agent, github_agent, community_agent]
)
```

### Context Filter Handoff

```python
# Filter context passed to target agent

handoff(
    target_agent=github_agent,
    input_filter=custom_filter,  # Reduce token overhead
    context={"query": current_query}
)
```

### Bidirectional Handoff

```python
# Both agents link to each other

academic_agent.handoffs.append(github_agent)
github_agent.handoffs.append(academic_agent)
```

---

## Code Patterns / 代码模式

### Pattern 1: State Persistence

```python
# Save state for resumability
state = ResearchState(query="Multi-agent timeout mechanisms")
state_json = state.to_json()

# Save to file
with open(f"{state.session_id}_state.json", "w") as f:
    f.write(state_json)

# Load from checkpoint
restored_state = ResearchState.from_json(state_json)
```

### Pattern 2: Parallel Agent Execution

```python
# Execute subagents in parallel (90% speed improvement)

async def _parallel_execute(self, query, state):
    """
    In actual Claude Code implementation, this would use Task tool:

    Task(subagent_type="academic-researcher", prompt="...")
    Task(subagent_type="github-watcher", prompt="...")
    Task(subagent_type="community-listener", prompt="...")
    """

    results = await asyncio.gather(
        run_academic_research(query),
        run_github_analysis(query),
        run_community_listening(query)
    )

    return results
```

### Pattern 3: Agent Instructions Template

```python
# Lead agent instructions
LEAD_INSTRUCTIONS = """
You are the lead researcher coordinating a multi-agent study.

RESPONSIBILITIES:
1. Analyze the research query and develop strategy
2. Determine if multi-agent approach is needed (45% threshold rule)
3. Delegate to specialized subagents in parallel
4. Synthesize findings from all subagents
5. Produce final report with clickable citations

DECISION FRAMEWORK:
- Single-agent success rate < 45%? → Use multi-agent
- Task has parallelizable aspects? → Use multi-agent
- Token budget: 15x normal, but 90.2% performance gain
"""
```

---

## CLI Usage / 命令行使用

```bash
python "tools\research_orchestrator.py" --query "Multi-agent frameworks"
python "tools\research_orchestrator.py" --dry-run --query "..."
python "tools\research_orchestrator.py" --output-dir "research_output"
```

**Commands**:
- `--query`: 研究查询 (必需)
- `--dry-run`: 仅分析不执行
- `--output-dir`: 输出目录 (默认 research_output)
- `--max-subagents`: 最大子代理数 (默认 5)

---

## Integration Points / 集成点

**Reading Agents**:
- `framework-selector`: 使用编排模式知识
- `deep-research-report-writer`: 使用状态管理模式
- `literature-review-writer`: 使用研究发现结构

**CLI Invocations**:
```bash
# 分析查询复杂度
python "tools\research_orchestrator.py" --dry-run --query "{query}"
```

**Related Knowledge Base**:
- `.claude/knowledge/framework_selection.md`: 框架选择决策
- `.claude/knowledge/resilience_patterns.md`: 弹性和恢复模式

---

## Research Subagent Specifications / 研究子代理规范

### academic-researcher

**Tools**:
- `mcp__arxiv-mcp-server__search_papers`
- `mcp__arxiv-mcp-server__download_paper`
- `mcp__arxiv-mcp-server__read_paper`
- `mcp__web-search-prime__webSearchPrime`

**Output Format**:
```json
{
    "arxiv_id": "2402.01680",
    "title": "Paper Title",
    "abstract": "Complete abstract (200-500 words)",
    "url_markdown": "[arXiv:ID](URL) | [PDF](PDF_URL)",
    "methodology": {
        "datasets": "...",
        "baselines": "...",
        "models_tested": "...",
        "evaluation_metrics": "..."
    },
    "quantitative_results": {
        "benchmarks": "...",
        "comparisons": "...",
        "statistical_significance": "..."
    },
    "limitations": ["..."],
    "future_work": ["..."],
    "implementation": {
        "code_url": "...",
        "datasets_available": true,
        "reproducibility_score": "high"
    },
    "summary": "Deep analysis (500-1000 words)"
}
```

### github-watcher

**Tools**:
- `mcp__zread__get_repo_structure`
- `mcp__zread__read_file`
- `mcp__zread__search_doc`
- `mcp__web-search-prime__webSearchPrime`

**Output Format**:
```json
{
    "name": "langchain-ai/langgraph",
    "url_markdown": "[langchain-ai/langgraph](URL) ⭐ 15k+",
    "stars_display": "⭐ 15,000+",
    "description": "...",
    "last_commit_date": "2026-01-15",
    "key_files": [
        {"path": "src/langgraph/graph.py", "description": "Core graph implementation"}
    ],
    "architecture_description": "Detailed analysis (200-500 words)",
    "integration_examples": "...",
    "performance_benchmarks": {...},
    "license": "MIT"
}
```

### community-listener

**Tools**:
- `mcp__web-reader__webReader`
- `mcp__web-search-prime__webSearchPrime`
- `Grep`, `Glob`

**Output Format**:
```json
{
    "platform": "reddit",
    "url_markdown": "[Discussion Title](URL)",
    "title": "Discussion title",
    "original_title": "Original English if non-English",
    "key_quotes": [
        {"user": "username", "quote": "...", "upvotes": 100}
    ],
    "consensus_level": "high",
    "summary": "Discussion summary (200-400 words)",
    "related_discussions": ["url1", "url2"]
}
```

---

## Notes / 说明

- **45% Threshold Rule**: 单 agent 成功率 < 45% 时使用 multi-agent
- **15x Token Cost**: Multi-agent 成本是单 agent 的 15 倍
- **90.2% Performance Gain**: 复杂查询性能提升
- **Parallel Execution**: 子代理并行执行，90% 速度提升
- **State Persistence**: 使用 ResearchState 实现检查点恢复
