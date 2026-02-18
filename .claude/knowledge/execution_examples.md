# Execution Examples / 执行示例代码

本文档包含从 CLAUDE.md 提取的完整 Python 示例代码，供编排器参考实现。

---

## NEW: Timeout Protection (v9.5) / 超时保护

**CRITICAL**: These functions are now implemented in `tools/checkpoint_manager.py`.

### Safe max_turns Calculation

```python
from tools.checkpoint_manager import calculate_max_turns

# With safety buffer (80% of theoretical)
max_turns = calculate_max_turns(
    per_agent_timeout_seconds=2880,  # 48 minutes
    seconds_per_turn=120,
    safety_buffer=0.8
)
# Result: 19 turns (not 24)
```

### Subagent Timeout Check

```python
from tools.checkpoint_manager import check_subagent_timeout, should_execute_tool

# Check at every checkpoint
timeout_check = check_subagent_timeout(
    start_time_iso="2026-02-18T10:00:00Z",
    timeout_seconds=2880,
    checkpoint_interval_seconds=300
)

print(timeout_check["message"])

if timeout_check["should_save_and_exit"]:
    # Save checkpoint immediately and exit
    checkpoint_manager.write_checkpoint(phase="emergency", ...)
    return  # Exit

# Before tool execution
should_exec, reason = should_execute_tool(timeout_check, "download_paper", 60)
if not should_exec:
    print(f"Skipping: {reason}")
else:
    paper = download_paper(arxiv_id)
```

### Continuation Signal Detection

```python
from tools.checkpoint_manager import check_continuation_needed, write_continuation_signal

# Orchestrator: Check if continuation needed
result = check_continuation_needed(
    output_file="research_data/academic_researcher_output.json",
    agent_type="academic-researcher"
)

if result["needs_continuation"]:
    print(f"Continuation needed: {result['reason']}")
    print(f"From checkpoint: {result['checkpoint_file']}")
    # Relaunch agent with continuation prompt

# Subagent: Write continuation signal when interrupted
write_continuation_signal(
    output_file="research_data/academic_researcher_output.json",
    agent_type="academic-researcher",
    reason="max_turns_reached",
    remaining_requirements={"papers_analyzed": {"current": 3, "required": 5}},
    checkpoint_manager=checkpoint_manager
)
```

### Heartbeat Monitoring

```python
from tools.heartbeat_monitor import HeartbeatMonitor

monitor = HeartbeatMonitor()

# Subagent: Write heartbeat periodically
monitor.write_heartbeat(
    agent_type="academic-researcher",
    status="running",  # or "accelerate", "saving", "complete", "error"
    items_processed=5,
    start_time_iso="2026-02-18T10:00:00Z",
    budget_seconds=2880
)

# Orchestrator: Check for stuck agents
stuck = monitor.find_stuck_agents(timeout_seconds=300)
for agent in stuck:
    print(f"STUCK: {agent['agent_type']} - age: {agent['age_formatted']}")

# List all heartbeats
heartbeats = monitor.list_heartbeats()
```

---

## User Intent Detection / 用户意图检测 {#user-intent-detection}

```python
def detect_user_intent(user_query: str) -> dict:
    """
    检测用户意图和期望的输出格式

    Returns:
        intent: {
            "output_formats": ["blog_post", "summary"],
            "research_depth": "standard" | "deep" | "quick",
            "target_audience": "general" | "technical" | "academic",
            "task_type": str or None
        }
    """
    import re

    query_lower = user_query.lower()

    intent = {
        "output_formats": [],
        "research_depth": "standard",
        "target_audience": "general",
        "task_type": None
    }

    # 检测输出格式关键词
    format_keywords = {
        "blog_post": ["博客", "blog", "article", "写一篇", "文章"],
        "slide_deck": ["幻灯片", "slide", "ppt", "presentation", "演示", "slides"],
        "code_examples": ["代码", "code", "示例", "tutorial", "怎么用", "example"],
        "summary": ["摘要", "summary", "总结", "简短", "概要"],
        "comparison": ["对比", "comparison", "区别", "vs", "versus", "比较"],
        "proposal": ["提案", "proposal", "建议", "方案"],
        "json_format": ["json", "api", "format"],
    }

    for format_type, keywords in format_keywords.items():
        if any(kw in query_lower for kw in keywords):
            intent["output_formats"].append(format_type)

    # 检测深度需求
    if any(kw in query_lower for kw in ["深入", "详细", "全面", "comprehensive", "deep"]):
        intent["research_depth"] = "deep"
    elif any(kw in query_lower for kw in ["快速", "简单", "简要", "quick", "brief"]):
        intent["research_depth"] = "quick"

    # 检测目标受众
    if any(kw in query_lower for kw in ["学术", "论文", "research", "scholarly"]):
        intent["target_audience"] = "academic"
    elif any(kw in query_lower for kw in ["工程师", "开发", "developer", "engineering"]):
        intent["target_audience"] = "technical"

    # 确定主要任务类型（用于 Phase 2e）
    if intent["output_formats"]:
        intent["task_type"] = intent["output_formats"][0]

    return intent


# 使用示例
user_intent = detect_user_intent(user_query)
if user_intent["output_formats"]:
    print(f"[INTENT DETECTED] User wants: {user_intent['output_formats']}")
    print(f"[INTENT] Research depth: {user_intent['research_depth']}")
    print(f"[INTENT] Auto-trigger Phase 2e: task_handle")
```

