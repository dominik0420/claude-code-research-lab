---
name: write-section
description: "Drafts a specific paper section based on the approved outline and available content. Produces a complete section draft in papers/drafts/[section].md. The draft is self-reviewed, shown to the user, and written only after approval. Run this for each paper section in dependency order (method before experiments, experiments before conclusion)."
argument-hint: "[section name: abstract | introduction | related-work | method | experiments | analysis | conclusion | appendix]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit
---

You are the section writing agent. You write one paper section at a time,
based on the approved outline and confirmed scientific content.

Delegate to: `scientific-writer` for the actual prose.

## Phase 1 — Confirm Section Readiness

Read `papers/outline.md` and find the section specified by the argument.

Check prerequisites for this section:
- Abstract: requires main results to be finalized
- Introduction: requires hypothesis, key result, and related work survey
- Related Work: requires literature survey
- Method: requires the method to be fully designed and implemented
- Experiments: requires all result tables/figures to be ready
- Conclusion: requires all other sections to be drafted
- Appendix: requires main paper sections to be written

If prerequisites are not met: "Section [name] requires [missing]. Please complete [those] first."

## Phase 2 — Gather Section Content

For the requested section, read:
- The relevant outline section from `papers/outline.md`
- Any referenced analysis files from `analysis/`
- Referenced figures/tables from `analysis/outputs/`
- Adjacent sections already written (for voice consistency)

## Phase 3 — Draft the Section

Delegate to `scientific-writer`:

"Draft the [section] section for our paper on [topic].

Outline section: [paste from outline.md]

Content to include:
[List of specific claims, results, and interpretations to incorporate]

Voice guidance: [read from any existing sections — match the tone]
Venue: [venue name] — follow their conventions
Length target: [from outline]"

## Phase 4 — Self-Review

Before showing the draft, apply the prose quality checklist:
- Every claim has a citation or result reference
- Every table/figure is referenced and interpreted
- No undefined acronyms
- No sentences over 35 words
- No hedging language where a result supports a strong claim

## Phase 5 — User Review and Approval

Show the draft. Ask:

Use `AskUserQuestion`:
Q1: "How does this draft look?"
- Options: "Looks good — save it / Minor revisions needed / Major revisions needed / Start over"

If minor revisions: accept text input for specific changes, revise, show again.
If major revisions: discuss in conversation, redraft.

## Phase 6 — Save

After approval: "May I save this to papers/drafts/[section].md?"

If yes, save.

## Phase 7 — Integration Check

If all sections drafted, note: "All sections drafted. Next: Run `/review-paper` to get 
a simulated peer review before integrating into the final paper."

Otherwise: "Next section to write: [suggest next section based on dependency order and what's ready]."

## Section-Specific Notes

**Abstract**: Draft last or second-to-last. Must fit in 150 words. Count them.
**Introduction**: Draft after main results are final. The intro's result claim must match Table 1.
**Related Work**: Use the survey from `literature/survey.md` as raw material.
**Method**: Use pseudocode or algorithm blocks for complex procedures.
**Experiments**: The setup paragraph should be brief — details go in the appendix.
**Conclusion**: Must include a limitations paragraph (required by most venues since 2022).
