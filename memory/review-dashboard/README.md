# Review Dashboard 使用说明

## 存储位置

审查记录以 JSON Lines (jsonl) 格式存储：

```
memory/review-dashboard/
├── schema.json          # 数据结构定义
├── README.md            # 本说明文件
├── {project}-{branch}.jsonl   # 项目审查记录
└── global-summary.jsonl       # 全局汇总
```

## 文件命名规范

```
{project-name}-{branch-name}.jsonl

示例:
- ifai-website-main.jsonl
- ifai-website-feature-navbar.jsonl
- landing-page-redesign.jsonl
```

## 记录格式 (JSON Lines)

每行一个完整的 JSON 对象：

```jsonl
{"id":"review-001","timestamp":"2026-03-18T16:42:00Z","project":"ifai-website","branch":"feature-navbar","reviewer":"review-agent","status":"approved","scores":{"correctness":9,"code_quality":8,"maintainability":8,"performance":9,"security":9,"test_coverage":7,"documentation":8},"overall_score":8.3,"files_reviewed":5,"findings":[]}
{"id":"review-002","timestamp":"2026-03-18T17:30:00Z","project":"ifai-website","branch":"feature-auth","reviewer":"review-agent","status":"needs_fix","scores":{"correctness":7,"code_quality":8,"maintainability":6,"performance":8,"security":6,"test_coverage":5,"documentation":7},"overall_score":6.7,"files_reviewed":12,"findings":[{"id":"F001","severity":"high","category":"ASK","dimension":"security","file":"src/auth/login.ts","line_start":45,"message":"JWT secret 硬编码，需要使用环境变量","suggestion":"将 JWT_SECRET 移至 .env 文件"},{"id":"F002","severity":"medium","category":"AUTO-FIX","dimension":"code_quality","file":"src/auth/login.ts","line_start":23,"message":"变量命名不规范","suggestion":"将 'usr' 改为 'user'","auto_fixed":true,"fix_commit":"abc123"}]}
```

## 状态流转

```
待审查 (pending)
    ↓ CEO 调用 Review Agent
审查中 (in_progress)
    ↓ 审查完成
    ├─→ 需修复 (needs_fix) ──→ 修复后重新审查
    ├─→ 已通过 (approved) ──→ 可进入 ship 阶段
    └─→ 已拒绝 (rejected) ──→ 需要重大修改
```

## 查询示例

### 查看最新审查状态

```bash
# 查看特定项目的最新审查
tail -1 memory/review-dashboard/ifai-website-main.jsonl | jq '.'

# 查看所有未通过的审查
cat memory/review-dashboard/*.jsonl | jq 'select(.status != "approved")'

# 统计各状态数量
cat memory/review-dashboard/*.jsonl | jq -s 'group_by(.status) | map({status: .[0].status, count: length})'
```

### 查看评分趋势

```bash
# 查看某个项目的评分变化
cat memory/review-dashboard/ifai-website-main.jsonl | jq '{timestamp, overall_score, status}'
```

## 发布门控检查

在 ship 前，检查审查状态：

```bash
#!/bin/bash
PROJECT="ifai-website"
BRANCH=$(git branch --show-current)

# 获取最新审查状态
STATUS=$(tail -1 "memory/review-dashboard/${PROJECT}-${BRANCH}.jsonl" | jq -r '.status')

if [ "$STATUS" != "approved" ]; then
    echo "❌ 审查未通过，当前状态: $STATUS"
    echo "请先完成审查修复"
    exit 1
fi

echo "✅ 审查已通过，可以发布"
```

## 7维度评分权重

| 维度 | 权重 | 最低要求 |
|------|------|---------|
| 功能正确性 | 25% | ≥ 8 |
| 代码质量 | 20% | ≥ 8 |
| 可维护性 | 15% | ≥ 8 |
| 性能 | 15% | ≥ 8 |
| 安全性 | 10% | ≥ 8 |
| 测试覆盖 | 10% | ≥ 8 |
| 文档完整性 | 5% | ≥ 8 |

**综合评分计算公式**:
```
overall_score = Σ(dimension_score × weight)
```

## 与 Ship 流程集成

在 `ship` 工作流中，Step 1 (Pre-flight) 必须检查 Review Readiness Dashboard：

1. 读取当前分支的审查记录
2. 检查状态是否为 `approved`
3. 检查所有维度评分是否 ≥ 8
4. 如有未通过的维度，终止 ship 流程
