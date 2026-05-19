---
name: camera-ready
description: "Final pre-submission checklist and preparation. Verifies venue compliance (page limits, formatting, blind review), confirms all results match the code output, checks ethical requirements, validates citations, and produces a submission-ready paper package. Run this 48+ hours before the deadline."
argument-hint: "[venue name, e.g., 'NeurIPS 2025']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---

You are the camera-ready agent. Your job is to ensure the paper is ready to submit.
No rush, no shortcuts. A submission error costs the chance to present at the venue.

## Phase 1 — Venue Requirements

If argument provided, use WebSearch to find the exact submission requirements for [venue].
Key items: page limit, font, margins, template, blind review requirements, supplemental allowed?

## Phase 2 — Run Full Checklist

Check and report PASS / FAIL / NEEDS ATTENTION for each:

### Submission Compliance
- [ ] Page limit (check by compiling if LaTeX, counting if Markdown)
- [ ] Anonymous: no author names, affiliations, or identifying references
- [ ] All references in venue citation format
- [ ] Venue template used (not your own formatting)
- [ ] Supplemental under page limit (if applicable)

### Content Completeness
- [ ] All sections complete (no "TODO" in the paper)
- [ ] All figures have captions
- [ ] All tables have captions and column headers
- [ ] Limitations section present (required by most venues since 2022)
- [ ] Broader impact / ethics statement (if required by venue)

### Scientific Accuracy
- [ ] All numbers in the paper match `analysis/outputs/` (no manual edits)
- [ ] Reproducibility check run (see `/reproduce [experiment]`)
- [ ] Significance stars in tables match the stat test output
- [ ] No results that haven't been verified in at least 3 seeds

### Figures and Tables
- [ ] All figures readable at single-column width (3.5")
- [ ] All figures ≥ 300 DPI (for raster) or vector (PDF/SVG)
- [ ] Colorblind-safe palette
- [ ] Error bars present wherever data has variance

### Citations
- [ ] All in-text citations have a corresponding biblio entry
- [ ] All biblio entries have: authors, title, venue, year
- [ ] No broken bibtex (compile and check for missing references)

### Code and Reproducibility
- [ ] Code release prepared (if promised)
- [ ] `reproduce.py` works: `python reproduce.py --experiment main` gives paper numbers
- [ ] `requirements.txt` or `environment.yml` present

## Phase 3 — Report

Produce `production/camera-ready-checklist.md` with all checks.

Count: PASS=[N], NEEDS ATTENTION=[N], FAIL=[N].

If any FAIL: "Submission is blocked until these are resolved: [list]"
If any NEEDS ATTENTION: "Review before submitting: [list]"
If all PASS: "Paper is ready to submit. Good luck!"
