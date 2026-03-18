# Gstack → iFAi 对照映射文档

## 1. 概念对照表

| Gstack 概念 | iFAi 对应概念 | 状态 | 说明 |
|------------|--------------|------|------|
| SKILL.md | agents/{role}/SOUL.md | ✅ 已存在 | 类似的角色定义文件 |
| `name` (YAML) | `agents/{role}/` 目录名 | ✅ 可映射 | kebab-case vs 缩写 |
| `version` | Git 版本历史 | ⚠️ 可扩展 | 文件级版本 vs 仓库级 |
| `allowed-tools` | 子代理权限继承 | ⚠️ 需设计 | Gstack 显式声明，iFAi 隐式 |
| Slash Command | sessions_spawn | ⚠️ 可整合 | 两种调用方式 |
| Preamble | 会话初始化 | ⚠️ 需设计 | Gstack 统一前置脚本 |
| Conductor | Pi Sub-agents | ⚠️ 需评估 | 不同并行模型 |
| Git Worktrees | 单实例多会话 | ⚠️ 需评估 | 隔离级别差异 |
| `~/.gstack/` | `memory_*` 工具 | ⚠️ 需整合 | 文件 vs 向量数据库 |
| reviews.jsonl | memory_recall/list | ⚠️ 需设计 | 结构化日志 vs 语义检索 |
| gstack-config | memory_store/update | ⚠️ 需设计 | KV 配置 vs 向量记忆 |
| TODOS.md | `memory/🎯 TASKS.md` | ✅ 已存在 | 任务追踪 |
| Completeness Principle | SOUL.md 价值观 | ⚠️ 需强化 | 可纳入文化 |
| Fix-First 模式 | 无明确对应 | ❌ 缺失 | 重要的工作流模式 |
| Review Readiness Dashboard | 无明确对应 | ❌ 缺失 | 审查状态追踪 |
| 0-10 评分系统 | 无明确对应 | ❌ 缺失 | 可复用的评估框架 |
| Test Coverage Audit | 无明确对应 | ❌ 缺失 | 重要的质量机制 |
| browse CLI | browser/canvas 工具 | ✅ 已存在 | 类似功能 |
| Test Framework Bootstrap | 无明确对应 | ❌ 缺失 | 自动测试框架配置 |

## 2. 可直接复用的模式

### 2.1 高价值、低改动成本

| 模式 | 价值 | 实现建议 |
|------|------|---------|
| **Fix-First 审查模式** | ⭐⭐⭐⭐⭐ | 新增 `review` 角色，实现 AUTO-FIX/ASK 分类 |
| **0-10 评分系统** | ⭐⭐⭐⭐⭐ | 所有审查角色标准化评分 |
| **AskUserQuestion 4 步格式** | ⭐⭐⭐⭐⭐ | 更新所有子代理的交互格式 |
| **Completeness Principle** | ⭐⭐⭐⭐⭐ | 纳入 SOUL.md 文化 |
| **Review Readiness Dashboard** | ⭐⭐⭐⭐ | 新增 memory 类别追踪审查状态 |
| **YAML Frontmatter 模板** | ⭐⭐⭐⭐ | 标准化 SKILL.md 格式 |
| **Preamble 会话管理** | ⭐⭐⭐ | 可选，用于会话追踪 |

### 2.2 中等价值、中等改动成本

| 模式 | 价值 | 实现建议 |
|------|------|---------|
| **Test Coverage Audit** | ⭐⭐⭐⭐ | 整合到 CTO 工作流 |
| **Test Framework Bootstrap** | ⭐⭐⭐⭐ | 新增 `bootstrap` 角色 |
| **Greptile 集成** | ⭐⭐⭐ | 可选的第三方集成 |
| **Eval Suites** | ⭐⭐⭐ | 用于 AI 生成内容的评估 |
| **VERSION + CHANGELOG 自动化** | ⭐⭐⭐ | 整合到发布流程 |

## 3. 需要改造的部分

### 3.1 架构差异

