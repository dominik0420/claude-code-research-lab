#!/bin/bash
# guard-results.sh — PreToolUse: Write | Edit
# Blocks any write or edit to experiments/results/
# Enforces the core research integrity rule: results are immutable.
#
# To fix a wrong result: re-run the experiment with a corrected config.
# Never edit results directly — the paper must be traceable to real runs.

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    path = tool_input.get('file_path', '') or tool_input.get('path', '')
    print(path)
except:
    print('')
" 2>/dev/null)

if echo "$FILE_PATH" | grep -qE "experiments/results/"; then
    echo "" >&2
    echo "╔══════════════════════════════════════════════════════════╗" >&2
    echo "║  BLOCKED — experiments/results/ is immutable             ║" >&2
    echo "╚══════════════════════════════════════════════════════════╝" >&2
    echo "" >&2
    echo "File:    $FILE_PATH" >&2
    echo "Reason:  Results files cannot be edited after creation." >&2
    echo "         Every number in the paper must trace to a real run." >&2
    echo "" >&2
    echo "Fix:     Re-run the experiment with a corrected config file." >&2
    echo "         New run → new results file. Never patch the old one." >&2
    echo "" >&2
    exit 1
fi

exit 0
