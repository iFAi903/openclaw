---
name: vibecoding-toolkit
description: Multi-tool orchestration for VibeCoding workflows. Intelligently selects and coordinates between OpenCode, Codex (OpenAI), and Antigravity based on project requirements, task type, and efficiency criteria. Provides unified interface for tool selection, execution, and result synthesis.
disable-model-invocation: false
---

# VibeCoding Toolkit

Unified orchestration layer for OpenCode, Codex, Antigravity, and **Claude Code** AI coding agents.

## Philosophy

**Not all tools are equal for every task.** This toolkit analyzes your project and task characteristics to recommend and orchestrate the optimal tool(s) for the job.

## Tool Profiles

### 🔮 Claude Code (Anthropic)
**Strengths**: Deep Anthropic integration, Plan Mode for systematic planning, subagent system, best-in-class code understanding
**Best for**: Complex refactoring, systematic debugging, multi-step implementations, projects requiring careful planning
**Models**: Claude 4 Opus/Sonnet, Claude 3.5 Sonnet
**Key Features**:
- Plan Mode (Shift+Tab) for exploration without code changes
- Subagent system (@mentions) for specialized tasks
- CLAUDE.md project configuration
- /clear, /compact, /context for context management
- Skills system (load custom skills)

### 🔧 OpenCode
**Strengths**: Multi-model, open-source, highly configurable, rich agent system
**Best for**: Complex multi-file projects, research-heavy tasks, custom workflows
**Models**: 75+ providers (Claude, GPT, Gemini, local models, etc.)
**Key Features**:
- Build/Plan/Explore agents
- AGENTS.md project configuration
- Subagent system (@mentions)
- /init, /connect, /models, /undo commands

### ⚡ Codex (OpenAI)
**Strengths**: Deep OpenAI integration, polished UX, strong code understanding
**Best for**: Quick iterations, OpenAI ecosystem users, standard web projects
**Models**: GPT-4o, o1, o3-mini
**Key Features**:
- Skills system ($skill-name)
- /commands (/, /config, /help)
- Full-screen terminal UI
- Native IDE extensions

### 🌐 Antigravity (Google)
**Strengths**: Browser automation, computer use capabilities, Gemini integration
**Best for**: Web scraping, UI testing, browser-based workflows, visual tasks
**Models**: Gemini 2.5/3 Pro/Flash
**Key Features**:
- Computer Use Preview (browser automation)
- Playwright/Browserbase integration
- Screenshot-based interaction
- Visual debugging

---

## Decision Matrix

### By Project Type

| Project Type | Primary | Secondary | Rationale |
|--------------|---------|-----------|-----------|
| Complex refactoring | **Claude Code** | OpenCode | Plan Mode essential for large refactors |
| Systematic debugging | **Claude Code** | OpenCode | Best debugging workflow and context management |
| Multi-step implementation | **Claude Code** | Codex | Plan → Execute pattern |
| Full-stack web app | OpenCode | Codex | Multi-agent for complex architecture |
| API/backend service | Codex | OpenCode | Fast iteration, standard patterns |
| Browser automation | Antigravity | - | Native web interaction |
| Legacy codebase | **Claude Code** | OpenCode | Plan Mode for understanding before changes |
| Quick prototype | Codex | - | Fastest setup-to-code |
| Research/exploration | **Claude Code** | OpenCode | Plan mode, subagents |

### By Task Type

| Task | Recommended Tool | Why |
|------|------------------|-----|
| **Refactoring** | **Claude Code** | Plan Mode first, systematic approach |
| **Debugging** | **Claude Code** | Best context management, /rewind support |
| **Initial project setup** | OpenCode (/init) | AGENTS.md generation |
| **Feature implementation** | **Claude Code** or Codex | Claude for complex, Codex for simple |
| **Code review** | **Claude Code** (@subagent) | Dedicated subagent system |
| **Web scraping** | Antigravity | Browser automation |
| **UI testing** | Antigravity | Visual interaction |
| **Documentation** | Codex | Quick generation |

