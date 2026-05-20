# pls-remember-me · v1 Plan

> **状态：FROZEN（v0.8.5 起，v0.9 二次重铸后重新冻结）。**
>
> **解冻历史**：v0.8.6 = S-1 真实日志事实回写。**v0.9 = 路线图重铸**：对比老项目 `personal-context-infrastructure` 后确认 v1 范围错位——老项目已是 yage context infrastructure 的 v0 实现，而 v1 计划只做 bootstrap seed 是自我缩水。v0.9 把 v1 定位升级为"个人 context infrastructure 启动器"，激进吃老项目（抽 export / observer / reflector / THEME_RULES / axiom 结构 / 真实输出样本）。
>
> **下一步硬动作**：S-0.5 老项目抽提（不再修订本文档）。FROZEN 规则不变：只接受 S-1/实现事实回写、自相矛盾修正、实现暴露的具体问题；不接受纯概念 critique。
>
> 本文档是什么：v1 实现前的**精细化计划**。**v0.8.5 后停止抽象打磨，剩余待确认项由 S-1 真实日志侦察结果 / v1 实现过程回写**。
>
> 上层依据：[`architecture.md`](architecture.md)（边界宪法，本文档不再挑战）。
>
> 维护规则：所有决策标 **🟢已定** 或 **🟡待确认**；🟡 项必须列出选项 + 各选项的代价 + 建议默认，方便后续讨论收敛。一旦拍板，🟡 改为 🟢 并删掉选项列表。

---

## 0. 怎么用这份文档（给后续 AI 工具的读法）

- 第 1–3 节是**背景与已定边界**，不要在这些点上重新讨论或挑战，直接当事实采信。
- 第 4 节起是**待精细化的内容**，每个待确认项都欢迎挑战、补选项、给反例。
- **v0.8.5 起 plan 进入 FROZEN 状态**：冻结期间只允许回写 S-1 真实日志事实、修正文档自相矛盾、补 v1 实现暴露的具体问题；**不接受纯概念 critique 与又一轮抽象打磨**。再加一版 v0.8.x 改写之前，先问"这条修订有没有真实输入证据支撑"。
- 用户是产品经理，不是工程师。技术内容要用产品语言讲（用"对接规范/接口口径"代替"schema/interface"；用"插件位"代替"adapter pattern"）。
- 决策遵循用户已蒸出来的偏好：直接推进、范围控制、边界清楚、禁止脑补、可落地。
- 章节内"已定的产品决策"是讨论收敛后的结论，挑战要给充分理由；"待磨的实操细节"是开放问题，欢迎补选项。
- **关键设计原则在 §1.5（目标用户与设计原则）**。每次"是不是该加个 X 让用户更方便"的提议出现时，先对照 §1.5 那条原则判定。

---

## 1. 项目定位（🟢已定）

### 1.0 初心：不是总结聊天记录，而是启动个人 context infrastructure

