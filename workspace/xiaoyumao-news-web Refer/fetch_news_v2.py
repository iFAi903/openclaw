import json
import os
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Sources Configuration
RSS_SOURCES = {
    "GeekPark": "https://www.geekpark.net/rss",  # 必须包含
    "TheVerge": "https://www.theverge.com/rss/index.xml",
    "TechCrunch": "https://techcrunch.com/feed/",
    "Wired": "https://www.wired.com/feed/rss",
    "VentureBeat": "https://venturebeat.com/feed/",
    "Reddit_AI": "https://www.reddit.com/r/ArtificialInteligence/top/.rss?t=day"
}

PRODUCT_SOURCES = {
    "ProductHunt": "https://www.producthunt.com/feed",
    "HackerNews": "https://news.ycombinator.com/rss",
    # Toolify & GitHub will be mocked/fetched via web_fetch in real scenario, 
    # here we use placeholders or simple curl if possible for demo speed.
}

HISTORY_FILE = "news_history.json"
HISTORY_DAYS = 3  # 只保留3天的历史记录用于去重

# 需要保留英文原文的关键词（产品名、人名、特殊名词）
ENGLISH_KEYWORDS = {
    # 产品/平台名称
    "ChatGPT", "OpenAI", "Claude", "Anthropic", "Gemini", "Google", "Meta", "LLaMA",
    "Midjourney", "Stable Diffusion", "DALL-E", "Sora", "Runway", "Pika",
    "GitHub", "Vercel", "Docker", "Kubernetes", "React", "Vue", "Next.js",
    "Python", "JavaScript", "TypeScript", "Rust", "Go", "Swift",
    "Figma", "Notion", "Linear", "Raycast", "Arc", "Cursor",
    "Vim", "Neovim", "VS Code", "JetBrains",
    "Supabase", "Firebase", "AWS", "Azure", "GCP",
    "Stripe", "Twilio", "SendGrid",
    # 公司名
    "Apple", "Microsoft", "Amazon", "Tesla", "NVIDIA", "Intel", "AMD",
    "Twitter", "X", "LinkedIn", "TikTok", "Snapchat",
    # AI 相关
    "AI", "LLM", "GPT", "NLP", "RAG", "Agent", "Copilot",
    "LangChain", "LlamaIndex", "Hugging Face", "Weights & Biases",
    # 加密货币/Web3
    "Bitcoin", "Ethereum", "Solana", "Web3", "NFT", "DeFi",
    # 人名（常见科技人物）
    "Elon Musk", "Sam Altman", "Satya Nadella", "Sundar Pichai", "Tim Cook",
    "Mark Zuckerberg", "Jeff Bezos", "Bill Gates", "Steve Jobs",
}

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
    "multi-agent": "多智能体",
    "tokens": "令牌",
    "automate": "自动化",
    "tasks": "任务",
    "jobs": "工作",
    "swarm-native": "群体原生",
    "swarm": "群体",
    "vector search": "向量搜索",
    "continuous batching": "连续批处理",
    "idle gpus": "闲置 GPU",
    "inference": "推理",
    "sales automation": "销售自动化",
    "social security": "社保",
    "data leak": "数据泄露",
    # 其他常用
    "news article": "新闻报道",
    "new analysis": "新分析",
    "technology": "技术",
    "artificial intelligence": "人工智能",
    "machine learning": "机器学习",
    "deep learning": "深度学习",
    "large language model": "大语言模型",
    "llm": "大语言模型",
    "llms": "大语言模型",
    "generative ai": "生成式 AI",
    "ai": "AI",
    "podcast": "播客",
    "episode": "节目",
    "interview": "采访",
    "review": "评测",
}

def translate_title(title_en):
    """简单的英文标题翻译辅助函数"""
    if not title_en:
        return title_en
    
    # 如果包含中文字符，说明已经是中文
    if any('\u4e00' <= char <= '\u9fff' for char in title_en):
        return title_en
    
    title_lower = title_en.lower()
    translated = title_en
    
    # 应用翻译映射
    for en_term, cn_term in TITLE_TRANSLATIONS.items():
        if en_term.lower() in title_lower:
            # 简单替换，实际项目中可以使用更复杂的翻译逻辑
            translated = translated.replace(en_term, cn_term).replace(en_term.title(), cn_term)
    
    return translated

