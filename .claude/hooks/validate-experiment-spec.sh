#!/bin/bash
# validate-experiment-spec.sh — PostToolUse: Write
# After writing an experiment spec to experiments/specs/, validates that
# required fields are present. Outputs warnings for any missing fields.
# Does not block — specs can be iteratively completed.

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

# Only run on experiment spec files
if ! echo "$FILE_PATH" | grep -q "experiments/specs/"; then
    exit 0
fi

CONTENT=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    print(tool_input.get('content', ''))
except:
    print('')
" 2>/dev/null)

# Required fields for a valid experiment spec
MISSING=()

check_field() {
    local field="$1"
    local pattern="$2"
    if ! echo "$CONTENT" | grep -qi "$pattern"; then
        MISSING+=("$field")
    fi
}

check_field "Hypothesis"         "hypothesis"
check_field "Primary metric"     "metric"
check_field "Dataset / task"     "dataset\|task\|benchmark"
check_field "Baseline"           "baseline\|comparison"
check_field "Done criteria"      "done\|success\|criteria\|threshold"
check_field "Compute budget"     "compute\|budget\|GPU\|hours\|cost"

if [ ${#MISSING[@]} -eq 0 ]; then
    echo "✅ Spec validated: $(basename $FILE_PATH) — all required fields present." >&2
    exit 0
fi

echo "" >&2
echo "⚠️  SPEC INCOMPLETE — $(basename $FILE_PATH)" >&2
echo "" >&2
echo "Missing fields:" >&2
for field in "${MISSING[@]}"; do
    echo "  • $field" >&2
done
echo "" >&2
echo "A complete spec is required before /implement or /team-experiments." >&2
echo "See .claude/docs/templates/experiment-spec.md for the full template." >&2
echo "" >&2

# Log the incomplete spec (project-aware path)
LOGFILE=$(ppath "research/research-log.md")
if [ -f "$LOGFILE" ]; then
    echo "" >> "$LOGFILE"
    echo "### $(date '+%Y-%m-%d %H:%M') — ⚠️ Incomplete spec: $(basename $FILE_PATH)" >> "$LOGFILE"
    echo "Missing: ${MISSING[*]}" >> "$LOGFILE"
fi

exit 0
