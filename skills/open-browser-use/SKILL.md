---
name: open-browser-use
description: 通用浏览器自动化技能 — 基于 Open Browser Use 的开源 Chrome 自动化栈。任何 Agent（CEO/CRO/COO/CTO/REVIEW/PLAN）均可通过 CLI、MCP 或 SDK 操控真实 Chrome 浏览器。
---

# Open Browser Use — 小羽毛 AI 天团通用技能

## 概述

**Open Browser Use** 是 iFurySt/Louis 开发的**开源浏览器自动化栈**，作为 Codex Browser Use 的开源替代。它提供一个 MV3 Chrome 扩展 + 原生消息主机 + CLI + SDK（JS/Python/Go）+ MCP 服务器，让 AI Agent 可以操控真实 Chrome 浏览器。

> 本技能对 AI 天团所有成员（CEO/CRO/COO/CTO/REVIEW/PLAN）通用，不限于特定运行时。

## 架构

```
Agent Runtime (任何 Agent)
  → open-browser-use CLI / MCP Server / SDK
  → Open Browser Use Socket
  → Native Messaging Host
  → Chrome Extension
  → Chrome Tabs / Debugger / History / Downloads
```

## 安装状态

| 组件 | 状态 | 路径 |
|------|------|------|
| CLI (`open-browser-use` / `obu`) | ✅ 已安装 v0.1.26 | `$HOME/.npm-global/bin/` |
| Chrome 扩展 | ⏳ 待安装 | 需运行 `open-browser-use setup beta` + 用户手动拖入 Chrome |
| JS SDK | ✅ npm install open-browser-use-sdk | 按需安装 |
| MCP Server | ⏳ 待配置 | 参见下方 MCP 配置 |

## 快速使用

### 1. 设置会话 ID（所有操作前必须先设置）

```sh
export OBU_SESSION_ID="obu-<task-slug>-$(date +%Y%m%d%H%M%S)"
export PATH="$HOME/.npm-global/bin:$PATH"
```

> ⚠️ **每个任务必须使用唯一 session-id**，不要共用 `obu-cli` 回退会话。

### 2. 检查连通性

```sh
obu ping --session-id "$OBU_SESSION_ID"
obu info --session-id "$OBU_SESSION_ID"
obu user-tabs --session-id "$OBU_SESSION_ID"
```

### 3. 常用操作

```sh
# 列出标签页
obu tabs --session-id "$OBU_SESSION_ID"
obu user-tabs --session-id "$OBU_SESSION_ID"

# 打开标签页
obu open-tab --session-id "$OBU_SESSION_ID" --url https://example.com

# 导航
obu navigate --session-id "$OBU_SESSION_ID" --tab-id <tab-id> --url https://example.com

# CDP 命令（执行 JS）
obu cdp --session-id "$OBU_SESSION_ID" --tab-id <tab-id> \
  --method Runtime.evaluate \
  --params '{"expression":"document.title"}'

# 命名会话
obu name-session --session-id "$OBU_SESSION_ID" --name "Task - OBU"

# 搜索历史
obu history --session-id "$OBU_SESSION_ID" --query "关键词" --limit 20

# 清理标签页（每次任务结束前必做）
obu finalize-tabs --session-id "$OBU_SESSION_ID" --keep '[]'
```

### 4. Action Plan（免 SDK 的多步骤编排）

```sh
obu run --session-id "$OBU_SESSION_ID" -c '
name-session "Hacker News - OBU"
open-tab https://news.ycombinator.com
wait-load domcontentloaded
page-info
finalize-tabs []
'
```

## MCP 配置（推荐）

向 OpenClaw 配置中添加 MCP 服务器，使所有 Agent 可通过 MCP 工具操控浏览器：

```toml
[mcp_servers.open_browser_use]
command = "obu"
args = ["mcp", "--session-id", "obu-<task-or-conversation-id>"]
```

