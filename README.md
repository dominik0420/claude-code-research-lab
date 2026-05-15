<div align="center">

# Claude Code Research Lab

**Turn a single Claude Code session into a full research lab.**  
22 agents · 37 commands · 12 hooks · ML and Social Science tracks

[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-22-blue?style=flat-square)](.claude/agents/)
[![Commands](https://img.shields.io/badge/commands-37-blueviolet?style=flat-square)](.claude/commands/)
[![Hooks](https://img.shields.io/badge/hooks-12-red?style=flat-square)](.claude/hooks/)
[![Rules](https://img.shields.io/badge/rules-3-orange?style=flat-square)](.claude/rules/)
[![Tracks](https://img.shields.io/badge/tracks-ML%20%2B%20Social%20Science-teal?style=flat-square)](#two-tracks)
[![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-black?style=flat-square)](https://claude.ai/code)

[English](README.md) · [中文](README_CN.md)

</div>

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-research-lab
cd claude-code-research-lab

# Activate the lab configuration (one-time)
mv lab .claude          # Mac / Linux
Move-Item lab .claude   # Windows PowerShell

claude
```

Once inside Claude Code, run `/start`. The onboarding command asks three questions, determines your research paradigm, and routes you to the appropriate workflow. No manual configuration required.

---

## Two Tracks

`/start` runs a decision tree and sets the active track automatically. The paradigm can also be set manually in `CLAUDE.md`.

| Track | For | Key commands |
|-------|-----|-------------|
| **ML** | Model training, benchmarks, ablations, experiment pipelines | `/experiment-design`, `/implement`, `/eval-metrics`, `/team-experiments` |
| **Social Science** | Surveys, interviews, qualitative coding, IRB | `/study-design`, `/survey-design`, `/irb-protocol`, `/interview-guide`, `/qual-codebook` |
| **Mixed Methods** | Computational social science, hybrid designs | Both tracks, sequenced by `/study-design` |

---

## Commands

### Discovery
| Command | Description |
|---------|-------------|
| `/start` | Decision tree: detects paradigm, reads project state, routes to the appropriate workflow |
| `/help` | Context-aware next-step suggestions based on current project state |
| `/status` | Project status snapshot |
| `/ideate [area]` | Generate 3 concrete research directions from a vague topic |
| `/hypothesis` | Guided process: formalize a vague idea into a falsifiable hypothesis with mechanism and quantitative prediction |
| `/lit-review [topic]` | Systematic literature survey with gap analysis |
| `/gap-analysis` | Position contribution against prior work |
| `/research-proposal` | Write the full research proposal document |

### Planning — ML Track
| Command | Description |
|---------|-------------|
| `/eval-metrics` | Lock the evaluation protocol — **required before any experiments** |
| `/experiment-design [name]` | Design an experiment with full spec: conditions, metrics, baselines, compute budget |
| `/baseline-plan` | Plan and justify all comparison methods |
| `/ablation-design [method]` | Design the ablation study matrix |
| `/sprint-plan` | Sprint schedule to submission deadline |
| `/run-plan` | Execution order and inter-experiment dependencies |
| `/milestone-review` | Progress review against milestones |

### Planning — Social Science Track
| Command | Description |
|---------|-------------|
| `/study-design` | Study design: design type, variables, validity threats, IRB flags, analysis plan |
| `/survey-design` | Questionnaire instrument: item wording, scales, response format, pilot testing plan |
| `/irb-protocol` | Ethics board submission: risk classification, consent form, data management plan |
| `/sampling-plan` | Power analysis (quantitative) or saturation strategy (qualitative) with recruitment plan |
| `/interview-guide` | Semi-structured interview or focus group guide with verbatim scripts and probes |
| `/qual-codebook` | Qualitative coding scheme with inter-rater reliability protocol (Cohen's κ) |

### Building
| Command | Description |
|---------|-------------|
| `/data-pipeline [dataset]` | Design and implement the data processing pipeline |
| `/implement [spec]` | Implement an experiment from its spec file |
| `/code-review [path]` | Review code for correctness and reproducibility |
| `/reproduce [paper]` | Implement a baseline paper's results |

### Analysis
| Command | Description |
|---------|-------------|
| `/analyze [experiment]` | Analyze results with structured interpretation |
| `/stat-test [experiment]` | Significance tests, regression, Cronbach's α, Cohen's κ |
| `/visualize` | Generate publication-quality figures |
| `/failure-analysis [experiment]` | Analyze failure cases and characterize limitations |

### Writing
| Command | Description |
|---------|-------------|
| `/outline-paper` | Paper outline — must exist before section drafting begins |
| `/write-section [section]` | Draft a specific paper section |
| `/review-paper` | Simulated peer review panel |
| `/write-rebuttal` | Author response to reviewer comments |
| `/camera-ready [venue]` | Final submission checklist for a specific venue |

### Orchestration
| Command | Description |
|---------|-------------|
| `/team-experiments [name]` | Full pipeline: design → build → run → reproduce → verify |
| `/team-writing` | Full pipeline: outline → draft all sections → integrate |
| `/team-review` | 3 independent reviewers → area chair meta-review |

---

## Agents

Agents are invoked automatically by commands or can be called directly by name.

### Tier 1 — Research Leadership (Opus)
| Agent | Domain |
|-------|--------|
| `research-director` | Scientific vision, contribution positioning, publish/no-publish decisions |
| `principal-investigator` | Hypothesis formation, daily research decisions, result interpretation |
| `project-manager` | Sprints, milestones, deadlines, risk management |

### Tier 2 — Department Leads (Sonnet)
| Agent | Domain |
|-------|--------|
| `lead-researcher` | Experiment design, evaluation protocol, ablations — ML Track |
| `social-researcher` | Study design, survey methodology, qualitative methods, IRB — Social Science Track |
| `lead-engineer` | Code architecture, quality standards, infrastructure |
| `data-scientist` | Statistical analysis, data quality, visualization strategy |
| `paper-author` | Writing strategy, narrative arc, venue compliance |
| `literature-lead` | Literature survey, gap analysis, related work positioning |

### Tier 3 — Specialists (Sonnet / Haiku)
| Agent | Domain |
|-------|--------|
| `ml-engineer` | Model implementation |
| `data-engineer` | Data pipelines |
| `stats-analyst` | ML benchmarks, survey statistics, regression, reliability measures |
| `viz-engineer` | Figures and tables |
| `code-reviewer` | Code correctness and reproducibility |
| `reproducibility-engineer` | End-to-end experiment reproducibility |
| `ablation-analyst` | Ablation design and interpretation |
| `baseline-engineer` | Baseline implementation and fair comparison |
| `scientific-writer` | Section-level academic writing |
| `peer-reviewer` | Simulated peer review |
| `ethics-reviewer` | ML dual-use risk / Social Science IRB and participant welfare |
| `devops-researcher` | Compute infrastructure |
| `domain-specialist` | Domain-specific knowledge (configurable per project) |

---

## Hooks

12 hooks enforce research integrity automatically throughout the session.

| Hook | Event | Behavior |
|------|-------|----------|
| `guard-results` | PreToolUse: Write\|Edit | **Blocks** any write to `experiments/results/` — results are immutable |
| `guard-eval-protocol` | PreToolUse: Bash | Warns before running experiments without a locked evaluation protocol |
| `guard-irb` | PreToolUse: Write | Warns before writing to data collection paths without an IRB protocol |
| `validate-experiment-command` | PreToolUse: Bash | Validates experiment commands have config files and output directories |
| `log-research-activity` | PostToolUse: Write | Auto-appends timestamped entries to `research/research-log.md` |
| `validate-experiment-spec` | PostToolUse: Write | Validates specs in `experiments/specs/` have all required fields |
| `update-session-state` | PostToolUse: Write | Keeps `production/session-state/active.md` current after each milestone |
| `capture-git-hash` | PostToolUse: Bash | Logs git hash and branch to `experiments/run-log.md` after experiment runs |
| `check-hardcoded-paths` | PostToolUse: Write | Scans Python source files for hardcoded paths, hyperparameters, missing seeds |
| `track-paper-sections` | PostToolUse: Write | Rebuilds `papers/STATUS.md` with DRAFT / REVIEWED / APPROVED status per section |
| `experiment-complete-notify` | PostToolUse: Write | Notifies when new results files appear; suggests next commands |
| `session-summary` | Stop | Prints a full project state checklist at session end |

---

## Workflows

### ML Track

```
# From a vague idea to a submitted experiment
/ideate [area]          → 3 concrete research directions
/lit-review [area]      → systematic survey of the space
/hypothesis             → formalize the research question
/eval-metrics           → lock evaluation protocol before writing any code
/experiment-design      → produce the full experiment specification
/team-experiments       → design → build → run → reproduce → verify

# From results to submitted paper
/analyze [experiment]   → structured interpretation of results
/stat-test              → significance tests and effect sizes
/outline-paper          → argument structure
/team-writing           → draft all sections
/team-review            → simulated peer review panel
```

### Social Science Track

```
# Study design and data collection
/ideate [topic]         → 3 concrete research directions
/hypothesis             → formalize the research question
/study-design           → full study design with validity analysis
/survey-design          → questionnaire instrument
/interview-guide        → semi-structured interview or focus group guide
/irb-protocol           → ethics board submission package
/sampling-plan          → sample size justification and recruitment plan

# Analysis and writing
/analyze [study]        → run the planned analysis
/stat-test              → regression, reliability measures, significance testing
/qual-codebook          → qualitative coding scheme with IRR protocol
/outline-paper → /team-writing → /team-review
```

---

## Research Integrity

The following rules are enforced automatically by hooks and agents. No component in the system can bypass them.

1. **Evaluation protocol is locked before experiments run.** `/eval-metrics` must exist and be marked `LOCKED` before any experiment command executes.
2. **Results files are immutable.** Writes to `experiments/results/` are blocked at the hook level. To correct an error, re-run the experiment with an updated config.
3. **Baselines receive equal tuning budget.** The `baseline-engineer` agent rejects configurations that give the proposed method an unfair advantage.
4. **Research log is append-only.** `research/research-log.md` is written automatically by the `log-research-activity` hook and is never edited retroactively.
5. **All conditions are reported.** Every condition defined in an experiment spec must appear in the results section. The `lead-researcher` gate rejects papers that omit conditions.
6. **IRB precedes data collection.** The `guard-irb` hook warns on any write to data collection paths without `research/irb-protocol.md` present.

---

## Repository Structure

```
.claude/
  agents/          ← 22 agent definitions
  commands/        ← 37 slash commands
  hooks/           ← 12 lifecycle hooks
  docs/            ← guides and templates
    templates/     ← experiment spec, paper outline, sprint plan
  rules/           ← path-specific enforcement rules
  settings.json    ← hook configuration
CLAUDE.md          ← master config: paradigm, domain, framework, target venue
CONTRIBUTING.md
LICENSE
README.md
README_CN.md
.gitignore
```

Project directories created at runtime:

```
research/            ← hypothesis, proposal, study design, research log
literature/          ← survey, gap analysis, bibliography
experiments/         ← specs, configs, eval protocol, run log, results
src/                 ← models, data loaders, training, evaluation, utils
data/                ← raw (gitignored), processed (gitignored)
baselines/
analysis/            ← scripts, figures, outputs (gitignored)
papers/              ← outline, section drafts, STATUS.md
production/          ← milestones, sprints, session state
```

---

## Collaboration Protocol

Every agent requests permission before writing any file:

> "May I write this to `[filepath]`?"

No agent writes, edits, or executes experiments without explicit approval. Every workflow follows the same sequence:

**Question → Hypothesis → Design → Draft → Review → Approve → Execute**

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding agents, commands, and tracks.

## License

[MIT](LICENSE)
