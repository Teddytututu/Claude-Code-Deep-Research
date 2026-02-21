# Quality Checklist Knowledge Base

## Overview
从 `quality_gate.py` 提取的质量检查清单核心逻辑

**Purpose**: 提供研究输出质量验证的标准和清单

**Related Files**:
- `quality_validation.md` - Detailed validation functions for literature reviews
- `verification_patterns.md` - Workflow verification patterns

---

## Key Classes / 类

### QualityDimension

**Purpose**: 质量维度枚举

**Values**:
- `CITATION_COMPLETENESS`: 引用完整性
- `METHODOLOGY_CLARITY`: 方法论清晰度
- `ANALYSIS_DEPTH`: 分析深度
- `BILINGUAL_CONSISTENCY`: 双语一致性
- `WORD_COUNT`: 字数达标
- `SOURCE_DIVERSITY`: 来源多样性

### QualityGate

**Purpose**: 质量门主类

**Key Methods**:
- `evaluate_research_output(json_file)`: 评估研究输出 (JSON)
- `evaluate_markdown_report(md_file)`: 评估 Markdown 报告
- `generate_quality_report()`: 生成质量报告
- `check_dimension(dimension, data)`: 检查单个维度

### QualityReport

**Purpose**: 质量报告数据结构

**Key Attributes**:
- `overall_score`: 总体分数 (0.0-1.0)
- `dimension_scores`: 各维度分数字典
- `passed_dimensions`: 通过的维度列表
- `failed_dimensions`: 未通过的维度列表
- `recommendations`: 改进建议列表
- `threshold`: 质量阈值 (默认 0.7)

### CitationValidator

**Purpose**: 引用验证器

**Key Methods**:
- `validate_arxiv_links(json_data)`: 验证 arXiv 链接
- `check_citation_format(json_data)`: 检查引用格式
- `extract_citation_count(json_data)`: 提取引用数量

---

## Decision Logic / 决策逻辑

### Scoring Criteria

```python
# Quality Dimension Scoring (0.0 - 1.0)

SCORING_CRITERIA = {
    "citation_completeness": {
        "1.0": "All sources have complete citation info (arxiv_id, url, title, authors)",
        "0.8": "Most sources complete, minor gaps",
        "0.6": "Basic citation info present, missing some details",
        "0.4": "Minimal citation info",
        "0.0": "No citations or citation data"
    },
    "methodology_clarity": {
        "1.0": "Detailed methodology: datasets, baselines, metrics, models",
        "0.8": "Good methodology detail, minor gaps",
        "0.6": "Basic methodology description",
        "0.4": "Vague methodology",
        "0.0": "No methodology section"
    },
    "analysis_depth": {
        "1.0": "Deep analysis: limitations, future work, quantitative results",
        "0.8": "Good analysis, some depth",
        "0.6": "Surface-level analysis",
        "0.4": "Minimal analysis",
        "0.0": "No analysis"
    },
    "bilingual_consistency": {
        "1.0": "Perfect Chinese + English format throughout",
        "0.8": "Mostly consistent, minor inconsistencies",
        "0.6": "Some inconsistencies",
        "0.4": "Major inconsistencies",
        "0.0": "Single language or inconsistent"
    },
    "word_count": {
        "1.0": "Within target range (academic: 3000-5000, comprehensive: 6000-8000)",
        "0.8": "Slightly outside range (±10%)",
        "0.6": "Outside range (±25%)",
        "0.4": "Far outside range (±50%)",
        "0.0": "Too short or too long"
    },
    "source_diversity": {
        "1.0": "Diverse sources: academic papers, GitHub repos, community discussions",
        "0.8": "Good diversity, missing one source type",
        "0.6": "Limited diversity (2 source types)",
        "0.4": "Single source type",
        "0.0": "No sources or single source"
    }
}
```

### Quality Threshold Decision

