# Task Plan

## Goal
在 `/Users/ifai_macpro/.openclaw/workspace/iFAi/C&P` 下生成一套“待审核、不直接生效”的完整配置方案，用于把 copy-agent / product-agent 收敛到 **主 Gateway + Feishu 多账号路由模式**。

## Phases
- [x] Phase 1 — 诊断当前失败根因
- [x] Phase 2 — 确定目标架构（主 Gateway 多账号路由）
- [in_progress] Phase 3 — 生成待审核配置包到 `C&P`
- [ ] Phase 4 — 向用户说明每个文件用途与审核方式
- [ ] Phase 5 — 等待用户确认后再实施线上配置

## Key Decisions
- 不直接修改当前在线配置
- 统一采用主 Gateway 多账号路由模式
- 账号 ID 统一为：`default` / `copy-agent` / `product-agent`
- `copy-agent` / `product-agent` 的本地独立实例配置仅保留为参考，不作为生效路径

## Risks
- 现有主配置中 Feishu accountId 与 bindings 不一致
- copy-agent/product-agent 本地配置与主路由模式混用，容易继续造成误判
- product-agent 历史上存在路径解析异常（`/.openclaw-product-agent`）

## Deliverables
- `C&P/README.md`
- `C&P/main-openclaw.proposed.json`
- `C&P/copy-agent-reference.proposed.json`
- `C&P/product-agent-reference.proposed.json`
- `C&P/implementation-checklist.md`
- `C&P/verification-checklist.md`
