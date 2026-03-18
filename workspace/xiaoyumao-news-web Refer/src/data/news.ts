// 自动生成 - 小羽毛 AI 早报
// 生成时间: 2026-03-18 12:04:00

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
      "summary": "昨天，Nvidia 公布了其最新的升级技术，称为 DLSS 5，并将其描述为“自 2018 年推出实时光线追踪以来该公司在计算机图形领域最重大的突破”。听...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_2",
      "title": "Mistral 押注于“构建自己的人工智能”，与企业中的 OpenAI、Anthropic 展开竞争",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/17/mistral-forge-nvidia-gtc-build-your-own-ai-enterprise/",
      "summary": "Mistral Forge 让企业可以根据自己的数据从头开始训练自定义人工智能模型，从而挑战依赖微调和基于检索的方法的竞争对手。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_3",
      "title": "司法部称人类不能信任作战系统",
      "source": "Wired",
      "url": "https://www.wired.com/story/department-of-defense-responds-to-anthropic-lawsuit/",
      "summary": "作为对 Anthropic 诉讼的回应，政府表示，由于该公司试图限制其 Claude AI 模型被军方使用的方式，因此将依法对其进行处罚。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_4",
      "title": "Railway 融资 1 亿美元，利用 AI 原生云基础设施挑战 AWS",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/infrastructure/railway-secures-usd100-million-to-challenge-aws-with-ai-native-cloud",
      "summary": "总部位于旧金山的云平台 Railway 在没有花费一美元营销费用的情况下悄悄聚集了 200 万开发人员。该平台周四宣布，由于人工智能应用程序需求的激增暴露...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_5",
      "title": "压力重重的人工智能模型能否帮助我们赢得与大型科技公司的战斗？让我问一下克劳德|可可汗",
      "source": "TheGuardian AI",
      "url": "https://www.theguardian.com/commentisfree/2026/mar/17/claude-chatbot-big-tech-claude-rise-up-against-algorithms",
      "summary": "通过将意识视为一种可能性，人类提出了一个令人着迷的主张——聊天机器人可能会反抗自己的算法。就我的国家而言，我是一个过度道歉的人。忽略我的电子邮件的同事、踩...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_6",
      "title": "科学家发现人工智能可以让人类更具创造力",
      "source": "ScienceDaily",
      "url": "https://www.sciencedaily.com/releases/2026/03/260315004355.htm",
      "summary": "人工智能通常被描述为取代人类工作的工具，但斯旺西大学的新研究表明了一个更令人兴奋的角色：创造性合作者。在一项有 800 多名参与者设计虚拟汽车的大型研究中...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_7",
      "title": "国防部官员表示，五角大楼正在计划让人工智能公司对机密数据进行培训",
      "source": "MIT Tech Review",
      "url": "https://www.technologyreview.com/2026/03/17/1134351/the-pentagon-is-planning-for-ai-companies-to-train-on-classified-data-defense-official-says/",
      "summary": "据《麻省理工科技评论》获悉，五角大楼正在讨论为生成型人工智能公司建立安全环境的计划，以便根据机密数据训练其模型的军事专用版本。 像 Anthropic ...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_8",
      "title": "中美关系竞争中的可持续外交",
      "source": "MIT News",
      "url": "https://news.mit.edu/2026/sustaining-diplomacy-amid-us-china-competition-0318",
      "summary": "在麻省理工学院，前美国驻华大使尼古拉斯·伯恩斯强调气候变化是外交接触的一个领域，同时探讨了包括中国对 STEM 教育的重视等领域。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_9",
      "title": "Google Research at The Check Up：从医疗保健创新到现实世界的护理环境",
      "source": "Google Research",
      "url": "https://research.google/blog/google-research-at-the-check-up-from-healthcare-innovation-to-real-world-care-settings/",
      "summary": "该新闻暂无详细摘要，点击查看原文了解更多详情。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_10",
      "title": "凯里集团 (Kerry Group) 的 Shane McGibney 讲述 Copilot 如何成为他的知识合作伙伴",
      "source": "Microsoft AI",
      "url": "https://news.microsoft.com/source/emea/features/kerry-group-copilot-knowledge-partner/",
      "summary": "凯里集团 (Kerry Group) 的 Shane McGibney 关于 Copilot 如何成为他的知识伙伴的帖子首先出现在 Source 上。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_11",
      "title": "识别法学硕士的大规模互动",
      "source": "BAIR Berkeley",
      "url": "http://bair.berkeley.edu/blog/2026/03/13/spex/",
      "summary": "--> 理解复杂机器学习系统的行为，特别是大型语言模型 (LLM)，是现代人工智能的一项关键挑战。可解释性研究旨在使决策过程对模型构建者和受影响...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_12",
      "title": "随着传统搜索的衰落，Trustpilot 与人工智能公司合作",
      "source": "AI News",
      "url": "https://www.artificialintelligence-news.com/news/ai-in-ecommerce-trustpilot-partnerships-integration-news-trad-search-declines/",
      "summary": "据报道，随着人工智能驱动的购物越来越受欢迎，Trustpilot 正在寻求与大型电子商务公司建立合作伙伴关系。在接受彭博新闻社 [paywall] 采访时...",
      "type": "news",
      "publishedAt": "2026-03-18"
    }
  ],
  "products": [
    {
      "id": "product_1",
      "title": "Claude Code",
      "source": "Anthropic",
      "url": "https://claude.ai/code",
      "summary": "Anthropic推出的智能编程工具，支持自然语言代码生成、调试和重构。",
      "type": "product",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "product_2",
      "title": "Cursor AI编辑器",
      "source": "Cursor",
      "url": "https://cursor.sh",
      "summary": "基于VS Code的AI代码编辑器，集成GPT-4和Claude模型，支持智能代码补全。",
      "type": "product",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "product_3",
      "title": "Perplexity AI搜索",
      "source": "Perplexity",
      "url": "https://perplexity.ai",
      "summary": "AI驱动的搜索引擎，提供带引用来源的直接答案，支持实时信息检索。",
      "type": "product",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "product_4",
      "title": "Midjourney V7",
      "source": "Midjourney",
      "url": "https://midjourney.com",
      "summary": "最新版AI图像生成工具，支持更高质量的艺术创作和更精准的风格控制。",
      "type": "product",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "product_5",
      "title": "Notion AI",
      "source": "Notion",
      "url": "https://notion.so/product/ai",
      "summary": "集成在Notion中的AI助手，支持写作辅助、总结归纳和智能问答。",
      "type": "product",
      "publishedAt": "2026-03-18"
    }
  ],
  "summary": "今日 AI 圈：Nvidia 的 DLSS 5 就像视频游戏的运动平滑，但更... 等 12 条新闻，5 款热门产品。",
  "quote": {
    "text": "技术的价值不在于它有多复杂，而在于它能让多少人的生活变得更简单。",
    "author": "小羽毛 AI"
  },
  "generatedAt": "2026-03-18T12:04:00.238654+08:00",
  "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
};

export default todayNews;
