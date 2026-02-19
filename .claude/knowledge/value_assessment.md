# Value Assessment Framework / 价值评估框架

> **Purpose**: Define the four-dimensional value assessment system for research papers.
> **Usage**: Reference this file via `@knowledge:value_assessment.md`
> **Depends on**: `@knowledge:institution_patterns.md`
> **Version**: 1.0 (2026-02-19)

---

## Overview / 概述

本文档定义了研究论文的**四维价值评估系统**，用于：
1. 识别高价值研究（S/A/B/C 分级）
2. 生成 Top Picks 推荐列表
3. 突出新兴趋势和行业采用信号

**核心公式**:
```
Value Score = Impact(30%) + Innovation(25%) + Practicality(25%) + Timeliness(20%) + Institution_Boost
```

---

## VALUE_DIMENSIONS / 四个评估维度

### 1. ImpactScore (影响力) - 30% 权重

衡量研究的外部影响和关注程度。

| Metric | Description | Score Range |
|--------|-------------|-------------|
| `citation_velocity` | 近 6 个月引用速度 (citations / months) | 0.0 - 1.0 |
| `github_stars` | 如有代码实现，GitHub 星标数 | 0.0 - 1.0 |
| `community_mentions` | 社区讨论热度（Reddit, HN, Twitter） | 0.0 - 1.0 |
| `big_tech_backing` | 大厂背书（来自 institution_patterns） | 0 / 1 |

**计算公式**:
```python
def calculate_impact_score(paper, github_data=None, community_data=None):
    """
    计算影响力分数

    Args:
        paper: 论文数据
        github_data: GitHub 相关数据（可选）
        community_data: 社区讨论数据（可选）

    Returns:
        float: 0.0 - 1.0
    """
    score = 0

    # 引用速度 (权重 40%)
    citations = paper.get("citations", 0)
    months_since_publish = paper.get("months_since_publish", 1)
    citation_velocity = citations / max(months_since_publish, 1)
    # 归一化: 10 citations/month = 1.0
    score += min(citation_velocity / 10, 1.0) * 0.40

    # GitHub 星标 (权重 30%)
    if github_data:
        stars = github_data.get("stars", 0)
        # 归一化: 1000 stars = 1.0
        score += min(stars / 1000, 1.0) * 0.30
    else:
        score += 0.15  # 无代码时给中等分

    # 社区讨论 (权重 30%)
    if community_data:
        mentions = community_data.get("mention_count", 0)
        # 归一化: 50 mentions = 1.0
        score += min(mentions / 50, 1.0) * 0.30
    else:
        score += 0.15

    return min(score, 1.0)
```

### 2. InnovationScore (创新性) - 25% 权重

衡量研究的新颖性和突破程度。

| Metric | Description | Values |
|--------|-------------|--------|
| `novelty` | 新颖性 | 0.0 - 1.0 |
| `breakthrough_level` | 突破程度 | incremental / significant / paradigm_shift |
| `first_of_kind` | 是否首创 | True / False |

**计算公式**:
```python
def calculate_innovation_score(paper):
    """
    计算创新性分数

    Returns:
        float: 0.0 - 1.0
    """
    score = 0

    # 新颖性 (权重 50%)
    novelty_indicators = [
        paper.get("novelty_keywords", []),  # 新方法关键词
        paper.get("new_dataset", False),    # 新数据集
        paper.get("new_benchmark", False),  # 新基准
        paper.get("new_task", False),       # 新任务定义
    ]
    novelty_count = sum(1 for ind in novelty_indicators if ind)
    score += min(novelty_count / 3, 1.0) * 0.50

    # 突破程度 (权重 50%)
    breakthrough = paper.get("breakthrough_level", "incremental")
    breakthrough_scores = {
        "paradigm_shift": 1.0,
        "significant": 0.7,
        "incremental": 0.4
    }
    score += breakthrough_scores.get(breakthrough, 0.4) * 0.50

    return min(score, 1.0)
```

### 3. PracticalityScore (实用性) - 25% 权重

衡量研究的工程可行性和应用价值。

| Metric | Description | Values |
|--------|-------------|--------|
| `engineering_readiness` | 工程就绪度 | theory / prototype / production |
| `code_available` | 代码可用性 | True / False |
| `reproducibility` | 可复现性 | 0.0 - 1.0 |

