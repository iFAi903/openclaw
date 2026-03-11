# Findings

## 2026-03-11

### Confirmed root causes
1. 主配置 `channels.feishu.accounts` 中真实账号名仍是中文装饰名：
   - `白色小羽毛copy-agent`
   - `紫色羽毛product-agent`
   但 `bindings` 绑定到的是：
   - `copy-agent`
   - `product-agent`
   导致 probe 一直显示 `not configured`。

2. `copy-agent` 本地独立配置仍是占位符：
   - `YOUR_APP_ID_HERE`
   - `YOUR_APP_SECRET_HERE`
   - `enabled: false`
   且 workspace 写成 `~/openclaw-copy-agent/workspace`，与真实目录不一致。

3. `product-agent` 本地独立配置里模型版本格式不规范（`4.6` 而非 `4-6`），且其本地独立运行模式与主 Gateway 路由模式混用。

4. 目标架构应统一为：
   - 主 Gateway 接管 Feishu 多账号
   - bindings 基于 accountId 精确路由
   - copy-agent / product-agent 不再依赖各自独立 Feishu 实例

### Proposed routing account IDs
- `default`
- `copy-agent`
- `product-agent`

### Scope of current work
- 仅准备待审核配置文件
- 不修改线上主配置
- 不重启 Gateway
