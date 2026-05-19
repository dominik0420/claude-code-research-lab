# Paper Outline Template

Used by `/outline-paper`. Customize for your paper's structure.

---

# Paper Outline: [Working Title]

**Target Venue**: [Venue, Year]
**Page Limit**: [N pages main + M pages supplemental]
**Central Argument**: [The one-sentence story this paper tells]
**Date Created**: [Date]

---

## Abstract (~150 words)

**Must contain:**
- Problem: [1 sentence — what specific problem]
- Gap: [1 sentence — what's missing in prior work]
- Method: [1–2 sentences — what we do and the key mechanism]
- Result: [1 sentence with number — e.g., "X outperforms baselines by Y% on Z"]
- Implication: [1 sentence — why this matters]

---

## 1. Introduction (~1 page)

**Purpose**: Motivate the problem and state the contribution.

**Paragraph 1 — Hook** (~100 words)
Content: [Opening with the real-world problem or motivating observation. What fails without our method?]
Key sentence: [A concrete, compelling opening that a non-expert understands]

**Paragraph 2 — Prior work landscape** (~150 words)
Content: [High-level survey of what's been tried. Not a list — organized around what approaches exist.]
Key sentence: [The sentence that positions the field, not individuals]

**Paragraph 3 — The gap** (~100 words)
Content: [The specific limitation addressed by this work. Concrete, not vague.]
Key sentence: "However, no prior work [specific gap]."

**Paragraph 4 — Our approach** (~100 words)
Content: [What we do and the key mechanism. Brief — details in Section 3.]
Key sentence: [The mechanism sentence — WHY our approach works]

**Paragraph 5 — Contributions** (~80 words)
Format:
- We propose [method name], which [does what]
- We show that [method] achieves [metric] on [benchmark], outperforming [baseline] by [amount]
- We demonstrate that [mechanism insight from ablations]
- [Optional: We release code at [URL]]

**Paragraph 6 — Paper structure** (~30 words)
"Section 2 reviews related work. Section 3 describes [method]. Section 4 presents experiments. Section 5 concludes."

---

## 2. Related Work (~1 page)

**Purpose**: Show mastery of the field; position this work as necessary.

**Section 2.1 — [Theme 1: e.g., "Retrieval-augmented methods"]**
Papers to cover: [List]
Key difference from this work: [1 sentence]

**Section 2.2 — [Theme 2]**
Papers to cover: [List]
Key difference: [1 sentence]

**Section 2.3 — [Theme 3 — most direct competitors]**
Papers to cover: [List]
Key differences: [2–3 sentences — this is the most important paragraph]

---

## 3. [Method Name] (~2 pages)

**Purpose**: Describe the method so a reader could implement it.

**Section 3.1 — Preliminaries** (~0.3 pages)
Content: [Mathematical notation, task formulation, background needed to understand the method]

**Section 3.2 — [Core Component 1]** (~0.7 pages)
Content: [First key technical contribution]
Figure needed: [Architecture diagram / algorithm pseudocode]

**Section 3.3 — [Core Component 2]** (~0.5 pages)
Content: [Second key technical contribution]

**Section 3.4 — [Training/Optimization]** (~0.5 pages)
Content: [How the method is trained]

**Figure 1**: Architecture overview — shows [what: e.g., "full model with component A and B labeled"]

---

## 4. Experiments (~2 pages)

**Purpose**: Provide evidence for the claims.

**Section 4.1 — Setup** (~0.4 pages)
Content: Datasets, baselines, metrics, implementation details (brief — details in appendix)

**Section 4.2 — Main Results** (~0.6 pages)
Content: Table 1 + interpretation
Table 1: [Main comparison table — proposed method vs. all baselines on all benchmarks]
Key takeaway: [1 sentence — what Table 1 proves about the hypothesis]

**Section 4.3 — Analysis** (~0.7 pages)
Content: Ablations + analysis figure
Table 2: [Ablation table — each design choice removed]
Figure 2: [Analysis figure — e.g., performance vs. compute, attention visualization, error breakdown]
Key takeaway: [What the analysis reveals about the mechanism]

**Section 4.4 — [Additional Analysis]** (optional, ~0.3 pages)
Content: [e.g., efficiency analysis, case studies, domain generalization]

---

## 5. Conclusion (~0.5 page)

**Purpose**: Crystallize the contribution and point forward.

- Summary: [What we showed — 2–3 sentences]
- Implications: [What this means for the field — 1–2 sentences]
- Limitations: [Honest statement of what this doesn't solve — required]
- Future work: [1–2 directions — keep brief]

---

## Appendix (if needed)

- A: Extended implementation details (hyperparameters, training procedures)
- B: Additional results (more benchmarks, more baselines)
- C: Proofs (if theoretical claims)
- D: Additional figures
- E: Broader impact (if not in main paper)

---

## Figure and Table Checklist

| Figure/Table | Section | Content | Status |
|-------------|---------|---------|--------|
| Figure 1 | §3 | Architecture overview | [needed/in-progress/ready] |
| Table 1 | §4.2 | Main results | [ready: path to .tex] |
| Table 2 | §4.3 | Ablations | [needed] |
| Figure 2 | §4.3 | Analysis | [needed] |

---

## Pre-Writing Checklist

Before writing any section, confirm:
- [ ] All main experiment results are in `analysis/outputs/`
- [ ] All ablation results are in `analysis/outputs/`
- [ ] All figures are drafted (even rough)
- [ ] `research/hypothesis.md` is finalized
- [ ] `literature/survey.md` is complete
