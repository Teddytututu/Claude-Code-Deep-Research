"""
Cross-Domain Relationship Tracker v2.0
跨域关系追踪器

Query layer on SemanticMemory from MAGMAMemory.
Leverages existing node types and edge types for cross-domain analysis.

Based on: MAGMA: Multi-Graph Agentic Memory Architecture (arXiv:2601.03236)

Author: Deep Research System
Date: 2026-02-11
Version: 2.0 - Integrated with SemanticMemory
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from datetime import datetime

# Import SemanticMemory for integration
try:
    from memory_graph import SemanticMemory, EdgeType, NodeType
    MEMORY_GRAPH_AVAILABLE = True
except ImportError:
    MEMORY_GRAPH_AVAILABLE = False
    EdgeType = None
    NodeType = None


class RelationshipType(Enum):
    """Types of cross-domain relationships (mirrors EdgeType)"""
    PAPER_TO_REPO = "implements"  # Paper implemented by repo
    PAPER_TO_COMMUNITY = "discusses"  # Paper discussed in community
    REPO_TO_COMMUNITY = "discusses"  # Repo discussed in community
    REPO_TO_PAPER = "cites"  # Repo README cites paper
    PAPER_TO_PAPER = "cites"  # Paper cites another paper


class Sentiment(Enum):
    """Sentiment of community discussion"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


@dataclass
class CrossDomainRelationship:
    """A relationship between entities from different domains"""
    source_id: str
    source_type: str  # "paper", "repo", "community"
    target_id: str
    target_type: str  # "paper", "repo", "community"
    relationship_type: RelationshipType
    confidence: float = 1.0
    evidence: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_type": self.source_type,
            "target_id": self.target_id,
            "target_type": self.target_type,
            "relationship_type": self.relationship_type.value,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "metadata": self.metadata
        }


@dataclass
class BridgingEntity:
    """An entity that connects multiple domains"""
    entity_id: str
    entity_type: str
    domains_connected: Set[str]
    connection_count: int
    importance_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "domains_connected": list(self.domains_connected),
            "connection_count": self.connection_count,
            "importance_score": self.importance_score
        }


