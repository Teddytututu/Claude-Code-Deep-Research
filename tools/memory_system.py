"""
Multi-Graph Agentic Memory Architecture (MAGMA) v9.0

Based on: MAGMA: Multi-Graph Agentic Memory Architecture (arXiv:2601.03236)

This module implements the complete memory system with three layers:
1. SemanticMemory: Knowledge graph for relationships between entities
2. TemporalMemory: Time-series tracking of research sessions and evolution
3. EpisodicMemory: Context windows for active and related sessions

Author: Deep Research System
Date: 2026-02-09
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import uuid
import hashlib

from memory_graph import (
    SemanticMemory,
    NodeType,
    EdgeType,
    GraphNode,
    GraphEdge,
    CitationNetwork
)


class MemoryLayer(Enum):
    """Memory layer types"""
    SEMANTIC = "semantic"  # Knowledge graph
    TEMPORAL = "temporal"  # Time-series tracking
    EPISODIC = "episodic"  # Context windows


@dataclass
class Finding:
    """A research finding with provenance"""
    id: str
    type: str  # "paper", "project", "discussion", "concept"
    content: Dict[str, Any]
    timestamp: str
    session_id: str
    agent_type: str  # Which agent found this
    confidence: float = 0.8
    source_url: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class TemporalSnapshot:
    """A snapshot of research state at a point in time"""
    timestamp: str
    session_id: str
    phase: str
    findings_count: int
    key_insights: List[str]
    metrics: Dict[str, Any]
    checkpoint_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EpisodicContext:
    """Context window for a research session"""
    session_id: str
    query: str
    start_time: str
    context_summary: str
    key_findings: List[str]
    related_sessions: List[str] = field(default_factory=list)
    context_embedding: Optional[List[float]] = None  # For similarity search


class TemporalMemory:
    """
    Temporal Memory Layer - Time-Series Tracking

    Tracks the evolution of research over time:
    - Research session timeline
    - Finding provenance (what agent found what, when)
    - Evolution of insights and concepts
    - Progress metrics over time
    """

    def __init__(self, storage_dir: str = "research_data/temporal"):
        """
        Initialize temporal memory.

        Args:
            storage_dir: Directory for storing temporal data
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self._snapshots: List[TemporalSnapshot] = []
        self._finding_timeline: List[Finding] = []
        self._session_timeline: Dict[str, List[Tuple[str, str]]] = defaultdict(list)  # session_id -> [(timestamp, event)]

    def record_finding(self, finding: Finding) -> None:
        """
        Record a finding with timestamp.

        Args:
            finding: The finding to record
        """
        self._finding_timeline.append(finding)
        self._add_session_event(finding.session_id, finding.timestamp, f"Finding: {finding.type}")

    def record_snapshot(self, snapshot: TemporalSnapshot) -> None:
        """
        Record a temporal snapshot.

        Args:
            snapshot: The snapshot to record
        """
        self._snapshots.append(snapshot)
        self._add_session_event(snapshot.session_id, snapshot.timestamp, f"Phase: {snapshot.phase}")

    def _add_session_event(self, session_id: str, timestamp: str, event: str) -> None:
        """Add an event to the session timeline"""
        self._session_timeline[session_id].append((timestamp, event))

    def get_session_timeline(self, session_id: str) -> List[Tuple[str, str]]:
        """
        Get timeline for a session.

        Args:
            session_id: Session ID

        Returns:
            List of (timestamp, event) tuples
        """
        return sorted(self._session_timeline.get(session_id, []), key=lambda x: x[0])

    def get_findings_by_timerange(
        self,
        start_time: str,
        end_time: str,
        session_id: Optional[str] = None
    ) -> List[Finding]:
        """
        Get findings within a time range.

        Args:
            start_time: ISO format start time
            end_time: ISO format end time
            session_id: Optional session filter

        Returns:
            List of findings in the time range
        """
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)

        findings = []
        for finding in self._finding_timeline:
            finding_time = datetime.fromisoformat(finding.timestamp)
            if start <= finding_time <= end:
                if session_id is None or finding.session_id == session_id:
                    findings.append(finding)

        return findings

    def get_evolution(self, session_id: str) -> List[TemporalSnapshot]:
        """
        Get evolution snapshots for a session.

        Args:
            session_id: Session ID

        Returns:
            List of snapshots showing progression
        """
        return [s for s in self._snapshots if s.session_id == session_id]

    def get_provenance(self, finding_id: str) -> Dict[str, Any]:
        """
        Get provenance information for a finding.

        Args:
            finding_id: Finding ID

        Returns:
            Provenance information
        """
        for finding in self._finding_timeline:
            if finding.id == finding_id:
                return {
                    "finding_id": finding.id,
                    "agent_type": finding.agent_type,
                    "timestamp": finding.timestamp,
                    "session_id": finding.session_id,
                    "confidence": finding.confidence,
                    "source_url": finding.source_url
                }
        return {}

    def save(self, session_id: str) -> None:
        """Save temporal memory for a session"""
        filepath = self.storage_dir / f"{session_id}_temporal.json"

        data = {
            "snapshots": [
                {
                    "timestamp": s.timestamp,
                    "session_id": s.session_id,
                    "phase": s.phase,
                    "findings_count": s.findings_count,
                    "key_insights": s.key_insights,
                    "metrics": s.metrics,
                    "checkpoint_data": s.checkpoint_data
                }
                for s in self._snapshots
            ],
            "findings": [
                {
                    "id": f.id,
                    "type": f.type,
                    "content": f.content,
                    "timestamp": f.timestamp,
                    "session_id": f.session_id,
                    "agent_type": f.agent_type,
                    "confidence": f.confidence,
                    "source_url": f.source_url
                }
                for f in self._finding_timeline
            ],
            "timeline": dict(self._session_timeline)
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, session_id: str) -> None:
        """Load temporal memory for a session"""
        filepath = self.storage_dir / f"{session_id}_temporal.json"

        if not filepath.exists():
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Load snapshots
        self._snapshots = [
            TemporalSnapshot(
                timestamp=s["timestamp"],
                session_id=s["session_id"],
                phase=s["phase"],
                findings_count=s["findings_count"],
                key_insights=s["key_insights"],
                metrics=s["metrics"],
                checkpoint_data=s.get("checkpoint_data", {})
            )
            for s in data.get("snapshots", [])
        ]

        # Load findings
        self._finding_timeline = [
            Finding(
                id=f["id"],
                type=f["type"],
                content=f["content"],
                timestamp=f["timestamp"],
                session_id=f["session_id"],
                agent_type=f["agent_type"],
                confidence=f.get("confidence", 0.8),
                source_url=f.get("source_url", "")
            )
            for f in data.get("findings", [])
        ]

        # Load timeline
        self._session_timeline = defaultdict(list)
        for session_id, events in data.get("timeline", {}).items():
            self._session_timeline[session_id] = [(t, e) for t, e in events]


