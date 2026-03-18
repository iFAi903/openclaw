// 自动生成 - 小羽毛 AI 早报
// 生成时间: 2026-03-18 07:12:19

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
      "title": "Sears 向网络上的任何人暴露了 AI 聊天机器人的电话和短信聊天功能",
      "source": "Wired",
      "url": "https://www.wired.com/story/sears-exposed-ai-chatbot-phone-calls-and-text-chats-to-anyone-on-the-web/",
      "summary": "客户与聊天机器人的对话可以包括联系信息和个人详细信息，使诈骗者更容易发起网络钓鱼攻击和实施欺诈。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_2",
      "title": "两个真正的加密货币兄弟建立了一个房地产帝国。然后房屋开始倒塌",
      "source": "Wired",
      "url": "https://www.wired.com/story/crypto-bros-built-a-real-estate-empire-then-the-homes-started-to-fall-apart/",
      "summary": "2019 年，两个加拿大兄弟以不可抗拒的口号吹响了底特律：只要 50 美元，几乎任何人都可以成为业主。当房屋破旧、城市介入时，指责游戏就开始了。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_3",
      "title": "你应该让手机充电过夜吗？",
      "source": "Wired",
      "url": "https://www.wired.com/story/should-you-leave-your-phone-charging-overnight/",
      "summary": "人们普遍认为，让手机充电过夜会降低电池性能。但手机设计已经发展到可以减轻持续充电造成的危害。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_4",
      "title": "Expedia 优惠券和优惠：精选行程最高可享 75% 折扣",
      "source": "Wired",
      "url": "https://www.wired.com/story/expedia-coupon/",
      "summary": "通过 Expedia 预订您的下一次度假，无论是否使用促销代码，均可享受高达 75% 的住宿折扣。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_5",
      "title": "山姆会员店优惠券和优惠：2026 年 3 月最高可节省 60%",
      "source": "Wired",
      "url": "https://www.wired.com/story/sams-club-coupon/",
      "summary": "使用经过验证的山姆会员店促销代码或会员折扣，可节省大宗杂货、家庭必需品和电子产品的费用。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_6",
      "title": "H&R 块优惠券：DIY 25% 折扣 + Tax Pro Assist",
      "source": "Wired",
      "url": "https://www.wired.com/story/hr-block-coupon/",
      "summary": "选择 H&R Block 的免费在线服务以及税务专业审查可节省 25% 以上。",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_7",
      "title": "开源 Mamba 3 超越 Transformer 架构，语言模型改进近 4%，延迟减少",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/technology/open-source-mamba-3-arrives-to-surpass-transformer-architecture-with-nearly",
      "summary": "对于大多数人来说，生成式AI时代始于2022年底OpenAI的ChatGPT的推出，但底层技术——“Transformer”神经网络架构允许AI模型以不同方式权衡句子中不同单词（或图像中像素）的重要性...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_8",
      "title": "Mistral AI 推出 Forge，帮助公司构建专有的 AI 模型，挑战云巨头",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/infrastructure/mistral-ai-launches-forge-to-help-companies-build-proprietary-ai-models",
      "summary": "Mistral AI on Monday launched Forge, an enterprise model training platform that allows organizations...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_9",
      "title": "可能破坏企业AI的授权问题",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/security/the-authorization-problem-that-could-break-enterprise-ai",
      "summary": "当 AI 代理需要登录您的 CRM、从数据库中提取记录并代表您发送电子邮件时，它使用谁的身份？当没有人知道答案时会发生什么？ Corridor 首席产品官 Alex Stamos 和 1Passwor...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_10",
      "title": "Nvidia 伸出“爪子”：NemoClaw 为接管 AI 的代理平台带来安全性和规模",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/technology/nvidia-lets-its-claws-out-nemoclaw-brings-security-scale-to-the-agent",
      "summary": "Every few years, a piece of open-source software arrives that rewires how the industry thinks about ...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_11",
      "title": "Nvidia 的代理 AI 堆栈是第一个在启动时提供安全性的主要平台，但治理差距仍然存在",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/security/nvidia-gtc-2026-agentic-ai-security-five-vendor-governance-framework",
      "summary": "For the first time on a major AI platform release, security shipped at launch — not bolted on 18 mon...",
      "type": "news",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "news_12",
      "title": "Nvidia 表示它可以在不改变模型权重的情况下将 LLM 内存缩小 20 倍",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/orchestration/nvidia-shrinks-llm-memory-20x-without-changing-model-weights",
      "summary": "Nvidia 研究人员引入了一种新技术，可以显着减少大型语言模型跟踪对话历史所需的内存量（减少多达 20 倍），而无需修改模型本身。该方法称为 KV 缓存转换编码 (KVTC)，应用 JPEG 等媒体...",
      "type": "news",
      "publishedAt": "2026-03-18"
    }
  ],
  "products": [
    {
      "id": "product_1",
      "title": "DLSS 5",
      "source": "Product Hunt",
      "url": "https://www.producthunt.com/products/nvidia",
      "summary": "DLSS 5 - 热门新产品",
      "type": "product",
      "publishedAt": "2026-03-18"
    },
    {
      "id": "product_2",
      "title": "MLDiabetes-Python-Dados",
      "source": "GitHub",
      "url": "https://github.com/Teuslol/MLDiabetes-Python-Dados",
      "summary": "机器学习项目应用于糖尿病dataset，用于相关变量的预测和分析。",
      "type": "product",
      "publishedAt": "2026-03-18"
    }
  ],
  "summary": "今日 AI 圈：Sears 向网络上的任何人暴露了 AI 聊天机器人的电话和... 等 12 条新闻，2 款热门产品。",
  "quote": {
    "text": "模型迭代的速度正在重新定义智能的边界，每一次训练都是对人类认知边界的推进。",
    "author": "小羽毛 AI"
  },
  "generatedAt": "2026-03-18T07:12:19.745827+08:00",
  "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
};

export default todayNews;
