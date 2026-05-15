# Research Directory Rules

When working in `research/` and `experiments/`:

## hypothesis.md

This file is the anchor for the entire project. When reading or writing it:
- Every claim must be falsifiable
- Every prediction must be quantitative
- Every mechanism must be explicit (not just "we expect improvement")
- Do NOT change the hypothesis without documenting the change in `research/research-log.md`

## eval-protocol.md

**This file is LOCKED once experiments begin.**

- May be created or edited ONLY before the first experiment runs
- Any change after experiments start requires PI approval AND documentation in research-log.md
- The metric in this file is the metric reported in the paper — no post-hoc changes

## experiments/specs/

- One file per experiment
- Must use the spec template from `lab/docs/templates/experiment-spec.md`
- Status field must be kept current: DRAFT → APPROVED → IMPLEMENTED → COMPLETE
- APPROVED status requires PI or Lead Researcher sign-off

## experiments/results/

- Results are never manually edited (they are code outputs)
- If a result needs to be regenerated, do so via the reproduce script
- Results directories should include: metrics.json, config_used.yaml, run_info.json (timestamp, git hash, hardware)

## research/research-log.md

- Append-only (never delete entries)
- Every hypothesis change must be logged
- Every "we decided not to pursue X" should be logged (prevents re-discovery)
- Use the template from `lab/docs/templates/research-log-entry.md`
