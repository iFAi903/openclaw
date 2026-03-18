"""
prepare.py - autoresearch 数据准备模块
固定不变的代码，AI 代理不会修改此文件
"""

import os
import requests
import tiktoken
from tqdm import tqdm
import torch
import numpy as np

# 固定常量
DATA_CACHE_DIR = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_BLOCK_SIZE = 1024
DEFAULT_BATCH_SIZE = 64
DEFAULT_VOCAB_SIZE = 50304  # 最接近 50257 的友好数字

def download_file(url: str, fname: str, chunk_size=1024):
    """Download a file with progress bar"""
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(fname, "wb") as file, tqdm(
        desc=fname,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)

def prepare_dataset(dataset_name: str = "openwebtext"):
    """
    准备训练数据集
    
    Args:
        dataset_name: 数据集名称，支持 "openwebtext", "shakespeare", "tiny_shakespeare"
    """
    os.makedirs(DATA_CACHE_DIR, exist_ok=True)
    
    if dataset_name == "tiny_shakespeare":
        input_file_path = os.path.join(DATA_CACHE_DIR, "input.txt")
        if not os.path.exists(input_file_path):
            data_url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
            print(f"Downloading {dataset_name} dataset...")
            download_file(data_url, input_file_path)
        
        with open(input_file_path, "r") as f:
            data = f.read()
        
        n = len(data)
        train_data = data[: int(n * 0.9)]
        val_data = data[int(n * 0.9) :]
        
        # 使用 tiktoken GPT-2 BPE
        enc = tiktoken.get_encoding("gpt2")
        train_ids = enc.encode_ordinary(train_data)
        val_ids = enc.encode_ordinary(val_data)
        
        print(f"Train has {len(train_ids):,} tokens")
        print(f"Val has {len(val_ids):,} tokens")
        
        # 保存为二进制文件
        train_ids = np.array(train_ids, dtype=np.uint16)
        val_ids = np.array(val_ids, dtype=np.uint16)
        train_ids.tofile(os.path.join(DATA_CACHE_DIR, "train.bin"))
        val_ids.tofile(os.path.join(DATA_CACHE_DIR, "val.bin"))
        
        return len(train_ids), len(val_ids)
    
    else:
        raise ValueError(f"Dataset {dataset_name} not supported yet")

def get_batch(split: str, block_size: int = DEFAULT_BLOCK_SIZE, batch_size: int = DEFAULT_BATCH_SIZE, device: str = "cuda"):
    """
    获取一个 batch 的数据
    
    Args:
        split: "train" 或 "val"
        block_size: 序列长度
        batch_size: batch 大小
        device: 设备类型
    
    Returns:
        x, y: 输入和目标张量
    """
    data = np.memmap(os.path.join(DATA_CACHE_DIR, f"{split}.bin"), dtype=np.uint16, mode="r")
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([torch.from_numpy((data[i : i + block_size]).astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy((data[i + 1 : i + 1 + block_size]).astype(np.int64)) for i in ix])
    
    if device == "cuda":
        # pin arrays x,y, which allows us to move them to GPU asynchronously (non_blocking=True)
        x = x.pin_memory().to(device, non_blocking=True)
        y = y.pin_memory().to(device, non_blocking=True)
    else:
        x, y = x.to(device), y.to(device)
    
    return x, y

def estimate_loss(model, ctx, eval_iters: int = 20, block_size: int = DEFAULT_BLOCK_SIZE, batch_size: int = DEFAULT_BATCH_SIZE, device: str = "cuda"):
    """
    评估模型在训练和验证集上的 loss
    
    Returns:
        dict: {"train": train_loss, "val": val_loss}
    """
    out = {}
    model.eval()
    for split in ["train", "val"]:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split, block_size, batch_size, device)
            with ctx:
                logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

def get_lr(it: int, warmup_iters: int, learning_rate: float, lr_decay_iters: int, min_lr: float) -> float:
    """
    学习率调度：线性 warmup + cosine decay
    """
    # 1) linear warmup for warmup_iters steps
    if it < warmup_iters:
        return learning_rate * (it + 1) / (warmup_iters + 1)
    # 2) if it > lr_decay_iters, return min learning rate
    if it > lr_decay_iters:
        return min_lr
    # 3) in between, use cosine decay down to min learning rate
    decay_ratio = (it - warmup_iters) / (lr_decay_iters - warmup_iters)
    assert 0 <= decay_ratio <= 1
    coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio))  # coeff ranges 0..1
    return min_lr + coeff * (learning_rate - min_lr)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="tiny_shakespeare", help="Dataset to prepare")
    args = parser.parse_args()
    
    print(f"Preparing {args.dataset} dataset...")
    train_tokens, val_tokens = prepare_dataset(args.dataset)
    print(f"✅ Dataset prepared: {train_tokens:,} train tokens, {val_tokens:,} val tokens")
    print(f"Data saved to: {DATA_CACHE_DIR}")
