# SDK 与协议参考

## 连接模型

```
Agent → CLI/MCP/SDK → Open Browser Use Socket → Native Host → Chrome Extension → Chrome
```

## 核心方法

| 方法 | 说明 |
|------|------|
| `ping` | 连通性检查 |
| `getInfo` | 获取扩展/浏览器信息 |
| `createTab` | 创建新标签页 |
| `getTabs` | 获取当前 session 标签页 |
| `getUserTabs` | 获取用户已打开标签页 |
| `getUserHistory` | 搜索浏览历史 |
| `claimUserTab` | 认领用户已有的标签页 |
| `finalizeTabs` | 释放/保留标签页 |
| `nameSession` | 命名当前 session |
| `attach` / `detach` | 附加/分离标签页 |
| `executeCdp` | 执行 CDP 命令 |
| `moveMouse` | 移动鼠标 |
| `waitForFileChooser` | 等待文件选择器 |
| `setFileChooserFiles` | 设置文件选择路径 |
| `waitForDownload` / `downloadPath` | 下载监控 |
| `readClipboardText` / `writeClipboardText` | 剪贴板 |
| `turnEnded` | 回合结束通知 |

## 用户标签页认领流程

1. `user-tabs` 列出用户标签页
2. 从返回数据中选择（基于 URL、标题、时间）
3. `claim-tab --tab-id <id>` 认领
4. 使用返回的可控标签页进行操作

## 清理

任务结束前必须 `finalize-tabs`。不要 finalize 之后再调用浏览器操作。

详情参见上游仓库：
https://github.com/iFurySt/open-codex-browser-use/blob/main/skills/open-browser-use/references/sdk-and-protocol.md
