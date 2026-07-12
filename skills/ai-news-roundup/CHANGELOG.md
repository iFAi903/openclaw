# Changelog

## v2.0.0 (2026-07-12)

### 🏗️ 架构重构
- **Agent 接管策展层**：选文、标题重写、标签分配、产品甄别、今日寄语全部由 Agent 编辑判断，脚本层只做确定性工作
- **agent_quality_pass.py 归档**：正则质量门禁被 Agent 编辑判断取代
- **build_daily_data.py 精简**：剥离金句生成、标签分配、质量门禁代码（~230 行），只保留去重/聚类/产品门禁

### ✨ 新功能
- 标题质量从"正则退化检测"升级为"编辑级重写"
- 标签从 `capability_tags`（泛指标签）变为精确的 12 分类体系
- 今日寄语从模板套话升级为基于当日真实新闻的编辑手记
- 产品雷达引入 Agent 甄别（剔除平台集合页、空名退化条目）

### 📖 文档
- README 重写：策展前后对比表、新的双层架构图、三层职责表
- SKILL.md：扩展 frontmatter、失败模式表（8 种场景 + fallback）、反例清单（标题/标签/引语/产品雷达）

### 🐛 修复
- README 架构图更新（移除已归档的 agent_quality_pass.py）
- README 示例更新（移除模板化引语）
- 快开始命令更新（移除已归档的脚本引用）
- 去重逻辑验证：URL 精确去重 + Jaccard 相似度 + 48h 历史交叉

### 🔧 调度
- cron 从系统 crontab 迁移到 OpenClaw 原生 cron（isolated agentTurn）
- 新增 `SCHEDULES.md` 记录调度配置

---

## v1.0.0 (2026-05-04)

- 初始版本
- 脚本全流程：fetch → build → quality_pass → format → deploy
- 16 个 RSS 源 + 5 个产品平台
- agent_quality_pass.py 正则质量门禁
- 系统 crontab 调度
- Vercel 前端部署
