# Reflection Protocol v1.0

标准化反思流程 - 让 Agent 从错误中学习，形成可沉淀的经验。

---

## Overview

| 触发条件 | 执行者 | 输入 | 输出 |
|---------|--------|------|------|
| Critic 评估返回 REVISE/REJECT | Subagent | Rewind Ticket | 反思报告 + 修复产出 |
| Subagent 自检发现问题 | Subagent | 自检结果 | 反思报告 |
| Director 要求重做 | Subagent | Director 指令 | 反思报告 |

---

## Core Principle

**LLM 自我评估存在严重幻觉** - 它几乎总是认为自己"做得很好"。

本协议的目标是：
1. **强制溯源**: 找出错误发生的具体过程
2. **分类归因**: 确定错误类型，匹配处理策略
3. **沉淀经验**: 生成可复用的学习笔记
4. **闭环修复**: 确保问题被真正解决

---

## Error Classification System / 错误分类体系

| 错误类型 | 代码 | 识别特征 | 根因 | 处理动作 |
|---------|------|---------|------|---------|
| **模型能力不足** | 3.3.1 | 反复犯同一类低级错误 | 模型本身能力边界 | 写入 anti-pattern，降低期望 |
| **思路/决策错误** | 3.3.2 | 方向性偏差 | System prompt 不明确 | 修改 system prompt |
| **Pipeline 崩溃** | 3.3.3 | 整个流程中断 | Phase 编排问题 | 修改 Phase 编排 |
| **缺少对应知识** | 3.3.4 | Agent 明确表示"不知道" | 知识库缺失 | 触发网络搜索/Consultation |
| **正常迭代尝试** | 3.3.5 | 先简单后复杂的尝试 | 探索性工作 | 记录尝试过程，无需修复 |

### Classification Decision Tree

```
是否完成任务？
├─ NO: 是否因流程中断？
│   ├─ YES → 3.3.3 Pipeline 崩溃
│   └─ NO: 是否明确表示"不知道"？
│       ├─ YES → 3.3.4 缺少对应知识
│       └─ NO: 是否反复犯同类错误？
│           ├─ YES → 3.3.1 模型能力不足
│           └─ NO → 3.3.2 思路/决策错误
└─ YES: 但质量不达标 → 3.3.5 正常迭代尝试
```

---

## Error Trace Report Format / 错误溯源报告格式

当 Subagent 需要反思时，必须产出以下结构：

```json
{
  "reflection_id": "ref_001",
  "timestamp": "2025-02-20T14:30:22.123456",
  "agent": "academic-researcher",
  "trigger": "critic_evaluation",
  "rewind_ticket_id": "rewind_20250220_143022",

  "error_analysis": {
    "surface_issue": "仅收集了 3 篇论文",
    "occurrence_process": [
      "1. 使用了过于狭窄的搜索词",
      "2. 仅搜索了 cs.AI 分类",
      "3. 在收集到 3 篇后过早停止"
    ],
    "root_cause": "搜索策略过于保守，没有充分利用时间预算"
  },

  "error_classification": {
    "type": "3.3.2",
    "description": "决策错误：过早停止搜索",
    "remediation": "修改 system prompt，强调必须满足最小要求"
  },

  "repair_actions": [
    {
      "action": "扩展搜索词",
      "status": "pending",
      "expected_outcome": "获取更多候选论文"
    },
    {
      "action": "增加搜索分类",
      "status": "pending",
      "expected_outcome": "覆盖 cs.LG, cs.CL 等相关领域"
    }
  ],

  "learning_notes": "未来执行时，应在早期检查数量是否达标，避免后期时间不足",

  "anti_pattern": {
    "pattern_name": "过早停止搜索",
    "symptoms": ["在未达标时停止", "搜索词过窄"],
    "prevention": "在搜索开始时设置明确的数量目标，并在过程中检查"
  }
}
```

---

## Reflection Workflow / 反思流程

### Step 1: Explore - 查看当前状态

```python
def explore_current_state():
    """查看当前工作目录和已有产出"""
    steps = [
        "1. 列出 research_data/ 目录下的文件",
        "2. 检查最近的输出文件",
        "3. 查看 checkpoint 文件（如果存在）",
        "4. 确认 Rewind Ticket 内容"
    ]
    return steps
```

**输出**: 当前状态快照

### Step 2: Reflect - 对照目标分析偏差

