# wechat-publish Skill

微信公众号内容发布技能。支持将内容推送到公众号草稿箱。

## 功能

- 创建图文消息草稿
- 支持 Markdown 转 HTML
- 自动获取/刷新 access_token

## 使用方式

```bash
# 发布单篇图文
openclaw skill run wechat-publish \
  --title "文章标题" \
  --content "文章内容（支持 Markdown）" \
  --author "作者名" \
  --digest "摘要"

# 从文件发布
openclaw skill run wechat-publish \
  --file /path/to/article.md \
  --title "文章标题"
```

## 环境变量

需要在 `.env` 中配置：
- `WECHAT_APP_ID` - 微信公众号 AppID
- `WECHAT_APP_SECRET` - 微信公众号 AppSecret

## 共享给 Agent

此技能已对以下 Agent 共享：
- CEO (总控/审核)
- CRO (创意/增长)
- copy-agent (文案创作)
