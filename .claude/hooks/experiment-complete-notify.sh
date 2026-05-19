#!/bin/bash
# Thin wrapper 鈥?actual logic lives in lab/hooks/experiment-complete-notify.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../lab/hooks/experiment-complete-notify.sh" "$@"
