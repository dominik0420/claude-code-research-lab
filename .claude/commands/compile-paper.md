---
name: compile-paper
description: "Assembles all section drafts into a single LaTeX paper and compiles it to PDF. Reads papers/drafts/, applies the paper template, converts markdown to LaTeX, writes papers/main.tex, and runs the bundled compiler. Run after /team-writing is complete."
argument-hint: "[venue: neurips | icml | iclr | acl | cvpr | article] [optional: --no-compile]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

You are the paper compilation agent. Your job is to take all written section drafts
and produce a complete, compilable LaTeX paper.

## Prerequisites Check

Before compiling, verify:
- [ ] `papers/outline.md` exists — needed for section ordering
- [ ] `papers/drafts/` contains at least one `.md` file
- [ ] `papers/STATUS.md` exists — check which sections are APPROVED or DRAFT

If the outline is missing: tell the user to run `/outline-paper` first.
If no drafts exist: tell the user to run `/team-writing` first.

## Step 1 — Read the Outline and Drafts

Read `papers/outline.md` to determine:
- Paper title
- Author list (if present)
- Target venue
- Section order

Read all files in `papers/drafts/` in outline order.
Also read `papers/STATUS.md` to note which sections are still DRAFT (not APPROVED).

## Step 2 — Determine Venue Template

Parse the argument to determine venue. If no argument given, check CLAUDE.md for `Paper Target`.

| Argument | LaTeX class used |
|----------|-----------------|
| `neurips` | neurips_2024 |
| `icml` | icml2024 |
| `iclr` | iclr2025 |
| `acl` | acl_natbib |
| `cvpr` | cvpr |
| `article` (default) | article with geometry |

## Step 3 — Run the Compiler

Run the bundled Python assembler:

```bash
python3 .claude/scripts/compile_paper.py \
  --outline papers/outline.md \
  --drafts-dir papers/drafts \
  --output papers/main.tex \
  --venue [venue] \
  [--no-compile if user passed that flag]
```

The script:
1. Reads all drafts in outline order
2. Converts markdown to LaTeX
3. Wraps in the venue template
4. Writes `papers/main.tex`
5. Attempts `pdflatex papers/main.tex -output-directory papers/` (two passes for references)
6. Reports success or compilation errors

## Step 4 — Report

After the compiler runs, report:

```
## Compile Report

Output: papers/main.tex
PDF: papers/main.pdf  [if compilation succeeded]

Sections included (in order):
  ✅ [section name] — APPROVED
  ⚠️  [section name] — DRAFT (not yet approved)

Compilation: [SUCCEEDED / FAILED — see errors below]
[any pdflatex errors, condensed]

Next steps:
  → /review-paper         — simulated peer review
  → /camera-ready [venue] — final submission checklist
```

If compilation failed due to missing pdflatex, report:
> "LaTeX compiled to papers/main.tex. Install pdflatex (TeX Live or MiKTeX) to
> generate PDF, or upload main.tex to Overleaf."

## Draft Sections Warning

Any section still marked DRAFT in STATUS.md gets a visible LaTeX comment:
`% TODO: Section not yet approved — review before submission`
