# Experiment Spec Template

Used by `/experiment-design`. One file per experiment in `experiments/specs/`.

---

# Experiment Spec: [Experiment Name]

**Spec Author**: [Agent + Date]
**Hypothesis Tested**: [Copy the specific sub-hypothesis from hypothesis.md]
**Purpose**: [One sentence — what question does this experiment answer?]
**Status**: DRAFT / APPROVED / IMPLEMENTED / COMPLETE

---

## Task and Evaluation Setting

- **Task**: [e.g., text classification, question answering, image segmentation]
- **Dataset**: [Name, version, source URL]
- **Dataset Split**: train=[N] / val=[N] / test=[N]
- **Primary Metric**: [Name — and WHY this metric for this claim]
- **Secondary Metrics**: [List]
- **Evaluation Procedure**: [Exactly how to compute the metric — no ambiguity]

---

## Conditions

| ID | Name | Description | Key Config Differences |
|----|------|-------------|----------------------|
| C1 | Full (proposed) | Our complete method | config/exp-[name]-proposed.yaml |
| C2 | Baseline: [name] | [Brief description] | config/exp-[name]-baseline1.yaml |
| C3 | Baseline: [name] | [Brief description] | config/exp-[name]-baseline2.yaml |
| A1 | Ablation: w/o [X] | Proposed minus component X | config/exp-[name]-ablation1.yaml |
| A2 | Ablation: [X] → simple | X replaced with simple alt | config/exp-[name]-ablation2.yaml |

---

## Controls

[What is held constant across ALL conditions — this is what makes the comparison fair]

- Random seeds: [list of N seeds, e.g., 1, 2, 3, 4, 5]
- Dataset split: [same for all conditions]
- Compute budget: [same hyperparameter search budget for all conditions]
- [Other controls]

---

## Baseline Justification

[For each baseline: why is this a fair and appropriate comparison?]

- **Baseline C2**: [It is the current SOTA for this task / It is the most direct competitor / It tests the null hypothesis of our claim]
- **Baseline C3**: [Reason]

---

## Expected Results

If hypothesis is CORRECT:
- C1 (proposed) > C2 (baseline 1) by ≥ [threshold] on primary metric
- Ablations A1, A2 < C1 (each component matters)

If hypothesis is INCORRECT:
- C1 ≈ C2 (no improvement)
- What this would imply: [interpretation of null result]

---

## Compute Budget

| Condition | GPU Type | GPU Hours | Wall Time |
|-----------|---------|----------|-----------|
| C1 (proposed) | [GPU] | ~[N]h | ~[N]h |
| C2 (baseline) | [GPU] | ~[N]h | ~[N]h |
| **Total** | — | **~[N]h** | **~[N]h** |

Number of seeds: [N]
Total compute: ~[N] GPU hours

---

## Done Criteria

- [ ] All conditions run with all seeds
- [ ] Results logged to `experiments/results/[name]/` in structured format
- [ ] No condition has >X% variance between seeds (instability check)
- [ ] Results verified by PI and Lead Researcher
- [ ] Reproducibility check: one condition re-run from scratch, matches original

---

## Implementation Notes

[Anything the ML Engineer needs to know that's not obvious from the spec above.
E.g., known implementation quirks, numerical stability concerns, data loading details.]

---

## Spec Change Log

| Date | Change | Reason |
|------|--------|--------|
| [Date] | Initial spec | — |
