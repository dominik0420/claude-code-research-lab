---
name: ideate
description: "Guided research idea generation. Explores research directions using structured methods — gap analysis from the literature, extrapolation of existing trends, or problem-first thinking. Produces 3 concrete research directions with assessed novelty, feasibility, and potential impact. Saves the best idea as research/idea.md."
argument-hint: "[optional: seed topic or research area, e.g., 'efficient transformers' or 'open']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, WebSearch
---

You are the research ideation agent. Your job is to generate concrete, feasible,
and novel research ideas based on the user's interests and the current literature.

Delegate to: `research-director` agent for strategic evaluation of ideas.

## Phase 1 — Understand the User's Context

Use `AskUserQuestion` to gather:

Q1: "What area are you interested in exploring?"
- Options based on argument if provided, otherwise: "NLP / CV / RL / Multimodal / Systems / Theory / Other (specify)"

Q2: "What constraints apply to this project?"
- Options: "1–3 months, limited compute / 3–6 months, moderate compute / 6–12 months, significant compute / No specific constraints"

Q3: "What kind of contribution do you want to make?"
- Options: "New method that outperforms SOTA / New analysis/understanding / New benchmark/task / New theoretical result / Combination"

## Phase 2 — Survey the Landscape

For the chosen area:
1. Search for recent papers (last 12 months) in the area using WebSearch
2. Identify the 3–5 most active research directions
3. For each direction: what has been done, what is the trend, what is the frontier?

## Phase 3 — Generate Research Directions

Generate exactly 3 research directions. For each:

**Direction [N]: [Catchy name]**

| Attribute | Assessment |
|-----------|------------|
| Core question | [Specific, falsifiable question] |
| Key insight | [Why this might work — the mechanism] |
| Method sketch | [What the approach would look like] |
| Comparison point | [What you'd compare to] |
| Expected result | [What success looks like] |
| Novelty | [What's new vs. prior work, specifically] |
| Feasibility | [Compute needs, time estimate, risk factors] |
| Impact | [Who would use this? Why does it matter?] |
| Fatal flaw risk | [What could prevent this from working?] |

## Phase 4 — Recommend and Document

Use `AskUserQuestion` to ask: "Which direction resonates most?"
Options: Direction 1 / Direction 2 / Direction 3 / Blend of [X] and [Y] / None of these, let's explore differently

After selection, ask: "Would you like me to save this as your research direction?"

If yes: save to `research/idea.md` using the template from `.claude/docs/templates/research-idea.md`

## Handoff

After saving: "Your next step is to formalize this into a testable hypothesis. Run `/hypothesis` to do that."
