#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import re

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
REPORT_PATH = ROOT / "reports" / "memory-integrity-latest.md"
TARGET_AGENTS = ["product-agent", "cfo", "cro", "coo", "cto"]
REQUIRED_SECTIONS = [
    "角色定义",
    "职责边界",
    "记忆回流规则",
    "核心",
    "决策",
    "输出",
]
ALIGNMENT_PATTERNS = [
    r"遵守.+MEMORY\.md",
    r"服从.+MEMORY\.md",
    r"Alignment.+MEMORY\.md",
    r"根目录.+MEMORY\.md",
]


@dataclass
class AgentAudit:
    name: str
    memory_path: Path
    p0_pass: bool
    p0_issues: list[str]
    p1_notes: list[str]


def has_alignment(text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.DOTALL) for pattern in ALIGNMENT_PATTERNS)


def has_required_sections(text: str) -> list[str]:
    missing = []
    for key in REQUIRED_SECTIONS:
        if key not in text:
            missing.append(key)
    return missing


def audit_agent(agent_name: str) -> AgentAudit:
    agent_dir = AGENTS_DIR / agent_name
    memory_path = agent_dir / "MEMORY.md"
    p0_issues: list[str] = []
    p1_notes: list[str] = []

    if not memory_path.exists():
        p0_issues.append("缺少 MEMORY.md")
        return AgentAudit(agent_name, memory_path, False, p0_issues, p1_notes)

    text = memory_path.read_text(encoding="utf-8").strip()
    if not text:
        p0_issues.append("MEMORY.md 为空")
        return AgentAudit(agent_name, memory_path, False, p0_issues, p1_notes)

    if not has_alignment(text):
        p0_issues.append("缺少对根 MEMORY.md 的对齐/服从声明")

    missing_sections = has_required_sections(text)
    if missing_sections:
        p0_issues.append("缺少核心模块: " + ", ".join(missing_sections))

    for extra in ["SOUL.md", "IDENTITY.md", "TOOLS.md", "USER.md"]:
        if not (agent_dir / extra).exists():
            p1_notes.append(f"建议补充 {extra}")

    return AgentAudit(agent_name, memory_path, len(p0_issues) == 0, p0_issues, p1_notes)


def build_report(results: list[AgentAudit]) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(results)
    passed = sum(1 for r in results if r.p0_pass)
    lines = [
        "# 记忆完整性审计报告（最小版）",
        "",
        f"- 生成时间: {ts}",
        f"- 目标角色数: {total}",
        f"- P0 通过数: {passed}/{total}",
        "",
        "## 审计口径",
        "- P0: MEMORY.md 存在、非空、具根记忆对齐声明、具六大核心模块",
        "- P1: SOUL / IDENTITY / TOOLS / USER 是否齐备，仅做提示",
        "",
        "## 结果明细",
    ]

    for result in results:
        status = "PASS" if result.p0_pass else "FAIL"
        lines.extend([
            "",
            f"### {result.name} - {status}",
            f"- 路径: `{result.memory_path.relative_to(ROOT)}`",
        ])
        if result.p0_issues:
            lines.append("- P0 问题:")
            lines.extend([f"  - {issue}" for issue in result.p0_issues])
        else:
            lines.append("- P0 问题: 无")
        if result.p1_notes:
            lines.append("- P1 提示:")
            lines.extend([f"  - {note}" for note in result.p1_notes])
        else:
            lines.append("- P1 提示: 无")

    lines.extend([
        "",
        "## 建议动作",
        "- 若有 FAIL，先补 MEMORY.md 结构完整性，再进入内容充实。",
        "- 下一版可加入新 Agent 自动发现与占位内容识别。",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    results = [audit_agent(name) for name in TARGET_AGENTS]
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(results), encoding="utf-8")
    print(REPORT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
