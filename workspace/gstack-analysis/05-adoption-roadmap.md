# 采用路线图

## 目标

将 Gstack 的核心设计模式整合到 iFAi，提升多 Agent 协作的效率和质量。

---

## 阶段 1: 基础对齐 ✅

**已完成**：
- Gstack 仓库深度分析
- 9 角色核心行为提取
- 技术机制分析
- 对照映射文档

---

## 阶段 2: 核心模式迁移 🎯（当前）

### 2.1 新增 `review` 子代理

**目标**：实现 Fix-First 代码审查模式

**文件**：`agents/review/SOUL.md`

**核心功能**：
- 0-10 评分系统（安全、架构、性能等维度）
- AUTO-FIX / ASK 分类
- Review Readiness Dashboard

**验收标准**：
- [ ] 能够分析代码 diff
- [ ] 自动修复简单问题
- [ ] 生成结构化审查报告
- [ ] 更新到 Review Readiness Dashboard

---

### 2.2 新增 `plan` 子代理

**目标**：整合计划审查功能

**文件**：`agents/plan/SOUL.md`

**核心功能**：
- 工程可行性审查（技术栈、依赖、风险）
- CEO 视角审查（价值、范围、成功指标）
- 设计审查（UI/UX 完整性）

**验收标准**：
- [ ] 能够读取 Product Spec
- [ ] 多维度评分
- [ ] 生成改进建议
- [ ] 输出标准化 PLAN

---

### 2.3 更新现有子代理交互格式

**目标**：标准化所有子代理的交互格式

**改动文件**：
- `agents/cto/SOUL.md`
- `agents/cro/SOUL.md`
- `agents/coo/SOUL.md`

**新增要求**：
```markdown
## AskUserQuestion Format

**ALWAYS follow this structure for every AskUserQuestion call:**
1. **Re-ground:** State the project, the current task. (1-2 sentences)
2. **Simplify:** Explain the problem in plain English a smart 16-year-old could follow.
3. **Recommend:** `RECOMMENDATION: Choose [X] because [one-line reason]`
4. **Options:** Lettered options: `A) ... B) ... C) ...`
```

**验收标准**：
- [ ] 所有子代理遵循 4 步格式
- [ ] 每次只问一个问题
- [ ] 始终提供推荐选项

---

### 2.4 引入 Completeness Principle

**目标**：培养"完整性优先"的文化

**改动文件**：
- `SOUL.md`（CEO）
- 所有子代理 `SOUL.md`

**核心内容**：
```markdown
## Completeness Principle — Boil the Lake

AI-assisted work makes the marginal cost of completeness near-zero.
When presenting options, always recommend the complete implementation.

**Lake vs. Ocean:**
- Lake = 100% 测试覆盖、完整功能、所有边界情况
- Ocean = 重写整个系统、添加依赖项不控制的功能

**Effort Compression:**
| Task | Human | AI | Compression |
|------|-------|----|-------------|
| Boilerplate | 2 days | 15 min | ~100x |
| Test writing | 1 day | 15 min | ~50x |
| Feature | 1 week | 30 min | ~30x |
```

---

## 阶段 3: 质量基础设施 🔧（未来）

### 3.1 增强 CTO 工作流

**新增功能**：
- Test Coverage Audit（代码路径追踪）
- Test Framework Bootstrap（自动配置测试框架）

**改动文件**：`agents/cto/SOUL.md`

---

### 3.2 标准化发布流程

**新增功能**：
- VERSION 文件管理
- CHANGELOG 自动生成
- 发布门控机制

**改动文件**：`agents/coo/SOUL.md`

---

### 3.3 增强记忆系统

**新增功能**：
- Review Readiness Dashboard 追踪
- 项目级记忆 scope
- 审查历史记录

**改动文件**：`memory/*`

---

## 阶段 4: 高级功能 🚀（未来）

### 4.1 Eval Suites
- AI 生成内容的自动评估
- LLM-as-a-Judge 模式

### 4.2 Browser 自动化增强
- QA 测试工作流
- 视觉回归测试

### 4.3 第三方集成
- Greptile 代码审查
- 其他外部工具

---

## 优先级矩阵

| 功能 | 价值 | 成本 | 优先级 | 阶段 |
|------|------|------|--------|------|
| Fix-First 审查模式 | ⭐⭐⭐⭐⭐ | 中 | P0 | 2.1 |
| 4 步 AskUserQuestion | ⭐⭐⭐⭐⭐ | 低 | P0 | 2.3 |
| Completeness Principle | ⭐⭐⭐⭐⭐ | 低 | P0 | 2.4 |
| 0-10 评分系统 | ⭐⭐⭐⭐⭐ | 低 | P0 | 2.1 |
| plan 子代理 | ⭐⭐⭐⭐ | 中 | P1 | 2.2 |
| Test Coverage Audit | ⭐⭐⭐⭐ | 高 | P1 | 3.1 |
| Review Dashboard | ⭐⭐⭐⭐ | 中 | P1 | 3.3 |
| VERSION/CHANGELOG | ⭐⭐⭐ | 低 | P2 | 3.2 |
| Eval Suites | ⭐⭐⭐ | 高 | P2 | 4.1 |
| Browser QA | ⭐⭐⭐ | 中 | P2 | 4.2 |

---

## 依赖关系

```
2.3 (4 步格式)
    ↓
2.1 (review 子代理) ──┐
    ↓                 │
2.2 (plan 子代理) ────┼→ 3.1 (CTO 增强)
    ↓                 │
2.4 (Completeness) ───┘
    ↓
3.3 (记忆增强)
    ↓
3.2 (发布流程)
    ↓
4.x (高级功能)
```

---

## 下一步行动

### 立即执行（今天）
1. [ ] 为 Leo 呈现 Phase 1 发现摘要
2. [ ] 获取反馈和优先级确认
3. [ ] 创建 `agents/review/` 目录和 `SOUL.md`

### 本周
4. [ ] 实现 `review` 子代理 MVP
5. [ ] 更新 `cto` 子代理交互格式
6. [ ] 在 CEO SOUL.md 中引入 Completeness Principle

### 本月
7. [ ] 创建 `plan` 子代理
8. [ ] 增强记忆系统支持 Review Dashboard
9. [ ] 全面测试新的工作流

---

## 成功指标

| 指标 | 当前 | 目标 | 测量方式 |
|------|------|------|---------|
| 代码审查覆盖率 | - | 100% PR | Review Dashboard |
| 计划审查完整性 | - | 8+ / 10 | 评分记录 |
| 用户满意度 | - | 9+ / 10 | 反馈收集 |
| 返工率 | - | < 10% | 任务追踪 |
