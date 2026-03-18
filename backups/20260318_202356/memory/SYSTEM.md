# 🛠️ SYSTEM.md - 系统配置

> 工具、权限与环境配置
> 最后更新：2026-02-25

---

## 📇 索引（快速查找）

| 工具/系统 | 配置项 | 详情位置 |
|-----------|--------|----------|
| **Obsidian** | 存档路径、Vault名称 | 见「Obsidian配置」 |
| **macOS日历** | 权限状态、AppleScript访问 | 见「日历配置」 |
| **飞书** | 用户ID、API权限、消息发送 | 见「飞书配置」 |
| **AI天团** | Gateway端口、启动命令 | 见「AGENTS.md」 |

---

## 📋 核心规则

### 1. Obsidian配置

**Vault路径**：
- 主Vault：`~/Documents/Obsidian Vault/`
- 学习笔记：`~/Documents/Obsidian Vault/AI_17天共学计划/`

**文件命名规范**：
- 学习笔记：`Day XX - 主题.md`
- 日期记录：`YYYY-MM-DD.md`

**CLI工具**：
- 命令：`obsidian-cli`
- 安装：`brew install yakitrak/yakitrak/obsidian-cli`

---

### 2. 日历配置

#### macOS日历
**权限状态**：✅ 已授权
**授权方式**：AppleScript直接访问
**使用示例**：
```bash
osascript -e 'tell application "Calendar" to make new event...'
```

**已创建的日程**：
| 标题 | 时间 | 提醒 |
|------|------|------|
| 汉高客户在线会议 - 展会视频 | 2月27日 16:00-17:00 | 15:30 |

#### 飞书日历
**权限状态**：⚠️ 受限
**限制原因**：创建用户日历事件需要user_access_token
**替代方案**：生成ICS文件手动导入

---

### 3. 飞书配置

**用户ID**：`ou_f804aeb5aa82fc47dca4830476a6e75d`

**已授权权限**（部分关键权限）：
- `im:message` - 发送消息
- `calendar:calendar.event:create` - 创建日历事件
- `calendar:calendar.event:read` - 读取日历事件
- `docs:document` - 文档操作
- `drive:file` - 云文件操作

**消息发送命令**：
```bash
openclaw message send --channel feishu --target [user_id] --message "内容"
```

---

### 4. Google日历配置（gog）

**状态**：❌ 未配置
**需要**：
1. `gog auth credentials /path/to/client_secret.json`
2. `gog auth add [email] --services calendar`

---

### 5. 工作空间路径

| 用途 | 路径 |
|------|------|
| 主工作区 | `~/.openclaw/workspace/Feishu/` |
| 记忆文件 | `~/.openclaw/workspace/Feishu/memory/` |
| 早报网站 | `~/.openclaw/workspace/xiaoyumao-news-web/` |
| AI天团配置 | `~/.openclaw-*/` |

---

## 🔄 更新记录

- 2026-02-25: 创建系统配置文件，记录工具配置状态
