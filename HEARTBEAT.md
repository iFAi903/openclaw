# HEARTBEAT.md - 贾维斯守护进程配置

## ⏰ 守护进程状态
- **状态**: RUNNING ✅
- **运行时段**: 24/7 (Always Active)
- **自动重启**: 已启用 ✅
- **崩溃恢复**: 已启用 ✅
- **最后更新**: 2026-06-13 12:06 Asia/Taipei

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
**状态**: ✅ **FIXED** — 2026-06-19 19:40 重建：cron `77a68848` (每日进化（潜龙计划）)，00:00 Taipei，模型 `gpt-5.4-mini`，轻量四阶段。2026-06-20 00:00 首次验收：成功落盘（1.2KB），4条洞察 + evolution.json 同步。

---

### 🌅 节拍二：晨间简报 (08:30)
**代号**：MORNING-BRIEF
**触发**：每日 08:30 (Asia/Taipei)
**输出**：飞书主动消息
**状态**: ✅ **OK** — 2026-06-14 08:30 核验：恢复成功，`ok`，34s，delivered。

---

### 🌙 节拍一：深夜复盘 (23:30)
**代号**：NIGHTLY-REVIEW
**触发**：每日 23:30 (Asia/Taipei)
**输出**：`00-Memory/daily/YYYY-MM-DD.md`
**状态**: ✅ **FIXED** — 2026-06-19 23:41 实测验证：`gpt-5.4-mini` 成功落盘（2.4KB，完整四段）。根因是 emoji 文件名 + 指令优先级。prompt 改为六步硬性流程，文件路径避开 emoji。

---

### 🔒 每晚安全审计 (23:00)
**代号**：NIGHTLY-SECURITY-AUDIT
**触发**：每日 23:00 (Asia/Taipei)
**状态**: ✅ **OK** — 2026-06-19 23:00 核验：模型切换后恢复成功，`ok`，206s。`gpt-5.4-mini` 稳定。

---

## 🧠 Self-Improving + Proactivity Check
- **Last Update**: 2026-06-28 23:44
- **Status**: ✅ **OK** — `gpt-5.4-mini` 配额已重置。关键发现：`custom-gateway-microflow-ai/gpt-5.4-mini` 别名 6/28 晚上连续返回 503（安全审计2次+复盘1次），切到 `openai/gpt-5.4-mini` 直连后秒通。已将所有 agentTurn cron job（安全审计/复盘/进化/晨间简报）全部改为 `openai/gpt-5.4-mini` + `deepseek-v4-flash` fallback。bash 类 job（战报/课表/AI早报）不受影响。晨间简报 6/28 模型被异常改成 `lmstudio/qwen/qwen3-4b-2507`，已修复。
- **Action Needed**: ①调查 `custom-gateway-microflow-ai/gpt-5.4-mini` 503 根因（gateway 侧还是 provider 侧）。②追查 `lmstudio/qwen` 别名写入来源。③明早 08:30 验证简报恢复。

### 🎒 小羽毛课表审计（每日 10:00 / 23:00）
**代号**：CLASS-AUDIT
**触发**：每日 10:00 + 23:00 (Asia/Taipei)
**执行体**：cron `7b47a862` → bash 脚本 ✅
**状态**: ✅ **NEW** — 2026-06-20 18:40 重建为 bash 脚本。每日两次点名：上午场查 00:00-10:00 四节课，夜间场查全天七节课。

### 📰 ai-news-roundup（每日 07:00）
**代号**：AI-NEWS-ROUNDUP
**触发**：每日 07:00 (Asia/Taipei)
**执行体**：cron → `agentId: main` ✅
**状态**: ✅ **OK** — 2026-06-13 07:00 核验：今日运行成功，`delivered`。

---
*最后更新: 2026-06-14 23:40*
