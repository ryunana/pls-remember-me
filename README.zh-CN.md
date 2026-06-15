# pls-remember-me

[English](README.md) | [简体中文](README.zh-CN.md)

> 别再对每个新的 AI 会话重新介绍自己。

`pls-remember-me` 会把你过去纠正 AI 的高信号片段，蒸馏成一份有证据链的个人协作上下文种子。它扫描你本机 Claude Code / Codex 风格的对话日志，找出你纠正、约束、推翻或重新引导 AI 的关键片段，并整理成一份可追溯的蒸馏证据包。

然后，你把这份证据包交给自己选择的 AI 工具。AI 输出 `profile.json`；本项目负责校验它，并渲染出真正可用的上下文产物：

- 可直接粘贴使用的 `profile.md`
- 单独用于审计追溯的 `profile-evidence.md`
- 可安装到 Codex 风格 skill 目录里的本地 `personal-context-skill/` 包
- 可安装到 Claude Code 的本地 `claude-code-skill/` 包
- 可选的 Claude Code 长期 memory 片段 `claude-code-memory/CLAUDE.md`

这个项目不是聊天记录总结器。它的目标是产出第一份 personal context seed：你如何判断、如何取舍、希望 AI 怎样与你协作。

## 跑完 demo 后你会得到什么

运行完整合成 demo：

```bash
git clone https://github.com/ryunana/pls-remember-me.git
cd pls-remember-me
bash scripts/run_full_demo.sh
```

它只使用仓库里提交的合成日志和 `samples/demo-profile.json`，不会读取你的真实日志。

稳定输出会写到已被 git 忽略的 `samples/out/full-demo/`：

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

`result-card.md` 是一张适合截图传播的 demo 结果卡：

```text
┌──────────────────────────────────────────────┐
│  Personal Context Seed                       │
│  Input: synthetic Claude-style logs          │
│  Evidence: high-signal user corrections      │
│  Output: profile.md + evidence appendix      │
│  Packages: Codex skill + Claude Code skill   │
└──────────────────────────────────────────────┘
```

一条渲染后的规则长这样：

```markdown
### 用户要求先查证再判断，证据不足时明说不足，不用脑补选项替用户猜。

How the AI should behave: 回答前优先检索、运行验证或说明证据缺口；不要用未经验证的可能性替代结论。
When not to over-apply it: 创意发散、命名或头脑风暴任务可以先给候选方向，但仍要标注它们只是候选。
```

生成的 skill 会让 agent 先读取 `context-profile.md`；证据引用留在单独的 appendix 里用于审计，不会默认塞进每次会话上下文。

## 它不是另一个 memory backend

| 如果你想要... | 更适合用... | 原因 |
|---|---|---|
| 自动长期捕获、索引和召回 | memsearch / episodic-memory / claude-mem 这类 memory backend | 它们负责持续的记忆基础设施 |
| 给新 AI 工具准备一份干净的起始个人画像 | `pls-remember-me` | 它把历史纠正蒸馏成可移植的上下文种子 |
| 不默认上传日志，但保留证据链 | `pls-remember-me` | packet 在本地生成，由你决定给哪个 AI 看 |
| 搜索过去所有决策 | 语义 memory / search 系统 | `pls-remember-me` 刻意只选高信号摩擦片段，不收集一切 |

`pls-remember-me` 最适合在接入长期 memory 系统之前或旁边使用：先生成第一份个人协作上下文，审阅证据，再把渲染结果粘贴或安装到你想用的 agent 里。

## 它不会做什么

- 不上传你的日志。
- 不运行托管记忆服务。
- 不自动调用云模型。
- 不收集统计数据。
- 不把你的真实 profile 或真实日志提交进这个仓库。

你的真实数据只会留在本机，以及你明确选择用于蒸馏的 AI 工具里。

## 快速 demo

### 只跑 packet demo

```bash
bash scripts/run_demo.sh
```

这会验证本地流水线的前半段：

```text
samples/logs/ → summary.md + friction.jsonl + distillation_packet.md
```

### 跑完整合成 demo

```bash
bash scripts/run_full_demo.sh
```

这会验证公开端到端形态：