```python
def reflect_on_deviation(problem, task, output):
    """对照问题 + 任务，分析偏差原因"""
    analysis = {
        "original_problem": problem,
        "assigned_task": task,
        "actual_output": output,
        "gap_analysis": {
            "expected": "5+ papers with 3 key papers",
            "actual": "3 papers with 2 key papers",
            "gap": "2 papers missing, 1 key paper missing"
        },
        "questions": [
            "Q1: 搜索词是否足够广泛？",
            "Q2: 是否充分利用了时间预算？",
            "Q3: 是否在过程中检查过数量？"
        ]
    }
    return analysis
```

**输出**: 偏差分析报告

### Step 3: Classify - 确定错误类型

```python
def classify_error(analysis):
    """根据分析结果确定错误类型"""
    # Use classification decision tree
    if analysis.get("process_interrupted"):
        return "3.3.3"

    if analysis.get("explicit_unknown"):
        return "3.3.4"

    if analysis.get("repeated_mistake"):
        return "3.3.1"

    # Default to decision error
    return "3.3.2"
```

**输出**: 错误类型代码和描述

### Step 4: Plan - 制定修复计划

```python
def create_repair_plan(rewind_ticket, error_type):
    """制定修复计划"""
    plan = {
        "repair_steps": [],
        "resources_needed": [],
        "estimated_effort": "medium"
    }

    for issue in rewind_ticket.get("issues", []):
        if issue["category"] == "completeness":
            plan["repair_steps"].extend([
                "1. 扩展搜索词范围",
                "2. 增加目标分类",
                "3. 降低筛选阈值"
            ])
        elif issue["category"] == "correctness":
            plan["repair_steps"].extend([
                "1. 验证数据源",
                "2. 修正格式错误"
            ])

    return plan
```

**输出**: 可执行的修复计划

### Step 5: Execute - 执行修复

```python
def execute_repair(repair_plan, agent_type):
    """执行修复"""
    results = []

    for step in repair_plan["repair_steps"]:
        # Execute each repair step
        result = execute_step(step)
        results.append({
            "step": step,
            "status": "completed" if result.success else "failed",
            "output": result.output
        })

    return {
        "repair_results": results,
        "all_completed": all(r["status"] == "completed" for r in results)
    }
```

**输出**: 修复执行结果

### Step 6: Submit - 提交修订产出

```python
def submit_revised_output(reflection_report, revised_output):
    """提交修订产出"""
    submission = {
        "reflection_report": reflection_report,
        "revised_output_file": f"research_data/{agent_type}_researcher_output_v2.json",
        "timestamp": datetime.now().isoformat(),
        "ready_for_re_evaluation": True
    }

    # Save reflection report
    save_json(f"research_data/reflection_{reflection_report['reflection_id']}.json", reflection_report)

    # Save revised output
    save_json(submission["revised_output_file"], revised_output)

    return submission
```

**输出**: 提交确认

---

## Implementation Code / 实现代码

### Trigger Reflection

```python
def trigger_reflection(agent_type, rewind_ticket):
    """触发反思流程"""
    prompt = f"""
    REFLECTION REQUIRED

    REWIND TICKET: {rewind_ticket['ticket_id']}
    VERDICT: {rewind_ticket['verdict']}
    QUALITY SCORE: {rewind_ticket['quality_score']}

    ISSUES IDENTIFIED:
    {json.dumps(rewind_ticket['issues'], indent=2)}

    REPAIR PLAN:
    {chr(10).join(rewind_ticket['repair_plan'])}

    请执行反思协议:
    1. Explore - 查看当前产出状态
    2. Reflect - 分析偏差原因
    3. Classify - 确定错误类型（3.3.1-3.3.5）
    4. Plan - 制定修复计划
    5. Execute - 执行修复
    6. Submit - 提交反思报告 + 修订产出

    OUTPUT FILES:
    - research_data/reflection_{rewind_ticket['ticket_id']}.json
    - research_data/{agent_type}_researcher_output_v2.json
    """

    return Task(
        subagent_type=agent_type,
        prompt=prompt,
        context={"rewind_ticket": rewind_ticket}
    )
```

### Handle Reflection Result

```python
def handle_reflection_result(agent_type, reflection_report, revised_output):
    """处理反思结果"""
    # Verify revised output meets requirements
    from tools.checkpoint_manager import check_minimum_requirements

    is_complete, remaining = check_minimum_requirements(
        f"research_data/{agent_type}_researcher_output_v2.json",
        agent_type
    )

    if is_complete:
        # Ready for re-evaluation
        return {
            "status": "ready_for_re_evaluation",
            "reflection_report": reflection_report,
            "revised_output": revised_output
        }
    else:
        # Still not meeting requirements
        return {
            "status": "needs_another_iteration",
            "remaining_issues": remaining
        }
```

