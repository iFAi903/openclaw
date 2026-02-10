#!/usr/bin/env python3
"""
Claude Code Runner for OpenClaw
解决无 TTY 环境下 Claude Code 调用卡住的问题

基于 win4r/claude-code-clawdbot-skill 改编
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def find_claude_binary():
    """查找 claude 可执行文件"""
    # 常见安装位置
    possible_paths = [
        "/usr/local/bin/claude",
        "/usr/bin/claude",
        os.path.expanduser("~/.local/bin/claude"),
        os.path.expanduser("~/npm-global/bin/claude"),
        os.path.expanduser("~/.npm-global/bin/claude"),
    ]
    
    # 检查 PATH
    path_env = os.environ.get("PATH", "")
    for path_dir in path_env.split(":"):
        possible_paths.append(os.path.join(path_dir, "claude"))
    
    for path in possible_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    
    return None


def run_with_pty(claude_path, args):
    """使用伪终端运行 Claude Code"""
    # 构建命令
    cmd_parts = [claude_path] + args
    cmd_str = " ".join(cmd_parts)
    
    # 使用 script 命令分配伪终端
    # -q: 静默模式
    # -c: 执行命令
    # /dev/null: 输出到空设备（因为我们只关心 stdout）
    script_cmd = ["script", "-q", "-c", cmd_str, "/dev/null"]
    
    try:
        result = subprocess.run(
            script_cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        # 输出结果
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        
        return result.returncode
    
    except subprocess.TimeoutExpired:
        print("Error: Claude Code execution timed out (5 minutes)", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("Error: 'script' command not found. Please install util-linux or BSD utilities.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error running Claude Code: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Run Claude Code via OpenClaw with TTY support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -p "Return only the single word OK." --permission-mode plan
  
  %(prog)s -p "Run tests and fix failures" --allowedTools "Bash,Read,Edit"
  
  %(prog)s -p "Summarize this repo" --output-format json
        """
    )
    
    parser.add_argument(
        "-p", "--prompt",
        required=True,
        help="The prompt to send to Claude Code"
    )
    
    parser.add_argument(
        "--permission-mode",
        choices=["plan", "accept-edits", "default"],
        default="default",
        help="Permission mode for Claude Code (default: default)"
    )
    
    parser.add_argument(
        "--allowedTools",
        help="Comma-separated list of allowed tools (e.g., 'Bash,Read,Edit')"
    )
    
    parser.add_argument(
        "--output-format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--model",
        help="Model to use (e.g., opus, sonnet)"
    )
    
    parser.add_argument(
        "--claude-path",
        help="Path to claude binary (auto-detected if not specified)"
    )
    
    args = parser.parse_args()
    
    # 查找 claude 二进制文件
    claude_path = args.claude_path or find_claude_binary()
    
    if not claude_path:
        print("Error: Claude Code binary not found.", file=sys.stderr)
        print("Please install Claude Code: npm install -g @anthropic-ai/claude-code", file=sys.stderr)
        print("Or specify the path with --claude-path", file=sys.stderr)
        return 1
    
    # 构建 Claude Code 参数
    claude_args = ["-p", args.prompt]
    
    if args.permission_mode != "default":
        claude_args.extend(["--permission-mode", args.permission_mode])
    
    if args.allowedTools:
        claude_args.extend(["--allowedTools", args.allowedTools])
    
    if args.output_format != "text":
        claude_args.extend(["--output-format", args.output_format])
    
    if args.model:
        claude_args.extend(["--model", args.model])
    
    # 运行
    return run_with_pty(claude_path, claude_args)


if __name__ == "__main__":
    sys.exit(main())