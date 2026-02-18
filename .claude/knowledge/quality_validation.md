# Quality Validation / 质量验证

> **Purpose**: Validation functions and quality checks for literature review reports.
> **Usage**: Reference this file via `@knowledge:quality_validation.md`

---

## Enhanced Quality Validation

```python
def validate_enhanced_quality(review_content, logic_analysis):
    """增强质量验证 (v2.1 更新)"""

    checks = {
        # 基础质量
        "uses_logic_analysis": check_logic_analysis_usage(review_content, logic_analysis),
        "not_mechanical": check_narrative_flow(review_content),
        "word_count": check_word_count(review_content, 3000, 5000),
        "citations_complete": check_citations_complete(review_content),

        # 逻辑流畅性
        "logical_connectors": check_logical_connectors(review_content),
        "evolution_narrative": check_evolution_narrative(review_content),
        "inheritance_citation": check_inheritance_citation(review_content),
        "synthesis_sentences": check_synthesis_sentences(review_content),

        # 结构质量
        "hourglass_structure": check_hourglass_structure(review_content),
        "introduction_conclusion_match": check_introduction_conclusion_match(review_content),
        "thematic_organization": check_thematic_organization(review_content),

        # 反模式检测
        "no_mechanical_listing": check_no_mechanical_listing(review_content),
        "no_annotated_bibliography": check_no_annotated_bibliography_style(review_content),
        "no_chronological_only": check_no_chronological_only(review_content),

        # 双语一致性
        "bilingual_consistency": check_bilingual_consistency(review_content),

        # 引用关系
        "citation_relationships": check_citation_relationships(review_content),

        # v2.1 NEW: 模板和路标检查
        "uses_paragraph_templates": check_uses_paragraph_templates(review_content, logic_analysis),
        "has_signposting": check_has_signposting(review_content, logic_analysis),
        "synthesis_opportunities_used": check_synthesis_opportunities_used(review_content, logic_analysis),
        "three_phase_verified": check_three_phase_verified(logic_analysis)
    }

    return all(checks.values()), checks
```

---

## Template & Signposting Checks (v2.1)

```python
# v2.1 NEW: 检查是否使用了段落模板
def check_uses_paragraph_templates(content, logic_analysis):
    """检查是否使用了段落模板"""
    writing_guidance = logic_analysis.get("writing_guidance", {})
    templates = writing_guidance.get("paragraph_templates", {})

    # 检查内容中是否包含模板的特征
    template_indicators = []
    for template_name, template_data in templates.items():
        example = template_data.get("example", "")
        if example:
            # 提取示例中的关键词
            keywords = ["demonstrated", "disagree", "evolved"]
            template_indicators.extend(keywords)

    return any(keyword.lower() in content.lower() for keyword in template_indicators)


# v2.1 NEW: 检查是否有路标
def check_has_signposting(content, logic_analysis):
    """检查是否有路标短语"""
    writing_guidance = logic_analysis.get("writing_guidance", {})
    signposting = writing_guidance.get("signposting_phrases", {})

    all_phrases = (
        signposting.get("section_opening", []) +
        signposting.get("section_transition", []) +
        signposting.get("synthesis_markers", [])
    )

    # 检查是否有至少2个路标短语
    found_count = sum(1 for phrase in all_phrases if phrase.lower() in content.lower())
    return found_count >= 2


# v2.1 NEW: 检查综合机会是否被使用
def check_synthesis_opportunities_used(content, logic_analysis):
    """检查综合机会是否被使用"""
    synthesis_opps = logic_analysis.get("synthesis_opportunities", [])

    for opp in synthesis_opps:
        papers = opp.get("papers", [])
        # 检查是否在同一句或同一段中引用了多篇文章
        for paper_id in papers[:2]:  # 至少检查前2篇
            if paper_id in content:
                # 检查附近是否有其他论文ID
                paper_index = content.find(paper_id)
                nearby_content = content[max(0, paper_index-200):paper_index+200]
                other_papers = [p for p in papers if p != paper_id]
                if any(other in nearby_content for other in other_papers):
                    return True
    return len(synthesis_opps) == 0  # 如果没有综合机会要求，返回True


# v2.1 NEW: 检查三阶段验证是否通过
def check_three_phase_verified(logic_analysis):
    """检查三阶段写作验证是否完成"""
    # 这个检查实际上在 verify_post_writing 中完成
    # 这里只检查 logic_analysis 是否有必需的字段
    required_fields = ["writing_guidance", "synthesis_opportunities", "anti_pattern_guidance"]
    return all(field in logic_analysis for field in required_fields)
```

