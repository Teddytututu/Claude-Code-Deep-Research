# 成功模式库 (Learned Patterns)

与 anti-patterns 对应，记录可复用的成功经验。

---

## 如何使用本文件

1. **PreFlect 协议** 在任务执行前参考本文件
2. 识别适用于当前任务的成功模式
3. 在执行计划中应用这些模式
4. **AfterFlect 协议** 在任务完成后更新本文件

---

## 学术论文搜索类成功模式 (Academic Research)

| 模式 | 描述 | 适用场景 | 效果 | 发现时间 |
|------|------|---------|------|---------|
| **多分类并行搜索** | 同时搜索 cs.AI + cs.LG + cs.CL | 主题跨领域时 | high | initial |
| **中期数量检查** | 每 3 篇论文检查是否达标 | 避免过早停止 | high | initial |
| **引用链追踪** | 对高被引论文追踪其引用 | 构建认知谱系 | high | initial |
| **OR 组合搜索** | 使用 "term1 OR term2" 扩展覆盖 | 关键词不确定时 | medium | initial |
| **年度过滤** | 结合 date_from/date_to 聚焦 | 需要最新进展时 | medium | initial |
| **机构优先** | 优先关注顶级机构的论文 | 时间有限时 | medium | initial |

### 详细模式说明

#### 多分类并行搜索
```
适用条件: 研究主题涉及 AI + ML + NLP 等多个领域
执行方法: 在单个搜索回合中并行调用多个分类
预期效果: 候选论文数量增加 2-3 倍
示例:
  search_papers(query="topic", categories=["cs.AI", "cs.LG", "cs.CL"])
```

#### 中期数量检查
```
适用条件: 所有论文搜索任务
执行方法: 每收集 3 篇论文后检查数量是否达标
预期效果: 避免过早停止，确保满足最小要求
示例:
  if papers_collected == 3:
      if papers_collected < min_target:
          adjust_search_strategy()
```

#### 引用链追踪
```
适用条件: 需要构建完整的认知谱系
执行方法: 对高被引论文（citations > 50）追踪其引用的根源论文
预期效果: 发现基础理论和早期工作
示例:
  for paper in high_citation_papers:
      track_citations(paper.arxiv_id, depth=2)
```

---

## GitHub 项目搜索类成功模式 (GitHub Research)

| 模式 | 描述 | 适用场景 | 效果 | 发现时间 |
|------|------|---------|------|---------|
| **论文→代码关联** | 检查论文中的 GitHub 链接 | 寻找官方实现 | high | initial |
| **Stars 渐进筛选** | 先 >100，再 >500，再 >1000 | 平衡数量和质量 | medium | initial |
| **Topics 组合搜索** | 使用 topics 参数而非仅关键词 | 发现相关项目 | high | initial |
| **架构模式提取** | 为每个项目标注架构类型 | 识别技术流派 | high | initial |
| **活跃度检查** | 检查 recent commits | 确保维护状态 | medium | initial |
| **依赖分析** | 检查 requirements.txt | 技术栈识别 | low | initial |

### 详细模式说明

#### 论文→代码关联
```
适用条件: 已有学术论文，需要找到对应的开源实现
执行方法:
  1. 检查 arXiv 论文页面的 code link
  2. 搜索 "paper title + github"
  3. 检查 Papers with Code
预期效果: 找到官方或社区实现
```

#### Stars 渐进筛选
```
适用条件: 候选项目过多，需要优先级排序
执行方法:
  1. 第一轮: stars > 100 (获取候选池)
  2. 第二轮: stars > 500 (筛选质量)
  3. 第三轮: stars > 1000 (顶级项目)
预期效果: 平衡数量和质量，避免遗漏小而精的项目
```

#### Topics 组合搜索
```
适用条件: 关键词搜索结果不足
执行方法:
  get_repo_structure(org/repo) 检查 topics
  搜索相同 topics 的其他项目
预期效果: 发现关键词搜索遗漏的项目
```

---

## 社区讨论搜索类成功模式 (Community Research)

| 模式 | 描述 | 适用场景 | 效果 | 发现时间 |
|------|------|---------|------|---------|
| **批量共识提取** | 每 5 个帖子暂停提炼共识 | 避免只收集不分析 | high | initial |
| **跨平台对比** | 对比 Reddit/HN/知乎的观点差异 | 获取多元视角 | high | initial |
| **高互动筛选** | 优先关注 upvotes/comments 高的帖子 | 获取热门观点 | medium | initial |
| **实践者优先** | 关注有代码示例的帖子 | 获取实践经验 | medium | initial |
| **时间窗口** | 关注最近 1 年的讨论 | 获取最新观点 | medium | initial |
| **情感分类** | 区分 positive/negative/mixed | 理解社区态度 | low | initial |

### 详细模式说明

#### 批量共识提取
```
适用条件: 所有社区调研任务
执行方法: 每收集 5 个帖子后暂停，提炼共识点
预期效果: 避免只收集不分析，及时发现模式
示例:
  if discussions_collected % 5 == 0:
      extract_consensus_points(discussions)
```

#### 跨平台对比
```
适用条件: 需要全面了解社区观点
执行方法:
  1. Reddit (r/LocalLLaMA, r/MachineLearning)
  2. Hacker News
  3. 知乎/掘金 (中文社区)
  4. 对比不同平台的观点差异
预期效果: 发现东西方观点差异，获取多元视角
```

---

## 通用成功模式 (Cross-Cutting Patterns)

| 模式 | 描述 | 适用场景 | 效果 |
|------|------|---------|------|
| **渐进式写入** | 每次更新立即写入磁盘 | 避免超时丢失数据 | critical |
| **并行工具调用** | 在单个回合中并行调用多个工具 | 提高效率 | high |
| **时间检查点** | 定期检查剩余时间 | 避免最后时刻失败 | high |
| **降级策略** | 准备 Plan B | 应对意外情况 | medium |
| **质量优先** | 宁可少而精，不要多而杂 | 资源有限时 | medium |

---

## 有效的预防措施 (Effective Preventions)

| 预防措施 | 预防的风险 | 证据 |
|---------|-----------|------|
| 设置中期检查点 | 过早停止 | 检查点发现数量不足，及时调整 |
| 使用 OR 组合搜索 | 搜索词过窄 | 候选数量增加 2-3 倍 |
| 添加重试延迟 | API Rate Limit | 成功完成请求 |
| 准备备用数据源 | 网络超时 | 主源失败后切换成功 |

---

## 更新本文件

当 AfterFlect 识别到高效果（effectiveness >= medium）的模式时，更新本文件：

1. 在相应任务类型下添加新模式
2. 记录模式描述、适用场景、效果
3. 可选：添加详细模式说明
4. 如果是有效的预防措施，也添加到预防措施表

---

## CHANGELOG

### v1.0 (2026-02-21)

**Initial Release**:
- 学术论文搜索类成功模式（6 项）
- GitHub 项目搜索类成功模式（6 项）
- 社区讨论搜索类成功模式（6 项）
- 通用成功模式（5 项）
- 有效的预防措施（4 项）
- 详细模式说明示例
