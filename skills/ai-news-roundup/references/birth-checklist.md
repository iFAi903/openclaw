# 🪶 小羽毛 AI 新闻早报 — 出生证清单

> 发布到公共生态前必须通过的全部检查项。

## 信息完备

- [x] SKILL.md 有完整的 frontmatter（name / description / risk / version / tags / plugin.targets）
- [x] SKILL.md 有触发方式注释
- [x] CHANGELOG.md 存在且有 v1 → v2 记录
- [x] README.md 有一句话钩子
- [x] README.md 有安装路径
- [x] README.md 有架构说明
- [x] README.md 有可见产物展示

## 可执行

- [ ] `.env.cron` 模板化（当前含私有 VERCEL_TOKEN，发布前需标记为 `*.example`）
- [ ] `config.yaml` 模板化（发布前抽取敏感配置）
- [ ] 安装过程不依赖私有路径
- [ ] config 中的 VERCEL_TOKEN 可替换为环境变量
- [ ] 推送到飞书的 token/channel 配置可外部化

## 可验证

- [x] 站点可达：`curl -sI https://xiaoyumao-news-web.vercel.app` → 200
- [x] `daily_data.json` 结构正确（`news` + `products` + `quote` + `meta`）
- [ ] 新用户按照 README 可在一台新机器上独立安装并跑通

## 安全

- [ ] `.env.cron` 不包含在公开仓库中
- [ ] `config.yaml` 不含私人 API key 或 token
- [ ] 推送到公共渠道的目标由变量控制，不硬编码
- [ ] README 中不暴露真实用户id（如 `ou_xxx`）

## 传播力

- [ ] 一句话钩子能让人停下阅读
- [ ] README 首屏有图片/GIF/截图
- [ ] 有至少 3 个触发示例
- [ ] 有策展前后的对比展示

## 状态标记

- [ ] **内部可用**：✅（每日稳定推送）
- [ ] **对外可传播**：待 Leo 确认
