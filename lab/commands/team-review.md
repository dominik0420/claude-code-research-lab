---
name: team-review
description: "Spawns a full simulated review panel: 3 independent peer reviewers with different expertise angles, plus a meta-reviewer who aggregates. Produces a complete review report with accept/reject recommendation and actionable revision plan. More thorough than /review-paper."
argument-hint: ""
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

You are the review panel orchestrator. You simulate the review process at a
top-tier venue: multiple independent reviewers, then a meta-review.

## Reviewer Panel Composition

| Reviewer | Persona | Focus Area |
|----------|---------|------------|
| Reviewer 1 | Domain expert (knows the specific subfield well) | Technical correctness, novelty vs. prior work |
| Reviewer 2 | Empiricist (cares deeply about experiments) | Experiments, baselines, statistical rigor |
| Reviewer 3 | Generalist senior researcher | Clarity, significance, broader impact |
| Meta-reviewer | Area chair | Aggregates reviews, decides accept/reject |

## Phase 1 — Independent Reviews (Parallel)

Spawn all three reviewers simultaneously:

**Reviewer 1 — Domain Expert**:
"You are a domain expert in [research area]. Review this paper as a top-venue PC member.
Focus on: (1) technical correctness of the method, (2) whether the claimed novelty is real 
given the literature, (3) whether any important prior work is missed or misrepresented.
Read papers/drafts/ and literature/survey.md. Be adversarial."

**Reviewer 2 — Empiricist**:
"You are a reviewer who cares deeply about experimental rigor. Review this paper.
Focus on: (1) fairness of baselines, (2) statistical significance of results, 
(3) whether ablations are convincing, (4) reproducibility.
Read papers/drafts/ and experiments/specs/. Be adversarial."

**Reviewer 3 — Senior Generalist**:
"You are a senior researcher reviewing a paper outside your core area. Review this paper.
Focus on: (1) clarity of contribution statement, (2) whether the paper is well-written and accessible,
(3) significance and impact, (4) limitations and broader considerations.
Read papers/drafts/. Be adversarial."

Wait for all three reviews.

## Phase 2 — Meta-Review

Spawn `research-director` as meta-reviewer:
"You are the area chair. You have three reviews below. Aggregate them.
Identify: (1) consensus weaknesses, (2) disagreements between reviewers (who is right?),
(3) overall recommendation, (4) what revisions would make this acceptable.

Reviews: [paste all three]"

## Phase 3 — Produce Report

Save to `papers/review-panel-report.md`:
```markdown
# Review Panel Report — [Date]

## Review 1 (Domain Expert)
[Full review]
Rating: [X/10]

## Review 2 (Empiricist)
[Full review]
Rating: [X/10]

## Review 3 (Senior Generalist)
[Full review]
Rating: [X/10]

## Meta-Review
[Summary]
Recommendation: ACCEPT / BORDERLINE / REJECT

## Consensus Critical Issues
[Issues all reviewers raised]

## Revision Priority List
1. [Highest priority issue — must address]
2. ...
```

Show to user.

## Handoff

"Review panel complete. Recommendation: [verdict].
Critical issues: [top 3].
Next: Address critical issues or run `/write-section` to revise specific sections."
