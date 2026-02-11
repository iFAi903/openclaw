#!/bin/bash
# Team Tasks wrapper script for Xiaoyumao's workspace
# Usage: team-task [command] [args...]

export TEAM_TASKS_DIR="/Users/ifai_macpro/.openclaw/data/team-tasks"
export TEAM_TASKS_BIN="/Users/ifai_macpro/.openclaw/workspace/team-tasks/scripts/task_manager.py"

python3 "$TEAM_TASKS_BIN" "$@"