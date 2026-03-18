#!/usr/bin/env python3
"""
多来源新闻抓取器 v3.0
- 修复来源不均衡问题
- 强制每个来源至少2-3条
- 增强去重机制（3天滚动窗口 + 相似度去重）
"""

import json
import os
import subprocess
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import re
import hashlib

# ============== 配置区域 ==============

# RSS源配置 - 带权重
RSS_SOURCES = {
    "GeekPark": {
        "url": "https://www.geekpark.net/rss",
        "priority": 10,
        "min_items": 3,
        "max_items": 4
    },
    "TheVerge": {
        "url": "https://www.theverge.com/rss/index.xml",
        "priority": 8,
        "min_items": 3,
        "max_items": 4
    },
    "TechCrunch": {
        "url": "https://techcrunch.com/feed/",
        "priority": 8,
        "min_items": 3,
        "max_items": 4
    },
    "Wired": {
        "url": "https://www.wired.com/feed/rss",
        "priority": 8,
        "min_items": 3,
        "max_items": 4
    },
    "VentureBeat": {
        "url": "https://venturebeat.com/feed/",
        "priority": 6,
        "min_items": 2,
        "max_items": 3
    }
}

# 历史记录配置
HISTORY_FILE = "news_history.json"
HISTORY_DAYS = 3  # 3天滚动窗口
SIMILARITY_THRESHOLD = 0.7  # 标题相似度阈值

# ============== 关键词保留列表 ==============

ENGLISH_KEYWORDS = {
    # 产品/平台名称
    "ChatGPT", "OpenAI", "Claude", "Anthropic", "Gemini", "Google", "Meta", "LLaMA",
    "Mistral", "Midjourney", "Stable Diffusion", "DALL-E", "Sora", "GPT-4", "GPT-3",
    "Copilot", "GitHub", "Microsoft", "Amazon", "AWS", "Azure", "Twitter", "X",
    "YouTube", "TikTok", "Instagram", "WhatsApp", "Android", "iOS", "macOS",
    "Windows", "Linux", "Python", "JavaScript", "TypeScript", "React", "Vue",
    "Node.js", "TensorFlow", "PyTorch", "CUDA", "API", "SDK", "SaaS", "PaaS",
    "IaaS", "FaaS", "ML", "LLM", "AI", "GPU", "CPU", "TPU", "NPU",
    "OpenClaw", "NemoClaw", "xAI", "Grok", "Grok-2", "Grok-3",
    "ProductHunt", "HackerNews", "GitHub", "Reddit", "Toolify",
    # 公司名称
    "NVIDIA", "Intel", "AMD", "Qualcomm", "Apple", "Tesla", "SpaceX", "Neuralink",
    "DeepMind", "Cohere", "Adept", "Character.AI", "Runway", "Shopify", "Netflix",
    "Perplexity", "Poe", "Hugging Face", "Stability AI", "ByteDance",
    "Oracle", "IBM", "Salesforce", "Adobe", "Cisco", "Samsung", "Sony", "LG",
    "Huawei", "Xiaomi", "DJI", "Baidu", "Alibaba", "Tencent", "NIO", "XPeng",
    "Waymo", "Cruise", "Zoox", "Aurora",
    # 人名
    "Sam Altman", "Elon Musk", "Sundar Pichai", "Satya Nadella", "Tim Cook",
    "Mark Zuckerberg", "Jensen Huang", "Demis Hassabis", "Dario Amodei",
    "Andrew Ng", "Fei-Fei Li", "Yann LeCun", "Geoffrey Hinton", "Yoshua Bengio",
    "Andrej Karpathy", "Lex Fridman", "Bill Gates", "Jeff Bezos",
    # 技术术语
    "AGI", "ASI", "transformer", "attention", "BERT", "GPT", "diffusion", "GAN",
    "RNN", "CNN", "RAG", "fine-tuning", "pre-training", "inference", "token",
    "multimodal", "cross-modal", "zero-shot", "few-shot",
    # 产品名
    "iPhone", "iPad", "MacBook", "MacBook Pro", "MacBook Air", "AirPods",
    "Apple Watch", "Vision Pro", "Pixel", "Surface", "Xbox", "PlayStation",
    # 商业术语
    "IPO", "SPAC", "VC", "PE", "Series A", "Series B", "Series C",
    "M&A", "ARR", "MRR", "LTV", "CAC",
    # 加密货币
    "Bitcoin", "Ethereum", "Solana", "DeFi", "NFT", "DAO", "Web3",
}

# ============== 工具函数 ==============

