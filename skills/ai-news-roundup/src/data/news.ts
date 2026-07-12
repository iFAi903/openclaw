// 自动生成 - 小羽毛 AI 新闻早报
// 生成时间: 2026-07-12 21:27:05

export interface NewsCard {
  id: string;
  rank: number;
  title: string;
  source: string;
  url: string;
  summary: string;
  publishedAt: string;
  type: 'news' | 'product';
  score: number;
  reason: string;
  platform?: string;
  tags?: string[];
}

export interface DailyNewsPayload {
  date: string;
  summary: string;
  quote: { text: string; author: string };
  generatedAt: string;
  websiteUrl: string;
  meta: Record<string, any>;
  aiNews: NewsCard[];
  products: NewsCard[];
}

export const todayNews: DailyNewsPayload = {
  "date": "2026年07月12日 周日",
  "summary": "",
  "quote": {
    "text": "三条线指向同一个事实：数据中心遭社区抵制、OpenAI走向家庭消费、工程师集体适应AI冲击。AI已经不是\"会不会发生\"，而是\"磨合期多痛\"。",
    "author": "小羽毛 AI"
  },
  "generatedAt": "2026-07-12T21:27:05.356876+08:00",
  "websiteUrl": "https://ai-news-roundup.vercel.app",
  "meta": {
    "source_stats": {
      "TheVerge": 1,
      "TechCrunch": 1,
      "Wired": 1,
      "TheGuardian AI": 1
    },
    "products_filtered_out": [
      "GitHub Trending（集合页）",
      "Hacker News（博客文章，非产品）"
    ],
    "curation_source": "Agent独立策展（fetch/build层异常后人工接管）"
  },
  "aiNews": [
    {
      "id": "news_1",
      "rank": 1,
      "title": "",
      "source": "TheVerge",
      "url": "https://www.theverge.com/column/963346/ai-data-centers-fight",
      "summary": "",
      "publishedAt": "",
      "type": "news",
      "score": 0,
      "reason": "基础设施, 行业",
      "tags": [
        "基础设施",
        "行业"
      ]
    },
    {
      "id": "news_2",
      "rank": 2,
      "title": "",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/07/11/openai-bets-on-families-as-chatgpt-goes-deeper-into-households/",
      "summary": "",
      "publishedAt": "",
      "type": "news",
      "score": 0,
      "reason": "产品, 应用",
      "tags": [
        "产品",
        "应用"
      ]
    },
    {
      "id": "news_3",
      "rank": 3,
      "title": "",
      "source": "Wired",
      "url": "https://www.wired.com/story/scientists-using-ai-and-quantum-computing-to-generate-new-peptides/",
      "summary": "",
      "publishedAt": "",
      "type": "news",
      "score": 0,
      "reason": "研究, 模型",
      "tags": [
        "研究",
        "模型"
      ]
    },
    {
      "id": "news_4",
      "rank": 4,
      "title": "",
      "source": "TheGuardian AI",
      "url": "https://www.theguardian.com/technology/ng-interactive/2026/jul/12/software-developers-engineers-ai",
      "summary": "",
      "publishedAt": "",
      "type": "news",
      "score": 0,
      "reason": "行业, 全球",
      "tags": [
        "行业",
        "全球"
      ]
    }
  ],
  "products": [
    {
      "id": "product_1",
      "rank": 1,
      "title": "Second Brain for AI v2",
      "source": "",
      "platform": "Product Hunt",
      "url": "https://www.producthunt.com/products/second-brain-cloudflare",
      "summary": "AI 记忆系统，自动连接所有工具中的信息碎片，构建跨应用的上下文大脑。适合重度知识工作者。",
      "publishedAt": "",
      "type": "product",
      "score": 0,
      "reason": "",
      "tags": []
    }
  ]
};

export default todayNews;
