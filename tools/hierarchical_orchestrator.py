"""
Hierarchical Multi-Agent Orchestrator v9.0

Based on:
- AgentOrchestra: A Hierarchical Multi-Agent Framework (arXiv:2506.12508)
- A Taxonomy of Hierarchical Multi-Agent Systems (arXiv:2508.12683)
- Tool-Environment-Agent (TEA) Protocol

This module implements a 3-layer hierarchical orchestration pattern:
1. Meta-Orchestrator Layer (Strategic): Query analysis, resource allocation, framework selection
2. Domain Layer (Coordination): Domain-specific coordination (Academic, GitHub, Community)
3. Worker Layer (Execution): Specialized executors (Paper Searcher, Code Explorer, Discussion Monitor)

Author: Deep Research System
Date: 2026-02-09
"""

from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from abc import ABC, abstractmethod
import uuid
import json
from datetime import datetime

from memory_system import MAGMAMemory


class OrchestrationLayer(Enum):
    """Orchestration layers in the hierarchy"""
    META_ORCHESTRATOR = "meta_orchestrator"  # Strategic layer
    DOMAIN_COORDINATOR = "domain_coordinator"  # Domain-specific coordination
    WORKER_EXECUTOR = "worker_executor"  # Specialized execution


class AgentCapability(Enum):
    """Agent capabilities for task assignment"""
    ACADEMIC_RESEARCH = "academic_research"
    GITHUB_ANALYSIS = "github_analysis"
    COMMUNITY_LISTENING = "community_listening"
    PAPER_SEARCH = "paper_search"
    CODE_EXPLORATION = "code_exploration"
    DISCUSSION_MONITORING = "discussion_monitoring"
    SYNTHESIS = "synthesis"
    QUALITY_ASSESSMENT = "quality_assessment"


@dataclass
class Task:
    """A task to be executed by an agent"""
    id: str
    description: str
    capability_required: AgentCapability
    priority: int = 1
    context: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 300
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, in_progress, completed, failed

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class AgentConfig:
    """Configuration for an agent"""
    id: str
    name: str
    layer: OrchestrationLayer
    capabilities: List[AgentCapability]
    model: str = "claude-sonnet-4-20250514"
    max_concurrent_tasks: int = 1
    tools: List[str] = field(default_factory=list)


@dataclass
class ExecutionResult:
    """Result from an agent execution"""
    task_id: str
    agent_id: str
    success: bool
    output: Dict[str, Any]
    error: Optional[str] = None
    execution_time_seconds: float = 0.0
    tokens_used: int = 0


class Agent(ABC):
    """Base class for all agents in the hierarchy"""

    def __init__(self, config: AgentConfig, memory: MAGMAMemory):
        """
        Initialize agent.

        Args:
            config: Agent configuration
            memory: Shared memory system
        """
        self.config = config
        self.memory = memory
        self.current_tasks: Dict[str, Task] = {}
        self.completed_tasks: List[ExecutionResult] = []

    @abstractmethod
    async def execute(self, task: Task) -> ExecutionResult:
        """Execute a task"""
        pass

    def can_handle(self, task: Task) -> bool:
        """Check if this agent can handle the task"""
        return task.capability_required in self.config.capabilities

    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_id": self.config.id,
            "layer": self.config.layer.value,
            "capabilities": [c.value for c in self.config.capabilities],
            "current_tasks": len(self.current_tasks),
            "completed_tasks": len(self.completed_tasks)
        }


