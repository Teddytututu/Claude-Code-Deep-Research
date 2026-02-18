# Resilience Patterns Knowledge Base

## Overview
从 `resilience.py` 提取的弹性模式核心逻辑

**Purpose**: 提供多智能体系统的弹性设计和恢复模式

---

## Key Classes / 类

### RetryPolicy

**Purpose**: 重试策略配置

**Key Attributes**:
- `max_attempts`: 最大重试次数 (默认 3)
- `base_delay`: 基础延迟 (秒，默认 1.0)
- `max_delay`: 最大延迟 (秒，默认 60.0)
- `backoff_multiplier`: 退避乘数 (默认 2.0)
- `jitter_enabled`: 是否启用抖动 (默认 True)

**Methods**:
- `get_delay(attempt)`: 获取第 N 次重试的延迟时间
- `should_retry(attempt)`: 判断是否应该继续重试

### CircuitBreaker

**Purpose**: 熔断器模式实现

**Key Attributes**:
- `failure_threshold`: 失败阈值 (默认 5)
- `success_threshold`: 成功阈值 (默认 2)
- `timeout`: 超时时间 (秒，默认 60.0)
- `half_open_timeout`: 半开状态超时 (默认 30.0)
- `state`: 当前状态 (CLOSED/OPEN/HALF_OPEN)

**Methods**:
- `call(func, *args, **kwargs)`: 通过熔断器调用函数
- `reset()`: 重置熔断器状态
- `get_state()`: 获取当前状态

### CircuitState

**Purpose**: 熔断器状态枚举

**Values**:
- `CLOSED`: 正常状态，允许请求通过
- `OPEN`: 熔断状态，拒绝请求
- `HALF_OPEN`: 半开状态，允许少量请求测试

### CheckpointRecovery

**Purpose**: 检查点恢复模式

**Key Attributes**:
- `checkpoint_interval`: 检查点间隔 (秒，默认 30)
- `checkpoint_dir`: 检查点目录 (默认 checkpoints/)
- `max_checkpoints`: 最大检查点数量 (默认 10)

**Methods**:
- `save_checkpoint(state)`: 保存检查点
- `load_checkpoint(session_id)`: 加载检查点
- `cleanup_old_checkpoints()`: 清理旧检查点

### ResilienceManager

**Purpose**: 弹性管理器主类

**Key Methods**:
- `execute_with_retry(func, policy)`: 带重试执行
- `execute_with_circuit_breaker(func, breaker)`: 通过熔断器执行
- `execute_with_checkpoint(func, session_id)`: 带检查点执行

---

## Decision Logic / 决策逻辑

### Retry Decision

```python
def should_retry(attempt, max_attempts, last_error):
    """
    重试决策逻辑

    Conditions:
    1. attempt < max_attempts: 可以重试
    2. last_error is retryable: 特定错误可重试

    Retryable Errors:
    - ConnectionError
    - TimeoutError
    - RateLimitError (HTTP 429)
    - ServerError (HTTP 5xx)

    Non-Retryable Errors:
    - AuthenticationError (HTTP 401)
    - PermissionError (HTTP 403)
    - ValidationError (HTTP 422)
    """

    if attempt >= max_attempts:
        return False, "Max attempts reached"

    # Check if error is retryable
    if isinstance(last_error, (ConnectionError, TimeoutError)):
        return True, "Network error, retrying"

    if isinstance(last_error, RateLimitError):
        return True, "Rate limited, retrying with backoff"

    return False, f"Non-retryable error: {type(last_error)}"
```

### Circuit Breaker State Transitions

