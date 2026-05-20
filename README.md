# pls-remember-me

> 让 AI 别再说"你是谁来着？"

每换一个 AI 工具、每开一个新会话，你都要重新解释一遍自己是谁、怎么工作、什么不能碰。

`pls-remember-me` 扫你本机的 AI 对话日志，整理成可追溯证据包，再借助你**自己选择**的 AI
工具（Claude Code / Codex 等）蒸馏出一份个人 `profile.md`——"我是谁 / 我怎么判断 / 我希望
AI 怎么配合我"。你可以把它粘到任何新 AI 会话里。

**它不是聊天记录总结器**，不是替你托管记忆的服务。目标是帮重度 AI 用户启动自己的**个人
context infrastructure**：把散落在历史对话里的稳定判断原则显性化，后续持续积累。

---

## 30 秒看它干了什么（不用你的任何数据）

```bash
git clone <repo>
cd pls-remember-me
bash scripts/run_demo.sh
```

仓库自带 3 个合成 demo 会话（`samples/logs/`，20+ 条消息），脚本会跑一次完整的
ingest → friction → packet 流程。耗时 < 1 秒。

产物落在 `samples/out/`（gitignored，不会进你的提交）：
- `*-summary.md`——关键词分布、theme 命中、top friction 片段
- `*-friction.jsonl`——机器可读
- `*-distillation_packet.md`——可直接发给 AI 的蒸馏证据包（带 prompt + 严格 JSON 输出契约）

合成样本只够演示**格式**——真实价值在下一段。

---

## 用你自己的数据（真实路径）

```bash
# 1. 扫描你的 Claude Code / Codex 日志，生成证据包
python3 scripts/pls_remember_me.py prepare \
    --input-dir ~/.claude/projects \
    --input-dir ~/.codex/sessions

# 2. 把生成的 distillation_packet.md 整段发给 Claude Code 或 Codex，
#    让它按 packet 顶部的 prompt 输出严格 JSON，保存为 profile.json

# 3. 校验 AI 蒸出来的 profile.json
python3 scripts/pls_remember_me.py validate \
    --profile profile.json \
    --friction ~/.pls-remember-me/out/<时间戳>-friction.jsonl

# 4. 渲染成可粘贴的 profile.md
python3 scripts/pls_remember_me.py render --profile profile.json
```

`profile.md` 是最终产物——贴到任何 AI 工具的 system prompt / 项目 context 文件 /
第一条消息里，让它在和你协作前就理解你的判断方式。

### 几个事实

- **不上传**：项目方不托管、不收集、不默认上传你的真实对话。流水线只读 `--input-dir`，
  不再硬编码任何本机路径。
- **真实数据只在你本机和你主动选择的 AI 工具之间流转**。
- **默认产物落 `~/.pls-remember-me/out`**（用户级，gitignored）。
- **C9 失败回喂**：validator 不通过会打印一段可直接复制给 AI 的回喂指令模板，告诉它该改什么。
- **真实尺度参考**：本机一次扫 `~/.claude/projects` + `~/.codex/sessions`（约 70 个文件、几 GB），
  ingest 在 1.5 秒内完成；生成的 packet 约 10K token，在主流 AI 工具 context window 内。

---

## v1 当前能做和不能做

**能做**：
- 4 种来源解析：Claude Code (.jsonl) / Codex (rollout-*.jsonl) / Hermes / ChatMemo
  （demo 演示前两种）
- 流式读 + 早期噪声过滤（应对 Codex 单文件最大 250MB 的真实情况）
- 占位符脱敏（`[SECRET]` / `[EMAIL]` / `[PHONE]`），保留文本语义结构
- 公开引用 `public_ref`（不暴露本机路径、项目名、仓库名）
- axiom 校验：≥2 条证据、confidence 枚举、`evidence_refs` 必须真实存在

**不能做（v1 已知限制，留 v1.1）**：
- **只蒸"判断原则"**——你的角色定位、表达风格偏好、常用业务主题这些不会被单独立条目
  （它们会出现在 packet 的高信号片段里，但 axiom-first 的产物不会专门捕获）
- **跨次重蒸跨次不可比**——v1 全量重蒸，每次跑都重新扫历史；`first_seen` / `last_seen` /
  `count` 只反映本次语料的时间分布，不要把它们当作"这条偏好正在累积"
- **daily / weekly 子命令未上**——v1.1 会补，让 observer/reflector 形态在本地循环起来
- **网页端 AI 工具导出（ChatGPT / Claude.ai / DeepSeek / 豆包 / Kimi）暂不支持**

---

## 这跟女娲（nuwa-skill）什么关系

镜像。女娲蒸馏**别人**（名人、公开资料、一次性）；`pls-remember-me` 蒸馏**你自己**
（私有对话、可持续迭代、用户自选 AI 工具参与）。女娲给 AI 装别人的脑子，这个给 AI 装你自己的脑子。

## 设计边界

详见 [`docs/architecture.md`](docs/architecture.md) 和 [`docs/v1-plan.md`](docs/v1-plan.md)。
一句话：项目是流水线，skill 只是它的一种产物；仓库里永远没有可识别、可回溯的真实个人数据，
只有机制 + 公开示例语料。

## License

MIT
