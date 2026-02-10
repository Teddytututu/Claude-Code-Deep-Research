#!/usr/bin/env python3
"""
Token Budget Monitoring Hook v7.0

Based on Anthropic's multi-agent research system findings:
- Multi-agent: 15x normal chat tokens
- Efficiency: 14-21 tasks/1K tokens (vs 67 for single agent)
- Coordination overhead: n(n-1)/2 interactions

Monitors token usage and provides warnings based on Chinese community best practices:
- Warning at 70% of budget
- Critical alert at 90% of budget
- Graceful degradation recommendations

Author: Deep Research System
Date: 2026-02-09
"""

import sys
import json
from typing import Dict, Any

# Token cost multipliers from Anthropic research
TOKEN_MULTIPLIERS = {
    "single_agent": 1.0,
    "multi_agent_centralized": 15.0,
    "multi_agent_hybrid": 15.0,
}

# Efficiency metrics (tasks per 1K tokens)
EFFICIENCY_METRICS = {
    "single_agent": 67,
    "multi_agent_centralized": 21,  # 69% less efficient
    "multi_agent_hybrid": 14,  # 79% less efficient
}

# Warning thresholds (Chinese community best practices)
WARNING_THRESHOLD = 0.70  # 70%
CRITICAL_THRESHOLD = 0.90  # 90%

# Estimated costs (per million tokens)
COST_PER_1M_TOKENS = {
    "input": 15.0,  # USD
    "output": 75.0,  # USD
}

def calculate_coordination_overhead(num_agents: int) -> int:
    """
    Calculate coordination overhead based on number of agents

    Formula: n(n-1)/2 potential interactions

    Args:
        num_agents: Number of agents in the system

    Returns:
        Number of potential interactions
    """
    return num_agents * (num_agents - 1) // 2


def estimate_cost(tokens_used: int, output_ratio: float = 0.3) -> Dict[str, float]:
    """
    Estimate cost based on token usage

    Args:
        tokens_used: Total tokens used
        output_ratio: Ratio of output tokens (default 30%)

    Returns:
        Cost breakdown in USD
    """
    input_tokens = int(tokens_used * (1 - output_ratio))
    output_tokens = int(tokens_used * output_ratio)

    input_cost = (input_tokens / 1_000_000) * COST_PER_1M_TOKENS["input"]
    output_cost = (output_tokens / 1_000_000) * COST_PER_1M_TOKENS["output"]

    return {
        "input_cost_usd": round(input_cost, 4),
        "output_cost_usd": round(output_cost, 4),
        "total_cost_usd": round(input_cost + output_cost, 4)
    }


def check_token_budget(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check token budget and generate appropriate warnings

    Args:
        input_data: Hook input with current token information

    Returns:
        Hook response with warnings if thresholds exceeded
    """
    # Extract token information
    current_tokens = input_data.get('current_tokens', 0)
    token_budget = input_data.get('token_budget', 200000)
    num_agents = input_data.get('num_agents', 1)
    orchestration_type = input_data.get('orchestration_type', 'single_agent')

    # Calculate usage percentage
    usage_percent = current_tokens / token_budget if token_budget > 0 else 0

    # Calculate metrics
    response = {
        "current_tokens": current_tokens,
        "token_budget": token_budget,
        "usage_percent": round(usage_percent * 100, 1),
        "remaining_tokens": token_budget - current_tokens,
        "coordination_overhead": calculate_coordination_overhead(num_agents),
        "efficiency_metric": EFFICIENCY_METRICS.get(orchestration_type, 67)
    }

    # Add cost estimate
    cost_estimate = estimate_cost(current_tokens)
    response.update({
        f"estimated_{k}": v for k, v in cost_estimate.items()
    })

    # Generate warnings based on thresholds
    warnings = []

    if usage_percent >= CRITICAL_THRESHOLD:
        warnings.append(f"CRITICAL: Token budget at {response['usage_percent']}%!")
        warnings.append(f"Recommendation: Stop and synthesize current findings.")
        warnings.append(f"Remaining: {response['remaining_tokens']:,} tokens")

    elif usage_percent >= WARNING_THRESHOLD:
        warnings.append(f"WARNING: Token budget at {response['usage_percent']}%.")
        warnings.append(f"Recommendation: Consider /compact to compress context.")
        warnings.append(f"Remaining: {response['remaining_tokens']:,} tokens")

        # Add efficiency warning for multi-agent
        if orchestration_type in ["multi_agent_centralized", "multi_agent_hybrid"]:
            warnings.append(f"Note: Multi-agent efficiency is {EFFICIENCY_METRICS[orchestration_type]} tasks/1K tokens")
            warnings.append(f"vs. 67 for single-agent (69-79% less efficient).")

    # Add coordination overhead warning
    if num_agents >= 4:
        warnings.append(f"Coordination overhead: {response['coordination_overhead']} potential interactions")

    if warnings:
        response["warnings"] = warnings
        response["systemMessage"] = " | ".join(warnings)

    return response


def format_research_context(input_data: Dict[str, Any]) -> str:
    """
    Format research context for the agent

    Args:
        input_data: Hook input with research information

    Returns:
        Formatted context string
    """
    session_id = input_data.get('session_id', 'unknown')
    query = input_data.get('query', '')
    phase = input_data.get('phase', 'unknown')

    context_parts = [
        f"Research Session: {session_id[:8]}...",
        f"Query: {query[:100]}..." if len(query) > 100 else f"Query: {query}",
        f"Phase: {phase}"
    ]

    return " | ".join(context_parts)


def main():
    """Main hook entry point"""
    try:
        # Read input from stdin (Claude Code hook format)
        input_data = json.load(sys.stdin)

        # Check token budget
        result = check_token_budget(input_data)

        # Add research context if available
        if 'query' in input_data:
            result["research_context"] = format_research_context(input_data)

        # Output as JSON
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError as e:
        # Invalid input, return minimal response
        print(json.dumps({"error": f"Invalid JSON input: {e}"}))
    except Exception as e:
        # Unexpected error, return error message
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
