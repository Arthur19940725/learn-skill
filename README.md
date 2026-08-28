# Learn Skill

[English](README.en.md) | 简体中文

`learn` 是面向 AI coding agents 的实用学习教练。它根据用户的真实意图，在五级路线、20 小时计划、分级测验、一页速查表、资源筛选、费曼复述，以及阅读、专注、复习和错题支持之间选择最小充分路径。

Skill 以可观察能力为目标：学习者能解释、解题、构建、判断或迁移什么。信息足够时直接开始；只有缺失信息会实质改变结果时，才问一个阻塞问题。

## 核心能力

- **先画地图**：宽主题先生成从零基础到独立项目的五级路线。
- **抓关键少数**：20 小时计划先给 10 节紧凑地图，默认只详细展开接下来的 1–2 节。
- **分级测验**：普通测试使用 3–7 题 Quick Active Recall；明确寻找知识边界时使用 10 题 Edge Quiz；系统查缺补漏使用 8–12 题 Weakness Diagnosis。
- **证据型错题本**：只记录学习者真实答案、代码、复述或作品暴露的问题，并默认安排 D+3 复测。
- **一页速查表**：中文默认约 400–700 字符，英文默认约 350–600 词。
- **资源做减法**：目标为 5 个高价值资源；合格资源不足时说明缺口，不用弱项凑数，也不会自动追加不需要的七天日程。
- **费曼闭环**：简明解释、学习者复述、定位具体缺口、只修补弱项，最多三轮。
- **来源与复习边界**：区分原文、推断和外部背景；支持 SQ3R、Cornell notes、focus blocks 和 D0/D1/D3/D7 等间隔复习。

## 目录结构

```text
learn/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── evals/
│   └── evals.json
└── references/
    ├── core-workflows.md
    └── supplemental-methods.md
tests/
├── __init__.py
├── skill_validation.py
├── test_skill.py
└── test_skill_validation.py
```

- `SKILL.md`：触发、路由、可信状态和交互边界。
- `core-workflows.md`：六个完整工作流的权威输出契约。
- `supplemental-methods.md`：阅读、笔记、专注、复习、错题和学习方法诊断。
- `evals.json`：23 个行为场景，覆盖正向、续接、约束和负向路由。

## 安装

```powershell
git clone https://github.com/Arthur19940725/learn-skill.git
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.codex\skills\learn"
```

也可以把 `learn/` 复制到客户端支持的其他 skill 目录。复制后重新启动客户端或开启新会话，让客户端重新发现 Skill。

## 示例

```text
使用 $learn，把 Python 从零基础到独立项目拆成五个等级。
```

```text
我只有 20 小时学视频剪辑，请先找出最重要的 20%，再给我路线。
```

```text
考考我对 Transformer attention 的理解，一次只问一道题。
```

```text
根据我刚才的错误整理一条错题记录，并安排复测。
```

```text
只筛选最值得看的 5 个 LangGraph 官方资源，不要日程。
```

## 设计原则

- 宽主题先给地图，窄问题直接解释。
- 不把每个学习请求都变成长计划。
- 一次只问一道测验题或一个 teach-back 问题。
- 不把讲过、看过或用户自称掌握当成能力证据。
- 只从当前会话可见内容或可信摘要续接学习状态。
- 当前资源、版本、价格和可访问性需要实时核验；无法核验时明确标记。
- 来源明确陈述、合理推断和外部背景分别标注。

## 验证

运行仓库测试：

```powershell
python -m unittest discover -s tests -v
```

运行 Codex Skill Creator 基础校验：

```powershell
python <skill-creator-path>\scripts\quick_validate.py .\learn
```

仓库测试会检查 frontmatter、文件结构、Markdown 链接、六个核心契约、23 个评测场景、可信状态、测验分级、计划分批展开、资源约束和双语 README 同步。它 **does not execute model outputs**；真实模型行为仍需由 agent runner 逐条运行 `evals/evals.json` 并评分。
