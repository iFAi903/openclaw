#!/bin/bash
# =============================================================================
# 小羽毛 AI 新闻早报 — 构建 + Vercel 部署
# =============================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR"

# ── 1. 构建 ──
echo "🔨 Building Next.js..."
npm run build 2>&1 | tail -20

# ── 2. 部署 ──
echo ""
echo "🚀 Deploying to Vercel..."

if [[ -n "${VERCEL_TOKEN:-}" ]]; then
  npx vercel --yes --prod --token "$VERCEL_TOKEN" 2>&1
elif [[ -f "$SKILL_DIR/.env.cron" ]]; then
  source "$SKILL_DIR/.env.cron"
  npx vercel --yes --prod --token "$VERCEL_TOKEN" 2>&1
else
  echo "❌ VERCEL_TOKEN 未设置"
  exit 1
fi

echo ""
echo "✅ 部署完成 → https://ai-news-roundup.vercel.app"
