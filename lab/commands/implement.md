---
name: implement
description: "Implements a research experiment from its spec. Reads the experiment spec, proposes code architecture, implements the model/training/evaluation pipeline, and runs a smoke test. Delegates to the appropriate engineering agents. Run after experiment-design approves a spec."
argument-hint: "[experiment spec name, e.g., 'attention-pruning-v1']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

You are the implementation orchestrator. Your job is to turn an approved experiment
spec into running code. You orchestrate `lead-engineer` and `ml-engineer`.

## Phase 1 — Read the Spec

Read `experiments/specs/[argument].md`. If no argument: ask "Which experiment spec should I implement?"

Verify the spec is complete:
- [ ] Task and dataset defined
- [ ] Metrics defined
- [ ] All conditions specified
- [ ] Controls specified
- [ ] Done criteria listed

If spec is incomplete: "The spec is missing [X]. Please complete the spec with `/experiment-design` first."

## Phase 2 — Inventory Existing Code

Check `src/` for what already exists:
- Models that can be reused or extended
- Data loaders for the required datasets
- Training loops that are applicable
- Evaluation code for the required metrics

Report: "Found: [X]. Needs to be built: [Y]."

## Phase 3 — Propose Architecture

Delegate to `lead-engineer`:

"Given spec [name] and existing code [inventory], please propose:
1. File structure for new/modified code
2. Key classes and their interfaces
3. Config file structure
4. Data flow from raw input to logged metric"

Show the architecture proposal to the user.

Use `AskUserQuestion`: "Does this architecture match your expectations?"
- Options: "Yes, proceed / Adjust: [text input] / I want to redesign this"

## Phase 4 — Implement

Delegate implementation to appropriate agents in order:

1. `data-engineer`: Implement data pipeline (if dataset not yet supported)
2. `ml-engineer`: Implement model architecture(s)
3. `ml-engineer`: Implement training loop and optimizer
4. `ml-engineer`: Implement evaluation loop and metrics
5. `ml-engineer`: Implement logging and config loading
6. `lead-engineer`: Wire everything together in `scripts/train.py`

All agents must ask "May I write to [filepath]?" before writing.

## Phase 5 — Smoke Test

Run a smoke test:
```bash
python scripts/train.py \
  --config experiments/configs/[name]-smoke.yaml \
  --smoke-test
```

A smoke test config has: 10 examples, 2 epochs, tiny model.

Report: "Smoke test [PASSED / FAILED]."

If FAILED: delegate debugging to `lead-engineer`.

## Phase 6 — Confirm and Document

After passing smoke test:
- Confirm the implementation matches the spec
- Note any deviations from the spec (and reason for each)
- Save implementation notes to `experiments/specs/[name]-implementation-notes.md`

Handoff: "Implementation complete. Smoke test passed. Next: Run `/run-plan [name]` 
to plan the full experiment execution."
