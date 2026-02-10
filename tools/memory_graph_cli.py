"""
Memory Graph CLI v1.0
记忆图谱命令行工具

Unified CLI for memory graph operations including building, querying,
visualizing, and analyzing the semantic knowledge graph.

Usage:
    python "tools\\memory_graph_cli.py" --build
    python "tools\\memory_graph_cli.py" --query 2501.03236
    python "tools\\memory_graph_cli.py" --visualize --format html
    python "tools\\memory_graph_cli.py" --stats

Author: Deep Research System
Date: 2026-02-11
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_graph import SemanticMemory, CitationNetwork, NodeType, EdgeType
from memory_system import MAGMAMemory


def build_graph_from_research_data(data_dir: str = "research_data") -> MAGMAMemory:
    """
    Build memory graph from existing research data files.

    Args:
        data_dir: Directory containing research output JSON files

    Returns:
        MAGMAMemory instance with populated semantic graph
    """
    memory = MAGMAMemory(storage_dir=data_dir)
    data_path = Path(data_dir)

    # Load academic research output
    academic_file = data_path / "academic_research_output.json"
    if academic_file.exists():
        print(f"Loading academic research from {academic_file}")
        with open(academic_file, encoding='utf-8') as f:
            data = json.load(f)
            papers = data.get("papers", [])
            print(f"  Found {len(papers)} papers")
            for paper in papers:
                memory.add_paper_finding(paper, "academic-researcher")

    # Load GitHub research output
    github_file = data_path / "github_research_output.json"
    if github_file.exists():
        print(f"Loading GitHub research from {github_file}")
        with open(github_file, encoding='utf-8') as f:
            data = json.load(f)
            projects = data.get("projects", data.get("repositories", []))
            print(f"  Found {len(projects)} projects")
            for project in projects:
                memory.add_project_finding(project, "github-watcher")

    # Load community research output
    community_file = data_path / "community_research_output.json"
    if community_file.exists():
        print(f"Loading community research from {community_file}")
        with open(community_file, encoding='utf-8') as f:
            data = json.load(f)
            discussions = data.get("discussions", data.get("threads", []))
            print(f"  Found {len(discussions)} discussions")
            for discussion in discussions:
                memory.add_discussion_finding(discussion, "community-listener")

    # Save the semantic graph
    memory.save_semantic_graph()
    print(f"Graph saved to {data_path / 'semantic_graph.json'}")

    return memory


def load_or_build_memory(data_dir: str, build: bool = False) -> MAGMAMemory:
    """
    Load existing memory graph or build from research data.

    Args:
        data_dir: Directory containing research data
        build: Whether to rebuild from research data

    Returns:
        MAGMAMemory instance
    """
    memory = MAGMAMemory(storage_dir=data_dir)
    graph_file = Path(data_dir) / "semantic_graph.json"

    if build or not graph_file.exists():
        if not graph_file.exists():
            print(f"Graph file not found: {graph_file}")
            print("Building from research data...")
        return build_graph_from_research_data(data_dir)

    # Try to load existing graph
    try:
        memory.semantic = SemanticMemory.load(str(graph_file))
        print(f"Loaded graph from {graph_file}")
    except Exception as e:
        print(f"Failed to load graph: {e}")
        print("Building from research data...")
        return build_graph_from_research_data(data_dir)

    return memory


def show_stats(memory: MAGMAMemory) -> None:
    """Display graph statistics."""
    stats = memory.semantic.to_dict()["stats"]

    print("\n" + "=" * 50)
    print("MEMORY GRAPH STATISTICS")
    print("=" * 50)

    print(f"\nTotal Nodes: {stats['node_count']}")
    print(f"Total Edges: {stats['edge_count']}")

    print("\nNodes by Type:")
    for node_type, count in sorted(stats.get('node_types', {}).items()):
        print(f"  {node_type}: {count}")

    print("\nEdges by Type:")
    for edge_type, count in sorted(stats.get('edge_types', {}).items()):
        print(f"  {edge_type}: {count}")

    # Show top papers by PageRank if available
    try:
        pagerank = memory.semantic.get_pagerank()
        top_papers = sorted(
            [k for k in pagerank.keys() if k.startswith("paper_")],
            key=lambda x: pagerank[x],
            reverse=True
        )[:5]

        print("\nTop Papers by PageRank:")
        for paper_id in top_papers:
            node = memory.semantic._nodes.get(paper_id)
            if node:
                title = node.attributes.get("title", paper_id)
                score = pagerank[paper_id]
                print(f"  {score:.4f}: {title[:60]}...")
    except Exception as e:
        print(f"\nPageRank not available: {e}")

    print("=" * 50 + "\n")


def query_related_papers(memory: MAGMAMemory, arxiv_id: str, top_k: int = 10) -> None:
    """
    Query and display papers related to a given arXiv ID.

    Args:
        memory: MAGMAMemory instance
        arxiv_id: arXiv paper ID to find related papers for
        top_k: Number of related papers to display
    """
    # Normalize paper ID
    paper_id = arxiv_id if arxiv_id.startswith("paper_") else f"paper_{arxiv_id}"

    # Check if paper exists
    if paper_id not in memory.semantic._nodes:
        print(f"Paper {arxiv_id} not found in graph")
        print(f"Available papers starting with '{arxiv_id}':")
        for pid in sorted(memory.semantic._nodes.keys()):
            if pid.startswith("paper_") and arxiv_id in pid:
                node = memory.semantic._nodes[pid]
                title = node.attributes.get("title", "Unknown")
                print(f"  {pid}: {title[:60]}...")
        return

    # Get related papers
    related = memory.semantic.find_related_papers(arxiv_id, top_k=top_k)

    print(f"\nPapers related to {arxiv_id}:")
    print("-" * 50)

    if not related:
        print("No related papers found")
        # Show direct connections instead
        neighbors = memory.semantic.get_neighbors(paper_id, max_depth=1)
        if neighbors:
            print("\nDirect connections:")
            for neighbor_id in neighbors:
                node = memory.semantic._nodes.get(neighbor_id)
                if node:
                    node_type = node.type.value
                    name = node.attributes.get("title") or node.attributes.get("name") or neighbor_id
                    print(f"  [{node_type}] {name[:60]}...")
    else:
        for related_id, score in related:
            node = memory.semantic._nodes.get(f"paper_{related_id}")
            if node:
                title = node.attributes.get("title", related_id)
                print(f"  {score:.3f}: {related_id} - {title[:60]}...")
            else:
                print(f"  {score:.3f}: {related_id}")

    print("-" * 50 + "\n")


def visualize_graph(memory: MAGMAMemory, output_path: str, format_type: str) -> None:
    """
    Generate visualization of the memory graph.

    Args:
        memory: MAGMAMemory instance
        output_path: Path for output file
        format_type: Type of visualization (html, png, svg, mermaid)
    """
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating {format_type.upper()} visualization...")

    if format_type == "mermaid":
        # Generate Mermaid diagram
        mermaid_code = memory.semantic.to_mermaid()
        mermaid_path = output.with_suffix(".mmd")
        with open(mermaid_path, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        print(f"Mermaid diagram saved to {mermaid_path}")

    elif format_type == "html":
        try:
            html_path = memory.semantic.visualize(
                format="html",
                output_path=str(output)
            )
            print(f"HTML visualization saved to {html_path}")
            print(f"Open in browser: file:///{html_path.replace(os.sep, '/')}")
        except RuntimeError as e:
            print(f"HTML generation failed: {e}")
            print("Falling back to Mermaid diagram...")
            visualize_graph(memory, str(output), "mermaid")

    elif format_type in ("png", "svg"):
        try:
            output_path = memory.semantic.visualize(
                format=format_type,
                output_path=str(output)
            )
            print(f"{format_type.upper()} visualization saved to {output_path}")
        except RuntimeError as e:
            print(f"{format_type.upper()} generation failed: {e}")
            print("Falling back to Mermaid diagram...")
            visualize_graph(memory, str(output), "mermaid")

    elif format_type == "json":
        # Export full graph as JSON
        graph_dict = memory.semantic.to_dict()
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(graph_dict, f, indent=2, ensure_ascii=False)
        print(f"JSON export saved to {output}")


def export_graphml(memory: MAGMAMemory, output_path: str) -> None:
    """Export graph to GraphML format for Gephi."""
    try:
        memory.semantic.export_graphml(output_path)
        print(f"GraphML export saved to {output_path}")
        print("Import into Gephi: File -> Open -> select the .graphml file")
    except Exception as e:
        print(f"GraphML export failed: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Memory Graph CLI - Manage semantic knowledge graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build graph from research data
  python memory_graph_cli.py --build

  # Show graph statistics
  python memory_graph_cli.py --stats

  # Query related papers
  python memory_graph_cli.py --query 2501.03236

  # Generate Mermaid diagram
  python memory_graph_cli.py --visualize --format mermaid

  # Generate HTML visualization
  python memory_graph_cli.py --visualize --format html

  # Export to GraphML for Gephi
  python memory_graph_cli.py --export-graphml output.graphml
        """
    )

    parser.add_argument("--build", action="store_true",
                        help="Build graph from research data (rebuilds existing)")
    parser.add_argument("--query", type=str, metavar="ARXIV_ID",
                        help="Query related papers by arXiv ID")
    parser.add_argument("--visualize", action="store_true",
                        help="Generate visualization")
    parser.add_argument("--format", type=str, default="mermaid",
                        choices=["html", "png", "svg", "mermaid", "json"],
                        help="Visualization format (default: mermaid)")
    parser.add_argument("--export-graphml", type=str, metavar="PATH",
                        help="Export graph to GraphML format for Gephi")
    parser.add_argument("--stats", action="store_true",
                        help="Show graph statistics")
    parser.add_argument("--data-dir", type=str, default="research_data",
                        help="Directory containing research data (default: research_data)")
    parser.add_argument("--output-dir", type=str, default="research_output/visualizations",
                        help="Directory for output files (default: research_output/visualizations)")
    parser.add_argument("--output", type=str,
                        help="Specific output file path (overrides --output-dir)")
    parser.add_argument("--top-k", type=int, default=10,
                        help="Number of related papers to show (default: 10)")

    args = parser.parse_args()

    # If no arguments, show help
    if not any([args.build, args.query, args.visualize,
                args.export_graphml, args.stats]):
        parser.print_help()
        return

    # Load or build memory
    memory = load_or_build_memory(args.data_dir, build=args.build)

    # Execute commands
    if args.stats:
        show_stats(memory)

    if args.query:
        query_related_papers(memory, args.query, top_k=args.top_k)

    if args.visualize:
        output_path = args.output or str(Path(args.output_dir) / f"graph.{args.format}")
        visualize_graph(memory, output_path, args.format)

    if args.export_graphml:
        export_graphml(memory, args.export_graphml)


if __name__ == "__main__":
    main()
