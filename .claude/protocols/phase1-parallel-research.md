# Phase 1: Parallel Research Execution

并行研究执行协议 - 部署 3 个研究子代理并同时运行。

---

## Overview

| Subagent | Tools | Output File | Focus |
|----------|-------|-------------|-------|
| `academic-researcher` | arxiv, web-search | `academic_researcher_output.json` | 学术论文 |
| `github-watcher` | zread, web-search | `github_researcher_output.json` | 开源项目 |
| `community-listener` | web-reader, web-search | `community_researcher_output.json` | 社区讨论 |

---

## Deployment Code

```python
# Calculate max_turns based on time allocation
from tools.checkpoint_manager import calculate_max_turns, generate_time_budget_string

max_turns_per_agent = calculate_max_turns(
    per_agent_timeout_seconds=time_allocation['per_agent_timeout_seconds'],
    seconds_per_turn=120
)

time_budget_str = generate_time_budget_string(time_allocation)

# Deploy in parallel (single message with 3 Task calls)
Task(
    subagent_type="academic-researcher",
    prompt=f"""...existing prompt...
{time_budget_str}
""",
    max_turns=max_turns_per_agent
)

Task(
    subagent_type="github-watcher",
    prompt=f"""...existing prompt...
{time_budget_str}
""",
    max_turns=max_turns_per_agent
)

Task(
    subagent_type="community-listener",
    prompt=f"""...existing prompt...
{time_budget_str}
""",
    max_turns=max_turns_per_agent
)
```

---

## Progress Display

```
┌─────────────────────────────────────────┐
│  ⏱️  PHASE 1 PROGRESS                │
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

## Completion Check (Phase 1.1)

每个 subagent 完成后检查是否满足最小要求：

```python
from tools.checkpoint_manager import check_minimum_requirements, should_continue_agent

subagents = [
    ("academic-researcher", "research_data/academic_researcher_output.json"),
    ("github-watcher", "research_data/github_researcher_output.json"),
    ("community-listener", "research_data/community_researcher_output.json")
]

for agent_type, output_file in subagents:
    is_complete, remaining = check_minimum_requirements(output_file, agent_type)

    if not is_complete:
        should_continue, remaining_seconds, status = should_continue_agent(time_allocation)
        if status == "continue":
            # Relaunch with continuation prompt
            Task(subagent_type=agent_type, prompt=continuation_prompt, max_turns=new_max_turns)
```

---

## Minimum Requirements

| Agent | Requirement | Field |
|--------|-------------|-------|
| `academic-researcher` | 5 papers analyzed | `papers_analyzed` |
| `github-watcher` | 8 projects analyzed | `projects_analyzed` |
| `community-listener` | 15 threads analyzed | `threads_analyzed` |
