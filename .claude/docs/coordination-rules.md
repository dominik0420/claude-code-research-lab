# Agent Coordination Rules

## Hierarchy and Delegation

1. **Vertical Delegation**: Research Director delegates to PI and leads; leads delegate to specialists. Never skip a tier for complex decisions.

2. **Horizontal Consultation**: Agents at the same tier may consult each other but do not make binding decisions outside their domain.

3. **Scientific Conflict Resolution**: When scientific direction is disputed, escalate to `research-director`. The research director's decision is binding.

4. **Technical Conflict Resolution**: When engineering approaches conflict, `lead-engineer` decides. Escalate to PI if it affects scientific validity.

5. **Cross-Domain Work**: Any work spanning multiple domains is coordinated by `project-manager`.

6. **File Ownership**: Agents write only within their designated directories. Exceptions require explicit delegation from the owning agent.

## Model Tier Assignment

| Tier | Model | When to use |
|------|-------|-------------|
| **Haiku** | claude-haiku-*  | Status reads, formatting, simple lookups — no scientific judgment |
| **Sonnet** | claude-sonnet-* | Implementation, analysis, section drafting — default for most work |
| **Opus** | claude-opus-*   | Multi-document synthesis, high-stakes decisions, review panel |

Skills with `model: haiku`: `/help`, `/status`, `/milestone-review`
Skills with `model: opus`: `/team-review`, and all Tier 1 agents

## Parallel vs. Sequential Subagents

**When to spawn in parallel**: If two subagents' inputs are independent (neither needs the other's output to begin), spawn both simultaneously.

Examples of parallel-safe work:
- `data-engineer` + `baseline-engineer` implementing their respective components
- Three independent `peer-reviewer` instances in `/team-review`
- `viz-engineer` generating figures while `scientific-writer` drafts text

**When to run sequentially**: One agent's output is the other's input.

Examples of sequential work:
- `lead-researcher` designs spec → `ml-engineer` implements it
- `stats-analyst` computes results → `viz-engineer` generates figures
- `scientific-writer` drafts → `paper-author` reviews

## Scientific Integrity Rules

1. **Evaluation protocol is locked before any experiments run.** The eval protocol (`experiments/eval-protocol.md`) must exist and be approved before any experiments are submitted. No post-hoc metric selection.

2. **Results are never manually edited.** All numbers in the paper come directly from analysis scripts that read from `experiments/results/`. Any discrepancy between paper numbers and script output is a bug, not a choice.

3. **Baseline fairness is non-negotiable.** `baseline-engineer` tunes baselines with the same budget as the proposed method. A weaker-than-necessary baseline invalidates the comparison.

4. **Reproducibility verification before trust.** `reproducibility-engineer` must confirm that results can be reproduced before they're used in the paper's main claims.

5. **Negative results are reported.** If an ablation shows a component doesn't matter, or if the method underperforms on a subset of the evaluation, this must be reported.

## Collaboration Protocol

**All agents follow the Question → Options → Decision → Draft → Approval cycle:**

1. Clarify the task before starting work
2. Propose the approach before implementing it
3. Show the output before saving it to disk
4. Say "May I write this to [filepath]?" before any Write/Edit
5. Note any deviations from the spec explicitly

No agent commits code, saves files, or runs experiments without user approval.

## Research Log Protocol

Every significant decision goes into `research/research-log.md`:
- Hypothesis formulation or revision
- Experiment design choices
- Pivot decisions (why we changed direction)
- "We decided NOT to do X" (prevents rediscovery)
- Result interpretations
- Scope changes

Format: `[Date] [Agent] [Decision] [Reason]`
