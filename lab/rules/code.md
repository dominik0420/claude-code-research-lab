# Code Directory Rules

When working in `src/`, `scripts/`, `tests/`, and `baselines/`:

## General Coding Standards

- **No hardcoded paths**: All paths from config or environment variable
- **No hardcoded hyperparameters**: All experiment parameters in YAML config files
- **Seed everything**: `torch.manual_seed`, `np.random.seed`, `random.seed`, `torch.cuda.manual_seed_all`
- **Log everything**: Config, git hash, hardware, timestamp at run start
- **Save as structured data**: JSON/CSV for results, not just `print()` statements

## Config Files

All experiment configs live in `experiments/configs/`.
Naming convention: `[experiment-name]-[condition].yaml`

Required fields in every config:
```yaml
experiment:
  name: [experiment-name]
  condition: [condition-name]
  seed: [integer]
  
output:
  dir: experiments/results/[experiment-name]-[condition]/
  
# ... model, data, training fields specific to the experiment
```

## Model Files (`src/models/`)

- One class per file
- Class name matches filename (PascalCase file, PascalCase class)
- All `__init__` parameters have type hints
- Docstring on every public class and method
- No global state

## Data Files (`src/data/`)

- `data/raw/` is read-only. Never write here.
- All preprocessing happens in `data/processed/`
- Every dataset class must have a `__len__` and `__getitem__`
- Data loading must be deterministic with a fixed seed

## Reproducibility Requirements

Before ANY results are included in the paper:
1. Run with 3+ different seeds
2. Confirm results match with the reproduce script: `python scripts/reproduce.py --config [config]`
3. Document in `experiments/specs/[name].md` under "Done Criteria"

## Baseline Code (`baselines/`)

- Each baseline in its own subdirectory
- Include `baselines/[name]/NOTES.md` documenting: source, deviations from original, reproduction results
- Baselines run with the SAME config structure as the proposed method

## Test Requirements

All model code must have:
- At least one unit test in `tests/test_models.py` (checks output shape)
- Smoke test coverage in `tests/test_smoke.py`

Run before any commit: `python -m pytest tests/ -x -q`
