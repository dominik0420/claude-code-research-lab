#!/bin/bash
# experiment-complete-notify.sh — PostToolUse: Write
# Fires when a new results file appears in experiments/results/.
# Prints a summary prompt so the researcher knows to run /analyze.

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

if ! echo "$FILE_PATH" | grep -q "experiments/results/"; then
    exit 0
fi

EXPERIMENT_NAME=$(basename "$FILE_PATH" .json)
EXPERIMENT_NAME=$(basename "$EXPERIMENT_NAME" .csv)
EXPERIMENT_NAME=$(basename "$EXPERIMENT_NAME" .txt)

echo "" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
echo "  🧪 Experiment results written: $EXPERIMENT_NAME" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
echo "" >&2
echo "  Next steps:" >&2
echo "  → /analyze $EXPERIMENT_NAME   — interpret results" >&2
echo "  → /stat-test $EXPERIMENT_NAME — run significance tests" >&2
echo "  → /failure-analysis $EXPERIMENT_NAME — examine error cases" >&2
echo "" >&2

# Log results creation
LOGFILE="research/research-log.md"
if [ -f "$LOGFILE" ]; then
    echo "" >> "$LOGFILE"
    echo "### $(date '+%Y-%m-%d %H:%M') — Results written: $EXPERIMENT_NAME" >> "$LOGFILE"
    echo "**File:** \`$FILE_PATH\`" >> "$LOGFILE"
    echo "**Next:** Run \`/analyze $EXPERIMENT_NAME\`" >> "$LOGFILE"
fi

exit 0
