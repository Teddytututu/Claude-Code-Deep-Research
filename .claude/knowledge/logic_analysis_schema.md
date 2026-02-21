# Logic Analysis Schema / 逻辑分析 Schema

> **Purpose**: Complete JSON schema and examples for literature-analyzer output.
> **Usage**: Reference this file via `@knowledge:logic_analysis_schema.md`
> **Depends on**: `@knowledge:value_assessment.md`, `@knowledge:institution_patterns.md`
> **Version**: 2.6 (2026-02-19)

---

## OUTPUT FORMAT: Structured Logic Analysis JSON v2.6

### Complete JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Literature Logic Analysis v2.6",
  "description": "Enhanced logic analysis with PRISMA 2020 compliance, quality assessment, value assessment (v2.6), synthesis opportunities, writing guidance, and cross-domain analysis",

  "research_metadata": {
    "agent_type": "literature-analyzer",
    "version": "2.3",
    "timestamp": "ISO 8601",
    "papers_analyzed": 7,
    "themes_identified": 4,
    "gaps_identified": 3,
    "quality_framework": "PRISMA 2020 + AMSTAR 2 + ROBIS",
    "validation_status": "passed"
  },

  "quality_assessment": {
    "framework_used": "AMSTAR_2_plus_ROBIS",
    "overall_quality_score": 0.78,
    "paper_quality_scores": [
      {
        "arxiv_id": "2307.16789",
        "quality_score": 0.85,
        "confidence_level": "high",
        "bias_risk": "low",
        "amstar2_domains": {
          "protocol_registered": true,
          "literature_search_comprehensive": true,
          "justified_exclusion": true,
          "risk_of_bias_assessed": false,
          "appropriate_meta_analysis": false
        },
        "robis_domains": {
          "study_eligibility": "low",
          "study_selection": "low",
          "data_collection": "low"
        }
      }
    ],
    "quality_distribution": {
      "high_quality": 3,
      "medium_quality": 3,
      "low_quality": 1
    }
  },

  "prisma_2020_compliance": {
    "identification": {
      "total_records_identified": 7,
      "duplicates_removed": 0,
      "records_screened": 7,
      "records_excluded": 0
    },
    "eligibility": {
      "full_text_assessed": 7,
      "inclusion_criteria": [
        "Peer-reviewed academic papers",
        "Relevant to research topic",
        "Published in last 5 years"
      ],
      "exclusion_records": []
    },
    "included": {
      "qualitative_synthesis": 7,
      "quantitative_synthesis": 0
    },
    "flow_diagram": "Generated automatically"
  },

  "citation_network": {
    "root_papers": [
      {
        "arxiv_id": "2307.16789",
        "title": "AgentBench: Evaluating AI Agents",
        "citation_count": 150,
        "is_root": true,
        "contribution": "建立多环境评估框架",
        "confidence_level": "high",
        "validation_status": "verified"
      }
    ],
    "inheritance_chains": [
      {
        "chain_id": "chain_001",
        "root": "2307.16789",
        "root_title": "AgentBench",
        "citing_papers": ["2404.03807", "2504.14773"],
        "citing_titles": ["AgentBoard", "PLANET"],
        "inheritance_type": "direct",
        "confidence": 0.92,
        "temporal_validated": true,
        "evolution_path": "多环境评估 → 多维度分析平台",
        "contribution_evolution": "从单一成功指标到细粒度进度追踪",
        "validation_notes": "引用时间顺序正确，继承关系明确"
      }
    ],
    "network_metrics": {
      "nodes": 7,
      "edges": 12,
      "density": 0.48,
      "avg_clustering": 0.62,
      "longest_path": 3
    },
    "citation_graph": "Detailed adjacency matrix or edge list"
  },

  "thematic_analysis": {
    "core_themes": [
      {
        "theme_id": "theme_001",
        "theme_name": "evaluation_metrics",
        "definition": "评估指标设计",
        "papers": ["2307.16789", "2404.03807", "2504.14773"],
        "paper_count": 3,
        "quality_score": 0.88,
        "evolution": "从二分类成功率 → 细粒度进度追踪 → 多维度综合评估",
        "consensus": "多维度评估优于单一指标",
        "consensus_strength": "strong",
        "controversies": [],
        "synthesis": "虽然所有论文都认同多维度评估的重要性，但在具体指标设计上存在不同路径。",
        "key_papers": [
          {
            "arxiv_id": "2307.16789",
            "contribution": "提出二分类成功指标",
            "evidence_strength": "high"
          }
        ]
      }
    ],
    "methodological_families": [
      {
        "family_id": "fam_001",
        "family_name": "simulation_based",
        "papers": ["2307.16789", "2401.02009"],
        "common_approach": "使用模拟环境评估 agent 能力",
        "approach_quality": 0.75,
        "distinct_features": [],
        "advantages": ["可控性强", "可重复", "成本低"],
        "limitations": ["与真实场景存在差距"],
        "validation_status": "empirically_supported"
      }
    ],
    "cross_domain_synthesis": [],
    "cross_cutting_concerns": []
  },

  "evolution_analysis": {
    "timeline": [
      {
        "period": "2023 Q3",
        "papers": ["2307.16789", "2307.13854"],
        "breakthrough": "建立基础评估框架",
        "key_development": "AgentBench 和 ToolBench 同时提出",
        "impact": "为后续研究奠定基础",
        "impact_level": "foundational",
        "temporal_validated": true
      }
    ],
    "paradigm_shifts": [
      {
        "shift_id": "shift_001",
        "shift_name": "从单一指标到多维评估",
        "from": "二分类成功/失败",
        "to": "多维度评估（成功+进度+成本）",
        "triggering_papers": ["2404.03807"],
        "rationale": "单一指标无法反映 agent 能力的细微差异",
        "evidence": "AgentBoard 引入 progress_rate 和 cost_efficiency",
        "evidence_strength": "strong",
        "impact": "提高了评估的区分度",
        "confidence_level": "high"
      }
    ],
    "evolution_drivers": [
      {
        "driver": "模型能力提升",
        "description": "随着 LLM 能力提升，需要更精细的评估指标",
        "affected_areas": ["evaluation_metrics", "task_complexity"],
        "evidence_support": "high"
      }
    ],
    "temporal_evolution": {
      "publication_trend": "increasing",
      "citation_velocity": "accelerating",
      "knowledge_accumulation": "exponential"
    }
  },

  "comparative_analysis": {
    "methodology_comparison": [
      {
        "dimension": "data_collection",
        "approaches": [
          {
            "paper": "2307.16789",
            "method": "人工标注+真实API",
            "pros": ["真实性高", "质量可控"],
            "cons": ["成本高", "规模受限"],
            "effectiveness_score": 0.85,
            "scalability_score": 0.45
          }
        ],
        "trade_off_center": "规模 vs 质量",
        "trend": "近期工作趋向混合方法",
        "recommended_approach": "混合评估策略"
      }
    ],
    "trade_offs": [
      {
        "trade_off_id": "to_001",
        "trade_off_name": "规模 vs 质量",
        "paper_a": "2307.16789",
        "paper_b": "2307.13854",
        "choice_point": "评估数据收集方法",
        "dimension": "data_collection_strategy",
        "implications": {
          "high_quality": "成本可控但样本量小",
          "large_scale": "覆盖广但质量参差"
        },
        "hybrid_approaches": ["2404.03807 采用分层采样策略"],
        "optimal_balance": "分层采样：关键任务高质，其他自动生成",
        "confidence": 0.78
      }
    ],
    "technical_approaches": [],
    "anti_patterns_detected": [],
    "synthesis_quality": {
      "overall_score": 0.82,
      "summary_vs_synthesis": "synthesis_dominant",
      "integration_level": "high",
      "critical_analysis": "present",
      "evidence_quality": "strong"
    }
  },

  "research_gaps": [
    {
      "gap_id": "gap_001",
      "gap_description": "缺少安全性评估维度",
      "gap_type": "implicit",
      "identified_by": ["analysis"],
      "evidence": "现有 benchmark 主要关注功能完成度，未系统性评估安全风险",
      "evidence_level": "moderate",
      "evidence_sources": ["2307.16789", "2404.03807"],
      "proposed_direction": "多维度安全框架，包括 adversarial testing 和 safety constraints",
      "relevant_papers": ["2404.03807"],
      "importance": "high",
      "feasibility": "medium",
      "confidence": 0.75,
      "community_support": "low"
    }
  ],

  "open_questions": [
    {
      "question_id": "oq_001",
      "question": "如何平衡评估成本与结果可靠性？",
      "question_type": "methodological",
      "relevant_papers": ["2307.16789", "2307.13854", "2404.03807"],
      "context": "人工标注成本高但可靠，自动生成成本低但质量存疑",
      "possible_approaches": [
        "混合评估：关键样本人工标注，其他自动生成",
        "渐进式验证：自动生成后分层抽样验证",
        "主动学习：模型选择最需要人工标注的样本"
      ],
      "research_directions": [
        "成本效益分析框架",
        "自适应采样策略",
        "质量预测模型"
      ],
      "community_interest": "high",
      "difficulty_level": "medium"
    }
  ],

  "synthesis_insights": [
    {
      "insight_id": "insight_001",
      "insight": "评估指标演进呈现明显的层次化趋势",
      "supporting_evidence": ["2307.16789", "2404.03807", "2504.14773"],
      "confidence": 0.89,
      "novelty": "medium",
      "implications": "未来评估框架应考虑多任务层次化指标设计"
    }
  ],

  "synthesis_opportunities": [
    {
      "opportunity_id": "syn_001",
      "type": "convergence",
      "description": "Multiple papers converge on multi-dimensional evaluation",
      "papers": ["2307.16789", "2404.03807", "2504.14773"],
      "synthesis_angle": "Cross-domain consensus on quality indicator evolution",
      "narrative_template": "Recent studies have consistently demonstrated..."
    },
    {
      "opportunity_id": "syn_002",
      "type": "divergence",
      "description": "Different perspectives on evaluation approaches",
      "papers": ["2307.16789", "2307.13854"],
      "synthesis_angle": "Methodological or conceptual differences",
      "narrative_template": "Researchers disagree on..."
    },
    {
      "opportunity_id": "syn_003",
      "type": "evolution",
      "description": "Evolution from early approaches to current methods",
      "papers": ["2307.16789", "2404.03807"],
      "synthesis_angle": "Technical progression",
      "narrative_template": "The field has evolved from..."
    }
  ],

  "anti_pattern_guidance": {
    "patterns_to_avoid": [
      {
        "pattern": "annotated_bibliography_style",
        "detection_regex": "\\([A-Z][a-z]+(?: et al\\.|, \\d{4})\\) (?:said|found|argued)",
        "fix_strategy": "按主题分组: 'Multiple studies (A; B) found X'",
        "example_bad": "Smith (2020) found X. Jones (2021) found Y.",
        "example_good": "Recent studies (Smith, 2020; Jones, 2021) have consistently shown X."
      },
      {
        "pattern": "single_sentence_citations",
        "detection_regex": "[^。.]*\\[@[^\\]]+\\][^。.]*。[ \\n]([^。.]*\\[@[^\\]]+\\][^。.]*。[ \\n]){2,}",
        "fix_strategy": "合并为综合陈述",
        "example_bad": "[@smith2020] found X.\n[@jones2021] found Y.",
        "example_good": "Recent studies (Smith, 2020; Jones, 2021) have demonstrated X."
      },
      {
        "pattern": "chronological_only_organization",
        "detection_criteria": "检测是否仅有时间顺序章节而无主题章节",
        "fix_strategy": "创建主题章节，仅在主题内使用时间顺序",
        "example_bad": "## 2023 Studies\n## 2024 Studies",
        "example_good": "## Theme 1: Evaluation Metrics\n### Early Approaches (2023)"
      },
      {
        "pattern": "missing_synthesis",
        "detection_criteria": "段落结尾无综合总结句",
        "fix_strategy": "每段结尾添加综合",
        "example_bad": "Paper A did X. Paper B did Y.",
        "example_good": "Collectively, these studies demonstrate..."
      },
      {
        "pattern": "lack_of_critical_analysis",
        "detection_criteria": "只描述贡献不提局限",
        "fix_strategy": "平衡描述: 'While X contributes Y, it faces limitations in Z'",
        "example_bad": "Paper A proposes a novel method for X.",
        "example_good": "Paper A proposes X. However, it faces challenges in Y."
      },
      {
        "pattern": "missing_signposting",
        "detection_criteria": "章节间无过渡句",
        "fix_strategy": "添加路标: 'Having examined X, I now turn to Y...'",
        "example_bad": "## Section 1\n## Section 2",
        "example_good": "## Section 1\nHaving examined X, the next section explores Y.\n## Section 2"
      }
    ],
    "quality_threshold": {
      "max_allowed_patterns": 0,
      "warning_threshold": 1,
      "critical_threshold": 3
    }
  },

  "writing_guidance": {
    "paragraph_templates": {
      "synthesis_convergence": {
        "structure": ["Topic Sentence", "Evidence", "Analysis", "Transition"],
        "template": "**Topic Sentence**: Recent studies have demonstrated {finding} ({citations}).\n**Evidence**: {evidence}.\n**Analysis**: {implication}.\n**Transition**: However, {contrast}.",
        "example": "Recent studies have demonstrated multi-agent effectiveness (Smith, 2020; Jones, 2021)."
      },
      "comparison_divergence": {
        "structure": ["Topic Sentence", "Viewpoint A", "Viewpoint B", "Synthesis"],
        "template": "**Topic Sentence**: Researchers disagree on {topic}.\n**Viewpoint A**: {papers_a} emphasize {point_a}.\n**Viewpoint B**: {papers_b} argue {point_b}.\n**Synthesis**: This divergence reflects {reason}.",
        "example": "Researchers disagree on optimal evaluation metrics."
      },
      "evolution_progressive": {
        "structure": ["Topic Sentence", "Early Work", "Evolution", "Current State", "Synthesis"],
        "template": "**Topic Sentence**: The field has evolved from {old} to {new}.\n**Early Work**: {early_paper} established {foundation}.\n**Evolution**: {middle_paper} introduced {innovation}.\n**Current State**: {recent_paper} demonstrates {current_state}.\n**Synthesis**: This evolution reflects {driver}.",
        "example": "The field has evolved from binary to multi-dimensional evaluation."
      }
    },
    "signposting_phrases": {
      "section_opening": [
        "Three main themes emerge from the literature:",
        "This section examines {theme} through the lens of {perspective}:",
        "Before discussing {next_topic}, it is necessary to understand {current_topic}:"
      ],
      "section_transition": [
        "Having examined {previous}, I now turn to {next}:",
        "The previous section established {previous_finding}. This section extends this by:",
        "Building on these findings, we now consider {implication}:"
      ],
      "synthesis_markers": [
        "Collectively, these studies suggest...",
        "Taken together, these findings indicate...",
        "The convergence of evidence points to...",
        "Synthesizing these results reveals...",
        "Across these studies, a clear pattern emerges..."
      ],
      "transition_within_paragraph": [
        "Similarly,", "In contrast,", "Building upon this,",
        "Conversely,", "Furthermore,", "Moreover,", "However,", "Nevertheless,"
      ]
    },
    "narrative_structures": {
      "hourglass": {
        "broad_intro_percent": 15,
        "narrow_focus_percent": 55,
        "broad_synthesis_percent": 30,
        "description": "Start broad, narrow to specific, then broaden to implications"
      },
      "thematic": {
        "recommended_themes": "3-5 main themes",
        "organization": "Group by concept, not by author or chronology",
        "description": "Organize around conceptual themes"
      },
      "developmental": {
        "structure": "Early → Middle → Current → Future",
        "best_for": "Historical reviews, theoretical evolution",
        "description": "Trace development of ideas over time"
      }
    },
    "quality_checklist": {
      "synthesis_verification": "确保每段综合多个来源，而非逐一罗列",
      "signposting_check": "验证章节过渡是否清晰，使用路标语言",
      "gap_explicitness": "确认研究空白明确陈述并证明其重要性",
      "critical_voice": "每篇论文的描述应包含贡献和局限",
      "logical_connectors": "使用演进、继承、对比等逻辑连接词"
    }
  },

  "cross_domain_analysis": {
    "bridging_entities": [
      {
        "entity_id": "2506.12508",
        "entity_type": "academic_paper",
        "title": "AgentOrchestra: A Hierarchical Multi-Agent Framework",
        "domains_connected": ["repo", "community"],
        "connection_count": 4,
        "importance_score": 8.0
      }
    ],
    "relationship_clusters": [
      {
        "cluster_id": "cluster_001",
        "cluster_type": "implementation_cluster",
        "paper_id": "2506.12508",
        "implementing_repos": ["microsoft/autogen", "crewAIInc/crewAI"],
        "repo_count": 2
      }
    ],
    "cross_domain_insights": [
      {
        "insight_type": "implementation_gap",
        "description": "Key papers lack GitHub implementations",
        "affected_papers": ["2308.08155"],
        "recommendation": "Priority for implementation"
      }
    ],
    "implementation_gaps": [],
    "community_validation_gaps": [],
    "cross_domain_graph": {
      "nodes": 35,
      "edges": 25,
      "paper_to_repo": 5,
      "repo_to_community": 7
    }
  },

  "value_assessment": {
    "paper_value_scores": [
      {
        "arxiv_id": "2601.23265",
        "title": "PaperBanana",
        "value_score": 0.92,
        "value_tier": "S",
        "institution_backing": "Google",
        "institution_type": "big_tech",
        "institution_boost": 0.30,
        "boost_reason": "Big Tech: Google",
        "dimension_scores": {
          "impact_score": 0.85,
          "innovation_score": 0.90,
          "practicality_score": 0.88,
          "timeliness_score": 0.95
        },
        "trend_indicators": ["emerging_hotspot", "industry_adoption"]
      },
      {
        "arxiv_id": "2602.03828",
        "title": "AutoFigure",
        "value_score": 0.78,
        "value_tier": "A",
        "institution_backing": null,
        "institution_type": null,
        "institution_boost": 0,
        "boost_reason": "No special institutional backing identified",
        "dimension_scores": {
          "impact_score": 0.70,
          "innovation_score": 0.80,
          "practicality_score": 0.85,
          "timeliness_score": 0.75
        },
        "trend_indicators": ["emerging_hotspot"]
      }
    ],
    "value_ranking": [
      {"rank": 1, "arxiv_id": "2601.23265", "title": "PaperBanana", "tier": "S", "value_score": 0.92},
      {"rank": 2, "arxiv_id": "2602.03828", "title": "AutoFigure", "tier": "A", "value_score": 0.78}
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
    ],
    "tier_distribution": {
      "S": 1,
      "A": 2,
      "B": 3,
      "C": 1
    }
  }
}
```

---

## JSON Validation Rules

```python
validation_rules = {
    "required_fields": [
        "research_metadata",
        "quality_assessment",
        "prisma_2020_compliance",
        "citation_network",
        "thematic_analysis",
        "evolution_analysis",
        "comparative_analysis",
        "research_gaps",
        "open_questions",
        "synthesis_insights",
        "synthesis_opportunities",
        "anti_pattern_guidance",
        "writing_guidance",
        "value_assessment"  # v2.6 新增
    ],
    "confidence_levels": ["low", "medium-low", "medium", "medium-high", "high"],
    "evidence_levels": ["weak", "moderate", "strong", "very_strong"],
    "quality_score_range": [0.0, 1.0],
    "value_tiers": ["S", "A", "B", "C"],  # v2.6 新增
    "institution_types": ["big_tech", "top_university", "star_author", "emerging", None],  # v2.6 新增
    "trend_indicators": ["emerging_hotspot", "paradigm_shift", "industry_adoption", "community_hype", "viral_spread"],  # v2.6 新增
    "timestamp_format": "ISO 8601",
    "id_formats": {
        "gap_id": r"^gap_\d{3}$",
        "question_id": r"^oq_\d{3}$",
        "theme_id": r"^theme_\d{3}$",
        "chain_id": r"^chain_\d{3}$",
        "opportunity_id": r"^syn_\d{3}$"
    },
    "synthesis_opportunity_types": ["convergence", "divergence", "evolution"],
    "paragraph_template_types": ["synthesis_convergence", "comparison_divergence", "evolution_progressive"]
}
```

---

## Field Definitions Quick Reference

| 字段 | 类型 | 说明 |
|------|------|------|
| `research_metadata` | object | 元数据信息 |
| `quality_assessment` | object | AMSTAR 2 + ROBIS 质量评估 |
| `prisma_2020_compliance` | object | PRISMA 2020 合规性 |
| `citation_network` | object | 引用网络分析 |
| `thematic_analysis` | object | 主题聚类分析 |
| `evolution_analysis` | object | 演进路径分析 |
| `comparative_analysis` | object | 比较分析 |
| `research_gaps` | array | 研究空白列表 |
| `open_questions` | array | 开放问题列表 |
| `synthesis_insights` | array | 综合洞察 |
| `synthesis_opportunities` | array | 综合机会（v2.1+） |
| `anti_pattern_guidance` | object | 反模式指导（v2.1+） |
| `writing_guidance` | object | 写作指导（v2.1+） |
| `cross_domain_analysis` | object | 跨域分析（v2.3+） |
| `value_assessment` | object | 价值评估（v2.6+） |

### value_assessment 子字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `paper_value_scores` | array | 每篇论文的价值评分详情 |
| `value_ranking` | array | 按价值排序的论文列表 |
| `top_picks` | object | 推荐列表（must_read, high_value, emerging_trends, foundational） |
| `institution_distribution` | object | 机构分布统计 |
| `emerging_hotspots` | array | 新兴热点列表 |
| `tier_distribution` | object | S/A/B/C 分布统计 |

---

## Related Knowledge Files / 相关知识文件

- `@knowledge:logic_analysis.md` - 逻辑分析方法和协议
- `@knowledge:memory_graph.md` - 记忆图谱系统
- `@knowledge:cross_domain_tracker.md` - 跨域追踪
- `@knowledge:value_assessment.md` - 价值评估框架（v2.6+）
- `@knowledge:institution_patterns.md` - 机构识别模式（v2.6+）
