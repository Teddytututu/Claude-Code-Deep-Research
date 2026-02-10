"""
Multi-Agent Research Visualization System v1.0
多智能体研究可视化系统

Generates interactive HTML visualizations for:
- Citation networks (paper-to-paper relationships)
- Cross-domain relationships (papers, repos, communities)
- Inheritance chains (technical evolution)

Output formats:
- HTML interactive graphs (pyvis)
- PNG/SVG static images (matplotlib)
- Mermaid diagrams (for markdown embedding)

Based on: MAGMA: Multi-Graph Agentic Memory Architecture (arXiv:2601.03236)

Dependencies:
- networkx>=3.1 (already in project)
- pyvis>=0.3.0 (new dependency for interactive HTML)

Author: Deep Research System
Date: 2026-02-10
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
from abc import ABC, abstractmethod

# Check for dependencies
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.colors import to_hex
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class VisualizationFormat(Enum):
    """Output visualization formats"""
    HTML = "html"  # Interactive HTML (pyvis)
    PNG = "png"  # Static PNG image
    SVG = "svg"  # Static SVG image
    MERMAID = "mermaid"  # Mermaid diagram string


class NodeType(Enum):
    """Node types for visualization styling"""
    PAPER = "paper"
    REPO = "repo"
    COMMUNITY = "community"
    CONCEPT = "concept"
    AUTHOR = "author"
    FRAMEWORK = "framework"


@dataclass
class VisualizationConfig:
    """Configuration for visualization generation"""
    output_dir: str = "research_output/visualizations"
    enable_physics: bool = True
    height: str = "600px"
    width: str = "100%"
    bgcolor: str = "#ffffff"
    font_color: str = "#000000"
    cdn_resources: str = "in_line"  # or "local" for offline use

    # Node colors by type
    color_paper: str = "#3498db"  # Blue
    color_repo: str = "#2ecc71"  # Green
    color_community: str = "#e67e22"  # Orange
    color_concept: str = "#9b59b6"  # Purple
    color_author: str = "#95a5a6"  # Gray
    color_framework: str = "#e74c3c"  # Red

    # Node sizes
    size_small: int = 10
    size_medium: int = 20
    size_large: int = 30

    # Layout options
    layout_algorithm: str = "hierarchical"  # "hierarchical", "force", "circular"


class BaseVisualizer(ABC):
    """Abstract base class for visualizers"""

    def __init__(self, config: Optional[VisualizationConfig] = None):
        self.config = config or VisualizationConfig()
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist"""
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def render(self, output_path: str, format: VisualizationFormat) -> str:
        """Render visualization to file"""
        pass


