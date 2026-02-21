# Verification Logic Protocol / 验证逻辑协议

本文档定义了系统验证的核心逻辑和函数，用于检查研究流程各阶段的完成状态。

---

## Overview / 概述

验证逻辑协议提供了一组可复用的验证函数，用于：
- 检查 Phase 完成状态
- 验证数据完整性
- 追踪时间预算使用
- 评估输出质量

---

## Version / 版本

v1.0 (2026-02-21)

---

## Verification Functions / 验证函数

### 1. Phase Completion Check / 阶段完成检查

```python
from pathlib import Path
from typing import Dict, List, Tuple

def check_phase_completion() -> Dict[str, Dict]:
    """
    检查所有阶段的完成状态

    Returns:
        dict: {phase_name: {"completed": bool, "path": str}}
    """
    phases = [
        ("Phase -1", "performance_predictor", "research_data/performance_prediction.json"),
        ("Phase 0", "framework_selector", "research_data/framework_selection.json"),
        ("Phase 0.5", "mcp_coordinator", "research_data/mcp_coordination.json"),
        ("Phase 1", "academic_researcher", "research_data/academic_researcher_output.json"),
        ("Phase 1", "github_watcher", "research_data/github_watcher_output.json"),
        ("Phase 1", "community_listener", "research_data/community_listener_output.json"),
        ("Phase 1.2", "critic_evaluator", "research_data/critic_evaluation_*.json"),
        ("Phase 1.5", "cross_domain_tracker", "research_data/cross_domain_tracking_output.json"),
        ("Phase 2a", "literature_analyzer", "research_data/logic_analysis.json"),
        ("Phase 2b", "deep_research_report_writer", "research_output/*_comprehensive_report.md"),
        ("Phase 2b", "literature_review_writer", "research_output/*_literature_review.md"),
        ("Phase 2d", "link_validator", "research_data/link_validation_output.json"),
    ]

    results = {}
    for phase, agent, path_pattern in phases:
        # Handle wildcard patterns
        if "*" in path_pattern:
            matches = list(Path(".").glob(path_pattern))
            completed = len(matches) > 0
            actual_path = matches[0] if matches else path_pattern
        else:
            actual_path = Path(path_pattern)
            completed = actual_path.exists()

        results[f"{phase}_{agent}"] = {
            "completed": completed,
            "path": str(actual_path)
        }

    return results
```

### 2. Minimum Requirements Check / 最小要求检查

```python
def check_minimum_requirements(output_file: str, agent_type: str) -> Tuple[bool, Dict]:
    """
    检查 Subagent 输出是否满足最小要求

    Args:
        output_file: 输出文件路径
        agent_type: Agent 类型

    Returns:
        tuple: (is_complete, details)
    """
    import json
    from pathlib import Path

    MIN_REQUIREMENTS = {
        "academic_researcher": {
            "papers_analyzed": 5,
            "key_papers": 3
        },
        "github_watcher": {
            "projects_analyzed": 8,
            "key_projects": 4
        },
        "community_listener": {
            "threads_analyzed": 15,
            "consensus_points": 3
        }
    }

    path = Path(output_file)
    if not path.exists():
        return False, {"error": "File not found"}

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    requirements = MIN_REQUIREMENTS.get(agent_type, {})
    issues = []

    if agent_type == "academic_researcher":
        papers = data.get("papers", [])
        key_papers = data.get("key_papers", [])
        if len(papers) < requirements["papers_analyzed"]:
            issues.append(f"Insufficient papers: {len(papers)} < {requirements['papers_analyzed']}")
        if len(key_papers) < requirements["key_papers"]:
            issues.append(f"Insufficient key papers: {len(key_papers)} < {requirements['key_papers']}")

    elif agent_type == "github_watcher":
        projects = data.get("projects", [])
        key_projects = data.get("key_projects", [])
        if len(projects) < requirements["projects_analyzed"]:
            issues.append(f"Insufficient projects: {len(projects)} < {requirements['projects_analyzed']}")
        if len(key_projects) < requirements["key_projects"]:
            issues.append(f"Insufficient key projects: {len(key_projects)} < {requirements['key_projects']}")

    elif agent_type == "community_listener":
        discussions = data.get("discussions", [])
        consensus = data.get("consensus_points", [])
        if len(discussions) < requirements["threads_analyzed"]:
            issues.append(f"Insufficient discussions: {len(discussions)} < {requirements['threads_analyzed']}")
        if len(consensus) < requirements["consensus_points"]:
            issues.append(f"Insufficient consensus: {len(consensus)} < {requirements['consensus_points']}")

    is_complete = len(issues) == 0
    details = {
        "issues": issues,
        "requirements": requirements,
        "actual": {
            "papers": len(data.get("papers", [])) if agent_type == "academic_researcher" else None,
            "projects": len(data.get("projects", [])) if agent_type == "github_watcher" else None,
            "discussions": len(data.get("discussions", [])) if agent_type == "community_listener" else None,
        }
    }

    return is_complete, details
```

