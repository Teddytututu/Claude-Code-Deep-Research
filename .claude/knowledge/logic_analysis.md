# Logic Analysis / 逻辑分析

## Overview / 概述

Literature Logic Analysis based on **PRISMA 2020** standards for systematic reviews and meta-analyses.

**Core Principle**: "Synthesis over Summary" - 综合建立洞察，而非简单罗列

---

## PRISMA 2020 Framework / PRISMA 2020 框架

### Compliance Check / 合规性检查

```python
def prisma_2020_compliance_check(academic_data):
    return {
        "identification": {
            "total_records_identified": len(papers),
            "duplicates_removed": 0,
            "records_screened": len(papers)
        },
        "eligibility": {
            "full_text_assessed": len(papers),
            "inclusion_criteria": [
                "Peer-reviewed academic papers",
                "Relevant to research topic",
                "Published in last 5 years (with exceptions)"
            ],
            "exclusion_criteria": [
                "Non-peer-reviewed sources",
                "Papers without methodology",
                "Papers with insufficient data"
            ]
        },
        "included": {
            "qualitative_synthesis": len(papers),
            "quantitative_synthesis": 0
        }
    }
```

---

## Citation Network Analysis / 引用网络分析

### Root Papers / 根基论文

**Identification criteria**:
- High citation count (>50)
- Early work in field
- Foundational contribution
- Time-validated influence

**Example**:
```json
{
  "arxiv_id": "2307.16789",
  "title": "AgentBench: Evaluating AI Agents",
  "citation_count": 150,
  "is_root": true,
  "contribution": "建立多环境评估框架",
  "confidence_level": "high"
}
```

### Inheritance Chains / 继承链条

**Types**:
- `direct`: Direct citation relationship
- `concept`: Conceptual inheritance
- `method`: Methodological inheritance

**Structure**:
```json
{
  "chain_id": "chain_001",
  "root": "2307.16789",
  "citing_papers": ["2404.03807", "2504.14773"],
  "inheritance_type": "direct",
  "evolution_path": "多环境评估 → 多维度分析平台",
  "temporal_validated": true
}
```

---

## Thematic Analysis / 主题分析

### Core Themes / 核心主题

**Identification**:
```python
def identify_core_themes(academic_data):
    # 1. Extract keywords from titles/abstracts
    # 2. Group papers by semantic similarity
    # 3. Identify consensus_strength
    # 4. Extract synthesis
```

**Theme structure**:
```json
{
  "theme_id": "theme_001",
  "theme_name": "evaluation_metrics",
  "papers": ["2307.16789", "2404.03807", "2504.14773"],
  "consensus": "多维度评估优于单一指标",
  "consensus_strength": "strong",
  "synthesis": "虽然所有论文都认同多维度评估的重要性，但在具体指标设计上存在不同路径..."
}
```

### Methodological Families / 方法论家族

```python
methodological_families = {
    "simulation_based": {
        "papers": ["2307.16789", "2401.02009"],
        "common_approach": "使用模拟环境评估 agent 能力",
        "advantages": ["可控性强", "可重复", "成本低"],
        "limitations": ["与真实场景存在差距"]
    }
}
```

---

## Evolution Analysis / 演进分析

### Timeline Tracking / 时间线追踪

```python
timeline = [
    {
        "period": "2023 Q3",
        "papers": ["2307.16789"],
        "breakthrough": "建立基础评估框架",
        "impact_level": "foundational"
    },
    {
        "period": "2024 Q2",
        "papers": ["2404.03807"],
        "breakthrough": "统一评估平台",
        "impact_level": "significant"
    }
]
```

### Paradigm Shifts / 范式转移

```json
{
  "shift_id": "shift_001",
  "shift_name": "从单一指标到多维评估",
  "from": "二分类成功/失败",
  "to": "多维度评估（成功+进度+成本）",
  "triggering_papers": ["2404.03807"],
  "evidence_strength": "strong"
}
```

---

## Research Gaps / 研究空白

### Gap Types / 空白类型

| Type | Description | Evidence Level |
|------|-------------|----------------|
| `stated` | Explicitly mentioned in papers | High |
| `implicit` | Not researched but important | Moderate |

**Gap structure**:
```json
{
  "gap_id": "gap_001",
  "gap_description": "缺少安全性评估维度",
  "gap_type": "implicit",
  "evidence": "现有 benchmark 主要关注功能完成度",
  "importance": "high",
  "feasibility": "medium",
  "confidence": 0.75
}
```

---

## Anti-Patterns / 反模式

### Detection & Prevention

| Pattern | Detection | Fix Strategy |
|---------|-----------|--------------|
| **Citation dumping** | Regex: `\([A-Z]+ et al.\) [^。.]+。 \([A-Z]+` | Group by theme: "Multiple studies (A; B) found X" |
| **Single-sentence citations** | Consecutive single-citation sentences | Merge: "Studies (A; B) consistently show X" |
| **Chronological-only organization** | Only time-based sections | Create thematic sections, use time within themes |
| **Missing synthesis** | No concluding summary sentence | Add: "Collectively, these studies suggest..." |
| **Lack of critical analysis** | Only contributions, no limitations | Balance: "While X contributes Y, it faces limitations in Z" |
| **Missing signposting** | No transition between sections | Add: "Having examined X, I now turn to Y..." |