```text
samples/logs/
  → distillation_packet.md
  → samples/demo-profile.json
  → validate
  → profile.md + evidence appendix + installable context packages
```

### 冒烟测试

```bash
bash scripts/test_full_demo.sh
```

这会检查完整合成 demo 是否渲染出所有预期产物。

## 用你自己的日志运行

### 1. 生成蒸馏证据包

```bash
python3 scripts/pls_remember_me.py prepare \
  --input-dir ~/.claude/projects \
  --input-dir ~/.codex/sessions
```

默认输出目录：

```bash
~/.pls-remember-me/out
```

### 2. 让你选择的 AI 工具蒸馏证据包

打开生成的 `*-distillation_packet.md`，把内容粘贴给 Claude Code / Codex / 其他你信任的 AI 工具，并要求它严格遵循 packet 里的说明。

把 AI 输出保存为 `profile.json`。

### 3. 校验 profile

```bash
python3 scripts/pls_remember_me.py validate \
  --profile profile.json \
  --friction ~/.pls-remember-me/out/<timestamp>-friction.jsonl
```

如果校验失败，命令会打印一段可直接复制回 AI 的修订指令。

### 4. 渲染 Markdown + 本地 Context 包

```bash
python3 scripts/pls_remember_me.py render --profile profile.json
```

这会生成：

- `~/.pls-remember-me/out/<timestamp>-profile.md`
- `~/.pls-remember-me/out/<timestamp>-profile-evidence.md`
- `~/.pls-remember-me/out/personal-context-skill/SKILL.md`
- `~/.pls-remember-me/out/personal-context-skill/context-profile.md`
- `~/.pls-remember-me/out/claude-code-skill/personal-context/SKILL.md`
- `~/.pls-remember-me/out/claude-code-skill/personal-context/context-profile.md`
- `~/.pls-remember-me/out/claude-code-memory/CLAUDE.md`

安装生成的 Codex skill：

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/personal-context
cp -R ~/.pls-remember-me/out/personal-context-skill ~/.codex/skills/personal-context
```

安装生成的 Claude Code skill：

```bash
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/personal-context
cp -R ~/.pls-remember-me/out/claude-code-skill/personal-context ~/.claude/skills/personal-context
```

如果想作为 Claude Code 长期 memory 使用，先人工审阅生成文件，再追加到用户级 memory：

```bash
mkdir -p ~/.claude
cat ~/.pls-remember-me/out/claude-code-memory/CLAUDE.md >> ~/.claude/CLAUDE.md
```

## 当前 v1 支持范围

已实现：

- Claude Code `.jsonl` 解析
- Codex `rollout-*.jsonl` 解析
- ChatMemo `.txt` dump 解析
- JSONL 流式读取和早期噪声过滤
- 对 secrets、认证 URL、device code、终端登录行、本机路径、邮箱和手机号做占位符脱敏
- 不含本机路径的 `public_ref` 证据引用
- 蒸馏证据包生成
- packet 选材时对长篇粘贴材料做通用结构降权
- profile 校验和 evidence ref 检查
- `profile.md` 渲染
- evidence appendix 渲染
- `personal-context-skill/` 渲染
- `claude-code-skill/` 渲染
- 可选 `claude-code-memory/` 渲染

已知限制：

- demo 只覆盖合成的 Claude 风格日志。
- ChatMemo 解析器已有，但还没有公开样本覆盖。
- Hermes SQLite 尚未实现。
- daily / weekly observer 命令尚未实现。
- v1 是 axiom-first：更擅长捕捉判断原则，不擅长稳定提取身份、风格或领域标签。
- v1 是全量重跑，不是真增量记忆。
- validator 只检查结构和证据引用，不判断 axiom 是否真的有洞察力。

## 项目边界

这个仓库只包含机制和合成样本数据。

真实日志、生成的 packet、生成的 profile 和生成的 context 包应留在 gitignored 或仓库外的本地路径，例如：

- `~/.pls-remember-me/out`
- `samples/out/`
- `local_dogfood/`

当前实现边界见 [docs/architecture.md](docs/architecture.md) 和 [docs/v1-plan.md](docs/v1-plan.md)。

## License

MIT
