#!/usr/bin/env python3
"""
印象笔记自动化导出方案
结合 AppleScript + UI 自动化
"""

import subprocess
import time
import json
from datetime import datetime

def get_notebooks():
    """获取所有笔记本列表"""
    script = '''
    tell application "印象笔记"
        set notebookList to {}
        repeat with nb in notebooks
            set end of notebookList to name of nb
        end repeat
        return notebookList
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            # 解析返回的列表
            notebooks = result.stdout.strip().split(', ')
            return [nb.strip() for nb in notebooks if nb.strip()]
    except Exception as e:
        print(f"获取笔记本失败: {e}")
    
    return []

def export_notebook_ui(notebook_name, export_dir):
    """使用 UI 自动化导出单个笔记本"""
    print(f"📤 导出笔记本: {notebook_name}")
    
    # 1. 激活印象笔记
    subprocess.run(['osascript', '-e', 'tell application "印象笔记" to activate'])
    time.sleep(1)
    
    # 2. 选择笔记本（通过搜索或列表）
    # 使用 Command+J 跳转到笔记本
    script = f'''
    tell application "印象笔记"
        activate
        tell application "System Events"
            keystroke "j" using command down
            delay 0.5
            keystroke "{notebook_name}"
            delay 0.5
            key code 36  -- 回车
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', script])
    time.sleep(1)
    
    # 3. 全选笔记 (Command+A)
    script = '''
    tell application "System Events"
        keystroke "a" using command down
        delay 0.5
    end tell
    '''
    subprocess.run(['osascript', '-e', script])
    
    # 4. 打开导出菜单
    safe_name = notebook_name.replace(' ', '_').replace('/', '_')
    export_path = f"{export_dir}/{safe_name}.enex"
    
    script = f'''
    tell application "印象笔记"
        activate
        tell application "System Events"
            -- 文件菜单
            click menu item "导出笔记..." of menu "文件" of menu bar 1 of application process "印象笔记"
            delay 2
            
            -- 这里需要处理保存对话框
            -- 实际实现需要更复杂的逻辑
        end tell
    end tell
    '''
    
    # 注意：UI 自动化需要辅助功能权限
    print(f"  导出路径: {export_path}")
    return True

def main():
    print("=" * 50)
    print("🎯 印象笔记批量导出工具")
    print("=" * 50)
    
    # 创建导出目录
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_dir = f"~/Desktop/Evernote_Batch_Export_{timestamp}"
    
    subprocess.run(['mkdir', '-p', export_dir])
    print(f"📁 导出目录: {export_dir}")
    
    # 获取笔记本列表
    print("\n📚 扫描笔记本...")
    notebooks = get_notebooks()
    
    if not notebooks:
        print("❌ 未能获取笔记本列表")
        print("\n💡 建议方案:")
        print("1. 确保印象笔记应用正在运行")
        print("2. 检查是否需要登录印象笔记账户")
        print("3. 考虑手动导出后使用转换工具")
        return
    
    print(f"✅ 发现 {len(notebooks)} 个笔记本:")
    for i, nb in enumerate(notebooks, 1):
        print(f"   {i}. {nb}")
    
    # 导出统计
    print("\n" + "=" * 50)
    print("📊 导出方案")
    print("=" * 50)
    print("\n由于印象笔记新版限制了自动化接口，推荐以下方案:")
    print("\n方案 A: 手动批量导出（推荐）")
    print("   1. 在印象笔记中选择所有笔记 (Command+A)")
    print("   2. 文件 → 导出笔记 → ENEX 格式")
    print("   3. 保存到桌面，我会自动处理后续转换")
    
    print("\n方案 B: 分笔记本导出")
    print("   逐个笔记本导出为独立的 .enex 文件")
    print("   优点: 结构清晰，便于分类")
    
    print("\n方案 C: 使用第三方工具")
    print("   evernote-backup (需要 API Token)")
    print("   可以云端同步后导出")
    
    # 保存笔记本清单
    manifest = {
        'export_time': timestamp,
        'total_notebooks': len(notebooks),
        'notebooks': notebooks,
        'export_dir': export_dir
    }
    
    manifest_path = f"{export_dir}/notebook_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 笔记本清单已保存: {manifest_path}")
    print("\n✨ 准备就绪！请选择上述方案之一开始导出。")

if __name__ == '__main__':
    main()
