# Visualization Patterns Knowledge Base

## Overview
从 `visualization.py` 和 `cross_domain_tracker.py` 提取的可视化模式核心逻辑

**Purpose**: 提供多智能体研究系统的可视化生成模式

---

## Key Classes / 类

### VisualizationFormat (可视化格式枚举)

**Purpose**: 输出可视化格式类型

**Values**:
- `HTML`: 交互式 HTML (pyvis)
- `PNG`: 静态 PNG 图片
- `SVG`: 静态 SVG 图片
- `MERMAID`: Mermaid 图表字符串

### NodeType (节点类型枚举)

**Purpose**: 可视化样式节点类型

**Values**:
- `PAPER`: 学术论文
- `REPO`: GitHub 仓库
- `COMMUNITY`: 社区讨论
- `CONCEPT`: 概念
- `AUTHOR`: 作者
- `FRAMEWORK`: 框架

### RelationshipType (关系类型枚举)

**Purpose**: 跨域关系类型

**Values**:
- `PAPER_TO_REPO` (implements): 论文被代码仓库实现
- `PAPER_TO_COMMUNITY` (validates): 论文在社区讨论中被验证
- `REPO_TO_COMMUNITY` (discusses): 代码仓库在社区被讨论
- `REPO_TO_PAPER` (cites): 代码仓库 README 引用论文
- `PAPER_TO_PAPER` (cites): 论文引用另一篇论文
- `REPO_TO_REPO` (forks): 代码仓库分支
- `COMMUNITY_TO_COMMUNITY` (references): 讨论引用另一讨论

### VisualizationConfig (可视化配置)

**Purpose**: 可视化生成配置数据结构

