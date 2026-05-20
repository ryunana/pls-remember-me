"""Shared helpers for local-only privacy and signal scoring."""

from __future__ import annotations

import re


# Placeholder substitution preserves sentence structure while removing obvious
# local or credential-bearing details from downstream artifacts.
REDACTION_PATTERNS = [
    (re.compile(r"\bhttps://auth\.[^\s`\"'<>]+", re.IGNORECASE), "[AUTH_URL]"),
    (re.compile(r"\b[A-Z0-9]{4}-[A-Z0-9]{4,8}\b"), "[DEVICE_CODE]"),
    (re.compile(r"(?im)^Last login: .*$"), "[TERMINAL_LOGIN]"),
    (
        re.compile(
            r"(?<![\w./-])"
            r"(?:~|/(?:Users|home)/[^/\s]+|/Volumes/[^/\s]+|[A-Za-z]:\\Users\\[^\\/\s]+)"
            r"(?:[\\/][^\n\r`\"'<>|,，;；]*)*"
        ),
        "[LOCAL_PATH]",
    ),
    (re.compile(r"sk-[A-Za-z0-9_\-]{16,}"), "[SECRET]"),
    (re.compile(r"sk-ant-[A-Za-z0-9_\-]{16,}"), "[SECRET]"),
    (re.compile(r"xox[bps]-[A-Za-z0-9_\-]{8,}"), "[SECRET]"),
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[EMAIL]"),
    (re.compile(r"\b1[3-9]\d{9}\b"), "[PHONE]"),  # CN mobile
]

STRUCTURAL_LINE_RE = re.compile(r"^\s*(?:[-*+>]|\d+[.)]|#{1,6}\s|```|\|)")
DIRECT_REQUEST_MARKERS = (
    "我需要你", "需要你", "帮我", "请你", "请帮", "你先", "直接", "不要", "必须",
    "i need you", "please", "can you", "help me",
)


def redact(text: str) -> str:
    for pattern, placeholder in REDACTION_PATTERNS:
        text = pattern.sub(placeholder, text)
    return text


def pasted_context_penalty(text: str) -> int:
    """Downrank long pasted source material without keying on domain-specific words."""
    stripped = text.strip()
    if len(stripped) < 1200:
        return 0

    lines = [line for line in stripped.splitlines() if line.strip()]
    if len(lines) < 12 and "```" not in stripped:
        return 0

    structural_lines = sum(1 for line in lines if STRUCTURAL_LINE_RE.match(line))
    long_lines = sum(1 for line in lines if len(line) > 160)
    source_like = (
        structural_lines >= 6
        or stripped.count("```") >= 2
        or len(lines) >= 25
        or long_lines >= 6
    )
    if not source_like:
        return 0

    penalty = 8 if len(stripped) > 3000 else 5
    lead = stripped[:600].lower()
    if any(marker in lead for marker in DIRECT_REQUEST_MARKERS):
        penalty = max(2, penalty // 2)
    return penalty
