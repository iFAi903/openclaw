# Development Skills Architecture

精简高效的软件开发 skill 体系，基于 Superpowers 和 VoltAgent 最佳实践提炼。

---

## 🎯 设计理念

### 精简去重
- **6 个核心 skills** 替代 100+ subagents
- 按**工作流阶段**组织，而非技术栈
- 语言/框架无关，专注**开发方法论**

### 经济有效
- 每个 skill 单职责，避免重复学习
- 清晰的输入/输出契约
- 使用 `sessions_spawn` 实现隔离执行

---

## 📦 Skill 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    dev-orchestrator                         │
│              （元协调器 - 自动路由任务）                      │
└─────────────┬─────────────┬─────────────┬───────────────────┘
              │             │             │
    ┌─────────▼────┐  ┌────▼─────┐  ┌────▼──────┐
    │ plan-creator │  │code-     │  │ code-     │
    │   （规划）    │  │executor  │  │ reviewer  │
    └──────────────┘  │（执行）   │  │（审查）    │
                      └────┬─────┘  └───────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼────┐  ┌───▼───┐  ┌─────▼─────┐
        │tdd-      │  │debug- │  │ （扩展位）  │
        │enforcer  │  │strategist     │
        │（TDD）   │  │（调试） │
        └──────────┘  └───────┘
```

---

## 🔧 Skills 详情

### 1. dev-orchestrator（元协调器）
**触发**: 任何多步骤开发任务
**职责**:
- 解析用户需求，判断复杂度
- 自动分派到合适的专项 skill
- 管理阶段间流转（规划→执行→审查）
- 汇总报告给用户

**使用**:
```
用户: "帮我实现用户认证功能"
→ orchestrator 自动调用 plan-creator → code-executor → code-reviewer
```

---

### 2. plan-creator（规划器）
**触发**: 需要多文件修改的任务
**输入**: 需求描述
**输出**: `docs/plans/YYYY-MM-DD-<feature>.md`

**核心**:
- 将复杂任务拆分为 2-5 分钟的微任务
- 每个任务包含：文件路径、完整代码、验证步骤
- 强调 TDD、DRY、YAGNI

---

### 3. code-executor（执行器）
**触发**: 已批准的 plan
**输入**: plan 文档
**输出**: 实现代码 + 测试 + commits

**核心**:
- 严格 RED-GREEN-REFACTOR 循环
- 每步验证，失败即停
- 频繁提交

---

### 4. code-reviewer（审查器）
**触发**: 代码实现完成
**输入**: 代码变更
**输出**: `docs/reviews/YYYY-MM-DD-<feature>.md`

**审查维度**:
- 正确性、安全性、性能
- 可维护性、测试覆盖、文档
- 严重/警告/建议三级反馈

---

### 5. tdd-enforcer（TDD 监督）
**触发**: 任何编码任务（嵌入式）
**职责**:
- 强制"测试优先"原则
- 防止"先写代码后补测试"
- 指导 RED-GREEN-REFACTOR 循环

---

### 6. debug-strategist（调试策略）
**触发**: 复杂 Bug 诊断
**流程**: REPRODUCE → ISOLATE → HYPOTHESIZE → TEST → FIX → VERIFY

**输出**: `docs/debug/YYYY-MM-DD-<issue>.md`

---

## 🔄 典型工作流

### 场景 1: 新功能开发
```
用户: "添加用户注册功能"
    ↓
dev-orchestrator 解析需求
    ↓
plan-creator 生成实现计划
    ↓
用户确认计划
    ↓
code-executor 执行开发（内置 tdd-enforcer）
    ↓
code-reviewer 质量审查
    ↓
用户验收
```

### 场景 2: Bug 修复
```
用户: "登录时偶尔报错"
    ↓
debug-strategist 系统诊断
    ↓
定位根因
    ↓
plan-creator 制定修复计划
    ↓
code-executor 执行修复
    ↓
验证修复
```

### 场景 3: 纯代码审查
```
用户: "审查这个 PR"
    ↓
code-reviewer 直接执行
    ↓
审查报告
```

---

## 📋 使用方式

### 在 OpenClaw 中

**直接调用特定 skill**:
```
使用 plan-creator 为[需求]创建实现计划
```

**让 orchestrator 自动协调**:
```
开发[功能]，请协调完整流程
```

**内部实现**:
```python
# orchestrator 内部使用 sessions_spawn
sessions_spawn(
    task="执行 docs/plans/feature.md",
    agent_id="main",
    label="code-executor"
)
```

---

## 💡 与参考源的差异

| 方面 | Superpowers/VoltAgent | 本架构 |
|------|----------------------|--------|
| 数量 | 20+ skills / 100+ agents | 6 core skills |
| 组织 | 按技术栈/领域 | 按工作流阶段 |
| 语言 | 多个语言专家 | 语言无关 |
| 执行 | Claude Code 内置 | sessions_spawn |
| Git 工作流 | 依赖 worktrees | 标准 git flow |

---

## 📁 文件结构

```
skills/
├── dev-orchestrator/SKILL.md      # 元协调器
├── plan-creator/SKILL.md          # 规划
├── code-executor/SKILL.md         # 执行
├── code-reviewer/SKILL.md         # 审查
├── tdd-enforcer/SKILL.md          # TDD
├── debug-strategist/SKILL.md      # 调试
└── README.md                      # 本文件
```

---

## 🚀 扩展建议

如需扩展，优先考虑：
1. **新增阶段**（如 deployment-skill）
2. **细分领域**（如 security-reviewer）
3. **语言模板**（在 code-executor 内添加语言特定提示）

避免：为每种语言/框架创建单独 skill（违背精简原则）

---

*Created for Leo's OpenClaw workspace*  
*Based on obra/superpowers + VoltAgent/awesome-claude-code-subagents*
