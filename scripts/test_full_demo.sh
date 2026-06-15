#!/usr/bin/env bash
# Smoke test for the public synthetic end-to-end demo.
# Uses only committed synthetic sample data; never reads real user logs.
set -euo pipefail
cd "$(dirname "$0")/.."

bash scripts/run_full_demo.sh >/tmp/pls-remember-me-full-demo.log

OUT_DIR="samples/out/full-demo"
PROFILE_JSON="samples/demo-profile.json"

[ -f "$PROFILE_JSON" ] || { echo "missing $PROFILE_JSON"; exit 1; }
[ -f "$OUT_DIR/profile.md" ] || { echo "missing rendered profile.md"; exit 1; }
[ -f "$OUT_DIR/profile-evidence.md" ] || { echo "missing rendered profile-evidence.md"; exit 1; }
[ -f "$OUT_DIR/personal-context-skill/SKILL.md" ] || { echo "missing personal-context-skill/SKILL.md"; exit 1; }
[ -f "$OUT_DIR/personal-context-skill/context-profile.md" ] || { echo "missing personal-context-skill/context-profile.md"; exit 1; }
[ -f "$OUT_DIR/claude-code-skill/personal-context/SKILL.md" ] || { echo "missing claude-code skill"; exit 1; }
[ -f "$OUT_DIR/claude-code-memory/CLAUDE.md" ] || { echo "missing Claude Code memory fragment"; exit 1; }
[ -f "$OUT_DIR/result-card.md" ] || { echo "missing result-card.md"; exit 1; }

grep -q "用户要求先查证再判断" "$OUT_DIR/profile.md" || { echo "profile.md did not include demo axiom"; exit 1; }
grep -q "context-profile.md" "$OUT_DIR/personal-context-skill/SKILL.md" || { echo "generated skill does not point to context-profile.md"; exit 1; }
grep -q "Turn past AI corrections into a traceable personal context seed" "$OUT_DIR/result-card.md" || { echo "result-card.md missing positioning line"; exit 1; }
grep -q "Full demo done" /tmp/pls-remember-me-full-demo.log || { echo "full demo did not finish cleanly"; exit 1; }

echo "OK: full demo smoke test passed"