---

## Minimum Requirements Check / 最小要求检查

```python
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
```

---

## Time Budget Allocation / 时间预算分配 {#time-budget-allocation}

```python
# Import utility functions from checkpoint_manager
from tools.checkpoint_manager import (
    parse_time_budget,
    calculate_time_allocation,
    calculate_max_turns,
    generate_time_budget_string,
    format_time_confirmation,
    should_continue_agent,
    generate_continuation_prompt,
    TimeBudgetTracker,
    format_phase_checkpoint,
    get_time_assessment_from_allocation
)

# Initialize time allocation
time_allocation = None

# 来源1: 用户明确指定 (优先级最高)
user_time_budget = parse_time_budget(user_query)
if user_time_budget:
    time_allocation = calculate_time_allocation(
        total_budget_seconds=user_time_budget['total_seconds'],
        subagent_count=3,
        coordination_overhead=0.20
    )
    time_allocation['time_source'] = 'user_specified'

# 来源2: performance-predictor估算 (如果没有用户指定)
if not time_allocation:
    performance_time_estimate = performance_result.get("estimated_time_seconds", 1800)
    time_allocation = calculate_time_allocation(
        total_budget_seconds=performance_time_estimate,
        subagent_count=3
    )
    time_allocation['time_source'] = 'performance_predictor'

# Initialize TimeBudgetTracker for automatic re-allocation
time_tracker = TimeBudgetTracker(
    total_budget_seconds=time_allocation['total_budget_seconds'],
    start_time_iso=time_allocation['start_time_iso']
)
```

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

## Subagent Deployment / 子代理部署

```python
# Calculate max_turns based on time allocation
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

# TIME CONFIRM: Display deployment parameters
print(f"""
[TIME CONFIRM - Phase 1: Subagent Deployment]
├─ Max Turns per Agent: {max_turns_per_agent}
├─ Per-Agent Timeout: {time_allocation.get('per_agent_timeout_minutes', 'N/A')} minutes
├─ Subagents to Deploy: 3 (academic-researcher, github-watcher, community-listener)
└─ Time Budget String Generated: {len(time_budget_str)} characters
""")

# 并行部署 3 个 Task
Task(
    subagent_type="academic-researcher",
    prompt=f"""...原有prompt...
{time_budget_str}
""",
    max_turns=max_turns_per_agent
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

---

## Time Confirmation Display / 时间确认显示

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

---

## Time Re-allocation / 时间重分配 {#time-re-allocation}

```python
# ⏱️ AUTOMATIC TIME RE-ALLOCATION - No user confirmation, based on wall-clock
from tools.checkpoint_manager import TimeBudgetTracker, format_phase_checkpoint

# Initialize tracker at session start (before Phase -1)
time_tracker = TimeBudgetTracker(
    total_budget_seconds=time_allocation['total_budget_seconds'],
    start_time_iso=time_allocation['start_time_iso']
)

# Mark completed phases
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
│                                                              │
│  ACTION: Report writers get +{reallocated_minutes}min for quality           │
│  • Deeper analysis and synthesis                            │
│  • Comprehensive citation verification                      │
│  • Enhanced quality validation                              │
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

---

## Task Handle Execution / 任务处理执行

