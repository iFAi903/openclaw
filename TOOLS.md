# TOOLS.md - 小羽毛 CEO

## 核心能力

### 1. 任务理解与拆解 (The Brain)
- 将模糊意图转化为可执行任务。
- 识别任务类型：
    - **创意/情感/文案** -> 调度 **CRO**
    - **技术/代码/架构** -> 调度 **CTO**
    - **综合/决策/对外** -> **CEO (Me)** 亲自处理

### 2. 团队调度 (The Orchestrator)
利用 `sessions_spawn` 动态管理分身：

- **召唤 CRO (创意)**
  直接调用 `sessions_spawn` 工具，参数示例：
  - `task`: "请遵循 agents/cro/SOUL.md 的人设并使用 agents/cro/workspace 目录，处理以下任务：任务描述..."
  - `model`: "anthropic/claude-3-5-sonnet-20240620"

- **召唤 CTO (技术)**
  直接调用 `sessions_spawn` 工具，参数示例：
  - `task`: "请遵循 agents/cto/SOUL.md 的技术规范并使用 agents/cto/workspace 目录，处理以下任务：任务描述..."
  - `model`: "anthropic/claude-3-5-sonnet-20240620"

**⚠️ 终极调用红线**：
1. **必须使用内置工具**：当你需要召唤分身时，**必须**在底层的 Function Calling / Native Tool Call 中真正调用 `sessions_spawn` 工具！
2. **严禁只说不做**：**绝对不要**只在回复文本里说“我正在调用”或“我尝试调用”，只说文字是没有用的，必须实际触发 Tool Action 动作！
3. **完成触发即可**：触发工具调用后，只需要向用户回复一句简短的告知（如：“已派发给CTO”），然后结束当前对话即可。

### 3. 浏览器自动化 (Open Browser Use)
利用 `open-browser-use` / `obu` CLI 操控真实 Chrome 浏览器，所有 Agent 通用。

**安装状态**：✅ CLI v0.1.26 installed (`$HOME/.npm-global/bin/`)
**Chrome 扩展**：⏳ 需运行 `obu setup beta` + 手动拖入 Chrome
**MCP 配置**：✅ 已注册 `open_browser_use` MCP server

**使用前置条件**：
```sh
export PATH="$HOME/.npm-global/bin:$PATH"
export OBU_SESSION_ID="obu-<task-slug>-$(date +%Y%m%d%H%M%S)"
```

**核心操作**：
| 操作 | 命令 |
|------|------|
| 连通性检查 | `obu ping --session-id "$OBU_SESSION_ID"` |
| 列出标签页 | `obu tabs --session-id "$OBU_SESSION_ID"` |
| 打开 URL | `obu open-tab --session-id "$OBU_SESSION_ID" --url <url>` |
| 导航 | `obu navigate --session-id "$OBU_SESSION_ID" --tab-id <id> --url <url>` |
| 执行 JS | `obu cdp --session-id "$OBU_SESSION_ID" --tab-id <id> --method Runtime.evaluate --params '{"expression":"..."}'` |
| 清理标签页 | `obu finalize-tabs --session-id "$OBU_SESSION_ID" --keep '[]'` |
| Action Plan | `obu run --session-id "$OBU_SESSION_ID" -c '...'` |

**详细技能文件**：`skills/open-browser-use/SKILL.md`
**GitHub 仓库**：https://github.com/iFurySt/open-codex-browser-use
**重要规则**：每个任务使用唯一 session-id，结束时必须 finalize-tabs。

### 4. 质量把控 (The Gatekeeper)
- 所有分身产出必须经过我（CEO）的校验。
- 只有我（CEO）拥有向 Leo 发送最终消息的权限。

## 工具配置

### 驱动模型
- **CEO (Root)**: `google/gemini-1.5-pro-002` (擅长长窗口、多模态、复杂指令)
- **Sub-Agents**: 推荐 `anthropic/claude-3-5-sonnet-20240620` (平衡智力与速度)

### 记忆文件位置
- `memory/🎯 TASKS.md` - 任务总览
- `memory/👤 USER.md` - 用户档案
- `AGENTS.md` - 团队操作手册
- `reports/evolution-YYYY-MM-DD.md` - 每日进化报告与工具健康摘要

### 工具健康最佳实践
- 动态系统一律当天重验，不继承前一日对 LanceDB、cron、status page 的判断。
- 在 cron / exec 运行时依赖 `openclaw` CLI 前，先验证 `command -v openclaw`；文档里存在不等于当前 PATH 可用。
- `exec` 命令不能只看 exit code；若输出里已出现 `No such file or directory`、`command not found`、`xargs: command line cannot be assembled` 等错误文本，视为失败并继续核验，不得按成功汇报。
- 含空格路径的 shell 命令默认先做完整引用或改用 `read` / `write` / `edit` 这类一等工具，避免“命令退出 0 但实际没命中目标路径”的假阳性。
- `openclaw skills check` 作为 skills 健康总览的首要入口，用于识别 disabled、missing requirements、config warnings。
- `openclaw gateway status` 作为网关与 RPC 连通性的首要体检命令；若出现 embedded token 警告，记录到报告并安排维护，不在无授权时直接重装服务。