---

## Synthesis Opportunities / 综合机会

### Convergence Type / 收敛型

**Multiple papers agree on a finding**:

```markdown
**Template**: Recent studies have consistently demonstrated {finding} ({citations}). **Evidence**: {details}. **Analysis**: {implication}. **Transition**: However, {contrast}.

**Example**: Recent studies have consistently demonstrated multi-dimensional evaluation superiority (AgentBench; AgentBoard; PLANET). Early work established binary success metrics, while subsequent studies introduced fine-grained progress tracking. This convergence reflects growing understanding that single metrics cannot capture complex agent behaviors.
```

### Divergence Type / 分歧型

**Different perspectives on a topic**:

```markdown
**Template**: Researchers disagree on {topic}. **Viewpoint A**: {papers_a} emphasize {point_a}. **Viewpoint B**: In contrast, {papers_b} argue that {point_b}. **Synthesis**: This divergence reflects {reason}.

**Example**: Researchers disagree on optimal evaluation metrics. While Smith et al. (2020) and Jones (2021) emphasize binary success metrics, Brown (2022) argues that fine-grained progress tracking is essential. This divergence reflects different application domains.
```

### Evolution Type / 演进型

**Progression over time**:

```markdown
**Template**: The field has evolved from {old} to {new}. **Early Work**: {early_paper} established {foundation}. **Evolution**: {middle_paper} introduced {innovation}. **Current State**: {recent_paper} demonstrates {current}. **Synthesis**: This evolution reflects {driver}.

**Example**: The field has evolved from binary to multi-dimensional evaluation. Early work established binary framework. Building on this, Jones (2021) introduced progress tracking. Brown (2022) now demonstrates comprehensive evaluation. This evolution reflects growing understanding of complex agent behaviors.
```

---

## Quality Assessment / 质量评估

### AMSTAR 2 Domains

```python
amstar2_domains = {
    "protocol_registered": paper.get("protocol_registered", False),
    "literature_search_comprehensive": search == "comprehensive",
    "justified_exclusion": len(exclusion_criteria) > 0,
    "risk_of_bias_assessed": paper.get("bias_assessment", False),
    "appropriate_meta_analysis": paper.get("meta_analysis", False)
}
```

### ROBIS Bias Risk

```python
robis_domains = {
    "study_eligibility": "low/medium/high",
    "study_selection": "low/medium/high",
    "data_collection": "low/medium/high"
}
```

---

## Writing Guidance / 写作指导

### Paragraph Templates / 段落模板

**Synthesis Convergence**:
- Topic Sentence → Evidence (multiple citations) → Analysis → Transition

**Comparison Divergence**:
- Topic Sentence → Viewpoint A → Viewpoint B → Synthesis

**Evolution Progressive**:
- Topic Sentence → Early Work → Evolution → Current State → Synthesis

### Signposting Phrases / 路标短语

**Section Opening**:
- "Three main themes emerge from the literature:"
- "This section examines {theme} through the lens of {perspective}:"

**Section Transition**:
- "Having examined {previous}, I now turn to {next}:"
- "The previous section established {previous_finding}. This section extends this by examining {next_aspect}:"

**Synthesis Markers**:
- "Collectively, these studies suggest..."
- "Taken together, these findings indicate..."
- "Synthesizing these results reveals..."

---

## Narrative Structures / 叙事结构

| Structure | Description | Best For |
|-----------|-------------|----------|
| **Hourglass** | Broad → Narrow → Broad (15-55-30%) | General introductions |
| **Thematic** | 3-5 main themes | Conceptual reviews |
| **Developmental** | Early → Middle → Current → Future | Historical reviews |

---

## CLI Usage / 命令行使用

```bash
# Logic analysis is performed by literature-analyzer agent
# No direct Python tool - uses Read/Write tools

# Input: research_data/*.json
# Output: research_data/logic_analysis.json
```

---

## Related Knowledge / 相关知识

- **report_templates.md**: Using logic analysis for report generation
- **quality_checklist.md**: Quality validation based on logic analysis
- **literature-review-writer.md**: Agent that uses logic analysis

---

## Evidence Levels / 证据等级

| Level | Description | Example |
|-------|-------------|---------|
| **very_strong** | Multiple high-quality studies, consistent findings | Meta-analysis with >1000 samples |
| **strong** | Multiple studies, consistent findings | 3+ RCTs with large samples |
| **moderate** | Few studies, some inconsistency | 2-3 observational studies |
| **weak** | Single study or expert opinion | Case study or expert opinion |

---

## Confidence Levels / 置信度

| Level | Range | Usage |
|-------|-------|-------|
| **high** | 0.8-1.0 | Strong evidence, validated |
| **medium-high** | 0.6-0.8 | Good evidence, some validation |
| **medium** | 0.4-0.6 | Moderate evidence, limited validation |
| **medium-low** | 0.2-0.4 | Weak evidence, indirect |
| **low** | 0.0-0.2 | Very weak evidence, speculation |
