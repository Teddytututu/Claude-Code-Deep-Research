"""
Deep Research System Configuration v10.0
深度研究系统配置模块

Uses Pydantic Settings for type-safe configuration management.
Supports environment variables, .env files, and programmatic overrides.

Author: Deep Research System
Date: 2026-02-18
"""

from typing import Literal, Optional
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global configuration for Deep Research System.

    Configuration priority:
    1. Environment variables (highest)
    2. .env file
    3. Default values (lowest)

    Usage:
        from tools.config import settings
        print(settings.default_time_budget_minutes)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # =========================================================================
    # API Configuration
    # =========================================================================

    anthropic_api_key: str = Field(
        default="",
        description="Anthropic API key for Claude models"
    )

    # =========================================================================
    # Time Budget Configuration
    # =========================================================================

    default_time_budget_minutes: int = Field(
        default=60,
        ge=5,
        le=480,
        description="Default time budget for research sessions in minutes"
    )

    per_agent_time_multiplier: float = Field(
        default=0.8,
        ge=0.1,
        le=1.0,
        description="Multiplier for per-agent time allocation"
    )

    # =========================================================================
    # MCP Configuration
    # =========================================================================

    mcp_tool_limit: int = Field(
        default=80,
        ge=10,
        le=200,
        description="Maximum number of MCP tools available"
    )

    active_mcp_count: int = Field(
        default=6,
        ge=1,
        le=10,
        description="Number of active MCP servers per session"
    )

    # =========================================================================
    # Storage Configuration
    # =========================================================================

    vector_db_backend: Literal["memory", "chroma"] = Field(
        default="memory",
        description="Vector database backend type"
    )

    persist_directory: str = Field(
        default=".chroma",
        description="Directory for persistent vector storage"
    )

    research_data_dir: str = Field(
        default="research_data",
        description="Research data storage directory"
    )

    research_output_dir: str = Field(
        default="research_output",
        description="Research output directory"
    )

    # =========================================================================
    # Performance Configuration
    # =========================================================================

    multi_agent_threshold: float = Field(
        default=0.45,
        ge=0.0,
        le=1.0,
        description="Threshold for multi-agent decision (45% rule)"
    )

    api_rate_limit: float = Field(
        default=10.0,
        ge=1.0,
        le=100.0,
        description="API rate limit in requests per second"
    )

    # =========================================================================
    # Visualization Configuration
    # =========================================================================

    default_viz_format: Literal["html", "png", "svg", "mermaid"] = Field(
        default="html",
        description="Default visualization format"
    )

    viz_enable_physics: bool = Field(
        default=True,
        description="Enable physics simulation in interactive visualizations"
    )

    # =========================================================================
    # Model Configuration
    # =========================================================================

    lead_model: str = Field(
        default="claude-opus-4-5-20250514",
        description="Model for lead researcher agent"
    )

    subagent_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Model for subagent workers"
    )

    default_max_turns: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Default maximum turns for agents"
    )

    # =========================================================================
    # Computed Properties
    # =========================================================================

    @property
    def per_agent_time_seconds(self) -> int:
        """Calculate per-agent time allocation in seconds."""
        return int(self.default_time_budget_minutes * 60 * self.per_agent_time_multiplier)

    @property
    def per_agent_time_str(self) -> str:
        """Human-readable per-agent time allocation."""
        minutes = self.per_agent_time_seconds // 60
        seconds = self.per_agent_time_seconds % 60
        return f"{minutes}m {seconds}s"

    @property
    def research_data_path(self) -> Path:
        """Path object for research data directory."""
        return Path(self.research_data_dir)

    @property
    def research_output_path(self) -> Path:
        """Path object for research output directory."""
        return Path(self.research_output_dir)

    @property
    def persist_path(self) -> Path:
        """Path object for persistent storage directory."""
        return Path(self.persist_directory)

    @property
    def use_vector_store(self) -> bool:
        """Whether to use vector store for semantic search."""
        return self.vector_db_backend == "chroma"

    # =========================================================================
    # Validators
    # =========================================================================

    @field_validator("anthropic_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API key format (allow empty for testing)."""
        if v and not v.startswith("sk-"):
            # Note: Anthropic keys don't always start with sk-, but we warn
            pass  # Allow any format for flexibility
        return v

    @field_validator("research_data_dir", "research_output_dir", "persist_directory")
    @classmethod
    def validate_directories(cls, v: str) -> str:
        """Ensure directory paths are valid."""
        # Remove trailing slashes for consistency
        return v.rstrip("/\\")

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def get_model_for_role(self, role: str) -> str:
        """
        Get appropriate model for a given agent role.

        Args:
            role: Agent role (e.g., "lead", "academic", "github")

        Returns:
            Model identifier string
        """
        if role in ["lead", "lead-researcher", "meta-orchestrator"]:
            return self.lead_model
        return self.subagent_model

    def calculate_max_turns(self, timeout_seconds: int, seconds_per_turn: int = 120) -> int:
        """
        Calculate max turns based on timeout.

        Args:
            timeout_seconds: Available time in seconds
            seconds_per_turn: Estimated time per turn (default 2 minutes)

        Returns:
            Maximum number of turns
        """
        return min(
            max(timeout_seconds // seconds_per_turn, 5),
            self.default_max_turns
        )

    def to_display_dict(self) -> dict:
        """
        Export configuration as dictionary for display.

        Masks sensitive values like API keys.
        """
        return {
            "Time Budget": f"{self.default_time_budget_minutes} minutes",
            "Per-Agent Time": self.per_agent_time_str,
            "MCP Tool Limit": self.mcp_tool_limit,
            "Active MCP Count": self.active_mcp_count,
            "Vector DB Backend": self.vector_db_backend,
            "Multi-Agent Threshold": f"{self.multi_agent_threshold * 100:.0f}%",
            "API Rate Limit": f"{self.api_rate_limit} req/s",
            "Lead Model": self.lead_model,
            "Subagent Model": self.subagent_model,
            "API Key Configured": "***" if self.anthropic_api_key else "(not set)",
        }


class TimeBudgetConfig(BaseSettings):
    """
    Time budget configuration for a specific research session.

    Use this when you need session-specific time overrides.
    """

    model_config = SettingsConfigDict(
        env_prefix="TIME_",
        extra="ignore",
    )

    total_minutes: int = Field(
        default=60,
        description="Total time budget in minutes"
    )

    buffer_percent: int = Field(
        default=10,
        description="Buffer percentage to reserve for synthesis"
    )

    phase_allocation: dict = Field(
        default_factory=lambda: {
            "performance_prediction": 0.02,  # 2%
            "framework_selection": 0.03,     # 3%
            "mcp_coordination": 0.02,        # 2%
            "parallel_research": 0.60,       # 60%
            "logic_analysis": 0.10,          # 10%
            "report_synthesis": 0.18,        # 18%
            "link_validation": 0.05,         # 5%
        },
        description="Time allocation per phase (must sum to 1.0)"
    )

    @property
    def total_seconds(self) -> int:
        """Total time budget in seconds."""
        return self.total_minutes * 60

    @property
    def buffer_seconds(self) -> int:
        """Reserved buffer time in seconds."""
        return int(self.total_seconds * self.buffer_percent / 100)

    @property
    def research_seconds(self) -> int:
        """Available research time after buffer."""
        return self.total_seconds - self.buffer_seconds

    def get_phase_time(self, phase: str) -> int:
        """
        Get time allocation for a specific phase.

        Args:
            phase: Phase name

        Returns:
            Time in seconds for the phase
        """
        allocation = self.phase_allocation.get(phase, 0.1)
        return int(self.research_seconds * allocation)


# Global singleton instance
settings = Settings()


# CLI interface
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Deep Research System Configuration")
    parser.add_argument("--show", action="store_true", help="Show current configuration")
    parser.add_argument("--check", action="store_true", help="Check configuration validity")
    parser.add_argument("--export", type=str, help="Export configuration to JSON file")

    args = parser.parse_args()

    if args.show:
        print("Current Configuration:")
        print("-" * 40)
        for key, value in settings.to_display_dict().items():
            print(f"  {key}: {value}")

    if args.check:
        print("\nConfiguration Check:")
        print("-" * 40)
        issues = []

        if not settings.anthropic_api_key:
            issues.append("ANTHROPIC_API_KEY not set")

        if settings.mcp_tool_limit > 100:
            issues.append(f"MCP tool limit ({settings.mcp_tool_limit}) may cause context issues")

        if settings.vector_db_backend == "chroma":
            try:
                import chromadb
                print("  ✓ ChromaDB available")
            except ImportError:
                issues.append("ChromaDB backend selected but not installed")

        if issues:
            print("  Issues found:")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("  ✓ Configuration is valid")

    if args.export:
        with open(args.export, 'w', encoding='utf-8') as f:
            json.dump(settings.to_display_dict(), f, indent=2)
        print(f"\nConfiguration exported to {args.export}")

    if not (args.show or args.check or args.export):
        parser.print_help()
