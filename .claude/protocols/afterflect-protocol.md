# AfterFlect Protocol v1.0

AfterFlect = After-execution Reflection (事后反思)

补全反思闭环：验证 PreFlect 预判的准确性，提炼成功模式。

---

## Core Principle

```
PreFlect (事前): 预测风险 → 制定预防措施
AfterFlect (事后): 验证预测 → 提炼经验教训
```

**关键洞察**: 仅有事前反思是不够的，需要事后验证才能形成完整的 learning loop。

---

## Trigger Conditions / 触发条件

| 触发时机 | 执行者 | 必要条件 |
|---------|--------|---------|
| Subagent 任务完成且 Critic 评估通过后 | Subagent | 任务成功完成 |
| 整个研究任务 Phase 完成后 | LeadResearcher | 可选，汇总所有 Subagent 的 AfterFlect |

---

## Execution Flow / 执行流程

### Step 1: 回顾 PreFlect 预测

```python
def review_preflect_predictions(preflect_output, actual_results):
    """
    对比事前预测与实际结果

    Args:
        preflect_output: PreFlect 阶段的输出
        actual_results: 实际执行的结果

    Returns:
        预测准确性分析
    """
    analysis = {
        "predicted_risks_occurred": [],      # 预测且发生的风险
        "predicted_risks_avoided": [],       # 预测但未发生的风险（预防成功）
        "unexpected_issues": [],             # 未预测到的问题
        "effective_preventions": []          # 有效的预防措施
    }

    for risk in preflect_output.get("plan_risks", []):
        if risk["risk"] in actual_results.get("issues_encountered", []):
            analysis["predicted_risks_occurred"].append(risk)
        else:
            analysis["predicted_risks_avoided"].append(risk)
            # 检查预防措施是否有效
            mitigation = preflect_output.get("mitigation_plan", {}).get(risk["risk"])
            if mitigation:
                analysis["effective_preventions"].append({
                    "risk": risk["risk"],
                    "prevention": mitigation
                })

    # 找出未预测到的问题
    for issue in actual_results.get("issues_encountered", []):
        if issue not in [r["risk"] for r in preflect_output.get("plan_risks", [])]:
            analysis["unexpected_issues"].append(issue)

    return analysis
```

### Step 2: 成功因素分析

输出以下结构：

```json
{
  "success_factors": [
    {
      "factor": "多分类并行搜索",
      "description": "同时搜索 cs.AI + cs.LG + cs.CL 获得了更全面的覆盖",
      "impact": "high",
      "reusable": true
    },
    {
      "factor": "中期检查点",
      "description": "每 3 篇论文检查数量，避免了过早停止",
      "impact": "medium",
      "reusable": true
    }
  ],
  "key_decisions": [
    {
      "decision": "使用 OR 组合搜索词",
      "rationale": "单一关键词覆盖不足",
      "outcome": "候选论文数量增加 3 倍"
    }
  ]
}
```

### Step 3: 提炼经验

```json
{
  "learned_patterns": [
    {
      "pattern_name": "多分类并行搜索",
      "description": "对于跨领域主题，同时搜索多个分类",
      "task_type": "academic-research",
      "effectiveness": "high",
      "when_to_use": "主题涉及 AI + ML + NLP 等多个领域时"
    }
  ],
  "effective_preventions": [
    {
      "prevention": "设置中期检查点",
      "prevented_risk": "过早停止",
      "evidence": "检查点发现数量不足，及时调整策略"
    }
  ],
  "unexpected_issues": [
    {
      "issue": "arXiv API 超时",
      "solution": "简化查询，减少 max_results",
      "future_prevention": "在 PreFlect 中增加网络超时风险评估"
    }
  ]
}
```

### Step 4: 计算预测准确率

```python
def calculate_prediction_accuracy(preflect_output, actual_results):
    """
    计算 PreFlect 预测准确率

    Returns:
        accuracy_metrics: 预测准确性指标
    """
    predicted_risks = [r["risk"] for r in preflect_output.get("plan_risks", [])]
    actual_issues = actual_results.get("issues_encountered", [])

    # 计算指标
    true_positives = len([r for r in predicted_risks if r in actual_issues])
    false_positives = len([r for r in predicted_risks if r not in actual_issues])
    false_negatives = len([i for i in actual_issues if i not in predicted_risks])

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    return {
        "precision": round(precision, 2),  # 预测的风险中实际发生的比例
        "recall": round(recall, 2),        # 实际问题中被预测到的比例
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }
```

### Step 5: 自动更新知识库（强制执行）

**重要**: AfterFlect 完成后，必须执行以下更新：

#### 5.1 识别新知识

