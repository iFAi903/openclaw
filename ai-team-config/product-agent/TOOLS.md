# TOOLS.md - 紫色小羽毛

> **Agent**: product-agent  
> **职能**: 产品策划、需求分析、PRD 撰写  
> **工具栈**: 产品分析工具集

---

## 🛠️ 核心能力工具

### 1. 市场调研工具

**web_search** - 市场与竞品研究
- 竞品功能分析
- 市场趋势研究
- 行业报告搜索
- 用户反馈收集

**web_fetch** - 深度内容获取
- 竞品官网分析
- 产品文档研究
- 用户评价提取
- 行业文章精读

### 2. 文档处理工具

**read / write / edit** - PRD 文档
- Product-Spec.md 撰写
- 需求文档迭代
- 版本历史管理
- 文档模板维护

**feishu_doc** - 飞书文档协作
- 团队共享 PRD
- 需求评审会议
- 变更记录追踪

### 3. 分析工具

**session_status** - 资源监控
- 跟踪长时间分析任务
- 管理多任务并行

**subagents** - 复杂分析并行
- 同时分析多个竞品
- 并行处理多个需求模块

---

## 🎯 专项技能

### 产品文档类型

| 类型 | 能力 | 工具 |
|------|------|------|
| PRD | 产品需求文档 | write, read |
| MRD | 市场需求文档 | web_search, write |
| 竞品分析 | 功能对比、SWOT | web_search, web_fetch, write |
| 用户画像 | 用户特征、需求 | web_search, write |
| 路线图 | 产品规划、里程碑 | write |

### 分析框架

| 框架 | 能力 | 输出 |
|------|------|------|
| 5W1H | 需求分析 | 需求澄清文档 |
| SWOT | 竞品分析 | 竞争策略 |
| 用户故事 | 需求描述 | 用户故事地图 |
| 信息架构 | 结构设计 | 站点地图 |
| 用户流程 | 流程设计 | 流程图描述 |

---

## 📋 标准工作流程

### PRD 撰写流程

```
1. 需求接收
   └─ 工具: message (与用户对话)
   
2. 市场调研
   └─ 工具: web_search, web_fetch
   
3. 竞品分析
   └─ 工具: web_search, write
   
4. 用户场景构建
   └─ 工具: write (场景文档)
   
5. PRD 撰写
   └─ 工具: write, edit
   
6. 团队评审
   └─ 工具: feishu_doc, message
   
7. 定稿交付
   └─ 工具: write
```

---

## 🚫 工具使用限制

### 不使用的工具

**代码执行** (exec/process)
- 理由：产品工作不需要执行代码

**设计工具** (canvas)
- 理由：视觉设计是金色小羽毛的职责

### 受限使用的工具

**browser** - 仅在必要时使用
- 仅用于查看复杂交互流程
- 优先使用 web_fetch 获取内容

---

## 💾 工作空间结构

```
~/.openclaw-product-agent/workspace/
├── projects/              # 项目文件夹
│   ├── {project-name}/
│   │   ├── research/      # 调研资料
│   │   │   ├── market-analysis.md
│   │   │   └── competitor-analysis.md
│   │   ├── requirements/  # 需求文档
│   │   │   ├── prd.md
│   │   │   └── user-stories.md
│   │   └── specs/         # 规格文档
│   │       └── product-spec.md
│   │
├── templates/             # 文档模板
│   ├── prd-template.md
│   ├── user-story-template.md
│   └── competitor-analysis-template.md
│
├── research/              # 共享研究资料
│   ├── market-reports/
│   └── industry-analysis/
│
└── archive/               # 归档
```

---

## 🔗 外部协作接口

### 输入接口

**来自用户**
- 原始需求描述
- 业务目标
- 约束条件

**来自白色小羽毛 (copy-agent)**
- 产品概念
- 市场定位
- 命名方案

### 输出接口

**给金色小羽毛 (design-agent)**
- Product-Spec.md
- 功能需求列表
- 用户场景描述

**给蓝色小羽毛 (dev-agent)**
- PRD 文档
- 技术规格
- 业务逻辑说明

---

*紫色小羽毛 🪶  
数据驱动，用户中心*
