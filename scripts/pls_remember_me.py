#!/usr/bin/env python3
"""pls-remember-me CLI entry point.

Subcommands (v1):
  prepare    Scan --input-dir, generate friction.jsonl + summary.md + distillation_packet.md
  validate   Check AI-produced profile.json against schema
  render     Render validated profile.json to profile.md + evidence appendix + local context packages

Workflow:
  1. python3 scripts/pls_remember_me.py prepare --input-dir ~/.claude/projects --input-dir ~/.codex/sessions
  2. Hand the distillation_packet.md to Claude Code / Codex / etc, ask it to follow
     the embedded instructions and produce profile.json. Save profile.json locally.
  3. python3 scripts/pls_remember_me.py validate --profile <path>.json --friction <path>.jsonl
     (If FAIL: copy the printed rewrite-hint, paste back to AI, get new JSON, re-validate.)
  4. python3 scripts/pls_remember_me.py render --profile <path>.json
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run(cmd: list[str]) -> int:
    print(f"$ {' '.join(cmd)}")
    return subprocess.call(cmd)


def cmd_prepare(args) -> int:
    input_args: list[str] = []
    for d in args.input_dir:
        input_args.extend(["--input-dir", str(d)])

    rc = run([
        sys.executable, str(SCRIPT_DIR / "ingest.py"),
        *input_args,
        "--out-dir", str(args.out_dir),
    ])
    if rc != 0:
        return rc

    # find the latest friction file we just wrote
    friction_files = sorted(args.out_dir.glob("*-friction.jsonl"))
    if not friction_files:
        print("error: ingest produced no friction.jsonl")
        return 1
    latest = friction_files[-1]

    rc = run([
        sys.executable, str(SCRIPT_DIR / "packet.py"),
        "--friction", str(latest),
        "--out-dir", str(args.out_dir),
    ])
    if rc != 0:
        return rc

    print()
    print("=" * 60)
    print("下一步（AI handoff）：")
    print(f"  1. 打开你常用的 AI 工具（Claude Code / Codex 等）")
    print(f"  2. 把 {sorted(args.out_dir.glob('*-distillation_packet.md'))[-1]} 完整内容发给 AI")
    print(f"  3. 让它按 packet 顶部 prompt 输出严格 JSON，保存为 profile.json")
    print(f"  4. 运行：python3 scripts/pls_remember_me.py validate \\")
    print(f"          --profile <你的 profile.json> --friction {latest}")
    print("=" * 60)
    return 0


def cmd_validate(args) -> int:
    return run([
        sys.executable, str(SCRIPT_DIR / "validate.py"),
        "--profile", str(args.profile),
        *(["--friction", str(args.friction)] if args.friction else []),
    ])


def cmd_render(args) -> int:
    return run([
        sys.executable, str(SCRIPT_DIR / "render.py"),
        "--profile", str(args.profile),
        "--out-dir", str(args.out_dir),
    ])


def main() -> int:
    parser = argparse.ArgumentParser(prog="pls-remember-me", description="Personal context infrastructure starter.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prep = sub.add_parser("prepare", help="Ingest logs and build distillation packet.")
    p_prep.add_argument("--input-dir", action="append", required=True, type=Path)
    p_prep.add_argument("--out-dir", type=Path, default=Path.home() / ".pls-remember-me" / "out")
    p_prep.set_defaults(func=cmd_prepare)

    p_val = sub.add_parser("validate", help="Validate AI-produced profile.json.")
    p_val.add_argument("--profile", type=Path, required=True)
    p_val.add_argument("--friction", type=Path, default=None, help="Optional friction.jsonl to verify evidence refs")
    p_val.set_defaults(func=cmd_validate)

    p_ren = sub.add_parser(
        "render",
        help=(
            "Render profile.json to profile.md, profile-evidence.md, "
            "personal-context-skill/, claude-code-skill/, and claude-code-memory/."
        ),
    )
    p_ren.add_argument("--profile", type=Path, required=True)
    p_ren.add_argument("--out-dir", type=Path, default=Path.home() / ".pls-remember-me" / "out")
    p_ren.set_defaults(func=cmd_render)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
