# Error: Escaped skill path skips during skill discovery

**Date:** 2026-04-25
**Type:** infrastructure-skipping-skill-path
**Category:** infrastructure
**Severity:** low
**Recurrence Count:** 150 (last 7 days)

## What Happened
Observed 150 matching log lines during the local-day scan window for 2026-04-25.

## Context
- Agent: observer cron
- Sessions: agent:main:cron:adfe73d9-98bd-4a6c-be04-42d153bbbfcb
- Common Pattern: 2026-04-24T16:10:13.973+08:00 [skills] Skipping escaped skill path outside its configured root: source=openclaw-managed root=~/.openclaw/skills reason=symlink-escape requested=~/.openclaw/skills/lark-base resolved=~/.agents/skills/lark-base

## Root Cause
Managed skill roots still reference symlinked paths that resolve outside ~/.openclaw/skills, so the loader skips them as escapes.

## Prevention
1. Normalize skill registration to canonical realpaths before validation.
2. Audit symlink-based managed skills and relocate or re-register them under allowed roots.

## Status
- [ ] Pending review
- [x] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