```python
def identify_new_knowledge(afterflect_output):
    """
    从 AfterFlect 输出中识别需要更新的知识
    """
    new_knowledge = {
        "patterns_to_add": [],
        "risks_to_add": []
    }

    # 筛选高效果模式（effectiveness >= "medium"）
    for pattern in afterflect_output.get("learned_patterns", []):
        if pattern.get("effectiveness") in ["high", "medium"]:
            new_knowledge["patterns_to_add"].append(pattern)

    # 提取可预防的风险
    for issue in afterflect_output.get("unexpected_issues", []):
        if issue.get("future_prevention"):
            new_knowledge["risks_to_add"].append(issue)

    return new_knowledge
```

#### 5.2 更新 learned-patterns.md

```
执行步骤:
1. 使用 Read 工具读取 .claude/knowledge/reflections/learned-patterns.md
2. 识别适当的部分（学术论文/GitHub/社区/通用）
3. 使用 Edit 工具追加新模式
4. 格式遵循现有模板：

#### {模式名称}
\```
适用条件: {when_to_use}
执行方法: {description}
预期效果: {expected_outcome}
效果: {effectiveness}
发现时间: {timestamp}
\```
```

#### 5.3 更新 summary.md

```
执行步骤:
1. 使用 Read 工具读取 .claude/knowledge/reflections/summary.md
2. 识别适当的任务类型部分
3. 使用 Edit 工具追加新风险到前瞻风险清单表格
4. 如果有典型场景，添加到场景列表
```

#### 5.4 验证更新

```
更新完成后：
1. 再次读取文件确认更新成功
2. 记录更新日志：
   - 更新时间
   - 更新内容摘要
   - 来源 agent_type
```

#### 5.5 原有函数保留

```python
def update_knowledge_base(afterflect_output):
    """
    将 AfterFlect 结果更新到知识库（原有函数）
    """
    # 1. 更新成功模式库
    for pattern in afterflect_output.get("learned_patterns", []):
        append_to_learned_patterns(pattern)

    # 2. 更新历史失败模式摘要（如果有新的意外问题）
    for issue in afterflect_output.get("unexpected_issues", []):
        update_failure_patterns(issue)

    # 3. 记录有效的预防措施
    for prevention in afterflect_output.get("effective_preventions", []):
        record_effective_prevention(prevention)
```

---

## AfterFlect Output Template / 输出模板

```json
{
  "afterflect_id": "af_20260221_120000",
  "timestamp": "2026-02-21T12:00:00Z",
  "agent_type": "academic-researcher",
  "preflect_id": "pf_20260221_100000",
  "task_summary": "收集 multi-agent orchestration 论文",

  "prediction_review": {
    "predicted_risks_occurred": ["搜索词过窄"],
    "predicted_risks_avoided": ["过早停止"],
    "unexpected_issues": ["arXiv API 超时"]
  },

  "prediction_accuracy": {
    "precision": 0.5,
    "recall": 0.33,
    "true_positives": 1,
    "false_positives": 1,
    "false_negatives": 2
  },

  "success_factors": [
    {
      "factor": "多分类并行搜索",
      "impact": "high",
      "reusable": true
    }
  ],

  "learned_patterns": [
    {
      "pattern_name": "多分类并行搜索",
      "effectiveness": "high",
      "when_to_use": "跨领域主题"
    }
  ],

  "effective_preventions": [
    {
      "prevention": "设置中期检查点",
      "prevented_risk": "过早停止"
    }
  ],

  "recommendations_for_next_time": [
    "在 PreFlect 中增加网络超时风险评估",
    "考虑使用备用数据源"
  ]
}
```

---

## Integration with Subagents / 与 Subagent 集成

每个研究 Subagent 在任务完成后，执行 AfterFlect：

```markdown
## EXECUTION PROTOCOL

...

### Step 8: AfterFlect 事后反思（任务完成后执行）

**触发条件**: 任务完成且输出文件已保存

1. **回顾 PreFlect 预测**
   - 加载本次任务的 PreFlect 输出
   - 对比预测与实际结果

2. **输出 AfterFlect 报告**
   - prediction_review: 预测回顾
   - prediction_accuracy: 准确率评估
   - success_factors: 成功因素
   - learned_patterns: 可复用模式

3. **更新知识库**
   - 如果发现新模式 → 更新 learned-patterns.md
   - 如果发现新风险 → 更新 summary.md
```

---

## Example Output / 示例输出

### academic-researcher AfterFlect

