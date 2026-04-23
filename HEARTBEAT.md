# HEARTBEAT.md - 贾维斯守护进程配置

## ⏰ 守护进程状态
- **状态**: RUNNING ✅
- **运行时段**: 24/7 (Always Active)
- **自动重启**: 已启用 ✅
- **崩溃恢复**: 已启用 ✅
- **最后更新**: 2026-04-23 14:50 Asia/Taipei

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

> **核心节律**：00:00 进化、23:30 复盘、08:30 简报，形成“进化-复盘-计划”的闭环

### 🧬 节拍零：每日进化 (00:00)
**代号**：DAILY-EVOLUTION
**触发**：每日 00:00 (Asia/Taipei)
**输出**：`reports/evolution-YYYY-MM-DD.md`
**状态**: ✅ 正常 (last run 19h ago, status=ok)

---

### 🌙 节拍一：深夜复盘 (23:30)
**代号**：NIGHTLY-REVIEW
**触发**：每日 23:30 (Asia/Taipei)
**输出**：`memory/📅 YYYY-MM-DD.md`
**状态**: ⏳ 今日 23:30 触发（尚未到达）

---

### 🌅 节拍二：晨间简报 (08:30)
**代号**：MORNING-BRIEF
**触发**：每日 08:30 (Asia/Taipei)
**输出**：飞书/Telegram 主动消息
**状态**: ✅ 正常 (last run 10h ago, status=ok)

---

## 🧠 Self-Improving + Proactivity Check
- **Last Check**: 2026-04-23 14:50
- **Status**: All 3 beats recovered. No failures today.

---
*最后更新: 2026-04-23 (all 3 beats OK)*
