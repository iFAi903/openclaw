"""
邮箱验证器 - 判断字符串是否为有效邮箱

使用方法:
    from output_email_validator import is_valid_email
    
    # 验证邮箱
    is_valid = is_valid_email("user@example.com")
"""

import re


def is_valid_email(email: str) -> bool:
    """
    判断字符串是否为有效邮箱地址。
    
    使用正则表达式匹配常见的邮箱格式规则：
    - 用户名部分：字母、数字、下划线、点、连字符
    - @ 符号
    - 域名部分：包含点的域名格式
    
    Args:
        email: 待验证的邮箱字符串
        
    Returns:
        bool: 有效返回 True，无效返回 False
    """
    if not isinstance(email, str) or not email:
        return False
    
    # 邮箱正则表达式模式（更严格版本）
    # 用户名: 字母数字开头，可包含 ._-+，但不能有连续点
    # 域名: 字母数字开头，可包含 -，但不能有连续点，必须有 . 和顶级域名
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+-]*(?<![.])@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,63}$'
    
    # 额外检查：不允许连续点号
    if '..' in email:
        return False
    
    return bool(re.match(pattern, email))


# ============== 测试用例 ==============

def test_is_valid_email():
    """运行所有测试用例并输出结果"""
    test_cases = [
        # (输入, 期望结果, 说明)
        # 有效邮箱
        ("user@example.com", True, "标准邮箱"),
        ("test.email@domain.org", True, "包含点的用户名"),
        ("user_name@test-site.com", True, "下划线和连字符"),
        ("a@b.co", True, "最短有效邮箱"),
        ("john.doe@company.io", True, "公司邮箱"),
        ("123@456.com", True, "纯数字"),
        ("user+tag@example.com", True, "带+标签"),
        
        # 无效邮箱
        ("", False, "空字符串"),
        ("invalid", False, "无@符号"),
        ("@example.com", False, "用户名缺失"),
        ("user@", False, "域名缺失"),
        ("user@domain", False, "缺少顶级域名"),
        ("user..name@example.com", False, "连续点号（根据宽松规则可能通过）"),
        (".user@example.com", False, "以点开头的用户名"),
        ("user@.example.com", False, "以点开头的域名"),
        ("user@domain..com", False, "连续点号域名"),
        ("user name@example.com", False, "包含空格"),
        ("user@exam ple.com", False, "域名包含空格"),
        ("user@example", False, "过短顶级域名"),
        (None, False, "None值"),
        (123, False, "非字符串类型"),
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("📧 邮箱验证器测试")
    print("=" * 60)
    
    for email, expected, description in test_cases:
        result = is_valid_email(email)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            
        print(f"{status} | {description}")
        print(f"       输入: {repr(email)}")
        print(f"       期望: {expected}, 实际: {result}")
        print()
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    # 运行测试
    success = test_is_valid_email()
    exit(0 if success else 1)
