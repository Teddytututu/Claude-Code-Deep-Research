"""
Multi-Graph Agentic Memory (MAGMA) v9.0
Knowledge Graph Implementation with NetworkX

Based on: MAGMA: Multi-Graph Agentic Memory Architecture (arXiv:2601.03236)

This module implements the semantic memory layer as a knowledge graph
connecting papers, projects, discussions, and concepts.

Author: Deep Research System
Date: 2026-02-09
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False


class NodeType(Enum):
    """Types of nodes in the knowledge graph"""
    ACADEMIC_PAPER = "academic_paper"
    GITHUB_PROJECT = "github_project"
    COMMUNITY_DISCUSSION = "community_discussion"
    CONCEPT = "concept"
    AUTHOR = "author"
    FRAMEWORK = "framework"
    TECHNIQUE = "technique"
    DATASET = "dataset"
    METRIC = "metric"


class EdgeType(Enum):
    """Types of relationships in the knowledge graph"""
    CITES = "cites"  # Paper cites another paper
    IMPLEMENTS = "implements"  # Project implements paper
    DISCUSSES = "discusses"  # Discussion discusses paper/project
    RELATED_TO = "related_to"  # General relatedness
    AUTHORED_BY = "authored_by"  # Paper authored by
    USES_FRAMEWORK = "uses_framework"  # Project uses framework
    INTRODUCES = "introduces"  # Paper introduces concept/technique
    EVALUATES_ON = "evaluates_on"  # Paper evaluates on dataset
    OPTIMIZES = "optimizes"  # Paper optimizes metric
    SIMILAR_TO = "similar_to"  # Semantic similarity


@dataclass
class GraphNode:
    """Node in the knowledge graph"""
    id: str
    type: NodeType
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "attributes": self.attributes
        }


@dataclass
class GraphEdge:
    """Edge in the knowledge graph"""
    source: str
    target: str
    type: EdgeType
    attributes: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "type": self.type.value,
            "attributes": self.attributes,
            "weight": self.weight
        }


class SemanticMemory:
    """
    Semantic Memory Layer - Knowledge Graph Implementation

    Stores research findings as a connected graph of entities:
    - Papers connected by citations
    - Projects connected by implementations
    - Discussions connected by references
    - Concepts connected by co-occurrence
    """

    def __init__(self, use_networkx: bool = True, output_dir: str = "research_output/visualizations"):
        """
        Initialize semantic memory.

        Args:
            use_networkx: Use NetworkX for graph operations (requires networkx)
            output_dir: Directory for visualization outputs
        """
        self.use_networkx = use_networkx and NETWORKX_AVAILABLE
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        """
        Initialize semantic memory.

        Args:
            use_networkx: Use NetworkX for graph operations (requires networkx)
        """
        self.use_networkx = use_networkx and NETWORKX_AVAILABLE

        if self.use_networkx:
            self.graph = nx.MultiDiGraph()
        else:
            # Fallback to simple adjacency list representation
            self._adjacency: Dict[str, Dict[str, List[GraphEdge]]] = defaultdict(lambda: defaultdict(list))

        self._nodes: Dict[str, GraphNode] = {}
        self._edges: List[GraphEdge] = []

    def add_node(self, node: GraphNode) -> None:
        """Add a node to the graph"""
        self._nodes[node.id] = node

        if self.use_networkx:
            self.graph.add_node(node.id, **node.attributes, node_type=node.type.value)

    def add_edge(self, edge: GraphEdge) -> None:
        """Add an edge to the graph"""
        self._edges.append(edge)

        if self.use_networkx:
            self.graph.add_edge(
                edge.source,
                edge.target,
                key=edge.type.value,
                **edge.attributes,
                edge_type=edge.type.value,
                weight=edge.weight
            )
        else:
            self._adjacency[edge.source][edge.target].append(edge)

    def add_paper(self, paper_data: Dict[str, Any]) -> str:
        """
        Add an academic paper to the graph.

        Args:
            paper_data: Paper data with arxiv_id, title, authors, etc.

        Returns:
            Node ID of the paper
        """
        arxiv_id = paper_data.get("arxiv_id", paper_data.get("id", ""))
        if not arxiv_id:
            return ""

        # Create paper node
        paper_node = GraphNode(
            id=f"paper_{arxiv_id}",
            type=NodeType.ACADEMIC_PAPER,
            attributes={
                "arxiv_id": arxiv_id,
                "title": paper_data.get("title", ""),
                "authors": paper_data.get("authors", []),
                "year": paper_data.get("year"),
                "venue": paper_data.get("venue"),
                "abstract": paper_data.get("abstract", ""),
                "citation_count": paper_data.get("citation_count", 0),
                "url": paper_data.get("url", ""),
                "url_markdown": paper_data.get("url_markdown", ""),
                "type_category": paper_data.get("type", "sota")  # root, sota, survey
            }
        )
        self.add_node(paper_node)

        # Add author nodes and edges
        for author in paper_data.get("authors", []):
            author_id = f"author_{author.lower().replace(' ', '_')}"
            author_node = GraphNode(
                id=author_id,
                type=NodeType.AUTHOR,
                attributes={"name": author}
            )
            self.add_node(author_node)

            edge = GraphEdge(
                source=paper_node.id,
                target=author_id,
                type=EdgeType.AUTHORED_BY,
                weight=1.0
            )
            self.add_edge(edge)

        # Add concepts as nodes
        for concept in paper_data.get("key_concepts", []):
            concept_id = f"concept_{concept.lower().replace(' ', '_')}"
            concept_node = GraphNode(
                id=concept_id,
                type=NodeType.CONCEPT,
                attributes={"name": concept}
            )
            self.add_node(concept_node)

            edge = GraphEdge(
                source=paper_node.id,
                target=concept_id,
                type=EdgeType.INTRODUCES,
                attributes={"context": "paper discusses concept"},
                weight=1.0
            )
            self.add_edge(edge)

        return paper_node.id

    def add_project(self, project_data: Dict[str, Any]) -> str:
        """
        Add a GitHub project to the graph.

        Args:
            project_data: Project data with name, stars, etc.

        Returns:
            Node ID of the project
        """
        name = project_data.get("name", "")
        if not name:
            return ""

        # Create project node
        project_node = GraphNode(
            id=f"project_{name.replace('/', '_')}",
            type=NodeType.GITHUB_PROJECT,
            attributes={
                "name": name,
                "description": project_data.get("description", ""),
                "stars": project_data.get("stars_display", ""),
                "language": project_data.get("language", ""),
                "license": project_data.get("license", ""),
                "url": f"https://github.com/{name}",
                "url_markdown": project_data.get("url_markdown", ""),
                "framework_type": project_data.get("framework_type", "")
            }
        )
        self.add_node(project_node)

        # Add framework edge if specified
        framework = project_data.get("framework_type")
        if framework:
            framework_id = f"framework_{framework.lower()}"
            framework_node = GraphNode(
                id=framework_id,
                type=NodeType.FRAMEWORK,
                attributes={"name": framework}
            )
            self.add_node(framework_node)

            edge = GraphEdge(
                source=project_node.id,
                target=framework_id,
                type=EdgeType.USES_FRAMEWORK,
                weight=1.0
            )
            self.add_edge(edge)

        # Add implementation edges to papers
        for paper_id in project_data.get("implements_papers", []):
            paper_node_id = f"paper_{paper_id}"
            edge = GraphEdge(
                source=project_node.id,
                target=paper_node_id,
                type=EdgeType.IMPLEMENTS,
                weight=1.0
            )
            self.add_edge(edge)

        return project_node.id

    def add_discussion(self, discussion_data: Dict[str, Any]) -> str:
        """
        Add a community discussion to the graph.

        Args:
            discussion_data: Discussion data with platform, title, etc.

        Returns:
            Node ID of the discussion
        """
        url = discussion_data.get("url", "")
        platform = discussion_data.get("platform", "")

        # Create discussion node
        discussion_id = f"discussion_{platform}_{hash(url)}"
        discussion_node = GraphNode(
            id=discussion_id,
            type=NodeType.COMMUNITY_DISCUSSION,
            attributes={
                "platform": platform,
                "title": discussion_data.get("title", ""),
                "url": url,
                "url_markdown": discussion_data.get("url_markdown", ""),
                "consensus_level": discussion_data.get("consensus_level", ""),
                "upvotes": discussion_data.get("upvotes", 0)
            }
        )
        self.add_node(discussion_node)

        # Add discussion edges to papers/projects mentioned
        for paper_id in discussion_data.get("papers_discussed", []):
            paper_node_id = f"paper_{paper_id}"
            edge = GraphEdge(
                source=discussion_node.id,
                target=paper_node_id,
                type=EdgeType.DISCUSSES,
                weight=1.0
            )
            self.add_edge(edge)

        return discussion_node.id

    def add_citation_edge(self, citing_paper: str, cited_paper: str) -> None:
        """
        Add a citation edge between two papers.

        Args:
            citing_paper: ArXiv ID of citing paper
            cited_paper: ArXiv ID of cited paper
        """
        citing_id = f"paper_{citing_paper}"
        cited_id = f"paper_{cited_paper}"

        edge = GraphEdge(
            source=citing_id,
            target=cited_id,
            type=EdgeType.CITES,
            weight=1.0
        )
        self.add_edge(edge)

    def get_neighbors(
        self,
        node_id: str,
        edge_type: Optional[EdgeType] = None,
        max_depth: int = 1
    ) -> List[str]:
        """
        Get neighboring nodes.

        Args:
            node_id: Starting node ID
            edge_type: Filter by edge type (optional)
            max_depth: Maximum depth to traverse

        Returns:
            List of neighboring node IDs
        """
        neighbors = set()
        frontier = {node_id}

        for _ in range(max_depth):
            next_frontier = set()
            for current in frontier:
                if self.use_networkx:
                    for successor in self.graph.successors(current):
                        if edge_type is None:
                            neighbors.add(successor)
                        else:
                            edge_data = self.graph.get_edge_data(current, successor)
                            if edge_data and any(e.get("edge_type") == edge_type.value for e in edge_data.values()):
                                neighbors.add(successor)
                        next_frontier.add(successor)
                else:
                    for target, edges in self._adjacency.get(current, {}).items():
                        if edge_type is None or any(e.type == edge_type for e in edges):
                            neighbors.add(target)
                        next_frontier.add(target)
            frontier = next_frontier

        return list(neighbors)

    def find_shortest_path(self, source: str, target: str) -> List[str]:
        """
        Find shortest path between two nodes.

        Args:
            source: Source node ID
            target: Target node ID

        Returns:
            List of node IDs forming the path
        """
        if self.use_networkx:
            try:
                return nx.shortest_path(self.graph, source, target)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                return []
        else:
            # Simple BFS for fallback
            from collections import deque
            queue = deque([(source, [source])])
            visited = {source}

            while queue:
                current, path = queue.popleft()
                if current == target:
                    return path

                for neighbor in self._adjacency.get(current, {}):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

            return []

    def get_pagerank(self, alpha: float = 0.85) -> Dict[str, float]:
        """
        Calculate PageRank for all nodes.

        Args:
            alpha: Damping parameter

        Returns:
            Dictionary of node ID to PageRank score
        """
        if self.use_networkx:
            return nx.pagerank(self.graph, alpha=alpha)
        else:
            # Fallback: return degree centrality
            centrality = {}
            for node_id in self._nodes:
                centrality[node_id] = len(self._adjacency.get(node_id, {}))
            return centrality

    def find_related_papers(self, paper_id: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find papers related to a given paper.

        Args:
            paper_id: ArXiv ID of the paper
            top_k: Number of related papers to return

        Returns:
            List of (paper_id, relevance_score) tuples
        """
        node_id = f"paper_{paper_id}"

        # Get neighbors through various relationship types
        related = defaultdict(float)

        # Direct citations
        for neighbor in self.get_neighbors(node_id, EdgeType.CITES):
            related[neighbor] += 1.0

        # Shared concepts (2-hop)
        concept_neighbors = self.get_neighbors(node_id, EdgeType.INTRODUCES)
        for concept in concept_neighbors:
            for paper in self.get_neighbors(concept, EdgeType.INTRODUCES):
                if paper != node_id and paper.startswith("paper_"):
                    related[paper] += 0.5

        # Convert to list and sort by relevance
        related_list = [(nid.replace("paper_", ""), score) for nid, score in related.items()]
        related_list.sort(key=lambda x: x[1], reverse=True)

        return related_list[:top_k]

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation"""
        return {
            "nodes": [node.to_dict() for node in self._nodes.values()],
            "edges": [edge.to_dict() for edge in self._edges],
            "stats": {
                "node_count": len(self._nodes),
                "edge_count": len(self._edges),
                "node_types": self._count_node_types(),
                "edge_types": self._count_edge_types()
            }
        }

    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type"""
        counts = defaultdict(int)
        for node in self._nodes.values():
            counts[node.type.value] += 1
        return dict(counts)

    def _count_edge_types(self) -> Dict[str, int]:
        """Count edges by type"""
        counts = defaultdict(int)
        for edge in self._edges:
            counts[edge.type.value] += 1
        return dict(counts)

    def save(self, filepath: str) -> None:
        """Save graph to JSON file"""
        data = self.to_dict()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: str, use_networkx: bool = True) -> 'SemanticMemory':
        """Load graph from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        memory = cls(use_networkx=use_networkx)

        # Load nodes
        for node_data in data.get("nodes", []):
            node = GraphNode(
                id=node_data["id"],
                type=NodeType(node_data["type"]),
                attributes=node_data.get("attributes", {})
            )
            memory.add_node(node)

        # Load edges
        for edge_data in data.get("edges", []):
            edge = GraphEdge(
                source=edge_data["source"],
                target=edge_data["target"],
                type=EdgeType(edge_data["type"]),
                attributes=edge_data.get("attributes", {}),
                weight=edge_data.get("weight", 1.0)
            )
            memory.add_edge(edge)

        return memory

    def to_mermaid(self) -> str:
        """
        Generate Mermaid diagram string from graph.

        Returns:
            Mermaid diagram string for markdown embedding
        """
        lines = ["graph TD"]

        # Add nodes by type
        for node_id, node in self._nodes.items():
            label = node.attributes.get("title", node.attributes.get("name", node_id))
            label = label.replace('"', "'")[:40]  # Truncate and escape
            safe_id = node_id.replace("-", "_").replace("/", "_")[:20]

            # Style by node type
            if node.type == NodeType.ACADEMIC_PAPER:
                type_cat = node.attributes.get("type_category", "sota")
                if type_cat == "root":
                    lines.append(f'    {safe_id}["{label}"]:::rootPaper')
                elif type_cat == "survey":
                    lines.append(f'    {safe_id}["{label}"]:::surveyPaper')
                else:
                    lines.append(f'    {safe_id}["{label}"]:::sotaPaper')
            elif node.type == NodeType.GITHUB_PROJECT:
                lines.append(f'    {safe_id}["{label}"]:::repo')
            elif node.type == NodeType.COMMUNITY_DISCUSSION:
                lines.append(f'    {safe_id}["{label}"]:::community')
            else:
                lines.append(f'    {safe_id}["{label}"]')

        # Add edges
        for edge in self._edges:
            source = edge.source.replace("-", "_").replace("/", "_")[:20]
            target = edge.target.replace("-", "_").replace("/", "_")[:20]

            if edge.type == EdgeType.CITES:
                lines.append(f'    {source} -->|cites| {target}')
            elif edge.type == EdgeType.IMPLEMENTS:
                lines.append(f'    {source} -->|implements| {target}')
            elif edge.type == EdgeType.DISCUSSES:
                lines.append(f'    {source} -->|discusses| {target}')
            else:
                lines.append(f'    {source} --> {target}')

        # Add style definitions
        lines.append("""
    classDef rootPaper fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    classDef sotaPaper fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    classDef surveyPaper fill:#f39c12,stroke:#e67e22,stroke-width:2px,color:#fff
    classDef repo fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:#fff
    classDef community fill:#e67e22,stroke:#d35400,stroke-width:2px,color:#fff
