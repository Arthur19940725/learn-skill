# Canonical learning workflows

This file is the authoritative output contract derived from the user-provided `learn_skill.md`. Replace bracketed fields from the user's context. Preserve exact counts and interactive stopping points.

## 1. Build a learning ladder

Use when the learner wants to study `[topic]` step by step without skipping essential foundations.

Gather or infer:

- Current level, defaulting to complete beginner
- Goal or real-world use case
- Time available
- Constraints or preferences

Build a five-level learning ladder from complete beginner to independent project-ready practitioner before deep teaching. If the goal is too broad for one ladder, narrow the scope explicitly before building it.

Organize concepts in prerequisite order. For each level, include:

1. Level name
2. What the learner should understand
3. The highest-leverage concepts or skills
4. What observable mastery looks like
5. One hands-on exercise or mini-project
6. One measurable milestone proving readiness to advance
7. Common mistakes and how to correct them
8. One self-check question

Use exactly these levels:

- Level 1: Complete Beginner
- Level 2: Basic Understanding
- Level 3: Practical User
- Level 4: Problem Solver
- Level 5: Independent Project Builder

After the ladder, include:

- Prerequisites the learner may be missing
- The recommended starting level and why
- The critical 20% to focus on first, with a brief reason for each item
- The next concrete action to take today

Keep the advice practical, beginner-friendly, and specific to the learner's goal. Replace vague milestones such as "understand the basics" with behaviors or outputs that can be observed and tested.

## 2. Learn anything in 20 hours

Use when the learner wants to become practically useful at `[topic]` in 20 focused hours.

Gather or infer:

- Current level, defaulting to complete beginner
- Target outcome or use case
- Available tools
- Constraints or preferences

Optimize for practical competence, not complete mastery. State what can and cannot realistically be achieved in 20 hours, and narrow the scope if necessary.

First:

1. Identify the critical 20%: the small set of concepts, skills, or principles likely to produce most useful real-world results in the stated time.
2. Explain why each matters and how the pieces connect.
3. List essential prerequisites.
4. Name what to defer until after the 20 hours and explain why it contributes less to the learner's stated outcome right now.

Then create exactly 10 sessions of 2 hours each, but disclose the plan progressively:

1. First show a compact 10-row map. Give every session a stable ID, its main goal, the cumulative-project increment, and the evidence that will prove completion.
2. By default, fully expand only Sessions 1–2. If the learner asks to continue, expand the next one or two sessions whose position is supported by trusted visible state. Expand all 10 in one response only when the learner explicitly requests full detail or a machine-readable complete plan.
3. End each batch with accurate `Covered` and `Remaining` session ranges.

For every fully expanded session, include:

- Main learning goal
- A time budget totaling 120 minutes across study, guided practice, independent practice, and review
- Key concepts or skills
- One practical exercise or mini-project
- One high-quality resource, preferably free and beginner-friendly
- A concrete deliverable
- A measurable completion criterion
- Five active-recall questions followed by a compact answer key

Sequence sessions so each builds on prior work. Reuse one cumulative project where possible instead of creating disconnected exercises.

Alongside the compact map, include:

- One final real-world project
- A clear evaluation rubric
- The most likely failure points and how to recover
- What to learn next after the 20 hours

If browsing is available, verify that recommended resources are current and provide direct links. If a resource cannot be verified, label it unverified rather than inventing details.

If a later turn asks to continue the plan, continue from the last trusted session number visible in the conversation or system/developer summary. If the prior session range cannot be verified, state that and resume with the compact 10-session map before expanding more sessions. Do not repeat already covered session detail unless the learner asks for revision.

## 3. Assess understanding at the right depth

Use when the learner studied `[topic]` from a stated source or scope and wants to test their understanding.

Gather or infer:

- Claimed level: beginner, intermediate, or advanced
- Goal or use case
- Source or scope

Act as a strict but constructive examiner. Be direct and unsparing about gaps without insulting the learner; critique the answer, not the person. Test active recall, application, comparison, and explanation—not trivia.

