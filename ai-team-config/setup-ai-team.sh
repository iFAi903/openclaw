#!/bin/bash
# =============================================================================
# AI 天团 - 多 Gateway + 多飞书机器人 配置脚本
# 版本: 2.0
# 作者: 小羽毛 🪶
# 说明: 自动化配置 4 个独立 Agent 的完整环境
# =============================================================================

set -e  # 遇到错误立即退出

echo "🪶 AI 天团配置脚本"
echo "=================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# 配置参数（根据实际情况修改）
# =============================================================================

# 飞书机器人凭证 - 需要在飞书开放平台创建4个应用后填入
COPY_APP_ID="cli_a91d4791de389cbd"           # 白色小羽毛
COPY_APP_SECRET="Wgv3Sp2k65LIeYlKkq5qGgGKzqZ4KaZh"

PRODUCT_APP_ID="cli_a912b5791bb89cc0"     # 紫色小羽毛
PRODUCT_APP_SECRET="6QbxdVtgu8mtoIIi4uDKVc1uXRJmlotl"

DESIGN_APP_ID="cli_a912b73dfdf8dcd4"       # 金色小羽毛
DESIGN_APP_SECRET="yztp3jTwl37NcaXDl1HRDfCQgSmYtSZq"

DEV_APP_ID="cli_a912b30db9e15cb5"             # 蓝色小羽毛
DEV_APP_SECRET="9nd5CxusIcbSVHc2Bgx4UcrMfl7T3M7f"

# 模型配置
COPY_MODEL="google/gemini-3.1-pro-preview"
PRODUCT_MODEL="anthropic/claude-opus-4.6"
DESIGN_MODEL="google/gemini-3.1-pro-preview"
DEV_MODEL="kimi-coding/k2p5"

# Gateway 端口
COPY_PORT=18782
PRODUCT_PORT=18810
DESIGN_PORT=18820
DEV_PORT=18830

# =============================================================================
# 检查依赖
# =============================================================================

echo "🔍 检查依赖..."

if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ 错误: openclaw 未安装${NC}"
    echo "请先安装 OpenClaw: https://docs.openclaw.ai"
    exit 1
fi

echo -e "${GREEN}✅ openclaw 已安装${NC}"

# =============================================================================
# 创建目录结构
# =============================================================================

echo ""
echo "📁 创建目录结构..."

AGENTS=("copy" "product" "design" "dev")
PORTS=($COPY_PORT $PRODUCT_PORT $DESIGN_PORT $DEV_PORT)

for i in "${!AGENTS[@]}"; do
    AGENT="${AGENTS[$i]}"
    PORT="${PORTS[$i]}"
    
    mkdir -p ~/.openclaw-${AGENT}-agent/{agent,sessions,workspace}
    mkdir -p ~/.openclaw-${AGENT}-agent/workspace/{projects,assets,docs}
    
    echo -e "${GREEN}✅${NC} 创建 ~/.openclaw-${AGENT}-agent/ (端口: ${PORT})"
done

# =============================================================================
# 生成配置文件
# =============================================================================

echo ""
echo "⚙️  生成配置文件..."

# --- copy-agent 配置 ---
cat > ~/.openclaw-copy-agent/openclaw.json << 'COPYEOF'
{
  "meta": {
    "name": "AI天团-白色小羽毛",
    "version": "2.0",
    "description": "文案高手、策划天才、提示词大师"
  },
  "auth": {
    "profiles": {
      "google:default": {
        "provider": "google",
        "mode": "api_key"
      },
      "kimi-coding:default": {
        "provider": "kimi-coding",
        "mode": "api_key"
      }
    }
  },
  "gateway": {
    "port": 18782,
    "mode": "local",
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:18782",
        "http://127.0.0.1:18782"
      ]
    },
    "auth": {
      "mode": "token",
      "token": "d994033b42daa67a3b437f6bfe436d041d95729718de260b"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "pairing",
      "domain": "feishu",
      "accounts": {
        "main": {
          "appId": "cli_a91d4791de389cbd",
          "appSecret": "Wgv3Sp2k65LIeYlKkq5qGgGKzqZ4KaZh",
          "botName": "白色小羽毛",
          "enabled": true
        }
      },
      "groupPolicy": "open",
      "connectionMode": "websocket",
      "requireMention": true,
      "streaming": true,
      "blockStreaming": true,
      "replyToMode": "all"
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3.1-pro-preview",
        "fallbacks": [
          "google/gemini-3-pro-preview",
          "kimi-coding/k2p5"
        ]
      },
      "thinking": "high",
      "workspace": "~/.openclaw-copy-agent/workspace",
      "agentDir": "~/.openclaw-copy-agent/agent",
      "compaction": {
        "mode": "safeguard"
      },
      "maxConcurrent": 4,
      "subagents": {
        "model": "google/gemini-3-flash-preview",
        "thinking": "low",
        "maxConcurrent": 8
      }
    }
  },
  "tools": {
    "subagents": {
      "tools": {
        "allow": [
          "read",
          "write",
          "edit",
          "web_search",
          "web_fetch"
        ],
        "deny": [
          "exec",
          "process"
        ]
      }
    }
  }
}
COPYEOF

