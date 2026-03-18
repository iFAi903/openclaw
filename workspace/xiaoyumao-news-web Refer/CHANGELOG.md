# 小羽毛 AI 新闻早报 - 热门产品追踪板块优化

## 更新日期
2026年03月17日

## 主要改动

### 1. 热门产品追踪板块重构

**原有问题：**
- 产品全部来自 HackerNews 单一平台
- 产品只有名称，没有摘要/简介
- 标题翻译混乱（如"多内利"、"英伟达's"）

**改进后：**
- ✅ 从 5 个平台各取 1 个热门产品：
  1. **Product Hunt** - 全球创新产品首发平台
  2. **GitHub** - 热门开源 AI 项目
  3. **Toolify** - AI 工具排行榜
  4. **HackerNews** - 技术社区热门
  5. **Reddit** - AI 社区讨论热点

- ✅ 每个产品包含：
  - 英文产品名称（保留原名）
  - 一句话中文摘要
  - 来源平台标识
  - 产品链接

### 2. 标题翻译策略统一

**规则：**
- 产品名称保留英文原文（如 Adaptive、mecha.im、Toolify）
- 摘要翻译为中文，但保留关键英文术语（如 AI、GPT、API）
- 新闻标题以中文为主，保留公司/产品英文名（如 NVIDIA、OpenAI）

### 3. 代码文件修改

**fetch_news_v2.py:**
- 新增 5 个产品抓取函数：
  - `fetch_product_hunt()` - 抓取 ProductHunt 热门产品
  - `fetch_github_trending()` - 抓取 GitHub AI 热门项目
  - `fetch_toolify()` - 抓取 Toolify AI 工具（含备用数据）
  - `fetch_hackernews_products()` - 抓取 HackerNews Show HN
  - `fetch_reddit_products()` - 抓取 Reddit AI 热门讨论

- 扩展 `ENGLISH_KEYWORDS` 列表，添加更多产品名保护

**src/data/news.ts:**
- 更新产品数据为 5 平台多样化来源
- 每个产品附带中文摘要

**daily_data.json:**
- 同步更新产品数据结构

### 4. 示例产品展示

```
1. [Product Hunt] Adaptive — The Agent Computer
   摘要: AI 智能体计算机，让自动化任务执行更简单高效

2. [GitHub] mecha.im
   摘要: 在你的机器上运行一支机器人大军 ⭐ 12

3. [Toolify] Toolify AI
   摘要: AI 工具导航网站，汇集全球最新 AI 应用与工具

4. [HackerNews] Trackm, a personal finance web app
   摘要: HackerNews 社区推荐的创新产品 - 个人理财 Web 应用

5. [Reddit] 1.5M people quit GPT and all for the right reasons tbh.
   摘要: Reddit AI 社区热门讨论：150万人退出 GPT 的深层原因分析
```

## 技术实现

### 多平台抓取策略
每个平台使用不同的抓取方式：
- ProductHunt: RSS Atom feed 解析
- GitHub: GitHub Search API
- Toolify: RSS feed + 备用数据
- HackerNews: RSS feed (优先 Show HN)
- Reddit: RSS Atom feed

### 标题翻译保护机制
使用 `ENGLISH_KEYWORDS` 集合保护关键术语，防止产品名/公司名被翻译：
- 保护 NVIDIA、OpenAI、ChatGPT 等品牌名
- 保护 API、SDK、LLM 等技术术语
- 保护 Jensen Huang、Sam Altman 等人名

## 后续优化方向
1. 添加产品封面图片抓取
2. 根据产品热度排序
3. 添加产品分类标签
4. 用户点击追踪分析

---
更新者: CTO 小羽毛
审核者: CEO 小羽毛