class WorkerAgent(Agent):
    """
    Worker Layer Agent - Specialized Executor

    Specialized agents that execute specific tasks:
    - PaperSearcher: Search and retrieve academic papers
    - CodeExplorer: Analyze GitHub repositories
    - DiscussionMonitor: Monitor community discussions
    """

    def __init__(self, config: AgentConfig, memory: MAGMAMemory):
        super().__init__(config, memory)
        self.domain_specialty = config.capabilities[0].value if config.capabilities else ""

    async def execute(self, task: Task) -> ExecutionResult:
        """
        Execute a specialized task.

        In production, this would invoke Claude Code Task tool with appropriate subagent.
        """
        import time
        start_time = time.time()

        try:
            # Task execution based on capability
            if task.capability_required == AgentCapability.PAPER_SEARCH:
                output = await self._search_papers(task)
            elif task.capability_required == AgentCapability.CODE_EXPLORATION:
                output = await self._explore_code(task)
            elif task.capability_required == AgentCapability.DISCUSSION_MONITORING:
                output = await self._monitor_discussions(task)
            else:
                output = {"error": f"Unknown capability: {task.capability_required}"}

            execution_time = time.time() - start_time

            return ExecutionResult(
                task_id=task.id,
                agent_id=self.config.id,
                success=True,
                output=output,
                execution_time_seconds=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                task_id=task.id,
                agent_id=self.config.id,
                success=False,
                output={},
                error=str(e),
                execution_time_seconds=execution_time
            )

    async def _search_papers(self, task: Task) -> Dict[str, Any]:
        """Search for academic papers"""
        # In production: Use mcp__arxiv-mcp-server__search_papers
        query = task.context.get("query", "")
        categories = task.context.get("categories", ["cs.AI", "cs.LG"])
        max_results = task.context.get("max_results", 10)

        # Simulated output
        return {
            "papers_found": max_results,
            "query": query,
            "categories": categories,
            "papers": []  # Would contain actual paper data
        }

    async def _explore_code(self, task: Task) -> Dict[str, Any]:
        """Explore GitHub code"""
        # In production: Use mcp__zread__ tools
        repo = task.context.get("repo", "")
        return {
            "repo": repo,
            "files_analyzed": [],
            "architecture": ""
        }

    async def _monitor_discussions(self, task: Task) -> Dict[str, Any]:
        """Monitor community discussions"""
        # In production: Use web-reader and web-search
        platform = task.context.get("platform", "reddit")
        query = task.context.get("query", "")
        return {
            "platform": platform,
            "query": query,
            "discussions": []
        }


class DomainCoordinatorAgent(Agent):
    """
    Domain Layer Agent - Domain-Specific Coordination

    Coordinates workers within a specific domain:
    - AcademicLead: Coordinates paper searchers and analyzers
    - GitHubLead: Coordinates code explorers
    - CommunityLead: Coordinates discussion monitors
    """

    def __init__(self, config: AgentConfig, memory: MAGMAMemory, workers: List[WorkerAgent]):
        super().__init__(config, memory)
        self.workers = workers
        self.task_queue: List[Task] = []

    async def execute(self, task: Task) -> ExecutionResult:
        """
        Execute a domain-level task by delegating to workers.

        Implements the TEA Protocol:
        - Task decomposition
        - Worker assignment
        - Result aggregation
        """
        import time
        start_time = time.time()

        try:
            # Decompose task into subtasks for workers
            subtasks = self._decompose_task(task)

            # Assign to workers and execute in parallel
            results = await asyncio.gather(*[
                self._assign_to_worker(subtask)
                for subtask in subtasks
            ])

            # Aggregate results
            aggregated = self._aggregate_results(results)

            execution_time = time.time() - start_time

            return ExecutionResult(
                task_id=task.id,
                agent_id=self.config.id,
                success=True,
                output=aggregated,
                execution_time_seconds=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                task_id=task.id,
                agent_id=self.config.id,
                success=False,
                output={},
                error=str(e),
                execution_time_seconds=execution_time
            )

    def _decompose_task(self, task: Task) -> List[Task]:
        """Decompose a domain task into worker tasks"""
        subtasks = []

        if task.capability_required == AgentCapability.ACADEMIC_RESEARCH:
            # Decompose into paper search tasks
            subtasks.append(Task(
                id="",
                description="Search for root papers",
                capability_required=AgentCapability.PAPER_SEARCH,
                context={**task.context, "paper_type": "root"},
                priority=1
            ))
            subtasks.append(Task(
                id="",
                description="Search for survey papers",
                capability_required=AgentCapability.PAPER_SEARCH,
                context={**task.context, "paper_type": "survey"},
                priority=2
            ))

        elif task.capability_required == AgentCapability.GITHUB_ANALYSIS:
            subtasks.append(Task(
                id="",
                description="Explore repository code",
                capability_required=AgentCapability.CODE_EXPLORATION,
                context=task.context,
                priority=1
            ))

        elif task.capability_required == AgentCapability.COMMUNITY_LISTENING:
            subtasks.append(Task(
                id="",
                description="Monitor discussions",
                capability_required=AgentCapability.DISCUSSION_MONITORING,
                context=task.context,
                priority=1
            ))

        return subtasks

    async def _assign_to_worker(self, task: Task) -> ExecutionResult:
        """Assign task to an appropriate worker"""
        for worker in self.workers:
            if worker.can_handle(task) and len(worker.current_tasks) < worker.config.max_concurrent_tasks:
                worker.current_tasks[task.id] = task
                result = await worker.execute(task)
                del worker.current_tasks[task.id]
                worker.completed_tasks.append(result)
                return result

        # No available worker
        return ExecutionResult(
            task_id=task.id,
            agent_id=self.config.id,
            success=False,
            output={},
            error="No available worker"
        )

    def _aggregate_results(self, results: List[ExecutionResult]) -> Dict[str, Any]:
        """Aggregate results from workers"""
        aggregated = {
            "total_workers": len(results),
            "successful": sum(1 for r in results if r.success),
            "failed": sum(1 for r in results if not r.success),
            "outputs": [r.output for r in results if r.success],
            "errors": [r.error for r in results if not r.success]
        }
        return aggregated


