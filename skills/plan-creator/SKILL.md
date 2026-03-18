---
name: plan-creator
description: Creates detailed implementation plans for software development tasks. Use when you have requirements for a multi-step feature, refactor, or bug fix. Breaks down complex work into bite-sized, actionable tasks (2-5 minutes each) with exact file paths, code snippets, and verification steps. Emphasizes TDD, DRY, YAGNI, and frequent commits.
disable-model-invocation: true
---

# Plan Creator

Creates comprehensive implementation plans assuming the executor has zero context and questionable taste.

## When to Use

- Multi-step feature implementation
- Complex refactoring projects  
- Architectural changes
- Any task needing 3+ file modifications

## Output Format

Save to: `docs/plans/YYYY-MM-DD-<feature-name>.md`

```markdown
# [Feature Name] Implementation Plan

**Goal:** One sentence describing outcome

**Architecture:** 2-3 sentences on approach

**Tech Stack:** Key technologies

---

## Task 1: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/path/to/test.py`

**Steps:**

### Step 1: Write failing test
```python
def test_feature():
    result = function(input)
    assert result == expected
```

### Step 2: Verify test fails
Run: `pytest tests/path/test.py::test_feature -v`
Expected: FAIL

### Step 3: Write minimal implementation
```python
def function(input):
    return expected
```

### Step 4: Verify test passes  
Run: `pytest tests/path/test.py::test_feature -v`
Expected: PASS

### Step 5: Commit
```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```

---

## Task 2: [Next Component]
...
```

## Task Granularity Rules

Each task = one action (2-5 minutes max):
- ✅ "Write failing test"
- ✅ "Run test to verify it fails"
- ✅ "Implement minimal code to pass test"
- ❌ "Implement authentication" (too big)
- ❌ "Add tests and code" (two actions)

## Code Complete Principle

Plan must include:
- **Exact file paths** - no "the utils folder"
- **Complete code** - not "add validation logic"
- **Exact commands** - with expected output
- **Test strategy** - how to verify each step

## Principles

- **TDD**: Every task starts with a failing test
- **DRY**: Factor out common patterns
- **YAGNI**: Don't implement speculative features
- **Small Commits**: Commit after each task

## Post-Plan Actions

After saving plan:
1. Present summary to user
2. Ask for approval/modifications
3. Once approved, handoff to code-executor