class CitationNetworkVisualizer(BaseVisualizer):
    """
    Citation Network Visualizer

    Generates visualizations of academic paper citation networks.
    Supports hierarchical layout: root -> sota -> survey papers.
    """

    def __init__(
        self,
        papers: List[Dict[str, Any]],
        citations: List[Tuple[str, str]],
        config: Optional[VisualizationConfig] = None
    ):
        """
        Initialize citation network visualizer.

        Args:
            papers: List of paper dictionaries with arxiv_id, title, type (root/sota/survey)
            citations: List of (citing_paper_id, cited_paper_id) tuples
            config: Visualization configuration
        """
        super().__init__(config)
        self.papers = {p.get("arxiv_id", p.get("id", "")): p for p in papers}
        self.citations = citations
        self._graph = self._build_graph()

    def _build_graph(self) -> Optional['nx.DiGraph']:
        """Build NetworkX directed graph from citation data"""
        if not NETWORKX_AVAILABLE:
            return None

        G = nx.DiGraph()

        # Add nodes
        for paper_id, paper_data in self.papers.items():
            paper_type = paper_data.get("type", "sota")
            G.add_node(
                f"paper_{paper_id}",
                label=paper_data.get("title", paper_id)[:40],
                title=paper_data.get("title", paper_id),
                type=paper_type,
                arxiv_id=paper_id,
                group=paper_type,
                color=self._get_color_for_type(paper_type),
                size=self._get_size_for_type(paper_type)
            )

        # Add edges
        for citing, cited in self.citations:
            if f"paper_{citing}" in G.nodes() and f"paper_{cited}" in G.nodes():
                G.add_edge(f"paper_{citing}", f"paper_{cited}")

        return G

    def _get_color_for_type(self, paper_type: str) -> str:
        """Get color for paper type"""
        colors = {
            "root": "#e74c3c",  # Red - foundational
            "sota": self.config.color_paper,  # Blue - current state
            "survey": "#f39c12"  # Orange - review
        }
        return colors.get(paper_type, self.config.color_paper)

    def _get_size_for_type(self, paper_type: str) -> int:
        """Get node size for paper type"""
        sizes = {
            "root": self.config.size_large,
            "sota": self.config.size_medium,
            "survey": self.config.size_small
        }
        return sizes.get(paper_type, self.config.size_medium)

    def render(self, output_path: str, format: VisualizationFormat = VisualizationFormat.HTML) -> str:
        """
        Render citation network visualization.

        Args:
            output_path: Output file path
            format: Output format (HTML, PNG, SVG, MERMAID)

        Returns:
            Path to generated file
        """
        if format == VisualizationFormat.HTML:
            return self._render_html(output_path)
        elif format in (VisualizationFormat.PNG, VisualizationFormat.SVG):
            return self._render_image(output_path, format.value)
        elif format == VisualizationFormat.MERMAID:
            return self._render_mermaid(output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _render_html(self, output_path: str) -> str:
        """Render interactive HTML using pyvis"""
        if not PYVIS_AVAILABLE or not NETWORKX_AVAILABLE:
            print("Warning: pyvis or networkx not available. Generating fallback HTML.")
            return self._render_fallback_html(output_path)

        # Create pyvis network
        net = Network(
            height=self.config.height,
            width=self.config.width,
            bgcolor=self.config.bgcolor,
            font_color=self.config.font_color,
            directed=True,
            cdn_resources=self.config.cdn_resources
        )

        # Configure physics
        if self.config.enable_physics:
            net.set_options("""
            {
                "physics": {
                    "enabled": true,
                    "hierarchicalRepulsion": {
                        "centralGravity": 0.0,
                        "springLength": 200,
                        "springConstant": 0.01,
                        "nodeDistance": 200,
                        "damping": 0.09
                    },
                    "minVelocity": 0.75,
                    "solver": "hierarchicalRepulsion"
                }
            }
            """)
        else:
            # Use hierarchical layout
            net.set_options("""
            {
                "layout": {
                    "hierarchical": {
                        "enabled": true,
                        "direction": "UD",
                        "sortMethod": "directed",
                        "levelSeparation": 150
                    }
                },
                "physics": {
                    "enabled": false
                }
            }
            """)

        # Add nodes from NetworkX graph
        if self._graph:
            for node, data in self._graph.nodes(data=True):
                net.add_node(
                    node,
                    label=data.get("label", node),
                    title=data.get("title", node),
                    color=data.get("color", self.config.color_paper),
                    size=data.get("size", self.config.size_medium),
                    group=data.get("group", "paper")
                )

            # Add edges
            for source, target in self._graph.edges():
                net.add_edge(source, target, arrows="to")

        # Save HTML
        net.save_graph(output_path)
        return output_path

    def _render_fallback_html(self, output_path: str) -> str:
        """Generate simple HTML fallback when pyvis unavailable"""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Citation Network</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .warning {{ background: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .paper-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
        .paper {{ border: 1px solid #ddd; padding: 10px; border-radius: 5px; }}
        .paper.root {{ border-left: 4px solid #e74c3c; }}
        .paper.sota {{ border-left: 4px solid #3498db; }}
        .paper.survey {{ border-left: 4px solid #f39c12; }}
        h2 {{ color: #333; }}
    </style>
</head>
<body>
    <h2>Citation Network Visualization</h2>
    <div class="warning">
        <strong>Note:</strong> Interactive visualization requires pyvis library.
        Install with: pip install pyvis
    </div>
    <h3>Papers ({len(self.papers)})</h3>
    <div class="paper-list">
"""

        for paper_id, paper in self.papers.items():
            paper_type = paper.get("type", "sota")
            title = paper.get("title", paper_id)
            url = f"https://arxiv.org/abs/{paper_id}" if paper_id else "#"
            html_content += f"""
        <div class="paper {paper_type}">
            <a href="{url}" target="_blank">{title}</a><br>
            <small>{paper_type.upper()}</small>
        </div>"""

        html_content += """
    </div>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_path

    def _render_mermaid(self, output_path: str) -> str:
        """Generate Mermaid diagram string"""
        lines = ["graph TD"]

        # Add nodes with styling
        for paper_id, paper in self.papers.items():
            paper_type = paper.get("type", "sota")
            title = paper.get("title", paper_id).replace('"', "'")
            short_id = paper_id.replace("-", "_")[:8]

            if paper_type == "root":
                lines.append(f'    {short_id}["{title}"]:::root')
            elif paper_type == "survey":
                lines.append(f'    {short_id}["{title}"]:::survey')
            else:
                lines.append(f'    {short_id}["{title}"]:::sota')

        # Add edges
        for citing, cited in self.citations:
            citing_short = citing.replace("-", "_")[:8]
            cited_short = cited.replace("-", "_")[:8]
            lines.append(f'    {citing_short} --> {cited_short}')

        # Add styles
        lines.append("""
    classDef root fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    classDef sota fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    classDef survey fill:#f39c12,stroke:#e67e22,stroke-width:2px,color:#fff
""")

        mermaid_diagram = "\n".join(lines)

        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_diagram)

        return output_path

    def _render_image(self, output_path: str, format: str) -> str:
        """Render static image using matplotlib"""
        if not MATPLOTLIB_AVAILABLE or not NETWORKX_AVAILABLE:
            raise RuntimeError("matplotlib and networkx required for image output")

        fig, ax = plt.subplots(figsize=(12, 8))

        if self._graph:
            # Use hierarchical layout
            try:
                pos = nx.nx_agraph.graphviz_layout(self._graph, prog='dot')
            except:
                pos = nx.spring_layout(self._graph)

            # Draw nodes by type
            for paper_type, nodes in self._group_nodes_by_type().items():
                node_list = [f"paper_{n}" for n in nodes if f"paper_{n}" in self._graph.nodes()]
                nx.draw_networkx_nodes(
                    self._graph, pos, nodelist=node_list,
                    node_color=self._get_color_for_type(paper_type),
                    node_size=[self._get_size_for_type(paper_type) * 50] * len(node_list),
                    label=paper_type.upper(), ax=ax
                )

            # Draw edges
            nx.draw_networkx_edges(self._graph, pos, alpha=0.5, arrows=True, ax=ax)

            # Draw labels for important nodes
            labels = {n: self.papers.get(n.replace("paper_", ""), {}).get("title", n)[:15]
                     for n in self._graph.nodes()}
            nx.draw_networkx_labels(self._graph, pos, labels, font_size=8, ax=ax)

        ax.legend()
        ax.set_title("Citation Network")
        plt.axis('off')

        fig.savefig(output_path, format=format, dpi=150, bbox_inches='tight')
        plt.close()

        return output_path

    def _group_nodes_by_type(self) -> Dict[str, List[str]]:
        """Group paper IDs by type"""
        groups = {"root": [], "sota": [], "survey": []}
        for paper_id, paper in self.papers.items():
            paper_type = paper.get("type", "sota")
            groups.setdefault(paper_type, []).append(paper_id)
        return groups

    def render_inheritance_chain(self, paper_id: str, max_depth: int = 3, output_path: str = "") -> str:
        """
        Render inheritance chain starting from a paper.

        Args:
            paper_id: Starting paper ArXiv ID
            max_depth: Maximum depth of chain
            output_path: Output file path

        Returns:
            Path to generated file
        """
        if not output_path:
            output_path = str(Path(self.config.output_dir) / f"inheritance_{paper_id.replace('/', '_')}.html")

        # Build subgraph of inheritance chain
        chain = self._get_citation_chain(paper_id, max_depth)

        # Create visualizer for chain
        chain_papers = {pid: self.papers.get(pid, {"title": pid}) for pid in chain}
        chain_citations = [(a, b) for a, b in self.citations if a in chain and b in chain]

        chain_viz = CitationNetworkVisualizer(
            papers=[chain_papers[pid] for pid in chain],
            citations=chain_citations,
            config=self.config
        )

        return chain_viz._render_html(output_path)

    def _get_citation_chain(self, paper_id: str, max_depth: int) -> List[str]:
        """Get all papers in citation chain"""
        chain = set()
        frontier = {paper_id}

        for _ in range(max_depth):
            next_frontier = set()
            for pid in frontier:
                chain.add(pid)
                # Find papers that cite this paper
                for citing, cited in self.citations:
                    if cited == pid and citing not in chain:
                        next_frontier.add(citing)
            frontier = next_frontier

        return list(chain)


class CrossDomainVisualizer(BaseVisualizer):
    """
    Cross-Domain Relationship Visualizer

    Generates visualizations of relationships across:
    - Academic papers
    - GitHub repositories
    - Community discussions
    """

    def __init__(
        self,
        graph_data: Dict[str, Any],
        config: Optional[VisualizationConfig] = None
    ):
        """
        Initialize cross-domain visualizer.

        Args:
            graph_data: Graph data with nodes and edges from CrossDomainTracker
            config: Visualization configuration
        """
        super().__init__(config)
        self.nodes = graph_data.get("nodes", [])
        self.edges = graph_data.get("edges", [])

    def render(self, output_path: str, format: VisualizationFormat = VisualizationFormat.HTML) -> str:
        """Render cross-domain visualization"""
        if format == VisualizationFormat.HTML:
            return self._render_html(output_path)
        elif format == VisualizationFormat.MERMAID:
            return self._render_mermaid(output_path)
        else:
            return self._render_html(output_path)

    def _render_html(self, output_path: str) -> str:
        """Render interactive HTML using pyvis"""
        if not PYVIS_AVAILABLE:
            return self._render_fallback_html(output_path)

        net = Network(
            height=self.config.height,
            width=self.config.width,
            bgcolor=self.config.bgcolor,
            font_color=self.config.font_color,
            directed=True,
            cdn_resources=self.config.cdn_resources
        )

        # Configure for cross-domain layout
        net.set_options("""
        {
            "physics": {
                "enabled": true,
                "barnesHut": {
                    "gravitationalConstant": -8000,
                    "centralGravity": 0.3,
                    "springLength": 200,
                    "springConstant": 0.04,
                    "damping": 0.09
                }
            },
            "nodes": {
                "font": {"size": 14}
            },
            "edges": {
                "smooth": {"type": "continuous"},
                "arrows": {"to": {"enabled": true, "scaleFactor": 0.5}}
            }
        }
        """)

        # Add nodes with domain-specific styling
        for node in self.nodes:
            node_type = node.get("type", "unknown")
            color = self._get_color_for_domain(node_type)
            shape = self._get_shape_for_domain(node_type)

            net.add_node(
                node["id"],
                label=node.get("label", node["id"])[:30],
                title=node.get("metadata", {}).get("title", node["id"]),
                color=color,
                shape=shape,
                size=self.config.size_medium,
                group=node_type
            )

        # Add edges
        for edge in self.edges:
            net.add_edge(
                edge["source"],
                edge["target"],
                label=edge.get("type", ""),
                title=edge.get("evidence", "")
            )

        net.save_graph(output_path)
        return output_path

    def _render_fallback_html(self, output_path: str) -> str:
        """Generate simple HTML fallback"""
        # Group nodes by domain
        by_domain = {"paper": [], "repo": [], "community": []}
        for node in self.nodes:
            node_type = node.get("type", "unknown")
            by_domain.setdefault(node_type, []).append(node)

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Cross-Domain Relationship Network</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .warning {{ background: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .domain-section {{ margin: 20px 0; }}
        .domain-title {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
        .paper-title {{ color: #3498db; }}
        .repo-title {{ color: #2ecc71; }}
        .community-title {{ color: #e67e22; }}
        .entity {{ border: 1px solid #eee; padding: 10px; margin: 5px 0; border-radius: 4px; }}
        .legend {{ display: flex; gap: 20px; margin: 20px 0; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; }}
        .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    </style>
</head>
<body>
    <h2>Cross-Domain Relationship Network</h2>
    <div class="warning">
        <strong>Note:</strong> Interactive visualization requires pyvis library.
        Install with: pip install pyvis
    </div>
    <div class="legend">
        <div class="legend-item"><span class="dot" style="background:#3498db"></span> Papers</div>
        <div class="legend-item"><span class="dot" style="background:#2ecc71"></span> Repos</div>
        <div class="legend-item"><span class="dot" style="background:#e67e22"></span> Community</div>
    </div>
"""

        # Add sections for each domain
        for domain, title in [("paper", "Academic Papers"), ("repo", "GitHub Repositories"), ("community", "Community Discussions")]:
            if domain in by_domain and by_domain[domain]:
                html_content += f'<div class="domain-section">'
                html_content += f'<div class="domain-title {domain}-title">{title} ({len(by_domain[domain])})</div>'
                for node in by_domain[domain]:
                    html_content += f'<div class="entity">{node.get("label", node["id"])}</div>'
                html_content += '</div>'

        html_content += """
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output_path

    def _render_mermaid(self, output_path: str) -> str:
        """Generate Mermaid diagram for cross-domain graph"""
        lines = ["graph TD"]

        # Add nodes with domain-specific styling
        for node in self.nodes:
            node_id = node["id"].replace("-", "_").replace("/", "_")[:20]
            label = node.get("label", node["id"]).replace('"', "'")[:30]
            node_type = node.get("type", "unknown")

            if node_type == "paper":
                lines.append(f'    {node_id}["{label}"]:::paper')
            elif node_type == "repo":
                lines.append(f'    {node_id}["{label}"]:::repo')
            elif node_type == "community":
                lines.append(f'    {node_id}["{label}"]:::community')

        # Add edges
        for edge in self.edges:
            source = edge["source"].replace("-", "_").replace("/", "_")[:20]
            target = edge["target"].replace("-", "_").replace("/", "_")[:20]
            label = edge.get("type", "")
            if label:
                lines.append(f'    {source} -->|{label}| {target}')
            else:
                lines.append(f'    {source} --> {target}')

        # Add styles
        lines.append("""
    classDef paper fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    classDef repo fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff
    classDef community fill:#e67e22,stroke:#d35400,stroke-width:2px,color:#fff
""")

        mermaid_diagram = "\n".join(lines)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_diagram)

        return output_path

    def _get_color_for_domain(self, domain: str) -> str:
        """Get color for domain type"""
        colors = {
            "paper": self.config.color_paper,
            "repo": self.config.color_repo,
            "community": self.config.color_community,
            "concept": self.config.color_concept,
            "author": self.config.color_author,
            "framework": self.config.color_framework
        }
        return colors.get(domain, "#95a5a6")

    def _get_shape_for_domain(self, domain: str) -> str:
        """Get shape for domain type"""
        shapes = {
            "paper": "dot",
            "repo": "square",
            "community": "diamond",
            "concept": "triangle",
            "author": "ellipse"
        }
        return shapes.get(domain, "dot")

    def render_bipartite(self, domain_a: str, domain_b: str, output_path: str) -> str:
        """
        Render bipartite graph between two domains.

        Args:
            domain_a: First domain (e.g., "paper")
            domain_b: Second domain (e.g., "repo")
            output_path: Output file path

        Returns:
            Path to generated file
        """
        if not PYVIS_AVAILABLE:
            return self._render_html(output_path)

        net = Network(
            height=self.config.height,
            width=self.config.width,
            bgcolor=self.config.bgcolor,
            font_color=self.config.font_color,
            directed=True,
            cdn_resources=self.config.cdn_resources
        )

        # Bipartite layout options
        net.set_options("""
        {
            "layout": {
                "hierarchical": {
                    "enabled": true,
                    "direction": "LR",
                    "sortMethod": "directed"
                }
            },
            "physics": {
                "enabled": false
            }
        }
        """)

        # Add nodes from both domains
        for node in self.nodes:
            if node.get("type") in [domain_a, domain_b]:
                net.add_node(
                    node["id"],
                    label=node.get("label", node["id"])[:30],
                    color=self._get_color_for_domain(node.get("type", "")),
                    shape=self._get_shape_for_domain(node.get("type", "")),
                    group=node.get("type", "")
                )

        # Add edges between domains
        for edge in self.edges:
            source_type = next((n.get("type") for n in self.nodes if n["id"] == edge["source"]), "")
            target_type = next((n.get("type") for n in self.nodes if n["id"] == edge["target"]), "")

            if {source_type, target_type} == {domain_a, domain_b}:
                net.add_edge(edge["source"], edge["target"])

        net.save_graph(output_path)
        return output_path


class VisualizationBuilder:
    """
    Unified visualization builder for Deep Research System.

    Automatically generates all visualizations from research data
    and provides HTML embed codes for report integration.
    """

    def __init__(
        self,
        research_data_dir: str = "research_data",
        output_dir: str = "research_output/visualizations",
        config: Optional[VisualizationConfig] = None
    ):
        """
        Initialize visualization builder.

        Args:
            research_data_dir: Directory containing research data JSON files
            output_dir: Directory for output visualization files
            config: Visualization configuration
        """
        self.research_data_dir = Path(research_data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = config or VisualizationConfig()

        # Import cross_domain_tracker
        try:
            from cross_domain_tracker import CrossDomainTracker
            self._tracker_available = True
        except ImportError:
            self._tracker_available = False

    def generate_all(self) -> Dict[str, str]:
        """
        Generate all visualizations from research data.

        Returns:
            Dictionary with visualization types and their HTML embed codes
        """
        embeds = {}

        # Try to load research data
        if not self.research_data_dir.exists():
            print(f"Warning: Research data directory not found: {self.research_data_dir}")
            return embeds

        # Load citation network
        citation_html = self._generate_citation_network()
        if citation_html:
            embeds["citation_network"] = self._get_embed_code(citation_html, "Citation Network")

        # Load cross-domain graph
        if self._tracker_available:
            cross_domain_html = self._generate_cross_domain_network()
            if cross_domain_html:
                embeds["cross_domain"] = self._get_embed_code(cross_domain_html, "Cross-Domain Relationships")

        return embeds

    def _generate_citation_network(self) -> Optional[str]:
        """Generate citation network visualization"""
        # Try to load from logic_analysis or academic research
        papers = []
        citations = []

        # Load from academic research
        academic_file = self.research_data_dir / "academic_research_output.json"
        if academic_file.exists():
            with open(academic_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for paper in data.get("papers", []):
                papers.append(paper)
                # Add citations
                for cited in paper.get("cites", []):
                    citations.append((paper.get("arxiv_id", ""), cited))

        # Load from logic analysis for citation chains
        logic_file = self.research_data_dir / "logic_analysis.json"
        if logic_file.exists():
            with open(logic_file, 'r', encoding='utf-8') as f:
                logic_data = json.load(f)

            # Extract citation relationships
            for paper_id, paper_data in logic_data.get("papers", {}).items():
                for related in paper_data.get("cites", []):
                    citations.append((paper_id, related))

        if not papers:
            return None

        output_path = self.output_dir / "citation_network.html"

        visualizer = CitationNetworkVisualizer(
            papers=papers,
            citations=citations,
            config=self.config
        )

        return visualizer._render_html(str(output_path))

    def _generate_cross_domain_network(self) -> Optional[str]:
        """Generate cross-domain relationship visualization"""
        try:
            from cross_domain_tracker import CrossDomainTracker

            tracker = CrossDomainTracker()
            tracker.load_from_research_data(str(self.research_data_dir))

            graph_data = tracker.get_cross_domain_graph()

            if not graph_data["nodes"]:
                return None

            output_path = self.output_dir / "cross_domain_network.html"

            visualizer = CrossDomainVisualizer(
                graph_data=graph_data,
                config=self.config
            )

            return visualizer._render_html(str(output_path))

        except Exception as e:
            print(f"Warning: Failed to generate cross-domain visualization: {e}")
            return None

    def _get_embed_code(self, html_path: str, title: str) -> str:
        """Generate HTML iframe embed code"""
        rel_path = Path(html_path).relative_to(self.output_dir.parent.parent)
        return f'<iframe src="{rel_path}" width="100%" height="600" frameborder="0" title="{title}"></iframe>'

    def get_legend_html(self) -> str:
        """Generate HTML legend for visualization node types"""
        return """
<div class="visualization-legend" style="display: flex; gap: 20px; margin: 15px 0; flex-wrap: wrap;">
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="width: 16px; height: 16px; background: #3498db; border-radius: 50%;"></span>
        <span>Academic Paper / 论文</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="width: 16px; height: 16px; background: #2ecc71; border-radius: 2px;"></span>
        <span>GitHub Repo / 代码库</span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <span style="width: 16px; height: 16px; background: #e67e22; transform: rotate(45deg);"></span>
        <span>Community Discussion / 社区讨论</span>
    </div>
</div>
"""


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Agent Research Visualization System")
    parser.add_argument("--data-dir", type=str, default="research_data",
                        help="Research data directory")
    parser.add_argument("--output-dir", type=str, default="research_output/visualizations",
                        help="Output directory for visualizations")
    parser.add_argument("--test", action="store_true",
                        help="Generate test visualizations with sample data")
    parser.add_argument("--format", type=str, default="html",
                        choices=["html", "png", "svg", "mermaid"],
                        help="Output format")

    args = parser.parse_args()

    builder = VisualizationBuilder(
        research_data_dir=args.data_dir,
        output_dir=args.output_dir
    )

    if args.test:
        print("Generating test visualizations...")

        # Create sample data
        sample_papers = [
            {"arxiv_id": "2308.00352", "title": "MetaGPT: Meta Programming for AI", "type": "sota"},
            {"arxiv_id": "2308.08155", "title": "AutoGen: Multi-Agent Conversation", "type": "sota"},
            {"arxiv_id": "2506.12508", "title": "AgentOrchestra: Hierarchical Framework", "type": "sota"},
        ]

        sample_citations = [
            ("2506.12508", "2308.00352"),
            ("2506.12508", "2308.08155"),
        ]

        # Generate citation network
        viz = CitationNetworkVisualizer(sample_papers, sample_citations)
        viz.render(str(Path(args.output_dir) / "test_citation.html"), VisualizationFormat.HTML)
        print(f"Test citation network: {Path(args.output_dir) / 'test_citation.html'}")

    else:
        # Generate all visualizations from research data
        embeds = builder.generate_all()

        print(f"Generated {len(embeds)} visualizations:")
        for name, embed in embeds.items():
            print(f"  - {name}")
