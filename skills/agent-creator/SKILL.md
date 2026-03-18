# Skill: agent-creator
# Description: 多 Agent 系统创建与管理工具
# Version: 1.0.0
# Author: 小羽毛 AI 天团

## 概述

本 Skill 用于快速创建、配置和管理 OpenClaw 多 Agent 系统。支持两种模式：
- **简化模式**: 单 Gateway + HTTP API 调用（CRO/CTO 模式）
- **完整模式**: 多 Gateway + 多飞书机器人（AI 天团模式）

## 快速开始

### 1. 创建单个 Agent（简化模式）

```bash
# 创建 CRO Agent
openclaw skill run agent-creator --action create \
  --name "cro" \
  --port 18766 \
  --model "anthropic/claude-opus-4-6" \
  --workspace "~/.openclaw-agents/cro"

# 创建 CTO Agent
openclaw skill run agent-creator --action create \
  --name "cto" \
  --port 18793 \
  --model "anthropic/claude-opus-4-6" \
  --workspace "~/.openclaw-agents/cto"
```

### 2. 创建完整 AI 天团（完整模式）

```bash
# 一键创建 4 个 Agent
openclaw skill run agent-creator --action create-team
```

## 配置详解

### 简化模式配置（推荐用于子 Agent）

适合 CRO、CTO 等通过 HTTP API 调用的子 Agent：

```json
{
  "gateway": {
    "port": 18766,              // 独立端口
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

### 完整模式配置（独立飞书机器人）

适合需要独立飞书账号的 Agent：

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

## 目录结构

### 简化模式

```
~/.openclaw-agents/
├── cro/
│   ├── openclaw.json          # 配置文件
│   ├── agent/                 # Agent 元数据
│   ├── sessions/              # 会话存储
│   ├── logs/                  # 日志
│   └── workspace/             # 工作目录
│       ├── projects/
│       ├── assets/
│       └── docs/
└── cto/
    └── ...
```

### 完整模式

```
~/.openclaw-{agent}-agent/
├── openclaw.json              # 配置文件
├── agent/
├── sessions/
├── logs/
└── workspace/
```

## 启动与管理

### 启动单个 Agent

```bash
# 方式 1: 环境变量（推荐）
cd ~/.openclaw-agents/cro
OPENCLAW_CONFIG=~/.openclaw-agents/cro/openclaw.json \
  openclaw gateway start --port 18766

# 方式 2: 使用 --profile（需要配置 profiles）
openclaw --profile cro gateway start --port 18766
```

### 启动多个 Agent

```bash
# 使用生成的启动脚本
~/ai-team-start.sh

# 或手动启动
cd ~/.openclaw-agents/cro && nohup openclaw gateway start --port 18766 > logs/gateway.log 2>&1 &
cd ~/.openclaw-agents/cto && nohup openclaw gateway start --port 18793 > logs/gateway.log 2>&1 &
```

### 查看状态

```bash
# 检查端口
lsof -i :18766  # CRO
lsof -i :18793  # CTO

# 使用状态脚本
~/ai-team-status.sh
```

### 停止 Agent

```bash
# 使用停止脚本
~/ai-team-stop.sh

# 或手动停止
pkill -f "openclaw.*port 18766"
pkill -f "openclaw.*port 18793"
```

## 跨 Agent 通信

### HTTP API 调用

```bash
# CEO 调用 CRO
curl http://localhost:18766/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "任务内容",
    "context": "背景信息"
  }'

# CEO 调用 CTO
curl http://localhost:18793/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "技术任务",
    "context": "架构设计需求"
  }'
```

### 通过文件传递（推荐）

```
CEO 写入任务文件
    ↓
CRO/CTO 读取并处理
    ↓
写入结果文件
    ↓
CEO 读取验收
```

## 关键注意事项

### ⚠️ 1. 端口管理
- 每个 Agent 必须使用唯一端口
- 建议范围：18700-18800
- 启动前检查：`lsof -i :PORT`

### ⚠️ 2. 工作目录隔离
- 每个 Agent 必须有独立的 workspace
- 避免配置文件冲突
- 日志目录分离

### ⚠️ 3. 配置参数不支持 `--config`
❌ 错误：`openclaw gateway --config xxx start`
✅ 正确：`OPENCLAW_CONFIG=xxx openclaw gateway start`

### ⚠️ 4. jiti 缓存清理
修改 `plugins/` 下的 `.ts` 文件后：
```bash
rm -rf /tmp/jiti/
openclaw gateway restart
```

### ⚠️ 5. 飞书机器人配置
- 每个 Agent 需要独立的飞书应用
- 获取 App ID 和 App Secret
- 启用机器人能力和事件订阅

### ⚠️ 6. 模型选择建议
| Agent 类型 | 推荐模型 | 说明 |
|-----------|---------|------|
| CEO/调度 | Gemini-3-pro | 意图理解、任务拆解 |
| CRO/创意 | Claude Opus 4 | 文案、策划、市场 |
| CTO/技术 | Claude Opus 4 / Kimi | 代码、架构 |
| 通用/快速 | Gemini Flash | 简单任务、子 Agent |

### ⚠️ 7. 内存插件配置
使用 LanceDB Pro 时配置 scope：
```json
"scopes": {
  "global": "共享知识",
  "agent:cro": "CRO 私有",
  "agent:cto": "CTO 私有"
}
```

## 故障排查

### Gateway 无法启动
```bash
# 检查端口占用
lsof -i :18766

# 检查配置语法
openclaw config validate --config ~/.openclaw-agents/cro/openclaw.json

# 查看日志
tail -f ~/.openclaw-agents/cro/logs/gateway.log
```

### 飞书机器人无响应
1. 检查 App ID 和 App Secret 是否正确
2. 确认事件订阅配置为"长连接模式"
3. 检查配对状态：`openclaw pairing list feishu`
4. 批准配对请求：`openclaw pairing approve feishu <CODE>`

### 跨 Agent 调用失败
1. 检查目标 Agent 是否运行：`lsof -i :PORT`
2. 验证 Token 是否正确
3. 检查防火墙设置
4. 查看目标 Agent 日志

## 最佳实践

1. **命名规范**
   - 目录：`~/.openclaw-{role}-agent/` 或 `~/.openclaw-agents/{role}/`
   - 端口：连续分配，便于管理
   - Token：统一生成，安全存储

2. **模型策略**
   - 主力 Agent：高性能模型（Opus/Gemini Pro）
   - 子 Agent：平衡模型（Sonnet/Kimi）
   - 快速任务：轻量模型（Flash）

3. **监控告警**
   - 定期检查 Gateway 状态
   - 监控 API 调用成功率
   - 设置日志轮转

4. **备份策略**
   - 配置文件版本控制
   - 记忆数据库定期备份
   - 会话日志归档

## 参考资源

- OpenClaw 官方文档: https://docs.openclaw.ai
- 飞书开放平台: https://open.feishu.cn
- LanceDB Pro 插件: https://github.com/win4r/memory-lancedb-pro

## 版本历史

- v1.0.0 (2026-03-01): 初始版本，支持简化/完整两种模式
