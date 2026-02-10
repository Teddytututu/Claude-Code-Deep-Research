"""
Checkpoint Manager for Deep Research System v9.2

Shared checkpoint utilities for all research agents.
Provides incremental writing, resume capability, and progress tracking.

v9.1: Time-aware checkpointing with automatic time budget tracking
v9.2: Continuation support - load checkpoints for interrupted subagents
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


class CheckpointManager:
    """
    渐进式写入器 - 边查边写 (Progressive Writer)

    Incremental checkpoint manager for research agents.
    Writes findings immediately to prevent data loss from context limits.

    Features:
    - Incremental writing (no context loss)
    - Resume capability
    - Real-time progress tracking
    - Multi-agent coordination
    - Time-aware checkpointing (v9.1)
    - Continuation support for interrupted agents (v9.2)
    """

    def __init__(
        self,
        agent_type: str,
        output_dir: str = "research_data/checkpoints",
        output_file: Optional[str] = None,
        start_time_iso: Optional[str] = None,
        budget_seconds: Optional[int] = None
    ):
        """
        Initialize checkpoint manager.

        Args:
            agent_type: Type of agent (academic-researcher, github-watcher, etc.)
            output_dir: Directory for checkpoint files
            output_file: Optional final output file path
            start_time_iso: ISO format start time (for time-aware checkpointing)
            budget_seconds: Time budget in seconds (for time-aware checkpointing)
        """
        self.agent_type = agent_type
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = output_file or f"research_data/{agent_type}_output.json"
        self.checkpoint_count = 0
        self.items_processed = 0

        # Time tracking (v9.1)
        self.start_time_iso = start_time_iso
        self.budget_seconds = budget_seconds
        if start_time_iso:
            try:
                self.start_time = datetime.fromisoformat(start_time_iso)
            except (ValueError, TypeError):
                self.start_time = datetime.now()
                self.start_time_iso = self.start_time.isoformat()
        else:
            self.start_time = datetime.now()
            self.start_time_iso = self.start_time.isoformat()

        # Load existing data if resuming
        self.data = self._load_existing()

    def _load_existing(self) -> Dict[str, Any]:
        """Load existing data (supports resume)."""
        output_path = Path(self.output_file)
        if output_path.exists():
            try:
                with open(output_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass

        return self._empty_data_structure()

    def _empty_data_structure(self) -> Dict[str, Any]:
        """Create empty data structure."""
        return {
            "subagent_metadata": {
                "agent_type": self.agent_type,
                "progressive_writing": True,
                "checkpoints": [],
                "version": "9.0"
            },
            "research_findings": self._empty_findings(),
            "items": []
        }

    def _empty_findings(self) -> Dict[str, Any]:
        """Create empty findings structure based on agent type."""
        if self.agent_type == "academic-researcher":
            return {
                "papers_analyzed": 0,
                "papers_with_full_text": 0,
                "citation_network_built": False,
                "key_papers": []
            }
        elif self.agent_type == "github-watcher":
            return {
                "projects_analyzed": 0,
                "technology_factions_identified": 0,
                "architecture_patterns_found": [],
                "key_projects": []
            }
        elif self.agent_type == "community-listener":
            return {
                "threads_analyzed": 0,
                "platforms_covered": [],
                "consensus_points": [],
                "controversial_topics": []
            }
        return {}

    def write_checkpoint(
        self,
        phase: str,
        content: Dict[str, Any],
        items: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Write checkpoint with metadata.

        Args:
            phase: Research phase identifier (e.g., "phase1_broad_exploration")
            content: Checkpoint content (findings, summary, etc.)
            items: Optional list of items to include

        Returns:
            Confirmation message with time assessment if time budget is set
        """
        self.checkpoint_count += 1
        timestamp = time.time()
        current_time = datetime.fromtimestamp(timestamp)

        checkpoint = {
            "checkpoint_number": self.checkpoint_count,
            "checkpoint_id": f"{self.agent_type.replace('-', '_')}_{self.checkpoint_count:03d}",
            "phase": phase,
            "timestamp": timestamp,
            "timestamp_iso": current_time.isoformat(),
            "items_processed": self.items_processed,
            "content": content
        }

        # Add time assessment if budget is set (v9.1)
        if self.budget_seconds:
            time_assessment = self._calculate_time_assessment(current_time)
            checkpoint["time_assessment"] = time_assessment

        if items:
            checkpoint["items"] = items
            # Also add to main items list
            self.data["items"].extend(items)
            self.items_processed += len(items)

        self.data["subagent_metadata"]["checkpoints"].append(checkpoint)
        self._save()

        msg = f"Checkpoint {self.checkpoint_count} written for phase: {phase}"
        if self.budget_seconds:
            time_assess = checkpoint.get("time_assessment", {})
            remaining = time_assess.get("remaining_formatted", "unknown")
            status = time_assess.get("time_status", "unknown")
            msg += f" | Time: {remaining} remaining ({status})"

        return msg

    def _calculate_time_assessment(self, current_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Calculate time assessment for checkpoint (v9.1).

        Args:
            current_time: Current datetime (defaults to now)

        Returns:
            Dictionary with time assessment data
        """
        if current_time is None:
            current_time = datetime.now()

        elapsed = (current_time - self.start_time).total_seconds()
        remaining = self.budget_seconds - elapsed
        progress = (elapsed / self.budget_seconds) * 100 if self.budget_seconds > 0 else 0

        # Calculate items per minute
        items_per_minute = 0
        if elapsed > 0 and self.items_processed > 0:
            items_per_minute = round(self.items_processed / (elapsed / 60), 2)

        # Estimate completion time
        if remaining > 0:
            estimated_completion = (current_time + timedelta(seconds=remaining)).isoformat()
        else:
            estimated_completion = "overdue"

        # Determine time status
        if remaining < 0:
            time_status = "overtime"
        elif remaining < 300:  # Less than 5 minutes
            time_status = "time_critical"
        elif remaining < self.budget_seconds * 0.25:  # Less than 25%
            time_status = "warning"
        else:
            time_status = "on_track"

        return {
            "start_time": self.start_time_iso,
            "current_time": current_time.isoformat(),
            "elapsed_seconds": int(elapsed),
            "elapsed_formatted": f"{int(elapsed // 60)} minutes {int(elapsed % 60)}s",
            "remaining_seconds": int(remaining),
            "remaining_formatted": f"{int(remaining // 60)} minutes {int(remaining % 60)}s",
            "budget_seconds": self.budget_seconds,
            "budget_formatted": f"{int(self.budget_seconds // 60)} minutes",
            "progress_percentage": round(progress, 2),
            "time_status": time_status,
            "items_per_minute": items_per_minute,
            "estimated_completion": estimated_completion
        }

    def get_time_assessment(self) -> Optional[Dict[str, Any]]:
        """
        Get current time assessment without writing checkpoint (v9.1).

        Returns:
            Time assessment dict or None if no budget set
        """
        if self.budget_seconds:
            return self._calculate_time_assessment()
        return None

    def is_time_critical(self) -> bool:
        """
        Check if time is critical (less than 5 minutes remaining) (v9.1).

        Returns:
            True if less than 300 seconds remaining
        """
        if not self.budget_seconds:
            return False

        elapsed = (datetime.now() - self.start_time).total_seconds()
        remaining = self.budget_seconds - elapsed
        return remaining < 300

    def should_accelerate(self) -> bool:
        """
        Check if should enter accelerate mode (v9.1).

        Returns:
            True if should accelerate (time critical or overtime)
        """
        if not self.budget_seconds:
            return False

        elapsed = (datetime.now() - self.start_time).total_seconds()
        remaining = self.budget_seconds - elapsed
        return remaining < 300  # 5 minutes threshold

    def add_item(self, item: Dict[str, Any]) -> str:
        """
        Add single item immediately (边发现边写).

        Args:
            item: Item to add (paper, project, discussion, etc.)

        Returns:
            Confirmation message
        """
        self.data["items"].append(item)
        self.items_processed += 1
        self._update_findings()
        self._save()

        item_id = item.get('arxiv_id') or item.get('name') or item.get('url', 'unknown')
        return f"Item added: {item_id} (Total: {len(self.data['items'])})"

    def add_items(self, items: List[Dict[str, Any]]) -> str:
        """
        Add multiple items immediately.

        Args:
            items: List of items to add

        Returns:
            Confirmation message
        """
        self.data["items"].extend(items)
        self.items_processed += len(items)
        self._update_findings()
        self._save()

        return f"Items added: {len(items)} items (Total: {len(self.data['items'])})"

    def _update_findings(self):
        """Update findings metadata based on items processed."""
        findings = self.data["research_findings"]

        if self.agent_type == "academic-researcher":
            findings["papers_analyzed"] = len([
                i for i in self.data["items"]
                if i.get("has_full_text") or i.get("abstract")
            ])
            findings["papers_with_full_text"] = len([
                i for i in self.data["items"]
                if i.get("has_full_text")
            ])
        elif self.agent_type == "github-watcher":
            findings["projects_analyzed"] = len(self.data["items"])
        elif self.agent_type == "community-listener":
            findings["threads_analyzed"] = len(self.data["items"])

    def update_metadata(self, updates: Dict[str, Any]):
        """Update metadata fields."""
        self.data["subagent_metadata"].update(updates)
        self._save()

    def finalize(
        self,
        citation_network: Optional[Dict[str, Any]] = None,
        gaps: Optional[List[str]] = None,
        recommendations: Optional[List[str]] = None
    ) -> str:
        """
        Finalize research and create final checkpoint.

        Args:
            citation_network: Optional citation network data
            gaps: Optional gaps identified
            recommendations: Optional recommendations

        Returns:
            Confirmation message
        """
        # Create final checkpoint
        final_checkpoint = {
            "checkpoint_number": self.checkpoint_count + 1,
            "checkpoint_id": f"{self.agent_type.replace('-', '_')}_FINAL",
            "phase": "final",
            "timestamp": time.time(),
            "timestamp_iso": datetime.now().isoformat(),
            "items_processed": self.items_processed,
            "status": "complete"
        }

        self.data["subagent_metadata"]["checkpoints"].append(final_checkpoint)

        # Add optional final data
        if citation_network:
            self.data["citation_network"] = citation_network
        if gaps:
            self.data["gaps_identified"] = gaps
        if recommendations:
            self.data["recommendations_for_lead"] = recommendations

        self.data["subagent_metadata"]["status"] = "complete"
        self._save()

        return f"Final checkpoint created: {final_checkpoint['checkpoint_id']}"

    def _save(self):
        """Save to file."""
        output_path = Path(self.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def list_checkpoints(self) -> List[str]:
        """List all checkpoints for this agent."""
        checkpoint_dir = self.output_dir
        if not checkpoint_dir.exists():
            return []
        return sorted(checkpoint_dir.glob(f"{self.agent_type.replace('-', '_')}_*.json"))

    def get_progress(self) -> Dict[str, Any]:
        """Get current progress status."""
        return {
            "agent_type": self.agent_type,
            "items_processed": self.items_processed,
            "checkpoints_written": self.checkpoint_count,
            "status": self.data["subagent_metadata"].get("status", "in_progress")
        }


class LaTeXConverter:
    """
    LaTeX Formula Converter for v9.0

    Converts various formula formats to LaTeX for consistent rendering.
    """

    @staticmethod
    def convert_inline(formula_text: str) -> str:
        """
        Convert formula to inline LaTeX format ($...$).

        Examples:
            "O(n^2)" → "$O(n^2)$"
            "n*(n-1)/2" → "$\\frac{n(n-1)}{2}$"
        """
        # Remove existing markdown code blocks
        formula_text = formula_text.strip()
        if formula_text.startswith("```") and formula_text.endswith("```"):
            formula_text = formula_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()

        # Add LaTeX delimiters if not present
        if not (formula_text.startswith("$") and formula_text.endswith("$")):
            formula_text = f"${formula_text}$"

        return formula_text

    @staticmethod
    def convert_block(formula_text: str) -> str:
        """
        Convert formula to block LaTeX format ($$...$$).

        Examples:
            "Cost = Tokens / 1000" → "$$Cost = \\frac{Tokens}{1000}$$"
        """
        # Remove existing markdown code blocks
        formula_text = formula_text.strip()
        if formula_text.startswith("```") and formula_text.endswith("```"):
            formula_text = formula_text.split("\n", 1)[1].rsplit("\n", 1)[0].strip()

        # Add LaTeX delimiters for block
        if not (formula_text.startswith("$$") and formula_text.endswith("$$")):
            formula_text = f"$$\n{formula_text}\n$$"

        return formula_text

    @staticmethod
    def convert_fractions(expression: str) -> str:
        """
        Convert division expressions to LaTeX fractions.

        Examples:
            "n(n-1)/2" → "\\frac{n(n-1)}{2}"
            "Tokens / 1000" → "\\frac{Tokens}{1000}"
        """
        import re

        # Match pattern: numerator/denominator
        pattern = r'([a-zA-Z0-9_\(\)\[\]\{\}\+\-\*\^\.]+)\s*/\s*([a-zA-Z0-9_\(\)\[\]\{\}\+\-\*\^\.]+)'

        def replace_fraction(match):
            numerator = match.group(1).strip()
            denominator = match.group(2).strip()
            return f"\\frac{{{numerator}}}{{{denominator}}}"

        return re.sub(pattern, replace_fraction, expression)

    @staticmethod
    def ensure_latex_format(formula: str, inline: bool = True) -> str:
        """
        Ensure formula is in proper LaTeX format.

        Args:
            formula: Formula text
            inline: True for inline ($...$), False for block ($$...$$)

        Returns:
            Properly formatted LaTeX formula
        """
        # Convert fractions first
        formula = LaTeXConverter.convert_fractions(formula)

        # Add delimiters
        if inline:
            return LaTeXConverter.convert_inline(formula)
        else:
            return LaTeXConverter.convert_block(formula)


# Convenience function for creating checkpoint manager
def create_checkpoint_manager(
    agent_type: str,
    output_dir: str = "research_data/checkpoints",
    start_time_iso: Optional[str] = None,
    budget_seconds: Optional[int] = None
) -> CheckpointManager:
    """
    Create a checkpoint manager for the specified agent type.

    Args:
        agent_type: Type of agent (academic-researcher, github-watcher, etc.)
        output_dir: Directory for checkpoint files
        start_time_iso: ISO format start time (for time-aware checkpointing)
        budget_seconds: Time budget in seconds (for time-aware checkpointing)

    Returns:
        CheckpointManager instance
    """
    return CheckpointManager(agent_type, output_dir, None, start_time_iso, budget_seconds)


def parse_time_from_prompt(prompt: str) -> Optional[Dict[str, Any]]:
    """
    Parse time budget from LeadResearcher prompt (v9.1).

    Args:
        prompt: The prompt string from LeadResearcher

    Returns:
        Dict with start_time_iso and budget_seconds, or None if not found
    """
    import re

    # Extract start_time_iso
    start_time_match = re.search(r'start_time_iso:\s*([^\n]+)', prompt)
    start_time_iso = start_time_match.group(1).strip() if start_time_match else None

    # Extract per_agent_timeout_seconds
    timeout_match = re.search(r'per_agent_timeout_seconds:\s*(\d+)', prompt)
    budget_seconds = int(timeout_match.group(1)) if timeout_match else None

    if start_time_iso and budget_seconds:
        return {
            "start_time_iso": start_time_iso,
            "budget_seconds": budget_seconds
        }
    return None


def get_latest_checkpoint(agent_type: str) -> Optional[Dict[str, Any]]:
    """
    Get the latest checkpoint for an agent (v9.2).

    This helper function is used by CLAUDE.md to retrieve checkpoint data
    for continuation when a subagent is interrupted.

    Args:
        agent_type: Type of agent (academic-researcher, github-watcher, etc.)

    Returns:
        Latest checkpoint dict or None if no checkpoints found
    """
    checkpoint_dir = Path("research_data/checkpoints")
    if not checkpoint_dir.exists():
        return None

    # Find all checkpoints for this agent
    pattern = f"{agent_type.replace('-', '_')}_*.json"
    checkpoints = sorted(checkpoint_dir.glob(pattern))

    if not checkpoints:
        return None

    # Load the latest checkpoint
    latest = checkpoints[-1]
    try:
        with open(latest, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def get_agent_progress(agent_type: str) -> Dict[str, Any]:
    """
    Get current progress of an agent (v9.2).

    Returns the number of items processed and whether minimum requirements
    have been met.

    Args:
        agent_type: Type of agent (academic-researcher, github-watcher, etc.)

    Returns:
        Dict with progress info: items_processed, meets_minimum, remaining, etc.
    """
    output_file = f"research_data/{agent_type}_output.json"
    output_path = Path(output_file)

    if not output_path.exists():
        return {
            "agent_type": agent_type,
            "items_processed": 0,
            "meets_minimum": False,
            "status": "not_started"
        }

    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "agent_type": agent_type,
            "items_processed": 0,
            "meets_minimum": False,
            "status": "error"
        }

    findings = data.get("research_findings", {})
    items = data.get("items", [])

    # Minimum requirements
    MINIMUM_REQUIREMENTS = {
        "academic-researcher": {"papers_analyzed": 5},
        "github-watcher": {"projects_analyzed": 8},
        "community-listener": {"threads_analyzed": 15}
    }

    requirements = MINIMUM_REQUIREMENTS.get(agent_type, {})
    remaining = {}
    meets_minimum = True

    for key, min_value in requirements.items():
        current_value = findings.get(key, len(items))
        if current_value < min_value:
            meets_minimum = False
            remaining[key] = {
                "current": current_value,
                "required": min_value,
                "remaining": min_value - current_value
            }

    return {
        "agent_type": agent_type,
        "items_processed": len(items),
        "findings": findings,
        "meets_minimum": meets_minimum,
        "remaining": remaining,
        "status": data.get("subagent_metadata", {}).get("status", "in_progress")
    }


def load_checkpoint_for_continuation(agent_type: str) -> Optional[Dict[str, Any]]:
    """
    Load checkpoint data for agent continuation (v9.2).

    Returns a formatted continuation summary that can be passed to
    a relaunching agent.

    Args:
        agent_type: Type of agent to continue

    Returns:
        Continuation data dict with checkpoint info and next steps
    """
    checkpoint = get_latest_checkpoint(agent_type)
    if not checkpoint:
        return None

    progress = get_agent_progress(agent_type)

    # Extract the last checkpoint entry from metadata if available
    checkpoints = checkpoint.get("subagent_metadata", {}).get("checkpoints", [])
    last_checkpoint = checkpoints[-1] if checkpoints else None

    if last_checkpoint:
        time_assessment = last_checkpoint.get("time_assessment", {})
        content = last_checkpoint.get("content", {})
    else:
        time_assessment = {}
        content = {}

    return {
        "agent_type": agent_type,
        "checkpoint_number": last_checkpoint.get("checkpoint_number") if last_checkpoint else 0,
        "phase": last_checkpoint.get("phase") if last_checkpoint else "unknown",
        "timestamp": last_checkpoint.get("timestamp_iso") if last_checkpoint else "",
        "items_processed": progress.get("items_processed", 0),
        "meets_minimum": progress.get("meets_minimum", False),
        "remaining_requirements": progress.get("remaining", {}),
        "time_assessment": time_assessment,
        "work_summary": content.get("work_summary", ""),
        "next_steps": content.get("next_steps", []),
        "checkpoint_file": f"research_data/checkpoints/{agent_type.replace('-', '_')}_FINAL.json"
    }


# ============================================================================
# Time Budget Management Functions (v9.3)
# ============================================================================

def parse_time_budget(user_query: str) -> Optional[Dict[str, Any]]:
    """
    Parse time budget from user query (v9.3).

    Supports both Chinese and English time formats:
    - Chinese: "给我1小时", "30分钟", "限时2小时"
    - English: "in 1 hour", "30 minutes", "1h", "30min", "deadline: 2h"

    Args:
        user_query: The user's query string

    Returns:
        Dict with total_seconds, total_minutes, and source, or None if no time specified
    """
    import re

    query_lower = user_query.lower()

    # Pattern 1: Explicit "X hour/minute" format (e.g., "1 hour", "30 minutes", "2h", "90min")
    explicit_pattern = r'(\d+(?:\.\d+)?)\s*(hour|hr|h|minute|min|m)'
    matches = re.findall(explicit_pattern, query_lower)
    if matches:
        total_minutes = 0
        for value, unit in matches:
            value = float(value)
            if unit.startswith('h'):
                total_minutes += value * 60
            else:  # minute/min/m
                total_minutes += value
        return {
            "total_seconds": int(total_minutes * 60),
            "total_minutes": int(total_minutes),
            "source": "explicit_specification"
        }

    # Pattern 2: Chinese format "给我X小时" / "限时X小时"
    chinese_pattern = r'(?:给我|限时?|时间限制?:?|研究时间|deadline\s*:?)\s*(\d+(?:\.\d+)?)\s*(小时|小时?|分钟|min|m)'
    cn_match = re.search(chinese_pattern, user_query)
    if cn_match:
        value = float(cn_match.group(1))
        unit = cn_match.group(2).lower()
        if '小时' in unit or unit in ['h', 'hour']:
            return {
                "total_seconds": int(value * 3600),
                "total_minutes": int(value * 60),
                "source": "chinese_specification"
            }
        else:  # minutes
            return {
                "total_seconds": int(value * 60),
                "total_minutes": int(value),
                "source": "chinese_specification"
            }

    # Pattern 3: "deadline in X" / "complete in X" / "finish in X"
    deadline_pattern = r'(?:deadline|complete|finish)(?:\s+in\s+|\s*:\s*)(\d+(?:\.\d+)?)\s*(hour|hr|h|minute|min|m)'
    dl_match = re.search(deadline_pattern, query_lower)
    if dl_match:
        value = float(dl_match.group(1))
        unit = dl_match.group(2)
        if unit.startswith('h'):
            return {
                "total_seconds": int(value * 3600),
                "total_minutes": int(value * 60),
                "source": "deadline_specification"
            }
        else:
            return {
                "total_seconds": int(value * 60),
                "total_minutes": int(value),
                "source": "deadline_specification"
            }

    # Default: No time budget specified
    return None


def calculate_time_allocation(
    total_budget_seconds: int,
    subagent_count: int = 3,
    coordination_overhead: float = 0.20
) -> Dict[str, Any]:
    """
    Calculate per-agent time allocation for parallel execution (v9.3).

    KEY: Agents run in PARALLEL, so each agent gets FULL available time,
    NOT divided by agent count.

    Args:
        total_budget_seconds: Total time budget in seconds
        subagent_count: Number of subagents (for reference only, not division)
        coordination_overhead: Coordination buffer (default 20%)

    Returns:
        Dict with time allocation details
    """
    available_time = total_budget_seconds * (1 - coordination_overhead)

    # Each agent gets FULL available time (parallel execution)
    per_agent_budget = available_time

    # Checkpoint interval is 10% of total budget
    checkpoint_interval = total_budget_seconds * 0.10

    return {
        "total_budget_seconds": total_budget_seconds,
        "total_budget_minutes": int(total_budget_seconds / 60),
        "coordination_buffer_seconds": int(total_budget_seconds * coordination_overhead),
        "available_time_seconds": int(available_time),
        "per_agent_timeout_seconds": int(per_agent_budget),  # Full time, NOT divided!
        "per_agent_timeout_minutes": int(per_agent_budget / 60),
        "checkpoint_interval_seconds": int(checkpoint_interval),
        "checkpoint_interval_minutes": int(checkpoint_interval / 60),
        "start_time_iso": datetime.now().isoformat(),
        "time_source": "calculated",
        "subagent_count": subagent_count,
        "wall_clock_time_seconds": total_budget_seconds,  # Same as total for parallel
    }


def calculate_max_turns(per_agent_timeout_seconds: int, seconds_per_turn: int = 120) -> int:
    """
    Calculate max_turns from time budget (v9.3).

    Assumes average 2 minutes (120 seconds) per turn.
    Minimum 10 turns to ensure meaningful work.

    Args:
        per_agent_timeout_seconds: Time budget per agent in seconds
        seconds_per_turn: Average seconds per turn (default 120)

    Returns:
        Maximum number of turns for the agent
    """
    return max(10, per_agent_timeout_seconds // seconds_per_turn)


def generate_time_budget_string(time_allocation: Dict[str, Any]) -> str:
    """
    Generate TIME_BUDGET string for subagent prompts (v9.3).

    Args:
        time_allocation: Dict from calculate_time_allocation()

    Returns:
        Formatted TIME_BUDGET string for prompt injection
    """
    return f"""
TIME_BUDGET:
- per_agent_timeout_seconds: {time_allocation.get('per_agent_timeout_seconds', 'default')}
- per_agent_timeout_minutes: {time_allocation.get('per_agent_timeout_minutes', 'default')}
- start_time_iso: {time_allocation.get('start_time_iso', datetime.now().isoformat())}
- checkpoint_interval_seconds: {time_allocation.get('checkpoint_interval_seconds', 'default')}
- time_source: {time_allocation.get('time_source', 'calculated')}

CRITICAL: You MUST track time at each checkpoint. When remaining_seconds < 300 (5 min),
enter ACCELERATE_MODE: stop deep analysis, skip citation chains, quickly summarize findings.
"""


def get_time_assessment_from_allocation(
    time_allocation: Dict[str, Any],
    start_time_iso: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get current time assessment from time allocation (v9.3).

    Args:
        time_allocation: Dict from calculate_time_allocation()
        start_time_iso: Start time in ISO format (uses allocation's if None)

    Returns:
        Time assessment dict with elapsed, remaining, status
    """
    if not time_allocation:
        return {}

    start_time_str = start_time_iso or time_allocation.get('start_time_iso')
    if not start_time_str:
        return {}

    try:
        start_time = datetime.fromisoformat(start_time_str)
    except (ValueError, TypeError):
        return {}

    current_time = datetime.now()
    elapsed = (current_time - start_time).total_seconds()
    budget_seconds = time_allocation.get('per_agent_timeout_seconds', 0)
    remaining = budget_seconds - elapsed

    # Determine time status
    if remaining < 0:
        time_status = "overtime"
    elif remaining < 300:  # Less than 5 minutes
        time_status = "time_critical"
    elif remaining < budget_seconds * 0.25:  # Less than 25%
        time_status = "warning"
    else:
        time_status = "on_track"

    return {
        "start_time": start_time_str,
        "current_time": current_time.isoformat(),
        "elapsed_seconds": int(elapsed),
        "elapsed_formatted": f"{int(elapsed // 60)} minutes {int(elapsed % 60)}s",
        "remaining_seconds": int(remaining),
        "remaining_formatted": f"{int(remaining // 60)} minutes {int(remaining % 60)}s",
        "budget_seconds": budget_seconds,
        "budget_formatted": f"{int(budget_seconds // 60)} minutes",
        "time_status": time_status,
        "should_accelerate": remaining < 300,
    }


def generate_continuation_prompt(
    agent_type: str,
    output_file: str,
    remaining_requirements: Dict[str, Any],
    remaining_seconds: int
) -> str:
    """
    Generate continuation prompt for relaunching an interrupted agent (v9.3).

    Args:
        agent_type: Type of agent to continue
        output_file: Path to the agent's output file
        remaining_requirements: Dict of requirements not yet met
        remaining_seconds: Time remaining in seconds

    Returns:
        Formatted continuation prompt string
    """
    remaining_minutes = int(remaining_seconds // 60)

    # Determine mode based on remaining time
    if remaining_seconds < 600:  # Less than 10 minutes
        mode = "RAPID_COMPLETION"
        instructions = """
1. Skip all full-text downloads - use abstracts only
2. Limit to direct citations - no deep citation chain exploration
3. Batch all tool calls together
4. Minimum viable output for each item
5. Focus on hitting minimum counts only
"""
    elif remaining_seconds < 1200:  # Less than 20 minutes
        mode = "ACCELERATE_MODE"
        instructions = """
1. Prioritize abstract over full-text
2. Track direct citations only (1 level deep)
3. Simplify analysis output
4. Focus on key items first
"""
    else:
        mode = "CONTINUATION_MODE"
        instructions = """
1. Continue from checkpoint efficiently
2. Use full-text for key papers only
3. Track critical citation chains
4. Maintain analysis quality
"""

    return f"""CONTINUE FROM CHECKPOINT - {mode.upper()}

Your previous session was interrupted due to time limit (max_turns).

AGENT TYPE: {agent_type}
OUTPUT FILE: {output_file}
TIME REMAINING: {remaining_seconds} seconds ({remaining_minutes} minutes)
MODE: {mode}

MINIMUM REQUIREMENTS REMAINING:
{json.dumps(remaining_requirements, indent=2)}

INSTRUCTIONS:
{instructions}

Time Budget: Use checkpoint_manager.get_time_assessment() to track progress.

Remember: When remaining_seconds < 300 (5 min), enter RAPID mode and complete
remaining items with minimal analysis.
"""


def should_continue_agent(
    time_allocation: Dict[str, Any],
    minimum_time_seconds: int = 300
) -> tuple[bool, int, str]:
    """
    Determine if an agent should be relaunched based on remaining time (v9.3).

    Args:
        time_allocation: Time allocation dict
        minimum_time_seconds: Minimum seconds required to relaunch (default 300)

    Returns:
        Tuple of (should_continue, remaining_seconds, status)
        - status: "continue", "insufficient_time", "no_budget"
    """
    if not time_allocation:
        return False, 0, "no_budget"

    time_assessment = get_time_assessment_from_allocation(time_allocation)
    remaining_seconds = time_assessment.get('remaining_seconds', 0)

    if remaining_seconds >= minimum_time_seconds:
        return True, remaining_seconds, "continue"
    else:
        return False, remaining_seconds, "insufficient_time"


def format_time_confirmation(
    phase_name: str,
    time_allocation: Dict[str, Any],
    extra_info: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format a time confirmation message for console output (v9.3).

    Args:
        phase_name: Name of the current phase
        time_allocation: Time allocation dict
        extra_info: Optional extra information to display

    Returns:
        Formatted time confirmation string
    """
    if not time_allocation:
        return f"[TIME CONFIRM - {phase_name}]: No time budget set"

    time_assessment = get_time_assessment_from_allocation(time_allocation)

    lines = [
        f"[TIME CONFIRM - {phase_name}]",
        f"├─ Elapsed: {time_assessment.get('elapsed_formatted', 'N/A')}",
        f"├─ Remaining: {time_assessment.get('remaining_formatted', 'N/A')}",
        f"├─ Status: {time_assessment.get('time_status', 'unknown')}",
    ]

    if extra_info:
        for key, value in extra_info.items():
            lines.append(f"├─ {key}: {value}")

    lines.append(f"└─ Should Accelerate: {time_assessment.get('should_accelerate', False)}")

    return "\n".join(lines)


# ============================================================================
# Time Re-allocation Functions (v9.4) - Transfer saved time to final phases
# ============================================================================

class TimeBudgetTracker:
    """
    Track time spent vs budget across all phases (v9.4).

    When phases complete faster than expected, re-allocate remaining time
    to later phases (especially report synthesis) to improve quality.
    """

    def __init__(self, total_budget_seconds: int, start_time_iso: Optional[str] = None):
        """
        Initialize time budget tracker.

        Args:
            total_budget_seconds: Total time budget for the entire research
            start_time_iso: Start time in ISO format
        """
        self.total_budget_seconds = total_budget_seconds
        self.start_time_iso = start_time_iso or datetime.now().isoformat()

        try:
            self.start_time = datetime.fromisoformat(self.start_time_iso)
        except (ValueError, TypeError):
            self.start_time = datetime.now()
            self.start_time_iso = self.start_time.isoformat()

        # Phase time allocations (estimated vs actual)
        self.phase_allocations = {
            "Phase -1": {"estimated": 60, "actual": 0},      # Performance Prediction: 1 min
            "Phase 0": {"estimated": 60, "actual": 0},        # Framework Selection: 1 min
            "Phase 0.5": {"estimated": 60, "actual": 0},      # MCP Coordination: 1 min
            "Phase 0.75": {"estimated": 0, "actual": 0},      # Production Readiness: optional
            "Phase 1": {"estimated": total_budget_seconds * 0.60, "actual": 0},  # Research: 60%
            "Phase 1.1": {"estimated": 60, "actual": 0},       # Completion Check: 1 min
            "Phase 1.5": {"estimated": 300, "actual": 0},      # Cross-Domain: 5 min
            "Phase 2a": {"estimated": 600, "actual": 0},       # Logic Analysis: 10 min
            "Phase 2b": {"estimated": total_budget_seconds * 0.25, "actual": 0},  # Reports: 25%
            "Phase 2d": {"estimated": 300, "actual": 0},       # Link Validation: 5 min
            "Phase 2e": {"estimated": 0, "actual": 0},        # Task Handler: optional
        }

        # Phases completed
        self.completed_phases = []
        self.current_phase = None

    def start_phase(self, phase_name: str):
        """Mark the start of a phase."""
        self.current_phase = phase_name

    def end_phase(self, phase_name: str):
        """Mark the end of a phase and record actual time."""
        if phase_name in self.phase_allocations:
            # Calculate actual time spent if we have a previous phase end time
            # For now, use current time - start time as approximation
            elapsed = int((datetime.now() - self.start_time).total_seconds())
            # Subtract time from previous phases
            for completed in self.completed_phases:
                elapsed -= self.phase_allocations[completed]["actual"]
            self.phase_allocations[phase_name]["actual"] = elapsed
            self.completed_phases.append(phase_name)
        self.current_phase = None

    def get_saved_time(self) -> Dict[str, Any]:
        """
        Calculate time saved across completed phases (v9.4).

        Returns:
            Dict with saved_seconds, phases_under_budget, and re-allocation recommendations
        """
        total_saved = 0
        phases_under_budget = []

        for phase_name in self.completed_phases:
            allocation = self.phase_allocations.get(phase_name, {})
            estimated = allocation.get("estimated", 0)
            actual = allocation.get("actual", 0)

            if actual < estimated:
                saved = estimated - actual
                total_saved += saved
                phases_under_budget.append({
                    "phase": phase_name,
                    "estimated": estimated,
                    "actual": actual,
                    "saved": saved
                })

        # Calculate remaining budget
        elapsed_total = (datetime.now() - self.start_time).total_seconds()
        remaining_budget = self.total_budget_seconds - elapsed_total

        return {
            "total_saved_seconds": int(total_saved),
            "total_saved_minutes": int(total_saved / 60),
            "remaining_budget_seconds": int(remaining_budget),
            "remaining_budget_minutes": int(remaining_budget / 60),
            "phases_under_budget": phases_under_budget,
            "reallocate_to_reports": int(total_saved + remaining_budget),
            "recommendation": self._get_reallocation_recommendation(total_saved, remaining_budget)
        }

    def _get_reallocation_recommendation(self, saved_seconds: int, remaining_seconds: int) -> str:
        """Generate recommendation for time re-allocation."""
        total_available = saved_seconds + remaining_seconds
        available_minutes = int(total_available / 60)

        if available_minutes < 5:
            return "No significant time saved - proceed as planned"
        elif available_minutes < 15:
            return f"Reallocate {available_minutes}min to report synthesis for refinement"
        elif available_minutes < 30:
            return f"Reallocate {available_minutes}min to reports: deeper analysis + citation verification"
        else:
            return f"Reallocate {available_minutes}min to reports: comprehensive expansion + link validation + custom output"

    def format_time_saved_report(self) -> str:
        """Format a time saved report for console display."""
        saved_info = self.get_saved_time()

        lines = [
            "┌─────────────────────────────────────────────────────────────┐",
            "│  ⏱️  TIME SAVED REPORT - Re-allocating to Final Phases            │",
            "├─────────────────────────────────────────────────────────────┤",
            f"│  Time Saved: {saved_info['total_saved_minutes']} minutes early completion",
            f"│  Remaining Budget: {saved_info['remaining_budget_minutes']} minutes",
            f"│  Total Available: {saved_info['reallocate_to_reports'] // 60} minutes for final phases",
            "│                                                                      │",
        ]

        if saved_info["phases_under_budget"]:
            lines.append("│  Phases Under Budget:")
            for phase_info in saved_info["phases_under_budget"]:
                phase = phase_info["phase"]
                saved = phase_info["saved"]
                lines.append(f"│    • {phase}: saved {saved//60}m {saved%60}s")

        lines.append("│                                                                      │")
        lines.append(f"│  Recommendation: {saved_info['recommendation']}")
        lines.append("└─────────────────────────────────────────────────────────────┘")

        return "\n".join(lines)


def format_phase_checkpoint(
    phase_name: str,
    time_allocation: Optional[Dict[str, Any]] = None,
    progress_percent: int = 0,
    next_phase: str = ""
) -> str:
    """
    Format a phase checkpoint message (v9.4).

    Args:
        phase_name: Name of the completed phase
        time_allocation: Time allocation dict
        progress_percent: Overall progress percentage (0-100)
        next_phase: Name of the next phase

    Returns:
        Formatted checkpoint message
    """
    elapsed_seconds = 0
    remaining_seconds = 0
    status = "on_track"

    if time_allocation:
        time_assessment = get_time_assessment_from_allocation(time_allocation)
        elapsed_seconds = time_assessment.get("elapsed_seconds", 0)
        remaining_seconds = time_assessment.get("remaining_seconds", 0)
        status = time_assessment.get("time_status", "on_track")

    # Create progress bar
    filled = int(progress_percent / 5)
    bar = "█" * filled + "░" * (20 - filled)

    lines = [
        "┌─────────────────────────────────────────────────────────────┐",
        f"│  ⏱️  PHASE CHECKPOINT: {phase_name}",
        "├─────────────────────────────────────────────────────────────┤",
        f"│  Elapsed:   {elapsed_seconds // 60}m {elapsed_seconds % 60}s",
        f"│  Remaining: {remaining_seconds // 60}m {remaining_seconds % 60}s",
        f"│  Progress:  [{bar}] {progress_percent}%",
        f"│  Status:    {status}",
    ]

    if next_phase:
        lines.append(f"│  Next:      {next_phase}")

    lines.append("└─────────────────────────────────────────────────────────────┘")

    return "\n".join(lines)