```python
# Phase -0.5 已经检测了用户意图
user_intent = detect_user_intent(original_query)

# Phase 2e: 根据检测到的意图自动执行
if user_intent["output_formats"]:
    # 用户隐含或明确指定了输出格式
    Task(
        subagent_type="task_handle",
        prompt=f"""Complete the following task based on research results:

USER QUERY: {original_query}
DETECTED INTENT: {user_intent}
INPUT_REPORTS:
- research_output/{sanitized_topic}_comprehensive_report.md
- research_output/{sanitized_topic}_literature_review.md

OUTPUT: research_output/{sanitized_topic}_{user_intent['task_type']}.md

Generate output in the detected format: {user_intent['output_formats']}
Target audience: {user_intent['target_audience']}
Research depth: {user_intent['research_depth']}
"""
    )
else:
    # 未检测到特定格式，跳过 task_handle
    print("[Phase 2e] No custom output format detected, skipping task_handle")
```

---

## Checkpoint Resume Format / 检查点续传格式

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

## Orchestration Object Pattern / 编排对象模式

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

## Hard Timeout Protection / 硬性超时保护 (v9.5 - CRITICAL)

**问题**: Subagent 可能因 `max_turns` 设置过大或工具调用卡住而无限执行。

**解决方案**: 添加 wall-clock 超时保护，强制终止超时任务。

### Max Turns 计算公式

```python
def calculate_max_turns_with_buffer(
    per_agent_timeout_seconds: int,
    seconds_per_turn: int = 120,
    safety_buffer: float = 0.8  # 保留 20% 缓冲
) -> int:
    """
    计算 max_turns，带安全缓冲

    KEY: 使用 80% 的理论值，确保有时间保存 checkpoint

    Args:
        per_agent_timeout_seconds: 每个 agent 的超时时间
        seconds_per_turn: 每轮平均时间（默认 2 分钟）
        safety_buffer: 安全缓冲系数（默认 0.8）

    Returns:
        保守的 max_turns 值
    """
    theoretical_turns = per_agent_timeout_seconds // seconds_per_turn
    safe_turns = int(theoretical_turns * safety_buffer)
    return max(5, safe_turns)  # 至少 5 轮


# 示例：48 分钟超时
# theoretical = 2880 / 120 = 24 turns
# safe = 24 * 0.8 = 19 turns (保留 5 轮用于保存和清理)
```

### Subagent 强制超时检测

```python
def check_subagent_timeout(
    start_time_iso: str,
    timeout_seconds: int,
    checkpoint_interval_seconds: int = 300
) -> dict:
    """
    检查 subagent 是否超时（每个 checkpoint 调用）

    Args:
        start_time_iso: 开始时间（ISO 格式）
        timeout_seconds: 超时时间（秒）
        checkpoint_interval_seconds: checkpoint 间隔

    Returns:
        {
            "is_timeout": bool,
            "should_save_and_exit": bool,
            "remaining_seconds": int,
            "action": "continue" | "accelerate" | "save_and_exit"
        }
    """
    from datetime import datetime

    start_time = datetime.fromisoformat(start_time_iso)
    elapsed = (datetime.now() - start_time).total_seconds()
    remaining = timeout_seconds - elapsed

    if remaining <= 0:
        return {
            "is_timeout": True,
            "should_save_and_exit": True,
            "remaining_seconds": 0,
            "action": "save_and_exit",
            "message": "⏰ TIMEOUT: Must save checkpoint and exit immediately"
        }
    elif remaining < checkpoint_interval_seconds:
        return {
            "is_timeout": False,
            "should_save_and_exit": True,
            "remaining_seconds": int(remaining),
            "action": "save_and_exit",
            "message": f"⏰ WARNING: Only {int(remaining)}s left - save checkpoint now"
        }
    elif remaining < 300:  # 5 分钟
        return {
            "is_timeout": False,
            "should_save_and_exit": False,
            "remaining_seconds": int(remaining),
            "action": "accelerate",
            "message": "⚡ ACCELERATE: Enter rapid completion mode"
        }
    else:
        return {
            "is_timeout": False,
            "should_save_and_exit": False,
            "remaining_seconds": int(remaining),
            "action": "continue",
            "message": "✅ On track"
        }
```

### Subagent 执行前超时检查

