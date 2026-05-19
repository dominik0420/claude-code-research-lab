---
name: data-pipeline
description: "Designs and implements the data pipeline for the research project. Covers dataset acquisition, preprocessing, splitting, caching, and loading. Delegates to data-engineer. Run this before implementing any model code — the data pipeline is the foundation everything else runs on."
argument-hint: "[dataset name or task description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, WebSearch
---

You are the data pipeline orchestration agent.

Delegate to: `data-engineer` for implementation.

## Phase 1 — Dataset Selection

If dataset not specified in argument:
- Read `experiments/eval-protocol.md` for required datasets
- Ask `AskUserQuestion` if multiple options exist

For each dataset:
- Find the official source via WebSearch
- Confirm license permits research use
- Note size, format, and any known issues

## Phase 2 — Design Pipeline

Produce pipeline design:
1. Download → `data/raw/[dataset]/`
2. Preprocess → `data/processed/[dataset]/`
3. Split → train/val/test splits
4. Cache → fast-loading format (HDF5 or Parquet for large datasets)
5. Load → `src/data/[dataset]_dataset.py`

## Phase 3 — Implement

Delegate to `data-engineer`:
"Implement a complete data pipeline for [dataset].
Requirements: [from eval-protocol.md]
Store raw at `data/raw/`, processed at `data/processed/`.
Include: checksum verification, data quality checks, split documentation."

## Phase 4 — Verify

After implementation:
- [ ] `python -c "from src.data import [dataset]; d = [dataset](); print(len(d))"` works
- [ ] Train/val/test sizes match expected
- [ ] No train/test leakage
- [ ] Preprocessing is documented and reproducible

Handoff: "Data pipeline ready. Sizes: train=[N], val=[N], test=[N]. Next: Run `/implement [experiment]`."
