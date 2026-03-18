"""
train.py - autoresearch 训练模块
⚠️ 这是 AI 代理唯一可以修改的文件

实验目标：在保持模型效果的前提下优化训练
- 可以修改：模型架构、优化器、超参数、batch size
- 不能修改：数据加载（使用 prepare.py 的接口）
"""

import os
import sys
import math
import time
from dataclasses import dataclass

import torch
import torch.nn as nn
from torch.nn import functional as F

# 导入 prepare.py 的固定函数
from prepare import (
    get_batch, estimate_loss, get_lr,
    DEFAULT_BLOCK_SIZE, DEFAULT_BATCH_SIZE, DEFAULT_VOCAB_SIZE,
    DATA_CACHE_DIR
)

# ============== 可修改区域开始 ==============

@dataclass
class Config:
    """模型和训练配置 - AI 可以修改这些参数"""
    # 模型架构
    block_size: int = 1024        # 序列长度
    vocab_size: int = 50304       # 词汇表大小（ GPT-2 是 50257，我们用友好数字）
    n_layer: int = 6              # Transformer 层数
    n_head: int = 6               # 注意力头数
    n_embd: int = 384             # 嵌入维度
    dropout: float = 0.2          # Dropout 率
    
    # 训练参数
    batch_size: int = 64          # Batch size
    learning_rate: float = 1e-3   # 学习率
    max_iters: int = 5000         # 最大迭代次数（5分钟实验用）
    warmup_iters: int = 100       # Warmup 步数
    lr_decay_iters: int = 5000    # 学习率衰减步数
    min_lr: float = 1e-4          # 最小学习率
    
    # 评估和日志
    eval_interval: int = 100      # 评估间隔
    eval_iters: int = 20          # 评估迭代次数
    log_interval: int = 10        # 日志间隔
    
    # 系统
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    compile: bool = True          # 使用 torch.compile
    
    # 实验元数据（AI 可以修改，用于追踪实验）
    experiment_name: str = "baseline"
    notes: str = "初始基线配置"


class CausalSelfAttention(nn.Module):
    """因果自注意力 - AI 可以修改实现方式"""
    
    def __init__(self, config: Config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        
        # 键、查询、值投影
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        # 输出投影
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.register_buffer("bias", torch.tril(torch.ones(config.block_size, config.block_size))
                                     .view(1, 1, config.block_size, config.block_size))
        self.dropout = config.dropout
    
    def forward(self, x):
        B, T, C = x.size()
        
        # 计算查询、键、值
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        
        # 注意力计算（使用 Flash Attention 如果有的话）
        y = F.scaled_dot_product_attention(q, k, v, attn_mask=None, 
                                           dropout_p=self.dropout if self.training else 0,
                                           is_causal=True)
        
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.c_proj(y)
        return y


class MLP(nn.Module):
    """前馈网络 - AI 可以修改"""
    
    def __init__(self, config: Config):
        super().__init__()
        self.c_fc = nn.Linear(config.n_embd, 4 * config.n_embd)
        self.gelu = nn.GELU()
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd)
        self.dropout = nn.Dropout(config.dropout)
    
    def forward(self, x):
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        x = self.dropout(x)
        return x


class Block(nn.Module):
    """Transformer Block - AI 可以修改架构（如更换归一化方式）"""
    
    def __init__(self, config: Config):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = MLP(config)
    
    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


