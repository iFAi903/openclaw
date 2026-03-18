#!/usr/bin/env python3
"""
RSS抓取最终版 - 小羽毛 AI 新闻早报数据获取模块

功能：
    - 从多个 RSS 源获取 AI 相关新闻
    - 自动翻译英文内容为中文
    - 生成 daily_data.json 供前端展示

用法：
    python3 fetch_news_final.py

环境变量：
    无需特殊环境变量

输出：
    daily_data.json - 当日新闻数据
"""

import json
import subprocess
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import html
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Any, Optional, Tuple

# =============================================================================
# 常量定义
# =============================================================================

# RSS 源配置
RSS_SOURCES: Dict[str, str] = {
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

# 时区配置
TIMEZONE = ZoneInfo("Asia/Taipei")

# 抓取配置
MAX_ITEMS_PER_SOURCE = 10      # 每个源最多抓取条目数
MAX_FINAL_NEWS = 12            # 最终保留新闻数
MAX_TITLE_LENGTH = 180         # 标题最大长度
MAX_SUMMARY_LENGTH = 150       # 摘要最大长度
CURL_TIMEOUT = 20              # curl 超时时间(秒)
TRANSLATE_TIMEOUT = 8          # 翻译 API 超时时间(秒)
TRANSLATE_MAX_LENGTH = 500     # 翻译文本最大长度

# =============================================================================
# 工具函数
# =============================================================================

def now_taipei() -> datetime:
    """获取当前台北时间。"""
    return datetime.now(TIMEZONE)


def clean_html(text: str) -> str:
    """
    清理 HTML 标签并解码 HTML 实体。
    
    Args:
        text: 可能包含 HTML 的原始文本
        
    Returns:
        清理后的纯文本
    """
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = html.unescape(text)
    return text.strip()


def translate_to_chinese(text: str) -> str:
    """
    使用 Google Translate API 将文本翻译为中文。
    
    注意：这是免费的非官方 API，可能存在速率限制。
    如果翻译失败，返回原文。
    
    Args:
        text: 要翻译的文本
        
    Returns:
        翻译后的中文文本或原文
    """
    if not text or len(text) < 3:
        return text
    # 如果已包含中文字符，跳过翻译
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return text
    
    try:
        url = (
            "https://translate.googleapis.com/translate_a/single?"
            "client=gtx&sl=auto&tl=zh-CN&dt=t&q="
        ) + urllib.parse.quote(text[:TRANSLATE_MAX_LENGTH])
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=TRANSLATE_TIMEOUT) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        if data and len(data) > 0 and len(data[0]) > 0:
            translated_parts = [item[0] for item in data[0] if item and len(item) > 0]
            return ''.join(translated_parts)
            
        return text
    except Exception:
        return text


def fetch_rss(url: str, name: str) -> List[Dict[str, Any]]:
    """
    从单个 RSS 源抓取新闻条目。
    
    支持标准 RSS 2.0 和 Atom 1.0 格式。
    自动处理 XML 命名空间。
    
    Args:
        url: RSS 源 URL
        name: 源名称(用于标记数据来源)
        
    Returns:
        新闻条目列表，每个条目包含 title, source, url, summary, publishedAt 等字段
    """
    news_items: List[Dict[str, Any]] = []
    
    try:
        # 使用 curl 获取 RSS 内容(更稳定的网络请求)
        result = subprocess.run(
            [
                'curl', '-s', '-L',
                '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)',
                '--max-time', str(CURL_TIMEOUT),
                url
            ],
            capture_output=True,
            text=True,
            timeout=CURL_TIMEOUT + 5
        )
        
        if result.returncode != 0:
            return []
        
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            return []
        
        # 解析 XML
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return []
        
        # 检测命名空间和格式类型
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        root_tag = root.tag.split('}')[-1] if '}' in root.tag else root.tag
        is_atom = root_tag == 'feed'
        
        # 获取条目列表
        if is_atom:
            items = root.findall('atom:entry', ns)
            if not items:
                items = root.findall('entry')
        else:
            channel = root.find('.//channel')
            items = channel.findall('item') if channel is not None else root.findall('.//item')
        
        # 处理每个条目
        for item in items[:MAX_ITEMS_PER_SOURCE]:
            try:
                # 提取标题
                title = ""
                if is_atom:
                    title_elem = item.find('atom:title', ns)
                    if title_elem is None:
                        title_elem = item.find('title')
                else:
                    title_elem = item.find('title')
                
                if title_elem is not None and title_elem.text:
                    title = clean_html(title_elem.text)
                
                # 提取链接
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
                
                # 提取摘要
                desc = ""
                if is_atom:
                    desc_elem = (
                        item.find('atom:summary', ns) or
                        item.find('summary') or
                        item.find('atom:content', ns) or
                        item.find('content')
                    )
                else:
                    desc_elem = item.find('description')
                if desc_elem is not None and desc_elem.text:
                    desc = clean_html(desc_elem.text)
                
                # 提取发布日期
                pub_date = ""
                if is_atom:
                    date_elem = (
                        item.find('atom:published', ns) or
                        item.find('published') or
                        item.find('atom:updated', ns) or
                        item.find('updated')
                    )
                else:
                    date_elem = item.find('pubDate')
                if date_elem is not None and date_elem.text:
                    pub_date = date_elem.text
                
                # 构建新闻条目
                if title and link:
                    title_zh = translate_to_chinese(title)
                    desc_zh = translate_to_chinese(desc)
                    
                    news_items.append({
                        'title': title_zh[:MAX_TITLE_LENGTH] if title_zh else title[:MAX_TITLE_LENGTH],
                        'source': name,
                        'url': link.strip(),
                        'summary': (
                            (desc_zh[:MAX_SUMMARY_LENGTH] + '...')
                            if len(desc_zh) > MAX_SUMMARY_LENGTH
                            else desc_zh
                        ),
                        'publishedAt': pub_date,
                        'type': 'news',
                        'fetched_at': now_taipei().isoformat()
                    })
            except Exception:
                continue
        
        return news_items
        
    except Exception:
        return []


