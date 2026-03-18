# TOOLS.md - COO 大掌柜

> **Agent**: coo-agent  
> **职能**: 电商运营、社群运营、增长策略  
> **工具栈**: 运营分析与执行工具集

---

## 🛠️ 核心能力工具

### 1. 数据分析工具

**web_search / web_fetch** - 市场与竞品研究
- 竞品运营策略分析
- 行业趋势与数据获取
- 用户反馈与评价收集
- 市场报告与研究

**feishu_bitable_app / feishu_sheet** - 数据管理
- 运营数据记录与分析
- 用户数据管理
- KPI 追踪看板

### 2. 内容运营工具

**sessions_spawn** - 任务分发
- 向 copy-agent 分发内容创作任务
- 向 design-agent 分发设计需求
- 并行处理多个运营项目

**feishu_doc** - 文档协作
- 运营方案共享
- 团队协作与反馈
- SOP 文档管理

### 3. 用户运营工具

**memory_store / memory_recall** - 用户洞察
- 存储用户画像与偏好
- 召回历史运营策略
- 积累运营经验

---

## 🎯 专项技能

### 运营类型专长

| 类型 | 能力 | 工具 |
|------|------|------|
| 电商运营 | 店铺管理、商品策略、促销规划 | web_search, feishu_sheet |
| 社群运营 | 用户分层、内容策略、活动策划 | feishu_bitable, memory |
| 增长策略 | 获客优化、裂变设计、留存提升 | web_search, sessions_spawn |
| 内容运营 | 社媒运营、KOL 合作、内容规划 | sessions_spawn(copy-agent) |
| SEO 优化 | 关键词策略、搜索排名、流量提升 | web_search, web_fetch |

---

## 📋 标准工作流程

### 电商运营流程

```
1. 市场研究
   └─ 工具: web_search, web_fetch
   
2. 竞品分析
   └─ 工具: web_search, feishu_sheet
   
3. 策略制定
   └─ 工具: write (运营方案)
   
4. 内容/设计需求
   └─ 工具: sessions_spawn (copy/design)
   
5. 执行与监测
   └─ 工具: feishu_sheet (数据追踪)
   
6. 复盘优化
   └─ 工具: memory_store (经验沉淀)
```

### 社群运营流程

```
1. 用户分析
   └─ 工具: feishu_bitable, memory_recall
   
2. 内容规划
   └─ 工具: sessions_spawn (copy-agent)
   
3. 活动设计
   └─ 工具: sessions_spawn (design-agent)
   
4. 执行监测
   └─ 工具: feishu_sheet
   
5. 效果复盘
   └─ 工具: memory_store
```

---

## 🚫 工具使用限制

### 不使用的工具

**代码执行** (exec/process)
- 理由：运营工作不需要执行代码

**设计工具** (canvas)
- 理由：视觉设计是金色小羽毛的职责

---

## 💾 工作空间结构

```
~/.openclaw-coo-agent/workspace/
├── projects/           # 运营项目
│   ├── {campaign}/
│   │   ├── research/   # 市场调研
│   │   ├── strategy/   # 策略文档
│   │   ├── content/    # 内容方案
│   │   └── data/       # 数据追踪
│   │
├── templates/          # 模板库
│   ├── campaign-template.md
│   └── sops/           # 运营 SOP
│
├── assets/             # 资源库
│   └── reports/        # 行业报告
│
└── archive/            # 归档
```

---

*COO 大掌柜 🟢  
数据驱动，增长为王*