**计算公式**:
```python
def calculate_practicality_score(paper):
    """
    计算实用性分数

    Returns:
        float: 0.0 - 1.0
    """
    score = 0

    # 工程就绪度 (权重 40%)
    readiness = paper.get("engineering_readiness", "theory")
    readiness_scores = {
        "production": 1.0,
        "prototype": 0.6,
        "theory": 0.3
    }
    score += readiness_scores.get(readiness, 0.3) * 0.40

    # 代码可用性 (权重 30%)
    if paper.get("code_available", False) or paper.get("github_url"):
        score += 0.30
    else:
        score += 0.10

    # 可复现性 (权重 30%)
    reproducibility = paper.get("reproducibility", 0.5)
    # 基于是否有详细方法描述、超参数、数据集链接等
    score += reproducibility * 0.30

    return min(score, 1.0)
```

### 4. TimelinessScore (时效性) - 20% 权重

衡量研究的新近度和趋势相关性。

| Metric | Description | Values |
|--------|-------------|--------|
| `recency` | 新近度 | 0.0 - 1.0 |
| `trend_acceleration` | 趋势加速度 | accelerating / stable / declining |

**计算公式**:
```python
def calculate_timeliness_score(paper):
    """
    计算时效性分数

    Returns:
        float: 0.0 - 1.0
    """
    from datetime import datetime

    score = 0

    # 新近度 (权重 60%)
    publish_date = paper.get("publish_date")
    if publish_date:
        current_year = datetime.now().year
        paper_year = publish_date.year if hasattr(publish_date, 'year') else int(publish_date[:4])
        years_old = current_year - paper_year

        if years_old <= 1:      # 2024-2025
            score += 1.0 * 0.60
        elif years_old == 2:    # 2023
            score += 0.8 * 0.60
        elif years_old == 3:    # 2022
            score += 0.6 * 0.60
        else:                   # 更早
            score += 0.4 * 0.60
    else:
        score += 0.5 * 0.60

    # 趋势加速度 (权重 40%)
    trend = paper.get("trend_acceleration", "stable")
    trend_scores = {
        "accelerating": 1.0,
        "stable": 0.6,
        "declining": 0.3
    }
    score += trend_scores.get(trend, 0.6) * 0.40

    return min(score, 1.0)
```

---

## COMPOSITE_VALUE_SCORE / 综合评分算法

### 权重配置

```python
VALUE_WEIGHTS = {
    "impact": 0.30,
    "innovation": 0.25,
    "practicality": 0.25,
    "timeliness": 0.20
}
```

### 综合计算函数

```python
from institution_patterns import identify_institution

def calculate_value_score(paper, github_data=None, community_data=None):
    """
    计算论文的综合价值评分

    Args:
        paper: 论文数据字典
        github_data: GitHub 相关数据（可选）
        community_data: 社区讨论数据（可选）

    Returns:
        dict: {
            "value_score": float,        # 0.0 - 1.0
            "value_tier": str,           # S/A/B/C
            "dimension_scores": dict,    # 四维分数
            "institution_info": dict     # 机构信息
        }
    """
    # 1. 计算四维分数
    impact_score = calculate_impact_score(paper, github_data, community_data)
    innovation_score = calculate_innovation_score(paper)
    practicality_score = calculate_practicality_score(paper)
    timeliness_score = calculate_timeliness_score(paper)

    # 2. 加权基础分数
    base_score = (
        impact_score * VALUE_WEIGHTS["impact"] +
        innovation_score * VALUE_WEIGHTS["innovation"] +
        practicality_score * VALUE_WEIGHTS["practicality"] +
        timeliness_score * VALUE_WEIGHTS["timeliness"]
    )

    # 3. 获取机构加成
    institution_info = identify_institution(paper)
    institution_boost = institution_info.get("value_boost", 0)

    # 4. 计算最终分数（上限 1.0）
    final_score = min(1.0, base_score + institution_boost)

    # 5. 确定价值层级
    value_tier = get_value_tier(final_score)

    return {
        "value_score": round(final_score, 2),
        "value_tier": value_tier,
        "dimension_scores": {
            "impact_score": round(impact_score, 2),
            "innovation_score": round(innovation_score, 2),
            "practicality_score": round(practicality_score, 2),
            "timeliness_score": round(timeliness_score, 2)
        },
        "institution_info": institution_info
    }
```

### 价值层级 (Value Tiers)

```python
def get_value_tier(score):
    """
    根据分数确定价值层级

    Args:
        score: 0.0 - 1.0 的分数

    Returns:
        str: S / A / B / C
    """
    if score >= 0.85:
        return "S"  # 必读、未来趋势、行业风向标
    elif score >= 0.70:
        return "A"  # 高价值、推荐阅读
    elif score >= 0.50:
        return "B"  # 有价值、参考阅读
    else:
        return "C"  # 一般参考
```

