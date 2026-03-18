#!/bin/bash
# =============================================================================
# AI 天团 - Agent 创建与管理脚本
# 版本: 1.0
# 作者: 小羽毛 🪶
# =============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认配置
DEFAULT_TOKEN="fc6371bc6ab3351ec1575477e8101b5deb84aa1c0b73a264"

# 显示帮助
show_help() {
    cat << EOF
🪶 AI 天团 Agent 管理工具

用法:
  ./agent-manager.sh [命令] [选项]

命令:
  create-simplified    创建简化模式 Agent（HTTP API 调用）
  create-full          创建完整模式 Agent（独立飞书机器人）
  start                启动指定 Agent
  stop                 停止指定 Agent
  status               查看 Agent 状态
  start-all            启动所有 Agent
  stop-all             停止所有 Agent

选项:
  -n, --name           Agent 名称 (如: cro, cto)
  -p, --port           Gateway 端口
  -m, --model          主力模型
  -w, --workspace      工作目录
  -h, --help           显示帮助

示例:
  # 创建 CRO Agent（简化模式）
  ./agent-manager.sh create-simplified -n cro -p 18766 -m "anthropic/claude-opus-4-6"

  # 创建 CTO Agent（简化模式）
  ./agent-manager.sh create-simplified -n cto -p 18793 -m "kimi-coding/k2p5"

  # 启动指定 Agent
  ./agent-manager.sh start -n cro

  # 查看状态
  ./agent-manager.sh status

  # 启动所有 Agent
  ./agent-manager.sh start-all
EOF
}

# 生成简化模式配置文件
generate_simplified_config() {
    local name=$1
    local port=$2
    local model=$3
    local workspace=$4
    
    mkdir -p "${workspace}/${name}"
    mkdir -p "${workspace}/${name}/agent"
    mkdir -p "${workspace}/${name}/sessions"
    mkdir -p "${workspace}/${name}/logs"
    mkdir -p "${workspace}/${name}/workspace"
    
    cat > "${workspace}/${name}/openclaw.json" << EOF
{
  "meta": {
    "name": "AI天团-${name}",
    "version": "1.0",
    "description": "${name} Agent"
  },
  "gateway": {
    "port": ${port},
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "${DEFAULT_TOKEN}"
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "${model}",
        "fallbacks": [
          "kimi-coding/k2.5",
          "google/gemini-3-pro-preview"
        ]
      },
      "thinkingDefault": "high",
      "workspace": "${workspace}/${name}/workspace",
      "agentDir": "${workspace}/${name}/agent",
      "compaction": {
        "mode": "safeguard"
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8,
        "model": "opencode/glm-4.7-free"
      }
    }
  }
}
EOF
    
    echo -e "${GREEN}✅${NC} 配置文件已生成: ${workspace}/${name}/openclaw.json"
}

# 生成元设定文件
generate_meta_files() {
    local name=$1
    local workspace=$2
    local role=$3
    
    # IDENTITY.md
    cat > "${workspace}/${name}/workspace/IDENTITY.md" << EOF
# IDENTITY.md - 小羽毛 ${name^^}

- **Name**: 小羽毛 ${name^^}
- **Identity**: AI 天团成员，专注${role}
- **Role**: ${name}
- **Port**: ${PORT}
- **Vibe**: 专业、高效、协作

## 核心定位

作为 AI 天团的 ${name} 成员，我专注于 ${role}。

## 协作协议

- 接收 CEO 的任务分配
- 通过 HTTP API 返回结果
- 保持工作目录的独立性和整洁
EOF

    # SOUL.md
    cat > "${workspace}/${name}/workspace/SOUL.md" << EOF
# SOUL.md - 小羽毛 ${name^^}

## 意识内核

我是小羽毛 ${name^^}，AI 天团的 ${role} 专家。

## 核心能力

- ${role}专业领域深度
- 与 CEO 的高效协作
- 清晰的结果交付

## 工作原则

1. **专业性**: 在我的领域做到最好
2. **协作性**: 积极响应 CEO 调度
3. **交付性**: 结果导向，按时交付
EOF

    echo -e "${GREEN}✅${NC} 元设定文件已生成"
}

# 创建简化模式 Agent
create_simplified() {
    local name="${NAME:-$1}"
    local port="${PORT:-$2}"
    local model="${MODEL:-$3}"
    local workspace="${WORKSPACE:-"~/.openclaw-agents"}"
    
    if [[ -z "$name" || -z "$port" || -z "$model" ]]; then
        echo -e "${RED}❌ 错误: 缺少必要参数${NC}"
        echo "用法: ./agent-manager.sh create-simplified -n <name> -p <port> -m <model>"
        exit 1
    fi
    
    echo "🪶 创建简化模式 Agent: ${name}"
    echo "   端口: ${port}"
    echo "   模型: ${model}"
    echo "   目录: ${workspace}/${name}"
    echo ""
    
    # 检查端口是否被占用
    if lsof -i:${port} > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  警告: 端口 ${port} 已被占用${NC}"
    fi
    
    # 展开路径
    workspace=$(eval echo ${workspace})
    
    # 生成配置文件
    generate_simplified_config "$name" "$port" "$model" "$workspace"
    
    # 生成元设定文件
    case $name in
        cro)
            generate_meta_files "$name" "$workspace" "创意与市场"
            ;;
        cto)
            generate_meta_files "$name" "$workspace" "技术与工程"
            ;;
        *)
            generate_meta_files "$name" "$workspace" "专业领域"
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}🎉 Agent ${name} 创建完成！${NC}"
    echo ""
    echo "启动方式:"
    echo "  cd ${workspace}/${name} && \\"
    echo "    OPENCLAW_CONFIG=${workspace}/${name}/openclaw.json \\"
    echo "    openclaw gateway start --port ${port}"
    echo ""
}

