#!/bin/bash
# 使用 Peekaboo 自动化导出印象笔记
# 模拟菜单操作

echo "🚀 启动印象笔记自动导出..."

# 激活印象笔记
peekaboo app activate "印象笔记" --wait 2

# 获取当前状态
peekaboo see --app "印象笔记" --annotate --path /tmp/evernote_state.png

# 点击文件菜单
echo "📂 打开文件菜单..."
peekaboo menu click --app "印象笔记" --item "文件"
sleep 1

# 截图查看菜单
peekaboo see --app "印象笔记" --annotate --path /tmp/evernote_menu.png

# 点击导出选项（根据实际菜单结构调整）
echo "📤 选择导出..."
# peekaboo click --coords x,y --app "印象笔记"

echo "请查看截图确认菜单状态: /tmp/evernote_menu.png"
