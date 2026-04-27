---
name: session-context-management
description: Use this skill when a task has a long or messy conversation/session history, repeated failed attempts, large context windows, Claude Code/OpenClaw coding work, debugging loops, handoffs, or when deciding whether to continue, rewind, clear, compact, or delegate to subagents. Helps prevent context rot and keep agent work reliable.
---

# Session Context Management

Core principle: bigger context is not cleaner context. Treat a large context window as buffer time, not permission to pile everything into one session.

## Context rot signals

Use this skill when any of these appear:

- The session contains multiple failed attempts or abandoned approaches.
- The model starts mixing old constraints with current instructions.
- Tool outputs, logs, or file reads dominate the conversation.
- A task shifts from exploration to implementation, or from debugging to shipping.
- The next step will produce lots of intermediate noise but only the conclusion matters.
- You are near compaction/autocompaction, or the current context feels “muddy.”

## Decision matrix

Choose the smallest reset that removes noise without losing useful state.

| Situation | Action | Why |
|---|---|---|
| Same task, current context still clean and relevant | Continue | Avoid rebuilding state unnecessarily. |
| A path failed and its intermediate steps are now harmful | Rewind / branch from earlier | Keep useful discoveries; remove failed-attempt noise. |
| Long session is still same task but cluttered | Compact with an explicit hint | Preserve task state while dropping irrelevant detail. |
| New task or major phase change | Clear / fresh session with brief | Zero context rot; inherit only chosen facts. |
| Next step creates lots of disposable intermediate output | Subagent | Parent keeps clean context; child returns only result. |

## Practical workflow

### Continue

Use when the next instruction depends directly on recent context and no major failed branch polluted the session.

### Rewind / branch

Use when a failed attempt would confuse future work.

If the platform has no literal rewind command, simulate it:

1. Identify the last clean decision point.
2. Write a short handoff: facts learned, failed approach, reason it failed, preferred next approach.
3. Start from that handoff in a fresh/branch session.

Handoff shape:

```text
Clean checkpoint:
- Goal:
- Known facts:
- Files/APIs already inspected:
- Failed approach to avoid:
- Reason it failed:
- Next approach:
```

### Compact

Use before the model becomes overloaded, not after. Always give a hint about what to keep/drop.

Good compact instruction:

```text
Compact this session for continuing the auth refactor. Keep: constraints, decisions, key files, rejected approaches and why. Drop: install logs, repeated test output, dead-end debugging details.
```

Avoid blind autocompact when the next step depends on a small detail discovered during debugging.

### Clear / fresh session

Use when the task is genuinely new or the old context is more liability than asset.

Fresh brief shape:

```text
Task:
Current state:
Important constraints:
Key files/links:
Decisions already made:
Do not repeat:
Next action:
```

### Subagent

Use when you only need the conclusion, not the intermediate trace.

Good subagent jobs:

- Read another repo and summarize the pattern to copy.
- Search logs/history for likely root causes.
- Verify a result against a spec.
- Draft docs from existing changes.
- Review code or prose and return only issues + fixes.

Ask before spawning: “Will I need the raw tool outputs later, or only the conclusion?” If only the conclusion, use a subagent.

## OpenClaw-specific defaults

- For long or noisy work, prefer `sessions_spawn` with isolated context for research/review/verification subagents.
- Use `context: "fork"` only when the child truly needs current transcript details; otherwise keep it isolated and pass a concise brief.
- After a subagent returns, preserve only the result, decisions, and blockers in the parent session.
- If a cron/heartbeat/session task times out because the prompt is too broad, rewrite it as a light-context task with explicit file scope, tool scope, output requirement, and completion phrase.

## Completion check

Before continuing a long session, ask:

1. Is the current context helping or distracting?
2. Are failed attempts still visible to the model?
3. Would a clean brief be cheaper than dragging the whole history forward?
4. Can a subagent absorb the noisy part?

If the answer suggests context rot, do not “just continue.” Reset deliberately.
