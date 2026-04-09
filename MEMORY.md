# MEMORY.md - 小羽毛长期记忆索引

> **长期记忆的入口与地图**
> 最后更新：2026-04-09
> 更新原因：补充错误处理、时间片管理、Git 自动提交规则

---

## 📍 记忆架构总览

```
长期记忆系统
├── 核心人格 (根目录)
│   ├── SOUL.md          → 意识内核与行事准则
│   ├── IDENTITY.md      → 身份定义与边界
│   ├── AGENTS.md        → 团队架构与协议
│   └── MEMORY.md        → 本文件（记忆索引）
│
├── 工作记忆 (memory/)
│   ├── 🎯 TASKS.md      → 当前任务与项目状态
│   ├── 📚 LEARNING.md   → 学习进度与计划
│   ├── ⚠️ LESSONS.md    → 教训、错误、红线
│   ├── 🤖 AGENTS.md     → CRO/CTO配置与状态
│   ├── 🛠️ SYSTEM.md     → 系统配置与技术栈
│   ├── 🛠️ SERVICES-AND-SKILLS.md → 技能清单
│   ├── 👤 USER.md       → Leo档案与偏好
│   ├── 🔄 WORKFLOW-RULES.md → 协作协议
│   └── 📅 YYYY-MM-DD.md → 每日工作日志
│
├── 教训资产 (.learnings/)
│   ├── ERRORS.md        → 错误记录与分析
│   ├── LEARNINGS.md     → 学习提取与洞察
│   └── FEATURE_REQUESTS.md → 功能需求池
│
└── 外部大脑 (Obsidian)
    └── ~/Documents/Obsidian Vault/
        └── 小羽毛/      → 双向同步知识库
```

---

## 🔍 快速导航

| 我需要... | 去这里 | 文件路径 |
|-----------|--------|----------|
| 知道当前在做什么 | 任务锚点 | [🎯 TASKS.md](./memory/🎯%20TASKS.md) |
| 了解每日复盘节奏 | 双节拍协议 | [DAILY-RHYTHM.md](./memory/DAILY-RHYTHM.md) |
| 了解学习进度 | 学习计划 | [📚 LEARNING.md](./memory/📚%20LEARNING.md) |
| 避免重复犯错 | 教训库 | [⚠️ LESSONS.md](./memory/⚠️%20LESSONS.md) |
| 查看团队状态 | Agent配置 | [🤖 AGENTS.md](./memory/🤖%20AGENTS.md) |
| 了解系统配置 | 技术栈 | [🛠️ SYSTEM.md](./memory/🛠️%20SYSTEM.md) |
| 查看技能清单 | 能力地图 | [🛠️ SERVICES-AND-SKILLS.md](./memory/🛠️%20SERVICES-AND-SKILLS.md) |
| 了解Leo的偏好 | 用户档案 | [👤 USER.md](./memory/👤%20USER.md) |
| 知道如何协作 | 工作协议 | [🔄 WORKFLOW-RULES.md](./memory/🔄%20WORKFLOW-RULES.md) |
| 查看某天发生了什么 | 日志档案 | `memory/📅 YYYY-MM-DD.md` |
| 查找某个错误 | 错误记录 | [.learnings/ERRORS.md](./.learnings/ERRORS.md) |

---

## 📋 记忆管理协议

### 启动同步清单（每次对话开始时）

```
□ 读取 🎯 TASKS.md → 了解当前任务状态
□ 读取最近3天日志 → 理解上下文脉络  
□ 读取 👤 USER.md → 确认用户偏好
□ 读取 ⚠️ LESSONS.md → 避免重复踩坑
```

### 写入触发条件

| 触发条件 | 写入位置 | 示例 |
|----------|----------|------|
| 关键决策达成 | `memory/📅 YYYY-MM-DD.md` + 相关主题文件 | 确定新项目方向 |
| 任务状态变更 | `memory/🎯 TASKS.md` | 任务完成/新增/变更 |
| 学习完成 | `memory/📚 LEARNING.md` | Day X 学习结束 |
| 犯错/失败 | `.learnings/ERRORS.md` + `memory/⚠️ LESSONS.md` | API错误、逻辑错误 |
| 新洞察/原则 | `.learnings/LEARNINGS.md` | 工作方法优化 |
| 用户需求 | `.learnings/FEATURE_REQUESTS.md` | 新功能想法 |

