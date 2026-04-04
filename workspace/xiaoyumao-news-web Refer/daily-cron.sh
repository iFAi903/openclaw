#!/bin/bash
# =============================================================================
# 小羽毛 AI 新闻早报 - 每日自动发布入口（自我兜底版）
# 说明：真正的主逻辑在 news_self_heal.py，这里只负责提供稳定的 cron 入口。
# =============================================================================

set -euo pipefail

readonly PROJECT_DIR="/Users/ifai_macpro/.openclaw/workspace/iFAi/workspace/xiaoyumao-news-web Refer"

cd "$PROJECT_DIR"

if [[ -f "$PROJECT_DIR/.env.cron" ]]; then
  # shellcheck disable=SC1090
  source "$PROJECT_DIR/.env.cron"
fi

exec python3 "$PROJECT_DIR/news_self_heal.py"
