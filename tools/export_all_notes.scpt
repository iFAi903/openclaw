#!/usr/bin/env osascript
-- 印象笔记全自动批量导出脚本 (System Events 版本)
-- 此脚本会模拟实际操作导出所有笔记

on run
    set exportFolder to (path to desktop as string) & "Evernote_Export_" & (do shell script "date +%Y%m%d_%H%M%S")
    
    tell application "Finder"
        make new folder at desktop with properties {name:"Evernote_Export_" & (do shell script "date +%Y%m%d_%H%M%S")}
        set exportFolder to result as string
    end tell
    
    set exportPath to POSIX path of exportFolder
    
    tell application "印象笔记"
        activate
        delay 3
        
        -- 获取笔记数量
        try
            set noteCount to count of notes
            display notification "发现 " & noteCount & " 条笔记，开始导出..." with title "印象笔记导出"
            
            -- 全选所有笔记
            select every note
            delay 1
            
        on error
            display notification "请手动全选笔记 (Command+A)" with title "需要操作"
        end try
    end tell
    
    -- 使用 System Events 操作菜单
    tell application "System Events"
        tell process "印象笔记"
            -- 点击文件菜单
            click menu item "导出笔记..." of menu "文件" of menu bar 1
            delay 2
            
            -- 处理保存对话框
            tell window 1
                -- 设置文件名
                set value of text field 1 to "All_Notes"
                delay 0.5
                
                -- 点击保存
                click button "存储"
                delay 1
            end tell
        end tell
    end tell
    
    display notification "导出完成！位置: " & exportPath with title "印象笔记导出"
    return exportPath
end run
