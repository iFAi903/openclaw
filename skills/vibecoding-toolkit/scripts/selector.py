#!/usr/bin/env python3
"""
VibeCoding Toolkit - Tool Selector
Recommends optimal tool(s) based on project and task characteristics.
"""

import json
import sys
from typing import Dict, List, Tuple

class ToolSelector:
    def __init__(self):
        self.tools = {
            "opencode": {
                "strengths": ["multi_model", "open_source", "configurable", "subagents"],
                "best_for": ["complex_projects", "research", "custom_workflows"],
                "setup": "medium",
                "cost": "variable",
                "speed": "medium"
            },
            "codex": {
                "strengths": ["polished_ux", "fast", "openai_integration"],
                "best_for": ["quick_iteration", "standard_projects", "prototyping"],
                "setup": "easy",
                "cost": "subscription",
                "speed": "fast"
            },
            "antigravity": {
                "strengths": ["browser_automation", "computer_use", "visual"],
                "best_for": ["web_scraping", "ui_testing", "browser_tasks"],
                "setup": "medium",
                "cost": "api",
                "speed": "medium"
            }
        }
    
    def score_tool(self, tool: str, project: Dict, task: Dict) -> int:
        """Score a tool for given project/task."""
        score = 0
        profile = self.tools[tool]
        
        # Complexity scoring
        if project.get("complexity") == "high":
            if "complex_projects" in profile["best_for"]:
                score += 3
        elif project.get("complexity") == "low":
            if "quick_iteration" in profile["best_for"]:
                score += 2
        
        # Task type scoring
        task_type = task.get("type", "")
        if task_type == "browser" and tool == "antigravity":
            score += 5
        elif task_type == "research" and tool == "opencode":
            score += 3
        elif task_type == "standard" and tool == "codex":
            score += 3
        
        # Priority scoring
        priority = project.get("priority", "")
        if priority == "speed" and profile["speed"] == "fast":
            score += 2
        if priority == "cost" and profile["cost"] == "variable":
            score += 2
        
        return score
    
    def select(self, project: Dict, task: Dict) -> Dict:
        """Select best tool(s) for project/task."""
        scores = {
            tool: self.score_tool(tool, project, task)
            for tool in self.tools
        }
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        primary = ranked[0][0]
        secondary = ranked[1][0] if ranked[1][1] > 0 else None
        
        return {
            "primary": primary,
            "secondary": secondary,
            "scores": dict(ranked),
            "rationale": self._explain_rationale(primary, project, task),
            "workflow": self._suggest_workflow(primary, secondary, task)
        }
    
    def _explain_rationale(self, tool: str, project: Dict, task: Dict) -> str:
        """Generate explanation for tool selection."""
        reasons = {
            "opencode": "Best for complex/multi-file projects with subagent support",
            "codex": "Fastest setup and iteration for standard development",
            "antigravity": "Native browser automation and visual interaction"
        }
        return reasons.get(tool, "General purpose selection")
    
    def _suggest_workflow(self, primary: str, secondary: str, task: Dict) -> List[str]:
        """Suggest workflow steps."""
        workflows = {
            ("opencode", "codex"): [
                "1. OpenCode /init for project setup",
                "2. OpenCode Plan mode for architecture",
                "3. Codex for rapid implementation",
                "4. OpenCode @code-reviewer for review"
            ],
            ("codex", "opencode"): [
                "1. Codex for quick scaffolding",
                "2. OpenCode for complex logic",
                "3. OpenCode subagents for testing"
            ],
            ("antigravity", "opencode"): [
                "1. Antigravity for data collection",
                "2. OpenCode for data processing",
                "3. OpenCode for analysis"
            ],
            ("opencode", None): [
                "1. OpenCode /init",
                "2. Use Plan/Build/Explore agents as needed"
            ],
            ("codex", None): [
                "1. Launch codex",
                "2. Use $skills for specialized tasks"
            ],
            ("antigravity", None): [
                "1. Setup Playwright/Browserbase",
                "2. Run browser automation tasks"
            ]
        }
        key = (primary, secondary)
        return workflows.get(key, [f"Use {primary} for this task"])


def main():
    if len(sys.argv) < 2:
        print("Usage: selector.py '{\"complexity\": \"high\", \"priority\": \"speed\"}' '{\"type\": \"web_app\"}'")
        sys.exit(1)
    
    project = json.loads(sys.argv[1])
    task = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    
    selector = ToolSelector()
    result = selector.select(project, task)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
