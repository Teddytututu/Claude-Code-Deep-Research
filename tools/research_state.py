"""
Research State Management System v7.0
LangGraph-inspired state management with persistence

Author: Deep Research System
Date: 2026-02-09
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
from pathlib import Path
from datetime import datetime
import uuid

class ResearchPhase(Enum):
    """Research workflow phases"""
    PLANNING = "planning"
    DISCOVERY = "discovery"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    REVIEW = "review"
    COMPLETE = "complete"

class FindingType(Enum):
    """Types of research findings"""
    ACADEMIC_PAPER = "academic_paper"
    GITHUB_PROJECT = "github_project"
    COMMUNITY_DISCUSSION = "community_discussion"
    CODE_EXAMPLE = "code_example"
    QUANTITATIVE_METRIC = "quantitative_metric"
    CONSENSUS_POINT = "consensus_point"
    CONTROVERSY = "controversy"

@dataclass
class Citation:
    """
    Standardized citation format with clickable links

    Examples:
    - Academic: [arXiv:2402.01680](https://arxiv.org/abs/2402.01680) | [PDF](https://arxiv.org/pdf/2402.01680.pdf)
    - GitHub: [langchain-ai/langgraph](https://github.com/langchain-ai/langgraph) ⭐ 10k+
    - Discussion: [Hacker News](https://news.ycombinator.com/item?id=12345) (200 upvotes)
    """
    id: str  # arxiv_id, repo_name, or discussion_id
    type: str  # "academic", "github", "reddit", "hn", "blog"
    title: str
    url: str  # Primary clickable URL
    url_markdown: str  # Full markdown with all links
    metadata: Dict[str, Any] = field(default_factory=dict)  # stars, upvotes, date, etc.

    def to_markdown(self) -> str:
        """Generate markdown citation"""
        return self.url_markdown

@dataclass
class AcademicPaper:
    """
    Academic paper finding with complete analysis
    """
    arxiv_id: str
    title: str
    authors: List[str] = field(default_factory=list)
    abstract: str = ""  # 200-500 word summary
    url_markdown: str = ""  # [arXiv:ID](URL) | [PDF](PDF_URL)

    # Methodology
    methodology: Dict[str, Any] = field(default_factory=dict)
    # datasets: str
    # baselines: str
    # models_tested: str
    # evaluation_metrics: str

    # Results
    quantitative_results: Dict[str, Any] = field(default_factory=dict)
    # benchmarks: Dict[str, float]
    # comparisons: str
    # statistical_significance: str

    # Analysis
    limitations: List[str] = field(default_factory=list)
    future_work: List[str] = field(default_factory=list)
    implementation: Dict[str, Any] = field(default_factory=dict)
    # code_url: str
    # datasets_available: bool
    # reproducibility_score: str

    summary: str = ""  # 500-1000 word deep analysis

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

@dataclass
class GitHubProject:
    """
    GitHub project finding with architecture analysis
    """
    name: str  # org/repo
    url_markdown: str  # [org/repo](URL) ⭐ Xk+
    stars_display: str  # "⭐ 10,000+"
    description: str = ""
    last_commit_date: str = ""

    key_files: List[Dict[str, str]] = field(default_factory=list)
    # path: str, description: str

    architecture_description: str = ""  # 200-500 words
    integration_examples: List[str] = field(default_factory=list)
    performance_benchmarks: Dict[str, Any] = field(default_factory=dict)

    license: str = ""
    language: str = ""
    framework_type: str = ""  # "orchestration", "state-management", etc.

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

@dataclass
class CommunityDiscussion:
    """
    Community discussion finding with consensus analysis
    """
    platform: str  # "reddit", "hn", "github", "blog"
    url_markdown: str  # Clickable link
    title: str
    original_title: str = ""  # Original if translated

    key_quotes: List[Dict[str, Any]] = field(default_factory=list)
    # user: str, quote: str, upvotes: int

    consensus_level: str = ""  # "high", "medium", "low", "controversial"
    summary: str = ""  # 200-400 words

    related_discussions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

@dataclass
class ResearchFindings:
    """
    Collection of all research findings by type
    """
    academic_papers: List[AcademicPaper] = field(default_factory=list)
    github_projects: List[GitHubProject] = field(default_factory=list)
    community_discussions: List[CommunityDiscussion] = field(default_factory=list)

    def add_paper(self, paper: AcademicPaper):
        """Add an academic paper finding"""
        self.academic_papers.append(paper)

    def add_project(self, project: GitHubProject):
        """Add a GitHub project finding"""
        self.github_projects.append(project)

    def add_discussion(self, discussion: CommunityDiscussion):
        """Add a community discussion finding"""
        self.community_discussions.append(discussion)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "academic_papers": [p.to_dict() for p in self.academic_papers],
            "github_projects": [p.to_dict() for p in self.github_projects],
            "community_discussions": [d.to_dict() for d in self.community_discussions]
        }

@dataclass
class ResearchState:
    """
    Complete research session state

    Inspired by LangGraph's StateGraph pattern with:
    - Checkpoint/resume capability
    - Phase tracking
    - Finding collection
    - Performance metrics
    """
    # Session metadata
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    query: str = ""
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())

    # Workflow state
    phase: ResearchPhase = ResearchPhase.PLANNING
    research_phases_completed: List[str] = field(default_factory=list)

    # Research data
    findings: ResearchFindings = field(default_factory=ResearchFindings)
    citations: List[Citation] = field(default_factory=list)
    executive_summary: List[Dict[str, str]] = field(default_factory=list)

    # Configuration
    token_budget: int = 200000
    tokens_used: int = 0
    subagents_deployed: int = 0

    # Quality tracking
    quality_scores: Dict[str, float] = field(default_factory=dict)

    # Context variables (Swarm-style)
    context_variables: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Serialize state to JSON"""
        data = asdict(self)
        # Convert Enum to string
        data["phase"] = self.phase.value
        data["findings"] = self.findings.to_dict()
        return json.dumps(data, indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'ResearchState':
        """Deserialize state from JSON"""
        data = json.loads(json_str)
        # Convert phase string back to Enum
        if "phase" in data and isinstance(data["phase"], str):
            data["phase"] = ResearchPhase(data["phase"])
        # Reconstruct findings
        if "findings" in data:
            findings_data = data["findings"]
            findings = ResearchFindings()
            for paper_data in findings_data.get("academic_papers", []):
                findings.add_paper(AcademicPaper(**paper_data))
            for project_data in findings_data.get("github_projects", []):
                findings.add_project(GitHubProject(**project_data))
            for discussion_data in findings_data.get("community_discussions", []):
                findings.add_discussion(CommunityDiscussion(**discussion_data))
            data["findings"] = findings
        return cls(**data)

    def advance_phase(self, new_phase: ResearchPhase):
        """Advance to next research phase"""
        self.research_phases_completed.append(self.phase.value)
        self.phase = new_phase

    def is_complete(self) -> bool:
        """Check if research is complete"""
        return self.phase == ResearchPhase.COMPLETE

    def get_progress(self) -> Dict[str, Any]:
        """Get research progress summary"""
        total_phases = len(ResearchPhase)
        completed = len(self.research_phases_completed)
        return {
            "current_phase": self.phase.value,
            "phases_completed": completed,
            "total_phases": total_phases,
            "progress_percent": int(completed / total_phases * 100),
            "papers_found": len(self.findings.academic_papers),
            "projects_found": len(self.findings.github_projects),
            "discussions_found": len(self.findings.community_discussions)
        }


class ResearchStateManager:
    """
    State management system with persistence

    Features:
    - Checkpoint state to disk
    - Resume from checkpoint
    - List all sessions
    - Session cleanup
    """

    def __init__(self, state_dir: str = "research_data"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)

    def save_state(self, state: ResearchState) -> Path:
        """
        Save state to disk

        Returns:
            Path to saved state file
        """
        state_file = self.state_dir / f"{state.session_id}_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            f.write(state.to_json())
        return state_file

    def load_state(self, session_id: str) -> Optional[ResearchState]:
        """
        Load state from disk

        Returns:
            ResearchState if found, None otherwise
        """
        state_file = self.state_dir / f"{session_id}_state.json"
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                return ResearchState.from_json(f.read())
        return None

    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        List all research sessions

        Returns:
            List of session metadata
        """
        sessions = []
        state_files = self.state_dir.glob("*_state.json")

        for state_file in state_files:
            session_id = state_file.stem.replace("_state", "")
            state = self.load_state(session_id)
            if state:
                sessions.append({
                    "session_id": session_id,
                    "query": state.query,
                    "phase": state.phase.value,
                    "start_time": state.start_time,
                    "progress": state.get_progress()
                })

        return sorted(sessions, key=lambda x: x["start_time"], reverse=True)

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a research session

        Returns:
            True if deleted, False if not found
        """
        state_file = self.state_dir / f"{session_id}_state.json"
        if state_file.exists():
            state_file.unlink()
            return True
        return False

    def cleanup_old_sessions(self, days: int = 7) -> int:
        """
        Delete sessions older than specified days

        Returns:
            Number of sessions deleted
        """
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(days=days)
        deleted = 0

        for state_file in self.state_dir.glob("*_state.json"):
            # Check modification time
            mtime = datetime.fromtimestamp(state_file.stat().st_mtime)
            if mtime < cutoff:
                state_file.unlink()
                deleted += 1

        return deleted


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Research State Manager")
    parser.add_argument("--list", action="store_true", help="List all sessions")
    parser.add_argument("--show", type=str, help="Show session details")
    parser.add_argument("--delete", type=str, help="Delete a session")
    parser.add_argument("--cleanup", type=int, help="Cleanup sessions older than N days")

    args = parser.parse_args()

    manager = ResearchStateManager()

    if args.list:
        sessions = manager.list_sessions()
        print(f"Found {len(sessions)} sessions:")
        for session in sessions:
            print(f"  {session['session_id'][:8]}... | {session['query'][:50]} | {session['progress']['progress_percent']}%")

    elif args.show:
        state = manager.load_state(args.show)
        if state:
            print(state.to_json())
        else:
            print(f"Session {args.show} not found")

    elif args.delete:
        if manager.delete_session(args.delete):
            print(f"Deleted session {args.delete}")
        else:
            print(f"Session {args.delete} not found")

    elif args.cleanup:
        deleted = manager.cleanup_old_sessions(args.cleanup)
        print(f"Deleted {deleted} old sessions")
