import json
from datetime import datetime
from zoneinfo import ZoneInfo

TAIPEI_TZ = ZoneInfo("Asia/Taipei")


def now_taipei():
    return datetime.now(TAIPEI_TZ)

with open('daily_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

news = data.get('news', [])
products = data.get('products', [])
date_str = data.get('date', now_taipei().strftime('%Y年%m月%d日'))
quote_text = data.get('quote', '')

# 清理文本，移除换行符和控制字符
def clean_text(text, max_len=100):
    if not text:
        return ""
    # 移除换行符和多余空格
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    # 移除HTML标签
    import re
    text = re.sub(r'<[^>]+>', '', text)
    # 压缩多余空格
    text = ' '.join(text.split())
    # 截取长度
    if len(text) > max_len:
        text = text[:max_len] + "..."
    return text.strip()

# 构建数据结构
today_news = {
    "date": f"{date_str} 周{'一二三四五六日'[now_taipei().weekday()]}",
    "aiNews": [],
    "products": [],
    "summary": f"今日 AI 圈：{clean_text(news[0].get('title', '最新 AI 资讯'), 30)} 等 {len(news)} 条新闻，{len(products)} 款热门产品。",
    "quote": {
        "text": clean_text(quote_text, 200),
        "author": "小羽毛 AI"
    },
    "generatedAt": now_taipei().isoformat(),
    "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
}

for i, item in enumerate(news[:15]):
    today_news["aiNews"].append({
        "id": f"news_{i+1}",
        "title": clean_text(item.get('title', ''), 100),
        "source": item.get('source', ''),
        "url": item.get('url', ''),
        "summary": clean_text(item.get('summary', ''), 100),
        "type": "news",
        "publishedAt": now_taipei().strftime('%Y-%m-%d')
    })

for i, item in enumerate(products[:5]):
    title = item.get('title', '')
    if ' - ' in title:
        title = title.split(' - ')[0]
    today_news["products"].append({
        "id": f"product_{i+1}",
        "title": clean_text(title, 80),
        "source": item.get('source', ''),
        "url": item.get('url', ''),
        "summary": clean_text(item.get('summary', '今日热门产品'), 100),
        "type": "product",
        "publishedAt": now_taipei().strftime('%Y-%m-%d')
    })

# 生成 TypeScript 内容
ts_content = f'''// 自动生成 - 小羽毛 AI 早报
// 生成时间: {now_taipei().strftime('%Y-%m-%d %H:%M:%S')}

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

export const todayNews: DailyNews = {json.dumps(today_news, ensure_ascii=False, indent=2)};

export default todayNews;
'''

with open('src/data/news.ts', 'w', encoding='utf-8') as f:
    f.write(ts_content)

print(f'✅ news.ts 更新完成: {len(news)}条新闻, {len(products)}个产品')
