# Gstack 架构深度分析报告

## 1. 仓库结构概览

```
gstack/
├── README.md                     # 项目概览和快速开始
├── SKILL.md                      # 主入口技能 - 导航枢纽
├── ARCHITECTURE.md               # 架构设计文档
├── CHANGELOG.md                  # 版本变更记录
├── CLAUDE.md                     # Claude Code 项目配置
├── CONTRIBUTING.md               # 贡献指南
├── TODOS.md                      # 任务追踪
├── conductor.json                # 多实例并行配置
├── package.json                  # Node.js 项目配置
│
├── .claude/skills/gstack/        # Claude Code 技能安装目录
│   └── [skill-folders]/
│
├── browse/                       # 浏览器自动化 CLI 工具
│   ├── SKILL.md
│   ├── src/
│   │   ├── cli.ts               # 命令行入口
│   │   ├── server.ts            # 浏览器服务器
│   │   ├── commands.ts          # 命令实现
│   │   ├── snapshot.ts          # 页面快照
│   │   └── ...
│   └── test/
│
├── review/                       # 代码审查工具
│   ├── SKILL.md
│   ├── checklist.md             # 审查检查清单
│   ├── design-checklist.md      # 设计审查清单
│   └── greptile-triage.md       # Greptile 集成
│
├── qa/                           # QA 测试技能
│   ├── SKILL.md
│   ├── qa-only/SKILL.md         # 仅报告模式
│   ├── references/issue-taxonomy.md
│   └── templates/qa-report-template.md
│
├── plan-eng-review/             # 工程计划审查
│   └── SKILL.md
├── plan-ceo-review/             # CEO 视角计划审查
│   └── SKILL.md
├── plan-design-review/          # 设计计划审查
│   └── SKILL.md
├── design-consultation/         # 设计系统咨询
│   └── SKILL.md
├── design-review/               # 实时代码设计审查
│   └── SKILL.md
├── ship/                        # 发布工作流
│   └── SKILL.md
├── document-release/            # 发布文档生成
│   └── SKILL.md
├── retro/                       # 项目回顾
│   └── SKILL.md
├── gstack-upgrade/              # 升级管理
│   └── SKILL.md
├── setup-browser-cookies/       # 浏览器 Cookie 设置
│   └── SKILL.md
│
├── scripts/                     # 开发脚本
│   ├── dev-skill.ts
│   ├── gen-skill-docs.ts
│   └── eval-*.ts
│
└── test/                        # 测试套件
    ├── skill-e2e.test.ts
    ├── skill-llm-eval.test.ts
    └── fixtures/
```

## 2. SKILL.md 格式分析

### 2.1 YAML Frontmatter 结构

```yaml
---
name: skill-name                    # 技能唯一标识（kebab-case）
version: 2.0.0                      # 语义化版本
skills:                             # 子技能列表（可选）
  - child-skill-1
  - child-skill-2
description: |
  多行描述文本，支持 Markdown
  说明技能用途和触发条件
allowed-tools:                      # 允许使用的 Claude Code 工具
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
---
```

### 2.2 核心内容结构

每个 SKILL.md 遵循统一模板：

```markdown
## Preamble (run first)
```
更新检查 + 会话管理 + 分支检测的 Bash 脚本
```

## AskUserQuestion Format
统一的提问格式规范（4 步结构）

## Completeness Principle — Boil the Lake
完整性原则说明

## Contributor Mode
贡献者模式（可选）

## Step 0: Detect base branch
检测目标分支

# /slash-command: 技能标题
详细的工作流说明...

### Phase X: 阶段名称
具体步骤...

## Important Rules
关键规则清单
```

## 3. Slash Command 映射表

| Slash Command | 对应 SKILL.md | 触发场景 | 主要工具 |
|--------------|---------------|---------|---------|
| `/browse` | `browse/SKILL.md` | 浏览器测试、页面验证 | Bash, Read, AskUserQuestion |
| `/review` | `review/SKILL.md` | PR 发布前代码审查 | Bash, Read, Edit, Write, Grep, Glob, AskUserQuestion |
| `/qa` | `qa/SKILL.md` | 系统 QA 测试+修复 | Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, WebSearch |
| `/qa-only` | `qa-only/SKILL.md` | 仅 QA 报告不修复 | (同上) |
| `/plan-eng-review` | `plan-eng-review/SKILL.md` | 工程计划审查 | Bash, Read, Edit, Grep, Glob, AskUserQuestion |
| `/plan-ceo-review` | `plan-ceo-review/SKILL.md` | CEO 视角计划审查 | Bash, Read, Edit, Grep, Glob, AskUserQuestion |
| `/plan-design-review` | `plan-design-review/SKILL.md` | 设计计划审查 | Bash, Read, Edit, Grep, Glob, AskUserQuestion |
| `/design-consultation` | `design-consultation/SKILL.md` | 设计系统创建 | Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, WebSearch |
| `/design-review` | `design-review/SKILL.md` | 实时代码设计审查 | Bash, Read, Edit, Write, Grep, Glob, AskUserQuestion |
| `/ship` | `ship/SKILL.md` | 发布工作流 | Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion, WebSearch |
| `/document-release` | `document-release/SKILL.md` | 发布文档 | Bash, Read, Edit, Write, Grep, AskUserQuestion |
| `/retro` | `retro/SKILL.md` | 项目回顾 | Bash, Read, Write, Grep, Glob, AskUserQuestion |
| `/gstack-upgrade` | `gstack-upgrade/SKILL.md` | gstack 升级 | (Bash 自发现) |
| `/setup-browser-cookies` | `setup-browser-cookies/SKILL.md` | Cookie 设置 | (Bash 自发现) |

**注意**: 所有技能都在 `allowed-tools` 中声明，Claude Code 会强制执行工具权限。
