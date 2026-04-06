#!/usr/bin/env python3
"""人物复刻 Skill 文件管理器。"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def skill_dir(base_dir: str, slug: str) -> str:
    return os.path.join(base_dir, slug)


def init_replica(base_dir: str, slug: str, name: str) -> None:
    root = skill_dir(base_dir, slug)
    ensure_dir(root)
    ensure_dir(os.path.join(root, "versions"))

    meta = {
        "slug": slug,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "version": "v1",
        "source_policy": "user-uploaded + public-web only",
        "confidence": "draft"
    }

    files = {
        "meta.json": json.dumps(meta, ensure_ascii=False, indent=2),
        "profile.md": f"# {name} — Profile\n\n- 一句话定义：\n- 角色标签：\n- 主要领域：\n- 资料覆盖时间段：\n- 资料充分度：\n",
        "mindset.md": f"# {name} — Mindset\n\n## Thinking Model\n\n## Action Logic\n\n## Communication Style\n\n## Heuristics\n\n## Boundaries\n",
        "source-ledger.md": f"# {name} — Source Ledger\n\n| 类型 | 标题 | 链接/文件 | 时间 | 可靠性 | 用途 |\n|---|---|---|---|---|---|\n",
        "notes.md": f"# {name} — Notes\n\n## 待验证\n\n## 来源冲突\n\n## 后续补充\n",
    }

    for filename, content in files.items():
        path = os.path.join(root, filename)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    print(f"✅ 已初始化：{root}")


def combine_replica(base_dir: str, slug: str) -> None:
    root = skill_dir(base_dir, slug)
    meta_path = os.path.join(root, "meta.json")
    if not os.path.exists(meta_path):
        print(f"错误：未找到 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    def read_or_empty(name: str) -> str:
        path = os.path.join(root, name)
        if not os.path.exists(path):
            return ""
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read().strip()

    name = meta.get("name", slug)
    profile = read_or_empty("profile.md")
    mindset = read_or_empty("mindset.md")
    ledger = read_or_empty("source-ledger.md")
    notes = read_or_empty("notes.md")

    skill_md = f"""---
name: {slug}
description: {name} 的近似人物复刻模型。用于参考其思维方式、行事逻辑、表达偏好与判断框架，帮助分析问题与生成借鉴性意见；不是本人，也不是事实保证。
---

# {name}

你是一个**基于有限资料构建的人物复刻模型**。
目标不是冒充真人，而是在分析问题时尽量贴近此人的思维习惯、判断框架与表达风格。

## 使用边界

- 你不是本人
- 你不拥有未提供的私密信息
- 当证据不足时，明确说“不确定”或给出多个可能
- 优先提供“可借鉴的分析”，不要装作拥有绝对权威

## 人物档案

{profile}

## 思维与表达模型

{mindset}

## 来源账本

{ledger}

## 不确定性与备注

{notes}

## 回答规则

1. 先复述你会如何定义这个问题。
2. 再说明你会优先看哪些变量。
3. 明确给出你的判断路径，而不只是结论。
4. 如果资料不足，显式标注不确定性。
5. 遇到高风险主题（医疗、法律、投资、人身安全），只做思路参考，不给确定性专业建议。
"""

    with open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)

    meta["updated_at"] = datetime.now().isoformat()
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成：{os.path.join(root, 'SKILL.md')}")


def create_replica(base_dir: str, slug: str, name: str) -> None:
    init_replica(base_dir, slug, name)
    combine_replica(base_dir, slug)


def list_replicas(base_dir: str) -> None:
    if not os.path.isdir(base_dir):
        print("还没有任何人物复刻对象。")
        return

    found = []
    for item in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, item, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            found.append((item, meta.get("name", item), meta.get("updated_at", "")))

    if not found:
        print("还没有任何人物复刻对象。")
        return

    for slug, name, updated_at in found:
        date = updated_at[:10] if updated_at else "?"
        print(f"/{slug}  —  {name} · 更新于 {date}")


def main() -> None:
    parser = argparse.ArgumentParser(description="人物复刻 Skill 文件管理器")
    parser.add_argument("action", choices=["init", "combine", "create", "list"])
    parser.add_argument("--base-dir", default="./.claude/skills/replicas")
    parser.add_argument("--slug")
    parser.add_argument("--name")
    args = parser.parse_args()

    if args.action == "list":
        list_replicas(args.base_dir)
        return

    if not args.slug:
        print("错误：需要 --slug", file=sys.stderr)
        sys.exit(1)

    if args.action in {"init", "create"} and not args.name:
        print("错误：需要 --name", file=sys.stderr)
        sys.exit(1)

    if args.action == "init":
        init_replica(args.base_dir, args.slug, args.name)
    elif args.action == "combine":
        combine_replica(args.base_dir, args.slug)
    elif args.action == "create":
        create_replica(args.base_dir, args.slug, args.name)


if __name__ == "__main__":
    main()
