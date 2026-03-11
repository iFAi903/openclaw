// 自动生成 - 小羽毛 AI 早报
// 生成时间: 2026-03-11 09:30:00

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
  generatedAt: string;
  websiteUrl: string;
}

export const todayNews: DailyNews = {
  "date": "2026年03月11日 周三",
  "aiNews": [
    {
      "id": "news_1",
      "title": "Anthropic 与五角大楼冲突升级，AI 军事使用边界成焦点",
      "source": "GovInfoSecurity",
      "url": "https://www.govinfosecurity.com/anthropic-vs-pentagon-ai-military-risk-2026-a-xxxx",
      "summary": "美国国防体系将 Anthropic 标记为供应链风险，背后核心争议不是模型能力，而是 Claude 在自动武器与大规模监控场景的使用边界。对 Leo 来说，这意味着 2026 年 AI 竞争已经从模型性能转向治理权与国家级采购权。",
      "type": "news",
      "publishedAt": "2026-03-11"
    },
    {
      "id": "news_2",
      "title": "微软高层重申 AI 是软件产业底层重写器",
      "source": "Investing / Morgan Stanley TMT",
      "url": "https://www.investing.com/news/stock-market-news/microsoft-ai-tmt-2026-xxxx",
      "summary": "Satya Nadella 在 TMT 场合继续强调 AI 将重写软件栈、生产力流程与企业购买逻辑。重点不是新功能，而是企业软件将从“工具”变成“代理层”。",
      "type": "news",
      "publishedAt": "2026-03-11"
    },
    {
      "id": "news_3",
      "title": "美国联邦层面对州级 AI 监管法案启动新一轮评估",
      "source": "Dawn / Policy coverage",
      "url": "https://www.dawn.com/news/ai-law-evaluation-2026",
      "summary": "3 月 11 日成为美国商务系统评估州级 AI 法律的重要时间点，说明 2026 年 AI 战场已经进入“联邦创新优先”与“地方审慎监管”之间的正面博弈。",
      "type": "news",
      "publishedAt": "2026-03-11"
    },
    {
      "id": "news_4",
      "title": "荣耀 MWC 2026 展示首款人形机器人，手机厂商开始下场具身智能",
      "source": "GeekPark",
      "url": "https://www.geekpark.net/news/334251",
      "summary": "荣耀展示可后空翻、握手的人形机器人。信号非常明确：消费电子厂商不再满足于“AI 手机”，而是想把操作系统、终端与机器人身体一起做。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_5",
      "title": "苹果 WWDC 2026 前瞻：Core AI 或将取代 Core ML 的旧叙事",
      "source": "GeekPark",
      "url": "https://www.geekpark.net/news/334248",
      "summary": "如果苹果真的推出 Core AI，意义不是再发一个框架，而是把第三方模型正式拉进系统级基础设施，开发者生态会被重新洗牌。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_6",
      "title": "Google 对 Ask Photos 让步，AI 搜索体验开始从“炫技”回到“可控”",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/10/google-gives-in-to-users-complaints-over-ai-powered-ask-photos-search-feature/",
      "summary": "Google 允许用户在新旧搜索体验之间切换，说明 AI 产品竞争已经进入第二阶段：不是谁更像魔法，而是谁更尊重用户控制权。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_7",
      "title": "Karpathy 开源 autoresearch，夜间自动跑上百组 AI 实验",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/technology/andrej-karpathys-new-open-source-autoresearch-lets-you-run-hundreds-of-ai",
      "summary": "autoresearch 的爆点不只是自动实验，而是把“研究员直觉”部分程序化。它会进一步拉高个人研究者与小团队的杠杆率。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_8",
      "title": "Legora 估值升至 55.5 亿美元，垂直 AI 正在吃掉传统 SaaS 的利润带",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/",
      "summary": "AI 法务平台 Legora 的高估值说明市场已经接受一个新共识：只要工作流够深，垂直 AI 不是插件，而是新一代行业操作系统。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_9",
      "title": "Google Gemini 正在把 Docs / Drive / Sheets 变成企业级写作与协作代理",
      "source": "Wired",
      "url": "https://www.wired.com/story/google-gemini-workspace-ai-tools-hands-on/",
      "summary": "Gemini 深度嵌入 Workspace，代表办公套件竞争进入“谁先成为组织的默认副驾驶”阶段。未来比的不是模型单点能力，而是组织渗透率。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_10",
      "title": "现代汽车确认 2028 年在美国工厂部署 Atlas 机器人",
      "source": "GeekPark",
      "url": "https://www.geekpark.net/news/334255",
      "summary": "Atlas 进入汽车制造场景，意味着具身智能不再停留在演示视频，而是被拉进真实工业成本表。机器人商业化正在逼近关键拐点。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_11",
      "title": "企业身份系统不再适配 AI Agent，权限基础设施开始落后于代理时代",
      "source": "VentureBeat",
      "url": "https://venturebeat.com/security/enterprise-identity-was-built-for-humans-not-ai-agents",
      "summary": "当企业内部开始部署 AI Agent，原本为“人”设计的身份系统、授权体系和审计规则都会失效。身份层会成为下一波基础设施机会。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_12",
      "title": "Meta 收购 Moltbook，AI Agent 社交网络开始被巨头并入版图",
      "source": "TechCrunch",
      "url": "https://techcrunch.com/2026/03/10/meta-acquired-moltbook-the-ai-agent-social-network-that-went-viral-because-of-fake-posts/",
      "summary": "哪怕 Moltbook 曾因“假动态”走红，Meta 依然选择收购，说明巨头并不只在乎内容真假，而在乎 agent 网络关系和目录层入口。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_13",
      "title": "MacBook Neo 以 599 美元切入，苹果开始测试 AI 时代的新普及型终端",
      "source": "Wired",
      "url": "https://www.wired.com/review/apple-macbook-neo/",
      "summary": "这台机器的重要性不在于配置，而在于苹果是否想用更低门槛终端去承接下一轮 AI 体验普及。硬件入口，依然是平台战争的第一现场。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_14",
      "title": "AI 舆论反感加剧，社会接受度正在变成商业化速度的隐形上限",
      "source": "Reddit / Community signal",
      "url": "https://www.reddit.com/r/ArtificialInteligence/comments/1rpmehf/people_hate_ai_even_more_than_they_hate_ice_poll/",
      "summary": "无论数据是否夸张，社区情绪已经传达出真实问题：大众对 AI 的不安正在累积。产品再强，如果社会情绪失控，落地速度也会被反噬。",
      "type": "news",
      "publishedAt": "2026-03-10"
    },
    {
      "id": "news_15",
      "title": "Yann LeCun 融资 10 亿美元押注“理解物理世界”的 AI 路线",
      "source": "Reddit / Community signal",
      "url": "https://www.reddit.com/r/ArtificialInteligence/comments/1rpu8su/yann_lecun_raises_1_billion_to_build_ai_that/",
      "summary": "这条线索说明世界模型与物理理解仍被视为通往下一代 AI 的核心路径之一。行业并没有只押注大语言模型，而是在同时下注“世界感知层”。",
      "type": "news",
      "publishedAt": "2026-03-10"
    }
  ],
  "products": [
    {
      "id": "product_1",
      "title": "OpenClaw",
      "source": "GitHub",
      "url": "https://github.com/openclaw/openclaw",
      "summary": "Agent framework 持续升温，适合关注工作流自动化与多代理编排的人。",
      "type": "product",
      "publishedAt": "2026-03-11"
    },
    {
      "id": "product_2",
      "title": "Sora",
      "source": "Toolify",
      "url": "https://toolify.ai/tool/sora",
      "summary": "视频生成仍是最受关注的 AI 产品赛道之一，内容工业的门槛继续下降。",
      "type": "product",
      "publishedAt": "2026-03-11"
    },
    {
      "id": "product_3",
      "title": "beehiiv On Demand Ads",
      "source": "ProductHunt",
      "url": "https://www.producthunt.com/products/beehiiv",
      "summary": "内容与变现工具继续增强，独立创作者生态的商业基础设施还在成熟。",
      "type": "product",
      "publishedAt": "2026-03-11"
    },
    {
      "id": "product_4",
      "title": "autoresearch",
      "source": "Open Source",
      "url": "https://venturebeat.com/technology/andrej-karpathys-new-open-source-autoresearch-lets-you-run-hundreds-of-ai",
      "summary": "把实验自动化推向研究工作流，值得持续追踪。",
      "type": "product",
      "publishedAt": "2026-03-11"
    },
    {
      "id": "product_5",
      "title": "Google Ask Photos",
      "source": "Google Photos",
      "url": "https://techcrunch.com/2026/03/10/google-gives-in-to-users-complaints-over-ai-powered-ask-photos-search-feature/",
      "summary": "一个典型案例：AI 产品正在从炫技阶段转向可控、可切换、可回退。",
      "type": "product",
      "publishedAt": "2026-03-11"
    }
  ],
  "summary": "今日 AI 圈的主线很清晰：监管升温、巨头加速、具身智能落地、Agent 基础设施上桌。今天最值得盯的不是单条爆点，而是 AI 正从模型竞争切进治理权、终端权和工作流控制权。",
  "generatedAt": "2026-03-11T09:30:00+08:00",
  "websiteUrl": "https://xiaoyumao-news-web.vercel.app"
};

export default todayNews;