### 3. Time Budget Validation / 时间预算验证

```python
def validate_time_budget(time_allocation: Dict, agent_outputs: List[str]) -> Dict:
    """
    验证时间预算分配是否正确执行

    Args:
        time_allocation: 时间分配字典
        agent_outputs: Agent 输出文件列表

    Returns:
        dict: 验证结果
    """
    from pathlib import Path
    import json

    results = {
        "per_agent_timeout_seconds": time_allocation.get("per_agent_timeout_seconds"),
        "agents_checked": [],
        "time_tracking_found": False
    }

    for output_file in agent_outputs:
        path = Path(output_file)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            time_assessment = data.get("time_assessment", {})
            checkpoints = data.get("checkpoints", [])

            if time_assessment:
                results["time_tracking_found"] = True
                results["agents_checked"].append({
                    "agent": output_file,
                    "elapsed": time_assessment.get("elapsed_seconds"),
                    "remaining": time_assessment.get("remaining_seconds"),
                    "status": time_assessment.get("time_status")
                })

    return results
```

### 4. Output File Naming Validation / 输出文件命名验证

```python
def validate_output_file_naming() -> Dict[str, bool]:
    """
    验证输出文件命名是否符合规范

    规范: {agent_type}_output.json (连字符转下划线)

    Returns:
        dict: {file_pattern: exists}
    """
    from pathlib import Path

    expected_files = {
        "academic_researcher_output.json": "research_data/academic_researcher_output.json",
        "github_watcher_output.json": "research_data/github_watcher_output.json",
        "community_listener_output.json": "research_data/community_listener_output.json",
        "logic_analysis.json": "research_data/logic_analysis.json",
        "cross_domain_tracking_output.json": "research_data/cross_domain_tracking_output.json",
    }

    results = {}
    for name, path in expected_files.items():
        results[name] = Path(path).exists()

    return results
```

### 5. Data Integrity Check / 数据完整性检查

```python
def check_data_integrity() -> Dict:
    """
    检查研究数据的完整性

    Returns:
        dict: 完整性检查结果
    """
    import json
    from pathlib import Path

    results = {
        "files_checked": [],
        "integrity_issues": []
    }

    research_files = [
        "research_data/academic_researcher_output.json",
        "research_data/github_watcher_output.json",
        "research_data/community_listener_output.json",
        "research_data/logic_analysis.json"
    ]

    for file_path in research_files:
        path = Path(file_path)
        results["files_checked"].append(file_path)

        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Check for required fields
                if "papers" in data or "projects" in data or "discussions" in data:
                    # Check for timestamp
                    if "timestamp" not in data:
                        results["integrity_issues"].append(f"{file_path}: Missing timestamp")

                    # Check for agent_type
                    if "agent_type" not in data:
                        results["integrity_issues"].append(f"{file_path}: Missing agent_type")

            except json.JSONDecodeError as e:
                results["integrity_issues"].append(f"{file_path}: Invalid JSON - {e}")

    return results
```

---

## Verification Report / 验证报告

### Report Format

```python
def generate_verification_report() -> str:
    """
    生成完整的验证报告

    Returns:
        str: 格式化的验证报告
    """
    phase_status = check_phase_completion()
    output_files = validate_output_file_naming()
    integrity = check_data_integrity()

    report = []
    report.append("┌" + "─" * 58 + "┐")
    report.append("│ " + " " * 15 + "VERIFICATION REPORT" + " " * 27 + "│")
    report.append("├" + "─" * 58 + "┤")

    # Phase Status
    report.append("│ Phase Completion:")
    for phase, status in phase_status.items():
        icon = "✅" if status["completed"] else "❌"
        report.append(f"│   {icon} {phase}")

    # Output Files
    report.append("│")
    report.append("│ Output Files:")
    for file_name, exists in output_files.items():
        icon = "✅" if exists else "❌"
        report.append(f"│   {icon} {file_name}")

    # Integrity
    report.append("│")
    report.append("│ Data Integrity:")
    if integrity["integrity_issues"]:
        for issue in integrity["integrity_issues"]:
            report.append(f"│   ⚠️  {issue}")
    else:
        report.append("│   ✅ No integrity issues found")

    report.append("└" + "─" * 58 + "┘")

    return "\n".join(report)
```

---

## Usage / 使用方法

### 在 CLAUDE.md 中引用

```markdown
## 引用验证协议

@knowledge: .claude/protocols/verification-logic.md
```

### 在代码中调用

```python
from .claude.protocols.verification_logic import (
    check_phase_completion,
    check_minimum_requirements,
    validate_time_budget,
    validate_output_file_naming,
    check_data_integrity,
    generate_verification_report
)

# 执行完整验证
report = generate_verification_report()
print(report)
```

---

## CHANGELOG

### v1.0 (2026-02-21)

**Initial Release**:
- ✅ Phase completion check function
- ✅ Minimum requirements validation
- ✅ Time budget validation
- ✅ Output file naming validation
- ✅ Data integrity check
- ✅ Verification report generation
