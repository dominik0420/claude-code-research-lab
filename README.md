# Claude Code Research Lab

Turn a single Claude Code session into a full research lab.  
22 agents. 37 commands. 12 hooks. Two tracks: ML and Social Science.

[![License: MIT](https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-22-blue?style=flat-square)](.claude/agents/)
[![Commands](https://img.shields.io/badge/commands-37-blueviolet?style=flat-square)](.claude/commands/)
[![Hooks](https://img.shields.io/badge/hooks-12-red?style=flat-square)](.claude/hooks/)
[![Rules](https://img.shields.io/badge/rules-3-orange?style=flat-square)](.claude/rules/)
[![Tracks](https://img.shields.io/badge/tracks-ML%20%2B%20Social%20Science-teal?style=flat-square)](#two-tracks)
[![Built for Claude Code](https://img.shields.io/badge/built%20for-Claude%20Code-black?style=flat-square)](https://claude.ai/code)

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-research-lab
cd claude-code-research-lab

# One-time: activate the lab config
mv lab .claude          # Mac / Linux
Move-Item lab .claude   # Windows PowerShell

claude
```

Then in Claude Code:
```
/start
```

That's it. The decision tree in `/start` asks three questions, determines your research paradigm, and routes you to the right workflow.

---

## Two Tracks

`/start` runs a decision tree and sets the track automatically. You can also set it manually in `CLAUDE.md`.

| Track | For | Key commands |
|-------|-----|-------------|
| **ML** | Model training, benchmarks, ablations, experiment pipelines | `/experiment-design`, `/implement`, `/eval-metrics`, `/team-experiments` |
| **Social Science** | Surveys, interviews, qualitative coding, IRB | `/study-design`, `/survey-design`, `/irb-protocol`, `/interview-guide`, `/qual-codebook` |
| **Mixed Methods** | Computational social science, hybrid designs | Both tracks, sequenced by `/study-design` |

---

## The 37 Commands

### Discovery
| Command | What it does |
|---------|-------------|
| `/start` | Decision tree: detects paradigm, reads project state, routes to the right workflow |
| `/help` | Context-aware next-step suggestions |
| `/status` | Quick project status snapshot |
| `/ideate [area]` | Brainstorm 3 concrete research directions from a vague topic |
| `/hypothesis` | Guided process: turn a vague idea into a falsifiable hypothesis with mechanism + prediction |
| `/lit-review [topic]` | Systematic literature survey with gap analysis |
| `/gap-analysis` | Position your contribution against prior work |
| `/research-proposal` | Write the full research proposal document |

### Planning — ML Track
| Command | What it does |
|---------|-------------|
| `/eval-metrics` | Lock the evaluation protocol — **run before any experiments** |
| `/experiment-design [name]` | Design an experiment with full spec: conditions, metrics, baselines, compute |
| `/baseline-plan` | Plan and justify all comparison methods |
| `/ablation-design [method]` | Design the ablation study matrix |
| `/sprint-plan` | Sprint schedule to submission deadline |
| `/run-plan` | Execution order and dependencies |
| `/milestone-review` | Progress review against milestones |

### Planning — Social Science Track
| Command | What it does |
|---------|-------------|
| `/study-design` | Design type, variables/constructs, validity threats, IRB flags, analysis plan |
| `/survey-design` | Build a questionnaire: item wording, scales, response format, pilot testing plan |
| `/irb-protocol` | Full ethics board submission: risk classification, consent form, data management |
| `/sampling-plan` | Power analysis (quant) or saturation strategy (qual), recruitment plan |
| `/interview-guide` | Semi-structured interview or focus group guide with verbatim scripts and probes |
| `/qual-codebook` | Qualitative coding scheme with IRR protocol (Cohen's κ) |

### Building
| Command | What it does |
|---------|-------------|
| `/data-pipeline [dataset]` | Design and implement the data pipeline |
| `/implement [spec]` | Implement an experiment from its spec file |
| `/code-review [path]` | Review code for correctness and reproducibility |
| `/reproduce [paper]` | Implement a baseline paper's results |

### Analysis
| Command | What it does |
|---------|-------------|
| `/analyze [experiment]` | Analyze results with interpretation |
| `/stat-test [experiment]` | Significance tests, regression, Cronbach's α, Cohen's κ |
| `/visualize` | Generate publication-quality figures |
| `/failure-analysis [experiment]` | Analyze failure cases and limitations |

### Writing
| Command | What it does |
|---------|-------------|
| `/outline-paper` | Paper outline — required before section drafting |
| `/write-section [section]` | Draft a specific section |
| `/review-paper` | Simulated peer review panel |
| `/write-rebuttal` | Conference rebuttal response |
| `/camera-ready [venue]` | Final submission checklist |

### Orchestration
| Command | What it does |
|---------|-------------|
| `/team-experiments [name]` | Full pipeline: design → build → run → reproduce → verify |
| `/team-writing` | Full pipeline: outline → draft all sections → integrate |
| `/team-review` | 3 independent reviewers → area chair meta-review |

---

## The 22 Agents

Agents are invoked automatically by commands, or you can call them directly.

### Tier 1 — Research Leadership (Opus)
| Agent | Owns |
|-------|------|
| `research-director` | Scientific vision, contribution positioning, publish/no-publish |
| `principal-investigator` | Hypothesis formation, daily research decisions, result interpretation |
| `project-manager` | Sprints, milestones, deadlines, risk management |

### Tier 2 — Department Leads (Sonnet)
| Agent | Owns |
|-------|------|
| `lead-researcher` | Experiment design, evaluation protocol, ablations — ML Track |
| `social-researcher` | Study design, survey methodology, qualitative methods, IRB — Social Science Track |
| `lead-engineer` | Code architecture, quality, infrastructure |
| `data-scientist` | Statistical analysis, data quality, visualization strategy |
| `paper-author` | Writing strategy, narrative arc, venue compliance |
| `literature-lead` | Literature survey, gap analysis, related work positioning |

### Tier 3 — Specialists (Sonnet / Haiku)
| Agent | Owns |
|-------|------|
| `ml-engineer` | Model implementation |
| `data-engineer` | Data pipelines |
| `stats-analyst` | ML benchmarks, survey stats, regression, reliability measures |
| `viz-engineer` | Figures and tables |
| `code-reviewer` | Code correctness and reproducibility |
| `reproducibility-engineer` | End-to-end experiment reproducibility |
| `ablation-analyst` | Ablation design and interpretation |
| `baseline-engineer` | Baseline implementation and fair comparison |
| `scientific-writer` | Section-level writing |
| `peer-reviewer` | Simulated peer review |
| `ethics-reviewer` | ML dual-use / Social Science IRB and participant welfare |
| `devops-researcher` | Compute infrastructure |
| `domain-specialist` | Domain-specific knowledge (configurable) |

---

## Common Workflows

### ML Track

```
# Starting from scratch
/ideate [area]          → 3 concrete directions
/lit-review [area]      → survey the space
/hypothesis             → formalize the question
/eval-metrics           → lock evaluation before touching code
/experiment-design      → spec the experiment
/team-experiments       → design → build → run → verify

# Have results, need to write
/analyze [experiments]
/stat-test
/outline-paper
/team-writing
/team-review
```

### Social Science Track

```
# Study design and data collection
/ideate [topic]         → 3 concrete directions
/hypothesis             → formalize the research question
/study-design           → full study design with validity analysis
/survey-design          → questionnaire instrument
  or /interview-guide   → interview guide with probes
/irb-protocol           → ethics board submission
/sampling-plan          → sample size / saturation strategy

# Analysis and writing
/analyze [study]        → run analysis
/stat-test              → regression, reliability, significance
  or /qual-codebook     → qualitative coding scheme
/outline-paper → /team-writing → /team-review
```

---

## Research Integrity Rules

Enforced automatically — no agent can bypass them:

1. **Evaluation protocol is locked before experiments run.** Use `/eval-metrics` first. No moving goalposts.
2. **Results files are immutable.** Never manually edit `experiments/results/`. Regenerate if wrong.
3. **Baselines get equal tuning budget.** Strawman comparisons are rejected.
4. **Research log is append-only.** All decisions recorded in `research/research-log.md`.
5. **No cherry-picking.** Every condition in the spec must appear in the paper.
6. **IRB before data collection.** The ethics-reviewer blocks study execution without an IRB plan.

---

## Repository Structure

```
.claude/
  agents/          ← 22 agent definitions
  commands/        ← 37 slash commands
  docs/            ← guides and templates
    templates/     ← experiment spec, paper outline, sprint plan, etc.
  rules/           ← path-specific enforcement rules
CLAUDE.md          ← master config — set your paradigm, domain, and target venue here
CONTRIBUTING.md
LICENSE
README.md
README_CN.md
.gitignore
```

When you start a project, the lab creates these directories in your working folder:

```
research/            ← hypothesis, proposal, research log, study design
literature/          ← survey, gap analysis, bibliography
experiments/         ← specs, configs, results (gitignored)
src/                 ← models, data, training, evaluation, utils
data/                ← raw (gitignored), processed (gitignored)
baselines/
analysis/            ← scripts, figures, outputs (gitignored)
papers/              ← outline, drafts
production/          ← milestones, sprints, session state
```

---

## Collaboration Protocol

Every agent asks before writing any file:

> "May I write this to [filepath]?"

No agent writes, edits, or runs experiments without your approval. The flow is always:  
**Question → Hypothesis → Design → Show Draft → You Approve → Execute**

---

## Further Reading

- `.claude/docs/quick-start.md` — full lifecycle walkthrough, all four starting-point paths
- `.claude/docs/agent-roster.md` — gate verdicts, delegation maps, full agent reference
- `.claude/docs/coordination-rules.md` — how agents hand off between each other
- `.claude/docs/research-standards.md` — research quality standards for both tracks
