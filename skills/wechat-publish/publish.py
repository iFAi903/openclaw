#!/usr/bin/env python3
"""
微信公众号发布脚本
支持创建图文消息草稿
"""

import os
import sys
import json
import requests
import argparse
from pathlib import Path

# 微信 API 基础地址
WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"

def get_access_token(app_id: str, app_secret: str) -> str:
    """获取微信 access_token"""
    url = f"{WECHAT_API_BASE}/token"
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "access_token" in data:
            return data["access_token"]
        else:
            print(f"❌ 获取 access_token 失败: {data.get('errmsg', '未知错误')}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)

def upload_thumb_image(access_token: str) -> str:
    """上传封面图片到微信永久素材库，返回 thumb_media_id"""
    # 使用新增永久素材接口
    url = f"{WECHAT_API_BASE}/material/add_material"
    params = {
        "access_token": access_token,
        "type": "thumb"
    }
    
    try:
        # 下载一个默认封面图
        default_image_url = "https://picsum.photos/200/200"
        img_response = requests.get(default_image_url, timeout=10)
        
        if img_response.status_code == 200:
            files = {'media': ('cover.jpg', img_response.content, 'image/jpeg')}
            response = requests.post(url, params=params, files=files, timeout=30)
            data = response.json()
            
            if "media_id" in data:
                print(f"✅ 封面上传成功: {data['media_id'][:20]}...")
                return data.get("media_id")
            else:
                print(f"⚠️ 封面上传失败: {data.get('errmsg', '未知错误')}")
                return None
    except Exception as e:
        print(f"⚠️ 封面上传异常: {e}")
        return None

def upload_image(access_token: str, image_path: str) -> str:
    """上传图片到微信素材库，返回图片 URL"""
    url = f"{WECHAT_API_BASE}/media/uploadimg"
    params = {"access_token": access_token}
    
    try:
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files, timeout=30)
            data = response.json()
            
            if "url" in data:
                return data["url"]
            else:
                print(f"⚠️ 图片上传失败: {data.get('errmsg', '未知错误')}")
                return None
    except Exception as e:
        print(f"⚠️ 图片上传异常: {e}")
        return None

def create_draft(access_token: str, title: str, content: str, author: str = "", digest: str = "") -> dict:
    """创建图文消息草稿"""
    url = f"{WECHAT_API_BASE}/draft/add"
    params = {"access_token": access_token}
    
    # 简单的 Markdown 转 HTML
    html_content = markdown_to_html(content)
    
    # 先上传封面图
    print("🖼️  上传封面图...")
    thumb_media_id = upload_thumb_image(access_token)
    
    # 构建图文消息
    article = {
        "title": title,
        "content": html_content,
        "author": author or "AI",
        "digest": digest or (title[:54] + "..." if len(title) > 54 else title),
        "show_cover_pic": 1,
        "need_open_comment": 1,
        "only_fans_can_comment": 0
    }
    
    # 如果有封面图，添加 thumb_media_id
    if thumb_media_id:
        article["thumb_media_id"] = thumb_media_id
    else:
        print("⚠️ 未上传封面图，继续尝试创建草稿...")
    
    data = {"articles": [article]}
    
    try:
        response = requests.post(url, params=params, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), timeout=30, headers={'Content-Type': 'application/json; charset=utf-8'})
        result = response.json()
        
        # 调试输出
        if result.get("errcode") != 0:
            print(f"📤 请求数据: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}")
        
        if result.get("errcode") == 0 or (result.get("errcode") is None and result.get("media_id")):
            return {
                "success": True,
                "media_id": result.get("media_id"),
                "thumb_media_id": thumb_media_id,
                "msg": "草稿创建成功"
            }
            return {
                "success": True,
                "media_id": result.get("media_id"),
                "thumb_media_id": thumb_media_id,
                "msg": "草稿创建成功"
            }
        else:
            return {
                "success": False,
                "errcode": result.get("errcode"),
                "errmsg": result.get("errmsg")
            }
    except Exception as e:
        return {
            "success": False,
            "errmsg": str(e)
        }

def markdown_to_html(markdown_text: str) -> str:
    """简单的 Markdown 转 HTML"""
    import re
    
    html = markdown_text
    
    # 标题
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体和斜体
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # 链接
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # 代码块
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # 段落
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<h') and not p.startswith('<pre'):
            p = f'<p>{p}</p>'
        html_paragraphs.append(p)
    
    return '\n'.join(html_paragraphs)

def main():
    parser = argparse.ArgumentParser(description='发布内容到微信公众号草稿箱')
    parser.add_argument('--title', '-t', required=True, help='文章标题')
    parser.add_argument('--content', '-c', help='文章内容（Markdown 格式）')
    parser.add_argument('--file', '-f', help='从文件读取内容')
    parser.add_argument('--author', '-a', default='', help='作者名')
    parser.add_argument('--digest', '-d', default='', help='文章摘要')
    parser.add_argument('--app-id', help='微信公众号 AppID（也可从环境变量读取）')
    parser.add_argument('--app-secret', help='微信公众号 AppSecret（也可从环境变量读取）')
    
    args = parser.parse_args()
    
    # 获取凭证
    app_id = args.app_id or os.environ.get('WECHAT_APP_ID')
    app_secret = args.app_secret or os.environ.get('WECHAT_APP_SECRET')
    
    if not app_id or not app_secret:
        print("❌ 错误: 未设置微信公众号凭证")
        print("请设置环境变量 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        print("或在命令行中指定 --app-id 和 --app-secret")
        sys.exit(1)
    
    # 获取内容
    if args.file:
        if not Path(args.file).exists():
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        content = Path(args.file).read_text(encoding='utf-8')
    elif args.content:
        content = args.content
    else:
        print("❌ 错误: 必须提供 --content 或 --file 参数")
        sys.exit(1)
    
    print(f"📝 正在发布: {args.title}")
    print("🔑 获取 access_token...")
    
    # 获取 access_token
    access_token = get_access_token(app_id, app_secret)
    print("✅ 获取 access_token 成功")
    
    # 创建草稿
    print("📤 创建草稿...")
    result = create_draft(access_token, args.title, content, args.author, args.digest)
    
    if result["success"]:
        print(f"✅ {result['msg']}")
        print(f"📋 Media ID: {result['media_id']}")
        if result.get('thumb_media_id'):
            print(f"🖼️  封面图 Media ID: {result['thumb_media_id']}")
        print("\n💡 提示: 登录公众号后台，在「草稿箱」中查看和发布")
    else:
        print(f"❌ 创建草稿失败")
        print(f"错误码: {result.get('errcode')}")
        print(f"错误信息: {result.get('errmsg')}")
        sys.exit(1)

if __name__ == '__main__':
    main()