def generate_quote() -> str:
    """
    生成每日引言。
    
    根据日期从预定义列表中选择一句引言，
    确保同一日期始终返回相同的引言。
    
    Returns:
        中文引言文本
    """
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


def deduplicate_news(news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    根据 URL 去重新闻列表。
    
    Args:
        news_list: 原始新闻列表
        
    Returns:
        去重后的新闻列表
    """
    seen_urls = set()
    unique_news = []
    
    for item in news_list:
        url = item.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_news.append(item)
    
    return unique_news


def generate_default_products() -> List[Dict[str, Any]]:
    """
    生成默认产品列表。
    
    Returns:
        产品条目列表
    """
    return [
        {
            "title": "今日热门AI产品精选",
            "source": "Product Hunt",
            "url": "https://www.producthunt.com",
            "summary": "查看今日最热门的AI产品和工具",
            "type": "product",
            "fetched_at": now_taipei().isoformat()
        }
    ]


# =============================================================================
# 主流程
# =============================================================================

def main() -> None:
    """
    主入口函数。
    
    执行完整的 RSS 抓取流程：
    1. 从所有配置的 RSS 源抓取新闻
    2. 去重并限制数量
    3. 生成 daily_data.json
    4. 更新 news.ts 文件
    """
    print("=" * 70)
    print("小羽毛AI早报 - RSS抓取系统 (最终版)")
    print(f"时间: {now_taipei().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    all_news: List[Dict[str, Any]] = []
    source_stats: Dict[str, int] = {}
    
    # 从每个 RSS 源抓取
    for name, url in RSS_SOURCES.items():
        print(f"\n📡 {name}")
        items = fetch_rss(url, name)
        source_stats[name] = len(items)
        all_news.extend(items)
        print(f"   ✅ {len(items)} 条")
    
    # 去重
    unique_news = deduplicate_news(all_news)
    
    # 限制最终数量
    final_news = unique_news[:MAX_FINAL_NEWS]
    
    # 生成产品数据
    products = generate_default_products()
    
    # 构建输出数据
    output = {
        "date": now_taipei().strftime("%Y年%m月%d日"),
        "news": final_news,
        "products": products,
        "quote": generate_quote(),
        "summary": f"今日 AI 领域 {len(final_news)} 条精选资讯，{len(products)} 款创新产品值得关注。",
        "meta": {
            "rss_sources_total": len(RSS_SOURCES),
            "rss_sources_success": sum(1 for c in source_stats.values() if c > 0),
            "total_fetched": len(all_news),
            "unique_news": len(unique_news),
            "final_news": len(final_news)
        }
    }
    
    # 写入 JSON 文件
    with open("daily_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # 更新 TypeScript 文件
    try:
        subprocess.run(
            ["python3", "update_news_ts.py"],
            check=True,
            timeout=30
        )
        print("\n✅ news.ts 更新完成")
    except Exception as e:
        print(f"\n⚠️ update_news_ts.py 失败: {e}")
    
    # 打印统计
    print("\n" + "=" * 70)
    print("📊 抓取统计")
    print("=" * 70)
    print(f"新闻源: {sum(1 for c in source_stats.values() if c > 0)}/{len(RSS_SOURCES)} 成功")
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
