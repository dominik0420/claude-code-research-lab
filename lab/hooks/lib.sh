#!/bin/bash
# lib.sh — shared utilities for Claude Code Research Lab hooks
# Source at the top of each hook:
#   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   source "$SCRIPT_DIR/lib.sh"

# Returns the active project directory from CLAUDE.md, or empty string.
# When non-empty, all project output paths are rooted here.
get_project_dir() {
    if [ -f "CLAUDE.md" ]; then
        local raw
        raw=$(grep -m1 "Active Project:" CLAUDE.md 2>/dev/null \
              | sed 's/.*Active Project:[[:space:]]*//' \
              | sed 's/[[:space:]]*$//' \
              | tr -d '[]')
        # Ignore unset placeholders
        if [ -n "$raw" ] && ! echo "$raw" | grep -qi "CHOOSE\|project-name"; then
            echo "$raw"
        fi
    fi
}

# Return a path prefixed with the active project dir, if one is set.
# Usage: ppath "research/hypothesis.md"
ppath() {
    local rel="$1"
    local pdir
    pdir=$(get_project_dir)
    if [ -n "$pdir" ]; then
        echo "${pdir}/${rel}"
    else
        echo "${rel}"
    fi
}

# Create parent directories for a path (project-aware mkdir -p).
# Usage: pmkdir "research/hypothesis.md"
pmkdir() {
    mkdir -p "$(dirname "$(ppath "$1")")"
}
