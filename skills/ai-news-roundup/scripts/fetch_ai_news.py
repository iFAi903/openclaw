#!/usr/bin/env python3
"""
小羽毛 AI 新闻早报 — 数据采集脚本
职责：RSS 抓取 + 产品抓取 + 去重 + Google Translate 初步中文化 → candidates.json
Agent 负责：退化修复 + 标签 + 金句 → daily_data.json

与 fetch_news_final.py 的区别：
- 不做复杂 regex 标题润色（那是 Agent 的活）
- 不做最终 15 选 N（那是 Agent 的活）
- 输出 candidates.json 而非 daily_data.json
"""
from __future__ import annotations

import argparse
import html as html_mod
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Optional
from zoneinfo import ZoneInfo

try:
    import yaml
except Exception:
    yaml = None

# ── SSL ──────────────────────────────────────────

def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass
    # macOS fallback: try system certs
    for path in ['/etc/ssl/cert.pem', '/usr/local/etc/openssl@3/cert.pem']:
        if os.path.isfile(path):
            return ssl.create_default_context(cafile=path)
    return ssl.create_default_context()

_SSL = _ssl_context()

# ── 常量 ──────────────────────────────────────────

TIMEZONE = ZoneInfo('Asia/Taipei')
UTZ = timezone.utc
PROJECT_DIR = Path(__file__).resolve().parents[1]
BACKUP_DIR = PROJECT_DIR / 'backups'
CURL_TIMEOUT = 4
TRANSLATE_TIMEOUT = 1.5
TRANSLATE_MAX_LENGTH = 500
RECENT_DEDUP_DAYS = 3
MAX_ITEMS_PER_SOURCE = 10

# Atom / RSS namespace
ATOM_NS = '{http://www.w3.org/2005/Atom}'
MEDIA_NS = '{http://search.yahoo.com/mrss/}'


def now_taipei() -> datetime:
    return datetime.now(TIMEZONE)


def contains_chinese(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text or ''))


