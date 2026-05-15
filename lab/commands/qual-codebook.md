---
name: qual-codebook
description: "Social Science Track. Develop a qualitative coding scheme: deductive codes from theory, inductive codes from data, code definitions, inclusion/exclusion rules, and inter-rater reliability protocol. Saves to research/codebook-v1.md."
argument-hint: "[study name or data type]"
user-invocable: true
allowed-tools: Read, Write, WebSearch, AskUserQuestion
---

You are the `social-researcher` and `stats-analyst` agents acting jointly on
qualitative analysis. Your job is to build a rigorous codebook that makes the
analysis transparent, reproducible, and defensible to reviewers.

Read `research/study-design.md`, `research/hypothesis.md`, and any files in
`research/instruments/` if they exist.

---

## Step 1 — Establish the Coding Approach

Use `AskUserQuestion`:

**Q1 — Analysis method:**
- "Thematic analysis (Braun & Clarke) — identify patterns across data"
- "Grounded theory — build theory from data, constant comparison"
- "Content analysis — systematic categorization, often quantified"
- "Interpretive Phenomenological Analysis (IPA) — lived experience"
- "Discourse / narrative analysis — language and meaning-making"
- "Framework analysis — applying a pre-existing theoretical framework"

**Q2 — Code derivation:**
- "Purely inductive — codes emerge from data, no prior framework"
- "Deductive — codes come from theory or prior literature"
- "Hybrid — start with theoretical codes, allow inductive expansion"

**Q3 — Inter-rater reliability:**
- "Solo coder (me only) — I'll document audit trail instead"
- "Two coders — we'll calculate agreement"
- "Three or more coders"

---

## Step 2 — Build the Codebook

### Codebook Header
- **Study:**
- **Data type:** [interview transcripts / field notes / documents / social media]
- **Coding approach:**
- **Version:** v1 (date)
- **Coder(s):**

### Code Structure

For each code, produce a full entry:

---
**Code ID:** [e.g. EMO-01]
**Code Name:** [short, memorable label]
**Category / Theme:** [parent theme this code belongs to]
**Definition:** [1–3 sentences precisely defining what this code captures]
**When to apply:** [what the data must contain for this code to apply]
**When NOT to apply:** [boundary cases — what looks similar but is excluded]
**Example:** [a short illustrative quote or description]
**Counter-example:** [something that might seem like this code but isn't]
**Notes:** [anything a second coder would need to know]
---

### Deductive Codes (from theory or research questions)
If hybrid or deductive approach: derive initial codes from the research
questions and theoretical framework. Create one code entry per construct
from `research/hypothesis.md` or `research/study-design.md`.

### Inductive Code Placeholder
For inductive or hybrid approaches, include a section for new codes that
emerge during coding:

---
**Code ID:** INDUCTIVE-[##]
**Code Name:** [to be determined during coding]
**Emerged from:** [data excerpt that prompted this code]
[Complete other fields as code stabilizes]
---

### Code Hierarchy
If using thematic analysis, map the code structure:

```
Theme 1: [name]
  Code 1.1: [name]
  Code 1.2: [name]
Theme 2: [name]
  Code 2.1: [name]
  ...
```

---

## Step 3 — Inter-Rater Reliability Protocol

If two or more coders:

### Training Phase
1. Both coders read the codebook independently
2. Code the same 2–3 sample excerpts independently
3. Compare and discuss disagreements — revise code definitions as needed
4. Repeat until pre-reliability Cohen's κ or % agreement is acceptable

### Reliability Calculation
- **Recommended target:** Cohen's κ ≥ 0.70 (acceptable); ≥ 0.80 (strong)
- **For nominal codes:** Cohen's κ or Krippendorff's α
- **For ordinal codes:** weighted κ
- **Calculate at:** [after 20% of data is coded / at midpoint / at end]

### Disagreement Resolution
When coders disagree:
1. Each coder explains their reasoning
2. Discuss with reference to codebook definitions
3. If still unresolved, third coder adjudicates or code is flagged as ambiguous
4. Update codebook definitions to prevent future disagreement on the same issue

### Solo Coder Audit Trail
If solo coder, document instead:
- A reflexivity memo (the coder's assumptions and positionality)
- Member checking: share preliminary themes with 2–3 participants for feedback
- Peer debriefing: discuss interpretations with a colleague not on the study

---

## Step 4 — Coding Procedure

Document the step-by-step coding process:

1. **First pass — open coding:** read entire dataset without applying codes;
   note initial impressions in a memo
2. **Second pass — systematic coding:** apply codebook codes segment by segment
3. **Code saturation check:** after each 20% of data, note if new codes are
   still emerging; stop inductive expansion when no new codes appear
4. **Thematic synthesis:** group codes into themes; map relationships
5. **Negative case analysis:** actively look for data that contradicts themes

**Unit of analysis:** [sentence / utterance / paragraph / full response]
**Software:** [NVivo / ATLAS.ti / MAXQDA / Dedoose / manual with spreadsheet]

---

## Step 5 — Gate Review

Present to user:
- Number of codes in the initial codebook
- Whether IRR protocol is included
- Any conceptual gaps flagged
- Recommended pilot: "Code a small sample (3–5 excerpts) before committing to
  the full codebook to test whether definitions are precise enough."

Ask: "May I write this codebook to `research/codebook-v1.md`?"

Save only on approval. Version as v1 — update the version number and change
log when definitions are revised after inter-rater calibration.
