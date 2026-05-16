# Claude Code Research Lab — Quick Start Guide

## What Is This?

This is a complete Claude Code agent architecture for AI/ML research. It organizes
22 specialized agents into a research lab hierarchy that mirrors how a real research
lab operates: a PI who owns the scientific vision, engineers who build the infrastructure,
analysts who rigorously interpret results, and writers who communicate findings.

The lab covers the complete research lifecycle:
**Ideation → Literature → Hypothesis → Experiments → Analysis → Writing → Review → Submission**

## How to Use

### 1. Understand the Hierarchy

Three tiers of agents:

**Tier 1 (Opus)** — Research leadership
- `research-director` — scientific vision, contribution positioning, publish/no-publish decisions
- `principal-investigator` — daily research decisions, hypothesis, result interpretation
- `project-manager` — timelines, sprints, deadlines, risk management

**Tier 2 (Sonnet)** — Department leads
- `lead-researcher` — experiment design, evaluation protocols, ablations
- `lead-engineer` — codebase architecture, code quality, infrastructure
- `data-scientist` — statistical analysis, data quality, visualization strategy
- `paper-author` — writing strategy, narrative, venue compliance
- `literature-lead` — literature survey, gap analysis, related work

**Tier 3 (Sonnet/Haiku)** — Specialists
- `ml-engineer`, `data-engineer`, `stats-analyst`, `viz-engineer`
- `code-reviewer`, `reproducibility-engineer`, `ablation-analyst`, `baseline-engineer`
- `scientific-writer`, `peer-reviewer`, `ethics-reviewer`, `devops-researcher`, `domain-specialist`

### 2. Pick the Right Agent

| I need to... | Use this agent |
|-------------|---------------|
| Decide if this contribution is publishable | `research-director` |
| Formulate or refine the hypothesis | `principal-investigator` |
| Plan the sprint | `project-manager` |
| Design a fair experiment | `lead-researcher` |
| Review or architect code | `lead-engineer` |
| Analyze experimental results | `data-scientist` |
| Write a paper section | `paper-author` or `scientific-writer` |
| Survey the literature | `literature-lead` |
| Implement a model | `ml-engineer` |
| Build a data pipeline | `data-engineer` |
| Run statistical tests | `stats-analyst` |
| Generate paper figures | `viz-engineer` |
| Check code correctness | `code-reviewer` |
| Verify reproducibility | `reproducibility-engineer` |
| Design ablations | `ablation-analyst` |
| Implement baselines | `baseline-engineer` |
| Get simulated peer review | `peer-reviewer` |
| Check ethical implications | `ethics-reviewer` |
| Set up compute infra | `devops-researcher` |

### 3. Use Slash Commands for Common Tasks

| Command | What it does |
|---------|-------------|
| `/start` | First session onboarding — where are you, what's next |
| `/help` | Context-aware next-step guidance |
| `/status` | Quick project status snapshot |
| `/ideate` | Brainstorm research directions |
| `/hypothesis` | Formalize a vague idea into a testable hypothesis |
| `/lit-review [topic]` | Systematic literature survey |
| `/gap-analysis` | Position contribution vs. prior work |
| `/research-proposal` | Write the full research proposal |
| `/eval-metrics` | Lock the evaluation protocol (do this BEFORE running experiments) |
| `/experiment-design [name]` | Design a specific experiment |
| `/baseline-plan` | Plan the baseline comparisons |
| `/ablation-design [method]` | Design ablation studies |
| `/data-pipeline [dataset]` | Build the data pipeline |
| `/implement [spec]` | Implement an experiment from its spec |
| `/code-review [file]` | Review code for correctness |
| `/run-plan` | Plan the experiment execution order |
| `/reproduce [paper]` | Reproduce a baseline paper's results |
| `/analyze [experiment]` | Analyze experimental results |
| `/stat-test [experiment]` | Run significance tests |
| `/visualize` | Generate publication figures |
| `/failure-analysis [experiment]` | Analyze failure cases |
| `/outline-paper` | Create the paper outline |
| `/write-section [section]` | Draft a paper section |
| `/review-paper` | Simulated peer review |
| `/write-rebuttal` | Write a conference rebuttal |
| `/camera-ready [venue]` | Final submission checklist |
| `/sprint-plan` | Create/update the sprint plan |
| `/milestone-review` | Review milestone progress |
| `/team-experiments [name]` | Run the full experiment pipeline |
| `/team-writing` | Run the full writing pipeline |
| `/team-review` | Run the full 3-reviewer panel |

### 4. The Research Lifecycle

