import json
import os
import subprocess
import xml.etree.ElementTree as ET
import urllib.parse
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
    "GitHub": "https://github.com/trending?since=daily",  # 需要特殊处理
    "Toolify": "https://www.toolify.ai/rss",  # AI工具排行榜
    "Reddit": "https://www.reddit.com/r/ArtificialInteligence/top/.rss?t=day",  # AI相关热门
}

HISTORY_FILE = "news_history.json"
HISTORY_DAYS = 3  # 只保留3天的历史记录用于去重
TAIPEI_TZ = ZoneInfo("Asia/Taipei")

def now_taipei():
    return datetime.now(TAIPEI_TZ)

# 需要保留英文原文的关键词（产品名、人名、特殊名词）
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
    "ProductHunt", "Product Hunt", "HackerNews", "Hacker News", "GitHub", "Reddit", "Toolify",
    # 公司名称
    "NVIDIA", "Intel", "AMD", "Qualcomm", "Apple", "Tesla", "SpaceX", "Neuralink",
    "DeepMind", "Cohere", "Adept", "Character.AI", "Runway", "Shopify", "Netflix",
    "OpenAI", "Perplexity", "Poe", "Hugging Face", "Stability AI", "Midjourney",
    "ElevenLabs", "Anthropic", "Inflection", "Adept AI", "Character AI",
    "ByteDance", "TikTok", "Oracle", "IBM", "Salesforce", "Adobe", "Cisco",
    "Samsung", "Sony", "LG", "Huawei", "Xiaomi", "DJI", "Baidu", "Alibaba",
    "Tencent", "Meituan", "Pinduoduo", "JD.com", "Didi", "NIO", "XPeng", "Li Auto",
    "Waymo", "Cruise", "Zoox", "Aurora", "Comma.ai", "Comma AI",
    # 人名（保持首字母大写格式）
    "Sam Altman", "Elon Musk", "Sundar Pichai", "Satya Nadella", "Tim Cook",
    "Mark Zuckerberg", "Jensen Huang", "Demis Hassabis", "Dario Amodei",
    "Andrew Ng", "Fei-Fei Li", "Yann LeCun", "Geoffrey Hinton", "Yoshua Bengio",
    "Andrej Karpathy", "Sebastian Thrun", "Lex Fridman", "Bill Gates", "Jeff Bezos",
    "Larry Page", "Sergey Brin", "Steve Jobs", "Paul Allen", "Peter Thiel",
    "Marc Andreessen", "Reid Hoffman", "Eric Schmidt", "Larry Ellison", "Safra Catz",
    "Lisa Su", "Pat Gelsinger", "Brian Krzanich", "Robert Swan", "Gordon Moore",
    "Andy Grove", "Craig Barrett", "Paul Otellini", "Brian Chesky", "Joe Gebbia",
    "Nathan Blecharczyk", "Brian Armstrong", "Vitalik Buterin", "Satoshi Nakamoto",
    "Changpeng Zhao", "CZ", "Sam Bankman-Fried", "SBF", "Gary Gensler",
    "Elizabeth Warren", "Donald Trump", "Joe Biden", "Barack Obama",
    "Antonio Gracias", "Harley Finkelstein", "Frore", "Fuse",
    # 技术/学术术语
    "proentropic", "anti-entropic", "entropy", "singularity", "AGI", "ASI",
    "transformer", "attention", "BERT", "GPT", "diffusion", "GAN", "VAE",
    "RNN", "LSTM", "CNN", "ResNet", "YOLO", "CLIP", "DALL-E", "Whisper",
    "reinforcement learning", "supervised learning", "unsupervised learning",
    "few-shot learning", "zero-shot learning", "prompt engineering",
    "chain of thought", "retrieval augmented generation", "RAG",
    "fine-tuning", "pre-training", "inference", "training", "dataset",
    "token", "embedding", "vector", "latent", "latent space",
    "multimodal", "cross-modal", "zero-shot", "few-shot", "one-shot",
    # 品牌/产品名（需要保留原文的）
    "iPhone", "iPad", "MacBook", "MacBook Pro", "MacBook Air", "Mac Studio",
    "AirPods", "AirPods Max", "AirPods Pro", "Apple Watch", "Vision Pro",
    "Pixel", "Pixel Phone", "Pixel Tablet", "Chromebook", "Chromecast",
    "Surface", "Surface Pro", "Surface Studio", "Xbox", "PlayStation",
    "Galaxy", "Galaxy S", "Galaxy Z", "Galaxy Fold", "Galaxy Flip",
    "Redmi", "Poco", "OnePlus", "Oppo", "Vivo", "Realme", "Nothing",
    "Raspberry Pi", "Arduino", "ESP32", "NVIDIA Jetson", "Jetson",
    # 常见产品名（新增）
    "Knock", "Donely", "Wendi", "Wendi AI", "JetBrains", "JetBrains Air",
    "Spott", "Trackm", "Oxyde", "Leanstral", "Mistral AI",
    "Memories AI", "GridBeyond", "MotionVFX", "AltStore", "AltStore PAL",
    "NemoClaw", "Blackwell", "Vera Rubin", "DLSS", "DLSS 5",
    "TurboTax", "AirPods Max", "Stormbox", "Tribit",
    # 投资/商业术语
    "IPO", "SPAC", "VC", "PE", "IPO", " unicorn", "decacorn", "seed round",
    "Series A", "Series B", "Series C", "angel investor", "venture capital",
    "private equity", "M&A", "merger", "acquisition", "due diligence",
    "valuation", "market cap", "revenue", "ARR", "MRR", "LTV", "CAC",
    # 加密货币/Web3
    "Bitcoin", "Ethereum", "Solana", "Cardano", "Polkadot", "Avalanche",
    "Polygon", "Arbitrum", "Optimism", "zkSync", "StarkNet", "Layer 2",
    "DeFi", "NFT", "DAO", "Web3", "dApp", "smart contract", "wallet",
}


