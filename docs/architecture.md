# pls-remember-me Architecture

> 本文档描述当前 v1 的实际架构，不是历史计划，也不是 v1.1 目标架构。
>
> 当前 v1 是一个本地流水线：把用户本机 AI 对话日志整理成证据包，让用户用自己选择的 AI 工具蒸馏 `profile.json`，再由本项目校验并渲染成 `profile.md` 和本地 skill 包。

## 1. Product Boundary

`pls-remember-me` 要解决的问题是：用户每开一个新 AI 会话，都要重新解释自己是谁、怎么判断、怎么希望 AI 配合。

v1 只做第一份可追溯的 personal context seed：

1. 扫描本机日志。
2. 提取高信号用户片段。
3. 生成可交给 AI 的 distillation packet。
4. 校验 AI 产出的 profile JSON。
5. 渲染成可粘贴的 Markdown profile 和可安装的 personal context skill。

v1 不是完整的长期 memory backend，也不是自动化托管服务。

## 2. Hard Boundaries

这些边界不能破：

1. 仓库不提交真实个人数据、真实 profile、真实 packet、真实 skill 包、真实路径映射。
2. 项目方不托管、不收集、不默认上传用户日志。
3. 用户自己决定把 packet 交给哪个 AI 工具。
4. 公开产物只使用 `public_ref`，不暴露本机路径、项目名、仓库名。
5. 真实输出默认落到 `~/.pls-remember-me/out`。
6. 本项目本体不是 skill；v1 输出的是用户自己的 personal context skill 包。

## 3. Data Flow

```text
input dirs
  │
  ▼
scripts/ingest.py
  - detect source format
  - parse Claude Code / Codex / ChatMemo
  - filter system/tool/noise records
  - redact secrets / email / phone
  - emit summary.md + friction.jsonl
  │
  ▼
scripts/packet.py
  - rank keyword hits
  - clip snippets
  - enforce soft packet size cap
  - emit distillation_packet.md
  │
  ▼
user-selected AI tool
  - reads packet
  - produces profile.json
  │
  ▼
scripts/validate.py
  - checks JSON shape
  - checks confidence enum
  - checks evidence refs format
  - optionally checks refs exist in friction.jsonl
  - prints rewrite hint on failure
  │
  ▼
scripts/render.py
  - emits paste-friendly profile.md
  - emits personal-context-skill/
```

## 4. Runtime Paths

### Demo Path

```bash
bash scripts/run_demo.sh
```

Input: `samples/logs/`

Output: `samples/out/`

The demo proves the local pipeline and output format. It does not prove semantic distillation quality because the sample logs are synthetic and small.

### Real Data Path

```bash
python3 scripts/pls_remember_me.py prepare \
  --input-dir ~/.claude/projects \
  --input-dir ~/.codex/sessions
```

Default output: `~/.pls-remember-me/out`

The user then manually gives the generated `distillation_packet.md` to an AI tool and saves the result as `profile.json`.

## 5. Current File Layout

```text
pls-remember-me/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── architecture.md
│   └── v1-plan.md
├── scripts/
│   ├── ingest.py
│   ├── packet.py
│   ├── pls_remember_me.py
│   ├── render.py
│   ├── run_demo.sh
│   └── validate.py
├── samples/
│   └── logs/
├── adapters/
│   └── .gitkeep
└── templates/
    └── .gitkeep
```

`adapters/` and `templates/` are placeholders. Current parser logic lives inside `scripts/ingest.py`.

Rendered real outputs are not committed. By default they live under `~/.pls-remember-me/out`, including:

- `<timestamp>-profile.md`
- `personal-context-skill/SKILL.md`
- `personal-context-skill/context-profile.md`

## 6. Source Support

Current v1 parser support:

| Source | Status | Notes |
|---|---|---|
| Claude Code `.jsonl` | implemented | demo uses synthetic Claude-style logs; real logs smoke-tested locally |
| Codex `rollout-*.jsonl` | implemented | real logs smoke-tested locally; noise-heavy records are filtered |
| ChatMemo `.txt` dump | implemented but not sample-covered | parser exists; no public sample in repo yet |
| Hermes SQLite | not implemented | planned for v1.1 |

## 7. Internal Contracts

### Message Contract

`ingest.py` normalizes parsed messages into a small internal shape:

- `source`
- `timestamp`
- `role`
- `text`
- `public_ref`

Only user messages are kept by default because v1 is preference / judgment mining, not conversation summarization.

### Friction JSONL Contract

Each line in `*-friction.jsonl` contains:

- `source`
- `timestamp`
- `role`
- `keywords`
- `text`
- `public_ref`

This file is the evidence source for `packet.py` and optional reference checking in `validate.py`.

### Profile JSON Contract

`profile.json` is produced by the user-selected AI tool. v1 expects:

- top-level `version`
- top-level `axioms`
- each axiom has `statement`
- each axiom has `confidence` in `high | medium | low | unstable`
- each axiom has at least two `evidence_refs`

`执行要求` and `反例` are recommended and rendered when present, but they are warning-level fields in the current validator.

## 8. Privacy Design

### Redaction

`ingest.py` replaces common sensitive patterns with placeholders:

- `[SECRET]`
- `[EMAIL]`
- `[PHONE]`

The goal is to preserve sentence structure while removing obvious secrets and personal contact details.

### Public Refs

`public_ref` is constructed from:

- source name
- short hash of the local file path
- line / block / uuid anchor

It intentionally avoids raw file paths. It is suitable for evidence linking inside packet and profile artifacts.

## 9. Skill Package Output

`scripts/render.py` writes a stable skill package directory:

```text
~/.pls-remember-me/out/personal-context-skill/
├── SKILL.md
└── context-profile.md
```

`SKILL.md` tells the AI to load `context-profile.md` first. `context-profile.md` contains the rendered axioms and evidence refs from the validated profile.

Users can install it into Codex-style skill directories with:

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/personal-context
cp -R ~/.pls-remember-me/out/personal-context-skill ~/.codex/skills/personal-context
```

## 10. Known Architecture Limits

v1 knowingly does not include:

- daily / weekly commands
- observer / reflector loop
- true incremental state
- task routing or context selection
- web UI
- automatic cloud model calls
- Hermes SQLite parsing
- complete identity / style / domain extraction
- structured signal classes beyond keyword-driven friction snippets

These are v1.1+ candidates, not current v1 commitments.
