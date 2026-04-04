# 小羽毛 AI 新闻早报自我兜底机制实施报告（2026-04-04）

## 结论先说
已经把新闻早报从“会失败的自动化”补成了**具备自我兜底能力的系统**，并完成了一次真实闭环演练。

当前机制已经落地到代码与脚本中，覆盖：
- 失败即告警
- 自动补跑一次
- 单实例保护
- 降级兜底发布
- 主域名验收闭环
- 状态文件 / 历史记录 / 告警产物

本次真实演练结果：
- 完整流程连续两次失败（都卡在 pipeline）
- 系统自动触发补跑
- 补跑仍失败后，自动进入 degraded 模式
- 使用最近成功数据重新构建、部署并通过主域名验收
- 主域名当前状态：`degraded_success`
- 主域名当前内容日期：`2026年04月04日 周六`

---

## 一、兜底架构（简洁版）

### 1. cron 入口层
`daily-cron.sh`
- 只负责进入项目目录、加载 `.env.cron`
- 真正执行权交给 `news_self_heal.py`

### 2. 自我兜底编排层
`news_self_heal.py`
- 负责完整流程编排
- 管理状态、锁、告警、重试、降级、构建、部署、主域名验收

### 3. 内容层
- `run-news-pipeline.sh`
- `fetch_news_final.py`
- `update_news_ts.py`

### 4. 站点感知层
- `src/data/siteRuntimeStatus.ts`
- `app/page.tsx`

站点会直接展示运行状态，而不是把降级结果伪装成完整成功。

---

## 二、修改文件清单

### 核心新增
- `workspace/xiaoyumao-news-web Refer/news_self_heal.py`
- `workspace/xiaoyumao-news-web Refer/src/data/siteRuntimeStatus.ts`

### 核心修改
- `workspace/xiaoyumao-news-web Refer/daily-cron.sh`
- `workspace/xiaoyumao-news-web Refer/install-cron.sh`
- `workspace/xiaoyumao-news-web Refer/app/page.tsx`

### 同次工作中存在但不属于“自我兜底机制本体”的历史/上下文改动
- `workspace/xiaoyumao-news-web Refer/fetch_news_final.py`
- `workspace/xiaoyumao-news-web Refer/update_news_ts.py`

---

## 三、三种状态如何判定

### 1. `full_success`
含义：完整流程成功
判定条件：
- pipeline 通过
- build 通过
- deploy 通过
- 主域名验收通过
- 页面 `data-run-status=full_success`

### 2. `degraded_success`
含义：完整流程失败，但系统自动用最近成功数据完成降级兜底并上线
判定条件：
- 完整流程两次均失败
- 找到可用备份数据
- 重新构建成功
- 重新部署成功
- 主域名验收通过
- 页面 `data-run-status=degraded_success`

### 3. `failed`
含义：完整流程失败，且降级也失败
判定条件：
- 主流程失败
- 自动补跑失败
- 降级恢复失败，或构建/部署/验收失败
- 页面无法进入成功状态

---

## 四、自动补跑怎么触发，如何避免无限重试

### 自动补跑触发逻辑
- 主流程第 1 次失败后：
  - 记录失败摘要
  - 产出告警文件
  - 等待 5 秒
  - 自动再跑第 2 次

### 避免无限重试
- `MAX_FULL_ATTEMPTS = 2`
- 只允许一次自动补跑
- 第二次仍失败后，直接进入 degraded 分支，不再继续无限重试

---

## 五、单实例保护怎么做

使用：
- `status/self_heal.lock.json`

机制：
- 启动时检查锁文件
- 若已有活跃进程且锁未过期，则本次直接跳过，避免重入
- 若锁陈旧（超时或 pid 不存在），自动清理后继续
- 结束时释放锁

这解决的是：
- 重复 cron 触发
- 手动补跑与定时任务撞车
- 并发实例互相覆盖状态/部署

---

## 六、状态与告警产物

### 状态文件
- `status/last_run_status.json`
- `status/news-status.json`
- `status/run_history.jsonl`

### 告警文件
- `status/alerts/last_alert.json`
- `status/alerts/alert_history.jsonl`

### 关键字段
- `status`
- `runMode`
- `attempt`
- `retryTriggered`
- `degraded`
- `alertRaised`
- `failureSummary`
- `failureHistory`
- `onlineDate`
- `buildOk / deployOk / verifyOk`

也就是说，现在即使外部消息通知链路还没完全接上，系统内部已经具备：
- 明确失败产物
- 可机器读取状态
- 可追溯历史
- 可被上层进一步接管的告警接口

---

## 七、站点端可见性

`app/page.tsx` 已接入运行状态：
- 会显示当前状态标签
- 当为降级模式时，会明确显示“降级兜底已上线”
- 会展示失败摘要
- 页面上带有可验收的数据属性：
  - `data-run-status`
  - `data-content-date`
  - `data-status-updated-at`
  - `data-failure-summary`

这意味着：
- 不再把降级交付伪装成完整成功
- 验收脚本可以直接基于线上页面判定状态

---

## 八、当前已验证到什么程度

我验证到的是**真实闭环**，不是本地假跑：

### 本次真实演练过程
1. 13:14 启动自我兜底版主流程
2. attempt 1：pipeline 失败
3. 系统自动写告警并等待 5 秒
4. attempt 2：pipeline 再次失败
5. 系统自动切换到 degraded 分支
6. 恢复最近成功数据
7. 重新 build
8. 重新 deploy 到 Vercel
9. 主域名验收通过

### 当前线上验证结果
- 主域名：`https://xiaoyumao-news-web.vercel.app`
- 页面运行状态：`degraded_success`
- 页面内容日期：`2026年04月04日 周六`
- 页面已出现“降级兜底已上线”
- 失败摘要已对外可见：`[pipeline] 新闻内容生成流水线失败（attempt 2）`

### 当前状态文件结果
- `status = degraded_success`
- `retryTriggered = true`
- `alertRaised = true`
- `attempt = 2`
- `verifyOk = true`

---

## 九、还剩哪些风险

### 风险 1：外部通知链路还没正式闭环到用户消息
当前已实现“项目内可观测告警”，但还没有在机制层确认一个稳定、安全、默认可用的用户侧即时通知出口。

现状：
- 系统内部已具备 alert 产物
- 上层可以读取并转发
- 但项目自身还没有安全固化“直接向用户发消息”的能力

### 风险 2：降级内容来自最近成功数据
这是合理兜底，但不是最优体验。
更理想的下一步是：
- 支持“简版当日内容”而非直接回滚最近成功集
- 让 degraded 模式也尽量保留当天新鲜度

### 风险 3：pipeline 根因仍需继续治本
这次机制已经保证“不会再沉默失败”，但 pipeline 自身的数据质量 / 去重 / 源波动问题，仍需要继续优化，避免频繁触发 degraded。

---

## 十、最终判断

这套系统现在已经不再是：
> 失败了就静默躺平，等用户来问。

而是：
> 失败 → 立刻记状态 → 自动补跑 → 再失败就自动降级交付 → 重新部署 → 主域名验收 → 明确告诉外界当前是降级态。

这就叫**具备自我兜底能力**。

还差的最后一层，不是“内部机制”，而是：
- 把告警正式接到用户侧通知链路
- 让 degraded 模式从“最近成功内容回滚”升级为“简版当日交付”

---

## Git 提交
本次机制层提交：待本轮整理后单独提交。
