# Error: Embedded run failover decisions

**Date:** 2026-04-15
**Type:** infrastructure anomaly
**Category:** infrastructure
**Severity:** medium
**Recurrence Count:** 9 (last 7 days)

## What Happened
Embedded agent runs triggered multiple fallback_model decisions.

## Context
- Agent: gateway
- Sessions: n/a
- Common Pattern: infrastructure-embedded-run-failover

## Root Cause
Embedded runs encountered upstream failures and repeatedly switched models.

## Prevention
1. Audit embedded-run model defaults for invalid or weak candidates.
2. Reduce repeated retries when the same failure reason recurs in a short window.

## Status
- [x] Pending review
- [ ] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
