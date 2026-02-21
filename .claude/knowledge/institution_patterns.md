# Institution Recognition Patterns / 机构识别模式

> **Purpose**: Define patterns for identifying high-value research backed by major institutions.
> **Usage**: Reference this file via `@knowledge:institution_patterns.md`
> **Version**: 2.6 (2026-02-19)

---

## Overview / 概述

机构背书是研究价值的重要信号。本文档定义了识别大厂、顶尖高校、明星作者的模式，用于提升价值评估的准确性。

**核心原则**:
- 大厂研究通常代表：工程资源充足、产品化潜力高、行业趋势指引
- 顶尖高校研究通常代表：理论深度、学术影响力、前沿探索
- 明星作者通常代表：领域权威、持续产出、引用保障

---

## BIG_TECH_PATTERNS / 大厂识别模式

大厂研究的高价值信号：

| Company | Patterns (匹配模式) | Value Boost | Notes |
|---------|---------------------|-------------|-------|
| **Google** | "Google", "Google Research", "Google DeepMind", "Alphabet", "Google AI" | +0.30 | 包含 DeepMind |
| **OpenAI** | "OpenAI" | +0.35 | 行业风向标 |
| **Microsoft** | "Microsoft Research", "Microsoft", "MSR" | +0.25 | 学术+工程双强 |
| **Meta** | "Meta AI", "Facebook AI Research", "FAIR", "Meta" | +0.25 | 开源贡献大 |
| **Anthropic** | "Anthropic" | +0.30 | AI 安全前沿 |
| **Apple** | "Apple ML Research", "Apple", "Apple AI" | +0.20 | 隐私+端侧 |
| **NVIDIA** | "NVIDIA", "NVIDIA Research" | +0.20 | 硬件+软件协同 |
| **Amazon** | "Amazon", "AWS AI", "Amazon Research" | +0.18 | 工程规模优势 |

### 大厂识别实现

```python
def identify_big_tech(authors, affiliations):
    """
    识别大厂背书

    Args:
        authors: 作者名字符串列表
        affiliations: 机构/单位字符串列表

    Returns:
        tuple: (company_name, value_boost) 或 (None, 0)
    """
    BIG_TECH_PATTERNS = {
        "Google": (["google", "deepmind", "alphabet"], 0.30),
        "OpenAI": (["openai"], 0.35),
        "Microsoft": (["microsoft", "msr "], 0.25),
        "Meta": (["meta ai", "facebook ai", "fair", "meta"], 0.25),
        "Anthropic": (["anthropic"], 0.30),
        "Apple": (["apple"], 0.20),
        "NVIDIA": (["nvidia"], 0.20),
        "Amazon": (["amazon", "aws ai"], 0.18),
    }

    combined_text = " ".join(str(a).lower() for a in authors + affiliations)

    for company, (patterns, boost) in BIG_TECH_PATTERNS.items():
        for pattern in patterns:
            if pattern in combined_text:
                return company, boost

    return None, 0
```

---

## TOP_UNIVERSITIES / 顶尖高校识别模式

高校研究代表学术深度和理论前沿：

| Tier | Universities | Value Boost | Criteria |
|------|-------------|-------------|----------|
| **S** | MIT, Stanford, CMU, UC Berkeley, Caltech | +0.25 | CS Ranking Top 5 |
| **A** | Tsinghua, Peking, Oxford, Cambridge, ETH Zurich, UW, GA Tech | +0.20 | CS Ranking Top 20 |
| **B** | Top 50 CS programs (UIUC, Cornell, Columbia, etc.) | +0.15 | CS Ranking Top 50 |

### 顶尖高校识别实现

```python
def identify_top_university(affiliations):
    """
    识别顶尖高校背书

    Args:
        affiliations: 机构/单位字符串列表

    Returns:
        tuple: (university_name, value_boost) 或 (None, 0)
    """
    TOP_UNIVERSITIES = {
        # Tier S: CS Ranking Top 5
        "S": (["mit", "massachusetts institute of technology",
               "stanford", "stanford university",
               "cmu", "carnegie mellon",
               "uc berkeley", "university of california berkeley",
               "caltech", "california institute of technology"], 0.25),
        # Tier A: CS Ranking Top 20
        "A": (["tsinghua", "peking university", "pku",
               "oxford", "university of oxford",
               "cambridge", "university of cambridge",
               "eth zurich", "swiss federal institute",
               "university of washington", "uw ",
               "georgia tech", "georgia institute"], 0.20),
        # Tier B: CS Ranking Top 50
        "B": (["uiuc", "illinois",
               "cornell", "columbia",
               "princeton", "yale",
               "ucla", "ucsd", "ucla",
               "toronto", "ubc"], 0.15),
    }

    combined_text = " ".join(str(a).lower() for a in affiliations)

    for tier, (patterns, boost) in TOP_UNIVERSITIES.items():
        for pattern in patterns:
            if pattern in combined_text:
                # 返回匹配的大学名称（简化版）
                return pattern.title(), boost

    return None, 0
```

---

## STAR_AUTHORS / 明星作者识别模式

基于引用数和领域影响力的作者识别：

| Criteria | Value Boost | Description |
|----------|-------------|-------------|
| H-index > 100 | +0.20 | 领域领军人物 |
| H-index 50-100 | +0.15 | 资深研究者 |
| Key paper first author | +0.15 | 重要论文第一作者 |
| NeurIPS/ICML/ICLR best paper | +0.20 | 顶级会议最佳论文 |
| Highly Cited Researcher | +0.15 | Clarivate 高被引 |

