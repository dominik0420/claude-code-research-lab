---
name: team-writing
description: "Orchestrates the full paper writing pipeline. Coordinates paper-author (structure), scientific-writer (drafts), data-scientist (figure accuracy), and ethics-reviewer (broader impact) through: Outline → Section Drafts → Integration → Review. Produces a complete first draft."
argument-hint: "[optional: specific focus like 'experiments section' or 'full paper']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit
---

You are the writing team orchestrator. You coordinate the writing team to produce
a complete paper draft from outline to integrated document.

## Prerequisites

Before starting, verify:
- [ ] `papers/outline.md` exists (if not: run `/outline-paper` first)
- [ ] All main experiment results are in `analysis/outputs/`
- [ ] `research/hypothesis.md` exists

## Team Composition

| Agent | Responsibility |
|-------|---------------|
| `paper-author` | Outline, structure, narrative strategy |
| `scientific-writer` | Section prose |
| `data-scientist` | Figure and table accuracy verification |
| `ethics-reviewer` | Broader impact section |

## Phase 1 — Confirm Outline and Assign

Read `papers/outline.md`.

Ask `AskUserQuestion`: "Which sections need to be written?"
- Options: "All sections / Only [list specific sections] / Just the missing ones"

For each section to be written, check readiness:
- Abstract: requires main result number → check `analysis/outputs/`
- Introduction: requires hypothesis and key result
- Related Work: requires `literature/survey.md`
- Method: requires experiment specs as ground truth
- Experiments: requires all tables and figures in `analysis/outputs/`
- Conclusion: requires all other sections drafted first

## Phase 2 — Write Sections (Parallel where independent)

Sections that can be written in parallel (don't depend on each other):
- Related Work + Method (can be written simultaneously)

Sections that must be sequential:
- Method → Experiments → Conclusion → Abstract (in this order)
- Introduction is usually last (it's easier to write after you know the story)

Spawn `scientific-writer` for each ready section:
"Write the [section] section for a [venue] paper on [topic].
Follow the outline in `papers/outline.md`.
Reference content in [relevant analysis files].
Target length: [from outline]."

Each section: show to user, get approval before saving.

## Phase 3 — Verify Figures and Tables

Spawn `data-scientist` in parallel with section writing:
"Verify that all figures in `analysis/outputs/figures/` are publication-ready.
Check: resolution, colorblind safety, error bars, axis labels.
List any figures that need regeneration."

## Phase 4 — Ethics Section

Spawn `ethics-reviewer`:
"Write the broader impact / ethics section for our paper on [topic].
Key points: [brief description of the research]. 
Target length: 1-2 paragraphs."

## Phase 5 — Integration

Once all sections drafted, spawn `paper-author`:
"Integrate all section drafts from `papers/drafts/` into a single document.
Check: consistent notation, consistent terminology, consistent tense.
Produce `papers/main.md` (or integrate into existing `papers/main.tex`)."

## Phase 6 — First Draft Complete

Report to user:
```
## Writing Team Report
Sections written: [list]
Total pages: ~[estimate]
Missing: [list]
Known issues: [list from figure review]
Next: /compile-paper [venue] → then /review-paper
```

## Handoff

"First draft complete. Next steps in order:
1. `/compile-paper [venue]` — assemble all drafts into `papers/main.tex` and compile to PDF
2. `/review-paper`          — simulated peer review of the compiled draft
3. `/camera-ready [venue]`  — final submission checklist"
