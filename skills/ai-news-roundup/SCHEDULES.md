# 🪶 小羽毛 AI 新闻早报 · 定时任务配置

> **架构**：双层流水线 — 脚本层（确定性）→ Agent 层（策展）

---

## 定时任务：每日 07:00

### 注册命令

```bash
openclaw cron add \
  --name "ai-news-roundup-daily" \
  --cron "0 7 * * *" \
  --tz "Asia/Taipei" \
  --session isolated \
  --message "...（见下文 Agent 任务描述）" \
  --no-deliver
```

### Agent 任务描述

```text
你是小羽毛早报编辑。执行小羽毛 AI 新闻早报的每日流水线。

=== 第1步：运行脚本层（确定性工作）===

cd /Users/ifai_macpro/.agents/skills/ai-news-roundup

python3 scripts/fetch_ai_news.py --config config.yaml
→ 生成 candidates.json

python3 scripts/build_daily_data.py
→ 生成 daily_data.json（原始草稿，含去重+结构化，但不含金句和标签）

确认两个文件已生成且不为空。如果任一脚本失败，报告失败源并终止。


=== 第2步：阅读 daily_data.json 原始草稿 ===

读取 daily_data.json，全面理解今日候选：
- 新闻候选池大小
- 来源分布（活跃源数）
- 产品候选池
- news 数组中的每条原始数据（title, summary, source, url, 等）
- quote 字段为空（脚本已不生成）
- tags 字段为空（脚本已不分配）


=== 第3步：Agent 策展（这是核心价值！）===

详细遵循 SKILL.md 中「Agent 层」的指引：

(1) 选文 — 阅读所有候选，挑选 ≤18 条最有价值的新闻
    - 覆盖多源、多维度
    - 不是机械取权重最高，你的判断比脚本好
    - 如果候选不足 18，如实保留实际数量

(2) 标题编辑 — 每条重写为 ≤20 字中文
    - 说清"谁的什么事"
    - 保留公司/产品英文名
    - 翻译残缺的标题完全重写
    - 禁止：新动态、今日观察、值得关注 等

(3) 摘要润色 — 每条 ≤120 字，补充标题之外的信息
    - 去除空话（"值得关注其影响"）
    - 补充具体信息（金额、能力、场景、后果）

(4) 标签分配 — 每条 ≤3 个，从以下 12 类中选择：
    资本 模型 Agent 基础设施 开源 产品 研究 政策 应用 硬件 行业 全球

(5) 产品雷达 — 从 product 数组中选 ≤5 个具体产品
    - 必须是具体工具/产品，不是平台集合页
    - 去除产品名空白的条目
    - 去除平台为 RSS 源的条目
    - 摘要要写"解决什么问题 + 场景"
    - 如果某平台当天只有集合页，宁缺毋滥

(6) 今日寄语 — 写一条 ≤90 字的编辑手记
    - 必须引用至少 1 条当日具体新闻/公司/动态
    - 时效性强，今天独有
    - 不像 AI 套话，像编辑看了今天的内容后写的笔记
    - 禁止：方向连续冒头、信号出现、值得关注、结构性变化等


=== 第4步：写回 daily_data.json ===

将策展后的完整数据写回 daily_data.json，结构保持：
{
  "date": "...",
  "news": [策展后的 18 条, 含 tags, 重写后的 title/summary],
  "products": [策展后的 ≤5 个产品],
  "quote": "你的今日寄语",
  "quote_context": {},
  "summary": "...",
  "meta": { ...保持原样 }
}


=== 第5步：格式化和部署 ===

cd /Users/ifai_macpro/.agents/skills/ai-news-roundup
python3 scripts/update_news_ts.py
npm run build
bash scripts/deploy.sh

验证：curl -sI https://xiaoyumao-news-web.vercel.app | head -1（期望 200）

如果某一步失败，跳过部署但继续推送（消息中说明部署失败原因）。


=== 第6步：飞书推送 ===

使用 message 工具发送飞书消息。格式如下：

🪶 小羽毛 AI 新闻早报 ｜ YYYY年MM月DD日 周X

💬 今日洞察
  你的编辑手记（≤90 字）

━━━ 📰 AI 新闻 ━━━

1️⃣ 【标签】编辑后的标题
📰 出处：来源名称
📝 编辑后的摘要
🔗 [查看原文](链接)

...（全部 18 条，或实际数量）

━━━ 🛍️ 产品雷达 ━━━

产品名｜平台
产品摘要
🔗 [查看原文](链接)

...（实际数量）

━━━
⚡ X 条新闻 + Y 产品 · AI 天团自动巡检

注意：
- target: 飞书用户（刘羽的 open_id）
- 不要发送空消息
- 如果脚本 fail，只报告失败源
- 如果候选不足，如实说明
```

### 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `--cron` | `0 7 * * *` | 每日早上 7:00（Asia/Taipei） |
| `--session` | `isolated` | 独立会话 |
| `--model` | 不指定（用 agent 默认） | 建议确保使用强推理模型 |
| `--no-deliver` | | 只有 Agent 明确调用 message 才推送 |

### 手动触发

```bash
openclaw cron run --id "ai-news-roundup-daily"
```

### 查看状态

```bash
openclaw cron list
```

---

## 环境变量

```bash
export VERCEL_TOKEN="<从 .env.cron 或 Vercel Dashboard 读取>"
```
