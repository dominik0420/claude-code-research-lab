#!/bin/bash
# Thin wrapper 鈥?actual logic lives in lab/hooks/guard-eval-protocol.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../lab/hooks/guard-eval-protocol.sh" "$@"
