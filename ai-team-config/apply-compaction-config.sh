#!/bin/bash
# =============================================================================
# AI 天团 - Compaction 配置应用脚本
# 版本: 2.0
# 作者: 小羽毛 🪶
# 说明: 为 4 个 Agent 应用差异化 compaction 配置
# =============================================================================

set -e

echo "🪶 AI 天团 Compaction 配置脚本"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}配置说明:${NC}"
echo "  📝 白色小羽毛 (copy-agent):     periodic, 8 turns, Gemini Flash"
echo "  📊 紫色小羽毛 (product-agent):  periodic, 10 turns, Claude Sonnet"
echo "  🎨 金色小羽毛 (design-agent):   periodic, 8 turns, Gemini Flash"
echo "  💻 蓝色小羽毛 (dev-agent):      safeguard, 80K tokens, 40K reserve"
echo ""

# 检查 openclaw 命令
if ! command -v openclaw &> /dev/null; then
    echo -e "${YELLOW}⚠️ 警告: openclaw 命令未找到，尝试查找...${NC}"
    
    # 尝试常见路径
    if [ -f "$HOME/.npm-global/bin/openclaw" ]; then
        export PATH="$HOME/.npm-global/bin:$PATH"
        echo "  找到: ~/.npm-global/bin/openclaw"
    elif [ -f "/opt/homebrew/bin/openclaw" ]; then
        export PATH="/opt/homebrew/bin:$PATH"
        echo "  找到: /opt/homebrew/bin/openclaw"
    elif [ -f "/usr/local/bin/openclaw" ]; then
        export PATH="/usr/local/bin:$PATH"
        echo "  找到: /usr/local/bin/openclaw"
    else
        echo "❌ 错误: 未找到 openclaw 命令"
        echo "请确保 openclaw 已安装并在 PATH 中"
        exit 1
    fi
fi

echo -e "${GREEN}✅ openclaw 命令可用${NC}"
echo ""

# =============================================================================
# 1. 配置白色小羽毛 (copy-agent)
# =============================================================================

echo "📝 配置白色小羽毛 (copy-agent)..."
echo "   模式: periodic, 8 turns, Gemini Pro"

# 创建临时配置文件
COPY_CONFIG=$(cat << 'EOF'
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "periodic",
        "interval": 8,
        "intervalType": "turns",
        "summaryModel": "google/gemini-3-pro-preview",
        "summaryPrompt": "保留文案创作项目的关键信息：\n1. 创作主题、目标受众和传播目标\n2. 已确定的文案风格、调性和品牌声音\n3. 当前文案版本和修改方向\n4. 用户反馈的核心要点\n5. 任何关键的金句或创意概念\n\n对话内容：{{history}}"
      }
    }
  }
}
EOF
)

# 应用配置
CONFIG_FILE="$HOME/.openclaw-copy-agent/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    # 备份原配置
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    
    # 使用 jq 合并配置（如果可用）
    if command -v jq &> /dev/null; then
        jq -s '.[0] * .[1]' "$CONFIG_FILE" <(echo "$COPY_CONFIG") > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    else
        echo "   ${YELLOW}⚠️ jq 未安装，请手动合并配置${NC}"
        echo "$COPY_CONFIG" > "$CONFIG_FILE.compaction.json"
        echo "   配置已保存到: $CONFIG_FILE.compaction.json"
    fi
    echo -e "   ${GREEN}✅ 配置已应用${NC}"
else
    echo -e "   ${YELLOW}⚠️ 配置文件不存在: $CONFIG_FILE${NC}"
    echo "   请先运行 setup-ai-team.sh 创建配置"
fi

echo ""

# =============================================================================
# 2. 配置紫色小羽毛 (product-agent)
# =============================================================================

echo "📊 配置紫色小羽毛 (product-agent)..."
echo "   模式: periodic, 10 turns, Claude Sonnet"

PRODUCT_CONFIG=$(cat << 'EOF'
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "periodic",
        "interval": 10,
        "intervalType": "turns",
        "summaryModel": "anthropic/claude-sonnet-4.6",
        "summaryPrompt": "保留产品策划项目的关键信息：\n1. 产品定位和目标用户画像\n2. 核心需求和痛点分析\n3. 功能优先级和 MVP 范围\n4. 竞品分析的关键洞察\n5. 已做出的产品决策及其理由\n6. 当前进展和待确认事项\n\n对话内容：{{history}}"
      }
    }
  }
}
EOF
)

CONFIG_FILE="$HOME/.openclaw-product-agent/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    
    if command -v jq &> /dev/null; then
        jq -s '.[0] * .[1]' "$CONFIG_FILE" <(echo "$PRODUCT_CONFIG") > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    else
        echo "$PRODUCT_CONFIG" > "$CONFIG_FILE.compaction.json"
        echo "   配置已保存到: $CONFIG_FILE.compaction.json"
    fi
    echo -e "   ${GREEN}✅ 配置已应用${NC}"
else
    echo -e "   ${YELLOW}⚠️ 配置文件不存在: $CONFIG_FILE${NC}"
fi

echo ""

