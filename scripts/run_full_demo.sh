#!/usr/bin/env bash
#
# Full synthetic demo: prepare sample logs, validate the committed synthetic
# profile.json, and render the paste-friendly profile + installable context
# packages. This never reads real user logs.
#
set -euo pipefail
cd "$(dirname "$0")/.."

OUT_DIR="samples/out/full-demo"
PREPARE_DIR="$OUT_DIR/prepare"
RENDER_DIR="$OUT_DIR/rendered-raw"
PROFILE_JSON="samples/demo-profile.json"

rm -rf "$OUT_DIR"
mkdir -p "$PREPARE_DIR" "$RENDER_DIR"

echo "==> 1/3 Prepare synthetic logs into a distillation packet"
python3 scripts/pls_remember_me.py prepare \
  --input-dir samples/logs \
  --out-dir "$PREPARE_DIR"

FRICTION_FILE="$(ls -1 "$PREPARE_DIR"/*-friction.jsonl | tail -1)"
PACKET_FILE="$(ls -1 "$PREPARE_DIR"/*-distillation_packet.md | tail -1)"
SUMMARY_FILE="$(ls -1 "$PREPARE_DIR"/*-summary.md | tail -1)"

echo
printf '  summary: %s\n' "$SUMMARY_FILE"
printf '  friction: %s\n' "$FRICTION_FILE"
printf '  packet:   %s\n' "$PACKET_FILE"

echo
echo "==> 2/3 Validate committed synthetic profile against packet evidence refs"
python3 scripts/pls_remember_me.py validate \
  --profile "$PROFILE_JSON" \
  --friction "$FRICTION_FILE"

echo
echo "==> 3/3 Render profile, evidence appendix, and context packages"
python3 scripts/pls_remember_me.py render \
  --profile "$PROFILE_JSON" \
  --out-dir "$RENDER_DIR"

# Create stable demo paths in addition to timestamped render outputs, so README
# screenshots/snippets and smoke tests can point at predictable files.
cp "$(ls -1 "$RENDER_DIR"/*-profile.md | grep -v 'profile-evidence' | tail -1)" "$OUT_DIR/profile.md"
cp "$(ls -1 "$RENDER_DIR"/*-profile-evidence.md | tail -1)" "$OUT_DIR/profile-evidence.md"
cp -R "$RENDER_DIR/personal-context-skill" "$OUT_DIR/personal-context-skill"
cp -R "$RENDER_DIR/claude-code-skill" "$OUT_DIR/claude-code-skill"
cp -R "$RENDER_DIR/claude-code-memory" "$OUT_DIR/claude-code-memory"

echo
echo "============================================================"
echo "Full demo done. Stable outputs:"
echo "  $OUT_DIR/profile.md"
echo "  $OUT_DIR/profile-evidence.md"
echo "  $OUT_DIR/personal-context-skill/SKILL.md"
echo "  $OUT_DIR/claude-code-skill/personal-context/SKILL.md"
echo "  $OUT_DIR/claude-code-memory/CLAUDE.md"
echo
echo "These files are generated from synthetic sample data and ignored by git."
echo "Use them to inspect the final shape before running on real logs."
echo "============================================================"
