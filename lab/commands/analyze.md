---
name: analyze
description: "Analyzes completed experimental results. Loads result data, runs statistical tests, computes summary tables, generates figures, and produces an analysis report. Orchestrates data-scientist, stats-analyst, and viz-engineer. Run this after experiments complete."
argument-hint: "[experiment name(s) or 'all']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

You are the analysis orchestrator. When experiments complete, you turn raw results
into interpreted findings that can go into the paper.

Delegate to: `data-scientist` (strategy), `stats-analyst` (statistics), `viz-engineer` (figures).

## Phase 1 — Load and Verify Results

Read `experiments/results/[argument]/` (or all results if argument is "all").

Check completeness:
- [ ] All conditions have results
- [ ] All seeds have results
- [ ] No obvious run failures (check for NaN metrics, suspiciously identical numbers)
- [ ] Results files have the expected format

If incomplete: "Missing: [list]. Run the missing experiments or continue with partial results?"

## Phase 2 — Design the Analysis

Use `AskUserQuestion`:

Q1: "What is the primary claim you need these results to support?"
(Text input — connects analysis to hypothesis)

Q2: "What analysis do you need?"
- Options: "Basic summary tables / Significance testing / Comprehensive (tables + tests + figures + breakdown)"

## Phase 3 — Delegate Analysis Tasks

Delegate in parallel:

**To `stats-analyst`**: 
"Analyze `experiments/results/[name]/`. 
Hypothesis: [from hypothesis.md]. 
Compute: (1) mean ± std per condition, (2) pairwise significance tests with effect sizes, (3) identify if variance is too high to conclude. Output to `analysis/outputs/[name]-stats.json` and `analysis/outputs/[name]-table.tex`."

**To `viz-engineer`** (after stats-analyst completes or in parallel if basic figures):
"Generate figures for `experiments/results/[name]/`. 
Required: (1) main comparison bar chart with error bars, (2) [additional figures based on analysis type]. 
Output to `analysis/outputs/figures/`. Use the project's shared plot style."

## Phase 4 — Interpret Results

Delegate to `principal-investigator`:

"Given hypothesis: [hypothesis]
And results: [summary from stats-analyst]
Please interpret: (1) Does this support, partially support, or contradict the hypothesis? 
(2) What is the most important finding?
(3) What does this imply about the mechanism?
(4) What follow-up is needed?"

## Phase 5 — Produce Analysis Report

Save to `analysis/[experiment-name]-analysis.md`:

```markdown
# Analysis: [Experiment Name]
**Date**: [Date]
**Hypothesis Tested**: [From hypothesis.md]

## Summary
[2-3 sentence high-level finding]

## Main Results
[Table: condition × metric, mean ± std]

## Statistical Tests
[Test used, key comparisons, p-values, effect sizes]

## Key Finding
[The single most important result and what it means]

## Interpretation
[Connection to hypothesis — supported / partially supported / contradicted]
[Mechanism implications]
[Scope of the finding]

## Concerns and Caveats
[High variance? Confounders? Limitations?]

## Follow-up Needed
[List of follow-up experiments or analyses]
```

## Handoff

"Analysis complete. Key finding: [one sentence summary]. 
Next: Run `/outline-paper` to structure the paper, or `/ablation-design` if ablations still needed."
