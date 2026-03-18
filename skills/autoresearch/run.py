#!/usr/bin/env python3
"""
run.py - Autoresearch 主运行循环
AI 代理的自主实验驱动程序
"""

import os
import sys
import json
import time
import subprocess
import shutil
from datetime import datetime
from pathlib import Path

# 实验日志文件
EXPERIMENT_LOG = "experiments.json"
TRAIN_FILE = "train.py"
BACKUP_DIR = "backups"

def load_experiments():
    """加载实验历史"""
    if os.path.exists(EXPERIMENT_LOG):
        with open(EXPERIMENT_LOG, 'r') as f:
            return json.load(f)
    return []

def save_experiments(experiments):
    """保存实验历史"""
    with open(EXPERIMENT_LOG, 'w') as f:
        json.dump(experiments, f, indent=2)

def backup_train_file(experiment_name):
    """备份 train.py"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, f"train_{experiment_name}_{int(time.time())}.py")
    shutil.copy(TRAIN_FILE, backup_path)
    return backup_path

def run_experiment(timeout_minutes=5):
    """
    运行一次实验
    
    Returns:
        dict: 实验结果
    """
    print(f"\n{'='*60}")
    print(f"Starting experiment at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 备份当前 train.py
    experiment_name = f"exp_{int(time.time())}"
    backup_path = backup_train_file(experiment_name)
    
    # 运行训练
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, TRAIN_FILE],
            capture_output=True,
            text=True,
            timeout=timeout_minutes * 60
        )
        
        stdout = result.stdout
        stderr = result.stderr
        
        # 解析结果
        # 查找 final loss
        final_train_loss = None
        final_val_loss = None
        best_val_loss = None
        
        for line in stdout.split('\n'):
            if 'Final: train loss' in line:
                parts = line.split(',')
                for part in parts:
                    if 'train loss' in part:
                        final_train_loss = float(part.split()[-1])
                    if 'val loss' in part:
                        final_val_loss = float(part.split()[-1])
            if 'Best val loss:' in line:
                best_val_loss = float(line.split(':')[-1].strip())
        
        elapsed_time = time.time() - start_time
        
        experiment = {
            'name': experiment_name,
            'timestamp': datetime.now().isoformat(),
            'status': 'success',
            'final_train_loss': final_train_loss,
            'final_val_loss': final_val_loss,
            'best_val_loss': best_val_loss,
            'elapsed_time': elapsed_time,
            'backup_path': backup_path,
            'stdout_tail': '\n'.join(stdout.split('\n')[-20:])  # 最后20行
        }
        
        print(f"\n✅ Experiment completed in {elapsed_time:.1f}s")
        print(f"Best val loss: {best_val_loss}")
        
        return experiment
        
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        print(f"\n⏱️ Experiment timed out after {timeout_minutes} minutes")
        
        return {
            'name': experiment_name,
            'timestamp': datetime.now().isoformat(),
            'status': 'timeout',
            'elapsed_time': elapsed_time,
            'backup_path': backup_path
        }
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ Experiment failed: {e}")
        
        return {
            'name': experiment_name,
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e),
            'elapsed_time': elapsed_time,
            'backup_path': backup_path
        }

def print_leaderboard(experiments, top_n=10):
    """打印实验排行榜"""
    print(f"\n{'='*60}")
    print("🏆 Experiment Leaderboard")
    print(f"{'='*60}")
    
    # 按 val loss 排序
    sorted_exps = sorted(
        [e for e in experiments if e.get('best_val_loss') is not None],
        key=lambda x: x['best_val_loss']
    )[:top_n]
    
    for i, exp in enumerate(sorted_exps, 1):
        print(f"{i}. {exp['name']}: val_loss={exp['best_val_loss']:.4f}, "
              f"time={exp.get('elapsed_time', 0):.0f}s")
    
    if not sorted_exps:
        print("No successful experiments yet.")
    
    print(f"{'='*60}\n")

def main():
    """主循环"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Autoresearch - AI-driven ML experiments')
    parser.add_argument('--mode', type=str, default='single', 
                       choices=['single', 'loop', 'leaderboard'],
                       help='Run mode: single experiment, continuous loop, or show leaderboard')
    parser.add_argument('--duration', type=int, default=5,
                       help='Duration per experiment in minutes')
    parser.add_argument('--experiments', type=int, default=100,
                       help='Number of experiments to run in loop mode')
    
    args = parser.parse_args()
    
    experiments = load_experiments()
    
    if args.mode == 'leaderboard':
        print_leaderboard(experiments)
        return
    
    if args.mode == 'single':
        # 运行单次实验
        result = run_experiment(args.duration)
        experiments.append(result)
        save_experiments(experiments)
        print_leaderboard(experiments)
        
    elif args.mode == 'loop':
        # 持续运行实验
        print(f"Starting experiment loop: {args.experiments} experiments")
        print(f"Each experiment limited to {args.duration} minutes")
        print("Press Ctrl+C to stop\n")
        
        try:
            for i in range(args.experiments):
                print(f"\n🧪 Experiment {i+1}/{args.experiments}")
                
                result = run_experiment(args.duration)
                experiments.append(result)
                save_experiments(experiments)
                
                # 显示当前最佳
                best = min([e for e in experiments if e.get('best_val_loss')],
                          key=lambda x: x['best_val_loss'], default=None)
                if best:
                    print(f"🏆 Current best: {best['best_val_loss']:.4f}")
                
                print(f"💾 Total experiments: {len(experiments)}")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Loop interrupted by user")
        
        print_leaderboard(experiments)

if __name__ == "__main__":
    main()
