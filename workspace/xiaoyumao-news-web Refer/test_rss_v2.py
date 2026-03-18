#!/usr/bin/env python3
"""RSS源测试脚本 - 快速验证所有13个源"""

import json
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 完整的13个RSS源配置
RSS_SOURCES = {
    # 主流科技媒体 (6个)
    "TheVerge": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
    "TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/",
    "Wired": "https://www.wired.com/feed/tag/ai/latest/rss",
    "VentureBeat": "https://venturebeat.com/category/ai/feed/",
    "TheGuardian AI": "https://www.theguardian.com/technology/artificialintelligenceai/rss",
    "ScienceDaily": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
    
    # 学术/研究源 (5个)
    "MIT Tech Review": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
    "MIT News": "https://news.mit.edu/rss/topic/artificial-intelligence2",
    "Google Research": "https://research.google/blog/rss/",
    "Microsoft AI": "https://news.microsoft.com/source/topics/ai/feed/",
    "BAIR Berkeley": "https://bair.berkeley.edu/blog/feed.xml",
    
    # AI专业媒体 (2个)
    "AI News": "https://www.artificialintelligence-news.com/feed/",
    "MarkTechPost": "https://www.marktechpost.com/feed/",
}

TAIPEI_TZ = ZoneInfo("Asia/Taipei")

def now_taipei():
    return datetime.now(TAIPEI_TZ)

def clean_html(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def fetch_rss_simple(url, name):
    """简化的RSS抓取，不进行翻译"""
    news_items = []
    status = {"name": name, "url": url, "status": "unknown", "items": 0, "error": None}
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', 
             '--max-time', '15', url],
            capture_output=True,
            text=True,
            timeout=20
        )
        
        if result.returncode != 0:
            status["status"] = "failed"
            status["error"] = f"curl failed: {result.returncode}"
            return [], status
        
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            status["status"] = "failed"
            status["error"] = "Empty response"
            return [], status
        
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            status["status"] = "failed"
            status["error"] = f"XML parse error: {e}"
            return [], status
        
        # 检测格式
        if root.tag == 'rss' or root.tag.endswith('rss'):
            channel = root.find('.//channel')
            if channel is None:
                items = root.findall('.//item')
            else:
                items = channel.findall('.//item')
        elif root.tag.endswith('feed') or root.tag == 'feed':
            items = root.findall('.//{http://www.w3.org/2005/Atom}entry')
            if not items:
                items = root.findall('.//entry')
        else:
            items = root.findall('.//item')
        
        for item in items[:5]:  # 只取前5个
            try:
                title_elem = item.find('title')
                title = title_elem.text if title_elem is not None else ""
                
                link_elem = item.find('link')
                if link_elem is not None:
                    link = link_elem.text
                    if not link:
                        link = link_elem.get('href', '')
                else:
                    link = ""
                
                desc_elem = item.find('description')
                if desc_elem is None:
                    desc_elem = item.find('.//{http://www.w3.org/2005/Atom}summary')
                if desc_elem is None:
                    desc_elem = item.find('summary')
                
                description = desc_elem.text if desc_elem is not None else ""
                
                if title and link:
                    title = clean_html(title)
                    description = clean_html(description)
                    
                    news_items.append({
                        'title': title[:100],  # 截断标题
                        'source': name,
                        'url': link,
                        'summary': description[:150] + '...' if len(description) > 150 else description,
                    })
            except Exception as e:
                continue
        
        status["status"] = "success"
        status["items"] = len(news_items)
        status["total_available"] = len(items)
        
    except subprocess.TimeoutExpired:
        status["status"] = "timeout"
        status["error"] = "Request timeout"
    except Exception as e:
        status["status"] = "error"
        status["error"] = str(e)
    
    return news_items, status

def main():
    print("="*70)
    print("RSS源抓取测试报告")
    print(f"时间: {now_taipei().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    all_results = []
    all_news = []
    success_count = 0
    
    for name, url in RSS_SOURCES.items():
        items, status = fetch_rss_simple(url, name)
        all_results.append(status)
        all_news.extend(items)
        if status["status"] == "success":
            success_count += 1
        print(f"\n{'✅' if status['status'] == 'success' else '❌'} {name}")
        print(f"   状态: {status['status']}")
        print(f"   获取: {status.get('items', 0)}/{status.get('total_available', 0)} 条")
        if status.get('error'):
            print(f"   错误: {status['error']}")
    
    # 统计
    print("\n" + "="*70)
    print("统计汇总")
    print("="*70)
    print(f"成功源: {success_count}/{len(RSS_SOURCES)}")
    print(f"总新闻: {len(all_news)} 条")
    
    # 来源分布
    source_count = {}
    for item in all_news:
        src = item['source']
        source_count[src] = source_count.get(src, 0) + 1
    
    print("\n来源分布:")
    for src, count in sorted(source_count.items(), key=lambda x: -x[1]):
        pct = count / len(all_news) * 100 if all_news else 0
        print(f"  {src}: {count}条 ({pct:.1f}%)")
    
    # 保存测试结果
    test_result = {
        "timestamp": now_taipei().isoformat(),
        "success_rate": f"{success_count}/{len(RSS_SOURCES)}",
        "sources": all_results,
        "total_news": len(all_news),
        "source_distribution": source_count
    }
    
    with open("rss_test_result.json", "w", encoding="utf-8") as f:
        json.dump(test_result, f, indent=2, ensure_ascii=False)
    
    print("\n详细结果已保存到: rss_test_result.json")
    
    # 返回是否通过
    if success_count >= 8:
        print(f"\n✅ 测试通过! {success_count}个源正常工作")
        return 0
    else:
        print(f"\n❌ 测试失败! 仅{success_count}个源正常工作")
        return 1

if __name__ == "__main__":
    exit(main())