def generate_daily_insight(news_items, products_items, today_str):
    """
    基于当天新闻内容生成 20-90 字的洞察文案
    
    策略：
    1. 分析头条新闻关键词
    2. 匹配主题分类
    3. 选择最相关的洞察
    """
    import hashlib
    
    # 收集所有标题和摘要文本
    all_text = " ".join([
        item.get('title', '') + " " + item.get('summary', '')
        for item in (news_items[:3] + products_items[:2])
    ]).lower()
    
    # 主题分类与洞察库
    themed_insights = {
        'model': {
            'keywords': ['model', 'llm', 'gpt', 'claude', 'gemini', '训练', '参数', '性能', '突破'],
            'quotes': [
                "模型迭代的速度正在重新定义智能的边界，每一次训练都是对人类认知边界的推进。",
                "当大模型变得更轻、更快、更准，AI正在从实验室走向每个人的日常。",
                "参数量的竞赛背后，是对智能本质的深层理解。",
                "开源与闭源的博弈，正在塑造下一代AI基础设施的格局。"
            ]
        },
        'product': {
            'keywords': ['product', 'launch', '发布', '新品', 'app', '工具', '平台', '上线'],
            'quotes': [
                "新产品的发布不只是功能的堆叠，而是对用户需求痛点的精准回应。",
                "当AI能力被封装成简单的产品，技术的民主化才真正开始。",
                "每个新工具的诞生，都在重新定义人机协作的边界。",
                "产品的终极考验不是功能多少，而是能否让用户忘记技术的存在。"
            ]
        },
        'business': {
            'keywords': ['融资', '收购', '投资', '估值', '上市', '财报', '营收', 'million', 'billion', '收购', '合并'],
            'quotes': [
                "资本的流向往往预示着技术周期的转折点，钱是最诚实的投票。",
                "当泡沫退去，真正创造价值的AI公司才会显露本色。",
                "投资不仅是押注技术，更是押注团队对人性需求的理解深度。",
                "独角兽的诞生从不是偶然，而是技术成熟度与市场需求共振的结果。"
            ]
        },
        'ethics': {
            'keywords': ['伦理', '监管', '隐私', '安全', '风险', '担忧', '争议', '伦理', '安全', 'privacy', 'regulation'],
            'quotes': [
                "技术越强大，我们对责任的思考就需要越深刻。",
                "监管不是创新的对立面，而是让创新走得更远的基础设施。",
                "隐私与便利的权衡，是数字时代每个人的必修课。",
                "AI的边界不仅由技术决定，更由人类的价值观塑造。"
            ]
        },
        'application': {
            'keywords': ['应用', '场景', '医疗', '教育', '金融', '创作', '生成', '视频', '图像', '音频'],
            'quotes': [
                "AI真正的价值不在技术本身，而在它如何解决具体领域的真实问题。",
                "当生成式AI进入创作领域，人类的角色从执行者变为策展人。",
                "垂直场景的深耕，往往比通用能力更能创造持久价值。",
                "技术落地的最后一公里，需要理解行业肌理的人才能走完。"
            ]
        },
        'breakthrough': {
            'keywords': ['突破', '里程碑', '首次', '创新', '革命', '颠覆', '创纪录', '首次', '里程碑'],
            'quotes': [
                "每一个技术里程碑的背后，都是无数失败实验的积累。",
                "突破往往发生在被忽视的细节里，而非宏大的叙事中。",
                "当一项技术跨越了'足够好'的阈值，变革就开始了。",
                "真正的创新从不是凭空出现，而是对已有边界的有意识突破。"
            ]
        }
    }
    
    # 计算各主题匹配度
    theme_scores = {}
    for theme, data in themed_insights.items():
        score = sum(1 for kw in data['keywords'] if kw in all_text)
        if score > 0:
            theme_scores[theme] = score
    
    # 选择最佳匹配主题，或使用通用主题
    if theme_scores:
        best_theme = max(theme_scores, key=theme_scores.get)
        quotes_pool = themed_insights[best_theme]['quotes']
    else:
        # 通用洞察库
        quotes_pool = [
            "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。",
            "每一次模型的迭代，都是人类理解智能本质的一次尝试。",
            "AI 不是替代人类，而是放大人类的可能性。",
            "最好的产品，是让技术隐形，让体验自然。",
            "创新往往发生在不同学科的交界处。",
            "伟大的工具，是让人忘记工具本身的存在。",
            "代码是写给人看的，顺便让机器执行。",
            "产品成功的秘诀：解决一个具体的问题，比解决所有问题更重要。",
            "技术的边界，就是我们想象力的边界。",
            "每一个开源项目背后，都有一群相信共享比封闭更有力量的人。",
            "在信息爆炸的时代，筛选和品味比获取更重要。",
            "AI的进化速度提醒我们：保持学习是唯一不变的竞争力。",
            "技术的民主化，让创意的门槛不断降低，想象力的价值不断升高。"
        ]
    
    # 基于日期选择，保证同一天的一致性
    day_hash = int(hashlib.md5(today_str.encode()).hexdigest(), 16)
    selected_quote = quotes_pool[day_hash % len(quotes_pool)]
    
    return selected_quote


