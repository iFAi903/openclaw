---
name: skill-forge-xiaoyumao
description: Universal Skill generator and manager for multi-agent workflows. Creates, packages, installs, and manages skills across Claude Code, Codex, Antigravity, and OpenCode. Integrates with existing tools when available, falls back to native implementation when needed.
metadata:
  version: 1.0.0
  author: 小羽毛 (Xiaoyumao)
  supports:
    - claude-code
    - codex
    - antigravity
    - opencode
  integrations:
    - skill-seekers
    - gemini-cli
    - openai-skills-api
---

# Skill Forge - 小羽毛 Skill 生成与管理器

**"有现成的，能拿来就用；找不到现成的，再写有针对性的"**

一个统一的 Skill 生成与管理工具，支持四大 AI 开发工具矩阵，智能集成现有生态，无缝适配多平台。

## 核心理念

| 原则 | 说明 |
|------|------|
| **Reuse First** | 优先使用 Skill Seekers 等现成工具，不重复造轮子 |
| **Platform Agnostic** | 一份 Skill，多平台使用（Claude/Codex/Antigravity/OpenCode） |
| **Smart Fallback** | 有现成工具就用，没有则提供原生实现 |
| **渐进增强** | 基础功能不依赖外部工具，高级功能自动启用 |

---

## 支持的 AI 工具矩阵

| 工具 | Skill 格式 | 安装路径 | 支持状态 |
|------|-----------|----------|---------|
| **Claude Code** | `SKILL.md` + resources | `~/.claude/skills/` | ✅ 完整支持 |
| **Codex** | `skills/` 目录 | `~/.codex/skills/` | ✅ 完整支持 |
| **Antigravity** | `prompts/` + configs | `~/.antigravity/skills/` | ✅ 完整支持 |
| **OpenCode** | `AGENTS.md` + skills | `~/.opencode/skills/` | ✅ 完整支持 |

---

## 快速开始

### 1. 生成新 Skill

```bash
# 方式 A：从文档网站生成（需要 skill-seekers）
skill-forge generate --from-docs https://react.dev --name react --tool claude-code

# 方式 B：从 GitHub 仓库生成
skill-forge generate --from-github facebook/react --name react --tool codex

# 方式 C：从本地模板创建
skill-forge generate --from-template python-api --name my-api --tool opencode

# 方式 D：交互式创建
skill-forge generate --interactive
```

### 2. 安装 Skill

```bash
# 安装到特定工具
skill-forge install ./my-skill --tool claude-code

# 安装到所有工具
skill-forge install ./my-skill --tool all

# 从 GitHub 直接安装
skill-forge install https://github.com/user/skill-repo --tool codex
```

### 3. 管理 Skills

```bash
# 列出所有已安装 Skills
skill-forge list --tool claude-code

# 启用/禁用 Skill
skill-forge enable my-skill --tool claude-code
skill-forge disable my-skill --tool codex

# 更新 Skill
skill-forge update my-skill --tool opencode

# 卸载 Skill
skill-forge uninstall my-skill --tool antigravity
```

### 4. 跨平台转换

```bash
# 将 Claude Code Skill 转换为 Codex 格式
skill-forge convert ./my-claude-skill --from claude-code --to codex

# 批量转换
skill-forge convert ./skills/ --from claude-code --to all
```

---

## Skill 格式标准

### 通用 Skill 结构

```
my-skill/
├── SKILL.md              # 核心说明文档（所有平台）
├── metadata.yaml         # 元数据（名称、描述、版本、作者）
├── resources/            # 资源文件
│   ├── templates/        # 模板文件
│   ├── examples/         # 示例代码
│   └── references/       # 参考资料
└── scripts/              # 辅助脚本
    ├── install.sh
    └── validate.sh
```

### SKILL.md 标准格式

```markdown
---
name: skill-name
description: Brief description of what this skill does
version: 1.0.0
author: Your Name
tools:
  - claude-code
  - codex
  - opencode
  - antigravity
tags:
  - web-dev
  - api
---

# Skill 名称

## 适用场景

什么时候使用这个 Skill...

## 核心能力

- 能力 1
- 能力 2
- 能力 3

## 使用示例

### 示例 1：基本用法

```
用户：帮我做 X
AI：使用 Skill 后的处理方式...
```

## 注意事项

- 注意 1
- 注意 2
```

---

## 平台特定适配

### Claude Code 适配

```yaml
# metadata.yaml
claude_code:
  path: ~/.claude/skills/my-skill
  auto_load: true
  context: fork  # 或 inline
  allowed_tools: [Read, Edit, Bash]
```

### Codex 适配

```yaml
# metadata.yaml
codex:
  path: ~/.codex/skills/my-skill
  commands:
    - my-skill:help
    - my-skill:run
```

### OpenCode 适配

```yaml
# metadata.yaml
opencode:
  path: ~/.opencode/skills/my-skill
  agents:
    - my-skill-agent
  triggers:
    - file_pattern: "*.py"
```

### Antigravity 适配

```yaml
# metadata.yaml
antigravity:
  path: ~/.antigravity/skills/my-skill
  prompts:
    - name: default
      template: prompts/default.txt
```

---

## 与现有工具集成

### Skill Seekers 集成（推荐）