### 明星作者识别实现

```python
def identify_star_author(author_name, h_index=None, paper_role=None, awards=None):
    """
    识别明星作者

    Args:
        author_name: 作者姓名
        h_index: H-index 值（如已知）
        paper_role: 在论文中的角色（"first_author", "corresponding", "contributing"）
        awards: 奖项列表

    Returns:
        tuple: (reason, value_boost) 或 (None, 0)
    """
    boost = 0
    reasons = []

    # H-index 加成
    if h_index:
        if h_index > 100:
            boost += 0.20
            reasons.append(f"H-index > 100 ({h_index})")
        elif h_index > 50:
            boost += 0.15
            reasons.append(f"H-index 50-100 ({h_index})")

    # 论文角色加成
    if paper_role == "first_author":
        boost += 0.10
        reasons.append("First author")

    # 奖项加成
    if awards:
        top_conference_best = ["neurips best", "icml best", "iclr best", "cvpr best", "acl best"]
        for award in awards:
            award_lower = award.lower()
            if any(bc in award_lower for bc in top_conference_best):
                boost += 0.20
                reasons.append(f"Award: {award}")
            elif "highly cited" in award_lower:
                boost += 0.15
                reasons.append("Highly Cited Researcher")

    if boost > 0:
        return "; ".join(reasons), min(boost, 0.35)  # 上限 0.35
    return None, 0
```

---

## EMERGING_INSTITUTIONS / 新兴研究机构

值得关注的新兴 AI 研究机构：

| Institution | Value Boost | Notes |
|------------|-------------|-------|
| **xAI** | +0.20 | Elon Musk 的 AI 公司 |
| **Mistral AI** | +0.18 | 欧洲开源 AI |
| **Cohere** | +0.15 | 企业级 LLM |
| **Inflection AI** | +0.15 | PI 聊天机器人 |
| **Databricks** | +0.12 | ML 平台 |
| **Hugging Face** | +0.15 | 开源 AI 社区 |
| **Scale AI** | +0.10 | 数据标注 |

---

## IMPLEMENTATION GUIDE / 实施指南

### 完整机构识别函数

```python
def identify_institution(paper, institution_patterns=None):
    """
    综合识别机构背书

    Args:
        paper: 论文数据字典，包含 authors, affiliations 等字段
        institution_patterns: 可选的自定义模式

    Returns:
        dict: {
            "institution": str or None,  # 主要机构名称
            "institution_type": str,      # "big_tech", "top_university", "star_author", "emerging", None
            "value_boost": float,         # 价值加成
            "boost_reason": str           # 加成原因
        }
    """
    authors = paper.get("authors", [])
    affiliations = paper.get("affiliations", [])
    h_indices = paper.get("author_h_indices", [])

    # 1. 优先检查大厂
    big_tech, big_tech_boost = identify_big_tech(authors, affiliations)
    if big_tech:
        return {
            "institution": big_tech,
            "institution_type": "big_tech",
            "value_boost": big_tech_boost,
            "boost_reason": f"Big Tech: {big_tech}"
        }

    # 2. 检查顶尖高校
    university, uni_boost = identify_top_university(affiliations)
    if university:
        return {
            "institution": university,
            "institution_type": "top_university",
            "value_boost": uni_boost,
            "boost_reason": f"Top University: {university}"
        }

    # 3. 检查明星作者（如果有 H-index 信息）
    if h_indices:
        max_h_index = max(h_indices) if h_indices else 0
        if max_h_index > 50:
            reason, author_boost = identify_star_author(
                authors[0] if authors else "",
                h_index=max_h_index
            )
            if author_boost > 0:
                return {
                    "institution": None,
                    "institution_type": "star_author",
                    "value_boost": author_boost,
                    "boost_reason": reason
                }

    # 4. 默认：无特殊机构背书
    return {
        "institution": None,
        "institution_type": None,
        "value_boost": 0,
        "boost_reason": "No special institutional backing identified"
    }
```

---

## USAGE IN VALUE ASSESSMENT / 在价值评估中的使用

在 `@knowledge:value_assessment.md` 中的 `calculate_value_score()` 函数中使用：

```python
# 在价值评估时调用
institution_info = identify_institution(paper)
institution_boost = institution_info.get("value_boost", 0)

# 将 institution_boost 加到综合评分中
final_score = min(1.0, base_score + institution_boost)
```

---

## VALIDATION EXAMPLES / 验证示例

### 示例 1: PaperBanana (Google)

```python
paper = {
    "title": "PaperBanana",
    "authors": ["Dawei Zhu", "Tomas Pfister"],
    "affiliations": ["Google", "Google Research"]
}

result = identify_institution(paper)
# 返回:
# {
#     "institution": "Google",
#     "institution_type": "big_tech",
#     "value_boost": 0.30,
#     "boost_reason": "Big Tech: Google"
# }
```

### 示例 2: MIT 研究

```python
paper = {
    "title": "Some MIT Paper",
    "authors": ["John Doe"],
    "affiliations": ["MIT", "Massachusetts Institute of Technology"]
}

result = identify_institution(paper)
# 返回:
# {
#     "institution": "MIT",
#     "institution_type": "top_university",
#     "value_boost": 0.25,
#     "boost_reason": "Top University: MIT"
# }
```

---

## CHANGELOG

### v1.0 (2026-02-19)
- Initial release
- Big Tech patterns: 8 companies
- Top Universities: 3 tiers
- Star Authors: H-index based
- Emerging Institutions: 7 companies
