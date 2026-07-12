# 🪶 小羽毛 AI 新闻早报 — AGENT 调用指南

> **共享位置**: `~/.openclaw/workspace/iFAi/skills/ai-news-roundup/`
> **打包文件**: `~/.openclaw/workspace/iFAi/skills/ai-news-roundup.skill`
> **技能名称**: `ai-news-roundup`
> **维护者**: 紫色小羽毛 (product-agent)

---

## 各 Agent 调用方式

### 主 Agent（your-agent — 负责派发）

**方式**: 使用 OpenClaw cron 注册每日 07:00 定时任务，执行 `ai-news-roundup` skill。

```bash
openclaw cron add \
  --name "ai-news-roundup-daily" \
  --cron "0 7 * * *" \
  --tz "Asia/Taipei" \
  --session isolated \
  --message "...（参见 SKILL.md 或 SCHEDULES.md 中的 Agent 任务描述）"
```

**引用 skill**: 安装后，Agent 在收到 cron 触发时读取 `SKILL.md` 执行全流程。

### 产品 Agent（product-agent）

**协作场景**: 当早报数据中含新产品/赛道动态时，product-agent 可引用 daily_data.json 做进一步的竞品分析或需求调研。

**取值方式**: 读取 `~/workspace/skills/ai-news-roundup/daily_data.json` 的 `products` 和 `news` 字段。

### 其他 Agent

任何 Agent 可通过以下方式使用：
1. 安装 .skill 包：`cp ~/.openclaw/workspace/iFAi/skills/ai-news-roundup.skill <目标路径>`
2. 直接引用共享目录：`read ~/.openclaw/workspace/iFAi/skills/ai-news-roundup/SKILL.md`
3. 定时执行：注册 cron 任务调用 skill

---

## 架构速览

```
双层流水线：
  脚本层（确定性）→ Agent 层（创造性策展）

每日 07:00 cron 自动触发
  1. fetch_ai_news.py → candidates.json
  2. build_daily_data.py → daily_data.json（原始草稿）
  3. Agent 策展 → 改写标题+摘要+标签+寄语
  4. 写回 daily_data.json
  5. update_news_ts.py + npm build + deploy.sh → Vercel
  6. message 工具 → 飞书推送
```

## 关键文件路径

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 完整技能指令（Agent 策展指南） |
| `SCHEDULES.md` | 定时任务注册方式 |
| `config.yaml` | 源配置（RSS/产品平台） |
| `scripts/fetch_ai_news.py` | 抓取脚本 |
| `scripts/build_daily_data.py` | 结构化脚本 |
| `scripts/format_feishu.py` | 飞书消息格式化 |
| `scripts/update_news_ts.py` | next.js 数据更新 |
| `scripts/deploy.sh` | Vercel 部署脚本 |
| `.env.example` | 环境变量模板 |
| `examples/` | 策展前后对比样本 |

## 环境要求

- Python 3.10+
- Node.js 20+
- Vercel CLI + VERCEL_TOKEN（环境变量）
- `npm install` 一次
