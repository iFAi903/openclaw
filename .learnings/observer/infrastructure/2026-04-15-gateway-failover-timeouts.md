# Error: Gateway failover timeouts

**Date:** 2026-04-15
**Type:** infrastructure anomaly
**Category:** infrastructure
**Severity:** high
**Recurrence Count:** 2 (last 7 days)

## What Happened
Gateway logged FailoverError timeout events in gateway.err.log.

## Context
- Agent: gateway
- Sessions: n/a
- Common Pattern: infrastructure-failover-timeout

## Root Cause
Provider/network instability caused failover timeouts during model execution.

## Prevention
1. Review provider/network reliability around the failure window.
2. Add guardrails to reduce cascading timeout retries during degraded periods.

## Status
- [x] Pending review
- [ ] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
