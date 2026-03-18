# 🌐 网页反爬抓取工具使用指南

> **安全实现** - 无需安装可疑 skill，直接使用标准工具

---

## 📁 工具清单

位置: `workspace/iFAi/tools/`

| 工具 | 用途 | 命令 |
|------|------|------|
| `web-fetch.sh` | 主脚本（自动尝试所有方法） | `./web-fetch.sh <URL>` |
| `web-fetch-curl.sh` | curl + 移动端UA | `./web-fetch-curl.sh <URL>` |
| `web-fetch-chrome.sh` | Chrome Headless | `./web-fetch-chrome.sh <URL>` |
| `web-fetch.js` | Node.js 版本（推荐） | `node web-fetch.js <URL>` |
| `wechat-fetch.sh` | 微信公众号专用 | `./wechat-fetch.sh <公众号URL>` |

---

## 🚀 快速开始

### 1. 普通网页抓取

```bash
# Bash 版本（最快）
./tools/web-fetch.sh "https://example.com"

# Node.js 版本（更稳定，支持 Playwright）
node tools/web-fetch.js "https://example.com"
```

### 2. 微信公众号文章

```bash
# 专用脚本（自动提取正文）
./tools/wechat-fetch.sh "https://mp.weixin.qq.com/s/xxxxx"

# 输出:
#   wechat_article.html - 原始HTML
#   wechat_content.txt  - 提取的正文内容
```

### 3. 指定方法

```bash
# 只用 curl
node tools/web-fetch.js "https://example.com" --method=curl

# 只用 Playwright（JS渲染）
node tools/web-fetch.js "https://example.com" --method=playwright
```

---

## 🔧 三种反爬方法

### 方法 1: curl + 移动端 UA（最快）✅

**原理**: 模拟手机浏览器访问，绕过部分PC端限制

**User-Agents**:
- iPhone Safari
- Android Chrome
- **微信内置浏览器**（最强）

**适用场景**: 大多数新闻网站、博客

**命令**:
```bash
./tools/web-fetch-curl.sh "https://target-site.com"
```

---

### 方法 2: Chrome Headless dump-dom（JS渲染）

**原理**: 启动无界面 Chrome，执行页面 JavaScript

**适用场景**: 
- React/Vue/Angular 单页应用
- 需要登录态的页面
- 动态加载内容的页面

**前置条件**:
```bash
# macOS 已内置 Chrome/Edge
# 检查是否可用
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

**命令**:
```bash
./tools/web-fetch-chrome.sh "https://spa-site.com"
```

---

### 方法 3: Chrome Remote Debugging（最强）

**原理**: 连接到已运行的 Chrome 实例，完全控制浏览器

**适用场景**:
- 需要保持登录态
- 需要执行复杂交互
- 需要绕过高级反爬

**启动 Chrome 调试模式**:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug
```

**连接使用**:
```bash
# 检查是否可连接
curl http://localhost:9222/json/version

# 使用 Puppeteer/Playwright 连接
```

---

## 📱 微信公众号专用

### 特点
- 必须使用手机UA（微信UA最佳）
- 正文在 `id="js_content"` 容器中
- 图片需要处理防盗链

### 使用
```bash
./tools/wechat-fetch.sh "https://mp.weixin.qq.com/s/xxxxx"
```

### 提取逻辑
```bash
# 1. 用微信UA抓取
curl -A 'Mozilla/5.0 (iPhone...MicroMessenger...)' URL

# 2. 提取 js_content
sed -n '/id="js_content"/,/\/div/p' page.html

# 3. 清理HTML标签
sed 's/<[^\u003e]*>//g'
```

---

## 🛡️ 反反爬策略

### 当前实现

| 策略 | 实现方式 |
|------|----------|
| **User-Agent轮换** | iPhone/Android/微信 |
| **请求头模拟** | Accept, Accept-Language, Referer |
| **压缩支持** | gzip, deflate, br |
| **超时控制** | 30秒超时，避免卡死 |
| **多方法 fallback** | curl → Chrome → Remote Debug |

### 高级策略（待实现）

- **代理池**: 轮换IP地址
- **请求频率控制**: 随机延迟
- **Cookie管理**: 保持会话
- **验证码识别**: OCR 或打码平台

---

## 📝 集成到工作流

### CEO 使用示例

```bash
# 抓取 RSS 失败时的备用方案
fetch_web_page() {
  local url="$1"
  local output="${2:-fetched.html}"
  
  # 尝试 web-fetch
  if ./tools/web-fetch.sh "$url" "$output"; then
    echo "✅ Web抓取成功"
    return 0
  fi
  
  # 失败则使用 web_search 作为后备
  echo "⚠️ Web抓取失败，使用搜索后备"
  web_search "$url"
}
```

### CRO 使用示例

```bash
# 抓取竞品公众号文章
fetch_competitor_content() {
  local article_url="$1"
  
  ./tools/wechat-fetch.sh "$article_url"
  
  # 读取提取的内容
  cat wechat_content.txt
}
```

---

## ⚠️ 注意事项

1. **遵守 robots.txt**: 尊重网站的爬虫协议
2. **控制频率**: 不要高频抓取，避免被封IP
3. **版权声明**: 抓取内容仅供学习研究，勿用于商业
4. **隐私保护**: 不要抓取用户隐私数据

---

## 🔗 相关资源

- [curl 文档](https://curl.se/docs/)
- [Playwright 文档](https://playwright.dev/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

---

**安全声明**: 本工具使用系统标准命令（curl、Chrome），不依赖第三方可疑 skill，符合安全审计要求。
