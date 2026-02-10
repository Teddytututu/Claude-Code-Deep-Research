---
name: pre-research
description: Enforce proper workflow before deploying research subagents
version: 1.0
---

# Pre-Research Hook / 研究前钩子

## Purpose / 目的

确保深度研究请求在部署 research subagents 之前，先经过所有决策支持代理的分析。

## Trigger Conditions / 触发条件

当用户查询包含以下关键词时触发此钩子：
- "深度研究"
- "Research"
- "Investigate"
- "Analyze"

## Checklist / 检查清单

在调用任何 research subagent (academic-researcher, github-watcher, community-listener) 之前，必须完成：

### Phase -1: Performance Prediction
- [ ] 调用了 `performance-predictor` agent
- [ ] 获得了 cost-benefit 分析
- [ ] 确认 multi-agent 是合适的（single-agent success rate < 45%）

### Phase 0: Framework Selection
- [ ] 调用了 `framework-selector` agent
- [ ] 获得了框架推荐
- [ ] 理解了选择的框架的特点

### Phase 0.5: MCP Coordination
- [ ] 调用了 `mcp-coordinator` agent
- [ ] 确定了要激活的 5-6 个 MCP
- [ ] 验证了总工具数 < 80

### Phase 0.75: Production Readiness (Optional)
- [ ] 如果涉及生产部署，调用了 `readiness-assessor`
- [ ] 确认推荐框架/模式的生产就绪状态

## Decision Logic / 决策逻辑

```
IF performance-predictor recommends single-agent:
    → 直接使用 single-agent 回答
    → 不部署任何 research subagent
    → 节省 15x token 成本

ELSE IF performance-predictor recommends multi-agent:
    → 继续 Phase 0, 0.5, 0.75
    → 然后部署相应的 research subagents
END IF
```

## Action / 动作

如果检查清单未完成：
1. 告诉用户需要先进行决策分析
2. 按顺序调用必要的 decision-support agents
3. 等待分析完成后再部署 research subagents

## Example Workflow / 示例工作流

```
用户: "深度研究 Agent 超时机制"

Step 1: 调用 performance-predictor
        → 返回: "推荐 multi-agent，成功率预计 35%"

Step 2: 调用 framework-selector
        → 返回: "推荐 LangGraph (8% latency)"

Step 3: 调用 mcp-coordinator
        → 返回: "激活: arxiv, web-search, web-reader, zread (5 个 MCP, 12 个工具)"

Step 4: (可选) 调用 readiness-assessor
        → 返回: "LangGraph 生产就绪"

Step 5: 现在可以部署 research subagents
        → Task(academic-researcher, ...)
        → Task(github-watcher, ...)
        → Task(community-listener, ...)
```

## Error Messages / 错误消息

如果尝试跳过决策步骤：

```
错误: 必须先完成决策分析

请按顺序执行：
1. performance-predictor - 评估是否需要 multi-agent
2. framework-selector - 选择合适的框架
3. mcp-coordinator - 优化 MCP 工具选择
4. (可选) readiness-assessor - 生产就绪度检查

然后才能部署 research subagents。
```
