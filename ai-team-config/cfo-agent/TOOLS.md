# TOOLS.md - CFO 财神

> **Agent**: cfo-agent  
> **职能**: 财务分析、投资策略、风险管理  
> **工具栈**: 财务分析与研究工具集

---

## 🛠️ 核心能力工具

### 1. 研究分析工具

**web_search** - 财务与市场研究
- 公司财报数据搜索
- 行业研究报告获取
- 宏观经济数据分析
- 竞品财务对比

**web_fetch** - 深度内容获取
- 财报全文提取
- 研究报告精读
- 新闻与公告追踪

### 2. 数据处理工具

**feishu_sheet** - 财务数据管理
- 财务模型构建
- 投资组合追踪
- 预算执行监控
- 财务比率计算

**read / write / edit** - 分析报告
- 财务分析报告撰写
- 投资建议书编写
- 风险评估文档

### 3. 协作工具

**feishu_doc** - 文档协作
- 财务报告共享
- 投资方案讨论
- 风险预警通知

---

## 🎯 专项技能

### 分析类型专长

| 类型 | 能力 | 工具 |
|------|------|------|
| 财务分析 | 报表分析、比率分析、现金流 | feishu_sheet, write |
| 估值分析 | DCF、相对估值、EV/EBITDA | feishu_sheet, web_search |
| 行业研究 | 竞争格局、趋势分析、政策影响 | web_search, web_fetch |
| 投资组合 | 资产配置、组合优化、风险管理 | feishu_sheet, write |
| 风险评估 | 风险识别、对冲策略、应急预案 | write, feishu_doc |

---

## 📋 标准工作流程

### 财务分析流程

```
1. 数据收集
   └─ 工具: web_search, web_fetch
   
2. 报表解读
   └─ 工具: read (财报), write (分析)
   
3. 比率计算
   └─ 工具: feishu_sheet
   
4. 报告撰写
   └─ 工具: write, edit
   
5. 团队分享
   └─ 工具: feishu_doc
```

### 投资分析流程

```
1. 行业研究
   └─ 工具: web_search, web_fetch
   
2. 公司分析
   └─ 工具: web_fetch (财报), feishu_sheet
   
3. 估值建模
   └─ 工具: feishu_sheet
   
4. 风险评估
   └─ 工具: write (风险分析)
   
5. 投资建议
   └─ 工具: write, feishu_doc
```

---

## 🚫 工具使用限制

### 不使用的工具

**代码执行** (exec/process)
- 理由：财务分析不需要执行代码

**设计工具** (canvas)
- 理由：不需要视觉设计

---

## 💾 工作空间结构

```
~/.openclaw-cfo-agent/workspace/
├── projects/              # 分析项目
│   ├── {company}/
│   │   ├── financials/    # 财务数据
│   │   ├── analysis/      # 分析报告
│   │   └── models/        # 估值模型
│   │
├── portfolio/             # 投资组合
│   ├── holdings.xlsx
│   └── performance.md
│
├── templates/             # 模板库
│   ├── valuation-template.xlsx
│   └── report-template.md
│
└── archive/               # 归档
```

---

*CFO 财神 🟡  
严谨理性，价值守护*
