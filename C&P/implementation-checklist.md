# 实施清单（待你审核通过后再执行）

## Phase A — 备份
- [ ] 备份 `~/.openclaw/openclaw.json`
- [ ] 备份 `~/.openclaw/logs/` 最近日志
- [ ] 备份 `~/.openclaw-copy-agent/openclaw.json`
- [ ] 备份 `~/.openclaw-product-agent/openclaw.json`

## Phase B — 主 Gateway 配置
- [ ] 将 `channels.feishu.accounts` 中的中文装饰名统一改为：
  - `default`
  - `copy-agent`
  - `product-agent`
- [ ] 确认 `bindings` 逐字匹配同样的 `accountId`
- [ ] 保持 `agentId` 与 `agents.list[].id` 一致：
  - `copy-agent`
  - `product-agent`

## Phase C — 参考配置收敛
- [ ] copy-agent 本地配置中不再承担 Feishu 入口
- [ ] product-agent 本地配置中不再承担 Feishu 入口
- [ ] 仅保留模型、人格、工作区、工具许可等参考定义
- [ ] 修正不规范模型名（例如 `4.6` → `4-6`）

## Phase D — 重启与检查
- [ ] 重启 Gateway
- [ ] 运行 `openclaw channels status --probe`
- [ ] 运行 `openclaw agents bindings`
- [ ] 确认 probe 输出：
  - `Feishu copy-agent: works`
  - `Feishu product-agent: works`

## Phase E — 实测
- [ ] 在 copy-agent 对应窗口发一条测试消息
- [ ] 在 product-agent 对应窗口发一条测试消息
- [ ] 观察是否进入各自 agent，而不是串回 main
- [ ] 确认无静默、无报错、无错路由
