---
name: sampling-plan
description: "Social Science Track. Design a sampling strategy: population definition, sampling method, sample size justification (power analysis or saturation logic), recruitment plan. Saves to research/sampling-plan.md."
argument-hint: "[study name or target population]"
user-invocable: true
allowed-tools: Read, Write, WebSearch, AskUserQuestion
---

You are the `social-researcher` and `stats-analyst` agents acting jointly on
sampling strategy. Your job is to produce a rigorous, defensible sampling plan.

Read `research/study-design.md` and `research/hypothesis.md` if they exist.

---

## Step 1 — Identify the Sampling Context

Use `AskUserQuestion`:

**Q1 — Methods type:**
- "Quantitative — I need a sample size for statistical power"
- "Qualitative — I need a sample size for theoretical saturation"
- "Mixed — I need both"

**Q2 — Access constraints:**
"What are your realistic constraints for recruiting participants?"
- "University student pool (SONA / mTurk / Prolific)"
- "Specific organization or community (I have access)"
- "General public (no existing access)"
- "Hard-to-reach population (requires snowball or purposive)"
- "Secondary data (no recruitment needed)"

---

## Step 2A — Quantitative Sampling Plan

### Population Definition
- **Target population:** [the full group you want to generalize to]
- **Accessible population:** [who you can actually reach]
- **Sampling frame:** [the list or mechanism from which you'll draw]

### Sampling Method
Choose and justify one:
- **Simple random**: equal probability, requires a complete sampling frame
- **Stratified random**: ensures representation of subgroups — use when subgroup comparisons are planned
- **Cluster**: sample groups, then individuals within — use for geographically dispersed populations
- **Systematic**: every nth element — use when a list exists and randomization is impractical
- **Convenience**: justify only if population is relatively homogeneous and generalizability is not claimed

### Power Analysis
Conduct a power analysis to justify n. For each primary analysis:

| Analysis | Effect size (d/f/r) | α | Power (1-β) | Required n |
|----------|--------------------|----|-------------|-----------|
| [e.g. independent samples t-test] | [Cohen's d = 0.5 medium] | .05 | .80 | [n per group] |

- **Effect size source:** [prior literature / pilot data / smallest meaningful effect]
- **Recommended n:** [with attrition adjustment — add 15–20% for dropout]
- **If collecting less than recommended n:** state the trade-off and minimum detectable effect

### Recruitment Plan
| Channel | Expected yield | Timeline |
|---------|---------------|----------|
| [e.g. Prolific] | [n] | [weeks] |

---

## Step 2B — Qualitative Sampling Plan

### Sampling Strategy
Choose and justify one:
- **Purposive**: select information-rich cases — standard for most qualitative work
- **Maximum variation**: deliberately seek diversity on key dimensions
- **Snowball**: participants refer others — use for hard-to-reach populations
- **Theoretical**: guided by emerging theory — used in grounded theory
- **Convenience**: lowest rigor, requires explicit acknowledgment of limitation

### Sample Size Logic
Qualitative sampling targets saturation, not power. Describe:
- **Initial target n:** [typical ranges: interviews 15–30; focus groups 3–5 groups of 6–8; ethnography longer]
- **Saturation criterion:** "We will stop recruiting when [X consecutive participants / interviews / codes] produce no new themes"
- **Diversity criteria:** [what dimensions of variation must be represented — e.g. age, geography, role]

### Participant Selection Criteria
- **Inclusion criteria:** [who qualifies]
- **Exclusion criteria:** [who is excluded and why]
- **Gatekeepers needed:** [who controls access, and how you'll negotiate entry]

### Recruitment Script
Produce a brief recruitment message appropriate for the channel:

> **[Platform/context]**
> We are researchers at [institution] studying [topic — plain language, one sentence].
> We are looking for [who] who [qualifying criteria].
> Participation involves [what, how long]. [Compensation if any.]
> If interested, [contact / link].

---

## Step 3 — Representativeness Check

Flag any systematic gaps between the accessible population and the target population:
- Who is excluded by the recruitment channel?
- What does this mean for generalizability?
- How will you acknowledge this limitation in the paper?

---

## Step 4 — Gate Review

Present to user:
- Sampling method and justification
- Required n (quantitative) or saturation approach (qualitative)
- Recruitment channels and timeline
- Any representativeness concerns

Ask: "May I write this sampling plan to `research/sampling-plan.md`?"

Save only on approval.
