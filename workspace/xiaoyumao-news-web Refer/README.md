# 🪶 小羽毛 AI 新闻早报

> 每日 AI 资讯一站式聚合，自动更新

**在线访问**: https://xiaoyumao-news-web.vercel.app

---

## 🚀 快速开始

### 环境要求
- Node.js 18+
- Python 3.9+
- Vercel CLI (可选，用于部署)

### 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:3000

---

## ⚙️ 环境变量配置

项目需要以下环境变量：

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `VERCEL_TOKEN` | ✅ | Vercel 部署 Token，用于自动部署 |

### 获取 VERCEL_TOKEN

1. 登录 Vercel: https://vercel.com/account/tokens
2. 点击 "Create Token"
3. 复制生成的 token

### 设置环境变量

```bash
# 临时设置（当前终端）
export VERCEL_TOKEN="your-token-here"

# 永久设置（推荐，添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export VERCEL_TOKEN="your-token-here"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🔄 自动部署

### 手动运行

```bash
# 获取新闻并部署
./daily-cron.sh
```

### 定时任务 (Cron)

```bash
# 安装定时任务
./install-cron.sh

# 或手动添加 crontab
crontab -e
```

添加以下行（每天 07:00 执行）：

```
0 7 * * * cd "/path/to/project" && /bin/bash daily-cron.sh >> /tmp/xiaoyumao-cron.log 2>&1
```

---

## 📁 项目结构

```
.
├── app/                    # Next.js 应用目录
│   ├── page.tsx           # 主页面
│   └── layout.tsx         # 根布局
├── src/data/              # 数据文件
│   └── news.ts            # 新闻数据（自动生成）
├── tests/                 # 测试文件
│   └── test_fetch_rss.py  # RSS 抓取测试
├── backups/               # 数据备份目录（自动创建）
├── daily-cron.sh          # 每日自动部署脚本 ⭐
├── fetch_news_final.py    # RSS 抓取主脚本 ⭐
├── daily_data.json        # 当日新闻数据（自动生成）
└── README.md              # 本文件
```

---

## 🧪 测试

```bash
# 运行所有测试
python3 tests/test_fetch_rss.py

# 或安装 pytest 后运行
pip install pytest
pytest tests/test_fetch_rss.py -v
```

---

## 🆘 故障排查

### 问题 1: daily-cron.sh 报错 "未设置 VERCEL_TOKEN"

**原因**: 环境变量未设置

**解决**:
```bash
export VERCEL_TOKEN="your-token-here"
```

### 问题 2: RSS 抓取返回 0 条新闻

**原因**: 网络问题或 RSS 源变更

**解决**:
1. 检查网络连接
2. 单独测试 RSS 源:
   ```bash
   curl -s -L "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
   ```
3. 查看日志 `/tmp/xiaoyumao-news-cron.log`

### 问题 3: 构建失败

**原因**: Node.js 版本不兼容或依赖问题

**解决**:
```bash
# 清理并重新安装
rm -rf node_modules package-lock.json
npm install
npm run build
```

### 问题 4: 部署失败

**原因**: Vercel Token 无效或权限不足

**解决**:
1. 检查 token 是否有效
2. 确保 token 有部署权限
3. 尝试重新登录:
   ```bash
   npx vercel login
   ```

---

## 🔐 安全说明

- **绝不提交密钥**: `VERCEL_TOKEN` 必须从环境变量读取
- **自动备份**: 每次运行 `daily-cron.sh` 会自动备份数据到 `backups/` 目录
- **定期清理**: 备份目录自动保留最近 10 个版本

---

## 📚 技术栈

- **前端**: Next.js 14 + React + TypeScript + Tailwind CSS
- **数据获取**: Python 3 + RSS Feed Parser
- **部署**: Vercel + Cron 定时任务
- **翻译**: Google Translate API (非官方)

---

## 📝 更新日志

查看 [CHANGELOG.md](./CHANGELOG.md)

---

*Powered by 小羽毛 AI 天团*
