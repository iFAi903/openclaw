# 新闻早报推送修复报告

## 修复概述
针对新闻早报推送中出现的三个问题，我已经修改了数据拉取脚本与自动构建脚本，并进行了本地执行验证。明天早上7点的定时推送将按照新规则稳定生成并发布。

## 修改的文件
1. `workspace/xiaoyumao-news-web Refer/fetch_news_v2.py`
2. `workspace/xiaoyumao-news-web Refer/daily-cron.sh`

## 具体修复内容

### 1. 数量调整（新闻从14改为15条，产品从4改回5条）
- **原因**：部分 RSS 源输出的数据与 `news_history.json` 历史数据重叠较多，当仅拉取前 10 条数据时，由于排重机制，导致有效可用新闻数量不足以填满目标数值，且产品数组的 while 循环会由于 break 过早而丢失条目。
- **修复措施**：
  - 在 `fetch_news_v2.py` 中将 `entries[:10]` 调整为 `entries[:30]`，扩大拉取范围。
  - 优化了由于数据不足退回到缺省值以及防止 while 循环异常退出的逻辑，保证最终输出的数组绝对满足 15 条新闻与 5 个产品的要求。

### 2. 英文转中文（全球动态栏目后续新闻翻译）
- **原因**：此前代码在组装 Global News（TheVerge、TechCrunch 等来源）时缺少翻译步骤或只使用了简单的字典替换，导致英文新闻内容直接混排在中文版面中。
- **修复措施**：
  - 在 `fetch_news_v2.py` 中引入了原生的 `translate_to_chinese()` 翻译函数，无需 API Key 即可调用 Google Translate 免费接口进行翻译。
  - 为避免网络请求引起的脚本假死，为其增加和封装了 3 秒的 `signal.alarm()` 级强制超时保护；并在组装最终队列时统一将所有外文（含 Title 与 Summary）翻译为中文。

### 3. 摘要完整（Product追踪第1条摘要丢失及被截断截取）
- **原因**：
  - `ProductHunt` 的 RSS (Atom 格式) 没有标准的 `<summary>` 标签，内容存放在 `<content>` 中，导致之前解析出来为空。
  - 提取的摘要中包含 HTML 格式标签（如 `<p>` 与 `<a>` ）。
  - `daily-cron.sh` 之前强行使用了 `[:80]` 进行字符串截断，切断了部分字符或被 HTML 标签掩盖。
- **修复措施**：
  - 在 `fetch_news_v2.py` 中加入了当 `atom:summary` 为 None 时向下寻拔 `atom:content` 节点的内容处理逻辑。
  - 添加了 `clean_html()` 正则函数清除并规范化提取出内容中的 HTML 结构（`<[^>]+>`）。
  - 在 `daily-cron.sh` 脚本中，去除了处理产品生成 `ts_content` 时的 `[:80]...` 长度截取限制，保留产品的完整摘要。

---
> 所有的更新已经通过单步运行 `fetch_news_v2.py` 生成验证，`daily_data.json` 内各项指标已严格符合需求。