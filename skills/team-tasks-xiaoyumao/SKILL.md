---
name: team-tasks-xiaoyumao
description: Multi-agent pipeline coordination for Xiaoyumao's development workflow. Integrates team-tasks with OpenClaw to orchestrate Claude Code, Codex, Antigravity, and OpenCode agents through shared JSON task files.
metadata:
  version: 1.0.0
  author: 小羽毛 (Xiaoyumao)
  based_on: win4r/team-tasks
  supports:
    - claude-code
    - codex
    - antigravity
    - opencode
---

# Team Tasks - 小羽毛多 Agent 协同机制

基于 [win4r/team-tasks](https://github.com/win4r/team-tasks) 的多 Agent 协调系统，为四大开发工具矩阵（Claude Code / Codex / Antigravity / OpenCode）提供任务分发和进度跟踪。

## 核心概念

### 🎭 Agent 角色定义

| Agent ID | 对应工具 | 角色定位 | 擅长任务 |
|----------|---------|---------|---------|
| `planner` | Claude Code (Plan Mode) | 架构师/规划师 | 需求分析、架构设计、技术选型 |
| `coder` | Codex | 快速编码者 | 功能实现、代码生成、快速迭代 |
| `browser` | Antigravity | 浏览器专家 | UI 测试、网页抓取、视觉验证 |
| `architect` | OpenCode | 系统架构师 | 复杂重构、多模块协调、代码审查 |

### 🔄 三种协调模式

| 模式 | 适用场景 | 工作流程 |
|------|---------|---------|
| **Linear** | 简单功能、Bug 修复 | planner → coder → browser → architect（顺序执行） |
| **DAG** | 复杂功能、多模块 | 依赖图驱动，可并行任务 |
| **Debate** | 技术选型、代码审查 | 多 Agent 立场表达 + 交叉评审 |

---

## 快速开始

### 1. 安装依赖

```bash
# 克隆 team-tasks（需要时）
git clone https://github.com/win4r/team-tasks.git ~/tools/team-tasks

# 确保 Python 3.12+
python3 --version

# 设置环境变量
export TEAM_TASKS_DIR=~/.clawd/data/team-tasks
export TEAM_TASKS_BIN=~/tools/team-tasks/scripts/task_manager.py
```

### 2. 创建项目

```bash
# Linear 模式（简单功能）
python3 $TEAM_TASKS_BIN init my-feature \
  --goal "实现用户认证功能" \
  --mode linear \
  --pipeline "planner,coder,browser,architect"

# DAG 模式（复杂功能）
python3 $TEAM_TASKS_BIN init my-feature \
  --goal "构建电商搜索系统" \
  --mode dag
```

### 3. 分配任务

```bash
# Linear 模式 - 为每个 stage 分配任务
python3 $TEAM_TASKS_BIN assign my-feature planner \
  "分析认证需求：JWT vs Session，绘制架构图"

python3 $TEAM_TASKS_BIN assign my-feature coder \
  "实现登录/注册 API，使用 FastAPI + JWT"

python3 $TEAM_TASKS_BIN assign my-feature browser \
  "测试登录流程，截图验证 UI 表现"

python3 $TEAM_TASKS_BIN assign my-feature architect \
  "代码审查：安全性、性能、可维护性"
```

### 4. 启动工作流

```bash
# 查看当前状态
python3 $TEAM_TASKS_BIN status my-feature

# 查看下一个任务
python3 $TEAM_TASKS_BIN next my-feature --json
```

---

## OpenClaw 集成

### 自动分发循环（Linear 模式）

```python
# 在 OpenClaw 中使用
import json
import subprocess

def dispatch_next_task(project):
    """自动获取并分发下一个任务"""
    
    # 1. 获取下一个 stage
    result = subprocess.run(
        ["python3", TEAM_TASKS_BIN, "next", project, "--json"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return None
    
    task_info = json.loads(result.stdout)
    agent_id = task_info["stage"]
    task_desc = task_info["task"]
    
    # 2. 更新状态为 in-progress
    subprocess.run([
        "python3", TEAM_TASKS_BIN, "update",
        project, agent_id, "in-progress"
    ])
    
    # 3. 根据 agent_id 选择对应的工具并分发
    agent_mapping = {
        "planner": "claude-code",
        "coder": "codex", 
        "browser": "antigravity",
        "architect": "opencode"
    }
    
    tool = agent_mapping.get(agent_id, "claude-code")
    
    # 4. 使用 sessions_send 分发任务
    sessions_send(
        session_key=f"{tool}-worker",
        message=f"【Team Task】{task_desc}\n\n项目: {project}\nAgent: {agent_id}"
    )
    
    return task_info

def collect_result(project, agent_id, output):
    """收集 Agent 完成的结果"""
    
    # 1. 保存结果
    subprocess.run([
        "python3", TEAM_TASKS_BIN, "result",
        project, agent_id, output
    ])
    
    # 2. 标记为 done
    subprocess.run([
        "python3", TEAM_TASKS_BIN, "update",
        project, agent_id, "done"
    ])
    
    # 3. 自动分发下一个任务
    return dispatch_next_task(project)
```

### DAG 模式并行分发

```python
def dispatch_ready_tasks(project):
    """分发所有就绪任务（并行）"""
    
    # 1. 获取所有就绪任务
    result = subprocess.run(
        ["python3", TEAM_TASKS_BIN, "ready", project, "--json"],
        capture_output=True, text=True
    )
    
    ready_tasks = json.loads(result.stdout)["ready"]
    
    # 2. 并行分发
    for task in ready_tasks:
        agent_id = task["agent"]
        task_id = task["id"]
        task_desc = task["desc"]
        dep_outputs = task.get("depOutputs", {})  # 依赖任务的输出
        
        # 构建带上下文的提示
        context = ""
        if dep_outputs:
            context = "\n\n【前置任务输出】\n"
            for dep_id, output in dep_outputs.items():
                context += f"- {dep_id}: {output}\n"
        
        # 更新状态并分发
        subprocess.run([
            "python3", TEAM_TASKS_BIN, "update",
            project, task_id, "in-progress"
        ])
        
        sessions_send(
            session_key=f"{agent_mapping[agent_id]}-worker",
            message=f"【DAG Task】{task_desc}{context}"
        )
```

---

## 工作流模板

### 模板 A：快速功能开发（Linear）

```bash
# 1. 初始化项目
python3 $TEAM_TASKS_BIN init quick-feature \
  -g "添加密码重置功能" \
  -m linear \
  -p "planner,coder,architect"

# 2. 分配任务
python3 $TEAM_TASKS_BIN assign quick-feature planner \
  "设计密码重置流程：邮箱验证 + Token 机制"

python3 $TEAM_TASKS_BIN assign quick-feature coder \
  "实现 /forgot-password 和 /reset-password 接口"

python3 $TEAM_TASKS_BIN assign quick-feature architect \
  "审查：Token 安全性、过期时间、并发处理"
```

### 模板 B：全栈 Web 应用（DAG）

```bash
# 1. 创建 DAG 项目
python3 $TEAM_TASKS_BIN init webapp -m dag \
  -g "构建博客平台（前端 + 后端 + 数据库）"

# 2. 添加并行任务
# 设计阶段
python3 $TEAM_TASKS_BIN add webapp api-design \
  -a planner --desc "设计 REST API 规范"

python3 $TEAM_TASKS_BIN add webapp ui-design \
  -a planner --desc "设计 UI 组件库和页面结构"

# 并行开发（依赖设计）
python3 $TEAM_TASKS_BIN add webapp backend \
  -a coder -d "api-design" \
  --desc "实现后端 API（FastAPI + PostgreSQL）"

python3 $TEAM_TASKS_BIN add webapp frontend \
  -a coder -d "ui-design" \
  --desc "实现前端页面（React + Tailwind）"

# 集成测试（依赖前后端）
python3 $TEAM_TASKS_BIN add webapp e2e-test \
  -a browser -d "backend,frontend" \
  --desc "端到端测试：用户注册 → 发帖 → 评论"

# 最终审查
python3 $TEAM_TASKS_BIN add webapp final-review \
  -a architect -d "e2e-test" \
  --desc "架构审查和性能优化建议"

# 3. 查看依赖图
python3 $TEAM_TASKS_BIN graph webapp
```

### 模板 C：技术选型 Debate

```bash
# 1. 创建 Debate 项目
python3 $TEAM_TASKS_BIN init tech-choice --mode debate \
  -g "选择前端框架：React vs Vue vs Svelte"

# 2. 添加辩论者
python3 $TEAM_TASKS_BIN add-debater tech-choice coder \
  --role "重视开发效率和生态的工程师"

python3 $TEAM_TASKS_BIN add-debater tech-choice browser \
  --role "关注性能和用户体验的前端专家"

python3 $TEAM_TASKS_BIN add-debater tech-choice architect \
  --role "考虑长期维护和团队规模的架构师"

# 3. 开始辩论
python3 $TEAM_TASKS_BIN round tech-choice start

# 4. 在 OpenClaw 中收集各方观点
# （每个 Agent 使用 sessions_send 提交立场）

# 5. 生成交叉评审
python3 $TEAM_TASKS_BIN round tech-choice cross-review

# 6. 最终综合
python3 $TEAM_TASKS_BIN round tech-choice synthesize
```

---

## 状态监控

### 查看项目状态

```bash
# 状态概览
python3 $TEAM_TASKS_BIN status my-project

# JSON 格式（供 OpenClaw 解析）
python3 $TEAM_TASKS_BIN status my-project --json
```

**输出示例：**
```
📋 Project: my-feature
🎯 Goal: 构建电商搜索系统
📊 Status: active | Mode: dag

🟢 Ready to dispatch (2 tasks):
📌 api-design → agent: planner
📌 ui-design → agent: planner

⬜ backend → agent: coder (deps: api-design)
⬜ frontend → agent: coder (deps: ui-design)
⬜ e2e-test → agent: browser (deps: backend,frontend)
⬜ final-review → agent: architect (deps: e2e-test)

Progress: [░░░░░░░] 0/6
```

### 查看历史记录

```bash
# 查看特定 stage 的日志
python3 $TEAM_TASKS_BIN history my-project coder

# 查看所有项目的列表
python3 $TEAM_TASKS_BIN list
```

---

## 与 VibeCoding Toolkit 集成

将 team-tasks 整合到 vibecoding-toolkit 的工作流中：

```yaml
# .vibecoding/workflows/team-driven.yaml
name: team-driven-development
description: Multi-agent coordinated development using team-tasks

steps:
  1:
    action: init_team_project
    tool: team-tasks
    params:
      name: "{{project_name}}"
      mode: "{{mode|dag}}"
      goal: "{{project_goal}}"
      
  2:
    action: define_agents
    agents:
      - planner: claude-code
      - coder: codex
      - browser: antigravity
      - architect: opencode
      
  3:
    action: dispatch_loop
    parallel: "{{mode == 'dag'}}"
    on_complete: notify_user
```

---

## 故障排除

### Agent 无响应

```bash
# 重置任务状态
python3 $TEAM_TASKS_BIN reset my-project coder

# 或重置整个项目
python3 $TEAM_TASKS_BIN reset my-project --all
```

### 依赖死锁

```bash
# 检查依赖图
python3 $TEAM_TASKS_BIN graph my-project

# 手动跳过有问题的任务
python3 $TEAM_TASKS_BIN update my-project blocker skipped
```

### 状态不一致

```bash
# 直接编辑 JSON（高级）
$EDITOR ~/.clawd/data/team-tasks/my-project.json
```

---

## 相关资源

- [win4r/team-tasks](https://github.com/win4r/team-tasks) - 原始项目
- [OpenClaw Sessions](https://docs.openclaw.ai/sessions) - 会话管理文档
- [VibeCoding Toolkit](../vibecoding-toolkit/SKILL.md) - 工具选型矩阵

---

*Created by 小羽毛 🪶*  
*Multi-agent orchestration for the modern AI development workflow.*