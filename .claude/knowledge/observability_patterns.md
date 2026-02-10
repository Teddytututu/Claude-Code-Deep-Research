# Observability Patterns Knowledge Base

## Overview
从 `observability.py` 提取的可观测性模式核心逻辑

**Purpose**: 提供多智能体系统的可观测性、监控和成本追踪模式

---

## Key Classes / 类

### MetricType

**Purpose**: 指标类型枚举

**Values**:
- `TOKEN_COUNT`: Token 计数
- `LATENCY`: 延迟 (秒)
- `COST`: 成本 (美元)
- `SUCCESS_RATE`: 成功率
- `ERROR_RATE`: 错误率
- `TOOL_CALL_COUNT`: 工具调用计数

### LogLevel

**Purpose**: 日志级别枚举

**Values**:
- `DEBUG`: 调试信息
- `INFO`: 一般信息
- `WARNING`: 警告
- `ERROR`: 错误
- `CRITICAL`: 严重错误

### Metric

**Purpose**: 单个指标数据结构

**Key Attributes**:
- `name`: 指标名称
- `type`: MetricType 枚举值
- `value`: 指标值
- `unit`: 单位 (tokens, seconds, usd, percent, count)
- `timestamp`: ISO 格式时间戳
- `labels`: 标签字典 (agent, session, tool, etc.)

### ObservabilityConfig

**Purpose**: 可观测性配置

**Key Attributes**:
- `enable_logging`: 是否启用日志 (默认 True)
- `log_level`: 日志级别 (默认 INFO)
- `enable_metrics`: 是否启用指标 (默认 True)
- `enable_tracing`: 是否启用追踪 (默认 True)
- `metrics_export_interval`: 指标导出间隔 (默认 60 秒)
- `log_file`: 日志文件路径
- `metrics_file`: 指标文件路径

### ObservabilityManager

**Purpose**: 可观测性管理器主类

**Key Methods**:
- `record_metric(name, value, labels)`: 记录指标
- `log(level, message, context)`: 记录日志
- `start_trace(operation_name)`: 开始追踪
- `end_trace(trace_id)`: 结束追踪
- `get_metrics_summary()`: 获取指标摘要
- `export_metrics(output_file)`: 导出指标

### TracingSpan

**Purpose**: 追踪跨度数据结构

**Key Attributes**:
- `trace_id`: 追踪 ID (UUID)
- `span_id`: 跨度 ID (UUID)
- `parent_span_id`: 父跨度 ID
- `operation_name`: 操作名称
- `start_time`: 开始时间
- `end_time`: 结束时间
- `duration`: 持续时间 (秒)
- `status`: 状态 (success/error)
- `attributes`: 属性字典

---

## Decision Logic / 决策逻辑

### Metric Collection Strategy

```python
def should_collect_metric(metric_name, config):
    """
    指标收集决策

    Criteria:
    1. enable_metrics == True
    2. metric_name in allowed_metrics
    3. Collection overhead < threshold
    """

    if not config.enable_metrics:
        return False, "Metrics disabled"

    allowed_metrics = [
        "token_count", "latency", "cost",
        "success_rate", "tool_call_count"
    ]

    if metric_name not in allowed_metrics:
        return False, f"Metric {metric_name} not allowed"

    return True, "OK"
```

### Log Level Decision

```python
def should_log(level, config, message):
    """
    日志级别决策

    Decision:
        level >= config.log_level → Log message

    Levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
    """

    level_order = {
        LogLevel.DEBUG: 0,
        LogLevel.INFO: 1,
        LogLevel.WARNING: 2,
        LogLevel.ERROR: 3,
        LogLevel.CRITICAL: 4
    }

    return level_order[level] >= level_order[config.log_level]
```

---

## Code Patterns / 代码模式

### Pattern 1: Context Manager for Tracing

```python
@contextmanager
def trace(operation_name, manager):
    """追踪上下文管理器"""

    trace_id = manager.start_trace(operation_name)
    start_time = time.time()

    try:
        yield trace_id
        duration = time.time() - start_time
        manager.end_trace(trace_id, status="success", duration=duration)

    except Exception as e:
        duration = time.time() - start_time
        manager.end_trace(trace_id, status="error", duration=duration)
        manager.log(LogLevel.ERROR, f"Error in {operation_name}: {e}")
        raise

# Usage:
with trace("academic_research", obs_manager):
    # Do work
    papers = search_arxiv(query)
```

### Pattern 2: Metric Recording

```python
def record_agent_metrics(manager, agent_name, tokens, latency, success):
    """记录 agent 指标"""

    manager.record_metric(
        name="token_count",
        value=tokens,
        unit="tokens",
        labels={"agent": agent_name, "operation": "research"}
    )

    manager.record_metric(
        name="latency",
        value=latency,
        unit="seconds",
        labels={"agent": agent_name, "operation": "research"}
    )

    manager.record_metric(
        name="success_rate",
        value=1.0 if success else 0.0,
        unit="percent",
        labels={"agent": agent_name}
    )
```

### Pattern 3: Cost Calculation

