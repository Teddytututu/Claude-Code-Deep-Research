"""
Heartbeat Monitor for Deep Research System v9.5

Provides real-time monitoring of subagent progress and health.
Detects stuck or unresponsive agents.

Usage:
    # Write heartbeat (called by subagents)
    python heartbeat_monitor.py --write academic-researcher --status running --items 5

    # Check heartbeat (called by orchestrator)
    python heartbeat_monitor.py --check academic-researcher

    # List all heartbeats
    python heartbeat_monitor.py --list

    # Check for stuck agents (no update for > 5 minutes)
    python heartbeat_monitor.py --stuck --timeout 300

Author: Deep Research System
Date: 2026-02-18
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import argparse


@dataclass
class Heartbeat:
    """Heartbeat data structure"""
    agent_type: str
    status: str  # "running", "accelerate", "saving", "complete", "error"
    items_processed: int
    timestamp: str
    elapsed_seconds: Optional[float] = None
    remaining_seconds: Optional[int] = None
    message: Optional[str] = None


class HeartbeatMonitor:
    """
    Monitor subagent health via heartbeat files.

    Heartbeats are written to research_data/heartbeat/{agent_type}.json
    """

    def __init__(self, heartbeat_dir: str = "research_data/heartbeat"):
        self.heartbeat_dir = Path(heartbeat_dir)
        self.heartbeat_dir.mkdir(parents=True, exist_ok=True)

    def write_heartbeat(
        self,
        agent_type: str,
        status: str,
        items_processed: int,
        start_time_iso: Optional[str] = None,
        budget_seconds: Optional[int] = None,
        message: Optional[str] = None
    ) -> str:
        """
        Write a heartbeat for an agent.

        Args:
            agent_type: Type of agent (academic-researcher, etc.)
            status: Current status
            items_processed: Number of items processed
            start_time_iso: Start time for elapsed calculation
            budget_seconds: Time budget for remaining calculation
            message: Optional message

        Returns:
            Path to heartbeat file
        """
        now = datetime.now()
        elapsed_seconds = None
        remaining_seconds = None

        if start_time_iso:
            try:
                start_time = datetime.fromisoformat(start_time_iso)
                elapsed_seconds = (now - start_time).total_seconds()
                if budget_seconds:
                    remaining_seconds = max(0, int(budget_seconds - elapsed_seconds))
            except (ValueError, TypeError):
                pass

        heartbeat = Heartbeat(
            agent_type=agent_type,
            status=status,
            items_processed=items_processed,
            timestamp=now.isoformat(),
            elapsed_seconds=elapsed_seconds,
            remaining_seconds=remaining_seconds,
            message=message
        )

        filepath = self.heartbeat_dir / f"{agent_type}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(heartbeat), f, indent=2)

        return str(filepath)

    def read_heartbeat(self, agent_type: str) -> Optional[Heartbeat]:
        """
        Read heartbeat for an agent.

        Args:
            agent_type: Type of agent

        Returns:
            Heartbeat object or None if not found
        """
        filepath = self.heartbeat_dir / f"{agent_type}.json"

        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return Heartbeat(**data)
        except (json.JSONDecodeError, TypeError):
            return None

    def get_heartbeat_age(self, agent_type: str) -> Optional[float]:
        """
        Get age of heartbeat in seconds.

        Args:
            agent_type: Type of agent

        Returns:
            Age in seconds or None if not found
        """
        heartbeat = self.read_heartbeat(agent_type)
        if not heartbeat:
            return None

        try:
            timestamp = datetime.fromisoformat(heartbeat.timestamp)
            return (datetime.now() - timestamp).total_seconds()
        except (ValueError, TypeError):
            return None

    def is_stuck(self, agent_type: str, timeout_seconds: int = 300) -> bool:
        """
        Check if an agent is stuck (no heartbeat for too long).

        Args:
            agent_type: Type of agent
            timeout_seconds: Timeout threshold (default 5 minutes)

        Returns:
            True if agent appears stuck
        """
        heartbeat = self.read_heartbeat(agent_type)
        if not heartbeat:
            return True  # No heartbeat = potentially stuck

        # Check status
        if heartbeat.status in ["complete", "error"]:
            return False  # Terminal states

        # Check age
        age = self.get_heartbeat_age(agent_type)
        if age is None:
            return True

        return age > timeout_seconds

    def list_heartbeats(self) -> List[Dict[str, Any]]:
        """
        List all heartbeats.

        Returns:
            List of heartbeat data dicts
        """
        heartbeats = []

        for filepath in self.heartbeat_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Calculate age
                timestamp = datetime.fromisoformat(data.get("timestamp", ""))
                age_seconds = (datetime.now() - timestamp).total_seconds()

                data["age_seconds"] = age_seconds
                data["age_formatted"] = f"{int(age_seconds // 60)}m {int(age_seconds % 60)}s"
                data["is_stale"] = age_seconds > 300

                heartbeats.append(data)
            except (json.JSONDecodeError, ValueError):
                continue

        return sorted(heartbeats, key=lambda x: x.get("timestamp", ""), reverse=True)

    def find_stuck_agents(self, timeout_seconds: int = 300) -> List[Dict[str, Any]]:
        """
        Find all stuck agents.

        Args:
            timeout_seconds: Timeout threshold

        Returns:
            List of stuck agent info
        """
        stuck = []

        for filepath in self.heartbeat_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if data.get("status") in ["complete", "error"]:
                    continue

                timestamp = datetime.fromisoformat(data.get("timestamp", ""))
                age_seconds = (datetime.now() - timestamp).total_seconds()

                if age_seconds > timeout_seconds:
                    data["age_seconds"] = age_seconds
                    data["age_formatted"] = f"{int(age_seconds // 60)}m {int(age_seconds % 60)}s"
                    stuck.append(data)

            except (json.JSONDecodeError, ValueError):
                continue

        return sorted(stuck, key=lambda x: x.get("age_seconds", 0), reverse=True)

    def clear_heartbeat(self, agent_type: str) -> bool:
        """
        Clear heartbeat for an agent.

        Args:
            agent_type: Type of agent

        Returns:
            True if cleared successfully
        """
        filepath = self.heartbeat_dir / f"{agent_type}.json"

        if filepath.exists():
            filepath.unlink()
            return True
        return False

    def clear_all_heartbeats(self) -> int:
        """
        Clear all heartbeats.

        Returns:
            Number of heartbeats cleared
        """
        count = 0
        for filepath in self.heartbeat_dir.glob("*.json"):
            filepath.unlink()
            count += 1
        return count


def format_heartbeat_report(heartbeats: List[Dict[str, Any]]) -> str:
    """Format heartbeats for console display."""
    lines = [
        "┌" + "─" * 70 + "┐",
        "│" + " " * 20 + "HEARTBEAT MONITOR" + " " * 32 + "│",
        "├" + "─" * 70 + "┤",
    ]

    if not heartbeats:
        lines.append("│  No heartbeats found" + " " * 48 + "│")
    else:
        for hb in heartbeats:
            agent = hb.get("agent_type", "unknown")[:20].ljust(20)
            status = hb.get("status", "unknown")[:10].ljust(10)
            items = str(hb.get("items_processed", 0)).ljust(5)
            age = hb.get("age_formatted", "?").ljust(10)

            # Status emoji
            if hb.get("status") == "complete":
                emoji = "✅"
            elif hb.get("is_stale"):
                emoji = "⚠️"
            elif hb.get("status") == "error":
                emoji = "❌"
            else:
                emoji = "🔄"

            line = f"│  {emoji} {agent} | {status} | {items} items | age: {age}│"
            lines.append(line)

    lines.append("└" + "─" * 70 + "┘")
    return "\n".join(lines)


# CLI interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heartbeat Monitor v9.5")

    # Write heartbeat
    parser.add_argument("--write", type=str, help="Write heartbeat for agent type")
    parser.add_argument("--status", type=str, default="running", help="Status to write")
    parser.add_argument("--items", type=int, default=0, help="Items processed")
    parser.add_argument("--start-time", type=str, help="Start time ISO format")
    parser.add_argument("--budget", type=int, help="Time budget in seconds")
    parser.add_argument("--message", type=str, help="Optional message")

    # Read heartbeat
    parser.add_argument("--check", type=str, help="Check heartbeat for agent type")

    # List heartbeats
    parser.add_argument("--list", action="store_true", help="List all heartbeats")

    # Find stuck agents
    parser.add_argument("--stuck", action="store_true", help="Find stuck agents")
    parser.add_argument("--timeout", type=int, default=300, help="Stuck timeout in seconds")

    # Clear heartbeats
    parser.add_argument("--clear", type=str, help="Clear heartbeat for agent type")
    parser.add_argument("--clear-all", action="store_true", help="Clear all heartbeats")

    args = parser.parse_args()

    monitor = HeartbeatMonitor()

    if args.write:
        filepath = monitor.write_heartbeat(
            agent_type=args.write,
            status=args.status,
            items_processed=args.items,
            start_time_iso=args.start_time,
            budget_seconds=args.budget,
            message=args.message
        )
        print(f"Heartbeat written: {filepath}")

    elif args.check:
        heartbeat = monitor.read_heartbeat(args.check)
        if heartbeat:
            print(json.dumps(asdict(heartbeat), indent=2))
        else:
            print(f"No heartbeat found for: {args.check}")

    elif args.list:
        heartbeats = monitor.list_heartbeats()
        print(format_heartbeat_report(heartbeats))

    elif args.stuck:
        stuck = monitor.find_stuck_agents(args.timeout)
        if stuck:
            print(f"Found {len(stuck)} stuck agent(s):")
            for agent in stuck:
                print(f"  - {agent['agent_type']}: age {agent['age_formatted']}")
        else:
            print("No stuck agents found")

    elif args.clear:
        if monitor.clear_heartbeat(args.clear):
            print(f"Cleared heartbeat for: {args.clear}")
        else:
            print(f"No heartbeat to clear for: {args.clear}")

    elif args.clear_all:
        count = monitor.clear_all_heartbeats()
        print(f"Cleared {count} heartbeat(s)")

    else:
        # Default: list heartbeats
        heartbeats = monitor.list_heartbeats()
        print(format_heartbeat_report(heartbeats))
