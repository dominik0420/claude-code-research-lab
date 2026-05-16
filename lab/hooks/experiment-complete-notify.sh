#!/bin/bash
# experiment-complete-notify.sh — PostToolUse: Bash
# Fires after any Bash command. Checks whether new result files have appeared
# in experiments/results/ since the last run, and notifies if so.
# Uses a lightweight manifest file to track what was known before.
# This hook intentionally exits 0 always — it is advisory only.

INPUT=$(cat)

# Only check if the bash command looks experiment-related
COMMAND=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('command', ''))
except:
    print('')
" 2>/dev/null)

# Skip if not an experiment-like command
if ! echo "$COMMAND" | grep -qiE "(python|train|run|experiment|eval|test|bash)"; then
    exit 0
fi

RESULTS_DIR="experiments/results"
MANIFEST=".experiment-notify-manifest"

if [ ! -d "$RESULTS_DIR" ]; then
    exit 0
fi

# Collect current result files
CURRENT_FILES=$(find "$RESULTS_DIR" -type f \( -name "*.json" -o -name "*.csv" -o -name "*.txt" \) 2>/dev/null | sort)

if [ -z "$CURRENT_FILES" ]; then
    exit 0
fi

# Load previously seen files
PREVIOUS_FILES=""
if [ -f "$MANIFEST" ]; then
    PREVIOUS_FILES=$(cat "$MANIFEST")
fi

# Diff: find new files
NEW_FILES=$(comm -23 <(echo "$CURRENT_FILES") <(echo "$PREVIOUS_FILES") 2>/dev/null)

if [ -z "$NEW_FILES" ]; then
    # Nothing new — update manifest and exit
    echo "$CURRENT_FILES" > "$MANIFEST"
    exit 0
fi

# Update manifest
echo "$CURRENT_FILES" > "$MANIFEST"

# Notify for each new file
while IFS= read -r NEW_FILE; do
    EXPERIMENT_NAME=$(basename "$NEW_FILE")
    EXPERIMENT_NAME="${EXPERIMENT_NAME%.*}"

    echo "" >&2
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
    echo "  🧪 New result file detected: $NEW_FILE" >&2
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
    echo "" >&2
    echo "  Next steps:" >&2
    echo "  → /analyze $EXPERIMENT_NAME   — interpret results" >&2
    echo "  → /stat-test $EXPERIMENT_NAME — run significance tests" >&2
    echo "  → /failure-analysis $EXPERIMENT_NAME — examine error cases" >&2
    echo "" >&2

    # Log to research log if it exists
    LOGFILE="research/research-log.md"
    if [ -f "$LOGFILE" ]; then
        echo "" >> "$LOGFILE"
        echo "### $(date '+%Y-%m-%d %H:%M') — New result detected: $NEW_FILE" >> "$LOGFILE"
        echo "**Next:** Run \`/analyze $EXPERIMENT_NAME\`" >> "$LOGFILE"
    fi
done <<< "$NEW_FILES"

exit 0
