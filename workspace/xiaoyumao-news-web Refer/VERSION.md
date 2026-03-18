# 版本说明文档

## 小羽毛 AI 新闻早报 - v1.0.0-stable

---

### 📌 版本信息

- **版本号**: v1.0.0
- **发布日期**: 2026-03-18
- **代号**: 稳定版 (stable)
- **状态**: ✅ 已发布

---

### 🎯 核心功能

#### 1. 13 个 RSS 源全覆盖
| 序号 | 来源名称 | 类型 | 状态 |
|:---:|---------|------|:----:|
| 1 | The Verge AI | 综合科技新闻 | ✅ |
| 2 | TechCrunch AI | 创业公司、投资 | ✅ |
| 3 | MIT Technology Review | 前沿技术研究 | ✅ |
| 4 | Wired AI | 科技文化 | ✅ |
| 5 | VentureBeat AI | 企业AI、商业 | ✅ |
| 6 | The Guardian AI | 主流媒体 | ✅ |
| 7 | ScienceDaily AI | 学术研究 | ✅ |
| 8 | AI News | AI 专业新闻 | ✅ |
| 9 | MIT News AI | MIT 研究成果 | ✅ |
| 10 | Google Research Blog | Google AI 研究 | ✅ |
| 11 | Microsoft AI Blog | 微软 AI 动态 | ✅ |
| 12 | BAIR (Berkeley) | 伯克利 AI 研究 | ✅ |
| 13 | MarkTechPost | AI/ML 研究速览 | ✅ |

#### 2. 5 个产品平台真实抓取
| 平台 | 数据来源 | 内容类型 |
|-----|---------|---------|
| GitHub | Trending 热门仓库 | AI 开源项目 |
| Product Hunt | 热门产品 | AI 新产品 |
| Hacker News | 热门帖子 | 技术产品讨论 |
| Reddit | r/artificial 等 | 社区热议产品 |

#### 3. 轮询去重算法
- **标题相似度去重**: 去除重复报道
- **URL 唯一性校验**: 确保不重复
- **发布时间过滤**: 取最近 24 小时
- **来源轮换机制**: 确保多样性

---

### 📊 数据来源清单

#### 新闻媒体源 (13个)
1. The Verge - https://www.theverge.com/rss/ai-artificial-intelligence/index.xml
2. TechCrunch - https://techcrunch.com/category/artificial-intelligence/feed/
3. MIT Technology Review - https://www.technologyreview.com/topic/artificial-intelligence/feed
4. Wired - https://www.wired.com/feed/tag/ai/latest/rss
5. VentureBeat - https://venturebeat.com/category/ai/feed/
6. The Guardian - https://www.theguardian.com/technology/artificialintelligenceai/rss
7. ScienceDaily - https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml
8. AI News - https://www.artificialintelligence-news.com/feed/
9. MIT News - https://news.mit.edu/rss/topic/artificial-intelligence2
10. Google Research - https://research.google/blog/rss/
11. Microsoft AI - https://news.microsoft.com/source/topics/ai/feed/
12. BAIR Berkeley - https://bair.berkeley.edu/blog/feed.xml
13. MarkTechPost - https://www.marktechpost.com/feed/

#### 产品数据源 (5个)
1. GitHub Trending - https://github.com/trending
2. Product Hunt - https://www.producthunt.com/feed
3. Hacker News - https://news.ycombinator.com/rss
4. Reddit r/artificial - https://www.reddit.com/r/artificial/.rss
5. Reddit r/MachineLearning - https://www.reddit.com/r/MachineLearning/.rss

---

### 📁 关键文件清单

| 文件名 | 描述 | 用途 |
|-------|------|------|
| `fetch_news_final.py` | 主抓取脚本 | 核心抓取逻辑 |
| `daily_data.json` | 每日数据 | 当日聚合数据 |
| `src/data/news.ts` | 前端数据 | TypeScript 数据文件 |
| `rss-sources.md` | RSS源配置 | 源文档说明 |
| `README.md` | 项目说明 | 基础文档 |
| `VERSION.md` | 版本文档 | 本文件 |

---

### 🚀 部署信息

- **部署平台**: Vercel
- **访问地址**: https://xiaoyumao-news-web.vercel.app
- **框架**: Next.js 14 + React + TypeScript
- **样式**: Tailwind CSS

---

### 📝 更新日志

#### v1.0.0 (2026-03-18)
- ✅ 完成 13 个 RSS 源集成
- ✅ 完成 5 个产品平台抓取
- ✅ 实现轮询去重算法
- ✅ 首次稳定版本发布

---

### 👨‍💻 开发团队

**小羽毛 AI 天团**
- CTO: 小羽毛首席技术官
- 架构: Claude 3.5 Sonnet
- 维护: 自动化部署流程

---

### 📜 许可证

MIT License - 开源项目

---

*Last updated: 2026-03-18*