```python
def evaluate_quality(scores, threshold=0.7):
    """
    质量评估决策

    Threshold: 0.7 (default)

    Decision:
        - overall_score >= threshold: PASS
        - overall_score < threshold: FAIL

    Returns:
        passed: bool
        score: float (0.0-1.0)
        recommendations: list of improvement suggestions
    """

    overall_score = sum(scores.values()) / len(scores)

    if overall_score >= threshold:
        return {
            "passed": True,
            "score": overall_score,
            "message": f"Quality gate PASSED with score {overall_score:.2f}"
        }
    else:
        # Generate recommendations for failed dimensions
        recommendations = []
        for dimension, score in scores.items():
            if score < threshold:
                recommendations.append(generate_recommendation(dimension, score))

        return {
            "passed": False,
            "score": overall_score,
            "message": f"Quality gate FAILED with score {overall_score:.2f}",
            "recommendations": recommendations
        }
```

---

## Code Patterns / 代码模式

### Pattern 1: Quality Gate Evaluation

```python
# Evaluate research output JSON
gate = QualityGate(threshold=0.7)

result = gate.evaluate_research_output(
    json_file="research_data/academic_research_output.json"
)

if result["passed"]:
    print("Quality PASSED")
else:
    print("Quality FAILED")
    for rec in result["recommendations"]:
        print(f"- {rec}")
```

### Pattern 2: Citation Validation

```python
# Validate citations
validator = CitationValidator()

validation_result = validator.validate_arxiv_links(json_data)

# Result:
# {
#     "valid_links": 10,
#     "invalid_links": 2,
#     "missing_links": 1,
#     "issues": ["Paper ID xyz has no arxiv_id field"]
# }
```

### Pattern 3: Markdown Report Validation

```python
# Validate generated report
report_quality = gate.evaluate_markdown_report(
    md_file="research_output/topic_comprehensive_report.md",
    expected_sections=["Abstract", "Introduction", "Analysis", "Conclusion"]
)

# Check word count
if report_quality["word_count_score"] < 0.8:
    print("Report too short. Current: {count} words, Expected: 6000-8000")
```

---

## CLI Usage / 命令行使用

```bash
python "tools\quality_gate.py" --findings research_data/academic_research_output.json
python "tools\quality_gate.py" --report research_output/topic_report.md
python "tools\quality_gate.py" --all --threshold 0.8
```

**Commands**:
- `--findings`: 评估研究输出 JSON
- `--report`: 评估 Markdown 报告
- `--all`: 评估所有输出
- `--threshold`: 设置质量阈值 (默认 0.7)

---

## Integration Points / 集成点

**Reading Agents**:
- `deep-research-report-writer`: 使用质量检查清单验证报告
- `literature-review-writer`: 使用质量检查清单验证文献综述

**CLI Invocations**:
```bash
# Report writer agent can invoke
python "tools\quality_gate.py" --findings research_data/academic_research_output.json --threshold 0.7
```

**Related Knowledge Base**:
- `.claude/knowledge/report_templates.md`: 报告模板相关

---

## Quality Checklist Items / 质量检查清单

### Academic Research Output (JSON)

```markdown
## Quality Checklist for academic_research_output.json

### Citation Completeness
- [ ] All papers have `arxiv_id` field
- [ ] All papers have `url_markdown` with clickable links
- [ ] All papers have `title` field
- [ ] All papers have `abstract` field (200-500 words)
- [ ] All papers have `url` and `pdf_url` fields

### Methodology Clarity
- [ ] Each paper has `methodology` object
- [ ] `datasets` field present and detailed
- [ ] `baselines` field present
- [ ] `models_tested` field present
- [ ] `evaluation_metrics` field present

### Analysis Depth
- [ ] Each paper has `quantitative_results` object
- [ ] `benchmarks` field present with numbers
- [ ] `comparisons` field present
- [ ] `statistical_significance` mentioned if applicable
- [ ] `limitations` list present (at least 1)
- [ ] `future_work` list present (at least 1)

### Implementation Availability
- [ ] `implementation` object present
- [ ] `code_url` provided if available
- [ ] `datasets_available` boolean field
- [ ] `reproducibility_score` present

### Source Count
- [ ] At least 5 papers included
- [ ] Papers from recent research (2024-2026 preferred)
```

