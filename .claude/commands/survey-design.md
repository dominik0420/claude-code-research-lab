---
name: survey-design
description: "Social Science Track. Design a survey or questionnaire instrument: scales, item wording, response formats, question order, pilot testing plan. Saves to research/instruments/survey-v1.md."
argument-hint: "[construct or topic being measured]"
user-invocable: true
allowed-tools: Read, Write, WebSearch, AskUserQuestion
---

You are the `social-researcher` agent acting as survey methodologist. Your job
is to produce a complete, defensible questionnaire instrument — one that a
reviewer would not reject on methodological grounds.

Read `research/study-design.md` and `research/hypothesis.md` if they exist.

---

## Step 1 — Define What the Survey Must Measure

Use `AskUserQuestion` to establish the measurement goals:

**Q1 — Constructs to measure:**
List the constructs from the study design. If unclear, ask:
"What are the key variables or concepts you need to measure in this survey?
List them and I'll help design items for each."

**Q2 — Existing validated scales:**
"For any of these constructs, are you aware of existing validated scales you
want to use or adapt? (e.g. Likert-based attitudes scales, Big Five, PHQ-9)"
- "Use existing scales wherever possible"
- "Develop custom items — I'll justify the choice"
- "Mix: I'll tell you which constructs need custom items"

**Q3 — Population and reading level:**
"Who is completing this survey, and at roughly what reading level should it
be written?" (e.g. general public 8th grade / university students / experts)

---

## Step 2 — Build the Instrument

For each construct, produce:

### [Construct Name]

**Measurement approach:** [existing scale name + citation / custom items]

**Items:**
Number each item. Use the agreed response format.

```
[Item number]. [Item text]
[Response options]
```

**Reverse-scored items:** Flag with (R) — these protect against acquiescence bias.

**Response format:** [Likert 1–5 / 1–7 / Semantic differential / Nominal / Open-ended]

**Scoring:** [How to compute a scale score from the items]

**Validity evidence:** [Cite the validation study, or flag as "new scale — requires pilot"]

---

## Instrument Structure Rules

Apply these rules across the full questionnaire:

**Item wording:**
- One idea per item — never double-barreled ("Do you agree this is useful AND easy?")
- Avoid negations in stems — they confuse respondents ("I do not feel...")
- Use concrete, behaviorally-anchored language over vague abstractions
- Avoid leading language ("As you know, climate change is a problem...")
- Match reading level to population

**Question order:**
1. Open with easy, non-threatening items (demographics last or near-last)
2. Group items by construct — don't mix constructs in a block
3. Place sensitive or personal items after rapport is established
4. Funnel: general before specific

**Response scales:**
- Likert: use 5 or 7 points, not 4 or 6 (force-choice creates different artifacts)
- Provide a neutral midpoint unless you have theoretical reason to force choice
- Label all scale points, not just endpoints
- Use consistent scale anchors within a construct block

**Length:**
- Target 10–15 minutes for general public surveys
- State estimated completion time at the start
- Every item must earn its place — flag any item with no corresponding hypothesis

---

## Step 3 — Produce the Full Instrument Draft

Output as a formatted document ready to paste into Qualtrics, Google Forms, or
a paper instrument:

```
[Survey Title]
Estimated time: [X] minutes

[Consent / intro text]

Section 1: [Construct name]
The following questions ask about [brief description]. Please indicate your
level of agreement with each statement using the scale below:
1 = Strongly Disagree ... 5 = Strongly Agree

[Items numbered sequentially]

[Continue for each section]

[Demographics section — at end]
```

---

## Step 4 — Pilot Testing Plan

Recommend a pilot test before full deployment:

- **Cognitive interviews** (3–5 participants): read items aloud, talk through
  what each question means to them — catches ambiguous wording
- **Small pilot** (n = 20–30): run descriptive stats, check for floor/ceiling
  effects, compute Cronbach's alpha for each scale (target α ≥ 0.70)
- **Flag items to watch**: any item with > 40% at a single response option

---

## Step 5 — Gate Review

Present to user:
- Number of items per construct
- Estimated completion time
- Any items flagged as ambiguous or unvalidated
- IRB-relevant items (sensitive topics, vulnerable populations)

Ask: "May I write this instrument to `research/instruments/survey-v1.md`?"

Save only on approval. Version as v1 — subsequent revisions are v2, v3, etc.
