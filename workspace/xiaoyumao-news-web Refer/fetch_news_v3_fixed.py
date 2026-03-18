import json
import os
import subprocess
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import html
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Sources Configuration - 13个主要AI新闻源
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

PRODUCT_SOURCES = {
    "ProductHunt": "https://www.producthunt.com/feed",
    "HackerNews": "https://news.ycombinator.com/rss",
    "GitHub": "https://github.com/trending?since=daily",
    "Toolify": "https://www.toolify.ai/rss",
    "Reddit": "https://www.reddit.com/r/ArtificialInteligence/top/.rss?t=day",
}

HISTORY_FILE = "news_history.json"
HISTORY_DAYS = 3
TAIPEI_TZ = ZoneInfo("Asia/Taipei")

def now_taipei():
    return datetime.now(TAIPEI_TZ)

# 英文关键词保留列表
ENGLISH_KEYWORDS = {
    "ChatGPT", "OpenAI", "Claude", "Anthropic", "Gemini", "Google", "Meta", "LLaMA",
    "Mistral", "Midjourney", "Stable Diffusion", "DALL-E", "Sora", "GPT-4", "GPT-3",
    "Copilot", "GitHub", "Microsoft", "Amazon", "AWS", "Azure", "Twitter", "X",
    "YouTube", "TikTok", "Instagram", "WhatsApp", "Android", "iOS", "macOS",
    "Windows", "Linux", "Python", "JavaScript", "TypeScript", "React", "Vue",
    "Node.js", "TensorFlow", "PyTorch", "CUDA", "API", "SDK", "SaaS", "PaaS",
    "IaaS", "FaaS", "ML", "LLM", "AI", "GPU", "CPU", "TPU", "NPU",
    "OpenClaw", "NemoClaw", "xAI", "Grok", "Grok-2", "Grok-3",
    "ProductHunt", "Product Hunt", "HackerNews", "Hacker News", "Reddit", "Toolify",
    "NVIDIA", "Intel", "AMD", "Qualcomm", "Apple", "Tesla", "SpaceX", "Neuralink",
    "DeepMind", "Cohere", "Adept", "Character.AI", "Runway", "Shopify", "Netflix",
    "OpenAI", "Perplexity", "Poe", "Hugging Face", "Stability AI",
    "ElevenLabs", "Inflection", "Adept AI", "Character AI",
    "ByteDance", "Oracle", "IBM", "Salesforce", "Adobe", "Cisco",
    "Samsung", "Sony", "LG", "Huawei", "Xiaomi", "DJI", "Baidu", "Alibaba",
    "Tencent", "Meituan", "Pinduoduo", "JD.com", "Didi", "NIO", "XPeng", "Li Auto",
    "Waymo", "Cruise", "Zoox", "Aurora", "Comma.ai", "Comma AI",
    "Sam Altman", "Elon Musk", "Sundar Pichai", "Satya Nadella", "Tim Cook",
    "Mark Zuckerberg", "Jensen Huang", "Demis Hassabis", "Dario Amodei",
    "Andrew Ng", "Fei-Fei Li", "Yann LeCun", "Geoffrey Hinton", "Yoshua Bengio",
    "Andrej Karpathy", "Sebastian Thrun", "Lex Fridman", "Bill Gates", "Jeff Bezos",
    "Larry Page", "Sergey Brin", "Steve Jobs", "Paul Allen", "Peter Thiel",
    "Marc Andreessen", "Reid Hoffman", "Eric Schmidt", "Larry Ellison", "Safra Catz",
    "Lisa Su", "Pat Gelsinger", "Brian Krzanich", "Robert Swan", "Gordon Moore",
    "iPhone", "iPad", "MacBook", "MacBook Pro", "MacBook Air", "Mac Studio",
    "AirPods", "AirPods Max", "AirPods Pro", "Apple Watch", "Vision Pro",
    "Pixel", "Surface", "Xbox", "PlayStation", "Galaxy", "Raspberry Pi", "Arduino",
    "IPO", "SPAC", "VC", "PE", "valuation", "market cap", "revenue", "ARR", "MRR",
    "Bitcoin", "Ethereum", "Solana", "DeFi", "NFT", "DAO", "Web3", "dApp",
    "DLSS", "DLSS 5", "Blackwell", "Jetson", "CUDA", "API", "SDK",
}

