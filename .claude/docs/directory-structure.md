# Directory Structure

## How Projects Are Organized

When you run `/start`, it asks for a **project name**. All output files go under
`[project-name]/` so multiple projects can coexist in the same repo without
collision. For example, if your project is `attention-study`:

```
attention-study/
├── research/
├── experiments/
├── papers/
└── ...
```

The active project is stored in `CLAUDE.md` under `Active Project:`. Every hook
reads this field and prefixes all output paths automatically via `lib.sh`.

If you choose **"Use repo root"** at the project-name prompt, files go to the
repo root directly (the original flat layout).

---

## Repo-Level Files

```
/
├── CLAUDE.md                        # Master config — paradigm, language, active project
│
├── .claude/                         # Lab config (committed directly — no setup needed)
│   ├── agents/                      # 22 agent definitions
│   ├── commands/                    # 39 slash command definitions
│   ├── hooks/                       # 13 lifecycle hooks
│   │   └── lib.sh                   # Shared path helpers (get_project_dir, ppath, pmkdir)
│   ├── scripts/                     # compile_paper.py, export_survey.py
│   ├── docs/                        # Documentation and templates
│   └── rules/                       # Path-specific rules
```

---

## Project Output Directory

All paths below are prefixed with `[project-name]/` when `Active Project` is set.
The tree shows the logical structure regardless of whether a prefix is used.

```
[project-name]/
│
├── research/                        # Research documents
│   ├── idea.md                      # Initial idea from /ideate
│   ├── hypothesis.md                # THE research hypothesis (anchor document)
│   ├── proposal.md                  # Full research proposal
│   ├── study-design.md              # Social Science: study design
│   ├── irb-protocol.md              # Social Science: IRB ethics submission
│   ├── instruments/                 # Survey instruments, interview guides
│   └── research-log.md              # Running log of decisions and pivots
│
├── literature/                      # Literature review
│   ├── survey.md                    # Literature survey by theme
│   ├── gap-analysis.md              # Property matrix and gap statement
│   ├── bibliography.bib             # BibTeX references
│   └── papers/                      # Individual paper notes
│
├── experiments/                     # Experiment management (ML Track)
│   ├── eval-protocol.md             # LOCKED evaluation protocol (write before experiments)
│   ├── specs/                       # Experiment specs (one per experiment)
│   ├── configs/                     # YAML configs (one per experiment run)
│   ├── results/                     # Experiment outputs — IMMUTABLE (guarded by hook)
│   ├── run-log.md                   # Git hash log for every run
│   └── baseline-plan.md             # Baseline comparison plan
│
├── src/                             # Research source code
│   ├── models/                      # Model architectures
│   ├── data/                        # Dataset loading and preprocessing
│   ├── training/                    # Training loops, optimizers
│   ├── evaluation/                  # Metric computation
│   └── utils/                       # Shared utilities
│
├── data/                            # Data files
│   ├── raw/                         # Original data (read-only, never modify)
│   └── processed/                   # Preprocessed, split data
│
├── baselines/                       # Baseline implementations
│   └── [method-name]/               # One directory per baseline
│
├── analysis/                        # Analysis scripts and outputs
│   ├── [experiment]-analysis.md     # Analysis reports
│   ├── analysis-plan.md             # Pre-experiment analysis plan
│   ├── figures/                     # Figure generation scripts
│   └── outputs/                     # Generated tables, figures, stats
│       ├── figures/                 # .pdf and .png figures
│       └── tables/                  # .tex table files
│
├── papers/                          # Paper drafts
│   ├── outline.md                   # Paper structure and argument map
│   ├── STATUS.md                    # Section progress dashboard (auto-updated)
│   ├── drafts/                      # Section drafts
│   │   ├── abstract.md
│   │   ├── introduction.md
│   │   ├── related-work.md
│   │   ├── method.md
│   │   ├── experiments.md
│   │   └── conclusion.md
│   ├── main.tex                     # Assembled LaTeX paper (from /compile-paper)
│   └── main.pdf                     # Compiled PDF (from /compile-paper)
│
└── production/                      # Project management
    ├── milestones/                  # Milestone definitions
    ├── sprints/                     # Sprint plans
    │   └── current-sprint.md        # Active sprint
    ├── risk-register.md             # Known risks and mitigations
    └── session-state/               # Active session state
        └── active.md                # Current work context (recovery point)
```

---

## Key Files

| File | Owned By | Purpose |
|------|----------|---------|
| `[project]/research/hypothesis.md` | `principal-investigator` | THE anchor document — everything serves the hypothesis |
| `[project]/experiments/eval-protocol.md` | `lead-researcher` | Locked before experiments — defines success |
| `[project]/papers/outline.md` | `paper-author` | Paper structure — defines section content |
| `[project]/production/session-state/active.md` | All | Recovery point after context loss |
| `[project]/research/research-log.md` | `principal-investigator` | Decision history (append-only) |

---

## Gitignore Recommendations

```gitignore
# Large data files
*/data/raw/
*/data/processed/
*/experiments/results/
*/experiments/logs/

# Session state
*/production/session-state/

# Generated outputs (regenerated from scripts)
*/analysis/outputs/

# Hook state
.experiment-notify-manifest

# Environment
*.egg-info/
__pycache__/
.env
```