class CrossDomainTracker:
    """
    Cross-Domain Relationship Tracker v2.0

    Query layer on SemanticMemory from MAGMAMemory.
    Leverages existing node types and edge types for cross-domain analysis.
    """

    def __init__(self, semantic_memory: Optional['SemanticMemory'] = None, storage_dir: str = "research_data"):
        """
        Initialize the tracker.

        Args:
            semantic_memory: Optional SemanticMemory instance. If None, loads from storage_dir.
            storage_dir: Directory to load/save SemanticMemory data.
        """
        self.storage_dir = Path(storage_dir)
        self.semantic_memory = semantic_memory

        # If no semantic memory provided, try to load it
        if self.semantic_memory is None and MEMORY_GRAPH_AVAILABLE:
            semantic_graph_path = self.storage_dir / "semantic_graph.json"
            if semantic_graph_path.exists():
                self.semantic_memory = SemanticMemory.load(str(semantic_graph_path))
            else:
                self.semantic_memory = SemanticMemory()

        # Maintain backwards-compatible indices for v1.0 API
        self._relationships: List[CrossDomainRelationship] = []
        self._paper_to_repo: Dict[str, Set[str]] = {}
        self._paper_to_community: Dict[str, Set[str]] = {}
        self._repo_to_community: Dict[str, Set[str]] = {}
        self._repo_to_papers: Dict[str, Set[str]] = {}

        # Entity metadata (for backwards compatibility)
        self._papers: Dict[str, Dict[str, Any]] = {}
        self._repos: Dict[str, Dict[str, Any]] = {}
        self._communities: Dict[str, Dict[str, Any]] = {}

        # Sync with semantic memory if available
        if self.semantic_memory:
            self._sync_from_semantic_memory()

    def _sync_from_semantic_memory(self) -> None:
        """Sync internal indices from SemanticMemory graph."""
        if not self.semantic_memory:
            return

        # Clear existing indices
        self._paper_to_repo.clear()
        self._paper_to_community.clear()
        self._repo_to_community.clear()
        self._repo_to_papers.clear()

        # Sync papers
        for node_id, node in self.semantic_memory._nodes.items():
            if node.type == NodeType.ACADEMIC_PAPER:
                arxiv_id = node.attributes.get("arxiv_id", node_id.replace("paper_", ""))
                self._papers[arxiv_id] = node.attributes

        # Sync repos
        for node_id, node in self.semantic_memory._nodes.items():
            if node.type == NodeType.GITHUB_PROJECT:
                name = node.attributes.get("name", node_id.replace("project_", "").replace("_", "/"))
                self._repos[name] = node.attributes

        # Sync communities
        for node_id, node in self.semantic_memory._nodes.items():
            if node.type == NodeType.COMMUNITY_DISCUSSION:
                url = node.attributes.get("url", node_id)
                self._communities[url] = node.attributes

        # Sync relationships from edges
        for edge in self.semantic_memory._edges:
            if edge.type == EdgeType.IMPLEMENTS:
                # Project implements paper
                source = edge.source.replace("project_", "").replace("_", "/")
                target = edge.target.replace("paper_", "")
                if source in self._repos and target in self._papers:
                    if target not in self._paper_to_repo:
                        self._paper_to_repo[target] = set()
                    self._paper_to_repo[target].add(source)
                    if source not in self._repo_to_papers:
                        self._repo_to_papers[source] = set()
                    self._repo_to_papers[source].add(target)

            elif edge.type == EdgeType.DISCUSSES:
                # Discussion discusses paper or project
                source = edge.source
                target = edge.target
                if source.startswith("discussion_") and target.startswith("paper_"):
                    paper_id = target.replace("paper_", "")
                    disc_id = self.semantic_memory._nodes[source].attributes.get("url", source)
                    if paper_id not in self._paper_to_community:
                        self._paper_to_community[paper_id] = set()
                    self._paper_to_community[paper_id].add(disc_id)

    def add_paper(self, paper_id: str, metadata: Dict[str, Any]) -> None:
        """
        Register an academic paper.

        Args:
            paper_id: ArXiv ID or unique identifier
            metadata: Paper metadata (title, authors, year, etc.)
        """
        self._papers[paper_id] = metadata

    def add_repo(self, repo_name: str, metadata: Dict[str, Any]) -> None:
        """
        Register a GitHub repository.

        Args:
            repo_name: Repository name (org/repo format)
            metadata: Repository metadata (stars, language, etc.)
        """
        self._repos[repo_name] = metadata

    def add_community(self, discussion_id: str, metadata: Dict[str, Any]) -> None:
        """
        Register a community discussion.

        Args:
            discussion_id: Unique identifier (URL or ID)
            metadata: Discussion metadata (platform, title, upvotes, etc.)
        """
        self._communities[discussion_id] = metadata

    def add_paper_repo_relationship(
        self,
        paper_id: str,
        repo_name: str,
        confidence: float = 1.0,
        evidence: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a paper-to-repo relationship (implementation).

        Args:
            paper_id: ArXiv ID or paper identifier
            repo_name: Repository name (org/repo format)
            confidence: Confidence score (0-1)
            evidence: Evidence string (e.g., "README mentions paper")
            metadata: Additional metadata
        """
        relationship = CrossDomainRelationship(
            source_id=paper_id,
            source_type="paper",
            target_id=repo_name,
            target_type="repo",
            relationship_type=RelationshipType.PAPER_TO_REPO,
            confidence=confidence,
            evidence=evidence,
            metadata=metadata or {}
        )
        self._relationships.append(relationship)

        # Update indices
        if paper_id not in self._paper_to_repo:
            self._paper_to_repo[paper_id] = set()
        self._paper_to_repo[paper_id].add(repo_name)

        if repo_name not in self._repo_to_papers:
            self._repo_to_papers[repo_name] = set()
        self._repo_to_papers[repo_name].add(paper_id)

    def add_paper_community_relationship(
        self,
        paper_id: str,
        discussion_id: str,
        sentiment: Sentiment = Sentiment.NEUTRAL,
        confidence: float = 1.0,
        evidence: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a paper-to-community relationship (validation/discussion).

        Args:
            paper_id: ArXiv ID or paper identifier
            discussion_id: Discussion URL or ID
            sentiment: Discussion sentiment
            confidence: Confidence score (0-1)
            evidence: Evidence string
            metadata: Additional metadata
        """
        relationship = CrossDomainRelationship(
            source_id=paper_id,
            source_type="paper",
            target_id=discussion_id,
            target_type="community",
            relationship_type=RelationshipType.PAPER_TO_COMMUNITY,
            confidence=confidence,
            evidence=evidence,
            metadata=metadata or {}
        )
        self._relationships.append(relationship)

        # Update indices
        if paper_id not in self._paper_to_community:
            self._paper_to_community[paper_id] = set()
        self._paper_to_community[paper_id].add(discussion_id)

    def add_repo_community_relationship(
        self,
        repo_name: str,
        discussion_id: str,
        discussion_type: str = "general",
        confidence: float = 1.0,
        evidence: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a repo-to-community relationship.

        Args:
            repo_name: Repository name (org/repo format)
            discussion_id: Discussion URL or ID
            discussion_type: Type of discussion (general, issue, pr, review)
            confidence: Confidence score (0-1)
            evidence: Evidence string
            metadata: Additional metadata
        """
        relationship = CrossDomainRelationship(
            source_id=repo_name,
            source_type="repo",
            target_id=discussion_id,
            target_type="community",
            relationship_type=RelationshipType.REPO_TO_COMMUNITY,
            confidence=confidence,
            evidence=evidence,
            metadata=metadata or {}
        )
        self._relationships.append(relationship)

        # Update indices
        if repo_name not in self._repo_to_community:
            self._repo_to_community[repo_name] = set()
        self._repo_to_community[repo_name].add(discussion_id)

    def add_repo_paper_relationship(
        self,
        repo_name: str,
        paper_id: str,
        confidence: float = 1.0,
        evidence: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a repo-to-paper relationship (citation in README).

        Args:
            repo_name: Repository name (org/repo format)
            paper_id: ArXiv ID or paper identifier
            confidence: Confidence score (0-1)
            evidence: Evidence string
            metadata: Additional metadata
        """
        relationship = CrossDomainRelationship(
            source_id=repo_name,
            source_type="repo",
            target_id=paper_id,
            target_type="paper",
            relationship_type=RelationshipType.REPO_TO_PAPER,
            confidence=confidence,
            evidence=evidence,
            metadata=metadata or {}
        )
        self._relationships.append(relationship)

        # Update indices
        if repo_name not in self._repo_to_papers:
            self._repo_to_papers[repo_name] = set()
        self._repo_to_papers[repo_name].add(paper_id)

    # ========== SemanticMemory Query Methods (v2.0 NEW) ==========

    def get_repos_for_paper_semantic(self, paper_id: str) -> Set[str]:
        """
        Get repos implementing a paper using SemanticMemory query.

        Args:
            paper_id: ArXiv ID of the paper

        Returns:
            Set of repo names implementing this paper
        """
        if not self.semantic_memory:
            return set()

        paper_node_id = f"paper_{paper_id}"
        neighbors = self.semantic_memory.get_neighbors(
            paper_node_id,
            edge_type=EdgeType.IMPLEMENTS,
            max_depth=1
        )

        # Convert node IDs back to repo names
        repos = set()
        for neighbor in neighbors:
            if neighbor.startswith("project_"):
                repo_name = neighbor.replace("project_", "").replace("_", "/")
                repos.add(repo_name)

        return repos

    def get_papers_for_repo_semantic(self, repo_name: str) -> Set[str]:
        """
        Get papers implemented by a repo using SemanticMemory query.

        Args:
            repo_name: Repository name (org/repo format)

        Returns:
            Set of ArXiv IDs implemented by this repo
        """
        if not self.semantic_memory:
            return set()

        repo_node_id = f"project_{repo_name.replace('/', '_')}"
        neighbors = self.semantic_memory.get_neighbors(
            repo_node_id,
            edge_type=EdgeType.IMPLEMENTS,
            max_depth=1
        )

        # Convert node IDs back to paper IDs
        papers = set()
        for neighbor in neighbors:
            if neighbor.startswith("paper_"):
                paper_id = neighbor.replace("paper_", "")
                papers.add(paper_id)

        return papers

    def get_discussions_for_paper_semantic(self, paper_id: str) -> Set[str]:
        """
        Get community discussions about a paper using SemanticMemory.

        Args:
            paper_id: ArXiv ID of the paper

        Returns:
            Set of discussion URLs/IDs
        """
        if not self.semantic_memory:
            return set()

        paper_node_id = f"paper_{paper_id}"
        neighbors = self.semantic_memory.get_neighbors(
            paper_node_id,
            edge_type=EdgeType.DISCUSSES,
            max_depth=1
        )

        discussions = set()
        for neighbor in neighbors:
            if neighbor.startswith("discussion_"):
                node = self.semantic_memory._nodes.get(neighbor)
                if node:
                    url = node.attributes.get("url", neighbor)
                    discussions.add(url)

        return discussions

    def get_bridging_entities_semantic(self, min_domains: int = 2) -> List['BridgingEntity']:
        """
        Find bridging entities using SemanticMemory graph traversal.

        Args:
            min_domains: Minimum number of domains an entity must connect

        Returns:
            List of bridging entities sorted by importance
        """
        if not self.semantic_memory:
            return self.find_bridging_entities(min_domains)

        bridging = []
        edge_types = [EdgeType.IMPLEMENTS, EdgeType.DISCUSSES, EdgeType.CITES]

        for node_id, node in self.semantic_memory._nodes.items():
            domains = set()
            connection_count = 0

            # Check what types of edges this node has
            for edge in self.semantic_memory._edges:
                if edge.source == node_id or edge.target == node_id:
                    connection_count += 1
                    # Determine domain based on edge type and connected node
                    other_id = edge.target if edge.source == node_id else edge.source

                    if edge.type == EdgeType.IMPLEMENTS:
                        if node.type == NodeType.ACADEMIC_PAPER:
                            domains.add("repo")  # Paper connected to repo
                        elif node.type == NodeType.GITHUB_PROJECT:
                            domains.add("paper")  # Repo connected to paper
                    elif edge.type == EdgeType.DISCUSSES:
                        if node.type == NodeType.ACADEMIC_PAPER:
                            domains.add("community")  # Paper discussed in community
                        elif node.type == NodeType.GITHUB_PROJECT:
                            domains.add("community")  # Repo discussed in community
                        elif node.type == NodeType.COMMUNITY_DISCUSSION:
                            if other_id.startswith("paper_"):
                                domains.add("paper")
                            elif other_id.startswith("project_"):
                                domains.add("repo")

            if len(domains) >= min_domains:
                # Calculate importance score
                importance_score = (
                    connection_count * 1.0 +
                    len(domains) * 2.0
                )

                bridging.append(BridgingEntity(
                    entity_id=node_id,
                    entity_type=node.type.value,
                    domains_connected=domains,
                    connection_count=connection_count,
                    importance_score=importance_score
                ))

        bridging.sort(key=lambda x: x.importance_score, reverse=True)
        return bridging

    def get_cross_domain_graph_semantic(self) -> Dict[str, Any]:
        """
        Get cross-domain graph using SemanticMemory.

        Returns:
            Dictionary with nodes and edges for visualization
        """
        if not self.semantic_memory:
            return self.get_cross_domain_graph()

        nodes = []
        edges = []

        # Add nodes from semantic memory
        for node_id, node in self.semantic_memory._nodes.items():
            if node.type in [NodeType.ACADEMIC_PAPER, NodeType.GITHUB_PROJECT, NodeType.COMMUNITY_DISCUSSION]:
                nodes.append({
                    "id": node_id,
                    "label": node.attributes.get("title") or node.attributes.get("name", node_id)[:50],
                    "type": node.type.value,
                    "domain": self._get_domain_for_node_type(node.type),
                    "color": self._get_color_for_node_type(node.type),
                    "attributes": node.attributes
                })

        # Add cross-domain edges
        cross_domain_edge_types = [EdgeType.IMPLEMENTS, EdgeType.DISCUSSES]
        for edge in self.semantic_memory._edges:
            if edge.type in cross_domain_edge_types:
                edges.append({
                    "source": edge.source,
                    "target": edge.target,
                    "type": edge.type.value,
                    "weight": edge.weight,
                    "attributes": edge.attributes
                })

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "papers": len([n for n in nodes if n["type"] == "academic_paper"]),
                "repos": len([n for n in nodes if n["type"] == "github_project"]),
                "communities": len([n for n in nodes if n["type"] == "community_discussion"])
            }
        }

    def _get_domain_for_node_type(self, node_type: NodeType) -> str:
        """Get domain name for node type."""
        mapping = {
            NodeType.ACADEMIC_PAPER: "academic",
            NodeType.GITHUB_PROJECT: "github",
            NodeType.COMMUNITY_DISCUSSION: "community"
        }
        return mapping.get(node_type, "unknown")

    def _get_color_for_node_type(self, node_type: NodeType) -> str:
        """Get color for node type."""
        mapping = {
            NodeType.ACADEMIC_PAPER: "#3498db",  # Blue
            NodeType.GITHUB_PROJECT: "#2ecc71",  # Green
            NodeType.COMMUNITY_DISCUSSION: "#e67e22"  # Orange
        }
        return mapping.get(node_type, "#95a5a6")

    # ========== Backwards Compatibility Methods (v1.0 API) ==========

    def get_repos_for_paper(self, paper_id: str) -> Set[str]:
        """Get all repositories that implement a paper"""
        return self._paper_to_repo.get(paper_id, set())

    def get_papers_for_repo(self, repo_name: str) -> Set[str]:
        """Get all papers implemented by a repository"""
        return self._repo_to_papers.get(repo_name, set())

    def get_communities_for_paper(self, paper_id: str) -> Set[str]:
        """Get all community discussions about a paper"""
        return self._paper_to_community.get(paper_id, set())

    def get_communities_for_repo(self, repo_name: str) -> Set[str]:
        """Get all community discussions about a repository"""
        return self._repo_to_community.get(repo_name, set())

    def find_bridging_entities(self, min_domains: int = 2) -> List[BridgingEntity]:
        """
        Find entities that connect multiple domains.

        Args:
            min_domains: Minimum number of domains an entity must connect

        Returns:
            List of bridging entities sorted by importance
        """
        bridging = []

        # Check papers
        for paper_id in self._papers:
            domains = set()
            if paper_id in self._paper_to_repo and self._paper_to_repo[paper_id]:
                domains.add("repo")
            if paper_id in self._paper_to_community and self._paper_to_community[paper_id]:
                domains.add("community")
            if len(domains) >= min_domains:
                connection_count = (
                    len(self._paper_to_repo.get(paper_id, set())) +
                    len(self._paper_to_community.get(paper_id, set()))
                )
                bridging.append(BridgingEntity(
                    entity_id=paper_id,
                    entity_type="paper",
                    domains_connected=domains,
                    connection_count=connection_count,
                    importance_score=float(connection_count)
                ))

        # Check repos
        for repo_name in self._repos:
            domains = set()
            if repo_name in self._repo_to_papers and self._repo_to_papers[repo_name]:
                domains.add("paper")
            if repo_name in self._repo_to_community and self._repo_to_community[repo_name]:
                domains.add("community")
            if len(domains) >= min_domains:
                connection_count = (
                    len(self._repo_to_papers.get(repo_name, set())) +
                    len(self._repo_to_community.get(repo_name, set()))
                )
                bridging.append(BridgingEntity(
                    entity_id=repo_name,
                    entity_type="repo",
                    domains_connected=domains,
                    connection_count=connection_count,
                    importance_score=float(connection_count)
                ))

        # Sort by importance score
        bridging.sort(key=lambda x: x.importance_score, reverse=True)
        return bridging

    def get_cross_domain_graph(self) -> Dict[str, Any]:
        """
        Get the complete cross-domain graph as a dictionary.

        Returns:
            Dictionary with nodes and edges for visualization
        """
        nodes = []
        edges = []

        # Add paper nodes
        for paper_id, metadata in self._papers.items():
            nodes.append({
                "id": f"paper_{paper_id}",
                "label": metadata.get("title", paper_id)[:50],
                "type": "paper",
                "domain": "academic",
                "color": "#3498db",  # Blue
                "shape": "dot",
                "metadata": metadata
            })

        # Add repo nodes
        for repo_name, metadata in self._repos.items():
            nodes.append({
                "id": f"repo_{repo_name.replace('/', '_')}",
                "label": repo_name,
                "type": "repo",
                "domain": "github",
                "color": "#2ecc71",  # Green
                "shape": "square",
                "metadata": metadata
            })

        # Add community nodes
        for discussion_id, metadata in self._communities.items():
            nodes.append({
                "id": f"community_{hash(discussion_id)}",
                "label": metadata.get("title", discussion_id)[:50],
                "type": "community",
                "domain": "community",
                "color": "#e67e22",  # Orange
                "shape": "diamond",
                "metadata": metadata
            })

        # Add edges
        for rel in self._relationships:
            source = f"{rel.source_type}_{rel.source_id.replace('/', '_')}" if rel.source_type == "repo" else f"{rel.source_type}_{rel.source_id}"
            if rel.source_type == "community":
                source = f"community_{hash(rel.source_id)}"

            target = f"{rel.target_type}_{rel.target_id.replace('/', '_')}" if rel.target_type == "repo" else f"{rel.target_type}_{rel.target_id}"
            if rel.target_type == "community":
                target = f"community_{hash(rel.target_id)}"

            edges.append({
                "source": source,
                "target": target,
                "label": rel.relationship_type.value,
                "type": rel.relationship_type.value,
                "confidence": rel.confidence,
                "evidence": rel.evidence
            })

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "papers": len(self._papers),
                "repos": len(self._repos),
                "communities": len(self._communities)
            }
        }

    def load_from_research_data(self, research_data_dir: str = "research_data") -> None:
        """
        Load cross-domain relationships from research data JSON files.

        Also populates SemanticMemory with nodes and edges for cross-domain queries.

        Args:
            research_data_dir: Directory containing research data JSON files
        """
        data_path = Path(research_data_dir)

        # Load academic research
        academic_file = data_path / "academic_research_output.json"
        if academic_file.exists():
            with open(academic_file, 'r', encoding='utf-8') as f:
                academic_data = json.load(f)

            for paper in academic_data.get("papers", []):
                paper_id = paper.get("arxiv_id", paper.get("id", ""))
                if paper_id:
                    self.add_paper(paper_id, paper)
                    # v2.0: Also add to SemanticMemory
                    if self.semantic_memory:
                        self.semantic_memory.add_paper(paper)

        # Load GitHub research
        github_file = data_path / "github_research_output.json"
        if github_file.exists():
            with open(github_file, 'r', encoding='utf-8') as f:
                github_data = json.load(f)

            for project in github_data.get("projects", []):
                repo_name = project.get("name", "")
                if repo_name:
                    self.add_repo(repo_name, project)
                    # v2.0: Also add to SemanticMemory
                    if self.semantic_memory:
                        self.semantic_memory.add_project(project)

                    # Track paper implementations mentioned in project
                    for paper_id in project.get("implements_papers", []):
                        self.add_paper_repo_relationship(
                            paper_id=paper_id,
                            repo_name=repo_name,
                            evidence="Project implements or mentions paper"
                        )

        # Load community research
        community_file = data_path / "community_research_output.json"
        if community_file.exists():
            with open(community_file, 'r', encoding='utf-8') as f:
                community_data = json.load(f)

            for discussion in community_data.get("discussions", []):
                discussion_id = discussion.get("url", str(hash(discussion.get("title", ""))))
                self.add_community(discussion_id, discussion)
                # v2.0: Also add to SemanticMemory
                if self.semantic_memory:
                    self.semantic_memory.add_discussion(discussion)

                # Track papers discussed
                for paper_id in discussion.get("papers_discussed", []):
                    self.add_paper_community_relationship(
                        paper_id=paper_id,
                        discussion_id=discussion_id,
                        evidence="Paper discussed in community"
                    )

                # Track repos discussed
                for repo_name in discussion.get("repos_discussed", []):
                    self.add_repo_community_relationship(
                        repo_name=repo_name,
                        discussion_id=discussion_id,
                        evidence="Repository discussed in community"
                    )

        # Load logic analysis for additional relationships
        logic_file = data_path / "logic_analysis.json"
        if logic_file.exists():
            with open(logic_file, 'r', encoding='utf-8') as f:
                logic_data = json.load(f)

            # Extract relationships from logic analysis
            for paper_id, paper_data in logic_data.get("papers", {}).items():
                for related in paper_data.get("related_papers", []):
                    # Paper-to-paper citations
                    if paper_id not in self._papers:
                        self.add_paper(paper_id, {"title": paper_id})
                    if related not in self._papers:
                        self.add_paper(related, {"title": related})

        # v2.0: Sync from semantic memory after loading all data
        if self.semantic_memory:
            self._sync_from_semantic_memory()

    def to_dict(self) -> Dict[str, Any]:
        """Convert tracker to dictionary representation"""
        return {
            "papers": self._papers,
            "repos": self._repos,
            "communities": self._communities,
            "relationships": [r.to_dict() for r in self._relationships],
            "paper_to_repo": {k: list(v) for k, v in self._paper_to_repo.items()},
            "paper_to_community": {k: list(v) for k, v in self._paper_to_community.items()},
            "repo_to_community": {k: list(v) for k, v in self._repo_to_community.items()},
            "repo_to_papers": {k: list(v) for k, v in self._repo_to_papers.items()},
            "bridging_entities": [b.to_dict() for b in self.find_bridging_entities()]
        }

    def generate_insights(self) -> List[Dict[str, Any]]:
        """
        Generate cross-domain insights from tracked relationships.

        Returns:
            List of insight dictionaries with type, description, and evidence
        """
        insights = []

        # Insight 1: Implementation gaps (papers without repos)
        papers_with_implementations = set(self._paper_to_repo.keys())
        all_papers = set(self._papers.keys())
        papers_without_repos = all_papers - papers_with_implementations

        if papers_without_repos:
            insights.append({
                "insight_id": "insight_impl_gap",
                "insight_type": "implementation_gap",
                "description": f"{len(papers_without_repos)} papers lack GitHub implementations",
                "affected_papers": list(papers_without_repos)[:5],
                "recommendation": "Priority for implementation"
            })

        # Insight 2: Community validation gaps
        papers_with_discussions = set(self._paper_to_community.keys())
        papers_without_discussions = all_papers - papers_with_discussions

        if papers_without_discussions:
            insights.append({
                "insight_id": "insight_comm_gap",
                "insight_type": "community_validation_gap",
                "description": f"{len(papers_without_discussions)} papers lack community discussion",
                "affected_papers": list(papers_without_discussions)[:5],
                "recommendation": "Opportunity for community engagement"
            })

        # Insight 3: Highly connected papers
        if self._paper_to_repo:
            most_implemented = max(self._paper_to_repo.items(),
                                   key=lambda x: len(x[1]),
                                   default=(None, set()))
            if most_implemented[0]:
                title = self._papers.get(most_implemented[0], {}).get("title", most_implemented[0])
                insights.append({
                    "insight_id": "insight_most_implemented",
                    "insight_type": "high_connectivity",
                    "description": f"'{title[:50]}...' has {len(most_implemented[1])} implementations",
                    "paper_id": most_implemented[0],
                    "implementation_count": len(most_implemented[1]),
                    "repos": list(most_implemented[1])
                })

        # Insight 4: Cross-domain bridges
        bridging = self.find_bridging_entities(min_domains=2)
        if bridging:
            insights.append({
                "insight_id": "insight_bridging",
                "insight_type": "cross_domain_bridges",
                "description": f"{len(bridging)} entities connect multiple domains",
                "bridging_entities": [{
                    "id": b.entity_id,
                    "type": b.entity_type,
                    "domains": list(b.domains_connected),
                    "importance": b.importance_score
                } for b in bridging[:5]]
            })

        return insights

    def identify_relationship_clusters(self) -> List[Dict[str, Any]]:
        """
        Identify clusters of related entities across domains.

        Returns:
            List of cluster dictionaries with cluster type and members
        """
        clusters = []

        # Cluster 1: Implementation clusters (papers + repos)
        for paper_id, repos in self._paper_to_repo.items():
            if len(repos) >= 2:  # Only include multi-implementation papers
                title = self._papers.get(paper_id, {}).get("title", paper_id)
                clusters.append({
                    "cluster_id": f"impl_cluster_{paper_id}",
                    "cluster_type": "implementation_cluster",
                    "description": f"Papers with multiple implementations",
                    "paper_id": paper_id,
                    "paper_title": title,
                    "implementing_repos": list(repos),
                    "repo_count": len(repos)
                })

        # Cluster 2: Validation clusters (papers + communities)
        for paper_id, discussions in self._paper_to_community.items():
            if len(discussions) >= 2:
                title = self._papers.get(paper_id, {}).get("title", paper_id)
                clusters.append({
                    "cluster_id": f"val_cluster_{paper_id}",
                    "cluster_type": "validation_cluster",
                    "description": f"Papers with multiple community discussions",
                    "paper_id": paper_id,
                    "paper_title": title,
                    "discussions": list(discussions),
                    "discussion_count": len(discussions)
                })

        # Cluster 3: Discussion clusters (repos + communities)
        for repo_name, discussions in self._repo_to_community.items():
            if len(discussions) >= 2:
                clusters.append({
                    "cluster_id": f"disc_cluster_{repo_name.replace('/', '_')}",
                    "cluster_type": "discussion_cluster",
                    "description": f"Repos with active community discussions",
                    "repo_name": repo_name,
                    "discussions": list(discussions),
                    "discussion_count": len(discussions)
                })

        return clusters

    def save(self, filepath: str) -> None:
        """Save tracker state to JSON file"""
        data = self.to_dict()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: str) -> 'CrossDomainTracker':
        """Load tracker state from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        tracker = cls()

        # Load entities
        for paper_id, metadata in data.get("papers", {}).items():
            tracker.add_paper(paper_id, metadata)

        for repo_name, metadata in data.get("repos", {}).items():
            tracker.add_repo(repo_name, metadata)

        for discussion_id, metadata in data.get("communities", {}).items():
            tracker.add_community(discussion_id, metadata)

        # Load relationships
        for rel_data in data.get("relationships", []):
            if rel_data["relationship_type"] == "implements":
                tracker.add_paper_repo_relationship(
                    paper_id=rel_data["source_id"],
                    repo_name=rel_data["target_id"],
                    confidence=rel_data.get("confidence", 1.0),
                    evidence=rel_data.get("evidence", ""),
                    metadata=rel_data.get("metadata", {})
                )
            elif rel_data["relationship_type"] == "validates":
                tracker.add_paper_community_relationship(
                    paper_id=rel_data["source_id"],
                    discussion_id=rel_data["target_id"],
                    confidence=rel_data.get("confidence", 1.0),
                    evidence=rel_data.get("evidence", ""),
                    metadata=rel_data.get("metadata", {})
                )
            elif rel_data["relationship_type"] == "discusses":
                tracker.add_repo_community_relationship(
                    repo_name=rel_data["source_id"],
                    discussion_id=rel_data["target_id"],
                    confidence=rel_data.get("confidence", 1.0),
                    evidence=rel_data.get("evidence", ""),
                    metadata=rel_data.get("metadata", {})
                )
            elif rel_data["relationship_type"] == "cites" and rel_data["source_type"] == "repo":
                tracker.add_repo_paper_relationship(
                    repo_name=rel_data["source_id"],
                    paper_id=rel_data["target_id"],
                    confidence=rel_data.get("confidence", 1.0),
                    evidence=rel_data.get("evidence", ""),
                    metadata=rel_data.get("metadata", {})
                )

        return tracker


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Cross-Domain Relationship Tracker v2.0 - Query layer on SemanticMemory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load research data and show statistics
  python cross_domain_tracker.py --load-data research_data --stats

  # Show bridging entities (connects 2+ domains)
  python cross_domain_tracker.py --load-data research_data --bridging --min-domains 2

  # Query repos implementing a specific paper
  python cross_domain_tracker.py --query-repos-for-paper 2506.12508

  # Generate cross-domain graph for visualization
  python cross_domain_tracker.py --load-data research_data --graph --save cross_domain_graph.json

  # Use SemanticMemory query (v2.0)
  python cross_domain_tracker.py --semantic-query --bridging
        """
    )

    # Data loading
    parser.add_argument("--load-data", type=str, default="research_data",
                        help="Load research data from directory")
    parser.add_argument("--load-graph", type=str,
                        help="Load SemanticMemory graph from file")

    # Output options
    parser.add_argument("--save", type=str, help="Save tracker state to file")
    parser.add_argument("--save-semantic", type=str, help="Save SemanticMemory graph to file")
    parser.add_argument("--graph", action="store_true",
                        help="Generate cross-domain graph for visualization")

    # Query options
    parser.add_argument("--bridging", action="store_true",
                        help="Show bridging entities (connects 2+ domains)")
    parser.add_argument("--min-domains", type=int, default=2,
                        help="Minimum domains for bridging entities (default: 2)")
    parser.add_argument("--query-repos-for-paper", type=str,
                        help="Query repos implementing a paper (arXiv ID)")
    parser.add_argument("--query-papers-for-repo", type=str,
                        help="Query papers implemented by a repo (org/repo)")

    # Analysis options
    parser.add_argument("--stats", action="store_true",
                        help="Show statistics")
    parser.add_argument("--semantic-query", action="store_true",
                        help="Use SemanticMemory query instead of v1.0 indices")
    parser.add_argument("--clusters", action="store_true",
                        help="Identify relationship clusters")
    parser.add_argument("--insights", action="store_true",
                        help="Generate cross-domain insights")

    # v2.0 flags
    parser.add_argument("--version", action="version", version="Cross-Domain Tracker v2.0")

    args = parser.parse_args()

    # Initialize tracker
    tracker = CrossDomainTracker(storage_dir=args.load_data)

    # Load semantic graph if specified
    if args.load_graph and MEMORY_GRAPH_AVAILABLE:
        tracker.semantic_memory = SemanticMemory.load(args.load_graph)
        tracker._sync_from_semantic_memory()
        print(f"Loaded SemanticMemory graph from {args.load_graph}")

    # Load research data if specified
    if args.load_data:
        tracker.load_from_research_data(args.load_data)
        print(f"Loaded cross-domain data from {args.load_data}")

        # If semantic memory has data, show its status
        if tracker.semantic_memory:
            print(f"SemanticMemory: {len(tracker.semantic_memory._nodes)} nodes, {len(tracker.semantic_memory._edges)} edges")

    # Show statistics
    if args.stats:
        if args.semantic_query and tracker.semantic_memory:
            graph = tracker.get_cross_domain_graph_semantic()
        else:
            graph = tracker.get_cross_domain_graph()
        stats = graph["stats"]
        print(f"\nCross-Domain Statistics:")
        print(f"  Papers: {stats['papers']}")
        print(f"  Repos: {stats['repos']}")
        print(f"  Communities: {stats['communities']}")
        print(f"  Total Nodes: {stats['total_nodes']}")
        print(f"  Total Edges: {stats['total_edges']}")

        # Show additional relationship stats
        print(f"\nRelationship Counts:")
        print(f"  Paper -> Repo: {len(tracker._paper_to_repo)}")
        print(f"  Paper -> Community: {len(tracker._paper_to_community)}")
        print(f"  Repo -> Community: {len(tracker._repo_to_community)}")

    # Show bridging entities
    if args.bridging:
        if args.semantic_query and tracker.semantic_memory:
            bridging = tracker.get_bridging_entities_semantic(args.min_domains)
        else:
            bridging = tracker.find_bridging_entities(args.min_domains)

        print(f"\nBridging Entities (connecting {args.min_domains}+ domains):")
        if not bridging:
            print("  No bridging entities found.")
        for entity in bridging[:10]:
            entity_label = entity.entity_id
            # Try to get a human-readable label
            if entity.entity_type == "academic_paper":
                entity_label = tracker._papers.get(entity.entity_id, {}).get("title", entity.entity_id)
            elif entity.entity_type == "github_project":
                entity_label = entity.entity_id.replace("_", "/")
            print(f"  [{entity.entity_type}] {entity_label[:50]}")
            print(f"    Domains: {', '.join(entity.domains_connected)}")
            print(f"    Connections: {entity.connection_count}, Importance: {entity.importance_score:.2f}")

    # Query repos for paper
    if args.query_repos_for_paper:
        if args.semantic_query and tracker.semantic_memory:
            repos = tracker.get_repos_for_paper_semantic(args.query_repos_for_paper)
        else:
            repos = tracker.get_repos_for_paper(args.query_repos_for_paper)

        print(f"\nRepos implementing paper {args.query_repos_for_paper}:")
        if not repos:
            print("  No implementations found.")
        for repo in sorted(repos):
            stars = tracker._repos.get(repo, {}).get("stars_display", "")
            print(f"  - {repo} {stars}")

    # Query papers for repo
    if args.query_papers_for_repo:
        if args.semantic_query and tracker.semantic_memory:
            papers = tracker.get_papers_for_repo_semantic(args.query_papers_for_repo)
        else:
            papers = tracker.get_papers_for_repo(args.query_papers_for_repo)

        print(f"\nPapers implemented by repo {args.query_papers_for_repo}:")
        if not papers:
            print("  No papers found.")
        for paper in sorted(papers):
            title = tracker._papers.get(paper, {}).get("title", paper)[:50]
            print(f"  - {paper}: {title}")

    # Generate and save graph
    if args.graph:
        if args.semantic_query and tracker.semantic_memory:
            graph = tracker.get_cross_domain_graph_semantic()
        else:
            graph = tracker.get_cross_domain_graph()

        output_file = args.save or "cross_domain_graph.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
        print(f"\nCross-domain graph saved to {output_file}")
        print(f"  Nodes: {len(graph['nodes'])}, Edges: {len(graph['edges'])}")

    # Generate insights
    if args.insights:
        insights = tracker.generate_insights()
        print(f"\nCross-Domain Insights:")
        for insight in insights[:5]:
            print(f"  [{insight['type']}] {insight['description']}")
            if insight.get('evidence'):
                print(f"    Evidence: {insight['evidence']}")

    # Save tracker state
    if args.save and not args.graph:
        tracker.save(args.save)
        print(f"\nTracker state saved to {args.save}")

    # Save semantic memory
    if args.save_semantic and tracker.semantic_memory:
        tracker.semantic_memory.save(args.save_semantic)
        print(f"\nSemanticMemory graph saved to {args.save_semantic}")
