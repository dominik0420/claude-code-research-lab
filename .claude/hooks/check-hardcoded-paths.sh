#!/bin/bash
# Thin wrapper 鈥?actual logic lives in lab/hooks/check-hardcoded-paths.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../lab/hooks/check-hardcoded-paths.sh" "$@"
