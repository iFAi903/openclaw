# Gstack 技术机制分析

## 1. Conductor 多实例并行实现

### 1.1 conductor.json 配置

```json
{
  "orchestrator": "conductor",
  "agents": [
    {
      "name": "claude-code",
      "sessions": 3,
      "worktree_pattern": ".claude-worktrees/{index}",
      "startup_delay_ms": 500
    }
  ]
}
```

### 1.2 Git Worktrees 用法

Gstack 使用 **Git Worktrees** 实现多实例并行：

```bash
# 创建 worktree 目录结构
.claude-worktrees/
├── 1/          # 第一个 Claude Code 实例
├── 2/          # 第二个 Claude Code 实例
└── 3/          # 第三个 Claude Code 实例
```

**技术原理**：
- 每个 worktree 是同一仓库的独立工作目录
- 共享 `.git` 对象库，节省磁盘空间
- 每个实例可以在不同分支或同一分支独立工作
- 通过 `{index}` 占位符动态分配

**会话管理**：
```bash
# Preamble 中的会话跟踪
mkdir -p ~/.gstack/sessions
touch ~/.gstack/sessions/"$PPID"  # 记录当前进程 ID
_SESSIONS=$(find ~/.gstack/sessions -mmin -120 -type f 2>/dev/null | wc -l)
find ~/.gstack/sessions -mmin +120 -type f -delete  # 清理 2 小时前的会话
```

### 1.3 与 iFAi 的对比

| 特性 | Gstack | iFAi (当前) |
|------|--------|------------|
| 并行模型 | Git Worktrees + 多进程 | Pi Sub-agents (单实例) |
| 状态隔离 | 目录级隔离 | 会话级隔离 |
| 内存模型 | 每个实例独立内存 | 共享内存池 |
| 适用场景 | 大规模并行编码任务 | 轻量级多角色协作 |

## 2. 角色切换的技术实现

### 2.1 Slash Command 机制

Gstack 使用 **文件路径 + 命名约定** 实现角色切换：

```
用户输入: "/plan-eng-review"
        ↓
Claude Code 查找: .claude/skills/gstack/plan-eng-review/SKILL.md
        ↓
读取 SKILL.md → 提取 instructions → 执行
```

**技术实现细节**：
- 无环境变量切换
- 无 CLI 参数传递
- 纯基于文件系统的技能发现

### 2.2 技能发现机制

```bash
# 技能搜索路径（按优先级）
1. $(git rev-parse --show-toplevel)/.claude/skills/gstack/  # 项目本地
2. ~/.claude/skills/gstack/                                 # 用户全局
```

### 2.3 与 iFAi 的对比

| 特性 | Gstack | iFAi (当前) |
|------|--------|------------|
| 角色切换 | Slash Command → 文件路径 | sessions_spawn 子代理 |
| 触发方式 | 用户主动输入 | CEO 调度 |
| 权限控制 | `allowed-tools` in YAML | 继承父代理权限 |
| 上下文传递 | 无显式传递 | 文件/memory 共享 |

## 3. 记忆/上下文传递机制

### 3.1 Gstack 的上下文策略

**无全局状态，基于文件系统**：

```
~/.gstack/
├── sessions/                    # 会话跟踪文件
│   └── {PPID}
├── projects/
│   └── {slug}/                  # 项目级状态
│       ├── {branch}-reviews.jsonl    # 审查历史
│       └── contributor-logs/         # 贡献者日志
├── contributor-logs/            # 全局贡献者日志
└── .completeness-intro-seen     # 一次性标记
```

**上下文传递方式**：
1. **分支检测**：通过 `git branch --show-current` 动态获取
2. **审查历史**：JSON Lines 文件记录
3. **配置存储**：`gstack-config` CLI 工具
4. **TODO 文件**：`TODOS.md` 作为项目级共享状态

### 3.2 关键上下文文件

**reviews.jsonl**（每分支一个）：
```json
{"skill":"plan-eng-review","timestamp":"2026-03-15T10:00:00Z","status":"clean","overall_score":9,"unresolved":0}
{"skill":"ship-review-override","timestamp":"2026-03-15T11:00:00Z","decision":"ship_anyway"}
```

**gstack-config**：
```bash
~/.claude/skills/gstack/bin/gstack-config set key value  # 设置配置
gstack-config get key                                    # 获取配置
```

### 3.3 与 iFAi 的对比

| 特性 | Gstack | iFAi (当前) |
|------|--------|------------|
| 记忆存储 | 文件系统（JSON Lines + Markdown） | memory_* 工具 |
| 上下文传递 | 文件读取 | 工具调用 + 文件 |
| 跨会话持久化 | 文件持久化 | 向量数据库 |
| 检索方式 | 文件读取 + grep | 语义检索 |

## 4. 工作流编排模式

### 4.1 Review Readiness Dashboard

```
+====================================================================+
|                    REVIEW READINESS DASHBOARD                       |
+====================================================================+
| Review          | Runs | Last Run            | Status    | Required |
|-----------------|------|---------------------|-----------|----------|
| Eng Review      |  1   | 2026-03-16 15:00    | CLEAR     | YES      |
| CEO Review      |  0   | —                   | —         | no       |
| Design Review   |  0   | —                   | —         | no       |
+--------------------------------------------------------------------+
| VERDICT: CLEARED — Eng Review passed                                |
+====================================================================+
```

