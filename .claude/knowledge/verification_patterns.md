# Verification Patterns / 验证模式

本文档包含工作流验证的完整代码实现。

---

## Workflow Verification / 工作流验证

```python
def verify_workflow_execution() -> dict:
    """
    验证完整工作流执行

    Returns:
        dict: {
            "phase_checks": {...},
            "data_integrity": {...},
            "time_tracking": {...},
            "output_quality": {...}
        }
    """
    from pathlib import Path
    import json

    results = {
        "phase_checks": {},
        "data_integrity": {},
        "time_tracking": {},
        "output_quality": {}
    }

    # 1. Phase Completion Checks
    phases = [
        ("Phase -1", "research_data/performance_prediction.json"),
        ("Phase 0", "research_data/framework_selection.json"),
        ("Phase 1", "research_data/academic_researcher_output.json"),
        ("Phase 1", "research_data/github_researcher_output.json"),
        ("Phase 1", "research_data/community_researcher_output.json"),
        ("Phase 2a", "research_data/logic_analysis.json"),
        ("Phase 2b", "research_output/{topic}_comprehensive_report.md"),
        ("Phase 2b", "research_output/{topic}_literature_review.md"),
    ]

    for phase, path in phases:
        exists = Path(path.format(topic="*")).exists() or Path(path).exists()
        results["phase_checks"][phase] = {
            "completed": exists,
            "path": path
        }

    # 2. Data Integrity Checks (Problem 3: 搜索完成但数据未记录)
    for agent_type in ["academic", "github", "community"]:
        output_file = f"research_data/{agent_type}_researcher_output.json"
        path = Path(output_file)

        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check atomic write markers
            has_error_handling = "last_error" in data.get("subagent_metadata", {})
            has_checkpoints = len(data.get("subagent_metadata", {}).get("checkpoints", [])) > 0

            results["data_integrity"][agent_type] = {
                "file_exists": True,
                "checkpoints_count": len(data.get("subagent_metadata", {}).get("checkpoints", [])),
                "atomic_write_markers": has_error_handling,
                "items_count": len(data.get("items", [])),
                "save_failed": data.get("subagent_metadata", {}).get("save_failed", False)
            }
        else:
            results["data_integrity"][agent_type] = {"file_exists": False}

    # 3. Time Tracking Checks (Problem 1: 搜索 subagent 没有按时间被打断)
    for agent_type in ["academic", "github", "community"]:
        output_file = f"research_data/{agent_type}_researcher_output.json"
        path = Path(output_file)

        if path.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            checkpoints = data.get("subagent_metadata", {}).get("checkpoints", [])
            time_assessments = [cp.get("time_assessment") for cp in checkpoints if cp.get("time_assessment")]

            # Check if any checkpoint has time data
            has_time_tracking = len(time_assessments) > 0

            # Check if any checkpoint entered time_critical
            entered_accelerate = any(
                ta.get("time_status") == "time_critical"
                for ta in time_assessments if ta
            )

            results["time_tracking"][agent_type] = {
                "has_time_tracking": has_time_tracking,
                "checkpoints_with_time": len(time_assessments),
                "entered_accelerate_mode": entered_accelerate,
                "latest_status": time_assessments[-1].get("time_status") if time_assessments else None
            }
        else:
            results["time_tracking"][agent_type] = {"file_exists": False}

    # 4. Output Quality Checks (Problem 4: 报告格式自动检测)
    import re

    # Check if Phase -0.5 intent detection exists
    intent_file = Path("research_data/user_intent.json")
    results["output_quality"]["intent_detected"] = intent_file.exists()

    if intent_file.exists():
        with open(intent_file, 'r', encoding='utf-8') as f:
            intent_data = json.load(f)
        results["output_quality"]["detected_formats"] = intent_data.get("output_formats", [])

    # Check for custom output files (from Phase 2e)
    custom_output_patterns = {
        "blog_post": "*_blog_post.md",
        "slide_deck": "*_slide_deck.md",
        "code_examples": "*_code_examples.md",
        "summary": "*_summary.md",
        "comparison": "*_comparison.md",
        "proposal": "*_proposal.md",
    }

    for format_type, pattern in custom_output_patterns.items():
        matches = list(Path("research_output").glob(pattern))
        results["output_quality"][f"has_{format_type}"] = len(matches) > 0

    return results
```

---

## Verification Report Printer / 验证报告打印

```python
def print_verification_report(results: dict):
    """打印验证报告"""
    print("┌" + "─" * 58 + "┐")
    print("│ " + " " * 10 + "WORKFLOW VERIFICATION REPORT" + " " * 24 + "│")
    print("├" + "─" * 58 + "┤")

    # Phase Completion
    print("│ Phase Completion:")
    for phase, check in results["phase_checks"].items():
        status = "✅" if check["completed"] else "❌"
        print(f"│   {status} {phase}")

    # Data Integrity
    print("│ Data Integrity (Problem 3):")
    for agent, check in results["data_integrity"].items():
        if check.get("file_exists"):
            save_status = "✅" if not check.get("save_failed") else "⚠️"
            print(f"│   {save_status} {agent}: {check['items_count']} items, {check['checkpoints_count']} checkpoints")
        else:
            print(f"│   ❌ {agent}: File not found")

    # Time Tracking
    print("│ Time Tracking (Problem 1):")
    for agent, check in results["time_tracking"].items():
        if check.get("file_exists"):
            tracking = "✅" if check["has_time_tracking"] else "⚠️"
            accelerate = "⚡" if check.get("entered_accelerate_mode") else ""
            print(f"│   {tracking} {agent}: {check['checkpoints_with_time']} timed checkpoints {accelerate}")
        else:
            print(f"│   ❌ {agent}: File not found")

    # Output Quality
    print("│ Output Detection (Problem 4):")
    intent = "✅" if results["output_quality"].get("intent_detected") else "❌"
    print(f"│   {intent} User Intent Detection")

    custom_outputs = [k for k, v in results["output_quality"].items() if k.startswith("has_") and v]
    if custom_outputs:
        print(f"│   ✅ Custom Outputs: {', '.join([co.replace('has_', '') for co in custom_outputs])}")
    else:
        print("│   ℹ️  No custom outputs detected")

    print("└" + "─" * 58 + "┘")
```

---

## Quality Checklists / 质量检查清单 {#quality-checklists}

### Comprehensive Report Quality
- [ ] research_output/{topic}_comprehensive_report.md exists
- [ ] Word count 6,000-8,000
- [ ] Executive Summary has 6-8 insights
- [ ] Citation graph (Mermaid) included
- [ ] All citations clickable

### Literature Review Quality
- [ ] research_output/{topic}_literature_review.md exists
- [ ] Word count 3,000-5,000
- [ ] Logical flow (not mechanical listing)
- [ ] Uses logic_analysis.json insights
- [ ] Contains evolution paths and paradigm shifts

### Link Validation
- [ ] research_data/link_validation_output.json exists
- [ ] All links validated (100% coverage)
- [ ] If broken_links > 0: Report details to user

---

## Link Validation Output Format / 链接验证输出格式

```json
{
  "validation_id": "link_validation_YYYYMMDD_HHMMSS",
  "total_links_found": 45,
  "valid_links": 42,
  "broken_links": 2,
  "timeout_links": 1,
  "validation_rate": 93.33,
  "broken_links_detail": [...]
}
```

**重要**: 链接验证是自动执行的，不修改原报告。如发现问题需手动修复。