def clean_html(text):
    import re
    if not text:
        return ""
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', text)
    text = html.unescape(text)
    return text.strip()

def translate_to_chinese(text):
    """翻译文本为中文，带超时和错误处理"""
    if not text or len(text) < 3:
        return text
    
    # 如果已经有中文，直接返回
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

def translate_with_keywords(text, is_title=False):
    """翻译文本但保留英文关键词"""
    import re
    
    if not text:
        return ""
    
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return text
    
    # 保护关键词
    placeholders = {}
    protected_text = text
    sorted_keywords = sorted(ENGLISH_KEYWORDS, key=len, reverse=True)
    
    for i, keyword in enumerate(sorted_keywords):
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, protected_text, re.IGNORECASE)
        for match in matches:
            placeholder = f"__KW_{i}_{len(placeholders)}__"
            placeholders[placeholder] = match
            protected_text = protected_text.replace(match, placeholder)
    
    # 翻译
    translated = translate_to_chinese(protected_text)
    translated = translated.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    
    # 还原关键词
    for placeholder, original in placeholders.items():
        translated = translated.replace(placeholder, original)
    
    return translated

def fetch_rss(url, name):
    """修复版的RSS抓取，支持RSS和Atom格式"""
    news_items = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', 
             '--max-time', '25', url],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode != 0:
            print(f"  ❌ {name}: curl failed")
            return []
        
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            print(f"  ❌ {name}: Empty response")
            return []
        
        # 保存XML用于调试 (完整内容)
        safe_name = name.replace(' ', '_').replace('/', '_')
        try:
            with open(f"{safe_name}.xml", 'w', encoding='utf-8') as f:
                f.write(xml_content)
        except:
            pass
        
        # 解析XML
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            print(f"  ❌ {name}: XML parse error - {e}")
            return []
        
        # 检测格式和命名空间
        root_tag_full = root.tag
        if '}' in root_tag_full:
            ns_uri = root_tag_full.split('}')[0][1:]  # 提取命名空间URI
            root_tag = root_tag_full.split('}')[1]
        else:
            ns_uri = ''
            root_tag = root_tag_full
        
        is_atom = root_tag == 'feed'
        
        # 获取条目 - 处理默认命名空间
        if is_atom and ns_uri:
            # 使用默认命名空间
            ns = {'atom': ns_uri}
            items = root.findall('atom:entry', ns)
        elif is_atom:
            items = root.findall('entry')
        else:
            channel = root.find('.//channel')
            items = channel.findall('item') if channel is not None else root.findall('.//item')
        
        if not items:
            print(f"  ⚠️ {name}: No items found")
            return []
        
        for item in items[:12]:  # 每源最多12条
            try:
                # 标题
                title = ""
                if is_atom:
                    title_elem = item.find('atom:title', ns) or item.find('title')
                else:
                    title_elem = item.find('title')
                if title_elem is not None and title_elem.text:
                    title = clean_html(title_elem.text)
                
                # 链接
                link = ""
                if is_atom:
                    link_elem = item.find('atom:link', ns) or item.find('link')
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
                    # 翻译标题和摘要
                    title_zh = translate_with_keywords(title, is_title=True)
                    desc_zh = translate_with_keywords(desc)
                    
                    news_items.append({
                        'title': title_zh[:180],
                        'source': name,
                        'url': link.strip(),
                        'summary': (desc_zh[:150] + '...') if len(desc_zh) > 150 else desc_zh,
                        'publishedAt': pub_date,
                        'type': 'news'
                    })
            except Exception as e:
                continue
        
        return news_items
        
    except subprocess.TimeoutExpired:
        print(f"  ❌ {name}: Timeout")
        return []
    except Exception as e:
        print(f"  ❌ {name}: Error - {e}")
        return []

