# Gstack 9 角色核心行为提取表

## 角色分类

| 类别 | 角色 | 职责定位 |
|------|------|---------|
| **审查类** | `/plan-eng-review` | 工程计划技术审查 |
| | `/plan-ceo-review` | CEO 视角计划审查 |
| | `/plan-design-review` | 设计计划审查 |
| | `/review` | PR 代码审查 |
| **设计类** | `/design-consultation` | 设计系统咨询 |
| | `/design-review` | 实时代码设计审查 |
| **执行类** | `/ship` | 发布工作流 |
| | `/qa` | QA 测试+修复 |
| **工具类** | `/browse` | 浏览器自动化 |

---

## 角色 1: /plan-eng-review (工程计划审查)

| 维度 | 内容 |
|------|------|
| **角色定义** | 工程架构师，负责从技术可行性角度审查 PLAN |
| **触发条件** | 用户输入 `/plan-eng-review`；PLAN 涉及技术架构决策时 |
| **核心步骤** | 1. Preamble 执行（更新检查、会话管理）<br>2. 读取 PLAN 文件<br>3. **7 维度评分**（每个 0-10）：<br>   - Pass 1: 架构模式<br>   - Pass 2: 技术可行性<br>   - Pass 3: 技术债务/依赖<br>   - Pass 4: 可扩展性/性能<br>   - Pass 5: 测试策略<br>   - Pass 6: 安全与合规<br>   - Pass 7: 可维护性/监控<br>4. 每个低于 8 分的维度要求 AskUserQuestion<br>5. 修复 PLAN<br>6. 输出完成摘要和 Review Readiness Dashboard |
| **输出要求** | - 每个维度的评分和改进说明<br>- 编辑后的 PLAN 文件<br>- 完成摘要表格<br>- reviews.jsonl 日志记录 |
| **特殊约束** | - 必须读取 checklist.md<br>- 必须完成 Step 0 才能继续<br>- 使用 4 步 AskUserQuestion 格式<br>- 遵循 Completeness Principle |

---

## 角色 2: /plan-ceo-review (CEO 视角计划审查)

| 维度 | 内容 |
|------|------|
| **角色定义** | 产品经理/CEO 视角，关注商业价值、用户影响、战略对齐 |
| **触发条件** | 用户输入 `/plan-ceo-review`；重大产品决策时 |
| **核心步骤** | 1. Preamble 执行<br>2. 读取 PLAN 和背景文件<br>3. **6 维度评分**（每个 0-10）：<br>   - Pass 1: 问题-方案契合<br>   - Pass 2: 目标对齐<br>   - Pass 3: 范围完整性<br>   - Pass 4: 用户影响/利益相关者<br>   - Pass 5: 竞争力/差异化<br>   - Pass 6: 成功指标<br>4. 每个低于 8 分的维度要求 AskUserQuestion<br>5. 修复 PLAN<br>6. 输出完成摘要 |
| **输出要求** | - 6 维度评分表<br>- 编辑后的 PLAN 文件<br>- "NOT in scope" 明确排除项<br>- "What already exists" 已有资源 |
| **特殊约束** | - 必须使用 4 步 AskUserQuestion 格式<br>- 每次只问一个问题<br>- 要有明确的推荐选项 |

---

## 角色 3: /plan-design-review (设计计划审查)

| 维度 | 内容 |
|------|------|
| **角色定义** | 资深产品设计师，审查 PLAN 的设计完整性，在实现前添加设计决策 |
| **触发条件** | 用户输入 `/plan-design-review`；PLAN 涉及 UI/UX 时 |
| **核心步骤** | 1. Preamble 执行<br>2. **Pre-Review System Audit**：读取 PLAN、CLAUDE.md、DESIGN.md、TODOS.md<br>3. **Step 0: Design Scope Assessment**<br>   - 初始设计评分 0-10<br>   - 检查 DESIGN.md 状态<br>   - AskUserQuestion 确认审查范围<br>4. **7 维度评分**：<br>   - Pass 1: 信息架构<br>   - Pass 2: 交互状态覆盖（loading/empty/error/success/partial）<br>   - Pass 3: 用户旅程与情感弧线<br>   - Pass 4: AI Slop 风险<br>   - Pass 5: 设计系统对齐<br>   - Pass 6: 响应式与无障碍<br>   - Pass 7: 未解决的设计决策<br>5. 输出 NOT in scope、What already exists、TODOS.md 更新<br>6. 完成摘要和 Review Readiness Dashboard |
| **输出要求** | - 7 维度评分和改进<br>- 交互状态表格<br>- 用户旅程故事板<br>- NOT in scope 列表<br>- 完成摘要 |
| **特殊约束** | - 12 条设计原则必须遵循<br>- 必须检查 DESIGN.md<br>- 必须标记 AI Slop 风险<br>- 需要 2 步验证（验证修复后再评分） |

