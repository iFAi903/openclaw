#!/bin/bash
# 微信公众号文章抓取专用脚本
# 使用方法: ./wechat-fetch.sh <公众号文章URL>

URL="$1"
OUTPUT="${2:-wechat_article.html}"
CONTENT_FILE="${3:-wechat_content.txt}"

if [ -z "$URL" ]; then
  echo "❌ 用法: $0 <微信公众号文章URL> [output.html] [content.txt]"
  echo "示例: $0 'https://mp.weixin.qq.com/s/xxxxx'"
  exit 1
fi

echo "📱 抓取微信公众号文章..."
echo "URL: $URL"
echo ""

# 微信专用UA
UA_WECHAT='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x18002628) NetType/WIFI Language/zh_CN'

# 抓取页面
echo "🌐 使用微信UA抓取..."
curl -s -L \
  -A "$UA_WECHAT" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: zh-CN,zh;q=0.9" \
  -H "Referer: https://mp.weixin.qq.com/" \
  --max-time 30 \
  -o "$OUTPUT" \
  "$URL" 2>/dev/null

if [ ! -s "$OUTPUT" ] || [ $(wc -c < "$OUTPUT") -lt 1000 ]; then
  echo "❌ 抓取失败，尝试备用UA..."
  
  UA_IPHONE='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
  
  curl -s -L \
    -A "$UA_IPHONE" \
    --max-time 30 \
    -o "$OUTPUT" \
    "$URL" 2>/dev/null
fi

if [ -s "$OUTPUT" ] && [ $(wc -c < "$OUTPUT") -gt 1000 ]; then
  echo "✅ 抓取成功: $OUTPUT ($(wc -c < "$OUTPUT") bytes)"
  echo ""
  
  # 提取正文内容
  echo "📝 提取文章内容..."
  
  # 方法1: 提取 js_content 部分
  if grep -q 'id="js_content"' "$OUTPUT"; then
    echo "✅ 找到 js_content 容器"
    
    # 使用 sed 提取 js_content 内容
    sed -n '/id="js_content"/,/\/div/p' "$OUTPUT" | \
      sed 's/<[^\u003e]*\u003e//g' | \
      sed 's/&nbsp;/ /g' | \
      sed 's/&lt;/</g' | \
      sed 's/&gt;/>/g' | \
      sed 's/&amp;/&/g' | \
      sed '/^$/d' > "$CONTENT_FILE"
    
    echo "✅ 内容已提取: $CONTENT_FILE"
    
    # 显示前20行
    echo ""
    echo "📄 内容预览（前20行）:"
    echo "===================="
    head -20 "$CONTENT_FILE"
    echo "===================="
    echo ""
    
  else
    echo "⚠️  未找到 js_content，可能页面结构已变更"
    echo "📝 尝试提取所有文本..."
    
    # 备用：提取所有文本
    sed 's/<[^\u003e]*\u003e//g' "$OUTPUT" | \
      sed 's/&nbsp;/ /g' | \
      sed '/^$/d' | \
      head -100 > "$CONTENT_FILE"
    
    echo "✅ 文本已提取: $CONTENT_FILE"
  fi
  
  # 提取标题
  TITLE=$(grep -o '<h1[^\u003e]*class="rich_media_title[^"]*"[^\u003e]*>[^\u003c]*' "$OUTPUT" | sed 's/.*>//' | head -1)
  if [ -z "$TITLE" ]; then
    TITLE=$(grep -o '<title>[^\u003c]*' "$OUTPUT" | sed 's/<title>//' | head -1)
  fi
  
  echo "📌 标题: $TITLE"
  echo ""
  echo "✅ 完成！"
  echo "  原始HTML: $OUTPUT"
  echo "  提取内容: $CONTENT_FILE"
  
  exit 0
else
  echo "❌ 抓取失败"
  exit 1
fi