当检测到 `skill-seekers` 已安装时，自动使用其功能：

```bash
# 自动检测并使用 skill-seekers
skill-forge generate --from-docs https://docs.example.com
# → 检测到 skill-seekers，使用其 scrape 功能
# → 自动增强、打包、转换格式
```

**优势**：
- 利用其强大的文档爬取能力
- 自动 AI 增强
- 多源合并（Docs + GitHub + PDF）

### Gemini CLI 集成

```bash
# 使用 Gemini 的 Skill 管理方式
skill-forge list --tool gemini
# → 实际调用: gemini skills list
```

### OpenAI Skills API 集成

```bash
# 上传 Skill 到 OpenAI
skill-forge upload ./my-skill --to openai
# → 调用 OpenAI Skills API
```

---

## 原生实现（无外部依赖）

当外部工具不可用时，提供原生实现：

### 文档爬取（原生）

```python
# 简化的文档爬取，不依赖外部工具
skill-forge generate --from-docs https://example.com --native
```

功能：
- 基础 HTML 解析
- Markdown 提取
- 简单分类

### Skill 模板（原生）

内置模板库：
- `python-api` - Python API 开发
- `web-frontend` - 前端开发
- `data-processing` - 数据处理
- `testing` - 测试相关
- `devops` - DevOps 工具

---

## 高级功能

### 1. Skill 市场

```bash
# 浏览官方 Skill 市场
skill-forge marketplace search react

# 安装市场 Skill
skill-forge marketplace install react-official

# 发布自己的 Skill
skill-forge marketplace publish ./my-skill
```

### 2. Skill 组合

```bash
# 创建 Skill 组合（多个 Skill 的集合）
skill-forge bundle create my-bundle --skills skill1,skill2,skill3

# 安装整个组合
skill-forge bundle install my-bundle --tool claude-code
```

### 3. 自动发现

```bash
# 扫描当前项目，推荐合适的 Skills
skill-forge discover .

# 自动安装推荐 Skills
skill-forge discover . --auto-install
```

### 4. 版本管理

```bash
# Skill 版本控制
skill-forge version my-skill --bump minor

# 回滚到旧版本
skill-forge rollback my-skill --to 1.0.0

# 比较版本差异
skill-forge diff my-skill 1.0.0 1.1.0
```

---

## 使用场景示例

### 场景 1：快速搭建项目环境

```bash
# 1. 发现项目类型
skill-forge discover ./my-project
# → 检测到 React + TypeScript 项目
# → 推荐：react-skill, typescript-skill, testing-skill

# 2. 安装推荐 Skills
skill-forge discover ./my-project --auto-install --tool claude-code

# 3. 开始使用
# 现在 Claude Code 已经具备了 React 和 TypeScript 的专业知识
```

### 场景 2：团队协作

```bash
# 1. 创建团队 Skill
skill-forge generate --from-template team-guidelines --name myteam-guidelines

# 2. 分享给团队成员
skill-forge package ./myteam-guidelines --output ./myteam-guidelines.zip

# 3. 团队成员安装
skill-forge install ./myteam-guidelines.zip --tool all
```

### 场景 3：从文档生成 Skill

```bash
# 使用 skill-seekers（如果有）或原生实现
skill-forge generate \
  --from-docs https://docs.djangoproject.com \
  --name django \
  --enhance \
  --tool claude-code

# 输出：~/.claude/skills/django/
```

---

## 故障排除

### 问题：Skill 无法加载

```bash
# 检查 Skill 格式
skill-forge validate ./my-skill

# 修复常见问题
skill-forge fix ./my-skill
```

### 问题：工具路径错误

```bash
# 查看配置
skill-forge config --show

# 修改工具路径
skill-forge config set claude-code.path ~/.config/claude/skills
```

### 问题：skill-seekers 未检测到

```bash
# 手动指定路径
skill-forge config set skill-seekers.path /usr/local/bin/skill-seekers

# 或强制使用原生实现
skill-forge generate --from-docs URL --native
```

---

## 配置

### 全局配置

```yaml
# ~/.config/skill-forge/config.yaml

default_tool: claude-code

paths:
  claude-code: ~/.claude/skills
  codex: ~/.codex/skills
  opencode: ~/.opencode/skills
  antigravity: ~/.antigravity/skills

integrations:
  skill-seekers:
    enabled: auto  # auto, true, false
    path: null     # 自动检测或指定路径
  
  gemini-cli:
    enabled: auto
    
  openai-api:
    enabled: false
    api_key: null

marketplace:
  registry: https://skills.clawhub.com
  auto_update: true
```

### 项目级配置

```yaml
# .skill-forge.yaml
project:
  name: my-project
  type: web-app
  
recommended_skills:
  - react
  - typescript
  - testing
  
auto_install: true
tool: claude-code
```

---

## 相关资源

- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) - 文档转 Skill 工具
- [Gemini CLI Skills](https://geminicli.com/docs/cli/skills/) - Google 的 Skill 系统
- [Claude Code Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) - Anthropic 官方文档
- [OpenAI Skills API](https://developers.openai.com/api/reference/resources/skills) - OpenAI API

---

*Created by 小羽毛 🪶*  
*Philosophy: Reuse first, create when needed.*