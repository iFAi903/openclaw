#!/bin/bash
# 网页抓取工具 - 方法1: curl + 移动端UA

URL="$1"
OUTPUT="${2:-page.html}"

# 移动端 User-Agent 列表
UA_IPHONE='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
UA_ANDROID='Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
UA_WECHAT='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x18002628) NetType/WIFI Language/zh_CN'

# 尝试不同UA
echo "🌐 抓取: $URL"
echo "📱 尝试 iPhone UA..."
curl -s -L -A "$UA_IPHONE" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: zh-CN,zh;q=0.9" \
  -H "Accept-Encoding: gzip, deflate, br" \
  --compressed \
  --max-time 30 \
  -o "$OUTPUT" \
  "$URL" 2>/dev/null

if [ -s "$OUTPUT" ] && [ $(wc -c < "$OUTPUT") -gt 1000 ]; then
  echo "✅ 成功: $OUTPUT ($(wc -c < "$OUTPUT") bytes)"
  exit 0
fi

echo "📱 尝试 Android UA..."
curl -s -L -A "$UA_ANDROID" \
  --max-time 30 \
  -o "$OUTPUT" \
  "$URL" 2>/dev/null

if [ -s "$OUTPUT" ] && [ $(wc -c < "$OUTPUT") -gt 1000 ]; then
  echo "✅ 成功: $OUTPUT"
  exit 0
fi

echo "📱 尝试微信 UA..."
curl -s -L -A "$UA_WECHAT" \
  --max-time 30 \
  -o "$OUTPUT" \
  "$URL" 2>/dev/null

if [ -s "$OUTPUT" ] && [ $(wc -c < "$OUTPUT") -gt 1000 ]; then
  echo "✅ 成功: $OUTPUT"
  exit 0
fi

echo "❌ curl 方法失败，尝试 Chrome Headless..."
exit 1
