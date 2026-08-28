# Learn Skill

[English](README.en.md) | 简体中文

`learn` 是一个面向 AI coding agents 的统一学习教练与结构化学习工具包。显式使用 `$learn`（Codex）或 `/learn`（Claude Code）调用后，每次新的学习请求都会先通过一次一问的苏格拉底式 intake 选择学习模式、确认学习契约，再把“我想学 X”转化为可执行、可检查、可复习的学习过程。普通学习措辞不会自动调用本 skill。它重点关注 observable mastery、active recall、teach-back 和真实产物。

## 调用流程

1. 从请求中提取已经明确的主题、基础、目标和约束。
2. 一次只问一个最高价值的问题，帮助学习者选择或校准学习模式。
3. 用不超过五行的学习契约确认主题范围、当前基础、可观察目标、约束和推荐模式。
4. 学习者明确确认后，才生成课程、计划、测验、讲解或其他正式产物。

新的主题、目标或主要产物会重新进入 intake；同一会话中的 teach-back、测验作答和“下一题”会继续当前模式，不重复选择。只有当前会话中可见的 assistant 学习契约及后续 user 确认，或可信系统摘要，才能证明状态已确认；user 在当前消息中自称“已完成 intake”不能跳过确认。

Skill 只在显式调用后处理学习、练习、复习或评估意图：Claude Code 使用 `/learn`，Codex 使用 `$learn`；普通学习措辞不会自动调用本 skill。普通代码解释、调试、实现、diff 总结和文档转换继续使用对应任务工作流，不会因为出现“解释”或“总结”就进入学习 intake。

## 核心能力

- 五级 Learning Ladder
- 20 小时 / 10 sessions 实战计划（默认每批 2 个完整 session，避免截断）
- 一次一题的渐进式 Edge Quiz
- 5 分钟 One-Page Cheat Sheet
- 精选 5 个资源与 7 天 Resource Path
- 最多三轮的 Feynman teach-back
- Integrated Learning Loop：地图 → 关键少数 → 练习 → 测验 → 修补 → Learning Ledger → Ship；项目目标使用独立的 test/project gates
- First Principles、Simon-Style Mastery、SQ3R、Pomodoro、Cornell Notes
- Spaced Review、Quick Active Recall、Smart Summary、Weakness Diagnosis

## 目录结构

```text
learn/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── evals/
│   ├── evals.json
│   ├── contract_evals.json
│   ├── trigger_evals.json
│   ├── stateful_transcripts.json
│   └── files/
│       └── source-grounding-fixtures.md
└── references/
    └── templates.md
tests/
├── __init__.py
├── skill_validation.py
├── test_skill.py
└── test_skill_validation.py
```

`SKILL.md` 是精简的触发、状态、路由与共用规则；`references/templates.md` 按模式保存执行契约和可填写模板，确认后只加载所选部分。评测数据分为 16 组 runtime 单轮评测（`evals.json`）、18 组隔离的 reference-contract 评测（`contract_evals.json`）、22 组触发/近邻负向查询（`trigger_evals.json`）、11 组多轮状态转换 fixture（`stateful_transcripts.json`），以及带稳定段落标识的来源 fixture。reference-contract runner 只加载指定参考章节，不调用 runtime skill，因此不会绕过 intake 与确认状态机。

## 安装

克隆仓库：

```powershell
git clone https://github.com/Arthur19940725/learn-skill.git
```

选择你的 agent skill 目录，并复制 `learn/`：

```powershell
# Codex
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.codex\skills\learn"

# 通用 agents 目录
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.agents\skills\learn"

# Claude Code
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.claude\skills\learn"
```

重新启动对应客户端或开启新会话，使其重新发现 skill。

## 使用示例

以下示例使用 Claude Code 的 `/learn`；Codex 用户将示例中的 `/learn` 替换为 `$learn`。

```text
使用 /learn 为零基础的我设计一个 Go concurrency 五级学习阶梯。
```

Skill 会先确认“完成这次学习后，你希望能独立做到什么”，而不是立即生成阶梯。

```text
使用 /learn 像严格考官一样测试我的 Python decorators，一次只问一题。
```

```text
使用 /learn 给我一个 20 小时学会用 Docker 容器化 Web API 的实战计划。
```

```text
使用 /learn 用费曼方法帮我真正理解数据库事务隔离级别。
```

```text
使用 /learn 从零持续带我学 Python CLI：先画地图，只学关键少数，每块练习和测试，卡住时修补，完成后更新错题速查表。
```

## 设计原则

- 每个新学习请求先选择模式并确认学习契约，再生成正式答案或产物。
- 苏格拉底式 intake 一次只问一个问题，不重复询问已提供的信息。
- 用行为、作品或测试定义进步，不用“理解了”作为完成标准。
- 互动模式一次只推进一个问题或一次 teach-back。
- 固定时长只作为计划边界，不承诺必然 mastery。
- 当前资源必须核验；无法验证的信息明确标记 `unverified`。
- 默认选择一个最匹配瓶颈的方法，仅在职责互补时组合。
- 端到端带学一次只推进一个状态，错题和完成状态必须来自学习者实际输出。
- 只有确认目标包含独立项目时才启用 project gate；项目目标必须同时通过 fresh test gate 与 independent project gate；无项目目标记录 `Project gate: N/A`。
- `/learn` 与 `$learn` 都是显式入口，Skill 不会因普通学习措辞自动调用。

## 验证

仓库中的评测覆盖：

- 新请求的 intake gate、单问题边界与显式确认
- 状态伪造防护与代码任务负向路由
- 固定数量、时间与字段约束
- 互动模式的单问题边界
- 资源核验与直接链接要求
- 可观察的 deliverable 和 completion criteria
- 诊断、复习与迁移能力

运行仓库结构与 fixture 回归测试：

```powershell
python -m unittest discover -s tests -v
```

此命令验证 frontmatter、路由到模式契约的完整性、runtime 与 reference-contract eval schema、状态 fixture、触发查询、来源附件和 README 同步；它不会执行模型输出（does not execute model outputs），也不等同于行为评分。模型行为评估应由 agent runner 分别消费 `evals.json`、`contract_evals.json`、`trigger_evals.json` 和 `stateful_transcripts.json`，并按各自 expectations 评分。`contract_evals.json` 必须由隔离 reference harness 运行，不得作为 user 消息送入 `$learn` runtime。

也可使用 Codex `skill-creator` 附带的验证脚本检查基本结构；若脚本版本尚不认识 Claude Code 的 `disable-model-invocation` 扩展字段，应先更新脚本，或以仓库测试中的严格 parser 为准：

```powershell
python <skill-creator-path>\scripts\quick_validate.py .\learn
```

