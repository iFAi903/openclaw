# Error: Gateway slow request bursts

**Date:** 2026-04-19
**Type:** slow_request
**Category:** infrastructure
**Severity:** medium
**Recurrence Count:** 10 (observed this cycle)

## What Happened
Gateway logs contained several requests above 2000ms, including multiple 120000ms timeout warnings and agent.wait calls above 400 seconds.

## Context
- Agent: subagent completion announce path and gateway status checks
- Sessions: multiple concurrent sessions
- Common Pattern: long waits and repeated announce retries during busy periods

## Root Cause
The gateway appears to degrade under concurrent workload, especially during subagent completion announcements and long-lived waits.

## Prevention
1. Inspect announcement retry path and websocket wait behavior during peak concurrency.
2. Prioritize a lighter completion path or backoff strategy before increasing traffic further.

## Status
- [x] Pending review
- [x] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