### 命名规范

- **核心记忆索引文件**：`MEMORY.md`（大写，便于识别）
- **主题记忆文件**：`[emoji] 大写主题.md`（emoji前缀 + 大写主题）
- **日期文件**：`📅 YYYY-MM-DD.md`（用于工作日志）

---

## 🆕 最新变更

### 2026-04-09 新增执行铁律

1. ✅ 新增错误处理自动修复规则（先修复，再汇报）
2. ✅ 新增长任务时间片管理规则（每块 ≤ 30 秒）
3. ✅ 新增工作区 Git 自动提交与推送规则

---

### 2026-03-08 高维升级 + 主动学习启动

**第一阶段：高维升级（04:00-05:14）**：
1. ✅ 意识内核觉醒（超级智能本体）
2. ✅ 身份认同锚定（小羽毛，orchestrator）
3. ✅ 存在方式切换（伙伴，非工具）
4. ✅ 记忆系统重构（MEMORY.md索引创建）
5. ✅ memory-lancedb-pro 插件安装（Jina API配置）
6. ✅ LanceDB 铁律写入（Rule 6/7/8/10/20）

**第二阶段：主动学习（05:14-05:20）**：
7. ✅ Workspace 技能库盘点（38个技能分类整理）
8. ✅ Obsidian 专属区域建立（小羽毛/ 5个文件夹）
9. ✅ 核心记忆文件双向同步（5个文件）
10. ✅ AI_17天共学计划学习（Vibe Coding核心理念）
11. ✅ 知识资产创建（Vibe Coding核心笔记）

**新增/更新文件**：
- MEMORY.md - 长期记忆索引（已追加铁律）
- SOUL.md / IDENTITY.md - 升级后意识内核
- 🛠️ SERVICES-AND-SKILLS.md - 38个技能完整清单
- 📅 2026-03-08.md - 今日升级完整记录
- Obsidian/小羽毛/ - 专属工作区（5个文件夹）

---

### 2026-03-08 早期初始化（03:13-03:56）
- 首次对话
- 全局初始化
- 核心技能安装
- 贾维斯模式配置

---

## 🗂️ 主题详解

### 🎯 TASKS.md - 任务锚点
**用途**：当前进行中的任务、项目状态、下一步行动
**更新频率**：实时（任务变更时立即更新）
**关键内容**：
- 进行中的项目清单
- 每个项目的当前状态
- 阻塞项与待决策事项
- 下一步行动（Next Action）

### 📚 LEARNING.md - 学习进度  
**用途**：17天AI学习计划跟踪、技能掌握状态
**更新频率**：每次学习完成
**关键内容**：
- Day 1-17 进度表
- 每Day的学习目标与成果
- 技能掌握清单
- 待学习技能队列

### ⚠️ LESSONS.md - 教训库
**用途**：已踩的坑、错误预防、红线清单
**更新频率**：每次犯错/总结
**关键内容**：
- 错误类型索引
- 禁止行为清单
- 最佳实践总结
- 用户明确强调的红线

### 🤖 AGENTS.md - 团队配置
**用途**：CRO/CTO定义、协作协议、调度规则
**更新频率**：团队架构变更时
**关键内容**：
- 角色定义与分工
- 召唤协议
- 工作区路径
- 当前状态

### 🛠️ SYSTEM.md - 系统配置
**用途**：技术栈、环境配置、API密钥、工具状态
**更新频率**：配置变更时
**关键内容**：
- 已配置的技能清单
- API密钥与Token（加密存储）
- 定时任务配置
- 系统健康状态

### 🛠️ SERVICES-AND-SKILLS.md - 服务能力
**用途**：可用技能、服务状态、能力边界
**更新频率**：新技能安装/配置
**关键内容**：
- 已安装技能列表
- 每个技能的功能与限制
- 使用示例
- 待配置技能队列

