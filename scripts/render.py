#!/usr/bin/env python3
"""Render a validated profile.json into a paste-friendly profile.md.

profile.md is what you paste into any AI tool's system prompt or context
to make it understand your judgment style.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


CONF_BADGE = {
    "high": "🟢 high",
    "medium": "🟡 medium",
    "low": "🟠 low",
    "unstable": "⚪ unstable",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Render profile.json to profile.md.")
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path.home() / ".pls-remember-me" / "out")
    args = parser.parse_args()

    profile = json.loads(args.profile.read_text(encoding="utf-8"))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    out_path = args.out_dir / f"{run_id}-profile.md"

    lines: list[str] = []
    lines.append("# 我的 AI 协作 context\n")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')} · "
                 f"by {profile.get('generated_by', 'unknown')} · "
                 f"schema {profile.get('version', '?')}_\n")
    lines.append("\n> 把这份内容贴进你打开的新 AI 会话（system prompt / 第一条消息 / 项目 context 文件），")
    lines.append("> 让它在和你协作前先理解你的判断方式。\n\n")
    lines.append("---\n\n")

    axioms = profile.get("axioms", [])
    lines.append(f"## 我的 {len(axioms)} 条判断原则\n\n")

    for i, ax in enumerate(axioms, 1):
        conf = ax.get("confidence", "?")
        badge = CONF_BADGE.get(conf, conf)
        lines.append(f"### {i}. {ax.get('statement', '(missing)')}\n\n")
        lines.append(f"_把握度：{badge} · 证据 {len(ax.get('evidence_refs', []))} 条_\n\n")

        if exec_req := ax.get("执行要求"):
            lines.append(f"**AI 应该怎么做**：{exec_req}\n\n")
        if counter := ax.get("反例"):
            lines.append(f"**不适用场景**：{counter}\n\n")

        refs = ax.get("evidence_refs", [])
        if refs:
            lines.append(f"<details><summary>证据 refs（{len(refs)}）</summary>\n\n")
            for ref in refs:
                lines.append(f"- `{ref}`\n")
            lines.append("\n</details>\n\n")

    lines.append("\n---\n\n")
    lines.append("_这份 profile 来自你自己的 AI 协作历史；跨次重蒸跨次不可比（v1 全量重蒸，详见 README）。_\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"profile_md={out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
