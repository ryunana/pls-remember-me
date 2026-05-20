# pls-remember-me

[English](README.md) | [简体中文](README.zh-CN.md)

> 别再对每个新的 AI 会话重新介绍自己。

`pls-remember-me` 是一个面向重度 AI 用户的本地工具。它会扫描你自己的 Claude Code / Codex 风格对话日志，找出你纠正、约束、推翻或重新引导 AI 的高信号片段，并整理成一份可追溯的蒸馏证据包。

然后，你把这份证据包交给自己选择的 AI 工具。AI 输出 `profile.json`；本项目负责校验它，并渲染出：

- 可直接粘贴使用的 `profile.md`
- 可安装到 Codex 风格 skill 目录里的本地 `personal-context-skill/` 包

这个项目不是聊天记录总结器。它的目标是产出第一份个人 context seed：你如何判断、如何取舍、希望 AI 怎样与你协作。

## 它不会做什么

- 不上传你的日志。
- 不运行托管记忆服务。
- 不自动调用云模型。
- 不收集统计数据。
- 不把你的真实 profile 或真实日志提交进这个仓库。

你的真实数据只会留在本机，以及你明确选择用于蒸馏的 AI 工具里。

## 不用个人数据先试一下

```bash
git clone <repo-url>
cd pls-remember-me
bash scripts/run_demo.sh
```

demo 使用 `samples/logs/` 下的合成日志，并把输出写到已被 git 忽略的 `samples/out/`：

- `*-summary.md`
- `*-friction.jsonl`
- `*-distillation_packet.md`

这只证明本地流水线能跑通。demo 数据刻意很小，只用于展示格式；真正价值来自你自己的历史对话。

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

### 4. 渲染 Markdown + Skill 包

```bash
python3 scripts/pls_remember_me.py render --profile profile.json
```

这会生成：

- `~/.pls-remember-me/out/<timestamp>-profile.md`
- `~/.pls-remember-me/out/personal-context-skill/SKILL.md`
- `~/.pls-remember-me/out/personal-context-skill/context-profile.md`

安装生成的 Codex skill：

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/personal-context
cp -R ~/.pls-remember-me/out/personal-context-skill ~/.codex/skills/personal-context
```

## 当前 v1 支持范围

已实现：

- Claude Code `.jsonl` 解析
- Codex `rollout-*.jsonl` 解析
- ChatMemo `.txt` dump 解析
- JSONL 流式读取和早期噪声过滤
- 占位符脱敏：`[SECRET]`、`[EMAIL]`、`[PHONE]`
- 不含本机路径的 `public_ref` 证据引用
- 蒸馏证据包生成
- profile 校验和 evidence ref 检查
- `profile.md` 渲染
- `personal-context-skill/` 渲染

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

真实日志、生成的 packet、生成的 profile 和生成的 skill 应留在 gitignored 或仓库外的本地路径，例如：

- `~/.pls-remember-me/out`
- `samples/out/`
- `local_dogfood/`

当前实现边界见 [docs/architecture.md](docs/architecture.md) 和 [docs/v1-plan.md](docs/v1-plan.md)。

## License

MIT
