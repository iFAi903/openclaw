#!/bin/bash
# autoresearch 快速启动脚本

echo "🧪 Autoresearch - AI-driven ML Experiments"
echo "============================================"

# 检查 Python
echo "Checking Python..."
python3 --version || { echo "❌ Python 3 not found"; exit 1; }

# 检查 CUDA
echo "Checking CUDA..."
if python3 -c "import torch; print(torch.cuda.is_available())" 2>/dev/null | grep -q "True"; then
    echo "✅ CUDA available"
else
    echo "⚠️ CUDA not available, will use CPU"
fi

# 安装依赖
echo "Installing dependencies..."
pip3 install -q -r requirements.txt

# 准备数据
echo "Preparing dataset..."
python3 prepare.py --dataset tiny_shakespeare

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  python3 run.py --mode single          # 运行单次实验"
echo "  python3 run.py --mode loop            # 持续运行实验"
echo "  python3 run.py --mode leaderboard     # 查看排行榜"
echo ""
echo "Edit train.py to modify the experiment configuration."