# =============================================================================
# 3. 配置金色小羽毛 (design-agent)
# =============================================================================

echo "🎨 配置金色小羽毛 (design-agent)..."
echo "   模式: periodic, 8 turns, Gemini pro"

DESIGN_CONFIG=$(cat << 'EOF'
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "periodic",
        "interval": 8,
        "intervalType": "turns",
        "summaryModel": "google/gemini-3-pro-preview",
        "summaryPrompt": "保留设计项目的关键信息：\n1. 设计风格方向和视觉调性\n2. 配色方案和设计系统决策\n3. 关键页面的布局和交互设计\n4. 生成的原型图提示词集合\n5. 用户反馈的设计修改方向\n6. 设计规范和组件库定义\n\n对话内容：{{history}}"
      }
    }
  }
}
EOF
)

CONFIG_FILE="$HOME/.openclaw-design-agent/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    
    if command -v jq &> /dev/null; then
        jq -s '.[0] * .[1]' "$CONFIG_FILE" <(echo "$DESIGN_CONFIG") > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    else
        echo "$DESIGN_CONFIG" > "$CONFIG_FILE.compaction.json"
        echo "   配置已保存到: $CONFIG_FILE.compaction.json"
    fi
    echo -e "   ${GREEN}✅ 配置已应用${NC}"
else
    echo -e "   ${YELLOW}⚠️ 配置文件不存在: $CONFIG_FILE${NC}"
fi

echo ""

# =============================================================================
# 4. 配置蓝色小羽毛 (dev-agent)
# =============================================================================

echo "💻 配置蓝色小羽毛 (dev-agent)..."
echo "   模式: safeguard, 80K tokens, 40K reserve"

DEV_CONFIG=$(cat << 'EOF'
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "thresholdTokens": 80000,
        "reserveTokens": 40000,
        "summaryModel": "google/gemini-3-pro-preview",
        "summaryPrompt": "保留开发项目的核心技术信息：\n1. 技术栈和架构设计决策\n2. 当前实现的功能模块和代码位置\n3. 遇到的关键 Bug 和解决方案\n4. 技术债务和待优化事项\n5. 下一步开发计划和优先级\n\n对话内容：{{history}}"
      }
    }
  }
}
EOF
)

CONFIG_FILE="$HOME/.openclaw-dev-agent/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    
    if command -v jq &> /dev/null; then
        jq -s '.[0] * .[1]' "$CONFIG_FILE" <(echo "$DEV_CONFIG") > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    else
        echo "$DEV_CONFIG" > "$CONFIG_FILE.compaction.json"
        echo "   配置已保存到: $CONFIG_FILE.compaction.json"
    fi
    echo -e "   ${GREEN}✅ 配置已应用${NC}"
else
    echo -e "   ${YELLOW}⚠️ 配置文件不存在: $CONFIG_FILE${NC}"
fi

echo ""

# =============================================================================
# 5. 复制更新后的 TOOLS.md
# =============================================================================

echo "📁 更新 Agent 工具配置..."

# 更新 design-agent TOOLS.md
if [ -f "$HOME/.openclaw/workspace/ai-team-config/design-agent/TOOLS.md" ]; then
    cp "$HOME/.openclaw/workspace/ai-team-config/design-agent/TOOLS.md" "$HOME/.openclaw-design-agent/agent/TOOLS.md"
    echo -e "   ${GREEN}✅ design-agent TOOLS.md 已更新${NC}"
    echo "      变更: 移除 canvas, 添加 Stitch/Pensil 工具选择"
fi

# 更新 dev-agent TOOLS.md
if [ -f "$HOME/.openclaw/workspace/ai-team-config/dev-agent/TOOLS.md" ]; then
    cp "$HOME/.openclaw/workspace/ai-team-config/dev-agent/TOOLS.md" "$HOME/.openclaw-dev-agent/agent/TOOLS.md"
    echo -e "   ${GREEN}✅ dev-agent TOOLS.md 已更新${NC}"
    echo "      变更: 添加 Vibe Coding 工具选择决策 (Claude Code/OpenCode/Antigravity/Codex)"
fi

echo ""

# =============================================================================
# 6. 完成提示
# =============================================================================

echo -e "${GREEN}🎉 AI 天团 Compaction 配置完成！${NC}"
echo ""
echo "配置摘要:"
echo "  📝 白色小羽毛: periodic, 8 turns, Gemini pro"
echo "  📊 紫色小羽毛: periodic, 10 turns, Claude Sonnet"
echo "  🎨 金色小羽毛: periodic, 8 turns, Gemini pro"
echo "  💻 蓝色小羽毛: safeguard, 80K tokens, 40K reserve"
echo ""
echo -e "${YELLOW}⚠️  请重启 Gateway 使配置生效:${NC}"
echo "   ~/ai-team-stop.sh"
echo "   ~/ai-team-start.sh"
echo ""
echo "验证配置:"
echo "   openclaw --profile copy-agent config get agents.defaults.compaction.mode"
echo "   openclaw --profile dev-agent config get agents.defaults.compaction.mode"
echo ""
