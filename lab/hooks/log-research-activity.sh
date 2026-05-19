#!/bin/bash
# log-research-activity.sh — PostToolUse: Write
# Auto-appends a timestamped entry to research/research-log.md whenever
# a significant research file is written. Keeps the log current without
# requiring the researcher to remember to write to it manually.

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

# Only log significant research files — not every write
SIGNIFICANT=false
for pattern in \
    "research/hypothesis" \
    "research/proposal" \
    "research/study-design" \
    "experiments/specs/" \
    "experiments/eval-protocol" \
    "papers/outline" \
    "papers/drafts/" \
    "literature/gap-analysis" \
    "literature/survey" \
    "research/instruments/"
do
    if echo "$FILE_PATH" | grep -q "$pattern"; then
        SIGNIFICANT=true
        break
    fi
done

if [ "$SIGNIFICANT" = false ]; then
    exit 0
fi

LOGFILE=$(ppath "research/research-log.md")

# Create log file if it doesn't exist
if [ ! -f "$LOGFILE" ]; then
    pmkdir "research/research-log.md"
    echo "# Research Log" > "$LOGFILE"
    echo "" >> "$LOGFILE"
    echo "All significant file writes are logged here automatically." >> "$LOGFILE"
    echo "Add notes manually after each entry to record the reasoning." >> "$LOGFILE"
    echo "" >> "$LOGFILE"
    echo "---" >> "$LOGFILE"
fi

# Get a brief description from the file content
PREVIEW=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    content = tool_input.get('content', '')
    # Get first non-empty, non-comment line
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('<!--') and not line.startswith('---'):
            print(line[:120])
            break
except:
    print('')
" 2>/dev/null)

# Determine a human-readable event label
if echo "$FILE_PATH" | grep -q "hypothesis"; then
    LABEL="Hypothesis written"
elif echo "$FILE_PATH" | grep -q "proposal"; then
    LABEL="Research proposal written"
elif echo "$FILE_PATH" | grep -q "study-design"; then
    LABEL="Study design written"
elif echo "$FILE_PATH" | grep -q "eval-protocol"; then
    LABEL="Evaluation protocol written"
elif echo "$FILE_PATH" | grep -q "specs/"; then
    SPECNAME=$(basename "$FILE_PATH" .md)
    LABEL="Experiment spec written: $SPECNAME"
elif echo "$FILE_PATH" | grep -q "outline"; then
    LABEL="Paper outline written"
elif echo "$FILE_PATH" | grep -q "drafts/"; then
    SECTION=$(basename "$FILE_PATH" .md)
    LABEL="Paper section drafted: $SECTION"
elif echo "$FILE_PATH" | grep -q "gap-analysis"; then
    LABEL="Gap analysis written"
elif echo "$FILE_PATH" | grep -q "instruments/"; then
    LABEL="Research instrument written: $(basename $FILE_PATH)"
else
    LABEL="File written: $(basename $FILE_PATH)"
fi

# Append to log
echo "" >> "$LOGFILE"
echo "### $(date '+%Y-%m-%d %H:%M') — $LABEL" >> "$LOGFILE"
echo "**File:** \`$FILE_PATH\`" >> "$LOGFILE"
if [ -n "$PREVIEW" ]; then
    echo "**Preview:** $PREVIEW" >> "$LOGFILE"
fi
echo "**Notes:** *(add reasoning here)*" >> "$LOGFILE"

exit 0
