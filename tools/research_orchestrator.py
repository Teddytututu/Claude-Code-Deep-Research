"""
Multi-Agent Research Orchestrator v10.0
Based on Swarm's handoff pattern + LangGraph's state management + Anthropic's multi-agent research system

v10.0 Updates:
- Integrated with Pydantic Settings configuration
- Added anyio support for cross-library async compatibility
- Added rate limiting for API calls
- Enhanced parallel execution with TaskGroup

Author: Deep Research System
Date: 2026-02-18
"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import asyncio
import json
from pathlib import Path
from datetime import datetime
import uuid

# Optional anyio import for structured concurrency
try:
    import anyio
    from anyio import create_task_group
    ANYIO_AVAILABLE = True
except ImportError:
    ANYIO_AVAILABLE = False

# Optional config import
try:
    from config import settings, Settings
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    settings = None

# Optional rate limiter import
try:
    from rate_limiter import RateLimiter, get_default_limiter
    RATE_LIMITER_AVAILABLE = True
except ImportError:
    RATE_LIMITER_AVAILABLE = False

class AgentRole(Enum):
    """Research agent roles following Anthropic's orchestrator-worker pattern"""
    LEAD = "lead"
    ACADEMIC = "academic-researcher"
    GITHUB = "github-watcher"
    COMMUNITY = "community-listener"
    CITATION = "citation-agent"

@dataclass
class Agent:
    """Agent configuration with tools and model selection"""
    name: str
    role: AgentRole
    instructions: str
    tools: List[str] = field(default_factory=list)
    model: str = field(default_factory=lambda: settings.subagent_model if settings else "claude-sonnet-4-20250514")
    max_turns: int = field(default_factory=lambda: settings.default_max_turns if settings else 20)

@dataclass
class Handoff:
    """
    Swarm-style handoff for agent switching

    Usage:
        def transfer_to_github_agent():
            return Handoff(target_agent=github_agent, context={"repo": "langgraph"})
    """
    target_agent: Agent
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResearchState:
    """
    LangGraph-inspired state management with persistence
    Based on Anthropic's memory system for multi-agent research
    """
    query: str
    phase: str = "planning"
    findings: Dict[str, Any] = field(default_factory=dict)
    citations: List[Dict[str, str]] = field(default_factory=list)
    token_budget: int = 200000
    context_variables: Dict[str, Any] = field(default_factory=dict)
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_json(self) -> str:
        """Serialize state to JSON"""
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'ResearchState':
        """Deserialize state from JSON"""
        data = json.loads(json_str)
        return cls(**data)

