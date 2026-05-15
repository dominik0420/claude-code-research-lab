#!/bin/bash
# This script is no longer needed.
# Setup is now: mv lab .claude
# See README.md for the full setup instructions.
echo "See README.md -- setup is now: mv lab .claude"
exit 0
# ---- old content below, kept for reference ----

set -e

echo "============================================"
echo " Claude Code Research Lab — Install"
echo "============================================"
echo ""

# Create .claude directory structure
echo "Setting up .claude/ structure..."
mkdir -p .claude/agents
mkdir -p .claude/commands
mkdir -p .claude/docs/templates
mkdir -p .claude/rules

# Copy lab configuration
echo "Copying agents..."
cp lab/agents/*.md .claude/agents/

echo "Copying commands..."
cp lab/commands/*.md .claude/commands/

echo "Copying docs..."
cp lab/docs/*.md .claude/docs/
cp lab/docs/templates/*.md .claude/docs/templates/

echo "Copying rules..."
cp lab/rules/*.md .claude/rules/

echo ""
echo "Creating project directory structure..."

# Research documents
mkdir -p research
mkdir -p literature/papers

# Experiments
mkdir -p experiments/specs
mkdir -p experiments/configs
mkdir -p experiments/results

# Source code
mkdir -p src/models
mkdir -p src/data
mkdir -p src/training
mkdir -p src/evaluation
mkdir -p src/utils

# Scripts
mkdir -p scripts

# Tests
mkdir -p tests

# Data
mkdir -p data/raw
mkdir -p data/processed

# Baselines
mkdir -p baselines

# Analysis
mkdir -p analysis/outputs/figures
mkdir -p analysis/figures

# Papers
mkdir -p papers/drafts

# Production
mkdir -p production/milestones
mkdir -p production/sprints
mkdir -p production/session-state

echo ""
echo "Creating starter files..."

# research-log.md
if [ ! -f research/research-log.md ]; then
cat > research/research-log.md << 'EOF'
# Research Log

All significant decisions and pivots are logged here.
Use the template in .claude/docs/templates/research-log-entry.md

---
EOF
fi

# session state
if [ ! -f production/session-state/active.md ]; then
cat > production/session-state/active.md << 'EOF'
## Current Focus
New project — run /start to begin.
EOF
fi

# .gitignore
if [ ! -f .gitignore ]; then
cat > .gitignore << 'EOF'
# Large data files
data/raw/
data/processed/
experiments/results/

# Session state
production/session-state/

# Generated outputs (regenerated from scripts)
analysis/outputs/

# Python
__pycache__/
*.egg-info/
*.pyc
.env
venv/
env/

# Jupyter
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db
EOF
echo "Created .gitignore"
fi

echo ""
echo "============================================"
echo " Installation complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Open this folder in Claude Code: claude (from this directory)"
echo "  2. Run /start to begin your research project"
echo "  3. See .claude/docs/quick-start.md for the full guide"
echo ""
