---
name: status
description: "Quick project status snapshot. Shows experiment progress, writing status, sprint state, and any blocking issues. Output is always under 30 lines."
argument-hint: ""
user-invocable: true
allowed-tools: Read, Glob, Grep
model: haiku
---

Read the project state and produce a concise status report. Maximum 30 lines.
No preamble. Just facts.

## Data to Read

1. `production/sprints/current-sprint.md` — sprint status
2. `experiments/specs/` — count of specs
3. `experiments/results/` — count of result directories
4. `papers/drafts/` — which sections exist
5. `production/session-state/active.md` — last active task

## Output Format

```
## Research Lab Status — [Date]

### Research
- Hypothesis: [defined / not defined]
- Eval protocol: [locked / not locked]
- Lit review: [complete / in progress / not started]

### Experiments
- Specs: [N defined]
- Running: [N] | Complete: [N] | Failed: [N]
- Baselines: [implemented / not started]
- Ablations: [complete / not started]

### Analysis
- Results analyzed: [yes / no]
- Statistical tests: [run / not run]
- Figures: [N ready]

### Paper
- Outline: [exists / missing]
- Sections drafted: [list]
- Sections remaining: [list]

### Sprint
- Current sprint: [name/number or "none"]
- Blocking issues: [list or "none"]
```
