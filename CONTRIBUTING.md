# Contributing to Claude Code Research Lab

Thank you for your interest in improving this project.

## What This Repo Is

This is a Claude Code agent architecture — a collection of agent definitions
(`.claude/agents/`), slash commands (`.claude/commands/`), documentation
(`.claude/docs/`), and path rules (`.claude/rules/`) that turn a Claude Code
session into a structured research lab.

## Ways to Contribute

### Adding or Improving Agents

Agent files live in `.claude/agents/`. Each file is a Markdown document with
YAML frontmatter specifying the agent's name, model tier, tools, and behavior.

Guidelines:
- One agent per file, named `role-name.md` in kebab-case
- Keep the agent's domain narrow — no agent should do everything
- Include a delegation map showing what the agent hands off to others
- Include gate verdicts if the agent is a quality gate (first line: APPROVE/REJECT)
- Specify the minimum necessary tool set in frontmatter

### Adding or Improving Commands

Command files live in `.claude/commands/`. These become slash commands in
Claude Code (e.g., `start.md` → `/start`).

Guidelines:
- Commands should be user-invocable workflows, not implementation details
- Use `AskUserQuestion` before starting any multi-step work
- Show drafts and ask "May I write this to [filepath]?" before saving
- Include output format requirements and line limits

### Track Additions

The lab currently supports two tracks: ML and Social Science. If you're adding
a track (e.g., computational biology, legal research):

1. Add track detection to `start.md` decision tree
2. Create the track-specific commands
3. Update `CLAUDE.md` with new paradigm/stack fields
4. Update both READMEs

### Documentation

Docs live in `.claude/docs/`. Templates live in `.claude/docs/templates/`.
Keep docs concise — agents read them at runtime and context is precious.

## Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b add-my-feature`
3. Make your changes in `.claude/`
4. Test by opening the folder in Claude Code and running the affected commands
5. Submit a pull request with a clear description of what changed and why

## Code of Conduct

Be constructive. Research is hard enough without bad-faith contributions.