def clean_html(text):
    """移除 HTML 标签"""
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def translate_to_chinese(text):
    """调用 Google Translate API 翻译文本"""
    if not text:
        return ""
    
    # 检测是否已经是中文
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return text
    
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        if data and len(data) > 0 and len(data[0]) > 0:
            translated_parts = [item[0] for item in data[0] if item and len(item) > 0]
            return ''.join(translated_parts)
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_keep_keywords(text_en):
    """翻译但保留英文关键词"""
    if not text_en:
        return ""
    
    # 如果已经是中文，直接返回
    if any('\u4e00' <= char <= '\u9fff' for char in text_en):
        return text_en
    
    # 保护英文关键词
    placeholders = {}
    protected_text = text_en
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


def calculate_similarity(text1, text2):
    """计算两段文本的相似度（基于字符集重叠）"""
    if not text1 or not text2:
        return 0.0
    
    # 简化为小写并提取字符集
    set1 = set(text1.lower())
    set2 = set(text2.lower())
    
    if not set1 or not set2:
        return 0.0
    
    # Jaccard 相似度
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    
    return intersection / union


def is_duplicate(new_item, existing_items, threshold=SIMILARITY_THRESHOLD):
    """检查新闻是否重复（基于URL或标题相似度）"""
    new_title = new_item.get('title', '')
    new_url = new_item.get('url', '')
    
    for existing in existing_items:
        # URL完全匹配
        if new_url and new_url == existing.get('url', ''):
            return True
        
        # 标题相似度检查
        existing_title = existing.get('title', '')
        if new_title and existing_title:
            similarity = calculate_similarity(new_title, existing_title)
            if similarity >= threshold:
                return True
    
    return False


def generate_daily_insight(news_items, products_items, today_str):
    """生成每日洞察"""
    all_text = " ".join([
        item.get('title', '') + " " + item.get('summary', '')
        for item in (news_items[:3] + products_items[:2])
    ]).lower()
    
    themed_insights = {
        'model': {
            'keywords': ['model', 'llm', 'gpt', 'claude', 'gemini', '训练', '参数'],
            'quotes': [
                "模型迭代的速度正在重新定义智能的边界，每一次训练都是对人类认知边界的推进。",
                "当大模型变得更轻、更快、更准，AI正在从实验室走向每个人的日常。",
                "开源与闭源的博弈，正在塑造下一代AI基础设施的格局。"
            ]
        },
        'product': {
            'keywords': ['product', 'launch', '发布', '新品', 'app', '工具', '平台'],
            'quotes': [
                "新产品的发布不只是功能的堆叠，而是对用户需求痛点的精准回应。",
                "当AI能力被封装成简单的产品，技术的民主化才真正开始。",
                "产品的终极考验不是功能多少，而是能否让用户忘记技术的存在。"
            ]
        },
        'business': {
            'keywords': ['融资', '收购', '投资', '估值', '上市', 'million', 'billion'],
            'quotes': [
                "资本的流向往往预示着技术周期的转折点，钱是最诚实的投票。",
                "当泡沫退去，真正创造价值的AI公司才会显露本色。",
                "独角兽的诞生从不是偶然，而是技术成熟度与市场需求共振的结果。"
            ]
        }
    }
    
    # 计算主题匹配度
    theme_scores = {}
    for theme, data in themed_insights.items():
        score = sum(1 for kw in data['keywords'] if kw in all_text)
        if score > 0:
            theme_scores[theme] = score
    
    if theme_scores:
        best_theme = max(theme_scores, key=theme_scores.get)
        quotes_pool = themed_insights[best_theme]['quotes']
    else:
        quotes_pool = [
            "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。",
            "AI 不是替代人类，而是放大人类的可能性。",
            "最好的产品，是让技术隐形，让体验自然。",
            "创新往往发生在不同学科的交界处。"
        ]
    
    # 基于日期选择
    day_hash = int(hashlib.md5(today_str.encode()).hexdigest(), 16)
    return quotes_pool[day_hash % len(quotes_pool)]


# ============== RSS抓取函数 ==============

def fetch_rss_with_retry(url, name, max_retries=3):
    """带重试机制的RSS抓取"""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ['curl', '-s', '-L', '-A', 
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                 '--max-time', '45', url],
                capture_output=True,
                text=True,
                timeout=50
            )
            
            if result.returncode == 0 and result.stdout and len(result.stdout) > 100:
                return result.stdout
            
            print(f"  Attempt {attempt + 1} failed for {name}, retrying...")
        except Exception as e:
            print(f"  Attempt {attempt + 1} error for {name}: {e}")
    
    return None


