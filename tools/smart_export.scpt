#!/usr/bin/env osascript
-- 智能分笔记本导出脚本
-- 逐个自动导出 9 个笔记本

set notebookList to {
    "在路上的日记",
    "会议必备",
    "哲学与思想",
    "个人创作",
    "thinkingblue的笔记本",
    "我的剪贴板",
    "01 INPUT",
    "02 PROCESSING",
    "03 OUTPUT"
}

set exportFolder to (path to desktop as string) & "Evernote_Notebooks_Export_" & (do shell script "date +%Y%m%d_%H%M%S")

-- 创建导出目录
do shell script "mkdir -p " & quoted form of (POSIX path of exportFolder)

tell application "印象笔记"
    activate
    display notification "开始批量导出 9 个笔记本..." with title "印象笔记导出助手"
    
    repeat with notebookName in notebookList
        try
            -- 尝试切换到该笔记本
            set current notebook to notebook notebookName
            delay 2
            
            -- 获取笔记数量
            set noteCount to count of notes
            
            if noteCount > 0 then
                -- 全选笔记
                select every note
                delay 1
                
                -- 这里需要 UI 自动化来点击导出菜单
                -- 由于权限限制，提示用户手动操作
                display notification "请手动导出: " & notebookName & " (" & noteCount & " 条笔记)" with title "需要操作"
                
                -- 暂停等待用户操作
                delay 5
            end if
            
        on error errMsg
            display notification "跳过 " & notebookName & ": " & errMsg with title "导出提示"
        end try
    end repeat
    
    display notification "笔记本遍历完成！" with title "导出助手"
end tell
