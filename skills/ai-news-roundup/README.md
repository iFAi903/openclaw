# 🪶 小羽毛 AI 新闻早报

> **由 Agent 编审，不止于聚合。** 每天 07:00，中文世界的 AI 新闻第一杯咖啡。

[![Powered by OpenClaw](https://img.shields.io/badge/Powered%20by-OpenClaw-6C47FF)](https://openclaw.ai)
[![Daily Run](https://img.shields.io/badge/Daily-07:00%20(GMT%2B8)-blue)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://python.org)
[![Languages](https://img.shields.io/badge/Languages-中文%20%7C%20English-brightgreen)]()

## 👀 它能替你做这些事

你有每天早上打开飞书，第一眼看到一条 **「今天的 AI 世界发生了什么」** 的需求。不是英文原文 RSS 聚合，不是泛泛的科技新闻，而是：

- **中文的**：英文标题和摘要已自动翻译
- **筛选过的**：从 16 个源 + 5 个产品平台中，Agent 帮你挑出值得读的
- **有洞察的**：不止列出新闻，还有今日寄语——基于当天真实内容的编辑手记
- **准时到达的**：每天早上 07:00 推送到飞书

[👀 在线预览](https://ai-news-roundup.vercel.app) · Vercel 部署的网页版

---

## ✨ 它和纯 RSS 聚合器有什么不同？

| 纯 RSS 聚合器 | 小羽毛早报 |
|---|---|
| 标题是机器直译："我间谍""聊天GPT工作" | 标题经 Agent 重写：清晰的中文说明，说清谁做了什么事 |
| 金句是模板套话："今日 X 方向有 Y 条动态" | 今日寄语是基于当天新闻内容的真实编辑手记 |
| 产品雷达混入非产品（招聘页、集合页） | 产品雷达经 Agent 甄别，只保留真正的产品 |
| 标签靠规则匹配，可能为空 | 标签由 Agent 从 12 分类体系中准确分配 |
| 去重有时会漏，同文出现多次 | 脚本层精确去重 + 编辑层二次验重 |

---

## 🚀 快速开始

### 前置条件

- **OpenClaw** 或其他支持 SKILL.md 的 Agent runtime
- **Python 3.11+**
- **飞书 Bot 或消息推送渠道**

### 安装

```bash
pip install PyYAML
```

将 `ai-news-roundup` 目录放进你的 Agent 的 skills 目录（或通过 clawhub install）。

### 配置

编辑 `config.yaml`，配置你的 RSS 源和推送目标。

### 手动运行

```bash
cd ~/.agents/skills/ai-news-roundup

# 脚本层：抓取 + 结构化
python3 scripts/fetch_ai_news.py
python3 scripts/build_daily_data.py

# Agent 通过消息触发策展：
# "今天的 AI 新闻早报策展"
# → 自动读取 daily_data.json → 编辑选文/重写标题/分配标签/撰写今日寄语
# → 格式化输出 → 推送飞书
```

### 自动调度（OpenClaw cron）

已在 cron 中注册 `ai-news-roundup-daily`：每日 07:00（Asia/Taipei）自动执行。

---

## 🏗️ 架构：双层 Agent 流水线

```
┌─────────────────────────────────────────────────────────────┐
│                     cron: 每日 07:00                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────── 脚本层（确定性）─────────────┐                    │
│  │ Step 1: fetch_ai_news.py              │                    │
│  │   ├─ RSS 抓取（16 源）→ 英文 → 中文   │                    │
│  │   ├─ 产品雷达（5 平台）               │                    │
│  │   └─ 输出: candidates.json            │                    │
│  │              ↓                        │                    │
│  │ Step 2: build_daily_data.py           │                    │
│  │   ├─ URL/similarity 精确去重          │                    │
│  │   ├─ 主题聚类 + 摘要截断              │                    │
│  │   ├─ 产品门禁(平台合法性检查)         │                    │
│  │   └─ 输出: daily_data.json            │                    │
│  └───────────────────────────────────────┘                    │
│              ↓                                               │
│  ┌────────── Agent 层（策展）─────────────┐                   │
│  │ Agent「小羽毛早报编辑」              │                    │
│  │   ├─ 从候选池选文（编辑判断）         │                    │
│  │   ├─ 标题重写（清除翻译残留）         │                    │
│  │   ├─ 摘要润色（保留信息量）           │                    │
│  │   ├─ 标签分配（12 分类体系）          │                    │
│  │   ├─ 产品雷达甄别（剔除非产品）       │                    │
│  │   └─ 今日寄语（基于真实内容撰写）     │                    │
│  └───────────────────────────────────────┘                    │
│              ↓                                               │
│  ┌────────── 发布层 ─────────────────────┐                    │
│  │ format_feishu.py                      │                    │
│  │   └─ 飞书纯文本消息格式              │                    │
│  ├─ 推送飞书（message tool）             │                    │
│  └─ Vercel 部署（deploy.sh）             │                    │
│     └─ 网页版更新                        │                    │
└─────────────────────────────────────────────────────────────┘
```

### 三层职责

| 层 | 做什么 | 由谁负责 | 失败影响 |
|---|---|---|---|
| **脚本层** | 抓取、翻译、去重、聚类、产品门禁 — 确定性工作 | `build_daily_data.py` | 候选数据质量不够 → Agent 选文受限 |
| **策展层** | 编辑判断、标题重写、标签分配、今日寄语 — 创造性工作 | **Agent「小羽毛早报编辑」** | 推送质量下降（标题残品、标签空白、寄语套话） |
| **发布层** | 格式化、推送、部署 | `format_feishu.py` + `deploy.sh` | 推送失败可重试，不影响数据 |

---

## 📡 数据源

### 新闻源（16 个 RSS）

三花AI · TheVerge · TechCrunch · Wired · VentureBeat ·
MIT Tech Review · AI News · TheGuardian AI · MarkTechPost ·
MIT News · Google Research · OpenAI Blog · BAIR Berkeley ·
ScienceDaily · KDnuggets · AI HOT

### 产品平台（5 个）

Product Hunt · GitHub Trending · Toolify · Hacker News · Trustmrr

---

## 🛡️ 质量体系

### 脚本层质量门禁（确定性）

| 关卡 | 手段 |
|---|---|
| **去重** | URL 精确去重 + Jaccard 内容相似度 + 48h 历史交叉 |
| **摘要截断** | 长度 10-160 字符，禁止标题简单重复 |
| **产品平台污染** | 检查 platform 字段合法性，禁止 news-site 文章混入 |
| **产品兜底** | 平台抓取失败时用历史补充 |

### Agent 策展层质量门禁（编辑级）

| 关卡 | Agent 自检问题 |
|---|---|
| **标题** | 是否清除了翻译残留（断句、未完成句、乱码、"我间谍"类）？标题是否说清了"谁 + 做了什么事"？ |
| **标签** | 是否属于 12 分类体系？是否准确？是否有更精确的标签？ |
| **摘要** | 是否保留了足够的信息量？是否补充了背景？ |
| **产品** | 是否真的是产品？（不是招聘帖、合集页、事件条目） |
| **今日寄语** | 是基于今天真实新闻内容的编辑手记，还是模板套话？ |

### Agent 自检清单（写入推送前最后检查）

- [ ] 选文覆盖了当日最重要的 AI 动态？
- [ ] 选项文没有明显的翻译残次标题？
- [ ] 标签分配到每个条目且准确？
- [ ] 产品雷达不含非产品条目？
- [ ] 今日寄语是今天独有的、基于真实内容的？
- [ ] 整体阅读体验流畅？

---

## 📊 输出产物

| 文件 | 说明 | 频率 |
|---|---|---|
| `candidates.json` | 原始抓取候选（未筛选） | 每次运行 |
| `daily_data.json` | 结构化输出（提交给 Agent 策展） | 每次运行 |
| 飞书推送 | 格式化后的纯文本消息 | 每日 07:00 |
| Vercel 前端 | `ai-news-roundup.vercel.app` | 每日更新 |

---

## 📜 License

MIT License

---

<p align="center">
  🪶 小羽毛 AI 天团产品 · 每日早报
</p>
