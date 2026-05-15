# Directory Structure

```
/
├── CLAUDE.md                        # Master configuration (read first)
├── install.bat                      # Windows: copies lab/ → .claude/
├── install.sh                       # Unix: copies lab/ → .claude/
│
├── lab/                             # Lab config (copy to .claude/ before use)
│   ├── agents/                      # 22 agent definitions
│   ├── commands/                    # 30 slash command definitions
│   ├── docs/                        # Documentation and templates
│   └── rules/                       # Path-specific rules
│
├── research/                        # Research documents
│   ├── idea.md                      # Initial idea from /ideate
│   ├── hypothesis.md                # THE research hypothesis (anchor document)
│   ├── proposal.md                  # Full research proposal
│   └── research-log.md              # Running log of decisions and pivots
│
├── literature/                      # Literature review
│   ├── survey.md                    # Literature survey by theme
│   ├── gap-analysis.md              # Property matrix and gap statement
│   ├── bibliography.bib             # BibTeX references
│   └── papers/                      # Individual paper notes
│
├── experiments/                     # Experiment management
│   ├── eval-protocol.md             # LOCKED evaluation protocol (write before experiments)
│   ├── specs/                       # Experiment specs (one per experiment)
│   ├── configs/                     # YAML configs (one per experiment run)
│   ├── results/                     # Experiment outputs (gitignore if large)
│   └── baseline-plan.md             # Baseline comparison plan
│
├── src/                             # Research source code
│   ├── models/                      # Model architectures
│   ├── data/                        # Dataset loading and preprocessing
│   ├── training/                    # Training loops, optimizers
│   ├── evaluation/                  # Metric computation
│   └── utils/                       # Shared utilities
│
├── scripts/                         # Runnable entry points
│   ├── train.py                     # Main training script
│   ├── evaluate.py                  # Standalone evaluation
│   └── reproduce.py                 # Reproduce a result from a config
│
├── tests/                           # Tests
│   ├── test_models.py               # Unit tests for models
│   ├── test_data.py                 # Data pipeline tests
│   └── test_smoke.py                # Quick end-to-end smoke tests
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
│   ├── drafts/                      # Section drafts
│   │   ├── abstract.md
│   │   ├── introduction.md
│   │   ├── related-work.md
│   │   ├── method.md
│   │   ├── experiments.md
│   │   └── conclusion.md
│   ├── main.tex (or .md)            # Integrated paper
│   └── review-panel-report.md       # Simulated peer review output
│
└── production/                      # Project management
    ├── milestones/                  # Milestone definitions
    ├── sprints/                     # Sprint plans
    │   └── current-sprint.md        # Active sprint
    ├── risk-register.md             # Known risks and mitigations
    ├── camera-ready-checklist.md    # Pre-submission checklist
    └── session-state/               # Active session state (gitignored)
        └── active.md                # Current work context
```

## Key Files

| File | Owned By | Purpose |
|------|----------|---------|
| `research/hypothesis.md` | `principal-investigator` | THE anchor document — everything serves the hypothesis |
| `experiments/eval-protocol.md` | `lead-researcher` | Locked before experiments — defines success |
| `papers/outline.md` | `paper-author` | Paper structure — defines section content |
| `production/session-state/active.md` | All | Recovery point after context loss |
| `research/research-log.md` | `principal-investigator` | Decision history |

## Gitignore Recommendations

```gitignore
# Large data files
data/raw/
data/processed/
experiments/results/
experiments/logs/

# Session state
production/session-state/

# Generated outputs (regenerated from scripts)
analysis/outputs/

# Environment
*.egg-info/
__pycache__/
.env
```
