---
name: run-plan
description: "Plans the full experimental run order and compute requirements. Given a set of experiments to run, determines the optimal order, estimates compute time, identifies parallelism opportunities, and produces a run schedule."
argument-hint: "[experiment name or 'all' to plan all pending experiments]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---

You are the run planning agent. You create a compute-efficient plan for running all pending experiments.

## Phase 1 — Inventory Experiments

Read all specs in `experiments/specs/` that don't have results yet.

For each: estimate compute cost (from spec's compute budget field).

## Phase 2 — Determine Dependencies

Which experiments depend on others?
- Ablations depend on main method being implemented
- Analysis experiments depend on main results

## Phase 3 — Optimize Order

Recommend order based on:
1. Critical path first (what blocks the most)
2. Parallelism (what can run simultaneously)
3. Smoke tests first (fail fast before burning compute)

## Phase 4 — Produce Run Schedule

```markdown
# Experiment Run Plan

## Priority 1 (Run First — Critical Path)
| Experiment | Config | GPUs | Hours | Status |
|-----------|--------|------|-------|--------|

## Priority 2 (Can Parallelize)
| Experiment | Config | GPUs | Hours | Status |

## Priority 3 (After P1/P2 complete)
| Experiment | Config | GPUs | Hours | Status |

## Total Estimate
- Total GPU hours: [N]
- Wall time (parallelized): [N]h
- Critical path length: [N]h
```

## Phase 5 — Submit or Stage

Ask `AskUserQuestion`: "How would you like to proceed?"
- Options: "Submit jobs now (cluster) / Run locally one by one / Prepare scripts only / Stage for later"

Handoff: "Run plan complete. Total compute: [N] GPU hours. Critical path: [N]h."
