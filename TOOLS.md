# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Team Tasks Configuration

**Installation Path**: `/Users/ifai_macpro/.openclaw/workspace/team-tasks/`
**Data Directory**: `/Users/ifai_macpro/.openclaw/data/team-tasks/`
**Wrapper Script**: `/Users/ifai_macpro/.openclaw/workspace/team-tasks-wrapper.sh`

### Environment Variables

```bash
export TEAM_TASKS_DIR="/Users/ifai_macpro/.openclaw/data/team-tasks"
export TEAM_TASKS_BIN="/Users/ifai_macpro/.openclaw/workspace/team-tasks/scripts/task_manager.py"
```

### Quick Commands

```bash
# Using wrapper (recommended)
./team-tasks-wrapper.sh init my-project -g "Project goal" -m linear

# Or directly
python3 /Users/ifai_macpro/.openclaw/workspace/team-tasks/scripts/task_manager.py --help
```

### Agent Mapping

| Agent ID | Tool | Role |
|----------|------|------|
| planner | Claude Code | 架构师/规划师 |
| coder | Codex | 快速编码者 |
| browser | Antigravity | 浏览器专家 |
| architect | OpenCode | 系统架构师 |

---

Add whatever helps you do your job. This is your cheat sheet.
