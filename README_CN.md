# Deep Researcher

> 基于 Anthropic 架构的多智能体研究编排系统，生成 Gemini Deep Research 风格的综合性深度研究报告

## 简介

**Deep Researcher** 是一个基于 Anthropic 多智能体架构的智能研究编排系统。它采用 **orchestrator-worker 模式**，从学术论文、GitHub 仓库、社区讨论等多维度进行深度研究，并将发现合成为双份综合报告。

**核心理念**：这是一个 **Claude Code 原生系统**。编排器逻辑位于 `CLAUDE.md` 中，通过 `Task` 工具协调专门的子代理。Python 模块提供参考实现和支持性基础设施。

## 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    用户查询                                  │
│           "深度研究 Agent 超时机制，给我1小时"                │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  阶段 -1: 性能预测器                                        │
│  - 是否应该使用多智能体？（45% 阈值规则）                     │
│  - 成本效益分析（15x token，90.2% 性能提升）                  │
└────────────────────────────┬────────────────────────────────┘
                             │ 使用多智能体？
                  ┌──────────┴──────────┐
                  │ 是                  │ 否 → 直接回答
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  阶段 0: 框架选择器                                          │
│  - "AutoGen快、CrewAI稳、LangGraph强"                         │
│  - 生产就绪度评估                                            │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  阶段 1: 并行研究执行                                        │
│  ├─ academic-researcher   (ArXiv 论文、引用网络)            │
│  ├─ github-watcher        (仓库分析、代码示例)              │
│  └─ community-listener    (社区讨论、实践反馈)              │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  阶段 2a: 逻辑分析                                          │
│  - 引用关系、主题聚类                                        │
│  - 技术演化路径、研究缺口                                    │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  阶段 2b: 双报告合成                                        │
│  ├─ comprehensive_report.md   (6,000-8,000 字)             │
│  └─ literature_review.md      (3,000-5,000 字)             │
└─────────────────────────────────────────────────────────────┘
```

## 使用方法

### 基本查询

```
深度研究 [topic]
Research [topic]
```

### 指定时间预算

```
深度研究 [topic]，给我1小时
研究 [topic]，30分钟
分析 [topic]，限时2小时
```

**重要提示**：子代理**并行运行**。每个代理获得全部可用时间（不是除以3！）

| 查询 | 时间预算 | 每代理时间 | 总研究量 |
|------|----------|------------|----------|
| `深度研究 Agent 超时机制，给我1小时` | 60 分钟 | ~48 分钟/代理 | 144 分钟并行研究 |
| `Research multi-agent frameworks in 30min` | 30 分钟 | ~24 分钟/代理 | 72 分钟并行研究 |

**时间分配公式**:
```
每代理时间 = 总预算 × 80% (20% 协调开销)

例如："给我1小时"
→ 每个agent: 48分钟
→ 3个agents并行: 总共144分钟的查询量
→ 你等: ~60分钟拿到报告
```

### 指定框架偏好

```
深度研究 [topic]，使用 LangGraph
Research [topic], framework: AutoGen
```

## 决策框架

### 何时使用多智能体

基于 Google/MIT 研究：

```
IF (单智能体成功率 < 45% AND 任务价值 > 成本):
    → 使用多智能体系统
    → 预期: +90.2% 性能提升，15x token 成本
ELSE:
    → 单智能体足够
