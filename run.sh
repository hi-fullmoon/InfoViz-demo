#!/bin/bash

# InfoViz-demo 启动脚本
# 使用方法: ./run.sh [参数]
# 参数: test - 运行测试, run - 运行主程序 (默认)

# 激活虚拟环境（如果存在）
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "⚠️  未找到 .venv，尝试使用系统 Python 运行..."
fi

# 检查参数
if [ "$1" = "test" ]; then
    echo "🧪 运行测试模式..."
    python test.py
elif [ "$1" = "run" ] || [ -z "$1" ]; then
    echo "🚀 运行主程序..."
    python main.py
else
    echo "使用方法:"
    echo "  ./run.sh test - 运行测试"
    echo "  ./run.sh run  - 运行主程序"
    echo "  ./run.sh      - 运行主程序 (默认)"
fi
