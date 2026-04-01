#!/bin/bash
# =============================================================================
# 小羽毛 AI 新闻早报 - 每日自动发布脚本
# 执行时间：每日 07:00 (Asia/Taipei)
# 执行流程：Fetch → Update → Build → Deploy → Verify
# =============================================================================

set -euo pipefail

# 防重入锁：避免 cron / scheduler 重复触发导致同一时刻并发执行
readonly LOCK_DIR="/tmp/xiaoyumao-news-cron.lock"

# =============================================================================
# 配置区
# =============================================================================
readonly PROJECT_DIR="/Users/ifai_macpro/.openclaw/workspace/iFAi/workspace/xiaoyumao-news-web Refer"
readonly RUNTIME_LOG_FILE="/tmp/xiaoyumao-news-cron.log"
readonly LOG_DIR="$PROJECT_DIR/logs"
readonly STATUS_DIR="$PROJECT_DIR/status"
readonly STATUS_FILE="$STATUS_DIR/last_run_status.json"
readonly PERSISTENT_LOG_FILE="$LOG_DIR/cron-$(date +%Y-%m-%d).log"
readonly BACKUP_BASE_DIR="./backups"
readonly MAX_BACKUPS=10
readonly START_TS=$(date '+%Y-%m-%dT%H:%M:%S%z')
readonly DATE=$(date '+%Y-%m-%d %H:%M:%S')
readonly BACKUP_DIR="${BACKUP_BASE_DIR}/$(date +%Y%m%d_%H%M%S)"
readonly PROD_URL="https://xiaoyumao-news-web.vercel.app"
readonly DEPLOY_TIMEOUT_SECONDS=180

mkdir -p "$LOG_DIR" "$STATUS_DIR"

# 从环境变量或项目内 .env.cron 读取 Token（cron 环境常常不继承交互式 shell）
if [[ -f "$PROJECT_DIR/.env.cron" ]]; then
    # shellcheck disable=SC1090
    source "$PROJECT_DIR/.env.cron"
fi
VERCEL_TOKEN="${VERCEL_TOKEN:-}"

STATUS="running"
STEP="init"
MESSAGE=""
DEPLOY_URL=""
PRODUCTION_URL="$PROD_URL"
GENERATED_DATE=""
ONLINE_DATE=""
NEWS_COUNT=0
PRODUCT_COUNT=0
BUILD_OK=false
DEPLOY_OK=false
VERIFY_OK=false
BACKUP_PATH=""

# =============================================================================
# 工具函数
# =============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$RUNTIME_LOG_FILE" "$PERSISTENT_LOG_FILE"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $1" | tee -a "$RUNTIME_LOG_FILE" "$PERSISTENT_LOG_FILE" >&2
}

log_success() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1" | tee -a "$RUNTIME_LOG_FILE" "$PERSISTENT_LOG_FILE"
}

json_escape() {
    python3 - <<'PY' "$1"
import json,sys
print(json.dumps(sys.argv[1], ensure_ascii=False))
PY
}

write_status() {
    local ended_at
    ended_at=$(date '+%Y-%m-%dT%H:%M:%S%z')
    cat > "$STATUS_FILE" <<EOF
{
  "status": $(json_escape "$STATUS"),
  "step": $(json_escape "$STEP"),
  "message": $(json_escape "$MESSAGE"),
  "startedAt": $(json_escape "$START_TS"),
  "endedAt": $(json_escape "$ended_at"),
  "generatedDate": $(json_escape "$GENERATED_DATE"),
  "onlineDate": $(json_escape "$ONLINE_DATE"),
  "newsCount": $NEWS_COUNT,
  "productsCount": $PRODUCT_COUNT,
  "buildOk": $BUILD_OK,
  "deployOk": $DEPLOY_OK,
  "verifyOk": $VERIFY_OK,
  "backupPath": $(json_escape "$BACKUP_PATH"),
  "deployUrl": $(json_escape "$DEPLOY_URL"),
  "productionUrl": $(json_escape "$PRODUCTION_URL"),
  "persistentLog": $(json_escape "$PERSISTENT_LOG_FILE")
}
EOF
}

fail_and_exit() {
    STATUS="failed"
    STEP="$1"
    MESSAGE="$2"
    write_status
    log_error "$2"
    exit 1
}

cleanup_old_backups() {
    if [[ -d "$BACKUP_BASE_DIR" ]]; then
        local count
        count=$(find "$BACKUP_BASE_DIR" -type d -maxdepth 1 2>/dev/null | wc -l)
        count=$((count - 1))
        if (( count > MAX_BACKUPS )); then
            find "$BACKUP_BASE_DIR" -type d -maxdepth 1 | sort -r | tail -n +$((MAX_BACKUPS + 1)) | while read -r dir; do
                if [[ "$dir" != "$BACKUP_BASE_DIR" ]]; then
                    rm -rf "$dir"
                fi
            done
            log "已清理旧备份，保留最近 $MAX_BACKUPS 个"
        fi
    fi
}

