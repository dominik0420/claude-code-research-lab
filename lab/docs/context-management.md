# Context Management

Research sessions involve deep technical content across many files. Context
management determines whether a session produces results or gets lost.

## File-Backed State

**The file is the memory, not the conversation.** Conversations compact or crash.
Files on disk persist. Write significant decisions to files immediately.

### Session State File

Maintain `production/session-state/active.md`:

```markdown
## Current Focus
[One sentence: what task is in progress right now]

## Progress Checklist
- [x] Completed task
- [ ] In-progress task
- [ ] Upcoming task

## Key Decisions Made This Session
- [Decision 1 and brief reason]
- [Decision 2 and brief reason]

## Files Modified This Session
- [path] — [what changed]

## Open Questions
- [Question waiting for user input]
- [Scientific uncertainty to resolve]

## Experiments Running
- [experiment name] — [status] — [expected completion]
```

Update this file after every significant milestone. After context compaction or crash, read this file first.

## Proactive Compaction

- Compact at ~60-70% context, not at the limit
- Use `/clear` between unrelated tasks (hypothesis work vs. code debugging)
- Natural compaction points: after writing a section to file, after getting experiment results, after an experiment run completes

## Context Budgets by Task Type

| Task | Context Budget | Strategy |
|------|---------------|---------|
| Literature survey | Large — reads many papers | Delegate to `literature-lead` subagent |
| Experiment design | Medium — reads spec + hypothesis | Direct in main session |
| Implementation | Large — reads many code files | Delegate to `lead-engineer` + specialists |
| Analysis | Medium — reads results data | Direct or delegate to `data-scientist` |
| Writing a section | Medium — reads outline + content | Direct in main session |
| Debugging | Potentially large | Delegate to `lead-engineer` subagent |

## Subagent Delegation for Context Efficiency

Use subagents when a task would consume >5k tokens of exploration in the main session:
- Subagents run in their own context window
- Return only summaries to the main session
- Provide full context in the subagent prompt (they don't inherit conversation history)

## Compaction Instructions

When context is compacted, preserve in summary:
- Reference to `production/session-state/active.md` (read it to recover)
- Files modified this session and their purpose
- Active experiment status (running/pending/failed)
- Current writing stage (which sections are drafted/approved/integrated)
- Any architectural decisions made and their rationale
- Unresolved blockers or questions awaiting user input
- Key scientific results observed

**After compaction**: Read `production/session-state/active.md` first.
Then read any actively-worked files listed in it.

## Incremental Document Writing

For long documents (proposal, paper sections):
1. Create file with skeleton (all section headers, empty bodies) immediately
2. Discuss and draft one section at a time
3. Write each section to file as soon as approved
4. After writing, previous discussion can be safely compacted

This keeps the active context to ~3-5k tokens instead of the entire document's discussion.

## Recovery After Crash

1. `production/session-state/active.md` shows the recovery point
2. Read it immediately at session start
3. Read the partially-completed file(s) listed in it
4. Continue from the next incomplete section or task

## Research-Specific Context Tips

- **Hypothesis is the anchor**: Always have `research/hypothesis.md` read at the start of any experiment or analysis session
- **Results are not small**: `experiments/results/` can be large — use the analysis agents rather than reading raw results directly
- **Literature survey grows**: Once `literature/survey.md` is long, delegate literature work to `literature-lead` rather than reading the whole survey in main context