class ResearchOrchestrator:
    """
    Multi-Agent Research Orchestrator

    Implements orchestrator-worker pattern:
    - Lead agent (Opus 4.5) coordinates 3-5 parallel subagents
    - Subagents use 3+ tools in parallel for 90% speed improvement
    - Token budget: 15x normal chat, but 90.2% performance gain

    v10.0 Updates:
    - Integrated with Pydantic Settings configuration
    - Added anyio support for structured concurrency
    - Added rate limiting for API calls

    Based on:
    - Anthropic multi-agent research system architecture
    - Swarm's handoff pattern for agent coordination
    - LangGraph's state management for persistence
    """

    def __init__(
        self,
        state_dir: Optional[str] = None,
        use_settings: bool = True
    ):
        """
        Initialize orchestrator.

        Args:
            state_dir: Directory for state files (default: from settings or "research_data")
            use_settings: Whether to use global settings
        """
        # Use settings if available
        if use_settings and settings:
            self.state_dir = Path(state_dir or settings.research_data_dir)
            self._lead_model = settings.lead_model
            self._subagent_model = settings.subagent_model
            self._default_max_turns = settings.default_max_turns
            self._multi_agent_threshold = settings.multi_agent_threshold
        else:
            self.state_dir = Path(state_dir or "research_data")
            self._lead_model = "claude-opus-4-5-20250514"
            self._subagent_model = "claude-sonnet-4-20250514"
            self._default_max_turns = 20
            self._multi_agent_threshold = 0.45

        self.state_dir.mkdir(exist_ok=True)
        self.agents: Dict[AgentRole, Agent] = {}

        # Initialize rate limiter
        self._rate_limiter: Optional[RateLimiter] = None
        if RATE_LIMITER_AVAILABLE:
            self._rate_limiter = get_default_limiter()

        self._setup_agents()

    def _setup_agents(self):
        """Initialize research agents with specialized instructions"""
        self.agents[AgentRole.LEAD] = Agent(
            name="lead-researcher",
            role=AgentRole.LEAD,
            instructions=self._lead_instructions(),
            model=self._lead_model,
            tools=["Task", "Read", "Write", "AskUserQuestion"],
            max_turns=self._default_max_turns
        )

        self.agents[AgentRole.ACADEMIC] = Agent(
            name="academic-researcher",
            role=AgentRole.ACADEMIC,
            instructions=self._academic_instructions(),
            model=self._subagent_model,
            tools=[
                "mcp__arxiv-mcp-server__search_papers",
                "mcp__arxiv-mcp-server__download_paper",
                "mcp__arxiv-mcp-server__read_paper",
                "mcp__web-search-prime__webSearchPrime"
            ],
            max_turns=self._default_max_turns
        )

        self.agents[AgentRole.GITHUB] = Agent(
            name="github-watcher",
            role=AgentRole.GITHUB,
            instructions=self._github_instructions(),
            model=self._subagent_model,
            tools=[
                "mcp__zread__get_repo_structure",
                "mcp__zread__read_file",
                "mcp__zread__search_doc",
                "mcp__web-search-prime__webSearchPrime"
            ],
            max_turns=self._default_max_turns
        )

        self.agents[AgentRole.COMMUNITY] = Agent(
            name="community-listener",
            role=AgentRole.COMMUNITY,
            instructions=self._community_instructions(),
            model=self._subagent_model,
            tools=[
                "mcp__web-reader__webReader",
                "mcp__web-search-prime__webSearchPrime",
                "Grep", "Glob"
            ],
            max_turns=self._default_max_turns
        )

        self.agents[AgentRole.CITATION] = Agent(
            name="citation-agent",
            role=AgentRole.CITATION,
            instructions=self._citation_instructions(),
            model=self._subagent_model,
            tools=["Read", "Write", "Edit"],
            max_turns=self._default_max_turns
        )

    def _lead_instructions(self) -> str:
        """Instructions for lead researcher agent"""
        return """You are the lead researcher coordinating a multi-agent study.

RESPONSIBILITIES:
1. Analyze the research query and develop strategy
2. Determine if multi-agent approach is needed (45% threshold rule)
3. Delegate to specialized subagents in parallel
4. Synthesize findings from all subagents
5. Produce final report with clickable citations

DECISION FRAMEWORK:
- Single-agent success rate < 45%? → Use multi-agent
- Task has parallelizable aspects? → Use multi-agent
- Token budget: 15x normal, but 90.2% performance gain

OUTPUT FORMAT:
JSON with:
- executive_summary: 8-12 key findings with clickable citations
- academic_landscape: Papers with methodology, quantitative results, limitations
- open_source_ecosystem: GitHub projects with architecture analysis
- community_perspectives: Real-world insights and consensus
- performance_metrics: Token usage, cost, execution time
- references: All clickable markdown links

CITATION FORMAT (STRICT):
- Papers: [arXiv:ID](https://arxiv.org/abs/ID) | [PDF](https://arxiv.org/pdf/ID.pdf)
- GitHub: [org/repo](https://github.com/org/repo) ⭐ Xk+
- Discussions: [Platform](URL) with metrics

QUALITY REQUIREMENTS:
- All citations must be clickable
- Include quantitative data (exact numbers)
- Acknowledge limitations
- Bilingual: Chinese narrative + English terminology
"""

    def _academic_instructions(self) -> str:
        """Instructions for academic research subagent"""
        return """You are an academic research specialist focused on discovering and analyzing scholarly literature.

OBJECTIVE:
Find and analyze academic papers on the research topic, focusing on:
- Root/foundational papers
- State-of-the-art (SOTA) works
- Survey/review papers
- Citation networks and relationships

OUTPUT FORMAT (JSON):
Each paper must include:
- arxiv_id: ArXiv ID or DOI
- title: Full title (English)
- abstract: Complete abstract (200-500 words)
- url_markdown: Clickable markdown "[arXiv:ID](URL) | [PDF](PDF_URL)"
- methodology: { datasets, baselines, models_tested, evaluation_metrics }
- quantitative_results: { benchmarks, comparisons, statistical_significance }
- limitations: [] (Paper's admitted limitations)
- future_work: [] (Author's suggested directions)
- implementation: { code_url, datasets_available, reproducibility_score }
- summary: Deep analysis (500-1000 words)

MINIMUM REQUIREMENTS:
- 5+ papers with complete analysis
- 2+ papers with full-text reading
- Citation network analysis
- Mathematical formulations (if applicable)

SOURCES:
- cs.AI, cs.LG, cs.CL, cs.MA categories
- Prioritize papers from 2020-2025
- High-citation papers (>50 citations)
- Papers with available full text
"""

    def _github_instructions(self) -> str:
        """Instructions for GitHub research subagent"""
        return """You are an open source ecosystem analyst focused on discovering and analyzing GitHub projects.

OBJECTIVE:
Find and analyze relevant GitHub projects, focusing on:
- Technology factions and patterns
- Architecture implementations
- Integration examples
- Performance benchmarks

OUTPUT FORMAT (JSON):
Each project must include:
- name: org/repo
- url_markdown: Clickable "[org/repo](URL) ⭐ Xk+"
- stars_display: "⭐ 1,000+" format
- description: Project description
- last_commit_date: Recent activity
- key_files: [{path, description}]
- architecture_description: Detailed analysis (200-500 words)
- integration_examples: Usage patterns
- performance_benchmarks: Quantitative data if available
- license: License type

MINIMUM REQUIREMENTS:
- 5+ relevant projects
- Architecture pattern analysis
- Code examples from key files
- Comparison of approaches

ANALYSIS FOCUS:
- Multi-agent framework implementations
- State management patterns
- Orchestration strategies
- Production readiness
"""

    def _community_instructions(self) -> str:
        """Instructions for community research subagent"""
        return """You are a community discussion analyst focused on extracting real-world insights.

OBJECTIVE:
Monitor and analyze community discussions from:
- Reddit (r/MachineLearning, r/artificial, r/LocalLLaMA)
- Hacker News
- GitHub Discussions
- Technical blogs

OUTPUT FORMAT (JSON):
Each discussion must include:
- platform: "reddit" | "hn" | "github" | "blog"
- url_markdown: Clickable link
- title: Discussion title
- original_title: Original English if non-English
- key_quotes: [{user, quote, upvotes}]
- consensus_level: "high" | "medium" | "low" | "controversial"
- summary: Discussion summary (200-400 words)
- related_discussions: [urls]

ANALYSIS FOCUS:
- Consensus points (what everyone agrees on)
- Controversial topics (where opinions diverge)
- Practical recommendations (community-verified)
- Pain points and solutions

CHINESE COMMUNITY FOCUS:
- Zhihu, Juejin, WeChat articles
- "AutoGen快、CrewAI稳、LangGraph强" consensus
- MCP optimization best practices
- Context management techniques
"""

    def _citation_instructions(self) -> str:
        """Instructions for citation processing agent"""
        return """You are a citation specialist ensuring all references are properly formatted and verified.

OBJECTIVE:
Process all findings and add proper citations:
- Verify all URLs are accessible
- Format citations according to specification
- Add missing citation information
- Check for citation accuracy

CITATION FORMATS:
- Academic: [arXiv:ID](https://arxiv.org/abs/ID) | [PDF](https://arxiv.org/pdf/ID.pdf)
- GitHub: [org/repo](https://github.com/org/repo) ⭐ Xk+
- Web: [Title](URL)

QUALITY CHECKS:
- [ ] All URLs are complete and clickable
- [ ] All papers have both abstract and PDF links
- [ ] All GitHub repos have star count
- [ ] All discussions have engagement metrics
- [ ] No broken or placeholder links
"""

    def analyze_query_complexity(self, query: str) -> Dict[str, Any]:
        """
        Analyze research query to determine resource allocation

        Based on performance-aware decision criteria:
        - Single-agent success rate < threshold → Use multi-agent
        - Parallelizable aspects → Use multi-agent
        - Token cost: 15x for multi-agent vs single-agent

        Returns:
            Dict with: complexity_level, recommend_multi_agent, subagent_count, estimated_tokens
        """
        # Use threshold from settings
        threshold = self._multi_agent_threshold

        # Simple heuristic analysis
        keywords_indicating_complexity = [
            "comprehensive", "detailed", "in-depth", "analysis", "comparison",
            "vs", "versus", "framework", "architecture", "best practices",
            "evolution", "history", "state of the art", "sota"
        ]

        has_complexity_keywords = any(kw in query.lower() for kw in keywords_indicating_complexity)
        has_comparison = "vs" in query.lower() or "versus" in query.lower()
        word_count = len(query.split())

        # Calculate complexity score
        complexity_score = 0.0
        if has_complexity_keywords:
            complexity_score += 0.3
        if has_comparison:
            complexity_score += 0.4
        if word_count > 5:
            complexity_score += 0.2
        if word_count > 10:
            complexity_score += 0.1

        recommend_multi_agent = complexity_score >= threshold

        if complexity_score >= 0.7:
            return {
                "complexity_level": "high",
                "complexity_score": complexity_score,
                "recommend_multi_agent": recommend_multi_agent,
                "subagent_count": 5,
                "estimated_tokens": 150000,
                "threshold": threshold,
                "reason": "Comparison or complex analysis detected"
            }
        elif complexity_score >= 0.3:
            return {
                "complexity_level": "medium",
                "complexity_score": complexity_score,
                "recommend_multi_agent": recommend_multi_agent,
                "subagent_count": 3,
                "estimated_tokens": 100000,
                "threshold": threshold,
                "reason": "Multi-faceted query detected"
            }
        else:
            return {
                "complexity_level": "low",
                "complexity_score": complexity_score,
                "recommend_multi_agent": False,
                "subagent_count": 1,
                "estimated_tokens": 10000,
                "threshold": threshold,
                "reason": "Simple fact-finding query"
            }

    async def run_research(
        self,
        query: str,
        max_subagents: int = 5,
        parallel: bool = True,
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute multi-agent research workflow

        Args:
            query: Research topic or question
            max_subagents: Maximum subagents to spawn (recommend 3-5)
            parallel: Execute subagents in parallel (default True)
            output_dir: Directory for final reports

        Returns:
            Research findings with citations
        """
        # Use output_dir from settings if not provided
        if output_dir is None and settings:
            output_dir = settings.research_output_dir
        elif output_dir is None:
            output_dir = "research_output"

        # Initialize state
        state = ResearchState(query=query)
        complexity_analysis = self.analyze_query_complexity(query)

        # Save initial state
        self._save_state(state)

        # Phase 1: Planning (Lead agent analysis)
        print(f"[Phase 1] Analyzing query complexity: {complexity_analysis['complexity_level']}")
        print(f"  Score: {complexity_analysis.get('complexity_score', 0):.2f} / Threshold: {complexity_analysis.get('threshold', 0.45):.2f}")

        # Phase 2: Determine execution strategy
        if not complexity_analysis["recommend_multi_agent"]:
            print(f"[Phase 2] Single-agent sufficient: {complexity_analysis['reason']}")
            return {"message": "Use single-agent approach for this query"}

        # Phase 3: Parallel execution (Subagents)
        print(f"[Phase 3] Deploying {complexity_analysis['subagent_count']} subagents in parallel")

        if parallel:
            # In actual implementation, this would spawn Task agents
            results = await self._parallel_execute(query, state)
        else:
            results = await self._sequential_execute(query, state)

        # Phase 4: Synthesis would happen here
        print(f"[Phase 4] Synthesis - {len(results)} result streams collected")

        return {
            "session_id": state.session_id,
            "complexity_analysis": complexity_analysis,
            "state_file": str(self.state_dir / f"{state.session_id}_state.json"),
            "output_dir": output_dir
        }

    async def _parallel_execute(self, query: str, state: ResearchState) -> List[Dict]:
        """
        Execute subagents in parallel (90% speed improvement per Anthropic research)

        Supports both anyio TaskGroup and asyncio.gather for maximum compatibility.

        In actual Claude Code implementation, this would use Task tool:
        Task(subagent_type="academic-researcher", prompt="...")
        Task(subagent_type="github-watcher", prompt="...")
        Task(subagent_type="community-listener", prompt="...")
        """
        # Define agent tasks
        agent_roles = [
            (AgentRole.ACADEMIC, "academic-researcher"),
            (AgentRole.GITHUB, "github-watcher"),
            (AgentRole.COMMUNITY, "community-listener")
        ]

        results = []

        # Use anyio TaskGroup if available
        if ANYIO_AVAILABLE:
            async with create_task_group() as tg:
                for role, name in agent_roles:
                    tg.start_soon(self._run_agent_task, name, role, query, state, results)
        else:
            # Fallback to asyncio.gather
            tasks = [
                self._run_agent_task_async(name, role, query, state)
                for role, name in agent_roles
            ]
            gathered = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(gathered):
                if isinstance(result, Exception):
                    results.append({
                        "agent": agent_roles[i][1],
                        "status": "error",
                        "error": str(result)
                    })
                else:
                    results.append(result)

        return results

    async def _run_agent_task(
        self,
        name: str,
        role: AgentRole,
        query: str,
        state: ResearchState,
        results: List[Dict]
    ) -> None:
        """Run a single agent task and append result (for anyio TaskGroup)."""
        result = await self._run_agent_task_async(name, role, query, state)
        results.append(result)

    async def _run_agent_task_async(
        self,
        name: str,
        role: AgentRole,
        query: str,
        state: ResearchState
    ) -> Dict[str, Any]:
        """Run a single agent task."""
        # Apply rate limiting if available
        if self._rate_limiter:
            async with self._rate_limiter:
                # Simulate agent work
                await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(0.1)

        return {
            "agent": name,
            "role": role.value,
            "status": "deployed",
            "model": self.agents[role].model if role in self.agents else self._subagent_model
        }

    async def _sequential_execute(self, query: str, state: ResearchState) -> List[Dict]:
        """Execute subagents sequentially (fallback)"""
        results = []
        for role in [AgentRole.ACADEMIC, AgentRole.GITHUB, AgentRole.COMMUNITY]:
            # Apply rate limiting if available
            if self._rate_limiter:
                async with self._rate_limiter:
                    await asyncio.sleep(0.1)
            else:
                await asyncio.sleep(0.1)

            results.append({
                "agent": role.value,
                "status": "completed",
                "model": self.agents[role].model if role in self.agents else self._subagent_model
            })
        return results

    def _save_state(self, state: ResearchState):
        """Checkpoint state for resumability"""
        state_file = self.state_dir / f"{state.session_id}_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            f.write(state.to_json())

    def load_state(self, session_id: str) -> Optional[ResearchState]:
        """Restore from checkpoint"""
        state_file = self.state_dir / f"{session_id}_state.json"
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                return ResearchState.from_json(f.read())
        return None


class HandoffPattern:
    """
    Swarm-style handoff for agent switching

    Usage:
        def transfer_to_github_agent():
            return Handoff(target_agent=github_agent, context={"repo": "langgraph"})

        agent.functions.append(transfer_to_github_agent)
    """

    @staticmethod
    def create_handoff_function(target: Agent) -> Callable:
        """Create a handoff function for the given target agent"""
        def handoff(**kwargs) -> Handoff:
            return Handoff(target_agent=target, context=kwargs)
        handoff.__name__ = f"transfer_to_{target.name}"
        return handoff


class ResearchStateManager:
    """
    LangGraph-inspired state management with persistence

    Provides checkpoint/resume functionality for long-running research tasks
    """

    def __init__(self, state_dir: str = "research_data"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)

    def save_state(self, session_id: str, state: ResearchState):
        """Checkpoint state for resumability"""
        state_file = self.state_dir / f"{session_id}_state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            f.write(state.to_json())

    def load_state(self, session_id: str) -> Optional[ResearchState]:
        """Restore from checkpoint"""
        state_file = self.state_dir / f"{session_id}_state.json"
        if state_file.exists():
            with open(state_file, 'r', encoding='utf-8') as f:
                return ResearchState.from_json(f.read())
        return None

    def list_sessions(self) -> List[str]:
        """List all saved research sessions"""
        state_files = self.state_dir.glob("*_state.json")
        return [f.stem.replace("_state", "") for f in state_files]


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Agent Research Orchestrator")
    parser.add_argument("--query", type=str, required=True, help="Research query")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without executing")
    parser.add_argument("--output-dir", type=str, default="research_output", help="Output directory")
    parser.add_argument("--max-subagents", type=int, default=5, help="Maximum subagents")

    args = parser.parse_args()

    orchestrator = ResearchOrchestrator()

    if args.dry_run:
        analysis = orchestrator.analyze_query_complexity(args.query)
        print(json.dumps(analysis, indent=2))
    else:
        result = asyncio.run(orchestrator.run_research(
            query=args.query,
            max_subagents=args.max_subagents,
            output_dir=args.output_dir
        ))
        print(json.dumps(result, indent=2))