create_backup() {
    mkdir -p "$BACKUP_DIR"
    if [[ -f "daily_data.json" ]]; then
        cp daily_data.json "$BACKUP_DIR/"
        BACKUP_PATH="$BACKUP_DIR/daily_data.json"
        log_success "数据已备份到 $BACKUP_DIR"
    fi
    cleanup_old_backups
}

read_generated_summary() {
    local summary
    summary=$(python3 - <<'PY'
import json
with open('daily_data.json','r',encoding='utf-8') as f:
    data=json.load(f)
print(data.get('date',''))
print(len(data.get('news',[])))
print(len(data.get('products',[])))
PY
)
    GENERATED_DATE=$(echo "$summary" | sed -n '1p')
    NEWS_COUNT=$(echo "$summary" | sed -n '2p')
    PRODUCT_COUNT=$(echo "$summary" | sed -n '3p')
}

verify_production_site() {
    local expected="$1"
    local deadline=$(( $(date +%s) + DEPLOY_TIMEOUT_SECONDS ))
    while (( $(date +%s) < deadline )); do
        ONLINE_DATE=$(python3 - <<'PY'
import urllib.request, re
url='https://xiaoyumao-news-web.vercel.app'
html=urllib.request.urlopen(url, timeout=20).read().decode('utf-8', errors='ignore')
m=re.search(r'2026年\d{2}月\d{2}日 周[一二三四五六日天]', html)
print(m.group(0) if m else '')
PY
)
        if [[ -n "$ONLINE_DATE" && "$ONLINE_DATE" == "$expected"* ]]; then
            VERIFY_OK=true
            return 0
        fi
        sleep 5
    done
    return 1
}

# =============================================================================
# 主流程
# =============================================================================

main() {
    if ! mkdir "$LOCK_DIR" 2>/dev/null; then
        log "⚠️ 检测到已有运行中的实例，跳过本次执行（lock: $LOCK_DIR）"
        exit 0
    fi
    trap 'rm -rf "$LOCK_DIR"' EXIT

    write_status

    if [[ -z "$VERCEL_TOKEN" ]]; then
        fail_and_exit "preflight" "安全错误: 未设置 VERCEL_TOKEN 环境变量"
    fi

    if ! cd "$PROJECT_DIR" 2>/dev/null; then
        fail_and_exit "preflight" "无法进入项目目录: $PROJECT_DIR"
    fi

    log "========================================"
    log "开始执行每日新闻更新"
    log "持久日志: $PERSISTENT_LOG_FILE"
    log "状态文件: $STATUS_FILE"
    log "========================================"

    STEP="backup"
    MESSAGE="创建数据备份"
    write_status
    create_backup

    STEP="pipeline"
    MESSAGE="执行新闻内容生成流水线"
    write_status
    log "Step 1/4: 执行新闻内容生成流水线..."
    if ! bash "$PROJECT_DIR/run-news-pipeline.sh" >> "$RUNTIME_LOG_FILE" 2>&1; then
        fail_and_exit "pipeline" "新闻内容生成流水线失败"
    fi
    read_generated_summary
    log_success "新闻内容生成完成：$GENERATED_DATE / ${NEWS_COUNT}条新闻 / ${PRODUCT_COUNT}个产品"

    STEP="build"
    MESSAGE="构建项目"
    write_status
    log "Step 2/4: 构建项目..."
    if ! npm run build >> "$RUNTIME_LOG_FILE" 2>&1; then
        fail_and_exit "build" "构建失败"
    fi
    BUILD_OK=true
    log_success "构建完成"

    STEP="deploy"
    MESSAGE="部署到 Vercel"
    write_status
    log "Step 3/4: 部署到 Vercel..."
    local deploy_output
    if ! deploy_output=$(npx vercel --prod --token "$VERCEL_TOKEN" --yes 2>&1); then
        echo "$deploy_output" >> "$RUNTIME_LOG_FILE"
        fail_and_exit "deploy" "部署失败"
    fi
    echo "$deploy_output" >> "$RUNTIME_LOG_FILE"
    DEPLOY_URL=$(echo "$deploy_output" | grep -Eo 'https://[^ ]+vercel.app' | head -1 || true)
    DEPLOY_OK=true
    log_success "部署完成${DEPLOY_URL:+：$DEPLOY_URL}"

    STEP="verify"
    MESSAGE="校验主域名上线状态"
    write_status
    log "Step 4/4: 校验主域名是否已更新..."
    if ! verify_production_site "$GENERATED_DATE"; then
        fail_and_exit "verify" "主域名未在限定时间内切换到最新日期（期望: $GENERATED_DATE，实际: ${ONLINE_DATE:-未知}）"
    fi

    STATUS="success"
    VERIFY_OK=true
    STEP="done"
    MESSAGE="每日新闻早报更新成功，并已通过主域名验收"
    write_status
    log_success "主域名验收通过：$ONLINE_DATE"
    log "========================================"
    log "🎉 每日新闻早报更新成功！"
    log "========================================"
}

main "$@"
exit 0