---

## Synthesis Sentence Checks

```python
def check_synthesis_sentences(content):
    """检查综合句（每段结尾）"""
    # 检测总结性语句模式
    synthesis_patterns = [
        r"综上所述",
        r"这些工作.*?共同",
        r"从上述分析",
        r"总体而言",
        r"可以看出.*?趋势"
    ]
    return sum(len(re.findall(pattern, content)) for pattern in synthesis_patterns) >= 3
```

---

## Structure Checks

```python
def check_hourglass_structure(content):
    """检查漏斗结构"""
    # 检查是否有广泛引入 -> 具体分析 -> 广泛综合的结构
    has_broad_intro = bool(re.search(r"(背景|领域|研究问题)", content[:1000]))
    has_specific_analysis = bool(re.search(r"(具体|详细|深入|方法)", content[1000:-1000]))
    has_broad_synthesis = bool(re.search(r"(综合|总结|未来方向|影响)", content[-1000:]))
    return has_broad_intro and has_specific_analysis and has_broad_synthesis


def check_introduction_conclusion_match(content):
    """检查引言和结论的呼应"""
    # 提取引言中的承诺和结论中的总结
    intro = re.search(r"# 1\. Introduction.*?(?=#\s[2-6]|\Z)", content, re.DOTALL)
    conclusion = re.search(r"# 6\. Conclusion.*?(?=\Z)", content, re.DOTALL)

    if not intro or not conclusion:
        return False

    # 检查是否有呼应的关键词
    intro_keywords = set(re.findall(r'(研究|分析|发现|演进)', intro.group()))
    conclusion_keywords = set(re.findall(r'(研究|分析|发现|演进)', conclusion.group()))

    return len(intro_keywords & conclusion_keywords) >= 2


def check_thematic_organization(content):
    """检查主题组织（而非论文组织）"""
    # 检查是否有主题标题
    thematic_headers = re.findall(r'## 3\. Thematic Analysis.*?### (.*?)\n', content)

    # 检查主题描述是否综合多篇论文
    if thematic_headers:
        # 随机检查一个主题段落
        for theme in thematic_headers:
            theme_section = re.search(rf'### {theme}.*?(?=###|\Z)', content, re.DOTALL)
            if theme_section:
                # 统计引用数量
                citations = len(re.findall(r'\[.*?\]', theme_section.group()))
                if citations >= 2:  # 至少引用2篇论文
                    return True

    return False
```

---

## Anti-Pattern Detection Functions

```python
def check_no_mechanical_listing(content):
    """检查无机械罗列"""
    mechanical_patterns = [
        r'[Pp]aper.*?提出.*?\.\s*[Pp]aper.*?提出',
        r'[Aa]uthor.*?提出.*?\.\s*[Aa]uthor.*?提出',
        r'[A-Z]\..*?\.\s*[A-Z]\..*?\.\s*[A-Z]\.'
    ]
    return not any(re.search(pattern, content) for pattern in mechanical_patterns)


def check_no_annotated_bibliography_style(content):
    """检查无注释书目风格"""
    # 检查是否按论文组织章节
    bad_headers = re.findall(r'###\s+(?:Paper|作者?|研究\s?\d+)', content)
    return len(bad_headers) == 0


def check_no_chronological_only(content):
    """检查非纯时间组织"""
    # 纯时间组织的特征：连续的年份引用
    year_pattern = r'(?:19|20)\d{2}年'
    year_mentions = re.findall(year_pattern, content)

    # 如果有5个以上连续的年份提及，可能是纯时间组织
    consecutive_years = 0
    for i in range(len(year_mentions) - 1):
        if int(year_mentions[i][:4]) + 1 == int(year_mentions[i + 1][:4]):
            consecutive_years += 1

    return consecutive_years < 3  # 允许少量连续年份，但不应该占主导
```

---

## Bilingual & Citation Checks

