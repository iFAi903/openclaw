# 🪶 小羽毛 AI 新闻早报 - 自动化部署

## 📅 定时任务配置

### 方法一：一键安装（推荐）

```bash
cd "/Users/ifai_macpro/.openclaw/workspace/iFAi/workspace/xiaoyumao-news-web Refer"
./install-cron.sh
```

### 方法二：手动配置

1. 编辑 crontab:
```bash
crontab -e
```

2. 添加以下内容:
```
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:$HOME/.npm-global/bin

# 小羽毛 AI 新闻早报 - 每日 7:00 自动更新
0 7 * * * /Users/ifai_macpro/.openclaw/workspace/iFAi/workspace/xiaoyumao-news-web\ Refer/daily-cron.sh >> /tmp/xiaoyumao-news-cron.log 2>&1
```

## 🔧 文件说明

| 文件 | 说明 |
|------|------|
| `daily-cron.sh` | 主执行脚本（Fetch → Update → Build → Deploy → Verify） |
| `install-cron.sh` | 一键安装脚本 |
| `crontab.config` | Crontab 配置参考 |
| `run-news-pipeline.sh` | 内容生成流水线 |
| `logs/` | 持久日志目录 |
| `status/last_run_status.json` | 最近一次运行状态 |

## 📊 执行流程

```
每天 07:00
    │
    ├─→ 1. 执行内容生成流水线
    ├─→ 2. 更新 TypeScript 数据
    ├─→ 3. 执行 npm run build 构建项目
    ├─→ 4. 执行 vercel --prod 部署到生产环境
    └─→ 5. 验证主域名日期是否切到当天版本
```

## 📜 日志查看

```bash
# 临时运行日志
cat /tmp/xiaoyumao-news-cron.log

# 持久日志（推荐）
ls logs/
tail -f logs/cron-$(date +%F).log
```

## 📦 状态查看

```bash
cat status/last_run_status.json
```

字段包含：
- `status`: success / failed / running
- `step`: 当前或失败阶段
- `generatedDate`: 本次生成的数据日期
- `onlineDate`: 主域名实际显示日期
- `newsCount` / `productsCount`
- `deployUrl`
- `persistentLog`

## 🧪 手动测试

```bash
./daily-cron.sh
```

## ⚙️ 修改定时时间

编辑 crontab:
```bash
crontab -e
```

修改时间格式：`分 时 日 月 周`
- `0 7 * * *` = 每天 7:00
- `0 8 * * *` = 每天 8:00
- `0 7 * * 1` = 每周一 7:00

## 🗑️ 卸载定时任务

```bash
crontab -e
# 删除包含 "daily-cron.sh" 的行
```

## 🔗 部署地址

- **生产环境**: https://xiaoyumao-news-web.vercel.app