```

**使用多智能体**：
- 单智能体成功率 < 45%
- 任务具有可并行方面
- 信息量超过单一上下文窗口
- 任务价值证明 15x 成本增加合理

### 框架选择矩阵

| 框架 | 部署企业 | 延迟 | 上线时间 | 最适合 |
|------|----------|------|----------|--------|
| **LangGraph** | ~400 | 8% | 2个月 | 状态繁重工作流、企业级 |
| **CrewAI** | 150+ (含60%财富500强) | 24% | 2周 | 团队工作流、快速上线 |
| **AutoGen → AG2** | Microsoft 生态 | 15% | - | 研究与学术 |
| **Swarm** | 0 | 0% | N/A | ⚠️ 仅教育用途 |

**社区共识**："AutoGen快、CrewAI稳、LangGraph强"

## 输出格式

### 双报告系统

| 报告 | 目标读者 | 字数 | 侧重 |
|------|----------|------|------|
| **综合报告** | 技术决策者、工程师 | 6,000-8,000 字 | 学术 + 工程 + 社区 |
| **文献综述** | 研究者、学者 | 3,000-5,000 字 | 学术为主，逻辑驱动 |

### 报告特色

- **双语**：中文叙述 + 英文术语
- **LaTeX 公式**：数学符号支持
- **可点击引用**：所有来源链接
- **引用关系图**：Mermaid 图表展示关系
- **演化路径**：技术变迁追踪
- **研究缺口**：开放问题识别

## 项目结构

```
deep-researcher/
├── .claude/                        # Claude Code 配置
│   ├── agents/                     # 子代理规范（12 个代理）
│   │   ├── academic-researcher.md
│   │   ├── github-watcher.md
│   │   ├── community-listener.md
│   │   ├── performance-predictor.md
│   │   ├── framework-selector.md
│   │   ├── mcp-coordinator.md
│   │   ├── timeout-specialist.md
│   │   ├── handoff-designer.md
│   │   ├── readiness-assessor.md
│   │   ├── literature-analyzer.md
│   │   ├── deep-research-report-writer.md
│   │   └── literature-review-writer.md
│   ├── hooks/                      # 工作流自动化
│   │   ├── detect_research_intent.py
│   │   ├── token_budget_check.py
│   │   └── research_hooks.json
│   ├── utils/                      # 工具脚本
│   │   └── checkpoint_manager.py
│   └── mcp-servers.json            # MCP 服务器配置
│
├── research_data/                  # 运行时研究数据
│   ├── academic_research_output.json
│   ├── github_research_output.json
│   ├── community_research_output.json
│   └── logic_analysis.json
│
├── research_output/                # 生成的报告
│   ├── {topic}_comprehensive_report.md
│   └── {topic}_literature_review.md
│
├── 核心Python模块                  # 参考实现
│   ├── research_orchestrator.py    # 主编排器 (534 行)
│   ├── hierarchical_orchestrator.py # 三层编排
│   ├── memory_system.py            # MAGMA 记忆架构
│   ├── memory_graph.py             # 语义知识图谱
│   ├── hybrid_retriever.py         # GraphRAG 混合检索
│   ├── framework_selection.py      # 框架选择引擎
│   ├── observability.py            # 指标与追踪
│   ├── resilience.py               # 错误恢复与熔断器
│   ├── quality_gate.py             # LLM-as-judge 验证
│   └── output_formatter.py         # 双语报告格式化
│
├── CLAUDE.md                       # ⭐ 主要编排器逻辑
├── README.md                       # 英文版
└── README_CN.md                    # 本文件
```

## 代理清单

### 决策支持代理（6个）

| 代理 | 用途 |
|------|------|
| **performance-predictor** | 成本效益分析（45% 阈值规则） |
| **framework-selector** | 框架推荐 |
| **mcp-coordinator** | MCP 工具优化 |
| **handoff-designer** | 代理协调模式 |
| **readiness-assessor** | 生产就绪度评估 |
| **timeout-specialist** | 超时预算分配 |

### 研究子代理（3个）

| 代理 | 工具 | 输出 |
|------|------|------|
| **academic-researcher** | ArXiv 搜索、论文下载/阅读 | 论文、引用、全文分析 |
| **github-watcher** | 仓库结构、文件读取、搜索 | 项目、架构、代码示例 |
| **community-listener** | 网页阅读器、网页搜索 | 讨论、共识、社区反馈 |

### 报告合成代理（3个）

| 代理 | 输出 |
|------|------|
| **literature-analyzer** | logic_analysis.json |
| **deep-research-report-writer** | comprehensive_report.md |
| **literature-review-writer** | literature_review.md |

## 学术基础

本系统基于以下研究成果：

| 论文 | 主题 | arXiv ID |
|------|------|----------|
| **MAGMA** | 多图谱智能体记忆架构 | [2601.03236](https://arxiv.org/abs/2601.03236) |
| **AgentOrchestra** | 分层多智能体框架 | [2506.12508](https://arxiv.org/abs/2506.12508) |
| **GraphRAG** | 混合检索系统 | [2507.03608](https://arxiv.org/abs/2507.03608) |
| **BudgetThinker** | 预算感知执行 | [2508.17196](https://arxiv.org/abs/2508.17196) |
| **ALAS** | 超时策略，60% token 减少 | [2511.03094](https://arxiv.org/abs/2511.03094) |
| **B2MAPO** | 批量优化，78.7% 时间减少 | [2407.15077](https://arxiv.org/abs/2407.15077) |

## 性能指标

基于 Anthropic 官方研究：

| 指标 | 数值 | 来源 |
|------|------|------|
| 单智能体效率 | 67 tasks/1K tokens | Anthropic Engineering |
| 多智能体效率 | 14-21 tasks/1K tokens | Anthropic Engineering |
| Token 成本倍数 | 15x | Anthropic Engineering |
| 性能提升 | +90.2% | Anthropic Research |
| 并行任务提升 | +80.9% | Anthropic Research |

## MCP 集成

系统使用 MCP (Model Context Protocol) 进行外部数据访问：

**优化规则**：
- 配置的 MCP 总数：20-30
- 每会话启用：5-6 个
- 活跃工具总数：< 80

**关键 MCP 服务器**：
- **ArXiv**：学术论文搜索和检索
- **GitHub (zread)**：仓库分析
- **Web Search Prime**：通用网页搜索
- **Web Reader**：博客/讨论内容解析

## 生产特性

### 可观测性栈
- Token 用量、延迟和成本追踪
- 分布式代理执行追踪
- 实时事件日志

### 弹性系统
- 指数退避重试策略
- 级联故障预防熔断器
- 基于检查点的恢复
- 优雅降级

### 质量门控系统
- LLM-as-judge 模式（88% vs 61% 人工一致性）
- 引用准确性验证
- 来源质量评估
- 完整性检查

## 配置

### MCP 服务器（可选）

在 `.claude/mcp-servers.json` 中配置：

```json
{
  "mcp_servers": {
    "arxiv": {
      "command": "npx",
      "args": ["-y", "@arxiv/mcp-server"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@github/mcp-server"]
    }
  }
}
```

### 环境变量

```bash
# 必需
ANTHROPIC_API_KEY=your_api_key_here

# 可选
DEFAULT_TIME_BUDGET_MINUTES=60
DEFAULT_FRAMEWORK=LangGraph
```

## 许可证

MIT License

---

**架构**：Claude Code 原生编排器 + 专门子代理
**更新**：2026-02-10

[English Version](README.md)