```python
def check_bilingual_consistency(content):
    """检查双语一致性"""
    # 检查中英文标题格式是否一致
    headers = re.findall(r'^(#{1,3})\s+(.*?)/\s*(.*?)$', content, re.MULTILINE)

    for header in headers:
        level, chinese, english = header
        # 检查是否有双语标题
        if not english or not chinese:
            continue

        # 检查格式一致性
        if chinese.count('(') != english.count('('):
            return False

    return True


def check_citation_relationships(content):
    """检查引用关系描述"""
    relationship_patterns = [
        r'基于.*?工作',
        r'扩展了',
        r'改进了',
        r'不同于',
        r'被.*?采用',
        r'引发了',
        r'推动'
    ]
    return sum(content.count(pattern) for pattern in relationship_patterns) >= 5
```

---

## Logical Flow Validation

```python
def validate_logical_flow(review_content):
    """验证逻辑流畅性（增强版）"""

    checks = {
        # 演进叙事
        "has_evolution_narrative": check_evolution_narrative(review_content),
        "has_inheritance_citation": check_inheritance_citation(review_content),
        "has_paradigm_shift_description": check_paradigm_shift_description(review_content),

        # 逻辑连接
        "has_logical_connectors": check_logical_connectors(review_content),
        "has_transition_sentences": check_transition_sentences(review_content),

        # 非机械性
        "not_mechanical_listing": check_not_mechanical(review_content),
        "has_synthesis": check_synthesis(review_content),

        # 逻辑分析使用
        "uses_logic_analysis": check_logic_analysis_usage(review_content),

        # 元评论
        "has_metacomment": check_metacomment(review_content)
    }

    return all(checks.values()), checks


def check_evolution_narrative(content):
    """检查演进叙事"""
    evolution_keywords = ["演进", "发展", "从...到...", "推动", "导致",
                          "催生了", "促进了", "沿此方向", "进一步发展"]
    count = sum(content.count(kw) for kw in evolution_keywords)
    return count >= 3  # 至少3个演进相关词汇


def check_inheritance_citation(content):
    """检查继承关系引用"""
    inheritance_patterns = [
        r"基于.*?工作",
        r"扩展了",
        r"改进了",
        r"沿用了",
        r"继承自",
        r"发展自",
        r"在.*?基础上"
    ]
    return any(re.search(pattern, content) for pattern in inheritance_patterns)


def check_paradigm_shift_description(content):
    """检查范式转移描述"""
    paradigm_keywords = ["范式", "转移", "转变", "从.*?到.*?的演进",
                         "根本性", "突破", "革命性"]
    return sum(content.count(kw) for kw in paradigm_keywords) >= 1


def check_logical_connectors(content):
    """检查逻辑连接词（多样化）"""
    connector_categories = {
        "演进": ["然而", "但是", "为解决这一问题"],
        "继承": ["基于", "扩展了", "改进了"],
        "对比": ["相比之下", "与.*?不同", "另一方面"],
        "因果": ["因此", "导致", "促使"],
        "综合": ["综上所述", "总体而言", "可以看出"]
    }

    used_categories = set()
    for category, connectors in connector_categories.items():
        if any(re.search(conn, content) for conn in connectors):
            used_categories.add(category)

    return len(used_categories) >= 3  # 至少使用3类连接词


def check_transition_sentences(content):
    """检查过渡句"""
    transition_patterns = [
        r"接下来的分析",
        r"下文将",
        r"接下来",
        r"首先.*?其次.*?最后",
        r"一方面.*?另一方面"
    ]
    return any(re.search(pattern, content) for pattern in transition_patterns)


def check_not_mechanical(content):
    """检查非机械罗列"""
    mechanical_patterns = [
        r"[Pp]aper.*?提出.*?\.\s*[Pp]aper.*?提出",
        r"[Aa]uthor.*?提出.*?\.\s*[Aa]uthor.*?提出",
        r"[A-Z]\..*?\.\s*[A-Z]\..*?\.\s*[A-Z]\."
    ]
    return not any(re.search(pattern, content) for pattern in mechanical_patterns)


def check_synthesis(content):
    """检查综合句"""
    synthesis_patterns = [
        r"综上所述",
        r"这些工作.*?共同",
        r"从上述分析.*?可以",
        r"总体而言",
        r"现有研究.*?趋势"
    ]
    return sum(len(re.findall(pattern, content)) for pattern in synthesis_patterns) >= 2


def check_logic_analysis_usage(content):
    """检查逻辑分析结果使用"""
    # 检查是否引用了逻辑分析的关键发现
    logic_indicators = [
        "根基论文", "继承链条", "核心主题", "演进时间线",
        "范式转移", "研究空白", "方法论家族", "演进路径"
    ]
    return any(indicator in content for indicator in logic_indicators)


def check_metacomment(content):
    """检查元评论"""
    metacomment_patterns = [
        r"值得注意的是",
        r"本节.*?分析",
        r"本文选择",
        r"接下来的分析",
        r"上述分析.*?表明"
    ]
    return any(re.search(pattern, content) for pattern in metacomment_patterns)
```

