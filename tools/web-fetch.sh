#!/bin/bash
# 网页反爬抓取主脚本 - 自动按顺序尝试所有方法
# 使用方法: ./web-fetch.sh <URL> [output.html]

URL="$1"
OUTPUT="${2:-page.html}"
TOOL_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$URL" ]; then
  echo "❌ 用法: $0 <URL> [output.html]"
  exit 1
fi

echo "🪶 小羽毛网页抓取工具"
echo "======================"
echo "目标: $URL"
echo "输出: $OUTPUT"
echo ""

# 方法1: curl + 移动端UA
echo "【方法1/3】curl + 移动端UA..."
if bash "$TOOL_DIR/web-fetch-curl.sh" "$URL" "$OUTPUT"; then
  echo "✅ 方法1成功"
  exit 0
fi

# 方法2: Chrome Headless
echo ""
echo "【方法2/3】Chrome Headless..."
if bash "$TOOL_DIR/web-fetch-chrome.sh" "$URL" "$OUTPUT"; then
  echo "✅ 方法2成功"
  exit 0
fi

# 方法3: Chrome Remote Debugging（需要手动启动Chrome）
echo ""
echo "【方法3/3】Chrome Remote Debugging..."
echo "⚠️  需要手动启动 Chrome 调试模式:"
echo "   /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug"
echo ""

# 检查 Chrome Remote Debugging 是否可用
if curl -s http://localhost:9222/json/version >/dev/null 2>&1; then
  echo "🌐 Chrome Remote Debugging 可用，正在抓取..."
  
  # 创建新页面
  PAGE_INFO=$(curl -s -X PUT http://localhost:9222/json/new?about:blank)
  WEBSOCKET_URL=$(echo "$PAGE_INFO" | grep -o '"webSocketDebuggerUrl":"[^"]*"' | cut -d'"' -f4)
  
  if [ -n "$WEBSOCKET_URL" ]; then
    echo "✅ 已连接到 Chrome Remote Debugging"
    echo "⚠️  方法3需要更复杂的 WebSocket 通信，建议使用 Puppeteer/Playwright"
    echo "   这里仅做演示，实际使用请调用 node scripts"
  fi
else
  echo "❌ Chrome Remote Debugging 未启动"
fi

echo ""
echo "❌ 所有方法均失败"
echo "建议:"
echo "  1. 检查网络连接"
echo "  2. 确认目标网站可访问"
echo "  3. 手动启动 Chrome 调试模式尝试方法3"
exit 1
