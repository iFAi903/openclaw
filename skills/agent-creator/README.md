# 🤖 AI 天团 Agent 创建 Skill

> 基于重新学习的官方指南和历史配置经验汇总
> 生成时间: 2026-03-01
> 版本: 1.0.0

---

## 📚 学习来源汇总

### 1. 官方指南（Obsidian 中保存）
- 《OpenClaw Multi-Agent 与 Sub-Agent 搭建指南》
- 《Subagent 配置案例》
- 《超级 Agent 原设定模板》
- 《Agent 元设定与职能配置参考》
- 《OpenClaw Agent 指南》

### 2. 历史配置经验
- **setup-ai-team.sh** (~/workspace/ai-team-config/)
  - 4 个完整 Agent 的配置脚本
  - 白色小羽毛 (copy) - 端口 18782
  - 紫色小羽毛 (product) - 端口 18785
  - 金色小羽毛 (design) - 端口 18788
  - 蓝色小羽毛 (dev) - 端口 18790
  - 多 Gateway + 多飞书机器人模式

- **现有 CRO/CTO 配置** (~/.openclaw-agents/)
  - CRO: 端口 18766, 模型 Claude Opus 4
  - CTO: 端口 18793, 模型 Claude Opus 4
  - 简化模式（HTTP API 调用）

### 3. 关键经验总结

#### ✅ 配置模式对比

| 维度 | 简化模式 | 完整模式 |
|------|---------|---------|
| **适用场景** | 子 Agent (CRO/CTO) | 独立机器人 |
| **通信方式** | HTTP API | 飞书消息 |
| **配置复杂度** | 低 | 高 |
| **飞书应用** | 不需要 | 每个 Agent 独立应用 |
| **端口需求** | 是 | 是 |
| **启动方式** | 环境变量 | 环境变量或 profile |

#### ✅ 核心避坑指南

1. **不支持 `--config` 参数**
   ```bash
   # ❌ 错误
   openclaw gateway --config xxx.json start
   
   # ✅ 正确
   OPENCLAW_CONFIG=xxx.json openclaw gateway start
   ```

2. **jiti 缓存清理（重要！）**
   ```bash
   # 修改 plugins/ 下的 .ts 文件后必须执行
   rm -rf /tmp/jiti/
   openclaw gateway restart
   ```

3. **端口检查**
   ```bash
   # 启动前检查端口占用
   lsof -i :18766
   
   # 强制占用
   openclaw gateway start --port 18766 --force
   ```

4. **工作目录隔离**
   - 每个 Agent 必须有独立 workspace
   - 配置文件、日志、会话分离
   - 避免相互污染

#### ✅ 推荐模型配置

| Agent 角色 | 推荐模型 | 说明 |
|-----------|---------|------|
| CEO/调度 | Gemini-3-pro | 意图理解、任务拆解 |
| CRO/创意 | Claude Opus 4 | 文案、策划、市场分析 |
| CTO/技术 | Claude Opus 4 / Kimi | 代码、架构设计 |
| 子 Agent | Gemini Flash | 简单任务、快速响应 |

---

## 🛠️ 生成的 Skill 文件

### 1. SKILL.md
完整的多 Agent 配置指南，包含：
- 快速开始（简化/完整模式）
- 配置详解
- 目录结构
- 启动与管理
- 跨 Agent 通信
- 故障排查
- 最佳实践

### 2. agent-manager.sh
实用的管理脚本，功能包括：
- `create-simplified` - 创建简化模式 Agent
- `start/stop` - 启动/停止指定 Agent
- `start-all/stop-all` - 批量操作
- `status` - 查看所有 Agent 状态

---

## 🚀 快速使用

### 创建 CRO Agent
```bash
cd ~/.openclaw/workspace/Feishu/skills/agent-creator
./agent-manager.sh create-simplified \
  -n cro \
  -p 18766 \
  -m "anthropic/claude-opus-4-6"
```

### 创建 CTO Agent
```bash
./agent-manager.sh create-simplified \
  -n cto \
  -p 18793 \
  -m "anthropic/claude-opus-4-6"
```

### 启动 Agent
```bash
./agent-manager.sh start -n cro
./agent-manager.sh start -n cto
```

### 查看状态
```bash
./agent-manager.sh status
```

---

## 📋 配置文件模板

### 简化模式（CRO/CTO 示例）

```json
{
  "gateway": {
    "port": 18766,
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "your-secure-token"
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["kimi-coding/k2.5"]
      },
      "thinkingDefault": "high",
      "workspace": "~/.openclaw-agents/cro/workspace"
    }
  }
}
```

### 完整模式（独立飞书机器人）

```json
{
  "gateway": {
    "port": 18782,
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "${OPENCLAW_GATEWAY_TOKEN}"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "pairing",
      "domain": "feishu",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "botName": "白色小羽毛",
          "enabled": true
        }
      },
      "groupPolicy": "open",
      "connectionMode": "websocket",
      "requireMention": true,
      "streaming": true
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3-pro-preview"
      },
      "workspace": "~/.openclaw-copy-agent/workspace"
    }
  }
}
```

---

## 🔗 相关文件位置

| 文件 | 路径 |
|------|------|
| Skill 文档 | `~/.openclaw/workspace/Feishu/skills/agent-creator/SKILL.md` |
| 管理脚本 | `~/.openclaw/workspace/Feishu/skills/agent-creator/agent-manager.sh` |
| 历史配置脚本 | `~/.openclaw/workspace/ai-team-config/setup-ai-team.sh` |
| CRO 配置 | `~/.openclaw-agents/cro/openclaw.json` |
| CTO 配置 | `~/.openclaw-agents/cto/openclaw.json` |

---

## 📝 后续迭代建议

1. **添加 launchd plist 配置**
   - 实现开机自动启动
   - 崩溃自动重启

2. **集成 LanceDB Pro**
   - 多 scope 记忆隔离
   - 跨 Agent 知识共享

3. **添加监控告警**
   - Gateway 健康检查
   - API 调用成功率统计

4. **完善元设定模板**
   - IDENTITY.md 自动生成
   - SOUL.md 角色定制
   - TOOLS.md 能力清单

---

*生成者: 小羽毛 CEO 🪶*
*基于 OpenClaw 多 Agent 最佳实践*
