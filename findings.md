# Findings

## 2026-04-05
- Karpathy 的核心不是增强 RAG，而是让 LLM 持续维护一个可增值的 wiki 中间层。
- 对小羽毛体系最关键的映射点：
  - 现有 memory 文件已具备雏形；
  - 天团分工天然适合承担 ingest / synthesis / lint / governance；
  - Leo 的工作方式更适合“意义网络”而非线性任务库。
- 设计重点应放在：
  - raw / wiki / schema 三层结构；
  - ingest / query / lint 三类操作；
  - index / log / registry 三类治理入口；
  - CEO/CRO/CTO/PLAN/REVIEW 的知识职责分工。
- Wiki OS 骨架的 MVP 至少应包含：
  - `knowledge/raw/` 资料入口；
  - `knowledge/wiki/index.md` 与 `knowledge/wiki/log.md`；
  - `knowledge/schema/WIKI-SCHEMA.md` 及三个流程规则文件；
  - 一个可复用页面模板。
- 对 Leo 当前工作方式而言，Wiki 正式主库放在 Obsidian 比放在 workspace 更合理；workspace 更适合保留入口说明与临时施工文件。\n