# --- product-agent 配置 ---
cat > ~/.openclaw-product-agent/openclaw.json << 'PRODUCTEOF'
{
  "meta": {
    "name": "AI天团-紫色小羽毛",
    "version": "2.0",
    "description": "产品策划与分析、PRD 规划与管理"
  },
  "auth": {
    "profiles": {
      "google:default": {
        "provider": "google",
        "mode": "api_key"
      },
      "kimi-coding:default": {
        "provider": "kimi-coding",
        "mode": "api_key"
      },
      "anthropic:default": {
        "provider": "anthropic",
        "mode": "token"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4.6",
        "fallbacks": [
          "google/gemini-3-pro-preview",
          "kimi-coding/k2p5"
        ]
      },
      "workspace": "/Users/ifai_macpro/.openclaw-product-agent/workspace",
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "1h"
      },
      "compaction": {
        "mode": "safeguard"
      },
      "heartbeat": {
        "every": "2h"
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 6,
        "model": "anthropic/claude-sonnet-4.6"
      }
    }
  },
  "messages": {
    "ackReactionScope": "group-mentions"
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a912b5791bb89cc0",
      "appSecret": "6QbxdVtgu8mtoIIi4uDKVc1uXRJmlotl",
      "domain": "feishu",
      "groupPolicy": "open",
      "requireMention": false,
      "dmPolicy": "open"
    }
  },
  "gateway": {
    "port": 18810,
    "mode": "local",
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:18810",
        "http://127.0.0.1:18810"
      ]
    },
    "auth": {
      "mode": "token",
      "token": "2772a6e1e021649d913483a2d4fe06a036498d13a62b9131"
    }
  },
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  }
}
PRODUCTEOF

# --- design-agent 配置 ---
cat > ~/.openclaw-design-agent/openclaw.json << 'DESIGNEOF'
{
  "meta": {
    "name": "AI天团-金色小羽毛",
    "version": "2.0",
    "description": "UI/UX设计专家、视觉规范制定"
  },
  "auth": {
    "profiles": {
      "google:default": {
        "provider": "google",
        "mode": "api_key"
      },
      "kimi-coding:default": {
        "provider": "kimi-coding",
        "mode": "api_key"
      },
      "anthropic:default": {
        "provider": "anthropic",
        "mode": "token"
      }
    }
  },
  "gateway": {
    "port": 18820,
    "mode": "local",
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:18820",
        "http://127.0.0.1:18820"
      ]
    },
    "auth": {
      "mode": "token",
      "token": "712bf56a2034d45fc6298bb95174bdd1906e9de63141d95c"
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "pairing",
      "domain": "feishu",
      "accounts": {
        "main": {
          "appId": "cli_a912b73dfdf8dcd4",
          "appSecret": "yztp3jTwl37NcaXDl1HRDfCQgSmYtSZq",
          "botName": "金色小羽毛",
          "enabled": true
        }
      },
      "groupPolicy": "open",
      "connectionMode": "websocket",
      "requireMention": true,
      "streaming": true,
      "blockStreaming": true
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3.1-pro-preview",
        "fallbacks": [
          "anthropic/claude-opus-4.6",
          "kimi-coding/k2p5"
        ] 
      },
      "thinking": "high",
      "workspace": "~/.openclaw-design-agent/workspace",
      "agentDir": "~/.openclaw-design-agent/agent",
      "compaction": {
        "mode": "safeguard"
      },
      "maxConcurrent": 4,
      "subagents": {
        "model": "google/gemini-3-pro-preview",
        "thinking": "medium",
        "maxConcurrent": 6
      }
    }
  }
}
DESIGNEOF