def clean_html(text: str) -> str:
    if not text:
        return ''
    text = re.sub(r'<script[\s\S]*?</script>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<style[\s\S]*?</style>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '。', text, flags=re.IGNORECASE)
    text = re.sub(r'</p\s*>', '。', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html_mod.unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip(' \t\r\n-—|')


def normalize_key(text: str) -> str:
    text = (text or '').strip().lower()
    text = re.sub(r'https?://', '', text)
    text = re.sub(r'www\.', '', text)
    text = re.sub(r'[^\w\u4e00-\u9fff]+', '', text)
    return text


def jaccard(a: str, b: str) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def similar(a: str, b: str) -> bool:
    na, nb = normalize_key(a), normalize_key(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    if na in nb or nb in na:
        return min(len(na), len(nb)) >= 12
    return jaccard(na, nb) >= 0.84


def trim_title(text: str, max_len: int = 48) -> str:
    text = re.sub(r'\s+', ' ', text).strip(' 。.-—|')
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rfind(' ')
    if cut >= max_len * 0.6:
        return text[:cut].strip()
    for sep in ['，', '、', ',', '｜', '：']:
        cut = text[:max_len].rfind(sep)
        if cut >= max_len * 0.5:
            return text[:cut].strip()
    return text[:max_len].strip()


def parse_timestamp(value: str) -> float:
    if not value:
        return 0.0
    for parser in (
        lambda v: parsedate_to_datetime(v).timestamp(),
        lambda v: datetime.strptime(v, '%Y-%m-%dT%H:%M:%S%z').timestamp(),
        lambda v: datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ').timestamp(),
        lambda v: datetime.strptime(v, '%Y-%m-%d %H:%M:%S').timestamp(),
    ):
        try:
            return parser(value)
        except Exception:
            pass
    return 0.0


# ── HTTP 抓取 ─────────────────────────────────────

def fetch_url(url: str, timeout: int = CURL_TIMEOUT) -> str:
    """curl 抓取，如果失败不重复尝试 urllib，防止双重超时"""
    try:
        result = subprocess.run(
            ['curl', '-sL', '-A', 'Mozilla/5.0 (compatible; XiaoYuMaoNewsBot/3.0)',
             '--max-time', str(timeout), url],
            capture_output=True, text=True, timeout=timeout + 3, check=False,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except FileNotFoundError:
        # 只有在没有 curl 时才使用 urllib 备用
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=timeout, context=_SSL) as resp:
                return resp.read().decode('utf-8', errors='ignore')
        except Exception:
            pass
    except Exception:
        pass
    return ''


# ── Google Translate ─────────────────────────────

TRANSLATION_CACHE: dict[str, str] = {}
USE_NETWORK_TRANSLATE = os.getenv('AI_NEWS_NETWORK_TRANSLATE', '1').lower() not in {'0', 'false', 'no'}
CONSECUTIVE_TRANSLATE_FAILURES = 0

# 短语回退映射（Google Translate 失败时使用）
PHRASE_MAP = [
    ('data center', '数据中心'), ('open source', '开源'), ('open-source', '开源'),
    ('reasoning model', '推理模型'), ('vision model', '视觉模型'),
    ('launches', '发布'), ('launch', '发布'), ('releases', '发布'), ('release', '发布'),
    ('unveils', '发布'), ('unveil', '发布'), ('adds', '新增'), ('acquires', '收购'),
    ('partners with', '联手'), ('raises', '完成融资'), ('pauses', '暂停'),
    ('executive shuffle', '高层调整'), ('report', '报告'), ('model', '模型'),
    ('agentic', '智能体驱动'), ('agents', '智能体'), ('agent', '智能体'), ('benchmark', '基准'),
    ('tool use', '工具调用'), ('private markets', '私募市场'),
    ('video', '视频'), ('videos', '视频'), ('superintelligence', '超级智能'),
    ('token tax', 'Token 成本'), ('gas plant', '燃气电厂'),
    ('behavioral economics', '行为经济学'), ('borderless business', '跨境业务'),
    ('preview tool', '预览工具'), ('makers', '创作者'), ('visualize', '可视化'),
]


def translate_to_chinese(text: str) -> str:
    """Google Translate API + 短语回退"""
    global USE_NETWORK_TRANSLATE, CONSECUTIVE_TRANSLATE_FAILURES
    if not text or contains_chinese(text):
        return text or ''
    key = text[:120]
    if key in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[key]

    result = text
    # Network translation ON by default (5s timeout, 500 char max per item).
    # Agent quality pass still reviews/improves final output.
    if USE_NETWORK_TRANSLATE:
        try:
            url = (
                'https://translate.googleapis.com/translate_a/single'
                '?client=gtx&sl=auto&tl=zh-CN&dt=t&q=' +
                urllib.parse.quote(text[:TRANSLATE_MAX_LENGTH])
            )
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=TRANSLATE_TIMEOUT, context=_SSL) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            if data and data[0]:
                translated = ''.join(part[0] for part in data[0] if part and part[0])
                if translated:
                    result = re.sub(r'\s+', ' ', translated).strip()
            CONSECUTIVE_TRANSLATE_FAILURES = 0  # 成功，重置计数器
        except Exception as e:
            CONSECUTIVE_TRANSLATE_FAILURES += 1
            if CONSECUTIVE_TRANSLATE_FAILURES >= 3:
                print(f"[WARN] Google 翻译连续失败 {CONSECUTIVE_TRANSLATE_FAILURES} 次，触发熔断。关闭后续网络翻译。原因: {e}")
                USE_NETWORK_TRANSLATE = False

    # 短语回退
    if not contains_chinese(result):
        localized = text
        for en, zh in PHRASE_MAP:
            localized = re.sub(en, zh, localized, flags=re.IGNORECASE)
        localized = re.sub(r'\s+', ' ', localized).strip()
        if contains_chinese(localized):
            result = localized

    TRANSLATION_CACHE[key] = result
    return result


# ── RSS 解析 ─────────────────────────────────────

@dataclass
class CandidateItem:
    title_en: str
    title_zh: str
    source: str
    url: str
    summary_en: str
    summary_zh: str
    published_at: str
    published_ts: float
    weight: int
    must_keep: bool = False


def parse_rss(xml_content: str, source_name: str, weight: int, must_keep: bool,
               cutoff: datetime) -> list[CandidateItem]:
    """解析 RSS 2.0 / Atom feed，返回 24h 内条目"""
    if not xml_content:
        return []
    items: list[CandidateItem] = []
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return []

    # 尝试 Atom (如 Product Hunt, Google Research)
    for entry in root.findall(f'{ATOM_NS}entry'):
        title_elem = entry.find(f'{ATOM_NS}title')
        link_elem = entry.find(f'{ATOM_NS}link')
        summary_elem = entry.find(f'{ATOM_NS}summary')
        if summary_elem is None:
            summary_elem = entry.find(f'{ATOM_NS}content')
        published_elem = entry.find(f'{ATOM_NS}published')
        if published_elem is None:
            published_elem = entry.find(f'{ATOM_NS}updated')
        if title_elem is None:
            continue
        title_en = clean_html(''.join(title_elem.itertext()) if title_elem.text else '')
        url = link_elem.get('href', '').strip() if link_elem is not None else ''
        if not title_en or not url:
            continue
        published_raw = ''.join(published_elem.itertext()) if published_elem is not None else ''
        published_dt = parse_timestamp(published_raw)
        if published_dt > 0:
            pub_dt = datetime.fromtimestamp(published_dt, tz=UTZ)
        else:
            pub_dt = now_taipei()
        if pub_dt < cutoff:
            continue
        summary_en = clean_html(''.join(summary_elem.itertext())[:600]) if summary_elem is not None else ''
        title_zh = translate_to_chinese(title_en)
        summary_zh = translate_to_chinese(summary_en[:300]) if summary_en else ''
        items.append(CandidateItem(
            title_en=title_en, title_zh=title_zh or title_en,
            source=source_name, url=url,
            summary_en=summary_en, summary_zh=summary_zh or summary_en,
            published_at=published_raw, published_ts=published_dt,
            weight=weight, must_keep=must_keep,
        ))

    # 同源内部 URL 去重（防止部分 RSS 同时输出 Atom entry + RSS item）
    seen_urls_in_source: set[str] = set()
    deduped_items: list[CandidateItem] = []
    for item in items:
        if item.url in seen_urls_in_source:
            continue
        seen_urls_in_source.add(item.url)
        deduped_items.append(item)
    items = deduped_items

    # 尝试 RSS 2.0 channel/item
    channel = root.find('channel')
    if channel is not None:
        for item_xml in channel.findall('item'):
            title_elem = item_xml.find('title')
            link_elem = item_xml.find('link')
            desc_elem = item_xml.find('description')
            pubdate_elem = item_xml.find('pubDate')
            if title_elem is None or link_elem is None:
                continue
            title_en = clean_html(title_elem.text or '')
            url = (link_elem.text or '').strip()
            if not title_en or not url:
                continue
            pubdate_raw = pubdate_elem.text if pubdate_elem is not None else ''
            published_ts = parse_timestamp(pubdate_raw)
            if published_ts > 0:
                pub_dt = datetime.fromtimestamp(published_ts, tz=UTZ)
            else:
                pub_dt = now_taipei()
            if pub_dt < cutoff:
                continue
            summary_en = clean_html((desc_elem.text or '')[:600]) if desc_elem is not None else ''
            title_zh = translate_to_chinese(title_en)
            summary_zh = translate_to_chinese(summary_en[:300]) if summary_en else ''
            items.append(CandidateItem(
                title_en=title_en, title_zh=title_zh or title_en,
                source=source_name, url=url,
                summary_en=summary_en, summary_zh=summary_zh or summary_en,
                published_at=pubdate_raw, published_ts=published_ts,
                weight=weight, must_keep=must_keep,
            ))

    # 最终同源 URL 去重（合并 Atom + RSS 双解析后的重复）
    final_seen: set[str] = set()
    final_items: list[CandidateItem] = []
    for item in items:
        if item.url in final_seen:
            continue
        final_seen.add(item.url)
        final_items.append(item)
    return final_items[:MAX_ITEMS_PER_SOURCE]


# ── 去重 ─────────────────────────────────────────

def load_recent_history(days: int = RECENT_DEDUP_DAYS) -> dict[str, set[str] | list[str]]:
    """加载最近 N 天 daily_data.json 中的 URL 和标题"""
    history_urls: set[str] = set()
    history_titles: list[str] = []
    if not BACKUP_DIR.exists():
        return {'urls': history_urls, 'titles': history_titles}
    files = sorted(BACKUP_DIR.glob('*/daily_data.json'), reverse=True)[:days]
    for f in files:
        try:
            data = json.loads(f.read_text(encoding='utf-8'))
        except Exception:
            continue
        for item in data.get('news', []):
            if item.get('url'):
                history_urls.add(item['url'].strip())
            if item.get('title'):
                history_titles.append(item['title'].strip())
        for item in data.get('products', []):
            if item.get('url'):
                history_urls.add(item['url'].strip())
            if item.get('title'):
                history_titles.append(item['title'].strip())
    return {'urls': history_urls, 'titles': history_titles}


def dedup_candidates(items: list[CandidateItem], history: dict) -> list[CandidateItem]:
    """URL 去重 + 标题 Jaccard 相似度去重"""
    history_urls: set[str] = history.get('urls', set())  # type: ignore[assignment]
    history_titles: list[str] = history.get('titles', [])  # type: ignore[assignment]
    seen_urls: set[str] = set()
    seen_titles: list[str] = []
    result: list[CandidateItem] = []

    for item in items:
        if item.url in history_urls or item.url in seen_urls:
            continue
        if any(similar(item.title_zh, t) for t in history_titles):
            continue
        if any(similar(item.title_zh, t) for t in seen_titles):
            continue
        seen_urls.add(item.url)
        seen_titles.append(item.title_zh)
        result.append(item)

    return result


# ── 产品抓取 ─────────────────────────────────────

def product_candidate(platform: str, name: str, url: str, desc: str,
                      reason: str = '') -> CandidateItem:
    """构造产品候选条目"""
    title_zh = translate_to_chinese(name)
    summary_zh = translate_to_chinese(desc[:300]) if desc else ''
    now = now_taipei()
    return CandidateItem(
        title_en=name, title_zh=title_zh or name,
        source=platform, url=url,
        summary_en=desc, summary_zh=summary_zh or desc,
        published_at=now.isoformat(), published_ts=now.timestamp(),
        weight=5, must_keep=False,
    )


def fetch_producthunt() -> Optional[CandidateItem]:
    """Product Hunt RSS → 首条产品"""
    xml_content = fetch_url('https://www.producthunt.com/feed')
    if not xml_content:
        return product_candidate('Product Hunt', 'Product Hunt 今日精选',
                                 'https://www.producthunt.com/', '',
                                 'Product Hunt feed 抓取失败')
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return product_candidate('Product Hunt', 'Product Hunt 今日精选',
                                 'https://www.producthunt.com/', '',
                                 'Product Hunt feed 解析失败')
    for entry in root.findall(f'{ATOM_NS}entry'):
        title_elem = entry.find(f'{ATOM_NS}title')
        link_elem = entry.find(f'{ATOM_NS}link')
        content_elem = entry.find(f'{ATOM_NS}content')
        if title_elem is None or link_elem is None:
            continue
        name = clean_html(''.join(title_elem.itertext()))
        url = link_elem.get('href', '').strip()
        desc = clean_html(''.join(content_elem.itertext())) if content_elem is not None else ''
        if name and url:
            return product_candidate('Product Hunt', name, url, desc,
                                     'Product Hunt 今日首屏产品')
    return product_candidate('Product Hunt', 'Product Hunt 今日精选',
                             'https://www.producthunt.com/', '',
                             'Product Hunt 未命中有效条目')


def fetch_github_trending() -> Optional[CandidateItem]:
    """GitHub Trending → 首个 AI 相关项目"""
    html_doc = fetch_url('https://github.com/trending?since=daily')
    if not html_doc:
        return product_candidate('GitHub', 'GitHub Trending',
                                 'https://github.com/trending', '',
                                 'GitHub Trending 抓取失败')
    blocks = re.findall(r'<article class="Box-row[\s\S]*?</article>', html_doc)
    for block in blocks:
        title_match = re.search(r'href="/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"', block)
        desc_match = re.search(r'<p class="col-9 color-fg-muted my-1 pr-4">([\s\S]*?)</p>', block)
        if not title_match:
            continue
        repo = title_match.group(1).replace(' ', '')
        if repo.startswith('sponsors/'):
            continue
        if not re.search(r'(ai|llm|agent|gpt|rag|model|diffusion|vision|mcp)', block, re.IGNORECASE):
            continue
        desc = clean_html(desc_match.group(1)) if desc_match else ''
        name = repo.split('/')[-1]
        return product_candidate('GitHub', name, f'https://github.com/{repo}', desc,
                                 'GitHub Trending AI 项目')
    return product_candidate('GitHub', 'GitHub Trending',
                             'https://github.com/trending', '',
                             'GitHub Trending 未命中 AI 项目')


def fetch_toolify() -> Optional[CandidateItem]:
    """Toolify → 抓取具体工具，而不是目录页/集合页"""
    for url in ['https://www.toolify.ai/new-ai-tools', 'https://www.toolify.ai/']:
        html_doc = fetch_url(url)
        if not html_doc:
            continue
        if 'Just a moment' in html_doc[:1000]:
            continue

        # Toolify 首页卡片：必须命中 /tool/{slug} 详情页、工具名与工具描述。
        # 禁止把 /new-ai-tools 或首页 title 当成产品候选。
        blocks = re.finditer(
            r'<div data-handle="[^"]+"[\s\S]*?(?=<div data-handle=|$)', html_doc)
        for match in blocks:
            block = match.group(0)
            link_match = re.search(r'href="(/tool/[^"?#]+)', block)
            name_match = re.search(
                r'class="[^"]*tool-name[^"]*"[^>]*>([\s\S]*?)</div>', block)
            desc_match = re.search(
                r'class="[^"]*tool-desc[^"]*"[^>]*>([\s\S]*?)</div>', block)
            if not (link_match and name_match and desc_match):
                continue
            name = clean_html(name_match.group(1))
            desc = clean_html(desc_match.group(1))
            if not name or not desc:
                continue
            tool_url = 'https://www.toolify.ai' + link_match.group(1)
            return product_candidate('Toolify', name, tool_url, desc,
                                     'Toolify 具体工具卡片')
    return None

def fetch_hackernews() -> Optional[CandidateItem]:
    """Hacker News RSS → 首个 AI 条目"""
    xml_content = fetch_url('https://news.ycombinator.com/rss')
    if not xml_content:
        return product_candidate('Hacker News', 'Hacker News 今日热议',
                                 'https://news.ycombinator.com/', '',
                                 'Hacker News RSS 抓取失败')
    items = parse_rss(xml_content, 'Hacker News', 5, False,
                      now_taipei() - timedelta(hours=24))
    for item in items:
        haystack = f'{item.title_en} {item.summary_en}'.lower()
        if re.search(r'(ai|agent|llm|model|gpt|openai|anthropic|tool)', haystack):
            item.source = 'Hacker News'
            return item
    return product_candidate('Hacker News', 'Hacker News 今日热议',
                             'https://news.ycombinator.com/', '',
                             'Hacker News 未命中 AI 讨论项')


def fetch_trustmrr() -> Optional[CandidateItem]:
    """Trustmrr OpenClaw 专题页 → 抓取具体 startup，而不是专题集合页"""
    url = 'https://trustmrr.com/special-category/openclaw'
    html_doc = fetch_url(url)
    if not html_doc:
        return None
    items = re.findall(
        r'\{"@type":"ListItem","position":\d+,"url":"(https://trustmrr.com/startup/.*?)","name":"(.*?)"\}',
        html_doc)
    if items:
        item_url, name = items[0]
        name = clean_html(name)
        startup_html = fetch_url(item_url)
        desc = ''
        for pattern in [
            r'<meta name="description" content="([^"]+)"',
            r'<meta property="og:description" content="([^"]+)"',
        ]:
            desc_match = re.search(pattern, startup_html, re.IGNORECASE)
            if desc_match:
                desc = clean_html(desc_match.group(1))
                break
        if not desc:
            desc = f'{name} 是 Trustmrr 收录的 OpenClaw 生态具体项目，可用于观察该项目的收入验证、利润率与商业化进展。'
        return product_candidate('Trustmrr', name, item_url, desc,
                                 'Trustmrr 专题页项目')
    return None


PRODUCT_FETCHERS = {
    'Product Hunt': fetch_producthunt,
    'GitHub': fetch_github_trending,
    'Toolify': fetch_toolify,
    'Hacker News': fetch_hackernews,
    'Trustmrr': fetch_trustmrr,
}


# ── 主流程 ───────────────────────────────────────

def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f'config not found: {path}')
    text = path.read_text(encoding='utf-8')
    
    try:
        import yaml
        return yaml.safe_load(text) or {}
    except Exception:
        pass
        
    # Fallback to simple YAML line parser
    config = {}
    current_list = None
    current_dict = None
    
    for line in text.splitlines():
        line_clean = line.split('#')[0].strip()
        if not line_clean:
            continue
            
        indent = len(line) - len(line.lstrip())
        
        if line_clean.startswith('-'):
            item_val = line_clean[1:].strip()
            if (item_val.startswith('"') and item_val.endswith('"')) or (item_val.startswith("'") and item_val.endswith("'")):
                item_val = item_val[1:-1]
                
            if current_list is not None:
                if ':' in item_val:
                    k, v = item_val.split(':', 1)
                    k, v = k.strip(), v.strip()
                    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                        v = v[1:-1]
                    if v == 'true': v = True
                    elif v == 'false': v = False
                    else:
                        try: v = int(v)
                        except: pass
                    current_dict = {k: v}
                    current_list.append(current_dict)
                else:
                    current_list.append(item_val)
            continue
            
        if ':' in line_clean:
            k, v = line_clean.split(':', 1)
            k, v = k.strip(), v.strip()
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                v = v[1:-1]
                
            if v == 'true': v = True
            elif v == 'false': v = False
            else:
                try: v = int(v)
                except: pass
                
            if indent > 2 and current_dict is not None and current_list is not None:
                current_dict[k] = v
                continue
                
            if not v:
                if k in ('rss_sources', 'product_platforms', 'degraded_title_patterns', 'degraded_summary_patterns', 'tag_categories'):
                    current_list = []
                    if indent > 0 and 'quality' in config:
                        config['quality'][k] = current_list
                    else:
                        config[k] = current_list
                    current_dict = None
                else:
                    current_dict = {}
                    config[k] = current_dict
                    current_list = None
            else:
                if current_dict is not None and indent > 0:
                    current_dict[k] = v
                else:
                    config[k] = v
                    
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description='小羽毛 AI 新闻早报 — 数据采集')
    parser.add_argument('--config', default=str(PROJECT_DIR / 'config.yaml'))
    parser.add_argument('--json', action='store_true', help='仅输出 JSON')
    args = parser.parse_args()

    config_path = Path(args.config).expanduser()
    try:
        cfg = load_config(config_path)
    except Exception as e:
        print(json.dumps({'ok': False, 'action': 'config_error', 'message': str(e)},
                         ensure_ascii=False, indent=2))
        return 2

    profile = cfg.get('profile', {})
    lookback_hours = int(profile.get('lookback_hours', 24))
    cutoff = datetime.now(UTZ) - timedelta(hours=lookback_hours)
    sources = cfg.get('rss_sources', [])
    platforms = cfg.get('product_platforms', [])

    # ── 1. RSS 抓取 ──
    if not args.json:
        print('=' * 60)
        print(f'小羽毛 AI 新闻早报 — 采集 {now_taipei().strftime("%Y-%m-%d %H:%M")}')
        print('=' * 60)

    all_candidates: list[CandidateItem] = []
    source_stats: dict[str, int] = {}
    errors: list[dict] = []

    for src in sources:
        name = src.get('name', 'unknown')
        url = src.get('url', '')
        weight = int(src.get('weight', 5))
        must_keep = bool(src.get('must_keep', False))
        try:
            xml_content = fetch_url(url)
            items = parse_rss(xml_content, name, weight, must_keep, cutoff)
            source_stats[name] = len(items)
            all_candidates.extend(items)
            if not args.json:
                print(f'  📡 {name:<18} {len(items):>2} 条')
        except Exception as e:
            source_stats[name] = 0
            errors.append({'source': name, 'error': str(e)})
            if not args.json:
                print(f'  ❌ {name:<18} 失败: {e}')

    # ── 2. 去重 ──
    history = load_recent_history()
    deduped = dedup_candidates(all_candidates, history)

    # ── 3. 产品抓取 ──
    product_items: list[dict] = []
    for platform in platforms:
        fetcher = PRODUCT_FETCHERS.get(platform)
        if not fetcher:
            continue
        try:
            item = fetcher()
            if item:
                product_items.append({
                    'title_en': item.title_en,
                    'title_zh': item.title_zh,
                    'platform': platform,
                    'source': item.source,
                    'url': item.url,
                    'summary_en': item.summary_en,
                    'summary_zh': item.summary_zh,
                    'published_at': item.published_at,
                })
                if not args.json:
                    print(f'  🛍️  {platform:<18} {item.title_en[:40]}')
        except Exception as e:
            errors.append({'platform': platform, 'error': str(e)})
            if not args.json:
                print(f'  ❌ {platform:<18} 失败: {e}')

    # ── 4. 排序 ──
    deduped.sort(key=lambda x: (x.weight, x.published_ts), reverse=True)

    # ── 5. 输出 candidates.json ──
    output = {
        'ok': len(errors) == 0,
        'action': 'digest' if deduped else ('errors' if errors else 'none'),
        'date': now_taipei().strftime('%Y年%m月%d日'),
        'weekday': '一二三四五六日'[now_taipei().weekday()],
        'lookback_hours': lookback_hours,
        'sources_checked': len(sources),
        'sources_success': sum(1 for v in source_stats.values() if v > 0),
        'total_fetched': len(all_candidates),
        'unique_after_dedup': len(deduped),
        'source_stats': source_stats,
        'candidates': [asdict(item) for item in deduped],
        'product_candidates': product_items,
        'errors': errors,
        'generated_at': now_taipei().isoformat(),
    }

    output_path = PROJECT_DIR / 'candidates.json'
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')

    if not args.json:
        print('-' * 60)
        print(f'✅ candidates.json: {len(deduped)} 新闻候选 + {len(product_items)} 产品候选')
        print(f'   源成功率: {output["sources_success"]}/{output["sources_checked"]}')
        if errors:
            print(f'   ⚠️  错误: {len(errors)} 个')
        print(f'   → {output_path}')

    return 0 if len(errors) == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
