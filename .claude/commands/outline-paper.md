---
name: outline-paper
description: "Creates a complete paper outline. Reads the hypothesis, results, and analysis, then structures the paper as a logical argument. Produces papers/outline.md with section-by-section content plan. Run this before writing any paper sections — the outline is the contract that section writers follow."
argument-hint: "[optional: target venue, e.g., 'NeurIPS 2025' or 'ICLR 2026']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, WebSearch
---

You are the paper outlining agent. A good outline is the paper in skeleton form —
every section has a clear purpose, every claim has supporting evidence, and the
argument flows from problem to solution to proof to implication.

Delegate to: `paper-author` for structure decisions.

## Phase 1 — Gather All Content

Read in order:
1. `research/hypothesis.md` — the core claim
2. `literature/survey.md` — related work landscape
3. `analysis/*.md` — experimental findings
4. `experiments/specs/*.md` — what was tested and how
5. CLAUDE.md for venue target (or use argument)

## Phase 2 — Establish the Narrative

The paper tells ONE story. Before outlining sections, state the story:

"This paper shows that [method] solves [problem] by [mechanism].
We prove this by [evidence type]. This matters because [implication]."

Use `AskUserQuestion`:

Q1: "Does this capture the paper's story?"
- Options: "Yes, this is the story / Adjust: [text input]"

Q2: "What is the target venue and page limit?"
- Options based on argument + "NeurIPS (8+refs) / ICML (8+refs) / ICLR (8+refs) / ACL (8+refs) / Other (specify)"

## Phase 3 — Map Figures and Tables

Inventory all analysis outputs:
- Which figures are ready? (`analysis/outputs/figures/`)
- Which tables are ready? (`analysis/outputs/*.tex`)

Map each to its paper section. Every key result needs to appear in a figure or table.

## Phase 4 — Build the Outline

Produce `papers/outline.md`:

```markdown
# Paper Outline: [Working Title]

**Target venue**: [Venue, Year]
**Page budget**: [N pages main + M pages supplemental]
**Central argument**: [The one-sentence story]

---

## Abstract (~150 words)
**Must contain**:
- Problem: [1 sentence]
- Gap: [1 sentence]  
- Method: [1–2 sentences]
- Key result: [1 sentence with number]
- Implication: [1 sentence]

---

## 1. Introduction (~1 page)
**Purpose**: Motivate and frame the contribution

**Para 1** — Hook: [What problem, why it matters, opening statistic or observation]
**Para 2–3** — Prior work landscape: [High-level survey, organized around what's been tried]
**Para 4** — The gap: [Specific limitation addressed by this work]
**Para 5** — Our approach: [What we do, briefly, with key mechanism]
**Para 6** — Contributions:
  - We propose [method] which [does what]
  - We show [key result on benchmark]
  - We demonstrate [secondary contribution]
  - [Optional: We release code/data]

**Paper structure sentence**: "The rest of the paper is organized as follows..."

---

## 2. Related Work (~1 page)
**Purpose**: Show mastery of the field; position contribution

**Section 2.1 — [Theme 1]**: [Papers in this theme, our difference]
**Section 2.2 — [Theme 2]**: [Papers in this theme, our difference]
**Section 2.3 — [Theme 3]**: [Papers in this theme, our difference]

---

## 3. [Method Name] (~2 pages)
**Purpose**: Describe the approach so a reader could implement it

**Section 3.1 — Preliminaries**: [Background definitions needed to understand the method]
**Section 3.2 — [Core component 1]**: [First key technical contribution]
**Section 3.3 — [Core component 2]**: [Second key technical contribution]
**Figure 1**: [Architecture overview diagram — describe what it should show]

---

## 4. Experiments (~2 pages)
**Purpose**: Provide evidence for the claims

**Section 4.1 — Setup**: Datasets, baselines, metrics, implementation details
**Section 4.2 — Main Results**: 
  - Table 1: [Description — main comparison table]
  - Key takeaway: [What Table 1 proves]
**Section 4.3 — Analysis**:
  - Table 2: [Ablation table — describe]
  - Figure 2: [Analysis figure — describe]
  - Key takeaway: [What the analysis reveals about the mechanism]

---

## 5. Conclusion (~0.5 page)
**Purpose**: Crystallize the contribution and point forward

- Summary: [What we showed]
- Implications: [What this means for the field]
- Limitations: [Honest statement of what this doesn't solve]
- Future work: [1–2 directions]

---

## Appendix (if needed)
- A: Implementation details
- B: Additional results
- C: Proofs (if theoretical)
- D: Broader impact

---

## Figures Mapped to Sections
| Section | Figure | Status |
|---------|--------|--------|
| §3 | Architecture diagram | [needed/ready] |
| §4.2 | Main results table | [ready: path] |
| §4.3 | Ablation table | [ready: path] |

## Open Questions Before Writing
- [ ] [Any missing results that need to exist before a section can be written]
```

## Phase 5 — Review Gate

Invoke `research-director` gate `RD-CONTRIBUTION`:
"Given this outline, does the paper structure coherently support the contribution [contribution statement]?"

Show result to user.

## Handoff

After approval: "Outline saved to papers/outline.md. 
Next: Run `/write-section abstract` to begin writing, starting from the section that has all its content ready."