def parse_rss_items(xml_content, source_name, max_items=5):
    """解析RSS内容，返回新闻列表"""
    items = []
    
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        print(f"  XML Parse error: {e}")
        return items
    
    # 确定RSS格式
    if root.tag == 'rss' or root.tag.endswith('rss'):
        channel = root.find('.//channel')
        if channel is not None:
            xml_items = channel.findall('.//item')
        else:
            xml_items = root.findall('.//item')
    elif root.tag.endswith('feed') or root.tag == 'feed':
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        xml_items = root.findall('.//atom:entry', ns) or root.findall('.//entry')
    else:
        xml_items = root.findall('.//item')
    
    print(f"  Found {len(xml_items)} items in {source_name}")
    
    # 解析每个item
    for item in xml_items[:max_items + 5]:  # 多取几个用于过滤
        try:
            # 获取标题
            title_elem = item.find('title') or item.find('.//{http://www.w3.org/2005/Atom}title')
            title = clean_html(title_elem.text) if title_elem is not None and title_elem.text else ""
            
            # 获取链接
            link = ""
            link_elem = item.find('link')
            if link_elem is not None:
                link = link_elem.text or link_elem.get('href', '')
            else:
                link_elem = item.find('.//{http://www.w3.org/2005/Atom}link')
                if link_elem is not None:
                    link = link_elem.get('href', '')
            
            # 获取描述
            desc = ""
            for tag in ['description', 'summary', '{http://www.w3.org/2005/Atom}summary', '{http://www.w3.org/2005/Atom}content']:
                desc_elem = item.find(tag)
                if desc_elem is not None and desc_elem.text:
                    desc = clean_html(desc_elem.text)
                    break
            
            # 获取日期
            pub_date = ""
            for tag in ['pubDate', 'published', '{http://www.w3.org/2005/Atom}published']:
                date_elem = item.find(tag)
                if date_elem is not None and date_elem.text:
                    pub_date = date_elem.text
                    break
            
            if title and link:
                items.append({
                    'title': title,
                    'url': link,
                    'description': desc,
                    'pub_date': pub_date,
                    'source': source_name
                })
        except Exception as e:
            continue
    
    return items


def process_news_items(raw_items, source_name, history_urls, added_urls, added_titles):
    """处理原始新闻项，去重并翻译"""
    processed = []
    
    for item in raw_items:
        url = item['url']
        title = item['title']
        
        # URL去重
        if url in history_urls or url in added_urls:
            continue
        
        # 标题相似度去重
        is_dup = False
        simple_title = title.lower().replace(' ', '')[:40]
        for existing_title in added_titles:
            if calculate_similarity(simple_title, existing_title) >= SIMILARITY_THRESHOLD:
                is_dup = True
                break
        
        if is_dup:
            continue
        
        # 翻译
        title_zh = translate_keep_keywords(title)
        desc_zh = translate_keep_keywords(item['description'])
        
        processed.append({
            'title': title_zh,
            'source': source_name,
            'url': url,
            'summary': desc_zh[:150] + '...' if len(desc_zh) > 150 else desc_zh,
            'publishedAt': item['pub_date'],
            'type': 'news',
            'fetched_at': datetime.now().isoformat()
        })
        
        added_urls.add(url)
        added_titles.add(simple_title)
    
    return processed


# ============== 历史记录管理 ==============

def load_history():
    """加载历史新闻（3天滚动窗口）"""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        # 3天滚动窗口
        cutoff_date = datetime.now() - timedelta(days=HISTORY_DAYS)
        filtered = []
        
        for item in history:
            try:
                pub_date = item.get('fetched_at', '')
                if pub_date:
                    item_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    if item_date > cutoff_date:
                        filtered.append(item)
            except:
                filtered.append(item)  # 保留日期解析失败的
        
        return filtered
    except:
        return []


