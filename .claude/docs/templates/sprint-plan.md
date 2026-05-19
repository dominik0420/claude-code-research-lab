# Sprint Plan Template

Used by `/sprint-plan`. One file per sprint in `production/sprints/`.

---

# Sprint [N]: [Sprint Goal]

**Dates**: [YYYY-MM-DD] to [YYYY-MM-DD]
**Goal**: [One sentence — what does this sprint achieve?]
**Submission Deadline**: [T-X days from sprint end]

---

## Tasks

| ID | Description | Owner Agent | Estimate | Depends On | Done When | Status |
|----|-------------|------------|---------|------------|-----------|--------|
| S[N]-001 | [Task] | [agent] | [Xh] | [] | [Observable condition] | pending |
| S[N]-002 | [Task] | [agent] | [Xh] | [S[N]-001] | [Observable condition] | pending |
| S[N]-003 | [Task] | [agent] | [Xh] | [] | [Observable condition] | pending |

**Task sizing rules**:
- Each task completable in 1–3 days by the owning agent
- "Done when" must be observable without judgment (a file exists, a test passes, etc.)
- Dependencies listed explicitly — no implicit ordering

---

## Critical Path

The tasks that, if delayed, delay the sprint end:
1. [Critical task 1] → [Critical task 2] → [Sprint deliverable]

**Buffer**: ~[N] hours for unexpected issues (always reserve ≥20% of capacity)

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | [High/Med/Low] | [High/Med/Low] | [What we do if it happens] |
| [Risk 2] | | | |

**Escalation triggers**:
- If [critical task] slips by >2 days → escalate to PI to reprioritize
- If [blocker] is not resolved by [date] → escalate to research-director

---

## Capacity

| Agent | Hours Available | Assigned Tasks | Hours Assigned |
|-------|---------------|---------------|---------------|
| [agent] | [N]h | [S[N]-00X, ...] | [N]h |

**Sprint velocity** (from last sprint): [N hours of tasks completed]

---

## Notes

[Any additional context for this sprint — what we learned from the previous sprint,
any external dependencies (compute allocation, collaborator review), any scope changes.]

---

## End-of-Sprint Criteria

This sprint is DONE when:
- [ ] All tasks in "done" status
- [ ] Sprint deliverable exists at [path]
- [ ] Next sprint's first task is unblocked
- [ ] Sprint retrospective logged in `production/retrospectives/sprint-[N].md`
