---
name: debug-strategist
description: Systematic debugging for complex issues. Use when facing bugs that aren't immediately obvious. Follows structured process: reproduce → isolate → hypothesize → test → fix → verify. Prevents random guessing and ensures root cause is found, not just symptoms fixed.
disable-model-invocation: true
---

# Debug Strategist

Systematic debugging following scientific method.

## When to Use

- Non-obvious bugs
- Intermittent failures
- Performance issues
- Complex system interactions

## The Debugging Process

### Phase 1: REPRODUCE
**Goal:** Make the bug happen consistently

Steps:
1. Document exact steps to reproduce
2. Create minimal reproduction case
3. Identify triggering conditions
4. Determine if environment-specific

Output: `docs/debug/YYYY-MM-DD-<issue>-repro.md`

```markdown
## Bug Reproduction

**Symptom:** [what happens]
**Expected:** [what should happen]

### Steps to Reproduce
1. [step 1]
2. [step 2]
3. [step 3]

### Environment
- OS: [version]
- Runtime: [version]
- Dependencies: [versions]

### Frequency
- [ ] Always
- [ ] Sometimes (%)
- [ ] Random
```

### Phase 2: ISOLATE
**Goal:** Find smallest code surface that exhibits bug

Techniques:
- Binary search (comment out half, test, repeat)
- Comment out dependencies
- Simplify input data
- Create isolated test case

### Phase 3: HYPOTHESIZE
**Goal:** Form educated guesses about root cause

Generate 3-5 hypotheses:
```markdown
## Hypotheses

1. [Hypothesis 1] - Likelihood: High/Medium/Low
   - Evidence: [observations supporting]
   - Test: [how to verify]

2. [Hypothesis 2]...
```

### Phase 4: TEST
**Goal:** Prove/disprove hypotheses

For each hypothesis:
- Design experiment to test it
- Add logging/metrics to gather data
- Run test, collect evidence
- Document results

```markdown
## Test Results

### Hypothesis 1: [description]
**Test:** [what was tested]
**Result:** [PASS/FAIL]
**Evidence:** [logs, data]
**Conclusion:** [validated/invalidated]
```

### Phase 5: FIX
**Goal:** Correct root cause (not just symptom)

Fix criteria:
- Addresses root cause
- Minimal code change
- Doesn't break existing functionality
- Includes regression test

### Phase 6: VERIFY
**Goal:** Confirm fix works, no regressions

Checklist:
- [ ] Original bug fixed
- [ ] Reproduction case passes
- [ ] All existing tests pass
- [ ] Edge cases tested
- [ ] No new warnings/errors

## Debugging Tactics

### Binary Search Debugging
```python
# Suspect code spans lines 1-100
# Comment out lines 51-100, test
# If bug present: problem in 1-50
# If bug gone: problem in 51-100
# Repeat until isolated
```

### Rubber Duck Debugging
Explain the problem aloud/to text:
- What should happen?
- What actually happens?
- Where do they diverge?
- What have I checked?

### Logging Strategy
Add strategic logging:
- Entry/exit of suspected functions
- State changes
- API responses
- Error paths

Remove after fix.

### Divide and Conquer
Split problem into:
- Data layer issue?
- Logic issue?
- Integration issue?
- Environment issue?

Test each separately.

## Common Bug Patterns

| Pattern | Symptoms | Detection |
|---------|----------|-----------|
| Null/undefined | Crash at random point | Check all nullable paths |
| Race condition | Intermittent failure | Add delays, check ordering |
| Off-by-one | Wrong count/last item | Check loop boundaries |
| State mutation | Unexpected values | Look for shared state |
| Async/await | Missing data, hanging | Check promise handling |
| Type coercion | Wrong comparisons | Strict equality checks |

## Debug Log Template

Save to: `docs/debug/YYYY-MM-DD-<issue>.md`

```markdown
# Debug Log: [Issue Title]

## Problem
[Description]

## Reproduction
[Steps]

## Investigation
### Hypothesis 1: [X] - [result]
### Hypothesis 2: [X] - [result]

## Root Cause
[What was actually wrong]

## Fix
[What was changed]

## Verification
[How confirmed fixed]

## Prevention
[How to avoid similar bugs]
```

## Completion

Bug fixed when:
- Root cause identified and documented
- Fix implemented and verified
- Regression test added
- Debug log saved for future reference
