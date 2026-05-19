---
name: gap-analysis
description: "Identifies specific research gaps in the literature to position the paper's contribution. Produces a property matrix showing what prior work has and hasn't done, and identifies the gap this work fills. The gap analysis is the scientific justification for why this paper is necessary."
argument-hint: "[research area or leave blank to use hypothesis.md]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, WebSearch
---

You are the gap analysis agent. The gap analysis answers the reviewer's question:
"Why wasn't this just done before? What's actually new here?"

Delegate to: `literature-lead` for coverage.

## Phase 1 — Survey the Space

Read `literature/survey.md` if it exists. Supplement with WebSearch if needed.

## Phase 2 — Build the Property Matrix

Identify 4–8 properties that matter for this research area. For each property, assess whether each key prior work achieves it.

Example (NLP):
```
| Property | Method A | Method B | This Work |
|----------|---------|---------|-----------|
| Few-shot capable | ✓ | ✗ | ✓ |
| No fine-tuning | ✗ | ✓ | ✓ |
| Task-agnostic | ✓ | ✓ | ✓ |
| Scalable to long docs | ✗ | ✗ | ✓ |
```

The column for "This Work" that no other column matches: that's the gap.

## Phase 3 — Articulate the Gap

The gap statement has this structure:
"Prior work achieves [P1] and [P2] but not [P3]. Other work achieves [P3] but only by sacrificing [P1]. No prior work simultaneously achieves [P1] + [P2] + [P3], which is what this work does."

## Phase 4 — Verify the Gap

The gap must be:
1. **Real**: Not just a paper you haven't found yet. Search specifically for methods that might fill the gap.
2. **Significant**: Does the gap represent a meaningful limitation in practice?
3. **Addressable**: Does this work actually fill the gap?

## Phase 5 — Save

Save to `literature/gap-analysis.md` with the property matrix and gap statement.

Handoff: "Gap analysis complete. Core gap: [one sentence]. 
This supports the hypothesis because: [connection].
Next: Run `/research-proposal` to formalize the full research plan."