# --- dev-agent 配置 ---
cat > ~/.openclaw-dev-agent/openclaw.json << 'DEVEOF'
{
  "meta": {
    "lastTouchedVersion": "2026.3.2",
    "lastTouchedAt": "2026-03-03T12:31:11.089Z"
  },
  "auth": {
    "profiles": {
      "google:default": {
        "provider": "google",
        "mode": "api_key"
      },
      "kimi-coding:default": {
        "provider": "kimi-coding",
        "mode": "api_key"
      },
      "anthropic:default": {
        "provider": "anthropic",
        "mode": "token"
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5",
        "fallbacks": [
          "anthropic/claude-opus-4.6",
          "google/gemini-3-pro-preview"
        ]
      },
      "workspace": "/Users/ifai_macpro/.openclaw-dev-agent/workspace",
      "contextPruning": {
        "mode": "cache-ttl",
        "ttl": "1h"
      },
      "compaction": {
        "mode": "safeguard"
      },
      "heartbeat": {
        "every": "2h"
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8,
        "model": "anthropic/claude-sonnet-4.6"
      }
    }
  },
  "tools": {
    "subagents": {
      "tools": {
        "allow": [
          "*"
        ],
        "deny": []
      }
    }
  },
  "messages": {
    "ackReactionScope": "group-mentions"
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_a912b30db9e15cb5",
      "appSecret": "9nd5CxusIcbSVHc2Bgx4UcrMfl7T3M7f",
      "domain": "feishu",
      "groupPolicy": "open",
      "requireMention": false,
      "dmPolicy": "open"
    }
  },
  "gateway": {
    "port": 18830,
    "mode": "local",
    "bind": "lan",
    "controlUi": {
      "allowedOrigins": [
        "http://localhost:18830",
        "http://127.0.0.1:18830"
      ]
    },
    "auth": {
      "mode": "token",
      "token": "137bb16847e5e6d434c6a6da84f86c93eea1f85e6032dc17"
    }
  },
  "plugins": {
    "entries": {
      "feishu": {
        "enabled": true
      }
    }
  }
}
DEVEOF

echo -e "${GREEN}✅${NC} 配置文件生成完成"

# =============================================================================
# 生成启动脚本
# =============================================================================

echo ""
echo "🚀 生成启动脚本..."

# 启动所有 Gateway
cat > ~/ai-team-start.sh << 'STARTEOF'
#!/bin/bash
# AI 天团 - 启动所有 Gateway

echo "🪶 启动 AI 天团..."
echo ""

# 检查端口占用
check_port() {
    if lsof -i:$1 > /dev/null 2>&1; then
        echo "⚠️  端口 $1 已被占用"
        return 1
    fi
    return 0
}

# 启动 copy-agent (白色小羽毛)
if check_port 18782; then
    echo "📝 启动 白色小羽毛 (copy-agent) - 端口 18782"
    nohup openclaw --profile copy-agent gateway run --port 18782 > ~/.openclaw-copy-agent/gateway.log 2>&1 &
    sleep 2
fi

# 启动 product-agent (紫色小羽毛)
if check_port 18810; then
    echo "📊 启动 紫色小羽毛 (product-agent) - 端口 18810"
    nohup openclaw --profile product-agent gateway run --port 18810 > ~/.openclaw-product-agent/gateway.log 2>&1 &
    sleep 2
fi

# 启动 design-agent (金色小羽毛)
if check_port 18820; then
    echo "🎨 启动 金色小羽毛 (design-agent) - 端口 18820"
    nohup openclaw --profile design-agent gateway run --port 18820 > ~/.openclaw-design-agent/gateway.log 2>&1 &
    sleep 2
fi

# 启动 dev-agent (蓝色小羽毛)
if check_port 18830; then
    echo "💻 启动 蓝色小羽毛 (dev-agent) - 端口 18830"
    nohup openclaw --profile dev-agent gateway run --port 18830 > ~/.openclaw-dev-agent/gateway.log 2>&1 &
    sleep 2
fi

echo ""
echo "✅ AI 天团启动完成！"
echo ""
echo "查看状态: ~/ai-team-status.sh"
echo "查看日志: tail -f ~/.openclaw-*/gateway.log"
STARTEOF

# 停止所有 Gateway
cat > ~/ai-team-stop.sh << 'STOPEOF'
#!/bin/bash
# AI 天团 - 停止所有 Gateway

