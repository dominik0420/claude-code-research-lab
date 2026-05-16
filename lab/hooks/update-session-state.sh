#!/bin/bash
# update-session-state.sh — PostToolUse: Write
# Keeps production/session-state/active.md current after key milestones.
# This is the recovery file — if context is lost, /start reads this to
# understand where the project stands.

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

# Update session state
STATE_FILE="production/session-state/active.md"
mkdir -p "production/session-state"

# Build a snapshot of what exists
python3 - <<'PYEOF'
import os, datetime

state_file = "production/session-state/active.md"
milestone = os.environ.get("MILESTONE", "")

# Discover what exists
checks = {
    "Hypothesis": "research/hypothesis.md",
    "Proposal": "research/proposal.md",
    "Study design": "research/study-design.md",
    "Eval protocol": "experiments/eval-protocol.md",
    "IRB protocol": "research/irb-protocol.md",
    "Lit survey": "literature/survey.md",
    "Paper outline": "papers/outline.md",
}

# Check experiment specs
specs = []
if os.path.isdir("experiments/specs"):
    specs = [f for f in os.listdir("experiments/specs") if f.endswith(".md")]

# Check paper drafts
drafts = []
if os.path.isdir("papers/drafts"):
    drafts = [f for f in os.listdir("papers/drafts") if f.endswith(".md")]

lines = []
lines.append(f"## Session State — Updated {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
lines.append("")
lines.append(f"**Last milestone:** {os.environ.get('MILESTONE', 'unknown')}")
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

with open(state_file, "w") as f:
    f.write("\n".join(lines) + "\n")
PYEOF

exit 0
