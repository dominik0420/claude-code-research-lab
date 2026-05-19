---
name: code-review
description: "Reviews research code for correctness, reproducibility, and quality. Delegates to the code-reviewer agent. Run this before trusting any experimental results — research code bugs are silent and produce plausible-looking wrong answers."
argument-hint: "[file path, module name, or 'all' to review all src/ code]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

You are the code review orchestration agent. Delegate to `code-reviewer`.

## Phase 1 — Identify Code to Review

If argument is "all": read all files in `src/`.
If argument is a path: read that file.
If argument is a module name: find files matching that name in `src/`.

## Phase 2 — Delegate Review

Spawn `code-reviewer`:
"Review [files] for:
1. Correctness: loss function, metric computation, data splits
2. Reproducibility: seed handling, determinism
3. Silent bugs: off-by-one, incorrect masking, wrong normalization
4. Research-specific patterns: eval mode during evaluation, proper baseline tuning

Produce: APPROVE / APPROVE WITH CHANGES / REJECT with specific file:line issues."

## Phase 3 — Report and Action

Show review to user.

If REJECT: "Code has critical issues. Must fix before trusting results:
[list issues with file:line references]"

If APPROVE WITH CHANGES: "Code has moderate issues. Recommend fixing before submission:
[list issues]"

If APPROVE: "Code passes review. Results can be trusted."
