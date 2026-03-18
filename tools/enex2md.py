#!/usr/bin/env python3
"""
简单的 enex 到 Markdown 转换器
支持基本的笔记、标签、附件转换
"""

import xml.etree.ElementTree as ET
import os
import sys
import base64
import re
from datetime import datetime
from pathlib import Path

def sanitize_filename(filename):
    """清理文件名，移除非法字符"""
    filename = re.sub(r'[\u003c\u003e:"/\\|?*]', '_', filename)
    filename = filename.strip(' .')
    return filename[:100]  # 限制长度

def parse_enex(enex_path, output_dir):
    """解析 enex 文件并转换为 Markdown"""
    
    print(f"📖 正在读取: {enex_path}")
    
    tree = ET.parse(enex_path)
    root = tree.getroot()
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 创建附件目录
    attachments_dir = output_path / "_attachments"
    attachments_dir.mkdir(exist_ok=True)
    
    notes_count = 0
    attachments_count = 0
    
    # 命名空间
    ns = {'en': 'http://xml.evernote.com/pub/enml2.dtd'}
    
    for note in root.findall('.//note'):
        try:
            # 获取标题
            title_elem = note.find('title')
            title = title_elem.text if title_elem is not None else "Untitled"
            
            # 获取创建时间
            created_elem = note.find('created')
            created = created_elem.text[:10] if created_elem is not None else datetime.now().strftime('%Y-%m-%d')
            
            # 获取标签
            tags = []
            for tag_elem in note.findall('tag'):
                if tag_elem.text:
                    tags.append(tag_elem.text)
            
            # 获取内容
            content_elem = note.find('content')
            content = ""
            if content_elem is not None and content_elem.text:
                # ENML 内容需要进一步解析
                content = enml_to_markdown(content_elem.text)
            
            # 处理附件
            resources = note.findall('resource')
            for resource in resources:
                try:
                    mime_elem = resource.find('mime')
                    data_elem = resource.find('data')
                    
                    if data_elem is not None and mime_elem is not None:
                        mime = mime_elem.text
                        data = base64.b64decode(data_elem.text)
                        
                        # 生成文件名
                        ext = mime.split('/')[-1] if mime else 'bin'
                        if ext == 'jpeg':
                            ext = 'jpg'
                        
                        res_filename = f"attachment_{attachments_count}.{ext}"
                        res_path = attachments_dir / res_filename
                        
                        with open(res_path, 'wb') as f:
                            f.write(data)
                        
                        attachments_count += 1
                        
                        # 在内容中添加附件链接
                        if mime.startswith('image/'):
                            content += f"\n\n![附件](_attachments/{res_filename})"
                        else:
                            content += f"\n\n[附件](_attachments/{res_filename})"
                
                except Exception as e:
                    print(f"  ⚠️ 附件处理失败: {e}")
            
            # 生成 Markdown 内容
            md_content = f"""---
title: {title}
created: {created}
tags: {tags}
---

# {title}

{content}
"""
            
            # 保存文件
            safe_title = sanitize_filename(title)
            filename = f"{created}_{safe_title}.md"
            file_path = output_path / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            notes_count += 1
            print(f"  ✅ {filename}")
            
        except Exception as e:
            print(f"  ❌ 笔记处理失败: {e}")
    
    # 生成索引文件
    index_content = f"""# 印象笔记导入索引

- 导入日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}
- 源文件: {enex_path}
- 笔记数量: {notes_count}
- 附件数量: {attachments_count}

## 笔记列表

"""
    
    for md_file in sorted(output_path.glob('*.md')):
        if md_file.name != '_index.md':
            index_content += f"- [[{md_file.stem}]]\n"
    
    with open(output_path / '_index.md', 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\n📊 转换完成!")
    print(f"   笔记: {notes_count}")
    print(f"   附件: {attachments_count}")
    print(f"   输出: {output_dir}")

def enml_to_markdown(enml_content):
    """简单转换 ENML 到 Markdown"""
    # 移除 XML 声明和 DOCTYPE
    content = re.sub(r'<\?xml.*?\?>', '', enml_content)
    content = re.sub(r'<!DOCTYPE.*?>', '', content)
    content = re.sub(r'<en-note[^>]*>', '', content)
    content = re.sub(r'</en-note>', '', content)
    
    # 基本 HTML 标签转换
    content = re.sub(r'<div[^>]*>', '\n', content)
    content = re.sub(r'</div>', '', content)
    content = re.sub(r'<p[^>]*>', '\n\n', content)
    content = re.sub(r'</p>', '', content)
    content = re.sub(r'<br[^>]*>', '\n', content)
    content = re.sub(r'<b>(.*?)</b>', r'**\1**', content)
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content)
    content = re.sub(r'<i>(.*?)</i>', r'*\1*', content)
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content)
    content = re.sub(r'<u>(.*?)</u>', r'_\1_', content)
    content = re.sub(r'<s>(.*?)</s>', r'~~\1~~', content)
    content = re.sub(r'<strike>(.*?)</strike>', r'~~\1~~', content)
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', content)
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', content)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n', content)
    content = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1\n', content)
    content = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1\n', content)
    content = re.sub(r'<h6[^>]*>(.*?)</h6>', r'###### \1\n', content)
    content = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', content)
    content = re.sub(r'<ul[^>]*>', '\n', content)
    content = re.sub(r'</ul>', '', content)
    content = re.sub(r'<ol[^>]*>', '\n', content)
    content = re.sub(r'</ol>', '', content)
    content = re.sub(r'<li[^>]*>', '- ', content)
    content = re.sub(r'</li>', '\n', content)
    content = re.sub(r'<code[^>]*>', '`', content)
    content = re.sub(r'</code>', '`', content)
    content = re.sub(r'<pre[^>]*>', '```\n', content)
    content = re.sub(r'</pre>', '\n```', content)
    content = re.sub(r'<blockquote[^>]*>', '\n> ', content)
    content = re.sub(r'</blockquote>', '\n', content)
    content = re.sub(r'<hr[^>]*>', '\n---\n', content)
    
    # 移除所有其他 HTML 标签
    content = re.sub(r'<[^>]+>', '', content)
    
    # 清理多余空白
    content = re.sub(r'\n\n\n+', '\n\n', content)
    content = content.strip()
    
    return content

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 enex2md.py <enex文件路径> [输出目录]")
        sys.exit(1)
    
    enex_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if output_dir is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f"{Path.home()}/Documents/Obsidian Vault/印象笔记导入/{timestamp}"
    
    parse_enex(enex_file, output_dir)
