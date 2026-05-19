#!/bin/bash
# session-summary.sh — Stop
# Runs when Claude Code ends a session. Prints a brief summary of
# project state so the researcher knows exactly where they left off.
# Also useful for catching the most common "forgot to do X" errors.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

export PDIR=$(get_project_dir)

python3 - <<'PYEOF'
import os, datetime, sys

pdir = os.environ.get("PDIR", "")
def ppath(rel):
    return os.path.join(pdir, rel) if pdir else rel

def exists(rel):
    return os.path.exists(ppath(rel))

def count_files(rel, extension=".md"):
    path = ppath(rel)
    if not os.path.isdir(path):
        return 0
    return len([f for f in os.listdir(path) if f.endswith(extension)])

def get_status(rel, keyword="LOCKED"):
    path = ppath(rel)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return keyword.upper() in content.upper()
    except:
        return False

# ── Collect state ──────────────────────────────────────────────────────────
paradigm = "Unknown"
project_name = pdir if pdir else "(repo root)"
if os.path.exists("CLAUDE.md"):
    try:
        with open("CLAUDE.md", "r", encoding="utf-8") as f:
            for line in f:
                if "Research Paradigm" in line and "CHOOSE" not in line:
                    paradigm = line.split(":", 1)[-1].strip().strip("[]")
                    break
    except:
        pass

has_hypothesis   = exists("research/hypothesis.md")
has_proposal     = exists("research/proposal.md")
has_study_design = exists("research/study-design.md")
has_lit_survey   = exists("literature/survey.md")
has_eval         = exists("experiments/eval-protocol.md")
eval_locked      = get_status("experiments/eval-protocol.md", "LOCKED")
has_irb          = exists("research/irb-protocol.md")
n_specs          = count_files("experiments/specs")

results_path = ppath("experiments/results")
if os.path.isdir(results_path):
    n_results = len([
        f for f in os.listdir(results_path)
        if os.path.isfile(os.path.join(results_path, f))
    ])
else:
    n_results = 0

has_outline  = exists("papers/outline.md")
n_drafts     = count_files("papers/drafts")
has_run_log  = exists("experiments/run-log.md")

# ── Print summary ──────────────────────────────────────────────────────────
BORDER = "═" * 54
print(f"\n╔{BORDER}╗", file=sys.stderr)
print(f"║  📋 Session Summary — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}".ljust(55) + "║", file=sys.stderr)
print(f"╚{BORDER}╝", file=sys.stderr)
print("", file=sys.stderr)

print(f"  Project:  {project_name}", file=sys.stderr)
print(f"  Paradigm: {paradigm}", file=sys.stderr)
print("", file=sys.stderr)

print("  Research Foundation:", file=sys.stderr)
print(f"    {'✅' if has_hypothesis else '⬜'} Hypothesis", file=sys.stderr)
print(f"    {'✅' if has_proposal else '⬜'} Research proposal", file=sys.stderr)
print(f"    {'✅' if has_lit_survey else '⬜'} Literature survey", file=sys.stderr)

if "social" in paradigm.lower() or "mixed" in paradigm.lower():
    print(f"    {'✅' if has_study_design else '⬜'} Study design", file=sys.stderr)
    print(f"    {'✅' if has_irb else '⚠️ '} IRB protocol {'(NEEDED before data collection)' if not has_irb else ''}", file=sys.stderr)

print("", file=sys.stderr)
print("  Experiments:", file=sys.stderr)

if "ml" in paradigm.lower() or paradigm == "Unknown":
    if eval_locked:
        print(f"    ✅ Eval protocol — LOCKED", file=sys.stderr)
    elif has_eval:
        print(f"    ⚠️  Eval protocol exists but NOT LOCKED", file=sys.stderr)
    else:
        print(f"    ⬜ Eval protocol (run /eval-metrics before experiments)", file=sys.stderr)

print(f"    {'✅' if n_specs > 0 else '⬜'} Specs: {n_specs} written", file=sys.stderr)
result_label = f"{n_results} results files" if n_results > 0 else "no results yet"
print(f"    {'✅' if n_results > 0 else '⬜'} Results: {result_label}", file=sys.stderr)

print("", file=sys.stderr)
print("  Paper:", file=sys.stderr)
print(f"    {'✅' if has_outline else '⬜'} Outline", file=sys.stderr)
print(f"    {'✅' if n_drafts > 0 else '⬜'} Drafted sections: {n_drafts}", file=sys.stderr)

# ── Critical warnings ──────────────────────────────────────────────────────
warnings = []
if n_results > 0 and not has_eval:
    warnings.append("Results exist but no eval protocol — document what you measured and why.")
if n_results > 0 and not has_run_log:
    warnings.append("Results exist but no run log — git hash not captured.")
if has_study_design and not has_irb and ("social" in paradigm.lower()):
    warnings.append("Study design written but no IRB protocol — run /irb-protocol.")
if n_drafts > 0 and not has_outline:
    warnings.append("Paper sections drafted without an outline — run /outline-paper first.")

if warnings:
    print("", file=sys.stderr)
    print("  ⚠️  Before next session:", file=sys.stderr)
    for w in warnings:
        print(f"    • {w}", file=sys.stderr)

print("", file=sys.stderr)

PYEOF

exit 0