```python
def should_execute_tool(
    time_check: dict,
    tool_type: str,
    estimated_duration_seconds: int = 60
) -> tuple[bool, str]:
    """
    决定是否执行某个工具调用

    Args:
        time_check: check_subagent_timeout() 的返回值
        tool_type: 工具类型 ("download_paper", "search", "full_analysis", etc.)
        estimated_duration_seconds: 预估耗时

    Returns:
        (should_execute, reason)
    """
    remaining = time_check.get("remaining_seconds", 0)
    action = time_check.get("action", "continue")

    # 超时或即将超时
    if action == "save_and_exit":
        return False, "TIMEOUT: Skip all tools, save checkpoint immediately"

    # 加速模式
    if action == "accelerate":
        if tool_type == "download_paper":
            return False, "ACCELERATE: Skip full-text download, use abstract"
        if tool_type == "full_analysis":
            return False, "ACCELERATE: Skip deep analysis, quick summary only"
        if tool_type in ["citation_chain", "deep_search"]:
            return False, f"ACCELERATE: Skip {tool_type}"

    # 检查是否有足够时间
    if remaining < estimated_duration_seconds * 1.5:  # 需要 1.5x 缓冲
        return False, f"INSUFFICIENT_TIME: Need {estimated_duration_seconds}s, have {remaining}s"

    return True, "OK"
```

### 使用示例

```python
# 在 subagent 中，每个 checkpoint 前调用
time_check = check_subagent_timeout(
    start_time_iso="2026-02-18T10:00:00Z",
    timeout_seconds=2880,  # 48 分钟
    checkpoint_interval_seconds=300
)

print(time_check["message"])

if time_check["should_save_and_exit"]:
    # 立即保存 checkpoint 并退出
    checkpoint_manager.write_checkpoint(
        phase="emergency_save",
        content={"reason": "timeout_protection", "items_processed": items_count}
    )
    print("Checkpoint saved. Exiting to prevent timeout.")
    # 不再执行任何工具调用

# 工具调用前检查
should_exec, reason = should_execute_tool(time_check, "download_paper", estimated_duration_seconds=60)
if not should_exec:
    print(f"Skipping download_paper: {reason}")
    # 使用降级方案：只用 abstract
else:
    # 正常执行
    paper = download_paper(arxiv_id)
```

---

## Auto-Continuation Trigger / 自动续传触发器 (v9.5)

**问题**: Phase 1.1 续传需要编排器手动执行，容易遗漏。

**解决方案**: 在 subagent 输出中添加续传信号。

### Subagent 输出中的续传信号

```python
# Subagent 在完成时写入
output = {
    "subagent_metadata": {
        "agent_type": "academic-researcher",
        "status": "incomplete_timeout",  # 或 "complete"
        "needs_continuation": True,       # 关键信号
        "continuation_reason": "max_turns_reached",
        "remaining_requirements": {
            "papers_analyzed": {"current": 3, "required": 5, "remaining": 2}
        },
        "last_checkpoint": "research_data/checkpoints/academic_002.json"
    },
    "research_findings": {...},
    "items": [...]
}
```

### 编排器自动检测续传

```python
def check_continuation_needed(output_file: str) -> dict:
    """
    检查 subagent 输出是否需要续传

    Returns:
        {
            "needs_continuation": bool,
            "reason": str,
            "remaining_requirements": dict,
            "checkpoint_file": str
        }
    """
    from pathlib import Path
    import json

    path = Path(output_file)
    if not path.exists():
        return {"needs_continuation": False, "reason": "no_output"}

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    metadata = data.get("subagent_metadata", {})

    # 检查续传信号
    needs_continuation = metadata.get("needs_continuation", False)
    status = metadata.get("status", "unknown")

    if needs_continuation or status == "incomplete_timeout":
        return {
            "needs_continuation": True,
            "reason": metadata.get("continuation_reason", "unknown"),
            "remaining_requirements": metadata.get("remaining_requirements", {}),
            "checkpoint_file": metadata.get("last_checkpoint", "")
        }

    # 检查最小要求
    agent_type = metadata.get("agent_type", "")
    is_complete, remaining = check_minimum_requirements(output_file, agent_type)

    if not is_complete:
        return {
            "needs_continuation": True,
            "reason": "minimum_requirements_not_met",
            "remaining_requirements": remaining,
            "checkpoint_file": ""
        }

    return {"needs_continuation": False, "reason": "complete"}
```
