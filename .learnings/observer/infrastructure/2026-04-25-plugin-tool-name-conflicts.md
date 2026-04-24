# Error: Plugin tool name conflicts during plugin load

**Date:** 2026-04-25
**Type:** infrastructure-plugin-tool-name-conflict
**Category:** infrastructure
**Severity:** low
**Recurrence Count:** 20 (last 7 days)

## What Happened
Observed 20 matching log lines during the local-day scan window for 2026-04-25.

## Context
- Agent: observer cron
- Sessions: agent:main:cron:adfe73d9-98bd-4a6c-be04-42d153bbbfcb
- Common Pattern: 2026-04-24T16:01:18.587+08:00 [plugins] plugin tool name conflict (memory-lancedb-pro): memory_compact

## Root Cause
Multiple plugins expose overlapping tool identifiers, causing collisions during registration.

## Prevention
1. Namespace conflicting tool names or disable duplicate providers.
2. Add startup linting that fails fast on duplicate public tool names.

## Status
- [ ] Pending review
- [x] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