### By Constraint

| Constraint | Best Choice |
|------------|-------------|
| **Planning-heavy** | **Claude Code** | Plan Mode essential |
| **Complex debugging** | **Claude Code** | Best debugging workflow |
| Cost-sensitive | OpenCode (choose cheaper models) |
| Speed priority | Codex (optimized UX) |
| Privacy-first | OpenCode (local models via Ollama) |
| Browser-heavy | Antigravity |
| Multi-model needs | OpenCode |
| Best code understanding | **Claude Code** |

---

## Usage Patterns

### Pattern 1: Single Tool (Simple)
```
User: "Create a React component"
→ Toolkit: Recommends Codex for speed
→ Execute: Launch Codex with prompt
```

### Pattern 2: Sequential Tools (Standard)
```
User: "Build a full-stack app"
→ Toolkit: 
  1. OpenCode /init (project setup)
  2. OpenCode Plan mode (architecture)
  3. Codex (frontend components)
  4. OpenCode @code-reviewer (review)
```

### Pattern 3: Parallel Tools (Complex)
```
User: "Create web app with scraping"
→ Toolkit:
  - Thread 1: OpenCode (backend API)
  - Thread 2: Antigravity (scraper)
  - Thread 3: Codex (frontend)
→ Synthesize results
```

---

## Execution Interface

### Command Structure

```bash
# Analyze and recommend
vibecoding-toolkit --analyze "Build e-commerce site"

# Execute with specific tool
vibecoding-toolkit --tool codex --task "Create React components"

# Multi-tool workflow
vibecoding-toolkit --workflow fullstack --input "spec.md"

# Compare tools for task
vibecoding-toolkit --compare "Debug Python API"
```

### Integration with OpenClaw

```python
# Toolkit recommends tool
recommended = toolkit.select_tool(
    project_type="web_app",
    complexity="high",
    constraints=["speed", "multi_file"]
)
# Returns: {"primary": "opencode", "secondary": "codex", "rationale": "..."}

# Spawn appropriate session
sessions_spawn(
    task=task_description,
    agent_id="main",
    tool_config=recommended["config"]
)
```

---

## Tool-Specific Launch Commands

### Claude Code
```bash
# Interactive mode (recommended for complex tasks)
claude

# Plan mode first
claude --permission-mode plan

# One-shot with wrapper (for automation)
./scripts/claude_code_run.py -p "task description" --permission-mode plan

# With specific tools allowed
./scripts/claude_code_run.py \
  -p "implement feature" \
  --allowedTools "Bash,Read,Edit"

# Continue recent conversation
claude -c

# List and resume previous sessions
claude --list
claude --resume
```

### OpenCode
```bash
# Standard
cd /project && opencode

# With specific model
opencode --model anthropic/claude-sonnet-4

# Plan mode first
opencode
> (Tab to switch to Plan)
```

### Codex
```bash
# Interactive
codex

# One-shot
codex -p "task description"

# With skills
codex
> $create-plan implement auth system
```

### Antigravity
```bash
# Browser automation
python main.py --query "Scrape product data from example.com"

# With specific URL
python main.py --env=playwright --initial_url="https://example.com" --query="..."
```

---

## Workflow Templates

### Template A: Web Application (Full Stack) - with Claude Code

```yaml
name: fullstack-webapp-claude
description: Complete web application development with Claude Code planning

steps:
  1:
    tool: claude_code
    mode: plan
    action: analyze codebase and create implementation plan
    output: implementation_plan.md
    
  2:
    tool: claude_code
    action: scaffold project structure based on plan
    output: project_skeleton/
    
  3:
    tool: codex
    parallel:
      - frontend: "Implement React components"
      - backend: "Implement API endpoints"
      
  4:
    tool: claude_code
    subagent: @code-reviewer
    action: comprehensive code review
    
  5:
    tool: antigravity
    action: e2e browser testing
```