**技术实现**：
- 读取 `~/.gstack/projects/{slug}/{branch}-reviews.jsonl`
- 解析最近 7 天的条目
- 根据配置 `skip_eng_review` 决定是否阻止 Ship

### 4.2 Fix-First 模式

```
发现 Issues
    ↓
分类：AUTO-FIX vs ASK
    ↓
自动修复所有 AUTO-FIX
    ↓
批量询问 ASK 项（一次性 AskUserQuestion）
    ↓
应用用户批准的修复
    ↓
如果需要修复 → 提交 → STOP → 重新运行
```

### 4.3 Completeness Principle 量化

| 任务类型 | 人工团队 | CC+gstack | 压缩比 |
|----------|----------|-----------|--------|
| Boilerplate | 2 天 | 15 分钟 | ~100x |
| 测试编写 | 1 天 | 15 分钟 | ~50x |
| 功能实现 | 1 周 | 30 分钟 | ~30x |
| Bug 修复+回归测试 | 4 小时 | 15 分钟 | ~20x |
| 架构/设计 | 2 天 | 4 小时 | ~5x |
| 研究/探索 | 1 天 | 3 小时 | ~3x |

## 5. 测试基础设施

### 5.1 Test Framework Bootstrap

自动检测和配置测试框架：

```bash
# 运行时检测
[ -f Gemfile ] && echo "RUNTIME:ruby"
[ -f package.json ] && echo "RUNTIME:node"
# ...其他运行时

# 测试框架检测
ls jest.config.* vitest.config.* playwright.config.* .rspec pytest.ini
```

**自动配置流程**：
1. B2: 研究最佳实践（WebSearch 或内置表格）
2. B3: 框架选择（AskUserQuestion）
3. B4: 安装和配置
4. B4.5: 第一个真实测试（3-5 个）
5. B5: 验证
6. B5.5: CI/CD 流水线（GitHub Actions）
7. B6: 创建 TESTING.md
8. B7: 更新 CLAUDE.md
9. B8: 提交

### 5.2 Eval Suites（LLM 评估）

```bash
# 触发条件：提示相关文件变更
EVAL_JUDGE_TIER=full EVAL_VERBOSE=1 bin/test-lane --eval test/evals/<suite>_eval_test.rb
```

**评估层级**：
| Tier | 场景 | 速度 | 成本 |
|------|------|------|------|
| `fast` (Haiku) | 开发迭代 | ~5s | ~$0.07 |
| `standard` (Sonnet) | 默认开发 | ~17s | ~$0.37 |
| `full` (Opus) | Ship 前 | ~72s | ~$1.27 |

## 6. 浏览器自动化 (browse)

### 6.1 架构

```
 browse CLI
    ↓
 browser-manager.ts  # 管理浏览器实例
    ↓
 server.ts           # Playwright 服务器
    ↓
 commands.ts         # 命令实现
    ↓
 Playwright          # 底层浏览器控制
```

### 6.2 核心特性

- **状态持久化**：cookies、localStorage、会话在调用间保持
- **@ref 选择器**：通过 `snapshot -i` 获取交互元素引用
- **截图对比**：`snapshot -D` 生成 before/after diff
- **多标签页**：支持标签页切换和管理

### 6.3 命令示例

```bash
$B goto https://example.com
$B snapshot -i -a -o /tmp/annotated.png    # 带标注的快照
$B click @e3                               # 点击 @ref 元素
$B fill @e4 "value"                        # 填写输入
$B responsive /tmp/layout                  # 响应式截图
```

## 7. 版本管理

### 7.1 VERSION 文件格式

```
MAJOR.MINOR.PATCH.MICRO
```

**自动决策规则**：
- **MICRO**: < 50 行变更，微小调整
- **PATCH**: 50+ 行变更，Bug 修复/小功能
- **MINOR**: 大功能/架构变更 → 询问用户
- **MAJOR**: 里程碑/破坏性变更 → 询问用户

### 7.2 CHANGELOG 自动生成

从 git 历史自动生成：
```bash
git log <base>..HEAD --oneline
git diff <base>...HEAD
```

分类：Added / Changed / Fixed / Removed

## 8. 关键设计决策

### 8.1 为什么选择 Git Worktrees？

| 方案 | 优点 | 缺点 |
|------|------|------|
| Git Worktrees | 共享对象库、磁盘高效、原生 git 支持 | 需要管理多个目录 |
| Docker 容器 | 完全隔离 | 开销大、复杂 |
| 单进程多线程 | 简单 | 状态污染风险 |
| 多仓库克隆 | 简单 | 磁盘浪费、同步复杂 |

### 8.2 为什么使用文件系统而非数据库？

- **简单性**：无需数据库依赖
- **可审计性**：人类可读的 JSON Lines
- **版本控制**：可纳入 git 历史
- **可移植性**：易于备份和迁移

### 8.3 为什么使用 YAML Frontmatter？

- **结构化元数据**：name、version、allowed-tools
- **工具兼容**：易于解析
- **人类可读**：Markdown 友好的格式