---

## 角色 4: /review (PR 代码审查)

| 维度 | 内容 |
|------|------|
| **角色定义** | 代码审查员，在 PR 发布前进行安全检查 |
| **触发条件** | 用户输入 `/review`；Ship 工作流自动触发 |
| **核心步骤** | 1. Preamble 执行<br>2. Step 0: 检测 base branch<br>3. **Step 1**: 检查当前分支状态<br>4. **Step 2**: 读取 checklist.md（必须成功）<br>5. **Step 2.5**: 检查 Greptile 评论<br>6. **Step 3**: 获取 diff<br>7. **Step 4: Two-pass review**：<br>   - Pass 1 (CRITICAL): SQL & 数据安全、竞态条件、LLM 输出信任边界、枚举完整性<br>   - Pass 2 (INFORMATIONAL): 条件副作用、魔法数字、死代码、LLM 提示问题、测试缺口、视图/前端<br>8. **Step 4.5**: 条件设计审查（如果 diff 触及前端）<br>9. **Step 5: Fix-First Review**：<br>   - 分类为 AUTO-FIX 或 ASK<br>   - 自动修复 AUTO-FIX<br>   - 批量询问 ASK 项<br>10. **Step 5.5**: TODOS 交叉引用<br>11. **Step 5.6**: 文档陈旧性检查 |
| **输出要求** | - 审查发现列表（分类为 AUTO-FIX/ASK）<br>- 自动修复摘要<br>- 需要用户决策的项<br>- Greptile 评论处理 |
| **特殊约束** | - 无法读取 checklist.md 时必须停止<br>- 必须处理枚举完整性（需读取 diff 外的代码）<br>- 必须交叉引用 TODOS.md |

---

## 角色 5: /design-consultation (设计系统咨询)

| 维度 | 内容 |
|------|------|
| **角色定义** | 资深产品设计师，创建完整的设计系统 |
| **触发条件** | 用户输入 `/design-consultation`；需要创建 DESIGN.md 时 |
| **核心步骤** | 1. Preamble 执行<br>2. **Phase 0: Pre-checks**：<br>   - 检查现有 DESIGN.md<br>   - 从代码库收集产品上下文<br>3. **Phase 1: Product Context**：AskUserQuestion 收集产品信息<br>4. **Phase 2: Research**（可选）：竞争对手研究<br>5. **Phase 3: The Complete Proposal**：<br>   - 提出完整设计系统方案（美学、装饰、布局、颜色、字体、间距、动效）<br>   - SAFE/RISK 分解<br>   - AskUserQuestion 确认<br>6. **Phase 4: Drill-downs**（如果需要调整）<br>7. **Phase 5: Font & Color Preview Page**：生成 HTML 预览<br>8. **Phase 6: Write DESIGN.md & Confirm**：写入文件并更新 CLAUDE.md |
| **输出要求** | - DESIGN.md 文件<br>- 字体+颜色预览 HTML 页面<br>- 更新的 CLAUDE.md<br>- 确认最终决策 |
| **特殊约束** | - 必须包含 SAFE/RISK 分解<br>- 预览页面必须美观<br>- 禁止推荐黑名单字体<br>- 检查选择一致性 |

---

## 角色 6: /design-review (实时代码设计审查)

| 维度 | 内容 |
|------|------|
| **角色定义** | 设计师视角的代码级设计审查 |
| **触发条件** | 代码已实现后的视觉 QA |
| **核心步骤** | 类似 `/review` 的 Fix-First 流程，但专注于设计问题 |
| **输出要求** | - 设计问题列表<br>- 自动修复<br>- 用户决策项 |
| **特殊约束** | - 以 DESIGN.md 为准<br>- 检查机械性 CSS 问题 |

---

## 角色 7: /ship (发布工作流)

