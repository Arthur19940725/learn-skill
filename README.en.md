# Learn Skill

English | [简体中文](README.md)

`learn` is a practical learning coach for AI coding agents. It selects the smallest sufficient path among a five-level map, a 20-hour plan, tiered assessment, a one-page cheat sheet, resource curation, Feynman teach-back, and focused support for reading, attention, review, or mistake repair.

The Skill optimizes for observable competence: what the learner can explain, solve, build, decide, or transfer. It begins immediately when the request contains enough context and asks one blocking question only when the missing answer would materially change the result.

## Core capabilities

- **Map before details**: broad topics start with a five-level route from complete beginner to independent project work.
- **High-leverage focus**: a 20-hour plan starts with a compact 10-session map and expands only the next one or two sessions by default.
- **Tiered assessment**: ordinary checks use 3–7 Quick Active Recall questions; explicit knowledge-boundary tests use a 10-question Edge Quiz; systematic gap finding uses an 8–12 question Weakness Diagnosis.
- **Evidence-based error notebook**: records only gaps shown in the learner's answers, code, teach-back, or artifacts, with a D+3 retest by default.
- **One-page review**: defaults to roughly 400–700 Chinese characters or 350–600 English words.
- **Resource subtraction**: targets five high-value resources, reports a shortfall instead of padding with weak candidates, and adds a seven-day schedule only when requested or useful.
- **Feynman loop**: explain simply, request a teach-back, identify exact gaps, and repair only weak parts for at most three rounds.
- **Source and retention boundaries**: separates source claims, inference, and outside background; supports SQ3R, Cornell notes, focus blocks, and spaced review such as D0/D1/D3/D7.

## Repository structure

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

- `SKILL.md` defines triggering, routing, trusted state, and interaction boundaries.
- `core-workflows.md` is the authoritative contract for the six full workflows.
- `supplemental-methods.md` covers reading, notes, focus, retention, error repair, and learning-method diagnosis.
- `evals.json` contains 23 behavioral scenarios covering positive routing, continuation, constraints, and a negative control.

## Installation

```powershell
git clone https://github.com/Arthur19940725/learn-skill.git
Copy-Item -Recurse -Force .\learn-skill\learn "$HOME\.codex\skills\learn"
```

You can also copy `learn/` into another skill directory supported by your client. Restart the client or open a new session so it can rediscover the Skill.

## Examples

```text
Use $learn to split Python into five levels from complete beginner to independent project work.
```

```text
I have 20 hours to learn video editing. Identify the highest-leverage 20% before building the plan.
```

```text
Test my understanding of Transformer attention, one question at a time.
```

```text
Turn the mistake I just made into one error-notebook entry and schedule a retest.
```

```text
Give me the five highest-value official LangGraph resources and no study schedule.
```

## Design principles

- Map broad topics before teaching details; explain narrow concepts directly.
- Do not turn every learning request into a long plan.
- Ask one assessment or teach-back question at a time.
- Do not treat exposure, explanation, or a mastery claim as competence evidence.
- Resume learning state only from visible conversation evidence or a trusted summary.
- Verify current resources, versions, prices, and availability; label anything unverified.
- Separate explicit source claims, reasonable inference, and outside background.

## Validation

Run the repository tests:

```powershell
python -m unittest discover -s tests -v
```

Run the basic Codex Skill Creator validator:

```powershell
python <skill-creator-path>\scripts\quick_validate.py .\learn
```

The repository suite checks frontmatter, structure, Markdown links, six core contracts, 23 evaluation scenarios, trusted state, tiered assessment, staged plans, resource constraints, and README synchronization. It **does not execute model outputs**; an agent runner must execute and grade the cases in `evals/evals.json` to measure real model behavior.