```python
"""
熔断器状态转换逻辑:

CLOSED (正常)
    ├── failures >= threshold → OPEN (熔断)
    └── successes reset counter

OPEN (熔断)
    ├── timeout elapsed → HALF_OPEN (尝试恢复)
    └── all requests rejected immediately

HALF_OPEN (尝试恢复)
    ├── success >= success_threshold → CLOSED (恢复正常)
    └── failure occurs → OPEN (重新熔断)
"""

def transition_state(current_state, success, failure_count, success_count):
    if current_state == CircuitState.CLOSED:
        if failure_count >= FAILURE_THRESHOLD:
            return CircuitState.OPEN
        return CircuitState.CLOSED

    elif current_state == CircuitState.OPEN:
        # Time-based transition handled separately
        return CircuitState.OPEN

    elif current_state == CircuitState.HALF_OPEN:
        if success_count >= SUCCESS_THRESHOLD:
            return CircuitState.CLOSED
        if failure_count > 0:
            return CircuitState.OPEN
        return CircuitState.HALF_OPEN
```

### Checkpoint Decision

```python
def should_save_checkpoint(elapsed_time, checkpoint_interval):
    """
    检查点保存决策

    Decision:
        elapsed_time >= checkpoint_interval → Save checkpoint

    Strategy:
    - Time-based: 定期保存
    - Event-based: 关键事件后保存
    - Size-based: 数据量达到阈值后保存
    """

    return elapsed_time >= checkpoint_interval
```

---

## Code Patterns / 代码模式

### Pattern 1: Exponential Backoff with Jitter

```python
def calculate_delay_with_jitter(attempt, base_delay, max_delay, multiplier):
    """
    计算带抖动的指数退避延迟

    Formula:
        delay = min(base_delay * (multiplier ** attempt), max_delay)
        jittered_delay = delay * (0.5 + random() * 0.5)

    Purpose: 避免 thundering herd 问题
    """

    # Exponential backoff
    delay = min(base_delay * (multiplier ** attempt), max_delay)

    # Add jitter (±50%)
    jittered_delay = delay * (0.5 + random.random() * 0.5)

    return jittered_delay
```

### Pattern 2: Circuit Breaker Protection

```python
@dataclass
class CircuitBreaker:
    """熔断器保护模式"""

    def call(self, func, *args, **kwargs):
        """通过熔断器调用函数"""

        # Check state
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        # Execute function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self):
        """检查是否应该尝试重置"""
        return time.time() - self.last_failure_time >= self.half_open_timeout
```

### Pattern 3: Checkpoint Recovery

```python
def execute_with_checkpoint(func, session_id, checkpoint_interval):
    """
    带检查点的执行模式

    Strategy:
    1. Load existing checkpoint if available
    2. Execute from checkpoint position
    3. Save checkpoint periodically
    4. Clean up old checkpoints
    """

    # Try to load checkpoint
    checkpoint = load_checkpoint(session_id)
    if checkpoint:
        state = checkpoint.state
        start_position = checkpoint.position
    else:
        state = initialize_state()
        start_position = 0

    # Execute with periodic checkpointing
    last_checkpoint_time = time.time()

    for position in range(start_position, total_items):
        result = func(state, position)

        # Check if we should save checkpoint
        elapsed = time.time() - last_checkpoint_time
        if elapsed >= checkpoint_interval:
            save_checkpoint(session_id, state, position)
            last_checkpoint_time = time.time()

    return result
```

---

## CLI Usage / 命令行使用

```bash
python "tools\resilience.py" --test-retry
python "tools\resilience.py" --test-circuit-breaker
python "tools\resilience.py" --checkpoint-stats
```

**Commands**:
- `--test-retry`: 测试重试机制
- `--test-circuit-breaker`: 测试熔断器
- `--checkpoint-stats`: 显示检查点统计

---

## Integration Points / 集成点

**Reading Agents**:
- `timeout-specialist`: 使用弹性模式处理超时和恢复

**CLI Invocations**:
```bash
# Test resilience patterns
python "tools\resilience.py" --test-all
```

**Related Knowledge Base**:
- `.claude/knowledge/orchestration_patterns.md`: 编排模式相关
- `.claude/knowledge/observability_patterns.md`: 可观测性相关

---

## Resilience Anti-Patterns / 弹性反模式

