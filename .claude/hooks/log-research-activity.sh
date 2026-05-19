#!/bin/bash
# Thin wrapper 鈥?actual logic lives in lab/hooks/log-research-activity.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../lab/hooks/log-research-activity.sh" "$@"