### 层级描述

| Tier | Score Range | Description | Report Treatment |
|------|-------------|-------------|------------------|
| **S** | 0.85 - 1.0 | 必读、未来趋势、行业风向标 | Executive Summary 突出展示 |
| **A** | 0.70 - 0.84 | 高价值、推荐阅读 | Top Picks 列表 |
| **B** | 0.50 - 0.69 | 有价值、参考阅读 | 正文提及 |
| **C** | < 0.50 | 一般参考 | 仅在 Works Cited |

---

## TREND_INDICATORS / 趋势指标

识别新兴热点和趋势：

```python
def identify_trend_indicators(paper, all_papers, community_data=None):
    """
    识别趋势指标

    Args:
        paper: 目标论文
        all_papers: 所有论文列表（用于对比）
        community_data: 社区讨论数据

    Returns:
        list: 趋势指标列表
    """
    indicators = []

    # 1. 新兴热点: 2024-2025 新主题，引用增长 > 50%
    if is_emerging_hotspot(paper, all_papers):
        indicators.append("emerging_hotspot")

    # 2. 范式转移: 方法论根本性变化
    if paper.get("breakthrough_level") == "paradigm_shift":
        indicators.append("paradigm_shift")

    # 3. 行业采用: 大厂开始采用
    institution_info = identify_institution(paper)
    if institution_info.get("institution_type") == "big_tech":
        indicators.append("industry_adoption")

    # 4. 社区热议: 社区讨论热度高
    if community_data and community_data.get("mention_count", 0) > 30:
        indicators.append("community_hype")

    # 5. 快速传播: 引用速度 > 5/month
    citation_velocity = paper.get("citations", 0) / max(paper.get("months_since_publish", 1), 1)
    if citation_velocity > 5:
        indicators.append("viral_spread")

    return indicators
```

### 趋势指标描述

| Indicator | Description | Visual Marker |
|-----------|-------------|---------------|
| `emerging_hotspot` | 新兴热点，引用增长 > 50% | 🔥 |
| `paradigm_shift` | 方法论根本性变化 | 💡 |
| `industry_adoption` | 大厂开始采用 | 🏢 |
| `community_hype` | 社区讨论热度高 | 📢 |
| `viral_spread` | 快速传播，引用速度 > 5/month | 📈 |

---

## TOP_PICKS_GENERATION / Top Picks 生成

### 生成推荐列表

```python
def generate_top_picks(papers_with_scores):
    """
    生成 Top Picks 推荐列表

    Args:
        papers_with_scores: 包含价值评分的论文列表

    Returns:
        dict: {
            "must_read": [...],      # S 级
            "high_value": [...],     # A 级
            "emerging_trends": [...], # 有 emerging_hotspot 指标
            "foundational": [...]    # 根基论文（高被引早期工作）
        }
    """
    # 按 value_score 排序
    sorted_papers = sorted(
        papers_with_scores,
        key=lambda p: p.get("value_score", 0),
        reverse=True
    )

    top_picks = {
        "must_read": [],
        "high_value": [],
        "emerging_trends": [],
        "foundational": []
    }

    for paper in sorted_papers:
        arxiv_id = paper.get("arxiv_id")
        tier = paper.get("value_tier")
        trend_indicators = paper.get("trend_indicators", [])

        # S 级: 必读
        if tier == "S":
            top_picks["must_read"].append({
                "arxiv_id": arxiv_id,
                "title": paper.get("title"),
                "institution": paper.get("institution_backing"),
                "value_score": paper.get("value_score"),
                "reason": generate_recommendation_reason(paper)
            })

        # A 级: 高价值
        if tier == "A":
            top_picks["high_value"].append({
                "arxiv_id": arxiv_id,
                "title": paper.get("title"),
                "value_score": paper.get("value_score")
            })

        # 新兴趋势
        if "emerging_hotspot" in trend_indicators or "paradigm_shift" in trend_indicators:
            top_picks["emerging_trends"].append({
                "arxiv_id": arxiv_id,
                "title": paper.get("title"),
                "trend_type": "Hotspot" if "emerging_hotspot" in trend_indicators else "Paradigm Shift"
            })

        # 根基论文
        if paper.get("type") == "root" or paper.get("citations", 0) > 100:
            top_picks["foundational"].append({
                "arxiv_id": arxiv_id,
                "title": paper.get("title"),
                "citations": paper.get("citations")
            })

    return top_picks

def generate_recommendation_reason(paper):
    """
    生成推荐理由
    """
    reasons = []

    if paper.get("institution_backing"):
        reasons.append(f"机构: {paper.get('institution_backing')}")

    trend_indicators = paper.get("trend_indicators", [])
    if "industry_adoption" in trend_indicators:
        reasons.append("大厂采用")
    if "emerging_hotspot" in trend_indicators:
        reasons.append("新兴热点")
    if "paradigm_shift" in trend_indicators:
        reasons.append("范式转移")

    return " | ".join(reasons) if reasons else "高综合评分"
```