---

## Error Type Handling / 错误类型处理

### Type 3.3.1: Model Capability Insufficient

**识别特征**:
- 反复犯同一类低级错误
- 即使有明确指引仍然出错
- 错误模式一致

**处理策略**:
```python
handle_331_capability():
    1. 记录 anti-pattern 到知识库
    2. 降低对该任务的期望
    3. 考虑使用更强的模型
    4. 增加人工检查点
```

### Type 3.3.2: Decision/Reasoning Error

**识别特征**:
- 方向性偏差（如过早停止）
- 没有充分利用资源
- 优先级判断错误

**处理策略**:
```python
handle_332_decision():
    1. 修改 system prompt，增加明确指令
    2. 添加中间检查点
    3. 重新执行任务
    4. 验证修复效果
```

### Type 3.3.3: Pipeline Crash

**识别特征**:
- 整个流程中断
- 某个 Phase 未执行
- 依赖关系断裂

**处理策略**:
```python
handle_333_pipeline():
    1. 检查 Phase 编排逻辑
    2. 修复依赖关系
    3. 从断点恢复执行
    4. 验证流程完整性
```

### Type 3.3.4: Missing Knowledge

**识别特征**:
- Agent 明确表示"不知道"
- 搜索结果为空
- 知识库无相关内容

**处理策略**:
```python
handle_334_knowledge():
    1. 触发网络搜索
    2. 调用 Consultation 机制（如可用）
    3. 更新知识库
    4. 重新执行任务
```

### Type 3.3.5: Normal Iteration

**识别特征**:
- 先尝试简单方法
- 逐步增加复杂度
- 最终达成目标或接近目标

**处理策略**:
```python
handle_335_iteration():
    1. 记录尝试过程
    2. 无需修复（正常探索）
    3. 可选：优化下次起点
```

---

## Quality Checklist / 质量检查

### Reflection Report Quality

- [ ] 包含 reflection_id
- [ ] 包含 timestamp
- [ ] 包含 agent 标识
- [ ] 包含 trigger 类型
- [ ] 包含 rewind_ticket_id（如适用）
- [ ] error_analysis 有具体描述
- [ ] error_classification 有正确的类型代码
- [ ] repair_actions 有具体步骤
- [ ] learning_notes 有可沉淀的经验
- [ ] 可选：包含 anti_pattern

### Revised Output Quality

- [ ] 满足最小产出要求
- [ ] 修复了 Rewind Ticket 中的所有问题
- [ ] 数据格式正确
- [ ] 文件命名正确（_v2 后缀）

---

## 结构化反思 Action（工具调用失败时触发）

### 核心价值

当 MCP 工具调用失败时，自动诊断并生成结构化修复方案，而非盲目重试。

```
传统做法: 工具失败 → 盲目重试 → 再次失败 → 放弃
结构化反思: 工具失败 → 诊断错误类型 → 生成修正方案 → 精准重试
```

### 触发条件

- 任何 MCP 工具调用返回错误
- 连续 2 次相同调用失败

### 执行流程

#### Step 1: 暂停执行，进入 `<reflect>` 阶段

```python
def trigger_tool_reflection(failed_tool, error_message, params):
    """
    工具调用失败时触发结构化反思

    Args:
        failed_tool: 失败的工具名称
        error_message: 错误信息
        params: 导致失败的参数
    """
    # 暂停当前执行
    pause_execution()

    # 进入反思阶段
    return {
        "stage": "tool_reflection",
        "failed_tool": failed_tool,
        "error_message": error_message,
        "params": params
    }
```

#### Step 2: 输出结构化诊断

```json
{
  "reflection_type": "tool_failure",
  "timestamp": "2026-02-21T10:45:00Z",
  "failed_tool": "mcp__arxiv-mcp-server__search_papers",
  "failed_params": {
    "query": "multi-agent orchestration",
    "categories": ["cs.AI"]
  },
  "error_message": "Timeout after 30s",
  "error_type": "external_service_exception",
  "diagnosis": {
    "error_type": "参数错误|工具选择错误|权限不足|外部服务异常",
    "root_cause": "arXiv API 响应超时，可能是网络问题或查询过于复杂",
    "severity": "medium"
  },
  "corrective_action": {
    "action": "重试策略",
    "modified_params": {
      "query": "multi-agent",  // 简化查询
      "max_results": 10        // 减少结果数量
    },
    "fallback_tool": null,     // 或指定替代工具
    "retry_delay_seconds": 5
  }
}
```

