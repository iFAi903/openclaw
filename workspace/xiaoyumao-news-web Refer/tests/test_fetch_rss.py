#!/usr/bin/env python3
"""
基础测试套件 - 小羽毛 AI 新闻早报

运行方式：
    python3 -m pytest tests/test_fetch_rss.py -v
    或
    python3 tests/test_fetch_rss.py
"""

import json
import os
import sys
import unittest
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestFetchRSS(unittest.TestCase):
    """RSS 抓取功能测试"""
    
    def setUp(self):
        """测试前置设置"""
        self.project_dir = Path(__file__).parent.parent
        self.daily_data_file = self.project_dir / "daily_data.json"
    
    def test_01_daily_data_json_exists_after_fetch(self):
        """
        冒烟测试：运行 fetch_news_final.py 后应生成 daily_data.json
        
        验证点：
        1. 脚本执行成功（返回码 0）
        2. daily_data.json 文件存在
        3. 文件内容是有效 JSON
        """
        import subprocess
        
        result = subprocess.run(
            ["python3", str(self.project_dir / "fetch_news_final.py")],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(self.project_dir)
        )
        
        self.assertEqual(
            result.returncode, 0,
            f"脚本执行失败: {result.stderr}"
        )
        self.assertTrue(
            self.daily_data_file.exists(),
            "daily_data.json 未生成"
        )
        
        # 验证 JSON 有效性
        try:
            with open(self.daily_data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.fail(f"daily_data.json 不是有效的 JSON: {e}")
        
        return data
    
    def test_02_daily_data_structure(self):
        """
        验证 daily_data.json 数据结构完整性
        
        必须包含的字段：
        - date: 日期字符串
        - news: 新闻列表
        - products: 产品列表
        - quote: 引言
        - summary: 摘要
        - meta: 元数据
        """
        data = self.test_01_daily_data_json_exists_after_fetch()
        
        required_fields = ['date', 'news', 'products', 'quote', 'summary', 'meta']
        for field in required_fields:
            self.assertIn(
                field, data,
                f"缺少必需字段: {field}"
            )
        
        # 验证 meta 字段
        meta = data['meta']
        meta_fields = ['rss_sources_total', 'rss_sources_success', 'total_fetched', 'unique_news', 'final_news']
        for field in meta_fields:
            self.assertIn(field, meta, f"meta 缺少字段: {field}")
        
        # 验证数据类型
        self.assertIsInstance(data['news'], list)
        self.assertIsInstance(data['products'], list)
        self.assertIsInstance(data['quote'], str)
    
    def test_03_news_item_structure(self):
        """
        验证新闻条目结构
        
        每个新闻条目必须包含：
        - title: 标题
        - source: 来源
        - url: 链接
        - summary: 摘要
        - type: 类型
        """
        data = self.test_01_daily_data_json_exists_after_fetch()
        
        if not data['news']:
            self.skipTest("没有获取到新闻")
        
        required_news_fields = ['title', 'source', 'url', 'summary', 'type']
        
        for i, news in enumerate(data['news']):
            for field in required_news_fields:
                self.assertIn(
                    field, news,
                    f"第 {i+1} 条新闻缺少字段: {field}"
                )
            
            # 验证字段类型和值
            self.assertIsInstance(news['title'], str)
            self.assertTrue(len(news['title']) > 0, f"第 {i+1} 条新闻标题为空")
            self.assertTrue(news['url'].startswith('http'), f"第 {i+1} 条新闻 URL 无效")
    
    def test_04_security_no_hardcoded_tokens(self):
        """
        安全测试：确保代码中没有硬编码密钥
        
        检查：
        - vcp_ 开头的 Vercel token
        - 常见密钥模式
        """
        excluded_patterns = [
            r'vcp_[a-zA-Z0-9]{20,}',
            r'sk-[a-zA-Z0-9]{20,}',  # OpenAI style keys
            r'ghp_[a-zA-Z0-9]{20,}',  # GitHub PAT
        ]
        
        files_to_check = [
            self.project_dir / "daily-cron.sh",
            self.project_dir / "fetch_news_final.py",
        ]
        
        import re
        
        for file_path in files_to_check:
            if not file_path.exists():
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for pattern in excluded_patterns:
                matches = re.findall(pattern, content)
                self.assertEqual(
                    len(matches), 0,
                    f"{file_path.name} 中发现硬编码密钥: {matches[:1]}"
                )


class TestCronScript(unittest.TestCase):
    """Cron 脚本测试"""
    
    def test_cron_script_syntax(self):
        """
        验证 daily-cron.sh 语法正确性
        """
        import subprocess
        
        script_path = Path(__file__).parent.parent / "daily-cron.sh"
        
        # 使用 bash -n 检查语法
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(
            result.returncode, 0,
            f"脚本语法错误: {result.stderr}"
        )
    
    def test_cron_script_uses_env_token(self):
        """
        验证脚本从环境变量读取 Token
        """
        script_path = Path(__file__).parent.parent / "daily-cron.sh"
        
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 验证使用环境变量模式
        self.assertIn(
            'VERCEL_TOKEN="${VERCEL_TOKEN:-}"',
            content,
            "脚本应使用环境变量读取 VERCEL_TOKEN"
        )
        
        # 验证有检查逻辑
        self.assertIn(
            'if [[ -z "$VERCEL_TOKEN" ]]',
            content,
            "脚本应检查 VERCEL_TOKEN 是否设置"
        )


# =============================================================================
# 简单运行器（不需要 pytest）
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("小羽毛 AI 新闻早报 - 基础测试套件")
    print("=" * 70)
    
    # 运行所有测试
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestFetchRSS))
    suite.addTests(loader.loadTestsFromTestCase(TestCronScript))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出摘要
    print("\n" + "=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"运行测试: {result.testsRun}")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("\n❌ 存在失败的测试")
        sys.exit(1)
