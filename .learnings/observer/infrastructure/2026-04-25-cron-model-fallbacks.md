# Error: Cron requested disallowed models and fell back to agent defaults

**Date:** 2026-04-25
**Type:** infrastructure-model-not-allowed-fallback
**Category:** infrastructure
**Severity:** medium
**Recurrence Count:** 4 (last 7 days)

## What Happened
Observed 4 matching log lines during the local-day scan window for 2026-04-25.

## Context
- Agent: observer cron
- Sessions: agent:main:cron:adfe73d9-98bd-4a6c-be04-42d153bbbfcb
- Common Pattern: 2026-04-24T16:01:16.362+08:00 [cron] payload.model 'google/gemma-4-31b-it' not allowed, falling back to agent defaults

## Root Cause
Some cron specs reference models outside the current allowlist, so scheduled runs silently shift to defaults.

## Prevention
1. Align cron frontmatter model values with the active provider allowlist.
2. Add validation at cron-save time so invalid model IDs are rejected before schedule execution.

## Status
- [ ] Pending review
- [x] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
