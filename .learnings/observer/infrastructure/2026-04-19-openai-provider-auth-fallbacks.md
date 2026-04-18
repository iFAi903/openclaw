# Error: OpenAI provider auth fallback loop

**Date:** 2026-04-19
**Type:** candidate_failed
**Category:** infrastructure
**Severity:** medium
**Recurrence Count:** 80 (observed this cycle)

## What Happened
Gateway logs showed frequent candidate_failed entries where openai/gpt-5.4 or openai/gpt-5.4-nano was requested without an API key, then fell back to another model.

## Context
- Agent: multiple sessions
- Sessions: main and Feishu-linked sessions
- Common Pattern: requested openai/* route without OPENAI_API_KEY, despite Codex OAuth being available on openai-codex/*

## Root Cause
Model routing is requesting provider names that require API-key auth, while the environment is configured for Codex OAuth routes instead.

## Prevention
1. Replace openai/gpt-5.4* routes with openai-codex/gpt-5.4 where OAuth is intended.
2. Keep API-key-only models out of default fallback chains unless credentials are actually configured.

## Status
- [x] Pending review
- [x] Suggested (see iteration plan)
- [ ] Executed
- [ ] Promoted
