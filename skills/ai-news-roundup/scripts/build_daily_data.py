#!/usr/bin/env python3
"""Agent 质量 pass: candidates.json → daily_data.json

对象事件级去重 + 主题聚类标注 + 历史污染拦截 + 产品雷达质量过滤。
脚本职责：
  - 对新闻候选做结构化补全与真重复判定
  - 保留同主题不同对象的并行进展，并打上聚类字段
  - 阻断 historical_review / 历史资料污染
  - 对产品候选做“具体产品/工具/项目”门禁
  - 输出带结构字段的 daily_data.json
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from zoneinfo import ZoneInfo

PROJECT_DIR = Path(__file__).resolve().parents[1]
TZ = ZoneInfo('Asia/Taipei')
UTZ = ZoneInfo('UTC')
now = datetime.now(TZ)
today_str = now.strftime('%Y年%m月%d日')
weekday = '一二三四五六日'[now.weekday()]

SOCIAL_DOMAINS = {'x.com', 'twitter.com'}
NEWSY_DOMAINS = {
    'reuters.com', 'techcrunch.com', 'theverge.com', 'venturebeat.com', 'wired.com',
    'bloomberg.com', 'nytimes.com', 'wsj.com', 'ft.com', 'axios.com', 'theinformation.com',
}
TRACKING_QUERY_KEYS = {
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'fbclid', 'gclid', 'ref', 'ref_src', 'ref_url', 'source',
}

TAG_KEYWORDS: dict[str, list[str]] = {
    '资本': ['融资', 'ipo', '收购', '投资', '估值', '美元', '亿元', 'funding', 'raise',
             'investor', 'valuation', 'billion', 'million', 'acquire', 'acquisition'],
    '模型': ['模型', '参数', '推理', 'token', '上下文', '训练', '微调', '预训练', 'model',
             'reasoning', 'parameter', 'fine-tun', 'pretrain', 'context window', 'benchmark'],
    'Agent': ['agent', '智能体', '代理', '自主', '多步', '工具调用', 'agentic', 'autonomous',
              'multi-step', 'tool use'],
    '基础设施': ['基础设施', '平台', '部署', 'api', '云', '芯片', '算力', '数据中心', 'infrastructure',
               'platform', 'deploy', 'cloud', 'data center', 'compute'],
    '开源': ['开源', 'open source', 'github', '社区', 'open-source', 'repository', 'repo',
             'apache', 'mit license', 'gpl'],
    '产品': ['发布', '产品', '上线', '推出', '应用', 'launch', 'release', 'shipping',
             'rollout', 'product', 'unveil'],
    '研究': ['研究', '论文', '学术', '实验', '科学', '突破', 'research', 'paper', 'study',
             'breakthrough', 'science', 'discover'],
    '政策': ['政策', '监管', '法律', '隐私', '合规', '治理', '禁令', 'regulation', 'policy',
             'privacy', 'compliance', 'govern', 'ban', 'law'],
    '应用': ['医疗', '金融', '教育', '工业', '视频', '音乐', '图像', '生成', '创作', 'health',
             'finance', 'education', 'video', 'music', 'image', 'generate', 'creation'],
    '硬件': ['芯片', 'gpu', '算力', '硬件', '服务器', '半导体', 'chip', 'hardware', 'server',
             'semiconductor', 'compute', 'h100', 'b200'],
    '行业': ['行业', '市场', '企业', '公司', '商业', 'industry', 'market', 'enterprise',
             'business', 'company', 'startup', 'saas'],
    '全球': ['全球', '国际', '美国', '中国', '欧洲', '各国', 'global', 'international',
             'us', 'china', 'europe', 'worldwide'],
}

TOPIC_RULES = [
    {
        'key': 'audio-generation',
        'label': 'AI 音频生成',
        'keywords': ['audio', 'voice', 'speech', 'music', 'tts', '配音', '语音', '音频', '音乐'],
        'capabilities': ['voice-ai', 'audio-model', 'music-generation'],
    },
    {
        'key': 'video-generation',
        'label': 'AI 视频生成',
        'keywords': ['video', 'movie', '镜头', '视频', '短片', '影像'],
        'capabilities': ['video-generation', 'prompting', 'multimodal-creation'],
    },
    {
        'key': 'coding-agent',
        'label': 'Coding Agent',
        'keywords': ['claude code', 'copilot', 'code', 'coding', '开发者', '编程', '插件', 'plugin'],
        'capabilities': ['developer-tooling', 'coding-agent', 'security-assistant'],
    },
    {
        'key': 'search-discovery',
        'label': '搜索与信息分发',
        'keywords': ['search', 'duckduckgo', '搜索', '检索', '浏览器', 'discovery'],
        'capabilities': ['search', 'distribution', 'consumer-product'],
    },
    {
        'key': 'model-infra',
        'label': '模型基础设施',
        'keywords': ['api', 'inference', 'router', 'infra', 'infrastructure', 'deployment', '平台', '基础设施'],
        'capabilities': ['model-routing', 'inference-platform', 'developer-infra'],
    },
    {
        'key': 'open-source-devtools',
        'label': '开源开发工具',
        'keywords': ['open source', 'github', 'repo', 'repository', '开源', '代码库'],
        'capabilities': ['open-source', 'developer-tooling', 'knowledge-graph'],
    },
    {
        'key': 'ai-policy',
        'label': 'AI 治理与政策',
        'keywords': ['policy', 'regulation', 'license', '监管', '政策', '合规', '治理', '法律'],
        'capabilities': ['policy', 'compliance', 'market-access'],
    },
    {
        'key': 'ai-safety',
        'label': 'AI 安全',
        'keywords': ['security', 'safety', '漏洞', '安全', 'risk'],
        'capabilities': ['ai-safety', 'security', 'developer-tooling'],
    },
    {
        'key': 'agent-workflow',
        'label': 'Agent 工作流',
        'keywords': ['agent', 'workflow', 'orchestration', '自动化', '智能体', '编排'],
        'capabilities': ['agentic-workflow', 'automation', 'tool-use'],
    },
    {
        'key': 'research-frontier',
        'label': '研究前沿',
        'keywords': ['research', 'paper', 'benchmark', '研究', '论文', '基准'],
        'capabilities': ['research', 'benchmark', 'frontier-model'],
    },
]

EVENT_RULES = [
    ('funding', ['融资', '投资', '估值', 'funding', 'raise', 'valuation', 'series a', 'series b']),
    ('acquisition', ['收购', 'acquire', 'acquisition', 'merge', 'merger']),
    ('partnership', ['合作', 'partnership', 'partner', 'jointly', '联盟']),
    ('policy', ['政策', '监管', '禁令', 'license', 'regulation', 'policy', 'compliance']),
    ('open_source', ['开源', 'github', 'repo', 'open source', 'open-source']),
    ('research_release', ['论文', '研究', 'benchmark', 'paper', 'research', 'study']),
    ('update', ['update', '更新', '升级', 'guide', '指南', 'plugin', '安全补丁', '改版']),
    ('launch', ['推出', '发布', '上线', 'launch', 'release', 'ship', 'unveil']),
]

PRODUCT_ALIASES = [
    ('Claude Code', 'Anthropic', 'product', ['claude code']),
    ('Claude', 'Anthropic', 'model', ['claude']),
    ('Gemini Omni', 'Google', 'model', ['gemini omni']),
    ('Gemini', 'Google', 'model', ['gemini']),
    ('OpenRouter', 'OpenRouter', 'platform', ['openrouter']),
    ('DuckDuckGo', 'DuckDuckGo', 'product', ['duckduckgo']),
    ('Stable Audio', 'Stability AI', 'product', ['stable audio']),
    ('OmniVoice Studio', 'OmniVoice', 'product', ['omnivoice studio']),
    ('ChatGPT', 'OpenAI', 'product', ['chatgpt']),
    ('Sora', 'OpenAI', 'product', ['sora']),
    ('GitHub Copilot', 'Microsoft', 'product', ['github copilot', 'copilot']),
    ('Llama', 'Meta', 'model', ['llama']),
    ('Qwen', 'Alibaba', 'model', ['qwen']),
    ('DeepSeek', 'DeepSeek', 'model', ['deepseek']),
    ('MiniCPM5-1B', 'MiniCPM', 'model', ['minicpm5-1b', 'minicpm 5-1b', 'minicpm']),
    ('Understand Anything', 'Understand Anything', 'product', ['understand-anything', 'understand anything']),
    ('Instagram Comments Scraper', 'Instagram Comments Scraper', 'product', ['instagram comments scraper']),
    ('Synta', 'Synta', 'product', ['synta']),
]

COMPANY_ALIASES = {
    'Anthropic': ['anthropic', 'claude'],
    'Google': ['google', 'google ai', 'deepmind', 'gemini'],
    'OpenAI': ['openai', 'chatgpt', 'gpt-4', 'gpt-5', 'sora'],
    'Meta': ['meta', 'llama'],
    'Microsoft': ['microsoft', 'github copilot', 'copilot'],
    'DuckDuckGo': ['duckduckgo'],
    'OpenRouter': ['openrouter'],
    'Stability AI': ['stability ai', 'stable audio'],
    'DeepSeek': ['deepseek'],
    'Alibaba': ['alibaba', 'qwen'],
    'NVIDIA': ['nvidia'],
    'Mistral': ['mistral'],
    'xAI': ['xai', 'grok'],
}

SOURCE_KIND_BY_SOURCE = {
    'Product Hunt': 'product_source',
    'GitHub': 'product_source',
    'Toolify': 'product_source',
    'Trustmrr': 'product_source',
    'Hacker News': 'product_source',
}


def contains_chinese(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text or ''))


def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text or '')
    text = re.sub(r'\s+', ' ', text or '').strip()
    return text


def canonicalize_url(url: str) -> str:
    if not url:
        return ''
    parsed = urlparse(url.strip())
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True) if k.lower() not in TRACKING_QUERY_KEYS]
    path = parsed.path.rstrip('/') or '/'
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, '', urlencode(query), ''))


def domain_of(url: str) -> str:
    netloc = urlparse(url).netloc.lower()
    return netloc[4:] if netloc.startswith('www.') else netloc


def parse_published_at(value: str, fallback_ts: float = 0.0) -> datetime:
    if value:
        try:
            if 'T' in value:
                dt = datetime.fromisoformat(value)
                return dt if dt.tzinfo else dt.replace(tzinfo=TZ)
        except Exception:
            pass
        try:
            dt = parsedate_to_datetime(value)
            return dt if dt.tzinfo else dt.replace(tzinfo=UTZ)
        except Exception:
            pass
    if fallback_ts:
        return datetime.fromtimestamp(fallback_ts, tz=UTZ)
    return now


def normalize_name(text: str) -> str:
    text = (text or '').lower().strip()
    text = text.replace('｜', '|')
    text = re.sub(r'https?://', '', text)
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '', text)
    return text


def tokenize_for_similarity(text: str) -> set[str]:
    text = (text or '').lower()
    word_tokens = set(re.findall(r'[a-z0-9]{2,}', text))
    chinese = ''.join(re.findall(r'[\u4e00-\u9fff]', text))
    zh_tokens = {chinese[i:i+2] for i in range(max(0, len(chinese) - 1))}
    return {t for t in word_tokens | zh_tokens if t}


def jaccard_similarity(a: str, b: str) -> float:
    ta = tokenize_for_similarity(a)
    tb = tokenize_for_similarity(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta | tb), 1)


def within_hours(a: datetime, b: datetime, hours: int) -> bool:
    return abs((a - b).total_seconds()) <= hours * 3600


def classify_tags(item: dict) -> list[str]:
    text = ' '.join([
        item.get('title_zh', '') or item.get('title_en', '') or item.get('title', '') or '',
        item.get('summary_zh', '') or item.get('summary_en', '') or item.get('summary', '') or '',
        item.get('canonical_topic', '') or '',
        ' '.join(item.get('capability_tags', []) or []),
    ])
    text_lower = text.lower()
    scores: dict[str, int] = {}
    for tag, keywords in TAG_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        if score > 0:
            scores[tag] = score
    sorted_tags = sorted(scores.keys(), key=lambda t: scores[t], reverse=True)
    return sorted_tags[:3]


def trim_title(item: dict, max_chars: int = 20) -> str:
    zh = clean_text(item.get('title_zh') or '')
    en = clean_text(item.get('title_en') or '')

    if zh and contains_chinese(zh):
        cn_chars = len(re.findall(r'[\u4e00-\u9fff]', zh))
        total = len(zh)
        cn_ratio = cn_chars / max(total, 1)
        if cn_ratio >= 0.4 and len(zh) <= 60:
            title = zh.strip(' 。.-—|，,')
            if len(title) <= max_chars:
                return title
            for sep in ['，', '、', '。', '；', '：', '—', '｜', ' ', ',']:
                idx = title[:max_chars + 4].rfind(sep)
                if idx >= max_chars * 0.4:
                    return title[:idx].strip()
            return title[:max_chars].strip()

    title = en or zh or ''
    title = re.sub(r'\s*[' + re.escape('|｜') + r']\s*\w+(\.\w+)*$', '', title)
    if len(title) <= 90:
        return title
    cut = title[:120].rfind(' ')
    if cut > 40:
        return title[:cut].strip() + '…'
    return title[:80].strip() + '…'


def trim_summary(item: dict, max_chars: int = 120) -> str:
    zh = clean_text(item.get('summary_zh') or '')
    en = clean_text(item.get('summary_en') or '')

    if zh and contains_chinese(zh):
        if len(zh) <= max_chars:
            return zh
        for sep in ['。', '；', '！', '？']:
            idx = zh[:max_chars + 5].rfind(sep)
            if idx >= max_chars * 0.5:
                return zh[:idx + 1].strip()
        return zh[:max_chars].strip()

    summary = en or ''
    if len(summary) <= 300:
        return summary
    cut = summary[:400].rfind('. ')
    if cut > 80:
        return summary[:cut + 1].strip()
    return summary[:300].strip() + '…'


def infer_event_type(text: str) -> str:
    lowered = (text or '').lower()
    for event_type, keywords in EVENT_RULES:
        if any(keyword in lowered for keyword in keywords):
            return event_type
    return 'update'


def infer_topic(text: str) -> tuple[str, str, list[str]]:
    lowered = (text or '').lower()
    best = None
    best_score = 0
    for rule in TOPIC_RULES:
        score = sum(1 for keyword in rule['keywords'] if keyword in lowered)
        if score > best_score:
            best = rule
            best_score = score
    if best:
        return best['key'], best['label'], list(best['capabilities'])
    return 'general-ai', 'AI 综合观察', ['ai-general']


def infer_capability_tags(topic_key: str, topic_caps: list[str], text: str) -> list[str]:
    caps = list(topic_caps)
    lowered = (text or '').lower()
    extras = [
        ('security-assistant', ['security', '安全', '漏洞']),
        ('prompting', ['prompt', '提示词', '镜头']),
        ('consumer-product', ['consumer', '安装量', '用户', 'app']),
        ('fundraising', ['funding', '融资', '估值']),
        ('compliance', ['policy', '监管', 'license', '合规']),
        ('benchmark', ['benchmark', '基准']),
        ('multimodal', ['multimodal', '多模态']),
    ]
    for cap, keywords in extras:
        if any(keyword in lowered for keyword in keywords):
            caps.append(cap)
    seen = []
    for cap in caps:
        if cap not in seen:
            seen.append(cap)
    return seen[:4]


def infer_company_product_entity(item: dict, text: str, url: str, is_product: bool = False) -> tuple[str, str, str]:
    lowered = (text or '').lower()
    for product, company, entity_type, aliases in PRODUCT_ALIASES:
        if any(alias in lowered for alias in aliases):
            return company, product, entity_type

    for company, aliases in COMPANY_ALIASES.items():
        if any(alias in lowered for alias in aliases):
            entity_type = 'company'
            product = company
            if any(alias in lowered for alias in ['model', '模型', 'llm', 'gpt', 'claude', 'gemini', 'llama', 'qwen', 'deepseek']):
                entity_type = 'model'
            return company, product, entity_type

    platform = item.get('platform') or item.get('source') or domain_of(url)
    title = clean_text(item.get('title_zh') or item.get('title_en') or item.get('title') or '')
    if is_product:
        product = title or platform
        return platform, product, 'product'
    return platform, title or platform, 'company'


def infer_source_kind(item: dict, is_product: bool = False) -> str:
    explicit = item.get('source_kind')
    if explicit:
        return explicit
    if item.get('is_from_historical_review'):
        return 'historical_review'
    src = item.get('source', '')
    if src in SOURCE_KIND_BY_SOURCE:
        return SOURCE_KIND_BY_SOURCE[src]
    return 'product_source' if is_product else 'news'


def is_historical_review(item: dict, source_kind: str, text: str, url: str) -> bool:
    if source_kind == 'historical_review':
        return True
    if item.get('is_from_historical_review'):
        return True
    lowered = ' '.join([source_kind, text or '', url or '', item.get('source', '') or '']).lower()
    strict_patterns = [
        'historical_review', 'review_doc', 'retro_notes', 'archive_summary',
        '/historical/', '/review-doc/', '/retro/', '/archive/',
    ]
    return any(pattern in lowered for pattern in strict_patterns)


def candidate_quality(item: dict) -> tuple[int, int, int, int, int]:
    domain = domain_of(item.get('url', ''))
    non_social_bonus = 1 if domain not in SOCIAL_DOMAINS else 0
    summary_len = len(item.get('summary_zh') or item.get('summary_en') or '')
    return (
        1 if item.get('must_keep') else 0,
        non_social_bonus,
        int(item.get('weight', 0)),
        summary_len,
        int(item.get('published_ts', 0)),
    )


def is_true_duplicate(a: dict, b: dict) -> bool:
    if a.get('canonical_url') and a.get('canonical_url') == b.get('canonical_url'):
        return True

    a_dt = a.get('published_dt', now)
    b_dt = b.get('published_dt', now)
    close_time = within_hours(a_dt, b_dt, 48)

    same_company = normalize_name(a.get('company', '')) == normalize_name(b.get('company', ''))
    same_product = normalize_name(a.get('product', '')) == normalize_name(b.get('product', ''))
    same_event_type = a.get('event_type') == b.get('event_type')

    title_sim = jaccard_similarity(
        f"{a.get('title_zh', '')} {a.get('title_en', '')}",
        f"{b.get('title_zh', '')} {b.get('title_en', '')}",
    )
    content_sim = jaccard_similarity(
        f"{a.get('title_zh', '')} {a.get('title_en', '')} {a.get('summary_zh', '')} {a.get('summary_en', '')}",
        f"{b.get('title_zh', '')} {b.get('title_en', '')} {b.get('summary_zh', '')} {b.get('summary_en', '')}",
    )

    if same_company and same_product and same_event_type and close_time:
        if title_sim >= 0.45 or content_sim >= 0.72:
            return True
        if (
            a.get('source_domain') in SOCIAL_DOMAINS
            and b.get('source_domain') not in SOCIAL_DOMAINS
            and content_sim >= 0.50
        ):
            return True
        if (
            b.get('source_domain') in SOCIAL_DOMAINS
            and a.get('source_domain') not in SOCIAL_DOMAINS
            and content_sim >= 0.50
        ):
            return True

    return False


def build_news_candidate(item: dict) -> dict:
    text = ' '.join([
        item.get('title_zh', '') or item.get('title_en', '') or '',
        item.get('summary_zh', '') or item.get('summary_en', '') or '',
        item.get('source', '') or '',
    ])
    canonical_url = canonicalize_url(item.get('url', ''))
    company, product, entity_type = infer_company_product_entity(item, text, canonical_url, is_product=False)
    event_type = infer_event_type(text)
    topic_key, topic_label, topic_caps = infer_topic(text)
    capability_tags = infer_capability_tags(topic_key, topic_caps, text)
    source_kind = infer_source_kind(item, is_product=False)
    published_dt = parse_published_at(item.get('published_at', ''), item.get('published_ts', 0.0))
    historical = is_historical_review(item, source_kind, text, canonical_url)
    date_bucket = published_dt.astimezone(TZ).strftime('%Y-%m-%d')

    candidate = dict(item)
    candidate.update({
        'canonical_url': canonical_url,
        'source_domain': domain_of(canonical_url),
        'company': company,
        'product': product,
        'entity_type': entity_type,
        'event_type': event_type,
        'canonical_topic': topic_key,
        'topic_label': topic_label,
        'capability_tags': capability_tags,
        'source_kind': source_kind,
        'is_from_historical_review': historical,
        'published_dt': published_dt,
        'dedupe_key': '|'.join([
            normalize_name(company),
            normalize_name(product),
            event_type,
            date_bucket,
        ]),
        'topic_cluster_key': topic_key,
        'why_it_matters': trim_summary(item, 120),
    })
    return candidate


def build_product_candidate(item: dict) -> dict:
    text = ' '.join([
        item.get('title_zh', '') or item.get('title_en', '') or '',
        item.get('summary_zh', '') or item.get('summary_en', '') or '',
        item.get('platform', '') or '',
    ])
    canonical_url = canonicalize_url(item.get('url', ''))
    company, product, entity_type = infer_company_product_entity(item, text, canonical_url, is_product=True)
    topic_key, topic_label, topic_caps = infer_topic(text)
    capability_tags = infer_capability_tags(topic_key, topic_caps, text)
    source_kind = infer_source_kind(item, is_product=True)
    published_dt = parse_published_at(item.get('published_at', ''))
    historical = is_historical_review(item, source_kind, text, canonical_url)

    candidate = dict(item)
    candidate.update({
        'canonical_url': canonical_url,
        'source_domain': domain_of(canonical_url),
        'company': company,
        'product': product,
        'entity_type': entity_type,
        'event_type': 'launch',
        'canonical_topic': topic_key,
        'topic_label': topic_label,
        'capability_tags': capability_tags,
        'source_kind': source_kind,
        'is_from_historical_review': historical,
        'published_dt': published_dt,
        'topic_cluster_key': topic_key,
    })
    return candidate


def dedupe_news_candidates(candidates: list[dict]) -> tuple[list[dict], list[dict]]:
    kept: list[dict] = []
    duplicate_meta: list[dict] = []
    for candidate in sorted(candidates, key=candidate_quality, reverse=True):
        matched_index = None
        for idx, existing in enumerate(kept):
            if is_true_duplicate(candidate, existing):
                matched_index = idx
                break
        if matched_index is None:
            kept.append(candidate)
            continue

        existing = kept[matched_index]
        winner = candidate if candidate_quality(candidate) > candidate_quality(existing) else existing
        loser = existing if winner is candidate else candidate
        kept[matched_index] = winner
        duplicate_meta.append({
            'kept_title': winner.get('title_zh') or winner.get('title_en') or '',
            'dropped_title': loser.get('title_zh') or loser.get('title_en') or '',
            'dedupe_key': winner.get('dedupe_key', ''),
            'kept_url': winner.get('canonical_url', ''),
            'dropped_url': loser.get('canonical_url', ''),
        })
    return kept, duplicate_meta


def select_news(candidates: list[dict], max_news: int = 18) -> list[dict]:
    source_groups: dict[str, list[dict]] = defaultdict(list)
    for candidate in candidates:
        source_groups[candidate.get('source', 'unknown')].append(candidate)

    default_cap = 2
    source_caps = {'AI HOT': 3}
    selected: list[dict] = []
    source_picked: dict[str, int] = defaultdict(int)

    def pick_from_source(src: str, cap: int) -> None:
        for candidate in source_groups.get(src, []):
            if len(selected) >= max_news or source_picked[src] >= cap:
                break
            selected.append(candidate)
            source_picked[src] += 1

    def src_weight(src: str) -> int:
        items = source_groups.get(src, [])
        return int(items[0].get('weight', 5)) if items else 0

    all_sources = sorted(source_groups.keys(), key=src_weight, reverse=True)
    for src in all_sources:
        pick_from_source(src, source_caps.get(src, default_cap))

    if len(selected) < max_news:
        for src in all_sources:
            if len(selected) >= max_news:
                break
            if src in source_caps:
                continue
            pick_from_source(src, default_cap + 1)

    return selected[:max_news]


def is_valid_news_candidate(item: dict) -> tuple[bool, str]:
    title = clean_text(item.get('title_zh') or item.get('title_en') or '')
    summary = clean_text(item.get('summary_zh') or item.get('summary_en') or '')
    url = item.get('canonical_url', '') or item.get('url', '')
    lowered = ' '.join([title, summary, url]).lower()

    promo_patterns = [
        'early bird ticket', 'ticket rates', 'register', 'save up to',
        '早鸟票', '通行证', '立即参加', '培训', 'mandatory', 'quiz', '测验',
    ]
    if any(pattern in lowered for pattern in promo_patterns):
        return False, 'promo-or-evergreen'

    return True, 'ok'


def product_summary_fallback(item: dict) -> str:
    summary = trim_summary(item, 100)
    if summary and summary not in {'评论', 'Comments'}:
        return summary

    platform = item.get('platform', '')
    title = item.get('title_zh') or item.get('title_en') or item.get('product') or '该项目'
    fallback_map = {
        'GitHub': f'{title} 是今日值得观察的 GitHub AI 项目，适合用来跟踪开源能力方向与开发者关注度。',
        'Product Hunt': f'{title} 是今日 Product Hunt 上榜产品，可作为新工具与新品类信号观察样本。',
        'Toolify': f'{title} 是一款具体 AI 工具，适合用来观察其目标场景与实际应用价值。',
        'Trustmrr': f'{title} 是 Trustmrr 收录的具体项目，可用于观察其商业化验证与营收表现。',
    }
    return fallback_map.get(platform, f'{title} 是今日值得留意的具体 AI 产品/项目。')


def is_valid_product_candidate(item: dict) -> tuple[bool, str]:
    if item.get('is_from_historical_review'):
        return False, 'historical-review'

    url = item.get('canonical_url', '') or item.get('url', '')
    domain = domain_of(url)
    title = clean_text(item.get('title_zh') or item.get('title_en') or '')
    summary = clean_text(item.get('summary_zh') or item.get('summary_en') or '')
    platform = item.get('platform', '')
    lowered = ' '.join([title, summary, platform, url]).lower()

    if not url:
        return False, 'missing-url'
    if summary in {'评论', 'Comments'}:
        return False, 'comment-only'
    if domain in NEWSY_DOMAINS:
        return False, 'news-article'
    if platform == 'Hacker News' and not any(k in lowered for k in ['github.com', '/tool/', 'product hunt', 'demo', 'app', 'plugin', 'model', 'repo']):
        return False, 'hn-non-product'
    if platform == 'Toolify' and '/tool/' not in url:
        return False, 'toolify-directory'
    if platform == 'GitHub' and 'github.com/' not in url:
        return False, 'github-non-repo'
    if platform == 'Trustmrr' and '/startup/' not in url:
        return False, 'trustmrr-non-startup'
    if re.search(r'(封锁|blocks|licence|license|lawsuit|regulation|监管)', lowered) and domain in NEWSY_DOMAINS | {'news.ycombinator.com'}:
        return False, 'policy-news-not-product'
    return True, 'ok'


# 📝 引语与标签 — 由 Agent（小羽毛早报编辑）在策展层生成
# 脚本层不再生成/检测模板化金句。Agent 选文后自行撰写基于当日内容的编辑手记。
# 1. 加载 candidates
raw_data = json.loads((PROJECT_DIR / 'candidates.json').read_text(encoding='utf-8'))
raw_news = raw_data.get('candidates', [])
raw_products = raw_data.get('product_candidates', [])

# 2. 结构化补全 + 历史污染拦截
news_candidates = [build_news_candidate(item) for item in raw_news]
blocked_historical_news = [item for item in news_candidates if item.get('is_from_historical_review')]
news_candidates = [item for item in news_candidates if not item.get('is_from_historical_review')]

product_candidates = [build_product_candidate(item) for item in raw_products]
blocked_historical_products = [item for item in product_candidates if item.get('is_from_historical_review')]
product_candidates = [item for item in product_candidates if not item.get('is_from_historical_review')]

# 3. URL 预去重（兜底：相同 canonical_url 的精确匹配，防止上游数据异常）
url_dedup_meta: list[dict] = []
url_seen: dict[str, int] = {}
url_filtered: list[dict] = []
for item in news_candidates:
    cu = item.get('canonical_url', '') or ''
    if not cu:
        url_filtered.append(item)
        continue
    if cu in url_seen:
        url_dedup_meta.append({
            'kept_title': (url_filtered[url_seen[cu]].get('title_zh') or url_filtered[url_seen[cu]].get('title_en', '')),
            'dropped_title': (item.get('title_zh') or item.get('title_en', '')),
            'dedupe_key': 'canonical_url',
            'kept_url': cu,
            'dropped_url': cu,
        })
        continue
    url_seen[cu] = len(url_filtered)
    url_filtered.append(item)
news_candidates = url_filtered

# 4. A 类真重复判定（相似度去重）
news_candidates, duplicate_meta_v2 = dedupe_news_candidates(news_candidates)
duplicate_meta = url_dedup_meta + duplicate_meta_v2

# 5. 非新闻/宣传类剔除
filtered_news_candidates: list[dict] = []
news_rejections: list[dict] = []
for item in news_candidates:
    valid, reason = is_valid_news_candidate(item)
    if not valid:
        news_rejections.append({
            'title': item.get('title_zh') or item.get('title_en') or '',
            'url': item.get('canonical_url', '') or item.get('url', ''),
            'reason': reason,
        })
        continue
    filtered_news_candidates.append(item)

# 6. 动态选文
selected_news = select_news(filtered_news_candidates, max_news=18)
cluster_counts = Counter(item.get('topic_cluster_key', 'general-ai') for item in selected_news)

# 7. 新闻输出加工
news_out: list[dict] = []
for item in selected_news:
    capability_tags = item.get('capability_tags', [])[:4]
    tags = classify_tags(item) or ['行业']
    title = trim_title(item)
    summary = trim_summary(item)
    news_out.append({
        'title': title,
        'source': item.get('source', ''),
        'url': item.get('canonical_url', '') or item.get('url', ''),
        'summary': summary,
        'tags': tags,
        'score': item.get('weight', 5),
        'publishedAt': item.get('published_at', ''),
        'company': item.get('company', ''),
        'product': item.get('product', ''),
        'entity_type': item.get('entity_type', 'company'),
        'event_type': item.get('event_type', 'update'),
        'canonical_topic': item.get('canonical_topic', 'general-ai'),
        'capability_tags': capability_tags,
        'source_kind': item.get('source_kind', 'news'),
        'is_from_historical_review': False,
        'dedupe_key': item.get('dedupe_key', ''),
        'topic_cluster_key': item.get('topic_cluster_key', 'general-ai'),
        'topic_label': item.get('topic_label', 'AI 综合观察'),
        'cluster_size': cluster_counts.get(item.get('topic_cluster_key', 'general-ai'), 1),
        'why_it_matters': item.get('why_it_matters') or summary,
    })

# 8. 产品门禁 + 输出加工
news_urls = {
    (item.get('url', '') or '').strip()
    for item in news_out
    if (item.get('url', '') or '').strip()
}
products: list[dict] = []
product_rejections: list[dict] = []
selected_product_urls: set[str] = set()
for item in product_candidates:
    valid, reason = is_valid_product_candidate(item)
    if not valid:
        product_rejections.append({
            'title': item.get('title_zh') or item.get('title_en') or '',
            'url': item.get('canonical_url', '') or item.get('url', ''),
            'reason': reason,
        })
        continue

    url = (item.get('canonical_url', '') or item.get('url', '')).strip()
    if url in news_urls:
        product_rejections.append({
            'title': item.get('title_zh') or item.get('title_en') or '',
            'url': url,
            'reason': 'cross-section-duplicate-with-news',
        })
        continue
    if url in selected_product_urls:
        product_rejections.append({
            'title': item.get('title_zh') or item.get('title_en') or '',
            'url': url,
            'reason': 'duplicate-product-url',
        })
        continue

    summary = product_summary_fallback(item)
    title = clean_text(item.get('title_zh') or item.get('title_en') or item.get('product') or f"{item.get('platform', '')} 今日精选")
    if title in {'理解-任何事情'}:
        title = 'Understand Anything'
    if title in {'迷你CPM5-1B'}:
        title = 'MiniCPM5-1B'

    products.append({
        'title': title,
        'platform': item.get('platform', ''),
        'source': item.get('source', item.get('platform', '')),
        'url': url,
        'summary': summary,
        'tags': classify_tags(item) or ['产品'],
        'score': 5,
        'publishedAt': item.get('published_at', now.isoformat()),
        'company': item.get('company', ''),
        'product': item.get('product', ''),
        'entity_type': item.get('entity_type', 'product'),
        'canonical_topic': item.get('canonical_topic', 'general-ai'),
        'capability_tags': item.get('capability_tags', [])[:4],
        'topic_cluster_key': item.get('topic_cluster_key', 'general-ai'),
        'topic_label': item.get('topic_label', 'AI 综合观察'),
    })
    selected_product_urls.add(url)
    if len(products) >= 5:
        break

# 8.1 第 5 个产品兜底逻辑（放宽门禁但仍排除明显无效项）
fallback_products_added = 0
if len(products) < 5:
    relaxed_reasons = {'hn-non-product', 'toolify-directory', 'github-non-repo', 'trustmrr-non-startup'}

    for item in product_candidates:
        if len(products) >= 5:
            break

        url = (item.get('canonical_url', '') or item.get('url', '')).strip()
        if not url or url in selected_product_urls:
            continue
        if url in news_urls:
            product_rejections.append({
                'title': item.get('title_zh') or item.get('title_en') or '',
                'url': url,
                'reason': 'cross-section-duplicate-with-news',
            })
            continue
        if item.get('is_from_historical_review'):
            continue

        valid, reason = is_valid_product_candidate(item)
        if (not valid) and (reason not in relaxed_reasons):
            continue

        title = clean_text(item.get('title_zh') or item.get('title_en') or item.get('product') or f"{item.get('platform', '')} 今日精选")
        if title in {'理解-任何事情'}:
            title = 'Understand Anything'
        if title in {'迷你CPM5-1B'}:
            title = 'MiniCPM5-1B'

        summary = product_summary_fallback(item)
        products.append({
            'title': title,
            'platform': item.get('platform', ''),
            'source': item.get('source', item.get('platform', '')),
            'url': url,
            'summary': summary,
            'tags': classify_tags(item) or ['产品'],
            'score': 4,
            'publishedAt': item.get('published_at', now.isoformat()),
            'company': item.get('company', ''),
            'product': item.get('product', ''),
            'entity_type': item.get('entity_type', 'product'),
            'canonical_topic': item.get('canonical_topic', 'general-ai'),
            'capability_tags': item.get('capability_tags', [])[:4],
            'topic_cluster_key': item.get('topic_cluster_key', 'general-ai'),
            'topic_label': item.get('topic_label', 'AI 综合观察'),
            'fallback_reason': f'relaxed-gate:{reason}' if not valid else 'relaxed-gate:pass',
        })
        selected_product_urls.add(url)
        fallback_products_added += 1

# 8.2 产品级新闻候选兜底：仅使用实体类型为 product/model 的未入选新闻候选补齐。
# 不允许将普通新闻文章伪装为产品（entity_bonus 过滤 + title 黑名单兜底）。
if len(products) < 5:
    selected_news_urls = {
        (item.get('canonical_url', '') or item.get('url', '')).strip()
        for item in selected_news
        if (item.get('canonical_url', '') or item.get('url', '')).strip()
    }

    eligible_candidates = [
        item for item in filtered_news_candidates
        if item.get('entity_type') in {'product', 'model'}
    ]

    def fallback_rank(item: dict) -> tuple[int, int]:
        non_newsy_bonus = 1 if item.get('source_domain', '') not in NEWSY_DOMAINS else 0
        return (non_newsy_bonus, int(item.get('weight', 0)))

    remaining_news_candidates = sorted(eligible_candidates, key=fallback_rank, reverse=True)

    for item in remaining_news_candidates:
        if len(products) >= 5:
            break

        url = (item.get('canonical_url', '') or item.get('url', '')).strip()
        if not url:
            continue
        if url in selected_news_urls or url in news_urls or url in selected_product_urls:
            continue

        entity_name = clean_text(item.get('product', '') or item.get('company', '') or '')
        if not entity_name:
            continue

        summary = clean_text(item.get('why_it_matters') or trim_summary(item, 100) or f'{entity_name} 是今日值得跟踪的产品化信号。')
        products.append({
            'title': entity_name,
            'platform': item.get('source', 'News Candidate'),
            'source': item.get('source', 'News Candidate'),
            'url': url,
            'summary': summary,
            'tags': classify_tags(item) or ['产品'],
            'score': 3,
            'publishedAt': item.get('published_at', now.isoformat()),
            'company': clean_text(item.get('company', '')),
            'product': entity_name,
            'entity_type': item.get('entity_type', 'product'),
            'canonical_topic': item.get('canonical_topic', 'general-ai'),
            'capability_tags': item.get('capability_tags', [])[:4],
            'topic_cluster_key': item.get('topic_cluster_key', 'general-ai'),
            'topic_label': item.get('topic_label', 'AI 综合观察'),
            'fallback_reason': 'news-candidate-entity-fallback',
        })
        selected_product_urls.add(url)
        fallback_products_added += 1

# 8. 金句与 meta（空占位 — 由 Agent 在策展层生成）
quote = ""
quote_context = {}
source_distribution = Counter(item.get('source', 'unknown') for item in news_out)
cluster_distribution = Counter(item.get('topic_label', 'AI 综合观察') for item in news_out)

output = {
    'date': f'{today_str} 周{weekday}',
    'news': news_out,
    'products': products,
    'quote': quote,
    'quote_context': quote_context,
    'summary': f'今日共 {len(news_out)} 条 AI 新闻 + {len(products)} 个产品 · {raw_data.get("sources_success", 0)}/{raw_data.get("sources_checked", 0)} 源活跃',
    'meta': {
        'generated_at': now.isoformat(),
        'source_stats': raw_data.get('source_stats', {}),
        'rss_sources_total': raw_data.get('sources_checked', 0),
        'rss_sources_success': raw_data.get('sources_success', 0),
        'total_fetched': raw_data.get('total_fetched', 0),
        'unique_news': len(news_out),
        'final_products': len(products),
        'dedup_window_hours': 48,
        'selection_method': 'object-event-dedupe + topic-cluster-preserve',
        'quality_pass': 'historical-block + true-dedupe + product-gate (Agent should still review)',
        'source_distribution': dict(source_distribution),
        'cluster_distribution': dict(cluster_distribution),
        'duplicates_removed': len(duplicate_meta),
        'duplicate_records': duplicate_meta,
        'news_rejections': news_rejections,
        'historical_blocked_news': len(blocked_historical_news),
        'historical_blocked_products': len(blocked_historical_products),
        'product_rejections': product_rejections,
        'fallback_products_added': fallback_products_added,
    },
}

out_path = PROJECT_DIR / 'daily_data.json'
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')

print(f'✅ daily_data.json: {len(news_out)} 新闻 + {len(products)} 产品')
print(f'📊 来源分布: {dict(source_distribution)}')
print(f'🧩 主题分布: {dict(cluster_distribution)}')
print(f'🧹 去重移除: {len(duplicate_meta)}')
print(f'🚫 产品拦截: {len(product_rejections)}')
# 引语由 Agent 在策展层生成
