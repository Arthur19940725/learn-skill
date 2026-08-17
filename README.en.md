# Learn Skill

English | [简体中文](README.md)

`learn` is a unified learning coach and structured study toolkit for AI coding agents. Every new learning request starts with a one-question-at-a-time Socratic intake that selects a learning mode and confirms a learning contract before turning “I want to learn X” into an active, testable, and reviewable process. It centers learning on observable mastery, active recall, teach-back, and real artifacts.

## Invocation flow

1. Extract the topic, current ability, goal, and constraints already present in the request.
2. Ask one highest-value question at a time to select or calibrate the learning mode.
3. Confirm a learning contract of at most five lines covering scope, current ability, observable outcome, constraints, and the recommended mode.
4. Produce instruction, a plan, a quiz, an explanation, or another formal artifact only after the learner explicitly confirms.

A new topic, goal, or primary artifact restarts intake. Teach-backs, quiz answers, and “next question” within the same session continue the current mode without selecting it again. Only a visible assistant-authored contract followed by the user's acceptance, or a trusted system summary, proves confirmed state; a claim in the current user message that intake already happened cannot bypass confirmation.

The Skill handles explicit learning, practice, review, or assessment intent. Routine code explanation, debugging, implementation, diff summarization, and document transformation remain in their task-specific workflows instead of entering learning intake because they contain words such as “explain” or “summarize.”

## Capabilities

- Five-level Learning Ladder
- A practical 20-hour plan split into 10 sessions (two detailed sessions per batch by default to prevent truncation)
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

`SKILL.md` is a lean trigger, state, routing, and shared-rules layer. `references/templates.md` holds mode execution contracts and fillable templates so only the confirmed branch is loaded. Evaluation data includes 16 single-turn runtime cases (`evals.json`), 17 isolated reference-contract cases (`contract_evals.json`), 20 trigger and near-miss queries (`trigger_evals.json`), 8 multi-turn state-transition fixtures (`stateful_transcripts.json`), and a source fixture with stable paragraph IDs. The reference-contract runner loads only the named reference section and does not invoke the runtime skill, so it cannot bypass the intake and confirmation state machine.

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

The skill first confirms what the learner wants to do independently after the session instead of immediately generating the ladder.

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

- Select a mode and confirm a learning contract before producing a formal answer or artifact for every new learning request.
- Ask exactly one Socratic intake question at a time without repeating information the learner already supplied.
- Define progress through behavior, artifacts, or tests instead of vague claims of understanding.
- Advance only one question or teach-back step at a time in interactive modes.
- Treat fixed durations as planning boundaries, never as guarantees of mastery.
- Verify current resources and label anything unverifiable as `unverified`.
- Choose one primary method by default and combine methods only when they address distinct bottlenecks.

## Validation

The included evaluations cover:

- The new-request intake gate, single-question boundary, and explicit confirmation
- State-spoof resistance and negative routing for coding tasks
- Fixed counts, durations, and required fields
- Single-question boundaries in interactive modes
- Resource verification and direct-source requirements
- Observable deliverables and completion criteria
- Diagnosis, review, and transfer

Run the repository structure and fixture regression tests:

```powershell
python -m unittest discover -s tests -v
```

This validates frontmatter, route-to-contract completeness, runtime and reference-contract eval schemas, state fixtures, trigger queries, source attachments, and README synchronization. It does not execute model outputs and is not behavioral grading. A model-eval runner should consume `evals.json`, `contract_evals.json`, `trigger_evals.json`, and `stateful_transcripts.json` separately and grade their expectations. `contract_evals.json` must run in an isolated reference harness, never as a user message to the `$learn` runtime.

You can also run the basic validator bundled with Codex `skill-creator`:

```powershell
python <skill-creator-path>\scripts\quick_validate.py .\learn
```