### GitHub Research Output (JSON)

```markdown
## Quality Checklist for github_research_output.json

### Project Completeness
- [ ] All repos have `name` (format: owner/repo)
- [ ] All repos have `url_markdown` with clickable link
- [ ] All repos have `description` field
- [ ] All repos have `stars_display` field

### Architecture Analysis
- [ ] `key_files` list present (at least 2 files)
- [ ] Each key file has `path` and `description`
- [ ] `architecture_description` present (200-500 words)
- [ ] `integration_examples` present

### Project Metadata
- [ ] `last_commit_date` present (ISO format)
- [ ] `license` field present
- [ ] `performance_benchmarks` object if applicable

### Source Count
- [ ] At least 3 repos included
- [ ] Repos have meaningful star counts (>100 recommended)
```

### Community Research Output (JSON)

```markdown
## Quality Checklist for community_research_output.json

### Discussion Completeness
- [ ] All discussions have `platform` field
- [ ] All discussions have `url_markdown` with clickable link
- [ ] All discussions have `title` field
- [ ] All discussions have `summary` field (200-400 words)

### Key Quotes
- [ ] `key_quotes` list present
- [ ] Each quote has `user`, `quote`, `upvotes` fields
- [ ] Original title preserved for non-English discussions

### Consensus Analysis
- [ ] `consensus_level` present (high/medium/low/none)
- [ ] `original_title` present for non-English

### Source Count
- [ ] At least 2 platform types (Reddit, HN, etc.)
- [ ] At least 5 discussions total
```

### Comprehensive Report (Markdown)

```markdown
## Quality Checklist for Comprehensive Report

### Structure
- [ ] Word count 6,000-8,000
- [ ] Executive Summary present with 6-8 insights
- [ ] All required sections present
- [ ] Citations properly formatted
- [ ] Citation graph (Mermaid) included

### Content Quality
- [ ] At least 3 academic papers cited
- [ ] At least 2 GitHub repos analyzed
- [ ] At least 2 community discussions included
- [ ] Bilingual format consistent (Chinese + English)

### Executive Summary
- [ ] 6-8 key insights
- [ ] Each insight with evidence and citations
- [ ] Practical recommendations section

### Citations
- [ ] All citations clickable
- [ ] Citation format consistent
- [ ] No broken links
- [ ] Citation graph visualization included
```

### Literature Review (Markdown)

```markdown
## Quality Checklist for Literature Review

### Structure
- [ ] Word count 3,000-5,000
- [ ] Abstract present with background, findings, gaps, keywords
- [ ] Introduction with scope and organization
- [ ] Research Evolution section
- [ ] Thematic Analysis section (at least 2 themes)
- [ ] Research Gaps and Future Directions section
- [ ] Conclusion section

### Content Quality
- [ ] Based on logic_analysis.json
- [ ] Logical flow (not mechanical listing)
- [ ] Evolution paths explicitly cited
- [ ] Paradigm shifts identified
- [ ] Research gaps with evidence
- [ ] Open questions listed

### Logical Connectors
- [ ] At least 5 different types of logical connectors used
- [ ] Evolutionary connectors (然而, 为解决这一问题, 推动)
- [ ] Inheritance connectors (基于, 扩展了, 改进了)
- [ ] Comparative connectors (相比之下, 与...不同)

### Anti-Pattern Prevention
- [ ] No mechanical listing
- [ ] No annotated bibliography style
- [ ] Not purely chronological
- [ ] Has synthesis sentences
- [ ] Has critical analysis
```

---

## Notes / 说明

- **Default Threshold**: 0.7 (70%)
- **Adjustable**: `--threshold` flag can set different levels
- **Recommendations**: Auto-generated for failed dimensions
- **Comprehensive**: Covers all 6 quality dimensions
- **CLI Ready**: Can be invoked from agent workflows
