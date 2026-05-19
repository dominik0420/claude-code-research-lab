# Research Quality Standards

These standards define what "done" means at each stage of the research process.
They are enforced by the gate checks in each agent.

## Hypothesis Standards

A hypothesis is ready when it:
- Names a specific method or approach (not "our method")
- Specifies a task and metric
- States a quantitative prediction
- Explains the mechanism (WHY it should work)
- Defines falsification conditions
- States scope explicitly

**Template check**: Fill the hypothesis template in `lab/docs/templates/hypothesis.md`. If you can't fill every field, the hypothesis isn't ready.

## Experiment Design Standards

An experiment is ready to implement when:
- It answers exactly one question (not multiple)
- The primary metric is defined and appropriate for the claim
- All baselines are identified and justified
- Controls are specified (what's held constant)
- Number of seeds/runs is specified (minimum 3)
- Expected results are stated before running
- Compute budget is estimated

## Evaluation Standards

All reported results must:
- Be averaged over ≥3 runs (≥5 preferred)
- Report mean AND standard deviation
- Use the metric defined in `eval-protocol.md` (no post-hoc metric changes)
- Include statistical significance testing when comparison is the main claim
- Note any results that are not statistically significant

## Baseline Standards

All baselines must:
- Be properly tuned (same hyperparameter search budget as proposed method)
- Run in the same evaluation setting
- Reproduce published numbers within 2% (if from literature)
- Be the strongest known version of the competing method

## Code Standards

Research code must:
- Be runnable with one command: `python scripts/train.py --config [config]`
- Have all hyperparameters in a config file (no hardcoding)
- Set and log all random seeds
- Log: timestamp, git hash, config, hardware
- Save results as structured data (JSON/CSV), not just printed output
- Pass smoke tests before full experiment runs

## Writing Standards

Paper sections must:
- Have every claim backed by a citation or a result
- Reference and interpret every table and figure
- Use consistent notation throughout
- Avoid vague language ("interesting", "novel", "significantly" without numbers)
- Meet the venue's page, font, and format requirements

## Reproducibility Standards (Pre-Submission)

Before submission:
- `python reproduce.py --experiment main` produces the paper's main results
- `requirements.txt` or `environment.yml` is present and tested
- Paper numbers match script outputs (no manual edits)
- At least one complete re-run confirms reproducibility

## Paper Sections Requirements by Venue Tier

| Section | NeurIPS/ICML/ICLR | ACL/EMNLP | CVPR/ICCV |
|---------|------------------|-----------|-----------|
| Abstract | ≤150 words | ≤150 words | ≤250 words |
| Limitations | Required | Required | Recommended |
| Broader impact | Required | Recommended | Recommended |
| Code release | Strongly encouraged | Strongly encouraged | Encouraged |
| Statistical tests | Expected | Expected | Expected |
| Ablations | Expected | Expected | Expected |
