# karpathy/autoresearch Skill

让 AI 代理自主运行机器学习实验的自动化研究工具。

## 核心概念

autoresearch 是一个 AI 驱动的自动化实验框架，核心思想是：
- 给 AI 代理一个小型真实的 LLM 训练环境
- 让 AI 自主修改代码、训练、评估、迭代
-  overnight 运行数百次实验，醒来查看结果

## 文件结构

```
autoresearch/
├── prepare.py      # 准备数据、常量、工具函数（AI 不修改）
├── train.py        # 训练代码（AI 唯一可修改的文件）
├── program.md      # 给 AI 的指令和上下文
├── run.py          # 主运行循环
├── requirements.txt # Python 依赖
└── setup.sh        # 快速启动脚本
```

## 快速开始

### 1. 初始化环境

```bash
cd ~/.openclaw/workspace/iFAi/skills/autoresearch
./setup.sh
```

### 2. 运行单次实验（测试）

```bash
python3 run.py --mode single --duration 5
```

### 3. 启动自主研究循环

```bash
# 运行 100 次实验，每次最多 5 分钟
python3 run.py --mode loop --experiments 100 --duration 5
```

### 4. 查看排行榜

```bash
python3 run.py --mode leaderboard
```

## AI 实验工作流

### 实验 1：修改 train.py

编辑 `train.py` 中的 Config 类：
```python
@dataclass
class Config:
    n_layer: int = 8        # 增加层数
    n_head: int = 8         # 增加头数
    n_embd: int = 512       # 增加维度
    learning_rate: float = 5e-4  # 调整学习率
    experiment_name: str = "deeper_model"
    notes: str = "增加模型深度，观察效果"
```

### 实验 2：运行并记录结果

```bash
python3 run.py --mode single
```

结果会自动保存到 `experiments.json`

### 实验 3：对比结果

```bash
python3 run.py --mode leaderboard
```

输出示例：
```
🏆 Experiment Leaderboard
============================================================
1. exp_1678901234: val_loss=1.8234, time=298s
2. exp_1678901000: val_loss=2.0123, time=301s
3. baseline: val_loss=2.4567, time=295s
============================================================
```

### 实验 4：持续迭代

根据排行榜结果，进一步修改 train.py 并重复。

## 可修改的优化方向

### 架构优化
```python
# 尝试更深的网络
n_layer: int = 12
n_head: int = 12
n_embd: int = 768

# 尝试不同的归一化
# 在 Block 类中修改：
self.ln_1 = nn.RMSNorm(config.n_embd)  # 替代 LayerNorm
```

### 训练优化
```python
# 调整学习率调度
learning_rate: float = 3e-4
warmup_iters: int = 200
lr_decay_iters: int = 4000

# 使用不同的优化器
# 在 configure_optimizers 中修改
```

### 超参数搜索
```python
# 尝试更大的 batch size
batch_size: int = 128  # 需要更多显存

# 或者使用梯度累积
# 在训练循环中修改
```

## 实际案例

Karpathy 用 autoresearch 优化 nanoGPT：
- 约 700 次实验
- 2 天时间
- 在已优化代码基础上再提升 11% 速度

## 注意事项

1. **GPU 需求**：需要 CUDA GPU 进行训练，CPU 会非常慢
2. **时间成本**：每次训练约 5 分钟（5000 steps），overnight 可运行数十到数百次实验
3. **代码安全**：train.py 是 AI 唯一可修改的文件，prepare.py 和 run.py 受保护
4. **实验记录**：每次实验自动备份到 `backups/` 目录

## 团队协作

### 分享实验

```bash
# 导出最佳实验
cp backups/train_best_*.py shared_experiments/
```

### 复现实验

```bash
# 复制实验配置
cp backups/train_exp_1678901234.py train.py
python3 run.py --mode single
```

### 团队排行榜

将 `experiments.json` 提交到 git，团队共享实验结果：
```bash
git add experiments.json backups/
git commit -m "feat: add experiments from overnight run"
git push
```

## 高级用法

### 自定义评估指标

在 `train.py` 中添加自定义指标：
```python
def custom_metric(model, data):
    # 你的自定义评估逻辑
    return score
```

### 多 GPU 训练

修改 `Config`：
```python
device: str = "cuda:0"  # 指定 GPU
# 或使用数据并行
```

### 长时间运行

使用 `tmux` 或 `screen`：
```bash
tmux new -s autoresearch
python3 run.py --mode loop --experiments 1000 --duration 5
# Ctrl+B, D  detach
tmux attach -t autoresearch  # 重新连接
```

## 参考

- 原始仓库：https://github.com/karpathy/autoresearch
- 作者：Andrej Karpathy
- 基于：nanoGPT (https://github.com/karpathy/nanoGPT)

## License

MIT License - 与原始 nanoGPT 保持一致
