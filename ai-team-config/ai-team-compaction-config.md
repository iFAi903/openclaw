# AI 天团 Compaction 配置方案

> **版本**: 2.0  
> **制定日期**: 2026-03-05  
> **制定者**: 小羽毛 🪶

---

## 🎯 配置策略总览

| Agent | 颜色 | 职能 | 模式 | 触发条件 | 原因 |
|-------|------|------|------|---------|------|
| **copy-agent** | ⚪ 白 | 文案/策划 | periodic | 8 turns | 创意迭代，保持风格一致性 |
| **product-agent** | 🟣 紫 | 产品/PRD | periodic | 10 turns | 需求分析，保留调研脉络 |
| **design-agent** | 🟡 金 | 设计/原型 | periodic | 8 turns | 视觉决策，保留设计思路 |
| **dev-agent** | 🔵 蓝 | 开发/部署 | safeguard | 80K tokens | 代码实现，保留完整技术历史 |

---

## 📋 详细配置方案

### 1️⃣ 白色小羽毛 (copy-agent)

**工作特点分析**:

- 多轮文案迭代修改
- 需要保持风格调性一致
- 单次任务通常 10-20 轮
- 关键词：风格、受众、创意方向

**推荐配置**:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3.1-pro-preview"
      },
      "thinking": "high",
      "compaction": {
        "mode": "periodic",
        "interval": 8,
        "intervalType": "turns",
        "summaryModel": "google/gemini-3-flash-preview",
        "summaryPrompt": "保留文案创作项目的关键信息：\n1. 创作主题、目标受众和传播目标\n2. 已确定的文案风格、调性和品牌声音\n3. 当前文案版本和修改方向\n4. 用户反馈的核心要点\n5. 任何关键的金句或创意概念\n\n对话内容：{{history}}"
      }
    }
  }
}
```

**设计理由**:

- ✅ **periodic + 8 turns**: 创意工作每 8 轮压缩一次，平衡迭代深度和 token 使用
- ✅ **自定义摘要**: 确保保留风格、受众、关键创意等核心信息
- ✅ **轻量级 summaryModel**: 使用 Flash 降低成本

---

### 2️⃣ 紫色小羽毛 (product-agent)

**工作特点分析**:

- 需求分析、市场调研、竞品分析
- PRD 文档撰写，逻辑链条长
- 单次任务通常 15-30 轮
- 关键词：需求、用户、功能、优先级

**推荐配置**:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4.6"
      },
      "thinking": "high",
      "compaction": {
        "mode": "periodic",
        "interval": 10,
        "intervalType": "turns",
        "summaryModel": "anthropic/claude-sonnet-4.6",
        "summaryPrompt": "保留产品策划项目的关键信息：\n1. 产品定位和目标用户画像\n2. 核心需求和痛点分析\n3. 功能优先级和 MVP 范围\n4. 竞品分析的关键洞察\n5. 已做出的产品决策及其理由\n6. 当前进展和待确认事项\n\n对话内容：{{history}}"
      }
    }
  }
}
```

**设计理由**:

- ✅ **periodic + 10 turns**: 产品分析通常更长，10 轮压缩保留更多上下文
- ✅ **Sonnet summaryModel**: 产品分析需要一定推理能力，Sonnet 比 Flash 更适合
- ✅ **结构化摘要**: 产品决策需要可追溯，摘要保留决策理由

---

### 3️⃣ 金色小羽毛 (design-agent)

**工作特点分析**:

- 设计策略制定、视觉规范
- 原型图提示词生成
- 单次任务通常 10-20 轮
- 关键词：风格、配色、布局、用户体验

**推荐配置**:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google/gemini-3.1-pro-preview"
      },
      "thinking": "high",
      "compaction": {
        "mode": "periodic",
        "interval": 8,
        "intervalType": "turns",
        "summaryModel": "google/gemini-3-pro-preview",
        "summaryPrompt": "保留设计项目的关键信息：\n1. 设计风格方向和视觉调性\n2. 配色方案和设计系统决策\n3. 关键页面的布局和交互设计\n4. 生成的原型图提示词集合\n5. 用户反馈的设计修改方向\n6. 设计规范和组件库定义\n\n对话内容：{{history}}"
      }
    }
  }
}
```

**设计理由**:

- ✅ **periodic + 8 turns**: 与 copy-agent 相同，设计也需要频繁迭代
- ✅ **保留提示词**: 原型图提示词是重要输出，需在摘要中保留
- ✅ **Flash summaryModel**: 设计摘要不需要复杂推理，Flash 足够

---

### 4️⃣ 蓝色小羽毛 (dev-agent)

**工作特点分析**:

- 代码实现、技术方案设计
- 错误调试、代码审查
- 单次任务可能 30-100+ 轮
- 关键词：代码、架构、Bug、部署

**推荐配置**:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/k2p5"
      },
      "thinking": "high",
      "workspace": "~/.openclaw-dev-agent/workspace",
      "compaction": {
        "mode": "safeguard",
        "thresholdTokens": 80000,
        "reserveTokens": 40000,
        "summaryModel": "google/gemini-3-pro-preview",
        "summaryPrompt": "保留开发项目的核心技术信息：\n1. 技术栈和架构设计决策\n2. 当前实现的功能模块和代码位置\n3. 遇到的关键 Bug 和解决方案\n4. 技术债务和待优化事项\n5. 下一步开发计划和优先级\n\n对话内容：{{history}}"
      }
    }
  }
}
```

