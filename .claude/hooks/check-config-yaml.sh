#!/bin/bash
# check-config-yaml.sh — PostToolUse: Write
# Validates YAML experiment config files written to experiments/configs/.
# Checks for required fields: seed, output_dir, and at least one
# model or training parameter.

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

# Only check YAML files in experiments/configs/
if ! echo "$FILE_PATH" | grep -qE "experiments/configs/.*\.(yaml|yml)$"; then
    exit 0
fi

ISSUES=()

# Validate using Python for proper YAML parsing
VALIDATION=$(echo "$CONTENT" | python3 -c "
import sys

content = sys.stdin.read()

# Try to parse as YAML (gracefully handle missing pyyaml)
try:
    import yaml
    try:
        config = yaml.safe_load(content)
        if not isinstance(config, dict):
            print('NOT_DICT')
            sys.exit(0)
    except yaml.YAMLError as e:
        print(f'YAML_ERROR: {e}')
        sys.exit(0)

    issues = []

    if 'seed' not in config:
        issues.append('Missing: seed (required for reproducibility)')

    if 'output_dir' not in config and 'save_dir' not in config and 'results_dir' not in config:
        issues.append('Missing: output_dir (where should results be saved?)')

    # Check for at least one training or model parameter
    param_keys = {'learning_rate', 'lr', 'batch_size', 'model', 'architecture',
                  'hidden_size', 'num_layers', 'dropout', 'optimizer', 'epochs',
                  'num_epochs', 'max_steps'}
    if not any(k in config for k in param_keys):
        issues.append('No model or training parameters found')

    for issue in issues:
        print(f'ISSUE: {issue}')

except ImportError:
    # No pyyaml — do basic text checks
    if 'seed' not in content:
        print('ISSUE: Missing: seed (required for reproducibility)')
    if 'output_dir' not in content and 'save_dir' not in content:
        print('ISSUE: Missing: output_dir')
" 2>/dev/null)

if echo "$VALIDATION" | grep -q "YAML_ERROR"; then
    echo "" >&2
    echo "❌ INVALID YAML — $(basename $FILE_PATH)" >&2
    echo "$VALIDATION" | grep "YAML_ERROR" | sed 's/YAML_ERROR: /   /' >&2
    echo "" >&2
    exit 0
fi

ISSUE_LINES=$(echo "$VALIDATION" | grep "^ISSUE:")
if [ -z "$ISSUE_LINES" ]; then
    echo "✅ Config valid: $(basename $FILE_PATH)" >&2
    exit 0
fi

echo "" >&2
echo "⚠️  CONFIG WARNINGS — $(basename $FILE_PATH)" >&2
echo "" >&2
echo "$ISSUE_LINES" | sed 's/^ISSUE: /  • /' >&2
echo "" >&2

exit 0
