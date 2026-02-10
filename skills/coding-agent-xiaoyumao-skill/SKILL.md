---
name: coding-agent-xiaoyumao-skill
description: Comprehensive Claude Code integration for OpenClaw. Combines headless execution wrapper with best practices for AI-driven development workflows. Supports planning, implementation, debugging, and code review via Claude Code CLI.
metadata:
  version: 1.0.0
  author: 小羽毛 (Xiaoyumao)
  based_on:
    - win4r/claude-code-clawdbot-skill (technical wrapper)
    - Anthropic Claude Code Best Practices
---

# Coding Agent - 小羽毛 Skill

让 Clawdbot 通过 Claude Code CLI 实现工程规划、代码开发、调试重构的完整工作流。

## 核心能力

| 能力 | 说明 |
|------|------|
| 🎯 **规划优先** | Plan Mode 先探索分析，再动手编码 |
| 📝 **上下文管理** | 自动处理 TTY/headless 环境，避免卡住 |
| 🔧 **全栈开发** | 代码编写、调试、重构、审查一站式 |
| 🤖 **Subagent 协作** | 支持多 Agent 并行处理复杂任务 |
| ⚡ **无缝集成** | 与 vibecoding-toolkit 工具矩阵联动 |

---

## 快速开始

### 前置要求

1. **安装 Claude Code**
   ```bash
   npm install -g @anthropic-ai/claude-code
   # 或
   pip install claude-code
   ```

2. **验证安装**
   ```bash
   claude --version
   # 预期输出：claude 0.x.x
   ```

3. **配置权限**（首次使用）
   ```bash
   claude
   # 按提示完成登录和授权
   ```

### 基础用法

**简单查询（无头模式）**
```python
# 使用 wrapper 脚本运行
./scripts/claude_code_run.py -p "分析这个代码库的结构" --permission-mode plan
```

**带工具权限**
```python
./scripts/claude_code_run.py \
  -p "运行测试并修复失败" \
  --allowedTools "Bash,Read,Edit" \
  --output-format json
```

**交互模式**
```bash
claude
# 然后直接输入你的需求
```

---

## 核心工作流

### 工作流 1：新项目启动（推荐）

```bash
# Step 1: 进入项目目录，启动 Claude Code
cd /path/to/your/project
claude

# Step 2: 切换到 Plan Mode（按 Shift+Tab）
# 显示 ⏸ plan mode on

# Step 3: 让 Claude 分析项目并创建规划
> 分析这个项目的技术栈和目录结构，创建一个 CLAUDE.md 配置文件

# Step 4: 审查生成的规划，确认后切换回普通模式

# Step 5: 执行实现
> 根据 CLAUDE.md 中的规划，实现核心功能模块
```

### 工作流 2：功能开发

```bash
# 方式 A：交互式（推荐复杂功能）
claude
> 我要添加用户认证功能，包括登录、注册、JWT token
> 先分析现有代码结构，然后制定实现计划

# 方式 B：一次性（适合简单任务）
./scripts/claude_code_run.py \
  -p "为 User 模型添加 email 验证方法" \
  --allowedTools "Read,Edit" \
  --permission-mode accept-edits
```

### 工作流 3：Debug 调试

```bash
claude
> 运行测试时出现了这个错误：[粘贴错误信息]
> 请定位问题并修复，修复后运行测试验证
```

### 工作流 4：代码审查

```bash
# 使用 Subagent 进行审查
claude
> 使用 @code-reviewer subagent 审查 src/auth/ 目录下的所有代码
> 关注安全漏洞、性能问题和代码风格
```

---

## 高级用法

### Plan Mode（规划模式）

**进入方式**：
- 启动时：`claude --permission-mode plan`
- 会话中：按 `Shift+Tab` 切换

**适用场景**：
- 新项目启动
- 复杂功能设计
- 大规模重构前
- 代码库探索

**特点**：
- 只使用只读工具（Read, Glob, Grep, Bash 查询）
- 不会修改任何文件
- 生成详细的实施计划

### Subagent 协作

**定义 Subagent**（在 `.claude/agents/` 目录）

```yaml
# .claude/agents/security-reviewer.md
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

**调用方式**：
```bash
claude
> @security-reviewer 审查 src/api/ 目录下的所有接口代码
```

### Context 管理技巧

| 命令 | 作用 |
|------|------|
| `/clear` | 清除对话历史，重置上下文 |
| `/compact` | 压缩上下文，保留关键信息 |
| `/context` | 查看当前上下文占用 |
| `/rewind` | 回退到之前的检查点 |

**最佳实践**：
- 不相关任务之间用 `/clear`
- 复杂任务中途用 `/compact` 整理
- 两次纠正失败后 `/clear` 重新开始

---

## 技术实现

### Wrapper 脚本说明

`scripts/claude_code_run.py` 解决了 headless/自动化场景下的 TTY 问题：

```python
# 核心逻辑：分配伪终端
# 使用 script -q -c ... /dev/null 包装 claude -p 命令
# 避免在无 TTY 环境下卡住
```

**参数说明**：

| 参数 | 说明 | 示例 |
|------|------|------|
| `-p, --prompt` | 要执行的提示 | `"分析代码结构"` |
| `--permission-mode` | 权限模式 | `plan`, `accept-edits`, `default` |
| `--allowedTools` | 允许的工具 | `"Bash,Read,Edit"` |
| `--output-format` | 输出格式 | `json`, `text` |
| `--model` | 指定模型 | `opus`, `sonnet` |

### 与 vibecoding-toolkit 集成

```python
# 在 vibecoding-toolkit 中使用
from coding_agent_xiaoyumao import ClaudeCodeAgent

# 创建 Claude Code 实例
agent = ClaudeCodeAgent(
    mode="plan",  # 或 "implement", "debug"
    allowed_tools=["Read", "Edit", "Bash"]
)

# 执行复杂任务
result = agent.run(
    task="实现用户认证系统",
    context_files=["src/models/user.py", "src/config/auth.py"]
)
```

---

## CLAUDE.md 配置建议

在项目根目录创建 `CLAUDE.md` 文件：

```markdown
# 代码风格
- 使用 ES modules，不用 CommonJS
- 优先使用 async/await

# 工作流
- 修改后运行 typecheck
- 优先运行单测而非全量测试

# 项目结构
- src/ 源码
- tests/ 测试
- docs/ 文档
```

Claude 会自动读取此文件并遵循其中的规范。

---

## 故障排除

### 问题：claude 命令未找到

```bash
# 检查安装位置
which claude
# 预期：/usr/local/bin/claude 或 ~/.local/bin/claude

# 如果未找到，添加到 PATH
export PATH="$HOME/.local/bin:$PATH"
```

### 问题：wrapper 脚本卡住

```bash
# 检查是否有 TTY
tty
# 如果输出 "not a tty"，wrapper 脚本会自动处理

# 手动测试伪终端
script -q -c "echo OK" /dev/null
```

### 问题：权限被拒绝

```bash
# 检查 Claude Code 是否已授权
claude auth list

# 重新登录
claude auth login
```

---

## 相关资源

- [Claude Code 官方文档](https://code.claude.com/docs)
- [Claude Code 最佳实践](https://code.claude.com/docs/zh-CN/best-practices)
- [VibeCoding Toolkit](../vibecoding-toolkit/SKILL.md) - 工具矩阵协同

---

*Created by 小羽毛 🪶*  
*Based on win4r/claude-code-clawdbot-skill + Anthropic Best Practices*