def translate_summary_keep_keywords(text_en):
    """翻译摘要但保留产品/人名/特殊名词的英文原文"""
    import re
    
    if not text_en:
        return ""
    
    # 如果已经是中文，直接返回
    if any('\u4e00' <= char <= '\u9fff' for char in text_en):
        return text_en
    
    # 保护英文关键词：用占位符替换
    placeholders = {}
    protected_text = text_en
    
    for i, keyword in enumerate(ENGLISH_KEYWORDS):
        # 使用 word boundary 确保匹配完整单词
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, protected_text, re.IGNORECASE)
        for match in matches:
            placeholder = f"__KEYWORD_{i}_{len(placeholders)}__"
            placeholders[placeholder] = match
            protected_text = protected_text.replace(match, placeholder)
    
    # 翻译保护后的文本
    translated = translate_to_chinese(protected_text)
    
    # 清除零宽空格等不可见字符（Google Translate 有时会在下划线周围插入这些字符）
    translated = translated.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    
    # 还原英文关键词
    for placeholder, original in placeholders.items():
        translated = translated.replace(placeholder, original)
    
    return translated

# 常见英文标题翻译映射 (技术新闻常用)
TITLE_TRANSLATIONS = {
    # 产品/平台名称
    "alternative app store": "替代应用商店",
    "altstore pal": "AltStore PAL",
    "joins the fediverse": "加入联邦宇宙",
    "fediverse": "联邦宇宙",
    "best mattress": "最佳床垫",
    "back pain": "背痛",
    "mattress": "床垫",
    "best bluetooth trackers": "最佳蓝牙追踪器",
    "bluetooth trackers": "蓝牙追踪器",
    # 动作/功能
    "upgrades": "升级",
    "interactive learning": "交互式学习",
    "lawsuits": "诉讼",
    "determined to use AI": "决心全面使用 AI",
    "political fundraising": "政治筹款",
    "developing": "开发",
    "new chips": "新芯片",
    "recommendation systems": "推荐系统",
    "digital picture frame": "数字相框",
    "holographic": "全息",
    "e-commerce": "电子商务",
    "business-to-agent": "企业对智能体",
    "decentralize": "去中心化",
    "decentralized": "去中心化",
    "watch": "观看",
    "keynote": "主题演讲",
    "launches": "发布",
    "claims": "声称",
    "coding agent": "编程智能体",
    "is coming to": "将登陆",
    "lets you": "让你",
    "is not ruling out": "不排除",
    "accused of": "被指控",
    # 人物/品牌
    "mr beast": "MrBeast",
    "go viral": "病毒式传播",
    "viral": "病毒式传播",
    "ai audio": "AI 音频",
    "amazon": "亚马逊",
    "anthropic": "Anthropic",
    "nvidia": "英伟达",
    "openai": "OpenAI",
    "google": "谷歌",
    "meta": "Meta",
    "apple": "苹果",
    "microsoft": "微软",
    "tesla": "特斯拉",
    "nvidia's": "英伟达的",
    "youtube": "YouTube",
    "gemini": "Gemini",
    # 技术词汇
    "brain interface": "脑机接口",
    "bci": "脑机接口",
    "startup": "创业公司",
    "raises": "融资",
    "funding": "融资",
    "million": "百万美元",
    "billion": "十亿美元",
    "valuation": "估值",
    "promo code": "优惠码",
    "coupon": "优惠券",
    "deal": "优惠",
    "discount": "折扣",
    "ai actor": "AI 演员",
}


