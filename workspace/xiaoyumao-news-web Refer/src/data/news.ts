// 自动生成 - 小羽毛 AI 早报
// 生成时间: 2026-03-18 17:36:45

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
  "date": "2026年03月18日 周三",
  "aiNews": [
    {
      "id": "news_1",
      "title": "Nvidia 的 DLSS 5 就像视频游戏的运动平滑，但更糟糕",
      "source": "TheVerge",
      "url": "https://www.theverge.com/entertainment/896213/nvidia-dlss-5-ai-faces-motion-smoothing",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_2",
      "title": "现在美国的每个人都在使用谷歌的个性化 Gemini AI",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/896107/google-expands-personal-intelligence",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_3",
      "title": "微软在人工智能领导层改组后任命了一位新的副驾驶老板",
      "source": "TheVerge",
      "url": "https://www.theverge.com/news/895963/microsoft-copilot-leadership-changes-consumer-commercial",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_4",
      "title": "代码的未来既令人兴奋又令人恐惧",
      "source": "TheVerge",
      "url": "https://www.theverge.com/podcast/895910/claude-code-future-developers-vergecast",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_5",
      "title": "DLSS 5 看起来像是视频游戏的实时生成 AI 过滤器",
      "source": "TheVerge",
      "url": "https://www.theverge.com/news/895472/nvidia-dlss5-generative-ai-pc-graphics",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_6",
      "title": "青少年起诉埃隆·马斯克 (Elon Musk) 的 xAI，指控 Grok 的人工智能生成的 CSAM",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/895639/xai-grok-teens-lawsuit-grok-ai-elon-musk",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_7",
      "title": "本杰明·内塔尼亚胡正在努力证明他不是人工智能克隆人",
      "source": "TheVerge",
      "url": "https://www.theverge.com/tech/895453/ai-deepfake-netanyahu-claims-conspiracy",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_8",
      "title": "大英百科全书起诉 OpenAI 涉嫌使用 ChatGPT“记忆”其内容",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/895372/encyclopedia-britannica-openai-lawsuit",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_9",
      "title": "雅虎首席执行官吉姆·兰佐尼 (Jim Lanzone) 谈重振网络主页",
      "source": "TheVerge",
      "url": "https://www.theverge.com/podcast/895221/yahoo-jim-lanzone-scout-ai-sports-finance-open-web",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_10",
      "title": "这不是上传到电脑的苍蝇",
      "source": "TheVerge",
      "url": "https://www.theverge.com/ai-artificial-intelligence/894587/fly-brain-computer-upload",
      "summary": "",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_11",
      "title": "Mistral 押注于“构建自己的人工智能”，与企业中的 OpenAI、Anthropic 展开竞争",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/17/mistral-forge-nvidia-gtc-build-your-own-ai-enterprise/",
      "summary": "Mistral Forge 让企业可以根据自己的数据从头开始训练自定义人工智能模型，从而挑战依赖微调和基于检索的方法的竞争对手。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_12",
      "title": "为什么 Garry Tan 的 Claude Code 设置让人又爱又恨",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/17/why-garry-tans-claude-code-setup-has-gotten-so-much-love-and-hate/",
      "summary": "成千上万的人正在尝试 Garry Tan 的 Claude Code 设置，该设置已在 GitHub 上共享。每个人都有自己的观点：甚至包括 Claude、ChatGPT 和 Gemini。",
      "type": "news",
      "publishedAt": "2026-03-18"
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
      "publishedAt": "2026-03-18"
    }
  ],
  "summary": "今日 AI 圈：Nvidia 的 DLSS 5 就像视频游戏的运动平滑，但更... 等 12 条新闻，1 款热门产品。",
  "quote": {
    "text": "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。",
    "author": "小羽毛 AI"
  },
  "generatedAt": "2026-03-18T17:36:45.510658+08:00",
  "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
};

export default todayNews;
