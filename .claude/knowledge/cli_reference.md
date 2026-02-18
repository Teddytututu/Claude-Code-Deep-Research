# CLI Reference / CLI 命令参考

本文档包含所有 CLI 工具的命令参考。

---

## Memory Graph CLI (v4.0)

```bash
# Build graph from existing research data
python "tools\memory_graph_cli.py" --build

# Query related papers
python "tools\memory_graph_cli.py" --query <arxiv_id>

# Generate visualization
python "tools\memory_graph_cli.py" --visualize --format html

# Show graph statistics
python "tools\memory_graph_cli.py" --stats
```

---

## Memory System CLI (v9.0)

```bash
# Save semantic graph
python "tools\memory_system.py" --save-graph research_data/semantic_graph.json

# Migrate old state
python "tools\memory_system.py" --migrate research_data/old_state.json --output research_data
```

---

## Cross-Domain Tracking (v2.0)

```bash
# Show statistics
python "tools\cross_domain_tracker.py" --load-data research_data --stats

# Find bridging entities
python "tools\cross_domain_tracker.py" --load-data research_data --bridging --min-domains 2

# Save output
python "tools\cross_domain_tracker.py" --load-data research_data --save cross_domain_tracking_output.json
```

---

## Heartbeat Monitor (v9.5) - NEW

**Purpose**: Monitor subagent health and detect stuck agents.

```bash
# Write heartbeat (called by subagents)
python "tools\heartbeat_monitor.py" --write academic-researcher --status running --items 5

# Write with time tracking
python "tools\heartbeat_monitor.py" --write academic-researcher --status accelerate --items 10 \
    --start-time "2026-02-18T10:00:00" --budget 2880

# Check heartbeat for specific agent
python "tools\heartbeat_monitor.py" --check academic-researcher

# List all heartbeats
python "tools\heartbeat_monitor.py" --list

# Find stuck agents (no update for > 5 minutes)
python "tools\heartbeat_monitor.py" --stuck --timeout 300

# Clear heartbeat
python "tools\heartbeat_monitor.py" --clear academic-researcher

# Clear all
python "tools\heartbeat_monitor.py" --clear-all
```

**Output Example**:
```
┌────────────────────────────────────────────────────────────────────────┐
│                    HEARTBEAT MONITOR                                   │
├────────────────────────────────────────────────────────────────────────┤
│  🔄 academic-researcher | running     | 5     items | age: 2m 30s     │
│  🔄 github-watcher      | accelerate  | 8     items | age: 3m 15s     │
│  ⚠️ community-listener  | running     | 3     items | age: 8m 45s     │
│  ✅ cross-domain-track  | complete    | 12    items | age: 1m 00s     │
└────────────────────────────────────────────────────────────────────────┘
```

**Status Codes**:
- 🔄 `running` - Normal operation
- ⚡ `accelerate` - Time critical, rapid mode
- 💾 `saving` - Saving checkpoint
- ✅ `complete` - Finished successfully
- ❌ `error` - Encountered error
- ⚠️ Stale (no update for > 5 min)

---

## Resilience CLI (v9.0)

```bash
# Show system status
python "tools\resilience.py" --status

# List checkpoints for session
python "tools\resilience.py" --checkpoints <session_id>

# Cleanup old checkpoints
python "tools\resilience.py" --cleanup <session_id> --keep 5
```

---

## Batch Visualization Generation

```bash
# Generate all visualizations
python "tools\generate_visualizations.py"
```

---

## Claude Code Usage Tips / Claude Code 使用技巧

```bash
# 使用 /init 初始化项目记忆
/init "这是一个 TypeScript 项目，使用 strict 模式"

# 分层 CLAUDE.md 文件结构
CLAUDE.md                 # 项目根目录
docs/CLAUDE.md            # 设计文档
components/CLAUDE.md       # 组件说明

# Git 分支策略
git checkout -b feature/new-function
# 完成后 /clear 清除上下文
```

---

## Verification Commands / 验证命令

```bash
# 1. 检查 CLAUDE.md 行数
wc -l "CLAUDE.md"

# 2. 检查 knowledge 文件
ls -la ".claude/knowledge/" | grep -E "execution|verification|phase|cli"

# 3. 检查引用格式
grep -c "@knowledge" "CLAUDE.md"

# 4. 检查心跳状态
python "tools\heartbeat_monitor.py" --list

# 5. 检查 stuck agents
python "tools\heartbeat_monitor.py" --stuck
```
