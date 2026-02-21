# CLAUDE.md 模块化重组计划

**Version**: v1.0 (2026-02-21)

## 目标
1. 将 CLAUDE.md 中冗长的示例内容提取到独立的协议文件
2. 使用相对路径引用，保持主文件简洁
3. 添加执行时可直接读取的验证逻辑

## 文件结构

```
.claude/
├── CLAUDE.md (主编排文件，简洁版)
├── protocols/           (可复用的协议和模板)
│   ├── time-budget.md
│   ├── phase1-parallel-research.md
│   ├── report-generation.md
│   └── verification-logic.md
├── agents/             (已有)
├── knowledge/           (已有)
└── hooks/              (已有)
```

## 待办

### Step 1: 创建协议文件 (已完成)
- [x] `.claude/protocols/time-budget.md` - 时间计算公式、状态阈值
- [x] `.claude/protocols/phase1-parallel-research.md` - 并行部署代码、进度显示
- [x] `.claude/protocols/report-generation.md` - 报告结构模板
- [ ] `.claude/protocols/verification-logic.md` - 验证函数

### Step 2: 更新 CLAUDE.md
将详细内容替换为相对路径引用：
- 代码示例 → 引用 `protocols/phase1-parallel-research.md`
- 时间计算 → 引用 `protocols/time-budget.md`
- 报告模板 → 引用 `protocols/report-generation.md`

### Step 3: 添加 @read 指令
确保 CLAUDE.md 执行时能读取子文件：
```markdown
## 引用协议文件

@read: .claude/protocols/time-budget.md
@read: .claude/protocols/phase1-parallel-research.md
@read: .claude/protocols/report-generation.md
```

## 验证方式

```bash
# 测试相对路径读取
python -c "
from pathlib import Path
import re

# 读取 CLAUDE.md
with open('CLAUDE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查 @read 引用
reads = re.findall(r'@read:\s+(.+?)\n', content)
print(f'找到 {len(reads)} 个 @read 引用')

# 检查文件是否存在
for read in reads:
    path = Path(read.strip())
    if path.exists():
        print(f'  ✅ {read}')
    else:
        print(f'  ❌ {read}')
"
```