本项目来自对 [yage.ai/context-infrastructure](https://yage.ai/context-infrastructure.html) 的产品化回应。那篇文章真正指出的问题是：AI 默认会回到大众平均答案；要让 AI 更像理解你判断方式的合作者，关键不是换模型，也不是写几句更长的 prompt，而是把你长期行为里稳定出现的判断原则、协作偏好、边界意识和反复纠错，沉淀成可被 AI 读取的上下文基础设施。

用产品经理能听懂的话讲：

- **不是**：把聊天记录总结成"个人简介"。
- **而是**：从真实协作痕迹里找出"这个人怎么判断、怎么取舍、怎么要求 AI 配合"，形成一份能复用、能追溯、后续能继续迭代的个人 context seed。

完整的 context infrastructure 应该包括四层：大量积累、分层提炼、按需加载、循环更新。v1 不做完整系统，只做启动器：先从 Claude Code / Codex 历史对话里蒸出第一版可用、可追溯的 context seed。

因此，v1 的 demo 不是证明"我们会总结聊天记录"，而是证明：**从历史协作痕迹里，可以提炼出几条有证据支撑的稳定判断原则，让下一个 AI 会话更快贴近用户的判断口径。**

### 1.1 一句话
让 AI 别再每次都问"你是谁来着？"——把你和各种 AI 工具的历史对话，借助**用户自己选择的 AI 工具**蒸馏成第一份个人 context seed："我是谁 / 我怎么判断 / 我希望 AI 怎么配合我"，输出可直接喂给任何新 AI 会话。

### 1.2 与女娲（nuwa-skill）的镜像关系

| 维度 | 女娲 | 本项目 |
|---|---|---|
| 蒸馏对象 | 别人（名人，公开资料） | **你自己**（私有对话） |
| 数据来源 | 系统自己抓 | 用户本地导出 / 整理 |
| 次数 | 一次性 | **持续迭代** |
| 运行 | 抓公开数据 | **用户本机项目 + 用户自选 AI 工具，隐私边界是卖点** |
| 传播钩子 | 名人名字本身就是钩子 | 名字（pls-remember-me）+ 反差对照女娲 |

### 1.3 "跑通"的定义（v0.9 改：行为留存为主）

**不是 star 数**（那是女娲形状的指标，对镜像项目结构上不成立）。

**v0.9 起改为行为留存为主指标**（理由：v1 = infrastructure 启动器，一次反馈 ≠ 真嵌入工作流）：

**主指标**：
- 一个非熟人在自己的日志上跑出来，**用了一周还在用**——daily / weekly 子命令至少跑过两次，或 observation / reflection 文件持续更新。

**辅助信号**（任一仍然算正面信号，但不替代主指标）：
- 反馈这改变了他和 AI 协作的方式（一次反馈，v0.8 老指标）
- 第一条主动 inbound（合作 / 求助 / 引用）

**测量限制**（必须坦诚承认）：项目方无中心化埋点，行为留存只能靠用户主动报数据 / GitHub 活跃度 / issue 提到具体使用场景间接看。信号到达比 star 数还慢。**§2.3 v1.1 触发条件依然是"§1.3 跑通后启动"，不动**。

### 1.4 卖点（🟢已定）
**"别再对每个新 AI 会话/工具重新解释你是谁。"**

不用"distill yourself/AI infrastructure"这种抽象词。

对外说人话时，第二层解释是：**不是让 AI 记住你的所有事实，而是让 AI 更快理解你的判断方式。**

### 1.5 目标用户与设计原则（🟢已定）

**目标用户**：重度多工具 AI 用户。能 `git clone` 跑开源项目、能跑 `python3` 脚本、能找到自己各工具的日志目录。

**核心设计原则——"不为非目标用户加便利 hedge"**

能用 GitHub 的人天然有技术下限。不要为"用不来命令行的人"加兜底功能。这条原则的具体含义是拒绝下面这些"为了让用户更省事"的提议：

- ❌ 包 `npx` 壳让用户不用敲 `python3`
- ❌ 加"从 ~/.claude、~/.codex 拷日志"的 collect 脚本（用户自己 `cp` 即可）
- ❌ 加 YAML 配置文件（用户写 shell alias / `.envrc` 更原生）
- ❌ 多平台日志同目录混放时自动识别（用户自己分子目录 / 多次传 `--input-dir`）
- ❌ skill 包同时输出 Claude / Codex 多种格式（v1 出一种，用户要别的自己改）
- ❌ "为了让用户不用敲长命令"包一个 npm 或 shell wrapper（增加分发复杂度，不解决任何用户能力问题）

**三个例外**：

1. **影响"零数据 30 秒看到 demo"承诺的环节**——那是冷启动核心，可以适度便利化（如 `samples/` 内置语料 + `run_demo.sh` 一键脚本）。
2. **输入验证 + 清晰错误信息**——不属于便利 hedge，属于产品质量。例：用户传一个空目录或格式不对的目录时，应该明确报"找到 0 个可解析的 jsonl 文件，期望 claude_code / codex 格式，参考 README 的导出方式"，而不是默默跑出空画像。这条豁免保护"第一批非熟人失败时能分清是产品 bug 还是输入问题"。
3. **数据完整性 / 失败可调试性 / 文本语义保留**——不属于便利 hedge，属于产品质量。例：脱敏用 `[EMAIL]` 占位符而不是删除（保留文本语义结构，避免下游 LLM 读破句）；高信息片段必须能追溯回原始消息位置（失败可调试）；C2 字段必须带稳定 ID、公开引用 `public_ref` 和仅本机审计用的 `raw_ref`（数据完整性 + 隐私边界）。这条豁免保护"画像产物作为一手证据可信"。

### 1.6 运行边界：不是离线工具，是用户自选 AI 工具参与的蒸馏流程（🟢已定）

本项目不是"脚本离线独立完成所有理解"。更准确的形态是：

1. **本仓库负责机制**：日志适配、清洗脱敏、高信息片段提取、证据包结构、蒸馏提示词、输出模板、demo 样本和防泄漏边界。
2. **用户自己的 AI 工具负责/参与理解和总结**：v1 主路径先限定为 Claude Code / Codex，因为 v1 的信息采集也只适配这两类本地日志，用户在同一类工具里处理 `distillation_packet.md` 最容易闭环。Cursor / OpenCode / 网页端 ChatGPT / Claude / DeepSeek / 豆包 / Kimi 等不被排除，但 v1 不把它们当主路径承诺；尤其网页端工具涉及复制粘贴、文件读取、上下文长度和隐私边界，放到后续版本再专门打磨。
3. **项目方不托管、不收集、不替用户上传真实数据**：真实对话只在用户本机和用户主动选择的 AI 工具之间流转。不能再把这件事说成"不联网 / 不调云"，因为用户可能主动选择联网 AI 工具。
4. **v1 先支持最容易稳定适配的本地日志**：Claude Code + Codex；长期定位从一开始就是"多 AI 工具历史对话画像蒸馏"，后续扩展到更多 CLI / IDE / 网页端导出。

### 1.7 三段路线图（🟢已定）

用 yage 原文的标准看，本项目不能把 v1 包装成完整 context infrastructure。路线图必须切成三段：

| 阶段 | 产品名 | 解决什么 | 明确不解决什么 |
|---|---|---|---|
| **v1**（v0.9 重铸）| **个人 context infrastructure 启动器** | 把老项目 `personal-context-infrastructure` 脱掉个人内容 + 公开化 → 陌生人可跑版本。包含 4 source ingest + signal extraction + axiom 输出 + **daily / weekly observer 雏形（不强制 cron）** + AI handoff 协议 + 真实输出样本 | 不做按需加载 / 任务路由 / 多 context 切换；不做循环更新自动化层（用户自己装 cron / Codex Automations）；不做中心化托管；不自动上传 |
| **v1.1** | **Dogfood 反馈打磨** | 用第一批非熟人反馈调 reflector / axiom 结构；按需补 Hermes / ChatMemo 流畅度（v1 已有代码但用户体验粗糙处）；尝试更多 AI 工具的 handoff 路径 | 不急着做通用 web UI；不做中心化托管 |
| **v2** | **长期循环** | 按需加载（任务路由 / 多 context 切换）+ 真增量去重 + 循环更新（context 用过后反哺新 context）| 不做"一键替你变深刻"的伪承诺 |

这条路线图的作用是防止两个方向的误判：

1. **过度收缩**：把 v1 做成"聊天记录总结器"就停了。
2. **过度膨胀**：在 v1 就硬塞长期任务系统、路由、自动增量、web UI，导致第一版跑不通。

---

## 2. 已定的边界（🟢，不再讨论）

### 2.1 第一原则（违反即架构错）

1. 仓库永不包含可识别、可回溯的真实个人数据，只有机制 + 公开示例语料。示例语料可以受真实 dogfood 启发，但必须经过脱敏、改写、结构重组、场景替换和多次合成化，不能让外部读者反推出真实人、真实项目、真实路径或真实对话。
2. 项目是流水线，不是 skill。skill 只是流水线的一种产物。
3. 无中心化服务：项目方不托管、不收集、不默认上传真实数据；用户可主动选择自己的 AI 工具处理自己的数据。
4. 零数据可演示：陌生人 clone 后一条命令、30 秒看到产物。
5. v1 是第一版 context seed，不是完整 infrastructure：窄 loop 跑通优先。

### 2.2 三层边界

| 层 | 是什么 | 在本仓库 |
|---|---|---|
| **L1 流水线** | 把对话日志 ETL 成画像的批处理（脚本 + CLI） | ✅ 核心 |
| **L2 产物** | 蒸出来的画像（可粘贴的 md / 用户自带数据渲染出的 skill 包） | ⚠️ 只产**示例**产物；真实产物落用户本机 `OUT_DIR` |

**项目本体不是 skill，没有 L3 分发壳。** 安装方式是 `git clone` + `python3 scripts/...`。理由：本项目活儿发生在批处理时，而 `npx skills` 生态装的是"AI 推理时调用的能力"——形态不匹配。`npx skills add` 形态只出现在 L2 输出（用户蒸出来的画像 skill 包，是数据 + SKILL.md），**不是装项目本身**。

判定规则：**"别人也能用的机制"才进仓库；"关于你这个人的内容"永不进**。

### 2.3 v1 硬切线

- **要做（v0.9 重定义，主线 = 抽老项目而不是从零写）**：
  1. **抽老项目 `export_ai_chats.py`** → C1 adapter（`--input-dir` 解耦本机硬编码、流式读、早期过滤、4 source 默认）。v1 adapter 数从 v0.8.5 的 2 个**回到 4 个**：Claude Code + Codex + Hermes + ChatMemo（老项目都已实现）。ChatMemo 文档化为 "user-provided text dump"，demo 范围只覆盖前三个 jsonl source。
  2. **抽老项目 `extract_observations.py`** → 信号提取 + observation 写入（v0.9 起 C3 不再"信号提取脚本从零写"）
  3. **抽老项目 `weekly_reflection.py`** → 周度 reflection 草稿生成（feeds C4 / AI handoff）
  4. **抽老项目 `THEME_RULES`** 5 类（agent-work / content-evidence / product-work / writing-style / runtime-accountability）作为 C8 默认词典，通用化处理
  5. **抽老项目 axiom 结构**（置信度 / 执行要求 / 反例 三件套）作为 C4 默认 schema **minimum viable**；plan v0.8.6 七字段降为 stretch goal（validator 不达成给 warning，不 fail）
  6. **抽老项目 `distilled-profile-2026-05-09.md` + 一份 axiom 文件**，做轻脱敏（删姓名 / 公司 / 客户名 / 真实项目名，保留判断原则本身）放进 `samples/expected-real-output/`——这是 v0.9 最大产品价值新增：陌生人 30 秒不仅看到合成 demo，还看到"真实使用了一个月的人最终长什么样"
  7. **新增 C9 AI handoff 协议**（packet 分片、超长策略、回喂指令模板，daily / weekly 两种 packet 形态）
  8. **新增 daily / weekly 子命令**（observer state 文件 `state/processed_fragments.json` 抽自老项目；不强制 cron，README 分"试一次" / "真用" 两段说明）
  9. **新增**：MIT 公开 README + 陌生人 onboarding 流程

- **v1 做到的层级（v0.9 改）**：**个人 context infrastructure 启动器**。提供从积累 → 提炼 → axiom 输出的完整链路（reflector / axiom 合并仍需 AI handoff 帮忙）。不再说"bootstrap seed"。
- **工作量预估**：scope 看起来扩了，但**增量代码量比 v0.8 计划低约 60%**——大部分代码不是新写，是从老项目抽 + 去本机硬编码 + 个人内容剥离。
- **v1.1 加**：Hermes Agent adapter（用户自己 dogfooding 用；v1 demo 不带，因为目标用户大多没用过 Hermes，私有结构会稀释通用感）；更多来源的积累；启发式聚类换 LLM 实验分支。
- **v1.1 触发条件**：**§1.3 跑通后才启动 v1.1**。如果 v1 发布 6 周仍未拿到 §1.3 信号，**做复盘判断"为什么没有跑通信号"，不自动扩到 v1.1 范围**。这条修正 v0.8.4 之前 "6 周取最早" 口径——避免 plan 一边把 §1.3 当硬指标、一边给自己留 6 周 fallback 的矛盾。
- **v2 加**：Observer / Reflector / Axiom 式长期分层系统 · 任务路由与按需加载 · 循环更新 · 真增量与去重流水线。
- **后续来源方向**：OpenClaw / QClaw 衍生体 / Cursor / OpenCode / Gemini CLI / ChatMemo / 网页端 ChatGPT / Claude / DeepSeek / 豆包 / Kimi 等导出或整理格式。
- **不做（= v2+ 或永不做）**：中心化托管服务 · 自动上传处理 · 多人物画像 · web UI。
- **永不做**：把个人产物提交进仓库 · 项目方默认收集 / 上传 / 托管用户真实对话。

### 2.4 与母体项目（`personal-context-infrastructure`）的关系

模型 A：**一次性抽干净机制，之后两边独立演进**。

| 类别 | 处理 |
|---|---|
| 过来 | `scripts/` 逻辑（去本机硬编码）、skill 壳、axioms 通用结构 |
| 永不过来 | `contexts/`、`state/`、`logs/`、`*-friction.jsonl`、`chatmemo_raw/`、绑本机路径的 cron |
| 新仓库独有 | `samples/` 公开示例语料 + `EXPECTED.md`、面向陌生人的 README、LICENSE、一键 demo 脚本 |

已知代价：脚本改进要手动两边同步，会漂移。等 v1 拿到第一个非熟人反馈再决定是否收敛成模型 B（私有实例反过来依赖本开源工具）。

---

## 3. 模块与对接规范（🟢框架已定）

### 3.1 模块对照表（PM 视角）

把"对接规范"理解成模块之间**谁管什么、传什么字段**——和产品里"AI 助手 vs 业务页面"分边界是一回事。

| # | CLI 里叫 | 说人话 | 干什么的 |
|---|---|---|---|
| C1 | Source + Adapter | **平台插件位** | 新增 AI 工具就插一个解析器，主流程不动 |
| C2 | NormalizedMessage | **统一对话卡** | 各平台原始日志先翻译成标准卡，下游只认这张卡 |
| C3 | SignalExtractor | **高信息信号提取 / 证据包预处理** | 挑出"你纠正/推翻 AI 的地方"，同时保留反复决策、边界声明、优先级取舍等能体现判断方式的片段，整理成可交给用户 AI 工具的证据包 |
| C4 | ProfileModel | **画像数据结构** | 用户 AI 工具蒸出来的画像长什么样，每条结论带出处 |
| C5 | Renderer | **导出器** | 同一份画像 → 多种格式产物 |
| C6 | Redactor | **脱敏过滤** | API key / 邮箱 / 姓名等进流水线前擦掉 |
| C7 | PipelineState | **增量记忆** | 跑过的对话别再重蒸（v1 不做，留位置） |
| C8 | Config | **配置文件** | 用哪些插件 / 哪些规则 / 产物放哪 |
| C9 | AIHandoffProtocol | **人工交接协议** | packet 怎么给 AI、JSON 不合格怎么回喂、超长怎么分片——v1 真实路径的一半（v0.8.5 升 P0） |

### 3.2 数据流

```
本地日志（--input-dir）
   │   C1 平台插件位 → 翻译成
   ▼
[C2 统一对话卡]
   │   C6 脱敏过滤
   ▼
清洁对话
   │   C3 高信息信号提取
   ▼
高信息片段 / 证据包
   │   C9 人工交接协议（packet 分片 / 切到 AI / 失败回喂指令）
   ▼
用户自选 AI 工具按本项目 prompt 蒸馏（脚本只做预处理与约束）
   │   C9 回喂控制环：validator 失败 → 回喂指令 → 重蒸
   ▼
[C4 画像数据结构]
   │   C5 导出器
   ▼
产物（OUT_DIR/，本机，gitignored）
（C7 增量记忆贯穿全程；C8 配置全局）
```

### 3.3 优先级（按"改它的代价"排，不按工作量）

| 优先级 | 模块 | 理由 |
|---|---|---|
| **P0** | C2、C4、**C9** | 整条流水线的脊柱 + 人工交接路径。改它们 = 全链路或 UX 重写。v0.8.5 把 C9 升 P0：handoff 是 v1 非熟人能否跑通的核心 UX。 |
| **P1** | C1、C3、C5、C6、C8、**C7（v0.9 升级）** | v1 要有，但实现可以薄。**v0.9 C7 从 P2 升 P1**：daily 子命令需要 observer state 文件 `state/processed_fragments.json` 支撑增量（抽自老项目），非完整真增量；完整增量仍留 v2。 |
| **P2** | （v0.9 起 C7 已升 P1，本行空）| — |

### 3.4 扩展矩阵（架构对不对的检验工具）

**判定规则：任何一个"未来想加的东西"，如果要动两个以上模块，说明 C1–C8 边界画错了，要重新切。**

| 未来要加 | 只改这一个 | 其他模块 | 在 v1 体现为 |
|---|---|---|---|
| Hermes Agent (v1.1) / OpenClaw / QClaw / ChatMemo / Cursor / 网页端 ChatGPT/DeepSeek/豆包/Kimi 解析 | C1 加一个插件 | 不动 | C1 接口定好，v1 只塞 Claude Code + Codex |
| 接入更多 AI 蒸馏方式（本地模型 / 云 API / 不同网页端）| C3 prompt / C4 渲染约束扩展 | C2 字段不动 | v1 已允许用户自选 AI 工具；项目不内置统一云调用 |
| Cursor rules / AGENTS.md 导出 | C5 加一个导出器 | 不动 | C5 v1 只导可粘贴 md（+ 一个 skill 包）|
| 加脱敏规则（邮箱/手机号/地址等）| C6 加一条规则 | 不动 | C6 v1 做 API key + 邮箱 + 手机号占位符 |
| 真增量重蒸 | C7 实现 + ingest 加滤网 | C4 字段完全不动 | C7 v1 空实现 |
| 多人物画像 | C8 配置多份 + OUT_DIR 分目录 | 蒸馏逻辑跑多次 | v1 单人物 |

---

## 4. P0 核心决策（🟢主要方向已定，🟡实操细节待磨）

> 这一节的两个模块（C2 统一对话卡、C4 画像数据结构）是整条流水线的脊柱，改一个 = 全链路重写。所以**字段不是讨论主体，产品决策才是**。字段表只作附录，用来落地决策。

### 4.1 C2 统一对话卡

#### 4.1.1 这一节在解决什么产品问题

类比 HR SaaS 里的"标准简历模板"：候选人简历来自 BOSS、智联、内推、PDF，格式全不一样。你不会让"面试评分页"自己去认每种格式——你会先做一个标准模板，所有外部简历都先翻译过来，下游所有页面只认这个模板。

C2 就是干这事。Claude Code 和 Codex 两家的对话日志格式完全不一样（字段名、嵌套结构、什么算"一条消息"都不同）。我们做一个统一的"对话标准格式"，先把两边日志都翻译过来，下游所有模块（摩擦提取、蒸馏、导出）就只用应付这一种格式。v1.1 加 Hermes Agent 时，再多写一个 adapter 即可，主流程不动。

#### 4.1.2 已定的产品决策（🟢）

**🟢 决策 1：字段策略——越精细越好，但分主干 vs 扩展**

理由：未来要扩展到 OpenClaw / QClaw / 网页端 GPT、DeepSeek、豆包、Kimi 等更多平台，字段不精细会让后续平台的特有信息丢失。

实现上分两层避免"精细变累赘"：
- **主干字段**：各平台都能稳定填的（谁说的、说了什么、什么时候、什么会话）。这些是字段表里的"必须"项。
- **扩展字段**：平台填不上就 `null`，不强制——这样精细化不会让 v1 adapter 难写。

**🟢 决策 2：平台特异字段一律塞 `meta` 逃生舱，绝不上浮顶层**

下游模块只读 C2 顶层字段。Codex 有但 Claude Code 没有的怪字段，全塞 `meta`。

这条对应你"边界清楚，本系统职责不串"的核心偏好——上浮就意味着下游必须知道"原始平台是谁"才能读，扩展性彻底废掉。

**🟢 决策 3：结构性路径字段在 C2 adapter 阶段整字段丢弃，不进 `meta`、不进 `raw_ref`、不进任何下游**（S-1 v0.8.6 新增）

S-1 发现的结构性路径泄漏点：
- Claude Code：顶层 `cwd`、`gitBranch`、**项目目录名本身**（编码了完整文件系统路径，含 iCloud / Vault / 项目名）
- Codex：`session_meta.payload.cwd`、`turn_context.payload.cwd`、`base_instructions`

这些是**字段级别的路径泄漏**，不是文本里偶尔出现的路径——C6 文本脱敏不能覆盖。adapter 必须在解码原始日志时就**整字段丢弃**：

- 不进 C2 主干字段
- 不进 `meta` 逃生舱（一旦进了 meta，下游就有概率把它带到 packet/profile/samples）
- 不进 `raw_ref` 字符串（`raw_ref` 仅保留 `source` + `session_id` + `file_line_offset` 的最小本机审计三元组，**不含路径**）

如果将来发现某些路径字段确实需要（如 per-project axiom 聚类），由 C8 配置显式 opt-in，**默认丢弃**。

#### 4.1.3 v1 字段清单（附录性质，是上面两条决策的具体落地）

| 字段 | 主干 / 扩展 | 干嘛用 | 备注 |
|---|---|---|---|
| `schema_version` | 主干 | 字段以后改了也能兼容 | 例 `"v1.0"`，每次破坏性改字段就升版本 |
| `source` | 主干 | 这条来自哪个工具 | 枚举：v1 = `claude_code` / `codex`；v1.1+ = `hermes_agent` / `openclaw` / `chatgpt_web` / ... |
| `session_id` | 主干 | 同一次会话的消息能聚合 | 由 adapter 从原始日志提取 |
| `message_id` | 主干 | 整条流水线里每条消息的稳定 ID | 构造规则 **adapter-specific**（S-1 v0.8.6 修正）：Claude Code 直接用原生 `uuid`（DAG 节点 ID，每行唯一）；Codex 构造 `codex:{session_id}:{file_line_offset}`。下游只要求字符串稳定唯一，**不强求统一构造规则** |
| `parent_message_id` | 主干（可空）| 父消息引用（S-1 v0.8.6 新增）| Claude Code 提供原生 DAG（`parentUuid`），含 sidechain 并行支线；Codex 线性会话填 `null`。`turn_index` 无法表达 sidechain，**必须并存而非替代** |
| `turn_index` | 主干 | 这条消息在会话里的位置（从 0 起）| "上一条 assistant + 当前 user 纠正"配对靠它；在有 DAG 的平台（Claude Code）作为辅助，主索引用 `parent_message_id` |
| `raw_ref` | 主干（仅本机审计） | 指回原始日志文件位置 | 例 `path/to/file.jsonl:42`（文件 + 行号），只允许留在本机中间产物 / debug 日志 / gitignored 输出里 |
| `public_ref` | 主干 | 可进入 packet / profile / samples 的公开引用 | 例 `claude_code:session_hash:42` 或 `codex:2026-05-demo-a:17`；不含本机路径、项目名、仓库名 |
| `role` | 主干 | 谁说的 | 枚举：`user` / `assistant` / `tool` / `system` / `developer`（S-1 v0.8.6 新增 `developer`：Codex 真实日志有此角色，承载 system prompt，median ≈ 7KB/条；v1 默认过滤但 schema 必须收，否则解析报错）|
| `text` | 主干 | 消息内容 | 清洗过的纯文本 |
| `ts` | 主干 | 时间戳 | ISO 8601；时序分析 + "持续累积"都靠它 |
| `is_tool_artifact` | 主干 | 是不是工具调用日志 | `true` 的会被过滤；区分"你说的话"和"系统日志" |
| `tool_artifact_type` | 扩展（仅 `is_tool_artifact=true` 时填）| 工具产物子类型（S-1 v0.8.6 新增）| 枚举（至少 6 种）：`tool_use` / `tool_result`（Claude Code 内联）/ `function_call` / `function_call_output` / `reasoning` / `thinking`。判断规则两边不一致，由 adapter 各自处理 |
| `lang` | 扩展 | 语言 | `zh` / `en` / ...；不一定每条都识别 |
| `meta` | 主干（永远在，可为空字典）| 平台特异字段逃生舱 | **绝不上浮成顶层字段** |

#### 4.1.4 待磨的实操细节（🟡）

- [ ] `lang` 字段 v1 要不要识别？怎么识别（按文件名 / 启发式 / 不识别留 null）？
- [ ] `session_id` 在 Codex / Claude Code 日志里都能稳定取到吗？取不到时怎么兜底（用文件名 + 行号？）？
- [x] ~~`is_tool_artifact` 的判断规则在三个平台是否一致？要不要再加一个 `artifact_type` 区分 tool_use / tool_result / system？~~ → 已定（S-1 v0.8.6）：**必须加 `tool_artifact_type` 字段**，枚举 6 种（见 §4.1.3 字段表）。判断规则两边不一致，由 adapter 各自处理。
- [x] ~~工具调用产物（`tool_use` / `tool_result`）整段丢，还是保留但标 `is_tool_artifact=true`？~~ → 已定（S-1 v0.8.6）：**C2 阶段保留并标记 `is_tool_artifact=true` + `tool_artifact_type`**（保留可调试性、可追溯性）；**C3 阶段激进丢弃**（噪声/信号比可达 24000:1，见 §5.2）。
- [ ] **Codex `compacted` records**（S-1 v0.8.6 新增 🟡）：Codex 大会话里存在 `compacted` 顶层 type（context 被压缩后的痕迹），plan v0.8.5 完全没提。v1 默认跳过；将来如果发现这些记录含"用户对话被压缩前的总结"，可能值得保留——留待 v1 实现阶段实际打开看一眼再决定。
- [ ] `raw_ref` / `public_ref` 的生成边界：本机 debug 可保留绝对/相对路径；任何会进入 `distillation_packet.md`、`profile.json`、`profile.md`、`samples/`、README、docs 的引用只能用 `public_ref`。

---

### 4.2 C4 画像数据结构

#### 4.2.1 这一节在解决什么产品问题

类比 HR SaaS 里的"员工档案"：档案要存什么字段是一面（姓名、岗位、绩效），但 HR 圈最关键的规矩是**每条评价必须有依据**。"张三高潜"——依据是哪几次项目、哪几次评审？没依据 = 档案不可信 = 不能用作晋升决策。

C4 就是干这事。蒸出来的画像里会说"你偏好直接推进"——这条结论的依据是什么？哪几段对话？出现过多少次？最近还在不在出现？这些没存清楚，整份画像就是个黑箱，违反你"不脑补、必须可追溯"的核心偏好。

#### 4.2.2 已定的产品决策（🟢）

**🟢 决策 1：自带出处，不是"追问出处"**

每条结论**直接长在出处旁边**，看到结论就同时看到证据。不藏在结构里等用户问。

代价：画像产物文件变大（每条都拖证据）。接受，因为可追溯性是这个项目的产品哲学硬要求。

**🟢 决策 2：渲染格式定死**

```
**直接推进，少写解释型废话**
*证据：47 次出现 · 时间跨度 3 个月 · 把握度：高*
```

每条 axiom = 一行结论 + 一行证据。

**🟢 决策 3：把握度用 4 档标签，不用分数**

`high` / `medium` / `low` / `unstable`

- `unstable` 定义：曾经出现过但最近一段时间没再出现（具体时间阈值 🟡 见 4.2.4）
- 不用 0–1 分数：假精确；0.87 和 0.72 没有可解释差别，反而误导

**🟢 决策 4：v1 用全量蒸馏，不做真增量**

每次跑流水线都扫所有历史日志、全量重蒸出画像。真增量（只蒸新增对话 + 跨次状态合并）留 v2。

三条核心理由：

1. **跑通指标是"非熟人第一次跑"**——那个场景下全量和增量等价，增量零额外价值。
2. **真增量需要 smart merge**——要么引入自动化 AI 调用和跨次状态合并，要么用脆弱启发式（合错偏好），都会显著增加 v1 复杂度。
3. **真增量伤可追溯性**——一条结论变成多轮合并的混合体，出处链变长，违反"不脑补"。

但**本次语料的历史跨度**可以靠时间字段展示出来——靠决策 5 实现（v0.8.5 收口径：不再说"持续累积"，跨次不可比）。

**🟢 决策 5：用时间字段让"在历史跨度里看见稳定信号"成立，不靠跨次状态管理**

每条 axiom / cluster / theme 都带：
- `first_seen` 这条偏好在**本次语料中**首次出现时间
- `last_seen` 在**本次语料中**最近一次出现时间
- `count` 在**本次语料中**出现次数

这样：
- 用户读到的：一条偏好在一段时间跨度里反复出现 = 比单次偶发更值得信
- `unstable` 标签：靠本次语料里 `last_seen` 离今天超过阈值判定
- v2 升级路径：真增量时 C4 字段不动，只在 ingest 加"过滤已处理"的滤网

**🟡 v0.8.5 收紧口径**：v1 全量重蒸，**跨次不可比**。`count / first_seen / last_seen` 反映的是"本次语料里的时间分布"，不暗示"画像在跨次累积"。用户跑两次看到 count 变化是正常的——samples 集合变了，不是"偏好真的更稳了"。这条必须在 README / handoff 提示里明说，避免第一批非熟人因体感事故（"跑两次结果完全不一样"）流失。

**🟢 决策 6：v1 是"启发式预处理 + 用户 AI 工具语义蒸馏"，不是纯脚本语义聚类**

每次全量重蒸时，目标是把语义重叠的偏好合并成一条。v1 不假装脚本能独立完成强语义理解，而是分两层：

1. **脚本层做预处理**：关键词命中、编辑距离、同义词字典先把高信息片段归成候选组，减少用户 AI 工具需要读的噪声。
2. **用户 AI 工具做语义蒸馏**：用户在自己的 Claude Code / Codex / Cursor / 网页端 AI 工具里，按本项目 prompt 把候选组蒸成 C4 画像。
3. **C4 / renderer 做结构约束**：最终输出必须符合 C4 字段、每条结论带 `message_id + short_quote + public_ref` 证据三件套。`raw_ref` 只用于本机审计，不能进入可公开产物。

项目本身不内置统一云 API，也不要求用户安装本地模型；AI 理解能力来自用户主动选择的工具。这样避免把项目做成另一个 memory backend / LLM gateway，同时承认真正的"画像蒸馏"需要语义理解。

后续可做的不是"是否允许 LLM"，而是"是否把某些 AI 调用自动化"：本地 Ollama、云 API、网页端导出辅助都属于 v1.1+ 实验，不进入 v1 的默认路径。

不引入跨次状态管理就能兑现你"画像不要越蒸越胖"的目标。

**🟢 决策 7：C4 必须 axiom-first，画像不是个人简介**

v1 最核心产物是 `axioms[]`，不是 `identity`，也不是一段好看的自我介绍。原因：yage 原文要解决的不是"AI 不知道你住哪/用什么工具"，而是"AI 不懂你的非共识判断方式"。

所以 C4 验收顺序定死：

1. **先看 `axioms[]`**：有没有稳定判断原则，是否跨时间 / 跨场景反复出现，是否有证据。
2. **再看 `decision_patterns[]`**：这些原则背后的判断/取舍模式是否能解释用户反复纠正 AI 的原因。
3. **最后看 `identity` / `working_style`**：它们只是帮助 AI 快速定位用户背景，不是 v1 成败主线。

每条 axiom 必须满足四个条件，否则 validator 应标为失败或至少 warning：

- 是**判断原则**，不是事实标签。例："评估方案时优先可维护性和可调试性"合格；"用户会 Python"不合格。
- 有**跨场景证据**，至少来自 2 个不同任务场景或会话主题。
- 有**反例边界**，说明什么时候这条原则不适用，避免 AI 机械套用。
- 有**行为指令价值**，新 AI 读完后知道协作时应该怎么改变输出。

#### 4.2.3 v1 字段清单（附录性质，是上面 7 条决策的具体落地）

**顶层结构：**

| 字段 | 干嘛用 |
|---|---|
| `version` | 画像 schema 版本 |
| `generated_at` | 这份画像什么时候蒸的 |
| `source_stats` | 用了多少条对话、几个平台、时间跨度 |
| `identity` | "我是谁"：角色、领域、工具栈 |
| `working_style` | "我怎么工作"：节奏、推进方式、协作偏好 |
| `axioms[]` | 稳定判断原则清单（带证据，按决策 2 渲染）——这是 v1 最核心产物 |
| `preference_clusters[]` | 偏好主题聚类（"直接推进"、"边界清楚"……）|
| `friction_themes[]` | 高摩擦主题（你最常纠正 AI 的地方）|
| `decision_patterns[]` | 反复出现的判断/取舍模式（如优先范围控制、先验证真实状态、拒绝无依据脑补）|

**每条 axiom 的必填字段**（决策 1 + 3 + 5 + 7 的落地）：

| 字段 | 干嘛用 |
|---|---|
| `statement` | 一句话判断原则，必须能指导 AI 后续行为 |
| `why_it_matters` | 这条原则解决什么协作问题 |
| `applies_when` | 适用场景 |
| `does_not_apply_when` | 不适用 / 需要谨慎套用的边界 |
| `recommended_ai_behavior` | AI 读到后应该怎么改变输出 |
| `evidence` | 见下面证据子结构 |

**每条 axiom / cluster / theme 的"证据子结构"**：

| 字段 | 干嘛用 | 对应决策 |
|---|---|---|
| `source_fragments[]` | 来自哪几段对话——每条 fragment 含 `message_id` + `short_quote`（30–80 字摘录）+ `public_ref`（不含本机路径的审计引用）| 决策 1 |
| `count` | 出现次数 | 决策 5 |
| `first_seen` | 首次出现时间 | 决策 5 |
| `last_seen` | 最近一次出现时间 | 决策 5 |
| `confidence` | `high` / `medium` / `low` / `unstable` | 决策 3 |

每条 fragment 同时存 `message_id`（精确引用）+ `short_quote`（产物自包含可读）+ `public_ref`（独立审计可定位到脱敏后的消息，不暴露本机路径）三件套，避免"画像产物脱离 C2 原始数据就读不懂"的问题。`raw_ref` 只存在本机 debug / audit 层，用户需要深查时由本机映射表从 `public_ref` 找回原始文件位置。

#### 4.2.4 待磨的实操细节（🟡）

- [ ] `identity` / `working_style` 是结构化字段（角色 / 领域 / 工具栈分开）还是自由文本？结构化好检索、自由文本好读，**v1 选哪个**？
- [ ] `axioms[]` 的 v1 prompt 怎么写：如何要求用户 AI 工具只从证据包抽结论、保留出处、不把一次性项目事实上升为长期偏好，并输出 `applies_when / does_not_apply_when / recommended_ai_behavior`？
- [ ] `unstable` 的时间阈值：30 天？60 天？还是按用户跑流水线频率自适应？
- [ ] `validate_profile.py` 的 axiom-first warning / fail 边界：脚本只能硬校验字段、证据数量、跨 session / 跨时间、引用存在性、边界字段是否为空；"这是不是好 axiom / 是否真的表达了用户判断原则"只能做启发式 warning，最终靠 prompt + 人审。
- [x] ~~决策 6 的语义聚类实现~~ → 已定（v0.6）：v1 是启发式预处理 + 用户自选 AI 工具语义蒸馏；项目不内置统一云调用。
- [x] ~~`source_fragments` 存原文片段还是只存引用 id~~ → 已定（v0.8.4 修正）：公开产物存 `message_id` + `short_quote` + `public_ref` 三件套；`raw_ref` 只做本机审计。

---

### 4.3 C9 AI handoff 协议（v0.8.5 升 P0）

#### 4.3.1 这一节在解决什么产品问题

v1 真实路径不是脚本一把跑完：

```
prepare → packet.md → 用户切到 Claude Code/Codex → 把 packet 喂给 AI → AI 输出 profile JSON → 切回来 validate → 失败→回 AI 改 → render
```

3–4 次人工切换 + 1 个不可控环节（AI 蒸馏）。**非熟人最容易卡死的地方**。v0.8.4 之前只用 S7.5 一节带过；v0.8.5 起升 P0，与 C2 / C4 并列。

#### 4.3.2 已定的产品决策（🟢）

**🟢 决策 1：handoff 设计必须与 S-1 并行，不能 S-1 之后再做**

理由：handoff 的核心约束是 packet 尺寸，而 packet 尺寸完全取决于 S-1 才能测出的真实数据（单条 tool_result 多大、一个 session 多少条、噪声占比）。等 S-1 出完结果再开始 handoff = 把两个高不确定性环节串联。

**🟢 决策 2：v1 必须给出 packet 超长时的明确策略，不能默认"反正用户的 AI 工具会处理"**

至少回答：
- 单 packet token 上限（具体数字 S-1 后回写）
- 超限时按 session / 时间窗 / 信号类型切
- 分片后画像合并由谁负责（脚本？用户？AI 工具？）

**🟢 决策 3：validator 失败必须给出"回喂指令模板"，不能只报错**

非熟人拿到 validator 报错时，最容易的下一步应该是"复制这段提示发给 AI"，而不是"自己改 JSON"。这是 §1.5 豁免 2（清晰错误信息）的延伸——错误信息 + 回喂指令是同一件事。

#### 4.3.3 待磨的实操细节（🟡，S-1 后回写）

- [x] ~~packet 单文件 token 上限~~ → 已定（S-1 v0.8.6）：**≤ 16K token**。事实依据：真实 Claude Code 一个 700+ 行大会话的"用户原话 + 真实 AI 文本回复"累积 ≈ 34KB ≈ 8K token；16K token 上限足够覆盖几十次会话的真实对话内容（在 §5.2 激进过滤生效后），同时给主流 AI 工具（Claude 200K / Codex 接近）留出足够 prompt 空间。
- [ ] 超长分片策略：按 session / 按时间窗 / 按信号类型
- [ ] 回喂指令模板格式：纯文本提示 / JSON patch 指令 / 直接 reprompt
- [ ] AI 工具切换提示是否内置（CLI 输出里写"现在请把 packet 交给 Claude Code，命令是 ..."）

---

## 5. P1 待补全设计（🟡，第二批讨论）

### 5.1 C1 平台插件位

- v1 实现：`claude_code` + `codex` 两个解析器。
- v1.1 加 `hermes_agent`（用户 dogfooding 用，不在 v1 demo 覆盖范围内——目标用户大多没用过 Hermes）。
- v1 多源处理：**用户自己分子目录放，或多次传 `--input-dir`**——不做自动识别（按 §1.5 原则）。
- **🟢 流式读 + 早期过滤（S-1 v0.8.6 新增，硬约束）**：S-1 发现 Codex 单文件最大 250MB（且约 80% 行非对话内容）。adapter 必须支持**逐行流式解析**，在反序列化阶段就丢弃明确非对话的 `type`：
  - Claude Code：丢弃 `file-history-snapshot` / `queue-operation` / `last-prompt` / `attachment` / `ai-title` / `system`
  - Codex：丢弃 `event_msg` / `turn_context` / `session_meta`（保留 `compacted` 待 §4.1.4 决定）；对 `response_item` 仅保留 `payload.type=message`
  - **不允许"全文件加载进内存"**。这是性能硬约束，不是优化。
- 🟡 接口形式：函数签名 / 类继承 / 注册表？
- 🟡 失败处理：单条解析失败时跳过还是报错停？建议默认：单条失败跳过 + 记 warning 到 stderr（按 §1.5 豁免 2 给清晰错误信息）。
- 🟡 v1.1 待定：Hermes Agent 多渠道（CLI / 微信 / api_server）是按"一个 adapter 内部消化"还是"按渠道拆三个 adapter"？母体项目已能解析（`~/.hermes/state.db`），抽过来时再决定。

### 5.2 C3 高信息信号提取

- v1 实现：关键词启发式（用户已蒸出的"别 / 不 / 重新 / 错"等高频词）+ 证据包生成。C3 不是最终画像生成器，它的职责是把最有信息量的片段整理出来，交给用户自己的 AI 工具继续蒸馏。
- **基于初心的修正**：摩擦是强信号，但不是唯一信号。C3 证据包至少分四类：`friction_signals`（纠正/推翻/重做）、`decision_patterns`（反复判断和取舍）、`boundary_statements`（明确说什么不能碰/不能做）、`workflow_preferences`（稳定工具链和协作方式）。否则项目会滑成"纠错语料总结器"，蒸不出真正的判断原则。
- **必须过滤占位符 token**：`[EMAIL]` / `[PHONE]` / `[SECRET]` 等脱敏占位符不能进高频信号统计——脱敏后"给 [EMAIL] 发邮件"在很多对话里反复出现，启发式会误判 `[EMAIL]` 是用户偏好。所有方括号占位符 token 一律从信号统计里剔除。
- **🟢 必须激进过滤工具产物消息（S-1 v0.8.6 新增）**：S-1 发现真实日志"用户原话/总数据量"比例 ≈ 1:47（Claude Code）至 1:24000（Codex）。C3 处理前必须丢弃以下消息：
  - 所有 `is_tool_artifact=true` 的 C2 卡（即 6 种 `tool_artifact_type` 全部）
  - 即使 `is_tool_artifact=false` 但 `role=developer` 的（Codex 的 system prompt，median 7KB/条）
  - 即使内容是 `text` 但极短（< 5 字符）或极长（> 8KB，单条 user 消息真实 p90 仅 256 字符，超长几乎都是粘贴内容）
  
  如果不在 C3 阶段砍掉，`distillation_packet.md` 会撑爆 AI 工具 context window，C9 handoff 直接失败。
- **证据包输出合同先定死**：`distillation_packet.md` 至少包含四个同级区块：`friction_signals` / `decision_patterns` / `boundary_statements` / `workflow_preferences`。每条 signal 最少包含 `signal_id`、`signal_type`、`summary`、`why_high_information`、`source_fragments[]`、`candidate_axiom_hint`；每个 fragment 只能包含 `message_id`、`turn_index`、`ts`、`role`、`short_quote`、`public_ref`，不得包含 `raw_ref`、本机路径、项目名、仓库名。
- **每类信号的最低样本要求**：demo 的 packet 里每类至少 3 条候选 signal；每条目标 axiom 至少由 2 类 signal 支撑，避免只靠"用户纠错"蒸出偏好。真实路径可以少于这个数，但 validator / handoff 应给 warning，提示画像把握度可能偏低。
- 🟡 `friction_signals` 里的摩擦片段 = 用户单条消息 还是 用户消息 + 上一条 AI 回复 + 用户的纠正？
- 🟡 启发式规则要不要做成可配置？v1 内置一套，v2 让用户改？
- 🟡 蒸馏 prompt 要不要作为 C3 产物一起输出？建议默认：要。输出 `distillation_packet.md`，里面包含候选片段、约束、禁止脑补规则和 C4 输出格式。

### 5.3 C5 导出器

- v1 实现：**两个导出器**。
  1. 可粘贴的 `profile.md`（往任何 LLM 网页对话框一贴即用）。
  2. 一个自带数据的 skill 包（参考母体项目的 `install_global_skills.sh` 思路，但产物落 `OUT_DIR`，不是 `~/.claude/skills/`）。**v1 只做一种 skill 格式**（按 §1.5 原则）。
- 🟡 skill 包目标格式 v1 选哪个：Claude skill / Codex skill？建议默认：**Claude skill**（母体项目装的就是它）。
- 🟡 `profile.md` 是 C4 画像数据结构的全量序列化，还是精简版？

### 5.4 C6 脱敏过滤

- v1 实现：擦 API key（`sk-...` / `xoxb-...` 等已知模式），方式：**替换为占位符**（`[SECRET]` / `[EMAIL]` / `[PHONE]`），保留文本语义结构。
- 占位符是产品质量考虑，**不是 §1.5 意义上的便利 hedge**——纯删除会让"给某邮箱发邮件"变成"给 发邮件"，下游 LLM 读到这样的破句会误解上下文。
- 🟡 邮箱 / 手机号 v1 要不要做？做了 = 多一条规则；不做 = 用户数据可能暴露在产物里。建议默认：**v1 同时做 API key + 邮箱 + 手机号**（占位符方案规则增加成本低）。

### 5.5 C8 配置文件

- v1 实现：**只用 CLI 参数，不要 YAML 配置文件**（按 §1.5 原则，用户想长期记配置自己写 shell alias 或 `.envrc`）。
- v1 CLI 参数集（仅这些）：`--input-dir`（可多次）、`--out-dir`、`--adapters`（启用哪些）。
- 🟢 默认 `--out-dir`：`~/.pls-remember-me/out`（v0.8.5 已拍板，见 §7.1）

---

## 6. v1 执行步骤（🟢顺序已定：先产物后字段；v0.9 重排）

### 6.0 v0.9 执行顺序调整

S-1 已完成（v0.8.6 回写）。基于 v0.9 路线图重铸（v1 = infrastructure 启动器，不是 bootstrap seed），原 §6 表里 S00–S13 的执行内容需做以下修正：

- **新增 S-0.5：老项目抽提**（在 S00 之前，**v1 主线工作量**）：
  - 把 `export_ai_chats.py` / `extract_observations.py` / `weekly_reflection.py` / `THEME_RULES` / axiom 结构 / `distilled-profile-2026-05-09.md` 从 `personal-context-infrastructure` 抽出
  - 做三件事：去本机硬编码（`Path.home()` 等）、通用化（去 user-specific 词汇）、个人内容剥离（删姓名 / 公司 / 客户 / 真实项目名）
  - 抽完落入 `scripts/` / `samples/expected-real-output/` 等位置
- **S00 / S0 / S1（demo 三件套）大幅缩水**：因为 `samples/expected-real-output/` 已经背书"真实输出长什么样"，合成 samples 不需要 over-engineer。S00 协同规则中"埋点矩阵"（每条 axiom 5 次出现 / 3 同义表达 / 跨 2 场景 / 跨 3 月）砍掉一半——合成 samples 只需 demo 流程跑通，不承担说服力。S0 `EXPECTED.md` 草案直接从 `expected-real-output/` 派生。
- **S4–S9 主线变化**：从"写 adapter / ingest / signal extraction" 改为 "抽老项目代码 + 通用化"。代码量预估降 60%。
- **新增 S9.5：daily / weekly 子命令封装**（在 S9 之后）：抽老项目 `run_daily_pipeline.sh` / `run_weekly_reflection.sh` 简化为 v1 子命令（不强制 cron，README 分"试一次" / "真用" 两段说明）。
- **S10 / S10.5 / S11 / S12 / S13 顺序不动**，但 S12 README 需要新增："这是 infrastructure 启动器，不是一次性蒸馏器"的口径校准 + daily/weekly 用法说明。

下方表格内的步骤内容**保留 v0.8 表述作为参考底版**，v1 实现按 v0.9 口径执行；冲突以 v0.9 为准。



**核心顺序原则**：第一性是"公开示例样本中埋的稳定判断原则能被准确蒸出来"，不是"schema 正确"。所以先写 EXPECTED 草案、定 samples，再倒推字段。这样实现失败时归因清楚：要么"埋的判断原则 X 没蒸出来"（产品问题），要么"字段缺信息"（schema 问题）。

**关键执行原则——demo 三件套必须协同设计**：S0（EXPECTED 草案）、S1（samples 语料）、S6（C3 启发式词典）是同一个设计单元的三个面，**必须由同一个人/同一会话连贯设计**，不能拆给不同人/不同会话独立动手。S00 把协同规则定死，是 S0 动手前的硬前提。

**新增现实校准原则**：S00 前必须先做 S-1，只看真实 Claude Code / Codex 日志的结构，不抽取真实语义内容。否则 samples 可能长得很漂亮，但 adapter 一碰真实日志就发现字段、层级、tool 噪声、时间戳和 session 规则全不一样。

| 阶段 | 动作 | 产物 | 前置依赖 |
|---|---|---|---|
| **S-1** | **真实日志结构侦察（只看结构，不带内容进仓库）**：在 gitignored / 仓库外路径抽样 Claude Code + Codex 真实 `.jsonl`，记录字段层级、session 取得方式、时间戳格式、role 枚举、tool_use/tool_result/system 噪声形态、单条消息长度分布、文件/行号定位方式、路径泄漏风险。只把"结构发现和实现规则"写回 plan，不写任何真实内容、真实路径、真实 axiom | 结构侦察笔记（可写入 docs，只含规则） | 第 4 节讨论收敛 |
| **S00** | **写 demo 三件套协同设计规则**：①每个目标判断原则必须有可观察行为证据，优先用"`assistant 误判/啰嗦/跑偏` → `user 纠正`"对话对形式埋，但也必须包含反复决策、边界声明、优先级取舍等非摩擦证据；②每个目标 axiom 至少出现 **5 次**，至少 **3 种同义表达**，且跨至少 **2 种任务场景**；③samples 必须覆盖至少 **3 个时间段**（建议 `2026-03 / 2026-04 / 2026-05`），让 first_seen ≠ last_seen 在 demo 里可见；④至少一条偏好**只在早期出现**，用来演示 `unstable` 标签；⑤必须放入"**近似但不该合并**"和"**表达不同但该合并**"的对照样本（验证启发式聚类的边界）；⑥S0/S1/S6 的 EXPECTED / 样本 / 启发式词典是同一组人/同一会话设计；⑦S-1 发现的真实结构差异必须反映到 samples 格式里，不能造一个 adapter 永远遇不到的理想日志 | 协同规则文档 🟢 | S-1 |
| **S0** | （**demo 三件套之一**，遵循 S00 规则）写 `samples/EXPECTED.md` 草案——明文写出"成功 demo 产物长什么样"（不写代码，只写最终画像该是什么内容、什么结构、带几条 axiom、`first_seen != last_seen`、`count > 1` 都在 EXPECTED 里展示）| EXPECTED 草案 | S00 |
| **S1** | （**demo 三件套之二**，遵循 S00 规则）设计 `samples/logs/` 公开示例语料：可由真实 dogfood 中发现的问题启发，但必须合成化为虚构人物 + 虚构项目 + 多个 `.jsonl` + 40–60 条 user 消息（按 S00 跨 3 个月分布）+ 埋点覆盖摩擦纠正、反复决策、边界声明、优先级取舍四类信号 + 含 unstable 演示 + 含合并/不合并对照对 | `samples/logs/*.jsonl` | S00, S0 |
| **S2** | 由 EXPECTED + samples 倒推 C2 字段拍死，写进本文档 §4.1 | C2 字段 🟢 | S1 |
| **S3** | 同上倒推 C4 字段拍死，写进本文档 §4.2 | C4 字段 🟢 | S1 |
| S4 | 写 2 个 adapter：`adapters/claude_code.py` + `adapters/codex.py`：原始日志 → C2 卡 | 两个解析器 | S2 |
| S5 | 写 `scripts/ingest.py`：调用 adapter + C6 脱敏（占位符替换）| 清洁对话流 | S4 |
| **S6** | （**demo 三件套之三**，遵循 S00 规则）写 C3 信号提取 + 证据包生成——关键词启发式词典 + 同义词字典必须覆盖 S1 埋点表达 + 过滤 `[EMAIL]` 等占位符 token + 输出给用户 AI 工具的 `distillation_packet.md`。文件名可仍叫 `friction.py`，但输出不能只有 friction，必须包含 S00 定义的四类高信息信号 | 高信息片段 + 蒸馏证据包 | S5, S00 |
| S7 | 写 `prompts/distill_profile.md` + `scripts/validate_profile.py`：用户 AI 工具按 prompt 将证据包蒸成 C4 画像；validator 先校验 C4 结构，再执行 axiom-first 规则（见 §4.2.2 决策 7）。validator 只负责可机械判断的合同，不冒充语义裁判：字段、引用、证据数量、跨 session / 跨时间是 fail/warning；axiom 好不好、有没有洞察力只做 warning + 人审提示 | profile JSON / profile draft | S6、S3 |
| **S7.5** | 写 AI handoff 协议：在 `distillation_packet.md` 顶部或独立 `AI_HANDOFF.md` 中说明"把哪段交给 AI / 期望生成什么文件 / validator 报错后如何让 AI 修复 / 不允许脑补什么"。这是 v0.6 后新增的关键产品面，不能只靠 README 一句带过 | 用户交接说明 | S7 |
| S8 | 写 `scripts/render.py`：C4 → `profile.md` + skill 包 | 可粘贴 md + skill 包 | S7 |
| S9 | 写 `scripts/pls_remember_me.py`：CLI 总入口（`prepare` / `validate` / `render` / `demo` 子命令 + 输入验证 + 清晰错误信息，按 §1.5 豁免 2）。`prepare` 生成证据包，`validate/render` 处理用户 AI 工具产出的 C4 画像，不假装脚本能自动完成语义蒸馏 | CLI | S5–S8 |
| **S10** | **跑可控 demo 闭环对照 S0 的 EXPECTED**：`samples/logs` → `distillation_packet.md` → **仓库内置 canned `samples/EXPECTED.profile.json`** → `validate` → `render` → 对照 `samples/EXPECTED.md`。**S10 只验证 schema 与流转**：证据包结构、C4 字段、axiom-first validator 规则、renderer 输出闭环。**S10 不验证、也不能验证**：（a）真实 AI 蒸馏质量、（b）C3 启发式提取的信号是否真有蒸馏价值、（c）用户能否完成人工 handoff。这三件事只能靠 S10.5 dogfood + 发布后 §1.3 验证。 | v1 实现完结 | S9 |
| **S10.5** | **本机真实数据 dogfood smoke**：允许在实现过程中用用户本机 Claude Code / Codex 真实日志跑 `prepare -> AI handoff -> validate -> render`，专门抓真实日志结构、脱敏、路径、超长文本、工具调用噪声等 samples 覆盖不到的问题。真实输入、真实 packet、真实 profile、真实 skill 和真实路径映射表必须落在 `.gitignore` 拦截路径（如 `local_dogfood/`、`raw_logs/`、`out/`、`~/.pls-remember-me/out`）；可以把机制问题和合成样本构造规则写回公开文档，但不能写回任何可识别真实内容 | 本机 smoke 结果（不进 git） | S10 |
| S11 | 写 `scripts/run_demo.sh`：一键跑 samples 的可控 demo 闭环（总耗时必须 < 30s，见 §6.2），明确提示用户 demo 使用 canned profile，真实路径需要用户自选 AI 工具生成 profile JSON | 一键 demo | S10.5 |
| S12 | 改 README：30 秒证明价值 + 女娲对照 + 真实数据用法 + skill 包安装一句话指引（如 `cp -R OUT_DIR/skill ~/.claude/skills/...`）| README ✅ | S11 |
| S13 | 加 LICENSE（MIT，署名 GitHub ID）| LICENSE | 🟡署名 ID |

### 6.1 v1 实现完成 ≠ 项目跑通

S10 校验通过和 §1.3 跑通是两件事，必须切开。v0.8 起，S10 只验证**可控 demo 闭环**，不再假装验证用户 AI 工具的真实语义蒸馏能力。

| | S10 校验 | §1.3 跑通 |
|---|---|---|
| 是什么 | 自己在虚构 samples 上跑通 `packet -> canned profile -> validate -> render -> EXPECTED` | 非熟人在真实日志上跑出 profile，并反馈改变协作方式 / 第一条 inbound |
| 时间点 | v1 实现阶段最后一关 | v1 发布后才能验证 |
| 控制权 | 完全在你手里 | 不在你手里 |
| 性质 | demo 与结构约束的"自测通过" | 项目的"真跑通" |

S10 明确不证明三件事：

1. 不证明任意 AI 工具都能稳定按 prompt 生成合格 profile。
2. 不证明真实用户日志里的信号足够干净。
3. 不证明用户会顺利完成 `prepare -> AI handoff -> validate -> render` 的人工交接。

这三件事只能靠发布后的非熟人试跑验证。因此 S7.5 的 handoff 说明和 validator 错误信息，是 v1 能否被真实用户跑通的关键产品面。

### 6.1.1 本机真实数据 dogfood 边界

实现阶段可以、也应该用用户本机真实 Claude Code / Codex 日志做 dogfood smoke。原因：纯凭空造 samples 容易失真，真实日志会暴露很多意想不到的问题，比如：

- Claude Code / Codex 日志结构和预想不一致。
- tool_use / tool_result / system message 噪声比 samples 多。
- 单条消息很长，导致 packet 过大或 prompt 不可用。
- `raw_ref` / 本机路径映射表误进入 packet、profile、samples 或 README，泄漏本机路径、项目名或其他隐私信息。
- 脱敏规则漏掉 API key、邮箱、手机号或其他敏感片段。
- 用户 AI 工具生成的 profile JSON 不符合 validator 预期。

但 dogfood 必须守住边界：

1. **原始真实数据不进仓库**：不得把真实日志、真实 packet、真实 profile、真实 skill 包放进 `samples/`、`docs/`、README 或任何会提交的路径。
2. **只用 gitignored 路径**：推荐输入放 `local_dogfood/raw_logs/` 或仓库外目录，输出放 `out/` 或 `~/.pls-remember-me/out`。
3. **允许真实启发的合成样本**：`samples/`、`docs/`、README 可以使用从真实 dogfood 中抽象出来的模式，但必须经过脱敏 + 改写 + 结构重组 + 场景替换 + 多次重构，变成不可回溯的公开示例。目标是保留"真实问题形状"，不保留"真实内容"。
4. **绝对不能进入公开产物的东西**：真实人名、公司名、客户名、项目名、仓库名、本机路径、URL、账号、密钥、原始长句、独特措辞、真实 axiom 原文、可定位到真实事件的时间线。
5. **只沉淀机制问题**：如果 dogfood 发现 bug，可以把"解析规则 / 脱敏规则 / validator 规则 / prompt 约束 / 示例构造模式"写回项目；不要把任何可识别真实片段、真实 axiom、真实路径写回公开文件。
6. **发布前做泄漏检查**：pull / push 前必须确认 `find .`、`rg`、或 git 状态里没有真实日志和真实产物；如果仓库不是 git repo，也要按 `.gitignore` 清单人工检查。

S10.5 不替代 S10，也不替代 §1.3。它的作用是降低"公开 demo 全过、真实日志一跑就炸"的风险，并为 samples 提供更接近真实问题形状的合成依据。

**S10 通过后的发布动作**（不在核心实现链路 S0–S13 里，是独立后续）：

1. **选 3–5 个潜在非熟人**（重度多工具 AI 用户：用 Claude Code / Codex / 其他 AI 编辑器的）
2. **主动私信邀请试跑**：提供 README 链接 + samples demo 录屏（如果有）+ 一句话价值主张
3. **反馈渠道**：GitHub issue / 私信均可，不要让用户填表格
4. **成功阈值**（§1.3 跑通的最低门槛）：**至少 1 个非熟人**在自己真实日志上跑出画像，并明确说"这能改变我后续喂 context 给 AI 的方式"；或第一条主动 inbound（合作 / 求助 / 引用）

🟡 待磨：3–5 个非熟人候选清单（不进 plan，等 S10 通过后另定）；要不要做录屏；inbound 怎么算（star 不算，star + 评论提到具体用例算）。

### 6.2 demo 性能约束（硬上限）

"30 秒看到 demo 产物"是承诺，不是 nice-to-have。这里的 demo 产物指 samples 的证据包、内置 canned `profile.json`、validator 结果和渲染结果；真实用户日志的 AI 蒸馏环节取决于用户自己的 AI 工具，不计入脚本性能预算。预算：

- `bash scripts/run_demo.sh` 总耗时 **< 30s**（含 Python 启动 + 依赖加载 + 可控 demo 闭环跑完 + 产物落盘 + 提示用户去看哪个文件）
- demo 预处理脚本（ingest + signal extraction + packet 生成）运行 **< 20s**（**对 samples 小语料**）
- **🟢 真实路径预算分开写（S-1 v0.8.6 新增）**：S-1 发现用户 `--input-dir` 指向 `~/.codex/sessions/` 时单文件可达 250MB，整目录可达数 GB——**demo 30s 承诺不适用于真实路径**。真实路径只承诺：流式解析、不爆内存、给清晰的进度提示（"已处理 X 个文件 / Y MB"）。具体处理速度上限留 v1 实现阶段实测后定，README 必须明说"真实路径耗时取决于你的日志体量"。
- 用户 AI 工具的人工/模型响应时间不计入脚本性能预算，但 README 不能把这段说成脚本自动完成。
- 任何加载（启发式词典、同义词字典、samples）必须在 1s 内完成

破这个预算 = v1 demo 核心卖点崩盘。**如果实现到 S10 跑出来超时，必须立刻找替代方案**（精简 samples / 优化启发式 / 砍中间步骤），不能放任。这条是硬约束，不接受"v1 先这样、性能 v1.1 优化"的妥协。

---

## 7. 待确认清单汇总

### 7.1 架构层（来自 architecture.md §6）

- [ ] **LICENSE 著作权人 GitHub ID 字符串**（决策已定用 GitHub ID，具体字符串待补）
- [x] ~~**OUT_DIR 默认位置**~~ → 已定（v0.8.5）：**`~/.pls-remember-me/out`**。理由：不污染项目目录、跨多次输入复用方便、`.gitignore` 漏写也不会进 git。"所见即所得"对目标用户（§1.5 重度 AI 用户）权重不高。

**已砍掉的架构层项**（沉淀在这里防止反复加回）：
- ~~`npx`/node 包装、顶层 SKILL.md、L3 分发壳~~：**因架构性原因砍掉**——项目本体是批处理流水线，不是 AI 推理时调用的 skill，不进 `npx skills` 生态。安装方式是 `git clone` + `python3 scripts/...`。
- ~~辅助拷日志脚本~~：按 §1.5 砍——用户自己 `cp ~/.codex/sessions ./my-logs/`
- ~~YAML 配置文件~~：按 §1.5 砍——v1 只 CLI 参数
- ~~多源自动识别~~：按 §1.5 砍——用户自己分子目录或多次传 `--input-dir`
- ~~脱敏纯删除~~：**反转决策**——纯删除会破坏文本语义（"给 发邮件"让下游 LLM 困惑），改为**占位符**（`[EMAIL]` / `[PHONE]` / `[SECRET]`）保留语义结构。占位符不是 §1.5 意义上的便利 hedge，是产品质量考虑。

### 7.2 P0 字段层（本文档 §4）

- C2 实操细节见 §4.1.4
- C4 实操细节见 §4.2.4（重点是 v1 蒸馏 prompt、axiom-first 校验边界、结构化字段和 unstable 阈值）
- **C9 handoff 实操细节见 §4.3.3**（packet token 上限、超长分片策略、回喂指令模板、AI 切换提示——全部 🟡，S-1 后回写）

### 7.3 P1 实现层（本文档 §5）

见 §5.1–§5.5 各小节的 🟡。

### 7.4 执行顺序（本文档 §6）

- [x] ~~S3 要不要提前到 S1/S2 之前~~ → 已定（v0.4）：整个顺序倒过来，S0 EXPECTED 草案 → S1 samples → S2/S3 字段反推。
- [x] ~~S10 是否验证真实 AI 蒸馏能力~~ → 已定（v0.8）：不验证。S10 只验证可控 demo 闭环；真实 AI 蒸馏能力靠发布后非熟人试跑验证。
- [x] ~~实现阶段能不能用本机真实数据~~ → 已定（v0.8.3）：可以，而且建议做 S10.5 dogfood smoke；原始真实输入/输出必须落在 gitignored 路径；公开 samples/docs/README 可以使用真实启发的合成样本，但必须不可识别、不可回溯。

---

## 8. 与现有文档/资产的关系

| 文档/资产 | 关系 | 备注 |
|---|---|---|
| [`docs/architecture.md`](architecture.md) | **上层**，边界宪法。本文档不挑战它，只细化。 | 已同步 v0.7 口径：无中心化服务 + 用户自选 AI 工具参与蒸馏 + v1 只是第一版 context seed。 |
| [`README.md`](../README.md) | **下游**，面向陌生人。本文档定完才动 README。 | S12 才改。 |
| `.gitignore` | 已物理拦截个人产物。本文档不动它。 | — |
| 母体项目 `personal-context-infrastructure` | 抽机制的源头，不双向同步（模型 A）。 | 见 §2.4。Hermes Agent adapter 逻辑可参考母体项目 `export_ai_chats.py`。 |
| 母体项目 Obsidian Vault `02-副业探索/蒸馏自己-方向探索.md` | 副业方向决策原始材料。 | 不进本仓库。 |

---

## 9. 变更记录

| 日期 | 变更 | 谁 |
|---|---|---|
| 2026-05-19 | 初版 v0.1：把 CLI 对话里定下来的边界、8 模块框架、P0/P1/P2 优先级、扩展矩阵、字段建议、待确认清单沉淀成文档 | Claude (本会话) |
| 2026-05-19 | v0.2：v1 adapter 范围从 2 个改为 3 个（加 Hermes Agent，移除 OpenClaw 进 v2）；§4 重写：用 HR 类比开篇 + C4 拍定 6 条产品决策（自带出处 / 渲染格式 / 4 档把握度标签含 unstable / v1 全量蒸馏 / 时间字段呈现持续累积 / 蒸馏阶段语义聚类）；§5.1 加 hermes_agent adapter；§6 S4 改成 3 个 adapter；§3.4 扩展矩阵把 Hermes 从"未来"挪到 v1 范围 | Claude (本会话) |
| 2026-05-19 | v0.3：新增 §1.5 目标用户与设计原则（"不为非目标用户加便利 hedge"）；按此原则砍掉拷日志辅助脚本 / `npx` 包装 / YAML 配置文件 / 多源自动识别 / skill 多格式 / 脱敏打码 6 项；§5.1/5.3/5.4/5.5 同步精简；§7.1 从 4 项瘦到 2 项，砍掉的项目沉淀到 §7.1 底部防止反复加回；§0 加指引让后续 AI 工具优先对照 §1.5 | Claude (本会话) |
| 2026-05-19 | v0.3.1：修订 L3 分发壳的真正定性——`npx skills add` / SKILL.md 被砍**不是因为 §1.5 便利 hedge**，而是**架构性原因**：项目本体是批处理流水线（活儿在离线时），`npx skills` 生态装的是 AI 推理时调用的能力，形态不匹配。§2.2 L3 行从"薄壳"改为"不存在"；§7.1 砍掉理由分类修正；同步更新 architecture.md §1 / §3 目录结构 / §6 待确认；README.md 安装命令从 `npx skills add` 改为 `git clone` | Claude (本会话) |
| 2026-05-19 | v0.4：批量吸收 critique 6 条全盘接受项。具体：（1）§1.5 加豁免 2——输入验证 + 清晰错误信息不算便利 hedge；（2）§2.3 / §3.4 / §5.1 / §6 把 Hermes Agent 从 v1 砍回 v1.1，v1 adapter 范围恢复为 Claude Code + Codex 2 个；（3）§4.1.3 C2 新增 `message_id` + `turn_index` + `raw_ref` 三字段（修复"声称可追溯但没稳定 ID"的缺口）；（4）§4.2.2 决策 6 改为启发式聚类三招（关键词重叠 + 编辑距离 + 同义词字典），明文写"v1 不承诺强语义聚类"，LLM 路径推到 v1.1 实验分支；（5）§4.2.3 `source_fragments` 子结构从单 id 改为 `message_id + short_quote + raw_ref` 三件套；（6）§5.4 脱敏从纯删除改为占位符 `[SECRET]/[EMAIL]/[PHONE]`，明文写"占位符是产品质量，不是 §1.5 便利 hedge"；（7）§6 执行顺序整体倒过来——S0 EXPECTED 草案 → S1 samples → S2/S3 字段反推 → 实现 → S10 对照 EXPECTED 校验；（8）§4.2.4 / §7.1 / §7.4 沉淀已定项的反转/修正记录 | Claude (本会话) |
| 2026-05-19 | v0.5：批量吸收 Codex 二次审视的 3 个真问题 + 5 个小毛病。具体：（1）§6 加 **S00 demo 三件套协同设计规则**（埋点必须为摩擦对话对 / 每偏好至少 5 次出现 3 种同义表达 / samples 跨 3 个月 / 含 unstable 演示 / 含合并对照样本 / S0+S1+S6 必须同一人/同一会话连贯设计）——修复"S0/S1/S6 串行设计互不对齐"的隐藏死循环；（2）§6 加 **§6.1 v1 实现完成 ≠ 项目跑通** 段——切开 S10（demo 自测）和 §1.3（项目真跑通），加发布动作 + 反馈渠道 + 成功阈值；（3）§6 加 **§6.2 demo 性能约束**——总耗时 < 30s 是硬上限，破预算必须立刻调整不能放任；（4）§1.5 加豁免 3——数据完整性 / 失败可调试性 / 文本语义保留 不算便利 hedge（防止占位符脱敏被再次误砍）；（5）§5.2 C3 启发式必须过滤 `[EMAIL]/[PHONE]/[SECRET]` 等占位符 token（防止脱敏污染高频信号统计）；（6）§2.3 v1.1 触发条件明文化——§1.3 跑通后 或 v1 发布后 6 周取最早；（7）S12 加 README 提示 skill 包安装一句话指引；（8）S0/S1/S6 在表里明文标 "demo 三件套之 X" | Claude (本会话) |
| 2026-05-20 | v0.6：修正 Codex 对项目运行方式的误读。具体：（1）§1.1 / §1.2 / §1.6 把"纯本地/离线蒸馏"改为"用户本机项目 + 用户自选 AI 工具参与蒸馏"；（2）§2.1 第一原则改为"无中心化服务，项目方不托管/不收集/不默认上传"，不再承诺用户不会联网或不会用云端 AI；（3）§2.3 明确 v1 先支持 Claude Code + Codex，但长期定位覆盖大部分 AI 工具和网页端导出；（4）§3 数据流改为 C3 生成摩擦证据包，用户自选 AI 工具按 prompt 蒸成 C4 画像；（5）§4.2 决策 6 改为"启发式预处理 + 用户 AI 工具语义蒸馏"，项目不内置统一云调用；（6）§5.2 / §6 执行步骤新增 `distillation_packet.md`、`prompts/distill_profile.md`、`validate_profile.py`，CLI 改为 `prepare/validate/render/demo`，不再假装脚本自动完成语义蒸馏；（7）§6.2 性能预算只约束 demo 和预处理脚本，用户 AI 工具响应时间不计入脚本预算；（8）§8 标记 architecture.md 后续需要同步新口径 | Codex (本会话) |
| 2026-05-20 | v0.7：回到 yage context infrastructure 初心。具体：（1）新增 §1.0，明确本项目不是聊天记录总结器，而是启动个人 context infrastructure 的第一步；（2）v1 定位收窄为第一版可追溯 context seed，不冒充完整长期系统；（3）C3 从单一摩擦信号扩展为高信息信号，至少覆盖 friction_signals / decision_patterns / boundary_statements / workflow_preferences；（4）C4 强调 `axioms[]` 是核心产物，并新增 `decision_patterns[]`；（5）S00 / S6 更新 demo 设计规则，要求样本体现稳定判断原则，而不只是用户纠错偏好 | Codex (本会话) |
| 2026-05-20 | v0.8：根据 v0.7 结论优化 plan。具体：（1）新增 §1.7 三段路线图：v1 Bootstrap context seed / v1.1 Accumulation dogfood / v2 Infrastructure loop；（2）§4.2 新增决策 7：C4 必须 axiom-first，`identity` 和 `working_style` 只是辅助；（3）给每条 axiom 增加 `statement / why_it_matters / applies_when / does_not_apply_when / recommended_ai_behavior / evidence` 必填字段；（4）S7 增加 axiom-first validator 要求，新增 S7.5 AI handoff 协议；（5）S10 重定义为可控 demo 闭环，只验证 `packet -> canned profile -> validate -> render -> EXPECTED`，真实 AI 蒸馏能力放到发布后验证；（6）§6.2 性能预算同步改为可控 demo 闭环 | Codex (本会话) |
| 2026-05-20 | v0.8.1：收窄 §1.6 蒸馏执行环境口径。v1 主路径先限定 Claude Code / Codex，与 v1 日志采集范围一致；其他 CLI / IDE / 网页端 AI 工具不排除，但不作为 v1 主路径承诺，尤其网页端 handoff 留到后续版本打磨 | Codex (本会话) |
| 2026-05-20 | v0.8.2：新增 S10.5 本机真实数据 dogfood smoke。实现阶段允许用用户本机 Claude Code / Codex 真实日志验证真实结构、脱敏、packet、handoff、validator 和 renderer，但真实输入/输出必须落在 `.gitignore` 拦截路径，不得进入 samples/docs/README/公开产物；同步把该边界写入 §6.1.1 和 §7.4 | Codex (本会话) |
| 2026-05-20 | v0.8.3：修正真实数据边界。公开 samples/docs/README 不再要求完全凭空造，允许使用真实 dogfood 启发的合成样本；但必须经过脱敏、改写、结构重组、场景替换和多次重构，确保不可识别、不可回溯。原始真实日志 / packet / profile / skill 仍然永不进仓库 | Codex (本会话) |
| 2026-05-20 | v0.8.4：实现前硬化修正。具体：（1）新增 S-1 真实日志结构侦察，S00 前先确认 Claude Code / Codex 真实 `.jsonl` 的结构、时间戳、role、tool 噪声和路径风险；（2）拆分 `raw_ref` 与 `public_ref`，公开 packet/profile/samples 只允许 `public_ref`，`raw_ref` 仅留本机审计；（3）补 C3 `distillation_packet.md` 输出合同，四类 signal 都必须有结构化字段和公开引用；（4）修正 S10.5 与 §6.1.1 的口径冲突：真实输入/输出不进仓库，但真实启发的合成样本和机制规则可以进公开文档；（5）明确 validator 只做机械合同校验，不冒充语义裁判 | Codex (本会话) |
| 2026-05-20 | **v0.8.5：plan freeze + 应用 Claude/Codex 批判结论**。下一步不再修 plan，直接跑 S-1。具体：（1）顶部加 **FROZEN** 状态标记；（2）§2.3 v1.1 触发从 "§1.3 跑通 或 6 周取最早" 改为 "§1.3 跑通后启动；6 周未跑通做复盘，不自动扩范围"——修复硬指标与 fallback 并存的矛盾；（3）§3.1 / §3.3 / §4.3 新增 **C9 AI handoff 协议升 P0**（与 C2/C4 并列），三条决策：handoff 与 S-1 并行设计、v1 必须给 packet 超长策略、validator 失败必须给回喂指令模板——修复把 handoff 当 S7.5 小步骤的低估；（4）§4.2 决策 5 收口径：v1 全量重蒸跨次不可比，`count / first_seen / last_seen` 只反映本次语料的时间分布——避免第一批非熟人体感事故；（5）§6 S10 诚实化：只验证 schema 与流转，**不验证** 真实 AI 蒸馏质量 / C3 启发式价值 / 用户能否完成 handoff，靠 S10.5 + §1.3 验证；（6）§7.1 OUT_DIR 拍板 `~/.pls-remember-me/out`。**v1 adapter 数量保持 2 个（Claude Code + Codex），不接受"砍到 1 个"建议**——adapter 是 C1 插件位的最小可信演示，少一个就证明不了 C1 设计成立 | Claude + Codex 批判 → 用户拍板 (本会话) |
| 2026-05-20 | **v0.8.6：S-1 真实日志侦察事实回写**。按 v0.8.5 FROZEN 规则允许的"S-1 事实回写"。事实依据均见 `local_dogfood/s1-recon.md`（gitignored，不进 git）。10 条修订：（1）§4.1.3 `role` 枚举加 `developer`——Codex 真实日志有此角色，承载 system prompt；（2）§4.1.3 `message_id` 构造改为 adapter-specific——Claude Code 用原生 `uuid`（DAG 节点 ID），Codex 构造 `codex:{session_id}:{file_line_offset}`；（3）§4.1.3 新增 `parent_message_id` 字段——Claude Code 有 sidechain DAG，`turn_index` 无法表达，必须并存；（4）§4.1.3 新增 `tool_artifact_type` 字段（6 种枚举），关闭 §4.1.4 待磨问题；（5）§4.1.2 新增**决策 3**——结构性路径字段（`cwd` / `gitBranch` / `source_meta` / 项目目录名）必须在 C2 adapter 阶段整字段丢弃，不进 `meta`、不进 `raw_ref`；（6）§5.1 C1 加**流式读 + 早期过滤硬约束**——Codex 单文件最大 250MB，不允许全加载内存；（7）§5.2 C3 加**激进过滤工具产物消息**——真实日志噪声/信号比可达 24000:1；（8）§4.3.3 packet token 上限拍板 **≤ 16K**——真实用户原话密度足够；（9）§4.1.4 新增 🟡 Codex `compacted` records 待磨；（10）§6.2 性能预算分场景写明——demo `< 30s` 不适用于真实路径（用户 `~/.codex` 可达 GB 级）。**plan 仍 FROZEN**，下一步进 S00 demo 协同规则 | S-1 recon → 回写 (本会话) |
| 2026-05-20 | **v0.9：路线图重铸 + 激进吃老项目**。背景：用户对比老项目 `personal-context-infrastructure` 后自我怀疑——老项目实际已是 yage context infrastructure 的 v0 实现（4 个 adapter / observer + reflector + axiom 三层 / 跑了一个月），而 v1 计划只做 bootstrap seed 是自我缩水。**这次解冻是 FROZEN 规则允许的"实现暴露的具体问题"**：老项目就是 v1 范围错位的反例，不是抽象 critique。用户拍板 D1=长期 / D2=daily-weekly 包含但不强制 cron / D3=行为留存。具体修订：（1）顶部 FROZEN 块更新解冻历史 + v0.9 重铸说明；（2）§1.3 跑通指标主指标改为"用了一周还在用 / 行为留存"，老指标降为辅助信号；（3）§1.7 v1 改名"个人 context infrastructure 启动器"，包含 observer/reflector 雏形（不强制 cron）；（4）§2.3 v1 范围重定义为 9 条主线，主线 = 抽老项目而不是从零写：adapter 数从 2 个回到 4 个（Claude Code + Codex + Hermes + ChatMemo，老项目都已实现），新增 daily/weekly 子命令、observer state、真实输出样本 `samples/expected-real-output/`；axiom schema 采用老项目验证过的"置信度/执行要求/反例"三件套作为 minimum viable，plan v0.8.6 七字段降为 stretch goal；（5）§3.3 C7 增量记忆从 P2 升 P1（最小实现 observer state 文件支撑 daily 增量）；（6）§6 新增 §6.0：S-0.5 老项目抽提是 v1 主线工作量，S00/S0/S1 demo 三件套因有真实输出样本可借而缩水，S4–S9 代码量降 60%，新增 S9.5 daily/weekly 子命令封装。**核心反转**：plan v0.8.5 砍 scope（2 adapter）、v0.8.6 硬化字段，v0.9 反向扩 scope——但增量代码量反而降 60%，因为大部分代码不是新写而是从老项目抽 + 通用化。**plan 重新冻结**，下一步动手 S-0.5 抽老项目。**未对齐章节**（v1 实现阶段渐进对齐，不在 v0.9 修订范围）：§2.4 与母体项目关系（v0.9 抽提范围比模型 A 原定更激进）、§4.2 axiom 字段细节（七字段 vs 三件套 reconciliation）、§5.x P1 模块细节、§6 表格内 S00–S13 具体描述。这些章节冲突以 v0.9 / §6.0 口径为准 | 用户 D1+D2+D3 拍板 + 对比老项目 (本会话) |
