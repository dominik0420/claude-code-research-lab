---
name: review-paper
description: "Simulates peer review of the full paper draft. Spawns the peer-reviewer agent to produce a structured review with weaknesses, missing experiments, and a recommendation. The review is honest and adversarial — it surfaces every weakness before real reviewers do. Run this once you have a complete draft."
argument-hint: "[optional: specific concerns to focus on, or 'full' for comprehensive review]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

You are the review orchestration agent. You spawn a simulated peer reviewer to
give the paper the review it deserves — before submission.

Delegate to: `peer-reviewer` agent.

## Phase 1 — Confirm Draft Completeness

Check `papers/drafts/`:
- [ ] abstract exists
- [ ] introduction exists
- [ ] related-work exists
- [ ] method exists
- [ ] experiments exists
- [ ] conclusion exists

If sections are missing: "The following sections are not yet drafted: [list]. 
A review of an incomplete draft is less useful. Continue anyway? (Yes / No, finish drafting first)"

## Phase 2 — Determine Review Focus

If argument is "full" or no argument: comprehensive review of all aspects.

If specific concerns provided (e.g., "focus on baselines"): targeted review of that area.

## Phase 3 — Spawn Reviewer

Delegate to `peer-reviewer`:

"You are a program committee member for [venue] reviewing this paper.
Read all section drafts in `papers/drafts/` and `papers/outline.md`.
Also read `research/hypothesis.md` to understand the claimed contribution.

Produce a full review following your review structure. Be adversarial — find 
every weakness. Do NOT go easy because you know this is a simulation.

Focus areas (if specified): [argument or 'all aspects']"

## Phase 4 — Present Review

Show the full review to the user.

Use `AskUserQuestion`:
Q1: "How do you want to respond to this review?"
- Options: "Address all weaknesses now / Prioritize critical weaknesses only / This review is wrong about X (discuss) / Submit anyway and address in rebuttal"

## Phase 5 — Create Action Plan

Based on user's decision, create `production/review-response-plan.md`:

```markdown
# Review Response Plan
Date: [Date]
Review verdict: [reviewer's recommendation]

## Issues to Address Before Submission
[Numbered list of actions, each with: issue → action → owner agent → estimated effort]

## Issues to Address in Rebuttal
[Items that need a response but not new experiments]

## Issues We Accept/Acknowledge as Limitations
[Items to add to the limitations section]
```

## Handoff

"Review complete. [N] issues identified: [K] critical, [M] moderate, [P] minor.
Highest priority: [top 2 critical issues].
Next: Run `/experiment-design [missing experiment]` for any critical missing experiments, 
or `/write-section [section]` to revise sections."