```python
def calculate_token_cost(input_tokens, output_tokens, model="claude-sonnet-4"):
    """
    计算 token 成本

    Pricing (示例，实际价格可能变化):
    - Sonnet 4 Input: $3.00 / 1M tokens
    - Sonnet 4 Output: $15.00 / 1M tokens
    """

    PRICING = {
        "claude-sonnet-4": {
            "input": 3.00 / 1_000_000,
            "output": 15.00 / 1_000_000
        },
        "claude-opus-4": {
            "input": 15.00 / 1_000_000,
            "output": 75.00 / 1_000_000
        }
    }

    pricing = PRICING.get(model, PRICING["claude-sonnet-4"])

    input_cost = input_tokens * pricing["input"]
    output_cost = output_tokens * pricing["output"]

    return {
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost
    }
```

---

## CLI Usage / 命令行使用

```bash
python "tools\observability.py" --metrics
python "tools\observability.py" --logs
python "tools\observability.py" --cost-report
python "tools\observability.py" --export observability_data.json
```

**Commands**:
- `--metrics`: 显示指标摘要
- `--logs`: 显示日志
- `--cost-report`: 显示成本报告
- `--export`: 导出可观测性数据

---

## Integration Points / 集成点

**Reading Agents**:
- `mcp-coordinator`: 使用可观测性模式监控 MCP 工具使用

**CLI Invocations**:
```bash
# Get current metrics
python "tools\observability.py" --metrics
```

**Related Knowledge Base**:
- `.claude/knowledge/orchestration_patterns.md`: 编排模式相关
- `.claude/knowledge/resilience_patterns.md`: 弹性模式相关

---

## Metrics to Track / 需要追踪的指标

### Agent-Level Metrics

| Metric | Description | Unit | Labels |
|--------|-------------|------|--------|
| `token_count` | Token 使用量 | tokens | agent, model |
| `latency` | 执行延迟 | seconds | agent, operation |
| `success_rate` | 成功率 | percent | agent |
| `tool_call_count` | 工具调用次数 | count | agent, tool |
| `error_count` | 错误次数 | count | agent, error_type |

### Session-Level Metrics

| Metric | Description | Unit | Labels |
|--------|-------------|------|--------|
| `total_duration` | 总执行时间 | seconds | session_id |
| `total_tokens` | 总 token 使用量 | tokens | session_id |
| `total_cost` | 总成本 | usd | session_id |
| `agent_count` | Agent 数量 | count | session_id |
| `parallel_efficiency` | 并行效率 | percent | session_id |

### MCP-Level Metrics

| Metric | Description | Unit | Labels |
|--------|-------------|------|--------|
| `mcp_tool_calls` | MCP 工具调用次数 | count | mcp_name, tool_name |
| `mcp_latency` | MCP 响应延迟 | seconds | mcp_name |
| `mcp_error_rate` | MCP 错误率 | percent | mcp_name |
| `active_mcp_count` | 活动 MCP 数量 | count | session_id |

---

## Logging Standards / 日志记录规范

### Log Message Format

```json
{
    "timestamp": "2026-02-10T12:34:56Z",
    "level": "INFO",
    "message": "Agent execution completed",
    "context": {
        "agent": "academic-researcher",
        "session_id": "abc-123",
        "duration_seconds": 45.2,
        "token_count": 15000
    }
}
```

### Log Levels Usage

```python
# DEBUG: Detailed diagnostic information
logger.debug("Processing paper {paper_id}, page {page}", paper_id="2402.01680", page=3)

# INFO: General informational messages
logger.info("Starting research for query: {query}", query="Multi-agent frameworks")

# WARNING: Something unexpected but not critical
logger.warning("MCP tool {tool} returned partial results", tool="arxiv-search")

# ERROR: Error occurred but execution can continue
logger.error("Failed to download paper {paper_id}, using fallback", paper_id="2402.01680")

# CRITICAL: Critical failure, execution cannot continue
logger.critical("All MCP servers failed, cannot proceed")
```

---

## Cost Monitoring / 成本监控

### Budget Awareness Pattern

```python
class BudgetAwareExecutor:
    """预算感知执行器"""

    def __init__(self, max_budget_usd):
        self.max_budget = max_budget_usd
        self.spent = 0.0

    def execute(self, agent_func):
        """执行前检查预算"""

        estimated_cost = self.estimate_cost(agent_func)

        if self.spent + estimated_cost > self.max_budget:
            raise BudgetExceededError(
                f"Estimated cost ${estimated_cost:.4f} would exceed "
                f"remaining budget ${self.max_budget - self.spent:.4f}"
            )

        result = agent_func()
        actual_cost = self.calculate_cost(result)

        self.spent += actual_cost
        self.log_cost(actual_cost, self.spent)

        return result

    def estimate_cost(self, agent_func):
        """估算执行成本"""
        # Estimate based on historical data
        return 0.05  # $0.05 estimate
```

---

## Notes / 说明

- **Token Cost Multiplier**: Multi-agent 成本是单 agent 的 15 倍
- **MCP Tool Overhead**: MCP 工具定义占用 token，需监控
- **200k Context Window**: 实际可用可能只剩 70k，需追踪使用情况
- **Daily Executions**: 生产环境可能每天 100,000+ 次执行，需成本控制
- **Performance-Aware**: 基于指标决定是否使用 multi-agent (45% threshold)
