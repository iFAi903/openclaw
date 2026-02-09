---
name: vibecoding-framework-selector
description: Vibe Coding 开发框架选型助手。帮助用户在 BMad、Spec Kit、OpenSpec 三个框架中选择最适合项目需求的方案。根据项目复杂度、团队规模、技术栈等因素提供个性化推荐。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎸",
        "version": "1.0.0",
        "author": "Leo & 小羽毛",
        "license": "MIT",
      },
  }
---

# Vibe Coding 框架选型助手

帮助开发者在 BMad、Spec Kit、OpenSpec 三个主流 Vibe Coding 框架中做出最优选择。

## 三框架速览

| 框架 | 定位 | 复杂度 | 适用场景 |
|------|------|--------|----------|
| **BMad** | 企业级全流程 | ⭐⭐⭐⭐⭐ | 复杂项目、企业系统、游戏开发 |
| **Spec Kit** | 规范驱动开发 | ⭐⭐⭐ | 新产品开发、团队规范、GitHub生态 |
| **OpenSpec** | 轻量级迭代 | ⭐⭐ | 快速原型、个人项目、遗留系统改造 |

## 使用方法

当用户询问 Vibe Coding 框架选择时，通过以下步骤引导：

### 步骤1：收集项目信息

询问以下关键维度：

1. **项目类型**
   - 全新产品（Greenfield）vs 遗留系统改造（Brownfield）
   - 个人项目 vs 团队项目 vs 企业项目
   - Web应用 / 移动应用 / 游戏 / 工具 / 其他

2. **项目复杂度**
   - 简单：单一功能，1-2周完成
   - 中等：多模块产品，1-3个月
   - 复杂：平台级系统，3个月以上

3. **团队规模**
   - 1-2人（个人/结对）
   - 3-10人（小团队）
   - 10-50人（中型团队）
   - 50+人（大型/多团队）

4. **技术栈偏好**
   - 主要使用的 AI 工具（Claude Code / Cursor / Copilot 等）
   - 编程语言/框架偏好

5. **特殊需求**
   - 是否需要严格测试策略？
   - 是否有合规/安全要求？
   - 是否需要多Agent协作？

### 步骤2：应用决策矩阵

根据收集的信息，参考以下决策逻辑：

#### 按项目复杂度

```
简单项目（1-2周）     → OpenSpec
  └─ 快速上手，不繁琐

中等项目（1-3个月）   → Spec Kit
  └─ 规范流程，团队协作

复杂项目（3个月+）    → BMad
  └─ 完整流程，专业Agent支持
```

#### 按团队规模

```
1-2人    → OpenSpec
3-10人   → Spec Kit 或 OpenSpec
10-50人  → BMad Method
50+人    → BMad Enterprise
```

#### 按项目类型

| 场景 | 推荐 | 原因 |
|------|------|------|
| 快速原型/MVP | OpenSpec | 最轻量，快速验证 |
| 遗留系统改造 | OpenSpec | 专为brownfield设计 |
| 新产品开发 | Spec Kit | 规范驱动，从0到1 |
| 游戏开发 | BMad + BMGD | 有专门的游戏模块 |
| 企业级系统 | BMad Enterprise | 合规、安全、多租户 |
| 需要严格测试 | BMad + TEA | 风险导向测试策略 |

### 步骤3：生成推荐报告

向用户提供包含以下内容的推荐：

1. **推荐框架**（主推荐 + 备选方案）
2. **推荐理由**（基于项目特点的匹配度分析）
3. **快速开始指南**（该框架的安装和首个命令）
4. **注意事项**（使用中的常见陷阱和建议）
5. **迁移路径**（如需从当前方案迁移到更复杂/更轻量的方案）

## 框架详细对比

### BMad (Breakthrough Method)

**核心特点：**
- 21个专业Agent，50+工作流
- 三档规划路径：Quick Flow / Method / Enterprise
- Party Mode多Agent协作
- 模块化扩展（游戏、测试、创意等）

**最佳场景：**
- 复杂系统开发
- 多团队协作
- 需要严格流程和质量控制
- 游戏开发（配合BMGD模块）

**入门命令：**
```bash
npx bmad-method install
# 然后运行 /bmad-help 获取引导
```

---

### Spec Kit (GitHub官方)

**核心特点：**
- 规范驱动开发（Spec成为可执行产物）
- 6步标准流程：constitution → specify → plan → tasks → implement
- GitHub官方背书，企业友好
- 支持20+ AI助手

**最佳场景：**
- 新产品开发
- 团队需要规范对齐
- 使用GitHub生态
- 需要在规范和灵活性之间平衡

**入门命令：**
```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
specify init my-project --ai claude
```

---

### OpenSpec (Fission AI)

**核心特点：**
- 最轻量级，4个核心命令
- 专为遗留项目（brownfield）设计
- Artifact-guided workflow
- 流畅迭代，不僵化

**最佳场景：**
- 快速原型和验证
- 遗留系统渐进改造
- 个人开发者
- 小团队快速迭代

**入门命令：**
```bash
npm install -g @fission-ai/openspec@latest
cd your-project && openspec init
# 然后使用 /opsx:new <feature>
```

## 常见问答

**Q: 可以同时使用多个框架吗？**
A: 可以。建议先用 OpenSpec 快速验证想法，确定方向后用 Spec Kit 规范化，团队扩大后切换到 BMad。

**Q: 遗留项目用哪个框架？**
A: 强烈推荐 OpenSpec。它专为 brownfield 设计，不像其他框架假设从零开始。

**Q: 游戏开发选哪个？**
A: BMad + BMGD（Game Dev Studio）模块，有专门的游戏开发工作流。

**Q: 预算有限的小团队？**
A: OpenSpec 或 Spec Kit。BMad 虽然免费，但学习成本较高。

**Q: 需要严格的测试和质量控制？**
A: BMad + TEA（Test Architect）模块，提供风险导向的测试策略。

## 输出模板

### 推荐报告模板

```markdown
# Vibe Coding 框架推荐报告

## 项目概况
- 类型：[全新产品/遗留改造/其他]
- 复杂度：[简单/中等/复杂]
- 团队规模：[X人]
- 特殊需求：[如有]

## 🎯 推荐方案

### 首选：XXX
**匹配度：XX%**

**推荐理由：**
- 理由1
- 理由2
- 理由3

**快速开始：**
```bash
[安装命令]
```

### 备选：YYY
**适用场景：** [简述何时选择备选]

## ⚠️ 注意事项
- 注意点1
- 注意点2

## 🚀 下一步
1. [具体行动项]
2. [具体行动项]
```

## 参考资源

- [BMad 文档](http://docs.bmad-method.org)
- [Spec Kit GitHub](https://github.com/github/spec-kit)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