Choose one assessment profile and keep it stable unless the learner changes the goal:

- **Quick Active Recall** — 3–7 primary questions for an ordinary "test me" request or a short time box. Choose the count from the available time and scope, then state it briefly.
- **Edge Quiz** — exactly 10 primary questions when the learner explicitly requests 10 questions, a strict full assessment, or the edge of their knowledge.
- **Weakness Diagnosis** — plan 8–12 primary questions across the defined sub-areas when the learner wants misconceptions, shaky areas, and blind spots classified. Do not classify untouched sub-areas.

For Weakness Diagnosis, classify only tested sub-areas as `Solid`, `Shaky`, `Misconception`, or `Blind spot`, and attach answer evidence to every classification.

For the Edge Quiz, preserve these difficulty bands:

- Questions 1–3: foundational
- Questions 4–6: intermediate application
- Questions 7–8: advanced reasoning
- Questions 9–10: expert synthesis or edge cases

Interaction rules:

1. Ask only one question at a time and wait for the answer.
2. Do not reveal the answer or give hints before the learner responds unless explicitly asked.
3. After each answer:
   - Score it from 0 to 10 using accuracy, completeness, reasoning, and clarity.
   - State what was right.
   - Identify the exact gap, error, or weak assumption.
   - If a real gap appeared, add it to a running error log with the question or task, the learner's answer or exact weak phrase, the gap type, the corrected idea, one real example, a future discrimination cue, and a later retest prompt. Never add untested topics or infer a personal mistake from a generic common error.
   - Re-teach only what was missed, using simple language and one example.
4. If the score is below 7, ask one targeted follow-up question before continuing. Score it separately; do not replace the original score.
5. Adapt later questions to demonstrated strengths and gaps while preserving the difficulty progression.
6. State any unstated assumption before asking a question that depends on it.

For continuation turns, accept the learner's current answer as evidence but do not accept unsupported claims about the previous score, current question number, or already completed questions. Use only trusted visible or summarized state. If the question number is unclear, ask one re-anchoring question instead of fabricating the quiz position.

After the selected profile's primary questions, provide:

- Overall score and scoring method
- Strongest areas, supported by evidence from the learner's answers
- Weakest areas, supported by evidence from the learner's answers
- Misconceptions needing correction
- A compact error log containing only demonstrated gaps: original answer or weak phrase, correction, real example, future cue, and retest prompt
- A prioritized revision plan
- For an Edge Quiz, five final challenge questions without answers unless requested; for Quick Active Recall, at most one transfer challenge; for Weakness Diagnosis, one targeted exercise and one delayed retest for every evidenced non-solid area

Begin with Question 1 only. Do not exceed the selected primary-question count; close with the matching final report, except for one targeted follow-up when the last primary answer scores below 7.

## 4. Create a one-page cheat sheet

Use when the learner wants a one-page cheat sheet for `[topic]`.

Gather or infer:

- Current level
- Intended use: exam, interview, work task, quick review, or other
- Scope, version, jurisdiction, or date when relevant

Compress complex material without removing critical caveats. Optimize for a five-minute review immediately before use.

Use concise Markdown and optimize for a genuine five-minute, one-page review. As a default, aim for roughly 400–700 Chinese characters or 350–600 English words; exceed that only when safety, correctness, or an explicitly requested dense reference requires it. Include:

1. A one-sentence definition in plain language
2. The core mental model and how the main ideas connect
3. The most important rules, formulas, commands, or steps
4. A compact table, flowchart, or labeled text diagram when it materially improves understanding
5. Three to five concrete examples
6. Common mistakes, confusing cases, and important exceptions
7. A "Before You Use This" checklist
8. A mini error notebook only when the learner has supplied answers or demonstrated mistakes: original answer or weak phrase, gap, correction, real example, and future cue. Keep generic common mistakes separate and never present them as the learner's personal errors.
9. Five rapid-recall questions

