---
name: claude-code-best-practices
description: Comprehensive Claude Code development workflow guidance. Use when working with Claude Code for coding tasks, especially for multi-step implementations, debugging, refactoring, code review, and project onboarding. Covers context management, Plan Mode, subagents, CLAUDE.md configuration, session management, and verification strategies.
---

# Claude Code 最佳实践

基于官方文档深度学习的 Claude Code 高效使用指南。

## 核心原则

### 1. Context Window 是最宝贵的资源

- Claude 的上下文窗口包含：对话历史、读取的文件、命令输出、CLAUDE.md、加载的 skills
- 随着上下文填充，性能会下降；满时可能"遗忘"早期指令
- **策略**：频繁使用 /clear、用 subagents 调查、保持 CLAUDE.md 简洁

### 2. 先探索，再规划，最后编码

**推荐四阶段工作流**：
1. **探索** (Plan Mode) - 使用只读工具分析代码库
2. **规划** - 创建详细实施计划，与用户迭代
3. **执行** - 实施计划
4. **验证** - 运行测试、检查输出

**进入 Plan Mode**：
- 会话中：按 Shift+Tab 切换到 Plan Mode（显示 ⏸ plan mode on）
- 启动时：`claude --permission-mode plan`

### 3. 提供验证标准

Claude 能自我验证时表现显著提高：

| 场景 | 差提示 | 好提示 |
|------|--------|--------|
| 实现函数 | "实现验证邮箱的函数" | "编写 validateEmail 函数。测试用例：[email] 为真，invalid 为假。实现后运行测试" |
| UI 更改 | "让仪表板更好看" | "[粘贴截图] 实现此设计。对结果截图并与原设计比较。列出差异并修复" |
| 修复错误 | "构建失败" | "构建失败，出现此错误：[粘贴]。修复它并验证构建成功。解决根本原因，不要抑制错误" |

## CLAUDE.md 配置

### 有效 CLAUDE.md 的特点

- **简短易读**：只包含 Claude 无法从代码推断的内容
- **广泛适用**：每行都问自己"删除这行会导致 Claude 犯错吗？"
- **可迭代**：像对待代码一样对待它——审查、修剪、测试更改

### ✅ 包含 vs ❌ 排除

| ✅ 包含 | ❌ 排除 |
|--------|--------|
| Claude 无法猜测的 Bash 命令 | Claude 能通过读取代码弄清楚的 |
| 与默认值不同的代码风格规则 | 标准语言约定 |
| 测试指令和首选测试运行器 | 详细 API 文档（链接代替） |
| 仓库礼仪（分支命名、PR 约定） | 经常变化的信息 |
| 项目特定的架构决策 | 长篇解释或教程 |
| 常见陷阱或非显而易见的行为 | 文件逐个描述代码库 |

### 示例 CLAUDE.md

```markdown
# Code style
- Use ES modules (import/export), not CommonJS (require)
- Destructure imports when possible

# Workflow
- Be sure to typecheck after making code changes
- Prefer running single tests, not the whole test suite

# Git
- Branch naming: feature/description or fix/description
- PRs should include tests and typecheck pass
```

### CLAUDE.md 存放位置

- `~/.claude/CLAUDE.md`：适用于所有 Claude 会话
- `./CLAUDE.md`：项目级，可检入 git
- `./CLAUDE.local.md`：个人本地配置（加入 .gitignore）
- 子目录：`packages/frontend/.claude/CLAUDE.md`（monorepo 支持）

## 会话管理

### 常用命令

| 命令 | 功能 |
|------|------|
| `claude` | 启动交互模式 |
| `claude -p "query"` | 运行一次性查询（无头模式） |
| `claude -c` / `--continue` | 继续最近对话 |
| `claude -r` / `--resume` | 恢复之前的对话 |
| `claude --resume --fork-session` | 分叉会话（保留历史，新会话ID） |
| `claude --from-pr <number>` | 从 PR 恢复会话 |

### 会话内命令