```
┌─────────────────────────────────────────────────────┐
│  🔍 AFTERFLECT: Academic Research                   │
├─────────────────────────────────────────────────────┤
│  Task: 收集 multi-agent orchestration 论文          │
│  PreFlect ID: pf_20260221_100000                    │
│                                                     │
│  Prediction Accuracy:                               │
│  ├─ Precision: 50% (1/2 预测发生)                   │
│  └─ Recall: 33% (1/3 问题被预测)                    │
│                                                     │
│  What Went Well:                                    │
│  ✅ 多分类并行搜索 - 覆盖更全面                      │
│  ✅ 中期检查点 - 避免过早停止                        │
│                                                     │
│  Unexpected Issues:                                 │
│  ⚠️  arXiv API 超时 - 通过简化查询解决               │
│                                                     │
│  Learned Patterns:                                  │
│  📌 多分类并行搜索 (effectiveness: high)            │
│                                                     │
│  Recommendations for Next Time:                     │
│  💡 增加网络超时风险评估                             │
└─────────────────────────────────────────────────────┘
```

### github-watcher AfterFlect

```
┌─────────────────────────────────────────────────────┐
│  🔍 AFTERFLECT: GitHub Watcher                      │
├─────────────────────────────────────────────────────┤
│  Task: 调研 multi-agent 框架开源实现                │
│  PreFlect ID: pf_20260221_100100                    │
│                                                     │
│  Prediction Accuracy:                               │
│  ├─ Precision: 67% (2/3 预测发生)                   │
│  └─ Recall: 50% (2/4 问题被预测)                    │
│                                                     │
│  What Went Well:                                    │
│  ✅ 论文→代码关联 - 找到了官方实现                   │
│  ✅ Stars 渐进筛选 - 平衡了数量和质量                │
│                                                     │
│  Unexpected Issues:                                 │
│  ⚠️  部分 repo 无 README - 通过代码结构分析          │
│  ⚠️  GitHub Rate Limit - 添加延迟解决                │
│                                                     │
│  Learned Patterns:                                  │
│  📌 论文→代码关联 (effectiveness: high)             │
│  📌 Stars 渐进筛选 (effectiveness: medium)          │
└─────────────────────────────────────────────────────┘
```

### community-listener AfterFlect

```
┌─────────────────────────────────────────────────────┐
│  🔍 AFTERFLECT: Community Listener                  │
├─────────────────────────────────────────────────────┤
│  Task: 收集 multi-agent 社区讨论和实践反馈          │
│  PreFlect ID: pf_20260221_100200                    │
│                                                     │
│  Prediction Accuracy:                               │
│  ├─ Precision: 100% (2/2 预测发生)                  │
│  └─ Recall: 67% (2/3 问题被预测)                    │
│                                                     │
│  What Went Well:                                    │
│  ✅ 批量共识提取 - 避免只收集不分析                  │
│  ✅ 跨平台对比 - 发现了东西方观点差异                │
│                                                     │
│  Unexpected Issues:                                 │
│  ⚠️  部分知乎帖子需登录 - 跳过处理                   │
│                                                     │
│  Learned Patterns:                                  │
│  📌 批量共识提取 (effectiveness: high)              │
│  📌 跨平台对比 (effectiveness: high)                │
│                                                     │
│  Key Consensus Points Found:                        │
│  💬 "AutoGen快、CrewAI稳、LangGraph强"              │
└─────────────────────────────────────────────────────┘
```

---

## Knowledge Base Updates / 知识库更新

### 更新 learned-patterns.md

当发现高效果的模式时，添加到成功模式库：

```markdown
## 论文搜索类成功模式

| 模式 | 描述 | 适用场景 | 效果 |
|------|------|---------|------|
| **多分类并行搜索** | 同时搜索 cs.AI + cs.LG + cs.CL | 主题跨领域时 | high |
| **中期数量检查** | 每 3 篇论文检查是否达标 | 避免过早停止 | high |
```

### 更新 summary.md

当发现新的意外问题时，添加到历史失败模式：

```markdown
## 学术论文搜索类任务 — 前瞻风险

| 风险 | 历史频率 | 严重程度 | 前瞻检查 | 预防措施 |
|------|---------|---------|---------|---------|
| **网络/API 超时** | 中 | 中 | 是否有网络稳定性评估？ | 准备备用数据源、简化查询 |
```

---

## Quality Checklist / 质量检查

### AfterFlect Report Quality

- [ ] 包含 afterflect_id
- [ ] 包含 preflect_id（关联事前反思）
- [ ] prediction_review 包含三类分析
- [ ] prediction_accuracy 有具体数值
- [ ] success_factors 至少识别 1 个因素
- [ ] learned_patterns 可选但推荐
- [ ] recommendations_for_next_time 有具体建议

---

## CHANGELOG

### v1.0 (2026-02-21)

**Initial Release**:
- 预测回顾流程（predicted/avoided/unexpected）
- 预测准确率计算（precision/recall）
- 成功因素分析
- 经验提炼（learned_patterns）
- 知识库更新机制
- 与 Subagent 的集成方案
