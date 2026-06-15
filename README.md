# pls-remember-me

[English](README.md) | [简体中文](README.zh-CN.md)

> Stop reintroducing yourself to every new AI session.

`pls-remember-me` turns your past AI corrections into a traceable personal context seed. It scans your local Claude Code / Codex style chat logs, extracts high-signal moments where you corrected, constrained, or redirected an AI, and prepares an evidence packet for a model you choose.

The model produces `profile.json`; this project validates it and renders context artifacts you can actually use:

- a paste-friendly `profile.md`
- a separate `profile-evidence.md` audit appendix
- a local `personal-context-skill/` package for Codex-style skill directories
- a local `claude-code-skill/` package for Claude Code
- an optional `claude-code-memory/CLAUDE.md` fragment for persistent Claude Code memory

The goal is not to summarize your chat history. The goal is to produce a first personal context seed: how you judge, how you make tradeoffs, and how an AI should collaborate with you.

## What You Get After The Demo

Run the full synthetic demo:

```bash
git clone https://github.com/ryunana/pls-remember-me.git
cd pls-remember-me
bash scripts/run_full_demo.sh
```

It uses only committed synthetic logs and the committed `samples/demo-profile.json`. No real user logs are read.

Stable generated outputs are written under the gitignored `samples/out/full-demo/` directory:

```text
samples/out/full-demo/
├── profile.md
├── profile-evidence.md
├── personal-context-skill/
│   ├── SKILL.md
│   └── context-profile.md
├── claude-code-skill/personal-context/
│   ├── SKILL.md
│   └── context-profile.md
├── claude-code-memory/CLAUDE.md
└── result-card.md
```

`result-card.md` is a screenshot-friendly summary of the demo output:

```text
┌──────────────────────────────────────────────┐
│  Personal Context Seed                       │
│  Input: synthetic Claude-style logs          │
│  Evidence: high-signal user corrections      │
│  Output: profile.md + evidence appendix      │
│  Packages: Codex skill + Claude Code skill   │
└──────────────────────────────────────────────┘
```

A rendered rule looks like this:

```markdown
### 用户要求先查证再判断，证据不足时明说不足，不用脑补选项替用户猜。

How the AI should behave: 回答前优先检索、运行验证或说明证据缺口；不要用未经验证的可能性替代结论。
When not to over-apply it: 创意发散、命名或头脑风暴任务可以先给候选方向，但仍要标注它们只是候选。
```

The generated skill points the agent at `context-profile.md` first, while evidence refs stay in the separate appendix for audit instead of being loaded into every session.

## Why This Is Not Another Memory Backend

| If you want... | Use... | Why |
|---|---|---|
| automatic long-term capture, indexing, and recall | a memory backend such as memsearch / episodic-memory / claude-mem | those tools manage ongoing memory infrastructure |
| one clean starting profile for a new AI tool | `pls-remember-me` | it distills your prior corrections into a portable context seed |
| evidence-backed collaboration rules without uploading logs by default | `pls-remember-me` | the packet is local, and you choose which AI sees it |
| a searchable archive of every past decision | a semantic memory/search system | `pls-remember-me` intentionally selects high-signal friction, not everything |

`pls-remember-me` is best used before or alongside a memory backend: generate the first personal context seed, inspect the evidence, then paste or install the rendered context where you want it.

## What It Does Not Do

- It does not upload your logs.
- It does not run a hosted memory service.
- It does not automatically call a cloud model.
- It does not collect analytics.
- It does not commit your real profile or real logs into this repo.

Your real data stays on your machine and inside the AI tool you explicitly choose for distillation.

## Quick Demos

### Packet-only demo

```bash
bash scripts/run_demo.sh
```

This proves the first half of the local pipeline:

```text
samples/logs/ → summary.md + friction.jsonl + distillation_packet.md
```

### Full synthetic demo

```bash
bash scripts/run_full_demo.sh
```

This proves the public end-to-end shape:

```text
samples/logs/
  → distillation_packet.md
  → samples/demo-profile.json
  → validate
  → profile.md + evidence appendix + installable context packages
```

### Smoke test

```bash
bash scripts/test_full_demo.sh
```

This validates that the full synthetic demo renders all expected artifacts.

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

### 4. Render Markdown + Local Context Packages

```bash
python3 scripts/pls_remember_me.py render --profile profile.json
```

This writes:

- `~/.pls-remember-me/out/<timestamp>-profile.md`
- `~/.pls-remember-me/out/<timestamp>-profile-evidence.md`
- `~/.pls-remember-me/out/personal-context-skill/SKILL.md`
- `~/.pls-remember-me/out/personal-context-skill/context-profile.md`
- `~/.pls-remember-me/out/claude-code-skill/personal-context/SKILL.md`
- `~/.pls-remember-me/out/claude-code-skill/personal-context/context-profile.md`
- `~/.pls-remember-me/out/claude-code-memory/CLAUDE.md`

To install the generated skill into Codex:

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/personal-context
cp -R ~/.pls-remember-me/out/personal-context-skill ~/.codex/skills/personal-context
```

To install the generated Claude Code skill:

```bash
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/personal-context
cp -R ~/.pls-remember-me/out/claude-code-skill/personal-context ~/.claude/skills/personal-context
```

For persistent Claude Code memory, review the generated file first, then append it to user memory:

```bash
mkdir -p ~/.claude
cat ~/.pls-remember-me/out/claude-code-memory/CLAUDE.md >> ~/.claude/CLAUDE.md
```

## Current v1 Support

Implemented:

- Claude Code `.jsonl` parsing
- Codex `rollout-*.jsonl` parsing
- ChatMemo `.txt` dump parsing
- streaming JSONL reading and early noise filtering
- redaction placeholders for secrets, auth URLs, device codes, terminal login lines, local paths, emails, and phone numbers
- path-free `public_ref` evidence references
- distillation packet generation
- generic downranking for long pasted source material in packet selection
- profile validation with evidence-ref checks
- `profile.md` rendering
- evidence appendix rendering
- `personal-context-skill/` rendering
- `claude-code-skill/` rendering
- optional `claude-code-memory/` rendering

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

Real logs, generated packets, generated profiles, and generated context packages should stay in gitignored or external local paths such as:

- `~/.pls-remember-me/out`
- `samples/out/`
- `local_dogfood/`

See [docs/architecture.md](docs/architecture.md) and [docs/v1-plan.md](docs/v1-plan.md) for the current implementation boundary.

## License

MIT