# Product fetching functions (simplified)
def fetch_product_hunt():
    """Fetch ProductHunt products"""
    products = []
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '20', 
             'https://www.producthunt.com/feed'],
            capture_output=True, text=True, timeout=25
        )
        if result.returncode == 0 and result.stdout:
            try:
                root = ET.fromstring(result.stdout)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                entries = root.findall('atom:entry', ns) or root.findall('entry')
                for entry in entries[:3]:
                    title_elem = entry.find('atom:title', ns) or entry.find('title')
                    link_elem = entry.find('atom:link', ns) or entry.find('link')
                    if title_elem is not None:
                        title = clean_html(title_elem.text or '')
                        link = link_elem.get('href', '') if link_elem is not None else ''
                        if title and link:
                            products.append({
                                'title': title,
                                'source': 'Product Hunt',
                                'url': link,
                                'summary': f"{title} - 热门新产品",
                                'type': 'product'
                            })
            except:
                pass
    except:
        pass
    return products[:2]

def fetch_github_trending():
    """Fetch GitHub trending"""
    products = []
    try:
        query = "machine learning OR llm OR chatgpt"
        encoded = urllib.parse.quote(query)
        url = f"https://api.github.com/search/repositories?q={encoded}&sort=updated&order=desc&per_page=5"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        for item in data.get('items', [])[:2]:
            title = item.get('name', '')
            desc = item.get('description', '') or "GitHub热门项目"
            url = item.get('html_url', '')
            stars = item.get('stargazers_count', 0)
            if title and url:
                desc_zh = translate_with_keywords(desc)
                products.append({
                    'title': title,
                    'source': 'GitHub',
                    'url': url,
                    'summary': f"{desc_zh} ⭐ {stars:,}" if stars else desc_zh,
                    'type': 'product'
                })
    except Exception as e:
        print(f"  GitHub error: {e}")
    return products[:2]

def fetch_hackernews():
    """Fetch HackerNews"""
    products = []
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '15', 
             'https://news.ycombinator.com/rss'],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0 and result.stdout:
            root = ET.fromstring(result.stdout)
            channel = root.find('.//channel')
            if channel:
                items = channel.findall('.//item')
                for item in items[:5]:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    if title_elem is not None and link_elem is not None:
                        title = clean_html(title_elem.text or '')
                        link = link_elem.text or ''
                        if 'Show HN' in title or 'Launch HN' in title:
                            clean_title = title.replace('Show HN:', '').replace('Launch HN', '').strip()
                            if clean_title and link:
                                products.append({
                                    'title': clean_title[:60],
                                    'source': 'HackerNews',
                                    'url': link,
                                    'summary': "HackerNews社区热门项目",
                                    'type': 'product'
                                })
                                break
    except:
        pass
    if not products:
        products.append({
            'title': 'Show HN项目',
            'source': 'HackerNews',
            'url': 'https://news.ycombinator.com/show',
            'summary': 'HackerNews社区热门项目精选',
            'type': 'product'
        })
    return products[:1]

def fetch_toolify():
    """Fetch Toolify"""
    return [{
        'title': 'Toolify AI',
        'source': 'Toolify',
        'url': 'https://www.toolify.ai',
        'summary': 'AI工具导航网站，汇集全球最新AI应用',
        'type': 'product'
    }]

def fetch_reddit():
    """Fetch Reddit"""
    return [{
        'title': 'Reddit AI社区',
        'source': 'Reddit',
        'url': 'https://www.reddit.com/r/ArtificialInteligence/',
        'summary': 'Reddit AI讨论社区热门话题',
        'type': 'product'
    }]

def load_history():
    """Load history"""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        cutoff = now_taipei() - timedelta(days=HISTORY_DAYS)
        filtered = []
        for item in history:
            try:
                pub_date = item.get('fetched_at', '')
                if pub_date:
                    item_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    if item_date > cutoff:
                        filtered.append(item)
            except:
                filtered.append(item)
        return filtered
    except:
        return []

