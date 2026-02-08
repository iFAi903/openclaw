# Memory - Skills Library

Last updated: 2026-02-09

## Available Skills

### Development Workflow Skills

#### 1. claude-code-best-practices
**Location**: `skills/claude-code-best-practices/`
**Purpose**: Comprehensive Claude Code development workflow guidance
**Use when**: Working with Claude Code for coding tasks, multi-step implementations, debugging, refactoring
**Key features**:
- Context Window management strategies
- Plan Mode workflow (explore → plan → execute → verify)
- CLAUDE.md configuration best practices
- Session management commands
- Common workflow examples
- Prompt techniques

#### 2. dev-orchestrator
**Location**: `skills/dev-orchestrator/`
**Purpose**: Meta skill for orchestrating software development workflows
**Use when**: Starting any multi-step development task, feature implementation, bug fix, or refactoring
**Key features**:
- Automatic routing to specialized skills
- Manages plan → execute → review cycles
- Coordinates between plan-creator, code-executor, code-reviewer
- Clear handoff between stages

#### 3. plan-creator
**Location**: `skills/plan-creator/`
**Purpose**: Creates detailed implementation plans for development tasks
**Use when**: You have requirements for a multi-step feature, refactor, or bug fix
**Key features**:
- Breaks work into 2-5 minute micro-tasks
- Each task includes: file paths, complete code, verification steps
- Emphasizes TDD, DRY, YAGNI, frequent commits
- Output saved to `docs/plans/YYYY-MM-DD-<feature>.md`

#### 4. code-executor
**Location**: `skills/code-executor/`
**Purpose**: Executes implementation plans following strict TDD cycle
**Use when**: You have an approved plan document and need to implement tasks
**Key features**:
- RED-GREEN-REFACTOR cycle enforcement
- Task-by-task execution
- Error handling and progress tracking
- Frequent commits after each task

#### 5. code-reviewer
**Location**: `skills/code-reviewer/`
**Purpose**: Comprehensive code quality assessment
**Use when**: Code implementation is complete, pre-commit/PR review
**Key features**:
- Checks: correctness, security, performance, maintainability, testing, documentation
- Severity levels: critical/blocking, warning, suggestion
- Quality score calculation
- Output saved to `docs/reviews/YYYY-MM-DD-<feature>.md`

#### 6. tdd-enforcer
**Location**: `skills/tdd-enforcer/`
**Purpose**: Enforces Test-Driven Development workflow
**Use when**: Any coding task (embedded in workflow)
**Key features**:
- RED-GREEN-REFACTOR cycle
- Prevents "write code then add tests" anti-pattern
- Test quality checklist

#### 7. debug-strategist
**Location**: `skills/debug-strategist/`
**Purpose**: Systematic debugging for complex issues
**Use when**: Facing bugs that aren't immediately obvious, intermittent failures, performance issues
**Key features**:
- REPRODUCE → ISOLATE → HYPOTHESIZE → TEST → FIX → VERIFY process
- Binary search debugging
- Rubber duck debugging
- Common bug patterns reference
- Output saved to `docs/debug/YYYY-MM-DD-<issue>.md`

### Tool Orchestration Skills

#### 8. vibecoding-toolkit
**Location**: `skills/vibecoding-toolkit/`
**Purpose**: Multi-tool orchestration for OpenCode, Codex, and Antigravity
**Use when**: Need to select optimal AI coding tool(s) for a task
**Key features**:
- Tool selection matrix (by project type, task type, constraints)
- Decision algorithm for tool recommendation
- Multi-tool workflow templates (sequential, parallel)
- Tool-specific launch commands and best practices

## Usage Patterns

### Pattern 1: Full Development Workflow
```
User request → dev-orchestrator → plan-creator → [user approval] → code-executor → code-reviewer → completion
```

### Pattern 2: Quick Task
```
User request → direct tool execution (codex/opencode/antigravity via vibecoding-toolkit)
```

### Pattern 3: Bug Fix
```
User report → debug-strategist → plan-creator → code-executor → verification
```

## GitHub Repository

Skills are tracked in: https://github.com/[username]/openclaw-skills
(Replace with actual repository URL once pushed)

## Notes

- All skills follow the Agent Skills format (SKILL.md frontmatter + instructions)
- Skills are stored in `skills/<skill-name>/SKILL.md`
- Additional resources in `skills/<skill-name>/references/` and `skills/<skill-name>/scripts/`
