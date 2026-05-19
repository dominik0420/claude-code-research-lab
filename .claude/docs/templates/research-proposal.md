# Research Proposal Template

Use this template with `/research-proposal`. Replace all bracketed content.

---

# Research Proposal: [Title]

**Date**: [YYYY-MM-DD]
**Target Venue**: [Venue, Year — e.g., NeurIPS 2025]
**Submission Deadline**: [Date]
**Authors**: [Names or "TBD"]

---

## 1. Problem Statement

[Describe the specific, concrete problem being addressed. This should be 2–3 paragraphs.

Para 1: What is the task/setting and why does it matter?
Para 2: What do current methods do, and what specific limitation do they have?
Para 3: Why is this limitation important to address — what fails in practice?]

---

## 2. Related Work and Gap

[Organized by approach, NOT by chronology.]

### [Approach 1 — e.g., "Retrieval-based methods"]
[2–4 methods. For each: 1 sentence on what it does, 1 sentence on its limitation.]

### [Approach 2 — e.g., "Generative methods"]
[Same format.]

### The Gap
[What no prior work does, stated precisely using the property matrix from gap-analysis.md.]

Prior work achieves [P1] and [P2] but not [P3].
This work is the first to simultaneously achieve [P1] + [P2] + [P3].

---

## 3. Proposed Approach

### Core Insight
[The key intellectual insight in 2–3 sentences. This is why the approach works.]

### Method Sketch
[High-level description. What are the key components? How do they work together?
A figure would go here in the paper.]

### Expected Advantages
[Why will this outperform prior work, based on the mechanism?]

---

## 4. Research Hypothesis

[Copy from research/hypothesis.md]

**Formal statement**: We hypothesize that [METHOD] will improve [METRIC] on [TASK]
compared to [BASELINE], because [MECHANISM].

**Quantitative prediction**: [Specific expected improvement]

**Falsification conditions**: [What would disprove this]

---

## 5. Experimental Plan

### Primary Evaluation
- Task: [task name]
- Benchmark: [benchmark name(s)]
- Metric: [primary metric]
- Baselines: [list]

### Ablation Plan
| Component | What it tests |
|-----------|--------------|
| [Component A] | [What contribution does A make?] |
| [Component B] | [What contribution does B make?] |

### Additional Analysis
- [Error analysis / breakdown by difficulty / etc.]

---

## 6. Expected Contributions

1. [Main contribution — the core claim in one sentence]
2. [Secondary: what else we demonstrate]
3. [Optional: benchmark / dataset / code release]

---

## 7. Success Criteria

The work is successful if:
- Main experiment: [specific numerical threshold or relative improvement]
- Ablations confirm: [what the ablations need to show]
- Analysis demonstrates: [what the analysis needs to reveal]

If we observe [specific failure], we will [pivot plan].

---

## 8. Timeline

| Milestone | Target Date | Deliverable |
|-----------|------------|-------------|
| Eval protocol locked | [date] | experiments/eval-protocol.md |
| All experiments designed | [date] | experiments/specs/ complete |
| Data pipeline ready | [date] | data/processed/ populated |
| All experiments run | [date] | experiments/results/ complete |
| Analysis complete | [date] | analysis/outputs/ complete |
| Paper outline approved | [date] | papers/outline.md |
| First draft complete | [date] | papers/drafts/ complete |
| Peer review simulation | [date] | papers/review-panel-report.md |
| Submission | [date] | papers/submission/ |

---

## 9. Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Method doesn't outperform baselines | Medium | High | [Alternative hypothesis or approach] |
| Insufficient compute | Low | Medium | [Cloud compute backup, scope reduction] |
| Critical competitor paper appears | Low | High | [Reposition, extend with new analysis] |
| [Project-specific risk] | [P] | [I] | [Mitigation] |
