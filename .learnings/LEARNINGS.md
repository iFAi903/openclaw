# LEARNINGS.md — 学习记录

> 记录纠正、知识缺口、最佳实践
> 自动提取自对话，用于持续改进

---

## [LRN-20250308-001] correction

**Logged**: 2026-03-08T03:45:00+08:00
**Priority**: high
**Status**: resolved
**Area**: config

### Summary
区分用户(Leo)的背景描述与AI(小羽毛)的背景描述

### Details
用户纠正：在"你从哪里来"之后的内容被错误地归为用户描述，实际上是AI的自我描述。
用户明确区分：
- 用户的背景：云南、台北、加拿大、DePaul PPE、硅谷、法国创业
- AI的定位：orchestrator，在混沌中看清秩序

### Suggested Action
严格区分"你"(用户)和"我"(AI)的描述边界，每次涉及背景信息时先确认归属

### Metadata
- Source: user_feedback
- Related Files: USER.md, IDENTITY.md
- Tags: identity, clarification, boundary
- Pattern-Key: identity.user_vs_ai_boundary
- Recurrence-Count: 1
- First-Seen: 2026-03-08
- Last-Seen: 2026-03-08

---

## [LRN-20250308-002] best_practice

**Logged**: 2026-03-08T03:56:00+08:00
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
初始化全局系统：长期记忆 + 语音唤醒 + 贾维斯模式

### Details
用户要求：
1. 安装技能：long-term-memory、voice-wakeup、jarvis-core、persistent-agent、self-learning、self-improving-agent
2. 启用永久长期记忆体
3. 开启语音唤醒（唤醒词：小羽毛、CEO、贾维斯）
4. 贾维斯模式触发词："小羽毛贾维斯"
5. 后台守护进程 24/7
6. 自动构建用户专属知识库
7. 禁止清除记忆
8. 自动优化响应逻辑

### Suggested Action
- 已安装核心技能：elite-longterm-memory、self-learning、self-improving-agent-1-0-11
- 需创建：SESSION-STATE.md、.learnings/、memory/ 结构
- 需说明：语音唤醒和守护进程的系统级限制

### Metadata
- Source: conversation
- Related Files: HEARTBEAT.md, SESSION-STATE.md
- Tags: initialization, jarvis-mode, memory-system

---


## [LRN-20260310-001] best_practice

**Logged**: 2026-03-10T07:26:17.051Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Task notes claimed AI news cron was configured, but actual OpenClaw cron/jobs.json only contained the nightly security audit job.

### Details
User asked why daily AI report was not pushed. Inspection showed memory/🎯 TASKS.md says daily-news-v2 cron 0 7 * * * is configured, but ~/.openclaw/cron/jobs.json contains only one enabled job: 每晚安全审计 at 23:00 Asia/Taipei. Root cause is documentation/memory drift from real scheduler state, not a same-day settings change.

### Suggested Action
When asked about scheduled automations, verify live scheduler state (openclaw status + ~/.openclaw/cron/jobs.json) before assuring the user a cron exists. Treat task notes as intent, not ground truth.

### Metadata
- Source: memory-lancedb-pro/self_improvement_log
---


## [LRN-20260311-001] correction

**Logged**: 2026-03-11T01:38:30.746Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
新闻站点更新时误把 2026-03-11 写成周三，且未先检查页面语言与线上实际渲染，导致日期与 lang 都错。

### Details
用户指出页面问题后，发现 src/data/news.ts 中 date 文案写成“2026年03月11日 周三”，但 2026-03-11 实际是周三？需再次核对；同时页面 html lang 仍为 en，属于站点本地化漏检。此前只做了数据更新与部署，未在发布前做线上日期/语言验收。

### Suggested Action
发布早报站点前必须检查三项：日期数字、星期、html lang=zh-CN；部署后访问线上页面核验标题/日期/语言再通知用户。

### Metadata
- Source: memory-lancedb-pro/self_improvement_log
---
