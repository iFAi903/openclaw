#!/usr/bin/env python3
"""RSS修复版 - 完整13源抓取"""

import json
import subprocess
import xml.etree.ElementTree as ET
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
HISTORY_FILE = "news_history.json"

def now_taipei():
    return datetime.now(TAIPEI_TZ)

def clean_html(text):
    import re
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    # 解码HTML实体
    import html
    text = html.unescape(text)
    return text

def fetch_rss_fixed(url, name):
    """修复版的RSS抓取，支持Atom和RSS格式"""
    news_items = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', 
             '--max-time', '20', url],
            capture_output=True,
            text=True,
            timeout=25
        )
        
        if result.returncode != 0:
            print(f"  ❌ curl failed")
            return []
        
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            print(f"  ❌ Empty response")
            return []
        
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            print(f"  ❌ XML parse error: {e}")
            return []
        
        # 检测格式和命名空间
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
            if channel is not None:
                items = channel.findall('item')
            else:
                items = root.findall('.//item')
        
        print(f"  📄 {len(items)} items in feed")
        
        for item in items[:10]:  # 每个源最多取10条
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
                    desc_elem = item.find('atom:summary', ns)
                    if desc_elem is None:
                        desc_elem = item.find('summary')
                    if desc_elem is None:
                        desc_elem = item.find('atom:content', ns)
                    if desc_elem is None:
                        desc_elem = item.find('content')
                else:
                    desc_elem = item.find('description')
                
                if desc_elem is not None and desc_elem.text:
                    desc = clean_html(desc_elem.text)
                
                # 日期
                pub_date = ""
                if is_atom:
                    date_elem = item.find('atom:published', ns)
                    if date_elem is None:
                        date_elem = item.find('published')
                    if date_elem is None:
                        date_elem = item.find('atom:updated', ns)
                    if date_elem is None:
                        date_elem = item.find('updated')
                else:
                    date_elem = item.find('pubDate')
                
                if date_elem is not None and date_elem.text:
                    pub_date = date_elem.text
                
                if title and link:
                    news_items.append({
                        'title': title[:200],
                        'source': name,
                        'url': link.strip(),
                        'summary': (desc[:200] + '...') if len(desc) > 200 else desc,
                        'publishedAt': pub_date,
                        'type': 'news'
                    })
            except Exception as e:
                continue
        
        return news_items
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def main():
    print("="*70)
    print("小羽毛AI早报 - RSS抓取 (13源修复版)")
    print(f"时间: {now_taipei().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    all_news = []
    source_counts = {}
    
    for name, url in RSS_SOURCES.items():
        print(f"\n📡 {name}")
        items = fetch_rss_fixed(url, name)
        source_counts[name] = len(items)
        all_news.extend(items)
        print(f"   ✅ {len(items)} 条新闻")
    
    # 统计
    print("\n" + "="*70)
    print("📊 抓取统计")
    print("="*70)
    print(f"成功源: {sum(1 for c in source_counts.values() if c > 0)}/13")
    print(f"总新闻: {len(all_news)} 条")
    
    print("\n📈 来源分布:")
    for name, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        pct = count / len(all_news) * 100 if all_news else 0
        bar = "█" * int(pct / 5)
        print(f"  {name:20s} {count:2d}条 ({pct:5.1f}%) {bar}")
    
    # 保存结果
    output = {
        "date": now_taipei().strftime("%Y年%m月%d日"),
        "news": all_news,
        "source_stats": source_counts,
        "total": len(all_news),
        "timestamp": now_taipei().isoformat()
    }
    
    with open("rss_diagnostic_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print("\n💾 结果已保存到: rss_diagnostic_result.json")
    
    # 验证标准
    success_count = sum(1 for c in source_counts.values() if c > 0)
    if success_count >= 8:
        print(f"\n✅ 成功! {success_count}个源正常工作")
        return 0
    else:
        print(f"\n❌ 失败! 仅{success_count}个源正常工作")
        return 1

if __name__ == "__main__":
    exit(main())
