# HEARTBEAT.md - 贾维斯守护进程配置

## ⏰ 守护进程状态
- **状态**: RUNNING ✅
- **运行时段**: 24/7 (Always Active)
- **自动重启**: 已启用 ✅
- **崩溃恢复**: 已启用 ✅
- **最后更新**: 2026-05-15 19:40 Asia/Taipei

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
**状态**: ✅ **OK** — 2026-04-28 01:45 手动实跑成功，已生成 `reports/evolution-2026-04-28.md`。已切换为 gpt-5.5、light-context、轻量守护 prompt、no-deliver。

---

### 🌅 节拍二：晨间简报 (08:30)
**代号**：MORNING-BRIEF
**触发**：每日 08:30 (Asia/Taipei)
**输出**：飞书主动消息
**状态**: ✅ **OK** — 2026-04-28 01:47 手动实跑成功；测试时临时 no-deliver，随后已恢复为 `announce -> feishu:user:ou_f804aeb5aa82fc47dca4830476a6e75d`。

---

### 🌙 节拍一：深夜复盘 (23:30)
**代号**：NIGHTLY-REVIEW
**触发**：每日 23:30 (Asia/Taipei)
**输出**：`00-Memory/daily/YYYY-MM-DD.md`
**状态**: ✅ **OK** — 2026-05-15 19:40 核验 cron payload：实际写入 `00-Memory/daily/YYYY-MM-DD.md`，下一次 23:30 运行将生成/追加当天日志。已切换为 gpt-5.5、light-context、轻量守护 prompt、no-deliver。

---

## 🧠 Self-Improving + Proactivity Check
- **Last Check**: 2026-04-28 01:52
- **Status**: ✅ **OK** — 三节拍 cron 均存在、启用、实跑成功；OpenClaw heartbeat 已启用，状态显示 `1h (main)`。
- **Action Needed**: 🟡 **WATCH** — Gateway service 仍提示旧式 embedded token，后续可安排 `openclaw gateway install --force` / doctor repair；不影响当前 cron 三节拍运行。

### 📰 ai-news-roundup（每日 07:00）
**代号**：AI-NEWS-ROUNDUP
**触发**：每日 07:00 (Asia/Taipei)
**执行体**：cron → `agentId: product-agent` ✅ 已切换
**质量参数（5/12 对齐）**：
- 选文：18 条（非 15），product-agent 自主决定
- 标题：英文原题可保留，不限 20 字硬截断
- Quote：要求有当日具体洞察，禁用"关键词"模板
- 产品雷达：与 AI 应用相关即合格
**状态**: ✅ **OK** — cron agentId 已切换为 product-agent，SKILL.md 5/12 08:08 已升级（金句退化检测 + 18条选文 + 产品雷达门禁加固）

---
*最后更新: 2026-05-15 19:40*
