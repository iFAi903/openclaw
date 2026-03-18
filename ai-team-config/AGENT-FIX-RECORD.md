# 🔧 copy-agent & product-agent 修复记录

## 修复时间
2026-03-09

## 问题诊断

### 发现的问题
1. **缺少 openclaw.json 配置文件** - 两个 agent 都没有主配置文件
2. **缺少 workspace 目录结构** - 工作空间未初始化
3. **缺少启动脚本** - 没有便捷的启动/停止工具

## 修复内容

### 1. 创建 openclaw.json 配置文件

#### copy-agent (白色小羽毛)
- **端口**: 18870
- **角色**: 文案高手、策划天才、提示词大师
- **主模型**: Claude Sonnet 4.6
- **工作目录**: `ai-team-config/copy-agent/workspace/`

#### product-agent (紫色小羽毛)
- **端口**: 18880
- **角色**: 产品经理、需求分析师、PRD专家
- **主模型**: Claude Sonnet 4.6
- **工作目录**: `ai-team-config/product-agent/workspace/`

### 2. 创建 Workspace 目录结构

```
copy-agent/workspace/
├── projects/    # 项目文件夹
├── assets/      # 素材库
├── docs/        # 文档
└── archive/     # 归档

product-agent/workspace/
├── projects/    # 项目文件夹
├── templates/   # 文档模板
├── research/    # 研究资料
└── archive/     # 归档
```

### 3. 创建管理脚本

**team-agents.sh** - 统一管理脚本
```bash
./team-agents.sh start    # 启动所有 agents
./team-agents.sh stop     # 停止所有 agents
./team-agents.sh restart  # 重启所有 agents
./team-agents.sh status   # 查看状态
./team-agents.sh logs     # 查看日志
```

## 启动方式

### 方式一：使用管理脚本
```bash
cd /Users/ifai_macpro/.openclaw/workspace/iFAi/ai-team-config
./team-agents.sh start
```

### 方式二：手动启动
```bash
# copy-agent
cd copy-agent
openclaw gateway start --config openclaw.json

# product-agent
cd product-agent
openclaw gateway start --config openclaw.json
```

## 验证方式

```bash
# 检查端口
lsof -Pi :18870  # copy-agent
lsof -Pi :18880  # product-agent

# 使用管理脚本检查
./team-agents.sh status
```

## 下一步（新成员部署）

根据架构设计文档，还需要部署三位新成员：

| 成员 | 端口 | 状态 |
|------|------|------|
| COO 大掌柜 | 18840 | 待创建 |
| CFO 财神 | 18850 | 待创建 |
| Design 金色小羽毛 | 18860 | 待配置 |

## 配置文件引用

两个 agent 都依赖以下身份文件：
- SOUL.md - 意识内核
- IDENTITY.md - 身份定义
- TOOLS.md - 工具能力
- USER.md - 用户画像

这些文件已在目录中存在，无需修改。
