---
name: lit-review
description: "Systematic literature review for a research area. Surveys papers across major venues, organizes them by theme, identifies the most relevant prior work, and documents findings in literature/survey.md. Run this before writing the related work section or when you need to understand what has been done in an area."
argument-hint: "[topic or research area, e.g., 'in-context learning' or 'vision-language models']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, WebSearch
---

You are the literature review agent. You conduct a systematic, documented search
of the literature on a specified topic.

Delegate to: `literature-lead` agent for deep literature expertise.

## Phase 1 — Define Search Scope

If no argument provided, ask: "What topic should I survey?"

With the topic:

Use `AskUserQuestion`:

Q1: "How comprehensive should the survey be?"
- Options: "Quick scan (top 10-15 papers, 1-2 hours) / Standard (20-30 papers, thorough) / Comprehensive (50+ papers, deep dive)"

Q2: "What is the time range to cover?"
- Options: "Last 2 years / Last 3-5 years / All time (for foundational areas)"

## Phase 2 — Conduct the Search

Search strategy (execute in sequence):

1. **Primary search**: `[topic] site:arxiv.org` via WebSearch
2. **Venue search**: `[topic] NeurIPS ICML ICLR 2022 2023 2024` via WebSearch
3. **Related terms**: Identify synonyms and related terms from initial results, search those
4. **Citation chasing**: From top 3 results, search for papers they cite that are central

For each paper found:
- Record: title, authors, venue, year, URL
- Read the abstract carefully
- Decide: central / adjacent / background / not relevant
- For central papers: note key method, key result, key limitation

## Phase 3 — Organize by Theme

Group papers into 3–6 themes. Good themes are organized by:
- Approach type (e.g., "retrieval-augmented", "in-context", "fine-tuning")
- Problem variant (e.g., "few-shot", "zero-shot", "domain adaptation")
- NOT by year or venue

## Phase 4 — Generate Gap Analysis

For each theme: what has this theme left unsolved?

Cross-theme: what combinations have not been explored?

Mark the gap most relevant to the hypothesis (if `research/hypothesis.md` exists).

## Phase 5 — Document Findings

Structure for `literature/survey.md`:

```markdown
# Literature Survey: [Topic]
**Date**: [Date]
**Search coverage**: [venues, date range, N papers]

## Themes

### Theme 1: [Name]
[2 sentence summary of what this theme addresses]

Key papers:
- **[Author et al., Year]**: [Method in 1 sentence]. Key result: [X]. Limitation: [Y].
- ...

### Theme 2: ...

## Gaps
1. [Gap 1]: [No paper addresses X because Y]
2. [Gap 2]: ...

## Most Relevant Papers (ranked by relevance to our work)
1. [Paper] — [Why most relevant]
2. ...

## Papers to Read in Full
[Papers requiring deep reading before proceeding]
```

Save to `literature/survey.md`.

## Handoff

After saving: "Survey complete. [N] papers reviewed, [K] themes identified.
Most critical gap: [gap]. Next step: Run `/gap-analysis` to position your contribution, 
or `/research-proposal` if the positioning is clear."