### ❌ Anti-Pattern 1: Fixed Delay Retry

```python
# BAD: Fixed delay can cause thundering herd
for i in range(max_retries):
    try:
        return func()
    except:
        time.sleep(1)  # Fixed delay
```

### ✅ Pattern 1: Exponential Backoff with Jitter

```python
# GOOD: Exponential backoff with jitter
delay = base_delay * (2 ** attempt) + random_jitter()
time.sleep(delay)
```

### ❌ Anti-Pattern 2: No Circuit Breaker

```python
# BAD: No protection against cascading failures
for _ in range(100):
    result = failing_service.call()  # Will hammer the service
```

### ✅ Pattern 2: Circuit Breaker Protection

```python
# GOOD: Circuit breaker prevents cascading failures
breaker = CircuitBreaker(threshold=5, timeout=60)
result = breaker.call(failing_service)
```

### ❌ Anti-Pattern 3: No Checkpointing

```python
# BAD: Long-running process with no recovery
def long_process():
    for item in million_items:
        process(item)  # If fails at 50%, must restart from 0%
```

### ✅ Pattern 3: Periodic Checkpointing

```python
# GOOD: Can resume from last checkpoint
def long_process():
    state = load_checkpoint() or initialize()
    for item in state.remaining_items:
        process(item)
        if should_checkpoint():
            save_checkpoint(state)
```

---

## Timeout Integration / 超时集成

### Orchestration Object Pattern + Checkpointing

```python
class OrchestrationObject:
    """
    结合超时机制和检查点恢复的编排对象模式

    Use case: Workflows exceeding per-agent timeout limits
    """

    def __init__(self):
        self.state = {}
        self.checkpoint_dir = "checkpoints/"
        self.checkpoint_interval = 30  # seconds

    def execute_agent(self, agent_name, agent_func):
        """执行单个 agent，带检查点"""

        checkpoint_file = f"{self.checkpoint_dir}/{agent_name}.json"

        # Try to load existing checkpoint
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file) as f:
                checkpoint = json.load(f)
            if checkpoint["status"] == "complete":
                return checkpoint["result"]

        # Execute agent
        result = agent_func(self.state)

        # Save checkpoint
        with open(checkpoint_file, "w") as f:
            json.dump({
                "status": "complete",
                "result": result,
                "timestamp": datetime.now().isoformat()
            }, f)

        self.state[agent_name] = result
        return result
```

---

## Notes / 说明

- **Retry with Jitter**: 避免 thundering herd 问题
- **Circuit Breaker**: 防止级联故障
- **Checkpoint Recovery**: 长运行流程必备
- **Orchestration Object**: 结合超时和恢复模式
- **Palantir Finding**: 90% 超时失败率源于无恢复机制

---

## Subagent Timeout Protection / Subagent 超时保护 (v9.5 - CRITICAL)

### Problem Diagnosis / 问题诊断

| 症状 | 根因 | 检查方法 |
|------|------|---------|
| Subagent 无限卡住 | `max_turns` 过大或未生效 | 检查 Task 的 max_turns 参数 |
| 工具调用超时 | 单次调用无超时限制 | 检查 MCP 服务器超时配置 |
| 续传未触发 | Phase 1.1 未执行或信号丢失 | 检查 output JSON 的 `needs_continuation` |
| Checkpoint 未保存 | Subagent 被强制中断 | 检查 checkpoint 目录是否有文件 |

### Solution 1: Conservative max_turns Calculation

```python
# 推荐：使用 80% 理论值作为安全边界
def safe_max_turns(timeout_minutes: int, min_turns: int = 5) -> int:
    """
    计算安全的 max_turns 值

    Rule of thumb:
    - 每轮平均 2 分钟
    - 保留 20% 缓冲用于保存和清理
    """
    theoretical_turns = (timeout_minutes * 60) // 120
    return max(min_turns, int(theoretical_turns * 0.8))

# 示例：
# 48 分钟 → theoretical = 24 → safe = 19
# 30 分钟 → theoretical = 15 → safe = 12
# 15 分钟 → theoretical = 7.5 → safe = 6
```

