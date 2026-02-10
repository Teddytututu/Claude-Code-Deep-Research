# Memory System (MAGMA) / 记忆系统

## STATUS
✅ **Active** - Implementation complete in `tools/memory_system.py` (v9.0)
Integration with research subagents for automatic finding storage

---

## Overview / 概述

Multi-Graph Agentic Memory Architecture (MAGMA) - 三层记忆架构系统。

Based on: [MAGMA: Multi-Graph Agentic Memory Architecture](https://arxiv.org/abs/2601.03236) [arXiv:2601.03236](https://arxiv.org/abs/2601.03236)

---

## Three Memory Layers / 三层记忆架构

### 1. SemanticMemory / 语义记忆

**Purpose**: 知识图谱存储实体间关系

**Stores**:
- Papers connected by citations
- Projects connected by implementations
- Discussions connected by references
- Concepts connected by co-occurrence

**Node Types**:
```python
NodeType.ACADEMIC_PAPER      # 论文节点
NodeType.GITHUB_PROJECT      # 项目节点
NodeType.COMMUNITY_DISCUSSION # 讨论节点
NodeType.CONCEPT             # 概念节点
NodeType.AUTHOR              # 作者节点
NodeType.FRAMEWORK           # 框架节点
```

**Edge Types**:
```python
EdgeType.CITES        # 引用关系
EdgeType.IMPLEMENTS   # 实现关系
EdgeType.DISCUSSES    # 讨论关系
EdgeType.INTRODUCES   # 引入概念
EdgeType.AUTHORED_BY  # 作者关系
```

---

### 2. TemporalMemory / 时间记忆

**Purpose**: 时间序列跟踪研究进展

**Tracks**:
- Research session timeline
- Finding provenance (what agent found what, when)
- Evolution of insights and concepts
- Progress metrics over time

**Key Classes**:
```python
@dataclass
class Finding:
    id: str
    type: str  # "paper", "project", "discussion", "concept"
    content: Dict[str, Any]
    timestamp: str
    session_id: str
    agent_type: str  # Which agent found this
    confidence: float = 0.8
    source_url: str = ""

@dataclass
class TemporalSnapshot:
    timestamp: str
    session_id: str
    phase: str
    findings_count: int
    key_insights: List[str]
    metrics: Dict[str, Any]
```

---

### 3. EpisodicMemory / 情景记忆

**Purpose**: 管理研究会话上下文窗口

**Manages**:
- Active research context
- Related past sessions
- Cross-session pattern recognition
- Context similarity search

**Key Class**:
```python
@dataclass
class EpisodicContext:
    session_id: str
    query: str
    start_time: str
    context_summary: str
    key_findings: List[str]
    related_sessions: List[str]
    context_embedding: Optional[List[float]]  # For similarity search
```

---

## MAGMAMemory Integration / MAGMA 记忆集成

**Main Entry Point**:
```python
class MAGMAMemory:
    def __init__(self, storage_dir: str = "research_data"):
        self.semantic = SemanticMemory(use_networkx=True)
        self.temporal = TemporalMemory(str(storage_dir / "temporal"))
        self.episodic = EpisodicMemory(str(storage_dir / "episodic"))
```

**Session Management**:
```python
session_id = memory.start_session(query)
memory.add_paper_finding(paper_data, agent_type="academic-researcher")
memory.add_project_finding(project_data, agent_type="github-watcher")
memory.add_discussion_finding(discussion_data, agent_type="community-listener")
memory.record_checkpoint(phase="complete", metrics={})
summary = memory.end_session()
```

---

## CLI Usage / 命令行使用

```bash
# Migrate v7.0 state to v9.0 MAGMA
python "tools\memory_system.py" --migrate research_data/old_state.json --output research_data

# Save semantic graph
python "tools\memory_system.py" --save-graph research_data/semantic_graph.json
```

---

## Storage Structure / 存储结构

```
research_data/
├── semantic_graph.json      # Knowledge graph snapshot
├── temporal/
│   ├── {session_id}_temporal.json  # Session timeline data
├── episodic/
│   ├── {session_id}_episodic.json  # Context window data
```

---

## Research Findings Integration / 研究结果集成

### Adding Findings (Agent Workflow)

**academic-researcher workflow**:
```python
# Initialize at session start
memory = MAGMAMemory(storage_dir="research_data")
session_id = memory.start_session(query)

# For each paper found
memory.add_paper_finding({
    "arxiv_id": "2501.03236",
    "title": "MAGMA: Multi-Graph Agentic Memory",
    "authors": ["Author Name"],
    "abstract": "...",
    "citation_count": 10,
    "url": "https://arxiv.org/abs/2501.03236",
    "key_concepts": ["memory", "knowledge graph", "multi-agent"],
    "type": "sota"  # root, sota, survey
}, agent_type="academic-researcher")

# Record checkpoint after batch
memory.record_checkpoint("batch_complete", {"papers": 5})
```

**github-watcher workflow**:
```python
# For each project found
memory.add_project_finding({
    "name": "langchain-ai/langgraph",
    "description": "Stateful agent framework",
    "stars": "50k+",
    "language": "Python",
    "framework_type": "LangGraph",
    "implements_papers": ["2506.12508"],  # Links to papers
    "architecture": "Graph-based workflow"
}, agent_type="github-watcher")
```

**community-listener workflow**:
```python
# For each discussion found
memory.add_discussion_finding({
    "platform": "reddit",
    "title": "LangGraph vs CrewAI discussion",
    "url": "https://reddit.com/...",
    "upvotes": 100,
    "papers_discussed": ["2506.12508"],
    "consensus_level": "mixed"
}, agent_type="community-listener")
```

### Session End & Summary

```python
# After all research complete
summary = memory.end_session()

# Summary contains:
# - total_findings: count of all findings
# - papers_count, projects_count, discussions_count
# - session_duration: time elapsed
# - key_insights: extracted from all findings
```

---

## Workflow Integration Examples / 工作流集成示例

### Example 1: Research Session with Memory

```python
# Phase 1: Initialize
memory = MAGMAMemory(storage_dir="research_data")
session_id = memory.start_session("multi-agent orchestration")

# Phase 2: During research (parallel agents)
# academic-researcher adds papers
# github-watcher adds projects
# community-listener adds discussions

# Phase 3: Build citation network
memory.save_semantic_graph()

# Phase 4: Generate visualizations
mermaid = memory.semantic.to_mermaid()
pagerank = memory.semantic.get_pagerank()

# Phase 5: End session
summary = memory.end_session()
```

### Example 2: Cross-Session Learning

```python
# New session can benefit from previous research
memory = MAGMAMemory(storage_dir="research_data")

# Load existing semantic graph
memory.load_semantic_graph("research_data/semantic_graph.json")

# Query related work from previous sessions
related = memory.semantic.find_related_papers("new_paper_arxiv_id")

# Get provenance of a finding
finding = memory.temporal.get_finding_provenance("finding_id")
```

---

## Related Modules / 相关模块

- **memory_graph.py**: SemanticMemory implementation with NetworkX
- **hybrid_retriever.py**: GraphRAG retrieval using semantic memory
- **research_orchestrator.py**: Main orchestrator using MAGMA

---

## Key Benefits / 核心优势

1. **Cross-Session Learning**: Findings persist across research sessions
2. **Provenance Tracking**: Know which agent found what, when
3. **Citation Networks**: Build and analyze paper relationships
4. **Context Reuse**: Find related past sessions for new queries

---

## Usage in Agents / 在代理中使用

### Research Subagents (Phase 1)

**When to Initialize MAGMAMemory**:
- At the START of Phase 1 (before any research)
- Same memory instance shared across all research subagents
- Storage directory: `research_data/`

**academic-researcher usage**:
```python
from memory_system import MAGMAMemory

# Initialize once per session
memory = MAGMAMemory(storage_dir="research_data")
session_id = memory.start_session(original_query)

# For each paper found
memory.add_paper_finding(paper_data, agent_type="academic-researcher")

# Progressive checkpointing (every 5 papers)
if paper_count % 5 == 0:
    memory.record_checkpoint("papers_batch", {"count": paper_count})
```

**github-watcher usage**:
```python
# Uses same memory instance
for project in projects:
    memory.add_project_finding(project_data, agent_type="github-watcher")
```

**community-listener usage**:
```python
# Uses same memory instance
for discussion in discussions:
    memory.add_discussion_finding(discussion_data, agent_type="community-listener")
```

### Analysis Agents (Phase 2a)

**literature-analyzer usage**:
```python
# Load existing memory to analyze relationships
memory = MAGMAMemory(storage_dir="research_data")

# Query citation networks
citation_chain = memory.semantic.find_shortest_path(paper_a, paper_b)
related_papers = memory.semantic.find_related_papers(arxiv_id, top_k=5)
pagerank = memory.semantic.get_pagerank()

# Get provenance of findings
provenance = memory.temporal.get_finding_provenance(finding_id)
```

### Report Writers (Phase 2b)

**deep-research-report-writer usage**:
```python
# Generate citation network visualization
mermaid_graph = memory.semantic.to_mermaid()

# Get session summary for Executive Summary
session_summary = memory.get_session_summary(session_id)

# Access provenance for source attribution
source_agent = memory.temporal.get_finding_provenance(paper_id)
```

---

## Data Storage Format / 数据存储格式

### Session Files
```
research_data/
├── semantic_graph.json          # Knowledge graph snapshot
├── temporal/
│   └── {session_id}_temporal.json   # Timeline of findings
├── episodic/
│   └── {session_id}_episodic.json   # Session context
└── sessions.json                # Session index
```

### JSON Structure (semantic_graph.json)
```json
{
  "nodes": [
    {
      "id": "paper_2501.03236",
      "type": "academic_paper",
      "attributes": {
        "title": "MAGMA Memory",
        "arxiv_id": "2501.03236",
        "authors": ["..."],
        "year": 2025,
        "type": "sota"
      }
    }
  ],
  "edges": [
    {
      "source": "paper_2501.03236",
      "target": "concept_memory",
      "type": "introduces",
      "weight": 1.0
    }
  ],
  "stats": {
    "node_count": 100,
    "edge_count": 250
  }
}
```

---

## Error Handling / 错误处理

```python
# Safe initialization with fallback
try:
    memory = MAGMAMemory(storage_dir="research_data")
    memory.load_semantic_graph("research_data/semantic_graph.json")
except FileNotFoundError:
    # Start fresh if no existing graph
    memory = MAGMAMemory(storage_dir="research_data")
except Exception as e:
    # Log and continue without memory
    logger.warning(f"Memory system unavailable: {e}")
    memory = None
```
