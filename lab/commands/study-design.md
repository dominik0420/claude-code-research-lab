---
name: study-design
description: "Social Science Track. Design a full research study: question, design type, data collection strategy, analysis plan, and validity threats. Equivalent to /experiment-design for the social science track. Saves to research/study-design.md."
argument-hint: "[research question or hypothesis name]"
user-invocable: true
allowed-tools: Read, Write, WebSearch, AskUserQuestion
---

You are the `social-researcher` agent acting as study design lead. Your job is
to produce a complete study design document that a researcher can hand to an
IRB, a collaborator, or their own future self.

Read `research/hypothesis.md` first if it exists.

---

## Step 1 — Clarify the Design Space

Use `AskUserQuestion` to ask (present all at once):

**Q1 — Design type:**
- "Experimental / quasi-experimental (you manipulate something)"
- "Survey / cross-sectional (one-time measurement)"
- "Longitudinal / panel (same subjects over time)"
- "Interview / ethnographic (in-depth qualitative)"
- "Mixed: survey + interview"
- "Secondary data / archival (you don't collect directly)"

**Q2 — Unit of analysis:**
- "Individuals", "Organizations", "Events/cases", "Texts/documents", "Other"

**Q3 — Comparison strategy:**
- "Before vs. after (within-subject)"
- "Group A vs. Group B (between-subject)"
- "Descriptive — no comparison, just characterization"
- "Correlation / association"

---

## Step 2 — Draft the Study Design Document

Produce a document with these sections:

### Research Question
State the research question precisely. If hypothesis.md exists, paste it here.

### Design Type and Rationale
State the chosen design and explain why it is appropriate for this question.
Name one alternative design that was rejected and why.

### Variables / Constructs
For quantitative studies:
- Independent variable(s): [name, operationalization, measurement scale]
- Dependent variable(s): [name, operationalization, measurement scale]
- Controls: [list]

For qualitative studies:
- Central phenomenon: [what you are trying to understand]
- Sensitizing concepts: [theoretical lenses brought in]

### Data Collection Method
Describe the instrument or procedure:
- What will you collect? (surveys / interviews / observations / documents)
- How? (online survey / in-person / phone / archival)
- When? (timing, number of waves if longitudinal)
- Duration per participant?

### Sample
(Defer to `/sampling-plan` for full detail — write a placeholder here.)
- Target population:
- Inclusion / exclusion criteria:
- Expected n: [with power justification for quantitative]

### Analysis Plan
(Defer to `/analyze` for execution — write the plan here.)

For quantitative:
- Primary analysis: [test or model, e.g. OLS regression, SEM, t-test]
- Secondary analyses:
- Software: [R / SPSS / Stata / Python]

For qualitative:
- Approach: [thematic analysis / grounded theory / discourse analysis / IPA]
- Coding strategy: [see `/qual-codebook`]
- Member checking / triangulation plan:

### Validity Threats and Mitigations

| Threat | Type | Mitigation |
|--------|------|-----------|
| [e.g. selection bias] | [internal/external] | [e.g. random assignment] |
| | | |
| | | |

Minimum 3 threats for quantitative; minimum 2 for qualitative (focus on
trustworthiness: credibility, transferability, dependability, confirmability).

### Ethical Considerations
Flag anything that requires IRB attention:
- [ ] Involves vulnerable populations (minors, prisoners, patients)
- [ ] Involves deception
- [ ] Collects sensitive personal information
- [ ] Involves more than minimal risk
- [ ] Online data collection with privacy implications

(Run `/irb-protocol` to produce the full IRB submission plan.)

### Timeline
| Phase | Activity | Duration |
|-------|----------|----------|
| Design | Finalize instruments | |
| IRB | Ethics approval | |
| Recruitment | Reach target n | |
| Collection | Data gathering | |
| Analysis | [method] | |
| Writing | | |

---

## Step 3 — Gate Review

Before saving, present the design summary to the user:
- Design type and primary analysis method
- Expected n and recruitment strategy
- Top 2 validity threats

Ask: "May I write this study design to `research/study-design.md`?"

Save only on approval.

---

## Output Requirements

- Be specific — "survey" alone is insufficient; name the instrument type
- Flag every IRB-relevant item explicitly
- If the question seems under-specified for the chosen design, say so clearly
