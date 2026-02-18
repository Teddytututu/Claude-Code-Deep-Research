# Chinese Community Insights / 中文社区洞察

> **Purpose**: Best practices and consensus from Chinese tech community.
> **Usage**: Reference this file via `@knowledge:chinese_community_insights.md`

---

## Claude Code Usage Tips / Claude Code 使用技巧

### Essential Commands / 基本命令

- `/init` - Initialize project memory (项目记忆初始化)
- `/clear` - Clear context after completing work (完成后清除上下文)
- `/compact` - Compress conversation while preserving important content (压缩对话保留重要内容)
- Git branching - Create branch for each new feature (每次新功能创建分支)

### Project Memory Structure / 项目记忆结构

- Use hierarchical CLAUDE.md file structure (分层 CLAUDE.md 文件结构)
- CLAUDE.md is the project's "memory" (项目的"记忆")
- Each conversation reads CLAUDE.md at start (每次对话开始时读取)

**Source**: [知乎 - 国内如何使用Claude code完整指南](https://zhuanlan.zhihu.com/p/1951793740248245774)

---

## Context Management (CRITICAL) / 上下文管理（关键）

### The Golden Rule of Context / 上下文黄金法则

```
配置 20-30 个 MCP (MCPs configured: 20-30)
每次只启用 5-6 个 (Active per session: 5-6)
工具总数 < 80 (Total tools: < 80)
```

### Why This Matters / 为什么重要

- MCP tool definitions consume context window
- Skills content uses thousands of tokens
- Historical dialogue consumes large context
- Without management, 200k token window may only have 70k available

### Monitor / 监控

Watch statusline context percentage

**Source**: [知乎 - Claude Code 完全指南](https://zhuanlan.zhihu.com/p/1996333664590639616)

---

## Framework Comparison Insights / 框架对比洞察

### Community Consensus / 社区共识

**"AutoGen快、CrewAI稳、LangGraph强"**

| Framework | Community Perception | Best Use Case |
|-----------|---------------------|---------------|
| AutoGen | 快速验证，十几行代码即可跑通 | 快速原型、学术研究 |
| CrewAI | 任务流与角色定义清晰 | 流程自动化、内容管线 |
| LangGraph | 可视化、状态追踪、循环分支 | 长流程、SaaS Agent 系统 |

### Practical Selection Guidance / 实际选择指南

- 初学者: OpenAI Swarm → CrewAI → LangGraph (learning path)
- 个人开发者: AutoGen (rapid prototyping)
- 中小团队/企业: CrewAI (workflow automation)
- 架构师/平台: LangGraph (long workflows/SaaS)

**Source**: [博客园 - AI Agent 框架实测](https://www.cnblogs.com/jxyai/p/19171973)

---

## Production Deployment Pain Points / 生产部署痛点

### Top Obstacles / 主要障碍

1. **知识冷启动** (Knowledge Cold Start)
   - RAG setup is the #1 obstacle
   - Format fragmentation, chunking disasters, table blind spots
   - Platform size limits (hard 15MB cap)

2. **成本失控** (Cost Spiraling)
   - One company: 30 million tokens consumed daily
   - Multi-agent: 15x token multiplier vs chat
   - Need careful cost-benefit analysis

3. **质量保证** (Quality Assurance)
   - Combinatorial explosion of test paths
   - Error handling complexity (each agent can fail)
   - Testing overhead grows exponentially

4. **上下文腐烂** (Context Rot)
   - Long-running agents accumulate stale context
   - Information degradation over time
   - Need context refresh strategies

**Source**: [AWS China - Agentic AI基础设施实践](https://aws.amazon.com/cn/blogs/china/agentive-ai-infrastructure-practice-series-1/)

---

## Production Timeout Best Practices / 生产超时最佳实践

### Industry Timeout Standards / 行业超时标准

| Platform | Default Timeout | Production Reality |
|----------|-----------------|-------------------|
| Palantir AIP Logic | 5 minutes | **90% failure rate** |
| AWS Bedrock AgentCore | 15 minutes idle | Async-first with /ping |
| Make.com | 5 minutes | Hard limit |
| LangGraph | Configurable | Checkpoint resume capable |

### Architectural Separation Principle / 架构分离原则

> **"Thinking about time" vs "enforcing time"**
>
> - Separating time reasoning from time enforcement prevents production failures
> - Let agents think about time constraints without being blocked by them
> - Enforce timeouts at orchestration level, not individual agent level

### AWS Bedrock Async Patterns / AWS Bedrock 异步模式

```python
@app.ping
def custom_status():
    if system_busy():
        return PingStatus.HEALTHY_BUSY  # "Processing background tasks"
    return PingStatus.HEALTHY            # "Ready for work"
```

**Non-Blocking Architecture Requirements**:
```
✓ DO: Use separate threads for blocking operations
✓ DO: Implement async/await patterns
✓ DO: Return immediately from @app.entrypoint
✗ DON'T: Block in main handler
✗ DON'T: Block /ping endpoint
```

---

## Claude Code vs Cursor Community Sentiment / Claude Code 与 Cursor 社区情绪

### Majority View / 多数观点

Claude Code is more powerful than Cursor:
- "通用计算机自动化框架，恰好很擅长写代码" (General automation framework that happens to be good at coding)
- Advantage comes from context management and tool calling
- Many users: "从那以后就再也没回头过" (Never looked back after switching)

### Challenges / 挑战

- Network restrictions in China
- Smaller interface for mobile coding
- Message sync not real-time
- Sometimes messes up comments despite instructions

**Source**: [知乎问答 - claude code使用感受如何？](https://www.zhihu.com/question/1945503640539333416)
