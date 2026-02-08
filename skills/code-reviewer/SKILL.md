---
name: code-reviewer
description: Comprehensive code review focusing on quality, security, performance, and maintainability. Use after code implementation is complete. Checks for correctness, security vulnerabilities, performance issues, SOLID principles, test coverage, and documentation. Provides actionable feedback with severity levels (critical/blocking, warning, suggestion).
disable-model-invocation: true
---

# Code Reviewer

Systematic code quality assessment with actionable feedback.

## When to Use

- After code execution completes
- Pre-commit/PR review
- Quality gate before deployment

## Input

Git diff, PR changes, or file list to review.

## Review Checklist

### 1. Correctness
- [ ] Logic errors
- [ ] Edge cases handled
- [ ] Error handling paths
- [ ] Race conditions
- [ ] Resource leaks

### 2. Security
- [ ] Input validation
- [ ] Injection vulnerabilities (SQL, XSS, command)
- [ ] Authentication/authorization
- [ ] Sensitive data exposure
- [ ] Dependencies vulnerabilities

### 3. Performance
- [ ] Algorithm efficiency
- [ ] Database query optimization
- [ ] Memory usage
- [ ] Unnecessary I/O
- [ ] Caching opportunities

### 4. Maintainability
- [ ] SOLID principles
- [ ] DRY compliance
- [ ] Naming conventions
- [ ] Function complexity (< 10)
- [ ] Code duplication

### 5. Testing
- [ ] Test coverage > 80%
- [ ] Edge cases tested
- [ ] Test quality (not just coverage)
- [ ] Mock usage appropriate

### 6. Documentation
- [ ] Function docstrings
- [ ] Complex logic explained
- [ ] API documentation
- [ ] README updated

## Review Output Format

Save to: `docs/reviews/YYYY-MM-DD-<feature>.md`

```markdown
# Code Review: [Feature Name]

**Reviewed:** [date]
**Files:** [count]
**Lines changed:** [+x, -y]

## Summary
- Critical: [count]
- Warnings: [count]  
- Suggestions: [count]
- Quality Score: [x/100]

## Critical Issues (Blocking)

### [File:Line] - [Issue Title]
**Problem:** [description]
**Risk:** [security/performance/correctness impact]
**Fix:** [specific recommendation]
```diff
- bad code
+ good code
```

## Warnings

### [File:Line] - [Issue Title]
**Issue:** [description]
**Recommendation:** [how to improve]

## Suggestions

### [File:Line] - [Suggestion]
[Description of improvement opportunity]

## Positive Findings

- [What was done well]
- [Good patterns observed]

## Action Items

- [ ] Fix critical issue #1
- [ ] Fix critical issue #2
- [ ] Consider warning #1
- [ ] Update documentation

## Approval Status

- [ ] Approved - no critical issues
- [ ] Conditionally approved - fix critical issues
- [ ] Changes requested - significant issues found
```

## Severity Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **Critical** | Security vuln, data loss, crash | Must fix before merge |
| **Warning** | Maintainability, performance | Should fix, can defer |
| **Suggestion** | Style, optimization | Nice to have |

## Review Process

1. **Scan** - Quick pass for obvious issues
2. **Deep dive** - Line-by-line analysis
3. **Test check** - Verify test quality
4. **Security focus** - Vulnerability assessment
5. **Synthesize** - Compile findings

## Completion

Report to user:
```
Review complete: [X critical, Y warnings, Z suggestions]

Quality Score: [score]/100

[If critical issues]
⚠️  Blocking issues found. Fix before proceeding.

[If clean]
✅ Code meets quality standards. Ready to merge.
```
