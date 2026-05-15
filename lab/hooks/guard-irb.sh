#!/bin/bash
# guard-irb.sh — PreToolUse: Write
# Warns before writing to data collection paths if no IRB protocol exists.
# Social Science Track only — silently passes for ML-only projects.
# Does NOT block — IRB timing varies by institution. Warns and logs.

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

# Only trigger for data collection related paths
if ! echo "$FILE_PATH" | grep -qE "(data/raw|data/processed|research/instruments|research/study-design|participants)"; then
    exit 0
fi

# Check if this is a social science project
CLAUDE_MD="CLAUDE.md"
if [ -f "$CLAUDE_MD" ]; then
    if ! grep -qi "social science\|sociology\|psychology\|survey\|interview\|qualitative\|quantitative" "$CLAUDE_MD"; then
        exit 0
    fi
fi

# Check if IRB protocol exists
IRB_PROTOCOL="research/irb-protocol.md"

if [ ! -f "$IRB_PROTOCOL" ]; then
    echo "" >&2
    echo "⚠️  WARNING — No IRB protocol found" >&2
    echo "" >&2
    echo "You are writing to a data collection path: $FILE_PATH" >&2
    echo "" >&2
    echo "Data collected without IRB / ethics board approval:" >&2
    echo "  • May be rejected by journals and conferences" >&2
    echo "  • Cannot be used in publications at most institutions" >&2
    echo "  • May violate your institution's research policies" >&2
    echo "" >&2
    echo "Run /irb-protocol to generate the ethics board submission." >&2
    echo "Proceeding — but this warning is logged." >&2
    echo "" >&2

    LOGFILE="research/research-log.md"
    if [ -f "$LOGFILE" ]; then
        echo "" >> "$LOGFILE"
        echo "## ⚠️ WARNING $(date '+%Y-%m-%d %H:%M') — Data write without IRB protocol" >> "$LOGFILE"
        echo "Path: \`$FILE_PATH\`" >> "$LOGFILE"
        echo "Action required: Run /irb-protocol before data collection." >> "$LOGFILE"
    fi
fi

exit 0
