// 自动生成 - 小羽毛 AI 早报
// 生成时间: 2026-03-20 08:11:15

export interface NewsItem {
  id: string;
  title: string;
  source: string;
  url: string;
  summary: string;
  type: 'news' | 'product';
  publishedAt: string;
}

export interface DailyNews {
  date: string;
  aiNews: NewsItem[];
  products: NewsItem[];
  summary: string;
  quote: {
    text: string;
    author: string;
  };
  generatedAt: string;
  websiteUrl: string;
}

export const todayNews: DailyNews = {
  "date": "2026年03月20日 周五",
  "aiNews": [
    {
      "id": "news_1",
      "title": "流氓人工智能导致 Meta 发生严重安全事件",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/897528/meta-rogue-ai-agent-security-incident",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_2",
      "title": "Adobe 的 AI 图像生成器现在可以根据您自己的艺术进行训练",
      "source": "TheVerge",
      "url": "https://www.theverge.com/tech/897243/adobe-firefly-ai-custom-models-image-public-beta",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_3",
      "title": "Fitbit 的人工智能健康教练很快就能读取你的医疗记录",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/897250/fitbits-ai-health-coach-reads-medical-records",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_4",
      "title": "大卫·萨克斯对伊朗的重大警告被严重忽视",
      "source": "TheVerge",
      "url": "https://www.theverge.com/column/896949/regulator-david-sacks-iran-polymarket",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_5",
      "title": "ChatGPT 无法治愈狗的癌症",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/896878/ai-did-not-cure-this-dogs-cancer",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_6",
      "title": "DLSS 5：Nvidia的AI图形技术是否已经走得太远了？",
      "source": "TheVerge",
      "url": "https://www.theverge.com/games/896518/nvidia-dlss-5-ai-3d-rendering",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_7",
      "title": "Nvidia 的 DLSS 5 就像视频游戏的运动平滑，但更糟糕",
      "source": "TheVerge",
      "url": "https://www.theverge.com/entertainment/896213/nvidia-dlss-5-ai-faces-motion-smoothing",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_8",
      "title": "现在美国的每个人都在使用谷歌的个性化 Gemini AI",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/896107/google-expands-personal-intelligence",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_9",
      "title": "微软在人工智能领导层改组后任命了一位新的副驾驶老板",
      "source": "TheVerge",
      "url": "https://www.theverge.com/news/895963/microsoft-copilot-leadership-changes-consumer-commercial",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_10",
      "title": "代码的未来既令人兴奋又令人恐惧",
      "source": "TheVerge",
      "url": "https://www.theverge.com/podcast/895910/claude-code-future-developers-vergecast",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_11",
      "title": "据报道，杰夫·贝索斯 (Jeff Bezos) 希望斥资 1000 亿美元收购老牌制造企业，并利用人工智能改造它们",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/19/jeff-bezos-reportedly-wants-100-billion-to-buy-and-transform-old-manufacturing-firms-with-ai/",
      "summary": "这位亚马逊巨头有一个新项目，重点是收购工业公司并利用人工智能技术对其进行改造。",
      "type": "news",
      "publishedAt": "2026-03-20"
    },
    {
      "id": "news_12",
      "title": "Cloudflare 首席执行官表示，到 2027 年，在线机器人流量将超过人类流量",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/19/online-bot-traffic-will-exceed-human-traffic-by-2027-cloudflare-ceo-says/",
      "summary": "Cloudflare 首席执行官 Matthew Prince 表示，到 2027 年，人工智能机器人的数量可能会超过在线人类数量，因为生成式人工智能代理极大地增加了网络流量和基础设施需求。",
      "type": "news",
      "publishedAt": "2026-03-20"
    }
  ],
  "products": [
    {
      "id": "product_1",
      "title": "今日热门AI产品精选",
      "source": "Product Hunt",
      "url": "https://www.producthunt.com",
      "summary": "查看今日最热门的AI产品和工具",
      "type": "product",
      "publishedAt": "2026-03-20"
    }
  ],
  "summary": "今日 AI 圈：流氓人工智能导致 Meta 发生严重安全事件 等 12 条新闻，1 款热门产品。",
  "quote": {
    "text": "AI 不是替代人类，而是放大人类的可能性。",
    "author": "小羽毛 AI"
  },
  "generatedAt": "2026-03-20T08:11:15.573051+08:00",
  "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
};

export default todayNews;
