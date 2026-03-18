# VibeCoding Toolkit - Quick Reference

## One-Command Selection

| You Say | Toolkit Recommends |
|---------|-------------------|
| "Quick React component" | Codex (fastest) |
| "Build full-stack app" | OpenCode + Codex combo |
| "Scrape a website" | Antigravity |
| "Debug this codebase" | OpenCode (@debugger) |
| "Review my code" | OpenCode (@code-reviewer) |
| "API with tests" | Codex → OpenCode review |

## Tool Launch Cheat Sheet

### OpenCode
```bash
# Setup
curl -fsSL https://opencode.ai/install | bash
opencode
/init                    # Initialize project
/connect                 # Add API keys
/models                  # Select model
Tab                      # Switch Build/Plan mode
```

### Codex
```bash
# Setup (requires ChatGPT Plus/Pro)
# Built into subscription

codex                    # Interactive mode
codex -p "task"         # One-shot mode
$skill-name             # Invoke skill
/help                   # See commands
```

### Antigravity
```bash
# Setup
git clone https://github.com/google/computer-use-preview
cd computer-use-preview
pip install -r requirements.txt
playwright install chrome

export GEMINI_API_KEY="..."

python main.py --query="Go to Google and search..."
```

## Multi-Tool Workflows

### Workflow 1: Web App (Full Stack)
```
1. opencode /init
2. opencode (Plan mode) → architecture.md
3. Parallel:
   - codex → Frontend
   - opencode → Backend  
4. opencode @code-reviewer → Review
5. antigravity → E2E test
```

### Workflow 2: Data Pipeline
```
1. antigravity → Scrape data
2. opencode → Transform
3. codex → Validate
```

### Workflow 3: API Development
```
1. codex → Scaffold
2. opencode (Plan) → Design
3. codex → Implement
4. opencode → Test
```

## Decision Tree

```
Task?
├── Browser/web scraping? 
│   └── → Antigravity
├── Simple/quick? 
│   └── → Codex
├── Complex/multi-file?
│   └── → OpenCode
├── Need specific subagent?
│   └── → OpenCode (@mention)
└── Cost-sensitive?
    └── → OpenCode (choose model)
```

## Model Selection (OpenCode)

| Need | Model |
|------|-------|
| Speed | anthropic/claude-haiku |
| Balance | anthropic/claude-sonnet |
| Power | anthropic/claude-opus |
| Cheap | deepseek/deepseek-chat |
| Local | ollama/llama2 |

## Common Patterns

### Pattern: Research → Implement → Review
```bash
# 1. Research with OpenCode Plan
opencode
(Tab to Plan mode)
> Analyze codebase and suggest architecture

# 2. Implement with Codex (speed)
codex -p "Implement the suggested architecture"

# 3. Review with OpenCode subagent
opencode
> @code-reviewer review all recent changes
```

### Pattern: Parallel Development
```bash
# Terminal 1: Backend
opencode
> implement API

# Terminal 2: Frontend  
codex
> implement UI

# Terminal 3: Testing
antigravity
> test user flows
```
