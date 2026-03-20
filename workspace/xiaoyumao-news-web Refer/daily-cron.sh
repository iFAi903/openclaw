#!/bin/bash
# =============================================================================
# 小羽毛 AI 新闻早报 - 每日自动发布脚本
# 执行时间：每日 07:00 (Asia/Taipei)
# 执行流程：Fetch → Update → Build → Deploy
# =============================================================================

set -euo pipefail  # 严格模式：遇到错误/未定义变量/管道失败立即退出

# =============================================================================
# 配置区
# =============================================================================
readonly PROJECT_DIR="/Users/ifai_macpro/.openclaw/workspace/iFAi/workspace/xiaoyumao-news-web Refer"
readonly LOG_FILE="/tmp/xiaoyumao-news-cron.log"
readonly BACKUP_BASE_DIR="./backups"
readonly MAX_BACKUPS=10
readonly DATE=$(date '+%Y-%m-%d %H:%M:%S')
readonly BACKUP_DIR="${BACKUP_BASE_DIR}/$(date +%Y%m%d_%H%M%S)"

# 从环境变量读取 Token（安全模式）
VERCEL_TOKEN="${VERCEL_TOKEN:-}"

# =============================================================================
# 工具函数
# =============================================================================

log() {
    echo "[$DATE] $1" >> "$LOG_FILE"
    echo "[$DATE] $1"
}

log_error() {
    echo "[$DATE] ❌ $1" >> "$LOG_FILE"
    echo "[$DATE] ❌ $1" >&2
}

log_success() {
    echo "[$DATE] ✅ $1" >> "$LOG_FILE"
    echo "[$DATE] ✅ $1"
}

cleanup_old_backups() {
    if [[ -d "$BACKUP_BASE_DIR" ]]; then
        local count
        count=$(find "$BACKUP_BASE_DIR" -type d -maxdepth 1 2>/dev/null | wc -l)
        count=$((count - 1))  # 减去基目录本身
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
        log_success "数据已备份到 $BACKUP_DIR"
    fi
    cleanup_old_backups
}

# =============================================================================
# 主流程
# =============================================================================

main() {
    # 前置检查
    if [[ -z "$VERCEL_TOKEN" ]]; then
        log_error "安全错误: 未设置 VERCEL_TOKEN 环境变量"
        log_error "请执行: export VERCEL_TOKEN='your-token-here'"
        exit 1
    fi

    # 进入项目目录
    if ! cd "$PROJECT_DIR" 2>/dev/null; then
        log_error "无法进入项目目录: $PROJECT_DIR"
        exit 1
    fi

    log "========================================"
    log "开始执行每日新闻更新"
    log "========================================"

    # 创建备份
    log "Step 0/4: 创建数据备份..."
    create_backup

    # Step 1: 获取新闻数据
    log "Step 1/4: 获取新闻数据..."
    if ! python3 fetch_news_final.py >> "$LOG_FILE" 2>&1; then
        log_error "新闻数据获取失败"
        exit 1
    fi

    if [[ ! -f "daily_data.json" ]]; then
        log_error "错误: daily_data.json 未生成"
        exit 1
    fi

    # 验证 JSON 有效性
    if ! python3 -c "import json; json.load(open('daily_data.json'))" 2>/dev/null; then
        log_error "错误: daily_data.json 不是有效的 JSON"
        exit 1
    fi

    log_success "新闻数据获取完成"

    # Step 2: 转换为 TypeScript 并更新 news.ts
    # 统一走 update_news_ts.py，避免与 fetch_news_final.py / generate_news_ts.py 出现双入口漂移
    log "Step 2/4: 更新新闻数据文件..."
    if ! python3 update_news_ts.py >> "$LOG_FILE" 2>&1; then
        log_error "TypeScript 文件生成失败"
        exit 1
    fi
    log_success "数据文件更新完成"

    # Step 3: 构建项目
    log "Step 3/4: 构建项目..."
    if ! npm run build >> "$LOG_FILE" 2>&1; then
        log_error "构建失败"
        exit 1
    fi
    log_success "构建完成"

    # Step 4: 部署到 Vercel
    log "Step 4/4: 部署到 Vercel..."
    if ! npx vercel --prod --token "$VERCEL_TOKEN" --yes >> "$LOG_FILE" 2>&1; then
        log_error "部署失败"
        exit 1
    fi
    log_success "部署完成"

    log "========================================"
    log "🎉 每日新闻早报更新成功！"
    log "========================================"
}

# 执行主流程
main "$@"
exit 0