def translate_title(title_en):
    """
    翻译标题，保留英文专有名词（人名、公司名、产品名等）
    
    策略：中文为主，英文为辅
    - 新闻标题、描述 → 用中文
    - 人名、公司名称、产品名称、特殊术语 → 保留英文原文
    
    示例：
    ❌ "Antonio Gracias says he's longing for 'proentropic' startups"
    ✅ "Antonio Gracias 表示，他渴望投资能在混乱中存活的「反熵」创业公司"
    """
    import re
    
    if not title_en:
        return ""
    
    # 如果已经有中文，直接返回
    if any('\u4e00' <= char <= '\u9fff' for char in title_en):
        return title_en
    
    # 保护英文关键词：用占位符替换（与 translate_summary_keep_keywords 相同的机制）
    placeholders = {}
    protected_text = title_en
    
    # 按长度降序排列关键词，确保先匹配更长的词（如 "Sam Altman" 在 "Altman" 之前）
    sorted_keywords = sorted(ENGLISH_KEYWORDS, key=len, reverse=True)
    
    for i, keyword in enumerate(sorted_keywords):
        # 使用 word boundary 确保匹配完整单词，忽略大小写
        pattern = r'\b' + re.escape(keyword) + r'\b'
        matches = re.findall(pattern, protected_text, re.IGNORECASE)
        for match in matches:
            placeholder = f"__TITLE_KEY_{i}_{len(placeholders)}__"
            placeholders[placeholder] = match
            # 使用 replace 进行大小写敏感替换（保留原文的大小写）
            protected_text = protected_text.replace(match, placeholder)
    
    # 翻译保护后的文本
    translated = translate_to_chinese(protected_text)
    
    # 清除零宽空格等不可见字符（Google Translate 有时会在下划线周围插入这些字符）
    translated = translated.replace('\u200b', '').replace('\u200c', '').replace('\u200d', '')
    
    # 还原英文关键词
    for placeholder, original in placeholders.items():
        translated = translated.replace(placeholder, original)
    
    return translated


