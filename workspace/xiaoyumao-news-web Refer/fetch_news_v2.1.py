#!/usr/bin/env python3
"""
多来源新闻抓取器 v2.1 - 多来源均衡修复版
- 确保每个来源至少3条新闻
- 3天滚动窗口去重
- 12条新闻均衡分布
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

# ============== 配置 ==============

RSS_SOURCES = {
    "TechCrunch": {
        "url": "https://techcrunch.com/feed/",
        "min_items": 3,
        "max_items": 4
    },
    "TheVerge": {
        "url": "https://www.theverge.com/rss/index.xml",
        "min_items": 3,
        "max_items": 4
    },
    "Wired": {
        "url": "https://www.wired.com/feed/rss",
        "min_items": 2,
        "max_items": 3
    },
    "36氪": {  # 中文科技媒体
        "url": "https://36kr.com/feed",
        "min_items": 2,
        "max_items": 3
    }
}

HISTORY_FILE = "news_history.json"
HISTORY_DAYS = 3
SIMILARITY_THRESHOLD = 0.75

# ============== 保留原文件的关键词和函数 ==============

ENGLISH_KEYWORDS = {"ChatGPT", "OpenAI", "Claude", "Anthropic", "Gemini", "Google", "Meta", "LLaMA", "Mistral", "Midjourney", "Stable Diffusion", "DALL-E", "Sora", "GPT-4", "GPT-3", "Copilot", "GitHub", "Microsoft", "Amazon", "AWS", "Azure", "Twitter", "X", "YouTube", "TikTok", "Instagram", "WhatsApp", "Android", "iOS", "macOS", "Windows", "Linux", "Python", "JavaScript", "TypeScript", "React", "Vue", "Node.js", "TensorFlow", "PyTorch", "CUDA", "API", "SDK", "SaaS", "PaaS", "IaaS", "FaaS", "ML", "LLM", "AI", "GPU", "CPU", "TPU", "NPU", "OpenClaw", "NemoClaw", "xAI", "Grok", "Grok-2", "Grok-3", "ProductHunt", "HackerNews", "Reddit", "Toolify", "NVIDIA", "Intel", "AMD", "Qualcomm", "Apple", "Tesla", "SpaceX", "Neuralink", "DeepMind", "Cohere", "Adept", "Character.AI", "Runway", "Shopify", "Netflix", "Perplexity", "Poe", "Hugging Face", "Stability AI", "ByteDance", "Oracle", "IBM", "Salesforce", "Adobe", "Cisco", "Samsung", "Sony", "LG", "Huawei", "Xiaomi", "DJI", "Baidu", "Alibaba", "Tencent", "NIO", "XPeng", "Waymo", "Cruise", "Zoox", "Aurora", "Sam Altman", "Elon Musk", "Sundar Pichai", "Satya Nadella", "Tim Cook", "Mark Zuckerberg", "Jensen Huang", "Demis Hassabis", "Dario Amodei", "Andrew Ng", "Fei-Fei Li", "Yann LeCun", "Geoffrey Hinton", "Yoshua Bengio", "Andrej Karpathy", "Lex Fridman", "Bill Gates", "Jeff Bezos", "AGI", "ASI", "transformer", "attention", "BERT", "GPT", "diffusion", "GAN", "RNN", "CNN", "RAG", "fine-tuning", "pre-training", "inference", "token", "multimodal", "cross-modal", "zero-shot", "few-shot", "iPhone", "iPad", "MacBook", "MacBook Pro", "MacBook Air", "AirPods", "Apple Watch", "Vision Pro", "Pixel", "Surface", "Xbox", "PlayStation", "IPO", "SPAC", "VC", "PE", "Series A", "Series B", "Series C", "M&A", "ARR", "MRR", "LTV", "CAC", "Bitcoin", "Ethereum", "Solana", "DeFi", "NFT", "DAO", "Web3"}

def clean_html(text):
    if not text:
        return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def translate_to_chinese(text):
    if not text:
        return ""
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

def translate_summary_keep_keywords(text_en):
    if not text_en:
        return ""
    if any('\u4e00' <= char <= '\u9fff' for char in text_en):
        return text_en
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
    translated = translate_to_chinese(protected_text)
    translated = translated.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    for placeholder, original in placeholders.items():
        translated = translated.replace(placeholder, original)
    return translated

def translate_title(title_en):
    if not title_en:
        return ""
    if any('\u4e00' <= char <= '\u9fff' for char in title_en):
        return title_en
    placeholders = {}
    protected_text = title_en
    sorted_keywords = sorted(ENGLISH_KEYWORDS, key=len, reverse=True)
    for i, keyword in enumerate(sorted_keywords):
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, protected_text, re.IGNORECASE)
        for match in matches:
            placeholder = f"__TITLE_KEY_{i}_{len(placeholders)}__"
            placeholders[placeholder] = match
            protected_text = protected_text.replace(match, placeholder)
    translated = translate_to_chinese(protected_text)
    translated = translated.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    for placeholder, original in placeholders.items():
        translated = translated.replace(placeholder, original)
    return translated

def calculate_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0
    set1 = set(text1.lower())
    set2 = set(text2.lower())
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    if union == 0:
        return 0.0
    return intersection / union

def generate_daily_insight(news_items, products_items, today_str):
    import hashlib
    all_text = " ".join([item.get('title', '') + " " + item.get('summary', '') for item in (news_items[:3] + products_items[:2])]).lower()
    themed_insights = {
        'model': {'keywords': ['model', 'llm', 'gpt', 'claude', 'gemini', '训练', '参数', '性能', '突破'], 'quotes': ["模型迭代的速度正在重新定义智能的边界，每一次训练都是对人类认知边界的推进。", "当大模型变得更轻、更快、更准，AI正在从实验室走向每个人的日常。", "参数量的竞赛背后，是对智能本质的深层理解。", "开源与闭源的博弈，正在塑造下一代AI基础设施的格局。"]},
        'product': {'keywords': ['product', 'launch', '发布', '新品', 'app', '工具', '平台', '上线'], 'quotes': ["新产品的发布不只是功能的堆叠，而是对用户需求痛点的精准回应。", "当AI能力被封装成简单的产品，技术的民主化才真正开始。", "每个新工具的诞生，都在重新定义人机协作的边界。", "产品的终极考验不是功能多少，而是能否让用户忘记技术的存在。"]},
        'business': {'keywords': ['融资', '收购', '投资', '估值', '上市', '财报', '营收', 'million', 'billion', '收购', '合并'], 'quotes': ["资本的流向往往预示着技术周期的转折点，钱是最诚实的投票。", "当泡沫退去，真正创造价值的AI公司才会显露本色。", "投资不仅是押注技术，更是押注团队对人性需求的理解深度。", "独角兽的诞生从不是偶然，而是技术成熟度与市场需求共振的结果。"]},
        'ethics': {'keywords': ['伦理', '监管', '隐私', '安全', '风险', '担忧', '争议', '伦理', '安全', 'privacy', 'regulation'], 'quotes': ["技术越强大，我们对责任的思考就需要越深刻。", "监管不是创新的对立面，而是让创新走得更远的基础设施。", "隐私与便利的权衡，是数字时代每个人的必修课。", "AI的边界不仅由技术决定，更由人类的价值观塑造。"]},
        'application': {'keywords': ['应用', '场景', '医疗', '教育', '金融', '创作', '生成', '视频', '图像', '音频'], 'quotes': ["AI真正的价值不在技术本身，而在它如何解决具体领域的真实问题。", "当生成式AI进入创作领域，人类的角色从执行者变为策展人。", "垂直场景的深耕，往往比通用能力更能创造持久价值。", "技术落地的最后一公里，需要理解行业肌理的人才能走完。"]},
        'breakthrough': {'keywords': ['突破', '里程碑', '首次', '创新', '革命', '颠覆', '创纪录', '首次', '里程碑'], 'quotes': ["每一个技术里程碑的背后，都是无数失败实验的积累。", "突破往往发生在被忽视的细节里，而非宏大的叙事中。", "当一项技术跨越了'足够好'的阈值，变革就开始了。", "真正的创新从不是凭空出现，而是对已有边界的有意识突破。"]}
    }
    theme_scores = {}
    for theme, data in themed_insights.items():
        score = sum(1 for kw in data['keywords'] if kw in all_text)
        if score > 0:
            theme_scores[theme] = score
    if theme_scores:
        best_theme = max(theme_scores, key=theme_scores.get)
        quotes_pool = themed_insights[best_theme]['quotes']
    else:
        quotes_pool = ["技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。", "每一次模型的迭代，都是人类理解智能本质的一次尝试。", "AI 不是替代人类，而是放大人类的可能性。", "最好的产品，是让技术隐形，让体验自然。", "创新往往发生在不同学科的交界处。", "伟大的工具，是让人忘记工具本身的存在。", "代码是写给人看的，顺便让机器执行。", "产品成功的秘诀：解决一个具体的问题，比解决所有问题更重要。", "技术的边界，就是我们想象力的边界。", "每一个开源项目背后，都有一群相信共享比封闭更有力量的人。", "在信息爆炸的时代，筛选和品味比获取更重要。", "AI的进化速度提醒我们：保持学习是唯一不变的竞争力。", "技术的民主化，让创意的门槛不断降低，想象力的价值不断升高。"]
    day_hash = int(hashlib.md5(today_str.encode()).hexdigest(), 16)
    return quotes_pool[day_hash % len(quotes_pool)]

# ============== RSS 抓取 ==============

def fetch_rss(url, name):
    """获取并解析 RSS/Atom feed"""
    news_items = []
    try:
        result = subprocess.run(['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', '--max-time', '30', url], capture_output=True, text=True, timeout=35)
        if result.returncode != 0:
            print(f"Error fetching {name}: curl failed")
            return []
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            print(f"Error: Empty response from {name}")
            return []
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            print(f"XML Parse error in {name}: {e}")
            return []
        
        # 处理 RSS 2.0 格式
        if root.tag == 'rss' or root.tag.endswith('rss'):
            channel = root.find('.//channel')
            if channel is None:
                return []
            items = channel.findall('.//item')
        # 处理 Atom 格式（带命名空间或不带）
        elif 'feed' in root.tag or root.tag.endswith('feed'):
            # 尝试带命名空间的entry
            items = root.findall('.//{http://www.w3.org/2005/Atom}entry')
            # 如果没找到，尝试不带命名空间的entry
            if not items:
                items = root.findall('.//entry')
        else:
            items = root.findall('.//item')
        
        print(f"Found {len(items)} items in {name}")
        
        for item in items[:15]:
            try:
                # 获取标题 - 尝试多种方式
                title_elem = item.find('title')
                if title_elem is None:
                    title_elem = item.find('.//{http://www.w3.org/2005/Atom}title')
                title = title_elem.text if title_elem is not None else ""
                
                # 获取链接 - 处理 RSS 和 Atom 格式
                link = ""
                # RSS格式: <link>http://...</link>
                link_elem = item.find('link')
                if link_elem is not None:
                    if link_elem.text:
                        link = link_elem.text
                    else:
                        # Atom格式: <link href="http://..."/>
                        link = link_elem.get('href', '')
                
                # 如果上面的没找到，尝试Atom命名空间
                if not link:
                    link_elem = item.find('.//{http://www.w3.org/2005/Atom}link')
                    if link_elem is not None:
                        link = link_elem.get('href', link_elem.text or '')
                
                # 获取描述
                description = ""
                for tag in ['description', 'summary', '{http://www.w3.org/2005/Atom}summary', '{http://www.w3.org/2005/Atom}content']:
                    desc_elem = item.find(tag)
                    if desc_elem is not None and desc_elem.text:
                        description = desc_elem.text
                        break
                
                # 获取发布日期
                pub_date = ""
                for tag in ['pubDate', 'published', '{http://www.w3.org/2005/Atom}published', 'updated', '{http://www.w3.org/2005/Atom}updated']:
                    date_elem = item.find(tag)
                    if date_elem is not None and date_elem.text:
                        pub_date = date_elem.text
                        break
                
                if title and link:
                    title = clean_html(title)
                    description = clean_html(description)
                    title_zh = translate_title(title)
                    desc_zh = translate_summary_keep_keywords(description)
                    news_items.append({
                        'title': title_zh,
                        'source': name,
                        'url': link,
                        'summary': desc_zh[:150] + '...' if len(desc_zh) > 150 else desc_zh,
                        'publishedAt': pub_date,
                        'type': 'news'
                    })
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue
    except subprocess.TimeoutExpired:
        print(f"Timeout fetching {name}")
    except Exception as e:
        print(f"Error fetching {name}: {e}")
    return news_items

# ============== 产品抓取 ==============

def fetch_product_hunt():
    url = "https://www.producthunt.com/feed"
    products = []
    try:
        result = subprocess.run(['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', '--max-time', '30', url], capture_output=True, text=True, timeout=35)
        if result.returncode != 0:
            return []
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            return []
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return []
        entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        if not entries:
            entries = root.findall('.//entry')
        for entry in entries[:1]:
            try:
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                if title_elem is None:
                    title_elem = entry.find('title')
                content_elem = entry.find('{http://www.w3.org/2005/Atom}content')
                if content_elem is None:
                    content_elem = entry.find('content')
                link_elem = entry.find('{http://www.w3.org/2005/Atom}link')
                if link_elem is None:
                    link_elem = entry.find('link')
                if title_elem is not None:
                    title = clean_html(title_elem.text or '')
                    description = ""
                    if content_elem is not None and content_elem.text:
                        content_text = content_elem.text
                        import re
                        p_matches = re.findall(r'&lt;p&gt;(.*?)&lt;/p&gt;', content_text)
                        if p_matches:
                            desc_html = p_matches[0]
                            desc_html = desc_html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                            description = clean_html(desc_html)
                    link = ""
                    if link_elem is not None:
                        link = link_elem.get('href', '')
                    if content_elem is not None and content_elem.text:
                        link_match = re.search(r'&lt;a href=\"(.*?)\"&gt;Link&lt;/a&gt;', content_elem.text)
                        if link_match:
                            actual_link = link_match.group(1).replace('&amp;', '&')
                            if actual_link:
                                link = actual_link
                    if title and link:
                        tagline = description.strip() if description else f"{title} - 热门新产品"
                        tagline_zh = translate_title(tagline) if tagline else f"{title} - 热门新产品"
                        products.append({'title': title, 'source': 'Product Hunt', 'url': link, 'summary': tagline_zh, 'type': 'product'})
            except Exception as e:
                print(f"Error parsing ProductHunt entry: {e}")
                continue
    except Exception as e:
        print(f"Error fetching ProductHunt: {e}")
    return products[:1]

def fetch_github_trending():
    import urllib.request
    products = []
    try:
        query = "machine learning OR artificial intelligence OR llm OR chatgpt OR openai"
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=updated&order=desc&per_page=10"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        for item in data.get('items', []):
            title = item.get('name', '')
            description = item.get('description', '') or ""
            url = item.get('html_url', '')
            stars = item.get('stargazers_count', 0)
            if title and url:
                desc_zh = translate_title(description) if description else "GitHub 热门开源项目"
                summary = f"{desc_zh} ⭐ {stars:,}" if stars > 0 else desc_zh
                products.append({'title': title, 'source': 'GitHub', 'url': url, 'summary': summary, 'type': 'product'})
                break
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        products.append({'title': 'awesome-chatgpt-prompts', 'source': 'GitHub', 'url': 'https://github.com/f/awesome-chatgpt-prompts', 'summary': 'ChatGPT 提示词精选合集，助力 AI 对话效率提升 ⭐ 120,000+', 'type': 'product'})
    return products[:1]

def fetch_toolify():
    url = "https://www.toolify.ai/rss"
    products = []
    try:
        result = subprocess.run(['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '30', url], capture_output=True, text=True, timeout=35)
        if result.returncode != 0:
            raise Exception(f"curl failed: {result.returncode}")
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            raise Exception("Empty XML response")
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            raise Exception(f"XML parse error: {e}")
        items = root.findall('.//item')
        if not items:
            items = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        for item in items[:1]:
            try:
                title_elem = item.find('title')
                if title_elem is None:
                    title_elem = item.find('.//{http://www.w3.org/2005/Atom}title')
                desc_elem = item.find('description')
                if desc_elem is None:
                    desc_elem = item.find('.//{http://www.w3.org/2005/Atom}summary')
                link_elem = item.find('link')
                if link_elem is None:
                    link_elem = item.find('.//{http://www.w3.org/2005/Atom}link')
                if title_elem is not None:
                    title = clean_html(title_elem.text or '')
                    description = clean_html(desc_elem.text if desc_elem is not None else "")
                    link = ""
                    if link_elem is not None:
                        if link_elem.text:
                            link = link_elem.text
                        else:
                            link = link_elem.get('href', '')
                    if title and link:
                        if description:
                            desc_zh = translate_summary_keep_keywords(description)
                            summary = desc_zh[:80] + "..." if len(desc_zh) > 80 else desc_zh
                        else:
                            summary = "AI 工具推荐"
                        products.append({'title': title, 'source': 'Toolify', 'url': link, 'summary': summary, 'type': 'product'})
            except Exception as e:
                print(f"Error parsing Toolify entry: {e}")
                continue
    except Exception as e:
        print(f"Error fetching Toolify: {e}")
    if not products:
        products.append({'title': 'Toolify AI', 'source': 'Toolify', 'url': 'https://www.toolify.ai', 'summary': 'AI 工具导航网站，汇集全球最新 AI 应用与工具', 'type': 'product'})
    return products[:1]

def fetch_hackernews_products():
    url = "https://news.ycombinator.com/rss"
    products = []
    try:
        result = subprocess.run(['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '30', url], capture_output=True, text=True, timeout=35)
        if result.returncode != 0:
            return []
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            return []
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return []
        channel = root.find('.//channel')
        if channel is None:
            return []
        items = channel.findall('.//item')
        for item in items:
            try:
                title_elem = item.find('title')
                if title_elem is None:
                    continue
                title = clean_html(title_elem.text or '')
                if 'Show HN' in title or 'Launch HN' in title:
                    link_elem = item.find('link')
                    link = link_elem.text if link_elem is not None else ""
                    clean_title = title.replace('Show HN:', '').replace('Show HN', '').strip()
                    summary = ""
                    if '–' in clean_title or '-' in clean_title:
                        parts = clean_title.replace('–', '-').split('-', 1)
                        if len(parts) > 1:
                            desc_part = parts[1].strip()
                            summary = translate_title(desc_part)
                            clean_title = parts[0].strip()
                    if not summary:
                        summary = "HackerNews 社区用户发布的创新产品项目"
                    if clean_title and link:
                        products.append({'title': clean_title, 'source': 'HackerNews', 'url': link, 'summary': summary, 'type': 'product'})
                        if len(products) >= 1:
                            break
            except Exception as e:
                continue
        if not products:
            for item in items[:5]:
                try:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    if title_elem is not None and link_elem is not None:
                        title = clean_html(title_elem.text or '')
                        link = link_elem.text or ""
                        skip_keywords = ['ask hn', 'tell hn', 'poll:', 'who is hiring']
                        if any(kw in title.lower() for kw in skip_keywords):
                            continue
                        summary = ""
                        if '–' in title or '-' in title:
                            parts = title.replace('–', '-').split('-', 1)
                            if len(parts) > 1:
                                summary = translate_title(parts[1].strip())
                                title = parts[0].strip()
                        if not summary:
                            summary = "HackerNews 热门技术产品/项目讨论"
                        if title and link:
                            products.append({'title': title, 'source': 'HackerNews', 'url': link, 'summary': summary, 'type': 'product'})
                            break
                except Exception:
                    continue
    except Exception as e:
        print(f"Error fetching HackerNews products: {e}")
    return products[:1]

def fetch_reddit_products():
    url = "https://www.reddit.com/r/SideProject/top/.rss?t=week"
    products = []
    try:
        result = subprocess.run(['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', '--max-time', '30', url], capture_output=True, text=True, timeout=35)
        if result.returncode != 0:
            return [{'title': 'IndieHackers Toolkit', 'source': 'Reddit', 'url': 'https://www.reddit.com/r/SideProject/', 'summary': 'Reddit 独立开发者社区本周热门产品项目精选', 'type': 'product'}]
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            return [{'title': 'IndieHackers Toolkit', 'source': 'Reddit', 'url': 'https://www.reddit.com/r/SideProject/', 'summary': 'Reddit 独立开发者社区本周热门产品项目精选', 'type': 'product'}]
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return [{'title': 'IndieHackers Toolkit', 'source': 'Reddit', 'url': 'https://www.reddit.com/r/SideProject/', 'summary': 'Reddit 独立开发者社区本周热门产品项目精选', 'type': 'product'}]
        entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        if not entries:
            entries = root.findall('.//entry')
        for entry in entries[:3]:
            try:
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                if title_elem is None:
                    title_elem = entry.find('title')
                link_elem = entry.find('{http://www.w3.org/2005/Atom}link')
                if link_elem is None:
                    link_elem = entry.find('link')
                content_elem = entry.find('{http://www.w3.org/2005/Atom}content')
                if content_elem is None:
                    content_elem = entry.find('content')
                if title_elem is not None:
                    title = clean_html(title_elem.text or '')
                    link = ""
                    if link_elem is not None:
                        link = link_elem.get('href', '')
                    description = ""
                    if content_elem is not None and content_elem.text:
                        content_text = clean_html(content_elem.text)
                        description = content_text[:200]
                    if title and link:
                        skip_keywords = ['how do i', 'how to', 'question', 'help', 'advice', 'feedback', '?']
                        if any(kw in title.lower() for kw in skip_keywords):
                            continue
                        if description:
                            summary = translate_summary_keep_keywords(description)
                            summary = summary[:80] + "..." if len(summary) > 80 else summary
                        else:
                            summary = "Reddit 独立开发者社区热门产品项目"
                        products.append({'title': title, 'source': 'Reddit', 'url': link, 'summary': summary, 'type': 'product'})
                        break
            except Exception as e:
                print(f"Error parsing Reddit entry: {e}")
                continue
        if not products:
            products.append({'title': 'IndieHackers Toolkit', 'source': 'Reddit', 'url': 'https://www.reddit.com/r/SideProject/', 'summary': 'Reddit 独立开发者社区本周热门产品项目精选', 'type': 'product'})
    except Exception as e:
        print(f"Error fetching Reddit: {e}")
        products.append({'title': 'IndieHackers Toolkit', 'source': 'Reddit', 'url': 'https://www.reddit.com/r/SideProject/', 'summary': 'Reddit 独立开发者社区本周热门产品项目精选', 'type': 'product'})
    return products[:1]

# ============== 历史记录 ==============

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        cutoff_date = datetime.now() - timedelta(days=HISTORY_DAYS)
        filtered_history = []
        for item in history:
            try:
                pub_date = item.get('fetched_at', '')
                if pub_date:
                    item_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    if item_date > cutoff_date:
                        filtered_history.append(item)
            except:
                filtered_history.append(item)
        return filtered_history
    except:
        return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

# ============== 主函数 ==============

def main():
    """主函数 - 多来源均衡抓取"""
    print("=" * 60)
    print("🚀 小羽毛新闻抓取器 v2.1 - 多来源均衡修复版")
    print("=" * 60)
    
    history = load_history()
    history_urls = {item['url'] for item in history}
    print(f"📚 历史记录: {len(history)} 条 ({HISTORY_DAYS}天窗口)")
    
    added_today_urls = set()
    added_titles = set()
    all_news = []
    
    # 第一轮：每个源获取最小数量
    print("\n📡 第一阶段：确保每个来源最小数量")
    print("-" * 60)
    
    for name, config in RSS_SOURCES.items():
        print(f"\n[{name}] → {config['url']}")
        items = fetch_rss(config['url'], name)
        
        if not items:
            print(f"  ⚠️ {name} 没有获取到数据")
            continue
        
        # 去重并选择
        selected = []
        for item in items:
            url = item['url']
            title = item['title']
            
            # URL去重
            if url in history_urls or url in added_today_urls:
                continue
            
            # 标题相似度去重
            simple_title = title.lower().replace(' ', '')[:30]
            is_dup = False
            for existing_title in added_titles:
                if calculate_similarity(simple_title, existing_title) >= SIMILARITY_THRESHOLD:
                    is_dup = True
                    break
            
            if is_dup:
                continue
            
            item['fetched_at'] = datetime.now().isoformat()
            selected.append(item)
            added_today_urls.add(url)
            added_titles.add(simple_title)
            
            # 达到最小数量就停止
            if len(selected) >= config['min_items']:
                break
        
        all_news.extend(selected)
        print(f"  ✅ {name}: {len(selected)}/{config['min_items']} 条")
        for item in selected:
            print(f"     • {item['title'][:45]}...")
    
    # 第二轮：补充到12条
    print("\n📡 第二阶段：补充到12条")
    print("-" * 60)
    
    remaining = 12 - len(all_news)
    if remaining > 0:
        for name, config in RSS_SOURCES.items():
            if remaining <= 0:
                break
            
            # 重新获取
            items = fetch_rss(config['url'], name)
            current_count = len([n for n in all_news if n['source'] == name])
            can_add = min(config['max_items'] - current_count, remaining)
            
            for item in items:
                if can_add <= 0:
                    break
                
                url = item['url']
                title = item['title']
                
                if url in history_urls or url in added_today_urls:
                    continue
                
                simple_title = title.lower().replace(' ', '')[:30]
                is_dup = False
                for existing_title in added_titles:
                    if calculate_similarity(simple_title, existing_title) >= SIMILARITY_THRESHOLD:
                        is_dup = True
                        break
                
                if is_dup:
                    continue
                
                item['fetched_at'] = datetime.now().isoformat()
                all_news.append(item)
                added_today_urls.add(url)
                added_titles.add(simple_title)
                remaining -= 1
                can_add -= 1
    
    # 抓取产品
    print("\n📦 抓取产品数据...")
    print("-" * 60)
    all_products = []
    
    for fetch_func, name in [
        (fetch_product_hunt, "ProductHunt"),
        (fetch_github_trending, "GitHub"),
        (fetch_toolify, "Toolify"),
        (fetch_hackernews_products, "HackerNews"),
        (fetch_reddit_products, "Reddit")
    ]:
        print(f"  {name}...", end=" ")
        try:
            items = fetch_func()
            for item in items:
                if item['url'] not in history_urls and item['url'] not in added_today_urls:
                    item['fetched_at'] = datetime.now().isoformat()
                    all_products.append(item)
                    added_today_urls.add(item['url'])
                    print(f"✓ ({item['title'][:30]}...)")
                    break
            else:
                print("✓ (cached)")
        except Exception as e:
            print(f"✗ ({e})")
    
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

if __name__ == "__main__":
    main()