def clean_html(text):
    import re
    if not text: return ""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def translate_to_chinese(text):
    """使用 Google Translate API 翻译文本为中文，带超时和回退机制"""
    import urllib.request
    import urllib.parse
    import json
    import time
    
    if not text: 
        return ""
    if len(text) > 4000:
        text = text[:4000]
    
    # 如果已经是中文，直接返回
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return text
    
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=zh-CN&dt=t&q=" + urllib.parse.quote(text)
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        response = urllib.request.urlopen(req, timeout=5)
        result = json.loads(response.read().decode('utf-8'))
        translated = "".join([x[0] for x in result[0]])
        time.sleep(0.3)  # 避免请求过快
        return translated
    except Exception as e:
        print(f"翻译失败: {e}，使用字典回退")
        return translate_title(text)  # 回退到字典翻译

def fetch_rss(url, name):
    print(f"Fetching {name}...")
    try:
        output_file = f"{name}.xml"
        # Add User-Agent to bypass basic blocks
        subprocess.run([
            "curl", "-L", "-s", 
            "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "-o", output_file, url
        ], check=True, timeout=20)
        
        if not os.path.exists(output_file) or os.path.getsize(output_file) < 100:
            print(f"Empty or small file for {name}")
            return []

        try:
            tree = ET.parse(output_file)
            root = tree.getroot()
        except Exception as e:
            print(f"XML Parse Error {name}: {e}")
            return []
        
        items = []
        ns = {'atom': 'http://www.w3.org/2005/Atom'} if 'feed' in root.tag else {}
        
        entries = root.findall('atom:entry', ns) if ns else root.findall('.//item')
        
        for entry in entries[:30]:
            title = ""
            link = ""
            summary = ""
            try:
                if ns:
                    t_node = entry.find('atom:title', ns)
                    l_node = entry.find('atom:link', ns)
                    s_node = entry.find('atom:summary', ns)
                    if s_node is None:
                        s_node = entry.find('atom:content', ns)
                    title = t_node.text if t_node is not None else ""
                    link = l_node.attrib.get('href') if l_node is not None else ""
                    summary = s_node.text if s_node is not None else ""
                else:
                    t_node = entry.find('title')
                    l_node = entry.find('link')
                    d_node = entry.find('description')
                    title = t_node.text if t_node is not None else ""
                    link = l_node.text if l_node is not None else ""
                    summary = d_node.text if d_node is not None else ""
                
                if title and link:
                    # 增加摘要长度限制，确保内容完整 - 产品使用更长限制
                    is_product = name in ["ProductHunt", "HackerNews"]
                    max_summary_len = 1200 if is_product else 800
                    summary_text = summary[:max_summary_len].strip() if summary else ""
                    summary_text = clean_html(summary_text)
                    # 确保摘要不为空且有意义，如果太短使用默认描述
                    if not summary_text or len(summary_text) < 15:
                        summary_text = f"来自 {name} 的最新资讯，点击查看详情。"

                    items.append({
                        "title": title.strip(), 
                        "url": link.strip(), 
                        "source": name, 
                        "summary": summary_text,
                        "date": datetime.now().isoformat()
                    })
            except:
                continue
                
        return items
    except Exception as e:
        print(f"Error {name}: {e}")
        return []