**Key Attributes**:
- `output_dir`: 输出目录 (默认 research_output/visualizations)
- `enable_physics`: 是否启用物理效果 (默认 True)
- `height`: 高度 (默认 600px)
- `width`: 宽度 (默认 100%)
- `bgcolor`: 背景色 (默认 #ffffff)
- `font_color`: 字体颜色 (默认 #000000)

**节点颜色配置**:
- `color_paper`: #3498db (蓝色)
- `color_repo`: #2ecc71 (绿色)
- `color_community`: #e67e22 (橙色)
- `color_concept`: #9b59b6 (紫色)
- `color_author`: #95a5a6 (灰色)
- `color_framework`: #e74c3c (红色)

### CitationNetworkVisualizer (引用网络可视化器)

**Purpose**: 生成学术论文引用网络的可视化

**Key Methods**:
- `__init__(papers, citations, config)`: 初始化
- `render(output_path, format)`: 渲染可视化
- `render_inheritance_chain(paper_id, max_depth, output_path)`: 渲染继承链

**支持的布局**: 分层布局 (root → sota → survey)

### CrossDomainVisualizer (跨域可视化器)

**Purpose**: 生成跨域关系可视化 (论文、代码、社区)

**Key Methods**:
- `__init__(graph_data, config)`: 初始化
- `render(output_path, format)`: 渲染可视化
- `render_bipartite(domain_a, domain_b, output_path)`: 渲染双分图

### VisualizationBuilder (统一可视化构建器)

**Purpose**: 自动从研究数据生成所有可视化

**Key Methods**:
- `__init__(research_data_dir, output_dir, config)`: 初始化
- `generate_all()`: 生成所有可视化并返回 HTML 嵌入代码
- `get_legend_html()`: 生成图例 HTML

### CrossDomainTracker (跨域关系追踪器)

**Purpose**: 维护跨研究域的关系图

**Key Methods**:
- `add_paper(paper_id, metadata)`: 注册论文
- `add_repo(repo_name, metadata)`: 注册代码仓库
- `add_community(discussion_id, metadata)`: 注册社区讨论
- `add_paper_repo_relationship(...)`: 添加论文-代码关系
- `add_paper_community_relationship(...)`: 添加论文-社区关系
- `add_repo_community_relationship(...)`: 添加代码-社区关系
- `find_bridging_entities(min_domains)`: 查找桥接实体
- `get_cross_domain_graph()`: 获取完整跨域图
- `load_from_research_data(research_data_dir)`: 从研究数据加载
- `save(filepath)`: 保存状态到 JSON
- `load(filepath)`: 从 JSON 加载状态

---

## Node Styling / 节点样式

### Domain-Based Colors (基于域的颜色)

| Domain | Color | Hex | Shape |
|--------|-------|-----|-------|
| Paper (论文) | Blue | #3498db | Dot |
| Repo (代码) | Green | #2ecc71 | Square |
| Community (社区) | Orange | #e67e22 | Diamond |
| Concept (概念) | Purple | #9b59b6 | Triangle |
| Author (作者) | Gray | #95a5a6 | Ellipse |
| Framework (框架) | Red | #e74c3c | Dot |

### Paper Type Colors (论文类型颜色)

| Type | Color | Hex | Description |
|------|-------|-----|-------------|
| Root (根基) | Red | #e74c3c | Foundational papers |
| SOTA (最先进) | Blue | #3498db | Current state |
| Survey (综述) | Orange | #f39c12 | Review papers |

---

## CLI Usage / 命令行使用

### visualization.py

```bash
# 生成测试可视化
python "tools\visualization.py" --test

# 从研究数据生成所有可视化
python "tools\visualization.py" --data-dir research_data --output-dir research_output/visualizations

# 指定输出格式
python "tools\visualization.py" --format mermaid
```

**命令参数**:
- `--data-dir`: 研究数据目录 (默认 research_data)
- `--output-dir`: 输出目录 (默认 research_output/visualizations)
- `--test`: 生成测试可视化
- `--format`: 输出格式 (html/png/svg/mermaid)

### cross_domain_tracker.py

```bash
# 从研究数据加载并显示统计
python "tools\cross_domain_tracker.py" --load-data research_data --stats

# 显示桥接实体
python "tools\cross_domain_tracker.py" --load-data research_data --bridging

# 保存追踪状态
python "tools\cross_domain_tracker.py" --load-data research_data --save cross_domain_state.json
```

**命令参数**:
- `--load-data`: 从目录加载研究数据
- `--save`: 保存追踪状态到文件
- `--bridging`: 显示桥接实体
- `--stats`: 显示统计信息

---

## Code Patterns / 代码模式

### Pattern 1: Generate All Visualizations

```python
from visualization import VisualizationBuilder

builder = VisualizationBuilder(
    research_data_dir="research_data",
    output_dir="research_output/visualizations"
)

embeds = builder.generate_all()
# Returns:
# {
#     "citation_network": '<iframe src="..."></iframe>',
#     "cross_domain": '<iframe src="..."></iframe>'
# }
```

### Pattern 2: Cross-Domain Tracking

```python
from cross_domain_tracker import CrossDomainTracker

tracker = CrossDomainTracker()

# 加载研究数据
tracker.load_from_research_data("research_data")

# 查找桥接实体（连接多个域）
bridging = tracker.find_bridging_entities(min_domains=2)

# 获取图数据用于可视化
graph_data = tracker.get_cross_domain_graph()
```

### Pattern 3: Custom Citation Network

```python
from visualization import CitationNetworkVisualizer, VisualizationConfig

papers = [
    {"arxiv_id": "2308.00352", "title": "MetaGPT", "type": "sota"},
    {"arxiv_id": "2308.08155", "title": "AutoGen", "type": "sota"},
]

citations = [
    ("2506.12508", "2308.00352"),  # paper1 cites paper2
]

config = VisualizationConfig(
    enable_physics=True,
    height="600px",
    layout_algorithm="hierarchical"
)

visualizer = CitationNetworkVisualizer(papers, citations, config)
visualizer.render("output.html", VisualizationFormat.HTML)
```

---

## Integration Points / 集成点

**Reading Agents**:
- `visualization-generator`: 使用此知识库生成可视化

**CLI Invocations**:
```bash
# Agent 可调用此命令生成可视化
python "tools\visualization.py" --data-dir research_data --output-dir research_output/visualizations
```

**Related Knowledge Base**:
- `.claude/knowledge/orchestration_patterns.md`: 编排模式相关
- `.claude/knowledge/quality_checklist.md`: 质量检查相关

---

## Fallback Handling / 降级处理

### Dependency Availability (依赖可用性)

| Dependency | Purpose | Fallback |
|------------|---------|----------|
| `networkx` | Graph operations | Adjacency list fallback |
| `pyvis` | Interactive HTML | Static HTML fallback |
| `matplotlib` | PNG/SVG images | Mermaid diagram fallback |

### Graceful Degradation Strategy

```python
# Check dependencies
NETWORKX_AVAILABLE = False
PYVIS_AVAILABLE = False
MATPLOTLIB_AVAILABLE = False

# Fallback hierarchy:
# 1. Try pyvis (interactive HTML)
# 2. Fallback to static HTML with lists
# 3. Fallback to Mermaid diagram
# 4. Fallback to plain text
```

---

## Performance Considerations / 性能考虑

| Graph Size | Nodes | Render Time | Memory |
|------------|-------|-------------|--------|
| Small | < 50 | < 10s | < 100MB |
| Medium | 50-200 | 10-30s | 100-500MB |
| Large | 200-500 | 30-60s | 500MB-1GB |
| XLarge | > 500 | Truncate | > 1GB |

**For large graphs**: 自动限制到 Top 节点 (按 PageRank)

---

## Notes / 说明

- **MAGMA Based**: 基于 MAGMA: Multi-Graph Agentic Memory Architecture (arXiv:2601.03236)
- **Fallback Ready**: 当 pyvis 不可用时自动生成降级 HTML
- **Domain Colors**: 蓝(论文)、绿(代码)、橙(社区) 是标准配色
- **Hierarchical Layout**: 引用网络使用分层布局 (root → sota → survey)
- **Bridge Detection**: 自动检测连接多个域的桥接实体