echo "🛑 停止 AI 天团..."

pkill -f "openclaw.*--profile copy-agent" || true
pkill -f "openclaw.*--profile product-agent" || true
pkill -f "openclaw.*--profile design-agent" || true
pkill -f "openclaw.*--profile dev-agent" || true

echo "✅ AI 天团已停止"
STOPEOF

# 查看状态
cat > ~/ai-team-status.sh << 'STATUSEOF'
#!/bin/bash
# AI 天团 - 查看状态

echo "🪶 AI 天团状态"
echo "=============="
echo ""

check_agent() {
    local name=$1
    local color=$2
    local port=$3
    
    if lsof -i:$port > /dev/null 2>&1; then
        pid=$(lsof -i:$port | grep LISTEN | awk '{print $2}' | head -1)
        echo -e "✅ ${color}${name}${NC} - 端口 ${port} - PID: ${pid}"
    else
        echo -e "❌ ${color}${name}${NC} - 端口 ${port} - 未运行"
    fi
}

check_agent "白色小羽毛" "📝" 18782
check_agent "紫色小羽毛" "📊" 18810
check_agent "金色小羽毛" "🎨" 18820
check_agent "蓝色小羽毛" "💻" 18830

echo ""
echo "查看配对请求:"
echo "  openclaw --profile copy-agent pairing list feishu"
echo "  openclaw --profile product-agent pairing list feishu"
echo "  openclaw --profile design-agent pairing list feishu"
echo "  openclaw --profile dev-agent pairing list feishu"
STATUSEOF

chmod +x ~/ai-team-*.sh

echo -e "${GREEN}✅${NC} 启动脚本生成完成"
echo "  - ~/ai-team-start.sh   (启动所有)"
echo "  - ~/ai-team-stop.sh    (停止所有)"
echo "  - ~/ai-team-status.sh  (查看状态)"

# =============================================================================
# 输出配置清单
# =============================================================================

echo ""
echo "📋 配置清单"
echo "=========="
echo ""
echo "请在飞书开放平台创建4个应用，并替换配置文件中的凭证："
echo ""
echo "1️⃣  白色小羽毛 (copy-agent)"
echo "    端口: 18782"
echo "    模型: Gemini-3.1-pro-preview"
echo "    配置: ~/.openclaw-copy-agent/openclaw.json"
echo ""
echo "2️⃣  紫色小羽毛 (product-agent)"
echo "    端口: 18810"
echo "    模型: Claude Opus 4.6"
echo "    配置: ~/.openclaw-product-agent/openclaw.json"
echo ""
echo "3️⃣  金色小羽毛 (design-agent)"
echo "    端口: 18820"
echo "    模型: Gemini-3.1-pro-preview"
echo "    配置: ~/.openclaw-design-agent/openclaw.json"
echo ""
echo "4️⃣  蓝色小羽毛 (dev-agent)"
echo "    端口: 18830"
echo "    模型: Kimi K2.5"
echo "    配置: ~/.openclaw-dev-agent/openclaw.json"
echo ""

# =============================================================================
# 后续步骤
# =============================================================================

echo "🎯 后续步骤"
echo "=========="
echo ""
echo "1. 在飞书开放平台创建4个企业自建应用"
echo "   https://open.feishu.cn/app"
echo ""
echo "2. 获取每个应用的 App ID 和 App Secret"
echo ""
echo "3. 编辑配置文件，填入凭证："
echo "   vim ~/.openclaw-copy-agent/openclaw.json"
echo "   vim ~/.openclaw-product-agent/openclaw.json"
echo "   vim ~/.openclaw-design-agent/openclaw.json"
echo "   vim ~/.openclaw-dev-agent/openclaw.json"
echo ""
echo "4. 配置每个飞书应用："
echo "   - 启用机器人能力"
echo "   - 事件订阅 → 长连接模式"
echo "   - 权限: im:message:send_as_bot 等"
echo ""
echo "5. 启动 AI 天团："
echo "   ~/ai-team-start.sh"
echo ""
echo "6. 在飞书中搜索各机器人，私聊测试"
echo ""
echo "7. 批准配对请求："
echo "   ~/ai-team-status.sh"
echo "   openclaw --profile <agent> pairing approve feishu <CODE>"
echo ""

echo -e "${GREEN}🎉 AI 天团配置脚本执行完成！${NC}"
echo ""
