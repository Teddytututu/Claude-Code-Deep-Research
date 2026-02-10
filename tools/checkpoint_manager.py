"""
Checkpoint Manager for Deep Research System v9.0

Shared checkpoint utilities for all research agents.
Provides incremental writing, resume capability, and progress tracking.
"""

import json
import time
from datetime import datetime
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
    """

    def __init__(
        self,
        agent_type: str,
        output_dir: str = "research_data/checkpoints",
        output_file: Optional[str] = None
    ):
        """
        Initialize checkpoint manager.

        Args:
            agent_type: Type of agent (academic-researcher, github-watcher, etc.)
            output_dir: Directory for checkpoint files
            output_file: Optional final output file path
        """
        self.agent_type = agent_type
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_file = output_file or f"research_data/{agent_type}_output.json"
        self.checkpoint_count = 0
        self.items_processed = 0

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
            Confirmation message
        """
        self.checkpoint_count += 1
        timestamp = time.time()

        checkpoint = {
            "checkpoint_number": self.checkpoint_count,
            "checkpoint_id": f"{self.agent_type.replace('-', '_')}_{self.checkpoint_count:03d}",
            "phase": phase,
            "timestamp": timestamp,
            "timestamp_iso": datetime.fromtimestamp(timestamp).isoformat(),
            "items_processed": self.items_processed,
            "content": content
        }

        if items:
            checkpoint["items"] = items
            # Also add to main items list
            self.data["items"].extend(items)
            self.items_processed += len(items)

        self.data["subagent_metadata"]["checkpoints"].append(checkpoint)
        self._save()

        return f"Checkpoint {self.checkpoint_count} written for phase: {phase}"

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
    output_dir: str = "research_data/checkpoints"
) -> CheckpointManager:
    """
    Create a checkpoint manager for the specified agent type.

    Args:
        agent_type: Type of agent (academic-researcher, github-watcher, etc.)
        output_dir: Directory for checkpoint files

    Returns:
        CheckpointManager instance
    """
    return CheckpointManager(agent_type, output_dir)