> 每个任务使用不同的 `--session-id`。

MCP 暴露的工具：
- `ping`, `info`, `tabs`, `user_tabs`, `history`
- `open_tab`, `claim_tab`, `navigate`, `wait_load`, `page_info`
- `cdp`, `move_mouse`, `wait_file_chooser`, `set_file_chooser_files`
- `name_session`, `finalize_tabs`, `turn_ended`, `call`, `run_action_plan`

## SDK 用法

### JavaScript
```ts
import { connectOpenBrowserUse } from "open-browser-use-sdk";
const browser = await connectOpenBrowserUse({ sessionId: "obu-task-..." });
const tab = await browser.newTab();
await tab.goto("https://example.com", { waitUntil: "domcontentloaded" });
// ... 操作
await browser.client.finalizeTabs([]);
browser.close();
```

### Python
```py
from open_browser_use import connect_open_browser_use
browser = connect_open_browser_use(socket_path=..., session_id="obu-task-...")
tab = browser.new_tab()
tab.goto("https://example.com")
browser.client.finalize_tabs([])
browser.close()
```

### Go
```go
import obu "github.com/ifuryst/open-codex-browser-use/packages/open-browser-use-go"
browser, _ := obu.ConnectActive(obu.Options{SessionID: "obu-task-...", Timeout: 20 * time.Second})
tab, _ := browser.NewTab()
// ...
defer browser.Client.FinalizeTabs(nil)
```

## 操作规则

### ✅ 必须做的
- 每个任务使用**唯一 session-id**，格式 `obu-<task-slug>-<timestamp>`
- 任务开始前先 `name-session` 命名会话
- 任务结束时 `finalize-tabs` 清理标签页
- 使用 `user-tabs` 找用户已有标签页前先列出，不猜测 tab id
- 优先使用 `claim-tab` 获取用户已有标签页
- 文件上传使用 `wait-file-chooser` + `set-file-chooser-files` 流程

### ❌ 禁止做的
- 不要检查 cookies、密码、session stores 或不相关的浏览器数据
- 不要猜 tab id — 先 list 再使用
- 不要依赖 `obu-cli` 回退会话做 agent 任务
- 除明确任务需要外，不要读/写剪贴板
- 不要在 finalize 之后再调用浏览器操作

### ⚠️ 需用户确认
- 安装扩展、打开 Chrome
- 上传本地文件、提交表单
- 购买、删除、发送等外部可见变更
- 登录、支付、CAPTCHA 等人工步骤

## Tab 生命周期

```
创建/认领标签页 → 操作 → finalize-tabs
                        ├── keep '[]' → 不保留（默认）
                        ├── keep '[{"url":"...","status":"deliverable"}]' → 交付保留
                        └── keep '[{"url":"...","status":"handoff"}]' → 移交
```

- **deliverable**：标签页本身就是交付物（编辑好的文档、仪表盘、购物车等）
- **handoff**：任务未完成，需要用户后续继续（登录、审批、CAPTCHA 等）

## 故障排除

```sh
# 检查连接
obu ping --session-id "$OBU_SESSION_ID"
obu info --session-id "$OBU_SESSION_ID"

# 修复原生消息主机
obu install-manifest

# 重新安装
obu setup  # Web Store 版
obu setup beta  # GitHub Release ZIP 版（推荐当前）

# 检查扩展
obu manifest
```

常见问题排查顺序：
1. Chrome 是否安装并运行
2. Open Browser Use 扩展是否安装并启用
3. 原生消息主机是否注册
4. 用户是否批准了 Chrome 扩展提示

## 参考

- [安装指南](./references/installation.md)
- [SDK 与协议](./references/sdk-and-protocol.md)
- [故障排除](./references/troubleshooting.md)
- [GitHub 仓库](https://github.com/iFurySt/open-codex-browser-use)
- [深度解析文章](https://www.ifuryst.com/en/blog/2026/open-browser-use/)
