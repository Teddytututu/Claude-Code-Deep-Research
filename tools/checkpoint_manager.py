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
            "timestamp_iso": datetime.fromtimestamp(timestamp).isoformat(),
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
