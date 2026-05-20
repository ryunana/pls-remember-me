# pls-remember-me

[English](README.md) | [简体中文](README.zh-CN.md)

> Stop reintroducing yourself to every new AI session.

`pls-remember-me` is a local tool for heavy AI users. It scans your own Claude Code / Codex style chat logs, extracts high-signal moments where you corrected, constrained, or redirected an AI, and turns them into a traceable evidence packet.

You then give that packet to an AI tool you choose. The AI produces a `profile.json`; this project validates it and renders:

- a paste-friendly `profile.md`
- a local `personal-context-skill/` package you can install into Codex-style skill directories

The goal is not to summarize your chat history. The goal is to produce a first personal context seed: how you judge, how you make tradeoffs, and how an AI should collaborate with you.

## What It Does Not Do

- It does not upload your logs.
- It does not run a hosted memory service.
- It does not automatically call a cloud model.
- It does not collect analytics.
- It does not commit your real profile or real logs into this repo.

Your real data stays on your machine and inside the AI tool you explicitly choose for distillation.

## Try It With No Personal Data

```bash
git clone <repo-url>
cd pls-remember-me
bash scripts/run_demo.sh
```

The demo uses synthetic logs under `samples/logs/` and writes gitignored output to `samples/out/`:

- `*-summary.md`
- `*-friction.jsonl`
- `*-distillation_packet.md`

This proves the local pipeline works. The demo data is intentionally small, so it only shows the format, not the real value of running on your own history.

## Run It On Your Logs

### 1. Build A Distillation Packet

```bash
python3 scripts/pls_remember_me.py prepare \
  --input-dir ~/.claude/projects \
  --input-dir ~/.codex/sessions
```

By default, output goes to:

```bash
~/.pls-remember-me/out
```

### 2. Ask Your AI Tool To Distill The Packet

Open the generated `*-distillation_packet.md`, paste it into Claude Code / Codex / another AI tool you trust, and ask it to follow the packet instructions exactly.

Save the AI output as `profile.json`.

### 3. Validate The Profile

```bash
python3 scripts/pls_remember_me.py validate \
  --profile profile.json \
  --friction ~/.pls-remember-me/out/<timestamp>-friction.jsonl
```

If validation fails, the command prints a rewrite instruction you can paste back to the AI.

### 4. Render Markdown + Skill Package

```bash
python3 scripts/pls_remember_me.py render --profile profile.json
```

This writes:

- `~/.pls-remember-me/out/<timestamp>-profile.md`
- `~/.pls-remember-me/out/personal-context-skill/SKILL.md`
- `~/.pls-remember-me/out/personal-context-skill/context-profile.md`

To install the generated skill into Codex:

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/personal-context
cp -R ~/.pls-remember-me/out/personal-context-skill ~/.codex/skills/personal-context
```

## Current v1 Support

Implemented:

- Claude Code `.jsonl` parsing
- Codex `rollout-*.jsonl` parsing
- ChatMemo `.txt` dump parsing
- streaming JSONL reading and early noise filtering
- redaction placeholders: `[SECRET]`, `[EMAIL]`, `[PHONE]`
- path-free `public_ref` evidence references
- distillation packet generation
- profile validation with evidence-ref checks
- `profile.md` rendering
- `personal-context-skill/` rendering

Known limits:

- demo covers synthetic Claude-style logs only
- ChatMemo parser exists but has no public sample yet
- Hermes SQLite is not implemented
- daily / weekly observer commands are not implemented
- v1 is axiom-first: it captures judgment principles better than identity, style, or domain labels
- v1 is full rerun, not incremental memory
- validator checks structure and evidence refs; it does not judge whether an axiom is insightful

## Project Boundary

This repo contains mechanism and synthetic sample data only.

Real logs, generated packets, generated profiles, and generated skills should stay in gitignored or external local paths such as:

- `~/.pls-remember-me/out`
- `samples/out/`
- `local_dogfood/`

See [docs/architecture.md](docs/architecture.md) and [docs/v1-plan.md](docs/v1-plan.md) for the current implementation boundary.

## License

MIT
