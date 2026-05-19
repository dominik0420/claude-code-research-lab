#!/bin/bash
# capture-git-hash.sh — PostToolUse: Bash
# After running an experiment command, captures the current git hash and
# logs it alongside the command. This ensures every result is traceable
# to a specific code commit — required for reproducibility.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat)

COMMAND=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    print(tool_input.get('command', ''))
except:
    print('')
" 2>/dev/null)

# Only run for experiment-like commands
if ! echo "$COMMAND" | grep -qE "(python|python3).*(train|run|experiment|main|evaluate|eval)"; then
    exit 0
fi

# Capture git hash
GIT_HASH=$(git rev-parse HEAD 2>/dev/null)
GIT_BRANCH=$(git branch --show-current 2>/dev/null)
GIT_STATUS=$(git status --short 2>/dev/null | head -5)

if [ -z "$GIT_HASH" ]; then
    echo "⚠️  No git repo found — experiment not version-tracked." >&2
    echo "   Run: git init && git add . && git commit -m 'Initial commit'" >&2
    exit 0
fi

if [ -n "$GIT_STATUS" ]; then
    echo "⚠️  WARNING: Uncommitted changes present when running experiment." >&2
    echo "   Results may not be reproducible from this git state." >&2
    echo "   Consider committing before running:" >&2
    echo "   git add -A && git commit -m 'Pre-experiment checkpoint'" >&2
fi

# Log to experiment run log (project-aware path)
RUNLOG=$(ppath "experiments/run-log.md")
pmkdir "experiments/run-log.md"

if [ ! -f "$RUNLOG" ]; then
    echo "# Experiment Run Log" > "$RUNLOG"
    echo "" >> "$RUNLOG"
    echo "All experiment runs are logged here with their git hash." >> "$RUNLOG"
    echo "This log ensures every result is traceable to a code version." >> "$RUNLOG"
    echo "" >> "$RUNLOG"
fi

echo "" >> "$RUNLOG"
echo "### $(date '+%Y-%m-%d %H:%M')" >> "$RUNLOG"
echo "**Command:** \`$COMMAND\`" >> "$RUNLOG"
echo "**Git hash:** \`$GIT_HASH\`" >> "$RUNLOG"
echo "**Branch:** $GIT_BRANCH" >> "$RUNLOG"
if [ -n "$GIT_STATUS" ]; then
    echo "**⚠️ Dirty working tree:**" >> "$RUNLOG"
    echo "\`\`\`" >> "$RUNLOG"
    echo "$GIT_STATUS" >> "$RUNLOG"
    echo "\`\`\`" >> "$RUNLOG"
fi

exit 0