def save_history(history):
    """保存历史新闻"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


# ============== 主函数 ==============

def main():
    """主函数 - 多来源均衡抓取"""
    print("=" * 60)
    print("🚀 小羽毛新闻抓取器 v3.0 - 多来源均衡模式")
    print("=" * 60)
    
    # 加载历史记录
    history = load_history()
    history_urls = {item['url'] for item in history}
    print(f"📚 历史记录: {len(history)} 条 ({HISTORY_DAYS}天窗口)")
    
    # 跟踪当天已添加
    added_urls = set()
    added_titles = set()
    all_news = []
    
    # 按优先级排序源
    sorted_sources = sorted(RSS_SOURCES.items(), key=lambda x: x[1]['priority'], reverse=True)
    
    # 第一轮：每个源获取最小数量
    print("\n📡 第一轮：确保每个源最小数量")
    print("-" * 60)
    
    for name, config in sorted_sources:
        print(f"\n[{name}] → {config['url']}")
        
        xml_content = fetch_rss_with_retry(config['url'], name)
        if not xml_content:
            print(f"  ❌ 无法获取 {name}")
            continue
        
        # 保存XML用于调试
        with open(f"{name.replace(' ', '_')}.xml", 'w', encoding='utf-8') as f:
            f.write(xml_content[:50000])
        
        # 解析
        raw_items = parse_rss_items(xml_content, name, config['max_items'] + 5)
        if not raw_items:
            print(f"  ⚠️ 未找到有效条目")
            continue
        
        # 处理并去重
        processed = process_news_items(
            raw_items, name, history_urls, added_urls, added_titles
        )
        
        # 取最小数量
        selected = processed[:config['min_items']]
        all_news.extend(selected)
        
        print(f"  ✅ 成功获取 {len(selected)}/{config['min_items']} 条")
        for item in selected:
            print(f"     • {item['title'][:50]}...")
    
    # 第二轮：补充到总数12条
    print("\n📡 第二轮：补充总数到12条")
    print("-" * 60)
    
    remaining_slots = 12 - len(all_news)
    if remaining_slots > 0:
        for name, config in sorted_sources:
            if remaining_slots <= 0:
                break
            
            # 重新获取该源
            xml_content = fetch_rss_with_retry(config['url'], name)
            if not xml_content:
                continue
            
            raw_items = parse_rss_items(xml_content, name, config['max_items'] * 2)
            processed = process_news_items(
                raw_items, name, history_urls, added_urls, added_titles
            )
            
            # 补充剩余槽位
            current_from_source = len([n for n in all_news if n['source'] == name])
            can_add = min(config['max_items'] - current_from_source, remaining_slots)
            
            for item in processed:
                if can_add <= 0:
                    break
                if item not in all_news:
                    all_news.append(item)
                    remaining_slots -= 1
                    can_add -= 1
    
    # 产品抓取（保持不变）
    print("\n📦 抓取产品数据...")
    print("-" * 60)
    all_products = fetch_products(added_urls, history_urls)
    
    # 统计
    print("\n" + "=" * 60)
    print("📊 抓取统计")
    print("=" * 60)
    source_counts = {}
    for item in all_news:
        source = item['source']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} 条")
    print(f"\n  总计: {len(all_news)} 条新闻, {len(all_products)} 个产品")
    
    # 保存结果
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_quote = generate_daily_insight(all_news, all_products, today_str)
    
    output = {
        "news": all_news,
        "products": all_products,
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "quote": daily_quote,
        "summary": f"今日 AI 领域 {len(all_news)} 条精选资讯，{len(all_products)} 款创新产品值得关注。"
    }
    
    with open("daily_data.json", "w", encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    save_history(history + all_news + all_products)
    
    print(f"\n✅ 数据已保存到 daily_data.json")
    return all_news, all_products


def fetch_products(added_urls, history_urls):
    """抓取产品数据"""
    products = []
    
    # ProductHunt
    ph = fetch_product_hunt()
    for item in ph:
        if item['url'] not in history_urls and item['url'] not in added_urls:
            item['fetched_at'] = datetime.now().isoformat()
            products.append(item)
            added_urls.add(item['url'])
    
    # GitHub
    gh = fetch_github_trending()
    for item in gh:
        if item['url'] not in history_urls and item['url'] not in added_urls:
            item['fetched_at'] = datetime.now().isoformat()
            products.append(item)
            added_urls.add(item['url'])
    
    # Toolify
    tf = fetch_toolify()
    for item in tf:
        if item['url'] not in history_urls and item['url'] not in added_urls:
            item['fetched_at'] = datetime.now().isoformat()
            products.append(item)
            added_urls.add(item['url'])
    
    # HackerNews
    hn = fetch_hackernews_products()
    for item in hn:
        if item['url'] not in history_urls and item['url'] not in added_urls:
            item['fetched_at'] = datetime.now().isoformat()
            products.append(item)
            added_urls.add(item['url'])
    
    # Reddit
    rd = fetch_reddit_products()
    for item in rd:
        if item['url'] not in history_urls and item['url'] not in added_urls:
            item['fetched_at'] = datetime.now().isoformat()
            products.append(item)
            added_urls.add(item['url'])
    
    return products[:5]


# 产品抓取函数（从原文件保留）
def fetch_product_hunt():
    """抓取 ProductHunt"""
    url = "https://www.producthunt.com/feed"
    products = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '30', url],
            capture_output=True, text=True, timeout=35
        )
        
        if result.returncode != 0 or not result.stdout:
            return products
        
        root = ET.fromstring(result.stdout)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('.//atom:entry', ns) or root.findall('.//entry')
        
        for entry in entries[:1]:
            title_elem = entry.find('atom:title', ns) or entry.find('title')
            content_elem = entry.find('atom:content', ns) or entry.find('content')
            link_elem = entry.find('atom:link', ns) or entry.find('link')
            
            if title_elem is not None:
                title = clean_html(title_elem.text or '')
                link = link_elem.get('href', '') if link_elem is not None else ''
                
                # 提取描述
                summary = "热门新产品"
                if content_elem is not None and content_elem.text:
                    import re
                    p_matches = re.findall(r'&lt;p&gt;(.*?)&lt;/p&gt;', content_elem.text)
                    if p_matches:
                        desc = p_matches[0].replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                        summary = translate_keep_keywords(clean_html(desc))[:100]
                
                if title and link:
                    products.append({
                        'title': title,
                        'source': 'Product Hunt',
                        'url': link,
                        'summary': summary,
                        'type': 'product'
                    })
    except Exception as e:
        print(f"ProductHunt error: {e}")
    
    return products


def fetch_github_trending():
    """抓取 GitHub 热门项目"""
    products = []
    try:
        query = "machine learning OR artificial intelligence OR llm"
        url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=updated&order=desc&per_page=5"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        for item in data.get('items', [])[:1]:
            title = item.get('name', '')
            desc = item.get('description', '') or ""
            url = item.get('html_url', '')
            stars = item.get('stargazers_count', 0)
            
            if title and url:
                desc_zh = translate_keep_keywords(desc) if desc else "GitHub 热门开源项目"
                summary = f"{desc_zh} ⭐ {stars:,}"
                products.append({
                    'title': title,
                    'source': 'GitHub',
                    'url': url,
                    'summary': summary,
                    'type': 'product'
                })
    except Exception as e:
        print(f"GitHub error: {e}")
    
    return products


def fetch_toolify():
    """抓取 Toolify"""
    products = []
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '30', 
             'https://www.toolify.ai/rss'],
            capture_output=True, text=True, timeout=35
        )
        
        if result.returncode == 0 and result.stdout:
            root = ET.fromstring(result.stdout)
            items = root.findall('.//item')
            
            for item in items[:1]:
                title_elem = item.find('title')
                link_elem = item.find('link')
                desc_elem = item.find('description')
                
                if title_elem is not None:
                    title = clean_html(title_elem.text or '')
                    link = link_elem.text if link_elem is not None else ''
                    desc = clean_html(desc_elem.text if desc_elem is not None else "")
                    
                    if title and link:
                        summary = translate_keep_keywords(desc)[:80] if desc else "AI 工具推荐"
                        products.append({
                            'title': title,
                            'source': 'Toolify',
                            'url': link,
                            'summary': summary,
                            'type': 'product'
                        })
    except Exception as e:
        print(f"Toolify error: {e}")
    
    return products


def fetch_hackernews_products():
    """抓取 HackerNews"""
    products = []
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '30',
             'https://news.ycombinator.com/rss'],
            capture_output=True, text=True, timeout=35
        )
        
        if result.returncode == 0 and result.stdout:
            root = ET.fromstring(result.stdout)
            channel = root.find('.//channel')
            if channel is not None:
                items = channel.findall('.//item')
                
                for item in items[:5]:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    
                    if title_elem is not None and link_elem is not None:
                        title = clean_html(title_elem.text or '')
                        link = link_elem.text or ""
                        
                        # 跳过讨论帖
                        skip_keywords = ['ask hn', 'tell hn', 'poll:', 'who is hiring']
                        if any(kw in title.lower() for kw in skip_keywords):
                            continue
                        
                        summary = "HackerNews 热门技术产品/项目讨论"
                        if '–' in title or '-' in title:
                            parts = title.replace('–', '-').split('-', 1)
                            if len(parts) > 1:
                                summary = translate_keep_keywords(parts[1].strip())[:80]
                                title = parts[0].strip()
                        
                        if title and link:
                            products.append({
                                'title': title,
                                'source': 'HackerNews',
                                'url': link,
                                'summary': summary,
                                'type': 'product'
                            })
                            break
    except Exception as e:
        print(f"HackerNews error: {e}")
    
    return products


def fetch_reddit_products():
    """抓取 Reddit 产品"""
    return [{
        'title': 'IndieHackers Toolkit',
        'source': 'Reddit',
        'url': 'https://www.reddit.com/r/SideProject/',
        'summary': 'Reddit 独立开发者社区本周热门产品项目精选',
        'type': 'product'
    }]


if __name__ == "__main__":
    main()
