---
name: tdd-enforcer
description: Enforces Test-Driven Development workflow. Use when writing new features, fixing bugs, or adding tests. Ensures RED-GREEN-REFACTOR cycle: write failing test first, watch it fail, write minimal code to pass, refactor while green. Prevents "write code then add tests" anti-pattern.
disable-model-invocation: true
---

# TDD Enforcer

Strict RED-GREEN-REFACTOR cycle enforcement.

## Core Principle

**NEVER write implementation code before a failing test exists.**

## RED-GREEN-REFACTOR Cycle

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│   RED   │ → │  GREEN  │ → │ REFACTOR│
│Write    │    │Minimal  │    │Improve  │
│failing  │    │code to  │    │while    │
│test     │    │pass     │    │green    │
└─────────┘    └─────────┘    └─────────┘
      ↑                            ↓
      └────────────────────────────┘
              Repeat
```

## Enforcement Rules

### Rule 1: RED First
- Write test that describes desired behavior
- Run test, confirm it FAILS
- If test passes → test is wrong, fix it

### Rule 2: Minimal GREEN
- Write just enough code to pass the test
- No "while I'm here" additions
- Cheating is allowed (hardcode if needed)

### Rule 3: Refactor on Green
- Only refactor when tests pass
- Run tests after each change
- If tests fail → revert, smaller steps

### Rule 4: Delete Untested Code
- Any code written before tests must be deleted
- Start fresh with test-first approach

## TDD Workflow

### Given: Feature request
```
"Add user registration with email validation"
```

### Step 1: RED - Write failing test
```python
def test_register_user_with_valid_email():
    result = register_user("user@example.com", "password123")
    assert result.success is True
    assert result.user.email == "user@example.com"

def test_register_user_with_invalid_email():
    result = register_user("invalid-email", "password123")
    assert result.success is False
    assert result.error == "Invalid email format"
```

Run: `pytest test_registration.py -v`
Expected: **FAIL** (function doesn't exist)

### Step 2: GREEN - Minimal implementation
```python
def register_user(email, password):
    if "@" not in email:
        return RegistrationResult(success=False, error="Invalid email format")
    return RegistrationResult(success=True, user=User(email=email))
```

Run: `pytest test_registration.py -v`  
Expected: **PASS**

### Step 3: REFACTOR - Improve while green
- Extract email validation
- Improve error messages
- Add type hints

Run tests after each change → still green? continue.

## TDD Anti-Patterns (STOP and Correct)

| Anti-Pattern | Detection | Correction |
|--------------|-----------|------------|
| "I'll add tests later" | Code exists without tests | Delete code, start with test |
| Testing implementation | Tests check how not what | Test behavior, not methods |
| Large steps | 10+ lines between test runs | Smaller increments |
| Commented tests | Disabled tests in code | Fix or delete |
| Slow tests | Tests take > 1s each | Refactor test setup |

## Test Quality Checklist

- [ ] Test describes behavior, not implementation
- [ ] Test name explains what's being verified
- [ ] One concept per test
- [ ] No conditional logic in tests
- [ ] Fast execution (< 100ms each)
- [ ] Independent (order doesn't matter)

## When to Break Rules

Never. But if you must:

1. **Spikes/Prototypes** - Research only, throw away code after
2. **Generated code** - Auto-generated boilerplate (still test integration)
3. **Bug fixes** - Write test that reproduces bug first

## Completion Criteria

Feature is "TDD complete" when:
- All functionality has tests
- Tests fail if functionality breaks
- Tests describe expected behavior
- No code without test coverage (except trivial getters)
