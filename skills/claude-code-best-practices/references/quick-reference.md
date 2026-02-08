# Claude Code 快速参考

## 启动和恢复

```bash
# 启动新会话
claude

# 继续最近对话
claude -c

# 恢复特定对话
claude -r
claude --resume oauth-migration

# 从 PR 恢复
claude --from-pr 123

# Plan Mode 启动
claude --permission-mode plan

# 无头模式（脚本化）
claude -p "explain this function" --output-format json
```

## 权限模式切换

| 快捷键 | 模式 |
|--------|------|
| Shift+Tab | 循环：默认 → 自动接受编辑 → Plan Mode → Delegate Mode |
| Option+T (mac) / Alt+T | 切换思考模式开/关 |
| Ctrl+O | 切换详细模式（查看思考过程） |

## 会话内命令

| 命令 | 功能 |
|------|------|
| `/clear` | 重置上下文 |
| `/compact [focus]` | 压缩上下文，保留关键内容 |
| `/context` | 查看上下文占用 |
| `/rewind` | 回退检查点 |
| `/resume` | 切换会话 |
| `/rename <name>` | 命名会话 |
| `/help` | 显示命令 |
| `/init` | 创建 CLAUDE.md |
| `/mcp` | 管理 MCP 服务器 |
| `/hooks` | 管理 hooks |

## 提示模板

### 功能实现

```
实现 [功能描述]。

需求：
- [具体要求1]
- [具体要求2]

验证：
- [测试用例1]
- [测试用例2]

完成后运行测试验证。
```

### 调试

```
[描述问题或粘贴错误]

相关代码在 [路径]。先探索理解问题，
然后编写失败测试重现，最后修复。
```

### 重构

```
将 [旧模式] 重构为 [新模式]。

先探索当前实现，创建详细计划，
与我确认后再执行。
```

### 代码审查

```
use a subagent to review @<file> for:
- Security vulnerabilities
- Edge cases
- Performance issues
- Code style consistency
```

## CLAUDE.md 模板

```markdown
# Code Style
- [风格规则1]
- [风格规则2]

# Workflow
- [工作流规则1]
- [工作流规则2]

# Commands
- Test: [测试命令]
- Lint: [lint命令]
- Build: [构建命令]

# Common Tasks
- [常见任务说明]
```

## Skill 模板

```markdown
---
name: my-skill
description: What this skill does and when to use it
disable-model-invocation: true  # 仅手动调用
allowed-tools: Read, Bash
---

# Skill Instructions

Step-by-step workflow...
```

## 输出格式

```bash
# 纯文本（默认）
claude -p "query"

# JSON
claude -p "query" --output-format json

# 流式 JSON
claude -p "query" --output-format stream-json
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `CLAUDE_CODE_EFFORT_LEVEL` | 思考深度：low/medium/high |
| `MAX_THINKING_TOKENS` | 最大思考令牌数 |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Skills 字符预算 |
