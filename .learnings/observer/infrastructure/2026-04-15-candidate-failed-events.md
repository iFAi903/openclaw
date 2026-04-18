# Error: Model fallback candidate_failed events

**Date:** 2026-04-15
**Type:** infrastructure anomaly
**Category:** infrastructure
**Severity:** medium
**Recurrence Count:** 25 (last 7 days)

## What Happened
Gateway recorded repeated candidate_failed fallback decisions.

## Context
- Agent: gateway
- Sessions: n/a
- Common Pattern: infrastructure-candidate-failed

## Root Cause
Fallback chain hit repeated auth, timeout, model_not_found, or overloaded states across candidates.

## Prevention
1. Trim invalid or unavailable candidates from active fallback chains.
2. Prioritize stable authenticated providers earlier in the route order.

## Status
- [x] Pending review
- [ ] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
