# Research State / 研究状态

## Overview / 概述

Research State Management System v7.0 - LangGraph-inspired state management with persistence.

---

## Research Phases / 研究阶段

```python
class ResearchPhase(Enum):
    PLANNING = "planning"      # 初始规划和分析
    DISCOVERY = "discovery"    # 信息发现阶段
    ANALYSIS = "analysis"      # 深度分析阶段
    SYNTHESIS = "synthesis"    # 结果合成阶段
    REVIEW = "review"          # 质量审核阶段
    COMPLETE = "complete"      # 研究完成
```

---

## Finding Types / 发现类型

```python
class FindingType(Enum):
    ACADEMIC_PAPER = "academic_paper"          # 学术论文
    GITHUB_PROJECT = "github_project"          # GitHub 项目
    COMMUNITY_DISCUSSION = "community_discussion"  # 社区讨论
    CODE_EXAMPLE = "code_example"              # 代码示例
    QUANTITATIVE_METRIC = "quantitative_metric"  # 定量指标
    CONSENSUS_POINT = "consensus_point"        # 共识观点
    CONTROVERSY = "controversy"                 # 争议点
```

---

## Data Schemas / 数据模式

### Citation / 引用格式

**Standardized citation format with clickable links**:

```python
@dataclass
class Citation:
    id: str           # arxiv_id, repo_name, or discussion_id
    type: str         # "academic", "github", "reddit", "hn", "blog"
    title: str
    url: str          # Primary clickable URL
    url_markdown: str # Full markdown with all links
    metadata: Dict    # stars, upvotes, date, etc.
```

**Examples**:
```markdown
# Academic
[arXiv:2402.01680](https://arxiv.org/abs/2402.01680) | [PDF](https://arxiv.org/pdf/2402.01680.pdf)

# GitHub
[langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) ⭐ 10k+

# Discussion
[Hacker News](https://news.ycombinator.com/item?id=12345) (200 upvotes)
```

---

### AcademicPaper / 论文模式

```python
@dataclass
class AcademicPaper:
    # 基本信息
    arxiv_id: str
    title: str
    authors: List[str]
    abstract: str
    url_markdown: str  # [arXiv:ID](URL) | [PDF](PDF_URL)

    # 方法论
    methodology: Dict[str, Any]
    # datasets: str
    # baselines: str
    # models_tested: str
    # evaluation_metrics: str

    # 结果
    quantitative_results: Dict[str, Any]
    # benchmarks: Dict[str, float]
    # comparisons: str
    # statistical_significance: str

    # 分析
    limitations: List[str]
    future_work: List[str]
    implementation: Dict[str, Any]
    # code_url: str
    # datasets_available: bool
    # reproducibility_score: str

    summary: str  # 500-1000 word deep analysis
```

---

### GitHubProject / 项目模式

```python
@dataclass
class GitHubProject:
    # 基本信息
    name: str           # org/repo
    url_markdown: str   # [org/repo](URL) ⭐ Xk+
    stars_display: str  # "⭐ 10,000+"
    description: str
    last_commit_date: str

    # 架构分析
    key_files: List[Dict[str, str]]  # path, description
    architecture_description: str     # 200-500 words
    integration_examples: List[str]
    performance_benchmarks: Dict[str, Any]

    # 元数据
    license: str
    language: str
    framework_type: str  # "orchestration", "state-management", etc.
```

---

### CommunityDiscussion / 讨论模式

```python
@dataclass
class CommunityDiscussion:
    # 基本信息
    platform: str       # "reddit", "hn", "github", "blog"
    url_markdown: str   # Clickable link
    title: str
    original_title: str

    # 分析
    key_quotes: List[Dict[str, Any]]  # user, quote, upvotes
    consensus_level: str  # "high", "medium", "low", "controversial"
    summary: str         # 200-400 words

    # 关联
    related_discussions: List[str]
```

---

## ResearchState / 研究状态

**Complete research session state**:

```python
@dataclass
class ResearchState:
    # Session metadata
    session_id: str
    query: str
    start_time: str

    # Workflow state
    phase: ResearchPhase
    research_phases_completed: List[str]

    # Research data
    findings: ResearchFindings
    citations: List[Citation]
    executive_summary: List[Dict[str, str]]

    # Configuration
    token_budget: int = 200000
    tokens_used: int = 0
    subagents_deployed: int = 0

    # Quality tracking
    quality_scores: Dict[str, float]

    # Context variables (Swarm-style)
    context_variables: Dict[str, Any]
```

---

## ResearchFindings / 研究发现集合

```python
@dataclass
class ResearchFindings:
    academic_papers: List[AcademicPaper]
    github_projects: List[GitHubProject]
    community_discussions: List[CommunityDiscussion]
```

---

## State Persistence / 状态持久化

**ResearchStateManager** features:
- Checkpoint state to disk
- Resume from checkpoint
- List all sessions
- Session cleanup

**Storage format**: `research_data/{session_id}_state.json`

---

## CLI Usage / 命令行使用

```bash
# List all sessions
python "tools\research_state.py" --list

# Show session details
python "tools\research_state.py" --show {session_id}

# Delete a session
python "tools\research_state.py" --delete {session_id}

# Cleanup old sessions
python "tools\research_state.py" --cleanup 7
```

---

## Progress Tracking / 进度跟踪

```python
state.get_progress()
# Returns:
{
    "current_phase": "synthesis",
    "phases_completed": 3,
    "total_phases": 6,
    "progress_percent": 50,
    "papers_found": 15,
    "projects_found": 8,
    "discussions_found": 12
}
```

---

## Related Knowledge / 相关知识

- **report_templates.md**: Report output format using ResearchFindings
- **quality_checklist.md**: Quality validation for ResearchState
- **orchestration_patterns.md**: Phase progression in ResearchState
