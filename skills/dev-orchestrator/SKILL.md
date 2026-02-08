---
name: dev-orchestrator
description: Meta skill for orchestrating software development workflows. Use when starting any multi-step development task, feature implementation, bug fix, or refactoring. Automatically selects and dispatches appropriate specialized skills based on task type and current stage. Acts as the central coordinator for plan-create-execute-review cycles.
disable-model-invocation: false
---

# Dev Orchestrator

Central coordinator for software development workflows. Routes tasks to specialized skills and manages the development lifecycle.

## When to Use

- Starting a new feature implementation
- Bug fixes requiring multi-step changes
- Refactoring projects
- Any task needing plan → execute → review cycle

## Workflow Stages

```
需求澄清 → 规划 → 执行 → 审查 → 完成
```

## Task Routing Logic

### Stage 1: Requirements Clarification
If user input is vague or incomplete:
- Ask clarifying questions
- Define success criteria
- Identify constraints and risks

### Stage 2: Planning (`plan-creator`)
For any multi-step task:
```
sessions_spawn with plan-creator skill
Input: feature requirements
Output: detailed implementation plan
```

### Stage 3: Execution (`code-executor`)
After plan approved:
```
sessions_spawn with code-executor skill  
Input: plan document
Output: implemented code + tests
```

### Stage 4: Review (`code-reviewer`)
After execution complete:
```
sessions_spawn with code-reviewer skill
Input: code changes
Output: review report with issues/suggestions
```

### Stage 5: Iteration
If review finds issues:
- Return to Stage 3 for fixes
- Or create new plan for significant changes

## Quick Reference: Skill Selection

| Task Type | Primary Skill | Secondary Skills |
|-----------|---------------|------------------|
| New feature | plan-creator → code-executor | code-reviewer |
| Bug fix | debug-strategist → code-executor | tdd-enforcer |
| Refactoring | plan-creator → code-executor | code-reviewer |
| Test addition | tdd-enforcer | code-executor |
| Code review only | code-reviewer | - |

## Usage Pattern

**User**: "帮我实现用户认证功能"

**Orchestrator Action**:
1. Clarify requirements (scope, tech stack, constraints)
2. Spawn plan-creator to create implementation plan
3. Present plan to user for approval
4. Spawn code-executor to implement
5. Spawn code-reviewer for quality check
6. Report completion status

## Coordination Protocol

### Between Sessions

Each specialized skill runs in isolated session via `sessions_spawn`:
- Clean context for each phase
- No context pollution
- Clear handoff via artifacts (plan docs, code, review reports)

### Artifact Naming

- Plans: `docs/plans/YYYY-MM-DD-<feature>.md`
- Reviews: `docs/reviews/YYYY-MM-DD-<feature>.md`
- Debug logs: `docs/debug/YYYY-MM-DD-<issue>.md`

## Principles

1. **Single Responsibility**: Each skill does one thing well
2. **Clean Handoffs**: Explicit artifacts between stages
3. **User Checkpoint**: Always get approval before next stage
4. **Fail Fast**: If plan is flawed, don't execute; revise first
