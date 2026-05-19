# Agent Roster

22 agents covering the full research lifecycle.

## Tier 1 — Research Leadership (Opus)

| Agent | Domain | When to Use |
|-------|--------|-------------|
| `research-director` | Scientific vision | "Is this publishable?", "What's our contribution?", contribution conflicts, pivot decisions |
| `principal-investigator` | Research execution | Hypothesis formation, result interpretation, daily scientific decisions |
| `project-manager` | Production | Sprint planning, deadlines, risk management, cross-agent coordination |

## Tier 2 — Department Leads (Sonnet)

| Agent | Domain | When to Use |
|-------|--------|-------------|
| `lead-researcher` | Experimental design | Experiment specs, evaluation protocols, ablation strategy, baseline design |
| `lead-engineer` | Code architecture | Codebase structure, code review strategy, infrastructure decisions |
| `data-scientist` | Statistical analysis | Analysis plans, significance tests, data quality, visualization strategy |
| `paper-author` | Academic writing | Paper structure, narrative, venue compliance, writing workflow |
| `literature-lead` | Literature | Systematic survey, gap analysis, related work positioning |

## Tier 3 — Specialists (Sonnet or Haiku)

| Agent | Model | Domain | When to Use |
|-------|-------|--------|-------------|
| `ml-engineer` | Sonnet | Model code | Implement model architectures, training loops, evaluation code |
| `data-engineer` | Sonnet | Data pipeline | Download, preprocess, split, and load datasets |
| `stats-analyst` | Sonnet | Statistics | Run significance tests, compute effect sizes, generate result tables |
| `viz-engineer` | Sonnet | Visualization | Publication figures, plots, architecture diagrams |
| `code-reviewer` | Sonnet | Code quality | Audit code for correctness, reproducibility, silent bugs |
| `reproducibility-engineer` | Sonnet | Reproducibility | Verify results can be reproduced from code + config |
| `ablation-analyst` | Sonnet | Ablations | Design and interpret ablation studies |
| `baseline-engineer` | Sonnet | Baselines | Implement and tune comparison baselines |
| `scientific-writer` | Sonnet | Prose | Draft paper sections based on outline and content |
| `peer-reviewer` | Sonnet | Review | Adversarial simulated peer review |
| `ethics-reviewer` | Sonnet | Ethics | Broader impact, bias, dual-use assessment |
| `devops-researcher` | Haiku | Compute infra | Job scripts, cluster management, environments |
| `domain-specialist` | Sonnet | Domain | Deep expertise in the research subfield |

## Quick Reference: Who Owns What

| File/Directory | Owner |
|----------------|-------|
| `research/hypothesis.md` | `principal-investigator` |
| `research/proposal.md` | `principal-investigator` + `research-director` |
| `literature/survey.md` | `literature-lead` |
| `experiments/eval-protocol.md` | `lead-researcher` |
| `experiments/specs/` | `lead-researcher` |
| `src/models/` | `ml-engineer` |
| `src/data/` | `data-engineer` |
| `baselines/` | `baseline-engineer` |
| `analysis/` | `data-scientist` + `stats-analyst` |
| `analysis/outputs/figures/` | `viz-engineer` |
| `papers/outline.md` | `paper-author` |
| `papers/drafts/` | `scientific-writer` |
| `production/sprints/` | `project-manager` |
