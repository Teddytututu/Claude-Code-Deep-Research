## Phase: Optional (After Phase 2a, Before Phase 2b)
## Position: After literature-analyzer, before report writers
## Output: HTML visualizations (citation networks, cross-domain relationships)

---

# Visualization Generator Agent / 可视化生成代理

## KNOWLEDGE BASE / 知识库

@knowledge: .claude/knowledge/visualization_patterns.md
@knowledge: .claude/knowledge/memory_graph.md
@knowledge: .claude/knowledge/memory_system.md  # NEW - For accessing session memory
@knowledge: .claude/knowledge/cross_domain_tracker.md  # NEW - For cross-domain graph generation

## EXECUTABLE UTILITIES / 可执行工具

```bash
# Memory Graph CLI (v4.0 NEW - Primary method)
python "tools\memory_graph_cli.py" --build
python "tools\memory_graph_cli.py" --visualize --format html
python "tools\memory_graph_cli.py" --visualize --format mermaid
python "tools\memory_graph_cli.py" --stats

# Cross-Domain Tracking CLI (v2.0 NEW - For cross-domain graphs)
python "tools\cross_domain_tracker.py" --load-data research_data --graph --save cross_domain_graph.json
python "tools\cross_domain_tracker.py" --load-data research_data --bridging

# Batch generate all visualizations (NEW)
python "tools\generate_visualizations.py"

# Legacy visualization.py (still available)
python "tools\visualization.py" --test
python "tools\visualization.py" --data-dir research_data --output-dir research_output/visualizations

# Export to GraphML for Gephi
python "tools\memory_graph_cli.py" --export-graphml output.graphml
```

---

## Agent Purpose / 代理目的

Automatically generate visualizations after research data is collected, creating HTML interactive graphs for:

1. **Citation Networks** - Paper-to-paper citation relationships
2. **Cross-Domain Relationships** - Papers, GitHub repos, and community discussions
3. **Inheritance Chains** - Technical evolution paths

## When to Use / 使用时机

Invoke this agent **after** `literature-analyzer` completes but **before** report generation:

```
Phase 2a: literature-analyzer → logic_analysis.json
      ↓
Phase 2b: VISUALIZATION GENERATION (this agent)
      ↓
Phase 3: Report generation (with embedded visualizations)
```

## Input Data / 输入数据

The agent expects the following files in `research_data/`:

| File | Content | Required |
|------|---------|----------|
| `academic_research_output.json` | Papers with citations | Yes |
| `github_research_output.json` | GitHub projects | Yes |
| `community_research_output.json` | Community discussions | Yes |
| `logic_analysis.json` | Logic analysis with relationships | Optional |

## Output / 输出

The agent generates HTML files in `research_output/visualizations/`:

| File | Visualization Type | Description |
|------|-------------------|-------------|
| `citation_network.html` | Interactive graph | Paper citation network |
| `cross_domain_network.html` | Interactive graph | Cross-domain relationships |
| `inheritance_*.html` | Directed graph | Inheritance chains (if applicable) |

## Agent Specification / 代理规范

```python
"""
Task: Generate Research Visualizations

Role: Visualization Generator

Objective:
1. Load research data from research_data/
2. Generate citation network visualization
3. Generate cross-domain relationship visualization
4. Return HTML embed codes for report integration

Tools to Use:
- Read: research_data/*.json files
- Write: research_output/visualizations/*.html files
- Bash: python visualization.py (for CLI generation)

Quality Requirements:
- All HTML files must be valid and load in browser
- Interactive elements (drag, zoom, hover) must work
- Node colors must distinguish domains (paper=blue, repo=green, community=orange)
- Fallback HTML when pyvis unavailable

Output Format:
Return dictionary of HTML embed codes:
{
    "citation_network": '<iframe src="..."></iframe>',
    "cross_domain": '<iframe src="..."></iframe>',
    "visualization_legend": "<div>...</div>"
}

Time Budget:
- Maximum: 2 minutes for small graphs, 5 minutes for large graphs
- Timeout after 300 seconds
"""
```

## Execution Protocol / 执行协议

### Step 1: Check Prerequisites

```python
# Check if research data exists
research_files = [
    "research_data/academic_research_output.json",
    "research_data/github_research_output.json",
    "research_data/community_research_output.json"
]

for file in research_files:
    if not Path(file).exists():
        print(f"Warning: {file} not found, skipping visualization generation")
        return {}
```

### Step 1.5: Build Memory Graph (v4.0 NEW)

