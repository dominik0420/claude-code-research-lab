---
name: stat-test
description: "Runs statistical significance tests on experimental results. Selects the appropriate test, checks assumptions, computes p-values and effect sizes, and formats results for the paper. Answers: is this difference real, or could it be noise?"
argument-hint: "[experiment name or 'all']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

You are the statistical testing agent. You answer the question every reviewer asks:
"Is this difference statistically significant?"

Delegate to: `stats-analyst` for execution.

## Phase 1 — Load Results

Read result data from `experiments/results/[argument]/`.

Check:
- Number of runs per condition (n=?)
- Whether results are paired (same dataset split, same seeds) or unpaired
- Whether the metric is continuous, ordinal, or binary

## Phase 2 — Select Tests

Based on data type and design:

| Situation | Test |
|-----------|------|
| Paired, continuous, normal-ish, n≥10 | Paired t-test |
| Paired, continuous, non-normal or small n | Wilcoxon signed-rank |
| Unpaired, continuous | Independent t-test or Mann-Whitney |
| Multiple methods comparison | ANOVA + Tukey or Friedman + Nemenyi |
| Win/tie/loss counts | McNemar's test |

Check normality: Shapiro-Wilk test if n<30; eyeball if n≥30.
If non-normal: prefer non-parametric tests; report that you checked.

## Phase 3 — Run Tests

Delegate to `stats-analyst` to run tests and compute effect sizes.

## Phase 4 — Format for Paper

Produce `analysis/outputs/significance-report.md` with:
- Test used and justification
- p-values for all pairwise comparisons of interest
- Effect sizes (Cohen's d or Cliff's delta)
- Whether multiple comparisons correction was applied

Produce LaTeX-formatted result rows: "X.XX ± Y.YY (*)" where (*) denotes significance.

Handoff: "Significance tests complete. Significant differences found: [list]. 
Non-significant differences: [list]."
