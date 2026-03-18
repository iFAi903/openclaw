#!/usr/bin/env osascript
-- 印象笔记批量自动导出脚本
-- 导出所有笔记到指定目录

on run argv
    set exportFolder to ""
    
    if (count of argv) > 0 then
        set exportFolder to item 1 of argv as string
    else
        set exportFolder to (path to desktop as string) & "Evernote_Export_" & (do shell script "date +%Y%m%d_%H%M%S")
    end if
    
    -- 创建导出目录
    do shell script "mkdir -p " & quoted form of (POSIX path of exportFolder)
    
    tell application "印象笔记"
        activate
        delay 2
        
        try
            -- 获取所有笔记本
            set allNotebooks to notebooks
            set notebookCount to count of allNotebooks
            
            log "找到 " & notebookCount & " 个笔记本"
            
            repeat with i from 1 to notebookCount
                set currentNotebook to item i of allNotebooks
                set notebookName to name of currentNotebook
                
                log "正在处理笔记本: " & notebookName
                
                try
                    -- 创建笔记本对应的导出文件
                    set safeName to do shell script "echo " & quoted form of notebookName & " | sed 's/[^a-zA-Z0-9]/_/g'"
                    set exportPath to exportFolder & ":" & safeName & ".enex"
                    
                    -- 导出整个笔记本
                    export currentNotebook to file exportPath format ENEX
                    
                    log "✓ 已导出: " & notebookName
                    
                on error errMsg
                    log "✗ 导出失败 [" & notebookName & "]: " & errMsg
                end try
                
                delay 1
            end repeat
            
            log "批量导出完成！"
            log "导出位置: " & exportFolder
            
        on error errMsg
            log "错误: " & errMsg
            -- 尝试英文版应用名称
            try
                tell application "Evernote"
                    set allNotebooks to notebooks
                    log "找到 Evernote (英文版): " & (count of allNotebooks) & " 个笔记本"
                end tell
            on error
                log "无法访问印象笔记，请确保应用正在运行"
            end try
        end try
    end tell
end run