class MetaOrchestratorAgent(Agent):
    """
    Meta-Orchestrator Layer - Strategic Coordination

    Highest level agent responsible for:
    - Query analysis and complexity assessment
    - Resource allocation (performance-aware)
    - Framework selection
    - Domain coordinator assignment
    - Result synthesis
    """

    def __init__(
        self,
        config: AgentConfig,
        memory: MAGMAMemory,
        domain_coordinators: List[DomainCoordinatorAgent]
    ):
        super().__init__(config, memory)
        self.domain_coordinators = domain_coordinators
        self.decision_history: List[Dict[str, Any]] = []

    async def execute(self, task: Task) -> ExecutionResult:
        """
        Execute a strategic research task.

        Workflow:
        1. Analyze query complexity
        2. Determine resource allocation
        3. Select framework/pattern
        4. Assign to domain coordinators
        5. Synthesize results
        """
        import time
        start_time = time.time()

        try:
            # Step 1: Analyze query
            query_analysis = self._analyze_query(task)

            # Step 2: Determine strategy
            strategy = self._determine_strategy(query_analysis)

            # Step 3: Create domain tasks
            domain_tasks = self._create_domain_tasks(task, strategy)

            # Step 4: Execute in parallel
            results = await asyncio.gather(*[
                self._assign_to_coordinator(domain_task)
                for domain_task in domain_tasks
            ])

            # Step 5: Synthesize
            synthesized = self._synthesize_results(results, query_analysis)

            execution_time = time.time() - start_time

            # Record decision
            self.decision_history.append({
                "timestamp": datetime.now().isoformat(),
                "query_analysis": query_analysis,
                "strategy": strategy,
                "execution_time": execution_time
            })

            return ExecutionResult(
                task_id=task.id,
                agent_id=self.config.id,
                success=True,
                output=synthesized,
                execution_time_seconds=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutionResult(
                task_id=task.id,
                agent_id=self.config.id,
                success=False,
                output={},
                error=str(e),
                execution_time_seconds=execution_time
            )

    def _analyze_query(self, task: Task) -> Dict[str, Any]:
        """
        Analyze query to determine complexity and resource needs.

        Based on performance-aware decision criteria from research.
        """
        query = task.description

        # Complexity indicators
        complexity_keywords = [
            "comprehensive", "detailed", "in-depth", "analysis",
            "vs", "versus", "comparison", "framework", "architecture"
        ]

        has_complexity = any(kw in query.lower() for kw in complexity_keywords)
        word_count = len(query.split())

        # Estimate single-agent success rate
        if has_complexity or word_count > 5:
            estimated_success = 0.35  # Below 45% threshold
        else:
            estimated_success = 0.60  # Above threshold

        return {
            "query": query,
            "complexity_level": "high" if has_complexity else "low",
            "estimated_single_agent_success": estimated_success,
            "parallelizable_aspects": self._assess_parallelizability(query),
            "word_count": word_count
        }

    def _assess_parallelizability(self, query: str) -> List[str]:
        """Assess which aspects can be parallelized"""
        aspects = []

        if any(kw in query.lower() for kw in ["paper", "academic", "research"]):
            aspects.append("academic_research")

        if any(kw in query.lower() for kw in ["github", "code", "implementation"]):
            aspects.append("github_analysis")

        if any(kw in query.lower() for kw in ["community", "discussion", "consensus"]):
            aspects.append("community_listening")

        return aspects

    def _determine_strategy(self, query_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine execution strategy based on query analysis.

        Decision framework based on research:
        - Single-agent success < 45% → Use multi-agent
        - Parallelizable aspects → Use hierarchical
        - Token cost: 15x for multi-agent but 90.2% improvement
        """
        success_rate = query_analysis["estimated_single_agent_success"]
        parallelizable = query_analysis["parallelizable_aspects"]

        if success_rate < 0.45 and len(parallelizable) >= 2:
            return {
                "approach": "hierarchical_multi_agent",
                "reason": "Below 45% threshold with multiple parallelizable aspects",
                "expected_improvement": "+90.2%",
                "token_multiplier": "15x",
                "domains_to_deploy": parallelizable
            }
        elif success_rate < 0.45:
            return {
                "approach": "single_domain_multi_agent",
                "reason": "Below 45% threshold but limited parallelizability",
                "expected_improvement": "+50-80%",
                "token_multiplier": "8x",
                "domains_to_deploy": parallelizable
            }
        else:
            return {
                "approach": "single_agent",
                "reason": "Above 45% success threshold",
                "expected_improvement": "baseline",
                "token_multiplier": "1x",
                "domains_to_deploy": []
            }

    def _create_domain_tasks(
        self,
        original_task: Task,
        strategy: Dict[str, Any]
    ) -> List[Task]:
        """Create tasks for domain coordinators"""
        domain_tasks = []

        for domain in strategy.get("domains_to_deploy", []):
            if domain == "academic_research":
                domain_tasks.append(Task(
                    id="",
                    description=f"Academic research: {original_task.description}",
                    capability_required=AgentCapability.ACADEMIC_RESEARCH,
                    context=original_task.context,
                    priority=1
                ))
            elif domain == "github_analysis":
                domain_tasks.append(Task(
                    id="",
                    description=f"GitHub analysis: {original_task.description}",
                    capability_required=AgentCapability.GITHUB_ANALYSIS,
                    context=original_task.context,
                    priority=1
                ))
            elif domain == "community_listening":
                domain_tasks.append(Task(
                    id="",
                    description=f"Community monitoring: {original_task.description}",
                    capability_required=AgentCapability.COMMUNITY_LISTENING,
                    context=original_task.context,
                    priority=1
                ))

        return domain_tasks

    async def _assign_to_coordinator(self, task: Task) -> ExecutionResult:
        """Assign task to appropriate domain coordinator"""
        for coordinator in self.domain_coordinators:
            if coordinator.can_handle(task):
                return await coordinator.execute(task)

        return ExecutionResult(
            task_id=task.id,
            agent_id=self.config.id,
            success=False,
            output={},
            error="No suitable domain coordinator"
        )

    def _synthesize_results(
        self,
        results: List[ExecutionResult],
        query_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize results from domain coordinators"""
        synthesized = {
            "query_analysis": query_analysis,
            "domains_completed": len([r for r in results if r.success]),
            "total_outputs": {},
            "execution_summary": {}
        }

        for result in results:
            if result.success:
                synthesized["total_outputs"][result.agent_id] = result.output

        # Calculate performance metrics
        total_time = sum(r.execution_time_seconds for r in results)
        synthesized["execution_summary"] = {
            "total_time_seconds": total_time,
            "average_time_seconds": total_time / len(results) if results else 0,
            "successful_domains": sum(1 for r in results if r.success),
            "failed_domains": sum(1 for r in results if not r.success)
        }

        return synthesized


class HierarchicalOrchestrator:
    """
    Hierarchical Multi-Agent Orchestrator

    Main entry point for the hierarchical orchestration system.
    Creates and manages the three-layer hierarchy.
    """

    def __init__(self, memory: Optional[MAGMAMemory] = None):
        """
        Initialize hierarchical orchestrator.

        Args:
            memory: Optional shared memory system
        """
        self.memory = memory or MAGMAMemory()

        # Build hierarchy
        self._build_hierarchy()

    def _build_hierarchy(self):
        """Build the three-layer hierarchy"""

        # Worker Layer - Specialized executors
        self.worker_agents = {
            "paper_searcher": WorkerAgent(
                AgentConfig(
                    id="paper_searcher",
                    name="Paper Searcher",
                    layer=OrchestrationLayer.WORKER_EXECUTOR,
                    capabilities=[AgentCapability.PAPER_SEARCH],
                    tools=["mcp__arxiv-mcp-server__search_papers"]
                ),
                self.memory
            ),
            "code_explorer": WorkerAgent(
                AgentConfig(
                    id="code_explorer",
                    name="Code Explorer",
                    layer=OrchestrationLayer.WORKER_EXECUTOR,
                    capabilities=[AgentCapability.CODE_EXPLORATION],
                    tools=["mcp__zread__get_repo_structure", "mcp__zread__read_file"]
                ),
                self.memory
            ),
            "discussion_monitor": WorkerAgent(
                AgentConfig(
                    id="discussion_monitor",
                    name="Discussion Monitor",
                    layer=OrchestrationLayer.WORKER_EXECUTOR,
                    capabilities=[AgentCapability.DISCUSSION_MONITORING],
                    tools=["mcp__web-reader__webReader", "mcp__web-search-prime__webSearchPrime"]
                ),
                self.memory
            )
        }

        # Domain Layer - Domain coordinators
        academic_workers = [self.worker_agents["paper_searcher"]]
        github_workers = [self.worker_agents["code_explorer"]]
        community_workers = [self.worker_agents["discussion_monitor"]]

        self.domain_coordinators = {
            "academic_lead": DomainCoordinatorAgent(
                AgentConfig(
                    id="academic_lead",
                    name="Academic Lead",
                    layer=OrchestrationLayer.DOMAIN_COORDINATOR,
                    capabilities=[AgentCapability.ACADEMIC_RESEARCH],
                    model="claude-sonnet-4-20250514"
                ),
                self.memory,
                academic_workers
            ),
            "github_lead": DomainCoordinatorAgent(
                AgentConfig(
                    id="github_lead",
                    name="GitHub Lead",
                    layer=OrchestrationLayer.DOMAIN_COORDINATOR,
                    capabilities=[AgentCapability.GITHUB_ANALYSIS],
                    model="claude-sonnet-4-20250514"
                ),
                self.memory,
                github_workers
            ),
            "community_lead": DomainCoordinatorAgent(
                AgentConfig(
                    id="community_lead",
                    name="Community Lead",
                    layer=OrchestrationLayer.DOMAIN_COORDINATOR,
                    capabilities=[AgentCapability.COMMUNITY_LISTENING],
                    model="claude-sonnet-4-20250514"
                ),
                self.memory,
                community_workers
            )
        }

        # Meta-Orchestrator Layer - Strategic coordination
        self.meta_orchestrator = MetaOrchestratorAgent(
            AgentConfig(
                id="meta_orchestrator",
                name="Meta Orchestrator",
                layer=OrchestrationLayer.META_ORCHESTRATOR,
                capabilities=[
                    AgentCapability.ACADEMIC_RESEARCH,
                    AgentCapability.GITHUB_ANALYSIS,
                    AgentCapability.COMMUNITY_LISTENING,
                    AgentCapability.SYNTHESIS
                ],
                model="claude-opus-4-5-20250514",
                max_concurrent_tasks=5
            ),
            self.memory,
            list(self.domain_coordinators.values())
        )

    async def execute_research(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a research query through the hierarchy.

        Args:
            query: Research query
            context: Optional context for the research

        Returns:
            Research results with synthesis
        """
        # Start a new session
        session_id = self.memory.start_session(query)

        # Create strategic task
        task = Task(
            id="",
            description=query,
            capability_required=AgentCapability.SYNTHESIS,
            context=context or {},
            priority=1
        )

        # Execute through meta-orchestrator
        result = await self.meta_orchestrator.execute(task)

        # End session and get summary
        session_summary = self.memory.end_session()

        return {
            "session_id": session_id,
            "result": result.output,
            "execution_time": result.execution_time_seconds,
            "success": result.success,
            "session_summary": session_summary
        }

    def get_hierarchy_status(self) -> Dict[str, Any]:
        """Get status of all agents in the hierarchy"""
        return {
            "meta_orchestrator": self.meta_orchestrator.get_status(),
            "domain_coordinators": {
                name: coord.get_status()
                for name, coord in self.domain_coordinators.items()
            },
            "worker_agents": {
                name: worker.get_status()
                for name, worker in self.worker_agents.items()
            }
        }


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hierarchical Multi-Agent Orchestrator v9.0")
    parser.add_argument("--query", type=str, help="Research query to execute")
    parser.add_argument("--status", action="store_true", help="Show hierarchy status")

    args = parser.parse_args()

    orchestrator = HierarchicalOrchestrator()

    if args.status:
        status = orchestrator.get_hierarchy_status()
        print(json.dumps(status, indent=2))

    elif args.query:
        import asyncio
        result = asyncio.run(orchestrator.execute_research(args.query))
        print(json.dumps(result, indent=2))

    else:
        print("Hierarchical Orchestrator v9.0")
        print("Use --query to execute research or --status to see hierarchy")