---

## EMERGING_HOTSPOT_DETECTION / 新兴热点检测

```python
def is_emerging_hotspot(paper, all_papers):
    """
    检测是否为新兴热点

    条件:
    1. 发表时间在 2024-2025
    2. 主题相关论文数量在增长
    3. 引用增长 > 50%（相对同类论文）
    """
    from datetime import datetime

    # 条件 1: 新近度
    publish_year = paper.get("year", 2020)
    if publish_year < 2024:
        return False

    # 条件 2: 同类论文数量
    paper_topic = paper.get("primary_topic", "")
    similar_papers = [p for p in all_papers if paper_topic in p.get("topics", [])]
    if len(similar_papers) < 3:
        return False

    # 条件 3: 引用增长
    avg_citations = sum(p.get("citations", 0) for p in similar_papers) / len(similar_papers)
    paper_citations = paper.get("citations", 0)

    growth_rate = (paper_citations - avg_citations) / max(avg_citations, 1)

    return growth_rate > 0.5  # 50% 以上增长
```

---

## VALUE_RANKING_OUTPUT / 价值排名输出格式

### JSON Schema

```json
{
  "value_assessment": {
    "paper_value_scores": [
      {
        "arxiv_id": "2601.23265",
        "title": "PaperBanana",
        "value_score": 0.92,
        "value_tier": "S",
        "institution_backing": "Google",
        "institution_boost": 0.30,
        "dimension_scores": {
          "impact_score": 0.85,
          "innovation_score": 0.90,
          "practicality_score": 0.88,
          "timeliness_score": 0.95
        },
        "trend_indicators": ["emerging_hotspot", "industry_adoption"]
      }
    ],
    "value_ranking": [
      {"rank": 1, "arxiv_id": "2601.23265", "tier": "S"},
      {"rank": 2, "arxiv_id": "2602.03828", "tier": "A"}
    ],
    "top_picks": {
      "must_read": [
        {
          "arxiv_id": "2601.23265",
          "title": "PaperBanana",
          "institution": "Google",
          "value_score": 0.92,
          "reason": "机构: Google | 大厂采用 | 新兴热点"
        }
      ],
      "high_value": [
        {"arxiv_id": "2602.03828", "title": "AutoFigure", "value_score": 0.78}
      ],
      "emerging_trends": [
        {"arxiv_id": "2601.23265", "title": "PaperBanana", "trend_type": "Hotspot"}
      ],
      "foundational": [
        {"arxiv_id": "2302.05543", "title": "Foundation Paper", "citations": 250}
      ]
    },
    "institution_distribution": {
      "big_tech": ["Google", "Microsoft"],
      "top_universities": ["MIT", "Stanford"],
      "star_authors": ["Author Name (H-index: 85)"]
    },
    "emerging_hotspots": [
      {
        "topic": "AI-generated scientific illustrations",
        "paper_count": 4,
        "growth_rate": "150%",
        "key_papers": ["2601.23265", "2602.03828"],
        "industry_backing": ["Google"]
      }
    ]
  }
}
```

---

## INTEGRATION_WITH_LOGIC_ANALYSIS / 与逻辑分析的集成

价值评估结果应集成到 `logic_analysis.json` 的 `value_assessment` 字段中：

```python
def integrate_value_assessment(logic_analysis, papers_with_value_scores):
    """
    将价值评估结果集成到逻辑分析 JSON
    """
    logic_analysis["value_assessment"] = {
        "paper_value_scores": papers_with_value_scores,
        "value_ranking": generate_value_ranking(papers_with_value_scores),
        "top_picks": generate_top_picks(papers_with_value_scores),
        "institution_distribution": analyze_institution_distribution(papers_with_value_scores),
        "emerging_hotspots": detect_emerging_hotspots(papers_with_value_scores)
    }
    return logic_analysis
```

---

## CHANGELOG

### v1.0 (2026-02-19)
- Initial release
- Four-dimensional value assessment (Impact, Innovation, Practicality, Timeliness)
- S/A/B/C tier classification
- Top Picks generation
- Trend indicators
- Emerging hotspot detection
