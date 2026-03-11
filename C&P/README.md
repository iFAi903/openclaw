# C&P 配置审核包

这是一套 **待审核、不直接生效** 的配置方案。
目标是把 `copy-agent` 与 `product-agent` 统一收敛到：

**主 Gateway + Feishu 多账号路由模式**

也就是：
- Feishu 消息入口统一走主 Gateway
- 主 Gateway 里维护多账号 `accountId`
- 再通过 `bindings` 把不同账号路由到不同 agent
- `copy-agent` / `product-agent` 不再依赖各自独立启动的 Feishu 实例来接收消息

## 本目录文件说明

### 1) `main-openclaw.proposed.json`
主配置的**建议替换片段**。
重点包含：
- `channels.feishu.accounts`
- `bindings`

这是最核心的一份。

### 2) `copy-agent-reference.proposed.json`
`copy-agent` 的**参考配置**。
用途：保留 agent 身份/模型/工作区等定义，但不把它作为独立 Feishu 入口实例使用。

### 3) `product-agent-reference.proposed.json`
`product-agent` 的**参考配置**。
同样保留 agent 身份/模型/工作区等定义，但不作为独立 Feishu 入口实例。

### 4) `implementation-checklist.md`
正式实施时的步骤清单。

### 5) `verification-checklist.md`
实施后验证是否成功的检查清单。

## 本次方案的关键原则

1. accountId 必须逐字一致
统一为：
- `default`
- `copy-agent`
- `product-agent`

2. 只保留一种生效架构
本次选定的是：
**主 Gateway 路由模式**

3. 独立 agent 本地配置只作参考
尤其是 `copy-agent` / `product-agent` 各自目录下的旧 `openclaw.json`，不应再承担 Feishu 接入职责。

## 你审核时重点看什么

- 账号名是否要统一成英文 ID
- copy-agent / product-agent 的角色描述、模型、工作区是否符合你的预期
- 是否接受“主 Gateway 接收 + 绑定路由”的架构

等你确认通过后，我再帮你把这套配置正式落地。