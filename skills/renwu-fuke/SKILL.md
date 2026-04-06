---
name: renwu-fuke
description: Safe 人物复刻 / character-replica builder and analyst. Use when the user wants to recreate a person’s thinking style, decision logic, communication habits, heuristics, or worldview from user-uploaded materials plus publicly available information, then use that replica for later analysis, comparison, or reference. Suitable for founders, authors, colleagues, historical figures, creators, public thinkers, and other named人物. Only use user-provided files and public-web sources; never use private chats, browser login sessions, OAuth tokens, internal docs, or auto-collection from Feishu/DingTalk/Slack.
---

# 人物复刻.skill

把“一个人”拆成可复用的分析结构，而不是神化成一个会胡说八道的角色扮演壳子。

## 快速判断

适合用这个 skill 的请求：
- “帮我复刻马斯克/乔布斯/段永平/某位创作者的思维方式”
- “我上传了一些访谈、文章、演讲，帮我做成人物复刻”
- “结合公开信息，生成一个能用于问题分析参考的人物镜像”
- “后面我想用某人的思路来评估产品/决策/文案”

不适合：
- 需要读取私聊、企业内部文档、浏览器登录态、用户 token
- 要伪造本人授权、伪装成本人发言、生成欺骗性身份冒充
- 让复刻对象对医疗、法律、投资等高风险问题给出权威结论

## 核心原则

1. **安全优先**：只用两类来源
   - 用户主动上传/粘贴的材料
   - 公开网络可检索信息
2. **复刻的是模式，不是灵魂**
   - 输出“思维方式、行事逻辑、表达偏好、判断框架”
   - 不宣称“这就是真人本人”
3. **证据绑定**
   - 每条关键判断尽量对应来源
   - 区分“高把握结论”和“推测性结论”
4. **用于参考，不用于冒充**
   - 重点服务于分析、借鉴、对照、启发
   - 不鼓励伪造私密关系或现实身份替身

## 工作流

### Step 1：定义复刻对象

先确认四件事：
1. 人物是谁（姓名 / 常用称呼 / slug）
2. 复刻目标是什么
   - 决策参考
   - 产品分析
   - 写作风格借鉴
   - 人格/沟通风格学习
3. 使用边界是什么
   - 仅供分析参考 / 不扮演本人 / 不输出高风险建议
4. 现有材料来自哪里
   - 用户上传
   - 用户粘贴
   - 公开网络

如果用户目标模糊，优先帮他收敛为一句话：
> 我想复刻 X 的【思维方式 / 行事逻辑 / 表达风格】，用于【什么任务】。

### Step 2：收集材料

只允许以下来源：
- 用户上传的 PDF / 图片 / Markdown / TXT / 导出记录
- 用户直接粘贴的文字
- 公开网页、公开采访、公开社媒、公开演讲、公开文章

如果需要来源边界，读取 `references/source-policy.md`。

禁止使用：
- 私聊自动采集
- 企业 IM / 云文档登录态
- OAuth code / access token
- 浏览器 profile
- 未公开资料
- 任何可能侵犯隐私或越权的采集方式

### Step 3：建立来源账本

先创建该人物目录，再记录来源账本。

使用：
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/replica_writer.py init --base-dir ./.claude/skills/replicas --slug <slug> --name "<name>"
```

然后把来源整理到 `source-ledger.md`，每条来源至少写：
- 类型：user_file / user_text / public_web
- 标题
- 链接或文件名
- 时间（若可得）
- 可靠性：high / medium / low
- 用途：支撑哪类判断

### Step 4：按四层分析

如需字段定义，读取 `references/analysis-schema.md`。

必须至少分析四层：

1. **Thinking Model**
   - 如何看问题
   - 优先看什么变量
   - 常用判断框架
   - 偏好的抽象层级

2. **Action Logic**
   - 决策速度
   - 风险偏好
   - 如何排序优先级
   - 遇到冲突时怎么取舍

3. **Communication Style**
   - 语气
   - 常见句式
   - 是否直接、冷静、煽动、犀利、温和
   - 会不会用比喻、反问、故事、数字

4. **Boundary & Uncertainty**
   - 我们知道什么
   - 我们猜测什么
   - 哪些部分证据薄弱
   - 哪些情境下不要强行模仿

### Step 5：生成复刻档案

先产出四个文件：
- `profile.md`：人物概况、背景、主题画像
- `mindset.md`：思维方式、决策逻辑、表达风格
- `source-ledger.md`：证据账本
- `notes.md`：待验证点、冲突点、低置信推断

建议先预览摘要给用户，再组合成最终可调用 Skill。

组合命令：
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/replica_writer.py combine --base-dir ./.claude/skills/replicas --slug <slug>
```

如果四个文件已经准备好，也可以直接：
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/replica_writer.py create --base-dir ./.claude/skills/replicas --slug <slug> --name "<name>"
```

### Step 6：使用复刻对象

生成后的对象用于：
- “如果按这个人的逻辑，会怎么拆这个问题？”
- “用这个人的标准，怎么评估这个产品/策略/文案？”
- “这个人的表达方式，会怎么重写这段话？”

生成后的复刻 Skill 默认应强调：
- 这是**基于有限资料的近似模型**
- 优先输出“参考性分析”，不要装作真人下断言
- 不凭空补全私生活、情绪、动机

## 输出标准

好的复刻结果至少要有：
- **一句话定义**：这个人最核心的判断方式是什么
- **3-7 条稳定原则**：这个人反复出现的决策/表达模式
- **置信度标注**：高 / 中 / 低
- **来源锚点**：能回指到材料
- **适用场景**：哪些问题适合借鉴，哪些不适合

避免：
- 只有人设，没有方法论
- 只有口头禅，没有判断逻辑
- 只会角色扮演，不会做分析
- 把缺证据的猜测写成事实

## 默认目录约定

推荐把生成结果放在：
- `./.claude/skills/replicas/<slug>/`

目录结构：
- `meta.json`
- `profile.md`
- `mindset.md`
- `source-ledger.md`
- `notes.md`
- `SKILL.md`
- `versions/`

## 资源

### scripts/
- `replica_writer.py`：初始化目录、写入元数据、组合最终 SKILL.md、列出已有复刻对象

### references/
- `source-policy.md`：允许/禁止来源与可靠性判断
- `analysis-schema.md`：人物复刻分析字段模板
