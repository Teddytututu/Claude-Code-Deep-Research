# Time Checkpoint Protocol / 时间检查点协议

> **Purpose**: Shared time-aware checkpointing for all research agents.
> **Usage**: Reference this file via `@knowledge:time_checkpoint_protocol.md`

---

## Time-Aware Checkpointing (时间感知检查点) - CRITICAL

**CRITICAL**: 每次保存checkpoint时，你必须执行时间评估！

### 时间检查点协议

如果收到 `TIME_BUDGET` 配置，你必须在每次checkpoint时：

```python
# 在每次checkpoint时执行
from datetime import datetime

def save_time_aware_checkpoint(checkpoint_manager, start_time_iso, budget_seconds, items_analyzed):
    current_time = datetime.now()
    start_time = datetime.fromisoformat(start_time_iso)
    elapsed_seconds = (current_time - start_time).total_seconds()
    remaining_seconds = budget_seconds - elapsed_seconds
    progress_percentage = (elapsed_seconds / budget_seconds) * 100

    # 时间评估
    time_assessment = {
        "start_time": start_time_iso,
        "current_time": current_time.isoformat(),
        "elapsed_seconds": int(elapsed_seconds),
        "elapsed_formatted": f"{int(elapsed_seconds // 60)} minutes",
        "remaining_seconds": int(remaining_seconds),
        "remaining_formatted": f"{int(remaining_seconds // 60)} minutes",
        "budget_seconds": budget_seconds,
        "budget_formatted": f"{int(budget_seconds // 60)} minutes",
        "progress_percentage": round(progress_percentage, 2),
        "time_status": "on_track" if remaining_seconds > 300 else "time_critical",
        "items_per_minute": round(items_analyzed / (elapsed_seconds / 60), 2) if elapsed_seconds > 0 else 0
    }

    # 保存checkpoint
    checkpoint_manager.write_checkpoint(
        phase=f"checkpoint_{checkpoint_manager.checkpoint_count + 1}",
        content={
            "time_assessment": time_assessment,
            "items_analyzed": items_analyzed,
            "work_summary": "当前工作总结..."
        }
    )

    # 如果时间不足5分钟，触发加速模式
    if remaining_seconds < 300:
        return "ACCELERATE_MODE"
    return "NORMAL_MODE"
```

---

## Accelerate Mode / 加速模式

### 触发条件

当 `remaining_seconds < 300` (5分钟)时进入 **ACCELERATE_MODE**：

- 停止深度分析（跳过详细分析）
- 跳过非关键操作
- 快速总结已有发现
- 立即准备最终输出
- 优先完成最小输出要求

### Time-Aware Tool Timeout

```python
def should_skip_tool(time_assessment, tool_type="general"):
    """
    如果时间不足，跳过耗时操作

    Returns:
        (should_skip, reason, alternative_action)
    """
    remaining = time_assessment.get('remaining_seconds', 0)
    time_status = time_assessment.get('time_status', 'unknown')

    # TIME_CRITICAL: Less than 5 minutes
    if remaining < 300:
        if tool_type == "download_full":
            return True, "TIME_CRITICAL: Skip full-text download", "Use abstract only"
        elif tool_type == "deep_analysis":
            return True, "TIME_CRITICAL: Skip deep analysis", "Quick summary only"
        else:
            return True, f"TIME_CRITICAL: Skip {tool_type}", "Use cached data or skip"

    # WARNING: Less than 25% of budget or less than 10 minutes
    elif remaining < 600 or time_status == "warning":
        if tool_type == "download_full":
            return True, "ACCELERATE: Use abstract only", "Prioritize key items only"
        else:
            return False, "OK", "Proceed normally"

    # ON_TRACK: Proceed normally
    return False, "OK", "Proceed normally"
```

---

## Degradation Strategy Table / 降级策略表

| 剩余时间 | download_full | deep_analysis | search | action |
|---------|--------------|---------------|--------|--------|
| < 300s | ❌ 跳过 | ⚡ 快速摘要 | ✅ 仅搜索 | 立即收尾 |
| 300-600s | ⚡ 仅关键 | ⚡ 中等分析 | ✅ 正常 | 加速模式 |
| > 600s | ✅ 正常 | ✅ 正常 | ✅ 正常 | 正常流程 |

---

## Checkpoint Timing

必须在这些时刻执行时间检查点：

1. 每处理 N 个项目后（N 因 agent 而异）
2. 每次深度分析前
3. 每次工具调用前（使用 should_skip_tool 检查）
4. 每次工具调用后（如果发现消耗时间较长）

### Agent-Specific Checkpoint Intervals

| Agent | Interval | Unit |
|-------|----------|------|
| academic-researcher | 3 | papers |
| github-watcher | 2 | repositories |
| community-listener | 5 | discussions |

---

## Checkpoint Format

每个checkpoint必须包含 `time_assessment` 字段：

```json
{
  "checkpoint_id": "agent_001",
  "timestamp": "2026-02-09T12:00:00Z",
  "items_analyzed": 3,
  "progress_percentage": 20,

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
    "items_per_minute": 0.1
  },

  "status": "in_progress"
}
```

---

## Timeout Configuration

| Agent | Per-Agent Timeout | Checkpoint Interval |
|-------|------------------|---------------------|
| academic-researcher | 2880s (48min) | Every 3 papers |
| github-watcher | 2880s (48min) | Every 2 repos |
| community-listener | 2880s (48min) | Every 5 discussions |
