# Learn Skill

English | [简体中文](README.md)

`learn` is a unified learning coach and structured study toolkit for AI coding agents. It turns “I want to learn X” into an active, testable, and reviewable process centered on observable mastery, active recall, teach-back, and real artifacts.

## Capabilities

- Five-level Learning Ladder
- A practical 20-hour plan split into 10 sessions
- One-question-at-a-time Edge Quiz
- Five-minute One-Page Cheat Sheet
- Five-resource curation and a seven-day Resource Path
- A bounded, three-round Feynman teach-back loop
- First Principles, Simon-Style Mastery, SQ3R, Pomodoro, and Cornell Notes
- Spaced Review, Quick Active Recall, Smart Summary, and Weakness Diagnosis

## Repository structure

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

`SKILL.md` defines routing and execution contracts. `references/templates.md` contains learning templates loaded on demand, while `evals/evals.json` provides 12 behavioral evaluation cases.

## Installation

Clone the repository:

```powershell
git clone https://github.com/Arthur19940725/learn-skill.git
```

Copy `learn/` into the skill directory used by your agent:

```powershell
# Codex
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.codex\skills\learn"

# Shared agents directory
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.agents\skills\learn"

# Claude Code
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.claude\skills\learn"
```

Restart the client or open a new session so it can rediscover the skill.

## Example prompts

```text
Use $learn to build a five-level learning ladder for Go concurrency from beginner to independent problem solving.
```

```text
Use $learn to test my understanding of Python decorators like a strict examiner, one question at a time.
```

```text
Use $learn to create a practical 20-hour plan for learning how to containerize a Web API with Docker.
```

```text
Use $learn and the Feynman method to help me truly understand database transaction isolation levels.
```

## Design principles

- Define progress through behavior, artifacts, or tests instead of vague claims of understanding.
- Advance only one question or teach-back step at a time in interactive modes.
- Treat fixed durations as planning boundaries, never as guarantees of mastery.
- Verify current resources and label anything unverifiable as `unverified`.
- Choose one primary method by default and combine methods only when they address distinct bottlenecks.

## Validation

The included evaluations cover:

- Fixed counts, durations, and required fields
- Single-question boundaries in interactive modes
- Resource verification and direct-source requirements
- Observable deliverables and completion criteria
- Diagnosis, review, and transfer

You can run the basic validator bundled with Codex `skill-creator`:

```powershell
python <skill-creator-path>\scripts\quick_validate.py .\learn
```
