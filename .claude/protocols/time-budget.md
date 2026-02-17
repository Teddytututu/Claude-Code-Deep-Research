# Time Budget Management Protocol

时间预算管理协议 - 用于管理深度研究系统的时间分配和超时控制。

---

## 核心原则

1. **Parallel Execution**: Agents run in parallel, each gets FULL available time
2. **Automatic Re-allocation**: Saved time automatically transferred to final phases
3. **Wall-Clock Based**: Decisions based on actual elapsed time, not agent-reported

---

## Time Calculation Formula

```
Per-Agent Time = Total Budget × 80%  # Coordination overhead: 20%
```

**关键**: 每个 agent 获得全部可用时间（不是除以 3！）

### Example

```
用户: "深度研究 [topic]，给我1小时"
→ Total Budget: 60 分钟
→ Per-Agent Timeout: 48 分钟 (60 × 80%)
→ Checkpoint Interval: 6 分钟
→ 你实际等待: ~60 分钟 (agents 并行运行)
```

---

## Checkpoint Format

每个 checkpoint 必须包含 `time_assessment` 字段：

```json
{
  "checkpoint_id": "academic_001",
  "timestamp": "2026-02-09T12:00:00Z",
  "items_processed": 3,

  "time_assessment": {
    "start_time": "2026-02-09T11:30:00Z",
    "current_time": "2026-02-09T12:00:00Z",
    "elapsed_seconds": 1800,
    "elapsed_formatted": "30 minutes",
    "remaining_seconds": 2700,
    "remaining_formatted": "45 minutes",
    "budget_seconds": 4500,
    "budget_formatted": "75 minutes",
    "progress_percentage": 40.0,
    "time_status": "on_track",
    "papers_per_minute": 0.1
  }
}
```

---

## Time Status Values

| Status | Threshold | 行为 |
|--------|----------|------|
| `on_track` | remaining > 25% | 正常执行 |
| `warning` | remaining < 25% | 考虑加速 |
| `time_critical` | remaining < 300s | 进入 ACCELERATE_MODE |
| `overtime` | remaining < 0 | 立即终止 |

---

## ACCELERATE_MODE Actions

当 `remaining_seconds < 300` (5分钟) 时：

1. **Skip full-text downloads** — 使用 abstract only
2. **Limit citation chains** — 只追踪直接引用
3. **Reduce tool calls** — 批量处理
4. **Simplify output** — 最小分析

---

## Utility Functions

```python
# From tools/checkpoint_manager.py
from tools.checkpoint_manager import (
    parse_time_budget,
    calculate_time_allocation,
    calculate_max_turns,
    generate_time_budget_string,
    format_time_confirmation,
    should_continue_agent,
    get_time_assessment_from_allocation
)
```

---

## 相关文件

- `tools/checkpoint_manager.py` - 实现
- `CLAUDE.md` - Phase 0.85, Phase 1.1
- `.claude/agents/*/md` - Agent-specific timeout protocols
