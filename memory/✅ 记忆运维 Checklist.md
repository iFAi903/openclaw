# ✅ 记忆运维 Checklist

> 用途：团队通用的记忆系统运维检查表。  
> 目标：确保小羽毛 CEO 与各分身的记忆链路、治理链路、权限链路持续可用。

---

# 一、日常检查（快速版）

## 1. 基础状态
- [ ] memory_stats 是否正常返回
- [ ] 总记忆数是否异常突增/突减
- [ ] recall 是否能正常返回结果
- [ ] 是否出现 embedding / rerank API 报错

## 2. 基础 CRUD
- [ ] 能写入一条临时测试记忆
- [ ] 能 recall 该测试记忆
- [ ] 能删除/忘记该测试记忆
- [ ] 删除后再次 recall，确认已移除

## 3. 自检清理
- [ ] 所有测试哨兵记忆是否已清理
- [ ] 是否遗留临时 debug 数据

---

# 二、每周检查（质量版）

## A. 排名质量检查

### 明确 query
测试示例：
- Leo 偏好 稳定 保守 默认 配置
- 新闻早报 来源分散

检查项：
- [ ] Top 1 是否正确命中目标记忆
- [ ] Top 3 内噪音是否可接受
- [ ] 是否有关键记忆缺失

### 抽象 query
测试示例：
- 小羽毛 CEO 天团 分身 总控
- 团队协作 组织方式 角色边界

检查项：
- [ ] 是否出现明显跑偏
- [ ] 是否命中真正的身份/结构类记忆
- [ ] 是否需要补关键词或重构记忆文本

### Debug / Explain
- [ ] memory_debug 是否正常
- [ ] rerank 耗时是否过长
- [ ] 是否出现 Jina 429 / embedding 超时
- [ ] explain_rank 是否能解释当前 top 结果

---

## B. 治理链路检查

### update
- [ ] 更新后 recall 是否命中最新文本
- [ ] 旧文本是否已正确替换/降级

### promote
- [ ] promote 后 state/layer 是否正确写入
- [ ] explain_rank 中是否可见治理状态

### archive
- [ ] archive 动作是否成功
- [ ] 是否明确理解 archive ≠ delete
- [ ] 默认召回是否降低，精准 recall 是否仍可见

### forget/delete
- [ ] 删除后是否确实 recall 不到
- [ ] 是否误删高价值记忆

---

# 三、团队权限检查（重点）

## 主会话
- [ ] CEO 是否拥有完整 memory CRUD
- [ ] 主会话能否执行 recall/debug/explain

## 子会话 / 分身
- [ ] 子会话是否能访问 memory_stats
- [ ] 子会话是否能访问 memory_store
- [ ] 子会话是否能访问 memory_recall
- [ ] 子会话是否能访问 memory_update
- [ ] 子会话是否能访问 memory_archive/promote

## 隔离性
- [ ] 子会话 A 是否只能看到自己的测试记忆
- [ ] 子会话 B 是否不会串读 A 的私有测试记忆
- [ ] CEO 是否能在预期范围内看到共享层信息

## 配置
- [ ] agents.list[].tools.alsoAllow 是否正确补齐 memory_* 工具
- [ ] 是否误改了不被 schema 支持的字段
- [ ] 重启后 gateway 是否正常加载

---

# 四、变更前 Checklist

任何涉及记忆插件 / 配置 / 权限修复时，先检查：

- [ ] 是否确认正在修改正确的插件仓库
- [ ] 是否先查看当前版本与远端差异
- [ ] 是否先备份配置文件
- [ ] 是否确认配置 schema 支持要改的字段
- [ ] 是否采用最小改动原则
- [ ] 修改 TS 插件代码后是否准备清 `/tmp/jiti/`
- [ ] 是否计划在改后立即 restart + 验证

---

# 五、变更后 Checklist

## 插件/代码更新后
- [ ] 依赖是否完整安装
- [ ] `/tmp/jiti/` 是否已清理
- [ ] gateway 是否已重启
- [ ] 插件是否成功注册
- [ ] 是否出现 failed to load

## 运行验证
- [ ] memory_stats 正常
- [ ] memory_store 正常
- [ ] memory_recall 正常
- [ ] memory_update 正常
- [ ] memory_promote 正常
- [ ] memory_archive 正常
- [ ] memory_forget 正常

---

# 六、常见故障模式

## 故障 1：主会话能用，子会话不能用
高概率原因：
- agent tools allowlist 未补 memory_* 工具
- subagent 继承到的是较窄工具集

检查：
- [ ] agents.list[].tools.alsoAllow
- [ ] 子会话工具清单

## 故障 2：插件更新后加载失败
高概率原因：
- 缺依赖
- jiti 缓存未清
- 配置 schema 不合法

检查：
- [ ] npm install
- [ ] rm -rf /tmp/jiti/
- [ ] gateway restart
- [ ] status / logs

## 故障 3：Recall 能用但结果很脏
高概率原因：
- 记忆文本不够原子
- query 太抽象
- ranking / rerank 受到噪音影响

检查：
- [ ] memory_debug
- [ ] 是否要补关键词
- [ ] 是否要拆分记忆

## 故障 4：Archive 后仍能 recall 到
说明：
- 这不一定是 bug
- archive 是治理降级，不是物理删除

检查：
- [ ] 是否误把 archive 当成 delete
- [ ] 是否应改用 forget

---

# 七、操作准则

### 做对一件事的顺序
1. 先判断问题属于：链路 / 排名 / 治理 / 权限 / 配置 哪一层
2. 先验证，再下结论
3. 先最小改动，再全局推广
4. 每做一步就立即验证
5. 测试痕迹必须清理

### 禁止事项
- [ ] 禁止把主记忆正常说成团队记忆正常
- [ ] 禁止把 archive 说成 delete
- [ ] 禁止配置未验 schema 就直接下注
- [ ] 禁止保留测试哨兵记忆污染长期库
- [ ] 禁止只凭 recall 成功就宣布系统没问题

---

# 八、值班结论模板

## 简版
- 主记忆：正常 / 异常
- 团队记忆：正常 / 异常 / 待验证
- 排名质量：良好 / 一般 / 噪音明显
- 治理链路：正常 / 部分异常
- 权限链路：正常 / 缺失 / 待修复

## 完整版
1. 现象
2. 已验证范围
3. 未验证范围
4. 高概率根因
5. 已证实根因
6. 修复动作
7. 修复后验证结果
8. 是否已清理测试痕迹

---

*状态：启用中*  
*建议：每周至少完整执行一次。每次插件升级后必须执行一次。*