| Gstack | iFAi | 改造方案 |
|--------|------|---------|
| Git Worktrees 并行 | Pi Sub-agents 串行 | 评估是否需要并行；如需要，使用 `sessions_spawn` 并行调用 |
| 文件系统存储 | 向量数据库 | 保持向量数据库为主，特定场景使用文件（如 reviews.jsonl） |
| 项目级 `.gstack/` | 全局 `memory/` | 在 memory 中增加 scope 字段区分项目 |
| Claude Code CLI | OpenClaw 平台 | API 适配 |

### 3.2 工作流差异

| Gstack 工作流 | iFAi 对应 | 改造方案 |
|--------------|----------|---------|
| `/plan-eng-review` → `/plan-ceo-review` → `/plan-design-review` | CEO 统一分发 | 保留 CEO 分发，但增加 `plan` 角色做标准化审查 |
| `/review` 阻塞 `/ship` | 无明确对应 | 新增发布前的审查门控 |
| `/qa` 自动修复 | 无明确对应 | QA 模式可以修复并提交 |
| `/ship` 完全自动化 | CEO 审核后发送 | 保留 CEO 最终审核，但标准化 Ship 流程 |

### 3.3 权限模型

| Gstack | iFAi | 改造方案 |
|--------|------|---------|
| `allowed-tools` 显式声明 | 权限继承 | 考虑在子代理中增加工具白名单配置 |
| 技能级权限控制 | 会话级权限 | 在 `sessions_spawn` 时传递权限限制 |

## 4. iFAi 现有优势（保留）

| 特性 | 说明 |
|------|------|
| **CEO 统一调度** | 比 Slash Command 更符合 Pi 架构 |
| **向量记忆** | 比文件系统更灵活的语义检索 |
| **中文支持** | Gstack 主要是英文 |
| **SOUL.md 人设** | 比 SKILL.md 更丰富的角色定义 |
| **Feishu 集成** | 已集成的消息渠道 |
| **Skill 生态系统** | 丰富的第三方技能 |

## 5. 整合路线图

### Phase 1: 基础对齐（已完成）
- ✅ 深度分析 Gstack 架构
- ✅ 提取核心设计模式
- ✅ 创建对照映射

### Phase 2: 核心模式迁移（建议）
1. **新增 `review` 角色**
   - 实现 Fix-First 模式
   - 0-10 评分系统
   - Review Readiness Dashboard

2. **新增 `plan` 角色**
   - 整合 plan-eng/ceo/design-review 的功能
   - 标准化计划审查流程

3. **更新所有子代理**
   - 采用 4 步 AskUserQuestion 格式
   - 纳入 Completeness Principle

### Phase 3: 质量基础设施（可选）
4. **增强 CTO 工作流**
   - 添加 Test Coverage Audit
   - Test Framework Bootstrap

5. **标准化发布流程**
   - VERSION + CHANGELOG 自动化
   - 发布门控机制

### Phase 4: 高级功能（未来）
6. **Eval Suites** - AI 生成内容评估
7. **Greptile 集成** - 第三方审查集成
8. **browse 工具增强** - 浏览器自动化

## 6. 风险与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| 过度工程化 | 高 | 中 | 优先高价值低成本的改进 |
| 文化冲突 | 中 | 高 | Completeness Principle 需渐进引入 |
| 性能问题 | 低 | 中 | 评估并行方案的必要性 |
| 用户学习成本 | 中 | 中 | 保留熟悉的 CEO 调度模式 |

## 7. 关键决策点

### 决策 1: 是否采用 Git Worktrees 并行模型？

**建议**: 暂不采用
- iFAi 的 Pi 架构更适合子代理模型
- 当前任务复杂度不需要目录级隔离
- 保持简单，如有需要再扩展

### 决策 2: 如何整合文件系统存储？

**建议**: 混合模式
- 继续使用 `memory_*` 工具作为主要存储
- 特定场景使用文件（reviews.jsonl、TODOS.md）
- 增加 memory scope 字段区分项目

### 决策 3: 是否保留 Slash Command？

**建议**: 整合但不替代
- 保留 CEO 统一调度作为主要模式
- Slash Command 作为快捷方式（如 Leo 熟悉后）
- 两者底层调用相同的子代理