### Template B: Complex Refactoring (Claude Code Optimized)

```yaml
name: complex-refactoring
description: Large-scale refactoring with systematic planning

steps:
  1:
    tool: claude_code
    mode: plan
    action: analyze current implementation and identify refactoring targets
    output: refactoring_plan.md
    
  2:
    tool: claude_code
    action: create test cases for existing behavior (before changes)
    output: regression_tests/
    
  3:
    tool: claude_code
    action: execute refactoring in small, verifiable steps
    checkpoint: after each module
    
  4:
    tool: claude_code
    action: run tests and fix any failures
    
  5:
    tool: opencode
    action: final review and edge case testing
```

### Template C: Data Pipeline

```yaml
name: data-pipeline
description: Extract, transform, load pipeline

steps:
  1:
    tool: antigravity
    action: scrape source websites
    output: raw_data/
    
  2:
    tool: opencode
    action: data transformation scripts
    
  3:
    tool: codex
    action: validation and testing
```

### Template C: API Development

```yaml
name: api-development
description: REST/GraphQL API with tests

steps:
  1:
    tool: codex
    action: scaffold API structure
    
  2:
    tool: opencode
    agent: plan
    action: endpoint design
    
  3:
    tool: codex
    action: implement endpoints
    
  4:
    tool: opencode
    action: systematic testing
```

---

## Selection Algorithm

```python
def select_tool(project_profile, task_profile):
    scores = {
        "claude_code": 0,
        "opencode": 0,
        "codex": 0,
        "antigravity": 0
    }
    
    # Project complexity
    if project_profile["files"] > 20:
        scores["opencode"] += 2  # Better for large projects
        scores["claude_code"] += 1  # Good for large projects with planning
    
    if project_profile["is_web"]:
        scores["antigravity"] += 2
    
    if project_profile["needs_planning"]:
        scores["claude_code"] += 3  # Plan Mode is best
    
    if project_profile["needs_quick_iteration"]:
        scores["codex"] += 2
        
    # Task characteristics
    if task_profile["type"] == "browser_automation":
        return "antigravity"
    
    if task_profile["type"] in ["refactoring", "debugging"]:
        scores["claude_code"] += 3  # Best for these tasks
    
    if task_profile["type"] == "research":
        scores["claude_code"] += 2  # Plan Mode great for research
        scores["opencode"] += 1
    
    if task_profile["complexity"] == "simple":
        scores["codex"] += 2
    elif task_profile["complexity"] == "high":
        scores["claude_code"] += 2  # Better for high complexity
        
    # Select highest score
    return max(scores, key=scores.get)
```

---

## Best Practices

1. **Start Simple**: Use single tool for simple tasks
2. **Escalate Complexity**: Add tools as needed
3. **Parallelize**: Run independent tasks concurrently
4. **Review Always**: Use code-reviewer subagent before completion
5. **Tool Context**: Don't switch tools mid-task unless necessary
6. **Cost Awareness**: OpenCode lets you choose cheaper models
7. **Privacy First**: Use OpenCode with local models for sensitive code

---

## Troubleshooting

### OpenCode Issues
- Check `opencode auth list` for credentials
- Verify provider config in opencode.json
- Use /models to see available models

### Codex Issues
- Verify ChatGPT Plus/Pro subscription
- Check ~/.codex/config.toml
- Use /help for available commands

### Antigravity Issues
- Ensure GEMINI_API_KEY set
- Check Playwright/Browserbase setup
- Verify Python environment

---

## Extensions

### Current Core Tools
- ✅ **Claude Code** (Anthropic) - Planning and systematic development
- ✅ OpenCode - Multi-model, open-source
- ✅ Codex (OpenAI) - Quick iterations
- ✅ Antigravity (Google) - Browser automation

### Future Integrations
- GitHub Copilot Chat
- Cursor
- Continue.dev
- Windsurf

### Custom Workflows
Users can define custom workflows in `.vibecoding/workflows/` directory.