### Solution 2: Wall-Clock Timeout Guard

```python
import signal
from datetime import datetime
from contextlib import contextmanager

class TimeoutError(Exception):
    pass

@contextmanager
def wall_clock_timeout(seconds: int, agent_name: str = "unknown"):
    """
    Wall-clock 超时保护（使用 signal 或 threading）

    Usage:
        with wall_clock_timeout(2880, "academic-researcher"):
            # 执行研究任务
            ...
    """
    start_time = datetime.now()

    def check_timeout():
        elapsed = (datetime.now() - start_time).total_seconds()
        if elapsed > seconds:
            raise TimeoutError(f"Agent {agent_name} exceeded {seconds}s timeout")

    # 简化实现：返回检查函数供手动调用
    yield check_timeout
```

### Solution 3: Graceful Degradation Protocol

```python
TIMEOUT_DEGRADATION_PROTOCOL = """
当检测到时间不足时，执行以下降级策略：

| 剩余时间 | 阶段 | 操作 |
|---------|------|------|
| > 10 min | NORMAL | 正常执行，深度分析 |
| 5-10 min | ACCELERATE | 跳过全文下载，只用摘要；跳过深层引用链 |
| 2-5 min | RAPID | 快速保存当前状态，最小化输出 |
| < 2 min | EMERGENCY | 立即保存 checkpoint 并退出 |

关键：在 EMERGENCY 阶段，不再执行任何工具调用！
"""
```

### Solution 4: Heartbeat Monitoring

```python
def write_heartbeat(agent_type: str, status: str, items_processed: int):
    """
    写入心跳文件，供编排器监控

    文件位置: research_data/heartbeat/{agent_type}.json
    """
    from datetime import datetime
    from pathlib import Path
    import json

    heartbeat_dir = Path("research_data/heartbeat")
    heartbeat_dir.mkdir(parents=True, exist_ok=True)

    heartbeat = {
        "agent_type": agent_type,
        "status": status,  # "running", "accelerate", "saving", "complete"
        "items_processed": items_processed,
        "timestamp": datetime.now().isoformat()
    }

    with open(heartbeat_dir / f"{agent_type}.json", 'w') as f:
        json.dump(heartbeat, f, indent=2)
```

### Solution 5: MCP Tool Timeout Configuration

```python
# 推荐的 MCP 工具超时配置
MCP_TIMEOUT_CONFIG = {
    # ArXiv MCP
    "arxiv_search": 30,       # 搜索论文
    "arxiv_download": 120,    # 下载全文（可能较慢）
    "arxiv_read": 60,         # 读取论文

    # Web Search
    "web_search": 20,         # 网页搜索

    # Web Reader
    "web_reader": 45,         # 读取网页

    # GitHub
    "github_read": 30,        # 读取 GitHub 文件
    "github_search": 20,      # 搜索 GitHub

    # Default
    "default": 30
}
```

---

## Quick Fix Checklist / 快速修复清单

当系统卡住时，检查以下项目：

1. **max_turns 是否合理**
   ```python
   # 检查：应该使用 80% 理论值
   max_turns = calculate_max_turns_with_buffer(per_agent_timeout_seconds)
   ```

2. **Checkpoint 是否在写入**
   ```bash
   # 检查 checkpoint 目录
   ls -la research_data/checkpoints/
   ```

3. **心跳是否在更新**
   ```bash
   # 检查心跳文件
   cat research_data/heartbeat/academic-researcher.json
   ```

4. **续传信号是否正确**
   ```python
   # 检查 output JSON
   import json
   with open("research_data/academic_researcher_output.json") as f:
       data = json.load(f)
   print(data["subagent_metadata"].get("needs_continuation"))
   ```

5. **MCP 工具是否响应**
   - 检查 MCP 服务器日志
   - 尝试单独调用工具测试
