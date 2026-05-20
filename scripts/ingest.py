#!/usr/bin/env python3
"""Ingest AI chat logs from one or more --input-dir into normalized messages.

Abstracted from personal-context-infrastructure/scripts/export_ai_chats.py:
- removed Path.home() hardcoding → user must pass --input-dir (one or more)
- streaming jsonl read with early type filtering (S-1 finding: codex single file up to 250MB)
- per-record path stripped to public_ref (no local filesystem paths leak downstream)
- minimal redaction for API key / email / phone
- adapter dispatch by directory hint or file pattern

Usage:
  python3 scripts/ingest.py --input-dir ~/.claude/projects --input-dir ~/.codex/sessions \\
      --out-dir ~/.pls-remember-me/out

Outputs:
  <out-dir>/<run-id>-summary.md       human review
  <out-dir>/<run-id>-friction.jsonl   machine-readable snippets
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    from common import pasted_context_penalty, redact
except ImportError:  # pragma: no cover - supports package-style imports
    from .common import pasted_context_penalty, redact


DEFAULT_KEYWORDS = [
    "不对", "不是这个意思", "重写", "太泛", "废话", "我想要的是", "不要", "不应该",
    "别", "太空", "具体", "不够", "重新", "错", "问题是", "关键是", "我的意思",
    "现实", "难", "麻烦", "直接", "简洁", "啰嗦", "落地", "可执行", "真实", "判断",
    "不要脑补", "不要伪造", "信息不足", "结论先行", "少废话", "说人话", "完整",
    "细化", "边界", "优先", "跳过",
]

NOISE_PREFIXES = (
    "# AGENTS.md instructions",
    "<environment_context>",
    "Base directory for this skill:",
    "# Files mentioned by the user:",
    "<INSTRUCTIONS>",
    "<permissions instructions>",
    "This session is being continued from a previous conversation",
)

NOISE_MARKERS = (
    "You are Codex, a coding agent",
    "You are Claude Code",
    "Available tools:",
    "How to use skills",
    "<skills_instructions>",
    "<plugins_instructions>",
)

THEMES = {
    "直接推进 / 不绕路": ["直接", "重新", "不要", "别"],
    "优先级 / 范围控制": ["优先", "跳过", "麻烦", "先"],
    "落地 / 细节 / 完整性": ["具体", "不够", "细化", "完整", "可执行", "落地"],
    "产品边界 / 规则判断": ["边界", "不应该", "应该", "判断", "功能边界"],
    "准确性 / 禁止脑补": ["不对", "错", "不要脑补", "不要伪造", "信息不足", "不是这个意思"],
    "反 AI 味 / 表达质量": ["废话", "太泛", "太空", "重写", "说人话", "简洁", "啰嗦"],
}

# Claude Code noise types (S-1 finding: ~46% of records are non-conversation)
CLAUDE_NOISE_TYPES = {
    "file-history-snapshot", "queue-operation", "last-prompt",
    "attachment", "ai-title", "system",
}

# Codex noise types (S-1 finding: ~80% of response_item are non-message)
CODEX_NOISE_TOP_TYPES = {"event_msg", "turn_context", "session_meta", "compacted"}
CODEX_NOISE_RESPONSE_TYPES = {
    "function_call", "function_call_output", "reasoning",
    "custom_tool_call", "custom_tool_call_output", "web_search_call",
}

@dataclass(frozen=True)
class Message:
    source: str          # "claude-code" | "codex" | "chatmemo"
    timestamp: str | None
    role: str
    text: str
    public_ref: str      # safe-to-publish reference (no local paths)


def content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") in {"text", "input_text", "output_text"}:
                parts.append(str(item.get("text", "")))
            elif isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(part for part in parts if part)
    if isinstance(content, dict) and isinstance(content.get("text"), str):
        return content["text"]
    return ""


def is_noise(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if any(stripped.startswith(prefix) for prefix in NOISE_PREFIXES):
        return True
    if any(marker in stripped[:2500] for marker in NOISE_MARKERS):
        return True
    if len(stripped) > 5000 and ("instructions" in stripped[:1000].lower() or "AGENTS.md" in stripped[:1000]):
        return True
    return False


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    """Streaming jsonl read. Bad lines and non-dict lines silently skipped."""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    yield obj
    except OSError:
        return


def public_ref_for(source: str, path: Path, anchor: str) -> str:
    """Build a path-free reference. anchor is uuid/turn-index/line-offset."""
    fname_hash = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10]
    return f"{source}:{fname_hash}:{anchor}"


def parse_codex(path: Path) -> list[Message]:
    messages: list[Message] = []
    line_no = 0
    for obj in iter_jsonl(path):
        line_no += 1
        top_type = obj.get("type")
        if top_type in CODEX_NOISE_TOP_TYPES:
            continue
        if top_type != "response_item":
            continue
        payload = obj.get("payload") or {}
        if payload.get("type") in CODEX_NOISE_RESPONSE_TYPES:
            continue
        if payload.get("type") != "message":
            continue
        role = payload.get("role")
        if role not in {"user", "assistant"}:  # filter out 'developer'
            continue
        text = content_to_text(payload.get("content")).strip()
        if not text or is_noise(text):
            continue
        timestamp = obj.get("timestamp") or payload.get("timestamp")
        ref = public_ref_for("codex", path, f"L{line_no}")
        messages.append(Message("codex", timestamp, role, redact(text), ref))
    return messages


def parse_claude(path: Path) -> list[Message]:
    messages: list[Message] = []
    for obj in iter_jsonl(path):
        t = obj.get("type")
        if t in CLAUDE_NOISE_TYPES:
            continue
        if t not in {"user", "assistant"}:
            continue
        nested = obj.get("message") or {}
        role = nested.get("role") or t
        if role not in {"user", "assistant"}:
            continue
        text = content_to_text(nested.get("content")).strip()
        if not text or is_noise(text):
            continue
        uuid = obj.get("uuid") or obj.get("messageId") or "noid"
        ref = public_ref_for("claude-code", path, uuid[:12])
        messages.append(Message("claude-code", obj.get("timestamp"), role, redact(text), ref))
    return messages


def parse_chatmemo(path: Path) -> list[Message]:
    messages: list[Message] = []
    current_role: str | None = None
    current_timestamp: str | None = None
    current_lines: list[str] = []
    block_no = 0

    def flush() -> None:
        nonlocal current_role, current_timestamp, current_lines, block_no
        if current_role is None:
            return
        text = "\n".join(current_lines).strip()
        if text and not is_noise(text):
            block_no += 1
            ref = public_ref_for("chatmemo", path, f"B{block_no}")
            messages.append(Message("chatmemo", current_timestamp, current_role, redact(text), ref))
        current_role = None
        current_timestamp = None
        current_lines = []

    header_re = re.compile(r"^(User|AI): \[([^\]]+)\]$")
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return messages

    for line in lines:
        if line.startswith("Title: ") or line.startswith("Platform: ") or line.startswith("URL: "):
            flush()
            continue
        match = header_re.match(line)
        if match:
            flush()
            current_role = "user" if match.group(1) == "User" else "assistant"
            current_timestamp = match.group(2).strip()
            continue
        if current_role is not None:
            if line and set(line) == {"="}:
                continue
            current_lines.append(line)
    flush()
    return messages


def detect_adapter(path: Path) -> str | None:
    """Pick adapter by file pattern, with content-sniffing fallback for jsonl.

    Returns 'codex' | 'claude-code' | 'chatmemo' | None.
    """
    name = path.name
    if name.startswith("rollout-") and name.endswith(".jsonl"):
        return "codex"
    if "/.codex/sessions/" in str(path):
        return "codex"
    if "/.claude/projects/" in str(path):
        if "/subagents/" in str(path):
            return None
        return "claude-code"
    if name.endswith(".jsonl"):
        if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.jsonl$", name):
            return "claude-code"
        # Content sniff: look at first non-blank line
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as h:
                for line in h:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        first = json.loads(line)
                    except json.JSONDecodeError:
                        return None
                    if not isinstance(first, dict):
                        return None
                    # Codex shape: top-level {type, payload, timestamp}
                    if "payload" in first and first.get("type") in {"response_item", "session_meta", "event_msg", "turn_context"}:
                        return "codex"
                    # Claude Code shape: top-level {type: user|assistant, message: {...}}
                    if first.get("type") in {"user", "assistant"} and "message" in first:
                        return "claude-code"
                    return None
        except OSError:
            return None
        return None
    if name.endswith(".txt"):
        return "chatmemo"
    return None


def collect_messages(input_dirs: list[Path], include_assistant: bool) -> list[Message]:
    messages: list[Message] = []
    file_count = 0
    skipped = 0

    for input_dir in input_dirs:
        if not input_dir.exists():
            print(f"warn: input-dir does not exist: {input_dir}")
            continue
        for path in input_dir.rglob("*"):
            if not path.is_file():
                continue
            adapter = detect_adapter(path)
            if adapter == "codex":
                messages.extend(parse_codex(path))
                file_count += 1
            elif adapter == "claude-code":
                messages.extend(parse_claude(path))
                file_count += 1
            elif adapter == "chatmemo":
                messages.extend(parse_chatmemo(path))
                file_count += 1
            else:
                skipped += 1

    print(f"info: parsed {file_count} files, skipped {skipped} unknown")

    deduped: list[Message] = []
    seen: set[tuple[str, str, str]] = set()
    for message in messages:
        if not include_assistant and message.role != "user":
            continue
        key = (message.source, message.role, message.text[:1000])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(message)
    return deduped


def clip(text: str, limit: int = 360) -> str:
    single_line = " ".join(text.split())
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 3] + "..."


def build_keyword_regex(keywords: list[str]) -> re.Pattern[str]:
    ordered = sorted(set(keywords), key=len, reverse=True)
    return re.compile("|".join(re.escape(keyword) for keyword in ordered))


def score_hit(found: list[str], text: str) -> int:
    important = {
        "不对", "不是这个意思", "重写", "太泛", "废话", "我想要的是",
        "不要脑补", "不要伪造", "信息不足", "不应该", "错", "问题是",
        "关键是", "不够", "现实", "难", "麻烦", "边界", "细化", "完整",
    }
    base = sum(4 if keyword in important else 1 for keyword in found)
    penalty = pasted_context_penalty(text)
    if penalty:
        return base - penalty
    return base + min(len(text) // 600, 2)


def write_outputs(messages: list[Message], keywords: list[str], output_dir: Path, top_n: int) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    keyword_re = build_keyword_regex(keywords)

    keyword_counts: Counter[str] = Counter()
    role_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    hits: list[tuple[Message, list[str]]] = []

    for message in messages:
        role_counts[f"{message.source}:{message.role}"] += 1
        source_counts[message.source] += 1
        found = keyword_re.findall(message.text)
        if found:
            keyword_counts.update(found)
            hits.append((message, found))

    theme_counts = {
        theme: sum(message.text.count(keyword) for message in messages for keyword in theme_keywords)
        for theme, theme_keywords in THEMES.items()
    }
    top_hits = sorted(hits, key=lambda hit: score_hit(hit[1], hit[0].text), reverse=True)[:top_n]

    summary_path = output_dir / f"{run_id}-summary.md"
    friction_path = output_dir / f"{run_id}-friction.jsonl"

    with friction_path.open("w", encoding="utf-8") as handle:
        for message, found in hits:
            handle.write(
                json.dumps(
                    {
                        "source": message.source,
                        "timestamp": message.timestamp,
                        "role": message.role,
                        "keywords": list(dict.fromkeys(found)),
                        "text": message.text,
                        "public_ref": message.public_ref,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

    with summary_path.open("w", encoding="utf-8") as handle:
        handle.write("# AI Chat Context Scan\n\n")
        handle.write(f"- Generated: {datetime.now().isoformat(timespec='seconds')}\n")
        handle.write(f"- Messages kept: {len(messages)}\n")
        handle.write(f"- Friction snippets: {len(hits)}\n")
        handle.write(f"- Sources: {dict(source_counts)}\n")
        handle.write(f"- Roles: {dict(role_counts)}\n\n")

        handle.write("## Top Keywords\n\n")
        for keyword, count in keyword_counts.most_common(40):
            handle.write(f"- {keyword}: {count}\n")

        handle.write("\n## Theme Counts\n\n")
        for theme, count in sorted(theme_counts.items(), key=lambda item: item[1], reverse=True):
            handle.write(f"- {theme}: {count}\n")

        handle.write("\n## Top User Friction Snippets\n\n")
        for index, (message, found) in enumerate(top_hits, 1):
            handle.write(f"### {index}. {message.source} {message.timestamp or ''}\n\n")
            handle.write(f"- Keywords: {', '.join(dict.fromkeys(found))}\n")
            handle.write(f"- Ref: `{message.public_ref}`\n\n")
            handle.write(f"> {clip(message.text)}\n\n")

    return summary_path, friction_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest AI chat logs to friction snippets and summary.")
    parser.add_argument(
        "--input-dir",
        action="append",
        required=True,
        type=Path,
        help="Directory to scan for jsonl/txt logs. Can be passed multiple times.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path.home() / ".pls-remember-me" / "out",
        help="Output directory (default: ~/.pls-remember-me/out)",
    )
    parser.add_argument("--top", type=int, default=30, help="Top friction snippets in summary.")
    parser.add_argument(
        "--include-assistant",
        action="store_true",
        help="Include assistant messages (default: user only, for preference mining).",
    )
    parser.add_argument("--keywords", nargs="*", default=DEFAULT_KEYWORDS)
    args = parser.parse_args()

    messages = collect_messages(args.input_dir, include_assistant=args.include_assistant)
    summary_path, friction_path = write_outputs(messages, args.keywords, args.out_dir, args.top)
    print(f"messages={len(messages)}")
    print(f"summary={summary_path}")
    print(f"friction={friction_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
