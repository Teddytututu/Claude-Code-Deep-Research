# Phase Protocols / Phase 执行协议

本文档包含所有 Phase 的完整执行代码实现。

---

## Phase -1: Performance Prediction / 性能预测 {#phase--1}

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

---

## Phase 0: Framework Selection / 框架选择 {#phase-0}

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

---

## Phase 0.5: MCP Coordination / MCP 协调

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

---

## Phase 0.75: Production Readiness / 生产就绪度

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

## Phase 1: Research Subagent Deployment / 研究子代理部署 {#phase-1}

```python
# Calculate max_turns based on time allocation
max_turns_per_agent = None
time_budget_str = ""

if time_allocation:
    max_turns_per_agent = calculate_max_turns(
        per_agent_timeout_seconds=time_allocation.get("per_agent_timeout_seconds", 0),
        seconds_per_turn=120
    )
    time_budget_str = generate_time_budget_string(time_allocation)

# 并行部署（在一个 Claude 消息中）
# IMPORTANT: Pass max_turns parameter to enforce time limits
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

**Subagent Task Specification**: 每个 Subagent 必须收到:
1. **Objective**: 明确的研究目标
2. **Output Format**: 期望的输出格式（包含详细的 JSON 字段要求）
3. **Tool Guidance**: 哪些工具优先使用
4. **Source Guidance**: 哪些信息源最相关
5. **Task Boundaries**: 什么在范围内，什么不在
6. **Quality Requirements**: 最小产出标准和质量检查清单
7. **Time Budget Constraints** (当 time_allocation 存在时)

**Critical**: `max_turns` 参数直接传递给 Task 工具，强制限制子智能体的执行轮次。

---

## Phase 1.1: Subagent Completion Check & Continuation / 完成检查与续传 {#phase-11}

```python
# 等待所有 subagents 完成
academic_result = wait_for_task(academic_task)
github_result = wait_for_task(github_task)
community_result = wait_for_task(community_task)

# TIME CONFIRM: Check elapsed time after subagent completion
if time_allocation:
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
        checkpoint_dir = Path("research_data/checkpoints")
        checkpoints = sorted(checkpoint_dir.glob(f"{agent_type.replace('-', '_')}_*.json"))

        if checkpoints:
            latest_checkpoint = checkpoints[-1]

            if time_allocation:
                should_continue, remaining_seconds, status = should_continue_agent(time_allocation)

                if status == "continue":
                    new_max_turns = calculate_max_turns(remaining_seconds, seconds_per_turn=120)

                    continuation_prompt = generate_continuation_prompt(
                        agent_type=agent_type,
                        output_file=output_file,
                        remaining_requirements=remaining,
                        remaining_seconds=remaining_seconds
                    )

                    continuation_prompt += f"\n\nLATEST CHECKPOINT: {latest_checkpoint}"

                    # 重新启动 agent
                    Task(
                        subagent_type=agent_type,
                        prompt=continuation_prompt,
                        max_turns=new_max_turns
                    )

                    # 等待 relaunch 完成并再次检查
                    relaunch_complete, relaunch_remaining = check_minimum_requirements(output_file, agent_type)

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

                        Task(
                            subagent_type=agent_type,
                            prompt=final_prompt,
                            max_turns=final_max_turns
                        )

                elif status == "insufficient_time":
                    print(f"[TIME CONFIRM] INSUFFICIENT TIME for {agent_type} - accepting incomplete")

        else:
            print(f"[CLAUDE.md] No checkpoint found for {agent_type}, cannot continue")
```

**Minimum Requirements by Agent Type**:

| Agent Type | Minimum Papers/Projects | Minimum Key Items |
|------------|------------------------|-------------------|
| `academic-researcher` | 5 papers analyzed | 3 key papers |
| `github-watcher` | 8 projects analyzed | 4 key projects |
| `community-listener` | 15 threads analyzed | 3 consensus points |

**Acceleration Mode Protocol**:
1. **Skip full-text downloads** — 使用 abstract 和 summary
2. **Limit citation chains** — 只追踪直接引用，不递归
3. **Reduce tool calls** — 批量处理而非逐个查询
4. **Simplify output** — 跳过详细分析，保留核心发现

---

## Phase 1.5: Cross-Domain Tracking / 跨域关系追踪

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

## Phase 2a: Logic Analysis / 逻辑分析

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

---

## Phase 2b: Dual Report Synthesis / 双报告合成

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

INPUT DATA:
- Academic research: research_data/academic_research_output.json
- GitHub research: research_data/github_research_output.json
- Community research: research_data/community_research_output.json

TOPIC: {original_query}

OUTPUT: research_output/{sanitized_topic}_comprehensive_report.md

See .claude/agents/deep-research-report-writer.md for complete specification."""
)

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

## Phase 2d: Link Validation / 链接验证

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

---

## Phase 3: Report Delivery / 报告交付

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

**Deliver to user**:
- Comprehensive report: {topic}_comprehensive_report.md
- Literature review: {topic}_literature_review.md
- Link validation summary (if issues found)
- Custom task output (if task_handle was used)
- Summary of key findings from both reports