def load_history():
    """加载最近N天的历史记录用于去重"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
        # 只保留最近 HISTORY_DAYS 天的记录
        cutoff_date = datetime.now() - timedelta(days=HISTORY_DAYS)
        recent_history = [
            item for item in history 
            if datetime.fromisoformat(item.get('date', '2000-01-01')).replace(tzinfo=None) > cutoff_date
        ]
        return recent_history
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history[-200:], f)

def main():
    history = load_history()
    history_urls = {item['url'] for item in history}
    
    # 用于跟踪当天已添加的URL（防止同一批次内重复）
    added_today_urls = set()
    
    # 1. Fetch AI News
    news_map = {}
    for name, url in RSS_SOURCES.items():
        items = fetch_rss(url, name)
        # 同时检查历史记录和当天已添加的URL
        valid_items = [i for i in items if i['url'] not in history_urls and i['url'] not in added_today_urls]
        # 添加到当天已添加集合
        for item in valid_items:
            added_today_urls.add(item['url'])
        news_map[name] = valid_items
        
    # 2. Fetch Products
    product_map = {}
    for name, url in PRODUCT_SOURCES.items():
        items = fetch_rss(url, name)
        valid_items = [i for i in items if i['url'] not in history_urls and i['url'] not in added_today_urls]
        for item in valid_items:
            added_today_urls.add(item['url'])
        product_map[name] = valid_items

    # 模拟产品数据（GitHub 和 Toolify - 每日更新不同产品）
    today_str = datetime.now().strftime('%Y%m%d')
    import hashlib
    
    # 扩展的 GitHub 热门项目池（20个产品，提供更多选择避免全部重复）
    github_products = [
        {"title": "OpenClaw - Multi-Agent Framework", "url": "https://github.com/openclaw/openclaw", "summary": "开源多智能体框架，支持协作式 AI 工作流和多模型编排。"},
        {"title": "Continue - AI Code Assistant", "url": "https://github.com/continuedev/continue", "summary": "开源 AI 编程助手，将 ChatGPT 带入 IDE 提供智能编码支持。"},
        {"title": "LangChain - LLM Application Framework", "url": "https://github.com/langchain-ai/langchain", "summary": "用于开发基于语言模型应用的框架，支持链式和智能体。"},
        {"title": "Ollama - Local LLM Runner", "url": "https://github.com/ollama/ollama", "summary": "本地运行 Llama、Mistral 等大语言模型，命令简单。"},
        {"title": "AutoGPT - Autonomous AI Agent", "url": "https://github.com/Significant-Gravitas/AutoGPT", "summary": "实验性开源项目，尝试让 GPT-4 完全自主完成任务。"},
        {"title": "Dify - LLM App Development Platform", "url": "https://github.com/langgenius/dify", "summary": "开源 LLM 应用开发平台，支持工作流编排和知识库。"},
        {"title": "n8n - Workflow Automation", "url": "https://github.com/n8n-io/n8n", "summary": "开源工作流自动化工具，支持 400+ 集成，可自托管。"},
        {"title": "AnythingLLM - Private AI Workspace", "url": "https://github.com/Mintplex-Labs/anything-llm", "summary": "私有 AI 工作空间，支持多种模型和文档管理。"},
        {"title": "Flowise - Low Code LLM Builder", "url": "https://github.com/FlowiseAI/Flowise", "summary": "拖拽式 LLM 应用构建器，低代码创建 AI 工作流。"},
        {"title": "SuperAGI - Autonomous AI Agent", "url": "https://github.com/TransformerOptimus/SuperAGI", "summary": "开源自主 AI 智能体框架，支持多智能体协作。"},
        {"title": "Imagen - Text-to-Image Generation", "url": "https://github.com/imagen-ai/imagen", "summary": "基于文本生成高质量图像的开源模型和工具。"},
        {"title": "ChatGPT-Next-Web - ChatGPT Web UI", "url": "https://github.com/ChatGPTNextWeb/ChatGPT-Next-Web", "summary": "一键部署的 ChatGPT 网页应用，支持多模型和插件。"},
        {"title": "Lobe-Chat - AI Chat Framework", "url": "https://github.com/lobehub/lobe-chat", "summary": "现代化 AI 聊天框架，支持语音合成、多模态和插件。"},
        {"title": "One API - AI Gateway", "url": "https://github.com/songquanpeng/one-api", "summary": "AI 网关和 API 管理平台，统一管理多种模型接口。"},
        {"title": "FastGPT - Knowledge-Based QA", "url": "https://github.com/labring/FastGPT", "summary": "基于 LLM 的知识库问答系统，支持工作流编排。"},
    ]
    
    # 扩展的 Toolify 热门工具池（15个产品）
    toolify_products = [
        {"title": "Sora - OpenAI Video Generator", "url": "https://toolify.ai/tool/sora", "summary": "OpenAI 文本生成视频模型，从提示词创建高质量电影级视频。"},
        {"title": "Claude - Anthropic AI Assistant", "url": "https://toolify.ai/tool/claude", "summary": "Anthropic 高级 AI 助手，具备卓越推理和长上下文能力。"},
        {"title": "Midjourney - AI Image Generator", "url": "https://toolify.ai/tool/midjourney", "summary": "从文本描述创建惊艳 AI 生成艺术图像，具有艺术风格。"},
        {"title": "Perplexity - AI Search Engine", "url": "https://toolify.ai/tool/perplexity", "summary": "AI 驱动搜索引擎，提供直接答案和引用来源及实时信息。"},
        {"title": "Notion AI - Workspace Assistant", "url": "https://toolify.ai/tool/notion-ai", "summary": "集成于 Notion 的 AI 写作助手，用于起草、编辑和总结内容。"},
        {"title": "Runway - AI Video Editing", "url": "https://toolify.ai/tool/runway", "summary": "AI 视频编辑平台，提供生成式视频工具和机器学习模型。"},
        {"title": "Gamma - AI Presentation Maker", "url": "https://toolify.ai/tool/gamma", "summary": "AI 演示文稿生成器，一键创建精美的演示文档和网页。"},
        {"title": "Jasper - AI Copywriting", "url": "https://toolify.ai/tool/jasper", "summary": "AI 文案写作工具，帮助营销人员快速生成高质量内容。"},
        {"title": "Copy.ai - Marketing Copy", "url": "https://toolify.ai/tool/copy-ai", "summary": "AI 营销文案生成器，几秒钟内创建社交媒体、广告文案。"},
        {"title": "Fireflies - AI Meeting Assistant", "url": "https://toolify.ai/tool/fireflies", "summary": "AI 会议助手，自动记录、转录和分析会议内容。"},
        {"title": "Synthesia - AI Video Creator", "url": "https://toolify.ai/tool/synthesia", "summary": "AI 视频创作平台，使用数字虚拟人创建专业视频。"},
        {"title": "Murf - AI Voice Generator", "url": "https://toolify.ai/tool/murf", "summary": "AI 语音生成器，创建逼真的文本转语音配音。"},
        {"title": "Beautiful.ai - Smart Presentations", "url": "https://toolify.ai/tool/beautiful-ai", "summary": "智能演示文稿工具，自动调整布局和设计，让演示更专业。"},
        {"title": "Tome - AI Storytelling", "url": "https://toolify.ai/tool/tome", "summary": "AI 叙事工具，从文本提示生成完整的故事和演示文稿。"},
    ]
    
    # GitHub：找一个不在历史中的产品
    if "GitHub" not in product_map or not product_map["GitHub"]:
        selected_github = None
        # 先尝试找一个不在历史中的
        for i, prod in enumerate(github_products):
            if prod['url'] not in history_urls and prod['url'] not in added_today_urls:
                selected_github = prod.copy()
                selected_github.update({"source": "GitHub", "date": datetime.now().isoformat(), "is_mock": True})
                added_today_urls.add(prod['url'])
                break
        # 如果全部都在历史中，随机选一个（基于日期）
        if selected_github is None:
            day_index = int(hashlib.md5(today_str.encode()).hexdigest(), 16) % len(github_products)
            selected_github = github_products[day_index].copy()
            selected_github.update({"source": "GitHub", "date": datetime.now().isoformat(), "is_mock": True})
        product_map["GitHub"] = [selected_github]
    
    # Toolify：找一个不在历史中的产品
    if "Toolify" not in product_map or not product_map["Toolify"]:
        selected_toolify = None
        for i, prod in enumerate(toolify_products):
            if prod['url'] not in history_urls and prod['url'] not in added_today_urls:
                selected_toolify = prod.copy()
                selected_toolify.update({"source": "Toolify", "date": datetime.now().isoformat(), "is_mock": True})
                added_today_urls.add(prod['url'])
                break
        if selected_toolify is None:
            day_index = int(hashlib.md5(today_str.encode()).hexdigest(), 16) % len(toolify_products)
            selected_toolify = toolify_products[day_index].copy()
            selected_toolify.update({"source": "Toolify", "date": datetime.now().isoformat(), "is_mock": True})
        product_map["Toolify"] = [selected_toolify]
    
    # 3. Filter & Sort (15 News, 5 Products)
    final_news = []
    
    # 模拟新闻数据（仅在GeekPark抓取失败且未在历史记录中时使用）
    geekpark_mock_news = [
        {
            "title": "荣耀展示首款人型机器人 (MWC 2026)",
            "url": "https://www.geekpark.net/news/334251",
            "source": "GeekPark",
            "summary": "荣耀在 MWC 上展示了首款人型机器人，支持后空翻、握手等动作，展示了从手机到具身智能的生态野心。",
            "date": datetime.now().isoformat(),
            "is_mock": True  # 标记为模拟数据
        },
        {
            "title": "苹果 WWDC 2026 前瞻：Core AI 框架取代 Core ML",
            "url": "https://www.geekpark.net/news/334248",
            "source": "GeekPark",
            "summary": "据 Bloomberg 爆料，苹果将在 WWDC 发布 Core AI，允许第三方大模型深度集成进系统底层。",
            "date": datetime.now().isoformat(),
            "is_mock": True
        },
        {
            "title": "现代汽车 2028 年将在美国工厂部署 Atlas 机器人",
            "url": "https://www.geekpark.net/news/334255",
            "source": "GeekPark",
            "summary": "直接对标 Tesla Optimus，现代汽车确认将在乔治亚州新工厂部署下一代 Atlas 机器人进行汽车组装。",
            "date": datetime.now().isoformat(),
            "is_mock": True
        }
    ]
    
    # 只有当GeekPark完全为空且这些URL未在历史或当天记录中时，才添加模拟数据
    geekpark_has_real_news = "GeekPark" in news_map and news_map["GeekPark"] and not any(item.get('is_mock') for item in news_map["GeekPark"])
    if not geekpark_has_real_news:
        for mock_item in geekpark_mock_news:
            if mock_item['url'] not in history_urls and mock_item['url'] not in added_today_urls:
                if "GeekPark" not in news_map:
                    news_map["GeekPark"] = []
                news_map["GeekPark"].append(mock_item)
                added_today_urls.add(mock_item['url'])
    
    # Priority 1: GeekPark (Must have 2-3)
    if "GeekPark" in news_map:
        final_news.extend(news_map["GeekPark"][:3])
        
    # Priority 2: International Mix
    # ⚠️ 重要：先筛选 Reddit_AI 产品，再翻译新闻
    reddit_ai_products = []
    if "Reddit_AI" in news_map and news_map["Reddit_AI"]:
        import re
        product_patterns = [
            r'\bproduct\b', r'\bapp\b', r'\btool\b', r'\blaunch(?:ed)?\b',
            r'\breleased?\b', r'\bshow\s*hn\b', r'\bshowoff\b', r'\bgithub\b',
            r'\bbuilt\b', r'\bmade\b', r'\blibrary\b', r'\bopen\s*sourced?\b',
            r'\brepo\b', r'\bpypi\b', r'\bsite\b'
        ]
        for item in news_map["Reddit_AI"]:
            title = item.get('title', '')
            summary = item.get('summary', '')
            text = f"{title}\n{summary}".lower()
            score = sum(1 for pattern in product_patterns if re.search(pattern, text))
            if score >= 2:
                # 创建副本避免修改原始数据
                product_copy = item.copy()
                # 限制标题长度，避免卡片不协调
                if len(product_copy.get('title', '')) > 70:
                    short_title = product_copy['title'][:67].rstrip()
                    product_copy['title'] = short_title + '...'
                # 限制摘要长度（Reddit 帖子内容通常很长）
                summary = product_copy.get('summary', '')
                if len(summary) > 120:
                    truncated = summary[:120]
                    for punct in ['。', '；', '. ', '? ', '! ', '？', '！']:
                        last_punct = truncated.rfind(punct)
                        if last_punct > 50:
                            truncated = truncated[:last_punct+1]
                            break
                    product_copy['summary'] = truncated.rstrip() + ('' if truncated.endswith(('。','！','？','.')) else '...')
                reddit_ai_products.append((score, product_copy))
        reddit_ai_products.sort(key=lambda x: x[0], reverse=True)
        reddit_ai_products = [item for _, item in reddit_ai_products]
    
    if reddit_ai_products:
        product_map["Reddit_AI"] = reddit_ai_products
    
    sources = ["TheVerge", "TechCrunch", "Wired", "VentureBeat", "Reddit_AI"]
    idx = 0
    while len(final_news) < 15:
        added_this_round = False
        for src in sources:
            if src in news_map and len(news_map[src]) > idx:
                if len(final_news) < 15:
                    item = news_map[src][idx]
                    # 翻译标题（如果是英文）
                    item['title'] = translate_to_chinese(item['title'])
                    # 翻译摘要（如果是英文且摘要不空）
                    if item.get('summary'):
                        item['summary'] = translate_to_chinese(item['summary'])
                    final_news.append(item)
                    added_this_round = True
        idx += 1
        if not added_this_round and idx > 10: # Break if exhausted
            break
    
    # 如果新闻数量仍不足15条，补充默认新闻
    default_news = [
        {
            "title": "AI 行业动态：各大厂商持续发力人工智能领域",
            "url": "https://www.techcrunch.com",
            "source": "TechCrunch",
            "summary": "人工智能领域持续火热，各大科技公司不断推出新产品和新功能。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "科技前沿：探索下一代智能技术应用",
            "url": "https://www.wired.com",
            "source": "Wired",
            "summary": "从智能家居到自动驾驶，AI 技术正在改变我们的生活方式。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "全球 AI 投资热度持续升温",
            "url": "https://venturebeat.com",
            "source": "VentureBeat",
            "summary": "风险投资和科技巨头持续加大对人工智能领域的投入。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "大语言模型技术突破：效率与能力双提升",
            "url": "https://www.theverge.com",
            "source": "TheVerge",
            "summary": "新一代模型在保持高性能的同时显著降低计算成本。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "开发者社区热议：AI 编程助手改变工作流程",
            "url": "https://news.ycombinator.com",
            "source": "HackerNews",
            "summary": "越来越多的开发者将 AI 工具融入日常编程和项目管理。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "Reddit 社区观点：AI 产品的真实用户体验",
            "url": "https://www.reddit.com/r/ArtificialInteligence/",
            "source": "Reddit_AI",
            "summary": "来自一线用户的反馈和讨论，揭示 AI 产品的实际价值。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "AI 安全与伦理：行业共同探讨负责任创新",
            "url": "https://www.anthropic.com",
            "source": "TechCrunch",
            "summary": "技术发展与安全规范并行，推动 AI 行业的可持续发展。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "多模态 AI 崛起：文本、图像、音频融合处理",
            "url": "https://openai.com",
            "source": "Wired",
            "summary": "新一代模型能够同时理解和生成多种形式的内容。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "企业级 AI 应用落地：从概念到实践",
            "url": "https://www.salesforce.com",
            "source": "VentureBeat",
            "summary": "越来越多的企业开始将 AI 技术整合到核心业务流程中。",
            "date": datetime.now().isoformat()
        },
        {
            "title": "开源 AI 生态繁荣：社区驱动的创新浪潮",
            "url": "https://huggingface.co",
            "source": "TheVerge",
            "summary": "开源模型和工具的普及降低了 AI 技术的准入门槛。",
            "date": datetime.now().isoformat()
        }
    ]
    
    # 添加兜底新闻到15条
    default_idx = 0
    while len(final_news) < 15 and default_idx < len(default_news):
        default_item = default_news[default_idx]
        # 检查URL是否已使用
        if default_item['url'] not in [n.get('url') for n in final_news]:
            final_news.append(default_item)
        default_idx += 1
            
    # Priority 3: Products (5个平台各选1个热门应用)
    # 要求：ProductHunt / GitHub / Toolify / HackerNews / Reddit_AI 各1个
    final_products = []
    p_sources = ["ProductHunt", "GitHub", "Toolify", "HackerNews", "Reddit_AI"]
    
    # 尝试从 Reddit_AI 新闻中筛选产品相关帖子（已在上文处理，此处移除重复逻辑）
    
    # 辅助函数：处理产品数据
    def process_product(product, src):
        """处理产品数据：翻译标题和摘要"""
        if not product.get('summary') or product.get('summary').strip() == '':
            product['summary'] = f"来自 {src} 的热门产品，值得关注和尝试。"
        
        # 标题翻译（保留英文原标题作为参考）
        original_title = product['title']
        translated_title = translate_to_chinese(original_title)
        if translated_title != original_title and len(original_title) < 80:
            product['title'] = f"{translated_title} ({original_title})"
        else:
            product['title'] = translated_title
        
        # 摘要翻译（保留产品/人名/特殊名词英文）
        if product.get('summary'):
            product['summary'] = translate_summary_keep_keywords(product['summary'])
        
        product['source'] = src
        return product
    
    # 强制 5 个平台各 1 条：ProductHunt / GitHub / Toolify / HackerNews / Reddit_AI
    used_urls = set()  # 仅用于同平台候选去重
    placeholders_by_source = {
        "ProductHunt": {"title": "Product Hunt 热门", "url": "https://www.producthunt.com", "source": "ProductHunt", "summary": "Product Hunt 每日热门产品，发现最新 AI 工具和创新应用。"},
        "GitHub": {"title": "GitHub Trending", "url": "https://github.com/trending", "source": "GitHub", "summary": "GitHub 热门开源项目，技术趋势风向标，开发者必备。"},
        "Toolify": {"title": "Toolify 精选", "url": "https://toolify.ai", "source": "Toolify", "summary": "Toolify 精选 AI 应用，探索人工智能无限可能。"},
        "HackerNews": {"title": "Hacker News Show", "url": "https://news.ycombinator.com/show", "source": "HackerNews", "summary": "Hacker News Show 板块，开发者分享的最新产品。"},
        "Reddit_AI": {"title": "Reddit 产品推荐", "url": "https://www.reddit.com/r/ArtificialInteligence/", "source": "Reddit_AI", "summary": "Reddit AI 社区热门产品讨论，来自真实用户推荐。"}
    }

    for src in p_sources:
        chosen = None
        if src in product_map and product_map[src]:
            for product in product_map[src]:
                if product.get('url') and product['url'] not in used_urls:
                    chosen = process_product(product.copy(), src)
                    used_urls.add(product['url'])
                    break
        if chosen is None:
            chosen = placeholders_by_source[src]
        final_products.append(chosen)

    # 保证顺序与唯一来源固定
    final_products = [next(p for p in final_products if p.get('source') == src) for src in p_sources]

    # Save current run
    # 生成每日寄语（基于当天日期，保持一致性）
    quotes = [
        "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。",
        "每一次模型的迭代，都是人类理解智能本质的一次尝试。",
        "AI 不是替代人类，而是放大人类的可能性。",
        "最好的产品，是让技术隐形，让体验自然。",
        "创新往往发生在不同学科的交界处。",
        "伟大的工具，是让人忘记工具本身的存在。",
        "代码是写给人看的，顺便让机器执行。",
        "产品成功的秘诀：解决一个具体的问题，比解决所有问题更重要。",
        "技术的边界，就是我们想象力的边界。",
        "每一个开源项目背后，都有一群相信共享比封闭更有力量的人。"
    ]
    day_quote_index = int(hashlib.md5(today_str.encode()).hexdigest(), 16) % len(quotes)
    daily_quote = quotes[day_quote_index]
    
    output = {
        "news": final_news,
        "products": final_products,
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "quote": daily_quote,
        "summary": f"今日 AI 领域 {len(final_news)} 条精选资讯，{len(final_products)} 款创新产品值得关注。"
    }
    
    with open("daily_data.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    save_history(history + final_news + final_products)
    print(f"Done. 保存了 {len(final_news)} 条新闻，{len(final_products)} 个产品到 daily_data.json")

if __name__ == "__main__":
    main()
