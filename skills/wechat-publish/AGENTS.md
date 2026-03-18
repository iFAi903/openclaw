# AGENTS.md - wechat-publish 技能共享配置

## 技能名称
wechat-publish

## 功能
将内容推送到微信公众号草稿箱

## 共享 Agent

| Agent | 角色 | 使用场景 |
|-------|------|----------|
| CEO | 总控 | 直接发布重要内容、最终审核 |
| CRO | 创意/增长 | 发布品牌文案、增长内容 |
| copy-agent | 文案 | 发布原创文章、创意内容 |

## 团队架构说明

- **CEO**: 总设计师和调度师，负责最终发布决策
- **CRO**: 创意与增长战略，负责品牌调性和增长文案
- **copy-agent**: 专职文案创作，负责内容撰写

## 使用方式

### 命令行调用
```bash
# 直接发布
python3 skills/wechat-publish/publish.py \
  --title "文章标题" \
  --content "文章内容" \
  --author "作者"

# 从文件发布
python3 skills/wechat-publish/publish.py \
  --title "文章标题" \
  --file /path/to/article.md
```

### Agent 工作流调用
```yaml
steps:
  - name: 发布到公众号
    action: exec
    params:
      command: |
        python3 skills/wechat-publish/publish.py \
          --title "{{title}}" \
          --file "{{content_file}}"
```

## 环境依赖

- Python 3.7+
- requests 库
- 环境变量: WECHAT_APP_ID, WECHAT_APP_SECRET

## 凭证配置

凭证已配置在 `~/.openclaw/workspace/iFAi/.env`：
- WECHAT_APP_ID=wx949ae2e2453a622b
- WECHAT_APP_SECRET=[已安全存储]
