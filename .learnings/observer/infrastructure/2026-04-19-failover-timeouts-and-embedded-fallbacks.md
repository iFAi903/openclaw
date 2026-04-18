# Error: Failover timeouts and embedded fallback churn

**Date:** 2026-04-19
**Type:** failover_timed_out / embedded_run_failover
**Category:** infrastructure
**Severity:** high
**Recurrence Count:** 17+ (observed this cycle)

## What Happened
Gateway logs showed repeated embedded runner timeouts and fallback decisions, especially on local qwen3.6 and gemma4 models. Several incidents clustered between 20:16 and 23:51 +08:00, including slug-generator failures.

## Context
- Agent: multiple agents and cron jobs
- Sessions: slug-generator temp sessions, cron sessions, subagent sessions
- Common Pattern: local model timeout or model load failure followed by fallback

## Root Cause
The local model layer appears unstable under load, producing timeout and HTTP 500 model-load failures that force repeated failover.

## Prevention
1. Reduce reliance on unstable local default candidates for latency-sensitive embedded tasks.
2. Review local model capacity and timeout thresholds before continuing to route slug generation and cron work through them.

## Status
- [x] Pending review
- [x] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
