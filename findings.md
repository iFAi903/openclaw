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
