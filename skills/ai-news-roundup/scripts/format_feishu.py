#!/usr/bin/env python3
"""将 daily_data.json 格式化为飞书纯文本消息。

v2.0 (2026-07-06) — 结构优化版
  - 去除冗余 diff_line（平台前缀噪音）
  - 结构化呈现：编号+标签+标题 → 出处 → 摘要 → 链接
  - 当日洞察标签明确，暗示需要真正洞见
  - 底层 URL 去重（兜底上游 pipeline 偶发重复）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]


def dedup_news(items: list[dict]) -> list[dict]:
    """基于 url 去重，保留首次出现的条目。"""
    seen: set[str] = set()
    result: list[dict] = []
    for item in items:
        url = item.get("url", "")
        if url and url in seen:
            continue
        if url:
            seen.add(url)
        result.append(item)
    return result


def format_news_item(item: dict, idx: int) -> list[str]:
    """生成单条新闻的结构化文本块。"""
    lines: list[str] = []

    # 编号 + 标签（分类） + 标题
    tags = item.get("tags", [])
    tags_str = "·".join(tags[:3]) if tags else "综合"
    title = (item.get("title") or "").strip()
    lines.append(f"{idx}️⃣ 【{tags_str}】{title}")

    # 出处（来源名）
    source = (item.get("source") or "").strip()
    if source:
        lines.append(f"📰 出处：{source}")

    # 摘要
    summary = (item.get("summary") or "").strip()
    if summary:
        lines.append(f"📝 {summary}")

    # 原文链接
    url = (item.get("url") or "").strip()
    if url:
        lines.append(f"🔗 [查看原文]({url})")

    return lines


def format_product_item(item: dict) -> list[str]:
    """生成单条产品的结构化文本块。"""
    lines: list[str] = []

    title = (item.get("title") or "").strip()
    platform = (item.get("platform") or "").strip()
    if platform and platform not in title:
        lines.append(f"  {title} ｜ {platform}")
    else:
        lines.append(f"  {title}")

    summary = (item.get("summary") or "").strip()
    if summary:
        lines.append(f"  {summary}")

    url = (item.get("url") or "").strip()
    if url:
        lines.append(f"  🔗 [查看原文]({url})")

    return lines


def main() -> int:
    daily_path = PROJECT_DIR / "daily_data.json"
    if not daily_path.exists():
        print(
            "❌ daily_data.json 不存在，请先运行 build_daily_data.py",
            file=sys.stderr,
        )
        return 1

    data = json.loads(daily_path.read_text(encoding="utf-8"))
    news = data.get("news", [])
    products = data.get("products", [])
    quote = data.get("quote", "")
    date = data.get("date", "")

    # 底层去重（上游 pipeline 偶有重复条目）
    news = dedup_news(news)

    lines: list[str] = []

    # ── 标题 ──
    lines.append(f"🪶 小羽毛 AI 新闻早报 ｜ {date}")
    lines.append("")

    # ── 当日洞察（金句） ──
    if quote and quote.strip():
        lines.append("💬 今日洞察")
        lines.append(f"  {quote.strip()}")
        lines.append("")

    # ── AI 新闻 ──
    lines.append("━━━ 📰 AI 新闻 ━━━")
    for i, item in enumerate(news, 1):
        lines.extend(format_news_item(item, i))
        lines.append("")

    # ── 产品雷达 ──
    lines.append("━━━ 🛍️ 产品雷达 ━━━")
    for item in products:
        lines.extend(format_product_item(item))
        lines.append("")

    # ── 底部统计 ──
    lines.append("━━━")
    meta = data.get("meta", {})
    sources_success = meta.get("rss_sources_success", 0)
    sources_total = meta.get("rss_sources_total", 0)
    lines.append(f"⚡ {len(news)} 条新闻 + {len(products)} 产品 · AI 天团自动巡检")

    # 仅在异常时显示详细信息
    if sources_total > 0 and sources_success < sources_total:
        lines.append(f"⚠️ 源覆盖率：{sources_success}/{sources_total}")

    output = "\n".join(lines)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
