#!/usr/bin/env python3
"""RSS抓取最终版 - 使用工作正常的逻辑生成daily_data.json"""

import json
import subprocess
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import html
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 完整的13个RSS源
RSS_SOURCES = {
    "TheVerge": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "Wired": "https://www.wired.com/feed/tag/ai/latest/rss",
    "VentureBeat": "https://venturebeat.com/category/ai/feed/",
    "TheGuardian AI": "https://www.theguardian.com/technology/artificialintelligenceai/rss",
    "ScienceDaily": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
    "MIT Tech Review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "MIT News": "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "Google Research": "https://research.google/blog/rss/",
    "Microsoft AI": "https://news.microsoft.com/source/topics/ai/feed/",
    "BAIR Berkeley": "https://bair.berkeley.edu/blog/feed.xml",
    "AI News": "https://www.artificialintelligence-news.com/feed/",
    "MarkTechPost": "https://www.marktechpost.com/feed/",
}

TAIPEI_TZ = ZoneInfo("Asia/Taipei")

def now_taipei():
    return datetime.now(TAIPEI_TZ)

def clean_html(text):
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = html.unescape(text)
    return text.strip()

def translate_to_chinese(text):
    """翻译文本为中文"""
    if not text or len(text) < 3:
        return text
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return text
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&dt=t&q=" + urllib.parse.quote(text[:500])
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))
        if data and len(data) > 0 and len(data[0]) > 0:
            translated_parts = [item[0] for item in data[0] if item and len(item) > 0]
            return ''.join(translated_parts)
        return text
    except Exception as e:
        return text

def fetch_rss(url, name):
    """RSS抓取 - 工作版本"""
    news_items = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', 
             '--max-time', '20', url],
            capture_output=True, text=True, timeout=25
        )
        
        if result.returncode != 0:
            return []
        
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            return []
        
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return []
        
        # 检测命名空间
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        root_tag = root.tag.split('}')[-1] if '}' in root.tag else root.tag
        is_atom = root_tag == 'feed'
        
        # 获取条目
        if is_atom:
            items = root.findall('atom:entry', ns)
            if not items:
                items = root.findall('entry')
        else:
            channel = root.find('.//channel')
            items = channel.findall('item') if channel is not None else root.findall('.//item')
        
        for item in items[:10]:
            try:
                # 标题
                title = ""
                if is_atom:
                    title_elem = item.find('atom:title', ns)
                    if title_elem is None:
                        title_elem = item.find('title')
                else:
                    title_elem = item.find('title')
                
                if title_elem is not None and title_elem.text:
                    title = clean_html(title_elem.text)
                
                # 链接
                link = ""
                if is_atom:
                    link_elem = item.find('atom:link', ns)
                    if link_elem is None:
                        link_elem = item.find('link')
                    if link_elem is not None:
                        link = link_elem.get('href', '')
                else:
                    link_elem = item.find('link')
                    if link_elem is not None:
                        link = link_elem.text or link_elem.get('href', '')
                
                # 摘要
                desc = ""
                if is_atom:
                    desc_elem = (item.find('atom:summary', ns) or item.find('summary') or 
                                item.find('atom:content', ns) or item.find('content'))
                else:
                    desc_elem = item.find('description')
                if desc_elem is not None and desc_elem.text:
                    desc = clean_html(desc_elem.text)
                
                # 日期
                pub_date = ""
                if is_atom:
                    date_elem = (item.find('atom:published', ns) or item.find('published') or
                                item.find('atom:updated', ns) or item.find('updated'))
                else:
                    date_elem = item.find('pubDate')
                if date_elem is not None and date_elem.text:
                    pub_date = date_elem.text
                
                if title and link:
                    # 翻译
                    title_zh = translate_to_chinese(title)
                    desc_zh = translate_to_chinese(desc)
                    
                    news_items.append({
                        'title': title_zh[:180] if title_zh else title[:180],
                        'source': name,
                        'url': link.strip(),
                        'summary': (desc_zh[:150] + '...') if len(desc_zh) > 150 else desc_zh,
                        'publishedAt': pub_date,
                        'type': 'news',
                        'fetched_at': now_taipei().isoformat()
                    })
            except Exception:
                continue
        
        return news_items
        
    except Exception:
        return []

def generate_quote():
    """生成每日引言"""
    quotes = [
        "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。",
        "每一次模型的迭代，都是人类理解智能本质的一次尝试。",
        "AI 不是替代人类，而是放大人类的可能性。",
        "最好的产品，是让技术隐形，让体验自然。",
        "创新往往发生在不同学科的交界处。",
        "伟大的工具，是让人忘记工具本身的存在。",
        "在信息爆炸的时代，筛选和品味比获取更重要。",
        "AI的进化速度提醒我们：保持学习是唯一不变的竞争力。",
        "技术的民主化，让创意的门槛不断降低，想象力的价值不断升高。"
    ]
    day = now_taipei().day
    return quotes[day % len(quotes)]

def main():
    print("="*70)
    print("小羽毛AI早报 - RSS抓取系统 (最终版)")
    print(f"时间: {now_taipei().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    all_news = []
    source_stats = {}
    
    for name, url in RSS_SOURCES.items():
        print(f"\n📡 {name}")
        items = fetch_rss(url, name)
        source_stats[name] = len(items)
        all_news.extend(items)
        print(f"   ✅ {len(items)} 条")
    
    # 去重（基于URL）
    seen_urls = set()
    unique_news = []
    for item in all_news:
        if item['url'] not in seen_urls:
            seen_urls.add(item['url'])
            unique_news.append(item)
    
    # 限制12条
    final_news = unique_news[:12]
    
    # 产品数据（简化）
    products = [
        {
            "title": "今日热门AI产品精选",
            "source": "Product Hunt",
            "url": "https://www.producthunt.com",
            "summary": "查看今日最热门的AI产品和工具",
            "type": "product",
            "fetched_at": now_taipei().isoformat()
        }
    ]
    
    # 输出
    output = {
        "date": now_taipei().strftime("%Y年%m月%d日"),
        "news": final_news,
        "products": products,
        "quote": generate_quote(),
        "summary": f"今日 AI 领域 {len(final_news)} 条精选资讯，{len(products)} 款创新产品值得关注。",
        "meta": {
            "rss_sources_total": 13,
            "rss_sources_success": sum(1 for c in source_stats.values() if c > 0),
            "total_fetched": len(all_news),
            "unique_news": len(unique_news),
            "final_news": len(final_news)
        }
    }
    
    with open("daily_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # 更新 news.ts
    try:
        subprocess.run(["python3", "update_news_ts.py"], check=True, timeout=30)
        print("\n✅ news.ts 更新完成")
    except Exception as e:
        print(f"\n⚠️ update_news_ts.py 失败: {e}")
    
    # 统计
    print("\n" + "="*70)
    print("📊 抓取统计")
    print("="*70)
    print(f"新闻源: {sum(1 for c in source_stats.values() if c > 0)}/13 成功")
    print(f"总获取: {len(all_news)} 条")
    print(f"去重后: {len(unique_news)} 条")
    print(f"最终: {len(final_news)} 条")
    
    print("\n📈 来源分布:")
    for name, count in sorted(source_stats.items(), key=lambda x: -x[1]):
        if count > 0:
            pct = count / len(all_news) * 100 if all_news else 0
            print(f"  {name:20s} {count:3d}条 ({pct:5.1f}%)")
    
    print("\n✅ 完成! 数据已保存到 daily_data.json")

if __name__ == "__main__":
    main()
