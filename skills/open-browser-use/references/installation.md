# Open Browser Use 安装指南

## 组件

- **Chrome 扩展**：浏览器端控制器，需用户 Chrome 确认
- **原生主机与 CLI**：`open-browser-use` / `obu` 二进制
- **SDKs**：JavaScript / Python / Go

## 安装 CLI

```sh
# npm（推荐）
npm install -g open-browser-use

# Homebrew
brew tap iFurySt/open-browser-use && brew install open-browser-use
```

验证：
```sh
open-browser-use version
obu version
```

注意：如果 `obu` 别名不可用，使用 `open-browser-use`。

## 安装 Chrome 扩展

### Web Store 版（待审核中）
```sh
open-browser-use setup
```

### GitHub Release ZIP 版（当前推荐）
```sh
open-browser-use setup beta
```
- 下载最新 ZIP 包
- 注册原生主机
- 打开 `chrome://extensions/`
- **用户手动操作**：开启开发者模式 → 将 ZIP 拖入扩展页

### 修复/重新注册原生主机
```sh
open-browser-use install-manifest
open-browser-use manifest  # 打印清单
```

## 平台说明

- macOS/Windows：Chrome 可能要求用户批准/启用扩展
- Linux：外部扩展注册可能需要提权
- 原生消息主机名：`com.ifuryst.open_browser_use.extension`
- 默认 socket 注册表：Unix 系统在 `/tmp/open-browser-use/`

## 验证安装

```sh
export OBU_SESSION_ID="obu-verify-$(date +%Y%m%d%H%M%S)"
open-browser-use ping --session-id "$OBU_SESSION_ID"
open-browser-use info --session-id "$OBU_SESSION_ID"
open-browser-use user-tabs --session-id "$OBU_SESSION_ID"
```

如果 `ping` 失败，检查：Chrome 是否运行、扩展是否启用、用户是否批准提示。
