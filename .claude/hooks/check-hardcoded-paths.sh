#!/bin/bash
# check-hardcoded-paths.sh — PostToolUse: Write
# Scans Python files written to src/ for hardcoded paths, hardcoded
# hyperparameters, and missing random seeds. These are the most common
# reproducibility failures in research code.

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

CONTENT=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    print(tool_input.get('content', ''))
except:
    print('')
" 2>/dev/null)

# Only scan Python files in src/
if ! echo "$FILE_PATH" | grep -qE "src/.*\.py$"; then
    exit 0
fi

ISSUES=()

# Check for hardcoded absolute paths
if echo "$CONTENT" | grep -qE '"/home/|"/Users/|"/data/|"C:\\\\|"/mnt/'; then
    ISSUES+=("Hardcoded absolute path detected")
fi

# Check for hardcoded learning rate (a float where 'lr' or 'learning_rate' isn't from config)
if echo "$CONTENT" | grep -qE "learning_rate\s*=\s*[0-9]|lr\s*=\s*[0-9]"; then
    ISSUES+=("Hardcoded learning rate (should come from config)")
fi

# Check for hardcoded batch size
if echo "$CONTENT" | grep -qE "batch_size\s*=\s*[0-9]"; then
    ISSUES+=("Hardcoded batch_size (should come from config)")
fi

# Check for hardcoded epochs
if echo "$CONTENT" | grep -qE "num_epochs\s*=\s*[0-9]|epochs\s*=\s*[0-9]"; then
    ISSUES+=("Hardcoded num_epochs (should come from config)")
fi

# Check for missing seed setting (only warn for training scripts)
if echo "$FILE_PATH" | grep -qE "train|trainer|run"; then
    if ! echo "$CONTENT" | grep -qE "seed|random\.seed|torch\.manual_seed|np\.random\.seed|set_seed"; then
        ISSUES+=("No random seed set — results won't be reproducible")
    fi
fi

# Check for hardcoded device (should use config or auto-detect)
if echo "$CONTENT" | grep -qE '"cuda:0"|"cuda:1"|"cpu"'; then
    ISSUES+=("Hardcoded device string (use torch.device or config)")
fi

if [ ${#ISSUES[@]} -eq 0 ]; then
    exit 0
fi

echo "" >&2
echo "⚠️  REPRODUCIBILITY WARNINGS — $(basename $FILE_PATH)" >&2
echo "" >&2
for issue in "${ISSUES[@]}"; do
    echo "  • $issue" >&2
done
echo "" >&2
echo "See .claude/rules/code.md for the full coding standards." >&2
echo "" >&2

exit 0
