# 小羽毛 AI 新闻早报 - RSS 源配置
# 更新日期：2026-02-12

## 主流科技媒体（15个 RSS 源）

1. **The Verge AI**
   - URL: https://www.theverge.com/rss/ai-artificial-intelligence/index.xml
   - 类型：综合科技新闻

2. **TechCrunch AI**
   - URL: https://techcrunch.com/category/artificial-intelligence/feed/
   - 类型：创业公司、投资新闻

3. **MIT Technology Review AI**
   - URL: https://www.technologyreview.com/topic/artificial-intelligence/feed
   - 类型：前沿技术研究

4. **Wired AI**
   - URL: https://www.wired.com/feed/tag/ai/latest/rss
   - 类型：科技文化

5. **VentureBeat AI**
   - URL: https://venturebeat.com/category/ai/feed/
   - 类型：企业AI、商业

6. **The Guardian AI**
   - URL: https://www.theguardian.com/technology/artificialintelligenceai/rss
   - 类型：主流媒体报道

7. **ScienceDaily AI**
   - URL: https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml
   - 类型：学术研究

8. **AI News**
   - URL: https://www.artificialintelligence-news.com/feed/
   - 类型：AI 专业新闻

9. **MarkTechPost**
   - URL: https://www.marktechpost.com/feed/
   - 类型：AI/ML 研究速览

10. **MIT News AI**
    - URL: https://news.mit.edu/rss/topic/artificial-intelligence2
    - 类型：MIT 研究成果

11. **Google Research Blog**
    - URL: https://research.google/blog/rss/
    - 类型：Google AI 研究

12. **Microsoft AI Blog**
    - URL: https://news.microsoft.com/source/topics/ai/feed/
    - 类型：微软 AI 动态

13. **BAIR (Berkeley)**
    - URL: https://bair.berkeley.edu/blog/feed.xml
    - 类型：伯克利 AI 研究

14. **O'Reilly AI & ML**
    - URL: https://www.oreilly.com/radar/topics/ai-ml/feed/index.xml
    - 类型：技术趋势分析

15. **KDnuggets**
    - URL: https://www.kdnuggets.com/feed
    - 类型：数据科学、机器学习

---

## 热门应用平台（5个 RSS 源）

### Product Hunt
- URL: https://www.producthunt.com/feed
- 备用：可能需要使用 API 或网页抓取

### GitHub Trending
- URL: https://github.com/trending
- 说明：GitHub 没有官方 Trending RSS，需要使用 API 或网页抓取
- 替代方案：https://github.com/NiceLabs/github-trending-rss

### Toolify.ai
- URL: https://www.toolify.ai/
- 说明：需要检查是否有 RSS 或 API

### Hacker News
- URL: https://news.ycombinator.com/rss
- 类型：科技社区热门

### Reddit
- r/artificial: https://www.reddit.com/r/artificial/.rss
- r/MachineLearning: https://www.reddit.com/r/MachineLearning/.rss
- r/OpenAI: https://www.reddit.com/r/OpenAI/.rss

---

## 备用 RSS 源（当主要源不可用时）

### 更多 AI 新闻源
- Unite.AI: https://www.unite.ai/feed/
- DailyAI: https://dailyai.com/feed/
- AI Weekly: https://aiweekly.co/issues.rss
- Becoming Human: https://becominghuman.ai/feed
- AI Summer: https://theaisummer.com/feed.xml

### 中文 AI 媒体
- Analytics India Magazine AI: https://analyticsindiamag.com/ai-news-updates/feed/

---

## 使用方法

### 1. 使用 web_fetch 获取 RSS
```python
web_fetch("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml")
```

### 2. 解析 RSS XML
提取 `<item>` 标签中的：
- `<title>` - 标题
- `<link>` - 链接
- `<pubDate>` - 发布时间
- `<description>` - 摘要

### 3. 去重策略
- 基于标题相似度（去除重复报道）
- 基于链接（确保不重复）
- 基于发布时间（取最近 24 小时）

### 4. 备选方案
当 RSS 不可用时：
1. 尝试使用 RSSHub 等 RSS 聚合服务
2. 使用 web_search 作为后备
3. 标注 "RSS 暂不可用，信息暂空"