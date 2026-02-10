#!/usr/bin/env python3
"""
Research Intent Detection Hook v7.0

Detects when a user query is a research request and recommends
using the multi-agent research system based on:
- Query complexity analysis
- 45% threshold rule (Google/MIT study)
- Parallelizable aspect detection

Author: Deep Research System
Date: 2026-02-09
"""

import sys
import json
from typing import Dict, Any, List, Tuple

# Research intent indicators
RESEARCH_KEYWORDS = [
    "research", "investigate", "analyze", "explore", "study",
    "comprehensive", "detailed", "in-depth", "overview", "survey",
    "compare", "versus", "vs", "difference", "evolution",
    "state of the art", "sota", "latest", "recent",
    "framework", "architecture", "best practices"
]

# Comparison keywords
COMPARISON_KEYWORDS = [
    "vs", "versus", "compare", "comparison", "difference",
    "better", "faster", "more efficient", "pros and cons"
]

# Academic keywords
ACADEMIC_KEYWORDS = [
    "paper", "arxiv", "publication", "citation", "reference",
    "study", "research", "journal", "conference"
]

# GitHub keywords
GITHUB_KEYWORDS = [
    "github", "repo", "repository", "project", "library",
    "framework", "implementation", "code"
]

# Community keywords
COMMUNITY_KEYWORDS = [
    "reddit", "hacker news", "hn", "discussion", "community",
    "consensus", "opinion", "experience"
]


def analyze_query_complexity(query: str) -> Tuple[str, float]:
    """
    Analyze query to determine complexity level

    Returns:
        Tuple of (complexity_level, confidence_score)
    """
    query_lower = query.lower()
    word_count = len(query.split())

    # Count keyword matches
    research_count = sum(1 for kw in RESEARCH_KEYWORDS if kw in query_lower)
    comparison_count = sum(1 for kw in COMPARISON_KEYWORDS if kw in query_lower)
    academic_count = sum(1 for kw in ACADEMIC_KEYWORDS if kw in query_lower)
    github_count = sum(1 for kw in GITHUB_KEYWORDS if kw in query_lower)
    community_count = sum(1 for kw in COMMUNITY_KEYWORDS if kw in query_lower)

    total_matches = research_count + comparison_count + academic_count + github_count + community_count

    # Determine complexity
    if comparison_count > 0 or (research_count >= 2 and word_count > 5):
        return "high", min(0.9, 0.5 + total_matches * 0.1)
    elif research_count >= 1 or word_count > 5:
        return "medium", min(0.7, 0.4 + total_matches * 0.1)
    else:
        return "low", 0.3


def detect_parallelizable_aspects(query: str) -> List[str]:
    """
    Detect aspects of the query that can be parallelized

    Returns:
        List of parallelizable aspect types
    """
    aspects = []
    query_lower = query.lower()

    if any(kw in query_lower for kw in ACADEMIC_KEYWORDS + ["paper", "study", "research"]):
        aspects.append("academic")

    if any(kw in query_lower for kw in GITHUB_KEYWORDS + ["code", "implementation", "library"]):
        aspects.append("github")

    if any(kw in query_lower for kw in COMMUNITY_KEYWORDS + ["discussion", "opinion", "consensus"]):
        aspects.append("community")

    # Add all aspects for comparison queries
    if any(kw in query_lower for kw in COMPARISON_KEYWORDS):
        if "academic" not in aspects:
            aspects.append("academic")
        if "github" not in aspects:
            aspects.append("github")
        if "community" not in aspects:
            aspects.append("community")

    return aspects