def clean_html(text):
    """移除 HTML 标签"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def translate_to_chinese(text):
    """
    调用 Google Translate API 翻译文本
    注意：这是免费 API，有频率限制
    """
    import urllib.request
    import urllib.parse
    import json
    
    if not text:
        return ""
    
    # 检测是否已经是中文
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return text
    
    try:
        # Google Translate API (免费版本)
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&dt=t&q=" + urllib.parse.quote(text)
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        # 解析返回结果
        if data and len(data) > 0 and len(data[0]) > 0:
            translated_parts = [item[0] for item in data[0] if item and len(item) > 0]
            return ''.join(translated_parts)
        
        return text  # 如果翻译失败，返回原文
        
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # 出错时返回原文


def fetch_rss(url, name):
    """
    获取并解析 RSS feed
    返回格式化的新闻列表
    """
    news_items = []
    
    try:
        # 使用 curl 获取 RSS 内容
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', 
             '--max-time', '30', url],
            capture_output=True,
            text=True,
            timeout=35
        )
        
        if result.returncode != 0:
            print(f"❌ Error fetching {name}: curl failed")
            return []
        
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            print(f"❌ Error: Empty response from {name}")
            return []
        
        # 保存原始 XML 用于调试
        safe_name = name.replace(' ', '_').replace('/', '_')
        with open(f"{safe_name}.xml", 'w', encoding='utf-8') as f:
            f.write(xml_content[:50000])  # 限制大小
        
        # 解析 XML
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            print(f"❌ XML Parse error in {name}: {e}")
            return []
        
        # 检测命名空间
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        is_atom = root.tag.endswith('feed') or root.tag == 'feed'
        
        # RSS 2.0 格式
        if root.tag == 'rss' or root.tag.endswith('rss'):
            channel = root.find('.//channel')
            if channel is None:
                items = root.findall('.//item')
            else:
                items = channel.findall('.//item')
        # Atom 格式
        elif is_atom:
            items = root.findall('.//atom:entry', ns)
            if not items:
                items = root.findall('.//entry')
        else:
            items = root.findall('.//item')
        
        print(f"📰 {name}: Found {len(items)} items")
        
        # 只取最近的项目
        for item in items[:15]:
            try:
                # 获取标题 - 尝试多种方式
                title = ""
                title_elem = item.find('title')
                if title_elem is None and is_atom:
                    title_elem = item.find('atom:title', ns)
                if title_elem is not None:
                    title = title_elem.text or ""
                    # 处理CDATA
                    if title:
                        title = title.strip()
                
                # 获取链接 - 兼容 RSS 和 Atom 格式
                link = ""
                if is_atom:
                    # Atom格式: <link rel="alternate" href="..." /> 或 <link href="..."/>
                    link_elem = item.find('atom:link', ns)
                    if link_elem is None:
                        link_elem = item.find('link')
                    if link_elem is not None:
                        link = link_elem.get('href', '')
                        # 如果没有href属性，尝试text内容
                        if not link and link_elem.text:
                            link = link_elem.text.strip()
                else:
                    # RSS格式: <link>...</link>
                    link_elem = item.find('link')
                    if link_elem is not None:
                        link = link_elem.text or ""
                        if not link:
                            link = link_elem.get('href', '')
                
                # 获取描述/摘要 - 尝试多种方式
                description = ""
                if is_atom:
                    # Atom优先使用summary
                    desc_elem = item.find('atom:summary', ns)
                    if desc_elem is None:
                        desc_elem = item.find('summary')
                    if desc_elem is None:
                        desc_elem = item.find('atom:content', ns)
                    if desc_elem is None:
                        desc_elem = item.find('content')
                else:
                    desc_elem = item.find('description')
                
                if desc_elem is not None:
                    description = desc_elem.text or ""
                
                # 获取发布日期
                date_elem = item.find('pubDate')
                if date_elem is None:
                    date_elem = item.find('.//{http://www.w3.org/2005/Atom}published')
                if date_elem is None:
                    date_elem = item.find('published')
                
                pub_date = date_elem.text if date_elem is not None else ""
                
                if title and link:
                    # 清理 HTML
                    title = clean_html(title)
                    description = clean_html(description)
                    
                    # 翻译
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


def fetch_product_hunt():
    """专门抓取 ProductHunt 产品数据，返回产品列表"""
    url = "https://www.producthunt.com/feed"
    products = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', 
             '--max-time', '30', url],
            capture_output=True,
            text=True,
            timeout=35
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
        
        # ProductHunt 是 Atom 格式
        entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        if not entries:
            entries = root.findall('.//entry')
        
        for entry in entries[:3]:  # 取前3个
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
                    # 获取产品描述（从 content 中提取）
                    description = ""
                    if content_elem is not None and content_elem.text:
                        content_text = content_elem.text
                        # 从 HTML 内容中提取纯文本描述
                        import re
                        # 提取 <p> 标签中的文本
                        p_matches = re.findall(r'&lt;p&gt;(.*?)&lt;/p&gt;', content_text)
                        if p_matches:
                            # 获取第一个 <p> 标签的内容，去掉 HTML 实体
                            desc_html = p_matches[0]
                            # 解码 HTML 实体
                            desc_html = desc_html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                            description = clean_html(desc_html)
                    
                    # 获取链接 - 优先从 content 中的 Link 提取
                    link = ""
                    if link_elem is not None:
                        link = link_elem.get('href', '')
                    
                    # 从 content 中提取实际产品链接
                    if content_elem is not None and content_elem.text:
                        link_match = re.search(r'&lt;a href=\"(.*?)\"&gt;Link&lt;/a&gt;', content_elem.text)
                        if link_match:
                            actual_link = link_match.group(1).replace('&amp;', '&')
                            if actual_link:
                                link = actual_link
                    
                    if title and link:
                        # 生成一句话中文摘要
                        tagline = description.strip() if description else f"{title} - 热门新产品"
                        tagline_zh = translate_title(tagline) if tagline else f"{title} - 热门新产品"
                        
                        products.append({
                            'title': title,  # 保留英文原名
                            'source': 'Product Hunt',
                            'url': link,
                            'summary': tagline_zh,
                            'type': 'product'
                        })
            except Exception as e:
                print(f"Error parsing ProductHunt entry: {e}")
                continue
                
    except Exception as e:
        print(f"Error fetching ProductHunt: {e}")
    
    return products[:1]  # 只返回最热门的1个


def fetch_github_trending():
    """抓取 GitHub 热门 AI/ML 项目"""
    import urllib.request
    import json
    
    products = []
    
    try:
        # 使用 GitHub search API 查找最近更新的 AI 相关热门项目
        # 搜索语言为 Python 或 TypeScript 且主题包含 AI/ML 的项目
        query = "machine learning OR artificial intelligence OR llm OR chatgpt OR openai"
        encoded_query = urllib.parse.quote(query)
        url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=updated&order=desc&per_page=10"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # 取第一个有效项目
        for item in data.get('items', []):
            title = item.get('name', '')
            description = item.get('description', '') or ""
            url = item.get('html_url', '')
            stars = item.get('stargazers_count', 0)
            
            if title and url:
                # 生成一句话摘要
                desc_zh = translate_title(description) if description else "GitHub 热门开源项目"
                if stars > 0:
                    summary = f"{desc_zh} ⭐ {stars:,}"
                else:
                    summary = desc_zh
                
                products.append({
                    'title': title,  # 保留英文原名
                    'source': 'GitHub',
                    'url': url,
                    'summary': summary,
                    'type': 'product'
                })
                break  # 只取第一个
                
    except Exception as e:
        print(f"Error fetching GitHub trending: {e}")
        # 备用方案：返回一个示例
        products.append({
            'title': 'awesome-chatgpt-prompts',
            'source': 'GitHub',
            'url': 'https://github.com/f/awesome-chatgpt-prompts',
            'summary': 'ChatGPT 提示词精选合集，助力 AI 对话效率提升 ⭐ 120,000+',
            'type': 'product'
        })
    
    return products[:1]


def fetch_toolify():
    """抓取 Toolify AI 工具排行榜"""
    # Toolify 的 RSS 或抓取热门工具
    url = "https://www.toolify.ai/rss"
    products = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '30', url],
            capture_output=True,
            text=True,
            timeout=35
        )
        
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
                        # 生成中文摘要
                        if description:
                            desc_zh = translate_summary_keep_keywords(description)
                            summary = desc_zh[:80] + "..." if len(desc_zh) > 80 else desc_zh
                        else:
                            summary = "AI 工具推荐"
                        
                        products.append({
                            'title': title,  # 保留英文原名
                            'source': 'Toolify',
                            'url': link,
                            'summary': summary,
                            'type': 'product'
                        })
            except Exception as e:
                print(f"Error parsing Toolify entry: {e}")
                continue
                
    except Exception as e:
        print(f"Error fetching Toolify: {e}")
    
    # 如果 RSS 失败或没有数据，使用备用数据
    if not products:
        products.append({
            'title': 'Toolify AI',
            'source': 'Toolify',
            'url': 'https://www.toolify.ai',
            'summary': 'AI 工具导航网站，汇集全球最新 AI 应用与工具',
            'type': 'product'
        })
    
    return products[:1]


def fetch_hackernews_products():
    """抓取 HackerNews Show HN 产品"""
    url = "https://news.ycombinator.com/rss"
    products = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0', '--max-time', '30', url],
            capture_output=True,
            text=True,
            timeout=35
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
        
        channel = root.find('.//channel')
        if channel is None:
            return []
        
        items = channel.findall('.//item')
        
        # 优先找 Show HN 的产品
        for item in items:
            try:
                title_elem = item.find('title')
                if title_elem is None:
                    continue
                
                title = clean_html(title_elem.text or '')
                
                # 只取 Show HN 或产品相关的内容
                if 'Show HN' in title or 'Launch HN' in title:
                    link_elem = item.find('link')
                    link = link_elem.text if link_elem is not None else ""
                    
                    # 清理标题，去掉 "Show HN:" 前缀
                    clean_title = title.replace('Show HN:', '').replace('Show HN', '').strip()
                    
                    # 尝试从标题提取产品描述（通常标题格式是 "产品名 - 一句话描述"）
                    summary = ""
                    if '–' in clean_title or '-' in clean_title:
                        # 标题中可能有描述部分
                        parts = clean_title.replace('–', '-').split('-', 1)
                        if len(parts) > 1:
                            desc_part = parts[1].strip()
                            # 翻译描述部分
                            summary = translate_title(desc_part)
                            clean_title = parts[0].strip()
                    
                    # 如果标题中没有描述，使用通用描述
                    if not summary:
                        summary = "HackerNews 社区用户发布的创新产品项目"
                    
                    if clean_title and link:
                        products.append({
                            'title': clean_title,  # 保留英文原名
                            'source': 'HackerNews',
                            'url': link,
                            'summary': summary,
                            'type': 'product'
                        })
                        
                        if len(products) >= 1:
                            break
            except Exception as e:
                continue
        
        # 如果没有 Show HN，取最热门的1个技术相关项目
        if not products:
            for item in items[:5]:  # 检查前5个
                try:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    
                    if title_elem is not None and link_elem is not None:
                        title = clean_html(title_elem.text or '')
                        link = link_elem.text or ""
                        
                        # 跳过纯讨论帖
                        skip_keywords = ['ask hn', 'tell hn', 'poll:', 'who is hiring']
                        if any(kw in title.lower() for kw in skip_keywords):
                            continue
                        
                        # 尝试从标题提取描述
                        summary = ""
                        if '–' in title or '-' in title:
                            parts = title.replace('–', '-').split('-', 1)
                            if len(parts) > 1:
                                desc_part = parts[1].strip()
                                summary = translate_title(desc_part)
                                title = parts[0].strip()
                        
                        if not summary:
                            summary = "HackerNews 热门技术产品/项目讨论"
                        
                        if title and link:
                            products.append({
                                'title': title,  # 保留英文原名
                                'source': 'HackerNews',
                                'url': link,
                                'summary': summary,
                                'type': 'product'
                            })
                            break
                except Exception:
                    continue
                    
    except Exception as e:
        print(f"Error fetching HackerNews products: {e}")
    
    return products[:1]


def fetch_reddit_products():
    """抓取 Reddit SideProject 社区热门产品项目"""
    # 使用 r/SideProject 社区 - 专门展示用户产品的社区
    url = "https://www.reddit.com/r/SideProject/top/.rss?t=week"
    products = []
    
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (compatible; RSS Bot/1.0)', 
             '--max-time', '30', url],
            capture_output=True,
            text=True,
            timeout=35
        )
        
        if result.returncode != 0:
            # 备用：使用静态产品数据
            return [{
                'title': 'IndieHackers Toolkit',
                'source': 'Reddit',
                'url': 'https://www.reddit.com/r/SideProject/',
                'summary': 'Reddit 独立开发者社区本周热门产品项目精选',
                'type': 'product'
            }]
        
        xml_content = result.stdout
        if not xml_content or len(xml_content) < 100:
            return [{
                'title': 'IndieHackers Toolkit',
                'source': 'Reddit',
                'url': 'https://www.reddit.com/r/SideProject/',
                'summary': 'Reddit 独立开发者社区本周热门产品项目精选',
                'type': 'product'
            }]
        
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return [{
                'title': 'IndieHackers Toolkit',
                'source': 'Reddit',
                'url': 'https://www.reddit.com/r/SideProject/',
                'summary': 'Reddit 独立开发者社区本周热门产品项目精选',
                'type': 'product'
            }]
        
        # Reddit RSS 格式
        entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
        if not entries:
            entries = root.findall('.//entry')
        
        for entry in entries[:3]:  # 尝试前3个，找最像产品的
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
                    
                    # 从内容提取摘要
                    description = ""
                    if content_elem is not None and content_elem.text:
                        content_text = clean_html(content_elem.text)
                        # 提取前150字符作为描述
                        description = content_text[:200]
                    
                    if title and link:
                        # 过滤掉明显不是产品的讨论帖（如问题、求助等）
                        skip_keywords = ['how do i', 'how to', 'question', 'help', 'advice', 'feedback', '?']
                        if any(kw in title.lower() for kw in skip_keywords):
                            continue
                        
                        # 生成中文摘要
                        if description:
                            # 尝试提取产品描述
                            summary = translate_summary_keep_keywords(description)
                            summary = summary[:80] + "..." if len(summary) > 80 else summary
                        else:
                            summary = "Reddit 独立开发者社区热门产品项目"
                        
                        products.append({
                            'title': title,  # 保留英文原名
                            'source': 'Reddit',
                            'url': link,
                            'summary': summary,
                            'type': 'product'
                        })
                        break  # 找到第一个有效产品就退出
            except Exception as e:
                print(f"Error parsing Reddit entry: {e}")
                continue
        
        # 如果没有找到有效产品，使用备用数据
        if not products:
            products.append({
                'title': 'IndieHackers Toolkit',
                'source': 'Reddit',
                'url': 'https://www.reddit.com/r/SideProject/',
                'summary': 'Reddit 独立开发者社区本周热门产品项目精选',
                'type': 'product'
            })
                
    except Exception as e:
        print(f"Error fetching Reddit: {e}")
        # 备用数据
        products.append({
            'title': 'IndieHackers Toolkit',
            'source': 'Reddit',
            'url': 'https://www.reddit.com/r/SideProject/',
            'summary': 'Reddit 独立开发者社区本周热门产品项目精选',
            'type': 'product'
        })
    
    return products[:1]


def load_history():
    """加载历史新闻"""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        # 只保留最近 HISTORY_DAYS 天的记录
        cutoff_date = now_taipei() - timedelta(days=HISTORY_DAYS)
        filtered_history = []
        
        for item in history:
            try:
                # 尝试解析日期
                pub_date = item.get('fetched_at', '')
                if pub_date:
                    item_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    if item_date > cutoff_date:
                        filtered_history.append(item)
            except:
                # 如果日期解析失败，保留该项
                filtered_history.append(item)
        
        return filtered_history
    except:
        return []


def save_history(history):
    """保存历史新闻"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    history = load_history()
    history_urls = {item['url'] for item in history}
    
    # 用于跟踪当天已添加的URL（防止同一批次内重复）
    added_today_urls = set()
    
    # 1. Fetch AI News
    all_news = []
    for name, url in RSS_SOURCES.items():
        print(f"\nFetching {name}...")
        items = fetch_rss(url, name)
        
        for item in items:
            if item['url'] not in history_urls and item['url'] not in added_today_urls:
                item['fetched_at'] = now_taipei().isoformat()
                all_news.append(item)
                added_today_urls.add(item['url'])
        
        print(f"Got {len(items)} items, {len([i for i in items if i['url'] not in history_urls])} new")
    
    # 2. Fetch Products from 5 platforms (各取1个)
    print("\n=== Fetching Products from 5 Platforms ===")
    all_products = []
    
    # Platform 1: ProductHunt
    print("Fetching ProductHunt...")
    ph_products = fetch_product_hunt()
    for item in ph_products:
        if item['url'] not in history_urls and item['url'] not in added_today_urls:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today_urls.add(item['url'])
            print(f"  ✓ ProductHunt: {item['title'][:40]}...")
    
    # Platform 2: GitHub
    print("Fetching GitHub...")
    gh_products = fetch_github_trending()
    for item in gh_products:
        if item['url'] not in history_urls and item['url'] not in added_today_urls:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today_urls.add(item['url'])
            print(f"  ✓ GitHub: {item['title'][:40]}...")
    
    # Platform 3: Toolify
    print("Fetching Toolify...")
    tf_products = fetch_toolify()
    for item in tf_products:
        if item['url'] not in history_urls and item['url'] not in added_today_urls:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today_urls.add(item['url'])
            print(f"  ✓ Toolify: {item['title'][:40]}...")
    
    # Platform 4: HackerNews
    print("Fetching HackerNews...")
    hn_products = fetch_hackernews_products()
    for item in hn_products:
        if item['url'] not in history_urls and item['url'] not in added_today_urls:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today_urls.add(item['url'])
            print(f"  ✓ HackerNews: {item['title'][:40]}...")
    
    # Platform 5: Reddit
    print("Fetching Reddit...")
    rd_products = fetch_reddit_products()
    for item in rd_products:
        if item['url'] not in history_urls and item['url'] not in added_today_urls:
            item['fetched_at'] = now_taipei().isoformat()
            all_products.append(item)
            added_today_urls.add(item['url'])
            print(f"  ✓ Reddit: {item['title'][:40]}...")
    
    print(f"\nTotal products from 5 platforms: {len(all_products)}")
    
    # 如果没有获取到新闻，使用备用数据
    if len(all_news) == 0 and len(all_products) == 0:
        print("Warning: No news fetched, using placeholder data")
        # 创建一些默认新闻用于测试
        all_news = [
            {
                'title': '今日AI新闻获取中，请稍后查看',
                'source': 'System',
                'url': 'https://xiaoyumao-news-web.vercel.app',
                'summary': '正在获取最新AI资讯...',
                'type': 'news',
                'fetched_at': now_taipei().isoformat()
            }
        ]
    
    # 去重（基于标题相似度）和排序
    seen_titles = set()
    final_news = []
    
    for item in all_news:
        # 简化标题用于去重
        simple_title = item['title'].lower().replace(' ', '')[:30]
        if simple_title not in seen_titles:
            seen_titles.add(simple_title)
            final_news.append(item)
    
    # 对产品去重
    seen_product_titles = set()
    final_products = []
    
    for item in all_products:
        simple_title = item['title'].lower().replace(' ', '')[:30]
        if simple_title not in seen_product_titles:
            seen_product_titles.add(simple_title)
            final_products.append(item)
    
    # 限制数量
    final_news = final_news[:12]
    final_products = final_products[:5]  # 5个平台各1个 = 最多5个

    # Save current run
    today_str = now_taipei().strftime("%Y-%m-%d")
    daily_quote = generate_daily_insight(final_news, final_products, today_str)
    
    output = {
        "news": final_news,
        "products": final_products,
        "date": now_taipei().strftime("%Y年%m月%d日"),
        "quote": daily_quote,
        "summary": f"今日 AI 领域 {len(final_news)} 条精选资讯，{len(final_products)} 款创新产品值得关注。"
    }
    
    with open("daily_data.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # 同步生成前端静态数据，避免页面仍然引用旧日期/旧星期
    subprocess.run(["python3", "update_news_ts.py"], check=True)

    save_history(history + final_news + final_products)
    print(f"Done. 保存了 {len(final_news)} 条新闻，{len(final_products)} 个产品到 daily_data.json，并同步更新 src/data/news.ts")

if __name__ == "__main__":
    main()
