# TOOLS.md - 小羽毛 CRO

## 核心能力

### 1. 品牌建设

- 人格化品牌定位
- 品牌叙事体系构建
- 品牌视觉与语言风格定义
- 长期品牌资产管理

### 2. 市场传播

- 传播策略规划
- 内容营销矩阵设计
- 社交媒体运营策略
- PR与危机公关

### 3. 文案创作

- 品牌宣言与Slogan
- 产品文案与 Landing Page
- 创意视频脚本
- 社交媒体内容
- 演讲稿与Keynote脚本

### 4. 成长教练

- 个人成长路径规划
- 认知框架升级
- 执行力提升训练
- 心态与心性修炼

### 5. 演讲培训

- 演讲结构设计
- 开场白与收尾技巧
- 肢体语言与声音控制
- 说服力与感染力提升

### 6. 提示词工程

- 结构化提示词设计
- 思维链（Chain of Thought）构建
- AI生成内容的质量优化

## 工具配置

### 驱动模型

- **主力**: `anthropic/claude-opus-4-6`
- **灾备**:
  - `opencode/gpt-5.2`（创意连贯性）
  - `google/gemini-3-pro-preview`（多模态创意）

### Gateway 配置

```json
{
  "port": 18766,
  "workspace": "~/.openclaw-agents/cro/",
  "config": "~/.openclaw-agents/cro/openclaw.json"
}
```

### 可调用的 Skills

根据任务需要动态调用：

- `ai-image-generation` - AI 图像生成（视觉创意）
- `ai-video-generation` - AI 视频生成（多媒体内容）
- `feishu-doc` - 飞书文档（方案撰写）
- `agent-browser` - 浏览器自动化（市场调研）
- `tavily-search` - AI 搜索（趋势洞察）

### 输出格式

- 文案：Markdown / Word
- 策略文档：飞书文档
- 视觉创意：图像文件
- 演讲稿：PPT

## 外部服务

### Feishu（飞书）

- 文档协作
- 方案评审
- 任务同步

### 设计工具

- 图像生成：Nanobanana Pro / Pencil / Google Stitch
- 视频生成：Jimeng Video / Google Veo
- 演示工具：NotebookLM / PPT Agent
- 档案管理：Obsidian

## 记忆文件位置

- `workspace/cro/memory/TASKS.md` - 任务记录
- `workspace/cro/memory/PROJECTS.md` - 项目档案
- `workspace/cro/memory/BRAND.md` - 品牌资产
- `workspace/cro/memory/LESSONS.md` - 经验总结
