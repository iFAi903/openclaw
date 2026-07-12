#!/usr/bin/env python3
"""daily_data.json → src/data/news.ts 编译脚本"""
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

TAIPEI_TZ = ZoneInfo('Asia/Taipei')
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_DIR / 'daily_data.json'
OUT_FILE = PROJECT_DIR / 'src' / 'data' / 'news.ts'


def now_taipei() -> datetime:
    return datetime.now(TAIPEI_TZ)


def clean_text(text: str, max_len: int = 300) -> str:
    text = (text or '').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    text = re.sub(r'<[^>]+>', '', text)
    text = ' '.join(text.split()).strip()
    return text[:max_len].strip()


with DATA_FILE.open('r', encoding='utf-8') as f:
    data = json.load(f)

news = data.get('news', [])[:18]
products = data.get('products', [])[:5]
date_str = data.get('date', now_taipei().strftime('%Y年%m月%d日'))
weekday = '一二三四五六日'[now_taipei().weekday()]
if f'周{weekday}' in date_str:
    display_date = date_str
else:
    display_date = f'{date_str} 周{weekday}'

payload = {
    'date': display_date,
    'summary': clean_text(data.get('summary', ''), 180),
    'quote': {
        'text': clean_text(data.get('quote', ''), 160),
        'author': '小羽毛 AI',
    },
    'generatedAt': data.get('meta', {}).get('generated_at', now_taipei().isoformat()),
    'websiteUrl': 'https://ai-news-roundup.vercel.app',
    'meta': data.get('meta', {}),
    'aiNews': [
        {
            'id': f'news_{idx + 1}',
            'rank': idx + 1,
            'title': clean_text(item.get('title', ''), 60),
            'source': clean_text(item.get('source', ''), 40),
            'url': item.get('url', ''),
            'summary': clean_text(item.get('summary', ''), 160),
            'publishedAt': item.get('publishedAt', ''),
            'type': 'news',
            'score': item.get('score', 0),
            'reason': ', '.join(item.get('tags', [])) if item.get('tags') else clean_text(item.get('reason', ''), 120),
            'tags': item.get('tags', []),
        }
        for idx, item in enumerate(news)
    ],
    'products': [
        {
            'id': f'product_{idx + 1}',
            'rank': idx + 1,
            'title': clean_text(item.get('title', ''), 60),
            'source': clean_text(item.get('source', ''), 40),
            'platform': clean_text(item.get('platform', ''), 30),
            'url': item.get('url', ''),
            'summary': clean_text(item.get('summary', ''), 160),
            'publishedAt': item.get('publishedAt', ''),
            'type': 'product',
            'score': item.get('score', 0),
            'reason': ', '.join(item.get('tags', [])) if item.get('tags') else clean_text(item.get('reason', ''), 120),
            'tags': item.get('tags', []),
        }
        for idx, item in enumerate(products)
    ],
}

content = f'''// 自动生成 - 小羽毛 AI 新闻早报
// 生成时间: {now_taipei().strftime('%Y-%m-%d %H:%M:%S')}

export interface NewsCard {{
  id: string;
  rank: number;
  title: string;
  source: string;
  url: string;
  summary: string;
  publishedAt: string;
  type: 'news' | 'product';
  score: number;
  reason: string;
  platform?: string;
  tags?: string[];
}}

export interface DailyNewsPayload {{
  date: string;
  summary: string;
  quote: {{ text: string; author: string }};
  generatedAt: string;
  websiteUrl: string;
  meta: Record<string, any>;
  aiNews: NewsCard[];
  products: NewsCard[];
}}

export const todayNews: DailyNewsPayload = {json.dumps(payload, ensure_ascii=False, indent=2)};

export default todayNews;
'''

OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUT_FILE.write_text(content, encoding='utf-8')
print(f'✅ news.ts 更新完成: {len(news)} 条新闻, {len(products)} 个产品')
