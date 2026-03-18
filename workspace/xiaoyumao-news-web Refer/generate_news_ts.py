#!/usr/bin/env python3
"""
生成 news.ts TypeScript 数据文件
从 daily_data.json 生成前端可用的 TypeScript 代码
"""

import json
from datetime import datetime
from typing import Dict, List, Any


def generate_typescript(data: Dict[str, Any]) -> str:
    """从 JSON 数据生成 TypeScript 代码"""
    
    news: List[Dict] = data.get('news', [])
    products: List[Dict] = data.get('products', [])
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
        title = str(item.get('title', '')).replace('"', '\\"')
        source = str(item.get('source', '')).replace('"', '\\"')
        url = str(item.get('url', '')).replace('"', '\\"')
        summary = str(item.get('summary', ''))[:100].replace('"', '\\"')
        
        ts_content += f'''    {{
      "id": "news_{i+1}",
      "title": "{title}",
      "source": "{source}",
      "url": "{url}",
      "summary": "{summary}...",
      "type": "news",
      "publishedAt": "{datetime.now().strftime('%Y-%m-%d')}"
    }}{',' if i < min(len(news), 15) - 1 else ''}
'''

    ts_content += '''  ],
  "products": [
'''

    # 添加产品
    for i, item in enumerate(products[:5]):
        title = str(item.get('title', '')).replace('"', '\\"').split(' - ')[0]
        source = str(item.get('source', '')).replace('"', '\\"')
        url = str(item.get('url', '')).replace('"', '\\"')
        summary = str(item.get('summary', '今日热门产品')).replace('"', '\\"')
        
        ts_content += f'''    {{
      "id": "product_{i+1}",
      "title": "{title}",
      "source": "{source}",
      "url": "{url}",
      "summary": "{summary}",
      "type": "product",
      "publishedAt": "{datetime.now().strftime('%Y-%m-%d')}"
    }}{',' if i < min(len(products), 5) - 1 else ''}
'''

    news_title = str(news[0].get('title', '最新 AI 资讯'))[:30] if news else '最新 AI 资讯'
    
    ts_content += f'''  ],
  "summary": "今日 AI 圈：{news_title}...等 {len(news)} 条新闻，{len(products)} 款热门产品。",
  "quote": {{
    "text": "{quote_text}",
    "author": "小羽毛 AI"
  }},
  "generatedAt": "{datetime.now().isoformat()}",
  "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
}};

export default todayNews;
'''

    return ts_content


def main():
    """主函数"""
    try:
        # 读取 JSON 数据
        with open('daily_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 生成 TypeScript
        ts_content = generate_typescript(data)
        
        # 写入文件
        with open('src/data/news.ts', 'w', encoding='utf-8') as f:
            f.write(ts_content)
        
        news = data.get('news', [])
        products = data.get('products', [])
        print(f"✅ news.ts 更新完成，包含 {len(news)} 条新闻，{len(products)} 个产品")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        exit(1)


if __name__ == "__main__":
    main()
