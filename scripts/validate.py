#!/usr/bin/env python3
"""Validate a profile.json produced by an AI tool from a distillation packet.

Hard rules (FAIL):
- valid JSON
- top-level: version, axioms (list)
- each axiom: statement, confidence, evidence_refs (list of >=2)
- confidence ∈ {high, medium, low, unstable}
- evidence_refs reference public_ref strings only (no local paths)
- evidence_refs each look like "<source>:<hash>:<anchor>" (loose check)

Warnings (don't fail, but print):
- missing 执行要求 / 反例 (recommended but not required in v1)
- axiom statement < 8 chars or > 200 chars
- evidence_ref not present in source friction.jsonl (if --friction given)

Failure ends with rewrite hint: a copy-pasteable message to feed back to the AI.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REF_PATTERN = re.compile(r"^(claude-code|codex|chatmemo):[a-f0-9]{6,}:[A-Za-z0-9_\-]+$")


def load_known_refs(friction_path: Path | None) -> set[str] | None:
    if friction_path is None or not friction_path.exists():
        return None
    refs: set[str] = set()
    with friction_path.open() as f:
        for line in f:
            try:
                obj = json.loads(line)
                if "public_ref" in obj:
                    refs.add(obj["public_ref"])
            except json.JSONDecodeError:
                continue
    return refs


def validate(profile: dict, known_refs: set[str] | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if "version" not in profile:
        errors.append("missing top-level 'version'")
    if "axioms" not in profile or not isinstance(profile["axioms"], list):
        errors.append("missing top-level 'axioms' (must be list)")
        return errors, warnings

    axioms = profile["axioms"]
    if not axioms:
        errors.append("axioms list is empty")
        return errors, warnings

    for i, ax in enumerate(axioms):
        prefix = f"axiom[{i}]"
        if not isinstance(ax, dict):
            errors.append(f"{prefix}: not a dict")
            continue

        # statement
        statement = ax.get("statement")
        if not statement:
            errors.append(f"{prefix}: missing 'statement'")
        elif not isinstance(statement, str):
            errors.append(f"{prefix}: 'statement' must be string")
        else:
            if len(statement) < 8:
                warnings.append(f"{prefix}: statement too short ({len(statement)} chars)")
            if len(statement) > 200:
                warnings.append(f"{prefix}: statement too long ({len(statement)} chars)")

        # confidence
        conf = ax.get("confidence")
        if conf not in {"high", "medium", "low", "unstable"}:
            errors.append(f"{prefix}: confidence must be one of high/medium/low/unstable (got {conf!r})")

        # evidence_refs
        refs = ax.get("evidence_refs")
        if not isinstance(refs, list):
            errors.append(f"{prefix}: 'evidence_refs' must be a list")
        elif len(refs) < 2:
            errors.append(f"{prefix}: need >=2 evidence_refs (got {len(refs)})")
        else:
            for j, ref in enumerate(refs):
                if not isinstance(ref, str):
                    errors.append(f"{prefix}.evidence_refs[{j}]: must be string")
                    continue
                if not REF_PATTERN.match(ref):
                    errors.append(f"{prefix}.evidence_refs[{j}]: bad format {ref!r} (expected '<source>:<hash>:<anchor>')")
                    continue
                if known_refs is not None and ref not in known_refs:
                    warnings.append(f"{prefix}.evidence_refs[{j}]: ref {ref!r} not found in source friction.jsonl (possibly hallucinated)")

        # recommended fields (warn only in v1)
        if not ax.get("执行要求"):
            warnings.append(f"{prefix}: missing '执行要求' (recommended)")
        if not ax.get("反例"):
            warnings.append(f"{prefix}: missing '反例' (recommended)")

    return errors, warnings


def rewrite_hint(errors: list[str]) -> str:
    return f"""

---

# 复制下面这段发回给生成 profile.json 的 AI：

> 上一版 profile.json 没过 validator。错误如下：
>
{chr(10).join(f"> - {e}" for e in errors)}
>
> 请只修订这些错误，保留其他字段不变。再次输出严格 JSON，从 `{{` 开始到 `}}` 结束，不要任何前后缀文字。

---
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate profile.json against pls-remember-me v1 schema.")
    parser.add_argument("--profile", type=Path, required=True, help="Path to profile.json from AI")
    parser.add_argument("--friction", type=Path, default=None, help="Optional friction.jsonl to verify evidence_refs exist")
    args = parser.parse_args()

    if not args.profile.exists():
        print(f"error: profile not found: {args.profile}")
        return 2

    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"FAIL: not valid JSON ({e})")
        print(rewrite_hint([f"invalid JSON: {e}"]))
        return 1

    known_refs = load_known_refs(args.friction)
    errors, warnings = validate(profile, known_refs)

    for w in warnings:
        print(f"WARN: {w}")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        print(rewrite_hint(errors))
        return 1

    print(f"OK: {len(profile.get('axioms', []))} axioms passed ({len(warnings)} warnings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
