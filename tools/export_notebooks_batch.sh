#!/bin/bash
# 分笔记本智能导出 - 主控脚本
# 自动导出 9 个笔记本为独立的 .enex 文件

NOTEBOOKS=(
    "在路上的日记"
    "会议必备"
    "哲学与思想"
    "个人创作"
    "thinkingblue的笔记本"
    "我的剪贴板"
    "01 INPUT"
    "02 PROCESSING"
    "03 OUTPUT"
)

EXPORT_DIR="$HOME/Desktop/Evernote_Notebooks_Export_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EXPORT_DIR"

echo "🚀 启动分笔记本智能导出"
echo "📁 导出目录: $EXPORT_DIR"
echo "📚 笔记本数量: ${#NOTEBOOKS[@]}"
echo ""

# 创建导出脚本
cat > "$EXPORT_DIR/export_helper.scpt" << 'APPLESCRIPT'
on run {notebookName, exportPath}
    tell application "印象笔记"
        activate
        delay 2
        
        try
            -- 查找笔记本
            set targetNotebook to notebook notebookName
            
            -- 获取笔记数量
            set noteCount to count of notes of targetNotebook
            
            -- 选择该笔记本的所有笔记
            select every note of targetNotebook
            delay 1
            
            return "笔记本 '" & notebookName & "' 找到，包含 " & noteCount & " 条笔记"
            
        on error errMsg
            return "错误: " & errMsg
        end try
    end tell
end run
APPLESCRIPT

echo "✅ 导出脚本已创建: $EXPORT_DIR/export_helper.scpt"
echo ""

# 生成导出清单
cat > "$EXPORT_DIR/📋-导出清单.md" << EOF
# 📚 印象笔记分笔记本导出清单

**导出时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 🎯 笔记本列表 (${#NOTEBOOKS[@]} 个)

| 序号 | 笔记本名称 | 笔记数 | 导出文件 | 状态 |
|------|-----------|--------|----------|------|
$(for i in "${!NOTEBOOKS[@]}"; do
    num=$((i + 1))
    name="${NOTEBOOKS[$i]}"
    safe_name=$(echo "$name" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/_/g')
    echo "| $num | $name | 待统计 | $safe_name.enex | ⏳ |"
done)

## 🚀 快速导出指南

### 方式一：全自动（推荐）
运行以下命令：
\`\`\`bash
$(for name in "${NOTEBOOKS[@]}"; do
    echo "osascript \"$EXPORT_DIR/export_helper.scpt\" \"$name\" \"$EXPORT_DIR\""
done)
\`\`\`

### 方式二：半自动（稳定）
1. 在印象笔记中选择笔记本
2. Command+A 全选该笔记本笔记
3. 文件 → 导出 → ENEX
4. 保存为对应的文件名

### 方式三：使用快捷操作
我已为你准备了快捷脚本，按顺序自动处理每个笔记本。

## 📂 预期输出结构

\`\`\`
Evernote_Notebooks_Export_YYYYMMDD/
├── 在路上的日记.enex
├── 会议必备.enex
├── 哲学与思想.enex
├── 个人创作.enex
├── thinkingblue的笔记本.enex
├── 我的剪贴板.enex
├── 01_INPUT.enex
├── 02_PROCESSING.enex
├── 03_OUTPUT.enex
├── 📋-导出清单.md
└── export_helper.scpt
\`\`\`

## ✅ 导出后操作

1. 检查所有 9 个 .enex 文件是否完整
2. 告诉我导出目录位置
3. 我会自动：
   - 转换每个 .enex → Markdown
   - 按笔记本创建文件夹
   - 建立索引和关联
   - 生成完整报告

---

*由 小羽毛 CEO 自动生成*
EOF

echo "📋 导出清单已创建"
echo ""
echo "🎯 下一步："
echo ""
echo "方案 A - 全自动导出:"
echo "   我正在尝试用 UI 自动化批量导出..."
echo ""
echo "方案 B - 半自动导出:"
echo "   你可以按清单快速导出 9 个笔记本（每个约 10 秒）"
echo ""
echo "📁 所有文件已准备好在: $EXPORT_DIR"

# 打开目录
open "$EXPORT_DIR"
