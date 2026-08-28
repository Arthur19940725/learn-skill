# Supplemental learning methods

Use this file only to strengthen a canonical workflow. Do not replace or alter the counts, sections, or interaction rules in `core-workflows.md`.

## Diagnose the bottleneck

Choose the smallest useful intervention:

| Bottleneck | Method | Coaching action |
|---|---|---|
| A broad field with no route | Goal decomposition | Define an observable outcome, map prerequisites, and create staged deliberate practice |
| Dense reading material | SQ3R | Survey, question, read, recite, and review |
| Notes are passive or disorganized | Cornell notes | Turn notes into cues, questions, summaries, and recall prompts |
| Procrastination or weak focus | Timeboxing | Assign one concrete outcome to each focus block and record interruptions |
| Illusion of understanding | Feynman teach-back | Require a plain-language explanation, expose gaps, and repair only weak parts |
| Weak retention | Retrieval and spacing | Recall without looking, revisit after delays, and interleave related skills |
| Inefficient study method | First-principles diagnosis | Trace whether the learner is actively constructing, restructuring, and applying knowledge |

Do not apply every method at once. Select one or two that address the current constraint.

## Goal decomposition and deliberate practice

1. Anchor learning to a real-world outcome.
2. Narrow the field to the knowledge and skills that outcome actually requires.
3. Break the path into prerequisite-ordered chunks.
4. Give each chunk a performance task and fast feedback.
5. Advance only after observable evidence, not mere exposure.

Prefer one cumulative project because it exposes integration gaps and creates a realistic artifact.

## SQ3R for reading

Use for books, papers, articles, documentation, or course material:

1. **Survey** — scan the title, headings, diagrams, abstract, introduction, conclusion, and exercises to build a map.
2. **Question** — rewrite each major heading as a question.
3. **Read** — read to answer those questions rather than to finish pages.
4. **Recite** — close the source and answer from memory in the learner's words.
5. **Review** — revisit missed questions after a delay and connect them to the larger map.

When the user supplies material, start by extracting its structure and generating the questions. If the material cannot be accessed, state what is unavailable.

Preserve the source boundary throughout the session:

- Label direct source claims, reasonable inferences, and outside background knowledge separately.
- Attach page, section, heading, paragraph, timestamp, or code-location evidence whenever the source provides it.
- Do not fill recall answers, teach-back text, remaining gaps, or completion status before the learner supplies closed-source evidence.
- If a missing or inaccessible passage could change the conclusion, stop at that boundary and request the passage instead of silently completing it.

## Cornell notes

Use notes as a retrieval tool, not a transcript:

```markdown
## Topic

| Cue / Question | Notes |
|---|---|
| What must I recall? | Concise explanation, example, formula, or trap |

### Summary
Write 3-5 sentences in the learner's own words.

### Recall prompts
- Question 1
- Question 2
```

During review, hide the notes column and answer from the cue column. Add a concept to a glossary only after the learner can use it correctly.

## Focus blocks

Default to 25 minutes of focused work plus 5 minutes of rest; use 50/10 for deeper work when appropriate. Each block needs:

- One task
- One visible deliverable
- A rule to record interruptions and return to the task
- A short review of what was completed and what blocked progress

Treat the timing ratio as adjustable. The value comes from single-task focus and feedback, not the timer itself.

## Retention and transfer

Distinguish fluent recognition from durable learning:

- **Retrieval practice** builds recall by answering without looking.
- **Spacing** revisits knowledge after increasing delays.
- **Interleaving** mixes related problem types so the learner must select the method.
- **Application** tests whether knowledge transfers to a new context.
- **Error logs** record the cause of an error, the correction, and a future discrimination cue.

Match difficulty to the learner's zone of proximal development: challenging enough to require effort, but small enough that feedback can repair the gap.

For an explicit spaced-review request, turn the material into about 10–20 atomic recall units with stable IDs. Default to D0, D1, D3, D7, D14, D30, D60, and D120; shorten the next interval after a failed unit and lengthen it only after successful closed-book retrieval. Later reviews should use comparison, diagnosis, application, or transfer rather than repeating identical wording. Output a calendar-ready checklist or the learner's requested tool format.

## Error notebook and delayed retest

Create an error entry only from evidence in the learner's answer, explanation, code, or other work. Do not turn a generic common mistake into a claimed personal weakness.

Use this compact schema:

| Field | Record |
|---|---|
| Prompt or task | What the learner was trying to answer or do |
| Original answer | The learner's exact answer or weak phrase; quote only the minimum needed |
| Gap type | Factual error, missing causal link, transfer failure, or unclear expression |
| Correction | The smallest accurate rule or explanation that repairs the gap |
| Real example | One concrete case showing the correction in use |
| Discrimination cue | How to recognize this case and avoid the same error next time |
| Retest | One closed-book question or task for a later attempt |

Retest after a delay rather than immediately repeating the same wording. Default to D+3 when no schedule is given, then keep, revise, or close the entry based on the learner's new answer. A correct answer closes the specific entry; it does not prove mastery of untested material.

## First-principles learning diagnosis

When the user asks whether a learning method or plan is effective, trace this chain:

1. **Self-direction** — Is the learner pursuing a concrete outcome or relying only on external instruction?
2. **Induction** — Are they extracting transferable patterns instead of accumulating disconnected facts?
3. **Self-output** — Are they producing answers, artifacts, or explanations rather than copying?
4. **Expression restructuring** — Can they reorganize the idea in their own model?
5. **Causal understanding** — Can they explain why the steps or relationships hold?
6. **Practice verification** — Can they demonstrate the idea in a minimal real task?

Report:

- The specific bottleneck and evidence
- One to three immediately actionable changes
- How each change will be tested

Avoid unsupported numerical claims about efficiency improvement. Estimate time or return only when the assumptions and calculation are explicit.

## Explanation refinements

For a plain-language explanation:

- Define every unavoidable jargon term immediately.
- Prefer concrete examples over abstract restatements.
- Include one common misconception when it prevents a likely error.
- State the key insight in one sentence.
- Offer a 30-second version only when useful.
- Explain where an analogy fails so it does not become a new misconception.
