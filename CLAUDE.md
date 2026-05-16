# Claude Code Research Lab — Multi-Paradigm Research Environment

A full research lab inside a single Claude Code session. Specialized agents coordinate
across the complete research lifecycle: idea → literature → design → data → analysis → paper.

Supports two research tracks — set your paradigm and the lab routes accordingly:
- **ML Track**: model training, benchmarks, ablations, experiment pipelines
- **Social Science Track**: survey design, IRB, qualitative coding, mixed methods

## What This Is

This is a structured agent architecture for academic research. It mirrors how a real research
lab operates — a PI who owns the scientific vision, methodologists who design studies,
analysts who interpret results, and writers who communicate findings. Every agent has a
specific domain; no agent steps outside its lane without delegation.

Run `/start` in a new project — it asks three questions and routes you to the right track.

## Research Stack

### Interface Language
- **Interface Language**: [CHOOSE: English / Chinese]

> **All agents read this field.** After `/start` sets it, every agent in the lab
> responds in the configured language for the rest of the session.
> To switch mid-session, edit this line and run `/start` again.

### Paradigm (set this first — it changes which commands are active)
- **Research Paradigm**: [CHOOSE: ML / Social Science / Mixed Methods]
- **Methods Type** *(Social Science)*: [CHOOSE: Quantitative / Qualitative / Mixed]

### ML Track
- **Domain**: [CHOOSE: NLP / CV / RL / Multimodal / Systems / Theory / Other]
- **Framework**: [CHOOSE: PyTorch / JAX / TensorFlow / Other]
- **Language**: Python 3.10+ (primary), Bash (scripts), LaTeX (papers)
- **Experiment Tracking**: [CHOOSE: Weights & Biases / MLflow / Sacred / Custom]
- **Compute**: [CHOOSE: Local GPU / Slurm / AWS / GCP / Azure]
- **Paper Target**: [CHOOSE: NeurIPS / ICML / ICLR / ACL / CVPR / Arxiv / Other]

### Social Science Track
- **Discipline**: [CHOOSE: Sociology / Psychology / Economics / Political Science / Anthropology / Education / Other]
- **Data Collection**: [CHOOSE: Survey / Interview / Observation / Experiment / Secondary Data / Mixed]
- **Analysis Approach**: [CHOOSE: Statistical / Thematic / Discourse / Grounded Theory / Mixed]
- **Citation Format**: [CHOOSE: APA / Chicago / MLA / Vancouver / Other]
- **Journal Target**: [CHOOSE: specify venue]

> **Setup**: After cloning, run `mv lab .claude` (Mac/Linux) or
> `Move-Item lab .claude` (Windows PowerShell) once to activate the lab configuration.
> Then open this folder with Claude Code.
>
> **First session?** Run `/start` — it asks three questions, determines your research
> paradigm, and routes you to the appropriate workflow.

## Project Structure

@.claude/docs/directory-structure.md

## Research Standards

@.claude/docs/research-standards.md

## Coordination Rules

@.claude/docs/coordination-rules.md

## Collaboration Protocol

**Language:** Check the `Interface Language` field above. If it is set to **Chinese**,
write all responses, drafts, questions, and file content in Simplified Chinese (简体中文).
If it is set to **English** or not yet set, use English. This applies to every agent
without exception.

**User-driven collaboration, not autonomous research.**
Every task follows: **Question → Hypothesis → Design → Execute → Approve**

- Agents MUST ask "May I write this to [filepath]?" before using Write/Edit tools
- Agents MUST show drafts or summaries before requesting approval
- No experiments run without user sign-off on the design
- No paper sections written without outline approval
- No commits without user instruction

## Context Management

@.claude/docs/context-management.md

## Coding Standards

@.claude/rules/code.md
