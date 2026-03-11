# 验证清单

## 配置正确性
- [ ] 主配置中不存在中文装饰版 accountId
- [ ] `channels.feishu.accounts` 与 `bindings` 的 accountId 完全一致
- [ ] `agents.list` 里的 agent id 与 bindings 的 agentId 完全一致

## 运行状态
- [ ] `openclaw channels status --probe` 显示：
  - [ ] Feishu default: works
  - [ ] Feishu copy-agent: works
  - [ ] Feishu product-agent: works
- [ ] `openclaw agents bindings` 显示两条路由绑定都存在

## 行为验证
- [ ] 发给 copy-agent 的消息由 copy-agent 回复
- [ ] 发给 product-agent 的消息由 product-agent 回复
- [ ] copy-agent / product-agent 不串回 main
- [ ] 不出现静默无响应
- [ ] 不出现 `not configured`

## 日志验证
- [ ] gateway.err.log 不再出现 accountId 不匹配迹象
- [ ] 不再出现 product-agent 的异常目录创建错误
- [ ] 不再出现由于独立 Feishu 实例引发的混乱日志

## 验收结论
- [ ] 可以稳定使用
- [ ] 后续新增 agent 时继续沿用同一套主 Gateway 路由模式