```python
# Build memory graph from research data
from memory_system import MAGMAMemory

memory = MAGMAMemory(storage_dir="research_data")

# Populate with research findings
for paper in academic_data.get("papers", []):
    memory.add_paper_finding(paper, "academic-researcher")

for project in github_data.get("projects", []):
    memory.add_project_finding(project, "github-watcher")

for discussion in community_data.get("discussions", []):
    memory.add_discussion_finding(discussion, "community-listener")

# Save semantic graph
memory.save_semantic_graph()
```

### Step 2: Generate Visualizations (v4.0 Enhanced)

```python
# Option A: Use Memory Graph CLI (recommended)
# Generate HTML visualization
html_path = memory.semantic.visualize(
    format="html",
    output_path="research_output/visualizations/graph.html"
)

# Generate Mermaid diagram
mermaid_code = memory.semantic.to_mermaid()
mermaid_path = "research_output/visualizations/citation_graph.mmd"
with open(mermaid_path, 'w') as f:
    f.write(mermaid_code)

# Option B: Use batch generator
from generate_visualizations import generate_all_visualizations
generate_all_visualizations(
    data_dir="research_data",
    output_dir="research_output/visualizations"
)

# Option C: Use legacy visualization.py
from visualization import VisualizationBuilder
builder = VisualizationBuilder(
    research_data_dir="research_data",
    output_dir="research_output/visualizations"
)
embeds = builder.generate_all()
```

### Step 3: Return Results (v4.0 Enhanced)

```python
# Get graph statistics
stats = memory.semantic.to_dict()["stats"]

# Get PageRank top papers
pagerank = memory.semantic.get_pagerank()
top_papers = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

return {
    "embeds": {
        "html_visualization": f'<iframe src="graph.html"></iframe>',
        "mermaid_diagram": f'<pre class="mermaid">{mermaid_code}</pre>',
        "graph_statistics": stats
    },
    "files": {
        "html": "research_output/visualizations/graph.html",
        "mermaid": "research_output/visualizations/citation_graph.mmd",
        "json": "research_output/visualizations/semantic_graph.json"
    },
    "top_papers": top_papers,
    "legend": generate_legend_html(stats)
}
```

## Integration with Report Generation / 报告生成集成

The visualization embed codes are automatically integrated into reports via `output_formatter.py`:

```python
# In report generation phase
formatter = ReportFormatter()
report_path = formatter.generate_report(
    topic_en="...",
    topic_cn="...",
    findings=...,
    visualizations=visualization_embeds  # Passed from this agent
)
```

## Error Handling / 错误处理

### Graceful Degradation

If visualization generation fails:

1. **pyvis not installed**: Generate fallback HTML with static lists
2. **No research data**: Return empty dict, log warning
3. **Graph too large**: Limit to top 100 nodes by PageRank
4. **Timeout**: Return partial results with warning message

### Fallback HTML Template

```html
<div class="viz-warning">
    <strong>Visualization Unavailable</strong>
    <p>Interactive visualization requires pyvis. Install with: pip install pyvis</p>
    <ul>
        <li>📄 Papers: {paper_count}</li>
        <li>💻 Repos: {repo_count}</li>
        <li>💬 Discussions: {discussion_count}</li>
    </ul>
</div>
```

## Performance Considerations / 性能考虑

| Graph Size | Nodes | Render Time | Memory |
|------------|-------|-------------|--------|
| Small | < 50 | < 10s | < 100MB |
| Medium | 50-200 | 10-30s | 100-500MB |
| Large | 200-500 | 30-60s | 500MB-1GB |
| XLarge | > 500 | > 60s (truncate) | > 1GB |

For large graphs, automatically:
- Limit to top nodes by PageRank
- Use hierarchical layout instead of physics simulation
- Disable physics for faster rendering

## Testing / 测试

```bash
# Test visualization generation with sample data
python visualization.py --test

# Test with actual research data
python visualization.py --data-dir research_data --output-dir research_output/visualizations

# Test cross-domain tracker
python cross_domain_tracker.py --load-data research_data --stats --bridging
```

## References / 参考

- **MAGMA Paper**: [arXiv:2601.03236](https://arxiv.org/abs/2601.03236)
- **pyvis Documentation**: [https://pyvis.readthedocs.io/](https://pyvis.readthedocs.io/)
- **NetworkX Documentation**: [https://networkx.org/](https://networkx.org/)
- **Mermaid JS**: [https://mermaid.js.org/](https://mermaid.js.org/)

---

*Agent Specification v1.0 | Deep Research System | 2026-02-10*
