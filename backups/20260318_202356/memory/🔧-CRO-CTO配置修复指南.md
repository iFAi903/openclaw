# 🔧 CRO & CTO 配置修复指南

## ❌ 问题诊断

**症状**：CRO 和 CTO 的消息都发给了 CEO，而不是各自独立的 Agent。

**根因**：Feishu Bot 的 Webhook URL 配置错误。

### 当前配置状态

| Agent | 本地端口 | Feishu Webhook | 状态 |
|-------|---------|----------------|------|
| CEO | 18756 (或 18789) | ✅ 正确 | 工作正常 |
| CRO | 18766 | ❌ 指向 CEO | 消息走错 |
| CTO | 18793 | ❌ 指向 CEO | 消息走错 |

---

## ✅ 修复步骤

### Step 1: 获取各 Agent 的正确 webhook URL

**CRO Agent**:
```
http://你的IP:18766/webhook/feishu
```

**CTO Agent**:
```
http://你的IP:18793/webhook/feishu
```

> 注意：如果用了 Tailscale，要用 Tailscale IP；如果是本机测试，用 `localhost` 或 `127.0.0.1`。

---

### Step 2: 修改 Feishu Bot Webhook 配置

#### 2.1 进入 Feishu 开发者平台
1. 访问 https://open.feishu.cn/app
2. 登录你的开发者账号

#### 2.2 修改 CRO Bot
1. 找到 CRO 对应的 Bot（应该是单独创建的一个应用）
2. 进入「事件订阅」或「机器人」设置
3. 找到 **Webhook URL** 或 **请求地址**
4. 修改为：`http://你的IP:18766/webhook/feishu`
5. 保存

#### 2.3 修改 CTO Bot
1. 找到 CTO 对应的 Bot
2. 同样的位置修改 Webhook URL
3. 修改为：`http://你的IP:18793/webhook/feishu`
4. 保存

---

### Step 3: 验证端口是否开放

在终端执行：

```bash
# 检查 CRO 端口
curl http://localhost:18766/status

# 检查 CTO 端口
curl http://localhost:18793/status
```

如果返回 JSON 状态信息，说明端口正常。

---

### Step 4: 重启验证

1. 重启 CRO Agent：
```bash
cd ~/.openclaw-agents/cro
openclaw restart
```

2. 重启 CTO Agent：
```bash
cd ~/.openclaw-agents/cto
openclaw restart
```

3. 在 Feishu 中分别给 CRO 和 CTO 发测试消息

---

## 📋 预期效果

修复后，三个 Agent 应该独立响应：

| 你给谁发消息 | 谁会回复 | 自称身份 |
|-------------|---------|---------|
| CEO Bot | CEO (我) | 小羽毛 CEO |
| CRO Bot | CRO | 小羽毛 CRO (首席关系官) |
| CTO Bot | CTO | 小羽毛 CTO (首席技术官) |

---

## 🧪 测试验证

发送测试消息：

**给 CRO**：
> "你好，请自我介绍一下"

**预期回复**：
> "你好！我是小羽毛 CRO，首席关系官..."（而非 CEO）

**给 CTO**：
> "你好，请自我介绍一下"

**预期回复**：
> "你好！我是小羽毛 CTO，首席技术官..."（而非 CEO）

---

## 💡 常见错误

### 错误 1: 三个 Bot 用了同一个 webhook URL
**解决**: 确保每个 Bot 的 webhook URL 中的端口号不同。

### 错误 2: 端口未开放
**解决**: 检查防火墙设置，或改用 `127.0.0.1` 测试。

### 错误 3: 只有一个 Bot 应用
**解决**: 需要为 CEO、CRO、CTO 分别创建三个独立的 Feishu 应用/Bot。

---

## 🆘 如果仍有问题

请检查以下信息：
1. CRO 的 `openclaw.json` 中 gateway.port 是否为 18766
2. CTO 的 `openclaw.json` 中 gateway.port 是否为 18793
3. Feishu 开发者平台中三个 Bot 的 webhook URL 是否分别对应三个端口

发送这些配置给我，我可以进一步帮你诊断。

---

*修复指南由 CEO 生成*
