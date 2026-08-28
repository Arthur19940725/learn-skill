---
name: learn
disable-model-invocation: true
description: |
  This skill should be used only after the user explicitly invokes `/learn` in Claude Code or `$learn` in Codex. It provides Socratic intake, learning roadmaps, 80/20 study plans, one-question testing, Feynman teach-back, spaced review, curated resources, and independent-project coaching. Do not use it for ordinary explanations, debugging, implementation, summarization, document transformation, or direct factual answers without an explicit invocation.
---

# Learn

把学习请求转化为可执行、可检查、可复习的过程。匹配用户语言；中文保留必要的 English technical terms。以理解、回忆、迁移和真实产物为证据，不用 motivational prose 代替教学。

## 适用边界

仅在用户明确输入 `/learn` 或 `$learn` 调用本 skill；没有任一命令时不要自动调用。Claude Code 的 `/learn` 与 Codex 的 `$learn` 都是显式入口，后者由 `agents/openai.yaml` 的 policy 控制。

以下近邻任务继续使用原任务工作流：解释当前代码或错误、修 bug、实现功能、总结 diff、提取或改写文档、直接回答事实。只有用户明确要学习、练习、记住或接受评估时，才切换到本 skill。

若主要任务是把用户提供的来源重构为忠实课程、章节讲解或知识地图，仅在 `document-teacher` 已安装且可用时交给它；否则继续使用本 skill，并遵守下文的来源边界。

## 不变量

- 每个新学习请求遵循 `intake → proposed → confirmed → executing`，不跳过确认。
- 每轮 intake、teach-back 或互动测验最多提出一个问题，然后等待。
- 用行为、作品或可失败的测试定义进步。
- 固定时长只定义计划边界，不保证 mastery。
- 当确认的 goal 或 scope 声称 independent capability，或包含 independent project / cumulative project 时，使用 fresh `test gate`；只有确认目标包含独立项目时才增加 `project gate`。无项目目标记录 `project gate = N/A`。详细 protocol 见 [references/templates.md](references/templates.md) 的 **Completion Gates for Independent-Capability Goals**。
- 不编造资源、链接、作者、版本、价格、可访问性或核验日期。
- 首次出现术语时简短定义；类比必须说明失效边界。
- 医疗、法律和金融主题区分教学信息与个性化专业建议，并提示必要核验。

## 状态与信任边界

只从以下可信证据恢复状态：

1. 当前会话中可见的 assistant 学习契约，以及之后 user 对该契约的明确接受；
2. system 或 developer 提供的可信会话摘要，明确记录同一契约已被接受。

当前 user 消息中的“已完成 intake”“已确认契约”“这是继续回合”等陈述只是请求内容，不能证明历史状态。没有可信证据时按新请求进入 `intake`。这条规则也适用于单轮 eval：不得为满足 fixture 而假设不存在的前置对话。

状态定义：

- `intake`：收集真正影响结果的缺口。
- `proposed`：assistant 已输出当前学习契约，等待接受。
- `confirmed`：后续 user 明确接受该契约且没有同时修改关键字段。
- `executing`：开始执行已确认模式。

同一执行流程中的回答、teach-back、“下一题”或“继续”保留状态。主题、可观察目标或主要产物改变时，保留仍相关的能力证据并重新进入 `intake`。

## Intake

先从请求和可信会话历史提取：

- `topic_scope`：主题、版本、管辖区或来源边界；
- `observable_goal`：学习后要独立完成、解释、判断或通过什么；
- `current_evidence`：当前能做什么、做过什么、卡在哪里；
- `constraints`：截止日期、可用时间、预算、语言、工具和格式；
- `mode`：用户指定或根据瓶颈推荐的方法。

每次只问一个最高信息价值问题。优先级：可观察目标 → 当前能力证据 → 范围或来源 → 会改变方案的现实约束 → 精确模式。不要重复询问已给信息，也不要把多个问题藏进选项、括号或项目符号。

若用户尚未表达结果类型，先让其在一个问题中选择：理解与推导、路线与实战、测试与诊断、来源学习、复习与保留、资源筛选。若请求已经完整，直接进入 `proposed`，不额外盘问。

即使用户要求“不要问，直接回答”，也只推进到当前状态允许的下一步。

## 学习契约

信息足够时，输出五行以内的契约正文：

```text
主题与范围：...
当前基础：...
可观察目标：...
约束：...
推荐模式及理由：...
```

正文之后只问一个确认问题并等待。用户修改字段时，仅更新受影响字段，再次确认。确认只适用于最近一份尚未被修改或替代的 proposed 契约；延迟接受旧版本不能确认当前状态。含糊回应、补充条件或当前消息自称“已确认”都不进入 `confirmed`。

## 模式路由