| 命令 | 功能 |
|------|------|
| `/clear` | 清除对话历史，重置上下文 |
| `/compact [focus]` | 手动压缩上下文（保留关键内容） |
| `/context` | 查看上下文占用情况 |
| `/rewind` | 回退到之前的检查点 |
| `/rename <name>` | 给会话命名（便于后续查找） |
| `/resume` | 切换到不同对话 |

### 纠正方向的最佳实践

- **Esc**：停止 Claude 当前操作，保留上下文
- **Esc + Esc** 或 `/rewind`：回退到之前的代码和对话状态
- **两次以上纠正后**：运行 `/clear` 用更好的提示重新开始

**避免"厨房水槽会话"**：不相关任务之间用 `/clear`，避免上下文充满无关信息。

## 常见工作流

### 理解新代码库

```
> what does this project do?
> what technologies does this project use?
> explain the folder structure
> how does the authentication system work?
```

### 高效修复错误

```
> 用户报告会话超时后登录失败。检查 src/auth/ 中的身份验证流程，
> 特别是令牌刷新。编写一个失败的测试来重现问题，然后修复它。
```

### 使用 Subagents 调查

```
> use subagents to investigate how our payment system handles refunds,
> and whether we have any existing utilities I should reuse.
```

**Subagent 用途**：
- 读取大量文件时代码库探索
- 专门关注不使主对话混乱的任务
- 实现后的验证（审查边界情况）

### 重构代码

```
> refactor the authentication module to use async/await instead of callbacks.
> first explore the current implementation, create a plan, then execute.
```

### 创建 PR

```
> /commit-push-pr
```
或使用分步：
```
> commit my changes with a descriptive message
> push to origin
> create a pull request
```

## 权限模式

按 **Shift+Tab** 循环切换：

1. **默认**：编辑文件和运行命令前询问
2. **自动接受编辑**：自动编辑文件，命令仍询问（⏵⏵ accept edits on）
3. **Plan Mode**：只使用只读工具，创建计划（⏸ plan mode on）
4. **Delegate Mode**：仅通过 agent teams 协调（有活跃 team 时可用）

**危险模式**：`claude --dangerously-skip-permissions` 绕过所有权限检查。

## 提示技巧

### 具体上下文

```
# 差
add a widget

# 好
查看主页上现有小部件的实现方式。HotDogWidget.php 是个好例子。
按照这个模式实现一个新的日历小部件，让用户选择月份并向前/向后分页选择年份。
```

### 使用 @ 引用文件

```
> explain how @src/auth/login.ts handles token refresh
> review @src/components/Button.tsx for accessibility issues
```

### 让 Claude 采访你

```
I want to build [描述]. Interview me in detail about technical implementation,
UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions,
dig into the hard parts. Then write a complete spec to SPEC.md.
```

## 扩展功能

### Skills

- 存放在 `~/.claude/skills/<name>/SKILL.md`（个人）或 `./.claude/skills/`（项目）
- 自动触发或手动调用 `/<skill-name>`
- `disable-model-invocation: true`：仅手动调用
- `context: fork`：在子代理中运行
- `allowed-tools`：限制工具访问

### MCP Servers

连接外部服务：GitHub、Slack、Figma、数据库等。

### Hooks

在 Claude 工作流特定点自动运行脚本：
```
> write a hook that runs eslint after every file edit
> write a hook that blocks writes to the migrations folder
```

运行 `/hooks` 交互配置。

### Subagents

定义在 `.claude/agents/<name>.md`：
```yaml
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for injection vulnerabilities,
authentication flaws, secrets in code, insecure data handling.
Provide specific line references and suggested fixes.
```

## 避免常见失败模式

| 失败模式 | 修复方法 |
|----------|----------|
| 厨房水槽会话 | 不相关任务之间用 `/clear` |
| 一遍又一遍纠正 | 两次失败后 `/clear` 用更好的提示重新开始 |
| 过度指定的 CLAUDE.md | 无情修剪，规则只在需要时保留 |
| 信任但不验证 | 始终提供测试、脚本或截图验证 |
| 无限探索 | 限定范围或使用 subagents |

## 相关资源

- 官方文档：https://code.claude.com/docs
- 最佳实践：https://code.claude.com/docs/zh-CN/best-practices
- 常见工作流：https://code.claude.com/docs/zh-CN/common-workflows
