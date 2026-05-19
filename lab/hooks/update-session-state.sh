#!/bin/bash
# update-session-state.sh — PostToolUse: Write
# Keeps production/session-state/active.md current after key milestones.
# This is the recovery file — if context is lost, /start reads this to
# understand where the project stands.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    print(tool_input.get('file_path', '') or tool_input.get('path', ''))
except:
    print('')
" 2>/dev/null)

# Map file paths to milestone labels
MILESTONE=""
if echo "$FILE_PATH" | grep -q "research/hypothesis"; then
    MILESTONE="Hypothesis defined"
elif echo "$FILE_PATH" | grep -q "research/proposal"; then
    MILESTONE="Research proposal written"
elif echo "$FILE_PATH" | grep -q "research/study-design"; then
    MILESTONE="Study design complete"
elif echo "$FILE_PATH" | grep -q "experiments/eval-protocol"; then
    MILESTONE="Evaluation protocol locked"
elif echo "$FILE_PATH" | grep -q "experiments/specs/"; then
    SPECNAME=$(basename "$FILE_PATH" .md)
    MILESTONE="Experiment spec written: $SPECNAME"
elif echo "$FILE_PATH" | grep -q "research/irb-protocol"; then
    MILESTONE="IRB protocol written"
elif echo "$FILE_PATH" | grep -q "research/instruments/"; then
    MILESTONE="Research instrument created: $(basename $FILE_PATH)"
elif echo "$FILE_PATH" | grep -q "papers/outline"; then
    MILESTONE="Paper outline written"
elif echo "$FILE_PATH" | grep -q "papers/drafts/"; then
    SECTION=$(basename "$FILE_PATH" .md)
    MILESTONE="Paper section drafted: $SECTION"
elif echo "$FILE_PATH" | grep -q "literature/survey"; then
    MILESTONE="Literature survey complete"
elif echo "$FILE_PATH" | grep -q "literature/gap-analysis"; then
    MILESTONE="Gap analysis complete"
else
    exit 0
fi

export MILESTONE
export PDIR=$(get_project_dir)

# Update session state (project-aware path)
STATE_FILE=$(ppath "production/session-state/active.md")
pmkdir "production/session-state/active.md"

# Build a snapshot of what exists
python3 - <<'PYEOF'
import os, datetime

pdir = os.environ.get("PDIR", "")
def ppath(rel):
    return os.path.join(pdir, rel) if pdir else rel

state_file = ppath("production/session-state/active.md")
milestone = os.environ.get("MILESTONE", "")

# Discover what exists
checks = {
    "Hypothesis":    ppath("research/hypothesis.md"),
    "Proposal":      ppath("research/proposal.md"),
    "Study design":  ppath("research/study-design.md"),
    "Eval protocol": ppath("experiments/eval-protocol.md"),
    "IRB protocol":  ppath("research/irb-protocol.md"),
    "Lit survey":    ppath("literature/survey.md"),
    "Paper outline": ppath("papers/outline.md"),
}

# Check experiment specs
specs = []
specs_dir = ppath("experiments/specs")
if os.path.isdir(specs_dir):
    specs = [f for f in os.listdir(specs_dir) if f.endswith(".md")]

# Check paper drafts
drafts = []
drafts_dir = ppath("papers/drafts")
if os.path.isdir(drafts_dir):
    drafts = [f for f in os.listdir(drafts_dir) if f.endswith(".md")]

lines = []
lines.append(f"## Session State — Updated {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
lines.append("")
lines.append(f"**Last milestone:** {milestone}")
lines.append("")
lines.append("### Project Status")
lines.append("")

for label, path in checks.items():
    status = "✅" if os.path.exists(path) else "⬜"
    lines.append(f"- {status} {label}")

if specs:
    lines.append(f"- ✅ Experiment specs: {', '.join(s.replace('.md','') for s in specs)}")
else:
    lines.append("- ⬜ Experiment specs")

if drafts:
    lines.append(f"- ✅ Paper drafts: {', '.join(d.replace('.md','') for d in drafts)}")
else:
    lines.append("- ⬜ Paper drafts")

lines.append("")
lines.append("### Next Step")
lines.append("*(run /start to get a recommendation)*")

os.makedirs(os.path.dirname(state_file), exist_ok=True)
with open(state_file, "w") as f:
    f.write("\n".join(lines) + "\n")
PYEOF

exit 0