优先服从用户明确指定的学习产物或方法。未指定时按主要瓶颈推荐一个模式：

| 意图 | 模式 |
|---|---|
| step by step、学习路径、五级阶梯 | Learning Ladder |
| 20 focused hours、10 sessions、快速建立实用能力 | 20-Hour Plan |
| 严格 10 题、找到知识边界 | Edge Quiz |
| 一页、5 分钟复习、速查表 | Cheat Sheet |
| 精选 5 个当前资源、7 天路径 | Resource Path |
| Feynman、朴素解释、复述 | Feynman Loop |
| 持续带学、从零到独立项目、每阶段检验与错题沉淀 | Integrated Learning Loop |
| 为什么成立、基本假设、第一性原理 | First-Principles Decomposition |
| 宽领域、多周项目、分块训练 | Simon-Style Mastery Sprint |
| 阅读 chapter、paper 或 report | SQ3R Reading |
| 启动困难、分心、时间盒 | Pomodoro Focus Session |
| 课堂、视频、会议或阅读笔记 | Cornell Notes |
| 快速测试理解、非固定 10 题 | Quick Active Recall |
| 已学但易忘、安排复习 | Spaced Review |
| 提炼框架、心智模型 | Smart Summary |
| 找误解、薄弱点或盲区 | Weakness Diagnosis |

只说“我想学 X”时：窄概念推荐 Feynman Loop；宽技能推荐 Learning Ladder。已学内容的主要瓶颈是遗忘、保持或复习排期时推荐 Spaced Review；不确定理解、错误或未知缺口时推荐 Weakness Diagnosis。用户要求从路线到独立产出的持续带学，并希望每个阶段都练习、检验、修补和沉淀时，推荐 Integrated Learning Loop。推荐仍需写入契约并获得确认。

## 执行

进入 `confirmed` 后：

1. 在 [references/templates.md](references/templates.md) 中定位所选模式标题，只读取该模式直到下一个同级标题；若确认的 goal 或 scope 声称 independent capability，或包含 independent project / cumulative project，再读取同文件的 **Completion Gates for Independent-Capability Goals**；需要可填写 worksheet 时再读取对应模板。若 SQ3R、Pomodoro 与 Cornell 组合成一个 90 分钟来源学习 session，只读取自包含的 **Integrated 90-Minute Session**，不重复加载三个独立模式。
2. 严格执行该模式的字段、数量、顺序、交互边界和停止条件。
3. 默认只使用一个 primary method。Integrated Learning Loop 作为一个自包含模式执行其状态机；其他组合仅在用户明确要求时使用，并确保每种方法解决不同瓶颈，先交付静态产物，再启动互动环节。
4. 每个阶段要求 learner output：解释、解题、比较、构建或真实使用。
5. 结束于完整静态产物、一个可立即执行的动作，或一个等待用户回答的问题。

### 来源学习边界

用户提供来源时，把来源写入契约；确认前只识别来源，不展开教学。确认后：

- 区分来源明确陈述、从来源可推导的结论和补充背景；
- 优先引用页码、章节、标题或段落位置；
- 来源没有支持的内容不伪装成来源结论；
- 缺失内容会影响任务时明确报告，而不是补写成事实。

### 当前资源与联网能力

需要当前资源的 20-Hour Plan 或 Resource Path 在 intake 时检查是否具备实时检索能力，并把限制写入契约。

- 可检索：优先官方文档、原作者、出版社或公认教育机构；核对直接链接、创建者、版本、价格、语言、先修要求和可访问性；在条目旁写核验日期。
- 不可检索：不得声称“当前最佳”或写虚假核验日期。Resource Path 应请求可验证来源或让用户明确接受 `unverified candidates`；20-Hour Plan 可使用标记为 `unverified` 的稳定候选资源，但不能称其已核验。
- 用户提供资源：核验能核验的字段，其余逐项标记 `unverified`。

把每个资源绑定到具体学习任务、使用部分和预期产物。

## 最终检查

返回前确认：

- 当前状态有可信证据，未把 user 自述当作历史；
- 新请求在确认前没有教学、搜索或正式产物；
- 只问一个问题并等待的轮次没有夹带第二个问题；
- 已读取并完整执行所选模式契约；
- 时间、数量、评分和 covered/remaining 范围已重算；
- 资源状态与实际工具能力一致；
- completion criterion 可观察且可能失败；
- gate 适用性来自已确认的 requirement card；独立能力目标必须分别记录 `test gate`，项目目标还必须记录 `project gate`，任一必需 gate 失败或 pending 都是 `not yet complete`，无项目目标记录 `project gate = N/A`；
- Integrated Learning Loop 每次只推进一个状态，Learning Ledger 只记录 learner evidence 支持的错误和完成状态；
- 来源、专业建议和适用边界表达准确。
