#!/bin/bash
# 印象笔记 → Obsidian 批量转换脚本
# 使用方法: ./migrate-evernote.sh <enex文件路径>

ENEX_FILE="$1"
OUTPUT_DIR="$HOME/Documents/Obsidian Vault/印象笔记导入/$(date +%Y-%m-%d)"

if [ -z "$ENEX_FILE" ]; then
    echo "❌ 请提供 .enex 文件路径"
    echo "用法: $0 <enex文件路径>"
    exit 1
fi

if [ ! -f "$ENEX_FILE" ]; then
    echo "❌ 文件不存在: $ENEX_FILE"
    exit 1
fi

echo "🚀 开始转换印象笔记..."
echo "📁 源文件: $ENEX_FILE"
echo "📂 输出目录: $OUTPUT_DIR"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 使用 Yarle 转换
cd ~/.openclaw/workspace/Feishu/tools/yarle
npx yarle --enexSource "$ENEX_FILE" --outputDir "$OUTPUT_DIR" --templateFile ./config/template.tmpl

echo "✅ 转换完成！"
echo "📊 统计信息："
find "$OUTPUT_DIR" -name "*.md" | wc -l | xargs echo "  Markdown 文件数:"
find "$OUTPUT_DIR" -type f ! -name "*.md" | wc -l | xargs echo "  附件数量:"
du -sh "$OUTPUT_DIR" | awk '{print "  总大小: " $1}'