**Phase 1: Discovery** (0–20% of project time)
1. `/ideate` → brainstorm 3 directions
2. `/lit-review [area]` → survey prior work
3. `/gap-analysis` → position the contribution
4. `/hypothesis` → formalize the research question

**Phase 2: Planning** (5–10%)
5. `/research-proposal` → write the contract
6. `/eval-metrics` → lock evaluation (BEFORE ANY EXPERIMENTS)
7. `/experiment-design` → design each experiment
8. `/baseline-plan` → identify comparison methods
9. `/ablation-design` → plan ablation matrix
10. `/sprint-plan` → schedule to submission deadline

**Phase 3: Building** (20–30%)
11. `/data-pipeline [dataset]` → prepare data
12. `/implement [spec]` → build the code
13. `/code-review src/` → verify correctness
14. `/reproduce [baseline]` → implement baselines

**Phase 4: Experimentation** (20–30%)
15. `/run-plan` → plan execution order
16. [Run experiments]
17. `/analyze [experiment]` → interpret results
18. `/stat-test [experiment]` → significance testing
19. `/failure-analysis` → understand limitations

**Phase 5: Writing** (15–25%)
20. `/outline-paper` → structure the argument
21. `/visualize` → create figures
22. `/team-writing` → draft all sections
23. `/review-paper` → get simulated review

**Phase 6: Submission** (5–10%)
24. Address review feedback
25. `/write-rebuttal` (if needed post-submission)
26. `/camera-ready [venue]` → final checklist

### 5. Follow the Coordination Rules

1. Work flows down the hierarchy: Directors → Leads → Specialists
2. Scientific conflicts escalate to `research-director`
3. Scheduling conflicts escalate to `project-manager`
4. Cross-department work is coordinated by `project-manager`
5. No agent modifies files outside its domain without delegation
6. All significant decisions go into `research/research-log.md`

## First Steps for a New Project

**Don't know where to begin?** Run `/start`. It asks where you are and routes
you to the right workflow.

### Path A: "I have a vague idea"
1. `/ideate [area]` — generate 3 concrete directions
2. `/lit-review [area]` — validate the space
3. `/hypothesis` — formalize the question
4. `/research-proposal` — write the contract

### Path B: "I have a hypothesis"
1. `/eval-metrics` — lock evaluation first
2. `/experiment-design` — design the core experiment
3. `/baseline-plan` — identify comparisons
4. `/sprint-plan` — schedule to deadline

### Path C: "I have results, need to write"
1. `/analyze [experiments]` — verify analysis is complete
2. `/stat-test [experiments]` — run significance tests
3. `/outline-paper` — structure the argument
4. `/team-writing` — draft the paper

### Path D: "I have a draft, need review"
1. `/team-review` — full 3-reviewer panel
2. Address critical weaknesses
3. `/camera-ready [venue]` — final check

## File Structure Reference

```
CLAUDE.md                           # Master config
lab/                                # Lab configuration (→ .claude/ after install)
  agents/                           # 22 agent definitions
  commands/                         # 37 slash commands
  docs/                             # Documentation
    quick-start.md                  # This file
    agent-roster.md                 # Agent reference table
    coordination-rules.md           # How agents coordinate
    context-management.md           # Context management strategy
    directory-structure.md          # Project directory layout
    research-standards.md           # Research quality standards
    templates/                      # Document templates
  rules/                            # Path-specific rules
research/                           # Research documents
  hypothesis.md                     # The research hypothesis
  proposal.md                       # The research proposal
  research-log.md                   # Decisions and pivots log
  idea.md                           # Initial idea (from /ideate)
literature/                         # Literature review
  survey.md                         # Literature survey
  gap-analysis.md                   # Gap analysis and positioning
  bibliography.bib                  # References
experiments/                        # Experiment management
  specs/                            # Experiment specs (write before code)
  configs/                          # Experiment config YAML files
  results/                          # Experiment outputs (gitignored by default)
  eval-protocol.md                  # Locked evaluation protocol
src/                                # Research code
  models/                           # Model architectures
  data/                             # Data loaders
  training/                         # Training loops
  evaluation/                       # Evaluation code
  utils/                            # Shared utilities
data/                               # Data files
  raw/                              # Raw data (never modified)
  processed/                        # Processed data
baselines/                          # Baseline implementations
analysis/                           # Analysis scripts and outputs
  outputs/                          # Generated tables and figures
papers/                             # Paper files
  outline.md                        # Paper structure
  drafts/                           # Section drafts
  main.tex (or .md)                 # Integrated paper
production/                         # Project management
  milestones/                       # Milestone definitions
  sprints/                          # Sprint plans
  session-state/                    # Active session state (gitignored)
```
