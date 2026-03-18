#!/bin/bash

# =============================================================================
# 小羽毛 AI 新闻早报 - 每日自动发布脚本
# 执行时间：每日 07:00 (Asia/Taipei)
# 执行流程：Fetch → Update → Build → Deploy
# =============================================================================

set -e  # 遇到错误立即退出

# 配置
PROJECT_DIR="/Users/ifai_macpro/.openclaw/workspace/iFAi/workspace/xiaoyumao-news-web Refer"
VERCEL_TOKEN="<VERCEL_TOKEN_REDACTED>"
LOG_FILE="/tmp/xiaoyumao-news-cron.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "========================================" >> "$LOG_FILE"
echo "[$DATE] 开始执行每日新闻更新" >> "$LOG_FILE"

# 进入项目目录
cd "$PROJECT_DIR"

# Step 1: 获取新闻数据
echo "[$DATE] Step 1/4: 获取新闻数据..." >> "$LOG_FILE"
python3 fetch_news_v2.py >> "$LOG_FILE" 2>&1

if [ ! -f "daily_data.json" ]; then
    echo "[$DATE] ❌ 错误: daily_data.json 未生成" >> "$LOG_FILE"
    exit 1
fi

echo "[$DATE] ✅ 新闻数据获取完成" >> "$LOG_FILE"

# Step 2: 转换为 TypeScript 并更新 news.ts
echo "[$DATE] Step 2/4: 更新新闻数据文件..." >> "$LOG_FILE"
python3 << 'PYTHON_SCRIPT'
import json
from datetime import datetime

# 读取获取的数据
with open('daily_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

news = data.get('news', [])
products = data.get('products', [])
date_str = data.get("date", datetime.now().strftime("%Y年%m月%d日"))
quote_text = data.get("quote", "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。")

# 生成 TypeScript 内容
ts_content = f'''// 自动生成 - 小羽毛 AI 早报
// 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

export interface NewsItem {{
  id: string;
  title: string;
  source: string;
  url: string;
  summary: string;
  type: 'news' | 'product';
  publishedAt: string;
}}

export interface DailyNews {{
  date: string;
  aiNews: NewsItem[];
  products: NewsItem[];
  summary: string;
  quote: {{
    text: string;
    author: string;
  }};
  generatedAt: string;
  websiteUrl: string;
}}

export const todayNews: DailyNews = {{
  "date": "{date_str} 周{'一二三四五六日'[datetime.now().weekday()]}",
  "aiNews": [
'''

# 添加新闻
for i, item in enumerate(news[:15]):
    ts_content += f'''    {{
      "id": "news_{i+1}",
      "title": "{item.get('title', '').replace('"', '\\"')}",
      "source": "{item.get('source', '').replace('"', '\\"')}",
      "url": "{item.get('url', '').replace('"', '\\"')}",
      "summary": "{item.get('summary', '')[:100].replace('"', '\\"')}...",
      "type": "news",
      "publishedAt": "{datetime.now().strftime('%Y-%m-%d')}"
    }}{',' if i < min(len(news), 15) - 1 else ''}
'''

ts_content += '''  ],
  "products": [
'''

# 添加产品
for i, item in enumerate(products[:5]):
    ts_content += f'''    {{
      "id": "product_{i+1}",
      "title": "{item.get('title', '').replace('"', '\\"').split(' - ')[0]}",
      "source": "{item.get('source', '').replace('"', '\\"')}",
      "url": "{item.get('url', '').replace('"', '\\"')}",
      "summary": "{item.get('summary', '今日热门产品').replace('"', '\\"')}",
      "type": "product",
      "publishedAt": "{datetime.now().strftime('%Y-%m-%d')}"
    }}{',' if i < min(len(products), 5) - 1 else ''}
'''

ts_content += f'''  ],
  "summary": "今日 AI 圈：{news[0].get('title', '最新 AI 资讯')[:30]}...等 {len(news)} 条新闻，{len(products)} 款热门产品。",
  "quote": {{
    "text": "{quote_text}",
    "author": "小羽毛 AI"
  }},
  "generatedAt": "{datetime.now().isoformat()}",
  "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
}};

export default todayNews;
'''

# 写入文件
with open('src/data/news.ts', 'w', encoding='utf-8') as f:
    f.write(ts_content)

print(f"✅ news.ts 更新完成，包含 {len(news)} 条新闻，{len(products)} 个产品")
PYTHON_SCRIPT

echo "[$DATE] ✅ 数据文件更新完成" >> "$LOG_FILE"

# Step 3: 构建项目
echo "[$DATE] Step 3/4: 构建项目..." >> "$LOG_FILE"
npm run build >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$DATE] ❌ 错误: 构建失败" >> "$LOG_FILE"
    exit 1
fi

echo "[$DATE] ✅ 构建完成" >> "$LOG_FILE"

# Step 4: 部署到 Vercel
echo "[$DATE] Step 4/4: 部署到 Vercel..." >> "$LOG_FILE"
npx vercel --prod --token "$VERCEL_TOKEN" --yes >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "[$DATE] ❌ 错误: 部署失败" >> "$LOG_FILE"
    exit 1
fi

echo "[$DATE] ✅ 部署完成" >> "$LOG_FILE"
echo "[$DATE] 🎉 每日新闻早报更新成功！" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

exit 0
