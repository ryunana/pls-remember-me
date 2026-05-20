#!/usr/bin/env python3
"""Build distillation_packet.md from a friction.jsonl + summary.md.

The packet is what you hand to an AI tool (Claude Code / Codex / etc) and ask
it to distill axioms. The packet is self-contained: prompt + evidence + output
contract. The AI reads it, produces profile.json, you bring it back to validate.

Usage:
  python3 scripts/packet.py --friction <path>.jsonl [--top 60] [--out-dir <dir>]
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

try:
    from common import pasted_context_penalty, redact
except ImportError:  # pragma: no cover - supports package-style imports
    from .common import pasted_context_penalty, redact


PROMPT_HEADER = """\
# pls-remember-me 蒸馏证据包

## 你的任务

基于下面的真实片段（这位用户在 AI 协作中的纠正、推翻、决策、边界声明），蒸馏出
**5–10 条稳定的判断原则（axioms）**。

axiom = "这位用户怎么判断 / 怎么取舍 / 怎么要求 AI 配合"，**不是事实标签**。

## 硬性要求

1. 每条 axiom 必须由 **至少 2 个不同 public_ref 的证据**支撑。
2. axiom 必须是判断原则，不是事实（❌ "用户用 Codex" / ✅ "评估方案时优先可调试性"）。
3. **不脑补**：证据里没出现的，宁可不写；信息不足就降 confidence，不要补。
4. 给出 **反例 / 不适用场景**——AI 后续看到这条不能机械套用。
5. 引用 `public_ref` 必须从证据列表里抄过来，不要发明新引用。

## 输出格式（**严格 JSON**，validator 会校验）

```json
{
  "version": "v1",
  "generated_by": "<你是哪个 AI 工具，例如 claude-code 或 codex>",
  "source_stats": {
    "messages_reviewed": 0,
    "evidence_used": 0
  },
  "axioms": [
    {
      "statement": "一句话判断原则（行为指令性，不是事实）",
      "confidence": "high | medium | low | unstable",
      "执行要求": "AI 读到后应该改变什么输出方式 / 协作动作",
      "反例": "什么场景这条不适用 / 需要谨慎套用",
      "evidence_refs": ["public_ref_1", "public_ref_2"]
    }
  ]
}
```

## confidence 标签

- `high`：跨多个场景、反复出现、最近还在出现
- `medium`：出现多次但场景较单一
- `low`：仅 2-3 次出现
- `unstable`：曾经出现但最近一段时间不见

---

## 证据：高信号片段（按命中关键词强度排序）

下面每个片段都是一条用户的真实消息。长篇粘贴材料会被通用结构规则降权，以优先保留用户自己的纠正、边界和协作要求。**只引用这里出现的 `public_ref`**。

"""

def score_hit(found: list[str], text: str) -> int:
    important = {
        "不对", "不是这个意思", "重写", "太泛", "废话", "我想要的是",
        "不要脑补", "不要伪造", "信息不足", "不应该", "错", "问题是",
        "关键是", "不够", "现实", "难", "麻烦", "边界", "细化", "完整",
    }
    base = sum(4 if kw in important else 1 for kw in found)
    penalty = pasted_context_penalty(text)
    if penalty:
        return base - penalty
    return base + min(len(text) // 600, 2)


def clip(text: str, limit: int = 600) -> str:
    text = text.replace("\n\n\n", "\n\n").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def main() -> int:
    parser = argparse.ArgumentParser(description="Build distillation packet for AI handoff.")
    parser.add_argument("--friction", type=Path, required=True, help="Path to friction.jsonl from ingest")
    parser.add_argument("--out-dir", type=Path, default=Path.home() / ".pls-remember-me" / "out")
    parser.add_argument("--top", type=int, default=60, help="Top snippets to include in packet (default 60)")
    parser.add_argument("--max-tokens", type=int, default=16000, help="Soft cap on packet body tokens (approx 3 chars/token)")
    args = parser.parse_args()

    if not args.friction.exists():
        print(f"error: friction file not found: {args.friction}")
        return 1

    snippets = []
    with args.friction.open() as f:
        for line in f:
            try:
                snippets.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    # Sort by score
    scored = [
        (s, score_hit(s.get("keywords", []), s.get("text", "")))
        for s in snippets
    ]
    scored.sort(key=lambda x: x[1], reverse=True)

    # Take top N, but also enforce soft token cap
    char_cap = args.max_tokens * 3  # rough estimate
    body_lines: list[str] = []
    body_chars = 0
    used = 0
    by_source: Counter[str] = Counter()

    for snippet, _score in scored[: args.top]:
        text = clip(redact(snippet.get("text", "")), 600)
        ref = snippet.get("public_ref", "?")
        kws = ", ".join(snippet.get("keywords", []))
        block = f"### snippet {used + 1}\n\n- ref: `{ref}`\n- keywords: {kws}\n- source: {snippet.get('source', '?')}\n\n> {text}\n\n"
        if body_chars + len(block) > char_cap:
            break
        body_lines.append(block)
        body_chars += len(block)
        used += 1
        by_source[snippet.get("source", "?")] += 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    packet_path = args.out_dir / f"{run_id}-distillation_packet.md"

    with packet_path.open("w", encoding="utf-8") as f:
        f.write(PROMPT_HEADER)
        f.write(f"_包含 {used} / {len(snippets)} 条证据 · 来源分布 {dict(by_source)} · 约 {body_chars // 3} tokens_\n\n")
        f.writelines(body_lines)
        f.write("\n---\n\n_证据包结束。请按上面 JSON 格式输出 profile.json。_\n")

    print(f"packet={packet_path}")
    print(f"included={used}/{len(snippets)} snippets, ~{body_chars // 3} tokens")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
