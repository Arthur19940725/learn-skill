# Learn Skill

[English](README.en.md) | 简体中文

`learn` 是一个面向 AI coding agents 的统一学习教练与结构化学习工具包。它把“我想学 X”转化为可执行、可检查、可复习的学习过程，重点关注 observable mastery、active recall、teach-back 和真实产物。

## 核心能力

- 五级 Learning Ladder
- 20 小时 / 10 sessions 实战计划
- 一次一题的渐进式 Edge Quiz
- 5 分钟 One-Page Cheat Sheet
- 精选 5 个资源与 7 天 Resource Path
- 最多三轮的 Feynman teach-back
- First Principles、Simon-Style Mastery、SQ3R、Pomodoro、Cornell Notes
- Spaced Review、Quick Active Recall、Smart Summary、Weakness Diagnosis

## 目录结构

```text
learn/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── evals/
│   └── evals.json
└── references/
    └── templates.md
```

`SKILL.md` 包含路由和执行契约；`references/templates.md` 提供按需加载的学习模板；`evals/evals.json` 包含 12 组行为评测。

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

```text
使用 $learn 为零基础的我设计一个 Go concurrency 五级学习阶梯。
```

```text
使用 $learn 像严格考官一样测试我的 Python decorators，一次只问一题。
```

```text
使用 $learn 给我一个 20 小时学会用 Docker 容器化 Web API 的实战计划。
```

```text
使用 $learn 用费曼方法帮我真正理解数据库事务隔离级别。
```

## 设计原则

- 用行为、作品或测试定义进步，不用“理解了”作为完成标准。
- 互动模式一次只推进一个问题或一次 teach-back。
- 固定时长只作为计划边界，不承诺必然 mastery。
- 当前资源必须核验；无法验证的信息明确标记 `unverified`。
- 默认选择一个最匹配瓶颈的方法，仅在职责互补时组合。

## 验证

仓库中的评测覆盖：

- 固定数量、时间与字段约束
- 互动模式的单问题边界
- 资源核验与直接链接要求
- 可观察的 deliverable 和 completion criteria
- 诊断、复习与迁移能力

可使用 Codex `skill-creator` 附带的验证脚本检查基本结构：

```powershell
python <skill-creator-path>\scripts\quick_validate.py .\learn
```