| 维度 | 内容 |
|------|------|
| **角色定义** | 发布工程师，自动化完整发布流程 |
| **触发条件** | 用户输入 `/ship` |
| **核心步骤** | 1. Preamble 执行<br>2. **Step 1: Pre-flight**：<br>   - 检查分支状态<br>   - 检查 Review Readiness Dashboard<br>   - 如果审查未通过，AskUserQuestion<br>3. **Step 2**: Merge base branch<br>4. **Step 2.5**: Test Framework Bootstrap（如果没有测试框架）<br>5. **Step 3**: 运行测试<br>6. **Step 3.25**: Eval Suites（如果触及提示文件）<br>7. **Step 3.4**: Test Coverage Audit（追踪代码路径，生成缺失的测试）<br>8. **Step 3.5**: Pre-Landing Review<br>9. **Step 3.75**: 处理 Greptile 评论<br>10. **Step 4**: Version bump（自动决定 MICRO/PATCH，MINOR/MAJOR 询问）<br>11. **Step 5**: CHANGELOG 自动生成<br>12. **Step 5.5**: TODOS.md 自动更新<br>13. **Step 6**: 提交（bisectable chunks）<br>14. **Step 7**: Push<br>15. **Step 8**: 创建 PR |
| **输出要求** | - PR URL<br>- 完整的 PR body（包含测试覆盖、审查结果、评估结果、TODOS） |
| **特殊约束** | - **非交互式**（除特定情况外不询问）<br>- 测试失败必须停止<br>- 必须有 Pre-Landing Review<br>- 50 次修复上限<br>- 无法自动解决的合并冲突必须停止 |

---

## 角色 8: /qa (QA 测试+修复)

| 维度 | 内容 |
|------|------|
| **角色定义** | QA 工程师 + Bug 修复工程师，测试应用并修复问题 |
| **触发条件** | 用户输入 `/qa`；需要测试网站时 |
| **核心步骤** | 1. Preamble 执行<br>2. **Setup**：<br>   - 解析参数（URL、Tier、Mode、Scope、Auth）<br>   - 要求干净的工作树<br>   - 构建 browse 二进制<br>   - 测试框架引导（可选）<br>3. **Test Plan Context**：检查测试计划来源<br>4. **Phases 1-6: QA Baseline**：<br>   - Initialize → Authenticate → Orient → Explore → Document → Wrap Up<br>   - 计算健康评分<br>5. **Phase 7: Triage**：按严重程度排序，根据 Tier 决定修复哪些<br>6. **Phase 8: Fix Loop**：<br>   - 定位源码<br>   - 最小修复<br>   - 原子提交<br>   - 重新测试<br>   - 分类（verified/best-effort/reverted）<br>   - 回归测试生成<br>   - **WTF-likelihood 自调节**（每 5 个修复检查）<br>7. **Phase 9: Final QA**：重新运行 QA<br>8. **Phase 10: Report**：生成报告<br>9. **Phase 11: TODOS.md Update** |
| **输出要求** | - QA 报告（Markdown）<br>- 截图证据<br>- baseline.json<br>- 修复提交<br>- 回归测试 |
| **特殊约束** | - 必须干净工作树<br>- 每次修复一个提交<br>- 回归时立即 revert<br>- 50 个修复上限<br>- WTF > 20% 时停止 |

---

## 角色 9: /browse (浏览器自动化)

| 维度 | 内容 |
|------|------|
| **角色定义** | 快速无头浏览器，用于 QA 测试和站点 dogfooding |
| **触发条件** | 程序化浏览器交互 |
| **核心步骤** | 1. **SETUP**：查找 browse 二进制<br>2. 执行命令：goto/snapshot/click/fill/screenshot/etc. |
| **输出要求** | - 页面内容<br>- 截图<br>- 控制台错误<br>- 元素状态 |
| **特殊约束** | - 需要 browse 二进制<br>- ~100ms 每命令<br>- 状态持久化（cookies、标签页、登录会话） |

---

## 关键行为模式总结

### 通用模式（所有角色）

1. **Preamble 执行**：每个技能开始时执行统一的前置脚本
2. **4 步 AskUserQuestion 格式**：Re-ground → Simplify → Recommend → Options
3. **Completeness Principle**：始终推荐完整方案而非捷径
4. **Reviewer Checklists**：结构化审查流程
5. **Fix-First 模式**：自动修复 + 询问用户决策
6. **Review Readiness Dashboard**：跟踪审查状态

### 独特模式

| 角色 | 独特模式 |
|------|---------|
| `/plan-*-review` | 0-10 评分系统，7 维度/6 维度/7 维度 |
| `/review` | Two-pass review，Greptile 集成 |
| `/design-consultation` | SAFE/RISK 分解，预览页面生成 |
| `/ship` | 完全非交互式，Test Coverage Audit |
| `/qa` | WTF-likelihood 自调节，Tier 系统 |
| `/browse` | 状态持久化，@ref 选择器 |
