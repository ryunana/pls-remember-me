#!/usr/bin/env bash
#
# 30 秒零数据 demo：用仓库自带的合成 samples/logs 跑一次完整 prepare。
# 不需要你的任何真实日志，可以放心 git clone 后直接 bash 这个脚本。
#
# 这个 demo 不证明真实蒸馏质量（合成样本太小），只证明：
# - 流水线能跑通（ingest → friction → packet）
# - 输出格式长什么样
# - 你的本机环境有 python3 能用
#
# 真实路径请见 README "用你自己的数据"。

set -e
cd "$(dirname "$0")/.."

OUT_DIR="samples/out"
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

echo "==> Running prepare on samples/logs (3 synthetic Claude Code sessions, ~20 messages)"
python3 scripts/pls_remember_me.py prepare \
  --input-dir samples/logs \
  --out-dir "$OUT_DIR"

echo
echo "============================================================"
echo "Demo done. Look at:"
ls -1 "$OUT_DIR"/*.md 2>/dev/null | sed 's/^/  /'
echo
echo "Next: open the *-distillation_packet.md, see what would get handed off to an AI."
echo "（合成样本只有 ~20 条消息，packet 内容很短，仅作格式演示。"
echo "  真实路径请把 --input-dir 换成 ~/.claude/projects 或 ~/.codex/sessions）"
echo "============================================================"
