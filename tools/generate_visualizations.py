"""
Generate Visualizations from Research Data
从研究数据生成可视化

Batch visualization generator that bridges between research data files
and the memory graph system. Automatically loads research outputs and
generates all available visualizations.

Usage:
    python "tools\\generate_visualizations.py"
    python "tools\\generate_visualizations.py" --data-dir research_data
    python "tools\\generate_visualizations.py" --output-dir visualizations

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

from memory_graph import SemanticMemory
from memory_system import MAGMAMemory


def load_research_data(data_dir: str) -> Dict[str, List[Dict]]:
    """
    Load all research data files from a directory.

    Args:
        data_dir: Directory containing research output JSON files

    Returns:
        Dictionary with keys: papers, projects, discussions
    """
    data_path = Path(data_dir)
    results = {
        "papers": [],
        "projects": [],
        "discussions": []
    }

    # Load academic research output
    academic_file = data_path / "academic_research_output.json"
    if academic_file.exists():
        print(f"Loading: {academic_file.name}")
        with open(academic_file, encoding='utf-8') as f:
            data = json.load(f)
            results["papers"] = data.get("papers", [])
            print(f"  -> {len(results['papers'])} papers")

    # Load GitHub research output
    github_file = data_path / "github_research_output.json"
    if github_file.exists():
        print(f"Loading: {github_file.name}")
        with open(github_file, encoding='utf-8') as f:
            data = json.load(f)
            results["projects"] = data.get("projects", data.get("repositories", []))
            print(f"  -> {len(results['projects'])} projects")

    # Load community research output
    community_file = data_path / "community_research_output.json"
    if community_file.exists():
        print(f"Loading: {community_file.name}")
        with open(community_file, encoding='utf-8') as f:
            data = json.load(f)
            results["discussions"] = data.get("discussions", data.get("threads", []))
            print(f"  -> {len(results['discussions'])} discussions")

    # Load logic analysis if available
    logic_file = data_path / "logic_analysis.json"
    if logic_file.exists():
        print(f"Loading: {logic_file.name}")
        with open(logic_file, encoding='utf-8') as f:
            results["logic_analysis"] = json.load(f)
            print(f"  -> logic analysis loaded")

    return results


def populate_memory(memory: MAGMAMemory, research_data: Dict[str, Any]) -> None:
    """
    Populate MAGMAMemory with research data.

    Args:
        memory: MAGMAMemory instance
        research_data: Dictionary with papers, projects, discussions
    """
    # Add papers
    for paper in research_data.get("papers", []):
        memory.add_paper_finding(paper, "academic-researcher")

    # Add projects
    for project in research_data.get("projects", []):
        memory.add_project_finding(project, "github-watcher")

    # Add discussions
    for discussion in research_data.get("discussions", []):
        memory.add_discussion_finding(discussion, "community-listener")


def generate_all_visualizations(
    data_dir: str = "research_data",
    output_dir: str = "research_output/visualizations"
) -> None:
    """
    Generate all visualizations from research data.

    Creates:
    - Mermaid diagram (.mmd)
    - HTML interactive visualization (.html)
    - JSON graph export (.json)
    - Statistics summary

    Args:
        data_dir: Directory containing research data
        output_dir: Directory for output files
    """
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS FROM RESEARCH DATA")
    print("=" * 60 + "\n")

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Initialize memory
    memory = MAGMAMemory(storage_dir=data_dir)

    # Load research data
    print("Step 1: Loading research data...")
    research_data = load_research_data(data_dir)

    total_items = (
        len(research_data.get("papers", [])) +
        len(research_data.get("projects", [])) +
        len(research_data.get("discussions", []))
    )

    if total_items == 0:
        print(f"\nNo research data found in {data_dir}")
        print("Looking for files:")
        print(f"  - {Path(data_dir) / 'academic_research_output.json'}")
        print(f"  - {Path(data_dir) / 'github_research_output.json'}")
        print(f"  - {Path(data_dir) / 'community_research_output.json'}")
        return

    # Populate memory
    print(f"\nStep 2: Populating memory with {total_items} items...")
    populate_memory(memory, research_data)

    # Save semantic graph
    print("\nStep 3: Saving semantic graph...")
    graph_path = output_path / "semantic_graph.json"
    memory.save_semantic_graph(str(graph_path))
    print(f"  -> Saved to {graph_path}")

    # Generate Mermaid diagram
    print("\nStep 4: Generating Mermaid diagram...")
    mermaid_path = output_path / "citation_graph.mmd"
    mermaid_code = memory.semantic.to_mermaid()
    with open(mermaid_path, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    print(f"  -> Saved to {mermaid_path}")

    # Generate HTML visualization
    print("\nStep 5: Generating HTML visualization...")
    try:
        html_path = memory.semantic.visualize(
            format="html",
            output_path=str(output_path / "graph.html")
        )
        print(f"  -> Saved to {html_path}")
        print(f"  -> Open in browser: file:///{html_path.replace(os.sep, '/')}")
    except RuntimeError as e:
        print(f"  -> HTML generation skipped: {e}")
        print(f"     (Install pyvis: pip install pyvis)")

    # Generate statistics
    print("\nStep 6: Generating statistics...")
    stats = memory.semantic.to_dict()["stats"]
    stats_path = output_path / "graph_stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"  -> Saved to {stats_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("VISUALIZATION SUMMARY")
    print("=" * 60)
    print(f"Total Nodes: {stats['node_count']}")
    print(f"Total Edges: {stats['edge_count']}")

    if stats.get('node_types'):
        print("\nNode Types:")
        for node_type, count in sorted(stats['node_types'].items()):
            print(f"  {node_type}: {count}")

    if stats.get('edge_types'):
        print("\nEdge Types:")
        for edge_type, count in sorted(stats['edge_types'].items()):
            print(f"  {edge_type}: {count}")

    print("\n" + "=" * 60)
    print(f"All visualizations saved to: {output_path}")
    print("=" * 60 + "\n")


def generate_from_logic_analysis(
    data_dir: str = "research_data",
    output_dir: str = "research_output/visualizations"
) -> None:
    """
    Generate citation network visualization from logic analysis.

    Creates a focused citation network based on the logic analysis results.

    Args:
        data_dir: Directory containing research data
        output_dir: Directory for output files
    """
    logic_file = Path(data_dir) / "logic_analysis.json"
    if not logic_file.exists():
        print(f"Logic analysis not found: {logic_file}")
        return

    print("Generating citation network from logic analysis...")

    with open(logic_file, encoding='utf-8') as f:
        logic_data = json.load(f)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Extract citation relationships from logic analysis
    citation_mermaid = generate_logic_citation_mermaid(logic_data)

    mermaid_path = output_path / "logic_citation_graph.mmd"
    with open(mermaid_path, 'w', encoding='utf-8') as f:
        f.write(citation_mermaid)

    print(f"Logic citation graph saved to {mermaid_path}")


def generate_logic_citation_mermaid(logic_data: Dict[str, Any]) -> str:
    """
    Generate Mermaid diagram from logic analysis data.

    Args:
        logic_data: Logic analysis JSON data

    Returns:
        Mermaid diagram code
    """
    lines = ["graph TD", "    %% Citation Network from Logic Analysis"]

    # Extract papers and their relationships
    papers = logic_data.get("papers", {})
    relationships = logic_data.get("citation_relationships", [])

    # Add nodes for each paper
    for paper_id, paper_info in papers.items():
        title = paper_info.get("title", paper_id)
        paper_type = paper_info.get("type", "unknown")
        safe_id = paper_id.replace(".", "_").replace("-", "_")

        style_class = "defaultPaper"
        if paper_type == "root":
            style_class = "rootPaper"
        elif paper_type == "survey":
            style_class = "surveyPaper"
        elif paper_type == "sota":
            style_class = "sotaPaper"

        lines.append(f'    {safe_id}["{title[:40]}..."]:::{style_class}')

    # Add edges for citations
    for rel in relationships:
        source = rel.get("source", "").replace(".", "_").replace("-", "_")
        target = rel.get("target", "").replace(".", "_").replace("-", "_")
        rel_type = rel.get("type", "cites")

        if source and target:
            lines.append(f"    {source} -->|{rel_type}| {target}")

    # Add style definitions
    lines.append("\n    classDef sotaPaper fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff")
    lines.append("    classDef rootPaper fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff")
    lines.append("    classDef surveyPaper fill:#f39c12,stroke:#e67e22,stroke-width:2px,color:#fff")
    lines.append("    classDef defaultPaper fill:#ecf0f1,stroke:#bdc3c7,stroke-width:1px,color:#2c3e50")

    return "\n".join(lines)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate visualizations from research data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all visualizations
  python generate_visualizations.py

  # Specify custom directories
  python generate_visualizations.py --data-dir research_data --output-dir visualizations

  # Generate from logic analysis only
  python generate_visualizations.py --logic-analysis
        """
    )

    parser.add_argument("--data-dir", type=str, default="research_data",
                        help="Directory containing research data (default: research_data)")
    parser.add_argument("--output-dir", type=str, default="research_output/visualizations",
                        help="Directory for output files (default: research_output/visualizations)")
    parser.add_argument("--logic-analysis", action="store_true",
                        help="Generate citation network from logic_analysis.json")

    args = parser.parse_args()

    if args.logic_analysis:
        generate_from_logic_analysis(args.data_dir, args.output_dir)
    else:
        generate_all_visualizations(args.data_dir, args.output_dir)


if __name__ == "__main__":
    main()