---

## Synthesis Quality Metrics

```python
def evaluate_synthesis_quality(review_content):
    """评估综合质量"""

    metrics = {
        "cross_paper_synthesis": evaluate_cross_paper_synthesis(review_content),
        "thematic_coherence": evaluate_thematic_coherence(review_content),
        "gap_justification": evaluate_gap_justification(review_content),
        "comparative_depth": evaluate_comparative_depth(review_content)
    }

    return metrics


def evaluate_cross_paper_synthesis(content):
    """评估跨论文综合质量"""
    # 检查是否将多篇论文综合描述
    multi_paper_sentences = re.findall(r'[^。]*?\[.*?\].*?\[.*?\][^。]*？。', content)

    if len(multi_paper_sentences) < 3:
        return {"score": "low", "reason": "跨论文综合句少于3句"}

    # 检查综合句的质量
    quality_indicators = ["共同", "都", "分别", "不同", "一致", "分歧"]
    has_quality = any(ind in content for ind in quality_indicators)

    return {
        "score": "high" if has_quality else "medium",
        "count": len(multi_paper_sentences)
    }


def evaluate_thematic_coherence(content):
    """评估主题连贯性"""
    # 检查主题是否清晰
    themes = re.findall(r'###\s+([^#\n]+)', content)

    if len(themes) < 2:
        return {"score": "low", "reason": "主题少于2个"}

    # 检查主题间是否有过渡
    transitions = 0
    for i in range(len(themes) - 1):
        # 检查两个主题之间是否有过渡句
        theme_text = content.split(themes[i])[1].split(themes[i + 1])[0] if themes[i + 1] in content else ""
        if any(word in theme_text for word in ["接下来", "下面", "此外", "进一步"]):
            transitions += 1

    return {
        "score": "high" if transitions >= len(themes) - 1 else "medium",
        "themes": len(themes),
        "transitions": transitions
    }


def evaluate_gap_justification(content):
    """评估研究空白论证质量"""
    # 检查研究空白是否有证据支撑
    gap_sections = re.findall(r'空白.*?：.*?(?=空白|$)', content, re.DOTALL)

    justified_gaps = 0
    for gap in gap_sections:
        # 检查是否有证据支撑
        if any(word in gap for word in ["指出", "缺少", "未", "缺乏", "忽视"]):
            # 检查是否有原因分析
            if any(word in gap for word in ["可能源于", "由于", "因为", "原因"]):
                justified_gaps += 1

    return {
        "score": "high" if justified_gaps == len(gap_sections) else "medium",
        "justified": justified_gaps,
        "total": len(gap_sections)
    }


def evaluate_comparative_depth(content):
    """评估比较分析深度"""
    # 检查是否有比较分析章节
    comparison_section = re.search(r'##\s+.*?比较.*?$(.*?)(?=##|$)', content, re.DOTALL)

    if not comparison_section:
        return {"score": "low", "reason": "无比较分析章节"}

    section_text = comparison_section.group(1)

    # 检查比较的深度
    depth_indicators = {
        "方法对比": ["采用.*?而", "与.*?不同", "相比之下"],
        "优劣势分析": ["优势", "劣势", "优点", "缺点"],
        "权衡分析": ["权衡", "平衡", "取舍"]
    }

    found_depths = []
    for depth, indicators in depth_indicators.items():
        if any(re.search(ind, section_text) for ind in indicators):
            found_depths.append(depth)

    return {
        "score": "high" if len(found_depths) == 3 else "medium",
        "aspects": found_depths
    }
```

---

## Related Knowledge Files / 相关知识文件

- `@knowledge:literature_review_template.md` - 报告结构模板
- `@knowledge:writing_principles.md` - 写作原则和叙事弧
- `@knowledge:anti_patterns.md` - 反模式检测与预防