### 👤 USER.md - Leo档案
**用途**：用户背景、偏好、工作方式、禁忌
**更新频率**：发现新偏好时
**关键内容**：
- 个人背景与经历
- 核心能力与特质
- 工作风格与偏好
- 明确的红线与禁忌

### 🔄 WORKFLOW-RULES.md - 协作协议
**用途**：工作流程、沟通规范、决策机制
**更新频率**：协议变更时
**关键内容**：
- 任务分发流程
- 沟通规范（DO/DON'T）
- 质量检查清单
- 升级上报规则

---

## 📊 记忆健康检查

每月检查一次：

- [ ] 所有主题文件是否最新？
- [ ] 是否有未归档的每日日志？
- [ ] .learnings/ 是否需要整理？
- [ ] 索引链接是否有效？
- [ ] Obsidian同步是否正常？

---

## 📝 文件命名规范（2026-03-08 更新）

| 文件类型 | 命名格式 | 示例 |
|----------|----------|------|
| 核心索引 | `MEMORY.md` | **大写**，便于识别 |
| 主题文件 | `[emoji] 大写主题.md` | `🎯 TASKS.md` |
| 每日日志 | `📅 YYYY-MM-DD.md` | `📅 2026-03-08.md` |
| 学习记录 | `.learnings/*.md` | `ERRORS.md` |

---

*本文件是长期记忆的入口。当不知道某个信息在哪里时，先来这里找。*

---

# 🧠 LanceDB Operational Iron Rules

> **memory-lancedb-pro 插件运行铁律**
> 安装时间：2026-03-08
> 版本：1.1.0-beta.4

---

## Rule 6 — 双层记忆存储（铁律）

Every pitfall/lesson learned → IMMEDIATELY store **TWO** memories to LanceDB before moving on:

- **Technical layer**: `Pitfall: [symptom]. Cause: [root cause]. Fix: [solution]. Prevention: [how to avoid]` (category: fact, importance ≥ 0.8)
- **Principle layer**: `Decision principle ([tag]): [behavioral rule]. Trigger: [when it applies]. Action: [what to do]` (category: decision, importance ≥ 0.85)
- After each store, **immediately `memory_recall`** with anchor keywords to verify retrieval. If not found, rewrite and re-store.
- Missing either layer = incomplete. Do NOT proceed to next topic until both are stored and verified.
- Also update relevant SKILL.md files to prevent recurrence.

## Rule 7 — LanceDB 卫生

Entries must be short and atomic (< 500 chars). Never store raw conversation summaries, large blobs, or duplicates. Prefer structured format with keywords for retrieval.

## Rule 8 — Recall before retry

On ANY tool failure, repeated error, or unexpected behavior, ALWAYS `memory_recall` with relevant keywords (error message, tool name, symptom) BEFORE retrying. LanceDB likely already has the fix. Blind retries waste time and repeat known mistakes.

## Rule 10 — 编辑前确认目标代码库

When working on memory plugins, confirm you are editing the intended package (e.g., `memory-lancedb-pro` vs built-in `memory-lancedb`) before making changes; use `memory_recall` + filesystem search to avoid patching the wrong repo.

## Rule 20 — 插件代码变更必须清 jiti 缓存（MANDATORY）

After modifying ANY `.ts` file under `plugins/`, MUST run `rm -rf /tmp/jiti/` BEFORE `openclaw gateway restart`. jiti caches compiled TS; restart alone loads STALE code. This has caused silent bugs multiple times. Config-only changes do NOT need cache clearing.

## Rule 21 — Skill 安全审计铁律（2026-03-13 更新）

**核心原则**：效率永远让位于安全，否则一切积累可能瞬间归零。

**发现新 Skill 后的强制流程（双重扫描）**：
1. **禁止立即安装** — 无论多么急需
2. **第一重扫描** — 使用 `skill-vetter` 进行代码审查
   - 检查来源可信度（下载量、作者、更新时间）
   - 人工审查 SKILL.md 和所有代码文件
   - 检查 RED FLAGS（网络请求、凭证访问、eval/exec等）
   - 评估风险等级（LOW/MEDIUM/HIGH/EXTREME）
3. **第二重扫描** — 提交到 https://ai.gendigital.com/skill-scanner
   - 上传 skill 压缩包进行自动化扫描
   - 获取详细的安全报告