class GPT(nn.Module):
    """GPT 模型 - AI 可以修改整体架构"""
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        
        self.transformer = nn.ModuleDict(dict(
            wte = nn.Embedding(config.vocab_size, config.n_embd),
            wpe = nn.Embedding(config.block_size, config.n_embd),
            drop = nn.Dropout(config.dropout),
            h = nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
            ln_f = nn.LayerNorm(config.n_embd),
        ))
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        
        # 权重共享
        self.transformer.wte.weight = self.lm_head.weight
        
        # 初始化
        self.apply(self._init_weights)
        for pn, p in self.named_parameters():
            if pn.endswith('c_proj.weight'):
                torch.nn.init.normal_(p, mean=0.0, std=0.02/math.sqrt(2 * config.n_layer))
    
    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
    
    def forward(self, idx, targets=None):
        device = idx.device
        b, t = idx.size()
        assert t <= self.config.block_size, f"Sequence length {t} exceeds block size {self.config.block_size}"
        
        pos = torch.arange(0, t, dtype=torch.long, device=device)
        
        tok_emb = self.transformer.wte(idx)
        pos_emb = self.transformer.wpe(pos)
        x = self.transformer.drop(tok_emb + pos_emb)
        for block in self.transformer.h:
            x = block(x)
        x = self.transformer.ln_f(x)
        
        if targets is not None:
            logits = self.lm_head(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1)
        else:
            logits = self.lm_head(x[:, [-1], :])
            loss = None
        
        return logits, loss
    
    def configure_optimizers(self, weight_decay, learning_rate, betas, device_type):
        """配置优化器 - AI 可以修改优化算法"""
        param_dict = {pn: p for pn, p in self.named_parameters() if p.requires_grad}
        decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
        nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
        optim_groups = [
            {'params': decay_params, 'weight_decay': weight_decay},
            {'params': nodecay_params, 'weight_decay': 0.0}
        ]
        
        # 使用 fused AdamW（如果可用）
        fused_available = 'fused' in inspect.signature(torch.optim.AdamW).parameters
        use_fused = fused_available and device_type == 'cuda'
        extra_args = dict(fused=True) if use_fused else dict()
        
        optimizer = torch.optim.AdamW(optim_groups, lr=learning_rate, betas=betas, **extra_args)
        return optimizer


# ============== 可修改区域结束 ==============


def train(config: Config = None):
    """训练函数 - AI 可以修改训练循环"""
    if config is None:
        config = Config()
    
    print(f"Starting experiment: {config.experiment_name}")
    print(f"Device: {config.device}")
    print(f"Notes: {config.notes}")
    print("-" * 50)
    
    # 设置随机种子
    torch.manual_seed(1337)
    
    # 创建模型
    model = GPT(config)
    model = model.to(config.device)
    
    # 编译模型（加速）
    if config.compile and hasattr(torch, 'compile'):
        print("Compiling model...")
        model = torch.compile(model)
    
    # 配置优化器
    optimizer = model.configure_optimizers(
        weight_decay=0.1,
        learning_rate=config.learning_rate,
        betas=(0.9, 0.95),
        device_type=config.device
    )
    
    # 训练循环
    ctx = torch.amp.autocast(device_type=config.device, dtype=torch.bfloat16 if config.device == 'cuda' else torch.float32)
    
    best_val_loss = float('inf')
    t0 = time.time()
    
    for iter_num in range(config.max_iters):
        # 学习率调度
        lr = get_lr(iter_num, config.warmup_iters, config.learning_rate, 
                    config.lr_decay_iters, config.min_lr)
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
        
        # 评估
        if iter_num > 0 and iter_num % config.eval_interval == 0:
            losses = estimate_loss(model, ctx, config.eval_iters, 
                                   config.block_size, config.batch_size, config.device)
            print(f"Step {iter_num}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
            
            if losses['val'] < best_val_loss:
                best_val_loss = losses['val']
                # 保存最佳模型
                checkpoint = {
                    'model': model.state_dict(),
                    'optimizer': optimizer.state_dict(),
                    'config': config,
                    'iter_num': iter_num,
                    'best_val_loss': best_val_loss,
                }
                torch.save(checkpoint, f"checkpoint_{config.experiment_name}.pt")
        
        # 训练步骤
        xb, yb = get_batch('train', config.block_size, config.batch_size, config.device)
        
        with ctx:
            logits, loss = model(xb, yb)
        
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        
        # 日志
        if iter_num % config.log_interval == 0:
            dt = time.time() - t0
            print(f"Iter {iter_num}: loss {loss.item():.4f}, time {dt*1000:.2f}ms, lr {lr:.2e}")
            t0 = time.time()
    
    # 最终评估
    losses = estimate_loss(model, ctx, config.eval_iters, 
                           config.block_size, config.batch_size, config.device)
    print(f"\nFinal: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
    print(f"Best val loss: {best_val_loss:.4f}")
    
    return {
        'final_train_loss': losses['train'],
        'final_val_loss': losses['val'],
        'best_val_loss': best_val_loss,
        'experiment': config.experiment_name
    }


if __name__ == "__main__":
    import inspect
    
    # 运行基线实验
    config = Config()
    result = train(config)
    print(f"\n✅ Experiment completed: {result}")
