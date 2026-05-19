#!/bin/bash
# Thin wrapper 鈥?actual logic lives in lab/hooks/capture-git-hash.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../lab/hooks/capture-git-hash.sh" "$@"
