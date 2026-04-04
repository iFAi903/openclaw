#!/bin/bash

# =============================================================================
# 小羽毛 AI 新闻早报 - Cron 任务安装脚本
# =============================================================================

echo "🪶 小羽毛 AI 新闻早报 - 定时任务安装"
echo "========================================"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="0 7 * * * ${SCRIPT_DIR}/daily-cron.sh >> /tmp/xiaoyumao-news-cron.log 2>&1"

echo ""
echo "📋 检查环境..."

# 检查必要命令
command -v python3 >/dev/null 2>&1 && echo "✅ python3" || echo "❌ python3 未安装"
command -v node >/dev/null 2>&1 && echo "✅ node" || echo "❌ node 未安装"
command -v npm >/dev/null 2>&1 && echo "✅ npm" || echo "❌ npm 未安装"
command -v crontab >/dev/null 2>&1 && echo "✅ crontab" || echo "❌ crontab 不可用"

echo ""
echo "📝 Cron 任务配置:"
echo "   执行时间: 每天 07:00 (Asia/Taipei)"
echo "   启动脚本: ${SCRIPT_DIR}/daily-cron.sh"
echo "   内容流水线: ${SCRIPT_DIR}/run-news-pipeline.sh"
echo "   日志文件: /tmp/xiaoyumao-news-cron.log"
echo ""

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "daily-cron.sh"; then
    echo "⚠️  检测到已存在 cron 任务"
    echo ""
    read -p "是否重新安装? (y/n): " REINSTALL
    if [ "$REINSTALL" != "y" ]; then
        echo "已取消"
        exit 0
    fi
    # 删除旧任务
    crontab -l 2>/dev/null | grep -v "daily-cron.sh" | crontab -
fi

echo ""
echo "🔧 安装 cron 任务..."

# 创建临时 crontab 文件
TEMP_CRON=$(mktemp)

# 导出当前 crontab（如果存在）
crontab -l > "$TEMP_CRON" 2>/dev/null || echo "# 新建 crontab" > "$TEMP_CRON"

# 去重：移除旧的同名注释块、SHELL/PATH、任务行
EXISTING_CRON=$(cat "$TEMP_CRON")
printf "%s\n" "$EXISTING_CRON" | \
  grep -v "小羽毛 AI 新闻早报 - 每日 7:00 自动更新" | \
  grep -v "^SHELL=/bin/bash$" | \
  grep -v "^PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:.*\\.npm-global/bin$" | \
  grep -v "daily-cron.sh >> /tmp/xiaoyumao-news-cron.log 2>&1" > "$TEMP_CRON.clean"
mv "$TEMP_CRON.clean" "$TEMP_CRON"

# 添加环境变量和任务
cat >> "$TEMP_CRON" << EOF

# 小羽毛 AI 新闻早报 - 每日 7:00 自动更新
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:$HOME/.npm-global/bin
VERCEL_TOKEN=
$CRON_JOB
EOF

# 安装新的 crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo ""
echo "✅ Cron 任务安装成功!"
echo ""
echo "📊 当前 crontab 内容:"
echo "----------------------------------------"
crontab -l | grep -A 5 "小羽毛"
echo "----------------------------------------"
echo ""
echo "🧪 测试运行:"
echo "   手动执行: ${SCRIPT_DIR}/daily-cron.sh"
echo ""
echo "📜 查看日志:"
echo "   tail -f /tmp/xiaoyumao-news-cron.log"
echo ""
echo "🎉 安装完成! 每日 7:00 将自动更新 AI 新闻早报"
