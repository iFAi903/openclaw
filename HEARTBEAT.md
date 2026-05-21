# HEARTBEAT.md - 贾维斯守护进程配置

## ⏰ 守护进程状态
- **状态**: RUNNING ✅
- **运行时段**: 24/7 (Always Active)
- **自动重启**: 已启用 ✅
- **崩溃恢复**: 已启用 ✅
- **最后更新**: 2026-05-21 11:10 Asia/Taipei

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
**状态**: 🟡 **WATCH** — 2026-05-21 08:40 核验：08:11 已移除显式 `toolsAllow` 并补偿生成 `reports/evolution-2026-05-21.md`；08:40 cron 配置确认 `toolsAllow=null`。需等 2026-05-22 00:00 下一轮自动执行确认是否真实恢复落盘。

---

### 🌅 节拍二：晨间简报 (08:30)
**代号**：MORNING-BRIEF
**触发**：每日 08:30 (Asia/Taipei)
**输出**：飞书主动消息
**状态**: ✅ **OK** — 2026-05-21 08:40 核验：08:30 自动运行已完成，cron 状态 `ok`，delivery 为 `delivered`，run summary 未再出现 `No filesystem` / `[blocked]`。显式 `toolsAllow` 已保持移除。

---

### 🌙 节拍一：深夜复盘 (23:30)
**代号**：NIGHTLY-REVIEW
**触发**：每日 23:30 (Asia/Taipei)
**输出**：`00-Memory/daily/YYYY-MM-DD.md`
**状态**: ✅ **OK** — 2026-05-21 23:40 核验：`nightly-review-001` 本轮 cron 状态 `ok`，且已自动生成 `00-Memory/daily/2026-05-21.md`。深夜复盘自动落盘恢复确认。

---

## 🧠 Self-Improving + Proactivity Check
- **Last Check**: 2026-04-28 01:52
- **Status**: 🟡 **WATCH** — 三节拍 cron 均存在且启用；08:30 晨间简报已恢复 delivered，23:30 深夜复盘已恢复自动落盘。00:00 每日进化仍需等下一轮自动产物验证。
- **Action Needed**: 🟡 **WATCH** — 2026-05-22 00:00 后核验每日进化是否生成 `reports/evolution-2026-05-22.md`；2026-05-22 07:00 后核验 AI 新闻早报是否自动投递。2026-05-21 11:10 已清理 OpenClaw 配置中的重复 bundled feishu path 与未安装 disabled line entry，使用 `$HOME/.npm-global/bin` 后 `openclaw cron list` 不再出现插件配置 warning。

### 📰 ai-news-roundup（每日 07:00）
**代号**：AI-NEWS-ROUNDUP
**触发**：每日 07:00 (Asia/Taipei)
**执行体**：cron → `agentId: product-agent` ✅ 已切换
**质量参数（5/12 对齐）**：
- 选文：18 条（非 15），product-agent 自主决定
- 标题：英文原题可保留，不限 20 字硬截断
- Quote：要求有当日具体洞察，禁用"关键词"模板
- 产品雷达：与 AI 应用相关即合格
**状态**: 🟡 **WATCH** — 2026-05-21 09:14 已定位 07:00 失败主因：`fetch_ai_news.py` 串行网络翻译导致抓取链路可能超时。已将 Google Translate 网络调用改为 opt-in，仅保留本地短语回退；手动验证 `fetch_ai_news.py` 42 秒完成，`build_daily_data.py` 成功生成 18 新闻 + 5 产品。待 2026-05-22 07:00 下一轮自动投递确认。

---
*最后更新: 2026-05-21 23:40*
