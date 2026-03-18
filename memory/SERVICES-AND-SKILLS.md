# 🛠️ SERVICES-AND-SKILLS.md - 外部服务与技能

> 第三方服务、API、工具技能的使用规范与配置
> 最后更新：2026-02-25

---

## 📇 索引（快速查找）

| 服务/技能 | 类型 | 用途 | 配置位置 |
|-----------|------|------|----------|
| **Feishu** | 消息平台 | 主要沟通渠道 | 见「飞书服务」 |
| **OpenClaw** | Agent框架 | AI天团运行基础 | 见「OpenClaw配置」 |
| **Deep Research Analyzer** | Skill | 研究仓库分析 | 见「已安装技能」 |
| **Vercel** | 部署平台 | 早报网站托管 | 见「部署服务」 |
| **Obsidian** | 笔记工具 | 学习资料存档 | 见「笔记工具」 |

---

## 📋 核心规则

### 1. 消息服务

#### 飞书 (Feishu)
**用途**：主要用户沟通渠道

**用户ID**：`ou_f804aeb5aa82fc47dca4830476a6e75d`

**已授权权限**：
- `im:message` - 发送消息
- `calendar:calendar.event:create` - 创建日历事件
- `docs:document` - 文档操作
- `drive:file` - 云文件操作

**使用方式**：
```python
message send --channel feishu --target [user_id] --message "内容"
```

**限制**：
- 创建用户日历事件需要 user_access_token（当前受限）
- 解决方案：生成 ICS 文件手动导入

---

### 2. Agent框架

#### OpenClaw
**用途**：AI天团运行基础框架

**配置路径**：
- 主配置：`~/.openclaw/openclaw.json`
- 工作空间：`~/.openclaw/workspace/Feishu/`
- 技能目录：`~/.openclaw/skills/`

**Gateway端口**：
| Agent | 端口 |
|-------|------|
| main | 18780 |
| copy-agent | 18782 |
| product-agent | 18785 |
| design-agent | 18788 |
| dev-agent | 18790 |

**常用命令**：
```bash
# 启动 Gateway
openclaw gateway start

# 查看状态
openclaw status

# 发送消息
openclaw message send --target [id] --message "内容"
```

---

### 3. 已安装技能

| 技能名称 | 路径 | 功能 | 状态 |
|----------|------|------|------|
| **deep-research-analyzer** | `~/.openclaw/skills/deep-research-analyzer/` | 研究仓库深度分析 | ✅ 已安装 |

**技能使用方式**：
- 技能通过 SKILL.md 自动触发
- 用户请求分析仓库时自动加载

---

### 4. 部署服务

#### Vercel
**用途**：AI新闻早报网站托管

**网站地址**：https://xiaoyumao-news-web.vercel.app

**部署方式**：
```bash
cd ~/.openclaw/workspace/xiaoyumao-news-web
npm run build
npx vercel@latest --token [TOKEN] --yes --prod
```

**更新频率**：每日 07:30（自动）

---

### 5. 笔记工具

#### Obsidian
**用途**：学习资料存档与管理

**Vault路径**：`~/Documents/Obsidian Vault/`

**学习笔记路径**：`~/Documents/Obsidian Vault/AI_17天共学计划/`

**CLI工具**：`obsidian-cli`

**命名规范**：`Day XX - 主题.md`

---

### 6. 日历服务

#### macOS日历
**状态**：✅ 已授权
**权限路径**：系统设置 → 隐私与安全性 → 日历
**使用方式**：AppleScript 直接操作

#### Google日历 (gog)
**状态**：❌ 未配置
**需要**：OAuth 授权配置

#### 飞书日历
**状态**：⚠️ API受限
**限制**：创建用户事件需要 user_access_token

---

### 7. 内容获取服务

#### RSS订阅源（AI新闻）
**用途**：每日早报新闻获取

**主要源**：
- 机器之心: https://www.jiqizhixin.com/rss
- The Verge AI: https://www.theverge.com/rss/ai-artificial-intelligence/index.xml
- TechCrunch AI: https://techcrunch.com/category/artificial-intelligence/feed/
- Product Hunt: https://www.producthunt.com/feed

---

### 8. 技能开发规范

**创建新技能步骤**：
1. 创建目录：`mkdir -p ~/.openclaw/skills/[skill-name]/`
2. 编写 `SKILL.md`（包含 frontmatter + 使用说明）
3. 添加 `scripts/` 或 `references/`（可选）
4. 打包：`zip -r [skill-name].skill [skill-name]/`

**SKILL.md 结构**：
```yaml
---
name: skill-name
description: 技能描述，触发条件
---

# 技能名称

## 何时使用
- 触发条件1
- 触发条件2

## 使用方式
...
```

---

### 9. OpenClaw 故障排查

#### 端口冲突问题
**症状**：`ai-team-status.sh` 显示 Agent 未运行，或启动时报 "Port already in use"

**排查步骤**：
1. 检查端口占用：
   ```bash
   for p in 18782 18785 18788 18790; do
     nc -z 127.0.0.1 $p && echo "$p open" || echo "$p closed"
   done
   ```

2. 检查 LaunchAgent 配置：
   ```bash
   grep -E '1878|1879' ~/Library/LaunchAgents/ai.openclaw.*.plist
   ```

3. 验证服务状态：
   ```bash
   launchctl list | grep openclaw
   ```

**修复流程**：
1. 停止所有 agent：
   ```bash
   for a in copy-agent product-agent design-agent dev-agent; do
     launchctl bootout gui/$UID/ai.openclaw.$a 2>/dev/null || true
   done
   ```

2. 修正 plist 端口（如被错误配置）：
   ```bash
   # copy-agent → 18782
   sed -i '' 's/18789/18782/g' ~/Library/LaunchAgents/ai.openclaw.copy-agent.plist
   # product-agent → 18785
   sed -i '' 's/18789/18785/g' ~/Library/LaunchAgents/ai.openclaw.product-agent.plist
   # design-agent → 18788
   sed -i '' 's/18789/18788/g' ~/Library/LaunchAgents/ai.openclaw.design-agent.plist
   # dev-agent → 18790
   sed -i '' 's/18789/18790/g' ~/Library/LaunchAgents/ai.openclaw.dev-agent.plist
   ```

3. 重新启动：
   ```bash
   for a in copy-agent product-agent design-agent dev-agent; do
     launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.$a.plist
   done
   ```

4. 验证修复：
   ```bash
   ~/ai-team-status.sh
   ```

#### ai-team-status.sh 无 lsof 问题
**症状**：脚本显示 "未运行" 但服务实际正常

**原因**：系统缺少 `lsof` 命令

**解决**：脚本已修复，使用 `nc` 作为回退检测方式

---

## 🔄 更新记录

- 2026-02-25: 创建外部服务与技能配置文件
- 2026-02-25: 添加 OpenClaw 故障排查指南（端口冲突修复）
