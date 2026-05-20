# pls-remember-me v1 Plan

> 本文档只描述当前准备发布的 v1。旧版讨论、冻结规则、迭代史和未实现的扩展设想不再保留。
>
> 当前判断：v1 是一个能跑通的 personal context seed starter，不是完整的 context infrastructure。

## 1. v1 要解决什么

`pls-remember-me` 的 v1 目标很窄：

1. 从用户本机已有的 AI 对话日志里抽取高信号片段。
2. 把这些片段整理成可追溯、可脱敏、可交给 AI 的证据包。
3. 让用户用自己选择的 AI 工具蒸馏出 `profile.json`。
4. 校验 `profile.json` 的结构和证据引用。
5. 渲染成可粘贴到新 AI 会话里的 `profile.md` 和可安装的 personal context skill。

它不是聊天记录总结器，也不是托管记忆的服务。v1 只做第一份可用 context seed，重点是“让新会话更快理解这个用户的判断方式”。

## 2. 当前可运行链路

### 2.1 Demo 路径

```bash
bash scripts/run_demo.sh
```

输入：`samples/logs/` 中的合成 Claude Code 会话。

输出：`samples/out/` 中的三类文件：

- `*-summary.md`
- `*-friction.jsonl`
- `*-distillation_packet.md`

这个 demo 只证明格式和流水线能跑通，不证明真实蒸馏质量。

### 2.2 真实数据路径

```bash
python3 scripts/pls_remember_me.py prepare \
  --input-dir ~/.claude/projects \
  --input-dir ~/.codex/sessions
```

然后把生成的 `distillation_packet.md` 交给 Claude Code / Codex 等 AI 工具，让它按 packet 顶部 prompt 输出严格 JSON，保存为 `profile.json`。

```bash
python3 scripts/pls_remember_me.py validate \
  --profile profile.json \
  --friction ~/.pls-remember-me/out/<timestamp>-friction.jsonl

python3 scripts/pls_remember_me.py render --profile profile.json
```

默认真实输出目录是 `~/.pls-remember-me/out`。真实数据、真实画像和真实 skill 包不进入仓库。

## 3. 当前模块状态

| 模块 | 文件 | 当前状态 |
|---|---|---|
| CLI | `scripts/pls_remember_me.py` | 已实现 `prepare / validate / render` |
| ingest | `scripts/ingest.py` | 已实现日志扫描、解析、脱敏、去噪、摘要和 friction 输出 |
| packet | `scripts/packet.py` | 已实现 AI handoff packet 生成和 16K token 软上限 |
| validate | `scripts/validate.py` | 已实现 JSON 结构、confidence、evidence refs 校验和失败回喂提示 |
| render | `scripts/render.py` | 已实现 `profile.json` 到 `profile.md` 和 `personal-context-skill/` 的基础渲染 |
| demo | `scripts/run_demo.sh` | 已实现零数据 demo |

## 4. 当前支持的数据来源

v1 当前支持三种解析路径：

1. Claude Code `.jsonl`
2. Codex `rollout-*.jsonl`
3. ChatMemo `.txt` dump

说明：

- demo 只覆盖 Claude Code 样式的合成日志。
- Claude Code 和 Codex 已用本机真实日志 smoke 过。
- ChatMemo 解析器在代码里，但当前仓库没有公开样本覆盖。
- Hermes adapter 未实现，放到 v1.1。

## 5. 数据与隐私边界

v1 必须遵守这些边界：

1. 仓库永不提交真实个人对话、真实 profile、真实 packet、真实 skill 包、真实路径映射。
2. `samples/` 只能放合成样本，可以受真实 dogfood 启发，但不能可识别、可回溯。
3. 真实输出默认落到 `~/.pls-remember-me/out`。
4. 仓库内临时 dogfood 输出必须落在 `.gitignore` 覆盖的目录，如 `local_dogfood/`、`samples/out/`、`out/`。
5. 下游公开产物只能使用 `public_ref`，不能暴露本机路径、项目名或仓库名。
6. 项目方不托管、不收集、不默认上传用户数据；用户自己决定把 packet 发给哪个 AI 工具。

## 6. v1 已知限制

### 6.1 只蒸判断原则

当前 profile 是 axiom-first。它适合提取：

- 用户如何判断问题
- 用户如何取舍优先级
- 用户希望 AI 如何配合
- 用户反复纠正 AI 的边界

它不专门提取：

- 身份标签
- 表达风格
- 常用业务领域
- 工具偏好全景

这些内容可能出现在 evidence 里，但 v1 不会稳定产出独立条目。

### 6.2 信号提取仍偏 friction

当前 `ingest.py` 主要靠关键词命中抓高信号片段。它能覆盖很多“纠正 / 推翻 / 重做 / 边界声明”，但还没有完整拆出四类结构化信号：

- friction
- decision pattern
- boundary statement
- workflow preference

这会导致 profile 更像“用户如何纠正 AI”，而不是完整的个人 context map。

### 6.3 非增量

v1 是全量重蒸：

- 每次重新扫输入目录。
- 不维护跨次 `first_seen / last_seen / count` 的稳定状态。
- 不提供 daily / weekly 子命令。
- 不做 observer / reflector 循环。

### 6.4 校验只管机械合同

`validate.py` 只判断：

- JSON 是否合法
- 字段是否存在
- confidence 是否在枚举内
- evidence refs 是否格式正确
- refs 是否存在于 friction 文件中

它不判断 axiom 是否真的有洞察力，也不判断 profile 是否完整代表用户。

## 7. 发布前检查清单

push / release 前至少跑：

```bash
git status --short
bash scripts/run_demo.sh
python3 scripts/pls_remember_me.py --help
python3 scripts/pls_remember_me.py prepare --help
python3 scripts/pls_remember_me.py validate --help
python3 scripts/pls_remember_me.py render --help
```

同时确认：

- `git ls-files` 不包含 `samples/out/`、`local_dogfood/`、真实 `profile.json`、真实 packet、真实 skill 包。
- README 的“能做 / 不能做”与当前代码一致。
- `docs/architecture.md` 如果仍保留目标架构表述，必须明确它不是当前实现清单。

## 8. v1.1 优先级

发布后优先补这些，不在 v1 硬塞：

1. Hermes adapter：从 `~/.hermes/state.db` SQLite 抽取可用消息。
2. ChatMemo 公开样本和 demo 覆盖。
3. identity / style / domain 三类补充信号。
4. 更结构化的 signal extractor：拆出 friction / decision / boundary / workflow。
5. daily / weekly 子命令和最小 observer state。
6. canned `samples/EXPECTED.profile.json`，让 demo 可以闭环 validate / render。
7. 更清晰的空输入、全 noise 输入、非法 render 输入错误提示。

## 9. 不做什么

v1 明确不做：

- 中心化服务
- 自动上传用户日志
- Web UI
- 多人物画像
- 通用网页端 ChatGPT / Claude.ai / DeepSeek / Kimi / 豆包导出
- 真增量去重和跨次画像合并
- 自动调用云模型完成蒸馏
- 多 skill 格式输出

这些都不是当前发布阻塞项。