def should_use_multi_agent(query: str) -> Tuple[bool, str]:
    """
    Determine if multi-agent approach is recommended

    Based on:
    - 45% threshold rule (Google/MIT study)
    - Query complexity
    - Parallelizable aspects

    Returns:
        Tuple of (recommend_multi_agent, reason)
    """
    complexity, confidence = analyze_query_complexity(query)
    parallelizable = detect_parallelizable_aspects(query)

    # Single-agent success rate estimation based on complexity
    success_rates = {
        "low": 0.85,  # 85% - single-agent fine
        "medium": 0.55,  # 55% - borderline
        "high": 0.35  # 35% - multi-agent needed
    }

    estimated_success_rate = success_rates.get(complexity, 0.5)

    # 45% threshold rule
    if estimated_success_rate < 0.45:
        return True, f"Complexity: {complexity}, Estimated single-agent success: {estimated_success_rate*100:.0f}% (<45% threshold)"

    if len(parallelizable) >= 2:
        return True, f"Has {len(parallelizable)} parallelizable aspects: {', '.join(parallelizable)}"

    if complexity == "high":
        return True, f"High complexity query with {len(parallelizable)} aspect(s) to explore"

    return False, f"Complexity: {complexity}, Single-agent sufficient (success rate: {estimated_success_rate*100:.0f}%)"


def generate_framework_recommendation(query: str) -> Dict[str, Any]:
    """
    Generate framework recommendation based on query analysis

    Based on Chinese community consensus:
    "AutoGen快、CrewAI稳、LangGraph强"

    Returns:
        Framework recommendation with reasoning
    """
    query_lower = query.lower()

    # Analyze query characteristics
    needs_state = any(kw in query_lower for kw in ["state", "memory", "context", "persistence"])
    needs_team = any(kw in query_lower for kw in ["team", "collaboration", "workflow", "orchestration"])
    needs_speed = any(kw in query_lower for kw in ["fast", "quick", "prototype", "research"])

    if needs_state:
        return {
            "framework": "LangGraph",
            "reason": "State-heavy workflow with complex state management",
            "production_ready": True,
            "overhead": "8% latency overhead, lowest token usage",
            "companies": "~400 companies"
        }
    elif needs_team:
        return {
            "framework": "CrewAI",
            "reason": "Team-based collaboration with defined workflows",
            "production_ready": True,
            "overhead": "24% overhead, 2 weeks to production",
            "companies": "150+ enterprises (60% Fortune 500)"
        }
    elif needs_speed:
        return {
            "framework": "AutoGen",
            "reason": "Fast prototyping and research iteration",
            "production_ready": True,
            "overhead": "Mature framework, multi-language support",
            "backing": "Microsoft"
        }
    else:
        return {
            "framework": "Swarm (pattern only)",
            "reason": "Simple handoff pattern for educational purposes",
            "production_ready": False,
            "warning": "NOT production-ready, use LangGraph/CrewAI for production"
        }


def detect_research_intent(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main detection function

    Args:
        input_data: Hook input with user query

    Returns:
        Detection result with recommendations
    """
    query = input_data.get('content', '')
    if not query:
        return {"error": "No query content provided"}

    # Analyze query
    complexity, confidence = analyze_query_complexity(query)
    parallelizable = detect_parallelizable_aspects(query)
    use_multi_agent, reason = should_use_multi_agent(query)
    framework_rec = generate_framework_recommendation(query)

    # Build result
    result = {
        "query": query[:100] + "..." if len(query) > 100 else query,
        "is_research_query": complexity in ["medium", "high"],
        "complexity_level": complexity,
        "confidence_score": confidence,
        "parallelizable_aspects": parallelizable,
        "recommend_multi_agent": use_multi_agent,
        "recommendation_reason": reason,
        "framework_recommendation": framework_rec
    }

    # Add user message if research query detected
    if result["is_research_query"]:
        if use_multi_agent:
            result["systemMessage"] = (
                f"Research query detected (complexity: {complexity}). "
                f"Recommend multi-agent approach: {reason}"
            )
        else:
            result["systemMessage"] = (
                f"Simple research query (complexity: {complexity}). "
                f"Single-agent approach should be sufficient."
            )

    return result


def main():
    """Main hook entry point"""
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        # Detect research intent
        result = detect_research_intent(input_data)

        # Output as JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {e}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