**设计理由**:

- ✅ **safeguard 模式**: 开发需要完整保留技术决策历史
- ✅ **80K threshold**: 提前触发，为代码生成预留 40K 空间
- ✅ **大 reserve**: 代码生成通常需要大量 token
- ✅ **文件持久化**: 代码本身保存在 workspace，补充上下文

---

## 🔧 配置文件生成脚本

```bash
#!/bin/bash
# 应用 AI 天团 compaction 配置

echo "🪶 配置 AI 天团 Compaction 策略"
echo "================================"

# 白色小羽毛 - 文案
echo "📝 配置白色小羽毛 (copy-agent)..."
openclaw --profile copy-agent config set agents.defaults.compaction.mode "periodic"
openclaw --profile copy-agent config set agents.defaults.compaction.interval 8
openclaw --profile copy-agent config set agents.defaults.compaction.intervalType "turns"
openclaw --profile copy-agent config set agents.defaults.compaction.summaryModel "google/gemini-3-pro-preview"

# 紫色小羽毛 - 产品
echo "📊 配置紫色小羽毛 (product-agent)..."
openclaw --profile product-agent config set agents.defaults.compaction.mode "periodic"
openclaw --profile product-agent config set agents.defaults.compaction.interval 10
openclaw --profile product-agent config set agents.defaults.compaction.intervalType "turns"
openclaw --profile product-agent config set agents.defaults.compaction.summaryModel "anthropic/claude-sonnet-4.5"

# 金色小羽毛 - 设计
echo "🎨 配置金色小羽毛 (design-agent)..."
openclaw --profile design-agent config set agents.defaults.compaction.mode "periodic"
openclaw --profile design-agent config set agents.defaults.compaction.interval 8
openclaw --profile design-agent config set agents.defaults.compaction.intervalType "turns"
openclaw --profile design-agent config set agents.defaults.compaction.summaryModel "google/gemini-3-pro-preview"

# 蓝色小羽毛 - 开发
echo "💻 配置蓝色小羽毛 (dev-agent)..."
openclaw --profile dev-agent config set agents.defaults.compaction.mode "safeguard"
openclaw --profile dev-agent config set agents.defaults.compaction.thresholdTokens 80000
openclaw --profile dev-agent config set agents.defaults.compaction.reserveTokens 40000
openclaw --profile dev-agent config set agents.defaults.compaction.summaryModel "google/gemini-3-pro-preview"

echo ""
echo "✅ AI 天团 Compaction 配置完成！"
echo ""
echo "配置摘要："
echo "  📝 白色小羽毛: periodic, 8 turns"
echo "  📊 紫色小羽毛: periodic, 10 turns"
echo "  🎨 金色小羽毛: periodic, 8 turns"
echo "  💻 蓝色小羽毛: safeguard, 80K tokens"
```

---

## 📊 配置对比矩阵

| 特性 | 白色 | 紫色 | 金色 | 蓝色 |
|------|------|------|------|------|
| **模式** | periodic | periodic | periodic | safeguard |
| **触发** | 8 turns | 10 turns | 8 turns | 80K tokens |
| **Summary Model** | Flash | Sonnet | Flash | Flash |
| **保留重点** | 风格/受众 | 需求/决策 | 设计/提示词 | 代码/架构 |
| **成本** | 低 | 中 | 低 | 低 |

---

## 🎯 关键设计决策说明

### 为什么 dev-agent 用 safeguard，其他用 periodic？

**开发工作的特殊性**:

- 代码实现通常 30-100+ 轮，远超其他 Agent
- 技术决策需要完整历史（"为什么选 React 而不是 Vue"）
- Bug 调试需要追溯之前的尝试

**其他工作的共性**:

- 文案/产品/设计通常在 10-20 轮内完成
- 可以定期摘要而不丢失关键信息
- 迭代性质强，定期压缩有助于聚焦

### 为什么紫色小羽毛用 Sonnet 做 summaryModel？

- 产品分析涉及需求推理和决策权衡
- Sonnet 比 Flash 在逻辑推理上更强
- 确保摘要准确捕捉需求优先级和决策逻辑

---

## 📝 验证清单

配置完成后，验证以下事项：

- [ ] 各 Agent 的 openclaw.json 包含 compaction 配置
- [ ] 重启 Gateway 后配置生效
- [ ] 长对话测试（超过触发阈值）验证压缩行为
- [ ] 检查摘要内容是否符合预期

---

## 🚀 后续优化建议

1. **监控阶段** (1周内)
   - 观察各 Agent 的 token 使用情况
   - 检查压缩是否过于频繁或稀疏

2. **调优阶段** (2-4周)
   - 根据实际使用情况调整 threshold/interval
   - 优化自定义摘要提示词

3. **文档化** (持续)
   - 记录最佳实践
   - 更新本配置文档

---

*AI 天团 Compaction 配置方案 v2.0*  
*为高效协作而生 🪶*