""")

        return "\n".join(lines)

    def export_graphml(self, filepath: str) -> None:
        """
        Export graph to GraphML format (Gephi compatible).

        Args:
            filepath: Output file path
        """
        if not self.use_networkx:
            raise RuntimeError("NetworkX required for GraphML export")

        # Convert to undirected for Gephi compatibility (optional)
        G = self.graph.to_undirected() if filepath.endswith(".graphml") else self.graph

        nx.write_graphml(G, filepath)

    def export_gexf(self, filepath: str) -> None:
        """
        Export graph to GEXF format (Gephi compatible).

        Args:
            filepath: Output file path
        """
        if not self.use_networkx:
            raise RuntimeError("NetworkX required for GEXF export")

        nx.write_gexf(self.graph, filepath)

    def visualize(
        self,
        output_path: str = "",
        format: str = "html",
        height: str = "600px",
        width: str = "100%"
    ) -> str:
        """
        Render graph visualization to file.

        Args:
            output_path: Output file path (default: auto-generated)
            format: Output format (html, png, svg)
            height: Height for HTML output
            width: Width for HTML output

        Returns:
            Path to generated file
        """
        if not self.use_networkx:
            raise RuntimeError("NetworkX required for visualization")

        # Generate output path if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = str(self.output_dir / f"graph_{timestamp}.{format}")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "html":
            return self._render_html(str(output_path), height, width)
        elif format in ("png", "svg"):
            return self._render_image(str(output_path), format)
        elif format == "mermaid":
            mermaid_content = self.to_mermaid()
            with open(output_path, 'w') as f:
                f.write(mermaid_content)
            return str(output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _render_html(self, output_path: str, height: str, width: str) -> str:
        """Render interactive HTML visualization"""
        try:
            from pyvis.network import Network

            net = Network(
                height=height,
                width=width,
                bgcolor="#ffffff",
                font_color="#000000",
                directed=True
            )

            # Configure for hierarchical layout
            net.set_options("""
            {
                "layout": {
                    "hierarchical": {
                        "enabled": true,
                        "direction": "UD",
                        "sortMethod": "directed"
                    }
                },
                "physics": {
                    "enabled": false
                }
            }
            """)

            # Add nodes
            for node_id, node_data in self.graph.nodes(data=True):
                node_type = node_data.get("node_type", "unknown")
                color = self._get_color_for_type(node_type)
                label = node_data.get("title", node_data.get("name", node_id))[:30]

                net.add_node(
                    node_id,
                    label=label,
                    title=node_data.get("title", node_id),
                    color=color,
                    shape="dot" if node_type == "academic_paper" else "square",
                    group=node_type
                )

            # Add edges
            for source, target, edge_data in self.graph.edges(data=True):
                net.add_edge(source, target, label=edge_data.get("edge_type", ""))

            net.save_graph(output_path)
            return output_path

        except ImportError:
            # Fallback: export as Mermaid
            fallback_path = output_path.replace(".html", "_fallback.mmd")
            return self._render_mermaid_fallback(fallback_path)

    def _render_image(self, output_path: str, format: str) -> str:
        """Render static image using matplotlib"""
        try:
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots(figsize=(14, 10))

            # Use hierarchical layout
            try:
                pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot')
            except:
                pos = nx.spring_layout(self.graph, k=2, iterations=50)

            # Group nodes by type
            node_types = {}
            for node, data in self.graph.nodes(data=True):
                node_type = data.get("node_type", "unknown")
                node_types.setdefault(node_type, []).append(node)

            # Draw nodes by type
            for node_type, nodes in node_types.items():
                nx.draw_networkx_nodes(
                    self.graph, pos, nodelist=nodes,
                    node_color=self._get_color_for_type(node_type),
                    label=node_type.replace("_", " ").title(),
                    node_size=300, ax=ax
                )

            # Draw edges
            nx.draw_networkx_edges(self.graph, pos, alpha=0.4, arrows=True, ax=ax)

            # Draw labels
            labels = {n: d.get("title", d.get("name", n))[:15]
                     for n, d in self.graph.nodes(data=True)}
            nx.draw_networkx_labels(self.graph, pos, labels, font_size=8, ax=ax)

            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.set_title("Knowledge Graph Visualization")
            plt.axis('off')

            fig.savefig(output_path, format=format, dpi=150, bbox_inches='tight')
            plt.close()

            return output_path

        except ImportError:
            raise RuntimeError("matplotlib required for image export")

    def _render_mermaid_fallback(self, output_path: str) -> str:
        """Generate Mermaid diagram as fallback"""
        mermaid_content = self.to_mermaid()
        with open(output_path, 'w') as f:
            f.write(mermaid_content)
        return output_path

    def _get_color_for_type(self, node_type: str) -> str:
        """Get color for node type"""
        colors = {
            "academic_paper": "#3498db",  # Blue
            "github_project": "#2ecc71",  # Green
            "community_discussion": "#e67e22",  # Orange
            "concept": "#9b59b6",  # Purple
            "author": "#95a5a6",  # Gray
            "framework": "#e74c3c"  # Red
        }
        return colors.get(node_type, "#95a5a6")

    def to_html(
        self,
        output_path: str = "",
        title: str = "Knowledge Graph",
        height: str = "600px"
    ) -> str:
        """
        Generate interactive HTML visualization.

        Args:
            output_path: Output file path
            title: Graph title
            height: iframe height

        Returns:
            Path to generated HTML file
        """
        return self.visualize(output_path, format="html", height=height)


class CitationNetwork:
    """
    Citation Network Builder and Analyzer

    Builds and analyzes citation relationships between papers.
    """

    def __init__(self, semantic_memory: SemanticMemory):
        """
        Initialize citation network.

        Args:
            semantic_memory: The semantic memory graph
        """
        self.memory = semantic_memory
        self._root_papers: Set[str] = set()
        self._survey_papers: Set[str] = set()

    def add_paper_with_citations(
        self,
        paper_id: str,
        cites: List[str],
        paper_type: str = "sota"
    ) -> None:
        """
        Add a paper with its citation relationships.

        Args:
            paper_id: ArXiv ID of the paper
            cites: List of ArXiv IDs that this paper cites
            paper_type: Type of paper (root, sota, survey)
        """
        # Categorize paper
        if paper_type == "root":
            self._root_papers.add(paper_id)
        elif paper_type == "survey":
            self._survey_papers.add(paper_id)

        # Add citation edges
        for cited in cites:
            self.memory.add_citation_edge(paper_id, cited)

    def get_citation_chain(self, paper_id: str, max_depth: int = 3) -> List[str]:
        """
        Get citation chain starting from a paper.

        Args:
            paper_id: Starting paper ArXiv ID
            max_depth: Maximum depth of chain

        Returns:
            List of ArXiv IDs in citation order
        """
        node_id = f"paper_{paper_id}"
        chain = []
        visited = set()

        def traverse(current_id: str, depth: int):
            if depth > max_depth or current_id in visited:
                return
            visited.add(current_id)
            chain.append(current_id.replace("paper_", ""))

            for neighbor in self.memory.get_neighbors(current_id, EdgeType.CITES):
                traverse(neighbor, depth + 1)

        traverse(node_id, 0)
        return chain

    def find_root_papers(self) -> List[str]:
        """Get papers that are roots of citation chains"""
        return list(self._root_papers)

    def find_survey_papers(self) -> List[str]:
        """Get survey/review papers"""
        return list(self._survey_papers)

    def build_citation_network_summary(self) -> Dict[str, Any]:
        """
        Build a summary of the citation network.

        Returns:
            Dictionary with network statistics and structure
        """
        pagerank = self.memory.get_pagerank()

        # Get top papers by PageRank
        paper_scores = [
            (nid.replace("paper_", ""), score)
            for nid, score in pagerank.items()
            if nid.startswith("paper_")
        ]
        paper_scores.sort(key=lambda x: x[1], reverse=True)

        return {
            "root_papers": list(self._root_papers),
            "survey_papers": list(self._survey_papers),
            "top_papers_by_importance": paper_scores[:10],
            "network_stats": {
                "total_papers": len([n for n in self.memory._nodes if n.startswith("paper_")]),
                "total_citations": len([e for e in self.memory._edges if e.type == EdgeType.CITES])
            }
        }


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MAGMA Memory Graph System")
    parser.add_argument("--build", action="store_true", help="Build graph from research data")
    parser.add_argument("--query", type=str, help="Query related papers")
    parser.add_argument("--load", type=str, help="Load graph from file")
    parser.add_argument("--save", type=str, help="Save graph to file")
    parser.add_argument("--stats", action="store_true", help="Show graph statistics")

    args = parser.parse_args()

    memory = SemanticMemory()

    if args.load:
        memory = SemanticMemory.load(args.load)
        print(f"Loaded graph with {len(memory._nodes)} nodes and {len(memory._edges)} edges")

    if args.stats:
        stats = memory.to_dict()["stats"]
        print(json.dumps(stats, indent=2))

    if args.query:
        related = memory.find_related_papers(args.query)
        print(f"Papers related to {args.query}:")
        for paper_id, score in related:
            print(f"  {paper_id}: {score:.3f}")

    if args.save:
        memory.save(args.save)
        print(f"Graph saved to {args.save}")