#### Step 3: 执行修正后的调用

```python
def execute_corrective_action(diagnosis):
    """执行修正后的调用"""
    action = diagnosis["corrective_action"]

    if action["fallback_tool"]:
        # 使用替代工具
        return invoke_tool(
            action["fallback_tool"],
            action.get("modified_params", {})
        )
    else:
        # 延迟后重试
        time.sleep(action.get("retry_delay_seconds", 3))
        return invoke_tool(
            diagnosis["failed_tool"],
            action["modified_params"]
        )
```

#### Step 4: 记录"失败-修复"对

将经验写入知识库：

```json
{
  "pattern_id": "tool_fail_001",
  "tool": "mcp__arxiv-mcp-server__search_papers",
  "error_type": "external_service_exception",
  "symptoms": ["Timeout", "无响应"],
  "successful_fix": "简化查询词，减少 max_results",
  "timestamp": "2026-02-21T10:45:30Z"
}
```

### 错误类型处理

| error_type | 诊断方向 | 处理方式 |
|------------|---------|---------|
| `参数错误` | 检查参数格式、类型、范围 | 修正参数格式后重试 |
| `工具选择错误` | 检查是否有更合适的工具 | 切换到替代工具 |
| `权限不足` | 检查 API key、访问权限 | 向 Director 汇报，请求授权 |
| `外部服务异常` | 检查网络、服务状态 | 添加重试延迟，或跳过该源 |

### 常见工具失败场景

#### 场景 1: arXiv 搜索超时

```json
{
  "failed_tool": "mcp__arxiv-mcp-server__search_papers",
  "error_type": "external_service_exception",
  "corrective_action": {
    "action": "简化查询并重试",
    "modified_params": {
      "query": "simplified_query",
      "max_results": 5
    },
    "retry_delay_seconds": 5
  }
}
```

#### 场景 2: GitHub 读取 Rate Limit

```json
{
  "failed_tool": "mcp__zread__read_file",
  "error_type": "external_service_exception",
  "error_message": "Rate limit exceeded",
  "corrective_action": {
    "action": "延迟重试",
    "retry_delay_seconds": 60,
    "alternative": "使用 search_doc 替代 read_file"
  }
}
```

#### 场景 3: Web Reader 403 Forbidden

```json
{
  "failed_tool": "mcp__web-reader__webReader",
  "error_type": "权限不足",
  "error_message": "403 Forbidden",
  "corrective_action": {
    "action": "跳过该 URL",
    "fallback": "记录 URL 为不可访问，继续处理其他源"
  }
}
```

#### 场景 4: 参数格式错误

```json
{
  "failed_tool": "mcp__arxiv-mcp-server__search_papers",
  "error_type": "参数错误",
  "error_message": "Invalid query syntax",
  "corrective_action": {
    "action": "修正查询语法",
    "modified_params": {
      "query": "multi-agent OR agent coordination",  // 使用正确的 OR 语法
      "categories": ["cs.AI"]
    }
  }
}
```

### 工具失败处理速查表

| 工具 | 常见失败 | 诊断方向 | 修正方案 |
|------|---------|---------|---------|
| `mcp__arxiv-mcp-server__search_papers` | 超时、无结果 | 检查查询语法、分类选择 | 简化查询、减少 max_results |
| `mcp__arxiv-mcp-server__download_paper` | 下载失败 | 检查网络、尝试其他镜像 | 延迟重试、使用 abstract |
| `mcp__zread__*` | Rate limit | 检查调用频率 | 添加延迟、使用缓存 |
| `mcp__web-reader__webReader` | 403/超时 | 检查 URL 有效性 | 跳过不可访问的 URL |

### 与 Subagent 的集成

在 Subagent 的工具调用代码中添加结构化反思：

```python
def safe_tool_call(tool_name, params, max_retries=2):
    """带结构化反思的安全工具调用"""
    for attempt in range(max_retries):
        try:
            result = invoke_tool(tool_name, params)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                # 最后一次尝试失败，记录并跳过
                log_tool_failure(tool_name, str(e), params)
                return None

            # 触发结构化反思
            diagnosis = trigger_tool_reflection(tool_name, str(e), params)

            # 输出诊断信息
            print(f"""
┌─────────────────────────────────────────────────────┐
│  ⚠️  TOOL REFLECTION                                │
├─────────────────────────────────────────────────────┤
│  Tool: {tool_name:<40} │
│  Error: {diagnosis['error_type']:<38} │
│  Action: {diagnosis['corrective_action']['action']:<36} │
└─────────────────────────────────────────────────────┘
""")

            # 执行修正
            params = diagnosis['corrective_action'].get('modified_params', params)
            time.sleep(diagnosis['corrective_action'].get('retry_delay_seconds', 3))
```

