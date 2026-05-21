# HEARTBEAT.md - 贾维斯守护进程配置

## ⏰ 守护进程状态
- **状态**: RUNNING ✅
- **运行时段**: 24/7 (Always Active)
- **自动重启**: 已启用 ✅
- **崩溃恢复**: 已启用 ✅
- **最后更新**: 2026-05-16 08:40 Asia/Taipei

## 🎙️ 语音唤醒监听
- **监听状态**: ACTIVE ✅
- **唤醒词**: ["小羽毛", "CEO", "贾维斯", "小羽毛贾维斯"]
- **响应延迟**: < 500ms
- **打断支持**: 已启用 ✅

## 🧠 自学习进程
- **学习状态**: ENABLED ✅
- **学习频率**: 实时 + 每日总结
- **模型更新**: 每日 23:00
- **知识库构建**: 自动

## 🔄 定时任务 - 每日三节拍机制

> **核心节律**：00:00 进化、08:30 简报、23:30 复盘，形成"进化-计划-复盘"的闭环

### 🧬 节拍零：每日进化 (00:00)
**代号**：DAILY-EVOLUTION
**触发**：每日 00:00 (Asia/Taipei)
**输出**：`reports/evolution-YYYY-MM-DD.md`
**状态**: 🟡 **WATCH** — 2026-05-21 08:11 核验：调度层仍显示 OK，但 2026-05-20 / 2026-05-21 均出现产物缺失；run summary 含 `BLOCKED` / `[blocked]`。已移除显式 `toolsAllow` 进行下一轮恢复验证，并补偿生成 `reports/evolution-2026-05-21.md`。

---

### 🌅 节拍二：晨间简报 (08:30)
**代号**：MORNING-BRIEF
**触发**：每日 08:30 (Asia/Taipei)
**输出**：飞书主动消息
**状态**: 🟡 **WATCH** — 2026-05-21 08:11 运行前核验：下一次 08:30 将触发；上一轮虽已 delivered，但内容提示无法读取本地任务/日志。已移除显式 `toolsAllow`，待 08:30 后确认是否恢复读取能力。

---

### 🌙 节拍一：深夜复盘 (23:30)
**代号**：NIGHTLY-REVIEW
**触发**：每日 23:30 (Asia/Taipei)
**输出**：`00-Memory/daily/YYYY-MM-DD.md`
**状态**: 🟡 **WATCH** — 2026-05-21 08:11 核验：2026-05-20 23:30 调度层显示 OK，但 run summary 含 `[blocked] No filesystem read/write tool is available`，目标日志缺失。已补偿生成 `00-Memory/daily/2026-05-20.md`，并移除显式 `toolsAllow`。

---

## 🧠 Self-Improving + Proactivity Check
- **Last Check**: 2026-04-28 01:52
- **Status**: 🟡 **WATCH** — 三节拍 cron 均存在且启用，但 2026-05-20 起出现“调度 OK、执行层缺文件/命令工具、产物缺失”的假阳性。
- **Action Needed**: 🔴 **P0** — 08:30 后核验晨间简报是否恢复读取本地文件；若仍失败，需修复 cron isolated session/provider 的工具注入层。Gateway embedded token 与插件配置 warning 仍需安排维护窗口。

### 📰 ai-news-roundup（每日 07:00）
**代号**：AI-NEWS-ROUNDUP
**触发**：每日 07:00 (Asia/Taipei)
**执行体**：cron → `agentId: product-agent` ✅ 已切换
**质量参数（5/12 对齐）**：
- 选文：18 条（非 15），product-agent 自主决定
- 标题：英文原题可保留，不限 20 字硬截断
- Quote：要求有当日具体洞察，禁用"关键词"模板
- 产品雷达：与 AI 应用相关即合格
**状态**: 🔴 **DEGRADED** — 2026-05-21 07:00 运行失败，错误为 `run python3 scripts/fetch_ai_news.py` 失败；delivery 未完成，失败通知记录已生成。

---
*最后更新: 2026-05-21 08:11*