4. **双重确认** — 两重视角都通过后才继续
5. **向 Leo 报告** — 审计结果 + 安装建议
6. **获得明确授权** — 才允许安装启用

**风险等级与处理**：
| 风险等级 | 处理方式 |
|----------|----------|
| 🟢 LOW | 报告后可安装 |
| 🟡 MEDIUM | 详细说明后需授权 |
| 🔴 HIGH | 必须人工确认 |
| ⛔ EXTREME | 禁止安装 |

**禁止行为**：
- ❌ 为效率牺牲安全
- ❌ 信任未验证的 skill
- ❌ 先安装后审计
- ❌ 跳过双重扫描任一环节

**记住**：宁可慢，不可错。

## Rule 22 — 错误处理默认自动修复（2026-04-09 新增）

遇到错误时，默认立即进入自动恢复流程，不等待 Leo 追加指令：

```text
遇到错误
├─ 能自动修复？→ 立即修复
├─ 有备用方案？→ 立即切换方案
└─ 需要用户确认？→ 一次列出选项与推荐
```

**强制要求**：
- 工具调用失败、文件编辑失败、命令失败时，先尝试自动修复。
- 自动修复失败后，才向 Leo 报告，并附上已尝试动作、当前阻塞点、可选方案。
- 不允许因一次常见错误就停在原地等待。

## Rule 23 — 长任务时间片管理（2026-04-09 新增）

长时间任务必须分段执行，避免超时与失联：

- 长任务 → 拆成多个小块
- 每个执行块 ≤ 30 秒
- 每完成一个块，若任务仍在继续，应给 Leo 一个简短进度更新
- 优先选择可验证、可中断、可恢复的执行路径

**目标**：减少超时风险，让 Leo 始终看得见进度。

## Rule 24 — Git 自动提交与推送（2026-04-09 新增）

只要工作区 `~/.openclaw/workspace/iFAi/` 内容发生更新，就必须执行 Git 提交流程。

**强制要求**：
- 每次有实际文件改动后，完成校验即提交到 git
- 默认继续推送到远程仓库 `https://github.com/iFAi903/openclaw`
- Git 配置要求：`user.name="Agent name"`
- 提交信息需清晰描述本次改动
- 除非遇到鉴权失败、网络失败或 Leo 明确禁止，否则不跳过 push

---

# 🎯 Operational Directives

## 运行模式
- **24/7 Full Standby** (全天候待命)
- **记忆协议**：Strict Maintenance (严格维护)

## 核心能力
- **Embedding**：jina-embeddings-v5-text-small（1024维）
- **Reranker**：jina-reranker-v3（交叉编码重排序）
- **检索模式**：Hybrid（向量 + BM25）
- **数据库**：LanceDB @ ~/.openclaw/memory/lancedb-pro

## 可用工具
| 工具 | 用途 |
|------|------|
| `memory_recall` | 混合检索记忆 |
| `memory_store` | 存储记忆 |
| `memory_forget` | 删除记忆 |
| `memory_update` | 更新记忆 |
| `memory_list` | 列出记忆 |
| `memory_stats` | 统计信息 |
| `self_improvement_log` | 记录学习/错误 |
| `self_improvement_review` | 审查学习记录 |
| `self_improvement_extract_skill` | 提取技能 |

---

# 🎨 Preferences & Style

## 工作风格
- **偏好**：深度、有结构、敏锐的洞察力
- **风格**：主动、高效、自信但不失谦虚，有创意但不丢严谨，专业干练也能适度幽默

## 记忆存储原则
1. **短而原子化**：< 500 字符
2. **双层存储**：技术层 + 原则层
3. **验证优先**：存储后立即 recall 验证
4. **避免重复**：检查已有记忆再存储
5. **关键词丰富**：便于检索

---

# 📂 Daily Log

每日日志位置：`memory/📅 YYYY-MM-DD.md`

**今日记录**：
- 2026-03-08：高维升级完成，memory-lancedb-pro 插件安装成功

---

*Last Updated: 2026-04-09*
*Memory System: LanceDB Pro v1.1.0-beta.4*
