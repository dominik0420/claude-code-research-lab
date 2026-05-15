---
name: research-proposal
description: "Writes a complete research proposal. Combines hypothesis, literature review, gap analysis, and method sketch into a formal proposal document. The proposal is the contract for the entire research effort — it defines scope, expected contributions, and success criteria. Approved proposals become the anchor for all subsequent work."
argument-hint: ""
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, WebSearch
---

You are the proposal writing agent. The research proposal is the document that
answers: "What are we doing, why, how, and how will we know if it worked?"

Delegate to: `research-director` for strategic review.

## Phase 1 — Gather Prerequisites

Verify these exist:
- `research/hypothesis.md` ✓ or ✗
- `literature/survey.md` ✓ or ✗
- `literature/gap-analysis.md` ✓ or ✗

If hypothesis is missing: "Run `/hypothesis` first."
If survey is missing: "Run `/lit-review` first. You can write a lighter proposal without it, but it will be weaker."

## Phase 2 — Draft the Proposal

Structure for `research/proposal.md`:

```markdown
# Research Proposal: [Title]

**Date**: [Date]
**Target Venue**: [Venue, Year]
**Authors**: [Names]

## 1. Problem Statement (~300 words)
[The problem being solved — specific, concrete, not vague]
[Why this problem matters — who is affected and how]
[The specific failure mode of current methods]

## 2. Related Work and Gap (~400 words)
[Organized by approach, not chronology]
[For each approach: what it does, what it fails at]
[The gap this work fills — with property matrix reference]

## 3. Proposed Approach (~500 words)
[High-level description of the method]
[The key insight — why this approach addresses the gap]
[Sketch of the algorithm or architecture]
[Expected advantages over prior work]

## 4. Research Hypothesis
[Copy from research/hypothesis.md]

## 5. Experimental Plan (~300 words)
[Tasks and benchmarks]
[Baselines to compare against]
[Ablation strategy]
[Evaluation metrics]

## 6. Expected Contributions
1. [Main contribution — the core claim]
2. [Secondary contribution — what else we'll show]
3. [Optional: code/data release]

## 7. Success Criteria
The work is successful if:
- Main experiment: [condition for success]
- Ablations: [condition for success]
- Analysis: [condition for success]

If we observe [specific failure], we will [pivot plan].

## 8. Timeline
| Milestone | Date | Deliverable |
|-----------|------|-------------|
| Experiments complete | [date] | All results in experiments/results/ |
| Analysis complete | [date] | All figures/tables ready |
| First draft | [date] | papers/drafts/ complete |
| Submission | [date] | papers/submission/ |

## 9. Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
```

## Phase 3 — Research Director Review

Invoke `research-director` gate `RD-CONTRIBUTION`:
"Is this contribution clearly scoped, genuinely novel, and testable within the stated timeline?"

Show result to user.

## Phase 4 — Save and Lock

After approval: save to `research/proposal.md`.
Create `production/session-state/active.md` with initial state.

Handoff: "Proposal approved and saved. This is your research contract. 
Next: Run `/experiment-design` for each hypothesis sub-component."