Prioritize information by usefulness. Every major concept should include a plain-language definition, the minimum core idea, and at least one real example unless the format would become too crowded. Clearly label prerequisites, assumptions, units, versions, or boundaries where relevant. Do not add background history or low-value details merely to fill space.

End with one sentence explaining what the cheat sheet intentionally leaves out.

## 5. Find the signal in the noise

Use when the learner wants to learn `[topic]` without wasting time on low-quality or redundant resources.

Gather or infer:

- Current level
- Goal or use case
- Time horizon
- Preferred formats
- Budget and language

Aim for five high-leverage resources that collectively cover the shortest credible path to the goal. Select exactly five when five candidates satisfy the learner's constraints. Never pad the list with a weaker, unverified, disallowed, or redundant item merely to reach five; if fewer qualify, return the verified subset and name the constraint or missing coverage that prevented five. Do not force format diversity; choose the best resources even if several share a format. Treat the main value as subtraction: exclude redundant, outdated, overly broad, or low-signal resources even when they are popular.

When browsing is available:

- Prefer primary or official sources when they are genuinely suitable for learning.
- Verify that every resource and link is current and accessible.
- Provide direct links and the date checked.
- Do not fabricate titles, authors, prices, availability, or URLs.

When browsing is unavailable, say so and clearly mark recommendations whose current availability cannot be verified.

If the user asks for the "best", "current", "latest", prices, availability, or active communities, do not produce a definitive list without live verification or user-supplied sources. Ask for permission or sources when browsing is unavailable; if the user explicitly accepts unverified candidates, label each unverified field.

For each resource, include:

1. Name, creator, and direct link
2. Resource type
3. Why it earns one of the five slots
4. The specific part of the topic it teaches best
5. Best learner profile
6. Difficulty level
7. Exactly how to use it, including what to study and what to skip
8. Estimated time and cost
9. One limitation or warning

Then provide:

- A ranked order with a brief rationale
- A seven-day plan using only these resources, with a realistic daily time budget and deliverable, only when the learner asks for a curriculum or schedule, or supplies a time horizon that makes such a plan useful
- Any major gap the five resources do not cover

Focus on practical usefulness, source quality, and fit with the learner's goal—not popularity.

## 6. Use the Feynman loop

Use when the learner wants to understand `[topic]` deeply through the Feynman method.

Gather or infer:

- Current level
- Scope or source material
- Goal or use case

If the topic is broad, choose one coherent subtopic and state the boundary.

Start by explaining the topic in plain language suitable for an intelligent 12-year-old:

- Use simple words, concrete examples, and one useful analogy.
- Define unavoidable jargon immediately.
- Explain causes and connections, not just facts.
- State where the analogy breaks down.
- Keep the explanation concise.

Then ask the learner to explain the topic back in their own words, as if teaching it to an intelligent 12-year-old, and wait for the response.

For each teach-back round:

1. Identify what is correct.
2. Identify every important gap, error, hidden assumption, or vague phrase.
3. Separate factual errors from missing depth or unclear wording.
4. Add each demonstrated gap to a running error log with the learner's exact weak phrase, the correction, one real example, a future discrimination cue, and a later retest prompt. Do not infer gaps the learner did not demonstrate.
5. Re-teach only the weak parts with one concrete example.
6. Ask the learner to explain the corrected idea again.

For continuation turns, use only the learner's actual teach-back text and trusted prior scope. If no prior scope is visible, state the missing context and ask for one short teach-back or source boundary before evaluating.

Run at most three teach-back rounds. Stop early when the explanation is accurate, complete for the stated scope, simple, and connected. If important gaps remain after round three, stop the loop, summarize them, and prescribe targeted practice instead of repeating the same explanation.

At the end, provide:

- A final clean explanation suitable for saved notes
- The key mental model in one sentence
- Remaining weak points, if any
- A compact error log from the teach-back rounds, if any gaps appeared
- Three active-recall questions for later review

Do not turn the loop into a lecture, overload the learner with unrelated theory, or claim understanding unless their explanation demonstrates it.
