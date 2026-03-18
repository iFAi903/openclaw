#!/bin/bash

# =============================================================================
# 小羽毛 AI 天团 - Agent 启动脚本
# 启动所有 AI 天团成员
# =============================================================================

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Agent 配置数组
# 格式: 名称:目录:端口:颜色代码
AGENTS=(
    "copy-agent:/Users/ifai_macpro/.openclaw/workspace/iFAi/ai-team-config/copy-agent:18870:$BLUE"
    "product-agent:/Users/ifai_macpro/.openclaw/workspace/iFAi/ai-team-config/product-agent:18880:$PURPLE"
    "design-agent:/Users/ifai_macpro/.openclaw/workspace/iFAi/ai-team-config/design-agent:18860:$YELLOW"
    "coo-agent:/Users/ifai_macpro/.openclaw/workspace/iFAi/ai-team-config/coo-agent:18840:$GREEN"
    "cfo-agent:/Users/ifai_macpro/.openclaw/workspace/iFAi/ai-team-config/cfo-agent:18850:$CYAN"
)

echo -e "${GREEN}"
echo "🪶 小羽毛 AI 天团 - Agent 启动器"
echo "========================================"
echo -e "${NC}"

# 函数：启动单个 agent
start_agent() {
    local name=$1
    local dir=$2
    local port=$3
    local color=$4
    
    echo -e "${color}▶ 启动 ${name}...${NC}"
    
    # 检查目录
    if [ ! -d "$dir" ]; then
        echo -e "${RED}  ✗ 目录不存在: $dir${NC}"
        return 1
    fi
    
    # 检查配置文件
    if [ ! -f "$dir/openclaw.json" ]; then
        echo -e "${RED}  ✗ 配置文件不存在: $dir/openclaw.json${NC}"
        return 1
    fi
    
    # 检查端口是否被占用
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}  ⚠ 端口 $port 已被占用，${name} 可能已在运行${NC}"
        return 0
    fi
    
    # 启动 agent
    cd "$dir"
    nohup openclaw gateway start --config "$dir/openclaw.json" > /tmp/${name}.log 2>&1 &
    
    # 等待启动
    sleep 2
    
    # 验证启动
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓ ${name} 已启动 (端口: $port)${NC}"
        return 0
    else
        echo -e "${RED}  ✗ ${name} 启动失败，查看日志: /tmp/${name}.log${NC}"
        return 1
    fi
}

# 函数：停止 agent
stop_agent() {
    local name=$1
    local port=$2
    local color=$3
    
    echo -e "${color}▶ 停止 ${name}...${NC}"
    
    # 查找并终止进程
    local pid=$(lsof -Pi :$port -sTCP:LISTEN -t 2>/dev/null)
    if [ -n "$pid" ]; then
        kill $pid 2>/dev/null
        sleep 1
        echo -e "${GREEN}  ✓ ${name} 已停止${NC}"
    else
        echo -e "${YELLOW}  ⚠ ${name} 未在运行${NC}"
    fi
}

# 函数：检查状态
check_status() {
    echo -e "${BLUE}"
    echo "📊 AI 天团 Agent 状态"
    echo "========================================"
    echo -e "${NC}"
    
    local running=0
    local total=${#AGENTS[@]}
    
    for agent in "${AGENTS[@]}"; do
        IFS=':' read -r name dir port color <<< "$agent"
        local pid=$(lsof -Pi :$port -sTCP:LISTEN -t 2>/dev/null)
        
        if [ -n "$pid" ]; then
            echo -e "${GREEN}●${NC} ${name} - 运行中 (PID: $pid, 端口: $port)"
            ((running++))
        else
            echo -e "${RED}○${NC} ${name} - 未运行 (端口: $port)"
        fi
    done
    
    echo ""
    echo -e "总计: ${running}/${total} 运行中"
}

# 主逻辑
case "${1:-start}" in
    start)
        echo "🚀 启动 AI 天团 Agents..."
        echo ""
        start_agent "copy-agent" "$COPY_AGENT_DIR" "$COPY_AGENT_PORT" "$BLUE"
        start_agent "product-agent" "$PRODUCT_AGENT_DIR" "$PRODUCT_AGENT_PORT" "$PURPLE"
        echo ""
        echo -e "${GREEN}✅ 启动完成！${NC}"
        echo ""
        check_status
        ;;
    
    stop)
        echo "🛑 停止 AI 天团 Agents..."
        echo ""
        stop_agent "copy-agent" "$COPY_AGENT_PORT" "$BLUE"
        stop_agent "product-agent" "$PRODUCT_AGENT_PORT" "$PURPLE"
        echo ""
        echo -e "${GREEN}✅ 已停止${NC}"
        ;;
    
    restart)
        echo "🔄 重启 AI 天团 Agents..."
        echo ""
        stop_agent "copy-agent" "$COPY_AGENT_PORT" "$BLUE"
        stop_agent "product-agent" "$PRODUCT_AGENT_PORT" "$PURPLE"
        sleep 2
        echo ""
        start_agent "copy-agent" "$COPY_AGENT_DIR" "$COPY_AGENT_PORT" "$BLUE"
        start_agent "product-agent" "$PRODUCT_AGENT_DIR" "$PRODUCT_AGENT_PORT" "$PURPLE"
        echo ""
        echo -e "${GREEN}✅ 重启完成！${NC}"
        echo ""
        check_status
        ;;
    
    status)
        check_status
        ;;
    
    logs)
        echo "📜 显示日志 (按 Ctrl+C 退出)..."
        echo "========================================"
        tail -f /tmp/copy-agent.log /tmp/product-agent.log 2>/dev/null
        ;;
    
    *)
        echo "用法: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "命令:"
        echo "  start    - 启动所有 agents"
        echo "  stop     - 停止所有 agents"
        echo "  restart  - 重启所有 agents"
        echo "  status   - 查看运行状态"
        echo "  logs     - 查看实时日志"
        exit 1
        ;;
esac
