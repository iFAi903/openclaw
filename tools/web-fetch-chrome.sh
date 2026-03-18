#!/bin/bash
# 网页抓取工具 - 方法2: Chrome Headless dump-dom

URL="$1"
OUTPUT="${2:-page.html}"

echo "🖥️  使用 Chrome Headless 渲染: $URL"

# 检查 Chrome/Edge 可用
CHROME_BIN=""
for bin in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
           "google-chrome" \
           "chromium"; do
  if command -v "$bin" >/dev/null 2>&1 || [ -x "$bin" ]; then
    CHROME_BIN="$bin"
    break
  fi
done

if [ -z "$CHROME_BIN" ]; then
  echo "❌ Chrome/Edge 未找到"
  exit 1
fi

echo "🌐 使用: $CHROME_BIN"

# Chrome Headless 抓取
"$CHROME_BIN" \
  --headless \
  --disable-gpu \
  --no-sandbox \
  --disable-setuid-sandbox \
  --disable-dev-shm-usage \
  --disable-accelerated-2d-canvas \
  --disable-accelerated-jpeg-decoding \
  --disable-accelerated-mjpeg-decode \
  --disable-accelerated-video-decode \
  --disable-extensions \
  --disable-default-apps \
  --mute-audio \
  --no-first-run \
  --memory-model=low \
  --max_old_space_size=512 \
  --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  --dump-dom \
  --virtual-time-budget=10000 \
  --run-all-compositor-stages-before-draw \
  "$URL" > "$OUTPUT" 2>/dev/null

if [ -s "$OUTPUT" ] && [ $(wc -c < "$OUTPUT") -gt 1000 ]; then
  echo "✅ 成功: $OUTPUT ($(wc -c < "$OUTPUT") bytes)"
  exit 0
else
  echo "❌ Chrome Headless 失败"
  exit 1
fi