### 质量检查

结构化反思 Action 质量检查：
- [ ] 包含 failed_tool 名称
- [ ] 包含 failed_params
- [ ] 正确分类 error_type
- [ ] 提供具体的 corrective_action
- [ ] 记录到 knowledge/reflections/

---

## Integration with CLAUDE.md

在 Phase 1.2 Critic Evaluation 之后添加：

```python
# After Critic Evaluation
for agent_type, eval_result in critic_evaluations.items():
    verdict = eval_result.get("verdict")

    if verdict == "PASS":
        continue  # Continue to Phase 1.5

    elif verdict == "REVISE":
        # Trigger Reflection Protocol
        reflection_task = trigger_reflection(agent_type, eval_result["rewind_ticket"])

        # Wait for reflection to complete
        reflection_result = await reflection_task

        # Handle reflection result
        handle_reflection_result(agent_type, reflection_result)

        # Re-run Critic Evaluation
        re_eval = Task(
            subagent_type="critic-evaluator",
            prompt=f"Re-evaluate {agent_type} after reflection"
        )

    elif verdict == "REJECT":
        # Director decision required
        log_decision(f"Critic REJECT for {agent_type}: {eval_result.get('reason')}")
```

---

## Example Scenarios / 示例场景

### Scenario 1: Insufficient Papers (3.3.2)

**触发**: academic-researcher 仅收集了 3 篇论文

**Rewind Ticket**:
```json
{
  "ticket_id": "rewind_001",
  "verdict": "REVISE",
  "issues": [
    {
      "category": "completeness",
      "severity": "high",
      "description": "仅收集了 3 篇论文，需要至少 5 篇"
    }
  ]
}
```

**反思报告**:
```json
{
  "reflection_id": "ref_001",
  "error_analysis": {
    "surface_issue": "仅收集了 3 篇论文",
    "occurrence_process": [
      "1. 搜索词过于狭窄",
      "2. 仅搜索了 cs.AI 分类",
      "3. 在收集到 3 篇后过早停止"
    ],
    "root_cause": "搜索策略过于保守"
  },
  "error_classification": {
    "type": "3.3.2",
    "description": "决策错误：过早停止搜索"
  },
  "repair_actions": [
    {"action": "扩展搜索词", "status": "completed"},
    {"action": "增加搜索分类", "status": "completed"}
  ],
  "learning_notes": "应在搜索开始时设置明确的数量目标"
}
```

### Scenario 2: Repeated Mistakes (3.3.1)

**触发**: community-listener 多次未能识别共识点

**Anti-Pattern 记录**:
```json
{
  "pattern_name": "共识点识别不足",
  "symptoms": [
    "只收集讨论，不提炼共识",
    "缺少跨帖子的模式识别"
  ],
  "prevention": "明确要求在每 5 个帖子后提炼一次共识点",
  "error_type": "3.3.1"
}
```

---

## Output Files / 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 反思报告 | `research_data/reflection_{ticket_id}.json` | 反思分析报告 |
| 修订产出 | `research_data/{agent}_researcher_output_v2.json` | 修复后的产出 |
| Anti-Pattern | `knowledge/anti_patterns/{pattern_name}.md` | 沉淀的反模式 |

---

## CHANGELOG

### v1.1 (2026-02-21)

**New Feature: 结构化反思 Action**
- ✅ 工具调用失败时自动诊断
- ✅ 4 种错误类型分类（参数错误、工具选择错误、权限不足、外部服务异常）
- ✅ 结构化诊断输出格式
- ✅ 修正方案生成和执行
- ✅ "失败-修复"对记录机制
- ✅ 工具失败处理速查表
- ✅ 与 Subagent 的集成代码

### v1.0 (2025-02-20)

**Initial Release**:
- ✅ 5 种错误类型分类（3.3.1 - 3.3.5）
- ✅ 错误溯源报告格式
- ✅ 6 步反思流程（Explore → Reflect → Classify → Plan → Execute → Submit）
- ✅ 与 Critic Evaluator 的集成
- ✅ Anti-Pattern 沉淀机制
- ✅ Learning Notes 格式