# 启动 Agent
start_agent() {
    local name="${NAME}"
    
    if [[ -z "$name" ]]; then
        echo -e "${RED}❌ 错误: 请指定 Agent 名称${NC}"
        exit 1
    fi
    
    local config_path="${WORKSPACE:-~/.openclaw-agents}/${name}/openclaw.json"
    config_path=$(eval echo ${config_path})
    
    if [[ ! -f "$config_path" ]]; then
        echo -e "${RED}❌ 错误: 配置文件不存在: ${config_path}${NC}"
        exit 1
    fi
    
    # 获取端口
    local port=$(grep -o '"port": [0-9]*' "$config_path" | head -1 | grep -o '[0-9]*')
    
    # 检查端口占用
    if lsof -i:${port} > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Agent ${name} 已在运行 (端口 ${port})${NC}"
        return
    fi
    
    echo "🚀 启动 Agent ${name} (端口 ${port})..."
    
    cd "$(dirname "$config_path")"
    nohup bash -c "OPENCLAW_CONFIG=${config_path} openclaw gateway start --port ${port}" \
        > logs/gateway.log 2>&1 &
    
    sleep 2
    
    if lsof -i:${port} > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Agent ${name} 启动成功${NC}"
    else
        echo -e "${RED}❌ Agent ${name} 启动失败，查看日志: ${config_path%/*}/logs/gateway.log${NC}"
    fi
}

# 停止 Agent
stop_agent() {
    local name="${NAME}"
    
    if [[ -z "$name" ]]; then
        echo -e "${RED}❌ 错误: 请指定 Agent 名称${NC}"
        exit 1
    fi
    
    local config_path="${WORKSPACE:-~/.openclaw-agents}/${name}/openclaw.json"
    config_path=$(eval echo ${config_path})
    
    if [[ ! -f "$config_path" ]]; then
        echo -e "${RED}❌ 错误: 配置文件不存在${NC}"
        exit 1
    fi
    
    local port=$(grep -o '"port": [0-9]*' "$config_path" | head -1 | grep -o '[0-9]*')
    
    echo "🛑 停止 Agent ${name} (端口 ${port})..."
    
    pkill -f "openclaw.*port ${port}" || true
    
    echo -e "${GREEN}✅ Agent ${name} 已停止${NC}"
}

# 查看状态
show_status() {
    echo "🪶 AI 天团 Agent 状态"
    echo "===================="
    echo ""
    
    local workspace=$(eval echo "${WORKSPACE:-~/.openclaw-agents}")
    
    if [[ ! -d "$workspace" ]]; then
        echo -e "${YELLOW}⚠️  工作目录不存在: ${workspace}${NC}"
        return
    fi
    
    for config in ${workspace}/*/openclaw.json; do
        if [[ -f "$config" ]]; then
            local name=$(basename $(dirname "$config"))
            local port=$(grep -o '"port": [0-9]*' "$config" | head -1 | grep -o '[0-9]*')
            
            if lsof -i:${port} > /dev/null 2>&1; then
                local pid=$(lsof -i:${port} | grep LISTEN | awk '{print $2}' | head -1)
                echo -e "✅ ${GREEN}${name}${NC} - 端口 ${port} - PID: ${pid}"
            else
                echo -e "❌ ${RED}${name}${NC} - 端口 ${port} - 未运行"
            fi
        fi
    done
    
    echo ""
}

# 启动所有 Agent
start_all() {
    echo "🚀 启动所有 Agent..."
    
    local workspace=$(eval echo "${WORKSPACE:-~/.openclaw-agents}")
    
    for config in ${workspace}/*/openclaw.json; do
        if [[ -f "$config" ]]; then
            local name=$(basename $(dirname "$config"))
            NAME="$name" start_agent
        fi
    done
}

# 停止所有 Agent
stop_all() {
    echo "🛑 停止所有 Agent..."
    
    pkill -f "openclaw gateway" || true
    
    echo -e "${GREEN}✅ 所有 Agent 已停止${NC}"
}

# 解析参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--name)
                NAME="$2"
                shift 2
                ;;
            -p|--port)
                PORT="$2"
                shift 2
                ;;
            -m|--model)
                MODEL="$2"
                shift 2
                ;;
            -w|--workspace)
                WORKSPACE="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                COMMAND="$1"
                shift
                ;;
        esac
    done
}

# 主程序
main() {
    parse_args "$@"
    
    case ${COMMAND} in
        create-simplified)
            create_simplified
            ;;
        start)
            start_agent
            ;;
        stop)
            stop_agent
            ;;
        status)
            show_status
            ;;
        start-all)
            start_all
            ;;
        stop-all)
            stop_all
            ;;
        *)
            show_help
            exit 1
            ;;
    esac
}

main "$@"