def save_history(history):
    """Save history"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def generate_quote(news_items, products, date_str):
    """Generate daily quote"""
    import hashlib
    quotes = [
        "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。",
        "每一次模型的迭代，都是人类理解智能本质的一次尝试。",
        "AI 不是替代人类，而是放大人类的可能性。",
        "最好的产品，是让技术隐形，让体验自然。",
        "创新往往发生在不同学科的交界处。",
        "伟大的工具，是让人忘记工具本身的存在。",
        "代码是写给人看的，顺便让机器执行。",
        "在信息爆炸的时代，筛选和品味比获取更重要。",
        "AI的进化速度提醒我们：保持学习是唯一不变的竞争力。",
        "技术的民主化，让创意的门槛不断降低，想象力的价值不断升高。"
    ]
    day_hash = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    return quotes[day_hash % len(quotes)]

def main():
    """Main function"""
    print("="*70)
    print("小羽毛AI早报 - RSS抓取系统 (修复版 v3.0)")
    print(f"时间: {now_taipei().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    history = load_history()
    history_urls = {item['url'] for item in history}
    added_today = set()
    
    # Fetch news from 13 sources
    print("\n📰 抓取新闻 (13个源)...")
    all_news = []
    source_stats = {}
    
    for name, url in RSS_SOURCES.items():
        print(f"\n🌐 {name}")
        items = fetch_rss(url, name)
        new_items = []
        for item in items:
            if item['url'] not in history_urls and item['url'] not in added_today:
                item['fetched_at'] = now_taipei().isoformat()
                new_items.append(item)
                added_today.add(item['url'])
        all_news.extend(new_items)
        source_stats[name] = len(new_items)
        print(f"   ✅ 新增 {len(new_items)}/{len(items)} 条")
    
    # Fetch products
    print("\n🛍️ 抓取产品...")
    all_products = []
    
    ph = fetch_product_hunt()
    for item in ph:
        if item['url'] not in history_urls and item['url'] not in added_today:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today.add(item['url'])
    print(f"   ProductHunt: {len(ph)} 个")
    
    gh = fetch_github_trending()
    for item in gh:
        if item['url'] not in history_urls and item['url'] not in added_today:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today.add(item['url'])
    print(f"   GitHub: {len(gh)} 个")
    
    hn = fetch_hackernews()
    for item in hn:
        if item['url'] not in history_urls and item['url'] not in added_today:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today.add(item['url'])
    print(f"   HackerNews: {len(hn)} 个")
    
    # Deduplicate
    seen_titles = set()
    final_news = []
    for item in all_news:
        simple = item['title'].lower().replace(' ', '')[:25]
        if simple not in seen_titles:
            seen_titles.add(simple)
            final_news.append(item)
    
    seen_products = set()
    final_products = []
    for item in all_products:
        simple = item['title'].lower().replace(' ', '')[:25]
        if simple not in seen_products:
            seen_products.add(simple)
            final_products.append(item)
    
    # Limit
    final_news = final_news[:12]
    final_products = final_products[:5]
    
    # Output
    today_str = now_taipei().strftime("%Y-%m-%d")
    quote = generate_quote(final_news, final_products, today_str)
    
    output = {
        "date": now_taipei().strftime("%Y年%m月%d日"),
        "news": final_news,
        "products": final_products,
        "quote": quote,
        "summary": f"今日 AI 领域 {len(final_news)} 条精选资讯，{len(final_products)} 款创新产品值得关注。",
        "meta": {
            "rss_sources_total": 13,
            "rss_sources_success": sum(1 for c in source_stats.values() if c > 0),
            "rss_sources_failed": sum(1 for c in source_stats.values() if c == 0),
            "products_target": 5,
            "products_actual": len(final_products)
        }
    }
    
    with open("daily_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # Update news.ts
    try:
        subprocess.run(["python3", "update_news_ts.py"], check=True, timeout=30)
    except Exception as e:
        print(f"\n⚠️ update_news_ts.py 失败: {e}")
    
    save_history(history + final_news + final_products)
    
    # Stats
    print("\n" + "="*70)
    print("📊 抓取统计")
    print("="*70)
    success_count = sum(1 for c in source_stats.values() if c > 0)
    print(f"新闻源: {success_count}/13 成功")
    print(f"新闻: {len(final_news)} 条")
    print(f"产品: {len(final_products)} 个")
    
    print("\n📈 来源分布:")
    for name, count in sorted(source_stats.items(), key=lambda x: -x[1]):
        if count > 0:
            pct = count / len(final_news) * 100 if final_news else 0
            bar = "█" * int(pct / 3)
            print(f"  {name:20s} {count:2d}条 ({pct:4.1f}%) {bar}")
    
    print("\n✅ 完成! 数据已保存到 daily_data.json")
    
    # Check if meets requirements
    if success_count >= 8 and len(final_news) >= 10:
        print("\n🎉 达到交付标准!")
        return 0
    else:
        print("\n⚠️ 未达到交付标准")
        return 1

if __name__ == "__main__":
    exit(main())
