---
name: code-executor
description: Executes implementation plans created by plan-creator. Use when you have an approved plan document and need to implement the tasks. Works through each task systematically: writes tests first (RED), makes them pass (GREEN), refactors (optional), commits. Reports progress and blockers. Stops on critical issues for human review.
disable-model-invocation: true
---

# Code Executor

Executes implementation plans following strict TDD cycle.

## When to Use

- Plan document approved and ready
- Task-by-task implementation needed
- RED-GREEN-REFACTOR cycle required

## Input

Read plan from: `docs/plans/YYYY-MM-DD-<feature>.md`

## Execution Workflow

For each task in plan:

### 1. Read Task Specification
```markdown
Task N: [Name]
Files: [create/modify/test paths]
Steps: [detailed steps]
```

### 2. Execute RED Phase
- Write failing test exactly as specified
- Run test, confirm it fails with expected error
- If test passes unexpectedly → STOP, review plan

### 3. Execute GREEN Phase  
- Write minimal code to pass test
- No refactoring yet, just make it work
- Run test, confirm it passes

### 4. Execute REFACTOR Phase (Optional)
- Improve code quality while keeping tests green
- Run tests after each change

### 5. Commit
```bash
git add <files>
git commit -m "<type>: <description>"
```

### 6. Report Progress
```
Completed Task N: [Name]
- Files changed: [list]
- Tests: [pass/fail count]
- Commits: [hash]
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Test fails unexpectedly | STOP, report to user with error |
| Plan step unclear | STOP, ask for clarification |
| File doesn't exist | Check if should create, then proceed or stop |
| Test passes before code | STOP, review test validity |
| Refactor breaks tests | Revert, try smaller steps |

## Anti-Patterns to Avoid

- ❌ Writing implementation before test
- ❌ Writing multiple tests at once
- ❌ Big bang commits
- ❌ Skipping verification steps
- ❌ "I'll fix it later" without test

## Progress Tracking

Maintain running status:
```markdown
## Execution Status

- [x] Task 1: User model (5 min)
- [x] Task 2: Auth service (8 min)  
- [ ] Task 3: Login endpoint (in progress)
- [ ] Task 4: Tests pending
```

## Completion Report

When all tasks complete:
```
✅ Plan execution complete

Summary:
- Tasks completed: N
- Files created: [list]
- Files modified: [list]  
- Tests added: [count]
- Commits: [count]
- Time elapsed: [duration]

Next: Run code-reviewer for quality check
```
