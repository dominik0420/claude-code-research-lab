#!/bin/bash
# validate-experiment-command.sh — PreToolUse: Bash
# Before running a Python experiment command, validates that:
# 1. A config file is passed (not hardcoded args)
# 2. An output directory is specified
# 3. The script file actually exists
# Does NOT block — exits 0 after warnings.

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

# Only check Python experiment commands
if ! echo "$COMMAND" | grep -qE "(python|python3).*(train|run|experiment|main)"; then
    exit 0
fi

ISSUES=()

# Check for config file argument
if ! echo "$COMMAND" | grep -qE "\-\-config|\-c |\.yaml|\.yml|\.json"; then
    ISSUES+=("No config file passed — hyperparameters should come from a config, not CLI args")
fi

# Check for output directory
if ! echo "$COMMAND" | grep -qE "\-\-output|\-\-out|\-\-save|\-\-results|output_dir|save_dir"; then
    ISSUES+=("No output directory specified — where will results be saved?")
fi

# Check if the Python script exists
SCRIPT=$(echo "$COMMAND" | python3 -c "
import sys, shlex
tokens = shlex.split(sys.stdin.read())
for i, t in enumerate(tokens):
    if t in ('python', 'python3') and i+1 < len(tokens):
        print(tokens[i+1])
        break
" 2>/dev/null)

if [ -n "$SCRIPT" ] && ! echo "$SCRIPT" | grep -qE "^-" && [ ! -f "$SCRIPT" ]; then
    ISSUES+=("Script not found: $SCRIPT")
fi

if [ ${#ISSUES[@]} -eq 0 ]; then
    exit 0
fi

echo "" >&2
echo "⚠️  EXPERIMENT COMMAND WARNINGS" >&2
echo "" >&2
echo "Command: $COMMAND" >&2
echo "" >&2
for issue in "${ISSUES[@]}"; do
    echo "  • $issue" >&2
done
echo "" >&2
echo "Proceeding — fix warnings before final results are reported." >&2
echo "" >&2

exit 0
