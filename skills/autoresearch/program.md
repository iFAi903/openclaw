# Autoresearch Program

## 任务目标

优化 GPT 小模型在 tiny_shakespeare 数据集上的训练。

## 基线性能

当前基线配置（train.py 中的 Config）：
- 模型：6层，6头，384维
- 训练 5000 steps（约5分钟）
- 基线 val loss: ~2.5

## 优化方向

你可以尝试以下改进：

### 1. 架构优化
- 尝试不同的层数/头数组合
- 使用 RoPE、ALiBi 等位置编码
- 尝试 SwiGLU 替代 GELU
- 使用 RMSNorm 替代 LayerNorm
- 尝试 Grouped Query Attention (GQA)

### 2. 训练优化
- 调整学习率和调度策略
- 尝试不同的优化器（Muon、Lion、Sophia）
- 调整 batch size
- 使用梯度累积模拟大 batch
- 尝试 warmup 策略

### 3. 正则化
- 调整 dropout
- 尝试 weight decay
- 使用 gradient clipping

### 4. 其他技巧
- 使用 bfloat16 训练
- 尝试不同的初始化策略
- 使用 gradient checkpointing 节省内存

## 实验规则

1. **每次实验限时5分钟**（max_iters=5000）
2. **关注 val loss** 作为评估指标
3. **记录改动**：在 Config.notes 中写明你的修改
4. **保存最佳模型**：自动保存为 checkpoint_{experiment_name}.pt

## 成功标准

- val loss < 2.0：良好
- val loss < 1.8：优秀
- val loss < 1.5：突破基线

## 提示

- 小改动，快验证
- 记录每次实验的结果
- 关注 loss 曲线的形状，不只是最终值
- 尝试组合多个优化技巧

## 实验命名规范

experiment_name 格式：
- `baseline`：初始基线
- `lr_{value}`：学习率调整
- `arch_{change}`：架构修改
- `opt_{optimizer}`：优化器修改
- `combo_{desc}`：组合优化

祝实验顺利！
