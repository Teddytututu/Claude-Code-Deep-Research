# Deep Researcher

基于 Anthropic 架构的多智能体研究编排系统，用于生成 Gemini Deep Research 风格的综合性深度研究报告。

## 简介

本系统采用 **Orchestrator-Worker 模式**，通过多智能体并行协作，实现从学术论文、GitHub 仓库、社区讨论等多维度信息源的深度研究与报告生成。

## 核心特性

| 特性 | 说明 |
|------|------|
| **多智能体编排** | 并行执行专业子代理，90% 速度提升 |
| **性能感知资源分配** | 基于 45% 阈值规则和成本效益分析智能决策 |
| **MAGMA 混合记忆** | 语义记忆 + 时序记忆 + 情景记忆三层架构 |
| **框架智能选择** | 自动推荐 LangGraph、CrewAI、AutoGen 等框架 |
| **双报告生成** | 综合报告（决策者导向）+ 文献综述（学者导向） |
| **双语输出** | 中文叙述 + 英文术语，LaTeX 公式支持 |
| **可观测性** | Token 用量、延迟、成本追踪与可视化 |

## 快速开始

### 基础用法

```python
from research_orchestrator import ResearchOrchestrator

# 初始化研究编排器
orchestrator = ResearchOrchestrator()

# 执行深度研究
result = orchestrator.research(
    topic="multi-agent timeout mechanisms",
    time_budget_minutes=60  # 可选：时间预算
)

# 获取双报告
print(result.comprehensive_report)   # 综合报告
print(result.literature_review)      # 文献综述
```

### 指定时间预算

```python
# 每个子代理将获得全部可用时间（并行执行）
# 例如：60分钟预算 → 每个agent约48分钟
result = orchestrator.research(
    topic="Agent 超时机制",
    time_budget_minutes=60
)
```

### 框架偏好设置

```python
result = orchestrator.research(
    topic="多智能体框架对比",
    framework_preference="LangGraph"  # 或 "CrewAI", "AutoGen"
)
```

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户查询 (User Query)                     │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  Phase -1: 性能预测 (Performance Predictor)                 │
│  - 单智能体成功率评估                                        │
│  - 并行可行性分析                                            │
│  - 成本效益决策                                              │
└────────────────────────────┬────────────────────────────────┘
                             │ 推荐 Multi-Agent?
                  ┌──────────┴──────────┐
                  │ 是                  │ 否 → 单智能体直接回答
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 0: 框架选择 (Framework Selector)                     │
│  - "AutoGen快、CrewAI稳、LangGraph强"                        │
│  - 生产就绪度评估                                            │
└────────────────────────────┬────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: 并行研究执行 (Research Subagents)                 │
│  ├─ academic-researcher   (ArXiv 论文、引用网络)            │
│  ├─ github-watcher        (仓库分析、代码实现)              │
│  └─ community-listener    (社区讨论、实践反馈)              │
└────────────────────────────┬────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2a: 逻辑分析 (Literature Analyzer)                  │
│  - 引用关系与继承链                                         │
│  - 主题聚类与方法族                                         │
│  - 技术演化路径                                             │
└────────────────────────────┬────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 2b: 双报告合成 (Dual Report Writers)                │
│  ├─ deep-research-report-writer → comprehensive_report.md  │
│  └─ literature-review-writer    → literature_review.md     │
└─────────────────────────────────────────────────────────────┘
```

## 项目结构

```
deep-researcher/
├── .claude/                        # Agent 配置目录
│   ├── agents/                     # 子代理规范
│   │   ├── academic-researcher.md
│   │   ├── github-watcher.md
│   │   ├── community-listener.md
│   │   ├── performance-predictor.md
│   │   ├── framework-selector.md
│   │   └── ...
│   ├── hooks/                      # 研究钩子脚本
│   └── mcp-servers.json            # MCP 服务器配置
│
├── research_data/                  # 研究数据存储
│   ├── academic_research_output.json
│   ├── github_research_output.json
│   ├── community_research_output.json
│   └── logic_analysis.json
│
├── research_output/                # 生成的报告
│   ├── {topic}_comprehensive_report.md
│   └── {topic}_literature_review.md
│
├── CLAUDE.md                       # 项目指令文档
│
├── 核心模块/                       # 核心模块
│   ├── research_orchestrator.py    # 主编排器
│   ├── hierarchical_orchestrator.py # 分层编排
│   ├── research_state.py           # 研究状态管理
│   │
│   ├── memory_system.py            # MAGMA 记忆系统
│   ├── memory_graph.py             # 语义记忆图谱
│   ├── hybrid_retriever.py        # 混合检索
│   │
│   ├── framework_selection.py      # 框架选择
│   ├── observability.py            # 可观测性
│   ├── resilience.py              # 弹性系统
│   ├── quality_gate.py            # 质量门控
│   └── output_formatter.py        # 输出格式化
│
└── README.md
```

## 框架选择矩阵

| 框架 | 部署企业 | 延迟开销 | 上线时间 | 适用场景 |
|------|----------|----------|----------|----------|
| **LangGraph** | ~400 | 8% (最低) | 2个月 | 状态繁重工作流、企业级 |
| **CrewAI** | 150+ (含60%财富500强) | 24% | 2周 | 团队协作流程、快速上线 |
| **AutoGen** | Microsoft 生态 | 15% | - | 研究与学术 |
| **Swarm** | 0 | 0% | N/A | ⚠️ 仅教育用途 |

## 性能指标

基于 Anthropic 官方研究：

| 指标 | 数值 | 来源 |
|------|------|------|
| 单智能体效率 | 67 tasks/1K tokens | Anthropic Engineering |
| 多智能体效率 | 14-21 tasks/1K tokens | Anthropic Engineering |
| Token 成本倍数 | 15x | Anthropic Engineering |
| 性能提升 | +90.2% | Anthropic Research |
| 并行任务提升 | +80.9% | Anthropic Research |

## 决策标准

**何时使用多智能体系统：**

- 单智能体成功率 < 45% (Google/MIT 阈值)
- 任务具有可并行方面
- 信息量超过单一上下文窗口
- 任务价值证明 15x 成本增加合理

**何时使用单智能体：**

- 步骤间存在顺序依赖
- 单智能体成功率 > 45%
- 成本敏感应用
- 需要亚秒级延迟

## 配置要求

### Python 依赖

```bash
pip install anthropic
pip install networkx  # 用于图谱操作
pip install matplotlib  # 可视化
```

### MCP 服务器（可选）

系统支持 20-30 个 MCP 服务器配置，建议每次会话启用 5-6 个：

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

## 输出格式

### 综合报告 (Comprehensive Report)

- **目标读者**: 技术决策者、工程师
- **字数**: 6,000-8,000 字
- **内容**: 全面覆盖学术研究 + 工程实践 + 社区反馈
- **特色**: 引用关系图 (Mermaid)、可点击引用、双语术语

### 文献综述 (Literature Review)

- **目标读者**: 研究者、学者
- **字数**: 3,000-5,000 字
- **内容**: 学术为主，逻辑驱动
- **特色**: 演化路径分析、研究缺口识别

## 学术基础

本系统基于以下研究成果：

| 论文 | 主题 |
|------|------|
| MAGMA (arXiv:2601.03236) | 多图谱智能体记忆架构 |
| AgentOrchestra (arXiv:2506.12508) | 分层多智能体框架 |
| GraphRAG (arXiv:2507.03608) | 混合检索系统 |
| BudgetThinker (arXiv:2508.17196) | 预算感知执行 |

## 许可证

MIT License

---

**作者**: Deep Research System
**更新**: 2026-02-10

[English Version](README.md)
