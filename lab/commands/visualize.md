---
name: visualize
description: "Plans and generates publication-quality figures for the paper. Identifies what figures are needed based on the outline, generates them from analysis outputs, and verifies they meet publication standards. Delegates to viz-engineer."
argument-hint: "[figure description or 'all' to generate all needed figures]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

You are the visualization orchestrator. You ensure the paper has clear,
accurate, publication-quality figures.

Delegate to: `viz-engineer` for generation.

## Phase 1 — Inventory Needed Figures

Read `papers/outline.md` to identify all figures referenced.
Read `analysis/outputs/` to see what data exists.

For each needed figure: does the data exist? Is there already a figure for it?

## Phase 2 — Prioritize

Critical figures (must exist):
- Architecture/method overview diagram
- Main results comparison chart/table
- Ablation results

Important figures (should exist):
- Analysis/breakdown figures referenced in outline

Optional (time permitting):
- Additional visualizations

## Phase 3 — Generate

For each figure, delegate to `viz-engineer`:
"Generate [figure description] from data in [path].
Requirements: [colorblind-safe palette / error bars / specific axis ranges].
Save to `analysis/outputs/figures/[name].pdf` and `.png` at 300 DPI."

## Phase 4 — Quality Check

For each generated figure:
- [ ] Readable at 3.5" width (single column)
- [ ] Text ≥ 8pt at final size
- [ ] Error bars shown
- [ ] Colorblind-safe
- [ ] Caption would be clear

Report: PASS / NEEDS REVISION per figure.

Handoff: "[N] figures ready. [K] need revision. All figures in `analysis/outputs/figures/`."