class EpisodicMemory:
    """
    Episodic Memory Layer - Context Windows

    Manages context windows for research sessions:
    - Active research context
    - Related past sessions
    - Cross-session pattern recognition
    - Context similarity search
    """

    def __init__(self, storage_dir: str = "research_data/episodic"):
        """
        Initialize episodic memory.

        Args:
            storage_dir: Directory for storing episodic data
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self._contexts: Dict[str, EpisodicContext] = {}
        self._active_sessions: Dict[str, EpisodicContext] = {}

    def create_context(
        self,
        query: str,
        session_id: Optional[str] = None
    ) -> EpisodicContext:
        """
        Create a new episodic context.

        Args:
            query: Research query
            session_id: Optional session ID (generated if not provided)

        Returns:
            New episodic context
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        context = EpisodicContext(
            session_id=session_id,
            query=query,
            start_time=datetime.now().isoformat(),
            context_summary=query,
            key_findings=[]
        )

        self._contexts[session_id] = context
        self._active_sessions[session_id] = context

        return context

    def update_context(self, session_id: str, findings: List[str]) -> None:
        """
        Update context with new findings.

        Args:
            session_id: Session ID
            findings: New findings to add
        """
        if session_id in self._contexts:
            self._contexts[session_id].key_findings.extend(findings)

            # Update context summary
            all_findings = self._contexts[session_id].key_findings
            if len(all_findings) <= 5:
                self._contexts[session_id].context_summary = "; ".join(all_findings)
            else:
                self._contexts[session_id].context_summary = "; ".join(all_findings[:5]) + f"... (+{len(all_findings) - 5} more)"

    def find_related_sessions(
        self,
        query: str,
        top_k: int = 3
    ) -> List[Tuple[str, float]]:
        """
        Find related past sessions.

        Args:
            query: Current research query
            top_k: Number of related sessions to return

        Returns:
            List of (session_id, similarity_score) tuples
        """
        # Simple keyword-based similarity (in production, use embeddings)
        query_words = set(query.lower().split())

        similarities = []
        for session_id, context in self._contexts.items():
            if session_id in self._active_sessions:
                continue  # Skip active sessions

            context_words = set(context.context_summary.lower().split())
            intersection = query_words & context_words
            union = query_words | context_words

            if union:
                similarity = len(intersection) / len(union)
            else:
                similarity = 0.0

            similarities.append((session_id, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def get_context(self, session_id: str) -> Optional[EpisodicContext]:
        """
        Get context for a session.

        Args:
            session_id: Session ID

        Returns:
            Episodic context if found
        """
        return self._contexts.get(session_id)

    def close_session(self, session_id: str) -> None:
        """
        Mark a session as closed.

        Args:
            session_id: Session ID
        """
        if session_id in self._active_sessions:
            del self._active_sessions[session_id]

    def save(self, session_id: str) -> None:
        """Save episodic memory for a session"""
        if session_id not in self._contexts:
            return

        context = self._contexts[session_id]
        filepath = self.storage_dir / f"{session_id}_episodic.json"

        data = {
            "session_id": context.session_id,
            "query": context.query,
            "start_time": context.start_time,
            "context_summary": context.context_summary,
            "key_findings": context.key_findings,
            "related_sessions": context.related_sessions
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_all(self) -> None:
        """Load all saved episodic contexts"""
        for filepath in self.storage_dir.glob("*_episodic.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            context = EpisodicContext(
                session_id=data["session_id"],
                query=data["query"],
                start_time=data["start_time"],
                context_summary=data["context_summary"],
                key_findings=data["key_findings"],
                related_sessions=data.get("related_sessions", [])
            )

            self._contexts[context.session_id] = context


class MAGMAMemory:
    """
    Multi-Graph Agentic Memory Architecture (MAGMA)

    Integrates all three memory layers:
    - SemanticMemory: Knowledge graph
    - TemporalMemory: Time-series tracking
    - EpisodicMemory: Context windows

    Based on: arXiv:2601.03236
    """

    def __init__(self, storage_dir: str = "research_data"):
        """
        Initialize MAGMA memory system.

        Args:
            storage_dir: Base directory for all memory storage
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize all three layers
        self.semantic = SemanticMemory(use_networkx=True)
        self.temporal = TemporalMemory(str(self.storage_dir / "temporal"))
        self.episodic = EpisodicMemory(str(self.storage_dir / "episodic"))

        # Load existing episodic contexts
        self.episodic.load_all()

        self._current_session: Optional[str] = None

    def start_session(self, query: str) -> str:
        """
        Start a new research session.

        Args:
            query: Research query

        Returns:
            Session ID
        """
        context = self.episodic.create_context(query)
        self._current_session = context.session_id

        # Record session start in temporal memory
        self.temporal.record_snapshot(TemporalSnapshot(
            timestamp=datetime.now().isoformat(),
            session_id=context.session_id,
            phase="session_start",
            findings_count=0,
            key_insights=[],
            metrics={"query": query}
        ))

        return context.session_id

    def add_paper_finding(self, paper_data: Dict[str, Any], agent_type: str) -> str:
        """
        Add a paper finding to memory.

        Args:
            paper_data: Paper data
            agent_type: Agent that found this paper

        Returns:
            Finding ID
        """
        # Add to semantic memory
        node_id = self.semantic.add_paper(paper_data)

        # Record in temporal memory
        finding = Finding(
            id="",  # Will be generated
            type="academic_paper",
            content=paper_data,
            timestamp=datetime.now().isoformat(),
            session_id=self._current_session or "",
            agent_type=agent_type,
            confidence=paper_data.get("relevance_score", 0.8),
            source_url=paper_data.get("url", "")
        )
        self.temporal.record_finding(finding)

        # Update episodic context
        if self._current_session:
            self.episodic.update_context(self._current_session, [paper_data.get("title", "")])

        return finding.id

    def add_project_finding(self, project_data: Dict[str, Any], agent_type: str) -> str:
        """Add a GitHub project finding to memory"""
        node_id = self.semantic.add_project(project_data)

        finding = Finding(
            id="",
            type="github_project",
            content=project_data,
            timestamp=datetime.now().isoformat(),
            session_id=self._current_session or "",
            agent_type=agent_type,
            confidence=0.8,
            source_url=project_data.get("url", "")
        )
        self.temporal.record_finding(finding)

        if self._current_session:
            self.episodic.update_context(self._current_session, [project_data.get("name", "")])

        return finding.id

    def add_discussion_finding(self, discussion_data: Dict[str, Any], agent_type: str) -> str:
        """Add a community discussion finding to memory"""
        node_id = self.semantic.add_discussion(discussion_data)

        finding = Finding(
            id="",
            type="community_discussion",
            content=discussion_data,
            timestamp=datetime.now().isoformat(),
            session_id=self._current_session or "",
            agent_type=agent_type,
            confidence=0.6,
            source_url=discussion_data.get("url", "")
        )
        self.temporal.record_finding(finding)

        if self._current_session:
            self.episodic.update_context(self._current_session, [discussion_data.get("title", "")])

        return finding.id

    def record_checkpoint(self, phase: str, metrics: Dict[str, Any]) -> None:
        """
        Record a research checkpoint.

        Args:
            phase: Current research phase
            metrics: Metrics to record
        """
        if not self._current_session:
            return

        snapshot = TemporalSnapshot(
            timestamp=datetime.now().isoformat(),
            session_id=self._current_session,
            phase=phase,
            findings_count=len(self.temporal._finding_timeline),
            key_insights=self.episodic.get_context(self._current_session).key_findings if self._current_session else [],
            metrics=metrics
        )

        self.temporal.record_snapshot(snapshot)

    def get_related_context(self, query: str) -> List[str]:
        """
        Get context from related past sessions.

        Args:
            query: Current research query

        Returns:
            List of context summaries from related sessions
        """
        related = self.episodic.find_related_sessions(query)

        contexts = []
        for session_id, _ in related:
            context = self.episodic.get_context(session_id)
            if context:
                contexts.append(f"Related session: {context.context_summary}")

        return contexts

    def end_session(self) -> Dict[str, Any]:
        """
        End the current research session.

        Returns:
            Session summary
        """
        if not self._current_session:
            return {}

        # Save all memory layers
        self.temporal.save(self._current_session)
        self.episodic.save(self._current_session)
        self.episodic.close_session(self._current_session)

        # Build session summary
        summary = {
            "session_id": self._current_session,
            "findings_count": len([
                f for f in self.temporal._finding_timeline
                if f.session_id == self._current_session
            ]),
            "snapshots": len([
                s for s in self.temporal._snapshots
                if s.session_id == self._current_session
            ]),
            "semantic_stats": self.semantic.to_dict()["stats"]
        }

        self._current_session = None

        return summary

    def save_semantic_graph(self, filepath: Optional[str] = None) -> str:
        """
        Save semantic knowledge graph.

        Args:
            filepath: Optional filepath (default: storage_dir/semantic_graph.json)

        Returns:
            Path to saved graph
        """
        if filepath is None:
            filepath = self.storage_dir / "semantic_graph.json"

        self.semantic.save(str(filepath))
        return str(filepath)

    def get_citation_network(self) -> CitationNetwork:
        """Get citation network analyzer"""
        return CitationNetwork(self.semantic)


# Migration helper for v7.0 -> v9.0
def migrate_v7_to_v9(
    old_state_file: str,
    output_dir: str = "research_data"
) -> MAGMAMemory:
    """
    Migrate v7.0 ResearchState to v9.0 MAGMA memory.

    Args:
        old_state_file: Path to v7.0 state JSON file
        output_dir: Output directory for v9.0 memory

    Returns:
        New MAGMAMemory instance
    """
    with open(old_state_file, 'r', encoding='utf-8') as f:
        old_state = json.load(f)

    memory = MAGMAMemory(storage_dir=output_dir)
    memory.start_session(old_state.get("query", "migrated_session"))

    # Migrate papers
    for paper in old_state.get("findings", {}).get("academic_papers", []):
        memory.add_paper_finding(paper, "migrated")

    # Migrate projects
    for project in old_state.get("findings", {}).get("github_projects", []):
        memory.add_project_finding(project, "migrated")

    # Migrate discussions
    for discussion in old_state.get("findings", {}).get("community_discussions", []):
        memory.add_discussion_finding(discussion, "migrated")

    # Build citation network
    for paper in old_state.get("findings", {}).get("academic_papers", []):
        for cited in paper.get("references", []):
            memory.semantic.add_citation_edge(paper.get("arxiv_id", ""), cited)

    return memory


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MAGMA Memory System v9.0")
    parser.add_argument("--migrate", type=str, help="Migrate v7.0 state file")
    parser.add_argument("--output", type=str, default="research_data", help="Output directory")
    parser.add_argument("--save-graph", type=str, help="Save semantic graph to file")

    args = parser.parse_args()

    if args.migrate:
        print(f"Migrating {args.migrate} to MAGMA v9.0...")
        memory = migrate_v7_to_v9(args.migrate, args.output)
        print(f"Migration complete. Session: {memory._current_session}")

        if args.save_graph:
            memory.save_semantic_graph(args.save_graph)
            print(f"Semantic graph saved to {args.save_graph}")
