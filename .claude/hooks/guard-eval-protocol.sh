#!/bin/bash
# guard-eval-protocol.sh — PreToolUse: Bash
# Warns before running experiment code if the eval protocol is not locked.
# Does NOT block — exits 0 after warning, so the researcher can override.
# A blocked experiment run is worse than a warned one.

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

# Only check commands that look like experiment runs
if ! echo "$COMMAND" | grep -qE "(python|python3).*(train|run|experiment|main|evaluate)"; then
    exit 0
fi

# Check if eval protocol exists and is locked
PROTOCOL=$(ppath "experiments/eval-protocol.md")
LOGFILE=$(ppath "research/research-log.md")

if [ ! -f "$PROTOCOL" ]; then
    echo "" >&2
    echo "⚠️  WARNING — No evaluation protocol found" >&2
    echo "" >&2
    echo "You are about to run an experiment but $PROTOCOL" >&2
    echo "does not exist." >&2
    echo "" >&2
    echo "Running experiments without a locked eval protocol risks:" >&2
    echo "  • Changing success criteria after seeing results (p-hacking)" >&2
    echo "  • Forgetting which metrics were primary vs. exploratory" >&2
    echo "  • Reviewer rejection for undisclosed metric selection" >&2
    echo "" >&2
    echo "Run /eval-metrics to create and lock the protocol first." >&2
    echo "Proceeding anyway — this warning is logged." >&2
    echo "" >&2

    # Log the warning
    if [ -f "$LOGFILE" ]; then
        echo "" >> "$LOGFILE"
        echo "## ⚠️ WARNING $(date '+%Y-%m-%d %H:%M') — Experiment run without eval protocol" >> "$LOGFILE"
        echo "Command: \`$COMMAND\`" >> "$LOGFILE"
    fi
    exit 0
fi

if ! grep -qi "LOCKED\|status: locked" "$PROTOCOL"; then
    echo "" >&2
    echo "⚠️  WARNING — Evaluation protocol is not locked" >&2
    echo "" >&2
    echo "File:   $PROTOCOL" >&2
    echo "Status: Not marked as LOCKED" >&2
    echo "" >&2
    echo "Edit the file and add 'Status: LOCKED' before running experiments." >&2
    echo "Proceeding anyway — this warning is logged." >&2
    echo "" >&2
    exit 0
fi

exit 0
