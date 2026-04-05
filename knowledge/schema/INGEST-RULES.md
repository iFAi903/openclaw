# INGEST-RULES

## 目标
把 raw sources 转成可累积的 wiki 资产，而不是只做一次性摘要。

## 标准流程
1. 将资料归入 `knowledge/raw/` 对应目录
2. 判断资料涉及的实体 / 概念 / 项目 / 决策
3. 提炼：事实、判断、冲突、启发
4. 选择需要更新的 wiki 页面
5. 若页面不存在，则创建主页面或待建占位
6. 更新 `wiki/index.md`
7. 追加 `wiki/log.md`

## 最低要求
- 每次 ingest 至少更新 1 个 wiki 页面
- 如果形成新结论，必须更新 decision 或 synthesis 页面
- 不允许只放 raw source 不做知识整合
